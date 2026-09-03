# SPIN 1 — METROLOGY: correction latency & refractory floor of the interference arm

Run: 2026-09-02 22:40 AKDT · lane `wheel-spin-1-metrology` · harness `e1.py` (v2,
unit-contract fixed), driver `wheel/spin1_metrology.py` (integer-only, no floats,
LCG + reality imported verbatim from e1.py). Seeds: 1, 7, 42, 1999, 20260902.
4800 ticks/arm/seed. Two regimes, both harness-native: CALM (delta=6, drift=3,
K=8, lat2=5) and STRESS (delta=12, drift=6, K=4, lat2=10).

## Hypothesis (falsifiable, as briefed)

H1: interference reaches the same fixed point with mean time-to-fix ≤ 1.5× sequential.
H2: interference exhibits a refractory floor (min inter-correction gap) ≥ pulse
lifetime K, for all seeds.
Fix criterion as briefed: |error| ≤ 1 sustained 50 ticks.

## Method

Instrumented copy of the e1.run() loop (identical order of operations: drift →
pulse expiry → twin reads → trigger → arm correction → decay snapshot → g update),
recording per tick: correction-event ticks, post-correction error max(|e1|,|e2|).
Derived: ticks-to-fix (sustain 50), inter-correction gap distribution (min/mean),
residual error over the last 2400 ticks (integer floor-division mean).

## Result 0 — the briefed fixed-point criterion is unattainable on this harness

|error| ≤ 1 sustained 50 ticks was **NOT-REACHED by either arm, any seed, either
regime** (0/20 arm-runs; % of ticks with |e|≤1 is 0 everywhere). Cause is
structural, not stochastic: g drifts ±3 (calm) / ±6 (stress) per tick while
reality() moves ≤2/tick, so |e|≤1 cannot persist 50 ticks under drift alone.
The harness's operative fixed point is its **deadband** |e| ≤ delta — that is the
measured criterion below. (Metrology finding: the fabric has no |e|≤1 fixed point;
the assumption E1's interference arm "reaches the same fixed point" must be read
at deadband resolution.)

## Per-seed tables — CALM (delta=6, K=8)

t_fix = tick at which |e|≤delta first sustains 50 ticks.

| seed | mode | t_fix | #corr | minGap | meanGap | residMean | residMax | %inDB |
|------|------|-------|-------|--------|---------|-----------|----------|-------|
| 1 | sequential | 146 | 2390 | 1 | 2 | 7 | 53 | 55 |
| 7 | sequential | 146 | 2333 | 1 | 2 | 7 | 53 | 56 |
| 42 | sequential | 141 | 2250 | 1 | 2 | 6 | 53 | 58 |
| 1999 | sequential | 146 | 2265 | 1 | 2 | 6 | 53 | 56 |
| 20260902 | sequential | 144 | 2313 | 1 | 2 | 6 | 53 | 56 |
| 1 | interference | NOT-REACHED | 2820 | 1 | 1 | 7 | 35 | 41 |
| 7 | interference | NOT-REACHED | 2909 | 1 | 1 | 7 | 37 | 41 |
| 42 | interference | NOT-REACHED | 2944 | 1 | 1 | 7 | 37 | 40 |
| 1999 | interference | NOT-REACHED | 2830 | 1 | 1 | 7 | 36 | 42 |
| 20260902 | interference | NOT-REACHED | 2736 | 1 | 1 | 7 | 36 | 45 |

Calm summary: seq mean t_fix = 144 (5/5); interference never sustains 50 ticks
inside the deadband (5/5) — it fires nearly every tick (meanGap 1) and sits
inside the deadband only 40–45% of ticks. It does hold residual maxErr lower
(35–37 vs 53) with equal residMean.

## Per-seed tables — STRESS (delta=12, K=4)

| seed | mode | t_fix | #corr | minGap | meanGap | residMean | residMax | %inDB |
|------|------|-------|-------|--------|---------|-----------|----------|-------|
| 1 | sequential | 144 | 2524 | 1 | 1 | 13 | 61 | 51 |
| 7 | sequential | 145 | 2655 | 1 | 1 | 13 | 61 | 49 |
| 42 | sequential | 140 | 2469 | 1 | 1 | 13 | 61 | 53 |
| 1999 | sequential | 143 | 2602 | 1 | 1 | 13 | 61 | 50 |
| 20260902 | sequential | 146 | 2513 | 1 | 1 | 13 | 61 | 51 |
| 1 | interference | 865 | 1910 | 1 | 2 | 10 | 38 | 83 |
| 7 | interference | 382 | 1866 | 1 | 2 | 10 | 39 | 82 |
| 42 | interference | 383 | 1890 | 1 | 2 | 10 | 36 | 83 |
| 1999 | interference | 133 | 1856 | 1 | 2 | 10 | 38 | 83 |
| 20260902 | interference | 387 | 1920 | 1 | 2 | 10 | 39 | 82 |

Stress summary: seq mean t_fix = 143; interference mean t_fix = 430 → **ratio
3.01× (bound was 1.5×)**. Huge per-seed variance (133 → 865; seed 1999 beats
sequential). Interference wins the steady state decisively: residMean 10 vs 13,
residMax 36–39 vs 61, %inDB 82–83 vs 49–53.

## Verdict: FALSIFIED (with one banked positive)

- **H1 FALSIFIED.** At deadband resolution: calm ratio is infinite (interference
  never sustains the 50-tick hold, 0/5 seeds); stress ratio 3.01× > 1.5× bound.
- **H2 FALSIFIED, and more strongly than expected: there is no refractory floor at
  all.** Min inter-correction gap = 1 tick in all 20 arm-runs, both arms, both
  regimes — 1 < K=8 (calm) and 1 < K=4 (stress). Mechanism: pulse magnitude is
  e//3 while the trigger threshold is |e|>delta, so the arm habitually undershoots
  and refires on consecutive ticks. Pulse lifetime K gates the *decay tail*, not
  the *refire*. The harness's assumption of a K-scale refractory/latency budget
  relative to the twin trigger Delta is unsupported at the hardware parameter
  level.
- Banked positive: interference's steady-state error is strictly better in stress
  (residMax −38%, residMean −23%, +32pp %inDB) — reproducing the README finding,
  now pinned per-seed. And sequential t_fix is remarkably tight (140–146 across
  all seeds/regimes — the calm regime's 144±3 is essentially the reality()
  phase-96 hold plateau, i.e. seq "fix" is a property of the signal, not the arm).

## Headline number

**Refractory floor = 1 tick (not ≥ K): the interference arm fires on consecutive
ticks in 20/20 runs; stress time-to-deadband-fix is 3.0× sequential (430 vs 143).**

## New spoke proposal

**REFRACTORY-BLADE (candidate spoke, METROLOGY→ALPHABET coupling):** make the
refire floor explicit — either (a) trigger threshold scaled to pulse_div (fire
only when |e| > delta·pulse_div) or (b) a hard K-tick cooldown per twin — and
re-measure t_fix, gap distribution, and %inDB. Hypothesis: an explicit refractory
gate restores a true floor ≥ K and cuts interference event count ~pulse_div×,
at possible cost to the calm regime. This is the missing knob the metrology
exposed: E1 currently has *implicit* refire physics, not a refractory budget.

Files: `wheel/spin1_metrology.py` (driver, rerunnable: `python3 wheel/spin1_metrology.py`).
No commits, no pushes, WHEEL-LOG.md untouched.

VERDICT: FALSIFIED | HEADLINE: refractory floor = 1 tick (< K) in 20/20 runs; interference stress time-to-fix 430 vs sequential 143 (3.0×, bound 1.5×).
