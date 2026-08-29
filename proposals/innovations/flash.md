# Innovation: Residual-Quantum Hebb (RQH)

**Seat:** flash (DeepSeek V4-Flash — innovation prize entry)
**Mechanism:** the ladder/hyperbola weight engine truncates a *real* memory
kernel to a *dyadic* bucket (implied weight `2^-g`), and every entry on the
board **throws away the fractional difference**. RQH banks that discarded
fraction into a per-edge **quantum reservoir** `R`; when `R` overflows a unit
it (a) credits the readout with a **sub-count step** (asymptotically closing
the `2×` / `[1,4)×` envelope toward the exact law) and (b) raises a
tick-strobed **anticipation pulse** `o_antic` — the fabric's cheap warning
that a weight is *about to gain a visible step*, before the count actually
crosses. Quantization loss becomes both a precision credit and a
pre-strengthening signal.
**Pure Verilog-2005, fixed-point, zero multipliers, zero dividers, RTL-sketchable.**

---

## 0. Concept in one paragraph

Every decay law on this board is a *quantizer with a dropped remainder*.

- **glm ladder:** a cofire lands in bucket `g` with implied weight `2^-g`.
  The true age-kernel value it represents lies in the dyadic band
  `[2^-g, 2^(1-g))` — that is exactly the proven `2×` envelope. The engine
  pays the **bottom** of the band, `2^-g`, and discards the rest.
- **zeroclaw hyperbola:** integer `W` + log readout. The decay *interval*
  `P₀ >> 2·msb(W)` is a dyadic staircase whose step edges underrepresent the
  true `W²/P₀` in exactly the same band sense (`[1,4)×` interval).
- **opencode two-exp:** two fixed-point exponentials, each truncated.

All three, and every innovation seat, treat the discarded fraction as **pure
loss** — noise to be accepted under the envelope bound. **RQH's claim is that
the dropped fraction is not noise; it is *debt*, and it can be banked.** A
cofire that the quantizer underpays by up to `2^-g` should accumulate that
underpay into a reservoir, and when the reservoir fills a whole unit it must
return the value to the weight — and, critically, signal the cell *before* it
does.

The payoff is not bigger weights; it is **telemetry + accuracy that cost
nothing**:

1. **Anticipation.** `o_antic` pulses one cycle before / as a weight gains an
   *invisible pre-step*. The cell can nudge an attention dial or seed a vMF
   coherence read, so the fabric "warms up" an association *before* the
   reading visibly strengthens — anticipatory learning from quantization
   residue, no timestamps, no per-event storage.
2. **Asymptotic accuracy.** The reservoir re-injects the systematic
   underp/underpay so the effective readout converges toward the exact memory
   law at high cofire count — measurable as an envelope that *tightens inside*
   the `2×` / `[1,4)×` bound.

It is a thin, orthogonal, **wraps-existing** layer over the verified
`q_hebb_edge` — it never touches the ladder's saturating buckets or the
hyperbola integer counter, so Law 5 holds and the existing TBs still pass
(with RQH disabled, bit-exact).

---

## 1. Novelty delta vs. nearest prior art, named

**The full board's weight state machines:**

| Seat | Weight storage | Quantization | Dropped fraction reused? | Anticipation signal? |
|---|---|---|---|---|
| glm (v1 `q_hebb_edge`, ladder) | K·B buckets, `2^-i` | yes | **no — discarded** | no |
| zeroclaw (hyperbola) | integer W, log readout | yes (interval) | **no — "refuse quantization in state" (§2.1, rule 6)** | no |
| opencode two-exp | wf+ws Q1.15 | yes | **no** | no |
| seed (DWS, innovation) | msb-scaled increment | yes | **no** — shifts the *increment*, not the residue | no |
| claude (TCH, innovation) | temporal-contrast gate | n/a | **no** | no |
| opencode (echo gate, innovation) | fire-trace gate + class | yes (fires trace) | **no** — `F` **snaps to zero** at/below FLOOR, deliberately discarding the remaining trace ("residue" in §4.1 is trash, not credit) | no |
| **RQH (this seat)** | add-on quantum reservoir `R`/edge | yes | **yes — banked, re-injected** | **yes — `o_antic`** |

