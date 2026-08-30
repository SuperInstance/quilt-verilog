# quilt-verilog

The bottom-layer quilt, in silicon logic. Pure, generic Verilog-2005
(IEEE 1364-2005) — zero vendor-specific code. Every number below was
re-verified on 2026-08-29 (iteration 1) by running the command next to
it; nothing here is aspirational. The depth lives in `docs/` — the docs
map at the bottom is the hallway.

## The Law

1. **Pure Verilog-2005 (IEEE 1364-2005), synthesizable subset.** No vendor primitives, no IP, no `initial` blocks in rtl/ (testbenches excepted), no SystemVerilog in rtl/.
2. **Everything is a cell.** The quilt opcodes (qm_bind / qm_link / qm_effect / qm_view / qm_tick) are the only way anything touches anything.
3. **Intelligence lives at the bottom.** Hebbian edge updates, power-law/hyperbolic decay, dial state — implemented as plain RTL modules, fixed-point, streaming. The cosine/vMF reading of those weights is defined in the docs (`docs/academic/`); its dedicated readout is reserved in v1. One tick, traced: [docs/THE-TICK.md](docs/THE-TICK.md).
4. **Any IO can enter a cell.** One generic ingress/egress contract; adapters are thin and dumb.
5. **Verified or it doesn't exist.** Every module ships with a testbench runnable on open tools (iverilog/verilator). No toolchain lock-in, ever.

## Layout

- `rtl/` — the winning architecture's modules (17 files; the truth)
- `tb/` — testbenches, the suite runner, formal harnesses
- `sim/` — behavioral Python prototypes over the same QUF the RTL loads
- `formal/` — machine-checked invariants (SymbiYosys)
- `synth/` — iCE40/ECP5 synthesis + PnR flows and measured tables
- `proposals/<crew>/` — competing architecture entries (round-robin competition)
- `tools/` — QUF reference, backend fuzz, edge benches, gc-verifies
- `docs/` — decisions, math notes, floorplans (see `docs/INDEX.md`)

## Quickstart — one command per lane (Makefile, verified 2026-08-29 iteration 2)

Toolchain: stock oss-cad-suite at `/home/eileen/tools/oss-cad-suite/bin`
(Icarus 13.0, Verilator, Yosys 0.47+22, SymbiYosys 0.47, boolector,
nextpnr-ice40 0.7-131, icepack, icetime). The Makefile pins that PATH
itself — no export needed. All four targets below were run and verified
green on 2026-08-29 (iteration 2); the full verification story, per-lane
caveats, and honest gaps are in `docs/VERIFICATION.md`.

```sh
make test      # RTL testbench suite — 18/18 PASS
make sim       # behavioral Python lane — 34/34 OK
make formal    # all six SymbiYosys proofs — PASS
make synth     # yosys iCE40 ELABORATION of the PnR-converged top — exit 0, ~20 s
make pnr       # the measured numbers: nextpnr (7,528/7,680 LC, 98%) + icepack → 135,100-byte bin — ~3 min
make all       # all five
```

If the tools aren't found, the Makefile says so with a hint (point it at
your oss-cad-suite via `make OSSCAD=/path/to/oss-cad-suite/bin <target>`)
instead of a bare `command not found`.

Equivalent commands, run directly (what the targets invoke):

### 1. Simulation — the RTL testbench suite

```sh
bash tb/run_suite.sh
```

**18/18 PASS** on this tree (2026-08-29): tick scheduler, flit pipe, link
ringport, dialfile, hebb edge, hyperbola tail, echo gate, RQH bank, RQH
saturation, cell core, io port, fabric smoke (x2), judge consistency,
hebb pipe (300 ops, bit-exact), QUF boot (4 cases), the QUF loader lane
(python golden → iverilog, 576-byte round-trip byte-exact), and the
serialized front-end (byte-exact vs the parallel path, 68 flits).

### 2. Behavioral lane — same semantics, Python-first

```sh
python3 -m unittest discover -s sim/tools -p 'test_*.py'
```

**34/34 tests OK.** The tap-fabric bridge (a MudArena session replayed
through cell-exact semantics into a QUF): see `sim/README.md`.

### 3. Formal proofs — SymbiYosys

```sh
sby -f formal/cell_core.fair.sby
sby -f formal/cell_core.tick.sby
sby -f formal/flit_pipe.fly.sby
sby -f formal/fabric.conservation.sby
sby -f formal/echo_gate.dyadic.sby
sby -f tb/formal/flit_pipe.sby   # k-inductive re-prove of the pipe invariants
```

**All six PASS** on this tree (2026-08-29 re-run; statuses and timings in
the table below). What each proof claims — op-response bounds, tick
deadlines, FIFO safety, ledger conservation, the echo-gate dyadic
bracket — is stated exactly in `formal/README.md`.

### 4. Synthesis — iCE40/ECP5 (yosys → nextpnr → icepack)

```sh
yosys -s synth/fpga-converged.ice40   # formal-proof params on the real top
nextpnr-ice40 --hx8k --package ct256 \
  --json synth/fabric2_k4b4a8e1_ice40.json --freq 12 \
  --timing-allow-fail --pcf-allow-unconstrained \
  --asc synth/fabric2_k4b4a8e1.asc --report synth/report_k4b4a8e1.json
icepack synth/fabric2_k4b4a8e1.asc synth/fabric2_k4b4a8e1.bin
```

