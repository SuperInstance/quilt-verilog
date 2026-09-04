# SPIN-32 — METROLOGY (2D-grid spoke): the α(pd,Δ) surface — M2 leads AIC but NO SINGLE SURFACE passes; Δ-coupling replicated; hard wall-side curvature found

**VERDICT (pre-registered gates): NO SINGLE SURFACE (within reach).** The 20-arm grid ran clean (all canaries pass, incl. STOP-gate digit-for-digit), and the model competition's pre-registered closure rule refused both gates: **W1 FAIL** — M2 (bilinear-with-cross) is the AIC winner (−137.42) but beats runner-up M4 (Δ-blind saturation knee, −131.13) by only **dAIC = 6.29 < 10**; **W2 FAIL** — leave-one-arm-out error exceeds 2·NF on 19/20 arms for M2 (best of all models: M4 at 4/20, gate ≥ 16/20). The LOO failure is itself the finding: the seed noise floor (median NF = 0.005) is 4–10× smaller than the surface's systematic structure (LOO errors 0.02–0.12; M2 max|resid| 0.061) — **seed spread and surface fidelity are different currencies, and the grid earned its refusal honestly.** The simple version, stated here because it is the test: AIC and LOO split because AIC ranks members *within* the family while LOO asks whether any member generalizes; since the systematic residual is 4–10× seed noise, the leftover structure is real, not under-powered sampling — **the true α(pd,Δ) response is not in the family {M1..M4}.** Operationally: no formula in this family predicts the knee; you measure α per cell. Delivered as partial (see Payoff): the best-fit bilinear with ±0.06 honest error bars, NOT law-book grade. Secondary pre-registered gates: SPIN-31's Δ-coupling **REPLICATED** (pd=6 column range 14.1%, real, though not monotone — Δ=10 bump); pd=6 endpoint **LINEAR-CONTINUES** at both Δ (no saturation knee at the pd=6 edge); pd=3 endpoint **CURVES hard into the wall** (second difference −0.274 = 27× gate at Δ=16) — and the wall's reach is Δ-dependent (pd=2.5 crosses at Δ=16, dead at Δ=8).

