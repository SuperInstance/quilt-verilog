// PROVENANCE: proposals/seed/RTL-SKETCH.md (round-1 competition entry: seed)
// synth: clean, no vendor primitives
module hebbian_edge_update (
    input   [15:0]  weight,
    input   [15:0]  pre,
    input   [15:0]  post,
    input   [3:0]   rate,

    output  [15:0]  new_weight
);

    wire product_pos = pre[15] == post[15];
    wire [14:0] pre_abs  = pre[15] ? ~pre[14:0] + 1 : pre[14:0];
    wire [14:0] post_abs = post[15] ? ~post[14:0] + 1 : post[14:0];

    // Mutual bit overlap approximation of product
    wire [14:0] overlap;
    assign overlap[0]  = pre_abs[0] & post_abs[0];
    assign overlap[1]  = pre_abs[1] & post_abs[1];
    assign overlap[2]  = pre_abs[2] & post_abs[2];
    assign overlap[3]  = pre_abs[3] & post_abs[3];
    assign overlap[4]  = pre_abs[4] & post_abs[4];
    assign overlap[5]  = pre_abs[5] & post_abs[5];
    assign overlap[6]  = pre_abs[6] & post_abs[6];
    assign overlap[7]  = pre_abs[7] & post_abs[7];
    assign overlap[8]  = pre_abs[8] & post_abs[8];
    assign overlap[9]  = pre_abs[9] & post_abs[9];
    assign overlap[10] = pre_abs[10] & post_abs[10];
    assign overlap[11] = pre_abs[11] & post_abs[11];
    assign overlap[12] = pre_abs[12] & post_abs[12];
    assign overlap[13] = pre_abs[13] & post_abs[13];
    assign overlap[14] = pre_abs[14] & post_abs[14];

    // Priority encoder for highest set bit
    reg [3:0] highest_bit;
    always @(*) begin
        casex (overlap)
            15'b1xxxxxxxxxxxxxx: highest_bit = 14;
            15'b01xxxxxxxxxxxxx: highest_bit = 13;
            15'b001xxxxxxxxxxxx: highest_bit = 12;
            15'b0001xxxxxxxxxxx: highest_bit = 11;
            15'b00001xxxxxxxxxx: highest_bit = 10;
            15'b000001xxxxxxxxx: highest_bit = 9;
            15'b0000001xxxxxxxx: highest_bit = 8;
            15'b00000001xxxxxxx: highest_bit = 7;
            15'b000000001xxxxxx: highest_bit = 6;
            15'b0000000001xxxxx: highest_bit = 5;
            15'b00000000001xxxx: highest_bit = 4;
            15'b000000000001xxx: highest_bit = 3;
            15'b0000000000001xx: highest_bit = 2;
            15'b00000000000001x: highest_bit = 1;
            15'b000000000000001: highest_bit = 0;
            default:             highest_bit = 0;
        endcase
    end

    wire [15:0] delta = {1'b0, 1'b1, 14'b0} >> (14 - highest_bit + rate);
    wire [15:0] delta_signed = product_pos ? delta : (~delta + 1);

    // Saturating add
    wire [16:0] sum = {weight[15], weight} + {delta_signed[15], delta_signed};
    assign new_weight = sum[16] == sum[15] ? sum[15:0] :
                        sum[16] ? 16'hC000 : 16'h3FFF;

endmodule
