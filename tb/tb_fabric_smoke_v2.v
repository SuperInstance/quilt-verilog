// tb_fabric_smoke_v2.v -- THE v2 acceptance gate (echo gate + RQH pair).
// train -> fire -> decay's v2 amendment (INNOVATION-JUDGEMENT §5.1):
// fire -> echo -> graded-train -> tighten, on the real 4-cell ring, with
// both features DEFAULT-OFF-able (the A/B referee collapses to v1 in situ).
//
//   P1 echo suppression under a flooding sender: cell 1 never fired, so a
//      60-effect flood trains NOTHING -- wsum stays exactly base (v1 would
//      read base + 60*256). FTRACE reads 0.
//   P2 fire opens the gate: drive act past THRESH, fire observed (act==0),
//      FTRACE==0xFFFF; then three deterministic graded cofires land in
//      buckets 0/1/4 as the trace decays (KLE=2): wsum moves by exactly
//      +256 / +128 / +16.
//   P3 RQH tightening observed in w readout: with RQEN on, a class-4
//      cofire moves wsum by 16 (engine) + 4 (corrected-T3c credit); the
//      A/B toggles RQEN off/on around it. Credit arithmetic is bit-exact.
//   P4 v1 collapse: FLOOR=0, RQEN=0 -> ungated +256/cofire, bit-exact v1.
//
// TPW=10 (1024-cycle ticks) so every "wait N ticks" window (N*1024+128)
// contains exactly N tick services regardless of phase; ring round trips
// (~100 cycles) never race a tick boundary.
`timescale 1ns/1ps
module tb_fabric_smoke_v2;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg         i_val = 0, i_rdy_t = 0;
    reg  [2:0]  i_op = 0;
    reg  [3:0]  i_src = 0, i_dst = 0;
    reg  [15:0] i_a0 = 0, i_a1 = 0, i_a2 = 0, i_dat = 0;
    wire        o_rdy, o_val;
    wire [2:0]  o_op;
    wire [3:0]  o_src, o_dst;
    wire [15:0] o_a0, o_a1, o_a2, o_dat;
    wire        ovf;

    integer errors = 0, guard, n;
    integer maxlat = 0, lat;
    localparam TICK = 1024;   // 2^TPW, TPW=10

    q_fabric_top #(.NCELL(4), .TPW(10)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_val(i_val), .o_rdy(o_rdy),
        .i_op(i_op), .i_src(i_src), .i_dst(i_dst),
        .i_a0(i_a0), .i_a1(i_a1), .i_a2(i_a2), .i_dat(i_dat),
        .o_val(o_val), .i_rdy(i_rdy_t),
        .o_op(o_op), .o_src(o_src), .o_dst(o_dst),
        .o_a0(o_a0), .o_a1(o_a1), .o_a2(o_a2), .o_dat(o_dat),
        .o_ovf(ovf)
    );

    task send(input [2:0] op, input [3:0] src, input [3:0] dst,
              input [15:0] a0, input [15:0] a1,
              input [15:0] a2, input [15:0] dat);
        begin
            @(negedge clk);
            i_val = 1; i_op = op; i_src = src; i_dst = dst;
            i_a0 = a0; i_a1 = a1; i_a2 = a2; i_dat = dat;
            guard = 0;
            while (o_rdy !== 1'b1 && guard < 2000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 2000) begin
                errors = errors + 1;
                $display("FAIL send_timeout op=%0d dst=%h", op, dst);
            end
            @(posedge clk);
            i_val <= 0;
        end
    endtask

    task recv_ack(input [127:0] name);
        begin
            lat = 0;
            while (o_val !== 1'b1 && lat < 20000) begin
                @(negedge clk); lat = lat + 1;
            end
            if (lat > maxlat) maxlat = lat;
            if (o_val !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL %0s timeout", name);
            end else begin
                if (o_op !== 3'd5 || o_dst !== 4'hF) begin
                    errors = errors + 1;
                    $display("FAIL %0s op=%0d dst=%h", name, o_op, o_dst);
                end
                i_rdy_t = 1;
                @(negedge clk);
                i_rdy_t = 0;
            end
        end
    endtask

    reg [15:0] vdat;
    task do_view(input [3:0] cid, input [1:0] sel, input [3:0] dial,
                 output [15:0] v);
        begin
            send(3'd3, 4'hF, cid, {14'd0, sel}, {12'd0, dial}, 16'd0, 16'd0);
            lat = 0;
            while (o_val !== 1'b1 && lat < 20000) begin
                @(negedge clk); lat = lat + 1;
            end
            if (lat > maxlat) maxlat = lat;
            if (o_val !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL view cid=%0d timeout", cid);
                v = 16'hxxxx;
            end else begin
                v = o_dat;
                i_rdy_t = 1;
                @(negedge clk);
                i_rdy_t = 0;
            end
        end
    endtask

    task chk16(input [15:0] got, input [15:0] exp, input [127:0] name);
        begin
            if (got !== exp) begin
                errors = errors + 1;
                $display("FAIL %0s got=%h exp=%h", name, got, exp);
            end
        end
    endtask

    // one paced effect from the flooding sender (peer 2) into cell 1
    task flood(input [15:0] dat);
        begin
            send(3'd2, 4'd2, 4'd1, 16'd0, 16'd0, 16'd0, dat);
            repeat (32) @(negedge clk);
        end
    endtask

    // wait exactly N tick services (N*TICK + margin < (N+1)*TICK)
    task wait_ticks(input integer n);
        integer w;
        begin
            for (w = 0; w < n*TICK + 128; w = w + 1)
                @(negedge clk);
        end
    endtask

    // dial write via bind
    task dial_wr(input [3:0] cid, input [3:0] addr, input [15:0] val,
                 input [127:0] name);
        begin
            send(3'd0, 4'hF, cid, {12'd0, addr}, val, 16'd0, 16'd0);
            recv_ack(name);
        end
    endtask

    task view_wsum(output [15:0] v);
        begin do_view(4'd1, 2'd1, 4'd0, v); end
    endtask

    integer hot;

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (10) @(negedge clk);

        // ---- setup: bind 1 and 2, link A=1<->peer2 base 0x1000 ----
        send(3'd0, 4'hF, 4'd1, 16'd1, 16'd0, 16'd0, 16'd0);
        recv_ack("bind1");
        send(3'd0, 4'hF, 4'd2, 16'd2, 16'd0, 16'd0, 16'd0);
        recv_ack("bind2");
        send(3'd1, 4'd2, 4'd1, 16'd0, 16'h1000, 16'd0, 16'd0);
        view_wsum(vdat);
        chk16(vdat, 16'h1000, "linkA_wsum");

        // echo gate ON: KLE=2 (dial 11), FLOOR=0x0080 (dial 12)
        dial_wr(4'd1, 4'd11, 16'd2,    "kle2");
        dial_wr(4'd1, 4'd12, 16'h0080, "floor80");

        // ---- P1: flooding sender, gate closed: nothing trains ----
        for (n = 0; n < 60; n = n + 1)
            flood(16'h0800);              // +256 act each, below THRESH
        view_wsum(vdat);
        chk16(vdat, 16'h1000, "P1_wsum_base");     // v1 would show 0x4C00
        do_view(4'd1, 2'd0, 4'd0, vdat);
        if (vdat == 16'd0 || vdat >= 16'h6000) begin
            errors = errors + 1;
            $display("FAIL P1_act=%h (flood must charge but not fire)", vdat);
        end
        do_view(4'd1, 2'd2, 4'd13, vdat);
        chk16(vdat, 16'h0000, "P1_ftrace0");       // never fired

        // ---- P2: fire opens the gate ----
        // hot effects until act >= 0x6800 (fire at the next tick service)
        hot = 0;
        do_view(4'd1, 2'd0, 4'd0, vdat);
        while (vdat < 16'h6800 && hot < 12) begin
            flood(16'h4000);                        // +2048 act each
            do_view(4'd1, 2'd0, 4'd0, vdat);
            hot = hot + 1;
        end
        if (vdat < 16'h6000) begin
            errors = errors + 1;
            $display("FAIL P2_no_charge act=%h", vdat);
        end
        // wait for the fire: act clears to exactly 0 at ST_FIRE
        guard = 0;
        vdat = 16'hFFFF;
        while (vdat !== 16'h0000 && guard < 200) begin
            do_view(4'd1, 2'd0, 4'd0, vdat);
            guard = guard + 1;
        end
        chk16(vdat, 16'h0000, "P2_fired");
        // trace refilled to max at the fire tick, before the next tick
        do_view(4'd1, 2'd2, 4'd13, vdat);
        chk16(vdat, 16'hFFFF, "P2_ftrace_full");

        // e1: echo inside the same tick window -> bucket 0 (+256)
        flood(16'h4000);
        view_wsum(vdat);
        chk16(vdat, 16'h1100, "P2_e1_b0");

        // e2: 3 ticks of trace decay: F=0x6C00 -> bucket 1 (+128)
        wait_ticks(3);
        flood(16'h4000);
        view_wsum(vdat);
        chk16(vdat, 16'h1180, "P2_e2_b1");

        // e3: 7 more ticks (10 total): F=0x0E6B -> bucket 4 (+16)
        wait_ticks(7);
        flood(16'h4000);
        view_wsum(vdat);
        chk16(vdat, 16'h1190, "P2_e3_b4");

        // ---- P3: RQH tightening observed in w readout ----
        // RQEN on (QDW=8). 1 tick: F=0x0AD9 -> still bucket 4. The graded
        // cofire pays engine +16 AND banks dep(4)=1152 quanta -> credit 4:
        // wsum = 0x1190 + 16 + 4.
        dial_wr(4'd1, 4'd14, 16'h8008, "rq_on");
        wait_ticks(1);
        flood(16'h4000);
        view_wsum(vdat);
        chk16(vdat, 16'h11A4, "P3_e4_credit_on");

        // A/B: RQEN off. 1 tick: F=0x081D -> still bucket 4 (+16 engine);
        // the credit is SUPPRESSED from the readout (frozen, not spent):
        // wsum = 0x11A0 + 16 + 0 (the -4 vs e4's view IS the A/B delta).
        dial_wr(4'd1, 4'd14, 16'h0008, "rq_off");
        wait_ticks(1);
        flood(16'h4000);
        view_wsum(vdat);
        chk16(vdat, 16'h11B0, "P3_e5_credit_off");

        // RQEN on again. 1 tick: F=0x0616 -> bucket 5 (+8); reservoir
        // (frozen at 1152) leaks 1152->1148, deposits dep(5)=576 -> 1724
        // -> credit 6: wsum = 0x11B8 + 6.
        dial_wr(4'd1, 4'd14, 16'h8008, "rq_on2");
        wait_ticks(1);
        flood(16'h4000);
        view_wsum(vdat);
        chk16(vdat, 16'h11BE, "P3_e6_credit_on2");

        // ---- P4: v1 collapse (the referee's switch) ----
        // FLOOR=0 + RQEN=0: ungated, ungraded, uncredited -- +256/cofire
        // and zero credit: engine ladder alone (0x11B8 + 10*256).
        dial_wr(4'd1, 4'd12, 16'h0000, "floor0");
        dial_wr(4'd1, 4'd14, 16'h0008, "rq_off2");
        for (n = 0; n < 10; n = n + 1)
            flood(16'h4000);
        view_wsum(vdat);
        chk16(vdat, 16'h1BB8, "P4_v1_semantics");

        // Q1 spot check on the live fabric
        if (maxlat > 20000) begin
            errors = errors + 1;
            $display("FAIL view latency %0d", maxlat);
        end

        if (errors == 0)
            $display("TB_FABRIC_SMOKE_V2 PASS (echo-gate+RQH, maxlat=%0d)",
                     maxlat);
        else
            $display("TB_FABRIC_SMOKE_V2 FAIL %0d", errors);
        $finish;
    end

    initial begin
        #50_000_000;
        $display("TB_FABRIC_SMOKE_V2 FAIL watchdog");
        $finish;
    end
endmodule
