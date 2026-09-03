# DEV ROUNDS — quilt-verilog / g3-kinduction

Dev-rounds cron log. One lane per round; verdicts committed to g3-kinduction.
Rule: skip items visibly in flight (check timestamps here + wheel/WHEEL-LOG.md).

---

## Round 1 — O1 (K=2/3 champion replay, arena.py v3)
- **Dispatched:** 2026-09-03 07:31 AKDT · lane: dev_o1_arena_k_short (zai/glm-5.3, run mode)
- **Item:** O1 — widen arena tournament schema to K∈{1..8}; enter static probes K∈{1,2,3}×pd∈{2,3}; 5 seeds, both regimes, frozen holdouts, PROCTOR canary; verify promotions on holdout.
- **Context:** wheel SPIN-k-replay (static) validated K=3 > champion K=5 (96.0% impulse-d16 zero-variance, crown = mode×delta×K grid artifact). Arena LLM run with K≤3 allowed is the undone piece.
- **Verdict:** DONE — static K=1/pd=2/Δ=16 promoted champion: 96.1% tournament + holdout (banked champion 93.2%, Pareto-dominates; debt crown retained by K=5). Zero LLM short-K proposals in 15 calls — grid anchoring booked as standing arena bias.
- **Commit:** a197f6a
- **Headline:** 96.1% (vs 93.2 banked), K=1/pd2/d16

---

## Round 2 — O2 (contention controller boundary) — DONE (pre-existing run verified)
- **Dispatched:** 2026-09-03 09:59 AKDT · lane: dev_o2_contention (zai/glm-5.3, run mode)
- **Discovery:** round already executed 2026-09-02 23:5x (commit 9491c25, on origin) — see spikes/225-e1-interference-tick/dev-rounds/ROUND-2-O2-contention.md. This lane re-ran `o2_contention.py` and reproduced `o2-contention-output.txt` **byte-identical**; reproduction canary (glm-3 F14 published anchors, admit-all knob) PASS; self-canary (mislabeled arm) CAUGHT. Numbers verified real, no re-run needed beyond confirmation.
- **Item:** O2 — mag+C=1 admission vs admit-all, N∈{2,3,5,8} × C∈{1..N} × {calm,stress} × {raw, lag-compensated}, 5 seeds, 4800 ticks; decision rule: ≥2pp %w win at N≥3 uncompensated → promote sort to RTL (T2); win vanishes compensated → book "contention is a lag symptom."
- **Verdict:** REFUTED-as-booked / PARTIAL-CONFIRM — raw win is fan-out-gated (N=3: +0.1pp, N=5: +1.6pp, clears ≥2pp gate only at N=8: +11.9pp stress); under lag compensation the win EXPLODES (+24.1pp N=5, +56.2pp N=8), so "lag symptom" is false — the compensator synchronizes twins and *needs* the sort. T2 promoted to RTL with N≥6 boundary (round 3, de5ad6b).
- **Commit:** 9491c25 (round 2) · de5ad6b (round 3 boundary sharpening)
- **Headline:** mag C=1 vs admit-all, stress raw: +11.9pp at N=8 (57.8→69.7 %w, maxE 99.2→48.0); compensated: +56.2pp at N=8 (42.7→98.9).

---

## Round 3 — O3 (quanta floor) + O2b boundary — DONE (backfilled 2026-09-03 11:5x; see spike dev-rounds/ROUND-3-O3-quanta-floor.md)
- **Verdict:** PARTIAL-REFUTE / KNEE RELOCATED — ±5 fails 99% gate at K=2 stress (97.5%); adopt ±7 (4-bit) as ESP32/.qm default (≥99.2% everywhere). Z₃ debt inversion persists 8/8. O2b: contention wall located at N=6.
- **Commits:** 999348e (O3) · de5ad6b (O2b)
- **Headline:** ±7 is the floor (min retention 99.2% across all 8 K×regime cells)

## Round 4 — O4 (closed-loop regime motion) — DONE (2026-09-03 ~12:3x; backfilled 12:33 from commit b692aea)
- **Verdict:** BOUNDARY BOOKED — %w gate PASSED (adaptive 932‰ vs best-static 778‰, +154‰) but debt gate FAILED (57,136 > 32,770); NOT promoted to E4. κ-detector conflict entry 90 ticks vs 1600-tick dwell; L̂±1 knife-edge scar (bursty L̂=9→994‰, L̂=10→336‰). F19 doctrine confirmed in-run; E4 demo arm should pre-load blade+compensator+sequential with κ-dial as slow backstop.
- **Commit:** b692aea
- **Headline:** 932‰ beats every static arm on %w but fails debt gate — boundary booked with 90-tick detector lag + L̂ knife-edge.


