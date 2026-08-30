#!/usr/bin/env python3
"""boot_fuzz.py -- quf_boot boundary fuzz: fuzzed QUF byte streams vs the
real boot FSM in iverilog (backend lane, Phase 2).

Contract under test (docs/FPGA-BOOT.md §1/§2, the warm-boot half of
"state is a file"):
  * a stream Python accepts (read+verify clean, not truncated) MUST boot:
    quf_boot reaches RUN, o_err==0, epoch pulsed exactly once, and the
    mycell dial row lands bit-exact. Python-clean + RTL-refused is a
    SPLIT-BRAIN finding (producer tool and silicon disagree).
  * a stream Python rejects for load-bearing reasons MUST fail static:
    HOLD_ERR sticky, o_rst_n NEVER asserted (never a released half-image).
  * don't-care corruption (padding, unknown-KV bytes, kind field, digest
    content) may go either way, but the FSM must TERMINATE and
    release ⟹ (RUN ∧ err==0).

Manifest: tb/run/boot_fuzz.hex (cases back-to-back; the TB PORs between
them). Per case: EXP, NBYTES, bytes, HAS_DIALS, d0..d15, tpw.
  EXP 0 = MUST_FAIL_STATIC, 1 = MUST_BOOT, 2 = EITHER.
Findings printed loud; exit 1 on any. Stdlib only.
"""
import os
import random
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
_TOOLS = os.path.join(_ROOT, "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
import quf  # noqa: E402

MYCELL = 2          # the cell row this boot instance claims
FAIL, BOOT, EITHER = 0, 1, 2
TBL = os.path.join(_ROOT, "tb", "tb_boot_fuzz.v")
OUT = os.path.join(_ROOT, "tb", "run")

# issues Python flags that the RTL legitimately cannot see (no sha engine,
# no kind policing, no tick_period cross-check, duplicate names where the
# loader is last-wins like the Python dict, alignment policing)
HW_BLIND = ("quf.sha256 mismatch", "non-standard kind",
            "tick_period", "duplicate section name", "align")


def hw_loadbearing(issues):
    return [i for i in issues if not any(b in i for b in HW_BLIND)]


def rand_doc(rng, cc):
    k = rng.choice([1, 4, 8, 16])
    doc = {
        "header": {"cell_count": cc, "edge.k": k,
                   "align": rng.choice([8, 16, 32])},
        "dials": [[rng.randrange(0x10000) for _ in range(quf.NDIALS)]
                  for _ in range(cc)],
        "edges": [{"src": rng.randrange(cc), "dst": rng.randrange(cc),
                   "mode": rng.randrange(2), "slot": rng.randrange(4),
                   "base": rng.randrange(0x10000), "wh": rng.randrange(4),
                   "age": 0, "buckets": [0] * k}
                  for _ in range(rng.randrange(0, 5))],
        "routing": [],
        "ticksched": {"tpw": rng.randrange(0, 32), "phases":
                      [rng.randrange(0x10000) for _ in range(cc)]},
    }
    if rng.random() < 0.4:
        doc["header"]["quf.version"] = "bootfuzz 1.0"
    if rng.random() < 0.3:
        doc["header"]["tap.cellnames"] = ",".join("c%d" % i
                                                  for i in range(cc))
    return doc


def expect_for(stream):
    """classify a stream: what must the RTL do"""
    if len(stream) == 0:
        return None                     # TB class 3: waits in HOLD (no byte)
    try:
        parsed = quf.read(bytes(stream))
        issues = quf.verify_bytes(bytes(stream), "fz")
    except quf.QufError:
        return FAIL
    if hw_loadbearing(issues):
        return FAIL
    # declared content must be inside the stream (not truncated)
    for name, kind, off, size in parsed["table"]:
        if off + size > len(stream):
            return FAIL
    return BOOT


def build_cases(seed=0xB007F02):
    rng = random.Random(seed)
    cases = []                          # (exp, bytes, dials or None, tpw)

    def add(stream, exp=None, doc=None):   # doc: kept for call-site clarity
        stream = bytes(stream)
        if exp is None:
            exp = expect_for(stream)
        if exp is None:                 # empty stream: class 3 (HOLD wait)
            cases.append((3, stream, None, 0))
            return
        dials, tpw = None, 0
        if exp == BOOT:
            # oracle = decode the ACTUAL stream (corrupted files boot with
            # the corrupted values -- that is what the loader must land)
            try:
                p_ = quf.read(stream)
                dec = quf.decode_sections(p_)
                cc_ = p_["header"].get("cell_count", 0)
                if cc_ > MYCELL and "dials" in dec:
                    dials = list(dec["dials"][MYCELL])
                    # dial 13 (FTRACE) is a read-only probe alias in
                    # q_dialfile: loader writes to it are ignored by
                    # construction, so the bound value is the POR default 0
                    dials[13] = 0
                tpw = dec.get("ticksched", {}).get("tpw", 0) & 0x1F
            except quf.QufError:
                pass
        cases.append((exp, stream, dials, tpw))

    # -- valid files, several shapes ----------------------------------
    valids = []
    for cc in (1, 3, 4, 5, 8):
        doc = rand_doc(rng, cc)
        valids.append((doc, quf.build(doc)))
    # digest-bearing file (string KV the loader must skip)
    doc_d = rand_doc(rng, 6)
    valids.append((doc_d, quf.build(quf.add_digest(doc_d))))
    # file with NO sections at all
    valids.append((None, quf.build({"header": {"cell_count": 1,
                                               "align": 8}})))
    # zero-size known section (the pleft-underflow regression): cc=0
    # builds a dials section with zero rows
    zdoc2 = {"header": {"cell_count": 0, "edge.k": 8, "align": 8},
             "dials": [], "edges": [], "routing": []}
    valids.append((zdoc2, quf.build(zdoc2)))
    # zero-size dials + REAL ticks: the true underflow shape (a lone
    # zero-size section is skipped by the same-cycle have/goto_data race;
    # with a second section present the loader really enters the empty
    # payload and pleft underflows -- unfixed this is E_TRUNC on a
    # verify-clean file: split-brain)
    zdoc3 = {"header": {"cell_count": 0, "edge.k": 8, "align": 8},
             "dials": [], "edges": [], "routing": [],
             "ticksched": {"tpw": 5, "phases": []}}
    valids.append((zdoc3, quf.build(zdoc3)))
    # single-section file (dials ONLY -- no ticks/edges/routing): the
    # last-table-entry have-set races goto_data's stale qany, and a
    # single-section file boots WITHOUT LOADING its only section
    s1 = {"header": {"cell_count": 3, "edge.k": 8, "align": 8},
          "dials": [[0x1111 * (r + 1) & 0xFFFF for _ in range(16)]
                    for r in range(3)]}
    valids.append((s1, quf.build(s1)))

    for doc, buf in valids:
        add(buf, doc=doc)
        content_end = max([o + s for _, _, o, s in quf.read(buf)["table"]],
                          default=0)
        # truncations: before header, mid, at content end, full, past end
        for n in (0, 4, 16, 40, content_end // 2 or 1,
                  max(0, content_end - 1), content_end,
                  min(len(buf), content_end + 1), len(buf)):
            if 0 <= n <= len(buf):
                # doc passed: truncations that still carry full content
                # (>= content_end) boot with the real dial row + tpw
                add(buf[:n], doc=(doc if n >= content_end else None))
        # corruptions at region-representative offsets
        parsed = quf.read(buf)
        kv_end = 16 + sum(4 + len(k.encode()) + 4 + len(quf.pack_value(vt, v))
                          for k, vt, v in parsed["kv"])
        spots = {0: "magic", 4: "ver", 8: "endian", 12: "nkv",
                 kv_end - 1: "kv-tail", kv_end + 2: "tbl-hdr"}
        for _, kind_, off, size in parsed["table"]:
            spots[off] = "payload-start"
            spots[off + size - 1] = "payload-end"
            spots[off - 4] = "pre-payload"
        spots[len(buf) - 1] = "last-pad"
        for off in sorted(spots):
            if 0 <= off < len(buf):
                b = bytearray(buf)
                b[off] ^= 0x5A
                # doc passed: corruption in don't-care bytes still boots
                # with the real dial row + tpw (checked when exp==BOOT)
                add(bytes(b), doc=doc)

    # -- garbage streams -----------------------------------------------
    add(b"")
    add(b"\x00" * 64)
    add(b"QUF\x00" + b"\x00" * 60)          # valid magic, zeroed rest
    add(bytes(rng.randrange(256) for _ in range(200)))
    add(b"QUF\x00\x01\x00\x00\x00\x01\x00\x00\x00" + b"\xff" * 40)
    return cases


def write_manifest(cases):
    os.makedirs(OUT, exist_ok=True)
    lines = ["%04X" % len(cases)]
    for exp, stream, dials, tpw in cases:
        lines.append("%04X" % exp)
        lines.append("%04X" % len(stream))
        lines += ["%02X" % b for b in stream]
        lines.append("0001" if dials else "0000")
        lines += ["%04X" % (d & 0xFFFF) for d in (dials or [0] * 16)]
        lines.append("%04X" % (tpw & 0x1F))
    path = os.path.join(OUT, "boot_fuzz.hex")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


def run_tb():
    vvp = os.path.join(OUT, "tb_boot_fuzz.vvp")
    env = dict(os.environ)
    env["PATH"] = "/home/eileen/tools/oss-cad-suite/bin:" + env["PATH"]
    r = subprocess.run(
        "iverilog -g2005 -s tb_boot_fuzz -o %s rtl/q_uf_loader.v "
        "rtl/quf_boot.v rtl/q_dialfile.v tb/tb_boot_fuzz.v && vvp %s"
        % (vvp, vvp),
        shell=True, cwd=_ROOT, capture_output=True, text=True, env=env)
    return r


def main():
    # Second-generation pass: argv[1]=seed override (default: pinned 0xB007F02).
    seed = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0xB007F02
    cases = build_cases(seed)
    path = write_manifest(cases)
    nfail = sum(1 for c in cases if c[0] == FAIL)
    nboot = sum(1 for c in cases if c[0] == BOOT)
    neither = sum(1 for c in cases if c[0] == EITHER)
    nhold = sum(1 for c in cases if c[0] == 3)
    print("boot_fuzz: %d cases (%d must-boot, %d must-fail-static, "
          "%d either, %d hold-wait) -> %s" % (len(cases), nboot, nfail,
                                              neither, nhold, path))
    r = run_tb()
    out = r.stdout + r.stderr
    print(out.strip())
    if r.returncode != 0 or "BOOT-FUZZ FAIL" in out:
        return 1
    if "BOOT-FUZZ PASS" not in out:
        print("boot_fuzz: no verdict line from TB")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
