# quilt-verilog

The bottom-layer quilt, in silicon logic. Pure, generic Verilog — zero vendor-specific code.

## The Law
1. **Pure Verilog-2005 (IEEE 1364-2005), synthesizable subset.** No vendor primitives, no IP, no `initial` blocks in rtl/ (testbenches excepted), no SystemVerilog in rtl/.
2. **Everything is a cell.** The quilt opcodes (qm_bind / qm_link / qm_effect / qm_view / qm_tick) are the only way anything touches anything.
3. **Intelligence lives at the bottom.** Hebbian edge updates, power-law decay, cosine/vMF estimation, dial state — implemented as plain RTL modules, fixed-point, streaming.
4. **Any IO can enter a cell.** One generic ingress/egress contract; adapters are thin and dumb.
5. **Verified or it doesn't exist.** Every module ships with a testbench runnable on open tools (iverilog/verilator). No toolchain lock-in, ever.

## Layout
- `rtl/` — the winning architecture's modules
- `tb/` — testbenches
- `proposals/<crew>/` — competing architecture entries (round-robin competition)
- `docs/` — decisions, math notes, floorplans

## Competition (running)
Entries under proposals/; cross-review round after; winners get built in rtl/ with testbenches.
