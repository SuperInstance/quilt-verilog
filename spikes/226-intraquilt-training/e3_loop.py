#!/usr/bin/env python3
"""226 E3 — SELF-IMPROVEMENT LOOP (tiny): does gating corrections with the
E2-trained model improve true-residency across rounds vs ungated control?

Loop shape (K rounds, testing SHAPE not convergence):
  round 0 : ungated runs on train grammars -> collect correction records
            -> train logreg gate (as in E2)
  round r : run fabric with GATE — a triggering sensor's pulse is emitted
            only if the gate predicts success (prob>thr); skipped pulses
            don't enter the ledger. Retrain on cumulative data each round.
  control : identical rounds with gate disabled (always emit).

Metric: within_pm true-residency per round (mean over eval configs x seeds).
Both arms share the same fabric seed stream, so round-0 ungated runs are
byte-identical by construction (canary).
"""
import json
import os
import sys
from collections import deque

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
FAB = os.path.join(HERE, "..", "225-e1-interference-tick", "inventors-derby")
sys.path.insert(0, FAB)
from exp_glm1 import LCG, reality, within_pm  # noqa: E402

FEATS = ["tick", "lag", "spread", "K", "trig_err", "abs_err", "pulse",
         "prior1", "prior2", "in_flight", "n_trig", "sign_agree"]
DELTA = 12
N = 6
K_PULSE = 2          # pulse life (matches E2 eval configs)
THR = 0.5
ROUNDS = 3

TRAIN_CFGS = [(f"ladder{sp}", [round(i * sp / (N - 1)) for i in range(N)])
              for sp in (5, 10, 15, 20, 25, 30)]
EVAL_CFGS = [("eval-ladder18", [0, 4, 7, 11, 14, 18]),
             ("eval-cohort3", [0, 0, 0, 15, 15, 15]),
             ("eval-laggard", [0, 0, 0, 0, 0, 21])]
SEEDS = (1, 7, 42, 1999, 20260902)


def gated_run(lats, seed, gate=None, ticks=1200):
    """run_fabric clone with optional per-emission gate (same integer core)."""
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    n = len(lats)
    spread = max(lats) - min(lats)
    emissions = []
    resid = []
    tick_of = {}
    skipped = 0
    for t in range(ticks):
        reads = [reality(max(0, t - lats[i])) for i in range(n)]
        s_true = reality(t)
        g += rng.below(2 * 6 + 1) - 6
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > DELTA]
        fired = []
        for i, e in trig:
            m = abs(e) // 3 or 1
            pm = m if e > 0 else -m
            prior1 = 1 if (t - 1) in tick_of else 0
            prior2 = 1 if (t - 2) in tick_of else 0
            in_flight = sum(len(tick_of.get(tt, []))
                            for tt in range(max(0, t - K_PULSE), t))
            rec = [t, lats[i], spread, K_PULSE, e, abs(e), abs(pm),
                   prior1, prior2, in_flight, len(trig),
                   1 if pm * e > 0 else 0]
            if gate is not None and gate(rec) <= THR:
                skipped += 1
                continue
            pulses.appendleft([pm, K_PULSE])
            emissions.append((t, i, pm, e, rec))
            fired.append(i)
        if fired:
            tick_of.setdefault(t, []).extend(fired)
        if pulses:
            net = sum(p[0] for p in pulses)
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
        resid.append(abs(s_true - g))
    # labels: success = post-correction tick within delta
    recs = []
    for (t, i, pm, e, rec) in emissions:
        rr = dict(zip(FEATS, rec))
        rr["success"] = 1 if resid[t] <= DELTA else 0
        rr["grammar"] = None
        recs.append(rr)
    return dict(resid=resid, recs=recs, skipped=skipped)


def train_gate(recs, seed=226):
    X = np.array([[r[f] for f in FEATS] for r in recs], dtype=float)
    y = np.array([r["success"] for r in recs])
    sc = StandardScaler().fit(X)
    clf = LogisticRegression(max_iter=300, random_state=seed).fit(sc.transform(X), y)
    def gate(rec):
        x = sc.transform(np.array([rec], dtype=float))
        return float(clf.predict_proba(x)[0, 1])
    return gate


def main():
    history = {"gated": [], "control": []}
    corpus = []
    # round 0: ungated train-grammar collection (both arms identical here)
    round0_eval = []
    for name, lats in EVAL_CFGS:
        for sd in SEEDS:
            r = gated_run(lats, sd, gate=None)
            round0_eval.append(within_pm(r["resid"], DELTA))
    r0 = sum(round0_eval) / len(round0_eval)
    for name, lats in TRAIN_CFGS:
        for sd in SEEDS:
            r = gated_run(lats, sd, gate=None)
            corpus.extend(r["recs"])
    gate = train_gate(corpus)
    history["gated"].append({"round": 0, "true_pm": round(r0, 1), "n_recs": len(corpus)})
    history["control"].append({"round": 0, "true_pm": round(r0, 1), "n_recs": len(corpus)})
    print(f"round 0 (ungated, shared): true_pm={r0:.1f} corpus={len(corpus)}")

    # canary: gated_run with gate=None must equal exp_glm1.run_fabric resid
    from exp_glm1 import run_fabric
    a = gated_run(EVAL_CFGS[0][1], 1, gate=None)
    b = run_fabric("interference", 1200, EVAL_CFGS[0][1], K=K_PULSE, pd=3,
                   delta=DELTA, drift=6, seed=1)
    byte_ident = a["resid"] == b["resid"]
    print(f"canary gated_run==run_fabric (resid lists identical): {byte_ident}")

    for rnd in range(1, ROUNDS + 1):
        for arm in ("gated", "control"):
            vals, skips, nrec = [], 0, 0
            for name, lats in EVAL_CFGS:
                for sd in SEEDS:
                    r = gated_run(lats, sd,
                                  gate=gate if arm == "gated" else None)
                    vals.append(within_pm(r["resid"], DELTA))
                    skips += r["skipped"]
                    nrec += len(r["recs"])
                    if arm == "gated":
                        corpus.extend(r["recs"])
            mean = sum(vals) / len(vals)
            history[arm].append({"round": rnd, "true_pm": round(mean, 1),
                                 "skipped": skips, "n_recs": nrec})
            print(f"round {rnd} {arm:8s}: true_pm={mean:.1f} skipped={skips}")
        gate = train_gate(corpus)  # retrain on cumulative data
    with open(os.path.join(HERE, "outputs", "e3_loop_results.json"), "w") as f:
        json.dump({"history": history, "canary_byte_identical": byte_ident,
                   "thr": THR, "rounds": ROUNDS}, f, indent=1)
    print(json.dumps(history, indent=1))


if __name__ == "__main__":
    main()
