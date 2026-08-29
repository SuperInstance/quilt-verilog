// PROVENANCE: proposals/opencode/RTL-SKETCH.md (round-1 competition entry: opencode)
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
    wire [2*PW-1:0]   dfw = dfm[3*PW-2 -: PW];   // >> (PW-1)
    wire [2*PW-1:0]   dsw = dsm[3*PW-2 -: PW];
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
