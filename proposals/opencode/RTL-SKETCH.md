# RTL-SKETCH — LOOM/1 (opencode lane)

Nine synthesizable Verilog-2005 (IEEE 1364-2005) module skeletons for
ARCHITECTURE.md. "Skeleton" means: complete port lists, complete reset,
complete valid/ready handshakes, and the core arithmetic/FSM logic written
out — not pseudocode. What remains for build time is called out per module
under *flesh-out points*.

Conventions (all modules):

- Clock `clk`, synchronous active-low reset `rst_n`. No `initial`, ever.
- Handshake: `valid` registered by producer, payload stable while
  `valid && !ready`, transfer on `valid && ready`.
- Flit field order in every flat bus: `op, src, dst, a0, a1, a2, dat`
  (widths 3, 4, 4, 16, 16, 16, 16 by default).
- No signed-multiply contexts where avoidable; magnitude+sign is used in
  the Hebbian datapath, explicit `$signed`/`>>>` where not avoidable
  (cosine, activation).
- `$clog2` avoided; log2 constants written as ternary chains (any
  1364-2005 tool handles both; chains are belt-and-braces).

Status: hand-checked against 1364-2005. **Not compiled** — iverilog absent
in the authoring environment; first CI action is
`iverilog -g2005 -tnull rtl/*.v` (ARCHITECTURE.md §11 limit 11).

Contents (build order):

1. `q_link_ringport` — intercell link router (deliver/transit/inject)
2. `q_flit_pipe` — registered flit slice (ring timing)
3. `q_dialfile` — dial registers
4. `q_hebbian_edge` — hebbian_edge_update engine
5. `q_isqrt16` — serial integer sqrt
6. `q_divu` — serial restoring divider
7. `q_cosine_stream` — streaming cosine estimator
8. `q_tick_sched` — tick scheduler
9. `q_cell_core` — cell core FSM (capstone)

---

## 1. q_link_ringport — intercell link

Pure-combinational ring node. One flit input from upstream (`ri`), one to
downstream (`ro`), local inject (`li`, effects from the cell), local
deliver (`ld`, into the cell ingress). Deliver consumes the ring slot and
leaves a bubble downstream; inject may use bubbles and consumed slots,
never preempts transit. Back-pressure from the cell (`ld_ready`) stops the
ring at this node until the flit is taken.

```verilog
// q_link_ringport.v -- one ring node: deliver / transit / inject.
// Pure comb. Registered slices (q_flit_pipe) inserted every ~2 nodes by
// fabric_top for timing; this module's ports stay identical either way.
module q_link_ringport #(
    parameter OPW  = 3,
    parameter AIDW = 4,
    parameter PW   = 16
)(
    // clk/rst_n unused in this comb variant; kept for port stability.
    input  wire               clk,
    input  wire               rst_n,
    input  wire [AIDW-1:0]    i_myid,

    input  wire               ri_valid,
    output wire               ri_ready,
    input  wire [OPW-1:0]     ri_op,
    input  wire [AIDW-1:0]    ri_src,
    input  wire [AIDW-1:0]    ri_dst,
    input  wire [PW-1:0]      ri_a0,
    input  wire [PW-1:0]      ri_a1,
    input  wire [PW-1:0]      ri_a2,
    input  wire [PW-1:0]      ri_dat,

    output wire               ro_valid,
    input  wire               ro_ready,
    output wire [OPW-1:0]     ro_op,
    output wire [AIDW-1:0]    ro_src,
    output wire [AIDW-1:0]    ro_dst,
    output wire [PW-1:0]      ro_a0,
    output wire [PW-1:0]      ro_a1,
    output wire [PW-1:0]      ro_a2,
    output wire [PW-1:0]      ro_dat,

    input  wire               li_valid,
    output wire               li_ready,
    input  wire [OPW-1:0]     li_op,
    input  wire [AIDW-1:0]    li_src,
    input  wire [AIDW-1:0]    li_dst,
    input  wire [PW-1:0]      li_a0,
    input  wire [PW-1:0]      li_a1,
    input  wire [PW-1:0]      li_a2,
    input  wire [PW-1:0]      li_dat,

    output wire               ld_valid,
    input  wire               ld_ready,
    output wire [OPW-1:0]     ld_op,
    output wire [AIDW-1:0]    ld_src,
    output wire [AIDW-1:0]    ld_dst,
    output wire [PW-1:0]      ld_a0,
    output wire [PW-1:0]      ld_a1,
    output wire [PW-1:0]      ld_a2,
    output wire [PW-1:0]      ld_dat
);

    wire hit      = ri_valid && (ri_dst == i_myid);
    wire consumed = hit && ld_ready;          // slot leaves the ring
    wire transit  = ri_valid && !consumed;    // still occupies the slot
    wire inject_ok = !ri_valid || consumed;   // bubble or freed slot

    assign ld_valid = hit;
    assign ld_op  = ri_op;
    assign ld_src = ri_src;
    assign ld_dst = ri_dst;
    assign ld_a0  = ri_a0;
    assign ld_a1  = ri_a1;
    assign ld_a2  = ri_a2;
    assign ld_dat = ri_dat;

    assign ro_valid = transit || (li_valid && inject_ok);
    assign ro_op  = transit ? ri_op  : li_op;
    assign ro_src = transit ? ri_src : li_src;
    assign ro_dst = transit ? ri_dst : li_dst;
    assign ro_a0  = transit ? ri_a0  : li_a0;
    assign ro_a1  = transit ? ri_a1  : li_a1;
    assign ro_a2  = transit ? ri_a2  : li_a2;
    assign ro_dat = transit ? ri_dat : li_dat;

    assign ri_ready = hit ? ld_ready : ro_ready;
    assign li_ready = inject_ok && ro_ready;

endmodule
```

Flesh-out points: none in-module; fabric_top adds `q_flit_pipe` slices.

---

## 2. q_flit_pipe — registered flit slice

