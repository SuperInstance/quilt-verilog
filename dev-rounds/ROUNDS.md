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

## Round 2 — O2 (contention controller boundary) — HELD
- **Checked 07:51 AKDT:** wheel lanes SPIN-6 (dispatched 07:02) and SPIN-11 (dispatched 07:42) both IN FLIGHT; 2-lane cap reached across wheel+dev-rounds. O2 dispatch deferred to next dev-rounds cycle when a lane frees.
- **Item (next up):** O2 — mag+C=1 admission vs admit-all, N∈{2,3,5,8} × C∈{1..N} × {calm,stress} × {raw, lag-compensated}, 5 seeds, 4800 ticks; decision rule: ≥2pp %w win at N≥3 uncompensated → promote sort to RTL (T2); win vanishes compensated → book "contention is a lag symptom."
