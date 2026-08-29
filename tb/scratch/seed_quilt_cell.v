// PROVENANCE: proposals/seed/RTL-SKETCH.md (round-1 competition entry: seed)
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