1-deep register slice: cuts the `valid` path fully; `ready` path is one OR
(`ready = !vq || m_ready`), so no ready-chain hazard beyond shallow gates.

```verilog
// q_flit_pipe.v -- registered valid/ready flit slice for the ring spine.
module q_flit_pipe #(
    parameter OPW  = 3,
    parameter AIDW = 4,
    parameter PW   = 16
)(
    input  wire               clk,
    input  wire               rst_n,

    input  wire               s_valid,
    output wire               s_ready,
    input  wire [OPW-1:0]     s_op,
    input  wire [AIDW-1:0]    s_src,
    input  wire [AIDW-1:0]    s_dst,
    input  wire [PW-1:0]      s_a0,
    input  wire [PW-1:0]      s_a1,
    input  wire [PW-1:0]      s_a2,
    input  wire [PW-1:0]      s_dat,

    output wire               m_valid,
    input  wire               m_ready,
    output wire [OPW-1:0]     m_op,
    output wire [AIDW-1:0]    m_src,
    output wire [AIDW-1:0]    m_dst,
    output wire [PW-1:0]      m_a0,
    output wire [PW-1:0]      m_a1,
    output wire [PW-1:0]      m_a2,
    output wire [PW-1:0]      m_dat
);
    localparam FW = OPW + 2*AIDW + 4*PW;

    reg            vq;
    reg [FW-1:0]   dq;

    wire [FW-1:0] s_bus = {s_op, s_src, s_dst, s_a0, s_a1, s_a2, s_dat};

    assign {m_op, m_src, m_dst, m_a0, m_a1, m_a2, m_dat} = dq;
    assign m_valid = vq;
    assign s_ready = !vq || m_ready;

    always @(posedge clk) begin
        if (!rst_n) begin
            vq <= 1'b0;
            dq <= {FW{1'b0}};
        end else if (s_valid && s_ready) begin
            dq <= s_bus;
            vq <= 1'b1;
        end else if (m_ready) begin
            vq <= 1'b0;
        end
    end

endmodule
```

Flesh-out points: optional skid (2-deep) variant if a pipe ever needs full
throughput under constant back-pressure; ring use here is low-duty-cycle.

---

## 3. q_dialfile — dial registers

16 dials, defaults loaded in reset (not `initial`), one sync write port
(from `qm_bind`), one sync read port (from `qm_view`), combinational
fan-outs to the cell datapath.

```verilog
// q_dialfile.v -- dial register file. Address map in ARCHITECTURE.md 7.3.
module q_dialfile #(
    parameter DW = 16,
    parameter ND = 16,
    parameter AW = 4
)(
    input  wire                 clk,
    input  wire                 rst_n,

    input  wire                 i_wr,
    input  wire [AW-1:0]        i_addr,
    input  wire [DW-1:0]        i_wdata,
    input  wire                 i_rd,
    output reg  [DW-1:0]        o_rdata,
    output reg                  o_rstb,

    output wire [DW-1:0]        o_eta_f,
    output wire [DW-1:0]        o_eta_s,
    output wire [3:0]           o_kf,
    output wire [3:0]           o_ks,
    output wire [3:0]           o_ka,
    output wire signed [DW-1:0] o_thresh,
    output wire [DW-1:0]        o_refr,
    output wire [DW-1:0]        o_cosmin
);
    localparam [AW-1:0] D_ETA_F  = 4'd0,
                        D_ETA_S  = 4'd1,
                        D_KF     = 4'd2,
                        D_KS     = 4'd3,
                        D_KA     = 4'd4,
                        D_THRESH = 4'd5,
                        D_REFR   = 4'd6,
                        D_COSMIN = 4'd7;

    reg [DW-1:0] dial [0:ND-1];

    always @(posedge clk) begin
        if (!rst_n) begin
            dial[D_ETA_F]  <= 16'h0800;  // 0.0625
            dial[D_ETA_S]  <= 16'h0080;  // 0.0031
            dial[D_KF]     <= 16'd6;     // tau_f = 64 ticks
            dial[D_KS]     <= 16'd12;    // tau_s = 4096 ticks
            dial[D_KA]     <= 16'd5;     // act leak
            dial[D_THRESH] <= 16'h6000;  // 0.75
            dial[D_REFR]   <= 16'd4;
            dial[D_COSMIN] <= 16'h2CCD;  // 0.35
            o_rdata <= {DW{1'b0}};
            o_rstb  <= 1'b0;
        end else begin
            if (i_wr)
                dial[i_addr] <= i_wdata;
            o_rstb <= i_rd;
            if (i_rd)
                o_rdata <= dial[i_addr];  // read-old on wr/rd collision
        end
    end

    assign o_eta_f  = dial[D_ETA_F];
    assign o_eta_s  = dial[D_ETA_S];
    assign o_kf     = dial[D_KF][3:0];
    assign o_ks     = dial[D_KS][3:0];
    assign o_ka     = dial[D_KA][3:0];
    assign o_thresh = dial[D_THRESH];
    assign o_refr   = dial[D_REFR];
    assign o_cosmin = dial[D_COSMIN];

endmodule
```

Flesh-out points: none. Ships as-is.

---

## 4. q_hebbian_edge — hebbian_edge_update

One edge, Q1.15, dual-timescale decay (`w = wf + ws`), magnitude+sign
datapath (no signed multiply). 3-cycle update. Inputs are sampled at
accept; `o_done` strobes with `o_ready` reasserted.

