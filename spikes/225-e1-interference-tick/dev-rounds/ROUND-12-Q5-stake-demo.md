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

## Results

(to be booked after the pre-reg commit)

## Verdict

(pending)

## Scars

(pending)

## Headline

(pending)
