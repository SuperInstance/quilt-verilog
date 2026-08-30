# VERIFICATION — what is proven, how to run it, and what is not

Every number on this page was measured by running the command shown, on this
tree, by the iteration named in the table. If you cannot reproduce a number,
that is a bug in this document.

## How to run everything

Toolchain: stock oss-cad-suite (Icarus 13.0, Yosys 0.47+22, SymbiYosys,
boolector, nextpnr-ice40 0.7-131, icepack, icetime) at
`/home/eileen/tools/oss-cad-suite/bin`. The root Makefile pins that path
itself; you do not need to export anything.

```sh
make test      # RTL testbench suite (iverilog)          — ~1-2 min
make sim       # behavioral Python lane (unittest)       — seconds
make formal    # all six SymbiYosys proofs               — see timings below
make synth     # yosys elaboration of the iCE40 top      — ~20 s
make all       # all four, in that order
```

All four targets were run and verified green on 2026-08-29 (iteration 2).
`make clean` removes generated proof dirs and `tb/run` artifacts (sources
untouched).

## Lane 1 — `make test`: the RTL testbench suite

Run: `bash tb/run_suite.sh` (the Makefile target). 18 testbenches compiled
with `iverilog -g2005` and executed; a PASS banner in the output is required
for each. What the suite proves, per bench:

- **tb_tick_sched / tb_flit_pipe / tb_link_ringport** — scheduler spacing,
  FIFO no-loss/no-reorder, ring-port handoff.
- **tb_dialfile / tb_hebb_edge / tb_hyperbola_tail** — dial storage, the
  Hebbian edge update, and the power-law decay tail, against golden values.
- **tb_q_echo_gate / tb_q_rqh_bank / tb_rqh_saturation** — echo-gate
  bracketing, RQH deposits, and saturation behavior (with `rtl/q_hebb_rqh.v`).
- **tb_cell_core / tb_io_port** — per-cell op FSM and the generic IO port.
- **tb_fabric_smoke / tb_fabric_smoke_v2** — whole-fabric train→fire→decay
  and echo-gate+RQH paths, max latency 31 cycles.
- **tb_judge_consistency** — UF-loader judge consistency (with
  `rtl/q_uf_loader.v`).
- **tb_hebb_pipe** — 300 pipelined ops, act/trace bit-exact at every checkpoint.
- **tb_quf_boot** — 4 boot cases: warm start, corrupt header, truncation,
  epoch latch.
- **tb_quf_loader lane** — Python golden builds a 576-byte QUF, iverilog
  loads it, round-trip byte-exact.
- **tb_serfabric** — serialized fabric front-end: serial vs parallel boot and
  egress streams byte/cycle-exact (68 flits), fail-static gate mode.

**Result (2026-08-29, iteration 2): 18/18 PASS** (same tree as iteration 1's
recorded 18/18).

## Lane 2 — `make sim`: the behavioral Python lane

Run: `python3 -m unittest discover -s sim/tools -p 'test_*.py'`.

**Result (2026-08-29, iteration 2): 34 tests, all OK**, runtime under a
second. This lane proves the Python tap-fabric bridge carries the same
semantics as the RTL lane over the same QUF container — it is a model check,
not a hardware proof.

## Lane 3 — `make formal`: SymbiYosys proofs

Six proofs (five in `formal/`, one k-induction harness in `tb/formal/`).
Exact invariants, environment assumptions, and the two RTL defects the
proofs forced are documented in `formal/README.md` — read it before trusting
any number here. Summary:

| proof | invariant (short) | mode/depth | verdict |
|---|---|---|---|
| `flit_pipe.fly.sby` | FIFO safety + value integrity (no loss/dup/reorder) | BMC 40 | PASS |
| `fabric.conservation.sby` | 2-cell ledger conservation, no silent drops | BMC 55 | PASS |
| `echo_gate.dyadic.sby` | dyadic octave bracket, PRIORITY, MONO, ZEROABSORB | BMC 25 | PASS |
| `cell_core.tick.sby` | tick suppression + service deadlines under flood | BMC 80 | PASS |
| `cell_core.fair.sby` | op-response bounds I1a/I1b/I2 | BMC 80 | PASS |
| `tb/formal/flit_pipe.sby` | k-inductive re-prove of pipe invariants | prove, depth 15 | PASS |