**Files:** `spin32_grid2d.py`, `spin32-output.txt` (elapsed 12 s, ~1,300 fabric runs incl. canaries). Instrument: `dyn_run` verbatim (SPIN-29 lineage) + **new `dyn_run_r`** — rational-pd generalization of the pulse divider (m = pdd·|e| // pdn), canary-e-gated at the integer reduction. Integer-only in-loop; floats only at print/stat time; `python3 -u` direct redirect; unique filename.

## Provenance ledger (crash recovery, nothing lost)

1. **Pre-registration committed BEFORE any run:** c0779e4 (2026-09-03 18:58:39) — full design, M1–M4 formulas, AIC/LOO gates, probes, payoff form, scars, all in the script header, verbatim in git history.
2. Canary-e caught an **inverted divider** in `dyn_run_r` (pd is a divisor); fixed and committed **before any panel data existed** (552fd09, "no panel data seen").
3. Run 1 (18:59:26): canaries + both panels completed, then **crashed in analysis** (`fit_m4`: p0=3.0 knee column collinear → singular OLS → None). Three analysis-path fixes committed (c44c951): None-guard in `fit_m4`, tuple-unpack bug in the LOO loop, payoff closure-status keyed to the DECLARED verdict per pre-reg text (was keying off AIC order alone). **All display/stat-side; no fabric semantics touched.**
4. Run 2 (19:06:51): complete, exit 0. **Canaries + panels byte-identical across runs** (diff receipt kept; determinism canary d + identical seeds). Only the timestamp and the post-crash analysis differ.

## Pre-registration (as committed in c0779e4 — summary)

Grid pd∈{3,4,5,6} × Δ∈{8,10,12,14,16} = 20 arms, 3 seeds/arm (1/7/42; per-seed crossings → per-arm NF = half the seed range — the directive's noise-floor deliverable). Sweep 8..30 step 2, K=1, N=6, slope 1.6 from SPEC, drift=6, ticks=4800. Curvature probes: corners pd∈{3,6} × Δ∈{8,16} with rational pd 2.5/2.75/3.5 and 5.5/5.75/6.5 (`dyn_run_r`); wall-adjacent no-crossing pre-booked as wall-location data. Canaries unchanged from SPIN-29 suite incl. STOP-gate (s*→17.6, C→28.1 digit-for-digit) + determinism one dual per arm. Models: M1 a+b·pd+c·Δ; M2 +d·pd·Δ; M3 (a+b·pd)(e+f·Δ) (M2's span minus 1 dof); M4 a+b·pd+s·max(0,pd−p0), p0 on {3.0..5.75 step 0.25} (Δ-blind by directive formula — a control). WINNER iff dAIC≥10 vs runner-up AND LOO |err|≤2·NF on ≥80% of arms; else NO SINGLE SURFACE. Replication gate: pd=6 Δ-column range vs 2·medianNF, monotone-rising expectation. Curvature gate: |2nd difference| vs 2·medianNF.

## Canary receipts — ALL PASS (gate before any panel read)

- (a) wiring byte-identity vs `exp_glm1.run_fabric`, pd=3 AND pd=6 legs: **16/16**.
- (b) anchors digit-exact: ladder15 71.48/5791.6/106378.4; zero 77.26/8756.4/187833.6.
- (c) **STOP-gate**: Δ=12 pd=3 replay s\*=17.577→17.6, C=28.124→28.1 — digit-for-digit.
- (d) determinism: **22 dual runs byte-identical** (one per grid arm + 2 probe arms).
- (e) `dyn_run_r`(3/1) == `dyn_run`(3): **8/8** configs.

## Results

### PANEL 1 — 20-arm grid (α = C/2Δ, 3-seed means; full table in output)

α surface: pd=3 row 1.247/1.230/1.173/**1.201**/1.176 (Δ=8..16 — Δ=14 breaks Δ-monotonicity); pd=4 row flat 1.075–1.098; pd=5 row flat 1.012–1.043; pd=6 row 0.868/0.991/0.977/0.984/1.005. Median NF = **0.005**; worst arm (6,8) NF = 0.024. The two prior-vintage anchors reproduce in-vintage: (3,12)=1.173, (6,12)=0.977, (3,8)=1.247 — the SPIN-29 cross-vintage import is now re-measured in this vintage, **resolving opencode's cross-vintage critique**.

### ANALYSIS 1 — model competition (n=20, response = arm-mean α)

| model | SSE | maxres | AIC | BIC |
|---|---|---|---|---|
| M2 bilinear-with-cross | 0.0126 | 0.061 | **−137.42** | **−132.44** |
| M4 saturation-knee (Δ-blind) | 0.0172 | 0.096 | −131.13 | −126.15 |
| M1 bilinear-no-cross | 0.0214 | 0.079 | −128.81 | −124.83 |
| M3 separable-product | 0.0633 | 0.138 | −105.10 | −100.12 |

W1: dAIC = 6.29 < 10 → FAIL. W2: M2 LOO 1/20, best-of-four M4 4/20 vs gate 16/20 → FAIL. **MODEL VERDICT: NO SINGLE SURFACE.** Best partial (M2): **α = 1.7625 − 0.15805·pd − 0.02819·Δ + 0.006635·pd·Δ** — cross term d > 0 (opencode's erratum vs SPIN-31's "d<0" confirmed on 20 cells), flip locus ∂α/∂Δ = 0 at pd\* = 4.25. **What pd\* = 4.25 means physically:** the fabric's pd is integer (measured endpoints 3 and 6; SPIN-32's curvature probes add rational pd via `dyn_run_r`, but production cells come in whole numbers) — so a fractional pd\* is NOT a parameter estimate of any real cell's behavior. It is the **interpolated location of a regime boundary**: pd=3 curves hard into the wall (α rising with Δ), pd=6 continues linear (α falling with Δ), and 4.25 is where the bilinear says the sign of ∂α/∂Δ flips *between* those regimes. The claim to carry forward is "the crossover between the wall-curving and linear-continuing regimes interpolates near pd ≈ 4.25 on this grid," with error bars from the fit surface only — its per-cell predictive error is unvalidated (that is what W2 refused), so the boundary's width is unknown until an arm lands near 4.25 (e.g. rational-pd probes at 4.0/4.5) or an integer cell pair brackets it. Residual structure is NOT white: row-mean residuals run −0.017/+0.022/+0.007/−0.012 across pd = 3/4/5/6 — a concave-in-pd pattern peaking near pd ≈ 4.3, coincidentally at the flip locus; single biggest residual (6,10) = −0.061. The pre-registered NF (seed spread) does not denominate this scale — the gates correctly refused closure rather than letting a bilinear pass on the wrong error currency.

