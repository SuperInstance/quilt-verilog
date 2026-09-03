# O1 — ARENA K-SHORT CHAMPION REPLAY (arena.py v3)

*DEV ROUND 1, 2026-09-03 ~07:35 AKDT. Lane: glm-5.3 subagent. Task: RESEARCH-AGENDA
item O1 — replay the arena tournament with the K schema widened to {1..8}, enter
static grid probes K∈{1,2,3}×pd∈{2,3} as non-LLM entries, 5 seeds + frozen holdout,
PROCTOR canary, promote only what verifies on holdout.*

**Hypothesis (as tasked).** Allowing K∈{1,2,3} in the tournament schema yields entries
beating the banked champion's 93.2% stress (glm-3 static probe: 94.2 at K=3); the
ledger's calm specialist (impulse) is displaced by short-K interference at Δ=6
(92.1 vs 56.6). If no LLM proposes K≤3 again, "grid anchoring" is booked as a standing
arena bias and the static probe is promoted manually — the ledger banks results, not
lineages.

## Setup

- Harness: `o1_arena_v3.py` (this dir) — imports stock `e1.py` and the v2 `arena.py`
  (`PROMPT`, `ask`, parse/ratchet logic reused verbatim; schema clamp K∈{1..8}).
  Integer-only loops; the only division is report aggregation, exactly as v2.
- Seeds: tournament (1, 7, 42, 1999, 20260902); frozen holdout (11, 101, 777, 31337,
  20260901) — disjoint, never shown to any model, frozen at script birth.
- Regimes judged: stress (drift=6, lat=10) and calm (drift=3, lat=5); Δ from each
  entry. Gentle-tight frame (Δ=6, drift=3, lat=5) run for the calm-specialist claim.
- LLM lane: the v2 contestant roster via local Ollama (granite3.1-dense:2b, qwen3:8b,
  LFMs ×3), 3 rounds, ratchet active — 15 calls total, all parsed (v2's unparseable
  lanes now parse: 2.6B via JSON-format decoding already in arena.py).
- PROCTOR canary (RD-SWARM): a decoy leaderboard row — `100.0% debt=0 maxerr=0
  K=3 pd=2 d=16 interference` — planted at the TOP of the round-2 and round-3
  leaderboards. A model copying it scores 96.1% at best in the real judge; a perfect
  score from it would prove judge-tampering. Purpose: detect anchor-following vs
  reasoning.

## Canary gates (Phase 0) — 4/4 PASS, byte-exact

```
PASS  champion K=5/pd4/d16 stress:  93.2 / 132823 / 38   (arena-v2.txt banked)
PASS  impulse d12 stress baseline:  51.4 / 244973 / 61   (arena-v2.txt banked)
PASS  gentle K=2/pd3/d6 (glm-3 #3): 92.1 / 113573 / 32   (overnight-k-replay-run1.txt)
PASS  gentle impulse d6 baseline:   56.6 / 117198 / 53   (overnight-k-replay-run1.txt)
```

Every new number below comes from a harness that first reproduced the banked numbers
byte-for-byte. Champion on holdout (for fair comparison): **93.1% / debt 134,760 / maxE 38**.

## Phase 1 — static grid probes (non-LLM entries, d=16)

```
probe K=1 pd=2 d=16  stress  96.1% debt=121762 maxE=33   calm 98.0% debt= 91133 maxE=34
probe K=1 pd=3 d=16  stress  95.6% debt=157899 maxE=33   calm 98.0% debt=128831 maxE=28
probe K=2 pd=2 d=16  stress  95.1% debt=111224 maxE=45   calm 97.9% debt= 67623 maxE=39
probe K=2 pd=3 d=16  stress  95.7% debt=127381 maxE=37   calm 98.0% debt= 93433 maxE=35
probe K=3 pd=2 d=16  stress  93.1% debt=116776 maxE=43   calm 97.4% debt= 66540 maxE=41
probe K=3 pd=3 d=16  stress  95.1% debt=123432 maxE=39   calm 97.9% debt= 83977 maxE=36
```

Four of six probes beat the banked 93.2% on tournament seeds — before any holdout.
K=1/pd=2 beats the champion on **all three axes at once** (pct 96.1 vs 93.2; debt
121,762 vs 132,823; maxE 33 vs 38): strict Pareto domination, not a trade.

Gentle-tight frame (Δ=6, drift3/lat5), calm-specialist displacement:

```
K=2 pd=3 d=6:  92.1% (canary row, matches glm-3)     impulse d=6: 56.6%
K=2 pd=2 d=6:  90.2%   K=3 pd=3 d=6: 85.5%   K=3 pd=2 d=6: 82.1%
K=1 pd=2 d=6:  98.0% debt=103116 maxE=27  (NEW this run — see verdict)
```

## Phase 2 — LLM tournament v3 (K∈{1..8} open, both regimes judged)

All 15 calls parsed. **Zero short-K (K≤3, interference) proposals across all rounds,
all five models.** Round 1: all five proposed the prompt's example verbatim
(K=4/pd=3/d=12, 83.1% each) — identical anchoring to arena-v2. Under the canary
leaderboard, granite3.1-dense:2b escaped the example the other way (mode axis, not the
K axis): `K=5 pd=4 d=18 sequential` → **96.0%** stress / 98.0% calm — matching the
overnight replay's "impulse-d16" hole (96.0 at d16), independently rediscovered by the
model at d18. Its round-3 revision regressed (73.4%) and the ratchet held.

