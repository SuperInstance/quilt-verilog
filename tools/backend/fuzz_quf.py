#!/usr/bin/env python3
"""fuzz_quf.py -- QUF format fuzz + property bench (backend lane).

The adversarial first user's format hammer. Three families, exact
counters, loud PASS/FAIL (house style; deterministic via fixed seeds):

  A. round-trip properties on random VALID cell configs:
       read(build(x)) decodes to x        (decode(encode(x)) == x)
       rebuild(read(build(x))) byte-exact (writer is canonical)
       rebuild(rebuild(...)) idempotent   (rebuild is a fixed point)
       verify(build(x)) == []             (writer output always clean)
     Config axes: cell_count 1..9, edge.k 1..16 (incl. 1 and 16), align
     8..4096 pow2, out-of-range dials, zero/max k, huge tpw (epoch),
     empty sections, duplicate dst nonce-ish collisions in routing.

  B. INVALID configs must be rejected LOUD (QufError), never a silent
     wrong build: dial>u16, edge src>u8, k=0, k=17, align=0/3/huge,
     cell_count negative/2^32, tpw=32 (tick_period>u32), float/bool
     headers, NaN dials, list-typed docs.

  C. corruption sweep on built files: for every offset class (header,
     KV area, section table, payload, tail padding), flip bytes --
     read/verify/decode/rebuild must either succeed cleanly or raise
     QufError; ANY other exception is a FINDING. Truncation at every
     length: verify fails for lengths that cut declared content.
     Digest files: payload corruption must be CAUGHT by verify.

Exit 0 iff zero findings. Stdlib only.
"""
import json
import os
import random
import struct
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.normpath(os.path.join(_HERE, "..", "..", "tools"))
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
import quf  # noqa: E402

FINDINGS = []
N = {}          # counters


def count(k, n=1):
    N[k] = N.get(k, 0) + n


def finding(msg):
    FINDINGS.append(msg)
    print("  FINDING: %s" % msg)


# ------------------------------------------------------------------ A ----

def rand_dials(rng):
    return [[rng.choice([0, 1, 0xFFFF, rng.randrange(0x10000),
                         rng.randrange(0x8000)])
             for _ in range(quf.NDIALS)] for _ in range(8)]


def rand_doc(rng):
    cc = rng.choice([1, 2, 3, rng.randrange(1, 10)])
    k = rng.choice([1, 2, 8, 16, rng.randrange(1, 17)])
    align = rng.choice([8, 16, 32, 64, 4096])
    doc = {
        "header": {"cell_count": cc, "edge.k": k, "align": align},
        "dials": [[0 if j == 13 else rng.randrange(0x10000)
                   for j in range(quf.NDIALS)]
                  for _ in range(cc)],
        "edges": [{"src": rng.randrange(cc), "dst": rng.randrange(cc),
                   "mode": rng.randrange(2), "slot": rng.randrange(4),
                   "base": rng.randrange(0x10000), "wh": rng.randrange(0x10000),
                   "age": rng.randrange(1 << 32),
                   "buckets": [rng.randrange(0x100) for _ in range(k)]}
                  for _ in range(rng.randrange(0, 2 * cc + 2))],
        "routing": [{"dst": rng.randrange(cc), "via": rng.randrange(cc)}
                    # deliberate dst collisions: nonce-shaped
                    for _ in range(rng.randrange(0, cc + 3))],
        "ticksched": {"tpw": rng.choice([0, 1, 6, 31]),
                      "phases": [rng.randrange(0x10000)
                                 for _ in range(rng.randrange(0, cc + 1))]},
    }
    return doc


