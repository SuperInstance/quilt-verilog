// tb_q_rqh_bank.v -- RQH residue bank tests (corrected deposit), house
// method: bit-exact integer golden; pass = zero errors.
// Covers flash.md §5 as amended by error-envelopes.md T3/C3: disabled A/B
// passthrough; bit-exact corrected deposit math for all classes; class
// clamp; credit/antic cadence incl. saturation; deadband leak; train-vs-
// tick priority; cross-edge isolation; QDW scale-invariance of the credit.
`timescale 1ns/1ps
module tb_q_rqh_bank;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg         train = 0, tick = 0, en = 0;
    reg  [3:0]  gcl = 0, qdw = 8, qleak = 8;
    reg  [3:0]  sel = 4'b0001;
    wire [15:0] credit;
    wire        antic;

    integer errors = 0;

    q_rqh_bank #(.RW(16), .K(8), .PW(16), .EDGES_N(4), .EIW(2)) u_dut (
        .clk(clk), .rst_n(rst_n),
        .i_train(train), .i_tick(tick),
        .i_sel(sel), .i_gclass(gcl),
        .i_qdw(qdw), .i_qleak(qleak), .i_en(en),
        .o_credit(credit), .o_antic(antic)
    );

    task do_reset; begin
        rst_n = 0; train = 0; tick = 0; en = 0;
        repeat (2) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);
    end endtask

    task pulse_train(input [3:0] g); begin
        @(negedge clk); gcl = g; train = 1;
        @(negedge clk); train = 0;
    end endtask

    task pulse_tick; begin
        @(negedge clk); tick = 1;
        @(negedge clk); tick = 0;
    end endtask

    // golden deposit: 2^(K+QDW-g) * 9/32, computed with the same shifts
    integer K_G = 8;
    function integer dep_g(input integer g, input integer q);
        integer x;
        begin
            x = 1 << (K_G + q - g);
            dep_g = (x >> 2) + (x >> 5);
        end
    endfunction

    function integer min32(input integer a, input integer b);
        begin
            min32 = (a < b) ? a : b;
        end
    endfunction

    task chk16(input [15:0] got, input [15:0] exp, input [127:0] name);
        begin
            if (got !== exp) begin
                errors = errors + 1;
                $display("FAIL %0s got=%h exp=%h", name, got, exp);
            end
        end
    endtask

    task chk1(input got, input exp, input [127:0] name);
        begin
            if (got !== exp) begin
                errors = errors + 1;
                $display("FAIL %0s got=%b exp=%b", name, got, exp);
            end
        end
    endtask

    // leak golden: R <- (R - R>>qleak), snap to 0 at <= 1 or no progress
    function integer lea_g(input integer r, input integer q);
        integer l;
        begin
            l = r - (r >> q);
            lea_g = (l <= 1 || l >= r) ? 0 : l;
        end
    endfunction

    integer g, n, rg, R0, R1;
    integer antic_cnt_x;

    // antic observer: count pulses whenever the DUT raises o_antic
    always @(posedge clk) begin
        if (rst_n && antic)
            antic_cnt_x = antic_cnt_x + 1;
    end

    initial begin
        do_reset;

        // ---- T1: enabled, empty bank: credit 0 ----
        en = 1; sel = 4'b0001;
        chk16(credit, 16'd0, "T1_credit0");

        // ---- T2: disabled A/B -- trains and ticks quiesce to nothing ----
        en = 0;
        pulse_train(4'd0); pulse_tick;
        chk16(credit, 16'd0, "T2_credit0");
        chk1(antic, 1'b0, "T2_antic0");
        // frozen-state check: deposit with en, then storm with !en
        en = 1; pulse_train(4'd0);            // R0 = dep(0)
        rg = dep_g(0, 8);
        chk16(credit, rg >> 8, "T2_r_en");
        en = 0;
        for (n = 0; n < 20; n = n + 1) begin
            pulse_train(4'd0); pulse_tick;
        end
        en = 1;
        @(negedge clk);                     // settle: let i_en propagate
        chk16(credit, rg >> 8, "T2_frozen");

        // ---- T3: corrected deposit math, bit-exact, all classes g=0..7 ----
        for (g = 0; g <= 7; g = g + 1) begin
            do_reset; en = 1; sel = 4'b0001; qdw = 8;
            pulse_train(g[3:0]);
            rg = dep_g(g, 8);
            chk16(credit, (rg >> 8), "T3_deposit");
            if ((rg >> 8) != (rg / 256)) begin
                errors = errors + 1;
                $display("FAIL T3_credit_math g=%0d", g);
            end
        end

        // ---- T4: class clamp: g >= K deposits as class K-1 ----
        for (g = 8; g <= 15; g = g + 1) begin
            do_reset; en = 1; sel = 4'b0001; qdw = 8;
            pulse_train(g[3:0]);
            chk16(credit, dep_g(7, 8) >> 8, "T4_clamp");
        end

        // ---- T5: credit/antic cadence + saturation (class 0, QDW=8) ----
        // dep(0) = 18432; credit 72/train; saturates at R=65535 (credit 255):
        // 6 trains -> credits 72,144,216,255,255,255 -> exactly 4 increments
        do_reset; en = 1; sel = 4'b0001; qdw = 8;
        rg = 0; antic_cnt_x = 0;
        for (n = 1; n <= 6; n = n + 1) begin
            pulse_train(4'd0);
            rg = min32(rg + dep_g(0, 8), 65535);
            chk16(credit, rg >> 8, "T5_credit");
        end
        if (antic_cnt_x !== 4) begin
            errors = errors + 1;
            $display("FAIL T5_antic cnt=%0d exp=4", antic_cnt_x);
        end

        // ---- T6: graded cadence (class 3): dep=2304, credit 9/train ----
        do_reset; en = 1; sel = 4'b0010; qdw = 8;
        rg = 0;
        for (n = 1; n <= 30; n = n + 1) begin
            pulse_train(4'd3);
            rg = min32(rg + dep_g(3, 8), 65535);
            chk16(credit, rg >> 8, "T6_credit");
        end

        // ---- T7: deadband leak, bit-exact + snap-to-0 + stays-0 ----
        // qleak=4: 18432 -> 0 in ~152 ticks (fits the 200-tick window)
        do_reset; en = 1; sel = 4'b0001; qdw = 8; qleak = 4;
        pulse_train(4'd0);                    // R = 18432
        rg = dep_g(0, 8);
        for (n = 1; n <= 200; n = n + 1) begin
            pulse_tick;
            rg = lea_g(rg, 4);
            chk16(credit, rg >> 8, "T7_leak");
            if (rg == 0) begin
                // snapped: must stay 0
                pulse_tick; rg = lea_g(rg, 4);
                chk16(credit, 16'd0, "T7_snap_hold");
                n = 201;                       // exit loop
            end
        end
        if (rg != 0) begin
            errors = errors + 1;
            $display("FAIL T7_no_snap rg=%0d", rg);
        end
        // fast leak: qleak=1 halves each tick, snaps cleanly
        do_reset; en = 1; sel = 4'b0001; qdw = 8; qleak = 1;
        pulse_train(4'd0); rg = dep_g(0, 8);
        for (n = 0; n < 25; n = n + 1) begin
            pulse_tick; rg = lea_g(rg, 1);
        end
        chk16(credit, 16'd0, "T7_fast_snap");

        // ---- T8: train beats same-cycle tick ----
        do_reset; en = 1; sel = 4'b0100; qdw = 8; qleak = 1;
        pulse_train(4'd2);
        @(negedge clk);
        tick = 1; train = 1; gcl = 4'd2;
        @(negedge clk); tick = 0; train = 0;
        rg = min32(dep_g(2, 8) * 2, 65535);
        chk16(credit, rg >> 8, "T8_train_wins");

        // ---- T9: cross-edge isolation ----
        do_reset; en = 1; qdw = 8; qleak = 8;
        sel = 4'b0001; pulse_train(4'd0);      // edge0: 18432
        R0 = dep_g(0, 8);
        sel = 4'b0010;
        for (n = 0; n < 10; n = n + 1) pulse_tick;   // edge1 ticks from 0
        chk16(credit, 16'd0, "T9_e1_zero");
        sel = 4'b0001;
        @(negedge clk);                     // settle: let the mux flip
        chk16(credit, R0 >> 8, "T9_e0_untouched");
        sel = 4'b0010; pulse_train(4'd1);      // edge1: dep(1) = 9216
        R1 = dep_g(1, 8);
        chk16(credit, R1 >> 8, "T9_e1_dep");
        sel = 4'b0001;
        @(negedge clk);                     // settle: let the mux flip
        chk16(credit, R0 >> 8, "T9_e0_still");

        // ---- T10: QDW scale-invariance of the credit (the T3c formula's
        //      2^QDW factor exactly cancels in readout LSBs) ----
        for (g = 0; g <= 5; g = g + 1) begin
            do_reset; en = 1; sel = 4'b0001; qdw = 6;
            pulse_train(g[3:0]);
            if (dep_g(g, 6) >= 65536) begin
                errors = errors + 1;
                $display("FAIL T10_overflow g=%0d", g);
            end
            chk16(credit, dep_g(g, 6) >> 6, "T10_qdw6");
        end

        if (errors == 0)
            $display("TB_Q_RQH_BANK PASS");
        else
            $display("TB_Q_RQH_BANK FAIL %0d", errors);
        $finish;
    end

    initial begin
        #20_000_000;
        $display("TB_Q_RQH_BANK FAIL watchdog");
        $finish;
    end
endmodule
