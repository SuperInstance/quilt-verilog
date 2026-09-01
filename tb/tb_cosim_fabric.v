// tb_cosim_fabric.v -- FABRIC-LEVEL differential cosim harness (backend
// lane, the §10/B6 artifact: small-scale Python-vs-RTL program diff on
// the REAL q_fabric_top ring, NCELL=2).
//
// Division of labor (honest):
//   * Python (tools/backend/cosim_fabric.py) generates the flit program
//     (op/src/dst/a0/a1/a2/dat + wait-cycles per flit) and, after this
//     TB runs, replays the SAME program through its fabric model and
//     diffs every egress flit bit-for-bit per window.
//   * This TB drives the program into q_fabric_top's external port,
//     captures EVERY egress flit with its window index, and measures
//     the per-cell SERVICED-tick counts at each grant (the Q2 interlock
//     latches s_tick into tick_pend and services at ST_IDLE -- pulses
//     arriving mid-service MERGE, so pulse counts are not the truth;
//     serviced counts are. Tick TIMING is scheduler fact fed to the
//     model, not a seam under test: the seam under test is op semantics
//     + ring routing + egress, end to end, on shared stimulus).
//
// Trace format (tb/run/cosim_fabric_trace.txt):
//   W <widx> <tc0> <tc1> <cyc>  cumulative serviced ticks per cell at
//                               each grant (informational; the model
//                               replays the P/T event streams instead)
//   E <widx> op src dst a0 a1 a2 dat
//                          one egress flit, in arrival order, attributed
//                          to the window of the most recent grant
//
// Pacing contract: each flit is granted, then the TB waits its
// wait-cycles AND a 64-cycle egress quiescence margin, so every
// response/fire lands inside its own window deterministically.
`timescale 1ns/1ps
module tb_cosim_fabric;
    reg clk = 0;
    always #5 clk = ~clk;

    integer errors = 0;

    // ---------------- DUT: the real parallel fabric -------------------
    reg por = 0;
    reg         i_val = 0;
    reg  [2:0]  i_op = 0;
    reg  [3:0]  i_src = 0, i_dst = 0;
    reg  [15:0] i_a0 = 0, i_a1 = 0, i_a2 = 0, i_dat = 0;
    wire        o_rdy;
    wire        o_val;
    wire [2:0]  o_op;
    wire [3:0]  o_src, o_dst;
    wire [15:0] o_a0, o_a1, o_a2, o_dat;

    q_fabric_top #(.NCELL(2), .TPW(14)) dut (
        .clk(clk), .rst_n(por),
        .i_val(i_val), .o_rdy(o_rdy),
        .i_op(i_op), .i_src(i_src), .i_dst(i_dst),
        .i_a0(i_a0), .i_a1(i_a1), .i_a2(i_a2), .i_dat(i_dat),
        .o_val(o_val), .i_rdy(1'b1),
        .o_op(o_op), .o_src(o_src), .o_dst(o_dst),
        .o_a0(o_a0), .o_a1(o_a1), .o_a2(o_a2), .o_dat(o_dat),
        .o_ovf()
    );

    // ---------------- program memory ----------------------------------
    integer nflits = 0;
    reg [2:0]  p_op   [0:8191];
    reg [3:0]  p_src  [0:8191], p_dst [0:8191];
    reg [15:0] p_a0   [0:8191], p_a1 [0:8191], p_a2 [0:8191], p_dat [0:8191];
    integer    p_wait [0:8191];

    integer cyc = 0, lasteg = -1000;
    always @(posedge clk) cyc <= cyc + 1;

    // window counter: increments at each grant
    integer win = 0;
    integer winr = 0;
    always @(posedge clk) winr <= win;

    // ---------------- per-cell core event streams --------------------
    // P: op accepted by the core (ci_valid && ci_ready_w handshake)
    // T: tick serviced (ST_TICK entry). Cycle+window stamped; the model
    // replays this MEASURED serialization (the grant-time window view
    // cannot see tick-vs-op order while an op is queued behind a tick).
    integer pc0 = 0, pc1 = 0, tc0c = 0, tc1c = 0;
    integer p_cyc0 [0:16383], p_cyc1 [0:16383];
    integer p_win0 [0:16383], p_win1 [0:16383];
    integer p_op0  [0:16383], p_op1  [0:16383];
    integer p_src0 [0:16383], p_src1 [0:16383];
    integer p_a00  [0:16383], p_a01  [0:16383];
    integer p_a10  [0:16383], p_a11  [0:16383];
    integer p_a20  [0:16383], p_a21  [0:16383];
    integer p_dat0 [0:16383], p_dat1 [0:16383];
    integer t_cyc0 [0:16383], t_cyc1 [0:16383];
    integer t_win0 [0:16383], t_win1 [0:16383];
    reg [4:0] pst0 = 5'd0, pst1 = 5'd0;

    always @(posedge clk) begin
        if (dut.nodes[0].conn0.u_cell.u_core.ci_valid === 1'b1 &&
            dut.nodes[0].conn0.u_cell.u_core.ci_ready === 1'b1) begin
            p_cyc0[pc0] = cyc; p_win0[pc0] = winr;
            p_op0[pc0] = dut.nodes[0].conn0.u_cell.u_core.ci_op;
            p_src0[pc0] = dut.nodes[0].conn0.u_cell.u_core.ci_src;
            p_a00[pc0] = dut.nodes[0].conn0.u_cell.u_core.ci_a0;
            p_a10[pc0] = dut.nodes[0].conn0.u_cell.u_core.ci_a1;
            p_a20[pc0] = dut.nodes[0].conn0.u_cell.u_core.ci_a2;
            p_dat0[pc0] = dut.nodes[0].conn0.u_cell.u_core.ci_dat;
            pc0 = pc0 + 1;
        end
        if (dut.nodes[1].connc.u_cell.u_core.ci_valid === 1'b1 &&
            dut.nodes[1].connc.u_cell.u_core.ci_ready === 1'b1) begin
            p_cyc1[pc1] = cyc; p_win1[pc1] = winr;
            p_op1[pc1] = dut.nodes[1].connc.u_cell.u_core.ci_op;
            p_src1[pc1] = dut.nodes[1].connc.u_cell.u_core.ci_src;
            p_a01[pc1] = dut.nodes[1].connc.u_cell.u_core.ci_a0;
            p_a11[pc1] = dut.nodes[1].connc.u_cell.u_core.ci_a1;
            p_a21[pc1] = dut.nodes[1].connc.u_cell.u_core.ci_a2;
            p_dat1[pc1] = dut.nodes[1].connc.u_cell.u_core.ci_dat;
            pc1 = pc1 + 1;
        end
        if (dut.nodes[0].conn0.u_cell.u_core.state === 5'd14 && pst0 !== 5'd14) begin
            t_cyc0[tc0c] = cyc; t_win0[tc0c] = winr;
            tc0c = tc0c + 1;
        end
        if (dut.nodes[1].connc.u_cell.u_core.state === 5'd14 && pst1 !== 5'd14) begin
            t_cyc1[tc1c] = cyc; t_win1[tc1c] = winr;
            tc1c = tc1c + 1;
        end
    end

    // ---------------- egress capture ----------------------------------
    // grant-sampled serviced counts (one per window, 0..nflits)
    integer w_sc0 [0:8192];
    integer w_sc1 [0:8192];
    integer w_cyc  [0:8192];

    integer ec = 0;
    integer e_win  [0:16383];
    integer e_cyc  [0:16383];
    reg [2:0]  e_op  [0:16383];
    reg [3:0]  e_src [0:16383], e_dst [0:16383];
    reg [15:0] e_a0  [0:16383], e_a1 [0:16383], e_a2 [0:16383], e_dat [0:16383];
    always @(posedge clk) if (o_val && 1'b1) begin
        if (ec < 16383) begin
            e_op[ec] = o_op; e_src[ec] = o_src; e_dst[ec] = o_dst;
            e_a0[ec] = o_a0; e_a1[ec] = o_a1; e_a2[ec] = o_a2;
            e_dat[ec] = o_dat; e_win[ec] = win; e_cyc[ec] = cyc;
        end
        ec = ec + 1;
        lasteg = cyc;
    end

    integer i, r, fd, tfd, tmo, tmpi, gcyc;
    initial tmo = 40000000;   // cycles; refined after program load

    initial begin
        // load the program (hex tokens; wait cycles decimal)
        fd = $fopen("tb/run/cosim_fabric_prog.hex", "r");
        if (fd == 0) begin
            $display("COSIM FABRIC FAIL: cannot open tb/run/cosim_fabric_prog.hex");
            $finish;
        end
        r = $fscanf(fd, "%d", nflits);
        if (r != 1 || nflits <= 0 || nflits > 8192) begin
            $display("COSIM FABRIC FAIL: bad program header");
            $finish;
        end
        tmo = 200000;
        for (i = 0; i < nflits; i = i + 1) begin
            r = $fscanf(fd, "%h %h %h %h %h %h %h %d",
                        p_op[i], p_src[i], p_dst[i], p_a0[i], p_a1[i],
                        p_a2[i], p_dat[i], p_wait[i]);
            if (r != 8) begin
                $display("COSIM FABRIC FAIL: program truncated at %0d", i);
                $finish;
            end
            tmo = tmo + p_wait[i] + 4000;
        end
        $fclose(fd);

        repeat (8) @(negedge clk);
        por = 1;
        repeat (8) @(negedge clk);

        // drive the program
        for (i = 0; i < nflits; i = i + 1) begin
            @(negedge clk);
            i_val = 1; i_op = p_op[i]; i_src = p_src[i]; i_dst = p_dst[i];
            i_a0 = p_a0[i]; i_a1 = p_a1[i]; i_a2 = p_a2[i]; i_dat = p_dat[i];
            while (o_rdy !== 1'b1) @(negedge clk);
            @(posedge clk);              // grant edge
            w_sc0[win] = tc0c; w_sc1[win] = tc1c; w_cyc[win] = cyc;
            win = win + 1;
            @(negedge clk);
            i_val = 0;
            // settle: RELATIVE wait-cycles AND egress quiescence
            gcyc = cyc;
            while ((cyc - gcyc) < p_wait[i] || (cyc - lasteg) < 64)
                @(negedge clk);
        end
        // final window sample: any ticks/fires after the last grant
        w_sc0[win] = tc0c; w_sc1[win] = tc1c; w_cyc[win] = cyc;
        win = win + 1;
        repeat (64) @(negedge clk);

        // write the trace
        tfd = $fopen("tb/run/cosim_fabric_trace.txt", "w");
        if (tfd == 0) begin
            $display("COSIM FABRIC FAIL: cannot write trace");
            $finish;
        end
        for (i = 0; i < win; i = i + 1)
            $fdisplay(tfd, "W %0d %0d %0d %0d", i, w_sc0[i], w_sc1[i], w_cyc[i]);
        for (i = 0; i < ec; i = i + 1)
            $fdisplay(tfd, "E %0d %0d %0d %0d %0d %0d %0d %0d %0d",
                      e_win[i], e_op[i], e_src[i], e_dst[i],
                      e_a0[i], e_a1[i], e_a2[i], e_dat[i], e_cyc[i]);
        for (i = 0; i < pc0; i = i + 1)
            $fdisplay(tfd, "P 0 %0d %0d %0d %0d %0d %0d %0d %0d",
                      p_win0[i], p_cyc0[i], p_op0[i], p_src0[i],
                      p_a00[i], p_a10[i], p_a20[i], p_dat0[i]);
        for (i = 0; i < pc1; i = i + 1)
            $fdisplay(tfd, "P 1 %0d %0d %0d %0d %0d %0d %0d %0d",
                      p_win1[i], p_cyc1[i], p_op1[i], p_src1[i],
                      p_a01[i], p_a11[i], p_a21[i], p_dat1[i]);
        for (i = 0; i < tc0c; i = i + 1)
            $fdisplay(tfd, "T 0 %0d %0d", t_win0[i], t_cyc0[i]);
        for (i = 0; i < tc1c; i = i + 1)
            $fdisplay(tfd, "T 1 %0d %0d", t_win1[i], t_cyc1[i]);
        $fclose(tfd);

        $display("TB-COSIM-FABRIC DONE: %0d flits, %0d egress flits, %0d windows, events c0=%0d(P)+%0d(T) c1=%0d(P)+%0d(T)",
                 nflits, ec, win, pc0, tc0c, pc1, tc1c);
        $finish;
    end

    initial begin
        #(tmo * 10);
        $display("COSIM FABRIC FAIL: global timeout (win=%0d ec=%0d)",
                 win, ec);
        $finish;
    end
endmodule
