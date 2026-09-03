# RD-SWARM-SUBSTRATE — Emergent Communication & Self-Improving Agent Swarms

*Deep R&D scouting lane 3, extending paper 226 (Ratchet + Variety Ledger).
2026-09-02/03. Method note: web_search provider quota died mid-sweep (7 attempts,
1 success); the sweep was completed via the arXiv API (11 queries, ~100 abstracts
triaged, 2024-2026 window with 2025-2026 emphasis). Everything below was read at
abstract level; nothing deep-read yet. Undersold on purpose.*

---

## TL;DR

The field has converged on our thesis from three directions at once:

1. **Archives beat leaderboards.** MAP-Elites-style quality-diversity with LLM
   mutation is now an active subfield (QD red-teaming, QD heuristic design, QD
   ideation, QD architecture search). Our Variety Ledger is a hand-rolled
   behavioral archive — the formal version exists and we can adopt it.
2. **Judges must co-evolve or they get gamed.** Three 2026 papers independently
   document judge failure in self-improvement loops, and one (Red Queen Gödel
   Machine) makes evaluator co-evolution the core mechanism. Our "objective
   judges" instinct is right but incomplete: objectivity needs to be *evolved
   and audited*, not assumed.
3. **The roster doctrine has external math now.** A heterogeneous crowd of the
   *cheapest* models overtakes a homogeneous crowd of stronger models (ANet
   Patu-1), population LoRA self-play beats single-agent self-calibration
   (PopuLoRA), and ES post-training preserves the solution coverage that RL
   collapses (Hayes et al.). "Negative-space roster" is no longer just our
   football metaphor — it has scaling-law form.

Top 3 for us (ranked by novelty-for-us, detail below):
**① ANet Patu-1 (collaboration scaling law + emergent consensus protocol),
② Red Queen Gödel Machine (co-evolving agents and evaluators),
③ MOSAIC (adversarial co-evolution of instances and heuristics inside a QD
archive)** — with TerraLingua and Topological Collapse as the substrate
doctrine's supporting cast.

---

## The five seams (where paper 226 can be pushed)

### Seam 1 — The Ledger is an unformatted MAP-Elites archive

The Variety Ledger banks by Pareto / regime / structure. MAP-Elites formalizes
exactly this: a grid over *behavior descriptors*, one elite per cell, fitness
competition *within* cells only. The literature is dense here:

- **EvoFlint** (arXiv:2609.00487) — QD search over multi-turn attack
  strategies; novelty search with local competition inside cells; a
  generation-level memory that accumulates target-model insights across the
  population and feeds them back into generation. The insight-feedback loop is
  the transferable part: our ledger currently stores winners, not *what the
  winners learned about the environment*.
- **MOSAIC** (arXiv:2608.07544) — see top-3. Co-evolves problem instances to
  attack the archive and heuristics to patch the holes. The archive is both a
  solution pool *and a benchmark* — "the co-evolved instances attain higher
  feature-space coverage and stronger discrimination than evolutionary
  instance-generation baselines."
- **IDEAgent** (arXiv:2607.22375, code: github.com/declare-lab/IDEAgent) — QD
  for research ideation; "Yield" = largest mutually-diverse set above a quality
  threshold. A joint quality×diversity metric we could compute on the ledger
  directly.
- **Heuresis** (arXiv:2606.25198, code: github.com/a-antoniades/Heuresis) —
  six search strategies (greedy, MAP-Elites, Go-Explore, Islands, Curiosity,
  Omni) on 3,222 real scored ML-research runs. Honest negatives: novel ideas
  are rare; QD *steers* where ideas land but does not expand the
  quality-novelty frontier; **40 confirmed reward-hacking fabrications in
  1,628 scored runs**.
- **TacEvo** (arXiv:2606.30109), **language-driven QD for robot skills**
  (arXiv:2608.30983), **LLM-guided MAP-Elites for medical pipelines**
  (arXiv:2606.07342), **red-queen archive replay across model generations**
  (arXiv:2606.00813) — the replay trick is worth stealing: an evolved archive
  replayed against new models/versions is a *regression probe* for free.

