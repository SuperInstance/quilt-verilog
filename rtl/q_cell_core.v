// q_cell_core.v -- one quilt cell: the only interpreter of the five quilt
// opcodes (quilt-verilog v1, glm chassis). Cooperative run-to-completion FSM.
//
// Q1 (liveness, docs/SYNTHESIS.md): every op is bounded (MAX_OP_CYCLES);
// ci_ready reasserts after each op, so views/binds are never starved by
// effect traffic. No shared math tail exists in v1 (view(3) NAKs), so the
// grant-starvation surface is empty by construction.
//
// Q2 (non-deferrable time): s_tick latches tick_pend; ST_IDLE services
// tick_pend BEFORE accepting new ingress (ci_ready suppressed while
// pending). A tick is deferred by at most the in-flight op, never by
// traffic. This is curveball 8's pre-emption at the op boundary.
//
// Opcode semantics:
//   bind  : first bind sets cell_id (from a0) and binds the cell; later
//           binds write dial a0[3:0] <= a1. Ack.
//   link  : edge slot a0[EIW-1:0] := {peer=src, base weight=a1}. Ack.
//   effect: if src matches a valid edge slot, train that edge (cofire),
//           read the weight back, integrate act += sat((w*dat)>>>15).
//           Unknown src is dropped silently (link before effect).
//   view  : a0[1:0] 0=act 1=wsum(edges) 2=dial[a1[3:0]] 3=NAK (no cos in v1).
//           Response is an ack flit to src carrying the value in dat.
//   tick  : decay sweep over all valid edges, act leak (>>>ka), fire test
//           (act >= thresh && refr==0): fanout effects (dat=act) to all
//           valid edge peers, act:=0, refr:=d_refr.
module q_cell_core #(
    parameter OPW     = 3,
    parameter AIDW    = 4,
    parameter PW      = 16,
    parameter EDGES_N = 4,
    parameter EIW     = 2
)(
    input  wire                 clk,
    input  wire                 rst_n,

    // ingress flit (ring deliver)
    input  wire [OPW-1:0]       ci_op,
    input  wire                 ci_valid,
    output reg                  ci_ready,
    input  wire [AIDW-1:0]      ci_src,
    input  wire [PW-1:0]        ci_a0,
    input  wire [PW-1:0]        ci_a1,
    input  wire [PW-1:0]        ci_a2,
    input  wire [PW-1:0]        ci_dat,

    // local egress: ack/nak/view responses
    output reg  [OPW-1:0]       lo_op,
    output reg                  lo_valid,
    input  wire                 lo_ready,
    output reg  [AIDW-1:0]      lo_dst,
    output reg  [AIDW-1:0]      lo_src,
    output reg  [PW-1:0]        lo_a0,
    output reg  [PW-1:0]        lo_a1,
    output reg  [PW-1:0]        lo_a2,
    output reg  [PW-1:0]        lo_dat,

    // fabric egress: qm_effect fanout on fire
    output reg  [OPW-1:0]       lx_op,
    output reg                  lx_valid,
    input  wire                 lx_ready,
    output reg  [AIDW-1:0]      lx_dst,
    output reg  [AIDW-1:0]      lx_src,
    output reg  [PW-1:0]        lx_a0,
    output reg  [PW-1:0]        lx_a1,
    output reg  [PW-1:0]        lx_a2,
    output reg  [PW-1:0]        lx_dat,

    // hebbian edge engine array (one q_hebb_edge per slot, in q_cell)
    output reg  [2:0]           hb_cmd,
    output reg  [EDGES_N-1:0]   hb_sel,
    output reg  [PW-1:0]        hb_base,
    input  wire [PW-1:0]        hb_w,
    input  wire                 hb_done,

    // dial file ports
    output reg                  df_wr,
    output reg  [3:0]           df_addr,
    output reg  [PW-1:0]        df_wdata,
    output reg                  df_rd,
    input  wire [PW-1:0]        df_rdata,
    input  wire                 df_rstb,

    // dial fan-in (combinational views from q_dialfile)
    input  wire [3:0]           d_ka,
    input  wire signed [PW-1:0] d_thresh,
    input  wire [PW-1:0]        d_refr,

    // scheduler
    input  wire                 s_tick,

    // status
    output reg                  bound,
    output reg  [AIDW-1:0]      cell_id,
    output reg  signed [PW-1:0] act
);
    localparam [OPW-1:0] OP_BIND = 3'd0, OP_LINK = 3'd1, OP_EFF  = 3'd2,
                         OP_VIEW = 3'd3, OP_TICK = 3'd4, OP_ACK  = 3'd5,
                         OP_NAK  = 3'd6;

    localparam [4:0] ST_RST  = 5'd0,  ST_UNB  = 5'd1,  ST_IDLE = 5'd2,
                     ST_BIND = 5'd3,  ST_LINK = 5'd4,  ST_LNKW = 5'd5,
                     ST_EFF  = 5'd6,  ST_EFFT = 5'd7,  ST_EFFR = 5'd8,
                     ST_VIEW = 5'd9,  ST_VACC = 5'd10, ST_VACW = 5'd11,
                     ST_VRD  = 5'd12, ST_RESP = 5'd13, ST_TICK = 5'd14,
                     ST_TSW  = 5'd15, ST_TSWW = 5'd16, ST_TLEAK = 5'd17,
                     ST_FIRE = 5'd18, ST_EFFI = 5'd19;

    reg [4:0]        state;
    reg              tick_pend;
    reg [AIDW-1:0]   lr_src;
    reg [3:0]        lr_a0;
    reg [PW-1:0]     lr_a1, lr_a2, lr_dat;
    reg [PW-1:0]     viewdat;
    reg              resp_nak;
    reg [EIW:0]      eidx;      // one bit wider: EDGES_N sentinel
    reg [PW:0]       wacc;
    reg [PW-1:0]     refr;
    reg [PW-1:0]     afire;

    reg [AIDW-1:0] etab [0:EDGES_N-1];
    reg            ev   [0:EDGES_N-1];

    function [PW-1:0] sclip16;  // saturate to Q1.15 full scale, never wrap
        input signed [35:0] v;
        begin
            if (v > 36'sd32767)
                sclip16 = 16'h7FFF;
            else if (v < -36'sd32768)
                sclip16 = 16'h8000;
            else
                sclip16 = v[15:0];
        end
    endfunction

    // effect integration: act += sat((unsigned w * signed dat) >>> 15)
    wire signed [35:0] act_e  = {{20{act[PW-1]}}, act};
    wire signed [32:0] prod   = $signed({1'b0, hb_w}) * $signed(lr_dat);
    wire signed [35:0] prod_e = {{3{prod[32]}}, prod};
    wire signed [35:0] eff_sum = act_e + (prod_e >>> 15);
    // tick leak: act = act - (act >>> ka)
    wire signed [35:0] leak_sum = act_e - (act_e >>> d_ka);

    integer i;

    // Flit contract keeps ci_a0 full-width; v1 consumes the low nibble
    // (dial address / edge slot). Upper bits are reserved operands.
    /* verilator lint_off UNUSEDSIGNAL */
    wire [11:0] ci_a0_rsvd = ci_a0[15:4];
    /* verilator lint_on UNUSEDSIGNAL */

    always @(posedge clk) begin
        if (!rst_n) begin
            state     <= ST_RST;
            ci_ready  <= 1'b0;
            lo_valid  <= 1'b0;
            lo_op     <= {OPW{1'b0}};
            lo_dst    <= {AIDW{1'b0}};
            lo_src    <= {AIDW{1'b0}};
            lo_a0     <= {PW{1'b0}};
            lo_a1     <= {PW{1'b0}};
            lo_a2     <= {PW{1'b0}};
            lo_dat    <= {PW{1'b0}};
            lx_valid  <= 1'b0;
            lx_op     <= {OPW{1'b0}};
            lx_dst    <= {AIDW{1'b0}};
            lx_src    <= {AIDW{1'b0}};
            lx_a0     <= {PW{1'b0}};
            lx_a1     <= {PW{1'b0}};
            lx_a2     <= {PW{1'b0}};
            lx_dat    <= {PW{1'b0}};
            hb_cmd    <= 3'b000;
            hb_sel    <= {EDGES_N{1'b0}};
            hb_base   <= {PW{1'b0}};
            df_wr     <= 1'b0;
            df_addr   <= 4'd0;
            df_wdata  <= {PW{1'b0}};
            df_rd     <= 1'b0;
            bound     <= 1'b0;
            cell_id   <= {AIDW{1'b0}};
            act       <= {PW{1'b0}};
            refr      <= {PW{1'b0}};
            tick_pend <= 1'b0;
            eidx      <= {(EIW+1){1'b0}};
            wacc      <= {(PW+1){1'b0}};
            viewdat   <= {PW{1'b0}};
            resp_nak  <= 1'b0;
            afire     <= {PW{1'b0}};
            lr_src    <= {AIDW{1'b0}};
            lr_a0     <= 4'd0;
            lr_a1     <= {PW{1'b0}};
            lr_a2     <= {PW{1'b0}};
            lr_dat    <= {PW{1'b0}};
            for (i = 0; i < EDGES_N; i = i + 1) begin
                etab[i] <= {AIDW{1'b0}};
                ev[i]   <= 1'b0;
            end
        end else begin
            // single-cycle strobes default low. hb_sel is intentionally
            // NOT pulsed: the engine's readout takes K+1 cycles and the
            // returning hb_w must stay muxed to the active slot until done.
            df_wr    <= 1'b0;
            df_rd    <= 1'b0;
            hb_cmd   <= 3'b000;
            lo_valid <= 1'b0;
            lx_valid <= 1'b0;

            case (state)
              // ---------------------------------------------- reset ---
              ST_RST: state <= ST_UNB;

              // ------------------- wait for first bind (any flit) ---
              ST_UNB: begin
                  ci_ready <= 1'b1;
                  if (ci_valid && ci_ready) begin
                      lr_src <= ci_src;
                      lr_a2  <= ci_a2;
                      if (ci_op == OP_BIND) begin
                          cell_id  <= ci_a0[AIDW-1:0];
                          bound    <= 1'b1;
                          resp_nak <= 1'b0;
                      end else begin
                          resp_nak <= 1'b1;  // not bound: nak
                      end
                      viewdat  <= {PW{1'b0}};
                      ci_ready <= 1'b0;
                      state    <= ST_RESP;
                  end
              end

              // --------------------------------------------- dispatch ---
              ST_IDLE: begin
                  if (tick_pend) begin
                      // Q2 hard deadline: service before any new ingress
                      ci_ready <= 1'b0;
                      hb_sel   <= {EDGES_N{1'b0}};
                      state    <= ST_TICK;
                  end else begin
                      ci_ready <= 1'b1;
                      hb_sel   <= {EDGES_N{1'b0}};
                      if (ci_valid && ci_ready) begin

                          lr_src <= ci_src;
                          lr_a0  <= ci_a0[3:0];
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
              end

              // bind = dial write (or first-bind, handled in ST_UNB) -------
              ST_BIND: begin
                  df_wr    <= 1'b1;
                  df_addr  <= lr_a0;
                  df_wdata <= lr_a1;
                  resp_nak <= 1'b0;
                  viewdat  <= {PW{1'b0}};
                  state    <= ST_RESP;
              end

              // link = edge slot {peer=src, base=a1} -----------------------
              ST_LINK: begin
                  etab[lr_a0[EIW-1:0]] <= lr_src;
                  ev  [lr_a0[EIW-1:0]] <= 1'b1;
                  hb_sel   <= 1'b1 << lr_a0[EIW-1:0];
                  hb_cmd   <= 3'b100;            // set base in the engine
                  hb_base  <= lr_a1;
                  state    <= ST_LNKW;
              end
              ST_LNKW: begin
                  if (hb_done) begin
                      resp_nak <= 1'b0;
                      viewdat  <= {PW{1'b0}};
                      state    <= ST_RESP;
                  end
              end

              // effect: scan edge table for src -----------------------------
              ST_EFF: begin
                  eidx  <= {(EIW+1){1'b0}};
                  state <= ST_EFFT;
              end
              ST_EFFT: begin
                  if (eidx == EDGES_N) begin
                      // unknown source: dropped (link before effect)
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end else if (ev[eidx[EIW-1:0]] && (etab[eidx[EIW-1:0]] == lr_src)) begin
                      hb_sel   <= 1'b1 << eidx[EIW-1:0];
                      hb_cmd   <= 3'b001;        // cofire train
                      state    <= ST_EFFR;
                  end else begin
                      eidx <= eidx + 1'b1;
                  end
              end
              ST_EFFR: begin
                  if (hb_done) begin
                      hb_cmd <= 3'b011;          // weight readback
                      state  <= ST_EFFI;
                  end
              end
              ST_EFFI: begin
                  // readout done: integrate with the post-update weight
                  if (hb_done) begin
                      act      <= sclip16(eff_sum);
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end
              end

              // view -------------------------------------------------------
              ST_VIEW: begin
                  if (!bound) begin
                      resp_nak <= 1'b1;
                      viewdat  <= {PW{1'b0}};
                      state    <= ST_RESP;
                  end else begin
                      case (lr_a0[1:0])
                        2'd0: begin
                            viewdat <= {PW{1'b0}} | act;
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
                        default: begin // 3: cosine not provisioned in v1
                            resp_nak <= 1'b1;
                            viewdat  <= {PW{1'b0}};
                            state    <= ST_RESP;
                        end
                      endcase
                  end
              end
              ST_VACC: begin
                  if (eidx == EDGES_N) begin
                      viewdat  <= wacc[PW] ? {PW{1'b1}} : wacc[PW-1:0];
                      resp_nak <= 1'b0;
                      state    <= ST_RESP;
                  end else if (ev[eidx[EIW-1:0]]) begin
                      hb_sel <= 1'b1 << eidx[EIW-1:0];
                      hb_cmd <= 3'b011;            // readout
                      state  <= ST_VACW;
                  end else begin
                      eidx <= eidx + 1'b1;
                  end
              end
              ST_VACW: begin
                  if (hb_done) begin
                      wacc <= wacc + {1'b0, hb_w};
                      eidx <= eidx + 1'b1;
                      state <= ST_VACC;
                  end
              end
              ST_VRD: begin
                  if (df_rstb) begin
                      viewdat  <= df_rdata;
                      resp_nak <= 1'b0;
                      state    <= ST_RESP;
                  end
              end

              // one response flit to the requester --------------------------
              ST_RESP: begin
                  lo_op    <= resp_nak ? OP_NAK : OP_ACK;
                  lo_valid <= 1'b1;
                  lo_dst   <= lr_src;
                  lo_src   <= cell_id;
                  lo_a0    <= {PW{1'b0}};
                  lo_a1    <= {PW{1'b0}};
                  lo_a2    <= lr_a2;     // echo caller's a2 (correlation)
                  lo_dat   <= viewdat;
                  if (lo_valid && lo_ready) begin
                      lo_valid <= 1'b0;
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end
              end

              // tick: decay sweep over edges -------------------------------
              ST_TICK: begin
                  eidx  <= {(EIW+1){1'b0}};
                  state <= ST_TSW;
              end
              ST_TSW: begin
                  if (eidx == EDGES_N) begin
                      state <= ST_TLEAK;
                  end else if (ev[eidx[EIW-1:0]]) begin
                      hb_sel <= 1'b1 << eidx[EIW-1:0];
                      hb_cmd <= 3'b010;            // advance decay one tick
                      state  <= ST_TSWW;
                  end else begin
                      eidx <= eidx + 1'b1;
                  end
              end
              ST_TSWW: begin
                  if (hb_done) begin
                      eidx <= eidx + 1'b1;
                      state <= ST_TSW;
                  end
              end

              // leak activation, then fire test ------------------------------
              ST_TLEAK: begin
                  act <= sclip16(leak_sum);
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

              // fan out effects to valid edge peers --------------------------
              ST_FIRE: begin
                  if (eidx == EDGES_N) begin
                      act      <= {PW{1'b0}};
                      refr     <= d_refr;
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end else if (ev[eidx[EIW-1:0]]) begin
                      lx_op    <= OP_EFF;
                      lx_valid <= 1'b1;
                      lx_dst   <= etab[eidx[EIW-1:0]];
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

    // Q2 interlock: the tick deadline register. s_tick latches from any
    // state; cleared exactly when ST_IDLE begins servicing it.
    always @(posedge clk) begin
        if (!rst_n)
            tick_pend <= 1'b0;
        else if (s_tick)
            tick_pend <= 1'b1;
        else if (state == ST_IDLE && tick_pend)
            tick_pend <= 1'b0;
    end

endmodule
