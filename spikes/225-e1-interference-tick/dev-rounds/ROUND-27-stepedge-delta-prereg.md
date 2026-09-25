# ROUND 27 — PRE-REGISTRATION: step-edge Δ-sweep at drift=12 (commit BEFORE any run)

Branch g3-kinduction · lane dev_r27_stepedge_delta · dispatched 2026-09-04 08:31 AKDT.

## Item (round 26's named next rung)

Is the drift-12 +1 parity step (the only drift-sensitive object in the r26
ladder: step crossing 2pd→2pd+1 migrates from pd 3→4 to pd 4→5 at drift 12,
lone deviation cell (12,4) wall 8 vs 9) **Δ-carried**? Prior evidence: r24
booked walls Δ-blind at drift 3 and 6 (Δ up to 48) — but the step edge is the
drift-sensitive object, so Δ may matter exactly there.

## Grid

- K=1, comp arm, calm regime, drift=12, pd ∈ {3,4,5} × Δ ∈ {8,12,16,24,32,48},
  N swept 2..18 (r26 harness wall-locating range), seeds 1/7/42/1999/20260902.
- Control: drift=6, pd=4, same Δ set (should stay 9 per r26, all Δ).
- Harness identical to r26_driftpd.py (same lats_for, same wall rule
  wall = first N with mean comp-arm win ≥ 2.0pp; integer-only plant, real runs).

## DECISION RULE — frozen before any run; never edited after a panel run

- **M1 (step edge Δ-carried at high drift):** if wall(12,4) moves ≥1 seat
  across the Δ set (i.e. not constant over Δ ∈ {8..48}) → book two-object
  model: ladder Δ-blind (r24/r26) + step edge Δ-sensitive at high drift.
- **M2 (Δ-flat; law closes):** if wall is Δ-flat in ALL three pd cells
  {3,4,5} at drift 12 (constant across the full Δ set in each cell) → the
  drift-12 step migration is Δ-blind like everything else; the (drift,Δ,pd)
  wall law closes as wall = 2pd / 2pd+1 with the step edge a pure
  (drift,pd) object. **Book as LAW.**
- **M3:** anything else (e.g. Δ-motion in pd 3 or 5 but flat at pd 4, walls
  None within N≤18, or rule-relevant cell disagreement between verdict
  criteria) → describe honestly, book as measured.

M1 vs M2 are decided on wall(12,4) and the Δ-flatness of all three pd cells;
pd=3 and pd=5 Δ-motion triggers M3, not M1.

## Canaries (all must pass before verdict)

- C1 double-run byte-identity (drift=12, pd=4, Δ=12 win vector ×2).
- C2 r26 drift-12 ladder anchor replay: pd 2..6 walls at Δ=12 must replay
  exact — expected 4 / 6 / 8 / 11 / 13 (incl. the (12,4)=8 deviation).
- C3 mislabeled-arm self-canary (sort↔raw swapped arms on one cell must be
  CAUGHT: wall differs from true).
- C4 drift=6 control cell (pd=4) replays r26's 9 at every Δ.

## Seeds / arithmetic

Seeds fixed 1/7/42/1999/20260902; integer-only arithmetic in-loop (no floats
in the decision path); real runs, no simulated results. One lane, no
sub-lanes. Other lanes' uncommitted files untouched.
