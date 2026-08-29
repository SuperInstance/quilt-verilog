// tb_q_echo_gate.v -- echo gate (fire trace) tests, house method:
// bit-exact integer golden + real-arithmetic envelope; pass = zero errors.
// Mirrors the verified scratch TB of proposals/innovations/opencode.md §5
// row 1 (reset; refill; leak recurrence KLE in {1,2,3}; real envelope;
// dyadic class bracket; snap hysteresis/window; fire-vs-leak priority;
// disabled mode; dead-trace semantics).
`timescale 1ns/1ps
module tb_q_echo_gate;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg          fire = 0, tick = 0;
    reg  [3:0]   kle = 2;
    reg  [15:0]  floor_v = 16'h0080;
    wire [15:0]  f;
    wire         live;
    wire [3:0]   gclass;

    integer errors = 0;

    q_echo_gate u_dut (
        .clk(clk), .rst_n(rst_n),
        .i_fire(fire), .i_tick(tick),
        .i_kle(kle), .i_floor(floor_v),
        .o_f(f), .o_live(live), .o_gclass(gclass)
    );

    task pulse_fire; begin
        @(negedge clk); fire = 1;
        @(negedge clk); fire = 0;
    end endtask

    task pulse_tick; begin
        @(negedge clk); tick = 1;
        @(negedge clk); tick = 0;
    end endtask

    // bit-exact golden model of the trace (snap: below floor, terminal
    // residue, or no progress)
    integer fg = 0;
    integer kle_g = 2;
    integer floor_g = 16'h0080;

    function integer leak1(input integer v, input integer k);
        integer l;
        begin
            l = v - (v >> k);
            leak1 = (l <= floor_g || l <= 1 || l >= v) ? 0 : l;
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

    integer d, n, winticks;
    real kpow, flo, fhi;

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);

        // ---- T0: reset -> dead trace, gate closed, class 0 ----
        chk16(f, 16'h0000, "T0_f");
        chk1(live, 1'b0, "T0_live");
        chk1(gclass, 4'd0, "T0_g");

        // ---- T1: fire refills to max, class 0, live ----
        floor_v = 16'h0080; kle = 2; kle_g = 2; floor_g = 16'h0080;
        pulse_fire;
        @(negedge clk);
        chk16(f, 16'hFFFF, "T1_f");
        chk1(live, 1'b1, "T1_live");
        chk1(gclass, 4'd0, "T1_g");

        // ---- T2: leak recurrence bit-exact for KLE in {1,2,3}, 40 ticks,
        //      plus the real envelope k(d)*F0 <= f <= k(d)*F0 + d ----
        for (n = 1; n <= 3; n = n + 1) begin
            kle = n[3:0]; kle_g = n;
            rst_n = 0; repeat (2) @(negedge clk); rst_n = 1;
            repeat (2) @(negedge clk);
            pulse_fire; fg = 16'hFFFF;
            kpow = 1.0;
            for (d = 1; d <= 40; d = d + 1) begin
                pulse_tick;
                @(negedge clk);
                fg = leak1(fg, kle_g);
                if (f !== fg[15:0]) begin
                    errors = errors + 1;
                    $display("FAIL T2_leak kle=%0d d=%0d got=%h exp=%h",
                             n, d, f, fg[15:0]);
                end
                // envelope: leak error accumulates < 1 LSB per tick
                kpow = kpow * (1.0 - (1.0 / (2.0 ** n)));
                flo = kpow * 65535.0;
                fhi = flo + d + 1.0;
                if (f != 0 && ((1.0 * f) < flo || (1.0 * f) > fhi)) begin
                    errors = errors + 1;
                    $display("FAIL T2_env kle=%0d d=%0d f=%0d lo=%f hi=%f",
                             n, d, f, flo, fhi);
                end
                // dyadic class bracket on live ticks: 2^(15-g) <= f < 2^(16-g)
                if (live) begin
                    winticks = 0;
                    winticks = 1 << (15 - gclass);
                    if (f < winticks || f >= (winticks << 1)) begin
                        errors = errors + 1;
                        $display("FAIL T2_bracket kle=%0d d=%0d f=%h g=%0d",
                                 n, d, f, gclass);
                    end
                end
            end
        end

        // ---- T3: snap hysteresis + window length (KLE=2, FLOOR=0x0080) ----
        kle = 2; kle_g = 2; floor_v = 16'h0080; floor_g = 16'h0080;
        rst_n = 0; repeat (2) @(negedge clk); rst_n = 1;
        repeat (2) @(negedge clk);
        pulse_fire; fg = 16'hFFFF;
        // analytic window: ln(0xFFFF/0x80)/ln(4/3) ~ 21.7 ticks
        d = 0;
        while (f !== 16'h0000 && d < 40) begin
            pulse_tick; @(negedge clk);
            fg = leak1(fg, kle_g);
            d = d + 1;
            if (f !== fg[15:0]) begin
                errors = errors + 1;
                $display("FAIL T3_leak d=%0d got=%h exp=%h", d, f, fg[15:0]);
            end
        end
        if (d < 18 || d > 24) begin
            errors = errors + 1;
            $display("FAIL T3_window d=%0d (exp 18..24)", d);
        end
        // dead stays dead: 5 more ticks, f pinned 0, gate closed
        for (n = 0; n < 5; n = n + 1) begin
            pulse_tick; @(negedge clk);
            chk16(f, 16'h0000, "T3_dead");
            chk1(live, 1'b0, "T3_deadlive");
        end

        // ---- T3b: sticky-band regression (small FLOOR, large KLE) ----
        // KLE=4, FLOOR=2: the raw sketch parks the trace at f in [2,15]
        // (leak-by-zero, no snap), leaving the gate open forever; the
        // no-progress snap must drain it to exactly 0
        kle = 4; kle_g = 4; floor_v = 16'd2; floor_g = 2;
        rst_n = 0; repeat (2) @(negedge clk); rst_n = 1;
        repeat (2) @(negedge clk);
        pulse_fire; fg = 16'hFFFF;
        d = 0;
        while (f !== 16'h0000 && d < 200) begin
            pulse_tick; @(negedge clk);
            fg = leak1(fg, kle_g);
            d = d + 1;
            if (f !== fg[15:0]) begin
                errors = errors + 1;
                $display("FAIL T3b_leak d=%0d got=%h exp=%h", d, f, fg[15:0]);
            end
        end
        chk16(f, 16'h0000, "T3b_drained");
        chk1(live, 1'b0, "T3b_dead");

        // ---- T4: fire beats same-cycle leak ----
        pulse_fire; fg = 16'hFFFF;
        @(negedge clk);
        fire = 1; tick = 1;
        @(negedge clk); fire = 0; tick = 0;
        chk16(f, 16'hFFFF, "T4_fire_wins");

        // ---- T5: disabled mode (FLOOR = 0) = v1 semantics ----
        floor_v = 16'h0000; floor_g = 0;
        kle = 2; kle_g = 2;
        rst_n = 0; repeat (2) @(negedge clk); rst_n = 1;
        repeat (2) @(negedge clk);
        // dead trace, gate still open, class 0
        chk16(f, 16'h0000, "T5_f0");
        chk1(live, 1'b1, "T5_live_dead");
        chk1(gclass, 4'd0, "T5_g_dead");
        // after fire and one leak: still live, class forced 0
        pulse_fire;
        pulse_tick; @(negedge clk);
        chk16(f, 16'hC000, "T5_f_leak");
        chk1(live, 1'b1, "T5_live_leak");
        chk1(gclass, 4'd0, "T5_g_leak");

        // ---- T6: graded classes from a full trace (KLE=2, FLOOR=0x0080) ----
        floor_v = 16'h0080; floor_g = 16'h0080;
        rst_n = 0; repeat (2) @(negedge clk); rst_n = 1;
        repeat (2) @(negedge clk);
        pulse_fire;
        // golden-checked ladder of classes as the trace decays; assert the
        // dyadic bracket on each live tick (d=0: g=0; the trace crosses
        // each class boundary at powers of two)
        for (d = 1; d <= 12; d = d + 1) begin
            pulse_tick; @(negedge clk);
            if (live) begin
                winticks = 1 << (15 - gclass);
                if (f < winticks || f >= (winticks << 1)) begin
                    errors = errors + 1;
                    $display("FAIL T6_bracket d=%0d f=%h g=%0d", d, f, gclass);
                end
            end
        end

        if (errors == 0)
            $display("TB_Q_ECHO_GATE PASS");
        else
            $display("TB_Q_ECHO_GATE FAIL %0d", errors);
        $finish;
    end

    initial begin
        #10_000_000;
        $display("TB_Q_ECHO_GATE FAIL watchdog");
        $finish;
    end
endmodule
