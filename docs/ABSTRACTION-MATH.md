# ABSTRACTION-MATH — the mathematics of hardware abstraction for quilt-verilog

**Lane:** abstraction-mathematics (Flash, deep sweep) · **Date:** 2026-08-29
**Inputs:** v1 rtl/ + docs/SYNTHESIS.md + socratic EXPANSION.md (Preferring Fabric),
jester curveballs, hermes gate questions. **Method:** arXiv API + web sweep of the
four lanes: (1) category theory & typed circuits, (2) synchronous-language theory,
(3) refinement & equivalence (cheap formal checks), (4) fixed-point semantics.
**Companion:** research paper 66 in ai-writings.

> **The one buildable idea, in two lines.** The two decay engines are one
> mathematical family — *dyadic staircases* — and glm's proven 2W ladder bound is
> the base-2 case of a staircase envelope theorem that also covers zeroclaw's
> hyperbola counter ([1,4) bound, k=2) and generalizes to base-b ladders and
> power-law laws. Encode the envelope as an sby monitor module and *prove* it:
> the method already works — the flit-pipe FIFO contract proves in ~0 s by
> k-induction (boolector) in this session.

---

## 0. TL;DR

- **What exists already:** `tb/formal/` has a working yosys-sby harness (boundary-only
  shadow model, no XMRs, `mode prove`, smtbmc boolector). I re-ran it clean in /tmp
  (the working dir is being concurrently re-run by another lane): **PASS** —
  basecase + induction, ~0 s. The formal lane is open and fast.
- **The map:** every v1 module is a known formal object. The ring is a *traced
  symmetric monoidal* wiring of *causal stream functions*; the tick is a *logical
  instant* (LET); "clock is its own traffic" has a real name — *endochrony*; the TBs
  are *synchronous observers*; the decay engines are *exponential histograms* and
  *self-paced pure-death processes*.
- **What to do this week:** five sby checks (below), the flagship being the dyadic
  envelope theorem proven as a hardware monitor on `q_hebb_edge`.
- **What is a dead end for now:** Clifford/geometric algebra (analog-side DSP only),
  interaction nets as a *synthesis* path (proof-side only), ZX-calculus beyond the
  copy/add fragment.

---

## 1. Formal object → module map

