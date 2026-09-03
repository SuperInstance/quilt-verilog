#!/usr/bin/env python3
"""SPIN 6, SPOKE 4: TOPOLOGY — PATTERN-GRAMMAR sweep proposed by SPIN-4.

SPIN-4 verdict: spread is first-order (knee ~15, the 2*DELTA=24 crossing),
pattern second-order but REAL (cohort 49.3% vs ladder 26.8% at spread=30,
K=1). SPIN-6 tests the cohort-majority law at the knee, where sensitivity
is maximal.

Fabric: exp_glm1.run_fabric (E1 contract: fdiv decay, 64-bit LCG, FIFO
oldest-first expiry, snapshot decay). Integer-only inside the loop.

HYPOTHESIS (cohort-majority law): at fixed spread=15 (the knee) and N=6,
true-residency is set by the size of the largest mutually-coherent cohort
relative to N. Grammar variants:
  ladder15        : [0,3,6,9,12,15]   graded staleness (spin4 baseline)
  k_cohort_k      : [0]*k + [15]*(6-k), k=1..5
                    k=5 = single laggard [0,0,0,0,0,15]
                    k=3 = binary 3v3 [0,0,0,15,15,15] (spin4 anchor)
                    k=1 = single outlier [0,15,15,15,15,15]
  bimodal         : [0,0,7,8,15,15]   two coherent blocs + bridge pair
Plus knee densification: ladder spread in {12,14,16,18,20,22,24} step 2,
to pin the critical spread vs the 2*DELTA=24 prediction within +/-2.

Self-canaries (mandatory):
  (a) replay spin4 ladder spread=15 N=6: expect true% ~71.5/60.0/70.7 for
      K=1/2/8 (5-seed means from spin4-output.txt);
  (b) spread=0 identity: every grammar variant degenerates to [0]*6 and
      must produce byte-identical results per K (catches name-map bugs).
"""
import sys
sys.path.insert(0, "inventors-derby")
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
N = 6


def ladder(s, n=N):
    return [round(i * s / (n - 1)) for i in range(n)]


def k_cohort(k, s):
    return [0] * k + [s] * (N - k)


def grammar(s=15):
    """Return ordered dict name -> latency multiset at spread s."""
    g = {"ladder": ladder(s)}
    for k in range(1, 6):
        g[f"kcoh{k}"] = k_cohort(k, s)
    g["bimodal"] = sorted([0, 0, 7, 8, 15, 15]) if s == 15 else None
    return {k: v for k, v in g.items() if v is not None}


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
    # ---- canary a: spin4 replay (ladder spread=15 N=6) ----
    print("== CANARY A: spin4 replay ladder s=15 N=6 (mean of 5 seeds) ==")
    print(row(["K", "true%", "spin4%", "events", "spin4ev"]))
    s4 = {1: (71.5, None), 2: (60.0, None), 8: (70.7, None)}
    ok_a = True
    for k in (1, 2, 8):
        res = [one("interference", ladder(15), k, sd) for sd in SEEDS]
        tp = mean([r["true_pm"] for r in res]) / 10
        match = abs(tp - s4[k][0]) <= 0.15
        ok_a &= match
        print(row([k, f"{tp:.1f}", s4[k][0],
                   f"{mean([r['events'] for r in res]):.0f}", "-"])
              + ("  OK" if match else "  DRIFT"))
    print("  spin4 replay PASS" if ok_a else "  spin4 replay FAIL")

    # ---- canary b: spread=0 identity across grammar variants ----
    print("== CANARY B: spread=0 identity across variants (seed 1) ==")
    base = one("interference", [0] * N, 1, SEEDS[0])
    ok_b = True
    for k in (1, 2, 8):
        ref = one("interference", [0] * N, k, SEEDS[0])
        for name in ("ladder", "kcoh1", "kcoh3", "kcoh5", "bimodal0"):
            lats = ([0] * N if name != "bimodal0"
                    else sorted([0, 0, 0, 0, 0, 0]))
            got = one("interference", lats, k, SEEDS[0])
            if got != ref:
                ok_b = False
                print(f"  MISMATCH {name} k={k}: {got} vs {ref}")
    print("  PASS: all degenerate variants byte-identical" if ok_b
          else "  FAIL")

    # ---- main grammar sweep: spread=15, N=6 ----
    print("\n== MAIN: grammar sweep at spread=15, N=6, interference ==")
    print(row(["grammar", "lats", "K", "s1", "s7", "s42", "s1999",
               "s2s60902", "mean%", "allW", "evMean", "debtMean", "canc"]))
    for name, lats in grammar(15).items():
        for k in (1, 2, 8):
            res = [one("interference", lats, k, sd) for sd in SEEDS]
            tp = [r["true_pm"] for r in res]
            print(row([name, str(lats), k] + tp +
                      [f"{mean(tp)/10:.1f}",
                       f"{mean([r['all_pm'] for r in res])/10:.1f}",
                       f"{mean([r['events'] for r in res]):.0f}",
                       f"{mean([r['debt'] for r in res]):.0f}",
                       f"{mean([r['cancels'] for r in res]):.0f}"]))

    # ---- knee densification: ladder spread 12..24 step 2 ----
    print("\n== KNEE: ladder spread 12-24 step 2, N=6, interference ==")
    print(row(["spread", "K", "s1", "s7", "s42", "s1999", "s2s60902",
               "mean%", "allW", "evMean", "debtMean"]))
    for s in (12, 14, 16, 18, 20, 22, 24):
        for k in (1, 2, 8):
            res = [one("interference", ladder(s), k, sd) for sd in SEEDS]
            tp = [r["true_pm"] for r in res]
            print(row([s, k] + tp +
                      [f"{mean(tp)/10:.1f}",
                       f"{mean([r['all_pm'] for r in res])/10:.1f}",
                       f"{mean([r['events'] for r in res]):.0f}",
                       f"{mean([r['debt'] for r in res]):.0f}"]))

    # ---- sequential reference across grammar (k=1 arm) ----
    print("\n== REFERENCE: sequential arm, mean of 5 seeds ==")
    print(row(["grammar", "spread", "true%", "allW", "events", "debt"]))
    for name, lats in grammar(15).items():
        res = [one("sequential", lats, 1, sd) for sd in SEEDS]
        print(row([name, 15,
                   f"{mean([r['true_pm'] for r in res])/10:.1f}",
                   f"{mean([r['all_pm'] for r in res])/10:.1f}",
                   f"{mean([r['events'] for r in res]):.0f}",
                   f"{mean([r['debt'] for r in res]):.0f}"]))


if __name__ == "__main__":
    main()
