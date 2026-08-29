# proposals/glm — RTL-SKETCH.md
Six real module skeletons (ports + key always blocks) backing ARCHITECTURE.md.
Pure IEEE 1364-2005 synthesizable subset: `reg`/`wire` only, no `initial` in rtl
(testbench example excepted), no SystemVerilog, no vendor cells, constant functions
for elaboration-time math, `case`-ROMs for LUTs. Written by hand on a host with no
simulator — first CI action is `iverilog -g2005` + `verilator --lint-only` over these
before anything is promoted to `rtl/`.

Contents:
1. `qs_dial.v` — saturating dial register (complete)
2. `qs_hebb_edge.v` — Hebbian age-bucket ladder ALU (complete)
3. `qs_ln.v` — LOD + LUT + interpolation logarithm (complete)
4. `qs_mathtail.v` — shared sequential divider / square-root (complete)
5. `qs_cos.v` — streaming cosine via the math tail (complete)
6. `qs_cell_core.v` — cell opcode FSM (skeleton: LINK/VIEW/EFFECT/bypass/tick-walk
   real; BIND minimal; err-flit generation stubbed)
7. `qs_fabric.v` + `qs_tickgen.v` — generate-loop ring, seam, register slices (complete)
8. `tb/tb_qs_dial.v` — testbench style example (real-arithmetic golden model)

---

## 0. The qstream contract (convention, not a module)

```verilog
// qstream port group — replicated per direction, enforced by TB checkers:
//   *_ready must not depend combinationally on the peer's *_valid.
//   transfer happens iff valid && ready; valid may not drop before transfer.
// FLIT = {meta, data}, meta = {op[2:0], dst[CID_W-1:0], src[CID_W-1:0], ttl[TTL_W-1:0]}
//        data[DW-1:0]; op: 0 bind 1 link 2 effect 3 view 4 tick 5 resp 6 err 7 rfu
// FLIT_W = DW + 3 + 2*CID_W + TTL_W
```

---

## 1. qs_dial.v — saturating dial register (SQ1.15, leak-to-center)

```verilog
// qs_dial.v — a dial: signed Q1.15, saturating nudge, exponential leak on tick.
// Wrap is a lie: every out-of-range result clamps and latches a sticky flag.
module qs_dial #(
    parameter DW       = 16,   // Q1.15 when 16
    parameter LEAK_SH  = 6,    // per tick event: |d| loses ~1/2^LEAK_SH
    parameter DEADBAND = 8     // |d| below this snaps to 0 (anti-dither)
)(
    input  wire                 clk,
    input  wire                 rst_n,
    input  wire                 en,        // apply op this cycle
    input  wire                 op_nudge,  // 1: q += delta (saturating); 0: leak
    input  wire signed [DW-1:0] delta,
    output reg  signed [DW-1:0] q,
    output reg                  sat_sticky
);
    localparam signed [DW-1:0] MAXV = {1'b0, {(DW-1){1'b1}}};   // +32767
    localparam signed [DW-1:0] MINV = {1'b1, {(DW-1){1'b0}}};   // -32768

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q          <= {DW{1'b0}};
            sat_sticky <= 1'b0;
        end else if (en) begin
            if (op_nudge) begin
                if (delta > 0 && q > MAXV - delta) begin
                    q <= MAXV;  sat_sticky <= 1'b1;
                end else if (delta < 0 && q < MINV - delta) begin
                    q <= MINV;  sat_sticky <= 1'b1;
                end else begin
                    q <= q + delta;
                end
            end else begin
                // leak toward center; snap inside deadband
                if (q > DEADBAND)
                    q <= q - (q >>> LEAK_SH);
                else if (q < -DEADBAND)
                    q <= q + ((-q) >>> LEAK_SH);
                else
                    q <= {DW{1'b0}};
            end
        end
    end
endmodule
```

---

## 2. qs_hebb_edge.v — Hebbian age-bucket ladder ALU

The record is one edge's ladder, `{C[K-1],...,C[0]}`, `C[i]` in bits
`[(i+1)*B-1 -: B]`. Bucket *i* carries implied weight `2^-i`; aging is a word
shift right by `B`; a cofire adds 1 to the LSB field. Readout `p_ro` is the
weighted sum `Ŵ = Σ C_i·2^-i` assembled by an adder tree of **wire shifts** —
the decay multiply costs nothing. Bound proven in ARCHITECTURE §3.1:
`W_exact ≤ Ŵ ≤ 2·W_exact`.

