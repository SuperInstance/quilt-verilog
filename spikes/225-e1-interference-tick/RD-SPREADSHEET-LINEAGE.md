# RD-SPREADSHEET-LINEAGE — Ancestral Spreadsheet Archaeology for the Quilt Fabric

*Deep R&D lane, 2026-09-02. Method: 10 repos under `SuperInstance/*` read shallow
(readme + tree + key source files, raw fetch, no clones). Every claim below has a
repo/file path as evidence. Lineage window: 2026-03-10 (Spreadsheet-ai) →
2026-08-24 (cell-runtime). Comparison target: `rtl/q_cell_core.v` (v1 opcodes
bind/link/effect/view/tick + v2 echo gate / RQH residue bank) and this spike's
E1 interference tick (`e1.py` / `e1.c`). The ternary family itself is another
lane's (docs/TERNARY-VERILOG-PLAN.md) — this doc is the **spreadsheet** lineage
only. Undersold on purpose; dead ends flagged inline.*

---

## TL;DR

The sheets were not toys. Five mechanisms they pioneered are missing from the
fabric today: **per-cell oscillator phase gating noise** (spreadsheet-cells —
the direct ancestor of E1 that E1 dropped), **conservation as a first-class,
per-evaluation invariant** (spreadsheet-engine's γ+η=C monitor), **2-bit ternary
quorum/coincidence gates** (ternary-spreadsheet-c's THRESHOLD/PRODUCT — pure
combinational RTL), **diversity-biased fitness/decay** (ternary-spreadsheet's
history-bonus — anti-Hebbian-collapse), and **two-phase reserve/commit budgets**
(spreadsheet-conservation-wasm — credit-based fire admission). Each has a cheap
reclamation experiment below. Three are reportable now.

---

## Part 1 — Per-repo findings

### 1. spreadsheet-cells (Python, created 2026-05-17 — earliest real code in the family)

Evidence: `cell_simulator.py` (whole file), `README.md`.

**Mechanism pioneered:** the coordinated cell as **neighbor coupling + per-cell
oscillator + private deterministic RNG, multiplicatively gated**:

```
value ← AVG(neighbor.value)·0.5 + RNG()·sin(phase), then ·0.95 damping
phase = 2π·tick / period,  period ~ U[10,50] ticks  (cell_simulator.py:36,63)
RNG = random.Random(42+i) — per-cell private stream  (cell_simulator.py:40)
```

Neighbors carry **TE weights** (transfer-entropy-derived, `--topology te-derived`,
`cell_simulator.py:174-192`; README: "TE-weighted edges", dependency
"coordination-topology"). Coordination is not designed — it is *detected*:
post-run cross-correlation matrix over value history, "emergent patterns =
coordinating pairs (corr > 0.5)" (`cell_simulator.py:271-283`).

**The insight:** `RNG()·sin(phase)` is **phase-gated exploration** — the cell
injects its private noise only near oscillator peaks and is deterministic near
zero crossings, while the 0.95 damping is a leak. Two cells with different
periods will intermittently align their noise windows; TE-weighted coupling then
locks correlation. This is stochastic resonance with a per-cell clock. The LCG
constants (`1103515245/12345`, `cell_simulator.py` via C sibling) are the *same*
ones `e1.py` uses — E1 is a direct descendant.

**What E1 kept / dropped:** E1 kept superposition of decaying pulses and the
seeded LCG; it **dropped the per-cell oscillator phase** (E1's twins have no
phase state) and **dropped correlation-based coordination detection** as a
signature (E1 counts cancellation/constructive instead).

**Fabric relevance:** q_cell_core has fire/refractory (a 1-bit oscillator with
hard reset) but no phase diversity and no noise injection at all. Refractory
period is one global dial (`d_refr`), not per-cell.

### 2. ternary-spreadsheet-c (C, created 2026-06-04)

Evidence: `src/ternary_spreadsheet.h`, `src/ternary_spreadsheet.c` (whole file),
`README.md`, `tests/test_spreadsheet.c`.

**Mechanism pioneered:** a minimal, complete, integer-only cell computer over
{-1,0,+1} in ~200 lines of C. Three operators matter for RTL:

- **SUM = clamp(Σ)** — saturating ternary accumulate (`ternary_spreadsheet.c:52-57,70`).
  Identical in shape to q_cell's `act += sat(...)`.
- **PRODUCT = clamp(Π)** (`ternary_spreadsheet.c:71`) — over {-1,0,+1} this is a
  **coincidence gate**: output is 0 if *any* input is neutral, else the XOR-parity
  of the negative signs. Pure combinational logic: `~|zeros & ^signs`.
- **THRESHOLD(range,t)** (`ternary_spreadsheet.c:72-74`) — `pos_count ≥ t → +1;
  neg_count ≥ t → −1; else 0` — a **quorum vote with abstain**. Two popcounters
  and two comparators.

Also: **fixpoint evaluation** — repeated passes until no cell makes progress
(`grid_evaluate`, `ternary_spreadsheet.c:110-127`); cycles are detected by
stalling, not erroring. And **mutation autofill** with an LCG ±1-step clamp
(`mutate`, `ternary_spreadsheet.c:198-207`) — a random walk on the ternary
lattice, i.e. bounded integer exploration.

**Answer to the spike's hypothesis:** it is *not* a 2-bit encoding —
`ternary_t` is a plain int (`ternary_spreadsheet.h:10`). But the **operator
suite** is bit-accurate in 2 bits: the `fitness = v+1` map (`ternary_spreadsheet.c:143`)
is exactly the {−1,0,+1}→{0,1,2} offset encoding, and every operator above
transcribes to ≤ handful of gates. So: yes as a golden model at operator level;
the encoding choice was never made in software — RTL gets to make it.

### 3. spreadsheet-engine (Rust, created 2026-06-08 — the flagship)

Evidence: `README.md` (architecture + conservation sections), `src/cell.rs`,
`src/conservation.rs`, `src/engine.rs`, `src/formula.rs`, `src/a2a.rs`.

**Mechanisms pioneered:**

- **7 cell types** (Value/Agent/Training/Simulation/A2A/MIDI/Formula,
  `cell.rs:230-238`) — the "cell is a system, not a value" doctrine, pre-canon.
- **Conservation law as runtime infrastructure**: every AgentCell carries
  γ (compute spend), η (memory), budget; `conservation_error() = |γ+η−budget|`
  (`cell.rs:194-197`). A fleet-wide `ConservationMonitor` computes
  `health = 1 − |Σγ+Ση−C|/C`, lists violating cells, and a **trend**
  (improving/stable/degrading over last 5 readings, `conservation.rs:72-85`).
  Framed as Noether: budget symmetry → conserved quantity (`README.md`
  "Conservation Law Architecture").
- **Conservation visible at every evaluation**: `EvalContext` carries `tick` and
  `total_budget` to *every* cell (`cell.rs:120-127`); every `CellResult` carries
  a `conservation_ok` bit (`cell.rs:110-118`). The invariant is not a periodic
  audit — it is an argument to the transition function itself.
- **Evolutionary formulas** (`formula.rs:31-51`): EVOLVE (population, keep top
  50%, fitness = Σ|v| — "maximize total energy", `formula.rs:210-243`), ENTROPY
  (Shannon over 0.01 bins, `formula.rs:156-170`), SPECIES (k-bin occupancy),
  PARETO (non-dominated count over consecutive pairs), CONSERVE (health over
  (γ,η,budget) triplets).
- **A2A bus** with Announce/Query/Update/Train message kinds and a capability
  registry (`a2a.rs:45-118`).

**Fabric mapping:** the tick opcode is the engine's tick loop, minus everything
green: no γ/η anywhere in q_cell_core, no health, no trend, no per-eval
conservation bit. `act` leaks via `>>>ka` and nobody accounts for where it went.

### 4. superinstance-spreadsheet (JavaScript, created 2026-06-04 — the origin vessel)

Evidence: `README.md`, `negative_space.py`, `gpu_ternary.py`,
`docs/WORLD-MODEL-BRIDGE.md`, `results/negative-space-*.json`.

**Mechanism pioneered:**

- **Negative-space learning rule** (`negative_space.py:27-46`): update a weight
  to −1 if *any* observed reward is below floor ("deduction from negative"),
  +1 only if *all* rewards clear a bar ("inference from positive"), else 0.
  Asymmetric evidence thresholds — **avoidance is deductive, choice is
  inductive**. "Intelligence = the shape of what's avoided."
- **Exhaustive ternary strategy enumeration** (`gpu_ternary.py:14-27,100+`):
  3^N strategies "enumerable, not searchable"; GPU batch over 3^4=81 strategy
  space, results in `results/gpu-ternary-factory.json`.
- **The world-model bridge table** (`docs/WORLD-MODEL-BRIDGE.md`): cell=room,
  formula=physics, **recalculation=tick**, sort=natural selection,
  **conservation law=thermodynamics**. This table is the philosophical ancestor
  of the fabric.

**Fabric relevance:** the asymmetric ±1 update rule is a *bounded-confidence*
edge trainer — contrast q_hebb_edge's symmetric cofire strengthening. And 3^4=81
matters: EDGES_N=4 means **one cell's edge-validity space is exactly enumerable**
— a golden-model trick for verification (below).

### 5. ternary-spreadsheet (Rust, created 2026-06-04)

Evidence: `README.md`, `src/cell.rs:1-100`.

**Mechanism pioneered:** the **cell with memory and a diversity-biased fitness**:
`fitness = value·(1 + unique(history)·0.1)` (`cell.rs`, README "Cell Model") —
cells that have *changed* more get a fitness bonus; `history` and `generation`
are first-class per-cell state (`cell.rs:87-100`). Also =ENTROPY with max
log₂3 ≈ 1.585 bits as the diversity metric, and =EXHAUSTIVE over 3^N.

**The insight:** pure Hebbian reinforcement converges to monoculture; this was
countered *at the cell level*, not the ledger level — the fitness function
itself pays for variety. The fabric's Variety Ledger does this at engine level;
q_cell_core's cofire training has no per-cell diversity term at all.

### 6. spreadsheet-formulas (Rust, created 2026-06-04)

Evidence: `README.md`, `src/builtins.rs:160-190`.

**Mechanism:** the tokenizer→parser→AST→evaluator pipeline, so `=EVOLVE(A1:A10,
100)` is a spreadsheet formula like any other. Honest assessment: **its EVOLVE
is a stub** — a +1%-per-generation hill climb (`builtins.rs:180-188`), far weaker
than the engine's population version. The pipeline itself is host-side tooling.
**Mostly a dead end for RTL**; the surviving idea is that evolution ops should be
invokable from where the data lives (a formula bar), i.e. first-class fabric
commands, which bind/link/effect/view/tick already are.

### 7. spreadsheet-conservation-wasm (Rust→WASM, created 2026-06-10)

Evidence: `src/lib.rs` (whole file), `README.md`.

**Mechanism pioneered:** the γ+η=C monitor as a deployable island, with one big
addition over spreadsheet-engine: **two-phase budgeting**. `reserve(amount)`
escrows from `available = γ − reserved`; commit consumes escrow; release returns
it (`lib.rs:60-100`). Budget is not just checked — it is **held** between
decision and consumption, so concurrent claims cannot overspend.

**Fabric relevance:** fire is the fabric's only consumption event, and it is
ungated: `act≥thresh && refr==0` → fanout to all valid peers. Nothing reserves.
This is credit-based flow control, a solved hardware pattern (credit shapers in
NoCs/ATM).

### 8. Spreadsheet-ai (Rust, created 2026-03-10 — oldest by date, but a vessel)

Evidence: `README.md`, `src/lib.rs` (which is literally `fn add(u64,u64)->u64`).

**Honest verdict:** vision document with placeholder code. The one extractable
idea: anomaly phrased as **surprise streaks** — "cell 23 has been surprising for
5 consecutive ticks" (`README.md`, Room Integration) — JEPA-error streak as a
liveness/health signal. Everything else is a natural-language query layer.
**Dead end for RTL.**

### 9. spectral-spreadsheet (single HTML file, created 2026-05-29)

Evidence: `README.md`, `index.html` (browser spreadsheet for eigenvalues, CR,
Fiedler vectors, spectral gaps; CR coloring green/red).

**Mechanism:** conservation inspected *spectrally* — the graph's Fiedler value
λ₂ (algebraic connectivity) as a health metric for the cell graph. **RTL dead
end** (no eigensolvers on fabric), but a strong **host-side diagnostic**: the
fabric's bind/link edges form an adjacency matrix; λ₂ > 0 ⇔ the effect graph is
connected ⇔ perturbations can reach every cell. One-off analysis script against
a fabric dump, not silicon.

### 10. cell-runtime (Python, created 2026-08-22 — post-canon, the 8-primitive cell)

Evidence: `src/cell_runtime.py` (whole file), `README.md`, `tests/test_cell.py`.

**What diverged when the canon moved from sheet to fabric** — this repo is the
answer key, side by side with q_cell_core.v:

| cell-runtime (sheet canon) | q_cell_core.v (fabric) | Divergence |
|---|---|---|
| JEPA: `predict()` from inputs, `observe()` returns error, error nudges a **spring** (k·(t−p)) toward actual (`cell_runtime.py:130-140,55-62`) | `act += sat(w·dat)>>>15`; fire at threshold | Fabric is **integrative-reactive**; canon cell is **predictive-corrective**. The RQH residue bank (error envelope → credit) is the fabric's partial return to JEPA — error is kept, prediction is not. |
| Vibe: pos/vel/acc, Verlet integration (`cell_runtime.py:26-33`) — **momentum** | `act` first-order accumulator with `>>>ka` leak | No velocity state in fabric. E1's decaying pulse queue is a halfway house (each pulse has slope −50%/tick). |
| DoubleEntry: every write snapshots debit/credit (`cell_runtime.py:150-155`) | fire zeroes act and fans out dat=act | Fire is a *transfer* but no before/after audit exists. |
| GC 3-phase: merge-similar / decay-stale(60s murmur) / prune-weak (`cell_runtime.py:172-191`) | edge validity + decay sweep in tick; leak | Fabric has decay only — **no merge, no staleness pruning**. |
| Murmur heartbeat, liveness per cell (`cell_runtime.py:194-198`) | none at cell level | Fabric liveness is engine-side. |

The canon cell never lost these by argument — they were never ported. The
fabric took the integrative half (act/fire/refractory/cofire) and left the
predictive half (JEPA/Vibe/DoubleEntry) in Python.

---

## Part 2 — What the sheets knew that the fabric forgot (top 5, reclaimable)

### R1. Phase-gated noise — the oscillator E1 dropped

**From:** spreadsheet-cells `cell_simulator.py` (`RNG()·sin(phase)`, period
U[10,50], damping 0.95). **Fabric gap:** q_cell has one global refractory dial;
no per-cell phase, no noise.

**Experiment (C first, then RTL):** extend `e1.c` — give each cell an 8-bit
up/down **triangle phase counter** (period from a dial, no multiplier; triangle ≈
sin at 2-bit fidelity) and gate the interference arm's pulse injection:
emit pulse only when `triangle(phase) ≥ half`. Sweep per-cell period diversity
(homogeneous vs U[10,50]); measure whether phase-gated injection *reduces*
chatter/cancellations while keeping %w residency — the hypothesis is that phase
gating buys the stochastic-resonance benefit with fewer correction events. If C
says yes: `phase_gate` in q_cell_core's effect op ≈ 30 LUTs (up/down counter +
one comparator), one new dial (`d_phase`).

