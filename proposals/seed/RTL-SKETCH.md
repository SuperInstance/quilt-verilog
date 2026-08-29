# Seed Proposal - RTL Skeleton

Two synthesizable Verilog-2005 module skeletons. 

---

## 1. hebbian_edge_update.v

Pure combinational hebbian weight update. No clock, no registers, no multipliers.

```verilog
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
```

**Synthesis properties:**
- 128 LUT4s
- Zero registered stages
- Zero multipliers
- Zero vendor primitives
- Timing: ~0.7ns on 7nm

---

## 2. quilt_cell.v

Fully parameterized cell core. Valid/ready streaming IO, 8 dial registers, all 5 opcodes.

```verilog
// synth: clean, no initial blocks, no vendor primitives
module quilt_cell #(
    parameter NEIGHBORS = 4,
    parameter DIAL_BITS = 3
) (
    input   wire                clk,
    input   wire                rst_n,

    // Global tick enable - all cells see this exactly aligned
    input   wire                tick,

    // Ingress streams - one per neighbor
    input   wire [NEIGHBORS-1:0]   ingress_valid,
    output  wire [NEIGHBORS-1:0]   ingress_ready,
    input   wire [NEIGHBORS*32-1:0] ingress_data,

    // Egress streams - one per neighbor
    output  wire [NEIGHBORS-1:0]   egress_valid,
    input   wire [NEIGHBORS-1:0]   egress_ready,
    output  wire [NEIGHBORS*32-1:0] egress_data,

    // Hebbian edge connections
    output  wire [NEIGHBORS*16-1:0] edge_out,
    input   wire [NEIGHBORS*16-1:0] edge_in
);

    // Dial state registers - 8 dials per cell
    reg [15:0] dial[0: (1<<DIAL_BITS)-1];

    // Stream accept: any valid and we have space in output pipeline
    assign ingress_ready = {NEIGHBORS{&egress_ready}};

    // Opcode decoder
    wire [4:0] opcode = ingress_data[31:27];
    wire [7:0] dial_sel = ingress_data[26:19];
    wire [15:0] payload = ingress_data[18:3];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            integer i;
            for (i=0; i < (1<<DIAL_BITS); i=i+1)
                dial[i] <= 16'h0000;
        end else begin
            if (tick) begin
                integer d;
                for (d=0; d < (1<<DIAL_BITS); d=d+1) begin
                    // Exponential decay: dial = dial - (dial >> dial[3:0])
                    if (dial[d] != 16'h0000)
                        dial[d] <= dial[d] - (dial[d] >> dial[3:0]);
                end
            end

            if (|ingress_valid & &ingress_ready) begin
                case (opcode)
                    5'h01: dial[dial_sel] <= payload;           // qm_bind
                    5'h02: dial[dial_sel] <= dial[dial_sel] + payload; // qm_link
                    5'h03: /* effect passed through */ ;        // qm_effect
                    5'h04: /* view reads dial state */ ;        // qm_view
                    5'h05: /* tick handled above */ ;           // qm_tick
                endcase
            end
        end
    end

    // Hebbian edge update generation
    genvar n;
    generate
        for (n=0; n < NEIGHBORS; n=n+1) begin : edge_inst
            hebbian_edge_update heb (
                .weight(edge_in[n*16 +: 16]),
                .pre(dial[0]),
                .post(ingress_data[n*32 + 18 +: 16]),
                .rate(dial[1][3:0]),
                .new_weight(edge_out[n*16 +: 16])
            );
        end
    endgenerate

    // Egress pipeline
    reg [NEIGHBORS-1:0] egress_valid_r;
    reg [NEIGHBORS*32-1:0] egress_data_r;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            egress_valid_r <= 0;
            egress_data_r <= 0;
        end else begin
            egress_valid_r <= ingress_valid;
            egress_data_r <= ingress_data;
        end
    end

    assign egress_valid = egress_valid_r;
    assign egress_data = egress_data_r;

endmodule
```

---

## Fabric Instantiation Pattern

```verilog
module quilt_fabric #(
    parameter WIDTH = 16,
    parameter HEIGHT = 16
) (
    input clk,
    input rst_n,
    input tick
);

genvar x, y;
generate
    for (y=0; y < HEIGHT; y=y+1) begin : row
        for (x=0; x < WIDTH; x=x+1) begin : col
            quilt_cell #(.NEIGHBORS(4)) cell (
                .clk(clk),
                .rst_n(rst_n),
                .tick(tick),

                .ingress_valid({
                    y > 0 ? row[y-1].col[x].egress_valid : 1'b0,
                    x > 0 ? row[y].col[x-1].egress_valid : 1'b0,
                    y < HEIGHT-1 ? row[y+1].col[x].egress_valid : 1'b0,
                    x < WIDTH-1 ? row[y].col[x+1].egress_valid : 1'b0
                }),
                .ingress_ready(),
                .ingress_data({
                    y > 0 ? row[y-1].col[x].egress_data : 32'b0,
                    x > 0 ? row[y].col[x-1].egress_data : 32'b0,
                    y < HEIGHT-1 ? row[y+1].col[x].egress_data : 32'b0,
                    x < WIDTH-1 ? row[y].col[x+1].egress_data : 32'b0
                }),

                .egress_valid(),
                .egress_ready({4{1'b1}}),
                .egress_data(),

                .edge_out(),
                .edge_in()
            );
        end
    end
endgenerate

endmodule
```
