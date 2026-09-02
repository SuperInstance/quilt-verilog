# WORLD-CLASS GAP — the cutting-edge survey, ranked

**Lane:** cutting-edge survey (relaunch 2026-08-31; the first lane died after
finding "NoC-Out" and saving nothing — this doc commits early and often).
**Branch:** `world-class-survey`. **Inputs:** the survey brief
(`WORLD-CLASS-SURVEY-BRIEF.md`), `CUTTING-EDGE-rtl.md`, `FORMAL-PROOFS.md`,
`coherence-arena/VERDICT.md`, `INDEX.md`, internal SuperInstance prior art,
and an external sweep (arXiv API; Gemini search quota was exhausted
mid-survey, 429, so the sweep leans on arXiv + known literature — noted as
a coverage limitation in §4).

**Baseline (ours):** Verilog-2005 cellular fabric; N cells on a ring,
flit-based messaging, 5+1 opcodes, conserved cellular state; formal suite
with PDR-closed UNBOUNDED conservation (machine-derived 854-clause
invariant committed, `docs/PDR-IVARIANT.md`); fabric-level Python-vs-RTL
cosim bit-exact at NCELL=2 (30/30 at second-generation seed), NCELL=4/8
parameterization in flight on `cosim-scaleup` (commit 5d9d848);
coherence-arena synthesis verdict landed (`coherence-arena/VERDICT.md`).

---

## 1. Ranked: the ten things that would make quilt-verilog world-class

Each row: **field's best → ours → gap → path in OUR architecture (Verilog-2005,
conservation, ring) → difficulty** (S/M/L, or **PORT** where internal prior
art applies).

