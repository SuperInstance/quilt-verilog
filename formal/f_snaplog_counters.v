// formal/f_snaplog_counters.v -- T1 QUF-SNAP: the boundary-visible
// counter contracts, closed UNBOUNDED by k-induction
// (q_snaplog.v; companion to f_snaplog_integrity.v).
//
// The log-content equality (S1 in f_snaplog_integrity.v) is a value
// property over the hidden 720-bit log register and cannot be carried
// through arbitrary induction states from the module boundary (no XMRs
// in this toolchain) -- the same class as the flit-pipe V1 caveat. But
// every counter property is a function of BOUNDARY-VISIBLE state
// (o_count, o_drops, o_tick are output ports), and those are exactly
// k-inductive:
//
//   S2  o_count/o_drops == shadow counters (transition-identical)
//   S3  o_count <= DEPTH, o_full == (o_count == DEPTH), both monotone
//   S4  delta-exact accounting: accepted fire -> count+1 iff !full,
//       else drops+1 (saturating); no accepted fire -> both hold
//   S5  frozen fires record nothing; the tick marches regardless
//
// Closing these unbounded means: the snaplog's AUDIT surface (how much
// history was surrendered, whether the gauge is full, that freezing
// never silently records or silently drops the clock) is a theorem for
// all time, while the per-entry field integrity stays BMC-bounded
// (snaplog.integrity.sby) pending a PDR/referee pass
// (snaplog.integrity.pdr.sby).
module f_snaplog_counters(input clk, input rst_n);
    localparam PW = 16, AIDW = 4, TICKW = 24, DEPTH = 16, MAG = 1;
    localparam IDXW = 4;

    reg f_tick, f_fire, f_freeze, f_fsign;
    reg [AIDW-1:0] f_fsrc;
    reg [PW-1:0]   f_fmag;
    reg [IDXW-1:0] f_ridx;

    wire [TICKW+1+AIDW+PW-1:0] o_rent;
    wire [IDXW:0]              o_count;
    wire [TICKW-1:0]           o_tick, o_drops;
    wire                       o_full;

    q_snaplog #(.PW(PW), .AIDW(AIDW), .TICKW(TICKW), .DEPTH(DEPTH), .MAG(MAG)) dut (
        .clk(clk), .rst_n(rst_n),
        .i_tick(f_tick), .i_fire(f_fire), .i_fsrc(f_fsrc), .i_fsign(f_fsign),
        .i_fmag(f_fmag), .i_freeze(f_freeze), .i_ridx(f_ridx),
        .o_rent(o_rent), .o_count(o_count), .o_tick(o_tick), .o_drops(o_drops),
        .o_full(o_full)
    );

    always @(posedge clk) begin
        f_tick   <= $anyseq;
        f_fire   <= $anyseq;
        f_freeze <= $anyseq;
        f_fsign  <= $anyseq;
        f_fsrc   <= $anyseq;
        f_fmag   <= $anyseq;
        f_ridx   <= $anyseq;
    end

    reg [1:0] f_rstctr = 0;
    always @(posedge clk)
        if (f_rstctr < 2) f_rstctr <= f_rstctr + 1;
    always @(*) begin
        if (f_rstctr < 2) assume (!rst_n);
        else              assume (rst_n);
    end

    wire fire_now = f_fire && !f_freeze;

    reg [IDXW:0]    f_count = {(IDXW+1){1'b0}};
    reg [TICKW-1:0] f_drops = {TICKW{1'b0}};
    always @(posedge clk) begin
        if (!rst_n) begin
            f_count <= {(IDXW+1){1'b0}};
            f_drops <= {TICKW{1'b0}};
        end else if (fire_now) begin
            if (f_count == DEPTH) begin
                if (f_drops != {TICKW{1'b1}})
                    f_drops <= f_drops + {{(TICKW-1){1'b0}}, 1'b1};
            end else
                f_count <= f_count + {{IDXW{1'b0}}, 1'b1};
        end
    end

    always @(posedge clk) if (rst_n) begin
        assert (o_count == f_count);                    // S2
        assert (o_drops == f_drops);
        assert (o_count <= DEPTH);                      // S3
        assert (o_full == (o_count == DEPTH));
        if ($past(rst_n)) begin
            assert (o_count >= $past(o_count));
            assert (o_drops >= $past(o_drops));
            if ($past(fire_now)) begin                  // S4
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
            if ($past(f_fire && f_freeze)) begin        // S5
                assert (o_count == $past(o_count));
                assert (o_drops == $past(o_drops));
            end
            if ($past(f_tick))
                assert (o_tick == $past(o_tick) + {{(TICKW-1){1'b0}}, 1'b1});
        end
    end

    always @(posedge clk) if (rst_n) begin
        cover (o_count == DEPTH);
        cover (o_drops != {TICKW{1'b0}});
        cover (f_fire && f_freeze);
    end
endmodule
