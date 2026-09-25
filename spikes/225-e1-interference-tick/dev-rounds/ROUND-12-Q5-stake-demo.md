# ROUND 12 — Q5 §3.2 stake demo: equal-budget GD control arm

Branch g3-kinduction. Pre-registration committed BEFORE any comparison
numbers were read (round-11 pattern, cf. 39e893c). Harness:
`q5_stake_demo.py`; captured output: `q5-stake-demo-output.txt`.

## Hypothesis

The selection-bias objection [CHARTER §5.1]: the banked champion
(interference K=1/pd=2/d16, 96.1% stress) may be an artifact of searching
only the interference family. Cure [§5.1, RESEARCH-AGENDA Q5]: an
equal-budget control arm that is NOT a family-restricted grid — a
discrete-greedy coordinate-descent local search over the FULL arena
strategy space (mode ∈ {sequential, interference}, K ∈ 1..8, pulse_div ∈
1..8, delta ∈ 4..24), integer-only, seeded at the pre-round-1 state of
knowledge (granite r1 banked champion K=5/pd=4/d16), fitness = the same
selection metric the family search promoted on (stress pct on primary
seeds, tie-break lower debt).

## Budget accounting (exact, from round-1 o1_k_replay.py output)

Round-1 discovery search consumed, in e1.run calls (1 call = 4800 ticks,
one seed):

| phase | calls |
|---|---|
| Phase 1 static probes: 9 entries × 3 frames × 5 seeds | 135 |
| Phase 1 calm-axis rows: 7 entries × 5 seeds | 35 |
| Phase 2 LLM proposals: 2 × 5 seeds | 10 |
| Phase 3 holdout verify: 2 entries × 3 seeds | 6 |
| **total discovery budget** | **186** |

Phase 0 control arms (50 calls) replayed already-published numbers
(byte-match gates, not exploration) — excluded from both sides equally.

GD lane budget: **186 calls total**, enforced by a hard counter: search
fitness evals capped at 183, plus its own 3-seed holdout verification
(3 calls), mirroring round-1's in-budget holdout. Each fitness eval = 5
calls (5 primary seeds) → up to 36 candidate evaluations.

## Pre-registered decision rule (committed before results)

Head-to-head: champion vs GD final on 3 frames (stress@own-delta,
gentle d6/drift3/lat5, lcalm d12/drift3/lat5), seeds 1/7/42/1999/20260902,
integer-only, plus 3-seed stress holdout (11/313/8888).

- **V1 OBJECTION LANDS**: GD beats champion by ≥ 1.0pp on stress AND on
  both calm frames → selection-bias objection lands; family search demoted.
- **V2 THIN MARGIN**: |GD − champ| < 1.0pp on stress and V1 not met →
  family advantage real but thin; book margin.
- **V3 OBJECTION REFUTED**: GD loses by > 1.0pp on stress → family search
  vindicated.
- **Special case**: GD final config == champion config (mode,K,pd,delta)
  → **V3-STRONG**: the optimum is findable by an unsteered equal-budget
  local search from outside the family-restricted grid; the win is a
  property of the substrate, not of where we looked.

## Pre-registered canaries

- C1 byte-identity: full pipeline run twice; sha256 of output body must match.
- C2 champion anchor replay: K1/pd2/d16 stress (96.1, 121762, 33); old
  champion K5/pd4/d16 stress (93.2, 132823, 38); impulse d16 stress
  (96.0, 139949, 61); champion gentle (98.0, 103116, 27). FAIL halts claims.
- C3 self-canaries: (a) fitness-inverted greedy from same seed must end
  strictly worse (search-machinery teeth); (b) anchor gate fed a
  deliberately wrong value must FAIL (gate teeth).

## Results (run of 2026-09-03 ~17:4x AKDT, pre-reg commit b354154)

