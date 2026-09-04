# NQ-1 — FABRIC-TWIN v0 (replay-only, CPU): learned model vs the two-constant laws

**Lane:** builder NQ-1 · **Date:** 2026-09-03 ~17:50 AKDT · **Branch:** g3-kinduction
**Files:** `nq1_twin.py` (harvest+fit), `dataset.csv` (171 verbatim rows), `dataset-table.md`
(full table), `results.txt`, `per-fold.txt` · **Fabric:** NONE — published numbers only,
zero byte-exact runs executed (read-only harvest of committed artifacts).

## Pre-registration (pinned, from ai-writings/docs/NEURAL-QUILT-INTEGRATION.md §4)

> **NQ-1:** Can a local model, given the archive table of (grammar, K, pd, trace) → rescue,
> predict held-out spins better than the two-constant laws themselves?
> **Pass:** beats the laws' predictions on ≥5 held-out configs by >2pp.
> **Fail:** laws win — and residuals get booked either way.

Two-constant laws = knee-meta's collapse: **Class-S knee at r = span·σ/2Δ = 1**,
**Class-M wall at m = N/(2pd+1) = 1**. Law predictor = 3-plateau step at those FIXED
thresholds (a + b·1[r≥1] + c·1[m≥1], OLS levels only — the constants 1,1 are never fitted).
Corpus constants: δ=12, σ=8/5 (R0), interference arm, 5-seed means, true-residency %
(spin11's true12% is the same metric — anchors cross-match exactly: pd3/N6 26.8 = spin9
ladder K=1 = spin4; pd3/N2 12.4 = spin4 control).

## Verdict

**NQ-1: PASS (quadratic twin) — with a split personality booked.**
- **ridge-quad MAE 9.05pp vs law 14.91pp → margin +5.87pp (>2pp bar), 5/5 folds,
  97/171 held-out configs beaten by >2pp each.** R² 0.804 vs law 0.544.
- **ridge-linear FAILS HARD: 34.35pp — worse than the constant-median baseline (23.74pp).**
  The rescue surface is a cliff landscape (r-knee, m-wall, inert-pd regime); linear-in-config
  cannot express the ratio cliffs and explodes out-of-fold (in-sample it is fine: 7–14pp
  by source — the failure is extrapolation across sparse config regions, e.g. N=7:
  pd=3→0.3% vs pd=6→8.1% vs pd=12→8.5%).
- **NQ-2 rider: FAIL** — adding r, m as features drops twin residual variance by **0.5%**
  (bar >50%). Degeneracy, not absence: σ and δ are constant across the whole harvest →
  r ≡ span/15 exactly (corr = 1.0000); only m = N/(2pd+1) is a new interaction and the
  quadratic terms already manufacture its equivalent. This corpus cannot distill r as a
  separate invariant — a σ/δ-varying corpus (spin8 δ-sweep, spin21 knees) is required.

## Dataset (171 rows; target ≥30 — exceeded)

Harvested + deduped (key: sorted lats × K × N × pd; cross-source duplicates agree to
<0.05pp, asserted in code; provenance per row in dataset.csv). All verbatim from:

| source | rows | content |
|---|---|---|
| spin9-output.txt EXP1 | 80 | 20 grammars × K{1,2,4,8}, spread 30, N=6, published lats |
| spin5-output.txt EXP2 | 28 (22 unique after dedupe vs spin9/4) | 7 grammars × K{1,2}, spread 15/30 |
| spin4-output.txt MAIN+CTRL | 42 (27 unique) | spread {0,5,10,15,20,30} × K{1,2,8} × {ladder,cohort}; N∈{2,3} controls |
| spin11-output.txt EXP1 | 55 (52 unique) | pd{1,2,3,6,12} × N{2..25} uncomp wall grid, K=1 |

Lats construction (spin4 ladder(s)=[0,s/5,…,s], cohort=[0,0,0,s,s,s]; spin11
ladder30(N)=round-half-even(30·i/(N−1))) verified against every published lats column
(7 spin11 anchors exact, incl. banker's-rounding pair [0,8,15,22,30]); rows using
constructed lats are flagged in dataset.csv. D (diverged) cells kept: 0.1–2.3% is the
published residency — divergence is the wall mechanism, booked not dropped. Sequential-arm
rows excluded (different arm; laws are interference-arm). Features per row (from config
only): span, N, K, log2K, pd, m_s (spin9's stale-mass, threshold δ/2), fresh, mean/std/max/min
lag; r, m computed for law+NQ-2. Full verbatim table: `dataset-table.md`.

## Method (pure numpy — no torch, no sklearn)

- 5-fold CV, stratified deal on outcome (seed 1; folds pinned in per-fold.txt).
- Models: constant-median; LAW (thresholds fixed 1,1); ridge-linear (11 features,
  standardized, λ=10 — sensitivity λ∈{1,100} ±0.2pp); ridge-linear+r,m (NQ-2 arm);
  ridge-quad (all pairwise products+squares of the 11, same λ).
- Law levels refit per training fold (3 params); twin never sees r, m in base features.

## Results (held-out, pp)

| model | MAE | RMSE | R² |
|---|---|---|---|
| constant median | 23.74 | 26.82 | −0.00 |
| **law (r=1, m=1)** | 14.91 | 18.10 | 0.544 |
| ridge-linear | 34.35 | 36.20 | −0.82 |
| ridge-linear + r,m | 34.34 | 36.12 | −0.82 |
| **ridge-quad** | **9.05** | **11.87** | **0.804** |

Per-fold law vs quad: 14.09/9.26 · 14.81/10.28 · 15.52/7.61 · 15.75/9.44 · 14.43/8.64 —
quad wins every fold. Per-config: quad < law on 105/171; by >2pp on 97.

## D2 knee mini-test (secondary: knee-position target)

SPIN-21 knee relocation (n=7; R3 σ=0 excluded, law n/a): law (knee=2Δ/σ) MAE 2.17 ticks;
LOO linear twin 2.88 ticks — **law wins; n=6 is below any trainable bar** (booked).
knee-meta's 23 unified knees are already meta-booked; no twin trained there (n too small —
the fabric-twin's home turf is the rescue grid, not the knee table).

## Scars

- **Linear twin worse than median** — first-run red flag caught by the baseline ladder
  (median row is load-bearing, not decoration). Diagnosis: cliff extrapolation, not a bug;
  stratified folds did not cure it (34.35 unstratified vs 34.20-34.39 λ-band — robust).
- **NQ-2 degeneracy:** r ≡ span/15 in this corpus (σ, δ pinned by every harvested spin).
  The >50% collapse bar is untestable here, not merely failed — needs a σ/δ-varying corpus.
- spin11 pd=12 wall-inert rows (8.0% at m=1.0) share the m-coordinate with hard walls —
  the twin learns "pd=12 ⇒ no wall" only via pd features; a rate-condition (echo factor)
  is missing from the feature list — booked as a third-axis candidate.
- Dedupe asserted cross-source agreement <0.05pp — three independent replays agree byte-
  level on 5 anchors; corpus is replay-grade.
- Verdict asymmetry honored: PASS claimed only for the quad twin; the linear twin's failure
  is booked first-class (the pre-registration says "learned model" — the honest twin family
  result is mixed, pass requires interactions).

## What this buys NQ-2+ / next

The laws carry the cliffs (R² 0.544 from 3 params); interactions beyond them carry
~26pp more. The prize question — is there a THIRD constant hiding in the quad twin's
residuals (R² 0.804 ≠ 1) — is exactly NQ-2's follow-up on a σ/δ-varying corpus.
