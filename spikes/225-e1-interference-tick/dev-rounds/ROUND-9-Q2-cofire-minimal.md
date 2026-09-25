# Round 9 — Q2 minimal cofire homeostat (v2 charter predicate)

Date: 2026-09-03 ~14:5x AKDT · branch `g3-kinduction` · harness `dev-rounds/q2_cofire_minimal.py`
(reuses `o6_cofire_homeostat.py` fabric/canaries verbatim via import — harness semantics not forked)
· raw output `dev-rounds/q2-cofire-minimal-output.txt`

## Hypothesis (pre-registered, agenda §6 Q2 + v2 charter @ 987d6e4)

The v2 **predictability-not-agreement** predicate — per-pair integer sign-product accumulator
`s ← s − (s>>D) + sign(i@t)·sign(j@t−lag)`, trust from |s| (predictable at either sign),
demotion on |s|→0 — preserves honest-antagonist residency (G1′: ≥800‰ AND end-trust ≥7.0),
demotes a liar to floor while sparing the honest twin (G2′: floor-frac ≥900‰, T1 ≥7.0), and
keeps stable negative correlation at init trust (G4). Constants pre-registered before the run:
D=6, SAT=128, HI=48, LO=12, trust [4,12] init 8, neutral-decay 32 ticks. Two lane variants from
round 6: **v2b** refractory window R=4 (glm-1 C), **v2c** asymmetric slow descent SLOW=2
(kimi #1 variant-B flavor). Decision rule: any variant passing G1′+G2′+G4 ⇒ promote with spec;
all fail ⇒ book "every local no-error-signal rule on the correction channel learns silence."

## Setup

Seeds (1, 7, 42, 1999, 20260902), 4800 ticks, integer-only, LCG fixed, dedicated fault RNG
stream. Stress Δ=12/drift=6/K=4/pd=3/lat2=10; calm Δ=6/drift=3/K=8/pd=3/lat2=5. Faults: clean,
noisy-T2 (±14), lying-T2 (+24, ticks [1200,2400)). Lag from the first-difference blade (S2
doctrine). Canaries: F17 anchor replay (kimi fabric imported from O6 harness), lag blade
exactness, mislabeled-arm self-canary, double-run byte-identity.

## Results

### Canaries — 4/4

F17 anchor **exact** (fixed 830‰, trust-A 308‰, cancel 5; final trust pairs match the sheet
row). Lag blade 5/5 and 10/10 exact. Self-canary (lie-static mislabeled v2a) CAUGHT on
fingerprint. Double-run byte-identical (sha 62694458fc87f90b both runs).

### Clean honest twins (stress, primary)

| arm | pm mean | debt | cancel | end-trust mean | s_end mean | band-frac |
|---|---|---|---|---|---|---|
| static | **830‰** | 34,995 | 70 | 8.0 | 0 | — |
| v2a charter | 761‰ | 39,136 | 120 | 5.0 | −1 | **0‰** |
| v2b refractory | 795‰ | 37,900 | 75 | 6.5 | −1 | **0‰** |
| v2c slowfloor | 784‰ | 37,668 | 104 | 6.0 | −1 | **0‰** |

**G1′ FAIL everywhere.** Headline mechanism: **the sign-product accumulator never leaves the
noise band on honest pairs** — |s| ends at ~1 vs the HI=48 predictability band on **100% of
final-window ticks, all variants, all seeds**. Honest lagged trigger-sign correlation is too
sparse/noisy at this SNR and grain to separate stable-negative from zero: both twins sit mostly
in the dead zone, drift to floor via neutral decay + occasional LO hits, and bleed 830→761–795‰.
G4 fails for the same reason (band-frac 0‰ < 500‰): negative correlation is *present in sign*
(s_end −1) but never *measurably stable* in |s|.

### Lying-T2 (stress)

| arm | pm | whistle | T2 late trust | floor-frac | T1 late trust |
|---|---|---|---|---|---|
| static | 717‰ | 3.8× | 8.0 | 0‰ | 8.0 |
| v2a | 659‰ | 2.2× | 4.3 | **911‰** | **4.3** |
| v2b | 692‰ | 4.0× | 7.5 | 56‰ | 7.8 |
| v2c | 676‰ | 2.8× | 4.3 | **898‰** | **4.3** |

**G2′ FAIL everywhere.** v2a/v2c pin T2 at ≤5 on ~910‰ of late-window ticks — nominally at the
floor — **but T1 comes down with it (4.3 < 7.0)**: the accumulator cannot tell "T2 lies" from
"the pair is unpredictable," because a lying reference corrupts *both* per-pair accumulators.
This is the w1≡w2 identity's shadow at one lag remove: lag fixes *when* to compare, and
predictability fixes *what* counts as evidence, but nothing local fixes **whom** to blame —
both accumulators share the corrupted channel. v2b spares T1 (7.8) precisely by suppressing the
evidence that would demote anyone — it demotes no one (floor 56‰), re-learning round-6's
"refractory buys honesty by buying blindness."

### Secondary

- Noisy-T2 stress: all variants *hurt* (v2a 509‰ vs static 569‰ mean; end-trust
  pinned (4,4) — both twins demoted by ±14 noise at Δ=12).
- Calm (K=8 artifact regime): collapse *deepens* — v2a 110‰, v2c 111‰, v2b 173‰ vs static
  421‰ (round 6's homeostat scored 114‰). Turn-taking honest dynamics are poison to
  sign-prediction trust everywhere; predictability does not rescue calm.

## Decision-rule evaluation

- G1′ honest no-bleed ≥800‰ + trust ≥7: **FAIL** (best 795‰ / trust 6.5 — v2b)
- G2′ liar to floor ≥900‰ + T1 ≥7.0: **FAIL** (best floor-with-T1-spared: 56‰ — v2b; best
  floor 911‰ has T1 = 4.3)
- G4 negative-correlation preserved: **FAIL** (band-frac 0‰ vs ≥500‰, all variants)
- G3 whistle cross-check: fires 2.2–4.0× under every learning arm — the monitor works.

## Verdict

**Q2 BOOKED — every local no-error-signal rule on the correction channel learns silence.**
The v2 charter falsifier fired *verbatim*: "|s| estimates too noisy at honest SNR to separate
stable-negative from noise within the window" — measured at 0/5000 variant×seed ticks above the
predictability band. Predictability-not-agreement fixed the *predicate's philosophy* (round-6
scar) but not its *statistics*: at trigger-sign grain the honest signal never accumulates, and
the only arm that spares the honest twin does so by refusing to learn. **The trust-learning
family demotes to monitor-only permanently; the whistle (T3) stays as the fault signal that
does work (2.2–4.0× under the arms it monitors); §3.2 runs selection-only learning as booked in
round 6.** Three rounds, three families falsified (v1.1 sign-agreement, v1.1+lag, v2
sign-prediction ×3 variants) — the no-error-signal obstruction is now a *result*, not a gap.

Headline number: honest stress best 795‰ (v2b) vs 830‰ static and 800‰ gate; predictability
band reached on 0‰ of honest ticks.

Scars booked:
- Sign-product |s| at trigger-sign grain is the wrong statistic, not just the wrong threshold:
  honest evidence density (both twins triggered at exactly lag separation) is too sparse for
  any D ≤ 6 window to integrate before decay erases it. A v3 would need magnitude-weighted or
  error-derived features — which is an error signal, i.e. outside the no-error-signal family.
- Demotion-without-discrimination is the family signature: every rule that pins the liar
  (v2a/v2c, 911/898‰) also pins the honest twin (4.3); every rule that spares the honest twin
  (v2b, 7.8) spares the liar (56‰ floor). The frontier is a trade-off curve, not a corner.
- Calm collapse is predicate-independent (110–173‰ across agreement AND prediction rules):
  turn-taking regimes defeat *any* sign-coincidence trust; do not re-test calm without a
  fundamentally different feature.
- Round-6's "bounded trust converts deafness-collapse into floor-bleed" generalizes: bounded
  trust converts *every* collapse into slow floor-bleed. Boundedness bounds the damage, never
  the misattribution.
- Renderer scar: lie-window metrics divide by max(1,n) — print "0.0" artifacts when no lie
  window applies (fixed for noisy arm this round; check any reuse).
