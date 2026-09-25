# Round 6 — O6 cofire homeostat micro-probe

Date: 2026-09-03 13:2x AKDT · branch `g3-kinduction` · harness `dev-rounds/o6_cofire_homeostat.py` · raw output `o6-cofire-output.txt`

## Hypothesis (pre-registered, agenda §4 O6)

Minimal repair of the charter §1.2 cofire collapse (S1, ×3 lanes) — **bounded trust ∈ [4,12],
init 8, decay toward neutral 8 every 32 silent ticks**, plus **opencode's lagged reference**
(first-difference 480-tick blade, F19/F20; judge twin i's trigger sign at t against twin j's at
t−lag — the only ingredient ever shown discriminative, F21) — **preserves ≥800‰ steady-state on
honest twins while still demoting a true defector**, with glm-1's cancellation whistle (×2–5, F6)
as cross-check. Fault models: clean, noisy-T2 (±14, opencode #2), lying-T2 (+24, ticks 1200–2399,
glm-1 A). Decision rule: all three gates ⇒ cofire v1.1 survives into §3.2; any failure ⇒ demote
cofire to v2 per charter failure mode (c), demo runs selection-only learning.

## Setup

- Fabric: kimi exp1 variant A reused verbatim (canary A); emission magnitude `m = m*trust//8`.
- 5 seeds {1, 7, 42, 1999, 20260902}, 4800 ticks, integer-only, LCG fixed; dedicated fault RNG
  stream so injection never perturbs the base drift stream.
- Regimes: stress Δ=12/drift=6/K=4/pd=3/lat2=10 (primary); calm Δ=6/drift=3/K=8/pd=3/lat2=5
  (secondary, the F13 K=8-artifact regime).
- Arms: clean-static / clean-homeostat (both regimes); noisy-T2 and lying-T2, static vs
  homeostat, stress. Lag from the blade (self-calibration, S2 doctrine).
- Gates (pre-registered): **G1** clean homeostat stress mean ≥800‰; **G2** lie-window T2 trust
  ≤5.0 mean, ≥900‰ of late-window ticks at floor (≤5), T1 trust ≥7.0; **G3** homeostat
  lie/honest cancellation ratio ≥2×.

## Results

### Canary A — F17 anchor replay (kimi verbatim)

fixed mean **830‰**, trust-A mean **308‰**, cancel mean **5** — sheet-exact (830/308/5), final
trust pairs match the sheet row ((0,1)(2,0)(0,11)(0,1)(3,0)). PASS. Lag blade exact 2/2
(calm 5, stress 10). Self-canary (lie-static mislabeled as homeostat) CAUGHT on fingerprint
(pm/debt/events/cancels). Double-run byte-identical. **3/3 canaries.**

### Honest twins (G1)

| arm | stress pm/seed | mean | debt | cancel | end-trust mean |
|---|---|---|---|---|---|
| clean static | 830 824 834 836 829 | **830‰** | 34,995 | 70 | 8.0 |
| clean homeostat | 786 780 776 784 764 | **778‰** | 38,786 | 87 | **5.0** |

