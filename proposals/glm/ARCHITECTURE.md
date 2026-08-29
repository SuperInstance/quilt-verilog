# proposals/glm — ARCHITECTURE.md
## The Chain-Quilt: cells, ladders, and one shared math tail

**Entry for the round-robin competition. Pure Verilog-2005 (IEEE 1364-2005), synthesizable
subset, zero vendor code.** Companion file: `RTL-SKETCH.md` (six real module skeletons).

---

## 0. What this entry bets on (and how it differs from a "normal" NoC entry)

Most fabric proposals reach for a crossbar or a mesh router. This one bets the opposite way:

1. **The network is the quilt.** There is no router RTL at all. Cells daisy-chain into a
   closed ring of single-beat flits with a 1-cycle bypass register. Scaling from 2 cells to
   2000 cells is instantiating more of the *same* cell and (optionally) more bridge-cells.
   Topology growth is a *generate-loop parameter*, not new source.
2. **Age buckets are the bits.** The Hebbian decay law `W = Σ 2^(-age/H)` is approximated by
   a counter ladder where bucket *i* carries the implied weight `2^-i`. The "multiply by the
   decay factor" is a **wire shift** — it costs nothing. Decay is one arithmetic shift per
   half-life. No exponential LUT, no per-event timestamps, no multiply.
3. **One shared math tail.** The only expensive arithmetic in the fabric — division, square
   root, `ln` — lives in one small sequential coprocessor (*math-tail*) time-multiplexed
   under the tick scheduler. The cosine unit is one signed multiplier + two accumulators;
   everything else queues for the tail. Transcendental cost is paid **once per fabric**,
   not once per edge.
4. **Saturate, never wrap.** A wraparound is a lie about magnitude. Every arithmetic
   operator saturates; every unit latches a sticky overflow flag readable via `qm_view`.
   The quilt may be wrong, but it is never silently wrong.

Everything below is sized for a bottom layer: small, streaming, tick-paced, dumb adapters.

---

## 1. Worldview: everything is a cell

### 1.1 The one ingress/egress contract: `qstream`

Exactly one streaming contract exists in the fabric. Any device, IO, or bridge enters as a
cell and speaks qstream on both sides. Verilog-2005 has no interfaces, so the contract is a
**naming convention + flit encoding**, enforced by review and by TB checkers:

```verilog
// qstream port group (per direction). DW = flit payload width (default 16).
input  wire          s_valid;    // sink side (I accept)
output wire          s_ready;
input  wire [FLIT_W-1:0] s_flit; // {meta, data}, see §1.2

output wire          m_valid;    // source side (I offer)
input  wire          m_ready;
output wire [FLIT_W-1:0] m_flit;
```

Contract rules (checked in every TB):

- `s_ready` must **not** depend combinationally on `s_valid` (and vice versa for the
  source side) — no combinational loops through the chain, ever.
- A flit is transferred exactly when `valid && ready`. Valid may not drop before transfer.
- One beat = one flit = one complete quilt operation. No multi-beat transactions in v1.
- Adapters are **thin and dumb**: they pack device bytes into flit payloads and select a
  destination id from a configuration register. They own CDC and pacing; the fabric is
  single-clock.

### 1.2 Flit format (the intercell link protocol)

A flit is one packed word: `{meta, data}`.

```
data [DW-1:0]                    payload (Q1.15 value, or address/param word)

meta:
  op  [2:0]   000 qm_bind    001 qm_link     010 qm_effect
              011 qm_view    100 qm_tick     101 resp
              110 err        111 rfu
  dst [CID_W-1:0]   destination cell id (resp/err route to original src)
  src [CID_W-1:0]   origin cell id
  ttl [3:0]         hop count, initialized to N_CELLS at injection; a flit
                    arriving at ttl==0 is dropped and an err flit is sent to src
```

Opcode semantics at the bottom layer:

- **qm_bind** — configure a cell's binding: which adapter stream feeds its ingress, which
  dial map an incoming activation touches. Payload = capability/config word. This is how
  "any IO enters a cell": the bind writes the thin adapter's steering register.
- **qm_link** — a cofire event on the edge (src→dst). The emitting cell find-or-creates
  the edge record keyed by `dst` and pulses the Hebbian ladder (`C_0 += 1`). Payload =
  `{edge hint, base nibble}`.