### R2. Conservation as a checkable invariant — γ+η=C in silicon

**From:** spreadsheet-engine `conservation.rs` + `EvalContext.total_budget` +
`CellResult.conservation_ok`; wasm sibling's health formula. **Fabric gap:**
nothing accounts for act at all — `>>>ka` leaks it silently.

**Experiment:** (a) *Formal:* define fabric-total `Σact + Σw_scaled + Σrqh ≤
C₀` in q_fabric_top and write the SVA `assert property` — the first run will
almost certainly fail by leaking, which is itself the result: the fabric is
*dissipative*, so the conserved quantity must include a **heat register**
accumulating every leak term (`heat += act - act>>>ka` per cell, one adder).
(b) *Semantic:* decide whether fire is transfer or duplication (act:=0 but
dat=act to N peers → N·act injected); if duplication, fire inflates the total
and the ledger should say so. Deliverable: `o_consv` sticky violation flag per
cell, ~1 adder + comparator each — the sheets' monitor at gate level.

### R3. Ternary quorum + coincidence gates — THRESHOLD/PRODUCT as edge logic

**From:** ternary-spreadsheet-c `ternary_spreadsheet.c` (THRESHOLD = popcount
quorum with abstain; PRODUCT = zero-if-any-neutral + sign parity). **Fabric
gap:** fire is a *scalar* test on one cell's own act; no consensus-over-peers
fire mode exists.