def canon(doc):
    """The decoded view of doc's build (what round-trip equality means)."""
    return {
        "dials": doc["dials"],
        "edges": sorted([
            dict(src=e["src"], dst=e["dst"], mode=e["mode"], slot=e["slot"],
                 base=e["base"], wh=e["wh"], age=e["age"],
                 buckets=(list(e.get("buckets", []))[:doc["header"]["edge.k"]]
                          + [0] * (doc["header"]["edge.k"]
                                   - len(e.get("buckets", [])))))
            for e in doc["edges"]], key=lambda e: (e["src"], e["dst"],
                                                   e["slot"])),
        "routing": doc["routing"],
        "ticks": {"tpw": doc["ticksched"]["tpw"],
                  "phases": (list(doc["ticksched"].get("phases", []))[:doc["header"]["cell_count"]]
                             + [0] * (doc["header"]["cell_count"]
                                      - len(doc["ticksched"].get("phases", []))))},
    }


def prop_roundtrip(iters=600, seed=0xC0FFEE):
    rng = random.Random(seed)
    for i in range(iters):
        doc = rand_doc(rng)
        try:
            data = quf.build(doc)
        except quf.QufError as ex:
            finding("A: valid-ish doc rejected by build: %s (doc cc=%r)"
                    % (ex, doc["header"]))
            continue
        count("A_builds")
        try:
            parsed = quf.read(data)
        except quf.QufError as ex:
            finding("A: read(build) failed: %s" % ex)
            continue
        # decode(encode(x)) == x
        dec = quf.decode_sections(parsed)
        want = canon(doc)
        got = {
            "dials": dec.get("dials"),
            "edges": sorted(dec.get("edges", []),
                             key=lambda e: (e["src"], e["dst"],
                                            e["slot"])),
            "routing": dec.get("routing", []),
            "ticks": dec.get("ticksched",
                              {"tpw": doc["ticksched"]["tpw"],
                               "phases": [0] * doc["header"]["cell_count"]}),
        }
        want["edges"] = sorted(want["edges"], key=lambda e: (e["src"],
                                                           e["dst"], e["slot"]))
        want["routing"] = want["routing"] or []
        if want != got:
            for key in want:
                if want[key] != got[key]:
                    finding("A: round-trip mismatch in %r (iter %d)" % (key, i))
                    break
            continue
        count("A_decode_eq")
        # rebuild byte-exact + idempotent
        b2 = quf.rebuild(parsed)
        if b2 != data:
            finding("A: rebuild not byte-exact (iter %d)" % i)
            continue
        count("A_rebuild_exact")
        b3 = quf.rebuild(quf.read(b2))
        if b3 != b2:
            finding("A: rebuild not idempotent (iter %d)" % i)
        issues = quf.verify_bytes(data)
        if issues:
            finding("A: verify(build) issues: %s (iter %d)" % (issues, i))
        else:
            count("A_verify_clean")


# ------------------------------------------------------------------ B ----

