// PROVENANCE: proposals/claude/RTL-SKETCH.md (round-1 competition entry: claude)
module hebbian_edge_update #(
  parameter LR_WIDTH = 8  // learning_rate in Q8 format (range 0–1)
) (
  input clk, rst_n,
  
  // Pre/post activations (Q15)
  input [15:0] pre_activation,   // signed Q15
  input [15:0] post_activation,  // signed Q15
  input [15:0] learning_rate,    // unsigned Q15 (0.0 to 1.0)
  
  // Current edge weight (Q15)
  input [15:0] weight_in,        // signed Q15
  
  // Updated weight (Q15)
  output [15:0] weight_out,      // signed Q15, saturated
  
  // Valid/ready handshake
  input start,
  output done
);

  // Pipeline stages
  reg [15:0] pre_r1, post_r1, lr_r1, w_r1;
  reg [31:0] product1;    // stage 1: pre * post (Q30)
  reg [31:0] product2;    // stage 2: product1 * lr (Q30)
  reg [31:0] sum;         // stage 3: w_old + product2 (Q30)
  reg [15:0] saturated;   // stage 4: saturate to Q15

  // Stage counters for 4-cycle latency
  reg [1:0] pipe_count;
  reg busy;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      pipe_count <= 2'b00;
      busy <= 1'b0;
      saturated <= 16'h0000;
      product1 <= 32'h0;
      product2 <= 32'h0;
      sum <= 32'h0;
    end else begin
      if (start && !busy) begin
        // Stage 1: capture inputs, multiply pre * post
        pre_r1 <= pre_activation;
        post_r1 <= post_activation;
        lr_r1 <= learning_rate;
        w_r1 <= weight_in;
        product1 <= pre_activation * post_activation;
        pipe_count <= 2'b01;
        busy <= 1'b1;
      end else if (busy) begin
        // Stage 2: multiply product1 * lr
        product2 <= (product1 >>> 15) * lr_r1;  // Shift by Q15 to keep precision
        
        // Stage 3: add to weight
        sum <= w_r1 + (product2 >>> 15);
        
        // Stage 4: saturate
        if (sum[31] == sum[30]) begin
          // No overflow
          saturated <= sum[30:15];
        end else begin
          // Saturate to max/min Q15
          saturated <= (sum[31]) ? 16'h8000 : 16'h7FFF;
        end

        pipe_count <= pipe_count + 1'b1;
        if (pipe_count == 2'b11) begin
          busy <= 1'b0;
        end
      end
    end
  end

  assign done = !busy;
  assign weight_out = saturated;

endmodule
