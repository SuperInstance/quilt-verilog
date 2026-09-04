# Round 4b — O4: regime motion, independent replication (equal-blade control)

- **Date:** 2026-09-04 ~07:4x AKDT · lane `dev_o4_regime_motion` (zai/glm-5.3)
- **Item:** RESEARCH-AGENDA §O4 — closed loop: lag discovery (480-tick blade, kimi #3/F19) → per-twin lag compensation → REGIME-META κ-detector state machine → mode dial, vs static arms under mid-stream regime shifts.
- **Script:** `o4_regime_motion_r4b.py` · raw output: `o4-regime-motion-r4b-output.txt`

## Hypothesis (pre-registered in script header BEFORE any stress run)

The closed loop beats every static arm because compensation converts conflict→calm
and the dial must follow (kimi #3: compensated sequential 1000‰ vs compensated
interference 984‰).

**Pre-registered decision rule:** with W(X) = mean settle-‰ over 5 seeds
(1/7/42/1999/20260902) under a UNIFORM post-compensation criterion |e|≤12 on both
twin views (canary-comparable; arm trigger deltas stay arm-owned), and D(X) = mean
ledger debt: PROMOTE iff W(adaptive) ≥ max(static W) − 10‰ AND D(adaptive) ≤
0.60·min(static D). Else book the boundary (detector lag vs regime dwell, with
numbers).

## Setup

Environment per charter §3.2 task shape, identical stream across arms per seed
(separate env LCG `seed^0x5EED`):

| ticks | segment | lat2 | drift | extras |
|---|---|---|---|---|
| 0–1599 | CALM | 5 | 3 | — |
| 1600–3199 | CONFLICT | 10 | 6 | — |
| 3200–4799 | BURSTY | 5 | 3 | 1-tick twin glitches, p=1/4, mag ±(28+e) |

Arms: **A** adaptive (blade refreshed every 480 ticks on raw twin diffs → laghat
compensation → REGIME-META detector, thresholds 120/4/280‰, entry 2 hits, exit 5
calm ticks, refractory 10/20 → dial CALM=sequential δ6 / CONFLICT=interference
δ12/K4/÷3); **B/C/D** static interference / sequential-δ12 / impulse-δ6, each raw
and compensated (compensated variants = the E compensated-static controls: same
blade, frozen dial).

## Canary (gate) — PASS

kimi #3 exp3 replay cells reproduced by importing the verbatim source:
blade **5/5 exact** (lags 3/5/7/10/15); raw seq 512‰, comp seq **1000‰**, raw int
830‰, comp int **984‰** — byte-exact on the canary cells. Double-run determinism
confirmed (second run diff-identical).

## Raw numbers (mean over 5 seeds; segments calm/conflict/bursty in ‰)

| arm | total ‰ | calm | conflict | bursty | debt | maxErr |
|---|---|---|---|---|---|---|
| A adaptive (blade+comp+κ-detector+dial) | **978** | 988 | 995 | 950 | 79,619 | 67 |
| B interference raw | 627 | 972 | 821 | 89 | 100,172 | 57 |
| B interference comp (E) | 683 | 980 | 980 | 88 | 93,595 | 79 |
| C sequential δ12 raw | 821 | 981 | 502 | 981 | 89,112 | 61 |
| C sequential δ12 comp (E) | **988** | 990 | 996 | 978 | **75,001** | 69 |
| D impulse δ6 raw | 717 | 981 | 191 | 981 | 101,156 | 61 |
| D impulse δ6 comp (E) | **988** | 990 | 996 | 978 | 79,071 | 67 |

Per-seed totals: A = [976, 981, 983, 971, 980]; C-comp = [988×5].
Per-seed debt: A = [79701, 79995, 79644, 80117, 78641]; C-comp ≈ 74–76k.

## Detector reaction lag vs dwell (the booked boundary, measured)

- Conflict onset t=1600 → confirmed flip to CONFLICT at **t=1683/1684 (lag ≈ 83–84
  ticks)** vs segment dwell 1600 (**5.2% of dwell**). Lag is dominated by the
  debt-climb window (16-tick halves + 120 threshold must charge from sequential
  chatter) — κ/cancel signals are unavailable in sequential mode, so entry rides
  debt-climb alone.
- Exit flicker: every confirmed entry into CONFLICT flipped back to CALM **~11
  ticks later** (exit 5 + refractory remainder), because compensation has already
  converted the conflict into calm — the detector's own hypothesis says so, and it
  obeys: the dial cannot hold CONFLICT in a compensated loop.
- **Spurious entries in CALM:** all 5 seeds flip 0→1 at t≈243/483/724 — exactly
  reality()'s period-240 walk corners (slope changes masquerade as debt climbing),
  each costing ~11 ticks of interference mode. Walk-corner aliasing is a real
  detector scar, not noise.
- Bursty onset t=3200 → flip at **3204–3207 (lag 4–7 ticks)**, exit ~13–15 ticks:
  glitch storms trip debt-climb fast; adaptive pays 950 vs C-comp's 978 in that
  segment from mode oscillation.

## Verdict per pre-registered decision rule — **BOOK-BOUNDARY (REFUTED as stated)**

- Gate 1 (W): 978 ≥ 988 − 10 = 978 → PASS, but exactly on the line (no margin).
- Gate 2 (debt): 79,619 ≤ 0.60 × 75,001 = 45,000 → **FAIL by 1.77×**.

The closed loop does NOT beat every static arm: **compensated-static sequential
(C/E, frozen dial) dominates adaptive on both axes** (988 vs 978 ‰; 75.0k vs
79.6k debt). The causal agent in the kimi #3 doctrine is the **lag blade +
compensation, not the dial**: once latency is compensated, the conflict regime
disappears from the loop's point of view (conflict segment: C-comp 996‰ ≥
adaptive's own 995‰), so REGIME-META's conflict mode has nothing to detect — the
detector correctly reports calm, and every flip it does make (walk corners, glitch
storms) is a cost, not a win. "The dial must follow" is true in the trivial
direction: it must stay still.

**Booked boundary:** detector entry lag 83–84 ticks (5.2% of a 1600-tick dwell)
would be affordable; the unaffordable part is *specificity* — with compensation
active, the conflict signal is gone and the residual signal (walk-corner debt
aliases at ~240-tick intervals, bursty glitch storms at 4–7 ticks) is 100%
false-positive. κ-detector-on-top-of-compensation is dominated. E4's architecture
should be **blade+compensation with a frozen sequential dial** (plus T2's N≥6
contention sort from round 3); the κ-detector belongs *upstream of* compensation
(or on the raw channel) if it is kept at all. No QTORCH arm pre-load — the §3.2
demo's adaptive-dial premise is not supported by these runs.

## Scars / lessons

1. **First full run was garbage because env glitches fired in all three segments**
   and comp-static arms never ran the blade (laghat≡0, "comp"≡raw, 67‰ rows).
   Pre-registered decision rule saved us from reporting a fabricated boundary —
   the absurd numbers (statics at 67–717 vs canary 984–1000) failed the smell test
   before any verdict was drawn. Always canary-gate per-arm, not just per-script.
2. **Gate-1 edge pass (978 ≥ 978) is not a win.** The −1pp tolerance was meant for
   detector lag cost; it instead absorbed the detector's *own* self-harm. Verdict
   hinges on gate 2, and honestly on the raw table: C-comp beats A outright.
3. **Dominance analysis beats threshold rules for architecture calls.** The static
   Pareto point (C-comp) dominates adaptive on both axes; the decision rule only
   failed to promote because of debt, but %w alone would have promoted a dominated
   design by 0‰ margin.
4. Walk-corner aliasing: any debt-trend detector on this reality() channel needs
   period-240 corner blanking or a slope-normalized trend, or it will "detect"
   the paper's own stimulus waveform.
5. REGIME-META.md failure mode #3 ("mode choice right, diagnosis confused") turned
   out optimistic: with compensation, mode choice and diagnosis are both
   unnecessary in-loop; the doc's E4.B–E4.C narrative assumes an *uncompensated*
   detector view.

## Relation to round 4 (attempt 1, commit 07d0035/1542785) — the replication sharpening

Round 4 (Sep 3 lane) booked the same gate-2 FAIL (57,136 > 32,770) but saw the
adaptive loop WIN %w by +154‰ (932 vs best static 778). The delta between the two
lanes is one design choice, and it is the whole story: **attempt 1 gave the static
arms frozen or per-segment-oracle compensation (L̂=10 forever / true-lag oracle),
while the adaptive arm alone owned the live 480-tick blade.** This lane (4b) gives
EVERY arm the same live blade — the equal-blade control attempt 1 lacked. Under
equal-blade conditions the adaptive advantage inverts (978 vs 988‰, and 79.6k vs
75.0k debt): the +154‰ was the *blade's* win over handicapped statics, not the
*dial's* win over statics. Both lanes converge on the operative conclusions:

- debt gate fails under any design (57.1k / 79.6k vs 32.8k / 45.0k budgets);
- compensation is the causal agent (F19 doctrine: comp converts conflict→calm,
  191→1000‰; comp-seq ≥ comp-int everywhere in both lanes);
- detector conflict-entry lag is ~83–90 ticks vs the 1600-tick dwell, and REGIME-
  META E4.B's 2–4-tick prediction is falsified at spec thresholds in both lanes.

**Consolidated verdict for E4:** blade + compensator with a frozen sequential
dial (plus T2's N≥6 contention sort, round 3); the κ-dial is at best a slow
backstop and is strictly dominated when statics are compensated equally. No
QTORCH adaptive-arm pre-load. The knife-edge L̂±1 underseat scar (attempt 1:
bursty seq L̂=9→994‰ vs L̂=10→336‰) stands and is the one boundary this lane did
not re-measure.