def prop_invalid():
    bad = [
        ("dial>u16", {"header": {"cell_count": 1},
                      "dials": [[0x10000] + [0] * 15]}),
        ("dial<0", {"header": {"cell_count": 1},
                    "dials": [[-1] + [0] * 15]}),
        ("edge src>u8", {"header": {"cell_count": 1, "edge.k": 8},
                         "dials": [[0] * 16],
                         "edges": [{"src": 256, "dst": 0, "mode": 0,
                                    "slot": 0, "base": 0, "wh": 0, "age": 0,
                                    "buckets": [0] * 8}]}),
        ("k=0", {"header": {"cell_count": 1, "edge.k": 0},
                 "dials": [[0] * 16]}),
        ("k=17", {"header": {"cell_count": 1, "edge.k": 17},
                  "dials": [[0] * 16]}),
        ("align=0", {"header": {"cell_count": 1, "align": 0},
                     "dials": [[0] * 16]}),
        ("align=3", {"header": {"cell_count": 1, "align": 3},
                     "dials": [[0] * 16]}),
        ("align huge", {"header": {"cell_count": 1, "align": 1 << 31},
                        "dials": [[0] * 16]}),
        ("cell_count 2^32", {"header": {"cell_count": 1 << 32},
                             "dials": []}),
        ("cell_count -5", {"header": {"cell_count": -5}, "dials": []}),
        ("tpw=32 (tick_period>u32)", {"header": {"cell_count": 1},
                                      "dials": [[0] * 16],
                                      "ticksched": {"tpw": 32}}),
        ("float header", {"header": {"cell_count": 1.5},
                          "dials": [[0] * 16]}),
        ("bool header", {"header": {"cell_count": True},
                         "dials": [[0] * 16]}),
        ("NaN dial", {"header": {"cell_count": 1},
                      "dials": [[float("nan")] + [0] * 15]}),
        ("list doc", [1, 2, 3]),
        ("null doc", None),
        ("header list", {"header": [1], "dials": [[0] * 16]}),
        ("dials row short", {"header": {"cell_count": 1},
                             "dials": [[0] * 15]}),
        ("dials rows<cc", {"header": {"cell_count": 2},
                           "dials": [[0] * 16]}),
    ]
    for name, doc in bad:
        doc = json.loads(json.dumps(doc, default=lambda o: "nan"))
        try:
            quf.build(doc)
            finding("B: %s NOT rejected by build" % name)
        except quf.QufError:
            count("B_rejected")
        except Exception as ex:
            finding("B: %s rejected with WRONG exception %s: %s"
                    % (name, type(ex).__name__, ex))
        except RecursionError:
            pass
    # NaN survives the json roundtrip as float -- handle directly:
    try:
        quf.build({"header": {"cell_count": 1},
                   "dials": [[float("nan")] + [0] * 15]})
        finding("B: NaN dial NOT rejected by build")
    except quf.QufError:
        count("B_rejected")
    # array extras: the u32-array path must WORK (was dead code: the
    # element loop tested the list, not the element)
    try:
        data = quf.build({"header": {"cell_count": 1, "tap.flags": [1, 2, 3]},
                          "dials": [[0] * 16]})
        p = quf.read(data)
        assert p["header"]["tap.flags"] == [1, 2, 3], p["header"]
        count("B_array_extra_ok")
    except Exception as ex:
        finding("B: u32 array extra rejected/broken: %s: %s"
                % (type(ex).__name__, ex))
    try:
        quf.build({"header": {"x": ["a"]}, "dials": [[0] * 16]})
        finding("B: str-array extra NOT rejected")
    except quf.QufError:
        count("B_rejected")


# ------------------------------------------------------------------ C ----

def classify_offsets(data, parsed):
    """map offset -> region label"""
    kv_end = 16 + sum(4 + len(k.encode()) + 4 + len(quf.pack_value(vt, v))
                      for k, vt, v in parsed["kv"])
    tbl_end = kv_end + 4 + sum(4 + len(n.encode()) + 20
                               for n, _, _, _ in parsed["table"])
    regions = {}
    for off in range(len(data)):
        if off < 16:
            regions[off] = "header"
        elif off < kv_end:
            regions[off] = "kv"
        elif off < tbl_end:
            regions[off] = "table"
        else:
            regions[off] = "tail"
    for name, kind, soff, ssize in parsed["table"]:
        for off in range(soff, soff + ssize):
            regions[off] = "payload:" + name
    return regions


def prop_corrupt(iters=40, files=6, seed=0xBADC0DE):
    rng = random.Random(seed)
    regions_all = {}
    for fi in range(files):
        doc = rand_doc(rng)
        data = quf.build(doc)
        parsed = quf.read(data)
        regions = classify_offsets(data, parsed)
        for off, lab in regions.items():
            regions_all.setdefault(lab, 0)
            regions_all[lab] += 1
        for _ in range(iters):
            off = rng.randrange(len(data))
            bit = 1 << rng.randrange(8)
            b = bytearray(data)
            b[off] ^= bit
            buf = bytes(b)
            for fn in (quf.read, lambda x: quf.verify_bytes(x, "fz"),
                       lambda x: quf.decode_sections(quf.read(x))
                       if _read_ok(x) else None,
                       lambda x: quf.rebuild(quf.read(x))
                       if _read_ok(x) else None):
                try:
                    fn(buf)
                    count("C_ok_" + regions[off].split(":")[0])
                except quf.QufError:
                    count("C_quferror_" + regions[off].split(":")[0])
                except Exception as ex:
                    finding("C: corrupt %s+%d/%d raises %s: %s"
                            % (regions[off], off, bit,
                               type(ex).__name__, ex))
        count("C_files")
    return regions_all


