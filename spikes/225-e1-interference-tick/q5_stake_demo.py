#!/usr/bin/env python3
"""Q5 — §3.2 STAKE DEMO: equal-budget discrete-greedy (GD) control arm.

Hypothesis under test [CHARTER §5.1 selection-bias objection]: the banked
round-1 champion (interference K=1/pd=2/d16, 96.1% stress) is an artifact of
searching only the interference family. Cure: a control arm that is NOT a
family-restricted grid — a discrete-greedy coordinate-descent local search
over the FULL strategy space (mode, K, pulse_div, delta), integer-only,
from a seed config equal to the pre-round-1 state of knowledge (the granite
r1 banked champion K=5/pd=4/d16), given an evaluation budget identical
(call-for-call e1.run invocations) to the round-1 discovery search.

Budget accounting (round-1 o1_k_replay.py, phases 1-3, from its output):
  Phase 1 probes:   9 entries x 3 frames x 5 seeds = 135 calls
  Phase 1 calm-ax:  7 entries x 5 seeds            =  35 calls
  Phase 2 LLM:      2 proposals x 5 seeds          =  10 calls
  Phase 3 holdout:  2 entries x 3 seeds            =   6 calls
  TOTAL discovery budget                            = 186 e1.run calls
(Phase 0 control arms — 50 calls — replayed already-published numbers and
were byte-match gates, not exploration; excluded from both sides equally.)

GD lane budget: 186 calls TOTAL (search fitness evals + its own 3-seed
holdout verification), enforced by a hard counter. Fitness = the same
selection metric the family search promoted on: stress pct on primary seeds
(1,7,42,1999,20260902), tie-broken by lower ledger debt. Integer-only
measurement path: stock e1.run, ints throughout; division only in the
already-published pct = round(mean per-seed pct_within, 1) aggregation.

No floats are introduced anywhere by this harness beyond stock e1.py.

PRE-REGISTERED DECISION RULE (committed before any comparison numbers):
  Head-to-head: champion vs GD final, 3 frames (stress@own-delta, gentle
  d6/drift3/lat5, lcalm d12/drift3/lat5), seeds 1/7/42/1999/20260902,
  plus 3-seed stress holdout (11,313,8888).
  V1 OBJECTION LANDS: GD beats champion by >= 1.0pp on stress AND on both
     calm frames -> family search demoted.
  V2 THIN MARGIN: |GD - champ| < 1.0pp on stress (and GD does not meet V1)
     -> family advantage real but thin, book margin.
  V3 OBJECTION REFUTED: GD loses by > 1.0pp on stress -> family search
     vindicated.
  Special case (pre-registered): if the GD final config EQUALS the champion
  config (mode,K,pd,delta), verdict is V3-STRONG: the optimum is findable
  by an unsteered equal-budget local search from outside the family-restricted
  grid — the win is a property of the substrate, not of where we looked.

CANARIES (pre-registered):
  C1 byte-identity: entire pipeline run twice, sha256 of all output lines
     must match.
  C2 champion anchor replay: champion K1/pd2/d16 stress must reproduce
     (96.1, 121762, 33); old champion K5/pd4/d16 stress (93.2, 132823, 38);
     impulse d16 stress (96.0, 139949, 61); champion gentle (98.0, 103116, 27).
     Any mismatch halts all claims.
  C3 self-canary: (a) a deliberately fitness-INVERTED greedy (minimizes pct)
     from the same seed must end strictly worse than its seed, else the
     search machinery is broken; (b) an anchor gate fed a deliberately wrong
     expected value must FAIL (the gate machinery must be able to say FAIL).
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e1

SEEDS = (1, 7, 42, 1999, 20260902)
HOLDOUT = (11, 313, 8888)
STRESS = dict(drift=6, lat=10)
GENTLE = dict(delta=6, drift=3, lat=5)
LCALM = dict(delta=12, drift=3, lat=5)

CHAMP = ("interference", 1, 2, 16)      # banked round-1 champion
SEEDCFG = ("interference", 5, 4, 16)    # pre-round-1 knowledge: granite r1 banked champ
GD_BUDGET = 186                          # call-for-call parity with round-1 phases 1-3
SEARCH_BUDGET = GD_BUDGET - 3            # reserve 3 calls for GD's own holdout verify


class OutOfBudget(Exception):
    pass


class Budget:
    def __init__(self, cap):
        self.cap = cap
        self.n = 0

    def spend(self, k=1):
        if self.n + k > self.cap:
            raise OutOfBudget(f"budget {self.cap} exhausted")
        self.n += k


FAILS = []
LINES = []


def say(line=""):
    print(line)
    LINES.append(line)


def gate(label, got, want):
    ok = got == want
    if not ok:
        FAILS.append(label)
    say(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got}  want {want}")


def run5(mode, K, pd, delta, drift, lat, seeds=SEEDS, budget=None):
    """Stock 5-seed (or n-seed) evaluation on the e1 substrate. Integer-only."""
    if budget is not None:
        budget.spend(len(seeds))
    rows = []
    for seed in seeds:
        e1.SEED = seed
        rows.append(e1.run(mode, delta=delta, K=K, pulse_div=pd, drift=drift, lat2=lat))
    return dict(
        pct=round(sum(r["pct_within"] for r in rows) / len(seeds), 1),
        debt=sum(r["ledger_mass"] for r in rows),
        maxerr=max(r["max_err"] for r in rows),
        pct_per_seed=tuple(r["pct_within"] for r in rows),
    )


def fitness(cfg, budget):
    """Selection metric identical to the family search's promotion rule:
    stress pct on primary seeds, tie-broken by lower debt. (pct, -debt) max."""
    mode, K, pd, delta = cfg
    r = run5(mode, K, pd, delta, STRESS["drift"], STRESS["lat"], budget=budget)
    return (r["pct"], -r["debt"]), r


def neighbors(cfg):
    """Discrete local moves over the FULL arena strategy space (no family restriction):
    mode flip, K +-1, pulse_div +-1, delta +-1 and +-2. Fixed order, first-improvement."""
    mode, K, pd, delta = cfg
    moves = []
    other = "sequential" if mode == "interference" else "interference"
    moves.append((other, K, pd, delta))
    for dK in (1, -1):
        if 1 <= K + dK <= 8:
            moves.append((mode, K + dK, pd, delta))
    for dP in (1, -1):
        if 1 <= pd + dP <= 8:
            moves.append((mode, K, pd + dP, delta))
    for dD in (1, -1, 2, -2):
        if 4 <= delta + dD <= 24:
            moves.append((mode, K, pd, delta + dD))
    return moves


def gd_arm(budget, invert=False, label="GD"):
    """Discrete-greedy coordinate-descent from SEEDCFG under a hard call budget."""
    cfg = SEEDCFG
    fit, r = fitness(cfg, budget)
    say(f"  {label} seed {cfg} -> stress {r['pct']}% debt {r['debt']}")
    step = 0
    improved = True
    while improved:
        improved = False
        for mv in neighbors(cfg):
            step += 1
            try:
                mfit, mr = fitness(mv, budget)
            except OutOfBudget:
                return cfg, r
            better = mfit < fit if invert else mfit > fit
            if better:
                cfg, fit, r = mv, mfit, mr
                say(f"  {label} step {step}: {cfg} -> stress {mr['pct']}% debt {mr['debt']}"
                    f"   {'(inverted)' if invert else ''}")
                improved = True
        # loop sweeps until no improving move or budget out
    return cfg, r


def head_to_head(cfg, name):
    mode, K, pd, delta = cfg
    say(f"\n== HEAD-TO-HEAD: {name} {cfg} ==")
    s = run5(mode, K, pd, delta, STRESS["drift"], STRESS["lat"])
    g = run5(mode, K, pd, GENTLE["delta"], GENTLE["drift"], GENTLE["lat"])
    c = run5(mode, K, pd, LCALM["delta"], LCALM["drift"], LCALM["lat"])
    h = run5(mode, K, pd, delta, STRESS["drift"], STRESS["lat"], seeds=HOLDOUT)
    say(f"  stress : pct={s['pct']} debt={s['debt']} maxE={s['maxerr']} per-seed={s['pct_per_seed']}")
    say(f"  gentle : pct={g['pct']} debt={g['debt']} maxE={g['maxerr']}")
    say(f"  lcalm  : pct={c['pct']} debt={c['debt']} maxE={c['maxerr']}")
    say(f"  holdout(stress, seeds 11/313/8888): pct={h['pct']} debt={h['debt']} maxE={h['maxerr']}")
    return dict(stress=s, gentle=g, lcalm=c, holdout=h)


def verdict(champ, gd, gd_cfg):
    say("\n== PRE-REGISTERED DECISION RULE APPLICATION ==")
    if gd_cfg == CHAMP:
        say("  GD final config == champion config -> V3-STRONG (objection refuted, method-independent)")
        return "V3-STRONG"
    ds = gd["stress"]["pct"] - champ["stress"]["pct"]
    dg = gd["gentle"]["pct"] - champ["gentle"]["pct"]
    dc = gd["lcalm"]["pct"] - champ["lcalm"]["pct"]
    say(f"  stress delta {ds:+.1f}pp | gentle {dg:+.1f}pp | lcalm {dc:+.1f}pp | "
        f"holdout {gd['holdout']['pct'] - champ['holdout']['pct']:+.1f}pp")
    if ds >= 1.0 and dg >= 1.0 and dc >= 1.0:
        return "V1-OBJECTION-LANDS"
    if ds < -1.0:
        return "V3-OBJECTION-REFUTED"
    return "V2-THIN-MARGIN"


def main():
    say("== C2: CHAMPION ANCHOR REPLAY (any FAIL halts claims) ==")
    a = run5(*CHAMP, STRESS["drift"], STRESS["lat"])
    gate("champion K1/pd2/d16 stress", (a["pct"], a["debt"], a["maxerr"]), (96.1, 121762, 33))
    a = run5("interference", 5, 4, 16, STRESS["drift"], STRESS["lat"])
    gate("old champion K5/pd4/d16 stress", (a["pct"], a["debt"], a["maxerr"]), (93.2, 132823, 38))
    a = run5("sequential", 8, 3, 16, STRESS["drift"], STRESS["lat"])
    gate("impulse d16 stress", (a["pct"], a["debt"], a["maxerr"]), (96.0, 139949, 61))
    a = run5(*CHAMP, GENTLE["drift"], GENTLE["lat"])
    gate("champion gentle", (a["pct"], a["debt"], a["maxerr"]), (98.0, 103116, 27))
    if FAILS:
        say("\nC2 FAILED — no claims from this run.")
        return 1

    say("\n== C3b: SELF-CANARY — wrong-anchor gate must FAIL (gate teeth) ==")
    fails_before = len(FAILS)
    gate("(deliberately wrong) champion stress", 0.0, 96.1)
    caught = len(FAILS) == fails_before + 1
    say(f"  [{'CAUGHT' if caught else 'MISSED'}] wrong-anchor gate failed as designed")
    if not caught:
        return 1

    say("\n== C3a: SELF-CANARY — fitness-inverted greedy must end strictly worse ==")
    b = Budget(GD_BUDGET + 60)  # canary lane runs OUTSIDE the real budget
    seed_fit, _ = fitness(SEEDCFG, b)
    bad_cfg, bad_r = gd_arm(b, invert=True, label="CANARY")
    bad_fit, _ = fitness(bad_cfg, b)
    ok = bad_fit < seed_fit
    say(f"  [{'CAUGHT' if ok else 'MISSED'}] inverted arm ended at {bad_cfg} "
        f"stress {bad_r['pct']}% (< seed {seed_fit[0]}%)")
    if not ok:
        return 1

    say("\n== GD CONTROL ARM (discrete greedy, full space, budget 186 calls) ==")
    budget = Budget(GD_BUDGET)
    budget.cap = SEARCH_BUDGET  # 3 calls reserved for in-budget holdout verify
    gd_cfg, gd_r = gd_arm(budget, label="GD")
    budget.cap = GD_BUDGET
    say(f"  GD final: {gd_cfg} stress {gd_r['pct']}% debt {gd_r['debt']} "
        f"| search evals used: {budget.n} / {GD_BUDGET} calls")
    # GD's own holdout verification (3 calls, inside its 186)
    mode, K, pd, delta = gd_cfg
    hv = run5(mode, K, pd, delta, STRESS["drift"], STRESS["lat"], seeds=HOLDOUT, budget=budget)
    say(f"  GD holdout verify (in-budget): pct={hv['pct']} debt={hv['debt']} maxE={hv['maxerr']}")
    say(f"  GD lane total call spend: {budget.n} / {GD_BUDGET}")

    champ = head_to_head(CHAMP, "CHAMPION")
    gd = head_to_head(gd_cfg, "GD ARM")
    v = verdict(champ, gd, gd_cfg)
    say(f"\nVERDICT: {v}")
    say(f"C1-BODY {hashlib.sha256(('\n'.join(LINES)).encode()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
