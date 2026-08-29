// PROVENANCE: proposals/opencode/RTL-SKETCH.md (round-1 competition entry: opencode)
// q_divu.v -- bit-serial restoring divider, unsigned, truncated quotient.
module q_divu #(
    parameter WN   = 63,   // numerator / quotient width (<= 64)
    parameter WD   = 32,   // denominator width
    parameter BIBW = 6     // >= clog2(WN)
)(
    input  wire            clk,
    input  wire            rst_n,
    input  wire            i_start,
    input  wire [WN-1:0]   i_num,
    input  wire [WD-1:0]   i_den,
    output reg             o_busy,
    output reg  [WN-1:0]   o_quot,
    output reg             o_zerr,
    output reg             o_done
);
    reg [BIBW-1:0] bi;
    reg [WN-1:0]   num;
    reg [WD-1:0]   den;
    reg [WD:0]     rem;
    reg [WN-1:0]   quot;

    wire [WD:0]   remn  = {rem[WD-1:0], num[WN-1]};
    wire          ge    = (den != {WD{1'b0}}) && (remn >= {1'b0, den});
    wire [WN-1:0] quotn = {quot[WN-2:0], ge};

    always @(posedge clk) begin
        if (!rst_n) begin
            o_busy <= 1'b0;
            o_done <= 1'b0;
            o_quot <= {WN{1'b0}};
            o_zerr <= 1'b0;
            bi     <= {BIBW{1'b0}};
            num    <= {WN{1'b0}};
            den    <= {WD{1'b0}};
            rem    <= {(WD+1){1'b0}};
            quot   <= {WN{1'b0}};
        end else begin
            o_done <= 1'b0;
            if (i_start && !o_busy) begin
                num    <= i_num;
                den    <= i_den;
                quot   <= {WN{1'b0}};
                rem    <= {(WD+1){1'b0}};
                bi     <= WN - 1;
                o_zerr <= (i_den == {WD{1'b0}});
                o_busy <= 1'b1;
            end else if (o_busy) begin
                num  <= num << 1;
                quot <= quotn;
                rem  <= ge ? (remn - {1'b0, den}) : remn;
                if (bi == {{BIBW-1{1'b0}}, 1'b0}) begin
                    o_quot  <= quotn;
                    o_busy  <= 1'b0;
                    o_done  <= 1'b1;
                end else begin
                    bi <= bi - {{BIBW-1{1'b0}}, 1'b0};
                end
            end
        end
    end

endmodule
