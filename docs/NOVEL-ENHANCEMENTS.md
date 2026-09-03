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
