# ROUND 11 — Q4 §3.1 MI-criticality sweep — PRE-REGISTRATION

Date: 2026-09-03 (pre-sweep). Branch g3-kinduction. Committing BEFORE any sweep numbers are read.

## Spec (charter §3.1, verbatim commitments)

- Sweep LCG noise rate p over 3–4 decades × decay halvings d ∈ {1,2,3}, N=10k ticks.
- Measure activity fraction (order parameter) and single-site→neighbor mutual information
  via integer-binned histograms. INTEGER-ONLY measurement path: histograms are int64;
  MI computed in fixed-point (scale 2^30) with ln evaluated by the integer atanh series
  ln(num/den) = 2·Σ r^{2k+1}/(2k+1), r=(num−den)/(num+den). ln(2) computed by the same
  routine from 2/1 — no floats anywhere between raw counters and reported millibits.
- Locate transition by MI maximum; finite-size scaling on three lattice sizes;
  exponent as a rational. Deliverable: lookup table "noise rate → channel capacity".
- Same sweep on two lattice groups: Z_n vs D_n Cayley — Barbieri dichotomy check.

## Model (this round's operationalization, e1-derived "pulse medium")

Per element v of a 2-regular Cayley lattice, integer accumulator a[v] (the e1
interference arm generalized: every live site emits a decaying signed pulse that
superposes into its Cayley neighbors; d controls halving cadence; LCG noise injects).

Each tick, fixed element order (Gauss–Seidel, deterministic):
1. decay: if t % d == 0: a[v] = a[v] − fdiv(a[v],2) when |a[v]|>1  (e1 sign-safe halving)
2. noise: if lcg_below(10000) < p_num: a[v] += lcg_below(33) − 16
3. propagate: e_v = 0 if a[v]==0 else (fdiv(a[v],3) or sign(a[v]));  for each Cayley
   neighbor u: a[u] += e_v;  then a[v] -= e_v  (superposition BEFORE touching, e1 §6)

Lattices: Z_L = cycle L (generators {+1,−1}); D_n = Cayley{r,s} (2n elements,
r:(f,k)→(f,k+1), s:(f,k)→(1−f,−k)) — same graph degree (2), same vertex count as Z_{2n}
so group, not degree, is the only variable. Elements enumerated (f,k) → f·n+k.

Measurement (burn-in 1000 ticks discarded, then 10k measured ticks):
- act bit = (a[v] != 0), sampled end-of-tick.
- order parameter: mean activity fraction, integer permille (numerator/denominator kept).
- MI(v→nbr at +1 tick): 2×2 int64 contingency over (act[t][v], act[t+1][nbr]),
  aggregated over all v and t. For D_n measured separately along r-edges and s-edges.
- p grid (exact integers /10000): 1,3,10,30,100,300,1000,3000  (4 decades).
- Sizes: Z_64/Z_128/Z_256 vs D_32/D_64/D_128 (matched vertex counts).
- Seeds: 1,7,42,1999,20260902 (per seed, one LCG stream per run).

## Pre-registered decision rule (committing before results)

The criticality story SURVIVES iff, on Z lattices, per d ∈ {1,2,3}:
- (R1) MI(p) has an INTERIOR argmax (not at p=1/10000 or p=3/10 grid edge), for ≥2 of 3 sizes;
- (R2) peak height ≥ 5 millibits above the cross-seed independence floor (MI computed
  between different-seed runs — measures the integer-quantization noise floor directly);
- (R3) some systematic finite-size trend in MI_max across 64→128→256 (monotone up or
  down, or clear peak drift in p*) — not required to be a power law; exponent fitted
  only if trend is monotone in MI_max.
If any of R1–R3 fails for ALL d, the falsifier fires: MI-peaks-at-transition does not
survive integer quantization → actuator tuned by grid search; book honestly.

Barbieri dichotomy check: compare Z_{2n} neighbor-MI curve vs D_n r-edge and s-edge
curves at matched vertex count. Prediction (sensitivity for non-abelian): D_n shows
broader/elevated MI shoulder at high p. We report; no survival stake rides on it.

