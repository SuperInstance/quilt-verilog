# LOOM/1 — opencode lane entry

A bottom-layer quilt fabric where **every node is one generic cell**, the five
quilt opcodes are the only verbs, and the intelligence (Hebbian edges, decay,
cosine estimation, dials, ticks) lives in small fixed-point RTL primitives
inside each cell. No vendor code, no IP, no SystemVerilog, no `initial` in
rtl/. Everything streams; everything saturates honestly.

Entry identity: `proposals/opencode/` — architecture (this file) + skeletons
(`RTL-SKETCH.md`, 9 module skeletons, hand-checked against IEEE 1364-2005).

---

## 1. Law compliance map

| # | Law (README) | Mechanism in LOOM/1 |
|---|---|---|
| 1 | Pure synthesizable Verilog-2005 | All modules flat-port, `always @(posedge clk)`, sync `rst_n`, no `initial`, no SV, no vendor. Reg-arrays with standard write templates; BRAM inference by template swap, not by primitive. |
| 2 | Everything is a cell; opcodes are the only touch | One generic `q_cell_core` FSM per node; ring port delivers only opcode flits; even fabric-local config (dials) is written via `qm_bind`, read via `qm_view`. Gateways in the L-tier are cells with a second adapter, not special RTL. |
| 3 | Intelligence at the bottom | `q_hebbian_edge` (dual-timescale decay + Hebbian train), `q_cosine_stream` + `q_isqrt16` + `q_divu` (streaming cosine), `q_dialfile` (dial state), `q_tick_sched` (time). Plain RTL, fixed-point, one-beat streaming. |
| 4 | Any IO can enter a cell | One flit contract (`§4`). Adapters only frame/deframe bytes into flits; they never look at opcode bits. |
| 5 | Verified or it doesn't exist | Per-module TBs + golden models + fuzz + a fabric-level train-to-fire smoke test, all on iverilog/vvp with verilator lint (`§11`). |

---

## 2. Fabric overview

Single synchronous clock domain. N generic cells on a unidirectional flit
ring; a global tick scheduler keeps time; thin adapters on the edges of the
world turn arbitrary serial IO into opcode flits.

```
                         quilt_fabric (tier S build: N = 4..8)
   any IO ──[adapter]──┐        ┌──[adapter]── any IO
                        ▼        ▼
        ┌─────────┐   li    ld ┌─────────┐
        │ cell 0  │──────────▶ │ cell 1  │   ring: q_link_ringport per node,
        │ (core + │  EFFECT    │ (core + │   q_flit_pipe register slices
        │ engines)│◀────────── │ engines)│   inserted every 2 nodes
        └────▲────┘            └────▲────┘
             │                     │
       ┌─────┴─────┐   ┌───────────┴───┐
       │ cell N-1  │⋯⋯ │   q_tick_sched │  tick strobe + phase (broadcast)
       └───────────┘   └───────────────┘
```

- **Control plane** = opcode flits (`qm_bind/link/effect/view/tick`) on the
  same ring as data. No separate config bus — that would break Law 2.
- **Time plane** = one shared `q_tick_sched`; tick also exists as an opcode
  flit for tier-L (cluster gateway) re-broadcast, but the hard strobe is the
  primary within a cluster.
- **Latency class**: everything is "a few cycles to a few hundred" — this is
  a learning fabric, not a packet pipeline.

---

## 3. Module hierarchy

