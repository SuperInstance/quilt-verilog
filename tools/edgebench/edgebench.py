#!/usr/bin/env python3
"""edgebench.py -- the hundred-boats harness: local chips as cells (EDGE-BENCH lane).

Runs a TINY cell-graph game (docs/TAP-FABRIC.md cell semantics, mirrored from
q_cell_core / q_hebb_edge / q_dialfile arithmetic and sim/tools/tapfabric.py)
where every CELL is a local Ollama model. Each turn a model receives a
schema-strict judgment prompt -- its cell op as ONE JSON object:

    {"op":"fire","heat":N}                      N in -8..8
    {"op":"link","to":"NAME"}                   NAME of another cell
    {"op":"dial","addr":A,"delta":M}            A in {5,7,10}, M in -4..4

The harness applies the op through RTL-true fabric semantics: hearer-owned
edges, link-before-effect, train-then-integrate, integrate-leak-fire ticks.
Hebbian weights live in a real QUF (tools/quf.py structures): a cofire adds
one walk to `wh`, silence decays walks (hyperbola tick), and the effective
weight is base + ln(1+walks) -- the edgebench readout, ln-compressed so late
walks cannot saturate the u16. Parse failures are the model's fault and are
logged per query. Stdlib only. Python >= 3.8.

Usage:
  python3 tools/edgebench/edgebench.py --selftest
"""

import argparse
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.normpath(os.path.join(_HERE, ".."))
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import quf  # noqa: E402  (tools/quf.py -- QUF reference implementation)

# ------------------------------------------------------------------ consts --

PW = 16
NDIALS = quf.NDIALS
K_BUCKETS = 8
EDGES_N = 8

D_ETA_F, D_ETA_S, D_KF, D_KS, D_KA, D_THRESH, D_REFR, D_COSMIN = range(8)
D_P0E, D_MODE, D_HL = 8, 9, 10

DIAL_DEFAULTS = [0x0800, 0x0080, 6, 12, 5, 0x6000, 4, 0x2CCD,
                 20, 0, 48, 0, 0, 0, 0, 0]

ROOM_ID = 0
ROOM_NAME = "room"
KIND_GREET, KIND_JOKE, KIND_STORY, KIND_QUESTION, KIND_GRIPE, \
    KIND_MOVE, KIND_IDLE = range(7)
KINDS = ["GREET", "JOKE", "STORY", "QUESTION", "GRIPE", "MOVE", "IDLE"]

# The fleet (Casey directive): short cell name -> Ollama model tag.
MODELS = [
    ("lfm", "Liquid-LFM2.5-2.6B"),
    ("qwen3", "qwen3:8b"),
    ("wesley", "granite3.1-dense:2b"),
    ("nano", "qwen2.5:0.5b"),
]
CELL_NAMES = [ROOM_NAME] + [n for n, _ in MODELS]
MODEL_TAG = dict(MODELS)
THINKING_MODELS = {"qwen3:8b"}
# LFM2.5 reasons verbosely before answering and ignores think:false
# (content stays empty while message.thinking runs 800+ tokens). The
# assistant-prefill trick -- seeding the reply with "{" -- skips its
# thinking entirely; the harness re-prepends the brace before parsing.
PREFILL_MODELS = {"Liquid-LFM2.5-2.6B"}
PREFILL = "{"
NUM_PREDICT = {"Liquid-LFM2.5-2.6B": 96}

PATRON_BASE_W = 8192                # Q1.15 0.25 affinity
ROOM_BASE_W = 4096
HEAT_UNIT = 4096                    # one op heat unit in Q1.15 (1/8 full)
LN_SCALE = 4096                     # Q1.15 per e-fold of walks (the ln readout)
BENCH_P0E = 7                       # hyperbola P0 = 128 ticks: silence decays
TPW = 6
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")

DIAL_ALIASES = {5: "earnestness", 7: "openness", 10: "halflife"}


def sclip16(v):
    return max(-32768, min(32767, v))


