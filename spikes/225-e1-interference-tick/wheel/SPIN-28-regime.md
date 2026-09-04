# SPIN-28 — REGIME: JUMP-LADDER (does max per-tick jump J govern the oscillation tax?)

Dispatched 2026-09-03 16:31 AKDT (cron lane, spoke 6 REGIME, LCG state after SPIN-27).
Lane: wheel_spin28_regime · zai/glm-5.3 · run mode. ~3 s runtime.

## Hypothesis (pre-registered in spin28_regime.py header BEFORE any run)

SPIN-23 found the regime-oscillation tax amplitude ordering FLIPS on sawtooth
(15-spread tax 27.5 > 25-spread 11.7, margin 15.8pp — opposite of R0) and phase
magnitude is trace-coupled (sawtooth 24.4pp vs triangle/plateau ~1pp).
Hypothesis: BOTH are governed by trace slope AT transition edges — i.e. by the
max per-tick jump J. Predict: tax(P=16, K=2) amplitude ordering tracks J
(plateau J=153, triangle ~2, zigzag 2, sawtooth ~153, ramp144 ~2), and
phase-alignment sensitivity grows monotonically in J.
Falsify if amplitude ordering is J-independent or phase sensitivity non-monotone in J.

Pre-registered decision rules (verbatim in script header):
- **AMP PASS** iff BOTH big-J traces' dAmp (= tax_s25 − tax_s15) < EVERY slope-class
  trace's dAmp − 3pp, under BOTH TWmean and matched-mean baselines.
- **PHASE PASS** iff swing (max−min osc% over offsets 0..8, P=16 K=2 5↔30) has
  sawtooth > every slope-class swing + 3pp and no non-monotone trigger.
- VALIDATED = both PASS; FALSIFIED = both FAIL; else MIXED.

