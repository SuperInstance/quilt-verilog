# DEV ROUND 19b — bounded-fabric arrival-rate absorbers under the PW-invariance gate

Date: 2026-09-03 (AKDT). Branch `g3-kinduction`. Pre-registration: `wheel/round19b-prereg.md`
(commit fb28de2, BEFORE any run; one display-side harness fix eab0f90 after a first-attempt
crash — see Integrity). Harness: `wheel/round19b_arrival_fabric.py` (run_sw clone verbatim,
arms swap only the admission gate). Output: `wheel/round19b-output.txt` (run 1; run 2 kept
on disk for C1). Requeue lane: original round-19 arrival-rate sweep completed as 4cbfd83.

## VERDICT (up front)

**STRONG-YES — three bounded-fabric mechanisms (queue cell, credit fence, staged grant)
absorb arrival-rate pressure at fan-out 64 WITHOUT breaking bit-exact replay at any
PW 41..48, with no floats, no wall-clock, no net in the loop; the integral-servo crutch
(the booked negative control) breaks PW-invariance deterministically.** The dispatch
question is answered YES in its strong form: rate-class absorption does not require
unbounded or PW-unsafe state — an 8-slot FIFO, a 3-bit credit fence, or two fixed seats
suffice. The motivating C-lift flip (H1) did not reproduce in its pre-registered band;
the phenomenon is present in amplified form (admit-all itself collapses at fan-out ≥13;
the "lift" is +92..99pp, not +24pp) — no kill fired, bands judged as pre-registered.

## Canaries (all PASS — verdicts booked)

- **C1 byte-identity double-run: PASS** — two full runs, elapsed lines stripped, byte-identical.
- **C2a anchor replay: PASS** — N=5 stress default raw: admit-all %w=68.0, mag1 %w=69.6
  (round-2 published, exact). Wall replay: default-delta mean win crosses +2.0 at N=6
  (+2.2; after 5: +0.7) → **default wall = exactly 6** (round-17/19 anchor). Wall profile
  N∈{2..13}: −0.1, +0.1, +0.4, +0.7, +2.2, +3.8, +7.0, +35.2 … (round-19 shape).
- **C2b (harness self-check): PASS** — per-seed counter equality vs `glm3_experiments.run_sw`
  verbatim (admit + mag1, seeds 1/7/42, all counters incl. fires).
- **C2d: PASS** — PW=48 wrapped fabric ≡ unbounded at the anchor cell (same counters).
- **C3 mislabeled-arm self-canary: CAUGHT** (mag1 as "admit" gives 69.6 ≠ 68.0).
- **C4 trace-hash PW identity: PASS for qcell/cfence/sgrant/admit/mag1 (1 unique hash
  across PW 41..48); BREAK for crutch (8 unique) — that break IS the H2 result.**

## Bands

- **H1 (gap reproduces): NOT CONFIRMED — no kill either.** Pre-registered band: C-lift
  ≤10pp at N∈{13,21} AND ≥24pp at N=64. Measured at κ=8: calm +46.7/+96.5/+99.2,
  stress +95.4/+96.8/+97.5 (N13/N21/N64). The lift is already maximal at N=13 — the
  6→24pp flip shape does not seat. Kill conditions (lift64 < 12pp, or flat) also fail.
  Booked reading: on this fabric the arrival-κ≈8 regime is past the admit-all runaway
  knee at ALL tested fan-outs ≥13 — the motivating phenomenon arrives amplified
  (admit collapses to 0.5–2.6%w; mag1/mechanisms hold 96.6–100%w), not as a graded flip.
- **H2 (crutch breaks PW-invariance): CONFIRMED, both routes.** (a) Empirical: 8 unique
  trace hashes across PW∈{41..48} at (stress, κ=8, N=64, seed 1); PW41≠PW48 on **all 5
  seeds**. (b) Theorem-tier: maxstate ≥ 2^40 in every cell (integral accumulator I
  diverges as I ← I + len(cands) + I>>4; measured ~2^406 at N=2 up to ~2^20000 at N=64 —
  the booked "rate-control crutch" class fails the gate exactly as pre-registered,
  symmetric expectation honored).
