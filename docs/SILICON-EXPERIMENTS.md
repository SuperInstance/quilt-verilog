# SILICON-EXPERIMENTS — first numbers, two failures booked (referee bench)

*2026-08-30. The lane that ran these died before its write-up and its claimed
commit (c0a13ea) never landed — phantom, per the known failure mode. The
referee bench-verified the artifacts and committed them honestly. Numbers are
real; the write-up is the referee's, not the lane's. Incident write-up:
docs/INCIDENTS.md #1.*

## 0. Adjudications (2026-08-30, devil-nudge lane — both failures now adjudicated)

**FAILURE #1 (XFER_TIMEOUT) — ADJUDICATED: bench-explained periodicity,
hardware deadlock REAL underneath.** The Devil's 2^12-register guess was the
right question with the wrong address space: the ~4,096-cycle period is the
bench's own `timeout = 4096` default in `xfer()`/`xfer_noack()`
(`sim/vlt/tb_scale_vlt.cpp`) — every failing transfer burns exactly its
timeout before printing, and the setup/phase loop then retries the same
target against a dead fabric, producing a metronome at the timeout constant.
There is no 12-bit hardware register on that path. The printout now says so
inline so the next reader doesn't re-derive the costume.

The REAL event the timeouts were masking: a **fabric-wide ring deadlock**,
captured in the preserved run log (`/tmp/vlt_out.txt`, different seed than the
committed run — same mechanism). At cyc≈34,560, ~20 ingress flits inject in 22
cycles while egress drain stalls; ring occupancy climbs 0→22 in ~20 cycles
(pipes: a/b valid in every node), all ring heads end up presenting dst=3 or
dst=f, cell 3 wedges in `state=13` with a full inbuf, and every counter
freezes (inj=208, emit=255, acc=316, drain=137 — frozen through cyc=201k).
Secondary anomaly booked with it: from the freeze onward `net≠occ`
(net=10 vs occ=36) — either the bench handshake counters undercount, or flits
exist in pipes the bench's ledger model doesn't see. Both readings are bad;
unadjudicated as sub-issue #1a.

**FAILURE #2 (P4 HASH-SENSE) — ADJUDICATED: vacuous test, not (yet) a dead
sensor.** P4's three reps each run reset + setup + 100k traffic, then hash.
But `setup_fabric()`'s own wsum-verify views are among the XFER_TIMEOUT
victims — the fabric deadlocks in setup, which is **seed-independent** (same
bind/link program every rep). Three corpses of the same deadlock hash
identically; "different seeds, identical hash" is the tautology of comparing
identical dead states. The hash sensor itself is NOT exonerated — it has
never yet read a live, seed-divergent state at scale. P4 now carries a
liveness guard (`FAIL P4 LIVENESS ... hash NOT taken` when occupancy ≠ 0 at
hash time) so it can never again hash a corpse and call it a reading.

**Downstream citations of P4/hash output:** `docs/SILICON-EXPERIMENTS.md`
only (this file, the two lines above). No README, formal doc, or academic
doc cites the P4 hash — blast radius of the vacuous reading is contained
here. The tournament's G2 "hash = audit organ" posture is unaffected: G2's
hash was never sourced from this bench.

**Verdict for the register:** both "failures" downgrade to one real failure
(the ring deadlock at scale) plus two bench artifacts (timeout-constant
periodicity, corpse-hashing). Next lane's job is unchanged but now pointed:
minimal repro of the cyc≈34.5k deadlock (burst injection → drain stall →
ring fill), starting from the cell-3 state=13 wedge and the dst=f drain
path.

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
