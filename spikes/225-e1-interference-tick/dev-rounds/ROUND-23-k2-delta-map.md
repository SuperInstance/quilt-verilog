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

---

## PART 2 — RESULT (run 00:25–00:28 AKDT 2026-09-04; canaries ALL PASS)

**VERDICT: FLAT-ALL.** K=2 walls stay ≤ 4 through Δ=48 in all pd cells — no crossing at
any Δ, not even intermediate growth. The K-line is a **true phase boundary** between the
single-stream world (K=1) and the multi-stream world (K≥2); only K=1 needs a
pd-stratified model. Booked.

### The map (comp arm, calm family, 5 seeds, N∈{2..13}, 4800 ticks)

| Δ | K=2 pd=2 | K=2 pd=3 | F2(Δ/2) ref | K=1 pd=2 ctrl | K=1 pd=3 ctrl |
|---|---|---|---|---|---|
| 8  | 3 | 4 | 4 | 4 | 6 |
| 12 | 3 | 4 | 4 | — | — |
| 16 | 3 | 4 | 4 | 4 | 6 |
| 20 | 3 | 4 | 4 | — | — |
| 24 | 3 | 4 | 4 | — | — |
| 32 | 3 | 4 | 5 | 4 | 6 |
| 48 | 3 | 4 | 6 | — | — |

- **K=2 is not just flat — it is flat in BOTH pd cells simultaneously** (pd=2 → wall 3,
  pd=3 → wall 4, constant across a 6× range of Δ). At Δ=48 F2 predicts 6; measured 3/4.
  The quarter-power F2 is dead at K=2 at every Δ tested. Round 22's surprise sharpens:
  not only is the Δ=12 grid structureless at K≥2, K=2 carries **zero Δ-dependence** in
  the comp wall over Δ ∈ [8,48].
- **pd is the only knob that moves the K=2 wall, and by exactly one seat** (3 vs 4).
  No Δ×pd interaction anywhere in the K=2 grid (7Δ × 2pd, every cell monotone-flat).
- **K=1 controls confirm the other side of the boundary**: pd-stratification appears at
  K=1 (pd=2 → 4, pd=3 → 6, flat in Δ at drift=3) and vanishes at K=2. The two worlds:
  K=1 = pd-stratified, Δ-flat-at-drift=3 (round 21's SPIN-32 seating showed Δ-growth at
  drift=6); K≥2 = everything collapses to a 1-seat pd offset, wall 3–4.

### Canaries (all pass, gate opens the verdict)

- C1 round-21 octave replays (pd=3 calm K=8): walls 2/3/4 **exact PASS**
- C2 round-22 K=2 replays (pd=3, Δ=8/16): 4/4 **exact PASS**
- C3 double-run byte-identity (K=2, pd=3, Δ=48 full cell): **PASS**
- C4 mislabeled-arm self-canary: anchor 68.0/69.6 PASS; sort-as-raw 69.6 vs 68.0 → **CAUGHT**
- (First build attempt had C4 wired to the comp arm by mistake — anchor FAIL, gate
  held, no verdict emitted; fixed to the r20 reference arm. No numbers from the failed
  build entered the verdict.)

### Booking

- **K-line is a phase boundary**: single-stream (K=1) vs multi-stream (K≥2). The
  interference-threshold mechanism story (killed in round 22) stays dead; the successor
  reading is cruder and stronger: with ≥2 concurrent pulse streams the comp wall is
  pinned at 3–4 by stream interference itself, Δ-blind; with exactly one stream the
  wall floats with pd (4→6 at pd 2→3) — pulse-geometry (division granularity) becomes
  load-bearing only when there is no second stream to absorb it.
- **K=1-only pd-stratified model stands** (round-22 conclusion now Δ-resolved to 48).
- Next rung (named): K=1 seating table at drift-matched grid — does the K=1 pd=3 wall
  (6 at drift=3, Δ-flat) re-acquire Δ-growth at drift=6 as round-21 SPIN-32 (6/9/none)
  suggested? If yes, the K=1 model is (pd, drift)-two-knob; if no, drift=6's round-21
  seating was Δ=range artifact.

Raw: `r23-k2deltamap-output.txt` (149 s; 20 grid cells + 5 canary/replay cells).