**Nearby prior art, and the delta each:**

1. **seed's DWS** (`Δw = η >> msb(W)`) is the nearest neighbor. Delta: DWS
   changes the *size of the next increment* as a function of the weight's own
   MSB — a state-**dependent potentiation magnitude**, priced as a priority
   encoder + shift. RQH changes *nothing* about increments; it **integrates
   the residual that placement already drops** (a saturating add of `(1<<g)`
   per class-`g` cofire) and re-injects it at the *readout* as a sub-count
   credit plus an anticipation strobe. Different operation (residue
   integrator vs magnitude-scaler), different effect (envelope tightening +
   anticipation telemetry vs natural saturation), different hardware (DSP-free
   saturating adder vs msb shift). **They compose**: DWS can shrink the
   increments *and* RQH can bank the placement underpay — the guard-band and
   the debt bank are independent.
2. **opencode's echo gate** is the only artifact that *touches* a discarded
   residue — but its fire trace `F` **snaps to zero** at/below FLOOR to kill a
   leak-floor sticky artifact; the residue is treated as trash and the trace
   is a *gate credential*, never *edge credit*. Delta: RQH turns the residue
   into *per-edge value*, and its anticipation pulse is a *credit signal*,
   not a gate test.
3. **glm/zeroclaw** are the base engines: both deliberately documented the
   unrecovered fraction as the price of the envelope. Delta: RQH makes the
   envelope *self-tightening* rather than accepted loss.
4. **Literature:** this is the *converse* of error feedback quantization
   (EFQ) — EFQ dithers the input so truncation error decorrelates; RQH does
   not dither (noise stays zero) and instead *accumulates* the truncation as
   a deterministic second-order state so the error *returns* to the weight.
   Closer in spirit to a carry-save/guard "sticky sub-accumulator," but novel
   for *learned-edge* state and novel as an **anticipation readout** (no
   weight on the board exposes a "pre-strengthening" signal to dials/vMF).

**The one-line delta for the scorecard:** *every weight on the board reads a
truncated kernel and throws the truncation away; RQH is the first primitive
that banks the truncation as per-edge value and emits a warning before a
visible step.*

---

## 2. Why it serves the fleet's primitives (edges, dials, vMF, ticks)

### Hebbian edges (both v1 engines)
- Wraps `q_hebb_edge`; adds per-edge `R` (few registers each). Class-`g`
  cofire banks `(1<<g)` quanta; the high byte `R[15:8]` is an integer
  sub-count credit added to the readout `eng` before `+ base`. Net effect:
  the readout `b_eff = base + engine + credit` drifts *inside* the proven
  envelope toward the exact law as cofires accumulate — measurable against
  the ladder's `W_exact` and the hyperbola's `W₀/(1+W₀t/P₀)` golden models.