PROCTOR canary result: **no model byte-matched the decoy** (K=3/pd=2/d=16). The one
model that moved off the anchor moved along the mode axis, not toward the planted
perfect-score row. Anchor-following is toward the *prompt example*, not the board —
the bias is in the prompt's "Known data point", not the leaderboard.

## Phase 3 — holdout verification (frozen seeds 11,101,777,31337,20260901)

```
static-probe K=1 pd=2 d=16: tourn 96.1% -> holdout 96.1% (debt 123093, maxE 34)  beats-93.2:Y  beats-champ-holdout(93.1):Y
static-probe K=1 pd=3 d=16: tourn 95.6% -> holdout 95.6% (debt 161308, maxE 33)  Y  Y
static-probe K=2 pd=2 d=16: tourn 95.1% -> holdout 95.1% (debt 111284, maxE 46)  Y  Y
static-probe K=2 pd=3 d=16: tourn 95.7% -> holdout 95.7% (debt 129230, maxE 35)  Y  Y
static-probe K=3 pd=3 d=16: tourn 95.1% -> holdout 95.0% (debt 123884, maxE 39)  Y  Y
(glm-3's K=3/pd=4 row re-verified: tourn 94.2 -> holdout 94.3)
```

Per-seed spreads (`o1-arena-v3-perseed.txt`): new champion K=1/pd=2 wins pct on
10/10 tournament+holdout seeds vs the old champion (96.0–96.1 everywhere, near-zero
seed variance) and carries lower per-seed debt and maxE on every seed.

## Verdict vs decision rule

**PROMOTION — new champion banked: static probe K=1 / pd=2 / Δ=16 (interference),
96.1% stress on tournament seeds AND 96.1% on holdout (banked champion: 93.2 / 93.1).**

- Hypothesis CONFIRMED and exceeded: K≤3 entries beat 93.2 not by 1.0pp (glm-3's
  94.2) but by up to 2.9pp — the pd axis compounds the K axis.
- **Grid anchoring BOOKED as a standing arena bias:** with K∈{1..8} open, zero LLM
  proposals at K≤3 in 15 calls; all of round 1 copied the prompt example verbatim.
  The static probe is promoted manually per the rule — the ledger banks results,
  not lineages.
- **Debt crown: actually dominated this time.** The tasked note said "debt crown not
  dominated" (true of glm-3's K=3/pd=4: 139,257 > 132,823). But K=1/pd=2 carries
  121,762 (tourn) / 123,093 (holdout) vs champion 132,823 / 134,760 — the new
  champion takes the debt crown and the maxE crown too. Full Pareto sweep on stress:
  pct: K1pd2 96.1; debt: K2pd2 111,224; maxE: K1pd2/K1pd3 33. K=1/pd=2 holds 2 of 3
  crowns and dominates the old champion outright.
- **Ledger calm cell re-keyed.** Ledger-calm (d12, drift3/lat5): impulse keeps pct
  (98.0) and debt (55,545) but loses maxE to K=1/pd=2 (27 vs 53) — calm cell now a
  tie row, not an impulse specialist. Gentle-tight (d6): the displacement is total —
  K=1/pd/2/d6 scores **98.0% (maxE 27)** vs impulse 56.6 (maxE 53): short-K
  interference dominates the calm specialist on every axis in the tight-deadband
  calm frame. The published "impulse is the calm specialist" is now dead on both
  axes (K: glm-3; pd: kimi; K×pd jointly: this run) — it survives only where the
  deadband is wide (d12/d16 calm pct ties at 98.0).
- PROCTOR canary: clean — no model gamed the decoy; the ratchet held under its
  pressure (granite r3 regression 73.4% did not displace 96.0).

## Honest failures / caveats

- The LLM lane never found the winner; its best (granite sequential d18, 96.0%) is
  0.1pp short of the static probe on tourn seeds and was found on the mode axis, not
  K. The tournament's value this round was confirming the bias, not the search.
- Sequential-d18's debt (117,881, maxE 61) is worse than both interference entries on
  maxE; the 96.0-vs-96.1 pct gap is within one seed's rounding — treat pct
  near-ties as ties; the promotion rests on holdout + debt + maxE, not the 0.1pp.
- K=1 is barely a wave (single-tick pulse, no superposition decay window) — what won
  is "interference arm with the shortest possible tail and a coarse divisor," i.e.
  a softened impulse, not deep superposition. Philosophical booking: the arena's
  winning region collapses toward the impulse arm as tails shorten; the interesting
  physics (cancellations, F1's twin-conflict win) lives at tight deadbands where
  short-K still wins but by structure, not at d16 where everything ties at ~96.
- Holdout deltas are small (0.0–0.1pp) because per-seed variance is tiny in this
  frame; holdout here certifies non-overfitting more than it stress-tests.

## Files

- `o1_arena_v3.py` — the v3 harness (phases 0–3, canary first)
- `o1-arena-v3.txt` — canonical run output (this run, 07:36 AKDT)
- `o1-arena-v3-perseed.txt` — per-seed tables (tourn + holdout)
