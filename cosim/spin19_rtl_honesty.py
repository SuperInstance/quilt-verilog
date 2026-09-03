#!/usr/bin/env python3
"""SPIN 19 -- RTL-HONESTY: does real silicon tooling (verilator RTL of the
wheel's pulse-dial fabric) co-sign the Python model, bit-exact?

Reference: spin16.run_fabric_gate / spin11.run_fabric_mc (committed,
canary-proven). RTL: rtl/q_wall_gate.v, one cycle per fabric tick,
integer-only. Comparison is FULL-DICT: every counter (events, mass,
cancels, chatter, settles, gopen, gcomp) plus the complete resid, cflags
and emissions traces, via canonical sha256 of both sides. Any single
divergent tick = MISMATCH, reported with the first divergent tick.

Panel (SPIN-16, pd=3, delta=12, K=1, drift=6, 4800 ticks, EV=12):
  kcoh5  gate@1.1 vs off/mc=0/mc=1 anchors  (byte-frozen claim)
  ladder gate@1.1
  step5  gate@1.1 vs off/mc=1               (rescue >= 9.0 claim)
  zero7  gate@1.1                            (diverged probe: guard bail)

Verdict rule (pre-registered in the task brief): RTL CO-SIGNS iff
  (a) every config/seed full-dict bit-exact vs Python,
  (b) step5 true12(RTL resid, EV=12) >= 9.0,
  (c) kcoh5 gate trace byte-identical to kcoh5 off (both sides).

Run with -u, no pipes:  python3 -u spin19_rtl_honesty.py
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WHEEL = os.path.join(ROOT, "spikes", "225-e1-interference-tick", "wheel")
sys.path.insert(0, WHEEL)
sys.path.insert(0, os.path.join(os.path.dirname(WHEEL), "inventors-derby"))
sys.path.insert(0, os.path.dirname(WHEEL))

from exp_glm1 import within_pm  # noqa: E402
from spin11_pulse_dial import run_fabric_mc  # noqa: E402
from spin16_pulse_dial2 import run_fabric_gate  # noqa: E402

TICKS = 4800
EV = 12
SEEDS = (1, 7, 42)
OUT = os.path.join(HERE, "out")

GRAMMARS = {
    "kcoh5":  [0, 0, 0, 0, 0, 30],
    "ladder": [0, 6, 12, 18, 24, 30],
    "step5":  [0, 5, 10, 15, 20, 25, 30],
    "zero7":  [0, 0, 0, 0, 0, 0, 0],
}


def ref(tag, lats, seed):
    """Python reference dict for one config/seed."""
    if tag.endswith("_gate"):
        return run_fabric_gate("interference", TICKS, lats, K=1, pd=3,
                               delta=12, drift=6, seed=seed, gate=1.1)
    if tag.endswith("_off"):
        return run_fabric_mc("interference", TICKS, lats, K=1, pd=3,
                             delta=12, drift=6, seed=seed, mc=0)
    if tag.endswith("_mc1"):
        return run_fabric_mc("interference", TICKS, lats, K=1, pd=3,
                             delta=12, drift=6, seed=seed, mc=1)
    raise ValueError(tag)


def canon(d):
    """Canonical form for hashing: scalars + the three traces."""
    return {
        "events": d["events"], "mass": d["mass"], "cancels": d["cancels"],
        "chatter": d["chatter"], "settles": d["settles"],
        "gopen": d.get("gopen", 0), "gcomp": d.get("gcomp", 0),
        "resid": list(d["resid"]), "cflags": list(d["cflags"]),
        "emissions": [list(e) for e in d["emissions"]],
    }


def hsh(c):
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def parse_rtl(path):
    """Parse T/E/F lines into the same canonical form."""
    resid, cflags, emissions = [], [], []
    fin = None
    with open(path) as f:
        for ln in f:
            p = ln.split()
            if not p:
                continue
            if p[0] == "T":
                resid.append(int(p[2]))
                cflags.append(int(p[3]))
            elif p[0] == "E":
                emissions.append([int(p[1]), int(p[2]), int(p[3]),
                                  int(p[4])])
            elif p[0] == "F":
                fin = [int(x) for x in p[1:8]]
    if fin is None:
        raise RuntimeError(f"{path}: no F line (sim did not finish)")
    return {"events": fin[0], "mass": fin[1], "cancels": fin[2],
            "chatter": fin[3], "settles": fin[4], "gopen": fin[5],
            "gcomp": fin[6], "resid": resid, "cflags": cflags,
            "emissions": emissions}


def first_diff(a, b):
    for k in ("events", "mass", "cancels", "chatter", "settles", "gopen",
              "gcomp"):
        if a[k] != b[k]:
            return f"counter {k}: py={a[k]} rtl={b[k]}"
    for k in ("resid", "cflags"):
        if len(a[k]) != len(b[k]):
            return f"trace {k} length py={len(a[k])} rtl={len(b[k])}"
        for i, (x, y) in enumerate(zip(a[k], b[k])):
            if x != y:
                return f"trace {k} first diff @tick {i}: py={x} rtl={y}"
    if len(a["emissions"]) != len(b["emissions"]):
        return (f"emissions count py={len(a['emissions'])} "
                f"rtl={len(b['emissions'])}")
    for i, (x, y) in enumerate(zip(a["emissions"], b["emissions"])):
        if x != y:
            return f"emission {i}: py={x} rtl={y}"
    return None


def main():
    tags = ["kcoh5_gate", "ladder_gate", "step5_gate", "zero7_gate",
            "kcoh5_off", "step5_off", "kcoh5_mc1", "step5_mc1"]
    ok = True
    print("== SPIN-19 RTL vs PYTHON: full-dict bit-exact cosim ==")
    for tag in tags:
        gram = tag.rsplit("_", 1)[0]
        lats = GRAMMARS[gram]
        for seed in SEEDS:
            path = os.path.join(OUT, f"{tag}_s{seed}.txt")
            r = ref(tag, lats, seed)
            try:
                v = parse_rtl(path)
            except Exception as e:  # noqa: BLE001
                print(f"  {tag:12s} s={seed:<6d} MISSING RTL: {e}")
                ok = False
                continue
            c_py, c_rtl = canon(r), canon(v)
            d = first_diff(c_py, c_rtl)
            if d is None:
                print(f"  {tag:12s} s={seed:<6d} MATCH  sha={hsh(c_py)[:16]}"
                      f"  true12={within_pm(v['resid'], EV)/10:5.1f}"
                      f"  maxresid={max(v['resid'])}")
            else:
                ok = False
                print(f"  {tag:12s} s={seed:<6d} MISMATCH: {d}")

    # byte-frozen claim: kcoh5 gate == kcoh5 off, BOTH sides
    print("== kcoh5 byte-frozen check (gate vs off) ==")
    frozen = True
    for side, getter in (("py", lambda t, s: canon(ref(t, GRAMMARS["kcoh5"],
                                                       s))),
                         ("rtl", lambda t, s: canon(parse_rtl(
                             os.path.join(OUT, f"{t}_s{s}.txt"))))):
        for seed in SEEDS:
            a = getter("kcoh5_gate", seed)
            b = getter("kcoh5_off", seed)
            same = a == b
            frozen = frozen and same
            print(f"  {side}: s={seed} gate==off {same}"
                  f"  sha_gate={hsh(a)[:12]} sha_off={hsh(b)[:12]}")

    # step5 rescue from RTL resid directly
    print("== step5 rescue (RTL resid, EV=12) ==")
    t12 = []
    for seed in SEEDS:
        v = parse_rtl(os.path.join(OUT, f"step5_gate_s{seed}.txt"))
        t12.append(within_pm(v["resid"], EV) / 10)
    mean12 = sum(t12) / len(t12)
    off12 = []
    for seed in SEEDS:
        v = parse_rtl(os.path.join(OUT, f"step5_off_s{seed}.txt"))
        off12.append(within_pm(v["resid"], EV) / 10)
    print(f"  step5 gate true12 = {mean12:.1f} (seeds {SEEDS}: "
          f"{[round(x,1) for x in t12]}), off = "
          f"{sum(off12)/len(off12):.1f}")

    rescue_ok = mean12 >= 9.0
    print()
    print(f"COSIM-BITEXACT: {'PASS' if ok else 'FAIL'}")
    print(f"STEP5-RESCUE (>=9.0): {'PASS' if rescue_ok else 'FAIL'} "
          f"[{mean12:.1f}]")
    print(f"KCOH5-BYTE-FROZEN: {'PASS' if frozen else 'FAIL'}")
    print(f"VERDICT: {'RTL CO-SIGNS' if (ok and rescue_ok and frozen) else 'RTL DOES NOT CO-SIGN'}")


if __name__ == "__main__":
    main()
