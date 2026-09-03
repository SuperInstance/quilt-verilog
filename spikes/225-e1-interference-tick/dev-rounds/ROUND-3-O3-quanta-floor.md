# ROUND 3 — O3: Quanta floor on RTL alphabets (K × cap interaction)

**Item:** O3 (RESEARCH-AGENDA.md §4, from F23 / opencode #4). Branch `g3-kinduction`.
**Date:** 2026-09-03. Harness: `o3_quanta_floor.py` (reuses `e1.py` LCG/reality
primitives line-for-line; seed-parameterized `run` with magnitude cap;
integer-only). Output: `o3-quanta-floor-output.txt`. Wall: ~40 s CPU (well
under budget).

## Hypothesis (pre-registered)

1. The 3-bit cap (±5, 99% of interference win at K=4 stress) holds at K=2 too.
2. The Z₃ debt inversion (sign-only: residency win, debt loss vs impulse)
   persists everywhere.

## Grid

cap ∈ {1,2,3,5,7,11,∞} × K ∈ {1,2,3,4} × regimes {calm (Δ6/d3/λ5), stress
(Δ12/d6/λ10)} × seeds {1,7,42,1999,20260902}, 4800 ticks, pulse_div=3.
Z₃ sign-only arm = cap=1, reported at K∈{2,4}. 320 runs, all real.

## Canaries

| Canary | Check | Result |
|---|---|---|
| A (byte-identity) | 4 cells (calm/stress × impulse/interference) vs `e1.run` at seed 20260902: events, debt, constructive, cancel, chatter, maxErr all exact; pm ±1‰ (floor-‰ vs e1's float round) | **PASS** (4/4 identical) |
| A2 (F23 anchors) | stress K=4 5-seed interference INF 830‰/34995 — **exact**; every cap row matches F23's table to the digit (±5: 824/35169; ±1: 575/53907; ±7: 834/34822; ±11: 830/35039) | **PASS** |
| B (self-canary) | deliberately mislabeled cap=5-as-INF arm must be caught (stats must differ from true INF): seeds 20260902 and 7 both CAUGHT | **PASS** |

**Booking scar found:** F23's *impulse* anchor (519‰/48397) reproduces only at
seed 20260902 — it was a single-seed number, while F23's interference rows are
exact 5-seed means. Discrepancy resolved; all F23 interference numbers stand.

## Verdict (per pre-registered decision rule)

**PARTIAL-REFUTE / KNEE RELOCATED — adopt 4-bit cap (±7) as the ESP32/.qm port default.**

- The rule said: cap=±5 retains ≥99% at K=2 ⇒ adopt 3-bit. **It does not**:
  K=2 stress retention is **97.5%** (pm 903 vs INF 913; the uncapped win is
  401‰, ±5 leaves 391‰). K=2 calm passes (100.6%). Strict reading: gate failed
  ⇒ "adopt the measured knee."
- The measured knee at K=2 is **±7** (stress 100.5%). **Cap=±7 (4-bit alphabet)
  retains ≥99% at every K×regime cell** — min 99.2% (K=1 calm) / 99.3% (K=1
  stress) — while ±5 does not (also 97.5% at K=1 calm, 88.7% at K=1 stress,
  98.1% at K=4 stress). The interaction of short tails × coarse alphabet is
  real: at K=1 the pulse never decays before dying, so magnitude truncation
  costs more; at K=2–3 the decay chain softens the cap.
- **Z₃ (cap=1): debt inversion persists everywhere** (all sampled K×regime:
  debt strictly above impulse; at K=2 it loses residency *and* debt). Z₃ stays
  sampling gear (dice), not correction gear. Below ~2 bits the trade stays
  inverted: residency (where kept) is bought with ledger mass and event count.

## Headline

> **±7 (4 bits) is the floor: the only cap retaining ≥99% of the uncapped
> interference win at every K∈{1..4} × regime; ±5 fails at K=2 stress
> (97.5%).** Z₃ debt inversion persists at 8/8 sampled cells (never below
> impulse).

Retention of cap=±5 (uncapped win = 100%): K1 calm 97.5 / stress 88.7 ·
K2 calm 100.6 / stress 97.5 · K3 calm 101.4 / stress 99.1 · K4 calm 103.7 /
stress 98.1. Retention of cap=±7: ≥99.2% in all 8 cells.

## Scars / limitations

- F23's impulse anchor was single-seed (20260902) — the 5-seed impulse
  baseline here is 512‰/48994, not 519‰/48397. Doesn't change any verdict
  (retention uses matched-seed baselines).
- Regime params reuse e1.py's two hardcoded presets; no mid-stream shifts
  (that's O4's lane).
- Verilator/q_cell_core.v rung not exercised (cosim spike not alive; agenda
  listed it as optional).
- Retention >100% cells are seed-mean noise on a saturating curve (capped pm
  within ±9‰ of INF); the knee read is insensitive to this.
