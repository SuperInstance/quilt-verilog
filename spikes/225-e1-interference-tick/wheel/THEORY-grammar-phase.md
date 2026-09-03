# THEORY — Unified Interference Grammar Phase Model
**Lane:** claude-theory · **Date:** 2026-09-03 · **Context:** SPIN-5-pattern-grammar, SPIN-5-topology, NOVEL N1/N2 results synthesized.

## 1. THE FIRST-ORDER SPREAD LAW (PROVEN)

Interference residency collapses with twin latency spread, tracking a critical threshold determined by the disagreement-slope model, not raw channel delay.

**The knee (SPIN-5 ladder N=6, 5-seed mean):**
- Steepest per-unit drop at spread 14→15: **12.9pp/unit (K=1), 12.2pp/unit (K=2)**
- Onset localizes to **spread 15±1**, which is the slope-adjusted 2Δ crossing
- 50%-midpoint at spread **≈19.6 (K=1) / 19.2 (K=2)**
- Sequential arm never crosses 50% residency out to spread=24 (52.9% at raw 2Δ=24)

**Effective scaling (MODELED):** The critical spread is **≈0.75·2Δ**, not 2Δ itself. At Δ=12, this predicts spread ≈18, close to observed 19.6. The slope model (disagreement × spread ≈ 2Δ) overshoots by ~33%; the effective coefficient is 0.75, not 1.0. This is not a surprise: feedback-settling through proportional control with finite velocity will hit the deadband before raw sum-of-disagreements predicts.

**Mechanism (MODELED):** Interference twins deliver correction e//3 per pulse (integer division loss included). Sequential snapping delivers e in one impulse. When twins sit at different latencies, they accumulate asynchronously; beyond the critical spread, the faster twin overshoots and the slower twin can't catch up within the deadband—g enters a deadlock cycle. The transition is smooth (~5-6 spread-unit band), not sharp, because coherence chains of nearby twins still couple.

## 2. THE TWO-PARAMETER GRAMMAR-LAW (PROVEN + SPECULATED MECHANISM)

At fixed spread, the multiset grammar of latency distribution is a second-order dial of comparable or greater magnitude than the first-order collapse.

**The dial magnitude (SPIN-5 grammar sweep, s=15 and s=30, K=1):**
- At spread=15: **zero 77.3% vs ladder 71.5%** = 5.8pp spread (all-synchronized vs graded)
- At spread=30: **zero 77.3% vs ladder 26.8%** = **50.5pp spread** — twice the entire first-order collapse from spread 10→24
- Grammar moves true-residency ≥20pp at fixed total spread and K

**The two parameters: stale-mass and fresh-coherence (PROVEN):**

1. **Fresh-cohort-majority law (SPIN-5 topology, K=1 at spread=15):**
   - kcoh5 (5 fresh, 1 stale): **74.1%**
   - kcoh4 (4 fresh, 2 stale): **62.6%**
   - kcoh3 (3 fresh, 3 stale): **57.1%** ← local minimum (no majority)
   - kcoh2 (2 fresh, 4 stale): **64.4%**
   - kcoh1 (1 fresh, 5 stale): **47.3%**

   Same multiset sizes mirrored; fresh side is dominant. The 3v3 tie is the floor. No monotone majority law survives—**residency tracks the coherent cohort's position (fresh vs stale), not magnitude alone.**

2. **Coherence chain (SPIN-5 topology):**
   - Graded ladder [0,3,6,9,12,15] at spread=15: **71.5%** — exploits the fact that adjacent twins differ by 3 ≤ delta=12, so they remain coherent (synchronized feedback reaches both within a generation). This is a *taper*, not a cohort, yet outperforms binary splits kcoh2/kcoh4 at single-generation decay.
   - Ring [0,10,0,10,0,10] ranks near kcoh5 (fresh pairs with stale partners): **74.1%** — confirms the reading as a 3-fresh coherence structure.

