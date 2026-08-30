# ENGINEERING-GUIDE — integrating and porting the quilt fabric

**Audience:** an engineer wiring this fabric into something else — a C
backend, a soft core, a simulator, an FPGA build — or porting it to a new
device. This is the page that consolidates the *contracts* the fleet
actually integrated against, the *bugs the integrations really hit*, and
the *measured costs*, with provenance for every number.

**Honesty policy (inherited from `docs/SYNTHESIS-RESULTS.md`):** every
measurement below is either measured by the pass named in its source or
committed in the artifact named there. Where a lane is still in flight,
this guide says so. Nothing here is an estimate quoted as a measurement.

Companion docs: `QUF-SPEC.md` (the container), `THE-TICK.md` (semantics
walk-through), `VERIFICATION.md` + `formal/README.md` (what is proven),
`SYNTHESIS-RESULTS.md` (silicon numbers), `SYNTHESIS-FPGA.md` (the
synthesis narrative). Sibling integrations (read-only references for this
guide): `~/projects/quilt-deck` (the worked application; three backends,
one semantics), `~/projects/quilt-tournament/teams/*` (independent
consumers of the spec).

---

## 1. Integration surfaces

You integrate against three surfaces. Get all three bit-right and the
conformance suites will prove your port equals the reference; get any one
wrong and the divergence shows up in exactly one place, which is what
makes the matrix in §5 diagnosable.

### 1.1 The QUF image contract

One file carries the whole fabric state. Full spec: `docs/QUF-SPEC.md`;
reference implementation `tools/quf.py` (stdlib only); C implementation
`quilt-deck/esp32/qufc.c`; synthesizable consumer `rtl/q_uf_loader.v`.
The load-bearing rules, in the order integrators break them:

- **Layout is canonical, not merely valid.** Magic `51 55 46 00`,
  version 1, little-endian everywhere, header KV in the spec's standard
  order, section table ascending, offsets multiples of `align`
  (default 32), zero padding, file length padded to `align`. Two
  "valid" QUF files with the same state but different KV order or
  padding are *different files* — byte-identity is the conformance bar
  (§2), and it leaves no room for creativity.
- **Extensibility is asymmetric.** Unknown KV keys, unknown section
  names, unknown section kinds: *skip*. Unknown value types: *reject
  loudly*. Applications append state as new sections (quilt-deck's
  `app.deck` books section is the worked example — `quf.py` skips it,
  the app reattaches it).
- **Two flavors, one state.** *Archive* QUF: the four v1 sections plus
  app sections (host-side tooling). *Boot* QUF: app sections stripped —
  this is what `rtl/quf_boot.v` + `rtl/q_uf_loader.v` consume on
  silicon. The loader profile does **not** restore Hebbian walk state
  (`wh`, `age`, ladder buckets): v1 edges have no load port, so a
  warm-started fabric re-binds dials + topology and *re-earns* the
  ladders from its own training stream. The Python path is the
  full-state path. Both end states are byte-equal — that is the warm
  theorem quilt-deck's conformance suite asserts (ARCHITECTURE §6).
- **Golden vector.** The 576-byte canonical vector (2 cells, 3 edges,
  3 routes, tpw=6), sha256 `5b2a236b…`, is embedded in `tools/quf.py`,
  asserted by `selftest`, and loaded by `tb/quf_tb.v` through the RTL.
  A new writer that cannot reproduce it byte-for-byte is not a QUF
  writer. Loader error codes 1–9 (bad magic … `edge.k` out of range)
  are in QUF-SPEC §9.

### 1.2 The egress frame contract

The serial fabric front-end (`rtl/q_serfabric_top.v`) speaks **10-byte
frames, MSB-first bytes of an 80-bit word**:

```
{op[2:0] @77, src[3:0] @73, dst[3:0] @69, a0 @53, a1 @37, a2 @21, dat @5, pad[4:0]=0}
```

