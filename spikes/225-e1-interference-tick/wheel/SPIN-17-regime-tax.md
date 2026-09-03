# SPIN-17 — REGIME TAX SPECTRUM (follow-up to SPIN-16-regime spoke 6)

Everything below was actually run: `wheel/spin17_regime_tax.py`, raw output
`wheel/spin17-output.txt` (elapsed 7 s). Config = SPIN-16-regime's base:
N=6 ladder, delta=12, drift=6, pd=3, 4800 ticks, seeds {1,7,42,1999,20260902}
(per-seed columns in raw output; means quoted here). Integer-only in every
loop; floats only at print/fit time. Instrument = `dyn_run`, the
canary-proven verbatim clone of `exp_glm1.run_fabric`, **k as a parameter**
(scar #1 honored). All scheduling is single-pass inline (no re-simulation).

**HYPOTHESIS (pre-registered):** the regime-switching tax decays
hyperbolically, tax(P) → 0 as 1/P; its collapse timescale equals pulse
settling (K × decay), not the reality period. Non-hyperbolic decay = a
second, slower memory channel.

## Verdicts

| # | Sub-claim | Verdict |
|---|-----------|---------|
| 1 | tax(P) → 0 as 1/P (hyperbolic) | **FALSIFIED** — exponential fits better or ties at every K |
| 2 | Collapse timescale = pulse settling (K×decay) | **FALSIFIED** — τ ≈ 95–131 ticks, flat in K |
| 3 | Non-hyperbolic ⇒ second slow memory channel | **MIXED** — non-hyperbolic confirmed, but the channel is phase resonance with the reality period, not fabric memory |
| 4 | Duty cycle: tax tracks time-in-bad-regime or transition count | **FALSIFIED (neither)** — strongly asymmetric: worst when the *good* regime dominates |
| 5 | Amplitude: tax linear in spread | **FALSIFIED** — gated: ~0 at spread 5, full at spread ≥ 15 |

**Headline: the K=2 switching tax peaks at 27.0 pp at P=16 and collapses
EXPONENTIALLY (τ ≈ 131 ticks, r² = 0.949 vs 0.620 for 1/P), on a timescale
that is K-independent and ≈ half the reality period (240) — the tax
spectrum is a resonance with reality's cycle, not a fading pulse memory.**

## EXP 1 — Fine period spectrum (5↔30 duty-50 square, P ∈ {8…1024}, K ∈ {1,2,4,8})

Cross-validation: all six SPIN-16 table cells reproduce **exactly**
(K=2: 27.0 @16, 11.7 @64, 1.7 @256; K=1: 5.1 @16, 5.9 @64, 2.6 @256).

Key structure (tax = TWmean − osc, pp):

- **The spectrum is non-monotone with a K-dependent peak.** K=1 peaks at
  P=48 (7.9); **K=2 peaks at P=16 (27.0, with P=8 already lower at 21.2)**;
  K=4 and K=8 peak at P=8 (10.4, 8.0) — the fastest measured period. A 1/P
  law is monotone and diverges at small P; the data turn over instead.
- **The tax is not monotone in K.** At P=16: K=1 5.1, **K=2 27.0**, K=4
  6.5, K=8 7.5. K=2 is uniquely catastrophic — an order-of-magnitude spike
  over both neighbors. This was invisible to SPIN-16's K∈{1,2} grid.
- **Decay is exponential, not hyperbolic.** Fits over positive taxes
  (log-linear): K=2 exp r²=0.949 (τ=131.0, A=19.6) vs hyper r²=0.620;
  K=8 exp 0.734 (τ=95.1) vs 0.699; K=1 exp 0.341 (τ=202.5, poor — the K=1
  spectrum is a broad bump, not a clean decay) vs 0.060; K=4 is a tie
  (0.803 hyper vs 0.787 exp, τ=100.0). Exponential wins or ties everywhere.
- **τ is flat in K** (131 / 100 / 95 at K=2/4/8) while pulse life spans
  2→8 ticks. If the collapse timescale were pulse settling (K×decay), τ
  should scale with K by 4×; it *shrinks* slightly. τ ≈ 100–130 ≈ half the
  reality period (240) — pointing at phase coverage of the reality cycle.
- **Long-P tail goes negative vs TWmean** (−1 to −3 pp at P≥384, all K):
  slow oscillation samples the concave spread→residency curve and *beats*
  the time-weighted mean — the Jensen floor, consistent with matched-mean
  statics sitting 3–6 pp above TWmean (e.g. K=8: static-17.5→18 = 57.8 vs
  TWmean 52.1). No slow memory: per SPIN-16, hysteresis is exactly zero;
  the residual is curve shape, not state.

## EXP 1b — Phase-inversion probe (same duty, same transitions, lo/hi order swapped)

| P | K | lo-first tax | hi-first tax | Δ |
|---|---|---|---|---|
| 16 | 2 | 27.0 | 32.0 | **−5.1 pp** |
| 64 | 2 | 11.7 | 13.4 | −1.7 |
| 16 | 1 | 5.1 | 6.2 | −1.1 |
| 16 | 4 | 6.5 | 5.1 | +1.3 |

Two schedules with identical duty and transition counts differ by up to
5.1 pp purely by phase alignment with the reality period (240; P=16 and
P=48 divide 240 exactly, and both show tax bumps). This is the smoking gun
for verdict 3: the "second channel" is **phase resonance**, the SPIN-10/11
phase-scheduling physics, not a slow fabric memory.

## EXP 2 — Duty cycle (30 for duty% of P, 5 otherwise)

| P | K | duty | osc% | TWm% | tax | mmS% | osc−mmS |
|---|---|---|---|---|---|---|---|
| 16 | 2 | 25 | 34.6 | 70.9 | **36.3** | 88.0 | **−53.5** |
| 16 | 2 | 50 | 29.9 | 56.9 | 27.0 | 53.5 | −23.6 |
| 16 | 2 | 75 | 30.2 | 42.9 | 12.7 | 36.3 | −6.1 |
| 64 | 2 | 25 | 59.4 | 70.9 | 11.5 | 88.0 | −28.6 |
| 64 | 2 | 50 | 45.2 | 56.9 | 11.7 | 53.5 | −8.3 |
| 64 | 2 | 75 | 34.3 | 42.9 | 8.6 | 36.3 | −2.0 |
| 16 | 1 | 25 | 79.6 | 79.9 | 0.3 | 96.9 | −17.3 |
| 16 | 1 | 50 | 57.0 | 62.2 | 5.1 | 53.2 | +3.9 |
| 16 | 1 | 75 | 36.4 | 44.5 | 8.1 | 31.7 | +4.7 |

Transitions are identical within each (P, duty) row (599 @ P=16, 149 @
P=64). **Neither predictor survives.** Transition count fixed → tax should
be duty-flat; it swings 36.3→12.7. Time-weighting is already in TWmean →
tax should vanish; instead the tax is *largest when 75% of the time is in
the good regime* (duty 25: K=2 osc collapses to 34.6 vs static-5's 84.9,
and 53.5 pp below the matched-mean static). Mechanism: brief bad-regime
(spread-30) pulses into a good background fire the wrong trigger set,
and the K=2 pulse superposition + phase mismatch lingers well past the
4-tick pulse itself. Asymmetry is adversarial: a *guerrilla* schedule
(rare bad phases) hurts far more per unit time than sustained badness.
K=1 note: vs TWmean the duty-25 tax looks like ~0, but vs matched-mean it
is −17.3 — the baseline choice flips the sign (scar #2, aggravated).

## EXP 3 — Amplitude (P=16)

| pair | K | spread | osc% | tax | osc−mmS |
|---|---|---|---|---|---|
| 5↔30 | 2 | 25 | 29.9 | 27.0 | −23.6 |
| 10↔25 | 2 | 15 | 39.6 | 22.8 | −13.8 |
| 15↔20 | 2 | 5 | 53.3 | **0.6** | −0.2 |
| 10↔25 | 1 | 15 | 61.1 | 1.8 | +7.9 |

**Gated, not linear**: cutting amplitude 5× (25→15) keeps 84% of the tax
(22.8/27.0), but spread 5 kills it entirely (0.6, indistinguishable from
matched-mean static). There is a threshold between spread 5 and 15 —
consistent with the trigger-set overlap picture (15↔20 never separates the
sensors' error profiles enough to matter). K=1 remains Jensen-dominated
(positive only vs matched-mean, and only for mid amplitudes).

## Canaries — all PASS

- **(a) Wiring byte-identity:** dyn_run vs `exp_glm1.run_fabric`, 12
  configs (3 grammars × K{1,4} × seeds{1,42}), every per-tick residency
  vector byte-identical. PASS.
- **(b) Anchor replays (5-seed means):** zero@15 K=1 = 77.3% / debt
  187834 (ev 8756); ladder@15 K=1 = 71.5% / ev 5792 / debt 106378 — exact.
  PASS. Plus 6/6 exact reproduction of SPIN-16's oscillation table.
- **(c) No-shift identity:** hold-5 through the *scheduler code path*
  (square_schedule with both phases = 5) == static-5, K∈{1,2,4,8} × 5
  seeds, byte-identical. PASS.

## Scars

1. **Phase-order bug (new, caught by anchors):** first draft put the
   hi-spread phase first in each period; SPIN-16's convention is lo-first.
   Identical duty/transition schedules differed by 5.1 pp at K=2 P=16
   purely from phase alignment with reality's 240-cycle. Lesson: a
   periodic-spread schedule has a *phase degree of freedom* — pin it,
   report it, and (better) exploit it (it's a real effect, EXP 1b).
2. **Baseline choice flips duty-cycle verdicts** (SPIN-16 scar #2,
   aggravated): at K=1 duty-25 the tax is +0.3 vs TWmean but −17.3 vs
   matched-mean. Never quote an oscillation gap without both baselines.
3. **K-grids of {1,2} hide non-monotonicity:** the K=2 spike at P=16
  (27 pp vs 6–8 pp at K=4/8) is the biggest effect in this spoke and was
   structurally invisible to SPIN-16. Sweep the interacting knob before
   declaring a K-law.

## Next spoke proposal

**SPIN-18 — REGIME RESONANCE MAP:** the tax spectrum's peak moves with K
(P=16 @ K=2 → P=8 @ K=4/8) and phase alignment with the 240-cycle moves
the tax by 5 pp — measure tax over the full (K ∈ 1..16) × (P ∈ 8..256) ×
{phase-aligned, anti-aligned, incommensurate-P} grid and test whether the
peak follows a K×P resonance law (e.g. tax maximal when pulse superposition
lifetime ≈ half-period) and whether an anti-aligned schedule can cancel
the K=2 catastrophe (27 pp → ?). Second thread: the **guerrilla duty
asymmetry** (duty-25, K=2: −53.5 pp vs matched-mean) as an adversarial
schedule — find the duty that maximizes damage per unit bad-regime time.

Status: **COMPLETE.** Nothing committed or pushed. WHEEL-LOG.md untouched.
