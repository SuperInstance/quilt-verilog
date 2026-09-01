// tb_tick_flood.v -- TICK-lane quantitative measurement (2026-08-31):
// worst-case tick service latency on the REAL fabric (q_fabric_top)
// under PERMANENT external ingress flood, NCELL-parameterized 2/4/8.
//
// What it measures, per cell, cycle-exact from the RTL's own state:
//   * DEFER latency: scheduler strobe (dut.tick, broadcast) -> ST_TICK
//     entry (state 5'd14) -- how long the pending tick waits behind
//     the in-flight op under flood (the Q2 suppression window).
//   * SERVICE duration: ST_TICK entry -> next ST_IDLE, which includes
//     the decay sweep, leak, fire test and, when the cell fires, the
//     ST_FIRE fanout onto a possibly congested ring.
//   * flood liveness evidence: per-cell op accepts (ci handshake) and
//     fabric egress flits during the flood window, so the reported
//     latencies are certified to have occurred UNDER load, not in an
//     idle fabric the flood failed to reach.
//
// Cells are bound + linked (4 edges each) and dialed to fire often
// (threshold 0x0100, ka small), so tick services carry the full
// worst-case payload: 4-edge sweep + fire fanout into ring traffic.
//
// TB-only hierarchical peeks (cap generate mirrors tb_cosim_fabric.v);
// measurement, not verification -- the proof obligations live in
// formal/f_cell_core_tick.v and docs/TICK-LATENCY.md.
`timescale 1ns/1ps
module tb_tick_flood;
`ifndef NCELL
    parameter NCELL = 4;
`else
    parameter NCELL = `NCELL;
