# USER GUIDE — building, loading, and watching a quilt fabric

*The hands-on manual: how to run the fabric, how a QUF file is put
together byte by byte, how to boot it, and how to read what comes back.
Written 2026-08-30 against tree `ccff448`; every command and every
output below was run on this tree. Theory lives in
[THE-TICK.md](THE-TICK.md); proofs in [VERIFICATION.md](VERIFICATION.md);
the format spec in [QUF-SPEC.md](QUF-SPEC.md). Tutorials with runnable
code: [TUTORIALS.md](TUTORIALS.md) + `examples/`.*

## 0. The 60-second mental model

A quilt is a **ring of cells**. Each cell is a small fixed-point
machine with:

- **16 dials** (`q_dialfile`) — named parameters: threshold, leak rate,
  refractory period, ladder half-life, ... all `u16`, most read as
  **Q1.15** signed fixed point (`0x6000` = 0.75, `0x3800` = 0.4375).
- an **activation register `act`** — the cell's buzz. Effects push it
  up; every **tick** leaks it down (`act −= act >>> KA`).
- up to **EDGES_N learned edges** (`q_hebb_edge`) — an edge is *not a
  wire*: it lives in the **hearing** cell, keys on a peer id, and is a
  tiny weight bank (an 8-bucket Hebbian ladder by default) that trains
  on cofires and decays on ticks.

Exactly **five opcodes** touch anything (`q_cell_core.v`):

| op | name  | operands (flit fields)                      | returns |
|----|-------|---------------------------------------------|---------|
| 0  | bind  | first: `a0` = cell id. later: dial `a0[3:0]` ← `a1` | ACK |
| 1  | link  | `dst` cell's slot `a0[EIW-1:0]` := {peer=`src`, base=`a1`} | ACK (to the peer) |
| 2  | effect| `src` → `dst`, payload `dat` (Q1.15)        | silent (unless a fire follows) |
| 3  | view  | `dst`=cell, `a0[1:0]`: 0=`act` 1=wsum(edges) 2=dial `a1[3:0]` | ACK with `dat`=value |
| 4  | tick  | *consumed, no action* — real ticks come from the scheduler | — |

Time is not an op you send: the tick scheduler (`q_tick_sched`)
free-runs and strobes **one tick every 2^TPW clock cycles** (TPW=4 →
every 16 cycles). One tick = decay every edge, leak `act`, fire-test.
If `act ≥ THRESH` and the refractory counter is clear, the cell
**fires**: `act` resets to 0 and one effect flit fans out to every
linked peer. That loop — integrate, leak, fire — is the whole
computation ([THE-TICK.md](THE-TICK.md) traces one tick through the
RTL, register by register).

Responses are ring traffic like anything else (Law 2): an ACK rides
the ring from the answering cell to the external id (`EXTID`, 0xF) and
you consume it with the same valid/ready handshake.

## 1. Build and run the fabric