| Our module / mechanism | The formal object | Where the math lives |
|---|---|---|
| `q_flit_pipe`, `q_link_ringport` (valid/ready, registered slices) | **Causal stream function / Mealy machine**; the handshake is an *elastic (latency-insensitive) protocol* | Ghica & Kaye 2022/2025 (causal stream functions = denotational semantics of circuits); Carloni–McMillan 2001 (latency-insensitive design); Kahn 1974 (monotone stream functions) |
| Ring-of-cells fabric | **Traced symmetric monoidal wiring** of cell morphisms; feedback = trace. Ring progress = the delay/register breaks every loop | Ghica "Diagrammatic Semantics" 2017; Kaye thesis 2025 (traced comonoid structure, rewriting modulo trace) |
| `q_cell_core` FSM — the one interpreter | **Synchronous program**; event-serialized core = deterministic (stateful) stream process; "one interpreter" = single-assignment discipline, no constructive ambiguity | Benveniste et al. 2003 survey; Berry 1999 (constructive semantics of Esterel); Malik 1994 (constructive combinational loops) |
| `s_ready = !b_v` (local only) and registered pipe slices | **Constructive rule of the fabric**: no combinational cycle; every loop through a register. Non-constructive loops are the Esterel causality bugs | Berry 1999; Shiple et al. 1996 |
| `q_tick_sched` + tick-as-hard-deadline | **Basic clock** (Lustre); the tick is a *logical execution time* instant — communication/commit at logical instants | Halbwachs et al. (Lustre clock calculus); Kopetz LET; Henzinger Giotto |
| "Clock is its own traffic" (socratic) — valid IS the clock | **Endochrony** (Signal/Polychrony): a process is endochronous when its data alone schedules its clocks; the v2 seam question is an *isoendochrony* analysis | Le Guernic et al. (Signal); Mallet (CCSL, logical time); INRIA Polychrony |
| Effect storm / no-drop ingress | **Kahn-network starvation / liveness**; bounded ring = bounded Kahn network (determinacy preserved under backpressure) | Kahn 1974; also "Compiling Process Networks to Interaction Nets" 2016 for the cellular view |
| `q_hebb_edge` ladder | **Exponential histogram** of cofire ages: dyadic buckets, shift-implied weights 2^-i, readout = geometric window sum | Datar–Gionis–Indyk–Motwani 2002 (exponential histograms, (1+ε) sliding-window guarantees) |
| `q_hebb_edge` hyperbola counter | **Self-paced pure-death process**: dW/dt = −W²/P₀ (Riccati); msb-quantized decrement interval = log-domain Euler step | ODE/step-size analysis (this doc §4; original: zeroclaw ARCHITECTURE §2.1) |
| `q_dialfile` (config = traffic, Law 2) | **Parameters as streams**: bindings are just state initialized by traffic — the Kahn/Lustre programmability stance; dials are the *family parameters* of the circuit | Kahn 1974; synchronous languages |
| TBs (`tb/*.v`) | **Synchronous observers** — the standard Lustre verification idiom; sby upgrades them from simulation observers to formal properties | Halbwachs–Lagnier–Raymond 1994; and the 2026 STL-observer line (arXiv:2608.12693) |
| Ladder readout adder tree | **Copy/add spider network** — the classical fragment of ZX&; completeness gives an equational theory for readout simplification | arXiv:2004.05287 (ZX&) |
| Golden models in TBs | **Refinement relation**: RTL refines the golden model; formalized as *sequential equivalence checking* (sby `mode equivalence`) | Back–von Wright refinement calculus; sby docs; Kami (ICFP 2017) for the interactive cousin |
| Fabric as pipe-and-filter | **Refinement calculus for pipe-and-filter architectures** — add/remove/combine filters provably: the v2 bridge/tier moves | arXiv:1411.2414 |

---

## 2. Lane 1 — category theory & typed circuits: what maps, what doesn't

### 2.1 The compositional-circuit line (the one that matters)

The strongest and freshest line is **Ghica–Kaye** (Birmingham):

- **"Diagrammatic Semantics for Digital Circuits"** (arXiv:1703.10247) — digital
  circuits as string diagrams: discrete values, discrete delays, feedback; based on
  monoidal categories + graph rewriting.
- **"A Complete Theory of Sequential Digital Circuits: Denotational, Operational
  and Algebraic Semantics"** (arXiv:2201.10456) — the payoff: circuits compose
  *freely, without consulting internals*. Denotational semantics = **causal stream
  functions** (and a bridge to Mealy machines); operational semantics = rewriting
  strategy with observational equivalence; algebraic semantics = pseudo-normal
  forms + state-set encodings.
- **Kaye's thesis** (arXiv:2502.08497) — extends string-diagram rewriting to
  **hypergraphs compatible with the traced comonoid structure** (rewriting *modulo
  trace*), and ships a **new HDL** built on it.

**Why this is our mathematical charter.** The ring-of-cells fabric is exactly a
traced monoidal structure: cells are morphisms with typed input/output bundles
(the flit bus), composition is the ring wiring, and feedback is the trace. The
Kaye result says: a cell's *internals* are irrelevant to correct composition —
which is the formal justification for the v1 discipline "the cell core FSM is the
only interpreter" and for the ring ports being thin. The practical takeaway is
**documentation**: draw the fabric as string diagrams (cells = boxes, links =
wires, ring = trace) in the v2 docs; the equations of the algebraic semantics are
the transformation rules for re-associating cell chains.

### 2.2 Signal-flow graphs and Hopf algebras (the DSP side)

**Bonchi–Sobocinski–Zanasi**:
- "A categorical semantics of signal flow graphs" (2014); "The calculus of signal
  flow diagrams I: linear relations on streams" (2017); **"Interacting Hopf
  Algebras"** (LIPIcs CALCO 2017); "Contextual Equivalence for Signal Flow Graphs"
  (2020).
