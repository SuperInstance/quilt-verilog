# SPIN 22 — QUANTIZED SCHEDULER (SPIN-20 question #3)

**Lane:** subagent spin (SPIN-20-questions.md question #3 — "does the learned
scheduler survive ±7/4-bit quantization?") · **Date:** 2026-09-03 ·
**Files:** `spin22_quantized_scheduler.py`, `spin22-output.txt`, this report.
Fabric: spin16 `run_fabric_gate` reused verbatim (integer-only in-loop gate
`100·|pd−nf| > t100·pd`); anchors on the spin-16 gate contract, pd=3,
delta=12, EV=12, drift=6, 4800 ticks.

## PRE-REGISTRATION (committed BEFORE any panel run)

**Question.** The echo-factor gate is analog: continuous θ ∈ (1, 4/3) is the
useful band at pd=3 (θ < 1+1/pd for the 2pd+1=7 wall to open; θ ≥ 4/3 never
opens; θ ≤ 1 admits nf=6). Does quantizing θ onto a coarse ladder (4 / 8 / 16
levels across the band) help or hurt vs continuous θ\* = 1.1 (SPIN-16's
corrected calibration)?

**Ladder construction.** Band t100 ∈ [100, 133] (θ ∈ [1.00, 1.33]). L-level
midpoint quantizer: t100 = 100 + round((i+0.5)·33/L), i = 0..L−1. The scheduler
uses ONLY the nearest ladder level to the desired θ (no dithering, no
interpolation — the ESP32 target is a lookup table replacing the divider).

**Panel (seeds {1,7,42}, K=1 unless noted):**
- kcoh5@15 [0,0,0,0,0,15] (healthy, gate structurally inert)
- ladder@30 = ladder(30) (healthy N=6)
- step5/N=7 = ladder_step(30,5) (wall casualty, THE rescue cell)
- step5/N=7, K=2 (memory-eroded rescue)
- zero7 [0]·7 (diverged, near-perfect cure)

Arms: continuous θ\*=1.1 (reference), plus every ladder level of the 4-, 8-,
and 16-level ladders (each level is a full fabric run — 4+8+16 = 28 quantized
θ settings + 1 continuous, × 5 panel cells × 3 seeds). Out-of-band probes to
book where quantization bites: t100 ∈ {99, 100, 134} on step5 K=1 (sub-1.0
edge, band floor, band ceiling).

**PREDICTION (pre-stated):** the gate is ALREADY quantal at pd=3. The in-loop
test is integer in t100 and the concurrent echo factor takes only values
|3−nf|/3 for nf ∈ 1..7; within the band the ONLY crossing is nf=7
(400 > t100·3 ⟺ t100 ≤ 133). Therefore every t100 ∈ {100..133} is
byte-identical on every panel cell: quantized == continuous to 0.0pp at 4, 8,
AND 16 levels — quantization is FREE at this pd, and the true ladder
resolution of the gate is ONE level. Falsifier: any byte-hash difference or
>1.0pp drop at any in-band ladder level.

**DECISION RULE (pre-stated):** quantized ≥ continuous − 1.0pp on ALL five
anchors ⇒ "coarse gate survives" ⇒ **GO** for embedded/ESP32 (16-level lookup
replaces the divider). Any anchor drops > 1.0pp ⇒ **NO-GO**; book which end of
the band bites (prediction if NO-GO: the TOP end — a single step 133→134
silently closes the gate at the pd=3 wall and re-loses the entire step5
rescue; the bottom end 100→99 admits nf=6 compensation, a milder wrong-side
error).

**CANARIES (abort on fail):** (1) spread=0 byte-identity on kcoh5 gate==off
(kcoh(5,0) full-dict sha identical across gate modes {never, 1.1} and across
dual runs); (2) ladder@15 K=1 = 71.5 exact (0.2pp tol); (3) zero7 gate = 99.8
anchor. 3-seed panel values noted at probe time: step5 K1 36.9 / K2 30.6,
kcoh5@15 74.6, ladder30 26.1.

## RESULTS — GO: "COARSE GATE SURVIVES" — QUANTIZATION IS FREE (THE GATE IS ALREADY ONE-LEVEL AT pd=3)

All canaries PASS (3/3): spread=0 byte-identity on kcoh5 gate==off (never == θ1.1
== dual-run, full-dict sha); ladder@15 K=1 = 71.5 exact; zero7 gate = 99.8 exact.

**Every one of the 28 in-band ladder levels (4/8/16-level ladders) is +0.0pp
and full-dict sha byte-identical to continuous θ\*=1.10 on all five anchors**
(kcoh5@15 74.6, ladder30 26.1, step5K1 36.9, step5K2 30.6, zero7 99.8 —
seeds {1,7,42}). Registered prediction CONFIRMED: the in-loop gate test is
integer in t100 and the concurrent echo factor |3−nf|/3 takes only 7 discrete
values; within the band the only crossing is nf=7 (2pd+1 wall), so every
t100 ∈ {100..133} is the same function. **The θ dial has exactly ONE useful
level at pd=3 — the ladder's true resolution is 1 bit, not 4/8/16.** Decision
rule met on all anchors (worst delta +0.0pp ≥ −1.0pp): **GO for
embedded/ESP32 — a single-entry lookup (t100=110, or any value in 100..133)
replaces the divider; there is nothing to quantize away.**

**Where quantization bites (out-of-band probes, step5 K=1):**
- TOP end: t100=133→134 (θ 1.33→1.34, one ladder step past the band ceiling)
  silently closes the gate at the pd=3 wall — reads 14.1 ≠ continuous, −22.8pp.
  Honest read: this is the guard-prefix statistic (numeric-gate arms carry the
  spin-11 memory guard, so the diverged run is truncated; true off = 0.3) —
  same artifact class as SPIN-16's θ=1.5/2.0 rows. The rescue is gone; the
  number 14.1 is a prefix window, not a steady-state. **The bite is at the TOP
  of the band exactly as pre-registered**, and it is cliff-shaped: one step,
  −36.6pp of rescue (36.9 → prefix 14.1 / true 0.3).
- BOTTOM end: t100=100→99 (θ 1.00→0.99) admits nf=6 compensation — mild, −0.6pp
  on step5 K=1 (36.9→36.3). The sub-1.0 regime is the gentler wrong side
  (SPIN-16's "missing dial").
- t100=100 (θ=1.00 exactly) is still byte-identical (the nf=6 test is
  300 > 300 = false, strict inequality).

### Table (levels vs rescue/healthy; all in-band cells identical)

| arm | kcoh5@15 | ladder30 | step5K1 | step5K2 | zero7 |
|---|---|---|---|---|---|
| continuous θ\*=1.10 | 74.6 | 26.1 | 36.9 | 30.6 | 99.8 |
| 4-level ladder (104..129) | 74.6== | 26.1== | 36.9== | 30.6== | 99.8== |
| 8-level ladder (102..131) | 74.6== | 26.1== | 36.9== | 30.6== | 99.8== |
| 16-level ladder (101..132) | 74.6== | 26.1== | 36.9== | 30.6== | 99.8== |
| top-edge probe θ=1.34 | — | — | 14.1 (−22.8, prefix) | — | — |
| bottom-edge probe θ=0.99 | — | — | 36.3 (−0.6) | — | — |

"==" = full-dict sha byte-identical per seed to continuous.

## SCARS
1. **The θ ladder is a phantom dial at fixed pd.** General law: the gate's
   effective resolution is the number of DISTINCT wall crossings
   ceil-thresholds in the band, i.e. one per reachable nf with
   t100 ∈ (100·|pd−nf|/pd − something) — at pd=3 with N≤7 twins that is ONE
   level. Any paper reporting a θ sweep INSIDE (1, 1+1/pd) at fixed pd=3,
   N=7 is sweeping a constant (SPIN-16 EXP-1's {1.05,1.1,1.25} row collapse
   was this, seen but not named).
2. **θ-quantization study needs a pd sweep to have content.** The ladder only
   acquires levels when multiple nf-crossings lie in the band — i.e. larger pd
   (e.g. pd=6: band (1, 7/6), crossings at nf=13 only at pd=6... still one
   level per pd). The genuinely quantized object is the PAIR (pd, wall nf),
   one bit each. Embedded recommendation: hard-code `nf > 2*pd` (θ≡1 as an
   integer comparison, zero multiply, zero LUT) — it is byte-identical to
   θ\*=1.10 by the same argument and is what the RTL already implements as
   the cross-mult 100·|pd−nf| > 110·pd.
3. **Guard-prefix asymmetry:** an out-of-band-high θ run is NOT equal to
   gate=never even though the gate never opens, because numeric-gate arms
   carry the memory guard and truncate divergence (14.1 vs true 0.3). Any
   "gate closed" arm must be run as gate="never" to be the honest off.

## NEXT
- pd-sweep ladder (pd ∈ {3,4,6,9}) to find the first pd where two in-band
  crossings exist — the true resolution curve of the gate vs pd.
- Wire the 1-bit form (nf > 2pd) into the RTL q_cell sidecar from SPIN-19's
  Next and re-run the bit-exact suite — expected free simplification.
