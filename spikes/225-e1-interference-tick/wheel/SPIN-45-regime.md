# SPIN-45 — REGIME: EDGE-SPACING RESONANCE (g × P commensurability map)

Date: 2026-09-04 · Spoke: REGIME (6) · Predecessor: SPIN-33 (filed
next-spoke proposal, executed here) · Script: `wheel/spin45_regime.py` ·
Output: `wheel/spin45-regime-output.txt` (unique spoke-suffixed name,
python3 -u redirect, no pipes) · Not committed.

## Design

SPIN-33's filed proposal verbatim: inter-edge gap g = 240/E ∈ {40, 48,
60, 80, 120, 240} × scheduler period P ∈ {8, 12, 16, 24, 32, 48}, 36
cells, at fixed J=153 and fixed slope s=6 (feasible at every gap:
(g−1)·6 ≥ 153). Phase swing = max−min mean osc% over offsets 0..P//2
(spin-18 convention; SPIN-33's 0..8 at P=16 = P//2), spread 5↔30, K=2,
seeds {1,7,42}. Amplitude flip dAmp = tax_s25 − tax_s15 at each cell's
own P under BOTH baselines (SPIN-17 scar), advisory-only.

## Pre-registered rule (SPIN-33, written before this spin; restated in
the script header BEFORE any panel run)

> "swing(t) monotonically decreasing in min distance
> |g/P − round(g/P)| modulo both; falsified if swing is flat across
> the resonance map."

Operationalization fixed in header: Spearman(swing, d) over 36 cells;
VALIDATED iff ≤ −0.70 AND range ≥ 5.0pp; FALSIFIED iff range ≤ 3.0pp
(flat) or Spearman ≥ +0.70 (inverted); else MIXED. No rule edited after
any panel run. Structural pre-check (SPIN-44 scar): no pd sweep; N=6 ≤
2·pd+1=7 holds; divergence gate (max resid < 10⁶) asserted on EVERY
run — never tripped (traces banded [400,553]; no exclusions needed,
no post-hoc gates used).

## Canary receipts — ALL PASS (gate cleared)

- a. Harness provenance: dyn45 = spin-28/33 dyn_run VERBATIM + read-only
  ledger; 34 configs byte-identical vs sp33.dyn_run (imported
  spin33_regime module).
- b. Anchors 5-seed: ladder15 K=1 71.48 / ev 5791.6 / debt 106378.4;
  zero K=1 77.26 / 8756.4 / 187833.6 — digit-exact vs 71.5/5792/106378
  and 77.3/8756/187834 (SPIN-5 rounding tolerance).
- c. SPIN-33 swing replays: E1s1 **16.3pp** ✓, E6s6 **1.5pp** ✓ (tol 0.2).
- d. gate=never ≡ mc=0: n_draws=created=deleted=0 on 6 arms; J==153 and
  edge-count==240/g asserted at every gap; SPIN-15 ledger closure assert
  (g-balance + mass-balance, integer-exact) LIVE on every arm.
- e. Double-run determinism: 2 dual runs byte-identical (resid + ledger).

## Results — resonance map, swing(g,P) in pp

| g\E | P=8 | P=12 | P=16 | P=24 | P=32 | P=48 | row mean |
|-----|-----|------|------|------|------|------|----------|
| 40 (6) | 4.3 | 5.8 | 1.5 | 7.3 | 8.4 | 5.4 | 5.5 |
| 48 (5) | 9.6 | 25.0 | 2.6 | 26.8 | 0.5 | 27.7 | 15.4 |
| 60 (4) | 0.8 | 25.4 | 1.1 | 1.1 | 1.9 | 1.8 | 5.3 |
| 80 (3) | 10.0 | 6.2 | 10.7 | 6.1 | 14.5 | 18.5 | 10.9 |
| 120 (2) | 30.1 | 36.0 | 6.7 | 40.8 | 8.0 | 17.8 | 23.2 |
| 240 (1) | 18.8 | 20.8 | 26.3 | 22.4 | 15.6 | 40.1 | 24.0 |

d=|g/P−round(g/P)| map in the output file; binned mean swing by d:
d=0 → **22.2pp** (n=17), d=0.125 → 1.9, d=0.167 → 5.4, d=0.25 → 4.8,
d=0.333 → 8.8, d=0.5 → **7.3pp** (n=8).

- Spearman(swing, d) = **−0.606** (VALIDATED needs ≤ −0.70)
- map swing range = **40.3pp** (flat-falsify gate ≤ 3.0)