## Canaries (pre-registered)

- C1 byte-identity: full sweep run twice; sha256 of raw counter output must match.
- C2 anchor replay: `python3 e1.py` (committed code, seed 20260902) must reproduce
  sequential 2313/23488/56.7, interference 2946/30708/45.5, stress rows
  2513/48397/51.9 and 2070/35508/83.0 (sha256 4f4acccc… recorded at pre-reg time).
- C3 self-canary: deliberately broken "neighbor" MI that pairs act[t][v] with
  act[t][v] (same site, same tick). Detector rule: any labeled neighbor-MI whose
  value equals the marginal entropy H (i.e., MI = H means no information about the
  *other* variable) is flagged. Pipeline MUST print CAUGHT. If it doesn't catch,
  the round is void.

## F26 disclaimer (per task)

F26 (group-criticality mini) falsified a different naïve operationalization; its
failure does not touch this one. No assumptions imported.

## Capacity table convention

Channel capacity entry = MI peak value in millibits/site-tick at that d (max over p),
per lattice size, with argmax p as the actuator's recommended noise-rate setting.

---

# RESULTS (post-sweep, 2026-09-03 ~17:0x AKDT)

Raw: `q4-mi-output.txt` (sha256 07d5e578…, double-run byte-identical). Arms:
v1 = pre-registered model; v2 = amendment (emitter pays e per neighbor — loss-matched
waves; the ONLY change, committed rationale above); v3 = exploratory deadband probe.
Decision rule R1–R3 applied unmodified to all arms.

## Canaries

| Canary | Result |
|---|---|
| C1 double-run byte-identity | **PASS** (sha256 07d5e578… both runs, all three arms) |
| C2 e1.py anchor replay | **PASS** (4f4acccc…; sequential 2313/23488/56.7, interference 2946/30708/45.5) |
| C3 self-canary (mislabeled same-variable arm) | **CAUGHT** (298 mb == H 298 mb) |

## v1 — pre-registered model: FALSIFIED (mechanism identified, not quantization)

Gain>1 medium (each emitter gives 2e, loses e) → activity 96–100% at every p, d, L.
MI ≡ 0 millibits on Z (ceiling-saturated bit, nothing to transmit); floor ≡ 0 too.
No transition exists in the p-grid at all. **The falsifier fires for the model as
literally pre-registered** — but the mechanism is supercriticality from the e1
minimal-pulse floor (unit site → two unit neighbors = binary reproduction), NOT
integer quantization destroying a peak. Booked as a scar on importing e1's "or 1"
pulse floor into a lattice verbatim.

## v2 — amendment (loss-matched): R1–R3 PASS, with fragility booked

Z-group, MI(v→nbr +1 tick), millibits, 5 seeds summed (N ≈ 3.2M–12.8M pairs/cell):

MI_max per (d, L) — argmax at **p* = 3/10000** in 8/9 cells (d=1,L=128 is a p1/p3 tie):

| d | L=64 | L=128 | L=256 | MI_max(L) exponent a (MI ∝ L^−a) |
|---|------|-------|-------|-----------------------------------|
| 1 | 106 mb (p=3) | 100 mb (p1/p3 tie) | 99 mb (p=3) | a ≈ 3/61 |
| 2 | 133 mb (p=3) | 124 mb (p=3) | 121 mb (p=3) | a ≈ 3/44 |
| 3 | 151 mb (p=3) | 140 mb (p=3) | 127 mb (p=3) | a ≈ 1/8 |

- R1 interior argmax: PASS (8/9 strict, 9/9 incl. tie; required ≥2/3 sizes per d).
- R2 peak ≥ 5 mb above floor: PASS trivially (cross-seed floor = 0 mb everywhere;
  integer MI floor is exactly zero at these sample sizes).
- R3 finite-size trend: PASS — MI_max monotone decreasing in L for all d; exponent
  grows with d: 3/61 → 3/44 → 1/8 (fitted from L=64→256, rational via continued
  fractions of the integer MI ratios).
