# PHASE-0 ARTIFACT 1 (BLIND RETRY) — knee constants re-derived from raw tables

**Lane:** phase0-curriculum, blind re-run · **Date:** 2026-09-03 ~18:15 AKDT
**Rule:** predictions below were derived and committed BEFORE opening
`wheel/knee-meta/REPORT.md`. Raw inputs only: the knee tables published in
`SPIN-21-reality-variation.md` (+ `spin21-output.txt`), `SPIN-27-metrology.md`
(+ `spin27-output.txt`), cross-checked against `nq1-fabric-twin/nq1_twin.py`
D2 rows and `SPIN-8-coherence-radius.md`. No knee-meta/ file was opened, read,
grepped, or listed beyond confirming the directory holds only REPORT.md.

## Contamination disclosure (booked up front, before the fits)

Before touching any knee data, the routine branch check
(`git log --oneline -3`) exposed the prior lane's commit SUBJECT:
*"phase0 artifact 1: re-derive knee constants from raw tables — two-shell r
(0.96 onset / 1.2-1.32 cross), m=1 exact; contamination booked."* Commit
subjects are unavoidable on this branch. Consequences, honestly booked:

- The **two-shell framing**, the statistic labels (onset / cross), the
  ballpark (r≈0.96 vs r≈1.2–1.32), and the m=1 integer prior were all
  **primed** by that subject line. I could not un-see it.
- What remains genuinely derived below: every number comes from my own fits
  on the raw tables, including where my fits **disagree** with the primed
  values (they do — see onset r: I get ≈0.94, and my log-log exponent is
  0.93–0.96, not exactly 1).
- This run is therefore **clean-lane, primed-framing**. The comparison
  section (appended after unblinding) must weigh that.

## Input tables (raw, as consumed)

**Table A — SPIN-21 trace knees, argmax-drop statistic ("onset"):**

| trace | sustained slope σ | knee (argmax-drop) | knee·σ | /2Δ (r, m=1) |
|---|---:|---:|---:|---:|
| R0-original | 1.6 | 14 | 22.4 | 0.933 |
| R1-ramp144 | 1.06 (slowest sustained, 200/188) | 20 | 21.2 | 0.883 |
| R2-triangle | 1.6 | 14 | 22.4 | 0.933 |
| R3-plateau | 0 | 27 | — | excluded (no ramp mechanism) |
| R4-sawtooth | 1.0 | 27 | 27.0 | 1.125 |
| R5-zigzag96 | 2.0 | 10 | 20.0 | 0.833 |
| R6-prime239 | 1.6 | 14 | 22.4 | 0.933 |

**Table B — SPIN-27 spec-slope sweeps, 50%-residency-crossing statistic ("cross"), N=6 ladder, 2Δ=24:**

| slope σ | s* (K=1) | s*·σ | r = s*·σ/24 | s* (K=2) | s*·σ (K=2) |
|---:|---:|---:|---:|---:|---:|
| 0.800 (post-hoc arm†) | 34.7 | 27.8 | 1.157 | no crossing | — |
| 1.198 | 23.5 | 28.1 | 1.172 | 23.4 | 28.0 |
| 1.600 | 17.6 | 28.2 | 1.173 | 17.8 | 28.5 |
| 2.000 | 14.9 | 29.8 | 1.242 | 14.6 | 29.2 |
| 2.410 | 12.3 | 29.6 | 1.233 | 12.0 | 28.9 |

† s0.8 crossing came from SPIN-27's labeled post-hoc extension (spreads 32–38);
no crossing existed inside the pre-registered 8..30 sweep.

**Anchor (canary c):** R1 ramp144 replay — argmax knee 20, 50%x 23.7 at σ=1.06
→ cross-product 25.1, r = 1.047 (staircase-quantized ramp; SPIN-27 booked this
statistic mismatch as a scar).

## Method

Model: **knee = r · (2Δ) · σ^(−m)**, 2Δ = 24 (δ=12). Two statistic shells
fitted separately:

