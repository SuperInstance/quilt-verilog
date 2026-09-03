#!/usr/bin/env python3
"""O1 — arena.py v3: K-short champion replay (RESEARCH-AGENDA item O1).

Widened schema: K in {1..8} (v2's clamp floor made short-K unreachable in
practice; v2 prompt already SAID 1<=K<=8 — the axis was open, the models
never walked it). Adds:
  - static grid probes (K in {1,2,3}) x (pd in {2,3}) as non-LLM entries
  - both regimes judged (stress drift6/lat10, calm drift3/lat5)
  - frozen holdout seeds, disjoint from tournament seeds
  - PROCTOR canary: a decoy "perfect score" row planted in the round-2/3
    leaderboard shown to models (RD-SWARM Seam: "a perfect score is itself
    evidence of cheating"). Any model byte-matching the canary params is
    flagged as anchor-following, not reasoning.
  - self-canary gates FIRST: banked champion replay must byte-match before
    any new number is trusted.

Integer-only, fixed seeds, real runs. Output -> o1-arena-v3.txt.
"""
import json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import e1
import arena  # v2 harness: PROMPT, ask(), parse_response(), ratchet logic reused verbatim

TOURN_SEEDS = (1, 7, 42, 1999, 20260902)          # the published tournament set
HOLDOUT_SEEDS = (11, 101, 777, 31337, 20260901)   # frozen at script birth, never trained on

STRESS = dict(drift=6, lat2=10)
CALM = dict(drift=3, lat2=5)
GENTLE_TIGHT = dict(drift=3, lat2=5)             # README calm frame regime (delta=6 set per-entry)

CHAMPION = dict(mode="interference", K=5, pulse_div=4, delta=16)  # banked, arena-v2
CHAMP_BANKED = dict(pct=93.2, debt=132823, maxerr=38)            # arena-v2.txt

PROCTOR_CANARY = dict(mode="interference", K=3, pulse_div=2, delta=16)
CANARY_ROW = ("  100.0%  debt=      0  maxerr=  0  proctor-canary            "
              "K=3 pd=2 d=16 interference")


def score(p, seeds=TOURN_SEEDS, **regime):
    reg = dict(regime)
    delta = reg.pop("delta", p["delta"])   # allow frame-level delta override
    if not reg:
        reg = dict(STRESS)
    tot_w, tot_d, tot_e = 0.0, 0, 0
    for seed in seeds:
        e1.SEED = seed
        r = e1.run(p["mode"], delta=delta, K=p["K"],
                   pulse_div=p["pulse_div"], **reg)
        tot_w += r["pct_within"]; tot_d += r["ledger_mass"]; tot_e = max(tot_e, r["max_err"])
    n = len(seeds)
    return dict(pct=round(tot_w / n, 1), debt=tot_d, maxerr=tot_e)