```verilog
// q_hebbian_edge.v -- Hebbian edge update with sum-of-two-exponentials
// decay (power-law approximation, ARCHITECTURE.md 7.1 / 11.1).
//   train : wf <- clip(wf - (wf>>kf) +- (|pre|*|post|*eta_f >> 15))
//           ws <- clip(ws - (ws>>ks) +- (|pre|*|post|*eta_s >> 15))
//   decay : same, increments zero
// Rectify at 0, saturate at 0xFFFF. o_w = sat(wf+ws).
module q_hebbian_edge #(
    parameter PW = 16
)(
    input  wire                 clk,
    input  wire                 rst_n,

    input  wire                 i_upd,
    output reg                  o_ready,
    input  wire                 i_train,   // 1=train, 0=decay-only
    input  wire signed [PW-1:0] i_pre,
    input  wire signed [PW-1:0] i_post,
    input  wire [PW-1:0]        i_eta_f,
    input  wire [PW-1:0]        i_eta_s,
    input  wire [3:0]           i_kf,      // fast shift, >=1
    input  wire [3:0]           i_ks,      // slow shift, > i_kf

    output reg  [PW-1:0]        o_w,
    output reg                  o_done
);
    localparam [1:0] S_IDLE = 2'd0, S_MUL = 2'd1, S_ACC = 2'd2;

    reg [1:0]        state;
    reg              train_r;
    reg [3:0]        kf_r, ks_r;
    reg [PW-1:0]     wf, ws;
    reg [PW-1:0]     eta_f_r, eta_s_r;
    reg [2*PW-1:0]   ppm;       // |pre|*|post|, Q2.30 magnitude
    reg              pps;       // 1 -> decrement (anti-Hebbian)
    reg [3*PW-1:0]   dfm, dsm;  // increment magnitudes, pre-shift

    wire [PW-1:0] pre_m  = i_pre[PW-1]  ? (~i_pre  + 1'b1) : i_pre;
    wire [PW-1:0] post_m = i_post[PW-1] ? (~i_post + 1'b1) : i_post;

    function [PW-1:0] wstep;            // rectify-at-0, saturate-at-max
        input [2*PW+1:0] v;
        begin
            if (v[2*PW+1])
                wstep = {PW{1'b0}};
            else if (|v[2*PW:PW])
                wstep = {PW{1'b1}};
            else
                wstep = v[PW-1:0];
        end
    endfunction

    wire [PW-1:0]     wfd = wf - (wf >> kf_r);
    wire [PW-1:0]     wsd = ws - (ws >> ks_r);
    // increment = (ppm*eta) >> (PW-1): bits [3*PW-2 : PW-1]; bit 3*PW-1 is
    // unreachable (ppm*eta < 2^47) so the drop is lossless.
    wire [2*PW-1:0]   dfw = dfm[3*PW-2 -: 2*PW];
    wire [2*PW-1:0]   dsw = dsm[3*PW-2 -: 2*PW];
    wire [2*PW+1:0]   wf_try = pps ? ({1'b0, wfd} - {1'b0, dfw})
                                   : ({1'b0, wfd} + {1'b0, dfw});
    wire [2*PW+1:0]   ws_try = pps ? ({1'b0, wsd} - {1'b0, dsw})
                                   : ({1'b0, wsd} + {1'b0, dsw});
    wire [PW-1:0]     wf_n = wstep(wf_try);
    wire [PW-1:0]     ws_n = wstep(ws_try);
    wire [PW:0]       wsum_n = wf_n + ws_n;

    always @(posedge clk) begin
        if (!rst_n) begin
            state    <= S_IDLE;
            o_ready  <= 1'b1;
            o_done   <= 1'b0;
            o_w      <= {PW{1'b0}};
            wf       <= {PW{1'b0}};
            ws       <= {PW{1'b0}};
            train_r  <= 1'b0;
            kf_r     <= 4'd6;
            ks_r     <= 4'd12;
            eta_f_r  <= {PW{1'b0}};
            eta_s_r  <= {PW{1'b0}};
            ppm      <= {(2*PW){1'b0}};
            pps      <= 1'b0;
            dfm      <= {(3*PW){1'b0}};
            dsm      <= {(3*PW){1'b0}};
        end else begin
            o_done <= 1'b0;
            case (state)
              S_IDLE:
                if (i_upd && o_ready) begin
                    o_ready  <= 1'b0;
                    train_r  <= i_train;
                    kf_r     <= i_kf;
                    ks_r     <= i_ks;
                    eta_f_r  <= i_eta_f;
                    eta_s_r  <= i_eta_s;
                    ppm      <= pre_m * post_m;
                    pps      <= i_pre[PW-1] ^ i_post[PW-1];
                    state    <= S_MUL;
                end
              S_MUL: begin
                  dfm <= train_r ? (ppm * eta_f_r) : {(3*PW){1'b0}};
                  dsm <= train_r ? (ppm * eta_s_r) : {(3*PW){1'b0}};
                  state <= S_ACC;
              end
              S_ACC: begin
                  wf     <= wf_n;
                  ws     <= ws_n;
                  o_w    <= wsum_n[PW] ? {PW{1'b1}} : wsum_n[PW-1:0];
                  o_done <= 1'b1;
                  o_ready <= 1'b1;
                  state  <= S_IDLE;
              end
              default: state <= S_IDLE;
            endcase
        end
    end

endmodule
```

Flesh-out points: none in logic; TB golden model is the deliverable at M1.
Widths note: `|pre|,|post| <= 2^15` so `ppm <= 2^30`; `ppm*eta <= 2^46`
fits the 48-bit `dfm`; shifted increment `<= 2^31` fits `dfw` (32 bits).

---

## 5. q_isqrt16 — serial integer sqrt

Trial-subtract via multiply (cand² ≤ arg), bit 15 down to bit 0, 17 cycles.
Used on the Q2.30 accumulators after the `>> log2(VW)` normalization — the
integer sqrt of a Q2.30 quantity is its Q1.15 root, which is the whole
trick that keeps magnitudes in Q1.15.