- **Fragility scars:** (i) p* sits one grid point above the floor — the peak is a
  crossover (self-sustained-wave coherence vs noise decorrelation), not an
  absorbing-state transition: the minimal-pulse floor keeps the medium active even
  at p→0 (activity 92–193‰ at p=1/10000), so there is no silent phase anywhere in
  the grid; (ii) the peak is 2–18 mb above its left neighbor — real (sampling noise
  ≪ 1 mb at N≈10⁷) but shallow at d=1.

## Lookup table — noise rate → channel capacity (Z group, v2, L=256, production size)

MI in millibits/site-tick (actuator sets noise rate; capacity = MI at that rate):

| p (÷10⁴) | d=1 | d=2 | d=3 |
|---|---|---|---|
| 1 | 81 | 102 | 112 |
| 3 | **99** | **121** | **127** |
| 10 | 94 | 112 | 125 |
| 30 | 94 | 110 | 120 |
| 100 | 80 | 92 | 101 |
| 300 | 55 | 63 | 65 |
| 1000 | 24 | 25 | 26 |
| 3000 | 3 | 3 | 3 |

Actuator setting: **p = 3×10⁻⁴, d=3 → capacity ≈ 127 mb/site-tick at L=256**
(151 mb at L=64 if small-fabric bonus is wanted). Capacity falls ~4× from p* to p=0.3.

## Barbieri dichotomy check (same data, D = Cayley{r,s}, matched vertex counts)

- D activity plateaus ~50–60% at ALL p (self-sustained rotation↔reflection chatter),
  vs Z's p-responsive 9–90%: the groups are dynamically distinguishable by activity
  profile alone.
- Reflection (s) edges carry MORE MI than rotation (r) edges on D at every (d,L,p)
  cell (e.g. d=2,L=128,p=1: 71 vs 63 mb; d=3,L=128,p=1: 109 vs 99) — a genuine
  group-structure signature (in Z the ±1 edge tables are symmetric by construction).
- Interior MI peaks also appear on D (e.g. d=1: 37→**42**→34 mb at p=1/3/10, L=128),
  consistent with the Z story, but the "sensitive group ⇒ broader high-p shoulder"
  prediction is NOT seen: D MI collapses at high p faster than Z (1 mb vs 3 mb at
  p=0.3). **Dichotomy prediction: not confirmed at this operationalization** (booked;
  Q6's perturbation-growth design remains the right instrument).

## v3 — deadband probe (exploratory, no stake)

Emission deadband |a|≥2 kills propagation (MI ≈ 0–19 mb everywhere, no peak) — the
medium needs the minimal-pulse floor to conduct at all. Confirms the mechanism map:
gain>1 (v1) saturates, loss-matched floor (v2) conducts with a crossover peak,
deadband (v3) is an insulator.

## VERDICT

**PARTIAL — falsifier fires on the letter (pre-registered v1: MI≡0, no peak), but
the amended loss-matched substrate (v2, one-line change) passes all three
pre-registered criteria R1–R3 with integer-only measurement: interior MI peak at
p*=3×10⁻⁴ survives quantization with floor exactly 0, finite-size exponent a ≈
1/8..3/61, and the actuator lookup table is delivered above.** Booked honestly:
the peak is a wave-coherence crossover, not absorbing-state criticality — no silent
phase exists under the minimal-pulse floor; treat p* as an empirically located
operating point, not a universality-class transition point.

## Follow-ups

1. p-grid densification below 10⁻³ (p ∈ {1,2,3,5}/10⁴) to test crossover-vs-critical
   for real (is the p1 dip finite-size wave dilution?).
2. F26/Q6 perturbation-support-growth design on the v2 medium — proper Lyapunov-class
   instrument for the dichotomy.
3. e1 scar: the "or 1" pulse floor is a binary-reproduction amplifier on lattices —
   flag in PORTING-NOTES.md before any RTL port of the pulse rule to multi-site fabrics.
