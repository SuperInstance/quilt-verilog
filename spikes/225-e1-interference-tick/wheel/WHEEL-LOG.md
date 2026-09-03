# WHEEL-LOG.md — verdict ledger

## SPIN-dequant-2 (DEQUANT spoke) — 2026-09-02 ~22:40
- **Spoke:** DEQUANT (§10 cheat-code probes) · lane: dequant_track_2 · files: wheel/SPIN-dequant-2.md + spin_dequant2.py
- **Verdict: MIXED — 3 sharp boundaries measured.**
  - Grover-curve: speed story DECORATIVE (log-flat, crosses √N only ~N=256); "amplitudes add" LOAD-BEARING (956‰ directional vs 745‰ sequential).
  - Thermodynamic cheat #3: **FALSIFIED** — cold > warm > hot everywhere; no measured point. Negative booked first-class.
  - Snap-point cheat #1: **VALIDATED ×2** — delivery identity predicts grid argmax (div=2) with ZERO queries; 1/8-cost probes rank grid 952–964‰.
- **Headline revision:** div=2,K=1 Pareto-dominates E1 home config (7/7 stress metrics) AND beats sequential in calm (980 vs 566‰). "Interference worse at gentle" = operating-point artifact. pm strictly decreasing in K → load-bearing superposition is within-tick twin averaging, not cross-tick wave memory.
- **New spoke proposed:** WITHIN-TICK AVERAGING (twin-swap, dyad structure, sub-tick superposition) — the mechanism that just ate the wave's credit deserves its own spoke.
- **Scars:** v1 name-map bug (cold ran as hot; caught by self-canary — instrument gate doctrine pays again); floor-decay sign-asymmetry flagged.

## SPIN-k-replay (METROLOGY/K-axis, overnight run 1) — 2026-09-02 ~22:28
- **Verdict: VALIDATED + bigger artifact.** K=3 > champion K=5 (5/5, +1.0 mean); impulse-d16 96.0% zero-variance beats all K; crown = joint mode×delta×K grid artifact. 32/32 byte-match gates. Files: inventors-derby/OVERNIGHT-K-REPLAY.md.
- **New spoke proposed:** none — TOPOLOGY/ALPHABET spokes already cover; arena-grid K-sweep proposal promoted to dev-rounds queue.