`endif
    parameter TPW = 10;             // strobe every 1024 cycles
    parameter MAXC = 16;

    reg clk = 0;
    always #5 clk = ~clk;

    reg por = 0;
    reg        i_val = 0;
    reg [2:0]  i_op = 0;
    reg [3:0]  i_src = 0, i_dst = 0;
    reg [15:0] i_a0 = 0, i_a1 = 0, i_a2 = 0, i_dat = 0;
    wire       o_rdy;
    wire       o_val;
    wire [2:0] o_op;
    wire [3:0] o_src, o_dst;
    wire [15:0] o_a0, o_a1, o_a2, o_dat;

    q_fabric_top #(.NCELL(NCELL), .TPW(TPW)) dut (
        .clk(clk), .rst_n(por),
        .i_val(i_val), .o_rdy(o_rdy),
        .i_op(i_op), .i_src(i_src), .i_dst(i_dst),
        .i_a0(i_a0), .i_a1(i_a1), .i_a2(i_a2), .i_dat(i_dat),
        .o_val(o_val), .i_rdy(1'b1),
        .o_op(o_op), .o_src(o_src), .o_dst(o_dst),
        .o_a0(o_a0), .o_a1(o_a1), .o_a2(o_a2), .o_dat(o_dat),
        .o_ovf()
    );

    integer cyc = 0;
    always @(posedge clk) cyc <= cyc + 1;

    // ---------------- per-cell monitors ------------------------------
    integer strobe_cyc [0:MAXC-1];   // cycle of last un-serviced strobe
    integer in_tick    [0:MAXC-1];   // service-start cycle
    integer pend       [0:MAXC-1];   // strobe outstanding flag
    integer in_svc     [0:MAXC-1];   // inside tick service (14..TLEAK/FIRE)
    integer tcnt       [0:MAXC-1];   // services completed
    integer dmax       [0:MAXC-1];   // max defer latency
    integer dsmax      [0:MAXC-1];   // max defer+service (strobe->idle)
    integer svmax      [0:MAXC-1];   // max service duration
    integer acc        [0:MAXC-1];   // op accepts under flood
    integer accid      [0:MAXC-1];   // pre-flood (setup) accepts
    integer ecyc;                    // egress count
    reg [4:0] pst [0:MAXC-1];

    genvar g;
    generate
        for (g = 0; g < NCELL; g = g + 1) begin : mon
            wire [4:0] cs = (g == 0) ? dut.nodes[0].conn0.u_cell.u_core.state
                                     : dut.nodes[g].connc.u_cell.u_core.state;
            wire cr = (g == 0) ? dut.nodes[0].conn0.u_cell.u_core.ci_ready
                               : dut.nodes[g].connc.u_cell.u_core.ci_ready;
            wire cv = (g == 0) ? dut.nodes[0].conn0.u_cell.u_core.ci_valid
                               : dut.nodes[g].connc.u_cell.u_core.ci_valid;
            always @(posedge clk) begin
                if (por) begin
                    if (cv && cr)
                        if (flood) acc[g] <= acc[g] + 1;
                        else       accid[g] <= accid[g] + 1;
                    if (dut.tick && pst[g] !== 5'd14 && !pend[g]) begin
                        pend[g] <= 1; strobe_cyc[g] <= cyc;
                    end
                    if (cs === 5'd14 && pst[g] !== 5'd14 && pend[g]) begin
                        in_tick[g] <= cyc;
                        in_svc[g]  <= 1;
                        if (cyc - strobe_cyc[g] > dmax[g])
                            dmax[g] <= cyc - strobe_cyc[g];
                    end
                    if (cs === 5'd2 && pst[g] !== 5'd2 && in_svc[g]) begin
                        // tick-path exit reached IDLE: service complete.
                        // armed at ST_TICK entry, completed from ANY tick
                        // exit state (ST_TLEAK or ST_FIRE both -> ST_IDLE;
                        // ST_RESP is op-only, never entered in service).
                        tcnt[g] <= tcnt[g] + 1;
                        if (cyc - strobe_cyc[g] > dsmax[g])
                            dsmax[g] <= cyc - strobe_cyc[g];
                        if (cyc - in_tick[g] > svmax[g])
                            svmax[g] <= cyc - in_tick[g];
                        pend[g]  <= 0;
                        in_svc[g] <= 0;
                    end
                    pst[g] <= cs;
                end
            end
        end
    endgenerate

    reg flood = 0;
    always @(posedge clk) if (o_val) ecyc <= ecyc + 1;

    // LCG for flood mix (deterministic, seedable)
    reg [31:0] seed = 32'hC0FFEE;
    function [31:0] rnd;
        input [31:0] s;
        begin rnd = (s * 1103515245 + 12345) & 32'h7FFFFFFF; end
    endfunction

    task send_flit(input [2:0] op, input [3:0] src, input [3:0] dst,
                   input [15:0] a0, input [15:0] a1, input [15:0] a2,
                   input [15:0] dat);
        begin
            @(negedge clk);
            i_val = 1; i_op = op; i_src = src; i_dst = dst;
            i_a0 = a0; i_a1 = a1; i_a2 = a2; i_dat = dat;
            while (o_rdy !== 1'b1) @(negedge clk);
            @(posedge clk);
            @(negedge clk);
            i_val = 0;
        end
    endtask

    integer i, j, run, idmax, ismax, ivmax, itot, iacc, iworst, gmax, gsmax, gvmax, gtot;
    integer RUNS;                    // flood cycles (plusarg, default 400k)
    initial RUNS = 400000;
    reg [1023:0] path;
    integer fd;
    initial begin
        if ($value$plusargs("runs=%d", RUNS)) ;
        if ($value$plusargs("seed=%d", seed)) ;
        path = "tb/run/tick_flood.txt";
        if ($value$plusargs("out=%s", path)) ;
        for (i = 0; i < MAXC; i = i + 1) begin
            strobe_cyc[i] = 0; in_tick[i] = 0; pend[i] = 0; in_svc[i] = 0;
            tcnt[i] = 0;
            dmax[i] = 0; dsmax[i] = 0; svmax[i] = 0; acc[i] = 0; accid[i] = 0;
            pst[i] = 5'd0;
        end
        ecyc = 0;

        repeat (8) @(negedge clk);
        por = 1;
        repeat (16) @(negedge clk);

        // ---- setup: bind + link 4 edges per cell, dial fire-friendly ----
        // dial map per rtl/q_dialfile.v: 4=ka, 5=thresh, 6=refr
        for (i = 0; i < NCELL; i = i + 1) begin
            send_flit(3'd0, 4'hF, i[3:0], i[15:0], 16'd0, 16'd0, 16'd0);       // bind id=i
            send_flit(3'd0, 4'hF, i[3:0], 16'd4, 16'd2, 16'd0, 16'd0);        // dial4 ka=2
            send_flit(3'd0, 4'hF, i[3:0], 16'd5, 16'h0100, 16'd0, 16'd0);     // dial5 thresh lo
            send_flit(3'd0, 4'hF, i[3:0], 16'd6, 16'd1, 16'd0, 16'd0);        // dial6 refr=1
            for (j = 0; j < 4; j = j + 1) begin
                send_flit(3'd1, ((i + 1) % NCELL), i[3:0], j[15:0], 16'h3000, // link slot j
                          16'd0, 16'd0);                                      // peer=(i+1)%N
            end
        end
        repeat (64) @(negedge clk);

        // ---- FLOOD: continuous ingress, never back off ------------------
        flood = 1;
        run = 0;
        while (run < RUNS) begin
            @(negedge clk);
            i_val = 1;
            i_src = 4'hF;
            i_dst = seed[3:0] % NCELL;
            seed  = rnd(seed);
            case (seed[2:0])
              3'd0, 3'd1: i_op = 3'd2;                       // EFFECT (heavy)
              3'd2, 3'd3: i_op = 3'd2;
              3'd4:       i_op = 3'd3; i_a0 = 16'd1;         // view(1): heaviest op
              3'd5:       i_op = 3'd3; i_a0 = 16'd0;
              3'd6:       i_op = 3'd2;
              default:    i_op = 3'd3; i_a0 = 16'd2;         // view dial
            endcase
            i_a1 = seed[15:0]; i_a2 = seed[15:0];
            i_dat = seed[15:0] & 16'h3FFF;                   // sizeable payloads
            seed = rnd(seed);
            if (o_rdy === 1'b1) run = run + 1;               // count accepted flits
        end
        i_val = 0;
        repeat (2048) @(negedge clk);      // drain: service any last strobe

        // ---- report -----------------------------------------------------
        fd = $fopen(path, "w");
        $display("TICK FLOOD NCELL=%0d TPW=%0d flits=%0d egress=%0d",
                 NCELL, TPW, RUNS, ecyc);
        idmax = 0; ismax = 0; ivmax = 0; itot = 0; iacc = 0; iworst = -1;
        for (i = 0; i < NCELL; i = i + 1) begin
            $display("  cell %0d: serviced=%0d defer_max=%0d service_max=%0d strobe2idle_max=%0d accepts=%0d",
                     i, tcnt[i], dmax[i], svmax[i], dsmax[i], acc[i]);
            $fwrite(fd, "cell %0d serviced %0d defer_max %0d service_max %0d s2i_max %0d accepts %0d\n",
                    i, tcnt[i], dmax[i], svmax[i], dsmax[i], acc[i]);
            if (dmax[i]  > idmax)  begin idmax  = dmax[i];  iworst = i; end
            if (svmax[i] > ismax)  ismax  = svmax[i];
            if (dsmax[i] > ivmax)  ivmax  = dsmax[i];
            itot = itot + tcnt[i];
            iacc = iacc + acc[i];
        end
        $display("TICK FLOOD RESULT NCELL=%0d: ticks_serviced=%0d defer_max=%0d (cell %0d) service_max=%0d strobe2idle_max=%0d accepts_under_flood=%0d egress=%0d",
                 NCELL, itot, idmax, iworst, ismax, ivmax, iacc, ecyc);
        $fwrite(fd, "RESULT NCELL=%0d ticks=%0d defer_max=%0d service_max=%0d s2i_max=%0d accepts=%0d egress=%0d\n",
                NCELL, itot, idmax, ismax, ivmax, iacc, ecyc);
        $fclose(fd);
        $finish;
    end
endmodule
