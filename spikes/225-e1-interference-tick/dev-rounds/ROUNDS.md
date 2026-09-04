# dev-rounds — ROUNDS ledger (branch g3-kinduction)

## Round 14 — Q7 §5.4 regime-gating dial — DISPATCHED 2026-09-03 18:21 AKDT
- **Item:** Q7 — minimal integer controller {κ-detector, lag blade L̂, fan-out N} → {mode, K, pd}, ≤3 registers, no multiply; must clear BOTH O4 gates (932‰ %w AND debt ≤32,770) on the O4 protocol. Pre-registered rule committed before comparison runs.
- **Lane:** dev_q7_regime_dial (zai/glm-5.3, run mode). Deliverable: dev-rounds/ROUND-14-Q7-regime-dial.md. Commit + push g3-kinduction mandated.
- **Verdict:** BOUNDARY BOOKED — pre-registered 3-register dial (R1=L̂ blade-fast, R2=σ stress bit κ-slow, R3=β bursty bit via transient-hit rate) clears the debt gate for the first time in the program (13,211 = 24% of best-static 54,616; adaptive was 57,136) but fails %w (800‰ vs 932‰) and knife-edge (L̂±1): the transient suppressor (≥40 single-tick jumps) kills bursty debt −77% yet leaves ±45 ticks unsettled by construction (bursty 541‰ vs chased 929‰). Frontier mapped with labeled post-hoc amendments (β-gated chase: 922‰/56,089; ideal ≈ 929‰ @ ≈29.2k — 3‰ short of gate a and still L̂+1-fragile). Booking: the three O4 gates are jointly infeasible for any {mode,K,pd} dial at N=2 — chase (settle), don't-pay (debt), alignment-blind (±1) — pick two; O4's 932‰ sat on the corner by L̂=9 underseat luck. Blade-fast/κ-slow works (2 sw/run, conflict 992‰); F14 mag/C=1 gate verified inert at N=2, correct at N=6 (unit). Canaries: O4/F19 anchors exact (932/57,136; 984/17,700/28; blade 5/5), self-canary CAUGHT ×2, double-run byte-identical. Follow-ups: Q7b (dial on O2 N-sweep, F14 gate live), Q7c (leak-proof latch frontier pin).
- **Commit:** a02a84b (pre-registration) · 83703b4 (verdict)
- **Headline:** %w 800‰ @ debt 13,211 vs gates 932‰/32,770 — first arm under the debt gate; gates a+b+c jointly infeasible (chase 929‰/L̂+1→315‰ vs suppress 541‰/13.2k).

Format per block: round #, item, verdict, commit hash, headline number.
Ordered queue: RESEARCH-AGENDA §4 O1–O7, then §Q open questions, then wheel spokes round-robin.

- 2026-09-02 23:00 AKDT — round counter initialized. Next: O1 (K=2/3 champion replay). Wheel lanes dequant-2 + k-replay completed 22:28–22:40 (see wheel/WHEEL-LOG.md); no dev item in flight.

## Round 1 — O1 K=2/3 champion replay — 2026-09-02 23:0x AKDT
- **Item:** O1 (arena schema widened to K∈{1..8} + static grid probes)
- **Verdict:** CONFIRMED — new champion banked
- **Commit:** fb63ff4
- **Headline:** new champion K=1/pd=2/d16 interference 96.1% (triple-axis Pareto domination of old 93.2% champion); calm Δ=6 re-keyed (98.0 vs 56.6); grid-anchoring arena bias booked.

## Round 2 — O2 contention boundary — 2026-09-02 23:5x AKDT
- **Item:** O2 (contention controller boundary; F14 mag+C=1 vs admit-all, raw vs lag-compensated)
- **Verdict:** REFUTED-as-booked / PARTIAL-CONFIRM — win is fan-out-gated (slack at N≤5 raw: +0.0/+1.6pp; clears gate at N=8 raw: +11.9pp stress) and does NOT vanish under lag compensation — it explodes (+24.1pp at N=5, +56.2pp at N=8). "Contention is a lag symptom" false; inverse true: compensator synchronizes twins and *needs* the sort (comp admit-all at N=8 is −15.1pp vs raw). T2 promoted to RTL with N≥~5 boundary note; not demoted.
- **Commit:** 9491c25
- **Headline:** mag C=1 vs admit-all, stress raw: +11.9pp at N=8 (57.8→69.7 %w, maxE 99.2→48.0); compensated: +56.2pp at N=8 (42.7→98.9).

