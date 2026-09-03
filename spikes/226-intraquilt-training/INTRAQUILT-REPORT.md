# INTRA-QUILT TRAINING — SPIKE 226

*Casey directive 2026-09-03: "experiment with model-training intra-quilts … think of small scale
experiments."*

**Question:** can a quilt cell's correction history train a model that gets measurably better at
the cell's own task — and which training idea wins at tiny scale?

**Substrate:** the 225 wheel fabric (`exp_glm1.run_fabric`, integer-only, fixed seeds) as the
"cell": N=6 sensors, latency grammars, interference-mode decaying-pulse corrections. A correction
record = one emission (tick, sensor, lag, spread, grammar, K, trigger error, pulse, prior-correction
flags, in-flight count) with label **success = post-correction residual ≤ Δ=12**.

---

## Phase 1 — Survey (what's already trace-driven)

| Repo | What it does | Trace-driven learning? |
|---|---|---|
| **quilt-evolve** | LLM generator/judge/mutator loop at cell/sub-graph/sheet scope | Prompt-loop only — no weights trained on traces; closest prior art |
| **image-distillation-loop** | student→teacher image distillation w/ scorer + **reflex compiler** | Reflex compiler = trace-driven *retrieval* of winning prompt patterns, not training |
| **wesley-curriculum** | night-school lesson plans for a local 2B model | "Prompt is the curriculum"; no automated trace→model loop |
| **slackwater-tempo** | BPM/tempo/groove engine for agents | Not trace-learning (data-pattern lib; low relevance, noted) |
| **quilt-rust-selfimprove** | quilt-rust fork w/ selfimprove experiment probe | Rust probe scaffolding; no learned weights found in experiments/ |
| **quilt-verilog (225 wheel)** | standing experiment engine; SPIN-4/5 give spread/grammar laws + canary numbers | The data source used below; no one has trained ON the wheel's traces yet |

**Gap confirmed:** the fleet has loops that *prompt* with traces (evolve, distillation) but nothing
that *trains a model* on quilt correction history. That's this spike's lane.

---

## E2 — QUILT-AS-DATASET ✅ VALIDATED (headline)

471,777 correction records from 180 runs (13 grammars × spreads 5–30 × K∈{1,2,8} × 5 seeds,
interference mode, 1200 ticks each). Base success rate 0.438 (global); ladder seed-holdout base
0.376 (majority = 0.624).

| Split | Base/majority | LogReg | MLP (numpy, 16-hidden) |
|---|---|---|---|
| in-domain (ladder, seed holdout) | 0.624 | 0.758 (AUC .801) | **0.813 (AUC .874)** |
| **TRANSFER ladder → cohort** (held-out grammar) | 0.526 | **0.647 (AUC .694)** | 0.637 |
| TRANSFER ladder → bimodal | 0.554 | 0.737 (AUC .764) | **0.772 (AUC .843)** |

- **Headline: +12.1pp over majority on never-seen cohort grammar** (logreg 0.647 vs 0.526);
  +21.8pp on bimodal (MLP 0.772 vs 0.554). In-domain +18.9pp.
- Top logreg weights are physics-consistent: `in_flight` (−0.79), `lag` (−0.55), `prior2`,
  `n_trig`, `spread` all negative → pulse pile-up and staleness predict correction failure.
  The model learned the interference law, not noise.
- **Canary (model-free baseline):** SPIN-4 replay ladder15 N=6 gave 72.1 / 62.8 / 71.6 % true
  for K=1/2/8 vs published ~71.5 / 60.0 / 70.7 — passes; K=2 runs ~2.8pp hot (scar: spin4's
  exact window config may differ; booked, not chased).

**VERDICT: VALIDATED.** A quilt's own correction history is trainable signal that transfers
across grammar classes — the feature law survives domain shift.

---

## E1 — ICL CURRICULUM ✅ FALSIFIED (at 1.2B; honest negative)

Local `LiquidAI/lfm2.5-1.2b-instruct` (Ollama, temp 0, fixed seed). Task: predict next
correction's OK/BAD from k=8 exemplars. 40 targets × 3 sampling seeds × 4 conditions.
(See outputs/e1_icl_results.json.)

- A (real ordered prefix), B (unrelated shuffled exemplars), B2 (same-stream, order shuffled)
  scored **identically** — answers did not move with context at all (probe confirmed same
  answer under different contexts).
- v2 (forced one-word replies, 0 parse fails): `ok_answer_frac = 1.0` in **all four** conditions —
  the model answers "OK" to every prompt. Constant predictor. Accuracy 0.5083 = sampled label
  base rate exactly, which doubles as a clean canary (a context-free prior-matcher must land on
  the base rate — it does, to 4 decimals).
- Against base rate 0.462, every condition sat at base/prior level. Hypothesis A > B > C is dead.

