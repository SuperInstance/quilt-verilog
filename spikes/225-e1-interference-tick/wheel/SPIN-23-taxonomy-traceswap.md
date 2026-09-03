# SPIN-23 — TAXONOMY TRACE-SWAP (SPIN-20 follow-up #2, filed by SPIN-21)

**Spoke:** TAXONOMY · **Date:** 2026-09-03 (pre-registration written BEFORE any run)
**Files:** `spin23_taxonomy_traceswap.py`, `spin23-output.txt`
**Base:** SPIN-17's oscillation-tax taxonomy arms, SPIN-21's integer trace generator, instrument `dyn_run` (reality_fn + k as parameters, spin-21 clone). Integer-only in-loop; floats only at print time; single-pass inline; no pipes.

## Question (SPIN-21's next-spoke filing)

Spin 17 measured the regime-switching tax against ONE reality — the ramp sea
(R0: ramp96 +8/5, descents, 240-cycle). Which tax classes survive the trace
swap, and which were the ramp talking?

## Traces (SPIN-21 code reused VERBATIM: r2_triangle, r4_sawtooth, r3_plateau)

All period 240, band ~400–553, integer. Rationale: triangle = same 8/5 slope
family but symmetric; sawtooth = slow slope 1.0 + jump; plateau = 0-slope +
jump (the SPIN-21 prediction: the 27pp tax should collapse toward the Jensen
floor there).

## Tax classes under test (Spin-17 exact anchors, all @ P=16, 5↔30 unless noted)

| ID | class | Spin-17 anchor (R0, 5-seed) | discriminating signature |
|----|-------|------------------------------|--------------------------|
| T1 | **Amplitude gate** | tax: 25-spread 27.0 > 15-spread 22.8 > 5-spread 0.6 (K=2, pairs 5↔30/10↔25/15↔20) | tax monotone ↓ in spread AND spread-5 tax < 3pp (gate kills it) |
| T2 | **Duty / guerrilla asymmetry** | tax: duty25 36.3 > duty50 27.0 > duty75 12.7 (K=2) | tax monotone ↓ in duty (worst when good regime dominates) |
| T3 | **Phase (timing/alignment)** | lo-first 27.0 vs hi-first 32.0 (K=2, same duty, same transitions) | hi-first tax ≥ lo-first (Δ = −5.1pp osc on R0) |
| T4 | **K=2 catastrophe spike** | tax @P=16: K=2 27.0 vs K=1 5.1 / K=4 6.5 / K=8 7.5 | K=2 tax exceeds every other K by ≥3pp |

## PRE-REGISTERED PREDICTIONS (before any panel run)

- **T1 amplitude gate: SURVIVES on slope traces (triangle, sawtooth), DIES on plateau.** The gate is trigger-set separation; a jump-dominated reality with 0-slope plateaus never separates error profiles gradually — predicted spread-5 ≈ spread-25 on plateau. Overall: survives (2/3).
- **T2 duty asymmetry: SURVIVES all three.** The guerrilla mechanism (brief bad pulses into a good background firing wrong trigger sets) is fabric-local; SPIN-21 already showed brief-bad-traces (its own jump/duty structure) amplify K=2 damage. Predicted survives 3/3, with plateau's margins compressed.
- **T3 phase: INDETERMINATE, leaning trace-coupled.** The phase effect is alignment with reality's 240-cycle. Triangle/sawtooth/plateau are all period-240 like R0, so some alignment effect should persist, but the sign of the alignment is a ramp-specific accident (P=16 divides 240). Predict ≥1 flip or near-zero Δ on ≥2 → indeterminate/trace-coupled.
- **T4 K=2 spike: SURVIVES all three.** SPIN-21 proved the zero-lock K=2 flip is a fabric law (7/7, incl. these 3 traces); the tax version is the same pulse-overlap lifetime mechanism. Predicted survives 3/3.

## DECISION RULE (pre-stated, verbatim contract)

Panel seeds {1,7,42} (3-seed, per task spec); 4800 ticks; integer-only.
For each class T1–T4 and each new trace τ ∈ {triangle, sawtooth, plateau},
evaluate the class's signature *within* trace τ:

- A pairwise ordering step "holds" on τ if same direction as R0's anchor,
  OR the two values are within ±3pp (neutral tie, counted as holding).
  An ordering step "flips" if opposite direction with margin > 3pp.
- **survives**: direction (overall monotonicity / signature) holds on ≥2 of 3 traces;
- **trace-coupled**: direction flips on ≥2 of 3;
- **indeterminate**: otherwise (e.g. 1 hold, 1 flip, 1 ambiguous).
- T4's single comparison (K=2 vs max(other K)) "holds" if margin ≥3pp same direction.

## CANARIES (mandatory gate, before any panel cell counts)

1. **spread=0 byte-identity:** square_schedule(lo=hi=5) through the scheduler
   path == static-5, per new trace, K∈{1,2,4,8} × seeds{1,7,42}, byte-identical.
2. **ladder@15 K=1 = 71.5 exact** on R0 (5-seed mean, ±0.2pp), plus zero@15 K=1 77.3.
3. **SPIN-21 K=2 floor ≥7.5pp reproduces:** zero-grammar K=2 trough
   (min(K1,K4)−K2, 5-seed mean) ≥ 7.5pp on EVERY rerun trace
   (SPIN-21: triangle 18.5 / sawtooth 26.6 / plateau 7.5).

## Stages

1. This pre-registration (commit before running).
2. Script + run + raw output.
3. Book: verdict table (class × trace), scars, follow-up, WHEEL-LOG line.
