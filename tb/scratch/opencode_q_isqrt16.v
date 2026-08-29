// PROVENANCE: proposals/opencode/RTL-SKETCH.md (round-1 competition entry: opencode)
// q_isqrt16.v -- bit-serial integer square root, 32-bit in, 16-bit out.
module q_isqrt16 (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        i_start,
    input  wire [31:0] i_arg,
    output reg         o_busy,
    output reg  [15:0] o_root,
    output reg         o_done
);
    reg [3:0]  bi;
    reg [31:0] arg_r;
    reg [15:0] root;

    wire [16:0] cand = root | (17'd1 << bi);
    wire [33:0] c2   = cand * cand;
    wire        keep = (c2 <= {2'b0, arg_r});

    always @(posedge clk) begin
        if (!rst_n) begin
            o_busy <= 1'b0;
            o_done <= 1'b0;
            o_root <= 16'd0;
            bi     <= 4'd0;
            arg_r  <= 32'd0;
            root   <= 16'd0;
        end else begin
            o_done <= 1'b0;
            if (i_start && !o_busy) begin
                arg_r  <= i_arg;
                root   <= 16'd0;
                bi     <= 4'd15;
                o_busy <= 1'b1;
            end else if (o_busy) begin
                if (keep)
                    root <= cand[15:0];
                if (bi == 4'd0) begin
                    o_root <= keep ? cand[15:0] : root;
                    o_busy <= 1'b0;
                    o_done <= 1'b1;
                end else begin
                    bi <= bi - 4'd1;
                end
            end
        end
    end

endmodule
