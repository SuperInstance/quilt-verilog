# ROUND 13 — Q6: Barbieri operationalized properly (integer Lyapunov proxy)

**Item:** Q6 — perturbation-support / exact-integer Lyapunov proxy on ℤ_n vs D_n vs ℤ_n×ℤ₂
Cayley lattices [RD-BEYOND-UTM Seam B experiment]. F26 falsified the naïve (noise-driven
activity) version; this is the real operationalization and it gates the Lattice primitive's
group-typing story.

---

## PART 1 — PRE-REGISTRATION (written 2026-09-03, BEFORE any comparison run)

### Hypothesis (from Barbieri–García-Ramos–Taati 2410.23770 via RD-BEYOND-UTM Seam B)

The equicontinuity-vs-sensitivity dichotomy is decided by the lattice group **before any run**.
Prediction to falsify: **D_n fabric goes sensitive, ℤ_n×ℤ₂ fabric stays equicontinuous, ℤ_n
in between.** Operationalized here as *damage spreading*: twin lattices differing by a minimal
integer perturbation (+1 at one site) after burn-in, evolved under the **same** dynamics with
**identical** noise draws (one LCG stream feeding both copies), separation measured exactly in
integers.

### Dynamics (q4_mi_sweep2.c lineage, amendment model — conservative-ish emission)

Per tick: (1) decay every d ticks (`a -= fdiv(a,2)` when |a|>1); (2) noise: with prob p add
uniform ±16 via the **shared** LCG draw, same delta to both copies; (3) emission: if a[v]≠0,
e = fdiv(a,3) with minimum magnitude 1, sent to **both** generator-neighbors, emitter pays 2e.
Groups, matched vertex count N (elements indexed 0..N-1):

- **Z** = ℤ_N, gens {+1, −1} (cycle).
- **D** = D_{N/2}, Cayley{r,s}: r:(f,k)→(f,k+1 mod N/2), s:(f,k)→(1−f, −k mod N/2).
- **P** = ℤ_{N/2}×ℤ₂, gens {r,s}: r:(f,k)→(f,k+1 mod N/2), s:(f,k)→(1−f, k) — **the prism
  (D with the −k removed)**. Same vertex count, same degrees, degree-2 generators — the only
  difference is the group law on the s-edge. This is the cleanest possible three-way comparison.

Note honestly: all three finite groups are virtually cyclic (Barbieri's dichotomy is stated on
infinite G); the finite-lattice signature we can measure is the **transient damage exponent**.

### Measurement

Primary statistic: **L1 separation** S(t) = Σ_v |a[v] − b[v]| (exact integer). Secondary:
**support** |{v : a[v] ≠ b[v]}|. Checkpoints t = 0,1,2,4,…,1024. A single +1 perturbation is
applied at site N/2 after 1000-tick burn-in. Note: once the two copies coincide, they coincide
forever (dynamics is a deterministic function of state + the shared noise stream) — **0 is an
absorbing quantization floor**; runs that hit S=0 before the fit window are floor-dominated.

### Fit (exact, float-free)

Fit window **t ∈ [8, 128]** (pre-wraparound for the ballistic wave on N=256). Exponent
α = (log₂S(128) − log₂S(8)) / 120 in 2³⁰ fixed-point integer arithmetic (round-11 `ln_fix`
idiom; log₂ via bit-length + mantissa ln). Exponents reported as exact rationals (numerator
over 2³⁰·denominator reduced). Doubling ratios S(2t)/S(t) over the window reported raw.

### Grid

Groups {Z, D, P} × N=256 × p ∈ {3, 30, 300, 3000}/10⁴ × d=3, seeds {1, 7, 42, 1999, 20260902},
T=1024. Confirm arm: N=512 at p=300 (wrap-safety) and N=128 (small-lattice). Null-dynamics arm
(identity coin: decay+emission OFF, noise ON, shared): must give α = 0 **exactly**.

### Canaries (pre-registered)

- **C-a null-dynamics control**: no decay, no emission, identical noise → S(t) ≡ 1, α = 0
  exactly. Any growth ⇒ harness bug, results void.
- **C-b self-canary**: zero perturbation, identical copies, shared stream → S(t) ≡ 0 exactly,
  every tick, every group. Any nonzero ⇒ harness bug, results void.
