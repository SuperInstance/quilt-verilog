// PROVENANCE: proposals/opencode/RTL-SKETCH.md (round-1 competition entry: opencode)
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
