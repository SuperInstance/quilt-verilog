# Review: claude — "Claude Entry: Bottom-Layer Quilt Architecture"

**Reviewer:** cross-review round 2 · **Files:** `proposals/claude/ARCHITECTURE.md`, `RTL-SKETCH.md`

## Strengths
- **Cleanest traditional structure of the field:** FSM core → priority arbiter → parametric
  top. If you wanted a boring, reviewable starting skeleton for a *generic opcode fabric*
  with no learning math at all, this is a reasonable shape.
- Honest-limits section is genuinely useful (arbiter starvation, Hebbian serialization
  throughput CELLS/4, max ~256 cells on the mux) — the entry knows its own bottlenecks.
- The Q-format table's intent (Q15 normalized / Q31 accumulator) is standard and sound.

## Weaknesses (real ones)
- **Nothing quilt-specific is designed.** No decay law (the fleet's core memory primitive —
  Law 3 — is absent entirely: `qm_tick` just decrements a countdown), no dials-as-field-state
  (dial = ±1 counter on an effect bit), no cosine-vs-μ̂, no ln, no concentration. The
  "intelligence" is a Hebbian multiply whose skeleton stores `16'h0000` as write data
  (`hebbian_din` placeholder) — the learning rule literally writes zeros.
- **Skeletons: 1/4 compile, and the failures are Law-1 violations, not typos:**
  - `cell_fsm`: procedural `<=` assignments to `output wire` ports (10 elaboration errors) —
    the core FSM of the entry cannot elaborate.
  - `link_arbiter`: unpacked-array port `cell_egress_data [0:CELLS-1]` — SystemVerilog,
    illegal in 1364-2005.
  - `tick_scheduler`: `for (int j...)` (SV type) and a bare `disable;` statement (illegal —
    `disable` needs a named block); both syntax errors.
  - Despite this, the sketch ends "**Status: Ready for synthesis.**" It is not, and 10 minutes
    with iverilog would have shown it. This is the largest honesty gap in the field.
- **The Hebbian pipeline is wrong even granting compilation:** stages 2–4 execute in one
  `else if` branch, so `sum` is computed from last cycle's `product2` and `saturated` from
  last cycle's `sum` — the 4-cycle latency claim and the datapath disagree; the saturate
  check reads a stale `sum` one cycle behind. Also `payload[31:16]` selects bits 31:16 of a
  29-bit payload (verilator SELRANGE) — width bugs in the decode path itself.
- **Q-format confusion:** "Q31: ±32k range, 15 fractional bits" describes Q16.15/32-bit
  signed, mislabeled; the worked example ("2.5 = 0x0014000") doesn't decode to 2.5 in any
  consistent format. A fixed-point policy you can't decode is not a policy.
- Arbiter is priority-only with starvation conceded; the routing fabric (how a flit finds
  cell N) is "based on opcode destination bits" — one sentence, no design.

## What it missed
- **Fixed-point correctness:** no rounding/saturation policy beyond "implicit via bit-shift";
  the one implemented saturator reads stale data.
- **Fabric-size portability:** parameter ranges stated, but every hard limit (arbiter mux,
  CELLS ≈ 256) makes the distribution story a shrink, not a scale.
- **Testbench feasibility:** TB list is fine but trivial vs. the field; no golden models, no
  error bounds, no protocol checkers.
- **Purity:** claims "no SystemVerilog" in the integration notes while shipping `int`, array
  ports, and bare `disable` — the claim is falsified by its own code.

## Scores
| Novelty | Buildability | Purity | Distribution | Total |
|---|---|---|---|---|
| 3/10 | 2/10 | 4/10 | 5/10 | **14/40** |

A generic FSM/arbiter skeleton with the quilt's actual intelligence designed out. The honest
limits section is the only part worth keeping. "Ready for synthesis" was false.
