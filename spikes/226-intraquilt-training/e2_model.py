#!/usr/bin/env python3
"""226 E2 — QUILT-AS-DATASET: does a tiny model beat the base rate at
predicting correction success? Does it TRANSFER to a held-out grammar?

Features (all integer): tick, lag, spread, K, trig_err, abs_err, pulse,
prior1, prior2, in_flight, n_trig, sign_agree, cancel.
Models: sklearn LogisticRegression (fixed seed where applicable) and a
2-layer numpy MLP (1 hidden layer, 16 units, fixed-seed SGD).

Splits:
  in-domain : ladder grammars, seeds {1,7,42,1999} train -> seed 20260902 test
  transfer  : ALL ladder train -> cohort1..5 + bimodal test (held-out grammar)
"""
import json
import os

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
FEATS = ["tick", "lag", "spread", "K", "trig_err", "abs_err", "pulse",
         "prior1", "prior2", "in_flight", "n_trig", "sign_agree", "cancel"]
DELTA = 12


def load():
    recs = []
    with open(os.path.join(HERE, "outputs", "e2_records.jsonl")) as f:
        for line in f:
            recs.append(json.loads(line))
    return recs


def mlp(X, y, seed=226, h=16, epochs=40, lr=0.05, bs=256):
    """2-layer MLP in numpy, fixed seed, manual SGD."""
    rng = np.random.RandomState(seed)
    n, d = X.shape
    W1 = rng.randn(d, h) * np.sqrt(2 / d)
    b1 = np.zeros(h)
    W2 = rng.randn(h, 1) * np.sqrt(2 / h)
    b2 = np.zeros(1)
    for ep in range(epochs):
        idx = rng.permutation(n)
        for s in range(0, n, bs):
            j = idx[s:s + bs]
            Xb, yb = X[j], y[j].reshape(-1, 1)
            z1 = Xb @ W1 + b1
            a1 = np.tanh(z1)
            z2 = a1 @ W2 + b2
            p = 1 / (1 + np.exp(-np.clip(z2, -30, 30)))
            dz2 = (p - yb) / len(j)
            dW2 = a1.T @ dz2
            db2 = dz2.sum(0)
            da1 = dz2 @ W2.T
            dz1 = da1 * (1 - a1 ** 2)
            dW1 = Xb.T @ dz1
            db1 = dz1.sum(0)
            for P, G in ((W1, dW1), (b1, db1), (W2, dW2), (b2, db2)):
                P -= lr * G
    def pred(Xv):
        a1 = np.tanh(Xv @ W1 + b1)
        return (a1 @ W2 + b2).ravel()
    return pred


def eval_split(name, train_recs, test_recs, results):
    Xtr = np.array([[r[f] for f in FEATS] for r in train_recs], dtype=float)
    ytr = np.array([r["success"] for r in train_recs])
    Xte = np.array([[r[f] for f in FEATS] for r in test_recs], dtype=float)
    yte = np.array([r["success"] for r in test_recs])
    sc = StandardScaler().fit(Xtr)
    base = yte.mean()
    row = {"split": name, "n_train": len(ytr), "n_test": len(yte),
           "base_rate": round(float(base), 4)}
    # logistic regression
    lr = LogisticRegression(max_iter=300, random_state=226)
    lr.fit(sc.transform(Xtr), ytr)
    ph = lr.predict_proba(sc.transform(Xte))[:, 1]
    row["logreg_acc"] = round(float(accuracy_score(yte, ph > .5)), 4)
    row["logreg_auc"] = round(float(roc_auc_score(yte, ph)), 4)
    # MLP
    pred = mlp(sc.transform(Xtr), ytr, seed=226)
    pm = pred(sc.transform(Xte))
    row["mlp_acc"] = round(float(accuracy_score(yte, pm > 0)), 4)
    row["mlp_auc"] = round(float(roc_auc_score(yte, pm)), 4)
    # majority baseline
    row["majority_acc"] = round(float(max(base, 1 - base)), 4)
    results.append(row)
    print(f"{name:28s} base={row['base_rate']:.3f} "
          f"maj={row['majority_acc']:.3f} "
          f"logreg={row['logreg_acc']:.3f}(auc {row['logreg_auc']:.3f}) "
          f"mlp={row['mlp_acc']:.3f}(auc {row['mlp_auc']:.3f})")
    return row


def main():
    recs = load()
    print(f"loaded {len(recs)} records")
    results = []
    # in-domain: ladder only, seed split
    lad = [r for r in recs if r["grammar"].startswith("ladder")]
    tr = [r for r in lad if r["seed"] != 20260902]
    te = [r for r in lad if r["seed"] == 20260902]
    eval_split("in-domain(ladder,seed-holdout)", tr, te, results)
    # transfer: all ladder -> each held-out grammar family
    coh = [r for r in recs if r["grammar"].startswith("cohort")]
    bim = [r for r in recs if r["grammar"] == "bimodal"]
    eval_split("TRANSFER(ladder->cohort)", lad, coh, results)
    eval_split("TRANSFER(ladder->bimodal)", lad, bim, results)
    # transfer across seeds too (fully honest: cohort seed-holdout only)
    coh_te = [r for r in coh if r["seed"] == 20260902]
    lad_tr = [r for r in lad if r["seed"] != 20260902]
    eval_split("TRANSFER(seed-hold,lad->coh)", lad_tr, coh_te, results)
    with open(os.path.join(HERE, "outputs", "e2_results.json"), "w") as f:
        json.dump(results, f, indent=1)
    # feature weights (logreg, ladder in-domain) for interpretability
    sc = StandardScaler().fit(np.array([[r[f2] for f2 in FEATS] for r in tr], dtype=float))
    ytr = np.array([r["success"] for r in tr])
    lr = LogisticRegression(max_iter=300, random_state=226).fit(
        sc.transform(np.array([[r[f2] for f2 in FEATS] for r in tr], dtype=float)), ytr)
    w = sorted(zip(FEATS, lr.coef_[0]), key=lambda kv: -abs(kv[1]))
    print("\ntop logreg weights (ladder in-domain):")
    for fname, wt in w[:6]:
        print(f"  {fname:>10s} {wt:+.2f}")


if __name__ == "__main__":
    main()