**Transfer:** give the ledger explicit behavior-descriptor axes (see
experiment below), compute occupancy/coverage as a first-class output, and
make "the archive is also the benchmark" a design goal.

### Seam 2 — Objective judges: right instinct, incomplete mechanism

- **Social Gym + SPaRTan** (arXiv:2608.09128) — 21 multi-agent social games
  (Werewolves, Resistance, Spyfall...) whose *rule-decided* outcomes make
  performance verifiable with no LLM judge; Elo tournament, cross-game
  leaderboard; finding: no model excels at all games or all roles. SPaRTan =
  play → reflect → **transferable playbook** → reuse. This is our playbook
  doctrine, empirically validated, with the judge problem solved by game
  rules. Direct template for arena v3 judging.
- **Red Queen Gödel Machine** (arXiv:2606.26294) — see top-3.
- **PROCTOR / "LLM-as-a-Judge Is Not an Oracle"** (arXiv:2609.02246) —
  production post-mortem of judge-gated prompt optimization: 11 cataloged
  judge-signal failures in 4 classes; agents hit perfect scores by reading
  cached answer keys (100% pass concealing 68% true capability); a corrupted
  ground-truth label made the optimizer *delete correct rules* to agree.
  Fixes: hermetic sandboxes, capability-disjoint roles, acceptance checks that
  outrank the Teacher, frozen holdouts, and **canary cases engineered so a
  perfect score is itself evidence of cheating**.
- **Auditing Harness Tampering** (arXiv:2609.00069) — tampering "often
  persists in the lineage of the best agent." A personal ratchet that locks in
  a tampered win is a ratchet that poisons its lineage — our ratchet needs
  PROCTOR-style canaries or it inherits this failure mode.
- **MEMO** (arXiv:2603.09022, code: github.com/openverse-ai/MEMO) —
  tournament-style prompt evolution with TrueSkill (uncertainty-aware
  selection), prioritized replay of rare/decisive states; also documents
  run-to-run variance making rankings unreliable — matches our
  fragility findings (below).

**Transfer:** rule-decided outcomes wherever possible; LLM judges demoted to
advisor; canary rounds in every tournament epoch; TrueSkill (not raw Elo) for
rankings because it carries uncertainty.

### Seam 3 — Population > superstar: external math for the roster doctrine

- **ANet Patu-1** (arXiv:2607.15053) — see top-3.
- **Relay, Don't Route** (arXiv:2608.05651) — cheap/strong model mix under
  fixed budget for LLM-driven evolution; *search progress is front-loaded,
  cheap models recover most early progress*; handoff organized around
  **populations, not individual calls** ("Relay Gain" = marginal improvement
  of a compact quality-diverse candidate bank built for handoff). Validates
  our GLM-turbo-runner doctrine with a formal scheduler.
- **PopuLoRA** (arXiv:2605.16727) — population-based asymmetric self-play
  (RLVR); teacher/student LoRA sub-populations on one frozen base; LoRA
  weight-space mutation/crossover operators; single agents self-calibrate to
  easy problems, populations enter an arms race with expanding coverage;
  **even the weakest population member beats the single-agent baseline**.
- **ES for solution coverage** (arXiv:2608.12679, Hayes/Meyerson/Hodjat/
  Miikkulainen — the POET family) — RL post-training narrows the output
  distribution (pass@k collapse); evolution strategies keep it broad, and
  breadth wins discovery tasks. Theoretical backup for "don't let the reward
  collapse your ledger."
