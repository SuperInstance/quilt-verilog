# ROUND 21 — comp-wall form pinning + pd legs + SPIN-32 seating (pre-registered cde784c→228fbc0, EXPERT nudge): F2 banks as the comp-regime form, pd-invariance FAILS at pd=6, and the K=1 regime is a different object entirely

**Verdict: SPLIT by the pre-registered gates.** G-FORM: **F2 = ⌈2·r^0.25⌉ banks decisively** (6/8 exact, 8/8 within ±1; F1 = 2+round(0.9·log₂ r) gets only 4/8). **DOMAIN STAMP (do not apply F2 outside it): K ≥ 4, pd ≤ 3 — swept domain K ∈ {4,8}, pd ∈ {2,3}, both families; applying F2 at pd=6 is 2–4 seats wrong (STUDENT nudge, round 22 extends the map).** G-COLLAPSE: **FAIL** (69% < 80% — pd=6 legs blow out). The combined headline claim ("first closed-form wall law, pd-invariant") required both gates and is therefore **NOT banked**. What is banked is narrower and stranger.

## The form adjudication (pd=3, fam-mean, abstain on wide fam-split)

- Off-octave cells decided it exactly where predicted: r=0.6→2 (F1 said 1, F2 said 2), r=1.25→3 (F1 2, F2 3), r=8→4 and r=10→4 (F1 said 5, 5). F2's only misses are r=4 and r=5 (obs 4, F2 said 3 — under-prediction, both missed in the same direction).
- Read: the comp wall grows like r^0.25 — **a quarter-power law in arrival rate**, not logarithmic. Both fitted forms were frozen from octave data before any off-octave number existed (cde784c); the octave replays (2/3/4) passed first.

## G-COLLAPSE fail: "pd-invariant" was a pd≤3 statement

pd=2 legs sit within ±1 of pd=3 (the round-19 collapse replicates there), but **pd=6 is off by 2–4 seats everywhere** (r=4: walls 6/8 vs pd=3's 4/3; r=8: 6/7 vs 4/4). In the comp regime, high pd *delays* the wall sharply — compensation helps less when pulse mass per correction is smaller (m = |e|//pd). Round 19's "single curve" was real but its domain was pd ∈ {2,3}.

## SPIN-32-cell seating (K=1, drift 6, r=Δ) — the bridge table, and it bridged to a surprise

At the exact (pd,Δ) cells SPIN-32 fit: **the comp wall is Δ-INVARIANT within each pd** (pd=3: 6,6,6,6,6 across Δ 8..16; pd=4: 9,9,9,9,8) and **pd-stratified** (pd=6: no N ≤ 12 clears +2pp at all). pd-invariant cells: 0/5 across pd — but invariant *in Δ*, which is its own law-shaped signature. At K=1 the gate threshold Δ and the pulse divisor pd apparently act on different sides of the wall: the seat depends on pd alone.

## Booked reading

Three regimes, one fabric:
1. **Raw wall** (rounds 17/19): two-knob fan-out object, pd a ±1 modulator.
2. **Comp wall, K≥4, pd≤3**: ⌈2·r^0.25⌉ — the banked form candidate; next SPIN-32-style family for THIS regime carries δ/K as a term, exactly as EXPERT argued.
3. **Comp wall, K=1**: Δ-flat, pd-stratified step (6 / 9 / >12) — a different mechanism (threshold-geometry side, not interference side), consistent with SPIN-32's LOO failure pointing at structure outside {M1..M4}.

The "third wall law in three rounds" is not a coincidence pile anymore: rounds 19–21 carved the comp regime by K, and the K=1/SPIN-32 cell column is where the next model family should be fit. Named next rung: sweep K ∈ {1, 2, 4, 8} at fixed (pd, Δ) to find where the Δ-flat regime hands over to the r^0.25 regime.

Raw: `r21-compwalllaw-output.txt` (canaries: octave replays 2/3/4 PASS, anchors/round-2 replay PASS, mislabeled-arm CAUGHT, adjudication grid 3 pd × 8 r × 2 fam + 20 SPIN-32 cells, 328 s). Round number note: pre-reg committed as round 20 (cde784c), renamed round 21 (228fbc0) after the concurrent wheel lane claimed r20 for the pd-legs sweep — content unchanged.
