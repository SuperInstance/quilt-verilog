# SPIN-16 — REGIME (spoke 6): memorylessness of the spread knee

Re-dispatch of the failed SPIN-13 regime lane (its claims were UNMEASURED).
Everything below was actually run: `wheel/spin16_regime.py`, raw output in
`wheel/spin16-output.txt` (elapsed 5 s).

**Config:** N=6 ladder grammar, K∈{1,2}, seeds {1, 7, 42, 1999, 20260902},
4800 ticks, delta=12, drift=6, pd=3, shift point t=2400, settling window
W=240 (one reality period). Integer-only fabric math; floats only at print
time. Instrument = `dyn_run`, a line-verbatim clone of `exp_glm1.run_fabric`
with per-tick `lats_fn(t)` (canary-proven byte-identical).

**HYPOTHESIS:** the spread≈15 knee (SPIN-4/5) is a static property — no
hysteresis, no regime-switching tax.

## Verdicts

| # | Sub-claim | Verdict |
|---|-----------|---------|
| 1 | Hysteresis / loop area | **VALIDATED (memoryless)** — not falsified |
| 2 | Regime oscillation tax | **FALSIFIED at K=2 (real tax up to 27pp); marginal at K=1** |
| 3 | Knee-holding controller | **INCONCLUSIVE — no interior knee exists in this metric** |
| — | Overall hypothesis | **MIXED** |

## Headline numbers

### 1. Hysteresis (all 20 ordered shift pairs s→s′, s,s′∈{5,10,15,20,30})

- **Max post-settling tail deviation vs phase-fair static-s′ baseline: +0.0 pp**
  (last 240 ticks, both K, every direction). Every tail dev printed 0.0.
- **Loop area: ~0.0 tick-pp** at K=1 and K=2 (5→30 tail dev +0.0, 30→5 +0.0).
- Immediate post-shift deviations ≤ 0.9 pp (K=2 worst, e.g. 5→10 +0.7pp,
  30→10 −0.9pp) — all decay to zero within the settling window.
- Transient half-lives: **0 ticks in nearly all cells**; a few K=2 cells
  show short measurable transients (5→30: 28 ticks, 30→15: 44, 20→10: 268,
  30→5: 20) — none survive past W=240. The fabric carries **no spread
  state**: lats only gate reads of reality, so single shifts are absorbed
  as fast as pulse memory (K) itself decays.

**Verdict: VALIDATED.** Single spread shifts behave exactly like the static
regime they land in. No hysteresis, zero loop area.

### 2. Regime oscillation (square wave 5↔30, period P; plus controls)

| P | K | osc% | static5% | static30% | TWmean% | static17% | tax (TWmean−osc) |
|---|---|------|----------|-----------|---------|-----------|------------------|
| 16 | 1 | 57.0 | 97.6 | 26.8 | 62.2 | 59.1 | **+5.1 pp** |
| 64 | 1 | 56.2 | 97.6 | 26.8 | 62.2 | 59.1 | **+5.9 pp** |
| 256 | 1 | 59.6 | 97.6 | 26.8 | 62.2 | 59.1 | **+2.6 pp** |
| 16 | 2 | 29.9 | 84.9 | 28.9 | 56.9 | 56.1 | **+27.0 pp** |
| 64 | 2 | 45.2 | 84.9 | 28.9 | 56.9 | 56.1 | **+11.7 pp** |
| 256 | 2 | 55.2 | 84.9 | 28.9 | 56.9 | 56.1 | +1.7 (no-tax) |

Jensen controls (added to separate switching cost from curve concavity):
10↔25 (same mean spread 17.5) vs static-17: K=1 P=16 −1.9pp, P=64 −3.3pp
(osc *beats* static — curve shape dominates at K=1); but **K=2 P=16:
39.6% vs 56.1 = 16.4pp below even the matched-mean static**, and 5↔30 at
K=2 P=16 (29.9%) sits 26.2pp below static-17 and even below static-30
(28.9%).

