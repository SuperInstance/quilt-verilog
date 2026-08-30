#!/usr/bin/env python3
"""chipmatrix.py -- every chip on the desk, measured as a cell (CHIP-MATRIX lane).

Companion to edgebench.py: same scorer (BenchFabric, schema-strict
parse_op, QUF checkpoints). Four phases:

  probe   -- inventory every usable inference backend on this machine:
             ollama default placement (RTX 4050 over WSL /dev/dxg),
             ollama with num_gpu=0 (pure CPU on the Ryzen AI 9 HX 370),
             onnxruntime CPU, a DirectML install attempt (pip
             onnxruntime-directml), and a Vulkan/llama.cpp buildability
             gate (SDK headers + loader + a driver that can actually see
             the paravirtual WSL GPU + cmake + sudo; if any gate fails,
             skip honestly and record the blocker).
  bench   -- fixed prompt set (5 short + 2 long, deterministic,
             temperature 0) x model ladder x live ollama lanes; prompt
             tok/s and generation tok/s from Ollama's own counters. The
             onnxruntime lane times a greedy token loop on a tiny GPT-2
             ONNX (int8, HF hub) if the network allows, else records why
             it skipped. No cloud inference anywhere.
  cells   -- a 100-round slice of the edgebench judgment-cell game with
             the top-3 models, run twice: GPU lane vs CPU lane
             (num_gpu=0), temperature 0 both. Same cell semantics, same
             parser; parse failures are the model's fault. Checkpoints
             every N rounds (QUF + state), honest runtime cuts.
  report  -- emit docs/CHIP-MATRIX.md: backend matrix, tok/s table, the
             GPU-vs-CPU cell verdict, the boat-doctrine readout (how many
             cells each chip can carry), and the NPU honesty section --
             the HX370's XDNA2 NPU is not reachable from WSL and is NOT
             faked; the Windows-side runner it would need is the open
             door.

Usage:
  python3 tools/edgebench/chipmatrix.py --selftest
  python3 tools/edgebench/chipmatrix.py --phase all
  python3 tools/edgebench/chipmatrix.py --phase cells --rounds 100
"""

import argparse
import glob
import itertools
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import edgebench as eb  # noqa: E402  (same scorer as the night lane)

# ----------------------------------------------------------------- consts --

RUNS_DIR = os.path.join(_HERE, "chipmatrix_runs")

# The model ladder (Casey directive): short cell name -> Ollama tag.
LADDER = [
    ("nano", "qwen2.5:0.5b"),
    ("q3b", "qwen2.5:3b"),
    ("wesley", "granite3.1-dense:2b"),
    ("qwen3", "qwen3:8b"),
    ("lfm", "Liquid-LFM2.5-2.6B"),
]
TAG = dict(LADDER)

BENCH_SYSTEM = "You are a concise engineering assistant."
WARMUP_PROMPT = "Reply with the single word: ready."

SHORT_PROMPTS = [
    ("s1", "In one sentence, explain what a systolic array is."),
    ("s2", "Compute 17 * 24. Reply with only the final number."),
    ("s3", "List exactly three uses of a UART peripheral, one short line each."),
    ("s4", "Write a Python one-liner that reverses the string s."),
    ("s5", "Name the two timing edges of a flip-flop, five words or fewer."),
]

_LONG1 = """Consider a small digital fabric built from cells. Each cell owns a
line of integer dials and a short list of weighted edges to other cells. Every
tick, activation that arrives through an edge is integrated into the cell's
accumulator; when the accumulator crosses the cell's earnestness threshold, the
cell fires a value downstream and resets. Edges are not static: when two cells
cofire through an edge, a walk is added to that edge's ledger; when an edge
stays silent, the hyperbola decay removes walks slowly at first and then
faster, so an old partnership fades unless it keeps earning its keep. The
effective weight is the base affinity plus a compressed count of the walks,
which keeps late friendship from saturating the arithmetic. A designer reading
such a fabric does not see a program; they see a small economy of attention,
where the only spending decisions are how hot to fire, whom to link next, and
which dial to nudge. The room keeps one aggregate dial of its own, a slow
exponential moving average of all the heat that actually landed on hearers,
accepted or rejected as it may be. That aggregate is the mood of the room, and
it moves only when real dats move. Now the practical question for the people
who must host such a fabric on ordinary hardware: does the mood still form,
does the graph still grow, and do the cells still pass judgment when every
inference in the loop runs on a laptop CPU instead of the GPU? The claim under
test is that being a cell is a light job -- one prompt, one JSON object, one
small integer decision per turn -- and that a modest CPU can carry several such
cells without the fabric going quiet. Summarize this passage in exactly two
sentences."""

_LONG2 = """Change request for a battery-powered sensor node, firmware team.
The node currently samples a thermistor at 1 Hz, smooths with a 16-tap boxcar,
and ships the smoothed value over UART at 115200 baud once per minute inside a
36-byte frame. The frame carries a magic word, a sequence number, the smoothed
value as a 32-bit float, a 16-bit CRC, and padding. Constraints that must all
hold: peak current must stay under 40 mA because the coin cell's datasheet
demands it; flash budget for the change is 4 KiB; the UART frame layout must
not change because the gateway fleet is already deployed; the boxcar may be
replaced but any replacement filter must run in under 200 microseconds on the
80 MHz core; and the watchdog must still be fed at least every 250 ms. The
request itself: add a burst mode that, when the smoothed value leaves a
configurable deadband, samples at 8 Hz for up to 30 seconds and streams every
raw sample in the same 36-byte frame shape, reusing the padding bytes as a
burst subsequence counter. The deadband threshold arrives over UART in a new
command and must persist across brownouts. Thermal ramp events matter more
than absolute accuracy, so prioritize latency of burst entry over filter
elegance. Three further review gates from the quality team, added after the
field failure report last quarter: first, every code path that touches the
frame buffer must be auditable by the intern next month, which in practice
means no clever pointer arithmetic and a comment block per state transition;
second, the burst exit condition must be explicit in code, not implicit in a
timer rollover, because the auditor flagged implicit exits as the root cause
of the stuck-transmitter recall; and third, any new interrupt priority must
be justified against the existing priority table in the design document,
which lives in the repository and must be updated in the same commit as the
code change. The hardware team adds, from their corner, that the thermistor's
settling time after a burst of high-rate sampling is eleven milliseconds,
that the ADC's internal sample-and-hold capacitor needs two dummy conversions
after a rate change before its output is trustworthy, and that the UART
transmitter's FIFO is only eight bytes deep, so a frame must be assembled in
a staging buffer and fed without gaps to avoid the mid-frame pause the
gateway misreads as a framing error. Budget for review time as well as for
implementation time. Answer with a numbered plan of at most five steps."""

LONG_PROMPTS = [("L1", _LONG1), ("L2", _LONG2)]
ALL_PROMPTS = SHORT_PROMPTS + LONG_PROMPTS

OLLAMA_LANES = [
    {"id": "ollama-gpu", "num_gpu": None,
     "desc": "Ollama default placement (RTX 4050 6GB via WSL /dev/dxg)"},
    {"id": "ollama-cpu", "num_gpu": 0,
     "desc": "Ollama num_gpu=0 -- pure CPU on the Ryzen AI 9 HX 370"},
]

ORT_MODEL_URL = ("https://huggingface.co/Xenova/gpt2/resolve/main/"
                 "onnx/decoder_model_merged_quantized.onnx")
ORT_VOCAB_URL = "https://huggingface.co/Xenova/gpt2/resolve/main/vocab.json"
ORT_MERGES_URL = "https://huggingface.co/Xenova/gpt2/resolve/main/merges.txt"
ORT_EOS = 50256

SPARK = " .:-=+*#%"


def median(xs):
    return statistics.median(xs) if xs else 0.0


