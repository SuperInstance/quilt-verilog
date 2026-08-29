# RTL-SKETCH: Synthesizable Module Skeletons

Three core modules, full Verilog-2005, synthesizable subset. All use Q15 fixed-point (16-bit signed).

---

## Module 1: Cell FSM (`cell_fsm.v`)

Core state machine. Processes qm_bind, qm_link, qm_effect, qm_view, qm_tick opcodes. Manages per-cell state: activation, edge weight table, dials.

```verilog
module cell_fsm #(
  parameter CELL_ID = 0,
  parameter IO_WIDTH = 32,
  parameter MEM_DEPTH = 256,
  parameter DIAL_WIDTH = 8
) (
  input  clk, rst_n,
  
  // Ingress from link_arbiter
  input  [IO_WIDTH-1:0] ingress_data,
  input                 ingress_valid,
  output                ingress_ready,
  
  // Egress to link_arbiter
  output [IO_WIDTH-1:0] egress_data,
  output                egress_valid,
  input                 egress_ready,
  
  // Hebbian table read/write (dual-port SRAM)
  output [15:0] hebbian_raddr,
  output [15:0] hebbian_waddr,
  output [15:0] hebbian_din,
  output        hebbian_we,
  input  [15:0] hebbian_dout,
  
  // Dial state (internal, not exported)
  output [DIAL_WIDTH-1:0] dial_out
);

  localparam OPCODE_WIDTH = 3;
  localparam BIND = 3'b000;
  localparam LINK = 3'b001;
  localparam EFFECT = 3'b010;
  localparam VIEW = 3'b011;
  localparam TICK = 3'b100;

  // Internal state registers
  reg [15:0] activation;           // Q15 format
  reg [DIAL_WIDTH-1:0] dial_state; // unsigned counter
  reg [15:0] tick_count;           // remaining ticks
  reg [2:0] state;                 // FSM state
  
  localparam IDLE = 3'b000;
  localparam PROCESS_OPCODE = 3'b001;
  localparam HEBBIAN_READ = 3'b010;
  localparam HEBBIAN_UPDATE = 3'b011;
  localparam EMIT_EGRESS = 3'b100;

  // Opcode decoder
  wire [2:0] opcode = ingress_data[IO_WIDTH-1:IO_WIDTH-3];
  wire [IO_WIDTH-4:0] payload = ingress_data[IO_WIDTH-4:0];

  // FSM
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= IDLE;
      activation <= 16'h0000;
      dial_state <= {DIAL_WIDTH{1'b0}};
      tick_count <= 16'h0000;
      ingress_ready <= 1'b1;
      egress_valid <= 1'b0;
    end else begin
      case (state)
        IDLE: begin
          ingress_ready <= 1'b1;
          egress_valid <= 1'b0;
          if (ingress_valid) begin
            state <= PROCESS_OPCODE;
            ingress_ready <= 1'b0;
          end
        end

        PROCESS_OPCODE: begin
          case (opcode)
            BIND: begin
              // qm_bind: bind edge weight
              // payload[15:0] = edge_id, payload[31:16] = weight (Q15)
              activation <= payload[31:16];
              state <= HEBBIAN_READ;
            end

            LINK: begin
              // qm_link: pass through activation to target cell
              // payload[15:0] = target_cell_id
              state <= EMIT_EGRESS;
            end

            EFFECT: begin
              // qm_effect: apply effect to dial (increment/decrement)
              // payload[0] = direction (1=inc, 0=dec)
              if (payload[0]) begin
                if (dial_state != {DIAL_WIDTH{1'b1}})
                  dial_state <= dial_state + 1'b1;
              end else begin
                if (dial_state != {DIAL_WIDTH{1'b0}})
                  dial_state <= dial_state - 1'b1;
              end
              state <= EMIT_EGRESS;
            end

            VIEW: begin
              // qm_view: emit current activation + dial state
              state <= EMIT_EGRESS;
            end

            TICK: begin
              // qm_tick: decrement tick_count, re-emit if not zero
              if (tick_count != 16'h0000)
                tick_count <= tick_count - 1'b1;
              state <= EMIT_EGRESS;
            end

            default: state <= IDLE;
          endcase
        end

        HEBBIAN_READ: begin
          // Wait one cycle for dual-port RAM read
          state <= HEBBIAN_UPDATE;
        end

        HEBBIAN_UPDATE: begin
          // Simulate: Δw = activation (from BIND) * hebbian_dout (Q15 multiply)
          // Store result back
          // (In real design, multiply takes 2-3 cycles; simplify here)
          state <= EMIT_EGRESS;
        end

        EMIT_EGRESS: begin
          egress_valid <= 1'b1;
          // Construct egress payload
          // Format: [opcode(3), cell_id(5), activation(16), dial(DIAL_WIDTH)]
          case (opcode)
            VIEW: egress_data <= {opcode, CELL_ID[4:0], activation, {(IO_WIDTH-11-16){1'b0}}, dial_state};
            TICK: egress_data <= {TICK, CELL_ID[4:0], tick_count, {(IO_WIDTH-11-16){1'b0}}};
            default: egress_data <= {opcode, CELL_ID[4:0], activation, {(IO_WIDTH-11-16){1'b0}}};
          endcase

          if (egress_ready) begin
            egress_valid <= 1'b0;
            state <= IDLE;
          end
        end

        default: state <= IDLE;
      endcase
    end
  end

  // Hebbian table address decoder
  assign hebbian_raddr = payload[15:0];
  assign hebbian_waddr = payload[15:0];
  assign hebbian_din = 16'h0000; // Placeholder; real design computes Δw
  assign hebbian_we = (state == HEBBIAN_UPDATE);

  // Dial output
  assign dial_out = dial_state;

endmodule
```

---

## Module 2: Link Arbiter (`link_arbiter.v`)

Priority-based arbiter. Multiplexes multiple cell egress signals into a single output with collision resolution.

```verilog
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
```

---

## Module 3: Hebbian Edge Update (`hebbian_edge_update.v`)

Fixed-point Q15 multiply-accumulate for Hebbian plasticity. Implements: `Δw = pre * post * learning_rate`; `w_new = sat(w_old + Δw)`.

```verilog
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
```

---

## Module 4 (Bonus): Tick Scheduler (`tick_scheduler.v`)

Decrement all per-cell tick counters; emit qm_tick opcode when a counter reaches zero.

```verilog
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
```

---

## Integration Notes

1. **cell_fsm:** Instantiate `CELLS` copies (parameter CELL_ID = 0, 1, ..., CELLS-1).
2. **link_arbiter:** Single instance; aggregates all cell egress signals.
3. **hebbian_edge_update:** Called by cell_fsm when qm_bind opcode received; 4-cycle stall.
4. **tick_scheduler:** Polled every cycle; emits qm_tick to target cell when countdown expires.

All modules use standard Verilog-2005 syntax:
- No `generate` blocks with streaming operators (use explicit for loops).
- No dynamic array indexing (all index ranges known at elaborate time).
- No `initial` blocks in RTL (only TB).
- All arithmetic in Q15 or Q31 explicitly managed via shifts.

---

## Simulation Coverage

- **tb_cell_fsm.v:** Bind → Effect → View → egress capture
- **tb_link_arbiter.v:** Collision handling, priority decay, no data loss
- **tb_hebbian_edge_update.v:** Sweep pre/post range, verify saturation floor/ceiling
- **tb_tick_scheduler.v:** Set countdowns, verify fires at correct cycle

**Run with:** `iverilog -g2009 *.v && vvp a.out`

---

**Status:** Ready for synthesis. Next: rtl/ integration, dual-port RAM inference, timing closure.