```verilog
// q_isqrt16.v -- bit-serial integer square root, 32-bit in, 16-bit out.
module q_isqrt16 (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        i_start,
    input  wire [31:0] i_arg,
    output reg         o_busy,
    output reg  [15:0] o_root,
    output reg         o_done
);
    reg [3:0]  bi;
    reg [31:0] arg_r;
    reg [15:0] root;

    wire [16:0] cand = root | (17'd1 << bi);
    wire [33:0] c2   = cand * cand;
    wire        keep = (c2 <= {2'b0, arg_r});

    always @(posedge clk) begin
        if (!rst_n) begin
            o_busy <= 1'b0;
            o_done <= 1'b0;
            o_root <= 16'd0;
            bi     <= 4'd0;
            arg_r  <= 32'd0;
            root   <= 16'd0;
        end else begin
            o_done <= 1'b0;
            if (i_start && !o_busy) begin
                arg_r  <= i_arg;
                root   <= 16'd0;
                bi     <= 4'd15;
                o_busy <= 1'b1;
            end else if (o_busy) begin
                if (keep)
                    root <= cand[15:0];
                if (bi == 4'd0) begin
                    o_root <= keep ? cand[15:0] : root;
                    o_busy <= 1'b0;
                    o_done <= 1'b1;
                end else begin
                    bi <= bi - 4'd1;
                end
            end
        end
    end

endmodule
```

Flesh-out points: none. Ships as-is.

---

## 6. q_divu — serial restoring divider

`quot = num / den` (truncated), unsigned, one bit per cycle. Default
63/32 for the cosine (numerator is `|dot| << 15`, up to 56 bits used).

```verilog
// q_divu.v -- bit-serial restoring divider, unsigned, truncated quotient.
module q_divu #(
    parameter WN   = 63,   // numerator / quotient width (<= 64)
    parameter WD   = 32,   // denominator width
    parameter BIBW = 6     // >= clog2(WN)
)(
    input  wire            clk,
    input  wire            rst_n,
    input  wire            i_start,
    input  wire [WN-1:0]   i_num,
    input  wire [WD-1:0]   i_den,
    output reg             o_busy,
    output reg  [WN-1:0]   o_quot,
    output reg             o_zerr,
    output reg             o_done
);
    reg [BIBW-1:0] bi;
    reg [WN-1:0]   num;
    reg [WD-1:0]   den;
    reg [WD:0]     rem;
    reg [WN-1:0]   quot;

    wire [WD:0]   remn  = {rem[WD-1:0], num[WN-1]};
    wire          ge    = (den != {WD{1'b0}}) && (remn >= {1'b0, den});
    wire [WN-1:0] quotn = {quot[WN-2:0], ge};

    always @(posedge clk) begin
        if (!rst_n) begin
            o_busy <= 1'b0;
            o_done <= 1'b0;
            o_quot <= {WN{1'b0}};
            o_zerr <= 1'b0;
            bi     <= {BIBW{1'b0}};
            num    <= {WN{1'b0}};
            den    <= {WD{1'b0}};
            rem    <= {(WD+1){1'b0}};
            quot   <= {WN{1'b0}};
        end else begin
            o_done <= 1'b0;
            if (i_start && !o_busy) begin
                num    <= i_num;
                den    <= i_den;
                quot   <= {WN{1'b0}};
                rem    <= {(WD+1){1'b0}};
                bi     <= WN - 1;
                o_zerr <= (i_den == {WD{1'b0}});
                o_busy <= 1'b1;
            end else if (o_busy) begin
                num  <= num << 1;
                quot <= quotn;
                rem  <= ge ? (remn - {1'b0, den}) : remn;
                if (bi == {{BIBW-1{1'b0}}, 1'b0}) begin
                    o_quot  <= quotn;
                    o_busy  <= 1'b0;
                    o_done  <= 1'b1;
                end else begin
                    bi <= bi - {{BIBW-1{1'b0}}, 1'b0};
                end
            end
        end
    end

endmodule
```

Flesh-out points: none. Ships as-is.

---

## 7. q_cosine_stream — streaming cosine

VW beats of (x, y) pairs (same-beat contract: `i_beat` gates both), then
two sqrt passes and one divide. Output Q1.15 signed, clamped; `o_err` on
zero vector. Error budget and latency math in ARCHITECTURE.md 7.2.

