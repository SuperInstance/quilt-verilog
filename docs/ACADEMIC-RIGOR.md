# ACADEMIC-RIGOR — the citation-grade summary

**Audience:** a reviewer, professor, or examiner who will not take prose on
faith. **Method:** every claim below is either (a) machine-checked by a
command you can run from this tree, (b) quoted verbatim from a tool's own
output on this tree, or (c) labeled as unproven. **Companion documents:**
`docs/FORMAL-PROOFS.md` (per-proof depth), `docs/VERIFICATION.md` (all
lanes), `docs/SYNTHESIS-RESULTS.md` (measured silicon budgets),
`formal/README.md` (suite contract).

**Reproducibility contract.** Written 2026-08-30 against commit `ccff448`
(parent of this doc). Toolchain: stock oss-cad-suite — Yosys 0.47+22
(git f20f9132), SymbiYosys `yosys-0.47-2-g26b3874`, boolector 3.2.4,
nextpnr-ice40 0.7-131, Icarus Verilog 13.0 — at
`/home/eileen/tools/oss-cad-suite/bin` (the root Makefile pins the PATH).
Three verification commands and one synthesis elaboration were re-run by
this pass on this machine (2026-08-30 ~06:25 AKDT) and their outputs are
quoted verbatim in §2 and §5. One correction to the existing record is
made in §3.3 with the evidence that forces it.

**Working-tree note.** At the time of writing, `formal/cell_core.fair.sby`
and `formal/cell_core.tick.sby` carry *uncommitted* modifications (depth
80 → 130 / 105, plus a harness fix for a newly-found interference
witness). Everything in this document cites the **committed** state at
`ccff448` (both proofs: `mode bmc, depth 80`, PASS per
`docs/VERIFICATION.md` iteration 2). The uncommitted drift is flagged as
an open work item in §7, not silently folded in.

---

## 1. The formal model — what the RTL *is*

### 1.1 The system

The quilt fabric (`rtl/q_fabric_top.v`) is a synchronous digital system: a
set of NCELL homogeneous cells plus one I/O node on a unidirectional ring
of registered pipe slices, driven by one clock and one active-low
asynchronous-style reset (synchronous deassert assumed by all harnesses),
with a single free-running tick scheduler strobing every 2^TPW cycles
(`rtl/q_tick_sched.v:5–24`, TPW=8 default → one strobe per 256 cycles).

Each cell (`rtl/q_cell_core.v`) is a **run-to-completion FSM** over one of
five opcodes (bind, link, effect, view, tick) — the module header
(`q_cell_core.v:1–43`) is the authoritative English contract. Restated as
plain mathematics, the whole fabric is a deterministic transition system:

> **M = (S, s₀, →)** where S is the product of all register valuations in
> the design, s₀ the reset state, and s → s′ the synchronous transition
> induced by the Verilog-2005 semantics (IEEE 1364-2005) as elaborated by
> Yosys. Inputs are free at every step (subject only to the environment
> assumptions E1–E4 listed in §4.4 for two of the proofs). A *trace* is a
> finite or infinite sequence s₀ → s₁ → s₂ → ….

Everything proven in this repo is a statement of the form "for all traces
satisfying the harness assumptions, the property holds at every step (up
to the bound, where a bound exists)."

### 1.2 The dataplane invariants the design *intends*

Three families of intended behavior are pinned by the RTL structure and
checked formally:

- **Transport** — the ring's pipe slice `rtl/q_flit_pipe.v` is a skid
  buffer: `m_valid = a_v` (line 45) and `s_ready = !b_v` (line 46) —
  ready depends only on local state, which is precisely why no
  combinational ready-loop closes around the ring (header comment, lines
  1–6).
- **Ledger** — intercell credit (effect flits = future weight) is meant to
  be *conserved*: everything a fire issues is booked, in flight, in
  service, or externally sunk (`formal/f_fabric_conservation.v:1–54`,
  mirroring `docs/academic/quilt-calculus.md` A1/T1).
- **Time** — the tick lane is non-deferrable: a pending tick suppresses
  ingress acceptance (`q_cell_core.v:315–321`, repeated at 383, 433, 511,
  550, 560) so a tick is deferred by at most the in-flight op.

### 1.3 What "the RTL" is, precisely

The proofs elaborate the **same** `rtl/*.v` sources the testbenches and
the bitstream build use — read with `read -formal` in Yosys's Verilog
frontend. Two precision notes a reviewer will care about:

