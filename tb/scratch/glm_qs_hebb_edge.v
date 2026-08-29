// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
module qs_hebb_edge #(
    parameter K = 12,          // buckets  (memory horizon = K half-lives)
    parameter B = 6            // count bits per bucket
)(
    input  wire               clk,
    input  wire               rst_n,
    input  wire               ld_en,     // load record (from edge RAM)
    input  wire [K*B-1:0]     rec_in,
    input  wire               evt_fire,  // cofire: C_0 += 1 (after aging if both)
    input  wire               hl_sh,     // age one class: ladder >>= B
    output wire [K*B-1:0]     rec_out,   // current (post-update) record
    output wire [K*B-1:0]     p_ro,      // weighted readout Ŵ (of loaded record)
    output reg                sat_evt    // sticky: bucket-0 saturate this record
);
    reg [K*B-1:0] rec;

    // combinational update
    wire [K*B-1:0] aged  = {{B{1'b0}}, rec[K*B-1:B]};      // C_i <- C_i-1, retire top
    wire [K*B-1:0] based = hl_sh ? aged : rec;
    wire             full0 = &based[B-1:0];                // C_0 saturated?
    wire [K*B-1:0] bumped = based + {{(K*B-1){1'b0}}, 1'b1};

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rec     <= {(K*B){1'b0}};
            sat_evt <= 1'b0;
        end else if (ld_en) begin
            rec     <= rec_in;
            sat_evt <= 1'b0;              // sticky is per-record (RAM walk clears)
        end else if (evt_fire || hl_sh) begin
            rec <= (evt_fire && full0) ? based : (evt_fire ? bumped : based);
            if (evt_fire && full0)
                sat_evt <= 1'b1;          // lost cofire: visible, counted
        end
    end

    assign rec_out = rec;

    // readout adder tree: bucket i placed at bit offset (K-1-i)*B  =>  Ŵ = P·2^-((K-1)B)
    wire [K*B-1:0] w [0:K-1];
    wire [K*B-1:0] t [0:K-1];
    genvar gi;
    generate
        for (gi = 0; gi < K; gi = gi + 1) begin : ro
            if (gi == 0) begin : b0            // avoid zero-width replication
                assign w[0] = {rec[B-1:0], {((K-1)*B){1'b0}}};
            end else begin : bi
                assign w[gi] = {{(gi*B){1'b0}}, rec[(gi+1)*B-1 -: B],
                                {((K-1-gi)*B){1'b0}}};
            end
        end
        assign t[0] = w[0];
        for (gi = 1; gi < K; gi = gi + 1) begin : tr
            assign t[gi] = t[gi-1] + w[gi];
        end
    endgenerate
    assign p_ro = t[K-1];
endmodule