## Round 3 — O2b boundary probe — 2026-09-03 ~00:3x AKDT
- **Item:** IDEATOR nudge on round 2 — sample N∈{6,7}, locate the transition
- **Verdict:** CONFIRMED-SHARPENED — the wall is at **N=6** (raw +4.5pp, first ≥2pp clearance; N=5 was +1.6). Comp-arm amplification has its own knee at 7→8 (+25.0 → +37.6 → +56.2). Lag blade 28/28 exact.
- **Commit:** 1542785
- **Headline:** "the wall is at N=6" — T2 RTL boundary note resolved to a located threshold; lag-amp curve booked as the measured response of a synthetic room-pressure generator (O2-ROOM-PRESSURE-MAPPING.md).

## Round 3b — O3 quanta floor — 2026-09-03 ~11:4x AKDT
- **Item:** O3 (cap × K × regime × 5 seeds; Z₃ sign-only arm; F23 anchor replay)
- **Verdict:** PARTIAL-REFUTE / KNEE RELOCATED — ±5 fails the ≥99% gate at K=2 stress (97.5%); adopt **±7 (4-bit)** as ESP32/.qm default (≥99.2% retention in all 8 K×regime cells). Z₃ debt inversion persists 8/8 (stays sampling gear). Scar: F23's impulse anchor was single-seed; interference rows exact.
- **Commit:** 1542785
- **Headline:** "±7 is the floor" — only cap ≥99% everywhere; K=1 stress retention at ±5 is 88.7%.

---

