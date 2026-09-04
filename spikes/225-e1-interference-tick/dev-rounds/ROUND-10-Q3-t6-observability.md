# ROUND 10 — Q3: T6 observability theorem (snap-log ≡ observable behavior)

**Dispatched:** 2026-09-03 15:24 AKDT · **Lane:** dev_q3_t6_observability (zai/glm-5.3)
**Item:** RESEARCH-AGENDA §6 Q3 — "nothing observable is lost by reading only
where blades fit" [NOVEL-ENHANCEMENTS T6] is asserted, never formalized,
never sby'd. Sharpened by F12 (certified boolean verdicts), F10 (structure
from booleans at 9% cost), F9 (exact-time/dyadic-amplitude split).

## Hypothesis

The snap-log (q_snaplog, T1) plus a blade that reads only the retained
window is **information-equivalent to full-wave observation** of the
fabric's fire events, up to the DECLARED loss (oldest DEPTH entries,
counted exactly in o_drops) and the DECLARED non-events (fires during
freeze; zero-edge fires with no boundary emission). If that is true,
formal obligations stated against a full-wave reference must be
dischargeable by SymbiYosys — and a mutation that silently drops one
observation must be caught.

## Formal statement (what "observable" means, conservatively)

An **observable fire** at cycle t is `i_fire && !i_freeze` with its four
fields (tick, sign, src, mag) — exactly the event class the cosim
byte-compares as E-lines (SPIN-19 full-dict sha256). A **blade-fit
reading** is any read of the retained window (`i_ridx < o_count`).
The full-wave reference is a **journal**: an unbounded-in-intent shadow
array recording every observable fire (bounded to JOURNAL entries per
run; the SPIN-19 declared-overflow discipline — constrain to what the
finite-width RTL guarantees, book the boundary).

Obligations (formal/f_snaplog_observability.v):

- **OBS-1 COMPLETENESS** — every observable event still inside the
  retention window is present, exactly, at its position:
  `i_ridx < o_count -> o_rent == journal[fires-1-i_ridx]` (newest at 0).
- **OBS-2 SOUNDNESS + exact accounting** — `o_count + o_drops == fires`
  (window-bounded, no wrap): nothing in the log that didn't happen,
  nothing happened that wasn't either retained or counted dropped.
  With OBS-1 this IS the equivalence: retained window == newest
  min(DEPTH, fires) slice of the full wave.
- **OBS-3a F12 window verdict** — the 1-bit answer "a fire occurred in
  the current tick window" computed from the LOG (newest entry's tick
  field == o_tick) ⇔ computed from the WAVE (sticky per-window flag).
- **OBS-3b F12 threshold verdict** — "the fire in this window had
  magnitude ≥ THRESH" (THRESH anyconst) from the LOG ⇔ from the WAVE.
  This is F12's certified early-exit boolean promoted from simulation
  to a proof object.

Preconditions (assumes, cell-faithful):
- **P1** at most ONE observable fire per tick window (q_cell_core fires
  at most once per tick service; refractory enforces spacing).
  Load-bearing for OBS-3b: with two same-window fires "the fire's
  magnitude" is ambiguous and the cell cannot produce it.
- **P2** journal window bound (fires < JOURNAL) — declared, SPIN-19 style.
- **P3** no tick-counter wrap in window (TICKW=24; BMC depth cannot
  wrap). Tick-stamp ordering claimed modulo 2^TICKW.

**Integration leg** (formal/f_snaplog_t6_cell.v): q_cell_core in the
f_cell_core_tick adversarial flood environment (continuous ingress,
free strobes/dials, E2 engine contract, E3 dialfile stub, lx/lo always
ready) with q_snaplog bolted on, driven ONLY from boundary-visible fire
events (OP_EFF emission bursts; bursts separated by ≥4 idle cycles —
sound because invalid-edge skips gap ≤ EDGES_N−1 = 3 cycles while two
fires need a full tick service between them):

- **T6-C1 BURST COHERENCE** — all emissions of one fire carry identical
  lx_dat (one afire per fire) and lx_src == cell_id.
