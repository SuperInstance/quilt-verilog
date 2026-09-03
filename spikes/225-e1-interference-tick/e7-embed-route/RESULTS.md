# E7-EMBED-ROUTE — Results

**Run:** 2026-09-02, night. Harness: `e7_embed_route.py` (pure stdlib, `python3 -u`, run2 = the reported run; run1 archived).
**Open lane:** `~/.openclaw/workspace/memory/open-lane-embedding-cells.md`
**Discipline:** integer-only route dynamics — embeddings quantized `round(v*S)` to int lattices (S ∈ {1000,250,100,40}), all distances/progress/tie-breaks exact integer arithmetic (Python bigints). Floats exist only inside model inference. Fixed seeds: pair seed 20260902, dither seeds 7/13/42.

## Setup

- **Corpus:** 120 single concepts, 4 domains × 30 (NAUTICAL, OBJECT, ABSTRACT, LANDSCAPE).
- **Models:** nomic-embed-text (768d), all-minilm:22m (384d), bge-m3 (1024d) — 3 families of trained embedders via local Ollama `/api/embed`. (Generative models rejected the endpoint: server not started with `--embeddings`; not restarted — system service.)
- **Cells:** corpus concepts snapped to integer lattices. A "route" for pair (A,B) = greedy max-progress walk over unvisited cells under integer hop-radius `hop2` = q25 of same-domain integer dist² (radius sweep q25/q50/q75 logged; dead-ends honest, capped 30 hops).
- **Pairs:** 60 frozen in `pairs.json` — 30 WARM (within-domain), 30 COLD (cross-domain, concrete↔abstract emphasis).
- **Metrics:** (a) quantization stability vs S=1000 baseline across severities × dither; (b) cross-model intermediate-cell Jaccard + hub top-10 overlap + hub-count Spearman + mismatched-pair nulls; domain-sequence LCS (coarse cell class) with its own null; (c) WARM vs COLD regime stats.

## Headline

**Routes are real (quantization-robust within model) but model-idiosyncratic (near-null cross-model at exact-cell grain), with consistent partial convergence at the coarse domain-class grain.**

### (a) Route convergence under quantization — YES

Mean intermediate-set Jaccard of routes vs the fine (S=1000) baseline, reference radius q25 (60 pairs; n = both-routed pairs):

| lattice | nomic | minilm | bge-m3 |
|---|---|---|---|
| S=250 (4× coarser) | **0.955** (95% routes identical) | **0.934** (95%) | **0.909** (97.5%) |
| S=100 | 0.849 | 0.724 | ~0.85* |
| S=40 (25× coarser) | 0.815 | 0.602 | 0.632 |

*run1 (80-concept corpus) value; same pipeline. Dither ±1 integer jitter (xorshift seeds 7/13/42, ~430/768 dims perturbed — verified) flips **zero** route decisions at any severity, any model.

→ Intermediate cells are **not lattice artifacts**: coarsen the grid 25× and jitter it, routes mostly survive. Same shape as E1's integer-dynamics finding, in embedding space.

### (b) Cross-model consistency — NO at exact-cell grain, PARTIAL at coarse grain

| pair | exact-cell Jaccard | (null) | domain-seq LCS | (domain null) | shared hubs |
|---|---|---|---|---|---|
| nomic ↔ minilm | 0.033 | 0.005 | 0.275 | 0.152 | 1/19 ('bluff') |
| nomic ↔ bge-m3 | **0.013** | 0.009 | **0.377** | 0.190 | 2/18 ('candle','grief') |
| minilm ↔ bge-m3 | 0.047 | 0.000 | 0.313 | 0.097 | 1/19 ('chaos') |

- **Exact cells: no convergence.** Lift over null is +0.005 to +0.047. Hub-count Spearman is negative in all pairs (−0.40, −0.40, −0.50) — caveat: sparse counts (hub usage 2–6), so read as "no stable shared hub ranking," not anti-correlation.
- **Coarse cells (domain class): consistent positive lift** in all 3 model pairs (0.28 vs 0.15, 0.38 vs 0.19, 0.31 vs 0.10). Models agree on the *kind* of cell a route transits far above chance, while disagreeing on the cell.
- Flavor: same pair `origin → … → virtue` routes as `origin > paradox > truth > virtue` (nomic) vs `origin > purpose > justice > virtue` (minilm) — same road's *shape*, different paving stones.