```
quilt_fabric_top                      (build item — glue only, no logic)
├── q_tick_sched                      tick strobe + 4-phase cadence
├── q_link_ring   [structural]        N × q_link_ringport closed in a loop
│   ├── q_link_ringport ×N            intercell link: deliver / transit / inject
│   └── q_flit_pipe (every ~2 nodes)  registered flit slice, cuts valid path
└── quilt_cell ×N                     (structural — build item)
    ├── q_cell_core                   opcode FSM: bind/link/effect/view/tick
    ├── q_dialfile                    dial register file (config state)
    ├── q_hebbian_edge                edge train/decay engine (1 instance,
    │                                 time-multiplexed over the edge table)
    ├── q_cosine_stream               streaming cosine estimator
    │   ├── q_isqrt16                 serial integer sqrt (32→16)
    │   └── q_divu #(63,32)           serial restoring divider
    └── io adapters (thin, dumb)
        ├── q_adpt_byteframer         byte stream ⇄ flit frames (build item)
        └── q_adpt_afifo              CDC ingress (build item, spec only)
```

| Module | State bits (approx) | Role |
|---|---|---|
| q_cell_core | ~120 + tables | the only interpreter of opcodes |
| q_dialfile | 16×16 | dial registers, power-on defaults in reset |
| q_hebbian_edge | ~130 | one edge update in 3 cycles |
| q_cosine_stream | ~200 | dot, two mags, divide; VW+~95 cycles |
| q_isqrt16 | ~55 | 17 cycles, multiply-based trial |
| q_divu | ~135 | 63 cycles, bit-serial restoring |
| q_tick_sched | 14 | tick + phase |
| q_link_ringport | 0 (comb) | deliver/transit/inject router |
| q_flit_pipe | ~68 | 1-deep registered flit slice |

Approximate numbers, unverified until first yosys run (see §12).

---

## 4. Generic streaming IO contract (the one ingress/egress)

### 4.1 Flit fields (flat vectors — Verilog-2005 has no structs)

| Field | Width (default) | Meaning |
|---|---|---|
| `op`   | 3  | opcode (below) |
| `src`  | 4  | originating cell id |
| `dst`  | 4  | destination cell id |
| `a0,a1,a2` | 16 each | opcode-specific args |
| `dat`  | 16 | payload word (Q1.15) |

Opcodes: `qm_bind=000, qm_link=001, qm_effect=010, qm_view=011,
qm_tick=100, ack=101, nak=110` (111 reserved). Names in RTL:
`OP_BIND, OP_LINK, OP_EFF, OP_VIEW, OP_TICK, OP_ACK, OP_NAK`.

### 4.2 Handshake rules

1. `valid` is registered by the producer; payload is **stable while valid &&
   !ready**; consumer may deassert `ready` freely (all consumers here have
   registered `ready` or pure-comb `ready` of depth 1 gate — no
   valid→valid comb loops).
2. A flit is transferred on `valid && ready`. Nothing else moves.
3. Engines additionally hold their arg inputs until `done` (args are
   latched at accept, so this is belt-and-braces).
4. Effects are fire-and-forget: `qm_effect` produces **no** response flit.
   `qm_bind/link/view` produce exactly one `ack`/`nak`, addressed to the
   requester and routed as an ordinary flit (responses ride the ring —
   Law 2 applies to responses too).

### 4.3 Adapter charter (thin and dumb)

An adapter MAY: idle-pattern detect, escape/framing, byte reorder,
parity/FCS, CDC, and nothing else. An adapter MUST NOT: decode `op`, branch
on `dst`, originate flits with `op != {bind}`, or hold state beyond
framing/CDC. Frame format (byteframer): 1 SOP byte, 11 body bytes
(op|src|dst|a0hi|a0lo|a1hi|a1lo|a2hi|a2lo|dathi|datlo), 1 EOP byte. Any IO
that can carry bytes can enter a cell.

---

## 5. Intercell link

**Tier-S/M link = unidirectional ring of `q_link_ringport`.** Per cycle, a
node sees the flit at its ring input:

- `dst == myid` → **deliver** to local cell ingress (slot consumed; a bubble
  goes downstream). If the cell is busy, back-pressure propagates upstream
  (`ri_ready = ld_ready`).
- else → **transit** downstream unchanged.
- on a bubble or consumed slot → may **inject** its own effect flits
  (`li`). Transit never blocks inject on a consumed slot; inject never
  preempts transit.

