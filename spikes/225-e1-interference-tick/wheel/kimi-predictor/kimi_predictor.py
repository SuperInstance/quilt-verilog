#!/usr/bin/env python3
"""KIMI-PREDICTOR — learned-predictor scheduler (g3-kinduction lane).

Idea (intra-quilt E2 lineage, spikes/226 e2_model.py): a tiny logistic
model over live fabric state — features [in-flight count, mean lag,
stale-mass, K] — predicts per-tick true-residency. DEPLOYED as a runtime
scheduler: each tick the interference arm scores its live grammar state
and nudges the latency spread (shrink when failure-prone, restore toward
nominal when healthy).

Fabric: exp_glm1.run_fabric E1 contract (fdiv decay, 64-bit LCG, FIFO
oldest-first expiry, snapshot decay). run_dyn() below is a verbatim
replica of that loop with per-tick hooks; byte-identity against
exp_glm1.run_fabric is a mandatory canary. Integer-only inside the loop —
the deployed predictor is fixed-point (SCALE=1024); floats appear only in
offline training (sklearn, like e2) and display statistics.

Split discipline:
  TRAIN : ladder-grammar grid, seeds {1,7,42}
  EVAL  : HELD-OUT grammars (cohort 3+3, outlier, kcoh5) x seeds
          {1999, 20260902}. Only residency gain on unseen grammars counts.

CANARIES (mandatory):
  1. sequential-arm byte-identity: scheduler must not change sequential
     behavior (run_dyn sequential, scheduler active, == run_fabric).
  2. harness identity: run_dyn interference (scheduler off) ==
     exp_glm1.run_fabric byte-identical.
  3. SPIN-5 replay: ladder s=15 K=1 scheduler-off within 2pp of 71.5%
     (published per-seed permille 709/713/721/714/717).
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS_TRAIN = (1, 7, 42)
SEEDS_EVAL = (1999, 20260902)
SEEDS_ALL = (1, 7, 42, 1999, 20260902)
SEEDS_REPLAY = SEEDS_ALL
DELTA = 12
N = 6
TICKS = 4800
SCALE = 1024          # fixed-point for the deployed integer predictor
GRID = (5, 10, 15, 20, 25, 30)   # ladder training grid (spreads)


# ---------------------------------------------------------- grammars
def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


def cohort33(s):
    return [0, 0, 0, s, s, s]


def outlier(s):
    return [0, 0, 0, 0, 0, s]


def kcoh5(s):
    # k-cohort split k=5 per SPIN-5-topology: [0]*5 + [s] — same multiset
    # as outlier (order-invariance, Spin-5 canary C); kept as a separate
    # named eval row to re-verify that identity on held-out seeds.
    return [0] * (N - 1) + [s]


HELDOUT = (("cohort3+3", cohort33), ("outlier", outlier), ("kcoh5", kcoh5))


# ---------------------------------------------------------- dynamic fabric
def run_dyn(mode, ticks, lats, K=4, pd=3, delta=12, drift=6,
            seed=20260902, scheduler=None, feats_out=None):
    """Verbatim replica of exp_glm1.run_fabric with two hooks:
      feats_out : if a list is given, append per-tick integer feature
                  tuples (in_flight, mean_lag, stale_mass, K, label) where
                  label = 1 iff post-correction resid <= delta. Features are
                  sampled AFTER FIFO expiry, BEFORE triggers.
      scheduler : interference arm only; callable(feats, lats, nominal)
                  -> new lats list, applied once per tick after features.
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
            feats = (inflight, mean_lag, stale, K)
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
    """Per-tick feature records from the ladder grid, TRAIN seeds only."""
    X, y = [], []
    for s in GRID:
        for k in (1, 2):
            for sd in SEEDS_TRAIN:
                feats = []
                run_dyn("interference", TICKS, ladder(s), K=k, pd=3,
                        delta=DELTA, drift=6, seed=sd, feats_out=feats)
                for f in feats:
                    X.append(f[:4])
                    y.append(f[4])
    return X, y