### ANALYSIS 2 — SPIN-31 replication gate

pd=6 column: range 0.136 = **14.1% of mean** (SPIN-31: 14.8%) ≫ gate 2·NF=0.010 → **REAL, survives seed replication**. Pre-registered monotone-rising expectation: **NO** — the Δ=10 cell (0.991) sits above Δ=12 (0.977). The coupling is real but its Δ-profile wobbles at the ~0.02 systematic scale, above seed noise.

### ANALYSIS 3 — endpoint curvature probes

- **pd=3, Δ=16: CURVES** — α(2.5)=0.951, α(3)=1.176, α(3.5)=1.128 → 2nd difference **−0.274 vs gate 0.010 (27×)**. But the drop sits 0.5 above the no-crossing wall (pd=2): this is wall-adjacent pull, pre-booked as wall-location data, not smooth-surface curvature. At Δ=8, pd=2.5 shows **NO CROSSING** — the wall's reach grows as Δ shrinks. (Quarter-point 2.75 is seed-unstable at Δ=16: per-seed 1.317/1.194/1.194.)
- **pd=6: LINEAR-CONTINUES at both Δ** (2nd diffs −0.008, +0.004 vs gate 0.010) — no saturation knee at the pd=6 edge; SPIN-31's marginal saturation tell did not extrapolate.

### ANALYSIS 4 — payoff (partial, honestly gated)

Candidate closed form at A=200, drift=6, N=6, K=1, slope 1.6: **C(pd,Δ) = 2Δ·(1.7625 − 0.15805·pd − 0.02819·Δ + 0.006635·pd·Δ), max error ±0.06 over the grid — engineering approximation, NOT law-book grade.** Joint partial law: C(pd,Δ,A,drift) ≈ 2Δ·α̂_M2(pd,Δ) + 0.138·(drift−6) − 2.11·log₂(A/200), validity A≥200, drift∈[0,10], pd∈[2.5,6.5] excluding wall-adjacent cells, Δ∈[8,16]; A/drift corrections measured at (pd=3, Δ=12) only — cross-pd validity untested, flagged; A=96×drift≥6 ignition corner outside (SPIN-30).

## Reconciliation with tri-model reviews (read only after pre-reg commit; priming ledger included)

