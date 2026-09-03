# SPIN 10 — SPOKE: PHASE-SCHEDULING (promoted from N1/N2 + SPIN-5 chatter)

**Lane:** wheel_spin10_phase · **Date:** 2026-09-03 07:2x AKDT ·
**Files:** `spin10_phase_scheduling.py`, `spin10-output.txt` ·
Fabric: `inventors-derby/exp_glm1.run_fabric` for e1 reality; the novel
lane's canaried `run2` port for the tri3 channel (re-imported, not
re-ported — byte-identity re-proven below). Integer-only inside every
loop; floats only in display. Seeds {1, 7, 42, 1999, 20260902}, 4800
ticks, stress (delta=12, drift=6, pd=3), N=6 unless stated. Full run
~25 s, ~600 fabric runs.

**Test (as briefed):** promote phase-aware scheduling to a first-class
control knob. (1) even-offset sweep from the zero-grammar origin,
residency-per-event metric, and an is-evenly-spread-optimal check at
matched max offset; (2) transplant the schedule into the real grammars
(ladder / cohort 3+3 / kcoh5-fresh) at spread 15 and 30; (3) the money
question — do cross-tick memory (K, the N1 +31.7pp window at sigma=3)
and anti-sync phase offsets **compose** on one channel?

## Canaries (2/2 PASS first run — no numbers booked without them)

- **A — port byte-identity:** `run2` ≡ `run_fabric` full-dict on e1
  reality, 8/8 configs (2 modes × 2 lats × K∈{1,8}).
- **B — published-anchor replay: 33/33 exact.** Zero-lock K1/2/8 =
  77.3/50.0/69.0 with **events 8756/15133/9964 and debt
  187834/511660/195470 exact** (novel N2); even-d=1 = ladder(5)
  97.6/84.9/90.2 with events 2598/5773/4172 exact; ladder10/15/30,
  cohort15/30, kcoh5@15/30 (= spin5-pattern outlier@30), quart15,
  tri15, kcoh1@15 all within 0.0 of published means; N1 tri3 [0,10]
  anchor 13.9/39.4/41.9/45.6 exact. offset=0 rows byte-match the novel
  lane's baseline as required.

## EXP 1 — offset sweep + is evenly-spread optimal?

**1a. Even schedules `lats=[0,d,2d,3d,4d,5d]`** (zero-grammar origin,
mean of 5 seeds; RPE = true%-points per 100 events):

| d | K=1 % | K=2 % | K=8 % | ev@K1 | best RPE |
|---|---|---|---|---|---|
| 0 | 77.3 | 50.0 | 69.0 | 8756 | — |
| 1 | **97.6** | 84.9 | 90.2 | 2598 | K=1: **d=1** (3.8) |
| 2 | 93.5 | **89.7** | **90.8** | 3805 | K=2/K=8: **d=2** (2.1/2.6) |
| 3 | 71.5 | 60.0 | 70.7 | 5792 | |
| 6 | 26.8 | 28.9 | 14.0 | 14952 | |

