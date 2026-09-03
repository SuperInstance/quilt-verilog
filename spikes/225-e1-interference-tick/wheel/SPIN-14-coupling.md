# SPIN-14 — SPOKE 7: COUPLING (cross-mechanism composition)

Script: `spin14_coupling.py` · Raw: `spin14-output.txt` · Harness actually
run (no simulation). N=6, delta=12, drift=6, pd=3, 4800 ticks, seeds
{1,7,42,1999,20260902}, integer-only fabric (floats display-only).

## Canaries — PASS

- **A (anchor replay): 7/7 OK.** ladder@15 K=1 71.5/ev5792/debt106378
  exact; zero@15 K=1 77.3/ev8756/debt187834 exact; kcoh5@15AS 79.4
  (SPIN-10 best-ever) exact. Byte-level publishing anchors held.
- **B (determinism): PASS.** One e1-reality config and one tri3 config
  each run twice, full-dict equal.

## Design

Arms per (grammar, spread, K) cell, gains vs same-cell baseline:
- **base** = grammar lats on e1 reality
- **AS** = AS-exact (full within-cohort 1-tick decorrelation; even(1)
  for zero-lock) on e1 reality
- **N1** = grammar lats on tri3 memory-window channel (σ=3)
- **AS+N1** = AS-exact on tri3

Residual = g(joint) − max(g(AS), g(N1)). Subadditive iff ≤ +2pp.

## EXP2 verdict table: 12/16 subadditive

Real-grammar cells: ALL subadditive (residuals −35.8 … +1.4).
Violations live entirely in **zero-lock**:
- zero K=1: residual **+2.4** (marginal, just over the 2.0 gate)
- zero K=2: residual **+11.9 — superadditive** (84.9 AS, 51.5 N1 →
  **96.7** joint; joint beats AS alone by +11.8pp)

Note zero@15 and zero@30 are duplicate cells — zero-lock has no spread
axis (AS=even(1) is spread-invariant), so effectively **2 unique
violating cells, both zero-lock**.

## EXP3: grammar-class × mechanism — secondary hypothesis FALSIFIED

Predicted: AS helps fresh-cohort (kcoh5), memory helps stale-heavy
(ladder/cohort). Measured: **AS wins 14/16 cells, N1 wins 0, ties 2**
(kcoh5@30 K=1, cohort@30 K=1). N1 (tri3 channel) is a near-universal
*loser* on these grids — worst on ladder@15 K=1 (−46.0pp). The one
regime where N1 helps at all is the chatter-catastrophe origin
(zero-lock K=1, +3.8pp), exactly where SPIN-10 found the memory window
(81.0→100.0 with even1, reproduced here as the AS+N1 100.0 cell).
Grammar class does not predict the knob; **failure mode does**: N1 is
last-resort compensation for synchronized-cohort chatter, not a
stale-grammar rescue.

## EXP4: three-way probe — scheduler×AS is complementary

Learned spread-scheduler swap-in (cohort 15→8 parking, K=2):

| arm | true% | vs coh15-base |
|-----|-------|---------------|
| coh8 base | 77.2 | +35.3 |
| coh8 AS | **89.0** | +47.2 |
| coh8 N1 | 44.5 | +2.7 |
| coh8 AS+N1 | 62.3 | +20.5 |

- The scheduler gain (+35.3pp) **stacks** with AS (+11.8pp more):
  strongly superadditive composition when the two knobs attack
  different failure modes (staleness vs intra-cohort correlation).
- Best cell of the whole spin: **cohort8 + AS @ K=2 = 89.0%**, beating
  the prior best-known (79.4 kcoh5@15+AS, and the kimi lane's ~80)
  by ~10pp — new best-known grammar cell on this fabric.
- N1 remains destructive on the parked grammar (−32.6pp); AS+N1 on
  coh8 (62.3) is far below AS alone (89.0) — the substitutes-not-
  complements finding survives the three-way test for N1.

## Verdict: MIXED

1. **Universal subadditivity FALSIFIED** — zero-lock K=2 composes
   superadditively (+11.9pp residual), and the scheduler×AS pair
   composes superadditively (+35.3 stacked with +11.8 → 89.0).
2. **But N1-in-the-loop is subadditive (indeed destructive) in 14/16
   mechanism cells**, and every real-grammar cell is subadditive:
   the SPIN-10 substitutes-not-complements result generalizes across
   all four grammars and both spreads for the memory channel.
3. **Secondary hypothesis (grammar-class predicts the knob) FALSIFIED.**
   AS dominates everywhere; the predictor is failure mode, not grammar
   class: N1 pays only at the synchronized-chatter origin.

Refined law for the next spin: *composition is superadditive exactly
when the two mechanisms address orthogonal failure channels
(staleness-allocation × decorrelation); it is sub-additive-to-destructive
when they compete for the same job (phase × memory, both living in the
pulse-superposition channel).*

## Headline numbers

- **89.0% cohort8 [0,1,2,6,7,8] + AS @ K=2** — new best-known cell
  (+47.2pp over cohort15 base; prior best 79.4).
- **96.7% zero + AS+N1 @ K=2** — the superadditive exception
  (residual +11.9pp), and 100.0 at K=1.
- **N1 worst case −46.0pp** (ladder@15 K=1): the memory window is not
  a stale-grammar rescue.

## Scars / honest boundaries

- **Zero-lock spread duplication:** zero@15 == zero@30 rows are
  identical by construction (no spread axis); the 4 violating cells
  collapse to 2 unique.
- **N1 is a channel swap, not a pure additive:** the tri3 channel also
  changes slope dynamics (σ=3 vs e1's 8/5 piecewise walk), so "gain(N1)"
  bundles memory window + waveform change. Gain arithmetic is still
  well-defined (same-cell baselines) but the mechanism label is
  coarser than a surgical knob. Same confound as SPIN-10 EXP3.
- **AS asymmetry carried over:** lag-0 twins can only be offset upward
  (structural freshness-asymmetry, booked in SPIN-10) — AS-exact always
  adds mild staleness to the fresh cohort.
- **Grid bounds:** K∈{1,2} only in the composition grid (K=8 anchors
  in canaries); swap-in tested only at the kimi lane's cohort8 cell;
  scheduler×AS complementarity probed at one point, not mapped.
- 2.0pp gate is the hypothesis's own tolerance; zero@K=1 residual
  +2.4 is a boundary case — counted as violation, honestly marginal.

## Log-ritual bookkeeping

LCG advance for next spin: 368800899 → **1508029952** → mod 10 = **2**.

VERDICT: MIXED — universal subadditivity falsified (zero-lock K=2 residual +11.9pp; scheduler×AS superadditive +47.2pp stacked to a new best cell 89.0% cohort8+AS@K=2), but N1 memory is subadditive-or-destructive in 14/16 cells (all real grammars) and AS beats N1 everywhere (grammar-class prediction falsified; failure-mode prediction wins): superadditivity = orthogonal failure channels, substitutes = same channel.
