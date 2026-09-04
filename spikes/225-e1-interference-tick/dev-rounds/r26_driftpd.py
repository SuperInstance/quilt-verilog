#!/usr/bin/env python3
"""DEV ROUND 26 -- drift x pd seat-field law (product vs separable).

Pre-registration: dev-rounds/ROUND-26-driftpd-prereg.md (commit BEFORE runs).
Harness identical to r25_pdladder.py (same lats_for, same wall rule) with the
drift axis added. Integer-only; real runs.

Run: python3 -u r26_driftpd.py > r26-driftpd-output.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o2_contention import run_sw_comp, discover_lag, SEEDS, TICKS

T0 = time.time()
NS = tuple(range(2, 19))
PD_GRID = (2, 3, 4, 5, 6)
DRIFTS = (3, 6, 12)
K = 1
DELTA = 12
LATS_N = {2: (0, 12), 3: (0, 6, 12), 5: (0, 3, 6, 9, 12),
          8: (0, 2, 3, 5, 7, 8, 10, 12)}
ANCHORS_D6 = {2: 4, 3: 6, 4: 9, 5: 11, 6: 13}  # r25 replay targets


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def wins_for(drift, pd, swap=False):
    """Mean comp-arm win per N. swap=True: mislabeled-arm (sort<->raw) probe."""
    wins = {}
    for n in NS:
        lats = lats_for(n)
        laghat = [discover_lag(L) for L in lats]
        a = b = 0.0
        for sd in SEEDS:
            p = dict(K=K, drift=drift, delta=DELTA, pulse_div=pd)
            if swap:
                a += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
                b += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
            else:
                a += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
                b += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
        wins[n] = (b - a) / len(SEEDS)
    return wins


def wall_from(wins):
    return next((n for n in NS if wins.get(n) is not None and wins[n] >= 2.0), None)


def main():
    print(f"== O2i R26 drift-x-pd seat-field start {time.strftime('%H:%M:%S')} ==")
    print(f"K={K} drift={DRIFTS} pd={PD_GRID} delta={DELTA} N={NS}")

    # ---- C2: double-run byte-identity on one cell (drift=6, pd=3) ----
    w_a = wins_for(6, 3)
    w_b = wins_for(6, 3)
    ok_c2 = all(w_a[n] == w_b[n] for n in NS)
    print(f"canary C2 double-run drift=6 pd=3: "
          f"{'IDENTICAL' if ok_c2 else 'MISMATCH'}")
    print(f"  run1 wins: {[round(w_a[n], 6) for n in NS]}")
    print(f"  run2 wins: {[round(w_b[n], 6) for n in NS]}")

    # ---- C3: mislabeled-arm self-canary (swap arms on same cell) ----
    w_true = w_a
    w_swap = wins_for(6, 3, swap=True)
    wall_true = wall_from(w_true)
    wall_swap = wall_from(w_swap)
    caught = wall_swap != wall_true
    print(f"canary C3 mislabel probe (drift=6 pd=3): true wall={wall_true}, "
          f"swapped-arm wall={wall_swap} -> {'CAUGHT' if caught else 'NOT CAUGHT'}")

    # ---- main grid ----
    ladder = {}  # (drift, pd) -> wall
    for d in DRIFTS:
        for pd in PD_GRID:
            if d == 6 and pd == 3:
                wins = w_a  # reuse the C2 cell
            else:
                wins = wins_for(d, pd)
            ladder[(d, pd)] = wall_from(wins)
            print(f"drift={d:2d} pd={pd}: wall={ladder[(d, pd)]} "
                  f"2pd={2*pd} off={(ladder[(d, pd)] - 2*pd) if ladder[(d, pd)] else '-'} "
                  f"[{time.time()-T0:4.0f}s]")

    # ---- C1: drift=6 column vs r25 anchors ----
    ok_c1 = all(ladder[(6, pd)] == ANCHORS_D6[pd] for pd in PD_GRID)
    print(f"canary C1 drift=6 column vs r25 anchors {{4,6,9,11,13}}: "
          f"{'EXACT' if ok_c1 else 'FAIL'}")

    ok = ok_c1 and ok_c2 and caught
    print(f"canaries: {'PASS' if ok else 'FAIL -> no verdict'}")
    if not ok:
        return

    # ---- ladder table ----
    print("\n-- ladder table (drift x pd -> wall) --")
    print("drift\\pd  " + "  ".join(f"{pd:>3d}" for pd in PD_GRID))
    for d in DRIFTS:
        print(f"{d:8d} " + "  ".join(
            f"{str(ladder[(d, pd)]):>3s}" for pd in PD_GRID))

    # ---- decision rule (frozen, prereg order) ----
    print("\n-- decision --")
    blind = all(ladder[(3, pd)] == ladder[(6, pd)] == ladder[(12, pd)]
                for pd in PD_GRID)
    collisions = [((6, 2), (3, 4)), ((12, 2), (6, 4), (4, 6)), ((12, 3), (6, 6))]
    prod_pairs_ok = all(
        len({ladder[c] for c in grp}) == 1 for grp in collisions)
    cells_sorted = sorted(((2 * d * pd, ladder[(d, pd)]) for d in DRIFTS
                           for pd in PD_GRID if ladder[(d, pd)] is not None),
                          key=lambda x: x[0])
    monotone = all(cells_sorted[i][1] <= cells_sorted[i + 1][1]
                   for i in range(len(cells_sorted) - 1))
    offs6 = {ladder[(6, pd)] - ladder[(3, pd)] for pd in PD_GRID}
    offs12 = {ladder[(12, pd)] - ladder[(3, pd)] for pd in PD_GRID}
    separable = (len(offs6) == 1 and len(offs12) == 1
                 and (offs6 | offs12) != {0})

    if blind:
        print("VERDICT: DRIFT-BLIND -- r25 ladder holds verbatim at drift "
              "3/6/12; r24 drift-artifact extends to the full pd-ladder; "
              "product and nontrivial separable laws FALSIFIED")
    elif prod_pairs_ok and monotone:
        print("VERDICT: PRODUCT law -- walls collapse onto pd*drift on "
              "collision pairs and are monotone in pd*drift")
    elif separable:
        print(f"VERDICT: SEPARABLE law -- constant column offsets "
              f"(d6-d3={sorted(offs6)}, d12-d3={sorted(offs12)})")
    else:
        print("VERDICT: UNBOOKED/two-knob -- wall(pd,drift) is a genuine "
              "two-knob object; report measured field")

    print("\n-- STEP-LOC sub-probe (+1 step at pd 3->4 at every drift?) --")
    for d in DRIFTS:
        w3, w4 = ladder[(d, 3)], ladder[(d, 4)]
        yes = (w3 == 6 and w4 == 9)
        print(f"drift={d}: wall(pd=3)={w3} wall(pd=4)={w4} "
              f"-> step at 3->4: {'YES' if yes else 'NO/shifted/None'}")

    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
