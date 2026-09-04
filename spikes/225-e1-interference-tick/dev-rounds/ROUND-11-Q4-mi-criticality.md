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
