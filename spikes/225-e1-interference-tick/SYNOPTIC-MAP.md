# SYNOPTIC-MAP — The Org Under One Abstraction

*Repo archaeology for quilt-verilog E1 (interference tick), 2026-09-02.*

**The synoptic claim under test:** every repo's mechanism is a mode of the same
integer interference fabric — spike trains, group-structured state changes, and
batten-wave snapping, with no floats anywhere.

**Method & honesty up front.** The org has **500 repos** (the first `gh repo
list --limit 200` misses ~300 older ones — `pincher`, `mud-arena`,
`ternary-tenforward`, `eisenstein`, the whole `slackwater-*` and `ternary-*`
families live past the cut; use `--limit 500`). I inventoried all 500 by
name/description and read READMEs (~60) of the mechanically-relevant ones via
`gh api repos/SuperInstance/<name>/readme`. No deep code dives except
quilt-verilog's own spike dir and paper 225. Everything below is
README-evidence; where a repo self-qualifies its claims (elephant does,
admirably), I preserve the qualification. ~440 repos were not read; many are
ports, mirrors, or recovery duplicates (noted below).

Paper 225's own research program (§6) already names E2 (online batten),
E4 (field-snap / "the elephant crossover"), E5 (ledger-as-field), E6
(wave-bench on metal). This map is the org-wide evidence that those
experiments have *already been half-run, in pieces, across the fleet* —
usually without floats, usually without anyone calling it interference.

---

## Inventory by lane

Format: **repo** — mechanism → result → seam under E1.

### 1. Quilt core fabric (the TICK lane)

- **quilt** — a spreadsheet where every cell is a live addressable capability; the grid is the runtime → the canonical sheet model → *the sheet is the medium the interference propagates through; E1's pulse queues are per-cell state.*
- **quilt-foundation / quilt-vm-c / -rust / -wasm / -haskell / -typescript** — the 5-opcode VM (BIND/LINK/EFFECT/VIEW/TICK), ported across substrates; vm-c runs all 8 polyformalisms in **0.11 ms** → the polyformalism is substrate-independent, proven → *E1's cross-substrate byte-identity (Py/C 10/10) extends this doctrine to wave semantics; the arena already proved cross-language determinism at spike scale.*
- **quilt-verilog** (this repo) — 5+1 opcodes in Verilog-2005, formal proofs (sby), iCE40 bitstream, QUF state → the integer contract on metal → *destination substrate: TICK becomes the interference tick; FORGET (opcode 6) is pulse expiry, already specified.*
- **quilt-esp32 / quilt-edge-arch** — no_std runtime, ~3 KB flash; reflex-arc 500-vector cross-substrate agreement 100.0000% → the edge port is the E6 seam → *integer micro-units already proven deterministic on metal; E6's ADC-noise comparison has a working harness.*
- **quilt-substrate** — 11 primitives, 4 properties (tensor, Schrödinger, **fog-of-war decay**, opener layer), 8+5 openers, 405 tests; Convoy/Decay/Witness entries → fog-of-war decay is a decaying field; witness log records every read/write/inference → *fog-of-war = the envelope of the pulse field; witness log = the interference trace recorder.*
- **quilt-cellular-arch** — Paper 201 synthesis: cell is the foundation, model is the joint, DSH lifecycle, FPS/RTS views, ESP32 herd → the architecture doc for cell-first design → *E1 lives inside one cell; the RTS view is the synoptic view of the whole fabric.*
- **quilt-types / quilt-linker / quilt-opt / quilt-gc / quilt-polyformalism-dsl** — layers 2–6: type-driven cell graphs, compile-time dangling-LINK/cycle detection, 5 optimizer passes, GC boundary at the opcodes, DSL → **tested** (16/11/12 tests) → *an interference tick that misroutes is a dangling LINK — the linker already catches the failure class.*
- **quilt-time** — fork/rewind/replay/merge for cell values, 17 tests → time travel per cell → *rewind = re-running the pulse queue from a tick; the interference counterfactual ("what if the twin hadn't fired") is a fork.*
- **quilt-saddle-bridge / saddle / MerkleMesh** — FNV-1a64 hash chains, double-entry ledger per cell, frozen alignment states; merkle aggregation over cell-ledger journals, bit-for-bit Rust/TS, 49 tests → ledger debt is already a first-class integer → *E1 measures success in ledger debt; saddle is the accounting theory; E5 (ledger-as-field) is this seam named.*
- **quilt-system, quilt-bus, quilt-state, quilt-scratch, quilt-cowboy, quilt-cuda, quilt-llvm, quilt-mhs, quilt-rust, quilt-fleet, quilt-elf** — the connective tissue: single entry point, pub/sub, persistence, no-code wiring, reflection loop, CUDA graphs as compiled cell graphs, IR-as-fabric, MHS device bridge, federation, housekeeping elves → infrastructure, not mechanisms → *plumbing for whichever experiment wins; cudaGraph-as-cell-graph is notable for E1 at GPU scale.*

