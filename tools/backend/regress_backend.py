#!/usr/bin/env python3
"""regress_backend.py -- regression bench: one loud test per bug the
adversarial first user broke (backend lane, Phase 4). A bug without a
regression test isn't fixed; every fix from BACKEND-NOTES.md is pinned
here. House style: exact checks, PASS/FAIL lines, exit 1 on any failure.
"""
import os
import re
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tools"))
sys.path.insert(0, os.path.join(_ROOT, "sim", "tools"))
import quf          # noqa: E402
import tapfabric as tf  # noqa: E402

PY = sys.executable
QUF = os.path.join(_ROOT, "tools", "quf.py")
FAILS = []
N = 0


def check(name, cond, detail=""):
    global N
    N += 1
    if cond:
        print("  ok   %s" % name)
    else:
        FAILS.append(name)
        print("  FAIL %s %s" % (name, detail))


def run_cli(*args, cwd=None):
    return subprocess.run([PY, QUF] + list(args), capture_output=True,
                          text=True, cwd=cwd or _ROOT)


GOOD_DOC = {
    "header": {"cell_count": 2, "edge.k": 8, "align": 32},
    "dials": [[i | 1 for i in range(16)] for _ in range(2)],
    "edges": [{"src": 0, "dst": 1, "mode": 0, "slot": 0, "base": 4096,
               "wh": 0, "age": 0, "buckets": [1] + [0] * 7}],
    "ticksched": {"tpw": 6, "phases": [0, 3]},
}
GOOD = quf.build(GOOD_DOC)


def t_cli_hygiene():
    print("== CLI hygiene (raw tracebacks -> clean errors) ==")
    with tempfile.TemporaryDirectory() as d:
        r = run_cli("info", os.path.join(d, "nope.quf"))
        check("info nonexistent: rc=1, no traceback",
              r.returncode == 1 and "Traceback" not in r.stderr
              and r.stderr.strip().startswith("quf.py: error:"), r.stderr[:80])
        r = run_cli("info", d)
        check("info directory: clean fail",
              r.returncode == 1 and "Traceback" not in r.stderr)
        badj = os.path.join(d, "bad.json")
        with open(badj, "w") as f:
            f.write("[1,2]")
        r = run_cli("create", badj, os.path.join(d, "o.quf"))
        check("create list JSON: clean QufError",
              r.returncode == 1 and "Traceback" not in r.stderr)
        with open(badj, "w") as f:
            f.write("{oops")
        r = run_cli("create", badj, os.path.join(d, "o.quf"))
        check("create bad JSON: clean QufError",
              r.returncode == 1 and "Traceback" not in r.stderr)
        r = run_cli("create", os.path.join(_ROOT, "tb", "quf_tb.json"),
                    os.path.join(d, "nodir", "x.quf"))
        check("create missing outdir: clean fail",
              r.returncode == 1 and "Traceback" not in r.stderr)
        # corrupt-file reads: every command fails CLEAN (QufError)
        b = bytearray(GOOD)
        b[20] = 0x9C            # KV name byte -> invalid UTF-8
        p = os.path.join(d, "c1.quf")
        with open(p, "wb") as f:
            f.write(bytes(b))
        for sub in ("info", "dump", "verify"):
            r = run_cli(sub, p)
            check("%s bad-utf8-kv: clean fail" % sub,
                  r.returncode == 1 and "Traceback" not in r.stderr,
                  r.stderr[:80])
        # header lies about cell_count: decode must QufError, not
        # struct.error (dump path)
        doc = {"header": {"cell_count": 4, "edge.k": 8, "align": 8},
               "dials": GOOD_DOC["dials"], "edges": [],
               "routing": [], "ticksched": GOOD_DOC["ticksched"]}
        # cell_count=4 but 2 rows: build refuses; craft via table edit
        parsed = quf.read(GOOD)
        import copy
        p2 = copy.deepcopy(parsed)
        p2["kv"] = [("cell_count", 4, 4) if k == "cell_count" else (k, vt, v)
                    for k, vt, v in p2["kv"]]
        crafted = quf.rebuild(p2)
        with open(p, "wb") as f:
            f.write(crafted)
        r = run_cli("dump", p)
        check("dump header-lies cc: clean fail (decode guard)",
              r.returncode == 1 and "Traceback" not in r.stderr)
        issues = quf.verify_bytes(crafted)
        check("verify header-lies cc: flagged",
              any("decodable" in i or "dials size" in i for i in issues),
              issues)


