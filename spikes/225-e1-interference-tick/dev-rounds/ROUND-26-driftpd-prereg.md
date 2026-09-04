# DEV ROUND 26 — PRE-REGISTRATION — drift×pd seat-field law (product vs separable)

Frozen BEFORE any new output number. Committed before runs.

## Item
Round 24's named rung, sharpened by round 25: K=1 comp-wall seat wall(pd,drift)
at Δ=12. Round 25 booked wall = 2pd (pd≤3) / 2pd+1 (pd≥4) at drift=6. What do
drift=3 and drift=12 do to that ladder?

## Grid (frozen)
K=1, comp arm (mag/C=1 vs admit-all, run_sw_comp), calm regime, Δ=12,
drift ∈ {3,6,12} × pd ∈ {2,3,4,5,6}, N ∈ {2..18}, seeds (1,7,42,1999,20260902),
4800 ticks, wall = first N with mean win ≥ 2.0pp (identical to r21/r23/r24/r25).
Latency grid lats_for(n) identical to r25.

## Decision rule (frozen; evaluated in this order; no rescue clauses)
Let wall(d,pd) be the measured ladder.

1. **DRIFT-BLIND** (falsifier (a)): if for every pd ∈ {2..6},
   wall(3,pd) = wall(6,pd) = wall(12,pd), book DRIFT-BLIND — the r25 ladder
   holds verbatim at all three drifts; r24's drift-artifact booking extends to
   the full pd-ladder; product and nontrivial separable laws both falsified
   (drift knob carries zero information at these settings).
2. **PRODUCT** (falsifier (b)): consider collision pairs with equal pd·drift:
   (drift,pd) ∈ {(6,2),(3,4)} → 12; {(12,2),(6,4),(4,6)} → 24;
   {(12,3),(6,6)} → 36. Book PRODUCT if every collision pair has EQUAL walls
   (±0 seats) AND walls are nondecreasing in pd·drift across the grid.
3. **SEPARABLE** (falsifier (c)): book SEPARABLE if wall(d,pd) − wall(3,pd)
   is the same constant for d ∈ {6,12} at every pd (column offsets constant
   across the pd axis, at least one offset nonzero).
4. Else book UNBOOKED/two-knob: wall is a genuinely two-knob object; report
   the measured field.

## Sub-probe (frozen)
STEP-LOC: does the +1 step (2pd → 2pd+1) sit at the pd=3→4 crossing at every
drift? Booked per-drift: YES if wall(d,3)=2·3 and wall(d,4)=2·4+1 both hold;
report exact offsets. (At drift=3, pd=6 wall vs N≤18 ceiling: if None, book
"past ceiling at 18" — round-25 lesson; do not extrapolate.)

## Canaries (all required; any FAIL → no verdict)
- C1 (r25 anchor replay): drift=6 column must read walls 4/6/9/11/13 EXACT
  for pd=2/3/4/5/6.
- C2 (double-run byte-identity): drift=6, pd=3 win-vector printed twice,
  values must be identical.
- C3 (mislabeled-arm self-canary): one cell computed with sort/raw arms
  swapped must NOT reproduce the true wall (detector must flag a difference);
  if the swap goes unnoticed, harness is broken → no verdict.

## Deliverables
r26_driftpd.py, r26-driftpd-output.txt, ROUND-26-driftpd-law.md, ROUNDS.md
append. Commit messages: this file → 'round 26 pre-registration: drift×pd
seat-field law (product vs separable)'; results → 'round 26: driftpd law:
<verdict>'. Push to g3-kinduction only, no force.

Fresh cells flagged: pd=3@drift=3, pd=4@drift=12 (first measurement).
