# SPIN 8 — SPOKE: COHERENCE-RADIUS (mechanizing the fresh-cohort law)

**Lane:** wheel_spin8_coherence_radius · **Date:** 2026-09-03 07:19–07:35 AKDT ·
**Files:** `spin8_coherence_radius.py`, `spin8_diag.py`, `spin8-output.txt` ·
Fabric: `inventors-derby/exp_glm1.run_fabric` (E1 contract pinned: fdiv decay,
64-bit LCG, FIFO oldest-first expiry, snapshot decay). Integer-only in-loop
(one integer-overflow diagnostic capped at 10^18 for display only — the
overflow itself is a finding). Seeds {1, 7, 42, 1999, 20260902}, 4800 ticks,
drift=6, pd=3, K=1 unless noted. Full run ~50 s including diagnostics.

## Hypothesis (dispatched from SPIN-5-topology's proposal)

The fresh-cohort law becomes mechanistic if the graded ladder's strength is
**connectivity of the coherence graph**: adjacent ladder twins within a
coherence radius rho(delta) of each other form a chain anchored at the fresh
end. Two blades: (1) step-granularity sweep at fixed spread 30 — finer
granularity (shorter per-twin coherence gap) should help monotonically or
peak at the delta=12 chain; (2) delta × grammar interaction — fresh-vs-stale
flips/saturates where rho(delta) crosses the bloc gap, fit rho against the
topology lane's knee at 0.75·2Δ. Plus the brief-mandated prediction gate:
pre-register kcoh5 @ delta=12, spread 45 **before running**.

**Pre-registered (in committed source, written before any run):** P3 kcoh5@45
= 41.0%, band [34,50] (linear extrap 32.3; saturation-above-linear argued);
P1 connectivity edge between steps 3 and 5, steps {1,2,3} high; P2 FVS ≥ 0 at
all deltas, ladder overtakes cohort near delta≈20 (Law A rho=0.3Δ) vs ≤12
(Law B rho=0.625Δ).

## Self-canaries (both PASS — mandatory gate)

1. **Spread=0 byte-identity:** 12 codepaths, 2 N-groups, full result-dict
   equality + constructor-map asserts. PASS.
2. **Lane replay (12 anchors, tol ±0.2pp):** topology kcoh5@15
   74.1/50.6/72.8 (K=1/2/8), kcoh1@15 47.3/34.4/38.3, ladder@15
   71.5/60.0/70.7; pattern-grammar @30 K=1 ladder 26.8 / cohort 49.3 /
   kcoh5 53.2 — **all 12 exact to 0.1pp**. PASS.

## EXP 1 — step-granularity at fixed spread 30 (K=1 unless noted)

| step | N | lats | K=1 % | K=2 % | K=8 % |
|---:|---:|---|---:|---:|---:|
| 1 | 31 | [0..30] | **0.1** | 0.1 | 0.1 |
| 2 | 16 | [0,2..30] | 0.1 | 0.1 | 0.1 |
| 3 | 11 | [0,3..30] | 0.1 | 0.1 | 0.1 |
| 5 | 7 | [0,5..30] | 0.3 | 0.4 | **18.0** |
| **6** | **6** | [0,6,12,18,24,30] | **26.8** | 28.9 | 14.0 |
| 10 | 4 | [0,10,20,30] | 10.5 | 12.9 | 12.5 |
| 15 | 3 | [0,15,30] | 10.0 | 12.4 | 12.7 |
| 30 | 2 | [0,30] | 12.4 | 14.5 | 14.1 |

**Finer granularity is catastrophically WORSE, not better** — 0.1% vs 26.8%
(≈270×). There is an interior optimum at N=6/step6, but it is NOT the
delta=12 coherence chain: diagnostics show the fine-ladder collapse is a
**divergent band oscillation** — ALL N twins fire EVERY tick (meanMult =
N exactly, e.g. 31.00/31 at step1), the per-tick net shove grows
geometrically until it **overflows 10^18** (Python bigints keep it exact;
capped for display), consecutive fire-tick nets flip sign at **1000‰**, and
|g−s_true| > 60 on 99.8% of ticks. This is the zero-lock chatter of
SPIN-5-pattern in its runaway regime.

**The bifurcation is an integer law: divergence iff N > 2·pd.** Each of the
N simultaneous firers shoves e//pd; the echo factor is |1 − N/pd|, which
exceeds 1 exactly when N > 2pd (=6 here). Verified three independent ways:

- **Discriminator (DIAG 2):** a same-error fresh bloc of M=6 + one laggard
  (N=7, no fine steps at all) **diverges (0.2%)**, while M=5 (N=6) is safe
  at 53.0% ≈ kcoh5@30 (53.2, continuity). Duplicate mass and gradient bands
  obey the same wall — grammar structure is irrelevant to divergence.
- **K-rescue (DIAG 1):** step5 K=8 converges (18.0%, meanMult drops 7.0 →
  3.6): longer pulse memory damps the alternation; K=2 still diverges.
