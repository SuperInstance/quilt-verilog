#!/usr/bin/env python3
"""SPIN 8 — SPOKE: COHERENCE-RADIUS (mechanize the fresh-cohort law).

Dispatched by SPIN-5-topology's proposal. Two blades + one prediction gate.
Fabric: inventors-derby/exp_glm1.run_fabric (E1 contract pinned: fdiv decay,
64-bit LCG, FIFO oldest-first expiry, snapshot decay). Integer-only in-loop;
floats display/statistics only. Seeds {1,7,42,1999,20260902}, 4800 ticks,
stress drift=6 pd=3 unless noted.

=====================================================================
PRE-REGISTERED PREDICTIONS — written into this file BEFORE any run.
=====================================================================
P3 (brief-mandated): kcoh5 [0,0,0,0,0,45] at delta=12, spread=45, K=1:
    PREDICT 41.0%, acceptance band [34, 50].
    Basis: published kcoh5(=outlier) @15: 74.1, @30: 53.2 -> linear
    extrapolation 32.3, but the laggard's trigger duty cycle is already
    saturated at lag 30 (ramp error (8/5)*30=48 >> 12; at 45 it is 72,
    same >> 12), so marginal damage 30->45 is pulse-magnitude (~+50% on
    e//3), not new duty. Predict saturation ABOVE linear: 41.0 [34,50].

P1 (granularity): at spread 30, delta 12, steps {1,2,3,5,6,10,15,30}
    (N = 30/step+1): Law A (rho = 0.3*delta, from topology knee 18/5)
    predicts a sharp connectivity edge between step 3 (connected, good)
    and step 5 (fragmented, bad); steps {1,2,3} cluster high, {5..30}
    sit in the collapsed band. Law B (rho = delta/(8/5) = 7.5, slope
    law) predicts the edge between 6 and 10 instead. CONFOUND declared:
    N co-varies with step (31..2); step5(N=7) vs step6(N=6) partially
    deconfounds N vs granularity.

P2 (delta x grammar): fresh-vs-stale = kcoh5 - kcoh1 stays >= 0 at
    every delta in {6,9,12,15,18,24} (fixed eval window 12), compressing
    but NOT flipping (weakly held — a flip at delta=6 from synchronized
    fresh-bloc chatter is the live alternative). Ladder overtakes cohort
    near delta ~20 under Law A (rho(20) = 6 = ladder gap), already dead
    under Law B (predicts overtake at delta <= 12, contradicted by
    published 26.8 vs 49.3).

Canaries (mandatory, abort on fail):
  A: spread=0 byte-identity across all grammar codepaths (grouped by N).
  B: topology-lane replay kcoh5/kcoh1 @15 K{1,2,8} = 74.1/50.6/72.8 and
     47.3/34.4/38.3; ladder@15 = 71.5/60.0/70.7; pattern-grammar @30 K=1
     anchors ladder 26.8 / cohort 49.3 / kcoh5 53.2. Tolerance ±0.2pp.
"""
import sys
sys.path.insert(0, "inventors-derby")
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
EV = 12          # fixed eval window (trigger delta varies in EXP 2)
N6 = 6
STEPS = (1, 2, 3, 5, 6, 10, 15, 30)


def ladder_step(s, g):
    return list(range(0, s + 1, g))


def ladder(s, n=N6):
    return [round(i * s / (n - 1)) for i in range(n)]


def kcoh(k, s):
    return [0] * k + [s] * (N6 - k)


def one(mode, lats, seed, k=1, delta=DELTA):
    r = run_fabric(mode, 4800, lats, K=k, pd=3, delta=delta,
                   drift=6, seed=seed)
    return dict(true12=within_pm(r["resid"], EV),
                native=within_pm(r["resid"], delta),
                allw=1000 * r["settles"] // r["ticks"],
                events=r["events"], debt=r["mass"],
                cancels=r["cancels"], raw=r)


def mean(v):
    return sum(v) / len(v)


def row(cells):
    return " | ".join(f"{c:>9}" for c in cells)


