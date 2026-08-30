# SILICON-EXPERIMENTS — first numbers, two failures booked (referee bench)

*2026-08-30. The lane that ran these died before its write-up and its claimed
commit (c0a13ea) never landed — phantom, per the known failure mode. The
referee bench-verified the artifacts and committed them honestly. Numbers are
real; the write-up is the referee's, not the lane's.*

## 1. Synthesis + PnR (yosys synth_ice40 + nextpnr-ice40, UP5K sg48)

Command: `bash synth/silicon.sh` (artifacts: `synth/report_k4b4a8e1.json`,
`synth/stat_fabric2_k4b4a8e1.txt`, k4 b4 a8 e1 = the 15-cell legal-max fabric
config, NCELL=15, EDGES_N=4).

- **It FITS — barely: 7,596 / 7,680 ICE40 LCs (98.9%).** The largest legal
  fabric consumes essentially the whole UP5K.
- 6,002 SB_LUT4 + 898 SB_CARRY + 2,434 flops; **0 BRAM** (state is all flops —
  the conserved-state design pays area, not memory).
- **fmax achieved 44.43 MHz against a 12 ns (83 MHz) constraint — timing MISS.**
  Critical path: Hebbian edge `wh`/`age` carry chain + o_ovf reload enable,
  ~22.5 ns inside one cell's edge datapath. That is the OP_ADJ/Hebbian unit —
  the exact block the same-logic thesis (paper 224) wants to grow.

## 2. Scale sim (Verilator 5.032, NCELL=15, K=8 B=8 AGEW=24)

Command: `bash sim/vlt/run_scale.sh` (build line quoted in the script).

- **11,038,199 cycles in 139.2 s wall ≈ 79k cycles/s** on this 15-cell fabric
  (single core, -j 4 build). iverilog is ~1000× slower; this lane exists
  because of that.
- **FAILURE #1 — XFER_TIMEOUT: 6,940 errors**, all `op=3` to dst=e, repeating
  every ~4,096 cycles. Reads as a livelock/starvation signature on one
  destination, not random noise. UNADJUDICATED whether fabric bug or bench
  stimulus bug — booked as-is.
- **FAILURE #2 — P4 HASH-SENSE: different seeds, identical state hash**
  (32582fc9… for seedA/A'/B). Either the fabric's serial/hash path ignores
  part of state, or the bench hashes the wrong signal. The tournament's G2
  posture (hash = the audit organ) makes this the more serious of the two.
  UNADJUDICATED, same honesty.

Both failures are wins by house law: this is exactly what "never met a board /
never ran at scale" was hiding. Next lane's job: adjudicate both with minimal
repros, not to fix blind.

## 3. Stress experiments

Not run — the lane died at 7m46s of runtime. The two failures above came from
the P1–P4 phases that did complete. The stress matrix (max-rate effects,
reset-mid-pipeline) is specified in `sim/vlt/tb_scale_vlt.cpp` phase stubs.

— referee bench, 2026-08-30. Undersold by construction: two unadjudicated
failures, one timing miss, zero confidence inflation.
