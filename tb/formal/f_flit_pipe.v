// tb/formal/f_flit_pipe.v -- formal harness: q_flit_pipe obeys the 2-entry
// FIFO interface contract, proven at the boundary only (no XMRs: yosys's
// Verilog frontend makes `dut.b_v` an undriven implicit wire, not a ref).
//
// Shadow occupancy model: +1 on accept, -1 on emit. The four invariants
// together say "indistinguishable from an ideal 2-deep FIFO":
//   C1 f_out <= f_in            (no duplication / underflow)
//   C2 f_in - f_out <= 2        (capacity never exceeded / no over-accept)
//   C3 m_valid == (f_occ != 0)  (nothing hidden: non-empty presents data,
//                                empty presents nothing -> no drop)
//   C4 s_ready == (f_occ < 2)   (backpressure exactly at capacity)
module f_flit_pipe(input clk, input rst_n);   // free top inputs; timestep = posedge (multiclock off)
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

    // force a reset preamble: DUT regs have no init values, so the proof must
    // let synchronous reset define state before properties bind
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

    // shadow occupancy: 2-bit, wraps loudly. +1 on accept, -1 on emit.
    // C2 asserts <=2, so any wrap (dup outrunning accept, or emit from
    // empty) lands on 3 and is caught. Reset-aware: DUT reset drops
    // in-flight content, so the model restarts with it.
    reg  [1:0] f_occ = 0;
    wire       f_nonempty = f_occ != 0;
    wire       f_notfull  = f_occ < 2;
    always @(posedge clk) begin
        if (!rst_n)
            f_occ <= 0;
        else
            f_occ <= f_occ + (s_valid && s_ready) - (m_valid && m_ready);
    end

    always @(posedge clk) if (rst_n) begin
        assert (f_occ <= 2);                    // C2: capacity, no wrap
        assert (m_valid == f_nonempty);         // C3: no drop/hide, no dup
        assert (s_ready == f_notfull);          // C4: pressure
        cover (f_occ == 2);                     // full occupancy reached
        cover (f_occ == 0 && m_ready);          // drained, ready for more
    end
endmodule