### (c) Regime dependence (cold vs warm) — YES, directionally consistent

| model | WARM hops / funnel | COLD hops / funnel |
|---|---|---|
| nomic | 0.90 / 0.20 | 1.33 / 0.27 |
| minilm | 0.90 / 0.10 | 1.17 / 0.20 |
| bge-m3 | 1.17 / 0.20 | 1.23 / 0.30 |

Cold (cross-domain) routes are longer and funnel through the model's top-3 hubs more than warm routes in all 3 models. Hub usage by domain: ABSTRACT cells are the #1 transit class in all 3 models (25/24/23 of ~70 uses) — abstract concepts are shared attractor territory, even though *which* abstract cell attracts is model-specific.

## Verdicts

1. **Route convergence (a): YES.** 0.934–0.955 Jaccard at 4× lattice coarsening; total dither immunity. The discrete cells a model routes through are stable objects of that model's geometry.
2. **Cross-model (b): NO at the exact-cell grain** (0.013–0.047 vs nulls 0.000–0.009) **— but PARTIAL YES at the domain-class grain** (domain-seq LCS ≈ 2–3× null in all pairs). Cells exist; their *identity* does not transfer across models. "Same geometry, different roads."
3. **Regime (c): YES.** Cold routes longer + more hub-funneling; abstract domain is the shared attractor class in all models.

**Most interesting number: 0.955 vs 0.013.** The same pipeline that is 95.5% self-consistent when the integer lattice is coarsened 4× (nomic) shows 1.3% exact-cell agreement between nomic and bge-m3. Route cells are maximally real within a model and maximally idiosyncratic across models — with the domain-seq lift (0.377 vs 0.190 null) showing where the transferable structure actually lives: one level up.

## Honest caveats

- Routes are short (mean 1.03–1.20 hops at q25); intermediate sets are 0–2 cells, so per-pair Jaccard is high-variance. The consistent near-null across all 3 model pairs (n=51–57) plus the detectable domain-level lift (measurement works when agreement exists) is why the negative still has teeth — but longer-route confirmation (below) would harden it.
- One routing policy tested (deterministic greedy, fixed across models). Policy is held constant, so cross-model differences are geometry, but other policies (A*, probabilistic walks) may route differently.
- Hub-count Spearman on sparse counts (2–6) is unstable; don't over-read the sign.
- Corpus is single words, 4 hand-picked domains; domain-seq result partly reflects that partition. Paraphrase-level stability (the lane brief's actual stability test) not yet run.
- Dead-ends at reference radius: 15% (nomic), 25% (minilm), 8% (bge-m3) — reported, not hidden; dead routes excluded from Jaccard means via the both-routed rule (n column).

## Tapestry note (for the lane's meta-question)

The convergence/divergence split landed exactly on **grain**: quantization-stable below, domain-transferable above, idiosyncratic between. Framework statement candidate: *cells emerge where the substrate quantizes itself — but the cells are the model's own; only coarse cell classes transfer.* That reframes the lane brief's "comparative cell census diff": the diff between two embedders' cell censuses is not noise to be averaged away — it IS each model's unique nature, exactly as booked.

## Next steps (E8 candidates)

1. **Longer routes**: tighter radius (q10) + bigger corpus → richer intermediate sets, harder test for the cross-model negative.
2. **Paraphrase stability** (lane brief's own test): same concept as 3 paraphrases — does the cell census stay fixed? This tests "cell is real" harder than quantization does.
3. **SAE/feature grain**: probe at discovered-feature granularity (the brief's predicted "yes, mostly" grain) rather than concept-cell granularity.
4. **Probabilistic routing**: k-best greedy or A*; does cross-model exact-cell agreement rise when the policy is less geometry-greedy?

## Artifacts

- `e7_embed_route.py` — harness (rerun: `python3 -u e7_embed_route.py > run.log 2>&1`; embeddings cached in `cache/`)
- `run2.log`, `metrics.json`, `routes_raw.json`, `pairs.json` — reported run
- `run1.log`, `metrics1.json`, `routes1.json`, `cache-run1/` — iteration 1 (80 concepts, q50 reference): same qualitative picture, archived per doctrine
- Not committed (per task).
