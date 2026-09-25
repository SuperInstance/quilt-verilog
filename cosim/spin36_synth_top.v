// spin36_synth_top.v -- SPIN-36 SYNTH: PW-parameterized clone of the
// SPIN-19 registered-IO gate-cell wrapper. Same structure, same ports
// (resid/tval/events width = PW), PW and GMODE set via yosys chparam.
module spin36_synth_top #(
    parameter PW = 48
) (
    input  wire clk,
    input  wire rst_n,
    input  wire i_go,
    input  wire [31:0] i_seed,
    input  wire [41:0] i_lats,
    output wire [PW-1:0] o_resid,
    output wire o_tval,
    output wire [PW-1:0] o_events
);
    reg         r_go   = 0;
    reg  [31:0] r_seed = 0;
    reg  [41:0] r_lats = 0;
    reg  [PW-1:0] o_resid_r = 0;
    reg         o_tval_r  = 0;
    reg  [PW-1:0] o_events_r = 0;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            r_go <= 0; r_seed <= 0; r_lats <= 0;
            o_resid_r <= 0; o_tval_r <= 0; o_events_r <= 0;
        end else begin
            r_go <= i_go; r_seed <= i_seed; r_lats <= i_lats;
            o_resid_r <= o_resid; o_tval_r <= o_tval;
            o_events_r <= o_events;
        end
    end

    q_wall_gate #(.N(7), .K(1), .PD(3), .DELTA(12), .DRIFT(6),
                  .PW(PW), .TW(14), .GMODE(2), .THETA100(8'd110))
        u_gate (.clk(clk), .rst_n(rst_n), .i_go(r_go), .i_seed(r_seed),
                .i_lats(r_lats), .o_running(), .o_bail(), .o_t(),
                .o_resid(o_resid), .o_tval(o_tval), .o_cflag(), .o_nf(),
                .o_gopen(), .o_em_mask(), .o_em_pm(), .o_em_e(),
                .o_events(o_events), .o_mass(), .o_cancels(),
                .o_chatter(), .o_settles(), .o_gopen_tot(), .o_gcomp());
endmodule
