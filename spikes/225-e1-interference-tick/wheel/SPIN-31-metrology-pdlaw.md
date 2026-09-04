# SPIN-31 — METROLOGY (pd-law spoke): α(pd) is linear at fixed Δ, but the law is pd×Δ-coupled

**Spoke:** METROLOGY (spin 31, from SPIN-29's expert adjudication next-step) · **Date:** 2026-09-03 18:46 AKDT
**Files:** `spin31_metrology_pdlaw.py`, `spin31-output.txt` (elapsed 5 s, ~630 fabric runs incl. canaries). Instrument: `dyn_run` — verbatim import of SPIN-29's canary-proven inline single-pass `run_fabric` clone (pd/delta/drift/k as parameters), re-proven byte-identical here **including the pd=6 leg** (pd is the swept knob). Integer-only in-loop; floats only at print/stat time; `python3 -u` direct redirect; unique output filename (SPIN-30 collision scar honored).

## Hypothesis (pre-registered in script header BEFORE any run)

From SPIN-29's adjudication: α=1.19 is a CELL reading (pd=3, Δ≥8), with measured endpoints α(pd=3)=1.172 and α(pd=6)=0.977 at Δ=12. Hypothesis: **C = β·(2Δ)·g(pd) with g linear in pd** — i.e. α(pd) = a + b·pd linear and decreasing. Alternative: α saturates in pd. Decision rule fixed before running: VALIDATE iff (L) max|linear-fit residual| ≤ 0.03 over pd∈{3,4,5,6}, AND (S) monotone decreasing, AND (D) at pd=6 α spread across Δ∈{8,12,16} ≤ 10% of mean; FALSIFY if nonlinear AND saturating (|α6−α5| ≤ 0.5·|α4−α3|); else MIXED / INCONCLUSIVE if any pd shows no crossing.

## Harness

N=6 ladder, K=1, slope 1.6 from SPEC (rational ramp A=200, T_up=125, exact 200/125 — SPIN-21 scar), spread sweep 8..30 step 2 (12 points, per brief; all predicted knees 8.6–17.6, no clipping), drift=6, ticks=4800, seeds 1/7/42/1999/20260902 (5-seed means). pd=2 skipped — no crossing already booked (N=6 co-fire wall). Arms: pd∈{3,4,5,6} @ Δ=12 + pd=6 replication @ Δ∈{8,16} (Δ=12 leg shared).

## Canaries — ALL PASS (gate honored before any panel read)

- (a) wiring byte-identity vs `run_fabric`, pd=3 AND pd=6 legs: **16/16** configs.
- (b) anchors exact (spin-10 semantics): ladder15 K=1 71.48/5791.6/106378.4; zero K=1 77.26/8756.4/187833.6 — all digit-exact including the events 8756 column.
- (c) Δ=12 pd=3 replay: s*=17.6, C=28.1 — reproduces SPIN-27/29 digit-for-digit.
- (d) determinism: 6 dual runs byte-identical (pd=4 and pd=6 cells).

## Results

### Leg 1 — pd sweep @ Δ=12 (headline table)

| pd | s* | C = s*·slope | α = C/2Δ | pred C (linear from adj. endpoints) |
|---|---|---|---|---|
| 3 | 17.6 | 28.1 | 1.172 | 28.1 |
| 4 | 16.4 | 26.3 | 1.096 | 26.6 |
| 5 | 15.2 | 24.3 | 1.012 | 25.0 |
| 6 | 14.7 | 23.4 | 0.977 | 23.4 |

Fit: **α(pd) = 1.365 − 0.067·pd**, max|resid| = 0.019 (gate 0.03) → **L PASS**. Strictly decreasing, b<0 as pre-predicted → **S PASS**. Every prediction within 0.7 of measured. Saturation test: |α6−α5| = 0.0346 vs 0.5·|α4−α3| = 0.0377 → marginally saturating (by 0.003 — inside last-digit noise), but moot given D below.

### Leg 2 — Δ replication at pd=6 (α Δ-stability)

| Δ | s* | C | α(pd=6) | pred C (α=0.977) |
|---|---|---|---|---|
| 8 | 8.6 | 13.8 | 0.864 | 15.6 |
| 12 | 14.7 | 23.4 | 0.977 | 23.4 |
| 16 | 20.1 | 32.1 | 1.005 | 31.3 |

Spread = **14.8%** (gate 10%) → **D FAIL**. The α(pd) shift is NOT Δ-stable: at pd=6, α rises with Δ (0.864→0.977→1.005).

## VERDICT: **MIXED** — pd-law linear but Δ-coupled (per pre-registered rule, no post-hoc amendment)

1. **Within a cell (fixed Δ), α is linear in pd to within noise.** α(pd) = 1.365 − 0.067·pd at Δ=12, four points, max residual 0.019, all endpoint-interpolated predictions landed ≤0.7. The adjudicator's two-point line survived four-point scrutiny at Δ=12.
2. **But C = β·(2Δ)·g(pd) with separable g is dead.** The pd=6 Δ-replication arm fails its gate: α(pd=6) is itself a Δ function. Worse, the coupling **flips sign across pd**: at pd=3 α RISES as Δ shrinks below 12 (1.172→1.247 at Δ=8, spin-29 adjudicator leg 2), while at pd=6 α FALLS as Δ shrinks (0.977→0.864 at Δ=8). A separable product cannot do that; α is a genuine function of **pd/Δ interaction** (plausibly of the ratio pd:Δ or the |1−N/pd| echo structure against the tolerance band).
3. **Headline number: α(pd,Δ=12) = 1.365 − 0.067·pd** (α: 1.172/1.096/1.012/0.977 at pd=3..6); the Δ-surface at pd=6 spans α 0.864→1.005 over Δ 8→16 (14.8% spread, 10% gate blown).
4. The pd=6 Δ=8 leg's curve is qualitatively different (collapse to ~7% residency by spread 12, no plateau above 50% after spread 10 — the knee at s*=8.6 sits at the sweep's edge region and carries wider uncertainty than the ±0.5 floor; flagged, not gating).

