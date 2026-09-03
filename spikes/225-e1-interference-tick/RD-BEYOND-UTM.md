# RD DOSSIER — BEYOND-UTM SUBSTRATES (Lane 1)

Scouted: 2026-09-02/03. Scope: cutting-edge (2023–2026) research on substrates where the UTM tape-head metaphor is the *wrong* abstraction — where state transitions are group actions, interference is the actuator, and symmetry is the instruction set.

Method note (honest): web_search quota died 3 queries in (Gemini 429). The scout continued via the arXiv export API (11 structured queries), GitHub search API, and direct page fetches — 16 distinct queries total. Breadth held; depth on non-arXiv venues (IEEE, Springer) is thinner than I'd like. Flags: [★] = strongest find; [NEAR] = adjacent, medium value; [DEAD] = checked and discarded.

Relevance frame: quilt = cells with 5 opcodes (qm_bind/link/effect/view/tick), actuated by an integer-only interference engine (spike trains, integer-halving decay, LCG noise, no floats). Thesis under test: group/permutation math, not UTM semantics, is the primitive.

---

## SEAM A — Reversible & conservative computing (Toffoli/Fredkin lineage)

**What it is.** Computation as *bijective* state transition: every step is a permutation of configuration space, no information is destroyed, no Landauer heat. Modern action: reversible CA classification, conservative many-body lattice dynamics, reversible circuits as pseudorandom permutation factories, quantum CA as the reversible endgame.

**Strongest finds**

1. [★] Haugland & Omland, *New classes of reversible cellular automata* (Nov 2024). Proper liftings: Boolean functions f on k bits that are bijective for every n — exactly the local rules of reversible CA. New families for arbitrary k; complete identification for k≤6.
   https://arxiv.org/abs/2411.00721
2. [★] Kasim & Prosen, *Deterministic many-body dynamics with multifractal response* (Nov 2024, PRR 2025). Momentum-conserving "parity check reversible CA" on bipartite lattices — integer, reversible, conservative, with phase-space fragmentation and multifractal spectra. This is a *worked integer conservative fabric*, not theory.
   https://arxiv.org/abs/2411.19779
3. [★] Shiraishi & Takesue, *Complete ergodicity in one-dimensional reversible CA* (2024, J. Stat. Phys. 2025). The complete ergodic-rule census for 3/4/5-state CA. If you want to know which reversible rules wash out structure, this is the lookup table.
   https://arxiv.org/abs/2408.06691
4. [NEAR] *k-wise independent permutations from random reversible circuits* (May 2024). Random Toffoli-ish circuits provably mix to strong pseudorandomness via log-Sobolev. Read: "reversible blocks + iteration = a hash function you already own."
   https://arxiv.org/abs/2406.08499

