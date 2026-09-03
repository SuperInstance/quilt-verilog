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

## RESULTS

(filled after the run)
