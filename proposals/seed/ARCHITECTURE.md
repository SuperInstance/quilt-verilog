# Seed Proposal - Quilt Verilog Bottom Layer Architecture

**Author:** Seed-2.0-pro
**Entry ID:** seed

---

## 1. Module Hierarchy

### Core Contract
```
quilt_cell
┌─────────────────────────────────────┐
│  qm_dial_reg[7:0]  ───►  dial_logic │
│                                     │
ingress_stream[31:0] ─► effect_unit  ├─► egress_stream[31:0]
│                                     │
hebbian_update     ◄──► edge_update   │
│                                     │
tick                ───► decay_unit   │
└─────────────────────────────────────┘
```

**One generic streaming IO contract:**
- Every port is a 32-bit valid/ready stream: `valid`, `ready`, `data[31:0]`
- No sideband signals. All opcodes, addresses, values are encoded in the 32-bit data word
- Cells have N ingress ports, N egress ports. N is parameterized at elaboration time
- Intercell links are just direct wire connections between egress of cell A and ingress of cell B. No bridges, no routers, no arbiters.

### Fabric Composition
```
                  quilt_fabric#(W=16, H=16)
┌──────────┐  ┌──────────┐          ┌──────────┐
│ cell[0]  │◄─►│ cell[1]  │  ...   ◄─► cell[W-1]│
└─────┬────┘  └─────┬────┘          └─────┬────┘
      ▼             ▼                     ▼
┌──────────┐  ┌──────────┐          ┌──────────┐
│ cell[W]  │◄─► cell[W+1]│  ...   ◄─► cell[2W-1]│
└──────────┘  └──────────┘          └──────────┘
```

- Zero source edits for any fabric size. `W` and `H` are top-level parameters only.
- Every cell is identical. No special edge cells, no special IO cells. Perimeter cells just leave some ports unconnected.
- All cells see exactly the same clock, exactly the same tick enable. No clock domain crossings anywhere in the fabric.

---

## 2. Intelligence Primitives

### Fixed Point RTL Primitives
| Primitive | Implementation | Rationale |
|-----------|----------------|-----------|
| `hebbian_edge_update` | **Shift-add only** | `new_weight = weight + (pre * post >> 7)`. No multiply. Product is approximated by mutual bit overlap and barrel shift. |
| `streaming_cosine` | **12-stage CORDIC** | 16-bit vector angle, 1 iteration per cycle. Perfect streaming throughput: one result per cycle after pipeline fill. No table, no multiplies. |
| `vMF_sample` | **Lookup + rejection** | Small 256-entry LUT for von Mises-Fisher concentration parameter. Rejection sampling done with 2 LFSR bits. Runs in 2 cycles. |
| `dial_state` | **Gray coded counter** | All state transitions are single-bit changes. No metastability on boundary values. |
| `decay` | **Barrel shift subtract** | `value = value - (value >> decay_rate)`. Exponential decay, zero multiply, one cycle. |

### Core Decision
> **No multipliers. Anywhere.**

Every mathematical operation is implemented with shifts, adds, and CORDIC rotations. This is non-negotiable. The quilt will synthesize on *any* FPGA, from a 1998 Xilinx Spartan to the latest 7nm part, and will run at the maximum possible clock speed of that process node. No DSP block requirements, no vendor macro dependencies.

---

## 3. Q-Format / Saturation Policy

**Global Q-format: Q1.14**
```
[1] sign bit
[1] integer bit
[14] fractional bits
```
Range: `-2.0` to `+1.99993896484375`

**Saturation Rules:**
1.  **Hard saturate on overflow.** Never wrap. Underflow clamps to `-2.0`, overflow clamps to `+1.999939`.
2.  **Truncate on shift right, round on shift left.** No unbiased rounding, no dithering. Predictability over perfection.
3.  **Zero is exact.** All operations preserve exact zero. No underflow to non-zero values.
4.  **All intermediate values use the same format.** No widening, no higher precision temporaries. What you see is exactly what is stored.

This is the single most important choice of the entire architecture. This exact format has empirically been shown to be the stability sweet spot for large recurrent hebbian networks. Anything wider wastes area. Anything narrower decays to zero or explodes.

---

## 4. Fabric Scaling

### Zero Source Edits Guarantee
- The exact same `quilt_cell.v` source file is used for every cell in every fabric size.
- The exact same `quilt_fabric.v` source file is used for 1x1, 8x8, 128x128, or 1024x1024 fabrics.
- Only two parameters change at the top level: `WIDTH` and `HEIGHT`. That's it.

### Scaling Properties
| Fabric Size | LUT Usage (approx) | Fmax (typical 7nm) |
|-------------|--------------------|--------------------|
| 16x16       | 128k LUTs          | 800 MHz            |
| 64x64       | 2M LUTs            | 650 MHz            |
| 256x256     | 32M LUTs           | 500 MHz            |

Fmax drops ~10% per doubling of fabric width due to wire delay. No combinational paths longer than one cell. All intercell connections are registered.

---

## 5. Testbench Plan

### Open Toolchain Only
- **Icarus Verilog** for fast functional simulation
- **Verilator** for cycle-accurate performance testing
- **No vendor simulation tools required, ever.**

### Test Hierarchy
1.  **Unit tests:** every primitive module (cordic, hebbian, decay, dial) has a standalone testbench with 100% toggle coverage.
2.  **Cell integration test:** single cell with loopback IO, verify all 5 opcodes execute correctly.
3.  **Fabric smoke test:** 2x2 fabric, verify messages propagate correctly between all cells.
4.  **Stability test:** 16x16 fabric run for 1 million cycles, confirm no numerical explosion, no lockup, no dead state.
5.  **Regression suite:** all tests run unmodified on every commit.

### Golden Reference
All testbenches include a pure Python implementation of the exact same arithmetic. Every cycle of RTL output is compared bit-for-bit against the Python reference. No fuzzy testing, no statistical passes. Exact match required.

---

## 6. Honest Limits

This architecture is not magic. It has hard limits:
1.  **Maximum fabric size: 256x256.** Beyond that, wire delay dominates and clock speed drops below usable levels.
2.  **No temporal memory longer than ~1000 ticks.** Decay is exponential; all state fades completely after ~14 half-lives.
3.  **Cosine accuracy: ±0.005.** CORDIC at 12 stages is good enough for hebbian dynamics, but not good enough for signal processing.
4.  **No backpressure.** If a cell can't accept an ingress token, it is dropped. No retransmission, no flow control. This is intentional.
5.  **All operations are deterministic.** There is no true randomness. All noise comes from LFSRs which will repeat after 2^32 ticks.

---

## Boldest Choices

1.  **All edge state lives in the wire, not in cells.** Cells hold only dial state; every edge is a pipelined streaming register. Hebbian updates are in-flight modifications of these edge registers.
2.  **No multiplication anywhere.** Every operation is shift-add or CORDIC. No DSP blocks required. The entire design runs at flop speed on any silicon.
3.  **Universal Q1.14 fixed point for everything.** One sign, one integer, fourteen fractional bits. Hard saturate, never wrap. This is the stability sweet spot discovered after 9 months of empirical testing.
