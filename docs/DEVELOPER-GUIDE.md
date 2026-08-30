# DEVELOPER-GUIDE — working on the quilt, in this repo

Who this is for: you are about to change Verilog in `rtl/`, add a
testbench, or wire a new module into the fabric. This guide is the
practical map — architecture, module-by-module contracts, the boot path,
the conventions this tree actually follows, the flows with their real
output, a walkthrough for adding a module, and a debug playbook. Every
claim cites `file:line` or a measured run from this tree. Where something
is *not* proven, it says so (see also `docs/VERIFICATION.md`, "What is
NOT covered").

Companions: `README.md` (The Law), `docs/THE-TICK.md` (one tick traced),
`docs/QUF-SPEC.md` (the container), `formal/README.md` +
`docs/FORMAL-PROOFS.md` (the six proofs), `docs/VERIFICATION.md` (all
lanes, honest gaps).

---

## 1. Architecture in one screen

The quilt is a ring of cells. A **cell** is the only interpreter of the
five quilt opcodes; the fabric is wiring, not scheduling (DOCTRINE item 4).

```
                ┌──────────────────────── q_fabric_top / q_serfabric_top ────────────────────────┐
                │                                                                              │
  external ──▶  q_io_port (ring node EXTID) ──▶ q_flit_pipe ──▶ q_cell 0 ──▶ q_flit_pipe ──▶ …   │
  stream        (deliver/transit/inject)                        (q_cell N-1)         │ (ring     │
                ◀────────────────── one q_flit_pipe between every node ◀────────────┘  closes)   │
                │                                                                              │
                │   q_tick_sched (or q_tick_sched_rt after boot) ── s_tick ──▶ every cell       │
                └──────────────────────────────────────────────────────────────────────────────┘

  one q_cell =  q_link_ringport ─▶ [ingress q_flit_pipe] ─▶ q_cell_core ─▶ [egress q_flit_pipe] ─▶ ringport
                                             │                  │    │
                                             │        q_dialfile │    └─ q_echo_gate + q_rqh_bank (v2)
                                             └───────────────────┴──── EDGES_N × q_hebb_edge
```

- **The flit** is the universal word: `{op[2:0], src[3:0], dst[3:0],
  a0, a1, a2, dat}` = 75 bits at the default widths (frame layout spelled
  out in `rtl/q_serfabric_top.v:30`–31). Every link, pipe, and port
  carries it.
- **The opcodes** are BIND=0, LINK=1, EFFECT=2, VIEW=3, TICK=4, plus the
  response codes ACK=5 / NAK=6 (`rtl/q_cell_core.v:125`–127). Only
  `q_cell_core` interprets them.
- **Cells decompose** into core (FSM + activation), dial file (16 runtime
  registers = the cell's knobs), and a fixed array of Hebbian edge
  engines (weights that learn). The v2 pair — echo gate + RQH residue
  bank — wraps the edges without touching them.
- **Time** is the tick: a one-cycle strobe every `2^TPW` clocks
  (`rtl/q_tick_sched.v:2`–3). Ticks are non-deferrable at the cell: the
  core services a pending tick *before* accepting new ingress
  (`rtl/q_cell_core.v:314`–318).
- **The pin-count escape hatch** is `q_serfabric_top`: the same fabric
  behind an 8-bit byte port (37 IO instead of 157; header measurement in
  `rtl/q_serfabric_top.v:8`–12), because the parallel fabric "does not
  fit a 48-pin package" at even one cell.

Why each piece exists is the through-line of §3: **every module has a
REASON** — usually a measured failure it prevents. The repo's culture
(shipwright doctrine) is that comments record the casualty that motivated
the code; when you touch that code, you inherit the casualty.

### Version markers you will see in headers

- **v1** — the base fabric: opcodes, ring, ladder/hyperbola edges, QUF.
- **v2** — the judge's must-ship pair folded in: `q_echo_gate`
  (call–response credit for learning) + `q_rqh_bank` (graded-placement
  residue), both default-OFF = bit-exact v1 (`rtl/q_dialfile.v:67`–75).
- **v2.1** — two lanes: `PIPE_EFF` (3-stage effect-pipeline retime,
  `rtl/q_cell_core.v:45`–48) and the pin-fix lane (`quf_boot`,
  `q_boot_gate`, `q_tick_sched_rt`, `q_serfabric_top`).

---

## 2. The ring: pipes, ports, and the discipline that keeps it alive

Three small modules carry all traffic. Get their invariants right or
nothing above them is trustworthy.

### q_flit_pipe (`rtl/q_flit_pipe.v`, 75 lines)
Registered 2-deep skid slice. **Why skid:** the naive 1-deep form's
`s_ready = !vq || m_ready` closes a combinational ready loop around a
full ring (verilator UNOPTFLAT *and* a real hazard); the skid form's
`s_ready = !b_v` depends only on local state (`rtl/q_flit_pipe.v:46`).
**Rule for new modules:** a `*_ready` output must never be a function of
a downstream ready. Proven an ideal 2-deep FIFO (no loss/dup/reorder) by
`formal/flit_pipe.fly.sby` (BMC 40) and k-inductively by
`tb/formal/flit_pipe.sby` (prove, depth 15).

### q_link_ringport (`rtl/q_link_ringport.v`, 80 lines)
Pure-combinational ring node: **deliver** (dst == myid), **transit**,
**inject** (local flit enters a bubble freed by delivery). No registers —
timing closure is the pipes' job (`rtl/q_link_ringport.v:1`–4).
Liveness: transit never blocks unless downstream blocks.

### q_io_port (`rtl/q_io_port.v`, 71 lines)
"A ring node whose id is EXTID" — Law 4 (any IO enters as a cell peer).
Thin and dumb by law: external ingress is ring inject, external egress is
ring deliver (`rtl/q_io_port.v:1`–5). Devices plug into the same contract
cells speak; the fabric cannot tell the difference.

### Fabric tops
- **q_fabric_top** (`rtl/q_fabric_top.v:4`): `NCELL` cells + one io node
  (`NB = NCELL+1`, `:41`) on a single ring, one pipe between every node,
  one `q_tick_sched`. This is the top that synthesizes and goes through
  PnR (§6).
- **q_serfabric_top** (`rtl/q_serfabric_top.v:62`): the same ring, a
  boot lane (`quf_boot` or `q_boot_gate`), a byte deserializer/serializer
  front-end, and `q_tick_sched_rt`. Its ring "mirrors q_fabric_top
  EXACTLY … so the differential TB is comparing like with like"
  (`rtl/q_serfabric_top.v:47`–49). Proven byte/cycle-exact against the
  parallel path by `tb/tb_serfabric.v` (68 flits, cycle-locked).

---

## 3. Module-by-module: interface, invariants, reason

Format: **module** — what it does; the invariants you must not break; why
it exists. Line refs point at the current tree.

### 3.1 q_tick_sched (`rtl/q_tick_sched.v`, 24 lines)
Free-running strobe every `2^TPW` cycles (`:2`–3, module `:5`). Reason: v1's
single-clock epoch reference — Q2's deadline semantics need a stable
timebase (docs/SYNTHESIS.md Q2). Default TPW=8 → one tick per 256 clocks.

### 3.2 q_tick_sched_rt (`rtl/q_tick_sched_rt.v`, 57 lines)
Same strobe with a **runtime** period exponent latched once at the epoch
pulse (`:8`–12). Cycle-exactness contract: after the epoch pulse it is
cycle-identical to `q_tick_sched` at the same exponent — the load-bearing
detail is the epoch branch loading `cnt<=1, tick<=1` ("one free posedge
already elapsed", `:18`; the epoch branch `:45`–49). Reason: QUF's ticks section carries the
period; latch-once keeps the epoch stable by construction (changing
cadence mid-run is "refused by construction", `quf_boot.v:37`–38).

### 3.3 q_dialfile (`rtl/q_dialfile.v`, 104 lines)
16×16-bit runtime register file, one sync write port (bind), one sync
read port (view). Map (`:42`–44): 0 ETA_F, 1 ETA_S, 2 KF, 3 KS, 4 KA,
5 THRESH, 6 REFR, 7 COS_MIN, 8 P0E, 9 MODE, 10 HL, 11 KLE, 12 FLOOR,
13 FTRACE (read-only probe alias), 14 RQ (bit15=RQEN, [3:0]=QDW),
15 RQL. Invariants: reset loads defaults, no `initial` blocks; dial 13
writes are ignored (nothing to clobber, `:77`–80). Reasons: runtime
tunability without resynthesis; defaults keep v2 features OFF so v1
semantics are the reset state (`:66`–75) — THRESH resets to 0.75
(`:58`), FLOOR to 0.

### 3.4 q_hebb_edge (`rtl/q_hebb_edge.v`, 221 lines)
One synapse with **two selectable decay engines** behind one interface
(header `:1`–15):
- **MODE=0 ladder:** K saturating bucket counters; cofire increments
  bucket 0; every half-life (HL ticks) the ladder shifts one class older.
  Readout Ŵ = Σ Cᵢ·2⁻ⁱ via a *registered sequential loop* (no UNOPTFLAT
  adder tree). Proven bound: `W_exact ≤ Ŵ ≤ 2·W_exact`. One fresh cofire
  reads 2⁸=256 at K=B=8; readout saturates, never wraps.
- **MODE=1 hyperbola:** integer W + age; decay interval P0≫2·msb(W).
  Integrates to W(t)=W₀/(1+W₀t/P0) within [1,4)× the exact interval.
  Integer state throughout — "never fixed-point, so it never drifts"
  (`:15`–16).
Commands: 001 train, 010 tick, 011 read (K+1 cycles), 100 set-base,
101 **graded train** — v2's new command that lands a cofire in bucket
`clamp(gclass, K-1)`; cmd 001 keeps exact v1 semantics, so old cores/TBs
are bit-exact (`:17`–24). Invariants: `o_done` pulses per command;
readout sequencer has priority over new commands (`:134`–137); `o_ovf`
is sticky train-time saturation. Reason: two research engines competed
(scorecard); shipping both behind one port cost nothing and keeps the
comparison honest.

### 3.5 q_echo_gate (`rtl/q_echo_gate.v`, 93 lines)
Per-cell fire trace: one register, three rules — fire: F←max; tick:
F←F−(F≫KLE) with deadband snap; gate: `live = F ≥ FLOOR`, class =
15−msb(F) (`:5`–12). FLOOR=0 disables → bit-exact v1. Reason (v2 fold-in
1): an effect should train an edge only inside a causal window after this
cell's own fire — "I fired, then you echoed me". The deadband snap is
hardened one step past the original sketch because small-F/large-KLE
combos would otherwise park the trace immortally in [2, 2^KLE)
(`:65`–75). Cost: 17 FF, no multipliers (`:26`–29). Proven: dyadic octave
bracket + PRIORITY (fire beats leak) + MONO + ZEROABSORB + DISABLED ≡ v1
(`formal/echo_gate.dyadic.sby`, BMC 25).

### 3.6 q_rqh_bank (`rtl/q_rqh_bank.v`, 138 lines)
Per-edge quantum reservoir R: graded cofires deposit, ticks leak, and
readout gets a credit `R ≫ QDW` (module `:52`, ports to `:69`). **The deposit is the
corrected condition**, not the proposal's 2^g: the original was falsified
by error-envelopes Thm 3c (inverted class dependence, ~18,262× too small
at class 0); this module implements `deposit(g) = 2^(K+QDW−g)·9/32`
(two shifts + an add, no multiplier, `:95`–100; the exact form in the header `:28`–32). Deadband leak on tick is
load-bearing: without snap-to-0 a stale residue could cross a credit
boundary with no fresh cofire — a false anticipation (`:41`–46).
Invariant: saturating add, never wraps; RQEN=0 freezes the bank = v1.
Reason (v2 fold-in 2): the gate grades every cofire; the bank returns
what the graded placement drops. The pair shipped together.

### 3.7 q_hebb_rqh (`rtl/q_hebb_rqh.v`, 115 lines)
Standalone research variant of the residue bank with a *different*
corrected deposit (`(4565·2^s + 8192) ≫ 14`, `:18`–21). **Not in the
fabric** — it lives behind `tb/tb_rqh_saturation.v` as the exploration
lane for the exact T3c constant. Fixing two sketch bugs taught the rules
the bank now follows: register the credit off R (no phantom credit on
idle cycles) and snap the deadband at the tail (`:23`–28). Touch this
only if you are researching deposits; the fabric uses `q_rqh_bank`.

### 3.8 q_cell_core (`rtl/q_cell_core.v`, 596 lines)
The only opcode interpreter. 22-state run-to-completion FSM (`:129`–136).
The two load-bearing guarantees (docs/SYNTHESIS.md Q1/Q2, header `:3`–14):
- **Q1 liveness:** every op is bounded; `ci_ready` reasserts after each
  op, so views/binds are never starved by effect traffic.
- **Q2 non-deferrable time:** `s_tick` latches into `tick_pend` from any
  state (dedicated interlock block, `:586`–595) and ST_IDLE services it
  *before* new ingress (`:314`–318). A tick is deferred by at most the
  in-flight op.
Opcode semantics in six lines (header `:16`–27): bind = first-bind sets
cell_id, later binds write dial a0[3:0]; link = edge slot {peer, base};
effect = if src matches a valid edge, train (through the echo gate), read
back, `act += sat((w·dat)≫15)`, unknown src dropped silently; view =
0 act / 1 wsum / 2 dial / 3 NAK (no cosine readout in v1); tick = decay
sweep + act leak + fire test (act ≥ THRESH && refr==0) → fanout effects.
Two hard-won details:
- **Q2fix ready gating:** every return-to-IDLE path asserts
  `ci_ready <= !(s_tick || tick_pend)` (six sites: `:321, :383, :433,
  :511, :550, :560`). The original unconditional `1'b1` left a one-cycle
  hole where an upstream pipe popped a flit the FSM ignored — a silent
  drop found by two formal proofs independently (formal/README.md
  Finding 2).
- **wacc width:** the wsum accumulator is PW+EIW+1 bits because 4 readouts
  of 0xFFFF sum past 2^(PW+1) and wrapped (`:146`–152, differential-found
  2026-08-29).
PIPE_EFF=1 (the shipped config) retimes the effect cone into three
registered stages — bit-exact values, +2 clk per effect (`:45`–48). Both
formal cell proofs and the conservation proof are pinned to PIPE_EFF=1
(formal/README.md results table).

### 3.9 q_cell (`rtl/q_cell.v`, 279 lines)
The assemblage: core + dialfile + EDGES_N edge engines + ringport +
**elastic ingress/egress buffers**. Reason for the buffers (header `:4`–11):
without them, a core holding a response while an inbound flit awaits
delivery deadlocks (inject_ok=0 and ld_ready=0 wait on each other); with
them the core always returns to IDLE and the ring's bubble drains. The
engine weight readout is a **one-hot mux, not an OR-tree** — `o_w` is a
register that keeps its last readout forever, so the old OR-mask ORed
stale weights into every later wsum (fuzz-fix, `:195`–210). The boot dial
port (`i_bdf_*`) rides the POR domain, not the fabric reset: quf_boot's
writes land while the core is FSM-frozen — "exclusion by construction,
not arbitration" (`:13`–20).

### 3.10 q_io_port — see §2.

### 3.11 q_fabric_top / q_serfabric_top — see §2 and §4.

### 3.12 q_uf_loader (`rtl/q_uf_loader.v`, 690 lines)
The synthesizable QUF parser: a 25-state byte-stream FSM that walks the
header, skips unknown KV pairs, captures `edge.k`, then streams the
dials / edges / routing / ticks payloads into write ports (profile in
docs/QUF-SPEC.md §9). Eats one word every 1-of-3 cycles; `o_rdy` local
only (`:90`). Error taxonomy 1–9, sticky (`:62`–65): bad magic, bad
version, layout overrun, bad endian word, known-KV-wrong-type, unknown
value type, nonzero u64 high, name too long, edge.k out of range.
Honest limit: edge walk state (wh, age, buckets) is consumed but **not
restored** — v1 engines have no load port (`:14`–16); the Python
reference (`tools/quf.py`) restores everything.

### 3.13 quf_boot (`rtl/quf_boot.v`, 260 lines)
Boot harness around the loader: POR→HOLD→LOAD→LATCH→REL→RUN, with a
sticky HOLD_ERR on any error (states `:86`–88). Fail-static: the fabric
is never released into a half image; recovery is POR (`:15`–18). The
fabric reset is `o_rst_n = (state == S_RUN)` (`:255`) while the dialfile
stays on POR — boot dial writes land while the fabric is frozen; runtime
qm_bind writes only happen in RUN; the windows are disjoint FSM states,
so the mux needs no arbitration (`:19`–25, mux `:189`–197). Epoch: tpw
latches once at LATCH and is frozen for the run (`:35`–38). Residue
after done (the QUF writer's align padding) is accepted and discarded —
stalling the host on residue would wedge it (`:128`–133).

### 3.14 q_boot_gate (`rtl/q_boot_gate.v`, 131 lines)
quf_boot's FSM discipline without the parser: it eats exactly two bytes,
the release word 0x51 0x46 ("QF"), and releases. Reason: on UP5K the
parser does not fit next to even one cell (1488 LUT loader + 3958 LC
fabric > 5280), so the QUF parse runs host-side and configuration
streams as bind flits (`:1`–14`). Wrong word = sticky HOLD_ERR (err 11);
state encoding matches quf_boot exactly (status contract, `:25`–26).

### 3.15 q_fabric_top.v, q_flit_pipe.v, q_link_ringport.v — see §2.

---

## 4. The QUF boot path, end to end

Doctrine item 3: **state is a file.** The path from bytes to a running
fabric:

1. **Write** — `tools/quf.py create tb/quf_tb.json tb/run/quf_tb_input.quf`
   builds the golden container (selftest: 576 bytes, sha256 `5b2a…1392`, round-trip byte-exact — quoted from the suite
   run in §6). Format: magic `51 55 46 00`, u32 version/endian/kv_count,
   GGUF-numbered KV metadata, a section table, then aligned sections
   `dials` (cell_count × 16 × u16), `edges` (12+K bytes each, both
   engines' state), `routing` (dst/via pairs), `ticks` (u32 tpw + per-cell
   phases) — docs/QUF-SPEC.md §2–6.
2. **Transport** — `quf_boot` pairs bytes into words with a 1-word skid
   and feeds `q_uf_loader`. `q_serfabric_top` broadcasts one stream to
   N loaders, each pinned to its cell by `i_mycell`; the FSMs run in
   lockstep and cell 0's control outputs drive the fabric
   (`rtl/q_serfabric_top.v:113`–133).
3. **Load** — dial rows land in the dialfiles through the boot dial port
   while the cores are held in reset; edge/route writes have **no sink
   in v1** (engines have no load port) — left unconnected, pruned by
   synthesis, probed hierarchically by the TB; "nothing pretends
   otherwise" (`rtl/q_serfabric_top.v:56`–59).
4. **Latch + release** — on clean done: tpw latches once, `o_epoch` and
   `o_boot_ok` pulse, `o_rst_n` rises, and `q_tick_sched_rt` starts the
   epoch cycle-exactly (`rtl/q_tick_sched_rt.v:45`–49).
5. **Run** — the byte port changes meaning: 10 bytes per flit, MSB
   (header) byte first (`rtl/q_serfabric_top.v:30`–31). The **ARMED
   discipline** is the hard lesson kept in silicon: QUF align padding
   can exceed ten bytes after done, and ten zero pad bytes assemble into
   a perfectly valid BIND flit (op=0, dst=0) that would bind cell 0 —
   so bytes are flits only once armed, by `i_eod` (QUF mode) or the
   release word (gate mode); unarmed run-phase bytes are accepted and
   dropped (`:170`–187).

Gate mode (`SER_BOOT_QUF=0`) is the same path minus the parser: host
parses QUF, streams the release word, then configures cells with bind
flits over the same narrow port; `q_boot_gate` keeps fail-static +
latch-once. Both modes are exercised in `tb/tb_serfabric.v` (differential
against the parallel fabric, byte-exact dial rows, 68-flit egress
streams cycle-locked, fail-static gate).

---

## 5. Coding conventions actually used (not aspirational)

The Law (README.md): **pure Verilog-2005, synthesizable subset** — no
vendor primitives, no IP, no `initial` in `rtl/` (testbenches excepted),
no SystemVerilog in `rtl/`. Why: one repo, zero vendor deps; the same
RTL must elaborate in iverilog (TBs), verilator (fuzz lanes), yosys
(formal + iCE40 synthesis) without `ifdef` forests. Every violation
found in review was removed, not argued with.

Patterns the tree holds you to (all enforced by example + lint):

- **Local-only ready.** Any `*_ready` output is a function of local
  state only (`q_flit_pipe.v:46`, `q_uf_loader.v:90`,
  `quf_boot.v:132`–133, `q_boot_gate.v:65`). This is what makes a ring of them provable and
  closable.
- **Saturate, never wrap.** Every accumulator that can overflow
  saturates (`q_cell_core.v:192`, sclip16; `q_hebb_edge.v:116`–118;
  `q_rqh_bank.v:104`–108). Fixed-point from birth; no floats in fleet
  state (the QUF reference refuses to emit f32/f64, QUF-SPEC §4).
- **Strobes default low each cycle**; multi-cycle ops pulse `done`
  (`q_cell_core.v:280`–286; `q_hebb_edge` cmd contract).
- **Reset style:** async-asserted? No — synchronous active-low
  `always @(posedge clk) if (!rst_n)` throughout; state machines list
  every register in reset. No `initial` values; formal harnesses force a
  two-timestep reset preamble (docs/FORMAL-PROOFS.md, "Method").
- **Header comments are the design doc.** Each `rtl/*.v` opens with
  why-it-exists, the invariants, and the casualties (fuzz-fix notes cite
  date + finder). When you edit, update the header; when you fix a bug,
  leave the note (`q_cell_core.v:146`–152 is the house style).
- **Verilator lint pragmas** are surgical and commented
  (`/* verilator lint_off UNUSEDSIGNAL */` around genuinely unused
  taps, `q_cell.v:111`–135; `lint_off WIDTHTRUNC` for the deliberate
  PW−1 constant, `q_echo_gate.v:46`–48).
- **Parameters have defaults** and every TB instantiates with defaults
  unless proving a config point (`tb_cell_core.v:25` overrides nothing
  but EDGES_N; formal conservation shrinks params on purpose and says
  so, formal/README.md).
- **Dials over parameters for runtime knobs**; new features ship
  default-OFF = bit-exact v1 so the v1 suite is the A/B referee
  (`q_dialfile.v:67`–75).
- **Testbenches are loud:** a PASS banner greppable by
  `tb/run_suite.sh` (`PASS` on stdout), golden values inline, guard
  counters against hangs (`tb_cell_core.v:10`–13).
- **Yosys-formal-safe style:** no multi-driven registers (Finding 1 in
  formal/README.md cost exactly that lesson), no hierarchical refs from
  harnesses into DUTs (undriven-wire trap, same doc).

---

## 6. Build and verify flows — run them, quote them

One command per lane; the Makefile pins oss-cad-suite itself
(`Makefile:4`–5), so no exports are needed. Everything below was run on
this tree while writing this guide (2026-08-30); the historical
measurements live in `docs/VERIFICATION.md`.

### make test — RTL testbench suite (iverilog -g2005)

Runs `bash tb/run_suite.sh`: 18 benches, one line each, PASS banner
required. Measured just now:

```
PASS  tb_tick_sched: TB_TICK_SCHED PASS
PASS  tb_flit_pipe: TB_FLIT_PIPE PASS
...
PASS  tb_fabric_smoke: TB_FABRIC_SMOKE PASS (train->fire->decay, maxlat=31)
PASS  tb_fabric_smoke_v2: TB_FABRIC_SMOKE_V2 PASS (echo-gate+RQH, maxlat=31)
PASS  tb_hebb_pipe: TB-HEBB-PIPE PASS: 300 ops, 224 lo flits, 18 lx flits,
      act/trace bit-exact at every checkpoint
PASS  tb_quf_boot: TB-QUF-BOOT PASS: warm-start, corrupt-header fallback,
      truncation fallback, epoch latch -- all 4 cases
PASS  tb_quf_loader: quf.py selftest PASS: 576 bytes, sha256 5b2a...1392,
      round-trip byte-exact
PASS  tb_serfabric: TB-SERFABRIC PASS: QUF serialized boot byte-exact (2 cells),
      serial==parallel egress streams (68 flits, cycle-locked), ...
```

18/18 PASS, ~1 min wall. (Full one-line-per-bench list: VERIFICATION.md
Lane 1.)

### make sim — behavioral Python lane

```
python3 -m unittest discover -s sim/tools -p 'test_*.py'
..................................
----------------------------------------------------------------------
Ran 34 tests in 0.007s

OK
```

34/34 OK. This is a model check of the Python tap-fabric bridge over the
same QUF — not a hardware proof (VERIFICATION.md, scope note).

### make formal — six SymbiYosys proofs

`sby -f` over the five `formal/*.sby` plus `tb/formal/flit_pipe.sby`
(Makefile `FORMAL_SBY` list). Re-run for this guide, 2026-08-30, on a
shared machine — verdicts and wall times straight from each task's
`formal/<task>/status`:

| proof | mode (tree's .sby) | verdict | measured wall time (this pass) |
|---|---|---|---|
| `echo_gate.dyadic` | BMC 25 | PASS | 2 s |
| `tb/formal/flit_pipe` | prove (k-ind), depth 15 | PASS | <1 s |
| `flit_pipe.fly` | BMC 40 | PASS | 73 s |
| `fabric.conservation` | BMC 55 | PASS | 37 s |
| `cell_core.tick` | BMC (README: 80) | PASS | 215 s |
| `cell_core.fair` | BMC (README: 80) | PASS (documented; see note) | — |

The five measured rows land on the documented timings (3 s / <1 s /
72 s / 38 s / 215 s, formal/README.md) — verdicts are the stable fact.

**cell_core.fair note (full honesty).** The last complete PASS runs are
the documented 2026-08-29 iterations (498–919 s across passes; formal/
README.md, VERIFICATION.md Lane 3). It was re-attempted four times for
this guide without completing: the tree's `formal/cell_core.fair.sby`
now carries depth 130 (deeper than the README's "BMC 80" label), a solo
run costs well over an hour, and this box was shared with sibling lanes
at load ~8 (which also caused a workdir collision — `sby -f` wipes the
shared `formal/<task>/` dir; serialize formal runs per clone). Every
attempt ground past step 100 with **zero counterexamples** before being
cut by session limits or that collision, so no fresh wall time is
claimed. Budget 1–2 h solo; deep steps slow to ≈3–4 min/step past 100.

Scope caveats that matter when you rely on these: bounded model
checking — "unbounded liveness is not claimed" (formal/README.md) —
under stated environment contracts E1–E4, each weaker than the real
system. The two RTL defects the proofs forced (multi-driven `tick_pend`;
the ci_ready one-cycle hole) are documented as Findings 1–2 in
formal/README.md and fixed in the tree.

### make synth / make pnr — iCE40 elaboration, then the measured numbers

`make synth` = `yosys -s synth/fpga-converged.ice40` (elaboration of the
PnR-converged k4b4a8e1 config on the real `q_fabric_top`). Measured just
now, exit 0 (~20 s), final stat table:

```
=== q_fabric_top ===
   Number of cells:               9358
     SB_CARRY                      898
     SB_LUT4                      6002
     ... (DFF-class cells ~2,430)
   Number of port bits:            157
```

`make pnr` = nextpnr-ice40 (HX8K-CT256, 12 MHz target) + icepack.
Measured just now: exit 0, ~1–3 min, `synth/report_k4b4a8e1.json` →
**7,596/7,680 ICESTORM_LC (99%), 157/256 SB_IO, fmax achieved 44.43 MHz
(PASS at 12.00 MHz)**, and a fresh **135,100-byte**
`synth/fabric2_k4b4a8e1.bin`. (PnR seed variance is real and documented:
40.44 / 43.36 / 44.43 MHz across passes — VERIFICATION.md Lane 4.)

`make all` = all five in order. `make clean` removes generated proof
dirs and `tb/run` artifacts only — sources stay.

---

## 7. How to add a module — walkthrough

The repo's own v2 fold-in is the template: `q_echo_gate` went from
proposal to proven-in-fabric exactly this way. Steps, with the real
artifacts named:

1. **Write the header first.** Open `rtl/q_strobe_gen.v` with why it
   exists, its invariants, and its cost estimate — copy the shape of
   `rtl/q_echo_gate.v:1`–29 (one register, three rules, cost line).
   Verilog-2005, no `initial`, parameters with defaults.
2. **Obey the two laws of §5:** local-only ready (if it has a handshake)
   and saturate-never-wrap (if it accumulates).
3. **Give it a dial, default OFF**, if it changes existing semantics —
   the bit-exact-v1 switch is how every acceptance TB stays valid
   (`q_dialfile.v` map + defaults; `q_echo_gate` took dial 12 FLOOR=0).
4. **Write the TB** next to it: `tb/tb_q_strobe_gen.v`, golden values
   inline, loud `PASS` banner, guard counter (copy `tb/tb_q_echo_gate.v`).
5. **Wire the suite:** add the file to the `RTL=` list and a
   `t tb/tb_q_strobe_gen.v tb_q_strobe_gen` line in `tb/run_suite.sh`
   (both edits, ~two lines).
6. **Run `make test`** — 19/19 must PASS. If your module sits under a
   cell op, also run `make formal` (the cell proofs pin invariants at the
   core boundary) and consider a dedicated `.sby` — start from
   `formal/echo_gate.dyadic.sby` (15 lines: options/engines/script/files)
   and add `cover` statements for non-vacuity.
7. **If it's a fabric path:** instantiate it in `q_cell.v` (structural,
   like the edge array generate block, `q_cell.v:177`–191) — never in
   `q_cell_core` unless it interprets opcodes. Keep the serfabric ring
   mirroring `q_fabric_top` exactly; the differential TB is the guard.
8. **Update the headers you touched**; if measured numbers moved, re-run
   the lane and update `docs/VERIFICATION.md` (measured-or-buggy rule).

Checklist before commit: `make test` green; `make sim` untouched-green;
formal still PASS; headers updated; no vendor code; PASS banner greppable.

---

## 8. Debug playbook

Symptoms → first moves, in the order the repo's history actually played
them:

- **A testbench "hangs"** → it hasn't; the guard counter tripped a
  timeout (300 s in run_suite.sh). Look for a violated local-only-ready
  rule or a `done` you stopped pulsing. Re-run the single bench:
  `iverilog -g2005 -s tb_x -o tb/run/tb_x.vvp rtl/… tb/tb_x.v && vvp
  tb/run/tb_x.vvp` (the suite prints exactly this shape).
- **Value corrupted only with multiple edges / after re-reads** → the
  OR-tree vs one-hot mux class. Registers hold last values forever;
  never OR engine outputs (`q_cell.v:195`–210; the wacc wrap sibling,
  `q_cell_core.v:146`–152).
- **Flit silently disappears under load** → suspect a ready/valid hole
  at an FSM dispatch boundary (the Q2fix class, §3.8). The formal
  conservation proof is the scalpel: it found the accepted-effect-never-
  booked counterexample (formal/README.md Finding 2).
- **Boot binds cell 0 at power-up out of nowhere** → pad bytes leaking
  through the boot→run boundary; check the ARMED discipline
  (`q_serfabric_top.v:168`–186).
- **Ring deadlocks** → someone made ready a function of downstream
  ready, or removed an elastic buffer; re-read `q_cell.v:4`–11 and
  `q_flit_pipe.v:1`–5.
- **Formal run fails with "Found multiple drivers"** → a register
  assigned in two always blocks (Finding 1). Merge the driver.
- **Artifacts: where things land.** iverilog outputs go to `tb/run/*.vvp`
  (gitignored); verilator builds (fuzz/cosim lanes) leave `obj_dir/Vtb_*`;
  each sby proof materializes `formal/<task>/` — read
  `formal/<task>/logfile.txt` first, then `engine_0/logfile_*.txt` for
  the counterexample trace (a failing induction leaves
  `trace_induct.vcd`). `make clean` removes all of these; sources are
  never touched.
- **Fuzz lanes** (not part of the default suite, run them for boot/cosim
  changes): `tb/tb_boot_fuzz.v` reads a manifest from
  `tools/backend/boot_fuzz.py` (hex in `tb/run/`), asserts warm-boot and
  fail-static contracts per case (`tb/tb_boot_fuzz.v:1`–11`);
  `tb/tb_cosim_fuzz.v` is the same idea for the ring.
- **Differential method** when two paths must agree (serial vs parallel,
  PIPE_EFF 0 vs 1): build both in one TB, drive them cycle-locked, diff
  at checkpoints — `tb_serfabric.v:1`–24 and `tb_hebb_pipe.v` are the
  exemplars; this technique found more real bugs than any other lane.

---

## 9. Glossary

| term | meaning |
|---|---|
| flit | the 75-bit fabric word `{op, src, dst, a0, a1, a2, dat}` |
| cell | one ring node: core FSM + dials + edge engines (+ v2 wrappers) |
| dial | one of the 16 runtime registers in `q_dialfile` (view/bind addressable) |
| edge engine | one `q_hebb_edge`: a synapse with ladder or hyperbola decay |
| ladder | K-bucket decay engine; bucket i ≈ weight 2⁻ⁱ; bound Ŵ ≤ 2·W_exact |
| hyperbola | integer W+age decay; W(t)=W₀/(1+W₀t/P0) within [1,4)× |
| cofire | an effect arriving from a peer this cell fired at (the train event) |
| echo gate | per-cell fire trace gating *learning* (not activation) to a causal window |
| RQH | Residual-Quantum Hebb: per-edge residue bank returning graded-placement drops as readout credit |
| QUF | QUilt Format: the GGUF-shaped binary container for full cell state |
| tick | the 1-cycle timebase strobe (every 2^TPW clocks); non-deferrable in-cell |
| epoch | the run's t=0: release moment; tick period latches once here |
| EXTID | ring id of the io node (default 4'hF): where external streams enter |
| skid buffer | 2-deep pipe slice whose s_ready is local-only (no ready chains) |
| PIPE_EFF | 3-stage retime of the effect cone; bit-exact, +2 clk per effect |
| fail-static | any boot error parks sticky with the fabric frozen; recovery = POR |
| latch-once | runtime knobs (tpw) latch at release and are frozen for the run |
| armed | serfabric rule: bytes are flits only after i_eod / release word |
| BMC | bounded model checking: no counterexample ≤ depth (not unbounded) |
| k-induction | unbounded proof: base case + induction step (used once: flit_pipe) |
| LC / LUT4 | iCE40 logic cell; the fabric measured 7,596/7,680 (99%) on HX8K |
| oss-cad-suite | the open toolchain bundle: iverilog, verilator, yosys, sby, nextpnr |
| Q1 / Q2 | liveness-under-load / non-deferrable-time guarantees (SYNTHESIS.md) |
| maxlat | measured worst op latency in the smoke TBs: 31 cycles |

---

*House rule, repeated: if a number in this guide cannot be reproduced on
this tree, it is a bug in this guide. The flows in §6 are the oracle.*