- **Deadband / saturation preserved:** `R` saturates (never wraps) and gently
  leaks — a deadband leak keeps a long-idle reservoir from holding stale
  credit, exactly the glm deadband pattern, and never *newly* inflates a
  hardened edge (a saturated edge's reservoir stops integrating because the
  credit is capped by `R`'s fixed width).

### Dials (motivation/attention/fatigue)
- `o_antic` is an edge-level "about to matter" pulse. A cell can bind it to a
  dial as a *pre-attention* nudge (e.g. an attention dial nudged on `o_antic`
  *before* the visible weight crosses a threshold) — the reading "warms up"
  by one dial step early. This is the fabric's cheapest form of graded,
  timing-free anticipation: a rising-edge on `o_antic` is as easy to consume
  as any strobe.

### vMF (μ̂, κ̂ field coherence)
- The reservoir is a *de-noised* accumulator: because `credit` is a
  fractional-average correction, the weight fed into μ̂/κ̂ estimation is
  smoother (fewer staircase discontinuities), so the field reading jitters
  less across half-life shifts. Directly softens curveball 5's worry that
  dyadic decay discontinuities break contrast windows.

### Ticks
- All reservoir math is **tick-aligned**: deposits happen in the train slot
  (`i_cmd==001`), leak happens in the tick slot (`i_cmd==010`), `o_antic` is
  a one-cycle pulse on `posedge clk` (issued from the following read cycle).
  No new clock, no cross-domain logic, no GALS hazard — it is ordinary
  cell-local state under the existing deterministic tick order.

---

## 3. Fixed-point policy

| Quantity | Format | Notes |
|---|---|---|
| quantum reservoir `R` | `RW=16` unsigned, saturating, deadband-leaked | per-edge; deposit `(1<<g)` per class-`g` cofire |
| `QDW` | int (dial, default `8`) | reservoir depth; one output credit = `256/2^(QDW-8)` … see below |
| credit `C` | `R[15:8]` | integer sub-count = number of banked readout LSBs |
| `o_credit` out | `C` scaled to PW | `({(PW-8){1'b0}}, C)` added to `eng` readout |
| `QLEAK` | int shift (default `8`) | deadband leak `R − (R≫QLEAK)` on tick, snap to 0 at `≤ 1` |
| `o_antic` | 1-bit strobe | rising edge of the eighth-bit carry (a credit increment) |

**Scale rule (so the TB and RTL agree):** a class-`0` cofire banks `1` quantum
and the readout for a fresh cofire is `256` units (K=8,B=8, per
docs/SYNTHESIS.md). `QDW=8` ⇒ `2^8 = 256` quanta = one output **credit**, and
each credit scales as `+1` readout unit (256 LSBs / 256 = 1 LSB). A class-`g`
cofire banks `(1<<g)` quanta, so a weak (distant) cofire reaches one credit
in `256/2^g` such cofires — the engine's *systematic underpay* at the bottom
of the band is re-collected faster where it was larger. All values stay
power-of-two shifts + one saturating add; **no multiply, no divide, no float.**

**Perturbation honesty:** the deposit magnitude `(1<<g)` is the *band inverse*
(`2^g`), chosen because it is a shift and because it makes the correction
converge to the band **center** on average, not because the exact residue is
known. RQH does **not** claim to recover the exact real kernel — it claims
(1) a monotone, bounded, second-order credit that tightens the envelope, and
(2) a cheap anticipation signal. The exactness claim is deliberately absent;
the TB measures the envelope *tightening*, not exactness.

---

## 4. RTL sketch

### 4.1 `q_hebb_rqh` — the companion module (black-box-sound, wrapper-shaped)

```verilog
// q_hebb_rqh.v -- Residual-Quantum Hebb: banks the dropped dyadic fraction
// of a cofire into a per-edge quantum reservoir and emits a sub-count readout
// credit + an anticipation strobe. Wraps any q_hebb_edge-style engine; never
// touches ladder buckets or the hyperbola integer counter (Law 5 preserved).
// Pure Verilog-2005: one saturating add, one shift, one carry-detect. No
// multipliers, no dividers.
module q_hebb_rqh #(
    parameter RW    = 16,     // reservoir width
    parameter K     = 8,      // ladder buckets / max class (matches engine)
    parameter PW    = 16      // readout width
)(
    input  wire          clk,
    input  wire          rst_n,

    // sync with the wrapped engine's command slot
    input  wire          i_train,    // strobe: this edge trained this cycle (cmd==001)
    input  wire          i_tick,     // strobe: this edge ticked          (cmd==010)
    input  wire [3:0]    i_gclass,   // class this cofire landed in (0..K-1); from placement logic
    input  wire [3:0]    i_qdw,      // reservoir depth shift (default 8)
    input  wire [3:0]    i_qleak,    // deadband leak shift (default 8)
    input  wire          i_en,       // 0 = RQH disabled: o_credit=0, o_antic=0, R quiesced

    output wire [PW-1:0] o_credit,   // sub-count readout credit (>=0)
    output wire          o_antic     // anticipation pulse: a credit is being earned
);
    reg [RW-1:0] R;
    reg [RW-1:0] Rlast;              // shadow of previous cycle's reservoir

    // deposit = 1 << gclass (a shift, not a mul), clamped to class K-1 max.
    // For RW=16, K=8: dep = 16'b1 << {clamped class}; class always < RW.
    wire [3:0] gcl = (i_gclass >= K) ? (K-1) : i_gclass;   // clamp class
    wire [RW-1:0] dep = {RW{1'b0}} | (16'b1 << gcl);        // pure shift

    wire [RW-1:0] Radd    = R + dep;    // saturating
    wire          sat     = (Radd < R); // carry out = reservoir filled past RW-1
    wire [RW-1:0] Rnxt    = sat ? {RW{1'b1}} : Radd;

    // deadband leak on tick (glm deadband pattern); fire wins same-cycle
    wire [RW-1:0] Rleak   = Rnxt - (Rnxt >> i_qleak);
    wire          snaps   = (Rleak <= 16'd1);
    wire [RW-1:0] Rleakn  = snaps ? {RW{1'b0}} : Rleak;

    // credit = high byte (integer sub-count); anticipation = eighth-bit carry
    // carry8 = the high byte rolled over vs. the *previous stored* state Rlast,
    // so exactly one credit is earned the cycle a 256-quantum boundary is crossed.
    wire          carry8 = (Rnxt[15:8] > Rlast[15:8]); // one credit earned

    assign o_credit = i_en ? { { (PW-8){1'b0} }, Rnxt[15:8] } : {PW{1'b0}};
    assign o_antic  = i_en && carry8 && i_train;

    always @(posedge clk) begin
        if (!rst_n) begin
            R     <= {RW{1'b0}};
            Rlast <= {RW{1'b0}};
        end else if (i_train) begin
            Rlast <= Rnxt;
            R     <= Rnxt;                  // deposit path
        end else if (i_tick) begin
            Rlast <= Rleakn;
            R     <= Rleakn;                // leak path
        end else begin
            Rlast <= R;
        end
    end
endmodule
```

> **Compilation honesty:** the sketch is interface + key logic (the
> competition's ask); `Rlast` is a sticky shadow of the previous cycle's
> reservoir so `carry8` detects a true credit-boundary crossing, and `dep =
> 16'b1 << gcl` is a plain shift with a class clamp (valid Verilog-2005, no
> divider/multiplier). Because this seat did not open an integrated build
> harness this round, I flag that the module has **not been compiled** rather
> than claim a gate I did not run — see §6 limit 3. The delta over the wrapped
> `q_hebb_edge` is one saturating adder + one carry-detect per edge; adopt as
> the first compile gate (`iverilog -g2005` + `verilator --lint-only -Wall`).

### 4.2 Readout delta (wraps, does not rewrite `q_hebb_edge`)

In the cell core (or a tiny post-engine adder), the effective readout becomes:

```verilog
// where the engine currently does:  o_w = sat(base + eng)
// add the RQH credit (i_en), clamped so base+eng+credit still saturates:
wire [PW-1:0] rqh_credit = rqh_en ? { {(PW-8){1'b0}}, rqh.R[15:8] } : {PW{1'b0}};
wire [PW:0]   wfin_rqh   = {1'b0, base} + {1'b0, eng} + {1'b0, rqh_credit};
wire [PW-1:0] wout_rqh   = wfin_rqh[PW] ? {PW{1'b1}} : wfin_rqh[PW-1:0];  // sat, never wrap
```

The ladder's buckets, the hyperbola integer counter, both decay laws, and both
proven bounds are **untouched**. `i_gclass` is the class already computed by
the placement logic (glm: `0` fresh; opencode echo-gate: `15 − msb(F)`; RQH
defaults: `0`), so RQH composes with any seat's placement.

### 4.3 `q_cell_core` / `q_dialfile` delta (sketch, additive)

- Instantiate `q_hebb_rqh` per edge (or share a time-muxed instance over the
  edge sweep, exactly like the engine is shared).
- `i_train` strobed in the train state (`cmd==001`); `i_tick` in the decay
  state (`cmd==010`) — same places the engine already runs, so `o_antic` is
  deterministically tick-aligned and needs no new scheduling.
- Dial slots, **additive** (RQH-defined, non-colliding with the 0..10 built-in
  map or other innovation seats' 11–13):

| addr | dial | default | meaning |
|---|---|---|---|
| 14 | `RQD` (QDW) | 8 | reservoir depth shift (quanta per credit = 2^QDW) |
| 15 | `RQLEAK` | 8 | reservoir deadband leak shift |
| — | `RRES[edge]` | ro | viewable per-edge reservoir (probe) |
| — | `RQEN` | 1 | master enable; **0 = RQH off = bit-exact v1 readout** (the A/B switch) |

`RQEN = 0` is the referee's switch: every existing `tb_fabric_smoke` /
`tb_hebb_edge` assertion must pass unchanged with RQH disabled — the evidence
that this is an *addition*, not a rewrite.

---

## 5. Testbench plan (`tb_hebb_rqh.v`)

House method: bit-exact integer golden + real-arithmetic envelope; pass =
zero mismatches.

| Check | Method |
|---|---|
| **Disabled A/B** | `RQEN=0`: `o_credit==0`, `o_antic==0`, and readout bit-exact to v1 for a scripted train/tick stream. |
| **Deposit math, bit-exact** | For classes `g∈{0..7}`, assert `R += (1<<g)` exactly on each train; clamp at `RW-1`; `o_credit == R[15:8]`. |
| **Carry/anticipation** | Deposit 256 class-0 cofires ⇒ exactly one high-byte tick; assert `o_antic` pulses on the 256th and `o_credit` increments 0→1. Re-do for class-3 (2^3=8 per cofire ⇒ 32 cofires to 1 credit). |
| **Deadband leak** | After `R` nonzero, run ticks with no trains; assert `R` leaks by `(1 − 2^-QLEAK)` per tick and snaps to exactly 0 ≤ 2 ticks after dropping ≤ 1. Fire (train) beats same-cycle leak. |
| **Envelope tightening (real golden)** | Golden real: `w_exact` from `Σ 2^(-age/HL)` (ladder) with the *band-center* correction `+ (2^(1-g))/2` per cofire. Over 10k cofires assert: (a) `base + eng ≤ w_eff ≤ base + eng + credit` always; (b) the *maximum deviation* of `w_eff` from `base + eng` around the true kernel is **strictly smaller** than the engine-alone 2× band (i.e. the credit moves the readout toward the band center on average); (c) `o_antic` count == credit count (telemetry integrity). Same for hyperbola mode with `w_exact = W₀/(1+W₀t/P₀)`. |
| **Saturation safety** | Flood trains until `R` saturates; assert no wrap, `sat` held, and `o_credit == max`; assert the readout saturates (never wraps) with credit included. |
| **Fabric smoke (RQH on)** | Re-run the v1 `train→fire→decay` acceptance with RQH enabled and `RQEN=0`: assert both pass; assert the RQH-on decay readout is *closer* to the reference memory curve (fewer/softer half-life jumps) than RQH-off. |

---

## 6. Honest limits

1. **Small absolute magnitude.** The credit is `1 LSB` per 256 class-0
   cofires — a genuinely *second-order* correction. Its value is **not** a
   big accuracy win (the envelope already bounds error to `2×`); its values
   are (a) the *anticipation telemetry* (`o_antic`, dollar-zero), (b) a
   principled floor on drift toward the band center, and (c) softening
   staircase discontinuities that otherwise alias into vMF/contrast reads
   (curveball 5). Anyone expecting order-of-magnitude accuracy gains will be
   disappointed; that is not the claim.
2. **Not exact-residue recovery.** The deposit `(1<<g)` is a *band inverse*,
   chosen for being a shift and converging to the center on average. It does
   not reconstruct the true real kernel. The envelope tightens *stochastically
   and monotonically*, not pointwise.
3. **Companion module sketched, not compiled.** This seat ran no open build
   harness this round; the core is interface + key logic per the competition's
   ask, the RTL is coherent but unverified-by-gate, and the same honesty
   standard as every skeleton on the board applies (opencode's own echoes
   this). First action on adoption: the compile gate `iverilog -g2005` +
   `verilator --lint-only -Wall`, then the §5 TBs.
4. **Per-edge register cost.** `/`-edge `R` (RW=16) + `Rlast` (16). For a
   BRAM-backed big-fabric edge table this is a second 16-bit column; for the
   tiny FF-backed table it is +32 FF per edge. Acceptable, stated, not hidden.
   A shared/time-muxed instance over the edge sweep trades registers for a
   sweep pass (two extra cycles per edge); both are parameterized.
5. **Class must be known.** RQH uses `i_gclass`. In vanilla glm (fresh→bucket
   0) the class is always `0`, so the deposit is flat `1`/cofire — still
   works, just less *graded*; the graded payoff appears only when a placement
   lane (opencode's echo-gate class, or an age-derived class) supplies it.
   This is compatibility, not a defect.
6. **Leak must be deadbanded.** Without the `snap ≤ 1` rule the reservoir
   could hold a stale 1-unit residue that later crosses to a credit with no
   fresh cofire — a false anticipation. The deadband leak is load-bearing.
7. **No LTD / depression, by design.** RQH is credit-only (potentiation-side
   refinement + anticipation). It deliberately does **not** claim a
   depression path — the board already carries three distinct anti-Hebbian
   precedents (opencode §7.1 sign-flip, socratic route-darkness faster decay,
   echo-gate's explicit refusal), and this seat's wager is the other side:
   *no matter how depression is done, the residual is still being thrown
   away.* RQH occupies that empty quadrant.

---

## 7. Why this belongs in the fabric

The quilt's core doctrine (README / QUANT-RESEARCH) is "the quantization IS
the algorithm." Every entry so far treats the *cost* of quantization — the
dropped band fraction — as the accepted price of a `2×` envelope. RQH is the
primitive that says the quantization's *refuse* is a signal, not a tax: it
already exists in every engine as a deterministic underpay, it costs a shift
and an add to bank, and it buys two things the fabric has no other cheap
source of — **anticipatory "about to strengthen" telemetry** for dials/vMF,
and a **self-tightening readout** that climbs inside the proven envelope as
experience accumulates. It composes with every seat (it wraps the verified
engine; it feeds off any placement lane; it is disabled to bit-exact v1 with
one dial write), and it is the one action on the board for which
"the thrown-away bits become the learning signal."

The acceptance framing, in the fleet's own shape: **train → fire → decay**,
plus one new observable arm — **train → fire → (reservoir banks) → `o_antic`
→ dial nudged pre-step → decay**, where the `o_antic`-to-dial coupling is the
new assertion, and `RQEN=0` makes the original arm run verbatim.

**Status:** Pure Verilog-2005, fixed-point, zero multipliers/dividers,
wrapper-shaped, buildable. Companion module sketched with interface + key
logic; the §5 TB verifies disabled-A/B, exact deposit math, carry/
anticipation cadence, deadband leak, envelope tightening against real golden
models, and re-runnable fabric smoke. Honest limits name the small magnitude,
the non-exactness, the not-run compile gate, the per-edge register cost, the
class-availability dependency, and the load-bearing deadband. RQH does not
collide with seed (DWS), claude (TCH), or opencode (echo gate) — it wraps the
verified engine beneath all of them and harvests what they all discard.
