#!/usr/bin/env python3
"""SPIN 4, SPOKE 1: METROLOGY — the SPREAD-LAW sweep proposed by SPIN-3.

SPIN-3 verdict: the F7 bundle-capacity wall is a topology artifact (ring
82.6% vs all-to-all 10.1% at N=6,K=8) — but in F7's staggered ladder,
N and staleness-spread (10*(N-1)) are confounded. This spin pins down the
critical spread parameter directly.

Fabric: exp_glm1.run_fabric (E1 contract: fdiv decay, 64-bit LCG, FIFO
oldest-first expiry, snapshot decay). Integer-only inside the loop.

HYPOTHESIS: interference-arm true-residency collapses at a critical
max-min twin-latency spread (predicted 15-20, where disagreement-slope x
spread crosses ~2*DELTA), largely independent of N once spread is
controlled and independent of the multiset *pattern*.

Design:
  - N=6 fixed, K in {1,2,8}, interference arm, 4800 ticks, stress params
    (delta=12, drift=6, pd=3), seeds {1,7,42,1999,20260902}.
  - Latency multisets with max-min spread s in {0,5,10,15,20,30}, TWO
    distinct patterns per spread (pattern-invariance is part of the
    hypothesis; only spread should matter):
      ladder : even steps  [0, s/5, 2s/5, ..., s] (rounded)
      cohort : binary split [0,0,0,s,s,s] (spread exactly s; for s=5 the
               split is [0,0,0,5,5,5] which still has max-min=5)
  - Shuffled-ladder control: spread=30 at N in {2,3} — tests
    N-independence directly against N=6 spread=30.
  - Sequential reference per spread (pattern collapsed: sequential is
    T1-priority, latency still matters via which sensor triggers first).

Self-canaries (mandatory):
  (a) spread=0 arms must be byte-identical across variants (all reduce
      to [0]*6; catches name-map / arm-label bugs);
  (b) replay spin3 configs exactly: ring N=6 K=8 (lat [0,10,0,10,0,10])
      mean true% 82.6 / events ~7589, all_to_all N=6 K=8 mean 10.1 /
      events ~19321 (5-seed means from spin3-output.txt).
"""
import sys
sys.path.insert(0, "inventors-derby")
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
N = 6


def ladder(s, n=N):
    return [round(i * s / (n - 1)) for i in range(n)]


def cohort(s, n=N):
    return [0, 0, 0, s, s, s][:n] if n >= 6 else \
           [0] * (n - n // 2) + [s] * (n // 2)


VARIANTS = {"ladder": ladder, "cohort": cohort}
SPREADS = (0, 5, 10, 15, 20, 30)


def one(mode, lats, k, seed):
    r = run_fabric(mode, 4800, lats, K=k, pd=3,
                   delta=DELTA, drift=6, seed=seed)
    return dict(true_pm=within_pm(r["resid"], DELTA),
                all_pm=1000 * r["settles"] // r["ticks"],
                events=r["events"], debt=r["mass"],
                cancels=r["cancels"])


def mean(vals):
    return sum(vals) / len(vals)  # display only


def row(cells):
    return " | ".join(f"{c:>8}" for c in cells)


def main():
    # ---- canary a: spread=0 byte-identical across variants ----
    print("== CANARY A: spread=0 identical across variants (seed 1) ==")
    ok = True
    for k in (1, 2, 8):
        base = one("interference", ladder(0), k, SEEDS[0])
        other = one("interference", cohort(0), k, SEEDS[0])
        if base != other:
            ok = False
            print(f"  MISMATCH k={k}: {base} vs {other}")
    print("  PASS: spread=0 byte-identical across variants x K" if ok
          else "  FAIL")

    # ---- canary b: spin3 replay ----
    print("== CANARY B: spin3 replay (N=6, K=8, mean of 5 seeds) ==")
    print(row(["config", "true%", "events", "s3true%", "s3ev"]))
    s3 = {"ring": (82.6, 7589), "all_to_all": (10.1, 19321)}
    lats3 = {"ring": [0, 10, 0, 10, 0, 10], "all_to_all": [0, 10, 20, 30, 40, 50]}
    ok2 = True
    for cfg in ("ring", "all_to_all"):
        res = [one("interference", lats3[cfg], 8, s) for s in SEEDS]
        tp = mean([r["true_pm"] for r in res]) / 10
        ev = mean([r["events"] for r in res])
        match = abs(tp - s3[cfg][0]) <= 0.15 and abs(ev - s3[cfg][1]) <= 40
        ok2 &= match
        print(row([cfg, f"{tp:.1f}", f"{ev:.0f}", s3[cfg][0], s3[cfg][1]])
              + ("  OK" if match else "  DRIFT"))
    print("  spin3 replay OK" if ok2 else "  spin3 replay DRIFTED")

    # ---- main spread sweep (N=6 fixed) ----
    print("\n== MAIN: N=6 interference, per-seed true-residency permille ==")
    print(row(["spread", "K", "variant", "s1", "s7", "s42", "s1999",
               "s2s60902", "mean%", "allW", "evMean", "debtMean", "canc"]))
    for s in SPREADS:
        for k in (1, 2, 8):
            for vname, vfn in VARIANTS.items():
                lats = vfn(s)
                res = [one("interference", lats, k, sd) for sd in SEEDS]
                tp = [r["true_pm"] for r in res]
                print(row([s, k, vname] + tp +
                          [f"{mean(tp)/10:.1f}",
                           f"{mean([r['all_pm'] for r in res])/10:.1f}",
                           f"{mean([r['events'] for r in res]):.0f}",
                           f"{mean([r['debt'] for r in res]):.0f}",
                           f"{mean([r['cancels'] for r in res]):.0f}"]))

    # ---- shuffled-ladder control: spread=30 at low N ----
    print("\n== CONTROL: spread=30 ladder at N in {2,3,6}, interference ==")
    print(row(["N", "K", "lats", "mean%", "allW", "evMean", "debtMean"]))
    ctrl = {2: ladder(30, 2), 3: ladder(30, 3), 6: ladder(30, 6)}
    for n, lats in ctrl.items():
        for k in (1, 2, 8):
            res = [one("interference", lats, k, sd) for sd in SEEDS]
            print(row([n, k, str(lats),
                       f"{mean([r['true_pm'] for r in res])/10:.1f}",
                       f"{mean([r['all_pm'] for r in res])/10:.1f}",
                       f"{mean([r['events'] for r in res]):.0f}",
                       f"{mean([r['debt'] for r in res]):.0f}"]))

    # ---- sequential reference per spread ----
    print("\n== REFERENCE: sequential arm, mean of 5 seeds (ladder) ==")
    print(row(["spread", "true%", "allW", "events", "debt"]))
    for s in SPREADS:
        res = [one("sequential", ladder(s), 1, sd) for sd in SEEDS]
        print(row([s,
                   f"{mean([r['true_pm'] for r in res])/10:.1f}",
                   f"{mean([r['all_pm'] for r in res])/10:.1f}",
                   f"{mean([r['events'] for r in res]):.0f}",
                   f"{mean([r['debt'] for r in res]):.0f}"]))


if __name__ == "__main__":
    main()
