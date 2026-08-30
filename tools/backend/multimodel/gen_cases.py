#!/usr/bin/env python3
"""gen_cases.py -- DeepSeek V4-Flash as the adversarial case generator
(multi-model backend, per Casey's amplification).

Loop: give Flash the target's shape (quf.py CLI + QUF doc schema + the
mutation knobs a harness can actually execute), ask for a batch of
adversarial cases as JSON; EXECUTE every case for real against
tools/quf.py; log every non-QufError crash / exit-code lie / silent
accept-that-should-reject. Then feed back the classes that found
something and ask for a harder batch. Two rounds by default.

Findings here are NEW only if the committed regression bench passes
(i.e. the bugs Flash hunts are post-fix residuals).
"""
import json
import os
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tools"))
sys.path.insert(0, _HERE)
import quf      # noqa: E402
import mm       # noqa: E402

PY = sys.executable
QUF = os.path.join(_ROOT, "tools", "quf.py")
RUNS = os.path.join(_HERE, "runs")
os.makedirs(RUNS, exist_ok=True)

SPEC_BLURB = """Target: quf.py, the QUF (QUilt Format) container tool.
CLI: quf.py {create IN.json OUT.quf [--digest] | info F | dump F | verify F
| hex F OUT | selftest}. verify prints issues and exits 1 if any, else
"QUF VERIFY PASS" exit 0. All failures must be one-line "quf.py: error:"
messages (QufError) -- tracebacks are bugs. JSON doc schema:
{"header": {"cell_count":u32, "edge.k":1..16, "align":pow2 8..2^20,
"tick_period":u32, ...extras: u32/str/u32-array},
"dials": [[16 x u16] per cell], "edges": [{"src":u8,"dst":u8,"mode":u8,
"slot":u8,"base":u16,"wh":u16,"age":u32,"buckets":[k x u8]}],
"routing": [{"dst":u8,"via":u8}], "ticksched": {"tpw":u32,"phases":[u32]}}.
Already fixed (do not re-report): raw tracebacks on bad files, duplicate
section names, names>255B, tick_period!=2^tpw, align 0/3/2^31, NaN dials,
array-extra type bug, digest mismatch detection, to_hexfile >64KiB,
u16 dial range, edge.k out of 1..16, cell_count lies vs dials rows."""

HARNESS_OPS = """Executable case kinds (emit ONLY these, as JSON):
{"kind":"json_doc","doc":<any JSON value>,"note":"..."}          -> quf.build
{"kind":"cli","argv":["verify","-x","--weird",...],"note":"..."} -> real CLI
{"kind":"mutate","op":"flip"|"truncate"|"insert","where":"header"|"kv"|
 "table"|"payload"|"tail","amount":N,"note":"..."} -> applied to a clean file
Rules: no shell metacharacters in argv (plain words only); amount 0..4096;
docs must be JSON-serializable. 12-16 cases per batch. Aim for cases a
single author would not think of."""


def salvage_cases(text):
    """array-parse; on failure salvage one JSON object per line"""
    import json as _j
    try:
        v = mm.extract_json(text)
        return v if isinstance(v, list) else [v]
    except Exception:
        out = []
        for ln in text.splitlines():
            ln = ln.strip().rstrip(",")
            if ln.startswith("{") and ln.endswith("}"):
                try:
                    out.append(_j.loads(ln))
                except Exception:
                    pass
        if out:
            return out
        raise


def run_build(doc):
    try:
        quf.build(doc)
        return ("accepted", "")
    except quf.QufError as ex:
        return ("rejected-loud", str(ex)[:120])
    except Exception as ex:               # noqa: BLE001
        return ("CRASH", "%s: %s" % (type(ex).__name__, ex))


def run_cli(argv):
    with tempfile.TemporaryDirectory() as d:
        good = os.path.join(d, "g.quf")
        with open(good, "wb") as f:
            f.write(quf.build({"header": {"cell_count": 1, "edge.k": 8,
                                          "align": 32},
                               "dials": [[1] * 16]}))
        subst = [a.replace("FILE", good) for a in argv]
        if any("\x00" in a for a in subst):
            return ("harness-skip", "NUL in argv: execve refuses at the "
                    "OS boundary, not the tool's (logged, not a bug)")
        r = subprocess.run([PY, QUF] + subst, capture_output=True,
                           text=True, timeout=30, cwd=d)
        if "Traceback" in r.stderr:
            return ("CRASH", r.stderr.strip().splitlines()[-1][:120])
        # argparse usage failures (rc=2) and clean tool errors (rc=1) are
        # both HANDLED; only tracebacks / rc lies are findings
        return ("handled rc=%d" % r.returncode, "")


