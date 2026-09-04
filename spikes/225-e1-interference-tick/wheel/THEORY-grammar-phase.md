# THEORY v1 — Unified Interference Grammar Phase Model
**Date:** 2026-09-03 · **Cycle:** SPIN-11 through SPIN-15 folded · **Status:** PROVEN/MODELED/SPECULATED claims tagged with spinref numbers

---

## Executive Summary

Quilt interference residency is determined by **five co-equal axes** composing with specific rules:

1. **Spread law** — twins decohere at critical latency spread ≈ 0.75·2Δ (rate-limited by echo factor |1−N/pd|)
2. **Grammar law** — fresh-cohort causality + n_f × K interaction (stale-mass nearly fungible)
3. **Phase/sync law** — synchronized duplicates create resonance; one-tick offset cures ∼40%
4. **Memory window** — K-stacked generations pay only where demand (slope σ) matches capacity (decay speed)
5. **Composition law** — mechanisms superadditive iff they attack orthogonal failure channels; subadditive iff substitutes

Three conservation laws hold exactly: **mass closure (Δ=0), debt additivity (Σ twin tolls), pulse evaporation (~0.2/event at expiry)**. Event ceiling is 99.85% occupancy; **debt ceiling exists only under deadband tightening, not drift escalation**.

---

## 1. THE SPREAD LAW REFINED — RATE-LIMITED DIVERGENCE

### Core Claim: Echo-Factor Governs Divergence Speed
**Status: PROVEN** [SPIN-11 EXP1, SPIN-8]

The critical spread where twins decohere is not a fixed line, but a **rate process** determined by the echo factor |1 − N/pd|:

**divergence occurs iff |1 − N/pd| > 1 by enough to outrun decay within the eval window**

At pd=12, N=25 (echo factor 1.08), growth is too slow to escape the basin within 4800 ticks. The familiar "N > 2pd diverges" rule (SPIN-8) describes a *structural necessity* but misses the temporal constraint: even when |1 − N/pd| > 1, divergence requires the overshoot velocity to exceed decay velocity. At pd=12, N=25, it does not.