Canaries: C1 PASS (double run byte-identical; body sha256
`497fcdc3…06`). C2 PASS 4/4 (champion stress 96.1/121762/33, old champ
93.2/132823/38, impulse d16 96.0/139949/61, champion gentle 98.0/103116/27).
C3a CAUGHT (inverted greedy descended 93.2→13.7, sequential/d8);
C3b CAUGHT (wrong-anchor gate fired FAIL as designed).

GD arm trace (183/186 calls spent, 36 candidate evals): seed
(interference, 5,4,16) 93.2% → **step 1 flips mode to sequential (96.0%)**
→ rides the delta ridge 17→22 (pct flat 96.0, debt 139949→92295) → stops at
**(sequential, K=5, pd=4, delta=22)**, stress 96.0%, debt 92295, maxE 61.

Head-to-head (champion vs GD arm):

| frame | champion | GD arm | Δ (GD−champ) |
|---|---|---|---|
| stress (primary 5 seeds) | 96.1 (debt 121762, maxE 33) | 96.0 (debt 92295, maxE 61) | **−0.1pp** |
| gentle d6/drift3/lat5 | 98.0 (debt 103116, maxE 27) | 56.6 (debt 117198, maxE 53) | **−41.4pp** |
| lcalm d12/drift3/lat5 | 98.0 (debt 94625, maxE 27) | 98.0 (debt 55545, maxE 53) | +0.0pp |
| holdout stress 11/313/8888 | 96.1 (debt 72518, maxE 35) | 96.0 (debt 55317, maxE 61) | −0.1pp |

Rule application: V1 needs ≥+1.0pp stress AND both calm frames — no.
V3 needs GD < champ by >1.0pp on stress — no (−0.1pp).
**→ V2-THIN-MARGIN fires by the letter of the pre-registration.**

## Verdict

**V2-THIN-MARGIN (booked per pre-registration).** On the crowning metric
(stress %within), an unsteered equal-budget discrete-greedy control arm —
seeded at pre-round-1 knowledge, free to leave the interference family,
and in fact leaving it at its very first move — comes within 0.1pp of the
champion (96.0 vs 96.1) with lower ledger debt. The selection-bias
objection therefore lands *partially on stress*: the family restriction
bought essentially nothing there; a plain mode-flip + delta-ride matches.
What the family search actually banked is **regime robustness**: the GD
arm collapses on the gentle calm frame (−41.4pp, 98.0→56.6) and carries
maxE 61 vs 33, exactly the leaderboard-impulse calm-specialist fragility
the Variety Ledger predicted. Family search is NOT demoted (V1 failed);
the stress margin is thin and now honestly booked as such (V2); the
champion's real edge is triple-frame domination, not the stress number.

## Scars

- **Greedy is mode-locked at step 1.** First-improvement accepted the
  sequential flip (93.2→96.0) and never returned; the interference family
  contains configs ≥96.1 but the unsteered local search cannot reach them
  from this seed without a non-local jump. Search-structure sensitivity is
  a live confound for ANY single-arm comparison — booked, not resolved.
- **Fitness was stress-only, by design** (matching the family search's
  promotion metric). A multi-frame fitness would have caught the gentle
  collapse during search; the champion's banked value is precisely that it
  didn't need to be told. Round-1's calm-axis rows served that role for the
  family search; an honest future control should score all frames in-budget.
- **Debt tie-break favors the GD arm on stress** (92295 vs 121762) — the
  champion survives on pct alone; the margin is thinner than the ledger's
  "triple-axis Pareto domination" phrasing suggests against this opponent.
- Anchor-#1 run of the harness had a frame-delta bug (calm frames used the
  arm's delta); caught by the C2 gentle anchor gate before any comparison
  numbers were produced. Gate machinery earned its keep.

## Headline

"0.1pp on stress, 41pp on calm" — the equal-budget unsteered control arm
matches the champion where the champion was crowned, and falls off a cliff
where the family search was never told to look: V2-THIN-MARGIN booked, the
selection-bias objection half-refuted, and the champion's crown quietly
moves from "96.1%" to "96.1% everywhere".
