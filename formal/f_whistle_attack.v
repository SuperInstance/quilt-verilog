// formal/f_whistle_attack.v -- T3 completeness arm: sustained lying is
// caught fast (q_whistle.v, NOVEL-ENHANCEMENTS T3).
//
// Statement: an attacker that overdrives cancellations at the maximum
// rate (i_can asserted every cycle) against windows that close regularly
// (i_tick exactly every d_win cycles) alarms at the FIRST judged window,
// within a bounded deadline, for EVERY legal dial pair.
//
//   dials (anyconst): d_base >= 1 (calibrated mode; base=0 paranoia is
//     trivially louder), d_mul >= 1, d_win in [limit+2, 16] with
//     limit = d_base*d_mul <= 14 (constraint keeps the dial set
//     nonempty; whistle.attack.cover.sby proves it is).
//   stimulus: i_can = 1 continuously, i_clr = 0 continuously, i_tick
//     from a phase counter that wraps at d_win -- the fabric-tick role,
//     regularized so the first window completes inside the BMC depth.
//
// With count = window length and the strict-> comparator, the constraint
// d_win >= limit+2 makes the first judged window (count d_win-1) already
// over-limit: W-1 >= limit+1 > limit. Bounded liveness in the house
// style (assert-within-N with a countdown armed at run start):
//
//   A1  o_whistle strobes at least once before the deadline (2*d_win+8)
//   A2  o_alert is latched when the deadline expires (sticky; no clear)
//   A3  o_strikes != 0 when the deadline expires
//
// PASS means the solver CANNOT avoid the alarm within the deadline under
// any legal dial pair -- a completeness result, strictly stronger than a
// cover (a cover only shows one escaping trace; this bounds every one).
// Together with the safety arm this brackets T3: honest windows never
// alarm (unbounded), lying windows always alarm (first window, bounded).
module f_whistle_attack(input clk, input rst_n);
    localparam PW = 16, MULW = 3;

    reg [PW-1:0]   d_base;
    reg [MULW-1:0] d_mul;
    reg [4:0]      d_win;

    wire          w_whistle, w_alert;
    wire [PW-1:0] w_wcnt, w_hist, w_strikes;

    q_whistle #(.PW(PW), .MULW(MULW)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_can(1'b1), .i_tick(f_tick),
        .i_base(d_base), .i_mul(d_mul),
        .i_clr(1'b0),
        .o_whistle(w_whistle), .o_alert(w_alert),
        .o_wcnt(w_wcnt), .o_hist(w_hist), .o_strikes(w_strikes)
    );

    always @(posedge clk) begin
        if (!rst_n) begin
            d_base <= $anyconst;
            d_mul  <= $anyconst;
            d_win  <= $anyconst;
        end
    end
    wire [PW+MULW-1:0] f_lim = d_base * d_mul;
    always @(*) begin
        assume (d_base >= {{(PW-1){1'b0}}, 1'b1});
        assume (d_mul  >= {{(MULW-1){1'b0}}, 1'b1});
        assume (f_lim <= 19'd14);                          // dial set nonempty
        assume ({14'd0, d_win} >= f_lim + 19'd2);          // W >= limit+2
        assume (d_win <= 5'd16);                           // window closes in depth
    end

    // reset preamble
    reg [1:0] f_rstctr = 0;
    always @(posedge clk)
        if (f_rstctr < 2) f_rstctr <= f_rstctr + 1;
    always @(*) begin
        if (f_rstctr < 2) assume (!rst_n);
        else              assume (rst_n);
    end

    // regular windows: phase wraps at d_win; tick on the last phase
    reg [4:0] f_phase = 5'd0;
    wire      f_tick  = (f_phase == d_win - 5'd1);
    always @(posedge clk) begin
        if (!rst_n)                       f_phase <= 5'd0;
        else if (f_phase == d_win - 5'd1) f_phase <= 5'd0;
        else                              f_phase <= f_phase + 5'd1;
    end

    // bounded liveness: countdown armed at run start, deadline 2*d_win+8
    reg        f_armed = 1'b0;
    reg [5:0]  f_dead  = 6'd0;
    reg        f_seen  = 1'b0;
    always @(posedge clk) begin
        if (!rst_n) begin
            f_armed <= 1'b0;
            f_dead  <= 6'd0;
            f_seen  <= 1'b0;
        end else begin
            if (!f_armed) begin
                f_armed <= 1'b1;
                f_dead  <= 6'd8 + {1'b0, d_win} + {1'b0, d_win}; // 2*d_win+8
            end else if (f_dead != 6'd0)
                f_dead <= f_dead - 6'd1;
            if (w_whistle)
                f_seen <= 1'b1;
        end
    end

    always @(posedge clk) if (rst_n && f_armed && f_dead == 6'd0) begin
        assert (f_seen);                 // A1: whistled within deadline
        assert (w_alert);                // A2: alert sticky at deadline
        assert (w_strikes != {PW{1'b0}}); // A3: strikes counted
    end

    // non-vacuity of the dial set + stimulus (cover companion)
    always @(posedge clk) if (rst_n) begin
        cover (w_whistle);               // the strobe happens
        cover (w_strikes >= {{(PW-1){1'b0}},1'b1} && w_strikes <= 16'd2);
        cover (f_armed && f_dead == 6'd0); // deadline reached (in depth)
    end
endmodule