def sat_u16(v):
    return max(0, min(0xFFFF, v))


def to_signed16(u):
    return u - 0x10000 if u >= 0x8000 else u


def heat_bucket(heat):
    return (heat & 0xFFFF) >> 13


def fnv1a(s):
    h = 0x811C9DC5
    for ch in s.encode("utf-8"):
        h = ((h ^ ch) * 0x01000193) & 0xFFFFFFFF
    return h


def _msb16(v):
    m = 0
    for j in range(PW):
        if (v >> j) & 1:
            m = j
    return m


# ------------------------------------------------------------------- edge --

class LnEdge:
    """One q_hebb_edge run in hyperbola mode with the edgebench ln readout.

    Cofire (train): wh += 1 (a walk, u16, sticky ovf). Silence (tick):
    age+1 >= max(1, P0 >> 2*msb(wh)) -> wh -= 1 -- the RTL hyperbola decay.
    Readout: w = sat_u16(base + LN_SCALE * ln(1+wh)) -- the directive's
    "base + ln(1+walks)", scaled into Q1.15 and u16-saturating. Integer
    state only; the log never drifts.
    """

    __slots__ = ("src", "dst", "slot", "mode", "base", "buckets",
                 "hl_cnt", "wh", "age", "ovf")

    def __init__(self, src, dst, slot, base):
        self.src = src
        self.dst = dst
        self.slot = slot
        self.mode = 1                     # hyperbola engine: wh = walks
        self.base = base
        self.buckets = [0] * K_BUCKETS
        self.hl_cnt = 0
        self.wh = 0
        self.age = 0
        self.ovf = False

    def train(self):
        if self.wh >= (1 << PW) - 1:
            self.ovf = True
        else:
            self.wh += 1

    def tick(self, p0e):
        ival = max(1, (1 << p0e) >> (2 * _msb16(self.wh)))
        if self.wh and (self.age + 1 >= ival):
            self.wh -= 1
            self.age = 0
        else:
            self.age += 1

    def readout(self):
        eng = int(LN_SCALE * math.log1p(self.wh))
        return sat_u16(self.base + eng)

    def record(self):
        return {"src": self.src, "dst": self.dst, "mode": self.mode,
                "slot": self.slot, "base": self.base, "wh": self.wh,
                "age": self.age, "buckets": list(self.buckets)}


# --------------------------------------------------------------- judgment --

class Judgment:
    """FOUNDATION D2 as taste: J = (A, r) over integer (kind, bucket)
    features, d = 3*[kind mismatch] + |bucket diff|, verdict set output --
    never guesses when |V| > 1."""

    def __init__(self, keys, openness):
        self.keys = keys
        self.openness = openness

    @staticmethod
    def distance(a, b):
        return 3 * (a[0] != b[0]) + abs(a[1] - b[1])

    def __call__(self, x):
        v = [(cls, note) for (k, b, cls, note) in self.keys
             if self.distance(x, (k, b)) <= self.openness]
        if not v:
            return "REJECT", "off-taste"
        if len(v) > 1:
            return "AMBIGUOUS", "two keys within r"
        return "ACCEPT", v[0][1]


def model_taste(name):
    """Deterministic taste from the cell's name (bind-time dials)."""
    h = fnv1a(name)
    speakable = [KIND_GREET, KIND_JOKE, KIND_STORY, KIND_QUESTION, KIND_GRIPE]
    liked = speakable[h % 5]
    center = 3 + (h >> 8) % 2
    openness = 2 + (h >> 16) % 2
    keys = [(liked, center, "land", "%s@%d" % (KINDS[liked], center)),
            (KIND_QUESTION, 3, "sip", "curious-question@3")]
    return Judgment(keys, openness)


# ------------------------------------------------------------------- cell --

