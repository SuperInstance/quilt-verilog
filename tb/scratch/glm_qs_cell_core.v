// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
module qs_cell_core #(
    parameter DW     = 16,
    parameter CID_W  = 8,
    parameter TTL_W  = 4,
    parameter E_LOG2 = 6,             // edges per cell = 2^E_LOG2
    parameter K      = 12,
    parameter B      = 6,
    parameter BASE_W = 8
)(
    input  wire                 clk,
    input  wire                 rst_n,
    input  wire [CID_W-1:0]     my_id,
    // qstream ingress / egress
    input  wire [DW+3+2*CID_W+TTL_W-1:0] us_flit,
    input  wire                 us_valid,
    output wire                 us_ready,
    output wire [DW+3+2*CID_W+TTL_W-1:0] ds_flit,
    output wire                 ds_valid,
    input  wire                 ds_ready,
    // edge RAM (sync single port, inferred in qs_cell wrapper)
    output reg  [E_LOG2-1:0]    eram_addr,
    output reg                  eram_we,
    output reg  [1+CID_W+K*B+BASE_W-1:0] eram_din,
    input  wire [1+CID_W+K*B+BASE_W-1:0] eram_dout,
    // ladder ALU
    output reg                  he_ld, he_evt, he_sh,
    input  wire [K*B-1:0]       he_ro,
    input  wire [K*B-1:0]       he_rec_out,
    input  wire                 he_sat,
    // ln unit
    output reg                  ln_start,
    input  wire                 ln_done,
    input  wire signed [15:0]   ln_q,
    // dials (qs_dial instances live in the wrapper)
    output reg  [1:0]           dial_sel,
    output reg                  dial_we,
    output reg                  dial_nudge,
    output reg  signed [DW-1:0] dial_delta,
    // tick bus
    input  wire                 tick_evt,
    input  wire                 hl_strobe
);
    localparam FLIT_W = DW + 3 + 2*CID_W + TTL_W;
    localparam EDGE_W = 1 + CID_W + K*B + BASE_W;

    // ---- intake skid: us_ready is a function of internal state only ----
    reg             in_v;
    reg [FLIT_W-1:0] in_f;
    wire [2:0]       iop  = in_f[DW+2:DW];
    wire [CID_W-1:0] idst = in_f[DW+3+CID_W-1:DW+3];
    wire [CID_W-1:0] isrc = in_f[DW+3+2*CID_W-1:DW+3+CID_W];
    wire [TTL_W-1:0] ittl = in_f[FLIT_W-1:FLIT_W-TTL_W];
    wire [DW-1:0]    idat = in_f[DW-1:0];
    wire             imine = (idst == my_id);

    // ---- bypass register ----
    reg              bp_v;
    reg [FLIT_W-1:0] bp_f;
    reg              ttl_drop_sticky;
    wire             bp_room = !bp_v || ds_ready;
    wire             bp_take = in_v && !imine && bp_room;   // move to bypass

    // ---- response register (FSM is the sole writer) ----
    reg              resp_v;
    reg [FLIT_W-1:0] resp_f;

    // FSM intake condition (mine + idle)
    wire core_take = in_v && imine && (st == S_IDLE) && !hl_strobe;

    assign us_ready = !in_v || core_take || bp_take;  // payload-independent

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            in_v <= 1'b0; in_f <= {FLIT_W{1'b0}};
            bp_v <= 1'b0; bp_f <= {FLIT_W{1'b0}}; ttl_drop_sticky <= 1'b0;
        end else begin
            if (bp_take) begin
                if (ittl <= {{TTL_W{1'b0}}}) begin
                    ttl_drop_sticky <= 1'b1;     // v1.1: also emit err flit
                    in_v <= 1'b0;
                end else begin
                    bp_v <= 1'b1;
                    bp_f <= in_f;
                    bp_f[FLIT_W-1:FLIT_W-TTL_W] <= ittl - {{(TTL_W-1){1'b0}},1'b1};
                    in_v <= 1'b0;
                end
            end else if (core_take) begin
                in_v <= 1'b0;                    // FSM latches fields this edge
            end else if (!in_v && us_valid) begin
                in_v <= 1'b1;  in_f <= us_flit;
            end
            // else: hold (backpressure via us_ready = 0 when full)
        end
    end

    // ---- egress mux: bypass has priority; responses wait their turn ----
    assign ds_valid = bp_v | resp_v;
    assign ds_flit  = bp_v ? bp_f : resp_f;

    // ---- edge record fields of eram_dout ----
    wire              e_use  = eram_dout[0];
    wire [CID_W-1:0]  e_dst  = eram_dout[1+:CID_W];
    wire [BASE_W-1:0] e_base = eram_dout[1+CID_W+K*B +: BASE_W];

    // strength = saturate(base:Q4.4 -> Q4.12 + ln_q)
    wire signed [19:0] s20 = $signed({{4{1'b0}}, e_base, 8'b0}) + {{4{ln_q[15]}}, ln_q};

    localparam S_IDLE=0, S_DECODE=1, S_SCAN_SET=2, S_SCAN_CHK=3,
               S_LINK_LD=4, S_LINK_EVT=5, S_LINK_WB=6,
               S_VIEW_LD=7, S_VIEW_LN=8, S_VIEW_W=9, S_RESP=10,
               S_EFF=11, S_TW_SET=12, S_TW_CHK=13, S_TW_LD=14, S_TW_WB=15;
    reg [3:0]   st;
    reg [2:0]   op_r;
    reg [CID_W-1:0] dst_r, src_r;
    reg [DW-1:0]    dat_r;
    reg [E_LOG2-1:0] scan_idx, alloc_idx;
    reg         fresh_r;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= S_IDLE; op_r <= 3'd0; dst_r <= 0; src_r <= 0; dat_r <= 0;
            scan_idx <= 0; alloc_idx <= 0; fresh_r <= 1'b0;
            eram_addr <= 0; eram_we <= 1'b0; eram_din <= {EDGE_W{1'b0}};
            he_ld <= 1'b0; he_evt <= 1'b0; he_sh <= 1'b0;
            ln_start <= 1'b0; dial_sel <= 0; dial_we <= 1'b0;
            dial_nudge <= 1'b0; dial_delta <= 0;
            resp_v <= 1'b0; resp_f <= {FLIT_W{1'b0}};
        end else begin
            he_ld <= 1'b0; he_evt <= 1'b0; he_sh <= 1'b0;
            ln_start <= 1'b0; dial_we <= 1'b0; eram_we <= 1'b0;

            case (st)
                S_IDLE: begin
                    if (hl_strobe) begin
                        scan_idx <= 0; st <= S_TW_SET;      // half-life boundary
                    end else if (core_take) begin
                        op_r <= iop; dst_r <= idst; src_r <= isrc; dat_r <= idat;
                        st   <= S_DECODE;
                    end
                end

                S_DECODE: begin
                    case (op_r)
                        3'b001: begin scan_idx <= 0; fresh_r <= 1'b0;
                                      st <= S_SCAN_SET; end                  // link
                        3'b010: begin dial_sel <= dst_r[1:0];                // effect
                                      dial_delta <= dat_r; dial_nudge <= 1'b1;
                                      dial_we <= 1'b1; st <= S_EFF; end
                        3'b011: begin eram_addr <= dat_r[E_LOG2-1:0];        // view
                                      st <= S_VIEW_LD; end
                        3'b000: begin /* qm_bind: adapter steering cfg reg in
                                      wrapper — skeleton: single cfg write */
                                      st <= S_IDLE; end
                        default:  st <= S_IDLE;      // qm_tick: wake-cfg, v1 reg wr
                    endcase
                end

                // ---------- qm_link: find-or-alloc edge, one cofire ----------
                S_SCAN_SET: begin
                    eram_addr <= scan_idx;
                    scan_idx  <= scan_idx + {{(E_LOG2-1){1'b0}},1'b1};
                    st <= S_SCAN_CHK;
                end
                S_SCAN_CHK: begin                       // eram_dout valid here
                    if (e_use && (e_dst == dst_r)) begin
                        st <= S_LINK_LD;                // found: address holds
                    end else if (scan_idx == {E_LOG2{1'b0}}) begin
                        // full sweep, no match: allocate at tail cursor.
                        // fresh edge => skip ladder load, write ladder == 1.
                        eram_addr <= alloc_idx;
                        alloc_idx <= alloc_idx + {{(E_LOG2-1){1'b0}},1'b1};
                        fresh_r  <= 1'b1;
                        st       <= S_LINK_WB;
                    end else begin
                        st <= S_SCAN_SET;
                    end
                end
                S_LINK_LD:  begin he_ld  <= 1'b1; st <= S_LINK_EVT; end
                S_LINK_EVT: begin he_evt <= 1'b1; st <= S_LINK_WB;  end
                S_LINK_WB: begin
                    eram_we  <= 1'b1;
                    eram_din <= fresh_r
                        ? {dat_r[BASE_W-1:0], {{(K*B-1){1'b0}},1'b1}, dst_r, 1'b1}
                        : {dat_r[BASE_W-1:0], he_rec_out,           dst_r, 1'b1};
                    fresh_r <= 1'b0;
                    st      <= S_IDLE;                // base nibble rides the flit
                end

                // ---------- qm_view(strength): ladder -> ln -> +base -> resp ----------
                S_VIEW_LD: begin he_ld <= 1'b1; st <= S_VIEW_LN; end
                S_VIEW_LN: begin ln_start <= 1'b1; st <= S_VIEW_W; end
                S_VIEW_W:  if (ln_done) begin
                               dat_r <= (s20 > 20'sd32767) ? 16'h7FFF : s20[15:0];
                               st <= S_RESP;
                           end
                // (ln input y = {1'b0, he_ro} + 2^((K-1)*B) wired in the wrapper)

                S_EFF: st <= S_RESP;                   // dial write landed; ack

                S_RESP: begin
                    if (!resp_v && !bp_v) begin
                        resp_v <= 1'b1;
                        resp_f <= {{TTL_W{1'b0}}, src_r, my_id, 3'b101, dat_r};
                    end else if (resp_v && ds_ready && !bp_v) begin
                        resp_v <= 1'b0;
                        st     <= S_IDLE;
                    end
                end

                // ---------- tick walk: age every edge, 4 cycles per record ----------
                S_TW_SET: begin eram_addr <= scan_idx; st <= S_TW_CHK; end
                S_TW_CHK: begin
                    if (e_use) begin
                        st <= S_TW_LD;
                    end else if (scan_idx == {E_LOG2{1'b1}}) begin
                        st <= S_IDLE;
                    end else begin
                        scan_idx <= scan_idx + {{(E_LOG2-1){1'b0}},1'b1};
                        st <= S_TW_SET;
                    end
                end
                S_TW_LD: begin he_ld <= 1'b1; he_sh <= 1'b1; st <= S_TW_WB; end
                S_TW_WB: begin
                    eram_we  <= 1'b1;
                    eram_din <= {e_base, he_rec_out, e_dst, 1'b1};
                    if (scan_idx == {E_LOG2{1'b1}}) st <= S_IDLE;
                    else begin
                        scan_idx <= scan_idx + {{(E_LOG2-1){1'b0}},1'b1};
                        st <= S_TW_SET;
                    end
                end

                default: st <= S_IDLE;
            endcase
        end
    end
endmodule