New points beyond anchors: ladder10 K8 = 90.8 (K8's max on this grid,
edging d=1's 90.2); ladder30 K8 = **14.0** — at raw 2Δ, K=8 collapses
below K=2 (memory is anti-useful deep in the collapsed regime).

**1b. Matched max-offset grids (same worst-case staleness):**

- **M=5:** coh5 `[0,0,0,5,5,5]` = **99.0** (K=1) > even5 97.6 > pair5
  96.5 > out5 93.8. At K=2 the order flips: **even5 84.9** > pair5 81.5
  > coh5 77.1 > out5 61.7.
- **M=15:** kcoh5@15 74.1 > even15 71.5 > tri15 64.6 > quart15 62.6 >
  coh15 57.1 > kcoh1@15 47.3 (K=1); **even15 wins K=2** (60.0) and RPE.

**Answer: evenly-spread is NOT optimal — but nearly.** A 2-phase coarse
split (coh5) beats the 6-phase even schedule by 1.4pp at M=5 and kcoh5
beats even15 by 2.6pp at K=1; even spreading wins every K=2 comparison.
The optimal *phase count* is K-dependent (few phases for K=1, many for
K=2) — but the fine structure is worth 1–3pp while the **max-offset
budget M is worth 25pp+** (M=5 band 93.8–99.0 vs M=15 band 47.3–74.1).
The first-order law is the budget; the schedule inside the budget is
second-order.

## EXP 2 — transplant into real grammars (K∈{1,2}, Δ vs base)

Anti-sync variants: AS-min (one 1-tick offset per cohort), AS-exact
(full within-cohort decorrelation, spread preserved:
`[0,1,2,13,14,15]`), AS-shift (cohort tops kept, spread grows). Ladder
= control: all lats already distinct — it IS a phase schedule (step 3).

| grammar | K | base | AS-min | AS-exact | AS-shift |
|---|---|---|---|---|---|
| cohort15 | 1 | 57.1 | +0.5 | **+2.8** (59.9) | +1.0 |
| cohort15 | 2 | 41.8 | +8.0 | **+14.8** (56.6) | +6.5 |
| cohort30 | 1 | 49.3 | +1.6 | **+2.9** (52.1) | +2.5 |
| cohort30 | 2 | 33.3 | +1.1 | −0.1 | +1.1 |
| kcoh5@15 | 1 | 74.1 | +2.9 | **+5.2 (79.4 — new best @15)** | ≡exact |
| kcoh5@15 | 2 | 50.6 | +4.5 | **+16.0** (66.6) | ≡exact |
| kcoh5@30 | 1 | 53.2 | **+3.5** (56.6) | **−3.1** (50.1) | ≡exact |
| kcoh5@30 | 2 | 47.4 | +1.8 | +8.8 (56.2) | ≡exact |

**Answer: anti-sync helps good grammars too — it is not just a chatter
cure.** kcoh5@15 + AS-exact = **79.4% K=1, the best grammar ever
measured at spread 15** (beats zero-lock's 77.3 with 32% fewer events:
7679 vs 8756), and the K=2 gains are huge (+14.8, +16.0) — AS-exact
mostly cures the K=2-specific pulse-memory overlap that SPIN-5
convicted at the origin. Sequential references are FLAT (cohort15
56.8→57.0, cohort30 53.6→52.9, kcoh5@15 56.8→56.7): the gains are
interference-arm-specific — phase scheduling acts through the
superposition, not through staleness reduction. Boundary found:
kcoh5@30 AS-exact K=1 = **−3.1pp** — at large spread, decorrelating the
fresh cohort spends freshness (four twins moved 0→1..4) that costs more
than the sync cure buys; AS-min (one twin moved) is the safe dose
there. Phase scheduling has a **dose-response curve**, not a monotone
knob.

## EXP 3 — the money question: memory × anti-sync on tri3 (sigma=3)

**3a. The N1 window is phase-fragile (faithful 2-twin test,
lats=[0,10+d]):**

| lats | K=1 | K=8 | K8−K1 |
|---|---|---|---|
| [0,10] | 13.9 | 45.6 | **+31.7** (the N1 window) |
| [0,11] | 7.1 | 28.3 | +21.2 |
| [0,12] | 6.9 | 14.5 | +7.6 |
| [0,13] | 7.0 | 9.0 | +2.0 |
| [0,16] | 6.9 | 6.7 | −0.2 |

One tick of extra phase on the stale twin erases a third of the memory
window; four ticks erase it entirely. The +31.7pp is a property of ONE
phase configuration, not of the channel.

**3b. 6-twin family on tri3 (zero-lock + even offsets):**

| lats | K=1 | K=2 | K=4 | K=8 |
|---|---|---|---|---|
| even0 (zero-lock) | 81.0 | 51.5 | 69.5 | 66.6 |
| even1 | **100.0** | 96.7 | 95.8 | 96.5 |
| even2 | 48.1 | 47.9 | 48.6 | 50.8 |
| even3 | 25.5 | 27.5 | 10.6 | 12.4 |
| even6 | 6.7 | 11.4 | 5.5 | 5.6 |

Sequential refs: zero 100.0% @ 913 events; even1 90.9% @ 2317. The
phase cure transfers across channels (e1: 77.3→97.6; tri3:
81.0→100.0) — but at d=1 the interference arm merely TIES sequential
on residency at 3.4× the events.

**3c. Composition decomposition (6-twin baseline d=0,K=1 = 81.0;
pure-K gain = −14.4):** the K8−K1 gap per d reads **−14.4 / −3.5 /
+2.7 / −13.1 / −1.2** — phase scheduling does not add to the memory
term, it **flips the K-dial's sign** (K hurts at zero-lock, is neutral
at d=1, helps at d=2). Surplus over the additive prediction is
positive everywhere (+1.3 to +17.1pp) — but only because pure-K is
NEGATIVE at the chatter baseline: the phase cure removes K's pathology
rather than stacking K's gift. The best combined config (even1, K=1,
100.0%) uses **no memory at all**.