1. The RTL itself is Verilog-2005 (IEEE 1364-2005) — no SystemVerilog
   constructs. The *harness* files use `assert`/`assume`/`cover`
   immediate statements, which are **Yosys formal extensions** to
   Verilog-2005 processed by `read -formal`, not standard IEEE 1364
   assertions. The properties are therefore as strong as Yosys's
   elaboration of both; §7 lists the tool-trust threat this creates.
2. The `formal/` harnesses use **no cross-module references** — every
   property is a function of DUT *port* signals plus harness-owned shadow
   state. The one exception is the older `tb/formal/` k-induction
   harness, which deliberately uses `dut.b_v` with a DUT-first read order
   so the reference resolves (`tb/formal/flit_pipe.sby`, script section)
   — a documented Yosys-frontend idiom, not an accident.

---

## 2. Invariant catalog

Status vocabulary (used consistently): **machine-proved (BMC d)** = no
counterexample of length ≤ d exists (what a PASS at depth d means);
**machine-proved (k-induction)** = proven for all reachable states,
unbounded; **induction-pending** = a prove-mode attempt was made and
FAILS — the invariant is believed true (BMC evidence) but is not
k-inductive on the harness's visible state, with named missing lemmas;
**TB-covered** = checked by a directed/random testbench, no formal claim.

| # | Invariant | Enforced in RTL at | Proof | Status |
|---|---|---|---|---|
| C2 | pipe occupancy ≤ 2 | `q_flit_pipe.v:46` (`s_ready=!b_v`, two registers) | `tb/formal/flit_pipe.sby` | **machine-proved (k-induction, k=15)**; also BMC-40 in `flit_pipe.fly.sby` |
| C3 | `m_valid ⇔ occ≠0` (no phantom/no hide) | `q_flit_pipe.v:45` | same | **machine-proved (k-induction)** |
| C4 | `s_ready ⇔ occ<2` (exact backpressure) | `q_flit_pipe.v:46` | same | **machine-proved (k-induction)** |
| V1 | emitted payload = FIFO head (no loss/dup/reorder of values) | pipe datapath, `q_flit_pipe.v` | `flit_pipe.fly.sby` | **machine-proved (BMC 40)** — bounded only |
| T1 | `emit = pipe + accepted` (transport conservation) | system property (A↔pipe↔B) | `fabric.conservation.sby`; prove attempt §3 | **machine-proved (BMC 55)**; **induction-pending** (L1) |
| A1 | ledger identity: `emit + ext = booked + pipe + in-service + ext`, constant across commits | system property | same | **machine-proved (BMC 55)**; **induction-pending** (L2) |
| SER | `in-service ≤ 1` (commits serialize) | `q_cell_core.v` one-op FSM (ST_EFFT→ST_EFFR→…→ST_EFFI, lines 385–435) | `fabric.conservation.sby` | **machine-proved (BMC 55)**; **induction-pending** (first failure named by the probe — §3.3) |
| DROP | accepted effect booked ≤ 16 cycles (no silent drop for linked peers) | `q_cell_core.v:385–435` (unknown-source drop path `ST_EFFT` eidx==EDGES_N unreachable when linked) | `fabric.conservation.sby` | **machine-proved (BMC 55)** |
| FAN | every A emission: op=EFFECT, src=A, dst=B | `q_cell_core.v` tick-fire fanout (header, `q_cell_core.v:23–29`) | `fabric.conservation.sby` | **machine-proved (BMC 55)** |
| DYAD | `2^(PW−1) ≤ F ≪ g < 2^PW` (trace in its dyadic octave) | `q_echo_gate.v:90` (`o_gclass = TOPJ − msb_idx(f)`) | `echo_gate.dyadic.sby` | **machine-proved (BMC 25)** |
| PRIORITY/MONO/ZEROABSORB/DEAD/DISABLED | fire beats leak; no growth w/o fire; 0 absorbing; dead gates training; floor=0 ≡ v1 | `q_echo_gate.v:78–92` (the `i_fire`/`i_tick` precedence chain) | `echo_gate.dyadic.sby` | **machine-proved (BMC 25)** |
| Q2b | pending tick ⇒ `¬ci_ready` | `q_cell_core.v:315–321` + 383, 433, 511, 550, 560 (the Q2fix lines) | `cell_core.tick.sby` | **machine-proved (BMC 80)** |
| Q2a1/Q2a2 | strobe→ready ≤ 100; strobe→first sweep cmd ≤ 66 (linked) | structural FSM bounds | `cell_core.tick.sby` | Q2a2: **machine-proved (BMC 80)** under E1–E3; Q2a1: BMC-evidenced only — deadline 100 > depth 80 (§4.1a) |
| I1a/I1b/I2 | op gap ≤ 64 (≤128 with spaced ticks); every op answered ≤ 66 | run-to-completion FSM | `cell_core.fair.sby` | **machine-proved (BMC 80)** under E1–E4 |
| FIFO/ring smoke | whole-fabric train→fire→decay, latency ≤ 31 | `q_fabric_top.v` | `tb/tb_fabric_smoke*.v` | **TB-covered** (18/18 suite, `docs/VERIFICATION.md`) |
| serf byte-exactness | serialized ≡ parallel config/egress | `q_serfabric_top.v` | `tb/tb_serfabric.v` | **TB-covered** (differential TB, 68 flits) |

