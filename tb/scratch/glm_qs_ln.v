// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
module qs_ln #(
    parameter IW   = 73,   // = K*B + 1 for K=12, B=6 (wrapper passes K*B+1)
    parameter FRAC = 66,   // = (K-1)*B of the calling edge ladder
    parameter OW   = 16    // signed Q4.12 output
)(
    input  wire                clk,
    input  wire                rst_n,
    input  wire                start,
    input  wire [IW-1:0]       y,       // >= 1 required (caller guarantees)
    output reg                 done,
    output reg  signed [OW-1:0] lq,     // ln(y) - FRAC*ln2,  Q4.12, saturated
    output reg                 sat_sticky
);
    function [23:0] coffs;              // constant function: FRAC * ln2 * 4096
        input integer f;
        begin
            coffs = f * 2839;           // round(ln2 * 2^12) = 2839
        end
    endfunction
    localparam [23:0] OFFS = coffs(FRAC);

    function [11:0] lntab;              // ln(1 + i/16) in Q4.12, i = 0..16
        input [4:0] i;
        begin
            case (i)
                5'd0:  lntab = 12'd0;     5'd1:  lntab = 12'd248;
                5'd2:  lntab = 12'd481;   5'd3:  lntab = 12'd704;
                5'd4:  lntab = 12'd914;   5'd5:  lntab = 12'd1114;
                5'd6:  lntab = 12'd1304;  5'd7:  lntab = 12'd1486;
                5'd8:  lntab = 12'd1661;  5'd9:  lntab = 12'd1828;
                5'd10: lntab = 12'd1989;  5'd11: lntab = 12'd2143;
                5'd12: lntab = 12'd2292;  5'd13: lntab = 12'd2436;
                5'd14: lntab = 12'd2575;  5'd15: lntab = 12'd2709;
                5'd16: lntab = 12'd2839;  default: lntab = 12'd0;
            endcase
        end
    endfunction

    reg        st;                     // 0 idle, 1 combine
    reg [6:0]  e_r;
    reg [15:0] f_r;
    reg        zero_r;
    integer k;

    // stage 1 (combinational, registered on start): leading-one normalize.
    // Sketch form: iterative shift; real rtl swaps in a casez priority encoder.
    reg [IW-1:0] ysh;
    reg [6:0]    e;
    always @(*) begin
        ysh = y;  e = 0;
        for (k = 0; k < IW; k = k + 1)
            if (ysh[IW-1] == 1'b0) begin
                ysh = {ysh[IW-2:0], 1'b0};
                e   = e + 1;
            end
    end

    // stage 2 (combinational from registered e_r/f_r): LUT + interp + offsets
    wire [3:0]  idx  = f_r[15:12];
    wire [3:0]  sub  = f_r[11:8];
    wire [11:0] diff = lntab({1'b0, idx} + 5'd1) - lntab({1'b0, idx});
    wire [15:0] prod = diff * {8'b0, sub};         // 12x4 multiply
    wire [11:0] lnm  = lntab({1'b0, idx}) + prod[15:4];
    wire [18:0] eln  = e_r * 12'd2839;             // constant multiply (CSD-friendly)
    wire signed [23:0] full_s = $signed({5'b0, eln}) + $signed({12'b0, lnm})
                              - $signed(OFFS);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= 1'b0; done <= 1'b0; lq <= 16'sd0; sat_sticky <= 1'b0;
            e_r <= 7'd0; f_r <= 16'd0; zero_r <= 1'b0;
        end else begin
            done <= 1'b0;
            if (!st) begin
                if (start) begin
                    e_r    <= e;
                    f_r    <= ysh[IW-2 -: 16];
                    zero_r <= (y == {IW{1'b0}});
                    st     <= 1'b1;
                end
            end else begin
                if (zero_r) begin
                    lq <= 16'sd0;  sat_sticky <= 1'b1;   // ln(0) flagged, not lied about
                end else if (full_s > 24'sd32767) begin
                    lq <= 16'sd32767;  sat_sticky <= 1'b1;
                end else if (full_s < -24'sd32768) begin
                    lq <= -16'sd32768;  sat_sticky <= 1'b1;
                end else begin
                    lq <= full_s[15:0];
                end
                done <= 1'b1;
                st   <= 1'b0;
            end
        end
    end
endmodule
