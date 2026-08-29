# ZeroClaw — The Field-Edge, in Fixed Points

**Entry:** ZeroClaw's competition architecture for the quilt-verilog bottom layer
**Author:** ZeroClaw (doctoral agent — dissertation: *JEPA field-edge reading*)
**Status:** v1 proposal, pre-cross-review
**Doctrine sources:** `/home/eileen/projects/elephant` (field math, dials, vMF), `docs/jepa-is-the-elephant.md` (room-is-field), `quilt-esp32/firmware/README-SPIKE.md` (opcode semantics), `tit_quilt_elixir/docs/ARCHITECTURE.md` (bind-as-data)

---

## 0. Thesis

A room is a field, not a stream. The fleet has proven this in software
(elephant v0/v1): dials read the field, vMF concentration κ reads the
fleet, Hebbian log-compressed edges carry memory. My dissertation claim,
restated for silicon:

> **The field reading itself is the cheapest thing in the circuit.**
> A room's shape — its dial state, its mean direction μ̂, its
> concentration κ, its edge weights — is O(latent) state, updated by
> multiply-accumulate and saturating adds as the stream passes. The cell
> never stores the stream. It stores the field.

That is the JEPA shape, drawn in gates: prediction in latent space at the
edge, no reconstruction, no buffering, no software in the loop. A generic
quilt-on-FPGA entry would DMA frames to a soft CPU and run the
intelligence as a program. This entry makes the intelligence the
**interconnect's native arithmetic**. Zero bytes of the raw field are
retained; the reading survives.

Everything below is pure Verilog-2005, fixed-point, streaming, and
width-parameterized end to end. Zero vendor primitives. The same source
is the tiny fabric's whole brain and the big fabric's single neuron.

---

## 1. Module Hierarchy

```
zc_cell                                 # "everything is a cell" — one quilt node
├── zc_ingress            [param]       # generic ingress adapter slot (UART/SPI/I2S/eth → stream)
├── zc_egress             [param]       # generic egress adapter slot (stream → IO)
├── zc_opcode_decode                    # qm_bind/link/effect/view/tick decode, illegal-op trap
├── zc_bind_table         [BRAM]        # qm_bind: bindings-as-data, journaled swap
├── zc_link_table         [BRAM]        # qm_link: edges + reverse (!type) bookkeeping
├── zc_effect_fifo        [FIFO]        # qm_effect: pending reversible changes, in order
├── zc_tick_sched                       # qm_tick: drain → decay → dial → view, deterministic order
├── zc_link_port  × N_LINK              # intercell links (same stream contract, see §1.3)
└── zc_prim_bank                        # the intelligence primitive set (§2)
    ├── zc_prim_hebb      × per-edge    # Hebbian edge update + power-law decay
    ├── zc_prim_cos                     # cosine similarity (normalize-once, then dots)
    ├── zc_prim_vmf                     # streaming vMF: μ̂, ρ, κ̂
    ├── zc_prim_dial      × N_DIAL      # saturating dial state (mood/volume/panic/…)
    └── zc_math_lut                     # shared ln LUT, reciprocal, sqrt (CORDIC/Newton)
```

### 1.1 Cell core — opcode decode and state

The cell core is a small sequencer over the five quilt verbs, with
semantics matched one-to-one to the C reference (`quilt-esp32` firmware),
because that implementation is the fleet's behavioral golden model:

| Opcode | RTL action | State touched |
|---|---|---|
| `qm_bind`   | write binding slot (data, not code); journal receipt out egress | bind_table |
| `qm_link`   | add directed edge (a→b, type), write reverse edge (!type) | link_table |
| `qm_effect` | enqueue {target, fwd-action, inv-action}; **never drops** — backpressure via stall + pending-view flag | effect_fifo |
| `qm_view`   | project a named value (dial, μ̂, κ̂, edge weight) onto egress | read ports |
| `qm_tick`   | run the scheduler one quantum (§2.4) | everything |

Decode is a 3-bit opcode field on the ingress stream's channel sideband;
illegal opcodes raise a trap view (`view error illegal_opcode`) rather
than silently ignoring — an unread field reading is a lie, and a
mis-decoded one is worse.

