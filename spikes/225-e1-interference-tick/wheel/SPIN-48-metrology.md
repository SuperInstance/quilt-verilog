# SPIN-48 — METROLOGY (window-local rate exponent α(drift, K, window))

Lane: wheel_spin48_metrology (zai/glm-5.3). Run: 2026-09-04 14:49 UTC
(129 s wall). Script: `wheel/spin48_metrology.py` (H1 + H2 with decision
rules pre-registered verbatim in the header BEFORE any panel run); raw
output: `wheel/spin48-metrology-output.txt` (python3 -u redirect, no
pipes). Nothing committed or pushed; WHEEL-LOG untouched by this lane.
Executes SPIN-46's filed next-spoke proposal.

## Instrument (pre-registered)

W_j = cumulative debt at end of window j (32 windows × 4800 ticks =
153,600 = 32× SPIN-38's window, seed-meaned over
{1, 7, 42, 1999, 20260902}); window-local exponent
**α_j = ln(W_{j+1}/W_j) / ln((j+1)/j)**; per-cell α = mean over the last
quarter (j = 24..31); error bar = max per-seed deviation from the seed
mean. All exponent math in log space (floats only at stat/print time;
harness loops integer-only, inherited verbatim from SPIN-46/38).

## Hypotheses (pre-registered) and verdicts

- **H1:** for K=2 at 32×, α ≈ 1 (linear) at low drift, > 1
  (accelerating) at high drift, with the α=1.05 transition drift d*
  bracketing SPIN-46's ρ-crossing at ~384 (192 < d* < 480).
  **FALSIFIED.** α(96) = 0.833 ✓linear and α(768) = 1.323 ✓accelerating
  (gates (i)/(ii) pass; spread 0.887 — not drift-flat), **but d\* = 192**:
  the transition sits at/below the low edge of the bracket, it does not
  bracket 384. α(drift) is also strongly non-monotone —
  0.833 → 1.193 → **1.719 (peak at 288)** → 1.554 → **1.251 (dip at
  480)** → 1.503 → 1.323 — no clean single crossing.
- **H2:** α(K=2) > α(K=1) at every drift ≥ 96 at 32× (exponent, not
  prefactor, carries the K-dichotomy). **FALSIFIED** — the exponents are
  equal within error at **all four** stress drifts (diffs −0.30 / +0.12 /
  +0.75 / +0.45 vs err bars 1.09–1.75). Point estimates favor K=2 at
  drift ≥ 384 (consistent with SPIN-46's late-window rates) but the
  single-window log-time estimator is too noisy at 5 seeds to certify an
  exponent difference.

## Canaries — ALL PASS

- **(a) provenance:** verbatim-copy runner ≡ `sp46.run_ledger`
  byte-identical 7/7 configs **including two 153,600-tick nw=32 cases**
  (full key + windows equality).
- **(b) anchors digit-exact:** zero@15 K=1 → 77.3 / 8756 / 187834;
  ladder@15 K=1 → 71.5 / 5792 / 106378 — all exact.
- **(c) SPIN-38/46 replay:** ladder@30 K=1 drift=384 debt/ev = 9202.3
  (anchor 9202.4 ± 5%).
- **(d) gate=never ≡ mc=0:** delta=10⁹ → all-zero ledgers 4/4.
- **(e) SPIN-15 mass/debt closure:** 5/5 seeds on every arm (H1 8 cells
  + H2 4 cells).
- **(f) double-run determinism:** 4/4 byte-identical (incl. 153,600-tick
  cases).

No divergence exclusions were needed (no cell crashed; identities held
everywhere).

## Results (all real)

1. **The drift=0 boundary cell is perfectly linear:** α = 1.001 with
   α_j curve flat at 1.001–1.006 across all 31 boundaries and err
   0.000 — the exponent instrument is exact where debt growth is exact
   (SPIN-46's 32×/8× = 4.01 there). At drift 0 the fabric is a pure
   linear accumulator.
2. **At stress the local exponent is not a constant — it oscillates.**
   α_j curves swing ±0.5–1.0 between adjacent window boundaries
   (e.g. K=2/96: 1.11 → 1.05 → 1.03 → 0.59 → 0.78 late-run; K=1/768:
   2.07 at j=12 down to 0.43 at j=28). SPIN-46's convergence question
   ("does γ converge to a constant or keep growing?") answers **neither:
   γ fluctuates persistently** — q2→q4 quarter-means move in both
   directions at 10 of 11 stress cells; only 192-cells (both K) show
   |q4−q2| < 0.05. There is no stable asymptotic exponent at 32×
   duration on outlier@30; the runaway is a fluctuating-slope process,
   not a clean power law.
3. **K-dichotomy at 32× is directional, not certified:** every point
   estimate of α(768-window debt ratios) still favors K=2 at drift ≥ 384
   (debt 81.3 vs 42.1 ×10⁹ at 768; 17.0 vs 11.2 at 384), and K=1/768's
   α = 0.876 with the largest err (1.114) contains SPIN-46's
   superlinear control inside its bar — but the exponent-difference
   claim fails its own gate.
4. **The ρ-crossing does not survive translation into exponent space.**
   SPIN-46's rate-ratio crossing at ~384 becomes a broad non-monotone
   α(drift) hump peaking at 288 with a local minimum at 480. Whatever
   the crossing is, it is not a sharp regime boundary in the local
   growth exponent.

## Headline number

**α(drift=0) = 1.001 exactly; at stress α oscillates 0.4–2.1
window-to-window with seed error bars 0.35–1.11, d\* = 192 (no 384
bracket), and α(K=2) − α(K=1) = −0.30/+0.12/+0.75/+0.45 — inside error
at every drift ≥ 96: the 4800-tick window is the wrong magnifier for an
exponent.**

## Scars / honest boundaries

- **Instrument power (the big one):** a single 4800-tick window increment
  is a high-variance sample of the debt process (echo-period
  oscillation visible in SPIN-46's w8/w16 dips); the log-ratio estimator
  divides two noisy increments, and 5 seeds cannot beat that down. The
  H2 falsification is partly an honest instrument-power failure, not
  evidence the exponents ARE equal — recorded as such, not as a positive
  equality claim. Log-space stats used throughout (SPIN-44 scar class).
- Last-quarter asymptote choice (j=24..31) is 8 samples of a fluctuating
  quantity; quarter-mean "converging vs drifting" labels are sensitive
  to this.
- Point α values are means over a non-stationary, oscillating curve;
  they should not be quoted as asymptotic constants (same scar class as
  SPIN-46's "Φ is a lower bound").
- Seeds 5/5 with max-deviation error bars (not Gaussian σ); with n=5 the
  max-dev estimate is itself unstable — reported, not gated on.
- Drift=0 boundary cell excluded from H1 by pre-registration; it is the
  cleanest number in the spin.

## Next-spoke proposal

**SUB-WINDOW EXPONENT (metrology follow-up):** re-measure α with
nw = 128 (1200-tick sub-windows, same 153,600-tick budget) × pooled
seeds (25 windows' worth of increments per cell), which cuts the
estimator variance by ~√(4800/1200 × pool) and makes the H2 exponent
comparison decidable rather than error-dominated. Secondary targets:
(a) spectrum of the α_j / per-window-increment oscillation (the echo
period SPIN-46 hypothesized as the crossing mechanism — measure it
directly instead of inferring from ρ), (b) the drift=288 α-peak vs the
480 dip with tight bars — if real, the α(drift) hump is a second
independent fingerprint of the resonance, mis-aligned with the ρ
crossing, and the mechanism model must explain both.
