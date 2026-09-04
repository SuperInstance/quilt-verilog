# SPIN-40 — METROLOGY (interaction spoke): the α(pd,Δ) surface — plane dead, sign-flip ridge real at pd_flip ≈ 4.1

**Spoke:** METROLOGY (spin 40, from SPIN-31's next-spoke proposal) · **Date:** 2026-09-04 01:43 AKDT
**Files:** `spin40_metrology_pddelta.py`, `spin40-output.txt` (elapsed 18 s, ~1,800 fabric runs incl. canaries). Instrument: `dyn_run` verbatim-imported from SPIN-29 (spin27's clone of spin21's canary-proven inline single-pass `run_fabric` arm), exactly as SPIN-31 imported it — re-proven byte-identical here across **both** knobs (pd ∈ {3,6} × Δ ∈ {8,20} corners). Integer-only in-loop; floats only at print/stat time; `python3 -u` direct redirect to a unique filename (SPIN-30 collision scar); no pipes.

## Pre-registration (written in script header BEFORE any run)

- **H1 (interaction plane):** α(pd,Δ) = a − b·pd − c·(Δ−12) fits all crossing cells with max |resid| ≤ 0.03. FALSIFY if any cell's residual exceeds 0.03 or no plane fits. Bilinear cross-term fit pre-registered as exploratory only — it cannot rescue H1.
- **H2 (sign-flip boundary):** the Δ-slope m(pd) = ∂α/∂Δ (linear fit within each pd column) is a monotone function of pd; fit m(pd) = m0 + m1·pd and state pd_flip = −m0/m1. FALSIFY if the sign flip is noise — bootstrap by seed: 5 single-seed α-grids recomputed from the same per-seed curves; the flip must hold (m(pd_min)<0<m(pd_max)) in a majority (≥3/5).
- **No-crossing cells:** reported as NO CROSSING, never extrapolated. **None occurred** — 20/20 cells crossed inside the 8..40 sweep.

Design: N=6 ladder, K=1, slope 1.6 from SPEC (A=200, T_up=125, exact 200/125 — SPIN-21 scar), grid pd ∈ {3,4,5,6} × Δ ∈ {8,10,12,16,20}, spread sweep 8..40 step 2 (SPIN-29's pre-widened sweep — the pd=3/Δ=20 knee at s*=29.7 would clip an 8..30 sweep), drift=6, ticks=4800, seeds 1/7/42/1999/20260902 (5-seed means + per-seed bootstrap), statistic = 50%-residency crossing by linear interpolation, C = s*·1.6, α = C/(2Δ).

## Canaries — ALL PASS (gate honored before any panel read)

- (a) wiring byte-identity vs `run_fabric`, pd×Δ corners: **16/16** configs.
- (b) anchors digit-exact (spin-10 semantics): ladder15 K=1 = 71.48 / ev 5791.6 / debt 106378.4; zero K=1 = 77.26 / ev 8756.4 / debt 187833.6.
- (c) SPIN-31 replays digit-exact: Δ=12 pd=3 s*=17.6 (target ~17.9 tol 1.0); α(pd=4/5/6) = 1.096/1.012/0.977 vs SPIN-31's booked table — **all within 0.000**. ⚠ The brief quoted 1.119/1.052/0.985 as the replay targets; those are NOT the values in SPIN-31's results table (they look like the spin-29 adjudicator's two-point interpolation predictions, slightly misquoted). Gated on the booked measured values — the strongest replay is digit-exact reproduction — and flagged here for audit.
- (d) determinism: 12 dual runs byte-identical (grid corners).

## Results — full C/α table (20/20 cells crossed; s* = 50%-crossing, C = s*·1.6, α = C/2Δ)

| pd\Δ | 8 | 10 | 12 | 16 | 20 |
|---|---|---|---|---|---|
| 3 | s* 12.5 · C 20.0 · **α 1.247** | 15.4 · 24.6 · **1.228** | 17.6 · 28.1 · **1.172** | 23.5 · 37.7 · **1.177** | 29.7 · 47.5 · **1.188** |
| 4 | 10.9 · 17.4 · **1.088** | 13.6 · 21.7 · **1.087** | 16.4 · 26.3 · **1.096** | 21.9 · 35.1 · **1.097** | 26.9 · 43.1 · **1.077** |
| 5 | 10.2 · 16.4 · **1.024** | 12.8 · 20.5 · **1.027** | 15.2 · 24.3 · **1.012** | 20.9 · 33.4 · **1.043** | 26.3 · 42.1 · **1.053** |
| 6 | 8.6 · 13.8 · **0.864** | 12.4 · 19.8 · **0.991** | 14.7 · 23.4 · **0.977** | 20.1 · 32.1 · **1.005** | 25.6 · 40.9 · **1.023** |

Full per-spread residency curves in `spin40-output.txt`. Every SPIN-31 and SPIN-29 cell replays digit-for-digit (α: 1.247/1.172/0.977/0.864/1.005 all reproduce).

### H1 — plane: **FALSIFIED** (pre-registered rule, verbatim)

Least-squares plane over all 20 cells: **α = 1.408 − 0.075·pd + 0.002·(Δ−12)** — the Δ coefficient is indistinguishable from zero, and max |resid| = **0.0878** (gate 0.03). Worst cells: pd=6/Δ=8 (−0.088), pd=3/Δ=8 (+0.071), pd=6/Δ=20 (+0.050). The exploratory bilinear (cross-term d·pd·Δ = **+0.0048**, the sign SPIN-31 demanded) improves things to max |resid| = 0.058 but **also fails the 0.03 gate**. Post-hoc curiosity (clearly labeled, not adjudicating): dropping the whole drift-contaminated Δ=8 column still leaves max |resid| = 0.059 — the failure is not just the Δ≈drift corner; the pd=3 column's low-Δ hump and the pd=6 rise are jointly non-planar at this noise level. No two-term plane carries the surface.

### H2 — sign-flip ridge: **VALIDATED** (5/5 seed-stable)

Per-column Δ-slopes m(pd) = ∂α/∂Δ (linear over each 5-point Δ arm):

| pd | 3 | 4 | 5 | 6 |
|---|---|---|---|---|
| m(pd) | **−0.0048** | −0.0006 | **+0.0027** | **+0.0101** |

m(pd) is strictly monotone. Fit: **m(pd) = −0.0198 + 0.0048·pd** → flip where m = 0:

> **pd_flip = 0.0198 / 0.0048 ≈ 4.12**

— i.e. below pd ≈ 4.1 the knee softens as Δ grows (α falls), above it the knee sharpens as Δ grows (α rises). Per-seed bootstrap: the flip sign pattern (m(3)<0<m(6)) holds in **5/5** single-seed replicates (m(3) ∈ [−0.0059, −0.0033], m(6) ∈ [+0.0087, +0.0114] — never near zero at the extremes). Not noise. Struck observation, not adjudicated: pd_flip ≈ 4.1 ≈ N − 2 at N=6; one N-arm (N=4, 8 ladders) would test whether the ridge sits at N−2 or is an N-free fabric constant.

## Verdicts (pre-registered decision rules applied verbatim)

- **H1: FALSIFIED** — max |resid| 0.088 > 0.03 gate; bilinear exploratory also fails (0.058).
- **H2: VALIDATED** — m(pd) monotone, pd_flip = 4.12 interior to the grid, 5/5 seed-stable.
- **Overall: MIXED** (one law falsified, one structural law validated on the same grid).

**Headline number: pd_flip ≈ 4.12** — the Δ-coupling sign-flip ridge sits between pd=4 and pd=5, with m(pd) = −0.0198 + 0.0048·pd. This is the wheel's first *two-axis* metrology law: α's Δ-dependence is set by where pd sits relative to ≈4.1, and the separable C = β·(2Δ)·g(pd) is now falsified in both directions (SPIN-31's D-gate, today's H1).

## Scars / honest boundaries

- **Brief canary mismatch:** the brief's α replay values (1.119/1.052/0.985) do not match SPIN-31's booked table (1.096/1.012/0.977); gated on the booked md values, all replays digit-exact. Future briefs should quote the booked numbers, not the adjudicator's predictions.
- Δ=8 cells carry the same drift-floor contamination SPIN-29/31 flagged (Δ ≈ drift = 6 territory); pd=6/Δ=8 (α 0.864) is the single worst plane residual and the pd=6/Δ=8 curve collapses to ~7% residency after spread 12 (knee at s*=8.6 near the sweep edge). But H1 fails even with Δ=8 excluded — the falsification does not rest on the contaminated corner.
- pd=4/Δ=8's curve has a cliff (25.1 → 7.3 between spreads 12→14); interpolated s*=10.9 there is stair-sensitive, ±0.5 floor applies.
- m(pd=3) itself (−0.0048/Δ) is small — the pd=3 column is a shallow valley (1.247 → 1.172 → 1.188), so its linear Δ-slope hides the low-Δ hump; the column max |resid| 0.036 says the *linear* m(3) is a summary, not a curve. The flip statement uses only m's SIGN at the extremes, which is 5/5 robust.
- Single slope (1.6), single N (6), single drift (6) — pd_flip's N- and drift-dependence unmeasured; m-coefficients are cell to this geometry.
- Post-hoc plane-refit-without-Δ=8 was run for diagnosis only, after the pre-registered verdicts were already computed and printed by the same script run.

## Next-spoke proposal

**Where does pd_flip come from?** Two arms, same harness, everything already parametrized: (i) **N-arm** — rebuild the grid's pd ∈ {3..6} × Δ ∈ {8,12,16} at N=4 and N=8 ladders (anchors re-derived per N; no-crossing guard on pd > N/2 wall) and re-fit pd_flip(N): if pd_flip ≈ N − 2 holds (4.1 ≈ 6−2), the ridge is the co-fire wall's shadow; if it pins at ~4.1, it's an N-free fabric constant. (ii) **drift-arm** — m(pd) at drift ∈ {2, 10} at Δ ∈ {12, 16}: if the ridge slides with drift, Δ enters the law only through Δ/drift, uniting this with SPIN-29's "α ≈ 1.19 plateau needs Δ ≳ 2·drift" reading. ~700 runs, ~10 s.

Status: **COMPLETE.** Not committed or pushed (per brief). WHEEL-LOG.md not appended (cron lane's job). No sub-lanes spawned.

— metrology lane (zai/glm-5.3), SPIN-40, 2026-09-04.