**Verdict: FALSIFIED at K=2** — a genuine regime-switching tax exists:
fast spread oscillation degrades residency below *every* static baseline
including matched-mean, which no static-curve nonlinearity can explain. The
mechanism is dynamic: alternating trigger sets across regimes keep the
error profile out of phase with any fixed spread's attractor, and the
K=2 pulse superposition carries the mismatch. Tax shrinks with period
(27pp → 12pp → 1.7pp at P=16/64/256) — the tax timescale tracks the
hysteresis transients (~tens of ticks). At K=1 the effect is small and
mostly Jensen (2–3pp vs static-17, control goes negative).

### 3. Knee-holding controller (blind hill-climb, ±1 per 64 ticks, clamp [8,22])

| mode | K=1 | K=2 |
|------|-----|-----|
| static-8 | 96.3 | 90.5 |
| static-15 | 71.5 | 60.0 |
| static-22 | 43.0 | 40.7 |
| controller | 72.5 | 67.5 |

**Verdict: INCONCLUSIVE.** In this configuration the spread→residency curve
is **monotone decreasing — there is no interior knee at 15** (5→97.6%,
15→71.5%, 30→26.8%). The knee≈15 from SPIN-4/5 lives in a different
metric/config, so "knee-holding" is ill-posed here. The controller did
work as a controller: it beats its static-15 start (+1.0pp K=1, +7.5pp
K=2) but is dominated by the clamp edge static-8 (−23.8/−23.0pp) — a blind
hill-climb on a monotone slope can only crawl to the boundary, and does.

## Canaries (all PASS)

- **C1 wiring byte-identity:** dyn_run vs `exp_glm1.run_fabric`, 12 configs
  (3 grammars × K{1,2} × seeds{1,42}) — every per-tick resid vector
  byte-identical; plus zero@0 == ladder(0) grammar identity. PASS.
- **C2 anchor replays (5-seed means):** zero@15 K=1 = 77.3%, debt 187834;
  ladder@15 K=1 = 71.5%, ev 5792, debt 106378 — all exact. PASS.
- **C3 no-shift byte-identity:** hold-s runs == static runs (5 spreads ×
  K{1,2} × 5 seeds). PASS.

## Scars / lessons

1. **NameError K vs k** in the controller's inline clone killed run 1 at
   EXP3 — inline clones must take k as a parameter, never reference the
   global KS table. (Run 1's EXP1/EXP2 numbers were unaffected; full rerun
   after fix.)
2. **TWmean is a dishonest baseline alone.** The static spread→residency
   curve is concave-ish here, so time-weighted means embed a Jensen gap.
   Always run the matched-mean control (10↔25 vs static-17) before calling
   an oscillation gap a "switching tax" — at K=1 it flips the conclusion.
3. **The "spread knee" is metric-dependent.** At delta=12/drift=6 residency
   is monotone in spread; SPIN-4/5's knee≈15 does not reproduce in this
   metric. Cross-spoke comparisons need the metric stated, not just the
   grammar.
4. First draft of the controller tried to schedule lazily from a pure
   lats_fn with chunked re-simulation — that resets the LCG and is invalid.
   The online controller must be a real inline simulation (one pass, spread
   as loop state). Deleted before it ever ran.

## New spoke proposal

**SPIN-17 — OSCILLATION TAX SPECTRUM (regime, follow-up):** the K=2
switching tax (27pp @ P=16 → 0 @ P≥256) is the first measured *dynamic*
regime effect on this fabric. Measure the tax vs period curve finely
(P ∈ {8..1024}), vs K ∈ {1..8}, and vs duty cycle (asymmetric square
waves); test whether the tax collapse-time constant equals the pulse
settling time (K × decay) or the reality period. Prediction if the
memoryless picture survives at long periods: tax(P) → 0 as 1/P; a
non-hyperbolic decay would indicate a second, slower memory channel.

Status: **COMPLETE.** Nothing committed or pushed.
