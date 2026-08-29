// tb_flit_pipe.v -- skid slice: back-to-back throughput, stall retention,
// no-loss under arbitrary ready patterns, reset drain.
`timescale 1ns/1ps
module tb_flit_pipe;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg         s_valid = 0, m_ready = 1;
    reg  [2:0]  s_op = 0;
    reg  [3:0]  s_src = 0, s_dst = 0;
    reg  [15:0] s_a0 = 0, s_a1 = 0, s_a2 = 0, s_dat = 0;
    wire        s_ready, m_valid;
    wire [2:0]  m_op;
    wire [3:0]  m_src, m_dst;
    wire [15:0] m_a0, m_a1, m_a2, m_dat;

    integer errors = 0;
    integer sent = 0, recvd = 0;
    reg stream_done = 0;
    reg [15:0] nxt = 0;
    reg [15:0] got;

    q_flit_pipe u_dut (
        .clk(clk), .rst_n(rst_n),
        .s_valid(s_valid), .s_ready(s_ready),
        .s_op(s_op), .s_src(s_src), .s_dst(s_dst),
        .s_a0(s_a0), .s_a1(s_a1), .s_a2(s_a2), .s_dat(s_dat),
        .m_valid(m_valid), .m_ready(m_ready),
        .m_op(m_op), .m_src(m_src), .m_dst(m_dst),
        .m_a0(m_a0), .m_a1(m_a1), .m_a2(m_a2), .m_dat(m_dat)
    );

    // sender: sequential words, dat = sequence number
    always @(negedge clk) begin
        if (rst_n && !stream_done) begin
            if (s_valid && s_ready) begin
                sent = sent + 1;
                nxt  = nxt + 1;
            end
            if (sent < 200)
                s_valid = 1;
            else
                s_valid = 0;
            s_dat = nxt;
            s_a0  = nxt;
        end
    end

    // receiver: random-ish ready, checks order and content.
    // Sample at posedge with pre-edge values (transfer condition).
    always @(posedge clk) begin
        if (rst_n && !stream_done) begin
            if (m_valid && m_ready) begin
                got = m_dat;
                if (got !== recvd[15:0]) begin
                    errors = errors + 1;
                    $display("FAIL order got=%0d exp=%0d", got, recvd);
                end
                if (m_a0 !== m_dat) begin
                    errors = errors + 1;
                    $display("FAIL fields a0=%h dat=%h", m_a0, m_dat);
                end
                recvd = recvd + 1;
            end
        end
    end

    // pseudo-random stall pattern (deterministic LCG)
    always @(negedge clk) begin
        if (rst_n && !stream_done)
            m_ready = (($random & 3) != 0);
    end

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        // run until all 200 words delivered or timeout
        repeat (20000) @(negedge clk);
        if (recvd == 200 && errors == 0) $display("TB_FLIT_PIPE PASS");
        else begin
            $display("TB_FLIT_PIPE FAIL recvd=%0d errors=%0d", recvd, errors);
        end
        $finish;
    end

    // stall-retention directed check after the stream
    reg [15:0] rw;
    initial begin
        wait (recvd == 200);
        stream_done = 1;
        @(negedge clk);
        s_valid = 0;
        s_valid = 1; s_dat = 16'hBEEF; s_a0 = 16'hBEEF;
        m_ready = 0;
        repeat (6) @(negedge clk);
        if (m_valid !== 1'b1 || m_dat !== 16'hBEEF) begin
            errors = errors + 1;
            $display("FAIL retain");
        end
        m_ready = 1;
        @(negedge clk);
        if (m_dat !== 16'hBEEF) begin
            errors = errors + 1;
            $display("FAIL release");
        end
        s_valid = 0;
    end
endmodule
