#!/usr/bin/env python3
"""SPIN 10 — PHASE-SCHEDULED INTERFERENCE (from banked N1/N2 + SPIN-5 chatter).

Brief: promote phase-aware scheduling to a first-class control knob.
  EXP1  even-offset sweep: all-zero grammar + per-twin offsets i*d,
        d in {0,1,2,3,6} (lats=[0,d,2d,3d,4d,5d]); metric = residency per
        event spent; then matched-MAX-OFFSET grids (M=5, M=15) asking
        "is evenly-spread optimal?" against every other multiset at the
        same worst-case staleness.
  EXP2  transplant the best phase schedule into the real grammars
        (ladder / cohort 3+3 / kcoh5-fresh) at spread 15 and 30, K in {1,2}:
        intra-cohort 1-tick decorrelation variants (min / exact-spread /
        shift). Does anti-sync help good grammars or only cure chatter?
  EXP3  composition on the N1 memory-window channel (tri3, sigma=3):
        6-twin zero-lock + even offsets d in {0,1,2,3,6} x K in {1,2,4,8},
        plus the 2-twin [0,10] anchor and its stale-offset family
        [0,10+d]. Does cross-tick memory (K) compose with anti-sync (d),
        additively or destructively?

Canaries (mandatory, run first):
  A  run2 (novel lane's proven pluggable-reality port) byte-identical to
     exp_glm1.run_fabric on e1 reality (8/8 full-dict) — catches port drift.
  B  published-anchor replay, means +-0.15 and events/debt rounded-exact:
     zero-lock K1/2/8 (novel N2: 77.3/50.0/69.0, ev 8756/15133/9964,
     debt 187834/511660/195470), even d=1 = ladder(5) (97.6/84.9/90.2),
     ladder15 (71.5/60.0/70.7), ladder30 (26.8/28.9), cohort15
     (57.1/41.8/61.4), cohort30 (49.3/33.3), kcoh5@15 (74.1/50.6/72.8),
     kcoh5@30 = outlier@30 (53.2/47.4), quart15 (62.6/56.1), tri15
     (64.6/59.4), kcoh1@15 (47.3/34.4), and the N1 tri3 [0,10] anchor
     (13.9/39.4/41.9/45.6).
  offset=0 rows must byte-match the novel lane's baseline (enforced by B).

Integer-only inside every loop (fabric contract). Floats only in display.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # spike root
sys.path.insert(0, str(ROOT / "inventors-derby"))
sys.path.insert(0, str(ROOT / "wheel" / "novel"))
from exp_glm1 import run_fabric, within_pm, LCG  # noqa: E402
from novel_exp import run2, tri, one, mean, SEEDS  # noqa: E402

DELTA = 12
N = 6
TICKS = 4800


def row(cells):
    return " | ".join(f"{c:>10}" for c in cells)


def even(d, n=N):
    return [i * d for i in range(n)]


def run_e1(lats, k, seed):
    return run_fabric("interference", TICKS, lats, K=k, pd=3,
                      delta=DELTA, drift=6, seed=seed)


def run_tri(ch, lats, k, seed):
    return run2("interference", TICKS, lats, ch, K=k, pd=3,
                delta=DELTA, drift=6, seed=seed)


def stats(lats, k, ch=None):
    rs = [run_tri(ch, lats, k, s) if ch else run_e1(lats, k, s)
          for s in SEEDS]
    tp = [within_pm(r["resid"], DELTA) for r in rs]
    return dict(tp=mean(tp) / 10, ev=mean([r["events"] for r in rs]),
                debt=mean([r["mass"] for r in rs]),
                canc=mean([r["cancels"] for r in rs]),
                chat=mean([r["chatter"] for r in rs]))


def rpe(tp, ev):
    """Residency permille per 1000 events (display float)."""
    return tp * 100.0 / ev if ev else 0.0     # tp in %, ev in events


# ------------------------- canaries -------------------------
def canaries():
    print("== CANARY A: run2 port byte-identical to run_fabric (e1 reality) ==")
    ok = True
    from exp_glm1 import reality
    for mode in ("sequential", "interference"):
        for lats in ([0] * 6, [0, 10]):
            for k in (1, 8):
                a = run_fabric(mode, TICKS, lats, K=k, pd=3,
                               delta=DELTA, drift=6, seed=SEEDS[0])
                b = run2(mode, TICKS, lats, reality, K=k, pd=3,
                         delta=DELTA, drift=6, seed=SEEDS[0])
                if a != b:
                    ok = False
                    print(f"  MISMATCH {mode} {lats} K={k}")
    print("  PASS: 8/8 configs full-dict identical" if ok else "  FAIL")

    print("\n== CANARY B: published-anchor replay (mean% +-0.15; ev/debt rounded-exact where published) ==")
    print(row(["config", "K", "got%", "want%", "ev", "evWant", "debt", "dWant", "ok"]))
    anchors = [
        # name, lats, K, want_tp, want_ev, want_debt, channel
        ("zero", [0] * 6, 1, 77.3, 8756, 187834, None),
        ("zero", [0] * 6, 2, 50.0, 15133, 511660, None),
        ("zero", [0] * 6, 8, 69.0, 9964, 195470, None),
        ("even1=lad5", even(1), 1, 97.6, 2598, 43929, None),
        ("even1=lad5", even(1), 2, 84.9, 5773, 147001, None),
        ("even1=lad5", even(1), 8, 90.2, 4172, 71893, None),
        ("even2=lad10", even(2), 1, 93.5, None, None, None),
        ("even2=lad10", even(2), 2, 89.7, None, None, None),
        ("even3=lad15", even(3), 1, 71.5, 5792, 106378, None),
        ("even3=lad15", even(3), 2, 60.0, None, None, None),
        ("even3=lad15", even(3), 8, 70.7, None, None, None),
        ("even6=lad30", even(6), 1, 26.8, None, None, None),
        ("even6=lad30", even(6), 2, 28.9, None, None, None),
        ("cohort15", [0, 0, 0, 15, 15, 15], 1, 57.1, None, None, None),
        ("cohort15", [0, 0, 0, 15, 15, 15], 2, 41.8, None, None, None),
        ("cohort15", [0, 0, 0, 15, 15, 15], 8, 61.4, None, None, None),
        ("cohort30", [0, 0, 0, 30, 30, 30], 1, 49.3, None, None, None),
        ("cohort30", [0, 0, 0, 30, 30, 30], 2, 33.3, None, None, None),
        ("kcoh5@15", [0, 0, 0, 0, 0, 15], 1, 74.1, None, None, None),
        ("kcoh5@15", [0, 0, 0, 0, 0, 15], 2, 50.6, None, None, None),
        ("kcoh5@15", [0, 0, 0, 0, 0, 15], 8, 72.8, None, None, None),
        ("kcoh5@30", [0, 0, 0, 0, 0, 30], 1, 53.2, None, None, None),
        ("kcoh5@30", [0, 0, 0, 0, 0, 30], 2, 47.4, None, None, None),
        ("quart15", [0, 0, 0, 0, 15, 15], 1, 62.6, None, None, None),
        ("quart15", [0, 0, 0, 0, 15, 15], 2, 56.1, None, None, None),
        ("tri15", [0, 0, 7, 7, 15, 15], 1, 64.6, None, None, None),
        ("tri15", [0, 0, 7, 7, 15, 15], 2, 59.4, None, None, None),
        ("kcoh1@15", [0, 15, 15, 15, 15, 15], 1, 47.3, None, None, None),
        ("kcoh1@15", [0, 15, 15, 15, 15, 15], 2, 34.4, None, None, None),
        ("tri3[0,10]K1", [0, 10], 1, 13.9, None, None, "tri3"),
        ("tri3[0,10]K2", [0, 10], 2, 39.4, None, None, "tri3"),
        ("tri3[0,10]K4", [0, 10], 4, 41.9, None, None, "tri3"),
        ("tri3[0,10]K8", [0, 10], 8, 45.6, None, None, "tri3"),
    ]
    ok2 = True
    for name, lats, k, want, wev, wdebt, ch in anchors:
        s = stats(lats, k, tri(3) if ch == "tri3" else None)
        good = abs(s["tp"] - want) <= 0.15
        if wev is not None:
            good &= round(s["ev"]) == wev
        if wdebt is not None:
            good &= round(s["debt"]) == wdebt
        ok2 &= good
        print(row([name, k, f"{s['tp']:.1f}", want,
                   f"{round(s['ev'])}", wev if wev is not None else "-",
                   f"{round(s['debt'])}", wdebt if wdebt is not None else "-",
                   "OK" if good else "DRIFT"]))
    print(f"  anchor replay: {'PASS' if ok2 else 'FAIL'}")
    return ok and ok2


# ------------------------- EXP 1 -------------------------
def exp1_sweep():
    print("\n== EXP1a: even-offset sweep  lats=[0,d,2d,3d,4d,5d]  (zero-grammar origin, K x d) ==")
    print(row(["d (step)", "K", "true%", "events", "debt", "RPE", "canc"]))
    tbl = {}
    for d in (0, 1, 2, 3, 6):
        for k in (1, 2, 8):
            s = stats(even(d), k)
            tbl[(d, k)] = s
            print(row([d, k, f"{s['tp']:.1f}", f"{s['ev']:.0f}",
                       f"{s['debt']:.0f}", f"{rpe(s['tp'], s['ev']):.0f}",
                       f"{s['canc']:.0f}"]))
    print("\n-- residency per event (RPE = true-permille per 1000 events), argmax per K --")
    for k in (1, 2, 8):
        best = max((0, 1, 2, 3, 6), key=lambda d: rpe(tbl[(d, k)]["tp"], tbl[(d, k)]["ev"]))
        line = "  ".join(f"d={d}:{rpe(tbl[(d,k)]['tp'], tbl[(d,k)]['ev']):.0f}"
                         for d in (0, 1, 2, 3, 6))
        print(f"  K={k}: {line}   -> best d={best}")
    return tbl


def exp1b_matched():
    print("\n== EXP1b: matched MAX-OFFSET grids — is evenly-spread optimal? ==")
    grids = [
        ("M=5", [
            ("even5  012345", even(1)),
            ("coh5   000555", [0, 0, 0, 5, 5, 5]),
            ("pair5  001155", [0, 0, 1, 1, 5, 5]),
            ("out5   000005", [0, 0, 0, 0, 0, 5]),
        ]),
        ("M=15", [
            ("even15 lad", even(3)),
            ("kcoh5@15", [0, 0, 0, 0, 0, 15]),
            ("tri15", [0, 0, 7, 7, 15, 15]),
            ("quart15", [0, 0, 0, 0, 15, 15]),
            ("coh15  3+3", [0, 0, 0, 15, 15, 15]),
            ("kcoh1@15", [0, 15, 15, 15, 15, 15]),
        ]),
    ]
    for gname, cfgs in grids:
        print(f"\n-- {gname} (same worst-case staleness; zero-lock = M0 reference) --")
        print(row(["schedule", "K", "true%", "events", "RPE"]))
        rows = []
        for name, lats in cfgs:
            for k in (1, 2):
                s = stats(lats, k)
                rows.append((name, k, s))
                print(row([name, k, f"{s['tp']:.1f}", f"{s['ev']:.0f}",
                           f"{rpe(s['tp'], s['ev']):.0f}"]))
        for k in (1, 2):
            bk = max((r for r in rows if r[1] == k),
                     key=lambda r: r[2]["tp"])
            br = max((r for r in rows if r[1] == k),
                     key=lambda r: rpe(r[2]["tp"], r[2]["ev"]))
            print(f"  K={k}: max true% = {bk[0]} ({bk[2]['tp']:.1f}); "
                  f"max RPE = {br[0]} ({rpe(br[2]['tp'], br[2]['ev']):.0f})")


# ------------------------- EXP 2 -------------------------
def exp2_grammars():
    print("\n== EXP2: phase-schedule transplant into real grammars (K in {1,2}) ==")
    print("   AS-min   = one 1-tick offset per cohort      (spread +0)")
    print("   AS-exact = full within-cohort decorrelation  (spread preserved)")
    print("   AS-shift = full decorrelation, cohort tops kept (spread grows)")
    print(row(["grammar", "variant", "lats", "K", "true%", "events",
               "d-base pp", "RPE"]))
    fam = [
        ("ladder15", [
            ("base", even(3)),
        ]),
        ("ladder30", [
            ("base", even(6)),
        ]),
        ("cohort15", [
            ("base", [0, 0, 0, 15, 15, 15]),
            ("AS-min", [0, 0, 1, 14, 15, 15]),
            ("AS-exact", [0, 1, 2, 13, 14, 15]),
            ("AS-shift", [0, 1, 2, 15, 16, 17]),
        ]),
        ("cohort30", [
            ("base", [0, 0, 0, 30, 30, 30]),
            ("AS-min", [0, 0, 1, 29, 30, 30]),
            ("AS-exact", [0, 1, 2, 28, 29, 30]),
            ("AS-shift", [0, 1, 2, 30, 31, 32]),
        ]),
        ("kcoh5@15", [
            ("base", [0, 0, 0, 0, 0, 15]),
            ("AS-min", [0, 0, 0, 0, 1, 15]),
            ("AS-exact", [0, 1, 2, 3, 4, 15]),
        ]),
        ("kcoh5@30", [
            ("base", [0, 0, 0, 0, 0, 30]),
            ("AS-min", [0, 0, 0, 0, 1, 30]),
            ("AS-exact", [0, 1, 2, 3, 4, 30]),
        ]),
    ]
    results = {}
    for gname, variants in fam:
        base_tp = {}
        for vname, lats in variants:
            for k in (1, 2):
                s = stats(lats, k)
                results[(gname, vname, k)] = s
                if vname == "base":
                    base_tp[k] = s["tp"]
        for vname, lats in variants:
            for k in (1, 2):
                s = results[(gname, vname, k)]
                dpp = s["tp"] - base_tp[k] if vname != "base" else 0.0
                print(row([gname, vname, str(lats), k, f"{s['tp']:.1f}",
                           f"{s['ev']:.0f}", f"{dpp:+.1f}",
                           f"{rpe(s['tp'], s['ev']):.0f}"]))
    print("\n-- sequential reference (K=1) --")
    print(row(["grammar", "variant", "true%", "events"]))
    for gname, vname, lats in [
        ("cohort15", "base", [0, 0, 0, 15, 15, 15]),
        ("cohort15", "AS-exact", [0, 1, 2, 13, 14, 15]),
        ("cohort30", "base", [0, 0, 0, 30, 30, 30]),
        ("cohort30", "AS-exact", [0, 1, 2, 28, 29, 30]),
        ("kcoh5@15", "base", [0, 0, 0, 0, 0, 15]),
        ("kcoh5@15", "AS-exact", [0, 1, 2, 3, 4, 15]),
    ]:
        rs = [run_fabric("sequential", TICKS, lats, K=1, pd=3,
                         delta=DELTA, drift=6, seed=s) for s in SEEDS]
        print(row([gname, vname,
                   f"{mean([within_pm(r['resid'], DELTA) for r in rs])/10:.1f}",
                   f"{mean([r['events'] for r in rs]):.0f}"]))
    return results


# ------------------------- EXP 3 -------------------------
def exp3_composition():
    ch = tri(3)
    print("\n== EXP3: composition on the N1 memory-window channel (tri3, sigma=3) ==")
    print("-- 3a. N1 anchor: 2-twin [0,10] replay + stale-offset family [0,10+d] --")
    print(row(["lats", "K", "true%", "events", "debt"]))
    for d in (0, 1, 2, 3, 6):
        for k in (1, 8):
            s = stats([0, 10 + d], k, ch)
            print(row([f"[0,{10+d}]", k, f"{s['tp']:.1f}", f"{s['ev']:.0f}",
                       f"{s['debt']:.0f}"]))
    print("\n-- 3b. 6-twin family on tri3: zero-lock + even offsets x K --")
    print(row(["lats", "K", "true%", "events", "debt", "chat", "RPE"]))
    tbl = {}
    for d in (0, 1, 2, 3, 6):
        for k in (1, 2, 4, 8):
            s = stats(even(d), k, ch)
            tbl[(d, k)] = s
            print(row([f"even{d}", k, f"{s['tp']:.1f}", f"{s['ev']:.0f}",
                       f"{s['debt']:.0f}", f"{s['chat']:.0f}",
                       f"{rpe(s['tp'], s['ev']):.0f}"]))
    print("\n-- 3c. decomposition: K-gap (K8-K1) per d; d-gain (vs d=0) per K --")
    for d in (0, 1, 2, 3, 6):
        gap = tbl[(d, 8)]["tp"] - tbl[(d, 1)]["tp"]
        print(f"  d={d}: K8-K1 = {gap:+.1f} pp   (K1 {tbl[(d,1)]['tp']:.1f} -> K8 {tbl[(d,8)]['tp']:.1f})")
    for k in (1, 2, 4, 8):
        gains = "  ".join(f"d={d}:{tbl[(d,k)]['tp']-tbl[(0,k)]['tp']:+.1f}"
                          for d in (1, 2, 3, 6))
        print(f"  K={k}: {gains}")
    b = tbl[(0, 1)]["tp"]
    gk = tbl[(0, 8)]["tp"] - b
    print(f"\n  baseline (d=0,K=1) = {b:.1f}; pure-K gain = {gk:+.1f} pp")
    for d in (1, 2, 3, 6):
        gd = tbl[(d, 1)]["tp"] - b
        comb = tbl[(d, 8)]["tp"]
        add = b + gk + gd
        print(f"  d={d}: pure-d gain {gd:+.1f}; additive pred {add:.1f}; "
              f"measured {comb:.1f}; surplus {comb-add:+.1f} pp")
    print("\n-- 3d. sequential reference on tri3 (K=1) --")
    for name, lats in (("zero", [0] * 6), ("even1", even(1))):
        rs = [run2("sequential", TICKS, lats, ch, K=1, pd=3,
                   delta=DELTA, drift=6, seed=s) for s in SEEDS]
        print(row([name,
                   f"{mean([within_pm(r['resid'], DELTA) for r in rs])/10:.1f}",
                   f"{mean([r['events'] for r in rs]):.0f}"]))


def main():
    ok = canaries()
    if not ok:
        print("\nCANARY FAILURE — aborting (no numbers booked)")
        sys.exit(1)
    exp1_sweep()
    exp1b_matched()
    exp2_grammars()
    exp3_composition()
    x = LCG(2035015474).next()
    print(f"\nLCG ritual: 2035015474 -> {x} -> mod 10 = {x % 10}")


if __name__ == "__main__":
    main()
