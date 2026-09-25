# ROUND 4 — O4: Lag-compensation regime motion (closed loop vs static arms)

**Item:** O4 (RESEARCH-AGENDA.md §4; from S2/F19 — kimi #3 lag blade + REGIME-META
κ-detector). Branch `g3-kinduction`. Date: 2026-09-03.
Harness: `dev-rounds/o4_regime_motion.py` (extends kimi exp3 / e1.py lineage
line-for-line: same `LCG`, `reality`, same E1 loop, same 5 seeds; integer-only
throughout — per-mille by integer division). Output: `dev-rounds/o4-regime-motion-output.txt`.
Wall: ~2 min CPU.

## Hypothesis (pre-registered)

Closed loop — lag discovery (480-tick first-difference blade) → per-twin lag
compensation → REGIME-META κ-detector → mode dial (sequential ↔ interference) —
beats every static arm under mid-stream regime shifts (calm→conflict→bursty per
charter §3.2), because compensation converts conflict→calm and the dial must
follow (kimi F19: compensated sequential 1000‰ vs compensated interference
984‰; ledger doctrine applies to the NEW regime).

**Decision rule (pre-registered):** adaptive ≥ max(static arms) − 1pp
post-compensation %w AND debt ≤ 60% of best static ⇒ promote to E4
architecture, pre-load §3.2 demo QTORCH arm; else book the boundary (detector
lag vs regime dwell) with numbers.

## Grid

Task shape (charter §3.2, shift times fixed, unknown to controllers), 4800
ticks: **calm** [0,1600) Δ6/drift3/lat5 → **conflict** [1600,3200)
Δ12/drift6/lat10 → **bursty** [3200,4800) Δ6/drift3/lat10 + 1-in-4 ±45 ADC
glitches (REGIME-META E4.E shape; glitch LCG `seed^0x5A5A`, deterministic).

Arms (identical budget — same ticks, same triggers, same pulse law; 7 × 5
seeds = 35 real runs):

| Arm | Mode | Compensation |
|---|---|---|
| seq-raw / int-raw | fixed | none (L̂=0) |
| seq-comp-fix / int-comp-fix | fixed | L̂=10 assumed forever (stress doctrine) |
| seq-comp-oracle / int-comp-oracle | fixed | L̂ = true per-segment lag (upper bound) |
| adaptive | κ-detector dial (CALM→seq/Δ6, CONFLICT→int/K4/Δ12) | 480-tick blade re-run every 480 ticks, live |