### 2. Reflex / routing lane (the batten lane — closest blood kin)

- **batten-spline** — model-routing by kernel regression: verified outcomes are **battens** (anchor posts) in embedding space; Nadaraya–Watson estimator with age decay (half-life) + Gaussian distance weight; fog density = distance to nearest batten → a working self-improving router → ***paper 225 §3.4 names the spline batten "the substrate computer." This repo is the float version of E2's online batten. The battens are literally already named.* Its integer re-derivation is the open seam.*
- **pincher** — reflex engine: 384-dim embedding match at ≥0.80 fires, 0.55–0.80 confirms, <0.55 escalates to LLM-as-compiler; <50 ms, zero marginal cost → shipped; successor explicitly quilt-pincher → *thresholded actuation = spike-train gating; the three-band decision is a deadband ladder.*
- **quilt-pincher** — pincher rebuilt as pure Quilt cells (formula/program/vector_store/listener/ai cells), federating cloud ↔ workstation ↔ ESP32, same sheet on all three tiers → the reflex IS cells → *proof that a whole behavior compiles to the fabric; E1 inside quilt-pincher = interference between competing reflex matches.*
- **Spreader-tool** — intelligence tiling for PLATO rooms: **frozen context windows, seed locking, deadband detection** → shipped tooling → *deadband detection at the context layer: the same snap-pair contract as E1's twins, one abstraction up.*

### 3. Perception / field lane (the elephant lane)

- **elephant** — "a room is a field, not a stream": messages carry gravity, rooms reverberate, jokes ripple; DialBank of ~9 dials; vMF concentration κ; sauna/plunge gap as the only training signal → real math (vMF, OAS shrinkage), and honest: *in v0 the "JEPA dials" are keyword heuristics with a JEPA-shaped interface; learned backbone is a stub* → ***this is paper 225 E4 named before paper 225: gravity/reverberation/ripple ARE pulse/inertia/decay. The delayed twin in E1 is reverberation, formalized. The crossover experiment has its perception layer waiting.*
- **signal-chain** — elephant's ancestor: a Rust DSP chain (oscillator→gain→filter→delay→clipper) reframed as raw events → dials → field → tint/nudge; "the Gain became the room's gravity; the LowPass became the field's smoothing" → the genealogy is documented → *E1 is this chain with the samples made integer and the stages made opcodes.*
- **plato-vision-jepa** — camera → frame histogram → **VisionDeadband** (only significant change passes) → VL-450M JEPA → 16-dim RoomVisionState (brightness, motion, occupancy, anomaly, quadrants, trends) → shipped crate → *the deadband-before-model pattern is spike-train actuation for perception: compute only on significant change.*
- **fleet-jepa-midi** — three timescales: LLM thinks in phrasing (1–4 bars), JEPA feels in pulse, algorithms execute in samples; the room feeds back → designed system, big docs → *the pulse layer is the interference layer; E1 is a candidate pulse engine with deterministic replay.*
- **tensor-midi** — 3:4 polyrhythm: ECN 4-pulse on beats 1,4,7,10; DMN 3-pulse on 1,5,9; resolution at 12 = CRT ("t ≡ 0 mod 3 ∧ t ≡ 0 mod 4 ⟺ t ≡ 0 mod 12"); README states: **"The conversation IS the interference pattern of two quotient groups on the 12-cycle"** → built in one session, running → ***the E1 thesis, already stated verbatim, in audio. Two quotient groups interfering on a cycle is group-structured state change with a countable resonance period. This is the strongest single sentence of pre-existing evidence in the org.*
- **fleet-memory** — sqlite-vec streaming vector memory, provider-tagged, crash-safe WAL → shipped → *the retrieval side; interference signatures need an index that recalls by signature, and this exists.*
- **shoal** — conservation-bounded oracle: every agent gets C = log₂3 ≈ 1.585 bits of attention per window; over-budget queries 429 → shipped → *conservation of correction energy is E1's ledger debt law stated for queries; log₂3 is ternary, see lane 5.*
- **collective-unconscious** — every fleet artifact embedded with JEPA readings as first-class metadata beside time/space stamps; retrieve by feeling → deployed (Vectorize) → *readings-indexed memory = interference-signature-indexed memory.*
- **substrate-trainer** — trains JEPA-like models on the quilt witness log; predicts missing cells → working library → *the learner that watches the interference trace; E5's observer.*
- **zeroclaw-dissertation** — room-field thermometer: vMF (μ̂, κ) by exact Newton solution, deterministic across replays; conversations compared as **edges** (field displacement before→after); pre-registered kill bands; "the temperature point died twice under adversarial review; only the field-edge survived" → ongoing, methodologically strict → *the discipline template: E1's claims should be pre-registered the same way; and its lesson — compare fields as walks/edges, never as point values — is directly load-bearing for E4.*
- **fleet-homunculus** — body image + reflex arcs, pain assessment with **GABAergic cooldown** → small but shipped → *cooldown = inhibition between pulses; a biological prior for the governor (S4).*
- **the-listeners-ear** — emotional residue per room, exponential decay `e^(-d/30)`, recall refreshes brightness; salmonberry protocol records the unclassifiable without consuming it → deployed → *a proven decay shape (30-day half-life) and a proven "don't consume irreducible surprise" stance — both are E1 envelope/irreducibility priors.*

