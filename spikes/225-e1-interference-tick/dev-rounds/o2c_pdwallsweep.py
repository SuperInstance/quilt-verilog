#!/usr/bin/env python3
"""DEV ROUND 17 (pre-registration) -- O2c: does the fan-out wall TRACK 2pd?

IDEATOR nudge, booked from round 16 (a486b40, "wall stays at N=6",
4th straight survival across lag-comp/dial/sort/suppressor knobs):
a wall no knob moves is a structural constant candidate, and spin-11's
echo law already predicts a lattice-structure boundary at N = 2pd
(safe at 2pd, divergent at 2pd+1).  All prior O2 rounds ran pd=3,
so N=6 == 2*3 is confounded: same-wall vs same-pd.  This round
un-confounds it with a PURE-pd sweep (EXP4 tested mixed-pd only).

Arms: admit-all raw vs mag+C=1 sorted switchboard (round-2/3 method,
verbatim metric), regimes calm+stress, pd in {2, 3, 6} via pulse_div,
N in 2..13 (canonical lat sets pinned for N in {2,3,5,8}; others
interpolate spreads 0..12), seeds (1, 7, 42, 1999, 20260902).

Wall definition (round-3 gate, unchanged): smallest N whose sorted
win (mean %w over calm+stress, 5 seeds) is >= +2.0pp over admit-all.

Pre-registered decision rule (decided BEFORE the run):
  G-TRACK: walls strictly increase with pd and each |wall(pd) - 2pd| <= 1
    -> the fan-out wall IS the echo-law safe boundary; round-17 verdict
    "promotion rule gains a pd clause: O2 wall predicted at N=2pd".
  G-SEVER: walls(pd) do not increase with pd (equal or non-monotone)
    -> cleanly severed; "the wall tracks structure" dies and the wall
    stays an empirical contention constant at this metric.
  else: PARTIAL -- report actual (pd, wall) table as measured.
  Control: pd=3 must reproduce wall at N=6 (|6 - wall| <= 1) or the
  harness is declared non-comparable and NO verdict is booked.

Integer-only inside loops; percentages once at print time.
Run: python3 -u o2c_pdwallsweep.py > o2c-pdwallsweep-output.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glm3_experiments import run_sw
from o2_contention import REGIMES, SEEDS

PDS = (2, 3, 6)
NS = tuple(range(2, 14))
LATS_N = {
    2: (0, 12),
    3: (0, 6, 12),
    5: (0, 3, 6, 9, 12),
    8: (0, 2, 3, 5, 7, 8, 10, 12),
}

T0 = time.time()


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def pct_w(rows):
    return sum(r["pct"] for r in rows) / len(rows)


def main():
    print(f"== O2c pure-pd wall sweep start {time.strftime('%H:%M:%S')} ==")
    print(f"pd={PDS} N={NS} seeds={SEEDS} regimes={list(REGIMES)}")
    win = {}
    for pd in PDS:
        for n in NS:
            lats = lats_for(n)
            raw_pct = sort_pct = 0.0
            nruns = 0
            for reg, rp in REGIMES.items():
                params = dict(rp)
                params["pulse_div"] = pd
                for sd in SEEDS:
                    r_raw = run_sw(sd, C=n, lats=lats, **params)          # admit-all: key=None, C=N
                    r_sort = run_sw(sd, key="mag", C=1, lats=lats, **params)
                    raw_pct += r_raw["pct"]
                    sort_pct += r_sort["pct"]
                    nruns += 1
            raw_pct /= nruns
            sort_pct /= nruns
            win[(pd, n)] = sort_pct - raw_pct
            print(f"  pd={pd} N={n:2d} lats={lats} raw%w={raw_pct:6.1f} "
                  f"sort%w={sort_pct:6.1f} win={win[(pd, n)]:+6.1f} "
                  f"[{time.time()-T0:5.0f}s]")
    print("\n-- walls (first N with mean win >= +2.0pp) --")
    walls = {}
    for pd in PDS:
        wall = next((n for n in NS if win[(pd, n)] >= 2.0), None)
        walls[pd] = wall
        print(f"  pd={pd}: wall={wall}  (echo-law 2pd={2*pd})")
    print("\n-- gates --")
    ctl = walls[3] is not None and abs(walls[3] - 6) <= 1
    print(f"control pd=3 wall~6: {'PASS' if ctl else 'FAIL -> no verdict, harness non-comparable'}")
    if ctl:
        inc = walls[2] is not None and walls[3] is not None and walls[6] is not None \
            and walls[2] < walls[3] < walls[6]
        track = inc and all(abs(walls[p] - 2 * p) <= 1 for p in PDS)
        sever = not (walls[2] is not None and walls[3] is not None and walls[6] is not None
                     and walls[2] < walls[3] < walls[6])
        if track:
            print("G-TRACK PASS: wall == echo-law safe boundary N=2pd; promotion rule gains pd clause")
        elif sever:
            print("G-SEVER PASS: walls do not increase with pd; wall is an empirical contention constant")
        else:
            print("PARTIAL: walls increase but do not bracket 2pd within +-1; table above is the verdict")
    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
