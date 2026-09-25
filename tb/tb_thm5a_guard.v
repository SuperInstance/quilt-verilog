// tb_thm5a_guard.v -- EXPECTED-FAIL harness for the q_hebb_edge elaboration
// guard (Thm 5a width check): instantiates the overflowing config K=9,B=8.
// PASS condition is the ELAB ERROR line + $finish at time 0 -- run_suite.sh
// greps for it. This TB must never print its own PASS.
`timescale 1ns/1ps
module tb_thm5a_guard;
    q_hebb_edge #(.PW(16), .K(9), .B(8)) dut (
        .clk(), .rst_n(), .i_sel(1'b0), .i_cmd(3'b000), .i_mode(1'b0),
        .i_base(16'h0000), .i_hl(16'h0001), .i_p0e(5'd0), .i_gclass(4'd0),
        .o_done(), .o_w(), .o_ovf());
    initial begin
        #1000;
        $display("TB-THM5A-GUARD FAIL: overflowing config elaborated without guard firing");
        $finish;
    end
endmodule
