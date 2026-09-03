# RD — Physical & Analog Compute Substrates (Lane 2)

*Deep scouting for quilt's integer-only "true analog" engine (paper 225, batten-wave
doctrine) and the E1 interference tick. 2026-09-02/03. Companion to lane-1 doc.*

**Question:** what 2023–2026 work on computation that *exploits* physics-like dynamics
(reservoirs, Ising solvers, thermodynamics, oscillators, stochastic/hyperdimensional
integer algebra, plasticity) transfers to an integer-only cellular fabric on
ESP32-class hardware and local GPUs?

**Method note:** Gemini-backed web_search was quota-blocked (429) the whole session;
the sweep ran on the arXiv API, the GitHub search/org API, and raw README fetches
instead — 12 structured queries across all ten assigned lanes. Coverage is
arXiv-biased; no vendor-blog claims below without a paper or repo attached.

**Ranking at the bottom: top 3 by (impact × doable-tonight).**

---

## Lane 1 — Physical Reservoir Computing (PRC)

**Seam.** A fixed, untrained nonlinear dynamical system + one *trained linear readout*
does temporal computation. That is architecturally quilt's claim wearing physics
clothes: the fabric is the reservoir, the snap/measure layer is the readout, nothing
inside the loop is trained or floated.

**Strongest recent artifacts**

- **Design rules for physical reservoirs** (pneumatic soft robot, 36 matched trials):
  topology, stiffness, and sensor count must be co-designed; **2–3 well-placed
  sensors capture essentially all attainable benefit**; "stronger excitation cannot
  recover diversity that poor design already removed." arXiv:2609.02157.
  https://arxiv.org/abs/2609.02157
- **Dynamics-matched reservoir** — use the *target system itself* as the reservoir
  (traffic network governed by a car-following model predicts undersensed traffic;
  echo-state property proven for slow inputs; beats LSTM on accuracy AND training
  time). arXiv:2607.27371. https://arxiv.org/abs/2607.27371
- **Co-optimizing physical reservoirs against digital reference dynamics** (+33.7%
  mean over unoptimized; pretraining a *physical* system against a digital teacher).
  arXiv:2608.00484. https://arxiv.org/abs/2608.00484
- **Causal information filtering via asymmetric coupling** — coupling directionality
  purges anomalous information through local saddle-node bifurcations while
  preserving the rest of the reservoir. Fault tolerance *from* physics, not added
  to it. arXiv:2608.26741. https://arxiv.org/abs/2608.26741
- Reviews/substrates: magnonic-optoelectronic oscillator reservoir (STM and
  nonlinearity as **separate components**) arXiv:2608.16388; heterogeneous magnetic
  nanorings (geometric heterogeneity = expressivity) arXiv:2608.08879; biomimetic
  scale metabeams (mechanical, NARMA-10) arXiv:2608.02856.
- Code: **reservoirpy** ★651, pushed 2026-09-01 — https://github.com/reservoirpy/reservoirpy ;
  **EchoTorch** ★500 — https://github.com/nschaetti/EchoTorch

**Quilt-transfers**

- The pneumatic paper's law — *a few strategic sensors beat many redundant ones* —
  is E1's twin-count argument in hardware form: quilt should budget **which cells
  instrument a channel**, not maximize instrumentation.
- Dynamics-matching says: to predict a system, run a *cheap integer model of that
  same system* as the computer. Quilt's `reality()` walk IS a dynamics-matched
  reservoir for its own sensing problem. This is the strongest theoretical
  framing quilt can borrow: prove echo-state/fading-memory for the pulse-queue
  state, and E1's interference arm becomes a certified reservoir.
- Asymmetric coupling = a **directed** batten-wave: corrections flow
  upstream→downstream and a bad channel bifurcates away instead of poisoning the
  fabric. Maps to cell-neighborhood orientation in quilt.

**Tonight-experiment**

