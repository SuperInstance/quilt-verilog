# DEV ROUND 19 — O2d: arrival-rate (delta/K) wall sweep at fixed pd

Date: 2026-09-03 (AKDT). Branch `g3-kinduction`. Pre-registration commit precedes all
comparison numbers. Harness: `r19_arrivalwall.py` (extends round-17 `o2c_pdwallsweep.py`,
which reuses round-2 `o2_contention.py` / glm-3 `run_sw` + `run_sw_comp` verbatim).
Output: `r19-arrivalwall-output.txt`. Working files prefixed `r19_`.

## PART 1 — Pre-registration (written BEFORE any comparison numbers)

### Hypothesis (booked verbatim from round 17, ef6e2b5)

"The wall tracks candidate arrival rate (delta/K) — sweep that at fixed pd next."
If true, wall position vs arrival rate collapses onto one curve across parameter
families; if false, the wall is genuinely fan-out-structural (N-driven, arrival-rate
insensitive).

### Grid (fixed pd=3 via pulse_div; round-17/round-3 comparability)

- Two families (drift and K held fixed per family, delta swept ⇒ arrival-rate knob
  is the threshold, per the booked hypothesis variable delta/K):
  - **calm-family**: K=8, drift=3, delta ∈ {2,4,6,12,24,48} → r = delta/K ∈ {0.25, 0.5, 0.75, 1.5, 3, 6}
  - **stress-family**: K=4, drift=6, delta ∈ {2,4,8,12,24,48} → r = delta/K ∈ {0.5, 1, 2, 3, 6, 12}
  - Combined r span 0.25 → 12 ≈ 1.7 decades (≥ 1 decade required).
  - Families overlap at r ∈ {0.5, 3, 6} — the cross-family collapse seats.
  - delta=6/K=8 and delta=12/K=4 are the round-2/3/17 default cells (anchors).
- N ∈ {2..13}, latency sets canonical at N∈{2,3,5,8}, interpolated spread 0..12 elsewhere
  (round-17 convention, verbatim).
- Arms: raw (admit-all vs mag+C=1, round-2/3 metric verbatim) AND lag-compensated
  (first-difference integer cross-correlation blade, window 480, maxlag 15, per-twin
  lag shift — round-2 `run_sw_comp`, verbatim). Primary wall = RAW arm (comparable to
  round-3/17 anchors); comp wall reported alongside.
- Seeds (1, 7, 42, 1999, 20260902), 4800 ticks, integer-only inside loops;
  percentages once at print time (round-2/17 convention).

### Wall definition (unchanged, round-3 gate)

Wall(family, r) = smallest N ∈ {2..13} whose mag+C=1 win over admit-all (mean %w over
5 seeds, raw arm) is ≥ +2.0pp. Same for the comp arm separately.

### Decision rule (pre-registered, decided BEFORE the run)

- CONTROL: the default cells (calm delta=6, stress delta=12, pd=3) must reproduce the
  round-17/round-3 wall at exactly N=6, and the N=5 stress raw anchor cells must
  reproduce round-2's published %w (admit-all 68.0, mag+C=1 69.6, ±0.05). Control
  failure ⇒ harness non-comparable, no verdict booked.
- **PROMOTE arrival-rate law** if ALL of:
  (a) wall(r) at pd=3 is non-flat: max−min ≥ 2 seats across the r decade (the wall
      genuinely moves with arrival rate);
  (b) cross-family collapse: at overlapping r ∈ {0.5, 3, 6}, calm-family and
      stress-family walls agree within ±1 seat;
  (c) out-of-sample anchors: round-17's pd=2 (wall 5) and pd=6 (wall 7) walls —
      which sit at the SAME default r as pd=3 — each fall within ±1 seat of the
      pd=3 default-r wall measured here.
- **BOOK fan-out structural** if (a) fails (wall flat across ≥1 decade of r) — the
  wall does not track candidate arrival rate; it is N-structural.
- **PARTIAL** otherwise (e.g. wall moves with r but families disagree ⇒ delta-vs-K
  confound, or anchors miss): report the (family, r, wall) table honestly and book
  the surviving reading, labeled post-hoc as such.

### Canaries (all must pass before any verdict is booked)

1. **Byte-identity double-run**: two full runs, outputs stripped of elapsed-time
   tokens must be byte-identical.
2. **Anchor replay**: round-2 N=5 stress raw numbers (%w 68.0 / 69.6) and round-17
   pd=3 wall = 6, exact (within the printed precision).
3. **Mislabeled-arm self-canary**: a deliberately mislabeled arm (mag+C=1 run
   relabeled "admit-all") must be CAUGHT by the anchor gate (69.6 ≠ 68.0).

## PART 2 — Results

(to be filled after the run)

## PART 3 — Verdict

(to be filled after the run)
