# SEMANTIC TOWER — the agentic compiler, from natural-language cells to substrate binaries

**Lane:** semantic-tower (GLM-5.3) · **Date:** 2026-08-29
**Companions:** `FOUNDATION.md` (the cell D1–D5 this tower compiles), `BACK-DECK-APP.md` (the worked application), `QUF-SPEC.md` (the file that crosses levels), `SYNTHESIS.md` (the fabric one manifest targets). Fleet kin: `flux-runtime` (markdown→bytecode, FLUX-ese), `flux-cross-assembler` (one source, cloud/edge encodings), `quilt-pincher` (LLM-as-compiler as an `ai` cell), `quilt-esp32` (the substrate this thesis was dictated about), `quilt-vm-c` (the C middle layer, verified on metal 2026-08-26).

> **The thesis being formalized (Casey's, stated plainly).** (1) The language running on the ESP32 is a **mere optimization**. What the engineer actually needs to say is three things: what is the IO, what is the raw prefilter (the raw voltage), and what must the filter be to render a proper reading for the application — a ToF sensor plus the speed of light gives you the distance equation, full stop. The cell emits oil-pressure-in-PSI; whether the loop compiles to C or Lua is *below the engineer's attention*. (2) The compiler is **agentic** — closer to the flux/agentic-compiler systems than to gcc — and this blurs *which* human-readable language embodies the opcodes: natural-language cells are the verbose exploded view (architecture plus links, readable like a wiring diagram); the compiler chooses C for the ESP32, Verilog for the fabric, JS for the worker — each choice a **human-verifiable middle layer** on the way to the critical function. (3) **Game-port simultaneity:** the same video-game port compiles *both* to the game engine/simulator *and* to a robotic twin; the twin's sensors correct the game's dependent variables when they drift beyond a deadband, snapping to agreement — and the snapping points are chosen with whole units so no floats are ever needed (Pythagorean snapping). Game code's instant-reaction discipline — fixed timestep, no allocation in the loop — is the connective tissue. (4) **Maintenance rendering:** the quilt renders *for maintenance*; zoom into a sensor cell and it reveals the raw voltage plus the equation that renders it, as a series of cells.

This document formalizes the compiler stack that thesis implies. Four levels, two cross-cutting contracts (§5 the snap, §6 the zoom), one knowledge table the agent must hold (§7).

---

## 0. The tower at a glance

| Level | What lives there | Readable by | Artifact |
|---|---|---|---|
| **L0 — natural-language cells** | names, IO declarations, raw prefilter, rendering equations, links, tolerance dials — the *exploded view* | the engineer (like a wiring diagram) | the sheet (markdown/YAML cell graphs, cf. quilt-vision) |
| **L1 — opcodes** | the five verbs `qm_bind/link/effect/view/tick` — the *semantic commitment*, substrate-free | any agent, any auditor | QUF (state-is-a-file) |
| **L2 — target manifests** | per-substrate middle layers: C for ESP32, Verilog for the fabric, JS for the worker, `no_std` Rust | the reviewing human (each layer verifiable) | generated source + manifest |
| **L3 — binaries** | `.qm` rule tables, QUF warm images, worker bundles | machines; humans via hash | hash-anchored artifacts |

The tower's defining property is **not** the levels — every compiler has passes — but *where the human stands*. In a classical compiler the human reads the source and trusts everything below it. In the semantic tower the human may read **every** level: L0 by design (it is written to be read), L1 because five verbs and a byte-exact file beat an IR dump, L2 because the agent is required to emit readable middle layers, L3 via hashes and ledgers. The agent does the drudgery; nothing is hidden. Verifiability is not a stage, it is the *column* the tower stands in.

---

## 1. Level 0 — natural-language cells: the exploded view

> **Definition (L0 cell).** A Level-0 cell is a record
>
> `N = (name, io, raw, eq, links, dials)`
>
> where `name` is a natural-language identifier ("oil-pressure-port"), `io` declares typed ports with units, `raw` names the **raw prefilter** — the physical quantity as it actually arrives (an ADC count, a millivolt, a nanosecond), `eq` is the **rendering equation** in human-readable form (with units on both sides), `links` are the wirings to other L0 cells, and `dials` are the named tolerances and calibration knobs. Everything is prose-shaped; nothing is code.

Worked examples, straight from the thesis:

- **Oil pressure.** `raw` = transducer millivolts (integer). `eq`: `psi = (mV − 500) · 3/80` — a 0.5–4.5 V transducer over 0–150 psi. Note the basis trick already present in the arithmetic: 4000 mV of span times 3/80 gives exactly 150; represent internally in 80ths of a psi and the calibration is *exact integer arithmetic, by choice of unit*. The cell emits oil-pressure-in-PSI. Whether that multiply compiles to C, Lua, or LUTs is not in the record, because it is not the engineer's business.
- **ToF distance.** `raw` = round-trip nanoseconds (integer, from the sensor). `eq`: `d = c·t/2`, with c = 299,792,458 m/s. The speed of light plus the raw measurement *is* the sensor's whole story. (§5.3 handles the fact that c/2 is not a whole number of mm per ns.)

> **Definition (attention horizon).** The engineer's **edit set** at L0 is exactly `{io, raw, eq, links, dials}`. Anything not in the edit set is **below the attention horizon**: a compiler degree of freedom. Formally, a Level-2 choice is below the horizon iff it is *semantics-preserving* — the observable contract (ports, units, the equation's values within tolerance, the link topology) is invariant across all admissible choices.
>
> **Language-below-the-horizon lemma.** The target language is below the horizon: the oil-pressure cell emits the same PSI on quilt-vm-c (ESP32, C), on the fabric (Verilog), and in a worker (JS) — differing only within the tolerance dials the cell itself declares. *Choosing C is an optimization, not a specification.* That is thesis (1), made exact.

