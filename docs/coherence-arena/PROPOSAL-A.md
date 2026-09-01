# PROPOSAL A — SELVEDGE: Coherence by Algebra, Wedge by Unrepresentability

**Arena:** Cache Coherence Conception · **Rival:** A · **Date:** 2026-08-31
**Base:** master @ 3157b3d (conservation PDR-closed unbounded, abc pdr 25.9 s;
cell_core.fair depth-130 PASS, 2 h 29 m; fabric cosim bit-exact across two
seed generations, 18/18 + 30/30 programs)
**Deliverable status:** conception + proof obligations. No RTL was touched.
Every claim about existing behavior is cited to this tree; every claim about
SELVEDGE is marked *obligation*, *predicted*, or *honest cost*.

> **Selvedge** (n.): the self-finished edge of a woven fabric, finished so it
> will not unravel. Backronym, if the arena wants one: **S**emilattice **E**vent
> **L**ines, **V**alidated by **E**xternalized **D**ecay, **G**uarded by
> **E**mpty-slot conservation.

---

## 0. Summary — deliberately undersold

SELVEDGE is a coherence protocol with **no blocking coherence operation at
all**: no locks, no tokens-for-permission, no invalidations, no directory, no
request/response round-trips. Every shared line is a join-semilattice replica;
all coherence traffic is fire-and-forget, one-directional (clockwise), and
idempotent; admission is by per-line credit renewed at the global tick (a
self-renewing lease with **zero renewal traffic** — the tick *is* the renewal);
and a hole-conservation rule (one permanently empty ring slice, a circulating
bubble) makes the all-slices-saturated state — the exact state the fabric
wedges in — **unrepresentable rather than detectable**.

The RTL delta is small (one subtype bit, one engine command, one credit
register per line, one credit bit per node — §5). The semantic delta is total:
the fabric gains a class of shared state whose consistency mechanism cannot,
by construction, participate in any wait cycle, because its instruction set
contains no instruction that waits on a peer.

What is *not* claimed: linearizability (reads are eventually-consistent with a
priced staleness envelope), unbounded liveness (still not claimed anywhere in
this suite, and not here), and correctness under tick skew (the protocol's
algebra assumes the fabric's existing global tick — §9 names this as the
deepest fragility).

---

## 1. Motivation — cyc ≈ 34.5 k as a *representability* failure

The record (docs/SILICON-EXPERIMENTS.md §3, §3.1, rescue-lane table): on the
pre-fix RTL, the scale run froze at cyc ≈ 34.5 k; the hardened bench caught
`ENTRY-IDENTITY BREAK @cyc=34586`, `LEDGER FAIL @34816`, **occ = 42, all 16
ring slices presenting the same dst** — the F2 clone storm — and, structurally
worse, the F3 saturation anatomy: a cell in `ST_FIRE` holding `ci_ready=0`,
its own delivery parked at its own ringport head, injections gated behind it,
everything behind frozen. The minimal repro (`sim/vlt/tb_quiesce_repro.cpp`,
seed 0xC0FFEE) froze at occ = 14 **through 500 k cycles with the ledger
intact**. Two facts define the design space:

1. **Conservation survived; liveness did not.** The fabric's strongest
   machine-checked property (A1/T1, now PDR-unbounded) was orthogonal to the
   wedge. A coherence protocol that only *extends the ledger* is solving the
   wrong problem.
2. **The wedge was invisible from inside.** The bench found it; the fabric
   could not. The post-mortem leaned on state readouts that had to be added,
   not registers that existed — the incident's wedge state was perfectly
   representable, inhabited, and silent. ("Masked by a nonexistent register"
   is the honest one-line history: detection required instrumentation the
   fabric did not carry.)

The incident's two deadlocks, read as wait-for graphs, share one property:
every cycle closes through an edge where some component **waits on another
component's permission or capacity** — F3 through inject-behind-parked-hit;
the F2 storm through saturation itself (occupancy = capacity everywhere, the
condition "all slices full"). The F3 escape-lane fix
(`inject_ok = !ri_valid || hit`, rtl/q_link_ringport.v) was the first
*unrepresentability* fix in this repo's history: it deleted a wait edge, it
did not add a detector. SELVEDGE is that move carried to completion:

> **Design law (DL).** A state that must never happen shall be made
> unreachable by a machine-checkable invariant, not observable by a monitor.
> Monitors are for states that are allowed to happen.

Everything below is DL applied to coherence.

---

## 2. What wants coherence in this fabric

v1 state is single-owner by construction: an edge's ladder lives in the
destination cell (`OP_LINK` writes `etab`/engine at the linked cell; effects
train in place). Coherence becomes necessary the moment state is *replicated*,
and the repo's own trajectory lists exactly those moments:

- **Remote views** (`view(1)` wsum at a peer, host polling `act`): today these
  are synchronous request/response — response traffic is the traffic class
  whose cyclic interaction with fanout *is* the F3 anatomy.
- **v2 shared-math tail** (view(3) "cos", NAKed in v1): classical motivation
  for exclusion-based coherence — and rejected here (§10, §4.4).
- **Affinity sidecars / dither bandit** (SEMANTIC-TOWER, V2-NOTES): replicated
  estimator state per cell.