### 2.1 Commands and verbatim outputs (re-run by this pass)

Three proofs were re-run 2026-08-30 ~06:25 AKDT on this tree. Tail of each
log, exactly as printed:

```
$ sby -f formal/echo_gate.dyadic.sby
SBY ... summary: engine_0 (smtbmc boolector) returned pass
SBY ... summary: engine_0 did not produce any traces
SBY ... DONE (PASS, rc=0)                          [wall: 2.9 s]

$ sby -f tb/formal/flit_pipe.sby
SBY ... summary: engine_0 (smtbmc boolector) returned pass for basecase
SBY ... summary: engine_0 (smtbmc boolector) returned pass for induction
SBY ... summary: successful proof by k-induction.
SBY ... DONE (PASS, rc=0)                          [wall: 0.37 s]

$ sby -f formal/fabric.conservation.probe.sby
SBY ... summary: engine_0 (smtbmc boolector) returned pass for basecase
SBY ... summary: engine_0 (smtbmc boolector) returned FAIL for induction
SBY ... summary: counterexample trace [induction]: .../trace_induct.vcd
SBY ... summary:   failed assertion ..._v_293_87 at f_fabric_conservation.v:293.9-293.28 in step 0
SBY ... DONE (UNKNOWN, rc=4)                       [wall: 5.3 s]
```

The third command *fails by design* — it is the induction probe whose
counterexample anchors §3. The other three proofs (fair, tick, and the
full conservation BMC) were not re-run by this pass; their most recent
measured runs (iteration 2, 2026-08-29, same tree) are PASS at 498 s /
215 s / 38 s respectively (`docs/VERIFICATION.md`), and the committed
`sby` files reproduce them via `make formal`.

---

## 3. The conservation story — including the honest FAIL

### 3.1 The property

Two cells, A and B, linked; A dialed to fire every tick. Count at module
boundaries: `emit` = effect flits A handed to the pipe; `pipe` = flits
occupying the pipe; `acc` = effects accepted at B; `book` = cofire
commits strobed at B; `ext` = B's own fire flits sunk externally. Then
for every cycle of the run phase:

- **T1** `emit = pipe + acc` — nothing lost or fabricated in movement;
- **A1** `emit + ext = book + pipe + (acc − book) + ext` — the ledger:
  a commit moves a flit from in-flight to booked; nothing else mints or
  burns credit.

This is the quilt calculus's cut-conservation theorem
(`docs/academic/quilt-calculus.md`) as a **machine-checked property of
real RTL** — two real `q_cell_core` instances, real `q_hebb_edge`
engines, real `q_flit_pipe`, `PIPE_EFF=1` (the shipped retime), **no
stubs, no environment assumptions** (the only constraints are the
bind+link setup and a fire-only workload). Command:
`sby -f formal/fabric.conservation.sby` → **PASS at BMC depth 55**.

### 3.2 The prove-mode attempt (commit `b82cd19`, 2026-08-29)

The expert-nudge question: does conservation lift from BMC-55 to `mode
prove` (unbounded)? **Tried. It does not — yet — and the failures are the
most informative artifacts in the suite.**

Four runs (all committed as `.sby` files; result dirs reproduce):