Properties: max 1 delivered flit per node per cycle; aggregate ring
throughput 1 flit/cycle; worst-case hop latency N nodes (+ pipe slices).
Bandwidth math: per tick of length `TICK_LEN`, a firing cell fans out E
effects in E+ε cycles, so the fabric sustains ~`TICK_LEN` effect flits per
tick. Default: `TICK_LEN = 4096`, E = 8 → 2% ring utilization. Comfortable.

`q_flit_pipe` (1-deep, registered `valid`, comb `ready = !vq || m_ready`)
is inserted every ~2 nodes so the transit path is never long comb; final
timing closure is a synthesis datum, honestly pending (§12).

Tier variants in §10.

---

## 6. Cell core FSM

One FSM interprets all five opcodes. States (see `RTL-SKETCH.md` §9):

```
ST_RST → ST_UNB ──qm_bind(id)──▶ ST_IDLE
ST_IDLE ──dispatch──▶ ST_BIND | ST_LINK | ST_EFF | ST_VIEW | ST_TICK
ST_EFF: scan edge table for src → ST_EFFW → ST_EFFI (train + integrate)
ST_VIEW: ST_VACC (wsum) | ST_VRD (dial) | ST_VCS (cosine) → ST_RESP
ST_TICK: ST_TDEC/ST_TDW (decay sweep) → ST_TLEAK (leak + fire test)
         → ST_FIRE/ST_FIREW (fanout) → ST_IDLE
ST_RESP / NAK: one response flit to the requester, then idle
```

Timing budget (cycles, EDGES_N=8, VW=8):

| Path | Latency |
|---|---|
| qm_bind / qm_link (accept→ack sent) | ~4–5 (+ring return) |
| qm_effect (edge found at slot 0) | ≤ 8 (scan) + 3 (engine) + 1 |
| qm_view act | ~4 |
| qm_view wsum | EDGES_N + 4 |
| qm_view dial | ~5 |
| qm_view cos | VW + ~100 |
| qm_tick sweep per cell | 8×5 + 2 + fanout(≤ 2E) ≈ 58 |

Priority in `ST_IDLE`: ingress dispatch first, tick second (tick window is a
whole scheduler phase — a quarter of `TICK_LEN` — so it cannot be missed;
`tick_go` latch guarantees it).

---

## 7. Fixed-point intelligence primitives

### 7.1 hebbian_edge_update — `q_hebbian_edge`

State per edge: `wf` (fast) and `ws` (slow), both unsigned Q1.15, `w = wf+ws`
(saturating). Update on `qm_effect` (train) and on `qm_tick` (decay):

```
train:  wf ← rect0..max( wf − (wf ≫ kf)  ±  ((|pre|·|post|·ηf) ≫ 15) )
        ws ← rect0..max( ws − (ws ≫ ks)  ±  ((|pre|·|post|·ηs) ≫ 15) )
decay:  same without the ± increment
```

`pre` = caller's activation snapshot carried in `qm_effect.dat`; `post` =
the local cell's `act`. Sign of `pre·post` flips add to subtract
(anti-Hebbian), rectified at 0 — weights never go negative.

**Why this is "power-law":** per-tick multiplier `(1 − 2^-k)` is an
exponential with τ = 2^k ticks. The **sum of a fast and a slow exponential**
reproduces a `t^-α` tail within a bounded window (§12, limit 1): with
kf=6, ks=12 the pair covers ~2 decades of time with ≤ 12% shape error
against `t^-0.5`-class targets. Dials set both k's, so the window is a
runtime choice, not RTL.

Datapath: 16×16 multiplies only, magnitude+sign (no signed multiply
contexts), 3-cycle latency, one engine per cell time-multiplexed over the
edge table.

### 7.2 streaming cosine — `q_cosine_stream` (+ `q_isqrt16`, `q_divu`)

