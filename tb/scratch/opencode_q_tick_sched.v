// PROVENANCE: proposals/opencode/RTL-SKETCH.md (round-1 competition entry: opencode)
// q_tick_sched.v -- tick strobe + 4-phase cadence, ARCHITECTURE.md 7.4.
module q_tick_sched #(
    parameter TPW = 12,     // log2(cycles per tick)
    parameter PHW = 2       // phase bits (4 phases)
)(
    input  wire            clk,
    input  wire            rst_n,
    output reg             o_tick,    // 1-cycle strobe at wrap
    output wire [PHW-1:0]  o_phase,   // cnt[TPW-1 -: PHW]
    output wire [TPW-1:0]  o_count
);
    reg [TPW-1:0] cnt;

    assign o_count = cnt;
    assign o_phase = cnt[TPW-1 -: PHW];

    always @(posedge clk) begin
        if (!rst_n) begin
            cnt    <= {TPW{1'b0}};
            o_tick <= 1'b0;
        end else begin
            cnt    <= cnt + {{TPW-1{1'b0}}, 1'b1};
            o_tick <= (cnt == {TPW{1'b0}});
        end
    end

endmodule
