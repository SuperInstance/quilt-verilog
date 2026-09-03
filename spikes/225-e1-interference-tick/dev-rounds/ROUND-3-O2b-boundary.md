# DEV ROUND 3 — O2b: the contention boundary is at N=6 (and lag-amp is a dial)

Date: 2026-09-03 (AKDT). Branch `g3-kinduction`. Item: IDEATOR nudge on round 2
(9491c25) — "you have data at ≤5 and at 8; the interesting number is 6 or 7."
Harness: `o2_boundary.py` (this directory) — round-2 method verbatim, N ∈ {6,7}
only. Seeds (1, 7, 42, 1999, 20260902), 4800 ticks, ~2 min CPU.
Latency sets (twin 0 live, spread 0..12 interpolated): N=6 (0,2,5,7,10,12);
N=7 (0,2,4,6,8,10,12). Lag blade: **28/28 exact** (round 2: 22/22 — no drift).

## Decision-table deltas (mag C=1 − admit-all, pp)

| regime | arm | N=2 | N=3 | N=5 | **N=6** | **N=7** | N=8 |
|---|---|---|---|---|---|---|---|
| stress | raw  | +0.0 | +0.1 | +1.6 | **+4.5** | +6.8 | +11.9 |
| stress | comp | +0.4 | +3.3 | +24.1 | **+25.0** | **+37.6** | +56.2 |
| calm   | raw  | −0.1 | +0.0 | −0.3 | −0.1 | +0.8 | +2.3 |
| calm   | comp | +12.5 | +10.3 | +13.9 | +22.3 | +39.6 | +52.6 |

(N≤5 columns = round 2; N∈{6,7} = this round, same seeds/gates.)

## Verdict

1. **The raw win's wall is at N=6.** The ≥2pp promotion gate is first cleared
   exactly there: +1.6 (N=5) → **+4.5 (N=6)**, then +6.8, +11.9. The round-2
   "N≥~5" note resolves to a located threshold: **the wall is at N=6.**
   ROUNDS ledger line: "the wall is at N=6."
2. **The comp-arm amplification is itself fan-out-shaped, and its knee is N=7→8.**
   Stress comp deltas: 24.1 → 25.0 → 37.6 → 56.2. Flat 5→6, then +12.6pp,
   then +18.6pp. So there are TWO thresholds, not one: admission control
   switches on at N=6 (raw), and compensation *superlinearly* amplifies it
   from N=7. Mechanism per round 2 §2: compensation synchronizes twins onto
   the same fresh error; at high N the synchronized pulse mass grows with N
   while the C=1 budget stays fixed — pressure ∝ N, relief ∝ 1.
3. **Naive compensation keeps degrading monotonically:** comp admit-all calm
   62.0 (N=6) → 44.7 (N=7) → 31.7 (N=8); stress 73.9 → 61.3 → 42.7. The
   "compensator depends on the controller" claim now has a full curve.
4. **C=1 invariance holds at the new N** (84.3 calm / 98.9 stress, identical
   to every other N — N-invariant by construction). Built-in determinism
   check passed at both new points.

## Booking

- T2 RTL note sharpened: q_tick_sched sort is slack for N≤5, load-bearing
  from **N=6**; budget = 1 is the N-invariant anchor. The C dial is the
  control surface; O4's closed loop should drive it from observed contention.
- The lag-amp curve (+24.1 → +56.2, knee at 7→8) is booked as the measured
  response curve of a **synthetic room-pressure generator** — see
  `O2-ROOM-PRESSURE-MAPPING.md` for the cross-repo mapping (elephant dials /
  zeroclaw field machinery / fc1b seeded-arm timing).

## Scars

- None this round: lag blade exact on both new sets, reproduction gate
  inherited from round 2 (identical seeds ⇒ N≤5 columns byte-reproducible),
  C=1 invariance check passed twice.
