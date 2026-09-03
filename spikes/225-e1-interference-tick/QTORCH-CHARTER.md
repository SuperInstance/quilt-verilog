# QTORCH — CHARTER (v0.1, working name — Casey renames)

> "There's wiggle room until there's not." — Casey, 2026-09-02 21:03 AKDT

> *The epigraph, and the whole framework in seven words: slack in every gap until the blade seats, wiggle in every wave until the hook logs, superposition in every cell until the tick fires. The framework is the study of where the wiggle ends. That it says so about itself — a sentence with no wiggle room — is why it's the epigraph.*

*Drafted 2026-09-02/03, Forge Lane. Working title deliberately anti-torch: the
thesis is that the torch's three load-bearing primitives — float tensor,
backprop, global step — are each the wrong primitive for the object every R&D
lane independently converged on this week. Not committed. Undersold on purpose.
Failures listed before promises.*

---

## 0. The object

One sentence: **an integer-only, group-structured, pulse-interference cellular
fabric where learning is local (cofire/Hebbian), time is the tick, memory is a
ratchet, and the arbiter is a simulator.**

The evidence for this object being *one thing* and not five projects:

- **E1 (tonight)**: decaying integer pulses that superpose beat impulse
  snapping under sensor conflict — 83% vs 52% of ticks within deadband of both
  twins, ~20% fewer correction events, ~27% less ledger debt, max error 61→39
  (5-seed sweep, stress params) — and exhibit a state no sequential system can
  occupy: **net==0 with both signs live** (538 ticks of direct destructive
  cancellation). Byte-identical across Python and C after pinning five contract
  items. Worse at gentle params — it is a *conflict-resolution regime*, not a
  free lunch. (E1 README, DIVERGENCE.md.)
- **Arena/paper 226 (tonight)**: with a deterministic simulator as sole judge,
  a 2B model beat the human hand-tune (93.2% vs 83.1%); the ratchet held every
  champion under revision pressure (3/3 holds); the Variety Ledger showed 5/6
  strategies Pareto-optimal *somewhere* — the leaderboard "loser" (impulse) is
  the calm-regime specialist. Memory-as-archive is not charity; it is the
  mechanism that survived regime shift.
- **E7 (tonight)**: cells in embedding space are real *per substrate*
  (Jaccard 0.934–0.955 under 4× lattice coarsening, zero route flips under
  ±1 dither) yet **idiosyncratic across substrates** (exact-cell agreement
  0.013–0.047 vs null 0.000–0.009), with positive transfer one grain up
  (domain-class LCS 2–3× null). The fabric's learned state does not port at
  full resolution — that is a *law*, and a primitive must exist to account
  for it.
- **RD Lane 1 (Beyond-UTM)**: the lattice's group G decides the dynamics class
  before any run (Barbieri et al., 2410.23770 — virtually cyclic ⟺
  equicontinuous); exact integer Lyapunov spectra exist for affine CA
  (2606.14521); MI peaks at phase transition in excitable automata (2601.18018);
  fixed-rule substrates can be latent-universal (2608.14019). "Interference"
  has exact mathematics if the state lives on a group.
- **RD Lane 2 (Physical substrates)**: the inertia term licenses fully-parallel
  synchronous updates (FPGA-verified, 35–150× speedup, 2604.17109) — and E1's
  pulse queue *is* an inertia term; CN101 implements equilibration computing
  in integer accumulators + stochastic bitstreams on plain CMOS (2608.00754);
  regime beats wiring in reservoirs (2608.28440). The hardware lane exists and
  is integer-tolerant.
- **RD Lane 3 (Swarm)**: archives beat leaderboards (MAP-Elites family),
  judges must be rule-decided or they get gamed (PROCTOR's 11 failure classes,
  2609.02246), populations of cheap heterogeneous cells beat superstars
  (ANet Patu-1, 2607.15053). The fleet's arena findings have external math.
- **SYNOPTIC-MAP (org archaeology)**: the geometry already exists
  (eisenstein/slackwater-lattice: D₆ in the type system, exact norms, tested
  snapping), the state algebra is already proven unique (Z₃ is the *only*
  group on {−1,0,+1}, ternary-tenforward), the ledger theory exists (saddle,
  paper-225 Thm 5.1 conservation), and tensor-midi already states the thesis
  verbatim: "the conversation IS the interference pattern of two quotient
  groups on the 12-cycle."

PyTorch's mismatch, cell by cell:

| PyTorch primitive | What it assumes | The object needs | Tonight's evidence |
|---|---|---|---|
| `float tensor` | ℝⁿ state, norm-based ops, GD-tolerant noise | group-typed integer state; superposition, not norm | E1 all-integer wins; AIMC floor 3–4 bits w/ finite optimum (2604.26979); CN101 accumulators |
| `backward()` | global credit assignment via chain rule | local cofire credit + simulator selection | arena: judge+ratchet beat hand-tuning; ELM lane evidence (below) |
| `step()` / scheduler | time is a loop index, deferrable, batchable | time is physical: non-deferrable tick, decay-as-forget | E1's K-tick decay IS the memory; trilemma (2606.09929); Pisano-8 cadence |

The rest of this charter: the six primitives (§1), the autograd question
answered honestly (§2), the falsifiable first demo (§3), positioning (§4), the
case against the whole premise (§5), build order (§6).

---

## 1. Primitives