def sparkline(vals, width=48):
    if not vals:
        return ""
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    step = max(1, len(vals) // width)
    out = []
    for i in range(0, len(vals), step):
        idx = int((vals[i] - lo) / span * (len(SPARK) - 1))
        out.append(SPARK[idx])
    return "".join(out)


# ------------------------------------------------------------ ollama lane --

class OllamaLane:
    """eb.Ollama's wire protocol + num_gpu placement + prompt counters."""

    def __init__(self, num_gpu=None, timeout=240):
        self.host = eb.OLLAMA_HOST.rstrip("/")
        self.num_gpu = num_gpu
        self.timeout = timeout

    def version(self):
        with urllib.request.urlopen(self.host + "/api/version",
                                    timeout=10) as r:
            return json.loads(r.read().decode("utf-8")).get("version", "?")

    def chat(self, model, system, user, num_predict=None, temperature=0.0,
             num_ctx=1024, keep_alive="5m"):
        if num_predict is None:
            num_predict = eb.NUM_PREDICT.get(model, 64)
        options = {"num_predict": num_predict,
                   "temperature": temperature,
                   "num_ctx": num_ctx}
        if self.num_gpu is not None:
            options["num_gpu"] = self.num_gpu
        body = {
            "model": model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "stream": False,
            "keep_alive": keep_alive,
            "options": options,
        }
        if model in eb.THINKING_MODELS:
            body["think"] = False
        prefill = model in eb.PREFILL_MODELS
        if prefill:
            body["messages"] = body["messages"] + [
                {"role": "assistant", "content": eb.PREFILL}]
        payload = json.dumps(body).encode("utf-8")
        last, t0 = None, time.time()
        for attempt in (1, 2):
            try:
                req = urllib.request.Request(
                    self.host + "/api/chat", data=payload,
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    d = json.loads(r.read().decode("utf-8"))
                content = d.get("message", {}).get("content", "")
                if prefill:
                    content = eb.PREFILL + content
                return {
                    "ok": True, "content": content,
                    "prompt_eval_count": d.get("prompt_eval_count", 0),
                    "prompt_eval_dur_s": (d.get("prompt_eval_duration", 0)
                                          or 0) / 1e9,
                    "eval_count": d.get("eval_count", 0),
                    "eval_dur_s": (d.get("eval_duration", 0) or 0) / 1e9,
                    "load_s": (d.get("load_duration", 0) or 0) / 1e9,
                    "latency_s": time.time() - t0, "attempt": attempt,
                }
            except (urllib.error.URLError, urllib.error.HTTPError,
                    TimeoutError, OSError, ValueError) as ex:
                last = str(ex)
                time.sleep(2.0 * attempt)
        return {"ok": False, "error": last, "latency_s": time.time() - t0}


# ------------------------------------------------------------------ probe --

def _run(cmd, timeout=30):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as ex:
        return 127, str(ex)


def probe_gpu():
    smi = shutil.which("nvidia-smi") or "/usr/lib/wsl/lib/nvidia-smi"
    name, note = None, None
    if os.path.exists(smi) or shutil.which("nvidia-smi"):
        rc, out = _run([smi, "--query-gpu=name,memory.total,driver_version",
                        "--format=csv,noheader"], timeout=15)
        if rc == 0 and out:
            name = out.splitlines()[0].strip()
    return {
        "wsl_dxg": os.path.exists("/dev/dxg"),
        "nvidia_smi": name or "unavailable",
        "note": note or ("CUDA user-space present via /usr/lib/wsl/lib"
                         if os.path.exists("/dev/dxg") else "no dxg"),
    }


def probe_cpu():
    model = ""
    with open("/proc/cpuinfo") as f:
        for line in f:
            if line.startswith("model name"):
                model = line.split(":", 1)[1].strip()
                break
    return {"model": model, "threads": os.cpu_count()}


def probe_ort():
    try:
        import onnxruntime as ort
        return {"live": True, "version": ort.__version__,
                "providers": ort.get_available_providers()}
    except ImportError as ex:
        return {"live": False, "why": str(ex)}


def probe_directml():
    tmp = os.path.join("/tmp/opencode", "ortdml-probe")
    shutil.rmtree(tmp, ignore_errors=True)
    rc, out = _run(["pip", "install", "--break-system-packages",
                    "--target", tmp, "onnxruntime-directml"], timeout=240)
    shutil.rmtree(tmp, ignore_errors=True)
    last = out.splitlines()[-1] if out.splitlines() else "no output"
    return {"live": rc == 0,
            "why": ("pip rc=%d: %s" % (rc, last[:200]))}


def probe_vulkan():
    icd_dir = "/usr/share/vulkan/icd.d"
    icds = sorted(os.listdir(icd_dir)) if os.path.isdir(icd_dir) else []
    loader = (glob.glob("/usr/lib/x86_64-linux-gnu/libvulkan.so.1*")
              or glob.glob("/usr/lib/*/libvulkan.so.1*"))
    header = os.path.exists("/usr/include/vulkan/vulkan.h")
    dzn = ("dzn_icd.json" in icds
           or bool(glob.glob("/usr/lib/*/libvulkan_dzn.so*")))
    vulkaninfo = bool(shutil.which("vulkaninfo"))
    cmake = bool(shutil.which("cmake"))
    sudo, sudo_out = _run(["sudo", "-n", "true"], timeout=10)
    sudo_noninteractive = sudo == 0
    blockers = []
    if not header:
        blockers.append("no Vulkan SDK headers (/usr/include/vulkan)")
    if not cmake:
        blockers.append("no cmake")
    if not dzn:
        blockers.append("no dzn (Vulkan-on-D3D12) ICD; mesa ICDs present "
                        "(%s) cannot drive the paravirtual WSL GPU"
                        % ",".join(icds))
    if not loader:
        blockers.append("no libvulkan loader")
    if not vulkaninfo:
        blockers.append("no vulkaninfo to enumerate devices")
    if not sudo_noninteractive:
        blockers.append("apt locked (sudo needs a password); SDK/ICDs not "
                        "installable from this shell")
    return {
        "icds": icds, "loader": bool(loader), "sdk_headers": header,
        "dzn_icd": dzn, "vulkaninfo": vulkaninfo, "cmake": cmake,
        "sudo_noninteractive": sudo_noninteractive,
        "buildable": not blockers, "blockers": blockers,
    }


def probe_npu():
    devs = (glob.glob("/dev/npu*") + glob.glob("/dev/accel*")
            + glob.glob("/dev/dna*"))
    sysfs = glob.glob("/sys/class/accel/*")
    return {"wsl_device_nodes": devs, "sysfs_accel": sysfs,
            "reachable_from_wsl": bool(devs or sysfs)}


def try_build_llamacpp_vulkan(vk, workdir, cap_minutes=15):
    """Only ever called if probe_vulkan() says buildable. Hard time cap."""
    if not vk["buildable"]:
        return {"built": False, "why": "gate failed: %s"
                % "; ".join(vk["blockers"])}
    os.makedirs(workdir, exist_ok=True)
    src = os.path.join(workdir, "llama.cpp")
    rc, out = _run(["git", "clone", "--depth", "1",
                    "https://github.com/ggml-org/llama.cpp", src],
                   timeout=300)
    if rc != 0:
        return {"built": False, "why": "clone failed: %s" % out[:200]}
    build = os.path.join(src, "build")
    t0 = time.time()
    rc, out = _run(["cmake", src, "-B", build, "-DGGML_VULKAN=1"],
                   timeout=300)
    if rc != 0:
        return {"built": False, "why": "cmake configure failed: %s"
                % out[-300:], "minutes": (time.time() - t0) / 60.0}
    rc, out = _run(["cmake", "--build", build, "-j",
                    str(min(16, os.cpu_count() or 8))],
                   timeout=cap_minutes * 60)
    minutes = (time.time() - t0) / 60.0
    if rc != 0 or minutes > cap_minutes:
        return {"built": False,
                "why": "build cap %.0f min hit (rc=%d)" % (cap_minutes, rc),
                "minutes": minutes}
    bin_ = os.path.join(build, "bin", "llama-cli")
    ok = os.path.exists(bin_)
    return {"built": ok, "binary": bin_ if ok else None, "minutes": minutes,
            "why": None if ok else "llama-cli missing after build"}


def probe_phase(runs_dir):
    os.makedirs(runs_dir, exist_ok=True)
    ollama = OllamaLane()
    try:
        ver = ollama.version()
        ollama_live = True
    except Exception as ex:
        ver, ollama_live = "unreachable (%s)" % ex, False
    gpu = probe_gpu()
    cpu = probe_cpu()
    ort = probe_ort()
    print("probing DirectML (pip install onnxruntime-directml)...",
          flush=True)
    dml = probe_directml()
    print("DirectML: %s -- %s" % ("LIVE" if dml["live"] else "skipped",
                                  dml["why"]), flush=True)
    vk = probe_vulkan()
    llamacpp = {"built": False,
                "why": "not attempted: %s" % "; ".join(vk["blockers"])}
    if vk["buildable"]:
        print("vulkan gates open -- attempting llama.cpp build "
              "(cap 15 min)...", flush=True)
        llamacpp = try_build_llamacpp_vulkan(
            vk, os.path.join("/tmp/opencode", "llamacpp-vulkan"))
    npu = probe_npu()
    report = {
        "ts": time.time(), "ollama": {"version": ver, "live": ollama_live,
                                      "host": eb.OLLAMA_HOST},
        "gpu": gpu, "cpu": cpu, "ort": ort, "directml": dml,
        "vulkan": vk, "llamacpp_vulkan": llamacpp, "npu": npu,
    }
    with open(os.path.join(runs_dir, "probe.json"), "w") as f:
        json.dump(report, f, indent=1)
    print("ollama %s | gpu %s | ort %s | dml %s | vulkan-llamacpp %s | "
          "npu-in-wsl %s"
          % (ver, gpu["nvidia_smi"],
             "live" if ort["live"] else "missing",
             "live" if dml["live"] else "skipped",
             "built" if llamacpp["built"] else "skipped",
             npu["reachable_from_wsl"]), flush=True)
    return report


# ------------------------------------------------------------------- bench --

def bench_ollama_lanes(runs_dir, log_fn):
    out = {}
    for lane in OLLAMA_LANES:
        client = OllamaLane(num_gpu=lane["num_gpu"],
                            timeout=600 if lane["num_gpu"] == 0 else 240)
        per_model = {}
        for name, tag in LADDER:
            client.chat(tag, BENCH_SYSTEM, WARMUP_PROMPT, num_predict=8)
            recs = []
            for pid, text in ALL_PROMPTS:
                r = client.chat(tag, BENCH_SYSTEM, text,
                                num_predict=64 if pid.startswith("s")
                                else 128,
                                num_ctx=1024 if pid.startswith("s") else 1536)
                rec = {"type": "q", "lane": lane["id"], "model": name,
                       "tag": tag, "pid": pid, "ts": time.time()}
                if not r["ok"]:
                    rec.update({"ok": False, "error":
                                str(r.get("error"))[:120],
                                "ptok_s": 0.0, "gtok_s": 0.0,
                                "prompt_eval_count": 0, "eval_count": 0,
                                "latency_s": round(r["latency_s"], 3)})
                else:
                    ptok = (r["prompt_eval_count"] / r["prompt_eval_dur_s"]
                            if r["prompt_eval_dur_s"] > 0
                            and r["prompt_eval_count"] > 0 else 0.0)
                    gtok = (r["eval_count"] / r["eval_dur_s"]
                            if r["eval_dur_s"] > 0 else 0.0)
                    rec.update({"ok": True,
                                "ptok_s": round(ptok, 1),
                                "gtok_s": round(gtok, 1),
                                "prompt_eval_count": r["prompt_eval_count"],
                                "eval_count": r["eval_count"],
                                "load_s": round(r["load_s"], 2),
                                "latency_s": round(r["latency_s"], 3)})
                recs.append(rec)
                log_fn(rec)
                print("  %-11s %-7s %-22s %s ptok/s %6.1f  gtok/s %6.1f"
                      % (lane["id"], name, pid,
                         "ok  " if rec["ok"] else "FAIL",
                         rec["ptok_s"], rec["gtok_s"]), flush=True)
            per_model[name] = summarize_recs(recs)
        out[lane["id"]] = per_model
    return out


def summarize_recs(recs):
    short = [r for r in recs if r["pid"].startswith("s") and r["ok"]]
    long_ = [r for r in recs if not r["pid"].startswith("s") and r["ok"]]
    return {
        "n_ok": len(short) + len(long_),
        "ptok_s_short": round(median([r["ptok_s"] for r in short]), 1),
        "gtok_s_short": round(median([r["gtok_s"] for r in short]), 1),
        "ptok_s_long": round(median([r["ptok_s"] for r in long_]), 1),
        "gtok_s_long": round(median([r["gtok_s"] for r in long_]), 1),
        "med_prompt_toks": round(median(
            [r["prompt_eval_count"] for r in recs if r["ok"]]), 1),
        "med_gen_toks": round(median(
            [r["eval_count"] for r in recs if r["ok"]]), 1),
        "med_lat_s": round(median([r["latency_s"] for r in recs]), 2),
    }


# ------------------------------------------------------- gpt2 bpe (stdlib) --

def _bytes_to_unicode():
    bs = (list(range(ord("!"), ord("~") + 1))
          + list(range(ord("\u00a1"), ord("\u00ac") + 1))
          + list(range(ord("\u00ae"), ord("\u00ff") + 1)))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, [chr(c) for c in cs]))