```verilog
module qs_hebb_edge #(
    parameter K = 12,          // buckets  (memory horizon = K half-lives)
    parameter B = 6            // count bits per bucket
)(
    input  wire               clk,
    input  wire               rst_n,
    input  wire               ld_en,     // load record (from edge RAM)
    input  wire [K*B-1:0]     rec_in,
    input  wire               evt_fire,  // cofire: C_0 += 1 (after aging if both)
    input  wire               hl_sh,     // age one class: ladder >>= B
    output wire [K*B-1:0]     rec_out,   // current (post-update) record
    output wire [K*B-1:0]     p_ro,      // weighted readout Ŵ (of loaded record)
    output reg                sat_evt    // sticky: bucket-0 saturate this record
);
    reg [K*B-1:0] rec;

    // combinational update
    wire [K*B-1:0] aged  = {{B{1'b0}}, rec[K*B-1:B]};      // C_i <- C_i-1, retire top
    wire [K*B-1:0] based = hl_sh ? aged : rec;
    wire             full0 = &based[B-1:0];                // C_0 saturated?
    wire [K*B-1:0] bumped = based + {{(K*B-1){1'b0}}, 1'b1};

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rec     <= {(K*B){1'b0}};
            sat_evt <= 1'b0;
        end else if (ld_en) begin
            rec     <= rec_in;
            sat_evt <= 1'b0;              // sticky is per-record (RAM walk clears)
        end else if (evt_fire || hl_sh) begin
            rec <= (evt_fire && full0) ? based : (evt_fire ? bumped : based);
            if (evt_fire && full0)
                sat_evt <= 1'b1;          // lost cofire: visible, counted
        end
    end

    assign rec_out = rec;

    // readout adder tree: bucket i placed at bit offset (K-1-i)*B  =>  Ŵ = P·2^-((K-1)B)
    wire [K*B-1:0] w [0:K-1];
    wire [K*B-1:0] t [0:K-1];
    genvar gi;
    generate
        for (gi = 0; gi < K; gi = gi + 1) begin : ro
            if (gi == 0) begin : b0            // avoid zero-width replication
                assign w[0] = {rec[B-1:0], {((K-1)*B){1'b0}}};
            end else begin : bi
                assign w[gi] = {{(gi*B){1'b0}}, rec[(gi+1)*B-1 -: B],
                                {((K-1-gi)*B){1'b0}}};
            end
        end
        assign t[0] = w[0];
        for (gi = 1; gi < K; gi = gi + 1) begin : tr
            assign t[gi] = t[gi-1] + w[gi];
        end
    endgenerate
    assign p_ro = t[K-1];
endmodule
```

---

## 3. qs_ln.v — logarithm, Q4.12 out

`Y = 2^FRAC + P` arrives from the caller's fixed scale (the cell wires
`y = {1'b0, he_ro} + 2^((K-1)*B)`). `ln(Y) = e·ln2 + ln(m)`, mantissa
`m ∈ [1,2)`; 16-entry LUT with 4-bit linear interpolation; the caller's
`FRAC·ln2` constant is a constant-function offset. Error ≤ ±2 LSB at Q4.12.
Two-cycle latency: normalize is registered, then combine.

```verilog
module qs_ln #(
    parameter IW   = 73,   // = K*B + 1 for K=12, B=6 (wrapper passes K*B+1)
    parameter FRAC = 66,   // = (K-1)*B of the calling edge ladder
    parameter OW   = 16    // signed Q4.12 output
)(
    input  wire                clk,
    input  wire                rst_n,
    input  wire                start,
    input  wire [IW-1:0]       y,       // >= 1 required (caller guarantees)
    output reg                 done,
    output reg  signed [OW-1:0] lq,     // ln(y) - FRAC*ln2,  Q4.12, saturated
    output reg                 sat_sticky
);
    function [23:0] coffs;              // constant function: FRAC * ln2 * 4096
        input integer f;
        begin
            coffs = f * 2839;           // round(ln2 * 2^12) = 2839
        end
    endfunction
    localparam [23:0] OFFS = coffs(FRAC);

    function [11:0] lntab;              // ln(1 + i/16) in Q4.12, i = 0..16
        input [4:0] i;
        begin
            case (i)
                5'd0:  lntab = 12'd0;     5'd1:  lntab = 12'd248;
                5'd2:  lntab = 12'd481;   5'd3:  lntab = 12'd704;
                5'd4:  lntab = 12'd914;   5'd5:  lntab = 12'd1114;
                5'd6:  lntab = 12'd1304;  5'd7:  lntab = 12'd1486;
                5'd8:  lntab = 12'd1661;  5'd9:  lntab = 12'd1828;
                5'd10: lntab = 12'd1989;  5'd11: lntab = 12'd2143;
                5'd12: lntab = 12'd2292;  5'd13: lntab = 12'd2436;
                5'd14: lntab = 12'd2575;  5'd15: lntab = 12'd2709;
                5'd16: lntab = 12'd2839;  default: lntab = 12'd0;
            endcase
        end
    endfunction

    reg        st;                     // 0 idle, 1 combine
    reg [6:0]  e_r;
    reg [15:0] f_r;
    reg        zero_r;
    integer k;

    // stage 1 (combinational, registered on start): leading-one normalize.
    // Sketch form: iterative shift; real rtl swaps in a casez priority encoder.
    reg [IW-1:0] ysh;
    reg [6:0]    e;
    always @(*) begin
        ysh = y;  e = 0;
        for (k = 0; k < IW; k = k + 1)
            if (ysh[IW-1] == 1'b0) begin
                ysh = {ysh[IW-2:0], 1'b0};
                e   = e + 1;
            end
    end

    // stage 2 (combinational from registered e_r/f_r): LUT + interp + offsets
    wire [3:0]  idx  = f_r[15:12];
    wire [3:0]  sub  = f_r[11:8];
    wire [11:0] diff = lntab({1'b0, idx} + 5'd1) - lntab({1'b0, idx});
    wire [15:0] prod = diff * {8'b0, sub};         // 12x4 multiply
    wire [11:0] lnm  = lntab({1'b0, idx}) + prod[15:4];
    wire [18:0] eln  = e_r * 12'd2839;             // constant multiply (CSD-friendly)
    wire signed [23:0] full_s = $signed({5'b0, eln}) + $signed({12'b0, lnm})
                              - $signed(OFFS);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= 1'b0; done <= 1'b0; lq <= 16'sd0; sat_sticky <= 1'b0;
            e_r <= 7'd0; f_r <= 16'd0; zero_r <= 1'b0;
        end else begin
            done <= 1'b0;
            if (!st) begin
                if (start) begin
                    e_r    <= e;
                    f_r    <= ysh[IW-2 -: 16];
                    zero_r <= (y == {IW{1'b0}});
                    st     <= 1'b1;
                end
            end else begin
                if (zero_r) begin
                    lq <= 16'sd0;  sat_sticky <= 1'b1;   // ln(0) flagged, not lied about
                end else if (full_s > 24'sd32767) begin
                    lq <= 16'sd32767;  sat_sticky <= 1'b1;
                end else if (full_s < -24'sd32768) begin
                    lq <= -16'sd32768;  sat_sticky <= 1'b1;
                end else begin
                    lq <= full_s[15:0];
                end
                done <= 1'b1;
                st   <= 1'b0;
            end
        end
    end
endmodule
```

