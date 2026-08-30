# TUTORIALS — three progressive, runnable lessons (+ a CLI appendix)

*Each tutorial lives in `examples/<name>/` with a `run.sh` and a
committed `.expected` output file. Everything printed below was
produced by actually running them (iverilog 13.0 from oss-cad-suite,
`ccff448`, 2026-08-30). Run them yourself:*

```sh
bash examples/t1_first_fabric/run.sh     # <1 s
bash examples/t2_hebbian_edges/run.sh    # <1 s
bash examples/t3_quf_roundtrip/run.sh    # <1 s
bash examples/t4_cli_tools/run.sh        # <1 s  (CLI appendix)
```

Each `run.sh` compiles/derives nothing outside its own `out/`
directory, runs the real RTL or the real `tools/quf.py`, prints its
trace, and **diffs itself against the committed expected output** —
exit 0 means what you just ran is byte-for-byte what this page shows.

Prerequisites: oss-cad-suite on PATH or via `OSSCAD=...` (see the
[User Guide](USER-GUIDE.md) §1), Python ≥ 3.8 stdlib for T3. No FPGA
needed — all three run in simulation on a laptop.

---

## T1 — Your first fabric: bind, link, effect, view, tick

**File:** `examples/t1_first_fabric/t1_first_fabric.v` (a testbench is
the honest first driver: it is exactly how `tb/` drives the fabric).
**Fabric:** `q_fabric_top`, NCELL=2, TPW=4 → one tick every 16 cycles.

The lesson: the five opcodes are the whole interface. You will bind
two cells, watch the **THRESH dial move** (write it, view it back),
wire cell 0 to hear peer 1, push one effect in, and watch `act` rise —
then watch free-running ticks **leak it back down**.

```sh
$ bash examples/t1_first_fabric/run.sh
== T1 first fabric: NCELL=2, TPW=4 (tick every 16 cycles) ==
      [egress op=5 src=0 dst=f dat=0000]
      [egress op=5 src=1 dst=f dat=0000]
bind  cells 0 and 1 bound (ACK seen)
      [egress op=5 src=0 dst=f dat=6000]
view  cell 0 THRESH before  = 0x6000   (THRESH before)
      [egress op=5 src=0 dst=f dat=0000]
      [egress op=5 src=0 dst=f dat=2000]
view  cell 0 THRESH after   = 0x2000   (THRESH after)
      [egress op=5 src=0 dst=f dat=1000]
view  cell 0 wsum (edges)   = 0x1000   (wsum (edges))
      [egress op=5 src=0 dst=f dat=0000]
view  cell 0 act before     = 0x0000   (act before)
      [egress op=5 src=0 dst=f dat=07bc]
view  cell 0 act after eff  = 0x07bc   (act after eff)
      [egress op=5 src=0 dst=f dat=06d2]
view  cell 0 act +3 ticks   = 0x06d2   (act +3 ticks)
T1 PASS: bind->link->effect->view->tick, 0 errors
```

What each number means:

- `[egress ...]` lines are the ring's chatter — every ACK/view
  response is a flit that rides the ring back to the external id
  (`dst=f`); Law 2: *responses are traffic*.
- `THRESH before 0x6000` — the dialfile POR default (0.75 in Q1.15).
  After a bind-as-dial-write (`a0=5, a1=0x2000`) it reads `0x2000`:
  **a dial moved**, the gentlest possible proof the fabric is alive.
- `wsum 0x1000` — the fresh link's base weight, read back through the
  edge engine.
- `act after eff 0x07bc` — the one effect trained the edge first
  (w: 0x1000 → 0x1100; a bucket-0 cofire is worth 2^8), integrated
  with the **post-update** weight — `act = (0x1100×0x4000)>>>15 =
  0x880` — and then free-running ticks leaked it
  (`act −= act>>>KA`, KA=5): 0x880 → 0x83C → 0x7FB → **0x7BC** by the
  time the view landed.
