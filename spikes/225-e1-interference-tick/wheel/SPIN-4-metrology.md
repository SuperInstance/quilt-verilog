# SPIN 4 — SPOKE 1: METROLOGY (SPREAD-LAW)

**Lane:** wheel_spin4_metrology · **Date:** 2026-09-03 00:00 AKDT ·
**Files:** `spin4_metrology.py`, `spin4-output.txt` · Fabric: `inventors-derby/exp_glm1.run_fabric` (E1 contract items pinned: fdiv decay, 64-bit LCG, FIFO oldest-first expiry, snapshot decay). Integer-only inside the loop.

## Hypothesis

Interference-arm true-residency collapses at a critical max−min twin latency
spread (predicted near 15–20, where disagreement-slope × spread crosses
~2Δ=24), largely independent of N once spread is controlled — and, since
only spread is hypothesized to matter, independent of the latency
*multiset pattern*. This decouples N from spread, which SPIN-3 flagged as
confounded in F7's staggered ladder (spread = 10·(N−1)).

## Operationalization

N=6 fixed (control arm varies N), K∈{1,2,8}, interference arm, 4800 ticks,
stress params (delta=12, drift=6, pd=3), seeds {1, 7, 42, 1999, 20260902}.
Spread s ∈ {0,5,10,15,20,30} realized as TWO distinct multisets:

- **ladder** : [0, s/5, 2s/5, …, s] — even steps (graded staleness)
- **cohort** : [0,0,0,s,s,s] — binary split (coherent fresh/stale cohorts)

Pattern-invariance is thus directly testable per spread. Control:
spread=30 ladder at N∈{2,3,6} (N-independence). Sequential reference per
spread (ladder).

## Self-canaries (both PASS)

1. **spread=0 byte-identical across variants:** ladder(0) ≡ cohort(0) ≡
   [0]×6 — all 3 K comparisons byte-identical (name-map/label bug would break this).
2. **spin3 replay:** ring N=6 K=8 → 82.6% / 7589 events and all_to_all
   N=6 K=8 → 10.1% / 19321 events — exact match to spin3-output.txt means.

## Raw results — interference, mean of 5 seeds (per-seed ‰ in spin4-output.txt)

### true-residency % by spread (N=6)

| spread | K=1 ladder | K=1 cohort | K=2 ladder | K=2 cohort | K=8 ladder | K=8 cohort |
|-------:|-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| 0 | 77.3 | 77.3 | 50.0 | 50.0 | 69.0 | 69.0 |
| 5 | 97.6 | 99.0 | 84.9 | 77.1 | 90.2 | 88.8 |
| 10 | **93.5** | 75.9 | **89.7** | 69.4 | **90.8** | 82.6 |
| 15 | **71.5** | 57.1 | **60.0** | 41.8 | **70.7** | 61.4 |
| 20 | **49.2** | 49.3 | **47.7** | 38.5 | **43.2** | 47.3 |
| 30 | **26.8** | **49.3** | **28.9** | **33.3** | **14.0** | **21.7** |

Control (spread=30 ladder): N=2: 12.4/14.5/14.1% (K=1/2/8); N=3:
10.0/12.4/12.7%; N=6: 26.8/28.9/14.0%. Sequential reference (ladder):
100.0 / 99.2 / 85.0 / 62.6 / 55.8 / 57.6% across spread 0→30 — the same
knee, shifted slightly earlier (~10–15).

## Verdict: MIXED

**Component 1 — critical spread near 15–20: VALIDATED.** The ladder arm
collapses between spread 10 and 20 at every K (K=1: 93.5→71.5→49.2 at
10/15/20; K=8: 90.8→70.7→43.2). The knee sits at spread ≈ 15, matching the
2Δ=24 crossing prediction. Sequential arm shows the same knee (85.0→62.6
across 10→15) — the spread law is arm-general.

**Component 2 — N-independence: SUPPORTED (first-order).** At spread=30,
N=2/3/6 all sit in the collapsed 10–29% band (vs ~90% at spread=10) — no
N=2 escape. But N is second-order, not null: N=6 doubles N=2/3 at K=1/2
(26.8/28.9 vs 12.4/12.4) — extra twins soften the collapse slightly at
matched spread.

**Component 3 — pattern-invariance: FALSIFIED.** Only spread does NOT
matter alone. Cohort vs ladder diverge sharply: at spread=10, ladder K=1
93.5% vs cohort 75.9% (cohort *worse* — a 3v3 stale bloc outranks graded
neighbors); at spread=30 the ordering flips — cohort K=1 49.3% vs ladder
26.8% (the coherent majority rescues residency where the graded ladder
cannot). Spread is first-order; pattern is a real second-order dial.

Sub-findings:
- **spread=0 anomaly:** 50–77%, *worse* than spread=5 (97.6%). Perfectly
  synchronized duplicates all-trigger simultaneously — a chatter/debt
  pile-up mode distinct from staleness disagreement (events 8756–15133,
  debt 188k–512k, near-zero cancels). The spread law is non-monotone at
  the origin: zero spread is not the optimum, *small* spread is.
- Events/debt scale with spread roughly linearly for ladder (2598→14952
  events, K=1, spread 5→30); cohort carries ~2× ladder's debt at every
  spread ≥ 10.
- The spin3 "ring 82.6%" reappears as cohort@10 K=8 = 82.6% — the ring
  benefit is reproducible as a coherent-cohort effect, not a ring-specific
  one.

## Headline number

**N=6, K=1, ladder: true-residency 93.5% → 71.5% → 49.2% across spread
10/15/20 — the knee sits at spread ≈ 15 (the 2Δ crossing), with N varying
N=2→6 at spread=30 only in the 10–29% collapsed band.**

## Scars / bugs

- None hit: both canaries passed first run; no name-map or arm-label bugs.
- Design scar booked: the spread grid {0,5,10,15,20,30} is too coarse to
  localize the knee tighter than ±5 and has no points in 20–30; a future
  sweep should densify 12–24.
- spread=0's non-identity with spread=5 broke a hidden monotonicity
  assumption in the original hypothesis text — the spread law is U-shaped
  at the origin, not monotone.
- Per-seed variance tiny (±10–15‰ typical), 5 seeds sufficient; no seed
  anomalies.

## New spoke proposed: YES — PATTERN-GRAMMAR (second-order dial)

The falsified pattern-invariance is the next measurement: hold spread=15
(at the knee, where sensitivity is maximal) and sweep the multiset
*grammar* — graded ladder, k-cohort splits (k∈{1..5} fresh), bimodal
weights, single outlier vs single laggard. Hypothesis: residency is set by
the size of the largest mutually-coherent cohort relative to N
(cohort-majority law), which would unify spin3's ring/star results and this
spin's cohort-over-ladder rescue at spread=30. Also densify the ladder
knee (spread 12–24, step 2) to pin the critical spread against the 2Δ=24
prediction to within ±2.

VERDICT: MIXED — the collapse knee sits at spread≈15 (2Δ crossing) and is N-independent first-order, but pattern-invariance is falsified (cohort 49.3% vs ladder 26.8% at spread=30, K=1) and spread=0 is a chatter anomaly worse than spread=5.