def train_predictor(X, y):
    """sklearn logistic regression on standardized features (e2 lineage),
    folded into a fixed-point integer scorer: z = OFF + sum(C_i * f_i),
    predict resident iff z >= 0. Returns (OFF, C, report dict)."""
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    Xa = np.array(X, dtype=float)
    ya = np.array(y)
    mu = Xa.mean(0)
    sd = Xa.std(0)
    sd[sd == 0] = 1.0
    lr = LogisticRegression(max_iter=500, random_state=226)
    lr.fit((Xa - mu) / sd, ya)
    w = lr.coef_[0]
    b = lr.intercept_[0]
    # fold standardization into raw-feature integer coefficients
    C = [int(round(wi / si * SCALE)) for wi, si in zip(w, sd)]
    OFF = int(round(b * SCALE)) - int(round(sum(
        ci * mi for ci, mi in zip(C, mu))))
    # fidelity: integer scorer vs sklearn sign agreement on the corpus
    zf = b + ((Xa - mu) / sd) @ w
    zi = OFF + np.array(X, dtype=np.int64) @ np.array(C, dtype=np.int64)
    agree = float(np.mean((zf >= 0) == (zi >= 0)))
    rep = dict(base_rate=round(float(ya.mean()), 4),
               in_domain_acc=round(float(lr.score((Xa - mu) / sd, ya)), 4),
               weights_std={f: round(float(wi), 3) for f, wi in
                            zip(("in_flight", "mean_lag", "stale_mass", "K"), w)},
               C=C, OFF=OFF, int_sign_agreement=round(agree, 4),
               mu=[round(float(m), 3) for m in mu],
               sd=[round(float(s), 3) for s in sd])
    return OFF, C, rep


def make_scheduler(OFF, C, tlo, thi):
    """Fixed-point integer scheduler. Per tick: score live state; if
    failure-prone (z < tlo) shrink every lag by 1 (spread -1); if healthy
    (z > thi) restore 1 toward nominal. Pure integer arithmetic."""
    def sched(feats, lats, nominal):
        z = OFF + sum(c * f for c, f in zip(C, feats))
        if z < tlo:
            return [max(0, l - 1) for l in lats]
        if z > thi:
            return [min(nm, l + 1) for l, nm in zip(lats, nominal)]
        return list(lats)
    return sched


def true_pm(mode, lats, k, seed, scheduler=None):
    r = run_dyn(mode, TICKS, lats, K=k, pd=3, delta=DELTA, drift=6,
                seed=seed, scheduler=scheduler)
    return within_pm(r["resid"], DELTA)


def mean_pm(mode, lats, k, seeds, scheduler=None):
    v = [true_pm(mode, lats, k, sd, scheduler) for sd in seeds]
    return sum(v) / len(v), v   # display-only float mean