- `act +3 ticks 0x06d2` — three more ticks of leak. The needle falls
  on its own; nobody sent anything.

**Try next:** change TPW to 8 and watch the leak slow; lower THRESH to
0x0400 and watch the cell fire (or run `tb/tb_fabric_smoke.v`, the
v1 acceptance gate, which does train→fire→decay end to end).

## T2 — Hebbian edges: the ladder learns and forgets

**File:** `examples/t2_hebbian_edges/t2_hebbian_edges.v`.
**Fabric:** NCELL=2, TPW=4; THRESH parked at 0x7FFF so nothing fires —
the lens stays on the weights. A VCD lands in `out/` for GTKWave.

The lesson: an edge is a *learned weight bank*, and its readout is a
dyadic staircase. Ten cofires go in; the sum rises by exactly
`10 × 0x100`; then you set the half-life dial (HL=2) and **watch ticks
sweep the ladder** until only the base weight remains.

```sh
$ bash examples/t2_hebbian_edges/run.sh
VCD info: dumpfile t2_hebbian_edges.vcd opened for output.
== T2 hebbian edges: NCELL=2, TPW=4, K=8 ladder ==
view  cell 0 wsum after link  = 0x1000
train 10 effects delivered (src=1 -> dst=0)
view  cell 0 wsum after 10x   = 0x1a00
view  cell 0 act (buzz)       = 0x425c
dial  HL=2 (half-life = 2 ticks), letting ticks sweep
view  cell 0 wsum ~4 ticks    = 0x1140
view  cell 0 wsum swept out   = 0x1000
T2 PASS: ladder learned 0x1000->0x1A00, forgot ->0x1000
```

The readout, read right to left:

- `0x1000` — base weight, nothing learned yet (asserted exact).
- `0x1A00` — after 10 paced effects: each accepted effect drops +1
  into **bucket 0**, and the ladder prices bucket *i* at `2^(K−i)`
  (K=8), so ten cofires = `10 × 0x100` exactly (asserted exact — the
  ladder *is* the dyadic staircase, equality by construction).
- `0x1140` — about 4 ticks after HL=2: two half-lives have shifted
  the whole bucket vector two classes older; the 10 counts now sit in
  bucket 2, priced `10 × 2^6 = 0x140`.
- `0x1000` — after 40+ ticks every count has shifted past the last
  bucket: **the ladder forgot everything except the base** (asserted
  exact).

The same walk in a waveform: `gtkwave examples/t2_hebbian_edges/out/
t2_hebbian_edges.vcd` — the `wsum` view responses step down the
staircase while `dut.nodes[0].u_core.act` sawtooths under the leak.

**Try next:** send the 11th effect *after* the sweep — one cofire
re-enters at bucket 0 (`wsum = 0x1100`), proving the ladder restarts
fresh classes; or set `mode=1` dials and watch the hyperbola engine's
`wh−−` tail instead (golden tails in `tb/tb_hyperbola_tail.v`).

## T3 — QUF round-trip: state is a file

**File:** `examples/t3_quf_roundtrip/t3_quf_roundtrip.py` (Python,
stdlib + `tools/quf.py`; no simulator). **State:** T2's ending frozen
into `room.json` — cell 0's edge still carries `buckets: [10,0,...]`.

The lesson: the doctrine's proof by construction — *state is a file*
(docs/DOCTRINE.md item 3). Save the room, reload it, prove identity;
mutate the live state, save elsewhere, then restore from the first
file and prove the original state comes back. Identity rests on the
**canonical-form property**: the writer emits header KVs and sections
in a fixed order with aligned payloads, so the *same state always
rebuilds to the same bytes* — asserted byte-exact by `quf.py
selftest`'s golden vector (sha256 pinned in [QUF-SPEC.md](QUF-SPEC.md)
§11) and exercised by the warm-start tests under `make sim`
([VERIFICATION.md](VERIFICATION.md), lane 2).