def t_quf_library():
    print("== quf.py library hardening ==")
    # u32 array extras: the element loop tested the list, not the element
    # (dead code -- every array extra was rejected)
    data = quf.build({"header": {"cell_count": 1, "tap.flags": [1, 2, 3]},
                      "dials": [[0] * 16]})
    p = quf.read(data)
    check("u32 array extra accepted + round-trips",
          p["header"].get("tap.flags") == [1, 2, 3])
    try:
        quf.build({"header": {"cell_count": 1, "x": ["s"]},
                   "dials": [[0] * 16]})
        check("str array extra rejected", False)
    except quf.QufError:
        check("str array extra rejected", True)
    # align guards in rebuild: 0 -> ZeroDivisionError, 2^31 -> bomb (was)
    import copy
    for align in (0, 3, 1 << 24, 1 << 31):
        parsed = quf.read(GOOD)
        p2 = copy.deepcopy(parsed)
        p2["kv"] = [("align", 4, align) if k == "align" else (k, vt, v)
                    for k, vt, v in p2["kv"]]
        try:
            out = quf.rebuild(p2)
            check("rebuild align=%d rejected" % align,
                  False, "built %d bytes" % len(out))
        except quf.QufError:
            check("rebuild align=%d rejected" % align, True)
    # build-side align cap
    try:
        quf.build({"header": {"cell_count": 1, "align": 1 << 31},
                   "dials": [[0] * 16]})
        check("build align=2^31 rejected", False)
    except quf.QufError:
        check("build align=2^31 rejected", True)
    # duplicate section names flagged (sections drive rebuild, not table)
    parsed = quf.read(GOOD)
    p2 = copy.deepcopy(parsed)
    p2["sections"].append(p2["sections"][0])
    dup = quf.rebuild(p2)
    check("duplicate section names flagged",
          any("duplicate section" in i for i in quf.verify_bytes(dup)))
    # names > 255 B flagged (hardware loaders reject with E_NAME)
    long_name = "z" * 300
    parsed = quf.read(GOOD)
    p2 = copy.deepcopy(parsed)
    p2["kv"].append((long_name, 4, 1))
    dup = quf.rebuild(p2)
    check("KV name >255B flagged",
          any("255" in i for i in quf.verify_bytes(dup)))
    # tick_period/tpw consistency, no int->str digit bomb on garbage tpw
    b = bytearray(GOOD)
    parsed = quf.read(bytes(b))
    ticks_off = [t for t in parsed["table"] if t[0] == "ticks"][0][2]
    b[ticks_off] = 0xF0                       # tpw garbage-huge
    issues = quf.verify_bytes(bytes(b))
    check("garbage tpw: flagged without ValueError",
          any("tick_period" in i for i in issues))
    # typed-KV guards (edge.k as string etc.)
    for kv, val in (("edge.k", "8"), ("cell_count", "2"),
                    ("edge_count", "3"), ("route_count", "3")):
        parsed = quf.read(GOOD)
        p2 = copy.deepcopy(parsed)
        p2["kv"] = [(kv, 8, val) if k == kv else (k, vt, v)
                    for k, vt, v in p2["kv"]]
        crafted = quf.rebuild(p2)
        issues = quf.verify_bytes(crafted)
        ok = any(kv in i for i in issues) if val is not None else True
        check("verify flags %s=%r" % (kv, val), ok, issues)
        try:
            quf.decode_sections(quf.read(crafted))
            dec_ok = True
        except quf.QufError:
            dec_ok = True
        except Exception as ex:
            dec_ok = False
        check("decode guards %s=%r" % (kv, val), dec_ok)
    # hex TB format length cap
    try:
        quf.to_hexfile(b"\x00" * 0x10000)
        check("to_hexfile >64KiB rejected", False)
    except quf.QufError:
        check("to_hexfile >64KiB rejected", True)


def t_digest():
    print("== content integrity (payload corruption was invisible) ==")
    clean = quf.build(quf.add_digest(GOOD_DOC))
    check("digest file verifies clean", quf.verify_bytes(clean) == [])
    parsed = quf.read(clean)
    off = [t for t in parsed["table"] if t[0] == "dials"][0][2]
    b = bytearray(clean)
    b[off + 5] ^= 0x40
    issues = quf.verify_bytes(bytes(b))
    check("digest catches payload bit flip",
          any("sha256" in i for i in issues), issues)
    # digest survives rebuild (content-only hash, offsets excluded)
    check("digest survives rebuild",
          quf.rebuild(quf.read(clean)) is not None and
          quf.verify_bytes(quf.rebuild(quf.read(clean))) == [])


