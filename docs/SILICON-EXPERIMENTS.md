# SILICON-EXPERIMENTS — measured synthesis + simulation at scale (2026-08-30)

The red team's sharpest hit was "verified once, by hand, at toy scale."
This lane answers with numbers measured in one session on the local box
(RTX 4050 host, WSL2). Every number below was produced by the quoted
commands THIS session; logs live in `synth/*silicon*` (regenerable,
gitignored) and `sim/vlt/scale-run.log` (committed evidence).
Toolchain: yosys 0.47+22, nextpnr-ice40 0.7-131, verilator 5.029
(oss-cad-suite), iverilog 13.0 (dev). iverilog is the functional lane;
verilator is the scale lane.

**Provenance (multi-lane tree, see docs/INCIDENTS.md):** this lane was
mid-debug when an adjudication lane snapshotted it as WIP 9300092 / a
referee bench-committed an earlier partial state as 0eb231b and wrote
this file's first version. The lane did not die; it completed. §0 below
preserves the referee's adjudications verbatim-in-substance; §1-5 are
the FINAL verified results and supersede the referee's interim numbers
(its "UP5K 98.9% fit" was the NCELL=2 HX8K run mislabeled — 7,680 LC is
HX8K capacity; see §1 for the true sg48 picture). Final bench re-run
twice from cold after tree reconciliation: identical PASS both times.

## 0. Adjudications (devil-nudge lane, preserved)

**XFER_TIMEOUT storms — ADJUDICATED: bench artifact over a real event.**
The ~4,096-cycle periodicity was the bench's own xfer timeout constant;
underneath it a REAL fabric-wide ring deadlock at cyc≈34.5k (cell 3
state=13, full inbuf, ring heads dst=3/dst=f, counters frozen). The
lane subsequently root-caused that deadlock into TWO RTL bugs (fixed,
§3 F1/F2) plus one architectural limit (§3 F3) — the adjudication's
"next lane's job" is done and documented below.
**P4 HASH-SENSE — ADJUDICATED: vacuous corpse-hashing.** The old hash
compared three identically-dead states. The final bench hashes live
egress streams instead (§3 determinism) and carries a liveness guard.

## 1. SYNTH — the canonical core vs the smallest UP5K (sg48)

Config: the Makefile `synth` target's PnR-converged top — `q_fabric_top`,
engine params K=4 B=4 AGEW=8, NCELL=2, EDGES_N=1, PIPE_EFF=1 (the exact
parameters of the committed HX8K bitstream and the conservation proof).

```
yosys -s synth/fpga-converged.ice40          # 6002 SB_LUT4, 2434 FF
nextpnr-ice40 --up5k --package sg48 \
  --json synth/fabric2_k4b4a8e1_ice40.json --freq 12 \
  --timing-allow-fail --pcf-allow-unconstrained
```

**Result: FIT-FAIL, twice over.** ICESTORM_LC 7596/5280 (**143%**) and
SB_IO 157/96 (**163%**); placement dies with "no BELs remaining
(ICESTORM_LC)" (synth/pnr_silicon_up5k_k4b4a8e1.log). The headline:
*the canonical parallel fabric does not fit the smallest UP5K package on
either axis* — logic AND pins. BRAM: 0 SB_RAM40 anywhere in the design
(dialfiles/engine state map to FFs+LUTRAM; state pays area, not memory).
For the record the same netlist on HX8K-CT256 closes at ~98% LC,
~40-44 MHz (synth/report_k4b4a8e1.json, prior rounds).

The smallest thing that DOES close on sg48 — the serialized front-end
(`q_serfabric_top`, SER_BOOT_QUF=0, NCELL=1, same engine params):

```
yosys -p "read_verilog <fabric rtl + serdes>; chparam -set K 4 -set B 4 \
  -set AGEW 8 q_cell; hierarchy -check -top q_serfabric_top \
  -chparam NCELL 1 -chparam EDGES_N 1 -chparam SER_BOOT_QUF 0; \
  synth_ice40 -top q_serfabric_top -abc2 -json synth/silicon_up5k_serf_n1.json"
nextpnr-ice40 --up5k --package sg48 --json synth/silicon_up5k_serf_n1.json \
  --freq 12 --timing-allow-fail --pcf-allow-unconstrained --asc ... --report ...
```

**3221 LUT4 / 1479 FF / 4232/5280 LC (80.2%) / 37 IO / fmax 16.78 MHz**
(PASS at the 12 MHz target; bitstream packed). One cell + narrow port is
the honest sg48 ceiling today. Full table: `make synth-report` →
`synth/silicon.tsv` (synth/silicon.sh, ~4 min). NOTE: the simulation
fabric below is 15 cells — no iCE40 device in the drawer holds it
(15 cells ≈ 45k LUT4 est., ECP5 25F territory per synth/scale.tsv).

## 2. SCALE SIM — a million cycles on the largest legal fabric