```verilog
// q_cosine_stream.v -- streaming cosine similarity, Q1.15 in/out.
//   dot, sxq, syq accumulate in Q2.30 + guard bits (ABW).
//   mx = isqrt(sxq >> log2(VW)); my likewise (VW power of two).
//   cos = (|dot| << 15) / (mx*my), sign reapplied, clamped to Q1.15.
module q_cosine_stream #(
    parameter PW  = 16,
    parameter VW  = 8,          // beats, power of two, <= 256
    parameter ABW = 2*PW + 8,   // accumulator width (40 default)
    parameter NBW = ABW + PW    // divider numerator width (56 default)
)(
    input  wire                 clk,
    input  wire                 rst_n,

    input  wire                 i_start,
    output reg                  o_busy,

    input  wire                 i_beat,
    input  wire signed [PW-1:0] i_x,
    input  wire signed [PW-1:0] i_y,

    output reg  signed [PW-1:0] o_cos,
    output reg                  o_err,
    output reg                  o_done
);
    localparam LGW = (VW <= 1)   ? 0 :
                     (VW <= 2)   ? 1 :
                     (VW <= 4)   ? 2 :
                     (VW <= 8)   ? 3 :
                     (VW <= 16)  ? 4 :
                     (VW <= 32)  ? 5 :
                     (VW <= 64)  ? 6 : 7;

    localparam [2:0] ST_IDLE = 3'd0, ST_ACC = 3'd1, ST_SQX = 3'd2,
                     ST_SQY  = 3'd3, ST_DIV = 3'd4;

    reg [2:0]            state;
    reg [7:0]            cnt;       // beat counter, VW <= 256
    reg signed [ABW-1:0] dot, sxq, syq;
    reg [PW-1:0]         mx, my;
    reg                  dneg;
    reg                  sq_start, dv_start;

    wire signed [2*PW-1:0] xy = i_x * i_y;
    wire signed [2*PW-1:0] xx = i_x * i_x;
    wire signed [2*PW-1:0] yy = i_y * i_y;

    wire [31:0] sxn = sxq >> LGW;   // nonnegative by construction
    wire [31:0] syn = syq >> LGW;

    wire signed [ABW-1:0] dot_abs = dot[ABW-1] ? (~dot + 1'b1) : dot;
    wire [NBW-1:0]        dnum    = {dot_abs, {PW{1'b0}}};
    wire [2*PW-1:0]       dden    = mx * my;

    wire        sq_busy, sq_done, dv_busy, dv_done, dv_zerr;
    wire [15:0] sq_root;
    wire [NBW-1:0] dv_quot;

    q_isqrt16 u_sqrt (
        .clk(clk), .rst_n(rst_n),
        .i_start(sq_start),
        .i_arg  (state == ST_SQX ? sxn : syn),
        .o_busy (sq_busy), .o_root(sq_root), .o_done(sq_done)
    );

    q_divu #(.WN(NBW), .WD(2*PW), .BIBW(6)) u_div (
        .clk(clk), .rst_n(rst_n),
        .i_start(dv_start),
        .i_num  (dnum), .i_den(dden),
        .o_busy (dv_busy), .o_quot(dv_quot),
        .o_zerr (dv_zerr), .o_done(dv_done)
    );

    wire [PW-1:0] q16 = dv_quot[PW-1:0];

    always @(posedge clk) begin
        if (!rst_n) begin
            state    <= ST_IDLE;
            o_busy   <= 1'b0;
            o_done   <= 1'b0;
            o_err    <= 1'b0;
            o_cos    <= {PW{1'b0}};
            cnt      <= 8'd0;
            dot      <= {ABW{1'b0}};
            sxq      <= {ABW{1'b0}};
            syq      <= {ABW{1'b0}};
            mx       <= {PW{1'b0}};
            my       <= {PW{1'b0}};
            dneg     <= 1'b0;
            sq_start <= 1'b0;
            dv_start <= 1'b0;
        end else begin
            o_done   <= 1'b0;
            sq_start <= 1'b0;
            dv_start <= 1'b0;

            case (state)
              ST_IDLE:
                if (i_start) begin
                    dot    <= {ABW{1'b0}};
                    sxq    <= {ABW{1'b0}};
                    syq    <= {ABW{1'b0}};
                    cnt    <= 8'd0;
                    o_busy <= 1'b1;
                    state  <= ST_ACC;
                end
              ST_ACC:
                if (i_beat) begin
                    dot <= dot + xy;
                    sxq <= sxq + xx;
                    syq <= syq + yy;
                    if (cnt == VW - 1) begin
                        dneg     <= ((dot + xy) < 0);
                        sq_start <= 1'b1;
                        state    <= ST_SQX;
                    end else begin
                        cnt <= cnt + 8'd1;
                    end
                end
              ST_SQX:
                if (sq_done) begin
                    mx       <= sq_root;
                    sq_start <= 1'b1;      // restart on y
                    state    <= ST_SQY;
                end
              ST_SQY:
                if (sq_done) begin
                    my       <= sq_root;
                    dv_start <= 1'b1;
                    state    <= ST_DIV;
                end
              ST_DIV:
                if (dv_done) begin
                    o_err  <= dv_zerr;
                    if (dv_zerr)
                        o_cos <= {PW{1'b0}};
                    else if (dneg)
                        o_cos <= (q16 >= 16'h8000) ? 16'h8000
                                                  : (~q16 + 1'b1);
                    else
                        o_cos <= (q16 >= 16'h8000) ? 16'h7FFF : q16;
                    o_done <= 1'b1;
                    o_busy <= 1'b0;
                    state  <= ST_IDLE;
                end
              default: state <= ST_IDLE;
            endcase
        end
    end

endmodule
```

Flesh-out points: none in-module. (A shared-isqrt variant saving 17 cycles
is a build-time option; not needed for correctness.)

---

## 8. q_tick_sched — tick scheduler

```verilog
// q_tick_sched.v -- tick strobe + 4-phase cadence, ARCHITECTURE.md 7.4.
module q_tick_sched #(
    parameter TPW = 12,     // log2(cycles per tick)
    parameter PHW = 2       // phase bits (4 phases)
)(
    input  wire            clk,
    input  wire            rst_n,
    output reg             o_tick,    // 1-cycle strobe at wrap
    output wire [PHW-1:0]  o_phase,   // cnt[TPW-1 -: PHW]
    output wire [TPW-1:0]  o_count
);
    reg [TPW-1:0] cnt;

    assign o_count = cnt;
    assign o_phase = cnt[TPW-1 -: PHW];

    always @(posedge clk) begin
        if (!rst_n) begin
            cnt    <= {TPW{1'b0}};
            o_tick <= 1'b0;
        end else begin
            cnt    <= cnt + {{TPW-1{1'b0}}, 1'b1};
            o_tick <= (cnt == {TPW{1'b0}});
        end
    end

endmodule
```

Flesh-out points: none. Ships as-is.

---

## 9. q_cell_core — cell core FSM

The capstone: the only interpreter of the five quilt opcodes. Latches each
ingress flit, runs the engines, holds `EDGES_N` edges (peer id, Q1.15
weight, valid), integrates activations, fires on threshold with refractory,
and answers bind/link/view with ack/nak flits. Edge table is a plain
reg-array (LUTRAM-shaped); synchronous-read template swap for BRAM is the
only planned change beyond EDGES_N > 16.