```sh
$ bash examples/t3_quf_roundtrip/run.sh
save   examples/t3_quf_roundtrip/out/room.quf (640 bytes)  verify clean  sha256 109a4118d7831443...
reload  cells=2  THRESH: cell0=0x6000 cell1=0x3800  edge buckets=[10, 0, 0, 0, 0, 0, 0, 0]
id     rebuild(parsed) == file bytes  -> canonical form holds
mutate  cells=2  THRESH: cell0=0x3800 cell1=0x3800  edge buckets=[11, 0, 0, 0, 0, 0, 0, 0]
       sha256 1a2da8fb33c00cae...  (differs: state changed, file changed)
restore cells=2  THRESH: cell0=0x6000 cell1=0x3800  edge buckets=[10, 0, 0, 0, 0, 0, 0, 0]
id     room.quf still boots the ORIGINAL state (THRESH 0x6000, 10 cofires) -- the file is the state
refuse dial byte flip: quf.sha256 mismatch: payload content corrupted after write
refuse bad version  : corrupt2.quf: unsupported version 2
refuse truncated    : truncated value at 284
T3 PASS: save -> reload -> identity -> mutate -> restore -> refuse
```

Reading it:

- **save** builds the container with the digest KV (`quf.sha256`)
  pinning section *content*; verify is clean.
- **reload** decodes the file back into state — dials, THRESH per
  cell, and the edge's ladder buckets all came off the disk image.
- **id** — re-emitting the parsed container reproduces the file
  byte-for-byte: canonical form.
- **mutate** — one dial eased (0x6000→0x3800) and one more cofire
  heard (10→11): a different state, a different sha256. State changed
  ⇒ file changed — the contrapositive is what makes the identity
  check meaningful.
- **restore** — the untouched first file still boots the ORIGINAL
  state. The file *is* the state.
- **refuse** — three corruption classes, all loud, all *before* any
  state is touched: a flipped dial byte (caught by the digest — the
  structure still parses, the content no longer matches), a bad
  version word, and truncation. Fail-static in silicon (`quf_boot`
  parks in `HOLD_ERR`), fail-loud in Python.

**Try next:** warm-boot the evolved file through the RTL loader lane
— `tools/run_quf_tb.sh` streams a container into `q_uf_loader` and
checks dial + edge readback byte-exact (the loader profile's known v1
limit: buckets ride the file but the RTL edge engines have no load
port — the Python path restores them); or replay a whole MudArena
session into a QUF with `sim/tools/tapfabric.py` (`sim/README.md`).

## T4 (appendix) — The QUF CLI tour

**File:** `examples/t4_cli_tools/run.sh` — the whole `tools/quf.py`
command set (`create → verify → info → dump → hex`) against
`room.json`, the no-simulator door from the
[User Guide](USER-GUIDE.md) §2.3. The committed expected file shows
every command's real output, ending with the byte-per-line hex image
the testbenches `$fscanf`:

```sh
$ bash examples/t4_cli_tools/run.sh   # tail of the transcript:
...
$ python3 tools/quf.py hex examples/t4_cli_tools/out/room.quf examples/t4_cli_tools/out/room.hex
wrote examples/t4_cli_tools/out/room.hex (544 bytes)
hex image header: 0220 (bytes); dials payload starts at hex line 385
```

(`0220` = 544 in hex: the first line of a `.hex` image is the byte
count, then one byte per line — `tb/quf_tb.v` eats exactly this
format. Line 385 = file offset 0x180 + 1: the dials payload, where
the User Guide's hexdump walk picks up.)

---

## Where the guarantees come from

These tutorials show *behavior*; the repo's claims about *correctness*
are separate and cited: the RTL testbench lane (`make test`, 18/18),
the Python lane (`make sim`, 34/34, which includes the QUF warm-start
round-trip this tutorial leans on), the six formal proofs, and the
synthesis flow — all in [VERIFICATION.md](VERIFICATION.md). The byte
walk behind T3's container format is the [User Guide](USER-GUIDE.md)
§3 (a real hexdump, annotated) and [QUF-SPEC.md](QUF-SPEC.md).