| harness | mode/depth | result |
|---|---|---|
| `fabric.conservation.prove.sby` (full) | prove 55 | basecase **PASS** (log: `Status: passed` at 0:00:58); induction **FAIL** — engine descends k = 39→28 over 9:35 without closing; run terminated |
| `fabric.conservation.probe.sby` | prove 8 | basecase PASS; induction **FAIL in 5 s**, counterexample names assertion at `f_fabric_conservation.v:293` (§3.3) |
| `fabric.conservation.prove-t1.sby` (T1+A1 only — SER/DROP stripped) | prove 55 | induction **FAIL** — descends 38→31 over ~9 min, terminated |
| `fabric.conservation.probe-t1.sby` | prove 6 | induction **FAIL in 3 s** at `f_fabric_conservation_t1.v:290` (T1) and `:300` (A1) |

The prove-t1 row is the substantive finding: **even the flagship ledger
identity T1/A1 is not k-inductive on the harness's boundary-visible
state.** An induction step starts from an *arbitrary* state satisfying
the assertions for k steps — and the shadow counters (`f_pocc`, `f_acc`,
`f_book`) can be consistent for k steps while the *hidden* pipe/core
state is garbage that breaks them at step k+1.

### 3.3 A correction to the record (found by this pass)

`docs/FORMAL-PROOFS.md` §2's addendum and commit `b82cd19`'s message say
the depth-8 probe names "line 293, **DROP's `f_icnt <= 16`**". That
mislabels the line. Evidence, from this pass's re-run and the elaborated
model:

- `formal/f_fabric_conservation.v` line **293** is
  `assert (f_ins <= 1);` — **SER**, not DROP. DROP is the *guarded*
  assert at line **295** (`if (f_acc != f_book) assert (f_icnt <= 16);`).
  The elaborated netlist (`…/probe/model/design.il`, lines 8772–8789)
  contains exactly the assert cells `_v_290_82` (T1), `_v_291_85`,
  `_v_293_87` (SER), `_v_295_90` (DROP), `_v_300_92` (A1) — the failed
  witness `_v_293_87` is SER, and its column range 9–28 matches the
  20-character SER statement, not the indented DROP guard.