# ---------------------------------------------------------- canaries
def canaries(OFF, C, tlo, thi):
    ok = True
    print("== CANARY 1: sequential-arm byte-identity (scheduler active) ==")
    sched = make_scheduler(OFF, C, tlo, thi)
    c1 = True
    for gname, gfn in (("ladder", ladder),) + HELDOUT:
        for s in (15, 30):
            for sd in SEEDS_EVAL:
                r1 = run_dyn("sequential", TICKS, gfn(s), K=1, pd=3,
                             delta=DELTA, drift=6, seed=sd, scheduler=sched)
                r2 = run_fabric("sequential", TICKS, gfn(s), K=1, pd=3,
                                delta=DELTA, drift=6, seed=sd)
                if not byte_identical(r1, r2):
                    c1 = False
                    print(f"  MISMATCH sequential {gname}@{s} seed={sd}")
    print("  PASS: 16/16 sequential runs byte-identical with scheduler "
          "active" if c1 else "  FAIL")
    ok &= c1

    print("\n== CANARY 2: harness identity (interference, scheduler off) ==")
    c2 = True
    for gname, gfn in (("ladder", ladder),) + HELDOUT:
        for s in (15, 30):
            for k in (1, 2):
                for sd in SEEDS_EVAL:
                    r1 = run_dyn("interference", TICKS, gfn(s), K=k, pd=3,
                                 delta=DELTA, drift=6, seed=sd)
                    r2 = run_fabric("interference", TICKS, gfn(s), K=k,
                                    pd=3, delta=DELTA, drift=6, seed=sd)
                    if not byte_identical(r1, r2):
                        c2 = False
                        print(f"  MISMATCH interference {gname}@{s} "
                              f"K={k} seed={sd}")
    print("  PASS: 32/32 interference runs byte-identical to "
          "exp_glm1.run_fabric" if c2 else "  FAIL")
    ok &= c2

    print("\n== CANARY 3: SPIN-5 replay ladder s=15 K=1 (scheduler off) ==")
    pub = (709, 713, 721, 714, 717)
    got = tuple(true_pm("interference", ladder(15), 1, sd)
                for sd in SEEDS_REPLAY)
    m = sum(got) / len(got) / 10
    c3 = got == pub and abs(m - 71.5) <= 2.0
    print(f"  per-seed permille got {got} pub {pub}  mean {m:.1f}% "
          f"(tolerance +-2pp of 71.5)")
    print("  PASS" if c3 else "  FAIL")
    ok &= c3

    print("\nALL CANARIES:", "PASS" if ok else
          "FAIL — results below do NOT count")
    return ok


