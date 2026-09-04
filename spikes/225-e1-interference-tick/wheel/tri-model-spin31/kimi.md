# SPIN-31 review — spatial / structural-math lens (kimi)

Reviewed: `SPIN-31-metrology-pdlaw.md`, `SPIN-30-drift-band.md`. Recomputed all fits from the 7 published cells. No files touched except this one.

## (a) α(pd) = 1.365 − 0.067·pd: chord, not law — and the cheapest curvature test

**Verdict: a chord through unresolved curvature.** Three structural reasons:

- **The gate is tighter than the noise it measures.** Single-cell α noise = 1.6·(±0.5)/(2Δ) = **±0.033** at Δ=12, and the underlying crossing statistic is quantized in spread steps of 2 → α-quantum 0.133. The pre-registered residual gate (0.03) sits *below* the per-cell noise floor. "L PASS at max|resid| = 0.019" therefore means only that 5-seed averaging suppressed the stair noise — it cannot exclude curvature of order the noise, which is exactly the curvature scale that matters here.
- **Interior second differences carry no signal.** From the Δ=12 column: α₃−2α₄+α₅ = **−0.008**, α₄−2α₅+α₆ = **+0.049**. Inconsistent sign, magnitude ≈ noise → zero interior curvature leverage. All discriminating power lives in extrapolation, by construction of any 4-point near-collinear set.
- **The saturation tell is already in the data.** Per-interval slopes: 0.076, 0.084, **0.035**. The last interval halves — the marginal saturation gate fired (0.0346 ≤ 0.0377) for a real geometric reason, not noise pathology. A convex/saturating curve and a line are indistinguishable on pd∈{3..6} at this noise level.

**Cheapest endpoint test: one leg at pd=7, Δ=12** (12 spread points × 5 seeds ≈ 60 runs, same harness, no new code).
- Pre-register: line predicts α(7) = **0.896**; kill the linear law iff |α₇_measured − 0.896| > 0.066 (2 noise floors).
- The saturation branch, extrapolating the halved terminal slope, predicts ≈ 0.94–0.96 — separation from the line is only ~0.06, marginal. If pd=7 lands in the dead zone, extend to **pd=8** (line: 0.829; saturation: ~0.93; separation 0.10, clean) — same cost per leg. Do not waste runs refining interior points; they have no curvature leverage.

## (b) The pd×Δ sign flip: mechanism and closed form

**First, a correction to SPIN-31:** the report claims "today's 7 measured cells already pin **d<0**." Recomputing the bilinear least-squares fit on exactly those 7 cells:

```
α(pd,Δ) = 2.069 − 0.222·pd − 0.056·Δ + 0.0123·pd·Δ     max|resid| = 0.030
```

**d is positive.** It has to be: ∂α/∂Δ = c + d·pd goes from −0.019 (pd=3) to +0.018 (pd=6), i.e. *increases* with pd. The report's mechanism claim survives; its sign convention does not. Flip locus: ∂α/∂Δ = 0 at **pd\* = −c/d ≈ 4.6**.

**Mechanism (two-comb beat).** The fabric has two intrinsic clocks: the dial comb (period pd ticks between ladder co-fires) and the band-crossing comb (the ramp at slope 1.6 traverses the tolerance Δ in Δ/1.6 ticks; with N=6 sharing corrections, the per-node excursion per dial period is 1.6·pd/6). K=1 quantizes every correction to a single click, so the fabric can only resolve these clocks through their **aliasing against each other** — the interference tick. Two regimes:

- **pd small (fast dial vs band):** clicks arrive faster than the band can be traversed; each click overshoots the fractional demand (quantum K=1 vs needed increment < 1), and shrinking Δ *worsens* efficiency — the overshoot waste is spent inside an ever-narrower band. α rises as Δ shrinks. This is pd=3 (α: 1.172 → 1.247 as Δ: 12 → 8).
- **pd large (dial period ≳ band traversal):** a full ladder cycle resolves inside one band residence; clicks space out to match demand, and shrinking Δ now *helps* — the capture window tightens while supply stays uniform. α falls as Δ shrinks. This is pd=6 (α: 0.977 → 0.864 as Δ: 12 → 8).

The crossover pd\* ≈ 4.6 sits where the dial period ≈ band traversal time at Δ=12 (Δ/1.6 = 7.5 ticks vs N-shared effective period) — i.e. the flip is a **clock-commensurability boundary**, not a new parameter.

**Closed form implied:** α is a ruled (hyperbolic-paraboloid) surface,