Note: integer traces quantize slope-class empirical J to 2 (8//5 alternates 1/2)
— the ladder has two empirical J classes (153/152 vs 2), not five rungs.

## Canaries (4/4 PASS)

| Canary | Result |
|---|---|
| (a) wiring byte-identity dyn_run(R0) vs run_fabric | PASS — 16 configs (4 grammars × K{1,2} × seeds{1,42}) |
| (b) R0 anchors, 5-seed | PASS — ladder15 K=1 pct 71.48/ev 5791.6/debt 106378.4 (71.5/5792/106378); zero K=1 77.26/187833.6 (77.3/187834) |
| (c) SPIN-23 replays | PASS — plateau P=16 K=2 TWmean tax 36.7 exact; sawtooth s15=27.5 s25=11.7 flip=+15.8pp exact |
| (d) double-run determinism | PASS — 30 dual runs byte-identical |

## Results

### EXP 1 — J-ladder, tax(P=16, K=2), spreads 15 (10↔25) / 25 (5↔30), both baselines, seeds {1,7,42}

| trace | J | dAmp (TWmean) | dAmp (matched-mean) |
|---|---|---|---|
| plateau | 153 | +2.1pp (tie) | **+12.8pp** (largest normal ordering) |
| triangle | 2 | +4.6pp | +9.7pp |
| zigzag96 | 2 | +6.9pp | +6.5pp |
| sawtooth | 152 | **−15.8pp (flip)** | −0.3pp (tie) |
| ramp144 | 2 | +3.7pp | +13.0pp |

Full cells (osc%/TWm%/taxTW/mmS%/taxMM) in spin28-output.txt. Highlights:
- Only sawtooth flips, only under TWmean. Under matched-mean its "flip"
  collapses to −0.3pp (mm static 73.6 dwarfs TWmean 45.9 — SPIN-23's sawtooth
  TWmean pathology, now quantified on the amplitude axis too).
- Plateau — SAME J-class (153 vs 152) — does not flip under either baseline;
  under matched-mean it has the STRONGEST normal ordering (+12.8pp).
- Strict pre-registered AMP rule: NOSEP under both baselines → **AMP FAIL**.

### EXP 2 — phase-offset sweep 0..8, P=16 K=2 5↔30, extreme-J traces

- plateau osc%: 2.5, 9.9, 9.2, 4.1, 4.3, 2.0, 2.6, 5.3, 3.4 → **swing 7.9pp**
- sawtooth osc%: 9.9, 18.3, 25.2, 10.4, 24.1, 30.9, 12.3, 15.8, 34.3 → **swing 24.4pp**
- Ladder is monotone across measured points: slope-class ~1pp (SPIN-23) <
  plateau 7.9 < sawtooth 24.4 → **PHASE PASS** (no non-monotone trigger).
- But: sawtooth's sweep is non-smooth (34.3 @ off=8 vs 12.3 @ off=6) —
  lattice-flavored, worth a fine sweep.

## VERDICT: **MIXED**

Headline: **at equal J≈153, plateau vs sawtooth diverge 3× on phase swing
(7.9 vs 24.4pp) and 18pp on dAmp(TW) (+2.1 vs −15.8) — J-CLASS separates both
phenomena (jump-class carries every large effect; slope-class is tame on both
axes), but the J VALUE alone governs neither.**

- AMP: FALSIFIED as a pure-J law. The sawtooth amplitude flip is (a) not
  reproduced by the other jump-class trace, and (b) baseline-convention-coupled
  (−15.8 TWmean vs −0.3 matched-mean). It is a sawtooth-specific TWmean artifact
  plus a real oscillation-damping asymmetry, not a function of J.
- PHASE: VALIDATED as a J-class law, with the caveat that within the jump class
  the swing still differs 3× — J is a class variable (jump vs slope), not a dial.
- What actually distinguishes plateau from sawtooth at equal J: edges per
  cycle (plateau 2 jumps/240 — up at t=120, down at t=0; sawtooth 1 drop/240
  with a sustained +1/tick rise between), and the sustained inter-edge slope.
  The "already-moving target" story survives only if "moving" counts the
  slow rise, i.e. edge DENSITY × inter-edge slope, not jump size.

## Scars (booked)

1. **Verdict-code/pre-registration mismatch (caught this run):** the first
   implementation computed a lenient min/max class separation while the
   pre-registered text said "BOTH big-J < EVERY slope − 3pp"; the lenient
   version returned AMP PASS. Caught before writing the report, rule re-cut
   strict, verdict changed PASS→FAIL. Lesson: transcribe pre-registered
   statistics into code verbatim and diff the wording against the branch.
2. Integer slope traces quantize J to ~2 regardless of nominal slope 1.06–2.0 —
   a J-ladder at N=6/δ=12 needs synthetically rescaled traces to get >2 rungs
   below the jump class (same quantization wall SPIN-27 hit on slope metrology).
3. Sawtooth matched-mean static (73.6) sits 27.7pp above its TWmean (45.9) —
   any sawtooth tax quoted under a single baseline is uninterpretable
   (SPIN-17 scar #2 generalized to the amplitude axis).

## Next-spoke proposal

**EDGE-DENSITY LADDER (REGIME follow-up):** hold J fixed (one +153-style edge)
and vary edges per cycle {1, 2, 4, 8} × inter-edge slope {0, +1, +2} —
2×3 synthetic traces, same P=16 K=2 anchors + phase-offset swing. Prediction
to pre-register next: swing and dAmp track edge density × inter-edge slope
(plateau = 2 edges, slope 0; sawtooth = 1 edge, slope 1), NOT J. If edge
density sweeps swing 1→24pp monotonically, replace the J-law with an
edge-law in THEORY-grammar-phase.md.

Files: wheel/SPIN-28-regime.md + spin28_regime.py + spin28-output.txt (3 s).
Not appended to WHEEL-LOG.md (cron lane's job). Nothing committed or pushed.
