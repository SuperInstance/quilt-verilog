// PROVENANCE: proposals/glm/RTL-SKETCH.md (round-1 competition entry: glm)
module qs_mathtail #(
    parameter W = 48
)(
    input  wire           clk,
    input  wire           rst_n,
    input  wire           start,
    input  wire [1:0]     op,        // 2'b00: div a/b (unsigned), 2'b01: isqrt(a)
    input  wire [W-1:0]   a,
    input  wire [W-1:0]   b,
    output wire           busy,
    output reg            done,
    output reg  [W-1:0]   q,
    output reg            err_sticky
);
    localparam N2 = W / 2;

    reg [1:0]     st;      // 0 idle, 1 div, 2 sqrt
    reg [6:0]     cnt;
    reg [W-1:0]   dvd, dvr, rd;
    reg [W:0]     drem;
    reg [W/2-1:0] root;
    reg [W-1:0]   rrem;

    assign busy = (st != 2'd0);

    // --- division step: restoring, MSB first ---
    wire        abit = dvd[W-1-cnt];
    wire [W:0]  dtop = {drem[W-1:0], abit};
    wire [W:0]  dsub = {1'b0, dvr};
    wire        dge  = (dtop >= dsub);

    // --- sqrt step: root <<= 1; trial = 4*root+1 vs (rrem<<2)|pair ---
    wire [W-1:0]   rdsh   = rd >> {cnt, 1'b0};         // rd >> (2*cnt)
    wire [1:0]     pairp  = rdsh[1:0];
    wire [W-1:0]   rrem_n = {rrem[W-3:0], pairp};
    wire [W/2+1:0] trial  = {root, 2'b01};             // 4*root + 1
    wire [W-1:0]   trial_e= {{(W-N2-2){1'b0}}, trial};
    wire           rge    = (rrem_n >= trial_e);
    wire [W/2-1:0] root_n = rge ? {root[W/2-2:0], 1'b1} : {root[W/2-2:0], 1'b0};

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= 2'd0; cnt <= 7'd0; done <= 1'b0; q <= {W{1'b0}};
            err_sticky <= 1'b0; dvd <= {W{1'b0}}; dvr <= {W{1'b0}};
            rd <= {W{1'b0}}; drem <= {(W+1){1'b0}}; root <= {(W/2){1'b0}};
            rrem <= {W{1'b0}};
        end else begin
            done <= 1'b0;
            case (st)
                2'd0: if (start) begin
                    if (op == 2'd00) begin
                        if (b == {W{1'b0}}) begin
                            err_sticky <= 1'b1;  q <= {W{1'b1}};  done <= 1'b1;
                        end else begin
                            st <= 2'd1; cnt <= 7'd0;
                            dvd <= a; dvr <= b; drem <= {(W+1){1'b0}};
                        end
                    end else if (op == 2'd01) begin
                        st <= 2'd2; cnt <= 7'd0;
                        rd <= a; root <= {(W/2){1'b0}}; rrem <= {W{1'b0}};
                    end
                end
                2'd1: begin                                      // divide
                    if (dge) begin
                        drem  <= dtop - dsub;
                        q[cnt] <= 1'b1;
                    end else begin
                        drem  <= dtop;
                        q[cnt] <= 1'b0;
                    end
                    if (cnt == W-1) begin  st <= 2'd0; done <= 1'b1; end
                    else                  cnt <= cnt + 7'd1;
                end
                2'd2: begin                                      // isqrt
                    rrem <= rge ? (rrem_n - trial_e) : rrem_n;
                    root <= root_n;
                    if (cnt == N2-1) begin
                        q    <= {{(W-N2){1'b0}}, root_n};         // floor sqrt
                        st   <= 2'd0;  done <= 1'b1;
                    end else begin
                        cnt <= cnt + 7'd1;
                    end
                end
                default: st <= 2'd0;
            endcase
        end
    end
endmodule
