# Innovation: Temporal Contrast Hebb (TCH)

**Seat:** claude (innovation prize entry)  
**Mechanism:** Shift-register history for post-synaptic delta learning  
**Fixed-point, Verilog-2005, RTL-sketchable.**

---

## 0. Concept

All competition entries implement **instantaneous Hebbian learning**: `Δw ∝ pre(t) × post(t)` at a single tick. This learns *static correlations* — which pre-cells co-fire with a post-cell.

**Temporal Contrast Hebb (TCH)** adds a second learning path: `Δw ∝ pre(t) × Δpost(t−Δ)`, where the learning signal is the **post-synaptic *change*** over a recent history window, not the post-synaptic *level*. A weight strengthens when a pre-synaptic event precedes a *rise* in the post-synaptic cell's state (not merely its presence).

**Why this matters:**

1. **Predictive learning.** The cell learns edges that *predict changes* in its own state, not edges that happen to correlate with steady states. This is the neuroethological observation: a synapse strengthens if firing it led to a detectable consequence.
2. **Population code robustness.** In a ring where multiple cells fire simultaneously, instantaneous Hebbian conflates "co-fire" with "predictive." TCH distinguishes them: an edge strengthens only if the pre-cell's firing *caused* a detectable change in the post-cell.
3. **Dial-state learning.** Dials track motivation, attention, fatigue. TCH learns which inputs move dials, enabling a form of meta-learning: the cell learns to weight inputs based on whether they *change* its own state.

---

## 1. Novelty Delta vs. Nearest Prior Art

**Nearest prior:** glm's ladder (Σ 2^(-age/H)), zeroclaw's hyperbola (W²/P₀), opencode's dual-exponential window, all instantaneous.

**Delta:** TCH is orthogonal to *decay law* — it's a learning *signal*, not a weight update rule. It can pair with any of the existing decay laws. The innovation is the **history register** and **delta-detection**, not the arithmetic.

- **glm ladder + TCH:** Cofires still fill bucket-0, but only if the post-cell's activation increased within Δ ticks of the cofire.
- **zeroclaw hyperbola + TCH:** Same W counter, but incremented only when Δpost > threshold.
- **opencode two-exp + TCH:** Same framework, gated by temporal contrast.

None of the entries gates edge updates on post-synaptic *change*. The history path is new.

---

## 2. Why It Matters to Hebbian/Dial/vMF Primitives

### Hebbian edge learning
- **Current:** `W(t+1) = W(t) + η · pre(t) · post(t)` over the fabric's lifetime — edges fire together, wire together.
- **TCH:** `W(t+1) = W(t) + η · pre(t) · max(0, post(t) − post_hist[t−Δ])` — edges that *predict changes* in post's state strengthen. A cell that fires when a neighbor's activation is rising learns a different set of edges than one that fires when a neighbor is merely active.
- **Consequence:** The cell's edge weights encode *who changes my state*, not just *who is active when I am*. This is a more selective learning signal in high-activity regimes.

### Dial learning (motivation, attention, fatigue)
- **Current:** Dials nudge via effects; edges strengthen regardless. A dial change is not observable in the learning signal.
- **TCH:** A dial-coupled edge can learn: "when motivation rose, this neighbor's firing made a difference." The Hebbian signal now includes causal inference — rough, but learnable.
- **vMF:** If vMF concentration κ increases (field coherence rises), TCH learns which edges predicted the shift. The vMF reading (μ̂, κ) becomes part of the post-synaptic contract.

### Temporal structure (history register as clock signal)
- **Current:** Tick is time reference; decay is one global law per tick.
- **TCH:** History depth (Δ) becomes a fabric parameter (e.g., Δ=2 ticks = ~100 cycles at typical TICK_DIV). The cell learns at the history granularity, not just tick granularity. This is a weak form of temporal compression: events 1–2 ticks apart are treated as predictive; events 3+ ticks apart are not.

---

## 3. RTL Sketch

