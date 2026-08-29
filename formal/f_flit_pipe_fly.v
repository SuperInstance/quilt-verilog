// formal/f_flit_pipe_fly.v -- baseline safety proof for q_flit_pipe (the
// skid-buffered flit slice used at every ring hop and every cell boundary).
//
// Re-establishes the tb/formal passing baseline (C2/C3/C4, k-induction) and
// STRENGTHENS it with value integrity (V1) so "no flit lost or duplicated"
// is literal, not just structural:
//   C2  f_in - f_out <= 2          capacity never exceeded (no over-accept)
//   C3  m_valid == (f_occ != 0)    nothing hidden, nothing presented when
//                                  empty (no drop, no phantom)
//   C4  s_ready == (f_occ < 2)     backpressure exactly at capacity
//   V1  on every m-handshake, m_dat equals the head of a 2-deep shadow FIFO
//       fed in order at the s-handshake  -> no duplication, no loss, no
//       reordering of payload words (BMC-bounded: value equality is not
//       inductive from arbitrary DUT register state, since the shadow
//       cannot be tied to DUT internals without XMRs; C2-C4 remain
//       k-inductive and are re-proven so at tb/formal/flit_pipe.sby).
// Counters bounded: f_occ is a 2-bit wrap-loud shadow (C2 catches wrap at 3).
//
// No XMRs (yosys Verilog frontend turns dut.* refs into undriven wires);
// everything is proven at the module boundary. Reset preamble: DUT regs have
// no init values, so the first two timesteps are forced into reset.
module f_flit_pipe_fly(input clk, input rst_n);
    localparam OPW = 3, AIDW = 4, PW = 16;

    reg              s_valid;
    wire             s_ready;
    reg [OPW-1:0]    s_op;
    reg [AIDW-1:0]   s_src, s_dst;
    reg [PW-1:0]     s_a0, s_a1, s_a2, s_dat;
    wire             m_valid;
    reg              m_ready;
    wire [OPW-1:0]   m_op;
    wire [AIDW-1:0]  m_src, m_dst;
    wire [PW-1:0]    m_a0, m_a1, m_a2, m_dat;

    q_flit_pipe #(.OPW(OPW), .AIDW(AIDW), .PW(PW)) dut (
        .clk(clk), .rst_n(rst_n),
        .s_valid(s_valid), .s_ready(s_ready),
        .s_op(s_op), .s_src(s_src), .s_dst(s_dst),
        .s_a0(s_a0), .s_a1(s_a1), .s_a2(s_a2), .s_dat(s_dat),
        .m_valid(m_valid), .m_ready(m_ready),
        .m_op(m_op), .m_src(m_src), .m_dst(m_dst),
        .m_a0(m_a0), .m_a1(m_a1), .m_a2(m_a2), .m_dat(m_dat)
    );

    // reset preamble
    reg [1:0] f_rstctr = 0;
    always @(posedge clk)
        if (f_rstctr < 2) f_rstctr <= f_rstctr + 1;
    always @(*)
        if (f_rstctr < 2) assume (!rst_n);

    // free inputs
    always @(posedge clk) begin
        s_valid <= $anyseq;
        m_ready <= $anyseq;
        {s_op, s_src, s_dst, s_a0, s_a1, s_a2, s_dat} <= $anyseq;
    end

    // shadow occupancy: +1 on accept, -1 on emit, reset-aware
    reg  [1:0] f_occ = 0;
    wire       f_nonempty = f_occ != 0;
    wire       f_notfull  = f_occ < 2;
    always @(posedge clk) begin
        if (!rst_n)
            f_occ <= 0;
        else
            f_occ <= f_occ + (s_valid && s_ready) - (m_valid && m_ready);
    end

    // shadow payload FIFO (order tracking): 2-deep circular buffer keyed by
    // wrap pointers; occupancy is f_occ above, so pointers stay in range.
    reg [PW-1:0] f_sq [0:1];
    reg [1:0]    f_wp = 0, f_rp = 0;
    always @(posedge clk) begin
        if (!rst_n) begin
            f_wp <= 0;
            f_rp <= 0;
        end else begin
            if (s_valid && s_ready) begin
                f_sq[f_wp[0]] <= s_dat;
                f_wp <= f_wp + 1'b1;
            end
            if (m_valid && m_ready)
                f_rp <= f_rp + 1'b1;
        end
    end

    always @(posedge clk) if (rst_n) begin
        assert (f_occ <= 2);                            // C2
        assert (m_valid == f_nonempty);                 // C3
        assert (s_ready == f_notfull);                  // C4
        if (m_valid && m_ready)
            assert (m_dat == f_sq[f_rp[0]]);            // V1: in-order payload
        cover (f_occ == 2);                             // full
        cover (f_occ == 0 && m_ready);                  // drained
        cover (s_valid && s_ready && m_valid && m_ready); // simultaneous rd/wr
    end
endmodule
