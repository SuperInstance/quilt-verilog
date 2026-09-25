#!/usr/bin/env python3
"""DEV ROUND 22 (pre-registration) -- regime-membership map + the 2pd=6
double-duty question (STUDENT nudge on round 21).

Two booked teeth, both pre-declared BEFORE any new number:

TOOTH 1 -- regime-membership table over (K, pd).  Round 21 carved three
regimes but left the (K, pd) map unstamped: is K=2 in the quarter-power
regime or the flat regime?  Sweep K in {2,4,8} x pd in {2,3,4,6} at
delta=12 (mid-grid), comp arm, plus K=2 delta in {8,16} at pd=3 for the
flatness probe.  Regime classifier (frozen):
  FLAT signature: |wall(delta=8) - wall(delta=16)| <= 1  (delta-insensitive)
  STRATIFIED signature: wall(pd=6) - wall(pd=3) >= 2 at matched (K, delta)
  QUARTER-POWER membership: wall(K, pd<=3, delta=12) within +-1 of F2(6)=4
    AND flatness probe fails.
Pre-declared expectation: K=2 joins the QUARTER-POWER regime -- mechanism
story: the r-law needs >=2 candidate streams for pulse interference to be
the binding constraint; K=1's single stream has none.  GATE M-K2: if K=2
tests FLAT (|w8-w16| <= 1), the interference-threshold story DIES and the
line sits at K >= 4 -- booked as falsification of the pre-declared
mechanism, membership table stamped regardless.

TOOTH 2 -- why is the comp domain edge exactly pd<=3?  STUDENT's
observation: at pd=3, 2*pd = 6 = the round-17 fan-out wall at default.
The number 6 would be doing double duty in two laws.  Probe: pd=4 cell
at K=8/delta=12 (2*4=8 != 6).  GATE M-PD4: comp regime extends to pd=4
iff wall(pd=4) within +-1 of wall(pd=3) at matched (K=8, delta=12).
  - If M-PD4 HOLDS: boundary pd* in (3,4], so 2pd* in (6,8] does NOT
    contain 6 -> the 2pd=6 coincidence is DEMOTED (6 is not doing double
    duty at the comp edge); ledger entry says so.
  - If M-PD4 FAILS: boundary is exactly pd=3, and 2pd = 6 = fan-out wall
    stands as an UNEXPLAINED structural coincidence -- flagged in the
    ledger for the K-handover sweep to attack (predict: at pd where
    2pd != wall, the edge moves).

Canaries (frozen): round-21 octave replay pd=3 calm r in {1,2,6} comp
walls 2/3/4 exact; mislabeled-arm CAUGHT is inherited from the harness
(run_sw_comp keyed calls; spot-check one cell admits-vs-sorts anchors).
Run: python3 -u r22_regimemap.py > r22-regimemap-output.txt
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o2_contention import run_sw_comp, discover_lag, SEEDS, TICKS

T0 = time.time()
NS = tuple(range(2, 14))
K_GRID = (2, 4, 8)
PD_GRID = (2, 3, 4, 6)
DELTA_MAIN = 12
DELTA_PROBE = (8, 16)          # K=2, pd=3 only
DRIFT = {"calm": 3, "stress": 6}
LATS_N = {2: (0, 12), 3: (0, 6, 12), 5: (0, 3, 6, 9, 12),
          8: (0, 2, 3, 5, 7, 8, 10, 12)}


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def comp_wins(delta, k, drift):
    wins = {}
    for n in NS:
        lats = lats_for(n)
        laghat = [discover_lag(L) for L in lats]
        raw = sort = 0.0
        for sd in SEEDS:
            p = dict(K=k, drift=drift, delta=delta, pulse_div=3)
            raw += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
            sort += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
        wins[n] = (sort - raw) / len(SEEDS)
    return wins


def wall_from(wins):
    return next((n for n in NS if wins.get(n) is not None and wins[n] >= 2.0), None)


def f2(r):
    return math.ceil(2 * r ** 0.25)


def main():
    print(f"== O2g regime map start {time.strftime('%H:%M:%S')} ==")
    print(f"K={K_GRID} pd={PD_GRID} delta={DELTA_MAIN} (probe K=2 pd=3 d{DELTA_PROBE})")

    # ---- canary: round-21 octave replays ----
    want = {1: 2, 2: 3, 6: 4}
    ok = True
    for r in want:
        w = wall_from(comp_wins(r * 8, 8, 3))
        ok = ok and w == want[r]
        print(f"replay pd=3 calm r={r}: wall={w} (want {want[r]})")
    print(f"canary: {'PASS' if ok else 'FAIL -> no verdict'}")
    if not ok:
        return

    # ---- main map ----
    wall = {}
    for k in K_GRID:
        for pd in PD_GRID:
            w = wall_from(comp_wins(DELTA_MAIN, k, DRIFT["calm"]))
            wall[(k, pd)] = w
            print(f"K={k} pd={pd} d=12: wall={w} F2(6)={f2(6)} [{time.time()-T0:4.0f}s]")
    flat = {}
    for d in DELTA_PROBE:
        flat[d] = wall_from(comp_wins(d, 2, DRIFT["calm"]))
        print(f"K=2 pd=3 d={d}: wall={flat[d]} [{time.time()-T0:4.0f}s]")

    # ---- tooth 1: K=2 membership ----
    print("\n-- M-K2: K=2 membership --")
    w8, w16 = flat[8], flat[16]
    is_flat = (w8 is not None and w16 is not None and abs(w8 - w16) <= 1)
    qp = wall[(2, 3)]
    near_f2 = qp is not None and abs(qp - f2(6)) <= 1
    print(f"K=2 pd=3 d=12 wall={qp} (F2(6)={f2(6)}, +-1: {near_f2}); "
          f"d8={w8} d16={w16} flat(|<=1|): {is_flat}")
    if is_flat:
        print("M-K2: K=2 -> FLAT regime -- pre-declared interference-threshold "
              "story FALSIFIED; line sits at K >= 4")
    elif near_f2:
        print("M-K2: K=2 -> QUARTER-POWER regime (as pre-declared); "
              "interference needs >=2 streams")
    else:
        print("M-K2: INDETERMINATE -- K=2 neither flat nor F2-close; "
              "third regime cell, map it")

    # ---- stratified signature per K ----
    print("\n-- stratified signature: wall(pd=6) - wall(pd=3) --")
    for k in K_GRID:
        a, b = wall[(k, 3)], wall[(k, 6)]
        d = (b - a) if (a is not None and b is not None) else None
        print(f"K={k}: pd3={a} pd6={b} gap={d} "
              f"{'STRATIFIED' if d is not None and d >= 2 else 'flat-ish/none'}")

    # ---- tooth 2: pd=4 probe ----
    print("\n-- M-PD4: the 2pd=6 double-duty question --")
    a, b = wall[(8, 3)], wall[(8, 4)]
    if a is None or b is None:
        print("M-PD4: INDETERMINATE (None wall)")
    else:
        holds = abs(b - a) <= 1
        print(f"K=8 d=12: pd3={a} pd4={b} -> regime {'EXTENDS' if holds else 'BREAKS'} at pd=4")
        if holds:
            print("2pd=6 coincidence DEMOTED: boundary pd* in (3,4], 2pd* in (6,8] "
                  "excludes 6 -- 6 is NOT doing double duty at the comp edge")
        else:
            print("Boundary EXACTLY pd=3: 2pd=6=round-17 fan-out wall stands as "
                  "UNEXPLAINED structural coincidence -- flagged for the K-handover "
                  "sweep (predict: edge moves where 2pd != wall)")

    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
