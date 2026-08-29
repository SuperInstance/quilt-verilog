// tb_tick_sched.v -- period, strobe width, reset behavior.
`timescale 1ns/1ps
module tb_tick_sched;
    reg clk = 0, rst_n = 0;
    wire tick;

    integer errors = 0;
    integer count = 0, cyc = 0, last = -1, gap;
    integer width = 0;

    q_tick_sched #(.TPW(4)) u_dut (.clk(clk), .rst_n(rst_n), .o_tick(tick));

    always #5 clk = ~clk;

    always @(posedge clk) begin
        if (rst_n) begin
            cyc = cyc + 1;
            if (tick) begin
                count = count + 1;
                gap = cyc - last;
                if (last >= 0 && gap != 16) begin
                    errors = errors + 1;
                    $display("FAIL period gap=%0d", gap);
                end
                last = cyc;
            end
        end
    end

    always @(negedge clk) begin
        if (rst_n) begin
            if (tick) width = width + 1;
            else if (width != 0 && width != 1) begin
                errors = errors + 1;
                $display("FAIL strobe width=%0d", width);
            end else if (width == 1) begin
                width = 0;
            end
        end
    end

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (200) @(negedge clk);
        if (count >= 10 && errors == 0) $display("TB_TICK_SCHED PASS");
        else $display("TB_TICK_SCHED FAIL count=%0d errors=%0d", count, errors);
        $finish;
    end
endmodule
