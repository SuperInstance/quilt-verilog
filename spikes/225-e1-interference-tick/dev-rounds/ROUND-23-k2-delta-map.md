# ROUND 23 — Δ-resolved comp-wall map at K=2 vs K=1 (round 22's named next rung)

## PART 1 — PRE-REGISTRATION (committed before any comparison number is computed)

**Item.** Round 22 booked K=2 as Δ-flat at Δ≤16 (walls 4,4 at Δ=8/16) and the whole Δ=12
grid structureless; the open question is whether K=2 stays flat at ALL Δ or crosses to the
quarter-power F2=⌈2·r^0.25⌉ regime at Δ≥24 (at K=2, r=Δ/2, so F2 predicts wall 4 at Δ≤24,
5 at Δ∈(24,48], 6 at Δ=48 — Δ=48 is the first cell where F2 separates from flat by 2 seats).
If K=2 never crosses, the K-line is a true phase boundary between the single-stream (K=1)
world and the multi-stream world, and only the K=1 seating table needs a pd-stratified model.

**Design.** Extend the r21/r22 harness (r21_compwalllaw.py / r22_regimemap.py). Sweep
Δ ∈ {8,12,16,20,24,32,48} at K=2, pd ∈ {2,3} (both, to check pd-interaction), comp arm
(lag-compensated mag+C=1 vs admit-all), N ∈ {2..13}, 4800 ticks, seeds 1/7/42/1999/20260902.
K=1 control cells at Δ ∈ {8,16,32} × pd ∈ {2,3} for continuity with the SPIN-32 seating
(round 21). Wall per cell = gate-clearing N (first N where mean comp win ≥ 2.0 pp), as in
rounds 19–22. NOTE (harness fix, declared): r22's pd-grid hard-coded pulse_div=3 (its pd
axis was inert); r23 passes pd through as r21 did, so pd cells here are real. The C2 anchor
replay is run at pd=3, which is what r22 actually measured.

**PRE-REGISTERED DECISION RULE (frozen):**
- **CROSS:** if K=2 walls grow with Δ beyond Δ=16 (wall ≥ 6 at Δ ≥ 24 in any pd cell) →
  book K=2 crosses to the F2 regime; record the Δ*(K=2) crossing point.
- **FLAT-ALL:** if K=2 walls stay ≤ 4 through Δ=48 in all pd cells → book the K-line as a
  true phase boundary between single- and multi-stream worlds; the K=1-only
  pd-stratified model stands.
- **AMBIGUOUS:** anything else (e.g. intermediate growth, 5-only) → map honestly, name
  the next resolving probe.

**Constraints.** Integer-only arithmetic in the fabric and verdict (r^0.25 used only for
F2 reference values, printed, never compared with floats — F2 precomputed exactly:
F2(r): r=4→4, r=6→4, r=8→4, r=10→4, r=12→4, r=16→4, r=24→4, r=32→5, r=48→6).
Seeds 1/7/42/1999/20260902 fixed. No floats in verdict computation (walls are integers).

**Canaries / anchors (frozen, all must pass before any verdict):**
- **C1** round-21 octave replay: pd=3, calm family (K=8, drift=3), r ∈ {1,2,6} →
  comp walls 2/3/4 EXACT.
- **C2** round-22 K=2 replay: pd=3, K=2, Δ ∈ {8,16}, calm drift=3 → walls 4/4 EXACT.
- **C3** double-run byte-identity: one full cell (K=2, pd=3, Δ=48) run twice; the
  deterministic per-cell dump lines must be byte-identical.
- **C4** mislabeled-arm self-canary: mag+C=1 relabeled admit-all at the round-2 anchor
  cell (N=5 stress default Δ=12 K=4 pd=3: raw=68.0, sort=69.6) must be CAUGHT
  (mislabeled %w ≠ 68.0 while the true anchor replays PASS).

**Deliverable.** This file (PART 1 → run → PART 2), r23_k2deltamap.py, raw output
r23-k2deltamap-output.txt. Commit+push to g3-kinduction (Casey override); other lanes'
uncommitted files (wheel/WHEEL-LOG.md, cosim/*) untouched.