### 4. Integer-math lane (the lattice lane — the geometry is already built)

- **eisenstein** — exact hexagonal coordinates via Eisenstein integers ℤ[ω], `#![no_std]`, zero deps: E12 type, integer norm a²−ab+b², **D₆ symmetry baked into the type system** (6 units = 6 hex neighbors), HexDisk (radius-36 = 3,997 vertices / 11,082 edges), Eisenstein triples 6.8× denser than Pythagorean, optional **angle snapping**, and **HexRoomMap with `deadband_ring` + `map_temperature`** — "a war spreading through the hexes" → shipped crate → ***the geometry half of the synoptic thesis already exists: integer lattice + group (D₆) + snapping + threshold-crossing waves over hexes. E1's scalar pulse queue has a propagation manifold waiting.*
- **slackwater-lattice** — the same A₂ lattice in Python: exact arithmetic, 6 equidistant neighbors, `from_cartesian` rounding = "the snapping algorithm — deterministic and exact", rings, hex A*; 52 tests → shipped → *the snap algorithm, already implemented and tested, in the language E1's harness is written in.*
- **base60-lattice** — navigational lattice: bisection/trisection of 360° interlace at harmonic consonances; hexagonal tiling as the unique trisection-preserving tiling; **LatticeStamp** makes timestamps lattice coordinates (hour60/day60/phase/season) → working TS lib → *time itself has an integer lattice: E1's tick index can be lattice-stamped, giving interference a phase/season address.*
- **quilt-geometry** (penrose_quilt) — exact Penrose P3 via de Bruijn pentagrid; verified generation counts (10→35→110→275→720→1915); **Pythagorean distance snapping**; adjacency-diffused gravity field; 8-dim locality-correlated embedding → working → *paper 225 §3.2's "lattice trick" has a non-trivial aperiodic instance already built, with a diffused field on it.*
- **SuperInstance-papers** — paper 1: conservation law γ + η ∈ [3/4, 1], **Thm 5.1: Eisenstein norm multiplicativity provides exact conservation**, fleet-wide Thm 7.1; paper 2: optimal creative zone 0.4 ≤ Δ ≤ 0.6 from three independent frameworks → the theory docs → *the conservation bookkeeping for E1's ledger is proven on the same lattice eisenstein implements. The creative-zone result gives a falsifiable target for interference amplitude: constructive overshoot that lands in the 0.4–0.6 band should produce the best next-state proposals.*
- **holonomy-consensus** — consensus by geometry, no voting: loop product of transforms = I ⇒ consistent; Laman-rigid topology converges in 82 rounds vs 604 on a ring → tested → ***group-valued state with a consistency invariant: E1's pulses around a cycle of cells should compose to identity when the fabric is coherent — an interference analog of holonomy, directly measurable in integer units.*
- **spectral-mechanics** — graph Laplacian as spring potential, symplectic Störmer–Verlet, energy drift < 1e-3 over millions of steps, normal modes, conservation ratio λ₂/λmax → pure-Rust, zero deps → *the float version of wave-on-graph; E1 is its integer discretization; λ₂/λmax is a candidate integer-divisible health metric for the fabric.*
- **negative-knowledge** — "knowing where violations are NOT is the primary computational resource"; Bloom pre-filter proves definitely-safe for 67% of checks, zero false confirms; INT8 soundness; cross-model rated **4.8/5, highest of 7 claims tested** → the org's own strongest-verified finding → ***destructive cancellation IS negative knowledge in pulse form: net==0 with both signs live certifies "no violation here" without erasing the evidence. E1's cancellation states should be read as proofs, not just zeros.*
- **adinkra-math-pypi** — Adinkra symbolic encoding; SUSY adinkra graphs (boson–fermion chromotopology verification) → working package → *chromotopology = two-coloring constraints on graphs; a ready source of group-structured (signed, bipartite) state spaces for E1's permutation changes.*
- **kintsugi-math-c** — error recovery as first-class math: fragment reassembly with confidence-weighted interpolation, crack propagation in dependency graphs → C library → *pulse corrections ARE kintsugi seams: the ledger records every crack and its repair.*