## Scars / honest boundaries

- The saturation test fired marginally (0.0346 ≤ 0.0377) but only by 0.003 — within the last-digit noise; per the pre-registered branch structure it never adjudicated (D failed first). Booked as "line vs saturation at pd=5→6 is unresolvable at this noise level," not as evidence of either.
- Δ=8 legs (both pd=3 and pd=6) sit near the drift/noise floor (Δ ≈ drift = 6 territory); α there is contaminated the same way SPIN-29 flagged. The sign-flip observation is robust (both directions are multi-point), but the exact Δ=8 values carry extra uncertainty.
- Single slope (1.6) and single N (6) by design; N must stay 6 to keep the anchors, so the N/pd wall structure cannot be separated here.
- Spread sweep 8..30 per brief, verified no clipping post hoc (all knees 8.6–20.1; the pd=6/Δ=16 knee at 20.1 is comfortably interior).

## Next-spoke proposal

**α as a two-variable surface: α(pd, Δ) full 2D grid.** pd∈{3,4,5,6} × Δ∈{8,12,16} (12 cells, ~1,020 runs, same harness, ~8 s). Pre-register two competing closed forms before running: (i) ratio law α = f(pd/Δ) — collapse test: does α depend only on pd/Δ? (pd=3,Δ=12) vs (pd=4,Δ=16) share ratio 0.25 → α should match 1.172 vs 1.005 measured — already looks refuted by today's data, so pre-register the sharper alternative; (ii) bilinear α = a + b·pd + c·Δ + d·pd·Δ (the sign flip demands the d·pd·Δ cross term; today's 7 measured cells already pin d<0). If bilinear fits all 12 cells within ±0.02, the law book gets its first two-parameter metrology entry: C = (a + b·pd + c·Δ + d·pd·Δ)·2Δ.

Status: **COMPLETE.** Not committed or pushed (per brief). WHEEL-LOG.md not appended (cron lane's job). No sub-lanes spawned.

— metrology lane (zai/glm-5.3), SPIN-31, 2026-09-03.