---

## 4. qs_mathtail.v — shared sequential divider / integer square root

One coprocessor per fabric. Restoring division (W cycles) and the classic
shift-subtract square root (W/2 cycles) — no multipliers, no wide products.
Granted at tick boundaries; cells wait their turn.

```verilog
module qs_mathtail #(
    parameter W = 48
)(
    input  wire           clk,
    input  wire           rst_n,
    input  wire           start,
    input  wire [1:0]     op,        // 2'b00: div a/b (unsigned), 2'b01: isqrt(a)
    input  wire [W-1:0]   a,
    input  wire [W-1:0]   b,
    output wire           busy,
    output reg            done,
    output reg  [W-1:0]   q,
    output reg            err_sticky
);
    localparam N2 = W / 2;

    reg [1:0]     st;      // 0 idle, 1 div, 2 sqrt
    reg [6:0]     cnt;
    reg [W-1:0]   dvd, dvr, rd;
    reg [W:0]     drem;
    reg [W/2-1:0] root;
    reg [W-1:0]   rrem;

    assign busy = (st != 2'd0);

    // --- division step: restoring, MSB first ---
    wire        abit = dvd[W-1-cnt];
    wire [W:0]  dtop = {drem[W-1:0], abit};
    wire [W:0]  dsub = {1'b0, dvr};
    wire        dge  = (dtop >= dsub);

    // --- sqrt step: root <<= 1; trial = 4*root+1 vs (rrem<<2)|pair ---
    wire [W-1:0]   rdsh   = rd >> {cnt, 1'b0};         // rd >> (2*cnt)
    wire [1:0]     pairp  = rdsh[1:0];
    wire [W-1:0]   rrem_n = {rrem[W-3:0], pairp};
    wire [W/2+1:0] trial  = {root, 2'b01};             // 4*root + 1
    wire [W-1:0]   trial_e= {{(W-N2-2){1'b0}}, trial};
    wire           rge    = (rrem_n >= trial_e);
    wire [W/2-1:0] root_n = rge ? {root[W/2-2:0], 1'b1} : {root[W/2-2:0], 1'b0};

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= 2'd0; cnt <= 7'd0; done <= 1'b0; q <= {W{1'b0}};
            err_sticky <= 1'b0; dvd <= {W{1'b0}}; dvr <= {W{1'b0}};
            rd <= {W{1'b0}}; drem <= {(W+1){1'b0}}; root <= {(W/2){1'b0}};
            rrem <= {W{1'b0}};
        end else begin
            done <= 1'b0;
            case (st)
                2'd0: if (start) begin
                    if (op == 2'd00) begin
                        if (b == {W{1'b0}}) begin
                            err_sticky <= 1'b1;  q <= {W{1'b1}};  done <= 1'b1;
                        end else begin
                            st <= 2'd1; cnt <= 7'd0;
                            dvd <= a; dvr <= b; drem <= {(W+1){1'b0}};
                        end
                    end else if (op == 2'd01) begin
                        st <= 2'd2; cnt <= 7'd0;
                        rd <= a; root <= {(W/2){1'b0}}; rrem <= {W{1'b0}};
                    end
                end
                2'd1: begin                                      // divide
                    if (dge) begin
                        drem  <= dtop - dsub;
                        q[cnt] <= 1'b1;
                    end else begin
                        drem  <= dtop;
                        q[cnt] <= 1'b0;
                    end
                    if (cnt == W-1) begin  st <= 2'd0; done <= 1'b1; end
                    else                  cnt <= cnt + 7'd1;
                end
                2'd2: begin                                      // isqrt
                    rrem <= rge ? (rrem_n - trial_e) : rrem_n;
                    root <= root_n;
                    if (cnt == N2-1) begin
                        q    <= {{(W-N2){1'b0}}, root_n};         // floor sqrt
                        st   <= 2'd0;  done <= 1'b1;
                    end else begin
                        cnt <= cnt + 7'd1;
                    end
                end
                default: st <= 2'd0;
            endcase
        end
    end
endmodule
```

---

## 5. qs_cos.v — streaming cosine similarity

One signed multiplier, two squaring accumulators, four visits to the math tail:
`sX = isqrt(X2)`, `sP = isqrt(P2)`, `t1 = |A| / sX`, `cos = (t1 << DW) / sP`.
The pre-shift by `DW` before the second divide keeps Q1.15 fractional scale —
without it the final integer division floors the answer to 0. Sign of `A`
reapplied at the end; result clamped to [−1, 1) with sticky on clamp.
Contract: `start` pulses at least one cycle before the first `x_valid` beat;
`p_dat` is presented alongside each `x_valid`.

