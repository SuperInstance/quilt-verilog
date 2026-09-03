// tb_q_tern_dice.v -- ternary dice (LCG noise unit) tests, house method:
// bit-exact integer golden (64-bit LCG model) + statistical envelopes;
// pass = zero errors.
`timescale 1ns/1ps
module tb_q_tern_dice;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg          tick = 0, seed_wr = 0;
    reg  [15:0]  seed = 16'd0;
    reg          en = 0;
    reg  [14:0]  band_neg = 15'd10923, band_pos = 15'd10923;
    wire signed [1:0] bias;
    wire [30:0]  state;

    integer errors = 0;

    q_tern_dice u_dut (
        .clk(clk), .rst_n(rst_n),
        .i_tick(tick), .i_seed_wr(seed_wr), .i_seed(seed),
        .i_en(en), .i_band_neg(band_neg), .i_band_pos(band_pos),
        .o_bias(bias), .o_state(state)
    );

    task pulse_tick; begin
        @(negedge clk); tick = 1;
        @(negedge clk); tick = 0;
    end endtask

    task write_seed(input [15:0] s); begin
        @(negedge clk); seed = s; seed_wr = 1;
        @(negedge clk); seed_wr = 0;
    end endtask

    task reset_dut; begin
        rst_n = 0; repeat (2) @(negedge clk); rst_n = 1;
        repeat (2) @(negedge clk);
    end endtask

    // ---------------- golden model (64-bit, mod 2^31 by mask) ------------
    reg [63:0] xg;

    task gold_seed(input integer s); begin
        xg = s & 64'h7FFFFFFF;
    end endtask

    task gold_tick; begin
        xg = (xg * 64'd1103515245 + 64'd12345) & 64'h7FFFFFFF;
    end endtask

    // golden bucket with the DUT's documented overlap priority (neg first)
    function [1:0] gold_bias;
        input [14:0] bn, bp;
        reg [14:0] dr;
        reg [15:0] plo;
        begin
            dr  = (xg >> 16) & 15'h7FFF;   // draw from the NEW state
            plo = 16'd32768 - {1'b0, bp};
            if (dr < bn)                 gold_bias = 2'b11;  // -1
            else if ({1'b0, dr} >= plo)  gold_bias = 2'b01;  // +1
            else                         gold_bias = 2'b00;
        end
    endfunction

    task chk_bias(input [1:0] exp, input [127:0] name);
        begin
            if (bias !== exp) begin
                errors = errors + 1;
                $display("FAIL %0s got=%b exp=%b", name, bias, exp);
            end
        end
    endtask

    integer n;
    integer cnt_neg, cnt_zero, cnt_pos;
    reg [63:0] sig_a, sig_b;

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);

        // ---- T0: reset -> state 0, bias 0 ----
        chk_bias(2'b00, "T0_bias");
        if (state !== 31'd0) begin
            errors = errors + 1;
            $display("FAIL T0_state got=%h", state);
        end

        // ---- T1: disabled (en=0): bias pinned 0, stream still advances --
        gold_seed(0);
        for (n = 0; n < 64; n = n + 1) begin
            pulse_tick;
            gold_tick;
            @(negedge clk);
            chk_bias(2'b00, "T1_bias_off");
            if (state !== xg[30:0]) begin
                errors = errors + 1;
                $display("FAIL T1_state n=%0d got=%h exp=%h",
                         n, state, xg[30:0]);
            end
        end

        // ---- T2: enabled, balanced bands: bit-exact bias, 2000 ticks ----
        reset_dut;
        write_seed(16'd42); gold_seed(42);
        en = 1; band_neg = 15'd10923; band_pos = 15'd10923;
        chk_bias(2'b00, "T2_seed_clears_bias");
        for (n = 0; n < 2000; n = n + 1) begin
            pulse_tick;
            gold_tick;
            @(negedge clk);
            chk_bias(gold_bias(band_neg, band_pos), "T2_bias");
            if (state !== xg[30:0]) begin
                errors = errors + 1;
                $display("FAIL T2_state n=%0d got=%h exp=%h",
                         n, state, xg[30:0]);
            end
        end

        // ---- T3: balance statistics, 100k ticks, ~1/3 each +- 1.5% ----
        cnt_neg = 0; cnt_zero = 0; cnt_pos = 0;
        for (n = 0; n < 100000; n = n + 1) begin
            pulse_tick;
            @(negedge clk);
            case (bias)
                2'b11:   cnt_neg  = cnt_neg + 1;
                2'b01:   cnt_pos  = cnt_pos + 1;
                default: cnt_zero = cnt_zero + 1;
            endcase
        end
        $display("T3 counts: neg=%0d zero=%0d pos=%0d (exp ~33333 each)",
                 cnt_neg, cnt_zero, cnt_pos);
        if (cnt_neg  < 31833 || cnt_neg  > 34833 ||
            cnt_zero < 31833 || cnt_zero > 34833 ||
            cnt_pos  < 31833 || cnt_pos  > 34833) begin
            errors = errors + 1;
            $display("FAIL T3_balance");
        end

        // ---- T4: reseed determinism: same seed -> same stream ----
        reset_dut;
        write_seed(16'd1234);
        sig_a = 0;
        for (n = 0; n < 300; n = n + 1) begin
            pulse_tick; @(negedge clk);
            sig_a = (sig_a << 2) | {62'd0, bias};
        end
        write_seed(16'd1234);
        sig_b = 0;
        for (n = 0; n < 300; n = n + 1) begin
            pulse_tick; @(negedge clk);
            sig_b = (sig_b << 2) | {62'd0, bias};
        end
        if (sig_a !== sig_b) begin
            errors = errors + 1;
            $display("FAIL T4_reseed a=%h b=%h", sig_a, sig_b);
        end
        // different seed -> different stream (300 draws make a collision
        // negligible; this pins per-cell seeding to actually matter)
        write_seed(16'd1235);
        sig_b = 0;
        for (n = 0; n < 300; n = n + 1) begin
            pulse_tick; @(negedge clk);
            sig_b = (sig_b << 2) | {62'd0, bias};
        end
        if (sig_a === sig_b) begin
            errors = errors + 1;
            $display("FAIL T4_seed_matters");
        end

        // ---- T5: extreme bands ----
        // both zero: never fires a bias
        reset_dut; write_seed(16'd7);
        en = 1; band_neg = 15'd0; band_pos = 15'd0;
        for (n = 0; n < 256; n = n + 1) begin
            pulse_tick; @(negedge clk);
            chk_bias(2'b00, "T5_zero_bands");
        end
        // full negative band: -1 unless draw == 32767 (p = 1/32768)
        band_neg = 15'd32767; band_pos = 15'd0;
        cnt_neg = 0;
        for (n = 0; n < 4096; n = n + 1) begin
            pulse_tick; @(negedge clk);
            if (bias === 2'b11) cnt_neg = cnt_neg + 1;
        end
        if (cnt_neg < 4094) begin
            errors = errors + 1;
            $display("FAIL T5_full_neg cnt=%0d (exp >= 4094)", cnt_neg);
        end
        // full positive band: +1 unless draw == 32767
        band_neg = 15'd0; band_pos = 15'd32767;
        cnt_pos = 0;
        for (n = 0; n < 4096; n = n + 1) begin
            pulse_tick; @(negedge clk);
            if (bias === 2'b01) cnt_pos = cnt_pos + 1;
        end
        if (cnt_pos < 4094) begin
            errors = errors + 1;
            $display("FAIL T5_full_pos cnt=%0d (exp >= 4094)", cnt_pos);
        end

        // ---- T6: overlapping bands -> negative wins (documented) ----
        reset_dut; write_seed(16'd99);
        en = 1; band_neg = 15'd20000; band_pos = 15'd20000;
        gold_seed(99);
        for (n = 0; n < 2000; n = n + 1) begin
            pulse_tick;
            gold_tick;
            @(negedge clk);
            chk_bias(gold_bias(band_neg, band_pos), "T6_overlap");
        end

        // ---- T7: disable mid-run -> bias 0, stream position kept ----
        en = 0;
        pulse_tick; gold_tick; @(negedge clk);
        chk_bias(2'b00, "T7_off_bias");
        if (state !== xg[30:0]) begin
            errors = errors + 1;
            $display("FAIL T7_off_state got=%h exp=%h", state, xg[30:0]);
        end
        en = 1;   // re-enable: the NEXT draw uses the kept stream position
        band_neg = 15'd10923; band_pos = 15'd10923;
        pulse_tick; gold_tick; @(negedge clk);
        chk_bias(gold_bias(band_neg, band_pos), "T7_resume");

        if (errors == 0)
            $display("TB_Q_TERN_DICE PASS");
        else
            $display("TB_Q_TERN_DICE FAIL %0d", errors);
        $finish;
    end

    initial begin
        #500_000_000;
        $display("TB_Q_TERN_DICE FAIL watchdog");
        $finish;
    end
endmodule
