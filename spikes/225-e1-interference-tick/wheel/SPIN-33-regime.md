# SPIN-33 — REGIME: EDGE-DENSITY LADDER (pinned-J 2D grid E × slope)

Date: 2026-09-03 · Spoke: REGIME · Predecessor: SPIN-28 (J-class separates;
pure-J amplitude law falsified) · Script: `wheel/spin33_regime.py` ·
Output: `wheel/spin33-output.txt` (unique filename, SPIN-30 scar).

## Hypothesis

SPIN-28 left amplitude governance open between three candidates: (a) edge
DENSITY E (edges/cycle — per-edge damage), (b) inter-edge SLOPE s, (c) the
E·J product. Design: pin jump size J=153 (sawtooth class) and walk an
L-shaped 2×D grid — E ∈ {1,2,3,4,6} edges per 240-cycle × s ∈ {1,2,3,4,6}
rise slope (feasibility: (240/E−1)·s ≥ 153; 16 grid points). Trace:
`400 + min(153, (t%L)*s)`, band [400,553] (spin-21 convention), single-tick
153-drop at every segment boundary. J and edge-count asserted empirically
at grid corners.

## Pre-registration (verbatim from script header, committed before run)

Metric: dAmp_B = tax_s25 − tax_s15, P=16 K=2 duty-50 square, spreads
25 (5↔30) and 15 (10↔25), BOTH baselines B ∈ {TWmean, matched-mean}
(SPIN-17 scar), seeds {1,7,42}.

- E_effect = mean within-slope-column range (columns with ≥3 E-points);
  s_effect = mean within-E-row range (rows with ≥3 s-points);
  range_all = full-grid range of dAmp.
- (a) iff E_effect ≥ 6.0pp AND E_effect > s_effect+3.0 AND s_effect ≥ 3.0
- (c) iff same E-condition AND s_effect < 3.0 (slope axis inert; with J
  pinned, E·J is monotone in E, so (c) is separated from (a) only by the
  inert slope axis)
- (b) iff s_effect ≥ 6.0pp AND s_effect > E_effect+3.0
- NONE (falsifies a, b, c; supports per-edge-J law) iff range_all ≤ 3.0pp
- Baselines disagreeing on rule class → MIXED-baseline.

Phase spot-check (advisory): offsets 0..8 at extremes E1s1 vs E6s6; pure-E
predicts swing grows with E.

## Canary receipts (all PASS — gate cleared)

- a. Wiring: dyn_run(R0) vs run_fabric byte-identical, 16 configs.
- b. Anchors 5-seed: ladder15 K=1 71.48 / ev 5791.6 / debt 106378.4;
  zero K=1 77.26 / 8756.4 / 187833.6 (SPIN-5 rounding tolerance).
- c. SPIN-23 replays: plateau TWmean tax 36.7 ✓; sawtooth flip s15=27.5,
  s25=11.7, +15.8pp ✓.
- d. Determinism: 12 dual runs byte-identical; J==153 and edge-count==E
  asserted at 4 grid corners.
- Integer-only in-loop; single-pass inline dyn_run (SPIN-16 scar);
  schedule-phase pinned; explicit `E{E}s{s}` labels on every cache/print
  (SPIN-23 scar).

## Results — EXP1 grid (P=16 K=2, seeds {1,7,42})

| trace | E | s | osc15 | osc25 | taxTW15 | taxTW25 | taxMM15 | taxMM25 | dTW | dMM |
|-------|---|---|-------|-------|---------|---------|---------|---------|------|------|
| E1s1 | 1 | 1 | 27.6 | 18.5 | 39.1 | 28.7 | 47.0 | 56.1 | −10.4 | +9.2 |
| E1s2 | 1 | 2 | 27.9 | 20.6 | 28.7 | 25.7 | 23.9 | 31.2 | −3.0 | +7.3 |
| E1s3 | 1 | 3 | 29.2 | 25.1 | 23.3 | 21.7 | 19.5 | 23.6 | −1.5 | +4.1 |
| E1s4 | 1 | 4 | 23.6 | 17.2 | 28.4 | 27.5 | 26.8 | 33.2 | −0.9 | +6.4 |
| E1s6 | 1 | 6 | 20.0 | 10.6 | 31.4 | 33.7 | 31.3 | 40.6 | +2.2 | +9.4 |
| E2s2 | 2 | 2 | 16.3 | 14.7 | 35.4 | 24.1 | 26.6 | 28.1 | −11.2 | +1.5 |
| E2s3 | 2 | 3 | 15.2 | 13.8 | 28.5 | 23.5 | 25.3 | 26.7 | −5.0 | +1.4 |
| E2s4 | 2 | 4 | 14.0 | 13.6 | 28.9 | 20.1 | 25.7 | 26.1 | −8.9 | +0.3 |
| E2s6 | 2 | 6 | 16.2 | 18.0 | 26.9 | 12.3 | 26.8 | 25.0 | −14.5 | −1.8 |
| E3s3 | 3 | 3 | 13.3 | 11.8 | 23.0 | 31.0 | 20.3 | 21.8 | +8.0 | +1.5 |
| E3s4 | 3 | 4 | 13.6 | 12.5 | 22.2 | 27.2 | 18.2 | 19.3 | +5.0 | +1.1 |
| E3s6 | 3 | 6 | 14.1 | 11.4 | 21.3 | 24.2 | 20.4 | 23.1 | +3.0 | +2.7 |
| E4s3 | 4 | 3 | 7.4 | 1.5 | 22.4 | 40.1 | 14.3 | 20.2 | +17.7 | +5.9 |
| E4s4 | 4 | 4 | 6.6 | 1.1 | 22.7 | 34.7 | 17.8 | 23.3 | +12.0 | +5.5 |
| E4s6 | 4 | 6 | 6.7 | 0.8 | 22.5 | 27.7 | 19.4 | 25.3 | +5.1 | +5.9 |
| E6s6 | 6 | 6 | 7.9 | 7.2 | 12.7 | 26.8 | 8.2 | 8.9 | +14.1 | +0.7 |

