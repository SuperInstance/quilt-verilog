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

---

## RESULTS (booked after the run; elapsed 4 s; all canaries PASS)

Canaries: (1) spread=0 byte-identity 36/36 PASS; (2) ladder@15 K=1 = 71.5 and
zero@15 K=1 = 77.3 EXACT; (3) SPIN-21 K=2 floor reproduces: triangle 18.5 /
sawtooth 26.6 / plateau 7.5pp — all ≥7.5, PASS.

### Verdict table (class × trace, pre-registered rule)

| class | triangle | sawtooth | plateau | VERDICT |
|-------|----------|----------|---------|---------|
| T1 amplitude gate (25>15>5 + gate<3pp) | hold (+1,+1,gate Y) | **FLIP** (15-spread tax 27.5 > 25-spread 11.7, margin 15.8pp) | tie/gate fails (spread-5 tax 6.9pp) | **INDETERMINATE** |
| T2 duty/guerrilla (25>50>75) | hold 30.4>25.2>10.3 | hold 22.6>11.7>9.6 (last step tie) | hold 35.4≈36.7>14.8 | **SURVIVES (3/3)** |
| T3 phase (hi-first ≥ lo-first) | hold (+0.9pp, tie) | hold (**+24.4pp**) | hold (+0.9pp, tie) | **SURVIVES (weak)** — direction 3/3, magnitude collapses to ~1pp except sawtooth |
| T4 K=2 spike (K2 > others by 3pp) | hold (+18.6) | hold (+8.3) | hold (+34.7) | **SURVIVES (3/3)** |

### One-line answer to SPIN-20/SPIN-21's question

**The K=2 spike, the guerrilla duty asymmetry, and the phase-alignment
direction are fabric laws (survive the trace swap); the amplitude ordering
was the ramp talking** — on the sawtooth the 10↔25 pair's tax (27.5pp)
EXCEEDS the 5↔30 pair's (11.7pp), flipping Spin-17's monotone ladder, and
the spread-5 "gate" leaks on the plateau (6.9pp residual).

### Notable honest findings

1. **SPIN-21's next-spoke prediction is FALSIFIED:** it predicted the 27pp
   regime tax "should collapse to the Jensen floor on a 0-slope reality."
   On the plateau the P=16 5↔30 K=2 tax is **36.7pp** — the LARGEST of all
   three traces. Jump-dominated realities don't mute the oscillation tax;
   they amplify it. (The zero-grammar trough is muted there (7.5pp), but
   that is a different quantity — the stale-grammar tax is not.)
2. **T3's magnitude is trace-coupled even though direction survives:** the
   R0 5.1pp phase effect shrinks to 0.9pp on triangle and plateau but
   EXPLODES to 24.4pp on the sawtooth (slow-rise realities punish phase
   alignment hardest). "Survives" here means direction only — book the
   magnitude as trace-property, echoing SPIN-21's split pattern.
3. **Sawtooth TWmean pathology:** its T1 flip is partly a baseline artifact
   (Spin-17 scar #2 recurring): on sawtooth, static-15 (10↔25 mean) sits
   far above static TWmean-5↔30; the ordering flip is real under the
   pre-registered TWmean convention but would need the matched-mean
   baseline to decompose (follow-up, not run — budget).

### Prediction scorecard (pre-registered vs actual)

- T1 SURVIVES 2/3 — **WRONG**: indeterminate (sawtooth flip, plateau gate leak).
- T2 SURVIVES 3/3 — **RIGHT**.
- T3 indeterminate/leaning coupled — **HALF**: direction survives 3/3 but
  magnitude collapses (the "leaning coupled" part was right).
- T4 SURVIVES 3/3 — **RIGHT** (and SPIN-21's floor canary held everywhere).

### Scars

1. **Cross-trace cache-key collision (caught by inspection before booking):**
  first run keyed the pct-cache by `fn.__name__` — every `_mk`-wrapped trace
  is named `g`, so triangle's numbers silently cloned onto sawtooth/plateau
  and all four classes "survived" identically. Lesson: cache keys for
  parameterized realities must carry an explicit trace label, never a
  function attribute. (Raw first-run output discarded; rerun is the booked
  one.)
2. 3-seed panel (per task spec) + ±3pp tie rule makes T2/T3 holds on some
   traces tie-graded; per-seed noise not re-estimated (SPIN-21 canary c
   covers determinism, not seed spread). Booked as judgment-constant
   boundary, same as SPIN-21's 5pp rule.

### Follow-up

Decompose the sawtooth T1 flip under the matched-mean static baseline
(Spin-17's dual-baseline scar) and sweep phase × slope on the sawtooth
family where the phase effect is 5× R0's — candidate new law: phase
sensitivity ∝ fraction of period spent on sustained slope.

Status: **COMPLETE.** Committed+pushed g3-kinduction. WHEEL-LOG appended.
