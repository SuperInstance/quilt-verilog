# O1 — K=2/3 CHAMPION REPLAY (dev round 1, night 2026-09-02)

*Overnight queue item O1 [RESEARCH-AGENDA §4]. Lane: glm-5.3 subagent, dev round 1.
Hypothesis: widening the tournament schema to K∈{1..8} yields entries beating the banked
champion on stress %w (glm-3 static probe: 94.2 vs 93.2); the ledger's calm specialist is
displaced by short-K interference at Δ=6 (92.1 vs impulse 56.6; 74.8 vs 56.6 on the pd axis).*

**VERDICT: CONFIRMED — and then some. New champion banked: `K=1, pulse_div=2, delta=16,
interference` — 96.1% stress %w, Pareto-dominating the old champion on all three axes.
Calm cell re-keyed at Δ=6 (98.0 vs impulse 56.6, holdout-confirmed). LLM still proposed
no K≤3 interference — grid anchoring booked as a standing arena bias.**

Reproduce: `cd inventors-derby && python3 o1_k_replay.py` → `o1-k-replay-output.txt`
(+ `o1-holdout-full.txt` for the full holdout table). Seeds {1, 7, 42, 1999, 20260902},
holdout {11, 313, 8888}, 4800 ticks, integer-only measurement (division only in report
aggregation, exactly the arena.py `score()` convention).

---

## §0 CONTROL ARMS — 10/10 PASS

Byte-match gates against every published number touched (champion row, glm-3 claim rows,
impulse-d16 unseen-entry control, gentle K=2, ledger-calm rows, arena-v2 baselines).
All PASS, 0 FAIL (full table in `o1-k-replay-output.txt`). No new claim below is read
from a harness that cannot reproduce the old numbers. Key gates:

```
banked champion K5/pd4/d16   (93.2, 132823, 38)   PASS
glm-3 claim K3/pd4/d16       (94.2, 139257, 39)   PASS
impulse d16 (unseen entry)   (96.0, 139949, 61)   PASS
gentle K=2 pd3               (92.1, 113573, 32)   PASS
ledger-calm impulse d12      (98.0,  55545, 53)   PASS
```

## §1 ARENA v3 — schema widened, static probes entered

`arena.py` widened: prompt constraint and parse clamp changed `1<=K<=16` → `1<=K<=8`
(two-line diff; rest of contract untouched). Static non-LLM probes entered at the
champion's own frame (d16, drift 6, lat 10), K∈{1,2,3} × pd∈{2,3} + glm-3's rows +
the champion itself. All rows scored on both regimes (stress + gentle + ledger-calm):

```
entry                          stress%   debt   maxE   gentle%  lcalm%
K=1 pd=2 d16  intf  ★NEW        96.1   121762   33     98.0    98.0
K=1 pd=3 d16  intf              95.6   157899   33     80.2    97.7
K=2 pd=2 d16  intf              95.1   111224   45     90.2    97.6
K=2 pd=3 d16  intf              95.7   127381   37     92.1    97.8
K=3 pd=2 d16  intf              93.1   116776   43     82.1    97.0
K=3 pd=3 d16  intf              95.1   123432   39     85.5    97.5
K=3 pd=4 d16  intf (glm-3)      94.2   139257   39     80.4    97.2
K=2 pd=4 d16  intf              94.1   150968   36     79.2    97.1
BANKED CHAMPION K=5 pd=4 d16    93.2   132823   38     55.1    97.2
impulse d16 (overnight control) 96.0   139949   61     56.6    98.0
```

**Every hypothesis-predicted displacement is real, and the probe grid found a better
entry than the one hypothesized.** Not one but SEVEN K≤3 entries beat 93.2 on the
primary seed set.

## §2 LLM ROUNDS — grid anchoring re-confirmed

