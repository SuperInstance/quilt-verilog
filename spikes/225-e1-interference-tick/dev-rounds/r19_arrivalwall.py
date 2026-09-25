#!/usr/bin/env python3
"""DEV ROUND 19 -- O2d: does the fan-out wall track candidate arrival rate (delta/K)?

Round-17's only surviving structural hypothesis, booked verbatim:
"wall tracks candidate arrival rate (delta/K) -- sweep that at fixed pd next."
Fixed pd=3; two families (K=8/drift=3 calm-like, K=4/drift=6 stress-like) with
delta swept so r = delta/K spans 0.25..12 (~1.7 decades). N in 2..13, raw +
lag-compensated arms (run_sw_comp verbatim), seeds (1,7,42,1999,20260902),
4800 ticks, integer-only inside loops.

Wall (round-3 gate, unchanged): smallest N whose mag+C=1 win over admit-all
(mean %w, 5 seeds) >= +2.0pp. Primary = raw arm (anchor-comparable); comp reported.

Canaries built in:
  (2) anchor replay: N=5 stress default raw admit-all %w=68.0, mag+C=1 %w=69.6
      (round-2 published, exact); pd=3 default wall must be exactly 6 (round-17/3).
  (3) mislabeled-arm self-canary: mag+C=1 relabeled admit-all must be CAUGHT.
  (1) byte-identity double-run: handled by the shell wrapper (two runs, diff).
Decision rule: see ROUND-19-arrival-rate-wall.md PART 1 (pre-registered).
Run: python3 -u r19_arrivalwall.py > r19-arrivalwall-output.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glm3_experiments import run_sw
from o2_contention import run_sw_comp, discover_lag, SEEDS, TICKS

PD = 3
NS = tuple(range(2, 14))
LATS_N = {
    2: (0, 12),
    3: (0, 6, 12),
    5: (0, 3, 6, 9, 12),
    8: (0, 2, 3, 5, 7, 8, 10, 12),
}
FAMILIES = {
    "calm":   dict(K=8, drift=3, deltas=(2, 4, 6, 12, 24, 48)),
    "stress": dict(K=4, drift=6, deltas=(2, 4, 8, 12, 24, 48)),
}
DEFAULT_DELTA = {"calm": 6, "stress": 12}   # round-2/3/17 anchors
R17_WALLS = {2: 5, 3: 6, 6: 7}              # out-of-sample anchors (ef6e2b5)

T0 = time.time()


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def cell_pct(fam, delta, n, arm):
    """Mean %w over 5 seeds for (admit-all, mag+C=1) at this cell, given arm."""
    lats = lats_for(n)
    p = dict(K=FAMILIES[fam]["K"], drift=FAMILIES[fam]["drift"],
             delta=delta, pulse_div=PD)
    raw = sort = 0.0
    if arm == "comp":
        laghat = [discover_lag(L) for L in lats]
    for sd in SEEDS:
        if arm == "raw":
            r_raw = run_sw(sd, C=n, lats=lats, **p)
            r_sort = run_sw(sd, key="mag", C=1, lats=lats, **p)
        else:
            r_raw = run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)
            r_sort = run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)
        raw += r_raw["pct"]
        sort += r_sort["pct"]
    raw /= len(SEEDS)
    sort /= len(SEEDS)
    return raw, sort


def wall_from(win_by_n):
    return next((n for n in NS if win_by_n.get(n) is not None and win_by_n[n] >= 2.0), None)


def main():
    print(f"== O2d arrival-rate (delta/K) wall sweep start {time.strftime('%H:%M:%S')} ==")
    print(f"pd={PD} families: {[(f, FAMILIES[f]['deltas']) for f in FAMILIES]}")
    print(f"N={NS} seeds={SEEDS} arms=raw+comp wall-gate=+2.0pp (round-3, unchanged)")

    # ---- Canary 2a: round-2 anchor replay (N=5 stress default, raw) ----
    raw5, sort5 = cell_pct("stress", DEFAULT_DELTA["stress"], 5, "raw")
    print(f"\n-- canary: round-2 anchor replay (stress delta=12 K=4 pd=3 N=5 raw) --")
    ok_anchor = abs(raw5 - 68.0) <= 0.05 and abs(sort5 - 69.6) <= 0.05
    print(f"  admit-all %w={raw5:.1f} (want 68.0)  mag+C=1 %w={sort5:.1f} (want 69.6)"
          f"  -> {'PASS' if ok_anchor else 'FAIL'}")

    # ---- Canary 3: mislabeled-arm self-canary (must be CAUGHT) ----
    print("-- canary: mislabeled arm (mag+C=1 relabeled admit-all) must be CAUGHT --")
    mislabeled_matches_anchor = abs(sort5 - 68.0) <= 0.05
    caught = not mislabeled_matches_anchor and ok_anchor
    print(f"  mislabeled %w={sort5:.1f} vs anchor 68.0 -> "
          f"{'CAUGHT' if caught else 'NOT CAUGHT (gate broken)'}")

    # ---- main sweep ----
    print("\n-- sweep (raw arm primary; comp arm alongside) --")
    wins = {}          # (fam, delta, arm) -> {n: win}
    for fam, cfg in FAMILIES.items():
        for delta in cfg["deltas"]:
            for arm in ("raw", "comp"):
                w = {}
                for n in NS:
                    raw, sort = cell_pct(fam, delta, n, arm)
                    w[n] = sort - raw
                    print(f"  {fam:6s} d={delta:2d} K={cfg['K']} r={delta/cfg['K']:5.2f} "
                          f"{arm:4s} N={n:2d} raw%w={raw:6.1f} sort%w={sort:6.1f} "
                          f"win={w[n]:+6.1f} [{time.time()-T0:5.0f}s]")
                wins[(fam, delta, arm)] = w

    # ---- walls ----
    print("\n-- walls (first N with mean win >= +2.0pp; raw = primary) --")
    walls_raw = {}
    walls_comp = {}
    for fam, cfg in FAMILIES.items():
        for delta in cfg["deltas"]:
            wr = wall_from(wins[(fam, delta, "raw")])
            wc = wall_from(wins[(fam, delta, "comp")])
            walls_raw[(fam, delta)] = wr
            walls_comp[(fam, delta)] = wc
            print(f"  {fam:6s} r={delta/cfg['K']:5.2f} (d={delta:2d},K={cfg['K']}) "
                  f"wall_raw={wr} wall_comp={wc}")

    # ---- Canary 2b: round-17 pd=3 default wall == 6 (exact) ----
    # default wall = mean of calm/stress default-delta wins per N, raw arm (round-17 metric)
    wmean = {}
    for n in NS:
        vals = []
        for fam in FAMILIES:
            v = wins[(fam, DEFAULT_DELTA[fam], "raw")].get(n)
            if v is not None:
                vals.append(v)
        wmean[n] = sum(vals) / len(vals) if vals else None
    wall_pd3 = wall_from(wmean)
    print(f"\n-- canary: round-17 pd=3 default wall replay --")
    print(f"  mean(default-delta) win by N: "
          + " ".join(f"{n}:{wmean[n]:+.1f}" for n in NS if wmean[n] is not None))
    ok_wall = wall_pd3 == R17_WALLS[3]
    print(f"  default wall={wall_pd3} (want exactly {R17_WALLS[3]}) -> "
          f"{'PASS' if ok_wall else 'FAIL -> no verdict, harness non-comparable'}")

    gates_ok = ok_anchor and caught and ok_wall
    if not gates_ok:
        print("\nCANARY/CONTROL FAILURE -- no verdict booked (see PART 2)")
        print(f"done in {time.time()-T0:.0f}s")
        return

    # ---- decision rule (pre-registered, PART 1) ----
    print("\n-- decision-rule evaluation --")
    # (a) non-flat across the r decade, per family, raw arm
    spans = {}
    for fam in FAMILIES:
        ws = [walls_raw[(fam, d)] for d in FAMILIES[fam]["deltas"]]
        known = [w for w in ws if w is not None]
        spans[fam] = (max(known) - min(known)) if len(known) == len(ws) else None
        print(f"  (a) {fam}: walls={ws} span={spans[fam]}")
    a_pass = all(s is not None and s >= 2 for s in spans.values())
    # (b) cross-family collapse at overlapping r, within +-1 seat
    rmap = {}
    for fam, cfg in FAMILIES.items():
        for d in cfg["deltas"]:
            rmap.setdefault((fam, d), d / cfg["K"])
    by_r = {}
    for (fam, d), w in walls_raw.items():
        by_r.setdefault(rmap[(fam, d)], []).append(w)
    b_detail, b_pass = [], True
    for r in sorted(by_r):
        ws = [w for w in by_r[r] if w is not None]
        if len(set(by_r[r]) and {None}) == 0 and len(ws) > 1:
            ok = max(ws) - min(ws) <= 1
            b_pass = b_pass and ok
            b_detail.append((r, ws, ok))
        print(f"  (b) r={r}: walls={by_r[r]}")
    for r, ws, ok in b_detail:
        print(f"      overlap r={r}: spread={max(ws)-min(ws)} -> {'OK' if ok else 'MISS'}")
    b_pass = len(b_detail) > 0 and b_pass
    # (c) round-17 out-of-sample anchors pd=2 (5) and pd=6 (7) at same default r
    c_pass = all(abs(R17_WALLS[pd] - wall_pd3) <= 1 for pd in (2, 6))
    print(f"  (c) r17 anchors: pd=2 wall {R17_WALLS[2]} vs default wall {wall_pd3} "
          f"(+-1) ; pd=6 wall {R17_WALLS[6]} -> {'PASS' if c_pass else 'MISS'}")

    print("\n-- verdict inputs --")
    print(f"  (a) non-flat (span>=2 both families): {'PASS' if a_pass else 'FAIL'}")
    print(f"  (b) cross-family collapse (+-1):      {'PASS' if b_pass else 'FAIL'}")
    print(f"  (c) r17 pd-anchor collapse (+-1):     {'PASS' if c_pass else 'FAIL'}")
    if a_pass and b_pass and c_pass:
        print("VERDICT: PROMOTE -- arrival-rate law; walls collapse onto delta/K")
    elif not a_pass:
        print("VERDICT: BOOK fan-out structural -- wall flat across >=1 decade of r")
    else:
        print("VERDICT: PARTIAL -- see PART 2 table; book surviving reading, post-hoc label")
    print(f"done in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