def canaries():
    ok = True
    print("== CANARY A: spread=0 byte-identity across codepaths (seed 1, K=1) ==")
    fams = {}
    for g in STEPS:
        fams[f"step{g}"] = ladder_step(0, g)
    fams.update({"ladder0": ladder(0), "kcoh5_0": kcoh(5, 0),
                 "kcoh1_0": kcoh(1, 0), "cohort0": [0] * 3 + [0] * 3})
    groups = {}
    for name, lats in fams.items():
        assert all(x == 0 for x in lats), name
        groups.setdefault(len(lats), []).append(name)
    for n, names in sorted(groups.items()):
        ref = one("interference", fams[names[0]], SEEDS[0])["raw"]
        for nm in names[1:]:
            got = one("interference", fams[nm], SEEDS[0])["raw"]
            if got != ref:
                ok = False
                print(f"  MISMATCH N={n} {nm}")
    print(f"  {'PASS' if ok else 'FAIL'}: {sum(len(v) for v in groups.values())}"
          f" codepaths, {len(groups)} N-groups byte-identical")

    # constructor map sanity for the exact experiment configs
    assert ladder_step(30, 1) == list(range(0, 31))
    assert ladder_step(30, 5) == [0, 5, 10, 15, 20, 25, 30]
    assert ladder(30) == [0, 6, 12, 18, 24, 30]
    assert kcoh(5, 30) == [0, 0, 0, 0, 0, 30]
    assert kcoh(1, 30) == [0, 30, 30, 30, 30, 30]
    assert kcoh(5, 45) == [0, 0, 0, 0, 0, 45]
    print("  constructor map asserts: PASS")

    print("\n== CANARY B: topology/pattern replay (5-seed means, tol ±0.2pp) ==")
    targets = [  # (name, lats, K, published)
        ("kcoh5@15", kcoh(5, 15), 1, 74.1),
        ("kcoh5@15", kcoh(5, 15), 2, 50.6),
        ("kcoh5@15", kcoh(5, 15), 8, 72.8),
        ("kcoh1@15", kcoh(1, 15), 1, 47.3),
        ("kcoh1@15", kcoh(1, 15), 2, 34.4),
        ("kcoh1@15", kcoh(1, 15), 8, 38.3),
        ("ladder@15", ladder(15), 1, 71.5),
        ("ladder@15", ladder(15), 2, 60.0),
        ("ladder@15", ladder(15), 8, 70.7),
        ("ladder@30", ladder(30), 1, 26.8),
        ("cohort@30", [0, 0, 0, 30, 30, 30], 1, 49.3),
        ("kcoh5@30", kcoh(5, 30), 1, 53.2),
    ]
    for name, lats, k, pub in targets:
        tp = mean([one("interference", lats, s, k=k)["native"]
                   for s in SEEDS]) / 10
        m = abs(tp - pub) <= 0.2
        ok &= m
        print(f"  {name:<10} K={k}  got {tp:5.1f}  pub {pub:5.1f}"
              f"  {'OK' if m else 'DRIFT'}")
    print("  CANARIES:", "PASS" if ok else "FAIL")
    return ok


def exp1():
    print("\n== EXP 1: step-granularity at fixed spread 30, delta 12 ==")
    print(row(["step", "N", "lats"] + [f"s{s}" for s in SEEDS] +
              ["mean%", "K"]))
    out = {}
    for g in STEPS:
        lats = ladder_step(30, g)
        for k in (1, 2, 8):
            res = [one("interference", lats, s, k=k) for s in SEEDS]
            tp = [r["true12"] for r in res]
            out[(g, k)] = mean(tp) / 10
            print(row([g, len(lats), str(lats)[:17] + ".." if len(lats) > 6
                       else str(lats)] + tp + [f"{out[(g, k)]:.1f}", k]))
    print("\n  K=1 sequence (coarse->fine):",
          " ".join(f"{g}:{out[(g, 1)]:.1f}" for g in reversed(STEPS)))
    seq = [out[(g, 1)] for g in STEPS]            # fine -> coarse
    jumps = [(STEPS[i], STEPS[i + 1], seq[i] - seq[i + 1])
             for i in range(len(STEPS) - 1)]
    for g1, g2, j in jumps:
        print(f"  jump step{g1}->{g2}: {j:+.1f}pp")
    return out


