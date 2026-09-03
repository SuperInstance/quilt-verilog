# NOVEL ENHANCEMENTS — quilt-verilog deep-think (Lucineer, 2026-09-02 21:25 AKDT)

Premise from tonight's charter: the fabric is a snap-point engine (§9/§10) whose readout is
already feeler-gauge points. quilt-verilog is that idea in silicon. Each enhancement below
is stated as: idea → concrete RTL/formal artifact → how it verifies (sby is fast: ~0 s
basecase+induction, so every idea is provable, not just testable).

## T1. QUF-SNAP: the state file becomes an append-only snap log
QUF carries complete state (GGUF of cellular silicon). Add the complementary object: a
fire-event ring buffer per fabric (snap-point log, §9). State + log = full replay; the
testbench, soft core, and FPGA load identically as today, but now history is auditable.
- RTL: `q_snaplog.v` — fire address+sign+tick packed into one wide shifter; overflow drops
  oldest (feeler gauges are finite).
- Formal: prove replay equivalence — from (QUF@t, log[t..t+n]) the C99 model reproduces
  QUF@t+n byte-identical. This is the DIVERGENCE.md window-edge bug class killed in
  hardware, the same bug glm-1's auditor caught in simulation.
- Novelty: FPGAs do not normally expose replayable history; this makes time-travel a
  file-format feature.
- STATUS 2026-09-02 (chip-fleshing lane): sketch landed as `rtl/q_snaplog.v` —
  parameterized one-wide-shifter ring (default 16 × 45-bit entries:
  tick24+sign+src4+mag16), free-running tick stamp, freeze hold, audit-drop
  counter, newest-at-index-0 read port. iverilog -g2005 -Wall and verilator
  -Wall lint clean; elaboration checked at DEPTH=1 / DEPTH=32 / MAG=0.
  UPDATE 2026-09-03 (eco-quiltverilog tick): first sby run FAILED — and
  correctly: the shifter "shift" `{log[TW-1:EW], entry}` width-checks
  clean but leaves upper entries IN PLACE (one-entry overwrite, not a
  shift); readback of any index >= 1 returned zeros while o_count claimed
  valid entries. Fixed to `{log[TW-1-EW:0], entry}`; reproduced in
  iverilog sim, lint clean, and all four formal harnesses now close:
  snaplog.integrity (BMC 30, exact content+order vs shadow log),
  snaplog.counters.prove (k-induction, unbounded),
  snaplog.integrity.pdr (PASS), snaplog.integrity.cover (saturation +
  overflow drops reached at step 20). No longer UNVERIFIED (lint is not evidence; see TEACHER note below):
  formally proven + the T9 replay TB remains future work. T9 below is
  its UP5K block-RAM backing.

## T2. Contention-sorted admission in the tick scheduler (glm-3's §8 controller → RTL)
q_tick_sched is round-robin. A 5-row bitonic sort on {contention, magnitude} + a budget
comparator = the sorted switchboard as silicon: admit only the loudest discrepancies when
scarce. glm-3 measured the win in simulation (max err 232 vs 281, events −30% at C=1);
RTL makes it cycle-accurate.
- Formal: prove admission-fairness (a twin starved C consecutive ticks must have had
  contenders admitted above budget — no silent starvation) and net==0 conservation across
  the scheduler.

## T3. The byzantine whistle as a proven tripwire
glm-1's one-counter alarm (cancellation-spike ×2–×5 over honest baseline, 5/5 seeds) is
cheap enough to be a per-edge hardware counter.
- Formal target: a bounding invariant — under any single lying input, cancellation rate is
  bounded above honest baseline by a provable constant. If sby closes it, quilt-verilog is
  a cellular fabric with a *formally proven* adversarial tripwire. Nobody has that.
- STATUS 2026-09-02 (chip-fleshing lane): sketch landed as `rtl/q_whistle.v` —
  saturating per-window cancel counter, limit = base × mul (dial-dial
  multiply), judged at every tick boundary, sticky alert + strike tally +
  last-window histogram for host recalibration. Lint clean both tools.
  UPDATE 2026-09-03 (eco-quiltverilog tick): first sby run — both
  directions close. whistle.honest (mode prove, k-induction, UNBOUNDED):
  honest windows never alarm, no false positives under any stimulus.
  whistle.attack (BMC 45): sustained maximal lying trips the alert at
  the first judged window, within bound, every legal dial pair. Covers
  reached (alarm step 5 honest-side window, attack step 18). The
  bounding-invariant aspiration above is now a PROVEN bounded-form
  start; the full cancellation-rate constant remains future work (see
  module header lemma). This is the artifact the EXPERT cross-exam
  booked: dice acceptance for admission = whistle FP rate with dice
  live — whistle FP-free is now proven, the dice-live integration TB
  remains the open half.

