#!/usr/bin/env python3
"""O2 follow-up (IDEATOR nudge, round 3): locate the fan-out phase transition.

Round 2 sampled N in {2,3,5,8}; the win switches on somewhere in 6..7.
Run ONLY N in {6,7}, full grid (regime x arm x C), same seeds/method.
Latency sets interpolate the round-2 spread 0..12:
  N=6: (0,2,5,7,10,12)   N=7: (0,2,4,6,8,10,12)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
from glm3_experiments import run_sw, KEYS
from o2_contention import discover_lag, run_sw_comp, REGIMES, KEY, SEEDS

LATS_N = {
    6: (0, 2, 5, 7, 10, 12),
    7: (0, 2, 4, 6, 8, 10, 12),
}

def cell(rows):
    n = len(rows)
    return (round(10 * sum(r["pct"] for r in rows) / n),
            round(sum(r["maxerr"] for r in rows) / n, 1),
            round(sum(r["events"] for r in rows) / n))

def main():
    print("== O2 boundary probe: N=6,7 (IDEATOR round 3) ==")
    laghat = {}
    for n, lats in LATS_N.items():
        hs = [discover_lag(L) for L in lats]
        laghat[n] = hs
        exact = all(h == L for h, L in zip(hs, lats))
        print(f"  N={n} lats={lats} -> discovered {hs} exact={exact}")
        assert exact, "lag blade must be exact or the comp arm is garbage"

    results = {}
    for reg, params in REGIMES.items():
        for n, lats in LATS_N.items():
            for arm, lag in (("raw", None), ("comp", laghat[n])):
                for C in range(1, n + 1):
                    rows = [run_sw_comp(s, key=KEY, C=C, lats=lats, laghat=lag, **params)
                            for s in SEEDS]
                    results[(reg, n, arm, C)] = cell(rows)
                rows = [run_sw_comp(s, key=None, C=n, lats=lats, laghat=lag, **params)
                        for s in SEEDS]
                results[(reg, n, arm, "all")] = cell(rows)

    print(f"\n{'regime':7s} {'N':>2s} {'arm':5s}  admit-all %w/maxE/ev   | C=1..N (%w|maxE)")
    for reg in REGIMES:
        for n in LATS_N:
            for arm in ("raw", "comp"):
                aa = results[(reg, n, arm, "all")]
                cs = "  ".join(
                    f"C{C}={results[(reg, n, arm, C)][0]/10:.1f}|{results[(reg, n, arm, C)][1]}"
                    for C in range(1, n + 1))
                print(f"{reg:7s} {n:2d} {arm:5s}  {aa[0]/10:5.1f} {aa[1]:5.1f} {aa[2]:6d}    {cs}")

    print("\n== DECISION TABLE (delta pp) ==")
    for reg in REGIMES:
        for arm in ("raw", "comp"):
            for n in LATS_N:
                aa = results[(reg, n, arm, "all")][0]
                c1 = results[(reg, n, arm, 1)][0]
                print(f"  {reg:7s} N={n} {arm:5s}  admit-all {aa/10:.1f}%w  magC1 {c1/10:.1f}%w"
                      f"  delta {(c1-aa)/10:+.1f}pp")

if __name__ == "__main__":
    main()
