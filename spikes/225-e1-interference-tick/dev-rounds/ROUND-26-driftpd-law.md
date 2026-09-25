# ROUND 26 — drift×pd seat-field law (pre-registered 485560e): DRIFT-BLIND IN 14/15 CELLS — one seat moves

**Verdict: two-knob by the frozen letter, drift-blind to first order.** The
prereg rule fires its fourth branch: the ladder is identical at drift=3 and
drift=6 in ALL five pd cells, identical at drift=12 in four of five — the
single deviation is (drift=12, pd=4): wall 8, one seat BELOW the r25 ladder's
9. Product law dead on collision pairs (pd·drift=24 column reads
4/9/13 — no collapse); separable dead on non-constant offsets
(d12−d3 = {0,0,−1,0,0}). Neither (a)-full nor (b) nor (c); booked as the
measured field with the drift-blind exception named.

## The measured ladder (K=1, comp arm, calm, Δ=12, N 2..18, 5 seeds)

| drift \ pd | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| 3  | 4 | 6 | **9** | 11 | 13 |
| 6  | 4 | 6 | **9** | 11 | 13 |
| 12 | 4 | 6 | **8** | 11 | 13 |

(r25 anchors = drift=6 column 4/6/9/11/13 — replayed EXACT.)

## What books

1. **Drift-blind to first order.** r24's drift-artifact booking (wall=6 at
   pd=3 for drift 3 and 6) extends across the whole pd-ladder: 14/15 cells
   carry zero drift response over a 4× drift range (3→12) at Δ=12. The wall
   is NOT a function of pd·drift (product falsified) and not g(pd)+h(drift)
   with nonzero h (separable falsified); the dominant law is h≡0.
2. **The lone seat that moves eats the +1 step.** At (12, 4) the wall drops
   9→8, landing exactly ON 2pd. STEP-LOC sub-probe: the 2pd→2pd+1 crossing
   sits at pd=3→4 at drift 3 and 6 (YES/YES) but NOT at drift=12 — the step
   erodes from the bottom, exactly where the ladder's parity flip lives
   (round-25 booking: pd≤3 even, pd≥4 odd). One-seed noise cannot do this:
   mean win curves jump +2pp gates, and the same cell reads 9 at both lower
   drifts. Interpretation (labeled post-hoc): the +1 premium is drift-carried
   at the ladder's step edge only — the only place in the field where a
   parity-changing seat exists to be moved.
3. **2pd boundary law half-resurrected again.** At drift=12 the wall touches
   2pd at pd∈{2,3,4} and sits +1 at {5,6} — the r25 step has migrated from
   pd=3→4 to pd=4→5 at this drift. The step LOCATION, not the step magnitude,
   is the drift-sensitive object.

## Canaries
- C1 r25 anchor replay: drift=6 column EXACT (4/6/9/11/13) — PASS.
- C2 double-run byte-identity (drift=6, pd=3 win vector ×2): IDENTICAL — PASS.
- C3 mislabeled-arm self-canary: swapped-arm probe wall=2 ≠ true 6 — CAUGHT.

## Named next rung
**Step-edge probe:** at (drift=12, pd=4), is 8 vs 9 a knife-edge (which seat
does the win curve actually clear by, and by how much)? Sweep Δ at drift=12 —
if the erosion is Δ-carried (r22 booked pd-stratification as Δ-carried),
Δ∈{8,16,32} × pd∈{3,4,5} at drift 12 locates whether the step edge is a
drift×Δ object. Falsifier: if the step returns at 9 for all Δ, the (12,4)=8
cell is a boundary anomaly and the field books pure drift-blind.

Raw: `r26-driftpd-output.txt` (148 s). Fresh cells as preregistered:
pd=3@drift=3 → 6, pd=4@drift=12 → 8.
