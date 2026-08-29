// tb_rqh_saturation.v -- RQH residue banking at the saturation boundaries;
// closes honest-ledger rows 4 and 5 (error-envelopes.md 7, Theorem 3).
//
//  S0  Deposit math, bit-exact, both schemes: corrected table for g in 0..7
//      equals round(2^(K+QDW-g)*(1 - 1/(2 ln 2))) to within the 16-bit dyadic
//      staging (<= 8 quanta), is strictly decreasing in g, and as-built 2^g
//      is below it for EVERY class (crossing at g ~= 7.08: 128 vs 143) --
//      the class dependence of the as-built deposit is inverted. Shortfall
//      census: at class 0 the as-built deposit is ~18,262x too small (the
//      doc's "~9,100x" is an arithmetic slip in its own formula
//      2^(K+QDW)*0.27865 = 2^16*0.27865; same conclusion, honest number).
//  S1  Disabled A/B (RQEN=0): credit and antic stay 0 (bit-exact v1 arm).
//  S2  Saturation flood, corrected: R pegs at 65535 after 4 deposits, never
//      wraps, credit = 255, o_antic count == credit-increment count == 4.
//      S2b, as-built class 7: saturates after 512 deposits, telemetry
//      integrity holds (antic count == credit rises == 255).
//  S3  Deadband leak: per-tick golden R <= 2^QLEAK snap (the flash sketch's
//      "snap at <= 1" leaves a sticky floor at R in [2, 2^QLEAK]; this
//      module snaps when the leak can no longer reduce R -- validated here:
//      reservoir reaches exactly 0).
//  S4  Envelope tightening under the CORRECTED deposit (Thm 3c/3b, honest
//      form): stationary stream, one class-0 cofire per half-life (HL=32),
//      read every 4 ticks after a 16-half-life warmup, golden W from the
//      event list with retirement at the engine's bucket horizon.
//        mis-phased stream (trains at phase 31: the +1-class regime, the
//        one place a positive credit genuinely reduces error):
//          qleak 4/5/6 -> mean|err| strictly BELOW engine-alone (tightening
//          occurs under the corrected scheme), qleak 8 -> reservoir
//          saturates every deposit cycle, over-credits ~3.4x the centering
//          level and the tightening is destroyed (worse than qleak 5);
//          the leak dial is the other half of the convergence condition.
//          as-built 2^g -> credit literally 0 for the whole run (18,262x
//          too small made visible), error identical to engine-alone.
//        aligned stream (trains at phase 0): credit WIDENS the mean error
//          (Theorem 3b: a non-negative credit cannot tighten the aligned
//          band) -- asserted, the honest negative result.
//      Preservation asserted at every sample: W/2-1 <= What <= 2W+1 and
//      W/2-1 <= What+C <= 2W+1+C, C <= 255 (Thm 3a/3b).
`timescale 1ns/1ps
module tb_rqh_saturation;
    reg clk = 0, rst_n = 0;
    always #5 clk <= ~clk;

    // engine side (ladder MODE=0)
    reg        sel = 1, mode = 0;
    reg  [2:0] cmd = 0;
    reg [15:0] base = 0, hl = 32;
    reg  [4:0] p0e = 12;
    wire        done;
    wire [15:0] weng;
    wire        ovf;

    // rqh side
    reg  trq = 0, tiq = 0, enb = 1, corr = 1;
    reg  [3:0] gcls = 0, qdw = 8, qlk = 5;
    wire [15:0] credit;
    wire        antic, satp;
    wire [15:0] rprobe;

    integer errors = 0;
    integer guard;

    q_hebb_edge u_eng (
        .clk(clk), .rst_n(rst_n), .i_sel(sel), .i_cmd(cmd),
        .i_mode(mode), .i_base(base), .i_hl(hl), .i_p0e(p0e),
        .i_gclass(4'd0),
        .o_done(done), .o_w(weng), .o_ovf(ovf)
    );

    q_hebb_rqh u_rqh (
        .clk(clk), .rst_n(rst_n),
        .i_train(trq), .i_tick(tiq), .i_gclass(gcls),
        .i_qdw(qdw), .i_qleak(qlk), .i_corr(corr), .i_en(enb),
        .o_credit(credit), .o_antic(antic), .o_sat(satp), .o_r(rprobe)
    );

    task pulse2(input [2:0] c, input rqs, input iqs);
        begin
            @(negedge clk); cmd = c; trq = rqs; tiq = iqs;
            @(negedge clk); cmd = 0; trq = 0;   tiq = 0;
        end
    endtask

    task do_train_s(output integer a, output integer s);
        begin
            @(negedge clk); cmd = 3'b001; trq = 1;
            @(negedge clk); cmd = 0; trq = 0;   // deposit edge just happened;
            a = {31'd0, antic}; s = {31'd0, satp};        // pulses still up
            @(negedge clk);
        end
    endtask

    task do_tick2;  begin pulse2(3'b010, 1'b0, 1'b1); @(negedge clk); end endtask

    task do_read2(output [15:0] rw);
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
                rw = weng;
                @(negedge clk);
            end
        end
    endtask

    // corrected-deposit golden table (what the RTL's dyadic staging must hit)
    integer dtc [0:7];
    integer g, ri, expv, antic_cnt, cred_rises, sat_cnt, cred_prev, cred_now;
    integer antic_s, sat_s;
    real    rf, ratio0;
    reg     failed;
    integer leak_l;

    initial begin
        dtc[0] = 18260; dtc[1] = 9130; dtc[2] = 4565; dtc[3] = 2283;
        dtc[4] = 1141;  dtc[5] = 571;  dtc[6] = 285;  dtc[7] = 143;
    end

    // ---------------- S4 stream machinery ----------------
    integer tickcnt, nev, st;
    integer tev [0:255];
    real    wsum, d1, d2;
    integer ai, dage, whati, credi, retage;
    real    seng, srqh, meane, meanr;
    integer nsamp, maxc;
    integer s4_fail;
    reg [15:0] rw;

    task step_to;
        input integer upto;
        input integer tphase;
        begin
            while (tickcnt < upto) begin
                if ((tickcnt % 32) == tphase) begin
                    tev[nev] = tickcnt;
                    nev = nev + 1;
                    do_train_s(antic_s, sat_s);
                end
                do_tick2;
                tickcnt = tickcnt + 1;
            end
        end
    endtask

    task sample;
        input integer tphase;
        begin
            do_read2(rw);
            whati = {16'd0, rw};
            credi = {16'd0, credit};
            // golden true kernel: events retire at age 256 - phase (the
            // mis-phased event is shifted out one tick after age 224)
            retage = 256 - tphase;
            wsum = 0.0;
            for (ai = 0; ai < nev; ai = ai + 1) begin
                dage = tickcnt - tev[ai];
                if (dage >= 0 && dage < retage)
                    wsum = wsum + 256.0 * (2.0 ** (-dage / 32.0));
            end
            // anchors: buckets hold exactly one event each. Mis-phased:
            // C0 empty at every sampled phase (trains at 31 land inside the
            // previous chunk). Aligned: phase-0 samples read the PRE-train
            // instant (the on-grid exact point, What == W == 254); phases
            // 4..28 read one fresh event in C0 (What == 510).
            if (tphase != 0) begin
                if (whati != 254) begin
                    s4_fail = s4_fail + 1;
                    $display("FAIL S4 anchor mis t=%0d What=%0d", tickcnt, whati);
                end
            end else begin
                if ((tickcnt % 32) == 0) begin
                    if (whati != 254) begin
                        s4_fail = s4_fail + 1;
                        $display("FAIL S4 anchor ali0 t=%0d What=%0d", tickcnt, whati);
                    end
                end else begin
                    if (whati != 510) begin
                        s4_fail = s4_fail + 1;
                        $display("FAIL S4 anchor ali t=%0d What=%0d", tickcnt, whati);
                    end
                end
            end
            // preservation (Thm 1 band; Thm 3b widened band with credit)
            if (!(wsum * 0.5 - 1.0 <= whati * 1.0 && whati * 1.0 <= 2.0 * wsum + 1.0)) begin
                s4_fail = s4_fail + 1;
                $display("FAIL S4 preserve eng t=%0d W=%f What=%0d", tickcnt, wsum, whati);
            end
            if (!(wsum * 0.5 - 1.0 <= whati * 1.0 + credi
                  && whati * 1.0 + credi <= 2.0 * wsum + 1.0 + credi)) begin
                s4_fail = s4_fail + 1;
                $display("FAIL S4 preserve rqh t=%0d W=%f What+C=%0d", tickcnt, wsum, whati + credi);
            end
            if (credi > 255) begin
                s4_fail = s4_fail + 1;
                $display("FAIL S4 credit cap t=%0d C=%0d", tickcnt, credi);
            end
            if (credi > maxc) maxc = credi;
            // accumulate
            d1 = whati * 1.0 - wsum;
            if (d1 < 0.0) d1 = -d1;
            d2 = whati * 1.0 + credi - wsum;
            if (d2 < 0.0) d2 = -d2;
            seng = seng + d1;
            srqh = srqh + d2;
            nsamp = nsamp + 1;
        end
    endtask

    // run one (phase, scheme, leak) config; results via mr_arr/me_arr/mc_arr
    real    me_arr [0:5];
    real    mr_arr [0:5];
    integer mc_arr [0:5];
    integer run_idx;
    real    seng_ref_mis, seng_ref_ali;

    task run_stream;
        input integer tphase;
        input integer usecorr;
        input integer ql;
        begin
            rst_n = 0; mode = 0; hl = 32; base = 0;
            corr = (usecorr != 0); qlk = ql[3:0]; qdw = 8; gcls = 0; enb = 1;
            repeat (2) @(negedge clk);
            rst_n = 1;
            repeat (2) @(negedge clk);
            tickcnt = 0; nev = 0;
            seng = 0.0; srqh = 0.0; nsamp = 0; maxc = 0; s4_fail = 0;
            step_to(512, tphase);
            for (st = 512; st < 1536; st = st + 4) begin
                step_to(st, tphase);
                sample(tphase);
            end
            meane = seng / nsamp;
            meanr = srqh / nsamp;
            me_arr[run_idx] = meane;
            mr_arr[run_idx] = meanr;
            mc_arr[run_idx] = maxc;
            if (tphase != 0) begin
                if (seng_ref_mis < 0.0) seng_ref_mis = seng;
                else if (seng != seng_ref_mis) begin
                    errors = errors + 1;
                    $display("FAIL S4 determinism mis ql=%0d", ql);
                end
            end else begin
                if (seng_ref_ali < 0.0) seng_ref_ali = seng;
                else if (seng != seng_ref_ali) begin
                    errors = errors + 1;
                    $display("FAIL S4 determinism ali ql=%0d", ql);
                end
            end
            if (s4_fail != 0) errors = errors + s4_fail;
            $display("  S4 run %0d %-8s qleak=%0d  mean|What-W|=%f  mean|What+C-W|=%f  maxC=%0d",
                     run_idx, (tphase != 0) ? "misphased" : "aligned",
                     ql, meane, meanr, maxc);
            run_idx = run_idx + 1;
        end
    endtask

    integer i;

    initial begin
        seng_ref_mis = -1.0;
        seng_ref_ali = -1.0;
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);

        // ---------------- S0: deposit math ----------------
        for (g = 0; g < 8; g = g + 1) begin
            // as-built
            corr = 0; gcls = g[3:0]; enb = 1;
            rst_n = 0; repeat (1) @(negedge clk); rst_n = 1; repeat (1) @(negedge clk);
            do_train_s(antic_s, sat_s);
            ri = {16'd0, rprobe};
            expv = 1 << g;
            if (ri != expv) begin
                errors = errors + 1;
                $display("FAIL S0 asbuilt g=%0d R=%0d exp=%0d", g, ri, expv);
            end
            // corrected
            corr = 1;
            rst_n = 0; repeat (1) @(negedge clk); rst_n = 1; repeat (1) @(negedge clk);
            do_train_s(antic_s, sat_s);
            ri = {16'd0, rprobe};
            if (ri != dtc[g]) begin
                errors = errors + 1;
                $display("FAIL S0 corr g=%0d R=%0d exp=%0d", g, ri, dtc[g]);
            end
            rf = (2.0 ** (16 - g)) * 0.2786524795555173;
            if (rf - dtc[g] > 8.0 || dtc[g] - rf > 8.0) begin
                errors = errors + 1;
                $display("FAIL S0 real-formula g=%0d dep=%0d exact=%f", g, dtc[g], rf);
            end
        end
        // class-dependence inversion + crossing point
        for (g = 0; g < 7; g = g + 1)
            if (dtc[g + 1] >= dtc[g]) begin
                errors = errors + 1;
                $display("FAIL S0 monotone g=%0d", g);
            end
        if ((1 << 7) >= dtc[7]) begin
            errors = errors + 1;
            $display("FAIL S0 crossing: as-built must stay below corrected");
        end
        ratio0 = (2.0 ** 16) * 0.2786524795555173;
        if (!(ratio0 > 15000.0 && ratio0 < 22000.0)) begin
            errors = errors + 1;
            $display("FAIL S0 class-0 ratio %f", ratio0);
        end
        $display("S0: deposit tables bit-exact; corrected strictly decreasing;");
        $display("FINDING S0: as-built 2^g vs corrected at class 0: 1 vs %0d quanta",
                 dtc[0]);
        $display("  = %0.0fx too small (doc says ~9,100x; its own formula gives", ratio0);
        $display("  2^16*0.2786525 = 18,262x (doc used 2^15 -- slip), same conclusion);");
        $display("  crossing at g~=7.08 (as-built 128 < corrected 143 at g=7).");

        // ---------------- S1: disabled A/B ----------------
        corr = 1; gcls = 0; enb = 0;
        rst_n = 0; repeat (1) @(negedge clk); rst_n = 1; repeat (1) @(negedge clk);
        failed = 0;
        for (i = 0; i < 40; i = i + 1) begin
            if (i % 3 == 0) do_train_s(antic_s, sat_s); else do_tick2;
            if (credit != 16'd0 || antic !== 1'b0) failed = 1;
        end
        if (failed) begin
            errors = errors + 1;
            $display("FAIL S1 disabled arm leaked a credit/antic");
        end else
            $display("S1: RQEN=0 arm bit-exact (credit=0, antic=0 through 40 ops)");

        // ---------------- S2: saturation flood, corrected ----------------
        enb = 1; corr = 1; gcls = 0;
        rst_n = 0; repeat (1) @(negedge clk); rst_n = 1; repeat (1) @(negedge clk);
        antic_cnt = 0; cred_rises = 0; sat_cnt = 0; cred_prev = 0;
        for (i = 0; i < 8; i = i + 1) begin
            do_train_s(antic_s, sat_s);
            cred_now = {16'd0, credit};
            if (cred_now > cred_prev) cred_rises = cred_rises + 1;
            cred_prev = cred_now;
            if (antic_s != 0) antic_cnt = antic_cnt + 1;
            if (sat_s != 0) sat_cnt = sat_cnt + 1;
        end
        ri = {16'd0, rprobe};
        if (ri != 65535 || cred_now != 255 || cred_rises != 4
            || antic_cnt != 4 || sat_cnt != 5) begin
            errors = errors + 1;
            $display("FAIL S2 flood R=%0d C=%0d rises=%0d antic=%0d sat=%0d",
                     ri, cred_now, cred_rises, antic_cnt, sat_cnt);
        end else
            $display("S2: corrected flood saturates at 4th deposit, R pegs 65535,");
        $display("    credit 255, no wrap, antic(4)==rises(4), sat pulses 5-8th");

        // ---------------- S2b: saturation flood, as-built g=7 ----------------
        corr = 0; gcls = 7;
        rst_n = 0; repeat (1) @(negedge clk); rst_n = 1; repeat (1) @(negedge clk);
        antic_cnt = 0; cred_rises = 0; sat_cnt = 0; cred_prev = 0;
        for (i = 0; i < 600; i = i + 1) begin
            do_train_s(antic_s, sat_s);
            cred_now = {16'd0, credit};
            if (cred_now > cred_prev) cred_rises = cred_rises + 1;
            cred_prev = cred_now;
            if (antic_s != 0) antic_cnt = antic_cnt + 1;
            if (sat_s != 0) sat_cnt = sat_cnt + 1;
        end
        ri = {16'd0, rprobe};
        if (ri != 65535 || cred_now != 255 || antic_cnt != cred_rises
            || cred_rises < 250 || sat_cnt != 89) begin
            errors = errors + 1;
            $display("FAIL S2b flood R=%0d C=%0d rises=%0d antic=%0d sat=%0d",
                     ri, cred_now, cred_rises, antic_cnt, sat_cnt);
        end else
            $display("S2b: as-built g=7 flood: R pegs 65535 (no wrap), credit 255,");
        $display("    telemetry integrity antic(%0d)==rises(%0d)", antic_cnt, cred_rises);

        // ---------------- S3: deadband leak ----------------
        corr = 1; gcls = 0; qlk = 4;
        rst_n = 0; repeat (1) @(negedge clk); rst_n = 1; repeat (1) @(negedge clk);
        do_train_s(antic_s, sat_s);              // R = 18260
        expv = 18260;                             // golden reservoir value
        failed = 0;
        for (i = 0; i < 3000; i = i + 1) begin
            do_tick2;
            leak_l = expv - (expv >> 4);
            if (leak_l >= expv) expv = 0; else expv = leak_l;
            ri = {16'd0, rprobe};
            if (ri != expv) begin
                failed = 1;
                if (errors < 25)
                    $display("FAIL S3 leak t=%0d R=%0d exp=%0d", i, ri, expv);
            end
            if (antic !== 1'b0) failed = 1;
        end
        ri = {16'd0, rprobe};
        if (failed || ri != 0) begin
            errors = errors + 1;
            $display("FAIL S3 deadband leak final=%0d failed=%0d", ri, failed);
        end else
            $display("S3: deadband leak golden-exact, reservoir reaches exactly 0");
        $display("    (sketch's 'snap at <=1' leaves a sticky floor at R in");
        $display("     [2,2^QLEAK]; this module snaps when the leak stalls)");

        // ---------------- S4: envelope tightening ----------------
        run_idx = 0;
        run_stream(31, 1, 4);   // 0: mis, corrected, qleak 4
        run_stream(31, 1, 5);   // 1: mis, corrected, qleak 5
        run_stream(31, 1, 6);   // 2: mis, corrected, qleak 6
        run_stream(31, 1, 8);   // 3: mis, corrected, qleak 8 (saturated)
        run_stream(31, 0, 5);   // 4: mis, as-built 2^g
        run_stream(0,  1, 5);   // 5: aligned, corrected, qleak 5

        if (!(mr_arr[0] < me_arr[0] && mr_arr[1] < me_arr[1]
              && mr_arr[2] < me_arr[2])) begin
            errors = errors + 1;
            $display("FAIL S4 tightening qleak 4/5/6");
        end
        if (!(mr_arr[1] < 0.5 * me_arr[1])) begin
            errors = errors + 1;
            $display("FAIL S4 qleak-5 halving");
        end
        if (!(mr_arr[3] > mr_arr[1])) begin
            errors = errors + 1;
            $display("FAIL S4 qleak-8 destroys tightening");
        end
        if (mc_arr[3] != 255) begin
            errors = errors + 1;
            $display("FAIL S4 qleak-8 saturation boundary (maxC=%0d)", mc_arr[3]);
        end
        if (!(mr_arr[4] == me_arr[4] && mc_arr[4] == 0)) begin
            errors = errors + 1;
            $display("FAIL S4 as-built no-op (err %f vs %f, maxC %0d)",
                     mr_arr[4], me_arr[4], mc_arr[4]);
        end
        if (!(mr_arr[5] > me_arr[5])) begin
            errors = errors + 1;
            $display("FAIL S4 aligned widening (Thm 3b)");
        end
        $display("S4: corrected deposit TIGHTENS the mis-phased envelope:");
        $display("  engine-alone mean|What-W| = %f", me_arr[0]);
        $display("  +corrected credit: qleak4 %f, qleak5 %f, qleak6 %f",
                 mr_arr[0], mr_arr[1], mr_arr[2]);
        $display("  qleak8 %f (reservoir saturates every deposit, over-credits,",
                 mr_arr[3]);
        $display("  tightening destroyed -- leak dial is the other half of the");
        $display("  convergence condition); as-built %f == engine-alone (credit",
                 mr_arr[4]);
        $display("  literally 0: 18,262x too small); ALIGNED control: %f > %f",
                 mr_arr[5], me_arr[5]);
        $display("  (credit widens -- Theorem 3b's honest negative result).");

        if (ovf !== 1'b0) begin
            errors = errors + 1;
            $display("FAIL S4 engine saturated during stream runs");
        end

        if (errors == 0) $display("TB_RQH_SATURATION PASS");
        else             $display("TB_RQH_SATURATION FAIL %0d", errors);
        $finish;
    end
endmodule