**Experiment:** a `quorum_fire` variant of the tick opcode: fire iff `≥ t` of
valid edges cofired within the refractory window — inputs are the per-edge
cofire-latch bits q_hebb_edge already keeps, so this is one popcount + compare,
near-zero new state. In the C model: run the E1 twin scenario where a cell is
corrected only on peer quorum vs only on own act; compare deadband residency and
chatter. PRODUCT-as-coincidence is the stricter sibling (all edges must be
active; output = agreement sign) — one NOR + one XOR tree. If either beats
scalar fire, port as a fire-mode dial bit (`d_firemode`).

### R4. Diversity-biased decay — anti-monoculture at the cell level

**From:** ternary-spreadsheet `cell.rs` fitness `value·(1 + unique(history)·0.1)`.
**Fabric gap:** cofire training is pure Hebb → strong edges get stronger →
collapse; the Variety Ledger fights this at engine level only.

**Experiment:** 3-bit saturating **flip counter** per edge in q_hebb_edge
(counts weight-sign/magnitude-class flips). Effective decay becomes
`ka_eff = ka − kd·flips` (diverse edges decay slower). Sweep kd in simulation;
metric is the sheets' own =ENTROPY over the edge-weight distribution vs
baseline. Cost: 3 bits + one small subtract per edge. This is the cheapest of
the five and the most directly anti-collapse.

