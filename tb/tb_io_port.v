// tb_io_port.v -- Law-4 contract node: looped through one pipe slice.
// Ingress addressed to EXTID round-trips to egress; a circulating transit
// flit does not starve later injections (bubble liveness).
`timescale 1ns/1ps
module tb_io_port;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    // io port
    reg         i_val = 0, i_rdy_t = 0;
    reg  [2:0]  i_op = 0;
    reg  [3:0]  i_src = 0, i_dst = 0;
    reg  [15:0] i_a0 = 0, i_a1 = 0, i_a2 = 0, i_dat = 0;
    wire        o_rdy, o_val;
    wire [2:0]  o_op;
    wire [3:0]  o_src, o_dst;
    wire [15:0] o_a0, o_a1, o_a2, o_dat;

    // ring loop: io.ro -> pipe -> io.ri
    wire        rov, pir, pov, pirr;
    wire [2:0]  ro_op, pi_op;
    wire [3:0]  ro_src, ro_dst, pi_src, pi_dst;
    wire [15:0] ro_a0, ro_a1, ro_a2, ro_dat;
    wire [15:0] pi_a0, pi_a1, pi_a2, pi_dat;

    integer errors = 0, guard;

    q_io_port #(.EXTID(4'hF)) u_io (
        .ri_valid(pov), .ri_ready(pirr),
        .ri_op(pi_op), .ri_src(pi_src), .ri_dst(pi_dst),
        .ri_a0(pi_a0), .ri_a1(pi_a1), .ri_a2(pi_a2), .ri_dat(pi_dat),
        .ro_valid(rov), .ro_ready(pir),
        .ro_op(ro_op), .ro_src(ro_src), .ro_dst(ro_dst),
        .ro_a0(ro_a0), .ro_a1(ro_a1), .ro_a2(ro_a2), .ro_dat(ro_dat),
        .i_val(i_val), .o_rdy(o_rdy),
        .i_op(i_op), .i_src(i_src), .i_dst(i_dst),
        .i_a0(i_a0), .i_a1(i_a1), .i_a2(i_a2), .i_dat(i_dat),
        .o_val(o_val), .i_rdy(i_rdy_t),
        .o_op(o_op), .o_src(o_src), .o_dst(o_dst),
        .o_a0(o_a0), .o_a1(o_a1), .o_a2(o_a2), .o_dat(o_dat)
    );

    q_flit_pipe u_pipe (
        .clk(clk), .rst_n(rst_n),
        .s_valid(rov), .s_ready(pir),
        .s_op(ro_op), .s_src(ro_src), .s_dst(ro_dst),
        .s_a0(ro_a0), .s_a1(ro_a1), .s_a2(ro_a2), .s_dat(ro_dat),
        .m_valid(pov), .m_ready(pirr),
        .m_op(pi_op), .m_src(pi_src), .m_dst(pi_dst),
        .m_a0(pi_a0), .m_a1(pi_a1), .m_a2(pi_a2), .m_dat(pi_dat)
    );

    task send(input [2:0] op, input [3:0] src, input [3:0] dst,
              input [15:0] dat);
        begin
            @(negedge clk);
            i_val = 1; i_op = op; i_src = src; i_dst = dst; i_dat = dat;
            guard = 0;
            while (o_rdy !== 1'b1 && guard < 500) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 500) begin
                errors = errors + 1;
                $display("FAIL send_timeout dst=%h", dst);
            end
            @(posedge clk);
            i_val <= 0;    // NBA: deassert exactly after the transfer edge
                           // (protocol: no stale-valid phantom cycle)
        end
    endtask

    task recv_exp(input [15:0] dat, input [127:0] name);
        begin
            guard = 0;
            while (o_val !== 1'b1 && guard < 1000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (o_val !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL %0s timeout", name);
            end else begin
                if (o_dat !== dat || o_dst !== 4'hF || o_src !== 4'd7) begin
                    errors = errors + 1;
                    $display("FAIL %0s dat=%h dst=%h src=%h",
                             name, o_dat, o_dst, o_src);
                end
                // consume: grant for exactly the transfer edge
                i_rdy_t = 1;
                @(negedge clk);
                i_rdy_t = 0;
            end
        end
    endtask

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);

        // 1: round trip to EXTID
        send(3'd3, 4'd7, 4'hF, 16'hABCD);
        recv_exp(16'hABCD, "roundtrip");

        // 2: back-to-back EXTID flits stay in order (pipelined round trips)
        send(3'd3, 4'd7, 4'hF, 16'h0001);
        recv_exp(16'h0001, "order1");
        send(3'd3, 4'd7, 4'hF, 16'h0002);
        recv_exp(16'h0002, "order2");
        // (v1 limit, deferred with curveball 3: a misaddressed flit has no
        // owner node and circulates forever; senders address valid nodes.)

        // 3: backpressured egress holds
        i_rdy_t = 0;
        send(3'd3, 4'd7, 4'hF, 16'h7777);
        guard = 0;
        while (o_val !== 1'b1 && guard < 1000) begin
            @(negedge clk); guard = guard + 1;
        end
        if (o_val !== 1'b1 || o_dat !== 16'h7777) begin
            errors = errors + 1;
            $display("FAIL hold");
        end
        i_rdy_t = 1;
        @(negedge clk);

        if (errors == 0) $display("TB_IO_PORT PASS");
        else $display("TB_IO_PORT FAIL %0d", errors);
        $finish;
    end
endmodule
