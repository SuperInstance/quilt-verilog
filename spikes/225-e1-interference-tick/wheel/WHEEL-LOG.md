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


## SPIN-5-TOPOLOGY (dispatched 2026-09-03 07:02 AKDT)
- **SPIN-4 verdict recorded:** MIXED — spread-law knee VALIDATED at spread≈15 (93.5→71.5→49.2% across 10/15/20, N=6 K=1 ladder), N-independence SUPPORTED first-order (N=2/3/6 all in 10–29% collapsed band at spread=30), pattern-invariance FALSIFIED (cohort 49.3% vs ladder 26.8% at spread=30 K=1), spread=0 chatter anomaly (50–77%, worse than spread=5's 97.6% — U-shaped at origin). Files: wheel/SPIN-4-metrology.md + spin4_metrology.py.
- **Spoke:** TOPOLOGY (spoke 4, LCG: 1147902781 → 2035015474 → 2035015474 mod 10 = 4) · lane: wheel_spin5_topology (zai/glm-5.3, run mode)
- **Brief:** Cohort-majority law test (SPIN-4's proposed PATTERN-GRAMMAR, framed as topology): N=6 fixed, K∈{1,2,8}, spread=15 at the knee, sweep multiset grammar (graded ladder, k-cohort splits k=1..5, bimodal, single laggard, single outlier, 3v3 binary anchor). Plus knee densification: ladder spread 12–24 step 2 vs 2Δ=24 prediction. Integer-only, seeds 1/7/42/1999/20260902, self-canaries (spin4 ladder spread=15 replay ~71.5/60.0/70.7%, spread=0 identity), real runs.
- **Dispatch status:** IN FLIGHT (one lane max — held). Deliverable: wheel/SPIN-5-topology.md.
- **Verdict:** pending (record in next spin's log entry when lane completes).
- **LCG state after this advance: 2035015474** (next spin continues from here).