### G1. Parametric-structure correctness proof — difficulty: L
- **Field:** **NoC-Out** (arXiv:2608.24478, Aug 2026 — the dead lane's lead,
  confirmed) is "the first library/generator for formally-verified
  k-dimensional NoC designs," built by extending **Kôika**, a rule-based HDL
  embedded in the **Rocq theorem prover**, with "a program logic for modular,
  automated reasoning." Every generated NoC "is equipped with a proof that it
  refines our formal NoC specification; no additional verification effort is
  required," including "a strong liveness guarantee."
  (https://arxiv.org/abs/2608.24478)
- **Ours:** proofs are per-instance: PDR closed conservation at NCELL=2
  (unbounded), k-induction open past 130, and the invariant is
  machine-derived, not yet human-minimal (`docs/PDR-IVARIANT.md`).
- **Gap:** they prove the *generator*; we prove *instances*. Every NCELL bump
  re-runs the whole formal battery.
- **Path:** a **parameterized proof** — induce on ring position: prove the
  single-cell interface contract (FIFO discipline + conservation credit) once,
  then argue composition along the ring (each cell's egress flit stream is the
  neighbor's ingress). The PDR invariant's clause families are already
  positional/uniform ("pipe-content hypothesis `!u_pipe.m_a0[3]` in 752/854
  clauses" — a per-cell pattern), which is exactly the shape a
  parameterized proof needs. Verilog-2005 compatible: no HDL change, just
  proof structure (candidate: induction on NCELL with SBY per-cell lemma +
  compositional argument in Isabelle/Rocq prose; or ABC `pdr` on a symbolic-N
  miter if the toolchain tolerates it).
- **Why ranked #1:** it is the single structural advantage the field has over
  us — *scale-invariance of proof* — and the field only just claimed it
  (Aug 2026). Closing it makes our NCELL=2→4→8 cosim story a special case of
  a theorem instead of a measurement campaign.

### G2. A stated-and-proven liveness (delivery) guarantee — difficulty: M
- **Field:** NoC-Out proves "a strong liveness guarantee, which consequently
  applies to all generated NoCs" (2608.24478). Duato's classic necessary and
  sufficient conditions for deadlock-free adaptive routing (Duato, IEEE TPDS
  1997, "A necessary and sufficient condition for deadlock-free adaptive
  routing in wormhole networks") remain the field's reference point for
  channel-dependence deadlock arguments. Modern practice keeps paying:
  preemptive-VC deadlock-free AXI NoCs (arXiv:2607.01430, Leone/Colagrande/
  Benini 2026) shows the deadlock-freedom bar is still where AXI-class
  designs compete.
- **Ours:** fairness exists small-scale (`formal/cell_core.fair.sby` — every
  op terminates and every op is answered), and the coherence arena ended at
  "eventual drain under stated contracts, not unbounded liveness, which
  nothing in this suite has ever claimed" (`coherence-arena/VERDICT.md`).
- **Gap:** we have no fabric-level liveness theorem — no bound from
  flit-injection to flit-delivery as a function of ring diameter d.
- **Path:** the VERDICT's surviving synthesis already names the ingredients:
  "staleness bounds from A's (d,k) lemma" + "eventual drain from K3
  arithmetic." Formalize the (d,k) ring lemma as an SBY liveness property
  (bounded-latency delivery under the E1–E4 assumption ledger) at NCELL=2,
  then lift via G1's composition. Duato's framework gives the vocabulary:
  our ring with a single flit class and no cycles in the channel-dependence
  graph is trivially deadlock-free *if* we state the grant/tick scheduler
  assumptions as channel properties — that's the honest version of the E4
  dependency the arena's Attack 6 exposed ("it's a scheduler property, not a
  protocol property" — arena-claude, VERDICT §1).

### G3. Feed the PDR invariant back as k-induction assumptions — difficulty: S
- **Field:** standard practice in the IC3/PDR school: use the
  machine-generated invariant as a lemma set for k-induction or as the
  candidate invariant for re-verification (Bradley & Manna,
  *Checking Deductive Proofs* / IC3 literature; cf. Een/Biere/McMillan PDR
  2011).
- **Ours:** the 854-clause invariant exists, is committed, ABC self-verified,
  and we named the obvious next experiment ourselves: "feeding the clauses
  back as assumptions = obvious next experiment" (commit 87f42bc).
- **Gap:** it's an open TODO in our own log.
- **Path:** exactly that experiment: `read_verilog -formal` harness with the
  PLA clauses as assumptions, `mode prove` k-induction. If it closes, we get a
  *re-checkable, engine-independent* inductive certificate instead of a
  PDR run log — and the human-readable clause families become the prose
  proof. Caveat already on file: "yosys silently re-declares hierarchical
  refs — lemma injection must be post-flatten" (commit cb14a9c).

### G4. Equivalence flow between fabric model and RTL beyond NCELL=2 — difficulty: M (partially PORT)
- **Field:** NoC-Out gets refinement for free from Rocq; the open-HDL world's
  standard is per-module `equiv_make`/`equiv_induct` (yosys), which our own
  `CUTTING-EDGE-rtl.md` already lists as "adopt later."
- **Ours:** fabric-level differential cosim is *bit-exact measurement*, not a
  proof — and honest about it: "tick TIMING is scheduler fact fed to the
  model via the measured event streams (that IS the serialization seam §10
  names)" (commit 3157b3d).
- **Gap:** no equivalence *proof* between the Python fabric model and the RTL
  at any NCELL; the serialization seam is measured, not discharged.
- **Path:** two-step: (1) reify the serialization seam as a deterministic
  spec (the "measured event streams" become an assumed schedule — the same
  move the VERDICT made with E4); (2) prove RTL ≡ model *given the schedule*
  per cell, then compose. **PORT-flavored:** MerkleMesh gives us
  "merkle aggregation + inclusion proofs over quilt cell-ledger journals"
  (SuperInstance/MerkleMesh) — a per-cell digest chain could make the cosim
  diff O(1) per window (compare roots, bisect on divergence) instead of
  flit-by-flit, which is what scaling NCELL=8 will need anyway.

### G5. Deadlock/routing-theory framing of the ring grant scheduler — difficulty: M
- **Field:** Duato 1997 (above); and the 2026 AXI work shows even
  "protocol-level dependencies between read and write traffic can create
  circular waits at the network endpoints, even when the routing algorithm
  itself is deadlock-free" (arXiv:2607.01430).
- **Ours:** the Q2 interlock MERGES tick pulses mid-service and grant-time
  sampling cannot see tick-vs-op order while an op is queued (commit 3157b3d
  — "found the hard way by the first rand disagreement").
- **Gap:** we've never drawn the channel-dependence graph of our own
  interlock+ring. The AXI lesson says endpoint/protocol dependencies (our
  fire/effect read-modify-write over link traffic) are where circular waits
  hide — precisely our unproven corner.
- **Path:** a paper exercise first (S→M): enumerate dependency classes
  (op-request, ACK, tick, fire-burst), show acyclicity under E-ledger
  assumptions or find the cycle. If a cycle exists at NCELL≥4 it is a *bug
  class the theory predicts*, found before the cosim does.

### G6. Fault tolerance / self-repair as a stated property — difficulty: L
- **Field:** **Self-Organising Digital Circuits** (arXiv:2608.02606, May
  2026): a topology-masked Transformer configures LUTs, "self-assembl[es]
  functional circuits from scratch and rapidly re-rout[es] logic around
  permanent, previously unseen hardware faults," >99.99% soft-error recovery
  (Barylli, Béna, Mordvintsev, Nisioti, Risi). Older but structural:
  FATAL+ self-stabilizing Byzantine clocking for SoCs (arXiv:1202.1925).
- **Ours:** nothing. Reset is a "contract-violation boundary" (our own
  formal docs); a wedged cell stays wedged; the coherence arena's
  wedge-freedom was *the* contested prize and both theorems died as stated.
- **Gap:** the field now demonstrates adaptation around damage; we don't
  even state a repair story. Dijkstra's self-stabilization (Dijkstra 1974,
  CACM 21(5); Schneider's 1993 survey) is the theory: local rules → global
  convergence — literally our doctrine, unclaimed.
- **Path:** smallest honest version: a **self-stabilizing conservation**
  experiment — after arbitrary state corruption (formal: BMC from
  free-at-t0, which our init-encoding OPEN from cb14a9c already touches),
  does the fabric re-reach a conserved manifold within k ticks? Our decay/
  leak semantics suggest partial yes; the answer either way is a paper.

### G7. Physical-NCA / embodied-cellular benchmark presence — difficulty: M
- **Field:** rotation-invariant embedded NCA platform with battery-powered,
  state-retaining cells, open hardware+sim (arXiv:2510.07440, ALIFE 2025,
  https://github.com/dwoiwode/embedded_nca); CA decoders for quantum codes
  at high performance (arXiv:2604.21866).
- **Ours:** iCE40/ECP5 synthesis results and a QUF boot story
  (`docs/SYNTHESIS-FPGA.md`, `docs/FPGA-BOOT.md`) — but no
  battery/physical-modularity story, no external benchmark participation.
- **Gap:** our hardware lane exists but doesn't speak to the ALIFE/physical-
  CA community's format; nobody there has heard of a quilt.
- **Path:** a CHIP-MATRIX row for the embedded-NCA platform's workload, or a
  QUF-boot on a modular battery cell (the "boat doctrine" already wants
  edge-native). This is visibility engineering as much as engineering.

### G8. Coherence with a proven cost model — difficulty: M (PORT assist)
- **Field:** **Token Coherence for multi-agent LLM systems**
  (arXiv:2603.15183): maps multi-agent synchronization onto MESI, TLA+-
  verified (single-writer safety, monotonic versioning, bounded staleness,
  ~2,400 states), with a proven savings lower bound
  (O(n·S·|D|) → O((n+W)·|D|)).
- **Ours:** the coherence arena produced a *synthesis* ("admission-gated
  fire-with-skip carrying wedge-freedom, SELVEDGE's learning algebra and
  (d,k) ring lemma carrying semantics and delivery bounds") with no cost
  theorem and both headline theorems dead (`coherence-arena/VERDICT.md`).
- **Gap:** the field proves coherence *savings*; we adjudicate coherence
  *wedges*. Also notable: their TLA+ verification is exactly the kind of
  protocol-level check our arena ran on prose.
- **Path:** fold the arena's surviving synthesis into a stated theorem with
  a cost model (staleness vs. token traffic on a ring is a (d,k)-lemma
  corollary). **PORT assist:** quilt-mhs (federation messaging) and
  quilt-fleet (quorum/migration) already implement the runtime side; the
  theorem would describe code we run.

### G9. Constraint-checking at scale for soak/fuzz — difficulty: S (pure PORT)
- **Field:** property fuzzing and statistical soak with automated
  scoreboards is standard (cocotb 2.x direction, our CUTTING-EDGE doc).
- **Ours:** directed + random programs, 30/30 bit-exact, but the checker is
  single-threaded Python replay.
- **Gap/Path:** **PORT** — cuda-constraint-engine ("GPU constraint checking
  at 1B+ constraints/sec, CUDA library with C and Python APIs",
  SuperInstance/cuda-constraint-engine) as a cosim oracle backend for
  NCELL=8/16 random soak at 100–1000× current volume. Cheapest difficulty
  class in this whole table: a wrapper, not a build.

### G10. Paper-grade write-up of the conservation+decay result — difficulty: M
- **Field:** NoC-Out shows what the bar is: claim + machine-checked proof +
  generated artifacts, all in one package.
- **Ours:** we have the claim, the PDR certificate, the named invariant
  families, and the honest residue list — scattered across a dossier the
  field will never read.
- **Path:** distill `FORMAL-PROOFS.md` + `PDR-IVARIANT.md` + the cosim
  ledger into an arXiv-shaped paper: "conserved cellular state on a ring,
  proven unbounded at small N, parameterized-composable at large N" (post-G1).
  The annals voice is charming; the field needs the plain one.

---

## 2. The three things we do that the field does NOT — honestly sorted

### N1. Genuinely novel: conserved cellular state as a *currency* inside a
learning fabric — the ledger (bind/link/effect/view/tick/fire) where credit
is conserved bit-exactly and the conservation itself is PDR-proven unbounded.
NoC-Out proves liveness of *transport*; nothing in the sweep proves a
conservation law over *payload semantics* (learning/decay state) as a fabric
invariant. Evidence: the field's guarantees are traffic-level (deadlock,
delivery, refinement — 2608.24478, 2607.01430); our `fabric.conservation`
PDR close (commit 4b67c30) with the 854-clause invariant's per-bit
conservation core (`docs/PDR-IVARIANT.md`) is a different kind of theorem.
**Caveat:** conservation invariants are classical (credit-based flow control
conserves credits — cf. Duato's credit discipline); the novelty is the
*object* conserved (Hebbian edge credit / probe energy), not conservation
per se. Honest grade: novel-in-object, re-derivation-in-method.

### N2. Genuinely novel: the measured-serialization differential cosim as an
epistemic instrument. We replay what the ring *actually did* (measured event
streams) rather than a chosen serialization, pinning two model-side
semantics the first disagreement exposed (link-ACK routing, dial-13 live
probe) — commit 3157b3d. The field's equivalent (NoC-Out) gets refinement by
construction in Rocq, but for *legacy/incremental* Verilog-2005 designs with
a semantic model, our "differential cosim against measured serialization"
has no direct counterpart in the sweep. Honest grade: a methodology, and the
field will say "that's just scoreboard-based cosim" — our twist is using the
measurement to *discover the spec*, then freezing it. Novel-ish, defensible.

### N3. Re-derivation (not novel, and we should say so): local rules with
global guarantees. Our decay/leak/fire dynamics are a cellular automaton
whose global property (conservation) is proven — that is Dijkstra 1974's
self-stabilization program and Angluin's population protocols (Angluin et
al., PODC 2004, "Computation in networks of passively mobile finite-state
sensors") re-instantiated in RTL. The annals' own doctrine ("local rules,
global guarantees") is the field's oldest idea. We do it *in Verilog-2005
with PDR* — the tooling is modern; the idea is not.

---

## 3. The single highest-leverage next move

**Close G3 this week, then G1 as the quarter's proof project.**

G3 (feed the 854-clause PDR invariant back as k-induction assumptions) is
hours of work, was named by our own commit log, and converts the PDR trophy
from "engine run log" to "re-checkable inductive certificate" — the artifact
that G1's parameterized proof will be *made of*. If the clause families are
as uniform as PDR-IVARIANT says (752/854 one family), the parameterized
induction in G1 becomes: prove the family template once, instantiate at
each ring position. That is our NoC-Out answer — same endgame
(generator-level correctness), reached through Verilog-2005 + ABC + SBY
instead of Rocq, which is the only honest lane our purity covenant allows.

## 4. Coverage limitations (recorded, not hidden)

- Gemini web-search quota exhausted (429) mid-survey; the external sweep is
  arXiv-API + prior repo knowledge. NOT covered this pass: ACM/IEEE
  paywalled 2025–2026 NoC literature (DATE/HPCA/NOCS proceedings), the
  Kôika/Rocq primary sources beyond the abstract, and GitHub code search for
  2026 NoC repos. A follow-up lane with quota should re-verify G1/G2 claims
  against the NoC-Out full text before we bet a quarter on them.
- Internal prior art read via `gh repo view` descriptions only (captain's
  read-only rule); PORT grades assume the descriptions are accurate.

## Citation index

- NoC-Out: arXiv:2608.24478 — https://arxiv.org/abs/2608.24478
- Preemptive VCs / deadlock-free AXI: arXiv:2607.01430 — Leone, Colagrande,
  Benini — https://arxiv.org/abs/2607.01430
- Self-Organising Digital Circuits: arXiv:2608.02606 — Barylli, Béna,
  Mordvintsev, Nisioti, Risi — https://arxiv.org/abs/2608.02606
- Embedded NCA platform: arXiv:2510.07440 (ALIFE 2025) —
  https://arxiv.org/abs/2510.07440 · https://github.com/dwoiwode/embedded_nca
- Token Coherence (multi-agent LLM): arXiv:2603.15183 —
  https://arxiv.org/abs/2603.15183
- FATAL+ self-stabilizing clocking: arXiv:1202.1925 —
  https://arxiv.org/abs/1202.1925
- CA decoders for quantum codes: arXiv:2604.21866 —
  https://arxiv.org/abs/2604.21866
- Duato, "A necessary and sufficient condition for deadlock-free adaptive
  routing in wormhole networks," IEEE TPDS, 1997.
- Dijkstra, "Self-stabilizing systems in spite of distributed control,"
  CACM 21(5), 1974. Schneider, "Self-stabilization," ACM CSUR 25(1), 1993.
- Angluin, Aspnes, Diamadi, Fischer, Peralta, "Computation in networks of
  passively mobile finite-state sensors," PODC 2004.
- Internal: SuperInstance/MerkleMesh, quilt-mhs, quilt-fleet,
  cuda-constraint-engine (via `gh repo view`, 2026-08-31).
- Repo evidence: commits 4b67c30, 87f42bc, cb14a9c, 3157b3d, 5d9d848,
  b0afb56; `docs/PDR-IVARIANT.md`, `docs/coherence-arena/VERDICT.md`,
  `docs/CUTTING-EDGE-rtl.md`, `docs/FORMAL-PROOFS.md`.