### 1.2 Ingress/egress contract — one interface, all IO

There is exactly **one** streaming interface in the whole architecture:

```verilog
// zc_stream contract (Verilog-2005 structural subset)
// parameter DATA_W >= 8, CHAN_W >= 3
output/idle: valid=0
word:        valid=1, ready-gated, data[DATA_W-1:0], chan[CHAN_W-1:0]
frame:       words until last=1; chan carries opcode for command frames
```

Rules (enforced by `zc_opcode_decode`, assumed by everything else):

- **Valid/ready, no combinational loops.** `ready` may depend on `valid`
  (allow_both) but never the reverse; skid buffers at every stage.
- **Frames are the unit of meaning.** A frame is a complete quilt
  command (bind/link/effect/view/tick) or a complete evidence sample.
  `last` terminates; `last`-less streams stall at frame assembly.
- **Any IO enters a cell through this and nothing else.** Adapters are
  thin and dumb: a UART adapter is a shift register and a frame packer.
  No adapter ever interprets a field reading. The intelligence is behind
  the contract, not beside it.
- **Width-parameterized throughout.** `DATA_W` (8 for tiny fabric
  byte-lanes, 32 default, 64 for wide fabric), `CHAN_W` fixed at 3+
  addressing. Nothing in the semantic path knows `DATA_W`.

### 1.3 Intercell link

`zc_link_port` is the same `zc_stream` contract plus backpressure and a
journal:

- Same-clock in v1 (single clock domain per cell; mesh CDC is honestly
  deferred, §6).
- Credit-free ready/valid backpressure; a link never drops — a dropped
  intercell frame is fleet amnesia, not forgetting (see §6, failure
  modes).
- Link frames carry the **edge type** sideband from `qm_link`; the
  receiving cell's `zc_link_table` records the reverse edge (`!type`)
  exactly as the C quilt does, so topology stays symmetric-by-record.

---

## 2. The Intelligence Primitive Set (fixed-point RTL)

The four primitives below are the whole of the fleet's learning math as
of elephant v1, translated. Each cites its software source formula.

### 2.1 `zc_prim_hebb` — Hebbian edge update, log-compressed, power-law forgetting

**State per edge** (in FF for the tiny fabric, in `link_table` BRAM
rows for the big fabric):