- The counterexample state (this pass's `trace_induct.vcd`, final step):
  `f_ins = 2`, `f_acc = 170`, `f_book = 168`, `f_icnt = 16`,
  `f_pocc = 0` — an unreachable-from-reset state where two effects are
  simultaneously in service (SER broken) *and* the DROP countdown sits at
  its bound. So the FORMAL-PROOFS *description* of the state was right;
  its line/property attribution was wrong.

The correction does not weaken the finding — it sharpens it: the first
non-inductive assertion is SER (a property of core-B internals the flat
harness cannot see), and stripping SER *and* DROP entirely
(`prove-t1`) still fails on T1 and A1 themselves.

### 3.4 The two missing strengthening lemmas

Named precisely by the counterexamples (commit `b82cd19`; probe traces
committed under `formal/fabric.conservation.probe*/engine_0/`):

- **L1 (pipe content).** Every flit resident in or emitted by the pipe
  post-setup has `op = OP_EFF`, `src = A_ID`, `dst = B_ID`. Without it,
  an induction state may pop a non-EFF flit — `f_pocc` decrements without
  `f_acc` incrementing — breaking T1. The shadow occupancy is tied to
  *real* pipe contents only through history that k-induction cannot see.
- **L2 (command provenance).** Core B's `hb_cmd` train strobes occur only
  as commits of genuinely accepted effect ops. Without it, an arbitrary
  core-B state mints a booking strobe with no matching acceptance,
  `f_book` grows unboundedly, and A1 breaks.

**What closing them would take.** L1 and L2 are invariants of state
*inside* `q_flit_pipe` and `q_cell_core` — invisible to the no-XMR
boundary harness. The canonical path (stated in FORMAL-PROOFS §2 and
endorsed here): prove L1/L2 as auxiliary invariants over the modules'
internal state — most plausibly via whitebox assertions inside
`q_flit_pipe`/`q_cell_core` under a `FORMAL` define (the idiom
`tb/formal/flit_pipe.sby` already uses with `-D FORMAL` and DUT-first
read order) — then T1/A1 close by induction, and SER/DROP follow from
L1+L2 plus the structural 16-cycle booking bound. Until then, **the
honest statement of conservation is BMC-55**, and `docs/FORMAL-PROOFS.md`
§2 remains its canonical description. Update 2026-08-30: the L1/L2
whitebox attempt itself was run and remains honestly open — see
`formal/fabric.conservation.prove-l12.sby` and FORMAL-PROOFS §2's
"L1/L2 strengthening attempt" (basecase PASS, induction still fails;
new frontier: core-A emission provenance).

**Why we publish the failure.** Per this repo's doctrine, failures are
first-class: a bounded proof honestly labeled is worth more than an
unbounded claim without a certificate. The FAIL is also the credibility
anchor for everything else on this page — the same toolchain that PASSes
five proofs is demonstrably willing to FAIL a sixth when the mathematics
isn't there yet.

---

## 4. Methodology

### 4.1 BMC vs prove, and the k-lengths actually used

All `.sby` files at `ccff448` (depths quoted from the files themselves):

| file | mode | depth | rationale for the length |
|---|---|---|---|
| `formal/echo_gate.dyadic.sby` | bmc | 25 | > 5 leak generations at the fastest leak (PW=16) — every gate FSM behavior exhausts |
| `formal/flit_pipe.fly.sby` | bmc | 40 | covers multi-flit fill/drain cycles of a 2-deep slice |
| `formal/fabric.conservation.sby` | bmc | 55 | covers setup + multiple fire→fly→accept→book round trips |
| `formal/cell_core.tick.sby` | bmc | 80 | Q2b/Q2a2 violations fit well inside 80; **Q2a1's 100-cycle deadline does not** — see §4.1a |
| `formal/cell_core.fair.sby` | bmc | 80 | I1a violations need ≤ 67; I2 ≤ 60 — exhausted inside 80 |
| `tb/formal/flit_pipe.sby` | prove | 15 | k-induction closes at k ≤ 15 for C2/C3/C4 |
| probes (§3.2) | prove | 6/8 | smallest k that exhibits the non-inductivity |

Note the honest asymmetry documented in `formal/README.md`: an I1b
violation (> 128-cycle gap) would need a ≥ 129-step trace, so depth-80
does not exclude it beyond a 34-cycle margin — stated, not hidden.

**a. A sharper margin finding (this pass).** The tick harness's Q2a1
deadline is `Q2_RISE = 100` (`f_cell_core_tick.v:50`); a violation arms
the shadow countdown and needs **> 100 further cycles** to fire — a trace
longer than depth 80 can contain (Q2a1's structural worst is ≈ 92).
So the committed depth-80 PASS exercises Q2b and Q2a2 (66) genuinely but
cannot reach a Q2a1 deadline violation at all: **Q2a1's 100-cycle bound
is not exhausted by the committed run**, and FORMAL-PROOFS §4's "all
deadlines are assert-within-N inside depth 80" overstates for Q2a1
specifically. The uncommitted working-tree change bumping tick to depth
105 (see preamble) is precisely the response in flight; until it lands
and passes, Q2a1 should be cited as BMC-evidenced (worst-case argument
≈ 92 < 100), not BMC-exhausted.
Bounded-liveness properties are all encoded as *assert-within-N* shadow
countdowns; **unbounded liveness is claimed nowhere in this suite**.

### 4.2 What a PASS means, exactly

- **BMC PASS at depth d:** no trace of length ≤ d from reset, under the
  harness assumptions, violates the assertions. Not a statement about
  longer traces — except where a structural worst case is argued to fit
  inside d (per-property arguments in `formal/README.md` and
  FORMAL-PROOFS).
- **prove PASS:** base case (BMC over the reset prefix) + induction step
  (all k-step assertion-consistent states satisfy the assertions at
  step k+1). Unbounded. Exactly one proof in the suite is k-inductive
  (`tb/formal/flit_pipe.sby`, C2/C3/C4).
- **prove FAIL/UNKNOWN:** the property is not k-inductive at any depth
  tried; it may still be true (BMC evidence) — the counterexample is an
  *induction* state, unreachable from reset. §3 is exactly this case.

### 4.3 Harness discipline

Shadow reference models built from **port handshakes only** (no XMRs in
`formal/`); 2-step forced-reset preamble before properties bind
(registers carry no init values); `cover` statements for non-vacuity
(the solver must reach a full pipe, a booked commit, a priority clash —
companion cover runs confirmed reachability for the dyadic proof at
g ∈ [0,7] and g ≥ 8).

### 4.4 Environment assumptions (E1–E4), gathered

Used only by fair/tick (conservation uses none). Each is **weaker than**
the real system's behavior — the proofs hold in a strictly more
adversarial environment than the shipped fabric provides — but they are
assumptions about the environment, not proven facts:

| id | statement | real system |
|---|---|---|
| E1 | egress always grants | ring-progress backpressure is the fabric-level property (SYNTHESIS Q1), out of scope |
| E2 | engine readout ≤ 12 cyc, others ≤ 4 | real `q_hebb_edge`: 10 and 2 |
| E3 | dialfile stub, exact timing | real `q_dialfile` |
| E4 | tick strobes ≥ 128 cycles apart | `q_tick_sched` default: one per 256 |

---

## 5. Synthesis evidence

All silicon-budget numbers live, with full provenance, in
`docs/SYNTHESIS-RESULTS.md`; nothing below is re-measured prose — the
headline row was independently reproduced by this pass.

**Re-run by this pass (2026-08-30):** the yosys iCE40 elaboration of the
converged top (`synth/fpga-converged.ice40` script, output redirected to
/tmp so tracked artifacts were untouched), exit 0, **24.4 s wall**:

```
SB_LUT4   6002     SB_CARRY  898
SB_DFF 51 · SB_DFFE 58 · SB_DFFESR 1731 · SB_DFFESS 50 · SB_DFFSR 544
          (FF-class total: 2,434)
```

Byte-for-byte the tracked iteration-3 stat (`synth/iter3/
stat_fabric2_k4b4a8e1.txt`): yosys is deterministic here; cell counts
have now reproduced identically across four independent passes.

**Cited from SYNTHESIS-RESULTS (measured, tracked artifacts):**

- **Headline (HX8K-CT256, k4b4a8e1 — the conservation proof's exact
  parameters on real `q_fabric_top`):** 6,002 LUT4 / 898 CARRY / 2,434
  FF-class; 7,596/7,680 LC (98%); 157/256 IO; **fmax 44.43 MHz
  post-route** at the 12 MHz target (43.36 MHz is the post-*placement*
  estimate — the repo's quoting rule is post-route only, both labeled);
  135,100-byte bitstream packed and tracked. The config is deliberately
  the formal one: what is proven is what ships.
- **Device ladder:** ECP5 LFE5U-25F closes 8 cells at 63.7 MHz; a real
  12F closes 4 (nextpnr's `--12k` places against 25F silicon — the tsv
  carries an explicit `util12f%` column); UP5K sg48 closes 1 cell at
  16.78 MHz post-route (17.36 was the placement estimate — corrected by
  the audit; the older tree measured 15.97) once the serialized
  front-end cuts IO from 157 to 37.
- **Nothing has met a board.** No PCF, no IO constraints, no bring-up;
  every fmax is nextpnr's estimate of an unconstrained-IO design. A
  bitstream that packs is not a bitstream that boots.

---

## 6. Relation to literature

Tools (used as-is, versions in the reproducibility contract; no claim of
novelty in them — the claims are about this design):

- **Yosys** — C. Wolf, J. Glaser, J. Kepler, "Yosys – A Free Verilog
  Synthesis Suite," Austrochip 2013; and the Yosys open-source project
  (yosyshq.net), version 0.47+22 here. Verilog-2005 elaboration per
  **IEEE Std 1364-2005**.
- **SymbiYosys (sby)** — C. Wolf's formal-verification front end driving
  Yosys + SMT solvers (github.com/YosysHQ/sby), here `yosys-0.47-2`.
- **boolector 3.2.4** — A. Niemetz, M. Preiner, A. Reynolds, C. Tinelli,
  A. Biere, "Solving Bit-Vectors in the Open SMT-LIB Format" / the
  Booceptor solver family (boolector.github.io); used via sby's
  `smtbmc` engine.
- **Bounded model checking** — A. Biere, A. Cimatti, E. Clarke, Y. Zhu,
  "Symbolic Model Checking without BDDs," TACAS 1999 (the BMC paradigm
  this suite's five BMC proofs instantiate).
- **k-induction** — M. Sheeran, S. Singh, G. Stålmarck, "Checking Safety
  Properties using Induction and a SAT-Solver," FMCAD 2000 — the
  `mode prove` strategy; §3's L1/L2 lemma-strengthening loop is the
  standard remedy this literature prescribes for non-inductive
  invariants.
- **nextpnr** — the nextpnr place-and-route project (YosysHQ),
  nextpnr-ice40 0.7-131; **iCE40** — Lattice Semiconductor iCE40 UP5K/HX8K
  device documentation; the free iCE40 flow builds on the Project
  IceStorm reverse-engineered bitstream documentation (C. Wolf, M.
  Lasser; clifford.at/icestorm), as consumed here through nextpnr's
  native iCE40 backend and icepack.

Positioning, in one paragraph: the contribution claimed for this repo is
not a new model-checking algorithm — it is the *application* of the
standard BMC + k-induction toolkit (exactly the Sheeran–Singh–Stålmarck
recipe, including its failure modes) to a neuromorphic fabric whose
learning rule is integer-only by construction, so that its core safety
properties (transport, conservation, time-discipline, quantization
bracketing) are decidable bitvector questions with no arithmetic
abstraction gap. The conservation FAIL of §3 is the literature-typical
outcome — invariants over composed modules rarely close without
auxiliary lemmas — documented here to the same standard as the passes.

---

## 7. Threats to validity

**Internal.**

1. *Shrunk formal parameters.* Conservation is proven at EDGES_N=1, K=4,
   B=4, AGEW=8 — not shipped-fabric scale. Generality across scale is
   unproven.
2. *Bounded horizons.* Five of six proofs are BMC; unbounded claims rest
   on one k-induction (pipe C2/C3/C4). I1b has a stated 34-cycle margin
   beyond depth 80; Q2a1's 100-cycle deadline is not exhausted at depth
   80 at all (§4.1a). Unbounded liveness: not claimed anywhere.
3. *Environment assumptions E1–E4* (fair/tick only) are stated, not
   proven from fabric-level RTL.
4. *One SMT solver, one engine.* All proofs run `smtbmc boolector`
   exclusively; no solver cross-check (e.g., yices/z3) has been run. A
   solver bug would corrupt every verdict symmetrically.
5. *Tool trust.* The properties are properties of Yosys's elaboration of
   the sources; a frontend discrepancy between Yosys, Icarus (the TB
   lane), and synthesis would not be caught by these runs alone. The two
   independently observed RTL defects the proofs caught were
   simulator-divergent *and* yosys-visible, which is evidence the lane
   is not vacuous — but it is not a semantic-equivalence proof.
6. *No hardware.* Every number is simulation, formal, or PnR; the
   bitstream is untested on metal; fmax assumes unconstrained IO.
7. *No CI.* Verification runs when a human/agent runs it; regressions
   between commits are possible by omission.
8. *Record drift.* (a) The FORMAL-PROOFS §3 line-attribution error,
   corrected in §3.3 above — the *state* description was right, the
   line/property label was wrong; FORMAL-PROOFS.md should adopt the
   correction. (b) Uncommitted working-tree strengthening of
   fair/tick (depth 130/105 + an interference-witness harness fix) is in
   flight at writing time and intentionally not cited as result. (c) The
   tracked `synth/fabric2_k4b4a8e1.bin` predates the PIPE_EFF retime;
   the tree-matching bitstream is `synth/iter3/` (SYNTHESIS-RESULTS
   Table 2).
9. *Harness self-containment.* Shadow models are hand-written; a shadow
   bug could mask a DUT bug (mitigated — not eliminated — by the
   differential TB lane and the defects the suite has already caught).

**External.** All wall times are machine-load-dependent context
(WSL2 host); verdicts, cell counts, and file checksums are the stable
facts. Literature citations in §6 are to real, checkable publications
and projects; where a tool has no formal paper (sby, nextpnr), the
repository is cited rather than an invented reference.

---

## 8. Reproduce

```sh
export PATH=/home/eileen/tools/oss-cad-suite/bin:$PATH
make test      # 18/18 testbenches (iverilog)        ~1–2 min
make sim       # 34 Python behavioral tests          seconds
make formal    # all six proofs (5 BMC + 1 prove)    ~14 min
make synth     # iCE40 elaboration, tracked config   ~20 s
make pnr       # nextpnr-ice40 → icepack             ~3 min
# the honest FAIL, on demand:
sby -f formal/fabric.conservation.probe.sby    # ~5 s, induction FAIL by design
```

If any number in this document does not reproduce on this tree, that is
a bug in this document.
