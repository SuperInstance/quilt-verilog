// t2_hebbian_edges.v -- TUTORIAL 2: Hebbian edges learn and forget
// (examples/).
//
// The edge is the star: a tiny learned weight bank (q_hebbian ladder,
// K=8 buckets) living in the HEARING cell. Every accepted effect trains
// it (+1 into bucket 0 = +0x100 of weight), every half-life the ladder
// shifts one class older and the old counts halve their say. You will:
//
//   link    cell 0 hears peer 1, base weight 0x1000,
//   train   10 paced effects (src=1 -> dst=0, dat=0x4000),
//   read    wsum = 0x1000 + 10*0x100 = 0x1A00  -- exact golden,
//   forget  set the half-life dial HL=2 and let ticks sweep the ladder,
//   read    wsum walks down as the counts shift bucket to bucket, then
//           lands back at the base 0x1000 when the ladder empties.
//
// A VCD waveform is dumped (out/t2.vcd): open it in GTKWave and watch
// dut.nodes[0].u_core.act fall tick by tick and the wsum view responses
// step down the dyadic staircase (0x1A00 -> ... -> 0x1000).
//
// THRESH is parked at 0x7FFF so nothing fires -- this tutorial keeps the
// lens on the weights. (Fires are Tutorial 1 territory: see
// tb/tb_fabric_smoke.v for the train->fire->decay acceptance gate.)
//
// Run: bash examples/t2_hebbian_edges/run.sh
`timescale 1ns/1ps
module t2_hebbian_edges;
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

    q_fabric_top #(.NCELL(2), .TPW(4)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_val(i_val), .o_rdy(o_rdy),
        .i_op(i_op), .i_src(i_src), .i_dst(i_dst),
        .i_a0(i_a0), .i_a1(i_a1), .i_a2(i_a2), .i_dat(i_dat),
        .o_val(o_val), .i_rdy(i_rdy_t),
        .o_op(o_op), .o_src(o_src), .o_dst(o_dst),
        .o_a0(o_a0), .o_a1(o_a1), .o_a2(o_a2), .o_dat(o_dat),
        .o_ovf(ovf)
    );

    // waveform for the ladder walk (see run.sh for the path)
    initial begin
        $dumpfile("t2_hebbian_edges.vcd");
        $dumpvars(0, dut);
    end

    // -- house send/recv pattern (tb/tb_fabric_smoke.v) -------------------
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
            guard = 0;
            while (o_val !== 1'b1 && guard < 20000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (o_val !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL %0s: no ack", name);
            end else begin
                i_rdy_t = 1;
                @(negedge clk);
                i_rdy_t = 0;
            end
        end
    endtask

    reg [15:0] v;
    task do_view(input [3:0] cid, input [1:0] sel, input [3:0] arg,
                 input [127:0] what);
        begin
            send(3'd3, 4'hF, cid, {14'd0, sel}, {12'd0, arg},
                 16'd0, 16'd0);
            guard = 0;
            while (o_val !== 1'b1 && guard < 20000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (o_val !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL view %0s: timeout", what);
            end else begin
                v = o_dat;
                i_rdy_t = 1;
                @(negedge clk);
                i_rdy_t = 0;
                $display("view  cell %0d %-16s = 0x%04h", cid, what, v);
            end
        end
    endtask

    task expect16(input [15:0] got, input [15:0] exp,
                  input [127:0] what);
        begin
            if (got !== exp) begin
                errors = errors + 1;
                $display("FAIL %0s: got %h exp %h", what, got, exp);
            end
        end
    endtask

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (10) @(negedge clk);
        $display("== T2 hebbian edges: NCELL=2, TPW=4, K=8 ladder ==");

        // ---- setup: bind both cells, park THRESH, link 0 <- 1 ----------
        send(3'd0, 4'hF, 4'd0, 16'd0, 16'd0, 16'd0, 16'd0);
        recv_ack("bind0");
        send(3'd0, 4'hF, 4'd1, 16'd1, 16'd0, 16'd0, 16'd0);
        recv_ack("bind1");
        send(3'd0, 4'hF, 4'd0, 16'd5, 16'h7FFF, 16'd0, 16'd0); // THRESH max
        recv_ack("thresh");

        // link: slot 0 of cell 0 := {peer=1, base=0x1000}; the ACK is
        // addressed to the PEER and is consumed there (Law 2: responses
        // are traffic) -- verify the link took by reading the sum back.
        send(3'd1, 4'd1, 4'd0, 16'd0, 16'h1000, 16'd0, 16'd0);
        do_view(4'd0, 2'd1, 4'd0, "wsum after link");
        expect16(v, 16'h1000, "wsum_fresh_link");

        // ---- train: 10 paced effects, one cofire each ------------------
        for (n = 0; n < 10; n = n + 1) begin
            send(3'd2, 4'd1, 4'd0, 16'd0, 16'd0, 16'd0, 16'h4000);
            repeat (48) @(negedge clk);    // pace: engine needs ~15 cy
        end
        $display("train 10 effects delivered (src=1 -> dst=0)");
        do_view(4'd0, 2'd1, 4'd0, "wsum after 10x");
        // each cofire puts +1 in bucket 0; the ladder readout prices
        // bucket i at 2^(8-i), so 10 cofires = 10 * 0x100:
        expect16(v, 16'h1A00, "wsum_10_cofires_exact");
        do_view(4'd0, 2'd0, 4'd0, "act (buzz)");

        // ---- forget: HL=2, ticks sweep the ladder ----------------------
        send(3'd0, 4'hF, 4'd0, 16'd10, 16'd2, 16'd0, 16'd0);   // HL dial=2
        recv_ack("hl2");
        $display("dial  HL=2 (half-life = 2 ticks), letting ticks sweep");

        repeat (4*16 + 8) @(negedge clk);   // ~4 ticks: ~2 shifts deep
        do_view(4'd0, 2'd1, 4'd0, "wsum ~4 ticks");

        repeat (40*16 + 64) @(negedge clk); // 40+ ticks: ladder swept out
        do_view(4'd0, 2'd1, 4'd0, "wsum swept out");
        // every count has shifted past bucket K-1; only the base remains
        expect16(v, 16'h1000, "wsum_back_to_base");

        if (errors == 0)
            $display("T2 PASS: ladder learned 0x1000->0x1A00, forgot ->0x1000");
        else
            $display("T2 FAIL: %0d error(s)", errors);
        $finish;
    end

    initial begin
        #2_000_000;
        $display("T2 FAIL: watchdog");
        $finish;
    end
endmodule