## VERDICT: MIXED (per pre-registration)

The commensurability law is directionally supported but fails the
monotonicity gate, and it is NOT the dominant axis:

1. **Direction holds at the extremes**: commensurate cells (d=0, edges
   landing phase-locked with spread ticks) average 22.2pp swing vs 7.3pp
   at maximally incommensurate d=0.5 — a 3× resonance contrast, and the
   E1s1-vs-E6s6 unification works exactly as filed (g=240/P=16 integer
   ratio → big swing; g=40/P=16 d=0.5 → the 1.5pp collapse cell).
2. **But a g-scale MAIN EFFECT dominates the map**: row means rise
   almost monotonically in gap (5.5/15.4/5.3/10.9/23.2/24.0 for
   g=40…240) largely irrespective of d — SPIN-33's density axis
   survives the commensurability test as the primary swing factor;
   Spearman(swing, g) is strongly positive. The rule's single-scalar
   d-law cannot absorb this second factor, hence −0.606, not ≤ −0.70.
3. **Non-monotone middle bins** (advisory): d=0.125–0.333 bins average
   1.9–8.8pp, BELOW the d=0.5 bin's 7.3pp — small-n bins (1–5 cells),
   but a strictly decreasing-in-d curve is already excluded visually.
4. **Within-d=0 variance is huge** (2.6–40.8pp): commensurability is
   nearly necessary-but-not-sufficient for peak swing — e.g. g=48/P=16
   (ratio 3) swings only 2.6pp while g=120/P=24 (ratio 5) swings 40.8.
5. Amplitude flip (advisory, both baselines): dAmp_TW ranges −21.2 to
   +40.8 across the map; matched-mean dAmp is near-zero on the whole
   g=40 row (renormalized quasi-static gradient, confirming SPIN-33)
   and flips sign with g and P elsewhere — the amplitude flip tracks
   the same two-factor structure but no clean d-law.

## Headline number

**Across the 36-cell g×P resonance map at pinned J=153 and s=6, phase
swing correlates with commensurability distance d=|g/P−round(g/P)| at
Spearman −0.606 with a 3× d=0-vs-d=0.5 contrast (22.2 vs 7.3pp mean),
but the pre-registered monotone-decreasing-in-d law fails its −0.70
gate because a gap-scale main effect (row means 5.5→24.0pp from g=40 to
g=240) dominates the map — commensurability modulates, density governs.**

## Scars / honest boundaries

- Slope is NOT held inert for phase by pinning alone: at g=240, P=16,
  s=1 replays 16.3pp but s=6 swings 26.3pp — the slope axis moves swing
  ~10pp at fixed g and J (extends SPIN-33's TWmean slope finding into
  the phase instrument; "fixed slope" results are slope-conditional).
- The registered d-statistic ignores ratio VALUE and g-scale — same
  confound class as SPIN-43's ρ (registered statistic confounded with
  the dominant factor). Future phase laws must register two-factor or
  g-matched designs.
- Offsets 0..P//2 give 5–25 offsets per cell; small-P cells have
  coarser swing estimates (5 offsets at P=8) — bin noise, not a bias.
- Advisory panel 2 taxes reuse each cell's own P (per SPIN-33
  convention P was pinned at 16); cross-P amplitude comparisons are
  therefore indicative only.
- One dev-run abort before any panel (static_fn takes a scalar spread,
  not a lateness list) — fixed; no rule text touched after any panel.

## Next-spoke proposal (SPIN-46+ candidate)

**RESONANCE-RESIDUAL / TWO-FACTOR PHASE LAW**: the d=0 column alone
spans 2.6–40.8pp — something beyond commensurability and gap scale
governs peak swing among phase-locked cells. Fix d=0 exactly and sweep
the integer ratio value r = g/P densely (e.g. g=240 pinned, P = 240/r
for r ∈ {2..30} divisors; cross-check at g=120), asking whether the
commensurate-column variance tracks r parity (edges alternating
in/out of spread-phase across periods), r magnitude, or the number of
distinct edge-phases per scheduler half-period. Pre-register: a
parity law (odd r > even r + 5pp) vs a flat-within-d=0 null;
falsify-with-style if the column variance is explained by the row
(g) effect alone (two-factor ANOVA-style decomposition on the
existing 36-cell map as the advisory prior).

---
Not committed/pushed; WHEEL-LOG.md append left to the cron lane, per
rules.
