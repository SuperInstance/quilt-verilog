# SPIN-13 — SNAP-SHADOW: multidimensional snapping shadowed back to 2D

**Verdict: SPLIT.** *Angle-count explosion at matched lattice budget: **REFUTED** (yield collapses ~N^{2/d}; d=8 yields 0.05× the 2D Eisenstein baseline at N=8192). Precision explosion at matched coefficient radius: **CONFIRMED** (×8–21 direction count, ×30–38 finer median gaps, ×21.8 unbiased target precision, ×26 spline edge-angle fidelity, ÷5–19 norm cost in the worked example — all at d=8).*

Claim under test (Casey): "multidimensional snapping shadowed back to smaller dimensions for an explosion in possible precise angles and splines."

## Method (integer-only core)

- Domain lattices Z^d, d ∈ {2,3,4,6,8}; d=2 is the **Eisenstein** lattice (form a²+ab+b²) — the strongest 2D baseline (its low shells are the classic 6/12 triangular snap directions).
- Shadow plane carries coordinates (X, Y·√3), X,Y ∈ Z. Projection X = Mx·z, Y = My·z with fixed seeded integer matrices (entries ∈ [−3,3], columns Smith-generate the full frame Z²). d=2 uses the Eisenstein identity (2,1),(0,1).
- Exact integer arithmetic for everything structural: direction dedup (primitive keys via integer gcd), parallelism (integer cross in the (X,Y√3) frame), budget accounting, B-spline tangent keys (dyadic de-Boor sampling, numerators over /8). Floats only for display angles, nearest-point search metrics, statistics.
- Budgets: **matched point count** (first N points by (norm², lex)) and **matched radius** (‖z‖² ≤ b²). Seeds 1/2/3.

## Canaries (all PASS)