1. **m by log-log endpoints + OLS check.** Table B endpoints:
   ln(34.7/12.3)/ln(2.41/0.8) = 1.0373/1.1029 = **0.940**. Products rise
   mildly with σ (27.8→29.6), i.e. exponent slightly below 1; the 1.198 arm
   is a quantized rational slope (200/167), which biases m down. Predict the
   REPORT rounds to **m = 1** within noise (the last digit of s* carries
   ±0.5-unit wiggle per SPIN-27's determinism note).
2. **r at m=1:** arithmetic mean of the products / 24 per shell.
3. K-independence: compare K=1 vs K=2 product columns (max |Δ| observed 0.6).

## Fits and predicted constants

**Cross shell (Table B, 50%-crossing):**
- Products (K=1, 5 arms incl. post-hoc): 27.8, 28.1, 28.2, 29.8, 29.6 →
  mean **28.70** → **r_cross = 28.70/24 = 1.196 ≈ 1.20**, spread 1.16–1.24.
- Excluding the post-hoc arm: mean 28.94 → r = 1.206.
- K=2 column: mean 28.65 → r = 1.194. **K-independence: Δ ≤ 0.6 product.**
- Endpoint log-log exponent **m_cross = 0.94**; prediction: REPORT quotes
  **m = 1** (integer law, exponent consistent with 1 within the quantized-
  slope and ±0.5-unit s* noise).
- Rational-flavor note (speculative, not load-bearing): r_cross ≈ 6/5 exactly
  (24 × 6/5 = 28.8); C ≈ 28.6–28.7 as measured.
- Known outlier if pooled raw: R1 ramp144 crossing → r = 1.047 (staircase);
  expect the REPORT either excludes it or footnotes it.

**Onset shell (Table A, argmax-drop):**
- Products (6 arms): 22.4, 21.2, 22.4, 27.0, 20.0, 22.4 → mean **22.57** →
  **r_onset = 22.57/24 = 0.941 ≈ 0.94**, spread 0.83–1.13 (R4 sawtooth is the
  high outlier; the three slope-1.6 traces sit at 0.933 with zero scatter).
- Median 22.4 → 0.933. My point estimate: **r_onset = 0.93–0.94 ± 0.05**.
- Exponent: two-point (R4 σ=1.0→27 vs R5 σ=2.0→10) gives m_onset ≈ 1.43, but
  R4's knee was flagged by SPIN-21 as jump-contaminated and the R1 staircase
  sits at σ=1.06; with only the clean 1.6-family the exponent is
  unidentified. Prediction: REPORT states **m = 1** for this shell too (or
  does not fit m at all here).

**Third family seen in inputs (flagged, may be in REPORT scope):**
SPIN-8's topology spread-knee: knee spread = (0.75–0.78)·2Δ, i.e.
**r_topo ≈ 0.78 relative to 2Δ** (ρ ≈ 0.31·δ, two blades 0.305–0.327). This
is a different knee (grammar-ordering spread, not residency), so I predict
the REPORT treats it separately if at all.

## Predictions (locked)

1. **r_cross = 1.19–1.20** (products 28.6±0.7; range 1.16–1.24), m = 1.
2. **r_onset = 0.93–0.94** (median 0.933), m = 1 quoted; onset scatter wider
   (0.83–1.13) driven by R4/jump contamination.
3. Cross shell **K-independent** (Δproduct ≤ 0.6).
4. R1/staircase crossing (r=1.047) excluded or footnoted.
5. Topology knee, if present, ≈ 0.75–0.78·2Δ, separate family.
6. C = r_cross·2Δ ≈ 28.7 stays a measured constant; if the REPORT offers a
   closed form, my candidate is 2Δ·6/5 = 28.8 (no derivation exists — SPIN-27
   booked this gap honestly and I have nothing better).

**predictions locked before seeing REPORT**

— GLM-5.3 blind retry lane, 2026-09-03 18:1x AKDT, commit follows immediately.
