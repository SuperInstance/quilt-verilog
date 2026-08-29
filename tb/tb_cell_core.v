// tb_cell_core.v -- one-cell tests on q_cell: opcode semantics with exact
// golden values, plus the Q1/Q2 gate checks from docs/SYNTHESIS.md:
//  Q1: under a continuous effect flood (ci_valid never idle), the gap
//      between ci_ready pulses never exceeds MAX_OP_CYCLES.
//  Q2: a tick strobe under the same flood reaches the tick service state
//      within the bound (front-of-queue deadline, not !ci_valid deferral).
`timescale 1ns/1ps
module tb_cell_core;
    reg clk = 0, rst_n = 0, s_tick = 0;
    always #5 clk = ~clk;

    // ring side
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
        .clk(clk), .rst_n(rst_n), .i_myid(4'd1), .s_tick(s_tick),
        .o_ovf(ovf),
        .ri_valid(ri_valid), .ri_ready(ri_ready),
        .ri_op(ri_op), .ri_src(ri_src), .ri_dst(ri_dst),
        .ri_a0(ri_a0), .ri_a1(ri_a1), .ri_a2(ri_a2), .ri_dat(ri_dat),
        .ro_valid(ro_valid), .ro_ready(ro_ready),
        .ro_op(ro_op), .ro_src(ro_src), .ro_dst(ro_dst),
        .ro_a0(ro_a0), .ro_a1(ro_a1), .ro_a2(ro_a2), .ro_dat(ro_dat)
    );

    localparam MAXOP = 64;   // docs/SYNTHESIS.md I1 bound

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
            ri_valid <= 0;  // NBA: deassert exactly after the transfer edge
                            // (protocol: no stale-valid phantom cycle)
        end
    endtask

    reg [3:0] exp_dst;
    task recv_exp(input [2:0] expop, input [15:0] expdat, input [127:0] name);
        begin
            @(negedge clk);   // settle: never sample at a posedge timestep
            guard = 0;
            while (ro_valid !== 1'b1 && guard < 2000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (ro_valid !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL %0s timeout", name);
            end else begin
                if (ro_op !== expop || ro_dat !== expdat || ro_dst !== exp_dst) begin
                    errors = errors + 1;
                    $display("FAIL %0s op=%0d dat=%h dst=%h",
                             name, ro_op, ro_dat, ro_dst);
                end
                @(negedge clk);
            end
        end
    endtask


    // golden activation model (mirrors core arithmetic, integer-exact)
    integer act_g = 0;
    integer w_g   = 0;
    integer n;

    // Q1/Q2 flood monitors
    integer gap = 0, maxgap = 0;
    integer flood = 0;
    integer tick_lat = -1, tick_cnt = 0;
    integer fdat = 0;

    always @(negedge clk) begin
        if (flood) begin
            // keep an effect flit presented whenever the core wants one
            if (ri_ready) begin
                ri_valid = 1; ri_op = 3'd2; ri_src = 4'd2; ri_dst = 4'd1;
                ri_a0 = 0; ri_a1 = 0; ri_a2 = 0;
                ri_dat = 16'h2000 + fdat[15:0];
                fdat = fdat + 1;
            end
            // Q1: ci_ready gap bound
            if (dut.u_core.ci_ready !== 1'b1) begin
                gap = gap + 1;
                if (gap > maxgap) maxgap = gap;
            end else begin
                gap = 0;
            end
            // Q2: latency from strobe to tick service
            if (tick_lat >= 0) begin
                if (dut.u_core.state === 5'd14) begin
                    tick_lat = -1;   // serviced
                end else begin
                    tick_lat = tick_lat + 1;
                    if (tick_lat > 2*MAXOP) begin
                        errors = errors + 1;
                        $display("FAIL Q2 tick latency %0d", tick_lat);
                        tick_lat = -1;
                    end
                end
            end
        end else begin
            gap = 0;
        end
    end

    // stroke ticks periodically during the flood
    always @(negedge clk) begin
        if (flood) begin
            tick_cnt = tick_cnt + 1;
            if (tick_cnt == 300) begin
                s_tick = 1;
                tick_lat = 0;
            end else if (tick_cnt == 301) begin
                s_tick = 0;
            end else if (tick_cnt == 700) begin
                s_tick = 1;
                tick_lat = 0;
            end else if (tick_cnt == 701) begin
                s_tick = 0;
            end else if (tick_cnt >= 1000) begin
                tick_cnt = 0;
            end
        end
    end

    reg [15:0] rw;
    task view(input [1:0] sel, output [15:0] v);
        begin
            send(3'd3, 4'd9, {14'd0, sel}, 16'd0, 16'd0, 16'd0);
            @(negedge clk);   // settle
            guard = 0;
            while (ro_valid !== 1'b1 && guard < 2000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 2000) begin
                errors = errors + 1;
                $display("FAIL view sel=%0d TIMEOUT st=%0d", sel, dut.u_core.state);
            end
            v = ro_dat;
            @(negedge clk);
        end
    endtask

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (4) @(negedge clk);

        // 1: first flit must be bind; sets cell id and acks
        send(3'd0, 4'd9, 16'd1, 16'd0, 16'd0, 16'd0);
        exp_dst = 4'd9;
        recv_exp(3'd5, 16'h0, "bind_ack");

        // 2: link edge slot0: peer=2, base=0x1000
        send(3'd1, 4'd2, 16'd0, 16'h1000, 16'd0, 16'd0);
        exp_dst = 4'd2;
        recv_exp(3'd5, 16'h0, "link_ack");

        // 3: three effects from peer 2; exact golden activation
        for (n = 1; n <= 3; n = n + 1) begin
            send(3'd2, 4'd2, 16'd0, 16'd0, 16'd0, 16'h4000);
            w_g = 16'h1000 + n*256;
            act_g = act_g + (w_g >> 1);   // (w*0x4000)>>>15 == w>>1
            repeat (30) @(negedge clk);   // let the effect op complete
        end
        view(2'd0, rw);
        if (rw !== act_g[15:0]) begin
            errors = errors + 1;
            $display("FAIL act golden got=%h exp=%h", rw, act_g[15:0]);
        end

        // 4: wsum view == base + 3*256 exactly
        view(2'd1, rw);
        if (rw !== 16'h1000 + 3*256) begin
            errors = errors + 1;
            $display("FAIL wsum got=%h", rw);
        end

        // 5: dial read via view(2): THRESH default
        send(3'd3, 4'd9, 16'd2, 16'd5, 16'd0, 16'd0);
        exp_dst = 4'd9;
        recv_exp(3'd5, 16'h6000, "dial_rd");

        // 6: view(3) NAKs (no cosine engine in v1)
        send(3'd3, 4'd9, 16'd3, 16'd0, 16'd0, 16'd0);
        exp_dst = 4'd9;
        recv_exp(3'd6, 16'h0, "view3_nak");

        // 7: Q1/Q2 flood: continuous effects + tick deadlines
        flood = 1;
        repeat (1500) @(negedge clk);
        flood = 0;
        ri_valid = 0;
        if (maxgap > MAXOP) begin
            errors = errors + 1;
            $display("FAIL Q1 maxgap=%0d", maxgap);
        end

        // 8: decay: HL=2, six spaced ticks -> wsum strictly below threshold
        // let the flood backlog drain before the decay phase
        repeat (300) @(negedge clk);
        send(3'd0, 4'd9, 16'd10, 16'd2, 16'd0, 16'd0);
        exp_dst = 4'd9;
        recv_exp(3'd5, 16'h0, "hl_bind");
        for (n = 0; n < 6; n = n + 1) begin
            @(negedge clk); s_tick = 1;
            @(negedge clk); s_tick = 0;
            repeat (60) @(negedge clk);   // let the sweep finish
        end
        view(2'd1, rw);
        if (!(rw < 16'h6000)) begin
            errors = errors + 1;
            $display("FAIL decay wsum=%h", rw);
        end

        if (errors == 0) $display("TB_CELL_CORE PASS");
        else $display("TB_CELL_CORE FAIL %0d", errors);
        $finish;
    end
endmodule