- Opcodes `0..6` = BIND / LINK / EFF / VIEW / TICK / ACK / NAK. The
  host / io node lives at `EXTID = 0xF`; v1 routing is positional
  (dst == ring slot). Reference framer/deframer: `quilt-deck/deck/
  fabric.py::flit_frame` / `parse_frame`.
- Byte-level handshake: ingress `i_sval / o_srdy / i_sbyte[7:0]` (+`i_eod`),
  egress `o_stx_val / o_stx[7:0]` with `i_strdy`. Status surfaces:
  `o_boot_ok`, `o_epoch`, `o_state[2:0]`, `o_err[7:0]`, `o_ovf`.
- The ESP32 backend, on its host-loopback protocol, uses text lines
  instead (in: `F <op> <src> <dst> <a0> <a1> <a2> <dat>`, `T <n>`, `V`,
  `D`, `S <path>`, `B <path>`, `E`; out: `E <…>` egress, `! <cell> <dat>`
  fire, `#` info) — but the *flit content* is the same contract. "Frame-exact"
  conformance means: the same flit stream, in order, field-for-field.

**Reference discipline (do not shortcut this):** every engine's egress is
compared against the **Python soft-fabric shadow** — never engine against
engine. `esp32 == py` and `RTL == py` chain transitively to
`esp32 == RTL`; two hardware-ish codepaths compared only to each other
would prove nothing about either (this rule was made explicit in
quilt-deck commit 60fc10d, and a drift sentinel fails the suite if
quilt-verilog ever grows a second bridge copy).

### 1.3 Tick discipline — and the negedge byte rule

- **Fabric side:** `q_tick_sched` strobes one `o_tick` cycle per 2^TPW
  clocks. The tick latches from any state (the Q2 interlock), wins the
  next idle slot, and is never dropped — formally bounded
  (`cell_core.tick`, BMC 80). One tick = decay sweep of every valid
  edge → act leak → fire test → (fanout | resume). Full walk:
  `docs/THE-TICK.md`.
- **Simulation side — the house race rule:** drive serial *bytes on the
  negedge*, let the DUT sample on the posedge. Driving on posedge races
  the DUT's sampling: the two-byte release word lands wrong and the
  boot gate reports **err 11** — that exact failure is why the rule
  exists (recorded in `quilt-deck/cosim/tb_deck_cosim.v`, obeyed by
  `tb/tb_serfabric.v`). If your driver sees err 11, this is bug #1 to
  check (§5).
- **Egress capture — count bytes, don't watch edges:** the frame-busy
  edge lags the first egress byte by one NBA update; a capture scheme
  keyed on the busy edge silently loses the first byte of every frame.
  The TBs count `o_stx_val` bytes and assemble frames every 10th byte.
- **Determinism protocol for co-sim (quilt-deck ARCHITECTURE §5):**
  tpw=15 (32,768 cycles per tick); every op segment ≤100 flits followed
  by an explicit tick marker (no segment can straddle a tick edge,
  >2.5× headroom), so both engines see the identical op/tick
  interleaving without cycle-exact modeling; settle ≥4096 cycles after
  each tick so fire fanout fully drains before the next observation.

---

## 2. Porting guide: the ESP32 C backend, or what "byte-identical" really cost

The worked port is `quilt-deck/esp32/deckbridge.c` + `qufc.c`: the deck
graph (15 cells, 4 edge slots, K=8) hosted on the vendored quilt-vm-c,
with the numeric core a C transcription of `deck/fabric.py`. The
conformance bar, proven in `quilt-deck/tests/test_day.py::
test_backend_conformance_python_esp32`:

1. same day log → **byte-identical final QUF** (sha256-equal; the
   archive flavor, five sections including `app.deck` — commit dd70406,
   asserted since fcfaa95),
2. **frame-exact egress** and identical fire streams vs the shadow,
3. identical ledger books (the ledger is backend-independent by design).

Everything below is from the conformance push (quilt-deck commit
47d020c, 2026-08-29). Five real bugs, each with the signature it
presented with — this list is the actual return-on-investment of
byte-identity: every one of these passes a casual "looks right" review.