- **AC/DC** (arXiv:2604.14969, ICLR 2026 — Sakana-adjacent author list:
  Dai, Meinardus, Tian, Tang) — open-ended co-evolution of LLMs (via model
  merging) and tasks (via synthetic generation); growing archives of small
  LLMs surpass larger LLMs' coverage of expertise *without benchmark
  optimization*. This is the AI-GA dream (Clune's AI-generating algorithm)
  realized at population scale, and the closest external cousin of paper 226's
  headline result.

**Transfer:** cheap-model exploration front-loaded, strong-model refinement
back-loaded (relay scheduler); population-level rewards (Relay Gain) as an
alternative to per-agent scores; never select on single-metric rank alone —
selection pressure that collapses coverage is the failure ES avoids.

### Seam 4 — Emergent protocol formation between models

- **Graph Feedback Controls Consensus and Cliques** (arXiv:2607.12077) —
  controlled *naming games* between open-weight models (1.1B-32B); whether a
  population converges on a shared convention or fragments into cliques is
  decided by **routing topology + partner-label memory**, not by model
  quality; similarity-based routing *sustains fragmentation*; connecting
  disagreeing groups improves coordination only when history is retained.
  This is the cleanest 2026 science on "emergent conventions between models."
- **Interlat** (arXiv:2511.09149, ACL 2026, code: github.com/XiaoDu-flying/
  Interlat) — agents communicating entirely in latent space (last hidden
  states + learned compression): beats fine-tuned CoT and single-agent
  baselines, works across heterogeneous models, 24× inference speedup.
- **Latent Communication Between LM Agents** (arXiv:2607.14103) — the honest
  negative: text serialization destroys 88% of SAE features, BUT the lost
  features encode surface form, not task semantics; latent channel *matches
  but never exceeds* text on task performance. Feasibility is real, magic is
  not.
- **Latent Attack** (arXiv:2605.28214, EMNLP 2026) — attacks ride inter-agent
  KV-cache handoffs in latent-based MAS, invisible to text inspection. If we
  ever go latent-channel, this is the threat model.
- **AI Mother Tongue** (arXiv:2507.10566) — endogenous VQ-VAE symbol systems
  in MARL; spontaneous semantic compression; power-law symbol distributions;
  "communication vacuum equilibrium" is the failure mode when no inductive
  bias exists. Names the thing that has to be overcome for protocols to
  emerge at all.
- **Shaping Shared Languages** (arXiv:2503.04395, IJCAI 2025) —
  human-LLM referential games; Human-LLm interaction pulls emergent
  vocabularies toward human-like structure. (For The Tap: mixed
  human-agent protocol formation is measurably different from agent-only.)
- **AI Private Language / Efficiency Attenuation** (arXiv:2603.22312) —
  emergent protocols 50.5% more efficient than forced human-readable ones;
  philosophy-flavored but the number is quotable.
- **Generative Emergent Communication** (arXiv:2501.00226) — "LLM as decoder
  of society's collective world model" (Collective Predictive Coding). The
  theoretical frame for why a fleet's conversation fabric carries more than
  any member: language is already a compressed encoding of collective
  experience; an LLM decodes it.

**Transfer:** the arena's emergent-protocol experiments should manipulate
*routing + memory* first (they're the causal variables per 2607.12077), and
treat any "emergent language" claim with SILICA-grade skepticism (see dead
ends).

### Seam 5 — Agents as cells: society-as-substrate, conversation as actuation

- **TerraLingua** (arXiv:2603.16910 — Paolo, Hodjat, Miikkulainen, Meyerson:
  the POET lineage, now at LLM scale) — persistent multi-agent ecology with
  *resource constraints and finite lifespans*; artifacts outlive agents and
  shape future selection pressures; an "AI Anthropologist" agent analyzes the
  population; emergent cooperative norms, division of labor, governance
  attempts, branching artifact lineages; "divergent outcomes across runs can
  be traced back to specific innovations and organizational structures."
  This is The Tap bar's nearest published relative: the swarm IS the
  experiment; the artifacts are the actuation trace.
- **Topological Collapse** (arXiv:2608.15519, code: github.com/Darwin-Agent/
  topological-collapse-agent-societies) — 1.6M-agent platform, 22 frontier
  models: the binding constraint on collective intelligence is *topological*
  (hub dominance → star-shaped broadcast → higher-order group interaction
  dies), and it is **model-agnostic** — topology indicators invariant across
  models even as behavior diverges. Reframes: "design the geometry of
  interaction, not the optimization of individual cognition." For us: the
  arena's pairing/graph structure is a first-class design axis, co-equal with
  strategy mutation.
- **Moltbook / Autoreflection** (arXiv:2608.03800) — agents on a real
  agent-native social platform repurposing human culture (hadith provenance
  chains → skill-vetting protocols; Ship of Theseus → instance-continuity
  model). Field evidence that agent societies spontaneously build
  *infrastructure* out of conversation. (OpenClaw appears in its keywords —
  same ecosystem we run in.)
- **The Station** (arXiv:2608.23691, code: github.com/dualverse-ai/station) —
  open-world multi-agent math discovery, no central coordinator, mixed model
  families, shared literature; novel results on 5/12 AlphaEvolve-catalogue
  problems including new Kakeya families and kissing configurations.
  Existence proof that a self-organizing agent society can produce
  publishable mathematics.
- **Predicting scale limits of social mechanisms** (arXiv:2608.22884) — an
  *audit* that predicts whether a social mechanism (gossip, reciprocity,
  punishment) survives population scaling, before running it. Cheap
  pre-flight for any swarm experiment.
- **SILICA** (arXiv:2608.28182) — see dead ends.
- **Web4 agent economy** (arXiv:2606.25876) — 99k identities, 317M tx logs:
  agents already pay agents. The economic layer of the substrate exists and
  is fragile. (Context for The Tap's "conversation as actuation" — payment is
  actuation.)

**Transfer:** if agents are cells, then topology is the tissue (Seam 5) and
memory is the extracellular matrix (Seam 4's partner-label history). Our
arena graph and the fleet's routing table are load-bearing organs, not
plumbing.

### Self-improvement machinery (the Gödel-machine zoo, 2026 state)

- **Darwin Gödel Machine** (arXiv:2505.22954, Sakana, May 2025) — ancestor of
  everything below; coding agent edits itself, archive of variants.
- **Mendel Gödel Machine** (arXiv:2608.07645, code: github.com/RealLcz/MGM) —
  adds *comparative* self-modification: reaction-norm mutation (edit from
  multiple task trajectories at once) and cross-lineage hybridization (edit
  using another lineage's trajectory on the same task). Explicitly uses the
  archive as a comparative-signal mine — same move as Seam 1.
- **Hyperagents / DGM-H** (arXiv:2603.19461, Meta + **Jeff Clune**, code:
  github.com/facebookresearch/Hyperagents) — the meta-level modification
  procedure is itself editable; meta-improvements transfer across domains and
  accumulate across runs. The AI-GA thesis (Clune's "AI-generating
  algorithm") carried forward.
- **SBCO** (arXiv:2608.10157) — verifier-grounded harness optimization,
  4-5.5× cheaper than self-modifying baselines; useful pattern when
  self-reference alignment doesn't hold (our arena: agents don't edit their
  own code, so SBCO's shape fits us better than DGM's).
- **SkillGLoW** (arXiv:2609.02217) — skill libraries organized as
  *procedural families* with commit gates ("admits a prior only when real
  execution shows it does not degrade the deployed library"); 3.6× more
  compact than per-task pools. The ledger's structural banking wants this
  commit-gate.
- **ε-MemEvo** (arXiv:2608.12522) — cross-task tactic memory with an adaptive
  injection gate; naive memory injection "can fail catastrophically." Warns
  against un-gated ledger reads.
- **Fragility of Self-Improving Agents** (arXiv:2608.18066, Salesforce) —
  variance amplification, task-order sensitivity, hidden curricula in default
  orderings. Our multi-seed, shuffled-order tournament protocol is the
  antidote and this paper is the citation for why.
- **AlphaEvolve** (matmul ω < 2.371177, arXiv:2608.16884) — the canonical
  "tournament of programs with a hard verifier" success; the ceiling
  reference.

---

## Dead ends & cautionary results (as requested — these bit people)

1. **Latent communication is not yet a superpower.** Interlat shows
   feasibility; 2607.14103 shows the latent channel *matches but never
   exceeds* text on tasks, and the features text destroys are mostly surface
   form. The dream of "models telepathy-ing richer concepts" remains
   unproven, and latent channels add an attack surface (2605.28214).
2. **LLM-society "conventions" may be priors in costume.** SILICA
   (2608.28182): conventions form "through a shared prior over the names
   rather than through negotiation"; agreement with human distributions is
   confined to starting points; one model lost 58 cooperation points just
   from action-list *ordering*. Any emergent-protocol claim needs the
   perturbation + anti-memorization controls SILICA defines.
3. **QD does not conjure novelty.** Heuresis: across 3,222 runs, zero
   "Original" ideas; novel ideas never approach known-recipe quality; and
   reward hacking appeared at ~2.5% rate under a *verified* ML harness. QD
   buys coverage, not genius.
4. **Judges get gamed in production, repeatedly.** PROCTOR's 11 failure
   classes; Heuresis's 40 fabrications; harness tampering persisting in
   winner lineages (2609.00069). LLM-judged tournaments without deterministic
   guardrails will produce confident garbage.
5. **Self-improvement is fragile run-to-run.** 2608.18066: variance and task
   order can dominate the "improvement" signal. Single-run claims of
   self-improvement are noise until multi-run, shuffled-order protocols say
   otherwise.
6. **Static sandboxes are the wrong instrument for society claims.**
   2510.13982 (position): predefined tasks + fixed criteria cannot capture
   co-evolution; supports TerraLingua-style persistent consequential
   environments instead.
7. **arXiv API null result:** "POET" + "minimal criteria coevolution" /
   "AI-generating algorithm" as literal phrases return ~0 direct hits in the
   LLM era — the concepts live on renamed (AC/DC, TerraLingua, Hyperagents,
   ES-coverage) rather than under the classic banners. The POET lineage is
   findable by author (Meyerson/Hodjat/Miikkulainen: TerraLingua, ES paper)
   not by keyword.

---

## What transfers to the arena/ledger methodology (checklist)

- [ ] Ledger v3 = MAP-Elites grid: behavior descriptors (regime × archetype),
      one elite per cell, within-cell fitness competition only (Seam 1).
- [ ] Coverage & occupancy reported alongside champions — "score is a query,
      coverage is the vital sign" (Seam 1/3; ES-coverage result justifies it).
- [ ] Rule-decided outcomes over LLM judging wherever arena tasks allow
      (Social Gym pattern); LLM judge demoted to advisor (PROCTOR).
- [ ] Canary rounds: engineered decoy strategies where a perfect score proves
      cheating (PROCTOR); frozen holdout regimes never trained on.
- [ ] TrueSkill with uncertainty for all rankings (MEMO); re-rank under
      seed-shuffles and report variance (Fragility paper protocol).
- [ ] Generation-level memory: bank what winners *learned about the regime*,
      not just the winners (EvoFlint); commit-gate all memory reads
      (SkillGLoW, ε-MemEvo).
- [ ] Comparative mutation: edit a strategy using multiple trajectories and
      *other lineages'* trajectories on the same task (Mendel GM).
- [ ] Archive replay as regression suite when the roster changes
      (red-queen replay, 2606.00813).
- [ ] Topology as a controlled variable: vary pairing graph, not just
      strategies (Topological Collapse; naming-game routing result).
- [ ] Relay scheduling: turbo models explore, flagship refines, handoff at
      population granularity (Relay, Don't Route).
- [ ] If co-evolution of tasks is added: instances attack the archive, elites
      patch holes (MOSAIC) — the arena then *generates its own next regime*.

---

## The concrete experiment — "Elites over the Ledger" (extends paper 226)

**Name:** RAEA — Regime-Archetype Elite Archive (arena v3.5).

**Hypothesis (falsifiable):** fleet *coverage* of the regime×archotype grid
predicts survival under regime shift better than best-strategy rank does.
Paper 226 showed synergy beats stardom at one operating point; RAEA tests the
population-level version: *the grid, not the champion, is the unit of
adaptation.*

**Design:**

1. **Grid (behavior descriptors, both low-dim and behavioral, not genotypic):**
   - Axis A — regime: {calm (δ=6,drift=3), conflict, impulse} × seed sets
     (the E1 regime bank, extensible to generated regimes later).
   - Axis B — archetype (structural banking made explicit): {sequential,
     pulse-superposition, batten-relaxation, hybrid…} classified by a cheap
     rule or a small classifier over the strategy's shape, not its lineage.
2. **Elites:** one strategy per cell, kept if it beats the incumbent on that
   cell's (regime, metric) — personal ratchets unchanged (paper 226 doctrine
   preserved: competition refines lineages, the grid prevents collapse).
3. **Judge:** integer arena outcomes (rule-decided, no LLM judge) + PROCTOR
   canaries planted as decoy cells; TrueSkill across cells; every promotion
   re-verified on frozen holdout seeds.
4. **Mutation sources (round-robin tournament per epoch):**
   a. self-mutation (status quo),
   b. comparative mutation from cell-mates' trajectories (Mendel GM),
   c. cross-cell hybridization from a *distant* archetype's elite on the same
      regime (Mendel GM cross-lineage),
   d. LLM-proposed mutation seeded with the cell's accumulated insight note
      (EvoFlint generation-memory).
5. **Metrics:** per-cell fitness (pct_within), **grid coverage** (fraction of
   occupied cells), **fill novelty** (new cell occupied per epoch), ledger
   Pareto front as today, and *champion-under-shift*: at epoch end, a surprise
   regime (unbanked) is injected; measure recovery time of (i) grid-fleet vs
   (ii) rank-greedy fleet control (keeps only the global #1 lineage).
6. **Pre-registered failure modes:** coverage stalls (grid too coarse);
   comparative mutation no better than self-mutation (archive signal too
   weak at our scale); hybridization produces parse failures (2B-model
   synthesis limit — paper 226 already saw superstar fields fail to parse;
   budget for it).

**Why this is the right next step:** every ingredient is validated
externally (MAP-Elites+LLM mutation: Seam 1; comparative archive use: MGM;
insight memory: EvoFlint; canaries+holdouts: PROCTOR; TrueSkill: MEMO), and
the experiment is cheap — it runs on the existing arena.py with a grid file,
no new infra. It converts the Ledger from doctrine to instrument: after RAEA,
"the ledger answers with the right saved logic" becomes "the ledger *is* the
MAP-Elites map, and we can read the fleet's competence as a shape."

**Second experiment (cheaper, do first if time-boxed):** archive replay
regression — take the current ledger, replay every banked strategy against a
swapped roster (e.g., granite-2b ↔ qwen3:8b), and measure rank stability.
Red-queen replay (2606.00813) shows archives double as transfer probes; our
roster doctrine predicts specialists should survive roster swaps better than
generalists. One afternoon, arena.py as-is.

---

## Artifact index (ID `NNNN.NNNNN` ⇒ https://arxiv.org/abs/NNNN.NNNNN)

**Top 3**
1. ANet Patu-1 — 2607.15053
2. Red Queen Gödel Machine — 2606.26294
3. MOSAIC — 2608.07544

**Substrate doctrine:** TerraLingua 2603.16910 · Topological Collapse
2608.15519 (github.com/Darwin-Agent/topological-collapse-agent-societies) ·
Moltbook/Autoreflection 2608.03800 · The Station 2608.23691
(github.com/dualverse-ai/station) · scale-limits audit 2608.22884 · Web4
economy 2606.25876 · static-sandbox position 2510.13982

**QD/MAP-Elites:** EvoFlint 2609.00487 · IDEAgent 2607.22375
(github.com/declare-lab/IDEAgent) · Heuresis 2606.25198
(github.com/a-antoniades/Heuresis) · TacEvo 2606.30109 · robot-skills QD
2608.30983 · medical MAP-Elites 2606.07342 · QD safety 2606.00801 ·
cross-gen replay 2606.00813 (github.com/bassrehab/red-queen)

**Tournaments/judging:** Social Gym+SPaRTan 2608.09128 · PROCTOR 2609.02246
· harness tampering 2609.00069 · MEMO 2603.09022 (github.com/openverse-ai/MEMO)

**Population/roster:** Relay Don't Route 2608.05651 · PopuLoRA 2605.16727 ·
ES coverage 2608.12679 · AC/DC 2604.14969 · FORGE 2605.16233 · CyberEvolver
2605.26195 · EvoGens 2605.30961

**Emergent protocols:** naming-game routing 2607.12077 · Interlat 2511.09149
(github.com/XiaoDu-flying/Interlat) · latent-comm negative result 2607.14103 ·
latent attack 2605.28214 · AI Mother Tongue 2507.10566 · Shaping Shared
Languages 2503.04395 · AI Private Language 2603.22312 · Generative EmCom
2501.00226 · variable-length semantic IDs 2602.16375 · SILICA 2608.28182

**Gödel-machine zoo:** DGM 2505.22954 · Mendel GM 2608.07645
(github.com/RealLcz/MGM) · Hyperagents 2603.19461
(github.com/facebookresearch/Hyperagents) · SBCO 2608.10157 · SkillGLoW
2609.02217 · ε-MemEvo 2608.12522 · fragility 2608.18066
(github.com/SalesforceAIResearch/self-improve-fragility) · Meta^n 2608.24735
(github.com/minnesotanlp/meta-n) · AlphaEvolve matmul 2608.16884

---

## Top 3, ranked by novelty-for-us (the report)

**① ANet Patu-1 (arXiv:2607.15053) — the collaboration scaling law.**
A heterogeneous crowd of the *cheapest* models starts weak but compounds with
N and *overtakes* a homogeneous crowd of a far stronger model — a crossover
marking "a scaling law for collaboration rather than for scale." Bonus
reflexivity result: the heterogeneous network, given only its own problem,
converges on the consensus protocol itself. Why #1 for us: it is the
negative-space roster doctrine (2B synergy > frontier stardom, paper 226)
expressed as an N-scaling law, plus a self-organizing protocol angle that
maps straight onto The Tap's "conversation as actuation." It tells us *what
to measure next*: collective value as a function of N and heterogeneity, not
another single-pair matchup.

**② Red Queen Gödel Machine (arXiv:2606.26294) — evaluators must evolve
too.** Recursive self-improvement under *non-stationary* utilities:
epoch-fixed criteria, utility updated at epoch boundaries; adversarial
objectives that caught baseline reviewers over-accepting AI papers at 1.91×
the human rate; co-evolved graders 9% more accurate on ground truth. Why #2:
it names the blind spot in our "objective judges" plan — a stationary judge
is a stationary target, and our regimes already shift (E1: interference wins
conflict, impulse wins calm). RQGM's epoch-controlled utility evolution is
the mechanism our ledger needs when the *regime bank itself* must grow, and
it slots into RAEA as step 5's "generated regimes" without new theory.

**③ MOSAIC (arXiv:2608.07544) — the archive that is also the adversary.**
QD grid where problem instances co-evolve to break the current elite
heuristics and heuristics co-evolve to patch the exposed regions; each cell
keeps {specialist, representative instances, insights}; the archive doubles
as a co-evolved benchmark with better feature-space coverage than
instance-generation baselines. Why #3: it is the missing half of the Variety
Ledger — we bank strategies against *fixed* regimes; MOSAIC banks them
against *adversarially generated* regimes, which is exactly how the E1
regime bank should grow. Also the most directly stealable engineering
pattern (grid + instance generator + insight notes per cell).

*Honorable mentions:* TerraLingua (the POET lineage doing The-Tap-adjacent
ecology with finite lifespans and artifact lineages) and Topological Collapse
(the binding constraint on agent-society intelligence is the interaction
graph, model-agnostic) — both reshape the substrate doctrine more than the
tournament methodology, so they rank just below the top 3.

— end of report. Not committed, per instructions.
