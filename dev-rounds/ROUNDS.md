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