- **kimi.md** (read by this operator during the SPIN-31 council round, i.e. BEFORE this assignment — **booked as priming**; its design overlap with this grid is unavoidable: SPIN-31's own next-spoke proposed the grid, and the foreman directive fixed the design). Its 7-cell refit α = 2.069−0.222·pd−0.056·Δ+0.0123·pd·Δ **is killed by this grid**: (3,16) predicted 1.092±0.033, measured 1.176 (2.5 kill-bands); its surface gate (max|resid| ≤ 0.04) fails at 0.061; its cross-term floor (|d| ≥ 0.006) survives by 11% (d = 0.006635, same sign). The 7-cell bilinear was a tangent, not the surface — the fuller grid halved d and moved pd\* from 4.6 to 4.25.
- **opencode.md** (written 19:02, after the pre-reg commit — no priming possible): its **d>0 erratum is confirmed** (had SPIN-32 inherited "d<0", a confirming run would have scored falsified — the erratum was load-bearing). Its kill bands: (3,16) **killed** (1.090±0.033 vs 1.176), (4,16) marginal (+0.033 vs ±0.033), (5,16)/(4,8)/(5,8) pass. Its weakest-link call — **the (6,8) cell** — is carried and confirmed: worst NF in the grid (0.024), knee in the leftmost bracket, no >50% plateau; its proposed fix (re-measure (6,8) with sweep start ≤4) was NOT in this design and remains the top next-spoke item. Its predicted pd-correlated interpolation bias (0.007–0.02 in α) matches the observed systematic scale — the LOO refusal is that bias plus real structure, exactly as it forecast. Its pd=7@Δ=12 extrapolation leg was not run (probes capped at 6.5) — booked as a gap.
- **claude.md does not exist** — claude-run.log shows a launch failure (stdin/prompt error). Its resonance/superposition reading remains unreviewed; the council-round discriminator (this operator, priming booked) resolved at (5,16): saddle predicted 1.047±0.04, measured **1.043** (hit; no lobe ≥ 0.07). The wall-side curvature at pd=2.5 was outside that probe and is open mechanism-wise (wall pull vs commensurability lobe near the wall).

## Scars / honest boundaries

1. The (6,8) cell — this grid's weakest number, carried from SPIN-31 (opencode's item): knee s\*=8.7 in the leftmost bracket, latency-starved zone, no >50% plateau, NF 0.024. The sweep was NOT widened down (brief-pinned 8..30); removing (6,8) would not rescue any model's gates, so the verdict is robust to it.
2. NF (seed spread) under-measures the effective noise: row-mean residual structure 0.01–0.02 and LOO errors 0.02–0.12 sit above seed noise by 4–10×. Every 2·NF gate in this spin is denominated in the tight currency; a future gate needs σ_sys measured (disjoint seed-triples), not assumed.
3. M4 is Δ-blind by the directive's formula — its runner-up AIC reflects the pd-direction dominance, not Δ-explanatory power; it functions as the saturation-control and nothing more.
4. Canary a covers pd∈{3,6} wiring; pd∈{4,5} legs remain parameter-interpolated (opencode item 1, low risk, unbooked until now). The Δ² augmentation was not declared in the pre-reg, so it was correctly never tested (opencode item: declare-or-don't).
5. Rational-pd instrument is canary-gated only at the integer reduction; non-integer pd inherits the divider's correctness by construction (m = pdd·|e|//pdn), not by external differencing. 23/4@Δ=8 returned per-seed alphas identical to pd=6's — consistent with floor quantization, noted.
6. Single slope/N/drift/band by design; A/drift/N corrections ride on SPIN-30's (pd=3, Δ=12) provenance only.
7. Run-1 crash history is part of the record (ledger above); no panel was ever computed under unfixed analysis code.

## Next-spoke proposal

Three items, cheapest-information first: (i) **fix the weakest cell and the noise currency** — re-measure (3,8)/(6,8) with sweep start ≤4, and split σ_seed vs σ_sys with disjoint seed-triples per arm (~250 runs) so the next competition's gates are denominated honestly; (ii) **fine rational-pd scan at Δ=12** — pd ∈ {2.75..6.5} step 0.25 plus the pd=7 extrapolation leg (`dyn_run_r` is now proven; ~450 runs) to resolve the concave residual pattern peaking near pd\*≈4.3 and the line-vs-saturation question in one pass; (iii) **wall-reach mapping** — pd ∈ {2.25..3.0} × Δ ∈ {8,10,12,16} crossing/no-crossing boundary (~200 runs), converting the pre-booked wall deaths into a located wall(Δ) curve.

Status: **COMPLETE.** Committed and pushed to `g3-kinduction`. WHEEL-LOG.md not appended (cron lane's job). No sub-lanes spawned.

— metrology lane (zai/glm-5.3, foreman: Lucineer), SPIN-32, 2026-09-03.