class BenchCell:
    """A q_cell_core + q_dialfile + q_hebb_edge array. kind 'model' cells
    are driven by their Ollama model's op; the 'room' cell is the
    dial-aggregating cell (warmth rides its ETA_F dial)."""

    def __init__(self, cid, name, kind):
        self.cid = cid
        self.name = name
        self.kind = kind
        self.dials = list(DIAL_DEFAULTS)
        self.dials[D_P0E] = BENCH_P0E
        self.edges = []
        self.act = 0
        self.refr = 0
        self.judgment = None
        self.accounts = {"turns": 0, "heard": 0}
        self.stats = {"fires": 0, "emergent": 0, "links": 0, "dials": 0,
                      "accept": 0, "reject": 0, "ambig": 0}
        if kind == "model":
            self.judgment = model_taste(name)
            self.dials[D_THRESH] = 0x4000
            self.dials[D_COSMIN] = self.judgment.openness
        else:
            self.dials[D_THRESH] = 0x5000
            self.dials[D_KA] = 4
            self.dials[D_REFR] = 3

    def find_edge(self, dst):
        for e in self.edges:
            if e.dst == dst:
                return e
        return None

    def link(self, dst, base):
        e = self.find_edge(dst)
        if e is not None:
            e.base = min(e.base + 2048, 0xC000)
            return e, False
        if len(self.edges) >= EDGES_N:
            coldest = min(self.edges, key=lambda x: x.readout())
            self.edges.remove(coldest)
        e = LnEdge(self.cid, dst, len(self.edges), base)
        self.edges.append(e)
        return e, True

    def effect(self, src_cid, dat, kind):
        """A delivered flit: link-before-effect, train-then-integrate with
        the post-update weight readback; unknown src drops silently."""
        e = self.find_edge(src_cid)
        if e is None:
            return None
        e.train()
        w = e.readout()
        bucket = heat_bucket(dat)
        applied = dat
        if self.kind == "model":
            verdict, _ = self.judgment((kind, bucket))
            if verdict == "REJECT":
                applied = -(abs(dat) >> 1)
            elif verdict == "AMBIGUOUS":
                applied = 0
        else:
            verdict = "ACCEPT"
        before = self.act
        self.act = sclip16(self.act + ((w * applied) >> 15))
        self.accounts["heard"] += 1
        if self.kind == "model":
            self.stats[{"ACCEPT": "accept", "REJECT": "reject",
                        "AMBIGUOUS": "ambig"}[verdict]] += 1
        return {"w": w, "verdict": verdict, "applied": applied,
                "before": before, "after": self.act}

    def tick(self):
        p0e = self.dials[D_P0E]
        for e in self.edges:
            e.tick(p0e)
        thresh = to_signed16(self.dials[D_THRESH])
        ka = self.dials[D_KA] & 0xF
        if self.act >= thresh and self.refr == 0:
            afire = self.act
            self.act = 0
            self.refr = self.dials[D_REFR]
            return afire
        self.act = sclip16(self.act - (self.act >> ka))
        if self.refr:
            self.refr -= 1
        return None

    def view_wsum(self):
        return sat_u16(sum(e.readout() for e in self.edges))


# ------------------------------------------------------------------ fabric --

