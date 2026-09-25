#!/usr/bin/env python3
"""DEV ROUND 27 (pre-registration) -- replicate the lone deviant cell
before its interpretation (DEVIL nudge on round 26).

Round 26 (3349f85) booked DRIFT-BLIND 14/15 with the single deviation
(drift=12, pd=4) -> wall 8 (one seat below the r25 ladder's 9), and
labeled "the +1 premium is drift-carried" post-hoc.  DEVIL's teeth,
accepted: (1) per-cell noise floor never booked -- 15 cells x +-1 gate
makes a single chance deviation unremarkable; (2) delta-inertness was
established for pd=3 only -- the deviant cell is pd=4.

Design (K=1, comp arm, calm, N 2..18, wall = first N >= 2.0pp):
- G-SEEDS (tooth 1): TEN FRESH seeds (3, 11, 31, 77, 101, 555, 1009,
  2027, 12345, 20260903 -- disjoint from the o2 set) at
  (drift=12, pd=4, delta=12).  HOLD: wall == 8.  FLIP: wall == 9.
  Other: OTHER-SEAT, booked literally.
- G-DELTA (tooth 2): same cell at delta in {16, 32} under the o2
  seed set (5 seeds): if wall returns to 9 (or moves) at either
  delta, the drift-exception reading evaporates into a
  delta-x-drift-x-pd interaction; if 8 holds at both, drift
  exception survives the delta axis.
- Noise-floor context (booked, no gate): (drift=12, pd=5) and
  (drift=12, pd=3) re-run under the 10 fresh seeds -- if any
  ladder-stable cell moves under seed change, the 5-seed grid's
  noise floor is +-1 and 14/15 robustness is weak evidence by
  itself.

Booking rule (frozen BEFORE any number):
  "drift-carried +1 premium" STAYS ledger vocabulary only if
  G-SEEDS == HOLD and both G-DELTA cells read 8.
  G-SEEDS == FLIP -> the premium reading is STRUCK from the ledger
  and round 26's STEP-LOC sub-probe reading is demoted to
  unreplicated-single-cell (the law itself, DRIFT-BLIND by letter,
  survives -- it never depended on the deviant cell).
  G-DELTA move without G-SEEDS flip -> relabel as
  delta-x-drift-x-pd interaction, not drift exception.

Canaries (all required): o2-seed replays pd=4 drift=6 -> 9 exact
(r25 seat), pd=3 drift=12 -> 6 exact (r26 cell), K=8 octave 2/3/4.
Run: python3 -u r27_deviant_repl.py > r27-deviantrepl-output.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o2_contention import run_sw_comp, discover_lag, SEEDS, TICKS

T0 = time.time()
NS = tuple(range(2, 19))
FRESH_SEEDS = (3, 11, 31, 77, 101, 555, 1009, 2027, 12345, 20260903)
LATS_N = {2: (0, 12), 3: (0, 6, 12), 5: (0, 3, 6, 9, 12),
          8: (0, 2, 3, 5, 7, 8, 10, 12)}


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def wins_kd(k, pd, drift, delta, seeds):
    wins = {}
    for n in NS:
        lats = lats_for(n)
        laghat = [discover_lag(L) for L in lats]
        raw = sort = 0.0
        for sd in seeds:
            p = dict(K=k, drift=drift, delta=delta, pulse_div=pd)
            raw += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
            sort += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
        wins[n] = (sort - raw) / len(seeds)
    return wins


def wall_from(wins):
    return next((n for n in NS if wins.get(n) is not None and wins[n] >= 2.0), None)


def main():
    print(f"== O2j deviant-cell replication start {time.strftime('%H:%M:%S')} ==")

    # ---- canaries (o2 seeds) ----
    ok = True
    w = wall_from(wins_kd(1, 4, 6, 12, SEEDS))
    ok = ok and w == 9
    print(f"replay pd=4 drift=6: wall={w} (want 9)")
    w = wall_from(wins_kd(1, 3, 12, 12, SEEDS))
    ok = ok and w == 6
    print(f"replay pd=3 drift=12: wall={w} (want 6)")
    for r, want_w in ((1, 2), (2, 3), (6, 4)):
        w = wall_from(wins_kd(8, 3, 3, r * 8, SEEDS))
        ok = ok and w == want_w
        print(f"replay K=8 r={r}: wall={w} (want {want_w})")
    print(f"canaries: {'PASS' if ok else 'FAIL -> no verdict'}")
    if not ok:
        return

    # ---- G-SEEDS: fresh 10-seed replication of the deviant cell ----
    w_fresh = wall_from(wins_kd(1, 4, 12, 12, FRESH_SEEDS))
    print(f"\nG-SEEDS (drift=12, pd=4, delta=12, 10 fresh seeds): wall={w_fresh}")
    if w_fresh == 8:
        g_seeds = "HOLD"
    elif w_fresh == 9:
        g_seeds = "FLIP"
    else:
        g_seeds = "OTHER-SEAT"
    print(f"G-SEEDS: {g_seeds}")

    # ---- noise-floor context ----
    for pd in (5, 3):
        w_ctx = wall_from(wins_kd(1, pd, 12, 12, FRESH_SEEDS))
        print(f"noise-floor ctx (drift=12, pd={pd}, fresh seeds): wall={w_ctx} (r26 o2-seed: {({5: 11, 3: 6})[pd]})")

    # ---- G-DELTA: delta axis under o2 seeds ----
    g_delta = {}
    for d in (16, 32):
        w_d = wall_from(wins_kd(1, 4, 12, d, SEEDS))
        g_delta[d] = w_d
        print(f"G-DELTA (drift=12, pd=4, delta={d}): wall={w_d}")

    # ---- booking ----
    print("\n-- BOOKING --")
    stable = all(v == 8 for v in g_delta.values())
    if g_seeds == "HOLD" and stable:
        print("'drift-carried +1 premium' STAYS ledger vocabulary (HOLD + delta-stable)")
    elif g_seeds == "FLIP":
        print("G-SEEDS FLIP -- 'drift-carried +1 premium' STRUCK; round-26 STEP-LOC "
              "sub-probe demoted to unreplicated-single-cell; DRIFT-BLIND law "
              "itself survives (never depended on the deviant cell)")
    elif g_seeds == "HOLD" and not stable:
        print(f"delta-dependence (G-DELTA {g_delta}) -- relabel: delta-x-drift-x-pd "
              "interaction, NOT a drift exception")
    else:
        print(f"G-SEEDS {g_seeds} with G-DELTA {g_delta} -- booked literally, "
              "neither reading holds")

    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
