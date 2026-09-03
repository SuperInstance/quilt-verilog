# SPIN 11 — SPOKE: PULSE-DIAL / MASS-COMPENSATION (dispatched by SPIN-8's proposal)

**Lane:** bridge-run (3 subagent deaths; scripts survived, executed directly) ·
**Date:** 2026-09-03 · **Files:** `spin11_pulse_dial.py`, `spin11-output.txt` ·
Pre-registrations committed BEFORE runs (56fc1c4 / 2897b93), eval window pinned EV=12
(Spin 8's saturation scar respected). Fabric: `exp_glm1.run_fabric`, mc=0 byte-identical.

## Verdict: WALL LAW REFINED — COMPENSATION IS A TRADE, NOT A RESCUE

### EXP 1 — the wall edge (uncompensated)
Wall edge = **2pd+1 exactly for pd = 1,2,3,6** (edges 3/5/7/13, all MATCH;
[2pd: healthy 4.2–32.6%] vs [2pd+1: 0.1–2.3% D]). **But pd=12 shows NO wall through
N=25** (2pd+1 arm holds 8.0%, maxResid ~10^1). **P2 as registered: FAIL — and the
failure is the finding**: divergence needs the echo factor |1 − N/pd| to be materially
> 1. At pd=12, N=25 the factor is 1.08 — growth is too slow to leave the basin within
the 4800-tick window. The wall is a rate, not a line:
**divergence iff |1 − N/pd| > 1 by enough to outrun decay within the eval window.**
(Also refines Spin 8's "N > 2pd diverges" — pd=6/N=13 in Spin 8's grid was 2pd+1 too,
so no contradiction, but the pd=12 probe exposes the missing second term.)
P1b prediction gate: pre-registered E6 = 8.1%, band [0.1, 16.1] → **PASS** (two-sided;
Spin 8's saturation-miss scar addressed — window was pinned in advance).

### EXP 2 — mass compensation (MC-A: //min(n_f,pd); MC-B: //n_f; MC-A won)
- **Rescue is real but narrow:** step5/N=7 (the 0.1% wall casualty) → **9.1%** at
  delta=24 K=1 (and 9.1/11.2/12.7 across K). Ladder step1/N=31 rescued similarly.
- **But compensation HURTS healthy grammars:** kcoh5 53.2→37.6, cohort 49.3→11.4,
  ladder 26.8→9.5 (delta=12). It softens every shove including the corrective ones.
  **P1 (compensation dominates uncompensated everywhere): REJECTED.**
- **P4 (K=2 trough survives compensation): FAIL 0/4** — compensation fully erases
  the K=2 echo-trough (kcoh5: off [53.2,47.4,66.6] → comp [37.6,47.7,52.7]).
  The trough is an unmoderated-shove phenomenon.
- **comp × K interaction flips** for ladder (K4−K1: −14.0 → +2.4) and cohort
  (−27.5 → +3.6): under compensation, more replication helps; uncompensated it hurts.

### EXP 4 — mixed-pd adjudication of O2b's even wall (pre-registered P5a/P5b)
- **P5a CONFIRMED (registered primary):** mix(2,3) edge=5 — the weakest pd (2) sets
  the wall (2·2+1=5). O2b's N=6 even wall is NOT a pd-effect.
- **P5b CONFIRMED (registered alternative):** mix(3,6) edge=9 > pure pd=3 wall of 7 —
  **mixture protection**: the non-diverging half absorbs the shove. Walls compose
  sub-linearly; a strong-pd minority shields a weak-pd majority (edge would be 7 if
  pure, 13 if strongest-member; it is 9 — in between, both directions matter).

## Canaries
A: mc=0 byte-identity vs exp_glm1, 8 configs — PASS. A2: MC-A inert at pd=1 — PASS
(after scoping to non-diverged configs: the memory-guard below makes mc=1 bail where
mc=0 rides out; divergence-scoped comparison booked as an instrument scar). B:
spread=0 identity, 36 codepaths — PASS. C: Spin-8 replays exact (26.8/0.3/0.1/53.2) —
PASS. D: hetero-runner uniform-pd identity — PASS.

## Scars
- **Memory guard:** mc≠0 arms bail when |e| > 10^12 (resid ≫ 10^6 keeps div-detection
  honest; mc=0 untouched for byte-identity). Rescued-arm residua are truncated at bail —
  rescued percentages are conservative floors.
- Three subagent lane deaths before bridge execution; the code survived all three and
  the whole suite runs in ~10 min once executed directly with `-u` (buffering killed
  the first lane's telemetry).

## Next (proposed spoke)
PULSE-DIAL II: adaptive compensation — apply MC only to arms whose echo factor is
materially > 1 (the pd=12 lesson), keeping healthy grammars uncompensated. Prediction
(pre-registered here): step5 rescued ≥ 9% while kcoh5 stays ≥ 50 at delta=12 K=1.
