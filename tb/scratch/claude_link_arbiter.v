// PROVENANCE: proposals/claude/RTL-SKETCH.md (round-1 competition entry: claude)
module link_arbiter #(
  parameter CELLS = 16,
  parameter IO_WIDTH = 32,
  parameter FIFO_DEPTH = 8
) (
  input clk, rst_n,
  
  // Ingress from each cell (egress)
  input  [CELLS-1:0] cell_egress_valid,
  output [CELLS-1:0] cell_egress_ready,
  input  [IO_WIDTH-1:0] cell_egress_data [0:CELLS-1],
  
  // Egress to routing fabric
  output [IO_WIDTH-1:0] fabric_egress_data,
  output                fabric_egress_valid,
  input                 fabric_egress_ready
);

  // Priority encoder: select highest-priority cell with valid data
  wire [CELLS-1:0] priority;
  reg [CELLS-1:0] selected;
  wire [IO_WIDTH-1:0] mux_data;

  // Priority encoding (cell 0 has highest priority)
  always @(*) begin
    selected = {CELLS{1'b0}};
    if (cell_egress_valid[0]) selected = (1 << 0);
    else if (cell_egress_valid[1]) selected = (1 << 1);
    else if (cell_egress_valid[2]) selected = (1 << 2);
    else if (cell_egress_valid[3]) selected = (1 << 3);
    else if (cell_egress_valid[4]) selected = (1 << 4);
    else if (cell_egress_valid[5]) selected = (1 << 5);
    else if (cell_egress_valid[6]) selected = (1 << 6);
    else if (cell_egress_valid[7]) selected = (1 << 7);
    else if (CELLS > 8 && cell_egress_valid[8]) selected = (1 << 8);
    else if (CELLS > 9 && cell_egress_valid[9]) selected = (1 << 9);
    else if (CELLS > 10 && cell_egress_valid[10]) selected = (1 << 10);
    else if (CELLS > 11 && cell_egress_valid[11]) selected = (1 << 11);
    else if (CELLS > 12 && cell_egress_valid[12]) selected = (1 << 12);
    else if (CELLS > 13 && cell_egress_valid[13]) selected = (1 << 13);
    else if (CELLS > 14 && cell_egress_valid[14]) selected = (1 << 14);
    else if (CELLS > 15 && cell_egress_valid[15]) selected = (1 << 15);
  end

  // Data multiplexer (combinatorial)
  wire [IO_WIDTH-1:0] cell_data [0:CELLS-1];
  generate
    genvar i;
    for (i = 0; i < CELLS; i = i + 1) begin : MUX_ASSIGN
      assign cell_data[i] = cell_egress_data[i];
    end
  endgenerate

  // Simple mux (in real design, would use tree or dynamic logic)
  wire [IO_WIDTH-1:0] selected_data;
  assign selected_data = (selected[0]) ? cell_data[0] :
                         (selected[1]) ? cell_data[1] :
                         (selected[2]) ? cell_data[2] :
                         (selected[3]) ? cell_data[3] :
                         (selected[4]) ? cell_data[4] :
                         (selected[5]) ? cell_data[5] :
                         (selected[6]) ? cell_data[6] :
                         (selected[7]) ? cell_data[7] :
                         (CELLS > 8 && selected[8]) ? cell_data[8] :
                         (CELLS > 9 && selected[9]) ? cell_data[9] :
                         (CELLS > 10 && selected[10]) ? cell_data[10] :
                         (CELLS > 11 && selected[11]) ? cell_data[11] :
                         (CELLS > 12 && selected[12]) ? cell_data[12] :
                         (CELLS > 13 && selected[13]) ? cell_data[13] :
                         (CELLS > 14 && selected[14]) ? cell_data[14] :
                         (CELLS > 15 && selected[15]) ? cell_data[15] :
                         {IO_WIDTH{1'b0}};

  // Ready backpressure
  wire any_valid = |cell_egress_valid;
  
  generate
    genvar j;
    for (j = 0; j < CELLS; j = j + 1) begin : READY_ASSIGN
      assign cell_egress_ready[j] = (selected[j] && fabric_egress_ready) ? 1'b1 : 1'b0;
    end
  endgenerate

  // Egress to fabric
  assign fabric_egress_valid = any_valid;
  assign fabric_egress_data = selected_data;

endmodule
