// tb_wedge_repro.v -- MINIMAL REPRO of the commissioning-order wedge
// found by sim/vlt/tb_scale_vlt.cpp (silicon experiment lane, 2026-08-30).
//
// Claim to test: a NON-BIND flit delivered to an UNBOUND cell wedges it:
// ST_UNB -> ST_RESP -> ST_IDLE with bound=0 (q_cell_core ST_RESP returns
// to ST_IDLE unconditionally), after which every bind is a dial write and
// the cell can NEVER be commissioned (cell_id never set, views NAK).
// In a multi-cell fabric the trigger is innocent: link cell A to peer B
// before B is bound -- the link ACK (dst=B) is the wedge flit.
//
// Sequence (the scale bench's exact setup order, 2 cells):
//   1. bind cell 1                      -> expect ACK, bound=1
//   2. link cell 1 slot0 to peer 2      -> ACK goes to cell 2 (unbound!)
//   3. bind cell 2                      -> ACK... but is it bound?
//   4. link cell 2 slot0 to peer 1
//   5. view wsum cell 2                 -> 0x0100 if linked, 0 if wedged
//   6. view act cell 2 (sel 0)          -> NAK (op 6) if wedged
// Plus a control run with the DOCUMENTED order (bind 1, bind 2, THEN
// link) proving the fabric itself is fine when commissioning order is
// bind-all-first.
`timescale 1ns/1ps
module tb_wedge_repro;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg         i_val = 0, i_rdy_t = 1;
    reg  [2:0]  i_op = 0;
    reg  [3:0]  i_src = 0, i_dst = 0;
    reg  [15:0] i_a0 = 0, i_a1 = 0, i_a2 = 0, i_dat = 0;
    wire        o_rdy, o_val;
    wire [2:0]  o_op;
    wire [3:0]  o_src, o_dst;
    wire [15:0] o_a0, o_a1, o_a2, o_dat;
    wire        ovf;

    integer errors = 0, guard, lat;
    reg [2:0] top_op;   // task outputs need variables, not wires
    reg [15:0] v;

    q_fabric_top #(.NCELL(3), .TPW(10)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_val(i_val), .o_rdy(o_rdy),
        .i_op(i_op), .i_src(i_src), .i_dst(i_dst),
        .i_a0(i_a0), .i_a1(i_a1), .i_a2(i_a2), .i_dat(i_dat),
        .o_val(o_val), .i_rdy(i_rdy_t),
        .o_op(o_op), .o_src(o_src), .o_dst(o_dst),
        .o_a0(o_a0), .o_a1(o_a1), .o_a2(o_a2), .o_dat(o_dat),
        .o_ovf(ovf)
    );

    task send(input [2:0] op, input [3:0] src, input [3:0] dst,
              input [15:0] a0, input [15:0] a1);
        begin
            @(negedge clk);
            i_val = 1; i_op = op; i_src = src; i_dst = dst;
            i_a0 = a0; i_a1 = a1; i_a2 = 0; i_dat = 0;
            guard = 0;
            while (o_rdy !== 1'b1 && guard < 4000) begin
                @(negedge clk); guard = guard + 1;
            end
            @(posedge clk);
            i_val <= 0;
        end
    endtask

    // collect one egress flit (op returned)
    task recv(output reg [2:0] op, output reg [15:0] dat);
        begin
            lat = 0;
            while (o_val !== 1'b1 && lat < 20000) begin
                @(negedge clk); lat = lat + 1;
            end
            if (o_val !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL recv timeout");
                op = 3'd7; dat = 16'hxxxx;
            end else begin
                op = o_op; dat = o_dat;
                i_rdy_t = 1;
                @(negedge clk);
                i_rdy_t = 0;
            end
        end
    endtask

    task do_view(input [3:0] cid, input [1:0] sel, output reg [2:0] op,
                 output reg [15:0] dat);
        begin
            send(3'd3, 4'hF, cid, {14'd0, sel}, 16'd0);
            recv(op, dat);
        end
    endtask

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (10) @(negedge clk);

        // ---- the scale bench's order: bind, THEN link (peer unbound) ---
        send(3'd0, 4'hF, 4'd1, 16'd1, 16'd0);       // bind cell 1
        recv(top_op, v);
        if (top_op !== 3'd5) begin errors = errors + 1;
            $display("FAIL bind1 op=%0d", top_op); end

        send(3'd1, 4'd2, 4'd1, 16'd0, 16'h0100);    // link 1<->2 (2 unbound)
        repeat (64) @(negedge clk);                 // let the ack land on 2

        send(3'd0, 4'hF, 4'd2, 16'd2, 16'd0);       // bind cell 2 (LATE)
        recv(top_op, v);
        if (top_op !== 3'd5) $display("note: bind2 op=%0d (ack ok)", top_op);
        else $display("note: bind2 ACK (a wedged cell still acks binds)");

        send(3'd1, 4'd1, 4'd2, 16'd0, 16'h0100);    // link 2<->1
        repeat (64) @(negedge clk);

        do_view(4'd2, 2'd1, top_op, v);               // wsum of cell 2
        if (v !== 16'h0100) begin
            $display("WEDGE CONFIRMED: cell2 wsum=%h (want 0100): unbound-in-ST_IDLE cell never commissioned", v);
            errors = errors + 1;
        end else begin
            $display("no wedge: cell2 wsum=%h", v);
        end

        do_view(4'd2, 2'd0, top_op, v);               // act view of cell 2
        if (top_op === 3'd6)
            $display("WEDGE CONFIRMED: cell2 act view NAKed (op=6): cell is unbound in ST_IDLE, permanently");

        // ---- control: documented order (bind both, then link) ----------
        send(3'd0, 4'hF, 4'd0, 16'd0, 16'd0);       // bind cell 0 FIRST
        recv(top_op, v);
        send(3'd1, 4'd2, 4'd0, 16'd0, 16'h0100);    // link 0<->2
        repeat (64) @(negedge clk);
        do_view(4'd0, 2'd1, top_op, v);
        if (v === 16'h0100)
            $display("control OK: bind-then-link cell0 wsum=%h", v);
        else begin
            $display("FAIL control: cell0 wsum=%h", v);
            errors = errors + 1;
        end

        if (dut.nodes[1].connc.u_cell.u_core.bound !== 1'b1) begin
            $display("WEDGE CONFIRMED: cell1 bound=%b", dut.nodes[1].connc.u_cell.u_core.bound);
        end
        if (dut.nodes[2].connc.u_cell.u_core.bound !== 1'b1)
            $display("WEDGE CONFIRMED: cell2 bound=%b after its bind",
                     dut.nodes[2].connc.u_cell.u_core.bound);
        if (dut.nodes[0].conn0.u_cell.u_core.bound !== 1'b1)
            $display("FAIL control: cell0 bound=%b",
                     dut.nodes[0].conn0.u_cell.u_core.bound);

        if (errors == 0) $display("REPRO: PASS (no wedge)");
        else             $display("REPRO: WEDGE REPRODUCED (see above)");
        $finish;
    end
endmodule
