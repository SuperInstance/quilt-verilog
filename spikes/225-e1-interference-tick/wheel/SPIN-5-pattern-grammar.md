# SPIN 5 — SPOKE: PATTERN-GRAMMAR (the second-order dial proposed by SPIN-4)

**Lane:** wheel_spin5_pattern_grammar · **Date:** 2026-09-03 ~07:05 AKDT ·
**Files:** `spin5_pattern_grammar.py`, `spin5-output.txt` · Fabric:
`inventors-derby/exp_glm1.run_fabric` (E1 contract items pinned: fdiv decay,
64-bit LCG, FIFO oldest-first expiry, snapshot decay). Integer-only inside
the loop; floats only in display statistics (means, interpolated crossings,
Pearson r). Full run: 8.3 s, ~615 fabric runs.

## Hypothesis space (as briefed)

Pattern is a real **second-order dial** on top of the first-order spread
law. At spread≈15 (near the 2Δ=24 knee) the multiset grammar — how the
spread is distributed across twins — changes true-residency; the U-shaped
origin anomaly (spread=0 worse than spread=5) is synchronized-duplicate
chatter.

Sharpened testable statements:

- **H1 (knee):** the ladder knee localizes to ±2 and tracks the
  slope-adjusted 2Δ crossing — reality slope 8/5 per tick × spread = 24 →
  spread ≈ 15 — not the raw 2Δ = 24.
- **H2 (grammar dial):** at fixed total spread (15 and 30) the grammar
  moves true-residency ≥ 10pp, ordered by the majority axis (largest
  coherent cohort: zero 6+0, outlier 5+1, quart 4+2, cohort 3+3, tri
  2+2+2, ladder graded) — SPIN-4's cohort-majority proposal.