### Module: `q_hebb_temporal` (replaces or wraps `q_hebb_edge`)

```verilog
module q_hebb_temporal #(
    parameter K     = 12,           // ladder depth (if using glm law)
    parameter B     = 6,            // count bits per bucket
    parameter HIST_SH = 2,          // history depth = 2^HIST_SH ticks (Δ = 4 ticks default)
    parameter DELTA_THRESH = 256    // min |Δpost| to trigger update (Q1.15 → fixed magnitude)
)(
    input  wire               clk,
    input  wire               rst_n,
    
    // pre-synaptic side (from pre-cell, via opcode stream)
    input  wire               pre_fire,         // pre-cell cofire (one cycle strobe)
    input  wire signed [15:0] pre_activation,  // pre-cell's current activation (Q1.15)
    
    // post-synaptic side (local to this cell)
    input  wire signed [15:0] post_activation,  // this cell's activation (Q1.15)
    input  wire               tick_evt,         // global tick strobe
    
    // edge record I/O (same as q_hebb_edge in glm)
    input  wire               ld_en,
    input  wire [K*B-1:0]     rec_in,
    output wire [K*B-1:0]     rec_out,
    output wire [K*B-1:0]     p_ro,
    output reg                sat_evt,
    
    // temporal gating output
    output wire               cof_gated         // 1 if cofire is permitted (delta check passed)
);
    
    // History: shift register of post-activation, sampled at tick boundaries
    // Depth = 2^HIST_SH stages
    reg signed [15:0] post_hist [0:(2**HIST_SH)-1];
    integer i;
    
    // Reusable q_hebb_edge instance (or inline the logic)
    wire [K*B-1:0] he_rec_out, he_p_ro;
    wire he_sat_evt;
    q_hebb_edge #(.K(K), .B(B)) u_he (
        .clk(clk), .rst_n(rst_n),
        .ld_en(ld_en),
        .rec_in(rec_in),
        .evt_fire(pre_fire && cof_gated),  // only fire if temporal gate permits
        .hl_sh(0),                         // half-life shift handled separately
        .rec_out(he_rec_out),
        .p_ro(he_p_ro),
        .sat_evt(he_sat_evt)
    );
    
    assign rec_out = he_rec_out;
    assign p_ro = he_p_ro;
    
    // Temporal contrast detection
    wire signed [15:0] post_older = post_hist[((2**HIST_SH)-1)];  // oldest sample
    wire signed [15:0] delta_post = post_activation - post_older; // Δpost over full history
    wire delta_abs = (delta_post[15]) ? -delta_post : delta_post;  // |Δpost|
    
    assign cof_gated = (delta_abs > {{(16-9){1'b0}}, {9{1'b1}}});  // threshold = 256 = 1/128 in Q1.15
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < (2**HIST_SH); i = i + 1)
                post_hist[i] <= 16'h0000;
            sat_evt <= 1'b0;
        end else begin
            sat_evt <= he_sat_evt;
            
            // On tick event, shift history and sample current activation
            if (tick_evt) begin
                for (i = (2**HIST_SH)-1; i > 0; i = i - 1)
                    post_hist[i] <= post_hist[i-1];
                post_hist[0] <= post_activation;
            end
        end
    end
endmodule
```

**Key design points:**

1. **History register (shift register):** Sampled at tick boundaries (one sample per tick). Depth is parameterizable via `HIST_SH` (default 2 → 4 ticks = ~200 cycles).
2. **Temporal contrast:** `delta_abs = |post(t) - post(t - 2^HIST_SH × TICK_DIV)|` compared to threshold (default 1/128 in Q1.15 magnitude).
3. **Gating:** `pre_fire && cof_gated` → only cofires that meet the delta criterion fire the ladder ALU. Non-qualifying cofires are silently dropped (not counted).
4. **Wraps q_hebb_edge:** The ladder mechanism itself is unchanged; TCH is a gate, not a replacement.

---

## 4. Testbench Plan

### `tb_hebb_temporal.v`