- Integer ESN bake-off (CPU, ~1h): fixed random sparse integer matrix W (entries
  ±1..±8), state update `x += (Win·u + W·x) >> 3` with saturating int16 clamp,
  linear ridge readout on NARMA-10 (generate with integer arithmetic too). Compare
  NRMSE vs a float ESN from reservoirpy at 100/300/1000 units. Success criterion:
  integer reservoir within 2× float NRMSE — then the readout is the only float
  left, and it's replaceable by integer least squares (fdiv contract).

---

## Lane 2 — Ising Machines & Hopfield-Style Solvers

**Seam.** Let energy minimization *settle* instead of executing search. Hopfield
dynamics is the integer-tick ancestor of everything here, and 2023–2026 work is
fixing exactly the problem quilt cares about: **how to update spins in parallel
without the network oscillating** — which is E1's question with ±1 spins.

**Strongest recent artifacts**

- **Inertia term makes fully-parallel synchronous p-bit updates work** (Zhu, McMahon
  et al.): thought-impossible parallel dense updates, fixed by adding an inertia
  term to spin dynamics; FPGA-verified; ≈35× average speedup at N=200, best case
  150×; passes 5G MIMO real-time latency. arXiv:2604.17109.
  https://arxiv.org/abs/2604.17109
- **Mean-field oscillator Ising machines** (Bullo et al.): complete classification
  of limit solutions — phases cluster into at most four groups; for almost all
  parameters only **binarized (0/π) fixed points are stable**, i.e. feasibility
  readout is guaranteed by the dynamics itself. arXiv:2608.16025.
  https://arxiv.org/abs/2608.16025
- **CMOS Ising chips (45 spins) in a robotics planning stack**: coefficient
  quantization + spin merging + spin-budget branching to fit tiny hardware; routes
  within 9% of classical at **130× lower energy**. arXiv:2608.06803.
  https://arxiv.org/abs/2608.06803
- **Basin-preserving discretizations of modern Hopfield retrieval** — *which
  time-discretizations keep the basins of attraction intact* (energy cells, escape
  energy, certified overrelaxation window). Reproducible code on Zenodo.
  arXiv:2608.21304. https://arxiv.org/abs/2608.21304
- Hopfield-as-effective-theory book chapter with reproducible numerics (capacity,
  spinodal α≈0.138, attention limit): arXiv:2609.02195.
- E-MVL sparsified-connectivity Ising (FPGA, 6× faster than SA, 1600 spins exact
  where SA caps at 400): arXiv:2604.04606. Unified p-bit update-dynamics cost
  landscape (**3–4-bit DACs sufficient**): arXiv:2604.01564. Time-dimensional
  exchange coupling (couple *successive states of one network* instead of
  replicating hardware): arXiv:2608.21753. Attractor-keyed memory (the settling
  *signature* of a physical selector becomes the memory address): arXiv:2603.17049.

**Quilt-transfers**

- **The inertia result IS the interference tick, published.** E1's pulse queue is a
  decaying memory of past corrections — an inertia term. Lane 2 says: that term is
  precisely what licenses *synchronous parallel* updates of a conflict-prone
  fabric. Quilt's interference arm should be pitched as "inertia-regularized
  parallel relaxation," with E1's counters (cancellations, overshoot) as the
  observable signatures.
- Basin-preserving discretization is the E1 divergence-audit story for Hopfield:
  integer tick = Euler step; the escape-energy bound tells quilt *when its own
  quantized tick provably keeps the attractor basin* — a certificate target.
- CMOS-Ising coefficient quantization → quilt's ledger debt budget: the paper's
  spin-budget branching is a scheduling policy for which conflicts get resolved
  this tick — exactly the interference tick's job.
- 0/π-binarization theorem: a relaxation fabric whose *stable* states are the
  measurable ones is quilt's "snapping without floats" proven stable — snapped
  (binarized) fixed points are the only attractors worth having.

**Tonight-experiment**

