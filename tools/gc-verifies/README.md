# gc-verifies — the GC-METAL lane

Machine checks for `docs/academic/GENERAL-CALCULUS.md` (the capstone).
The five §8 benches live in `../verifies/` (house pattern: exact
integer/Fraction arithmetic, zero float verdicts, PASS/FAIL printed,
bounds stated per section, FAIL printed loudly). This directory holds the
lane runner and the register of what landed.

Run everything (five GC benches + the three pre-existing verifies benches
as a regression guard):

```sh
bash tools/gc-verifies/run_gc.sh
```

## The five benches (GENERAL-CALCULUS.md §8)

| bench | file | statements exercised | checks | bounds |
|---|---|---|---|---|
| escrow | `../verifies/escrow_bench.py` | GC-X1 (executable), GC-T3 (all cuts), GC-T4 (escrow: no phantom / k-full formation / tick-bounded refund / conservation at every commit) | 519 | k ≤ 4, all 2^k−1 consent subsets, τ_consent = 3, all 2^k cut subsets per commit |
| nc | `../verifies/nc_bench.py` | GC-X3 (witness (13,0) vs (3,10)), GC-L1 (every order, every commit), GC-T7 (prefix fold / in-flight exactly / convergence / price exhibited) | 10,194 | tx sequences len ≤ 3 over a 4-symbol alphabet (85), ≤ 120 at-least-once delivery schedules each |
| wavefront | `../verifies/wavefront_bench.py` | GC-T8 (sequences preserved / staleness ≤ W / latency no later), GC-C2(a) machine-checked, GC-C2(b) burst pressure measured (evidence-bounded) | 59,783 | W ∈ {2,3,4}, 27 batch shapes, ≤ 40 due-time patterns, φ ∈ 0..W−1; bursts e·W ≤ 12, B ∈ {1,2,4,8} |
| type | `../verifies/type_bench.py` | GC-X2 (0xC8 split executable, 256-byte census boundary-exact), GC-T6 (digest-pinned agreement / nominal refusal / structural counterfactual) | 10,772 | all 256 bytes × 6 radii; anchor grid 6 × radius grid 3 for pinned pairs |
| product | `../verifies/product_bench.py` | GC-T9 (seam = ordinary crossing / union conserved every commit / het ticks / pair-period ρ with per-tick and faster-period quotes falsified), span round-trips + thinness + consent, GC-C3 direction (three named single-condition failures), GC-C4 bounded probe (four-posting normal form on the enumerated class) | 1,255,756 | (τ₁,τ₂) ∈ {(3,2),(5,2)}, Δ = 1, r = 1, horizon 2 pair periods; game seqs fully enumerated (81), twin seqs stride-29 sample; C4: g,s ∈ [−3,3], α ∈ [−2,2], x ∈ [−3,3], 3 assignment rules |

## Grades (what changed, what did not)

Landed as machine-checked **CLOSED-BOUNDED** (bounds in the table):
GC-T4's constructive content, GC-L1, GC-T7, GC-T8, GC-T6, GC-T9's worked
instance (snap pair incl. the heterogeneous-tick deadband corollary),
GC-X1/GC-X2/GC-X3 executed as counterexamples (the paper's prose
witnesses now run).

**Conjectures stay conjectures** (bench labels say so in-file):
- GC-C2(b): burst pressure measured (occupancy = k for every burst,
  exceeds every tested B with no drops/blocks) — evidence-bounded, not an
  unboundedness proof. Grade unchanged: open.
- GC-C3: each span condition's necessity exhibited (encoding agreement →
  exact-integer seam imbalance; consent representability → seam phantom;
  thinness → ownerless drop, Q1+Q3). The full converse is untouched.
  Grade unchanged: open.
- GC-C4: four-posting decomposition verified on the enumerated
  single-fire correction class (every survivor is the normal form; every
  excluded candidate dies by a named clause — no third option at this
  scale). n-variable/multi-fire cases unprobed. Grade unchanged: open.
- GC-C1: not probed by these benches (its falsifier is a separation
  triple, not a bounded enumeration).

Doc status lines updated in `docs/academic/GENERAL-CALCULUS.md` §8 only,
where the bounded checks genuinely landed.
