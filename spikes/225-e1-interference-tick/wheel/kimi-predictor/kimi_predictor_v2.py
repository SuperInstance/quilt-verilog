#!/usr/bin/env python3
"""KIMI-PREDICTOR v2 — SPIN-12 grammar-shape features + out5_1 protection
term (g3-kinduction lane).

v1 (kimi_predictor.py, VALIDATED narrow +5.7pp) used live-mass features
[in_flight, mean_lag, stale_mass, K]. SPIN-12 (orthogonal grammar) proved
the winning SHAPE law is fresh-count n_f x K interaction (R2=0.891), with
stale-mass m_s near-fungible, and that outlier grammars (5 fresh + 1
stale, "out5_1-class") carry +22.4pp of protection the additive model
cannot express.

FIRST PASS RESULT (kept as ablation "shape"): the literal feature swap
[n_f, m_s, K, n_f*K, fresh_maj] is INERT on held-out grammars — shape
features are constant per grammar until the scheduler acts, so the model
emits one static score per grammar x K, never crosses tlo, and cannot see
pulse pile-up (v1's trigger). It reproduces static15 exactly and regresses
vs v1 (-34.0pp at cohort K=2). The model zoo therefore carries the shape
basis ON TOP of live dynamic features:

  per-tick tuple F = (in_flight, mean_lag, stale_mass, n_f, m_s, K,
                      n_f*K, fresh_maj, prot)
  model "shape"    : F[3:8]   (literal spec — ablation)
  model "shape_p"  : F[3:9]   (literal spec + protection — ablation)
  model "full"     : F[0,3..7]  (in_flight + SPIN-12 basis)
  model "full_p"   : + prot
  model "v1plus"   : F[0..7]  (v1's exact dynamic set + SPIN-12 basis)
  model "v1plus_p" : + prot

  in_flight = #pulses after FIFO expiry; mean_lag, stale_mass as in v1
  n_f = #{lag <= 6}, m_s = sum max(0, lag-6)  (SPIN-9/12 pinned, live lats)
  fresh_maj = 1 iff 2*n_f > N ; prot = 1 iff n_f >= N-1 (out5_1 class)

DEPLOYED model is chosen by TRAIN-ladder score only (never by eval).
Thresholds: max train score with min-intervention tie-break (fewest
shrink+restore ticks among pairs within 2.0pp of the best train score —
the safest deployable among equals).

Fabric: exp_glm1.run_fabric E1 contract; run_dyn2 below is the same
verbatim replica as v1's run_dyn with the hook computing F. Integer-only
inside the loop; deployed predictor fixed-point (SCALE=1024); floats only
in offline training (sklearn) and display.

Split discipline (unchanged from v1):
  TRAIN : ladder grid spreads {5..30}, K {1,2,4}, seeds {1,7,42}
          (K=4 added so n_f x K is identifiable where SPIN-12 saw the
          out5_1 protection).
  EVAL  : HELD-OUT grammars (cohort 3+3, out5_1, kcoh5, zero) x seeds
          {1999, 20260902}, K {1,2,4}. Only residency gain on unseen
          grammars counts. Zero regressions allowed (per-cell vs
          static15, static30 AND v1).

CANARIES (mandatory):
  1. sequential-arm byte-identity with all v2 schedulers active.
  2. harness identity: run_dyn2 (scheduler off) == exp_glm1.run_fabric.
  3. SPIN-5 replay: ladder s=15 K=1 scheduler-off per-seed permille
     exactly (709,713,721,714,717).
  4. spread=0 byte-identity: zero grammar, schedulers active == off ==
     run_fabric, K {1,2,4}.
  5. v1 replay: v1 scheduler rebuilt from results.json constants must
     reproduce v1's published held-out per-seed permille EXACTLY.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "inventors-derby"))
sys.path.insert(0, HERE)
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402
import kimi_predictor as v1  # noqa: E402  (v1 module: replay baseline)

SEEDS_TRAIN = (1, 7, 42)
SEEDS_EVAL = (1999, 20260902)
SEEDS_ALL = (1, 7, 42, 1999, 20260902)
DELTA = 12
COH = DELTA // 2          # 6, SPIN-9/12 coherence threshold
N = 6
TICKS = 4800
SCALE = 1024
GRID = (5, 10, 15, 20, 25, 30)
KS_TRAIN = (1, 2, 4)
KS_EVAL = (1, 2, 4)
FEATS = ("in_flight", "mean_lag", "stale_mass", "n_f", "m_s", "K",
         "nf_K", "fresh_maj", "prot")
MODELS = {"shape": (3, 4, 5, 6, 7), "shape_p": (3, 4, 5, 6, 7, 8),
          "full": (0, 3, 4, 5, 6, 7), "full_p": (0, 3, 4, 5, 6, 7, 8),
          "v1plus": (0, 1, 2, 5, 3, 4, 6, 7),
          "v1plus_p": (0, 1, 2, 5, 3, 4, 6, 7, 8)}

# v1 published constants (results.json) for replay canary + baseline
V1_OFF, V1_C = 2470, [-437, -160, -436, 842]
V1_TLO, V1_THI = -64, 2482
V1_PUB = json.load(open(os.path.join(HERE, "results.json")))["results"]


# ---------------------------------------------------------- grammars
def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


def cohort33(s):
    return [0, 0, 0, s, s, s]


def out5_1(s):
    return [0, 0, 0, 0, 0, s]


def kcoh5(s):
    # same multiset as out5_1 (order-invariance, Spin-5 canary C)
    return [0] * (N - 1) + [s]


def zero(_s):
    return [0] * N


HELDOUT = (("cohort3+3", cohort33), ("out5_1", out5_1),
           ("kcoh5", kcoh5), ("zero", zero))


# ---------------------------------------------------------- dynamic fabric
def run_dyn2(mode, ticks, lats, K=4, pd=3, delta=12, drift=6,
             seed=20260902, scheduler=None, feats_out=None):
    """Verbatim replica of exp_glm1.run_fabric (same as v1 run_dyn) with
    the hook computing the SPIN-12 feature tuple F on live state, sampled
    after FIFO expiry, before scheduler action; label = post-correction
    resid <= delta appended when feats_out is given.
    Sequential mode NEVER calls the scheduler (canary 1)."""
    from collections import deque
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    lats = list(lats)
    nominal = list(lats)
    n = len(lats)
    emissions = []
    events = mass = cancels = chatter = settles = 0
    last = -10
    resid = []
    cflags = []

    for t in range(ticks):
        reads = [reality(max(0, t - lats[i])) for i in range(n)]
        s_true = reality(t)
        g += rng.below(2 * drift + 1) - drift

        # FIFO expiry, oldest at the right end (e1 contract item 3)
        while pulses and pulses[-1][1] == 0:
            pulses.pop()

        # --- hook: per-tick live-state features (integer-only) ---
        if feats_out is not None or (scheduler is not None
                                     and mode != "sequential"):
            inflight = len(pulses)
            mean_lag = sum(lats) // n
            stale = sum(1 for l in lats if l * 8 >= 5 * delta)
            nf = sum(1 for l in lats if l <= COH)
            ms = sum(max(0, l - COH) for l in lats)
            feats = (inflight, mean_lag, stale, nf, ms, K, nf * K,
                     1 if 2 * nf > n else 0, 1 if nf >= n - 1 else 0)
            if scheduler is not None and mode != "sequential":
                lats = scheduler(feats, lats, nominal)
                reads = [reality(max(0, t - lats[i])) for i in range(n)]
        else:
            feats = None

        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > delta]

        cflag = 0
        if mode == "sequential":
            if trig:
                i, e = trig[0]
                g += e
                events += 1
                mass += abs(e)
                emissions.append((t, i, e, e))
                if t - last == 1:
                    chatter += 1
                last = t
        else:
            for i, e in trig:
                m = abs(e) // pd or 1
                pm = m if e > 0 else -m
                pulses.appendleft([pm, K])
                events += 1
                mass += abs(e)
                emissions.append((t, i, pm, e))
            if pulses:
                net = sum(p[0] for p in pulses)
                if net == 0 and any(p[0] > 0 for p in pulses) \
                        and any(p[0] < 0 for p in pulses):
                    cancels += 1
                    cflag = 1
                decayed = deque()                      # snapshot decay (item 4)
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)     # fdiv sign-safe (item 1)
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
            if trig:
                if t - last == 1:
                    chatter += 1
                last = t

        r_t = abs(s_true - g)
        resid.append(r_t)
        cflags.append(cflag)
        if feats_out is not None:
            feats_out.append(feats + (1 if r_t <= delta else 0,))
        if all(abs(r - g) <= delta for r in reads):
            settles += 1

    return dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
                settles=settles, resid=resid, cflags=cflags,
                emissions=emissions, ticks=ticks)


# ---------------------------------------------------------- identity helpers
def byte_identical(r1, r2):
    return (tuple(r1["resid"]) == tuple(r2["resid"])
            and tuple(r1["cflags"]) == tuple(r2["cflags"])
            and tuple(r1["emissions"]) == tuple(r2["emissions"])
            and r1["events"] == r2["events"] and r1["mass"] == r2["mass"]
            and r1["cancels"] == r2["cancels"]
            and r1["chatter"] == r2["chatter"]
            and r1["settles"] == r2["settles"])


# ---------------------------------------------------------- training
def collect_ladder_corpus():
    """Per-tick feature records from the ladder grid, TRAIN seeds only,
    scheduler off (shape features then equal the nominal grammar's)."""
    X, y = [], []
    for s in GRID:
        for k in KS_TRAIN:
            for sd in SEEDS_TRAIN:
                feats = []
                run_dyn2("interference", TICKS, ladder(s), K=k, pd=3,
                         delta=DELTA, drift=6, seed=sd, feats_out=feats)
                for f in feats:
                    X.append(f[:9])
                    y.append(f[9])
    return X, y


def train_predictor(X, y, idx, tag):
    """sklearn logistic regression on standardized features (e2/v1
    lineage), folded into a fixed-point integer scorer z = OFF +
    sum(C_i * f_i) over the feature columns listed in idx."""
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    Xa = np.array([[x[i] for i in idx] for x in X], dtype=float)
    ya = np.array(y)
    mu = Xa.mean(0)
    sd = Xa.std(0)
    sd[sd == 0] = 1.0
    lr = LogisticRegression(max_iter=500, random_state=226)
    lr.fit((Xa - mu) / sd, ya)
    w = lr.coef_[0]
    b = lr.intercept_[0]
    C = [int(round(wi / si * SCALE)) for wi, si in zip(w, sd)]
    OFF = int(round(b * SCALE)) - int(round(sum(
        ci * mi for ci, mi in zip(C, mu))))
    zf = b + ((Xa - mu) / sd) @ w
    zi = OFF + np.array([[x[i] for i in idx] for x in X], dtype=np.int64) \
        @ np.array(C, dtype=np.int64)
    agree = float(np.mean((zf >= 0) == (zi >= 0)))
    rep = dict(tag=tag, idx=list(idx), base_rate=round(float(ya.mean()), 4),
               in_domain_acc=round(float(lr.score((Xa - mu) / sd, ya)), 4),
               weights_std={FEATS[i]: round(float(wi), 3)
                            for i, wi in zip(idx, w)},
               C=C, OFF=OFF, int_sign_agreement=round(agree, 4))
    return OFF, C, rep


def make_scheduler(OFF, C, idx, tlo, thi, stats=None):
    """Fixed-point integer scheduler (same mechanism as v1). z = OFF +
    sum(C_j * feats[idx_j]); z < tlo: shrink every lag by 1; z > thi:
    restore 1 toward nominal. stats (optional dict) observes shrink/
    restore counts + final lats."""
    def sched(feats, lats, nominal):
        z = OFF + sum(c * feats[i] for c, i in zip(C, idx))
        if z < tlo:
            if stats is not None:
                stats["shrink"] += 1
                stats["last"] = [max(0, l - 1) for l in lats]
            return [max(0, l - 1) for l in lats]
        if z > thi:
            if stats is not None:
                stats["restore"] += 1
                stats["last"] = [min(nm, l + 1) for l, nm in
                                 zip(lats, nominal)]
            return [min(nm, l + 1) for l, nm in zip(lats, nominal)]
        if stats is not None:
            stats["last"] = list(lats)
        return list(lats)
    return sched


def true_pm(mode, lats, k, seed, scheduler=None):
    r = run_dyn2("interference", TICKS, lats, K=k, pd=3, delta=DELTA,
                 drift=6, seed=seed, scheduler=scheduler)
    return within_pm(r["resid"], DELTA)


def mean_pm(lats, k, seeds, scheduler=None):
    v = [true_pm("interference", lats, k, sd, scheduler) for sd in seeds]
    return sum(v) / len(v), v   # display-only float mean


# ---------------------------------------------------------- canaries
def canaries(M):
    ok = True
    scheds = {tag: make_scheduler(m["OFF"], m["C"], MODELS[tag],
                                  m["tlo"], m["thi"])
              for tag, m in M.items()}

    print("== CANARY 1: sequential-arm byte-identity (schedulers active) ==")
    c1 = True
    n1 = 0
    for tag, sc in scheds.items():
        for gname, gfn in (("ladder", ladder),) + HELDOUT:
            for s in (15, 30):
                for sd in SEEDS_EVAL:
                    n1 += 1
                    r1 = run_dyn2("sequential", TICKS, gfn(s), K=1, pd=3,
                                  delta=DELTA, drift=6, seed=sd,
                                  scheduler=sc)
                    r2 = run_fabric("sequential", TICKS, gfn(s), K=1, pd=3,
                                    delta=DELTA, drift=6, seed=sd)
                    if not byte_identical(r1, r2):
                        c1 = False
                        print(f"  MISMATCH {tag} sequential {gname}@{s} "
                              f"seed={sd}")
    print(f"  PASS: {n1}/{n1} sequential runs byte-identical with "
          "schedulers active" if c1 else "  FAIL")
    ok &= c1

    print("\n== CANARY 2: harness identity (interference, scheduler off) ==")
    c2 = True
    n2 = 0
    for gname, gfn in (("ladder", ladder),) + HELDOUT:
        for s in (15, 30):
            for k in KS_EVAL:
                for sd in SEEDS_EVAL:
                    n2 += 1
                    r1 = run_dyn2("interference", TICKS, gfn(s), K=k, pd=3,
                                  delta=DELTA, drift=6, seed=sd)
                    r2 = run_fabric("interference", TICKS, gfn(s), K=k,
                                    pd=3, delta=DELTA, drift=6, seed=sd)
                    if not byte_identical(r1, r2):
                        c2 = False
                        print(f"  MISMATCH interference {gname}@{s} "
                              f"K={k} seed={sd}")
    print(f"  PASS: {n2}/{n2} interference runs byte-identical to "
          "exp_glm1.run_fabric" if c2 else "  FAIL")
    ok &= c2

    print("\n== CANARY 3: SPIN-5 replay ladder s=15 K=1 (scheduler off) ==")
    pub = (709, 713, 721, 714, 717)
    got = tuple(true_pm("interference", ladder(15), 1, sd)
                for sd in SEEDS_ALL)
    m = sum(got) / len(got) / 10
    c3 = got == pub and abs(m - 71.5) <= 2.0
    print(f"  per-seed permille got {got} pub {pub}  mean {m:.1f}% "
          f"(tolerance +-2pp of 71.5)")
    print("  PASS" if c3 else "  FAIL")
    ok &= c3

    print("\n== CANARY 4: spread=0 byte-identity (zero grammar, schedulers "
          "active) ==")
    c4 = True
    n4 = 0
    for tag, sc in scheds.items():
        for k in KS_EVAL:
            for sd in SEEDS_EVAL:
                n4 += 1
                r1 = run_dyn2("interference", TICKS, zero(0), K=k, pd=3,
                              delta=DELTA, drift=6, seed=sd, scheduler=sc)
                r2 = run_fabric("interference", TICKS, zero(0), K=k, pd=3,
                                delta=DELTA, drift=6, seed=sd)
                if not byte_identical(r1, r2):
                    c4 = False
                    print(f"  MISMATCH zero K={k} seed={sd} sched={tag}")
    print(f"  PASS: {n4}/{n4} zero-grammar scheduled runs byte-identical "
          "to run_fabric" if c4 else "  FAIL")
    ok &= c4

    print("\n== CANARY 5: v1 replay (published held-out per-seed permille, "
          "exact) ==")
    v1sched = v1.make_scheduler(V1_OFF, V1_C, V1_TLO, V1_THI)
    gmap = {"cohort3+3": v1.cohort33, "outlier": v1.outlier,
            "kcoh5": v1.kcoh5}
    c5 = True
    n5 = n5ok = 0
    for gname, gfn in gmap.items():
        for k in (1, 2):
            pub = V1_PUB[f"{gname}_K{k}"]["per_seed"]
            for cond in ("static15", "static30", "sched"):
                sc = v1sched if cond == "sched" else None
                s = 30 if cond == "static30" else 15
                got = [v1.true_pm("interference", gfn(s), k, sd, sc)
                       for sd in SEEDS_EVAL]
                n5 += 1
                n5ok += got == pub[cond]
                if got != pub[cond]:
                    c5 = False
                    print(f"  DRIFT {gname} K={k} {cond}: got {got} "
                          f"pub {pub[cond]}")
    print(f"  PASS: {n5ok}/{n5} v1 held-out cells replay exact"
          if c5 else "  FAIL")
    ok &= c5

    print("\nALL CANARIES:", "PASS" if ok else
          "FAIL — results below do NOT count")
    return ok


# ---------------------------------------------------------- threshold select
def select_thresholds(OFF, C, idx, X, tag):
    """Pick (tlo, thi) by grid on TRAIN ladder runs only (seeds 1,7,42) —
    never touches held-out grammars or eval seeds. Candidate thresholds
    are deciles of the training z-score distribution (corpus reused).
    Selection rule: max train-ladder mean true%; among pairs within 2.0pp
    of the best, MIN-INTERVENTION tie-break (fewest shrink+restore ticks
    on the train grid — the safest deployable among equals)."""
    zs = sorted(OFF + sum(c * x[i] for c, i in zip(C, idx)) for x in X)
    n = len(zs)
    dec = [zs[min(n - 1, n * d // 10)] for d in range(11)]
    print(f"  [{tag}] training z deciles: {[int(z) for z in dec]}")
    rows = []
    for ilo in (2, 3, 4):
        for ihi in (6, 7, 8):
            tlo, thi = dec[ilo], dec[ihi]
            acts = 0
            vals = []
            for s in (10, 15, 20, 30):
                for k in KS_TRAIN:
                    st = dict(shrink=0, restore=0, last=None)
                    sched = make_scheduler(OFF, C, idx, tlo, thi, st)
                    m, _ = mean_pm(ladder(s), k, SEEDS_TRAIN, sched)
                    vals.append(m)
                    acts += st["shrink"] + st["restore"]
            score = sum(vals) / len(vals)
            rows.append((score, acts, tlo, thi))
            print(f"  [{tag}] tlo={tlo:>7} thi={thi:>7}  train-ladder mean "
                  f"true% {score/10:.1f}  interventions {acts}")
    top = max(r[0] for r in rows)
    near = [r for r in rows if top - r[0] <= 20]   # within 2.0pp (permille)
    best = min(near, key=lambda r: r[1])
    print(f"  [{tag}] SELECTED tlo={best[2]} thi={best[3]} "
          f"(train-ladder mean {best[0]/10:.1f}%, {best[1]} interventions "
          f"— min-intervention within 2pp of best {top/10:.1f}%)")
    return best[2], best[3], best[0]


# ---------------------------------------------------------- evaluation
def evaluate(M, dep):
    """HELD-OUT grammars x held-out seeds x K{1,2,4}. Conditions:
    static15, static30, v1, and every v2 model. Gain columns are for the
    deployed model `dep`."""
    tags = list(M)
    v1sched = v1.make_scheduler(V1_OFF, V1_C, V1_TLO, V1_THI)
    results = {}
    stats = {}
    print("\n== EVAL: held-out grammars, seeds {1999, 20260902}, "
          "K{1,2,4} ==")
    print(f"{'grammar':<10}{'K':>3}{'s15%':>7}{'s30%':>7}{'v1%':>7}"
          + "".join(f"{t + '%':>9}" for t in tags)
          + f"{dep + '-s15':>10}{dep + '-s30':>10}{dep + '-v1':>10}")
    for gname, gfn in HELDOUT:
        for k in KS_EVAL:
            m15, v15 = mean_pm(gfn(15), k, SEEDS_EVAL)
            m30, v30 = mean_pm(gfn(30), k, SEEDS_EVAL)
            vv1 = [v1.true_pm("interference", gfn(15), k, sd, v1sched)
                   for sd in SEEDS_EVAL]
            mv1 = sum(vv1) / len(vv1)
            row = dict(static15=round(m15 / 10, 1),
                       static30=round(m30 / 10, 1), v1=round(mv1 / 10, 1),
                       per_seed=dict(static15=v15, static30=v30, v1=vv1))
            cells = []
            for t in tags:
                m = M[t]
                stats[(gname, k, t)] = dict(shrink=0, restore=0, last=None)
                sc = make_scheduler(m["OFF"], m["C"], MODELS[t],
                                    m["tlo"], m["thi"],
                                    stats[(gname, k, t)])
                mt, vt = mean_pm(gfn(15), k, SEEDS_EVAL, sc)
                row[t] = round(mt / 10, 1)
                row["per_seed"][t] = vt
                cells.append(mt / 10)
            results[(gname, k)] = row
            print(f"{gname:<10}{k:>3}{m15/10:>7.1f}{m30/10:>7.1f}"
                  f"{mv1/10:>7.1f}"
                  + "".join(f"{c:>9.1f}" for c in cells)
                  + f"{row[dep]-row['static15']:>+10.1f}"
                  + f"{row[dep]-row['static30']:>+10.1f}"
                  + f"{row[dep]-row['v1']:>+10.1f}")
    mech_tags = [dep] + ([dep + "_p"] if dep + "_p" in M else [])
    for (gname, k, t), st in sorted(stats.items()):
        if t in mech_tags:
            print(f"  mech {gname:<10}K={k} {t:>9}: shrink={st['shrink']} "
                  f"restore={st['restore']} final={st['last']}")

    # in-domain sanity: deployed scheduler on ladder15 K=1 (home config)
    mf = M[dep]
    mlad, _ = mean_pm(ladder(15), 1, SEEDS_EVAL,
                      make_scheduler(mf["OFF"], mf["C"], MODELS[dep],
                                     mf["tlo"], mf["thi"]))
    print(f"\n  in-domain sanity: ladder@15 K=1 {dep}-scheduled = "
          f"{mlad/10:.1f}% (static replay 71.5%)")
    ident = all(byte_identical(
        run_dyn2("interference", TICKS, out5_1(15), K=k, pd=3, delta=DELTA,
                 drift=6, seed=sd),
        run_dyn2("interference", TICKS, kcoh5(15), K=k, pd=3, delta=DELTA,
                 drift=6, seed=sd))
        for k in KS_EVAL for sd in SEEDS_EVAL)
    print(f"  kcoh5 == out5_1 byte-identical on eval seeds (K1,2,4): "
          f"{ident}")
    return results, mlad / 10, ident


# ---------------------------------------------------------- main
def main():
    print("== TRAIN: ladder grid {} K{} seeds {} ==".format(
        GRID, KS_TRAIN, SEEDS_TRAIN))
    X, y = collect_ladder_corpus()
    print(f"  corpus {len(y)} ticks, base resident rate "
          f"{sum(y)/len(y):.4f}")

    M = {}
    for tag, idx in MODELS.items():
        OFF, C, rep = train_predictor(X, y, idx, tag)
        M[tag] = dict(OFF=OFF, C=C, rep=rep)
        print(f"  [{tag:>7}] acc {rep['in_domain_acc']}, int-sign "
              f"{rep['int_sign_agreement']}, weights {rep['weights_std']}")
        print(f"  [{tag:>7}] OFF={OFF} C={C}")

    print("\n== THRESHOLD SELECT (train seeds/grammars only) ==")
    for tag, idx in MODELS.items():
        tlo, thi, score = select_thresholds(M[tag]["OFF"], M[tag]["C"],
                                            idx, X, tag)
        M[tag]["tlo"], M[tag]["thi"] = tlo, thi
        M[tag]["train_score"] = score

    # deployed model: best train-ladder score (train-only model selection;
    # ties broken by MODELS insertion order)
    dep = max(MODELS, key=lambda t: M[t]["train_score"])
    print(f"\n== DEPLOYED MODEL: {dep} (train-ladder "
          f"{M[dep]['train_score']/10:.1f}%) ==")

    if not canaries(M):
        print("ABORT: canaries failed — no results collected.")
        sys.exit(1)

    results, ladder15_sched, kcoh_ident = evaluate(M, dep)

    def gains(cond, base):
        return [v[cond] - v[base] for v in results.values()]

    mg = lambda v: sum(v) / len(v)  # noqa: E731
    print(f"\n== VERDICT (deployed candidate = {dep}) ==")
    summ = {}
    for cond in MODELS:
        g15, g30, gv1 = (gains(cond, b)
                         for b in ("static15", "static30", "v1"))
        noreg = min(g15) >= 0 and min(g30) >= 0 and min(gv1) >= 0
        verd = ("VALIDATED" if mg(g15) > 0 and noreg else
                "MIXED" if (mg(g15) > 0 or mg(g30) > 0) else "FALSIFIED")
        summ[cond] = dict(verdict=verd, zero_regressions=bool(noreg),
                          vs_static15=round(mg(g15), 1),
                          vs_static30=round(mg(g30), 1),
                          vs_v1=round(mg(gv1), 1),
                          worst_s15=round(min(g15), 1),
                          worst_s30=round(min(g30), 1),
                          worst_v1=round(min(gv1), 1))
        print(f"  [{cond:>9}]{'*' if cond == dep else ' '} {verd:<9} "
              f"mean vs s15 {mg(g15):+5.1f}  vs s30 {mg(g30):+5.1f}  "
              f"vs v1 {mg(gv1):+5.1f}   "
              f"worst {min(g15):+5.1f}/{min(g30):+5.1f}/{min(gv1):+5.1f}  "
              f"zero-reg {noreg}")

    # protection-term gap analysis on the out5_1 class (SPIN-12: +22.4pp
    # above additive fit at K=4)
    print("\n== PROTECTION TERM: out5_1-class gap (SPIN-12 residual "
          "+22.4pp @ K=4) ==")
    gap = {}
    for base in ("shape", "full", "v1plus"):
        ptag = base + "_p"
        for gname in ("out5_1", "kcoh5"):
            for k in KS_EVAL:
                v = results[(gname, k)]
                d = v[ptag] - v[base]
                gap[f"{ptag}-{base}_{gname}_K{k}"] = d
                if k == 4 or d != 0:
                    print(f"  [{ptag}-{base:>7}] {gname} K={k}: "
                          f"{v[base]} -> {v[ptag]}  ({d:+.1f})  "
                          f"[static15 {v['static15']}, v1 {v['v1']}]")
    print(f"  prot weight (std): full_p "
          f"{M['full_p']['rep']['weights_std'].get('prot')}, "
          f"v1plus_p {M['v1plus_p']['rep']['weights_std'].get('prot')}")

    out = dict(deployed=dep, summary=summ,
               models={t: dict(idx=list(MODELS[t]), rep=M[t]["rep"],
                               OFF=M[t]["OFF"], C=M[t]["C"],
                               tlo=M[t]["tlo"], thi=M[t]["thi"],
                               train_score=round(M[t]["train_score"] / 10,
                                                 1))
                       for t in MODELS},
               ladder15_sched=ladder15_sched, kcoh5_eq_out5_1=kcoh_ident,
               protection_gap=gap,
               results={f"{g}_K{k}": v for (g, k), v in results.items()})
    with open(os.path.join(HERE, "results2.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  wrote {os.path.join(HERE, 'results2.json')}")


if __name__ == "__main__":
    main()