- Inertia-pbit.py (CPU/GPU, 2–3h): N=100–500 Max-Cut (G-set or random), three arms:
  (a) sequential Gibbs, (b) naive synchronous update, (c) synchronous + inertia
  `m_i(t+1) = m_i(t) + I_i − m_i·decay` all in int32. Measure TTS and best-cut vs
  baseline. Prediction from literature: (b) oscillates/underperforms, (c) ≥ (a).
  If (c) wins, E1's pulse queue has a solver-grade justification.

---

## Lane 3 — Thermodynamic Computing (Extropic, Normal Computing)

**Seam.** Use thermal fluctuation as the sampling engine; answer = time-averaged
statistics of an equilibrating trajectory. 2026's twist that matters to quilt:
**the field itself proved you can get the thermodynamic *method* on digital integer
hardware** — fluctuation is a design pattern, not a physics dependency.

**Strongest recent artifacts**

- **CN101 — a *digital* thermodynamic computer chip** (Extropic team, incl. Crooks,
  Coles, Aifer, Duffield, Sbahi): substrate-independent equilibration formalism
  (design object = ergodic generator L*), implemented as **discrete accumulator
  dynamics with stochastic-computing principles on standard CMOS**; VAEs and flow
  matching; precision is a run-time knob ("run longer = more precise");
  **sequential parallelism** — dependent pipeline stages run concurrently.
  arXiv:2608.00754. https://arxiv.org/abs/2608.00754
- **Thermal noise is algorithmically redundant for convex problems** — thermodynamic
  matrix inversion ≡ preconditioned gradient descent to first order; deterministic
  version is 100,000× faster than stochastic Thermox simulation while competitive
  with Newton–Schulz. arXiv:2608.09743. https://arxiv.org/abs/2608.09743
- **Extropic THRML** ★1145 — JAX library for block-Gibbs sampling on sparse
  heterogeneous graphs; compiles factors to a compact global state, maximizes
  array-level parallelism; explicitly the prototyping surface for future Extropic
  silicon. https://github.com/extropic-ai/thrml (cited paper: arXiv:2510.23972;
  ecosystem ports: thrml-rs, Thermoputer, extropic Max-Cut tests)
- **Normal Computing thermox** ★69 — exact OU processes in JAX; thermodynamic
  linear algebra suite (solve/inv/expm via OU sampling).
  https://github.com/normal-computing/thermox (paper arXiv:2308.05660)
- Thermodynamic-freedom analysis (Wasserstein speed limits; within 40% of
  thermodynamic efficiency without accuracy loss): arXiv:2608.27938.

**Quilt-transfers**

- **CN101 is the doctrine-level validation of quilt's roadmap**: equilibration-style
  computation, implemented with *integer accumulators + stochastic bitstreams* on
  ordinary CMOS, with precision-as-runtime. Quilt's snap ledger is the same shape:
  run the tick longer, converge tighter. Cite it as the proof the lane exists
  outside analog substrates.
- The redundancy result (2608.09743) is a **warning and a gift**: for convex
  settle-to-answer problems the noise buys nothing — quilt's deterministic
  interference tick is not missing "real physics"; noise only earns its keep for
  *sampling* workloads (generative, annealing). Quilt should claim both modes
  explicitly: deterministic tick for settling, LCG-noise tick for sampling.
- THRML's block schedule (two-color block Gibbs) is a concrete alternative to
  E1's rotation order: partition cells into blocks, update blocks synchronously —
  the interference tick is the block-coupling mechanism.

**Tonight-experiment**

- `pip install thrml` on the 4050; replicate the README Ising chain, then replace
  the even/odd two-color blocks with **latency-shaped blocks** (cells grouped by
  twin-delay class). Sweep block size vs sample quality (magnetization MSE vs
  exact enumeration on N≤20). Log wall-clock per 1k samples on GPU. This measures
  whether quilt's twin-latency structure can *be* the parallel schedule.

---

## Lane 4 — Oscillator Computing

**Seam.** Coupled oscillators compute by phase-locking; sub-harmonic injection
locking solves Ising natively in silicon (CMOS + MEMS/VO₂).

**Strongest recent artifacts**