- **qm_effect** — a touch: payload is a signed Q1.15 activation applied to dst's dial /
  activation registers. In v1 the *emission* of an effect along an edge is itself the
  cofire that strengthens it (documented simplification, §7).
- **qm_view** — non-destructive read: `{kind, addr}` selects dial / edge strength /
  sticky-status / cos result; response comes back as a `resp` flit to `src`.
- **qm_tick** — per-cell scheduler programming (wake period, leak rate) or a forced tick.
  The global heartbeat itself is hardware (§3.5), not a flit.

### 1.3 Routing: minimal on purpose

- Cells form a **closed ring**: cell *i* drives cell *i+1*, cell *N−1* wraps to cell 0.
  Each cell consumes flits whose `dst == MY_ID`, else registers them to its egress
  (1 cycle per hop, bypass register).
- The fabric's external ingress injects at the ring seam **with wrap priority**: a
  returning wrapped flit always beats external injection; external ingress simply sees
  `ready` deassert. No in-ring flit ever waits on the seam → no structural deadlock,
  no starvation of ring traffic (external injection is backpressured, which is the
  correct trade for a bottom layer).
- `ttl` catches misaddressed flits; drops raise a per-cell sticky counter visible via
  `qm_view`.
- **Bridges are cells.** Two rings join by instantiating a `qs_bridge` cell on each ring
  that repeats flits whose `dst` matches the other ring's id-space. It is the same cell
  RTL with a bind configuration — no new network code. This is the distribution story:
  the fabric grows by *quilting*, same as everything else.

---

## 2. Module hierarchy

```
qs_fabric                     generate-loop ring of N cells + seam + tick broadcast
├── qs_tickgen (×1)           prescaler → tick strobe, half-life strobe, tick counter
├── qs_cell (×N, identical)   one quilt node
│   ├── qs_cell_core          opcode FSM: decode, scan, execute, respond, bypass
│   ├── edge RAM (inferred)   E_LOG2 deep × {dst, ladder, base, flags}
│   ├── qs_hebb_edge (×1)     ladder ALU: load / event / age-shift / readout  (§3.1)
│   ├── qs_ln (×1)            LOD + LUT + interpolate, Q4.12 out              (§3.2)
│   ├── qs_cos (opt.)         streaming MAC + norms, drives math tail         (§3.3)
│   ├── qs_dial (×D)          saturating dial registers with leak             (§3.4)
│   └── wake countdown        per-cell tick scheduler slice                    (§3.5)
├── qs_bridge (opt.)          ring↔ring repeater — a cell with a bind config
└── qs_adapter_* (thin)       uart / spi / gpio / eth packers → qstream
qs_mathtail (×1 per fabric)   shared sequential divider / sqrt coprocessor
```

Principles: one ladder ALU and one ln unit **per cell** (time-multiplexed over its edges),
one math-tail **per fabric** (time-multiplexed over cells, granted at tick boundaries).
Small designs can drop `qs_cos` and the math-tail entirely via generate-if (`HAS_COS`,
`HAS_MT`) and still run bind/link/effect/view/tick — intelligence degrades gracefully,
it never disappears.

---

## 3. Intelligence primitives in fixed-point RTL

### 3.1 Hebbian edge: age-bucket ladder (`qs_hebb_edge`)

**Target law.** Edge weight `W(t) = Σ_events 2^(-age_e/H)`, `H` = half-life in ticks
(the "90 days" of the quilt — wall-clock meaning comes from the tick divider, §7).

**Approximation.** Keep `K` counters `C_0..C_{K-1}` of `B` bits each.
- A cofire event does `C_0 ← C_0 + 1` (saturating; overflow sets a sticky lost-event flag).
- Every half-life (`hl_strobe`): the whole ladder shifts one class older,
  `C_i ← C_{i-1}`, `C_0 ← 0`; `C_{K-1}` retires.
- Bucket *i* therefore holds events with age in `[i·H, (i+1)·H)`, and carries the
  **implied weight `2^-i`**.

**Readout.** `Ŵ = Σ_i C_i · 2^-i` — assembled by an adder tree that places bucket *i*'s
bits at offset `(K-1-i)·B` in a `K·B`-bit word `P`. The multiply-by-`2^-i` is *wiring*.

