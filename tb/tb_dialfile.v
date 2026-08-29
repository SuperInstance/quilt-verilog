// tb_dialfile.v -- defaults, write/read-back, strobe timing.
`timescale 1ns/1ps
module tb_dialfile;
    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg         wr = 0, rd = 0;
    reg  [3:0]  addr = 0;
    reg  [15:0] wdata = 0;
    wire [15:0] rdata;
    wire        rstb;

    wire [15:0] eta_f, eta_s, refr, cosmin, hl;
    wire [3:0]  kf, ks, ka;
    wire signed [15:0] thresh;
    wire [4:0]  p0e;
    wire        mode;

    integer errors = 0;

    q_dialfile u_dut (
        .clk(clk), .rst_n(rst_n),
        .i_wr(wr), .i_addr(addr), .i_wdata(wdata),
        .i_rd(rd), .o_rdata(rdata), .o_rstb(rstb),
        .o_eta_f(eta_f), .o_eta_s(eta_s),
        .o_kf(kf), .o_ks(ks), .o_ka(ka),
        .o_thresh(thresh), .o_refr(refr), .o_cosmin(cosmin),
        .o_p0e(p0e), .o_mode(mode), .o_hl(hl)
    );

    task check(input [15:0] got, input [15:0] exp, input [127:0] name);
        begin
            if (got !== exp) begin
                errors = errors + 1;
                $display("FAIL %0s: got %h exp %h", name, got, exp);
            end
        end
    endtask

    task rd_dial(input [3:0] a);
        begin
            @(negedge clk);
            rd = 1; addr = a;
            @(negedge clk);
            rd = 0;
            // rdata/rstb registered on the edge where rd was high
        end
    endtask

    integer i;
    reg [15:0] pat;

    initial begin
        repeat (4) @(negedge clk);
        rst_n = 1;
        repeat (2) @(negedge clk);

        // reset defaults (fan-outs)
        check(eta_f, 16'h0800, "eta_f_def");
        check(eta_s, 16'h0080, "eta_s_def");
        check({4'd0,kf}, 16'd6, "kf_def");
        check({4'd0,ks}, 16'd12, "ks_def");
        check({4'd0,ka}, 16'd5, "ka_def");
        check(thresh, 16'h6000, "thresh_def");
        check(refr, 16'd4, "refr_def");
        check(cosmin, 16'h2CCD, "cosmin_def");
        check({27'd0, p0e}, 32'd20, "p0e_def");
        check(mode, 1'b0, "mode_def");
        check(hl, 16'd64, "hl_def");

        // defaults via the read port
        rd_dial(4'd0); check(rdata, 16'h0800, "rd_eta_f");
        rd_dial(4'd5); check(rdata, 16'h6000, "rd_thresh");
        rd_dial(4'd8); check(rdata, 16'd20,  "rd_p0e");
        rd_dial(4'd9); check(rdata, 16'd0,   "rd_mode");
        rd_dial(4'd10); check(rdata, 16'd64, "rd_hl");

        // write/read-back every mapped dial
        for (i = 0; i <= 10; i = i + 1) begin
            pat = 16'hA000 | i[15:0];
            @(negedge clk);
            wr = 1; addr = i[3:0]; wdata = pat;
            @(negedge clk);
            wr = 0;
            rd_dial(i[3:0]);
            check(rdata, pat, "wr_rd");
        end

        // fan-outs follow writes
        rd_dial(4'd9);  // leave mode=0xA009 -> bit0=1
        @(negedge clk);
        if (mode !== 1'b1) begin
            errors = errors + 1;
            $display("FAIL mode_follow");
        end

        if (errors == 0) $display("TB_DIALFILE PASS");
        else $display("TB_DIALFILE FAIL %0d", errors);
        $finish;
    end
endmodule