| # | bug | where | signature you'd see | fix |
|---|-----|-------|---------------------|-----|
| 1 | **feeder double-send** | `deck/backends.py` | shadow model's predicted egress diverges from the bridge at the first traffic (events effectively doubled); separately, the driver deadlocks writing `F` lines while the bridge blocks writing `E` lines (the 64K pipe) | the replay driver already sends flits to the fabric it drives; the on-flits callback is an **observer** that only *mirrors* to the bridge. Plus: full-duplex reader thread; quiescence-based `drain()` (event-driven days have no fixed event count — counting to a predicted N both deadlocks and lies) |
| 2 | **vm NULL deref** | `esp32/deckbridge.c::vm_apply` | bridge process dies (SIGSEGV) on the first `T` command — tick events pass `f == NULL` and `arg.f = *f` dereferenced it | null-guard the flit copy (`if (f) … else zero`) |
| 3 | **deck/tick thing missing** | `esp32/deckbridge.c::main` | the VM rejects the tick's effect application — ticks are forwarded as queued effects onto a thing (`deck/tick`) that was never bound | `qm_bind_str(vm, "deck/tick", …)` at startup. Sibling fix in the same commit: the ladder half-life counter lives **per edge**, not per cell — the dump showed all of a cell's edges sharing one `hl_cnt` and shifting together (`c->hl_cnt` → `e->hl_cnt`) |
| 4 | **qufc producer field** | `esp32/qufc.c` (+`qufc.h`) | esp32-saved QUF fails `quf.py verify` / hashes differ from Python's despite identical state; diff localized to header KV — the producer string was hardcoded `"quf.py 1.0"` and `edge_k`/`tick_period`/`align` were never set (0 is not a legal `edge.k` or `align`) | `QufcDoc.producer` field; the deck sets `producer="quilt-deck 1.0"`, `edge_k=K`, `tick_period=1<<tpw`, `align=32`. Canonical KV order fixed in the writer |
| 5 | **stack buffer overflow** | `esp32/qufc.c::qufc_build` | garbage QUF or a crash on `S` at deck scale — the section staging buffers were sized for the 2-cell golden vector (`edges_buf[256]`) while the deck's edges section is up to 60 records × 20 B = 1,200 B | size the staging buffers for the real fleet (8 KiB class), not the test vector |

Porting checklist distilled from that push:

- Reproduce the **golden vector** both directions (build-from-doc ==
  576 golden bytes; parse-and-rebuild == same) before touching real
  state. `qufc.c`'s selftest does exactly this.
- Transcribe the arithmetic, don't reimplement it: saturating
  Q1.15 (`sclip16`), ladder buckets, echo gate, hyperbola — bit-for-bit
  against the Python model, whose own values came from the RTL's golden
  tests (`tests/test_fabric.py` cites SYNTHESIS Part A).
- One booking authority. The ledger/refusal logic stays backend-
  independent; backends only execute accepted traffic. Refusals emit
  zero fabric traffic (state-hash-asserted).
- Compare against the Python shadow, never against the other port (§1.2).
- Drain by quiescence, not by predicted counts.
- Size every buffer from the fleet's parameters, then re-derive the
  limit from the spec (`cell_count × 32` dials, `edges × (12+K)`, …).

---

## 3. FPGA flow: Yosys → nextpnr → icepack on iCE40

Toolchain: stock **oss-cad-suite** (yosys 0.47+22, nextpnr-ice40
0.7-131, icepack; iverilog 13.0 for the TB lane). The root `Makefile`
pins `OSSCAD ?= /home/eileen/tools/oss-cad-suite/bin` — override with
`make OSSCAD=/path/to/oss-cad-suite/bin <target>`.

```sh
make test     # 18/18 RTL testbenches (iverilog -g2005)     ~1–2 min
make sim      # 34 behavioral Python tests                  seconds
make formal   # six SymbiYosys proofs (BMC + one prove)     ~14 min
make synth    # yosys iCE40 elaboration of the converged top  ~20 s
make pnr      # synth + nextpnr + icepack                   ~3 min
make all      # everything, in order
```