- **Delta-independence (DIAG 3):** the N=6 optimum persists at delta ∈
  {6, 12, 24} (25.3 / 26.8 / 11.7 vs step10's 9.4 / 10.5 / 9.4) — the
  optimum tracks the pulse dial (2·pd), not delta. Coefficient check: at
  N=6=2pd the echo factor is exactly 1 — marginal, and indeed the N=6
  configs sit at the edge (occasional 6-fire bursts that barely decay,
  resid>60 on 8‰ of ticks at step6 K=1).

**The step5→step6 cliff (0.3 → 26.8) is the N=7 > 2·pd wall, not a coherence
edge.** The proposed monotone-help law and the coherence-chain-optimum law
are both FALSIFIED; the operative variable is simultaneous firing mass.

## EXP 2 — delta ∈ {6,9,12,15,18,24} × grammars at spread 30, K=1

Primary metric: true% at FIXED eval window 12 (trigger delta varies, spec
pinned — cross-delta comparability). Native trueΔ in parentheses where it
matters.

| delta | kcoh5 | kcoh1 | FVS | ladder | cohort | ladder−cohort |
|---:|---:|---:|---:|---:|---:|---:|
| 6 | 62.1 (37.0) | 10.2 (5.3) | **+51.9** | 25.3 (10.4) | 41.1 (32.4) | −15.8 (−22.0) |
| 9 | 58.7 (47.7) | 11.0 (8.3) | +47.7 | 24.1 (18.6) | 48.1 (47.1) | −24.0 (−28.5) |
| 12 | 53.2 (53.2) | 13.2 (13.2) | +40.0 | 26.8 (26.8) | 49.3 (49.3) | −22.5 (−22.5) |
| 15 | 48.8 (60.9) | 14.1 (19.9) | +34.7 | 25.4 (36.3) | 49.2 (50.2) | −23.7 (−13.9) |
| 18 | 41.2 (61.4) | 14.8 (30.5) | +26.5 | 17.3 (49.1) | 49.3 (51.7) | −32.1 (−2.6) |
| 24 | 30.9 (81.5) | 11.9 (53.3) | **+19.0** | 11.7 (69.2) | 49.3 (57.2) | −37.6 (**+12.0**) |

- **Fresh-vs-stale NEVER flips in range:** FVS > 0 at all six deltas,
  compressing near-linearly (≈ −2pp per delta; endpoint fit zero-cross at
  delta ≈ 34, outside the sweep — mechanistically bracketed by the lag-30
  staleness errors: plateau diff 30, ramp diff 48). The fresh side of the
  bloc gap is load-bearing at every trigger tolerance tested.
- **kcoh5 declines with delta at pinned spec** (62.1 → 30.9): bigger trigger
  tolerance = bigger pulses per fire = bigger overshoot ripple against a
  fixed ±12 spec. kcoh1 is flat ~10–15 (already saturated-bad). The FVS
  compression is almost entirely the fresh side giving back ground.
- **cohort@30 is structurally pinned at ≈49.3** (3v3 tie locks the estimate
  mid-bloc regardless of delta).
- **rho fit — two blades agree:** in the NATIVE (co-moving) window, ladder
  overtakes cohort between delta 18 and 24: parity at **delta\* ≈ 19.1** →
  kappa = ladder_gap/delta\* = 6/19.1 = **0.315**. The topology lane's
  spread-blade gives kappa = knee/(5·delta) = (18.3–19.6)/60 = **0.305–0.327**.
  Two independent measurements: **rho(delta) ≈ 0.31·delta** (rho(12) ≈ 3.7),
  implied ladder knee spread = 5·rho ≈ **0.78·2Δ** — the topology lane's
  0.75·2Δ knee CONFIRMED as a co-moving-window law. Law B (rho = 0.625·delta
  = slope law) is dead by 2×.
- **But the pinned window shows NO rescue:** at fixed spec ±12 the ladder
  never recovers (11.7% at delta 24) — the parity exists only if your
  acceptance widens with your trigger. Spec-relative vs spec-pinned is a
  real distinction for any E4/O4 mode dial: the coherence radius orders
  grammars only under co-moving acceptance.

## EXP 3 — pre-registered prediction gate: **FAIL (informative)**

Predicted (committed before running): kcoh5 @ delta=12, spread=45, K=1 =
41.0%, band [34,50]. **Measured 52.5%** (per-seed 517/532/521/531/523 —
tight). Missed the band by +2.5pp; the linear extrapolation (32.3) was even
further off. Salvage: the saturation-above-linear direction was correct and
is stronger than argued — laggard damage is essentially **fully saturated
by lag 30**: 74.1 (@15) → 53.2 (@30) → 52.5 (@45). Beyond lag ≈ 30 ≈
2.5·delta the stale twin's firing duty and pulse mass stop mattering; the
fresh cohort fixes the equilibrium and the laggard only decorates it.

## Verdict: MIXED

- **Mechanization: ACHIEVED, but by a different variable than proposed.**
  The fresh-cohort law's missing mechanism is not coherence-graph
  connectivity — it is the **2·pd firing-mass wall** (divergence iff N > 2·pd,
  verified by duplicate-bloc discriminator, K-rescue, and delta-independence)
  plus the **rho ≈ 0.31·delta coherence radius** which orders graded-vs-bloc
  grammars under co-moving acceptance (two-blade agreement 0.315 vs
  0.305–0.327), plus **lag-saturated laggard damage** (flat beyond lag ≈ 2.5·delta).
- **Coherence-chain optimum law: FALSIFIED** (blade 1). The interior optimum
  at N=6 tracks 2·pd, is delta-independent, and sits exactly at the marginal
  echo factor |1 − N/pd| = 1.
- **Fresh-vs-stale flip: does not exist in delta ∈ [6,24]** (blade 2) — FVS
  compresses linearly, extrapolated zero-cross ≈ 34.
- **Mandated prediction: FAIL** (52.5 vs [34,50]) — booked as the wheel's
  second consecutive prediction-gate miss on saturation-magnitude calls;
  the direction was right, the magnitude of saturation was not.

## Headline numbers

1. **0.1% vs 26.8% at fixed spread 30:** every fine ladder (steps 1–5, N ≥ 7)
   locks into all-N-fire divergence with integer overflow past 10^18 and
   1000‰ sign-flipping nets — the wall is **N > 2·pd**, not granularity.
2. **rho(delta) = 0.31·delta, measured twice independently** (delta-blade
   parity 19.1 → 0.315; topology spread-knee → 0.305–0.327); knee spread =
   0.78·2Δ confirms the topology lane's 0.75·2Δ — but only under co-moving
   acceptance; at pinned spec ±12 there is no rescue (ladder 11.7% at delta 24).
3. **FVS > 0 at every delta** (51.9 → 19.0pp, no flip, zero-cross ≈ 34);
   laggard damage saturates totally by lag 30 (53.2 → 52.5 at lag 45 —
   pre-registered prediction missed high by 2.5pp).

## Scars / honest boundaries

- **Prediction-gate miss (2nd consecutive on saturation magnitude):** my
  band [34,50] assumed partial saturation; reality is total saturation by
  lag 30. Lesson: when a duty cycle is already ≫ threshold, the next +50%
  of stimulus magnitude buys ~nothing — predict the flat tail, not the tail's
  slope.
- **P2 was window-ambiguous** ("ladder overtakes near delta 20" — true only
  in the native window). Pre-registrations must pin the eval window; the
  native/fixed distinction changed the answer from "parity at 19.1" to
  "never".
- **N-step confound in blade 1 was real but got converted:** DIAG 2 (pure
  duplicate bloc, no steps) shows the collapse is N-mass, not step-geometry;
  DIAG 3 shows delta-independence. The granularity sweep alone could not
  have said this.
- The delta* ≈ 19.1 parity and zero-cross ≈ 34 are linear interpolations on
  5-seed means (per-seed spread ±1–4‰; n=5, descriptive).
- K=8 rescue of step5 (18.0%) shows the wall is soft under long pulse
  memory — the 2·pd law is a K=1/K=2 statement; K interacts with the wall
  (booked for the proposed spoke).
- Native-window FVS at delta 24 shrinks to 81.5−53.3 = 28.2 (not 19.0) —
  the compression rate itself is window-dependent; only the no-flip
  conclusion is window-robust.

## New spoke proposed: YES — PULSE-DIAL / MASS-COMPENSATION

The 2·pd wall makes pd (shove denominator) a first-order dial this fleet
has never swept: (1) pd ∈ {1,2,3,6,12} × N ∈ {2..8} at fixed spread 30 —
does the divergence boundary track N = 2·pd exactly, and is the N=6/pd=3
home point an accident of choosing N=2pd? (2) mass-compensated emission:
divide the per-tick total shove by the firing count (net = Σe/n_f) — an
E-lane fabric variant that should erase the wall and rescue fine ladders;
if it does, the 2·pd law is confirmed as causal and the fabric gets a
free structural upgrade. (3) optional: FVS zero-cross verification at
delta ∈ {30, 36, 48}.

## Log-ritual bookkeeping

Proposal-dispatched spin (SPIN-5-topology's proposal); LCG advance recorded:
2035015474 → **368800899** → mod 10 = **9** — the wheel ledger resumes LCG
selection at the next cycle.

VERDICT: MIXED — fresh-cohort law mechanized, but the mechanism is the 2·pd firing-mass wall (N > 2·pd diverges: 0.1% vs 26.8% at spread 30, verified by duplicate-bloc/K-rescue/delta-independence triad), with rho ≈ 0.31·delta confirmed on two blades as a co-moving-window law (0.78·2Δ knee) and FVS never flipping in delta 6–24; the mandated prediction FAILED high (52.5 vs [34,50]) because laggard damage saturates totally by lag 30.
