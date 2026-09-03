// tb_act_bias.v -- THE-BREAKDOWN B8 / error-envelopes.md §7 row 8:
// the act truncation bias (E2, Thm 5c) is PROVED, here it is MEASURED.
//
//   act_rtl(n) = act_ideal(n) - err(n),  err(n) = sum of floor losses
//   per effect: loss_e in {0,1} LSB (positive and negative dat both,
//   `>>>` is an arithmetic floor), so 0 <= err(N) <= N and the
//   zero-mean fluctuation model says err ~ N/2 ± sqrt(N)/2.
//
// Three checks per epoch:
//   A) RTL act == exact floor golden, bit-exact at every checkpoint
//      (validates the harness mirrors q_cell_core's arithmetic exactly;
//      the floor model is the RTL's own semantics, so this MUST hold).
//   B) err = ideal - floor measured against the Thm 5c envelope:
//      0 <= err <= N (hard bound) and |err - N/2| <= 3*sqrt(N)/2
//      (bias + fluctuation, 3-sigma practical band; printed, not just
//      asserted, so the measured bias is on the record).
//   C) threshold-shift companion: with THRESH placed strictly between
//      act_rtl and act_ideal at a checkpoint, count the extra effects
//      the RTL needs to reach it. Assert delay >= 0 (floor can only
//      delay) and delay <= (N/2 + sqrt(N)/2)/min_inc + 2 effects.
//
// Weight dynamics mirror tb_cell_core test 3 (and were re-probed): the
// effect TRAIN potentiates first (LTP +256), then the readback weight is
// integrated, so effect n carries w_n = base + 256*n (base = link a1);
// RQEN=0 keeps credit 0 (bit-exact v1); no ticks, so no leak, no decay,
// no fire during the streams.
`timescale 1ns/1ps
module tb_act_bias;
    reg clk = 0, rst_n = 0, s_tick = 0;
    always #5 clk = ~clk;

    reg         ri_valid = 0, ro_ready = 1;
    reg  [2:0]  ri_op = 0;
    reg  [3:0]  ri_src = 0, ri_dst = 0;
    reg  [15:0] ri_a0 = 0, ri_a1 = 0, ri_a2 = 0, ri_dat = 0;
    wire        ri_ready, ro_valid;
    wire [2:0]  ro_op;
    wire [3:0]  ro_src, ro_dst;
    wire [15:0] ro_a0, ro_a1, ro_a2, ro_dat;
    wire        ovf;

    integer errors = 0, guard;

    q_cell #(.EDGES_N(4)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_por_n(rst_n), .i_bdf_wr(1'b0), .i_bdf_addr(4'd0),
        .i_bdf_wdata(16'd0), .i_myid(4'd1), .s_tick(s_tick),
        .o_ovf(ovf),
        .ri_valid(ri_valid), .ri_ready(ri_ready),
        .ri_op(ri_op), .ri_src(ri_src), .ri_dst(ri_dst),
        .ri_a0(ri_a0), .ri_a1(ri_a1), .ri_a2(ri_a2), .ri_dat(ri_dat),
        .ro_valid(ro_valid), .ro_ready(ro_ready),
        .ro_op(ro_op), .ro_src(ro_src), .ro_dst(ro_dst),
        .ro_a0(ro_a0), .ro_a1(ro_a1), .ro_a2(ro_a2), .ro_dat(ro_dat)
    );

    // no saturation anywhere in these streams
    always @(negedge clk) if (ovf !== 1'b0 && rst_n) begin
        errors = errors + 1;
        $display("FAIL o_ovf pulsed");
    end

    task send(input [2:0] op, input [3:0] src,
              input [15:0] a0, input [15:0] a1,
              input [15:0] a2, input [15:0] dat);
        begin
            @(negedge clk);
            ri_valid = 1; ri_op = op; ri_src = src; ri_dst = 4'd1;
            ri_a0 = a0; ri_a1 = a1; ri_a2 = a2; ri_dat = dat;
            guard = 0;
            while (ri_ready !== 1'b1 && guard < 500) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 500) begin
                errors = errors + 1;
                $display("FAIL send_timeout op=%0d", op);
            end
            @(posedge clk);
            ri_valid <= 0;
        end
    endtask

    reg [15:0] rw;
    task view(input [1:0] sel, output [15:0] v);
        begin
            send(3'd3, 4'd9, {14'd0, sel}, 16'd0, 16'd0, 16'd0);
            @(negedge clk);
            guard = 0;
            while (ro_valid !== 1'b1 && guard < 2000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 2000) begin
                errors = errors + 1;
                $display("FAIL view sel=%0d TIMEOUT", sel);
            end
            v = ro_dat;
            @(negedge clk);
        end
    endtask

    // convergent (round-half-to-even) of signed p / 2^15, exact integer
    function integer conv_q15(input integer p);
        integer q, r;
        begin
            q = p >>> 15;               // arithmetic floor
            r = p - (q <<< 15);         // frac in [0, 2^15)
            if (r > 32'h4000) q = q + 1;
            else if (r == 32'h4000 && q[0]) q = q + 1;  // tie -> even
            conv_q15 = q;
        end
    endfunction

    integer n, nfx, w_g, p_g, act_floor, act_ideal, err;
    integer dat0, NEG;
    integer n_rtl, n_ideal_cross, T;
    real    sigma, delay_bound;
    reg [15:0] vr;

    // one epoch: fresh reset, bind, link, NFX effects with stride dat0
    // (NEG=1 -> dat = -dat0), checkpoints every 32 effects + final.
    // Returns nothing; checks A/B inline, prints measured err.
    task epoch(input integer nfx_, input integer dat0_, input integer neg_);
        integer k;
        begin
            nfx = nfx_; dat0 = dat0_; NEG = neg_;
            rst_n = 0; s_tick = 0;
            repeat (4) @(negedge clk);
            rst_n = 1;
            repeat (4) @(negedge clk);
            send(3'd0, 4'd9, 16'd1, 16'd0, 16'd0, 16'd0);   // bind id=1
            send(3'd1, 4'd2, 16'd0, 16'h1000, 16'd0, 16'd0); // link slot0 peer2
            act_floor  = 0;
            act_ideal  = 0;
            for (n = 1; n <= nfx; n = n + 1) begin
                w_g = 16'h1000 + n*256;             // post-train weight
                p_g = (NEG ? -dat0 : dat0) * w_g;   // exact: |p| < 2^23
                act_floor  = act_floor  + (p_g >>> 15);
                act_ideal  = act_ideal  + conv_q15(p_g);
                send(3'd2, 4'd2, 16'd0, 16'd0, 16'd0,
                     (NEG ? -dat0 : dat0));
                repeat (12) @(negedge clk);   // let the effect complete
                begin   // interleave a view per effect: the loss-free
                        // regime (see NOTE above); also strictest check
                    view(2'd0, vr);
                    if (vr !== act_floor[15:0]) begin
                        errors = errors + 1;
                        $display("FAIL floor-model n=%0d rtl=%h floor=%h",
                                 n, vr, act_floor[15:0]);
                    end
                end
            end
            view(2'd0, vr);
            err = act_ideal - $signed(vr);
            sigma = $sqrt(1.0 * nfx) / 2.0;
            $display("  epoch N=%0d dat=%0d: err=%0d  N/2=%0.1f  sigma=%0.2f  err/sigma=%0.2f",
                     nfx, NEG ? -dat0 : dat0, err, nfx/2.0, sigma,
                     (err - nfx/2.0)/sigma);
            // B1: hard Thm 5c bound 0 <= err <= N
            if (err < 0 || err > nfx) begin
                errors = errors + 1;
                $display("FAIL envelope bound err=%0d N=%0d", err, nfx);
            end
            // B2: bias+fluctuation practical band (3-sigma)
            if ((err - nfx/2.0) > 3.0*sigma || (nfx/2.0 - err) > 3.0*sigma) begin
                errors = errors + 1;
                $display("FAIL bias band err=%0d not within N/2 +/- 3sqrt(N)/2 (N=%0d)",
                         err, nfx);
            end
        end
    endtask

    initial begin
        $display("== TB-ACT-BIAS: act truncation bias measured (B8, Thm 5c) ==");

        // three regimes: positive dat, negative dat (signed floor), and
        // a different odd stride (different truncation phase profile)
        epoch(128, 65, 0);
        epoch(128, 65, 1);
        epoch(96, 321, 0);

        // C: threshold-shift companion on a fresh epoch.
        // Stream until ideal crosses T=12000 (record n_ideal), keep the
        // checkpoint floor/ideal pair, then stream until RTL reaches T
        // (record n_rtl). Assert 0 <= n_rtl - n_ideal <= bound.
        rst_n = 0; repeat (4) @(negedge clk);
        rst_n = 1; repeat (4) @(negedge clk);
        send(3'd0, 4'd9, 16'd1, 16'd0, 16'd0, 16'd0);
        send(3'd1, 4'd2, 16'd0, 16'h1000, 16'd0, 16'd0);
        act_floor = 0; act_ideal = 0;
        T = 12000;
        n_ideal_cross = 0; n_rtl = 0;
        for (n = 1; n <= 300 && n_rtl == 0; n = n + 1) begin
            w_g = 16'h1000 + n*256;
            p_g = 65 * w_g;
            act_floor = act_floor + (p_g >>> 15);
            act_ideal = act_ideal + conv_q15(p_g);
            send(3'd2, 4'd2, 16'd0, 16'd0, 16'd0, 16'd65);
            repeat (12) @(negedge clk);
            if (n_ideal_cross == 0 && act_ideal >= T) n_ideal_cross = n;
            view(2'd0, vr);
            if (vr !== act_floor[15:0]) begin
                errors = errors + 1;
                $display("FAIL floor-model(T) n=%0d", n);
            end
            if (n_rtl == 0 && $signed(vr) >= T) n_rtl = n;
        end
        if (n_ideal_cross == 0 || n_rtl == 0) begin
            errors = errors + 1;
            $display("FAIL threshold stream did not cross (ideal@%0d rtl@%0d)",
                     n_ideal_cross, n_rtl);
        end else begin
            // local per-effect increment at the crossing point (exact
            // from the same model): inc = w(ideal_cross)*65/2^15 floored
            delay_bound = (1.0*n_ideal_cross/2.0 + $sqrt(1.0*n_ideal_cross)/2.0)
                          / ((65.0*(16'h1000 + n_ideal_cross*256))/32768.0) + 2.0;
            $display("  threshold shift: ideal crossed T at n=%0d, RTL at n=%0d (delay %0d, bound %0.1f)",
                     n_ideal_cross, n_rtl, n_rtl - n_ideal_cross, delay_bound);
            if (n_rtl < n_ideal_cross) begin
                errors = errors + 1;
                $display("FAIL RTL crossed before ideal -- bias direction inverted");
            end
            if (n_rtl - n_ideal_cross > delay_bound) begin
                errors = errors + 1;
                $display("FAIL threshold delay %0d exceeds envelope bound",
                         n_rtl - n_ideal_cross);
            end
        end

        if (errors == 0) $display("TB-ACT-BIAS PASS");
        else $display("TB-ACT-BIAS FAIL %0d", errors);
        $finish;
    end
endmodule
