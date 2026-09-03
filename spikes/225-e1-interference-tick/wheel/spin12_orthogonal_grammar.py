#!/usr/bin/env python3
"""SPIN 12, SPOKE: ORTHOGONAL-GRAMMAR (proposed by SPIN-9).

SPIN-9's finding to decouple: stale-mass m_s is a validated first-order law
(pooled within-K isotonic R^2=0.973) but the second axis — the coherent
fresh cohort n_f (# lags <= delta/2) — was CONFOUNDED: every grammar in
SPIN-9's grid varied fresh-cohort and stale-mass together (anticorrelated
by construction). The 3-param law (n_f, m_s, K) reached R^2=0.877 with
identifiable residual structure. This spin builds the orthogonal grid.

DEFINITIONS (pinned, SPIN-9):
  coherence threshold  c = delta/2 = 6               (delta = 12, stress)
  fresh cohort         n_f = # lags <= 6             (never fire on ramps:
                                                     (8/5)lag > 12 iff lag >= 8)
  stale-mass           m_s = sum max(0, lat-6) / 144 (lags >= delta=12 are
                                                     'stale'; danger zone
                                                     (6,12) EXCLUDED from the
                                                     orthogonal family)
  K in {1,2,4}.

DESIGN NOTES (structural, honest):
  - Spread-30 + contains-0 + lags<=30 forces n_f >= 1 (the 0 counts) and
    n_f <= 5 (a 30 must be present). Brief's n_f=0 and n_f=6 are not
    realizable in-family; realized grid n_f in {1,2,3,4,5}, with the
    spread-0 zero-lock [0]*6 control (n_f=6, m_s=0) run out-of-family.
  - With N=6 fixed, raising n_f lowers the stale COUNT; the m_s WINDOW
    shrinks mechanically (fewer stale slots): n_f=1:[48,120], 2:[42,96],
    3:[36,72], 4:[30,48], 5:[24,24] (units: excess/144). Common bands:
    m_s=48 shared by n_f in {1,2,3,4}; m_s=60,72 by n_f in {1,2,3}.
  - 'Pure n_f effect at fixed m_s' therefore means: pinned scalar pair,
    stale multiset redistributed underneath. EXP2 tests whether that
    redistribution (stale internals) matters at all.

EXPERIMENTS
  EXP1 ORTHO GRID  30 in-family grammars spanning (n_f, m_s) cells
      (16 cells, up to 4 grammars per cell) x K{1,2,4} x 5 seeds.
      Slices: n_f at fixed m_s (48/60/72) and m_s at fixed n_f (1-4).
  EXP2 STALE FUNGIBILITY  at pinned (n_f, m_s): stale dispersion
      {all-equal, half-half, spread, cluster/block} — does internal stale
      structure matter, or is stale mass fungible? Includes SPIN-9's
      residual hint: coherent block {24,24,30} vs split {18,30,30} at
      (3,60), and fresh-internals pairs (0s vs 6s) at pinned scalars.
  EXP3 REFIT  G1 additive (n_f, m_s, K) [SPIN-9 F1c analog, R^2 vs 0.877];
      G2 = +n_f x K interaction (SPIN-9 flip surface predicts real gain);
      G3 = +n_f x m_s (cell-saturated + K); G4 fully saturated (cell x K)
      ceiling — 1-G4 = pure within-cell (stale/fresh internals) spread.
      Out-of-family failure controls g2/stag (danger-zone lags 8/10)
      scored against G1: where the law still fails.

PRE-REGISTERED PREDICTIONS (before running):
  P1  m_s slice monotone DECREASING in all four n_f rows (SPIN-9 first-
      order law, now unconfounded), Spearman <= -0.8 per row.
  P2  n_f slice at fixed m_s monotone INCREASING but sublinear (plateau
      by n_f~3), per SPIN-9 fresh x K cell means 51.9/50.5/54.3 flat top.
  P3  G1 R^2 >= 0.877 on the clean orthogonal family (danger-zone
      confounds excluded).
  P4  n_f x K interaction REAL: G2 - G1 >= +0.03 (SPIN-9 flip surface:
      n_f>=4 rows rise with K, n_f<=3 fall).
  P5  stale NOT fungible: within-(3,60) spread >= 10pp (coherent block
      {24,24,30} beats split {18,30,30}).
  P6  fresh internals (0s vs 6s at pinned scalars) differ <= 3pp.

CANARIES (mandatory):
  A. wiring byte-identity: helper-built lats == literal lats (ladder30 and
     zero0), full resid+cflags traces, 5 seeds x K{1,2}; plus spread-0
     [0]*6 byte-identity.
  B. SPIN-9 replay anchors, exact per-seed permille + events/debt:
     zero@30 K=1  (791,755,775,780,762) ev 8756 debt 187834
     ladder@30 K=1 (264,253,266,281,274) ev 14952 debt 366275
     m24@30 K=1    (504,505,494,504,494)   [bimodal ~50% invariance]
     d24@30 K=1    (505,504,492,501,492)   [bimodal ~50% invariance]
     zero@30 K=4 mean 73.9 / K=8 mean 69.0 (brief's '~74' = K=4) tol 1.5pp.
  C. determinism: independent canary-B run of ladder@30 K=1 must equal the
     grid's nf2_ms60 K=1 cell byte-for-byte.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
COH = DELTA // 2          # 6
N = 6
TICKS = 4800
KS = (1, 2, 4)
T0 = time.time()


# ---------------------------------------------------------- grammars
def fresher(nf, stale):
    """Helper: nf fresh twins (one 0 + (nf-1) sixes) + sorted stale lags."""
    return [0] + [6] * (nf - 1) + sorted(stale)


GRAMMARS = (  # (name, lats, group, tag)
    # --- orthogonal grid: fresh lags <= 6, stale lags >= 12, spread 30
    ("nf1_ms48",  [0, 12, 12, 12, 12, 30], "grid", "stale 12x4+30"),
    ("nf1_ms60",  [0, 12, 12, 18, 18, 30], "grid", "half-half"),
    ("nf1_ms72",  [0, 18, 18, 18, 18, 30], "grid", "stale 18x4+30"),
    ("nf1_ms120", [0, 30, 30, 30, 30, 30], "grid", "=l1_5"),
    ("nf2_ms48",  [0, 6, 12, 12, 18, 30],  "grid", ""),
    ("nf2_ms60",  [0, 6, 12, 18, 24, 30],  "grid", "=ladder30 graded stale"),
    ("nf2_ms72",  [0, 6, 18, 18, 30, 30],  "grid", "half-half"),
    ("nf2_ms96",  [0, 6, 30, 30, 30, 30],  "grid", "fresh6 b2_4-class"),
    ("nf3_ms36",  [0, 6, 6, 12, 12, 30],   "grid", "stale pair 12,12"),
    ("nf3_ms48",  [0, 6, 6, 12, 24, 30],   "grid", ""),
    ("nf3_ms60",  [0, 6, 6, 18, 30, 30],   "grid", "split 18,30"),
    ("nf3_ms72",  [0, 6, 6, 30, 30, 30],   "grid", "fresh6 c3_3-class"),
    ("nf4_ms30",  [0, 6, 6, 6, 12, 30],    "grid", "stale 12,30"),
    ("nf4_ms42",  [0, 6, 6, 6, 24, 30],    "grid", "fresh6 m24-class"),
    ("nf4_ms48",  [0, 6, 6, 6, 30, 30],    "grid", "fresh6 q4_2-class"),
    ("nf5_ms24",  [0, 6, 6, 6, 6, 30],     "grid", "fresh6 out5_1-class"),
    # --- SPIN-9 exact anchors (fresh-0 internals) — in-family cells
    ("b2_4",   [0, 0, 30, 30, 30, 30],    "anchor", "(2,96)"),
    ("c3_3",   [0, 0, 0, 30, 30, 30],     "anchor", "(3,72)"),
    ("m24",    [0, 0, 0, 0, 24, 30],      "anchor", "(4,42)"),
    ("q4_2",   [0, 0, 0, 0, 30, 30],      "anchor", "(4,48)"),
    ("out5_1", [0, 0, 0, 0, 0, 30],       "anchor", "(5,24)"),
    ("d24",    [0, 0, 0, 24, 24, 30],     "anchor", "(3,60) block 24,24,30"),
    # --- intra-stale coherence variants at pinned (n_f, m_s)
    ("coh1_eq",     [0, 15, 15, 15, 15, 30], "coh", "(1,60) all-equal 15x4"),
    ("coh1_spread", [0, 12, 14, 16, 18, 30], "coh", "(1,60) spread 12-18"),
    ("coh1_clus",   [0, 12, 12, 12, 24, 30], "coh", "(1,60) 3x12+24"),
    ("coh2_eq",     [0, 6, 18, 18, 18, 30],  "coh", "(2,60) all-equal 18x3"),
    ("coh2_half",   [0, 6, 12, 12, 30, 30],  "coh", "(2,60) half 12,12|30s"),
    ("coh2_spread", [0, 6, 14, 16, 24, 30],  "coh", "(2,60) spread 14-24"),
    ("coh3_block",  [0, 6, 6, 24, 24, 30],   "coh", "(3,60) block 24,24,30"),
    ("coh3_spread", [0, 6, 6, 22, 26, 30],   "coh", "(3,60) spread 22,26"),
    ("coh2b_eq",    [0, 6, 22, 22, 22, 30],  "coh", "(2,72) all-equal 22x3"),
    ("coh2b_spread", [0, 6, 18, 24, 24, 30], "coh", "(2,72) spread 18-24"),
    # --- out-of-family failure controls (danger-zone lags present)
    ("g2",   [0, 4, 8, 12, 16, 30],  "oof", "nf2 ms42/144, lag 8 in (6,12)"),
    ("stag", [0, 0, 0, 10, 20, 30],  "oof", "nf3 ms42/144, lag 10 in (6,12)"),
)

ZERO = [0] * N
LADDER30 = [0, 6, 12, 18, 24, 30]


def ms_num(lats):
    return sum(max(0, x - COH) for x in lats)          # over 144


def fresh(lats):
    return sum(1 for x in lats if x <= COH)


# ---------------------------------------------------------- helpers
def one(lats, k, seed, ticks=TICKS, delta=DELTA):
    return run_fabric("interference", ticks, lats, K=k, pd=3,
                      delta=delta, drift=6, seed=seed)


def scalars(r, delta=DELTA):
    return dict(true_pm=within_pm(r["resid"], delta), events=r["events"],
                debt=r["mass"], cancels=r["cancels"])


def mean(v):
    return sum(v) / len(v)


def row(cells, w=9):
    return " | ".join(f"{c:>{w}}" for c in cells)


def byte_identical(r1, r2):
    return (tuple(r1["resid"]) == tuple(r2["resid"])
            and tuple(r1["cflags"]) == tuple(r2["cflags"])
            and r1["events"] == r2["events"] and r1["mass"] == r2["mass"])


def ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    rk = [0] * len(vals)
    for pos, i in enumerate(order):
        rk[i] = pos + 1
    return rk


def spearman(xs, ys):
    rx, ry = ranks(xs), ranks(ys)
    return pearson(rx, ry)


def pearson(xs, ys):
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = ((sum((x - mx) ** 2 for x in xs)
            * sum((y - my) ** 2 for y in ys)) ** 0.5)
    return num / den if den else 0.0


# ---------------------------------------------------------- results
RES = {}       # (name, k) -> dict(mean pm, seeds, ev, dbt)
LATS = {n: l for n, l, _, _ in GRAMMARS}
GROUP = {n: g for n, _, g, _ in GRAMMARS}


def run_all():
    print("== EXP 0: FULL GRID RUNS (5 seeds x K{1,2,4}, interference, "
          "delta=12 drift=6 pd=3, 4800 ticks) ==")
    hdr = ["n_f", "m_s", "grammar", "lats", "grp", "K",
           "s1", "s7", "s42", "s1999", "s2s60902", "mean%", "evMean",
           "debtMean"]
    print(row(hdr, 9))
    for name, lats, grp, _tag in GRAMMARS:
        for k in KS:
            sc = [scalars(one(lats, k, sd)) for sd in SEEDS]
            tp = [x["true_pm"] for x in sc]
            RES[(name, k)] = dict(
                mean=mean(tp), seeds=tp,
                ev=mean([x["events"] for x in sc]),
                dbt=mean([x["debt"] for x in sc]))
            print(row([fresh(lats), f"{ms_num(lats)}/144", name, str(lats),
                       grp, k] + tp + [f"{mean(tp)/10:.1f}",
                       f"{RES[(name, k)]['ev']:.0f}",
                       f"{RES[(name, k)]['dbt']:.0f}"], 9))


# ---------------------------------------------------------- canaries
def canaries():
    ok = True
    print("\n== CANARY A: wiring byte-identity (helper lats == literal lats) ==")
    a_ok = True
    pairs = [(fresher(2, [12, 18, 24, 30]), LADDER30, "nf2_ms60/ladder30"),
             (fresher(3, [24, 24, 30]), [0, 6, 6, 24, 24, 30], "coh3_block"),
             (fresher(1, [30] * 5), [0, 30, 30, 30, 30, 30], "nf1_ms120"),
             ([0] * N, ZERO, "zero0 spread-0")]
    nchk = 0
    for helper, literal, tag in pairs:
        for k in (1, 2):
            for sd in SEEDS:
                nchk += 1
                if not byte_identical(one(helper, k, sd), one(literal, k, sd)):
                    a_ok = False
                    print(f"  MISMATCH {tag} K={k} seed={sd}")
    print(f"  PASS: {nchk}/{nchk} full-trace byte-identical"
          if a_ok else "  FAIL")
    ok &= a_ok

    print("\n== CANARY B: SPIN-9 replay anchors (exact per-seed permille) ==")
    pub = (("zero@30", ZERO, 1, (791, 755, 775, 780, 762), 8756, 187834),
           ("ladder@30", LADDER30, 1, (264, 253, 266, 281, 274),
            14952, 366275),
           ("m24@30", [0, 0, 0, 0, 24, 30], 1, (504, 505, 494, 504, 494),
            16616, 509310),
           ("d24@30", [0, 0, 0, 24, 24, 30], 1, (505, 504, 492, 501, 492),
            14628, 563127))
    b_ok = True
    for name, lats, k, pubpm, pubev, pubdbt in pub:
        sc = [scalars(one(lats, k, sd)) for sd in SEEDS]
        got = tuple(x["true_pm"] for x in sc)
        ev, dbt = mean([x["events"] for x in sc]), mean([x["debt"] for x in sc])
        good = (got == pubpm and abs(ev - pubev) <= 1
                and abs(dbt - pubdbt) <= 200)
        b_ok &= good
        print(f"  {name} K={k}: per-seed {got} vs pub {pubpm}  "
              f"ev {ev:.0f}/{pubev} debt {dbt:.0f}/{pubdbt}  "
              f"{'OK' if good else 'DRIFT'}")
    for k, pubmean in ((4, 73.9), (8, 69.0)):
        sc = [scalars(one(ZERO, k, sd)) for sd in SEEDS]
        got = mean([x["true_pm"] for x in sc]) / 10
        good = abs(got - pubmean) <= 1.5
        b_ok &= good
        print(f"  zero@30 K={k}: mean {got:.1f} vs pub {pubmean}  "
              f"{'OK' if good else 'DRIFT'}"
              f"   (brief's '~74' anchor = the K=4 value)")
    print("  PASS: all replay anchors" if b_ok else "  FAIL")
    ok &= b_ok
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — results below do "
          "NOT count")
    return ok


def determinism_check():
    print("\n== CANARY C: determinism (canary-B ladder run == grid "
          "nf2_ms60 run) ==")
    ok = True
    for sd in SEEDS:
        if not byte_identical(one(LADDER30, 1, sd),
                              one(LATS["nf2_ms60"], 1, sd)):
            ok = False
    print("  PASS: byte-identical 5/5" if ok else "  FAIL")
    return ok


# ---------------------------------------------------------- EXP 1
def cell_of(name):
    l = LATS[name]
    return (fresh(l), ms_num(l))


def exp1_slices():
    print("\n== EXP 1a: PURE n_f EFFECT at fixed m_s (cell means, pp) ==")
    for mtarget in (48, 60, 72):
        names = [n for n, _, g, _ in GRAMMARS if g != "oof"
                 and ms_num(LATS[n]) == mtarget]
        nfs = sorted({fresh(LATS[n]) for n in names})
        print(f"  -- m_s = {mtarget}/144 --")
        print(row(["n_f"] + [f"K={k}" for k in KS] + ["grammars"], 9))
        for nf in nfs:
            cell = [n for n in names if fresh(LATS[n]) == nf]
            vals = [mean([RES[(n, k)]["mean"] for n in cell]) / 10
                    for k in KS]
            print(row([nf] + [f"{v:.1f}" for v in vals]
                      + ["+".join(cell)], 9))
        # spearman over cell means, per K
        for k in KS:
            xs, ys = [], []
            for nf in nfs:
                cell = [n for n in names if fresh(LATS[n]) == nf]
                xs.append(nf)
                ys.append(mean([RES[(n, k)]["mean"] for n in cell]) / 10)
            print(f"     K={k}: Spearman(n_f, true%) = "
                  f"{spearman(xs, ys):+.2f}   "
                  f"range {min(ys):.1f}..{max(ys):.1f} "
                  f"(span {max(ys)-min(ys):.1f}pp)")

    print("\n== EXP 1b: PURE m_s EFFECT at fixed n_f (primary grammars, pp) ==")
    prim = {"nf1_ms48": 1, "nf1_ms60": 1, "nf1_ms72": 1, "nf1_ms120": 1,
            "nf2_ms48": 2, "nf2_ms60": 2, "nf2_ms72": 2, "nf2_ms96": 2,
            "nf3_ms36": 3, "nf3_ms48": 3, "nf3_ms60": 3, "nf3_ms72": 3,
            "nf4_ms30": 4, "nf4_ms42": 4, "nf4_ms48": 4, "nf5_ms24": 5}
    bynf = {}
    for n, nf in prim.items():
        bynf.setdefault(nf, []).append(n)
    for nf in (1, 2, 3, 4):
        ns = sorted(bynf[nf], key=lambda n: ms_num(LATS[n]))
        print(f"  -- n_f = {nf} --")
        print(row(["m_s"] + [f"K={k}" for k in KS] + ["grammar"], 9))
        for n in ns:
            vals = [RES[(n, k)]["mean"] / 10 for k in KS]
            print(row([f"{ms_num(LATS[n])}/144"] + [f"{v:.1f}" for v in vals]
                      + [n], 9))
        for k in KS:
            xs = [ms_num(LATS[n]) for n in ns]
            ys = [RES[(n, k)]["mean"] / 10 for n in ns]
            print(f"     K={k}: Spearman(m_s, true%) = "
                  f"{spearman(xs, ys):+.2f}   "
                  f"range {min(ys):.1f}..{max(ys):.1f} "
                  f"(span {max(ys)-min(ys):.1f}pp)")


# ---------------------------------------------------------- EXP 2
def exp2_stale():
    print("\n== EXP 2: STALE FUNGIBILITY at pinned (n_f, m_s) ==")
    cells = {(1, 60): ["nf1_ms60", "coh1_eq", "coh1_spread", "coh1_clus"],
             (2, 60): ["nf2_ms60", "coh2_eq", "coh2_half", "coh2_spread"],
             (3, 60): ["nf3_ms60", "coh3_block", "coh3_spread", "d24"],
             (2, 72): ["nf2_ms72", "coh2b_eq", "coh2b_spread"],
             (2, 96): ["nf2_ms96", "b2_4"],
             (3, 72): ["nf3_ms72", "c3_3"],
             (4, 42): ["nf4_ms42", "m24"],
             (4, 48): ["nf4_ms48", "q4_2"],
             (5, 24): ["nf5_ms24", "out5_1"]}
    for (nf, m), ns in cells.items():
        print(f"  -- cell (n_f={nf}, m_s={m}/144) --")
        print(row(["grammar", "stale lags", "fresh lags"]
                  + [f"K={k}" for k in KS] + ["swing"], 9))
        for n in ns:
            l = LATS[n]
            stale = [x for x in l if x >= DELTA]
            fr = [x for x in l if x <= COH]
            vals = [RES[(n, k)]["mean"] / 10 for k in KS]
            sw = max(max(RES[(n, k)]["seeds"]) - min(RES[(n, k)]["seeds"])
                     for k in KS) / 10
            print(row([n, str(stale), str(fr)] + [f"{v:.1f}" for v in vals]
                      + [f"~{sw:.1f}"], 9))
        for k in KS:
            vs = {n: RES[(n, k)]["mean"] / 10 for n in ns}
            sp = max(vs.values()) - min(vs.values())
            best = max(vs, key=vs.get)
            worst = min(vs, key=vs.get)
            print(f"     K={k}: within-cell spread {sp:.1f}pp  "
                  f"best {best} {vs[best]:.1f} / worst {worst} "
                  f"{vs[worst]:.1f}")

    print("\n== EXP 2b: FRESH INTERNALS (0s vs 6s) at pinned scalars, pp ==")
    pairs = [("nf5_ms24", "out5_1"), ("nf4_ms42", "m24"),
             ("nf4_ms48", "q4_2"), ("nf3_ms72", "c3_3"),
             ("nf2_ms96", "b2_4"), ("coh3_block", "d24")]
    for a, b in pairs:
        da = [RES[(a, k)]["mean"] / 10 - RES[(b, k)]["mean"] / 10
              for k in KS]
        print(f"  {a:>10} (fresh 0,6..) - {b:>7} (fresh 0,0..): "
              f"K1 {da[0]:+.1f}  K2 {da[1]:+.1f}  K4 {da[2]:+.1f} pp")


# ---------------------------------------------------------- EXP 3
def anova(obs, factors, iters=500):
    """obs: list of (y, key=(nf, ms, K)). factors: tuples of key indices.
    Alternating-means fit; returns predictions at observation granularity
    (SPIN-9 scar rule: nested models scored at the same granularity)."""
    ys = [o[0] for o in obs]
    keys = [o[1] for o in obs]
    mu = mean(ys)
    eff = []
    for f in factors:
        levs = {tuple(k[i] for i in f) for k in keys}
        eff.append({lv: 0.0 for lv in levs})
    for _ in range(iters):
        for fi, f in enumerate(factors):
            for lv in eff[fi]:
                idx = [i for i, k in enumerate(keys)
                       if tuple(k[i] for i in f) == lv]
                eff[fi][lv] = mean(
                    [ys[i] - mu
                     - sum(eff[gj][tuple(keys[i][j] for j in factors[gj])]
                           for gj in range(len(factors)) if gj != fi)
                     for i in idx])
    pred = lambda key: mu + sum(eff[fi][tuple(key[i2] for i2 in factors[fi])]
                                 for fi in range(len(factors)))
    return [pred(k) for k in keys], pred


def r2(ys, preds):
    m = mean(ys)
    sst = sum((y - m) ** 2 for y in ys)
    ssr = sum((y - p) ** 2 for y, p in zip(ys, preds))
    return 1 - ssr / sst if sst else 0.0


def exp3_fits():
    print("\n== EXP 3: REFIT on orthogonal grid (96 in-family grammar x K "
          "obs; SPIN-9 F1c = 0.877 reference) ==")
    obs = []
    for name, _, grp, _ in GRAMMARS:
        if grp == "oof":
            continue
        for k in KS:
            obs.append((RES[(name, k)]["mean"], cell_of(name) + (k,)))
    ys = [o[0] for o in obs]

    g1, g1_pred = anova(obs, [(0,), (1,), (2,)])
    print(f"  G1  mu + a(n_f) + c(m_s) + b(K):          R^2 = {r2(ys, g1):.3f}")
    g2, _ = anova(obs, [(0, 2), (1,)])
    print(f"  G2  mu + ab(n_f,K) + c(m_s):              R^2 = {r2(ys, g2):.3f}"
          f"   [G1 + n_f x K interaction: "
          f"{r2(ys, g2) - r2(ys, g1):+.3f}]")
    g3, _ = anova(obs, [(0, 1), (2,)])
    print(f"  G3  mu + cell(n_f,m_s) + b(K):            R^2 = {r2(ys, g3):.3f}"
          f"   [G1 + n_f x m_s interaction: "
          f"{r2(ys, g3) - r2(ys, g1):+.3f}]")
    g4, _ = anova(obs, [(0, 1, 2)])
    print(f"  G4  saturated cell(n_f,m_s) x K:          R^2 = {r2(ys, g4):.3f}"
          f"   [ceiling; 1-R2 = pure within-cell internals]")

    # additive-only reference with m_s alone (SPIN-9 F1 analog)
    g0, _ = anova(obs, [(1,), (2,)])
    print(f"  G0  mu + c(m_s) + b(K)  (no n_f):         R^2 = {r2(ys, g0):.3f}"
          f"   [n_f adds {r2(ys, g1) - r2(ys, g0):+.3f}]")
    g0b, _ = anova(obs, [(0,), (2,)])
    print(f"  G0b mu + a(n_f) + b(K)  (no m_s):         R^2 = {r2(ys, g0b):.3f}"
          f"   [m_s adds {r2(ys, g1) - r2(ys, g0b):+.3f}]")

    # worst G1 residuals (in-family)
    keyed = [(name, k) for name, _, grp, _ in GRAMMARS if grp != "oof"
             for k in KS]
    resid = sorted(((abs(y - p), name, k, y / 10, p / 10)
                    for (name, k), y, p in zip(keyed, ys, g1)), reverse=True)
    print("  worst G1 residuals, in-family (|pp|):")
    for r, name, k, y, p in resid[:8]:
        print(f"    {name:>11} K={k}: obs {y:.1f} fit {p:.1f} "
              f"resid {y - p:+.1f}pp")

    # out-of-family controls against G1
    print("  out-of-family controls (danger-zone lags) vs G1 prediction:")
    for name in ("g2", "stag"):
        l = LATS[name]
        for k in KS:
            p = g1_pred((fresh(l), ms_num(l), k)) / 10
            y = RES[(name, k)]["mean"] / 10
            print(f"    {name:>5} K={k}: obs {y:.1f} fit {p:.1f} "
                  f"resid {y - p:+.1f}pp  (n_f={fresh(l)}, "
                  f"m_s={ms_num(l)}/144)")

    # zero-lock control context
    print("  zero-lock spread-0 control (out of family): K=1/2/4/8 =",
          " ".join(f"{z:.1f}" for z in
                   [mean([scalars(one(ZERO, k, sd))["true_pm"]
                          for sd in SEEDS]) / 10 for k in (1, 2, 4, 8)]))


def main():
    ok = canaries()
    if not ok:
        return
    ok &= determinism_check()
    run_all()
    exp1_slices()
    exp2_stale()
    exp3_fits()
    print(f"\nelapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