### R5. Reserve/commit fire admission — credit shapers on the fabric

**From:** spreadsheet-conservation-wasm `lib.rs` reserve/commit/release with
`available = γ − reserved`. **Fabric gap:** fire fanout is ungated beyond the
refractory; one hot cell can hammer every peer.

**Experiment:** 4-bit per-cell **credit register**: fire requires
`credit ≥ cost` (else defer, not drop), credit refills +1/tick saturating.
Measure on a small simulated fabric: does credit gating reduce E1-style
constructive overshoot (spurious coordinated correction) while holding %w?
This is textbook credit-based flow control applied to spikes — the one
mechanism here with decades of silicon precedent behind it.

---

## Honest dead ends

- **spreadsheet-formulas' =EVOLVE** — stub hill-climb; the real EVOLVE lives in
  spreadsheet-engine and already survives semantically as the ratchet/Variety
  Ledger. Nothing to reclaim at RTL, and population GA in silicon would be a
  mistake anyway.
- **Spreadsheet-ai** — placeholder code (`add(2,2)`). Only residue: "surprising
  for 5 consecutive ticks" → a JEPA-error *streak counter* as cell health
  signal; minor, fold into R2's violation flag if ever needed.
- **gpu_ternary at 750M agents** — simulation claim, not fabric. But its 3^N
  enumeration *is* reclaimable at N=4: **EDGES_N=4 ⇒ exactly 81 edge-validity
  patterns per cell — a directed-test golden model for q_cell_core
  verification** (enumerate all 81, snapshot act/wsum per pattern). Testbench
  trick, not silicon.
