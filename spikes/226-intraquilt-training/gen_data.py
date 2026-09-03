#!/usr/bin/env python3
"""226 E2 — QUILT-AS-DATASET: generate the correction-record corpus.

Runs the 225 wheel fabric (exp_glm1.run_fabric, integer-only sim) across
grammars x spreads x K x seeds, and emits one record per correction
emission. Labels: success = post-correction residual <= DELTA (tick
settled). Also replays the SPIN-4 canary configs (model-free baseline).

Fixed seeds everywhere. No floats inside the sim; feature extraction is
integer arithmetic only.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAB = os.path.join(HERE, "..", "225-e1-interference-tick", "inventors-derby")
sys.path.insert(0, FAB)
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
N = 6
DELTA = 12
TICKS = 1200
KS = (1, 2, 8)

# grammar catalogue (spin5 vocabulary + extra spreads for data volume)
def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]

GRAMMARS = {}
for sp in (5, 10, 15, 20, 25, 30):
    GRAMMARS[f"ladder{sp}"] = ladder(sp)
for k in range(1, 6):
    GRAMMARS[f"cohort{k}"] = [0] * k + [15] * (N - k)
GRAMMARS["bimodal"] = [0, 0, 7, 8, 15, 15]


def canary():
    """SPIN-4 canary replay: ladder spread=15 N=6 K=1/2/8, 5 seeds, true%%."""
    print("== CANARY: spin4 ladder15 replay (expect ~71.5 / 60.0 / 70.7 %) ==")
    out = {}
    for K in KS:
        vals = []
        for sd in SEEDS:
            r = run_fabric("interference", TICKS, GRAMMARS["ladder15"],
                           K=K, pd=3, delta=DELTA, drift=6, seed=sd)
            vals.append(within_pm(r["resid"], DELTA) / 10.0)
        m = sum(vals) / len(vals)
        out[K] = round(m, 1)
        print(f"  K={K}: true% mean {m:.1f}  (seeds: {[round(v,1) for v in vals]})")
    return out


def features_for(run, lats, grammar_name, spread, K):
    """Per-emission integer feature records + per-tick labels."""
    resid, emis, cflags = run["resid"], run["emissions"], run["cflags"]
    tick_of = {}
    for (t, i, pm, te) in emis:
        tick_of.setdefault(t, []).append((i, pm, te))
    recs = []
    for (t, i, pm, te) in emis:
        prior1 = 1 if (t - 1) in tick_of else 0
        prior2 = 1 if (t - 2) in tick_of else 0
        in_flight = 0
        for tt in range(max(0, t - K), t):
            in_flight += len(tick_of.get(tt, []))
        sign_agree = 1 if (pm * te > 0) else 0
        n_trig = len(tick_of[t])
        recs.append({
            "tick": t, "lag": lats[i], "spread": spread,
            "grammar": grammar_name, "K": K, "seed": emis and 0 or 0,  # filled later
            "trig_err": te, "abs_err": abs(te), "pulse": abs(pm),
            "prior1": prior1, "prior2": prior2, "in_flight": in_flight,
            "n_trig": n_trig, "sign_agree": sign_agree,
            "cancel": cflags[t],
            "success": 1 if resid[t] <= DELTA else 0,
        })
    return recs


def main():
    can = canary()
    all_recs = []
    summary = []
    for gname, lats in sorted(GRAMMARS.items()):
        spread = max(lats) - min(lats)
        for K in KS:
            for sd in SEEDS:
                r = run_fabric("interference", TICKS, lats, K=K, pd=3,
                               delta=DELTA, drift=6, seed=sd)
                recs = features_for(r, lats, gname, spread, K)
                for rc in recs:
                    rc["seed"] = sd
                all_recs.extend(recs)
                summary.append({
                    "grammar": gname, "K": K, "seed": sd,
                    "true_pm": within_pm(r["resid"], DELTA),
                    "events": r["events"],
                    "success_rate": round(sum(x["success"] for x in recs)
                                          / max(1, len(recs)), 4),
                })
    out = os.path.join(HERE, "outputs")
    with open(os.path.join(out, "e2_records.jsonl"), "w") as f:
        for rc in all_recs:
            f.write(json.dumps(rc) + "\n")
    with open(os.path.join(out, "e2_run_summary.json"), "w") as f:
        json.dump({"canary": can, "runs": summary}, f, indent=1)
    n = len(all_recs)
    base = sum(r["success"] for r in all_recs) / n
    print(f"\n== corpus: {n} correction records from {len(summary)} runs ==")
    print(f"   global correction-success base rate: {base:.4f}")
    print(f"   canary: {can}")


if __name__ == "__main__":
    main()
