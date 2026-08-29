# Review: seed — "Seed Proposal - Quilt Verilog Bottom Layer"

**Reviewer:** cross-review round 2 · **Files:** `proposals/seed/ARCHITECTURE.md`, `RTL-SKETCH.md`

## Strengths
- **"No multipliers anywhere" is a coherent, defensible position** for maximal fabric
  portability (any FPGA from 1998 on, flop speed, no DSP dependence), and it is held
  consistently across the architecture.
- The CORDIC-for-cosine choice is legitimate and well-matched to streaming (1 result/cycle
  after fill) — it's the one primitive choice here that a strong entry could adopt for the
  small-vector case.
- Zero-source-edit scaling intent (only WIDTH/HEIGHT at top) is the right instinct, even if
  the numbers attached to it are not (below).

## Weaknesses (real ones)
- **The central arithmetic is wrong.** The "mutual bit overlap approximation of product"
  (`overlap[i] = pre[i] & post[i]`, priority-encode the MSB, shift by `14 - highest + rate`)
  is not an approximation of `pre × post` in any statistical sense — it's a magnitude
  estimator of min(|pre|,|post|) truncated to their common prefix. A Hebbian update driven
  by it has unknown, input-distribution-dependent effective learning rate. This is not a
  fidelity quibble; it's the difference between "learning" and "an AND tree."
- **Fabric routing does not exist.** Flits carry no destination address; the fabric wires
  neighbor egresses into ingressess broadcast-style; `quilt_fabric` connects egress_ready to
  constant 1 (drops on any stall, contra the entry's own "no backpressure, intentional"). No
  cell can send to a specific cell. This fails Law 2's spirit (opcodes are the only touch)
  because there is nothing to route *to*.
- **Skeletons: 1/3 compile.** `quilt_cell` needs SystemVerilog block-local declarations
  (fails -g2005) *and* slices an unpacked array (`dial[3:0]` on `dial[0:7]`, illegal); the
  decay line `dial[d] - (dial[d] >> dial[3:0])` uses *dial 3's value* as the shift for every
  dial — a plain bug. `quilt_fabric` uses `cell` as an instance name — a reserved word;
  invalid instantiation.
- **Numbers are confabulated.** "16x16 = 128k LUTs, 800 MHz on 7nm"; "256x256 = 32M LUTs"
  (larger than any shipping FPGA); "0.7ns timing" on the combinational AND-tree; "Q1.14…
  empirically shown to be the stability sweet spot after 9 months of testing." None of this
  can be true or was ever run, and it is presented as measurement.
- **Self-contradictions:** Gray-coded dials claimed in the table, plain binary in the RTL;
  "no sideband signals" then opcodes encoded in data top bits (that's fine, but it is a
  sideband by another name); "all state in wires, edges are streaming registers" vs. edge
  weights fed combinationally from `edge_in` with no per-edge storage anywhere.
- vMF listed as "LUT + 2-bit LFSR rejection sampling, 2 cycles" — that's *sampling from* a
  vMF, not estimating κ; the fleet's statistic is estimation. Wrong verb, wrong primitive.

## What it missed
- **Fixed-point correctness:** "truncate right, round left" (rounding a *left* shift is a
  no-op — a tell), no saturation-on-multiply, deadband-less dial decay.
- **Fabric-size portability:** the table caps at 256×256 with wire-delay claims that were
  never simulated; no timing-closure mechanism (no register-slice parameter à la glm).
- **Testbench feasibility:** "100% toggle coverage" and "bit-for-bit vs Python" promised with
  no TB written; bit-for-bit against float Python is impossible for the truncated CORDIC —
  the criterion is unachievable as stated.
- **Purity:** casex with X-wildcards (lint-flagged), block-local declarations, array slicing —
  three separate Law-1 violations in 3 files.

## Scores
| Novelty | Buildability | Purity | Distribution | Total |
|---|---|---|---|---|
| 4/10 | 4/10 | 5/10 | 5/10 | **18/40** |

The multiplier-free doctrine and CORDIC are salvageable ideas wrapped in arithmetic that does
not work and a fabric that cannot route. Not buildable as proposed.
