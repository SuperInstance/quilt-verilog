# INNOVATION PRIZE — opencode seat

## The Echo Gate: call–response credit for Hebbian edges

**Entry:** `proposals/innovations/opencode.md` (this file, the only artifact).
**Claim in one line:** every learning rule on this board strengthens an edge on
*reception or emission* of activity — none requires the causal loop to close.
The echo gate does: an edge's cofire counts only if the receiving cell fired
recently, graded by a leaky per-cell fire trace, so **weight grows only on
evidence of round-trip causation** — "I fired, then you fired" — at ~50 LUTs,
zero multiplies, zero timestamps, zero new opcodes.

Pure Verilog-2005, fixed-point/integer state, cell-local, deterministic. The
core module below is not a paper sketch: it compiles under `iverilog -g2005`,
passes a self-checking testbench (bit-exact integer golden + real-arithmetic
envelope), and is `verilator --lint-only -Wall` clean (§8, status).

---

## 1. The mechanism

### 1.1 What v1 does today, and why it is causal-blind

In `rtl/q_hebb_edge.v`, a delivered `qm_effect` from a linked peer issues an
unconditional cofire (cmd `001`): ladder mode bumps bucket 0, hyperbola mode
bumps `W`. The glm and zeroclaw proposals, and the v1 built from them, all
share the same event definition — the *arrival* of an effect is the co-
activation. zeroclaw says it out loud (§1.1: "the emission of an effect along
an edge is itself the cofire"); glm's `qm_link` pulses the ladder directly.

Consequence: the fabric cannot distinguish three completely different worlds —

1. I fired and my effect made you fire (my edge to you is *causal*),
2. you fired on your own and I happened to hear it (correlation, not
   causation),
3. I never fired at all and you are shouting at me (reception-only).

All three train identically. hermes §1.4 showed where reception-shaped rules
end up (seed's edges fill as a function of scale, not "fire together"); the
same blindness is latent in every count-based rule on the board, just with
events instead of magnitudes as the confound. And opencode's own §11.3
admission ("No homeostasis... dials are the operator's responsibility") names
the second structural gap: nothing bounds a runaway cell's learning.

### 1.2 The echo gate

One new per-cell register, the **fire trace** `F` (Q1.15 unsigned), plus three
rules:

```
on fire  (tick service, fire test passed):  F ← 0xFFFF
on tick  (once per tick service):           F ← F − (F ≫ KLE)      (leak, snap below FLOOR)
on effect from a linked peer:               cofire counts iff F ≥ FLOOR,
                                           landing in ladder bucket g = 15 − msb(F)
```

`KLE` (leak shift) and `FLOOR` are new dial slots (§4.4). The reading of the
rule:

- **Gating** (`F ≥ FLOOR`): an effect trains the edge only inside a causal
  window of `W_E ≈ ln(FLOOR⁻¹)/ln((1−2⁻ᴷᴸᴱ)⁻¹)` ticks after the receiver's
  own last fire. Since the only thing my fire can causally explain is a peer's
  echo arriving within the window (ring round trip at v1 scale is well under
  one tick), `F ≥ FLOOR` is the fabric's cheap test for *loop closure*.
- **Grading** (bucket `g = 15 − msb(F)`): a gated cofire is not inserted as a
  fresh memory (bucket 0) but as an *already-aged* one, bucket `g`. Because
  `F(d) ≈ (1 − 2⁻ᴷᴸᴱ)·ᵈ`, the implied weight `2⁻ᵍ` tracks the kernel value
  dyadically: an echo arriving one tick after my fire (defaults KLE=2) is
  worth ~0.75 of a fresh cofire, three ticks late ~0.42, and so on down to the
  floor. The ladder's existing decay machinery does all the work — the gate is
  a *bucket-select*, one priority encoder and one mux, reusing the `msb16`
  pattern already in `rtl/q_hebb_edge.v` for the hyperbola interval.
- **Silence earns nothing**: `F = 0` gates every train off. A cell that never
  fires can receive forever and its edges never strengthen — act integration
  is untouched (the cell still charges toward THRESH), so a driven cell will
  fire once and the gate opens; but *level without event* trains nothing.
  This is hermes §1.4's counterexample class promoted to a regression test.

### 1.3 What falls out for free

- **Plasticity budget = fire budget (structural homeostasis).** Fires are
  refractory-bounded (`refr := REFR`), and only fires open the gate. A cell
  therefore trains at most `E` gated cofires per `REFR+1` ticks, no matter how
  hard the world drives it. opencode §11.3's admitted gap closes as a *side
  effect of causality*, with no normalization circuit, no divider, no shared
  math tail — the thing socratic R3 needed a tail visit for.
- **The busiest-receiver perversity becomes semantics.** hermes §1.2's
  finding — the cell receiving the most effects learns the least under v1's
  tick deadline — reads, under the echo gate, as *correct behavior*: receiving
  without firing is not co-firing. (v1's Q2 fix keeps the tick honest; the
  gate makes the learning rule agree with it.)
- **Bootstrap is one act.** A cell earns its edges by firing once. Before
  that, it is amnesiac by construction — feature or footgun per §6.4, but
  dial-visible (`F` is viewable, §4.4).
- **GALS-safe by construction.** No timestamps, no clock comparison: the time
  reference is *local order* (my fire event vs subsequent arrivals). The
  mechanism survives the socratic R5 GALS direction and the R6 event-time
  doctrine untouched — in an event-time fabric, `F` simply leaks per local
  event instead of per tick (one line changes).
- **Law 2 untouched.** No new opcode, no flit-format change, no response
  traffic added. The gate is invisible above the cell boundary; the only
  contract surface is two dial writes.

---

## 2. Novelty audit — what the board has instead

| Board artifact | Training event | Causal? | Graded? | Where |
|---|---|---|---|---|
| v1 `q_hebb_edge` (built) | effect arrival | no | n/a (count) | `rtl/q_hebb_edge.v` cmd `001` |
| glm ladder | `qm_link` pulse | no | no (count) | glm ARCH §1.2, §3.1 |
| zeroclaw hyperbola | effect emission *is* the cofire | no | no (integer W) | zeroclaw §1.1, §2.1 |
| opencode LOOM/1 | `pre·post` product, sign flip | no (symmetric) | yes (magnitude) | opencode ARCH §7.1 |
| socratic R3 route-mem | frame sent **and** far end responds | **partially** — nearest | no (binary +1) | EXPANSION R3 |
| jester curveballs 1–14 | — | none touch causality/credit | — | CURVEBALLS.md |
| SYNTHESIS v1 + steals | count cofires | no | no | docs/SYNTHESIS.md |

The socratic entry is the only artifact on the board that requires a
*response* before strengthening anything — it is the nearest prior art and is
treated as such in §7. The delta: socratic's rule is send-side, binary
(`W ← W+1` on any response), lives in a v2 route table that v1 explicitly
deferred ("route-shaped memory would be decoration" on a single ring), and its
homeostatic variant needs the shared math tail. The echo gate is receiver-
side, graded by a leaky kernel, applies to the *v1 edge engines as built*,
needs no arithmetic beyond a shift and a priority encoder, and encodes the
kernel in the ladder's own bucket geometry. No curveball asks for it; no
honest-limits list reserves it; nothing on the board or in `rtl/` implements
any form of credit assignment.

---

## 3. Math and fixed-point policy

| Quantity | Format | Notes |
|---|---|---|
| fire trace `F` | Q1.15 unsigned, `[0, 0xFFFF]` | refill-to-max on fire; leak `F − (F≫KLE)`; snap to 0 at/below `FLOOR` or residue ≤ 1 |
| `KLE` | int 1..15 (dial 11, default 2) | per-tick multiplier `(1−2⁻ᴷᴸᴱ)`; τ ≈ ln2·2^KLE ticks |
| `FLOOR` | Q1.15 unsigned (dial 12, default 0x0080) | gate threshold; **0 = disabled = exact v1 semantics** (the A/B switch) |
| gate class `g` | int 0..15 | `g = 15 − msb(F)`; cofire implied weight `2⁻ᵍ`, engine clamps `g` to `K−1` |
| kernel | `k(d) = (1−2⁻ᴷᴸᴱ)ᵈ` | dyadic envelope: `2⁻ᵍ` ∈ `(k(d)/2, k(d)]` — the same ±1-class staircase bound the SYNTHESIS ladder already proves |
| window `W_E` | ticks | `≈ ln(0xFFFF/FLOOR)/ln((1−2⁻ᴷᴸᴱ)⁻¹)`; defaults → ~19–20 ticks |

Policy compliance: `F` is *not* integrating state in the drift sense — it is
a monotone-decaying trace with snap-to-zero (the glm deadband pattern), so
truncation bias cannot random-walk it; the cofire state itself stays integer
(zeroclaw §2.1 rule 6 preserved — the ladder/hyperbola counters are untouched
integers). Saturate-never-wrap holds trivially (`F` is bounded by refill-to-
max; bucket increment keeps its existing sticky `o_ovf`).

Hyperbola mode (`MODE=1`): integer `W` has no fractional buckets, so the gate
is binary there — train iff `F ≥ FLOOR`, no class. Stated, not hidden; the
graded kernel is a ladder-mode property.

---

## 4. RTL

### 4.1 `q_echo_trace` — the new module (complete, verified — §8)

```verilog
// q_echo_trace.v -- per-cell fire trace: the echo gate.
// One register, three rules (innovation entry, proposals/innovations/opencode.md):
//   fire : F <- max            (fire wins over a same-cycle leak)
//   tick : F <- F - (F >> KLE) (snap to 0 at/below FLOOR or residue <= 1)
//   gate : live = F >= FLOOR (or FLOOR == 0 = disabled = v1 semantics);
//          gclass = 15 - msb(F) = ladder bucket for a gated cofire.
module q_echo_trace #(
    parameter PW = 16
)(
    input  wire          clk,
    input  wire          rst_n,

    input  wire          i_fire,     // strobe: this cell fired this tick
    input  wire          i_tick,     // strobe: once per tick service (leak)
    input  wire [3:0]    i_kle,      // trace leak shift, >=1 by dial contract
    input  wire [PW-1:0] i_floor,    // gate floor; 0 = gate disabled (v1 mode)

    output wire [PW-1:0] o_f,        // trace value (viewable via dial 13)
    output wire          o_live,     // gate open: effects may train edges
    output wire [3:0]    o_gclass    // ladder bucket index for the cofire
);
    reg [PW-1:0] f;

    function [3:0] msb16;            // same pattern as q_hebb_edge's msb16
        input [PW-1:0] v;
        integer j;
        begin
            msb16 = 4'd0;
            for (j = 0; j < PW; j = j + 1)
                if (v[j] == 1'b1)
                    msb16 = j[3:0];
        end
    endfunction

    // leak with deadband snap: below-floor or residue values go to exactly
    // zero (kills the leak-floor sticky artifact; glm deadband pattern).
    wire [PW-1:0] fleak = f - (f >> i_kle);
    wire          fsnap = (fleak <= i_floor) || (fleak <= 16'd1);

    always @(posedge clk) begin
        if (!rst_n)
            f <= {PW{1'b0}};
        else if (i_fire)
            f <= {PW{1'b1}};
        else if (i_tick)
            f <= fsnap ? {PW{1'b0}} : fleak;
    end

    assign o_f      = f;
    assign o_live   = (i_floor == {PW{1'b0}}) || (f >= i_floor);
    assign o_gclass = (i_floor == {PW{1'b0}}) || (f == {PW{1'b0}})
                        ? 4'd0
                        : (4'd15 - msb16(f));

endmodule
```

Cost: 17 FF, one barrel shift, one comparator pair, one priority encoder —
~50 LUT4, zero multipliers, zero dividers, **+0 cycles on every opcode** (the
gate is combinational on the cycle `ST_EFFT` already spends on the edge hit).
Ring timing is untouched: everything is cell-local.

### 4.2 `q_hebb_edge` delta — train takes a bucket operand (sketch)

New port `input wire [3:0] i_gclass;`. Ladder branch of cmd `001`:

```verilog
3'b001: begin // gated cofire: land in bucket i_gclass (clamp K-1)
  if (!i_mode) begin
      if (i_gclass >= K[3:0]) begin
          if (c[K-1] == {B{1'b1}}) o_ovf <= 1'b1;
          else                    c[K-1] <= c[K-1] + 1'b1;
      end else begin
          if (c[i_gclass] == {B{1'b1}}) o_ovf <= 1'b1;
          else                         c[i_gclass] <= c[i_gclass] + 1'b1;
      end
  end else begin
      // hyperbola: unchanged +1 (gate is binary in mode 1, core-side)
      ...
  end
  o_done <= 1'b1;
end
```

Readout, decay, and both proven bounds are untouched — a bucket-`g` cofire is
simply an event born `g` half-lives old, which is exactly the object the
staircase bound `W_exact ≤ Ŵ ≤ 2·W_exact` already covers.

### 4.3 `q_cell_core` delta — gate issue and trace maintenance (sketch)

- Instantiate `q_echo_trace`; `i_fire` strobed entering `ST_FIRE`; `i_tick`
  strobed entering `ST_TLEAK` (exactly once per tick service, same place `act`
  leaks — so fire wins the same-cycle ordering by construction).
- `ST_EFFT` on the edge hit:

```verilog
hb_sel <= 1'b1 << eidx[EIW-1:0];
if (eg_live) begin
    hb_cmd <= 3'b001;              // gated cofire
    hb_gcl <= eg_gclass;           // new engine port
    state  <= ST_EFFR;
end else begin
    hb_cmd <= 3'b011;              // gate closed: skip train, read weight,
    state  <= ST_EFFI;             // integrate act as usual (ungated)
end
```

Integration (`ST_EFFI`) is deliberately unchanged: the gate prices *learning*,
not *activation*. A gated-off effect still charges the cell — that is what
eventually fires it and opens the gate.

### 4.4 `q_dialfile` delta — three slots (sketch)

| addr | dial | default | meaning |
|---|---|---|---|
| 11 | `KLE` | 2 | trace leak shift (τ ≈ 4·ln2 ticks) |
| 12 | `FLOOR` | 0x0080 | gate floor; **0 = disabled = bit-exact v1 behavior** |
| 13 | `FTRACE` | ro | read-only alias of `o_f` (write ignored/NAKed); the operator's window probe |

`FLOOR = 0` is the referee's switch: the existing `tb_fabric_smoke` acceptance
gate must still pass, unchanged, with the gate disabled — the A/B evidence
that the mechanism is an addition, not a rewrite.

---

## 5. Verification plan

Golden-model method per the house rules: bit-exact integer models plus real
arithmetic for envelopes; pass criterion zero mismatches.

| TB | Checks |
|---|---|
| `tb_q_echo_trace` | **written and passing now (§8)**: reset; fire refills to max, class 0; leak recurrence bit-exact for KLE ∈ {1,2,3} over 40 ticks; real envelope `f ∈ [k(d)·F₀, k(d)·F₀ + d+1]`; dyadic class bracket `2^(15−g) ≤ f < 2^(16−g)` on every live tick; snap hysteresis (closed gate ⇒ `F = 0` within 2 ticks, stable dead); fire beats same-cycle leak; disabled mode (`FLOOR=0`) live/class-0 always; dead-trace semantics |
| `tb_hebb_edge` (extend) | gclass insertion: cofire with `g` lands in bucket `g` (readout moves by exactly `2⁻ᵍ` pre-shift); clamp `g ≥ K` → bucket `K−1`; sticky ovf in the *target* bucket; decay/readout paths bit-identical to v1 for `g=0` |
| `tb_cell_core` (extend) | **the anti-seed regression**: effect storm with zero fires ⇒ `wsum` stays exactly `base` (hermes §1.4's counterexample class as CI); one fire opens the window — effects inside it train with decaying class, effects after snap train nothing, deterministically (no dither anywhere); gated-off effect still integrates `act`; `FLOOR=0` restores v1-directed behavior |
| `tb_fabric_smoke` (amended scenario, gate on) | **fire→echo→sustain→decay, end-to-end on the ring**: link A↔B both directions; host drives B past THRESH (B's pre-fire effects train *nothing* — assert `w_A→B == base`); B fires at tick k; drive A's loop; assert both edges now grow (loop closure trains both sides); remove host drive, assert the pair self-sustains ≥ N ticks on echo-trained weights; raise THRESH (fire stops ⇒ gate snaps shut), assert decay-only ticks shrink both edges below THRESH — the v1 death path, intact |

The amended acceptance is a spec change to the golden model and is flagged as
one: v1's "100 co-active effects train w past THRESH" becomes "effects train
only inside fire-opened windows" — train-to-fire becomes
**fire-to-train-to-sustain-to-decay**. With `FLOOR=0` the original scenario
and its assertions run verbatim.

---

## 6. Honest limits

1. **Attribution, not proof.** The gate tests temporal consistency (my recent
   fire, your current one), not causation. A peer that fires inside my window
   for unrelated reasons earns class-`g` credit; several simultaneous senders
   share credit for one fire. `F` is a scalar — the deep limit. Per-edge
   eligibility traces would sharpen attribution and cost `E × PW` bits; v2
   candidate, not claimed.
2. **Last-fire semantics.** Refill-to-max means the window is measured from
   the *most recent* fire; an echo of an earlier fire arriving after a newer
   one gets fresh-class credit. Accumulate-on-fire was the alternative and
   was rejected: it breaks the monotone kernel the class encoder relies on.
   Documented choice, not an oversight.
3. **No LTD direction.** A peer firing while I am silent trains nothing — it
   does not *depress* the edge. Depression remains decay's job (as in v1).
   Anti-Hebbian echo (depress on echo arriving after the window snapped) is
   speculable but unsketched.
4. **Bootstrap is mandatory.** A cell whose THRESH is unreachable never
   trains — amnesia by construction. Dial-visible via `FTRACE`; still a
   footgun for an operator who does not know it is there.
5. **Window must cover the loop.** `W_E` (defaults ~19 ticks) must exceed the
   worst-case echo round trip: fanout (≤ E flits) + ring transit (≤ N + pipe
   slices) + peer op deferral (≤ MAX_OP_CYCLES each) + one tick of fire-test
   latency. Comfortable at v1 scale (all ≪ one 4096-cycle tick); at v2
   hierarchies (bridges, GALS) `KLE`/`FLOOR` must be re-budgeted per hop —
   the knobs exist, the budget is the operator's.
6. **Hyperbola mode is binary-gated.** No graded class without fractional
   state; mode-1 cells get the rectangular window only.
7. **Path-dependence.** Training is now a function of fire times, so golden
   models must track fire events (trace-driven, socratic R9 style). All v1
   strobes are deterministic, so the port is mechanical — but the acceptance
   scenario itself changes (§5), and the old scenario only holds with the
   gate disabled.
8. **One verified module, two sketched deltas.** `q_echo_trace` is compiled,
   simulated, lint-clean. The `q_hebb_edge` and `q_cell_core` deltas are
   hand-written, hand-checked against the v1 sources, and *not* compiled —
   the same honesty standard as every skeleton on this board, restated here
   so nobody has to dig for it.

---

## 7. Novelty delta vs nearest prior art, named

- **socratic EXPANSION R3** (closest on-board): "when a frame is routed via
  entry e and the far end responds... `W_e ← W_e + 1`". Binary, send-side,
  route-table-shaped, v2-deferred by SYNTHESIS ("route-shaped memory would be
  decoration" on a single ring), homeostasis via a shared-tail divide. Delta:
  the echo gate is receiver-side, graded by a leaky dyadic kernel, drops into
  the *v1 engines as built*, needs no tail/no arbiter/no new table, and gets
  its homeostasis structurally from the refractory bound.
- **v1 `rtl/q_hebb_edge.v` cmd 001** (the thing replaced): unconditional
  cofire on arrival. Delta: arrival ≠ causation; gate + class.
- **opencode LOOM/1 §7.1** (`pre·post`, sign flip): symmetric magnitude rule,
  time-blind; the anti-Hebbian case is sign-of-product, not order-of-events.
- **glm §1.2 / zeroclaw §1.1**: "emission of the effect is itself the cofire"
  — conflate send with train; the echo gate requires the *return*.
- **Literature — pair-based STDP** (Bi & Poo 1998; Song & Abbott 2000 as the
  hardware-friendly form): nearest classical art. STDP needs per-spike (pre,
  post) timing resolution; the echo gate works at tick granularity with no
  timestamps and no per-event storage, pricing delay via a single leaky
  scalar. Closer in spirit to eligibility-trace / third-factor learning
  (Izhikevich 2007; Gerstner et al., three-factor rules) — but the "reward"
  here is endogenous (the echo itself, arriving), not a separate
  neuromodulator signal, and the credit state is one integer-safe register
  per cell, not a per-synapse analog variable.
- **What does not exist anywhere on this board or in `rtl/`**: any mechanism
  requiring loop closure before potentiation; any fire-rate bound on learning
  rate; any per-cell eligibility/credit state. The jester's 14 curveballs and
  every honest-limits list were checked — credit assignment is not asked for,
  not reserved, and not built.

One sentence for the scorecard: **the echo gate is the first rule on this
board that can tell "I made you fire" from "you fired near me" — priced at a
shift, a compare, and a priority encoder.**

---

## 8. Status (what actually ran)

The `q_echo_trace` code in §4.1 is verbatim what was verified, in a scratch
directory (not committed — this file is the entry's only artifact):

```
iverilog -g2005 -tnull q_echo_trace.v                      # compile gate: PASS
iverilog -g2005 -o tb.vvp tb_q_echo_trace.v q_echo_trace.v
vvp tb.vvp                                                  # PASS tb_q_echo_trace
verilator --lint-only -Wall --top-module q_echo_trace q_echo_trace.v   # clean
```

Testbench: bit-exact integer recurrence model, real-arithmetic envelope
(`$pow`), dyadic class-bracket checks, snap hysteresis, fire-priority,
disabled-mode, dead-trace — zero errors. The §4.2–§4.4 deltas are sketches
(limit 8); first action on adoption is the compile gate over the integrated
`rtl/`, then the extended TBs of §5.
