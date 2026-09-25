// formal/f_snaplog_observability.v -- T6 OBSERVABILITY THEOREM (round 10,
// Q3; NOVEL-ENHANCEMENTS T6, sharpened by F12/F10/F9).
//
// THE CLAIM: "nothing observable is lost by reading only where blades
// fit." Formalized here as an equivalence between the FULL-WAVE journal
// (a shadow that records every observable fire event, unbounded in
// intent, bounded to JOURNAL=64 entries in this BMC window) and the
// snap-log's retained window (q_snaplog, DEPTH=16, oldest dropped and
// COUNTED). The obligations:
//
// DEFINITION (observable event). An observable fire at cycle t is an
// event with i_fire && !i_freeze -- exactly the events the cosim
// byte-compares as E-lines (per-emission traces, SPIN-19). A fire
// during i_freeze is DECLARED NON-OBSERVABLE (the blade is lifted off
// the work; q_snaplog S5 pins the DUT drops it, by design). This
// matches the operational definition the program already audits.
//
// DEFINITION (blade-fit reading). A blade reads only where it fits:
// the retained window read at any index i < o_count. The theorem says
// this is information-equivalent to the full wave, up to the DECLARED
// loss (o_drops oldest entries, counted exactly).
//
//   OBS-1 COMPLETENESS: every observable event still inside the
//       retention window is present, exactly, at its position: for the
//       presented index i < o_count, o_rent == journal[fires-1-i]
//       (newest at 0). The log never misses an event it had room for.
//
//   OBS-2 SOUNDNESS (nothing in the log that didn't happen + exact
//       accounting): o_count + o_drops == fires (no wrap, window-
//       bounded): every journal event is either retained or counted
//       dropped -- nothing counted that didn't happen, nothing
//       happened that wasn't counted. Together with OBS-1's positional
//       equality this is the equivalence: retained window == newest
//       min(DEPTH, fires) slice of the full wave.
//
//   OBS-3 F12 VERDICT EQUIVALENCE (boolean blades are as strong as the
//       full wave at blade-fit ticks): with W = current tick window
//       (the value o_tick holds between i_tick strobes),
//        (a) window verdict:  "a fire occurred in W" computed from the
//            LOG (newest entry exists, tick field == o_tick)  <==>
//            computed from the WAVE (sticky per-window fire flag).
//        (b) threshold verdict (THRESH anyconst): "the fire in W had
//            magnitude >= THRESH" from the LOG (newest entry tick ==
//            o_tick && fmag >= THRESH)  <=>  from the WAVE.
//       This is F12's certified early-exit boolean, promoted from
//       simulation to a proof object: the 1-bit answer read off the
//       log is provably identical to the full-observation answer.
//
// PRECONDITIONS (assumes; the SPIN-19 declared-overflow discipline --
// constrain to what the finite-width RTL guarantees):
//   P1  at most ONE observable fire per tick window. Faithful to
//       q_cell_core: one fire test per tick service, and refractory
//       blocks the next until it expires. Load-bearing for OBS-3b
//       (two fires in one window make "the fire" ambiguous; the cell
//       cannot produce this).
//   P2  window-bounded journal: fires < JOURNAL (64). The BMC window
//       admits full saturation (16) + 48 overflow drops. Unbounded
//       attempts: snaplog.t6.pdr.sby (PDR sees the hidden log register,
//       the integrity.pdr path); journal equality is not boundary-
//       inductive (same class as S1) -- booked honestly either way.
//   P3  no tick-counter wrap in the window (TICKW=24 needs 2^24 ticks;
//       BMC depth 80 cannot wrap; stated for the record). Tick-stamp
//       ordering is claimed modulo 2^TICKW wrap.
module f_snaplog_observability(input clk, input rst_n);
    localparam PW = 16, AIDW = 4, TICKW = 24, DEPTH = 16, MAG = 1;
    localparam EW = TICKW + 1 + AIDW + PW;   // 45
    localparam IDXW = 4;                     // clog2(DEPTH)
    localparam JOURNAL = 64, JW = 6;         // full-wave shadow depth

    reg f_tick, f_fire, f_freeze, f_fsign;
    reg [AIDW-1:0] f_fsrc;
    reg [PW-1:0]   f_fmag;
    reg [IDXW-1:0] f_ridx;

    wire [EW-1:0]    o_rent;
    wire [IDXW:0]    o_count;
    wire [TICKW-1:0] o_tick, o_drops;
    wire             o_full;

    q_snaplog #(.PW(PW), .AIDW(AIDW), .TICKW(TICKW), .DEPTH(DEPTH), .MAG(MAG)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_tick(f_tick), .i_fire(f_fire), .i_fsrc(f_fsrc), .i_fsign(f_fsign),
        .i_fmag(f_fmag), .i_freeze(f_freeze), .i_ridx(f_ridx),
        .o_rent(o_rent), .o_count(o_count), .o_tick(o_tick), .o_drops(o_drops),
        .o_full(o_full)
    );

    // free stimulus (the wave: every cycle observed in full)
    always @(posedge clk) begin
        f_tick   <= $anyseq;
        f_fire   <= $anyseq;
        f_freeze <= $anyseq;
        f_fsign  <= $anyseq;
        f_fsrc   <= $anyseq;
        f_fmag   <= $anyseq;
        f_ridx   <= $anyseq;
    end

    // reset preamble (single-reset contract)
    reg [1:0] f_rstctr = 0;
    always @(posedge clk)
        if (f_rstctr < 2) f_rstctr <= f_rstctr + 1;
    always @(*) begin
        if (f_rstctr < 2) assume (!rst_n);
        else              assume (rst_n);
    end

    // ---------------- full-wave journal (the reference observation) ----
    wire         fire_now = f_fire && !f_freeze;   // OBSERVABLE event
    wire [PW-1:0] fmag_g  = (MAG != 0) ? f_fmag : {PW{1'b0}};
    wire [EW-1:0] entry   = {o_tick, f_fsign, f_fsrc, fmag_g};

    reg [EW-1:0] f_journal [0:JOURNAL-1];
    reg [JW:0]   f_fires = 0;                     // total observable fires

    // P2: window-bounded journal
    always @(*) assume (f_fires < JOURNAL);

    // P1: at most one observable fire per tick window (cell-faithful)
    reg f_wfire = 1'b0;                           // a fire already in this window
    always @(*) assume (!(fire_now && f_wfire));

    // ---------------- verdict references (full-wave booleans) ---------
    reg f_vwin  = 1'b0;   // a fire occurred in the current window
    reg f_vmag  = 1'b0;   // that fire's magnitude >= THRESH
    reg [PW-1:0] f_thresh;  // anyconst verdict threshold (F12 blade)
    always @(*) f_thresh = $anyconst;

    // log-derived verdicts (boolean blades): newest entry via index 0.
    // Fields: [EW-1 -: TICKW]=tick, [EW-TICKW-1]=sign,
    //         [EW-TICKW-2 -: AIDW]=src, [PW-1:0]=fmag.
    wire [EW-1:0] ent0_w = o_rent;                // presented at f_ridx
    wire ent0_is_newest = (f_ridx == {IDXW{1'b0}});
    wire v_log_win  = ent0_is_newest && (o_count != 0)
                      && (o_rent[EW-1 -: TICKW] == o_tick);
    wire v_log_mag  = v_log_win && (o_rent[PW-1:0] >= f_thresh);

    always @(posedge clk) begin
        if (!rst_n) begin
            f_fires <= 0;
            f_wfire <= 0;
            f_vwin  <= 0;
            f_vmag  <= 0;
        end else begin
            // journal append (the wave records everything observable)
            if (fire_now) begin
                f_journal[f_fires[JW-1:0]] <= entry;
                f_fires <= f_fires + 1'b1;
            end
            // window bookkeeping: a fire coincident with i_tick belongs
            // to the ENDING window (stamped with its pre-increment tick,
            // q_snaplog S6); the new window starts empty.
            if (f_tick) begin
                // fire coincident with i_tick belongs to the ENDING window
                // (stamped with its pre-increment tick, q_snaplog S6);
                // the new window starts unfired.
                f_wfire <= 1'b0;
                f_vwin  <= 1'b0;
                f_vmag  <= 1'b0;
            end else if (fire_now) begin
                f_wfire <= 1'b1;
                f_vwin  <= 1'b1;
                f_vmag  <= (fmag_g >= f_thresh);
            end
        end
    end

    // ---------------- the obligations ----------------------------------
    always @(posedge clk) if (rst_n) begin
        // OBS-1 COMPLETENESS: presented retained entry == its full-wave
        // journal event (positional: newest at 0 == fires-1)
        if ({1'b0, f_ridx} < o_count)
            assert (o_rent == f_journal[f_fires[JW-1:0] - 1 - {1'b0, f_ridx}]);
        // OBS-2 SOUNDNESS + exact accounting: retained + dropped == all
        // observable events (no wrap in window: drops <= 48 < 2^24)
        assert (o_count + o_drops == f_fires);
        // OBS-3a window verdict equivalence
        if (ent0_is_newest)
            assert (v_log_win == f_vwin);
        // OBS-3b threshold verdict equivalence (F12 boolean, proved)
        if (ent0_is_newest)
            assert (v_log_mag == f_vmag);
    end

    // non-vacuity
    always @(posedge clk) if (rst_n) begin
        cover (f_fires == JOURNAL-1);                 // journal near-full
        cover (o_drops >= 48);                        // deep overflow regime
        cover (o_count == DEPTH);                     // saturated log
        cover (v_log_win && f_vwin);                  // verdict TRUE reachable
        cover (!v_log_win && !f_vwin && o_count > 0); // verdict FALSE w/ history
        cover (v_log_mag && !(!f_vmag));              // mag verdict TRUE
        cover (f_fire && f_freeze);                   // frozen (non-observable) fire
        cover (f_fire && f_tick);                     // window-edge fire
    end
endmodule