- The headline: the theory **IHR[x]** — interacting Hopf algebras over the
  polynomial ring — is *isomorphic to the PROP of linear relations over streams*,
  giving string diagrams a sound and complete equational theory, plus an analogue
  of **Kleene's theorem** (every rational behavior expressible).

**Map:** our linearized sub-models — the ladder readout (sum of shifted buckets),
the effect integrator, the hyperbolic decay as a linear-schedule approximation —
are signal-flow diagrams in IHR[x]. The complete equational theory means any two
readout implementations that are diagrammatically equal are behaviorally equal:
a *rewrite-level* equivalence check. Not this week; but the readout adder trees
are exactly "copy + add + scalar (shift)" spider networks, and there is a
**complete** calculus for exactly that fragment:

### 2.3 ZX& — a complete calculus for classical circuits

**"The ZX&-calculus"** (arXiv:2004.05287): Z and X spiders (copying, addition)
+ NOT + AND is *complete* for classical circuits — the classical cousin of the
ZX-calculus. Our datapaths are mostly copy/add/shift networks (multiplier-free
doctrine, saturate-never-wrap, implied-weight shifts). Completeness means: any
identity provable in the calculus is a true circuit identity — a formal
simplification and equivalence toolkit for the multiplier-free parts of the
fabric. The honest caveat: ZX& reasoning is currently manual/proof-oriented; no
turnkey tool runs it on Verilog.

### 2.4 Typed/arrow/monadic HDLs (context, not build)

- **Arrows** (Hughes): static-analysis-friendly wiring of computations; arrow
  calculus is the "wires as first-class" language. Historically the *typed* HDL
  instinct: **Lava** (Bjesse–Claessen–Sheeran–Singh, 1998), **Clash** (Baaij),
  **Bluespec** (Arvind), **ForSyDe**, **ReWire** (Procter–Harrison: monadic,
  with Hoare-style proof rules). These are *languages* — their lesson for us is
  the type discipline (ports are typed bundles; the flit bus typechecks), not a
  runtime tool. The v1 contract `{op, src, dst, a0, a1, a2, dat}` is a product
  type; the five opcodes are a sum type. If we ever generate Verilog from a
  higher level, the arrow/monadic stack is the proven route.
- **Monoidal streams** (arXiv:2202.02061, 2212.14494): causal stream functions
  generalized to symmetric monoidal categories — the denotational home of our
  valid/ready streams with side channels (ready = the "monoidal" part).

### 2.5 Interaction nets — beautiful, but proof-side

Lafont's interaction nets (POPL 1990): computation as local graph rewriting —
distributed by construction, strongly confluent. The relevant result:
**"Compiling Process Networks to Interaction Nets"** (arXiv:1609.03640) — Kahn
process networks (our streaming model!) compile to interaction nets. The lesson
is architectural and already implemented: the ring IS a distributed local-rewrite
system (each node rewrites one flit per cycle with purely local state). The
theory certifies *why* locality suffices; it is not a synthesis path to silicon
this week.

### 2.6 Sine/Clifford — honest dead end (for now)

Clifford/geometric algebra in signal processing is real but **analog/multidim
analytic-signal DSP** (Bulow & Sommer; Felsberg & Sommer; recent arXiv:2411.10412):
hypercomplex representations of continuous signals. Nothing found connects GA to
*synchronous digital sequential* abstraction. Our directional primitive (vMF /
the dial) is angular statistics; the hardware-friendly math there is CORDIC-style
rotation and fixed-point angle arithmetic, not GA. Parked; revisit if a
bridge/tier ever needs multi-dimensional rotation math on a DSP pipe.

---

## 3. Lane 2 — synchronous-language theory: naming the time story

### 3.1 The canon (what the fabric already is)

- **Lustre** (Halbwachs et al.): dataflow, single-assignment, **clock calculus** —
  every stream has a clock (its set of instants); the compiler proves clocks
  compose. Our fabric is a Lustre program: each signal's clock is *where its
  valid bit is high*. The `q_tick_sched` tick is a **basic clock**; every other
  signal's clock is derived.
