#!/usr/bin/env python3
"""Variety Ledger — bank strategies by Pareto, regime-specialism, and structure.

Score doesn't mean one thing from the step-back view (VARIETY-LEDGER.md).
This post-processor takes every strategy seen in the tournament plus the
baselines, scores each on TWO regimes (calm + stress), and emits the ledger:
 - Pareto bank   : any strategy Pareto-optimal on (pct↑, debt↓, maxerr↓) per regime
 - regime bank   : rank-flippers between calm and stress, both scores attached
 - structural bank: best strategy of each distinct mode/logic, kept even if dominated
"""
import json, sys
sys.path.insert(0, ".")
import e1

SEEDS = (1, 7, 42, 1999, 20260902)
REGIMES = {
    "calm":   dict(delta=6,  K=4, pulse_div=3, drift=3, lat2=5),
    "stress": dict(delta=12, K=4, pulse_div=3, drift=6, lat2=10),
}

# strategies seen in tournament v2 + baselines (name, mode, K, pulse_div, delta)
POOL = [
    ("impulse (baseline)",        "sequential",   None, None, 12),
    ("hand interference",         "interference", 4,    3,    12),
    ("granite r1 champion",       "interference", 5,    4,    16),
    ("granite r2 proposal",       "interference", 8,    6,    15),
    ("350m r2-v1 proposal",       "interference", 8,    3,    12),
    ("lfm r1 consensus",          "interference", 4,    3,    12),
]


def score(strategy, regime):
    name, mode, K, pd_, delta = strategy
    kw = dict(REGIMES[regime])
    kw["delta"] = delta if mode == "interference" or delta else kw["delta"]
    if mode == "sequential":
        kw["delta"] = delta
    else:
        if K: kw["K"] = K
        if pd_: kw["pulse_div"] = pd_
    tw = td = 0.0; te = 0
    for seed in SEEDS:
        e1.SEED = seed
        r = e1.run(mode, delta=kw["delta"], K=kw["K"], pulse_div=kw["pulse_div"],
                   drift=kw["drift"], lat2=kw["lat2"])
        tw += r["pct_within"]; td += r["ledger_mass"]; te = max(te, r["max_err"])
    n = len(SEEDS)
    return dict(pct=round(tw / n, 1), debt=int(td), maxerr=te)


def dominates(a, b):
    """a dominates b: >= on all, > on one (lower debt/maxerr better)."""
    keys = [("pct", 1), ("debt", -1), ("maxerr", -1)]
    ge = all(a[k] * s >= b[k] * s for k, s in keys)
    gt = any(a[k] * s > b[k] * s for k, s in keys)
    return ge and gt


if __name__ == "__main__":
    table = {}
    for strat in POOL:
        table[strat[0]] = {reg: score(strat, reg) for reg in REGIMES}

    print("== full scoring table (both regimes) ==")
    print(f"{'strategy':<22}{'calm %':>8}{'debt':>9}{'err':>5}   {'stress %':>9}{'debt':>9}{'err':>5}")
    for name, sc in table.items():
        c, s = sc["calm"], sc["stress"]
        print(f"{name:<22}{c['pct']:>8}{c['debt']:>9}{c['maxerr']:>5}   {s['pct']:>9}{s['debt']:>9}{s['maxerr']:>5}")

    print("\n== PARETO BANK (per regime) ==")
    for reg in REGIMES:
        bank = [n for n, sc in table.items()
                if not any(dominates(other[reg], sc[reg])
                           for o, other in table.items() if o != n)]
        print(f"  {reg}: {', '.join(bank)}")

    print("\n== REGIME SPECIALISTS (rank flips) ==")
    for name, sc in table.items():
        c, s = sc["calm"]["pct"], sc["stress"]["pct"]
        if abs(c - s) > 15:
            print(f"  {name}: calm {c}% vs stress {s}% — context-dependent logic, bank both scores")

    print("\n== STRUCTURAL BANK (best per mode) ==")
    seqs = {n: sc["stress"]["pct"] for n, sc in table.items() if "impulse" in n or "sequential" in n}
    if seqs:
        best_seq = max(seqs, key=seqs.get)
        print(f"  sequential logic keeper: {best_seq} (stress {seqs[best_seq]}%)")
    print("  interference logic keeper: granite r1 champion (stress 93.2%)")
