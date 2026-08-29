// tb_hebb_edge.v -- hebbian_edge_update engine tests (Q3 golden bounds).
//  T1 ladder exact: N cofires, no shift -> base + N*2^8 exactly.
//  T2 ladder envelope: global shift boundaries put each event in class
//     floor(age/H) or floor(age/H)+1 (phase-dependent), so the staircase
//     stays within a factor of 2 of the continuous law either way:
//     W_exact/2 <= What <= 2*W_exact.
//  T3 ladder shift: HL ticks halve the readout (staircase steps).
//  T4 hyperbolic exact: W cofires -> W*2^8 readout.
//  T5 hyperbolic envelope: W_true(P0) <= W_rtl <= W_true(t/4), checkpoints.
`timescale 1ns/1ps
module tb_hebb_edge;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg         sel = 1;
    reg  [2:0]  cmd = 0;
    reg         mode = 0;
    reg  [15:0] base = 0, hl = 64;
    reg  [4:0]  p0e = 20;
    wire        done;
    wire [15:0] w;
    wire        ovf;

    integer errors = 0;
    integer guard;

    q_hebb_edge u_dut (
        .clk(clk), .rst_n(rst_n), .i_sel(sel), .i_cmd(cmd),
        .i_mode(mode), .i_base(base), .i_hl(hl), .i_p0e(p0e),
        .o_done(done), .o_w(w), .o_ovf(ovf)
    );

    task pulse(input [2:0] c);
        begin
            @(negedge clk); cmd = c;
            @(negedge clk); cmd = 0;
        end
    endtask

    task do_train; begin pulse(3'b001); end endtask
    task do_tick;  begin pulse(3'b010); @(negedge clk); end endtask

    task do_read(output [15:0] rw);
        begin
            @(negedge clk); cmd = 3'b011;
            @(negedge clk); cmd = 0;
            guard = 0;
            while (done !== 1'b1 && guard < 100) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 100) begin
                errors = errors + 1;
                $display("FAIL read_timeout");
                rw = 16'hxxxx;
            end else begin
                rw = w;
                @(negedge clk);
            end
        end
    endtask

    task do_setbase(input [15:0] b);
        begin
            base = b; pulse(3'b100);
        end
    endtask

    task chk(input [15:0] got, input [15:0] exp, input [127:0] name);
        begin
            if (got !== exp) begin
                errors = errors + 1;
                $display("FAIL %0s got=%h exp=%h", name, got, exp);
            end
        end
    endtask

    // envelope helper: real bounds to integer compare
    real wlo, whi;
    integer wint;
    reg [15:0] rw;

    // T2 event schedule (ages at read): 35,32,28,15,0 with HL=8
    real wexp;

    integer n, t, k;
    real glo, ghi;

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);

        // ---------------- T1: ladder exact ----------------
        mode = 0; hl = 64;
        do_setbase(16'h1000);
        for (n = 0; n < 100; n = n + 1) do_train;
        do_read(rw);
        chk(rw, 16'h1000 + 100*256, "T1_ladder_exact");

        // ---------------- T3: ladder shift staircase ----------------
        // hl=2: after 2 ticks bucket0 -> bucket1 (halves), etc.
        hl = 2;
        do_tick; do_tick;
        do_read(rw);
        chk(rw, 16'h1000 + 100*128, "T3_shift1");
        do_tick; do_tick;
        do_read(rw);
        chk(rw, 16'h1000 + 100*64, "T3_shift2");

        // ---------------- T2: ladder 2x envelope ----------------
        rst_n = 0; base = 0; hl = 8;
        repeat (2) @(negedge clk); rst_n = 1;
        repeat (2) @(negedge clk);
        // events at tick offsets 0, 3, 7, 20, 45 (ages 35,32,28,15,0)
        do_train;                       // age will be 35
        for (k = 0; k < 3;  k = k + 1) do_tick;
        do_train;                       // 32
        for (k = 0; k < 4;  k = k + 1) do_tick;
        do_train;                       // 28
        for (k = 0; k < 13; k = k + 1) do_tick;
        do_train;                       // 15
        for (k = 0; k < 15; k = k + 1) do_tick;
        do_train;                       // 0
        do_read(rw);
        wexp = 256.0 * (2.0**(-35.0/8.0) + 2.0**(-32.0/8.0)
                      + 2.0**(-28.0/8.0) + 2.0**(-15.0/8.0) + 1.0);
        wint = rw;
        if (!(wexp/2.0 - 1.0 <= wint && wint <= 2.0*wexp + 1.0)) begin
            errors = errors + 1;
            $display("FAIL T2_env wexp=%f rtl=%0d", wexp, wint);
        end

        // ---------------- T4: hyperbolic exact ----------------
        rst_n = 0; mode = 1; p0e = 12; base = 0;
        repeat (2) @(negedge clk); rst_n = 1;
        repeat (2) @(negedge clk);
        for (n = 0; n < 100; n = n + 1) do_train;
        do_read(rw);
        chk(rw, 100*256, "T4_hyp_exact");

        // ---------------- T5: hyperbolic envelope ----------------
        // bounds: W0/(1+W0*t/P0) <= W_rtl <= W0/(1+W0*t/(4*P0))
        for (t = 1; t <= 4096; t = t + 1) begin
            do_tick;
            if (t == 256 || t == 512 || t == 1024 || t == 2048 || t == 4096) begin
                do_read(rw);
                wint = rw >> 8;   // undo the x256 scale (no saturation: W<=100)
                glo = 100.0 / (1.0 + 100.0 * t / 4096.0);
                ghi = 100.0 / (1.0 + 100.0 * t / (4.0 * 4096.0));
                if (!(glo - 1.0 <= wint && wint <= ghi + 1.0)) begin
                    errors = errors + 1;
                    $display("FAIL T5_env t=%0d rtl=%0d lo=%f hi=%f",
                             t, wint, glo, ghi);
                end
            end
        end

        if (errors == 0) $display("TB_HEBB_EDGE PASS");
        else $display("TB_HEBB_EDGE FAIL %0d", errors);
        $finish;
    end
endmodule