```verilog
// q_cell_core.v -- one quilt cell. Opcode semantics in ARCHITECTURE 4/6/7.
module q_cell_core #(
    parameter OPW     = 3,
    parameter AIDW    = 4,
    parameter PW      = 16,
    parameter EDGES_N = 8,
    parameter EIW     = 3
)(
    input  wire                 clk,
    input  wire                 rst_n,

    // ingress flit (ring deliver, priority-muxed with local adapter)
    input  wire [OPW-1:0]       ci_op,
    input  wire                 ci_valid,
    output reg                  ci_ready,
    input  wire [AIDW-1:0]      ci_src,
    input  wire [PW-1:0]        ci_a0,
    input  wire [PW-1:0]        ci_a1,
    input  wire [PW-1:0]        ci_a2,
    input  wire [PW-1:0]        ci_dat,

    // local egress (ack/nak/view data)
    output reg  [OPW-1:0]       lo_op,
    output reg                  lo_valid,
    input  wire                 lo_ready,
    output reg  [AIDW-1:0]      lo_dst,
    output reg  [AIDW-1:0]      lo_src,
    output reg  [PW-1:0]        lo_a0,
    output reg  [PW-1:0]        lo_a1,
    output reg  [PW-1:0]        lo_a2,
    output reg  [PW-1:0]        lo_dat,

    // fabric egress (qm_effect fanout)
    output reg  [OPW-1:0]       lx_op,
    output reg                  lx_valid,
    input  wire                 lx_ready,
    output reg  [AIDW-1:0]      lx_dst,
    output reg  [AIDW-1:0]      lx_src,
    output reg  [PW-1:0]        lx_a0,
    output reg  [PW-1:0]        lx_a1,
    output reg  [PW-1:0]        lx_a2,
    output reg  [PW-1:0]        lx_dat,

    // hebbian engine
    output reg                  hb_upd,
    input  wire                 hb_ready,
    output reg                  hb_train,
    output reg  signed [PW-1:0] hb_pre,
    output reg  signed [PW-1:0] hb_post,
    output reg  [PW-1:0]        hb_eta_f,
    output reg  [PW-1:0]        hb_eta_s,
    output reg  [3:0]           hb_kf,
    output reg  [3:0]           hb_ks,
    input  wire [PW-1:0]        hb_w,
    input  wire                 hb_done,

    // cosine engine
    output reg                  cs_start,
    input  wire                 cs_busy,
    input  wire                 cs_done,
    input  wire signed [PW-1:0] cs_cos,

    // dial file ports
    output reg                  df_wr,
    output reg  [3:0]           df_addr,
    output reg  [PW-1:0]        df_wdata,
    output reg                  df_rd,
    input  wire [PW-1:0]        df_rdata,
    input  wire                 df_rstb,

    // dial fan-in (combinational views from q_dialfile)
    input  wire [PW-1:0]        d_eta_f,
    input  wire [PW-1:0]        d_eta_s,
    input  wire [3:0]           d_kf,
    input  wire [3:0]           d_ks,
    input  wire [3:0]           d_ka,
    input  wire signed [PW-1:0] d_thresh,
    input  wire [PW-1:0]        d_refr,

    // scheduler
    input  wire                 s_tick,
    input  wire [1:0]           s_phase,

    // status
    output reg                  bound,
    output reg  [AIDW-1:0]      cell_id,
    output reg  signed [PW-1:0] act
);
    localparam [OPW-1:0] OP_BIND = 3'd0, OP_LINK = 3'd1, OP_EFF  = 3'd2,
                         OP_VIEW = 3'd3, OP_TICK = 3'd4, OP_ACK  = 3'd5,
                         OP_NAK  = 3'd6;

    localparam [4:0] ST_RST = 5'd0,  ST_UNB   = 5'd1,  ST_IDLE  = 5'd2,
                     ST_BIND = 5'd3,  ST_LINK  = 5'd4,  ST_EFF   = 5'd5,
                     ST_EFFW = 5'd6,  ST_EFFI  = 5'd7,  ST_VIEW  = 5'd8,
                     ST_VACC = 5'd9,  ST_VRD   = 5'd10, ST_VCS   = 5'd11,
                     ST_RESP = 5'd12, ST_TICK  = 5'd13, ST_TDEC  = 5'd14,
                     ST_TDW  = 5'd15, ST_TLEAK = 5'd16, ST_FIRE  = 5'd17,
                     ST_FIREW = 5'd18;

    reg [4:0]        state;
    reg [OPW-1:0]    lr_op;
    reg [AIDW-1:0]   lr_src;
    reg [PW-1:0]     lr_a0, lr_a1, lr_a2, lr_dat;
    reg [PW-1:0]     viewdat;
    reg              resp_nak;
    reg [EIW:0]      eidx;      // one bit wider than slot index so the
                                 // sweep can hold the EDGES_N sentinel
    reg [EIW-1:0]    eslot;
    reg [PW:0]       wacc;
    reg [PW-1:0]     refr;
    reg signed [PW-1:0] afire;
    reg              tick_go;

    reg [AIDW-1:0] etab [0:EDGES_N-1];
    reg [PW-1:0]   wtab [0:EDGES_N-1];
    reg            ev   [0:EDGES_N-1];

    function [PW-1:0] sclip16;           // saturate to Q1.15 full scale
        input signed [31:0] v;
        begin
            if (v > 32'sd32767)
                sclip16 = 16'h7FFF;
            else if (v < -32'sd32768)
                sclip16 = 16'h8000;
            else
                sclip16 = v[15:0];
        end
    endfunction

    always @(posedge clk) begin
        if (!rst_n) begin
            state    <= ST_RST;
            ci_ready <= 1'b0;
            lo_valid <= 1'b0;
            lo_op    <= {OPW{1'b0}};
            lo_dst   <= {AIDW{1'b0}};
            lo_src   <= {AIDW{1'b0}};
            lo_a0    <= {PW{1'b0}};
            lo_a1    <= {PW{1'b0}};
            lo_a2    <= {PW{1'b0}};
            lo_dat   <= {PW{1'b0}};
            lx_valid <= 1'b0;
            lx_op    <= {OPW{1'b0}};
            lx_dst   <= {AIDW{1'b0}};
            lx_src   <= {AIDW{1'b0}};
            lx_a0    <= {PW{1'b0}};
            lx_a1    <= {PW{1'b0}};
            lx_a2    <= {PW{1'b0}};
            lx_dat   <= {PW{1'b0}};
            hb_upd   <= 1'b0;
            hb_train <= 1'b0;
            hb_pre   <= {PW{1'b0}};
            hb_post  <= {PW{1'b0}};
            hb_eta_f <= {PW{1'b0}};
            hb_eta_s <= {PW{1'b0}};
            hb_kf    <= 4'd0;
            hb_ks    <= 4'd0;
            cs_start <= 1'b0;
            df_wr    <= 1'b0;
            df_addr  <= 4'd0;
            df_wdata <= {PW{1'b0}};
            df_rd    <= 1'b0;
            bound    <= 1'b0;
            cell_id  <= {AIDW{1'b0}};
            act      <= {PW{1'b0}};
            refr     <= {PW{1'b0}};
            tick_go  <= 1'b0;
            eidx     <= {(EIW+1){1'b0}};
            eslot    <= {EIW{1'b0}};
            wacc     <= {(PW+1){1'b0}};
            viewdat  <= {PW{1'b0}};
            resp_nak <= 1'b0;
            afire    <= {PW{1'b0}};
            lr_op    <= {OPW{1'b0}};
            lr_src   <= {AIDW{1'b0}};
            lr_a0    <= {PW{1'b0}};
            lr_a1    <= {PW{1'b0}};
            lr_a2    <= {PW{1'b0}};
            lr_dat   <= {PW{1'b0}};
        end else begin
            // single-cycle strobes default low each cycle
            df_wr  <= 1'b0;
            df_rd  <= 1'b0;
            hb_upd <= 1'b0;
            cs_start <= 1'b0;
            lo_valid <= 1'b0;
            lx_valid <= 1'b0;

            case (state)
              // ------------------------------------------------ reset ---
              ST_RST: begin
                  state <= ST_UNB;
              end

              // ------------------------------ wait for first bind ---
              ST_UNB: begin
                  ci_ready <= 1'b1;
                  if (ci_valid && ci_ready) begin
                      lr_src <= ci_src;
                      if (ci_op == OP_BIND) begin
                          cell_id  <= ci_a0[AIDW-1:0];
                          bound    <= 1'b1;
                          resp_nak <= 1'b0;
                          viewdat  <= {PW{1'b0}};
                      end else begin
                          resp_nak <= 1'b1;   // not bound: nak anything
                          viewdat  <= {PW{1'b0}};
                      end
                      ci_ready <= 1'b0;
                      state    <= ST_RESP;
                  end
              end

              // ----------------------------------------- dispatch ---
              ST_IDLE: begin
                  ci_ready <= 1'b1;
                  if (s_tick)
                      tick_go <= 1'b1;
                  if (tick_go && !ci_valid) begin
                      tick_go  <= 1'b0;
                      ci_ready <= 1'b0;
                      state    <= ST_TICK;
                  end else if (ci_valid && ci_ready) begin
                      lr_op  <= ci_op;
                      lr_src <= ci_src;
                      lr_a0  <= ci_a0;
                      lr_a1  <= ci_a1;
                      lr_a2  <= ci_a2;
                      lr_dat <= ci_dat;
                      ci_ready <= 1'b0;
                      case (ci_op)
                        OP_BIND: state <= ST_BIND;
                        OP_LINK: state <= ST_LINK;
                        OP_EFF:  state <= ST_EFF;
                        OP_VIEW: state <= ST_VIEW;
                        OP_ACK, OP_NAK, OP_TICK:
                                 state <= ST_IDLE;  // consumed, no action
                        default: begin
                            resp_nak <= 1'b1;
                            viewdat  <= {PW{1'b0}};
                            state    <= ST_RESP;
                        end
                      endcase
                  end
              end

              // bind = dial write (first bind handled in ST_UNB) -------
              ST_BIND: begin
                  df_wr    <= 1'b1;
                  df_addr  <= lr_a0[3:0];
                  df_wdata <= lr_a1;
                  resp_nak <= 1'b0;
                  viewdat  <= {PW{1'b0}};
                  state    <= ST_RESP;
              end

              // link = write edge slot {peer=src, weight=a1} ----------
              ST_LINK: begin
                  etab[lr_a0[EIW-1:0]] <= lr_src;
                  wtab[lr_a0[EIW-1:0]] <= lr_a1;
                  ev  [lr_a0[EIW-1:0]] <= 1'b1;
                  resp_nak <= 1'b0;
                  viewdat  <= {PW{1'b0}};
                  state    <= ST_RESP;
              end

              // effect: scan edge table for src ------------------------
              ST_EFF: begin
                  eidx  <= {(EIW+1){1'b0}};
                  state <= ST_EFFW;
              end
              ST_EFFW: begin
                  if (eidx == EDGES_N) begin
                      // unknown source: dropped (link before effect)
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end else if (ev[eidx] && (etab[eidx] == lr_src)) begin
                      eslot    <= eidx;
                      hb_upd   <= 1'b1;
                      hb_train <= 1'b1;
                      hb_pre   <= lr_dat;
                      hb_post  <= act;
                      hb_eta_f <= d_eta_f;
                      hb_eta_s <= d_eta_s;
                      hb_kf    <= d_kf;
                      hb_ks    <= d_ks;
                      state    <= ST_EFFI;
                  end else begin
                      eidx <= eidx + 1'b1;
                  end
              end
              ST_EFFI: begin
                  if (hb_done) begin
                      // train-then-integrate with the post-update weight
                      wtab[eslot] <= hb_w;
                      act <= sclip16(act +
                              (($signed({1'b0, hb_w}) * $signed(lr_dat))
                               >>> 15));
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end
              end

              // view: 0=act 1=wsum 2=dial(a1=addr) 3=cosine ------------
              ST_VIEW: begin
                  case (lr_a0[1:0])
                    2'd0: begin
                        viewdat <= act;
                        resp_nak <= 1'b0;
                        state   <= ST_RESP;
                    end
                    2'd1: begin
                        wacc  <= {(PW+1){1'b0}};
                        eidx  <= {(EIW+1){1'b0}};
                        state <= ST_VACC;
                    end
                    2'd2: begin
                        df_rd   <= 1'b1;
                        df_addr <= lr_a1[3:0];
                        state   <= ST_VRD;
                    end
                    default: begin
                        cs_start <= 1'b1;
                        state    <= ST_VCS;
                    end
                  endcase
              end
              ST_VACC: begin
                  if (eidx == EDGES_N) begin
                      viewdat  <= wacc[PW] ? {PW{1'b1}} : wacc[PW-1:0];
                      resp_nak <= 1'b0;
                      state    <= ST_RESP;
                  end else begin
                      wacc <= wacc + {1'b0, wtab[eidx]};
                      eidx <= eidx + 1'b1;
                  end
              end
              ST_VRD: begin
                  if (df_rstb) begin
                      viewdat  <= df_rdata;
                      resp_nak <= 1'b0;
                      state    <= ST_RESP;
                  end
              end
              ST_VCS: begin
                  if (cs_done) begin
                      viewdat  <= cs_cos;
                      resp_nak <= 1'b0;
                      state    <= ST_RESP;
                  end
              end

              // one response flit to the requester ---------------------
              ST_RESP: begin
                  lo_op    <= resp_nak ? OP_NAK : OP_ACK;
                  lo_valid <= 1'b1;
                  lo_dst   <= lr_src;
                  lo_src   <= cell_id;
                  lo_dat   <= viewdat;
                  lo_a0    <= {PW{1'b0}};
                  lo_a1    <= {PW{1'b0}};
                  lo_a2    <= {PW{1'b0}};
                  if (lo_valid && lo_ready) begin
                      lo_valid <= 1'b0;
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end
              end

              // tick: decay sweep over edges ---------------------------
              ST_TICK: begin
                  eidx  <= {(EIW+1){1'b0}};
                  state <= ST_TDEC;
              end
              ST_TDEC: begin
                  if (eidx == EDGES_N) begin
                      state <= ST_TLEAK;
                  end else if (ev[eidx]) begin
                      hb_upd   <= 1'b1;
                      hb_train <= 1'b0;
                      hb_pre   <= {PW{1'b0}};
                      hb_post  <= {PW{1'b0}};
                      hb_eta_f <= {PW{1'b0}};
                      hb_eta_s <= {PW{1'b0}};
                      hb_kf    <= d_kf;
                      hb_ks    <= d_ks;
                      state    <= ST_TDW;
                  end else begin
                      eidx <= eidx + 1'b1;
                  end
              end
              ST_TDW: begin
                  if (hb_done) begin
                      wtab[eidx] <= hb_w;
                      eidx       <= eidx + 1'b1;
                      state      <= ST_TDEC;
                  end
              end

              // leak activation, then fire test -------------------------
              ST_TLEAK: begin
                  act <= sclip16(act - (act >>> d_ka));
                  if ((act >= d_thresh) && (refr == {PW{1'b0}})) begin
                      afire <= act;
                      eidx  <= {(EIW+1){1'b0}};
                      state <= ST_FIRE;
                  end else begin
                      if (refr != {PW{1'b0}})
                          refr <= refr - 1'b1;
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end
              end

              // fan out effects to valid edges --------------------------
              ST_FIRE: begin
                  if (eidx == EDGES_N) begin
                      act      <= {PW{1'b0}};
                      refr     <= d_refr;
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end else if (ev[eidx]) begin
                      lx_op    <= OP_EFF;
                      lx_valid <= 1'b1;
                      lx_dst   <= etab[eidx];
                      lx_src   <= cell_id;
                      lx_dat   <= afire;
                      lx_a0    <= {PW{1'b0}};
                      lx_a1    <= {PW{1'b0}};
                      lx_a2    <= {PW{1'b0}};
                      if (lx_valid && lx_ready) begin
                          lx_valid <= 1'b0;
                          eidx     <= eidx + 1'b1;
                      end
                  end else begin
                      eidx <= eidx + 1'b1;
                  end
              end

              default: state <= ST_IDLE;
            endcase
        end
    end

endmodule
```

