// tb_envelope_fuzz.v -- B2 closing artifact, error-envelopes.md section 7
// row 1: the ladder envelope W/2 - 1 <= What <= 2W + 1 (Theorem 1,
// arbitrary arrivals) asserted at EVERY read of two long random arrival
// streams. tb_hebb_edge T2 asserts the band on ONE 5-event schedule;
// this bench fuzzes: LCG-driven gaps (1..2.5H ticks) with bursts (1..5
// trains at one tick), exact continuous golden W = 2^K * sum
// 2^(-(t-te)/H) accumulated per event (K=8: one fresh cofire reads
// 256), readout checked after every event batch.
// Configs: H=16 and H=64, 400 events each, base=0 so o_w is the raw
// readout. Also asserts o_ovf stays clear (saturation would break the
// sum and is a different theorem). Deterministic seeds; real arithmetic
// is self-test-only per house rule.
`timescale 1ns/1ps
module tb_envelope_fuzz;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg         sel = 1;
    reg  [2:0]  cmd = 0;
    reg         mode = 0;
    reg  [15:0] base = 0, hl = 16;
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

    // deterministic LCG
    reg [31:0] rng = 32'hDECAFBAD;
    function [31:0] lcg(input [31:0] x);
        lcg = x * 32'h41C64E6D + 32'h3039;
    endfunction

    task pulse(input [2:0] c);
        begin
            @(negedge clk); cmd = c;
            @(negedge clk); cmd = 0;
        end
    endtask

    task do_tick;  begin pulse(3'b010); end endtask
    task do_train; begin pulse(3'b001); end endtask

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

    // one fuzz config: H ticks/half-life, n_ev events
    task run_config(input [15:0] H, input integer n_ev,
                    input [31:0] seed);
        real wexp, lo, hi, rw_r;
        integer t, i, gap, burst, j;
        reg [15:0] rw;
        begin
            rng = seed;
            hl = H;
            // reset DUT state via rst_n pulse
            @(negedge clk); rst_n = 0;
            repeat (2) @(negedge clk); rst_n = 1;
            repeat (2) @(negedge clk);
            t = 0;
            wexp = 0.0;
            for (i = 0; i < n_ev; i = i + 1) begin
                gap = (lcg(rng) % (H + (H >> 1))) + 1;   // 1 .. 2.5H
                rng = lcg(rng);
                for (j = 0; j < gap; j = j + 1) begin
                    do_tick; t = t + 1;
                    wexp = wexp / 2.0 ** (1.0 / H);
                end
                burst = (lcg(rng) % 5) + 1;              // 1..5 trains
                rng = lcg(rng);
                for (j = 0; j < burst; j = j + 1) begin
                    do_train;
                    wexp = wexp + 256.0;  // fresh cofire reads 2^K = 256
                end
                if (ovf === 1'b1) begin
                    errors = errors + 1;
                    $display("FAIL ovf at event %0d (H=%0d)", i, H);
                end
                do_read(rw);
                rw_r  = rw;
                lo    = wexp / 2.0 - 1.0;
                hi    = wexp * 2.0 + 1.0;
                if (!(lo <= rw_r && rw_r <= hi)) begin
                    errors = errors + 1;
                    $display("FAIL envelope H=%0d ev=%0d t=%0d: W=%f band=[%f,%f] read=%0d",
                             H, i, t, wexp, lo, hi, rw);
                end
            end
            $display("  config H=%0d: %0d events, %0d reads checked, final W=%.2f read=%0d",
                     H, n_ev, n_ev, wexp, rw);
        end
    endtask

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);

        mode = 0; base = 0; p0e = 20;
        run_config(16, 400, 32'hB2F00001);
        run_config(64, 400, 32'hB2F00007);

        if (errors == 0)
            $display("TB-ENV-FUZZ PASS");
        else
            $display("TB-ENV-FUZZ FAIL %0d", errors);
        $finish;
    end
endmodule