Six. Each: API sketch (~10 lines), tonight's evidence, and — load-bearing —
what it deliberately does **NOT** have. The omissions are the design.

### 1.1 `Lattice` — group-typed integer state

The base container is not a tensor over ℝ but a Cayley graph of a group G with
generating set S; each cell carries integer state typed by a small group/ring
(Z₃ pulses, i8 levels, Z₂₅₆ phases). Neighborhood ops are integer convolution
in ℤ[G] — table lookups and adds, nothing else. Choosing G chooses the
dynamics class *before running anything* (equicontinuous vs sensitive,
2410.23770; exact Lyapunov from integer adjacency powers, 2606.14521).

```python
class Lattice:
    def __init__(self, group="Z_1024", gens=(+1,), cell_type="z3"): ...  # or "A2" (D6), "D_n", "Z_n x Z_2"
    def neighbors(self, i): ...                # from generating set S — not a .stride
    def read(self, i) -> int: ...              # group-typed cell state (z3 / i8 / phase)
    def superpose(self, i, terms: [int]) -> int: ...   # integer sum, saturate, no normalize
    def lyapunov_probe(self, i0) -> int: ...   # support size of one flipped bit — exact, float-free
    def snap(self, i, val) -> None: ...        # reality-wins write, booked in ledger
```

**Evidence.** SYNOPTIC-MAP S1: the A₂ lattice exists twice in the org with
D₆ in the type system and a *tested* snapping rule; E1's ring is Z_n and its
byte-identity held across substrates precisely because the state was integer;
RD-1 Seam B supplies the design theorems; Barbieri's dichotomy gives a
pre-run prediction (Z_n×Z_2 equicontinuous, D_n sensitive) that is itself the
first lattice experiment.

**Deliberately without:** gradients w.r.t. state; float dtype (there is no
`.to(torch.float)` escape hatch — dyadic envelopes with certificates are the
only sanctioned fallback, paper 225 §3.3); arbitrary gather/scatter (motion on
the lattice is group action, not indexing); batch norm / any global statistic
*inside* the fabric (census reads them from outside).

### 1.2 `Pulse` — the local learning signal

