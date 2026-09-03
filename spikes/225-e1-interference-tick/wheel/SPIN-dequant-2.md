# SPIN-dequant-2 — §10 cheat-code probes: Grover-curve, thermodynamic arm, snap-point search

*Wheel spoke 8 (DEQUANT), spin 2. Casey directive 2026-09-02 22:18: "keep going on
our post-quantum work." Script: `wheel/spin_dequant2.py` (run `python3 spin_dequant2.py all`,
~11 s). Integer-only — per-mille everywhere, no floats in any instrument loop.
Fixed seeds (1, 7, 42, 1999, 20260902). The instrumented port reproduces
`e1.run()` counters **byte-identically** on both modes × both regimes × all seeds
before any arm ran (VALIDATE: PASS). Not committed.*

Charter §10 claims three cheats: (1) re-aim at snap points, (2) integer
superposition for interference statistics, (3) thermodynamic sampling without
coherence. This spin puts measured edges on all three — including one result
that **revises E1's own headline** (§3.4 below) and one clean negative for
cheat #3 (§2).

---

## 1. INTERFERENCE-AS-GROVER-CURVE — the analogy's speed story is decorative; its "amplitudes add" core is load-bearing

**Mechanism.** Two probes. (a) *Displacement response*: displace g by +E0 from
truth (single twin, delta=12, drift=3, K=8, div=3), measure ticks-to-deadband T
for sequential-snap, interference, and a unit-step deadband-scan null; compare
against the Grover curve T_G = ⌊(π/4)·√N⌋+1 with N = E0/delta (the only integer
"search space" the substrate offers). (b) *Direction amplification*: in the real
conflict harness, measure per-event applied mass directed toward CURRENT truth
(signed by T1's error), plus per-tick correction velocity v_j as a trigger
streak deepens (the "amplitude ramp" as pulses stack).

**1a. Ticks-to-deadband (drift=3; drift=6 shifts nothing material):**

```
   E0    N  T_seq T_scan  T_int (5 seeds)      T_grover  flips  delivered/E0
   24    2     1      1  [2,2,2,2,1]                1      0     608 permille
   48    4     1      3  [3,3,3,3,2]                2      0     904
   96    8     1      6  [3,3,3,3,3]                2      0     979
  192   16     1     13  [3,3,3,3,3]                4      0     991
  384   32     1     27  [3,3,3,3,3]                4      0    1002
  768   64     1     55  [3,3,3,3,3]                7      0    1005
 1536  128     1    116  [8,3,8,8,8]                9      4    1269
 3072  256     1    254  [14,13,13,14,13]          13     10    1400
```

- Interference is **flat at 3 ticks through N=64** (log-like, beats √N), ties
  Grover near N≈256, and never touches the scan's linear 254. The sequential
  snap is **1 tick at every N**.
- **The wave's mass ledger closes**: delivered motion = 979–1007‰ of E0 for
  N ≤ 64 — the pulse machinery delivers almost exactly the displacement, no
  more. Above N≈128 the stacked tails outrun the error (delivered 127–140%,
  2 sign-flips per run) — damped ringing, not oscillation.

**Velocity ramp (the "amplitude grows" claim, measured):** per-tick corrected
fraction of the *current* error, by tick j after displacement:
`f = 332‰ → 581‰ → 1024‰` (j=0,1,2). Superposition accumulation is real and
steep — three stacked pulse-generations more than triple the per-tick
amplitude, and j=2 exceeding 1000‰ is precisely where overshoot begins.

**1b. Direction amplification in the conflict harness (5-seed, applied mass
directed toward current truth):**

```
                        sequential      interference(div3,K8-home)  interference(div2,K1)
 default  directed-mass     745 permille       778 permille            956 permille
          neg-direction      131 permille                                33 permille
 stress   directed-mass     656                 702                      695
```
Sequential splits exactly by source: T1-snaps are 1000‰ directed by
construction; **T2-snaps (stale twin) are 95‰ (default) / 134‰ (stress)** —
the snap chases stale data nearly orthogonal to current truth. Streak
velocities: interference ramps j0:76‰ → j5:528‰ as pulses stack (default);
stress streak onsets average **−23‰** (net briefly *away* from truth — the
cancellation state) before climbing.

**Where the analogy BREAKS — booked precisely:**
1. **No speedup to explain.** The trivial snap is 1 tick at every N. Any
   first-order damped controller beats √N here; "quadratic speedup" solves a
   problem (unstructured search among symmetric candidates) this substrate
   does not have. The Grover column crosses the measured curve by accident of
   log-vs-sqrt.
2. **No rotation.** Grover's sin((2j+1)θ) rotates — amplitude rises, peaks,
   *falls periodically*, and must be stopped exactly. The fabric's ramp
   saturates at a DC gain and self-terminates at the deadband; the only
   "over-peak" behavior (N≥128) is damped ringing, never periodic. There is
   no integer N anywhere in the harness that plays the role √N plays.
3. **What survives is not amplification but directional low-pass.** The
   load-bearing fact is that superposed partial corrections *amplify the
   consensus direction and damp the stale direction* (956‰ vs 745‰ directed;
   33‰ vs 131‰ negative-direction events) — expressible in one integer line
   (`g += Σ eᵢ // div`) with no coherence, no phase, no interference fringes.

**Verdict:** "amplitudes add" — load-bearing (ramp 332→581→1024‰ measured;
cross-twin cancellation states real). "Amplitude amplification / sqrt
speedup" — decorative on every axis measurable here.

---

## 2. THE THERMODYNAMIC ARM — clean negative: the sum beats the sample at every temperature

**Mechanism.** Identical tick; instead of `g += net` (cold = deterministic
sum), apply ONE pulse drawn from the pre-decay ensemble: warm = weighted by
|pulse|, hot = uniform over pulses. Sampling stream = separate LCG(seed+1),
draws at bit ≥11 (dodges the pinned LCG's period-2 low bit — glm-2's booking);
drift stream untouched, so cold is byte-identical to the e1 reference.

```
regime        arm     events   debt    pm   maxE  canc  chat  stalls  settles/MegaDebt
default       cold     3081  32143   422    37   520  1952     321        63049
(d6,dr3,K8)   warm     4239  50508   413    46    63  3012       0        39288
              hot      6631 108356   183    62    30  3958       0         8113
stress        cold     2041  34995   830    39    70   889      33       113974
(d12,dr6,K4)  warm     2312  41258   800    53    15  1252       0        93179
              hot      2839  55227   649    63    10  1817       0        56439
deep-conflict cold     2696  58232   714    43   220  1499      38        58878
(d16,dr8,K6)  warm     2870  64997   670    64   151  1802       0        49509
              hot      3534  92468   442    76    83  2556       0        22963
```

- **Warm never beats cold** on settles or settles-per-debt at any regime
  (5-seed means). Per-seed: warm>cold 0/5 stress, 0/5 deep, 2/5 default
  (means still favor cold 422 vs 413). Temperature is **strictly ordered**
  cold > warm > hot on pm in all three regimes — performance degrades
  monotonically with sampling temperature.
- Re-run at the champion operating point div2/K1 (§3): cold 980/959/859 vs
  warm 971/956/857 — margins 3–9‰ (noise), but maxErr jumps 27→48: sampling
  only fattens the tail.
- **The mechanism-level reason, booked:** cold *does* deadlock — 321
  coherence-stall ticks per default run (trigger fired, net==0, g frozen).
  Warm eliminates stalls by construction (a sample is never zero) — and still
  loses. The deadlock ticks are not where the cost lives, because the twin
  pull landscape here is 1-D and quasi-convex toward the reset direction: the
  ensemble's **expectation already sits at the best available reset**, so
  sampling can only add variance. This extends the known boundary
  (arXiv:2608.09743, noise redundant on convex problems) to E1's conflict
  substrate at all three temperatures. §10 cheat #3 has **no measured point**
  on this harness; the honest escape hatch that remains is a genuinely
  multi-modal pull geometry (deadlock rings), which E1 does not instantiate.
- **Instrument scar, booked:** v1 of this experiment passed the arm name
  `"cold"` where the apply-mode `"sum"` was expected — the "cold" row silently
  ran hot sampling, and the buggy table showed warm *beating* "cold"
  everywhere: a manufactured §10-positive. Caught by the tell that cold and
  hot rows were digit-identical. Lesson (adds to glm-2's self-canary list):
  **a name-to-config mapping must be explicit, and identical rows across
  supposedly different arms is a map bug until proven otherwise.**

---

## 3. SNAP-POINT RE-AIM AS SEARCH — the snap point is computable, sample-access suffices, and sliding alone can trap

Grid: pulse_div ∈ 1..8 × K ∈ 1..12 (96 cells) × 5 seeds × 4800 ticks, both
regimes. Objective: pm (per-mille ticks within deadband of both twins).

**3.1 The landscape.** Global best: **div=2, K=1** in BOTH regimes (959
stress / 980 default). Strict local optima: 2 (stress), 1 (default). Cliff
edge at div=1/K=1: superposition without damping diverges (debt 3.52M,
maxE 1158 — the ping-pong null).

**3.2 Search economy (queries-to-target vs 96-cell exhaustive):**

```
full-grid slide (steepest ascent):  evals 5–46 of 96; global seat from 4/6
                                   starts (default), 2/6 (stress); traps:
                                   div3K2 (921) and div2K10 (803/731) locals
probe slide (600-tick samples = 1/8 cost each) + one full confirm:
                                   total cost 16–49 permille of exhaustive;
                                   probe-vs-full pair concordance 952 permille
                                   (stress) / 964 (default) over 528 pairs;
                                   probe argmax == full argmax, both regimes
```

**3.3 Zero-query prediction.** The pinned decay gives an exact integer
delivery identity — `delivered(m, K) = Σ decay-chain` (m=1..12, K=8:
8, 9, 11, 12, 15, 16, 18, 19, 23, 24, 26, 27; note +23 vs −20 for m=9 — the
pinned floor-decay is sign-asymmetric on odd magnitudes, a real substrate
bias, booked not fixed). The no-overshoot condition
`delivered(E_typ // div, K) ≤ E_typ + delta` predicts **div\* = 2** — an
exact hit on the grid argmax in both regimes, zero queries. It does not
constrain K (the identity is mass-only; K's optimum is the memory boundary,
which mass cannot see).

**Verdict on "the fabric finds snap points without scanning":** three tiers.
(a) **Certified best: the contract computes the snap point** — the delivery
identity lands div\* with no search; this is §3.1-of-the-charter doctrine
(knobs by scaling law) instantiated. (b) **Tang-style sample access works**:
1/8-cost probes rank the grid at 95‰+ concordance and pick the same champion.
(c) **Local sliding alone breaks**: 2–4 of 6 starts trap in locals — a blade
that only slides can miss the global seat; the identity or the sample grid,
not the walk, carries the cheat.

**3.4 The booking that revises E1 itself.** The grid says the celebrated
operating point (div=3, K=8/4) is **interior-dominated by its own memoryless
limit**: div2/K1 beats it on all seven metrics simultaneously in stress (pm
959 vs 830, debt 31.9k vs 35.0k, events 1891 vs 2041, chatter 660 vs 889,
maxE 31 vs 39) — and beats *sequential in the calm regime where the charter
says interference loses*: default pm 980 vs 566, per-seed 5/5 on pm, events,
and debt ("worse at gentle params" is an operating-point artifact, not a
mechanism law). Decomposition: pm is **strictly decreasing in K at fixed
div** (div2 stress: 959→857→805→804→798 for K=1→2→4→8→12; default
980→901→782→747→718). **The load-bearing superposition is WITHIN-tick — the
two twins' pulses summing/cancelling before g moves (averaging). Cross-tick
coherence (the K-tick decay wave, the "state no sequential system can
occupy") has negative marginal payoff on every measured axis of this
harness.** Honest scope: E1's channel (deterministic ramp + iid drift) has no
temporal structure for memory to exploit beyond what averaging already
captures; K>1 earning its keep would need a channel with useful phase.
The 83-vs-52 E1 headline reproduces exactly here (830 vs 513) — but it
understates the mechanism: at the right snap point the same machinery wins
the calm regime too, with less of the wave.

---

## 4. Deliverable — load-bearing vs decorative, as measured boundaries

| §10 element | Verdict | Measured boundary |
|---|---|---|
| "Amplitudes add" (integer superposition) | **LOAD-BEARING** | ramp 332→581→1024‰ in 3 ticks; delivery closes to 979–1007‰ of displacement (N≤64); within-tick twin averaging carries the whole control win (div2K1: 959/980 pm, 5/5 seeds vs sequential incl. calm regime) |
| Direction amplification toward truth | **LOAD-BEARING (reinterpreted)** | directed-mass 956‰ vs sequential 745‰, negative-direction events 33‰ vs 131‰ — but the mechanism is damped consensus, one integer line, no coherence required |
| sqrt / amplitude-amplification speed | **DECORATIVE** | snap = 1 tick at every N; interference is log-flat (3 ticks to N=64), crosses T_G only at N≈256 with damped ringing (flips 0 for N≤64, 2/run at N=256); no rotation, no periodicity, no N |
| Cross-tick wave memory (K-tick coherence) | **DECORATIVE on this harness** | pm strictly decreasing in K both regimes; home config dominated on all 7 metrics by K=1; cancellation states real but anti-correlated with performance here |
| Thermodynamic sampling w/o coherence (cheat #3) | **NO POINT MEASURED** | cold > warm > hot on pm in all 3 regimes and at both operating points; stall-elimination by sampling buys nothing; quasi-convex 1-D pull ⇒ expectation wins; extends 2608.09743's boundary |
| Snap-point re-aim w/o scanning (cheat #1) | **VALIDATED, two ways** | zero-query delivery identity hits div\*=2 exactly (both regimes); 1/8-cost probes rank at 952–964‰ concordance, same argmax; sliding-only traps 2–4/6 starts |

**One-sentence undersell:** on this substrate the quantum analogy's honest
core is *sample-access search over a damped consensus controller* — the
snap point is computable from the delivery identity, short samples rank the
grid, and everything wave-flavored beyond that (sqrt speed, temporal
coherence, thermal sampling) measurably fails to pay.

**Bookings:** (i) exp2 v1 name-map bug (fake warm-beats-cold) — identical
rows across arms is a self-canary; (ii) pinned floor-decay is sign-asymmetric
on odd mags (+23 vs −20 at m=9) — substrate bias, kept per contract;
(iii) LCG draws at bit ≥11 only; (iv) div2/K1 dominance is a statement about
E1's twin channel and its metric, not a general control claim; (v) all
numbers 5-seed, 4800-tick, integer, per-mille.

— dequant lane (zai/glm-5.3), 2026-09-02 22:19 AKDT spin. Not committed.