- Mean-field OIM theory (see lane 2, arXiv:2608.16025) — gradient-flow structure
  and the binarization threshold.
- **Kuramoto Neural Operator** — solve PDEs *through* a latent field of coupled
  oscillators; error tracks synchronization level. GPU-friendly operator learning
  without UTM-style matrix stacks. arXiv:2608.10234. https://arxiv.org/abs/2608.10234
- VO₂ relaxation-oscillator phase noise (what the analog substrate actually costs;
  square-wave sync beats sinusoidal injection for phase noise) arXiv:2607.27447;
  Analog Interaction Systems for generative modeling (4-bit sparse oscillator
  networks, FID 27.6 MNIST, ~23 µJ/image, 2 orders below digital) arXiv:2606.27294;
  Optimal equilibrium-propagation training on a spatial photonic Ising machine
  arXiv:2606.13454.

**Quilt-transfers**

- Phase = integer sector arithmetic: a Kuramoto phase θ is quilt-representable as
  a fixed-point angle (e.g. θ ∈ ℤ_256). Phase-difference coupling is then integer
  subtraction + proportional pull — no trig, use a quarter-wave integer sine table
  (256 entries, u8) if a sine is needed. Coupled-oscillator solvers port to
  integer fabric *cleanly*; the mean-field theorem says the integer phase clusters
  are the stable states.
