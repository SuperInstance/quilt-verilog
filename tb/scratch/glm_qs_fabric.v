// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
module qs_fabric #(
    parameter N_CELLS        = 16,      // <= 2^CID_W - 1 (host id reserved)
    parameter CID_W          = 8,
    parameter DW             = 16,
    parameter TTL_W          = 4,
    parameter E_LOG2         = 6,
    parameter K              = 12,
    parameter B              = 6,
    parameter BASE_W         = 8,
    parameter TICK_DIV       = 16,      // < 2^24
    parameter HALF_LIFE_TICKS= 65536,   // any value < 2^24; the "90 days"
    parameter REG_SLICE_EVERY= 0        // 0 = plain chain
)(
    input  wire clk,
    input  wire rst_n,
    // external seam: injection and egress (host id = all-ones)
    input  wire                    in_valid,
    output wire                    in_ready,
    input  wire [DW+3+2*CID_W+TTL_W-1:0] in_flit,
    output wire                    out_valid,
    input  wire                    out_ready,
    output wire [DW+3+2*CID_W+TTL_W-1:0] out_flit,
    // tick bus (broadcast)
    output wire                    tick_stb,
    output wire                    hl_stb,
    output wire [15:0]             tick_cnt
);
    localparam FLIT_W = DW + 3 + 2*CID_W + TTL_W;
    localparam [CID_W-1:0] EXT_ID = {CID_W{1'b1}};

    // ---- per-cell link bundles ----
    wire [FLIT_W-1:0] pre_f [0:N_CELLS-1];
    wire [N_CELLS-1:0] pre_v, pre_r;
    wire [FLIT_W-1:0] dn_f  [0:N_CELLS-1];
    wire [N_CELLS-1:0] dn_v, dn_r;

    genvar gi;
    generate
        for (gi = 0; gi < N_CELLS; gi = gi + 1) begin : cellring
            qs_cell #(
                .DW(DW), .CID_W(CID_W), .TTL_W(TTL_W), .E_LOG2(E_LOG2),
                .K(K), .B(B), .BASE_W(BASE_W),
                .CELL_ID(gi)          // truncated to CID_W inside; N_CELLS
                                       // legality (< 2^CID_W) is a wrapper check
            ) u_cell (
                .clk(clk), .rst_n(rst_n),
                .us_flit(pre_f[gi]), .us_valid(pre_v[gi]), .us_ready(pre_r[gi]),
                .ds_flit(dn_f[gi]),  .ds_valid(dn_v[gi]),  .ds_ready(dn_r[gi]),
                .tick_stb(tick_stb), .hl_stb(hl_stb), .tick_cnt(tick_cnt)
            );
        end
        // interior links (cell gi -> cell gi+1), optional register slices
        for (gi = 0; gi < N_CELLS-1; gi = gi + 1) begin : link
            if (REG_SLICE_EVERY != 0 && ((gi+1) % REG_SLICE_EVERY == 0)) begin : sliced
                reg              v_q;
                reg [FLIT_W-1:0] f_q;
                wire             acc = !v_q || pre_r[gi+1];
                always @(posedge clk or negedge rst_n) begin
                    if (!rst_n) v_q <= 1'b0;
                    else if (acc) begin v_q <= dn_v[gi]; f_q <= dn_f[gi]; end
                end
                assign dn_r[gi]    = acc;
                assign pre_v[gi+1] = v_q;
                assign pre_f[gi+1] = f_q;
            end else begin : direct
                assign pre_v[gi+1] = dn_v[gi];
                assign pre_f[gi+1] = dn_f[gi];
                assign dn_r[gi]    = pre_r[gi+1];
            end
        end
    endgenerate

    // ---- seam: wrap has priority over external injection ----
    wire              seam_v = dn_v[N_CELLS-1];
    wire [FLIT_W-1:0] seam_f = dn_f[N_CELLS-1];
    wire              to_ext = seam_v && (seam_f[DW+3+CID_W-1:DW+3] == EXT_ID);
    wire              wrap_v = seam_v && !to_ext;

    assign out_valid = to_ext;
    assign out_flit  = seam_f;
    assign dn_r[N_CELLS-1] = to_ext ? out_ready : pre_r[0];
    assign pre_v[0]  = wrap_v || in_valid;
    assign pre_f[0]  = wrap_v ? seam_f : in_flit;
    assign in_ready  = !wrap_v && pre_r[0];

    // ---- global heartbeat ----
    qs_tickgen #(.TICK_DIV(TICK_DIV), .HL_TICKS(HALF_LIFE_TICKS)) u_tg (
        .clk(clk), .rst_n(rst_n),
        .tick_stb(tick_stb), .hl_stb(hl_stb), .tick_cnt(tick_cnt)
    );
endmodule
