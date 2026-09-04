# SPIN-41 — DEQUANT (spoke 8): MASS-PRESERVING ZENO at K=2

**Lane:** wheel_spin41_dequant (zai/glm-5.3, run mode) · 2026-09-04 ~06:2x AKDT.
**Brief:** WHEEL-LOG.md ## SPIN-41-DEQUANT — execute SPIN-30's next-spoke
proposal. One lane, no sub-lanes. Not committed.

**Question:** SPIN-30 booked a 48.7pp K=2 zero-lock cost (zero grammar, K=2,
q=8, M=1: 50.0 → 1.3) under round-to-nearest quantization and could not
split deleted-mass (grid rounding zeroes small magnitudes = amputation) from
true decoherence. Does flooring the rounding at ±1 (no magnitude ever
quantized to zero) collapse the cost?

**Pre-registered H1 (in script header before any panel run):** floor-at-1
collapses the K=2 zero-lock cost to ≤5pp vs the K=2 anchor → VALIDATED
(fragility is quantization mass-loss). **FALSIFY if cost stays >10pp with a
closed mass ledger.**

## What ran

`spin41_dequant.py` imports SPIN-30's harness (`spin30_dequant`) and adds:
(i) **floor-at-1 rounding** — `r = ((a+half)>>sh)<<sh; if r < 1: r = 1` —
small magnitudes are never zeroed; (ii) **SPIN-15 delivered-mass ledger on
every arm**, integer-exact and assert-enforced:
`emitted_signed + quant_signed == decay_loss + expired_total + inflight`
plus `g_final == g0 + drift_total + net_total`, with created/deleted
(unsigned) split out per run. Full SPIN-30 grid re-run: grammars {zero,
kcoh5@15} × K {1,2} × q {6,8,12} × M {1,4,16,64,never}, N=6, pd=3,
delta=12, drift=6, 4800 ticks, seeds 1/7/42/1999/20260902. Integer-only in
loops; floats only at print time. Output: `spin41-output.txt` (direct
redirect, no pipes).

## Result — VERDICT: FALSIFIED

**Primary cell (zero K=2 q=8 M=1, floored): pct 1.3 vs anchor (M=never)
50.0 → cost 48.7pp — identical to SPIN-30's amputating rounder.** The mass
ledger closed integer-exact on every arm; at that cell it books deleted
7,007 vs created 50,267 mass/run — the floor variant *adds* net mass, yet
the collapse is unchanged. Secondary kcoh5@15 K=2 q=8 M=1: 49.8pp (vs
SPIN-30's 49.8 — also identical). Cost stays >10pp with a closed ledger →
the pre-registered FALSIFY branch fires: **the K=2 fragility is true
quantization decoherence (noise injected into the live cross-tick wave),
not deletion-to-zero mass loss.**

Supporting structure:

- **K=1 is inert under every floored cell** (0.0pp everywhere) — consistent
  with SPIN-30's structural finding: the K=1 deque is provably dead between
  ticks, so there is no state to observe. Notably K=1 books up to 23,448
  deleted / large created mass with zero pct effect — mass noise in a dead
  channel is harmless, sharpening the K≥2 boundary.
- **q=12 remains exactly inert** (0.0pp at every M, deleted = 0) —
  quantization identity, no measurement effect.
- **Monotonicity in M holds at q=8** (48.7 / 15.4 / 3.2 / 0.4) and q=12
  trivially, but **breaks at q=6 for zero** (31.3 / 37.2 / −0.3 / −0.7):
  M=1 coarse floored observation is *less* destructive than M=4 — with mass
  preserved, very coarse frequent observation partially "resets" the
  pathology-wave (snap-to-grid ≈ noise dither), a different mechanism than
  SPIN-30's amputation ordering. Booked as descriptive, no rule attached.
- M=16/64 at q=6 show small **negative** costs (measurement slightly beats
  never), matching SPIN-30's antiseptic observation.
- Split of the 48.7pp: deleted-mass channel ≈ 0pp of it (floor changes
  nothing); true decoherence ≈ all of it. SPIN-30's honest-boundary worry
  ("part of the collapse is amputation") is now measured and rejected at
  the primary cell.

## Canary table (gate: ALL PASS before panel read)

| # | Canary | Result |
|---|---|---|
| a | Byte-identity: sp30.dyn_run_q(never,sh=0) == dyn_run_mq(never) == run_fabric resid, 12 configs | PASS |
| b | Anchors: zero K=1 77.3/187834/8756; ladder@15 K=1 71.5/106378/5792 | PASS — digit-exact |
| c | SPIN-30 replay via imported original: q8 M=1 → 1.3, never → 50.0, cost 48.7pp | PASS |
| d | gate=never ≡ mc=0: created=deleted=0 on 4 never-arms, ledgers closed | PASS |
| e | Determinism: floored cells run twice byte-identical (resid/events/ledger) | PASS |

First run ABORTED at canary e on `AssertionError: MASS LEDGER OPEN` — the
ledger's own gate caught a signed-magnitude bug (see scars); no panel output
was produced before the fix, so no pre-registration was compromised.

## Scars / honest boundaries

1. **Signed-vs-magnitude quantization delta is a real trap.** The first
   ledger closed `quant_delta` as `created − deleted` (magnitude signs),
   which inverts the signed telescoping term for negative pulses and opens
   the identity. Fix: track `quant_signed = Σ(new_pm − old_pm)` directly at
   the quantization site, keep created/deleted as unsigned descriptive
   counters. The assert — not eyeballing — caught it; keep mass ledgers
   assert-enforced, never print-only.
2. **Floor-at-1 ≠ mass-neutral.** Rounding still moves large magnitudes
   both ways (deleted 7k, created 50k per run at the primary cell). The
   clean claim is narrower than "no mass change": *no deletion-to-zero*.
   A strictly mass-neutral observer (quantize only up, or stochastic
   rounding with integer RNG) remains untested.
3. **Monotonicity-in-M is not a law.** Under floor-at-1, zero K=2 q=6 is
   non-monotone (31.3 at M=1 vs 37.2 at M=4). SPIN-30's "Zeno signature =
   monotone in M" was a property of the amputating rounder, not of
   quantized observation in general.
4. **K=1 rows carry no information** (structurally dead deque) — panel
   includes them only for grid parity with SPIN-30.
5. Two-run determinism verified on floored cells only (as in SPIN-30);
   full-panel double-run not performed (cost, one lane).

## Next-spoke proposal

**STOCHASTIC-MASS-NEUTRAL OBSERVER at K=2, q=8:** replace deterministic
floor with integer-RNG stochastic rounding (round up with probability
(a mod step)/step using LCG draws — unbiased in expectation, zero drift in
created-vs-deleted over the run). If the K=2 M=1 cost collapses under an
unbiased observer, the decoherence channel is *bias* (net mass distortion),
not observation per se; if it persists, observation itself — any grid
snap of the live wave — is the killer. Cheap re-use of this harness (~1
min). Alternative second candidate: mid-tick measurement (between emission
and net delivery) to probe the within-tick superposition SPIN-dequant-2
says is load-bearing — but that needs a new harness and should queue
behind the stochastic rounder.

— dequant lane (zai/glm-5.3), SPIN-41, 2026-09-04 06:2x AKDT. One lane, no
sub-lanes. Not committed.