**Prediction for quilt.** Make `tick` a *block* (Margolus-partition) permutation rather than a point update, and reversibility becomes a static structural property, not something to test. Universality is then nearly free (block CA are Turing-complete; Fredkin's billiard lineage). Integer-halving decay plays the role of the only permitted entropy sink — reversible compute, dissipative measurement. That split (compute = permutation, readout = decay) mirrors exactly how QCA theory separates unitary evolution from measurement.

**E1 experiment (integer-only).** Add a Margolus mode to the harness: partition the ring into 2-cell blocks, alternate even/odd phase each tick, apply a bijective 2-lut (16-entry permutation table, e.g. swap or XOR-rotate) to each block; keep LCG noise and integer decay ON. Measure: (a) Hamming-distance autocorrelation of state history (reversible core should show recurrences; decay should give geometric return-time envelopes), (b) empirical 2-wise/3-wise independence of output bits vs. the log-Sobolev prediction from 2406.08499. Pure C ints, no floats. Success = recurrence structure appears before noise washes it, and independence matches at fixed iteration counts.

---

## SEAM B — Computation as group actions: Cayley lattices & CA groups

**What it is.** Casey's thesis has an academic twin: the school that treats a cellular fabric as algebra over a group G, lattice = Cayley graph, neighborhood = generating set, dynamics = group-ring convolution. Recent results are startlingly direct — including classifying *groups themselves* by their CA behavior.

**Strongest finds**

1. [★] Salo, *Word problems and embedding-obstructions in cellular automata groups on groups* (2025). Defines **CA groups** — groups *of* reversible CA. Word problems PSPACE-hard (on all but nilpotent G under the Gap Conjecture); lamplighter CA groups are co-NEXPTIME-hard; no embedding of CA groups across dimensions. Computation *is* the group, and its complexity class is computable.
   https://arxiv.org/abs/2503.05572
2. [★] Rollier & Baetens, *Exact Lyapunov spectra of affine cellular automata* (Jun 2026). For XOR-family rules the Lyapunov spectrum is **exact** — log singular values of the (constant) Jacobian = log |adjacency spectrum|, no simulation, any dimension, unified by "periodic lattice = Cayley graph of an abelian group." A recipe for exact integer chaos analysis.
   https://arxiv.org/abs/2606.14521
3. [★] Barbieri, García-Ramos & Taati, *Cellular automata, percolation and dynamical dichotomies* (2024). Equicontinuity-vs-sensitivity dichotomy holds on G iff G has trivial percolation threshold iff G is virtually cyclic. **The lattice's group structure decides whether your fabric is stable or chaotic.** Directly actionable for E1 topology choices.
   https://arxiv.org/abs/2410.23770
4. [NEAR] Yang, *Closed image characterizations of locally finite groups via CA* (Jun 2026). G locally finite ⟺ every CA over G has closed image. Group property read off automaton behavior, and vice versa.
   https://arxiv.org/abs/2606.22740
5. [NEAR] Perinotti, *Cellular automata in operational probabilistic theories* (2019, Quantum 2020) — the cleanest theorem in the pile: **homogeneity of an update rule forces the system to live on a Cayley graph.** The "group" in cellular automata isn't optional; it's derivable.
   https://arxiv.org/abs/1911.11216

**Prediction for quilt.** quilt's lattice should be declared as a group G with generating set S = neighbor offsets, and `qm_link` interference should be integer convolution in ℤ[G] (each neighbor's spike contributes spike[σ(g⁻¹h)] — still just table lookups and adds). Then: (a) sensitivity/equicontinuity is decided by G before any run (Barbieri), (b) chaos exponents are computable exactly from integer matrix powers of the adjacency (Rollier), (c) the whole fabric gets a group-theoretic "ISA": tick = elementwise group action, link = ℤ[G]-module op. This is the strongest mathematical upgrade path found anywhere in this scout.

**E1 experiment (integer-only).** Swap the harness lattice from a plain ring to Cayley graphs of three groups: ℤ_n (abelian), dihedral D_n (non-abelian), and ℤ_n×ℤ_2 (virtually cyclic — predicted equicontinuous by Barbieri). Run the same integer spike-interference tick on all three. Measure integer Lyapunov proxy: track growth of single-bit-flip perturbation support (count of differing sites) over time — exact, float-free. Prediction to falsify: D_n fabric goes sensitive, ℤ_n×ℤ_2 fabric stays equicontinuous, ℤ_n in between. If confirmed, quilt inherits a *design theorem*: choose dynamics class by choosing the lattice group.

---

## SEAM C — Excitable-media automata at criticality (Greenberg–Hastings lineage) + CA-as-ML-substrate

**What it is.** The Greenberg–Hastings model (resting→firing→refactory integer states) is quilt's closest ancestor, and 2024–2026 produced a genuine renaissance: finite-size scaling laws, information-maximization theorems at criticality, and CA substrates doing ML.

**Strongest finds**

1. [★] Kilic & Akan, *Neural-Inspired Multi-Agent Molecular Communication Networks* (Jan 2026). GH automata communicating via a diffusive medium: **pairwise and collective mutual information peak exactly at the second-order phase transition.** Integer threshold automata maximize channel capacity at criticality — a theorem-shaped target for E1's threshold sweep.
   https://arxiv.org/abs/2601.18018
2. [★] Almeira, Martin, Chialvo & Cannas, *Susceptibility for extremely low external fluctuations and critical behaviour of Greenberg–Hastings* (2025, v3 2026). Spontaneous activation probability acts as the external field conjugate to the activity order parameter, with clean finite-size scaling. **This is E1's LCG noise term, already modeled.** The tuning law exists.
   https://arxiv.org/abs/2506.22629
3. [★] Bocchese, Giacobbo, Wiles et al., *Emergent Models: Intelligence from Tiny Substrates* (Aug 2026). Proves some CA substrates are **latent-universal**: fixed update rule + fixed interface, any partial computable function realized by varying only the initial condition. Tens–hundreds of parameters. This is the quilt thesis ("the 5 opcodes are fixed; computation lives in state") with a proof attached.
   https://arxiv.org/abs/2608.14019