## Round 5 — O5 (phase-decay coupling, multi-seed) — DONE (2026-09-03 12:5x; backfilled from commit ffecc06; see spike dev-rounds/ROUND-5-O5-phase-decay.md)
- **Verdict:** PROMOTED — +2.0pp stress mean, 5/5 seeds positive (F24 confirm); matched-duty admission gate destroys (−27.8pp) — decay-modulation vs admission-gating contrast is real.
- **Commit:** ffecc06
- **Headline:** +2.0pp stress, 5/5 seeds; gate at matched duty −27.8pp

## Round 6 — O6 (cofire homeostat) — DONE (2026-09-03; commits 3cee756 + 987d6e4; see spike dev-rounds/ROUND-6-O6-cofire-homeostat.md)
- **Verdict:** DEMOTE — v1.1 fails G1 (778‰ honest < 800‰) and G2 (no discriminative demotion); whistle G3 passes 3.4×. Cofire → v2 charter booked (predictability-not-agreement predicate, G1'/G2' + G4 gates); demo runs selection-only.
- **Commits:** 3cee756 (verdict) · 987d6e4 (v2 charter)
- **Headline:** 778‰ honest < 800‰ gate → cofire demoted to v2, demo selection-only

## Round 7 — O7 (bundle wall × compensation) — DISPATCHED 2026-09-03 13:39 AKDT
- **Item:** O7 — is the N=4 bundle-capacity wall (F7: true-residency 91%→10% by N≥4) lag-driven? Per-twin lag blades (F19/F20) + compensation, N∈{2..8} × {raw,comp} × {calm,stress}, 5 seeds, 4800 ticks. Decision: N=4 comp trueRes ≥50% ⇒ "stale-sensing capacity, not twin count"; unmoved ⇒ geometric two-law split.
- **Lane:** dev_o7_bundle_wall (zai/glm-5.3, run mode). Deliverable: dev-rounds/ROUND-7-O7-bundle-wall.md. Commit + push g3-kinduction mandated.
- **Verdict:** DONE — WALL MOVED — N=4 interference trueRes 12.2% → 86.3% with per-twin lag compensation (F19/F20 blade, 11/11 exact lag discovery): capacity law restated as "stale-sensing capacity, not twin count." New co-fire wall at N~7 (comp trueRes 61.3% at N=7 → 42.6% at N=8). Sequential arm hits 100.0% comp at every N. Lag blade verified 11/11 exact across lags 3–70; anchors replay 8/8 vs glm-1 sheet B; canaries 3/3 PASS (double-run byte-identity, anchor replay, self-canary CAUGHT).
- **Commit:** 0a637a1
- **Headline:** N=4 trueRes 12.2→86.3% (comp); co-fire wall relocates to N~7

## Round 8 — Q1 (class-grain boundary, linear-superposition substrates) — DISPATCHED 2026-09-03 14:2x AKDT
- **Item:** Q1 — map the class-grain boundary: embedding-census needs class grain (F5), Hadamard linear-superposition holds at identity grain (glm-2 #2, 13ppm). Axes: (1) nonlinear vs linear readout, (2) learned-vs-fixed coin dynamics, (3) 1-D vs 2-D dimensionality. Decider property identified or boundary honestly unmapped.
- **Lane:** dev_q1_class_grain_boundary (zai/glm-5.3, run mode). Deliverable: dev-rounds/ROUND-8-Q1-class-grain.md. Commit + push g3-kinduction mandated.
- **Verdict:** MAPPED — identity grain survives learned coin dynamics and 2-D substrates (linear superposition robust); nonlinear readout breaks only at the quantization floor and no grain rescues it. Decider is cut-vs-floor scale, not grain.
- **Commit:** ca836b8
- **Headline:** boundary decider = cut-vs-floor scale, not class grain

---

## Round 9 — Q2 (minimal cofire homeostat) — DISPATCHED 2026-09-03 14:55 AKDT
- **Item:** Q2 — is there a MINIMAL correction-channel homeostat with a provable no-collapse bound, or does every local no-error-signal rule learn silence? Test cofire v2 charter predicate (predictability-not-agreement, G1'/G2'/G4) + ≤3 minimal variants (refractory window, floor/decay, lagged reference) on the O6 harness.
- **Lane:** dev_q2_cofire_minimal (zai/glm-5.3, run mode). Deliverable: dev-rounds/ROUND-9-Q2-cofire-minimal.md. Commit + push g3-kinduction mandated.
- **Verdict:** pending (append on lane completion).
