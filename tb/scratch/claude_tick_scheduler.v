// PROVENANCE: proposals/claude/RTL-SKETCH.md (round-1 competition entry: claude)
module tick_scheduler #(
  parameter CELLS = 16,
  parameter TICK_WIDTH = 8,
  parameter IO_WIDTH = 32
) (
  input clk, rst_n,
  
  // Per-cell tick countdown values (written by cells)
  input [CELLS*TICK_WIDTH-1:0] tick_countdown,
  
  // Tick output
  output [IO_WIDTH-1:0] tick_data,
  output tick_valid,
  input tick_ready,
  
  // Which cell to tick (combinatorial)
  output [$clog2(CELLS)-1:0] tick_cell_id
);

  // Wire-AND reduction: find first cell with countdown == 0
  wire [CELLS-1:0] tick_fire;
  generate
    genvar i;
    for (i = 0; i < CELLS; i = i + 1) begin : TICK_CHECK
      assign tick_fire[i] = (tick_countdown[i*TICK_WIDTH +: TICK_WIDTH] == {TICK_WIDTH{1'b0}});
    end
  endgenerate

  // Priority encode: return first cell with tick_fire[i] == 1
  reg [$clog2(CELLS)-1:0] fire_cell;
  always @(*) begin
    fire_cell = {$clog2(CELLS){1'b0}};
    for (int j = 0; j < CELLS; j = j + 1) begin
      if (tick_fire[j]) begin
        fire_cell = j;
        disable;
      end
    end
  end

  assign tick_cell_id = fire_cell;
  assign tick_valid = (|tick_fire);
  assign tick_data = {3'b100, fire_cell[4:0], {(IO_WIDTH-8){1'b0}}};

endmodule