L0 graphs already exist in the fleet as prose: quilt-vision's YAML cells (`id`, `kind`, `description`), FLUX-ese's "natural but precise" contract blocks, the back-deck paragraph-cells of paper 68. The tower makes their shared claim explicit: **the wiring diagram is the source of truth; code is a rendering of it.**

## 2. Level 1 — opcodes: the semantic commitment

L0 compiles to the five verbs of FOUNDATION D1: `qm_bind` (dials), `qm_link` (wiring — L0's `links`, directly), `qm_effect` (a balanced transaction), `qm_view` (bounded-freshness read), `qm_tick` (the fixed timestep, §5.4). Nothing new is invented at this level — that is the point. The opcodes are the **semantic commitment**: everything the system will ever do is now stated in substrate-free form, and QUF is its serialization. Two consequences:

1. **The commitment is checkable before any target exists.** Link topology, dial ranges, balance of every transaction — all auditable on the file, per FOUNDATION D3, before a line of C or Verilog exists.
2. **The commitment is portable by construction.** L1 knows nothing of substrates, so every L2 manifest below it is a *projection*, not a port. The same QUF warms the testbench, the soft core, and the fabric (QUF-SPEC §0); the tower extends the same guarantee upward to L0.

## 3. Level 2 — target manifests: human-verifiable middle layers

One L1 commitment, many L2 renderings. Per-substrate, today, in the fleet:

| Substrate | Middle layer | Fleet instance | Verified how |
|---|---|---|---|
| ESP32-class MCU | C (compiled `.qm` rule tables on quilt-vm-c) | `blink.qm` on ESP32-S3, 2026-08-26; RAM 6.5% | limb-blink on metal; UART replay |
| ESP32-class MCU | `no_std` Rust engine | quilt-esp32 `QuiltEngine` | cargo tests; browser sim |
| Silicon fabric | Verilog-2005 | `rtl/`, oss-cad-suite | testbenches, Law 5 |
| Edge/worker | TypeScript/JS | quilt-llm-worker, quilt-vm-typescript | worker test suites |
| Any (research) | FLUX bytecode | flux-runtime, flux-cross-assembler | 2037 tests; dual-target asm |

The flux-cross-assembler is the tower's proof-of-concept in miniature: one semantic source, two encodings (cloud 4-byte fixed, edge variable-width), the *same mnemonics* choosing bytes per target. The tower generalizes from two targets to N, and from mnemonics to natural language.

> **Middle-layer selection rule.** The agent emits the **most readable language that satisfies every substrate constraint** (§7's table). Readability is not sentiment; it is the requirement that a human can verify the layer against the L1 commitment — the layer is a *proof sketch in a programming language*. Selection itself is a judgment (FOUNDATION D2) at zero tolerance: the candidate language either satisfies the capability manifest (ACCEPT) or does not (REJECT); among ACCEPTed candidates, choose by readability, because every layer must pass a human eye on the way to the critical function.

> **The agentic part, stated honestly.** "Agentic compiler" means three things here, all already practiced in the fleet: (a) the compiler *reads* — the substrate table, the L0 graph, the ledger of what worked (quilt-pincher's `ai` cell is LLM-as-compiler in production shape); (b) the compiler *chooses* — middle layer, encoding, memory layout — within the below-the-horizon degrees of freedom; (c) the compiler *can be argued with* — its output is a readable diff a human or another agent can audit, reject, or improve. What it does **not** mean: the agent may not change semantics. Dials, equations, links — the edit set — are above its pay grade. The agent owns the optimization; the engineer owns the meaning; the ledger records both.

## 4. Level 3 — binaries

`.qm` rule tables (ESP32), QUF warm images (fabric/sim), worker bundles (JS). Three properties required of every L3 artifact:

1. **Hash-anchored.** The artifact's digest is its name (mint-receipt sha256 at boot, per quilt-esp32's reflex-arc discipline). A binary without a receipt does not exist.
2. **Warm-loadable.** L3 artifacts restore by QUF semantics: dials, edges, routing, ticks — state-is-a-file all the way down.
3. **Provenance-carrying.** The binary embeds (or its manifest references) the L0 metadata — raw units, equation text, tolerance dials — in QUF header KV pairs. This is not decoration; §6's maintenance invariant is unenforceable without it. QUF's extensibility rule (unknown keys skip, QUF-SPEC §8) already carries the extension; this document is what those keys are *for*.

---

## 5. The deadband-snap contract (thesis 3, formalized)

### 5.1 Game-port simultaneity

One L0 graph — the game port: the playable spec of a machine, its levels, its physics, its sensors — compiles to **two** L2 manifests at once: the **simulator** (game engine target) and the **robotic twin** (metal target). Not two ports; one port, two renderings. The simulator is the fast, cheap, rewindable rendering; the twin is the rendering that touches reality. They run the same dependent variables — position, velocity, joint state — and the twin's sensors are the *only* member of the pair in contact with ground truth. Therefore: **when they disagree, reality wins.**

### 5.2 The judgment-cell pair

> **Definition (snap pair).** A **snap pair** is two cells sharing a dependent variable x: the game cell G (simulated value `g`) and the twin cell T (sensor-derived value `s`). T's chain is a rendering chain (§6): raw IO ⟶ prefilter ⟶ s. The pair carries a **deadband dial** Δ (an L0 dial, integer, in x's units) and a **judge** J_snap — FOUNDATION D2 with the integer metric and tolerance r = Δ, polarity inverted: verdict **WITHIN** (d(g,s) ≤ Δ: no action — the deadband is a Schmitt trigger against chatter) and **SNAP** (d(g,s) > Δ: correct).

The judge evaluates in **squared form**: compare `d²(g,s) ≤ Δ²`. The map t ↦ t² is monotone on non-negatives, so the verdict is identical — and the comparison never needs a square root. This is the first whole-unit dividend: *the judge itself is float-free.*

### 5.3 Whole-unit snapping: when integers suffice

The load-bearing question of the thesis: **when does integer measurement suffice, with no floats anywhere?**

> **Definition (measurement basis; integer sufficiency).** A **measurement basis** b for quantity x is the unit quantum in which x is represented (x lives on the lattice b·ℤ, or b·ℤⁿ for a vector). Integer representation **suffices for tolerance ε** iff every reachable true value lies within ε of the lattice: `dist(x, b·ℤⁿ) ≤ ε` for all reachable x. Since the covering radius of b·ℤⁿ is `b·√n / 2`, a sufficient design condition is
>
> `b ≤ 2ε / √n`   (the **basis inequality**; in 1D, `b ≤ 2ε`).
>
> **Pythagorean snapping** is the exact end of that spectrum: *choose the measurement points themselves* — sensor placements, calibration marks, report units — so that the quantities the application computes are integer vectors with integer norms, i.e. members of the Pythagorean configurations `{v ∈ ℤⁿ : ‖v‖ ∈ ℤ}` (in 2D: the 3-4-5 family and its multiples). Then the required value is **on** the lattice, the distance-to-lattice is 0, and arithmetic over ℤ is *exact* — no floats because none are needed, not because we approximated. The oil-pressure cell's "80ths of a psi" is the 1-D case: pick the report unit so the calibration constant comes out whole.

> **Proposition (float-free loop).** *If (i) both members of a snap pair represent x in the same integer basis b satisfying the basis inequality (or a Pythagorean configuration, giving distance 0), (ii) the judge compares in squared form, and (iii) all rendering equations are integer or fixed-point with provable envelopes (paper 67's dyadic staircases — the honest fallback when a physical constant, like c/2 mm/ns, refuses to be whole), then the entire correction loop — sense, prefilter, render, compare, snap — executes without floats, and the snap error never exceeds ε.*
>
> *Why the weakest substrate sets the arithmetic:* the pair's judge spans two substrates. If either side computed in floats, the two sides could disagree *about the verdict itself* (float divergence across FPU/no-FPU/double-precision-JS), and the deadband comparison would be meaningless. Simultaneity therefore forces the **lowest common discipline** — integers — chosen at L0, enforced by the compiler at L2 for *both* manifests identically. The compiler does not get to choose floats per-substrate; the contract spans substrates, so the contract chooses.

### 5.4 The snap event, and the connective tissue

When the judge returns SNAP, the correction is a transaction, not a write:

`T_snap (nonce n): {(G:authority-on-x, −1), (T:authority-on-x, +1), (G:snap-debt, +|g−s|)}`

G's dependent variable is set to s (reality wins); the drift magnitude is booked as **snap debt**; the transaction lands in **both ledgers** — game and twin — with one nonce, replayable forever (FOUNDATION D3 idempotence makes redelivery safe). Every correction the twin ever makes to the game is three balanced lines. The game's history is never rewritten; it is *annotated with reality*.

The cadence is game discipline, formalized as cell anatomy:

- **Fixed timestep = the tick.** τ is the tick discipline (D1); in the fabric it is the hardware-interlocked deadline that traffic cannot starve (SYNTHESIS Q2); in the twin it is the real-time loop. The game industry's fixed-timestep rule — same Δt every frame, determinism over speed — *is* `qm_tick`. The connective tissue of the thesis is that game-loop discipline and cell discipline are the same discipline discovered by two cultures.
- **No allocation in the loop = state-is-a-file.** All state pre-allocated, byte-addressable, warm-loadable — the game rule against per-frame allocation is QUF's doctrine wearing a different shirt. Allocation happens at load time (L3 warm start) or between epochs (night cron), never inside the loop.

### 5.5 The contract, one line

**Agree-to-within-Δ, snap-on-exceed, reality-wins, log-both-books, all-integer, fixed-tick.** Any sim-twin pair satisfying §5.2–5.4 never displays divergence beyond max(Δ, sensor error), never allocates in the loop, never touches a float, and never corrects silently.

---

## 6. The maintenance-zoom invariant (thesis 4, formalized)

> **Invariant M (zoom).** Every value rendered to any human surface is the endpoint of a finite **rendering chain**
>
> `raw-IO ⟶(f₁) x₁ ⟶(f₂) … ⟶(fₙ) v`
>
> where each `fᵢ` is a cell whose manifest carries its rendering equation (human-readable, units on both sides — the L0 `eq`, carried down through QUF KV per §4.3), and each arrow is a `qm_link` visible in the graph. IO cells are leaves: chains terminate at raw by construction.
>
> **Zoom** is the maintenance gesture: iterative `qm_view` from any displayed value down its chain to the raw IO at the bottom. The quilt rendered for maintenance is the quilt *as a zoomable exploded view* — zoom into the oil-pressure gauge and you find, as cells: the transducer (raw mV), the calibration (the equation, with its 80ths-of-a-psi basis visible), the tolerance dial, the links out.

**Corollary (debugging is zooming).** Under M, a wrong displayed value has exactly three possible failure sites: an equation is wrong (a cell), a wiring is wrong (a link), or the sensor is wrong (raw IO). Zooming terminates at one of them, always. There is no fourth place for error to hide — *that* is what "rendered for maintenance" buys, and why provenance metadata in the binaries (§4.3) is load-bearing rather than documentation.

**Corollary (the tower read top-down).** Maintenance rendering is L0 re-derived *from the running artifact*: zoom is the inverse of compilation. The tower compiles down (L0→L3) and renders up (L3→L0) along the same chain, and both directions are human-verifiable at every step — which is the tower's defining property (§0) doing maintenance work.

## 7. What the agentic compiler must know (the substrate table)

The L1→L2 choice is only as good as the agent's model of the substrate. The knowledge table — the capability manifest every target must present:

| Substrate fact | It decides | Getting it wrong |
|---|---|---|
| **Numeric discipline** (FPU? Q-formats? JS doubles?) | whether equations compile to integer ladders, Pythagorean bases, or dyadic fixed point; whether whole-unit basis is *required* | cross-substrate verdict divergence — the §5.3 failure |
| **Memory budget** (ESP32-S3: 320 KB RAM / 4 MB flash) | cell count, table sizes, stripe placement (D5) | won't load; silent truncation |
| **Tick guarantee** (hardware interlock vs soft timer) | τ's target; whether Δ-deadline cadence is *enforced* or merely hoped | starved corrections under load |
| **IO surface** (ADC/GPIO/UART/NMEA/USB; MHS devices) | adapter cells; the raw-IO vocabulary L0 may name | phantom sensors; unverifiable raw |
| **Allocation policy** (none-in-loop / static / GC) | loop codegen; whether state must be a flat image | jitter, fragmentation, missed ticks |
| **Latency class** (cycles-per-op; MAX_OP_CYCLES analog) | interpreter vs compiled table vs RTL — the middle-layer family | missed deadline; illusion (D4) breaks |
| **Verification harness** (testbench / cargo test / vitest / UART replay) | the Law-5 gate the manifest must pass | unverified existence |

Selection consumes the table row by row (§3's rule); verification closes it (last row). A substrate without a harness is not a target — it is a rumor.

## 8. What is real today vs. what is specified here

**Real and verified in the fleet:** `.qm` on metal (blink.qm, ESP32-S3, 2026-08-26); cross-substrate integer agreement as a *measured fact* — reflex-arc's critic gate, integer-only micro-units, replayed over UART against the desktop gate on 500 real vectors: 100.0000% agreement, zero divergences, mint-receipt at boot (that is §5.3's weakest-substrate discipline, already proven in the small); dual-target semantic assembly (flux-cross-assembler); markdown→bytecode compilation with a human-readable intermediate (flux-runtime); LLM-as-compiler as a cell (quilt-pincher); L0-shaped graphs in production (quilt-vision YAML). **Specified by this document, not yet built:** the four-level tower as one pipeline; the snap pair and its dual-ledger transaction; the maintenance-zoom invariant and its QUF-KV provenance keys; the substrate capability manifest as a formal input to middle-layer selection. Nothing here requires a new fabric; everything here is expressible as L0 convention + L2 agent discipline + QUF keys.

---

## Appendix — the tower in one line each

- **L0 — natural-language cells:** name, IO, raw prefilter, rendering equation, links, dials — the exploded view the engineer reads like a wiring diagram; the edit set, and everything outside it is below the attention horizon.
- **L1 — opcodes:** the five verbs and QUF — the substrate-free semantic commitment, auditable before any target exists.
- **L2 — target manifests:** the most readable language satisfying the substrate table (C/ESP32, Verilog/fabric, JS/worker, no_std Rust) — each a human-verifiable proof sketch toward the critical function; the agent's choice, the human's audit.
- **L3 — binaries:** `.qm` tables and QUF images — hash-anchored, warm-loadable, provenance-carrying.

And the two contracts that span the tower: **snap** (agree-to-within-Δ, snap-on-exceed, reality-wins, log-both-books, all-integer, fixed-tick) and **zoom** (every rendered value traceable to raw IO + its equation, every step human-verifiable, no fourth place for error to hide).

*Semantic-tower lane, 2026-08-29. The definitions stand on FOUNDATION's; the fish are the back deck's; the discipline — fixed timestep, no allocation in the loop, integers everywhere — turned out to be game code's all along. Casey said that too.*