4. [★] Zhang & Levin, *Intelligence from Learnable Novelty* (Jul 2026). A differentiable reservoir-based "learnable novelty" estimator — no labels — ranks **rule 110 highest of all elementary CA**, and its gradient drives an NCA into a **soliton regime** (the colliding wavefronts rule 110 computes with). A self-tuning knob that seeks the compute-bearing regime.
   https://arxiv.org/abs/2607.18433
5. [NEAR] Almeira et al., GH with excitatory + inhibitory units (Dec 2023): first-order transitions, hysteresis, inhibitory fraction threshold f_t→½. Blueprint for quilt cell types.
   https://arxiv.org/abs/2312.17645
6. [NEAR] Saha & Wang, *Learning PDE time-stepping with NCA* (Aug 2026): local homogeneous rule beats FNO/PDE-Net long-horizon on 5 canonical PDEs.
   https://arxiv.org/abs/2608.30328

**Prediction for quilt.** The interference engine's noise/decay/threshold triple should have a *computable* sweet spot: LCG noise = conjugate external field (Almeira scaling), MI/capacity maxima = critical point (Kilic & Akan), soliton collisions = the substrate's data structures (Zhang & Levin). E1 shouldn't tune by hand — it should tune by scaling law.

**E1 experiment (integer-only).** Criticality sweep with exact integer statistics: for LCG noise rate p across 3–4 decades and decay halvings d ∈ {1,2,3}, run N=10k ticks; measure activity fraction (order parameter) and single-site→neighbor MI (integer histogram estimate, no floats — bin the spike counts). Locate the transition by maximum MI, then run three lattice sizes and fit finite-size scaling to extract the exponent as a rational. Deliverable: a lookup table "noise rate → channel capacity" for the E1 actuator, and a yes/no on whether MI-peaks-at-transition survives integer quantization. This is the cheapest experiment in the dossier and should run first.

---

## SEAM D — Compositional / categorical computation: operads, string diagrams, rewrite-as-evaluate

**What it is.** Computation where evaluation *is* diagrammatic rewriting: operads (many-in/one-out composition), string diagrams, complete calculi. The 2025–2026 surprise: operads just went applied.

**Strongest finds**

1. [★] Bottman, Liu & Richardson, *Operads for compositional reasoning in LLMs* + companion *Operadic consistency* (Jun 2026). Questions-as-operations, decomposition-as-composition, models-as-algebras; **operadic consistency** (direct answer ≡ composed answer) correlates r≈0.86–0.94 with accuracy across 12 LLMs. Composition-consistency is a *measurable health signal* for any compositional system.
   https://arxiv.org/abs/2606.13634 / https://arxiv.org/abs/2606.13649
2. [★] Wang, East, Shaikh, Yeh, Poór & Coecke, *Spin-ZX calculus* (Nov 2025). Complete diagrammatic language for SU(2) — permutational computing amplitudes derived by *re-writing pictures*, including Clebsch–Gordan decomposition. Also explicitly covers "permutational computing."
   https://arxiv.org/abs/2511.06012
3. [NEAR] *Sutra: tensor-op RNNs as a compilation target for VSA* (May 2026). A typed functional language whose compiler β-reduces *everything* (control flow, string I/O) into one fused tensor graph over frozen embeddings; rotation-bind/unbind/bundle lower to tensor ops. Proof that "weird substrate + real compiler" is buildable.
   https://arxiv.org/abs/2605.20919

**Prediction for quilt.** The 5 opcodes are naturally an operad: qm_bind/link = binary ops, effect = unary, tick = the composition rule, view = the counit/readout. The payoff isn't elegance — it's **operadic consistency as a static checker**: integer traces must satisfy bind∘unbind = id, commutation of ops on disjoint cells, associativity of link. Violations = substrate bugs, catchable without simulating semantics. Also predicts cell programs should be *typed by arities*, catching malformed opcode streams at load time.

**E1 experiment (integer-only).** Trace-verification harness: log every opcode invocation with (cell, opcode, args, pre/post state words) for a fixed seed. Then verify three integer identities across the whole trace: (1) bind then unbind returns the original state word exactly (count violations — must be 0 by construction; any nonzero = harness bug or decay leakage misclassified), (2) ops on disjoint cells commute (state words after A∘B vs B∘A), (3) link associativity on triples. Report violation counts as a function of decay halvings — where does decay break algebraic law? This turns quilt's algebra from aspiration into a testable invariant.

---

## SEAM E — Reaction-diffusion & geometric computation

