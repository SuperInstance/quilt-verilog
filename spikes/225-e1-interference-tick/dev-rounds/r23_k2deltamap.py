#!/usr/bin/env python3
"""DEV ROUND 23 -- delta-resolved comp-wall map at K=2 vs K=1
(pre-registration: ROUND-23-k2-delta-map.md PART 1, committed first).

Question (round 22's named rung): is K=2 delta-flat at ALL delta, or does it
cross to the quarter-power F2 regime at delta >= 24?  At K=2, r = delta/2, so
F2(48/2=24)=4, F2(32/2=16)=4, F2(48)=... F2 values below are PRECOMPUTED
exactly with integer math where possible (F2 uses r**0.25 once, offline, in
this comment; runtime prints integers only):
  r=4 (d=8)->4   r=6 (d=12)->4  r=8 (d=16)->4  r=10 (d=20)->4
  r=12 (d=24)->4 r=16 (d=32)->5 r=24 (d=48)->6
So delta=48 is the first cell where F2 separates from flat by 2 seats.

Harness fix (declared in PART 1): r22's pd-grid hard-coded pulse_div=3; r23
passes pd through (as r21 did).  C2 anchor replay runs at pd=3 = what r22
measured.

Grid: K=2 x delta{8,12,16,20,24,32,48} x pd{2,3}, comp arm, calm family
(drift=3), N 2..13, 4800 ticks, 5 seeds.  K=1 controls at delta{8,16,32} x
pd{2,3}, drift=3 (continuity w/ round-21 SPIN-32 seating which used drift=6;
controls recorded, not gated).

Canaries (frozen in PART 1): C1 r21 octave replays 2/3/4 exact; C2 r22 K=2
d8/d16 = 4/4 exact; C3 byte-identity double run of the (K=2,pd=3,d=48) cell;
C4 mislabeled-arm CAUGHT at the round-2 anchor cell (68.0/69.6).

Verdict (pre-registered, frozen):
  CROSS      wall >= 6 at delta >= 24 in any pd cell
  FLAT-ALL   wall <= 4 through delta=48 in all pd cells
  AMBIGUOUS  otherwise -> honest map + next probe
Run: python3 -u r23_k2deltamap.py > r23-k2deltamap-output.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o2_contention import run_sw_comp, run_sw, discover_lag, SEEDS, TICKS

T0 = time.time()
NS = tuple(range(2, 14))
K2_DELTAS = (8, 12, 16, 20, 24, 32, 48)
K1_DELTAS = (8, 16, 32)
PDS = (2, 3)
DRIFT = 3                      # calm family, as rounds 21/22
F2_REF = {8: 4, 12: 4, 16: 4, 20: 4, 24: 4, 32: 5, 48: 6}   # F2(delta/2) at K=2, precomputed

LATS_N = {2: (0, 12), 3: (0, 6, 12), 5: (0, 3, 6, 9, 12),
          8: (0, 2, 3, 5, 7, 8, 10, 12)}


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def cell_dump(k, pd, delta, drift):
    """Deterministic per-cell dump (for the C3 byte-identity canary)."""
    lines = []
    for n in NS:
        lats = lats_for(n)
        laghat = [discover_lag(L) for L in lats]
        raw = sort = 0.0
        for sd in SEEDS:
            p = dict(K=k, drift=drift, delta=delta, pulse_div=pd)
            raw += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
            sort += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
        lines.append(f"N={n} win={(sort - raw) / len(SEEDS):.6f}")
    return "\n".join(lines)


def comp_wins(k, pd, delta, drift):
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


def wall_from(wins):
    return next((n for n in NS if wins.get(n) is not None and wins[n] >= 2.0), None)


def main():
    print(f"== R23 k2 delta-map start {time.strftime('%H:%M:%S')} ==")
    print(f"K=2 deltas={K2_DELTAS} pd={PDS} N={NS} seeds={SEEDS} ticks={TICKS} comp arm calm")
    print(f"F2 ref (K=2): {F2_REF}")

    # ---- C1: round-21 octave replays (pd=3, calm K=8, r=delta/8) ----
    want = {1: 2, 2: 3, 6: 4}
    ok_c1 = True
    for r in want:
        w = wall_from(comp_wins(8, 3, r * 8, DRIFT))
        ok_c1 = ok_c1 and w == want[r]
        print(f"C1 replay pd=3 calm K=8 r={r}: wall={w} (want {want[r]}) "
              f"[{time.time()-T0:4.0f}s]")
    print(f"C1 octave replays: {'PASS' if ok_c1 else 'FAIL -> no verdict'}")

    # ---- C2: round-22 K=2 replays (pd=3, calm) ----
    ok_c2 = True
    for d, wantw in ((8, 4), (16, 4)):
        w = wall_from(comp_wins(2, 3, d, DRIFT))
        ok_c2 = ok_c2 and w == wantw
        print(f"C2 replay K=2 pd=3 d={d}: wall={w} (want {wantw}) [{time.time()-T0:4.0f}s]")
    print(f"C2 r22 replays: {'PASS' if ok_c2 else 'FAIL -> no verdict'}")

    # ---- C3: byte-identity double run (full K=2 pd=3 d=48 cell) ----
    a = cell_dump(2, 3, 48, DRIFT)
    b = cell_dump(2, 3, 48, DRIFT)
    ok_c3 = a == b
    print(f"C3 double-run byte-identity (K=2 pd=3 d=48): {'PASS' if ok_c3 else 'FAIL'}")

    # ---- C4: mislabeled-arm self-canary at round-2 anchor cell ----
    # round-2 anchor: N=5 stress default (delta=12 K=4 pd=3), raw=68.0 sort=69.6
    lats = lats_for(5)
    laghat = [discover_lag(L) for L in lats]
    p = dict(K=4, drift=6, delta=12, pulse_div=3)
    raw5 = sum(run_sw(sd, C=5, lats=lats, **p)["pct"] for sd in SEEDS) / len(SEEDS)
    sort5 = sum(run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
                for sd in SEEDS) / len(SEEDS)
    ok_anchor = abs(raw5 - 68.0) <= 0.05 and abs(sort5 - 69.6) <= 0.05
    caught = ok_anchor and not (abs(sort5 - 68.0) <= 0.05)
    print(f"C4 anchor raw={raw5:.1f} sort={sort5:.1f} (want 68.0/69.6) "
          f"anchor={'PASS' if ok_anchor else 'FAIL'}; "
          f"mislabeled(sort->'raw')={sort5:.1f} vs 68.0 -> "
          f"{'CAUGHT' if caught else 'NOT CAUGHT'}")
    print(f"C4: {'PASS' if caught else 'FAIL -> no verdict'}")

    gates = ok_c1 and ok_c2 and ok_c3 and caught
    print(f"\ncanary gate: {'ALL PASS' if gates else 'FAIL -> no verdict'}")
    if not gates:
        return

    # ---- main grid: K=2 ----
    wall = {}
    for pd in PDS:
        for d in K2_DELTAS:
            wall[(2, pd, d)] = wall_from(comp_wins(2, pd, d, DRIFT))
            print(f"K=2 pd={pd} d={d:2d}: wall={wall[(2, pd, d)]} "
                  f"F2={F2_REF[d]} [{time.time()-T0:4.0f}s]")

    # ---- K=1 controls (recorded, not gated) ----
    print("\n-- K=1 controls (drift=3) --")
    for pd in PDS:
        for d in K1_DELTAS:
            wall[(1, pd, d)] = wall_from(comp_wins(1, pd, d, DRIFT))
            print(f"K=1 pd={pd} d={d:2d}: wall={wall[(1, pd, d)]} [{time.time()-T0:4.0f}s]")

    # ---- pre-registered verdict ----
    print("\n-- verdict (pre-registered rule, frozen) --")
    big = {d: [wall[(2, pd, d)] for pd in PDS if wall[(2, pd, d)] is not None]
           for d in K2_DELTAS}
    cross_deltas = [d for d in K2_DELTAS if d >= 24 and any(w >= 6 for w in big[d])]
    flat_ok = all(w is not None and w <= 4 for d in K2_DELTAS for w in big[d])
    print(f"K=2 walls by delta: d8={big[8]} d12={big[12]} d16={big[16]} "
          f"d20={big[20]} d24={big[24]} d32={big[32]} d48={big[48]} (lists=[pd2,pd3])")
    if cross_deltas:
        dstar = min(cross_deltas)
        print(f"VERDICT: CROSS -- wall >= 6 at delta >= {dstar}; K=2 joins the F2 regime; "
              f"delta*(K=2) recorded at {dstar}")
    elif flat_ok:
        print("VERDICT: FLAT-ALL -- K=2 walls <= 4 through delta=48 in all pd cells; "
              "K-line is a TRUE PHASE BOUNDARY between single- and multi-stream worlds; "
              "K=1-only pd-stratified model stands")
    else:
        print("VERDICT: AMBIGUOUS -- intermediate growth (5-only or None cells); "
              "map honest, next probe: densify delta grid around first wall>4 cell")

    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