def t_tapfabric():
    print("== tapfabric bridge ==")
    # UTF-8 hostile log: the parser never chokes (was: whole-replay
    # UnicodeDecodeError from the file open)
    with tempfile.TemporaryDirectory() as d:
        log = os.path.join(d, "log.jsonl")
        with open(log, "wb") as f:
            f.write(b"pearl says: 'hello there'\n")
            f.write(b'\x82\x91 garbage bytes \xff\n')
            f.write(b'{"type":"agent_update","agent_id":"hank",'
                    b'"location":"bar_rail","action":"tell story"}\n')
        fab = tf.replay(log)
        check("non-UTF-8 log tolerated (never choke)",
              len(fab.order) >= 4 and fab.tick >= 2)
        # slot uniqueness after eviction (was: duplicate slot 7)
        c = tf.Cell(0, "x", "patron")
        for i in range(9):
            c.link(100 + i, 4096)
        slots = [e.slot for e in c.edges]
        check("edge slots unique after eviction", len(set(slots)) == len(slots),
              slots)
        # warm-boot fail-static family
        fab = tf.Fabric()
        fab.sit_down("pearl", "bar_rail")
        fab.sit_down("hank", "bridge_table")
        fab.speak(fab.patron("pearl"),
                  tf.Note(tf.KIND_STORY, 16384, "t"))
        fab.round()
        data = fab.export_quf("t")
        parsed = quf.read(data)
        dec = quf.decode_sections(parsed)
        h = dict(parsed["header"])

        def mk(names=None, edges=None, drop_dials=False, cc=None,
               edge_oob=False):
            hh = dict(parsed["header"])
            if names is not None:
                hh["tap.cellnames"] = names
            if cc is not None:
                hh["cell_count"] = cc
            doc = {"header": hh,
                   "dials": None if drop_dials else dec["dials"],
                   "edges": (edges if edges is not None else dec["edges"]),
                   "routing": dec.get("routing", []),
                   "ticksched": dec.get("ticksched")}
            return quf.build(doc)

        for name, buf in [
            ("short cellnames refused", mk(names="the-tap")),
            ("edge src out of range refused",
             mk(edges=dec["edges"] + [{"src": 99, "dst": 0, "mode": 0,
                                       "slot": 0, "base": 0, "wh": 0,
                                       "age": 0, "buckets": [0] * 8}])),
            ("missing dials refused", mk(drop_dials=True, cc=None)),
        ]:
            try:
                tf.Fabric.import_quf(fab, buf)
                check(name, False, "loaded")
            except quf.QufError:
                check(name, True)
            except Exception as ex:
                check(name, False, "%s: %s" % (type(ex).__name__, ex))
        # a QUF with NO edges section must warm-load (was: KeyError)
        noedge = quf.build(quf.add_digest(
            {"header": dict(parsed["header"], edge_count=0),
             "dials": dec["dials"], "edges": [],
             "routing": [], "ticksched": dec["ticksched"]}))
        # strip tap.* act/refr to len-matched defaults is fine; names kept
        try:
            w = tf.Fabric.import_quf(fab, noedge)
            check("edgeless QUF warm-loads", len(w.order) == len(fab.order))
        except Exception as ex:
            check("edgeless QUF warm-loads", False,
                  "%s: %s" % (type(ex).__name__, ex))
        # gap EMA round-trip
        fab2 = tf.Fabric.import_quf(fab, data)
        check("gap EMAs ride tap.gap",
              fab2._gap["ef"] == fab._gap["ef"] and
              fab2._gap["es"] == fab._gap["es"])


def t_dial_parity():
    print("== Python/RTL dial POR parity (was drifted: HL 48 vs 64) ==")
    rtl = open(os.path.join(_ROOT, "rtl", "q_dialfile.v")).read()
    def rtlval(v):
        if "'" in v:
            base, num = v.split("'h") if "'h" in v else v.split("'d")
            return int(num, 16) if "'h" in v else int(num, 10)
        return int(v, 10)

    table = {m[0]: rtlval(m[1]) for m in
             re.findall(r"dial\[D_(\w+)\]\s*<=\s*([0-9A-Fa-fx'hd]+);",
                        rtl)}
    names = ["ETA_F", "ETA_S", "KF", "KS", "KA", "THRESH", "REFR",
             "COSMIN", "P0E", "MODE", "HL", "KLE", "FLOOR", "FTRACE",
             "RQ", "RQL"]
    for i, nm in enumerate(names):
        want = int(table[nm])
        check("dial %2d (%s) == RTL POR %d" % (i, nm, want),
              tf.DIAL_DEFAULTS[i] == want,
              "python %r" % (tf.DIAL_DEFAULTS[i],))


def t_scale_tsv():
    print("== rebuild_scale_tsv cwd independence (was: silent empty) ==")
    r = subprocess.run([PY, os.path.join(_ROOT, "synth",
                                         "rebuild_scale_tsv.py")],
                       capture_output=True, text=True, cwd="/")
    lines = [l for l in r.stdout.strip().splitlines() if l.strip()]
    check("runs from / with rows", r.returncode == 0 and len(lines) > 2,
          r.stdout[:80] + r.stderr[:80])


def t_record_night():
    print("== record_night clean errors ==")
    r = subprocess.run([PY, os.path.join(_ROOT, "tools", "openmic",
                                         "record_night.py"),
                        "--outdir", "/nonexistent/definitely"],
                       capture_output=True, text=True, cwd="/tmp")
    check("bad outdir: rc=1, no traceback",
          r.returncode == 1 and "Traceback" not in r.stderr,
          r.stderr[:80])


def main():
    t_cli_hygiene()
    t_quf_library()
    t_digest()
    t_tapfabric()
    t_dial_parity()
    t_scale_tsv()
    t_record_night()
    print()
    if FAILS:
        print("REGRESS FAIL: %d of %d checks failed" % (len(FAILS), N))
        for f in FAILS:
            print("  - %s" % f)
        return 1
    print("REGRESS PASS: %d checks, 0 failures" % N)
    return 0


if __name__ == "__main__":
    sys.exit(main())