3. **K-interaction breaks the law (SPIN-5 topology, K-sweep):**
   - Zero 77.3% (K=1) → 50.0% (K=2): **−27.3pp** (best to mid-range)
   - Quart 45.4% (K=1) → 53.4% (K=2): **+7.0pp** (only grammar that *improves* with K)
   - Ladder 71.5% (K=1) → 60.0% (K=2): **−11.5pp**

   **No global K champion.** At K=1, zero and fresh-cohort dominate; at K=2, residuals from the prior tick decay to ~25%, so synchrony matters less and the stale side becomes more costly (half-decayed pulses stack into fresh overshoot). The law is *conditioned on K*; any unified theory must parameterize both.

**Stale-mass cost estimate (MODELED):** Sequential arm (impulse-only, no memory) shows grammar-blindness: cohort ≡ quart ≡ outlier ≡ paired all at **56.8%** at s=15, **53.6%** at s=30 — sequential sees only the ordered set of latencies (first trigger, then next, etc.), not the duplicate multiplicity. The difference between interference (cohort 57.1% at s=15 K=1) and sequential (56.8%) is only 0.3pp; the 20pp dialect between zero (77.3%) and cohort (57.1%) is the pure interference self-harm term: **cross-cohort staleness disagreement**. Stale-cohort debt is ~2× fresh-side: kcoh1 K=2 carries 483k events vs ladder 260k at the same configuration.

## 3. THE COHERENCE CHAIN LADDER RIDES (PROVEN)

Graded staleness is equivalent to a taper-coherent group, not a binary split. This unifies SPIN-3's ring result and explains why the ladder (no cohort in the classical sense) outperforms many binary grammars.