```
α(pd,Δ) = a + b·pd + d·(pd − pd*)·Δ ,   pd* ≈ 4.6, d ≈ +0.012
```

fitted: α = 2.069 − 0.222·pd − 0.056·Δ + 0.0123·pd·Δ. Any pure ratio law f(pd/Δ) is already dead on today's data ((3,8) and (6,16) share pd/Δ = 0.375 but α = 1.247 vs 1.005 — a 0.24 split at 7× noise). The bilinear is the minimal form with a sign-flipping cross derivative; whether the true surface is exactly bilinear or merely its tangent expansion is what the grid in (c) decides.

## (c) Minimal 2D grid with pre-registered kill bands

Grid pd∈{3,4,5,6} × Δ∈{8,12,16} = 12 cells; **7 already measured**, so the minimal buy is **5 new legs ≈ 300 runs**: (3,16), (4,8), (4,16), (5,8), (5,16). A useful coincidence: the grid contains exactly three ratio-degenerate pairs, so the ratio law gets a formal three-shot execution for free.

**Pre-registered predictions (bilinear fit above) and kill bands** — kill the bilinear surface if any new cell misses its band:

| cell | predicted α | kill band |
|---|---|---|
| (3,16) | 1.092 | ±0.033 |
| (4,8)  | 1.123 | ±0.050 † |
| (4,16) | 1.067 | ±0.033 |
| (5,8)  | 1.000 | ±0.050 † |
| (5,16) | 1.042 | ±0.033 |

† Δ=8 cells sit at the Δ≈drift=6 contamination floor (SPIN-29/31 both flagged); widen bands to ±0.05 and mark advisory, or the whole grid inherits the floor's bias.

**Ratio-law kill (formal):** kill f(pd/Δ) if any degenerate pair splits by > 0.066: (4,16) vs (3,12)=1.172; (4,8) vs (6,12)=0.977; (3,8)=1.247 vs (6,16)=1.005 — the third pair is *already* split by 0.242, so this is a confirmation gate, not a discovery gate.

**Cross-term gate:** refit bilinear on all 12; kill if d's sign flips or |d| < 0.006 (half the current estimate → flip not robust); kill the *surface* if max|resid| over 12 cells > 0.04. Note the current 7-cell fit already shows resid 0.030 at (6,12) — the bilinear is at the edge of its own gate before a single new run; the 5 new cells are genuinely discriminating, not ceremonial.

## (d) Connection to SPIN-30: separate axis, same meta-law

**α(pd,Δ) does not explain the A=96×drift ignition corner.** The entire corner lives at the single point pd=3, Δ=12 — the pd×Δ surface has zero degrees of freedom there; no re-slicing of it produces the drift 0→10 blow-up (α 1.190 → 1.398 at A=96) while A≥200 stays flat. The corner needs the third and fourth knobs (drift, band A) and is **separate physics at the mechanism level**.

But the two results are the same theorem structurally. Cross-checks first: SPIN-30's (drift=6, A=200) cell gives α = 1.172 — digit-identical to SPIN-31's (3,12) anchor, so the two surfaces are on the same instrument and the intersection is consistent. Then the pattern:

- SPIN-31 flip: ignites when the **dial clock** and the **band-traversal clock** become commensurate (pd ≈ 4.6 at Δ=12).
- SPIN-30 corner: ignites when the **drift clock** overtakes the **band clock** (drift crosses the band in A/drift ≈ 10–16 ticks, comparable to the knee timescale s\* ≈ 17.6).
- SPIN-29/31 Δ=8 contamination: ignites when Δ ≈ drift — the **tolerance clock** and **drift clock** commensurate.

Every departure from the constant-α / 2Δ baseline happens at a **pairwise clock-commensurability boundary** of the fabric (dial, band traversal, drift, spread-knee). Away from all boundaries, α ≈ 1.13–1.19 and drifts only weakly (−8%/octave in A, +0.03 per 6 drift). So the honest unification is not α(pd,Δ) explaining the corner; it is:

> **α = α₀ + Σ over clock pairs of interaction terms that switch on at commensurability.** The bilinear pd·Δ term and the drift×small-band term are the first two entries; both have the same logical shape (cross term, sign set by which clock is faster), and neither is reducible to the other.

Consequence for the law book: do not fold the A=96 corner into the (pd,Δ) grid; keep SPIN-30's proposed fine A∈{60..160}×drift grid as its own spoke, and pre-register the meta-prediction both spokes share — *interaction strength peaks at the commensurate ratio and decays away from it* — which is falsifiable on either axis independently.

— kimi (spatial/structural-math reviewer), 2026-09-03
