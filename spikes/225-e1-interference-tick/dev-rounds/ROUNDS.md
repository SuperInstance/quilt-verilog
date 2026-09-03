# dev-rounds — ROUNDS ledger (branch g3-kinduction)

Format per block: round #, item, verdict, commit hash, headline number.
Ordered queue: RESEARCH-AGENDA §4 O1–O7, then §Q open questions, then wheel spokes round-robin.

- 2026-09-02 23:00 AKDT — round counter initialized. Next: O1 (K=2/3 champion replay). Wheel lanes dequant-2 + k-replay completed 22:28–22:40 (see wheel/WHEEL-LOG.md); no dev item in flight.

## Round 1 — O1 K=2/3 champion replay — 2026-09-02 23:0x AKDT
- **Item:** O1 (arena schema widened to K∈{1..8} + static grid probes)
- **Verdict:** CONFIRMED — new champion banked
- **Commit:** fb63ff4
- **Headline:** new champion K=1/pd=2/d16 interference 96.1% (triple-axis Pareto domination of old 93.2% champion); calm Δ=6 re-keyed (98.0 vs 56.6); grid-anchoring arena bias booked.

## Round 2 — O2 contention boundary — 2026-09-02 23:5x AKDT
- **Item:** O2 (contention controller boundary; F14 mag+C=1 vs admit-all, raw vs lag-compensated)
- **Verdict:** REFUTED-as-booked / PARTIAL-CONFIRM — win is fan-out-gated (slack at N≤5 raw: +0.0/+1.6pp; clears gate at N=8 raw: +11.9pp stress) and does NOT vanish under lag compensation — it explodes (+24.1pp at N=5, +56.2pp at N=8). "Contention is a lag symptom" false; inverse true: compensator synchronizes twins and *needs* the sort (comp admit-all at N=8 is −15.1pp vs raw). T2 promoted to RTL with N≥~5 boundary note; not demoted.
- **Commit:** 9491c25
- **Headline:** mag C=1 vs admit-all, stress raw: +11.9pp at N=8 (57.8→69.7 %w, maxE 99.2→48.0); compensated: +56.2pp at N=8 (42.7→98.9).

## Round 3 — O2b boundary probe — 2026-09-03 ~00:3x AKDT
- **Item:** IDEATOR nudge on round 2 — sample N∈{6,7}, locate the transition
- **Verdict:** CONFIRMED-SHARPENED — the wall is at **N=6** (raw +4.5pp, first ≥2pp clearance; N=5 was +1.6). Comp-arm amplification has its own knee at 7→8 (+25.0 → +37.6 → +56.2). Lag blade 28/28 exact.
- **Commit:** (this commit)
- **Headline:** "the wall is at N=6" — T2 RTL boundary note resolved to a located threshold; lag-amp curve booked as the measured response of a synthetic room-pressure generator (O2-ROOM-PRESSURE-MAPPING.md).

## Round 3b — O3 quanta floor — 2026-09-03 ~11:4x AKDT
- **Item:** O3 (cap × K × regime × 5 seeds; Z₃ sign-only arm; F23 anchor replay)
- **Verdict:** PARTIAL-REFUTE / KNEE RELOCATED — ±5 fails the ≥99% gate at K=2 stress (97.5%); adopt **±7 (4-bit)** as ESP32/.qm default (≥99.2% retention in all 8 K×regime cells). Z₃ debt inversion persists 8/8 (stays sampling gear). Scar: F23's impulse anchor was single-seed; interference rows exact.
- **Commit:** (this commit)
- **Headline:** "±7 is the floor" — only cap ≥99% everywhere; K=1 stress retention at ±5 is 88.7%.