## Results — EXP2 phase-offset (advisory extremes)

- E1s1 swing = **16.3pp** (osc 10.4–26.7 across offsets 0..8)
- E6s6 swing = **1.5pp** (osc 6.2–7.7)
- Pure-E prediction (swing grows with E) is **inverted**: denser edges
  give much FLATTER phase sensitivity.

## Pre-registered rule outcome

- [TWmean] E_effect=24.0pp, s_effect=10.0pp, range=32.2pp → rule **(a)** edge density
- [matched-mean] E_effect=7.2pp, s_effect=2.6pp, range=11.2pp → rule **(c)** E·J (slope axis inert < 3pp)
- Baselines disagree on rule class → **VERDICT: MIXED-baseline** (per pre-registration).

## VERDICT: MIXED (baseline-dependent rule class)

Unambiguous part BOTH baselines agree on: **slope (b) loses** — s_effect
(10.0 / 2.6pp) is dominated by E_effect (24.0 / 7.2pp) in both. Amplitude
governance rides the E axis at pinned J, not the inter-edge slope axis.
The disagreement is only whether the slope axis is "inert" (MM: 2.6 < 3pp
→ (c)) or "secondary-active" (TW: 10.0 ≥ 3pp → (a)). The TW slope effect
is real but column-confounded (s=6 columns behave distinctly), so (a)-vs-(c)
is not separable at this grid resolution.

Further falsifications beyond pre-registration (advisory):
- **Pure per-edge damage accumulation is falsified by phase**: if each of
  E edges added damage, phase swing should grow with E; it collapses
  (16.3 → 1.5pp). Dense edges act like a *renormalized quasi-static
  gradient*: E6s6 looks slope-like (tiny flip, tiny swing, near-zero MM
  taxes 8.2/8.9) despite every edge being a J=153 jump.
- The sawtooth flip is an E=1 phenomenon: at E=1 the TW dAmp wanders
  −10.4…+2.2 with slope; at E≥3 sign stabilises positive; at E=4,6 dAmp
  +5…+18pp (R0-like ordering restored).

## Headline number

**At pinned J=153, walking edge density E=1→6 swings the TWmean amplitude
delta dAmp across a 32.2pp range (−14.5 to +17.7pp) — an E_effect of
24.0pp vs a slope effect of 10.0pp — while phase sensitivity inverts from
16.3pp swing (E1s1) to 1.5pp (E6s6).**

## Scars / lessons

- Both baselines remain mandatory and still disagree on rule *class*
  (not direction) — TWmean inflates the slope-axis contribution; matched-
  mean is the conservative amplitude instrument (SPIN-17 scar generalizes).
- Integer grid feasibility couples E and s ((240/E−1)·s ≥ 153); the grid
  is L-shaped, so "columns with ≥3 points" drive E_effect — pre-registration
  accounted for this; future grids should pre-plan orthogonal coverage.
- Quasi-static renormalisation emerges *inside* jump-class traces — J-class
  labels (SPIN-28) are about edge *spacing*, not edge *size* alone.

## Next-spoke proposal (SPIN-35 candidate)

**EDGE-SPACING RESONANCE**: sweep inter-edge gap g = 240/E ∈ {40, 48, 60,
80, 120, 240} against scheduler period P ∈ {8, 12, 16, 24, 32, 48} at
fixed J and fixed slope. Hypothesis: amplitude flip and phase swing are
governed by the commensurability ratio g/P (edges landing in-phase with
spread-shock ticks), predicting swing peaks at integer g/P and collapse
at incommensurate ratios — which would unify the E1s1 swing (g=240, far
from P=16) vs E6s6 collapse (g=40, near 2.5×P) and explain the SPIN-28
sawtooth phase sensitivity. Pre-register: swing(t) monotonically decreasing
in min distance |g/P − round(g/P)| modulo both; falsified if swing is flat
across the resonance map.

---
Not committed/pushed; WHEEL-LOG.md append left to the cron lane, per rules.
