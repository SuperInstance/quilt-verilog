// PROVENANCE: proposals/seed/RTL-SKETCH.md (round-1 competition entry: seed)
module quilt_fabric #(
    parameter WIDTH = 16,
    parameter HEIGHT = 16
) (
    input clk,
    input rst_n,
    input tick
);

genvar x, y;
generate
    for (y=0; y < HEIGHT; y=y+1) begin : row
        for (x=0; x < WIDTH; x=x+1) begin : col
            quilt_cell #(.NEIGHBORS(4)) cell (
                .clk(clk),
                .rst_n(rst_n),
                .tick(tick),

                .ingress_valid({
                    y > 0 ? row[y-1].col[x].egress_valid : 1'b0,
                    x > 0 ? row[y].col[x-1].egress_valid : 1'b0,
                    y < HEIGHT-1 ? row[y+1].col[x].egress_valid : 1'b0,
                    x < WIDTH-1 ? row[y].col[x+1].egress_valid : 1'b0
                }),
                .ingress_ready(),
                .ingress_data({
                    y > 0 ? row[y-1].col[x].egress_data : 32'b0,
                    x > 0 ? row[y].col[x-1].egress_data : 32'b0,
                    y < HEIGHT-1 ? row[y+1].col[x].egress_data : 32'b0,
                    x < WIDTH-1 ? row[y].col[x+1].egress_data : 32'b0
                }),

                .egress_valid(),
                .egress_ready({4{1'b1}}),
                .egress_data(),

                .edge_out(),
                .edge_in()
            );
        end
    end
endgenerate

endmodule
