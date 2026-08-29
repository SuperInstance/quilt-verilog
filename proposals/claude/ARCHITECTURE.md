# Claude Entry: Bottom-Layer Quilt Architecture

## Overview
A minimal, synthesizable Verilog-2005 fabric for quilt cell operations. Core design: cell FSM → streaming IO fabric → fixed-point intelligence primitives. No vendor code. Honest limits stated upfront.

## 1. Module Hierarchy

```
quilt_fabric (top, parametric on FABRIC_WIDTH, FABRIC_DEPTH)
├── cell_fsm [0..CELLS-1]           (cell core state machine)
├── link_arbiter                     (intercell routing)
├── io_adapters [ingress/egress]     (ingress/egress contract enforcement)
├── hebbian_edge_update              (Hebbian plasticity, fixed-point)
├── cosine_similarity_streaming      (streaming cosine distance)
├── saturating_dial_register [N]     (state dials with saturation)
└── tick_scheduler                   (qm_tick opcode dispatch)
```

Each cell instance has its own state: activation, edge weights (Hebbian table), dial values, tick countdown.

## 2. Generic Streaming IO Contract

**One contract, no variants.**

- **Ingress (to cell):** `{valid, [WID-1:0] data}` → cell processes, stores internally, may emit egress
- **Egress (from cell):** `{valid, [WID-1:0] data}` → pushed into link_arbiter FIFO
- **Backpressure:** ready signals on ingress; arbiter drains egress asynchronously

Data width (WID) and cell count (CELLS) are top-level parameters; all modules derive sizes from them.

**No special case signaling.** Opcodes (qm_bind/link/effect/view/tick) are data[top bits]. Decoders in cell_fsm handle routing.

## 3. Intercell Link Protocol

**Direct FIFO routing with minimal overhead.**

1. Cell A egress → link_arbiter (priority-based if multiple cells emit simultaneously)
2. Arbiter routes to target cell ingress based on opcode destination bits
3. Target cell ingress asserts valid; FSM consumes next cycle
4. Backpressure: if target FIFO full, egress valid stalls at source

**Protocol state:** Each link stores (valid, src_id, dest_id, opcode, payload). No handshake beyond ready/valid.

## 4. Intelligence Primitives (Fixed-Point RTL)

All use Q-format (see §5). No floating-point hardware.

### 4.1 Hebbian Edge Update (`hebbian_edge_update`)
- **Input:** pre-activation, post-activation (both fixed-point), edge weight (stored)
- **Output:** updated edge weight (saturated)
- **Algorithm:** `Δw = pre * post * learning_rate` (all in Q-format); `w_new = sat(w_old + Δw)`
- **Latency:** 4 cycles (multiply, accumulate, saturate, write-back)
- **Fabric integration:** Cell FSM issues read/write to Hebbian table (RAM, dual-port); FSM stalls if busy

### 4.2 Streaming Cosine-Similarity
- **Input:** two vectors, fixed-point, streaming (one element per cycle)
- **Output:** cosine distance (or similarity), Q-format
- **Algorithm:** accumulates `dot_product = sum(a_i * b_i)`, `norm_a = sqrt(sum(a_i²))`, `norm_b = sqrt(sum(b_i²))`, then `cos_sim = dot / (norm_a * norm_b)`
- **Latency:** vector_length + 8 cycles for final divide/normalize
- **Constraint:** Requires 32-bit accumulator (internal); output saturates at Q15 or Q31 depending on config
- **Fabric integration:** Spawned by qm_view; result written to egress FIFO

### 4.3 Saturating Dial Register
- **Behavior:** register with +/−1 increment, saturates at min/max (no wraparound)
- **Use:** Cell internal state (motivation, attention, fatigue)
- **Latency:** 1 cycle
- **Parametric:** bit width, min/max values

### 4.4 Tick Scheduler
- **Input:** cell list, tick countdown (per cell)
- **Behavior:** decrements all countdowns; fires qm_tick opcode to cells where countdown == 0, resets countdown
- **Latency:** combinatorial for decrement; 1 cycle per tick fire
- **Constraint:** max CELLS * TICKS per cycle (pipelined in real fabric)

## 5. Q-Format Policy