granite3.1-dense:2b (the banked champion's own designer), arena v3 widened prompt,
2 rounds, leaderboard feedback including the probe's 94.2%:

```
round 1: K=4 pd=3 d=12 interference -> 83.1%
round 2: K=5 pd=5 d=16 sequential   -> 96.0%   (echoed impulse-d16; still no K<=3)
```

No K≤3 interference proposal — again. The model re-anchored on K=4 (the prompt's own
example) and then jumped mode entirely. Per the decision rule, **"grid anchoring" is
booked as a standing arena bias** (now observed in 4 rounds across arena v2 + v3) and
the static probe is promoted manually — the ledger banks results, not lineages.

## §3 HOLDOUT VERIFICATION (seeds 11, 313, 8888)

```
entry                    holdout%  per-seed         debt   maxE
K=1 pd=2 d16  ★          96.1     (96.1, 96.1, 96.1)  72518   35
K=1 pd=3 d16             95.6     (95.6, 95.6, 95.6)  94001   33
K=2 pd=2 d16             95.0     (94.9, 95.1, 95.0)  66807   42
K=2 pd=3 d16             95.7     (95.6, 95.8, 95.7)  76494   35
K=3 pd=2 d16             93.0     (92.8, 93.1, 93.0)  69111   42
K=3 pd=3 d16             95.0     (95.0, 94.9, 95.0)  74395   38
K=3 pd=4 d16 (glm-3)     94.4     (94.5, 94.4, 94.4)  83373   39
K=2 pd=4 d16             94.0     (94.1, 93.7, 94.1)  90008   36
CHAMPION K=5 pd=4 d16    93.1     (93.3, 93.1, 93.0)  79044   38
impulse d16 (control)    96.0     (96.0, 96.0, 96.0)  84888   61
```

7/7 K≤3 candidates beat 93.2% on holdout. K=1/pd=2 wins the primary set AND the
holdout with **zero seed variance on both** (96.1 on all 8 seeds run).

## §4 DECISION RULE APPLIED — new champion banked

**New champion: interference, K=1, pulse_div=2, delta=16** (stress regime drift 6/lat 10).

- **96.1% vs old champion 93.2%** (+2.9pp), holdout 96.1 vs 93.1.
- **Pareto domination of the old champion on ALL THREE axes**: pct 96.1>93.2, debt
  121,762<132,823, maxE 33<38. The "debt crown note" the decision rule anticipated is
  moot vs the old champion — but the stress-frame debt crown does NOT come with the new
  title: **K=2/pd=2/d16 holds it (111,224)**, and the maxE crown is shared K=1 pd2/pd3
  (33; K2/pd4's was 36). The stress Pareto front is now: K1/pd2 (pct + maxE),
  K2/pd2 (debt), K3/pd4 (interior, glm-3's row, still banked).
- K=1/pd=2 also **dominates the overnight impulse-d16 "unseen entry"** (96.0/139,949/61),
  which was itself the pct leader of the overnight sweep — the sequential arm's stress
  insurgency lasted one night.

**Calm cell re-keyed.** At Δ=6 (gentle-tight frame) the published calm specialist was
impulse at 56.6%: short-K interference displaces it exactly as hypothesized, only
harder — **K=1/pd=2 scores 98.0% vs 56.6** (the hypothesized K=2/pd=3's 92.1 was still
an underestimate of the axis). Holdout-confirmed (98.0 vs impulse 57.3). On the
ledger-calm d12 frame impulse keeps its seat (98.0 tie, debt 33,514 ≪ 57,264 on
holdout) — the re-key is Δ-specific, matching the overnight verdict that the calm
inversion boundary is a deadband-to-conflict property, not a mode property.

## §5 Ledger deltas

- Champion (stress): granite K5/pd4/d16 (93.2) → **static probe K1/pd2/d16 (96.1)**.
- Stress Pareto bank: add K1/pd2 (pct+maxE), K2/pd2 (debt crown 111,224); K3/pd4
  stays banked (interior). Old champion now dominated — demoted from champion, kept
  in the structural bank (first LLM-crowned champion; the lineage is the story).
- Calm (Δ=6) specialist: impulse (56.6) → **K1/pd2 interference (98.0)**.
- Calm (d12) specialist: impulse keeps (98.0, debt 55,545).
- Standing bias booked: **grid anchoring** — no LLM has ever proposed K≤3 interference
  in any round (arena v2 all K∈{4,5,8}; v3 rounds: K=4 then mode-jump). Static probes
  are now a permanent arena fixture (schema widened in arena.py v3).

## §6 What K=1 means (booked honestly)

K=1 pulses are single-tick corrections with no tail to smear — the "barely a wave"
regime the overnight replay flagged as chatter-prone at pd=3 (5,059 chatter) yet
pct-topping. At pd=2/d16 the deadband absorbs the chatter cost. This is not
"superposition wins"; it is "the shortest possible tail + coarse division + wide
deadband wins THIS frame." Whether K=1 still counts as the interference mode's thesis
or is a third mode ("quantized impulse") is a question for the next round, not this one.