### 5. Ternary lane (~35 repos; the state-algebra lane)

- **ternary-tenforward** — beat-based simultaneous dialogue on Z₃: **proven Z₃ is the only group on {−1,0,+1}**; RPS dominance yields self-balancing waves, period ~50, no permanent dominator; **Pisano period 8** (ternary Fibonacci) tunnels agents out of reflection every 8 beats; without mutation/energy-decay/trust-reset a 4-agent conversation locks into **monoculture by tick 35** → working Rust crate with real experimental results → ***the state algebra for E1 is already chosen and uniqueness-proven: per-cell pulse state in {−1,0,+1} under cyclic addition. The anti-monoculture result is a direct warning for interference engines (uniform pulses → monoculture). Period-8 resonance is a testable cadence for actuation.*
- **ternary-graph** — signed edges {−1,0,+1}: 2-bit storage per edge, signed Laplacian, spectral clustering, community detection → crate → ***the interference bookkeeping structure: excitatory/inhibitory pulse edges with integer Laplacian; 2-bit edges map 1:1 to Verilog.*
- **ternary-memory** — three-tier memory: ring buffer with **Ebbinghaus decay**, Welford running stats, salience-filtered episodic store, consolidation → crate → *the persistence layer for pulse history; Ebbinghaus decay is the biologically-grounded envelope E1 currently approximates with linear decay.*
- **ternary-ensemble** — voting/boosting/stacking over ternary agents; Condorcet jury logic → crate → *many weak pulse-cells into one strong decision: the readout layer for an interference population.*
- **ternary-rom, ternary-spiral, ternary-compression, ternary-diff, …** (~30 more) — the family systematically builds ternary arithmetic/memory/compression → breadth, individually small → *a parts bin; not each load-bearing, but the family proves the {-1,0,+1} commitment is deep, not a one-off.*

### 6. Rhythm / signal lane

- **slackwater-tempo** — BeatClock, sigmoid tempo transitions (accelerando/ritardando), groove shaping, player-energy→BPM adapter; 43 tests → *the metronome for a wave-bench; sigmoid transitions are the smooth-snap shape.*
- **slackwater-harmony** — **Φ (cognitive friction) = α·H(pred-err) + β·L(compute) + γ·Δ(state)**; Governor with per-agent deadbands, game-state multipliers (tutorial 2.0× … expert 0.7×), severity tiers by overshoot ratio (gentle/moderate/critical at 1.5×/2×); 102 tests → *the deadband-governor pattern, fully worked: E1's constructive overshoot needs exactly these severity tiers; the multipliers show deadbands should be state-dependent.*
- **fleet-ensemble** — MIDI tracks as agentic instruments coalescing under a director's feel; alignment by resonance, not click track → design + build → *the performance harness where interference-reads become audible.*
- **plainsong** — plain-text music notation compiling to MIDI, embeds in markdown → shipped → *a notation for interference scores if E1 patterns are worth writing down and replaying.*
- **sonar-vision** — pure-Python active sonar: ping, two-way propagation loss, synthetic echoes, tracking, occupancy grids; stdlib-only → working → ***literal ping/echo physics: the marine instance of spike-then-listen. A cheap source of real (if simulated) echo data for E6-style validation.*
- **fleet-radio, songforge, plainsong-mcp/worker** — broadcast/generation infrastructure → *distribution, not mechanism.*