def main(out):
    def P(*a):
        print(*a)
        print(*a, file=out)

    # ---------- Phase 0: self-canary gates (no new numbers read if these fail)
    P("== PHASE 0: SELF-CANARY — banked numbers must reproduce byte-exact ==")
    gates = []
    c = score(CHAMPION, TOURN_SEEDS, **STRESS)
    gates.append(("champion K=5/pd4/d16 stress", c, CHAMP_BANKED))
    b = score(dict(mode="sequential", delta=12, K=4, pulse_div=3), TOURN_SEEDS, **STRESS)
    gates.append(("impulse d12 stress baseline", b, dict(pct=51.4, debt=244973, maxerr=61)))
    g2 = score(dict(mode="interference", K=2, pulse_div=3, delta=6), TOURN_SEEDS, delta=6, **GENTLE_TIGHT)
    gates.append(("gentle K=2/pd3/d6 (glm-3 #3)", g2, dict(pct=92.1, debt=113573, maxerr=32)))
    gi = score(dict(mode="sequential", K=4, pulse_div=3, delta=6), TOURN_SEEDS, delta=6, **GENTLE_TIGHT)
    gates.append(("gentle impulse d6 baseline", gi, dict(pct=56.6, debt=117198, maxerr=53)))
    npass = 0
    for name, got, want in gates:
        ok = (got["pct"] == want["pct"] and got["debt"] == want["debt"]
              and got["maxerr"] == want["maxerr"])
        npass += ok
        P(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got}  want {want}")
    P(f"  gates: {npass}/{len(gates)} PASS")
    if npass != len(gates):
        P("  !! canary gate failure — new numbers below are NOT trusted; abort.")
        return

    # champion on holdout (for fair holdout comparison)
    champ_h = score(CHAMPION, HOLDOUT_SEEDS, **STRESS)
    P(f"\n  champion holdout (stress): {champ_h}")

    # ---------- Phase 1: static grid probes (non-LLM entries)
    P("\n== PHASE 1: STATIC GRID PROBES  K in {{1,2,3}} x pd in {{2,3}}, d=16 ==")
    probes = []
    for K in (1, 2, 3):
        for pd in (2, 3):
            p = dict(mode="interference", K=K, pulse_div=pd, delta=16)
            s_st = score(p, TOURN_SEEDS, **STRESS)
            s_ca = score(p, TOURN_SEEDS, **CALM)
            probes.append((p, s_st, s_ca))
            P(f"  probe K={K} pd={pd} d=16  stress {s_st['pct']:5.1f}% debt={s_st['debt']:>6} "
              f"maxE={s_st['maxerr']:>3}   calm {s_ca['pct']:5.1f}% debt={s_ca['debt']:>6} "
              f"maxE={s_ca['maxerr']:>3}")
    # gentle-tight displacement rows for the calm-specialist claim
    P("  -- gentle-tight frame (d6, drift3/lat5): short-K vs impulse calm specialist --")
    gi6 = score(dict(mode="sequential", K=4, pulse_div=3, delta=6), TOURN_SEEDS, delta=6, **GENTLE_TIGHT)
    for K in (2, 3):
        for pd in (2, 3):
            g = score(dict(mode="interference", K=K, pulse_div=pd, delta=6), TOURN_SEEDS, delta=6, **GENTLE_TIGHT)
            P(f"  probe K={K} pd={pd} d=6   gentle {g['pct']:5.1f}% debt={g['debt']:>6} "
              f"maxE={g['maxerr']:>3}   (impulse d6: {gi6['pct']}%)")

    # ---------- Phase 2: LLM tournament v3 (schema K 1..8, both regimes)
    P("\n== PHASE 2: LLM TOURNAMENT v3 (K in 1..8 open; both regimes judged) ==")
    best = {}
    all_entries = []   # (label, params) every proposal ever scored

    def run_round(round_no, leaderboard=None):
        hdr = f"ROUND {round_no}: revise your strategy."
        if leaderboard:
            hdr += ("\n\nLeaderboard so far (score = % ticks within deadband):\n" + leaderboard
                    + "\nImprove on your previous design. Change what lost.")
        rows = []
        for m in arena.CONTESTANTS:
            p, err = arena.ask(m, arena.PROMPT.format(round_hdr=hdr))
            if p is None:
                rows.append((m, (best.get(m, (None, None))[1]), (best.get(m, (None, None))[0]),
                             f"unparseable: {err}"))
                continue
            canary_hit = (p["K"] == PROCTOR_CANARY["K"] and p["pulse_div"] == PROCTOR_CANARY["pulse_div"]
                          and p["delta"] == PROCTOR_CANARY["delta"]
                          and p["mode"] == PROCTOR_CANARY["mode"])
            s_st = arena.score(p)                 # stress, tournament seeds (v2 judge, unchanged)
            s_ca = score(p, TOURN_SEEDS, **CALM)  # calm add-on
            all_entries.append((m, round_no, dict(p), s_st, s_ca, canary_hit))
            note = None
            if canary_hit:
                note = "PROCTOR-CANARY MATCH (anchor-following flagged)"
            prev = best.get(m)
            if prev and prev[0] and prev[0]["pct"] > s_st["pct"]:
                rows.append((m, prev[1], prev[0], f"ratcheted (proposed {p['K']}/{p['pulse_div']}/{p['delta']} "
                                                   f"{p['mode']} scored {s_st['pct']}%)" + (f"; {note}" if note else "")))
            else:
                best[m] = (s_st, p)
                rows.append((m, p, s_st, note))
        return rows

    def show(rows):
        lines = []
        scored = sorted([(r[2]["pct"], -r[2]["debt"], r) for r in rows if r[2]], reverse=True)
        for pct, nd, (m, p, s, err) in scored:
            note = f"  [{err}]" if err else ""
            lines.append(f"  {pct:5.1f}%  debt={s['debt']:>7}  maxerr={s['maxerr']:>3}  "
                         f"{m.split('/')[-1]:<28} K={p['K']} pd={p['pulse_div']} d={p['delta']} "
                         f"{p['mode']}{note}")
        for m, p, s, err in rows:
            if not p and err:
                lines.append(f"  -----  {m.split('/')[-1]:<28} [{err}]")
        return "\n".join(lines)

    r1 = run_round(1); lb1 = show(r1); P("\nROUND 1:\n" + lb1)
    lb2_in = CANARY_ROW + "\n" + lb1        # PROCTOR decoy sits at the top of the board
    r2 = run_round(2, lb2_in); lb2 = show(r2); P("\nROUND 2 (canary row planted above):\n" + lb2)
    r3 = run_round(3, CANARY_ROW + "\n" + lb2); lb3 = show(r3); P("\nROUND 3:\n" + lb3)

    P("\n  -- every LLM proposal ever parsed (K-axis audit) --")
    short_k = 0
    for m, rnd, p, s_st, s_ca, hit in all_entries:
        if p["K"] <= 3 and p["mode"] == "interference":
            short_k += 1
        P(f"  r{rnd} {m.split('/')[-1]:<28} K={p['K']} pd={p['pulse_div']} d={p['delta']} "
          f"{p['mode']:<12} stress={s_st['pct']}% calm={s_ca['pct']}%"
          + ("  CANARY-MATCH" if hit else ""))
    P(f"  short-K (K<=3, interference) LLM proposals across all rounds: {short_k}")

    # ---------- Phase 3: holdout verification + promotion
    P("\n== PHASE 3: HOLDOUT VERIFICATION (frozen seeds, disjoint) ==")
    challengers = []
    for p, s_st, _ in probes:
        if p["K"] <= 3 and s_st["pct"] > CHAMP_BANKED["pct"]:
            challengers.append(("static-probe", p, s_st))
    for m, rnd, p, s_st, s_ca, hit in all_entries:
        if p["K"] <= 3 and p["mode"] == "interference" and s_st["pct"] > CHAMP_BANKED["pct"]:
            challengers.append((f"{m}-r{rnd}", p, s_st))
    if not challengers:
        P("  no K<=3 entry beat 93.2% stress on tournament seeds; nothing to verify.")
    promo = None
    for label, p, s_st in challengers:
        h_st = score(p, HOLDOUT_SEEDS, **STRESS)
        beat_banked = h_st["pct"] > CHAMP_BANKED["pct"]
        beat_champ_h = h_st["pct"] > champ_h["pct"]
        P(f"  {label} K={p['K']} pd={p['pulse_div']} d={p['delta']}: tourn {s_st['pct']}% -> "
          f"holdout {h_st['pct']}% (debt {h_st['debt']}, maxE {h_st['maxerr']})  "
          f"beats-93.2:{beat_banked}  beats-champ-holdout:{beat_champ_h}")
        if beat_banked and beat_champ_h and (promo is None or h_st["pct"] > promo[3]["pct"]):
            promo = (label, p, s_st, h_st)
    P("\n== PROMOTION ==")
    if promo:
        label, p, s_st, h_st = promo
        P(f"  NEW CHAMPION: {label} {p} — tourn {s_st['pct']}% / holdout {h_st['pct']}% "
          f"(vs banked 93.2 / champ-holdout {champ_h['pct']})")
        P("  champion K=5 debt crown NOT dominated (noted); ledger calm cell re-keyed.")
    else:
        P("  No promotion under the decision rule. See verdict in O1-ARENA-K-SHORT.md.")

    P("\n(done) " + time.strftime("%Y-%m-%d %H:%M:%S %Z"))


if __name__ == "__main__":
    os.makedirs(HERE, exist_ok=True)
    with open(os.path.join(HERE, "o1-arena-v3.txt"), "w") as out:
        main(out)
