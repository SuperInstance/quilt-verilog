// tb_cosim_fuzz.v -- differential driver (backend lane, Phase 3).
// Replays random/directed op programs from tools/backend/cosim_cell.py
// (tb/run/cosim_fuzz.hex) against the REAL q_cell (PIPE_EFF retime, v2
// dials at POR = off) and compares, after EVERY op:
//   view(0) = act          (bit-exact u16)
//   view(1) = wsum(edges)  (bit-exact u16, saturating)
//   tick fire fanout       (dst,dat multiset, exact)
// Manifest per op:  <op><src><a0:4><a1:4>  then
//                   <v0:4><v1:4><nfire:2>  then nfire x <dst><dat:4>
// a1 means the op's payload operand: dial value / link base / effect dat.
// The TB injects its own view(0)/view(1) flits after each op (views never
// mutate state) and matches their acks; fire fanout leaves as OP_EFF ring
// flits. Loud PASS/FAIL; first mismatch dumps the full context.
`timescale 1ns/1ps
module tb_cosim_fuzz;
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

    localparam [2:0] OP_BIND = 3'd0, OP_LINK = 3'd1, OP_EFF = 3'd2,
                     OP_VIEW = 3'd3, OP_TICK = 3'd4, OP_ACK = 3'd5,
                     OP_NAK = 3'd6;

    integer errors = 0, guard;
    integer fd, r, nprog, pi, nops, oi, ci;
    integer tmpi, op, src;
    reg [15:0] a0, a1;
    reg [15:0] exp_v0, exp_v1;
    integer nfire, fi;
    reg [3:0]  f_dst;
    reg [15:0] f_dat;
    reg [3:0]  exp_fdst [0:63];
    reg [15:0] exp_fdat [0:63];
    // collected fires for the current op
    integer got_nfire;
    reg [3:0]  got_dst [0:63];
    reg [15:0] got_dat [0:63];
    integer ckpts, fires_total, ops_total;
    integer cur_prog, cur_op;

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

    task send(input [2:0] sop, input [3:0] ssrc, input [15:0] sa0,
              input [15:0] sa1);
        begin
            @(negedge clk);
            ri_valid = 1; ri_op = sop; ri_src = ssrc; ri_dst = 4'd1;
            ri_a0 = sa0; ri_a1 = sa1; ri_a2 = 16'd0;
            // a1 is the op's payload operand: effect carries it in dat
            ri_dat = (sop == OP_EFF) ? sa1 : 16'd0;
            guard = 0;
            while (ri_ready !== 1'b1 && guard < 2000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (ri_ready !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL prog %0d op %0d: send timeout (op=%0d)",
                         cur_prog, cur_op, sop);
            end
            @(posedge clk);
            ri_valid <= 0;
        end
    endtask

    // collect one egress flit if valid this cycle (negedge sample)
    task step_collect;
        begin
            if (ro_valid === 1'b1 && ro_ready) begin
                if (ro_op === OP_EFF) begin
                    if (got_nfire < 64) begin
                        got_dst[got_nfire] = ro_dst;
                        got_dat[got_nfire] = ro_dat;
                    end
                    got_nfire = got_nfire + 1;
                end
            end
        end
    endtask

    // wait for the op''s own ack (BIND/LINK/VIEW ack; EFFECT/TICK silent)
    task await_op_ack(input integer needs_ack);
        begin
            guard = 0;
            while (needs_ack && guard < 20000) begin
                @(negedge clk);
                step_collect;
                if (ro_valid === 1'b1 && ro_ready &&
                    (ro_op === OP_ACK || ro_op === OP_NAK))
                    needs_ack = 0;
                guard = guard + 1;
            end
            if (needs_ack) begin
                errors = errors + 1;
                $display("FAIL prog %0d op %0d: op ack timeout",
                         cur_prog, cur_op);
            end
        end
    endtask

    // bounded settle for silent ops (effect integrate, tick sweep+fire)
    task settle(input integer cycles);
        integer k;
        begin
            for (k = 0; k < cycles; k = k + 1) begin
                @(negedge clk);
                step_collect;
            end
        end
    endtask

    // checkpoint: send view(0)/view(1) AFTER the op fully completed, then
    // match their acks in order (strict sequencing, tb_cell_core style)
    task checkpoint(input [15:0] xv0, input [15:0] xv1);
        integer acks;
        begin
            send(OP_VIEW, 4'd0, 16'd0, 16'd0);
            send(OP_VIEW, 4'd0, 16'd1, 16'd0);
            acks = 0;
            guard = 0;
            while (acks < 2 && guard < 20000) begin
                @(negedge clk);
                step_collect;
                if (ro_valid === 1'b1 && ro_ready &&
                    (ro_op === OP_ACK || ro_op === OP_NAK)) begin
                    if (acks === 0) begin
                        ckpts = ckpts + 1;
                        if (ro_dat !== xv0) begin
                            errors = errors + 1;
                            $display("FAIL prog %0d op %0d: view0 %h != %h",
                                     cur_prog, cur_op, ro_dat, xv0);
                        end
                    end else begin
                        ckpts = ckpts + 1;
                        if (ro_dat !== xv1) begin
                            errors = errors + 1;
                            $display("FAIL prog %0d op %0d: view1 %h != %h",
                                     cur_prog, cur_op, ro_dat, xv1);
                        end
                    end
                    acks = acks + 1;
                end
                guard = guard + 1;
            end
            if (acks !== 2) begin
                errors = errors + 1;
                $display("FAIL prog %0d op %0d: view acks timeout",
                         cur_prog, cur_op);
            end
        end
    endtask

    task check_fires;
        integer i, j, found;
        begin
            // read ALL expected pairs first (counts may disagree)
            for (i = 0; i < nfire; i = i + 1) begin
                r = $fscanf(fd, "%h", tmpi);
                f_dst = tmpi[19:16];
                f_dat = tmpi[15:0];
                exp_fdst[i] = f_dst;
                exp_fdat[i] = f_dat;
            end
            if (got_nfire !== nfire) begin
                errors = errors + 1;
                $display("FAIL prog %0d op %0d: %0d fires, expected %0d",
                         cur_prog, cur_op, got_nfire, nfire);
            end else begin
                for (i = 0; i < nfire; i = i + 1) begin
                    found = 0;
                    for (j = 0; j < got_nfire; j = j + 1) begin
                        if (!found && got_dst[j] === exp_fdst[i]
                            && got_dat[j] === exp_fdat[i]) begin
                            found = 1;
                            got_dst[j] = 4'hF;      // burn: 1:1 matching
                            got_dat[j] = 16'hFFFF;
                        end
                    end
                    if (!found) begin
                        errors = errors + 1;
                        $display("FAIL prog %0d op %0d: fire (%0d,%h) missing",
                                 cur_prog, cur_op, exp_fdst[i], exp_fdat[i]);
                    end
                end
            end
            fires_total = fires_total + nfire;
        end
    endtask

    initial begin
        fd = $fopen("tb/run/cosim_fuzz.hex", "r");
        if (fd == 0) begin
            $display("COSIM FAIL: cannot open tb/run/cosim_fuzz.hex (run tools/backend/cosim_cell.py)");
            $finish;
        end
        r = $fscanf(fd, "%h", nprog);
        ckpts = 0; fires_total = 0; ops_total = 0;
        repeat (3) @(negedge clk); rst_n = 1;
        @(negedge clk);

        for (pi = 0; pi < nprog; pi = pi + 1) begin
            cur_prog = pi;
            // fresh cell per program: POR
            rst_n = 0;
            repeat (3) @(negedge clk); rst_n = 1;
            @(negedge clk);
            r = $fscanf(fd, "%h", nops);
            for (oi = 0; oi < nops; oi = oi + 1) begin
                cur_op = oi;
                ops_total = ops_total + 1;
                r = $fscanf(fd, "%h", tmpi);
                op  = (tmpi >> 20) & 3'h7;
                src = (tmpi >> 16) & 4'hF;
                a0  = tmpi[15:0];
                r = $fscanf(fd, "%h", tmpi);
                a1  = tmpi[15:0];
                r = $fscanf(fd, "%h", tmpi);
                exp_v0 = (tmpi >> 16) & 16'hFFFF;
                exp_v1 = tmpi[15:0];
                r = $fscanf(fd, "%h", tmpi);
                nfire = tmpi[7:0];

                got_nfire = 0;
                if (op == OP_TICK) begin
                    @(negedge clk);
                    s_tick = 1;
                    @(negedge clk);
                    s_tick = 0;
                    settle(800);                       // sweep + fanout
                    checkpoint(exp_v0, exp_v1);
                end else if (op == OP_EFF) begin
                    send(op[2:0], src[3:0], a0, a1);
                    settle(400);                       // train+readout+pipe
                    checkpoint(exp_v0, exp_v1);
                end else begin
                    send(op[2:0], src[3:0], a0, a1);
                    await_op_ack(1);
                    checkpoint(exp_v0, exp_v1);
                end
                check_fires;
            end
        end
        if (errors == 0)
            $display("COSIM PASS: %0d programs, %0d ops, %0d view checkpoints, %0d fire events -- Python model == RTL, bit-exact",
                     nprog, ops_total, ckpts, fires_total);
        else
            $display("COSIM FAIL: %0d mismatch(es) over %0d checkpoints",
                     errors, ckpts);
        $fclose(fd);
        $finish;
    end

    initial begin
        #5_000_000_000;
        $display("COSIM FAIL: global timeout");
        $finish;
    end
endmodule