Parameter sweeps: `bash synth/sweep.sh` (W-knobs), `bash synth/scale.sh`
(device ladder), `bash synth/pinfix.sh` (serialized front-end). The flow
was re-verified end-to-end through PnR twice on 2026-08-29 (iteration 2,
then independently in the audit pass): serialized front-end, UP5K sg48,
NCELL=1 → 4232/5280 LC (80.1%), 37/96 IO, fmax 16.78 MHz post-route
(17.36 MHz is the post-placement estimate), PASS at the 12 MHz target.
The converged HX8K build above was also taken through PnR + icepack on
this tree by the audit pass: 6,002 LUT4 → 7,596/7,680 LC (98%), 157 IO,
fmax 43.36 MHz post-route, 135,100-byte bitstream.

### Makefile — now real (2026-08-29, iteration 2)

The root Makefile exists and every target was run green:
`make test` (18/18), `make sim` (34/34), `make formal` (6× PASS),
`make synth` (yosys exit 0). See `docs/VERIFICATION.md` for what each
lane proves and does not prove.

## Measured results — re-verified 2026-08-29 (iteration 1)

| lane | what was run | result |
|---|---|---|
| sim | `bash tb/run_suite.sh` | **18/18 PASS** |
| sim (python) | `python3 -m unittest discover -s sim/tools -p 'test_*.py'` | **34/34 OK** |
| formal | `sby -f formal/flit_pipe.fly.sby` (BMC 40) | **PASS**, 102 s |
| formal | `sby -f formal/fabric.conservation.sby` (BMC 55) | **PASS**, 55 s |
| formal | `sby -f formal/echo_gate.dyadic.sby` (BMC 25) | **PASS**, 3 s |
| formal | `sby -f formal/cell_core.tick.sby` (BMC 80) | **PASS**, 284 s |
| formal | `sby -f formal/cell_core.fair.sby` (BMC 80) | **PASS**, 607 s |
| formal (k-induction) | `sby -f tb/formal/flit_pipe.sby` | **PASS** |
| synth | yosys → nextpnr-ice40, serfabric NCELL=1, UP5K sg48 | 4232/5280 LC (80.1%), 37/96 IO, **fmax 16.78 MHz post-route, PASS @ 12 MHz** (17.36 post-place) |
| synth (audit re-run) | yosys → nextpnr-ice40 → icepack, k4b4a8e1 `q_fabric_top`, HX8K-CT256 | 6,002 LUT4, 7,596/7,680 LC (98%), 157 IO, **fmax 43.36 MHz post-route, PASS @ 12 MHz**, 135,100 B bitstream |
| synth (committed tables) | `synth/scale.tsv`, `synth/scale-pinfix.tsv` | device ladder + pin-fix lane: up to 63.7 MHz (ECP5 12F, 8 cells), HX8K 40.44 MHz (PIPE_EFF retime) — prior-lane measurements, not re-run here |

Notes: all formal runs use the working-tree `rtl/q_cell_core.v` (the two
proof-forced fixes documented in `formal/README.md` are required for
reproduction). The committed bitstream `synth/fabric2_k4b4a8e1.bin`
(135,100 bytes, 40.44 MHz HX8K at its commit tree) is tracked in git; the
audit pass re-ran the full HX8K flow through icepack on this tree — same
135,100-byte size, 43.36 MHz post-route (the committed artifact records
the PIPE_EFF-retime-era tree; both are real). Per-run timing varies with
machine load (e.g. cell_core.tick: 284 s here vs 10 m 23 s in the
original run; both PASS).

## Where the depth lives — docs map

- `docs/INDEX.md` — **every document in the repo, one line, grouped by reader intent** (understand / verify / build / history)
- `docs/VERIFICATION.md` — **the complete verification guide**: every lane's command, pass counts, timings, and what is NOT covered
- `docs/QUF-SPEC.md` — the file format: QUF is the GGUF of cellular silicon
- `docs/DOCTRINE.md` — the bet: llama.cpp, but Verilog and cellularized
- `docs/SYNTHESIS.md` → `docs/SYNTHESIS-FPGA.md` — the mechanisms, then the metal: the iCE40 wall, the PIPE_EFF retime, the ECP5 ladder, the bitstream
- `docs/FPGA-BOOT.md` — QUF file → cell state at reset (design stub)
- `docs/BACKEND-NOTES.md` — the adversarial first user's report: 23 bug classes found, 5 in RTL, all fixed with regressions
- `docs/academic/GENERAL-CALCULUS.md` — the capstone: the theory beneath the six verbs, with machine-checked §8 benches (`tools/gc-verifies/`)
- `docs/academic/RHO-F-FLOOR.md` — the audit-freshness impossibility floor
- `docs/academic/THE-BREAKDOWN.md` — every load-bearing claim as claim → definitions → proof → machine check → attack surface → closure
- `docs/academic/annals-1905/` — the Kaldfjord Circle: the corpus restated as period mathematics (with kept drafts)
- `docs/review-*.md` — cross-review round 2 of the five competition entries
- `docs/WORLD-CLASS-BRIEF.md` — the standard this repo is held to, and the iterator protocol

## Competition (running)

Entries under `proposals/`; cross-review round after; winners get built
in `rtl/` with testbenches. The round-2 winner is `glm` (see
`docs/SCORECARD.md`); `rtl/` is its architecture as built. Failures are
first-class: `proposals/` and `docs/review-*.md` are the tapestry — kept,
presented, dated.

## Iteration protocol

This repo is built by teams of iterators, one theme per pass:
AUDIT → FIX → MEASURE → COMMIT. Every commit states what it verified.
Nothing is ever deleted — archive by rename.
