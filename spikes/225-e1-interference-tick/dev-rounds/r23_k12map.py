#!/usr/bin/env python3
"""DEV ROUND 23 (pre-registration) -- delta-resolved K=2 vs K=1 map.
Booked next rung of round 22 (3e9ab40): K=2 tested delta-FLAT at
d in {8,16}; this round asks whether K=2 stays flat at ALL delta or
crosses to growth like the K>=4 quarter-power world, and extends the
K=1 pd-stratified world beyond d<=16.

Design: comp arm, pd=3, K in {1,2}, delta in {8,16,24,32,48,64,96},
N 2..13, seeds (1,7,42,1999,20260902).  Round-19/21 anchors: K=8/pd=3
comp walls 2/3/4 at r=0.5/2/6 (delta=4/16/48); K=1 walls 6 (d8..16),
9 (pd=4), none<=12 (pd=6).

Pre-declared classifier (frozen BEFORE runs):
  FLAT: walls within +-1 of the K=2 anchor cell wall(d=8).
  GROWING: wall(d=96) >= wall(d=8) + 2 (monotone-ish rise; F2 at r=d/2
    predicts 3,3,3,4,4,4,5 -> +2 at d=96).
  GATE M-K2CROSS: GROWING -> K=2 belongs to the r-law world and the
    round-22 "line between K=1 and K=2" stands as a STREAM-COUNT
    threshold (single-stream world has no r-law); FLAT -> K=2 is a
    genuine third cell: flat at all probed delta, and the quarter-power
    regime boundary moves UP to K>=4 (round-21 naming restored).
  K=1 extension (booked alongside, no gate -- classification only):
    walls at d 24..96 show whether the 6-seat pd=3 plateau holds or
    grows; if wall(K=1,d=96) >= 8 the K=1 world also grows in delta
    and the "flat" label for K=1 was a d<=16 artifact.
Canaries (frozen): round-21 octave replay pd=3 K=8 r in {1,2,6} ->
walls 2/3/4 exact; K=1 d=8 -> wall 6 exact (round-21 seat).
Run: python3 -u r23_k12map.py > r23-k12map-output.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o2_contention import run_sw_comp, discover_lag, SEEDS, TICKS

T0 = time.time()
NS = tuple(range(2, 14))
K_GRID = (1, 2)
DELTAS = (8, 16, 24, 32, 48, 64, 96)
PD = 3
DRIFT = 3          # calm family throughout (round-19/21 anchors ran calm for these cells)
LATS_N = {2: (0, 12), 3: (0, 6, 12), 5: (0, 3, 6, 9, 12),
          8: (0, 2, 3, 5, 7, 8, 10, 12)}


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def comp_wins(k, delta):
    wins = {}
    for n in NS:
        lats = lats_for(n)
        laghat = [discover_lag(L) for L in lats]
        raw = sort = 0.0
        for sd in SEEDS:
            p = dict(K=k, drift=DRIFT, delta=delta, pulse_div=PD)
            raw += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
            sort += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
        wins[n] = (sort - raw) / len(SEEDS)
    return wins


def wall_from(wins):
    return next((n for n in NS if wins.get(n) is not None and wins[n] >= 2.0), None)


def main():
    print(f"== O2h K1/K2 delta map start {time.strftime('%H:%M:%S')} ==")
    print(f"K={K_GRID} pd={PD} drift={DRIFT} deltas={DELTAS} comp arm")

    # ---- canaries ----
    want = {1: 2, 2: 3, 6: 4}
    ok = True
    for r in want:
        w = wall_from(comp_wins(8, r * 8))
        ok = ok and w == want[r]
        print(f"replay K=8 r={r}: wall={w} (want {want[r]})")
    w1 = wall_from(comp_wins(1, 8))
    ok = ok and w1 == 6
    print(f"replay K=1 d=8: wall={w1} (want 6)")
    print(f"canaries: {'PASS' if ok else 'FAIL -> no verdict'}")
    if not ok:
        return

    wall = {}
    for k in K_GRID:
        for d in DELTAS:
            w = wall_from(comp_wins(k, d))
            wall[(k, d)] = w
            print(f"K={k} d={d:2d}: wall={w} [{time.time()-T0:4.0f}s]")

    print("\n-- M-K2CROSS --")
    base = wall[(2, 8)]
    ws = [wall[(2, d)] for d in DELTAS]
    growing = (ws[-1] is not None and base is not None and ws[-1] >= base + 2)
    print(f"K=2 walls: {dict(zip(DELTAS, ws))} base(d8)={base}")
    if growing:
        print("M-K2CROSS: GROWING -- K=2 joins the r-law world; line between "
              "K=1 and K=2 is a STREAM-COUNT threshold")
    else:
        flat = all(w is not None and base is not None and abs(w - base) <= 1 for w in ws)
        print(f"M-K2CROSS: {'FLAT at all probed delta -- quarter-power boundary moves UP to K>=4' if flat else 'INDETERMINATE (neither flat nor +2 rise) -- map stands, no label'}")

    print("\n-- K=1 extension (classification) --")
    w1s = [wall[(1, d)] for d in DELTAS]
    print(f"K=1 walls: {dict(zip(DELTAS, w1s))}")
    if w1s[-1] is not None and w1s[-1] >= 8:
        print("K=1 GROWS in delta (>=8 at d=96): 'flat' label was a d<=16 artifact")
    elif w1s[-1] is not None:
        print(f"K=1 plateau holds through d=96 (wall {w1s[-1]})")

    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