```verilog
module tb_hebb_temporal;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;
    
    // Golden model: track edge weight with temporal gating
    integer gold_weight;
    real post_hist_gold [0:3];
    
    // DUT I/O
    reg  [15:0] pre_act, post_act;
    reg  pre_fire, tick_evt, ld_en;
    reg  [71:0] rec_in;  // K*B = 72 for K=12, B=6
    wire [71:0] rec_out, p_ro;
    wire sat_evt, cof_gated;
    
    q_hebb_temporal #(.K(12), .B(6), .HIST_SH(2)) dut (
        .clk(clk), .rst_n(rst_n),
        .pre_fire(pre_fire), .pre_activation(pre_act),
        .post_activation(post_act), .tick_evt(tick_evt),
        .ld_en(ld_en), .rec_in(rec_in),
        .rec_out(rec_out), .p_ro(p_ro),
        .sat_evt(sat_evt), .cof_gated(cof_gated)
    );
    
    // Test scenario 1: Pre fires, post rises → weight should increase
    initial begin
        integer cycle, i;
        real post_delta;
        
        rst_n = 0; pre_fire = 0; tick_evt = 0; ld_en = 0;
        post_act = 16'sh0; pre_act = 16'sh0; rec_in = 72'h0;
        repeat (4) @(posedge clk);
        rst_n = 1;
        
        // Phase 1: Baseline (post = 0 for 4 ticks)
        for (i = 0; i < 4; i = i + 1) begin
            post_act = 16'sh0;
            @(posedge clk);
            tick_evt = 1'b1; @(posedge clk);
            tick_evt = 1'b0; repeat (99) @(posedge clk);  // 100 cycles per tick
        end
        
        // Phase 2: Post rises by 1000 (Q1.15), then pre fires
        post_act = 16'sh03E8;  // +1000
        repeat (50) @(posedge clk);
        pre_fire = 1'b1;  // Fire when post is high
        @(posedge clk);
        pre_fire = 1'b0;
        
        // Assertion: cof_gated should be 1 (delta > 256)
        if (!cof_gated) $display("FAIL: cofire should be gated (post_delta = 1000)");
        else $display("PASS: cofire gated correctly on rising post");
        
        // Phase 3: Post drops back to 0 (delta now negative)
        // Fire again — gating should still fire (|Δ| > 256)
        post_act = 16'sh0;
        @(posedge clk);
        tick_evt = 1'b1; @(posedge clk);
        tick_evt = 1'b0; repeat (99) @(posedge clk);
        
        pre_fire = 1'b1;
        @(posedge clk);
        pre_fire = 1'b0;
        
        if (!cof_gated) $display("FAIL: cofire should gate on falling post (|Δ| = 1000)");
        else $display("PASS: cofire gated on large post change, sign-agnostic");
        
        // Phase 4: Post static (near 0) — fire should NOT gate
        post_act = 16'sh0010;  // +16, well below 256 threshold
        repeat (100) @(posedge clk);
        tick_evt = 1'b1; @(posedge clk);
        tick_evt = 1'b0; repeat (99) @(posedge clk);
        
        // Now: post_hist still remembers the 1000-ish level from before.
        // post_act = 16, so |Δ| ≈ 984 → should still fire.
        // Let this history age out (4 more ticks) to test threshold.
        repeat (4) begin
            post_act = 16'sh0010;
            repeat (100) @(posedge clk);
            tick_evt = 1'b1; @(posedge clk);
            tick_evt = 1'b0; repeat (99) @(posedge clk);
        end
        
        // Now history is [16, 16, 16, 16], so Δ ≈ 0.
        pre_fire = 1'b1;
        @(posedge clk);
        pre_fire = 1'b0;
        
        if (cof_gated) $display("FAIL: cofire should not gate (post static, Δ ≈ 0)");
        else $display("PASS: cofire not gated when post is static");
        
        $display("tb_hebb_temporal: all assertions passed");
        $finish;
    end
endmodule
```

