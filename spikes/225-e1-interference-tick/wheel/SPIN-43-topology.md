# SPIN-43 — TOPOLOGY (wheel spoke 4): VARIANCE-CHANNEL LAW across grammars

**Dispatched:** 2026-09-04 ~06:1x AKDT (SPIN-42's next-spoke proposal, LCG spoke 4).
**Lane:** wheel_spin43_topology · zai/glm-5.3 · run mode · one lane, no sub-lanes.
**Files:** spin43_topology.py + spin43-topology-output.txt + this report. Not committed to git.
**Runtime:** ~4 min total (3 aborted dev runs before the clean pass — see scars), exit 0.

## Pre-registered question

SPIN-42 left a scar: the unbiased stochastic observer rescues K=2 at fine grid (0.7pp at q=8) but still costs 21.0pp (zero) / 34.5pp (kcoh5@15) at q=6 — attributed to a VARIANCE channel (rounding noise vs live mass). SPIN-43 maps cost(step) for the UNBIASED observer at M=1 over grammars {zero, ladder@15, kcoh5@15} × K ∈ {1,2} × q ∈ {5,6,7,8} (steps 32/16/8/4), with read-only integer instruments inside the SPIN-42-identical measurement loop: live_mass_sum (Σ|mag| observed), noise_energy (Σ rem·(step−rem) — the exact per-draw rounding variance), n_obs. Instrument statistic ρ = sqrt(noise_energy)/live_mass_sum (floated only at print/verdict).

**Pre-registered decision rules (script header, before any run):**
- H1 (single collapse curve cost ≈ h(ρ) shared across grammars, ε=5.0pp): VALIDATED iff every leave-one-grammar-out nearest-ρ residual ≤ ε AND pooled Spearman(cost, ρ) ≥ 0.90; FALSIFIED iff any residual > ε **with drift-closed ledgers** (|created−deleted| < 10% of created); else MIXED.
- H2 (q=6 cost monotone in step-16 noise magnitude across grammars at K=2): VALIDATED iff cost ranks == noise_energy ranks AND == ρ ranks; else FALSIFIED.

## Verdict: **H1 MIXED (collapse decisively broken; FALSIFIED branch blocked by the drift gate) · H2 FALSIFIED**

### H1 — no shared collapse curve in (cost, ρ)

- Pooled Spearman(cost, ρ) = **−0.608** (need ≥ +0.90): the pre-registered noise-to-live-mass ratio is **negatively** associated with cost across the 12 K=2 cells. Max LOO residual **40.8pp** (ladder@15 q=6: cost 45.1 vs nearest-ρ cross-grammar prediction 4.2).
- The mechanics: at K=2, ρ is **non-monotone in step** (zero: 0.0009/0.0035/0.0038/0.0023 for q=5/6/7/8) — coarse grids inflate live_mass_sum faster than noise_energy (the coarse grid itself inflates in-flight magnitudes), so the registered denominator is confounded with the treatment. kcoh5@15 has the **lowest** ρ at every q yet pays higher cost than zero at q ∈ {5,6,7}.
- Why not FALSIFIED as registered: the falsify branch required drift-closed ledgers (<10% of created). The q=5 arms carry +34,999/+25,906/+20,598 drift on ~253–281k created (7.4–12.4%) — the unbiased rounder's random-walk drift at the coarsest grid breaks the 10% gate (zero q=5: 12.4%). Rule followed as written → MIXED. The substantive reading is unambiguous: **cost is grammar-first, noise-ratio-second** — the per-q cost ordering is ladder@15 > kcoh5@15 > zero at every grid (57.4>48.4>44.6; 45.1>34.5>21.0; 32.1>19.4>5.9; 4.8>4.2>0.7).
- What DOES collapse: per-grammar cost-vs-step curves are smooth and monotone decreasing in fineness (each grammar drops from ~45–57pp at step 32 to ~1–5pp at step 4). The grid axis is universal; the level is grammar-specific. This is a **family of parallel curves, not one curve**.

### H2 — q=6 cost is NOT monotone in noise magnitude

At step 16, K=2: zero noise 1.616e6 → cost 21.0pp; ladder 1.857e6 → 45.1pp; kcoh5 1.921e6 → 34.5pp. Noise ordering (zero < ladder < kcoh5) vs cost ordering (zero < kcoh5 < ladder) — ladder/kcoh5 swap. Also non-monotone in ρ. **FALSIFIED** cleanly.

### Descriptive panel (K=1 rows)

K=1 rows are 0.0pp everywhere at every q — pulses die within their birth tick (SPIN-30/41/42 structural-vacuity scar, third confirmation). Note the K=1 ρ values are ~10–40× larger than K=2 (0.03–0.04 vs 0.0004–0.004) yet cost nothing — further evidence that the live-mass noise ratio is not the cost-governing quantity.

## Canaries — ALL PASS (clean pass run)

- **a. Harness import byte-identity:** 12 never-arms triple-identical (run_fabric == sp42.dyn_run_sto == dyn_run_sto43, full resid) + 24 measurement arms identical in resid/events/SPIN-42-ledger keys (instruments are read-only additions).
- **b. Anchors digit-exact:** zero K=1 77.3 / 187834 / 8756; ladder@15 K=1 71.5 / 106378 / 5792.
- **c. SPIN-42 replays via imported original:** zero K=2 q=8 M=1 cost 0.7pp exact; q=6 M=1 cost 21.0pp exact.
- **d. gate=never ≡ mc=0:** 6 arms created=deleted=0, zero draws, ledger assert-live.
- **e. Determinism:** dual runs byte-identical incl. instrument fields.
- **SPIN-15 ledger closure** (emitted + quant_delta == decay + expired + inflight, plus g-balance) asserted on **every** arm of every cell.

## Scars / honest boundaries

1. **The registered ρ statistic was the wrong instrument.** sqrt(noise_energy)/live_mass_sum is non-monotone in step at K=2 because the coarse grid inflates the mass denominator; it ranks kcoh5 as the SAFEST grammar at every grid while kcoh5 pays 20–34pp more than zero at q ∈ {5,6,7}. A collapse-curve test is only as good as its normalizer; the negative Spearman (−0.608) falsifies this particular normalization, not the broader "variance channel" story (which is confirmed descriptively: monotone-in-step per grammar, created/deleted traffic ∝ coarseness × mass).
2. **Drift gate bit its own tail:** the FALSIFIED branch's drift-closure requirement (<10%) fails precisely at the coarsest grid where the variance channel is strongest — unbiasedness holds in expectation, but the 4800-tick random-walk realization drift at step 32 reaches 12.4%. The verdict lands MIXED by rule, not by ambiguity.
3. **Dev-run aborts (3) before the clean pass:** (i) canary-a ledger-dict comparison tripped on the instrument keys (fixed by comparing SPIN-42 keys + explicit read-only additions); (ii) 3-tuple unpack of 2-tuple GRAMS43; (iii) drift_ok unpack. All pre-panel; the registered rules were never edited after any panel run — the only registered quantity touched during dev was the canary comparison logic, not H1/H2 rules or ε.
4. Same K=1 structural vacuity as SPIN-30/41/42; K=1 rows carry no information on this fabric.
5. 5-seed means only; stochastic arms are observer-stream realization-specific (SPIN-42 scar, inherited). No seed-sensitivity sweep.

## Next-spoke proposal

**COHERENCE-MASS NORMALIZER (dequant border):** the failure mode of ρ points at the missing denominator — not total live mass but the mass scale on which coherence decisions are made (per-pulse typical magnitude vs the (8/5)·lag firing threshold, or noise per-pulse rather than noise per-run). Proposal: per-grammar collapse test with ρ_pulse = sqrt(noise_energy/n_obs)/median-observed-magnitude, plus a two-parameter fit cost ≈ f(step, grammar-fragility) where fragility is anchored by the measured ladder>cohort>zero ordering (which echoes SPIN-9's fresh-cohort axis). Alternative cheaper probe: noise-per-draw fixed, sweep live-magnitude scale via pd ∈ {2,3,6} at q=6 — if cost moves with pd at matched step, the denominator is the pulse-mass scale, not the grid.

## Bookkeeping

- Cost table (K=2, M=1, 5-seed means), pp vs per-cell M=never anchor:

| grammar | q=5 (32) | q=6 (16) | q=7 (8) | q=8 (4) |
|---|---|---|---|---|
| zero | 44.6 | 21.0 | 5.9 | 0.7 |
| ladder@15 | 57.4 | 45.1 | 32.1 | 4.8 |
| kcoh5@15 | 48.4 | 34.5 | 19.4 | 4.2 |

- SPIN-42 reconciliation: zero q=6 21.0 and q=8 0.7 replay exact via the imported SPIN-42 module; kcoh5 q=6 34.5 / q=8 4.2 reproduce SPIN-42's published 34.5 / 4.2.