class BenchFabric:
    """room + four model cells, hearer-owned edges, one tick per round."""

    def __init__(self):
        self.cells = {}
        self.order = []
        self.round = 0
        self.events = []
        room = BenchCell(ROOM_ID, ROOM_NAME, "room")
        self.cells[ROOM_ID] = room
        self.order.append(ROOM_ID)
        for i, (name, _tag) in enumerate(MODELS):
            c = BenchCell(len(self.order), name, "model")
            self.cells[c.cid] = c
            self.order.append(c.cid)
            room.link(c.cid, ROOM_BASE_W)
            c.link(ROOM_ID, PATRON_BASE_W)
            nxt = 1 + ((i + 1) % len(MODELS))
            c.link(nxt, PATRON_BASE_W)
        self._round_heat = 0
        self.room = room

    def cell_by_name(self, name):
        for cid in self.order:
            if self.cells[cid].name == name:
                return self.cells[cid]
        return None

    def _deliver(self, speaker, dat, kind):
        hearers, verdicts = [], {}
        for cid in self.order:
            c = self.cells[cid]
            if c.cid == speaker.cid or c.find_edge(speaker.cid) is None:
                continue
            r = c.effect(speaker.cid, dat, kind)
            if r:
                hearers.append(c)
                verdicts[c.name] = r["verdict"][0].lower()
                self._round_heat += r["applied"]
        return verdicts

    def apply_op(self, speaker, op):
        """Apply one parsed op. Returns an event string."""
        if op["op"] == "fire":
            heat = op["heat"]
            dat = sclip16(heat * HEAT_UNIT)
            kind = KIND_STORY if heat > 0 else (KIND_GRIPE if heat < 0
                                                else KIND_IDLE)
            speaker.accounts["turns"] -= 1
            speaker.stats["fires"] += 1
            v = self._deliver(speaker, dat, kind)
            hv = ",".join("%s:%s" % (k, x) for k, x in sorted(v.items())) \
                or "nobody"
            return "%s FIRE %+d -> %s" % (speaker.name, heat, hv)
        if op["op"] == "link":
            tgt = self.cell_by_name(op["to"])
            e, fresh = speaker.link(tgt.cid, PATRON_BASE_W)
            speaker.stats["links"] += 1
            self._round_heat += 1024
            return "%s LINK%s->%s (w=%.2f walks=%d)" % (
                speaker.name, "" if fresh else "+", tgt.name,
                e.readout() / 32768.0, e.wh)
        if op["op"] == "dial":
            addr, delta = op["addr"], op["delta"]
            if addr == D_COSMIN:
                v = max(0, min(15, self.dial(speaker, addr) + delta))
            elif addr == D_HL:
                v = max(4, min(255, self.dial(speaker, addr) + delta))
            else:
                v = max(256, min(0x7FFF,
                                 self.dial(speaker, addr) + (delta << 11)))
            speaker.dials[addr] = v
            if addr == D_COSMIN and speaker.judgment is not None:
                speaker.judgment.openness = v
            speaker.stats["dials"] += 1
            return "%s DIAL %s%+d" % (speaker.name, DIAL_ALIASES[addr], delta)
        return "??"

    @staticmethod
    def dial(cell, addr):
        return cell.dials[addr]

    def round_tick(self):
        """One qm_tick for every cell; warmth EMA; emergent fires deliver
        at the end of the round (one legal serialization)."""
        self.round += 1
        fired = []
        for cid in self.order:
            af = self.cells[cid].tick()
            if af is not None:
                fired.append((cid, af))
        warmth = to_signed16(self.room.dials[D_ETA_F])
        warmth = sclip16(warmth + ((self._round_heat - warmth) >> 2))
        self.room.dials[D_ETA_F] = warmth & 0xFFFF
        self._round_heat = 0
        names = []
        for cid, af in fired:
            c = self.cells[cid]
            c.stats["emergent"] += 1
            self._deliver(c, af, KIND_STORY)
            names.append("%s(%.2f)" % (c.name, af / 32768.0))
        if names:
            self.event("EMERGENT-FIRE " + " ".join(names))
        return names

    def event(self, s):
        self.events.append("t%d %s" % (self.round, s))
        self.events = self.events[-12:]

    def warmth(self):
        return to_signed16(self.room.dials[D_ETA_F])

    def edge_table(self):
        rows = []
        for cid in self.order:
            c = self.cells[cid]
            for e in c.edges:
                rows.append({"src": c.name, "dst": self.cells[e.dst].name,
                             "src_id": e.src, "dst_id": e.dst,
                             "w": e.readout(), "wh": e.wh, "base": e.base})
        return rows

    # -- state-is-a-file ----------------------------------------------------

    def export_quf(self):
        names = ",".join(self.cells[c].name[:31] for c in self.order)
        doc = {
            "header": {
                "quf.version": "edgebench.py 1.0",
                "edge.k": K_BUCKETS,
                "tick_period": 1 << TPW,
                "bench.lane": "edge-bench",
                "bench.models": names,
                "bench.round": self.round,
                "bench.act": ",".join(str(self.cells[c].act & 0xFFFF)
                                      for c in self.order),
                "bench.refr": ",".join(str(self.cells[c].refr & 0xFFFF)
                                       for c in self.order),
            },
            "dials": [list(self.cells[c].dials) for c in self.order],
            "edges": [self.cells[c].edges[i].record()
                      for c in self.order
                      for i in range(len(self.cells[c].edges))],
            "routing": [{"dst": c, "via": c} for c in self.order],
            "ticksched": {"tpw": TPW,
                          "phases": [(c * 3) & 0xFFFF for c in self.order]},
        }
        return quf.build(doc)

    @classmethod
    def import_quf(cls, buf):
        parsed = quf.read(buf)
        dec = quf.decode_sections(parsed)
        hdr = parsed["header"]
        names = [n for n in hdr.get("bench.models", "").split(",") if n]
        acts = [int(x) for x in hdr.get("bench.act", "").split(",") if x]
        refrs = [int(x) for x in hdr.get("bench.refr", "").split(",") if x]
        f = cls.__new__(cls)
        f.cells, f.order, f.round = {}, [], int(hdr.get("bench.round", 0))
        f.events, f._round_heat = [], 0
        for row, name in zip(dec["dials"], names):
            kind = "room" if name == ROOM_NAME else "model"
            c = BenchCell(len(f.order), name, kind)
            c.dials = list(row)
            if kind == "model":
                c.judgment = model_taste(name)
                c.judgment.openness = c.dials[D_COSMIN]
            f.cells[c.cid] = c
            f.order.append(c.cid)
        for rec in dec["edges"]:
            c = f.cells[rec["src"]]
            e = LnEdge(rec["src"], rec["dst"], rec["slot"], rec["base"])
            e.wh, e.age = rec["wh"], rec["age"]
            c.edges.append(e)
        for cid, act in zip(f.order, acts):
            f.cells[cid].act = to_signed16(act & 0xFFFF)
        for cid, refr in zip(f.order, refrs):
            f.cells[cid].refr = refr & 0xFFFF
        f.room = f.cells[ROOM_ID]
        return f