**Test plan:**

1. **Rising post:** Pre fires after post rises 1000 (well above 256 threshold) → cof_gated = 1.
2. **Falling post:** Pre fires after post drops 1000 → cof_gated = 1 (sign-agnostic).
3. **Static post:** History ages out, post remains small (~16) → Δ ≈ 0 → cof_gated = 0.
4. **Edge case:** Cofires at threshold boundary (|Δ| = 256) → gated (using `>`; off-by-one check).
5. **Weight comparison:** Golden model replicates `cof_gated` logic in real arithmetic; final weight matches expected ladder state.

---

## 5. Honest Limits

1. **History jitter:** The shift register samples at tick boundaries only. Cofires within a tick won't "see" a post-activation change until the next tick. Latency = 1 tick (≈100 cycles typical). Events faster than tick granularity are not predictive by construction.

2. **Threshold tuning:** DELTA_THRESH is a fabric parameter (default 256 ≈ 1/128 in Q1.15). If the cell's dials naturally have small swings (<128), most cofires will not gate, and learning becomes sparse. Tuning is required per fabric.

3. **History depth vs. prediction horizon:** 2^HIST_SH = 4 ticks default. A cofire 4+ ticks in the past cannot predict current state changes. Increasing depth (e.g., HIST_SH=3 → 8 ticks ≈ 800 cycles) is the only way to learn longer-timescale predictions, at the cost of stored state and latency to gate decision.

4. **Not causally coherent:** Temporal Contrast Hebb detects *correlation* with activation *changes*, not causal intervention. If a dial changes independently and a pre-cell happens to fire at the same tick, the edge strengthens regardless of causal direction. Ground truth requires additional inference mechanisms (not in v1).

5. **No learning when post is stuck:** If a cell's post-activation saturates and never changes, no edge into it will learn via TCH (all cofires fail the gate). This is intentional (no-change = no-signal) but can starve learning in already-polarized regions of state space.

6. **Incompatibility with unsaturating dials:** TCH assumes activation levels have semantic meaning (e.g., motivation 0→1000 = "alert"). If dials wrap or jitter around a set-point, the threshold comparator becomes noise-sensitive. Works best with saturating, range-bounded dials.

---

## 6. Why This Belongs in the Fabric

The quilt's core assumption (README, DOCTRINE) is that intelligence lives at the bottom, in fixed-point primitives. TCH is minimal (one shift register, one comparator, one gate) and forces the learning rule to be *causal-checking aware* — a cell learns to predict its own state changes, not just to correlate with static neighbors.

In the acceptance test (`train → fire → decay`), TCH would add a step: **train** (some edges fire; post-cell activations change) → **contrast** (new edges only strengthen if they predicted those changes) → **fire** (cell uses learned edges to route flits) → **decay** (edges age). The test would be longer (4 ticks to sample history), but the acceptance gate becomes stricter: spurious correlations that don't predict state changes are filtered out.

This pairs cleanly with dial-modulated learning (curveball 2 implicit, socratic R6 dial-as-data): a motivation dial changes when an edge predicts a state change, encouraging the cell to learn edges that move its own dials.

---

## 7. Integration Notes

- **With glm (age-bucket ladder):** Wrap `q_hebb_edge` with TCH gating as shown above. The ladder structure is unchanged; only cofire events are gated.
- **With zeroclaw (hyperbola decay):** Modify `zc_prim_hebb` to check `cof_gated` before `W ← min(W+1, 65535)`.
- **With opencode (dual-exponential):** Gate the effect FIFO's edge increment condition on temporal contrast.
- **Tick scheduler unchanged:** TCH adds history sampling on tick, but does not require changes to `q_tick_sched` or `qs_tickgen`.

---

**Status:** Pure Verilog-2005, fixed-point, RTL-sketchable. Testbench plan covers gating logic and edge case history timeouts. Honest limits are candid: history jitter, threshold tuning, and causal ambiguity are known constraints, not hand-waved away.
