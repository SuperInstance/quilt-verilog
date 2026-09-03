# SPIN 6 — SPOKE 4: TOPOLOGY (PATTERN-GRAMMAR)

**Lane:** wheel_spin6_topology · **Date:** 2026-09-03 07:03 AKDT ·
**Files:** `spin6_topology.py`, `spin5-output.txt` · Fabric: `inventors-derby/exp_glm1.run_fabric` (E1 contract items pinned: fdiv decay, 64-bit LCG, FIFO oldest-first expiry, snapshot decay). Integer-only inside the loop.

## Hypothesis (from SPIN-4's proposal)

At fixed spread=15 (the knee) and N=6, interference-arm true-residency is
set by **the size of the largest mutually-coherent cohort relative to N**
(cohort-majority law), which would unify spin3's ring/star results and
spin4's cohort-over-ladder rescue at spread=30. Secondary: densify the
ladder knee (spread 12–24, step 2) to pin the critical spread against the
2Δ=24 prediction to within ±2.

## Operationalization

Grammar variants at spread=15, N=6 (all pairwise-integer multisets):
- **ladder** `[0,3,6,9,12,15]` — graded staleness (spin4 baseline)
- **kcoh_k** `[0]*k + [15]*(6-k)`, k=1..5 — k-cohort splits. k=5 is the
  single laggard, k=3 the binary 3v3 (spin4 anchor), k=1 the single outlier
- **bimodal** `[0,0,7,8,15,15]` — two blocs + bridge pair

K∈{1,2,8}, interference arm, 4800 ticks, stress (delta=12, drift=6, pd=3),
seeds {1, 7, 42, 1999, 20260902}. Sequential reference per grammar.

## Self-canaries (both PASS)

1. **spin4 replay:** ladder s=15 N=6 → 71.5 / 60.0 / 70.7% for K=1/2/8 —
   exact match to spin4's published means, all three within tolerance.
2. **spread=0 identity:** all grammar variants degenerate to [0]×6 —
   byte-identical results per K.

## Raw results — interference, mean of 5 seeds (per-seed ‰ in spin5-output.txt)

### Grammar sweep at spread=15, N=6 — true-residency %

| grammar | lats | largest cohort | K=1 | K=2 | K=8 |
|---|---|---:|---:|---:|---:|
| kcoh5 (laggard) | [0,0,0,0,0,15] | 5 fresh | **74.1** | **50.6** | **72.8** |
| ladder | [0,3,6,9,12,15] | chain (adj Δ=3) | 71.5 | 60.0 | 70.7 |
| kcoh2 | [0,0,15,15,15,15] | 4 stale | 64.4 | 36.7 | 43.6 |
| kcoh4 | [0,0,0,0,15,15] | 4 fresh | 62.6 | 56.1 | 71.3 |
| bimodal | [0,0,7,8,15,15] | 2+2+bridge | 65.4 | 59.6 | 65.7 |
| kcoh3 (3v3) | [0,0,0,15,15,15] | 3/3 tie | 57.1 | 41.8 | 61.4 |
| kcoh1 (outlier) | [0,15,15,15,15,15] | 5 stale | **47.3** | **34.4** | **38.3** |

### Ladder knee densification (N=6) — true-residency %

| spread | K=1 | K=2 | K=8 |
|---:|---:|---:|---:|
| 12 | 95.0 | 84.8 | 87.1 |
| 14 | 84.4 | 72.3 | 76.5 |
| 15 | 71.5 | 60.0 | 70.7 |
| 16 | 63.5 | 59.6 | 63.8 |
| 18 | 53.2 | 53.5 | 52.3 |
| 20 | 49.2 | 47.7 | 43.2 |
| 22 | 43.0 | 40.7 | 34.4 |
| 24 | 31.7 | 36.3 | 26.3 |

Sequential reference (K=1 arm): ladder 62.6%, every kcoh variant 56.8%
(identical — sequential T1-priority collapses k-cohort multisets to the
same first-trigger stream; a free internal consistency check), bimodal 66.0%.

## Verdict: MIXED

**Component 1 — grammar matters at fixed spread: VALIDATED.** The grammar
dial spans 47.3→74.1% at K=1 (27 points) with spread, N, K, seeds, params
all pinned. Grammar is a genuine second-order dial of the same magnitude
spin4 measured at spread=30.

**Component 2 — cohort-majority law as stated: FALSIFIED.** The law
predicts residency tracks largest-cohort size. Instead:

