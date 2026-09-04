# SPIN-15 — CONSERVATION (closure sweep on the E1 fabric)

Re-dispatch of the failed SPIN-12 conservation lane (brief verbatim). Lane:
wheel_spin15_conservation (zai/glm-5.3). Run: 2026-09-03 20:03 UTC (~5 s wall).
Script: `wheel/spin15_conservation.py`; raw output: `wheel/spin15-output.txt`.
Nothing committed or pushed; WHEEL-LOG untouched (cron lane logs).

## Hypothesis (pre-registered by the brief)

- (C1) Mass closure: debt − Σ|trigger err| = 0, integer-exact, every run.
- (C2) Additivity: global debt = Σ per-twin toll subledgers, integer-exact.
- (C3) Toll-per-event is grammar-INVARIANT at fixed K (tolls track K and
  occupancy, not grammar).
- (C4) Saturation: a debt/event cap exists somewhere in stress space.

## Method

Harness: `inventors-derby/exp_glm1.run_fabric` (interference arm, delta=12,
drift=6, pd=3, 4800 ticks) + `run_ledger`, a clone whose every g/pulse line
is copied verbatim (floor-div decay `mag = mag - (mag//2)`) plus an exact
integer ledger: per-twin tolls, emitted signed/abs pulse mass, net
injections, decay removals, expiry evaporation, in-flight residual, drift
sum, g trajectory. Integer-only inside every loop; floats only at print.
Grid: 6 grammars (ladder@15, ladder@30, zero, cohort3+3, kcoh5@15,
outlier@30) × K∈{1,2,4,8} × seeds {1,7,42,1999,20260902} = 120 runs, plus
saturation arms (~120 more). All numbers below are real runs.

**Why SPIN-12 failed (post-mortem, fixed here):** two independent ledger
bugs. (a) The old clone re-derived negative-mag decay with different
semantics than run_fabric's floor division → byte-identity canary death.
(b) Both the old clone and this lane's first draft wrote the pulse-mass
identity without an expiry channel — pulses whose life expires carry an
un-decayed residual the fabric silently destroys. Correct law (validated):

```
emitted_signed == decay_loss + inflight + expired_residual   (exact, every run)
g_final        == g0 + drift_total + net_total               (exact, every run)
```

## Canaries — ALL PASS

- **C1 wiring byte-identity:** 24/24 configs (6 grammars × K{1,8} × seeds
  {1,42}), every run_fabric key identical. (Brief asked ≥8.)
- **C2 SPIN-11 anchor replay:** ladder@15 K=1 → 71.5% / ev 5792 / debt
  106378 — EXACT on all three. zero@15 K=1 → 77.3% / debt 187834 — EXACT.
- **C3 closure identities exact** on both anchors, all 5 seeds.

## Results

### (C1) Mass closure — VALIDATED (wiring-exact)
Δ = 0 on every run: 24 sweep configs × 5 seeds + all saturation arms.
Honest caveat: the emission list and the mass counter are built in the same
pass, so this is a wiring invariant — it certifies instrumentation, not
harness honesty.

### (C2) Debt additivity — VALIDATED (wiring-exact)
Σ per-twin toll = global debt exactly, every run (same caveat as C1).
The non-tautological laws (pulse-mass with evaporation, g-trajectory) also
close exactly everywhere — **headline physics: the fabric EVAPORATES pulse
mass at expiry**, |evaporation| ≈ 0.17–0.30 per event, roughly constant
across all stress levels (it is the sum of ±1 residuals of dying pulses).

### (C3) Toll-per-event grammar-invariance — FALSIFIED
Rel-spread across grammars at fixed K: **29.4–38.1%** (K=1: 18.4→26.9;
K=2: 27.4→36.8; K=4: 18.0→25.9; K=8: 18.2→26.3). Toll/event depends
strongly on grammar. Structure found:
- Ranking is STABLE: ladder@15 minimum, outlier@30 maximum at every K —
  toll/ev tracks stale-mass m_s (grammar law of SPIN-9/12), i.e. worse
  grammars pay more toll per event, not just more events.
- K=2 is a uniform pathology: +9 to +12 debt/ev over K=1/4/8 for every
  grammar (resonance between 2-tick pulse life and the drift/reality ramp).
- Curious exact tie: zero ≡ kcoh5@15 at K=1 (both 21.5) despite different
  event counts (8756 vs 11211) — one 15-lag twin adds events but not
  per-event toll at K=1. Not chased further (booked as open).

### (C4) Saturation — MIXED (cap on events, none on debt/ev under drift)
Worst grammar: ladder@30 (12.8% residency at K=4).
- **Arm A (drift → 384):** debt/ev grows 24.5 → 28.5 → 61.0 → 188.1 →
  683.2 → 2584.9 → **9202.4** — no ceiling, roughly linear in drift beyond
  drift≈24 (trigger error scales with drift). Event count DOES saturate:
  28,757 events / 28,800 possible = **99.85% occupancy ceiling** (every
  twin fires nearly every tick).
- **Arm B (delta → 1):** debt/ev FALLS 24.5 → 17.1 and total debt
  PLATEAUS at ~460k — under tightening, debt is capped by the deadband
  itself (errors can never grow far past delta before re-trigger).
- **Arm C (ticks → 38400):** debt/ev stationary at 24.5–24.6; identities
  hold at 8× duration. No drift with time.

## Headline number

**debt/event = 9202 at drift=384 and still climbing — the fabric has an
event ceiling (99.85% occupancy) but NO debt ceiling under drift
escalation;** while under deadband tightening debt is hard-capped (~460k
plateau) and under duration extension it is perfectly linear.

## Verdict table

| Sub-claim | Verdict |
|---|---|
| Mass closure Δ=0 | VALIDATED (wiring-exact) |
| Debt = Σ twin tolls | VALIDATED (wiring-exact) |
| Pulse-mass conservation | VALIDATED with NEW expiry-evaporation channel (~0.2/event) |
| g-trajectory identity | VALIDATED (exact everywhere) |
| Toll/event grammar-invariant at fixed K | FALSIFIED (29–38% spread; stable ranking tracks m_s; K=2 uniform pathology) |
| Debt/event saturation cap | MIXED: events saturate (99.85%), debt/ev unbounded under drift; debt capped under delta-tightening |

## Inconclusive / honestly booked

- C1/C2 are structurally near-tautological (same-pass ledgers); they bound
  instrumentation error only.
- The zero ≡ kcoh5@15 K=1 toll/ev tie is unexplained; single point, no
  mechanism chased.
- Evaporation is reported as mean of |net expired|; its sign structure
  (does the fabric preferentially destroy + or − pulses?) is unmeasured.
- Saturation hunt ran on ladder@30 only (worst by residency); drift
  escalation on grammars with fresh twins may saturate differently.