- d_in=2 shadow set == independently-coded direct Eisenstein enumeration at N ∈ {6,24,128,1024} (set equality, after fixing a prefix-completeness bug in the independent path — the first version's square-window growth truncated shells).
- Eisenstein cumulative shells 6/12/18/30 at norm² ≤ 1/3/4/7 (note: shell 4 adds **zero** new directions — duplicates of shell-1 parities).
- Full-suite double run byte-identical (in-script) **and** two external runs byte-identical (`diff` clean).

## EXP1a — angle count at MATCHED POINT BUDGET: collapse, not explosion

| N | eis-2D | d=3 | d=4 | d=6 | d=8 | ratio d8/eis |
|---|--------|-----|-----|-----|-----|--------------|
| 24 | 18 | 18–24 | 13–21 | 18 | 16–19 | 0.97 |
| 128 | 74 | 58–96 | 44–88 | 47–74 | 46–50 | 0.65 |
| 1024 | 636 | 268–708 | 156–398 | 126–260 | 123–145 | 0.21 |
| 8192 | 4988 | 1062–4218 | 621–1332 | 282–654 | 251–294 | **0.05** |

Direction yield falls monotonically in d. Mechanism: the shadow image of a d-ball is a rank-2 ellipse holding ~A_d·r² lattice points while the budget spends ~c_d·r^d domain points; the (d−2)-dim kernel wastes them (kernel redundancy 2.9× at d=3 → 18.4× at d=8, EXP4). Two earlier crashes of this lane (WSL, since fixed) left no artifacts; this run started fresh.

## EXP1b — angle count at MATCHED RADIUS (coefficient budget): the explosion regime

| ‖z‖² ≤ | eis-2D | d=3 | d=4 | d=6 | d=8 | ratio d8/eis |
|--------|--------|-----|-----|-----|-----|--------------|
| 2 | 6 | 12–18 | 18–26 | 30–40 | 46–50 | 8.0× |
| 4 | 12 | 20–26 | 26–62 | 94–168 | 146–176 | 13.4× |
| 6 | 12 | 48–74 | 66–142 | 144–274 | 226–280 | **21.1×** |
| 8 | 24 | 48–74 | 66–168 | 198–454 | 336–406 | 15.5× |

Equal per-axis coefficient magnitude ⇒ combinatorially many shell directions (±e_i ± e_j images). Honest caveat: addressing a point in Z^d costs ~d·log(2R+1) bits vs 2·log(2R+1) in 2D; per-bit the gain shrinks (but stays positive: 46 dirs / ~6.5 bits vs 6 dirs / ~2.6 bits ≈ 7 vs 2.3 dirs/bit at ‖z‖²≤2).

## EXP2 — gap distributions: clustered at matched budget, finer at matched radius

- Matched budget N=1024: eis median gap 0.46°, d=8 median 1.77–1.95° (coarser — collapse side).
- Matched radius 16: eis 36 dirs, median gap 10.9°, min 5.2°; d=8 712–866 dirs, median 0.29–0.36° (**30–38× finer**), min 0.064° (**~80× finer**). Cost: max gap (holes) 4.5–6.6° from anisotropy (σ₁/σ₂ ≈ 1.4–7).

## EXP3 — splines and the unrepresentable angle

**Point-snap (quantization vs reach), budget 16:** common-region (r=3) median error eis 0.90 vs shadows 0.62–0.82 — parity-to-slightly-better (the full frame is denser than E); reach (ellipse min-axis σ₂·r): eis 8.0 vs up to 22.9 (d=6 s=1) / 18.4 (d=8 s=1) — **2–2.9× reach**, but seed-dependent (d=3 s=2: reach 2.8, near-degenerate A=3.6 projection).

**Direction-snapped splines (budget 16 per stored edge), exact dyadic B-spline sampling:**
- Edge-angle fidelity: eis median 0.893°/max 3.9° → d=8 median **0.034°**/max 0.5–0.8° (**26× median, 5–8× max**).
- Tangent-direction multiplicity 16/16 everywhere (parity); turning regularity parity-to-slightly-worse (medTurnDev 2.5° eis vs 2.1–4.0° shadows); endpoint drift comparable (22–56 vs 49).

**Worked example — (113, 20·√3) ≈ 17.0433°, never exactly representable in Eisenstein (X−Y odd):**
- Direct-E: 1° at norm² 39, 0.05° at norm² 79.
- Shadows: 1° at norm² **2** (d=3, 19× cheaper); 0.05° at norm² **11** (d=6, 7× cheaper), 14 (d=8, 5×).

**Unbiased test — 64 golden-ratio targets, budget 16:** eis median error 2.51° → d=8 **0.115° (21.8×)**. One bad seed (d=3 s=2, A=3.6) lands at 2.98° — worse than baseline; projection conditioning is a real failure mode (1 of 12 seeds).

## EXP4 — cost & sweet spot

| d | A=σ₁σ₂ | dirs@8192 | kernel redundancy | medAngErr@16 | medPtErr@r3 | reach |
|---|--------|-----------|-------------------|--------------|-------------|-------|
| eis | 1.0 | 4988 | 1.00× | 2.51° | 0.90 | 8.0 |
| 3 | 10.1 | 1062–4218 | 2.92× | 0.49° | 0.64 | 9.7 |
| 4 | 14.1 | 621–1332 | 5.92× | 0.29° | 0.62 | 12.0 |
| 6 | 24.8 | 282–654 | 12.80× | 0.27° | 0.62 | 10.6 |
| 8 | 27.6 | 251–294 | 18.38× | 0.115° | 0.62 | 18.4 |

Precision tracks A = √det(MMᵀ) ≈ v·√(d(d−1)) (Cauchy–Binet), not d itself; A is a seed lottery (3.6–35.4 here). **Sweet spot: d = 4–6** — most of the precision gain (0.27–0.29° vs 0.115°), 3–8× less kernel waste than d=8, reach doubled, before the N^{2/d} count collapse bites.

## Interpretation

High-D shadowing buys **precision per stored coefficient**, not directions per enumerated lattice point. The fixed projection matrix is an amortized dictionary: each snap transmits only z (d small ints) while inheriting slope complexity up to ~σ₂·r. The count "explosion" is real only in the small-coefficient regime (‖z‖² ≲ 8), which is exactly the hardware-attractive one (trit-scale coefficients). For splines: edge/tangent angle fidelity improves dramatically; point placement does not (sublattice/covering arguments cap it near parity).

## Scars & limits

- Two earlier SPIN-13 attempts died to WSL crashes (infra, since fixed); no files survived — this run is a clean restart.
- Bug found & fixed mid-run: independent canary path truncated shells via square-window growth (prefix-completeness fix); spline point-snap v1 placed control points outside the reachable region (measured reach, not quantization) — redesigned as EXP3a probe + EXP3a2/3b direction-snapped splines.
- d=8 point-snap/spline arms run seed 1 only (runtime); frontier caps asymmetric (16/25/36 by d); turn-regularity metric dominates little — B-spline smoothing washes turning differences.
- Anisotropy holes (max gap ≤ 6.6°) and seed degeneracy (A as low as 3.6) are unaddressed costs; an optimized projection (balanced σ₂, conditioned A) is obvious follow-up but untested here.

## Repro

```
python3 -u spin13_snap_shadow.py > spin13-output.txt 2>&1   # ~40 s, byte-identical across runs
python3 -u spin13b_closure.py > spin13b-output.txt 2>&1  # ~50 s, byte-identical across runs
```
Artifacts: `wheel/spin13_snap_shadow.py`, `wheel/spin13-output.txt`, `wheel/spin13b_closure.py`, `wheel/spin13b-output.txt`, this file.

---

# ADDENDUM (SPIN-13b) — BISECTION-COMBINATION CLOSURE (Casey, same day)

**Claim tested:** "snapped angles themselves can be bisected and combined for a plethora of absolute precision with a finite number of bits to explain, each optimizable for a situation depending on what they are relative to."

**Verdict: CONFIRMED with two sharp caveats.** Closure is a massive precision multiplier under a fixed coefficient cap (eis: 36 → 32,254 exact directions, median gap 10.89° → 0.0085° = **1,285×**, min gap **45,000×** finer; target error 2.51° → 0.0046° = **548×**), and the context-optimality structure is real and clean. But (1) per *address bit*, raw budget growth beats closure (eis raw @ budget 256 reaches 0.12° in **10 bits** vs closure 0.1° in **20 bits**), and (2) closure largely **erases the dimension advantage** — the plain 2D Eisenstein seed, once closed, matches or beats the d=8 shadow seed per bit (0.1°: eis-closure 20 bits vs d8-closure 22).

**Ops (integer-only, lattice renorm, no trig):** BIS_N = prim(u+v); BIS_B = prim(λu+μv) with λ²‖u‖² ≈ μ²‖v‖² chosen by exact integer norm comparison (true arc-midpoint balancing; canary: bisB of the 0° and 60° Eisenstein directions = (3,1) at **exactly 30°**); COMB = prim(αu+βv), α,β ∈ {±1,±2}. Address = op tag + two parent indices (+3 coef bits). Deterministic LCG pair sampling (12k pairs/depth, 3 depths, random/adjacent/new×random mix). Canaries 5/5 PASS incl. zero-vector rejection and double-run + external byte identity.

**Plethora & ladder (eis seed, cumulative):** depth 1/2/3 → 341 / 6,012 / 32,254 directions at mean 15.2/20.9/29.7 bits for the new nodes; min gap 0.193° → 0.00214° → 0.000116° (≈90× then 18× per depth — **faster than 2⁻ᵈᵉᵖᵗʰ**, because combination Farey-density dominates, not pure halving); median gap shrinks ~6–16× per depth. Shadow seeds start richer (d=6: 984 dirs, 0.257° median) and saturate similarly (~82k dirs, 0.003° median at depth 3).

**Context optimality (op duel across 32 golden targets):** loose tolerance → BASE wins; **mid tolerance (1°–0.03°) → BIS_B dominates** (e.g. 23/32 winners at 0.1° eis); **tightest tolerance (≤0.01°) → COMB takes over** (17/32 at 0.003° d=8). Interpretation: balanced bisection is the systematic gap-refiner; deep integer combinations are the extreme-precision Farey engine; the raw dictionary suffices when the target happens to sit near a lattice direction — exactly the "optimizable for a situation depending on what they are relative to" structure.

**Bits-to-precision vs raw budget growth (the honest cost):** every derived node pays 2·log₂(pool) parent bits, so closure trades address bits for precision at ~2× the bit cost of just enlarging the lattice budget (d=4 raw: 0.012° @ 13 bits vs d=4 closure: 0.01° @ 28 bits). Closure wins exactly when the coefficient budget is *capped* (hardware trit-scale coefficients) — it is a precision multiplier at fixed budget, not a bit-efficient replacement for budget growth. Unreached targets at 0.003° (5–20 of 32) mark the sampling frontier of 12k pairs/depth; full closure would close them at further bit cost.
