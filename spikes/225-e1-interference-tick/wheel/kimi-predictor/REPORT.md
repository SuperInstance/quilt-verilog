# KIMI-PREDICTOR — learned-predictor scheduler (g3-kinduction lane)

**Lane:** kimi-predictor · **Date:** 2026-09-03 ·
**Files:** `kimi_predictor.py`, `run-output.txt`, `results.json` ·
Fabric: `inventors-derby/exp_glm1.run_fabric` (E1 contract pinned via
byte-identity canary). Integer-only inside the loop: the deployed
predictor is a fixed-point integer scorer (SCALE=1024); floats only in
offline training (sklearn logreg, spike-226 `e2_model.py` lineage) and
display statistics.

## Design

- **Features** (per tick, integer): `[in_flight, mean_lag, stale_mass, K]`
  — in-flight pulse count after FIFO expiry, mean of current latencies,
  count of twins with `(8/5)*lag >= Δ` (`l*8 >= 5*Δ`), and K. These are
  the e2 lane's top-weighted physics features (`in_flight −0.79`,
  `lag −0.55`) reduced to a 4-integer live-state vector.
- **Train:** sklearn LogisticRegression on 172,800 per-tick records from
  the **ladder-grammar grid** (spreads 5–30, K∈{1,2}, seeds **{1,7,42}**),
  label = post-correction residual ≤ Δ. Standardized weights folded into a
  fixed-point integer scorer `z = OFF + Σ Cᵢ·fᵢ` (integer sign agreement
  with the float model: 1.0000).
- **Deploy:** runtime scheduler heuristic, one integer score per tick.
  `z < tlo` → shrink every lag by 1 (spread −1); `z > thi` → restore 1
  toward nominal. Hysteresis thresholds `(tlo, thi) = (−64, 2482)`
  grid-selected on **train seeds/grammars only**.
- **Eval (the only metric that counts):** residency gain on **held-out
  grammars** (cohort 3+3, outlier, kcoh5) × **held-out seeds**
  {1999, 20260902} vs fixed heuristics static spread 15 / static spread 30.

## Canaries (all PASS — mandatory gate)

1. **Sequential-arm byte-identity:** 16/16 sequential runs with the
   scheduler active are byte-identical to `run_fabric` (full resid,
   cflags, emissions traces + scalars).
2. **Harness identity:** 32/32 interference runs scheduler-off
   byte-identical to `exp_glm1.run_fabric`.
3. **SPIN-5 replay:** ladder s=15 K=1 scheduler-off per-seed permille
   **709/713/721/714/717 EXACT** (mean 71.5%, tolerance was ±2pp).

## Headline numbers (held-out, seeds {1999, 20260902})

| grammar | K | static15 | static30 | scheduled | gain vs s15 | gain vs s30 |
|---|---|---|---|---|---|---|
| cohort 3+3 | 1 | 57.1 | 48.9 | 57.1 | +0.0 | +8.2 |
| cohort 3+3 | 2 | 41.1 | 33.3 | **75.2** | **+34.0** | +41.9 |
| outlier | 1 | 73.5 | 53.2 | 73.5 | +0.0 | +20.2 |
| outlier | 2 | 49.1 | 46.0 | 49.1 | +0.0 | +3.1 |
| kcoh5 | 1 | 73.5 | 53.2 | 73.5 | +0.0 | +20.2 |
| kcoh5 | 2 | 49.1 | 46.0 | 49.1 | +0.0 | +3.1 |

- **Mean held-out gain: +5.7pp vs static15, +16.2pp vs static30;
  worst cell vs static15: +0.0pp (no grammar harmed).**
- The entire gain is one mechanism: at cohort 3+3 K=2 the predictor rides
  the spread down 15 → 8 (`[0,0,0,8,8,8]` steady state; 244 shrink-ticks
  vs 237 restore-ticks) and holds it there — 41.1% → **75.2%**, beating
  even zero-lock-at-K=2 (50.0%) because it parks *at* spread 8 instead of
  collapsing to the chatter mode.
- Learned weights are physics-consistent with e2: in_flight −0.69,
  mean_lag −0.68, stale_mass −0.62, K +0.41 (standardized).
- In-domain sanity: ladder@15 K=1 scheduled = 71.5% — the scheduler is a
  perfect no-op on its home config.

## Verdict: VALIDATED (narrow)

The learned predictor transfers from ladder grammars to unseen grammars
and produces real residency gain on held-out seeds with zero regressions
— but the gain is concentrated in exactly one cell (cohort 3+3, K=2).
Everywhere else the scheduler correctly refuses to act.

## Scars / honest boundaries

- **K=1 inert:** at K=1 the predictor never shrinks on any held-out
  grammar (0 shrink-ticks; pulse pile-up never crosses `tlo` because
  pulses die in one tick). All "gains vs s30" at K=1 are just the
  scheduler sitting still at spread 15 while the static-30 baseline
  self-destructs — real, but cheap.
- **kcoh5 ≡ outlier:** same multiset (`[0,0,0,0,0,s]`), byte-identical on
  eval seeds (order-invariance, Spin-5 canary C, re-verified here). The
  held-out suite is effectively 2 distinct grammars × 2 K × 2 seeds.
- **n=2 eval seeds** per cell; per-seed spread within cells is small
  (≤2pp) but this is a 2-point estimate, not an inference.
- Threshold grid is coarse (deciles of the train z-distribution, 9 pairs);
  finer grids might find a K=1-active band. Not chased — held-out honesty
  preferred over tuning.
- The predictor sees only its 4 features; it cannot distinguish grammar
  *shape*, only its mass/lag shadow. The cohort-K=2 rescue works because
  pile-up + lag is the right shadow there; a grammar whose losses hide
  from these features would be invisible to it.

VERDICT: VALIDATED (narrow) — +5.7pp mean held-out gain vs static15 (+16.2pp vs static30), zero regressions; mechanism = one cohort-K=2 rescue (41.1→75.2% via spread 15→8 parking); K=1 scheduler inert; 3/3 canaries PASS (sequential byte-identity, harness identity, spin-5 replay exact).