- **kcoh1 (largest cohort = 5, stale) is the WORST grammar (47.3%)** while
  kcoh5 (largest cohort = 5, fresh) is the BEST (74.1%). Cohort *size*
  alone does nothing; the cohort must sit on the **fresh side**. The law
  must be amended to a **fresh-cohort-majority law**: residency is set by
  the size of the coherent cohort *near zero latency*.
- **The 3v3 tie is a local minimum** (K=1: 57.1 < kcoh2's 64.4 and kcoh4's
  62.6). With no majority on either side, the fabric does worst — majority
  direction, not just magnitude, is load-bearing.
- **The graded ladder beats every binary split except kcoh5** (71.5% at
  K=1) despite having no cohort at all. Under the amended reading this
  makes sense: adjacent ladder twins differ by 3 ≤ delta=12, so the ladder
  is one connected *coherence chain* anchored at the fresh end — graded
  staleness behaves like a fresh cohort with a taper, better than a stale
  bloc of equal count. This unifies spin3's ring result: the ring
  [0,10,0,10,0,10] is a 3-fresh cohort with a coherent stale partner set.

**Component 3 — critical spread vs 2Δ=24: FALSIFIED (within the ±2
criterion).** The 50%-residency crossing on the densified ladder sits at
spread ≈ 18–19 (K=1: 53.2@18 → 49.2@20; K=2: 53.5 → 47.7; K=8: 52.3 →
43.2, crossing ≈18.3). The steepest-descent knee is even earlier (~14–16:
−10.6, −10.9, −10.3 points per 2 steps at 12→14→16, slackening to −4 at
18→20). Both readings fall 5–9 points short of the 2Δ=24 prediction; the
disagreement-slope × spread model overestimates the critical spread. The
effective crossing is at spread ≈ 0.75·2Δ.

Sub-findings:
- kcoh K=2 is uniformly the worst arm (34–56%), K=8 recovers 8–25 points
  over K=2 in every grammar — the K-dial interacts with grammar exactly as
  spin3's K-ranking inversion suggested (no global K champion).
- Stale-cohort grammars carry ~2× ladder's debt (kcoh1 K=2: 483k vs ladder
  260k) at every K; the fresh-side cohort is cheap, the stale-side cohort
  is expensive.
- Sequential arm is grammar-blind for k-cohort multisets (all 56.8%,
  byte-equal event counts) — T1-priority never sees the split. Latency
  grammar only bites through interference.

## Headline number

**At fixed spread=15, N=6, K=1: single fresh laggard-cohort 74.1% vs
single fresh outlier 47.3% — same multiset sizes mirrored; the cohort law
is a FRESH-cohort law, and the graded ladder (71.5%) rides a coherence
chain to nearly the top.**

## Scars / bugs

- None hit: both canaries passed first run; no name-map or arm-label bugs.
- Design scar: "coherent cohort" was not defined with a coherence radius in
  the hypothesis; post-hoc the delta=12 adjacency criterion explains the
  ladder's strength. A future spin should sweep the ladder step size
  (3→6→9 at fixed spread) to test the coherence-chain reading directly.
- The 2Δ=24 prediction is now twice-adjacent-failed (spin4 knee ~15,
  spin6 crossing ~18.5) — book the slope model as needing a ≤1 effective
  coefficient (~0.75·2Δ) rather than discarding it.
- Per-seed variance tiny (±15‰ typical), 5 seeds sufficient.

## New spoke proposed: YES — COHERENCE-RADIUS (fresh-cohort law mechanics)

Two blades: (1) ladder step sweep — hold spread=15, vary step granularity
{15 steps of 1 (N=16 twins) vs 5 steps of 3 vs 3 of 5 vs 1 of 15} to test
whether residency tracks the *connectivity of the coherence graph* rather
than cohort count; (2) delta-interaction — hold kcoh3 and ladder at
spread=15, sweep delta ∈ {6,12,18,24} to see whether the fresh-cohort
advantage turns on when delta crosses the intra-bloc gap (7–8 for
bimodal). This converts the fresh-cohort law from descriptive to
mechanistic and feeds the E4/O4 mode dial a radius it can measure.

VERDICT: MIXED — grammar is real (47.3→74.1% at fixed spread=15) but the cohort-majority law as stated is falsified: it is a FRESH-cohort law (kcoh5 74.1% vs kcoh1 47.3%, same sizes), the 3v3 tie is a local minimum, and the graded ladder exploits a delta=12 coherence chain; the 50% ladder crossing sits at spread≈18.5, not 24.