**Error is provable, not hand-waved:**
- Per event, `floor(a/H) ≤ a/H < floor(a/H)+1` ⇒ `2^-a/H ≤ 2^-floor(a/H) < 2·2^-a/H`,
  so **`W_exact ≤ Ŵ ≤ 2·W_exact`** — a bounded staircase over-estimate, no drift, no bias
  machinery needed.
- Counts are integers and weights are exact powers of two ⇒ the readout sum itself has
  **zero rounding error** in fixed point.
- Retirement tail: an event older than `K·H` contributes `< 2^-K` of a fresh event
  (K=12 → < 2.4·10⁻⁴, i.e. ~12 half-lives ≈ 3.6 years of 90-day halves).
- Storage: `dst (CID_W) + K·B + base (8) + flags` per edge. Std profile: 12+72+10 ≈ 94
  bits/edge; 64 edges/cell ≈ 6 kb — one inferred block RAM.

**Strength.** `S = base + ln(1 + Ŵ)` in Q4.12 (`base` is Q4.4 promoted by a constant
shift). `ln` below. S is what routing preference and `qm_view` report; `Ŵ` is what decays.

**Cascade variant (explicitly future work, not claimed):** giving each bucket its own
geometric half-life (Fusi/Drew/Abbott cascade) yields a power-law tail from the same
ladder. Parameter hook `LADDER_MODE` is reserved; v1 ships the faithful staircase only.

### 3.2 `ln` unit (`qs_ln`)

