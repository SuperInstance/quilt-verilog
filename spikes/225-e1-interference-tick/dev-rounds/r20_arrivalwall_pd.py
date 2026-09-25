#!/usr/bin/env python3
"""DEV ROUND 20 -- does the comp-collapse law survive at pd in {2, 6}?

Round-19 booked next spoke: lag compensation collapses the K degree of freedom --
comp wall(delta/K) is a single curve across both delta/K families over 1.7 decades
(pd=3). Test at pd=2 and pd=6 (same sweep: calm K=8/drift=3, stress K=4/drift=6,
deltas spanning r=delta/K over >=1 decade, N=2..13, raw + comp arms, seeds
(1,7,42,1999,20260902), 4800 ticks, integer-only core).

Canaries built in:
  (1) byte-identity: per-cell dumps written to r20-data/ (deterministic, no
      timings); wrapper runs twice and diffs -- see ROUND-20 .md.
  (2) anchor replay: r19 pd=3 comp walls reproduce EXACTLY (hardcoded from
      4cbfd83); round-17 raw default walls pd2->5, pd3->6, pd6->7 (exact);
      round-2 N=5 stress raw anchor 68.0/69.6.
  (3) mislabeled-arm self-canary: mag+C=1 relabeled admit-all must be CAUGHT.
Wall gate: round-3, unchanged -- smallest N with mean win (mag+C=1 minus
admit-all, 5 seeds) >= +2.0pp. comp wall at r<0.5 excluded from collapse read
(r19's calm r=0.25 outlier is pre-declared out of the law's stated domain).
Run: python3 -u r20_arrivalwall_pd.py > r20-pd-output.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glm3_experiments import run_sw
from o2_contention import run_sw_comp, discover_lag, SEEDS, TICKS

PDS = (2, 3, 6)
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
R17_WALLS = {2: 5, 3: 6, 6: 7}              # raw default walls (ef6e2b5)
# r19 (4cbfd83) comp walls, pd=3, exact-replay anchors: (fam, delta) -> wall
R19_COMP_PD3 = {
    ("calm", 2): 7, ("calm", 4): 2, ("calm", 6): 2,
    ("calm", 12): 3, ("calm", 24): 3, ("calm", 48): 4,
    ("stress", 2): 2, ("stress", 4): 2, ("stress", 8): 3,
    ("stress", 12): 3, ("stress", 24): 4, ("stress", 48): 4,
}
RMIN = 0.5   # comp-collapse domain floor (pre-declared)

T0 = time.time()
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r20-data")


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def cell_pct(fam, delta, n, arm, pd):
    lats = lats_for(n)
    p = dict(K=FAMILIES[fam]["K"], drift=FAMILIES[fam]["drift"],
             delta=delta, pulse_div=pd)
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
    print(f"== round 20 comp-collapse pd sweep start {time.strftime('%H:%M:%S')} ==")
    print(f"pd={PDS} families: {[(f, FAMILIES[f]['deltas']) for f in FAMILIES]}")
    print(f"N={NS} seeds={SEEDS} arms=raw+comp wall-gate=+2.0pp (round-3, unchanged)")
    os.makedirs(OUTDIR, exist_ok=True)

    # ---- Canary 2a: round-2 anchor replay (N=5 stress default, raw, pd=3) ----
    raw5, sort5 = cell_pct("stress", DEFAULT_DELTA["stress"], 5, "raw", 3)
    print(f"\n-- canary: round-2 anchor replay (stress delta=12 K=4 pd=3 N=5 raw) --")
    ok_anchor = abs(raw5 - 68.0) <= 0.05 and abs(sort5 - 69.6) <= 0.05
    print(f"  admit-all %w={raw5:.1f} (want 68.0)  mag+C=1 %w={sort5:.1f} (want 69.6)"
          f"  -> {'PASS' if ok_anchor else 'FAIL'}")

    # ---- Canary 3: mislabeled-arm self-canary (must be CAUGHT) ----
    print("-- canary: mislabeled arm (mag+C=1 relabeled admit-all) must be CAUGHT --")
    caught = not (abs(sort5 - 68.0) <= 0.05) and ok_anchor
    print(f"  mislabeled %w={sort5:.1f} vs anchor 68.0 -> "
          f"{'CAUGHT' if caught else 'NOT CAUGHT (gate broken)'}")

    # ---- main sweep: pd in {2, 3, 6} ----
    wins = {}          # (pd, fam, delta, arm) -> {n: win}
    walls = {}         # (pd, fam, delta, arm) -> wall N
    for pd in PDS:
        print(f"\n-- sweep pd={pd} (raw = round-17 anchor arm; comp = collapse arm) --")
        for fam, cfg in FAMILIES.items():
            for delta in cfg["deltas"]:
                for arm in ("raw", "comp"):
                    w = {}
                    for n in NS:
                        raw, sort = cell_pct(fam, delta, n, arm, pd)
                        w[n] = sort - raw
                        print(f"  pd={pd} {fam:6s} d={delta:2d} K={cfg['K']} "
                              f"r={delta/cfg['K']:5.2f} {arm:4s} N={n:2d} "
                              f"raw%w={raw:6.1f} sort%w={sort:6.1f} "
                              f"win={w[n]:+6.1f} [{time.time()-T0:5.0f}s]")
                    wins[(pd, fam, delta, arm)] = w
                    walls[(pd, fam, delta, arm)] = wall_from(w)
                    # deterministic per-cell dump for byte-identity canary
                    fn = os.path.join(OUTDIR, f"pd{pd}_{fam}_d{delta}_{arm}.txt")
                    with open(fn, "w") as fh:
                        fh.write("\n".join(
                            f"N={n} win={w[n]:+.1f}" for n in NS) + "\n")

    # ---- walls summary ----
    print("\n-- walls (first N with mean win >= +2.0pp) --")
    for pd in PDS:
        for fam, cfg in FAMILIES.items():
            for delta in cfg["deltas"]:
                wr = walls[(pd, fam, delta, "raw")]
                wc = walls[(pd, fam, delta, "comp")]
                print(f"  pd={pd} {fam:6s} r={delta/cfg['K']:5.2f} (d={delta:2d},"
                      f"K={cfg['K']}) wall_raw={wr} wall_comp={wc}")

    # ---- Canary 2b: round-17 raw default walls (exact), pd in {2,3,6} ----
    print("\n-- canary: round-17 raw default wall replay (mean of default-delta wins) --")
    ok_wall = {}
    for pd in PDS:
        wmean = {}
        for n in NS:
            vals = [wins[(pd, fam, DEFAULT_DELTA[fam], "raw")][n] for fam in FAMILIES]
            wmean[n] = sum(vals) / len(vals)
        w = wall_from(wmean)
        ok_wall[pd] = (w == R17_WALLS[pd])
        print(f"  pd={pd} mean win by N: "
              + " ".join(f"{n}:{wmean[n]:+.1f}" for n in NS)
              + f"  -> wall={w} (want exactly {R17_WALLS[pd]}) "
              f"{'PASS' if ok_wall[pd] else 'FAIL'}")

    # ---- Canary 2c: r19 pd=3 comp walls reproduce EXACTLY ----
    print("\n-- canary: r19 pd=3 comp wall exact replay (anchor curve) --")
    ok_comp = True
    for (fam, d), want in sorted(R19_COMP_PD3.items()):
        got = walls[(3, fam, d, "comp")]
        match = got == want
        ok_comp = ok_comp and match
        print(f"  pd=3 {fam:6s} d={d:2d}: comp wall={got} (want {want}) "
              f"{'PASS' if match else 'FAIL'}")

    gates_ok = ok_anchor and caught and all(ok_wall.values()) and ok_comp
    if not gates_ok:
        print("\nCANARY/CONTROL FAILURE -- no verdict booked (see PART 2)")
        print(f"done in {time.time()-T0:.0f}s")
        return

    # ---- decision rule (pre-registered, ROUND-20 PART 1) ----
    print("\n-- decision-rule evaluation (comp arm, r >= 0.5 domain) --")
    # build comp wall vs r per pd: r -> list of walls (both families)
    by_pd = {}
    for pd in PDS:
        cur = {}
        for fam, cfg in FAMILIES.items():
            for d in cfg["deltas"]:
                r = d / cfg["K"]
                if r >= RMIN:
                    cur.setdefault(round(r, 3), []).append(
                        walls[(pd, fam, d, "comp")])
        by_pd[pd] = cur

    for pd in PDS:
        print(f"  pd={pd} comp walls by r: "
              + " ".join(f"{r}:{by_pd[pd][r]}" for r in sorted(by_pd[pd])))

    # (a) collapse WITHIN each pd: at every overlapping r, family spread <= 1 seat
    within_ok = {}
    for pd in PDS:
        det, ok = [], True
        for r in sorted(by_pd[pd]):
            ws = [w for w in by_pd[pd][r] if w is not None]
            if len(by_pd[pd][r]) > 1 and len(ws) == len(by_pd[pd][r]):
                m = max(ws) - min(ws) <= 1
                ok = ok and m
                det.append((r, max(ws) - min(ws), m))
        within_ok[pd] = ok
        for r, s, m in det:
            print(f"  (a) pd={pd} overlap r={r}: spread={s} -> {'OK' if m else 'MISS'}")

    # (b) collapse ACROSS pd: same r, wall within +-1 seat of pd=3 anchor value
    across_ok, offsets = {}, {}
    for pd in (2, 6):
        okp, offs = True, []
        for r in sorted(by_pd[pd]):
            a3 = by_pd[3].get(r)
            ap = by_pd[pd][r]
            if a3 is None or any(w is None for w in a3 + ap):
                continue
            m3, mp = max(a3), max(ap)
            okp = okp and abs(mp - m3) <= 1
            offs.append((r, m3, mp))
            print(f"  (b) pd={pd} r={r}: pd3={m3} pd{pd}={mp} "
                  f"{'OK' if abs(mp - m3) <= 1 else 'MISS'}")
        across_ok[pd] = okp
        offsets[pd] = offs

    print("\n-- verdict inputs (comp arm) --")
    print(f"  (a) within-pd family collapse: "
          + " ".join(f"pd{pd}:{'PASS' if within_ok[pd] else 'FAIL'}" for pd in PDS))
    print(f"  (b) cross-pd collapse vs pd=3 anchor (+-1): "
          + " ".join(f"pd{pd}:{'PASS' if across_ok[pd] else 'FAIL'}" for pd in (2, 6)))
    if all(within_ok.values()) and all(across_ok.values()):
        print("VERDICT: PROMOTE -- comp-collapse law survives pd in {2,3,6};")
        print("         comp wall(r) single curve, pd is not a knob in comp regime")
    elif not across_ok[2] and not across_ok[6]:
        # measure offsets for the booking
        print("VERDICT: BOOK -- pd is a second knob in the comp regime too;")
        print("         measured offsets vs pd=3 (max seat shift per r, pd arm):")
        for pd in (2, 6):
            for r, m3, mp in offsets[pd]:
                if mp != m3:
                    print(f"           pd={pd} r={r}: +{mp - m3:+d} seats")
    else:
        bad = [pd for pd in (2, 6) if not across_ok[pd]]
        good = [pd for pd in (2, 6) if across_ok[pd]]
        print(f"VERDICT: PARTIAL -- collapse holds at pd={good}, breaks at pd={bad};")
        print("         boundary lies between; book offsets for the breaking pd above")
    print(f"done in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