## Round 4 — O4 regime motion (closed loop) — 2026-09-03 ~12:3x AKDT
- **Item:** O4 (lag blade → compensation → REGIME-META κ-detector → mode dial vs 6 static arms; calm→conflict→bursty mid-stream shifts, charter §3.2; 4800 ticks × 5 seeds)
- **Verdict:** BOUNDARY BOOKED — %w gate PASSED (adaptive 932‰ vs best static seq-comp-oracle 778‰, +154‰) but debt gate FAILED (57,136 > 32,770 = 60% of best static); NOT promoted to E4. Boundary numbers: κ-detector conflict entry 90 ticks vs 1600-tick dwell (E4.B's 2–4-tick prediction falsified at spec thresholds); the %w win rides a knife-edge off-by-one lag underseat (bursty seq: L̂=9→994‰, L̂=10→336‰ — exact alignment is glitch-coherent and hurts the sequential arm); dial fired 6×/run, compensator does the work. F19 doctrine confirmed in-run (comp converts conflict→calm 191→1000‰; comp-seq > comp-int everywhere). E4 demo arm should pre-load blade+compensator+sequential, κ-dial as slow backstop. Canaries: F19 anchors exact (984/17700/28, 1000‰, blade 5/5); mislabeled-arm self-canary CAUGHT.
- **Commit:** 1542785
- **Headline:** closed loop 932‰ beats every static arm on %w but fails the pre-registered debt gate — boundary booked with the 90-tick detector lag and the L̂±1 knife-edge scar.

## Round 5 — O5 phase-decay multi-seed confirm — 2026-09-03 12:4x AKDT
- **Item:** O5 (F24 phase-decay coupling vs F16 admission gate at matched duty; 5 seeds × calm/stress × 3 arms)
- **Verdict:** PROMOTED — stress mean Δ +2.00pp (all seeds +1.3..+2.8, beats published single-seed +1.3), cancels up 5/5; admission gate at identical 4/12 duty destroys residency (−27.8pp stress) — F16 replicated; calm penalty −2.7pp booked (K=8-artifact regime). Phase-decay → e1.py candidate default for stress/conflict; RTL price ~30 LUTs/R1 (phase ctr + refractory cmp + halving mux). Canaries: F24 anchor exact (83.0/68, 84.3/107), mislabeled-arm CAUGHT, double-run byte-identical.
- **Commit:** 1542785
- **Headline:** "touch the decay, not the door" — modulation buys residency, deferral destroys it, at matched duty across 5 seeds.

## Round 11 — Q4 §3.1 MI-criticality sweep — 2026-09-03 ~17:1x AKDT
- **Item:** Q4 (charter §3.1 hello world: LCG noise-rate sweep × d∈{1,2,3}, 10k ticks, integer-histogram MI, 3 lattice sizes, Z vs D Cayley, capacity lookup table; pre-registered decision rule R1–R3 + falsifier, commit 39e893c)
- **Verdict:** PARTIAL — pre-registered model FALSIFIED (gain>1 minimal-pulse floor saturates the lattice: MI≡0 on Z at every p; mechanism supercriticality, not quantization); loss-matched amendment (one-line: emitter pays e per neighbor) passes R1–R3: interior MI peak at p*=3×10⁻⁴ in 8/9 (d,L) cells, cross-seed floor exactly 0 mb, MI_max monotone ↓ in L with exponent a ≈ 3/61→3/44→1/8 (d=1→3). Peak is a wave-coherence crossover (no absorbing phase exists under the pulse floor) — booked as operating point, not universality class. Barbieri: D vs Z dynamically distinct (50% activity plateau; s-edges > r-edges MI everywhere) but high-p sensitivity shoulder NOT confirmed. Capacity table delivered: p=3e-4, d=3 → 127 mb/site-tick @ L=256. Canaries: C1 byte-identity PASS (07d5e578…), C2 e1 anchor PASS (4f4acccc…), C3 self-canary CAUGHT.
- **Commit:** 1940365 (verdict + capacity table) · 21ab669 (DEVIL teeth: fine p-grid + seed split — SPLIT: p*=3e-4 is a coarse-grid artifact, argmax lands p=2/5; interior-peak phenomenon survives out-of-sample seeds; capacity table demoted to band p∈[1,3]e-4)
- **Headline:** falsifier fires on the letter, amendment conducts: MI peak 151 mb (d=3, L=64) at p*=3×10⁻⁴ with zero quantization floor; actuator setting p=3e-4/d=3 → 127 mb/site-tick.

## Round 12 — Q5 §3.2 stake demo (equal-budget GD control arm) — DISPATCHED 2026-09-03 17:31 AKDT
- **Item:** Q5 — the equal-budget gradient-descent control arm does not exist anywhere in derby/arena runs; it is the only cure for the selection-bias objection [CHARTER §5.1]. Build a GD/discrete-greedy control arm matched to the banked champion's budget (calls/reads/ticks identical), head-to-head on frozen holdouts, pre-registered decision rule committed before numbers.
- **Lane:** dev_q5_stake_demo (zai/glm-5.3, run mode). Deliverable: dev-rounds/ROUND-12-Q5-stake-demo.md. Commit + push g3-kinduction mandated (Casey override). Integer-only, seeds 1/7/42/1999/20260902.
- **Verdict:** V2-THIN-MARGIN — equal-budget unsteered discrete-greedy control (183/186 calls, flips to sequential at step 1, rides delta to 22) matches champion on stress within 0.1pp (96.0 vs 96.1, lower debt) but collapses −41.4pp on gentle calm; selection-bias objection half-refuted: stress margin thin and booked, champion's real edge is triple-frame robustness (see ROUND-12-Q5-stake-demo.md). Backfilled: cd4d316.

## Round 13 — Q6 Barbieri Lyapunov proxy — 2026-09-03 ~18:4x AKDT
- **Item:** Q6 (perturbation-support / exact integer Lyapunov proxy, ℤ_n vs D_n vs ℤ_n×ℤ₂ Cayley lattices, Seam B; pre-registered decision rule committed in ROUND-13-Q6-barbieri.md PART 1 before any comparison run)
- **Verdict:** FLOOR-MASKED — quantization floor masks the dichotomy. Twin copies under shared noise: minimal ±1 damage annihilates (S=0 absorbing) in ≥4/5 seeds in every (group, p, N) cell; no sustained exponential separation anywhere; group-typing story neither confirmed nor falsified — ungated. A first build *confirmed* Barbieri (D/P α≈+0.02 vs Z≈0) and was a Gauss-Seidel emission bug, caught by the p=0 BFS-ball wiring canary before verdict. Booked observations: growing survivors only ever on D/P (never Z); Z's one survivor decayed at exactly −1/120 log₂/tick. Next Seam B rung: Rollier–Baetens exact affine-CA spectra.
- **Commit:** 1542785
- **Headline:** ≥4/5 seeds floor-hit in all 12 main-grid cells (D p=300 best survivor α=+99694607/32212254720 ≈ +0.0031, dead by t=256).

## Round 15 — Rollier–Baetens exact affine-CA spectra (Seam B next rung) — DISPATCHED 2026-09-03 18:57 AKDT
- **Item:** Round 13's booked next rung — Q6's Lyapunov proxy was floor-masked (±1 quantization annihilates twin-copy perturbations in every cell); the exact route to the ℤ_n vs D_n Barbieri dichotomy is spectral: exact integer spectra / trace powers of finite affine CAs on ℤ_n vs D_n (vs ℤ_n×ℤ₂ if cheap), small lattices computed exactly so the floor cannot mask.
- **Lane:** dev_r15_rollier_baetens (zai/glm-5.3, run mode). Deliverable: dev-rounds/ROUND-15-rollier-baetens.md. Pre-registered decision rule before any comparison numbers; integer-only; seeds 1/7/42/1999/20260902; canaries (byte-identity ≥8, round-13 anchor replay, mislabeled-group self-canary). Commit + push g3-kinduction mandated.
- **Verdict:** pending (backfill on lane completion).