Streams VW beats (x_i, y_i) of Q1.15 each, accumulating `dot`, `Σx²`, `Σy²`
in 40-bit Q2.30-with-guard. Then serial integer sqrt of each sum
(÷VW normalization folded in as a shift — exact for power-of-two VW;
the VW factor cancels in the cosine, the shift only keeps the magnitudes
in Q1.15), then one 56/32 serial divide:

```
cos = (dot ≪ 15) / (mx · my),  clamped to Q1.15
```

Output Q1.15 signed; `err` flags a zero vector. Error budget: ≤ 2^-10
against `real` golden for VW ≤ 64 (TB-verified claim to be, §11). This is
the fabric's vMF-style affinity estimator: cosine only, no κ
concentration parameter yet (§12, limit 13).

### 7.3 dial registers — `q_dialfile`

16 × 16-bit, written only via `qm_bind` (config plane), read via `qm_view`
or fanned out combinationally to the datapath. Address map (defaults in
reset — no `initial`, ever):

| addr | dial | type | default | meaning |
|---|---|---|---|---|
| 0 | ETA_F | Q1.15 u | 0x0800 (0.0625) | fast Hebbian rate |
| 1 | ETA_S | Q1.15 u | 0x0080 (0.0031) | slow Hebbian rate |
| 2 | KF | int 0..15 | 6 | fast decay shift (τ=64 ticks) |
| 3 | KS | int 0..15 | 12 | slow decay shift (τ=4096 ticks) |
| 4 | KA | int 0..15 | 5 | activation leak shift (per tick) |
| 5 | THRESH | Q1.15 s | 0x6000 | fire threshold |
| 6 | REFR | int | 4 | refractory period (ticks) |
| 7 | COS_MIN | Q1.15 u | 0x2CCD (0.35) | link-admission affinity floor |
| 8–15 | spare | — | 0 | reserved |

### 7.4 tick scheduler — `q_tick_sched`

Free-running counter, `TICK_LEN = 2^TPW` cycles (default 4096), strobe at
wrap, phase = top 2 counter bits. Phase contract:

| phase | span (cycles) | guarantee |
|---|---|---|
| 0 TICK | 1024 | all cells complete decay sweep + leak (needs ~58) |
| 1 SETTLE | 1024 | weights quiescent; views are coherent here |
| 2 FIRE | 1024 | cells that crossed THRESH fan out effects |
| 3 DRAIN | 1024 | ring empties before next tick |

Phases are advisory (no hard interlock hardware — §12, limit 9); the TB
asserts the deadlines.

Fire rule (in core, at ST_TLEAK): `act ≥ THRESH && refr == 0` → send
`qm_effect(dat = act)` to every valid edge, `act ← 0`, `refr ← REFR`.

Activation integration on receive: `act ← sat( act + (w_new · payload) ≫ 15 )`
using the **post-update** weight (train-then-integrate order, one engine
pass).

---

## 8. Q-format policy

| Quantity | Format | Notes |
|---|---|---|
| activations (`act`, `pre`, `post`, payloads) | **Q1.15 signed** | −1.0 … +0.99997 |
| edge weights `wf, ws, w` | **Q1.15 unsigned, rectified** | [0, 0.99997]; readout saturates |
| `pre·post` | Q2.30 (magnitude+sign) | 16×16, one per train |
| eta dials | Q1.15 unsigned | increments `(ppm·η) ≫ 15` back to Q2.30 |
| `dot, Σx², Σy²` | Q2.30 in 40b (8 guard bits) | VW ≤ 256 safe |
| `mx, my` | Q1.15 | isqrt of shifted sums |
| cosine | Q1.15 signed, clamped | ±0.99997; parallel vectors clamp to 0x7FFF |
| THRESH | Q1.15 signed | compared against `act` |
| k-shifts (KF/KS/KA), REFR | plain ints | not fixed-point |

