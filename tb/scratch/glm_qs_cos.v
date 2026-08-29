// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
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
