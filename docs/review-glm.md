# Review: glm — "The Chain-Quilt: cells, ladders, and one shared math tail"

**Reviewer:** cross-review round 2 · **Files:** `proposals/glm/ARCHITECTURE.md`, `RTL-SKETCH.md`

## Strengths
- **The age-bucket ladder is the best single idea in the competition.** Approximating
  `W = Σ 2^(-age/H)` with bucket counters whose decay multiply is *wiring* (bit placement), plus
  a **proven bound** (`W_exact ≤ Ŵ ≤ 2·W_exact`, retirement tail < 2^-K), is exactly how silicon
  should treat heavy-tailed memory: provable, cheap, honest. No timestamps, no per-event multiply.
- **One shared math tail** (divider/isqrt coprocessor, per fabric) is the right factoring of the
  only expensive arithmetic; cosine via one multiplier + two squaring accumulators + tail visits
  is a credible ±3-LSB design with no wide product.
- **Ring-as-quilt** distribution story is coherent: bridges are cells, wrap-priority seam kills
  structural deadlock, `REG_SLICE_EVERY` makes timing closure a parameter. Generate-if
  (`HAS_COS`, `HAS_MT`) degrades intelligence gracefully instead of deleting it.
- **Saturation policy is enforced, not stated**: sticky flags readable via `qm_view`, rails at
  operator boundaries, deadband snap on dial leak (anti-dither — a detail nobody else thought of).
- Skeleton quality: 5/8 compile clean under `-g2005`; `qs_dial`, `qs_tickgen`, `qs_mathtail`,
  `qs_ln`, `qs_cos` all pass iverilog on first contact. The TB style example (real-arithmetic
  golden model, exact equality for saturating ops) is the best verification doctrine in the field.

## Weaknesses (real ones)
- **`qs_cell_core` does not compile**: `core_take` references `st` and `S_IDLE` ~40 lines before
  their declaration. Verilog-2005 permits use-after-declaration for nets/variables at module
  scope only in some tools; iverilog rejects it. Two-line fix, but the entry's own README claim
  ("first CI action is compile") was never run.
- **`qs_hebb_edge` readout tree trips UNOPTFLAT** (circular comb on the `t` chain). Legal but a
  real synthesis/timing hazard; needs registering or a proper adder-tree restructure.
- **O(N) ring latency + shared bandwidth** is conceded, but the effect-storm interaction with
  the seam's external backpressure under load is not analyzed (only steady-state math given).
- **Edge lookup is a linear scan** (O(E) per link) — conceded, but find-or-alloc also *writes*
  during scan on allocation; victim policy ("tail cursor") can wrap into live edges silently.
  Not addressed.
- **vMF/κ: entirely absent.** Cosine-only is an honest scoping choice but weakens the
  "intelligence lives at the bottom" claim vs zeroclaw.
- Cosine requires a math-tail *grant* path across cells that is named but not sketched; the
  arbitration FSM is the hardest unscheduled piece of the build.

## What it missed
- **Fixed-point correctness:** truncation-only policy; no convergent rounding at integrating
  boundaries (the dial/S accumulators are exactly where zeroclaw proves bias accumulates). The
  leak-path truncation is defended ("decay is supposed to forget") — fair — but nudges are not.
- **Fabric-size portability:** good story, but `CID_W ≤ 12` + one ring per bridge id-space has
  no broadcast/multicast, and fan-out from a hot cell serializes E cycles — a mesh-scale fabric
  would starve. Conceded but not priced.
- **Testbench feasibility:** strong per-module plan; the fabric scoreboard (in-order per
  (src,dst)) is right. No train-to-fire *behavioral* acceptance scenario — nothing proves a
  ladder actually learns across the fabric.
- **Purity:** `-Wall` not clean (unused signals, width mismatches in `qs_ln` multiply widths);
  `casex`-free, no `initial` in rtl — compliant. Minor: `based`/`bumped` naming obscures that
  saturation check reads pre-shift `full0`.

## Scores
| Novelty | Buildability | Purity | Distribution | Total |
|---|---|---|---|---|
| 8/10 | 9/10 | 8/10 | 8/10 | **33/40** |

Novelty: ladder-with-bound + ring-as-quilt is genuinely new composition, not Fusi-citation.
Buildability: near-complete skeleton set, one real compile bug, one comb-loop hazard. Purity:
policy enforced and lint-mostly-honest. Distribution: parameterized timing + bridges as cells.
