# SPIN-21 — REALITY-VARIATION (SPIN-20 question #1 / V2)

**Spoke:** REALITY (dispatched by SPIN-20's top-ranked question) · **Date:** 2026-09-03 ~14:25 AKDT
**Files:** `spin21_reality_variation.py`, `spin21-output.txt` (elapsed 10 s, ~600 fabric runs). Instrument: `dyn_run` — spin-17's canary-proven verbatim clone of `run_fabric` interference arm with **reality_fn and k as parameters**, re-proven byte-identical here (12/12 configs). Integer-only in-loop; floats only at print time; single-pass inline; no pipes; `python3 -u` direct redirect.

## Question

Every sweep in the wheel's history varied fabric knobs (K, grammar, spread, schedule) against **ONE fixed 240-cycle reality trace** (ramp<96 @+8/5, descent 48 @−1, descent 96 @−8/5, band 400–553). Is the K=2 catastrophe, the knee, and the fresh-cohort causality a fabric law or a property of THIS trace?

## Traces (7, integer, matched amplitude band)

| trace | period | band | structure | sustained slope |
|---|---|---|---|---|
| R0-original | 240 | 353–553 | ramp96 +8/5, desc48 −1, desc96 −8/5 | 1.6 |
| R1-ramp144 | 240 | 400–553 | slow rise 144 (~1.06), fast descent 96 | 1.6 (descent) |
| R2-triangle | 240 | 400–553 | up 96 +8/5, down 96 −8/5, hold 48 | 1.6 |
| R3-plateau | 240 | 400–553 | two 0-slope plateaus, jump 153 | 0 |
| R4-sawtooth | 240 | 400–552 | rise 153 @+1, drop, hold 87 | 1.0 |
| R5-zigzag96 | 96 | 400–496 | ±2/tick ramps, 48+48 | 2.0 |
| R6-prime239 | 239 | 354–553 | R0 partition, prime period (incommensurate) | 1.6 |

**Pre-registered decision rule (stated before any panel run, in the script header and the output's first lines):** phenomenon is STABLE/fabric-law iff sign preserved on all 7 traces AND cross-trace range ≤ 5pp; TRACE-PROPERTY if sign flips anywhere OR range > 5pp. Knee "moves" iff argmax-drop spread differs > 2 units from R0.

## Canaries — ALL PASS

- (a) wiring byte-identity dyn_run(R0) vs `run_fabric`: 12/12 configs byte-identical.
- (b) R0 anchors EXACT: zero K-sweep 77.3/50.0/73.9/69.0; ladder@30 K=1 26.8; ladder@15 K=1 71.5 — all 6 PASS at 0.0pp error.
- (c) determinism: 14 dual-runs across all traces byte-identical; the full panel rerun reproduced identically.

## Results

### Panel (5-seed mean %, per trace)

R0 column = published numbers, exact. Full grid in raw output.

| grammar | trace | K=1 | K=2 | K=4 | K=8 |
|---|---|---|---|---|---|
| zero | R0 / R1 / R2 / R3 / R4 / R5 / R6 | 77.3 / 83.9 / 83.9 / 37.0 / 61.1 / 83.5 / 78.3 | 50.0 / 54.8 / 56.1 / 29.4 / 34.5 / 52.9 / 50.6 | 73.9 / 74.7 / 74.6 / 74.3 / 75.9 / 73.2 / 74.1 | 69.0 / 71.0 / 69.4 / 68.7 / 69.0 / 68.4 / 69.2 |
| ladder30 | same order | 26.8 / 36.6 / 36.8 / 26.0 / 31.1 / 24.4 / 27.1 | 28.9 / 37.9 / 35.2 / 21.3 / 20.2 / 26.9 / 29.4 | 12.8 / 29.2 / 25.1 / 58.8 / 45.0 / 21.2 / 13.0 | 14.0 / 30.1 / 25.2 / 53.8 / 44.5 / 21.5 / 13.8 |
| kcoh5@30 | same order | 53.2 / 59.7 / 63.9 / 32.1 / 44.9 / 62.0 / 54.4 | 47.4 / 49.4 / 53.7 / 21.9 / 24.9 / 48.4 / 47.2 | 66.6 / 69.2 / 69.5 / 58.7 / 64.5 / 67.0 / 67.1 | 67.3 / 68.5 / 69.8 / 57.2 / 62.8 / 67.7 / 66.8 |

### Cross-trace stability table (the deliverable)

| phenomenon | R0 | R1 | R2 | R3 | R4 | R5 | R6 | range | verdict |
|---|---|---|---|---|---|---|---|---|---|
| zero K-flip exists (K2=argmin, trough≥5pp) | Y | Y | Y | Y | Y | Y | Y | — | **FABRIC-LAW (7/7)** |
| zero trough depth (pp) | 23.9 | 20.0 | 18.5 | 7.5 | 26.6 | 20.3 | 23.5 | 19.0 | trace-property |
| kcoh5 trough depth (pp) | +5.8 | +10.3 | +10.2 | +10.2 | +20.0 | +13.6 | +7.3 | 14.2 | sign-stable, depth trace-prop |
| ladder30 trough sign | − | − | − | + | + | − | − | 27.3 | **TRACE-PROPERTY (sign flips)** |
| cohort33 trough sign | − | + | − | + | + | − | − | 29.1 | **TRACE-PROPERTY (sign flips)** |
| n_f effect @K=1 (kcoh5−cohort) | +3.9 | +4.9 | +5.2 | +2.8 | +7.6 | +3.8 | +4.4 | 4.9 | **FABRIC-LAW** |
| n_f effect @K=2 | +14.1 | +12.5 | +15.3 | −1.9 | +5.2 | +17.2 | +14.7 | 19.1 | trace-prop (plateau sign-flip) |
| n_f effect @K=4/8 | +44.9 | +31.2 | +39.3 | +1.2 | +13.7 | +39.5 | +45.3 | 44.1 | sign-stable, magnitude trace-prop |
| knee (argmax drop) | 14 | 20 | 14 | 27* | 27 | 10 | 14 | 17 | **MOVES** (4/6 new traces) |

*R3 has no ramp knee (0-slope trace); its "27" is the spread-30 collapse under the 153-jump, a different mechanism.

## VERDICT: SPLIT — the catastrophe's EXISTENCE is a fabric law; its DEPTH, grammar-reach, and the knee are trace-properties

1. **The zero-lock K=2 catastrophe is a FABRIC LAW (7/7 traces).** K=2 is the unique minimum of the K-sweep on every reality — including the 0-slope plateau, the ±2/tick zigzag, and the prime-period 239 trace. The pulse-overlap lifetime mechanism (Spin-5's K=2 stacking) needs nothing from reality's phase structure. SPIN-17's "K=2 uniquely catastrophic" survives reality replacement **at zero-lock**.
2. **The K=2 trough DEPTH is a trace-property** (zero: 7.5–26.6pp, range 19 > 5). Jump-dominated traces mute it (plateau 7.5); a sawtooth amplifies it (26.6).
3. **The stale-grammar K=2 pathology does NOT generalize: TRACE-PROPERTY (sign flips).** On all four 8/5-ramp-family traces (R0, R1, R2, R6) and zigzag, ladder/cohort are WORSE at K=4/8 than K=2 (R0: 26.8/28.9 vs 12.8/14.0 — the published "K=2 not the worst" pattern) — but on plateau and sawtooth the order inverts (ladder R3: 26.0/21.3 vs 58.8/53.8). "K=2 is mild for stale grammars" was a ramp-trace artifact: slow sustained slopes let stale lags re-fire in lockstep; jump-dominated realities punish long pulse trains (K=4/8) instead.
4. **Fresh-cohort causality (Spin 12's n_f effect) is a FABRIC-LAW at K=1** (sign-stable, range 4.9 ≤ 5) and direction-stable at K=4/8 on every ramp trace, but its MAGNITUDE is trace-coupled (1.2→45.3pp) and the K=2 amplification sign-flips on the plateau (−1.9). The n_f×K interaction survives; its size is reality-dependent.
5. **The knee/wall edge MOVES and tracks reality's slope** — R0/R2/R6 (slope 1.6): knee 14; R4 (slope 1.0): 27 (pred 24); R5 (slope 2.0): 10 (pred 12); plateau (slope 0): no knee mechanism at all. R1 is the exception that refines the law: knee 20, 50%-crossing 23.7 — which matches 2Δ/**min**-sustained-slope (24/1.06 ≈ 22.6), not the max slope (24/1.6 = 15). **Refined law: knee ≈ 2Δ / (slowest sustained ramp slope), not the steepest** — the binding constraint is the gentlest slope a stale twin can ride. (The 2pd+1 co-fire wall itself is unreachable at N=6 — outside this panel, honestly booked.)

**One-line answer to SPIN-20 #1:** the K=2 regime catastrophe is a **joint fabric×reality property**: its existence (zero-lock flip, K=2 argmin) is fabric-intrinsic and survived all 6 replaced realities; its magnitude, its extension to stale grammars, and the spread knee are properties of the trace's slope structure — SPIN-17's headline number 27.0pp should be re-quoted as "trace-coupled, fabric-guaranteed ≥7.5pp."

## Scars / honest boundaries

- **Slope-fingerprint bug (caught in dev):** first version measured max per-tick diff, which caught the R0 wrap jump (+47) instead of the ramp slope (8/5) — pred-knees were garbage. Analytic slopes pinned per-trace-spec instead. Lesson: fingerprints of synthetic traces must be computed from the spec, not sampled.
- R0's true band is 353–553 (the wrap drop undershoots 400 by 47) — the "400–553" folklore in the docs is slightly wrong; harmless (all traces compared within ±1% mean).
- The plateau trace has no knee mechanism, so its knee row measures a different phenomenon (jump response), labeled as such.
- 5 seeds, 4800 ticks per cell; per-seed spreads are small (canary c byte-identity), but the 5pp rule is a judgment constant chosen before running, as registered.

## Next spoke proposal

**Slope-law knee:** the refined knee law (2Δ / slowest-sustained-slope) is a one-sweep confirm: synthesize traces with matched period/band and slopes {0.8, 1.0, 1.2, 1.6, 2.0, 2.4}, measure knee vs 24/slope, and test whether the 50%-crossing (not argmax-drop) is the cleaner statistic (R1 suggested it is). Also: rerun the SPIN-17 oscillation-tax spectrum on the plateau trace — if the 27pp regime tax requires ramps, it should collapse to the Jensen floor on a 0-slope reality, killing the "resonance" reading for jump-dominated realities.

Status: **COMPLETE.** Committed+pushed g3-kinduction. WHEEL-LOG.md appended.