Largest legal = what the parameters admit: AIDW=4 caps ids at 0..15 and
EXTID=0xF owns one, so **NCELL=15**; EIW=2 (q_cell default, not exposed
by the top) caps **EDGES_N=4**; engines at q_cell defaults **K=8, B=8,
AGEW=24** (the widest config in the tree — wider than the bitstream's).

```
verilator --cc --build --exe -j 4 --top-module q_fabric_top \
  -GNCELL=15 -GEDGES_N=4 --public-flat-rw -Mdir sim/vlt/obj_scale \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
  <11 fabric rtl files> sim/vlt/tb_scale_vlt.cpp     # or: make sim-scale
```

Phase P1: **1,000,000 cycles, ~10% effect rate** (5,814 of 58,080
injected flits; host windows ≤12 outstanding views):

- wall **11.0 s** (0.09 Mcyc/s sim rate, includes always-on per-cycle
  ledger/trace instrumentation — the bench IS its own checker)
- **58,431 ops accepted** at cell cores (5,866 effects, 52,275 views);
  4,042 ticks × 15 cells = 60,630 decay sweeps; 52,560 core emissions
  (55 fires); 52,393 flits drained at the io port
- **cell-ops = 171,621 → 15,574 cell-ops/sec** (accepts + tick sweeps +
  emissions — the fabric's own service throughput under mixed load)
- **conservation: 0 violations in 2,852,899 total cycles.** The LEDGER
  checker is the runtime form of the formal A1/T1 ledger
  (formal/f_fabric_conservation.v): cum(io_injected + core_emitted) −
  cum(core_accepted + io_drained) == pipes occupied, checked every 256
  cycles and exactly zero at every clean quiesce — it held through every
  phase INCLUDING the wedged states of §3 F3.

## 3. STRESS FINDINGS — two RTL bugs (fixed), one architectural limit

**F1 commissioning wedge (RTL, FIXED — q_cell_core ST_RESP).** Any
non-bind flit delivered to an unbound cell (e.g. a link ACK from a peer
commissioned earlier) kicked it ST_UNB → ST_RESP → ST_IDLE with bound=0,
after which every bind executed as a dial write AND ACKED SUCCESS —
silent misconfiguration; the cell NAKs views forever. Found at scale
(cells 1-14 all `bound=0` after a fully-acked setup), reproduced
minimal on iverilog AND verilator (tb/tb_wedge_repro.v, now in the TB
suite). Fix: return to ST_UNB while unbound. Suite 19/19.

**F2 ringport flit cloning (RTL, FIXED — q_link_ringport transit).** A
HIT flit blocked by a full ingress buffer satisfied `transit` while
`ri_ready` held the original in the upstream slice: the ringport PUSHED
A COPY downstream every stalled cycle. Measured by the bench's
ENTRY-IDENTITY trap (per-pipe push/pop witnesses): ring(push−pop)=2
with io_li+cell_li=1 — one phantom entry per stall cycle; the ring
filled with clones and the ledger broke by exactly the clone count.
This is the mechanism under the referee's adjudicated "net≠occ"
sub-issue #1a — resolved: neither undercount nor invisible pipes; the
fabric was manufacturing flits. Fix: `transit = ri_valid && !hit` (hold
at the slice head, per the unit-TB contract "stalls ring, no ro
progress"). Suite 19/19.

**F3 saturation deadlock (ARCHITECTURAL, NOT FIXED — the honest wall).**
No end-to-end flow control. Mixed traffic with effects — whose fire
fanout is fabric-internal traffic no host window can throttle —
eventually wedges the ring in a cyclic wait (egbuf→ring→inbuf→core→
egbuf across cells). Measured: P1's drain left 11 flits permanently
stuck (occ=11, ledger intact, QUIESCE-DEADLOCK line in scale-run.log);
view latency exceeded 8192 cycles 10 times (ACKLAT-TRIP lines) before
that; earlier fire-prone configurations froze mid-run at occ=23-26.
Conservation survives; liveness does not. Fix direction: admission
control / credits on inject (design work, deliberately not patched in
this lane — the referee's no-blind-fixes rule applies to architecture
too).

**Reset mid-pipeline (PASS).** 15 flits held in pipes (egress drain
gated off), rst_n asserted 16 cycles under load: post-release residue
0, ledger rebased clean, full re-commissioning + 50k-cycle recovery
pass CLEAN (errors +0).

**Determinism (PASS).** Same-seed full runs (reset → commission → 100k
traffic) reproduce the egress stream bit-exactly: FNV-1a-64 over the
ordered (op,dst,dat) of all drained flits = 2126a3c74072d7ff twice
(49,968 flits each); different seed → 2b25401359ce0215. This replaces
the task's suggested QUF round-trip variant honestly: v1 has no RTL
unload sink (q_serfabric_top header), so replay-hash is the equivalent
at this scale.

## 4. Incident note

Mid-session, an adjudication lane snapshotted this lane's in-flight
bench (9300092), a referee bench-committed an earlier partial state and
wrote this file's first version (0eb231b), and a rescue lane stashed
the lane's trace-gating edits; one rebuild from the mid-revert tree
produced a spurious failing run. After reconciliation the final bench
was re-run twice from cold: identical PASS (2,852,899 cycles, errors=0,
acklat_trips=10). Full story: docs/INCIDENTS.md.

## 5. Re-run everything

```
make test          # 19/19 iverilog TBs (wedge repro is a permanent guard)
make sim           # 34/34 python QUF lane
make synth-report  # E1: fresh sg48 numbers -> synth/silicon.tsv (~4 min)
make sim-scale     # E2+E3: build + run the scale bench (~2 min + build)
```