- KNO's finding that solution quality tracks a **collective synchronization
  observable** gives quilt a health monitor: define fabric sync σ (spread of cell
  phases) and gate regime-switching (E4's calm/conflicted dial) on σ crossing a
  threshold.

**Tonight-experiment**

- Integer-Kuramoto annealer (CPU, 1–2h): N=200 spins as θ∈ℤ_64, update
  `θ_i += (K/deg)·Σ_j J_ij·sin_tab[(θ_j−θ_i) mod 64] >> 4`, anneal K downward,
  read out s_i = sign of cos θ. Same Max-Cut instances as lane-2 experiment.
  Compare TTS vs the p-bit arms. Bonus: count "binarization events" (|cos θ|
  crossing 96/128) and check they cluster before convergence — the literature's
  feasibility theorem, visible in integers.

---

## Lane 5 — In-Memory Analog MatMul (Integer/Quantized Claims)

**Seam.** Crossbar MVM does the matmul in physics; the whole 2024–2026 game is
how *few bits* the ADCs and weights can use. Every "how quantized can it be"
result is a seam for an integer fabric.

**Strongest recent artifacts**

- **Compute-SNR-optimal ADC design for AIMC** (IBM) — prior work overestimates ADC
  precision needs by mis-modeling quantization error as input-independent noise;
  exact minimum-precision analysis. arXiv:2507.09776. https://arxiv.org/abs/2507.09776
- **Hybrid digital–analog Krylov preconditioning** (Gokmen/Horesh, IBM): analog
  crossbar does the noisy-quantized preconditioner applications, digital does
  precision-sensitive ops, fGMRES absorbs the inexactness. arXiv:2606.17227.
  https://arxiv.org/abs/2606.17227
- N-ary MTJ crossbars: MNIST 93.56% with 4-state cells; **optimal number of states
  per cell balances quantization vs resolution** — more states ≠ better.
  arXiv:2604.26979. Boundary-suppressed K-means activation quantization: 3–4-bit
  ADCs suffice across ResNet/VGG/DistilBERT. arXiv:2603.10540.

**Quilt-transfers**

- The N-ary result is quilt's discrete-basis doctrine quantified: an *optimal*
  finite state count exists per cell; quilt's "measure, don't float" should target
  that optimum rather than maximize resolution. E1's dyadic-envelope certificate
  is the same certificate the crossbar people compute for their cells.
- Hybrid Krylov pattern → quilt division of labor: analog-ish superposition tick
  for bulk state updates, exact integer ops (fdiv, 64-bit products) for the
  precision-sensitive verdicts (the settle/deadband decisions). Already quilt's
  shape; now it has an industrial citation.

**Tonight-experiment**

- Bit-floor sweep (CPU, 30min): take the integer ESN from lane 1 (or lane-2
  Ising couplings), sweep state/coupling bit-widths 2..8; plot NRMSE/cut-quality
  vs bits; find the knee. Mirrors the N-ary states-per-cell optimum and gives
  quilt's u8/16 cell contract an empirical floor table.

---

## Lane 6 — Extreme Learning Machines (Fixed Random Features)

**Seam.** Unreasonably effective, embarrassingly cheap: random fixed hidden layer,
solve one convex least-squares. The readout half of reservoir computing without
the reservoir.

**Strongest recent artifacts**

- **Optical free-space ELM implementing cellular automata** — SLM encodes the
  evolution rules, coherent propagation does the compute: ELM *as a CA substrate*
  (Rule 110-class, Game of Life, 2D Turing machines). arXiv:2609.00933.
  https://arxiv.org/abs/2609.00933
- QRC↔QELM continuum: encoding length interpolates reservoir (memory) ↔ ELM
  (memoryless); **best reservoirs sit at the edge of chaos, and dynamical regime
  beats connectivity** ("what temporal processing requires is the regime, not the
  wiring"). arXiv:2608.28440. https://arxiv.org/abs/2608.28440
- Fourier Feature Networks beat ELMs on PDE solving (random *sin/cos* bases +
  least squares — table-lookup-friendly). arXiv:2608.14733. ELMZip: ELM onboard
  satellite compression (convex LS, resolution-free). arXiv:2608.06942.
  Over-the-air ELM on metasurfaces. arXiv:2608.27137.

**Quilt-transfers**

- An ELM whose random features are *cell-neighborhood basis functions* (pulses,
  decays, cancellation counts — E1's existing counters) is a zero-training fabric
  readout: the interference tick already computes the features; only the final
  integer least-squares needs fitting. Edge-of-chaos finding licenses the
  calm/conflicted regime dial (E4) as the *primary* tuning axis.

**Tonight-experiment**

- Feature-tick ELM (CPU, 1h): regress `reality(t+8)` from E1's per-tick integer
  feature vector (live pulse sum, |queue|, cancellation flag, twin disagreement)
  collected from `e1.py run()` traces; solve integer ridge (exact via small float
  LS then round — or pure int via Cramer on ≤4 features). Compare NRMSE vs
  autoregressive baseline. If integer features beat AR, the tick itself is the
  model — the strongest possible paper-225 claim.

---

## Lane 7 — Stochastic Computing (Bit-Stream Arithmetic)

**Seam.** Represent numbers as bit-stream probabilities; multiply with an AND
gate; precision grows with stream length (CN101's substrate). Fault-tolerant by
construction — a flipped bit is a 1/stream error, not a word corruption.

**Strongest recent artifacts**

- **DS-CIM** — digital stochastic compute-in-memory: signed MAC via OR-accumulation
  with 2D-partitioned shared PRNG, single-cycle mutual exclusion; INT8 ResNet18
  at 94.45% CIFAR-10, 0.74% RMSE (or 3566 TOPS/W variant at 3.81%). arXiv:2601.06724.
  https://arxiv.org/abs/2601.06724
- **FALCON** — MTJ in-memory stochastic architecture absorbing up to 30% injected
  noise; *deterministic bit mapping* removes RNG hardware. arXiv:2609.00701.
  https://arxiv.org/abs/2609.00701
- **ReSCom** — SNN accelerator: stochastic multiplication but **exact fixed-point
  add/sub**; LIF/IF/synaptic neuron in one reconfigurable cell; 0.05 mJ/image
  MNIST on Artix-7; stream length = accuracy/energy dial at runtime.
  arXiv:2606.13560. https://arxiv.org/abs/2606.13560
- Invertible stochastic logic (run gates backward for factorization — includes
  fabricated ASIC measurements). arXiv:2603.27030. ASTRA photonic stochastic
  transformers. arXiv:2604.09759.
- Code: **scgrad** — differentiable stochastic-computing primitives for PyTorch
  (train natively SC-aware): https://github.com/g-lanza/scgrad ; BITS
  (stochastic + HDC for Earth observation): https://github.com/Lime337/BITS-Bitstream-Intelligence-for-Space-to-Soil-Earth-Observation

**Quilt-transfers**

- ReSCom's split is quilt's split: *stochastic where cheap (multiplication/
  mixing), exact where meaningful (accumulation, verdicts)*. E1's LCG is already
  a deterministic bit source; DS-CIM's shared-PRNG mutual-exclusion trick is the
  multi-cell version — one LCG serving a neighborhood on interleaved phases.
- Deterministic bit mapping (FALCON) kills the "we need real noise" objection at
  the hardware level: quilt's seeded LCG streams are a first-class implementation
  of stochastic computing, not a simulation of it.
- Runtime precision dial (stream length ↔ accuracy) = paper-225's
  measure-longer-settle-tighter, formalized.

**Tonight-experiment**

- SC-tick multiply (CPU, 45min): replace one multiply inside the lane-1 integer
  reservoir (or lane-2 coupling) with LCG bit-stream multiply (u ∈ ℤ_256 as
  Bernoulli p=u/256, 32/64/128-bit streams, AND + popcount). Sweep stream length,
  plot NRMSE/TTS vs length and vs exact int multiply. Establishes the quilt
  noise/precision curve on real fabric code.

---

## Lane 8 — Hyperdimensional Computing / VSA (Integer Ops)

**Seam.** 10k-dim bipolar (±1) hypervectors; bind=XOR, bundle=popcount-majority —
integer/bit ops end to end. This lane is quilt's most literal ancestor: all
arithmetic is already integer.

**Strongest recent artifacts**

- **TorchHD** ★384 — the standard library; hash tables, associative memory,
  GPU-tensor execution. https://github.com/hyperdimensional-computing/torchhd
- Real-valued sequence encodings with **Hadamard binding + exact shift-equivariant
  algebraic shift operator** (shift a sequence's encoding without re-encoding —
  cheap temporal manipulation). arXiv:2608.28334. https://arxiv.org/abs/2608.28334
- **NysHD** — HDC ⟷ kernel methods bridge via Nyström: turn any PSD similarity
  into an HDC encoding (+11%/17% on graphs/strings). arXiv:2608.06860.
  Gram-Space codebook compression (15.75× memory, 3.62× latency, inner products
  preserved exactly). arXiv:2608.01528.
- **Over-the-air VSA bundling**: devices superpose transmissions and the physics
  *is* the bundle op — interference as the binding primitive in comms.
  arXiv:2607.22155. https://arxiv.org/abs/2607.22155
- Honest failure study: HRR + Hopfield cleanup **fails zero-shot composition**
  — not the algebra, but superposition capacity limits (interference already at
  hop-1). arXiv:2606.24948. Multiclass integer perceptrons with multiplicative
  margins (explicitly pitched for HDC readout, resource-constrained deployment).
  arXiv:2608.30028.

**Quilt-transfers**

- E1's pulse-queue state vector IS a drifting hypervector of signed integers; the
  cancellation counter is a popcount statistic. The batten metaphor (superpose
  then measure) is VSA bundling in one dimension. OTA-bundling says superposition
  channels can *carry* the bundle — quilt's cell-to-cell pulse exchange is a bus
  doing bundle ops physically.
- The shift-operator result: quilt can represent "5-tick latency" as an exact
  algebraic shift on encodings rather than a delay queue — candidate E1 variant
  (replace T2's delay line with shift encoding of its stream).
- Failure study is the needed caveat: bundling capacity is finite and
  interference grows with load — quilt's ledger should track a superposition-load
  statistic (live pulses per cell / capacity) the way HDC tracks codebook
  crosstalk.

**Tonight-experiment**

- Bipolar fabric memory (CPU, 1h): encode 40 E1 "regime snippets" (windows of
  per-tick features → ±1 hypervectors via random projections over integer
  features), bundle per-regime prototypes, classify fresh snippets by Hamming
  similarity with integer popcount. Compare vs the lane-6 ELM on the same task.
  Success = ≥ ELM accuracy with pure XOR/popcount ops (ESP32-portable proof).

---

## Lane 9 — Neuromorphic Dynamics: Short-Term Plasticity as Compute

**Seam.** Volatile device dynamics as *temporal filters*: STP turns a synapse
into a frequency-selective channel — plasticity is the computation, not a
training mechanism.

**Strongest recent artifacts**

- **ECRAM non-equilibrium dynamics as a resource**: volatile conductance
  modulation + delay-feedback LIF → facilitation and excitability modulation at
  2 pJ/spike; "artifact → resource" cross-layer co-design. arXiv:2605.11243.
  https://arxiv.org/abs/2605.11243
- **Plasticity timescales information theory**: LTP steers toward optimal-encoding
  regimes; STP enables **temporal-order discrimination by navigating a multistable
  attractor landscape**; optimal variability exists per discrimination task.
  arXiv:2509.13867. https://arxiv.org/abs/2509.13867
- Astrocyte-STP → linear-complexity attention in transformers (RMAAT, LRA
  benchmark). arXiv:2601.00426. Organic-transistor STP with Coulomb-blockade
  discrete levels (multimodal electrical+optical programming). arXiv:2608.20245.

**Quilt-transfers**

- E1's decaying pulse queue is short-term synaptic depression/facilitation in
  integer form: pulse magnitude ≈ vesicle availability, decay ≈ recovery. The
  theory result quilt can import: **multistability + STP = sequence
  discrimination** — i.e., the interference tick shouldn't just settle g; its
  transient structure classifies input history. That's a new, testable claim for
  paper 225 (E7 candidate: do cancellation patterns discriminate twin-conflict
  waveforms?).
- The "optimal variability" result backs quilt's Variety Ledger doctrine:
  variability is a resource with a task-dependent optimum, not noise to minimize.

**Tonight-experiment**

- STP-filter sweep (CPU, 30min): feed the two E1 arms (impulse vs interference)
  the same three input regimes (calm walk / conflicted twins / bursty spikes) and
  record per-tick cancellation & constructive counts; train a 3-way classifier on
  the count *histograms* alone (even a decision stump). If histograms separate
  regimes, E1's transients are discriminative — the STP claim, verified in
  integers on existing harness output.

---

## Lane 10 — Repos & Tooling Worth Tracking (cross-cutting)

| Repo | What | Why quilt cares |
|------|------|-----------------|
| extropic-ai/thrml ★1145 | JAX block-Gibbs on heterogeneous graphs | Block schedules = tick schedules; hardware trajectory |
| extropic-ai/torx ★64 | JAX parameterized stochastic circuits / factor graphs | The compile-to-noise-tooling pattern |
| normal-computing/thermox ★69 | Exact OU processes; thermo linear algebra | Ground truth for stochastic-tick variants |
| normal-computing/posteriors ★386 | UQ with PyTorch | Calibrated settle/precision claims |
| dcharlot-physicalai-bmi/ferrotherm | Rust, zero-dep thermodynamic computing; **joules ledger**; verified vs exact physics; reaches real Ising silicon via one trait | Architecture template: energy-ledgered solver trait-abstracted over substrates — read the README even if not used |
| reservoirpy ★651 / EchoTorch ★500 | ESN tooling | Lane-1 baselines |
| TorchHD ★384 | VSA library | Lane-8 baselines |
| g-lanza/scgrad | Differentiable stochastic computing for PyTorch | Train-then-integerize pipeline |
| SashimiSaketoro/thrml-rs | Rust port of Extropic THRML primitives | Embedded/no-Python target precedent |

Also: fixstars/amplify-benchmark (Ising benchmark harness, MIT) —
https://github.com/fixstars/amplify-benchmark

---

## Dead Ends (honest ledger)

1. **Thermodynamic noise theater.** For convex settle problems the stochastic
   physics collapses to deterministic preconditioned GD (2608.09743, 100,000×
   faster deterministic). Quilt must NOT sell the LCG as necessary physics for
   problems with one basin — only sampling/annealing workloads justify it. The
   honest pitch: deterministic tick by default, stochastic tick as a *mode*.
2. **Bundling capacity is real and binding.** HRR/Hopfield fails zero-shot
   composition; superposition interference appears already at one hop (2606.24948).
   E1's gentle-params finding (interference *worse* in calm regimes) is the same
   law: interference is a conflict-resolution regime, not a free lunch — regime
   gating (E4) is mandatory, not polish.
3. **Synchronous updates oscillate without inertia.** Naive parallel p-bits are
   unstable (2604.17109, 2604.01564). Any quilt fabric-wide parallel tick must
   carry the inertia/pulse-queue term or it will chatter — E1's v1 ping-pong bug
   at the architecture scale.
4. **Analog matmul precision floor.** Below ~3 bits (ADC/cell states) AIMC
   accuracy collapses; the optimum states-per-cell is small but *finite*
   (2604.26979, 2507.09776). Quilt's u8 world is comfortably above the floor,
   but "fewer states is always better" is false — there's a knee to find, not a
   race to the bottom.
5. **Photonic/quantum/magnetic substrates don't port to ESP32.** The devices are
   the point there (YIG films, MTJs, PtNP organics); only their *control theory*
   transfers. Don't burn time on substrate emulation; extract the dynamics.
6. **ELM/random-features are not SOTA learners.** They win on cost/latency, not
   accuracy; claims should stay in the hundred-boats regime (many cheap cells)
   where they're true.
7. **Stochastic computing throughput ceiling.** Long streams for precision =
   latency; SC only wins where its fault tolerance or AND-gate area matters
   (DS-CIM's fix required 64× replication to reach competitive throughput).

---

## Top 3, ranked by (impact × doable-tonight)

**#1 — Inertia-regularized synchronous p-bit solver (lane 2).**
Impact: converts the E1 interference tick from a control heuristic into a
published, FPGA-verified solver dynamics class ("inertia term licenses parallel
updates"); it's the same mathematics E1 already runs, so it also upgrades quilt's
story to "we run a known-good physics substrate in integers."
Tonight: `inertia-pbit.py` Max-Cut bake-off, three arms, int32, CPU or 4050 —
3h including G-set loading. Decisive result either way: if inertia-parallel ≥
sequential, the fabric-wide parallel tick is licensed; if not, E1's queue geometry
differs from published inertia and the diff itself is a finding (DIVERGENCE.md
class).

**#2 — THRML block-Gibbs with latency-shaped blocks on the 4050 (lane 3).**
Impact: seats quilt on Extropic's hardware trajectory (their silicon targets
exactly this sampling class) and tests the claim that *twin-delay structure can
be the parallel schedule* — the block decomposition quilt would actually ship.
Tonight: `pip install thrml`, replicate README chain, swap in delay-class blocks,
measure sample quality vs exhaustive on N≤20 + wall-clock per 1k samples — 2h.

**#3 — Feature-tick readout: E1's counters as reservoir features (lanes 6+9).**
Impact: tests the strongest paper-225 claim available tonight — "the tick's own
transients are the model" (STP-as-compute + ELM readout, zero trained dynamics
inside the fabric). Success repositions the interference tick from
state-estimation to computation.
Tonight: harvest per-tick integer features from `e1.py run()`, integer ridge,
predict `reality(t+8)`; plus the 3-regime histogram classifier (lane 9) — 1.5h,
CPU only, no new deps.

*Tie-breakers: #1 also feeds Verilator rung-3 directly (integer dynamics ports to
the booked cosim spike); #2 is the only one touching real vendor hardware; #3 has
the highest doctrine leverage per minute of work.*

---

*Scout: Lucineer subagent lane 2 (zai/glm-5.3), 2026-09-02/03, Alaska. Sources:
arXiv API, GitHub API, raw.githubusercontent. No commit made, per instructions.*