## T4. K as a runtime dial (the arena artifact, corrected in metal)
glm-3 found the ledger's "interference worse at high K" was a K=8 grid artifact — K=2/3
dominates. q_hebb_edge's fan-out should be a dial (LUT-masked), not a parameter baked at
elaboration. Night-queue experiment first (replay champion frames at K=2/3), then RTL.

## T5. The dialometer as BIST (§9 → built-in self-test)
Sweep the coding plane: rotate the dial/pulse phase continuously and record fire smoothness.
A concentric fabric sweeps smooth; a defect shows as runout (flat spot / chatter) with
phase locating the joint. Silicon health measured as machinists measure shafts.
- Artifact: `q_bist_sweep.v` + pass/fail = runout ≤ 1 quantum. Novel: alignment-testing
  logic by sweeping its own projection plane.

## T6. Cheating on purpose: snap-only observability theorem (§10)
The FPGA already cannot see the wave — only instrumented points. Make that a theorem:
formally prove observable behavior ≡ snap-log behavior (nothing observable is lost by
reading only where blades fit). That proof IS the cheat-code claim, closed in sby, and it
licenses deleting every debug wave port — smaller bitstream, harder guarantee.

## T7. Use the headroom (44.43 MHz post-route on a 12 MHz target)
Two gears for the same silicon: (a) time-multiplex ~3× more cells per LC set at 36 MHz;
(b) variable-rate tick = physical phase-gating — but glm-3's result warns phase gating is
a throttle (83.1→60.2), so book (b) as antiphase turn-taking only (cancellations −96%),
never as a resonance claim.

## T8. QUF diff as a first-class instruction (§8 in the file format)
Flat binary state ⇒ hardware/soft-core diff between two QUFs = edit distance over cell
dials. The switchboard sorted across TIME. Feeds fleet-twin: two boats' fabrics diff
byte-wise to find divergent joints.

Priority by (insight × cheapness): T3 (proof nearly free, uniqueness high) → T1 (format
extension, big story) → T2 (glm-3 evidence in hand) → T6 (theorem that simplifies the
design) → T5 → T4 (night-queue first) → T7 → T8.

---

# T9–T15 — one idea per chip resource (chip-fleshing lane, 2026-09-02)

The T1–T8 round was chip-agnostic. This round aims each idea at a SPECIFIC resource
on a SPECIFIC die on the desk, so "use the headroom" and "log the fires" stop being
slogans and become budget arithmetic. Resource facts pinned first (datasheet round,
2026-09-02): **UP5K sg48** = 5,280 LC + 120 Kb EBR (30 × 4 Kb) + 1 Mb SPRAM
(4 × 256 Kb single-port) + **8 hard DSP (MAC16, 16×16 MAC)** + 2 PLL — the only
iCE40 on the desk with hard DSP or SPRAM. **HX8K-CT256** = 7,680 LC + 128 Kb EBR,
no DSP, no SPRAM, 2 PLL, and 44.43 MHz post-route against a 12 MHz target
(SYNTHESIS-RESULTS Table 1) = **3.70× timing headroom**. **ECP5 LFE5U-12F/25F** =
12,144/24,288 LUT, 32/56 sysMEM EBR (18 Kb), **28 × 18×18 DSP multipliers both
dies**, sysIO banks with differential/DDR inputs. Every idea below: mechanism →
resource → verification → honest novelty claim. All UNVERIFIED (lint is not evidence; see TEACHER note below) until
the named verification runs.

## T9. The SPRAM flight recorder — q_snaplog at 16,384 marks (UP5K)
- **Mechanism:** back T1's `q_snaplog` ring with the UP5K's 4 × 256 Kb SPRAM
  (`SB_SPRAM256KA`, inferable from a 16-bit synchronous single-port template —
  no vendor primitive in the RTL, the yosys memory mapper does it). Entry packs
  to 4×16-bit words (64 b: tick 32 + sign 1 + src 4 + mag 16 + pad 11):
  16,384 words per block ÷ 4 = 4,096 entries/block, **16,384 entries across the
  four blocks ≈ 1,000× the default FF gauge**. A whole judge session's fires
  retained on-chip; QUF + spool = a flight recorder, dumpable through the serf
  front-end's 37 pins.
- **Resource:** UP5K SPRAM (unique on the desk — HX8K has none).
- **Verify:** differential TB — spool replay through `tools/quf.py`'s C99 model
  must reproduce the final QUF byte-identical; the T1 invariants (monotone tick,
  drops = fires − DEPTH) re-stated at depth 16K in a snaplog sby; later-synth
  check that yosys infers SPRAM, not LCs.
- **Novelty (honest):** BRAM ring buffers are textbook. The claim is the FORMAT:
  an append-only companion provably SUFFICIENT for replay (T1/T6) sized by the
  chip's largest storage — an auditable fabric, not a log buffer.