Measured on this machine, iteration 2 (2026-08-29, `make formal` re-run):

| proof | verdict | measured wall time (iter 2) |
|---|---|---|
| `cell_core.fair.sby` (BMC 80) | PASS | 498 s |
| `cell_core.tick.sby` (BMC 80) | PASS | 215 s |
| `flit_pipe.fly.sby` (BMC 40) | PASS | 72 s |
| `fabric.conservation.sby` (BMC 55) | PASS | 38 s |
| `echo_gate.dyadic.sby` (BMC 25) | PASS | 3 s |
| `tb/formal/flit_pipe.sby` (prove) | PASS | <1 s |

Total ~14 min. For comparison, iteration 1 same-day runs of the same
proofs: 607 s / 284 s / 102 s / 55 s / 3 s — wall time varies with machine
load; the verdicts are the stable fact.

Important scope notes (from `formal/README.md`): all bounded-liveness claims
are assert-within-N in BMC mode; **unbounded liveness is not claimed**. The
proofs hold under the environment contracts E1–E4 listed there (each weaker
than the real system's behavior — e.g. E2's 12-cycle engine bound vs the
real q_hebb_edge's 10). The conservation proof uses shrunk parameters
(EDGES_N=1, K=4, B=4, AGEW=8), not the full fabric.

## Lane 4 — `make synth`: iCE40 elaboration

Run: `yosys -s synth/fpga-converged.ice40` — the PnR-converged k4b4a8e1
config (the formal conservation proof's parameters) on the real
`q_fabric_top`.

**Result (2026-08-29, iteration 2): exit 0, ~20 s**, 6002 SB_LUT4, 898
SB_CARRY, ~2430 FF-class cells, 157 port bits — consistent with the committed
`synth/stat_fabric2_k4b4a8e1.txt`. `make synth` covers elaboration only;
the full PnR + bitstream flow (nextpnr-ice40 → icepack, commands in README
§4) was verified end-to-end in iteration 1: UP5K sg48 NCELL=1 → 4232/5280 LC
(80.1%), fmax 17.36 MHz, PASS at the 12 MHz target. The committed bitstream
`synth/fabric2_k4b4a8e1.bin` (HX8K, 40.44 MHz) is tracked in git.

## What is NOT covered — read this before relying on the quilt

- **No on-hardware test.** Every result above is simulation, formal, or
  synthesis. No board bring-up has been done; the bitstream is untested on
  metal. No PCF exists yet (IO is auto-placed, `--pcf-allow-unconstrained`).
- **Unbounded liveness is unproven.** BMC proofs bound violations within
  their depth; they are not k-induction certificates (except the one
  `tb/formal/flit_pipe.sby` prove run). Fair/tick proofs rely on E1–E4
  environment contracts, which are stated, not proven from the RTL above
  the cell.
- **Formal params are shrunk.** Conservation is proven at EDGES_N=1, K=4,
  B=4, AGEW=8 — not at the shipped fabric's scale.
- **The Python lane is a model, not a miter.** No formal equivalence proof
  between Python semantics and RTL exists.
- **PnR timing depends on unconstrained IO.** fmax numbers come from
  nextpnr with auto-placed pins; a real PCF could change them.
- **No CI.** Verification runs when an iterator runs it; nothing prevents
  regressions between commits except the discipline of running these
  targets. (Open lane.)

## History of verification runs

| date | iteration | what ran | result |
|---|---|---|---|
| 2026-08-29 | 1 | suite + python + 6 proofs + PnR through UP5K | 18/18, 34/34, 6×PASS, 17.36 MHz fmax |
| 2026-08-29 | 2 | `make test/sim/synth` + `make formal` (all six re-run) | 18/18, 34/34, 6×PASS, yosys exit 0 — one-command front door verified |
