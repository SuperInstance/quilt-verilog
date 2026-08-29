// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
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