Flesh-out points (build time, all additive):

- wire-up inside `quilt_cell`: core ⇄ engines ⇄ dialfile; ring `ld→ci`
  priority mux with the local adapter (deliver wins; both hold payload
  until ready — a 2-way OR-mux with per-side ready is ~15 lines).
- responses ride the ring: `lo` merges into the same ring inject as `lx`
  (dst already set to `lr_src`), so ack/nak/view data reach remote
  requesters as ordinary flits — Law 2 applies to responses too. A second
  inject slot on `q_link_ringport` (or a 2-flit `q_inject_mux`) is the
  only link-side addition.
- EDGES_N > 16: swap `wtab/etab` for synchronous-read templates
  (read-data-reg states `ST_EFFW`/`ST_TDW` gain one wait cycle each —
  budgeted in ARCHITECTURE 6).
- `s_phase` input is unused in this skeleton (phases are advisory,
  ARCHITECTURE 11.9); the first build either wires a watchdog counter on
  it or removes the port. Kept now so fabric_top wiring is final.

---

## Not in this sketch (deliberately)

- `quilt_fabric_top`, `quilt_cell` — structural glue only (M4/M5).
- `q_adpt_byteframer`, `q_adpt_afifo` — adapters, spec'd in
  ARCHITECTURE 4.3, built at M6.
- `q_hebbian_log` — log-domain power-law decay variant (docs-only idea,
  ARCHITECTURE 11.1).
- `q_logtab` — log/exp tables for vMF κ (docs-only, 11.13).