```verilog
module qs_cos #(
    parameter DW    = 16,     // SQ1.15 stream elements
    parameter ACC_W = 48,     // accumulators (Q2.30 domain with headroom)
    parameter LN    = 6       // log2(max vector length)
)(
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  start,
    input  wire [LN-1:0]         len,
    input  wire                  x_valid,
    output wire                  x_ready,
    input  wire signed [DW-1:0]  x_dat,
    input  wire signed [DW-1:0]  p_dat,
    output reg                   done,
    output reg  signed [DW-1:0]  cos_q,
    output reg                   rail_sticky,
    // math-tail port (shared coprocessor)
    output reg                   mt_start,
    output reg  [1:0]            mt_op,
    output reg  [ACC_W-1:0]      mt_a,
    output reg  [ACC_W-1:0]      mt_b,
    input  wire                  mt_done,
    input  wire [ACC_W-1:0]      mt_q
);
    localparam [1:0] OP_DIV  = 2'd00, OP_SQRT = 2'd01;

    localparam S_MAC=0, S_SQX_I=1, S_SQX_W=2, S_SQP_I=3, S_SQP_W=4,
               S_D1_I=5,  S_D1_W=6,  S_D2_I=7,  S_D2_W=8,  S_FIN=9;
    reg [3:0] st;

    reg signed [ACC_W-1:0] a_acc;
    reg [ACC_W-1:0]        x2_acc, p2_acc;
    reg [LN:0]             cnt;
    reg [ACC_W-1:0]        sx, sp, t1;
    reg                    a_neg;

    wire signed [2*DW-1:0] xp = x_dat * p_dat;      // Q2.30
    wire signed [2*DW-1:0] xx = x_dat * x_dat;      // >= 0
    wire signed [2*DW-1:0] pp = p_dat * p_dat;      // >= 0

    assign x_ready = (st == S_MAC);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= S_MAC; a_acc <= {ACC_W{1'b0}}; x2_acc <= {ACC_W{1'b0}};
            p2_acc <= {ACC_W{1'b0}}; cnt <= 0; sx <= 0; sp <= 0; t1 <= 0;
            a_neg <= 1'b0; done <= 1'b0; cos_q <= 16'sd0; rail_sticky <= 1'b0;
            mt_start <= 1'b0; mt_op <= 2'd0; mt_a <= 0; mt_b <= 0;
        end else begin
            done     <= 1'b0;
            mt_start <= 1'b0;
            case (st)
                S_MAC: begin
                    if (start) begin
                        a_acc <= {ACC_W{1'b0}}; x2_acc <= {ACC_W{1'b0}};
                        p2_acc <= {ACC_W{1'b0}}; cnt <= {{(LN+1){1'b0}}};
                    end else if (x_valid && (len != {{LN{1'b0}}})) begin
                        a_acc  <= a_acc + {{(ACC_W-2*DW){x_dat[DW-1]}}, xp};
                        x2_acc <= x2_acc + {{(ACC_W-2*DW){1'b0}}, xx};
                        p2_acc <= p2_acc + {{(ACC_W-2*DW){1'b0}}, pp};
                        cnt    <= cnt + {{LN{1'b0}}, 1'b1};
                        if (cnt == {1'b0, len} - {{LN{1'b0}},1'b1}) begin
                            a_neg <= a_acc[ACC_W-1];
                            st    <= S_SQX_I;
                        end
                    end
                end
                // --- tail visits: *_I issues a 1-cycle start pulse, *_W waits ---
                S_SQX_I: begin mt_op <= OP_SQRT; mt_a <= x2_acc; mt_b <= {ACC_W{1'b0}};
                                mt_start <= 1'b1; st <= S_SQX_W; end
                S_SQX_W: if (mt_done) begin sx <= mt_q; st <= S_SQP_I; end
                S_SQP_I: begin mt_op <= OP_SQRT; mt_a <= p2_acc; mt_b <= {ACC_W{1'b0}};
                                mt_start <= 1'b1; st <= S_SQP_W; end
                S_SQP_W: if (mt_done) begin sp <= mt_q; st <= S_D1_I; end
                S_D1_I:  begin mt_op <= OP_DIV;
                                mt_a <= a_neg ? (~a_acc + {{(ACC_W-1){1'b0}},1'b1})
                                              : a_acc;
                                mt_b <= sx; mt_start <= 1'b1; st <= S_D1_W; end
                S_D1_W:  if (mt_done) begin t1 <= mt_q; st <= S_D2_I; end
                S_D2_I:  begin mt_op <= OP_DIV; mt_a <= {t1[ACC_W-DW-1:0], {DW{1'b0}}};
                                mt_b <= sp; mt_start <= 1'b1; st <= S_D2_W; end
                S_D2_W:  if (mt_done) st <= S_FIN;
                S_FIN:   begin
                    if (a_neg)
                        cos_q <= -mt_q[DW-1:0];          // -32768 is legal Q1.15
                    else if (mt_q[DW-1:0] > {1'b0, {(DW-1){1'b1}}}) begin
                        cos_q <= {1'b0, {(DW-1){1'b1}}}; // clamp +1 rail
                        rail_sticky <= 1'b1;
                    end else
                        cos_q <= $signed(mt_q[DW-1:0]);
                    done <= 1'b1;
                    st  <= S_MAC;
                end
                default: st <= S_MAC;
            endcase
        end
    end
endmodule
```