# ---------------------------------------------------------- threshold select
def select_thresholds(OFF, C):
    """Pick (tlo, thi) by grid on TRAIN ladder runs only (seeds 1,7,42) —
    never touches held-out grammars or eval seeds. Candidate thresholds are
    deciles of the training z-score distribution."""
    # training z distribution from the ladder corpus (re-collected cheaply:
    # features only, scheduler off)
    zs = []
    for s in GRID:
        for k in (1, 2):
            for sd in SEEDS_TRAIN:
                feats = []
                run_dyn("interference", TICKS, ladder(s), K=k, pd=3,
                        delta=DELTA, drift=6, seed=sd, feats_out=feats)
                zs.extend(OFF + sum(c * f for c, f in zip(C, ft[:4]))
                          for ft in feats)
    zs.sort()
    n = len(zs)
    dec = [zs[min(n - 1, n * d // 10)] for d in range(11)]
    print(f"  training z deciles: {[int(z) for z in dec]}")
    best = None
    rows = []
    for ilo in (2, 3, 4):
        for ihi in (6, 7, 8):
            tlo, thi = dec[ilo], dec[ihi]
            sched = make_scheduler(OFF, C, tlo, thi)
            vals = []
            for s in (10, 15, 20, 30):
                for k in (1, 2):
                    m, _ = mean_pm("interference", ladder(s), k,
                                   SEEDS_TRAIN, sched)
                    vals.append(m)
            score = sum(vals) / len(vals)
            rows.append((score, tlo, thi))
            print(f"  tlo={tlo:>7} thi={thi:>7}  train-ladder mean "
                  f"true% {score/10:.1f}")
            if best is None or score > best[0]:
                best = (score, tlo, thi)
    print(f"  SELECTED tlo={best[1]} thi={best[2]} "
          f"(train-ladder mean {best[0]/10:.1f}%)")
    return best[1], best[2], rows


# ---------------------------------------------------------- evaluation
def evaluate(OFF, C, tlo, thi):
    """HELD-OUT grammars x held-out seeds. Baselines: static spread 15,
    static spread 30. Scheduled: nominal s=15 + live predictor scheduler."""
    sched = make_scheduler(OFF, C, tlo, thi)
    results = {}
    print("\n== EVAL: held-out grammars, seeds {1999, 20260902} ==")
    print(f"{'grammar':<10}{'K':>3}{'static15%':>10}{'static30%':>10}"
          f"{'sched%':>8}{'gain vs s15':>12}{'gain vs s30':>12}")
    for gname, gfn in HELDOUT:
        for k in (1, 2):
            m15, v15 = mean_pm("interference", gfn(15), k, SEEDS_EVAL)
            m30, v30 = mean_pm("interference", gfn(30), k, SEEDS_EVAL)
            msc, vsc = mean_pm("interference", gfn(15), k, SEEDS_EVAL, sched)
            results[(gname, k)] = dict(
                static15=round(m15 / 10, 1), static30=round(m30 / 10, 1),
                sched=round(msc / 10, 1),
                per_seed=dict(static15=v15, static30=v30, sched=vsc))
            print(f"{gname:<10}{k:>3}{m15/10:>10.1f}{m30/10:>10.1f}"
                  f"{msc/10:>8.1f}{(msc-m15)/10:>+12.1f}"
                  f"{(msc-m30)/10:>+12.1f}")
    # in-domain sanity: scheduler on ladder15 K=1 (should not wreck home)
    mlad, _ = mean_pm("interference", ladder(15), 1, SEEDS_EVAL, sched)
    print(f"\n  in-domain sanity: ladder@15 K=1 scheduled = {mlad/10:.1f}% "
          f"(static replay 71.5%)")
    # kcoh5 vs outlier order-invariance re-verification on eval seeds
    ident = all(byte_identical(
        run_dyn("interference", TICKS, outlier(15), K=k, pd=3, delta=DELTA,
                drift=6, seed=sd),
        run_dyn("interference", TICKS, kcoh5(15), K=k, pd=3, delta=DELTA,
                drift=6, seed=sd))
        for k in (1, 2) for sd in SEEDS_EVAL)
    print(f"  kcoh5 == outlier byte-identical on eval seeds (K1,2): {ident}")
    return results, mlad / 10, ident


# ---------------------------------------------------------- main
def main():
    print("== TRAIN: ladder grid {} K(1,2) seeds {} ==".format(GRID,
                                                              SEEDS_TRAIN))
    X, y = collect_ladder_corpus()
    OFF, C, rep = train_predictor(X, y)
    print(f"  corpus {len(y)} ticks, base resident rate {rep['base_rate']}")
    print(f"  logreg in-domain acc {rep['in_domain_acc']}, "
          f"int-sign agreement {rep['int_sign_agreement']}")
    print(f"  standardized weights {rep['weights_std']}")
    print(f"  fixed-point: OFF={OFF} C={C} (SCALE={SCALE})")

    print("\n== THRESHOLD SELECT (train seeds/grammars only) ==")
    tlo, thi, _rows = select_thresholds(OFF, C)

    if not canaries(OFF, C, tlo, thi):
        print("ABORT: canaries failed — no results collected.")
        sys.exit(1)

    results, ladder15_sched, kcoh_ident = evaluate(OFF, C, tlo, thi)

    gains15 = [v["sched"] - v["static15"] for v in results.values()]
    gains30 = [v["sched"] - v["static30"] for v in results.values()]
    mg15 = sum(gains15) / len(gains15)
    mg30 = sum(gains30) / len(gains30)
    verdict = ("VALIDATED" if mg15 > 0 and mg30 > 0 and min(gains15) > -2
               else "MIXED" if (mg15 > 0 or mg30 > 0) else "FALSIFIED")
    print(f"\n== VERDICT: {verdict} ==")
    print(f"  mean held-out residency gain vs static15: {mg15:+.1f}pp")
    print(f"  mean held-out residency gain vs static30: {mg30:+.1f}pp")
    print(f"  worst-cell gain vs static15: {min(gains15):+.1f}pp")

    out = dict(verdict=verdict, train=rep, tlo=tlo, thi=thi, OFF=OFF, C=C,
               ladder15_sched=ladder15_sched, kcoh5_eq_outlier=kcoh_ident,
               gains15=round(mg15, 1), gains30=round(mg30, 1),
               results={f"{g}_K{k}": v for (g, k), v in results.items()})
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  wrote {os.path.join(HERE, 'results.json')}")


if __name__ == "__main__":
    main()
