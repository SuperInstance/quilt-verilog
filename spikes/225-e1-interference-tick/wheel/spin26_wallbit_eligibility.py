#!/usr/bin/env python3
"""SPIN 26 — WALL-BIT-ONLY ELIGIBILITY SWEEP (pre-reg in SPIN-26-wallbit-eligibility.md).

t100 in {100,105,110,120,133}: admission set {nf=7} only (nf=6 rejected).
(1) sha-distinctness FIRST, run panel only on distinct classes;
(2) panel = anchors kcoh5@15, ladder30, zero7, step5K1/K2; pd=3, K=1, seeds {1,7,42};
(3) byte-compare gate==never per healthy anchor (per-seed shas).
Reuses spin25 machinery verbatim (spin16 run_fabric_gate). Integer-only in-loop.
"""
import hashlib
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
sys.path.insert(0, HERE)
from exp_glm1 import within_pm, LCG  # noqa: E402
from spin11_pulse_dial import ladder, ladder_step  # noqa: E402
from spin16_pulse_dial2 import run_fabric_gate  # noqa: E402

TICKS = 4800
EV = 12
S3 = (1, 7, 42)
S5 = (1, 7, 42, 1999, 20260902)
T0 = time.time()

PANEL = (
    ("kcoh5@15", [0, 0, 0, 0, 0, 15], 1),
    ("ladder30", ladder(30), 1),
    ("zero7", [0] * 7, 1),
    ("step5K1", ladder_step(30, 5), 1),
    ("step5K2", ladder_step(30, 5), 2),
)
HEALTHY = ("kcoh5@15", "ladder30", "zero7")
RESCUE = ("step5K1", "step5K2")
T_SWEEP = (100, 105, 110, 120, 133)


def sha(r):
    h = hashlib.sha256()
    for k in ("events", "mass", "cancels", "chatter", "settles",
              "resid", "cflags", "emissions", "gopen", "gcomp"):
        h.update(repr((k, r.get(k))).encode())
    return h.hexdigest()[:16]


def pct(r):
    return within_pm(r["resid"], EV) / 10.0


def run(lats, k, gate, s):
    return run_fabric_gate("interference", TICKS, lats, K=k, pd=3,
                           delta=12, drift=6, seed=s, gate=gate)


def cell(lats, k, gate):
    v = 0.0
    for s in S3:
        v += pct(run(lats, k, gate, s))
    return v / len(S3)


def mean(v):
    return sum(v) / len(v)


def canaries():
    ok = True
    print("== CANARY 1: spread=0 byte-identity, kcoh5@0 gate modes ==")
    hs = {}
    for mode in ("never", 1.1, "never2"):
        gate = "never" if mode == "never2" else mode
        hs[mode] = [sha(run([0] * 6, 1, gate, s)) for s in (1, 42)]
    g = hs["never"] == hs[1.1] == hs["never2"]
    print(f"  never==theta1.1==dual-run shas: {'PASS' if g else 'FAIL'}")
    ok &= g

    print("\n== CANARY 2: ladder@15 K=1 = 71.5 exact (5-seed, R0) ==")
    v = mean([pct(run(ladder(15), 1, "never", s)) for s in S5])
    g = abs(v - 71.5) <= 0.2
    print(f"  got {v:.1f}  want 71.5  {'PASS' if g else 'FAIL'}")
    ok &= g

    print("\n== CANARY 3: SPIN-25 toggle table reproduces (t100=99 IN vs 100 OUT) ==")
    latsmap = {n: (l, k) for n, l, k in PANEL}
    for n in ("kcoh5@15", "ladder30"):
        l, k = latsmap[n]
        vin = cell(l, k, 0.99)
        vout = cell(l, k, 1.0)
        print(f"  {n:9s} IN(99)={vin:5.1f} OUT(100)={vout:5.1f} "
              f"delta={vin - vout:+5.1f}pp")
        if n == "kcoh5@15":
            ok &= (vin - vout) >= 5.0
        else:
            ok &= (vin - vout) <= -1.0  # booked -1.4 level cost
    print(f"  (rule: kcoh5 >= +5, ladder30 <= -1)  "
          f"{'PASS' if ok else 'see above'}")
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


def sweep():
    print("\n== STEP 1: sha distinctness of t100 in {100,105,110,120,133} ==")
    latsmap = {n: (l, k) for n, l, k in PANEL}
    sig = {}
    for t in T_SWEEP:
        s_list = []
        for n, (l, k) in latsmap.items():
            for s in S3:
                s_list.append(sha(run(l, k, t / 100, s)))
        sig[t] = tuple(s_list)
    classes = {}
    for t in T_SWEEP:
        classes.setdefault(sig[t], []).append(t)
    print(f"  distinct behavioral classes: {len(classes)}")
    for i, (sg, ts) in enumerate(classes.items()):
        print(f"    class {i}: t100={ts}  sha-prefix={sg[0]}")

    print("\n== STEP 2/3: panel + gate==never byte-compare, per distinct class ==")
    verdicts = []
    for i, (sg, ts) in enumerate(classes.items()):
        t = ts[0]
        vals = {n: cell(l, k, t / 100) for n, (l, k) in latsmap.items()}
        never = {n: cell(l, k, "never") for n, (l, k) in latsmap.items()}
        rescue = mean([vals[n] - never[n] for n in RESCUE])
        ident = {}
        for n in HEALTHY:
            l, k = latsmap[n]
            pairs = [(s, sha(run(l, k, t / 100, s)) == sha(run(l, k, "never", s)))
                     for s in S3]
            ident[n] = all(p for _, p in pairs)
        row = " ".join(f"{n}={vals[n]:5.1f}(nv {never[n]:5.1f})"
                       for n in vals)
        print(f"    class {i} (rep t100={t}, members {ts}): rescue={rescue:+5.1f}pp")
        print(f"      {row}")
        for n in HEALTHY:
            print(f"      byte-identical to never @ {n}: "
                  f"{'YES' if ident[n] else 'NO'}")
        eligible = all(ident.values()) and rescue >= 33.0
        verdicts.append((t, ts, eligible, rescue, ident))
        print(f"      ELIGIBLE-EMBEDDED: {'YES' if eligible else 'NO'} "
              f"(rule: healthy byte-identity AND rescue >= +33pp)")
    return classes, verdicts


def main():
    print("SPIN-26 WALL-BIT-ONLY ELIGIBILITY SWEEP —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"panel seeds {S3}; ticks {TICKS}; pd=3; delta/drift 12/6; EV=12")
    if not canaries():
        sys.exit(1)
    classes, verdicts = sweep()
    print("\n== VERDICTS (exact, per t100) ==")
    free = False
    for t, ts, elig, rescue, ident in verdicts:
        print(f"  t100 members {ts}: eligible={'Y' if elig else 'N'} "
              f"rescue={rescue:+.1f}pp healthy-byte-ident="
              f"{'ALL' if all(ident.values()) else {k for k, v in ident.items() if not v}}")
        free |= elig
    if free:
        print('  VERDICT: "free lunch lives at the wall bit" -> BEACONS.md one-liner')
    else:
        print("  VERDICT: wall bit NOT eligible-embedded — booked")
    print(f"DONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
