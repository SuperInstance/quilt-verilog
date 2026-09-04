// formal/f_snaplog_t6_cell.v -- T6 INTEGRATION LEG (round 10, Q3): the
// observability equivalence CLOSED THROUGH A REAL CELL. q_cell_core in
// the adversarial flood environment of f_cell_core_tick.v (continuous
// ingress, free strobes/dials, E2 engine contract, E3 dialfile stub,
// lx/lo always ready) with a q_snaplog bolted on as the blade, driven
// ONLY from boundary-visible fire events:
//
//   OBSERVABLE FIRE (cell, boundary definition): an emission burst on
//   the fabric port -- lx_valid && lx_ready && lx_op==OP_EFF. In the
//   RTL these emissions are issued ONLY by ST_FIRE (the fire fanout),
//   all carrying lx_dat == afire (the activation at fire) and
//   lx_src == cell_id. A burst = maximal run of accepted OP_EFF
//   emissions separated by at most 3 idle cycles (invalid edge slots
//   advance eidx with lx_valid low for up to EDGES_N-1 = 3 cycles);
//   two distinct fires are separated by a full tick service (~30+
//   cycles: fire sets refr, the next fire test needs a completed
//   sweep), so >= 4 idle cycles is a sound burst boundary WITHOUT any
//   scheduler-spacing assumption.
//
// Obligations (blade reads only the log; the wave is the ports):
//
//   T6-C1 BURST COHERENCE: within a burst every accepted emission
//        carries identical lx_dat (one afire per fire) and
//        lx_src == cell_id. (The wave's own fire witness is well-
//        formed; this is what makes "the fire's magnitude" a single
//        number the log can store.)
//   T6-C2 COMPLETENESS: the cycle after each burst starts, the log's
//        newest entry holds exactly that burst's magnitude and source:
//        entry.fmag == lx_dat, entry.fsrc == cell_id, and entry sign
//        bit == lx_dat[15] (activation sign at fire). Every boundary-
//        observable fire is recorded, exactly.
//   T6-C3 SOUNDNESS: the log only moves on real bursts -- o_count
//        increments ONLY in cycles with an accepted OP_EFF emission
//        (the burst-start detector fires only inside real bursts), so
//        nothing can appear in the log that the wave did not emit.
//        (Structural by the wiring; asserted as the delta law.)
//   T6-C4 (F12 corollary, cell-level): the newest entry's magnitude is
//        the most recent burst's lx_dat -- the boolean blade "last fire
//        magnitude >= THRESH" read off the log equals the same verdict
//        read off the port, one cycle after burst start.
//
// Booking: fires with ZERO linked edges produce no emissions and are
// NOT boundary-observable (nothing to lose: there is no wave event);
// this leg claims the equivalence for emission-observable fires only.
// The tick stamping uses i_tick = s_tick (window = between strobes;
// fire is stamped with the window it fires inside -- a definition
// choice, matches the cosim T-line windows).
module f_snaplog_t6_cell(input clk, input rst_n);
    localparam OPW = 3, AIDW = 4, PW = 16, EDGES_N = 4, EIW = 2, K = 8;
    localparam TICKW = 24, SDEPTH = 16, MAG = 1;
    localparam EW = TICKW + 1 + AIDW + PW;
    localparam IDXW = 4;
    // burst gap bound: EDGES_N-1 = 3 invalid-edge idle cycles max
    localparam [2:0] GAP = 3'd4;

    localparam [OPW-1:0] OP_BIND = 3'd0, OP_LINK = 3'd1, OP_EFF  = 3'd2,
                         OP_VIEW = 3'd3, OP_TICK = 3'd4, OP_ACK  = 3'd5,
                         OP_NAK  = 3'd6;

    reg  [OPW-1:0]    ci_op;
    reg               ci_valid;
    wire              ci_ready;
    reg  [AIDW-1:0]   ci_src;
    reg  [PW-1:0]     ci_a0, ci_a1, ci_a2, ci_dat;

    wire [OPW-1:0]    lo_op;
    wire              lo_valid;
    wire              lo_ready = 1'b1;
    wire [AIDW-1:0]   lo_dst, lo_src;
    wire [PW-1:0]     lo_a0, lo_a1, lo_a2, lo_dat;

    wire [OPW-1:0]    lx_op;
    wire              lx_valid;
    wire              lx_ready = 1'b1;
    wire [AIDW-1:0]   lx_dst, lx_src;
    wire [PW-1:0]     lx_a0, lx_a1, lx_a2, lx_dat;

    wire [2:0]        hb_cmd;
    wire [EDGES_N-1:0] hb_sel;
    wire [PW-1:0]     hb_base;
    wire [3:0]        hb_gcl;
    reg  [PW-1:0]     hb_w;
    reg               hb_done;

    wire              df_wr;
    wire [4-1:0]      df_addr;
    wire [PW-1:0]     df_wdata;
    wire              df_rd;
    reg  [PW-1:0]     df_rdata;
    reg               df_rstb;

    reg  [3:0]        d_ka;
    reg  signed [PW-1:0] d_thresh;
    reg  [PW-1:0]     d_refr;
    reg  [3:0]        d_kle, d_qdw, d_qleak;
    reg  [PW-1:0]     d_floor;
    reg               d_rqen;

    reg               s_tick;

    wire              bound, o_ftrace, o_antic;
    wire [AIDW-1:0]   cell_id;
    wire signed [PW-1:0] act;

    q_cell_core #(.OPW(OPW), .AIDW(AIDW), .PW(PW),
                  .EDGES_N(EDGES_N), .EIW(EIW), .K(K)) cell (
        .clk(clk), .rst_n(rst_n),
        .ci_op(ci_op), .ci_valid(ci_valid), .ci_ready(ci_ready),
        .ci_src(ci_src), .ci_a0(ci_a0), .ci_a1(ci_a1), .ci_a2(ci_a2),
        .ci_dat(ci_dat),
        .lo_op(lo_op), .lo_valid(lo_valid), .lo_ready(lo_ready),
        .lo_dst(lo_dst), .lo_src(lo_src),
        .lo_a0(lo_a0), .lo_a1(lo_a1), .lo_a2(lo_a2), .lo_dat(lo_dat),
        .lx_op(lx_op), .lx_valid(lx_valid), .lx_ready(lx_ready),
        .lx_dst(lx_dst), .lx_src(lx_src),
        .lx_a0(lx_a0), .lx_a1(lx_a1), .lx_a2(lx_a2), .lx_dat(lx_dat),
        .hb_cmd(hb_cmd), .hb_sel(hb_sel), .hb_base(hb_base), .hb_gcl(hb_gcl),
        .hb_w(hb_w), .hb_done(hb_done),
        .df_wr(df_wr), .df_addr(df_addr), .df_wdata(df_wdata),
        .df_rd(df_rd), .df_rdata(df_rdata), .df_rstb(df_rstb),
        .d_ka(d_ka), .d_thresh(d_thresh), .d_refr(d_refr),
        .d_kle(d_kle), .d_floor(d_floor),
        .d_qdw(d_qdw), .d_qleak(d_qleak), .d_rqen(d_rqen),
        .s_tick(s_tick),
        .bound(bound), .cell_id(cell_id), .act(act),
        .o_ftrace(o_ftrace), .o_antic(o_antic)
    );

    // the blade: q_snaplog on the fire events
    wire [EW-1:0]    s_rent;
    wire [IDXW:0]    s_count;
    wire [TICKW-1:0] s_tickc, s_drops;
    wire             s_full;
    reg              f_fire_det;                 // burst-start pulse
    reg [IDXW-1:0]   f_ridx;                     // free read index

    q_snaplog #(.PW(PW), .AIDW(AIDW), .TICKW(TICKW),
                .DEPTH(SDEPTH), .MAG(MAG)) snap (
        .clk(clk), .rst_n(rst_n),
        .i_tick(s_tick), .i_fire(f_fire_det),
        .i_fsrc(f_bsrc), .i_fsign(f_bmag[PW-1]), .i_fmag(f_bmag),
        .i_freeze(1'b0), .i_ridx(f_ridx),
        .o_rent(s_rent), .o_count(s_count), .o_tick(s_tickc),
        .o_drops(s_drops), .o_full(s_full)
    );

    // reset preamble
    reg [1:0] f_rstctr = 0;
    always @(posedge clk)
        if (f_rstctr < 2) f_rstctr <= f_rstctr + 1;
    always @(*)
        if (f_rstctr < 2) assume (!rst_n);

    // free inputs (flood, as f_cell_core_tick)
    always @(posedge clk) begin
        ci_valid <= $anyseq;
        s_tick   <= $anyseq;
        {ci_op, ci_src, ci_a0, ci_a1, ci_a2, ci_dat} <= $anyseq;
        hb_w     <= $anyseq;
        hb_done  <= $anyseq;
        {d_ka, d_refr, d_kle, d_qdw, d_qleak, d_rqen} <= $anyseq;
        d_thresh <= $anyseq;
        d_floor  <= $anyseq;
        f_ridx   <= $anyseq;
    end
    always @(*)
        if (f_rstctr >= 2 && rst_n) assume (ci_valid);

    // E3: dialfile stub with real q_dialfile timing
    always @(posedge clk) begin
        df_rstb <= df_rd;
        if (df_rd) df_rdata <= $anyseq;
    end

    // E2: engine responsiveness contract (as f_cell_core_tick.v)
    reg [2:0] f_lcmd = 3'b000;
    reg [4:0] f_hbc  = 0;
    wire f_eng_active = (hb_sel != {EDGES_N{1'b0}}) || (hb_cmd != 3'b000);
    wire [4:0] f_hblim = (f_lcmd == 3'b011) ? 5'd12 : 5'd4;
    always @(posedge clk) begin
        if (hb_cmd != 3'b000) f_lcmd <= hb_cmd;
        if (!rst_n)
            f_hbc <= 0;
        else if (!f_eng_active || hb_done || (lx_valid && lx_ready) || ci_ready)
            f_hbc <= 0;
        else
            f_hbc <= f_hbc + 1'b1;
    end
    always @(*)
        if (f_rstctr >= 2) assume (f_hbc <= f_hblim);

    // ---------------- burst detector (blade-side event abstraction) ----
    wire f_emission = lx_valid && lx_ready && (lx_op == OP_EFF);
    reg  f_inburst  = 1'b0;    // inside an emission burst
    reg  [2:0] f_gap = 0;      // consecutive non-emission cycles
    reg  [PW-1:0] f_bmag = 0;  // this burst's magnitude (first emission)
    reg  [AIDW-1:0] f_bsrc = 0;// this burst's source (cell_id at fire)

    always @(posedge clk) begin
        if (!rst_n) begin
            f_inburst <= 1'b0; f_gap <= 0; f_bmag <= 0; f_bsrc <= 0;
            f_fire_det <= 1'b0;
        end else begin
            f_fire_det <= 1'b0;                       // default: no pulse
            if (f_emission) begin
                f_gap <= 0;
                if (!f_inburst) begin
                    f_inburst   <= 1'b1;              // burst starts
                    f_bmag      <= lx_dat;            // T6-C1 anchor
                    f_bsrc      <= lx_src;
                    f_fire_det  <= 1'b1;              // record this fire
                end
            end else if (f_inburst) begin
                f_gap <= f_gap + 1'b1;
                if (f_gap + 1'b1 >= GAP) begin
                    f_inburst <= 1'b0;                // burst ends
                    f_gap     <= 0;
                end
            end
        end
    end

    // ---------------- obligations --------------------------------------
    // verdict threshold (F12 boolean blade)
    reg [PW-1:0] f_thresh;
    always @(*) f_thresh = $anyconst;

    wire ent0_newest = (f_ridx == {IDXW{1'b0}});
    wire [PW-1:0] ent0_fmag = s_rent[PW-1:0];
    wire [AIDW-1:0] ent0_fsrc = s_rent[PW-1 + AIDW -: AIDW];

    always @(posedge clk) if (rst_n) begin
        // T6-C1: burst coherence -- one magnitude per burst, source is
        // the cell, every emission is an OP_EFF fire fanout
        if (f_emission && f_inburst) begin
            assert (lx_dat == f_bmag);
            assert (lx_src == cell_id);
        end
        // T6-C2: completeness -- cycle after burst start, newest log
        // entry holds exactly the burst's fire fields (latched anchors)
        if ($past(f_fire_det && rst_n) && ent0_newest && s_count != 0) begin
            assert (ent0_fmag == $past(f_bmag));
            assert (ent0_fsrc == $past(f_bsrc));
            assert (s_rent[PW+AIDW] == $past(f_bmag[PW-1]));   // sign bit
        end
        // T6-C3: soundness, delta-exact -- the log moves ONLY on the
        // detector pulse (a real wave burst), one entry per pulse,
        // drops accounting exact on saturation
        if ($past(rst_n)) begin
            if (!$past(s_full))
                assert (s_count == $past(s_count)
                         + ({{IDXW{1'b0}}, $past(f_fire_det) ? 1'b1 : 1'b0}));
            else if ($past(f_fire_det) && $past(s_drops) != {TICKW{1'b1}})
                assert (s_drops == $past(s_drops) + {{(TICKW-1){1'b0}}, 1'b1});
            else if (!$past(f_fire_det))
                assert (s_drops == $past(s_drops));
        end
        // T6-C4: F12 boolean at cell level -- log magnitude verdict ==
        // port magnitude verdict, one cycle after burst start
        if ($past(f_fire_det && rst_n) && ent0_newest && s_count != 0)
            assert ((ent0_fmag >= f_thresh) == ($past(f_bmag) >= f_thresh));
    end

    // non-vacuity: the whole path must actually fire through the cell
    always @(posedge clk) if (rst_n) begin
        cover (f_emission);                       // a real fire fanout
        cover (f_fire_det);                       // detector pulses
        cover (s_count >= 1);                     // a fire is logged
        cover (s_count >= 2);                     // two fires logged
        cover (f_emission && f_inburst);          // multi-emission burst
        cover (s_count == SDEPTH);                // log saturated via cell
        cover (s_drops != 0);                     // overflow via cell fires
    end
endmodule