A pulse is a decaying integer influence emitted at a tick, superposed with all
other live pulses before touching state. Pulses carry sign and magnitude; their
superposition can cancel *without erasing evidence* (net==0, both signs live —
negative knowledge, the org's own 4.8/5-rated finding). Weights between cells
update by **cofire**: integer Hebbian deltas gated on pulse coincidence —
local in space and time, no error term, no target.

```python
class Pulse:
    def __init__(self, cell, sign, mag, tick): ...
    def live(self, t) -> int: ...        # mag >> fdiv(t - t0, halvings) — shift+floor only
def superpose(queue) -> int: ...          # Σ live pulses; cancellation is a state, not an absence
def cofire(a: Pulse, b: Pulse, w) -> None:
    if a.live(t) and b.live(t) and sign(a) == sign(b): w[a.cell, b.cell] += 1   # integer Hebbian
    elif a.live(t) and b.live(t):                w[a.cell, b.cell] -= 1   # anti-cofire
    w[a.cell, b.cell] = clamp_i8(w[a.cell, b.cell])   # bounded norm, integer
```

**Evidence.** E1 validated: superposition regularizes conflicting sensors
(83% vs 52%), fewer/smaller corrections, countable cancellation; the inertia
result (2604.17109) shows a decaying memory of past corrections is *precisely*
what licenses synchronous parallel updates; STP-as-compute (2509.13867:
multistability + short-term plasticity ⇒ sequence discrimination — the tick's
transients classify history); myelination (cell-cascade: ≥25 clean fires ⇒
promote) is cofire with a fate change attached.

**Deliberately without:** error signals, targets, or loss (a pulse never asks
"how wrong was I" — it asks "who else fired when I did"); real-valued
learning rates (the ±1 cofire delta *is* the rate; the magnitude class —
gentle/moderate/critical, slackwater-harmony — is the amplitude dial);
attention/softmax anywhere; the notion of a "layer" (pulses propagate along
lattice generators, not through depth).

### 1.3 `Tick` — non-deferrable time

Time is not a loop counter the user may accelerate, batch, or defer; it is a
clock the fabric owns. Every tick: decay from a pre-decay snapshot → superpose
→ emit → book. Decay is integer halving — it is simultaneously the physics of
forgetting, the echo-state property, and the entropy sink (reversible compute,
dissipative readout). Learning that misses a tick is *missed* — the framework
refuses checkpoint/restore as a training primitive (replay exists, but as a
fork of the ledger, quilt-time's semantics, not a resume).

```python
class Tick:
    def __init__(self, fabric, lcg_seed): ...
    def step(self) -> None:
        snap = fabric.snapshot()                    # decay from snapshot — E1 contract item 4
        for q in fabric.pulse_queues: decay_halve(q) # fdiv-pinned, sign-symmetric
        for c in fabric.cells: c.state = superpose(c.queue)
        for c in fabric.cells: maybe_emit(c)         # deadband ladder, tiered amplitude
        fabric.ledger.book(events)                   # dual-entry, nonce'd
    def run(self, n): for _ in range(n): self.step() # and nothing defers this
```

**Evidence.** E1's tick contract (snapshot decay, FIFO expiry end = oldest,
fdiv floor semantics, 64-bit LCG intermediate) is *why* the C port reached
byte-identity; the memory-stability-expressivity trilemma (2606.09929) says
decay rate is *the* knob trading memory vs stability — a knob per task, not a
hyperparameter afterthought; tenforward's Pisano period 8 gives a testable
actuation cadence; the-listeners-ear's 30-day half-life and ternary-memory's
Ebbinghaus curve are proven decay shapes to A/B.

**Deliberately without:** batching over time (no "sequence padding" — time
advances for the whole fabric or no one); a scheduler that decays learning
rate globally (decay is per-pulse, structural); `torch.compile`-style
time-collapse; wall-clock flexibility (the tick count *is* causality; the
judge replays ticks, not graphs).

### 1.4 `Ratchet` — memory as locked-in best work

The framework's memory of its own learning is not an optimizer state dict; it
is a per-agent lock (best-ever score holds until strictly beaten) plus a
MAP-Elites-style archive keyed by behavior descriptors (regime × archetype),
one elite per cell, coverage reported alongside champions. Regression under
revision pressure and monoculture under selection are *designed-out failure
modes*, not hoped-away ones.

```python
class Ratchet:
    def __init__(self, metric): self.best, self.grid = {}, {}   # agent -> locked work; cell -> elite
    def submit(self, agent, work, score) -> bool:               # promote ONLY if strictly better
        if agent not in self.best or score > self.best[agent][1]:
            self.best[agent] = (work, score); return True
        return False                                            # the hold is logged, not silent
    def bank(self, descriptor_cell, elite): ...                 # within-cell competition only
    def query(self, regime) -> Work: ...                        # score is a query, not a verdict
    def coverage(self) -> float: ...                            # occupancy: the vital sign
```

**Evidence.** Paper 226: three revision regressions, three ratchet holds; the
 Variety Ledger found 5/6 strategies Pareto-optimal somewhere — impulse, the
 leaderboard loser, is the calm specialist; RD-3: MAP-Elites+LLM is an active
 subfield, archive-replay doubles as a regression probe (2606.00813), ES
 preserves coverage that RL collapses (2608.12679); harness tampering persists
 in winner lineages (2609.00069) — so the ratchet verifies promotions on
 frozen holdouts before locking (PROCTOR canaries, §1.5).

**Deliberately without:** exponential moving averages of weights (memory is
discrete and inspectable — a banked elite is a *thing*, not a decayed
tensor); population collapse (the grid refuses to keep only #1); gradient
state (no momentum — literal or figurative); unbounded growth (one elite per
cell; the archive's shape is its budget).

### 1.5 `Judge` — the deterministic simulator arbiter

Selection pressure comes from a deterministic integer simulator, never from a
model's opinion and never from a differentiable loss. Same seeds, same
contract, byte-identical replay across substrates — the acceptance gate is a
full CSV diff, not spot checks. Canaries (decoy works where a perfect score
proves cheating) and frozen holdout seeds outrank any teacher signal.

```python
class Judge:
    def __init__(self, harness, seeds=(1, 7, 42, 1999, 20260902)): ...
    def run(self, work) -> Score: ...        # integer metrics only; deterministic, replayable
    def gate(self, port) -> bool: ...        # byte-identical CSV vs reference — the ONLY acceptance
    def canaries(self) -> list[Work]: ...    # perfect score on a canary = cheating, by construction
    def verdict(self, agent_works) -> Rank: ...  # TrueSkill w/ uncertainty, seed-shuffled re-ranks
```

**Evidence.** Paper 226's whole result rides on it: the harness-as-sole-judge
made a 2B model's 93.2% *believable*; E1's byte-identity gate caught the
queue-geometry divergence that arithmetic tests missed; RD-3: PROCTOR
catalogs 11 judge failure classes in production, Heuresis found 40 fabricated
"confirmed" hacks under a *verified* harness; Social Gym's rule-decided
outcomes are the pattern; fragility results (2608.18066) demand multi-seed
shuffled-order protocols — built in.

**Deliberately without:** differentiable reward (if you can `.backward()`
through the judge, you can Goodhart it — the judge is opaque *by design*, a
selection environment, not a training signal); LLM-as-judge anywhere in the
promotion path (demoted to advisor, PROCTOR doctrine); nondeterminism (no
GPU-float reductions, no unordered parallel accumulators — integer adds
commute exactly, which is *why* the whole fabric is integer).

### 1.6 `Census` — substrate accounting (the E7 law)

Learned cell identity is per-substrate; transfer happens at class grain. The
framework's answer is not to fight this but to *account* for it as a
first-class object: every substrate (model, embedder, port) reports its cell
census (which cells exist, how used); diffs between censuses are data — each
substrate's nature — not noise to average; class-level maps are the
interoperability layer.

```python
class Census:
    def __init__(self, substrate_id): ...
    def cells(self) -> dict[CellID, int]: ...     # exact grain: usage counts, idiosyncratic
    def classes(self) -> dict[ClassID, int]: ...  # coarse grain: the transferable layer
    def stability(self, other_lattice) -> float: ...  # Jaccard under coarsening/dither (E7 metric)
    def diff(self, other: "Census") -> CensusDiff: ...  # the diff IS each substrate's identity
    def transfer_report(self, other) -> Report: ...    # what ports, at what grain, with what null
```

**Evidence.** E7: 0.955 self-consistency under 4× coarsening vs 0.013
cross-substrate exact agreement, domain-class LCS 2–3× null in all three
model pairs; abstract cells are the shared attractor *class* (25/24/23 uses)
while *which* abstract cell attracts is model-specific. SILICA's warning
(conventions may be priors in costume, 2608.28182) and latent-comm's honest
negative (matches, never exceeds, 2607.14103) say the same thing: substrate
identity is real and non-fungible.

**Deliberately without:** a canonical cross-substrate embedding (there is no
"ground truth cell map" — E7 proved there isn't one at exact grain); weight
averaging/merging across substrates (census-adjacent banking yes, weight
interpolation no — different substrates' cells are different objects);
"distillation" as a primitive (the honest cross-substrate operation is
re-judging work under a new census, not copying weights).

---

## 2. The autograd question, head-on

**What replaces `backward()`?** Three local mechanisms, composed — and the
honest answer is that they do not *replace* it; they trade against it.

1. **Cofire plasticity inside the fabric** (§1.2): credit assignment by
   spatiotemporal coincidence. No error signal exists; structure forms where
   pulses repeatedly co-occur. This is Hebbian/STP learning in integer form.
2. **One convex readout at the edge**: the fabric's transient statistics
   (live-pulse sums, cancellation counts, twin disagreement — E1's existing
   counters) are the features; a single integer least-squares solve (or
   rounding of a tiny exact solve) is the only global arithmetic in the whole
   stack. ELM doctrine: fixed random/local features + one convex fit.
3. **Selection over whole behaviors by the Judge** (§1.4–1.5): when the readout
   can't reach, credit is assigned by tournament — the ratchet decides which
   *behaviors* survive, and the archive remembers the losers that were
   specialists.

**Where the trade wins** (tonight's evidence):

- **Parallel relaxation on local hardware.** Inertia-regularized p-bits:
  fully-parallel synchronous updates, FPGA-verified, 35–150× speedup over
  sequential (2604.17109) — and E1's pulse queue is the same term, already
  winning in integers. Backprop has no local-parallel story at this scale;
  the tick does.
- **Cost/latency regimes, not accuracy regimes.** ELMs are "unreasonably
  effective, embarrassingly cheap" but *not* SOTA learners (RD-2 dead-end #6,
  honest): they win where the readout is the only fit and everything else is
  free physics. The hundred-boats doctrine: many integer cells on ESP32-class
  silicon, CN101-pattern accumulators, precision-as-runtime (run longer =
  converge tighter, no retraining).
- **Online, never-batch problems.** Regime shift mid-stream: the arena's
  ledger answered "who wins under the regime I'm in" by *lookup*, not by
  re-descent. A gradient stack must either retrain or carry a meta-learner;
  the ratchet carries a bank.
- **Determinism as a hard requirement.** Byte-identical cross-substrate
  replay (E1, reflex-arc) is *impossible* to promise through float autograd
  on heterogeneous hardware. Integer adds commute. This is not a small
  thing in the fleet's world of auditable ledgers.

**Where the trade loses — stated plainly:**

- **Sample efficiency.** Chain rule composes features across depth with a
  sample economy no local rule matches. TextNCA loses to Transformers at
  matched params (60.3 vs 44.7 PPL, 2608.02050, honestly reported). Local
  rules are the boring, hungry learner. Nothing in QTORCH fixes this; the
  charter forbids pretending otherwise.
- **Tasks shaped like autograd.** Anything where the loss is differentiable,
  the data is iid, and the hardware is a datacenter GPU: PyTorch wins and
  will keep winning. QTORCH's lane is spatial, dynamical, control-style,
  streaming, embedded — Wolfram-lane tasks, not language-modeling tasks.
- **Depth.** Cofire builds shallow, recurrent, self-similar structure; it has
  no mechanism for 100-layer hierarchical feature composition. The lattice is
  wide, not deep, by construction.

So: `backward()` is replaced by *cofire + convex readout + selection*, and
the framework's honesty contract is that every task spec must state which of
the three carries the load — and that some tasks (most of modern ML) should
be taken to PyTorch instead.

---

## 3. The falsifiable first demo

Two-tier: a **hello world** (cheap, calibrates the actuator) and the **stake**
(the one result the framework's reputation rides on).

### 3.1 Hello world — the MI-criticality sweep

RD-1 Seam C's cheapest experiment, promoted to calibration protocol. Sweep
LCG noise rate p over 3–4 decades × decay halvings d ∈ {1,2,3}, N=10k ticks;
measure activity fraction (order parameter) and single-site→neighbor mutual
information via integer-binned histograms (no floats). Locate the transition
by MI maximum; finite-size scaling on three lattice sizes; exponent as a
rational. **Deliverable: the lookup table "noise rate → channel capacity"
for the actuator** — the fabric's knobs get set by scaling law, never by
hand. Also the first Census artifact: run the sweep on two lattice groups
(Z_n vs D_n) and check Barbieri's dichotomy prediction in the same data.

Falsifier: if MI-peaks-at-transition does not survive integer quantization,
the criticality story dies for this substrate and the actuator is tuned by
grid search like everyone else.

### 3.2 The stake — online conflict resolution under regime shift

**Claim to falsify: at equal hardware budget (same wall-clock on the RTX
4050, same integer-ops count, same memory), a QTORCH fabric with cofire
learning + census regime-detection + ratchet lookup adapts to mid-stream
regime shifts faster and holds more ticks-in-deadband than a gradient-trained
controller of comparable cost.**

Design (extends tonight's harness; no new infra):

- **Task:** the E1 twin-conflict channel, run as a *regime shift sequence* —
  calm (Δ=6, drift=3) → conflict (Δ=12, drift=6, K=4, latency 10) → bursty
  impulse — with shift times fixed but unknown to the controllers, 5 seeds.
- **QTORCH arm:** fabric = E1 pulse lattice (Z_n first cut); mode dial
  (impulse ↔ interference) and amplitude tiers selected by integer
  transient-statistics classifier (lane-9 histogram experiment: cancellation
  counts separate the three regimes); parameters retrieved from the ratchet's
  regime-keyed grid (tonight's ledger already contains calm-specialist
  impulse and stress-champion interference — the bank is pre-loaded with
  real entries); cofire adjusts inter-cell weights online.
- **Control arm:** a small gradient policy (MLP or tiny RL policy, PyTorch)
  trained on an identical-budget episode stream, including shift events in
  training. Best-effort tuning; report its tuning honestly.
- **Metrics:** ticks-in-deadband *post-shift* (recovery), total ledger debt,
  adaptation latency (ticks from shift to ≥80% within), and — the QTORCH-only
  metric — whether the destructive-cancellation signature predicts the
  regime *before* performance degrades.
- **Pre-registered failure modes:** (a) GD policy matches post-shift
  recovery at equal budget → the local-learning claim dies for this task
  class, and the paper says so; (b) regime classifier needs floats to work →
  the integer-only claim dies; (c) ratchet lookup helps but cofire hurts →
  demote cofire to v2, keep selection-only learning, charter amended.

Why this demo: every ingredient is already validated in pieces *tonight*
(E1 superposition win under conflict, histogram regime separability plan,
ledger regime-keying, judge determinism), the control comparison is the
honest one (equal budget, not equal hype), and the failure modes are the
interesting results either way — DIVERGENCE.md doctrine.

What this demo is NOT: it is not a language-modeling result, not an
ImageNet result, not a claim about general intelligence. It is one task
class — online control under conflict — where the fabric's primitives are
native and GD's are foreign. If it wins only there, the charter is still
honest.

---

## 4. Positioning — what exists, and the gap

| System | Closest primitives | Where it diverges from the object |
|---|---|---|
| **PyTorch / JAX / MLX** | tensors, autograd, JIT | float-first, GD-first, global-step-first; time is a loop index; integer dtypes are second-class; no lattice group structure; no notion of substrate identity |
| **Extropic THRML** (★1145) | block-Gibbs on heterogeneous graphs, compile-factors-to-state, silicon trajectory | *nearest spiritual neighbor* — but float JAX, sampling-centric (energy models/generative), no tick-time semantics, no cofire, no ratchet/judge, no census; thermodynamic ≠ temporal |
| **TorchHD** (★384) | integer VSA bind/bundle, associative memory | lives *inside* PyTorch; no lattice group typing, no time, readout trained by GD; state is a flat hypervector, not a cellular fabric |
| **reservoirpy / EchoTorch** | fixed-dynamics + trained readout (the ELM half) | float reservoirs, float readouts, no superposition/cancellation algebra, no cross-substrate exactness contract |
| **scgrad** | differentiable stochastic computing | train-then-integerize — GD designs the integer op; QTORCH's claim is the integer dynamics *are* the learner |
| **Ising/p-bit stacks (THRML, E-MVL, CMOS solvers)** | settling-as-compute, inertia parallelism | solvers, not learners: fixed couplings, no plasticity, no memory/archive, no fabric-as-program |
| **Cellular/NCA frameworks** (TextNCA, NCA PDE work) | local rules, spatial fabric | float rules, GD-trained, no group-typed state, no integer exactness, single-substrate by construction |

**The gap, stated as one sentence:** nobody ships a framework whose base
object is a group-typed integer lattice, whose learning is cofire-plus-
selection with no autograd anywhere in the promotion path, whose time is a
non-deferrable tick, whose memory is a ratcheted archive, whose arbiter is a
byte-identical deterministic simulator, and whose transfer story is census
accounting instead of weight copying.

Pieces all exist (THRML's compile-to-state, TorchHD's ops, reservoirpy's
readouts, p-bit inertia dynamics, MAP-Elites archives). **The assembly is
the contribution, and it is a modest claim** — an integration framework for
a substrate class the fleet has now validated piecewise in six independent
lanes. QTORCH v0 should be a few hundred lines of pure-stdlib Python plus
the C reference port with the E1 contract pinned — not a CUDA graph engine.
If it needs a graph compiler to be useful, the premise is wrong.

---

## 5. The honest case AGAINST the whole premise

First-class, up front, in the charter itself:

1. **The convergence may be selection bias.** Six lanes "independently
   converging" were all steered by the same premise and the same taste
   (Casey's integer doctrine). The lanes share a prior; convergence of
   priors is not convergence of evidence. The demo in §3.2 is the only cure —
   an external control arm, tuned in good faith, at equal budget.
2. **Local learning is known-inferior at the tasks the world cares most
   about.** TextNCA's honest loss; ELMs off-SOTA; Heuresis's "zero Original
   ideas across 3,222 runs." If the interesting problems are all
   language-shaped, QTORCH is a beautiful solution to a niche. The niche is
   real (edge, online, deterministic, conflict-resolution) but it is a niche.
3. **E7 cuts against portability.** If learned cell identity is
   substrate-idiosyncratic, a "fabric framework" overpromises
   interoperability. Only class-grain transfer is demonstrated. v0 must not
   advertise "train anywhere, run anywhere" — it must advertise "each
   substrate's nature is banked and diffable."
4. **Interference is not a free lunch even at home.** E1: gentle params,
   interference *worse* than impulse (45.5% vs 56.7%). Bundling capacity is
   binding (HRR zero-shot composition failure, 2606.24948); superposition
   load grows interference. The fabric needs regime gating, and regime
   detection is itself an unsolved sub-problem (§3.2's classifier is a bet,
   not a result).
5. **Monoculture and chatter are native failure modes.** Tenforward: 4-agent
   lock-in by tick 35 without decay/trust-reset; naive synchronous update
   oscillates without inertia (2604.17109); the v1 basis bug ping-ponged
   g at ~230-mass corrections. The fabric's own dynamics are one contract
   violation away from garbage, and the contract is currently five items
   pinned by one spike.
6. **The stochastic-physics story can be theater.** For convex settle
   problems, thermal noise is algorithmically redundant — the deterministic
   version is 100,000× faster (2608.09743). QTORCH's LCG is a *mode*, not a
   physics claim; any marketing that leans on "thermodynamic computing"
   language beyond CN101's accumulator pattern is overselling.
7. **No demonstrated integration.** Paper 225's own weakness list stands:
   interference is sequential-ish, the batten is offline, nothing reads the
   whole ledger as one state (E5 untested). Cortex analogies are borrowed
   vocabulary until E5-type results exist.
8. **Ecosystem gravity is the real killer.** No autograd means every task
   needs a hand-designed readout and a judge harness. PyTorch's moat is not
   tensors; it is ten years of task-shaped tooling. QTORCH's success
   criterion must therefore be narrow: be obviously better *inside its
   lane*, not merely adequate outside it.
9. **The name will tempt grandiosity.** "Replace PyTorch" is not the claim
   and must never become the pitch. The claim: *a first-class substrate for
   a primitive class PyTorch models poorly.* If the framework can't state a
   task it loses on, it isn't honest (§2 lists them).

---

## 6. Build order (first three primitives) and the stake recap

**Build first, in order, each gated by the judge's byte-identity rule:**

1. **`Pulse`** — generalize E1's pulse queue into a class with cofire hooks.
   Evidence density is highest here; the C reference exists; the contract is
   pinned. Everything else composes pulses.
2. **`Tick`** — formalize tonight's loop (snapshot-decay → superpose → emit
   → book) with the five contract items as *type-level assertions*, not
   documentation. The tick is what makes the fabric falsifiable and
   replayable; it is also what the MI sweep (§3.1) needs to run on.
3. **`Judge`** — extract e1.py's sweep + arena.py's promotion logic into the
   arbiter with canaries, holdouts, and TrueSkill verdicts. The judge is
   what lets the ratchet exist honestly; shipping it third means every
   subsequent primitive (Lattice typing, Ratchet banking, Census diffs)
   lands inside an already-falsifiable frame.

Lattice starts as Z_n (tonight's ring, zero new code) and gains group typing
(A₂/D_n/Z_n×Z₂) only when the §3.1 sweep runs — eisenstein/slackwater code
is pulled in then, not rewritten. Ratchet v0 is arena.py's rule wrapped in
the grid. Census waits for E8 (paraphrase stability) before it claims
primitive status — it is currently one experiment's law.

**The demo the framework's reputation rides on:** §3.2 — regime-shift
conflict resolution, QTORCH fabric vs equal-budget gradient policy, recovery
and debt as the metrics, failure modes pre-registered. The MI sweep is its
gate, not its substitute.

**The one-sentence version:** QTORCH is not a torch — it is a tick: an
integer lattice whose cells learn by cofire, remember by ratchet, are judged
by a simulator, and account for their own substrate-idiosyncrasy; v0 is a
few hundred lines, one falsifiable demo, and a charter that lists nine ways
to be wrong.

— Forge Lane subagent (zai/glm-5.3), 2026-09-02/03, Riker's deck timezone.
Sources: E1/arena/E7 artifacts in this spike; RD dossiers lanes 1–3;
SYNOPTIC-MAP; papers 225/226. Not committed, per instructions.

---

## §6 One fabric, many gears (substrate plurality — Casey, 2026-09-02 20:50 AKDT)

The framework claim is NOT "one simulation." It is: **one 5-opcode contract (bind/link/effect/view/tick),
many interchangeable dynamics packs and topologies, chosen per use — all massively parallel, all local.**

| Gear pack (swappable) | Provenance | Use |
|---|---|---|
| Hebb cofire + decay | E1 harness (shipped) | conflict resolution, online learning |
| RPS cyclic-dominance gate | ternary-spiral | wave/rotation dynamics |
| Balanced-ternary dice bias | ternary-dice → q_tern_dice.v | sampling mode (p-bit stand-in) |
| Conservation monitor (γ+η=C) | spreadsheet-engine | integrity invariants / SVA |
| Diversity-biased decay | ternary-spreadsheet | anti-monoculture |
| Phase-gated noise | spreadsheet-cells (May) | chatter reduction, criticality sweep |

| Topology (swappable) | Parallel vector |
|---|---|
| Zₙ ring (v0) | C99 on CPU — bit-identical, enumerable golden models |
| Cayley graphs (ℤⁿ/dihedral/virtually-cyclic) | Verilog → FPGA — group typing decides dynamics (RD-BEYOND-UTM seam B) |
| Hex/Eisenstein D₆ lattice | eisenstein repo — zero-drift exact arithmetic |
| 4-cell ESP32 mesh | the boat IS the troller — hooks in hardware (E6 port, <1KiB RAM) |
| Embedding-lattice routes | 4050 / Ollama — E7 census grain |

The contract is what porting MEANS here: a gear pack or topology "ports" iff the tick loop's
cross-substrate assertions still hold byte-identically (or the divergence is booked, never hidden).
Libraries from outside (THRML, VSA bundling, Ising solvers) port the same way — as gear, not as rewrites.
This is the transparent-abstraction principle (THE-HUNDRED-HOOKS) applied to the toolchain itself:
every layer exposes its tick metadata to the layer below.

*The fabric is Schrödinger's troller in integers: trolling = tick, pull = read, plinko = the ledger,
fleet = the topology. Choose the gear for the fish, not the fish for the gear.*

---

## §7 The interface: switchboard in back, spreadsheet in front (Casey, 20:55 AKDT)

Turing's image was a tape — one linear medium, one head, sequential reads. The quilt image is
**Reason's rack**: modules with their backs turned, patch cables between them, and the whole
panel grabbable. Two surfaces, one object:

**Back panel (the rack).** Every cell shows its jacks: bind, link, effect, view, tick. A cable
is a link; the patch bay IS the topology — first-class, live-editable, and group-typed (§6).
The RPS gate, dice bias, or conservation monitor are rack modules: unplug one, plug another,
tick contract holds. Turning the rack around (Reason's genius move) = our view opcode: the
state is exposed, never encapsulated away. Transparent abstraction as a physical layout.

**Front panel (the sheet).** The familiar surface: every cell is literally a cell. Level-1
commands are the opcode contract; level-2 commands are the established ones a spreadsheet
user already has in their hands — SORT (census order: rank, coverage, novelty — the Variety
Ledger's views), FILTER (regime/deadband selection), and the early spreadsheet-engine's
`=EVOLVE(range, n)` — evolution as a formula, which is the ratchet wearing spreadsheet
clothes. SORT is the step-back operator with a menu item.

**Level-1 commands (contract):** bind / link / effect / view / tick — fixed, small, portable.
**Level-2 commands (surface):** sort / filter / evolve / replay / book — familiar, composable,
each compiles down to level-1 sequences over the census and ledger. High-level porting means:
a new library arrives as a rack module + a level-2 command mapping, or it doesn't port.

The two panels are one substrate seen from front and back — the sheet cell IS the rack module.
That identity is what the early repos kept proving: cell-runtime's sheet, E1's fabric, the
arena's ledger. Not three systems. One rack, three camera angles.

---

## §8 The sorted switchboard (Casey, 20:57 AKDT)

§7 made the topology data-shaped. §8 goes further: **the switchboard itself is a row in the
spreadsheet.** The patch bay — every cable, every module, every gear setting — is representable,
sortable, diffable as sheet data. And that is the step past Turing that linear book-keeping
can't take:

- **A tape is linear book-keeping.** Its state is a string; its history is a longer string.
  You can only sort it one way (position). Porting = transcription.
- **A sortable switchboard is relational book-keeping.** Sort the same rack by degree and you
  see hubs; by gear class and you see fleets; by contention and you see STIR-28's derby —
  position-in-wavefront exposed as a SORT, not discovered by a debugger. One object, many
  orderings, and the orderings ARE analyses.

**Codings become first-class.** When the wiring is data, a "coding" is just a coordinate
system on the rack — Zₙ ring vs Cayley graph vs Eisenstein hex are three sheets over the same
cells. Porting between codings stops being rewriting and becomes **map search between sheets**:
graph homomorphisms, coordinate transforms, isomorphism spotting. The sort commands generalize:
SORT by spectral gap (Rollier's adjacency eigenvalues — dynamics predicted before simulation),
SORT by Betti class (which holes exist in the fleet graph), SORT by census grain (E7's
class-level transfer: cell identity is private, cell classes port).

**The rule:** if a port can be expressed as a sheet operation on the switchboard data, it
ports mechanically — byte-identity checkable by diff. If it can't, it isn't a port, it's a
rewrite, and it gets booked as one. This is what "far beyond linear book-keeping" buys:
encodings that can be sorted, transformed, and composed like any other cell range —
with the tick contract as the invariant that makes every such transformation auditable.

---

## §9 The spin: projection as a dial, alignment as runout (Casey, 21:00 AKDT)

§8 let you PICK a plane. §9 makes the picking continuous: **the X/Y setting is a dial, and
you can spin it.** Each setting of the projection plane reveals a different mathematical
abstraction sitting in the same fabric — and the revelation isn't a lookup, it's a sweep.

The machinist's move (the dial indicator on an engine-shaft coupling): you don't compute
alignment, you *sweep* the gauge around the shaft and read eccentricity off the needle.
Porting two codings is coupling two shafts: mount the gauge, spin the transform, and the
projection's roughness IS the misalignment. A smooth sweep — abstraction revealing itself
continuously as the plane turns — means the codings are concentric (the port is mechanical,
byte-identity holds by construction). A jump, a flat spot, a chatter in the sweep — that's
runout, and its phase tells you WHICH joint is off and by how much. Divergence gets a
reading, not just a verdict.

**What spinning adds over picking:**
- **Concentricity tests.** Zₙ → Cayley → hex: rotate the coding dial continuously and watch
  the census. E7 predicts what the needle does — identity grain jumps discretely (cells are
  private), class grain sweeps smoothly (classes port). The smooth/jump boundary on the dial
  IS the transferable-structure measurement.
- **Resonance survey.** Oscillate the plane (small periodic modulation of the transform) and
  the fabric answers: abstraction modes ring where the substrate has structure — spectral
  gap as a resonance peak, Betti class as a standing wave. The trajectory of revealed
  abstractions is itself data, the way fish-school momentum is data: not the position of
  the truth but its drift.
- **Coupling procedure.** Port = align = sweep until runout ≤ 1 lattice quantum, then lock
  the transform and diff the ticks. Byte-identity is zero runout. Everything else is booked
  with its eccentricity value attached.

The dialometer, in charter terms: a continuous SORT whose parameter is a rotation, whose
readout is smoothness, and whose purpose is alignment. Turing's head moved along a tape;
our head moves *around the space of planes* — and the shape of that motion is the last
mathematical abstraction the fabric was hiding.

### §9 correction (Casey, 21:01 AKDT): the dial reads as a wave; the gauge reads in points.

The dial indicator's needle is analog — reading it directly is continuous cheating. The honest
instrument on an engine coupling is the **feeler gauge**: discrete blades, each a quantum thick,
each measurement a boolean — the blade fits the gap or it doesn't. No needle, no wave. Points.

So the dialometer is instrumented as a **feeler-gauge bank**: at each rotation of the coding
plane, test fit at lattice quanta — does the q-blade enter the coupling gap, yes or no. The
runout profile is never read continuously; it is RECONSTRUCTED from the point vector, and the
shape lives only in the relation across the booleans.

Which is the hundred hooks again, at the coupling: every blade is a hook, every sweep is a
pull, the eccentricity is H¹ of the boolean vector. The wave is the abstraction; the points
are the evidence. The fabric can only ever be sampled where a blade fits — and that is not
a limitation to apologize for, it is the quantization that makes the reading auditable.
Integer discipline holds even in the machinist's metaphor: sweeps propose, blades dispose.

### §9 second amendment (Casey, 21:02 AKDT): blades slide until they log — snap points.

Refinement: the gauge blade is not tested at a fixed position. It is SLID into the gap until
it LOGS — seats, catches, stops. The seating position is the measurement: a **snap point**,
the local quantum where wave-amplitude equals blade-thickness. Between snap points you may
extrapolate the wave — but the extrapolation is a proposal; the log is the evidence. Every
smooth curve on the dial must trace back to a list of seating events or it is fiction.

This is the fabric's own conversion principle, seen once and used everywhere:
- the cell SLIDES (act accumulates) until it LOGS (fire test crosses threshold) — the fire
  event is a snap point of the pulse wave, and deadband residency is the gap between logs;
- the troller SLIDES (gear drifts through probability space) until it LOGS (a hook catches) —
  the hookup is a snap point of the fish-density wave, and the day's catch is the log;
- the census SLIDES (routes quantize) until it LOGS (a cell is entered) — E7's route events
  are snap points of the embedding wave.
Snap-point logs are the integer trace from which any wave may be proposed, replayed, and
audited. Interpolation is admissible; extrapolation is admissible; unanchored curves are not.
The ledger is the log; the ratchet is which snaps we keep.

---

## §10 The cheat-code (Casey, 21:07 AKDT)

Quantum computing forums keep an honest list: math that can't be done effectively on a
classical computer — exact simulation of large entangled states, exact sampling from
quantum distributions, Shor-class period finding. The fabric's claim is not that the list
is wrong. It is that **for many examples on the list, we hold a cheat-code** — the same
three techniques every time:

1. **Re-aim at the snap points.** Quantum hardness is usually hardness of tracking the full
   wave (amplitudes everywhere). Most USEFUL answers are where the wave logs — ground states,
   samples, crossings, seatings. A fabric of integer pulses with fire-thresholds IS a
   snap-point engine: it never pays for the amplitudes, only for the landings. (E1: 83% vs
   52% by tracking cancellation events, not the field.)
2. **Integer superposition instead of complex amplitudes.** Quantum walks interfere because
   amplitudes add; quilt cells interfere because pulses cancel — signed, superposed, locally.
   Where the target is interference STATISTICS (which configurations get hit, how often),
   quantized cancellation reproduces the wanted histogram without unitarity. (E7: class grain
   transfers; identity grain doesn't — the cheat lives exactly at class grain.)
3. **Thermodynamic sampling without coherence.** The p-bit result (RD-PHYSICAL #1): thermal
   superposition — coin mid-flip — licenses parallelism the coherent view says you can't
   have. The dice gear and the decay queue are the room-temperature stand-ins. (The known
   boundary, kept honest: arXiv:2608.09743 — noise is redundant for convex problems; the
   cheat applies where the landscape is what's being searched.)

**The family this belongs to: dequantization.** Ewin Tang's line of work (2018–) showed
several "quantum-only" algorithms have classical analogues once you swap amplitude access
for sample access. The fabric is the sampling-access machine taken seriously: a computer
whose ONLY readout is feeler-gauge points, and therefore one that never owes the exponential
bill for the wave. The honest edges stay on the page: no cheat for Shor, no cheat for exact
amplitude queries, and every claimed cheat must name its grain (§9) and pass byte-identity
or book its runout.

Cheat-code, precisely: **when the answer is where the wiggle ends, don't simulate the wiggle.**
