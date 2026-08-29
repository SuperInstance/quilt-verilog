// PROVENANCE: proposals/opencode/RTL-SKETCH.md (round-1 competition entry: opencode)
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
    reg [EIW-1:0]    eidx, eslot;
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
            eidx     <= {EIW{1'b0}};
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
                  eidx  <= {EIW{1'b0}};
                  state <= ST_EFFW;
              end
              ST_EFFW: begin
                  if (eidx == EDGES_N[EIW-1:0]) begin
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
                      eidx <= eidx + {{EIW-1{1'b0}}, 1'b1};
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
                        eidx  <= {EIW{1'b0}};
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
                  if (eidx == EDGES_N[EIW-1:0]) begin
                      viewdat  <= wacc[PW] ? {PW{1'b1}} : wacc[PW-1:0];
                      resp_nak <= 1'b0;
                      state    <= ST_RESP;
                  end else begin
                      wacc <= wacc + {1'b0, wtab[eidx]};
                      eidx <= eidx + {{EIW-1{1'b0}}, 1'b1};
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
                  eidx  <= {EIW{1'b0}};
                  state <= ST_TDEC;
              end
              ST_TDEC: begin
                  if (eidx == EDGES_N[EIW-1:0]) begin
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
                      eidx <= eidx + {{EIW-1{1'b0}}, 1'b1};
                  end
              end
              ST_TDW: begin
                  if (hb_done) begin
                      wtab[eidx] <= hb_w;
                      eidx       <= eidx + {{EIW-1{1'b0}}, 1'b1};
                      state      <= ST_TDEC;
                  end
              end

              // leak activation, then fire test -------------------------
              ST_TLEAK: begin
                  act <= sclip16(act - (act >>> d_ka));
                  if ((act >= d_thresh) && (refr == {PW{1'b0}})) begin
                      afire <= act;
                      eidx  <= {EIW{1'b0}};
                      state <= ST_FIRE;
                  end else begin
                      if (refr != {PW{1'b0}})
                          refr <= refr - {{PW-1{1'b0}}, 1'b1};
                      ci_ready <= 1'b1;
                      state    <= ST_IDLE;
                  end
              end

              // fan out effects to valid edges --------------------------
              ST_FIRE: begin
                  if (eidx == EDGES_N[EIW-1:0]) begin
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
                          eidx     <= eidx + {{EIW-1{1'b0}}, 1'b1};
                      end
                  end else begin
                      eidx <= eidx + {{EIW-1{1'b0}}, 1'b1};
                  end
              end

              default: state <= ST_IDLE;
            endcase
        end
    end

endmodule
