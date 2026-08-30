// tb_boot_fuzz.v -- quf_boot boundary fuzz harness (backend lane).
// Reads a manifest of fuzzed QUF byte streams (tools/backend/boot_fuzz.py
// writes tb/run/boot_fuzz.hex), runs each through the REAL boot FSM with a
// POR between cases, and asserts the warm-boot contract:
//   EXP=1 must boot:    RUN reached, o_err==0, epoch pulsed once, mycell
//                       dial row bit-exact (when the manifest carries it)
//   EXP=0 must fail:    HOLD_ERR sticky, o_rst_n NEVER asserted (never a
//                       released half-image)
//   EXP=2 either:       terminates in RUN or HOLD_ERR; release implies
//                       err==0
//   EXP=3 hold-wait:    empty stream: FSM waits in HOLD, never releases
// Loud PASS/FAIL, one line per finding; case 0 details on mismatch.
`timescale 1ns/1ps
module tb_boot_fuzz;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg         i_bval = 0;
    wire        o_brdy;
    reg  [7:0]  i_byte = 0;
    reg         i_eod = 0;
    wire [3:0]  df_addr;
    wire [15:0] df_wdata;
    wire        df_wr;
    wire [3:0]  edge_addr, route_dst, route_via;
    wire [31:0] edge_data;
    wire        edge_wr, route_wr;
    wire [4:0]  o_tpw;
    wire        o_epoch, o_rst_n, o_boot_ok;
    wire [2:0]  o_state;
    wire [7:0]  o_err;
    wire [15:0] df_rdata_probe;
    wire        df_probe_stb;

    localparam [2:0] S_HOLD = 3'd1, S_RUN = 3'd5, S_HERR = 3'd6;

    quf_boot #(.AIDW(4)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_bval(i_bval), .o_brdy(o_brdy), .i_byte(i_byte), .i_eod(i_eod),
        .i_mycell(4'd2),
        .i_qm_wr(1'b0), .i_qm_addr(4'd0), .i_qm_wdata(16'd0),
        .o_df_wr(df_wr), .o_df_addr(df_addr), .o_df_wdata(df_wdata),
        .o_edge_wr(edge_wr), .o_edge_addr(edge_addr), .o_edge_data(edge_data),
        .o_route_wr(route_wr), .o_route_dst(route_dst), .o_route_via(route_via),
        .o_tpw(o_tpw), .o_epoch(o_epoch), .o_rst_n(o_rst_n),
        .o_boot_ok(o_boot_ok), .o_state(o_state), .o_err(o_err)
    );

    // the dialfile this boot instance drives (POR domain = dut rst_n)
    wire [15:0] dummy_o;
    q_dialfile u_df (
        .clk(clk), .rst_n(rst_n),
        .i_wr(df_wr), .i_addr(df_addr), .i_wdata(df_wdata),
        .i_rd(1'b0), .o_rdata(dummy_o), .o_rstb(df_probe_stb),
        .o_eta_f(), .o_eta_s(), .o_kf(), .o_ks(), .o_ka(),
        .o_thresh(), .o_refr(), .o_cosmin(), .o_p0e(), .o_mode(),
        .o_hl(), .i_probe(16'd0), .o_kle(), .o_floor(),
        .o_qdw(), .o_qleak(), .o_rqen()
    );

    integer errors = 0;
    integer fd, r, ncases, ci, exp, nbytes, bi, i, tmpi;
    integer nboot, nfail, neither, nhold;
    integer released, epochs, df_writes, edge_writes;

    // pulse-catchers: sample at posedge so one-cycle pulses (epoch,
    // release) are never missed by the settle-loop's exit condition
    always @(posedge clk) begin
        if (o_rst_n === 1'b1)  released = 1;
        if (o_epoch === 1'b1)  epochs  = epochs + 1;
    end
    integer guard;

    reg [15:0] exp_dials [0:15];
    reg        has_dials;
    reg [4:0]  exp_tpw;

    // snapshot dialfile via hierarchical read (verilog-2005 friendly here)
    task check_dials(input integer ok_needed);
        begin
            if (has_dials && ok_needed) begin
                for (i = 0; i < 16; i = i + 1)
                    if (u_df.dial[i[3:0]] !== exp_dials[i]) begin
                        errors = errors + 1;
                        $display("FAIL case %0d dial[%0d] = %h, expected %h",
                                 ci, i, u_df.dial[i[3:0]], exp_dials[i]);
                    end
            end
        end
    endtask

    task do_por;
        begin
            rst_n = 0; i_bval = 0; i_eod = 0;
            repeat (3) @(negedge clk);
            rst_n = 1;
            @(negedge clk);
        end
    endtask

    task run_case;
        begin
            released = 0; epochs = 0;
            // stream the bytes; 1-in-3 backpressure is the loader's own
            // cadence; drive one byte per brd
            for (bi = 0; bi < nbytes; bi = bi + 1) begin
                r = $fscanf(fd, "%h", tmpi);
                if (r != 1) begin
                    errors = errors + 1;
                    $display("FAIL manifest truncated (case %0d byte %0d)",
                             ci, bi);
                    $display("BOOT-FUZZ FAIL: %0d error(s)", errors);
                    $finish;
                end
                guard = 0;
                @(negedge clk);
                while (o_brdy !== 1'b1 && guard < 32) begin
                    @(negedge clk); guard = guard + 1;
                end
                if (o_brdy !== 1'b1) begin
                    errors = errors + 1;
                    $display("FAIL case %0d: transport stalled at byte %0d",
                             ci, bi);
                end
                i_bval = 1; i_byte = tmpi[7:0];
                @(negedge clk);
                i_bval = 0;
            end
            // end of stream: a well-behaved host asserts eod only after
            // the machine drained (o_brdy stably high; the skid + loader
            // 1-in-3 cadence). eod mid-drain is a TRUNCATION by contract.
            guard = 0;
            while (guard < 64 && !(o_brdy === 1'b1 && o_state !== 3'd2)) begin
                @(negedge clk); guard = guard + 1;
            end
            repeat (8) @(negedge clk);
            i_eod = 1; @(negedge clk); i_eod = 0;
            // monitor release during settle
            guard = 0;
            while (guard < 200000 && o_state !== S_RUN && o_state !== S_HERR) begin
                @(negedge clk);
                guard = guard + 1;
            end
            // settle a window (monitors above catch any late pulses)
            repeat (50) @(negedge clk);
        end
    endtask

    initial begin
        fd = $fopen("tb/run/boot_fuzz.hex", "r");
        if (fd == 0) begin
            $display("BOOT-FUZZ FAIL: cannot open tb/run/boot_fuzz.hex (run tools/backend/boot_fuzz.py)");
            $finish;
        end
        r = $fscanf(fd, "%h", ncases);
        if (r != 1) begin
            $display("BOOT-FUZZ FAIL: bad manifest header");
            $finish;
        end
        nboot = 0; nfail = 0; neither = 0; nhold = 0;
        for (ci = 0; ci < ncases; ci = ci + 1) begin
            do_por;
            r = $fscanf(fd, "%h", exp);
            r = $fscanf(fd, "%h", nbytes);
            run_case;
            // expectations
            r = $fscanf(fd, "%h", tmpi); has_dials = (tmpi == 1);
            for (i = 0; i < 16; i = i + 1) begin
                r = $fscanf(fd, "%h", tmpi);
                exp_dials[i] = tmpi[15:0];
            end
            r = $fscanf(fd, "%h", tmpi); exp_tpw = tmpi[4:0];

            if (exp == 1) begin
                nboot = nboot + 1;
                if (o_state !== S_RUN || o_err !== 8'd0 || !released) begin
                    errors = errors + 1;
                    $display({"FAIL case %0d: MUST BOOT but state=%0d err=%0d ",
                             "released=%0d"}, ci, o_state, o_err, released);
                end else begin
                    if (epochs !== 1) begin
                        errors = errors + 1;
                        $display("FAIL case %0d: epoch pulsed %0d times",
                                 ci, epochs);
                    end
                    if (o_tpw !== exp_tpw) begin
                        errors = errors + 1;
                        $display("FAIL case %0d: tpw=%0d expected %0d",
                                 ci, o_tpw, exp_tpw);
                    end
                    check_dials(1);
                end
            end else if (exp == 0) begin
                nfail = nfail + 1;
                if (released) begin
                    errors = errors + 1;
                    $display({"FAIL case %0d: MUST FAIL-STATIC but released ",
                             "(state=%0d err=%0d) -- HALF-LOADED CELL"},
                             ci, o_state, o_err);
                end else if (o_state !== S_HERR) begin
                    errors = errors + 1;
                    $display({"FAIL case %0d: MUST FAIL-STATIC but state=%0d ",
                             "err=%0d"}, ci, o_state, o_err);
                end
            end else if (exp == 2) begin
                neither = neither + 1;
                if (o_state !== S_RUN && o_state !== S_HERR) begin
                    errors = errors + 1;
                    $display("FAIL case %0d: EITHER but hung in state=%0d",
                             ci, o_state);
                end
                if (released && (o_err !== 8'd0 || o_state !== S_RUN)) begin
                    errors = errors + 1;
                    $display("FAIL case %0d: released dirty (err=%0d)",
                             ci, o_err);
                end
            end else begin // exp == 3: hold-wait
                nhold = nhold + 1;
                if (released || o_state !== S_HOLD) begin
                    errors = errors + 1;
                    $display({"FAIL case %0d: empty stream must HOLD (got ",
                             "state=%0d released=%0d)"}, ci, o_state, released);
                end
            end
            do_por;
        end
        if (errors == 0)
            $display({"BOOT-FUZZ PASS: %0d cases (%0d booted clean + dial ",
                     "rows, %0d fail-static, %0d either, %0d hold-wait); ",
                     "0 half-loads, 0 split-brains"},
                     ncases, nboot, nfail, neither, nhold);
        else
            $display("BOOT-FUZZ FAIL: %0d error(s) over %0d cases",
                     errors, ncases);
        $fclose(fd);
        $finish;
    end

    // watchdog
    initial begin
        #5_000_000_000;
        $display("BOOT-FUZZ FAIL: global timeout (state=%0d err=%0d)",
                 o_state, o_err);
        $finish;
    end


endmodule