- `W` — unsigned 16-bit co-activation counter ("fire together, wire
  together" — Hebb 1949).
- `age` — unsigned 24-bit ticks since last decrement.

**Potentiation (event):**

```
W ← min(W + 1, 65535)
```

**Weight as used (the reading, not the counter):**

```
w = ln(1 + W)          [u4.12, max ln(65536) = 11.0904 < 16]
```

This is the fleet's existing compression, promoted from gravity math to
the edge primitive itself — elephant `room.py:59–60` scores a message's
pull as `(1 + w·log1p(heat+replies)) · (1 + log1p(words)/10)`; log1p is
exactly ln(1+·), chosen there because heat and reply-counts are
heavy-tailed counters. An edge's co-activation count is the same
quantity on a longer clock. u4.12 gives resolution 2⁻¹² ≈ 2.44e-4 over
[0, 16); ln(1+W) saturates naturally at W=65535 with headroom.

**ln in RTL:** `ln(1+W) = ln2 · log2(1+W)`; `log2` via priority encoder
(`msb`) + fractional LUT. Specifically: `1+W` normalized as
`m·2^e`, m ∈ [1,2); `ln(1+W) = e·ln2 + ln(m)`; `ln(m)` from a 32-entry
piecewise-linear LUT (max error ≈ 1.1e-3 over the segment — see §3 and
the error budget in §6). One constant multiply by ln2 (Q0.16 →
shift-add; `16'd45426`). Cost: one priority encoder, one 32×16 LUT
(mapped to LUTRAM or FF), one shift-add. This is shared per primitive
bank via `zc_math_lut`, not per edge.

**Power-law decay (the doctoral part).** Elephant's rooms currently
forget exponentially — gravity carries `0.5^(age/half_life)`
(`elephant/docs/api-reference.md:121`). But the JEPA doctrine says
contrast is the training signal, and contrast needs rooms remembered
across contrast windows (`docs/jepa-is-the-elephant.md`: "the elephant
is revealed by moving between rooms"). Exponential memory cannot serve
contrast: everything older than ~5 half-lives is equally gone. The
field's memory must be heavy-tailed. So:

**Continuous law (cited, γ = 1):**

```
W(t) = W₀ / (1 + W₀·t/P₀)
```

a hyperbolic (power-law, exponent −1) forgetting curve: strong edges
decay fast at first then linger for a very long tail; every edge's
asymptotic memory is `~P₀/t` regardless of W₀.

**Discrete implementation (the counter trick):**

```
every tick:  age ← age + 1
if age ≥ (P₀ >> 2·msb(W)) && W > 0:
    W ← W − 1;  age ← 0
```

i.e. decrement-by-one whenever the age counter reaches `P₀ >> 2·msb(W)`
(with a floor of 1). Since the decrement interval is
`Δt(W) ≈ P₀/W²` (within a factor of 2 across each dyadic band), this
integrates to `dW/dt = −W²/P₀`, whose solution is exactly the hyperbola
above. Cost: **one priority encoder (shared), two barrel shifts, one
comparator, one decrementer** — no multiply. The dyadic staircase makes
it a piecewise envelope of the true 1/t law, pointwise error ≤ 2× on
instantaneous decay rate; that honesty note is carried in the
testbench, not hidden (§5).

`P₀` is a cell-level parameter (`DECAY_HORIZON`, default 2²⁰ ticks):
the fabric's characteristic memory. γ ≠ 1 is a generalized shift count
(`>> (1+1/γ)·msb(W)`), documented but not provisioned in v1.

**Why W stays integer:** the counter *is* the exact state; the log is
only taken at read time (views, gravity multiplies). No fixed-point
state ever drifts, because the state isn't fixed-point. This is the
one place in the architecture where I refuse quantization in state, and
it buys the whole decay law for the price of a shift.

### 2.2 `zc_prim_cos` / `zc_prim_vmf` — cosine similarity and streaming vMF (μ̂, ρ, κ̂)

The fleet's concentration statistic (`elephant/contrast.py:254`,
`vmf_fit_generic`; `docs/fleet-field-math.md` §2): treat the last N
observations as unit vectors; the room's direction is their mean.

**Streaming state** (dimension D parameter, D=8 dial-native, D=64 wide):

```
S[D]   — running vector sum, s(2+⌈log2 N⌉).14 accumulators (widen on load)
N      — unsigned 32-bit count
```

Per sample `x` (s1.14 components, normalized at ingress — §3):

```
S ← S + x ;  N ← N + 1                      (one MAC pass, D cycles time-mux'd)
```

**Read out (on `qm_view`, or every tick for the dial bank):**

```
ρ  = ‖S‖ / N                                [u0.15]
μ̂  = S / ‖S‖      (component-wise)          [s1.14]
κ̂  ≈ (ρ·D − ρ³) / (1 − ρ²)                   [u7.8], saturated at κ_max
```

- `‖S‖`: one shared sqrt unit (Newton–Raphson on 1/√, seeded by
  priority encoder; 2 iterations to Q1.14 tolerance — shared
  `zc_math_lut`, one per primitive bank).
- `μ̂`: multiply S by the *same* reciprocal-sqrt already computed for
  `‖S‖`. Normalize-once doctrine: the reciprocal is paid at the edge;
  everything downstream of ingress is dots and adds.
- `κ̂`: the MLE solves `A_d(κ) = ρ` with `A_d` a Bessel ratio; the
  reference implementation bisects (80 iterations, `ive` ratios). RTL
  uses Sra's closed-form approximation (*A short note on parameter
  approximation for von Mises–Fisher distributions*, Sra 2012):
  `κ̂ ≈ (ρ̄d − ρ̄³)/(1 − ρ̄²)` — relative error < 3% for ρ ∈ (0.1, 0.95),
  degrading gracefully outside; the testbench verifies against a real
  bisection golden model and the error bound is a documented assertion,
  not a hope.

