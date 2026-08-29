// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
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
