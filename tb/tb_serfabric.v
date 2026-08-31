// tb_serfabric.v -- DIFFERENTIAL TB for the serialized fabric front-end
// (quilt-verilog v2.1, pin-fix lane; rtl/q_serfabric_top.v).
//
// House pattern: differential TB (tb_hebb_pipe style) -- two fabrics,
// one serialized (DUT-SER: bytes in, bytes out), one parallel (DUT-PAR:
// the wide q_fabric_top flit port, i.e. THE PARALLEL CONFIG PATH),
// driven cycle-locked so their behavior is comparable edge for edge.
//
// CASE A (QUF mode, SER_BOOT_QUF=1):
//   A1 the golden QUF container (tools/quf.py from tb/quf_tb.json, hex
//      image tb/run/quf_tb_input.hex) boots DUT-SER over the 8-bit port;
//      BOTH cells' dialfile rows land BYTE-EXACT vs the container
//      (the §7 broadcast: one quf_boot per cell on one stream), epoch
//      tpw=6 latches once, boot_ok/epoch pulse exactly once, no egress
//      byte escapes while the fabric is frozen.
//   A2 the same dial state is installed on DUT-PAR through the parallel
//      config path (qm_bind flits on the wide port); then a mixed
//      runtime stream (binds, views of all 32 dials, effects, an EXTID
//      echo) flows through BOTH fronts with each flit landing the SAME
//      clock edge (the TB mirrors DUT-SER's wide-ingress grant cycle
//      onto DUT-PAR). Egress streams must match flit-for-flit: same
//      count, same fields, same order, serialized first byte exactly
//      one cycle after the parallel capture edge (the two first-binds
//      skew +2: PAR's cells answer from ST_UNB, SER's are already bound
//      and route ST_BIND first -- documented in the check), pad zero.
//      The 32 mirrored view responses ARE the end-state proof: every
//      dial row byte-exact SER vs PAR (A3 folded in).
// CASE B (gate mode, SER_BOOT_QUF=0): a wrong release word parks sticky
//   in HOLD_ERR (fail-static, err 11, fabric held); POR retry with the
//   word 0x51 0x46 releases with the TPW0 epoch; a double bind (first
//   consumed as the bind, second performs the write) + view round trip
//   through the serial flit path lands and reads back exactly -- the
//   host-parses-QUF mode where dials stream as qm_bind flits.
//
// Protocol notes baked into this TB (found the hard way, kept honest):
//   * dial views are op=VIEW with a0[1:0]=2 (dialfile read), dial
//     index in a1; effects are SILENT (no ACK unless a fire);
//   * the host asserts i_eod with the container's end -- the QUF
//     align padding rides with it and the front-end's ARMED epoch
//     drops it (ten zero pad bytes would otherwise assemble into a
//     valid BIND flit and bind cell 0 -- the bug this TB caught).
//
// Run: iverilog -g2005 -o tb/run/tb_serfabric.vvp \
//        <fabric rtl> rtl/q_uf_loader.v rtl/quf_boot.v \
//        rtl/q_tick_sched_rt.v rtl/q_boot_gate.v rtl/q_serfabric_top.v \
//        tb/tb_serfabric.v && vvp tb/run/tb_serfabric.vvp
// (needs tb/run/quf_tb_input.hex: bash tools/run_quf_tb.sh regenerates)
`timescale 1ns/1ps
module tb_serfabric;
    reg clk = 0;
    always #5 clk = ~clk;

    integer errors = 0;

    // ---------------- DUT-SER: the serialized front end (QUF mode) ----
    reg         por = 0;             // POR for SER + PAR (shared epoch)
    reg         s_sval = 0, s_eod = 0;
    reg  [7:0]  s_sbyte = 0;
    wire        s_srdy;
    wire        s_stx_val;
    wire [7:0]  s_stx;
    wire        s_boot_ok, s_epoch, s_ovf;
    wire [2:0]  s_state;
    wire [7:0]  s_err;

    q_serfabric_top #(.NCELL(2), .SER_BOOT_QUF(1)) dut_ser (
        .clk(clk), .rst_n(por),
        .i_sval(s_sval), .o_srdy(s_srdy), .i_sbyte(s_sbyte), .i_eod(s_eod),
        .o_stx_val(s_stx_val), .i_strdy(1'b1), .o_stx(s_stx),
        .o_boot_ok(s_boot_ok), .o_epoch(s_epoch),
        .o_state(s_state), .o_err(s_err), .o_ovf(s_ovf)
    );

    // ---------------- DUT-PAR: the parallel config path ---------------
    // released the SAME cycle DUT-SER's boot FSM releases (epoch lock)
    reg         p_val = 0, p_rdy_t = 1;
    reg  [2:0]  p_op = 0;
    reg  [3:0]  p_src = 0, p_dst = 0;
    reg  [15:0] p_a0 = 0, p_a1 = 0, p_a2 = 0, p_dat = 0;
    wire        p_rdy, p_val_o;
    wire [2:0]  p_op_o;
    wire [3:0]  p_src_o, p_dst_o;
    wire [15:0] p_a0_o, p_a1_o, p_a2_o, p_dat_o;
    wire        p_ovf;

    q_fabric_top #(.NCELL(2), .TPW(6)) dut_par (
        .clk(clk), .rst_n(por && dut_ser.boot_rst_n),
        .i_val(p_val), .o_rdy(p_rdy),
        .i_op(p_op), .i_src(p_src), .i_dst(p_dst),
        .i_a0(p_a0), .i_a1(p_a1), .i_a2(p_a2), .i_dat(p_dat),
        .o_val(p_val_o), .i_rdy(p_rdy_t),
        .o_op(p_op_o), .o_src(p_src_o), .o_dst(p_dst_o),
        .o_a0(p_a0_o), .o_a1(p_a1_o), .o_a2(p_a2_o), .o_dat(p_dat_o),
        .o_ovf(p_ovf)
    );

    // ---------------- DUT-GATE: flit-mode front end (case B) ----------
    reg         gpor = 0;            // independent POR (case B only)
    reg         g_sval = 0, g_eod = 0;
    reg  [7:0]  g_sbyte = 0;
    wire        g_srdy, g_stx_val;
    wire [7:0]  g_stx;
    wire        g_boot_ok, g_epoch, g_ovf;
    wire [2:0]  g_state;
    wire [7:0]  g_err;

    q_serfabric_top #(.NCELL(2), .SER_BOOT_QUF(0), .TPW0(6)) dut_gate (
        .clk(clk), .rst_n(gpor),
        .i_sval(g_sval), .o_srdy(g_srdy), .i_sbyte(g_sbyte), .i_eod(g_eod),
        .o_stx_val(g_stx_val), .i_strdy(1'b1), .o_stx(g_stx),
        .o_boot_ok(g_boot_ok), .o_epoch(g_epoch),
        .o_state(g_state), .o_err(g_err), .o_ovf(g_ovf)
    );

    // ---------------- cycle counter + capture machinery ---------------
    integer cyc = 0;
    always @(posedge clk) cyc <= cyc + 1;   // NBA: all monitors read the same edge value

    // pulse catchers (wire-edge style, house rule from tb_quf_boot)
    reg saw_s_boot = 0, saw_s_epoch = 0, saw_g_epoch = 0;
    always @(s_boot_ok) if (s_boot_ok === 1'b1) saw_s_boot  = 1;
    always @(s_epoch)   if (s_epoch   === 1'b1) saw_s_epoch = 1;
    always @(g_epoch)   if (g_epoch   === 1'b1) saw_g_epoch = 1;

    // parallel egress capture
    integer pc = 0;
    reg [2:0]  pc_op   [0:255];
    reg [3:0]  pc_src  [0:255], pc_dst [0:255];
    reg [15:0] pc_a0   [0:255], pc_a1 [0:255];
    reg [15:0] pc_a2   [0:255], pc_dat [0:255];
    integer    pc_cyc  [0:255];
    always @(posedge clk) if (p_val_o && p_rdy_t) begin
        if (pc < 255) begin
            pc_op[pc] = p_op_o; pc_src[pc] = p_src_o; pc_dst[pc] = p_dst_o;
            pc_a0[pc] = p_a0_o; pc_a1[pc] = p_a1_o; pc_a2[pc] = p_a2_o;
            pc_dat[pc] = p_dat_o; pc_cyc[pc] = cyc; pc = pc + 1;
        end
    end

    // serialized egress capture: bytes -> flits (10 per flit)
    integer sc = 0, sbytes = 0;
    reg [79:0] sacc;
    reg [2:0]  sc_op   [0:255];
    reg [3:0]  sc_src  [0:255], sc_dst [0:255];
    reg [15:0] sc_a0   [0:255], sc_a1 [0:255];
    reg [15:0] sc_a2   [0:255], sc_dat [0:255];
    integer    sc_cyc  [0:255];
    always @(posedge clk) if (s_stx_val && 1'b1) begin
        sacc = {sacc[71:0], s_stx};           // little-endian, LSB first
        if (sbytes == 0 && sc < 255) sc_cyc[sc] = cyc;   // first byte
        sbytes = sbytes + 1;
        if (sbytes == 10) begin
            sbytes = 0;
            if (sacc[4:0] !== 5'd0) begin
                errors = errors + 1;
                $display("FAIL egress pad bits nonzero (%h)", sacc[4:0]);
            end
            if (sc < 255) begin
                sc_op[sc] = sacc[79:77]; sc_src[sc] = sacc[76:73];
                sc_dst[sc] = sacc[72:69];
                sc_a0[sc] = sacc[68:53]; sc_a1[sc] = sacc[52:37];
                sc_a2[sc] = sacc[36:21]; sc_dat[sc] = sacc[20:5];
                sc = sc + 1;
            end
        end
    end

    // gate-DUT egress capture (bytes -> flits)
    integer gc = 0, gbytes = 0;
    reg [79:0] gacc;
    reg [15:0] gc_dat [0:31];
    reg [2:0]  gc_op  [0:31];
    always @(posedge clk) if (g_stx_val && 1'b1) begin
        gacc = {gacc[71:0], g_stx};
        gbytes = gbytes + 1;
        if (gbytes == 10) begin
            gbytes = 0;
            if (gc < 31) begin
                gc_op[gc] = gacc[79:77]; gc_dat[gc] = gacc[20:5]; gc = gc + 1;
            end
        end
    end

    // ---------------- helpers -----------------------------------------
    task check(input cond, input [255:0] name);
        begin
            if (cond !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL %0s (t=%0t ser_state=%0d err=%0d)",
                         name, $time, s_state, s_err);
            end
        end
    endtask

    task sendbyte(input [7:0] b);
        begin
            @(negedge clk);
            s_sval = 1; s_sbyte = b;
            while (s_srdy !== 1'b1) @(negedge clk);
            @(negedge clk);
            s_sval = 0;
        end
    endtask

    // frame word mirrors q_serfabric_top: {op,src,dst,a0,a1,a2,dat,pad}
    // gate-port byte sender (one byte consumed per call; the inline
    // loop pacing held each byte for two posedges -- every byte
    // consumed twice, garbage frames; found by the debug lane)
    task gsendbyte(input [7:0] b);
        begin
            @(negedge clk);
            g_sval = 1; g_sbyte = b;
            while (g_srdy !== 1'b1) @(negedge clk);
            @(negedge clk);
            g_sval = 0;
        end
    endtask

    function [79:0] packflit(input [2:0] op, input [3:0] src,
                             input [3:0] dst, input [15:0] a0,
                             input [15:0] a1, input [15:0] a2,
                             input [15:0] dat);
        begin
            packflit = {op, src, dst, a0, a1, a2, dat, 5'd0};
        end
    endfunction

    // serialized flit + cycle-locked parallel twin. Bytes 0..8 go as
    // plain bytes; byte 9 is consumed at posedge P, the assembled flit
    // is granted to DUT-SER's ring at P+1, and DUT-PAR is driven at the
    // negedge between P and P+1 so BOTH fabrics consume the flit on the
    // SAME edge. Alignment is verified, not assumed (the TB fails loudly
    // if the io node backpressures -- paced traffic keeps it ready).
    task serflit(input [2:0] op, input [3:0] src, input [3:0] dst,
                 input [15:0] a0, input [15:0] a1, input [15:0] a2,
                 input [15:0] dat);
        integer k;
        reg [79:0] sh;
        begin
            sh = packflit(op, src, dst, a0, a1, a2, dat);
            for (k = 0; k < 9; k = k + 1)
                sendbyte(sh[79 - 8*k -: 8]);
            @(negedge clk);
            s_sval = 1; s_sbyte = sh[7:0];
            while (s_srdy !== 1'b1) @(negedge clk);
            @(posedge clk);                    // P: byte 9 consumed
            @(negedge clk);                     // between P and P+1
            s_sval = 0;
            if (dut_ser.pend !== 1'b1 || dut_ser.ing_rdy !== 1'b1)
                check(1'b0, "serflit grant alignment (P+1)");
            if (p_rdy !== 1'b1)
                check(1'b0, "par ingress ready at mirror edge");
            p_val = 1; p_op = op; p_src = src; p_dst = dst;
            p_a0 = a0; p_a1 = a1; p_a2 = a2; p_dat = dat;
            @(posedge clk);                     // P+1: both consume
            p_val = 0;
        end
    endtask

    // wait for the next egress flit on BOTH fabrics (paced traffic:
    // every ingress flit yields exactly one egress flit -- ACK/NAK to a
    // cell, echo to EXTID), then settle margin
    task wait_pair(input [255:0] name);
        integer base_p, base_s, n;
        begin
            base_p = pc; base_s = sc; n = 0;
            while ((pc <= base_p || sc <= base_s) && n < 20000) begin
                @(negedge clk); n = n + 1;
            end
            check(pc > base_p && sc > base_s, name);
            repeat (60) @(negedge clk);         // ring settle margin
        end
    endtask

    task waitrun(input [2:0] dum);
        integer n;
        begin
            n = 0;
            while (s_state !== 3'd5 && n < 100000) begin
                @(negedge clk); n = n + 1;
            end
            repeat (4) @(negedge clk);
        end
    endtask

    // serialized-only flit (no parallel twin): for the post-boot golden
    // readback phase, where DUT-PAR is still unconfigured
    task serflit_solo(input [2:0] op, input [3:0] src, input [3:0] dst,
                      input [15:0] a0, input [15:0] a1, input [15:0] a2,
                      input [15:0] dat);
        integer k;
        reg [79:0] sh;
        begin
            sh = packflit(op, src, dst, a0, a1, a2, dat);
            for (k = 0; k < 10; k = k + 1)
                sendbyte(sh[79 - 8*k -: 8]);
            repeat (200) @(negedge clk);   // ring round trip + response
        end
    endtask

    // container row goldens (tb/quf_tb.json dials, decimal->hex exact)
    reg [15:0] row0 [0:15];
    reg [15:0] row1 [0:15];
    integer i, j, r, fd, nbytes, tmpi, sc0;
    reg [3:0]  ja;
    reg [79:0] gpack;
    reg [7:0] imem [0:65535];

    // dial probes are direct hierarchical references (house style);
    // iverilog rejects variable hierarchical selects inside functions,
    // so the checks below address each cell's row explicitly

    initial begin
        // INCIDENTS x1000 rule: probe prints carry explicit units
        // (%t otherwise formats in the finest declared precision, ps here)
        $timeformat(-9, 0, " ns", 10);
        // golden container rows (values == tb/quf_tb.json, aligned so the
        // only deltas vs POR defaults are dial5/9/10)
        row0[0]=16'h0800; row0[1]=16'h0080; row0[2]=16'd6;   row0[3]=16'd12;
        row0[4]=16'd5;    row0[5]=16'h5000; row0[6]=16'd4;   row0[7]=16'h2CCD;
        row0[8]=16'd20;   row0[9]=16'd0;    row0[10]=16'h0030;
        row0[11]=16'd0;   row0[12]=16'd0;   row0[13]=16'd0;
        row0[14]=16'd0;   row0[15]=16'd0;
        row1[0]=16'h0800; row1[1]=16'h0080; row1[2]=16'd6;   row1[3]=16'd12;
        row1[4]=16'd5;    row1[5]=16'h6000; row1[6]=16'd4;   row1[7]=16'h2CCD;
        row1[8]=16'd20;   row1[9]=16'd1;    row1[10]=16'h0040;
        row1[11]=16'd0;   row1[12]=16'd0;   row1[13]=16'd0;
        row1[14]=16'd0;   row1[15]=16'd0;

        fd = $fopen("tb/run/quf_tb_input.hex", "r");
        if (fd == 0) begin
            $display("FAIL: cannot open tb/run/quf_tb_input.hex (run tools/run_quf_tb.sh first)");
            $finish;
        end
        r = $fscanf(fd, "%h", nbytes);
        if (r != 1 || nbytes <= 0 || nbytes > 65536 || (nbytes % 2) != 0) begin
            $display("FAIL: bad hex header");
            $finish;
        end
        for (i = 0; i < nbytes; i = i + 1) begin
            r = $fscanf(fd, "%h", tmpi);
            if (r != 1) begin
                $display("FAIL: hex truncated at %0d", i);
                $finish;
            end
            imem[i] = tmpi[7:0];
        end
        $fclose(fd);
        $display("SERFABRIC_TB: %0d-byte golden container", nbytes);
    end

    initial begin
        wait (nbytes > 0);
        repeat (2) @(negedge clk);

        // ================= POR =========================================
        @(negedge clk); por = 0;
        repeat (4) @(negedge clk);
        saw_s_boot = 0; saw_s_epoch = 0;
        @(negedge clk); por = 1;
        repeat (4) @(negedge clk);
        check(s_state === 3'd1, "POR -> HOLD");

        // ================= CASE A1: serialized QUF boot ================
        for (i = 0; i < nbytes; i = i + 1)
            sendbyte(imem[i]);
        // host contract: eod with the container's end (align padding
        // rides with it; the front-end flushes any partial frame)
        @(negedge clk); s_eod = 1;
        @(negedge clk); s_eod = 0;
        waitrun(3'd0);
        check(s_state === 3'd5, "A1 reached RUN");
        check(s_err === 8'd0, "A1 no boot error");
        check(saw_s_boot === 1'b1, "A1 boot_ok pulse");
        check(saw_s_epoch === 1'b1, "A1 epoch pulse");
        check(dut_ser.boot_tpw === 5'd6, "A1 epoch tpw latched = 6");
        check(sbytes === 0, "A1 no egress byte while frozen");
        // bind each cell FIRST: the core's ST_UNB consumes the very
        // first flit as the bind itself (no dial write on that flit --
        // symmetric on both fabrics later); until then every op NAKs
        serflit_solo(3'd0, 4'hF, 4'd0, 16'd0, 16'd0, 16'd0, 16'd0);
        serflit_solo(3'd0, 4'hF, 4'd1, 16'd0, 16'd0, 16'd0, 16'd0);
        // byte-exact rows, both cells (the §7 broadcast proof), read
        // back through the SAME narrow port: one view per dial
        // (a0[1:0]=2 selects the dialfile read, index in a1), response
        // dat must equal the container word exactly
        for (j = 0; j < 16; j = j + 1) begin
            ja = j[3:0];
            serflit_solo(3'd3, 4'hF, 4'd0, {14'd0, 2'd2}, {12'd0, ja},
                         16'd0, 16'd0);
            check(sc_op[sc-1] === 3'd5, "A1 cell0 view acked");
            if (sc_dat[sc-1] !== row0[j]) $display("DBG c0 d%0d got=%h exp=%h", j, sc_dat[sc-1], row0[j]);
            check(sc_dat[sc-1] === row0[j], "A1 cell0 row byte-exact");
        end
        for (j = 0; j < 16; j = j + 1) begin
            ja = j[3:0];
            serflit_solo(3'd3, 4'hF, 4'd1, {14'd0, 2'd2}, {12'd0, ja},
                         16'd0, 16'd0);
            check(sc_op[sc-1] === 3'd5, "A1 cell1 view acked");
            check(sc_dat[sc-1] === row1[j], "A1 cell1 row byte-exact");
        end
        sc0 = sc;   // phase-2 (mirrored) compare starts here on SER side
        check(pc === 0, "A1 parallel twin silent (held until mirror phase)");

        // ================= CASE A2: parallel config + diff stream ======
        // first flit to each cell on PAR is consumed as the first-bind
        // (ST_UNB: binds, no dial write); SER's cells are already bound
        // from A1, so the SAME flit executes as a real bind there -- it
        // must therefore write the SAME value PAR already holds (dial0 =
        // 0x0800 POR default = container value): converged by content.
        serflit(3'd0, 4'hF, 4'd0, {12'd0, 4'd0}, 16'h0800, 16'd0, 16'd0);
        wait_pair("A2 first-bind cell0 ack");
        for (j = 0; j < 16; j = j + 1) begin
            ja = j[3:0];
            serflit(3'd0, 4'hF, 4'd0, {12'd0, ja}, row0[j],
                    16'd0, 16'd0);
            wait_pair("A2 cell0 bind ack");
        end
        serflit(3'd0, 4'hF, 4'd1, {12'd0, 4'd0}, 16'h0800, 16'd0, 16'd0);
        wait_pair("A2 first-bind cell1 ack");
        for (j = 0; j < 16; j = j + 1) begin
            ja = j[3:0];
            serflit(3'd0, 4'hF, 4'd1, {12'd0, ja}, row1[j],
                    16'd0, 16'd0);
            wait_pair("A2 cell1 bind ack");
        end

        // views of ALL 32 dials: the mirrored egress responses prove the
        // end-state dial rows are byte-exact SER vs PAR (old A3 folded in)
        for (j = 0; j < 16; j = j + 1) begin
            ja = j[3:0];
            serflit(3'd3, 4'hF, 4'd0, {14'd0, 2'd2}, {12'd0, ja},
                    16'd0, 16'd0);
            wait_pair("A2 view c0");
        end
        for (j = 0; j < 16; j = j + 1) begin
            ja = j[3:0];
            serflit(3'd3, 4'hF, 4'd1, {14'd0, 2'd2}, {12'd0, ja},
                    16'd0, 16'd0);
            wait_pair("A2 view c1");
        end

        // effects into cells are SILENT (consumed, act integrated, no
        // ACK unless a fire -- dats kept far under thresh so none fires,
        // deterministically on both fabrics); only the EXTID echo
        // egresses
        serflit(3'd2, 4'hF, 4'd0, 16'd0, 16'd0, 16'd0, 16'h0100);
        repeat (200) @(negedge clk);
        serflit(3'd2, 4'hF, 4'd1, 16'd0, 16'd0, 16'd0, 16'h0200);
        repeat (200) @(negedge clk);
        serflit(3'd2, 4'hF, 4'hF, 16'd0, 16'd0, 16'd0, 16'hABCD);
        wait_pair("A2 EXTID echo");

        // tick-domain exercise: 2+ tick periods of decay, then re-view
        repeat (160) @(negedge clk);
        serflit(3'd3, 4'hF, 4'd0, {14'd0, 2'd2}, {12'd0, 4'd10},
                16'd0, 16'd0);
        wait_pair("A2 post-tick view c0 d10");
        serflit(3'd2, 4'hF, 4'd0, 16'd0, 16'd0, 16'd0, 16'h0300);
        repeat (200) @(negedge clk);

        // ================= compare the egress streams ==================
        // SER carried the phase-1 golden readback first; the mirrored
        // phase aligns PAR[0..] with SER[sc0..]
        check(pc === sc - sc0, "A2 egress counts equal (parallel vs serial)");
        if (pc === sc - sc0) begin
            for (j = 0; j < pc; j = j + 1) begin
                check(pc_op[j]   === sc_op[sc0+j],  "A2 egress op match");
                check(pc_src[j]  === sc_src[sc0+j], "A2 egress src match");
                check(pc_dst[j]  === sc_dst[sc0+j], "A2 egress dst match");
                check(pc_a0[j]   === sc_a0[sc0+j],  "A2 egress a0 match");
                check(pc_a1[j]   === sc_a1[sc0+j], "A2 egress a1 match");
                check(pc_a2[j]   === sc_a2[sc0+j], "A2 egress a2 match");
                check(pc_dat[j]  === sc_dat[sc0+j], "A2 egress dat match");
                // cycle lock: SER's first TX byte exactly one cycle
                // after PAR's capture edge. Exception, by construction:
                // the two first-bind flits (j=0, j=17) -- PAR's cells
                // take them from ST_UNB (response straight from the
                // bind state), SER's cells are already bound from the
                // A1 readback and route ST_IDLE->ST_BIND->ST_RESP, one
                // core state later. Same content, one-cycle emission
                // skew, documented cause -- everything else is +1.
                check(sc_cyc[sc0+j] === pc_cyc[j] + 1 ||
                      ((j == 0 || j == 17) &&
                       sc_cyc[sc0+j] === pc_cyc[j] + 2),
                      "A2 egress cycle lock (serial = parallel + 1)");
            end
        end
        // ================= (A3 folded into A2 views above) =============

        // ================= CASE B: gate mode (flit front end) ==========
        @(negedge clk); gpor = 0;
        repeat (4) @(negedge clk);
        @(negedge clk); gpor = 1;
        repeat (4) @(negedge clk);
        check(g_state === 3'd1, "B gate HOLD");
        // wrong word -> sticky HOLD_ERR, fabric never released
        @(negedge clk); g_sval = 1; g_sbyte = 8'h00;
        @(posedge clk);
        @(negedge clk); g_sval = 0;
        repeat (8) @(negedge clk);
        check(g_state === 3'd6, "B wrong word -> HOLD_ERR");
        check(g_err === 8'd11, "B err 11 (bad release word)");
        check(dut_gate.boot_rst_n === 1'b0, "B fabric held");
        // POR retry, correct word 0x51 0x46
        @(negedge clk); gpor = 0;
        repeat (4) @(negedge clk);
        @(negedge clk); gpor = 1;
        repeat (4) @(negedge clk);
        @(negedge clk); g_sval = 1; g_sbyte = 8'h51;
        while (g_srdy !== 1'b1) @(negedge clk);
        @(negedge clk); g_sbyte = 8'h46;
        @(negedge clk); g_sval = 0;
        repeat (8) @(negedge clk);
        check(g_state === 3'd5, "B release word -> RUN");
        check(g_err === 8'd0, "B no error");
        check(saw_g_epoch === 1'b1, "B epoch pulse");
        check(dut_gate.boot_tpw === 5'd6, "B TPW0 epoch latched");
        // dials stream as bind flits over the SAME narrow port. The
        // FIRST bind to the cell is consumed as the bind itself (no
        // write); the second performs the dial write -- then the view
        // must read the written value back through the serial port
        gc = 0;
        gpack = packflit(3'd0, 4'hF, 4'd0, {12'd0, 4'd5},
                         16'h5000, 16'd0, 16'd0);
        for (j = 0; j < 10; j = j + 1)
            gsendbyte(gpack[79 - 8*j -: 8]);
        repeat (400) @(negedge clk);           // first-bind consumed
        for (j = 0; j < 10; j = j + 1)
            gsendbyte(gpack[79 - 8*j -: 8]);
        repeat (400) @(negedge clk);           // dial write lands
        check(gc >= 2, "B bind acks egressed");
        check(gc_op[0] === 3'd5, "B bind ack op");
        check(gc_op[1] === 3'd5, "B dial-write ack op");
        gpack = packflit(3'd3, 4'hF, 4'd0, {14'd0, 2'd2}, {12'd0, 4'd5},
                         16'd0, 16'd0);
        for (j = 0; j < 10; j = j + 1)
            gsendbyte(gpack[79 - 8*j -: 8]);
        repeat (600) @(negedge clk);
        if (gc < 3) $display("DBG B gc=%0d gbytes=%0d", gc, gbytes);
        check(gc >= 3, "B view egressed");
        check(gc_dat[2] === 16'h5000, "B view reads back 0x5000");

        if (errors == 0)
            $display("TB-SERFABRIC PASS: QUF serialized boot byte-exact (2 cells), serial==parallel egress streams (%0d flits, cycle-locked), end-state dial rows byte-exact, gate-mode fail-static + release-word epoch + serial-flit config -- all cases", pc);
        else
            $display("TB-SERFABRIC FAIL: %0d error(s)", errors);
        $finish;
    end

    // global watchdog
    initial begin
        #80_000_000;
        $display("TB-SERFABRIC FAIL: global timeout (ser_state=%0d err=%0d pc=%0d sc=%0d)",
                 s_state, s_err, pc, sc);
        $finish;
    end
endmodule
