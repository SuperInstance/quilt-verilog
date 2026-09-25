#!/usr/bin/env python3
"""DEV ROUND 25 (pre-registration) -- the K=1 pd-ladder vs the 2pd boundary
(IDULATOR nudge on rounds 21/24; runs BEFORE the named drift x pd sweep so
that sweep's grid covers wherever the pd=6 wall actually is).

Observation being tested: K=1 comp walls at drift 6, delta 12 read
pd=2 -> 4 (=2pd, r23/24 anchors), pd=3 -> 6 (=2pd, r23/24),
pd=4 -> 9 (2pd+1), pd=5 -> 11 (2pd+1), pd=6 -> None<=12 -- but 2pd=12
for pd=6 IS the N-grid ceiling of rounds 21/24.  A wall pinned at the
ceiling scores as None.  Round 16's "comp wall = echo-law safe boundary"
may be dead only in the middle of the ladder.

Design: K=1, drift=6, delta=12, pd in {2,3,4,5,6}, N in {2..18}
(extended past the old ceiling), comp arm (mag+C=1 vs admit-all,
run_sw_comp), seeds (1,7,42,1999,20260902), 4800 ticks, wall = first N
with mean win >= 2.0pp (identical to r21/r23/r24).

Canaries (all required, any fail -> no verdict):
- C1: pd=3 -> wall 6 EXACT (r23/24 seat).
- C2: pd=4 -> wall 9 EXACT (round-21 seat, pre-extended grid).
- C3: K=8 octave replay r in {1,2,6} -> walls 2/3/4 EXACT.

Decision rule (frozen BEFORE any new number):
- G-2PD: decisive cell is pd=6 on the extended grid.
  * wall(pd=6) == 12 -> book "K=1 comp wall = 2pd except pd in {4,5} +1";
    the middle-of-ladder sag (+1 at pd 4,5) becomes the named object:
    why does the ladder sit EXACTLY on the echo-law safe boundary at the
    ends but one seat above it in the middle?
  * wall(pd=6) > 12 or None <= 18 -> the 2pd coincidence dies cleanly;
    the {4,5} bumps are the whole story and the boundary law is dead
    for the whole K=1 ladder (not just the middle).
  * pd=2 re-check on the extended grid: expect 4 (r23/24 anchors were
    N<=13; confirm no late crossing to a lower-seat ambiguity) -- if
    wall(pd=2) != 4, flag grid inconsistency, book INDETERMINATE.
- No rescue clauses.  Whatever the cells read is what books.
Run: python3 -u r25_pdladder.py > r25-pdladder-output.txt
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
K = 1
DRIFT = 6
DELTA = 12
LATS_N = {2: (0, 12), 3: (0, 6, 12), 5: (0, 3, 6, 9, 12),
          8: (0, 2, 3, 5, 7, 8, 10, 12)}


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def comp_wins(pd):
    wins = {}
    for n in NS:
        lats = lats_for(n)
        laghat = [discover_lag(L) for L in lats]
        raw = sort = 0.0
        for sd in SEEDS:
            p = dict(K=K, drift=DRIFT, delta=DELTA, pulse_div=pd)
            raw += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
            sort += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
        wins[n] = (sort - raw) / len(SEEDS)
    return wins


def wall_from(wins):
    return next((n for n in NS if wins.get(n) is not None and wins[n] >= 2.0), None)


def main():
    print(f"== O2i K=1 pd-ladder extended-N start {time.strftime('%H:%M:%S')} ==")
    print(f"K=1 pd={PD_GRID} drift={DRIFT} delta={DELTA} N={NS}")

    # ---- canaries ----
    def wins_kd(k, pd, drift, delta):
        wins = {}
        for n in NS:
            lats = lats_for(n)
            laghat = [discover_lag(L) for L in lats]
            raw = sort = 0.0
            for sd in SEEDS:
                p = dict(K=k, drift=drift, delta=delta, pulse_div=pd)
                raw += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
                sort += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
            wins[n] = (sort - raw) / len(SEEDS)
        return wins

    def comp_wins(pd):
        return wins_kd(K, pd, DRIFT, DELTA)

    ok_c3 = True
    for r, want_w in ((1, 2), (2, 3), (6, 4)):
        w = wall_from(wins_kd(8, 3, 3, r * 8))
        ok_c3 = ok_c3 and w == want_w
        print(f"replay K=8 r={r}: wall={w} (want {want_w})")
    w3 = wall_from(comp_wins(3))
    ok_c1 = w3 == 6
    print(f"canary C1 pd=3: wall={w3} (want 6)")
    w4 = wall_from(comp_wins(4))
    ok_c2 = w4 == 9
    print(f"canary C2 pd=4: wall={w4} (want 9)")
    ok = ok_c1 and ok_c2 and ok_c3
    print(f"canaries: {'PASS' if ok else 'FAIL -> no verdict'}")
    if not ok:
        return

    wall = {3: w3, 4: w4}
    for pd in (2, 5, 6):
        wall[pd] = wall_from(comp_wins(pd))
        print(f"pd={pd}: wall={wall[pd]} 2pd={2*pd} [{time.time()-T0:4.0f}s]")

    print("\n-- G-2PD --")
    for pd in PD_GRID:
        print(f"pd={pd}: wall={wall[pd]}  2pd={2*pd}  off={wall[pd]-2*pd if wall[pd] else 'None'}")
    w6 = wall[6]
    w2 = wall[2]
    if w6 == 12:
        print("G-2PD: wall(pd=6)=12 EXACTLY -- book 'K=1 comp wall = 2pd except "
              "pd in {4,5} +1'; middle-ladder sag is the named object")
    elif w6 is None or w6 > 12:
        print("G-2PD: 2pd coincidence DIES cleanly for the K=1 ladder; "
              "the {4,5} bumps are the whole story")
    else:
        print(f"G-2PD: wall(pd=6)={w6} in (6,12) -- neither boundary law; "
              "book the measured ladder, boundary question open")
    if w2 != 4:
        print(f"GRID INCONSISTENCY: wall(pd=2)={w2} != 4 anchor -- INDETERMINATE flag")

    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
