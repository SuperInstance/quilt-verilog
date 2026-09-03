# DEV ROUND 2 — O2: Contention controller boundary

Date: 2026-09-02 (AKDT). Branch `g3-kinduction`. Item: O2 (RESEARCH-AGENDA.md §4, from F14 /
glm-3 #1). Harness: `o2_contention.py` (this directory), output: `o2-contention-output.txt`.
Runtime ~9 s CPU. Integer-only core, seeds (1, 7, 42, 1999, 20260902), 4800 ticks.

## Hypothesis (as booked)

mag+C=1 admission beats admit-all at N≥3 under conflict (69.6 vs 68.0 %w, maxE 232 vs 281 at
N=5), but the win is lag-shaped — with per-twin lag compensation (first-difference integer
cross-correlation blade, 480-tick window, F19/F20) the contention dial goes slack and the win
collapses.

## Method

- Twin harness = glm-3 `run_sw` (verbatim import) generalized: N ∈ {2,3,5,8} × C ∈ {1..N} ×
  regime ∈ {calm (Δ=6, drift=3, K=8), stress (Δ=12, drift=6, K=4)} × arm ∈ {raw, comp}.
  pd=3 everywhere. Latency sets (twin 0 live): N=2 (0,12); N=3 (0,6,12); N=5 (0,3,6,9,12)
  (= glm-3 LATS); N=8 (0,2,3,5,7,8,10,12).
- Lag blade: F19's `discover_lag` (first-difference integer cross-correlation, window 480,
  maxlag 15), run per twin against the live twin's stream. **Exact 4/4 N-configs, every twin**
  (all `exact=True`) — 22/22 lags recovered. Compensated arm shifts each delay line by its
  discovered lag (exact ⇒ all compensated twins read fresh).
- Instrument gates:
  - **Reproduction PASS:** N=5 stress raw admit-all %w=68.0, maxE-sum₅=281; mag+C=1 %w=69.6,
    maxE-sum₅=232 — exactly glm-3's published numbers.
  - **Self-canary CAUGHT:** a deliberately mislabeled arm (mag+C=1 run labeled "admit-all")
    was flagged by the instrumentation (69.6 ≠ 68.0). Note the scar below: glm-3's `agg`
    SUMS int metrics over 5 seeds; first reproduction attempt compared a mean to a sum and
    "failed" until the convention was decoded (281 = 5 × 56.2). The gate doctrine worked twice.

## Raw numbers (mean over 5 seeds; %w in %, maxE = mean per-seed max, ev = mean events)

| regime | N | arm | admit-all %w / maxE / ev | mag C=1 %w / maxE | Δpp (C=1 − admit-all) |
|---|---|---|---|---|---|
| calm | 2 | raw | 5.0 / 36.0 / 7369 | 4.9 / 46.2 | −0.1 |
| calm | 3 | raw | 4.7 / 46.4 / 7675 | 4.7 / 47.6 | +0.0 |
| calm | 5 | raw | 4.5 / 57.0 / 10207 | 4.2 / 48.2 | −0.3 |
| calm | 8 | raw | 1.8 / 74.4 / 20463 | 4.1 / 47.8 | **+2.3** |
| calm | 2 | comp | 71.8 / 25.6 / 3072 | 84.3 / 39.0 | **+12.5** |
| calm | 3 | comp | 74.0 / 32.2 / 4296 | 84.3 / 39.0 | **+10.3** |
| calm | 5 | comp | 70.4 / 38.4 / 7829 | 84.3 / 39.0 | **+13.9** |
| calm | 8 | comp | 31.7 / 106.4 / 26372 | 84.3 / 39.0 | **+52.6** |
| stress | 2 | raw | 69.8 / 37.6 / 2738 | 69.8 / 47.4 | +0.0 |
| stress | 3 | raw | 69.7 / 47.4 / 2904 | 69.8 / 47.6 | +0.1 |
| stress | 5 | raw | 68.0 / 56.2 / 3673 | 69.6 / 46.4 | +1.6 |
| stress | 8 | raw | 57.8 / 99.2 / 6653 | 69.7 / 48.0 | **+11.9** |
| stress | 2 | comp | 98.5 / 26.2 / 1099 | 98.9 / 36.4 | +0.4 |
| stress | 3 | comp | 95.6 / 33.0 / 1765 | 98.9 / 36.4 | **+3.3** |
| stress | 5 | comp | 74.8 / 42.2 / 7075 | 98.9 / 36.4 | **+24.1** |
| stress | 8 | comp | 42.7 / 124.8 / 22940 | 98.9 / 36.4 | **+56.2** |

C-dial shape (comp, stress): C=1 98.9 → C=2 98.5 → C=3 95.6 → C=4 86.3 → C=5 74.8 → C=6 73.9 →
C=7 61.3 → C=8 42.7 — monotone decay from C=1, and **C=1 identical across all N** (84.3 calm /
98.9 stress: with every twin fresh, admitting exactly one is N-invariant by construction — a
built-in determinism check that passed).

## Verdict

**REFUTED in the booked direction; PARTIAL-CONFIRM with a sharper boundary.**

1. **Uncompensated, the win is fan-out-gated, not N≥3-generic.** At N=3 it is zero (+0.1pp),
   at N=5 it is +1.6pp (stress) — *below* the 2pp gate; glm-3's N=5 point was the top of a
   hill whose base starts around N≥5–8. At N=8 it clears the gate decisively: **+11.9pp stress
   (57.8 → 69.7), +2.3pp calm**, with maxE 99.2 → 48.0. Per the decision rule's letter
   (≥2pp at N≥3 uncompensated ⇒ promote), the promotion trigger fires at N=8 only.
2. **The win does NOT vanish under lag compensation — it explodes.** Compensated deltas are
   +3.3 to +56.2pp at N≥3. "Contention is a lag symptom" is false; the truth is the inverse:
   raw contention is largely a lag artifact (small, marginal win), but exact lag compensation
   *synchronizes* all twins onto the same fresh error, creating coherent same-tick contention
   that only admission control can arbitrate.
3. **Naive compensation without a switchboard actively harms at high N:** comp admit-all at
   N=8 stress is 42.7 vs raw admit-all 57.8 (−15.1pp), events 22940 vs 6653. The lag
   compensator *depends on* the contention controller, not the other way round.

**Booking:** promote T2 (contention-sorted admission) to RTL as planned, but note the boundary
— the sort is slack at fan-out N≤5 uncompensated and load-bearing at N≥8 and anywhere the lag
compensator is deployed. Do NOT demote T2 behind the compensator; the two are coupled
(O4's closed loop should carry the C dial as an output). T2 RTL note stands: q_tick_sched
bitonic sort + budget comparator, SVA no-silent-starvation + net==0 across scheduler.

## Scars / bugs found

- **glm-3's `agg` sums int metrics over seeds** (its printed maxE=281 is a 5-seed *sum*, not a
  max or mean). First reproduction attempt read 281 as per-run max and the gate FAILED
  spuriously. Any future re-use of glm-3 §8 numbers must divide sums by 5. Caught by the
  instrument gate, not by eyeballing.
- Compensation at C=N (admit-all) degrades with N even though every read is fresh — the
  failure is self-inflicted chatter (identical twins firing identical pulses, events 3.4×
  raw at N=8). Worth a C-dial chapter in the T2 RTL spec.
- The calm raw arm at N≥3 is degenerate (~5% settles — K=8/pd=3/Δ=6 interference never
  settles under multi-twin conflict; matches kimi #2's calm geometry, where the calm champion
  is pd=2, not the derby defaults). Calm raw cells are booked as-is; the calm signal lives in
  the comp arm.
