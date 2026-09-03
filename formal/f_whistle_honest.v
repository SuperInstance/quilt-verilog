// formal/f_whistle_honest.v -- T3 safety arm: the honest whistle never
// sounds (q_whistle.v, NOVEL-ENHANCEMENTS T3).
//
// Statement: under ANY stimulus whose per-window cancellation count never
// exceeds an honest baseline (calibrated at or below i_base), the whistle
// NEVER alarms -- no strobe, no sticky alert, no strikes -- for all time.
// Formally:
//
//   dials (anyconst, fixed per run): i_base = d_base, i_mul = d_mul >= 1
//     (dial contract), d_honest <= d_base (the calibration premise: the
//     honest rate is what i_base was calibrated to bound).
//   env   (anyseq, unconstrained timing): i_can, i_tick, i_clr.
//   ENV CONTRACT (the assumption under test, invariant form):
//     f_wcnt <= d_honest at every cycle, where f_wcnt is a shadow window
//     counter built with the DUT's own window-edge convention (i_tick
//     closes first; a coincident i_can is the first mark of the new
//     window). Every completed window therefore judged <= d_honest.
//
//   W1  !o_whistle forever          (no strobe)
//   W2  !o_alert forever            (no sticky alarm)
//   W3  o_strikes == 0 forever      (no strike counting)
//   W4  o_wcnt == f_wcnt            (DUT count == shadow count: the
//                                    structural tie that carries the
//                                    induction)
//   W5  o_hist == f_hist            (judged window latched exactly)
//
// Why it is k-inductive (all whistle state is boundary-visible outputs):
// from any state with W4 and the env contract, o_wcnt <= d_honest <=
// d_base <= d_base*d_mul = limit, so `over` is false and no transition
// can set o_whistle/o_alert/o_strikes; W4/W5 transition-identically
// (the shadow mirrors the DUT's saturation at all-ones). Closing this
// unbounded (mode prove) upgrades T3 from "calibrated alarm" to
// "proven alarm": the false-positive rate on honest traffic is exactly
// zero, not merely unobserved in simulation.
//
// Covers (checked by whistle.honest.cover.sby): a nonzero honest window
// completes; the window-edge coincidence (i_can && i_tick); the TIGHTEST
// legal window (count == i_base with i_mul == 1, i.e. count == limit,
// which must stay silent because the comparator is strict >); a host
// clear strobe. Non-vacuity: the environment assumption is exercised at
// its boundary, not just at zero.
module f_whistle_honest(input clk, input rst_n);
    localparam PW = 16, MULW = 3;

    reg [PW-1:0]   d_base;
    reg [MULW-1:0] d_mul;
    reg [PW-1:0]   d_honest;

    reg f_can, f_tick, f_clr;

    wire          w_whistle, w_alert;
    wire [PW-1:0] w_wcnt, w_hist, w_strikes;

    q_whistle #(.PW(PW), .MULW(MULW)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_can(f_can), .i_tick(f_tick),
        .i_base(d_base), .i_mul(d_mul),
        .i_clr(f_clr),
        .o_whistle(w_whistle), .o_alert(w_alert),
        .o_wcnt(w_wcnt), .o_hist(w_hist), .o_strikes(w_strikes)
    );

    // free strobes; dials fixed per run
    always @(posedge clk) begin
        f_can  <= $anyseq;
        f_tick <= $anyseq;
        f_clr  <= $anyseq;
    end
    always @(posedge clk) begin
        if (!rst_n) begin
            d_base   <= $anyconst;
            d_mul    <= $anyconst;
            d_honest <= $anyconst;
        end
    end
    always @(*) begin
        assume (d_mul >= {{(MULW-1){1'b0}}, 1'b1});   // dial contract
        assume (d_honest <= d_base);                  // calibration premise
    end

    // reset preamble (single-reset contract, as fabric.conservation)
    reg [1:0] f_rstctr = 0;
    always @(posedge clk)
        if (f_rstctr < 2) f_rstctr <= f_rstctr + 1;
    always @(*) begin
        if (f_rstctr < 2) assume (!rst_n);
        else              assume (rst_n);
    end

    // shadow window counter, DUT convention, saturation mirrored
    reg [PW-1:0] f_wcnt = {PW{1'b0}};
    always @(posedge clk) begin
        if (!rst_n)
            f_wcnt <= {PW{1'b0}};
        else if (f_tick)
            f_wcnt <= f_can ? {{(PW-1){1'b0}}, 1'b1} : {PW{1'b0}};
        else if (f_can && (f_wcnt != {PW{1'b1}}))
            f_wcnt <= f_wcnt + {{(PW-1){1'b0}}, 1'b1};
    end
    reg [PW-1:0] f_hist = {PW{1'b0}};
    always @(posedge clk) begin
        if (!rst_n)         f_hist <= {PW{1'b0}};
        else if (f_tick)    f_hist <= f_wcnt;
    end

    // THE environment contract: cancels in the open window <= honest
    always @(*) assume (f_wcnt <= d_honest);

    always @(posedge clk) if (rst_n) begin
        assert (!w_whistle);                     // W1
        assert (!w_alert);                       // W2
        assert (w_strikes == {PW{1'b0}});        // W3
        assert (w_wcnt == f_wcnt);               // W4
        assert (w_hist == f_hist);               // W5
    end

    // non-vacuity
    always @(posedge clk) if (rst_n) begin
        cover (f_hist != {PW{1'b0}});              // honest traffic happens
        cover (f_can && f_tick);                   // window-edge coincidence
        cover (f_hist == d_base && d_mul == {{(MULW-1){1'b0}},1'b1});
                                                   // count == limit: silent
        cover (f_clr);                             // host clear exercised
    end
endmodule
