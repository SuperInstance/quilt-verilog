// formal/f_snaplog_observability_canary.v -- MUTATION CANARY for the
// T6 observability proof (round 10): the harness is byte-identical to
// f_snaplog_observability.v except the DUT is a DELIBERATELY BROKEN
// q_snaplog copy (formal/canary/q_snaplog_drop.v) that silently drops
// one log entry (the 6th fire vanishes: neither retained nor counted
// as a drop -- the classic "lost observation" bug T6 exists to catch).
// EXPECTED RESULT: sby FAILS (OBS-1 and OBS-2 both catch it). If this
// harness PASSES, the real proof is vacuous and must not be trusted.
module f_snaplog_observability_canary(input clk, input rst_n);
    localparam PW = 16, AIDW = 4, TICKW = 24, DEPTH = 16, MAG = 1;
    localparam EW = TICKW + 1 + AIDW + PW;
    localparam IDXW = 4;
    localparam JOURNAL = 64, JW = 6;

    reg f_tick, f_fire, f_freeze, f_fsign;
    reg [AIDW-1:0] f_fsrc;
    reg [PW-1:0]   f_fmag;
    reg [IDXW-1:0] f_ridx;

    wire [EW-1:0]    o_rent;
    wire [IDXW:0]    o_count;
    wire [TICKW-1:0] o_tick, o_drops;
    wire             o_full;

    q_snaplog_drop #(.PW(PW), .AIDW(AIDW), .TICKW(TICKW), .DEPTH(DEPTH), .MAG(MAG)) dut (
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

    wire         fire_now = f_fire && !f_freeze;
    wire [PW-1:0] fmag_g  = (MAG != 0) ? f_fmag : {PW{1'b0}};
    wire [EW-1:0] entry   = {o_tick, f_fsign, f_fsrc, fmag_g};

    reg [EW-1:0] f_journal [0:JOURNAL-1];
    reg [JW:0]   f_fires = 0;

    always @(*) assume (f_fires < JOURNAL);

    reg f_wfire = 1'b0;
    always @(*) assume (!(fire_now && f_wfire));

    reg f_vwin  = 1'b0;
    reg f_vmag  = 1'b0;
    reg [PW-1:0] f_thresh;
    always @(*) f_thresh = $anyconst;

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
            if (fire_now) begin
                f_journal[f_fires[JW-1:0]] <= entry;
                f_fires <= f_fires + 1'b1;
            end
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

    always @(posedge clk) if (rst_n) begin
        if ({1'b0, f_ridx} < o_count)
            assert (o_rent == f_journal[f_fires[JW-1:0] - 1 - {1'b0, f_ridx}]);
        assert (o_count + o_drops == f_fires);
        if (ent0_is_newest)
            assert (v_log_win == f_vwin);
        if (ent0_is_newest)
            assert (v_log_mag == f_vmag);
    end

    // force the mutation to matter: reach >= 6 fires
    always @(posedge clk) if (rst_n)
        cover (f_fires >= 6);
endmodule
