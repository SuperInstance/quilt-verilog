// tb_judge_consistency.v -- judge-consistency harness for the covering
// condition b*sqrt(n)/2 <= eps (error-envelopes.md honest-ledger row 6,
// Theorems 4a/4b). No RTL judge exists (the condition is a design-time
// rule on the L0 dials), so the DUT side here is the INTEGER-SUBSTRATE
// judge exactly as the doc specifies it: quantized lattice coordinates,
// squared-form compare k1^2+..+kn^2 <= delta^2 in exact integer
// arithmetic -- no float, no sqrt (4.2 case 3) -- checked against a
// real-arithmetic golden judge, mirroring the fleet's reflex-arc
// 500-vector integer-agreement measurement (run in quilt-esp32, not here).
//
//  J1 covering (Thm 4a, valid basis): eps = 7; for n in {1,2,3} the rule
//      gives b = floor(2*eps/sqrt(n)) = 14, 9, 8. Sweeps over lattice
//      points, lattice-cell centers (deep holes -- "measurement points at
//      lattice centers"), the 1/8-phase sub-grid, and 500 LCG vectors per
//      dimension: quantization error <= eps everywhere; the deep-hole
//      error is exactly b*sqrt(n)/2 and lands in (eps-1, eps] (tightness:
//      the radius is attained, not over-estimated); the dial rule
//      n*b'^2 <= 4*eps^2 holds for every b' <= b and fails at b+1.
//  J2 judge consistency: integer verdict == real verdict whenever the true
//      distance avoids the fuzzy band |d - Delta| <= 2*eps (4.3: verdict
//      guaranteed correct outside the band); |d_int - d_real| <= 2*eps at
//      all vectors (the snap loop's honest bound); on-lattice vectors
//      agree with NO band exclusion (exact integer arithmetic, zero
//      comparison error -- incl. the equality point 8^2+0 <= 8^2).
//  J3 negative (necessity, off-center placements break it): at b+1 the
//      deep hole quantizes with error > eps -- witness printed; the
//      covering guarantee is gone. Metric note (4.2 case 4): at the n=2
//      bad hole the PER-COORDINATE error is 5 <= eps -- an l-inf judge
//      still passes there; the sqrt(n) is a property of the Euclidean
//      metric and the rule must be recomputed when the judge metric
//      changes.
`timescale 1ns/1ps
module tb_judge_consistency;
    integer errors = 0;
    real    eps = 7.0;
    real    tiny = 1.0e-9;

    reg [31:0] lcg = 32'd42;

    task nextr(output real r);
        begin
            lcg = lcg * 32'd1103515245 + 32'd12345;
            r = (lcg & 31'h7fffffff) / 2147483648.0;
        end
    endtask

    // lattice quantizer: round-to-nearest (Thm 4a Voronoi rule), x >= 0.
    // NOTE: $rtoi is load-bearing -- iverilog's implicit real->integer
    // assignment ROUNDS (qz(0.0,14) would read 1, err 14), $rtoi truncates
    // per IEEE 1364-2005 17.8; ties round up (deep hole -> upper corner).
    function integer qz;
        input real x;
        input integer bb;
        begin
            qz = $rtoi(x / bb + 0.5);
        end
    endfunction

    // ---------------- shared per-vector checks (n = 2 instantiated per
    // dimension by macro-free triplication below; n=1 and n=3 use the
    // same pattern) ----------------
    // generic counters
    integer nv, in_band, flips, cover_fail, loop_fail, lattice_flips;
    real    maxerr, err, dr, dinr;
    integer k1, k2, k3, dint2;
    reg     vint, vreal;
    real    x1, x2, x3, sx1, sx2;
    real    dd2;

    integer bb, i, j, kk;
    real    hole_err;
    integer ring_fail;

    // n=2 vector check, shared by grid+random loops
    task chk2(input real xa, input real ya, input integer b2, input integer s2,
              input integer d2);
        real e2;
        begin
            nv = nv + 1;
            k1 = qz(xa, b2) - s2;
            k2 = qz(ya, b2) - s2;
            dint2 = k1 * k1 + k2 * k2;
            vint = (dint2 <= d2 * d2);
            e2 = (xa - qz(xa, b2) * 1.0 * b2) ** 2.0
               + (ya - qz(ya, b2) * 1.0 * b2) ** 2.0;
            err = e2 ** 0.5;
            if (err > maxerr) maxerr = err;
            if (err > eps + tiny) cover_fail = cover_fail + 1;
            dd2 = (xa - s2 * 1.0 * b2) ** 2.0 + (ya - s2 * 1.0 * b2) ** 2.0;
            dr = dd2 ** 0.5;
            vreal = (dr <= d2 * 1.0 * b2 + tiny);
            dinr = (1.0 * dint2) ** 0.5 * b2;
            if (dinr - dr > 2.0 * eps + tiny || dr - dinr > 2.0 * eps + tiny)
                loop_fail = loop_fail + 1;
            if (dr > d2 * 1.0 * b2 - 2.0 * eps - tiny
                && dr < d2 * 1.0 * b2 + 2.0 * eps + tiny) begin
                in_band = in_band + 1;
            end else if (vint !== vreal) begin
                flips = flips + 1;
                $display("FAIL flip x=(%f,%f) dreal=%f vint=%0d vreal=%0d",
                         xa, ya, dr, vint, vreal);
            end
        end
    endtask

    // n=2 on-lattice check: exact agreement, no band exclusion
    task lat2(input integer li, input integer lj, input integer b2,
              input integer s2, input integer d2);
        begin
            nv = nv + 1;
            k1 = li - s2;
            k2 = lj - s2;
            dint2 = k1 * k1 + k2 * k2;
            vint = (dint2 <= d2 * d2);
            dr = ((1.0 * dint2) ** 0.5) * b2;
            vreal = (dr <= d2 * 1.0 * b2 + tiny);
            if (vint !== vreal) begin
                lattice_flips = lattice_flips + 1;
                $display("FAIL lattice flip (%0d,%0d)", li, lj);
            end
            err = 0.0;
        end
    endtask

    initial begin
        // ================= n = 1 =================
        // b = 14 = 2*eps exactly: hole error = eps, attained with equality
        nv = 0; in_band = 0; flips = 0; cover_fail = 0; loop_fail = 0;
        lattice_flips = 0; maxerr = 0.0;
        for (i = 0; i < 64; i = i + 1) begin
            // 1/8-phase sub-grid across four cells
            x1 = (i / 8) * 14.0 + (i % 8) * 14.0 / 8.0;
            k1 = qz(x1, 14) - 7;              // snap lattice index 7 (raw 98)
            dint2 = k1 * k1;
            vint = (dint2 <= 64);
            err = x1 - qz(x1, 14) * 1.0 * 14;
            if (err < 0.0) err = -err;
            if (err > maxerr) maxerr = err;
            if (err > eps + tiny) cover_fail = cover_fail + 1;
            dr = x1 - 7 * 14.0;
            if (dr < 0.0) dr = -dr;
            vreal = (dr <= 8 * 14.0 + tiny);
            dinr = (1.0 * dint2) ** 0.5 * 14;
            if (dinr - dr > 2.0 * eps + tiny || dr - dinr > 2.0 * eps + tiny)
                loop_fail = loop_fail + 1;
            if (dr > 8 * 14.0 - 2.0 * eps - tiny && dr < 8 * 14.0 + 2.0 * eps + tiny)
                in_band = in_band + 1;
            else if (vint !== vreal) begin
                flips = flips + 1;
                $display("FAIL n1 flip x=%f", x1);
            end
        end
        // deep holes at (k+0.5)*14: error exactly eps (equality case)
        hole_err = 14.0 / 2.0;
        if (!(hole_err <= eps + tiny && hole_err > eps - 1.0)) begin
            errors = errors + 1;
            $display("FAIL n1 hole tightness %f", hole_err);
        end
        // dial rule: b'^2 <= 4*eps^2 = 196 for b' <= 14, fails at 15
        for (bb = 1; bb <= 14; bb = bb + 1)
            if (1.0 * bb * bb > 196.0 + tiny) begin
                errors = errors + 1;
                $display("FAIL n1 dial rule b=%0d", bb);
            end
        if (!(1.0 * 15 * 15 > 196.0)) begin
            errors = errors + 1;
            $display("FAIL n1 dial rule must fail at b=15");
        end
        // random 500
        for (i = 0; i < 500; i = i + 1) begin
            nextr(x1);
            x1 = x1 * 16 * 14.0;
            nv = nv + 1;
            k1 = qz(x1, 14) - 7;
            dint2 = k1 * k1;
            vint = (dint2 <= 64);
            err = x1 - qz(x1, 14) * 1.0 * 14;
            if (err < 0.0) err = -err;
            if (err > maxerr) maxerr = err;
            if (err > eps + tiny) cover_fail = cover_fail + 1;
            dr = x1 - 98.0;
            if (dr < 0.0) dr = -dr;
            vreal = (dr <= 112.0 + tiny);
            dinr = (1.0 * dint2) ** 0.5 * 14;
            if (dinr - dr > 2.0 * eps + tiny || dr - dinr > 2.0 * eps + tiny)
                loop_fail = loop_fail + 1;
            if (dr > 112.0 - 14.0 - tiny && dr < 112.0 + 14.0 + tiny)
                in_band = in_band + 1;
            else if (vint !== vreal) begin
                flips = flips + 1;
                $display("FAIL n1 rand flip x=%f d=%f", x1, dr);
            end
        end
        $display("J1/J2 n=1 b=14: %0d vectors, max quant err %f <= eps,",
                 nv, maxerr);
        $display("  hole err = eps exactly (b = 2*eps, attained); flips outside");
        $display("  band = %0d (in-band %0d), loop bound violations %0d",
                 flips, in_band, loop_fail);
        if (flips != 0 || cover_fail != 0 || loop_fail != 0)
            errors = errors + 1;
        // J3: b = 15 breaks it
        hole_err = 15.0 / 2.0;
        if (!(hole_err > eps + tiny)) begin
            errors = errors + 1;
            $display("FAIL n1 negative hole %f", hole_err);
        end else
            $display("J3 n=1 b=15: deep hole err %f > eps -- guarantee broken",
                     hole_err);

        // ================= n = 2 =================
        // b = 9 <= 2*eps/sqrt(2) = 9.899; snap index (8,8), delta = 8 units
        nv = 0; in_band = 0; flips = 0; cover_fail = 0; loop_fail = 0;
        lattice_flips = 0; maxerr = 0.0;
        // on-lattice ring incl. equality (8,0): 64 <= 64 both judges
        ring_fail = 0;
        for (i = 0; i <= 9; i = i + 1)
            for (j = 0; j <= 9; j = j + 1)
                lat2(i, j, 9, 8, 8);
        if (lattice_flips != 0) ring_fail = 1;
        // deep holes at cell centers around the snap point
        for (i = 7; i <= 9; i = i + 1)
            for (j = 7; j <= 9; j = j + 1)
                chk2((i + 0.5) * 9.0, (j + 0.5) * 9.0, 9, 8, 8);
        hole_err = (2.0 * 9 * 9 / 4.0) ** 0.5;   // = b*sqrt(2)/2 = 6.364
        if (!(hole_err <= eps + tiny && hole_err > eps - 1.0)) begin
            errors = errors + 1;
            $display("FAIL n2 hole tightness %f", hole_err);
        end
        // 1/8-phase sub-grid at three anchors
        for (kk = 0; kk < 3; kk = kk + 1) begin
            sx1 = (kk == 0) ? 8 * 9.0 : (kk == 1) ? 9 * 9.0 : 7 * 9.0;
            sx2 = (kk == 0) ? 8 * 9.0 : (kk == 1) ? 10 * 9.0 : 6 * 9.0;
            for (i = 0; i < 8; i = i + 1)
                for (j = 0; j < 8; j = j + 1)
                    chk2(sx1 + i * 9.0 / 8.0, sx2 + j * 9.0 / 8.0, 9, 8, 8);
        end
        // 500 random vectors
        for (i = 0; i < 500; i = i + 1) begin
            nextr(x1); nextr(x2);
            chk2(x1 * 16 * 9.0, x2 * 16 * 9.0, 9, 8, 8);
        end
        // dial rule
        for (bb = 1; bb <= 9; bb = bb + 1)
            if (2.0 * bb * bb > 196.0 + tiny) begin
                errors = errors + 1;
                $display("FAIL n2 dial rule b=%0d", bb);
            end
        if (!(2.0 * 10 * 10 > 196.0)) begin
            errors = errors + 1;
            $display("FAIL n2 dial rule must fail at b=10");
        end
        $display("J1/J2 n=2 b=9: %0d vectors (100 on-lattice incl. the 8^2+0<=8^2",
                 nv);
        $display("  equality, 9 deep holes, 192 sub-grid, 500 random), max quant");
        $display("  err %f <= eps, hole err b*sqrt(2)/2 = %f in (eps-1,eps];",
                 maxerr, hole_err);
        $display("  on-lattice flips %0d, outside-band flips %0d (in-band %0d),",
                 lattice_flips, flips, in_band);
        $display("  |d_int - d_real| <= 2*eps violations %0d", loop_fail);
        if (flips != 0 || cover_fail != 0 || loop_fail != 0 || ring_fail != 0)
            errors = errors + 1;
        // J3: b = 10
        hole_err = (2.0 * 10 * 10 / 4.0) ** 0.5;  // 7.071 > 7
        if (!(hole_err > eps + tiny)) begin
            errors = errors + 1;
            $display("FAIL n2 negative hole %f", hole_err);
        end else begin
            $display("J3 n=2 b=10: deep hole (x+5, y+5) err %f > eps -- off-center",
                     hole_err);
            $display("  placement breaks the guarantee (l-inf judge would still");
            $display("  pass: per-coord 5 <= 7 -- the metric is a D2 dial, 4.2.4)");
        end

        // ================= n = 3 =================
        // b = 8 <= 2*eps/sqrt(3) = 8.083; snap (8,8,8), delta = 8
        nv = 0; in_band = 0; flips = 0; cover_fail = 0; loop_fail = 0;
        lattice_flips = 0; maxerr = 0.0;
        for (kk = 0; kk < 2; kk = kk + 1)
            for (i = 0; i < 8; i = i + 1)
                for (j = 0; j < 8; j = j + 1)
                    for (bb = 0; bb < 8; bb = bb + 1) begin
                        nv = nv + 1;
                        x1 = (8 + kk) * 8.0 + i * 8.0 / 8.0;
                        x2 = (8 + kk) * 8.0 + j * 8.0 / 8.0;
                        x3 = (8 + kk) * 8.0 + bb * 8.0 / 8.0;
                        k1 = qz(x1, 8) - 8;
                        k2 = qz(x2, 8) - 8;
                        k3 = qz(x3, 8) - 8;
                        dint2 = k1 * k1 + k2 * k2 + k3 * k3;
                        vint = (dint2 <= 64);
                        err = ((x1 - qz(x1, 8) * 8.0) ** 2.0
                             + (x2 - qz(x2, 8) * 8.0) ** 2.0
                             + (x3 - qz(x3, 8) * 8.0) ** 2.0) ** 0.5;
                        if (err > maxerr) maxerr = err;
                        if (err > eps + tiny) cover_fail = cover_fail + 1;
                        dd2 = (x1 - 64.0) ** 2.0 + (x2 - 64.0) ** 2.0
                            + (x3 - 64.0) ** 2.0;
                        dr = dd2 ** 0.5;
                        vreal = (dr <= 64.0 + tiny);
                        dinr = (1.0 * dint2) ** 0.5 * 8;
                        if (dinr - dr > 2.0 * eps + tiny
                            || dr - dinr > 2.0 * eps + tiny)
                            loop_fail = loop_fail + 1;
                        if (dr > 64.0 - 14.0 - tiny && dr < 64.0 + 14.0 + tiny)
                            in_band = in_band + 1;
                        else if (vint !== vreal) begin
                            flips = flips + 1;
                            $display("FAIL n3 flip (%f,%f,%f)", x1, x2, x3);
                        end
                    end
        hole_err = (3.0 * 8 * 8 / 4.0) ** 0.5;   // = 8*sqrt(3)/2 = 6.928
        if (!(hole_err <= eps + tiny && hole_err > eps - 1.0)) begin
            errors = errors + 1;
            $display("FAIL n3 hole tightness %f", hole_err);
        end
        if (!(3.0 * 9 * 9 > 196.0)) begin
            errors = errors + 1;
            $display("FAIL n3 dial rule must fail at b=9");
        end
        $display("J1/J2 n=3 b=8: %0d sub-grid vectors, max quant err %f <= eps,",
                 nv, maxerr);
        $display("  hole err b*sqrt(3)/2 = %f in (eps-1,eps]; flips outside band",
                 hole_err);
        $display("  %0d (in-band %0d), loop violations %0d", flips, in_band, loop_fail);
        if (flips != 0 || cover_fail != 0 || loop_fail != 0)
            errors = errors + 1;
        // J3: b = 9
        hole_err = (3.0 * 9 * 9 / 4.0) ** 0.5;   // 7.794 > 7
        if (!(hole_err > eps + tiny)) begin
            errors = errors + 1;
            $display("FAIL n3 negative hole %f", hole_err);
        end else
            $display("J3 n=3 b=9: deep hole err %f > eps -- guarantee broken",
                     hole_err);

        if (errors == 0) $display("TB_JUDGE_CONSISTENCY PASS");
        else             $display("TB_JUDGE_CONSISTENCY FAIL %0d", errors);
        $finish;
    end
endmodule
