# SPIN-29 — METROLOGY (C = f(Δ) spoke): the knee constant is ~2.38·Δ, not 2Δ

**Spoke:** METROLOGY (spin 29, dispatched from SPIN-27's next-spoke proposal) · **Date:** 2026-09-03 17:32 AKDT
**Files:** `spin29_metrology_cdelta.py`, `spin29-output.txt` (elapsed 6 s, ~590 fabric runs). Instrument: `dyn_run` — verbatim clone of SPIN-27's clone of SPIN-21's canary-proven inline single-pass `run_fabric` interference arm (reality_fn/k/**delta** as parameters), re-proven byte-identical here (16/16 configs). Integer-only in-loop; floats only at print/stat time; single-pass inline (no chunked re-sim — SPIN-16 LCG-reset scar); `python3 -u` direct redirect, no pipes.

## Hypothesis (pre-registered in script header before any panel run)

C(Δ) = s*·slope ≈ α·2Δ with α constant ≈ 1.192 (= 28.6/24 from SPIN-27). Falsify if C(Δ) is not linear in Δ, or if α varies >15% across the Δ grid. Secondary: fit C(Δ) to {linear-through-origin, affine, 2Δ + const}.

## Harness

Δ ∈ {8, 10, 12, 16, 20}, slope pinned at 1.6 (integer rational ramp A=200, T_up=125 — **spec slope exactly 200/125 = 1.600**, SPIN-21 scar honored: slope from SPEC, never sampled). N=6 ladder, spread sweep 8..40 step 2 (17 points), K=1 primary + K=2 continuity column at Δ=12; seeds 1/7/42/1999/20260902 (5-seed means); 4800 ticks; drift=6, pd=3. Statistic: 50%-residency crossing by linear interpolation (SPIN-21/27).

**Pre-registered deviation from brief:** sweep widened 8..40 (brief said 8..30) because at Δ=20 the prediction puts s*≈29.8 — an 8..30 sweep would have clipped the knee exactly as s0.8 clipped SPIN-27. Widened BEFORE any run, symmetric across all Δ.

## Canaries — ALL PASS

- (a) wiring byte-identity vs `exp_glm1.run_fabric` (Δ=12 leg): **16/16** configs.
- (b) anchors exact: ladder15 K=1 pct 71.48/ev 5791.6/debt 106378.4 (=71.5/5792/106378); zero K=1 pct 77.26/debt 187833.6 (=77.3/187834).
- (c) Δ=12 slope-1.6 replay of SPIN-27: s* = **17.6** (SPIN-27 measured 17.6, prediction 17.9; tol 1.0), C = 28.1 — reproduced digit-for-digit.
- (d) determinism: 30 dual runs byte-identical across all five Δ.

## Results

### Headline: C(Δ) = s*·slope, α = C/(2Δ), slope 1.6, K=1

| Δ | s* | **C = s*·slope** | α = C/2Δ | predicted C (α=1.192) |
|---|---|---|---|---|
| 8 | 12.5 | **20.0** | 1.247 | 19.1 |
| 10 | 15.4 | **24.6** | 1.228 | 23.8 |
| 12 | 17.6 | **28.1** | 1.172 | 28.6 |
| 16 | 23.5 | **37.7** | 1.177 | 38.1 |
| 20 | 29.7 | **47.5** | 1.188 | 47.7 |

α range = **6.3%** of mean α (falsifier was >15%) — far inside the gate. C is decisively linear in Δ (max affine residual 0.69, gate 1.5, noise floor ~0.5). K=2@Δ12: s*=17.8, C=28.6 — K-independent, matching SPIN-27.

### Secondary fits

| form | best fit | SSE | max resid | note |
|---|---|---|---|---|
| through-origin | **C = 2.381·Δ** | 1.80 | 0.90 | implied α = 1.191 — dead on SPIN-27 |
| affine (winner by SSE) | C = 1.35 + 2.289·Δ | 0.93 | 0.69 | intercept 1.35 ≈ noise floor; not separable |
| 2Δ + const | C = 2Δ + 5.16 | 8.69 | 2.35 | **rejected** — slope ≠ 2 |

The clean 2Δ law is **dead permanently**: fixing the slope at exactly 2 gives residuals 5× the noise floor. The through-origin slope 2.381 and the affine slope 2.289 bracket the truth; with intercept indistinguishable from zero, the parsimonious reading is **C ≈ 2.38·Δ (α ≈ 1.19)**.

## VERDICT: **VALIDATED** — C = f(Δ), linear, C ≈ 2.38·Δ

1. **C is set by Δ.** Five-point grid, 2.5× range of Δ, α holds within 6.3%. The SPIN-27 constant 28.6 was no accident of one delta — it is α·2·12 with α ≈ 1.19.
2. **The constant is α ≈ 1.19, not 1.** Every candidate "clean" story that returns the prefactor to 1 is falsified: 2Δ is out (resid 2.35 max), and the affine intercept is within noise of zero while its slope is 2.29, not 2.
3. **Δ=8 is the only mild outlier** (α = 1.247, +5% off mean) — at Δ=8 the knee (s*=12.5) sits close to the drift/noise floor of the grammar (spreads below ~10 are latency-starved), so a small additive contamination would show exactly this sign. Not falsifying (inside 15% gate) but flagged: if C has a tiny additive term, it shows up at small Δ.
4. **K-independence confirmed again** (28.6 vs 28.1 at Δ=12): the constant is fabric×trace geometry, not pulse lifetime.

## Scars / honest boundaries

- Spread sweep widened beyond the brief's 8..30 to 8..40 — pre-registered in the script header with rationale, but it IS a deviation from the task text; noted here so WHEEL-LOG can audit it.
- Curves are stair-noisy at large spreads (e.g. Δ=12 has a nonmonotonic 28.0→34.4 wiggle at spread 24–26); the interpolation statistic averages through it but the last digit of every C carries ±0.5.
- α's gentle downward drift with Δ (1.247→1.188) is consistent with either a small positive affine intercept or small-Δ contamination; the two fit forms cannot be separated at this noise level. One more delta near 6 would split them — but Δ=6 is within 2·drift of the fabric's noise floor, so the experiment may be unbuildable.
- Single slope (1.6) by design; C's slope-dependence is assumed nil from SPIN-27's hyperbola (products flat across 0.8–2.4 at Δ=12) but not re-tested here.

## Next-spoke proposal

**Where does α ≈ 1.19 come from?** Remaining free parameters in the geometry: drift (6) and band amplitude (A=200). Two-arm spoke: (i) drift sweep {2, 6, 10} at Δ=12, slope 1.6 — if α moves with drift, α = 1 + f(drift/Δ) and a floor of drift=0 (α→1?) restores 2Δ; (ii) band-amplitude sweep A ∈ {100, 200, 400} at fixed Δ=12 — tests whether α carries band dependence (SPIN-27 already suspected "geometry (band + Δ + drift)"). ~120 fabric runs, same harness, delta/drift/band all already parametrized. Either α collapses to 1 at drift→0 (the 2Δ law returns with drift as its violator) or α is a genuine fabric constant and the law is C = 2.38·Δ, full stop.

Status: **COMPLETE.** Not committed or pushed (per brief). WHEEL-LOG.md not appended (cron lane's job). No sub-lanes spawned.
