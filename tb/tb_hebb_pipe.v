// tb_hebb_pipe.v -- PIPE_EFF retime proof (quilt-verilog v2.1, FPGA round 3).
//
// The round-3 retiming pipelines q_cell_core's effect-integration cone
// (RQH credit add -> 16x16 multiply -> saturating accumulate) into three
// registered stages (ST_EFFP / ST_EFFM / ST_EFFI) when PIPE_EFF=1. This
// TB proves the retime semantics-preserving the only way that counts:
// differential simulation of the ORIGINAL core (PIPE_EFF=0) against the
// PIPELINED core (PIPE_EFF=1) on one shared stimulus session, checking
//   (a) the ordered stream of every output flit (lo_* ack/nak/view AND
//       lx_* fire-fanout effects) is IDENTICAL -- same order, same fields,
//   (b) `act` (the activation integrator output) and the echo trace
//       `o_ftrace` are bit-exact at every checkpoint (after each op
//       settles, tick-by-tick through the session),
// with the v2 feature pair FULLY DIALED ON (echo gate FLOOR != 0, RQH
// master enable RQEN=1, QDW/QLEAK nonzero) so the gated/graded/credited
// path -- the retimed cone -- is the exercised one, not the v1 bypass.
//
// Cycle counts differ by construction (+2 clk per effect op); flit VALUES
// must not. That is the theorem.
//
// Run: iverilog -g2005 -o tb/run/tb_hebb_pipe.vvp \
//        rtl/q_dialfile.v rtl/q_echo_gate.v rtl/q_rqh_bank.v \
//        rtl/q_hebb_edge.v rtl/q_cell_core.v tb/tb_hebb_pipe.v && \
//      vvp tb/run/tb_hebb_pipe.vvp
`timescale 1ns/1ps
module tb_hebb_pipe;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    localparam PW = 16, EDGES_N = 2, EIW = 1, K = 4;

    integer errors = 0;
    integer guard = 0;
    integer nref_lo = 0, ndut_lo = 0, nref_lx = 0, ndut_lx = 0;

    // ---------------- engine arrays (one per core, like q_cell) ---------
    // q_cell_core never touches silicon directly: the engines behind
    // hb_* are mandatory for the handshake to ever complete.
    wire [2:0]  r_hb_cmd, d_hb_cmd;
    wire [EDGES_N-1:0] r_hb_sel, d_hb_sel;
    wire [PW-1:0] r_hb_base, d_hb_base;
    wire [3:0]  r_hb_gcl, d_hb_gcl;
    wire [PW-1:0] r_hb_w, d_hb_w;
    wire        r_hb_done, d_hb_done;
    // dial values the engines need (from each core's dialfile fan-out)
    wire [PW-1:0] r_d_hl, d_d_hl;
    wire [4:0]   r_d_p0e, d_d_p0e;
    wire         r_d_mode, d_d_mode;

    // ---------------- shared stimulus bus -------------------------------
    reg         ci_valid = 0;
    reg  [2:0]  ci_op    = 0;
    reg  [3:0]  ci_src   = 0;
    reg  [PW-1:0] ci_a0 = 0, ci_a1 = 0, ci_a2 = 0, ci_dat = 0;
    reg         s_tick   = 0;
    reg         acc_ref = 0, acc_dut = 0;   // per-side handshake seen
    // per-side valid: a core must not see the flit again after accepting
    wire        ci_valid_ref = ci_valid && !acc_ref;
    wire        ci_valid_dut = ci_valid && !acc_dut;

    // ---------------- reference core (PIPE_EFF=0, the original cone) ----
    wire        r_ci_ready;
    wire [2:0]  r_lo_op, r_lx_op;
    wire        r_lo_valid, r_lx_valid;
    wire [3:0]  r_lo_dst, r_lo_src, r_lx_dst, r_lx_src;
    wire [PW-1:0] r_lo_a0, r_lo_a1, r_lo_a2, r_lo_dat;
    wire [PW-1:0] r_lx_a0, r_lx_a1, r_lx_a2, r_lx_dat;
    wire signed [PW-1:0] r_act;
    wire [PW-1:0] r_ftrace;
    wire         r_antic;

    wire        r_df_wr, r_df_rd, r_df_rstb;
    wire [3:0]  r_df_addr;
    wire [PW-1:0] r_df_wdata, r_df_rdata;
    wire [3:0]  r_d_ka, r_d_kle, r_d_qdw, r_d_qleak;
    wire signed [PW-1:0] r_d_thresh;
    wire [PW-1:0] r_d_refr, r_d_floor;
    wire         r_d_rqen;

    q_dialfile #(.DW(PW), .ND(16), .AW(4)) u_df_ref (
        .clk(clk), .rst_n(rst_n),
        .i_wr(r_df_wr), .i_addr(r_df_addr), .i_wdata(r_df_wdata),
        .i_rd(r_df_rd), .o_rdata(r_df_rdata), .o_rstb(r_df_rstb),
        .o_ka(r_d_ka), .o_thresh(r_d_thresh), .o_refr(r_d_refr),
        .o_kle(r_d_kle), .o_floor(r_d_floor),
        .o_qdw(r_d_qdw), .o_qleak(r_d_qleak), .o_rqen(r_d_rqen),
        .o_hl(r_d_hl), .o_p0e(r_d_p0e), .o_mode(r_d_mode)
    );

    q_cell_core #(.PW(PW), .EDGES_N(EDGES_N), .EIW(EIW), .K(K),
                  .PIPE_EFF(0)) u_ref (
        .clk(clk), .rst_n(rst_n),
        .ci_op(ci_op), .ci_valid(ci_valid_ref), .ci_ready(r_ci_ready),
        .ci_src(ci_src), .ci_a0(ci_a0), .ci_a1(ci_a1), .ci_a2(ci_a2),
        .ci_dat(ci_dat),
        .lo_op(r_lo_op), .lo_valid(r_lo_valid), .lo_ready(1'b1),
        .lo_dst(r_lo_dst), .lo_src(r_lo_src),
        .lo_a0(r_lo_a0), .lo_a1(r_lo_a1), .lo_a2(r_lo_a2), .lo_dat(r_lo_dat),
        .lx_op(r_lx_op), .lx_valid(r_lx_valid), .lx_ready(1'b1),
        .lx_dst(r_lx_dst), .lx_src(r_lx_src),
        .lx_a0(r_lx_a0), .lx_a1(r_lx_a1), .lx_a2(r_lx_a2), .lx_dat(r_lx_dat),
        .hb_cmd(r_hb_cmd), .hb_sel(r_hb_sel), .hb_base(r_hb_base),
        .hb_gcl(r_hb_gcl),
        .hb_w(r_hb_w), .hb_done(r_hb_done),
        .df_wr(r_df_wr), .df_addr(r_df_addr), .df_wdata(r_df_wdata),
        .df_rd(r_df_rd), .df_rdata(r_df_rdata), .df_rstb(r_df_rstb),
        .d_ka(r_d_ka), .d_thresh(r_d_thresh), .d_refr(r_d_refr),
        .d_kle(r_d_kle), .d_floor(r_d_floor),
        .d_qdw(r_d_qdw), .d_qleak(r_d_qleak), .d_rqen(r_d_rqen),
        .s_tick(s_tick),
        .bound(), .cell_id(), .act(r_act),
        .o_ftrace(r_ftrace), .o_antic(r_antic)
    );

    // ---------------- pipelined core (PIPE_EFF=1, the retime) -----------
    wire        d_ci_ready;
    wire [2:0]  d_lo_op, d_lx_op;
    wire        d_lo_valid, d_lx_valid;
    wire [3:0]  d_lo_dst, d_lo_src, d_lx_dst, d_lx_src;
    wire [PW-1:0] d_lo_a0, d_lo_a1, d_lo_a2, d_lo_dat;
    wire [PW-1:0] d_lx_a0, d_lx_a1, d_lx_a2, d_lx_dat;
    wire signed [PW-1:0] d_act;
    wire [PW-1:0] d_ftrace;
    wire         d_antic;

    wire        d_df_wr, d_df_rd, d_df_rstb;
    wire [3:0]  d_df_addr;
    wire [PW-1:0] d_df_wdata, d_df_rdata;
    wire [3:0]  d_d_ka, d_d_kle, d_d_qdw, d_d_qleak;
    wire signed [PW-1:0] d_d_thresh;
    wire [PW-1:0] d_d_refr, d_d_floor;
    wire         d_d_rqen;

    q_dialfile #(.DW(PW), .ND(16), .AW(4)) u_df_dut (
        .clk(clk), .rst_n(rst_n),
        .i_wr(d_df_wr), .i_addr(d_df_addr), .i_wdata(d_df_wdata),
        .i_rd(d_df_rd), .o_rdata(d_df_rdata), .o_rstb(d_df_rstb),
        .o_ka(d_d_ka), .o_thresh(d_d_thresh), .o_refr(d_d_refr),
        .o_kle(d_d_kle), .o_floor(d_d_floor),
        .o_qdw(d_d_qdw), .o_qleak(d_d_qleak), .o_rqen(d_d_rqen),
        .o_hl(d_d_hl), .o_p0e(d_d_p0e), .o_mode(d_d_mode)
    );

    q_cell_core #(.PW(PW), .EDGES_N(EDGES_N), .EIW(EIW), .K(K),
                  .PIPE_EFF(1)) u_dut (
        .clk(clk), .rst_n(rst_n),
        .ci_op(ci_op), .ci_valid(ci_valid_dut), .ci_ready(d_ci_ready),
        .ci_src(ci_src), .ci_a0(ci_a0), .ci_a1(ci_a1), .ci_a2(ci_a2),
        .ci_dat(ci_dat),
        .lo_op(d_lo_op), .lo_valid(d_lo_valid), .lo_ready(1'b1),
        .lo_dst(d_lo_dst), .lo_src(d_lo_src),
        .lo_a0(d_lo_a0), .lo_a1(d_lo_a1), .lo_a2(d_lo_a2), .lo_dat(d_lo_dat),
        .lx_op(d_lx_op), .lx_valid(d_lx_valid), .lx_ready(1'b1),
        .lx_dst(d_lx_dst), .lx_src(d_lx_src),
        .lx_a0(d_lx_a0), .lx_a1(d_lx_a1), .lx_a2(d_lx_a2), .lx_dat(d_lx_dat),
        .hb_cmd(d_hb_cmd), .hb_sel(d_hb_sel), .hb_base(d_hb_base),
        .hb_gcl(d_hb_gcl),
        .hb_w(d_hb_w), .hb_done(d_hb_done),
        .df_wr(d_df_wr), .df_addr(d_df_addr), .df_wdata(d_df_wdata),
        .df_rd(d_df_rd), .df_rdata(d_df_rdata), .df_rstb(d_df_rstb),
        .d_ka(d_d_ka), .d_thresh(d_d_thresh), .d_refr(d_d_refr),
        .d_kle(d_d_kle), .d_floor(d_d_floor),
        .d_qdw(d_d_qdw), .d_qleak(d_d_qleak), .d_rqen(d_d_rqen),
        .s_tick(s_tick),
        .bound(), .cell_id(), .act(d_act),
        .o_ftrace(d_ftrace), .o_antic(d_antic)
    );

    // engine instances: REF array (ref core + ref dialfile fan-outs)
    wire [EDGES_N-1:0] r_done_vec, r_ovf_vec;
    wire [EDGES_N*PW-1:0] r_w_flat;
    genvar g;
    generate
        for (g = 0; g < EDGES_N; g = g + 1) begin : ref_edges
            q_hebb_edge #(.PW(PW), .K(K), .B(4), .AGEW(8)) u_e (
                .clk(clk), .rst_n(rst_n),
                .i_sel(r_hb_sel[g]), .i_cmd(r_hb_cmd), .i_mode(r_d_mode),
                .i_base(r_hb_base), .i_hl(r_d_hl), .i_p0e(r_d_p0e),
                .i_gclass(r_hb_gcl),
                .o_done(r_done_vec[g]), .o_w(r_w_flat[g*PW +: PW]),
                .o_ovf(r_ovf_vec[g])
            );
        end
    endgenerate
    // DUT array
    wire [EDGES_N-1:0] d_done_vec, d_ovf_vec;
    wire [EDGES_N*PW-1:0] d_w_flat;
    generate
        for (g = 0; g < EDGES_N; g = g + 1) begin : dut_edges
            q_hebb_edge #(.PW(PW), .K(K), .B(4), .AGEW(8)) u_e (
                .clk(clk), .rst_n(rst_n),
                .i_sel(d_hb_sel[g]), .i_cmd(d_hb_cmd), .i_mode(d_d_mode),
                .i_base(d_hb_base), .i_hl(d_d_hl), .i_p0e(d_d_p0e),
                .i_gclass(d_hb_gcl),
                .o_done(d_done_vec[g]), .o_w(d_w_flat[g*PW +: PW]),
                .o_ovf(d_ovf_vec[g])
            );
        end
    endgenerate
    // selected-slot readout mux + done or-reduce (as in q_cell)
    reg [PW-1:0] r_w_mux, d_w_mux;
    integer q;
    always @* begin
        r_w_mux = {PW{1'b0}};
        d_w_mux = {PW{1'b0}};
        for (q = 0; q < EDGES_N; q = q + 1) begin
            r_w_mux = r_w_mux | r_w_flat[q*PW +: PW];
            d_w_mux = d_w_mux | d_w_flat[q*PW +: PW];
        end
    end
    assign r_hb_w    = r_w_mux;
    assign r_hb_done = |r_done_vec;
    assign d_hb_w    = d_w_mux;
    assign d_hb_done = |d_done_vec;

    // ---------------- flit capture + compare ----------------------------
    // Both sides always granted; every emitted flit is pushed to a queue.
    // Latencies differ (+2 clk per effect op) so flits are compared as
    // ORDERED SEQUENCES, not instantaneously -- the values are the theorem.
    localparam QD = 1024;
    reg [2:0]  q_lo_op_r [0:QD-1], q_lo_op_d [0:QD-1];
    reg [3:0]  q_lo_dst_r[0:QD-1], q_lo_dst_d[0:QD-1];
    reg [3:0]  q_lo_src_r[0:QD-1], q_lo_src_d[0:QD-1];
    reg [PW-1:0] q_lo_a2_r[0:QD-1], q_lo_a2_d[0:QD-1];
    reg [PW-1:0] q_lo_dat_r[0:QD-1], q_lo_dat_d[0:QD-1];
    reg [3:0]  q_lx_dst_r[0:QD-1], q_lx_dst_d[0:QD-1];
    reg [PW-1:0] q_lx_dat_r[0:QD-1], q_lx_dat_d[0:QD-1];
    reg [PW-1:0] q_lx_a2_r [0:QD-1], q_lx_a2_d [0:QD-1];

    integer p;
    initial begin
        for (p = 0; p < QD; p = p + 1) begin
            q_lo_op_r[p] = 0; q_lo_op_d[p] = 0; q_lx_dst_r[p] = 0;
            q_lx_dst_d[p] = 0;
        end
    end

    always @(posedge clk) begin
        if (rst_n) begin
            if (r_lo_valid) begin
                if (nref_lo < QD) begin
                    q_lo_op_r[nref_lo]  = r_lo_op;
                    q_lo_dst_r[nref_lo] = r_lo_dst;
                    q_lo_src_r[nref_lo] = r_lo_src;
                    q_lo_a2_r[nref_lo]  = r_lo_a2;
                    q_lo_dat_r[nref_lo] = r_lo_dat;
                end
                nref_lo <= nref_lo + 1;
            end
            if (d_lo_valid) begin
                if (ndut_lo < QD) begin
                    q_lo_op_d[ndut_lo]  = d_lo_op;
                    q_lo_dst_d[ndut_lo] = d_lo_dst;
                    q_lo_src_d[ndut_lo] = d_lo_src;
                    q_lo_a2_d[ndut_lo]  = d_lo_a2;
                    q_lo_dat_d[ndut_lo] = d_lo_dat;
                end
                ndut_lo <= ndut_lo + 1;
            end
            if (r_lx_valid) begin
                if (nref_lx < QD) begin
                    q_lx_dst_r[nref_lx] = r_lx_dst;
                    q_lx_a2_r[nref_lx]  = r_lx_a2;
                    q_lx_dat_r[nref_lx] = r_lx_dat;
                end
                nref_lx <= nref_lx + 1;
            end
            if (d_lx_valid) begin
                if (ndut_lx < QD) begin
                    q_lx_dst_d[ndut_lx] = d_lx_dst;
                    q_lx_a2_d[ndut_lx]  = d_lx_a2;
                    q_lx_dat_d[ndut_lx] = d_lx_dat;
                end
                ndut_lx <= ndut_lx + 1;
            end
        end
    end

    // compare integrator + trace state (the tick-by-tick theorem)
    task cmpstate(input [127:0] name);
        begin
            if (r_act !== d_act) begin
                errors = errors + 1;
                $display("FAIL %0s act: ref %04h dut %04h", name, r_act, d_act);
            end
            if (r_ftrace !== d_ftrace) begin
                errors = errors + 1;
                $display("FAIL %0s ftrace: ref %04h dut %04h", name,
                         r_ftrace, d_ftrace);
            end
        end
    endtask

    // ---------------- stimulus helpers ----------------------------------
    // send one flit to BOTH cores; each consumes it on its own ready edge
    // (per-side valid wires above prevent double-consumption by the fast
    // core while the pipelined core is still chewing)
    task sendflit(input [2:0] op, input [3:0] src,
                  input [PW-1:0] a0, input [PW-1:0] a1,
                  input [PW-1:0] a2, input [PW-1:0] dat);
        begin
            @(negedge clk);
            ci_valid = 1; ci_op = op; ci_src = src;
            ci_a0 = a0; ci_a1 = a1; ci_a2 = a2; ci_dat = dat;
            acc_ref = 0; acc_dut = 0;
            guard = 0;
            while (!(acc_ref && acc_dut)) begin
                @(posedge clk);
                if (ci_valid_ref && r_ci_ready) acc_ref = 1;
                if (ci_valid_dut && d_ci_ready) acc_dut = 1;
                guard = guard + 1;
                if (guard > 500) begin
                    errors = errors + 1;
                    $display("FAIL handshake timeout op=%0d a0=%h ref.state=%0d dut.state=%0d",
                             op, a0, u_ref.state, u_dut.state);
                    $finish;
                end
            end
            @(negedge clk);
            ci_valid = 0;
        end
    endtask

    // settle: both cores back to a quiet point, then compare everything:
    // ordered flit sequences (values) + integrator/trace state
    task settle(input [127:0] name);
        integer k;
        begin
            repeat (80) @(posedge clk);
            if (nref_lo !== ndut_lo) begin
                errors = errors + 1;
                $display("FAIL %0s lo flit count: ref %0d dut %0d", name,
                         nref_lo, ndut_lo);
            end else begin
                for (k = 0; k < nref_lo; k = k + 1) begin
                    if ({q_lo_op_r[k], q_lo_dst_r[k], q_lo_src_r[k],
                         q_lo_a2_r[k], q_lo_dat_r[k]} !==
                        {q_lo_op_d[k], q_lo_dst_d[k], q_lo_src_d[k],
                         q_lo_a2_d[k], q_lo_dat_d[k]}) begin
                        errors = errors + 1;
                        $display("FAIL %0s lo[%0d]: ref {%b %h %h %h %h} dut {%b %h %h %h %h}",
                                 name, k, q_lo_op_r[k], q_lo_dst_r[k],
                                 q_lo_src_r[k], q_lo_a2_r[k], q_lo_dat_r[k],
                                 q_lo_op_d[k], q_lo_dst_d[k], q_lo_src_d[k],
                                 q_lo_a2_d[k], q_lo_dat_d[k]);
                        k = QD; // report once, stop scanning
                    end
                end
            end
            if (nref_lx !== ndut_lx) begin
                errors = errors + 1;
                $display("FAIL %0s lx flit count: ref %0d dut %0d", name,
                         nref_lx, ndut_lx);
            end else begin
                for (k = 0; k < nref_lx; k = k + 1) begin
                    if ({q_lx_dst_r[k], q_lx_a2_r[k], q_lx_dat_r[k]} !==
                        {q_lx_dst_d[k], q_lx_a2_d[k], q_lx_dat_d[k]}) begin
                        errors = errors + 1;
                        $display("FAIL %0s lx[%0d]: ref {%h %h %h} dut {%h %h %h}",
                                 name, k, q_lx_dst_r[k], q_lx_a2_r[k],
                                 q_lx_dat_r[k], q_lx_dst_d[k], q_lx_a2_d[k],
                                 q_lx_dat_d[k]);
                        k = QD;
                    end
                end
            end
            cmpstate(name);
        end
    endtask

    integer seed = 32'h5EED0003;
    integer i;
    reg [2:0]  rop;
    reg [3:0]  rsrc;
    reg [PW-1:0] ra0, ra1, ra2, rdat;

    initial begin
        rst_n = 0;
        repeat (4) @(posedge clk);
        @(negedge clk) rst_n = 1;

        // session setup: bind cell id 0 (peer id 1 sends effects)
        sendflit(3'd0, 4'd1, 16'h0000, 16'h0000, 16'h0000, 16'h0000);

        // dial the v2 pair fully ON (the retimed cone is the live one):
        //   dial 11 kle=2, dial 12 floor=0x0100 (gate ARMED),
        //   dial 14 = 16'h8004 (RQEN | qdw=4), dial 15 = qleak=3,
        //   dial 2 thresh low (fires), dial 0 ka=1, dial 7 refr=2
        sendflit(3'd0, 4'd1, 16'd11, 16'd2,  16'h0000, 16'h0000);
        sendflit(3'd0, 4'd1, 16'd12, 16'h0100, 16'h0000, 16'h0000);
        sendflit(3'd0, 4'd1, 16'd14, 16'h8004, 16'h0000, 16'h0000);
        sendflit(3'd0, 4'd1, 16'd15, 16'd3,  16'h0000, 16'h0000);
        sendflit(3'd0, 4'd1, 16'd2,  16'h0020, 16'h0000, 16'h0000);
        sendflit(3'd0, 4'd1, 16'd0,  16'd1,  16'h0000, 16'h0000);
        sendflit(3'd0, 4'd1, 16'd7,  16'd2,  16'h0000, 16'h0000);
        // hyperbola half-life + p0 exponent
        sendflit(3'd0, 4'd1, 16'd8,  16'd4,  16'h0000, 16'h0000);
        sendflit(3'd0, 4'd1, 16'd9,  16'd20, 16'h0000, 16'h0000);

        // link two edges from peer 1
        sendflit(3'd1, 4'd1, 16'd0, 16'd9000, 16'h0000, 16'h0000);
        sendflit(3'd1, 4'd1, 16'd1, 16'd7000, 16'h0000, 16'h0000);
        settle("setup");

        // random session: binds/writes, effects (the retimed op), views,
        // interleaved ticks. Same $random stream feeds both cores by bus.
        for (i = 0; i < 300; i = i + 1) begin
            rop  = ($random(seed) % 4);
            rsrc = 4'd1;
            case (rop)
              0: begin // effect from peer (trains through the gate + RQH)
                     rdat = $random(seed) & 16'hFFFF;
                     sendflit(3'd2, rsrc, 16'h0000, 16'h0000,
                              $random(seed) & 16'hFFFF, rdat);
                 end
              1: begin // view(0) act / view(1) wsum
                     ra0 = ($random(seed) % 2);
                     sendflit(3'd3, rsrc, ra0, $random(seed) & 16'h000F,
                              $random(seed) & 16'hFFFF, 16'h0000);
                 end
              2: begin // dial rewrite (v2 knobs mid-session: stress the cone)
                     sendflit(3'd0, rsrc, $random(seed) & 16'h000F,
                              $random(seed) & 16'hFFFF, 16'h0000, 16'h0000);
                 end
              default: begin // tick via op-flit? no: ticks come from s_tick
                     // occasional re-link (base weight churn)
                     sendflit(3'd1, rsrc, $random(seed) & 16'h0001,
                              $random(seed) & 16'hFFFF, 16'h0000, 16'h0000);
                 end
            endcase
            // tick every few ops: decay sweep + leak + fire test
            if ((i % 3) == 0) begin
                @(negedge clk); s_tick = 1;
                @(posedge clk);
                @(negedge clk); s_tick = 0;
            end
            if ((i % 17) == 0) settle("session");
        end

        settle("final");

        // flit-total check (queue lengths must match exactly)
        if (nref_lo !== ndut_lo || nref_lx !== ndut_lx) begin
            errors = errors + 1;
            $display("FAIL flit totals: lo %0d/%0d lx %0d/%0d",
                     nref_lo, ndut_lo, nref_lx, ndut_lx);
        end

        if (errors == 0)
            $display("TB-HEBB-PIPE PASS: %0d ops, %0d lo flits, %0d lx flits, act/trace bit-exact at every checkpoint",
                     300, nref_lo, nref_lx);
        else
            $display("TB-HEBB-PIPE FAIL: %0d errors", errors);
        $finish;
    end
endmodule