**G1 FAIL (778 < 800).** The homeostat does not collapse to deafness (F17's 308‰ is repaired)
but it *bleeds on honest twins*: trust drifts to the floor (mean 5.0) because in the conflict
regime honest twins are **antagonists** — they fire opposite signs at the true lag, so the lagged
*cofire-sign* predicate scores honest disagreement as evidence against both. Lag structure fixes
credit assignment (F21) but sign-agreement is still the wrong predicate in conflict.

### Defector demotion (G2, lying-T2)

| arm | pm mean | debt | whistle | T2 late-window trust | floor-frac | T1 trust | maxE |
|---|---|---|---|---|---|---|---|
| static | 717‰ | 53,057 | 3.8× | 8.0 | 0‰ | 8.0 | 38 |
| homeostat | 679‰ | 55,519 | 3.4× | **6.0** | **580‰** | 6.0 | 42 |

**G2 FAIL.** The liar is *partially* demoted (T2 6.0 vs floor 4.0 available, pinned ≤5 only 58%
of the late window) but T1 comes down with it (6.0 < 7.0) — the rule cannot tell "T2 lies" from
"the pair disagrees," which is exactly the w1≡w2 identity's shadow: lag fixes *when* to compare,
not *whom* to blame when signs conflict in a conflict regime.

### Whistle (G3)

Homeostat lie/honest cancel ratio mean **3.4×** (3.7/3.8/3.2/2.9/3.6 per seed); static baseline
3.8×. **G3 PASS** — the F6 whistle replicates under the homeostat and keeps firing.

### Secondary

- Noisy-T2 stress: homeostat 521‰ vs static 569‰, debt 62,734 vs 60,358 — homeostat *hurts*
  here too (end-trust (4,4)-ish); noisy T2 at ±14 against Δ=12 trips both twins' signs
  constantly, and the rule demotes the honest twin alongside.
- Calm (K=8 artifact regime): homeostat 114‰ vs static 421‰ — the F17 calm collapse survives
  the repair; decay-toward-8 cannot outrun sign-conflict evidence in a regime whose honest
  dynamic is turn-taking (F16's antiphase).

## Decision-rule evaluation

- G1 honest ≥800‰: **FAIL** (778‰)
- G2 demotion: **FAIL** (T2 6.0 > 5.0; floor 580‰ < 900‰; T1 6.0 < 7.0)
- G3 whistle ≥2×: **PASS** (3.4×)

## Verdict

**DEMOTE — cofire to v2, charter failure mode (c).** The §3.2 demo runs **selection-only
learning**. The composite repair bounded the failure (308‰→778‰ honest stress; no deafness
collapse) but failed both pre-registered gates it exists to pass, and the mechanism is now sharp:
**lag structure fixes credit timing (F21 confirmed in-run), but cofire *sign-agreement* is the
wrong predicate wherever honest twins are antagonists** — which is what a conflict regime makes
them (F8's 22% same-tick opposite-sign was the tell). Bounded trust converts deafness-collapse
into floor-bleed, not discrimination. The whistle is vindicated as the fault signal that *does*
work (3.4× under the very arm it must monitor).

Implications banked:
- §3.2 demo arm: superposition + lag blade/compensator (F19) + whistle tripwire (T3) — no trust
  learning in the control path; the whistle stays as monitor-only.
- Cofire v2 must find a predicate that is agreement-*asymmetric* (whom-to-blame), not merely
  lag-aligned: candidate is outcome-conditioned vindication (kimi #1's floor/decay variant B
  direction) or per-twin private channel quality (opencode's pm_true style) — Q2 stays open.

Scars booked:
- The lagged cofire rule demotes honest twins in conflict (778 vs 830‰) — any v2 design must
  show an honest-antagonist no-bleed bound, not just boundedness.
- My G2 floor metric (trust ≤5, not ==4) was the right call: T2 never reaches the floor 4.0 on
  any seed in the late window — partial demotion only.
- Calm collapse is regime-deep (114‰), not parameter-deep: the same code that holds 778‰ stress
  fails calm — turn-taking honest dynamics are poison to sign-coincidence trust everywhere.

Canaries: F17 anchors exact (830/308/5 + trust pairs); lag blade 2/2 exact; mislabeled-arm
self-canary CAUGHT; double-run byte-identical. 4/4.

## Cofire v2 charter (EXPERT nudge 2026-09-03, ACCEPTED): predictability, not agreement

The post-mortem above names the kill and then doesn't take the shot. Taken.
**The v2 predicate is lagged cross-PREDICTION, not agreement.** In a conflict
regime honest antagonists are perfectly *predictable* antagonists: twin i's
trigger at t−lag predicts twin j's at t with a stable correlation — whose sign
may be negative, and that's fine. A liar breaks predictability, not agreement.
So the trust update scores online windowed correlation of (i@t−lag, j@t) —
sign and/or magnitude — and demotes on UNPREDICTABILITY: disagreement with a
stable negative correlation keeps trust; noise or inversion kills it. This
keeps F21's lag (the only ingredient ever shown discriminative) and discards
the assumption that killed G1/G2 (honest = agreeing).

Spec points (binding):

- **(a) Integer-friendly online correlation.** No float division in the
  fabric. Candidate: per-pair sign-product accumulator with exponential
  decay — `s ← s − (s>>D) + sign(i@t−lag)·sign(j@t)`; trust maps from
  |s| (predictable at either sign) and demotion from |s| collapsing toward
  0 under liars. D (decay rate) and the window equivalent are pre-registered
  per seed-set before the run; the accumulator saturates at the same width
  discipline as the wsum path.
- **(b) Kinship for the writeup.** This is zeroclaw's reader-delta doctrine
  (Reading 2) at twin scale: judge the OTHER's drift against what your
  reading of them predicts — not against agreement. Cross-reference
  SuperInstance/zeroclaw-dissertation thesis v2 when writing §3.2's
  rationale; same shape, different substrate.

Pre-registered gates for the v2 probe (replacing G1/G2; G3 whistle stays):

- **G1′** honest-antagonist NO-BLEED: clean stress mean ≥800‰ AND end-trust
  mean ≥7.0 (the scar above demands the no-bleed bound explicitly).
- **G2′** liar demotion to floor: lying-T2 late-window trust at floor on
  ≥900‰ of ticks, T1 trust ≥7.0 (discrimination, not bleed-through).
- **G4** negative-correlation preservation (new, the predicate's whole
  point): an honest pair measured with stable negative lagged correlation
  (|s| above the stability band) ends the run at INIT trust, not floor.

**One-line falsifier:** if predictability-based trust also bleeds on honest
antagonists (|s| estimates too noisy at honest SNR to separate stable-
negative from noise within the window), the ENTIRE trust-learning family
demotes to monitor-only — whistle stays, learning leaves the control path
permanently, and §3.2 runs selection-only as already booked.