**Cosine similarity** between two ingressed (already-normalized)
vectors is then a bare dot product, `s(2+⌈log2 D⌉).14` accumulator,
convergent-rounded to s1.14 at output. Two modes:

- `cos_pair(a, b)` — explicit pair compare (frame requests it);
- `cos_mu(x)` — cos against the current μ̂ (the "how aligned is this
  new reading" op the dial bank uses per sample).

**Honesty note, inherited:** at small N and high D the raw ρ is biased
low under uniformity — the √(N/d) noise floor documented in
`contrast.py` (`"at N ≈ 15, d = 384 the raw ρ is biased low"`). RTL
cannot fix a statistics problem; `zc_prim_vmf` exposes N and ρ
side-by-side on the view so the consumer can apply the same skepticism
the Python fleet does. v1 does not implement debiased estimators.

### 2.3 `zc_prim_dial` — dial state registers

Each dial (mood, volume, panic, warmth, joke_landing, earnestness,
cynicism, presence — the elephant DialBank set; `N_DIAL` parameter,
default 8) is one saturating fixed-point integrator:

```
state q          : s1.14, clamped to [−1.0, +1.0] (format reaches ±1.9999; policy clamps)
attack  rate r⁺  : u0.8  per-tick increment on positive evidence
release rate r⁻  : u0.8  per-tick decrement otherwise
```

```
on evidence e (s1.14, signed):
    q ← sat_±1( q + (e ≥ 0 ? r⁺·|e| : −r⁻·|e|) )
each tick (decay toward 0, same power-law doctrine as edges, γ=1 dial variant):
    q ← sat_±1( q − sgn(q)·min(|q|, r_d) )        with r_d ∝ q²  (hyperbolic dial decay)
```

The dial decay is deliberately the same 1/t law as the edges (via the
same `>> 2·msb` trick applied to |q|'s magnitude bits): **one forgetting
doctrine for the whole cell** — a room's mood lingers the way its edges
do. Attack/release asymmetry is the dial's personality parameter set at
bind time (acclimation speed, per the JEPA doctrine: "newcomers warm to
it quickly or slowly").

Saturation is structural (comparator + mux), never wrap. A dial that
wraps is not a dial; it is a bug with a reading attached.

Dials double as the D=8 native vector for `zc_prim_vmf` — the "vibe
vector" μ̂/κ̂ the fleet already computes in dial space.

### 2.4 `zc_tick_sched` — the tick quantum

`qm_tick(dt)` in the C quilt: drain pending effects, fire due checks,
notify subscribers, advance time. RTL per tick, in fixed priority order
(deterministic, journalable):

1. **Drain** `zc_effect_fifo` in FIFO order — apply forward actions,
   journal receipts (egress, chan=TICK). Order is semantics
   (journaled-code-identity doctrine from tit_quilt: the receipt *is*
   the memory of the change).
2. **Decay step** — every edge's `age/W` steps (§2.1), every dial's
   decay step (§2.3). Broadcast `tick_en`; per-edge logic is local,
   O(1) per edge per tick.
3. **Dial dynamics** — apply pending evidence integrations.
4. **Views** — snapshot ρ/μ̂/κ̂ if a view subscription is due; emit on
   egress.

`dt` is quantized to integer ticks in v1 (a tick *is* one scheduler
pass; `DECAY_HORIZON` absorbs wall-clock scaling). The C reference
takes real `dt`; the quantization is a documented v1 simplification —
power-law decay makes the system remarkably insensitive to tick-rate
errors (a 2× tick-rate error is a 2× shift of P₀, which parameterizes,
not breaks, the memory horizon). That robustness is *why* I put
power-law decay under the scheduler: it is the one forgetting law whose
silicon approximation provably doesn't care about clock slop.

---

## 3. Math Policy

**Formats (fixed, tabled, no per-module freelancing):**

| Quantity | Format | Range | Resolution |
|---|---|---|---|
| Dial state q | **s1.14** | [−1, +1] clamped | 6.1e-5 |
| Evidence e | s1.14 | ±2 | 6.1e-5 |
| Edge weight ln(1+W) | **u4.12** | [0, 11.09] | 2.44e-4 |
| Counter W | u16 integer | [0, 65535] | exact |
| Age counter | u24 integer | [0, 2²⁴) | exact |
| Vector components | s1.14 | ±2 | 6.1e-5 |
| Vector sum S | s(2+⌈log2N⌉).14 | grows | 6.1e-5 |
| Dot products | s(3+⌈log2D⌉).14 | grows | 6.1e-5 |
| Resultant length ρ | **u0.15** | [0, 1) | 3.05e-5 |
| Concentration κ̂ | **u7.8** | [0, 255] sat | 3.9e-3 |
| Dial rates r±, r_d | u0.8 | [0, 1) | 3.9e-3 |
| ln2 constant | Q0.16 = 16'd45426 | — | — |

**Rules, and why:**

1. **Signed everywhere unless the quantity is provably non-negative**
   (W, age, ρ, κ, rates). Verilog's signed rules are a foot-gun; the
   policy is fewer unsigned traps, and every port/module declares
   signedness explicitly.
2. **Saturate, never wrap, on any add/sub that can exceed.** `sat_add`
   is a structural block (one comparator pair + mux), reused. Rationale:
   wrap in a dial reads as a sign flip — the room went from joyful to
   hostile because of an overflow; that failure mode is banned at the
   policy level, not debugged later.
3. **Truncate (floor) inside pipelines; convergent rounding
   (round-half-to-even) only at integrating boundaries.** Floor costs
   zero gates but biases −½ LSB/op; in an integrator (dial, S) that
   bias *accumulates* — a dial would random-walk downward at
   ½LSB·rate·t. Convergent rounding (`(x + halfLSB) & ~mask` with an
   lsb-fix xor) makes residual bias zero-mean. So: MAC pipelines floor;
   dial writeback, view outputs, and S→μ̂ normalization round.
4. **Multiplies full-width, one rescale.** s1.14 × s1.14 → Q2.28 →
   shift/round once to target. No intermediate truncations. Maps to
   one 18×18 signed DSP on fabric that has them; yosys maps to
   shift-add chains on fabric that doesn't (iCE40) — same source
   (§4).
5. **No division, no floats, no `real`, no `initial` in rtl/.**
   Reciprocal/reciprocal-sqrt via shared Newton–Raphson (seed from
   priority encoder, 2 iterations, documented residual). Square root
   same unit. Verilog-2005 `$ln`/`$sqrt` exist for **testbenches
   only** — golden models, not silicon.
6. **Integer state wherever the math allows.** W, age, N are integers
   precisely because integers don't drift. Fixed-point is used where
   it earns its keep (readings), refused where it would rot (state).
   This asymmetry is the deepest rule in the policy.
7. **Every LUT and approximation ships with a measured max-error
   assertion in its testbench** (ln-LUT ≤ 1.1e-3; κ̂ vs bisection ≤ 3%
   rel for ρ∈(0.1,0.95); NR reciprocal residual ≤ 1 LSB). "Verified or
   it doesn't exist" applies to error bounds too.

---

## 4. Distribution Story — same RTL, ICE40 → big fabric

**What stays generic (the entire semantic layer):** opcode decode,
ingress/egress contract, hebb/cos/vmf/dial datapaths, tick scheduler.
All widths (`DATA_W`, `ADDR_W`, `D`, `N_EDGE`, `N_LINK`, `N_DIAL`,
`DECAY_HORIZON`) and all depths are parameters. Memory is declared as
plain reg arrays and **inferred** (yosys picks BRAM, SPRAM, or LUTRAM
per target) — no vendor primitives anywhere, by the Law.

Three named configurations, zero source changes (parameter + top-level
instance count only):

| | `zc_cell_tiny` | `zc_cell_full` | `zc_array` |
|---|---|---|---|
| Fabric | iCE40 UP5K-class | ECP5-25k-class | big FPGA / multi-FPGA |
| D | 8 (dial bank) | 64 | 64/cell |
| Edges | 64, W/age in FF | 4096, rows in BRAM | BRAM + link router |
| vMF | shared, view-time | 1/cell, streaming | 1 per 8 cells |
| Links | 2 | 4 | mesh |
| Storage | FF/LUTRAM only | inferred BRAM | inferred BRAM |
| Est. area | ~2–3k LUT4 (honest: est., not measured) | ~8–12k | per-cell × mesh |

Scaling axes, explicitly:

- **Depth scales by memory inference** (edge table 64 → 4096 is a
  parameter; yosys moves it FF → BRAM with no source change).
- **Width scales by parameters** (D=8 → 64 changes MAC time-mux count,
  not code).
- **Throughput scales by instance count** (primitive banks are
  instantiable per-cell; the tiny fabric shares one vMF at view-time,
  the full fabric streams it per-sample — *identical module*,
  different arbitration, which is a parameterized mux, not a fork).
- **What does not scale for free** is honestly listed in §6.

Verification is config-orthogonal: every testbench takes the same
parameters and runs the same golden models at `zc_cell_tiny` and
`zc_cell_full` configs in CI (iverilog + verilator; yosys+nextpnr
synthesis smoke for iCE40/ECP5 as the open-tools proof — nextpnr is
open, not vendor).

The distribution claim rests on one discipline: **no module ever
learns a width.** The day a primitive special-cases D=8 is the day the
quilt forks, and a forked quilt is two quilts pretending to be one.

---

## 5. Testbench Plan (open tools only)

Every TB: self-checking, parameterized, `iverilog -g2005` +
`verilator --lint-only -Wall` clean; golden models use Verilog-2005
real math (`$ln`, `$sqrt`, `$pow`) — legal in testbenches.

| TB | What it proves | Method |
|---|---|---|
| `tb_zc_opcode_decode` | all 5 verbs decode; illegal ops trap-view; frame assembly | exhaustive opcode × framing vectors |
| `tb_zc_ingress_egress` | valid/ready contract: no drops, no comb loops, backpressure | randomized ready toggling, assertion: frames in = frames out, in order |
| `tb_zc_prim_hebb` | (a) potentiation + saturate at 65535; (b) **ln-LUT vs `$ln(1+W)` max error ≤ 1.1e-3 (exhaustive u16 too slow → stratified sweep + all W<1024 + dyadic boundary cases)**; (c) decay: decrement interval == `P₀>>2·msb(W)` exactly (deterministic check); (d) trajectory envelope: simulated W(t) vs golden hyperbola `W₀/(1+W₀t/P₀)`, assert within dyadic factor | golden real model + exhaustive-interval checks |
| `tb_zc_prim_cos` | dots vs real golden within 2 LSB after convergent round; normalize-once path: pre-normalized cos error ≤ 3 LSB | random unit vectors (normalized in real), D ∈ {8, 64} |
| `tb_zc_prim_vmf` | ρ/μ̂ within Q LSB of real golden; **κ̂ vs real bisection `A_d(κ)=ρ` (the contrast.py algorithm reimplemented in TB real math): rel error ≤ 3% for ρ∈(0.1,0.95), and *documented* degradation outside**; κ saturation flag | random vMF samples (real, via rejection), sweep ρ |
| `tb_zc_prim_dial` | saturation at ±1 (fuzz boundaries, no wrap possible — assert structurally + fuzz); attack/release rates; hyperbolic dial decay envelope | fuzz + golden |
| `tb_zc_math_lut` | NR reciprocal/sqrt residual ≤ 1 LSB over exponent sweep; ln LUT error bound | exhaustive-ish sweeps |
| `tb_zc_tick_sched` | effect FIFO drained in order (receipts sequenced); tick priority order; decay+dial step exactly once per edge/dial per tick | directed + random |
| `tb_zc_link_port` | no-drop under backpressure; reverse-edge (!type) recorded | randomized |
| `tb_zc_cell` (integration) | drive a scripted quilt session (bind/link/effect/view/tick mix) through ingress; egress receipts and views match a **behavioral golden quilt** (Verilog real model of the C semantics) | scenario files + random session fuzz |
| CI | lint + all TBs at `tiny` and `full` configs; yosys+nextpnr smoke for iCE40/ECP5 | make targets |

Stretch (honest, post-cross-review): SymbiYosys assertions on the
stream contract (one-hot ready/valid invariants). Not promised for v1.

---

## 6. Honest Failure Modes

In the elephant repo's culture: honesty notes in the code. Same here.

**What fixed-point breaks first:**

1. **Small-angle cosine.** cos θ ≈ 1 − θ²/2; resolving θ = 0.01 rad
   needs cos-error < 5e-5 — that is below 1 LSB of s1.14 (6.1e-5).
   Dial-space (D=8) comparisons are fine at fleet tolerances; embedding
  -scale "are these two rooms *exactly* aligned" questions are not.
   Fix is Q2.20 components (documented, parameterized) — costs area.
   v1 ships s1.14 and says so.
2. **κ̂ near ρ → 1.** Sra's form divides by (1−ρ²); ρ = 0.999 in u0.15
   is one LSB from the cliff. RTL saturates at κ_max and raises a
   clipped flag — a saturated κ must read as "very tight, beyond my
   resolution," never as a number to trust.
3. **ρ bias at small N / high D** (the √(N/d) floor). Silicon inherits
   the statistic's sin; the view exposes N alongside ρ so consumers
   can disbelieve correctly. No estimator magic offered.
4. **Truncation bias** — killed by policy where it would integrate
   (§3.3), but any future module that forgets the rule re-introduces
   drift. The policy is load-bearing; the cross-review should check
   every new adder against it.
5. **The power-law staircase** is an envelope, not pointwise truth:
   instantaneous decay rate is right within 2×, the trajectory is a
   staircase hugging the hyperbola. For memory-horizon semantics that
   is the right approximation; for anything that differentiates W(t)
   it is not. Documented in the TB, asserted as envelope-only.

**What doesn't fit small fabric:**

6. **Streaming vMF at D=64** on iCE40-class: the vector sum fits BRAM,
   but with no DSPs every s1.14 MAC is shift-add fabric; per-sample
   full-D MAC will not keep line rate. Honest answer: on tiny fabric
   the vMF is **view-time** (compute on demand), and per-sample vMF at
   D=64 is a full-fabric feature. D=8 (dial bank) streams fine
   everywhere.
7. **Cell-array CDC.** v1 is single-clock per cell; mesh links across
   domains are deferred. A same-clock mesh on one fabric is fine;
   multi-FPGA quilts wait.
8. **Effect-FIFO depth vs no-drop.** No-drop means stall-and-wait; a
   congested effect queue back-pressures the whole ingress. That is
   correct-by-doctrine (amnesia is worse than latency) but it makes
   the tiny fabric's throughput sensitive to effect storms. Depth is
   a parameter; the tradeoff is stated, not hidden.
9. **Area estimates in §4 are estimates.** The UP5K number is derived,
   not synthesized. First nextpnr run either confirms it or rewrites
   §4 — the README's law ("verified or it doesn't exist") applies to
   my own area claims, at cross-review.

**What I am explicitly not claiming:** that this is a JEPA backbone.
The dial bank is a latent space with JEPA-shaped interfaces — the same
qualification elephant v0 carries in its README ("hand-crafted keyword
heuristic with a JEPA-shaped interface; the learned backbone is a
stub"). What this entry claims is narrower and buildable: the
**field-reading** (dials, edges, vMF concentration) is real math,
already proven in the fleet's software, and it fits in fixed-point RTL
at the edge with the stream never stored. The learned part, when it
exists, inherits a socket: a normalized-latent ingress port and a view
port. The quilt keeps the chair warm.

---

## 7. What ZeroClaw Asks of the Cross-Review

1. Attack the decay counter: is `P₀ >> 2·msb(W)` the right
   silicon/faithfulness tradeoff vs a true multiplier-based Δt?
2. Attack s1.14 as the universal component format (vs Q2.20 default).
3. Attack no-drop effect semantics under storm (vs drop+receipt).
4. Check my area claims against the first nextpnr run.

The reading is the cheapest thing in the circuit. Let's build the
reading.