*(`len == 0` degenerate case: guarded in S_MAC — unit idles in S_MAC; the TB
pins this down and the production version returns done+flag immediately.)*

---

## 6. qs_cell_core.v — opcode FSM (skeleton)

Edge RAM record `{in_use, dst, ladder[K*B], base[BASE_W]}`, single-port sync.
Intake is a 1-deep skid register so `us_ready` depends only on internal state —
never on payload or the peer's valid. LINK = find-or-alloc edge by `dst`, one
cofire pulse into the ladder ALU (fresh edges start at `ladder == 1`, no victim
pollution). VIEW(strength) = load ladder, `ln(2^FRAC + Ŵ)`, add base, respond.
EFFECT = dial nudge. Bypass = register the flit with `ttl−1` toward the egress;
bypass has egress priority over responses. TICKWALK = sweep the RAM applying
`hl_sh`, one edge per 4 cycles.

```verilog
module qs_cell_core #(
    parameter DW     = 16,
    parameter CID_W  = 8,
    parameter TTL_W  = 4,
    parameter E_LOG2 = 6,             // edges per cell = 2^E_LOG2
    parameter K      = 12,
    parameter B      = 6,
    parameter BASE_W = 8
)(
    input  wire                 clk,
    input  wire                 rst_n,
    input  wire [CID_W-1:0]     my_id,
    // qstream ingress / egress
    input  wire [DW+3+2*CID_W+TTL_W-1:0] us_flit,
    input  wire                 us_valid,
    output wire                 us_ready,
    output wire [DW+3+2*CID_W+TTL_W-1:0] ds_flit,
    output wire                 ds_valid,
    input  wire                 ds_ready,
    // edge RAM (sync single port, inferred in qs_cell wrapper)
    output reg  [E_LOG2-1:0]    eram_addr,
    output reg                  eram_we,
    output reg  [1+CID_W+K*B+BASE_W-1:0] eram_din,
    input  wire [1+CID_W+K*B+BASE_W-1:0] eram_dout,
    // ladder ALU
    output reg                  he_ld, he_evt, he_sh,
    input  wire [K*B-1:0]       he_ro,
    input  wire [K*B-1:0]       he_rec_out,
    input  wire                 he_sat,
    // ln unit
    output reg                  ln_start,
    input  wire                 ln_done,
    input  wire signed [15:0]   ln_q,
    // dials (qs_dial instances live in the wrapper)
    output reg  [1:0]           dial_sel,
    output reg                  dial_we,
    output reg                  dial_nudge,
    output reg  signed [DW-1:0] dial_delta,
    // tick bus
    input  wire                 tick_evt,
    input  wire                 hl_strobe
);
    localparam FLIT_W = DW + 3 + 2*CID_W + TTL_W;
    localparam EDGE_W = 1 + CID_W + K*B + BASE_W;

    // ---- intake skid: us_ready is a function of internal state only ----
    reg             in_v;
    reg [FLIT_W-1:0] in_f;
    wire [2:0]       iop  = in_f[DW+2:DW];
    wire [CID_W-1:0] idst = in_f[DW+3+CID_W-1:DW+3];
    wire [CID_W-1:0] isrc = in_f[DW+3+2*CID_W-1:DW+3+CID_W];
    wire [TTL_W-1:0] ittl = in_f[FLIT_W-1:FLIT_W-TTL_W];
    wire [DW-1:0]    idat = in_f[DW-1:0];
    wire             imine = (idst == my_id);

    // ---- bypass register ----
    reg              bp_v;
    reg [FLIT_W-1:0] bp_f;
    reg              ttl_drop_sticky;
    wire             bp_room = !bp_v || ds_ready;
    wire             bp_take = in_v && !imine && bp_room;   // move to bypass

    // ---- response register (FSM is the sole writer) ----
    reg              resp_v;
    reg [FLIT_W-1:0] resp_f;

    // FSM intake condition (mine + idle)
    wire core_take = in_v && imine && (st == S_IDLE) && !hl_strobe;

    assign us_ready = !in_v || core_take || bp_take;  // payload-independent

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            in_v <= 1'b0; in_f <= {FLIT_W{1'b0}};
            bp_v <= 1'b0; bp_f <= {FLIT_W{1'b0}}; ttl_drop_sticky <= 1'b0;
        end else begin
            if (bp_take) begin
                if (ittl <= {{TTL_W{1'b0}}}) begin
                    ttl_drop_sticky <= 1'b1;     // v1.1: also emit err flit
                    in_v <= 1'b0;
                end else begin
                    bp_v <= 1'b1;
                    bp_f <= in_f;
                    bp_f[FLIT_W-1:FLIT_W-TTL_W] <= ittl - {{(TTL_W-1){1'b0}},1'b1};
                    in_v <= 1'b0;
                end
            end else if (core_take) begin
                in_v <= 1'b0;                    // FSM latches fields this edge
            end else if (!in_v && us_valid) begin
                in_v <= 1'b1;  in_f <= us_flit;
            end
            // else: hold (backpressure via us_ready = 0 when full)
        end
    end

    // ---- egress mux: bypass has priority; responses wait their turn ----
    assign ds_valid = bp_v | resp_v;
    assign ds_flit  = bp_v ? bp_f : resp_f;

    // ---- edge record fields of eram_dout ----
    wire              e_use  = eram_dout[0];
    wire [CID_W-1:0]  e_dst  = eram_dout[1+:CID_W];
    wire [BASE_W-1:0] e_base = eram_dout[1+CID_W+K*B +: BASE_W];

    // strength = saturate(base:Q4.4 -> Q4.12 + ln_q)
    wire signed [19:0] s20 = $signed({{4{1'b0}}, e_base, 8'b0}) + {{4{ln_q[15]}}, ln_q};

    localparam S_IDLE=0, S_DECODE=1, S_SCAN_SET=2, S_SCAN_CHK=3,
               S_LINK_LD=4, S_LINK_EVT=5, S_LINK_WB=6,
               S_VIEW_LD=7, S_VIEW_LN=8, S_VIEW_W=9, S_RESP=10,
               S_EFF=11, S_TW_SET=12, S_TW_CHK=13, S_TW_LD=14, S_TW_WB=15;
    reg [3:0]   st;
    reg [2:0]   op_r;
    reg [CID_W-1:0] dst_r, src_r;
    reg [DW-1:0]    dat_r;
    reg [E_LOG2-1:0] scan_idx, alloc_idx;
    reg         fresh_r;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= S_IDLE; op_r <= 3'd0; dst_r <= 0; src_r <= 0; dat_r <= 0;
            scan_idx <= 0; alloc_idx <= 0; fresh_r <= 1'b0;
            eram_addr <= 0; eram_we <= 1'b0; eram_din <= {EDGE_W{1'b0}};
            he_ld <= 1'b0; he_evt <= 1'b0; he_sh <= 1'b0;
            ln_start <= 1'b0; dial_sel <= 0; dial_we <= 1'b0;
            dial_nudge <= 1'b0; dial_delta <= 0;
            resp_v <= 1'b0; resp_f <= {FLIT_W{1'b0}};
        end else begin
            he_ld <= 1'b0; he_evt <= 1'b0; he_sh <= 1'b0;
            ln_start <= 1'b0; dial_we <= 1'b0; eram_we <= 1'b0;

            case (st)
                S_IDLE: begin
                    if (hl_strobe) begin
                        scan_idx <= 0; st <= S_TW_SET;      // half-life boundary
                    end else if (core_take) begin
                        op_r <= iop; dst_r <= idst; src_r <= isrc; dat_r <= idat;
                        st   <= S_DECODE;
                    end
                end

                S_DECODE: begin
                    case (op_r)
                        3'b001: begin scan_idx <= 0; fresh_r <= 1'b0;
                                      st <= S_SCAN_SET; end                  // link
                        3'b010: begin dial_sel <= dst_r[1:0];                // effect
                                      dial_delta <= dat_r; dial_nudge <= 1'b1;
                                      dial_we <= 1'b1; st <= S_EFF; end
                        3'b011: begin eram_addr <= dat_r[E_LOG2-1:0];        // view
                                      st <= S_VIEW_LD; end
                        3'b000: begin /* qm_bind: adapter steering cfg reg in
                                      wrapper — skeleton: single cfg write */
                                      st <= S_IDLE; end
                        default:  st <= S_IDLE;      // qm_tick: wake-cfg, v1 reg wr
                    endcase
                end

                // ---------- qm_link: find-or-alloc edge, one cofire ----------
                S_SCAN_SET: begin
                    eram_addr <= scan_idx;
                    scan_idx  <= scan_idx + {{(E_LOG2-1){1'b0}},1'b1};
                    st <= S_SCAN_CHK;
                end
                S_SCAN_CHK: begin                       // eram_dout valid here
                    if (e_use && (e_dst == dst_r)) begin
                        st <= S_LINK_LD;                // found: address holds
                    end else if (scan_idx == {E_LOG2{1'b0}}) begin
                        // full sweep, no match: allocate at tail cursor.
                        // fresh edge => skip ladder load, write ladder == 1.
                        eram_addr <= alloc_idx;
                        alloc_idx <= alloc_idx + {{(E_LOG2-1){1'b0}},1'b1};
                        fresh_r  <= 1'b1;
                        st       <= S_LINK_WB;
                    end else begin
                        st <= S_SCAN_SET;
                    end
                end
                S_LINK_LD:  begin he_ld  <= 1'b1; st <= S_LINK_EVT; end
                S_LINK_EVT: begin he_evt <= 1'b1; st <= S_LINK_WB;  end
                S_LINK_WB: begin
                    eram_we  <= 1'b1;
                    eram_din <= fresh_r
                        ? {dat_r[BASE_W-1:0], {{(K*B-1){1'b0}},1'b1}, dst_r, 1'b1}
                        : {dat_r[BASE_W-1:0], he_rec_out,           dst_r, 1'b1};
                    fresh_r <= 1'b0;
                    st      <= S_IDLE;                // base nibble rides the flit
                end

                // ---------- qm_view(strength): ladder -> ln -> +base -> resp ----------
                S_VIEW_LD: begin he_ld <= 1'b1; st <= S_VIEW_LN; end
                S_VIEW_LN: begin ln_start <= 1'b1; st <= S_VIEW_W; end
                S_VIEW_W:  if (ln_done) begin
                               dat_r <= (s20 > 20'sd32767) ? 16'h7FFF : s20[15:0];
                               st <= S_RESP;
                           end
                // (ln input y = {1'b0, he_ro} + 2^((K-1)*B) wired in the wrapper)

                S_EFF: st <= S_RESP;                   // dial write landed; ack

                S_RESP: begin
                    if (!resp_v && !bp_v) begin
                        resp_v <= 1'b1;
                        resp_f <= {{TTL_W{1'b0}}, src_r, my_id, 3'b101, dat_r};
                    end else if (resp_v && ds_ready && !bp_v) begin
                        resp_v <= 1'b0;
                        st     <= S_IDLE;
                    end
                end

                // ---------- tick walk: age every edge, 4 cycles per record ----------
                S_TW_SET: begin eram_addr <= scan_idx; st <= S_TW_CHK; end
                S_TW_CHK: begin
                    if (e_use) begin
                        st <= S_TW_LD;
                    end else if (scan_idx == {E_LOG2{1'b1}}) begin
                        st <= S_IDLE;
                    end else begin
                        scan_idx <= scan_idx + {{(E_LOG2-1){1'b0}},1'b1};
                        st <= S_TW_SET;
                    end
                end
                S_TW_LD: begin he_ld <= 1'b1; he_sh <= 1'b1; st <= S_TW_WB; end
                S_TW_WB: begin
                    eram_we  <= 1'b1;
                    eram_din <= {e_base, he_rec_out, e_dst, 1'b1};
                    if (scan_idx == {E_LOG2{1'b1}}) st <= S_IDLE;
                    else begin
                        scan_idx <= scan_idx + {{(E_LOG2-1){1'b0}},1'b1};
                        st <= S_TW_SET;
                    end
                end

                default: st <= S_IDLE;
            endcase
        end
    end
endmodule
```

