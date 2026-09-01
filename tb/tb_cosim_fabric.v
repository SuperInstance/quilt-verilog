// tb_cosim_fabric.v -- FABRIC-LEVEL differential cosim harness (backend
// lane, the §10/B6 artifact: Python-vs-RTL program diff on the REAL
// q_fabric_top ring, NCELL-parameterized -- scale-up lane 2026-08-31:
// NCELL 2 -> 4/8 via -DNCELL=n, default 4).
//
// Division of labor (honest):
//   * Python (tools/backend/cosim_fabric.py) generates the flit program
//     (op/src/dst/a0/a1/a2/dat + wait-cycles per flit) and, after this
//     TB runs, replays the SAME program through its fabric model and
//     diffs every egress flit bit-for-bit per window.
//   * This TB drives the program into q_fabric_top's external port,
//     captures EVERY egress flit with its window index, and records the
//     per-cell SERVICED-tick event stream (the Q2 interlock latches
//     s_tick into tick_pend and services at ST_IDLE -- pulses arriving
//     mid-service MERGE, so pulse counts are not the truth; serviced
//     counts are. Tick TIMING is scheduler fact fed to the model, not a
//     seam under test: the seam under test is op semantics + ring
//     routing + egress, end to end, on shared stimulus).
//
// Trace format (tb/run/cosim_fabric_trace.txt):
//   W <widx> <cyc> <tc0> ... <tc{NCELL-1}>  cumulative serviced ticks
//                               per cell at each grant (informational;
//                               the model replays the P/T event streams)
//   E <widx> op src dst a0 a1 a2 dat
//                          one egress flit, in arrival order, attributed
//                          to the window of the most recent grant
//   P <cell> <win> <cyc> op src a0 a1 a2 dat
//                          one op acceptance (ci_valid && ci_ready)
//   T <cell> <win> <cyc>   one tick service (ST_TICK entry)
//
// Pacing contract: each flit is granted, then the TB waits its
// wait-cycles AND an egress quiescence margin (64 + 16*NCELL cycles --
// scaled with ring diameter in the scale-up lane), so every
// response/fire lands inside its own window deterministically.
`timescale 1ns/1ps
module tb_cosim_fabric;
`ifndef NCELL
    parameter NCELL = 4;
`else
    parameter NCELL = `NCELL;
