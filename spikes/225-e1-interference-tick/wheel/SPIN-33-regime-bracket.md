# SPIN-33 — REGIME BRACKET (pre-registered 975ea4c): the pd*=4.25 flip locus does NOT exist on the lattice — FALSIFIED, and the falsification is the finding

**VERDICT: G1 FAIL, G3 FAIL — no Δ-slope sign flip anywhere in pd ∈ [3.5, 5].** Every arm's α *rises* with Δ, at nearly the same slope: dα/dΔ = +1.37 (pd=4), +1.32 (3.5), +1.30 (4.25), +1.34 (4.75), +1.31 (5) — a ~4% spread of near-identical positive slopes, max arm NF 0.11. There is no regime boundary between pd=4 and pd=5; the SPIN-32 bilinear's flip locus ∂α/∂Δ = 0 at pd\* = 4.25 is an **artifact of the refused model family**, exactly the failure mode the W2 gate predicted: M2 was never licensed to extrapolate, and its internal crossover does not correspond to any measurable feature of the lattice in [4,5].

## What this falsifies

The SPIN-32 doc (ea8a693) said pd\* = 4.25 "is the interpolated location of a regime boundary … pd=3 curves hard into the wall (α rising with Δ), pd=6 continues linear (α falling with Δ)". **The parenthetical was family-tinted**: "α falling with Δ" for large pd came from the bilinear's negative ∂α/∂Δ there, not from measurement. Measured truth (this spin, 5 arms × 5 Δ × 3 seeds): α rises with Δ at ~+1.3 spread/tick for every pd in [3.5, 5]. SPIN-32's own raw measurements never contradicted this — its endpoints were classified by *curvature* (pd=3 second difference −0.274 = 27× gate; pd=6 linear), never by slope sign. The sign-flip reading was imported from the fit, not the data.

## What survives

- The wall is a **curvature** phenomenon anchored at pd=3 (the pd ≤ N/2 = 3 wall from SPIN-29), not a slope-sign regime: if a boundary exists, it sits between pd=3 and pd=3.5 (not bracketed by this spin; SPIN-32's probes had 3.5 but only at Δ ∈ {8, 16} and it was not used as a curvature bracket on a common Δ axis).
- α's Δ-response is essentially pd-independent in [3.5, 5] — one slope to ~4%. Any future surface model must reproduce "α ≈ affine in Δ with pd-independent slope ~+1.3" in this band; M2's pd-coupled Δ response is dead here.
- G3's non-monotone bracket (slopes wiggle ±3% around +1.32, no ties) is consistent with these being one slope plus arm noise at the 0.02–0.05 NF scale.

## Corrected operational statement (replaces the ea8a693 wording)

No formula predicts the knee; α is measured per cell. The bilinear flip locus pd\* = 4.25 is a fit artifact with no lattice counterpart (this spin); the only measured regime structure remains the pd=3 wall (curvature, SPIN-29/32). A candidate boundary pd ∈ (3, 3.5) is unprobed on a common Δ axis.

## Method

Arms pd ∈ {3.5, 4, 4.25, 4.75, 5} (pdn/pdd rationals) × Δ ∈ {8,10,12,14,16}, seeds (1,7,42), spreads 8..30 step 2, K=1, N=6, slope 1.6, drift=6, ticks=4800; `dyn_run_r` from SPIN-32, `pct`/`crossing` from SPIN-29; α = 50% crossing of the seed-mean curve; NF = half the per-arm seed range. Pre-registration verbatim in the script header (975ea4c); 14 s runtime. Raw: `spin33-output.txt`. Script fix during analysis: `crossing()` takes `spreads=` kwarg (display-side only, no instrument change).