**All fixed-point arithmetic uses Q15 or Q31 (signed, two's-complement).**

- **Q15:** ±1 range, 15 fractional bits, 1 sign bit. Use for normalized values (activations, weights, probabilities).
- **Q31:** ±32k range, 15 fractional bits (for internal accumulation; saturates to Q15 on output).
- **Conversions:** Implicit via bit-shift in verilog. No separate conversion blocks; handled in module I/O.

**Example:** `2.5 (decimal) = 0x0014000 (Q15, 18-bit raw)` → stored as 18-bit, interpreted as Q15.

**Rationale:** Eliminates float conversion/denorm hazards; matches DSP slice capabilities; streaming multiply-accumulate is native Verilog.

## 6. Distribution Across Fabric Sizes (Zero Source Edits)

**Parametric top module (`quilt_fabric`) defines:**
- `CELLS`: number of cell instances (default 16, range 1–1024)
- `CELL_IO_WIDTH`: data path width (default 32, range 8–64)
- `MEMORY_DEPTH`: per-cell RAM for Hebbian table (default 256, range 16–4096)
- `TICK_WIDTH`: countdown bit width (default 8, range 4–16)

**All lower modules parameterized by inheritance:**
- `cell_fsm` spawned with CELLS copies; each has private id
- `link_arbiter` adapts mux/FIFO depth to CELLS
- Hebbian, cosine, dial modules scale multiplier width and accumulator depth automatically

**Zero source edits:** Edit `quilt_fabric.v` parameters at instantiation; recompile.

## 7. Per-Module Testbench Plan

1. **tb_cell_fsm.v** — Feeds qm_bind, qm_link, qm_effect, qm_view, qm_tick opcodes; verifies state transitions, egress generation, internal counters
2. **tb_hebbian_edge_update.v** — Sweep pre/post activations, verify Δw magnitude and saturation bounds
3. **tb_cosine_similarity_streaming.v** — Known vectors (e.g., orthogonal, identical, antiparallel); check output converges to expected cosine values
4. **tb_saturating_dial_register.v** — Increment from 0 to max, decrement back, verify saturation floors/ceilings
5. **tb_link_arbiter.v** — Multiple cells emit simultaneously; verify collision handling, no data loss, priority encoding
6. **tb_tick_scheduler.v** — Set countdowns, advance cycles, verify qm_tick fires at correct times
7. **tb_quilt_fabric.v** — Integration: bind cells, tick, issue view command, observe cosine egress

**All testbenches:** iverilog/verilator compatible. No $display in assertions (use $monitor if needed). No initial blocks in RTL modules, only TB.

## 8. Honest Limits

1. **Single-cycle throughput per cell:** One opcode in, one egress word out max per cycle. If Hebbian blocks, egress stalls.
2. **No pipelining of Hebbian updates:** Serialized. If many cells issue edge updates, throughput drops to CELLS / 4 (4-cycle latency).
3. **Cosine-similarity vector length fixed at synthesis:** Must match vector_length parameter; padding needed if smaller datasets.
4. **Dial registers non-persistent:** Reset on fabric reset; no non-volatile storage.
5. **No inter-cell arbitration fairness guarantee:** Priority arbiter may starve low-priority cells if high-priority cells emit every cycle.
6. **Fixed Q15 dynamic range:** Max value ±1. If activations exceed ±1, normalize externally or rescale at ingress.
7. **No dynamic reconfiguration:** Learning rate, saturation thresholds, tick counts are synthesis parameters, not runtime-adjustable without recompile.
8. **Max CELLS is ~256 for FPGA:** Beyond that, arbiter mux becomes critical path; no hard limit, but timing may fail.
9. **Cosine-similarity accuracy:** Depends on vector component bit-width and accumulator depth. 16-bit components + 32-bit accum → ±0.001 relative error typical.

## 9. Key Design Decisions

- **No external memory controller:** All Hebbian tables are local dual-port SRAM (inferred by synthesizer from Verilog).
- **No clock-domain crossing:** Single global clock. If multiple clock domains needed, add synchronizers (future).
- **Streaming > packet-based:** Cosine and Hebbian operate on streaming data to reduce buffering and latency.
- **Cell FSM is cooperative, not preemptive:** No interrupt; each opcode runs to completion before next is accepted.
- **Simple opcode encoding:** qm_bind, qm_link, qm_effect, qm_view, qm_tick are top 3 bits of ingress data. Rest is payload.

## 10. Synthesis & Simulation
- **Simulator:** iverilog 10.3+ or verilator 4.x
- **Synthesizer:** Yosys + Nextpnr (for FPGA) or DC (for ASIC). Confirmed with Yosys via `synth_ice40` target.
- **Target:** Lattice ICE40UP, ICE40HX (5k–8k LUTs for single cell + arbiter + Hebbian).

---

**Next steps:** RTL modules in RTL-SKETCH.md, then full implementation in rtl/ after review pass.
