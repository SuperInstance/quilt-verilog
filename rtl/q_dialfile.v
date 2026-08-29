// q_dialfile.v -- runtime dial register file (quilt-verilog v1).
// Map per opencode RTL-SKETCH §3 (steal 2 of the scorecard), extended with
// the v1 decay-engine dials P0E / MODE / HL. One sync write port (qm_bind),
// one sync read port (qm_view); reset loads defaults (no `initial`).
// ETA_F/ETA_S/KF/KS/COS_MIN are reserved for post-v1 engines; they are
// readable fabric state via view(2). Pure Verilog-2005.
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

    // combinational datapath fan-outs
    output wire [DW-1:0]        o_eta_f,
    output wire [DW-1:0]        o_eta_s,
    output wire [3:0]           o_kf,
    output wire [3:0]           o_ks,
    output wire [3:0]           o_ka,
    output wire signed [DW-1:0] o_thresh,
    output wire [DW-1:0]        o_refr,
    output wire [DW-1:0]        o_cosmin,
    output wire [4:0]           o_p0e,     // log2(P0): hyperbolic horizon
    output wire                 o_mode,    // 0=ladder, 1=hyperbolic decay
    output wire [DW-1:0]        o_hl       // ladder half-life (ticks)
);
    localparam [AW-1:0] D_ETA_F  = 4'd0,  D_ETA_S  = 4'd1,  D_KF     = 4'd2,
                        D_KS     = 4'd3,  D_KA     = 4'd4,  D_THRESH = 4'd5,
                        D_REFR   = 4'd6,  D_COSMIN = 4'd7,  D_P0E    = 4'd8,
                        D_MODE   = 4'd9,  D_HL     = 4'd10;

    reg [DW-1:0] dial [0:ND-1];

    always @(posedge clk) begin
        if (!rst_n) begin
            dial[D_ETA_F]  <= 16'h0800;  // 0.0625
            dial[D_ETA_S]  <= 16'h0080;  // 0.0031
            dial[D_KF]     <= 16'd6;     // tau_f = 64 ticks
            dial[D_KS]     <= 16'd12;    // tau_s = 4096 ticks
            dial[D_KA]     <= 16'd5;     // act leak shift
            dial[D_THRESH] <= 16'h6000;  // 0.75
            dial[D_REFR]   <= 16'd4;
            dial[D_COSMIN] <= 16'h2CCD;  // 0.35
            dial[D_P0E]    <= 16'd20;    // P0 = 2^20 ticks
            dial[D_MODE]   <= 16'd0;     // glm ladder
            dial[D_HL]     <= 16'd64;    // ladder half-life
            o_rdata <= {DW{1'b0}};
            o_rstb  <= 1'b0;
        end else begin
            if (i_wr)
                dial[i_addr] <= i_wdata;
            o_rstb <= i_rd;
            if (i_rd)
                o_rdata <= dial[i_addr]; // read-old on wr/rd collision
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
    assign o_p0e    = dial[D_P0E][4:0];
    assign o_mode   = dial[D_MODE][0];
    assign o_hl     = dial[D_HL];

endmodule
