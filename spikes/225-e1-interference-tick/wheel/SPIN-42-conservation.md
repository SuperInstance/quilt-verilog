# SPIN-42 — CONSERVATION (wheel spoke 5): STOCHASTIC-MASS-NEUTRAL OBSERVER at K=2

**Dispatched:** 2026-09-04 ~06:1x AKDT (SPIN-41's next-spoke proposal; LCG spoke 5: 744964398 → 1969681615 → mod 10 = 5).
**Lane:** wheel_spin42_conservation · zai/glm-5.3 · run mode · one lane, no sub-lanes.
**Files:** spin42_conservation.py + spin42-conservation-output.txt + this report. Not committed to git.
**Runtime:** ~2 min, exit 0, first run (canary gate + panel in one pass; no re-runs needed).

## Pre-registered question

SPIN-41 falsified the floor-at-1 rescue: the K=2 zero-lock quantization cost stayed 48.7pp even when no magnitude is ever floored to zero — but its ledger showed the floored rounder is NOT mass-neutral (created 50,267 / deleted 7,007 per run → +43,260 net mass injected). Two candidate channels remained: **BIAS** (systematic net-mass distortion of the live wave) vs **OBSERVATION PER SE** (any grid snap of the live wave destroys coherence).

SPIN-42 replaces the deterministic rounder with **unbiased stochastic rounding**: round up with probability (a mod step)/step via integer LCG draws on a dedicated stream — E[new] = a exactly, drift ≈ 0 over the run, SPIN-15 delivered-mass ledger assert-enforced on every arm (same closure identity as SPIN-41).

**Pre-registered decision rule (committed in script header BEFORE any panel run):** PRIMARY cell zero K=2 q=8 (grid 4) M=1: cost ≤ 5.0pp → VALIDATED (channel = BIAS); cost > 10.0pp with drift-closed ledger → FALSIFIED (observation per se is the killer); else MIXED.

## Verdict: **VALIDATED — the decoherence channel is BIAS, not observation per se.**

- **PRIMARY cell: zero K=2 q=8 M=1 stochastic = 49.3 vs anchor (M=never) 50.0 → cost 0.7pp.** The SPIN-30/41 48.7pp catastrophe collapses to noise level under an unbiased observer at the identical observation rate and grid.
- Ledger drift: deleted 19,367 / created 19,424 mass/run → **+57** (vs SPIN-41 floored bias +43,260 — 750× smaller, consistent with random-walk residual, not systematic). SPIN-15 closure identity (emitted + quant_delta = decay + expired + inflight) assert-enforced and closed integer-exact on every panel arm; g-balance assert also live.
- Secondary kcoh5@15 K=2 q=8 M=1 cost = 4.2pp (drift −88) — same story, also inside the ≤5pp band.
- Reconciliation across spins: SPIN-30's round-to-nearest deleted small-mass pulses (amputation); SPIN-41's floor-at-1 removed the deletion channel but injected a huge upward bias (+43k); BOTH killed K=2 identically (48.7pp). SPIN-42 removes the last distortion — expectation-exact mass — and the cost vanishes. Three-rounders triangulation: **what destroys the K=2 wave is any systematic mass distortion of the live pulse state; unbiased noise at grid 4 is essentially free.**

## Grid detail (secondary, descriptive)

- K=1 rows: 0.0pp everywhere (as in SPIN-30/41 — structurally dead, pulses decay within birth tick).
- q=8 (step 4): all K=2 costs ≤ 4.2pp, M-monotone-ish weak (zero: 0.7/1.4/0.1/−0.2 — flat at noise; kcoh5: 4.2/1.1/2.4/0.3). Zeno signature gone at fine grid.
- **q=6 (step 16): the honest boundary — cost survives at 21.0pp (zero) / 34.5pp (kcoh5) at M=1**, monotone decreasing in M (21.0→11.6→3.3→2.5 and 34.5→21.4→8.0→1.8), with near-zero drift (+3,359 and +3,268 on ~100–120k mass — ~3% residual, still small). Unbiasedness fixes the expectation, not the variance: at coarse grid the per-draw rounding noise (±step) is large relative to live pulse magnitudes and decoheres by VARIANCE, not bias. SPIN-30's original q=6 M=1 zero K=2 catastrophe conflated both channels; SPIN-42 splits them: **bias channel dominant at fine grid, variance channel dominant at coarse grid.**
- q=12 (step 1): structural no-op, 0.0pp everywhere, 0 draws (rem==0 always) — expected.
- Created/deleted scale linearly with observation count (M=1 q=8 zero K=2: ~19.4k each vs q=6 ~100k): the observer's traffic is proportional to grid coarseness × live mass, exactly as the (a mod step) ledger predicts.

## Canaries — ALL PASS (first and only run)

- **a. Harness byte-identity:** run_fabric == sp41.dyn_run_mq(never) == dyn_run_sto(never) — 12 configs triple-identical, full resid lists (3 grammars × K{1,2} × seeds{1,42}).
- **b. Anchors digit-exact:** zero K=1 77.3 / debt 187834 / ev 8756; ladder@15 K=1 71.5 / 106378 / 5792.
- **c. SPIN-41 floored primary replay (via imported spin41_dequant):** floored zero K=2 q=8 = 1.3 vs never 50.0 → cost 48.7pp, exact.
- **d. gate=never ≡ mc=0:** 4 arms, created=deleted=0, zero observer draws, ledgers closed under live assert.
- **e. Determinism:** 1 floored + 2 stochastic cells run twice, byte-identical (resid, events, full ledger dict incl. n_draws).

## Scars / honest boundaries

1. **Stochastic rounding CAN zero a magnitude** (a < step: down-branch gives 0 with prob (step−a)/step) — this is the price of true unbiasedness (E[r]=a requires it) and is ledgered like every delta. The deletion channel is closed in expectation, not pathwise; at grid 4 with live mags ≈ 1–20 it is rare-but-nonzero. Anyone quoting "mass-preserving stochastic observer" must say *preserving in expectation*.
2. **Rescue is grid-fine-specific:** the ≤5pp VALIDATED claim is a q=8/grid-4 statement. At q=6/grid-16 the unbiased observer still costs 21–34.5pp (variance channel). Falsifying-observation-per-se is only established where the rounding noise is small; a variance-vs-noise decoherence law (cost ~ f(step/typical-mass)) is unmeasured.
3. **Drift "closed" is empirical, not asserted:** +57 on ~19.4k gross traffic (0.3%) at the primary cell; ~3% at q=6. The hard asserts are the SPIN-15 integer-exact identities (per-path), which hold regardless; the near-zero drift is a realization property of 4800-tick runs, verified 5-seed means.
4. **Dedicated observer LCG stream** (seed ^ 0x5A17C0DE) keeps dynamics byte-identical when measurement is off (canary a/d), but means stochastic-arm results are stream-seed-specific in realization; 5-seed means only. No seed-sensitivity sweep was run (would be the first follow-up if the primary had landed near the 5pp boundary — it landed at 0.7).
5. Same structural vacuity scar as SPIN-30/41: K=1 rows carry no information (pulses dead within birth tick); only K=2 rows have content on this fabric.

## Next-spoke proposal

**VARIANCE-CHANNEL LAW (dequant/conservation border):** measure cost(step) for the unbiased observer at K=2 M=1 across q ∈ {5,6,7,8} (steps 32/16/8/4) × grammars {zero, kcoh5@15}, with per-run rounding-noise bookkeeping (Σ|a − E[r]| / live mass as the instrument statistic). Pre-register: cost is governed by noise-to-live-mass ratio, not by step per se — predict a single collapse curve cost ≈ h(Σ|Δ|/M_live) shared across grammars; falsify if grammars separate at matched noise ratio. This closes the decoherence taxonomy: amputation (SPIN-30) / bias (SPIN-41) / observation-free variance (SPIN-42 residual).