- **H3 (chatter):** spread=0's anomaly is synchronized-duplicate chatter —
  all twins read the same residual, all fire the same tick (Spin-1's gap=1
  refire at cohort scale), the arm shoves ~6×(e//3) ≈ 2e, overshoots onto
  its own echo and re-fires next tick; grammar losses correlate with
  same-tick correlated corrections.

## Operationalization

N=6, interference arm, 4800 ticks, stress params (delta=12, drift=6, pd=3),
seeds {1, 7, 42, 1999, 20260902}, K ∈ {1,2}. Grammars at nominal spread s
(max−min latency):

| grammar | lats at s=15 | at s=30 | structure |
|---|---|---|---|
| ladder | [0,3,6,9,12,15] | [0,6,12,18,24,30] | graded (SPIN-4 continuity) |
| cohort | [0,0,0,15,15,15] | [0,0,0,30,30,30] | half-half 3+3 (SPIN-4 cohort) |
| tri | [0,0,7,7,15,15] | [0,0,15,15,30,30] | tripartite 2+2+2 (the literal ((0,0),(15,15),(30,30)) reading of the brief) |
| quart | [0,0,0,0,15,15] | [0,0,0,0,30,30] | 4 fresh + 2 stale |
| outlier | [0,0,0,0,0,15] | [0,0,0,0,0,30] | single stale twin (5+1) |
| paired | [0,15,0,15,0,15] | [0,30,0,30,0,30] | duplicate pairs |
| zero | [0]×6 | [0]×6 | synchronized chatter mode (ignores s) |

The brief's "cohort splits" notation admits two readings; **both are
covered** (cohort = half-half, tri = 2+2+2). "paired" turned out to be the
same *multiset* as cohort — see Canary C. Chatter instrumentation: per-tick
correction-event logs from the emissions ledger — multi-sensor ticks,
all-6 ticks, same-sensor gap-1 refires (Spin-1's metric, generalized),
synchronized refires (firing sets of consecutive ticks overlapping ≥2).

## Self-canaries (all four PASS — mandatory gate)

1. **A — spread=0 byte-identity:** all 7 grammar codepaths byte-identical
   at s=0, K ∈ {1,2} (12/12 comparisons, full resid+cflags traces). PASS.
2. **B — SPIN-4 replay:** ladder spread=15 K=1 → per-seed permille
   709/713/721/714/717 EXACT; events 5791.6 (pub 5792), debt 106378 exact,
   cancels 4.2 (pub "4" was display-rounded). PASS.
3. **C — order-invariance (added):** paired ≡ cohort **byte-identical in
   both arms**, s ∈ {15,30}, K ∈ {1,2}, all seeds (30/30). PASS — and
   promoted to a finding: the interference correction is a pure function
   of the error *multiset* (net = Σ pulses; decay order-free), and
   sequential trig[0] resolves to fresh-else-stale for both orders.
4. **D — zero-lock ignores nominal spread:** zero@15 ≡ zero@30
   byte-identical (K ∈ {1,2}, 5 seeds). PASS.

## Results

### EXP 1 — densified knee (ladder, N=6, mean of 5 seeds)

| spread | 10 | 12 | 14 | 15 | 16 | 18 | 20 | 22 | 24 |
|---|---|---|---|---|---|---|---|---|---|
| K=1 true% | 93.5 | **95.0** | 84.4 | 71.5 | 63.5 | 53.2 | 49.2 | 43.0 | 31.7 |
| K=2 true% | 89.7 | 84.8 | 72.3 | 60.0 | 59.6 | 53.5 | 47.7 | 40.7 | 36.3 |
| seq K=1 % | 85.0 | 76.9 | 65.9 | 62.6 | 60.7 | 64.3 | 55.8 | 51.2 | 52.9 |

- **Onset:** steepest per-spread-unit drop for BOTH K sits on **[14,15]**
  (K=1: 84.4→71.5 = 12.9pp/unit; K=2: 12.2pp/unit) with [15,16] second.
  The collapse *begins* at 15±1 — the slope-adjusted 2Δ crossing — not at
  raw 2Δ=24, where the arm is already deep in collapse (31.7%).
- **Midpoint:** 50%-crossing at spread ≈ 19.6 (K=1) / 19.2 (K=2) — the
  transition is a ~5-6-spread-wide band, not a sharp knee.
- Sequential never crosses 50% on this grid (52.9% at 24) — the
  interference arm's dive below the sequential floor is a genuine arm
  property, confirming SPIN-4's coarse-grid finding.
- Fine structure: consistent local bump at 12 (95.0 vs 93.5 at 10; every
  seed higher) — unexplained, booked open.

### EXP 2 — grammar sweep at fixed total spread (interference, mean %)

| grammar | s=15 K=1 | s=15 K=2 | s=30 K=1 | s=30 K=2 | seq s=15 | seq s=30 |
|---|---|---|---|---|---|---|
| zero 6+0 | **77.3** | 50.0 | **77.3** | 50.0 | **100.0** | **100.0** |
| outlier 5+1 | 74.1 | 50.6 | 53.2 | 47.4 | 56.8 | 53.6 |
| quart 4+2 | 62.6 | 56.1 | 45.4 | **53.4** | 56.8 | 53.6 |
| cohort 3+3 | 57.1 | 41.8 | 49.3 | 33.3 | 56.8 | 53.6 |
| tri 2+2+2 | 64.6 | 59.4 | 30.2 | 30.2 | 65.3 | 51.0 |
| ladder graded | 71.5 | **60.0** | 26.8 | 28.9 | 62.6 | 57.6 |
| paired (=cohort) | 57.1 | 41.8 | 49.3 | 33.3 | 56.8 | 53.6 |

- **Grammar is a big second-order dial: 20.1pp at s=15 K=1, 50.5pp at
  s=30 K=1** (zero 77.3 vs ladder 26.8) — the s=30 dial alone is double
  the entire ladder spread-collapse from 10→24.
- **Majority axis: only the top end orders.** zero > outlier at both
  spreads and K — a coherent supermajority protects. But quart (4+2)
  UNDERperforms cohort (3+3) at s=30 K=1 (45.4 vs 49.3), the graded ladder
  breaks the axis at s=15 (3rd, above tri/quart/cohort), and **K flips
  orderings**: zero falls 77.3→50.0 (best to bottom-half) while quart@30
  RISES 45.4→53.4 (the only grammar that improves with K). No single
  monotone majority law survives.
- **Sequential is multiplicity-blind:** cohort ≡ quart ≡ outlier ≡ paired
  EXACTLY in the sequential arm (56.8% / 4228 events / 103160 debt at
  s=15; 53.6/4500/198066 at s=30) — sequential sees only the ordered set
  of distinct latencies (fresh-else-stale(,s/2)-else…). Grammar acts on
  interference through duplicate *mass*; on sequential only through the
  distinct-lag set.
- **Isolated chatter cost:** at zero-lock sequential is perfect (100.0%,
  527 events) while interference spends 8756 events for 77.3% — **pure
  interference self-harm with zero staleness = 22.7pp (K=1), 50.0pp (K=2)**
  — first clean isolation of the arm's self-injury term.
- Sub-finding: interference can BEAT sequential at fixed grammar —
  outlier@15: 74.1% vs 56.8% (+17.3pp): 5 fresh twins each shoving e//3
  (≈1.67e total, gentle) beats hard impulse snapping. "Interference is
  fragile" is grammar-conditional.

### EXP 3 — chatter mechanism

**Named-mode stats (s=15, 5-seed means):** zero K=1: **100% of event-ticks
are all-6 synchronized fires** (1459/1459), 69.4% of events are same-sensor
gap-1 refires, sshare 694‰. cohort K=1: also 100% multi-sensor (fires are
3+3) but refire share only 18‰ — disagreement, not echo. ladder K=1:
multi-share 350‰.

**Mechanism excerpt (zero-lock K=1, seed 1, t=1200-1226):** all 6 twins
fire every tick, sumPM alternates sign (+114, −108, +102, −90, …) ≈ ±2×
the trigger error, and the oscillation decays 56→17 then stops when the
residual finally drops inside Δ. The arm overshoots onto its own echo and
re-fires on it — **exactly the hypothesized synchronized-duplicate
chatter**, with Spin-1's gap=1 refire generalized: gap-1 refires present
in **140/140** grammar runs (Spin-1: 20/20).

**Echo sign analysis (zero K=1):** consecutive synchronized fires flip
sign **5058/5066 = 99.84%** across seeds — it is an overshoot-echo
oscillation, not same-residual grinding. At K=2 the previous tick's
half-decayed pulses stack onto the fresh overshoot → zero-lock halves
(77.3→50.0): the U-shape at the origin is pulse-memory overlap, not
staleness.

**Does chatter predict grammar losses? Only weakly.** Pearson over the 28
grammar×spread×K configs: r(true%, synchronized-refire share) = **−0.51**
pooled (−0.40 within s=30, −0.35 within s=15); multi-sensor share −0.33;
gap-1 refire share −0.33. Moderate at best — and decisively: **the most
synchronized grammar (zero-lock) is the BEST grammar at K=1.** Correlated
corrections are not per se the loss; the loss driver at real spread is
cross-cohort staleness disagreement (cohort@15: 57.1% with zero refires
but 3v3 conflict; ladder@30: 26.8%).

## Verdict: MIXED

- **E1 knee: VALIDATED.** Collapse onset at **spread 14–16** (steepest
  drop 84.4→71.5pp over [14,15], 12.9pp/unit) — it tracks the
  slope-adjusted 2Δ=24 crossing at spread=15, NOT the raw 2Δ=24 (where the
  arm already sits at 31.7%). 50%-midpoint ≈ 19.6; sequential never
  crosses 50 by spread 24.
- **E2 grammar dial: VALIDATED as a dial, majority law MIXED.** 18–50pp
  swings at fixed spread; supermajority protects (zero/outlier on top) but
  the middle scrambles and K flips the orderings (zero 77.3→50.0;
  quart@30 45.4→53.4 rising with K). Cohort-majority as a single monotone
  law: FALSIFIED in detail.
- **E3 chatter: mechanism VALIDATED, generalization MIXED.** Zero-lock is
  exactly synchronized-duplicate chatter (1000‰ synchronized fires,
  99.84% alternating-sign echo, 140/140 gap-1 runs) and explains the
  U-shaped origin anomaly — but synchronized-correction share predicts
  cross-grammar losses only at r ≈ −0.5, and the maximally synchronized
  grammar is the best one at K=1. Chatter is the origin anomaly; stale
  cross-cohort disagreement is the grammar-loss driver.

## Headline numbers

1. **Knee:** steepest ladder drop 84.4→71.5% at spread 14→15 (onset
   15±1 = slope-adjusted 2Δ crossing; 50%-crossing 19.6; 31.7% already at
   raw 2Δ=24).
2. **Dial:** fixed spread=30, K=1: zero 77.3% … ladder 26.8% = **50.5pp
   grammar dial** — twice the entire first-order spread-collapse.
3. **Chatter:** zero-lock K=1: 1459/1459 event-ticks fully synchronized,
   99.84% sign-flip echo, isolated cost **22.7pp vs sequential's 100.0%**
   (50.0pp at K=2); but r(losses, sync share) = −0.51 — chatter explains
   the origin, not the grammar losses.

## Scars / honest boundaries

- **Instrument scar (booked):** Canary B first-run FAIL was *my* tolerance
  bug — spin4's published "canc 4" was display-rounded (true mean 4.2).
  Replay tolerances must be written against the publishing format's
  rounding, not against exact equality with a rounded number.
- **Hypothesis-space scar:** the brief's paired-duplicates-vs-cohort
  contrast is vacuous on this fabric — same multiset, byte-identical in
  both arms (Canary C, 30/30). Grammar naming must be done on multiset
  equivalence classes; order never matters in either arm of this fabric.
- The spread=12 bump (95.0 > 93.5 at 10, all 5 seeds) is consistent but
  unexplained — possible interaction of ladder rounding with reality()'s
  3-4-5 phase structure; open.
- Pearson r's are descriptive on 28 config means (5-seed means, per-seed
  spread ±1–4‰ — means stable, n small). No inferential claim.
- Sequential knee "never crosses 50" is bounded by the grid (≤24);
  spin4's spread=30 point (57.6%) suggests it flattens ~52–58 rather than
  collapses.

## New spoke proposed: YES — GRAMMAR-LAW (stale-mass × coherence)

The data point past chatter: losses track **cross-cohort staleness
disagreement weighted by duplicate mass**, not synchronization. Next
spoke: parameterize grammar by two integers — stale-mass fraction (share
of twins at lag where (8/5)·lag ≳ Δ) and max coherent-cohort size — and
test the 2-parameter law against a fresh grammar grid (asymmetric splits
[0,0,0,0,3,15], staggered-stale [0,0,0,10,20,30], weighted duplicates at
fixed spread), including the K-interaction (why quart@30 rises with K
while everything else falls). Either a predictive law pins or the
2-parameter reduction falsifies.

## Log-ritual bookkeeping

LCG advance for next spin: 1147902781 → **2035015474** → mod 10 = **4**
(TOPOLOGY). This spin was dispatched by SPIN-4's proposal (not the LCG
pick); the wheel ledger resumes LCG selection at the next cycle.

VERDICT: MIXED — knee onset at spread 14–16 (slope-adjusted 2Δ, not raw 24); grammar is a real 18–50pp second-order dial but no monotone majority law (K flips orderings); zero-lock chatter mechanism directly observed (99.84% sign-flip echo, 22.7pp isolated cost) yet predicts cross-grammar losses only r≈−0.5 — staleness disagreement, not synchronization, drives grammar losses.