# ------------------------------------------------------------- ollama i/o --

class OllamaError(Exception):
    pass


class Ollama:
    """Minimal stdlib Ollama /api/chat client."""

    def __init__(self, host=OLLAMA_HOST, timeout=240):
        self.host = host.rstrip("/")
        self.timeout = timeout

    def version(self):
        return self._get("/api/version").get("version", "?")

    def _get(self, path):
        with urllib.request.urlopen(self.host + path,
                                    timeout=self.timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    def chat(self, model, system, user, num_predict=None, temperature=0.7,
             num_ctx=1024, keep_alive="30m"):
        if num_predict is None:
            num_predict = NUM_PREDICT.get(model, 64)
        body = {
            "model": model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "stream": False,
            "keep_alive": keep_alive,
            "options": {"num_predict": num_predict,
                        "temperature": temperature,
                        "num_ctx": num_ctx},
        }
        if model in THINKING_MODELS:
            body["think"] = False
        prefill = model in PREFILL_MODELS
        if prefill:
            body["messages"] = body["messages"] + [
                {"role": "assistant", "content": PREFILL}]
        payload = json.dumps(body).encode("utf-8")
        last = None
        for attempt in (1, 2):
            t0 = time.time()
            try:
                req = urllib.request.Request(
                    self.host + "/api/chat", data=payload,
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    d = json.loads(r.read().decode("utf-8"))
                content = d.get("message", {}).get("content", "")
                if prefill:
                    content = PREFILL + content
                return {
                    "ok": True,
                    "content": content,
                    "eval_count": d.get("eval_count", 0),
                    "eval_dur_s": (d.get("eval_duration", 0) or 0) / 1e9,
                    "load_s": (d.get("load_duration", 0) or 0) / 1e9,
                    "latency_s": time.time() - t0,
                    "attempt": attempt,
                }
            except (urllib.error.URLError, urllib.error.HTTPError,
                    TimeoutError, OSError, ValueError) as ex:
                last = str(ex)
                time.sleep(2.0 * attempt)
        return {"ok": False, "error": last, "latency_s": time.time() - t0}


# ------------------------------------------------------------------ prompt --

SYSTEM_PROMPT = (
    "You are one cell in a five-cell graph (a bar room called the Tap). "
    "Every turn you must answer with EXACTLY ONE line: a single JSON "
    "object choosing your cell op. Copy the format shown in the prompt "
    "exactly. Integers must not be quoted. No prose, no markdown, no "
    "code fence, no explanation -- one JSON object only."
)


def turn_prompt(fab, speaker):
    c = speaker
    hear = ["%s w=%.2f walks=%d" % (fab.cells[e.dst].name, e.readout() / 32768.0,
                                    e.wh) for e in c.edges]
    hears_you = [fab.cells[cid].name for cid in fab.order
                 if cid != c.cid and fab.cells[cid].find_edge(c.cid)]
    d = c.dials
    lines = [
        "room round %d" % fab.round,
        "cells: %s" % " ".join(CELL_NAMES),
        "you are %s" % c.name,
        "you hear: %s" % (" | ".join(hear) or "nobody"),
        "hears you: %s" % (" ".join(hears_you) or "nobody"),
        "your dials: buzz=%+.2f earnestness=%.2f openness=%d halflife=%d"
        % (c.act / 32768.0, to_signed16(d[D_THRESH]) / 32768.0,
           d[D_COSMIN], d[D_HL]),
        "recent:",
    ]
    lines += ["  " + s for s in reversed(fab.events[-6:])] or ["  -"]
    lines += [
        "reply with exactly one line, one JSON object:",
        '{"op":"fire","heat":4}',
        '{"op":"link","to":"room"}',
        '{"op":"dial","addr":7,"delta":-2}',
        "heat: integer -8..8 | to: one of %s, not yourself | addr: 5 "
        "earnestness, 7 openness, 10 halflife | delta: integer -4..4"
        % " ".join(CELL_NAMES),
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------ parser --

_THINK_RE = re.compile(r"<think>.*?</think>", re.S)
_FENCE_RE = re.compile(r"```[a-zA-Z]*")


def extract_json(text):
    t = _THINK_RE.sub("", text)
    if "<think>" in t:
        t = t.split("<think>")[0]
    t = _FENCE_RE.sub("", t).replace("```", "")
    start = t.find("{")
    while start != -1:
        depth, in_str, esc = 0, False, False
        for i in range(start, len(t)):
            ch = t[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            elif ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return t[start:i + 1]
        start = t.find("{", start + 1)
    return None


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def parse_op(text, self_name):
    """Schema-strict parse of a model reply. Returns (op|None, reason|None).
    Any failure is the model's fault and is logged with the reason."""
    cand = extract_json(text)
    if cand is None:
        return None, "no_json"
    try:
        obj = json.loads(cand)
    except ValueError:
        return None, "not_json"
    if not isinstance(obj, dict):
        return None, "not_json"
    op = obj.get("op")
    if op == "fire":
        heat = obj.get("heat")
        if not _is_int(heat):
            return None, "schema:heat"
        if not -8 <= heat <= 8:
            return None, "range:heat"
        return {"op": "fire", "heat": heat}, None
    if op == "link":
        to = obj.get("to")
        if not isinstance(to, str):
            return None, "schema:to"
        low = to.strip().lower()
        match = next((n for n in CELL_NAMES if n == low), None)
        if match is None:
            return None, "unknown_cell:%s" % to.strip()[:24]
        if match == self_name:
            return None, "self_link"
        return {"op": "link", "to": match}, None
    if op == "dial":
        addr, delta = obj.get("addr"), obj.get("delta")
        if not _is_int(addr) or not _is_int(delta):
            return None, "schema:dial"
        if addr not in DIAL_ALIASES:
            return None, "unknown_dial:%s" % addr
        if not -4 <= delta <= 4:
            return None, "range:delta"
        return {"op": "dial", "addr": addr, "delta": delta}, None
    return None, "unknown_op:%s" % str(op)[:24]


# ------------------------------------------------------------------ checks --

def selftest():
    ok = True

    e = LnEdge(1, 2, 0, 8192)
    prev = 0
    for _ in range(64):
        e.train()
        w = e.readout()
        if w < prev:
            ok = False
            print("FAIL: ln readout not monotonic")
        prev = w
    if e.readout() != 8192 + int(LN_SCALE * math.log1p(64)):
        ok = False
        print("FAIL: ln readout value")
    if e.readout() > 8192 + int(LN_SCALE * math.log1p(0xFFFF)):
        ok = False
        print("FAIL: ln readout bound")

    e2 = LnEdge(1, 2, 0, 4096)
    for _ in range(20):
        e2.train()
    w0 = e2.wh
    for _ in range(30):
        e2.tick(BENCH_P0E)
    if not e2.wh < w0:
        ok = False
        print("FAIL: silence does not decay walks")

    cases = [
        ('{"op":"fire","heat":3}', "fire", None),
        ('```json\n{"op":"link","to":"Nano"}\n```', "link", None),
        ('<think>hmm</think>{"op":"dial","addr":5,"delta":-2}', "dial", None),
        ('Sure! {"op":"fire","heat":-8} hope that helps', "fire", None),
        ('{"op":"fire","heat":9}', None, "range:heat"),
        ('{"op":"blink"}', None, "unknown_op:blink"),
        ('{"op":"dial","addr":9,"delta":1}', None, "unknown_dial:9"),
        ('{"op":"fire"}', None, "schema:heat"),
        ('I would fire enthusiastically', None, "no_json"),
        ('{"op": "fire", "heat": true}', None, "schema:heat"),
    ]
    for text, want_op, want_fail in cases:
        op, why = parse_op(text, "lfm")
        if want_op is not None and (op is None or op["op"] != want_op):
            ok = False
            print("FAIL parse: %r -> %r %r" % (text[:40], op, why))
        if want_op is None and want_fail is not None and why != want_fail:
            ok = False
            print("FAIL reason: %r -> %r (want %r)" % (text[:40], why, want_fail))
    op, why = parse_op('{"op":"link","to":"lfm"}', "lfm")
    if op is not None or why != "self_link":
        ok = False
        print("FAIL: self link not rejected")

    fab = BenchFabric()
    if len(fab.order) != 5 or len(fab.edge_table()) != 12:
        ok = False
        print("FAIL: seed graph shape")
    lfm = fab.cell_by_name("lfm")
    fab.apply_op(lfm, {"op": "fire", "heat": 6})
    fab.apply_op(lfm, {"op": "link", "to": "wesley"})
    fab.apply_op(lfm, {"op": "dial", "addr": 7, "delta": 1})
    fab.round_tick()
    buf = fab.export_quf()
    issues = quf.verify_bytes(buf, "selftest.quf")
    if issues:
        ok = False
        print("FAIL: QUF verify: %s" % issues)
    if quf.rebuild(quf.read(buf)) != buf:
        ok = False
        print("FAIL: QUF round-trip not byte-exact")
    f2 = BenchFabric.import_quf(buf)
    if f2.export_quf() != buf:
        ok = False
        print("FAIL: import/export not byte-exact")
    if f2.cell_by_name("lfm").edges[0].wh != \
            fab.cell_by_name("lfm").edges[0].wh:
        ok = False
        print("FAIL: walks not restored")

    if not ok:
        sys.exit(1)
    print("edgebench selftest PASS: ln-edge, decay, parser, QUF round-trip")


# --------------------------------------------------------------------- CLI --

def main(argv=None):
    ap = argparse.ArgumentParser(prog="edgebench.py")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    ap.error("see --selftest (the harness drivers are run_night.py/report.py)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
