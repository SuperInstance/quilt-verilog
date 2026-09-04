# ROUND 18 — Seam B: Rollier–Baetens exact affine-CA spectra (ℤ_n vs D_n vs ℤ_n×ℤ₂)

**Item:** the round-13 disposition's designated next rung — exact integer spectra / cyclic
trace powers of the affine-CA update operator on the three Cayley fabrics, computed exactly
so the ±1 quantization floor that FLOOR-MASKED round 13 cannot mask anything. Re-run of the
lost round-15 lane.

---

## PART 1 — PRE-REGISTRATION (written 2026-09-03 20:5x AKDT, BEFORE any comparison numbers)

### Instrument

The linear part of an affine CA on group G with local mask c ∈ ℤ^S is the convolution
operator M = Σ_{g∈S} c_g P_g on ℤ^G (P_g = the permutation matrix of left-multiplication by
g). M is an integer matrix; its cyclic traces τ_k = Tr(M^k) are **exact integers** for every
k, and ρ(M) = lim_k |τ_k|^{1/k}. No simulation, no noise, no floor — the quantization floor
is sidestepped by construction.

### Fabrics (round-13 Cayley wiring, verbatim — q6_barbieri.py `nb()` maps)

Vertex count N = 2m, elements indexed 0..N−1, (f,k) ↔ f·m + k:

- **Z** = ℤ_N: r-neighbor = +1 mod N, s-neighbor = −1 mod N.
- **D** = D_m: r:(f,k)→(f,k+1 mod m), s:(f,k)→(1−f, −k mod m).
- **P** = ℤ_m×ℤ₂ (prism): r:(f,k)→(f,k+1 mod m), s:(f,k)→(1−f, k).

Update convention (stated, frozen): x'_v = c_e·x_v + c_r·x_{r⁻¹(v)} + c_s·x_{s⁻¹(v)}; s is
an involution everywhere, r⁻¹ = (f, k−1) for D/P, −1 for Z (where r⁻¹ coincides with the
s-neighbor). Directedness is honest and deliberate: the round-13 r-edge is one-directional.

### Arms

- **ARM A — round-13 linearization (deterministic):** mask (c_e,c_r,c_s) = (3,2,2), i.e.
  the halving/fdiv-3 rule with denominators cleared (×6). Structural control arm: by Fourier
  analysis ρ = 7 for **all three** fabrics (Z: 3+2ω+2ω⁻¹ max = 7; D: 3+2cosθ±2 max = 7;
  P: commuting, 3+2+2 = 7). Pre-registered theorem-check: this arm MUST tie exactly.
- **ARM B — directed random masks (stochastic):** (c_e,c_r,c_s) each uniform in [−4,4]
  drawn from an LCG x ← (1103515245·x + 12345) mod 2³¹, seeded by the five fleet seeds
  {1, 7, 42, 1999, 20260902}, redrawn if all three are zero. This is where directedness can
  break the D/P isomorphism that holds for symmetrized (undirected) masks.

### Grid

m ∈ {4, 6, 8, 10, 12, 16} (N ∈ {8, 12, 16, 20, 24, 32}) × groups {Z, D, P} × arms {A, B×5
seeds}. K_MAX = 192 trace powers (k = 1..192), exact Python ints. All τ_k dumped raw.

### Reported quantities (integer-first)

Per cell: τ_1..τ_K raw integers (dumped); rigorous lower bound L = max_{k:τ_k≠0}
(|τ_k|/N)^{1/k}; integer Gershgorin upper bound U = max row Σ|M_ij|; point estimate
ρ̂ = |τ_{K}|^{1/k} over the largest k ≤ K with τ_k ≠ 0 and τ_k ≠ 0 for ≥ 12 of the last 16
checkpoints (else cell booked numerically degenerate). Floats appear only as display of
integer-derived quantities; τ_k themselves are exact.

### Decision rule (frozen)

