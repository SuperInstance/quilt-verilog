// tb_01_counter.sv -- self-checking testbench for quilt_01_counter (the
// step-1 lowering of examples/quil/01-counter.qm by tools/quilt_lower.py).
// Checks: synchronous reset holds count at the init value 0, then ten
// free-running clocks leave count == 10 (one journal entry per tick).
`timescale 1ns/1ps

module tb_01_counter;
    reg  clk = 1'b0;
    reg  rst = 1'b1;
    wire [15:0] count;

    integer errors = 0;
    integer i;

    quilt_01_counter dut (.clk(clk), .rst(rst), .count(count));

    always #5 clk = ~clk;

    task check(input integer got, input integer expect_val,
               input string what);
        if (got !== expect_val) begin
            $display("FAIL %s: count=%0d, expected %0d", what, got, expect_val);
            errors = errors + 1;
        end else begin
            $display("PASS %s: count=%0d", what, got);
        end
    endtask

    initial begin
        @(posedge clk);
        @(posedge clk);
        #1 rst = 1'b0;
        check(count, 0, "after synchronous reset");

        for (i = 1; i <= 10; i = i + 1) begin
            @(posedge clk);
            #1;
            check(count, i, $sformatf("tick %0d", i));
        end
        check(count, 10, "final: count==10 after 10 clocks");

        if (errors == 0) begin
            $display("TB PASS tb_01_counter");
            $finish;
        end else begin
            $display("TB FAIL tb_01_counter: %0d check(s) failed", errors);
            $fatal(1);
        end
    end
endmodule