**Effective scaling (MODELED)** [SPIN-5, SPIN-8]: The critical spread is not the raw 2Δ but **≈ 0.75·2Δ**. At Δ=12, this predicts spread ≈18, close to observed 19.6 (SPIN-5 ladder). The slope model overshoots by ~33%; the effective coefficient is 0.75, reflecting integer division loss (e//3), asymmetric decay dynamics, and feedback settling lag. This lag is **not yet understood** [SPIN-theory scar 1].

**Measured knee (PROVEN)** [SPIN-5, SPIN-4]:
- Onset: spread 14–16 (slope-adjusted 2Δ crossing at Δ=12)
- Steepest drop: 12.9–12.2 pp/unit at spread 14→15
- 50%-crossing: ≈19.6 (K=1) / 19.2 (K=2)
- Sequential arm never crosses 50% out to spread=24 (52.9% at raw 2Δ=24)

**Mechanism (MODELED)** [SPIN-5]:
Interference twins deliver correction e//3 per pulse, decaying over ~5–10 ticks. When twins sit at different latencies, they accumulate asynchronously. Beyond the critical spread, the faster twin overshoots; the slower twin can't catch up within the deadband. The system enters a deadlock cycle. The transition is smooth (~5–6 spread-unit band) because coherence chains of nearby twins (step ≤ delta/2) still couple.

---

## 2. THE WALL LAW: COMPENSATION IS A TRADE, NOT A RESCUE

### Claim: Mass Compensation Narrows Rescue, Hurts Healthy Grammars
**Status: PROVEN** [SPIN-11 EXP2, EXP4]

The wall (divergence at pd=12, N>2pd) can be partially crossed with mass compensation: when divergence is imminent (echo factor |1−N/pd| just barely > 1), the adaptive n_f-scaled correction (MC-A: //min(n_f, pd)) rescues collapsed arms at the edge.

**Rescue magnitude (PROVEN)** [SPIN-11]:
- step5 (0.1% casualty at uncompensated) → 9.1% at delta=24, K=1
- Ladder step1 at N=31: similar narrow rescue

**But cost elsewhere (PROVEN)** [SPIN-11]:
- kcoh5: 53.2% → 37.6% (−15.6pp healthy grammar)
- cohort: 49.3% → 11.4% (−37.9pp)
- ladder: 26.8% → 9.5% (−17.3pp)

Compensation softens *every* shove, including corrective ones. K-interaction reversal shows the same: K=1→K=2 under compensation flips sign for ladder (−14.0 → +2.4) and cohort (−27.5 → +3.6).

**Prediction gate (PROVEN)** [SPIN-11]:
P1 (compensation dominates everywhere): **REJECTED**. P4 (K=2 trough survives): **FAIL** — kcoh5 [53.2, 47.4, 66.6] → [37.6, 47.7, 52.7]; the trough is an unmoderated-shove phenomenon.

**Mixture protection (PROVEN)** [SPIN-11 EXP4]:
In mixed-pd systems, the non-diverging half absorbs the shove. Mix(3,6) edge = 9 > pure pd=3 edge of 7, yet < strongest-member edge of 13. Walls **compose sub-linearly**; a strong-pd minority shields a weak-pd majority.

---

## 3. THE GRAMMAR LAW REFINED — FRESH-COHORT × n_f × K

### Claim: Fresh-count is the Dominant Second Axis; Stale-Mass is Nearly Fungible
**Status: PROVEN** [SPIN-12, SPIN-9]

At fixed spread, the multiset grammar of latency distribution is a second-order dial. SPIN-9 initially confounded fresh-cohort and stale-mass; SPIN-12 decoupled them orthogonally.

**Leave-one-out on additive model (PROVEN)** [SPIN-12]:
- Dropping n_f costs −0.260 R² (0.789 → 0.529)
- Dropping m_s costs only −0.018 (0.789 → 0.771)

At fixed m_s, each added fresh twin (lag ≤ δ) buys residency. At fixed n_f, rearranging stale mass barely matters (≤3pp at K=1–2; coh3_block exception of −9.6pp at K=4 marks where structure starts mattering in high-K regime).

**Winning model: n_f × K interaction (PROVEN)** [SPIN-12, SPIN-9]:
- SPIN-12 G2: R² = 0.891 (beats SPIN-9's confounded 0.877)
- n_f × m_s interaction is noise (+0.005)
- **The K-flip is an interaction with freshness, not a separate axis**

**Fresh-cohort-majority law (PROVEN)** [SPIN-5 topology]:
At spread=15, K=1:
- kcoh5 (5 fresh, 1 stale): 74.1%
- kcoh4 (4 fresh, 2 stale): 62.6%
- kcoh3 (3 fresh, 3 stale): 57.1% ← local minimum (no majority)
- kcoh2 (2 fresh, 4 stale): 64.4%
- kcoh1 (1 fresh, 5 stale): 47.3%

Same multiset sizes mirrored; fresh side is dominant. Residency tracks the *coherent cohort's position* (fresh vs stale), not magnitude alone.

**Extreme-fresh-majority protection (PROVEN)** [SPIN-12]:
Outlier grammars (5 fresh + 1 stale) at K=4 carry protection the additive model can't express. out5_1 residual **+22.4pp** above additive fit. Saturated cell×K ceiling R²=0.940; remaining 6pp is within-cell structure.

**Stale-mass cost estimate (MODELED)** [SPIN-5 grammar sweep]:
Sequential arm (impulse-only, no memory) shows grammar-blindness: cohort ≡ quart ≡ outlier ≡ paired all at **56.8%** at spread=15. The difference (cohort 57.1% vs sequential 56.8%) is only 0.3pp; the 20pp spread between zero (77.3%) and cohort (57.1%) is the pure **cross-cohort staleness disagreement** self-harm. Stale-cohort debt is ≈2× fresh: kcoh1 K=2 carries 483k events vs ladder 260k.

---

## 4. COHERENCE CHAIN LADDER RIDES

### Claim: Graded Staleness Equals Taper-Coherent Group, Not Binary Split
**Status: PROVEN** [SPIN-5 topology, SPIN-8 granularity]

Graded ladder [0,3,6,9,12,15] at spread=15: **71.5%** — exploits the fact that adjacent twins differ by 3 ≤ delta=12, so they remain coherent (synchronized feedback reaches both within one generation of decay, ~e//3 cycle).

**Coherence radius (PROVEN)** [SPIN-8]:
The ladder's step-size rule is **step ≤ delta/2** for coherence. At step=3, delta=12, adjacency holds. At step=5, coherence breaks (exceeds delta/2). The ladder performs better than binary splits (kcoh2 [0,0,15,15,15,15]) because the taper creates a **connected coherence graph** anchored at the fresh end, protecting coherence better than a hard boundary.

---

## 5. SYNC-RESONANCE CHATTER & ANTI-SYNC PHASE CURE

### Claim: Synchronized Duplicates Create Resonance; One-Tick Offset Cures ∼40%
**Status: PROVEN** [SPIN-5, SPIN-10 EXP2 & EXP3, SPIN-14 composition]

**The chatter mechanism (PROVEN)** [SPIN-5]:
At spread=0 (zero-lock), all 6 twins fire simultaneously at every step. 99.84% of consecutive fires flip sign (5058/5066): the arm oscillates on its own echo. All twins read the same residual, all generate correlated corrections that cancel or reinforce together—a classical sampled-system instability.

**Isolated cost (PROVEN)** [SPIN-5, SPIN-10]:
- Zero-lock K=1: **22.7pp self-harm** (77.3% vs sequential 100.0%)
- Zero-lock K=2: **50.0pp self-harm** (50.0% vs 100.0%) — half-decayed prior pulses make resonance worse
- Sequential at spread=0: perfect (100%, only 527 events) — no echo, no memory

**Anti-sync phase cure (PROVEN)** [SPIN-10 EXP2 & EXP3]:
Spread=1 (one-tick phase offset between duplicate classes): **89.3%** (ladder N=6 K=1, 5-seed mean)
- Events collapse 8756 → 5232 on first tick (−40%)
- Debt collapses 187.8k → 87.4k
- **One tick of offset buys 12.0pp residency recovery** — sharp, not gradual

**Phase as a control knob (MODELED)** [SPIN-10]:
This is **phase-lag stabilization** from classical digital control: if both twins fire at the same tick t with residual e, they both generate e//3, summing to ∼2e overshoot. At t+1, the system refires with reversed sign. If one twin lags by one tick, the corrected error from tick t feeds forward into only one twin's decision at t+1, breaking the symmetric oscillation. This is a mode-specific phenomenon; at other grammars (cohort, ladder), residency already spreads corrections, so phase offset has less impact.

**Pattern-blindness of spread≤1 (PROVEN)** [SPIN-10]:
Ring@1 [0,1,0,1,0,1], cohort@1 [0,0,0,1,1,1], ladder@1 [0,1,2,3,4,5] are **byte-identical** (5 seeds × 3 K values). At spread ≤1, pattern grammar doesn't discriminate — **only the offset matters**. Multiset structure becomes irrelevant when twins are too close to separate.

---

## 6. THE MEMORY WINDOW: DEMAND MATCHES CAPACITY

### Claim: K-Stacked Generations Pay Only Where Channel Slope Matches Pulse Decay
**Status: PROVEN** [SPIN-5 novel-N1, with decay-window model MODELED]

Cross-tick wave memory (K>1) is conditional: useful in a narrow velocity window at the wall's edge.

**Three channel regimes (PROVEN)** [SPIN-5]:
| Regime | σ (slope/tick) | K=1 resid | K=8 resid | ΔK | seq |
|---|---|---|---|---|---|
| **Slow** | σ≤2 | 93.8% | 89.0% | −4.8pp | 57.2% |
| **Window** | σ≈3 | **13.9%** | **45.6%** | **+31.7pp** | 52.3% |
| **Fast** | σ≥4 | 5.2% | 7.1% | +1.9pp | 51.5% |

**The slope wall (PROVEN)** [SPIN-5]:
Beyond σ=3 or σ=4, residency drops below 10% for interference regardless of K, while sequential holds 51–52% at the wall and 81.3% far beyond (σ=16). **Factor separation: ∼100× at σ=16** (impulse 81.3% vs interference 0.9%).

**Mechanism (MODELED)** [SPIN-5]:
A twin firing at error e delivers e//3 per pulse, decaying over ∼5–10 ticks. When channel slope σ outruns pulse decay tail, the system can never catch the rising error; the deadband is permanently out of reach. Sequential snapping delivers the full correction in one tick (impulse), independent of channel slope. This is a **finite-velocity-capacity phenomenon**: interference has v_max = f(σ_pulse, K, pd) depending on decay speed and generation count; sequential has v_max = ∞.

**Bandwidth-matching sweet spot (MODELED)** [SPIN-5]:
At σ=3, K=1's single-generation decay can't keep pace (13.9%), but K=8's stacked generations deliver faster correction velocity (45.6%), closing the gap to 31.7pp. Memory pays where **demand ≈ capacity**. The window should slide with delta and pd: if delta increases (tighter deadband, higher demand) or pd decreases (longer decay, higher capacity), the window center shifts. **Full scaling law is open** [theory scar 2].

---

## 7. THE COMPOSITION LAW: ORTHOGONAL CHANNELS SUPERADDITIVE

### Claim: Superadditivity iff Mechanisms Attack Orthogonal Failure Channels
**Status: PROVEN** [SPIN-14, SPIN-10]

Does gain(A) + gain(B) ≤ max(A,B) + 2pp (subadditive), or can mechanisms stack?

**Universal subadditivity FALSIFIED (PROVEN)** [SPIN-14]:
The naive hypothesis was rejected. Zero-lock K=2 composes **superadditively**: 84.9 (AS alone) + 1.6 (N1 alone) → **96.7 joint** (residual +11.9pp). Learned scheduler × AS pair composes superadditively: +35.3 (scheduler gain) + 11.8 (AS gain) → **89.0% cohort8 [0,1,2,6,7,8] + AS @ K=2**, a **new best-known cell** (prior best 79.4 kcoh5@15+AS).

**But N1 memory is subadditive-or-destructive (PROVEN)** [SPIN-14]:
N1 (tri3 channel σ=3) is subadditive in 14/16 mechanism cells, and **every real-grammar cell passes** (all subadditive). Worst: ladder@15 K=1 (−46.0pp). SPIN-10's substitutes-not-complements result **generalizes for the memory channel**.

**Secondary hypothesis FALSIFIED (PROVEN)** [SPIN-14]:
Predicted: AS helps fresh-cohort (kcoh5), memory helps stale-heavy (ladder/cohort). Measured: **AS wins 14/16 cells, N1 wins 0, ties 2** (kcoh5@30 K=1, cohort@30 K=1). The predictor is **failure mode, not grammar class**: N1 is last-resort compensation for synchronized-cohort chatter (the zero-lock K=1 origin, 81.0 → 100.0 with even1), not a stale-grammar rescue.

**Refined composition law (MODELED)** [SPIN-14]:
**Superadditive ⟺ orthogonal failure channels**
- Scheduler (staleness-allocation) × AS (decorrelation): superadditive (+47.2pp stacked to new best)
- AS (decorrelation) × N1 (memory): subadditive-to-destructive (compete in pulse-superposition channel)

**Mechanism value is predictor of failure mode** [SPIN-14]:
- AS: dominates everywhere (knob effectiveness)
- N1: pays only at synchronized chatter origin
- Learned scheduler: staleness remedy at specific K (K=2 rescue via cohort8 parking)

---

## 8. CONSERVATION LAWS — EXACT CLOSURE

### Claim 1: Mass Closure Δ = 0
**Status: VALIDATED (wiring-exact)** [SPIN-15]

emitted_signed == decay_loss + inflight + expired_residual *exactly, every run*

Δ=0 on all 120 runs (6 grammars × K∈{1,2,4,8} × 5 seeds) plus all saturation arms. Honest caveat: emission list and mass counter built in same pass, so this **certifies instrumentation, not harness honesty**. But the fix (SPIN-12 failure post-mortem) was real: pulses whose life expires carry an un-decayed residual that the fabric silently destroys.

### Claim 2: Debt Additivity
**Status: VALIDATED (wiring-exact)** [SPIN-15]

Σ per-twin toll = global debt exactly, every run.

Non-tautological laws (pulse-mass with evaporation, g-trajectory) also close exactly everywhere.

### Claim 3: Expiry Evaporation Channel
**Status: PROVEN** [SPIN-15]

The fabric **EVAPORATES pulse mass at expiry**. |evaporation| ≈ 0.17–0.30 per event, roughly constant across all stress levels (it is the sum of ±1 residuals of dying pulses).

### Claim 4: Toll-per-Event Grammar-Dependence
**Status: FALSIFIED (not invariant)** [SPIN-15]

C3 hypothesis: toll-per-event grammar-invariant at fixed K. **FALSIFIED**. Rel-spread across grammars at fixed K: **29.4–38.1%** (K=1: 18.4→26.9; K=2: 27.4→36.8). Structure found:
- Ranking **STABLE**: ladder@15 minimum, outlier@30 maximum at every K
- **Toll/event tracks stale-mass m_s** (grammar law from SPIN-9/12)
- K=2 **uniform pathology**: +9 to +12 debt/ev over K=1/4/8 for every grammar (resonance between 2-tick pulse life and drift/reality ramp)
- Curious tie: zero ≡ kcoh5@15 at K=1 (both 21.5) despite different event counts — booked as open

### Claim 5: Saturation Cap on Debt
**Status: MIXED** [SPIN-15]

Worst grammar: ladder@30 (12.8% residency at K=4).

**Under drift escalation (arm A drift → 384):**
debt/ev grows 24.5 → 28.5 → 61.0 → 188.1 → 683.2 → 2584.9 → **9202.4** — **NO CEILING, roughly linear beyond drift≈24**. Trigger error scales with drift.

**Event count DOES saturate:** 28,757 events / 28,800 possible = **99.85% occupancy ceiling** (every twin fires nearly every tick).

**Under deadband tightening (arm B delta → 1):**
debt/ev **FALLS** 24.5 → 17.1; total debt **PLATEAUS** at ∼460k — **debt is hard-capped by the deadband itself** (errors can never grow far past delta before re-trigger).

**Headline: The fabric has an EVENT ceiling (99.85% occupancy) but NO debt ceiling under drift escalation**. Debt ceiling exists only under deadband tightening.

---

## 9. FALSIFIABLE PREDICTIONS & CURRENT STATUS

### Tested (SPIN-11 through SPIN-15)

| Prediction | Status | Evidence | Spin |
|---|---|---|---|
| F1a: Coherence-radius scaling (step > delta/2 breaks chain) | PARTIALLY TESTED | ladder step sensitivity found; full *connectivity* law unmeasured | SPIN-8 |
| F1b: Mixture protection (non-diverging half absorbs) | CONFIRMED | mix(3,6) edge 9 vs pure pd=3 edge 7 | SPIN-11 |
| F2: Delta-scaling law (c·Δ constant) | OPEN | Not swept; only delta=12 pin | — |
| F3: Window-center sliding (σ* vs delta, pd) | OPEN | Partial measurement; full grid unmeasured | — |
| F4: K-interaction with fresh-cohort | PARTIALLY TESTED | Inversion measured K=1,2,4,8; mechanism pulse-overlap MODELED not proven | SPIN-9 |
| C1: Mass closure Δ=0 | VALIDATED | 120 runs + saturation arms; wiring-exact | SPIN-15 |
| C2: Debt additivity | VALIDATED | Σ twin-toll = global debt; wiring-exact | SPIN-15 |
| C3: Toll/event grammar-invariant | FALSIFIED | 29–38% spread; stable ranking tracks m_s | SPIN-15 |
| C4: Saturation cap | MIXED | Event 99.85% ceiling; debt unbounded under drift, capped under delta-tightening | SPIN-15 |
| Superadditivity rule | VALIDATED | Orthogonal channels superadditive; same channel subadditive-to-destructive | SPIN-14 |
| N1 substitutes memory | VALIDATED | 14/16 cells subadditive; all real-grammar cells pass | SPIN-14 |

### Untested, Highest-Leverage Claims (Top 5)

1. **Delta-scaling universality (F2):** Does c·Δ with c ∈ [0.75, 0.85] hold across delta∈{6, 9, 12, 18, 24}? Or is the slope model regime-specific? **Impact:** predicts knee location for any delta, enabling scheduler design. **Test cost:** 225 runs (~2 min).

2. **Window-center sliding with (delta, pd) (F3):** Where does memory pay for unexplored (delta, pd) pairs? Does σ* increase with delta (higher demand) and decrease with pd (higher capacity) monotonically? **Impact:** extends memory-utility prediction beyond current delta=12, pd=3 measurement. **Test cost:** 900 runs (~7 min).

3. **Coherence-radius connectivity law (F1a refined):** Does residency(ladder_step, spread) follow *connectivity of coherence graph* (sharp drop at step > delta/2) vs. linear dependence? **Impact:** explains why graded staleness outperforms binary splits; enables custom ladder design. **Test cost:** 75 runs (~30 s).

4. **Full K-interaction pulse-overlap mechanism proof:** Does the K=2 echo-trough (K1 53.2% / K2 47.4% / K4 66.6% for kcoh5) arise predictably from pulse-decay overlap (50% residual at K=2)? **Impact:** allows prediction of K-optimal regime without grid sweep. **Test cost:** 50 runs with detailed lag-trace logs (~1 min).

5. **Window-edge phase-fragility boundary:** How fragile is the N1 memory window to phase offset? SPIN-10 showed K8−K1 sign-flips with d; does the window *collapse* at some d-threshold, or degrade smoothly? **Impact:** explains why memory is last-resort (fragile to orthogonal knobs); constrains scheduler design. **Test cost:** 120 runs (N1 tri3 × phase 0–6 × 4 K × 5 seeds; ~1 min).

---

## 10. SCARS & HONEST SCOPE

**Unresolved mysteries:**
1. The effective 0.75·2Δ coefficient—why not 1.0? Integer division losses, asymmetric decay dynamics, feedback settling lag. **Mechanistically not yet understood.**
2. Fresh-cohort law holds descriptively at K=1 but K=2 scrambles it. No unified formulation across K. **Rule is conditioned on K.**
3. Coherence chain (ladder step < delta/2) is PROVEN in action but the connectivity-graph prediction (sharp drop at threshold) is SPECULATED, not independently tested.
4. Memory window shape and center—measured at one point (delta=12, pd=3, σ≈3); full scaling is open.
5. Pulse-overlap mechanism for K-interaction—MODELED from pattern matching (K=2 pathology at 2-tick decay), not proven with controlled pulse traces.
6. Phase-fragility of N1 memory—SPIN-10 shows sign-flips with d, but the collapse boundary is unmeasured.

**Structural assumptions still load-bearing:**
- Integer-only arithmetic on the run fabric; float-only at display
- Delay model (discrete 1-tick lags) with floor-division decay mag = mag - (mag//2)
- All runs at 4800-tick horizon (longer runs in C4 extended to 38400 ticks, no time-drift)
- Grid measurements at K∈{1,2,4,8} only; K=3,6,7 unmeasured
- All fresh-cohort claims at spread ≤ 30; extrapolation to spread=45 failed (SPIN-8 prediction gate)

---

## 11. SYNTHESIS: THE FIVE-AXIS MODEL

**Residency is determined by:**

```
residency = baseline(spread, grammar, K)
          − phase_resonance_cost(sync, K)
          ± memory_window_gain(σ, delta, pd, K)
          − composition_substitution_cost(knobs sharing channel)
          + composition_orthogonal_stacking(knobs on separate channels)
```

**Baseline:**
- Spread axis: rate-limited collapse at 0.75·2Δ (echo factor governs speed)
- Grammar axis: fresh-cohort majority dominates; coherence chains (step ≤ delta/2) outperform binary splits; stale-mass nearly fungible conditional on n_f
- K-interaction: fresh≥4 improves with K; fresh≤3 declines; K=2 echo-trough is global worst

**Resonance cost:**
- Spread=0: 22.7pp (K=1) to 50.0pp (K=2) self-harm
- One-tick offset: restores 12.0pp sharp

**Memory gain:**
- Non-zero only at σ ≈ 3–4 (delta=12, pd=3): +31.7pp at σ=3
- Fragile to phase offset (sign-flips with d)

**Composition:**
- Orthogonal channels (scheduler × AS): superadditive, new best-known 89.0% cohort8+AS@K=2
- Substitutes (decorrelation × memory on pulse-superposition): subadditive-to-destructive, worst −46.0pp

**Conservation:**
- Mass closure: exact Δ=0 every run
- Debt additivity: exact Σ tolls every run
- Event ceiling: 99.85% occupancy (every twin fires ~every tick)
- Debt scaling: unbounded under drift, capped under deadband-tightening

---

## BIBLIOGRAPHY: EVIDENCE BY SPIN

- **SPIN-4 (Metrology):** First spread-law knee measurement; pattern-invariance falsified
- **SPIN-5 (Pattern-Grammar):** Knee densification, grammar dial magnitude, chatter mechanism, slope wall
- **SPIN-8 (Coherence-Radius):** Wall divergence rule N > 2pd; effective 0.75·2Δ law
- **SPIN-9 (Grammar-Law):** Stale-mass × K interaction grid; K-flip mechanism
- **SPIN-10 (Phase-Scheduling):** Phase-lag stabilization validated; memory window; N1/N2 novel; substitutes-not-complements
- **SPIN-11 (Pulse-Dial):** Echo-factor rate law; compensation as trade; mixture protection
- **SPIN-12 (Orthogonal-Grammar):** Fresh-count causality proven; n_f × K interaction; stale-mass near-fungibility
- **SPIN-13 (Snap-Shadow + Addenda):** Design methodology (engineer tolerance / mechanic refinement); cost doctrine
- **SPIN-14 (Coupling):** Superadditivity rule; orthogonal channels; N1 substitutes
- **SPIN-15 (Conservation):** Mass closure, debt additivity, expiry evaporation, event ceiling, debt unbounded under drift

---

**End of theory v1. Ready for replication and contradiction.**