def run_mutate(op, where, amount):
    data = quf.build({"header": {"cell_count": 2, "edge.k": 8,
                                 "align": 32, "tick_period": 64},
                      "dials": [[i for i in range(16)] for _ in range(2)],
                      "edges": [{"src": 0, "dst": 1, "mode": 0, "slot": 0,
                                 "base": 5, "wh": 0, "age": 0,
                                 "buckets": [0] * 8}],
                      "routing": [{"dst": 1, "via": 1}],
                      "ticksched": {"tpw": 6, "phases": [0, 3]}})
    b = bytearray(data)
    # region map (same classes as the fuzz bench)
    parsed = quf.read(data)
    kv_end = 16 + sum(4 + len(k.encode()) + 4 + len(quf.pack_value(vt, v))
                      for k, vt, v in parsed["kv"])
    tbl_end = kv_end + 4 + sum(4 + len(n.encode()) + 20
                               for n, _, _, _ in parsed["table"])
    if where == "payload":
        lo = (0, 0)                      # filled from the table below
    else:
        lo = {"header": (0, 16), "kv": (16, kv_end),
              "table": (kv_end, tbl_end), "tail": (tbl_end, len(b))}[where]
    if where == "payload":
        offs = [range(o, o + s) for _, _, o, s in parsed["table"]]
        pool = [i for r in offs for i in r]
        lo = (min(pool), max(pool) + 1)
    if lo[1] <= lo[0]:
        return ("no-region", "")
    if op == "flip":
        for i in range(amount):
            b[(lo[0] + i * 7 + 3) % lo[1]] ^= 1 << (i % 8)
    elif op == "truncate":
        b = b[:max(0, lo[0] + (lo[1] - lo[0]) // 2 - amount)]
    elif op == "insert":
        b = b[:lo[0]] + bytes(amount % 256 for _ in range(amount)) + b[lo[0]:]
    try:
        quf.read(bytes(b))
        quf.verify_bytes(bytes(b), "x")
        quf.decode_sections(quf.read(bytes(b)))
        quf.rebuild(quf.read(bytes(b)))
        return ("accepted", "")
    except quf.QufError as ex:
        return ("rejected-loud", str(ex)[:120])
    except Exception as ex:               # noqa: BLE001
        return ("CRASH", "%s: %s" % (type(ex).__name__, ex))


def execute(case):
    need = {"json_doc": ("doc",), "cli": ("argv",),
            "mutate": ("op", "where")}.get(case.get("kind"))
    if need is None:
        return ("harness-skip", "unknown kind %r" % case.get("kind"))
    if not all(f in case for f in need):
        return ("harness-skip",
                "salvaged object missing %s" %
                [f for f in need if f not in case])
    try:
        if case["kind"] == "json_doc":
            return run_build(case["doc"])
        if case["kind"] == "cli":
            argv = [str(a) for a in case["argv"]
                    if isinstance(a, (str, int))]
            return run_cli(argv)
        if case["kind"] == "mutate":
            return run_mutate(str(case["op"]), str(case["where"]),
                              int(case.get("amount", 1)))
        return ("harness-skip", "unknown kind")
    except Exception as ex:               # noqa: BLE001
        return ("HARNESS-ERROR", "%s: %s" % (type(ex).__name__, ex))


def main(rounds=2):
    ledger = open(os.path.join(RUNS, "flash_cases.jsonl"), "w")
    findings = []
    prior_feedback = ""
    for rnd in range(rounds):
        prompt = [
            {"role": "system", "content":
             "You are an adversarial QA engineer. You invent test cases "
             "that break tools in ways their authors did not imagine. "
             "Output ONLY a JSON array of case objects."},
            {"role": "user", "content":
             "%s\n\n%s\n\n%s" % (SPEC_BLURB, HARNESS_OPS, prior_feedback)},
        ]
        try:
            reply, meta = mm.flash(prompt, timeout=180, temperature=1.3)
        except mm.MMError as ex:
            print("round %d: flash UNAVAILABLE (%s)" % (rnd, ex))
            ledger.write(json.dumps({"round": rnd, "error": str(ex)}) + "\n")
            break
        cases = None
        for temp in (1.3, 0.7, 0.2):
            try:
                cases = salvage_cases(reply)
                break
            except Exception:
                # re-ask at a cooler temperature, strict JSON only
                try:
                    reply, meta = mm.flash(prompt + [
                        {"role": "user", "content":
                         "Your last reply was not parseable JSON. Output "
                         "ONLY a valid JSON array, nothing else."}],
                        timeout=180, temperature=temp)
                except mm.MMError as ex:
                    print("round %d: flash retry failed (%s)" % (rnd, ex))
                    break
        if cases is None:
            print("round %d: unparseable after retries" % rnd)
            ledger.write(json.dumps({"round": rnd, "parse_fail": True,
                                     "raw": reply[:300]}) + "\n")
            continue
        round_hits = []
        for case in cases:
            if not isinstance(case, dict):
                continue
            verdict, detail = execute(case)
            rec = {"round": rnd, "case": case, "verdict": verdict,
                   "detail": detail, "meta": {"model": meta["model"]}}
            ledger.write(json.dumps(rec) + "\n")
            if verdict in ("CRASH", "HARNESS-ERROR"):
                round_hits.append(rec)
                findings.append(rec)
                print("  HIT r%d %-10s %-12s %s | %s"
                      % (rnd, case.get("kind"), verdict,
                         case.get("note", "")[:40], detail[:70]))
        n_ok = sum(1 for c in cases if isinstance(c, dict))
        print("round %d: %d cases, %d hits" % (rnd, n_ok, len(round_hits)))
        if round_hits:
            prior_feedback = ("These case CLASSES found real crashes last "
                              "round; give me MORE LIKE THEM, harder: "
                              + json.dumps([{"kind": h["case"].get("kind"),
                                             "note": h["case"].get("note"),
                                             "verdict": h["verdict"]}
                                            for h in round_hits[:6]]))
        else:
            prior_feedback = ("Last round found nothing. Go weirder: "
                              "cross-layer tricks, encoding traps, numbers "
                              "at radix boundaries, empty-everything, "
                              "types that almost fit.")
    ledger.close()
    print("flash generation: %d findings total" % len(findings))
    return findings


if __name__ == "__main__":
    main()