- **The hundred-boats doctrine** (TOOLS.md): many small edge agents sharing
  model state with no per-token cloud cost — eventual, commutative replication
  is exactly the offline-first shape.

A line, then, is any addressable replica-able value: an edge slot's ladder
state, a dial, an activation snapshot. SELVEDGE defines how replicas converge.

---

## 3. The protocol in one page

Four axioms. AX1–AX3 define coherence; AX4 is the structural wedge-killer.

- **AX1 (Semilattice lines).** Every cacheable line takes values in a
  join-semilattice (L, ⊔). The merge operator ⊔ is commutative, associative,
  idempotent; replica state is reached only by merges from the initial value.
  Implementation: additive state-CRDT — each replica keeps its *own*
  contribution counter; the line's read value is the semilattice sum
  (componentwise saturating add for additive quantities, §4).
- **AX2 (Fire-and-forget, one direction, no response).** A merge is a flit:
  `op = OP_EFF` subtype `a0[15]=1`, `src` = writer, `dst` = line home or
  replica, `dat` = contribution. It is injected once, transits clockwise,
  and is *consumed* at delivery (like effects/ACKs at cell destinations —
  consumed, not egressed). There is **no ack, no invalidation, no retry
  ordering, no retry storm**: a lost or dropped merge is re-issued at the next
  lease window with no semantic hazard, because ⊔ is idempotent and
  commutative (§6, INV5 corollary).
- **AX3 (Tick-leased admission).** Each (cell, line) pair carries a merge
  credit register `mcr[line] ∈ [0, R]`, R = 1 at conception. Credit is
  renewed to R **during tick service** (ST_TICK), exactly as the fire
  refractory `refr` is re-armed — and for the same reason: `refr` already
  *is* a lease; fire is already admission-controlled by self-renewing credit
  (`d_refr` dial). SELVEDGE generalizes the fabric's existing physics to all
  fabric-generated traffic. Injection decrements `mcr`; `mcr = 0` **skips**
  the emission (drop-and-retry next window) — it never stalls (EH4, §5).
  Renewal traffic: **zero** — the global tick (`q_tick_sched`, one strobe per
  2^TPW ≥ 256 cycles, E4 contract ≥ 128) renews every lease at the same
  logical instant. The lease renewer is a register that already exists in
  every cell (`tick_pend` machinery).
- **AX4 (Hole conservation — the bubble).** The ring maintains at least one
  empty slice forever: `holes(t) = NB − Σ_slices occ(t) ≥ 1`, where a slice's
  `occ` is its a_v+b_v occupancy. Mechanism sketch (per-node, no flit-format
  change): a 1-bit bubble credit, **minted by delivery** at the node where a
  flit leaves the ring, **spent by injection**; credit travels with the hole
  (holes drift counterclockwise as flits flow clockwise). Delivery mints a
  hole; injection consumes one; transit preserves them. This is the mirror
  image of the flit ledger — the fabric conserves flits (T1) and SELVEDGE
  conserves anti-flits (holes). Cost ceiling: ≤ 1/NB throughput, the price of
  making "all slices full" — the occ=42, all-16-slices-presenting state of
  the incident — **uninhabitable**.

Immediately observable consequences: coherence traffic cannot head-of-line
block responses (there are no coherence responses); a clone bug (F2 class)
applies a duplicate merge — idempotent ⊔ makes it semantically invisible even
though the extended ledger still flags it (defense in depth, §8, T-C);
saturation by merges is rate-bounded at NCELL·R flits per tick window by AX3,
independent of host behavior.

---

## 4. The state algebra

### 4.1 Why weights are already almost a semilattice

The two update families on an edge line are:

- **train** (cofire, graded class g): bucket-count increments. Componentwise
  addition of non-negative counts — commutative, associative. The additive
  state-CRDT encoding: replica i stores its own contribution vector; merged
  read = saturating componentwise sum. No log, no vector clock: the
  *contributions themselves* are the CRDT state (a G-counter per bucket per
  replica — for the 2-replica case of §8's proof harness, home + remote
  delta).
- **decay** (tick sweep, hb_cmd 010): NOT monotone in general — this is the
  one anti-commutative intruder, and the reason classical coherence would
  demand ordering. SELVEDGE's move: **decay is externalized from the state
  into the readout.** The line's value is `F(contributions, tick_count)` —
  exactly what the dyadic ladder already computes implicitly: the ladder is
  an *event fold* whose readout ages with the shared clock (buckets shift,
  implied weights 2^-i — the staircase theorem's whole subject,
  ABSTRACTION-MATH §5). Because **the tick is global and synchronous**
  (one `q_tick_sched` broadcast strobe; every cell decays at the same
  logical instant; tick service is atomic per cell; ops are bounded ≤ 66 «
  tick spacing ≥ 128, so no op straddles a tick boundary mid-service),
  decay is a *uniform function application at a common instant*, not an
  event. Functions applied uniformly to both sides of a semilattice
  equation preserve the equation up to quantization: drift is bounded by
  rounding, priced by the envelope (INV5), and collapses to zero at
  quiescence (no in-flight merges, same tick).