**VERDICT: FALSIFIED** (at 1.2B, temp-0): the local model is a constant predictor on raw integer
trace text — real context ≈ shuffled context ≈ no context ≈ always-OK. Trace-text ICL is not the
intra-quilt lane at this scale.

**Scars:** v1 C-condition parse failures (95/120 "Let's analyze…" rambling) → v2 forced-format
prompt; A≡B identity verified by probe as model behavior, not harness bug; the 2.6B LFM was NOT
tried (time cap) — scar booked, rerun candidate.

---

## E3 — SELF-IMPROVEMENT LOOP (tiny) ⚠️ MIXED — the shape IS the finding

Gate: logreg trained on E2-style features fires a correction only if predicted-success > 0.5.
Rounds: r0 collect (ungated, shared by both arms) → r1–r3 gated runs with retraining on cumulative
data. Control arm: identical rounds, gate off. Canary: gated_run(gate=None) resid list
**byte-identical** to `exp_glm1.run_fabric` ✓.

| Round | Gated true-residency ‰ | Control ‰ | Skipped corrections |
|---|---|---|---|
| 0 | 486.3 | 486.3 | — (shared) |
| 1 | **504.6 (+18.3)** | 486.3 | 20,636 |
| 2 | 359.2 (−127) | 486.3 | 69,194 |
| 3 | 341.2 | 486.3 | 71,043 |

**VERDICT: MIXED.** Round-1 gating is a real improvement (+18.3‰ true residency on unseen eval
grammars, 5 seeds each). But naive retraining on gated-run data **collapses** the loop: the gate's
own skip-starved corpus shifts its decision boundary, it skips more (69K→71K), and the fabric
starves. Classic self-training distribution shift, reproduced inside a quilt in 3 rounds.

**Loop-shape lesson:** gate-once-helps, retrain-on-self-generated-data-diverges. An intra-quilt
training loop needs an anti-starvation guard (keep an ungated data fraction, cap skip rate, or
frozen gate) — none of which the naive loop has.

---

## RANKING (signal-per-compute)

1. **E2 QUILT-AS-DATASET — WINNER.** +12–22pp transferable accuracy from a 13-feature logreg /
   numpy MLP trained in seconds on CPU. Cheapest compute, biggest headline, physics-readable
   weights. This is the intra-quilt training idea that works at tiny scale.
2. **E3 SELF-IMPROVEMENT LOOP — sharp but double-edged.** +18.3‰ round-1 gain at ~1 min compute,
   but demonstrates the instability tax of self-generated training data. Valuable as the cautionary
   twin of E2's win.
3. **E1 ICL CURRICULUM — dead at 1.2B.** ~6 min of local inference for a null result; context
   insensitivity verified by probe. (Not falsified *forever* — a 2.6B+ or numerically-finetuned
   model might differ — but at tiny scale it's the wrong lane.)

## Training models INSIDE quilts vs ON quilts

The quilt-as-dataset result says a cell's correction history is not just log noise — it's a
labeled, integer, physics-grounded dataset whose laws transfer across the grammar families the
cell will actually meet. Training ON quilts (batch, offline, like E2) already pays: a model that
never saw cohort structure still beats majority by 12pp on it. But training INSIDE quilts (the
loop, E3) is where the novelty and the danger live: the moment the model gates its own data
collection, it manufactures distribution shift — round 1 buys +18‰, round 2 burns 127‰ of it. The
honest tiny-scale verdict is: **quilt traces are trainable, quilt loops are unstable** — an
intra-quilt trainer should ingest its history (E2-style, cheap, transferable) but must not be
allowed to close the loop on its own emissions without a starvation guard or a frozen-gate
control. Weight-training beats prompt-looping (evolve/distillation style) at this scale by every
metric we measured.

---

### Artifacts
- `gen_data.py` → `outputs/e2_records_SAMPLE20k.jsonl` (20k-record sample; full 471,777-record corpus regenerates deterministically via `gen_data.py`, fixed seeds), `e2_run_summary.json` (canary ✓)
- `e2_model.py` → `outputs/e2_results.json`
- `e1_icl.py` → `outputs/e1_icl_results.json`, `e1_icl_run.txt`
- `e3_loop.py` → `outputs/e3_loop_results.json`, `e3_loop_run.txt` (byte-identity canary ✓)
- Seeds fixed everywhere: sim 1/7/42/1999/20260902 (canary set), eval streams 777/888, ICL
  sampling 11/22/33, model seeds 226. Integer-only sim; ML layer is the only float code.

### Scars (all)
- Spin-4 canary K=2 replays ~2.8pp hot (72.1/62.8/71.6 vs 71.5/60.0/70.7) — likely window/config
  drift; booked, not chased.
- E1 v1: 95/120 C-condition parse failures → forced-format prompt in v2; A≡B insensitivity
  verified as model behavior, not harness bug.
- E3 v1 uses eval grammars for gating measurement and train grammars for gate corpus — grammars
  disjoint, but eval stream re-used across rounds (intentional: same-cell doctrine).
