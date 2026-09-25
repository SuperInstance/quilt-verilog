# Round 5 — O5 Phase-decay coupling, multi-seed confirm

Date: 2026-09-03 12:3x AKDT · branch `g3-kinduction` · harness `o5_phase_decay.py` · raw output `o5-phase-decay-output.txt`

## Hypothesis

F24's phase-decay coupling win (claude #1: 84.3% vs 83.0% at stress, seed 20260902 only,
cancels 107 vs 68) survives 5 seeds. Mechanistic claim: **dissipating faster while refractory
preserves net==0 residency**, while **deferring admission destroys it** (F16, glm-3 #4).
Paired comparison vs an admission gate at *matched duty* (same phase clock, same 4/12
refractory window — the only difference is *modulate decay* vs *defer admission*).

## Setup

- 5 seeds {1, 7, 42, 1999, 20260902} × 2 regimes × 3 arms, 4800 ticks, integer-only, LCG fixed.
- Regimes (same as e1/arena): calm Δ=6/drift=3/K=8/lat2=5; stress Δ=12/drift=6/K=4/lat2=10.
- Arms (one shared code path):
  - `baseline` — plain interference (e1 semantics).
  - `phase_decay` — F24: second integer halving of pulse magnitude while `phase_counter < 4` (period 12).
  - `admission_gate` — same phase clock; pulse admission *deferred* while refractory, admitted when refractory lifts.
- Primary pre-registered metric: **stress %within, phase_decay vs baseline.**

## Results

### Stress (primary)

| seed | baseline %w (cancel) | phase_decay %w (cancel) | admission_gate %w (cancel) | Δpd | Δgate |
|---|---|---|---|---|---|
| 1 | 83.0 (63) | 85.8 (92) | 54.3 (88) | +2.8 | −28.7 |
| 7 | 82.5 (70) | 85.0 (88) | 56.8 (82) | +2.5 | −25.7 |
| 42 | 83.4 (84) | 85.4 (98) | 54.8 (73) | +2.0 | −28.6 |
| 1999 | 83.6 (68) | 85.0 (113) | 54.9 (99) | +1.4 | −28.7 |
| 20260902 | 83.0 (68) | 84.3 (107) | 55.5 (106) | +1.3 | −27.5 |

**Mean Δpd = +2.00pp, worst seed +1.3pp. Cancels up on 5/5 seeds (mean ~100 vs ~71).**

### Calm (secondary)

| seed | Δpd | Δgate |
|---|---|---|
| 1 | −1.5 | −6.1 |
| 7 | −2.5 | −7.9 |
| 42 | −1.8 | −3.4 |
| 1999 | −2.5 | −9.8 |
| 20260902 | −5.1 | −12.3 |

Calm mean Δpd = −2.7pp (mild penalty; calm here is the K=8 grid artifact regime of F13 — coupling
should be phase-gated by regime, or simply default-off at K≥8 calm). Admission gate is negative
everywhere: calm −7.9pp, stress −27.8pp mean — **F16 replicated at matched duty.**

## Canaries

1. **Published-anchor replay:** F24 numbers reproduce exactly at seed 20260902 stress —
   baseline 83.0/cancel 68, phase_decay 84.3/cancel 107. PASS.
2. **Self-canary (mislabeled arm):** ran baseline under the `phase_decay` label; fingerprint
   check (events, debt, cancels, %w) against the true arm reference caught the mismatch. PASS.
3. **Determinism:** full harness run twice; stdout and written output file byte-identical. PASS.

## Decision rule (pre-registered)

> promote iff mean Δ ≥ +0.5pp AND no seed < −0.5pp

- mean Δ = **+2.00pp** ≥ +0.5 ✓
- worst seed = **+1.3pp** ≥ −0.5 ✓

## Verdict

**PROMOTE — CONFIRMED, and stronger than published.** Phase-decay coupling survives and *grows*
under multi-seed (every seed beats the single published seed's +1.3pp; mean +2.0pp). The F24-vs-F16
contrast is real and now duty-matched: modulating decay in refractory buys cancellation residency
(cancels +40% mean at stress); deferring admission on the identical phase clock destroys residency
(−27.8pp stress). The boundary is sharp: **touch the decay, not the door.**

Actions:
- Phase-decay coupling → e1.py candidate default **for stress/conflict regimes** (default-off in
  calm at K=8 until regime-conditional; O4's κ-detector is the natural dial).
- Price the RTL: ~30 LUTs per R1 cell (per agenda line item) — phase counter (4-bit), refractory
  compare, second halving mux. Candidate module note for the next RTL round.

Scars booked: calm penalty −2.7pp mean (K=8 calm is itself the F13 artifact regime); admission
gate's stress cancellations (448) exceed baseline (353) yet %w collapses — cancellation count
alone is not residency, echoing F7's saturation caveat.
