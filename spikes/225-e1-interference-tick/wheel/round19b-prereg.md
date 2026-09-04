# DEV ROUND 19b — arrival-rate vs fan-out: bounded-fabric absorbers under the PW-invariance gate

Requeue lane (prior round-19 lane died at provider; original arrival-rate sweep completed and
committed as 4cbfd83 / ROUND-19-arrival-rate-wall.md). This round consumes that verdict:
raw wall = fan-out-structural, comp wall = delta/K arrival-rate law. Branch `g3-kinduction`.
Deliverables: this prereg + `round19b_arrival_fabric.py` (committed BEFORE any run),
then `round19b-output.txt` + `ROUND-19b-results.md` (verdict commit).
Ledger note: dev-rounds/ROUNDS.md and wheel/WHEEL-LOG.md carry live uncommitted edits from
other lanes — left untouched; backfill of this round's entry is pending on the bridge.

## The question (verbatim from dispatch)

"Is there a bounded-fabric mechanism (queue cell? credit fence? staged grant?) that absorbs
arrival-rate pressure WITHOUT (a) breaking bit-exact replay at any PW, (b) using floats or
wall-clock, (c) violating determinism (no net in the loop)?"

Booked gap being probed: "cells at fan-out 64 flip the arrival-geometric C-lift (6→24+ pp at
arrival κ≈8); rate-control crutches break PW-invariance; trace-hash invariance is the hard
gate (SPIN-34: PW 41..48 identical)."

## PART 1 — Models (fixed before any run)

### Fabric