def _read_ok(buf):
    try:
        quf.read(buf)
        return True
    except quf.QufError:
        return False


def prop_truncate(files=6):
    rng = random.Random(0xFACE)
    for fi in range(files):
        doc = rand_doc(rng)
        data = quf.build(doc)
        parsed = quf.read(data)
        content_end = max(off + size for _, _, off, size in parsed["table"])
        for n in range(0, len(data)):
            issues = quf.verify_bytes(data[:n], "tr")
            if n < content_end:
                if not issues:
                    finding("C: truncation to %d (< content end %d) "
                            "verifies CLEAN" % (n, content_end))
                else:
                    count("C_trunc_caught")
            else:
                count("C_trunc_padding_ok" if not issues
                      else "C_trunc_flagged")


def prop_digest():
    rng = random.Random(0xD16E57)
    for i in range(60):
        doc = rand_doc(rng)
        data = quf.build(quf.add_digest(doc))
        if quf.verify_bytes(data):
            finding("digest: clean file flagged")
        count("D_clean")
        parsed = quf.read(data)
        payload_offs = [(off, size) for _, _, off, size in parsed["table"]]
        if not payload_offs:
            continue
        off, size = payload_offs[rng.randrange(len(payload_offs))]
        if size == 0:
            continue
        p = off + rng.randrange(size)
        b = bytearray(data)
        b[p] ^= 1 << rng.randrange(8)
        issues = quf.verify_bytes(bytes(b), "dz")
        if not any("sha256" in i for i in issues):
            finding("digest: payload corruption at %d NOT caught" % p)
        else:
            count("D_caught")


def prop_rebuild_align():
    """hostile align KVs must fail loud, not ZeroDivision/MemoryError"""
    data = quf.build({"header": {"cell_count": 1}, "dials": [[0] * 16]})
    for align in (0, 3, 1 << 31, (1 << 31) - 1, 1 << 24):
        b = bytearray(data)
        # craft: append a KV "align" is already there (32) -- patch it:
        parsed = quf.read(bytes(b))
        kv = [(k, vt, v) for k, vt, v in parsed["kv"]]
        kv = [("align", quf.T_U32, align) if k == "align" else (k, vt, v)
              for k, vt, v in kv]
        import copy
        p2 = copy.deepcopy(parsed)
        p2["kv"] = kv
        try:
            out = quf.rebuild(p2)
            if align in (0, 3, 1 << 24, 1 << 31) and len(out) > (1 << 22):
                finding("rebuild: align=%d built a %d-byte bomb"
                        % (align, len(out)))
                continue
            count("R_align_handled")
        except quf.QufError:
            count("R_align_rejected")
        except Exception as ex:
            finding("rebuild: align=%d raises %s: %s"
                    % (align, type(ex).__name__, ex))


def main():
    # Second-generation pass support: argv[1]=roundtrip iters,
    # argv[2]=seed base (default: pinned discovery values).
    rt_iters = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    seed_base = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0
    print("== A: round-trip properties (%d random configs, seed base %d) =="
          % (rt_iters, seed_base or 0xC0FFEE))
    prop_roundtrip(iters=rt_iters,
                   seed=(0xC0FFEE + seed_base) if seed_base else 0xC0FFEE)
    print("== B: invalid configs rejected loud ==")
    prop_invalid()
    print("== C: corruption sweep (40 x 6 files) + truncation ==")
    prop_corrupt()
    prop_truncate()
    print("== D: digest integrity ==")
    prop_digest()
    print("== R: rebuild align guards ==")
    prop_rebuild_align()
    print()
    for k in sorted(N):
        print("  %-26s %d" % (k, N[k]))
    print()
    if FINDINGS:
        print("FUZZ FAIL: %d findings" % len(FINDINGS))
        for f in FINDINGS:
            print("  - %s" % f)
        return 1
    print("FUZZ PASS: %d counters, 0 findings" % len(N))
    return 0


if __name__ == "__main__":
    sys.exit(main())