Rules:
1. Multiplies: one 16×16 (or 17×16) per engine stage. No DSP assumptions,
   no vendor multiply instantiation, ever.
2. Rounding: truncation (shift-right drops bits) everywhere, except
   saturation always follows — truncation bias is counted in the TB error
   budget rather than hidden by rounding logic.
3. Saturation: weights rectify at 0 and clamp at 0xFFFF; `act` clamps at
   ±full scale; `w = wf+ws` clamps at readout. Saturated values are legal
   states, not errors.
4. No floating point anywhere in rtl/. Float appears only in TB golden
   models.

---

## 9. Fabric-size distribution strategy

**The strategy is replication, not specialization.** One generic cell RTL,
identical everywhere; a cell's role is its dial values and its edge table,
both written through opcodes at runtime. No per-role RTL exists in this
proposal, by construction.

| Tier | Cells | Interconnect | Change vs default build |
|---|---|---|---|
| S | 2–8 | single ring (this entry's build: N=4) | none — parameters as shipped |
| M | 9–64 | two counter-rotating rings; `dst[0]` picks direction | fabric_top wiring only |
| L | 65+ | clusters of ≤16 rings; **gateway cells** bridge | gateway = same core + 2nd ring port adapter; still a cell (Law 2) |

Scaling parameters (all module-level, no code edits):

| Parameter | Default | Range |
|---|---|---|
| `AIDW` (id width) | 4 | ≤ 8 (256 ids) |
| `EDGES_N` (edge table) | 8 | ≤ 16 as reg-array; beyond → BRAM template swap |
| `VW` (cosine window) | 8 | power of 2, ≤ 256 |
| `PW` (word) | 16 | 16 shipped; Q policy written for PW=16 |
| `TPW` (tick length log2) | 12 | ≥ ceil(log2(EDGES_N·8)) |

Resource scaling: cell cost is linear in N; ring port is O(1) per node;
pipe slices O(N/2). Register-array edge table maps to LUTRAM at
EDGES_N ≤ 16; the synchronous-read template swap for inferred BRAM keeps
ports identical (build item, §12 limit 7).

Toolchain posture: everything targets open flow (iverilog/vvp,
verilator lint, yosys+nextpnr for iCE40/ECP5-class parts) with **zero**
vendor primitives — if a flow can't synthesize plain 1364-2005, the flow is
wrong, not the RTL.

---

## 10. Testbench plan

Golden-model method: each TB carries a `real`-arithmetic reference model of
the same math; pass criterion = mismatch count 0 within a per-module
tolerance, plus FSM-state-visit coverage counters dumped at end (no vendor
coverage; hand-rolled).

| TB | Target | Checks |
|---|---|---|
| tb_q_hebbian_edge | 7.1 | 10k random (pre,post) trains vs fixed-point golden ≤2 LSB; decay-only matches two-exponential closed form; rectify/saturate corners; handshake (args stable, done strobe) |
| tb_q_isqrt16, tb_q_divu | 7.2 helpers | exhaustive sweep at small args, 20k random at width; zerr case |
| tb_q_cosine_stream | 7.2 | random vector pairs VW ∈ {8,64} vs `real` cos, tol 2^-10; zero-vector err; back-to-back starts |
| tb_q_dialfile | 7.3 | reset defaults; write/readback; sync-read latency; fan-out wiring |
| tb_q_tick_sched | 7.4 | period, strobe width, phase boundaries |
| tb_q_link_ringport + tb_q_flit_pipe | §5 | deliver/transit/inject; bubble-after-consume; inject-vs-transit priority; back-pressure propagation; pipe correctness under contradicting ready |
| tb_q_cell_core | §6 | directed: bind→link→effect→view→tick; scan hit/miss; fire + refractory; NAK on bad op; view of every mux source |
| tb_fabric_smoke | fabric | **the acceptance test**: 4 cells on a real ring netlist; bind all, link A→B; 100 co-active effects train w past THRESH (verified via qm_view); tick until B fires; observe B's effect egress at its neighbors; then decay-only ticks shrink w below THRESH |
| tb_fabric_fuzz | fabric | random opcode streams (valid + garbage), protocol checkers (valid never dropped, payload stable, ring never deadlocks — watchdog), 10^5 flits |

Regression commands (Make targets, all open tools):

```
make test:  for each tb: iverilog -g2005 -o build/tb.vvp tb/tb_x.v rtl/*.v && vvp build/tb.vvp
make lint:  verilator --lint-only -Wall rtl/*.v
make synth: yosys -p "synth_* -top quilt_fabric_top" rtl/*.v   (optional, timing-unchecked)
```

Known CI note: iverilog was not installable in the authoring environment
(no root); the first CI action on merge is the compile gate
`iverilog -g2005 -tnull rtl/*.v`. Skeletons are hand-checked only (§12,
limit 11).

---

## 11. Honest limits

1. **Power-law decay is approximate.** `wf+ws` is a sum of two
   exponentials; it tracks a `t^-α` tail only between ~τf and ~10·τs
   (~2 decades with defaults). True `1/t` tails need log-domain state —
   a `q_hebbian_log` variant is sketched in docs, not built, not promised.
2. **Cosine is slow-path.** ~VW+95 cycles per estimate, serialized against
   other engine use by the core FSM. It is an estimator for link admission
   and views, not a per-beat attention score.
3. **No homeostasis.** Saturating Q1.15 with user-set eta: runaway
   co-activation clips at full scale rather than renormalizing. Dials are
   the operator's responsibility.
4. **Ring is half-duplex, 1 flit/cycle aggregate.** Fire fanout serializes
   (E cycles per firing cell); hot cells are throughput bottlenecks by
   design trade for simplicity.
5. **Comb ring port + pipe slices**: timing at N ≥ 8 on small parts is
   unverified until synthesis; pipe insertion interval is a placement
   datum, not proven.
6. **Single clock, sync reset.** CDC exists only inside the async-FIFO
   adapter, which is specified but not built in this entry.
7. **Edge table is a reg-array** (LUTRAM-shaped). BRAM template swap is
   planned and port-compatible but unexercised.
8. **Verilog-2005 flatness tax**: flit "structs" are comment conventions;
   port lists are wide. Accepted cost of the law.
9. **Tick phases are advisory**, not interlocked; a wedged cell could
   overrun phase 0. HW watchdog is a build item; TB asserts deadlines
   meanwhile.
10. **Cosine precision** ≤ 2^-10 (VW ≤ 64) vs golden — not a float
    substitute; near-orthogonal vectors quantize coarsely at Q1.15.
11. **No tool runs yet**: no iverilog/verilator/yosys execution in the
    authoring environment; every "verified" claim above is a plan with a
    named test, not a green checkmark. First CI action is the compile gate.
12. **Resource numbers are paper estimates** until the first yosys run.
13. **vMF means cosine-only**: κ (concentration) estimation needs log/exp
    tables — specified as future `q_logtab`, not built.
14. **Tier-L gateways are specified, not built**; the entry ships tier-S
    parameters and tier-M wiring notes.

---

## 12. Build order (if this entry wins)

1. M1: primitives (`q_hebbian_edge`, `q_isqrt16`, `q_divu`,
   `q_cosine_stream`) + their TBs — engines proven standalone.
2. M2: `q_dialfile`, `q_tick_sched` + TBs.
3. M3: `q_cell_core` directed TB (opcode-by-opcode).
4. M4: `q_link_ringport`, `q_flit_pipe`; 4-node ring netlist TB with
   protocol checkers.
5. M5: fabric smoke — train-to-fire-decay scenario, end to end.
6. M6: fuzz + verilator -Wall clean + yosys synth + adapters
   (byteframer, async-FIFO ingress).
