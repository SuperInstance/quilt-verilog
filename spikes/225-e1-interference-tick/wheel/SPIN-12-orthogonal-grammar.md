# SPIN 12 — ORTHOGONAL-GRAMMAR (decoupling fresh-cohort × stale-mass)

**Lane:** bridge-run (after 2 subagent deaths; script from the second lane, executed directly) ·
**Date:** 2026-09-03 · **Files:** `spin12_orthogonal_grammar.py`, `spin12-output.txt` ·
Runtime: 10 s full grid (96 in-family obs + controls). Fabric: `inventors-derby/exp_glm1.run_fabric`
(delta=12, drift=6, pd=3, 4800 ticks, seeds {1,7,42,1999,20260902}, K ∈ {1,2,4}).

## Question

Spin 9's 3-param law (stale-mass + coherent-fresh-cohort, R²=0.877) was confounded:
every tested grammar varied fresh-cohort and stale-mass together. This lane decouples them
on a proper orthogonal grid and adjudicates causality.

## Verdict: FRESH-COHORT IS THE SECOND AXIS — CAUSAL, MONOTONE, AND IT INTERACTS WITH K

1. **Fresh-count is the dominant second parameter, stale-mass is nearly fungible.**
   Leave-one-out on the additive model: dropping n_f costs **−0.260 R²** (0.789→0.529);
   dropping m_s costs only **−0.018** (0.789→0.771). Spin 9's ordering was right, and now
   it's causal: at fixed m_s, each added fresh twin (lag ≤ δ) buys residency; at fixed n_f,
   how the stale mass is arranged barely matters.
2. **The winning model is n_f × K interaction** (G2: R² = **0.891**, beating Spin 9's
   confounded 0.877). The n_f×m_s interaction is noise (+0.005). The K-flip from Spin 9 is
   an **interaction with freshness**, not a separate axis: fresh benefit is largest at K=2
   (the echo-trough K) and compresses at K=4.
3. **Intra-stale dispersion: mostly fungible.** At fixed n_f/m_s, rearranging stale lags
   moves results ≤3pp at K=1–2; the one large effect (coh3_block −9.6pp at K=4) is the
   exception, not the rule — stale structure only starts to matter in the high-K regime.
4. **Where the law still fails:** outlier grammars (5 fresh + 1 stale) at K=4 —
   `out5_1` residual **+22.4pp** above additive fit. Extreme-fresh-majority grammars carry
   a protection the additive model can't express. Saturated cell×K ceiling R²=0.940:
   the remaining 6pp is within-cell internal structure.
5. **Zero-lock control replicated exactly** (K=1/2/4/8 = 77.3/50.0/73.9/69.0) — confirming
   the K=2 trough on the out-of-family grammar too.

## Canaries

- A: wiring byte-identity 40/40 PASS (this was the gate that caught the previous lane's
  invocation bug — the `fresher` helper was correct, its calls were wrong).
- B: Spin-9 replay anchors **exact per-seed to the permille**, events and debt counters
  identical (8756/8756, 14952/14952, 16616/16616, 14628/14628).
- C: determinism — canary-B ladder run byte-identical to the grid nf2_ms60 row, 5/5 seeds.

## Scars

- Two subagent lane deaths before bridge execution — concurrent GLM lanes starve
  (doctrine re-confirmed); experiment code survived both deaths and ran in 10 s once
  executed directly. Also: the WSL crash during this spoke left the tree on `master`
  with stray untracked wheel/ files (moved to `wheel.stray-master-20260903/`).
- The brief's "~74" zero@30 anchor is the **K=4** value (73.9), not a K-average —
  Spin 9's phrasing was ambiguous; pinned here.

## Next

- Model out5_1-class grammars explicitly (protection term for extreme fresh-majority).
- Fold n_f×K into the scheduler predictor (Kimi lane's features already carry both).

## "Near-fungible" — what it does and does not mean (for the non-WHEEL reader)

Setup in one breath: a *twin* is a scripted agent that replays recorded
behavior into the room; *fresh* twins replay recent recordings (lag ≤ δ,
they're reacting to the current stream), *stale* twins replay old ones.
The verdict says fresh-count is causal and "stale-mass is near-fungible
(+0.018)". That number means **arrangement doesn't matter — NOT presence
doesn't matter.** The +0.018 is the R² cost of dropping the stale-mass
TERM *conditional on fresh-count already being in the model*: given how
many fresh arrivals a grammar has, changing the stale crowd's size and
lag arrangement buys almost no additional prediction. It does NOT say
stale twins are causally inert: stale-mass ALONE still explains R²=0.529
of the grid — a room with no established crowd is a very different room.
The right reading for the analogy: the old crowd is the room's backdrop
and its sheer size does shift outcomes on its own; but once you know the
arrival profile, the backdrop's internal arrangement is furniture.
Concretely: you cannot fix a cold room by rearranging the regulars — you
add new arrivals (and the win is biggest in a loose-echo regime, §verdict
point 2). The claim that IS excluded: permuting stale lags matters ≤3pp
at K=1–2; the coh3_block exception (−9.6pp at K=4) marks where backdrop
structure starts to matter — in the high-K regime only.