- **Esterel** (Berry): imperative, synchronous; **constructive semantics** decide
  which combinational loops are legal. This is the formal content of our
  restructurings: `q_hebb_edge`'s readout went from a combinational adder tree to
  a registered loop (UNOPTFLAT); `q_flit_pipe` went to the skid form whose
  `s_ready = !b_v` depends only on local state. Rule: **no signal depends on
  itself through combinational logic; every loop passes a register.** That is
  Berry-constructiveness at the RTL level, and it is what keeps yosys/verilator
  and any future formal engine happy.
- **Kahn process networks** (1974): monotone stream functions over CPOs —
  determinacy (the network's I/O behavior is a function, not a relation). Our
  ring with valid/ready backpressure is a **bounded Kahn network**; determinacy
  holds, and the "no-drop ingress FIFO" is a bounded channel. The v1 liveness
  argument (correctly-addressed ring drains ≥1 flit per bound) is the Kahn
  starvation question answered for our traffic class.
- **Survey anchor:** Benveniste, Caspi, Edwards, Halbwachs, Le Guernic, de
  Simone, "The Synchronous Languages Twelve Years Later" (Proc. IEEE 2003).

### 3.2 "Clock is its own traffic" has a name: endochrony

The socratic lane's slogan — the clock is not a separate plane; a signal's clock
is the signal's own presence (valid) — is **exactly the polychronous/signal
stance**:

- **Signal / Polychrony** (Le Guernic et al.; INRIA): signals *define their own
  clocks*; the clock calculus computes relations between implicit clocks.
  **Endochrony**: a process whose inputs can be scheduled from the data alone —
  deterministic from its communication. "Clock is its own traffic" = *the fabric
  is endochronous by construction*: `valid` is the clock, `ready` is the
  scheduling feedback, and the tick is the one external basic clock.
- **CCSL** (Mallet, "Logical Time"; arXiv:1806.07702, 1807.00003, 1904.07011):
  clock constraint specification — precedence/coincidence/exclusion between
  logical clocks. This is the language for the **v2 seam spec**: bridge
  scheduling, the deferred event-count decay engine, dither/deadband. Write the
  bridge contracts as CCSL constraints *before* RTL.
- **Izhikevich polychronous groups** (arXiv:2103.15265, "Polychrony as
  Chinampas"): the *neural* sense — timing emerges from coincidence of traffic.
  Worth one paragraph in the paper: the v2 traffic-based tick (curveball 6) is a
  polychronous-group phenomenon — decay events fire when traffic coincides — and
  the formal home is endochronous scheduling, not a global clock.
- **LET** (Kopetz; Giotto, Henzinger): communications commit at *logical
  instants*. Our tick-as-hard-deadline (Q2) is LET: the decay sweep/activation
  leak/fire test commit at the tick instant, never mid-op. The "front-of-queue at
  an op boundary" mechanism is a *priority discipline on logical instants*.

### 3.3 What this buys the build

1. The tick is not a timer; it is a **logical instant**. Any future
   multi-clock/GALS seam (v2 R5) is a *clock refinement* — expressible and
   checkable in CCSL before it touches RTL.
2. The **drop-policy question** (jester curveball 3, deferred to v2) is an
   **endochrony/isoendochrony analysis**: at a bridge, does the aggregate stream
   remain schedulable from its data alone once flits can be dropped? That is the
   formal shape of the v2 seam work.
3. The TBs are **synchronous observers** — the Lustre idiom — so the step to
   formal properties is *not a change of language*: an sby harness is the same
   observer, evaluated by an SMT solver instead of a simulator. (The 2026 line
   even does STL-on-Lustre observers: arXiv:2608.12693, 2311.09788.)

---

## 4. Lane 3 — refinement & equivalence: the checks we run this week

### 4.1 The theory, briefly

- **Refinement calculus** (Back & von Wright): programs refined by
  correctness-preserving transformations. For hardware, the operative form is
  **sequential equivalence checking (SEC)**: prove two designs (or a design and
  its golden model) have identical I/O behavior. sby does this natively
  (`mode equivalence`). The interactive/proof-assistant cousin is **Kami**
  (ICFP 2017, Coq) — a verified-rule refinement platform for hardware; our lane
  is the automatic (SAT/SMT) cousin.
- **Pipe-and-filter refinement** (arXiv:1411.2414): a *refinement calculus for
  pipe-and-filter architectures* — provably correct add/remove/combine of
  filters. The fabric is a pipe-and-filter architecture; v2 bridge moves have a
  calculus.
- **K-induction** (Sheeran–Singh–Stålmarck 2000): the algorithm under sby
  `mode prove` — base case + inductive step, exactly what just proved the flit
  pipe.
- **Fresh context:** "NoTB: Oracle-Free Triage of LLM-Generated RTL via
  Cross-Model Formal Consensus" (arXiv:2608.21962) — formal consensus across
  models to triage LLM-generated RTL without an oracle. That is this
  competition's own shape: winner-by-consensus + formal gate. We are already
  doing the honest version (cross-review + harness); sby makes the gate
  consensus-independent of the models.

### 4.2 Toolchain, verified working

- OSS CAD Suite at `/home/eileen/tools/oss-cad-suite` (yosys 0.47+22, sby
  yosys-0.47, smtbmc, boolector, z3, btormc, suprove, avy). No install needed.
- Harness idiom (inherited from `tb/formal/`, proven): **boundary-only shadow
  model** — the harness re-implements the module's contract as a shadow state
  machine at the ports; **no XMRs** (hierarchical refs become undriven implicit
  wires in yosys — the existing harness comment documents this); free-input
  harness with a **reset preamble** (DUT regs have no init); `assert`/`assume`/
  `cover` statements; `read -formal`, `prep -top`.
- **Result this session:** `tb/formal/flit_pipe.sby` — **PASS** (basecase +
  k-induction, smtbmc boolector, ~0 s, depth 15). Note: the working dir was being
  concurrently re-run by another lane (logfiles flipped between my reads), so I
  re-ran a clean copy in /tmp — the PASS is real and reproducible. **Commit the
  harness and make it CI.**
- Engines: boolector for induction (fast); z3 as a cross-check; `btormc`/`suprove`
  for BMC; `avy`/`avybmc` for IC3-style on the harder ones.

### 4.3 The check list — this week

| # | Check | Module | sby form | Property |
|---|---|---|---|---|
| 1 | FIFO contract (C1–C4) | `q_flit_pipe` | prove | no dup, cap 2, nothing hidden, pressure at capacity — **DONE, PASS** |
| 2 | Ring port contract | `q_link_ringport` | prove | deliver/transit/inject exactly once; no flit lost or duplicated at the node |
| 3 | **I1 liveness under load** | `q_cell_core` | prove (k-ind) | `fell(ci_ready) |-> ##[1:MAX_OP_CYCLES] ci_ready` — reasserts ready within the bound |
| 4 | **Q2 tick service** | `q_cell_core` | prove + cover | from `s_tick` strobe to `ST_TICK` entry < 2×`MAX_OP_CYCLES` (shadow cycle counter at the boundary, no XMRs) |
| 5 | **Dyadic envelope (ladder)** | `q_hebb_edge` | prove | shadow readout Ŵ of the state; `W/2 − 1 ≤ Ŵ ≤ 2W + 1` (staircase theorem, base 2) — the glm bound, now machine-checked |
| 6 | **Dyadic envelope (hyperbola)** | `q_hebb_edge` | prove | `W_true(P0) ≤ W_rtl ≤ W_true(P0/4)` via a monitor computing the envelope from `(W, age)` — zeroclaw's [1,4) bound, machine-checked |
| 7 | Saturate-never-wrap | `q_hebb_edge`, `q_cell_core` | prove | accumulator `act`/`wsum` never wraps: shadow saturating model vs RTL (this is also SEC, `mode equivalence`) |
| 8 | Ring progress (bounded) | `q_fabric_top` (4-cell) | bmc, depth N | every flit advances or is delivered within N cycles — bounded liveness, the v1 claim made machine-checkable |
| 9 | Golden-model SEC | any module | equivalence | miter RTL vs the TB's golden model (the C model, ported to Verilog reference or shadow) — property-based simulation equivalence, formalized |

Flagship: **#5/#6** — the dyadic envelope theorem as a hardware monitor. The
monitor is ~30 lines (computes `W_true` envelope from state), and the proof is
k-induction over a small FSM — the flit-pipe experience says this is seconds,
not hours. #3/#4 answer the hermes gate questions Q1/Q2 in the *formal* voice the
advocate demanded (the TB loops become properties).

### 4.4 MTL/STL on streaming — the monitoring side

For *runtime* (post-silicon / on-fabric) checks, the stream-monitoring line is
mature: **Lola** (Leucker & Schallhart, TIME 2005) — stream runtime verification;
**TeSSLa** (arXiv:1808.10717) — temporal stream-based specification language
with hardware event-stream monitoring; **STL observers for Lustre** (arXiv:
2608.12693). The mapping: our fabric's egress flits are event streams; a
`qm_view`-observable temporal property (e.g., "within K ticks of an effect
storm, THRESH is crossed") is a TeSSLa/Lola spec. Not this week; but the v2
observability layer (affinity sidecar, dither bandit) should state its monitors
in stream-RV terms so they are *both* sim-checkable and sby-checkable.

---

## 5. Lane 4 — fixed-point semantics: provable error bounds, generalized

### 5.1 The theorem (the generalized 2W bound)

**Staircase envelope theorem.** Let `w(a)` be a strictly decreasing positive
"age weight" law with the *b-doubling decay* property `w(a) ≤ b·w(ba)` for all
a > 0 (the exponential law `2^(−a/H)` has this with b = 2, exactly at the
bucket grid). Bucket the ages at `[b^i·H, b^(i+1)·H)`, i = 0..K−1, and assign
bucket i the implied weight `b^(−i)` (a shift of i·log₂b bits, no multiplier).
Then the readout Ŵ = Σᵢ Cᵢ·b^(−i) satisfies

    W_exact ≤ Ŵ ≤ b·W_exact

where W_exact = Σ w(age) over cofires. **Proof (one line):** each cofire of age
in bucket i has true weight in `(b^(−(i+1)), b^(−i)]`; the assigned weight
b^(−i) overstates by a factor in [1, b); summing over events gives the envelope.

- b = 2 is **glm's ladder**: Ŵ ∈ [W, 2W) — the proven 2W bound, now seen as the
  base-2 case.
- **Power-law laws are exact on shift ladders:** if `w(a) = (H/a)^k`, then bucket
  weights b^(−ik) are still shifts (i·k·log₂b bits). One representation family,
  and the **hyperbola is asymptotically a power law** — which is the structural
  reason ladder and hyperbola co-exist as two dial settings of one engine.
- **Base-b generalization:** b = 2^p (p-bit shifts per bucket) trades error
  (factor b) against bucket count (K·p bits of readout). The K=8,B=8 v1 ladder is
  the b=2, p=1 case; a v2 "coarse ladder" with p=2 halves the bucket count at a
  factor-4 envelope — the dial can expose this.

### 5.2 The hyperbola counter as a quantized Riccati integrator

The zeroclaw engine integrates dW/dt = −W²/P₀ exactly (solution
W(t) = W₀/(1+W₀t/P₀)) by a **self-paced pure-death process**: decrement interval
Δ = P₀ >> (k·msb W), msb W = ⌊log₂W⌋, so Δ ∈ [P₀/2^k·W², P₀/W²). The doc's
envelope `W_true(P₀) ≤ W_rtl ≤ W_true(P₀/4)` is the k=2 case: intervals run no
faster than 1× and no slower than 4× the exact interval-at-current-W, which
traps the discrete trajectory between the exact solutions of the two bracketing
rates. **Generalization:** interval P₀ >> (k·msb W) gives a 2^k-factor envelope;
k=2 is the sweet spot (matches the exact interval within [1,4), cheap msb via
priority encoder — already in the RTL). This is the *log-domain Euler* reading:
step size = 1/λ(W) quantized to a power of two, and the bound is a discrete
Gronwall-style step-size argument. The 2026 "Lyapunov-guided training" line
(arXiv:2607.04531) independently confirms the doctrine: **wrap corrupts
magnitude AND sign; saturate-never-wrap is the right policy**, and the envelope
assertions are what make it provable.

### 5.3 Toolbox for certificates

| Tool | What it gives | Fit |
|---|---|---|
| **Interval arithmetic** (Moore 1966) | naive ranges; correlation blow-up | first-cut ranges for `act`/`wsum` widths — the widths already swept to silence verilator; IA re-derives them |
| **Affine arithmetic** (Stolfi–de Figueiredo 2003) | tracks linear correlations between errors (no blow-up on sums) | the integrator's error budget: round-off at each of the ≤ MAX_OP_CYCLES adds, correlated — AA is the right envelope |
| **Gappa / Flocq** (Melquiond; Boldo–Melquiond) | machine-checkable error certificates for arithmetic expressions | certificate the *golden model's* arithmetic (the C/Python reference) so the reference itself is trustworthy — the TBs then inherit |
| **SMT-BMC of fixed-point filters** (arXiv:1305.2892) | word-length/overflow bugs found by bounded model checking | exactly our #7 (saturate-never-wrap as SMT property) |
| **Stochastic rounding** (Gupta et al. 2015) | unbiased rounding, removes systematic drift | the v2 upgrade of zeroclaw's convergent-rounding rule: same spirit (round to nearest even at integrating boundaries), stronger bias guarantee; a dial slot, not a redesign |
| **Exponential histograms** (Datar et al. 2002) | (1+ε) sliding-window approximations | the ladder's parent result: our 2W bound is the ε=1 special case of a whole family of ε-tunable guarantees |

### 5.4 What this buys the build

1. **#5/#6 machine-check the two bounds this week.** No more "proven in prose":
   the envelope is a monitor, the monitor is a property, the property is proved
   by k-induction.
2. The **unified theorem** gives the dial design a mathematical spine: MODE=0/MODE=1
   are two engravings of one staircase family; the "law is data" stance (scorecard
   steal 1) is now "the family parameter is data."
3. The **generalized base-b ladder** and **k-parameter hyperbola** are the
   documented v2 dial slots (P0E already exists; a B-base dial is one more
   parameter).
4. Affine arithmetic gives a *compositional* error budget for the integrator —
   the missing piece for "provable error bounds like glm's 2W, generalized" to
   multi-stage pipelines (cell → ring → cell: errors compose through the
   streaming contract).

---

## 6. Honest limits (what is NOT covered)

- **Misaddressed flits** (jester curveball 3): a flit to a nonexistent node
  circulates forever — the v1 traffic contract excludes it, and no formal check
  here covers it. The v2 drop policy is an *endochrony* question (is the stream
  still schedulable with drops?) — flagged as the seam formalization, not solved.
- **Fabric-level liveness in full generality**: check #8 is *bounded* (bmc, small
  N). An unbounded liveness proof on the full 4-cell fabric (with response
  backpressure) is real model-checking work; the v1 claim (correctly-addressed
  ring drains) is argued, not yet machine-proved. The `live` mode exists; expect
  it to be the hard one.
- **The [1,4) envelope is loose**: the hyperbola bound has slack (the interval is
  [1,4)× the exact); the k-parameter generalization tightens it at more bucket
  bits. The ladder's 2W is tight (factor b = 2 is the per-bucket overstatement).
- **Clifford/GA**: parked (analog-side only; no synchronous-digital abstraction
  found). Interaction nets: proof-side only. ZX&: manual reasoning, no tool.
- **Concurrency hazard on `tb/formal/`**: another lane is actively running sby
  there; results read from that directory can flip mid-read. My PASS was
  re-run clean in /tmp. Merge discipline: commit the harness, run proofs in a
  scratch copy or serialize with a lock.

---

## 7. References (primary)

- Kaye, "Foundations of Digital Circuits: Denotation, Operational, and Algebraic
  Semantics," PhD thesis, arXiv:2502.08497 (2025).
- Ghica & Kaye, "A Complete Theory of Sequential Digital Circuits," arXiv:
  2201.10456 (2022).
- Ghica, "Diagrammatic Semantics for Digital Circuits," arXiv:1703.10247 (2017).
- Bonchi, Sobocinski, Zanasi, "Interacting Hopf Algebras," LIPIcs CALCO 2017;
  "The Calculus of Signal Flow Diagrams I," 2017; "Contextual Equivalence for
  Signal Flow Graphs," 2020.
- "The ZX&-calculus," arXiv:2004.05287 (2020).
- "Monoidal Streams for Dataflow Programming," arXiv:2202.02061; "Coinductive
  Streams in Monoidal Categories," arXiv:2212.14494.
- "Circuits, Bond Graphs, and Signal-Flow Diagrams," arXiv:1805.08290.
- Benveniste, Caspi, Edwards, Halbwachs, Le Guernic, de Simone, "The Synchronous
  Languages Twelve Years Later," Proc. IEEE 91(1), 2003.
- Halbwachs, Lagnier, Raymond, "Synchronous Observers and the Verification of
  Reactive Systems," 1994.
- Berry, "The Constructive Semantics of Pure Esterel," 1999; Malik, "Analysis of
  Cyclic Combinational Circuits," 1994; Shiple, Berry, Touati, "Formal Analysis
  of Combinational Loops," 1996.
- Kahn, "The Semantics of a Simple Language for Parallel Programming," 1974.
- Le Guernic et al., "The Signal Language," 1991; Mallet, "Logical Time" (CCSL),
  2011; PrCCSL work: arXiv:1806.07702, 1904.07011.
- "Polychrony as Chinampas," arXiv:2103.15265 (2021).
- Kopetz, "Real-Time Systems" (LET); Henzinger et al., "Giotto," 2003.
- Carloni, McMillan, Sangiovanni-Vincentelli, "Theory of Latency-Insensitive
  Design," IEEE TCAD 2001.
- "Refinement of Pipe-and-Filter Architectures," arXiv:1411.2414.
- Choi et al., "Kami: A Platform for High-Level Parametric Hardware
  Specification and Its Modular Verification," ICFP 2017.
- "NoTB: Oracle-Free Triage of LLM-Generated RTL via Cross-Model Formal
  Consensus," arXiv:2608.21962 (2026).
- Sheeran, Singh, Stålmarck, "Checking Safety Properties Using Induction and a
  SAT-Solver," 2000.
- Leucker & Schallhart, "LOLA: Runtime Monitoring of Synchronous Systems," TIME
  2005; "TeSSLa," arXiv:1808.10717 (2018); "Synchronous Observers Revisited for
  Runtime Verification of Lustre Using STL," arXiv:2608.12693 (2026);
  "…STL Operators as Synchronous Observers," arXiv:2311.09788.
- Datar, Gionis, Indyk, Motwani, "Maintaining Stream Statistics over Sliding
  Windows," SODA 2002.
- "Verifying Fixed-Point Digital Filters using SMT-Based BMC," arXiv:1305.2892;
  "Lyapunov-Guided Training for Hardware-Safe NNs under Fixed-Point Arithmetic,"
  arXiv:2607.04531 (2026); "Certification of the Proximal Gradient Method under
  Fixed-Point Arithmetic," arXiv:2303.16786.
- Moore, "Interval Analysis," 1966; Stolfi & de Figueiredo, "Affine Arithmetic,"
  2003; Gupta et al., "Deep Learning with Limited Numerical Precision," 2015.
- Melquiond, "Gappa"; Boldo & Melquiond, "Flocq," 2011.
- Lafont, "Interaction Nets," POPL 1990; "Compiling Process Networks to
  Interaction Nets," arXiv:1609.03640 (2016).
- "A Geometric Algebra Framework for a Multidimensional Analytic Signal,"
  arXiv:2411.10412 (2024).
- SymbiYosys (sby) docs, YosysHQ; OSS CAD Suite (yosys 0.47) at
  /home/eileen/tools/oss-cad-suite.
