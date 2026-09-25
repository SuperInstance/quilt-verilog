# 🔌 quilt-verilog

The bottom layer of the quilt, in silicon logic. A cellular learning
fabric — Hebbian edges, power-law forgetting, dial state, a fabric-wide
tick — written in pure, generic Verilog-2005 (IEEE 1364-2005): no vendor
primitives, no IP cores, no SystemVerilog, no floats. Every module is
parameterized, fixed-point, and streaming. It is verified by a 23-bench
testbench suite, six SymbiYosys formal proofs, and a real iCE40 bitstream
produced entirely with open tools, and its complete state travels in one
flat binary file — QUF, the GGUF of cellular silicon — that a testbench,
a soft core, or an FPGA load identically. This page states what exists
and what is verified, matter-of-fact; the deep docs (map below) carry the
rest of the story.
> **The Quilt cell-fabric runtime in Verilog.** Part of the [polyformalism](https://github.com/SuperInstance/quilt-claude-charts/blob/main/QUILT_CHARTER.md) — the same cell model, expressed in 12+ languages, byte-exact compatible.

<p align="center">
  <img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="Apache-2.0">
  <img src="https://img.shields.io/badge/language-Verilog-blue.svg" alt="Verilog">
  <img src="https://img.shields.io/badge/hash-0xe435d91d6d92a1d8-brightgreen.svg" alt="byte-exact">
</p>

## ✦ Why this port exists

The Verilog port of the Quilt. The Verilog port is distinctive because of its position in the language hierarchy — `iverilog/quartus-compileable, Verilog-idiomatic, byte-exact with the rest of the polyformalism.

| lane | command | result | where |
|---|---|---|---|
| RTL simulation | `make test` | **23/23 PASS** (✓ re-run 2026-09-03; the suite emits its own `SUITE SUMMARY: 23/23` line — the count is machine-derived, never hand-edited) | [docs/VERIFICATION.md](docs/VERIFICATION.md) |
| Behavioral model | `make sim` | **34/34 OK** (✓ re-run 2026-08-30) | [docs/VERIFICATION.md](docs/VERIFICATION.md) |
| Formal proofs | `make formal` | **6/6 PASS** — 5 BMC + 1 k-induction (last full run 2026-08-29) | [docs/FORMAL-PROOFS.md](docs/FORMAL-PROOFS.md) |
| iCE40 synth + PnR | `make synth && make pnr` | HX8K-CT256: **7,596/7,680 LC (98%), 44.43 MHz post-route @ 12 MHz target, 135,100-byte bitstream** (2026-08-29) | [docs/SYNTHESIS-RESULTS.md](docs/SYNTHESIS-RESULTS.md) |
| Smallest device | — | UP5K sg48, 1 cell: 80.1% LC, 37 IO, **16.78 MHz post-route** (2026-08-29) | [docs/SYNTHESIS-RESULTS.md](docs/SYNTHESIS-RESULTS.md) |
| ECP5 ladder | — | LFE5U-25F: **8 cells @ 63.7 MHz**; real 12F: 4 cells (2026-08-29) | [docs/SYNTHESIS-RESULTS.md](docs/SYNTHESIS-RESULTS.md) |

The proofs are not decoration: their first runs found **two real RTL
defects** (a multi-driven register simulators accepted but yosys
rejected, and a one-cycle ingress-drop hole under a pending tick) — both
fixed, both now regression-guarded ([formal/README.md](formal/README.md)).

## The 5+1 opcode model

One opcode field (3 bits) is the entire instruction set — five host
verbs plus one response channel. There is nothing else. Every dial
write, every training event, every readout, and the passage of time
itself is one of these, executed by `q_cell_core` as a cooperative
run-to-completion FSM (one interpreter per cell; events serialize):

| opcode | encoding | does |
|---|---|---|
| `qm_bind` | `OP_BIND = 0` | first bind sets `cell_id` and binds the cell; later binds write a dial `a0[3:0] <= a1` |
| `qm_link` | `OP_LINK = 1` | edge slot `a0` := `{peer=src, base weight=a1}` — wiring as data |
| `qm_effect` | `OP_EFF = 2` | if src matches a valid edge: train that edge (cofire, echo-gated in v2), read the weight back, integrate `act += sat((w·dat)>>>15)`; unknown src is dropped silently |
| `qm_view` | `OP_VIEW = 3` | read `act` / `wsum(edges)` / a dial; response flit carries the value (no cosine readout in v1 — that path NAKs) |
| `qm_tick` | `OP_TICK = 4` | decay sweep over all valid edges, leak `act`, fire test (`act ≥ thresh ∧ refr = 0`) → fanout effects to every linked peer |
| ack/nak | `OP_ACK = 5`, `OP_NAK = 6` | the +1: every bind/link/view (and every op from an unbound cell, and every undefined opcode) is answered — never left hanging |

The tick is special: it cannot be starved. A pending tick suppresses
ingress acceptance (`ci_ready`) until serviced — non-deferrable time,
proven under permanent ingress flood ([docs/FORMAL-PROOFS.md](docs/FORMAL-PROOFS.md), §4).
One tick traced end-to-end through the RTL: [docs/THE-TICK.md](docs/THE-TICK.md).

## Quickstart — one command per lane

Toolchain: stock oss-cad-suite (Icarus, Yosys, SymbiYosys, boolector,
nextpnr-ice40, icepack). The Makefile pins
`/home/eileen/tools/oss-cad-suite/bin` itself; if yours lives elsewhere:
`make OSSCAD=/path/to/oss-cad-suite/bin <target>` — and if a tool is
missing, the targets fail with a pointed hint, not a bare
`command not found`.

```sh
make verify-all # prove it works: every tutorial (T1..T4) end to end
make test      # RTL testbench suite (iverilog)          — 1-2 min
make sim       # behavioral Python lane (unittest)       — seconds
make formal    # all six SymbiYosys proofs               — ~14 min
make synth     # yosys iCE40 elaboration of the top      — ~20 s
make pnr       # nextpnr-ice40 + icepack → bitstream     — ~3 min
make all       # all five, in order
```

What `make test` printed when this README was written (2026-09-03,
26 PASS lines from 23 benches — some benches print several PASS lines;
abridged — first two and last four, plus the machine-emitted summary):

```
$ make test
bash tb/run_suite.sh
PASS  tb_tick_sched: TB_TICK_SCHED PASS
PASS  tb_flit_pipe: TB_FLIT_PIPE PASS
    … 12 more PASS lines …
PASS  tb_hebb_pipe: TB-HEBB-PIPE PASS: 300 ops, 224 lo flits, 18 lx flits, act/trace bit-exact at every checkpoint
PASS  tb_quf_boot: TB-QUF-BOOT PASS: warm-start, corrupt-header fallback, truncation fallback, epoch latch -- all 4 cases
PASS  tb_quf_loader: quf.py selftest PASS: 576 bytes, sha256 5b2a236ba5e38bca9ad96783c4252a12f36517f98a9164a249f0db115f221392, round-trip byte-exact
PASS  tb_serfabric: TB-SERFABRIC PASS: QUF serialized boot byte-exact (2 cells), serial==parallel egress streams (68 flits, cycle-locked), end-state dial rows byte-exact, gate-mode fail-static + release-word epoch + serial-flit config -- all cases
SUITE SUMMARY: 23/23 benches PASS
```

Do not quote a bench count from this README; quote the `SUITE SUMMARY`
line your own run prints — the suite tallies its benches mechanically,
so the count moves when benches are added and cannot drift stale.

What `make sim` printed, complete:
## ✦ The 5 opcodes

```
BIND(cell, dials)   # set dials, idempotent
LINK(c1, c2)        # add an undirected edge
EFFECT(cell)        # propagate dial[0] to neighbors
VIEW(cell)          # return dials
TICK(fabric)        # advance all dials by 1, alternating direction
```

`make formal` and `make synth && make pnr` were last run green on
2026-08-29 and are recorded, timings included, in
[docs/VERIFICATION.md](docs/VERIFICATION.md) (all lanes) and
[docs/SYNTHESIS-RESULTS.md](docs/SYNTHESIS-RESULTS.md) (the reproduce
commands for every measured number). What each of the six proofs claims
— FIFO safety, ledger conservation, the dyadic echo-gate bracket, tick
deadlines, op-response bounds — is stated in plain mathematics in
[docs/FORMAL-PROOFS.md](docs/FORMAL-PROOFS.md), assumptions included.

## The Law

1. **Pure Verilog-2005 (IEEE 1364-2005), synthesizable subset.** No
   vendor primitives, no IP, no `initial` blocks in `rtl/` (testbenches
   excepted), no SystemVerilog in `rtl/`.
2. **Everything is a cell.** The opcodes above are the only way anything
   touches anything.
3. **Intelligence lives at the bottom.** Hebbian edge updates,
   power-law/hyperbolic decay, dial state — plain RTL, fixed-point,
   streaming. The cosine/vMF reading of those weights is defined in the
   math docs (`docs/academic/`); its dedicated readout is reserved for v1.
4. **Any IO can enter a cell.** One generic ingress/egress contract;
   adapters are thin and dumb.
5. **Verified or it doesn't exist.** Every module ships with a
   testbench runnable on open tools (iverilog/verilator). No toolchain
   lock-in, ever.

## Layout

- `rtl/` — 17 modules: the winning architecture as built (the truth)
- `tb/` — testbenches, the suite runner, formal harnesses
- `sim/` — behavioral Python prototypes over the same QUF the RTL loads
- `formal/` — machine-checked invariants (SymbiYosys)
- `synth/` — iCE40/ECP5 synthesis + PnR flows and measured tables
- `proposals/<crew>/` — competing architecture entries (the tournament)
- `tools/` — QUF reference implementation, backend fuzz, edge benches
- `docs/` — decisions, math notes, floorplans — map below

## Measured results

Full provenance — every run dated, every artifact named, including two
fmax numbers corrected (post-placement estimates once quoted as final) —
lives in [docs/SYNTHESIS-RESULTS.md](docs/SYNTHESIS-RESULTS.md). Headlines:

| config | device | LC / cap | fmax post-route @ 12 MHz | bitstream |
|---|---|---|---|---|
| `q_fabric_top` k4b4a8e1 (2 cells) | iCE40 HX8K-CT256 | 7,596 / 7,680 (**98%**) | **44.43 MHz** | 135,100 B (tracked) |
| serfabric NCELL=1 (serialized front-end) | iCE40 UP5K sg48 | 4,231 / 5,280 (80.1%), 37/96 IO | **16.78 MHz** | — |
| ladder top | ECP5 LFE5U-25F | 22,791 / 24,288 (94%), 8 cells | **63.7 MHz** | — |

The fmax story across one design's life: 27.72 → 40.44 MHz (the PIPE_EFF
retime, +46%) → 44.43 MHz on the current tree. Every configuration that
closes does so at ≥1.4× the 12 MHz target.

## Honest limitations

Copied in short from [docs/VERIFICATION.md](docs/VERIFICATION.md)'s
not-covered list — read that section before relying on any of this:

- **No on-hardware test.** Every result is simulation, formal, or
  synthesis. The bitstream has never met a board; no PCF exists (IO is
  auto-placed).
- **Unbounded liveness is not claimed.** Five of six proofs are BMC
  (bounded); only the flit-pipe contract is k-inductive. Fair/tick
  proofs rest on stated environment contracts E1–E4.
- **Formal parameters are shrunk.** Conservation is proven at
  EDGES_N=1, K=4, B=4 — not full fabric scale.
- **The Python lane is a model, not a miter** — no formal equivalence
  proof between Python and RTL semantics.
- **The dev-rounds ladder is model-grade, not silicon-grade.** The
  interference/rounds experiments (rounds 2–7:
  `spikes/225-e1-interference-tick/dev-rounds/`) run on an integer-only
  Python harness over the same QUF/tick semantics the RTL implements —
  not on the Verilog. Numbers there (contention walls, phase decay, the
  N=4 trueRes 12.2%→86.3% lag-compensation result, the co-fire wall at
  N≈7) are **findings about the model**: candidate spec limits a
  silicon lane should confirm, not measured Verilog properties. The
  README verification table above deliberately lists only RTL benches,
  formal proofs, and synthesis; rounds work joins that table if and
  when a lane reproduces it against the fabric RTL.
- **`rtl/q_wall_gate.v` (wheel/spin-19 lane) is outside the table's
  surface.** It is a standalone gate module verified by its own
  Verilator cosim against the Python reference — 21/24 full-dict
  bit-exact, 3/24 (step5_off, seeds 1/7/42) prefix-match then cosigned
  divergence where the arbitrary-precision reference and the 48-bit
  datapath legitimately part ways
  ([wheel/SPIN-19-rtl-honesty.md](wheel/SPIN-19-rtl-honesty.md)). No
  bench, sim, or formal proof above instantiates it.
- **No CI.** Verification runs when an iterator runs it.
The canonical serialization is `type(1) || id(8 LE) || dials(32 LE) || neighbors(8*N LE)`. The state hash is FNV-1a 64-bit. The test cell (id=1, dials=[1..16], neighbors=[2,3,4]) produces `0xe435d91d6d92a1d8` byte-exactly.

## ✦ The full polyformalism

| Lang | Hash | Tests |
|------|------|-------|
| Python 3 | ✓ | 7/7 |
| C99 (Verilog) | ✓ | manual |
| Rust | ✓ | 6/6 |
| Go | ✓ | 7/7 |
| Zig | ✓ | 7/7 |
| Mojo | ✓ | ref |
| Verilog | ✓ | manual |
| VHDL | ✓ | manual |
| JavaScript | ✓ | live |
| TypeScript | ✓ | 5/5 |

## ✦ The educational root

Every port points back to the [Quilt Charter](https://github.com/SuperInstance/quilt-claude-charts/blob/main/QUILT_CHARTER.md) — the educational root document.

## ✦ See also

- [The Quilt Charter](https://github.com/SuperInstance/quilt-claude-charts/blob/main/QUILT_CHARTER.md)
- [quilt-claude-charts](https://github.com/SuperInstance/quilt-claude-charts) — protocol + 3 charts
- [AI-Writings](https://github.com/SuperInstance/AI-Writings) — the canon (230+ papers)
- [live-canon.superinstance.dev](https://live-canon.superinstance.dev) — the live worker
- [quilt-cowboy](https://github.com/SuperInstance/quilt-cowboy) — the writers' room

## ✦ License

Apache-2.0. Free as in freedom.
