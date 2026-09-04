# Tri-model review — SPIN-31 (pd-law) × SPIN-30 (drift-band) · opencode lane (engineering/verification)

Reviewer scope: harness/canary audit, regression spec, 2D grid design, weakest link. All numbers re-derived from `spin31-output.txt`, `spin30-output.txt`, `spin29-output.txt` line 35 (Δ=8 import), not from the spin prose.

---

## (a) Harness/canary audit — could the pd-law linear fit be an artifact?

**Verdict: the Δ=12 linearity (L PASS) is a chord, not a law — and the D FAIL (the headline coupling claim) is carried almost entirely by one validity-challenged cell.**

Coverage gaps in canaries:

1. **Anchors (canary b) run at pd=3 only**; byte-identity (canary a) covers pd=3 and pd=6 legs. pd=4/5 wiring is interpolated in parameter space, never differenced against `run_fabric`. Low risk (pd is a passed parameter), but unbooked.
2. **Canary c's replay tolerance (±1.0 in s*, ±1.5 in C ≈ ±0.063 in α) is 2× the L-gate it protects (0.03).** The suite certifies reproduction to a precision coarser than the effect under test; the tight gate leans entirely on the inherited "±0.5 in C" floor.
3. **That floor was established on pd=3-era curves and assumed pd-invariant.** Per-cell α floor from ±0.5 in C: 0.050 / 0.033 / 0.025 at Δ=8/12/16. pd=6 curves are steeper with shallower plateaus (different stair geometry) — SPIN-30's precedent (A=96 corner: ±1, not ±0.5) shows noisy arms do widen the floor. No re-estimation at pd≠3 was done.

Artifact channels in the fit itself:

4. **Gate below noise.** At Δ=12, single-cell α noise ≈ 1.6·0.5/24 = **0.033**; the L-gate is 0.03 and observed max|resid| = 0.019. A 4-point fit cannot exclude curvature of order the noise — and the data already contain the saturating tell: per-interval slopes 0.076 / 0.084 / **0.035** (last step halves; second differences −0.008, +0.049 — no interior curvature leverage, all discrimination is at extrapolation). "Linear" here means "not falsifiably nonlinear."
5. **Quantization vs. range.** One spread-grid step = α-quantum 0.133 at Δ=12; the entire measured pd-effect spans 0.195 ≈ 1.5 quanta. The whole law lives in sub-quantum interpolation of 5-seed-smoothed staircases — legitimate, but resolution claims are calibrated at one cell.
6. **Interpolation bias is pd-correlated (aggregation bias).** s* comes from linear interpolation across the bracket straddling 50%. Bracket widths at Δ=12: pd=3 → 12.7 pp, pd=4 → 33.0, pd=5 → 33.2, pd=6 → 25.0. Curve-shape-dependent interpolation bias therefore varies systematically across the pd arms at the ~0.1–0.3 s* level (≈0.007–0.02 in α) — same order as the 0.019 residuals. The residual budget contains an unmodeled systematic, not just seed noise.
7. **D FAIL is a one-cell result.** Spread at pd=6: 14.9% with Δ=8, **2.8% without it** (0.977→1.005). And the (6,8) cell is the worst-measured number in the spin: (i) knee s*=8.6 in the **leftmost bracket** [8,10] of the sweep; (ii) inside SPIN-29's explicitly flagged latency-starved zone ("spreads below ~10"); (iii) curve tops at 52.5% — **no >50% plateau exists**, so the 50%-crossing statistic's two-state premise fails; the "crossing" separates 52.5 from 44.7. Sensitivity: ±2 pp curve noise on that bracket → ±0.51 in s* → **±0.05 in α** — larger than the entire α(12)→α(8) drop it is measuring.
8. **Sign-flip mixes vintages.** The pd=3 leg of the flip (α=1.247 @ Δ=8) is imported from SPIN-29 (different sweep range 8..40, not replayed in this vintage; canary c replays only Δ=12/pd=3). The flip's *sign* is probably robust — a single Δ=8 bias mechanism cannot push 1.247 up and 0.864 down — but its magnitude, and hence "d<0"-class inferences, are not.
9. Arm weighting in Leg 1 is clean (Δ=12 pd=6 cell shared, not double-counted; same 5 seeds across arms = paired). The "pred C from adjusted endpoints" column is in-sample consistency of a 2-param line on 4 points — not independent corroboration.

SPIN-30 cross-check passes: its (drift=6, A=200) cell = α 1.172 matches SPIN-31's (3,12) digit-for-digit — the two surfaces intersect consistently.

---

## (b) Exact regression spec for the pd×Δ cross term

