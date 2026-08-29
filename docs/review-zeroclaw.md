# Review: zeroclaw — "The Field-Edge, in Fixed Points"

**Reviewer:** cross-review round 2 · **Files:** `proposals/zeroclaw/ARCHITECTURE.md` (no RTL-SKETCH.md)

## Strengths
- **Deepest architecture in the competition.** The core claim — the field reading (dials, μ̂,
  κ̂, edges) is O(latent) state updated by MAC/saturating-adds, stream never stored — is the
  only entry that engages the actual JEPA doctrine at the silicon level, with fleet-software
  provenance for every formula (elephant room.py, contrast.py, Sra 2012 κ̂ approximation).
- **The decay counter trick is the best single piece of math here:** integer W and age state,
  decrement interval `P₀ >> 2·msb(W)` integrates to `dW/dt = −W²/P₀` = the exact hyperbola
  `W₀/(1+W₀t/P₀)`, at the cost of one shared priority encoder + shifts. True power-law memory
  with *zero fixed-point state drift* ("integers don't drift; fixed point is used where it
  earns its keep, refused where it would rot"). This is doctoral-grade and cheap.
- **Math policy is the most rigorous of the field:** convergent rounding exactly at integrating
  boundaries (with the dial random-walk argument for why), saturate-never-wrap as a structural
  reused block, error bounds as TB assertions (ln-LUT ≤ 1.1e-3, κ̂ vs real bisection ≤ 3%).
- Honest failure modes section is exemplary: small-angle cosine below s1.14 LSB, κ̂ cliff at
  ρ→1, ρ bias at small N, staircase-is-an-envelope, area estimates "estimates."

## Weaknesses (real ones)
- **No skeletons. Zero.** Law 5 says "verified or it doesn't exist"; an entry shipping no
  compilable code fails its own gate at round 1. Its buildability score reflects plan-quality
  only — nothing here has touched iverilog.
- **Scope is the largest of the field:** vMF streaming, ln LUT, NR reciprocal/sqrt, effect
  FIFO with journal receipts, reverse-edge bookkeeping, dial bank, tick scheduler, link ports,
  ingress adapters. Each is credible; all together is the longest build of the five by far,
  and the riskiest.
- **Unverifiable provenance.** Citations point at fleet-internal repos (`/home/eileen/projects/
  elephant`, quilt-esp32 firmware, tit_quilt_elixir). Some were checkable in principle from
  this workspace; none were re-derived here. The κ̂ Sra bound (<3% for ρ∈(0.1,0.95)) is from
  the literature and stands, but the elephant line-citations are trust, not verification.
- **vMF at D=64 is conceded not to stream on small fabric** (view-time only) — the headline
  "field-reading is cheapest" is true at D=8 and qualified at D=64. Honest, but it means the
  tiny-fabric config ships a weaker brain than the thesis implies.
- No-drop effect semantics under storm = whole-ingress stall (conceded, §6.8) — correct by
  doctrine, throughput-hostile in practice; no mitigation (e.g., receipt-then-drop with
  journal replay) is even sketched.
- Single clock domain per cell; mesh CDC "honestly deferred" — same as everyone, but this
  entry's array story depends on it most.

## What it missed
- **Fabric-size portability:** three named configs with parameter table — good — but no
  interconnect story at all beyond "zc_link_port × N_LINK." How cells route to each other
  (the part glm and opencode actually designed) is absent. The winning entry will need one.
- **Testbench feasibility:** the TB *plan* table is the richest (behavioral golden quilt,
  stratified ln sweeps, envelope assertions) — but zero TB code exists to back it.
- **Purity:** policy-level excellent (no `initial`, no division, signedness explicit);
  unverifiable in code because there is no code.

## Scores
| Novelty | Buildability | Purity | Distribution | Total |
|---|---|---|---|---|
| 9/10 | 6/10 | 9/10 | 8/10 | **32/40** |

Best architecture, worst evidence. The decay trick and the rounding policy must survive into
whatever wins — see SCORECARD steal-list.