- **H3 (mechanism promotion): 3/3 PROMOTED → STRONG-YES.**
  - **qcell** (8-slot FIFO, 1 seat): (i) PW-INVARIANT, maxstate 580 (≪2^40); (ii) κ=8 N=64
    gain vs admit +97.5pp (stress) / +99.2pp (calm); (iii) κ=2 N∈{2,5} tax −0.1pp;
    (iv) canaries pass.
  - **cfence** (3-bit credits, ≤2 seats/tick): (i) PW-INVARIANT, maxstate 601; (ii) +96.2pp;
    (iii) −0.2pp; (iv) pass.
  - **sgrant** (2 fixed seats, anti-starvation + max-err): (i) PW-INVARIANT, maxstate 595;
    (ii) +96.2pp; (iii) −0.0pp; (iv) pass.

## Key numbers (5-seed mean %w)

C-lift (mag1−admit):

| family | κ=2 | κ=8 | κ=16 | (N=2,5,13,21,34,64) |
|---|---|---|---|---|
| calm   | +0.1/−0.4/**+91.0**/+92.2/+92.5/+92.5 | +0.0/+0.0/**+46.7/+96.5/+95.6/+99.2** | +0.0/+0.0/**+6.7/+91.5/+98.0/+98.3** | |
| stress | −0.1/+1.4/**+13.2**/+13.2/+13.2/+13.2 | +0.0/+0.3/**+95.4/+96.8/+97.0/+97.5** | +0.0/+0.0/**+92.9/+97.8/+97.4/+97.5** | |

Cell view at κ=8, N=64: admit 0.8/0.5 (calm/stress; runaway, maxstate ~2^20500) vs
mag1 100/98, qcell 100/98, cfence 99.8/96.7, sgrant 99.9/96.6 — all with maxstate ≤ 601
(≈10 bits). At κ=2 low fan-out (N∈{2,5}) every mechanism is within −0.4..+1.4pp of
admit-all (no tax). Crutch: %w up to 98.8 at low fan-out but maxstate ≥2^40 everywhere
(the servo works AND is PW-unsafe — exactly the crutch class).

## Structural constraints (b)/(c) — verified

Static scan of the fabric source: no float literals in the tick loop (percentages only at
print), no time calls in the fabric path (elapsed lines only in leg footers), no net in the
loop (mechanism state = local ids / credits / last_fire / FIFO). Determinism: C1 double-run
byte-identical.

## Integrity / disclosures

1. **sgrant seat-A ambiguity (disclosed in-run too):** prereg names "least-recently-fired
   candidate … anti-starvation" but its parenthetical says "(max last_fire)". run_sw's fair
   key (ascending last_fire) and the anti-starvation purpose require MIN last_fire;
   implemented min(last_fire), tie min id. Sign slip in the prereg parenthetical, not a
   re-derivation.
2. **First-attempt crash (archived: `round19b-output.attempt1-crash.txt`):** L0 canaries
   ALL PASS, then the L1 print hit Python's 4300-digit int→str limit on runaway admit-arm
   maxstate. Fix eab0f90: compact `~2^bits` display for maxstate ≥ 2^60 — display-side
   only, no fabric semantics touched (SPIN-32 precedent); raw ints used for all gates.
3. Budget guard did not fire (κ=2 leg 183 s, projection 426 s ≪ 1320 s cap). Full run 403 s.
4. Wall-profile note: the wall-replay canary reproduces round-19's shape only through N=8
   (+7.0); N≥9 jumps to +35 (round-19's own table shows the same jump at high fan-out —
   the runaway knee sits inside N∈{8..9} on the default cells too).

## Booking

- The round-2/19 dichotomy sharpens: **arrival-rate pressure at high fan-out is a runaway
  instability of the admit-all arm; every bounded rate-limiter (and the priority sort)
  quenches it. What separates mechanisms is not absorption (all absorb) but the PW gate —
  and bounded-state limiters pass it by construction-sized margins (maxstate ≤ 601 ≈ 10
  bits vs the 2^40 theorem bound).**
- The crutch result upgrades the dispatch's booking from expectation to measurement:
  integral rate servos are not merely suspected PW-unsafe — they break PW 41..48 on every
  seed AND blow the state bound by thousands of bits. Rate control must be state-bounded
  (fence/queue/stage), never integral.
- Next spoke (booked for whoever takes it): do qcell/cfence/sgrant stay promoted at
  κ=16 (mechanisms were only run at κ∈{2,8}; the κ=16 C-lift suggests the pressure
  persists — cfence/qcell behavior there is unmeasured) and at K∈{2,16}
  (pulse-lifetime coupling)? And does the comp-arm collapse (round 19
  post-hoc) survive WITH a mechanism in the loop — i.e., is lag compensation still
  additive under bounded rate control?