`run_sw` semantics from glm3_experiments.py (round-2/19 fabric, cloned verbatim statement
order so anchors replay bit-exact): N-twin channel, twin i reads `e1.reality(max(0,t-lats[i]))`,
g drifts ±drift per tick (LCG(seed)), candidates = |s−g| > delta, admission limited by the
mechanism, each admitted twin emits pulse (mass |e|//pd sign-corrected, lifetime K), pulses
halve per tick (life−1), g += net(pulse masses), settle tick iff ALL reads within delta.
%w = 100·settles/ticks (printed at 1 decimal, round-2 convention). pd=3 (round-17/19 pin).

Families (round-19 verbatim): calm {K=8, drift=3}, stress {K=4, drift=6}.
Arrival knob κ = delta/K (round-19's booked arrival-rate variable): κ ∈ {2, 8, 16}
→ calm deltas {16, 64, 128}, stress deltas {8, 32, 64}.
Fan-out N ∈ {2, 5, 13, 21, 34, 64}; lats = round-17/19 interpolation
(round(i·12/(N−1)); N∈{2,5} canonical, N=13..64 interpolated).
Seeds (1, 7, 42, 1999, 20260902), 4800 ticks, integer-only in the tick loop.

### Arms (6)

1. **admit** — admit-all (C=N). Baseline; round-2 control.
2. **mag1** — mag+C=1: sort (−err_abs, id), admit top-1 (round-2/19 T2 sort). The proven
   priority absorber; reference, not a candidate answer (it is priority-class, not rate-class).
3. **qcell** (queue cell) — global FIFO of deferred twin ids, capacity 8. Per tick:
   purge queued ids that are not candidates this tick (oldest-first scan); seat budget 1 goes
   first to the oldest still-queued candidate; if no queued candidate holds, the mag-top fresh
   candidate takes the seat; all unadmitted fresh candidates append id to FIFO while room
   remains (FIFO full → candidate dropped, not queued). Bounded state: ≤8 ids ≤ 63.
4. **cfence** (credit fence) — integer credits c ∈ [0, 8], init 0; +1 per tick (saturate at 8)
   BEFORE admission; admit mag-sorted while c>0 and admitted<2, each admission spends 1.
   Steady 1/tick rate, burst 8. Bounded state: 3 bits.
5. **sgrant** (staged grant) — 2 seats/tick, fixed stages: seat-A to the least-recently-fired
   candidate (max last_fire, tie min id), seat-B to max err_abs of the remainder (tie min id).
   Anti-starvation absorber. State: last_fire ticks (≤ 4800).
6. **crutch** (integral rate servo — the booked negative control) — integer accumulator
   I (fabric-wrapped): I ← I + len(cands) + (I >> 4) each tick; grant ceiling
   G = 1 + clamp(I >> 8, 0, N); admit mag-sorted top-G. Textbook aggressive integral action:
   unbounded-amplifying state, i.e. the "rate-control crutch" class the dispatch says breaks
   PW-invariance. Pre-registered expectation: FAILS the PW gate. If it passes, that booking is
   falsified — stated symmetric, decided by the run.

### Metric numbers vs PW semantics (two separate legs, kept separate on purpose)

- **Metric leg** (C-lift, gains, walls): UNBOUNDED Python fabric — round-2/19 convention,
  anchor-comparable. C-lift(N, κ) := %w(mag1) − %w(admit), 5-seed mean, per family.
- **PW leg** (the hard gate): the same fabric with every state variable two's-complement
  wrapped at PW bits (g, pulse masses, debt, I; SPIN-19/34 semantics), canonical trace =
  sha256 over JSON {events, debt, rejected, maxerr, fires, per-tick admitted-count list,
  settle-bit string}. PW-invariance for an arm×cell = all hashes at PW ∈ {41..48} identical.
  Two-tier test:
  (T1, theorem tier) maxstate := max |any wrapped state| over the run, tracked on every
      metric-leg run. If maxstate < 2^40 (signed-41 range), PW∈{41..48} replay is provably
      identical (two's-complement wrap cannot diverge inside the width).
  (T2, empirical tier) full 8-width hash sweep on the worst cell per mechanism arm
      (stress, κ=8, N=64, seed 1) + PW∈{41,48} all 5 seeds + admit/mag1 at the round-2
      anchor cell: hash sets must collapse to exactly 1.

## PART 2 — Decision rule (kill bands, fixed before any run)

Canaries (all must pass before any verdict; a failed canary voids the run):
- C1 byte-identity double-run (shell: two full runs, diff after stripping elapsed-time lines).
- C2 anchor replay: stress default (delta=12, N=5, raw) admit %w=68.0, mag1 %w=69.6 exactly
  (round-2 published); round-19 default wall = exactly 6 (default-delta cells, wall gate
  reproduced on the cloned fabric at N∈{2..13}); PW=48 wrapped fabric ≡ unbounded fabric at
  the anchor cell (same counters).
- C3 mislabeled-arm self-canary: mag1 relabeled "admit" must be CAUGHT by the 68.0/69.6 gate.
- C4 trace-hash PW 41..48 identity legs per PART 1 (reported per arm; counts toward band (i)).

H1 — the gap reproduces (C-lift flip at fan-out 64): CONFIRMED if at κ=8,
  mean C-lift at N∈{13,21} ≤ 10.0pp AND at N=64 ≥ 24.0pp in ≥1 family (and ≥ +12pp over its
  own N=21 value). Kill: lift(64) < 12pp or monotone-flat → NEGATIVE-on-gap (mechanism bands
  still judged, but the motivating phenomenon is booked absent on this fabric).

H2 — crutch breaks PW-invariance: CONFIRMED if the crutch shows hash-set >1 across
  PW∈{41..48} at ≥1 (stress, κ=8, N=64) seed OR maxstate ≥ 2^40 in any of its cells.
  If the crutch stays single-hash with maxstate < 2^40, book "crutch PW-safe here" — the
  dispatch's negative-control claim fails to reproduce and the round says so.

H3 — the main question. A mechanism (qcell / cfence / sgrant) is PROMOTED iff ALL:
  (i) PW gate: hash-set = 1 on every T2 leg cell AND maxstate < 2^40 in every one of its
      metric-leg cells;
  (ii) absorbs arrival-rate pressure: at κ=8, N=64, %w gain vs admit ≥ +6.0pp (5-seed mean)
      in BOTH families;
  (iii) no low-pressure tax: at κ=2, N∈{2,5}, %w within −2.0pp of admit (both families);
  (iv) C1–C4 pass.
  Verdict ladder: 3 promoted → STRONG-YES; 1–2 → YES (named); 0 → NEGATIVE (no bounded-fabric
  rate absorber in this family; arrival-rate pressure is structural in the raw arm — only
  priority sort and/or lag compensation governs it, per round 2/19).

Structural constraints (b)/(c) are gates by construction, verified: no float ops in the tick
loop (percentages only at print), no wall-clock in the fabric path (elapsed only in the
footer), no net in the loop (mechanism state is local fabric state: ids, credits, last_fire,
queue — no external channel, no cross-run state), determinism = C1 double-run.

Budget guard (pre-registered): if after the κ=2 leg the projection for the full grid
exceeds 22 min wall, drop N=34 from the mechanism κ=2 rows (labeled in output). 30-min cap.

## Run plan

python3 -u round19b_arrival_fabric.py > round19b-output.txt  (from wheel/)

Legs: (L0) canaries C2/C3 + round-19 wall replay; (L1) metric grid — arms {admit, mag1} ×
κ∈{2,8,16}, {qcell, cfence, sgrant, crutch} × κ∈{2,8}, all × families × N × seeds, with
maxstate tracking; (L2) PW hash legs T2; (L3) C-lift table + band evaluation printed at the
end. Wall definition for the wall-replay canary only (round-3 gate): smallest N with
mag1−admit ≥ +2.0pp.