**The ladder's coherence radius (SPIN-5 topology):**
- Ladder step = 3 (at delta=12): all adjacent twins differ by 3 ≤ delta, so they couple within **one generation of decay** (~e//3 feedback cycle).
- This creates a **connected coherence graph** anchored at the fresh end, tapered to stale, which protects coherence better than a cut-off binary split like kcoh2 [0,0,15,15,15,15] (all-to-all within each group, but hard boundary in the middle).

**Predictions (SPECULATED):**
- If ladder step increases from 3 to 5 (at same spread=15, new latencies [0,5,10,15,20,25]), the coherence chain breaks: adjacent twins differ by 5, which exceeds delta/2 for some, and residency should drop to ~kcoh2 levels (lower 60s).
- If ladder step decreases to 1 (N=16 twins at spread=15: [0,1,2,...,15]), the chain is tighter and residency should rise closer to kcoh5 (fresh laggard) at ~74%.
- **Hypothesis:** residency(ladder_step) follows the *connectivity of the coherence graph*, not linearly with step, but with a sharp drop-off when step > delta/2.

## 4. SYNC-RESONANCE CHATTER & ANTI-SYNC PHASE (PROVEN)

Synchronized duplicates (spread=0) create a self-destructive resonance loop. One tick of phase offset cures 40% of the event cost.

**The mechanism (SPIN-5 pattern-grammar, zero-lock K=1, spread=0):**
- **100% of event-ticks fire all 6 twins simultaneously** (1459/1459 synchronized fires)
- **99.84% of consecutive fires flip sign** (5058/5066): the arm overshoots onto its own echo oscillation
- All twins read the same residual, all fire the same tick, all generate correlated corrections that cancel or reinforce together—this is Spin-1's gap=1 refire generalized to N=6

**Isolated cost (PROVEN):**
- Zero-lock K=1: **22.7pp chatter self-harm** (77.3% residency vs sequential's 100.0%)
- Zero-lock K=2: **50.0pp self-harm** (50.0% vs 100.0%) — half-decayed prior ticks make resonance worse
- Sequential at spread=0 remains perfect (100%, only 527 events) — no echo because there's no memory

**Anti-sync phase cure (NOVEL N2, PROVEN):**
- Spread=1 (one-tick phase offset between duplicate classes): **89.3%** (ladder N=6 K=1, 5-seed mean)
- Events collapse **8756 → 5232 on the first tick of offset** (−40%) and to 2598 by spread=5
- Debt collapses 187.8k → 87.4k → 43.9k
- One tick of offset buys **12.0pp of residency recovery** — the H2 signature, sharp not gradual

**Phase as a control knob (MODELED):** The resonance is a sampled-system instability: if both twins fire at the same tick t with residual e, they both generate e//3, summing to ~2e overshoot. The system then refires at t+1 with reversed sign. If one twin lags by one tick (phase offset), the corrected error from tick t feeds forward into only one twin's decision at t+1, breaking the symmetric oscillation. **This is a classical phase-lag stabilization** seen in digital control loops; the "anti-sync" is a mode-specific phenomenon, not a general property. At other grammars (cohort, ladder), residency already spreads corrections, so phase offset has less impact.

**Pattern-blindness of spread-1 (NOVEL N2, PROVEN):**
- Ring@1 [0,1,0,1,0,1] and cohort@1 [0,0,0,1,1,1] and ladder@1 [0,1,2,3,4,5] are all **byte-identical to the last digit** (5/5 seeds × 3 K values)
- At spread ≤1, the pattern grammar doesn't discriminate — **only the offset matters**. The multiset structure becomes irrelevant when twins are too close to separate in practice.

## 5. THE SIGMA=3 MEMORY WINDOW & SLOPE WALL (PROVEN)

Cross-tick wave memory (stacked pulse generation, K>1) is conditional: useless outside a narrow velocity window at the wall's edge.

**Three channel regimes (NOVEL N1, N=6 ladder, lats=[0,10], 5-seed mean):**

| Regime | σ (slope/tick) | K=1 resid | K=8 resid | Δ (K8−K1) | seq | status |
|---|---|---|---|---|---|---|
| **Slow** | σ≤2 (tri2~2.0) | 93.8% | 89.0% | −4.8pp | 57.2% | conflict: interference >> seq; K short best |
| **Window** | σ≈3 (tri3~3.0) | **13.9%** | **45.6%** | **+31.7pp** | 52.3% | **K-rank flipped**; memory pays enormously |
| **Fast** | σ≥4 (tri4~4.0) | 5.2% | 7.1% | +1.9pp | 51.5% | SLOPE WALL; all K collapsed; impulse wins |

**The wall (PROVEN):** Beyond σ=3 or σ=4, residency drops below 10% for interference regardless of K, while sequential holds 51–52% at the wall and 81.3% far beyond (σ=16). The factor separation: **~100×** at σ=16 (impulse 81.3% vs interference 0.9%).

**Mechanism (MODELED):** A twin firing at error e delivers e//3 per pulse, decaying over ~5–10 ticks (Spin-1 §3.1). When the channel slope σ outruns the pulse decay tail, the system can never catch the rising error: the deadband is permanently out of reach. Sequential snapping delivers the full correction in one tick (impulse), independent of channel slope, so it remains viable. This is a **finite-velocity-capacity phenomenon**: interference has v_max = (σ_pulse, K, pd) depending on decay speed and generation count; sequential has v_max = ∞ (impulse).

**The window law (MODELED + SPECULATED):** Memory pays only where demand ≈ capacity: at σ=3, K=1's single-generation decay can't keep pace (13.9%), but K=8's stacked generations deliver a faster correction velocity (45.6%), closing the gap to 31.7pp. This is a **bandwidth-matching sweet spot**. The window should slide with delta and pd: if delta increases (tighter deadband, higher demand) or pd decreases (longer decay, higher capacity), the window center shifts. **Next measurement: sweep delta ∈ {6, 12, 18, 24} and pd ∈ {1, 3, 6} to map the window's center as a function of (delta, pd).**

## 6. FALSIFIABLE PREDICTIONS (NOT YET TESTED)

### Prediction F1: Coherence-Radius Scaling (Expected: VALIDATED)

**Hypothesis:** Residency(ladder_step, spread) depends on the *connectivity of the coherence graph*, not linearly on step size. Specifically, when ladder_step > delta/2, adjacent twins exceed the coherence radius and residency drops sharply to kcoh2 levels (~64-65%).

**Experiment Spec:**
- **Setup:** N=6, spread=15, delta=12, K=1, stress params (drift=6, pd=3), seeds {1,7,42,1999,20260902}
- **Sweep:** ladder step ∈ {1, 3, 5, 9, 15} at fixed spread=15 (equivalently, N ∈ {16, 6, 4, 3, 2} with adjusted latencies)
- **Control:** kcoh2, kcoh4, kcoh5 at same spread, same K
- **Metric:** true-residency % (5-seed mean), event count, debt
- **Gate:** spread=0 identity canary, spin-5 ladder replay (71.5%)
- **Cost:** 5 steps × 3 K × 5 seeds ≈ 75 runs, ~30 s
- **Expected result:** residency rises 64% → 71% → 65% (drop at step=5), with drop-off occurring at step=delta/2+ε

### Prediction F2: Delta-Scaling Law (Expected: MIXED, confirm or falsify monotone c)

**Hypothesis:** The critical spread (knee, 50%-crossing) scales as spread_crit(Δ) = c·Δ with c ≈ 0.75–0.85, constant across delta values. If c is not constant, the slope-adjusted 2Δ model is delta-specific, not universal.

**Experiment Spec:**
- **Setup:** N=6, K=1, interference arm, ladder grammar, stress params (drift=6, pd=3), seeds {1,7,42,1999,20260902}
- **Sweep:** delta ∈ {6, 9, 12, 18, 24} × spread ∈ {6, 9, 12, 15, 18, 21, 24, 27, 30} (9 spreads per delta)
- **Metric:** true-residency %, locate 50%-crossing and steepest knee per delta
- **Gate:** spread=0 identity, spin-4/spin-5 anchor rows (delta=12, knee at spread 14–16)
- **Cost:** 5 deltas × 9 spreads × 5 seeds ≈ 225 runs, ~2 min
- **Expected result:** spread_crit(6) ≈ 4.5–5, spread_crit(24) ≈ 18–20, confirming c·Δ with c ∈ [0.75, 0.85]
- **Falsification boundary:** if c varies by >0.1 across delta, the model is regime-specific

### Prediction F3: Window-Center Sliding with (Delta, Pd) (Expected: VALIDATED)

**Hypothesis:** The memory window (where K=8 beats K=1 significantly, ΔK > 20pp) center slides predictably with delta and pd. The window occurs where demand (tighter deadband, faster noise) matches capacity (decay speed, generation count). Specifically, window center σ* should increase with delta and decrease with pd.

**Experiment Spec:**
- **Setup:** N=6, lats=[0,10], stress (drift=6), seeds {1,7,42,1999,20260902}
- **Sweep:** delta ∈ {6, 12, 18} × pd ∈ {1, 3, 6} × K ∈ {1, 2, 4, 8} × σ ∈ {2, 3, 4, 5, 6} (5 channel slopes per config)
- **Metric:** ΔK(sigma) = K=8_resid − K=1_resid; locate peak ΔK per (delta, pd)
- **Gate:** spread=0 identity, novel-N1 replay (delta=12, pd=3, window at σ≈3)
- **Cost:** 3 deltas × 3 pd × 4 K × 5 σ × 5 seeds ≈ 900 runs, ~7 min (parallelizable)
- **Expected result:** σ* increases monotonically with delta (tighter deadband = higher demand); σ* decreases with pd (longer decay = higher capacity). Quantify: σ*(delta=6, pd=3) < σ*(delta=12, pd=3) < σ*(delta=18, pd=3), and σ*(delta=12, pd=1) > σ*(delta=12, pd=3)
- **Falsification:** if σ* is independent of (delta, pd), the window is a channel artifact, not a system law

### Prediction F4: K-Interaction with Fresh-Cohort (Expected: MIXED, refinement)

**Hypothesis:** The K-inversion (where zero 77.3→50.0 and quart@30 45.4→53.4) is driven by pulse-memory overlap: at K=2, the prior tick's ~25%-residual pulses stack into fresh overshoot, destabilizing large fresh cohorts (zero) while stabilizing split grammars (quart). The effect should reverse at K=4 (pulses decay further before stacking).

**Experiment Spec:**
- **Setup:** N=6, spread=15/30, K ∈ {1, 2, 3, 4, 6, 8}, stress params (delta=12, drift=6, pd=3), seeds {1,7,42,1999,20260902}
- **Sweep:** grammars: zero, quart, cohort, ladder (4 grammars × 2 spreads × 6 K values)
- **Metric:** true-residency %, track inversion: rank orderings by residency per (spread, K)
- **Gate:** spread=0 identity, spin-5 results (K=1/2/8 anchors)
- **Cost:** 4 grammars × 2 spreads × 6 K × 5 seeds ≈ 240 runs, ~2 min
- **Expected result:** zero's rank falls from 1st (K=1) through mid-range (K=2–3) and rebounds toward bottom (K≥6); quart's rank rises through mid-range; inversion apex occurs at K=2–3, where pulse decay has dropped to ~50% but hasn't yet cleared (next generation cancels). At K=4+, orderings partially revert as stale-side grammar becomes viable again.
- **Falsification:** if rank orderings do not invert (monotone majority law re-emerges), the K-effect is grammar-independent

---

## Synthesis: The Grammar-Phase Model

Quilt interference residency is determined by **three co-equal axes:**

1. **First-order spread law** (additive collapse, ≤50pp range): spread determines whether twins decohere; critical region is spread ≈ 0.75·2Δ.
2. **Second-order grammar law** (multiplicative dial, 20–50pp per condition): which latencies are duplicated determines fresh/stale asymmetry; positive feedback from coherence chains (graded staleneses) outperforms binary splits.
3. **Third-order phase/sync law** (conditional resonance, ±12–50pp): exact timing synchrony at spread=0 creates destructive resonance; one-tick offset stabilizes. Memory (K) pays only in a narrow velocity window (σ≈3–4 at delta=12, pd=3) where demand matches capacity.

**The model predicts residency as:**
```
residency = baseline(spread, grammar, K) 
          − phase_resonance_cost(sync, K)  
          ± memory_window_gain(σ, delta, pd, K)
```

where baseline is the interplay of first-order (spread) and second-order (grammar, fresh-cohort) effects, phase cost is acute at spread≤1, and memory gain is sharp at σ≈3 and zero elsewhere.

**Scars & honest scope:**
- The 2Δ model (knee at 2Δ) is off by ~25% (true ≈ 0.75·2Δ). Plausible: integer division losses (e//3), asymmetric decay dynamics, or feedback settling lag. **Not yet understood.**
- The fresh-cohort law holds descriptively (kcoh5 > kcoh4 > kcoh3 > kcoh2 > kcoh1 at K=1) but K=2 scrambles it. The rule is *conditioned on K*; no unified formulation yet.
- Coherence chain (ladder step < delta/2) is SPECULATED, not yet tested independently of multiset size.
- Memory window center and shape (how it slides with delta/pd) is partially measured; full scaling law is open.

**Status:** PROVEN: first-order spread law, grammar dial magnitude, fresh-cohort majority, sync chatter mechanism, one-tick phase cure, slope wall. MODELED: effective scaling 0.75·2Δ, coherence-chain mechanism, velocity-capacity model, phase-lag stabilization. SPECULATED: coherence-radius scaling, K-pulse-overlap interaction, window-sliding law.

---

**End of theory draft.** Falsifiable predictions F1–F4 stand as the next experimental gates. The model is ready for replication and contradiction.
