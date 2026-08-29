// PROVENANCE: proposals/claude/RTL-SKETCH.md (round-1 competition entry: claude)
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