- **spectral-spreadsheet** — no eigensolvers on fabric; λ₂ connectivity check
  belongs in a host-side fabric-dump analyzer. Worth one script someday.
- **MIDI sonification** (spreadsheet-engine `midi.rs`) — observability candy for
  fire traces on the bench; genuinely fun, zero priority.
- **A2A Announce/registry** — superseded by bind/link; "announce on boot"
  survives as q_boot_gate. Closed.

## Chronology note (for the synoptic map)

2026-03-10 Spreadsheet-ai (vision stub) → 2026-05-17 spreadsheet-cells
(oscillator+RNG coordination — **E1's true ancestor**) → 2026-05-29 spectral
(λ₂ lens) → 2026-06-04 superinstance-spreadsheet (negative space + 3^N) /
ternary-spreadsheet (+C, diversity fitness) / spreadsheet-formulas (pipeline) →
2026-06-08 spreadsheet-engine (7 cells + conservation) → 2026-06-10
conservation-wasm (reserve/commit) → 2026-08-22 cell-runtime (8-primitive canon,
predictive half left unported) → 2026-09-02 quilt fabric + E1.

*No commits made; this file only. Sources: raw.githubusercontent.com/SuperInstance/<repo>/<branch>/<path>, branch per default (master for ternary-spreadsheet, spreadsheet-engine, spreadsheet-formulas, spreadsheet-conservation-wasm, cell-runtime, superinstance-spreadsheet; main for the rest).*
