# ROUND 14 — Q7: minimal regime-gating dial (charter §5.4)

**Item:** Q7 (RESEARCH-AGENDA.md, open tier; charter §5.4 regime-gating mandate).
Branch `g3-kinduction`. Date: 2026-09-03. Lane `dev_q7_regime_dial`.
Harness: `dev-rounds/q7_regime_dial.py` (reuses `o4_regime_motion.py` arms,
protocol, κ-detector, and live blade VERBATIM; `e1.py` LCG/reality lineage;
integer-only, no multiply anywhere in the control path — shifts/adds/compares
only). Output: `dev-rounds/q7-dial-output.txt`.

---

## PART 1 — PRE-REGISTRATION (committed before any comparison run)

### Hypothesis

A minimal integer controller mapping observable state {κ-detector output,
lag-blade estimate L̂, fan-out N} (+ one transient-hit sensor, see below) to
config {mode, K, pd} exists with **3 integer registers and no multiply**, and
clears BOTH O4 gates that the O4 κ-dial alone failed:

- (a) **%w ≥ 932‰** (beat O4 adaptive), and
- (b) **debt ≤ 32,770** (60% of best-static seq-comp-oracle 54,616 — the gate
  O4 failed at 57,136), and
- (c) **L̂ knife-edge**: no dial arm may degrade >5pp vs its L̂-aligned twin
  (O4 scar: bursty sequential L̂=9→994‰, L̂=10→336‰).

on the same calm→conflict→bursty protocol (4800 ticks × 5 seeds, shifts at
1600/3200, unknown to controllers), same 6 static arms + O4 adaptive arm as
baselines, re-run verbatim from `o4_regime_motion.py`.

### Why O4 failed and what changes (mechanism, pre-registered)

O4's booking decomposed the failure into three causes; the dial is designed
against each:

1. **90-tick κ-detector entry lag** (debt-climb window must fill ~11× while
   the regime hurts). Fix (task doctrine): the **lag blade is the fast path** —
   L̂ jumps 5→10 at the conflict shift and seats within one 480-tick refresh;
   κ is demoted to **slow confirm** (bridge before the first post-shift blade
   refresh). Bursty is detected FASTER than both by a **transient-hit sensor**
   (below), since bursty = calm deltas + ±45 single-tick ADC glitches.
2. **Debt is a floor under bursts at Δ6**: every ±45 glitch is answered
   tick-for-tick (~90 debt per glitch event: chase out + chase back), ~36k of
   the 54.6k best-static debt. Fix: a **single-tick transient suppressor** on
   the aligned streams — a genuine per-tick reading change is ≤2 (reality
   slope) ± alignment shift at blade refresh (≤ ~10); any aligned single-tick
   jump ≥ 40 can only be a glitch, so that stream's trigger is suppressed for
   one tick. This is an *admission* filter on triggers (per-stream, one tick,
   no deferral queue — F16's deferred-admission failure mode is avoided
   because nothing is ever admitted late; the tick is simply skipped and g
   keeps drifting ≤3). Known coupling, booked up front: **threshold 40 is
   informed by the pre-registered ±45 glitch magnitude** (REGIME-META E4.E
   shape, characterized in round 4); robustness probed at glitch mag 60 and 20.
3. **L̂ knife-edge** (exact alignment is glitch-coherent and kills sequential
   in bursty): the transient suppressor removes the mechanism — whether twins
   glitch on the same aligned tick (L̂ exact) or split ticks (L̂±1), each
   stream's jump is ≥40 and suppressed individually. Gate (c) tests this
   directly at forced L̂±1.

### Dial spec (3 registers, integer, no multiply)