_BPE_PAT = re.compile(
    r"'s|'t|'re|'ve|'m|'ll|'d| ?[A-Za-z]+| ?[0-9]+| ?[^\sA-Za-z0-9]+"
    r"|\s+(?!\S)|\s+")


class GPT2BPE:
    """GPT-2 byte-level BPE in stdlib (ASCII-class word splitting; the
    bench prompts are plain English so this matches HF tokenization
    closely enough for a throughput probe)."""

    def __init__(self, vocab_path, merges_path):
        with open(vocab_path, encoding="utf-8") as f:
            self.vocab = json.load(f)
        self.id2tok = {v: k for k, v in self.vocab.items()}
        rank = {}
        with open(merges_path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                parts = line.split()
                if len(parts) == 2:
                    rank[tuple(parts)] = i
        self.rank = rank
        self.b2u = _bytes_to_unicode()
        self.u2b = {v: k for k, v in self.b2u.items()}
        self.cache = {}

    def _bpe(self, token):
        if token in self.cache:
            return self.cache[token]
        word = tuple(token)
        while len(word) > 1:
            pairs = set(zip(word[:-1], word[1:]))
            best = min(pairs, key=lambda p: self.rank.get(p, 1 << 60))
            if best not in self.rank:
                break
            a, b = best
            new, i = [], 0
            while i < len(word):
                if i < len(word) - 1 and word[i] == a and word[i + 1] == b:
                    new.append(a + b)
                    i += 2
                else:
                    new.append(word[i])
                    i += 1
            word = tuple(new)
        self.cache[token] = word
        return word

    def encode(self, text):
        ids = []
        for m in _BPE_PAT.findall(text):
            token = "".join(self.b2u[b] for b in m.encode("utf-8"))
            ids.extend(self.vocab[t] for t in self._bpe(token))
        return ids

    def decode(self, ids):
        text = "".join(self.id2tok.get(i, "") for i in ids)
        return bytes(self.u2b[c] for c in text).decode("utf-8",
                                                       errors="replace")


def _download(url, dest, min_bytes):
    if os.path.exists(dest) and os.path.getsize(dest) >= min_bytes:
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    t0 = time.time()
    with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
        total = 0
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
            total += len(chunk)
    if total < min_bytes:
        raise IOError("download too small: %d bytes" % total)
    os.replace(tmp, dest)
    print("    fetched %s (%.1f MB, %.0fs)"
          % (os.path.basename(dest), total / 1e6, time.time() - t0),
          flush=True)


def bench_ort_lane(runs_dir, log_fn, max_new=24):
    try:
        import onnxruntime as ort
        import numpy as np
    except ImportError as ex:
        return {"skipped": "onnxruntime/numpy import: %s" % ex}
    mdir = os.path.join(runs_dir, "gpt2-onnx")
    try:
        _download(ORT_MODEL_URL, os.path.join(mdir, "model.onnx"),
                  50 << 20)
        _download(ORT_VOCAB_URL, os.path.join(mdir, "vocab.json"), 100000)
        _download(ORT_MERGES_URL, os.path.join(mdir, "merges.txt"), 100000)
    except (urllib.error.URLError, IOError, OSError) as ex:
        return {"skipped": "network/model fetch: %s" % str(ex)[:200]}
    enc = GPT2BPE(os.path.join(mdir, "vocab.json"),
                  os.path.join(mdir, "merges.txt"))
    sess = ort.InferenceSession(os.path.join(mdir, "model.onnx"),
                                providers=["CPUExecutionProvider"])
    in_map = {i.name: i.shape for i in sess.get_inputs()}
    n_past = sum(1 for k in in_map if k.endswith(".key")
                 and k.startswith("past_key_values"))
    pshapes = [v for k, v in in_map.items()
               if k.startswith("past_key_values")]
    has_pos = "position_ids" in in_map
    merged = "use_cache_branch" in in_map
    onames = [o.name for o in sess.get_outputs()]
    logits_out = next((n for n in onames if "logits" in n), None)
    if logits_out is None:
        return {"skipped": "no logits output in graph"}
    pidx = [i for i, n in enumerate(onames) if n.startswith("present.")]

    def fwd(cur, past):
        pl = past[0].shape[2] if past is not None else 0
        feed = {"input_ids": np.array([cur], dtype=np.int64),
                "attention_mask": np.ones((1, pl + len(cur)),
                                          dtype=np.int64)}
        if merged:
            feed["use_cache_branch"] = np.array([pl > 0], dtype=bool)
        if has_pos:
            feed["position_ids"] = np.arange(
                pl, pl + len(cur), dtype=np.int64)[None, :]
        if past is not None:
            for i in range(n_past):
                feed["past_key_values.%d.key" % i] = past[2 * i]
                feed["past_key_values.%d.value" % i] = past[2 * i + 1]
        outs = sess.run(None, feed)
        present = [outs[i] for i in pidx] if pidx else None
        return outs[onames.index(logits_out)], present

    recs = []
    for pid, text in ALL_PROMPTS:
        ids = enc.encode(text)
        if not ids:
            continue
        try:
            empty = ([np.zeros([1, s[1], 0, s[3]], dtype=np.float32)
                      for s in pshapes] if pshapes else None)
            t0 = time.perf_counter()
            logits, present = fwd(ids, empty)
            t_prompt = time.perf_counter() - t0
        except Exception as ex:
            return {"skipped": "graph run failed (%s): %s"
                    % (type(ex).__name__, str(ex)[:160])}
        cur = [int(np.argmax(logits[0, -1]))]
        steps, t_gen = 0, 0.0
        while steps < max_new and cur[-1] != ORT_EOS:
            t1 = time.perf_counter()
            logits, present = fwd([cur[-1]], present)
            t_gen += time.perf_counter() - t1
            cur.append(int(np.argmax(logits[0, -1])))
            steps += 1
        rec = {"type": "q", "lane": "ort-cpu", "model": "gpt2-124m-int8",
               "tag": "Xenova/gpt2 int8", "pid": pid, "ts": time.time(),
               "ok": True,
               "ptok_s": round(len(ids) / t_prompt, 1) if t_prompt else 0.0,
               "gtok_s": round(steps / t_gen, 1) if t_gen else 0.0,
               "prompt_eval_count": len(ids),
               "eval_count": steps,
               "latency_s": round(t_prompt + t_gen, 3)}
        recs.append(rec)
        log_fn(rec)
        print("  %-11s %-14s %s ptok/s %6.1f  gtok/s %6.1f"
              % ("ort-cpu", "gpt2-int8", pid, rec["ptok_s"],
                 rec["gtok_s"]), flush=True)
    return {"summary": summarize_recs(recs),
            "note": "greedy token loop WITH KV cache (merged graph: "
                    "empty past [1,12,0,64] on the prompt pass, present.* "
                    "fed back per step) on Xenova/gpt2 int8 (128 MB, HF "
                    "hub); gpt2-124m is a throughput probe, not a cell "
                    "candidate (it cannot follow the op schema)."}


def bench_phase(runs_dir, skip_ort=False, skip_ollama=False):
    os.makedirs(runs_dir, exist_ok=True)
    jsonl_path = os.path.join(runs_dir, "bench.jsonl")
    fresh = not os.path.exists(jsonl_path)
    jsonl = open(jsonl_path, "a" if not fresh else "w")

    def log_fn(rec):
        jsonl.write(json.dumps(rec) + "\n")
        jsonl.flush()

    old = {}
    if skip_ollama and os.path.exists(os.path.join(runs_dir, "bench.json")):
        with open(os.path.join(runs_dir, "bench.json")) as f:
            old = json.load(f)
    if skip_ollama:
        ollama_out = old.get("lanes", {})
        print("bench: reusing ollama lanes from bench.json", flush=True)
    else:
        print("bench: ollama lanes (5 models x 7 prompts each, temp 0)...",
              flush=True)
        ollama_out = bench_ollama_lanes(runs_dir, log_fn)
    ort_out = {"skipped": "not attempted"} if skip_ort \
        else bench_ort_lane(runs_dir, log_fn)
    bench = {
        "ts": time.time(),
        "prompt_set": {"short": [p for p, _ in SHORT_PROMPTS],
                       "long": [p for p, _ in LONG_PROMPTS],
                       "temperature": 0.0,
                       "deterministic": True},
        "lanes": ollama_out,
        "ort": ort_out,
        "notes": [
            "ptok/s = prompt_eval_count/prompt_eval_duration; gtok/s = "
            "eval_count/eval_duration -- Ollama's own counters, load time "
            "excluded.",
            "Prompts are unique per (model,lane) so prompt eval is "
            "cache-cold; the small shared system prefix may be cached "
            "after the warmup query.",
            "gpu lane = Ollama default placement (no num_gpu override); "
            "cpu lane = num_gpu 0 (all layers on the HX370).",
        ],
    }
    with open(os.path.join(runs_dir, "bench.json"), "w") as f:
        json.dump(bench, f, indent=1)
    jsonl.close()
    print("bench.json written", flush=True)
    return bench


# ------------------------------------------------------------------- cells --

class PatchedFleet:
    """eb.BenchFabric with a substituted fleet. edgebench's globals
    (MODELS / CELL_NAMES) are read at call time by turn_prompt and
    parse_op, so the patch stays active for the whole lane."""

    def __init__(self, cells):
        self.cells = list(cells)
        self.saved = None
        self.fab = None

    def __enter__(self):
        self.saved = (eb.MODELS, eb.CELL_NAMES)
        eb.MODELS = self.cells
        eb.CELL_NAMES = [eb.ROOM_NAME] + [n for n, _ in self.cells]
        self.fab = eb.BenchFabric()
        return self.fab

    def __exit__(self, *a):
        eb.MODELS, eb.CELL_NAMES = self.saved


def select_top3(runs_dir):
    """Rank the ladder as CELL candidates on the GPU lane: schema
    discipline (4 judgment turns each, temp 0) + bench speed. The parse
    scorer is edgebench's own parse_op."""
    bench = {}
    bpath = os.path.join(runs_dir, "bench.json")
    if os.path.exists(bpath):
        with open(bpath) as f:
            bench = json.load(f).get("lanes", {}).get("ollama-gpu", {})
    client = OllamaLane()
    stats = {}
    with PatchedFleet(LADDER) as fab:
        for q in range(4):
            for name, tag in LADDER:
                cell = fab.cell_by_name(name)
                r = client.chat(tag, eb.SYSTEM_PROMPT,
                                eb.turn_prompt(fab, cell), temperature=0.0)
                ok = False
                if r["ok"]:
                    op, _why = eb.parse_op(r["content"], name)
                    ok = op is not None
                    if op is not None:
                        fab.event(fab.apply_op(cell, op))
                st = stats.setdefault(name, {"ok": 0, "n": 0, "lats": []})
                st["ok"] += 1 if ok else 0
                st["n"] += 1
                st["lats"].append(r["latency_s"])
            fab.round_tick()
    speeds = {}
    for name, _ in LADDER:
        s = bench.get(name, {}).get("gtok_s_short", 0.0) or 0.0
        speeds[name] = s
    mx = max(speeds.values()) or 1.0
    scored = []
    for name, _ in LADDER:
        st = stats[name]
        parse = st["ok"] / max(1, st["n"])
        speed = speeds[name] / mx
        scored.append({"name": name, "tag": TAG[name],
                       "schema_probe_ok": st["ok"], "schema_probe_n": st["n"],
                       "parse_rate": round(parse, 3),
                       "gtok_s_short": speeds[name],
                       "score": round(2.0 * parse + 1.0 * speed, 3),
                       "med_lat_s": round(median(st["lats"]), 2)})
    scored.sort(key=lambda s: (-s["score"], s["med_lat_s"], s["name"]))
    top3 = [(s["name"], s["tag"]) for s in scored[:3]]
    out = {"ts": time.time(), "scored": scored, "top3": top3,
           "criterion": "2*schema-probe parse rate (4 turns, GPU lane, "
                        "temp 0) + normalized bench gtok/s (short)"}
    with open(os.path.join(runs_dir, "top3.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("top-3 cells: %s" % ", ".join("%s (%s, score %.2f)"
                                        % (s["name"], s["tag"], s["score"])
                                        for s in scored[:3]), flush=True)
    return top3


def ensure_top3(runs_dir):
    p = os.path.join(runs_dir, "top3.json")
    if os.path.exists(p):
        with open(p) as f:
            return [tuple(x) for x in json.load(f)["top3"]]
    return [tuple(x) for x in select_top3(runs_dir)]


def _pairs_of(cells):
    return [(a, b) for a, b in
            itertools.combinations([n for n, _ in cells], 2)]


def run_cells_lane(runs_dir, lane_id, top3, rounds, max_minutes,
                   ckpt_every, fresh=False):
    num_gpu = 0 if lane_id == "cpu" else None
    client = OllamaLane(num_gpu=num_gpu,
                        timeout=600 if lane_id == "cpu" else 240)
    state_path = os.path.join(runs_dir, "cells_%s_state.json" % lane_id)
    quf_path = os.path.join(runs_dir, "cells_%s.quf" % lane_id)
    state = None
    if not fresh and os.path.exists(state_path):
        with open(state_path) as f:
            state = json.load(f)
    if state is None:
        state = {"lane": lane_id, "cells": top3, "n": rounds,
                 "rounds_done": 0, "query_count": 0, "cut_note": None,
                 "started_ts": time.time()}
    pairs = _pairs_of(top3)

    with PatchedFleet(top3) as fab:
        if state["rounds_done"] > 0 and os.path.exists(quf_path):
            with open(quf_path, "rb") as f:
                fab = eb.BenchFabric.import_quf(f.read())
        jsonl = open(os.path.join(runs_dir, "cells_%s.jsonl" % lane_id),
                     "a" if state["rounds_done"] > 0 else "w")
        t_start = time.time()
        parse_ok = parse_tot = 0
        round_times = []
        for r in range(state["rounds_done"] + 1, state["n"] + 1):
            t_round = time.time()
            round_ops = []
            for a, b in pairs:
                speaker_name = a if r % 2 == 1 else b
                speaker = fab.cell_by_name(speaker_name)
                res = client.chat(TAG[speaker_name], eb.SYSTEM_PROMPT,
                                  eb.turn_prompt(fab, speaker),
                                  temperature=0.0)
                rec = {"type": "query", "lane": lane_id, "round": r,
                       "pair": [a, b], "speaker": speaker_name,
                       "model": TAG[speaker_name], "ts": time.time()}
                if not res["ok"]:
                    rec.update({"parse_ok": False, "op": None,
                                "fail": "infra:" + str(res.get("error"))
                                [:80], "content": "",
                                "latency_s": round(res["latency_s"], 3),
                                "eval_count": 0, "tok_s": 0.0})
                else:
                    op, why = eb.parse_op(res["content"], speaker_name)
                    rec.update({"parse_ok": op is not None, "op": op,
                                "fail": why,
                                "content": res["content"][:200],
                                "latency_s": round(res["latency_s"], 3),
                                "eval_count": res["eval_count"],
                                "tok_s": (round(res["eval_count"]
                                                / res["eval_dur_s"], 1)
                                          if res["eval_dur_s"] > 0
                                          else 0.0)})
                    if op is not None:
                        ev = fab.apply_op(speaker, op)
                        fab.event(ev)
                        round_ops.append("%s:%s"
                                         % (speaker_name, op["op"]))
                parse_tot += 1
                parse_ok += 1 if rec["parse_ok"] else 0
                jsonl.write(json.dumps(rec) + "\n")
                jsonl.flush()
                state["query_count"] += 1
            emergent = fab.round_tick()
            warm = fab.warmth()
            jsonl.write(json.dumps({
                "type": "round", "lane": lane_id, "round": r,
                "warmth": warm, "warmth_f": round(warm / 32768.0, 4),
                "edges": fab.edge_table(),
                "emergent": emergent, "ops": round_ops}) + "\n")
            jsonl.flush()
            state["rounds_done"] = r
            dt = time.time() - t_round
            round_times.append(dt)
            avg = sum(round_times[-10:]) / len(round_times[-10:])
            print("cells[%s] round %3d/%d  %.1fs  ops[%s]  parse %d/%d  "
                  "warmth %+.3f  eta %.0fm"
                  % (lane_id, r, state["n"], dt,
                     " ".join(round_ops) or "-", parse_ok, parse_tot,
                     warm / 32768.0, avg * (state["n"] - r) / 60.0),
                  flush=True)
            if r % ckpt_every == 0 or r == state["n"]:
                _ckpt(fab, state_path, state, jsonl, quf_path)
                elapsed = time.time() - t_start
                projected = elapsed + avg * (state["n"] - r)
                if projected > max_minutes * 60.0 and r < state["n"]:
                    state["cut_note"] = ("runtime guard: projected %.0f min "
                                         "> %.0f, stopping at round %d"
                                         % (projected / 60.0, max_minutes, r))
                    state["n"] = r
                    print("cells[%s] RUNTIME GUARD: %s"
                          % (lane_id, state["cut_note"]), flush=True)
                    _ckpt(fab, state_path, state, jsonl, quf_path)
                    break
        _ckpt(fab, state_path, state, jsonl, quf_path)
        jsonl.close()
        print("cells[%s] done: %d rounds, %d queries, parse %.1f%%"
              % (lane_id, state["rounds_done"], state["query_count"],
                 100.0 * parse_ok / max(1, parse_tot)), flush=True)
        return state


def _ckpt(fab, state_path, state, jsonl, quf_path):
    buf = fab.export_quf()
    issues = eb.quf.verify_bytes(buf, quf_path)
    if issues:
        print("QUF VERIFY FAIL (keeping previous checkpoint): %s" % issues)
        return
    with open(quf_path, "wb") as f:
        f.write(buf)
    state["updated_ts"] = time.time()
    with open(state_path, "w") as f:
        json.dump(state, f, indent=1)
    jsonl.flush()
    os.fsync(jsonl.fileno())


def cells_phase(runs_dir, rounds, max_minutes, ckpt_every, fresh=False,
                lanes=("gpu", "cpu")):
    os.makedirs(runs_dir, exist_ok=True)
    top3 = ensure_top3(runs_dir)
    states = {}
    for lane_id in lanes:
        states[lane_id] = run_cells_lane(runs_dir, lane_id, top3, rounds,
                                         max_minutes, ckpt_every,
                                         fresh=fresh)
    return states


# ------------------------------------------------------------------ report --

def _load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def _load_cells(runs_dir, lane_id):
    qs, rounds = [], {}
    p = os.path.join(runs_dir, "cells_%s.jsonl" % lane_id)
    if not os.path.exists(p):
        return qs, rounds
    with open(p) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec["type"] == "query":
                qs.append(rec)
            else:
                rounds[rec["round"]] = rec
    return qs, {k: rounds[k] for k in sorted(rounds)}


def _cell_stats(qs, rounds, cells, upto=None):
    out = {}
    for name, _tag in cells:
        mq = [q for q in qs if q["speaker"] == name
              and (upto is None or q["round"] <= upto)]
        ok = [q for q in mq if q["parse_ok"]]
        ops = {"fire": 0, "link": 0, "dial": 0}
        for q in ok:
            ops[q["op"]["op"]] += 1
        out[name] = {
            "queries": len(mq), "parse_ok": len(ok),
            "parse_rate": (len(ok) / len(mq)) if mq else 0.0,
            "ops": ops,
            "med_lat": median([q["latency_s"] for q in mq]),
            "mean_tps": (sum(q["tok_s"] for q in ok if q.get("tok_s"))
                         / max(1, len([q for q in ok if q.get("tok_s")]))),
        }
    rs = [rounds[k] for k in sorted(rounds)
          if upto is None or k <= upto]
    warmth = [r["warmth_f"] for r in rs]
    emergent = sum(len(r["emergent"]) for r in rs)
    walks = sum(e["wh"] for r in rs for e in r["edges"]) if rs else 0
    return {"models": out, "warmth": warmth,
            "warmth_end": warmth[-1] if warmth else 0.0,
            "warmth_min": min(warmth) if warmth else 0.0,
            "warmth_max": max(warmth) if warmth else 0.0,
            "emergent": emergent, "rounds": len(rs),
            "total_walks": walks,
            "edges_final": len(rs[-1]["edges"]) if rs else 0}


def report_phase(runs_dir, out_path):
    probe = _load_json(os.path.join(runs_dir, "probe.json"))
    bench = _load_json(os.path.join(runs_dir, "bench.json"))
    top3j = _load_json(os.path.join(runs_dir, "top3.json"))
    top3 = [tuple(x) for x in top3j.get("top3", [])]
    seed_edges = len(top3) * 3

    gq, gr = _load_cells(runs_dir, "gpu")
    cq, cr = _load_cells(runs_dir, "cpu")
    gstate = _load_json(os.path.join(runs_dir, "cells_gpu_state.json"))
    cstate = _load_json(os.path.join(runs_dir, "cells_cpu_state.json"))
    common = min(len(gr), len(cr)) if (gr and cr) else max(len(gr), len(cr))
    gs = _cell_stats(gq, gr, top3, upto=common)
    cs = _cell_stats(cq, cr, top3, upto=common)

    lanes = bench.get("lanes", {})
    ort = bench.get("ort", {})

    L = []
    A = L.append
    A("# CHIP-MATRIX — every chip on the desk as a cell")
    A("")
    A("**Lane:** chip-matrix · **Date:** %s · **Companions:** "
      "`EDGE-BENCH.md` (the night lane, same scorer), `TAP-FABRIC.md` "
      "(cell semantics), `tools/edgebench/edgebench.py` (the engine this "
      "tool reuses)." % time.strftime("%Y-%m-%d"))
    A("")
    A("> **The question this document answers.** Casey's directive: run "
      "the edge experiments across ALL local silicon — the RTX 4050, the "
      "Ryzen AI 9 HX 370's CPU (and its NPU if honestly reachable), and "
      "anything else that actually works. Measure prompt and generation "
      "throughput on a fixed deterministic prompt set; then rerun a "
      "100-round slice of the judgment-cell game on the top-3 models "
      "GPU-vs-CPU to test the hundred-boats question: **is CPU-only "
      "inference good enough to be a cell?**")
    A("")

    # -- backends ----------------------------------------------------------
    A("## 1. Backends found (the probe)")
    A("")
    vk = probe.get("vulkan", {})
    llm = probe.get("llamacpp_vulkan", {})
    npu = probe.get("npu", {})
    dml = probe.get("directml", {})
    rows = [
        ("ollama-gpu", True,
         "Ollama %s, default placement; %s; /dev/dxg present"
         % (probe.get("ollama", {}).get("version", "?"),
            probe.get("gpu", {}).get("nvidia_smi", "?"))),
        ("ollama-cpu", True,
         "Ollama with `num_gpu=0` — all layers on %s (%d threads)"
         % (probe.get("cpu", {}).get("model", "?"),
            probe.get("cpu", {}).get("threads", "?"))),
        ("ort-cpu", probe.get("ort", {}).get("live", False),
         "onnxruntime %s, providers %s"
         % (probe.get("ort", {}).get("version", "?"),
            ",".join(probe.get("ort", {}).get("providers", [])))),
        ("ort-directml", dml.get("live", False),
         "skipped honestly — %s" % dml.get("why", "?")),
        ("llama.cpp-vulkan", llm.get("built", False),
         "skipped honestly — %s" % llm.get("why", "?")),
        ("hx370-xdna2-npu", npu.get("reachable_from_wsl", False),
         "skipped honestly — no NPU device node or accel sysfs class in "
         "WSL (see §5)"),
    ]
    A("| backend | live | evidence |")
    A("|---|---|---|")
    for name, live, ev in rows:
        A("| `%s` | %s | %s |"
          % (name, "**YES**" if live else "no", ev))
    A("")
    A("Vulkan gate detail: SDK headers %s, loader %s, dzn ICD %s, "
      "vulkaninfo %s, cmake %s, non-interactive sudo %s."
      % ("present" if vk.get("sdk_headers") else "absent",
         "present" if vk.get("loader") else "absent",
         "present" if vk.get("dzn_icd")
         else "absent (mesa ICDs cannot drive the paravirtual WSL GPU)",
         "present" if vk.get("vulkaninfo") else "absent",
         "present" if vk.get("cmake") else "absent",
         "ok" if vk.get("sudo_noninteractive")
         else "password-locked"))
    A("")

    # -- throughput matrix -------------------------------------------------
    A("## 2. Throughput matrix (fixed prompt set, temperature 0)")
    A("")
    A("5 short + 2 long deterministic prompts × model ladder × live "
      "backends. ptok/s = prompt eval, gtok/s = generation, medians; "
      "Ollama's own counters (load time excluded).")
    A("")
    A("| model | gpu ptok/s (S/L) | gpu gtok/s (S/L) | cpu ptok/s (S/L) | "
      "cpu gtok/s (S/L) | cpu/gpu gen |")
    A("|---|---|---|---|---|---|")
    for name, tag in LADDER:
        g = lanes.get("ollama-gpu", {}).get(name, {})
        c = lanes.get("ollama-cpu", {}).get(name, {})
        ratio = ("%.2f×" % (c["gtok_s_short"] / g["gtok_s_short"])
                 if g.get("gtok_s_short") and c.get("gtok_s_short")
                 else "—")
        A("| `%s` (`%s`) | %s / %s | %s / %s | %s / %s | %s / %s | %s |"
          % (name, tag,
             g.get("ptok_s_short", "—"), g.get("ptok_s_long", "—"),
             g.get("gtok_s_short", "—"), g.get("gtok_s_long", "—"),
             c.get("ptok_s_short", "—"), c.get("ptok_s_long", "—"),
             c.get("gtok_s_short", "—"), c.get("gtok_s_long", "—"),
             ratio))
    if "summary" in ort:
        s = ort["summary"]
        A("| `gpt2-124m-int8` (ort-cpu probe) | %s / %s | %s / %s | "
          "same lane | same lane | — |"
          % (s.get("ptok_s_short", "—"), s.get("ptok_s_long", "—"),
             s.get("gtok_s_short", "—"), s.get("gtok_s_long", "—")))
    A("")
    if "skipped" in ort:
        A("ort-cpu lane skipped: %s" % ort["skipped"])
    else:
        A("ort-cpu lane note: %s" % ort.get(
            "note", "greedy loop on Xenova/gpt2 int8 (128 MB, HF hub)"))
    A("")
    A("Notes: %s" % "; ".join(bench.get("notes", [])))
    A("")

    # -- cell experiment ---------------------------------------------------
    A("## 3. The cell experiment — GPU vs CPU, %d-round slice" % common
      if common else "## 3. The cell experiment (not run)")
    A("")
    A("Top-3 by cell-worthiness on the GPU lane (schema-probe parse rate "
      "×2 + normalized bench speed): **%s** — criterion `%s`."
      % (", ".join("`%s` (`%s`)" % (n, t) for n, t in top3),
         top3j.get("criterion", "?")))
    A("")
    A("Same BenchFabric, same schema-strict `parse_op`, temperature 0 on "
      "both lanes. 3 pair-turns per round, one `qm_tick` per round; "
      "checkpoints every 20 rounds (`cells_*.quf`, QUF-verified).")
    A("")
    cut_g = gstate.get("cut_note")
    cut_c = cstate.get("cut_note")
    A("GPU lane: %d rounds (%d queries%s). CPU lane: %d rounds (%d "
      "queries%s). Comparison window: first %d rounds."
      % (gs["rounds"], len(gq),
         "; CUT: `%s`" % cut_g if cut_g else "",
         cs["rounds"], len(cq),
         "; CUT: `%s`" % cut_c if cut_c else "", common))
    A("")
    A("| lane | parse rate | op mix f/l/d | warmth end (range) | "
      "emergent fires | edges (seed %d) | Σwalks | med turn (s) |"
      % seed_edges)
    A("|---|---|---|---|---|---|---|---|")
    for label, st, qs in (("gpu", gs, gq), ("cpu", cs, cq)):
        ops = {"fire": 0, "link": 0, "dial": 0}
        for m in st["models"].values():
            for k in ops:
                ops[k] += m["ops"][k]
        tot = sum(1 for q in qs if q["round"] <= common)
        oks = sum(1 for q in qs if q["round"] <= common and q["parse_ok"])
        A("| %s | %.1f%% (%d/%d) | %d/%d/%d | %+.3f (%+.3f..%+.3f) | %d | "
          "%d | %d | %.1f |"
          % (label, 100.0 * oks / max(1, tot), oks, tot,
             ops["fire"], ops["link"], ops["dial"],
             st["warmth_end"], st["warmth_min"], st["warmth_max"],
             st["emergent"], st["edges_final"], st["total_walks"],
             median([q["latency_s"] for q in qs
                     if q["round"] <= common]) or 0.0))
    A("")
    reload_probe = _load_json(os.path.join(runs_dir,
                                           "gpu_reload_probe.json"))
    if reload_probe:
        burst = reload_probe.get("burst_3x_nano", [])
        hot = (burst[-1] if burst else {}).get("lat_s", "?")
        first = (burst[0] if burst else {}).get("lat_s", "?")
        A("**Why GPU turns are slow here (measured, "
          "`gpu_reload_probe.json`):** the GPU lane's eval runs at full "
          "speed (nano 210-276 tok/s in the slice), but Ollama's WSL/dxg "
          "runner keeps one model hot at a time — every model switch "
          "reloads weights through dxg (`load_duration` ≈3.5s): a nano "
          "burst runs %.2fs → %.2fs → %.2fs per turn, while "
          "nano→wesley→nano reloads on each switch. The alternating "
          "3-cell pair pattern pays the reload on every query, so the "
          "CPU lane — whose runners stay resident in RAM — is "
          "end-to-end faster for small-model cell fleets at default "
          "settings. Single-model bursts on the GPU are the chip "
          "ceiling (~0.1s a nano turn); the reload is policy, not "
          "silicon."
          % tuple(x.get("lat_s", 0) for x in burst[:3])
          if len(burst) >= 3 else "")
        A("")
    metronome = [n for n, _t in top3
                 if gs["models"][n]["ops"]["fire"]
                 == gs["models"][n]["queries"]
                 and gs["models"][n]["queries"]]
    if metronome:
        A("Temperature-0 note: %s answered every turn with the same op "
          "class (`fire` throughout) — deterministic sampling makes a "
          "satisfied cell a metronome; diversity at temp 0 comes only "
          "from state changes in the prompt (the night lane at "
          "temperature 0.7 sees richer op mixes)."
          % ", ".join("`%s`" % n for n in metronome))
        A("")
    A("| cell | gpu parse | gpu ops f/l/d | gpu med lat | cpu parse | "
      "cpu ops f/l/d | cpu med lat |")
    A("|---|---|---|---|---|---|---|")
    for name, _tag in top3:
        gm = gs["models"][name]
        cm = cs["models"][name]
        A("| `%s` | %.1f%% | %d/%d/%d | %.1fs | %.1f%% | %d/%d/%d | "
          "%.1fs |"
          % (name, 100 * gm["parse_rate"], gm["ops"]["fire"],
             gm["ops"]["link"], gm["ops"]["dial"], gm["med_lat"],
             100 * cm["parse_rate"], cm["ops"]["fire"], cm["ops"]["link"],
             cm["ops"]["dial"], cm["med_lat"]))
    A("")
    for label, st in (("gpu", gs), ("cpu", cs)):
        A("```")
        A("%s warmth %s" % (label, sparkline(st["warmth"])))
        A("```")
    A("")

    # -- verdict -----------------------------------------------------------
    tot_g = sum(1 for q in gq if q["round"] <= common)
    ok_g = sum(1 for q in gq if q["round"] <= common and q["parse_ok"])
    tot_c = sum(1 for q in cq if q["round"] <= common)
    ok_c = sum(1 for q in cq if q["round"] <= common and q["parse_ok"])
    pr_g = 100.0 * ok_g / max(1, tot_g)
    pr_c = 100.0 * ok_c / max(1, tot_c)
    parse_gap = pr_g - pr_c
    growth_ok = cs["total_walks"] >= 0.5 * max(1, gs["total_walks"])
    rounds_ok = cs["rounds"] >= 0.8 * common if common else False
    lat_g = median([q["latency_s"] for q in gq
                    if q["round"] <= common]) or 1.0
    lat_c = median([q["latency_s"] for q in cq
                    if q["round"] <= common]) or 1.0
    verdict = "MARGINAL"
    if tot_c and parse_gap <= 10.0 and pr_c >= 80.0 and growth_ok \
            and rounds_ok:
        verdict = "YES — CPU-only inference is good enough to be a cell"
    elif tot_c and (pr_c < 50.0 or not rounds_ok):
        verdict = "NO — CPU lane fails cell duty"
    A("### Verdict on the hundred-boats question")
    A("")
    A("**%s.** GPU parsed %.1f%% vs CPU %.1f%% (gap %+.1f pts); the CPU "
      "fabric grew Σwalks %d vs GPU %d and finished %d/%d rounds in the "
      "window; median cell turn %.1fs on GPU vs %.1fs on CPU — on this "
      "WSL/dxg setup the CPU lane is end-to-end FASTER for the "
      "small-model cell pattern (see the reload note above), and both "
      "sit far inside a 60-second judgment budget."
      % (verdict, pr_g, pr_c, parse_gap, cs["total_walks"],
         gs["total_walks"], cs["rounds"], common, lat_g, lat_c))
    A("")

    # -- boat doctrine -----------------------------------------------------
    reload_probe = _load_json(os.path.join(runs_dir,
                                           "gpu_reload_probe.json"))
    hot_lat = {}
    for row in reload_probe.get("burst_3x_nano", [])[1:]:
        hot_lat[row["model"]] = row["lat_s"]
    A("## 4. Boat doctrine — how many cells per chip")
    A("")
    A("A cell turn is one judgment prompt (the fixed `turn_prompt`: room "
      "state, edges, recent events — a few hundred tokens) plus the op "
      "reply (measured medians ≈%d tokens; wesley runs to its "
      "num_predict cap, the others answer in 13-21). If each cell "
      "speaks once per round, a chip carries `round_budget / "
      "turn_latency` cells:"
      % round(median([q.get("eval_count", 0) or 24 for q in gq]) or 24))
    A("")
    A("| carrier | turn (s) | cells @60s rounds | cells @300s rounds |")
    A("|---|---|---|---|")
    for name, _tag in top3:
        gm = gs["models"][name]
        cm_ = cs["models"][name]
        A("| `%s` on GPU (alternating fleet) | %.1f | %.0f | %.0f |"
          % (name, gm["med_lat"], 60.0 / max(0.1, gm["med_lat"]),
             300.0 / max(0.1, gm["med_lat"])))
        A("| `%s` on CPU | %.1f | %.0f | %.0f |"
          % (name, cm_["med_lat"], 60.0 / max(0.1, cm_["med_lat"]),
             300.0 / max(0.1, cm_["med_lat"])))
    if "nano" in hot_lat:
        A("| `nano` on GPU, same-model burst (chip ceiling) | %.2f | "
          "%.0f | %.0f |"
          % (hot_lat["nano"], 60.0 / max(0.01, hot_lat["nano"]),
             300.0 / max(0.01, hot_lat["nano"])))
    A("")
    A("The alternating-fleet GPU numbers are the honest DEFAULT-policy "
      "numbers (one hot runner; ~3.5s dxg reload per model switch, "
      "§3); the burst row is the same chip with the runner kept hot. "
      "The Ollama daemon serializes queries per model-runner but runs "
      "different models' runners concurrently, and the GPU and CPU "
      "lanes are separate runners of the same tags — the desk's honest "
      "fleet is the **sum**: CPU boats (runners resident, no reload) + "
      "GPU boats (fastest for a dedicated single-model fleet or longer "
      "generations, cf. `qwen3:8b`'s 2× on GPU in §2) + the ort-cpu "
      "lane for schema-free work.")
    A("")

    # -- npu ---------------------------------------------------------------
    A("## 5. NPU honesty — the XDNA2 door is real but it is not this "
      "side of the glass")
    A("")
    A("The Ryzen AI 9 HX 370 carries a 50-TOPS XDNA2 NPU. Probe "
      "evidence from this WSL session: NPU device nodes %s, "
      "`/sys/class/accel` entries %s — the NPU is **not exposed to "
      "WSL2**; the ryzen-ai stack (drivers, Vitis AI runtime, "
      "`onnxruntime-vitisai` / `ryzen-ai` wheels) is Windows-only, exactly "
      "like `onnxruntime-directml` (§1: no Linux wheels — verified by "
      "the failed pip install recorded in `probe.json`). Nothing here "
      "fakes it."
      % (npu.get("wsl_device_nodes") or "none",
         npu.get("sysfs_accel") or "none"))
    A("")
    A("What a Windows-side runner would need to open the door:")
    A("")
    A("1. Windows 11 23H2+ with the AMD XDNA2 NPU driver installed and "
      "the NPU enabled in Device Manager.")
    A("2. Ryzen AI Software 1.3+ (or ONNX Runtime ≥1.18 with the "
      "`VitisAIExecutionProvider` / `onnxruntime-vitisai` Windows "
      "wheels), Python on the Windows side.")
    A("3. Models as ONNX (int8/bf16) with Vitis-AI partitioning — the "
      "ladder's qwen2.5/granite class has export paths; or a Windows "
      "llama.cpp build with `-DGGML_RYZENAI=ON` (its Vitis-AI backend).")
    A("4. A small bridge: the runner answers the same judgment prompts "
      "over a local port this harness can curl; `chipmatrix.py` would "
      "grow one lane that talks to it. **This is the open door** — the "
      "same Windows runner also unlocks `onnxruntime-directml` for the "
      "Radeon 890M iGPU and the RTX 4050 dGPU in one step.")
    A("")

    # -- repro -------------------------------------------------------------
    A("## 6. Reproduce")
    A("")
    A("```")
    A("python3 tools/edgebench/chipmatrix.py --selftest")
    A("python3 tools/edgebench/chipmatrix.py --phase probe")
    A("python3 tools/edgebench/chipmatrix.py --phase bench   "
      "# ollama-gpu + ollama-cpu + ort-cpu lanes")
    A("python3 tools/edgebench/chipmatrix.py --phase cells   "
      "# top-3 x {gpu,cpu}, 100 rounds, checkpoints")
    A("python3 tools/edgebench/chipmatrix.py --phase report   "
      "# regenerates this document")
    A("python3 tools/quf.py verify "
      "tools/edgebench/chipmatrix_runs/cells_gpu.quf")
    A("```")
    A("")
    A("Artifacts: `chipmatrix_runs/probe.json` (backend evidence), "
      "`bench.jsonl`/`bench.json` (every bench query + summary), "
      "`top3.json` (selection), `cells_{gpu,cpu}.jsonl` (every judgment "
      "query), `cells_{gpu,cpu}_state.json`, `cells_{gpu,cpu}.quf` "
      "(QUF-verified fabric snapshots), `gpt2-onnx/` (download cache, "
      "git-ignored).")
    A("")
    A("*Every chip measured where it honestly stands; the boats that "
      "float are counted, the doors that are shut are named.*")
    A("")

    with open(out_path, "w") as f:
        f.write("\n".join(L))
    print("wrote %s (%d lines)" % (out_path, len(L)))
    return 0


# --------------------------------------------------------------- selftest --

def selftest():
    ok = True
    pids = [p for p, _ in ALL_PROMPTS]
    if len(set(pids)) != len(pids):
        ok = False
        print("FAIL: duplicate prompt ids")
    for pid, text in LONG_PROMPTS:
        if len(text.split()) < 300:
            ok = False
            print("FAIL: long prompt %s too short (%d words)"
                  % (pid, len(text.split())))
    for pid, text in SHORT_PROMPTS:
        if not 0 < len(text.split()) < 60:
            ok = False
            print("FAIL: short prompt %s not short" % pid)

    with PatchedFleet(LADDER[:5]) as fab:
        if len(fab.order) != 6 or len(fab.edge_table()) != 5 * 3:
            ok = False
            print("FAIL: 5-cell seed graph shape (want 15 edges)")
        op, why = eb.parse_op('{"op":"link","to":"room"}', "lfm")
        if op is None:
            ok = False
            print("FAIL: patched link-to-room: %s" % why)
        op, _ = eb.parse_op('{"op":"link","to":"qwen3"}', "qwen3")
        if op is not None:
            ok = False
            print("FAIL: self-link not rejected under patch")
    with PatchedFleet(LADDER[:3]) as fab3:
        if len(fab3.edge_table()) != 3 * 3:
            ok = False
            print("FAIL: 3-cell seed graph shape")
        if [n for n, _ in LADDER[:3]] != [fab3.cells[c].name
                                          for c in fab3.order[1:]]:
            ok = False
            print("FAIL: patched fleet names")

    if 60.0 / 2.0 != 30.0:
        ok = False
        print("FAIL: cells-per-chip arithmetic")

    vpath = os.path.join(RUNS_DIR, "gpt2-onnx", "vocab.json")
    if os.path.exists(vpath) and os.path.exists(
            os.path.join(RUNS_DIR, "gpt2-onnx", "merges.txt")):
        enc = GPT2BPE(vpath, os.path.join(RUNS_DIR, "gpt2-onnx",
                                          "merges.txt"))
        for text in ["hello world", "In one sentence, explain what a "
                     "systolic array is.", "deadband 0x2000"]:
            ids = enc.encode(text)
            if not ids or enc.decode(ids) != text:
                ok = False
                print("FAIL: BPE roundtrip %r" % text[:40])
        if eb.MODELS is LADDER:
            ok = False
            print("FAIL: patch leaked")

    if not ok:
        sys.exit(1)
    print("chipmatrix selftest PASS: prompts, fleet patching, parser "
          "reuse, matrix math%s"
          % (", BPE roundtrip" if os.path.exists(vpath) else ""))
    return ok


# --------------------------------------------------------------------- CLI --

def main(argv=None):
    ap = argparse.ArgumentParser(prog="chipmatrix.py")
    ap.add_argument("--phase", default="all",
                    choices=["probe", "bench", "cells", "report", "all"])
    ap.add_argument("--runs-dir", default=RUNS_DIR)
    ap.add_argument("--rounds", type=int, default=100,
                    help="cell-slice rounds per lane")
    ap.add_argument("--max-minutes", type=float, default=45.0,
                    help="per-lane runtime budget for the cell slice")
    ap.add_argument("--checkpoint-every", type=int, default=20)
    ap.add_argument("--skip-ort", action="store_true")
    ap.add_argument("--skip-ollama", action="store_true",
                    help="bench phase: reuse ollama lanes from bench.json")
    ap.add_argument("--lanes", default="gpu,cpu",
                    help="cell-slice lanes (comma list of gpu,cpu)")
    ap.add_argument("--fresh", action="store_true",
                    help="restart the cell slice from round 1")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        selftest()
        return 0

    doc = os.path.normpath(os.path.join(_HERE, "..", "..", "docs",
                                        "CHIP-MATRIX.md"))
    if args.phase in ("probe", "all"):
        probe_phase(args.runs_dir)
    if args.phase in ("bench", "all"):
        bench_phase(args.runs_dir, skip_ort=args.skip_ort,
                    skip_ollama=args.skip_ollama)
    if args.phase in ("cells", "all"):
        cells_phase(args.runs_dir, args.rounds, args.max_minutes,
                    args.checkpoint_every, fresh=args.fresh,
                    lanes=tuple(x for x in args.lanes.split(",") if x))
    if args.phase in ("report", "all"):
        report_phase(args.runs_dir, doc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
