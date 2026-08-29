// tb_hyperbola_tail.v -- hyperbolic-decay TAIL validation; closes the two
// hyperbola gaps named in error-envelopes.md 7 (honest ledger rows 2 and 3).
//
//  TA  Theorem 2a interval band, full formula sweep: for P0 in {2^1..2^15}
//      and W in [1,255], assert the corrected band
//          P0/W^2 <= Delta(W)                 (always)
//          Delta(W) < 4*P0/W^2                (when W^2 < 4*P0)
//          Delta(W) = 1                       (allowed when W^2 >= 4*P0)
//      and take a census of violations of the theorem AS WRITTEN (the strict
//      half-open band with no floor caveat). FINDING: the as-written band
//      fails for every W >= 2*sqrt(P0) -- the tick-granularity floor forces
//      Delta = 1 >= 4*P0/W^2 there. The doc's parenthetical "the floor-1
//      rule only tightens the lower edge at W=1" is wrong and is corrected.
//  TB  DUT-driven cadence, small cases W0 in {1,2,3} x P0 in {2,4,8} (the
//      ledger's named corner): per-level crossing times measured from the
//      engine; per-level interval bit-exact vs the mirror formula
//      max(1, P0 >> 2*msb(L)); tau_0 (time to W=0) bit-exact vs the level
//      sum; every observed interval inside the corrected band.
//  TC  Theorem 2b trajectory envelope: every config above plus the big one
//      (W0=100, P0=4096) driven past the W=1 plateau into the tail,
//      t <= 2*tau_0, checked at EVERY tick:
//          W_true(P0;t) - 1 <= W_rtl(t) <= W_true(4*P0;t) + 1
//      No-slack counters are the witnesses that the +1 slack is necessary on
//      BOTH sides (the doc claims only the lower bound needs it; the small
//      cases falsify that: between crossings the staircase holds a level
//      while the slow curve falls below it).
`timescale 1ns/1ps
module tb_hyperbola_tail;
    reg clk = 0, rst_n = 0;
    always #5 clk <= ~clk;

    reg        sel  = 1;
    reg  [2:0] cmd  = 0;
    reg        mode = 1;
    reg [15:0] base = 0, hl = 64;
    reg  [4:0] p0e  = 12;
    wire       done;
    wire [15:0] w;
    wire        ovf;

    integer errors = 0;
    integer guard;

    q_hebb_edge u_dut (
        .clk(clk), .rst_n(rst_n), .i_sel(sel), .i_cmd(cmd),
        .i_mode(mode), .i_base(base), .i_hl(hl), .i_p0e(p0e),
        .i_gclass(4'd0),
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
            while (done !== 1'b1 && guard < 200) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 200) begin
                errors = errors + 1;
                $display("FAIL read_timeout");
                rw = 16'hxxxx;
            end else begin
                rw = w;
                @(negedge clk);
            end
        end
    endtask

    // ---- Theorem 2a mirror: Delta(W) = max(1, P0 >> 2*msb(W)) ----
    function integer msb_of;
        input integer v;
        integer j;
        begin
            msb_of = 0;
            for (j = 0; j < 16; j = j + 1)
                if (((v >> j) & 1) == 1) msb_of = j;
        end
    endfunction

    function integer delta_of;
        input integer vv;
        input integer ee;
        integer iv;
        begin
            iv = (1 << ee) >> (2 * msb_of(vv));
            delta_of = (iv == 0) ? 1 : iv;
        end
    endfunction

    // ---- shared state ----
    integer leave [0:256];        // leave[L] = tick at which W first reads L-1
    integer wlo_no_slack;         // witness count: W_rtl < W_true(P0)
    integer whi_no_slack;         // witness count: W_rtl > W_true(4P0)
    real    p0r, glo, ghi, lox, hix, dvr;
    integer t, lvl, wl, wprev, tmax, tau0f, tau0m, dv;
    integer goti;
    reg [15:0] rw;

    task run_cfg;
        input integer w0;
        input integer ee;
        begin
            rst_n = 0; p0e = ee[4:0];
            repeat (2) @(negedge clk);
            rst_n = 1;
            repeat (2) @(negedge clk);
            for (lvl = 0; lvl < 256; lvl = lvl + 1) leave[lvl] = -1;
            for (lvl = 0; lvl < w0; lvl = lvl + 1) do_train;
            do_read(rw);
            goti = {16'd0, rw};
            if (goti !== w0 * 256) begin
                errors = errors + 1;
                $display("FAIL TB read-after-train w0=%0d got=%0d", w0, goti);
            end
            tau0f = 0;
            for (lvl = 1; lvl <= w0; lvl = lvl + 1)
                tau0f = tau0f + delta_of(lvl, ee);
            p0r   = (1 << ee) * 1.0;
            wprev = w0;
            leave[w0 + 1] = 0;   // top level entered at t=0 (dv base)
            tmax  = 2 * tau0f + 8;
            for (t = 1; t <= tmax; t = t + 1) begin
                do_tick;
                do_read(rw);
                wl = {24'd0, rw[15:8]};
                glo = w0 * 1.0 / (1.0 + w0 * 1.0 * t / p0r);
                ghi = w0 * 1.0 / (1.0 + w0 * 1.0 * t / (4.0 * p0r));
                if (!(glo - 1.0 <= wl && wl <= ghi + 1.0)) begin
                    errors = errors + 1;
                    $display("FAIL TC env w0=%0d P0=%0d t=%0d rtl=%0d lo=%f hi=%f",
                             w0, 1 << ee, t, wl, glo, ghi);
                end
                if (wl < glo) wlo_no_slack = wlo_no_slack + 1;
                if (wl > ghi) whi_no_slack = whi_no_slack + 1;
                if (wl != wprev) begin
                    if (wl == wprev - 1) begin
                        leave[wprev] = t;
                    end else begin
                        errors = errors + 1;
                        $display("FAIL TB multi-drop w0=%0d t=%0d %0d->%0d",
                                 w0, t, wprev, wl);
                    end
                    wprev = wl;
                end
            end
            // per-level cadence + corrected interval band
            for (lvl = 1; lvl <= w0; lvl = lvl + 1) begin
                if (leave[lvl] < 0) begin
                    errors = errors + 1;
                    $display("FAIL TB level %0d never left (w0=%0d ee=%0d)",
                             lvl, w0, ee);
                end else begin
                    dv = leave[lvl] - leave[lvl + 1];
                    if (dv != delta_of(lvl, ee)) begin
                        errors = errors + 1;
                        $display("FAIL TB cad lvl=%0d got=%0d exp=%0d (ee=%0d)",
                                 lvl, dv, delta_of(lvl, ee), ee);
                    end
                    lox = p0r / (lvl * 1.0 * lvl);
                    hix = 4.0 * lox;
                    dvr = dv * 1.0;
                    if (dvr < lox - 1.0e-9) begin
                        errors = errors + 1;
                        $display("FAIL TB band-lo lvl=%0d dv=%0d lo=%f", lvl, dv, lox);
                    end
                    if (lvl * lvl < 4 * (1 << ee)) begin
                        if (dvr >= hix - 1.0e-9) begin
                            errors = errors + 1;
                            $display("FAIL TB band-hi lvl=%0d dv=%0d hi=%f", lvl, dv, hix);
                        end
                    end else begin
                        if (dv != 1) begin
                            errors = errors + 1;
                            $display("FAIL TB band-floor lvl=%0d dv=%0d", lvl, dv);
                        end
                    end
                end
            end
            tau0m = leave[1];
            if (tau0m != tau0f) begin
                errors = errors + 1;
                $display("FAIL TB tau0 w0=%0d got=%0d exp=%0d", w0, tau0m, tau0f);
            end
            if (ovf !== 1'b0) begin
                errors = errors + 1;
                $display("FAIL TB o_ovf w0=%0d", w0);
            end
            $display("  cfg W0=%0d P0=%0d tau0=%0d ticks, tail checked to t=%0d",
                     w0, 1 << ee, tau0m, tmax);
        end
    endtask

    // TA sweep state
    integer e_sweep, w_sweep, viol_written, viol_lo;

    integer ww0, ee0;

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);

        // ---------------- TA: interval-band formula sweep ----------------
        viol_written = 0;
        viol_lo = 0;
        for (e_sweep = 1; e_sweep <= 15; e_sweep = e_sweep + 1) begin
            for (w_sweep = 1; w_sweep <= 255; w_sweep = w_sweep + 1) begin
                dv  = delta_of(w_sweep, e_sweep);
                lox = (1 << e_sweep) * 1.0 / (w_sweep * 1.0 * w_sweep);
                hix = 4.0 * lox;
                dvr = dv * 1.0;
                if (dvr < lox - 1.0e-9) begin
                    viol_lo = viol_lo + 1;
                    errors  = errors + 1;
                    if (viol_lo <= 5)
                        $display("FAIL TA lower e=%0d W=%0d dv=%0d lo=%f",
                                 e_sweep, w_sweep, dv, lox);
                end
                if (w_sweep * w_sweep < 4 * (1 << e_sweep)) begin
                    if (dvr >= hix - 1.0e-9) begin
                        errors = errors + 1;
                        $display("FAIL TA upper(unfloored) e=%0d W=%0d dv=%0d hi=%f",
                                 e_sweep, w_sweep, dv, hix);
                    end
                end else begin
                    if (dv != 1) begin
                        errors = errors + 1;
                        $display("FAIL TA floor e=%0d W=%0d dv=%0d", e_sweep, w_sweep, dv);
                    end
                    // census vs the theorem AS WRITTEN (strict half-open band)
                    if (dvr * (w_sweep * 1.0 * w_sweep) >= 4.0 * (1 << e_sweep) - 0.5)
                        viol_written = viol_written + 1;
                end
            end
        end
        if (viol_lo != 0) begin
            errors = errors + 1;
            $display("FAIL TA lower-edge violations: %0d", viol_lo);
        end
        if (viol_written == 0) begin
            errors = errors + 1;
            $display("FAIL TA expected as-written violations, found none");
        end
        $display("TA: corrected interval band holds on all 3825 (P0,W) pairs");
        $display("FINDING TA: Theorem 2a AS WRITTEN (Delta < 4*P0/W^2, no floor");
        $display("  caveat) FAILS at %0d of 3825 pairs -- every W >= 2*sqrt(P0),",
                 viol_written);
        $display("  where the tick floor forces Delta=1 >= 4*P0/W^2. The doc's");
        $display("  'floor-1 rule only tightens the lower edge at W=1' is wrong.");

        // ---------------- TB+TC: small corner + big tail ----------------
        wlo_no_slack = 0;
        whi_no_slack = 0;
        for (ww0 = 1; ww0 <= 3; ww0 = ww0 + 1)
            for (ee0 = 1; ee0 <= 3; ee0 = ee0 + 1)
                run_cfg(ww0, ee0);
        run_cfg(100, 12);

        if (wlo_no_slack == 0) begin
            errors = errors + 1;
            $display("FAIL TC expected lower no-slack witnesses, found none");
        end
        if (whi_no_slack == 0) begin
            errors = errors + 1;
            $display("FAIL TC expected upper no-slack witnesses, found none");
        end
        $display("TC: +-1 envelope held at every tick of every config;");
        $display("FINDING TC: no-slack witnesses: lower %0d ticks (W_rtl < W_true(P0)),",
                 wlo_no_slack);
        $display("  upper %0d ticks (W_rtl > W_true(4P0)) -- the +1 slack is necessary",
                 whi_no_slack);
        $display("  on BOTH sides; 'upper bound exact' holds only at crossings.");

        if (errors == 0) $display("TB_HYPERBOLA_TAIL PASS");
        else             $display("TB_HYPERBOLA_TAIL FAIL %0d", errors);
        $finish;
    end
endmodule
