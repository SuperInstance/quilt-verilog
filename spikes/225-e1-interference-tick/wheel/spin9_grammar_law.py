#!/usr/bin/env python3
"""SPIN 9, SPOKE: GRAMMAR-LAW — the two-parameter law proposed by SPIN-5.

SPIN-5 verdict to build on: grammar is a real 18-50pp second-order dial but
no monotone majority law; K flips orderings; chatter explains the origin,
stale cross-cohort disagreement explains the grammar losses. Proposed law:
true% = f(stale-mass m_s, K).

DEFINITIONS (pinned for this spin):
  coherence threshold  c = delta/2 = 6            (delta = 12, stress)
  stale-mass           m_s = sum_i max(0, lat_i - c) / (N*(30 - c))
                       = excess lag mass above coherence, normalized so
                         that all-6-at-30 would be 1.0 (spread-30 grid
                         caps at [0,30,...,30] = 0.833 under max-min=30).
  K                    pulse replication {1,2,4,8}.

FABRIC: exp_glm1.run_fabric, unchanged (E1 contract items pinned).
Integer-only inside the loop; floats only in display statistics and in the
post-hoc law fits (PAV isotonic, additive two-way, rank-1 interaction,
Spearman/Pearson) — all computed on already-collected integers.

EXPERIMENTS
  EXP1 GRID   20 grammars at spread 30 (every grammar contains a 0 and a
              30), K in {1,2,4,8}, 5 seeds. Grammars chosen so ~15 distinct
              m_s levels span [0.167, 0.833], with deliberate STRUCTURAL
              DUPLICATES (3 grammars at m_s=1/6, 4 at m_s=7/24) to test
              whether (m_s, K) is complete. Fits: additive two-way,
              per-K isotonic (PAV), +rank-1 interaction. R^2 + failure map.
  EXP2 K-FLIP ladder / cohort / quart / outlier (+ zero-lock control)
              across K in {1,2,4,8}: rank table, pairwise inversions,
              per-grammar d(true)/dK — characterize the flip surface.
  EXP3 BUMP (priority) spread in {9..14} x {ladder, cohort} K=1;
              phase-folded residency (24 bins of reality period 240),
              per-lag fire counts split ramp-up/flat/ramp-down phase,
              event-train periodogram (periods 2..120),
              iso-spread perturbation of the ladder-12 lag set,
              delta in {10,14} co-move probe (does the bump track
              spread=delta?), 9600-tick confirmation runs.
              Discriminates: real resonance (period-locked, phase-local,
              survives iso-spread perturbation, tracks delta) vs
              instrument scar (rounding artifact of one lag set).

CANARIES (mandatory):
  A. wiring byte-identity: helper-built lats == literal lats, full
     resid+cflags traces, 5 seeds x K{1,2}.
  B. SPIN-5 replay: zero@30 K=1 per-seed permille (791,755,775,780,762)
     and ladder@30 K=1 (264,253,266,281,274) exact; events/debt in tol.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
COH = DELTA // 2          # 6
N = 6
TICKS = 4800
KS = (1, 2, 4, 8)


# ---------------------------------------------------------- grammars
def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


GRID = (  # (name, lats) — every entry max-min == 30
    ("out5_1", [0, 0, 0, 0, 0, 30]),      # m_s 24/144
    ("m6",     [0, 0, 0, 0, 6, 30]),      # 24/144  (dup m_s, structural)
    ("asy3",   [0, 0, 0, 0, 3, 30]),      # 24/144  (dup m_s, structural)
    ("m10",    [0, 0, 0, 0, 10, 30]),     # 28/144
    ("d10",    [0, 0, 0, 10, 10, 30]),    # 32/144
    ("m15",    [0, 0, 0, 0, 15, 30]),     # 33/144
    ("m20",    [0, 0, 0, 0, 20, 30]),     # 38/144
    ("m24",    [0, 0, 0, 0, 24, 30]),     # 42/144  (dup m_s x4)
    ("d15",    [0, 0, 0, 15, 15, 30]),    # 42/144
    ("g2",     [0, 4, 8, 12, 16, 30]),    # 42/144
    ("stag",   [0, 0, 0, 10, 20, 30]),    # 42/144
    ("q4_2",   [0, 0, 0, 0, 30, 30]),     # 48/144
    ("d20",    [0, 0, 0, 20, 20, 30]),    # 52/144
    ("d24",    [0, 0, 0, 24, 24, 30]),    # 60/144  (dup with ladder)
    ("ladder", [0, 6, 12, 18, 24, 30]),   # 60/144
    ("tri",    [0, 0, 15, 15, 30, 30]),   # 66/144
    ("c3_3",   [0, 0, 0, 30, 30, 30]),    # 72/144
    ("g3",     [0, 8, 16, 24, 28, 30]),   # 76/144
    ("b2_4",   [0, 0, 30, 30, 30, 30]),   # 96/144
    ("l1_5",   [0, 30, 30, 30, 30, 30]),  # 120/144
)

ZERO = [0] * N


def ms(lats):
    """Excess stale-mass, normalized (integer arithmetic; print floats)."""
    num = sum(max(0, x - COH) for x in lats)
    return num, N * (30 - COH)          # keep as fraction; display num/den


def fresh(lats):
    """Coherent fresh cohort: twins at lag <= delta/2 (read agreement
    within the deadband on every phase). The candidate THIRD parameter."""
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


def row(cells, w=8):
    return " | ".join(f"{c:>{w}}" for c in cells)


def fingerprint(r):
    return (hash(tuple(r["resid"])), hash(tuple(r["cflags"])))


def byte_identical(r1, r2):
    return (fingerprint(r1) == fingerprint(r2)
            and tuple(r1["resid"]) == tuple(r2["resid"])
            and tuple(r1["cflags"]) == tuple(r2["cflags"]))


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


def pav(levels, vals):
    """Pool-adjacent-violators isotonic (non-increasing in level order —
    hypothesis: more stale mass is worse). Returns fitted values."""
    blocks = [[v] for v in vals]
    i = 0
    while i < len(blocks) - 1:
        if mean(blocks[i]) < mean(blocks[i + 1]):   # violator (want <=)
            blocks[i] = blocks[i] + blocks[i + 1]
            del blocks[i + 1]
            while i > 0 and mean(blocks[i - 1]) < mean(blocks[i]):
                blocks[i - 1] = blocks[i - 1] + blocks[i]
                del blocks[i]
                i -= 1
        else:
            i += 1
    out = []
    for b in blocks:
        out.extend([mean(b)] * len(b))
    return out


# ---------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY A: wiring byte-identity (helper lats == literal lats) ==")
    a_ok = True
    for k in (1, 2):
        for sd in SEEDS:
            if not byte_identical(one(ladder(30), k, sd),
                                  one([0, 6, 12, 18, 24, 30], k, sd)):
                a_ok = False
                print(f"  MISMATCH K={k} seed={sd}")
    print("  PASS: 10/10 full-trace byte-identical" if a_ok else "  FAIL")
    ok &= a_ok

    print("\n== CANARY B: SPIN-5 replay (zero@30 K=1, ladder@30 K=1) ==")
    pub = (("zero@30", ZERO, 1, (791, 755, 775, 780, 762), 8756, 187834),
           ("ladder@30", [0, 6, 12, 18, 24, 30], 1,
            (264, 253, 266, 281, 274), 14952, 366275))
    b_ok = True
    for name, lats, k, pubpm, pubev, pubdbt in pub:
        res = [one(lats, k, sd) for sd in SEEDS]
        sc = [scalars(r) for r in res]
        got = tuple(x["true_pm"] for x in sc)
        ev, dbt = mean([x["events"] for x in sc]), mean([x["debt"] for x in sc])
        good = (got == pubpm and abs(ev - pubev) <= 1
                and abs(dbt - pubdbt) <= 200)
        b_ok &= good
        print(f"  {name}: per-seed {got} vs pub {pubpm}  "
              f"ev {ev:.0f}/{pubev} debt {dbt:.0f}/{pubdbt}  "
              f"{'OK' if good else 'DRIFT'}")
    print("  PASS: both anchors exact" if b_ok else "  FAIL")
    ok &= b_ok
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — results below do "
          "NOT count")
    return ok


# ---------------------------------------------------------- EXP 1
GRID_RES = {}   # (name, k) -> dict(mean true permille, seed pm, ms frac)


def exp1_grid():
    print("\n== EXP 1: (m_s, K) GRID — 20 grammars at spread 30, interference "
          "==\n(per-seed true-residency permille; m_s = excess lag mass / 144)")
    print(row(["m_s", "grammar", "lats", "K", "s1", "s7", "s42", "s1999",
               "s2s60902", "mean%", "evMean", "debtMean"], 9))
    for name, lats in GRID:
        num, den = ms(lats)
        for k in KS:
            res = [one(lats, k, sd) for sd in SEEDS]
            sc = [scalars(r) for r in res]
            tp = [x["true_pm"] for x in sc]
            GRID_RES[(name, k)] = dict(
                mean=mean(tp), seeds=tp, ms=num / den,
                ev=mean([x["events"] for x in sc]),
                dbt=mean([x["debt"] for x in sc]))
            print(row([f"{num}/{den}", name, str(lats), k] + tp +
                      [f"{mean(tp)/10:.1f}",
                       f"{GRID_RES[(name, k)]['ev']:.0f}",
                       f"{GRID_RES[(name, k)]['dbt']:.0f}"], 9))

    fit_law()


GRID_LATS = {name: lats for name, lats in GRID}


def fit_law():
    # level table: distinct m_s values
    levels = sorted({GRID_RES[(n, 1)]["ms"] for n, _ in GRID})
    names_by_level = {lv: [n for n, _ in GRID
                           if GRID_RES[(n, 1)]["ms"] == lv] for lv in levels}
    M = {}                                   # (level, k) -> cell mean
    for lv in levels:
        for k in KS:
            M[(lv, k)] = mean([GRID_RES[(n, k)]["mean"]
                               for n in names_by_level[lv]])
    gmean = mean([GRID_RES[(n, k)]["mean"] for n, _ in GRID for k in KS])

    # ---- F1: additive two-way  mu + a(level) + b(K)  (alternating means)
    a = {lv: M[(lv, 1)] - gmean for lv in levels}
    b = {k: 0.0 for k in KS}
    for _ in range(200):
        for k in KS:
            b[k] = mean([M[(lv, k)] - gmean - a[lv] for lv in levels])
        for lv in levels:
            a[lv] = mean([M[(lv, k)] - gmean - b[k] for k in KS])
    ss_t = ss_f1 = 0.0
    for name, _ in GRID:
        lv = GRID_RES[(name, 1)]["ms"]
        for k in KS:
            y = GRID_RES[(name, k)]["mean"]
            ss_t += (y - gmean) ** 2
            ss_f1 += (y - (gmean + a[lv] + b[k])) ** 2
    print("\n== EXP 1b: LAW FITS (on 80 grammar x K cells, 5-seed means) ==")
    print(f"  F1 additive  true% ~ mu + a(m_s) + b(K):   "
          f"R^2 = {1 - ss_f1 / ss_t:.3f}")
    print(f"     a(m_s) levels: " + " ".join(
        f"{a[lv]:+.0f}" for lv in levels))
    print(f"     b(K) K=1/2/4/8: " + " ".join(f"{b[k]:+.0f}" for k in KS))

    # ---- F1b: additive with FRESH-COHORT instead of m_s
    fr_levels = sorted({fresh(l) for _, l in GRID})
    Mf = {(f, k): mean([GRID_RES[(n, k)]["mean"] for n, _ in GRID
                        if fresh(GRID_LATS[n]) == f])
          for f in fr_levels for k in KS}
    af = {f: Mf[(f, 1)] - gmean for f in fr_levels}
    bf = {k: 0.0 for k in KS}
    for _ in range(200):
        for k in KS:
            bf[k] = mean([Mf[(f, k)] - gmean - af[f] for f in fr_levels])
        for f in fr_levels:
            af[f] = mean([Mf[(f, k)] - gmean - bf[k] for k in KS])
    ss_f1b = sum((GRID_RES[(n, k)]["mean"]
                  - (gmean + af[fresh(GRID_LATS[n])] + bf[k])) ** 2
                 for n, _ in GRID for k in KS)
    print(f"  F1b additive true% ~ mu + a(fresh) + b(K):  "
          f"R^2 = {1 - ss_f1b / ss_t:.3f}")
    print(f"     fresh levels {fr_levels}: " + " ".join(
        f"{af[f]:+.0f}" for f in fr_levels))
    for k in KS:
        print(f"     fresh x K={k} cell means: " + " ".join(
            f"{Mf[(f, k)] / 10:.1f}" for f in fr_levels))

    # ---- F1c: three-way additive fresh + m_s + K
    af2 = dict(af)
    ac2 = dict(a)
    b2 = {k: 0.0 for k in KS}
    for _ in range(300):
        for k in KS:
            b2[k] = mean([GRID_RES[(n, k)]["mean"] - gmean
                          - af2[fresh(GRID_LATS[n])] - ac2[GRID_RES[(n, 1)]["ms"]]
                          for n, _ in GRID])
        for f in fr_levels:
            af2[f] = mean([GRID_RES[(n, k)]["mean"] - gmean - b2[k]
                           - ac2[GRID_RES[(n, 1)]["ms"]]
                           for n, _ in GRID if fresh(GRID_LATS[n]) == f
                           for k in KS])
        for lv in levels:
            ac2[lv] = mean([GRID_RES[(n, k)]["mean"] - gmean - b2[k]
                            - af2[fresh(GRID_LATS[n])]
                            for n, _ in GRID if GRID_RES[(n, 1)]["ms"] == lv
                            for k in KS])
    ss_f1c = sum((GRID_RES[(n, k)]["mean"]
                  - (gmean + af2[fresh(GRID_LATS[n])]
                     + ac2[GRID_RES[(n, 1)]["ms"]] + b2[k])) ** 2
                 for n, _ in GRID for k in KS)
    print(f"  F1c additive true% ~ mu + a(fresh) + c(m_s) + b(K):  "
          f"R^2 = {1 - ss_f1c / ss_t:.3f}")
    print(f"     a(fresh): " + " ".join(f"{af2[f]:+.0f}" for f in fr_levels)
          + f"   c(m_s): " + " ".join(f"{ac2[lv]:+.0f}" for lv in levels)
          + f"   b(K): " + " ".join(f"{b2[k]:+.0f}" for k in KS))

    # ---- F2: per-K isotonic in m_s (non-increasing)
    pooled_ss = isot_ss = 0.0
    for k in KS:
        ys = [M[(lv, k)] for lv in levels]
        fit = pav(levels, ys)
        ssr = sum((y - f) ** 2 for y, f in zip(ys, fit))
        sst = sum((y - mean(ys)) ** 2 for y in ys)
        pooled_ss += sst
        isot_ss += ssr
        # violations = pooled blocks
        nviol = sum(1 for i in range(len(levels) - 1)
                    if fit[i] == fit[i + 1] and ys[i] < ys[i + 1])
        sr = spearman(levels, ys)
        print(f"  F2 K={k}: isotonic R^2 = {1 - ssr / sst:.3f}  "
              f"Spearman(m_s, true) = {sr:+.2f}  pooled-steps {nviol}")
    print(f"  F2 pooled isotonic R^2 = {1 - isot_ss / pooled_ss:.3f}")

    # ---- F3: rank-1 interaction on residual of F1 (power iteration)
    # cell-level: pred = gmean + a + b + u[level]*v[K]  (proper nesting)
    E = [[M[(lv, k)] - gmean - a[lv] - b[k] for k in KS] for lv in levels]
    u = [1.0] * len(levels)
    for _ in range(100):
        unew = [sum(E[i][j] * u[i] for j in range(len(KS)))
                for i in range(len(levels))]
        nrm = sum(x * x for x in unew) ** 0.5 or 1.0
        u = [x / nrm for x in unew]
    v = [sum(E[i][j] * u[i] for i in range(len(levels))) for j in
         range(len(KS))]
    sig = sum(u[i] * E[i][j] * v[j] for i in range(len(levels))
              for j in range(len(KS)))
    uu = u if sig >= 0 else [-x for x in u]
    vv = v if sig >= 0 else [-x for x in v]
    ss_f3 = sum((GRID_RES[(n, k)]["mean"]
                 - (gmean + a[GRID_RES[(n, 1)]["ms"]] + b[k]
                    + uu[levels.index(GRID_RES[(n, 1)]["ms"])]
                    * vv[KS.index(k)])) ** 2
                 for n, _ in GRID for k in KS)
    print(f"  F3 F1 + rank-1 interaction:               "
          f"R^2 = {1 - ss_f3 / ss_t:.3f}")

    # ---- failure map
    print("\n== EXP 1c: FAILURE MAP ==")
    # structural duplicates: within-level spread vs seed noise
    for lv in levels:
        nms = names_by_level[lv]
        if len(nms) < 2:
            continue
        for k in (1, 8):
            vals = {n: GRID_RES[(n, k)]["mean"] / 10 for n in nms}
            spread = max(vals.values()) - min(vals.values())
            # seed noise: max per-seed swing of a single grammar
            noise = max(max(GRID_RES[(n, k)]["seeds"])
                        - min(GRID_RES[(n, k)]["seeds"]) for n in nms) / 10
            print(f"  m_s={lv:.3f} K={k}: grammars "
                  + ", ".join(f"{n} {v:.1f}" for n, v in vals.items())
                  + f"  within-spread {spread:.1f}pp (seed swing ~{noise:.0f}pp)")

    # worst F1 residuals
    resid = []
    for name, _ in GRID:
        lv = GRID_RES[(name, 1)]["ms"]
        for k in KS:
            y = GRID_RES[(name, k)]["mean"]
            resid.append((abs(y - (gmean + a[lv] + b[k])), name, k,
                          y / 10, (gmean + a[lv] + b[k]) / 10))
    resid.sort(reverse=True)
    print("  worst additive-fit residuals (|pp|):")
    for r, name, k, y, f in resid[:8]:
        print(f"    {name:>7} K={k}: obs {y:.1f} fit {f:.1f} "
              f"resid {y - f:+.1f}pp")


# ---------------------------------------------------------- EXP 2
def exp2_kflip():
    print("\n== EXP 2: K-FLIP SURFACE (spread-30 interference, 5-seed mean "
          "%; zero-lock is the spread-0 control) ==")
    sel = [g for g in GRID if g[0] in
           ("ladder", "c3_3", "q4_2", "out5_1", "m24", "d24")]
    print(row(["grammar", "lats", "m_s", "fresh"] + [f"K={k}" for k in KS]
              + ["dK81"], 9))
    table = {}
    for name, lats in sel:
        num, den = ms(lats)
        vals = [GRID_RES[(name, k)]["mean"] / 10 for k in KS]
        table[name] = vals
        print(row([name, str(lats), f"{num}/{den}", fresh(lats)] +
                  [f"{v:.1f}" for v in vals] +
                  [f"{vals[-1]-vals[0]:+.1f}"], 9))
    zvals = []
    for k in KS:
        res = [one(ZERO, k, sd) for sd in SEEDS]
        zvals.append(mean([scalars(r)["true_pm"] for r in res]) / 10)
    table["zero0"] = zvals
    print(row(["zero0", "[0]*6", "0/144", 6] + [f"{v:.1f}" for v in zvals] +
              [f"{zvals[-1]-zvals[0]:+.1f}"], 9))
    names = list(table)
    for kx, ky in ((1, 2), (2, 4), (4, 8), (1, 8)):
        i, j = KS.index(kx), KS.index(ky)
        inv = 0
        for a_i in range(len(names)):
            for b_i in range(a_i + 1, len(names)):
                s_a = (table[names[a_i]][i] - table[names[b_i]][i])
                s_b = (table[names[a_i]][j] - table[names[b_i]][j])
                if s_a * s_b < 0:
                    inv += 1
        sr = spearman([table[n][i] for n in names],
                      [table[n][j] for n in names])
        print(f"  K {kx}->{ky}: pairwise rank inversions {inv}/15  "
              f"Spearman = {sr:+.2f}")
    print("  Spin-5 claim check: zero0 falls 77.3->50.0 by K=2; "
          "which spread-30 grammars RISE with K?")
    for n in names:
        v = table[n]
        if v[-1] > v[0]:
            print(f"    RISING: {n}: " + " ".join(f"{x:.1f}" for x in v))


# ---------------------------------------------------------- EXP 3
def phase_of(t):
    p = t % 240
    return "up" if p < 96 else ("flat" if p < 144 else "down")


def exp3_bump():
    print("\n== EXP 3a: THE SPREAD=12 BUMP — spread 9..14, K=1, 5 seeds ==")
    print(row(["spread", "grammar", "lats", "s1", "s7", "s42", "s1999",
               "s2s60902", "mean%", "evMean", "debtMean", "canc"], 9))
    bump = {}
    for s in (9, 10, 11, 12, 13, 14):
        for gname, glats in (("ladder", ladder(s)),
                             ("cohort", [0, 0, 0, s, s, s])):
            res = [one(glats, 1, sd) for sd in SEEDS]
            sc = [scalars(r) for r in res]
            tp = [x["true_pm"] for x in sc]
            bump[(gname, s)] = dict(res=res, mean=mean(tp), lats=glats)
            print(row([s, gname, str(glats)] + tp +
                      [f"{mean(tp)/10:.1f}",
                       f"{mean([x['events'] for x in sc]):.0f}",
                       f"{mean([x['debt'] for x in sc]):.0f}",
                       f"{mean([x['cancels'] for x in sc]):.0f}"], 9))
    for gname in ("ladder", "cohort"):
        m = {s: bump[(gname, s)]["mean"] / 10 for s in (9, 10, 11, 12, 13, 14)}
        peak = max(m, key=m.get)
        print(f"  {gname}: local structure " +
              " ".join(f"{s}:{v:.1f}" for s, v in m.items()) +
              f"  peak at spread={peak}")

    print("\n== EXP 3b: phase-folded residency (ladder, K=1, pooled 5 seeds; "
          "24 bins of 10 over reality period 240) ==")
    print(row(["phaseBin", "w11", "w12", "w13", "ev11", "ev12", "ev13"], 9))
    fold = {}
    for s in (11, 12, 13):
        within = [0] * 24
        evs = [0] * 24
        for r in bump[("ladder", s)]["res"]:
            for t, x in enumerate(r["resid"]):
                if x <= DELTA:
                    within[t % 240 // 10] += 1
            for (t, i, pm, e) in r["emissions"]:
                evs[t % 240 // 10] += 1
        fold[s] = (within, evs)
        tot_ev = sum(evs)
        print(f"  spread {s}: total events {tot_ev}  flat-phase share "
              f"{sum(evs[9:15]) / max(1, tot_ev):.2f}  "
              f"ramp share {1 - sum(evs[9:15]) / max(1, tot_ev):.2f}")
    for b_ in range(24):
        print(row([b_ * 10] + [f"{fold[s][0][b_] / 50:.0%}" if False else
                               f"{1000 * fold[s][0][b_] // (50 * 10 * 5)}‰"
                               for s in (11, 12, 13)] +
                  [f"{fold[s][1][b_] // 5}" for s in (11, 12, 13)], 9))

    print("\n== EXP 3c: per-lag fire counts by phase (ladder K=1, 5-seed "
          "sum; phases: up<96 flat 96-143 down>=144 of t%240) ==")
    for s in (11, 12, 13):
        lats = bump[("ladder", s)]["lats"]
        cnt = {i: {"up": 0, "flat": 0, "down": 0} for i in range(N)}
        for r in bump[("ladder", s)]["res"]:
            for (t, i, pm, e) in r["emissions"]:
                cnt[i][phase_of(t)] += 1
        print(f"  spread {s} lats {lats}:")
        for i in range(N):
            c = cnt[i]
            tot = c["up"] + c["flat"] + c["down"]
            print(f"    lag {lats[i]:>2}: fires {tot:>6}  "
                  f"up {c['up']:>5} flat {c['flat']:>5} down {c['down']:>5}")

    print("\n== EXP 3d: event-train periodogram (ladder K=1 seed 1, 9600 "
          "ticks; folded-count variance ratio for periods 2..120) ==")
    for s in (11, 12, 13):
        r = one(bump[("ladder", s)]["lats"], 1, SEEDS[0], ticks=9600)
        train = [0] * 9600
        for (t, i, pm, e) in r["emissions"]:
            train[t] = 1
        nev = sum(train)
        scored = []
        for p in range(2, 121):
            bins = [0] * p
            for t in range(9600):
                if train[t]:
                    bins[t % p] += 1
            mu = nev / p
            var = sum((x - mu) ** 2 for x in bins) / p
            scored.append((var / mu if mu else 0, p, 240 % p == 0))
        scored.sort(reverse=True)
        top = [(p, f"{v:.1f}") for v, p, _ in scored[:6]]
        div240 = [(p, f"{v:.1f}") for v, p, d in scored if d][:4]
        print(f"  spread {s}: events {nev}  top6 periods {top}  "
              f"divisors-of-240 {div240}")
        # long-run true% at 9600
        print(f"    9600-tick true% = "
              f"{within_pm(r['resid'], DELTA) / 10:.1f}")

    print("\n== EXP 3e: iso-spread perturbation at spread 12 (K=1) — does "
          "the bump belong to the SPREAD or the lag SET? ==")
    isos = (("isoA_round", [0, 2, 5, 7, 10, 12]),
            ("isoB", [0, 3, 5, 8, 11, 12]),
            ("isoC", [0, 2, 4, 7, 9, 12]),
            ("isoD", [0, 1, 4, 7, 10, 12]),
            ("isoE_nodiv", [0, 2, 5, 7, 11, 12]))
    print(row(["set", "lats", "div240", "s1", "s7", "s42", "s1999",
               "s2s60902", "mean%"], 9))
    for nm, lats in isos:
        res = [one(lats, 1, sd) for sd in SEEDS]
        tp = [scalars(r)["true_pm"] for r in res]
        d240 = all(x == 0 or 240 % x == 0 for x in lats if x > 0)
        print(row([nm, str(lats), d240] + tp + [f"{mean(tp)/10:.1f}"], 9))
    for s in (10, 13):
        res = [one(ladder(s), 1, sd) for sd in SEEDS]
        tp = [scalars(r)["true_pm"] for r in res]
        print(row([f"ladder{s}ref", str(ladder(s)), "-"] + tp +
                  [f"{mean(tp)/10:.1f}"], 9))

    print("\n== EXP 3f: delta co-move probe — does the bump sit at "
          "spread=delta? (ladder K=1) ==")
    d12 = {s: bump[("ladder", s)]["mean"] / 10 for s in (9, 10, 11, 12, 13, 14)}
    print(f"  delta=12 (from 3a): " +
          " ".join(f"{s}:{v:.1f}" for s, v in d12.items()))
    for d in (10, 14):
        print(f"  delta={d}:")
        print(row(["spread", "lats", "mean%", "mark"], 9))
        for s in (9, 10, 11, 12, 13, 14):
            res = [one(ladder(s), 1, sd, delta=d) for sd in SEEDS]
            tp = [scalars(r, d)["true_pm"] for r in res]
            print(row([s, str(ladder(s)), f"{mean(tp)/10:.1f}",
                       "<== spread=delta" if s == d else ""], 9))
    print("  dip localization: deepest LOCAL dip over 9..13 (below both "
          "neighbors) per delta:")
    print(f"    delta=12: {min((s for s in (10, 11, 12, 13)),
                       key=lambda s: d12[s] - max(d12[s-1], d12[s+1]))} "
          f"(10 is below BOTH neighbors by "
          f"{max(d12[9], d12[11]) - d12[10]:.1f}pp vs max neighbor)")


if __name__ == "__main__":
    ok = canaries()
    if ok:
        exp1_grid()
        exp2_kflip()
        exp3_bump()
    else:
        print("ABORT: canaries failed — no results collected.")
