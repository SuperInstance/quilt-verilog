// tb_link_ringport.v -- directed: deliver/transit/inject/backpressure.
`timescale 1ns/1ps
module tb_link_ringport;
    reg  [3:0]  myid = 4'd3;

    reg         ri_valid = 0, ld_ready = 1, ro_ready = 1, li_valid = 0;
    reg  [2:0]  ri_op = 0, li_op = 0;
    reg  [3:0]  ri_src = 0, ri_dst = 0, li_src = 0, li_dst = 0;
    reg  [15:0] ri_a0 = 0, ri_dat = 0, li_a0 = 0, li_dat = 0;
    wire        ri_ready, ro_valid, li_ready, ld_valid;
    wire [2:0]  ro_op, ld_op;
    wire [3:0]  ro_src, ro_dst, ld_src, ld_dst;
    wire [15:0] ro_a0, ro_dat, ld_a0, ld_dat;

    integer errors = 0;

    q_link_ringport u_dut (
        .i_myid(myid),
        .ri_valid(ri_valid), .ri_ready(ri_ready),
        .ri_op(ri_op), .ri_src(ri_src), .ri_dst(ri_dst),
        .ri_a0(ri_a0), .ri_a1(), .ri_a2(), .ri_dat(ri_dat),
        .ro_valid(ro_valid), .ro_ready(ro_ready),
        .ro_op(ro_op), .ro_src(ro_src), .ro_dst(ro_dst),
        .ro_a0(ro_a0), .ro_a1(), .ro_a2(), .ro_dat(ro_dat),
        .li_valid(li_valid), .li_ready(li_ready),
        .li_op(li_op), .li_src(li_src), .li_dst(li_dst),
        .li_a0(li_a0), .li_a1(), .li_a2(), .li_dat(li_dat),
        .ld_valid(ld_valid), .ld_ready(ld_ready),
        .ld_op(ld_op), .ld_src(ld_src), .ld_dst(ld_dst),
        .ld_a0(ld_a0), .ld_a1(), .ld_a2(), .ld_dat(ld_dat)
    );

    task chk(input cond, input [127:0] name);
        if (!cond) begin
            errors = errors + 1;
            $display("FAIL %0s", name);
        end
    endtask

    initial begin
        // 1: hit with ld_ready -> delivered, consumed, ro idle
        ri_valid = 1; ri_dst = 4'd3; ri_dat = 16'h1111; ri_src = 4'd9;
        #1;
        chk(ld_valid === 1'b1, "ld_valid_hit");
        chk(ld_dat === 16'h1111, "ld_dat_hit");
        chk(ro_valid === 1'b0, "ro_idle_on_deliver");
        chk(ri_ready === 1'b1, "ri_ready_hit");

        // 2: hit with backpressure -> stalls ring, no ro progress
        ld_ready = 0;
        #1;
        chk(ri_ready === 1'b0, "backpressure_ri");
        chk(ld_valid === 1'b1, "ld_valid_hold");
        ld_ready = 1;

        // 3: not hit -> transits
        ri_dst = 4'd2;
        #1;
        chk(ro_valid === 1'b1, "transit_ro_valid");
        chk(ro_dat === 16'h1111, "transit_ro_dat");
        chk(ro_dst === 4'd2, "transit_ro_dst");
        chk(ld_valid === 1'b0, "no_ld_on_transit");
        chk(ri_ready === 1'b1, "transit_ri_ready");

        // 4: inject on bubble
        ri_valid = 0; li_valid = 1; li_src = 4'd3; li_dst = 4'd1;
        li_dat = 16'h2222;
        #1;
        chk(li_ready === 1'b1, "inject_bubble_ready");
        chk(ro_valid === 1'b1, "inject_ro_valid");
        chk(ro_dat === 16'h2222, "inject_ro_dat");

        // 5: no inject while transit occupies the slot
        ri_valid = 1; ri_dst = 4'd2; ri_dat = 16'h3333;
        #1;
        chk(li_ready === 1'b0, "no_inject_in_transit");
        chk(ro_dat === 16'h3333, "transit_wins");

        // 6: inject into a slot freed by delivery (hit+ld_ready)
        ri_dst = 4'd3;
        #1;
        chk(ld_valid === 1'b1, "freed_ld_valid");
        chk(li_ready === 1'b1, "inject_freed_slot");
        chk(ro_dat === 16'h2222, "inject_uses_freed");

        // 7: ro backpressure propagates to ri (transit) and li
        ri_dst = 4'd2; ro_ready = 0;
        #1;
        chk(ri_ready === 1'b0, "ro_bp_ri");
        chk(li_ready === 1'b0, "ro_bp_li");
        ro_ready = 1;

        if (errors == 0) $display("TB_LINK_RINGPORT PASS");
        else $display("TB_LINK_RINGPORT FAIL %0d", errors);
        $finish;
    end
endmodule
