# ROUND 25 — K=1 pd-ladder on the extended N grid (pre-registered 4ead455, IDEATOR nudge): the ceiling hid a real wall at 13, and the ladder books as 2pd for pd≤3, 2pd+1 for pd≥4

**Verdict: G-2PD fires its second branch — the exact-2pd boundary law dies cleanly — but IDEATOR's core instinct was confirmed: the pd=6 leg of rounds 21/24 was truncated, not wall-less. On N ≤ 18 the pd=6 wall exists at 13, one seat past the old ceiling.** Grid inconsistency check passed: pd=2 re-reads 4 on the extended grid.

## The measured ladder (K=1, drift 6, Δ=12, N 2..18)

| pd | wall | 2pd | off |
|---|---|---|---|
| 2 | 4 | 4 | 0 |
| 3 | 6 | 6 | 0 |
| 4 | 9 | 8 | +1 |
| 5 | 11 | 10 | +1 |
| 6 | 13 | 12 | +1 |

Canaries: pd=3 → 6 exact, pd=4 → 9 exact (round-21 seats reproduce on the bigger grid), K=8 octave 2/3/4 exact.

## Booked reading

The ladder is a **single-step law: wall = 2pd for pd ≤ 3, wall = 2pd + 1 for pd ≥ 4**. Not "exact at the ends, sagging in the middle" (IDEATOR's shape) — the +1 starts exactly after pd=3 and holds to the ladder's top. Two structural observations booked with it:

1. **Parity flips with the step**: pd ≤ 3 walls are even (2pd), pd ≥ 4 walls are odd (2pd+1). Any mechanism for the wall seat must explain why one extra candidate seat is needed exactly when pd crosses 3 — and why that seat carries odd parity.
2. **The step sits at the same pd where the θ-band empties** (round-21 booked: for pd ≥ 4 with N=7 twins the (1−1/pd, 1+1/pd] band has no in-range twin count). Coincidence for now; flagged as the first place to look.

Round 16's echo-law-boundary claim stays dead as an exact law but is **half-resurrected as a low-pd limit**: the wall touches the safe boundary exactly where pd ≤ 3. The named drift × pd sweep should run its grid to N ≥ 14 — there are seats past the old ceiling, and pd=6's wall is now known to live at 13.

Raw: `r25-pdladder-output.txt` (130 s).