| Register | Meaning | Source | Update |
|---|---|---|---|
| R1 = L̂ | lag-blade estimate, 0..15 | O4 live blade (`discover_lag_obs`, sign-clipped, verbatim) | every 480 ticks from t=480 |
| R2 = σ (stress bit) | regime estimate | fast: L̂ ≥ 8 → 1; slow confirm: κ-detector CONFLICT → 1 | per tick (OR of fast/slow) |
| R3 = β (bursty bit) | transient regime | ≥2 transient hits in the last 16 ticks (16-slot integer window) | per tick |

Sensor front-ends reused from O4 organs (not counted as dial registers, since
O4 already paid for them): the κ-detector's own windows, the blade's
cross-correlation, the 480-tick observation history, and a 16-slot transient-hit
window (same idiom as the detector's cancel window).

**Outputs {mode, K, pd, td} (all integer compares/selects):**

- `mode` = interference iff (σ=1 AND β=0), else sequential. (Bursty forces
  sequential at Δ6; conflict holds interference per O4/E4 doctrine; the
  compensator+filter make sequential dominant everywhere else — O4's booking.)
- `K` = 1 when interference (O1 champion axis: K small under stress), inert
  under sequential.
- `pd` (pulse_div) = 2 when interference (O1 champion), inert under sequential.
  Phase-decay doubling (O5, promoted +2.0pp stress) ON when σ=1 AND β=0.
- `td` (trigger threshold) = 12 iff (σ=1 AND β=0), else 6. (Tracks the
  environment's Δ; bursty's Δ is calm-like and β is what distinguishes it —
  L̂ cannot, both conflict and bursty sit at lag 10.)
- Compensation: fresh twin delayed by L̂ (O4 live-realizable frame, verbatim).
- Transient suppressor: per aligned stream, |jump vs previous aligned reading|
  ≥ 40 → suppress that stream's trigger this tick, log a hit.
- **F14 sort gate**: when fan-out N ≥ 6 and >1 trigger is live, admit only the
  single largest-|e| trigger (mag key, C=1 — rounds 2/3: wall at N=6, +11.9pp
  raw/+56.2pp comp at N=8). At this round's N=2 it is **inert by design**;
  verified by (i) rejected-count == 0 on all dial runs and (ii) a unit check
  that the gate selects argmax|e| on a synthetic N=6 candidate set.
- No multiply anywhere in the dial path (correlation blade is O4-reused;
  inside the dial: adds, subtracts, compares, //2 halving only).

### Arms

Baselines (verbatim `run_arm`): seq-raw, int-raw, seq-comp-fix, int-comp-fix,
seq-comp-oracle, int-comp-oracle, adaptive — 7 × 5 seeds.
Dial arms: `dial` (live), plus booked probes (not gate arms): `dial-Lm1` /
`dial-Lp1` (forced L̂±1, whole run — gate (c) arms), `dial-nofilter`
(suppressor off — shows the knife-edge returns and that the filter is
load-bearing), `dial-g60` / `dial-g20` (glitch magnitude 60/20 — threshold
coupling probe). All 5 seeds each.

### Decision rule (pre-registered)

PROMOTE iff ALL of:
1. mean %w (dial) ≥ 932‰;
2. mean debt (dial) ≤ 32,770;
3. knife-edge: min(pm(dial-Lm1), pm(dial-Lp1)) ≥ pm(dial) − 50‰ AND
   bursty-seg pm at L̂±1 ≥ aligned bursty-seg pm − 50‰;
4. canaries pass: (i) double-run byte-identity; (ii) O4/F19 anchor replay —
   adaptive mean 932‰/57,136, int-comp 984‰/17,700/28, seq-comp 1000‰, blade
   exact on 3/5/7/10/15; (iii) mislabeled-arm self-canary CAUGHT (inverted
   dial must be caught by the mode-doctrine checker; filter-off arm passed
   off as full dial must be caught by fingerprint).

If the debt gate fails again: book WHICH register saturated / WHICH input
misled (per-segment debt telemetry is recorded for exactly this). If an anchor
fails to replay: STOP, commit failure analysis, no verdict.

— end PART 1 (pre-registration; comparison runs begin only after this is committed)