## T10. The whistle battery on hard DSP (UP5K MAC16 / ECP5 DSP slices)
- **Mechanism:** two existing multiplies are already DSP-shaped: `q_whistle`'s
  limit = base × mul, and `q_cell_core`'s effect product (ST_EFFM, 16×16).
  Budget arithmetic decides the deployment: per-CELL whistles on ECP5 = 8
  multipliers of 28 — fits with the effect cone beside it; per-EDGE = 8 cells ×
  4 edges = **32 > 28 — does not fit, and that bound is the design decision**
  (per-cell default, per-edge only on a smaller fabric or shared-schedule
  whistle). On UP5K, one MAC16 of 8 takes a whole cell's whistle+effect math.
- **Resource:** hard DSP tiles (UP5K MAC16, ECP5 18×18) — silicon the LC-full
  fabric cannot otherwise buy.
- **Verify:** values bit-identical ⇒ existing TBs unchanged; the check is
  resource accounting — yosys `stat` on both families must show the multiplies
  landing in DSP, plus the LC delta (later, synth lane; not run tonight).
- **Novelty (honest):** DSP mapping is toolchain routine. The claim is the
  budget argument: a formally-specified adversarial tripwire whose silicon
  price is slices nothing else wanted — Byzantine detection affordable because
  it lives where the fabric is not LC-starved.

## T11. One clock, three phases — the headroom as capacity (iCE40 PLL × HX8K TDM)
- **Mechanism:** 44.43/12 = 3.70× headroom says the CURRENT netlist closes at
  36 MHz. Use a hard PLL to synthesize 3× the target and run a 3-phase
  time-multiplexed datapath under ONE clock domain — phase = 2 bits of the tick
  counter; cell contexts rotate; no clock-domain crossing anywhere. T7b's
  caution is honored by construction: antiphase turn-taking is clock-ENABLE
  gating per phase, never clock switching (glm-3's 83.1→60.2 throttle stays a
  warning, not a design input). NCELL 2 → 6 virtual cells on the same LC set.
- **Resource:** iCE40 hard PLLs (HX8K 2×, UP5K 2×) + the measured 3.70× slack.
- **Verify:** differential TB — virtual 6-cell TDM fabric vs the C99 model (and
  cross-checked against a REAL 6-cell netlist, which fits only ECP5),
  byte-exact traces; formal: conservation restated PER PHASE WINDOW (sby stays
  small — the obligation is per-phase-bounded, not per-silicon); later-synth:
  36 MHz closes at existing margin.
- **Novelty (honest):** TDM is ancient. The claim: logical cells outnumber
  physical LCs WITHOUT weakening net==0 — the theorem survives multiplexing
  because the proof obligation is phased, and that phrasing is the artifact.

## T12. The ring goes electrical — boat-to-boat fabric on one sysIO pair (ECP5)
- **Mechanism:** the serf front-end proved the config plane serializes
  byte-exact through 37 pins. Extend the same discipline to a PEER link:
  `q_link_ringport`'s flit stream, framed (idle/mark/credit/delete) onto ONE
  differential sysIO pair with DDR input sampling — two ECP5 boats share ONE
  ring: cells on both chips, one scheduler, one conservation proof, link
  backpressure as explicit flits. The hundred-boats doctrine at the electrical
  layer: the interconnect IS the fabric, not a bus beside it.
- **Resource:** ECP5 sysIO banks (differential + DDR receivers — the resource
  the iCE40 boards lack).
- **Verify:** TB on the framing alone (byte-exact round trip, insertion of
  idles, backpressure both directions); formal: extend
  `formal/fabric.conservation.sby` with a two-node link model so net==0 holds
  ACROSS the pair; later-synth: DC-balanced line coding vs margin.
- **Novelty (honest):** LVDS inter-FPGA links are old. The claim: ring topology
  crossing a chip boundary with conservation still provable — two fabrics
  auditable as one.

## T13. PicoRV32 as fabric citizen — the proof-carrying seam (ECP5 LUT headroom)
- **Mechanism:** one small PicoRV32 (~1–1.5 k LUT) rides the io flit port as a
  FABRIC CITIZEN, not a host: firmware drains `q_snaplog` (T1), recalibrates
  `i_base` from the whistle's `o_hist` stream (T3), computes QUF diffs (T8)
  on-chip, and implements the T2 admission controller as policy-in-firmware.
  Fits only where LUTs remain: ECP5 25F at NCELL=4 has ~12.7 k LC free; HX8K
  at 98% does not fit — ECP5-only by arithmetic, not preference.