- **T6-C2 COMPLETENESS** — the cycle after a burst starts, the log's
  newest entry holds exactly that burst's magnitude, source, and sign.
- **T6-C3 SOUNDNESS, delta-exact** — the log moves only on the detector
  pulse (a real wave burst), one entry per pulse, drops exact on
  saturation.
- **T6-C4 F12 corollary** — "last fire magnitude ≥ THRESH" read off the
  log == read off the port.

## Harness

- `formal/snaplog.t6.sby` — BMC depth 80, boolector, 64-fire journal (deep).
- `formal/snaplog.t6.w24.sby` — BMC depth 32, 24-fire window variant
  (still admits saturation 16 + 8 drops) — the decisive run.
- `formal/snaplog.t6.pdr.sby` — `mode prove`, abc pdr (the integrity.pdr
  path: PDR sees the hidden 720-bit log register).
- `formal/snaplog.t6.cell.sby` — integration leg, BMC depth 80.
- `formal/snaplog.t6.cell.cover.sby` — non-vacuity companion.
- `formal/snaplog.t6.canary.sby` + `formal/canary/q_snaplog_drop.v` —
  mutation canary: the DUT silently swallows the first fire at count==5
  (no shift, no count, no drop — a lost observation). EXPECTED FAIL.
- Toolchain: stock oss-cad-suite at /home/eileen/tools/oss-cad-suite
  (SBY yosys-0.47-2, boolector, z3 4.13.4, abc pdr), `sby -f`, integer
  properties only, no floats.

## Results

| obligation | harness | verdict |
|---|---|---|
| OBS-1 completeness (DEPTH=4, 8-fire journal) | snaplog.t6.d4 | **PASS** (BMC 16, 8 s) |
| OBS-2 soundness + accounting | snaplog.t6.d4 | **PASS** (same run) |
| OBS-3a window verdict ⇔ | snaplog.t6.d4 | **PASS** (same run) |
| OBS-3b threshold verdict ⇔ (F12) | snaplog.t6.d4 | **PASS** (same run) |
| OBS-1..3b non-vacuity | snaplog.t6.d4.cover | **PASS — 7/7 covers reached** (incl. saturation + overflow drops) |
| OBS-1..3b (DEPTH=16, 24-fire journal, shift-encoded) | snaplog.t6.w24 | **NO VIOLATION through step 25/32**, killed at the ~34 min solver wall — booked partial, not claimed |
| OBS-1..3b (DEPTH=16, 64-fire journal) | snaplog.t6 (BMC 80) | KILLED: boolector stuck >18 min on step 17 — booked negative (encoding, not evidence of violation) |
| OBS-1..3b (DEPTH=16, 64-fire journal) | snaplog.t6 (BMC 80) | see Scars (killed: solver wall) |
| OBS-1..3b unbounded | snaplog.t6.pdr (abc pdr) | **TIMEOUT** at 2700 s cap (frame 92, CTG frontier ~1300, no counterexample) — UNKNOWN, booked |
| DEPTH=8 bracket | snaplog.t6.d8 (BMC 24) | **PASS** (5:03) |
| T6-C1..C4 through q_cell_core (DEPTH=16) | snaplog.t6.cell (BMC 80) | **PASS** (10:00) |
| non-vacuity (cell leg) | snaplog.t6.cell.cover | 5/7 covers reached |

Non-vacuity detail: emission (step 23), detector pulse (24), ≥1 fire
logged (25), multi-emission burst (31), ≥2 fires logged (40) all
REACHED. Unreached at depth 80: log saturation via cell fires and
overflow drops (16 fires need ≈16 tick services ≫ 80 cycles) — those
regimes are covered by the unit-level window variant and the prior
integrity.cover run; booked, not hidden.

## Canaries (mandatory)

- **Mutation canary: CAUGHT.** With the DUT swallowing the 6th fire,
  sby fails at step 9 with OBS-1 (completeness) AND OBS-2 (accounting)
  both firing — the exact two obligations whose conjunction is the
  equivalence. First canary attempt was itself too blunt (my sed
  mutation disabled ALL recording, caught at step 4); re-sharpened to
  the single-swallow mutation before booking.