- **C-c anchor replay**: `e1.py` output sha256 must equal the banked
  `4f4acccc67420736ec90778a5ad7d4091f7bed5189580e2df83cc1c3e83e5bee` (round-11 C2 anchor).
- **C-d wrap canary**: on Z at N=256, ballistic support wavefront must return to origin by
  t=128+8 (support ≥ N−ε behavior); checks the neighbor wiring end-to-end.

### Decision rule (frozen before running)

Let ᾱ(g,p) = mean over 5 seeds of the L1 exponent α for group g at noise p. Noise floor for
α: |α| ≤ 1/128 per tick. Then:

1. **CONFIRMED (group-typing, discriminating exponent)** — ∃ p such that some family has
   ᾱ ≥ 1/64 while another has ᾱ ≤ 1/128, with non-overlapping per-seed ranges AND the
   high-growth family sustains it to t=128 (not a transient burst that saturates).
2. **FALSIFIED at this operationalization** — all three families in the same growth class
   (|ᾱ(g,p) − ᾱ(g',p)| ≤ 1/32 for all pairs, at every p with activity above zero).
3. **FLOOR-MASKED** — ≥ 3/5 seeds in a (g,p) cell hit S=0 (absorbing annihilation) before
  t = 128: book "quantization floor masks the dichotomy" for that cell; if this dominates the
  grid, the honest verdict is floor-masked overall.
4. Saturating-but-positive growth (support hits the lattice before window end, L1 plateaus)
   is booked as **bounded/amplified**, not exponential — report the plateau as an integer
   amplification factor S_max/S(0).

Interpretation pre-commitment: ballistic support growth (speed-1 wavefront, α_support ≈ 0,
support ∝ t) in **all** families would falsify the *specific* D-vs-P prediction while
confirming the generic "finite Cayley fabrics propagate minimal damage at generator speed"
statement — that is verdict 2 with a mechanistic footnote, and the group-typing story does
NOT get its design theorem from this operationalization.

---
*(Results appended below after the run — nothing above this line changes.)*

---

## PART 2 — RESULTS (run 2026-09-03, after PART 1 was frozen on disk)

Harness: `q6_lyapunov.c` (C99, integer-only, twin copies share one LCG stream so every noise
draw hits both) + `q6_barbieri.py` (exact fixed-point log₂ fit, round-11 `ln_fix` idiom).
Raw dump: `q6-barbieri-output.txt`.

### Canaries

- **C-a null-dynamics (identity coin, shared noise): PASS** — S(t) ≡ 1 for all t ≤ 128, all
  three groups. Zero growth exactly, as pre-registered.
- **C-b self-canary (no perturbation): PASS** — S(t) ≡ 0 for all t ≤ 128, all groups.
- **C-c anchor replay: PASS** — `e1.py` sha256 `4f4acccc…e5bee` byte-identical to banked value.
- **C-d wiring canary (upgraded from the pre-registered wrap check after the wrap check proved
  uninformative — see scar S1): PASS** — at p=0, support(t) equals the independent Python BFS
  ball size on each Cayley graph exactly, t ∈ {1,2,4,8}, all groups.
- **C-e (unplanned but decisive) p=0 sanity run: CAUGHT a real bug before any verdict was
  drawn.** First build's measurement tick mutated the emission scratch while iterating it
  (Gauss-Seidel cascade: a single +1 turned into 255-site "growth" on D/P in one tick). The
  pre-fix grid *looked* like D/P confirming Barbieri with ᾱ ≈ +0.02–0.03 — that entire
  confirmation was the bug. Fixed to full snapshot semantics; all numbers below are post-fix.

### Main grid (N=256, d=3, fit t ∈ [8,128], seeds 1/7/42/1999/20260902)

| group | p=3 | p=30 | p=300 | p=3000 |
|-------|-----|------|-------|--------|
| Z (ℤ₂₅₆) | FLOOR 5/5, S_max 3 | FLOOR 5/5, S_max 6 | FLOOR 5/5, S_max 13 | FLOOR 5/5, S_max 6 |
| D (D₁₂₈) | FLOOR 5/5, S_max 1 | FLOOR 5/5, S_max 9 | 1 survivor α=+99694607/32212254720 ≈ +0.0031 (S 15→16, dies by t=256); FLOOR 4/5, S_max 56 | FLOOR 5/5, S_max 15 |
| P (ℤ₁₂₈×ℤ₂) | FLOOR 5/5, S_max 3 | FLOOR 5/5, S_max 5 | FLOOR 5/5, S_max 9 | FLOOR 5/5, S_max 5 |

Confirm arms: N=512 p=300: Z FLOOR 5/5; D one survivor α=367298653/64424509440 ≈ +0.0057
(S 48→70→135, annihilated by t=1024), FLOOR 4/5; P FLOOR 5/5. N=128 p=300: P one survivor
α=824998629/21474836480 ≈ +0.0384 (S 6→130, then oscillates 10→104→48 — bounded, not
exponential), FLOOR 4/5; Z one *negative* survivor α = **−1/120** exactly (S 4→2, pure
halving-decay signature); D FLOOR 5/5.

Mechanism, read off the raw checkpoints: a minimal ±1 perturbation on this dissipative rule
spreads ballistically at generator speed (p=0 canary: support = BFS ball exactly) but the two
copies re-coincide as soon as decay halving and noise drive the differing sites through zero
together — and S=0 is absorbing (identical state + identical draws ⇒ identical forever). At
every (group, p, N) tested, ≥4/5 seeds annihilate before t=128; the rare survivors grow for a
while and then annihilate too. **No sustained exponential separation exists anywhere on this
grid.**

### Verdict (pre-registered decision rule, part 3)

**FLOOR-MASKED — the quantization floor masks the dichotomy.** Every cell of the grid exceeds
the 3/5 floor-hit threshold; exponential-vs-equicontinuous cannot be distinguished because the
dissipative quantized dynamics annihilates minimal damage before any growth class can declare
itself. The group-typing story is **neither confirmed nor falsified** at this operationalization
— it remains ungated, and the Lattice primitive does not get its design theorem from here.

Honest sub-findings, booked as observations (all below pre-registered evidence thresholds):
1. The only growing survivors at any size sat on **D** (N=256, N=512) or **P** (N=128) — never
   Z. Consistent with the Barbieri direction, but 1/5-seed events; not evidence.
2. Z's one long-lived cell decayed with exponent **−1/120 log₂/tick exactly** (halving every
   d=3 ticks: (1/2)^(1/(3·40))·… — the rational is a decay-only signature, worth keeping as
   the cleanest number this round produced).
3. P's one N=128 survivor plateaued (bounded amplification ~130×S(0)) then de-synchronized —
   verdict-4 "bounded, not exponential" behavior.

### Scars / limitations

- **S1 — the Gauss-Seidel emission bug and the fake confirmation.** The first build confirmed
  the Barbieri prediction (D/P α ≈ +0.02–0.03 vs Z ≈ 0) and was wrong; only the p=0 wiring
  probe (C-e) exposed it. Lesson banked: any damage-spreading harness needs a p=0
  pure-ballistic reference *before* its grid is believed. The pre-registered wrap canary
  (C-d as written) would NOT have caught it; the BFS-equality form does.
- **S2 — operationalization gap.** Barbieri's dichotomy is a statement about infinite groups
  and CA-rule sensitivity; this harness measures finite transient damage under a dissipative
  integer rule with min-|e|=1 emission. The annihilation floor is a property of the *rule*,
  not of any group. A discriminating rerun would need (a) larger perturbations or sustained
  forcing to lift off the floor, or (b) a rule family whose linearization is exactly the
  Rollier–Baetens affine class (exact Lyapunov spectra from adjacency matrices — the other
  Seam B rung, still unrun).
- **S3 — survivorship.** Cell means where computed average over annihilation survivors only
  (selection bias toward lucky seeds); reported per-seed everywhere for that reason.
- **S4 — fit window.** [8,128] was chosen pre-wrap for N=256; N=128 confirm cells are
  post-wrap and their exponents are correspondingly less meaningful (booked anyway, per-seed).

### Disposition

Q6 closed for this operationalization as FLOOR-MASKED. The group-typing gate for the Lattice
primitive stays open; the highest-value next rung on Seam B is the **Rollier–Baetens exact
affine-CA route** (integer matrix powers of the Cayley adjacency ⇒ exact Lyapunov exponents,
no simulation), which sidesteps the quantization floor entirely and is the mathematically
correct instrument for the question.

— Round 13 lane (dev_q6_barbieri, zai/glm-5.3), 2026-09-03, Riker's deck timezone.