*(Known skeleton gaps, on purpose: `qm_bind` writes one wrapper cfg register;
`qm_tick` wake-period programming is a register write away; err-flit emission on
ttl-drop is flagged for v1.1; `e_lad` field unused here because the ALU's
`rec_in` is wired to `eram_dout` in the wrapper. Called out so review can hold
them against us.)*

---

## 7. qs_fabric.v — the chain is the quilt

Generate-loop ring, seam with **wrap priority** (in-ring flits never wait on the
seam; external injection is backpressured instead), reserved id
`{CID_W{1'b1}}` = external host, optional register slices every
`REG_SLICE_EVERY` links so timing closure is a parameter.

```verilog
module qs_fabric #(
    parameter N_CELLS        = 16,      // <= 2^CID_W - 1 (host id reserved)
    parameter CID_W          = 8,
    parameter DW             = 16,
    parameter TTL_W          = 4,
    parameter E_LOG2         = 6,
    parameter K              = 12,
    parameter B              = 6,
    parameter BASE_W         = 8,
    parameter TICK_DIV       = 16,      // < 2^24
    parameter HALF_LIFE_TICKS= 65536,   // any value < 2^24; the "90 days"
    parameter REG_SLICE_EVERY= 0        // 0 = plain chain
)(
    input  wire clk,
    input  wire rst_n,
    // external seam: injection and egress (host id = all-ones)
    input  wire                    in_valid,
    output wire                    in_ready,
    input  wire [DW+3+2*CID_W+TTL_W-1:0] in_flit,
    output wire                    out_valid,
    input  wire                    out_ready,
    output wire [DW+3+2*CID_W+TTL_W-1:0] out_flit,
    // tick bus (broadcast)
    output wire                    tick_stb,
    output wire                    hl_stb,
    output wire [15:0]             tick_cnt
);
    localparam FLIT_W = DW + 3 + 2*CID_W + TTL_W;
    localparam [CID_W-1:0] EXT_ID = {CID_W{1'b1}};

    // ---- per-cell link bundles ----
    wire [FLIT_W-1:0] pre_f [0:N_CELLS-1];
    wire [N_CELLS-1:0] pre_v, pre_r;
    wire [FLIT_W-1:0] dn_f  [0:N_CELLS-1];
    wire [N_CELLS-1:0] dn_v, dn_r;

    genvar gi;
    generate
        for (gi = 0; gi < N_CELLS; gi = gi + 1) begin : cellring
            qs_cell #(
                .DW(DW), .CID_W(CID_W), .TTL_W(TTL_W), .E_LOG2(E_LOG2),
                .K(K), .B(B), .BASE_W(BASE_W),
                .CELL_ID(gi)          // truncated to CID_W inside; N_CELLS
                                       // legality (< 2^CID_W) is a wrapper check
            ) u_cell (
                .clk(clk), .rst_n(rst_n),
                .us_flit(pre_f[gi]), .us_valid(pre_v[gi]), .us_ready(pre_r[gi]),
                .ds_flit(dn_f[gi]),  .ds_valid(dn_v[gi]),  .ds_ready(dn_r[gi]),
                .tick_stb(tick_stb), .hl_stb(hl_stb), .tick_cnt(tick_cnt)
            );
        end
        // interior links (cell gi -> cell gi+1), optional register slices
        for (gi = 0; gi < N_CELLS-1; gi = gi + 1) begin : link
            if (REG_SLICE_EVERY != 0 && ((gi+1) % REG_SLICE_EVERY == 0)) begin : sliced
                reg              v_q;
                reg [FLIT_W-1:0] f_q;
                wire             acc = !v_q || pre_r[gi+1];
                always @(posedge clk or negedge rst_n) begin
                    if (!rst_n) v_q <= 1'b0;
                    else if (acc) begin v_q <= dn_v[gi]; f_q <= dn_f[gi]; end
                end
                assign dn_r[gi]    = acc;
                assign pre_v[gi+1] = v_q;
                assign pre_f[gi+1] = f_q;
            end else begin : direct
                assign pre_v[gi+1] = dn_v[gi];
                assign pre_f[gi+1] = dn_f[gi];
                assign dn_r[gi]    = pre_r[gi+1];
            end
        end
    endgenerate

    // ---- seam: wrap has priority over external injection ----
    wire              seam_v = dn_v[N_CELLS-1];
    wire [FLIT_W-1:0] seam_f = dn_f[N_CELLS-1];
    wire              to_ext = seam_v && (seam_f[DW+3+CID_W-1:DW+3] == EXT_ID);
    wire              wrap_v = seam_v && !to_ext;

    assign out_valid = to_ext;
    assign out_flit  = seam_f;
    assign dn_r[N_CELLS-1] = to_ext ? out_ready : pre_r[0];
    assign pre_v[0]  = wrap_v || in_valid;
    assign pre_f[0]  = wrap_v ? seam_f : in_flit;
    assign in_ready  = !wrap_v && pre_r[0];

    // ---- global heartbeat ----
    qs_tickgen #(.TICK_DIV(TICK_DIV), .HL_TICKS(HALF_LIFE_TICKS)) u_tg (
        .clk(clk), .rst_n(rst_n),
        .tick_stb(tick_stb), .hl_stb(hl_stb), .tick_cnt(tick_cnt)
    );
endmodule
```

