# ROUND 24 — K=1 seating at drift-matched grid (two-knob vs Δ-artifact)

## Item

Round 23's named next rung. The K=1 pd=3 comp-wall is 6 and Δ-flat at
drift=3 (r23 controls: 6/6/6 at Δ=8/16/32). Round 21 (SPIN-32 seating,
drift=6, Δ∈{8..16}) saw K=1 walls 6/9/11/None across pd∈{3,4,5,6}. Question:
does the K=1 pd=3 comp-wall re-acquire Δ-growth at drift=6? I.e., is
pd-stratification a two-knob (pd,drift) object — each (pd,drift) cell has its
own Δ-flat wall — or was round 21's structure a Δ-range artifact of its
narrow Δ∈{8..16} grid?

## Grid (frozen)

K=1 × pd∈{3} (anchor) × drift∈{3,6} × Δ∈{8,16,32,48} × N∈{2..13},
comp arm (mag+C=1 vs admit-all, run_sw_comp), calm, seeds 1/7/42/1999/20260902,
4800 ticks, wall = first N with mean win ≥ 2.0pp (identical to r21/r23).
Integer-only arithmetic in all measurement paths.

## Canaries (all required, any fail → no verdict)

- C1: double-run byte-identity of the (pd=3, drift=6, Δ=8) cell dump.
- C2: round-23 K=1 anchor replay EXACT — drift=3: pd=2 Δ{8,16,32} → 4/4/4,
  pd=3 Δ{8,16,32} → 6/6/6.
- C3: mislabeled-arm self-canary at the round-2 anchor cell
  (N=5 stress default: raw=68.0, sort=69.6); verdict logic must CATCH the
  deliberate mislabel (sort reported as raw).

## Decision rule (frozen BEFORE any comparison number)

Let wall(drift, Δ) be the K=1 pd=3 comp wall.

- **DRIFT-TWO-KNOB** if: drift=6 shows Δ-monotone (non-decreasing) growth
  ≥ 2 seats from Δ=8 to Δ=48 (wall(6,48) − wall(6,8) ≥ 2) AND drift=3 stays
  flat (max−min ≤ 1 across Δ). → Δ re-enters the K=1 world only under
  drift=6; pd-stratification is a genuinely two-knob (pd,drift) object.
- **DRIFT-ARTIFACT** if: drift=6 stays flat or moves ≤ 1 seat across all Δ
  (walls equal to the drift=3 wall ± 1), with no Δ-monotone trend. → Round
  21's pd-ladder lives at its (pd,drift) seats independent of Δ; the
  Δ-blindness of r23 extends to drift=6; two-knob object with Δ-flat walls.
- **AMBIGUOUS** otherwise (incl. any None wall at drift=6 Δ=8 — if the wall
  sits above N=13 at the left edge we cannot read growth; booked honestly
  with the seated cells only).

## Verdict

(to be filled after the run)
