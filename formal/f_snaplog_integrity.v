// formal/f_snaplog_integrity.v -- T1 QUF-SNAP: log-entry integrity
// (q_snaplog.v, NOVEL-ENHANCEMENTS T1).
//
// Statement: every accepted fire (i_fire && !i_freeze) is recorded with
// its EXACT packed fields, in FIFO/shift order, with overflow dropping
// the oldest entry and the drop counted. Proven against a shadow log --
// a DEPTH-deep shadow shift register fed the identical packed entries
// from BOUNDARY signals only (the shadow entry is built from o_tick,
// i_fsign, i_fsrc, i_fmag -- all ports; no XMRs, per house rule):
//
//   S1  CONTENT+ORDER: for the presented read index, whenever
//       i_ridx < o_count, o_rent == f_log[i_ridx] -- every valid entry,
//       at every index, equals the shadow entry that position must hold
//       (newest at 0, oldest at count-1). Since the shadow shifts
//       entries down exactly once per accepted fire, S1 at all indices
//       IS the no-loss/no-reorder/no-corruption statement, and pins the
//       whole retained history to the fire stream.
//   S1' NEWEST DIRECT (shadow-free, human-readable): the cycle after an
//       accepted fire, reading index 0 yields exactly the packed fields
//       observed at the fire cycle: {o_tick, fsign, fsrc, fmag}.
//   S2  COUNTERS: o_count/o_drops equal the shadow counters.
//   S3  BOUNDS: o_count <= DEPTH; o_full == (o_count == DEPTH); count
//       and drops never decrease (monotone).
//   S4  ACCOUNTING, DELTA-EXACT: on an accepted fire, count increments
//       iff not full, else drops increments (saturating at all-ones);
//       with no accepted fire neither moves. Telescoped from reset this
//       is "accepted = retained + dropped", counted exactly.
//   S5  FREEZE: a fire during freeze records nothing (count/drops
//       unchanged; S1+shadow give log bit-stability), and the tick
//       counter still marches (the log's clock never freezes).
//   S6  WINDOW-EDGE STAMP: a fire coincident with i_tick is stamped
//       with the tick of the window ENDING (pre-increment value), read
//       back directly from the entry's tick field.
//
// BMC depth 30 admits >= 18 fires: enough to saturate DEPTH=16 and
// exercise two overflow drops. The content property (S1) is a value
// equality over the hidden 720-bit log register -- not k-inductive from
// the boundary (same class as the flit-pipe V1 caveat); the unbounded
// attempt is the PDR companion (snaplog.integrity.pdr.sby), and the
// boundary-visible counter properties are closed unbounded by
// snaplog.counters.prove.sby.
module f_snaplog_integrity(input clk, input rst_n);
    localparam PW = 16, AIDW = 4, TICKW = 24, DEPTH = 16, MAG = 1;
    localparam EW = TICKW + 1 + AIDW + PW;   // 45
    localparam IDXW = 4;                     // clog2(DEPTH)

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

    // free stimulus
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

    // shadow log: same packed entry, from boundary ports only
    wire         fire_now = f_fire && !f_freeze;
    wire [PW-1:0] fmag_g  = (MAG != 0) ? f_fmag : {PW{1'b0}};
    wire [EW-1:0] entry   = {o_tick, f_fsign, f_fsrc, fmag_g};

    reg [EW-1:0]    f_log [0:DEPTH-1];
    reg [IDXW:0]    f_count = {(IDXW+1){1'b0}};
    reg [TICKW-1:0] f_drops = {TICKW{1'b0}};
    integer i;
    always @(posedge clk) begin
        if (!rst_n) begin
            for (i = 0; i < DEPTH; i = i + 1) f_log[i] <= {EW{1'b0}};
            f_count <= {(IDXW+1){1'b0}};
            f_drops <= {TICKW{1'b0}};
        end else if (fire_now) begin
            for (i = DEPTH-1; i > 0; i = i - 1) f_log[i] <= f_log[i-1];
            f_log[0] <= entry;
            if (f_count == DEPTH) begin
                if (f_drops != {TICKW{1'b1}})
                    f_drops <= f_drops + {{(TICKW-1){1'b0}}, 1'b1};
            end else
                f_count <= f_count + {{IDXW{1'b0}}, 1'b1};
        end
    end

    always @(posedge clk) if (rst_n) begin
        // S1: content + order at every valid presented index
        if ({1'b0, f_ridx} < o_count)
            assert (o_rent == f_log[f_ridx]);
        // S1': newest entry, direct from the ports (shadow-free)
        if ($past(fire_now && rst_n) && f_ridx == {IDXW{1'b0}} && o_count != {(IDXW+1){1'b0}})
            assert (o_rent == {$past(o_tick), $past(f_fsign), $past(f_fsrc), $past(f_fmag)});
        // S2: counters match the shadow
        assert (o_count == f_count);
        assert (o_drops == f_drops);
        // S3: bounds, flag, monotonicity
        assert (o_count <= DEPTH);
        assert (o_full == (o_count == DEPTH));
        if ($past(rst_n)) begin
            assert (o_count >= $past(o_count));
            assert (o_drops >= $past(o_drops));
            // S4: delta-exact accounting
            if ($past(fire_now)) begin
                if ($past(o_full)) begin
                    if ($past(o_drops) == {TICKW{1'b1}})
                        assert (o_drops == {TICKW{1'b1}});
                    else
                        assert (o_drops == $past(o_drops) + {{(TICKW-1){1'b0}}, 1'b1});
                end else
                    assert (o_count == $past(o_count) + {{IDXW{1'b0}}, 1'b1});
            end else begin
                assert (o_count == $past(o_count));
                assert (o_drops == $past(o_drops));
            end
            // S5: freeze drops the fire, never the clock
            if ($past(f_fire && f_freeze)) begin
                assert (o_count == $past(o_count));
                assert (o_drops == $past(o_drops));
            end
            if ($past(f_tick))
                assert (o_tick == $past(o_tick) + {{(TICKW-1){1'b0}}, 1'b1});
        end
        // S6: fire at a window edge stamps the ENDING window's tick
        if ($past(fire_now && f_tick && rst_n)
            && f_ridx == {IDXW{1'b0}} && o_count != {(IDXW+1){1'b0}})
            assert (o_rent[EW-1 -: TICKW] == $past(o_tick));
    end

    // non-vacuity
    always @(posedge clk) if (rst_n) begin
        cover (o_count == DEPTH);                            // saturated
        cover (o_drops != {TICKW{1'b0}});                    // overflow drop
        cover (o_drops >= {{(TICKW-1){1'b0}}, 1'b1});        // >= 2 drops
        cover (f_fire && f_freeze);                          // frozen fire
        cover (f_fire && f_tick);                            // window-edge fire
        cover (f_ridx == 4'd15 && o_count == DEPTH);      // oldest read (DEPTH-1)
        cover (o_count > 1 && f_ridx < o_count[IDXW-1:0]);   // mid-log read
    end
endmodule