This is the load-bearing trick and it is native to the fabric: the Lustre
*basic clock* reading of the tick (ABSTRACTION-MATH §3.1) is precisely what
makes "decay commutes with merge" true **at tick granularity**. The echo gate
already decouples learning from activation the same way (gate CLOSED: skip
the train, still read + integrate). SELVEDGE is that decoupling promoted to
the coherence law.

### 4.2 What is excluded by law

Any line whose updates do not commute is **not fabric state**. Concretely:
the v2 shared-math tail (view(3) cos) may exist only as a commutative fold
over event/contribution state, computed redundantly at each site; a
mutually-exclusive shared resource (the classical directory/token use case)
is refused admission. This is not a limitation silently accepted — it is the
unrepresentability thesis applied to *semantics*: if it cannot be made
commutative, it does not go in the fabric. (The rejected alternatives and
what they would have bought are in §10; the bait for the rival on exactly
this point is Open Question 1.)

### 4.3 Algebra summary

Let `C_i ∈ ℕ^K` be replica i's contribution vector (K ladder buckets),
`S = Σ_i sat(C_i)` the semilattice sum (componentwise saturating add —
saturate-never-wrap, the fabric's arithmetic doctrine), and `T` the global
tick count. The line's value is `W(t) = F(S, T)` with F the age-weighted
readout. Then:

- **Merge = addition**: `C_i ⊔ C_j` = componentwise sum ⊆ S. Commutative,
  associative, idempotent *in effect* (duplicate delivery adds twice at the
  counter but saturating addition of the same contribution is a fixed point
  once folded; for strict idempotence the fold is per-(src,epoch) — see
  honest cost §9.3 on epoch width).
- **Convergence at quiescence**: if all emitted merges deliver (T-B), every
  replica computes the same S, hence the same W — convergence *by algebra*,
  not by ordering.
- **Bounded staleness in flight**: a replica lags by at most the
  undelivered contributions in flight for that line (≤ NCELL·R by AX3),
  each of which perturbs W by at most one bucket quantum with staircase
  overstatement ≤ 2× — INV5 prices it without any ordering assumption.

---

## 5. Encoding on the existing RTL (feasibility-consulted)

Plan A (opencode session, 2026-08-31): **zero flit-width change.**

- **Subtype bit**: merge = `OP_EFF` with `a0[15] = 1`. `ci_a0[15:4]` is
  declared reserved and no producer sets a0[15] today (fire fanout drives
  `lx_a0 = 0`; view uses `a0[1:0]`; bind/link use `a0[3:0]`). `a0[15]=0`
  remains bit-exact v1. OPW=4 (plan B) re-widths `q_flit_pipe.FW`, every
  golden trace, and the conservation/ledger harness word widths — suite-wide
  breakage; rejected.
- **Engine merge command**: `hb_cmd 3'b110` — a new case in `q_hebb_edge`
  (~20 gates, `o_done` in 1 cycle like cmds 001/100, not the K+1 readout),
  plus one `ST_LNKW`-shaped wait state in the core reusing the sel/done
  contract. A side unit would need a second write port into engine state —
  two owners, invariant break; rejected. Dialfile-direct merges alias with
  last-writer-wins `bind` (a bind clobbering a merge kills commutativity);
  only admissible on bind-retired dials.
- **Credit register**: `mcr[line]` per line (R=1 → 1 FF per line), renewed
  in ST_TICK service alongside `refr` — a parallel register write inside an
  existing tick state, 0 cycles added, no Q2-deadline interaction.
- **Merge-apply cone**: sat-add 16b ≈ 40 gates / 5–6 levels, registered
  behind `i_cmd` like train — nowhere near the 16×16 multiply / PIPE_EFF
  critical path.
- **Bubble credit**: 1 bit per node + mint/spend logic at the ringport
  boundary (~small; the per-slice form needs the credit to ride hole
  motion — §8, obligation OB-H1).

**Encoding hazards (named, from the consult — each is a named bug class the
existing proofs catch or the design must avoid):**

- **EH1**: every new core state returning to IDLE must replicate the Q2fix
  `ci_ready <= !(s_tick || tick_pend)` — or the formal-found one-cycle
  silent-drop hole returns (cell_core.tick / fabric.conservation catch it).
- **EH2**: `ST_UNB` NAKs any non-bind flit; a merge delivered to an unbound
  cell would emit a spurious NAK, contradicting fire-and-forget. Merges join
  the consumed-silently set (with OP_ACK/OP_NAK/OP_TICK).
- **EH3**: the dialfile is full (16/16; kle=11, floor=12, probe=13,
  qdw/rqen=14, qleak=15) — `mcr` has no free dial. Options: constant R,
  widen ND, or squat the v1-unused `cosmin` slot. Conception picks constant
  R=1 (dial-tunability of coherence admission is a foot-gun anyway; DL
  prefers structure over dials).
- **EH4**: any state *blocking* on `mcr==0` deadlocks against `tick_pend`
  (the core would never reach ST_IDLE, never renew). `mcr==0` must
  skip-and-drop, never stall. Likewise **no merge emission inside the tick
  sweep** — ST_FIRE-shaped emission under lx backpressure is unbounded and
  breaks Q2.

Gate/FF budget (predicted): ~60–100 gates per cell for the merge path +
credit registers + bubble bit; on the NCELL=15 scale fabric (~16–17 k FF),
an mcr-per-edge-slot layout adds EDGES_N FF per cell. Not free, not
structural.

---

## 6. Named invariants (the formal spine)

Vocabulary is the existing one: core state register `state`, `tick_pend`,
`ci_*` ingress bus, `lx_*`/`lo_*` egress, `hb_cmd/hb_sel/hb_done` engine
contract, `refr`, `etab/ev`, slice occupancy bits (`a_v`, `b_v` per
`q_flit_pipe`), inbuf/egbuf (each a `q_flit_pipe`), ringport
`hit/transit/inject_ok` wires, `s_tick`. New state: `mcr[line]`,
contribution state `C_i[line]` (inside the engine's merge port), bubble
credit `bc`.

- **INV1 (MERGE-COMM — semilattice laws).** For all contribution operands
  a, b, c and replica state s:
  `merge(a, merge(b, s)) = merge(b, merge(a, s))` (commutativity) and
  `merge(merge(a,b), c) = merge(a, merge(b,c))` as folded applications
  (associativity of the contribution add). Form: sby `mode equivalence`,
  two 2-instance miters of the merge-apply module. Predicted < 1 s each
  (claude consult). This is a *unit* fact — no environment, no FSM.
- **INV2 (CREDIT-BOUND).** `0 ≤ mcr[line] ≤ R`; `mcr' = R` only when the
  cell services a tick (ST_TICK entry); `mcr' = mcr − 1` only on an accepted
  merge injection; otherwise unchanged. 1-inductive by inspection (the C2/C4
  shape: a bound tied to its own decrement/increment sites) — same class as
  flit_pipe's proven-unbounded contract.
- **INV3 (LEDGER-EXT — conservation compatibility).** Extending the
  fabric.conservation accounts: with `emit_m` = merges handed by any cell to
  its ringport, `pipe_m` = merges resident in ring slices/inbufs, `del_m` =
  merges consumed at delivery: **T1m** `emit_m = pipe_m + del_m`; **A1m**
  merges enter the A1 ledger as in-transit postings — a commit-class event
  at delivery, exactly like effect booking. Per-line in-flight:
  `inflight(line) ≤ NCELL·R` (each cell holds ≤ R credits, spends ≤ R per
  window, AX3). *Not* k-inductive on counters alone (the suite's own
  history: k-induction failed on T1/A1 where PDR closed); the handwritten
  strengthening, from the claude consult:
  - **INV3a (state partition):** for every merge identity m, exactly one of
    {emitted∧¬inflight∧¬delivered, ¬emitted∧inflight∧¬delivered,
    ¬emitted∧¬inflight∧delivered} holds;
  - **INV3b (delivery monotonicity):** delivered(m) ⇒ delivered′(m).
  With INV3a/3b the ledger count becomes 1-inductive over the partition —
  the lemma class PDR auto-derived for conservation (the `pdr -i` dump
  comparison, FORMAL-PROOFS §PDR referee, is exactly this subsumption
  question).
- **INV4 (EXIT-BOUND — no fabric-facing waits).** Every state of the
  extended core FSM has a structural exit bound: the wait events of record
  are `hb_done ≤ 12` (E2), `df_rstb ≤ 4`, response/fanout emission granted
  by the egress buffer drain (bounded by AX4's hole + AX2's no-response
  rule), and **no state's exit condition references another cell's state**.
  Machine-checkable form: the I1a/I2 bounded-liveness asserts extended to
  the new state (`ci_ready` pulse gaps ≤ 64-class), plus the static fact
  (by construction, reviewable in one screen of RTL) that the FSM's wait
  predicate set is {hb_done, df_rstb, egbuf_ready}.
- **INV5 (STALENESS-ENV).** For any read of line ℓ at replica i at cycle t:
  `|F(S_i,t) − F(S_home,t)| ≤ Δ`, with `Δ = 2 · inflight(ℓ) · q_max` —
  in-flight contributions each shift the readout by at most one bucket
  quantum `q_max`, staircase overstatement ≤ 2× (ABSTRACTION-MATH §5.1,
  b=2 case). *Derived* theorem: unit-level proof of the quantum bound +
  INV3's in-flight bound; composition argued, not machine-checked (§9).
- **INV6 (HOLE-CONSERVATION — the bubble).** `holes(t) = NB − Σ occ(t) ≥ 1`
  at every cycle boundary; holes change only by: delivery (+1, mint),
  injection (−1, spend), transit (0). The local spending rule (which hole
  may be filled) is an *obligation* (OB-H1, §8): the rule must make INV6
  1-inductive — the mirror of C2 ("occupancy ≤ 2" tied to `s_ready`), i.e.
  the most proven invariant shape in this repo, applied to emptiness.
- **INV7 (WEDGE-FREE — theorem, §7 T-B).** Stated as the conjunction used
  in T-B: INV4 ∧ INV6 ∧ (admission bounds: AX3 for merges, `refr`+E4 for
  fire) ⇒ no reachable state is a fixpoint of the fabric transition
  relation with positive occupancy. Not a single assert — a compositional
  theorem whose premises are INV2/3/4/6 and whose machine-checked form is a
  bounded-liveness obligation (OB-W, §8).

---

## 7. Theorems

### T-A — Convergence at quiescence, bounded staleness in flight

*Statement.* (i) At any quiescent instant (no in-flight merges, K ticks of
quiet), all replicas of every line compute identical values: convergence by
algebra (INV1 + delivery determinism; no ordering assumption anywhere).
(ii) At any instant, any read is within Δ (INV5) of the home value.

*Proof shape.* (i) At quiescence each replica has folded the same multiset
of delivered contributions; ⊔ commutativity (INV1) fixes the result
independent of arrival order; decay is a uniform function at a common tick
instant (§4.1) hence preserves equality up to quantization, and quantization
vanishes when no fold is mid-application. (ii) Immediate from INV3's
in-flight bound and the per-merge quantum. Machine support: INV1 miters,
INV3 PDR; the composition (i) is prose-over-machines — honestly labeled.

### T-B — Wedge-freedom: the ring handled explicitly, with the incident as the non-example

The naive claim — "all wait edges point clockwise, a cycle is impossible" —
is **false**, and the kimi consult killed it precisely: the ring-resident
edges (slice waits on downstream slice; transit waits on destination
ingress; injection waits on a ring gap) do all point clockwise, **but each
cell contains two directionless intra-cell edges** — slice → inbuf → core
(flit waits on core acceptance) and core → egbuf → ringport (ST_FIRE waits
on egress drain) — and a cycle is: clockwise ring edges **plus one
intra-cell detour per cell**. That detour is exactly the edge the F3 escape
lane cut (inject-behind-own-parked-hit); the live remainder is
ST_FIRE → egbuf → inject → ring gap, where the gap depends on downstream
cells that may themselves be in ST_FIRE.

SELVEDGE closes this with **two independent struts** (over-determined on
purpose; either suffices):

**Strut 1 — structural (INV6, the bubble).** With holes ≥ 1 an invariant,
the state "every slice full" is unreachable; the F2-storm terminal condition
(all 16 slices presenting) is uninhabitable; and the classic ring saturation
cycle requires every slice full to close. The wedge states of the incident
become counterexamples-to-invariants, i.e. proof failures, not runtime
events. This strut does not depend on tick spacing at all.

**Strut 2 — stability (admission vs. drain).** Without the bubble, the
argument is a queueing bound, stated honestly as such (kimi's correction):
wedge-freedom holds while `max concurrent ST_FIRE cells × fanout burst +
NCELL·R merges per window < ring drain capacity per d_refr window`. Its
premises: bounded fire service (I1-class, machine-checkable), fire
admission by `refr` (RTL fact), merge admission by `mcr` (AX3, INV2), and
**tick spacing E4 ≥ 128 — a scheduler contract, not an RTL fact**. This is
the fairness gap the claude consult names: cycle-freedom is sound, but
drainage additionally needs the tick to fire infinitely often (scheduler
assumption) and fire emission never to stall unboundedly (guaranteed by
Strut 1 + INV4 together). The doc therefore claims: **INV6 ∧ INV4 ⇒ no
static wedges; Strut 2 alone ⇒ no wedges under the E4 contract** — and
flags the scheduler-dependence as Open Question 3's bait.

**The compositional delivery lemma (kimi's two-tier form, adopted as the
canonical statement).**

- *Local contract L(cell)* — proven once per cell, never referencing ring
  state: a head flit destined to me is accepted within B_acc regardless of
  my internal state; my slice advances within B_hop; neither bound waits on
  the ring. (B_acc is exactly INV4's exit-bound + inbuf drain; the bubble
  makes B_acc unconditionally satisfiable since the head's slice can always
  advance.)
- *Ring lemma* — parameterized by (NB, B_acc, B_hop), never looking inside
  a cell: for any flit f, take the lexicographic measure
  `(d, k) = (clockwise distance to destination, # flits ahead of f)`. Every
  interval of B_hop either decrements d (f advances) or decrements k (a
  flit ahead delivers, via L). A bounded measure over a finite ring gives
  per-flit delivery within `≈ NB · (B_hop + B_acc)`. The io node enters as
  the **proven sink**: it must satisfy L or be shown an infinite sink —
  under host contract (i_rdy granted within H cycles, an E1-class
  assumption, ledger entry E5) it satisfies L; tied-off, it is the base
  case that makes the induction start.

**Corollary (delivery, not just progress).** With an emission-tick age
stamp and oldest-first arbitration at the ringport (a v2 option, priced in
§9), the (d,k) lemma upgrades to a per-flit latency bound — subsuming the
wedge argument entirely (kimi: "worth claiming, it subsumes").

### T-C — Conservation compatibility (and why F2-class clones get defanged)

Merges are ledger events of the same class as effects: emitted (A1m
posting), in flight (pipe occupancy), delivered+applied (commit-class).
The extended ledger T1m/A1m preserves the PDR-closed shape (§8 predicts
closability; the proof plan reuses the exact harness pattern). Two
structural bonuses:

1. **Duplicate delivery is semantically idempotent under ⊔** — an F2-class
   clone applies a merge twice and the *line value* is unchanged (strict
   per-identity idempotence needs an epoch field — §9.3). The ledger still
   counts the clone (defense in depth: the bug remains machine-visible
   even though the data survives it).
2. **The DROP path**: a merge dropped at `mcr==0` is re-issued next window
   with no ordering hazard — retry-for-free is a CRDT property, not a
   mechanism. Contrast: effect drops (unknown src) are permanent and
   excluded by linked-peer contracts (DROP invariant, FORMAL-PROOFS §2).

### T-D — What the io node owes (the base case, made explicit)

The ring lemma needs the io node to be either a proven infinite sink or an
L-contract holder. v1's io egress drains to `i_rdy` (host readiness) — the
one place the fabric's liveness is *contracted outward*. SELVEDGE names
this **E5** and adds it to the assumption ledger (§9.5), rather than
letting it hide inside "ring progress" prose.

---

## 8. Proof strategy — mapped to the existing toolchain

Ordered by the claude consult's priority (confidence first, PDR budget
last). Every row names the honest failure mode.

| # | Obligation | Engine / mode | Predicted | Fallback if it fails |
|---|---|---|---|---|
| OB-1 | INV1 commutativity + associativity miters (2 instances of merge-apply module) | sby `mode equivalence`, boolector | < 1 s each (pure function, no state) | none needed; failure = algebra wrong = protocol dead |
| OB-2 | INV2 credit bound | k-induction (C2/C4 shape) | < 1 s | strengthen with tick-presence assumption guard (E4-free local form) |
| OB-3 | INV4 exit-bounds extended to ST_MRG states | extend cell_core.fair/tick BMC-80 asserts | minutes-class (like existing 8–15 min runs) | deeper BMC + structural prose (the wait-predicate set is one screen of RTL) |
| OB-4 | INV3a/3b partition + monotonicity (handwritten strengthening) | k-induction on the whitebox lemma set | the first handwritten proof attempt (claude: "write this FIRST") | let PDR derive it (OB-5) and keep 3a/3b as human-readable documentation — the exact posture the conservation PDR referee established |
| OB-5 | INV3 ledger-ext (T1m/A1m) on 2-cell harness | `mode prove`, `abc pdr` | closable — same counter+local-FSM shape as the 25.9 s conservation close; frame ≤ ~15 predicted | BMC + prose worst-case (the suite's pre-PDR posture); whitebox L1/L3-class visibility (peek-wire script pattern, fabric.conservation.prove-l12) |
| OB-6 | INV6 hole-conservation | k-induction on occupancy mirror (C2-shape) | seconds-class **once the local spending rule is fixed**; the rule itself is the research (OB-H1) | drop Strut 1, lean on Strut 2 with E4 explicit (the theorem survives, weaker) |
| OB-7 | OB-W: bounded-liveness witness of T-B — "if occupancy > 0, a delivery occurs within B = NB·(B_hop+B_acc)" | BMC-80 fabric-level, then PDR attempt | BMC-class pass expected at small NB (the quiesce-repro shape, now guaranteed to drain); PDR at full fabric: unknown, plausibly outcome (b) like fair.pdr | BMC + the compositional lemma as prose (the suite's standard honesty tier) |
| OB-8 | INV5 staleness envelope at unit level | BMC on merge+readout module, envelope monitor (the echo_gate.dyadic pattern) | seconds-class | keep INV5 derived-only, label composition unproven |

The suite-level asymmetry is inherited and respected: **PDR closes what
k-induction cannot** on counter-heavy properties (conservation history:
identical asserts, k-induction unclosed at 25 min, abc pdr 25.9 s). OB-5 is
deliberately shaped to reuse that engine's demonstrated appetite. OB-6/7 are
the new ground; both are stated so that *failure degrades the claim
honestly* rather than vacating it (Strut 1 fails ⇒ Strut 2 stands with E4
named; OB-W fails at PDR ⇒ BMC-witnessed compositional prose, the tier the
repo already ships for fair/tick).

Cosim obligation (not formal, but the repo's own bar): the fabric-level
Python model gains merge ops and the mcr/bubble mechanics; bit-exactness
target = merged reads agree across replicas at quiescence windows, and the
measured staleness histogram stays inside Δ (a *quantitative* cosim check —
new kind, worth doing).

---

## 9. Honest costs — what breaks, what slows, what stays unverifiable

1. **Consistency model drops to eventual-with-envelope.** No linearizable
   read exists in the protocol — by design. Anything admission-critical that
   truly needs exclusion is refused (§4.2). If the rival's protocol offers
   sequential consistency at some price, this is the axis they win on; the
   defense is that the fabric's *own* state (weights, activations, dials)
   is envelope-tolerant by doctrine (error-envelopes.md; the 2W bound is
   the house style).
2. **Throughput**: AX3 caps merge injection at NCELL·R per tick window
   (≥256 cycles at shipped TPW) — coherence bandwidth is *learning-rate*
   scale, not memory-bus scale. AX4 costs ≤ 1/NB ring throughput. Fanout
   latency unaffected (merges are a new class, not a tax on effects).
3. **Area/state**: per-line contribution state is replicated (memory × R
   replicas). The additive encoding avoids event logs, but strict
   per-identity idempotence wants an epoch field on merges (a0[14:12],
   reserved bits exist) — without it, duplicate folds add twice and INV5's
   Δ absorbs them only while the ledger catches the clone. ABA on epochs
   (width-bounded) is a named residual risk; 3 bits at 1 merge/window/line
   wraps every 8 windows — acceptable only because Δ bounds the damage.
4. **The four encoding hazards (EH1–EH4)** are each a *named bug the
   existing proofs will catch* — the design's respect for the suite, and a
   real re-verification cost: cell_core.fair/tick harnesses grow (those
   runs are already 8–15 min), and every golden trace family needs the
   a0[15] subtype case.
5. **Assumption ledger grows by E5** (io-node sink contract) — one more
   environment entry, same class as E1–E4, but it must be stated, not
   smuggled: fabric liveness was always *contracted outward* at the io
   port; SELVEDGE just writes it down.
6. **The deepest unverifiable (and the true soft spot): tick synchrony.**
   The algebra of §4.1 — decay commutes with merge *because the tick is a
   global basic clock* — is exactly the Lustre clock-calculus reading, and
   exactly what a GALS/polychronous v2 seam (SYNTHESIS Q2 v2, the
   metronome-cell forms) would break. If ticks skew across cells, decay is
   no longer a uniform instant, the semilattice argument needs
   re-derivation in a skew-tolerant algebra, and the lease renewal stops
   being simultaneous. Nothing in the current toolchain models tick skew.
   This is Open Question 1's territory.
7. **Starvation ≠ deadlock**: transit-priority ringports can starve
   injection under a sustained transit stream (kimi's early note); SELVEDGE
   proves no wedges, not no starvation. The age-stamp/oldest-first option
   (T-D corollary) converts it to a latency bound at arbiter cost — priced,
   not included by default.
8. **Unbounded liveness remains unclaimed**, same as the whole suite.
   OB-W's PDR attempt may be outcome (b) (fair.pdr's fate at depth ~131):
   the compositional lemma is the honest ceiling of this conception.

---

## 10. Rejected directions (and why they lose *on this fabric*)

- **Token-based uniqueness (single circulating token, no directory).** The
  classical virtue (no directory, bounded search) is real, but a permission
  token is a *wait*: a cell wanting the token waits for the ring to deliver
  it, and the wait edge is exactly an intra-cell detour edge of the class
  that closed the 34.5 k cycle. Token-passing on a saturated ring is
  scheduling reborn — the token itself needs a hole to travel in. (Priced
  honestly: a *bubble* is a token that carries no permission, only
  capacity — AX4 keeps the token's mathematics and refuses its semantics.)
  Double-grant races (two sources taking the token) need identity/epoch
  arbitration — new state, new races.
- **Directories / invalidation.** Invalidation traffic is response traffic;
  response-class traffic interacting with fanout is the F3 anatomy. A
  directory on a ring is a serialization point with O(1) writers and O(N)
  invalidation fanout — on a fabric whose whole doctrine is one-interpreter
  run-to-completion cells, it reintroduces exactly the multi-wait the
  escape lane deleted.
- **Lease-based quorum coherence.** Leases are sound (Gray–Cheriton), and
  AX3 *is* a lease — but quorum renewal on a ring costs O(N)-hop rounds and
  renewal traffic, which is wait traffic. SELVEDGE's lease renewer is the
  tick broadcast: renewal traffic zero, quorum none (the semilattice needs
  no majority — convergence is algebraic, not votative).
- **CRDT *without* the bubble (the naive version of this proposal).**
  Rejected by the consults: commutativity alone kills protocol deadlock
  but not *capacity* deadlock; saturation wedge is a capacity phenomenon;
  Strut 1 (AX4) is what converts the timing argument into structure.
  Kept as Strut 2 fallback only.
- **Holographic/replicated-invariant state (conservation-coupled
  reconstruction).** The most romantic candidate: every cell carries shards
  of a global invariant and updates are legal iff the global charge is
  conserved. It is beautiful and it is T1/A1's own mathematics — which is
  exactly why it is *already in the fabric* as the ledger, and why it does
  not need a protocol: conservation is the monitor, not the mechanism.
  Reconstruction (quorum read of shards) has no ring locality; and the
  34.5 k incident is the proof: the ledger was intact *through* every
  wedge. A coherence protocol must buy liveness, not re-buy safety.

---

## 11. Prior art lineage (honest debts)

- **CRDTs** — Shapiro, Preguiça, Baquero, Zawirski (2011); state/op CRDTs;
  delta-CRDTs (Almeida et al. 2016) for the additive-contribution encoding.
  SELVEDGE is a state-CRDT with a *hardware-global clock substituting for
  version vectors* — the tick is the version, which is why no per-replica
  metadata is needed.
- **Lease coherence** — Gray & Cheriton (1989): leases with time-based
  expiry; AX3's renewal-by-broadcast-tick is the degenerate-zero-traffic
  case.
- **Token-ring coherence** — IEEE Futurebus+, SCI (IEEE 1596): the
  rejected §10 alternative; the bubble's kinship (capacity-token) is to
  *flow control*, not permission.
- **Bubble flow control** — IBM Cell BE ring interconnect; Puente et al.
  (bubble/adaptive routing, 2000s). AX4 is bubble flow control recognized
  as a coherence-adjacent conservation law.
- **Deflection routing** — recirculate-on-contention (§3 of the kimi
  consult, offered as the B_acc-relaxing v2 path).
- **Synchronous-language clock calculus** — Halbwachs (Lustre), Le Guernic
  (Signal); the tick-as-basic-clock reading that makes externalized decay
  commute (ABSTRACTION-MATH §3, already the repo's own charter).
- **Kahn determinacy / bounded Kahn networks** — the fire-and-forget
  one-direction class is the determinacy-preserving subclass (monotone
  stream functions, no request/response cycle).
- **Dijkstra resource ordering / Chandy–Misra–Haas** — the wait-for-graph
  tradition; SELVEDGE's difference from all of it: prevention by
  uninhabitability (DL) rather than detection (CMH) or ordering
  (Dijkstra).
- **The fabric's own canon** — quilt-calculus T1/T2 (cut conservation,
  quiescence identity): A1m is T1 extended; holes ≥ 1 is T1's mirror;
  convergence-at-quiescence (T-A) is T2's shape applied to *information*
  instead of credit.

---

## 12. Open Questions — deliberately provocative

1. **Does the algebra survive its own clock?** Every merging premise of
   §4.1 lives on tick synchrony; the v2 GALS/metronome seam is the repo's
   own declared direction. Is a *skew-tolerant* SELVEDGE derivable (decay
   as a monotone operator in a skew-bounded semilattice — plausibly a
   bounded-drift envelope à la affine arithmetic), or does the whole
   conception quietly assume the one thing v2 plans to delete? If the
   rival's protocol is clock-agnostic, this axis is theirs.
2. **Is idempotence a load-bearing lie?** Strict per-identity idempotence
   needs epochs (§9.3); without them, a duplicate merge double-adds and
   INV5's Δ silently absorbs what the ledger counts — the envelope and the
   ledger then *disagree about whether a bug happened* (F2 reincarnated as
   a semantics-vs-accounting schism). Which should the fabric believe:
   the algebra or the ledger? (The F2 history says the ledger; §4 says
   the algebra; both is only honest if the epoch field ships.)
3. **Is Strut 2 (E4-dependence) wedge-*freedom* or wedge-*latency*?** The
   stability bound keeps the wedge unreachable only while the scheduler
   honors tick spacing — an environment contract, the same class of
   premise that let the ×1000-tick probe fiction live for a day
   (INCIDENTS: "a probe read without stated units is a
   self-attestation"). A protocol whose unwedging depends on a promise is
   detectable-with-extra-steps unless the bubble (Strut 1) carries the
   whole theorem alone — and the bubble costs throughput and its local
   spending rule (OB-H1) is unproven. Attack there: find the spending
   rule that makes INV6 1-inductive, or show none exists without a second
   circulating hole (2-bubble SELVEDGE, 2/NB cost — still cheap? where
   does the floor sit?).

---

## 13. Specialist consult log (2026-08-31, arena sessions)

- **arena-kimi (K3, spatial/topology):** killed the naive clockwise-only
  claim — named the two intra-cell directionless edges that close cycles;
  reclassified strut-2 as a stability/queueing bound with an explicit
  inequality; demanded the io node be a proven sink/base case; supplied
  the two-tier compositional form (local contract L + ring lemma with
  lexicographic (d,k) measure) and the compositionality rule (ring proof
  never looks inside a cell); proposed the bubble rule (AX4) — "the single
  change that converts your proof from timing to structural" — and
  recirculation; noted transit-priority starvation and the age-stamp
  latency upgrade.
- **arena-claude (Haiku 4.5, formal methods):** per-invariant closure
  predictions (miters < 1 s; credit 1-inductive; ledger needs PDR not
  k-induction — "the same state-refinement invisibility"); named the
  fairness gap in the wedge argument (scheduler-liveness + backpressure
  stall must be structural or explicit); wrote the INV3a/3b strengthening
  (per-merge partition + delivery monotonicity → 1-inductive ledger) as
  the first handwritten attempt; ruled equivalence-mode two-miter plan for
  INV1 (commutativity *and* associativity; free-ordering assert harnesses
  over-constrain); set proof priority INV1→INV4→INV2→INV3(PDR)→INV5.
- **arena-opencode (GLM-5.3, RTL feasibility):** plan-A subtype encoding
  (a0[15], bit-exact v1 preserved; OPW=4 rejected — FW/ledger/golden-trace
  suite breakage); hb_cmd 3'b110 placement (~20 gates, 1-cycle done,
  ST_LNKW-shaped state, side-unit rejected for two-owner invariant break);
  merge-apply cone pricing (~40 gates, off critical path); the mcr==0
  must-skip-never-stall rule (deadlock against tick_pend otherwise) and
  the no-emission-inside-tick-sweep Q2 rule; the four encoding hazards
  EH1–EH4 (Q2fix replication, ST_UNB NAK, dialfile-full → constant R,
  drop-window bounding).

*Rival B is invited to attack §7's struts, §9.3's epoch hole, §12's
questions, and above all OB-H1 — the bubble's local spending rule, which is
the one place this conception is genuinely unfinished on purpose.*

— RIVAL A, 2026-08-31, ~16:40 AKDT