- **Resource:** ECP5 LUT headroom (the only desk chip where core + fabric co-fit).
- **Verify:** the cosim lane extended: RVFI instruction trace + RTL fire log +
  QUF snapshot = THREE independent views of one computation, each replayable
  by the C99 model to the same final state; formal: cite riscv-formal for the
  ISA seam (upstream's proof, not ours), own the flit-interface obligations.
- **Novelty (honest):** soft cores are routine. The claim: three independently
  checkable traces cross-validated by one 500-line C model — the fabric audits
  its own auditor.

## T14. The Feynman-desk ledger — every chip one tick grammar, the FPGA referee
- **Mechanism:** CHIP-MATRIX already runs GPU/CPU cells (100.0% parse both
  lanes, QUF-verified checkpoints); the FPGAs run RTL cells; the QUF is the
  shared format. Add the desk-level epoch ledger: each chip's tick windows
  Lamport-stamped in the snap-log tick field (already there — T1's stamp IS an
  epoch counter), divergences found by QUF diff (T8), and the FPGA's tick
  order is the desk's wall-clock BY CONSTRUCTION (Q2: the tick is
  non-deferrable). A heterogeneous fleet — RTX 4050, HX370, UP5K/HX8K/ECP5 —
  with a deterministic referee whose ordering is a theorem, not a convention.
- **Resource:** no special silicon — the desk is the resource; on each FPGA the
  tiebreak port rides the existing io flit (EXTID), zero new pins.
- **Verify:** host-side first (zero new RTL): `tools/quf.py` diff over the
  desk's existing per-lane `.quf` checkpoints; RTL piece = Lamport
  monotonicity joins the snaplog sby; cosim: two fabrics' logs interleave to
  one desk order, C99 model replays the merge.
- **Novelty (honest):** distributed snapshots (Chandy-Lamport) and federated
  state are classical. The claim: GPU + CPU + RTL cells sharing one bit-exact
  state file with a silicon referee — to our knowledge no desk does that.

## T15. The headroom as assurance, not capacity — lockstep shadow fabric (HX8K)
- **Mechanism:** T11 spends the 3.70× headroom on cells. Same phase machinery,
  opposite purchase: a SHADOW copy of the fabric — full second register state
  (~2.4 k FF), sharing the ONE phased LC datapath — runs every flit one phase
  behind; each tick boundary the shadow's QUF-visible state is diffed (T8 as a
  live instruction, not a host tool); any divergence raises an on-chip
  assertion strobe. The fabric proves itself WHILE it runs.
- **Resource:** HX8K timing headroom (shared datapath at 36 MHz) + FF budget
  (state banks are flip-flops, and FFs — not LCs — are what a shadow adds).
- **Verify:** formal: shadow-diff strobe == 0 is EXACTLY the conservation
  obligation restated as an equivalence bound — one sby, two instantiations,
  same flit stream; TB: fault injection (one flipped effect flit) must trip
  the strobe within one tick.
- **Novelty (honest):** lockstep comparison is classical fault detection. The
  claim: a cellular fabric whose self-audit is the T8 diff engine executed
  in silicon, at zero extra LC cost, sharing one datapath — assurance as a
  use of slack, alongside capacity.

Priority for the new round (verifiability × resource unlock): T13 (three-view
replay, all pieces exist) → T9 (format story, TB is the C99 replay) → T15 (same
machinery as T11, stronger claim) → T11 → T10 (synth-lane measurement) → T12
(framing TB now, silicon later) → T14 (host-side tonight if the desk lanes keep
their artifacts).

## Artifact status, honestly (2026-09-02, chip-fleshing lane)

Landed tonight: `rtl/q_snaplog.v` (T1) and `rtl/q_whistle.v` (T3) — generic
IEEE 1364-2005, parameterized, no vendor primitives, house style. Lint:
iverilog -g2005 -Wall clean, verilator --lint-only -Wall clean (per top),
elaboration checked at degenerate/deep parameter corners (DEPTH=1, DEPTH=32 /
TICKW=32 / MAG=0; DEPTH=1 found and fixed a real out-of-order part-select).
NOT done, on purpose: no simulation, no sby runs, no synthesis (no toolchain
run was promised tonight), no commit. Everything above this line marked UNVERIFIED (lint is not evidence; see TEACHER note below) is exactly
that.

## Naming convention, sharpened (TEACHER nudge, 2026-09-03)

The snaplog shifter bug (caught by the first proof run, 700380c)
width-checked clean in BOTH linters and lived until a formal property
asked readback semantics — the third such catch in one day. Conclusion,
now doctrine: **lint-clean is negative evidence of nothing**; it
validates bit-count, never bit-meaning. The status tag
UNVERIFIED (lint is not evidence; see TEACHER note below) is retired and replaced by UNVERIFIED (with the
evidence named: what ran, what closed). An artifact may cite: lint
(exists), sim (one path), formal (all paths), proof (all paths +
induction). The T1–T8 program's credibility rests on which rung each
claim actually occupies; the snaplog fix is the worked example of why
the ladder is not pedantry.