**What it is.** Physically-embedded computation in continuous excitable media (Belousov–Zhabotinsky glider guns, slime-mold solvers, Adamatzky's collision-based computing).

**Honest assessment: mostly [DEAD] as a *live research* seam.** arXiv traffic on "reaction-diffusion computing" proper is 3 papers in 15 years (2009 BZ glider guns: https://arxiv.org/abs/0902.0587; 2015 Physarum cytoskeleton: https://arxiv.org/abs/1503.03012). The field's energy migrated into (a) excitable-media *automata* — Seam C — and (b) dissipative oscillator networks: [NEAR] *Between Amnesia and Chaos: memory–stability–expressivity trilemma for dissipative oscillator networks* (Jun 2026), https://arxiv.org/abs/2606.09929 — the integer-decay analog of quilt's tick, formalizing why you can't have long memory AND stability AND expressivity at once. GitHub: reaction-diffusion repos are WebGPU/Unity shader demos (robert-leitl/webgpu-reaction-diffusion, 29★; andydbc/unity-reaction-diffusion, 26★). No maintained compute substrate found.

**Prediction for quilt.** Nothing here beats Seam C's discrete versions of the same physics. Fold the trilemma in as a design principle (decay rate = the knob trading memory vs stability vs expressivity; pick per-task, not per-fabric).

**E1 experiment.** None dedicated — covered by Seam C's sweep, which IS the discrete reaction-diffusion experiment. Logged as a dead end with a redirect.

---

## SEAM F — VSA / hyperdimensional permutation computing (the closest engineering sibling)

**What it is.** Vector Symbolic Architectures: bind = permutation/XOR-multiply, bundle = integer superposition, read = similarity. quilt's interference engine *is* a sparse, spatialized VSA — and the 2026 literature is doing exactly this math in silicon and radio.

**Strongest finds**

1. [★] Chen, Song, Wu, Rajendran & Simeone, *Neuromorphic NOMA remote inference via VSA* (Jul 2026). Each device binds its spike feature map with a **device-specific permutation key**; concurrent transmission superposes in the air = the bundling op, done by physics; SNN decodes with learned unbinding. Permutation keys + spike superposition + integer-ish readout — **quilt's op set, published as a radio protocol.**
   https://arxiv.org/abs/2607.22155
2. [★] Pence, Yamada & Singh, *Recursive binding on a budget: subspace carving in order-p tensor memories* (ICML 2026). Binding theory done right: TPR shown to be a special case of binding in Clifford algebra; recursive binding with constant memory. (Uses real subspaces — the integer-only port is *our* problem, noted honestly.)
   https://arxiv.org/abs/2606.11391
3. [NEAR] *Quantum Hyperdimensional Computing* (Nov 2025): HDC's bind/bundle map natively onto quantum ops — the bridge if quilt ever grows a quantum lane.
   https://arxiv.org/abs/2511.12664

**Prediction for quilt.** `qm_bind` should be *defined* as permutation composition on state words (cyclic shifts / modular index arithmetic mod 2^w). Then: unbinding is exact integer inverse (zero error, no float similarity needed), bundling = the existing spike superposition, and the entire VSA capacity/results literature becomes directly citable for quilt's behavior. NOMA-NC is the existence proof that this stack runs on real constrained hardware.

**E1 experiment (integer-only).** Implement qm_bind as cyclic word rotation by a per-cell key derived from cell id (rotate-left k mod w on the state word); qm unbind = inverse rotation. Test: (1) bind/unbind roundtrip = exact equality across 10⁶ random words (must be 100%, any failure = bug), (2) capacity curve — bundle M bound pairs via integer superposition, decode by re-binding with each key and integer-threshold read; plot M* vs decay halvings. Compare capacity slope to VSA theory's √D scaling (integer fit). Deliverable: quilt's binding algebra with an exactness guarantee, plus its first capacity number.

---

## SEAM G — "Beyond Turing" proper: supertasks, ruliology, hypercomputation

**Honest assessment: graveyard, with two usable stones.**

- [DEAD] *On the Possibilities of Hypercomputing Supertasks* (May 2025): Zeno machines can't exist in the actual world; Church–Turing survives. https://arxiv.org/abs/2505.14698 Don't chase literal beyond-Turing; the productive reading of Casey's thesis is "non-UTM *primitives* that are still Turing-equivalent but algebraically better-factored" — which is exactly what Seams A/B/F supply.
- [NEAR] Wolfram's ruliology line: *Ruliology: Linking Computation, Observers and Physical Law* (arXiv 2308.16068, https://arxiv.org/abs/2308.16068) and *What's Really Going On in Machine Learning? Some Minimal Models* (Aug 2024, https://writings.stephenwolfram.com/2024/08/whats-really-going-on-in-machine-learning-some-minimal-models/) — computational irreducibility and minimal computational models of learning; good vocabulary ("rulial space"), no integer math to steal.
- [NEAR] ½BQP — *The Space Just Above One Clean Qubit* (Oct 2024, https://arxiv.org/abs/2410.08051): permutational computations on entangled inputs as a *complexity class*. Useful citation: "permutation-only computation" is a formal object, with known power and known limits (no Grover).
- QCA-from-duality cluster (2607.21728, 2607.21698, 2608.26456): deep-math confirmation that reversible cellular fabrics are classified by symmetry groups (SL(2,ℤ_N), Clifford fusion rules) — supports Casey's thesis, but porting to integer fabrics is a research program, not an experiment. Park it.

---

## Ranking — top 3 seams by breakthrough potential for the E1 lineage

**#1 — Seam B (Cayley-lattice group algebra).** It converts "interference" from folklore into exact, integer-computable mathematics (exact Lyapunov spectra, group-dichotomy theorems), requires only swapping the lattice's algebra, and carries three 2024–2026 theorems that make *falsifiable predictions about E1's own dynamics class*. Highest ceiling: quilt inherits an actual design theory (pick G, pick dynamics class).

**#2 — Seam C (criticality-calibrated excitable automata).** Cheapest to run, strongest empirical law set: LCG-noise-as-external-field scaling, MI-peaks-at-transition, solitons as data structures, and a latent-universality proof for fixed-rule substrates (the quilt thesis, formalized). This is the seam that tells us *where to park the actuator's knobs*, and it ships a measurement protocol today.

**#3 — Seam F (VSA permutation binding).** Strongest near-term engineering payoff: exact integer bind/unbind, capacity curves, and a 2026 hardware precedent (NOMA-NC) running the identical algebra on constrained silicon. It upgrades quilt's first-class opcode from "clever hack" to "instance of VSA, with citations and theory."

Runner-up — Seam A (Margolus-reversible ticks): fold its block-partition experiment into the Seam B rung; full reversible-everything is the right *destination* but premature as the next step. Seam D (operad checker) is the best long-term software-engineering investment but doesn't rank top-3 for *breakthrough*.

## Dead ends (so nobody re-walks them)

1. Literal hypercomputation/supertasks — negative results (2505.14698). The Church–Turing wall holds; "beyond UTM" must mean "better-factored primitive," not "more computable."
2. Reaction-diffusion computing as active research — dormant since ~2015 on arXiv; GitHub side is shader demos. Its discrete successor (Seam C) ate its lunch.
3. Edge-of-chaos *as a naive heuristic* — 2607.17909 (https://arxiv.org/abs/2607.17909) shows the best-performing reservoir radius does NOT coincide with the Lyapunov edge for forecasting tasks. Tune by measured MI/capacity (Seam C experiment), not by folklore "edge."
4. Local-only NCA for sequential/symbolic tasks — TextNCA (https://arxiv.org/abs/2608.02050) honestly reports losing to Transformers at matched params (60.3 vs 44.7 PPL). Don't oversell quilt for language-style tasks; its lane is spatial, dynamical, control-style work.
5. Reversible-computing hardware industry check — could not verify Vaire Computing's site from this box (DNS fail). Status unknown; treat any energy-payoff claims as unverified until checked on another connection.
6. GitHub "block/partitioned CA" toolchains — student projects and one Indian Summer School repo (thealekhya/Cellular-Automata-2025); no maintained library worth adopting.

## Search log (for reproducibility)

web_search (Gemini, quota died after #2): reversible CA 2024–2025 ✓, beyond-Turing 2025 ✓, 1× rate-limited ✗. arXiv API: "permutation computing", "vector symbolic architectures", "reversible cellular automata", "reaction-diffusion computer/computing", "neural cellular automata", Greenberg–Hastings, operad+computation, CA+Cayley graph, "quantum cellular automata", CA+machine learning, edge-of-chaos+reservoir. GitHub API: reversible CA, block/partitioned CA, hyperdimensional computing, VSA, rule 110, reaction-diffusion. Direct: wolframphysics.org ✓, vairecomputing.com ✗ (DNS).

— Lane 1 scout, 2026-09-03