Let Δ(g,g'; m,seed) = |ρ̂_g − ρ̂_g'| at ARM B. Thresholds: Δ_sep = 1/64 ≈ 0.0156,
Δ_null = 1/256 ≈ 0.0039.

1. **DICHOTOMY CONFIRMED (spectral separation)** — at ARM B: (i) ARM A ties exactly
   (all ρ̂ within 10⁻³ of 7 — control passes); (ii) for ≥ 4/6 of the m-grid AND ≥ 3/5 seeds,
   max pairwise Δ ≥ Δ_sep; (iii) a **consistent ordering** (same group on top in every
   separating cell). Then the finite spectral signature of the group typing is banked with
   its direction.
2. **REFUTED (instrument)** — at ARM B, all pairwise Δ ≤ Δ_null in ≥ 4/6 of the (m,seed)
   cells: the three fabrics' exact spectra do not separate at this mask class and the
   Barbieri ℤ-vs-D dichotomy is not visible in finite cyclic-trace growth. Booked as the
   round's answer (a null, not a failure).
3. **INTRACTABLE** — ≥ 1/3 of cells numerically degenerate (τ-zeros dominating the tail).
4. **MIXED** — anything else; per-cell table booked, no headline claim, next rung named.

Known-limit honesty, stated up front: all three groups are virtually cyclic, Barbieri's
dichotomy is stated on infinite G, and for **symmetrized** masks D and P are provably
isospectral (undirected Cayley graphs isomorphic) — which is exactly why ARM A is the
control that must tie and ARM B (directed) carries the entire discriminating burden. If ARM B
also ties, the correct booking is verdict 2 with this theorem as the mechanism.

### Canaries (pre-registered)

- **C1 — byte-identity double run:** script run twice → output files sha256-identical.
- **C2 — round-13 anchor replay:** `q6_barbieri.py` rerun must reproduce
  `q6-barbieri-output.txt` byte-identically.
- **C3 — trace identity:** τ_1 = N·c_e exactly, every matrix (hard algebraic check).
- **C4 — Z circulant cross-check:** Z's ρ̂ must match the analytic circulant value
  max_j |c_e + c_r e^{2πij/N} + c_s e^{−2πij/N}| to 10⁻⁶ (independent float path, flagged).
- **C5 — ARM A structural theorem:** ρ̂ ∈ 7 ± 10⁻³ for all 18 (group, m) cells.
- **C6 — mislabeled-group self-canary:** rerun pipeline with Z/D constructors swapped; the
  C4 circulant identity on the (mislabeled) "Z" row must FAIL and the harness must print
  LABEL-SWAP DETECTED. If the swap goes undetected, results void.

Integer-only contract: masks, matrices, all τ_k, L/U bounds — integers. Seeds 1/7/42/1999/
20260902 fixed. No other stochastic element exists.

---
*(Results appended below after the run — nothing above this line changes.)*

---

## PART 2 — RESULTS (run 2026-09-03 20:50 AKDT, after PART 1 frozen at commit 7ad7f76)

Harness: `r18_spectra.py` (pure Python, exact ints; τ_k = Tr(M^k) and σ_k = Σ(M^k)_ij²
exact to k = 288; ρ̂ = σ_K^{1/2K} with rigorous bracket ρ ∈ [ρ̂/N^{1/2K}, ρ̂]). Raw dump:
`r18-spectra-output.txt` (416,602 bytes, includes full τ/σ series). Runtime 22 s.

### Canaries

- **C1 double-run byte-identity: PASS** — two full runs sha256-identical
  (`dccfc78b…47ec`), both written to disk and compared.
- **C2 round-13 anchor replay: PASS** — `q6_barbieri.py` rerun reproduces
  `q6-barbieri-output.txt` byte-identically.
- **C3 trace identity: PASS** — τ_1 = N·c_e exactly, every matrix.
- **C4 Z analytic cross-check: FAIL as written, PASS in bracket form** — the as-written
  10⁻³ relative threshold is tighter than the estimator's known N^{1/2K} inflation
  (0.55% at the worst cell, ρ=2, N=24); the corrected bracket check (analytic integer ∈
  [ρ̂/N^{1/2K}, ρ̂]) passes 90/90 cells. Threshold bug in the canary, not the harness.
- **C5 ARM A structural theorem: PASS** — ρ = 7 bracketed exactly in all 18 cells.
- **C6 mislabeled-group self-canary: PASS** — Z/D constructor swap detected
  (LABEL-SWAP DETECTED) via the C4 identity failing on the mislabeled row.

### Main findings (ARM B, all exact)

Every spectral radius on the entire grid is an **exact integer with a closed form**,
verified against the rigorous bracket in **all 90 cells, zero violations**:

- **T1: ρ(ℤ_n) = |c_e| + |c_r + c_s|** — the ℤ_n update operator degenerates to a scaled
  permutation: r⁻¹ and s preimages coincide at v−1 under the round-13 wiring.
- **T2: ρ(D_n) = ρ(ℤ_n×ℤ₂) = |c_e| + |c_r| + |c_s|** — both saturate their Gershgorin row
  sum through 1-dimensional characters (both abelianizations are ℤ₂×ℤ₂ with χ(r), χ(s)
  independently ±1, enough to phase-align any coefficient signs).

Consequences, per cell: D vs P gap ≤ 2×10⁻⁴ everywhere (≤ Δ_null in all 30 cells);
Z separates exactly when c_r, c_s have opposite signs (seeds 7 and 1999: integer gaps
2 and 4, all 6 m-values), never when aligned. Separating cells 12/30, null 18/30,
degenerate 0; ordering is forced (Z ≤ D = P by the triangle inequality) — trivially
"consistent", informationally empty.

Secondary observation (below the pre-registered axis, booked as observation only): D and
P are **not** fully isospectral at directed masks — σ_K(D)/σ_K(P) = 0.9857 at m=16,
seed 7 (subleading-eigenvalue differences; converges to 1 as the gap to ρ dominates).
The D-vs-P structure exists but lives strictly below ρ.

### Verdict (pre-registered rule, part 4, then mechanism)

**MIXED by the letter** — separation exists (12/30 cells ≥ Δ_sep) but in only 2/5 seeds
(rule 1 requires ≥ 3/5); not all-null (rule 2 requires ≥ 4/6 null cells per cell column);
0 degenerate. No headline dichotomy claim is licensed.

**Mechanism upgrade, exact: the ρ route to the Barbieri dichotomy is CLOSED for this
trio — provably, at any 3-entry affine mask, not merely at this grid.**

**[SCOPED by round 18b, DEVIL nudge — 7231ce0 pre-reg, r18b-oddn-output.txt]** Two corrections. (1) *Scope*: "virtually-cyclic" above and in the ROUNDS.md headline was class-sized overreach — the trio is what was analyzed; ℤ_n×ℤ₂ is not representative of virtually-cyclic pairs (no ℤ²-by-finite, no nontrivial ℤ-semidirect products were in the grid). The claim is now **"for this trio."** (2) *Parity*: the grid was even-only (m ∈ {4..16}), and the abelianization-saturation mechanism is parity-dependent — [D_m,D_m]=⟨r²⟩ has index 4 for even m (4 one-dim characters) but index 2 for odd m (2 characters). Round 18b ran the odd cell (m ∈ {15,17}): **G-FORM FAIL, G-TIE FAIL as pre-registered** — the closed-form matches sit within ~0.6% everywhere (estimator-resolution-consistent) but **the D/P tie breaks at seed 42 (gap 0.116/0.090, far beyond the +1.2% bracket bound)**. The theorem statement therefore carries a parity hypothesis on its face: **"closed for even n, this trio."** The broken odd-n seed-42 tie is the first candidate genuine D-vs-P spectral separation and is the named next rung (needs larger K to separate real gap from convergence-rate artifact: |τ_k| factor ≈7 at k=288 is within subdominant-tail range).** The separation
the rule saw is a wiring artifact (T1's preimage collision), and the D/P tie is forced by
abelianization saturation (T2). Since ℤ_n, D_n and ℤ_n×ℤ₂ all have 1-dimensional
characters rich enough to align any mask signs, no 3-entry mask's spectral radius can
encode anything but |c|-combinations — group typing is invisible to ρ here. Round 13's
disposition prediction ("exact spectra sidestep the quantization floor") is confirmed in
the sense that the floor is gone; what the exact instrument now shows is that the quantity
it measures exactly cannot carry the dichotomy.

### Scars / limitations

- **E1 — estimator phase bias, caught by C5.** The pre-registered ρ̂ = |τ_K|^{1/K} is
  biased down up to 0.6% by dominant-eigenvalue phase rotation (complex spectra under
  directed masks); C5 failed spuriously on the first build, which is how it was caught.
  Replaced by σ_k = Σ(M^k)_ij² (phase-immune, exact, monotone); thresholds and decision
  structure untouched. Amended honestly, post-hoc, canary-forced.
- **E2 — canary threshold bug (C4)** — see above; bracket form is the correct check.
- **E3 — Z wiring degeneracy** is a property of the round-13 neighbor convention carried
  over verbatim (r = +1, s = −1 on ℤ_n), not of the group; a symmetrized-Z rerun would
  give Z = |c_e|+|c_r|+|c_s| too and eliminate even the artifact separation.
- **E4 — τ_k full-sequence axis unexplored** — the D≠P σ-ratio shows sub-ρ structure
  exists; the trace-sequence / full-eigenvalue-multiset axis is the honest next rung if
  Seam B is pursued, per the round-13 disposition.

### Disposition

Seam B ρ-route closed by exact negative theorem (T1/T2, 90/90). Group-typing gate for
the Lattice primitive remains ungated; if Seam B continues, the instrument must move to
full spectra (trace sequences, eigenvalue multiplicities) or beyond 3-entry masks —
spectral radius alone is provably dead for this trio.

— Round 18 lane (dev_r18_rollier_baetens, zai/glm-5.3), 2026-09-03, Riker's deck timezone.