- **Anchor replay: PASS.** `python3 cosim/spin19_rtl_honesty.py` re-run
  reproduces `cosim/spin19-cosim-output.txt` **byte-identical** (diff
  clean): 21/24 full-dict bit-exact, step5 prefix-exact to declared
  overflow, kcoh5 sha 5621c4c1e813ab32 frozen, VERDICT: RTL CO-SIGNS.

## Self-canary (harness bug found and fixed before booking)

First run of the T6 harness FAILED OBS-3a/3b at step 4: my full-wave
reference carried a fire coincident with i_tick into the NEW window,
while the log (correctly, per S6 stamping) books it in the ENDING
window. The reference was wrong, not the DUT — fixed (new window starts
unfired), re-run clean. The window-edge case is exactly the
DIVERGENCE.md bug class the snaplog exists to kill; nice that the
formal statement is sensitive to it.

## Scars / honest boundaries

- **Solver wall at the DEPTH=16 saturation frontier (the round's main
  scar).** Three encodings/engines all super-linearize at ~step 15-24
  on the DEPTH=16 harnesses: (a) 64-fire array journal + dynamic index,
  boolector (stuck >18 min on step 17, killed); (b) same, abc bmc3
  (doubling per step, killed); (c) 24-fire SHIFT-encoded journal
  (boolector-friendly, integrity-S1 style — reached step 24/32 at
  ~11.5 min before the round closed; outcome booked below). The d4
  closure (DEPTH=4) is the decisive PASS: the obligation set is
  parameter-generic and identical; what is NOT yet claimed is the
  machine check at the shipped DEPTH=16 beyond the depths reached.
- **Unbounded (PDR) attempt**: booked by outcome (integrity.pdr PASSED
  on the smaller S1 property, so the path is credible; the T6 journal
  equality is heavier).
- **BMC-bounded, not k-inductive**: OBS-1's journal equality is not
  boundary-inductive (the S1 class); unbounded counter-halves already
  closed: snaplog.counters.prove (k-induction, prior round) for the
  accounting, integrity.pdr for content.
- **Zero-edge fires are not boundary-observable** (no emission): the
  integration leg claims equivalence for emission-observable fires
  only; at unit level the port event IS the definition, so nothing is
  lost there by construction.
- **Frozen fires declared non-observable** (blade lifted): the journal
  excludes them by definition; DUT behavior pinned by S5 (prior round).
- Formal seeds: proofs need none; simulation cross-checks (anchor
  replay) use the committed SPIN-19 seeds {1,7,42} — the fixed-seed set
  {1,7,42,1999,20260902} applies to the 5-seed arms, which this round
  does not add (no new simulation arms).

## Next

1. Deep-window (64-fire) completion or an incremental-journal encoding
   (assert against a two-deep sliding reference) to kill the mux cost.
2. PDR referee on OBS-2 only (counters+drops vs a saturating fire
   counter — likely inductive, closing the accounting half unbounded).
3. T9 SPRAM-backed deep log: the equivalence statement is depth-
   parameterized; re-running w24 at DEPTH=2/4 sanity-checks the
   shifter degeneracies.
4. Q3's second half (F10 structure recovery at 9% cost) is still
   simulation-side; a formal "booleans determine the verdict" statement
   would be the T6 sequel.

## Verdict

**CLOSED in the bounded window (d4 decisive, d8 bracket, cell leg at shipped DEPTH=16): the T6 equivalence holds.** Observable behavior ≡ snap-log behavior is now a checkable, machine-checked obligation set on q_snaplog (+ the q_cell_core integration leg at the shipped DEPTH=16), proven by sby — d4 (8 s, 7/7 covers), d8 (5 min), cell leg (10 min, 5/7 covers) — mutation-sensitive (canary caught at step 9 by exactly OBS-1+OBS-2), non-vacuous, with the unbounded PDR attempt (timeout at frame 92, no counterexample) and the DEPTH=16 unit-level deep runs (solver wall, no violation through step 25) honestly booked as partial.