**Toolchain**: stock [oss-cad-suite](https://github.com/YosysHQ/oss-cad-suite-builds)
(Icarus 13.0, Yosys 0.47+, SymbiYosys, boolector, nextpnr-ice40). The
root Makefile pins `/home/eileen/tools/oss-cad-suite/bin`; override
with `make OSSCAD=/path/to/bin <target>`.

```sh
make test      # 18 RTL testbenches (iverilog)        — expect 18/18 PASS
make sim       # behavioral Python lane               — expect 34/34 OK
make formal    # six SymbiYosys proofs                — ~14 min
make synth     # yosys iCE40 elaboration of the top   — ~20 s
make pnr       # nextpnr-ice40 + icepack bitstream    — ~3 min
```

(Counts and timings as measured in [VERIFICATION.md](VERIFICATION.md);
re-run them yourself — that document's rule is that every number is
reproducible or it's a bug.)

There is no separate "build the fabric" step for simulation: a
testbench *instantiates* `q_fabric_top` and iverilog compiles the RTL
list (see any `examples/*/run.sh` or `tb/run_suite.sh` for the file
list — eleven `.v` files). For FPGA, `make synth` / `make pnr` take it
to an iCE40 bitstream.

## 2. Three doors into a running fabric

### 2.1 The parallel flit port — `q_fabric_top`

The direct door: a 75-bit flit contract (`i_op/i_src/i_dst/i_a0/i_a1/
i_a2/i_dat` + `i_val/o_rdy` ingress; mirrored egress) into a ring of
`NCELL` cells.

```verilog
q_fabric_top #(.NCELL(2), .TPW(4)) dut (
    .clk(clk), .rst_n(rst_n),
    .i_val(i_val), .o_rdy(o_rdy),
    .i_op(i_op), .i_src(i_src), .i_dst(i_dst),
    .i_a0(i_a0), .i_a1(i_a1), .i_a2(i_a2), .i_dat(i_dat),
    .o_val(o_val), .i_rdy(i_rdy_t),
    .o_op(o_op), .o_src(o_src), .o_dst(o_dst),
    .o_a0(o_a0), .o_a1(o_a1), .o_a2(o_a2), .o_dat(o_dat),
    .o_ovf(ovf));
```

House driving pattern (copy it from `tb/tb_fabric_smoke.v` or
`examples/t1_first_fabric/`): assert `i_val` at `negedge`, wait for
`o_rdy`, deassert with a non-blocking assign right after the transfer
edge; consume each response by pulsing `i_rdy` for one cycle when
`o_val` is high.

**Cell ids are 0..NCELL-1 — the node at ring position NCELL is the
IO port, not a cell.** Binding "cell NCELL" silently disappears into
the IO node; this is the #1 first-day gotcha (it bit this guide's own
tutorial author).

### 2.2 The serialized byte port — `q_serfabric_top`

The same fabric behind **8 pins**: three phases over one byte stream
(`i_sval/i_sbyte/o_srdy` in, `o_stx_val/o_stx` out):

- **BOOT** — the bytes are a QUF container (default
  `SER_BOOT_QUF=1`): one `quf_boot` per cell on the *same broadcast
  stream*, each picking its own dial row and edge records out of the
  section payloads. When the stream ends (`i_eod`), `o_boot_ok`
  pulses, the epoch (`tpw`) latches **once**, and the fabric releases.
  In gate mode (`SER_BOOT_QUF=0`, for packages where the parser does
  not fit) the host parses the QUF itself and streams dials as
  `qm_bind` flits; a 2-byte release word `0x51 0x46` commissions the
  fabric instead.
- **RUN** — bytes are flits, **10 bytes per flit**, most-significant
  byte first (`byte[0]` = header `{op,src,dst}`, ... `byte[9]` = pad,
  driven zero on egress).
- **ERROR** — any boot error parks the FSM sticky in `HOLD_ERR` with
  the fabric frozen; recovery is power-on reset. Fail-static, never a
  half-booted fabric (`rtl/quf_boot.v` header, `docs/FPGA-BOOT.md`).

`tb/tb_serfabric.v` is the reference driver for both modes and the
differential check that the serial and parallel fronts are
flit-for-flit identical.

### 2.3 The Python lane — `tools/quf.py` + `sim/tools/tapfabric.py`

No simulator needed: build, inspect, verify, and warm-start QUF files
with `tools/quf.py` (stdlib only), and run whole cell graphs with
RTL-exact integer semantics through `sim/tools/tapfabric.py` (see
`sim/README.md`, `docs/TAP-FABRIC.md`). The Python lane is a *model
check*, not a hardware proof ([VERIFICATION.md](VERIFICATION.md), lane
2) — but its tick/edge arithmetic is defined bit-for-bit against the
RTL and differentially checked by the cosim harness.

## 3. QUF by hand: build a container and read it byte by byte

QUF is "the GGUF of cellular silicon": a flat, little-endian binary
holding the **complete state** of a quilt — dials, edges (with ladder
walk counts), routing, tick schedule. Full spec: [QUF-SPEC.md](QUF-SPEC.md).
This section builds a real one and walks every byte.

Start from the JSON "golden shape" (`examples/t3_quf_roundtrip/room.json`,
a 2-cell room whose single edge still carries the 10 ladder cofires
trained in Tutorial 2):

```json
{
  "header":  { "quf.version": "t3 tutorial 1.0", "edge.k": 8,
               "tick_period": 16, "quant.dials": "Q1.15",
               "quant.edges": "Q1.15", "quant.routing": "u8", "align": 32 },
  "dials":   [ [2048,128,6,12,5,24576,4,11469,20,0,64,2,0,0,8,8],
               [2048,128,6,12,5,14336,4,11469,20,0,64,2,0,0,8,8] ],
  "edges":   [ {"src":0,"dst":1,"mode":0,"slot":0,"base":4096,"wh":0,
                "age":0,"buckets":[10,0,0,0,0,0,0,0]} ],
  "routing": [ {"dst":0,"via":0}, {"dst":1,"via":1} ],
  "ticksched": { "tpw": 4, "phases": [0, 3] }
}
```

Build and inspect it (run these; the outputs below are the real ones):

```sh
$ python3 tools/quf.py create examples/t3_quf_roundtrip/room.json /tmp/room.quf
wrote /tmp/room.quf (544 bytes) + /tmp/room.quf.hex
$ python3 tools/quf.py verify /tmp/room.quf && python3 tools/quf.py info /tmp/room.quf
QUF VERIFY PASS: /tmp/room.quf (544 bytes)
QUF v1, 10 KV pairs, 4 sections
  quf.version    string t3 tutorial 1.0
  cell_count     u32    2
  edge_count     u32    1
  route_count    u32    2
  edge.k         u32    8
  tick_period    u32    16
  quant.dials    string Q1.15
  quant.edges    string Q1.15
  quant.routing  string u8
  align          u32    32
  section dials    kind=0 off=384    size=64
  section edges    kind=0 off=448    size=20
  section routing  kind=0 off=480    size=4
  section ticks    kind=0 off=512    size=12
```

### 3.1 The hexdump, walked

`xxd /tmp/room.quf` (544 bytes; section payloads begin at `0x180`):

```
00000000: 5155 4600 0100 0000 0100 0000 0a00 0000  QUF.............
00000010: 0b00 0000 7175 662e 7665 7273 696f 6e08  ....quf.version.
00000020: 0000 000f 0000 0074 3320 7475 746f 7269  .......t3 tutori
00000030: 616c 2031 2e30 0a00 0000 6365 6c6c 5f63  al 1.0....cell_c
00000040: 6f75 6e74 0400 0000 0200 0000 0a00 0000  ount............
00000050: 6564 6765 5f63 6f75 6e74 0400 0000 0100  edge_count......
00000060: 0000 0b00 0000 726f 7574 655f 636f 756e  ......route_coun
00000070: 7404 0000 0002 0000 0006 0000 0065 6467  t............edg
00000080: 652e 6b04 0000 0008 0000 000b 0000 0074  e.k............t
00000090: 6963 6b5f 7065 7269 6f64 0400 0000 1000  ick_period......
000000a0: 0000 0b00 0000 7175 616e 742e 6469 616c  ......quant.dial
000000b0: 7308 0000 0005 0000 0051 312e 3135 0b00  s........Q1.15..
000000c0: 0000 7175 616e 742e 6564 6765 7308 0000  ..quant.edges...
000000d0: 0005 0000 0051 312e 3135 0d00 0000 7175  .....Q1.15....qu
000000e0: 616e 742e 726f 7574 696e 6708 0000 0002  ant.routing.....
000000f0: 0000 0075 3805 0000 0061 6c69 676e 0400  ...u8....align..
00000100: 0000 2000 0000 0400 0000 0500 0000 6469  .. ...........di
00000110: 616c 7300 0000 0080 0100 0000 0000 0040  als............@
00000120: 0000 0000 0000 0005 0000 0065 6467 6573  ...........edges
00000130: 0000 0000 c001 0000 0000 0000 1400 0000  ................
00000140: 0000 0000 0700 0000 726f 7574 696e 6700  ........routing.
00000150: 0000 00e0 0100 0000 0000 0004 0000 0000  ................
00000160: 0000 0005 0000 0074 6963 6b73 0000 0000  .......ticks....
00000170: 0002 0000 0000 0000 0c00 0000 0000 0000  ................
00000180: 0008 8000 0600 0c00 0500 0060 0400 cd2c  ...........`...,
00000190: 1400 0000 4000 0200 0000 0000 0800 0800  ....@...........
000001a0: 0008 8000 0600 0c00 0500 0038 0400 cd2c  ...........8...,
000001b0: 1400 0000 4000 0200 0000 0000 0800 0800  ....@...........
000001c0: 0001 0000 0010 0000 0000 0000 0a00 0000  ................
000001d0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000001e0: 0000 0101 0000 0000 0000 0000 0000 0000  ................
000001f0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000200: 0400 0000 0000 0000 0300 0000 0000 0000  ................
00000210: 0000 0000 0000 0000 0000 0000 0000 0000  ................
```

**Fixed header — 16 bytes** (`0x000`–`0x00F`), §3 of the spec:

| bytes (LE)      | value          | meaning                        |
|-----------------|----------------|--------------------------------|
| `51 55 46 00`   | `'Q','U','F',0`| magic ("QUF\\0")               |
| `01 00 00 00`   | 1              | version (readers reject other) |
| `01 00 00 00`   | 1              | endian = little                |
| `0a 00 00 00`   | 10             | kv_count: 10 KV pairs follow   |

**KV pairs** (`0x010`–`0x0FF`), each `u32 name_len, name, u32
value_type, value`. Types are GGUF's numbering (`4`=u32, `8`=string).
Walking the first two:

- `0x010`: `0b 00 00 00` = name_len 11, then the 11 bytes `quf.version`
  (visible in the ASCII column), then type `08 00 00 00` (string), then
  a string value = `u32 len` (`0f 00 00 00` = 15) + 15 bytes
  `t3 tutorial 1.0`.
- `0x036`: `0a 00 00 00` = 10, `cell_coun`+`t`, type `04` (u32), value
  `02 00 00 00` = **2 cells**.

The remaining eight KVs encode `edge_count`=1, `route_count`=2,
`edge.k`=8 (ladder buckets), `tick_period`=16 (= 2^tpw, from
`ticksched.tpw`=4), the three `quant.*` strings, and `align`=32.
Header KVs the writer does not know are *skipped, never fatal* —
that rule is load-bearing for forward compatibility (§8).

**Section table** (`0x100`–`0x17F`): `u32 section_count` = `04`, then
per section `u32 name_len, name, u32 kind, u64 offset, u64 size`:

- `dials`, kind 0, offset `0x180` (384), size 64
- `edges`, kind 0, offset `0x1C0` (448), size 20
- `routing`, kind 0, offset `0x1E0` (480), size 4
- `ticks`, kind 0, offset `0x200` (512), size 12

Offsets must be multiples of `align` (32), strictly ascending,
non-overlapping. The zero bytes at `0x124`–`0x17F` are the padding
that pads the table end up to the first section.

**Payloads**, at exactly the advertised offsets:

- **dials** `0x180`: `cell_count × 16 u16 words`, row-major. Row 0
  (cell 0) reads (LE): `0x0800 0x0080 0x0006 0x000c 0x0005 0x6000
  0x0004 0x2ccd 0x0014 0x0000 0x0040 0x0002 0 0 0x0008 0x0008` —
  dial map per `q_dialfile.v`: ETA_F, ETA_S, KF, KS, KA, **THRESH
  (0x6000 = 0.75)**, REFR, COS_MIN, P0E, MODE, **HL (64 ticks)**, KLE,
  FLOOR, FTRACE, RQ, RQL. Cell 1's row differs only in THRESH
  (`0x3800` = 0.4375 — a more earnest cell).
- **edges** `0x1C0`: one record of `12 + edge.k` bytes:
  `00` src=0, `01` dst=1, `00` mode=0 (ladder), `00` slot=0,
  `00 10` base=0x1000, `00 00` wh, `00 00 00 00` age, then **K=8
  bucket bytes: `0a 00 ...`** — ten cofires parked in bucket 0: this
  file literally carries Tutorial 2's learned state.
- **routing** `0x1E0`: 2-byte records `(dst, via)`: `00 00`, `01 01`
  (single ring: via == dst).
- **ticks** `0x200`: `u32 tpw` = 4, then per-cell `u32 phase`:
  `[0, 3]` (carried for v2 metronome cells; v1 ignores them).

Trailing zeros pad the file to a multiple of `align` (544 = 17×32).

### 3.2 The digest KV (content pinning)

`quf.py create --digest` (or `quf.add_digest(doc)`) adds a
`quf.sha256` header KV hashing every section's *content* in table
order. With it, a flipped payload byte is refused by `verify` even
though the structure still parses — the difference between a corrupt
file that *looks* fine and one that fails loudly (this hardening came
from the fuzz lane; see `docs/BACKEND-NOTES.md`). Tutorial 3
demonstrates both refusals.

## 4. Load, run, observe

### 4.1 Load (boot)

Three loaders, one container:

- **Testbench word-stream** — `rtl/q_uf_loader.v` eats the QUF as
  16-bit little-endian words on the `q_io_port` handshake
  (`i_val/o_rdy/i_dat[15:0]`), writes the dial row of `i_mycell`,
  captures `edge.k`, fills edge/route RAMs, latches `tpw`, asserts
  `o_done`. `tools/run_quf_tb.sh` (python builds the file → iverilog
  loads it → byte-exact readback) is the runnable end-to-end.
- **Boot harness** — `rtl/quf_boot.v` wraps the loader with the boot
  FSM `POR → HOLD → LOAD → LATCH → RELEASE → RUN`: the fabric cores
  are held in reset while state lands, the tick epoch latches **once**
  at release (changing cadence mid-run is a spec change, refused by
  construction), and any error parks sticky in `HOLD_ERR` — POR is the
  only way out, and a failed boot leaves the POR dial defaults, never
  a half-image.
- **Serialized front-end** — `q_serfabric_top` BOOT phase broadcasts
  the same bytes to one `quf_boot` per cell (§2.2 above).

**Known v1 limit, on purpose**: the RTL loader restores dials, edge
*topology* (base weights), routing, and the epoch — but the ladder
walk state (`buckets`, `wh`, `age`) is *consumed but not restored*
(the `q_hebb_edge` engines have no load port in v1). A warm-started
fabric re-binds and trains the ladders back; full state restore is the
Python path (`tapfabric.py` round-trips buckets — Tutorial 3).

### 4.2 Run

Send ops (§0). Pacing: an effect occupies the hearing cell for ~10–20
cycles (train, K+1-cycle weight readout, integrate); views similar.
The fabric smoke benches pace effects ~48 cycles apart; faster is
fine — the ring's elasticity and the cell's backpressure handle it,
but your view responses will queue behind in-flight ops.

### 4.3 Observe

- **view(0)** — a cell's `act` (Q1.15). After one 0x4000-strength
  effect across a 0x1100-weight edge: `(0x1100×0x4000)>>>15 = 0x880`.
- **view(1)** — `wsum`: the saturating sum of the cell's edge weights.
  Fresh link with base 0x1000 reads 0x1000; each cofire adds 2^8
  (bucket 0 is priced at `2^K` with K=8); after 10 cofires: `0x1A00`.
- **view(2, dial)** — any dial word, live.
- **Egress capture** — every ACK/response is a flit on the egress
  port; log transfers (`o_val && i_rdy`) to see the fabric's chatter
  (Tutorial 1 prints each one).
- **Waveforms** — `$dumpfile/$dumpvars` and open the VCD in GTKWave;
  Tutorial 2's run leaves `out/t2_hebbian_edges.vcd` with the ladder
  decay visible in the wsum view responses.
- **Python** — `python3 tools/quf.py dump FILE` decodes every section
  to JSON; `tapfabric.py` renders whole-session transcripts.

Latency: view response latency on a live fabric is bounded (the smoke
benches measure max 31 cycles through the full ring path).

## 5. Reading refusal codes

Refusals are *loud and sticky* in every loader — the discipline is
fail-static: a bad container never boots a half-fabric.

**`q_uf_loader` / `quf_boot` `o_err`** (sticky, stops the load;
codes from QUF-SPEC §9, `E_TRUNC` from `quf_boot.v`):

| code | meaning                                              |
|------|------------------------------------------------------|
| 1    | bad magic (first 4 bytes not `QUF\0`)                |
| 2    | bad version (not 1)                                  |
| 3    | layout overrun (stream position passed a section offset) |
| 4    | bad endian word (≠ 1)                                |
| 5    | known KV (`edge.k`) present but not u32              |
| 6    | unknown value type / bad array element type          |
| 7    | nonzero u64 high word (offset or size ≥ 4 GiB)       |
| 8    | KV/section name longer than 255 bytes                |
| 9    | `edge.k` outside 1..16                               |
| 10   | truncated stream (boot harness end-of-data before done) |
| 11   | wrong commissioning word in gate mode (`0x51 0x46` expected — `tb_serfabric.v` case B) |

**Flit-level NAK (op 6)**: an op arriving at an *unbound* cell is
NAKed; `view` with `a0[1:0]=3` (the reserved cosine readout) NAKs in
v1. NAKs are ordinary egress flits — consume them like ACKs.

**Python refusals** — `tools/quf.py verify` / `tapfabric.py`'s warm
boot raise/exit non-zero with a one-line reason *before any state is
touched*: structural lies (`truncated (need N bytes at off)`),
unknown versions, digest mismatches (`quf.sha256 mismatch: payload
content corrupted after write`), and warm-boot consistency refusals
(`tap.cellnames carries 3 names for cell_count 2 -- refuse (no silent
half-load)`). Tutorial 3 runs all three classes.

## 6. Interpreting the numbers

- Everything except bucket counts and ages is **Q1.15**: divide by
  32768 to read it as a fraction. `0x6000`=0.75, `0x3800`=0.4375,
  `0x2CCD`≈0.35 (COS_MIN default), `0x1000`=0.0625.
- **One cofire = +0x100 of weight** (bucket 0 priced at 2^K, K=8):
  the ladder *is* a dyadic staircase; after one half-life (HL ticks)
  the whole bucket vector shifts one class older and every count's
  say halves.
- **The leak** is a shift, not a multiply: `act −= act >>> KA`; KA=5
  loses ~3% per tick.
- **wsum saturates** at 0xFFFF rather than wrapping (a width bug the
  cosim caught — BACKEND-NOTES).
- Which claims are *proven*, and how far: [VERIFICATION.md](VERIFICATION.md)
  (and its honest not-covered list — e.g. no on-hardware test yet).

## 7. Troubleshooting

| symptom | cause / fix |
|---------|-------------|
| `ERROR: 'iverilog' not found on PATH` | pass `make OSSCAD=/path/to/oss-cad-suite/bin` (or export `OSSCAD`) |
| bind ACKs for cell *k* never arrive | *k* ≥ NCELL: that ring node is the IO port, not a cell (§2.1) |
| link seems to do nothing | the ACK is addressed to the **peer** and is consumed there; verify the link with `view(1)` (wsum == base) |
| effect sent, nothing came back | effects are **silent by design** (no ACK unless a fire); poll with `view(0)` |
| view returns stale/garbage dat | you consumed an ACK you didn't want (e.g. the peer's link ACK); responses are ring traffic — count your consumptions, or log egress transfers |
| `cannot open tb/run/quf_tb_input.hex` | generated file: run `bash tools/run_quf_tb.sh` first |
| sim and RTL disagree on a decay trace | check HL: the dial default is 64 ticks; a wrong HL is a 1.33× decay-rate error (this exact drift was a real bug — `sim/tools/tapfabric.py` header) |

## 8. Where to go next

- [TUTORIALS.md](TUTORIALS.md) — three runnable tutorials (first
  fabric, Hebbian edges, QUF round-trip) + a CLI appendix, with
  committed expected outputs in `examples/` (see `examples/README.md`).
- [THE-TICK.md](THE-TICK.md) — one tick through the RTL.
- [docs/FPGA-BOOT.md](FPGA-BOOT.md) — the boot design rationale.
- [sim/README.md](../sim/README.md) — the behavioral lane.
