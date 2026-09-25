#!/usr/bin/env python3
"""DEV ROUND 24 -- K=1 seating at drift-matched grid
(pre-registration: ROUND-24-k1-drift.md PART 1, committed cd09969 BEFORE numbers).

Question (round 23's named rung): does the K=1 pd=3 comp-wall (6, delta-flat
at drift=3) re-acquire delta-growth at drift=6?  Two-knob (pd,drift) object
vs delta-range artifact of round-21's narrow delta grid (SPIN-32: walls
6/9/11/None across pd 3..6 at drift=6, delta in 8..16).

Grid: K=1 x pd=3 x drift{3,6} x delta{8,16,32,48} x N 2..13, comp arm
(mag+C=1 vs admit-all), calm, seeds 1/7/42/1999/20260902, 4800 ticks.
Wall = first N with mean win >= 2.0pp (identical to r21/r23).

Canaries (frozen in PART 1): C1 double-run byte-identity of the
(pd=3, drift=6, delta=8) cell; C2 round-23 K=1 anchor replay EXACT
(drift=3: pd2 -> 4/4/4, pd3 -> 6/6/6 at delta 8/16/32); C3 mislabeled-arm
self-canary at the round-2 anchor cell (68.0/69.6) -- verdict logic must
CATCH the deliberate mislabel.

Verdict (pre-registered, frozen):
  DRIFT-TWO-KNOB  drift=6 delta-monotone growth >=2 seats (d8->d48) AND
                  drift=3 flat (max-min <= 1)
  DRIFT-ARTIFACT  drift=6 flat or moves <=1 seat, no monotone trend
  AMBIGUOUS       otherwise (incl. None at drift=6 delta=8: left edge above
                  N=13, book seated cells honestly)
Run: python3 -u r24_k1_drift.py > r24-k1drift-output.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o2_contention import run_sw_comp, run_sw, discover_lag, SEEDS, TICKS

T0 = time.time()
NS = tuple(range(2, 14))
DELTAS = (8, 16, 32, 48)
DRIFTS = (3, 6)
PD = 3
K = 1
# round-23 K=1 anchors (drift=3): {(pd, delta): wall}
R23_ANCHORS = {(2, 8): 4, (2, 16): 4, (2, 32): 4,
               (3, 8): 6, (3, 16): 6, (3, 32): 6}

LATS_N = {2: (0, 12), 3: (0, 6, 12), 5: (0, 3, 6, 9, 12),
          8: (0, 2, 3, 5, 7, 8, 10, 12)}


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def cell_dump(drift, delta):
    """Deterministic per-cell dump (C1 byte-identity canary)."""
    lines = []
    for n in NS:
        lats = lats_for(n)
        laghat = [discover_lag(L) for L in lats]
        raw = sort = 0.0
        for sd in SEEDS:
            p = dict(K=K, drift=drift, delta=delta, pulse_div=PD)
            raw += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
            sort += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
        lines.append(f"N={n} win={(sort - raw) / len(SEEDS):.6f}")
    return "\n".join(lines)


def comp_wins(drift, delta, pd=PD, k=K):
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
    print(f"== R24 k1 drift-matched start {time.strftime('%H:%M:%S')} ==")
    print(f"K={K} pd={PD} drift={DRIFTS} delta={DELTAS} N={NS} "
          f"seeds={SEEDS} ticks={TICKS} comp arm calm")

    # ---- C1: double-run byte-identity (pd=3, drift=6, delta=8 cell) ----
    a = cell_dump(6, 8)
    b = cell_dump(6, 8)
    ok_c1 = a == b
    print(f"C1 double-run byte-identity (pd=3 drift=6 d=8): "
          f"{'PASS' if ok_c1 else 'FAIL'}")

    # ---- C2: round-23 K=1 anchor replay (drift=3) ----
    ok_c2 = True
    for (pd, d), want in sorted(R23_ANCHORS.items()):
        w = wall_from(comp_wins(3, d, pd=pd))
        ok = w == want
        ok_c2 = ok_c2 and ok
        print(f"C2 replay K=1 pd={pd} d={d:2d} drift=3: wall={w} "
              f"(want {want}) {'OK' if ok else 'MISMATCH'} "
              f"[{time.time()-T0:4.0f}s]")
    print(f"C2 r23 K=1 anchor replay: {'PASS' if ok_c2 else 'FAIL'}")

    # ---- C3: mislabeled-arm self-canary at round-2 anchor cell ----
    # round-2 anchor: N=5 stress default (delta=12 K=4 pd=3), raw=68.0 sort=69.6
    lats = lats_for(5)
    p = dict(K=4, drift=6, delta=12, pulse_div=3)
    raw5 = sum(run_sw(sd, C=5, lats=lats, **p)["pct"] for sd in SEEDS) / len(SEEDS)
    sort5 = sum(run_sw(sd, key="mag", C=1, lats=lats, **p)["pct"]
                for sd in SEEDS) / len(SEEDS)
    ok_anchor = abs(raw5 - 68.0) <= 0.05 and abs(sort5 - 69.6) <= 0.05
    caught = ok_anchor and not (abs(sort5 - 68.0) <= 0.05)
    print(f"C3 anchor raw={raw5:.1f} sort={sort5:.1f} (want 68.0/69.6) "
          f"anchor={'PASS' if ok_anchor else 'FAIL'}; "
          f"mislabeled(sort->'raw')={sort5:.1f} vs 68.0 -> "
          f"{'CAUGHT' if caught else 'NOT CAUGHT'}")
    print(f"C3: {'PASS' if caught else 'FAIL'}")

    gates = ok_c1 and ok_c2 and caught
    print(f"\ncanary gate: {'ALL PASS' if gates else 'FAIL -> no verdict'}")
    if not gates:
        return

    # ---- main grid: K=1 pd=3, drift x delta walls ----
    wall = {}
    for drift in DRIFTS:
        for d in DELTAS:
            wall[(drift, d)] = wall_from(comp_wins(drift, d))
            print(f"K=1 pd={PD} drift={drift} d={d:2d}: wall={wall[(drift, d)]} "
                  f"[{time.time()-T0:4.0f}s]")

    # ---- pre-registered verdict ----
    print("\n-- verdict (pre-registered rule, frozen) --")
    w3 = [wall[(3, d)] for d in DELTAS]
    w6 = [wall[(6, d)] for d in DELTAS]
    print(f"walls drift=3: {w3}  drift=6: {w6} (delta {DELTAS})")

    def flat(ws):
        present = [w for w in ws if w is not None]
        return len(present) == len(ws) and max(present) - min(present) <= 1

    def monotone_growth(ws):
        present = [w for w in ws if w is not None]
        if None in ws or len(present) < len(ws):
            return 0
        mono = all(ws[i + 1] >= ws[i] for i in range(len(ws) - 1))
        return (present[-1] - present[0]) if mono else -1

    g6 = monotone_growth(w6)
    print(f"drift=3 flat={flat(w3)}; drift=6 monotone_growth={g6} seats")
    if wall[(6, 8)] is None:
        print("VERDICT: AMBIGUOUS -- drift=6 d=8 wall sits above N=13; "
              "left edge unseated, no growth readable; seated cells booked")
    elif g6 >= 2 and flat(w3):
        print(f"VERDICT: DRIFT-TWO-KNOB -- drift=6 grows {g6} seats (d8->d48, "
              "monotone) while drift=3 stays flat; delta re-enters the K=1 "
              "world only under drift=6; pd-stratification is a genuinely "
              "two-knob (pd,drift) object")
    elif all(w is not None for w in w6) and max(w6) - min(w6) <= 1:
        print("VERDICT: DRIFT-ARTIFACT -- drift=6 wall flat (moves <=1 seat "
              "across delta, no monotone trend); r23's delta-blindness "
              "extends to drift=6; two-knob (pd,drift) object with "
              "delta-flat walls at each seat")
    else:
        print("VERDICT: AMBIGUOUS -- intermediate pattern; seated cells "
              "booked honestly, next probe named in the round doc")

    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
