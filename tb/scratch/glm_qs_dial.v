// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
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