**Answer: they INTERFERE — substitutes, not complements.** Two
independent mechanisms, one channel: anti-sync and cross-tick memory
compete for the same job (keeping the pulse stream coherent). Phase
scheduling makes the memory window unnecessary; the memory window only
existed because synchrony pathology made K=1 collapse. Neither
mechanism's gain survives on top of the other's optimum.

## Unifying observation (booked, boundary unmeasured)

The decorrelation budget looks like **(max−min)·σ ≲ 2Δ**: e1 knee at
span 15 (1.6×15=24=2Δ, SPIN-5); tri3 even1 span 5 (3×5=15 ≤ 24:
perfect) vs even2 span 10 (3×10=30 > 24: collapsed to ~48%). The e1
origin dip is the σ·span=0 degenerate point. A single span-budget law
would unify the SPIN-4 knee, the N2 origin dip, and EXP3's even1/even2
cliff — proposed as the next spoke.

## Verdict: VALIDATED (as a first-class knob) / MIXED (composition)

- **Phase scheduling is validated as a control knob:** origin cure
  +20.3pp (77.3→97.6 at 1 tick), cross-channel transfer (tri3
  81.0→100.0), upgrades the best real grammar (+5.2 → 79.4 @15 K=1,
  +16.0 on kcoh5 K=2, +14.8 on cohort15 K=2), all with sequential
  controls flat (arm-specific mechanism).
- **Evenly-spread: near-optimal, not optimal.** Coarse 2-phase splits
  win at K=1 (99.0 vs 97.6), even-6-phase wins at K=2; phase-count
  optimum is K-dependent; the max-offset budget dominates the fine
  structure 25pp vs 1–3pp.
- **Composition (money question): FALSIFIED for additivity — the
  mechanisms are substitutes.** The N1 memory window is phase-fragile
  (+31.7 → −0.2 over 6 ticks of offset); phase scheduling flips the
  K-sign; the joint optimum uses K=1. Memory is the compensation of
  last resort when phase scheduling is unavailable.

## Headline numbers

1. **79.4% @ spread 15, K=1: `[0,1,2,3,4,15]`** — phase-scheduled
   kcoh5, best grammar ever at the knee, 32% cheaper in events than
   zero-lock.
2. **One tick of offset is worth +12pp at the origin but the budget is
   what matters:** M=5 band 93.8–99.0 vs M=15 band 47.3–74.1.
3. **+31.7pp → −0.2pp:** the N1 cross-tick memory window dissolves
   under 6 ticks of phase offset — memory and anti-sync are
   substitutes, one channel, one job.

## Scars / honest boundaries

- **Display scar:** RPE printed at integer rounding over a 0–4 range —
  orderings and argmax are exact; read magnitudes at 1 decimal (raw
  events columns carry the exact data).
- **Confound bounded, not eliminated:** AS-exact moves lag-0 twins to
   1..4 (decorrelation + mild staleness redistribution). The flat
   sequential refs (±0.2pp) bound the staleness channel, but "pure
   de-sync at zero staleness" is **impossible on this fabric** — lag-0
   twins can only be offset upward. Structural freshness-asymmetry,
   booked.
- **N-change:** the 6-twin tri3 family (3b/3c) changes N vs the N1
  anchor; the faithful 2-twin test is 3a and both are reported
  separately. Decomposition arithmetic is against the 6-twin baseline.
- **Grid bounds:** evenly-spread-optimality tested only at M∈{5,15},
  K∈{1,2}(+8 anchors); the tri3 span boundary (even1/even2 cliff) is
  bracketed (5 < b ≤ 10) but unmeasured.
- kcoh5@30 AS-exact K=1 (−3.1) is the single anti-sync regression
  found — dose matters at large spread; AS-min is the safe default.

## Log-ritual bookkeeping

LCG advance for next spin: 2035015474 → **368800899** → mod 10 = **9**.

VERDICT: VALIDATED-as-knob / substitutes-not-complements — phase scheduling is a first-class control knob (origin cure +20.3pp, cross-channel transfer to 100.0%, new best grammar 79.4@15, K=2 rescues up to +16.0pp, sequential-flat arm-specificity); evenly-spread near-optimal not optimal (2-phase wins K=1, budget M dominates fine structure); memory × anti-sync do NOT compose — the +31.7pp window is phase-fragile to −0.2pp and the joint optimum uses K=1: the mechanisms are substitutes competing for one job.
