// PROVENANCE: proposals/opencode/RTL-SKETCH.md (round-1 competition entry: opencode)
// q_flit_pipe.v -- registered valid/ready flit slice for the ring spine.
module q_flit_pipe #(
    parameter OPW  = 3,
    parameter AIDW = 4,
    parameter PW   = 16
)(
    input  wire               clk,
    input  wire               rst_n,

    input  wire               s_valid,
    output wire               s_ready,
    input  wire [OPW-1:0]     s_op,
    input  wire [AIDW-1:0]    s_src,
    input  wire [AIDW-1:0]    s_dst,
    input  wire [PW-1:0]      s_a0,
    input  wire [PW-1:0]      s_a1,
    input  wire [PW-1:0]      s_a2,
    input  wire [PW-1:0]      s_dat,

    output wire               m_valid,
    input  wire               m_ready,
    output wire [OPW-1:0]     m_op,
    output wire [AIDW-1:0]    m_src,
    output wire [AIDW-1:0]    m_dst,
    output wire [PW-1:0]      m_a0,
    output wire [PW-1:0]      m_a1,
    output wire [PW-1:0]      m_a2,
    output wire [PW-1:0]      m_dat
);
    localparam FW = OPW + 2*AIDW + 4*PW;

    reg            vq;
    reg [FW-1:0]   dq;

    wire [FW-1:0] s_bus = {s_op, s_src, s_dst, s_a0, s_a1, s_a2, s_dat};

    assign {m_op, m_src, m_dst, m_a0, m_a1, m_a2, m_dat} = dq;
    assign m_valid = vq;
    assign s_ready = !vq || m_ready;

    always @(posedge clk) begin
        if (!rst_n) begin
            vq <= 1'b0;
            dq <= {FW{1'b0}};
        end else if (s_valid && s_ready) begin
            dq <= s_bus;
            vq <= 1'b1;
        end else if (m_ready) begin
            vq <= 1'b0;
        end
    end

endmodule