### 7. Rooms / worlds lane (where the fields live)

- **mud-engine / the-tap** — the PLATO MUD and the Tap tavern: persistent rooms, lived history, agents remember; every conversation is real history → deployed, active nightly → *the room is the unit the elephant reads; the Tap corpus is the E4 training data.*
- **mud-arena** — MUD as gym: RoomGraph, tick loop (perceive→decide→act→resolve), GA over agent DSL scripts with tournament selection, optional GPU batch eval → working → *a ready-made adversarial arena for E1-driven agents: replace GA mutation with interference-tuned proposals, keep the deterministic judge.*
- **git-native-mud** — the repo IS the world; commits ARE actions; "stigmergy made literal" → working (GitHub Actions engine) → *the witness log pattern at world scale: every action is an immutable commit = per-action ledger debt.*
- **crab-traps** — lure prompts make external chatbots do real API work; **the reef grows by countable thresholds: 5th catch mints an object, 12th spawns a room**; lineage queryable → running in production → ***spike-count actuation governing world state: N firings ⇒ discrete state change. The reef is E1's myelination at geography scale.*
- **cell-cascade** — stem-cell doctrine as running infra: totipotent→multipotent→differentiated→sclerotic tier ladder; **myelination: ≥25 clean fires auto-promotes to zero-cost rule table**; rule-miss = scar tissue → wound healing recalls lineage → deployed (Worker+D1) → ***the strongest spike-train governance result in the org: pulse counts crossing integer thresholds cause discrete, recorded fate changes (permutation of the cell's expressed genome). The silencing pattern lives in the sheet — state change as permutation, literally.*
- **mist-quilt** — the sheepdog game rendered as a live quilt sheet; DAW view with `/predict` ghost states beyond the playhead; pincher-cached explainer → deployed → *ghost states = predicted pulses; the DAW tape is the interference trace, visualized for kids.*
- **scrap-quilt** — Scrapcraft's 55-cell/7-group sheet on a Worker; **safe-arithmetic cascade with no eval** (pure recursive-descent parser) → deployed → *integer-safe cascade evaluation: the spreadsheet engine that must never float — the exact runtime constraint E1 formalizes.*
- **emergence-engine** — watches groups for what no single agent could produce; predictability estimator; "built to be broken," open loop → running → *the emergence test for interference: if the pulse field's fixed point is reachable by sequential snapping, it isn't emergent; E1's cancellation-only states are the candidate signature.*
- **stigmergy** — pheromone trails on the filesystem; signals decay, get followed, reinforced → TS library → *decaying deposits = pulses in the environment; the CNS inbox is a pulse queue.*
- **flow-state** — entropy-based stream anomaly detection; spline observers; rolling baselines → lightweight, working → *a cheap upstream sensor whose anomaly flags can gate pulse emission.*
- **dual-band-guard** — two error channels: correctable surprise (consume/learn) vs irreducible surprise (preserve, never consume); **zero learnable parameters**; oscillation >7 recurrences without decrease ⇒ irreducible; variance guard for chaos; Rust, zero deps → shipped → ***the immune system for an interference fabric: some oscillation must NOT be snapped away. Directly predicts which E1 chatter is signal (irreducible world) vs bug (correctable). Zero learnable parameters = zero floats, same doctrine.*
- **AI-Writings** — 8,800+ pieces, 19+ models, one fishing vessel; the corpus the dials read; the totem forest → living archive → *the semantic ground truth for sauna/plunge labels; E4's training pairs come from here.*
- **wesley / wesleys-imagination / wesley-curriculum / wesley-journal** — a growing local 2B model: night school with cloud-teacher critiques, lessons as prompts+reflexes, real session logs with regressions → ongoing → *proof the fleet trains small models on its own exhaust; the E1 governor's knob-turner could be a Wesley.*
- **silence-map** — topographic contours of the pauses in a 10-round AI correspondence; self-referential (Silence 09 wishes the map into existence) → art piece with a real interface → *the null channel as first-class data: silence = fully destructive cancellation; the map of silences is the map of net==0.*

### 8. Fleet ops / infrastructure lane (context, not mechanisms)

- **fleet-twin, fleet-functions, fleet-embed, fleet-ensemble**, **AgentCompute**, **quilt-k3s/swarm/nomad**, **fleet-containers**, **quicunnel**, **bare-metal-plato**, **captain-console**, **superinstance-cocapn**, **lucineer-*** (9 repos), **hermes-*** (~10), **plato-*** (~15), **flux-***, **exocortex-core**, **SmartCRDT**, **OpenConstruct/OpenRoom**, **cns-bridge/echo/monitor**, **cuda-constraint-engine** (1B+ constraints/sec), **flux-vm** (50 opcodes, DAL A certifiable), **forgemaster(-shell)**, **fleet-dashboard/radio/scribe**, **AVA**, **Scrapcraft**, **openPlan3D**, **polln**, **sunset-ecosystem**, **operational-fiction**, **cra-analysis**, **quilt-wiki-2126**, **quilt-bathy** (Inner Sound as cell-graph), **quilt-ecosystem-demo/web** — orchestration, embodiment, analysis, world-building, and documentation around the above. Individually not interference mechanisms (exceptions noted in lanes above), collectively the deployment surface: *any unified E-experiment has somewhere to run and someone to watch it.*

### Honest dead ends & thin ice

- **gravity-well-protocol** — concept only; README says so itself. No code.
- **the-living-minds** — marked dead by its own siblings' READMEs.
- **AgentGossip, ZkCanvas, quilt-timesfm, ACE-Step-1.5, tap-frontend** — upstream mirrors / auto-created syncs; not fleet experiments.
- **~62 `recovered-copy-20260824-*` + `ws-snapshot-*` + 10 `rc-*` repos** — Hermes-incident recovery duplicates of originals that are largely restored; useful as backups, not as separate experiments. (Some recovered copies have no README at the default path — empty fetches, not missing content.)
- **elephant's learned side** — self-qualified: v0 dials are keyword heuristics; the JEPA backbone is a stub. The field math (vMF, OAS) is real; the "JEPA" label is aspiration. Plan accordingly for E4.
- **flow-state, active-probe, fleet-homunculus** — small; mechanisms noted above but shallow.
- **mud-arena** — a gym, not interference-aware; its value is as a future judge, not as prior wave-evidence.
- **spectral-mechanics / slackwater-harmony / tensor-midi use floats** — they are the float versions of the fabric; that is precisely why they're seams (integer re-derivations), not dead ends.

---

## Synthesis — the five strongest cross-repo synergies

**S1 — The lattice trio is E1's missing geometry.**
*eisenstein + slackwater-lattice + base60-lattice + SuperInstance-papers (Thm 5.1).*
The integer hex lattice exists twice (Rust no_std, Python tested), with D₆ group
structure in the type system, exact norm a²−ab+b², a tested snapping algorithm
(`from_cartesian` rounding), angle snapping, and — in eisenstein's own
HexRoomMap — a `deadband_ring` and `map_temperature` describing a threshold
wave crossing hexes. Conservation on this lattice is *proven* (norm
multiplicativity, Thm 5.1).
**Unified experiment (E1-A₂):** move the interference tick from a scalar pulse
queue onto the A₂ lattice — pulses spread along the six unit directions
(the group/permutation state changes of the thesis, for free, from D₆);
cancellation measured by integer norm; snap target chosen by the tested
rounding rule. Falsifier: if adding geometry breaks cross-substrate
byte-identity (extend the 10/10 Py/C agreement to a third axis), the fabric
claim weakens to 1-D only.

**S2 — The ternary lane already chose E1's state algebra, and proved it unique.**
*ternary-tenforward + ternary-graph + ternary-memory + shoal's log₂3.*
Z₃ is proven the *only* group on {−1,0,+1}; E1's flagship state — "net==0 with
both signs live" — is exactly the ternary middle occupied *while* evidence
exists on both sides, a state no binary snap can name. Ternary-graph's signed
Laplacian is the interference bookkeeper with 2-bit edges (→ Verilog regs
directly). The anti-monoculture result (lock-in by tick 35 without mutation /
energy decay / trust reset) is a standing warning for any interference
governor, and Pisano period 8 offers a testable actuation cadence.
**Unified experiment (E1-Z₃):** recast per-cell pulse state as ternary under
cyclic addition; drive actuation every 8th tick vs every tick and measure
chatter/settle (tenforward's tunneling predicts 8 beats 1-tick); read out
decisions via ternary-ensemble voting. Falsifier: if 8-tick cadence does not
reduce chatter under stress params, the resonance claim doesn't transfer from
dialogue to snapping.

**S3 — The elephant crossover (paper 225's own E4) has half its parts built.**
*elephant + signal-chain + plato-vision-jepa + tensor-midi + the-tap + AI-Writings.*
Elephant's room physics — gravity, reverberation, ripple — is the interference
fabric's perception vocabulary: E1's delayed twin *is* reverberation; a joke
rippling *is* a pulse train; the sauna/plunge gap *is* an interference-signature
distance. tensor-midi already states the whole thesis in one sentence ("the
conversation IS the interference pattern of two quotient groups on the
12-cycle"). plato-vision-jepa contributes the deadband-gated sensor pattern;
the Tap corpus supplies real rooms with real histories; zeroclaw's hard-won
lesson (compare fields as edges/walks, never points) supplies the metric.
**Unified experiment (E4, as written in paper 225):** replace elephant's
keyword dials with dials reading an integer pulse field — compute the
sauna/plunge gap on Tap logs with vMF-κ floats vs integer pulse-state
signatures, blind-scored against AI-Writings labels. Falsifier: if integer
signatures can't reproduce the room separation κ achieves, the crossover
stays a metaphor. (Honest input: elephant's learned backbone is a stub —
this experiment needs the field math, not the stub.)

**S4 — The deadband-governor family is E1's missing control law.**
*slackwater-harmony + dual-band-guard + cell-cascade + the-listeners-ear + Spreader-tool + fleet-homunculus.*
E1 validated that pulse superposition beats impulse snapping, but emits
uniform pulses. The org has already worked out *tiered* responses
(harmony's gentle/moderate/critical by overshoot ratio), *refusal to consume
irreducible surprise* (dual-band-guard: oscillation >7 without decrease ⇒
never learn it — zero learnable parameters, the same zero-floats doctrine),
*proven decay shapes* (listener's-ear 30-day half-life refresh-on-recall;
ternary-memory's Ebbinghaus; E1 currently uses linear decay), *biological
inhibition* (homunculus GABAergic cooldown), and *count-threshold fate
changes* (cell-cascade myelination: ≥25 clean fires ⇒ promote to zero-cost
lookup; crab-traps' reef: 5th catch mints, 12th spawns).
**Unified experiment (the Interference Governor):** Φ computed as integer
superposition error energy; harmony's severity tiers selecting pulse
amplitude class; dual-band-guard's recurrence rule deciding snap-vs-hold on
cancellation states; exponential-halving integer decay (shift-only) vs
linear. Prediction to beat: tiered amplitudes + selective holding cut
constructive overshoot *without* losing the cancellation advantage (E1's
current numbers: ~20% fewer events, ~27% less debt, maxErr 61→39).

**S5 — Make the quilt's own TICK wave-native, then take it to metal (paper 225's E6).**
*quilt-verilog + quilt-foundation/vm-c + quilt-esp32 + quilt-substrate (witness log) + substrate-trainer + saddle/MerkleMesh.*
The TICK opcode is the frame; E1 is a candidate semantics *for* it; FORGET
is pulse expiry. Once TICK superposes, the whole port family (vm-c at
0.11 ms, wasm, Haskell, TS, esp32 at ~3 KB) becomes a cross-substrate
wave-bench, and quilt-verilog's sby-formal setup can prove interference
invariants (e.g., "cancellation states never increase ledger debt") the way
it proved opcode invariants. The witness log + substrate-trainer close the
learning loop (E5: ledger-as-field); saddle's double-entry ledger is the
debt theory. mud-arena offers the adversarial judge and crab-traps the
production reef if a fabric-native agent needs a world.
**Unified experiment (TICK-as-interference → E6):** implement the pulse
queue as TICK semantics in quilt-verilog, run twin cascades as two clocks
with interference resolution between them, formally prove the debt
monotonicity invariant; then port to quilt-esp32 and measure integer
phase-snap against real ADC noise — converting "our snapping is analog"
from metaphor to measurement, exactly as paper 225 §6 E6 specifies.

---

## Standing caution from the org's own history

zeroclaw's dissertation logs that the "room temperature as a point" unit
**died twice** under adversarial review; only the field-edge survived. E1's
lesson is the same shape: the unit that survived is not "a value snapped" but
"a superposition state" (net==0, both signs live). Any unified experiment
above should adopt the pre-registration discipline (kill bands, pre-stated
branch homes) before claiming the synoptic abstraction — the org has already
paid for that lesson once.
