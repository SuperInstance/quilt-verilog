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