`endif
    localparam MAXC  = 16;          // hard cap on supported NCELL
    localparam EVCAP = 16384;       // per-cell event capacity
    localparam QMARG = 64 + 16 * NCELL;

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

    initial begin
        if (NCELL < 1 || NCELL > MAXC) begin
            $display("COSIM FABRIC FAIL: NCELL %0d out of range 1..%0d",
                     NCELL, MAXC);
            $finish;
        end
    end

    q_fabric_top #(.NCELL(NCELL), .TPW(14)) dut (
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

    integer cyc = 0, lasteg = -1000000;
    always @(posedge clk) cyc <= cyc + 1;

    // window counter: increments at each grant
    integer win = 0;
    integer winr = 0;
    always @(posedge clk) winr <= win;

    // ---------------- per-cell core event streams --------------------
    // P: op accepted by the core (ci_valid && ci_ready handshake)
    // T: tick serviced (ST_TICK entry). Cycle+window stamped; the model
    // replays this MEASURED serialization (the grant-time window view
    // cannot see tick-vs-op order while an op is queued behind a tick).
    integer pc [0:MAXC-1];          // per-cell op-acceptance counts
    integer tc [0:MAXC-1];          // per-cell serviced-tick counts
    integer ev_cyc [0:MAXC*EVCAP-1];
    integer ev_win [0:MAXC*EVCAP-1];
    integer ev_op  [0:MAXC*EVCAP-1];
    integer ev_src [0:MAXC*EVCAP-1];
    integer ev_a0  [0:MAXC*EVCAP-1];
    integer ev_a1  [0:MAXC*EVCAP-1];
    integer ev_a2  [0:MAXC*EVCAP-1];
    integer ev_dat [0:MAXC*EVCAP-1];
    integer t_cyc [0:MAXC*EVCAP-1];
    integer t_win [0:MAXC*EVCAP-1];
    reg [4:0] pst  [0:MAXC-1];

    integer ii;
    initial begin
        for (ii = 0; ii < MAXC; ii = ii + 1) begin
            pc[ii] = 0; tc[ii] = 0; pst[ii] = 5'd0;
        end
    end

    genvar g;
    generate
        for (g = 0; g < NCELL; g = g + 1) begin : cap
            // node 0 hangs off conn0 (ring wrap pipe); cells 1..NCELL-1
            // off connc; both wrap the same q_cell -> u_core
            if (g == 0) begin : c0
                always @(posedge clk) begin
                    if (dut.nodes[0].conn0.u_cell.u_core.ci_valid === 1'b1
                        && dut.nodes[0].conn0.u_cell.u_core.ci_ready === 1'b1
                        && pc[0] < EVCAP) begin
                        ev_cyc[0*EVCAP+pc[0]] = cyc; ev_win[0*EVCAP+pc[0]] = winr;
                        ev_op[0*EVCAP+pc[0]] = dut.nodes[0].conn0.u_cell.u_core.ci_op;
                        ev_src[0*EVCAP+pc[0]] = dut.nodes[0].conn0.u_cell.u_core.ci_src;
                        ev_a0[0*EVCAP+pc[0]] = dut.nodes[0].conn0.u_cell.u_core.ci_a0;
                        ev_a1[0*EVCAP+pc[0]] = dut.nodes[0].conn0.u_cell.u_core.ci_a1;
                        ev_a2[0*EVCAP+pc[0]] = dut.nodes[0].conn0.u_cell.u_core.ci_a2;
                        ev_dat[0*EVCAP+pc[0]] = dut.nodes[0].conn0.u_cell.u_core.ci_dat;
                        pc[0] = pc[0] + 1;
                    end
                    if (dut.nodes[0].conn0.u_cell.u_core.state === 5'd14
                        && pst[0] !== 5'd14 && tc[0] < EVCAP) begin
                        t_cyc[0*EVCAP+tc[0]] = cyc; t_win[0*EVCAP+tc[0]] = winr;
                        tc[0] = tc[0] + 1;
                    end
                    pst[0] <= dut.nodes[0].conn0.u_cell.u_core.state;
                end
            end else begin : cn
                always @(posedge clk) begin
                    if (dut.nodes[g].connc.u_cell.u_core.ci_valid === 1'b1
                        && dut.nodes[g].connc.u_cell.u_core.ci_ready === 1'b1
                        && pc[g] < EVCAP) begin
                        ev_cyc[g*EVCAP+pc[g]] = cyc; ev_win[g*EVCAP+pc[g]] = winr;
                        ev_op[g*EVCAP+pc[g]] = dut.nodes[g].connc.u_cell.u_core.ci_op;
                        ev_src[g*EVCAP+pc[g]] = dut.nodes[g].connc.u_cell.u_core.ci_src;
                        ev_a0[g*EVCAP+pc[g]] = dut.nodes[g].connc.u_cell.u_core.ci_a0;
                        ev_a1[g*EVCAP+pc[g]] = dut.nodes[g].connc.u_cell.u_core.ci_a1;
                        ev_a2[g*EVCAP+pc[g]] = dut.nodes[g].connc.u_cell.u_core.ci_a2;
                        ev_dat[g*EVCAP+pc[g]] = dut.nodes[g].connc.u_cell.u_core.ci_dat;
                        pc[g] = pc[g] + 1;
                    end
                    if (dut.nodes[g].connc.u_cell.u_core.state === 5'd14
                        && pst[g] !== 5'd14 && tc[g] < EVCAP) begin
                        t_cyc[g*EVCAP+tc[g]] = cyc; t_win[g*EVCAP+tc[g]] = winr;
                        tc[g] = tc[g] + 1;
                    end
                    pst[g] <= dut.nodes[g].connc.u_cell.u_core.state;
                end
            end
        end
    endgenerate

    // ---------------- egress capture ----------------------------------
    // grant-sampled serviced counts (one per window, 0..nflits)
    integer w_sc [0:MAXC-1];
    integer w_scw [0:8192*MAXC-1];   // [win*MAXC + cell]
    integer w_cyc [0:8192];

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

    integer i, j, r, fd, tfd, tmo, gcyc;
    initial tmo = 40000000;   // cycles; refined after program load

    // private paths (plusargs) so concurrent batteries never share
    // tb/run files; defaults keep the original single-run behaviour
    reg [1023:0] prog_path, trace_path;
    initial begin
        prog_path  = "tb/run/cosim_fabric_prog.hex";
        trace_path = "tb/run/cosim_fabric_trace.txt";
    end

    initial begin
        for (j = 0; j < MAXC; j = j + 1) w_sc[j] = 0;
        if ($value$plusargs("prog=%s", prog_path)) ;
        if ($value$plusargs("trace=%s", trace_path)) ;
        // load the program (hex tokens; wait cycles decimal)
        fd = $fopen(prog_path, "r");
        if (fd == 0) begin
            $display("COSIM FABRIC FAIL: cannot open %0s", prog_path);
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
            for (j = 0; j < NCELL; j = j + 1)
                w_scw[win*MAXC + j] = tc[j];
            w_cyc[win] = cyc;
            win = win + 1;
            @(negedge clk);
            i_val = 0;
            // settle: RELATIVE wait-cycles AND egress quiescence
            gcyc = cyc;
            while ((cyc - gcyc) < p_wait[i] || (cyc - lasteg) < QMARG)
                @(negedge clk);
        end
        // final window sample: any ticks/fires after the last grant
        for (j = 0; j < NCELL; j = j + 1)
            w_scw[win*MAXC + j] = tc[j];
        w_cyc[win] = cyc;
        win = win + 1;
        repeat (QMARG) @(negedge clk);

        // write the trace
        tfd = $fopen(trace_path, "w");
        if (tfd == 0) begin
            $display("COSIM FABRIC FAIL: cannot write trace");
            $finish;
        end
        for (i = 0; i < win; i = i + 1) begin
            $fwrite(tfd, "W %0d %0d", i, w_cyc[i]);
            for (j = 0; j < NCELL; j = j + 1)
                $fwrite(tfd, " %0d", w_scw[i*MAXC + j]);
            $fdisplay(tfd, "");
        end
        for (i = 0; i < ec; i = i + 1)
            $fdisplay(tfd, "E %0d %0d %0d %0d %0d %0d %0d %0d %0d",
                      e_win[i], e_op[i], e_src[i], e_dst[i],
                      e_a0[i], e_a1[i], e_a2[i], e_dat[i], e_cyc[i]);
        for (j = 0; j < NCELL; j = j + 1)
            for (i = 0; i < pc[j]; i = i + 1)
                $fdisplay(tfd, "P %0d %0d %0d %0d %0d %0d %0d %0d %0d",
                          j, ev_win[j*EVCAP+i], ev_cyc[j*EVCAP+i],
                          ev_op[j*EVCAP+i], ev_src[j*EVCAP+i],
                          ev_a0[j*EVCAP+i], ev_a1[j*EVCAP+i],
                          ev_a2[j*EVCAP+i], ev_dat[j*EVCAP+i]);
        for (j = 0; j < NCELL; j = j + 1)
            for (i = 0; i < tc[j]; i = i + 1)
                $fdisplay(tfd, "T %0d %0d %0d", j, t_win[j*EVCAP+i],
                          t_cyc[j*EVCAP+i]);
        $fclose(tfd);

        $write("TB-COSIM-FABRIC DONE: %0d flits, %0d egress flits, %0d windows, NCELL=%0d, events:",
                 nflits, ec, win, NCELL);
        for (j = 0; j < NCELL; j = j + 1)
            $write(" c%0d=%0d(P)+%0d(T)", j, pc[j], tc[j]);
        $write("\n");
        $finish;
    end

    initial begin
        #(tmo * 10);
        $display("COSIM FABRIC FAIL: global timeout (win=%0d ec=%0d)",
                 win, ec);
        $finish;
    end
endmodule