`ln(1+Ŵ)`: form `Y = 2^FRAC + P` (caller's fractional scale), then
`ln(Y) = e·ln2 + ln(m)` with `Y = m·2^e`, `m ∈ [1,2)`:
1. Leading-one detect + barrel normalize → `e` (7 bits) and mantissa `m`.
2. 16-entry `ln(m)` LUT (Q4.12, `case`-ROM — no `initial` blocks in rtl/) with linear
   interpolation on the 4 sub-fraction bits: error ≤ ±2 LSB at Q4.12
   (≤ ±5·10⁻⁴ relative — the curvature term `(Δ²/8)·max|ln''|`).
3. `e·ln2` from a second tiny LUT (or constant multiply); the caller's scale constant
   `FRAC·ln2` is subtracted via a **constant function** evaluated at elaboration.
Latency ~4 cycles, no divider, no multiplier wider than 12×4.

### 3.3 Streaming cosine (`qs_cos` + shared `qs_mathtail`)

Compare an incoming activation stream `x_i` (Q1.15) against a stored pattern `p_i`:

- **Streaming phase** (one signed multiplier, two squaring accumulators):
  `A += x·p`, `X2 += x²`, `P2 += p²` — all in `ACC_W = 2·DW + log2(MAXN) + 2` guard bits
  (Q3.29-class headroom; saturation, never wrap, sticky on rail-touch).
- **Tail phase** on the shared math-tail, in sequence:
  `sX = √X2`, `t = A / sX`, `cos = t / sP` — two sequential divides and two
  shift-subtract square roots, **no wide multiplier anywhere** (the classic 96-bit
  `X2·P2` product is deliberately avoided).
- Result clamped to [−1, 1) Q1.15. Total error ≤ ~3 LSB (2 from the tail's last-bit
  rounding, 1 from the final clamp), verified against a real-arithmetic golden model in TB.
- Latency: `N + ~3·ACC_W/2` cycles ≈ 200 for N=32, DW=16 — irrelevant at tick pace.

Bold consequence: the whole cosine affair costs **one DSP-ish multiplier per cell** and a
shared ~150-cycle sequential tail. vMF concentration (κ) estimation is *not* implemented;
cosine is the sufficient statistic v1 ships (§7).

### 3.4 Saturating dial registers (`qs_dial`)

A dial is a signed Q1.15 register in [−1, 1) with two operations:
- **nudge**: saturating add of a signed delta (wrap is a lie; rail-touch latches sticky).
- **leak** (on the cell's tick event): `d ← d − sign(d)·(|d| ≫ LEAK_SH)` — exponential
  return toward center with half-life `≈ ln2·2^LEAK_SH` ticks — plus a **deadband snap**
  (`|d| < DEADBAND → 0`) so alternating nudges can't keep a dead dial flickering at ±1.

### 3.5 Tick scheduler (`qs_tickgen` + per-cell wake)

One global generator: prescaler (`TICK_DIV`, reload down-counter, any value — no modulo)
produces `tick_stb`; a second down-counter produces `hl_stb` every `HALF_LIFE_TICKS`;
both plus the free-running tick count are broadcast on a thin tick bus to all cells.
Per cell, a **wake countdown** (programmable via `qm_tick`) fires the cell-local tick
event: dials leak, the edge RAM walks address-by-address through the ladder ALU applying
the age-shift (one edge per cycle, `E` cycles per half-life-class boundary — scheduled
in idle slots and preemptible at slot granularity by opcode traffic). Large-fabric
time-wheel RAM is a generate-if future (`HAS_WHEEL`), not claimed for v1.

---

## 4. Q-format and saturation policy

| Signal class | Format | Notes |
|---|---|---|
| Activations, dials, cos result | **SQ1.15** | saturating signed, rails ±(1 − 2⁻¹⁵) |
| MAC / norm accumulators | **SQ3.29** (`ACC_W=48`) | 4× headroom before saturation |
| Ladder counts | unsigned integer, `B` bits | implied weight 2⁻ⁱ per bucket |
| Edge readout `P` | unsigned, `K·B` bits | `Ŵ = P·2^-(K-1)·B` |
| Strength `S = base + ln(1+Ŵ)` | **Q4.12** | range to ~8 covers ln of any sane W |
| ln internals | Q6.12 | headroom for the scale constant before subtraction |

Policy, in five lines:
1. **Every add/sub/multiply saturates** at its format's rails. Wrapping is banned by
   style rule and by TB checker.
2. Accumulators carry log2(N)-ish guard bits so saturation is a *rare event*, not a
   routine one; when it happens it is *visible*.
3. **Sticky flags** (`ovf`, `lost-event`, `ttl-drop`) latch per unit, never self-clear,
   and are readable via `qm_view` — the quilt can be audited in operation.
4. Shifts toward zero (leak, decay) are truncating by design — decay is *supposed* to
   forget.
5. Saturation happens at operator boundaries, not "somewhere later": a value on a wire
   is always a legal value of its format.

---

## 5. Distribution: same RTL, any size, zero source edits

All size dependence is parameters with legal floors; optional units hide behind generate-if:

| Parameter | Tiny | Std | Large | Meaning |
|---|---|---|---|---|
| `N_CELLS` | 2 | 16 | 128/ring | ring length (generate loop) |
| `CID_W` | 4 | 8 | 12 | cell id width (bridges extend) |
| `DW` | 16 | 16 | 16 | flit payload width |
| `E_LOG2` | 4 | 6 | 8 | edges per cell (RAM depth) |
| `K`, `B` | 8, 4 | 12, 6 | 16, 8 | ladder depth/count bits |
| `HALF_LIFE_TICKS` | 2⁹ | 2¹⁶ | 2²⁴ | the "90 days" in ticks |
| `TICK_DIV`, `LEAK_SH`, `DEADBAND` | tuned per fabric | | | scheduler/dial character |
| `HAS_COS`, `HAS_MT`, `HAS_WHEEL` | 0 | 1 | 1 | generate-if unit enables |
| `REG_SLICE_EVERY` | 0 | 0 | 8 | insert pipe register every S links |

- **Small → large is a wrapper edit** (parameter overrides in a profile top), never an
  rtl/ edit. Defaults = Std profile.
- Beyond one ring: add `qs_bridge` cells — same cell RTL, a bind config, and a second
  ring; id-space partitioning is by `CID_W` per ring. There is no "large fabric mode"
  in the source because there is no large/small distinction in the source.
- Timing at scale: the ready chain is the only combinational path that grows with N;
  `REG_SLICE_EVERY` inserts a register slice (costing 1 cycle on that link) so timing
  closure is a parameter, not a rewrite.

## 6. Per-module testbench plan (iverilog / verilator)

Conventions: `tb/tb_<module>.v`, golden models in **real arithmetic** (testbenches are
exempt from the synthesizable rules), a shared `tb/qchk.v` with the qstream protocol
checker task and the pass/fail counter. Regression: `make regress` →
`iverilog -g2005 ... && vvp` per TB; `verilator --default-language 1364-2005
--lint-only -Wall` over rtl/ as the CI gate (and `--binary` smoke runs where available).

| TB | What it proves | Pass criteria |
|---|---|---|
| `tb_qs_dial` | saturate-never-wrap, leak curve, deadband snap | hammer 10⁵ random nudges: no wrap (bit-level check vs saturating model), leak half-life within ±1 tick of ln2·2^LEAK_SH, \|d\|<DEADBAND ⇒ 0 |
| `tb_qs_hebb_edge` | ladder = staircase of Σ2^(-age/H) | random event streams vs real golden model: `W_exact ≤ Ŵ ≤ 2·W_exact` at every strobe boundary; retirement ≤ 2⁻ᴷ; bucket-0 saturation flagged, never silently dropped |
| `tb_qs_ln` | LUT+interp accuracy | sweep all 2¹⁶ input codes: \|err\| ≤ 2 LSB Q4.12 vs `$ln` real model; scale-constant subtraction exact |
| `tb_qs_mathtail` | divider/sqrt last-bit correctness | exhaustive small operands + random wide: ÷ exact-quotient-truncated ±1 ulp, √ within ±1 ulp |
| `tb_qs_cos` | streaming cosine | random ±full-scale vectors, N∈{1..64}: \|cos − golden\| ≤ 3 LSB; sticky set iff rail touched |
| `tb_qs_tickgen` | prescaler & half-life strobes | strobe spacing == programmed period for non-power-2 values (no modulo bugs); tick count monotone |
| `tb_qs_cell_core` | opcode FSM | per-opcode directed sequences + randomized opcode streams with a reference model of the edge RAM: link increments the right ladder, view returns `base+ln(1+Ŵ)`, unknown dst → ttl err; bypass latency exactly 1 cycle/hop |
| `tb_qs_fabric` | ring delivery | N=2 and N=16, random unicast + resp traffic, scoreboard: exactly-once, in-order per (src,dst), no valid-drop, `s_ready` independent of `s_valid` (concurrent checker), wrap-priority backpressure behavior |
| `tb_qs_bridge` | two-ring routing | dst in other ring's space crosses exactly once, ttl consumed across seam |

Every module in rtl/ must appear in this table before it is allowed to exist (README law 5).

## 7. Honest limits

1. **Staircase decay is an over-estimate by up to 2×** on clustered old events (bounded,
   proven, §3.1) — the quilt remembers slightly *more*, never invents weight.
2. **Horizon is K·H.** 12 half-lives, then events are gone (tail < 2⁻¹²/event). Longer
   memory costs linearly more ladder bits — the cascade variant would break this trade
   but is future work.
3. **Bucket-0 saturation** drops cofires beyond `2^B−1` per half-life per edge (flagged,
   counted, visible — but dropped).
4. **ln is ±2 LSB** at Q4.12; cos is ±3 LSB. If the quilt ever needs better, the LUTs
   deepen — the interfaces don't change.
5. **The ring is O(N) latency and shared bandwidth.** No multicast, no QoS, no
   cut-through. Bridges fix scale, not physics. Sustained saturation backpressures
   external injection by design.
6. **Edge lookup is a linear scan** (O(E) cycles). Fine at E ≤ 256 and tick pace; a hash
   index is the first thing v2 would buy.
7. **Single clock, no CDC inside the fabric.** Adapters own synchronization; the contract
   says so and the TB checks they don't leak comb paths.
8. **No RTC.** "90 days" is `HALF_LIFE_TICKS` divided by tick rate; wall-clock truth is a
   system configuration fact, not a silicon fact.
9. **No timing-closure claims.** Frequencies are target-dependent; the parameter strategy
   (§5) exists precisely because this entry refuses to promise Fmax.
10. **vMF/κ estimation, cascade ladders, time-wheel scheduler: not implemented, not
    claimed.** Hooks exist; code doesn't. This entry ships what it can prove.

## 8. Build order (if this entry wins)

1. `qs_dial`, `qs_tickgen` + TBs (week 1 — zero dependencies, style-proof the repo)
2. `qs_hebb_edge` + `tb_qs_hebb_edge` (the staircase bound *is* the acceptance test)
3. `qs_ln`, `qs_mathtail` + TBs
4. `qs_cell_core` with edge RAM, opcodes bind/link/view first
5. `qs_fabric` ring + scoreboard TB; then `qs_cos`; then effect path end-to-end
6. profiles (tiny/std/large wrappers) + verilator lint gate in CI