Every tool invocation is wrapped in a `GUARD` macro (Makefile, commit
ccff448): if `iverilog`/`sby`/`yosys`/`boolector`/`nextpnr-ice40`/
`icepack` is missing you get `ERROR: '<tool>' not found on PATH` plus
the `OSSCAD=` override hint and exit 127 — never a bare
`command not found`.

The converged build is `synth/fpga-converged.ice40` → `q_fabric_top`,
config **k4b4a8e1** (NCELL=2, EDGES_N=1, K=4, B=4, AGEW=8 — exactly the
formal conservation proof's parameters). Exact commands (what `make
synth` / `make pnr` run):

```sh
yosys -s synth/fpga-converged.ice40
nextpnr-ice40 --hx8k --package ct256 \
  --json synth/fabric2_k4b4a8e1_ice40.json --freq 12 \
  --timing-allow-fail --pcf-allow-unconstrained \
  --asc synth/fabric2_k4b4a8e1.asc --report synth/report_k4b4a8e1.json
icepack synth/fabric2_k4b4a8e1.asc synth/fabric2_k4b4a8e1.bin
```

Gotchas worth knowing before you touch the scripts:

- **`chparam` must precede `hierarchy`** — parameters set on `q_cell`'s
  definition only propagate into instances that don't pin their own
  K/B/AGEW if the def defaults are set before hierarchy expansion
  (see the comment block in `synth/fpga-converged.ice40`).
- No PCF exists: IO is auto-placed (`--pcf-allow-unconstrained`) and
  `--timing-allow-fail` is set against the 12 MHz target. A real pin
  constraint file could move fmax either way.
- **Quote post-route fmax only.** nextpnr prints a post-*placement*
  estimate and a post-*route* number; both of this repo's recorded
  corrections (UP5K 17.36→16.78, HX8K 43.36→44.43) were the estimate
  quoted as final. This is now a repo-wide quoting rule
  (SYNTHESIS-RESULTS Tables 1† and 5).

**What fits where** (all rows measured 2026-08-29; full tables with
per-run provenance in `docs/SYNTHESIS-RESULTS.md`):

| device | config | LC / cap | IO | fmax (post-route) | closes 12 MHz? |
|---|---|---|---|---|---|
| iCE40 HX8K-CT256 | parallel FE, 2 cells (k4b4a8e1) | 7,596 / 7,680 (98%) | 157 / 256 | 44.43 MHz | PASS |
| iCE40 UP5K sg48 | **serialized FE** (serf), 1 cell | 4,231 / 5,280 (80.1%) | **37** / 96 | 16.78 MHz | PASS |
| ECP5 LFE5U-25F | parallel FE, 8 cells | 22,791 / 24,288 (94%) | — | 63.7 MHz | PASS |
| ECP5 LFE5U-12F (real die) | parallel FE, **4 cells max** | 11,554 / 12,144 (95%) | — | 62.9 MHz | PASS |

Two walls the tables document honestly: the parallel front-end needs 157
IO, which is why the UP5K cannot place even NCELL=1 without the
**serialized fabric front-end** (`q_serfabric_top`, commit 225a9c1 —
byte-exact vs the parallel config path, differential-TB-proven); and
nextpnr's `--12k` places against the 25F die, so a "12F" row that says
/24,288 is lying to you about a real 12F (physical capacity 12,144
LUT4s — max 4 cells). Bitstream for the converged top: 135,100 bytes.

**Nothing on this page has met a board.** No PCF, no bring-up, no
hardware test — `docs/VERIFICATION.md`'s not-covered list applies to
every silicon number. A bitstream that packs is not a bitstream that
boots.

---

## 4. Co-simulation

### 4.1 The deck cosim: RTL refereed by the Python model

`quilt-deck/cosim/tb_deck_cosim.v` (commit 656ca09) instantiates two
DUTs of the real `q_serfabric_top` (15 cells):

- **DUT-COLD** (`SER_BOOT_QUF=0`, gate mode, TPW0=15): released with
  the commissioning word, then plays the whole fishing day as framed
  ops — bind/link commissioning, landings, moves, hooks, ticks, night.
- **DUT-WARM** (`SER_BOOT_QUF=1`): boots the day's saved boot-QUF
  (hex image), then replays the *same* training stream — the warm
  doctrine made literal: dials warm, ladders re-earned.

Script format (`$fscanf`-friendly, one op per line): `1 <20-hex 80-bit
frame>` send; `2 <n>` settle; `3 <n>` run n ticks (+4096 settle);
`9` dump state; `0` end. The driver `deck/cosim.py` builds scripts from
the same day log via `replay(..., on_flits=...)`, predicts egress with
the soft model, runs iverilog, and referees four claims: egress
**frame-exact** (cold and warm), cold end state dials+edges byte-equal
(py vs RTL), warm re-earn byte-equal (RTL warm == RTL cold), and the
rebuilt QUF byte-identical. Settle sizing: `min(200 × nframes + 2000,
24000)` cycles per segment.

### 4.2 How the fixtures were synthesized — and honestly labeled

The `cosim/run/` fixtures are **regenerated by the driver**, not
hand-maintained: `cold.ops`/`warm.ops` scripts, `boot.hex`, the `*.egr`
egress logs, `*.dump` state dumps (90 lines: DC/DA/DE per cell). The
git history is the honest label (quilt-deck):

- 656ca09 committed the TB + driver with **empty `.egr` captures** —
  the lane did not pass yet, and the commit says so by what it holds.
- 47d020c committed the passing cold day's egress log — **149,472
  lines**, the artifact that proved frame-exactness at that tree.
- 16b0140 untracked the bulky regenerable artifacts (ops/egr) in favor
  of on-demand regeneration; `.vvp`/`.hex` are gitignored.
- The probe lineage (`tbp2/tbp3/tbp4.vvp`, `cosim/mkprobe4.py`) is the
  warm-lane debugging trail: mkprobe4 patches the TB with a **stuck-state
  watchdog** (no-egress-for-4M-cycles → photograph `o_state`/`o_err`/
  per-cell core states, then finish). When a cosim hangs, photograph
  first, bisect second — the watchdog exists because blind bisecting
  a 9,075-line op script is misery.

Treat it this way: **cold-lane frame-exactness is artifact-proven at a
named commit; the warm lane's passing capture is documented in
ARCHITECTURE §5 and asserted by the driver — re-run `python3 -m
deck.cosim` to regenerate both** rather than trusting any checked-in
copy to be current.

### 4.3 The semantics prototype: `sim/tools/tapfabric.py`

The behavioral lane (`make sim`, 34 tests) proves the *semantics* in
Python before/alongside silicon: `tapfabric.py` mirrors `q_cell_core` /
`q_hebb_edge` / `q_dialfile` arithmetic bit-for-bit (saturating Q1.15,
ladder, hyperbola, dial POR table) and replays real-format session logs
into a cell graph, emitting a QUF + transcript. Two lessons that
generalize to any port:

- The dial POR table must be copied in **raw-word parity** — the
  Python table once drifted (HL 48 vs RTL 64; KLE/RQ/RQL 0 vs 2/8/8)
  and the ladder half-life drift was load-bearing: a silent 1.33×
  decay-rate mismatch (fuzz-found 2026-08-29, note in the source).
- Model ordering is *defined* to match the RTL's sweep order (slot 0
  first); any reordering keeping per-edge math identical is
  observationally equivalent at tick boundaries — that's the lemma the
  differential cosim leans on (`THE-TICK.md`, honesty notes).

---

## 5. Troubleshooting matrix

Every row below is a real event from the integration record (§1–§4);
symptoms are quoted the way they actually presented.

| symptom | cause | fix |
|---|---|---|
| boot gate reports **err 11**; release word "lands wrong" | TB drives serial bytes on posedge, racing the DUT's sampling | drive on **negedge**, sample on posedge (§1.3) |
| egress capture drops the first byte of each frame | frame-busy edge lags the first byte by one NBA | count `o_stx_val` **bytes**, assemble every 10th (§1.3) |
| `ERROR: '<tool>' not found on PATH`, exit 127 | oss-cad-suite not at the pinned path | `make OSSCAD=/path/... target` (GUARD hint, commit ccff448) |
| nextpnr IO failure on UP5K ("157 IO > 96 pins") | parallel config front-end's IO budget exceeds the package | use the **serialized front-end** (`q_serfabric_top`, 37 IO); see SYNTHESIS-RESULTS Table 4 |
| `PNR_FAIL (LC)` at NCELL≥2 on UP5K / ≥12 on ECP5 | fabric exceeds device logic capacity | climb the device ladder (Table 3): UP5K=1 cell (serf), HX8K=2, real 12F=4, 25F=8 |
| "12F" row closes 12 cells and looks fine | nextpnr `--12k` places against the 25F die (12F is binned 25F silicon) | check against physical 12,144 LUT4 capacity; the tracked `scale.tsv` carries a `util12f%` column |
| fmax claim doesn't reproduce | post-placement estimate quoted as final | quote **post-route** only; label estimates if cited at all (Tables 1†, 5) |
| new backend's QUF fails `quf.py verify` despite correct state | non-canonical KV order / unset `edge.k`, `align`, producer (bug #4) | canonical writer; set all standard KVs from fleet parameters (§2) |
| bridge/daemon **segfaults on first tick** | tick path dereferences a null flit pointer (bug #2) | null-guard; ticks carry no flit |
| VM rejects tick effects ("no such thing") | tick drain forwards effects onto an unbound host thing (bug #3) | bind the tick thing at init |
| predicted egress diverges from device; events roughly doubled | driver double-sends (replay drives the fabric *and* the mirror callback feeds it again) (bug #1) | mirror-only observer; one sender of record (§1.2) |
| driver hangs mid-replay, both sides blocked | 64K pipe write-write deadlock + count-based drain | full-duplex reader thread; quiescence drain (§2) |
| all of a cell's ladder buckets shift together; `hl_cnt` identical across `DE` dump slots | half-life counter stored per-**cell** instead of per-**edge** (sibling of bug #3) | move the counter onto the edge (`e->hl_cnt`) |
| saved QUF is garbage or the save crashes at fleet scale (15 cells) | staging buffers sized for the golden vector (bug #5) | size from fleet parameters: dials `N×32`, edges `E×(12+K)`, … |
| warm-started ladders differ from the saved file | loader profile *consumes but does not restore* walk state — by design | re-earn from the training stream (loader path) or use the Python full-state path; both converge byte-equal (§1.1) |
| RTL/Python semantics drift with no code change visible | model's dial POR or sweep order drifted from RTL raw words | raw-word parity for POR tables; sweep order defined to match (§4.3) |
| cosim hangs partway through a long op script | a real stuck state (or a genuine RTL bug) — blind bisection over 9k ops is hopeless | watchdog probe that photographs `o_state`/`o_err`/core states on egress silence (`mkprobe4.py`), then bisect |

---

## 6. Performance and cost (measured, cited — never invented)

**Silicon** (`docs/SYNTHESIS-RESULTS.md`, all 2026-08-29, oss-cad-suite
yosys 0.47+22 / nextpnr-ice40 0.7-131, 12 MHz target, no board):

| what | measured | source |
|---|---|---|
| HX8K-CT256, k4b4a8e1, 2 cells | 6,002 LUT4 / 898 CARRY / 2,434 FF; 7,596/7,680 LC (98%); 157 IO; 44.43 MHz post-route; 135,100 B bitstream | Table 1 + `synth/iter3/` (committed artifacts) |
| fmax progression, same design family | 27.72 → 40.44 MHz (PIPE_EFF retime, +46%) → 44.43 (re-measure) | Table 1 |
| UP5K sg48, serf, 1 cell | 4,231/5,280 LC (80.1%), 37 IO, 16.78 MHz post-route (15.97 at the pinfix commit tree; 17.36 was the placement estimate) | Tables 4–5 |
| ECP5 25F, 8 cells | 22,791/24,288 LC (94%), 63.7 MHz | Table 3 |
| Build wall time | yosys ~18–20 s; nextpnr ~32 s; icepack instant ("~3 min" covers the full `make pnr` incl. synth) | SYNTHESIS-RESULTS §Reproduce; Makefile |

**Verification lanes** (`docs/VERIFICATION.md`, iteration-2 re-run,
2026-08-29): `make test` 18/18 PASS (~1–2 min); `make sim` 34/34
(seconds); `make formal` six proofs PASS, ~14 min total (fair 498 s,
tick 215 s, conservation 38 s, fly 72 s, dyadic 3 s, k-induction <1 s);
wall times vary with load — verdicts are the stable fact. Scope: all
liveness is assert-within-N in BMC; **unbounded liveness is not
claimed**; conservation proved at k4b4a8e1 with PIPE_EFF pinned
(`formal/README.md`; the prove-mode strengthening attempt and its named
lemmas L1/L2: commit b82cd19).

**Application lane** (quilt-deck, 2026-08-29): Python+esp32 suites 31
tests, ~3 s, stdlib only; the esp32 bridge compiles with the system cc
(no cross-toolchain needed for host loopback); a full fishing day
replays in seconds; the FPGA cosim run is capped at a 1,200 s vvp
timeout (regenerated per run — no committed wall-time number to cite,
so none is quoted). esp32/py conformance: byte-identical QUF,
frame-exact egress, identical fire streams and books
(`tests/test_day.py`).

**Cost of integration, honestly:** the ESP32 conformance push cost five
real bugs (§2) — all caught by byte-identity, all invisible to "looks
right" review. Budget for the conformance suite *before* trusting a
port; it is the cheapest debugging you will do in this stack.

---

## 7. Downstream consumers: what the tournament teams actually consume

`quilt-tournament` (2026-08-29→) runs independent teams
(`teams/{ledger,stream,organism,shipwright,procession,deadband,
deadledger}`) building cell runtimes to the GENERAL-CALCULUS shape.
What they integrate against, from `CHALLENGE.md`, maps 1:1 onto the
surfaces in §1:

- **QUF-style bounded serialization** with fold round-trip
  (`decode(encode(x)) == x`, canonical) — i.e. §1.1's canonical-layout
  rule, not just parseability;
- **the back-deck fish pipeline as the conformance scenario** — moves
  as balanced effects, "a fish in the hold without a booked debit is
  refused with a booked reason" — the same closed refusal set and
  zero-traffic-on-refusal property quilt-deck's ledger enforces (§2);
- **adversarial duty**: double-move, overflow, phantom entry, corrupt
  state, truncated fold — refused or contained, never silent;
- hard rules that mirror this repo's doctrine: no float decides any
  verdict; state bounded; self-graded honesty
  (machine-checked / pen-only / claim).

If your integration satisfies §1's three surfaces and can run the
back-deck scenario with booked refusals, it will interoperate with both
the quilt-deck backends and the tournament harnesses.

---

## 8. What this guide does not claim

- No hardware bring-up has happened anywhere in this stack; every
  silicon number is synth→place→route→pack with no board attached (§3).
- Unbounded liveness is not proven; formal results are bounded-model
  checks plus one k-induction, under the documented environment
  contracts E1–E4 (`formal/README.md`).
- The warm-replay cosim lane's fixtures are regenerated per run; the
  committed artifact record is at the commits named in §4.2, not a
  permanently tracked golden capture.
- The ESP32 path is host-loopback C today; the firmware/PlatformIO path
  runs the same code, but that claim rests on code identity, not on a
  measured device run (quilt-deck ARCHITECTURE §5).

When this guide and a measured artifact disagree, the artifact wins and
this guide gets corrected — that rule is inherited from
`SYNTHESIS-RESULTS.md` and `VERIFICATION.md`, and it has already fired
twice on the fmax rows alone.
