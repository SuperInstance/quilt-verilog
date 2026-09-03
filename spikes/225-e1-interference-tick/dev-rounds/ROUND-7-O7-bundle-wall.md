# Round 7 — O7 bundle wall × compensation

Date: 2026-09-03 13:4x AKDT · branch `g3-kinduction` · harness `dev-rounds/o7_bundle_wall.py` · raw output `dev-rounds/o7-bundle-wall-output.txt`

## Hypothesis (pre-registered, agenda §4 O7)

The N=4 bundle-capacity toxicity wall (F7, glm-1 sheet B: interference true-residency 91.0% at
N=2 → 12.2% at N=4 → ~10% flat, while the impulse/sequential arm holds a flat ~51% floor) is
**lag-driven**. Applying per-twin lag compensation — F19 kimi lag blade / F20 opencode 480-tick
first-difference integer cross-correlation, argmax, then `lat' = max(0, lat − L̂)` per twin —
moves the wall right: N=4 trueRes recovers toward the ~51% impulse floor or better.

**Decision rule:** N=4 trueRes ≥ 50% compensated ⇒ capacity law restated as *"stale-sensing
capacity, not twin count"*; wall unmoved ⇒ wall is geometric (10-tick-stale disagreement up to
16 on the 8/5 slope), book the two-law split.

## Method

- `run_fabric` ported **verbatim** from `inventors-derby/exp_glm1.py` (anchor harness, untouched).
- Lag blade ported from kimi exp3 (`INVENTIONS-kimi.md` #3) / `o4_regime_motion.py`: 480-tick
  first-difference integer dot products vs the twin-0 reference stream; streams are reality-only
  so discovery is seed-independent; per-twin `maxlag = lat + 5` (blade margin, extends F19's
  maxlag-15 pattern to lags up to 70 for N=8 stress).
- Grid: N ∈ {2..8} × {raw, comp} × {interference, sequential} × {stress (Δ12/drift6/K4/pd3,
  spacing 10 — glm-1 sheet B exact regime), calm (Δ6/drift3/K8/pd3, spacing 5 — kimi calm)},
  seeds {1, 7, 42, 1999, 20260902}, 4800 ticks. Integer-only verdict path (permille); floats
  only in display division.

## Lag blade verification (gate before trusting comp arms)

**11/11 exact** (lags 3, 5, 7, 10, 15, 20, 30, 40, 50, 60, 70 → all discovered exactly) —
extends F19's 5/5 to the full bundle range. Compensated arms therefore run with oracle-grade
lags (`L̂ = lat` exactly, all compensated lats = 0 ⇒ all twins co-located with the reference).

## Canary results (all 3 mandatory)

1. **Double-run byte-identity:** full grid (56 cells × 5 seeds × 2 passes) — **PASS**, every
   cell identical.
2. **Anchor replay vs glm-1 sheet B published values (stress raw):** 8/8 PASS — interf N=2
   91.0 vs 91.0, N=3 34.4 vs 34.5, N=4 12.1 vs 12.2; seq N=2 78.4 vs 78.4, N=3 53.1, N=4 51.4,
   N=5/8 50.8 vs 50.9 (±0.1pp is permille-integer rounding of the 5-seed mean; tolerance ±2pp).
   Anchor also reproduces the event-explosion rate (2041→28316 raw stress) and the flat
   sequential floor — the published shape is byte-for-byte the harness's.
3. **Self-canary:** N=2 raw interference arm deliberately passed off as N=4 raw → checker
   flagged it (91.0 vs 12.2, FAIL as required) — **CAUGHT**.

## Numbers (5-seed means, 4800 ticks; trueRes% = |g − s_true| ≤ Δ)

### Stress (Δ12 drift6 K4 pd3 spacing10)

| N | intf raw | intf comp | seq raw | seq comp | intf raw ev | intf comp ev |
|---|---|---|---|---|---|---|
| 2 | 91.0 | 98.4 | 78.4 | 100.0 | 2041 | 1099 |
| 3 | 34.5 | 95.6 | 53.1 | 100.0 | 6415 | 1765 |
| 4 | **12.2** | **86.3** | 51.4 | 100.0 | 10408 | 3698 |
| 5 | 9.7 | 74.7 | 50.9 | 100.0 | 15025 | 7075 |
| 6 | 9.9 | 73.9 | 50.9 | 100.0 | 19338 | 8900 |
| 7 | 10.9 | 61.3 | 50.9 | 100.0 | 23690 | 13952 |
| 8 | 11.4 | 42.6 | 50.9 | 100.0 | 28316 | 22940 |

### Calm (Δ6 drift3 K8 pd3 spacing5)

| N | intf raw | intf comp | seq raw | seq comp |
|---|---|---|---|---|
| 2 | 73.4 | 71.8 | 84.3 | 100.0 |
| 3 | 46.5 | 74.0 | 53.6 | 100.0 |
| 4 | 13.3 | **77.4** | 51.4 | 100.0 |
| 5 | 6.7 | 70.4 | 51.2 | 100.0 |
| 6 | 4.9 | 62.0 | 51.1 | 100.0 |
| 7 | 5.0 | 44.7 | 51.1 | 100.0 |
| 8 | 5.3 | 31.6 | 51.1 | 100.0 |

## Verdict vs decision rule

**WALL MOVED.** N=4 stress interference trueRes = **86.3%** compensated (vs 12.2% raw;
gate ≥ 50%, cleared by 36pp; also beats the 51% impulse floor by 35pp). The N=4 wall is
**lag-driven**, and the capacity law is restated: **the bundle capacity is a stale-sensing
capacity, not a twin count.** Confirmed in both regimes (calm N=4: 13.3 → 77.4).

**But the wall is not abolished — it is moved right, and the mechanism changes.** Compensated
interference degrades again from N≈7 (stress 86→74→61→43; calm 77→70→62→45→32), with the
familiar event explosion returning in the comp arm (3698→22940). With all lags repaid the twins
are co-located and **co-fire**: every triggering twin injects its own pulse in the same tick,
so net correction scales ~N·(‖e‖/pd) — a genuine amplification wall, not a staleness wall.
Two mechanisms, one per arm: raw wall = staleness (geometric 10-tick-stale disagreement),
comp wall = co-fire gain. The stale-sensing restatement is the primary booking; the co-fire
ceiling at N≈6–7 is the new secondary law (candidate: pulse-divisor pd should scale with N,
or admission should dedupe co-located co-fires — connects to T2/O2 contention sorting).

Sequential comp = 100.0% at every N (identical aligned twins + T1 priority = single perfect
sensor) — trivial ceiling, not evidence of capacity; noted and discounted.

## Scars / lessons

- The blade stays exact out to lag 70 with a 480-tick window (period 240 ⇒ first-difference
  seat is unique within maxlag); no need for a longer window at these lags.
- Anchor replay caught a 0.1pp permille-rounding wobble (34.4 vs 34.5) — integer 5-seed mean
  floors; tolerance ±2pp absorbs it, but anchors must be booked in permille to compare exactly.
- Compensation makes `allW == trueRes` identically (all reads equal) — the allWithin metric
  loses discriminating power in comp arms; trueRes + events carry the signal.
- seq-comp 100% is a siren: co-located twins behind a priority scheduler collapse to one sensor.
  Never book it as capacity.

## Canaries

double-run **PASS** · anchor 8/8 **PASS** · self-canary **CAUGHT** — 3/3.