Compensation is **live-realizable**: the fresh twin (T1) is delayed by L̂ to
align with the stale twin (T2) — no future peeking. Residency judged
**post-compensation** on the aligned pair (per the rule's own wording).
κ-detector exactly per REGIME-META.md constants (DEBT_CLIMB 120, CANCEL 4,
κ 280‰, entry 2, exit 5). The live blade uses sign-clipped first differences
(glitches are common-mode same-tick spikes that would seat a false L=0 peak
in the raw-product blade; sign-clipping keeps them at unit weight).

## Canary table

| Canary | Check | Result |
|---|---|---|
| A (byte-identity, kimi F19 anchors) | `exp3_lag_blade.py` verbatim replay: lag blade 3/5/7/10/15 → exact 5/5; seq raw 512‰/48994/61, seq comp 1000‰/8428/12, int raw 830‰/34995/39, **int comp 984‰/17700/28** | **PASS** (all four anchor rows exact) |
| B (self-canary, mislabeled arm) | 'adaptive' run with inverted mode dial must be caught by the dial-doctrine checker (sequential must own the calm segment): calm-seq 46 vs calm-int 1554 ticks | **CAUGHT** |

## Results (5 seeds, mean per-mille / mean debt / max maxErr)

| Arm | pm | debt | maxErr | seg pm calm/conflict/bursty |
|---|---|---|---|---|
| seq-raw | 266‰ | 87,152 | 61 | 576/191/31 |
| int-raw | 371‰ | 105,027 | 54 | 289/821/4 |
| seq-comp-fix | 636‰ | 59,686 | 53 | 574/1000/335 |
| int-comp-fix | 422‰ | 81,193 | 50 | 281/982/3 |
| **seq-comp-oracle** (best static) | **778‰** | **54,616** | 45 | 1000/1000/335 |
| int-comp-oracle | 545‰ | 80,320 | 50 | 650/983/3 |
| **adaptive** | **932‰** | 57,136 | 53 | 871/995/**929** |

Adaptive per-seed: [932, 935, 932, 932, 929]‰ — tight. Lag blade live: exact
5/5/5 in calm, 10/10/10 in conflict, **9/9/9 in bursty** (true 10 — off-by-one
underseat under glitch noise, all seeds). Detector telemetry (all seeds):
conflict entry lag **90 ticks** after the shift (debt-climb signal needs the
stale-vs-fresh misalignment to build); calm exit at/before the bursty edge
(lag 0); bursty conflict re-entry ~6–8 ticks after edge (glitch debt spikes),
held to 11 interference ticks by hysteresis. Mode switches: 6 per run.

## Decision rule, applied

- %w: adaptive 932‰ ≥ best static 778‰ − 10‰ ⇒ **PASS** (+154‰).
- Debt: adaptive 57,136 ≤ 0.60 × 54,616 = 32,770? ⇒ **FAIL** (104.6% of best
  static's debt — bursts must be answered tick-for-tick at Δ6; the dial saves
  %w, not spend).

**VERDICT: BOOK BOUNDARY — not promoted to E4 architecture.** Both conditions
were required; debt fails by 1.75×.

## The boundary, with numbers (and a scar)

1. **Detector lag vs regime dwell:** conflict entry takes **90 ticks** (5.6% of
   the 1600-tick dwell lost while the detector's debt-climb window fills) —
   the REGIME-META E4.B prediction of a 2–4-tick switch is **falsified** at
   these thresholds; the debt-climb signal (recent vs older 8-tick sums,
   threshold 120) needs the regime to hurt for ~11 window-fills before firing.
   Calm-exit and bursty re-entry are fast (0 and ~7 ticks). The dial is
   half-fast: pain is detected slowly, relief quickly.

2. **The %w win is real but knife-edge (booking scar).** Adaptive's headline
   932‰ rides its bursty-segment 929‰ — and that rides the live blade's
   off-by-one underseat (L̂=9, true 10). Forced-lag probe (sequential, Δ6,
   bursty segment, seed 20260902): L̂=8→335‰, **9→994‰**, 10→336‰, 11→340‰.
   The off-by-one *decorrelates the synchronized glitch triggers* the exactly-
   aligned pair produces (with L̂=true, both twins glitch identically and
   sequential chases ±45 in lockstep; with L̂=true−1 the triggers split and
   the impulse snaps land off-glitch). Exact compensation is *worse* than
   accidental near-compensation under common-mode bursts: **the aligned frame
   is glitch-coherent, and coherence is the enemy of the sequential arm.**
   Mechanism label: measured sensitivity, hypothesis-level explanation
   (decorrelation) — not microtrace-verified.
   The adaptive arm did not earn 932‰ by the pre-registered mechanism (dial
   follows compensation); the dial fired 6 times/run and held interference for
   ~28 ticks total. The lag compensator (blade + per-twin delay) is doing
   nearly all the work.

3. **Debt is irreducible under bursts at Δ6.** Every ±45 glitch must be
   answered within a tick at trigger threshold 6, so no arm — static or
   adaptive — gets bursty debt below ~⅓ of its total; compensation cuts
   total run debt 87,152→57,136 (−34%; F19's stress-only halving replicates
   inside the conflict segment) but burst
   debt is a floor, not a lag symptom.

## Bookings

- F19 doctrine CONFIRMED in-run: compensation converts conflict→calm
  (comp-fix arms: 191‰→1000‰ in the conflict segment) and the compensated
  optimal arm is sequential (comp seq > comp int in every segment, every seed).
  The mode dial the κ-detector actually wants is "sequential almost always,
  once lag is repaid" — E4's dial as specified (interference under conflict)
  is *behind* the compensation, not ahead of it.
- E4 architecture NOT promoted. The §3.2 demo QTORCH arm should not pre-load
  the κ-dial as its spine; pre-load **lag blade + compensator + sequential**,
  and treat the κ-detector as a slow backstop (90-tick entry) rather than the
  regime organ. Follow-up candidate (O4b): detector retuned on *misalignment*
  (blade residual) instead of debt-climb — the blade seats in ≤480 ticks and
  its underseat predicted the bursty regime 480 ticks before the κ-detector
  moved.
- Knife-edge scar logged: near-miss lag (L̂=true−1) beats exact lag under
  common-mode bursts for the sequential arm (994 vs 336‰). Robustness of any
  promoted arm must be probed at L̂±1 (this round's probe is the template).

## Headline number

**Adaptive closed loop 932‰ vs best static 778‰ (+154‰, %w gate PASSED) —
but debt 57,136 > 60% gate (32,770): BOUNDARY BOOKED; detector lag 90 ticks
vs 1600-tick dwell, and the %w win rides a knife-edge off-by-one lag (9→994‰,
10→336‰ in the bursty segment).**