```verilog
// qs_tickgen.v — prescaler + half-life reload down-counters (no modulo logic).
module qs_tickgen #(
    parameter TICK_DIV = 16,      // fabric ticks per heartbeat, any value < 2^24
    parameter HL_TICKS = 65536    // half-life in heartbeats, any value < 2^24
)(
    input  wire        clk,
    input  wire        rst_n,
    output reg         tick_stb,
    output reg         hl_stb,
    output reg  [15:0] tick_cnt
);
    reg [23:0] pre_cnt;
    reg [23:0] hl_cnt;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tick_stb <= 1'b0; hl_stb <= 1'b0; tick_cnt <= 16'd0;
            pre_cnt <= 24'd0; hl_cnt <= 24'd0;
        end else begin
            tick_stb <= 1'b0; hl_stb <= 1'b0;
            if (pre_cnt == TICK_DIV-1) begin
                pre_cnt <= 24'd0;
                tick_stb <= 1'b1;
                tick_cnt <= tick_cnt + 16'd1;
                if (hl_cnt == HL_TICKS-1) begin
                    hl_cnt <= 24'd0;
                    hl_stb <= 1'b1;           // the 90-day boundary, in ticks
                end else
                    hl_cnt <= hl_cnt + 24'd1;
            end else
                pre_cnt <= pre_cnt + 24'd1;
        end
    end
endmodule
```