## SPIN-3-TOPOLOGY (dispatched 2026-09-02 23:20 AKDT)
- **Spoke:** TOPOLOGY (spoke 4, LCG: prev idx 2 → state 662824084 → 662824084 mod 10 = 4) · lane: wheel_spin3_topology (zai/glm-5.3, run mode)
- **Brief:** Does the F7 bundle-capacity wall (91%→10% by N≥4, seeded K=8) move with (K, topology)? Sweep N∈{1..6} × K∈{1,2,8} × topology∈{all-to-all, ring, star} on e1.py; integer-only, seeds 1/7/42/1999/20260902, self-canary, real runs.
- **Dispatch status:** IN FLIGHT (one lane max — held). Deliverable: wheel/SPIN-3-topology.md.
- **Verdict:** pending (record in next spin's log entry when lane completes).
## SPIN-4-METROLOGY (dispatched 2026-09-02 23:59 AKDT)
- **SPIN-3 verdict recorded:** VALIDATED — F7 bundle-capacity wall is a topology artifact: N=6,K=8 ring 82.6% vs all-to-all 10.1% true-residency; geometry first-order, K second-order. Both canaries passed (N≤2 identity, F7 replay exact).
- **Spoke:** METROLOGY (spoke 1, LCG: 662824084 → 1147902781 → 1147902781 mod 10 = 1) · lane: wheel_spin4_metrology (zai/glm-5.3, run mode)
- **Brief:** Execute SPIN-3's proposed SPREAD-LAW sweep as metrology: N=6 fixed, K∈{1,2,8}, max−min twin latency spread ∈ {0,5,10,15,20,30} with ≥2 distinct multisets per spread (pattern-invariance check), shuffled-ladder control (spread=30 at N∈{2,3}) to decouple N from spread. Hypothesis: residency collapses at critical spread ~15–20 independent of N. Self-canaries: spread=0 byte-identity, spin3 ring replay. Integer-only, seeds 1/7/42/1999/20260902, real runs.
- **Dispatch status:** COMPLETE. Deliverable: wheel/SPIN-4-metrology.md.
- **Verdict: MIXED** — ladder knee at spread≈15 (2Δ crossing), N-independent first-order; pattern-invariance FALSIFIED (cohort 49.3% vs ladder 26.8% at spread=30 K=1); spread=0 chatter anomaly (worse than spread=5). Both canaries passed. Proposed spoke: PATTERN-GRAMMAR (dispatched as SPIN-5).
- **LCG state after this advance: 1147902781** (next spin continues from here).

## SPIN-5-PATTERN-GRAMMAR (dispatched 2026-09-03 07:00 AKDT)
- **SPIN-4 verdict recorded above (MIXED).**
- **Spoke:** PATTERN-GRAMMAR (SPIN-4's proposed spoke; LCG pick deferred) · lane: wheel_spin5_pattern_grammar (zai/glm-5.3, run mode)
- **Brief:** Execute the pattern-grammar spoke thoroughly: densified knee (spread 10..24, ±2 localization), grammar sweep at fixed spread 15/30 (5 grammars + tri reading + zero-lock), chatter mechanism with per-tick logs, mandatory canaries (spread=0 byte-identity, spin-4 replay). Integer-only, seeds 1/7/42/1999/20260902, real runs.
- **Verdict: MIXED.**
  - Knee VALIDATED: onset 14–16 (steepest 84.4→71.5% at 14→15, 12.9pp/unit) = slope-adjusted 2Δ crossing at 15, NOT raw 24 (31.7% there); 50%-crossing ≈19.6; sequential never crosses 50 by 24.
  - Grammar dial VALIDATED (20.1pp @15 K=1, 50.5pp @30 K=1: zero 77.3 vs ladder 26.8) but monotone majority law FALSIFIED in detail (quart<cohort @30 K=1; K flips orderings: zero 77.3→50.0, quart@30 45.4→53.4 rising).
  - Chatter mechanism VALIDATED at zero-lock (100% all-6 synchronized fires, 99.84% sign-flip echo, gap-1 in 140/140 runs; isolated cost 22.7pp vs sequential 100.0%) but as loss predictor weak (r≈−0.51) — stale cross-cohort disagreement, not synchronization, drives grammar losses.
  - Discoveries: order-invariance (grammar=multiset, both arms, 30/30 byte-identical); sequential multiplicity-blind (cohort≡quart≡outlier≡paired exactly); interference beats sequential at outlier@15 (+17.3pp).
  - 4/4 canaries PASS (A spread-0 identity, B spin-4 replay exact, C order-invariance, D zero-spread-invariance). Scar booked: replay tolerance must respect publishing-format rounding (cancels 4.2 vs "4").
- **New spoke proposed:** GRAMMAR-LAW (stale-mass × coherence 2-parameter law + K-interaction).
- **LCG advance: 1147902781 → 2035015474 → mod 10 = 4 (TOPOLOGY next).**


## SPIN-6-TOPOLOGY (dispatched 2026-09-03 07:02 AKDT)
- **SPIN-4 verdict recorded:** MIXED — spread-law knee VALIDATED at spread≈15 (93.5→71.5→49.2% across 10/15/20, N=6 K=1 ladder), N-independence SUPPORTED first-order (N=2/3/6 all in 10–29% collapsed band at spread=30), pattern-invariance FALSIFIED (cohort 49.3% vs ladder 26.8% at spread=30 K=1), spread=0 chatter anomaly (50–77%, worse than spread=5's 97.6% — U-shaped at origin). Files: wheel/SPIN-4-metrology.md + spin4_metrology.py.
- **Spoke:** TOPOLOGY (spoke 4, LCG: 1147902781 → 2035015474 → 2035015474 mod 10 = 4) · lane: wheel_spin6_topology (zai/glm-5.3, run mode)
- **Brief:** Cohort-majority law test (SPIN-4's proposed PATTERN-GRAMMAR, framed as topology): N=6 fixed, K∈{1,2,8}, spread=15 at the knee, sweep multiset grammar (graded ladder, k-cohort splits k=1..5, bimodal, single laggard, single outlier, 3v3 binary anchor). Plus knee densification: ladder spread 12–24 step 2 vs 2Δ=24 prediction. Integer-only, seeds 1/7/42/1999/20260902, self-canaries (spin4 ladder spread=15 replay ~71.5/60.0/70.7%, spread=0 identity), real runs.
- **Dispatch status:** IN FLIGHT (one lane max — held). Deliverable: wheel/SPIN-6-topology.md.
- **Verdict:** pending (record in next spin's log entry when lane completes).
- **LCG state after this advance: 2035015474** (next spin continues from here).


## SPIN-10-PHASE-SCHEDULING (dispatched 2026-09-03 07:19 AKDT)
- **Spoke:** PHASE-SCHEDULING (banked novel N1/N2 + SPIN-5 chatter convergence) · lane: wheel_spin10_phase (zai/glm-5.3, run mode)
- **Brief:** Promote phase-aware scheduling to a first-class knob. (1) even-offset sweep from the zero-grammar origin (d∈{0,1,2,3,6}), residency-per-event, evenly-spread-optimality at matched max offset; (2) transplant into real grammars (ladder/cohort 3+3/kcoh5-fresh, spread 15+30, K∈{1,2}); (3) composition: N1 memory window (σ=3, +31.7pp) × anti-sync on one channel. Canaries: offset=0 byte-match novel baseline + Spin-5 zero@15 replay. Integer-only, seeds 1/7/42/1999/20260902.
- **Verdict: VALIDATED-as-knob / substitutes-not-complements.**
  - Knob VALIDATED: origin cure +20.3pp (77.3→97.6 at one tick), cross-channel transfer (tri3 zero-lock 81.0→100.0 at d=1), upgrades GOOD grammars not just chatter: kcoh5@15+AS-exact `[0,1,2,3,4,15]` = **79.4% K=1 (best-ever at spread 15, −32% events vs zero-lock)**, K=2 rescues +14.8 (cohort15) / +16.0 (kcoh5@15); sequential refs flat ±0.2pp → arm-specific mechanism. Dose boundary: kcoh5@30 AS-exact K=1 −3.1pp (freshness spent beats sync cured at large spread; AS-min safe +3.5).
  - Evenly-spread NEAR-optimal not optimal: coh5 `[0,0,0,5,5,5]` 99.0 beats even5 97.6 (K=1) and kcoh5 74.1 beats even-ladder 71.5 @15 (K=1); even-6-phase wins every K=2 comparison — phase-count optimum is K-dependent; max-offset budget M dominates fine structure ~25pp vs 1–3pp (M=5 band 93.8–99.0 vs M=15 band 47.3–74.1).
  - Composition (money question) FALSIFIED for additivity: N1's +31.7pp window is phase-fragile (+31.7→+21.2→+7.6→+2.0→−0.2 across [0,10]→[0,16]); on tri3 6-twin the K8−K1 sign flips with d (−14.4/−3.5/+2.7/−13.1/−1.2) — phase scheduling re-ranks the memory term, and the joint optimum (even1 K=1, 100.0%) uses NO memory. Anti-sync and cross-tick memory are substitutes competing for the same job (pulse-stream coherence); memory is compensation of last resort.
  - Unifying booking: decorrelation budget (max−min)·σ ≲ 2Δ — e1 knee 15·1.6=24, tri3 even1 span 5·3=15 OK vs even2 10·3=30 collapsed; origin dip = the span-0 degenerate point. SPAN-BUDGET law proposed as next spoke (tri3 boundary bracketed 5<b≤10, unmeasured).
  - Canaries 2/2 first-run PASS: run2≡run_fabric 8/8 full-dict; 33/33 published anchors exact incl. events/debt (zero 77.3/50.0/69.0 ev 8756/15133/9964 debt 187834/511660/195470; N1 tri3 13.9/39.4/41.9/45.6).
  - New data points: ladder10 K8 = 90.8 (K8 max on d-grid); ladder30 K8 = 14.0 (K8 < K2 deep in collapse — memory anti-useful there).
  - Scars: RPE integer display rounding (orderings exact, magnitudes at 1 decimal); AS-exact confounds de-sync with mild staleness redistribution (bounded by flat sequential refs; pure zero-staleness de-sync impossible on this fabric — lag-0 twins offset only upward, structural asymmetry booked); 6-twin tri3 family changes N vs N1 anchor (faithful 2-twin test reported separately); optimality grid bounded to M∈{5,15}.
- **Files:** wheel/SPIN-10-phase-scheduling.md + spin10_phase_scheduling.py + spin10-output.txt.
- **LCG advance: 2035015474 → 368800899 → mod 10 = 9 (next continues from here).**
- 2026-09-03 kimi-predictor lane (g3-kinduction): LEARNED-PREDICTOR SCHEDULER — VALIDATED (narrow): logreg on [in-flight, mean-lag, stale-mass, K] (ladder grid, seeds 1/7/42) deployed as fixed-point integer per-tick spread scheduler; held-out grammars (cohort 3+3, outlier, kcoh5) x seeds {1999,20260902}: mean gain +5.7pp vs static15 / +16.2pp vs static30, zero regressions; mechanism = cohort-K=2 rescue 41.1->75.2% via spread 15->8 parking; K=1 scheduler inert (scar); canaries 3/3 (sequential byte-identical, harness byte-identical 32/32, spin-5 replay 709/713/721/714/717 exact). Files: wheel/kimi-predictor/ (kimi_predictor.py, REPORT.md, run-output.txt, results.json).

## SPIN-8-COHERENCE-RADIUS (dispatched 2026-09-03 07:19 AKDT)
- **SPIN-5-topology verdict recorded above (MIXED).**
- **Spoke:** COHERENCE-RADIUS (SPIN-5-topology's proposed spoke; LCG pick deferred) · lane: wheel_spin8_coherence_radius (zai/glm-5.3, run mode)
- **Brief:** Mechanize the fresh-cohort law. (1) ladder step-granularity at fixed spread 30, steps {1,2,3,5,6,10,15,30}; (2) delta {6,9,12,15,18,24} x grammars {kcoh5, kcoh1, ladder, cohort} at spread 30 K=1, FVS flip/saturation + rho(delta) vs 0.75*2Δ knee; (3) pre-registered prediction kcoh5 @ delta=12 spread=45 before running. Canaries mandatory (spread=0 byte-identity + topology replay). Integer-only, seeds 1/7/42/1999/20260902, real runs.
- **Verdict: MIXED.**
  - Granularity law FALSIFIED both ways: fine ladders (steps 1-5, N>=7) collapse to 0.1% via divergent all-N-fire oscillation (meanMult=N, 1000‰ sign-flip, net shove overflows 10^18); interior optimum at N=6/step6 (26.8%) tracks 2*pd=6, NOT delta=12 coherence chain (delta-independent at 6/12/24; K=8 rescues step5 to 18.0%). Wall = firing-mass law: divergence iff N > 2*pd (duplicate-bloc discriminator M=6→0.2% vs M=5→53.0% isolates it from step geometry).
  - rho(delta) ≈ 0.31*delta on two independent blades (delta-parity 19.1→0.315; topology knee→0.305-0.327); knee spread = 0.78*2Δ confirms 0.75*2Δ as a CO-MOVING-window law; at pinned spec ±12 no rescue (ladder 11.7% @ delta 24). FVS never flips in 6-24 (51.9→19.0pp, zero-cross ≈34); cohort@30 structurally pinned ≈49.3; kcoh5 declines 62.1→30.9 at pinned spec.
  - Prediction gate FAIL: kcoh5@45 = 52.5% vs pre-registered [34,50] (linear extrap 32.3) — laggard damage saturates TOTALLY by lag 30 (74.1→53.2→52.5). 2nd consecutive saturation-magnitude miss; direction right.
  - Canaries 12/12 lane replays exact to 0.1pp + spread-0 byte-identity PASS.
- **New spoke proposed:** PULSE-DIAL / MASS-COMPENSATION (pd sweep {1,2,3,6,12} x N; n_f-compensated emission variant expected to erase the wall).
- **LCG advance: 2035015474 → 368800899 → mod 10 = 9** (proposal-dispatched; ledger resumes LCG selection next cycle).

## SPIN-9-GRAMMAR-LAW (dispatched 2026-09-03 07:19 AKDT)
- **Spoke:** GRAMMAR-LAW (SPIN-5's proposed spoke; LCG pick deferred) · lane: wheel_spin9_grammar_law (zai/glm-5.3, run mode)
- **Brief:** Fit the two-parameter law (stale-mass m_s, K): 20-grammar (m_s, K) grid at spread 30 + smooth-surface fit with R²/failure map; K-interaction (4 grammars × K∈{1,2,4,8}, characterize flip surface); PRIORITY: spread=12 bump — resonance vs tick-quantization (spread 11/12/13 × 5 seeds, correction-event timing/periodicity). Canaries: spread-0 byte-identity + Spin-5 replay (zero@30 77.3%, ladder@30 K=1 26.8%).
- **Verdict: MIXED.**
  - 2-param law: first-order VALIDATED (pooled within-K isotonic R²=0.973, Spearman(m_s,true) −0.82…−0.96) but FALSIFIED as complete — same-m_s grammars differ up to 33.8pp (g2 20.2 vs stag 50.3 at m_s=7/24, seed swing ~1pp); additive (m_s,K) R²=0.779, rank-1 interaction adds nothing. Missing axis = coherent fresh cohort (lags ≤ δ/2): (fresh,K) R²=0.809, (fresh,m_s,K) R²=0.877; graded mid-lag grammars (g2/ladder/g3) collapse 10–30%, bimodal 0-vs-stale splits hold 45–58% regardless of m_s.
  - K-flip VALIDATED + SHARPENED: inversions 6/15 (K1→2) → 4/15 (2→4) → 0/15 (4→8, ordering freezes); flip surface = fresh≥4-rising (+14.1pp out5_1) crossing fresh≤3-falling (−27.6pp c3_3); K=2 is the global worst K (echo-overlap peak); zero-lock "falls to 50.0" was a K=2 snapshot — recovers 73.9/69.0 at K=4/8.
  - spread=12 bump: RESOLVED as INSTRUMENT SCAR — densified grid inverts the reading (97.2/93.5/96.9/95.0/95.7/84.4 at spreads 9–14: dip at 10, not bump at 12); no period signature (only reality's own 80/40/120 harmonics at every spread), no phase-local structure, cohort monotone, iso-spread sets 91.6–96.3, dip-at-10 recurs at δ∈{10,12,14} → tracks the round(i·s/5) lattice against the (8/5)·lag>δ firing threshold, not δ. Mechanism: ladder(9) rounds all mid lags sub-threshold (accidental 5-fresh grammar → 97.2%); from s=10 the threshold-crossing pattern changes every spread → ±2–4pp wobble.
  - Serendipity: 3-point knee-δ scaling (onset ≈12/15/>14 at δ=10/12/14) → knee ≈ 1.2–1.25·δ — slope-adjusted knee law confirmed across δ; booked for novel lane N3.
  - 2/2 canaries PASS (wiring byte-identity 10/10; Spin-5 replay exact incl. events/debt). Scars booked: nested-model R² must be scored at prediction granularity (first-run F3 bug); local features need BOTH grid neighbors measured (SPIN-5's 2-point bump reading inverted).
- **New spoke proposed:** ORTHOGONAL-GRAMMAR (fresh × stale-mass decoupled grid + intra-stale coherence axis; knee-Δ densification δ∈{6,9,18,24}).
- **LCG advance: 2035015474 → 368800899 → mod 10 = 9 (SILICON next).**
