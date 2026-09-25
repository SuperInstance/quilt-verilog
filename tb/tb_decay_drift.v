// tb_decay_drift.v -- truncation-drift measurement on the act leak chain.
//
// The unsloth cross-exam's one measured question (docs/UNSLOTH-CROSS-EXAM.md
// §3): the canonical tick leak is `act <= sclip16(act - (act >>> ka))`
// (q_cell_core.v:220,:541). The arithmetic right shift is floor division;
// for positive act it discards the fractional leak (act retains MORE than
// the exact geometric decay -- any act < 2^ka is a fixed point: it stalls,
// never reaching 0), and for negative act the floor over-subtracts (-1
// >>> ka == -1, so -1 annihilates in one tick). The two signs drift in
// opposite directions; the pitch's claim of a systematic truncation bias
// is directionally right. This TB measures it on the REAL core -- no model
// substitution for the DUT -- and runs a convergent-rounding
// (round-half-to-even) variant as a PARALLEL MODULE (decay_rne, below);
// the canonical RTL is untouched.
//
// Method: one q_cell, one linked edge at base weight 0x7F00 (one cofire's
// ladder readout of 0x0100 brings the integrating weight to exactly 0x8000,
// so a single effect seeds act := dat bit-exactly). thresh=0x7FFF so the
// cell never fires; mass stays in act and the only dynamics is the leak.
// Then N ticks; every 10k the act register is read back with view(0) and
// cross-checked bit-exactly against a TB-side truncation model. The RNE
// module runs the same ticks with leak = act - rne(act/2^ka).
//
// PASS = the TB model matches the RTL act at every checkpoint (the
// measurement is validated); the drift numbers themselves are data, not
// pass/fail. Expected from the analysis above: trunc stalls positive mass
// inside [1, 2^ka-1] forever; RNE halves the stall band to [1, 2^(ka-1)]
// and ties (rem == 2^(ka-1)) round to even. Exact geometric decay from
// |act0| <= 32767 with ka=4 crosses below 0.5 by tick ~700, so at 10k+
// the exact residue is 0: every reported LSB of stall IS drift.
`timescale 1ns/1ps
module tb_decay_drift;
    reg clk = 0, rst_n = 0, s_tick = 0;
    always #5 clk = ~clk;

    // ring side (same shape as tb_cell_core)
    reg         ri_valid = 0, ro_ready = 1;
    reg  [2:0]  ri_op = 0;
    reg  [3:0]  ri_src = 0, ri_dst = 0;
    reg  [15:0] ri_a0 = 0, ri_a1 = 0, ri_a2 = 0, ri_dat = 0;
    wire        ri_ready, ro_valid;
    wire [2:0]  ro_op;
    wire [3:0]  ro_src, ro_dst;
    wire [15:0] ro_a0, ro_a1, ro_a2, ro_dat;
    wire        ovf;

    integer errors = 0, guard;

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

    localparam integer KA      = 4;      // dial 4 value written below
    localparam integer NTICK   = 100000; // measured run length
    localparam integer CHK     = 10000;  // checkpoint spacing

    // ---------------- parallel module: convergent (round-half-to-even) leak
    // Same state update as the canonical ST_TLEAK, but the leak amount is
    // rounded to nearest-even instead of floored. Standalone by design:
    // q_cell_core.v is byte-identical to HEAD; this module is the A/B.
    // (decls before use: oss-cad iverilog 13 rejects forward refs in ports)
    reg          rne_step = 0;
    reg  signed [15:0] rne_start = 16'sd0;
    wire signed [15:0] rne_act;
    decay_rne #(.W(16), .KA(KA)) u_rne (
        .clk(clk), .rst_n(rst_n), .i_step(rne_step),
        .i_start(rne_start), .o_act(rne_act)
    );

    // ---------------- TB-side integer models (self-check the measurement)
    integer m_trunc;          // mirrors canonical: x - (x >>> KA), floor
    integer m_rne;            // mirrors decay_rne
    real    m_exact;          // exact geometric: x * (1 - 2^-KA) per tick
    integer mm_errors = 0;    // model-vs-RTL mismatches at checkpoints
    integer mm_rne_err = 0;   // decay_rne-module-vs-model mismatches
    integer tickno = 0;       // global tick counter (both runs)
    integer settle_t = 0, settle_r = 0;  // tick of last state change
    integer m_trunc_prev, m_rne_prev;

    // rne division on integers: floor + non-negative remainder, then
    // rem > half -> up; rem == half -> to even quotient.
    function integer rne_div;
        input integer x;
        integer q, rem, half;
        begin
            q    = x >>> KA;
            rem  = x - (q <<< KA);
            half = 1 << (KA - 1);
            if ((rem > half) || ((rem == half) && (q[0] == 1'b1)))
                q = q + 1;
            rne_div = q;
        end
    endfunction

    // ---------------- ring helpers (style of tb_cell_core)
    task send(input [2:0] op, input [3:0] src,
              input [15:0] a0, input [15:0] a1,
              input [15:0] a2, input [15:0] dat);
        begin
            @(negedge clk);
            ri_valid = 1; ri_op = op; ri_src = src; ri_dst = 4'd1;
            ri_a0 = a0; ri_a1 = a1; ri_a2 = a2; ri_dat = dat;
            guard = 0;
            // Acceptance at the coming posedge is decided by the REGISTERED
            // inbuf state, not the ri_ready wire: a same-delta read of
            // ri_ready after the blocking assignments above sees the stale
            // pre-assignment value (transit-path ready) and can exit the
            // wait with the hit flit undelivered -- TB-side flit loss,
            // root-caused 2026-09-03 (BACKEND-NOTES gapped-stream weak
            // point). b_v is race-free here; latency unchanged. Non-hit
            // (transit) flits keep the immediate-transfer behavior.
            while (ri_dst == dut.i_myid && dut.u_inbuf.b_v !== 1'b0 && guard < 500) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 500) begin
                errors = errors + 1;
                $display("FAIL send_timeout op=%0d", op);
            end
            @(posedge clk);
            ri_valid <= 0;
        end
    endtask

    // wait for one ack flit, return its dat
    task recv_ack(output [15:0] dat);
        begin
            @(negedge clk);
            guard = 0;
            while (ro_valid !== 1'b1 && guard < 2000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (ro_valid !== 1'b1) begin
                errors = errors + 1;
                $display("FAIL ack timeout");
                dat = 16'hDEAD;
            end else begin
                dat = ro_dat;
                @(negedge clk);
            end
        end
    endtask

    task view_act(output [15:0] dat);
        reg [15:0] d;
        begin
            send(3'd3, 4'd2, 16'd0, 16'd0, 16'd0, 16'd0); // view, sel 0 = act
            recv_ack(d);
            dat = d;
        end
    endtask

    // one tick: strobe, wait for the service to finish (ready returns),
    // advance all three models
    task do_tick;
        begin
            @(negedge clk); s_tick = 1;
            @(negedge clk); s_tick = 0;
            guard = 0;
            while (ri_ready !== 1'b1 && guard < 1000) begin
                @(negedge clk); guard = guard + 1;
            end
            if (guard >= 1000) begin
                errors = errors + 1;
                $display("FAIL tick service hang");
            end
            // parallel RNE module steps once per tick service
            rne_step = 1;
            @(negedge clk);
            rne_step = 0;
            m_trunc = m_trunc - (m_trunc >>> KA);
            m_rne   = m_rne   - rne_div(m_rne);
            m_exact = m_exact * (1.0 - 1.0 / (1 << KA));
            tickno  = tickno + 1;
            if (m_trunc != m_trunc_prev) begin
                settle_t = tickno; m_trunc_prev = m_trunc;
            end
            if (m_rne != m_rne_prev) begin
                settle_r = tickno; m_rne_prev = m_rne;
            end
        end
    endtask

    integer n, seed_i;
    reg [15:0] rd;
    reg signed [15:0] srd;
    integer drift_t, drift_r;

    // ---------------- one measured run: seed act = seed0, tick NTICK ----
    task run_chain(input integer seed0, input [127:0] tag);
        begin
            // parallel module seeds at reset release: set BEFORE rst_n=1
            // (o_act <= i_start while rst_n low)
            rne_start = seed0;
            // reset the cell
            rst_n = 0; repeat (4) @(negedge clk); rst_n = 1;
            repeat (4) @(negedge clk);

            // bind (cell_id=1), link edge slot 0 at base 0x7F00
            send(3'd0, 4'd2, 16'd1, 16'd0, 16'd0, 16'd0);
            recv_ack(rd);
            send(3'd1, 4'd2, 16'd0, 16'h7F00, 16'd0, 16'd0);
            recv_ack(rd);
            // seed: one cofire -> weight 0x7F00+0x0100 = 0x8000, so
            // act += (0x8000 * dat) >>> 15 = dat, bit-exact.
            // (Effects do NOT ack -- tb_cell_core test 3 style: just wait.)
            send(3'd2, 4'd2, 16'd0, 16'd0, 16'd0, seed0[15:0]);
            repeat (60) @(negedge clk);       // let the effect op complete
            // dials: ka=4 (dial 4), thresh=0x7FFF (dial 5), refr=0 (dial 6)
            send(3'd0, 4'd2, 16'd4, 16'd4,    16'd0, 16'd0);
            recv_ack(rd);
            send(3'd0, 4'd2, 16'd5, 16'h7FFF, 16'd0, 16'd0);
            recv_ack(rd);
            send(3'd0, 4'd2, 16'd6, 16'd0,    16'd0, 16'd0);
            recv_ack(rd);

            m_trunc = seed0; m_rne = seed0; m_exact = seed0;
            m_trunc_prev = seed0; m_rne_prev = seed0;
            settle_t = 0; settle_r = 0; tickno = 0;

            $display("== %0s: seed=%0d  ka=%0d  N=%0d",
                     tag, seed0, KA, NTICK);
            $display("   tick      act(RTL)   trunc(model)  rne(module)  exact");

            for (n = 1; n <= NTICK; n = n + 1) begin
                do_tick();
                if (n % CHK == 0) begin
                    view_act(rd);
                    srd = $signed(rd);
                    if (srd !== m_trunc) begin
                        mm_errors = mm_errors + 1;
                        $display("FAIL model mismatch tick %0d: rtl=%0d model=%0d",
                                 n, srd, m_trunc);
                    end
                    if (rne_act !== m_rne) begin
                        mm_rne_err = mm_rne_err + 1;
                        $display("FAIL rne mismatch tick %0d: mod=%0d model=%0d",
                                 n, rne_act, m_rne);
                    end
                    $display("   %0d   %0d   %0d   %0d   %0.3g",
                             n, srd, m_trunc, rne_act, m_exact);
                end
            end

            // drift vs exact: the exact geometric residue is < 0.5 LSB by
            // the first checkpoint, so drift = |final state - 0| in LSB.
            drift_t = (m_trunc >= 0) ? m_trunc : -m_trunc;
            drift_r = (m_rne   >= 0) ? m_rne   : -m_rne;
            $display("   DRIFT_TRUNC_LSB %0d (settled tick %0d)  DRIFT_RNE_LSB %0d (settled tick %0d)  (%0s)",
                     drift_t, settle_t, drift_r, settle_r, tag);
        end
    endtask

    initial begin
        run_chain(20000, "positive_seed");
        run_chain(-20000, "negative_seed");

        $display("");
        if (errors == 0 && mm_errors == 0 && mm_rne_err == 0) begin
            $display("TB_DECAY_DRIFT PASS (models bit-exact; drift numbers above are data)");
        end else begin
            $display("TB_DECAY_DRIFT FAIL errors=%0d mm=%0d mm_rne=%0d",
                     errors, mm_errors, mm_rne_err);
        end
        $finish;
    end
endmodule

// ---------------- convergent-rounding leak, standalone ------------------
// One state register, stepped on i_step. Update:
//   o_act <= o_act - rne_half_even(o_act / 2^KA)
// where rne_half_even = floor, remainder ties round quotient to even.
// Identical interface position to the canonical leak expression
// (q_cell_core.v:220); kept OUT of rtl/ so the shipped core is untouched.
module decay_rne #(
    parameter W  = 16,
    parameter KA = 4
)(
    input  wire               clk,
    input  wire               rst_n,
    input  wire               i_step,
    input  wire signed [W-1:0] i_start,   // reset/reload value (parallel-
                                          // module convenience: the real
                                          // core seeds via OP_EFF instead)
    output reg  signed [W-1:0] o_act
);
    reg signed [W+KA:0] q, rem;
    localparam signed [W+KA:0] HALF = 1 << (KA - 1);

    always @(posedge clk) begin
        if (!rst_n) begin
            o_act <= i_start;
        end else if (i_step) begin
            q   = o_act >>> KA;              // floor division
            rem = o_act - (q <<< KA);        // always in [0, 2^KA-1]
            if ((rem > HALF) || ((rem == HALF) && (q[0] == 1'b1)))
                q = q + 1;                   // ties to even quotient
            o_act <= o_act - q;
        end
    end
endmodule
