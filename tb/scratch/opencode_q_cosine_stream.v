// PROVENANCE: proposals/opencode/RTL-SKETCH.md (round-1 competition entry: opencode)
// q_cosine_stream.v -- streaming cosine similarity, Q1.15 in/out.
//   dot, sxq, syq accumulate in Q2.30 + guard bits (ABW).
//   mx = isqrt(sxq >> log2(VW)); my likewise (VW power of two).
//   cos = (|dot| << 15) / (mx*my), sign reapplied, clamped to Q1.15.
module q_cosine_stream #(
    parameter PW  = 16,
    parameter VW  = 8,          // beats, power of two, <= 256
    parameter ABW = 2*PW + 8,   // accumulator width (40 default)
    parameter NBW = ABW + PW    // divider numerator width (56 default)
)(
    input  wire                 clk,
    input  wire                 rst_n,

    input  wire                 i_start,
    output reg                  o_busy,

    input  wire                 i_beat,
    input  wire signed [PW-1:0] i_x,
    input  wire signed [PW-1:0] i_y,

    output reg  signed [PW-1:0] o_cos,
    output reg                  o_err,
    output reg                  o_done
);
    localparam LGW = (VW <= 1)   ? 0 :
                     (VW <= 2)   ? 1 :
                     (VW <= 4)   ? 2 :
                     (VW <= 8)   ? 3 :
                     (VW <= 16)  ? 4 :
                     (VW <= 32)  ? 5 :
                     (VW <= 64)  ? 6 : 7;

    localparam [2:0] ST_IDLE = 3'd0, ST_ACC = 3'd1, ST_SQX = 3'd2,
                     ST_SQY  = 3'd3, ST_DIV = 3'd4;

    reg [2:0]            state;
    reg [5:0]            cnt;
    reg signed [ABW-1:0] dot, sxq, syq;
    reg [PW-1:0]         mx, my;
    reg                  dneg;
    reg                  sq_start, dv_start;

    wire signed [2*PW-1:0] xy = i_x * i_y;
    wire signed [2*PW-1:0] xx = i_x * i_x;
    wire signed [2*PW-1:0] yy = i_y * i_y;

    wire [31:0] sxn = sxq >> LGW;   // nonnegative by construction
    wire [31:0] syn = syq >> LGW;

    wire signed [ABW-1:0] dot_abs = dot[ABW-1] ? (~dot + 1'b1) : dot;
    wire [NBW-1:0]        dnum    = {dot_abs, {PW{1'b0}}};
    wire [2*PW-1:0]       dden    = mx * my;

    wire        sq_busy, sq_done, dv_busy, dv_done, dv_zerr;
    wire [15:0] sq_root;
    wire [NBW-1:0] dv_quot;

    q_isqrt16 u_sqrt (
        .clk(clk), .rst_n(rst_n),
        .i_start(sq_start),
        .i_arg  (state == ST_SQX ? sxn : syn),
        .o_busy (sq_busy), .o_root(sq_root), .o_done(sq_done)
    );

    q_divu #(.WN(NBW), .WD(2*PW), .BIBW(6)) u_div (
        .clk(clk), .rst_n(rst_n),
        .i_start(dv_start),
        .i_num  (dnum), .i_den(dden),
        .o_busy (dv_busy), .o_quot(dv_quot),
        .o_zerr (dv_zerr), .o_done(dv_done)
    );

    wire [PW-1:0] q16 = dv_quot[PW-1:0];

    always @(posedge clk) begin
        if (!rst_n) begin
            state    <= ST_IDLE;
            o_busy   <= 1'b0;
            o_done   <= 1'b0;
            o_err    <= 1'b0;
            o_cos    <= {PW{1'b0}};
            cnt      <= 6'd0;
            dot      <= {ABW{1'b0}};
            sxq      <= {ABW{1'b0}};
            syq      <= {ABW{1'b0}};
            mx       <= {PW{1'b0}};
            my       <= {PW{1'b0}};
            dneg     <= 1'b0;
            sq_start <= 1'b0;
            dv_start <= 1'b0;
        end else begin
            o_done   <= 1'b0;
            sq_start <= 1'b0;
            dv_start <= 1'b0;

            case (state)
              ST_IDLE:
                if (i_start) begin
                    dot    <= {ABW{1'b0}};
                    sxq    <= {ABW{1'b0}};
                    syq    <= {ABW{1'b0}};
                    cnt    <= 6'd0;
                    o_busy <= 1'b1;
                    state  <= ST_ACC;
                end
              ST_ACC:
                if (i_beat) begin
                    dot <= dot + xy;
                    sxq <= sxq + xx;
                    syq <= syq + yy;
                    if (cnt == VW - 1) begin
                        dneg     <= ((dot + xy) < 0);
                        sq_start <= 1'b1;
                        state    <= ST_SQX;
                    end else begin
                        cnt <= cnt + 6'd1;
                    end
                end
              ST_SQX:
                if (sq_done) begin
                    mx       <= sq_root;
                    sq_start <= 1'b1;      // restart on y
                    state    <= ST_SQY;
                end
              ST_SQY:
                if (sq_done) begin
                    my       <= sq_root;
                    dv_start <= 1'b1;
                    state    <= ST_DIV;
                end
              ST_DIV:
                if (dv_done) begin
                    o_err  <= dv_zerr;
                    if (dv_zerr)
                        o_cos <= {PW{1'b0}};
                    else if (dneg)
                        o_cos <= (q16 >= 16'h8000) ? 16'h8000
                                                  : (~q16 + 1'b1);
                    else
                        o_cos <= (q16 >= 16'h8000) ? 16'h7FFF : q16;
                    o_done <= 1'b1;
                    o_busy <= 1'b0;
                    state  <= ST_IDLE;
                end
              default: state <= ST_IDLE;
            endcase
        end
    end

endmodule
