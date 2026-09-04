# SPIN-30 — METROLOGY: drift × band sweep at Δ=12 — α is NOT drift; 2Δ stays dead at drift=0

**VERDICT (pre-registered gates): MIXED — H1 falsified outright; H2 survives everywhere except the small-band × high-drift corner.** Neither clean story wins:

- **H1 (drift is the violator; 2Δ returns at drift→0) is DEAD.** At drift=0, α = 1.190 / 1.142 / 1.126 (A = 96/200/400) — no collapse toward 1. Removing drift entirely moves α by ~0.5% (α(d2)=1.135 vs α(d0)=1.142 at A=200). Even at drift=0, C ≈ 27–28.5, i.e. 3–4.5 above 2Δ=24 — 6–9× the noise floor. **The 2Δ law does not return; it is dead with or without drift.**
- **H2 (α ≈ 1.19 fabric constant) holds to first order but not exactly.** Across A ∈ {200, 400} (8 arms) α ranges only 1.114–1.192 (6.8%, inside the 15% gate). The all-12 gate fails (23.9%) solely because the A=96 arm blows up with drift: α = 1.190 → 1.323 → 1.398 at drift 0/6/10.
- Best compact reading: **C = 2.38·Δ (base) + weak negative log-band term + drift×small-band interaction.** At A=200: C = 27.22 + 0.138·drift (intercept ≠ 24, slope ≈ 0 — a near-drift-independent constant of ≈2.27·Δ). At drift=6: C = 45.20 − 2.11·log₂(A) (maxres 0.94).

**Files:** `spin30_drift_band_sweep.py`, `spin30-output.txt` (elapsed 10 s, ~1090 fabric runs). Harness: SPIN-29's `dyn_run` verbatim; canary suite carried forward **unchanged** — ALL PASS (see receipts below), including the STOP-gate canary c: Δ=12 baseline replayed s* = 17.6, C = 28.1 digit-for-digit vs SPIN-29.

## Headline table: α = C/(2·12), slope 1.6 spec, K=1, 5-seed means

| drift \ A | 96 | 200 | 400 |
|---|---|---|---|
| 0 | C=28.5, α=1.190 | C=27.4, α=1.142 | C=27.0, α=1.126 |
| 2 | C=28.6, α=1.190 | C=27.2, α=1.135 | C=26.7, α=1.114 |
| 6 | C=31.7, α=1.323 | C=28.1, α=1.172 | C=27.4, α=1.143 |
| 10 | C=33.6, α=1.398 | C=28.6, α=1.192 | C=27.6, α=1.152 |

## Fit vs both laws

- **2Δ law (C = 24):** every one of 12 arms measures C ∈ [26.7, 33.6]. Minimum miss = +2.7 (≈5.4 noise floors of ±0.5). **Rejected, permanently, with drift removed as the last candidate rescuer.**
- **2.38·Δ law (C = 28.56):** predicts all 8 arms at A ≥ 200 within ±1.9 (observed 26.7–28.6); fails only the A=96/drift≥6 corner (31.7, 33.6). The constant is real but carries a **weak negative log-band dependence** (≈ −2.1 per octave in C at drift=6, itself ≈ 8% per octave in α) and a **drift×small-band interaction** that only ignites when band amplitude ≲ 8×drift… i.e. when uncorrected drift wander is a nontrivial fraction of band width (A=96, drift 10: 96/10 = 9.6 ticks of band per unit drift).

## Pre-registered design (written BEFORE the run — unchanged)

- Δ=12 fixed, slope exactly 1.6 by SPEC (t_up = A·5/8), K=1, N=6 ladder, 4800 ticks, pd=3, seeds 1/7/42/1999/20260902, spread sweep 8..40 step 2 (17 pts). Arms: drift {0,2,6,10} × A {96,200,400}, full grid, Δ=12. Statistic: 50%-residency crossing by interpolation; C = s*·spec-slope. BAND_LO pinned 353 → bands [353,449], [353,553], [353,753].
- **Pre-registered deviation from brief (registered before any run):** brief said A ∈ {100,200,400}; A=100 is not integer-realizable at spec slope exactly 1.6 (t_up=62.5 non-integer; SPIN-21 scar: slope from SPEC, never sampled). Substituted A=96 (t_up=60, 96/60=1.600 exact). 4% band change on a 4.17× grid — no discrimination lost.
- **H1 validated iff** α(d0,A200) within 15% of 1.0 AND drift-range of α @A200 > 15%. **H2 validated iff** α within 15% of mean across all 12 arms. Else MIXED.
- Secondary fits: C vs drift @A200 (affine, α=1+c·drift/Δ); C vs A @drift=6 (const vs affine-in-log₂A).

## Canary receipts — ALL PASS (gate before any panel counted)

- (a) wiring byte-identity dyn_run(R0, Δ=12) vs `exp_glm1.run_fabric`: **16/16 configs**.
- (b) anchors exact: ladder15 K=1 pct **71.48** / ev **5791.6** / debt **106378.4**; zero K=1 pct **77.26** / debt **187833.6**.
- (c) **STOP-gate**: Δ=12 slope-1.6 baseline replay: s* = **17.6**, C = **28.1** — reproduced digit-for-digit vs SPIN-29 (tol 1.0). Did not stop.
- (d) determinism: **12 dual runs byte-identical**, one per (drift, band) arm — every arm in the grid covered (see Scars #2 for the count-vs-SPIN-29 note).

## Scars / honest boundaries (pre-registered items + post-run admissions)

1. *(pre-registered)* Arms whose 50% crossing fell outside 8..40 would be INCONCLUSIVE — none did; 12/12 crossed. No post-hoc widening performed.
2. *(admission)* Canary d ran 12 dual runs (one per arm) where SPIN-29 ran 30 across its 5-delta grid; the pre-registration text said "30 dual runs". Arm coverage is complete (every panel cell determinism-checked); per-arm multiplicity is lower. Logged, not rerun.
3. *(pre-registered)* drift=0 is a boundary arm — but its curves are clean (100→13% monotone-ish with the usual stair noise); no latency-starvation artifact like SPIN-29's Δ=8 appears.
4. The A=96 curves are the noisiest (e.g. drift=0: 48.3 at spread 18 then 61.6 at 20); the last digit of the A=96 C values carries ±1, not ±0.5. The α=1.398 corner could shrink somewhat under a finer spread grid, but it would have to shrink by >1.5 to re-enter H2's gate — unlikely to be pure interpolation noise.
5. The interaction reading (band-per-drift ratio) is post-hoc pattern-matching on 12 points — a hypothesis for the next spoke, not a validated mechanism.

## Next-spoke proposal

The constant's base is now pinned: C₀ ≈ 2.27–2.31·Δ, drift-independent, weakly band-dependent. Two live threads: (i) **why does α fall ~8%/octave with band amplitude?** — test A ∈ {400, 800, 1600} at drift=0, Δ=12 to chase the A→∞ limit (does α → a clean rational like 9/8 = 1.125?); (ii) **the A=96×drift corner** — map the interaction boundary with a fine A ∈ {60..160} × drift ∈ {6,10} grid. Either pins α's provenance or exposes the additive contamination SPIN-29 flagged at small Δ.

Status: **COMPLETE.** Committed and pushed to `g3-kinduction`. No sub-lanes spawned. WHEEL-LOG.md not appended (cron lane's job).