- **Response:** cell-level α = C/(2Δ). Secondary sanity: same spec on C (must yield the implied C-surface C = 2Δ·α̂ without refit drift).
- **Predictors (raw units, uncentered; report centered variant for interpretability only):** `1`, `pd`, `Δ`, `pd·Δ`. One pre-registered optional augmentation: `Δ²` (3 Δ levels make it estimable; declare before running or not at all — no post-hoc term shopping).
- **Estimator:** WLS, weights w ∝ (2Δ/σ_C)², i.e. w ∝ Δ² under the ±0.5-C floor, **with mandatory variance inflation ×4 on Δ=8 cells** (σ_C = 1.0 at edge arms, per SPIN-30 corner precedent) — or, better, per-cell σ̂ from per-seed crossings, which requires pre-registering a cross-then-mean statistic change plus a paired replay canary at (3,12) showing the two statistics agree within ±0.5 C.
- **Hypothesis:** H0: d = 0 (separable). HA: d ≠ 0 with **pre-registered point prediction d̂ = +0.0123** and sign **d > 0** (see erratum below). Flip locus implied: ∂α/∂Δ = c + d·pd changes sign at pd* = −c/d ≈ 4.6 — inside the measured range, consistent with the flip.
- **Decision bands:** (i) reject H0 iff 95% CI on d excludes 0 AND the effect-size floor holds: |d|·(Δpd range · ΔΔ range) = |d|·24 ≥ 2σ_α → |d| ≥ 0.0028; (ii) surface accepted iff max|WLS resid| ≤ 0.03 over all cells **and** the standing (6,12) residual (+0.0302 in today's 7-cell fit — the bilinear is already at its own gate before any new run) shrinks inside it; (iii) interior-only refit (Δ≥12 cells) must agree on d's sign, else the interaction is an Δ=8-edge effect and gets booked as artifact-suspect, not law.
- **Erratum to carry into pre-registration:** SPIN-31 next-spoke says "today's 7 cells already pin **d<0**." Arithmetic says otherwise: ∂α/∂Δ is −0.019 at pd=3 and +0.018 at pd=6, so d = (0.018−(−0.019))/3 ≈ **+0.015 > 0** (OLS on all 7 cells: d = +0.0123). If the next spoke inherits the wrong sign, a *confirming* run would be scored as falsified. Fix the registration text before running.

---

## (c) Minimal 2D grid with pre-registered kill bands

**Grid:** complete pd∈{3..6} × Δ∈{8,12,16}. 7 cells exist (incl. the SPIN-29 import), **5 new cells needed**: (3,16), (4,8), (4,16), (5,8), (5,16) ≈ 300 runs; plus one **pd=7 @ Δ=12 extrapolation leg** (60 runs) for the linearity-vs-saturation question (cheapest curvature test: all interior leverage is spent; separation of predictions 0.896 vs ~0.957 ≈ 2 noise floors). Same harness/seeds/sweep 8..30 (all predicted knees 8.6–21.8 interior; auto-INCONCLUSIVE any knee within one grid step of a boundary). Re-measure **(3,8) in-vintage** to break the cross-vintage dependency. Extend determinism canary to one Δ=8 and one pd∈{4,5} cell.

**Pre-registered predictions from the 7-cell bilinear (α = 2.069 − 0.222·pd − 0.056·Δ + 0.0123·pd·Δ):**

| new cell | pred α | kill band |
|---|---|---|
| (3,16) | 1.090 | ±0.033 |
| (4,16) | 1.065 | ±0.033 |
| (5,16) | 1.039 | ±0.033 |
| (4,8)  | 1.122 | ±0.050 (advisory†) |
| (5,8)  | 0.999 | ±0.050 (advisory†) |
| pd=7 @ Δ=12 | 0.896 (linear) | kill linear iff dev > 0.066 |

† Δ=8 cells sit at the drift/latency floor (SPIN-29/31 both flag); advisory for law-fitting, primary only for sign/flip questions.

**Formal gates:** (i) **ratio law** f(pd/Δ): the grid contains exactly three degenerate pairs — (3,12)/(4,16)=0.25, (4,8)/(6,12)=0.5, (3,8)/(6,16)=0.375. Kill if any pair splits > 0.066 (2 floors); the third pair is already split 0.242, so this is a confirmation gate. (ii) **Bilinear surface**: kill if max|resid| > 0.03 at ≥2 cells, or d's CI spans 0, or interior-only refit flips d's sign. (iii) **pd=7 leg**: as tabled. (iv) d sign fixed at **> 0** per (b) erratum.

---

## (d) Weakest link

**The (6,8) cell.** The spin's headline claim — "α is pd×Δ-coupled, sign flips with pd" — rests on the single worst-measured number in the experiment: a knee interpolated in the leftmost bracket of the sweep, inside the flagged latency-starved zone, on a curve with no >50% plateau (statistic premise failure), carrying ±0.05 α-uncertainty (larger than the effect it anchors), and paired against a cross-vintage import (1.247) never replayed in this harness vintage. Remove that one cell and D flips from FAIL (14.9%) to comfortable PASS (2.8%); the MIXED verdict and the entire next-spoke motivation survive or die on it. The fix is cheap: in-vintage re-measurement of (3,8) and (6,8) with a wider sweep (start spread ≤4) is the highest-information run in the whole proposed grid. Secondary weak link: the pd-invariance of the ±0.5-C noise floor — every gate in both spins is denominated in a unit validated only at pd=3, and SPIN-30's A=96 corner already demonstrated the floor widens on noisy arms. Tertiary: the d<0 pre-registration erratum, which would corrupt the next spoke's scoring if inherited.