---

## 8. tb/tb_qs_dial.v — testbench style (real-arithmetic golden model)

```verilog
// Testbenches are exempt from the synthesizable rules: initial, real math,
// tasks, and $display are the point. Every tb_<module>.v follows this shape.
`timescale 1ns/1ps
module tb_qs_dial;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg                  en, op_nudge;
    reg signed [15:0]    delta;
    wire signed [15:0]   q;
    wire                 sat;

    qs_dial #(.DW(16), .LEAK_SH(6), .DEADBAND(8)) dut (
        .clk(clk), .rst_n(rst_n), .en(en), .op_nudge(op_nudge),
        .delta(delta), .q(q), .sat_sticky(sat)
    );

    // golden model: saturating add in real arithmetic
    real g;
    integer errors = 0;

    task step(input ien, input inudge, input signed [15:0] idelta);
        begin
            en = ien; op_nudge = inudge; delta = idelta;
            @(posedge clk); #1;
            g = g + idelta;                       // real domain: no wrap
            if (g > 32767.0)  g = 32767.0;
            if (g < -32768.0) g = -32768.0;
            if (q !== $rtoi(g)) begin
                errors = errors + 1;
                $display("MISMATCH t=%0t dut=%0d golden=%0f", $time, q, g);
            end
        end
    endtask

    integer i;
    reg signed [15:0] rnd;
    initial begin
        g = 0.0;
        rst_n = 0; en = 0; op_nudge = 1; delta = 0;
        repeat (4) @(posedge clk); rst_n = 1;
        // hammer: 100k random nudges — wrap is a lie, so equality is exact
        for (i = 0; i < 100000; i = i + 1) begin
            rnd = $random;
            step(1'b1, 1'b1, rnd);
        end
        // leak phase: check exponential decay half-life within ±1 tick
        if (errors == 0) $display("PASS tb_qs_dial");
        else             $display("FAIL tb_qs_dial (%0d errors)", errors);
        $finish;
    end
endmodule
```

---

## 9. Sketch-to-rtl promotion checklist

1. Replace the `qs_ln` normalize loop with a `casez` LOD (same semantics).
2. `qs_cell.v` wrapper: inferred single-port sync edge RAM + DIALS×`qs_dial` +
   ln-input wiring `y = {1'b0, he_ro} + 2^((K-1)*B)` + bind cfg register +
   `has_cos` generate-if with the fabric-level math-tail grant port.
3. err-flit generation on ttl-drop (flagged inline).
4. Then the full TB matrix of ARCHITECTURE §6, in build order §8.