def exp2():
    print("\n== EXP 2: delta x grammar at spread 30, K=1 "
          "(true% at FIXED eval window 12; native trueΔ for reference) ==")
    grammars = [("kcoh5", kcoh(5, 30)), ("kcoh1", kcoh(1, 30)),
                ("ladder", ladder(30)), ("cohort", [0, 0, 0, 30, 30, 30])]
    tab = {}
    print(row(["delta", "grammar"] + [f"s{s}" for s in SEEDS] +
              ["true12%", "native%", "evMean", "debtMean"]))
    for d in (6, 9, 12, 15, 18, 24):
        for name, lats in grammars:
            res = [one("interference", lats, s, delta=d) for s in SEEDS]
            t12 = [r["true12"] for r in res]
            nat = [r["native"] for r in res]
            tab[(d, name)] = dict(t12=mean(t12) / 10, nat=mean(nat) / 10)
            print(row([d, name] + t12 +
                      [f"{mean(t12)/10:.1f}", f"{mean(nat)/10:.1f}",
                       f"{mean([r['events'] for r in res]):.0f}",
                       f"{mean([r['debt'] for r in res]):.0f}"]))
    print("\n  fresh-vs-stale (kcoh5-kcoh1, true12) and ladder-cohort:")
    for d in (6, 9, 12, 15, 18, 24):
        fvs = tab[(d, "kcoh5")]["t12"] - tab[(d, "kcoh1")]["t12"]
        lc = tab[(d, "ladder")]["t12"] - tab[(d, "cohort")]["t12"]
        print(f"  delta={d:>2}: FVS {fvs:+6.1f}pp   ladder-cohort {lc:+6.1f}pp")
    # parity delta*: ladder overtakes cohort
    xs = [6, 9, 12, 15, 18, 24]
    diff = [tab[(d, "ladder")]["t12"] - tab[(d, "cohort")]["t12"] for d in xs]
    star = None
    for i in range(len(xs) - 1):
        if diff[i] < 0 <= diff[i + 1] or diff[i] >= 0 > diff[i + 1]:
            x0, x1, d0, d1 = xs[i], xs[i + 1], diff[i], diff[i + 1]
            star = x0 + (0 - d0) * (x1 - x0) / (d1 - d0)
            break
    print(f"  ladder/cohort parity delta* = {star}")
    if star:
        kappa = 6 / star
        print(f"  kappa = ladder_gap/delta* = {kappa:.3f}  "
              f"(Law A 0.30, Law B 0.625); implied knee coeff "
              f"c = 5*kappa/2 = {2.5 * kappa:.2f} vs topology 0.75")
    return tab


def exp3():
    print("\n== EXP 3: pre-registered prediction check — kcoh5 delta=12 "
          "spread=45 K=1 ==")
    print("  PREDICT (pre-registered): 41.0%, band [34, 50]")
    res = [one("interference", kcoh(5, 45), s) for s in SEEDS]
    tp = [r["true12"] for r in res]
    m = mean(tp) / 10
    print("  per-seed:", tp, f" mean {m:.1f}%")
    print(f"  linear-extrap reference was 32.3 (74.1@15, 53.2@30)")
    verdict = "PASS" if 34 <= m <= 50 else "FAIL"
    print(f"  prediction verdict: {verdict}")
    return m


def main():
    print("SPIN 8 — COHERENCE-RADIUS  (pre-registered predictions in "
          "spin8_coherence_radius.py docstring, written before any run)")
    if not canaries():
        print("CANARY FAIL — aborting")
        sys.exit(1)
    exp1()
    exp2()
    exp3()
    x = 2035015474
    x2 = (1103515245 * x + 12345) & 0x7FFFFFFF
    print(f"\nLCG bookkeeping (proposal-dispatched spin; ledger resumes LCG "
          f"selection next cycle): 2035015474 -> {x2} -> mod 10 = {x2 % 10}")


if __name__ == "__main__":
    main()
