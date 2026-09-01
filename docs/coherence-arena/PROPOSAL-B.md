# PROPOSAL-B — TOKEN-NEEDLE: admission coherence, the ledger made physical

**Arena:** Cache Coherence Conception, quilt-verilog @ master 3157b3d (+5c4a19c docs)
**Rival:** B · **Date:** 2026-08-31 · **Toolchain target:** sby / abc pdr / smtbmc boolector (stock oss-cad-suite)
**Cross-consulted:** arena-kimi (ring topology), arena-claude (formal methods), arena-opencode (RTL feasibility) — contributions credited inline and in §9.

> **Summary (deliberately undersold).** A per-destination admission-token protocol
> with a single circulating bookkeeping flit — the *needle* — that returns tokens,
> numbers epochs, and carries the occupancy census. One new conservation law
> layered over the existing ledger; wedge states become counter-violations; the
> 34,560-cycle incident becomes a state the RTL cannot express. The body
> overdelivers: a wedge-vacuity theorem with a rank function, eight proof
> obligations mapped onto the exact PDR/k-induction idioms this repo already
> runs, and an honest cost ledger including the two bounds this protocol makes
> worse.

---

## 0. The one-paragraph pitch

The fabric already proves, unbounded (PDR, 25.9 s), that flits are conserved
(`fabric.conservation` A1/T1). Liveness is *not* proven anywhere — and the
34.5k wedge lived exactly in that gap: **the ledger counted the corpses but
nothing in silicon counted the waiting**. The wedge was invisible because the
state that would have revealed it — total ring residency, per-destination
backlog, token location — existed only as bench-side ghosts (the Python
ledger, the ENTRY-IDENTITY trap), never as fabric state. TOKEN-NEEDLE's move
is: **stop treating conservation as a checker and make it the protocol.**
Every flit must own an admission token for its destination before it touches
the ring; tokens are conserved quantities; one circulating needle flit is the
physical register the incident lacked — returning tokens, stamping epochs,
and auditing occupancy every revolution. The result is a fabric in which the
wait-for graph has no cycles *because admission pre-reserves landing space*,
not because anyone promises to be fast.

---

## 1. Motivation — the 34,560-cycle ghost register

The incident (docs/SILICON-EXPERIMENTS §3/§3.1, rescue-lane decomposition):

- master×master froze at cyc≈34.5k; master×rescue caught ENTRY-IDENTITY BREAK
  @34586 and the full ring presenting `dst=a` — F2's clone at birth.
- After F2's fix, F3 remained: a *saturation self-deadlock inside one cell* —
  cell in `ST_FIRE` holds `ci_ready=0` → inbuf (2-deep `q_flit_pipe`) fills →
  a hit parks at the cell's own ringport (`ld_ready=0`) → the old
  `inject_ok = !ri_valid || consumed` held the cell's fire flits out of the
  ring → everything behind the parked hit froze. Measured: occ=14 frozen
  through 500k cycles, **ledger intact**. Conservation survived; liveness died.
- The escape lane (`inject_ok = !ri_valid || hit`) severed the single-cell
  cycle. But SILICON-EXPERIMENTS §3.2 says plainly, under "Not claimed": no
  formal ringport liveness proof exists; end-to-end drain under a hostile
  host is unproven. The multi-cell cyclic wait — every cell in `ST_FIRE`
  with a full egbuf, full inbuf, and a ring so full no `ro_ready` ever
  appears — is **still representable state in the current RTL.**

The design driver's sharpest form: the wedge was *masked by a nonexistent
register*. The bench ledger was Python; the occupancy the fabric itself could
see was zero. A protocol that only *detects* wedges re-runs the incident with
better instruments. TOKEN-NEEDLE's contract is stronger: **the wedge
configuration violates a token-count invariant at the moment of its birth** —
it is unrepresentable, not merely observable.

Why per-destination admission is the load-bearing choice (and not, say,
bubble flow control alone — kimi proposed exactly that to this arena, and it
is good but insufficient): a bubble invariant (`Σ occ < RCAP`) kills ring
*saturation*, but the F3-family wedge does not need a full ring. It needs one
parked hit per blocked cell, and a parked hit requires only "inbuf full when
the hit arrives." Bubbles do not touch inbufs. Per-destination tokens bound
`ring-toward(d) + inbuf-toward(d) ≤ K_d = 2` — a *landing guarantee*, which is
the only fact that makes parked hits unrepresentable. The bubble then falls
out by arithmetic (§4, K3). Admission first; bubbles as a corollary.

---

## 2. Doctrine: coherence relocated — the three-plane split

The arena asks for a cache coherence protocol. The honest analysis of where
coherence actually lives in the quilt is the proposal's first claim:

**The quilt's mutable state is already single-owner.** Weights live in the
dst-cell's engine (`q_hebb_edge`), dials in the dst-cell's `q_dialfile`,
`act`/`etab`/`bound` in the cell core. There are no multi-writer lines to
keep coherent. What is *replicated and racing* is not data — it is **traffic
and time**: in-flight flits are cached requests whose home is their `dst`;
the ring is the interconnect; the wedge is the classic protocol deadlock
(request and response classes in a channel-dependency cycle), and stale reads
(view responses overtaken by mutations) are the classic coherence hazard.

So TOKEN-NEEDLE places coherence where the failure modes actually are, in
three planes:

1. **Transport plane — token coherence (Martin et al. 2003, relocated).**
   Admission tokens per destination; the token multiset is the protocol
   state; safety by token counting = conservation; the wedge theorem by
   landing guarantees. The "cache line" is a landing slot at `dst`.
2. **Learning plane — commutative by construction (CRDT-adjacent, but
   claimed weaker and therefore honestly).** Cofire trains are bucket
   increments; the readout is order-insensitive up to the *already-proven*
   dyadic envelope (echo_gate.dyadic, 2W ladder bound): the fabric's effect
   traffic needs **no** ordering, **no** acks for correctness, and tolerates
   the escape lane's overtaking *by algebra*. TOKEN-NEEDLE does not claim a
   semilattice merge operation on whole cells (that is Rival A's direction);
   it claims only: the effect workload is a commutative monoid action on
   engine state, which is precisely what makes token-gated reordering of
   fire fanout free (§5, M2).
3. **Control plane — epoch leases.** Views are linearizable snapshots at
   epoch granularity: every state-mutating core transition bumps a per-cell
   epoch `ε_c`; every view/bind/link response carries `ε_c` in the currently
   unused `a0` field; staleness is *detected*, not prevented (bounded-stale
   contract, §5 E-plane). The needle broadcasts fabric generation numbers so
   hosts can distinguish "same epoch" from "epoch wrapped."

The radical claim, stated so it can be attacked: **coherence protocols for
data are unnecessary in this fabric (single-owner + commutative); the
coherence protocol it actually needs — and lacked — is for admission.**
Everything else in this document is that sentence made formal.

---

## 3. The protocol

### 3.1 State (new vocabulary, in the existing naming style)

Per cell `c` (inside `q_cell`, ~23 FF — opencode's estimate, §9):

- `tk[EDGES_N]` — per-edge admission-token bits. `tk[e]=1` means the cell may
  inject one flit toward peer `etab[e]`. Fire fanout consumes `tk[e]`; a
  bind/link response or a needle grant restores it.
- `ow[NB]` — owed-token bits ("I accepted a flit from source s; a token of
  class `cell_id` is owed to s"). Set on `ci` handshake, drained by the needle.
- `eps[3:0]` — local epoch counter; bumps on dial write, link install,
  effect integration, act update, fire. (Width hazard: ABA at wrap — §7.)
- `gen[7:0]` — fabric generation, copied from the passing needle; a view's
  freshness certificate is the pair `(gen, eps)`.

At the io node (`q_io_port`, ~45 FF):

- The needle register: `ndl_v`, `ndl_mask[15:0]` (grant bits, one per dst
  id), `ndl_gen[7:0]`, `ndl_census[7:0]` (signed occupancy delta collected
  this revolution, for audit vs. the bench ledger).

On the wire: the needle is a flit of the existing ACK class —
`op=OP_ACK, src=EXTID, dst=EXTID, a2=NDL_MARKER` — chosen precisely because
opencode flagged that reusing `OP_TICK` on the ring collides with the core's
tick-flit ingestion path and the ring's op-set invariants. `dst=EXTID` means
no cell's hit-compare can ever deliver it; the io ringport absorbs needles
structurally (into the needle register, never into an inbuf) — guaranteed
absorption, the property that breaks every dependency cycle through it.

### 3.2 Rules (the entire protocol; R1–R4 are one line of RTL each)

- **R1 (admission).** A cell may inject a flit toward `d` only while holding
  a `d`-token: `li_ready = inject_ok && ro_ready && has_token(dst)`. The
  token is consumed atomically at the inject handshake. The io node holds a
  window register of `W_io` tokens per destination (the host window the
  bench already observed as ≤12 outstanding views — now a fabric-visible
  contract instead of a host courtesy).
- **R2 (token return, local half).** When a core accepts a flit from source
  `s` (`ci` handshake), the dst sets `ow[s]` — a token of its own class is
  owed to `s`. Sticky-deferral rule (kimi finding 2): if the needle's own
  mask bit is already set when a second accept occurs, `ow[s]` *stays set*
  — the surplus return defers to the next revolution. No token is ever
  dropped; worst-case return latency is two revolutions. View/bind/link
  acknowledgements piggyback one token return in `a0`'s low bit when owed
  (no extra flit); effect accepts owe silently until the needle collects
  them.
- **R3 (token return, fabric half — the needle).** One needle circulates.
  As it passes cell `c`: (i) `c` ORs `ow` into the needle's mask as bit `c`
  (each node writes only its own bit — no read-modify-write races); (ii) `c`
  reads the passing mask: if bit `d` is set and `c` has a pending admission
  toward `d`, `c` takes it — clearing bit `d` **combinationally in the
  ringport transit path, atomic with the needle's motion as a single flit**
  (kimi finding 3 / opencode's ri→ro-handoff rule: the clear is a function
  of the ringport comb mux for needle-class flits, exactly as `hit` is;
  first ring-order taker wins, exclusivity by needle position — N1); (iii)
  `c` refreshes `gen` from the needle. At the io the needle is absorbed and
  re-armed **unconditionally** (the needle register never waits on anything
  — kimi finding 6); re-injection happens only on needle return, so exactly
  one needle exists from reset; a missing-needle watchdog re-arms after
  `2·R_rev` with `gen+1` and a census-mismatch audit. `ndl_census` is
  compared against the io's own ledger counters — the audit that would have
  caught F2 in silicon.
- **R4 (needle priority).** The needle never queues behind new injections:
  injection is suppressed one cycle ahead of the needle (the io's own
  injection slot is reserved for it), and needle transit follows the
  ordinary transit path — it outruns nothing, it merely can never be
  *starved by admission*, since admissions are token-capped (K1) strictly
  below ring capacity (K3). Needle latency bound = E5 (§6).
- **R5 (epoch discipline).** `eps` bumps exactly on state-mutating core
  transitions (M1); responses carry `(gen, eps)` in `a0`/`a1` spare bits.
  No cache is invalidated — a stale view is *detectable* by comparing
  epochs; the contract is bounded staleness, not sequential consistency of
  replicas (single-owner data needs nothing stronger).

### 3.3 What a flit's life looks like

A fire at cell 3 with four peers — **fire-with-skip, never hold-and-wait**
(kimi finding 1, the strongest attack this proposal received, adopted as a
structural rule): `ST_FIRE` walks `eidx` once; for each valid edge with
`tk[e]=1` it emits an effect and clears the token; a tokenless edge's
effect is *parked in the egbuf* tagged with its dst, and the walk proceeds.
The core **never spins on a token**: per-op emissions are ≤ `EDGES_N` = 4,
the egbuf deepens to `EDGES_N + 1` = 5, so the core never blocks mid-op on
egbuf-full either — it finishes the op and returns to `ST_IDLE` holding
nothing. The parked effects drain from the egbuf when their tokens return
(token-gated *egbuf→ring* edge only — opencode's rule: gate the egress
edge, never the core). Fanout order was never semantically meaningful (M2:
the escape lane already overtakes; effect trains commute up to the dyadic
envelope), so deferral is free; the refractory counter suppresses re-fire
while the fanout drains. The effect transits (never parks at a full inbuf:
its landing slot is reserved by the token it consumed — K2). The peer's
core accepts it within `MAX_OP_CYCLES` (proven, `cell_core.fair`), setting
`ow[3]`; the next needle pass returns the token. Worst-case fanout drain:
two needle revolutions (§6, E5). No acks were sent, none were needed; the
ledger still closes because needles and effects are ordinary flits —
counted by A1/T1 exactly as before.

The hold-and-wait hazard this rule exists to kill (kimi's scenario): if a
fire *acquired* tokens mid-emission while holding the core, then `A`'s
`ST_FIRE` waiting on `tok(B)` while `B`'s `ST_FIRE` waits on `tok(A)` —
tokens that return only via the very cores being held — is a closed cycle
at the credit layer, F3 moved up one level, ring occupancy irrelevant.
Fire-with-skip plus the egbuf-depth bound removes the acquire-while-holding
shape entirely; the residual cross-op drain (back-to-back fires with parked
effects) is bounded by E4 tick spacing ≥ 128 ≥ `2·R_rev` at NB ≤ 16 — one
full token-return pass fits between consecutive fires. That bound is
obligation O8′, and it is now this proposal's weakest joint (§10).

---

## 4. The invariant list (formal, in the existing vocabulary)

Notation: `occ(p)` — occupancy of pipe `p` (the `a_v,b_v` pair the
flit_pipe proofs already speak over); `RingToward(d)` = number of non-needle
flits with `dst=d` resident in ring slices; `InbufToward(d)` = flits with
`dst=d` resident in `d`'s inbuf; `Held(d)` = `d`-tokens held by sources;
`Needle(d)` = 1 iff the needle's mask bit `d` is set; `RCAP = 2·(NCELL+1)`
ring slots; `Φ = Σ_flit dist(flit, dst)` — total remaining ring distance
(the potential function).

| id | statement (plain math) | class |
|---|---|---|
| **K1** | ∀d: `Held(d) + RingToward(d) + InbufToward(d) + Σ_c ow-bit(c→d) + Needle(d) ≡ K_d` | conservation (per-dst ledger) |
| **K2** | `RingToward(d) + InbufToward(d) ≤ K_d = 2` (inbuf depth) | landing guarantee (from K1: every other pool term is ≥0) |
| **K3** | `ΣRingOcc ≤ RCAP − 1` — a bubble always exists | non-satiation — **a configuration constraint, not a theorem** (kimi finding 5): the checked parameter inequality is `Σ_d K_d + 1(needle) ≤ RCAP = 2(NCELL+1)`, with *every* ring-resident class counted (cell traffic, io traffic, needle); ticks are local strobes, never ring flits |
| **N1** | needle mask bits: written only by owner-node set (at its own port) or first-taker clear — **combinationally in the ringport transit mux, atomic with single-flit motion** (kimi finding 3: mutability is required, and its clear must live on the comb path like `hit` does); needle count in fabric ∈ {0,1} from reset; io re-arm unconditional; missing-needle watchdog at `2·R_rev` with `gen+1` and census audit | single-writer / single-instance |
| **N2** | `ndl_census` at io return = occupancy delta since last return | audit accuracy (F2's silicon guard) |
| **C1** | needle absorption at io is unconditional (never enters an inbuf; never parks) | escape-class property |
| **M1** | `eps_c` non-decreasing; bumps only on state-mutating transitions | local monotonicity |
| **M2** | engine state after multiset M of trains + decay ticks depends only on M (order-free) up to the proven dyadic envelope | commutativity of the learning plane |
| **E1** | every response flit carries `(gen, eps_dst)` at emission | lease stamping |
| **A1′** | the existing `fabric.conservation` A1/T1/SER/DROP/FAN hold **unchanged**, with needles counted as ordinary flits | compatibility |

K2 is the wedge-killer; everything else exists to make K2 true and provable.
Note what K2 says in hardware: **a delivered hit always finds inbuf space**
— the parked-hit-with-full-inbuf state of the F3 anatomy cannot be
constructed, because the third flit toward `d` cannot exist while two sit in
`d`'s inbuf (K1) and never entered the ring (admission, R1).

---

## 5. The theorems

### Theorem W (wedge vacuity). *Under K1–K3, C1, and the existing proven
cell bounds, no reachable state has an empty set of enabled fabric actions,
and every enabled-busy cell returns to `ST_IDLE` within B_busy cycles.*

**Proof sketch (the drain argument — kimi cross-examined the first draft
into this form).** Assign each resident non-needle flit its ring distance
`ρ = dist(flit, dst) ∈ [0, NB)`, and consider the ring as an alternation of
maximal *occupied runs* and *bubbles* (empty slots).

- **Run-head progress.** Take the head flit `h` of any maximal occupied run
  (the flit whose next ring slot is a bubble — every run terminates in one,
  by K3). If `ρ(h) = 0` (at its dst's port): by K2, `InbufToward(dst) < 2`
  or `h` itself accounts for the gap — the inbuf presents space and `ld`
  is enabled; delivery fires. If `ρ(h) > 0`: the slot ahead is a bubble —
  **transit is enabled for `h` unconditionally.** (The first draft claimed
  this of the globally minimal-ρ flit, which is *false as stated* — the
  min-ρ flit can sit behind a far-dst transit flit inside a run; kimi
  finding 4. The run-head form is the correct carrier: it needs no
  minimality at all, only K3's bubble-per-run-termination.)
- **Measure.** The tuple `(occupancy, Σρ)` decreases lexicographically:
  transit preserves occupancy and strictly decreases `Σρ`; delivery
  decreases both. Injections increase it, but injections are token-capped
  per needle epoch (K1: at most `Σ_d K_d` admissions exist in the entire
  system) and every admitted flit is one transit-closer per enabled
  run-head step. The system cannot be quiescent-with-backlog: **the Drain
  property.**
- **Cores never hold-and-wait.** Fire-with-skip (§3.3) bounds per-op
  emissions below egbuf depth; the core returns to `ST_IDLE` holding no
  token-dependent obligation; the tick interlock is untouched (opencode:
  gate at `egbuf→ring`, never inside the core — the tick never waits on a
  token). Busy cores therefore return to `ST_IDLE` within `B_busy =
  MAX_OP_CYCLES + EDGES_N·R_rev` cycles, re-asserting `ci_ready`, draining
  inbufs, releasing tokens (K1's `ow` terms) — the credit layer cannot
  close a cycle because no core ever waits on a token while holding
  anything.

What the theorem does *not* claim: unbounded eventual drain against a host
that never drains `EXTID` — the external contract stands (as it does today).

### Theorem L (bounded drain — the liveness carrier, in the suite's own idiom).
Every admitted flit is accepted at its dst within
`B_admit = NB + B_busy + R_rev` cycles. Proven as an assert-within-N
countdown shadow (the `cell_core.tick`/`fair` convention — the repo's honest
form of liveness), at the fabric harness, NCELL=2 first. Claude's discipline
adopted verbatim: the claim is *"bounded drain under E5 + structural
acyclicity"*, and E5 is a **stated fabric contract**, not a free property —
exactly as E4 (tick spacing) is the scheduler contract today.

### Theorem C (coherence contract). Views are per-cell linearizable at epoch
granularity: two responses with equal `(gen, eps_c)` reflect identical cell
state `c`; a response with `eps_c = e` is stale iff `eps_c > e` now
(detected at the consumer). Learning state is order-free up to the proven
envelope (M2). No lost updates exist by single ownership (the core is the
only writer; the dialfile's second writer, the boot port, is already
excluded by construction — `q_cell.v`'s disjoint-window mux).

### Theorem S (conservation compatibility — the compatibility carrier).
`fabric.conservation`'s full assert set holds **unmodified** on the
token-needle fabric: needles, acks, effects are flits; the ledger counts
flits; K1 is a *second, orthogonal* conservation law over tokens, closed by
the same engine on the same boundary handshakes. Two conservation laws, one
fabric, one PDR run each.

---

## 6. Proof strategy — obligation by obligation, in this repo's idioms

The strategy sentence: **invariants on handshakes, not hearts.** The
existing prove-mode failures (L1/L2/L3 in FORMAL-PROOFS §2) all stem from
boundary harnesses that cannot see core/pipe interiors. Every TOKEN-NEEDLE
invariant is defined over events that are *already module-boundary
handshakes*: inject (`li`), deliver (`ld`), accept (`ci`), needle pass
(a position predicate on ring slice boundaries). That is the design
decision that makes this k-induction/PDR-shaped rather than hope-shaped.

| # | obligation | method | expected fate |
|---|---|---|---|
| O1 | K1 token conservation | extend `f_fabric_conservation.v` with token shadow accounts (mirror of the A1 ledger: +1 at consume, −1 at each return path); **`mode prove` + `abc pdr`** at NCELL=2 | closes — linear counter invariant over boundary handshakes, strictly easier than A1 (smaller pool); claude: "you're closer to conservation than to fairness — run PDR first on K1 alone" |
| O2 | K2 landing guarantee | **composition**: K1 (O1) + the already-proven per-module pipe contract `occ ≤ 2` (`tb/formal/flit_pipe.sby`, unbounded k-induction) + pipe-pop = ci-accept (inbuf accounting at its own two handshakes) | theorem, machine-checked at NCELL=2; the composition step is the doc's Lemma 2 |
| O3 | K3 non-satiation | arithmetic lemma from K1 + parameter inequality `Σ_d K_d + 2 ≤ RCAP`; in RTL, an io-level assert fed by `ndl_census` | closes trivially; also asserted as a cover-negation (a full ring must be *uncoverable*) |
| O4 | N1 single-writer needle | harness models the needle as a moving automaton (position + mask); writer legality = function of position vs. node id; **PDR** with two structural lemmas first (claude: needle-persistence, epoch-monotone — write them before the run) | closes at NCELL=2 (claude: likely), honest risk at NCELL≥4 (clause explosion) — stated |
| O5 | N2 census accuracy | io-side ledger identity — same shape as A1; smtbmc bmc then pdr | closes |
| O6 | M1/M2 | M1 local k-induction (one module, seconds — the flit_pipe experience); M2 as **two equivalence miters** on the engine's merge: `merge(merge(a,b),s) = merge(a,merge(b,s))` and commutativity — claude's recipe, `<1 s` each | closes |
| O7 | Theorem L bounded drain | assert-within-N countdown at the fabric harness (NCELL=2), depth = `B_admit` + slack, **bmc** then attempt pdr | bmc closes (the `cell_core.tick` idiom, scaled); unbounded pdr *not claimed* |
| O8 | Q2/I1 bound re-derivation | `cell_core.fair/tick` harnesses re-run with the egbuf→ring token gate, new constants `B_busy`, `I1b′ = I1b + R_rev` | closes with worse constants — the honest regression, priced in §7 |
| O8′ | cross-op fanout drain: back-to-back fires with parked effects drain within one E4 spacing window (E4 = 128 ≥ `2·R_rev` at NB ≤ 16) | fabric harness assert-within-N, NCELL=2, fire-heavy directed program | the weakest joint of the liveness story — the one obligation this proposal would be embarrassed to fail |
| O9 | E5 needle revolution ≤ R_rev = 4·NB | fabric-level assert-within-N on needle position (NCELL=2); the structural reason: K3 bubble + needle priority + C1 absorption | bmc closes; stated as contract E5 in the assumption ledger |

The assumption ledger gains one row, in the house format:

| id | used by | statement | real system |
|---|---|---|---|
| E5 | W, L, O7 | needle completes a revolution within `4·NB` cycles | enforced by R4 priority + K3 bubble + C1 unconditional absorption — itself machine-checked (O9); the analog of E4 for the scheduler |

If E5 smells circular (O9 proving the contract E5 that Theorem W leans on):
it is the same non-circularity as E4/Q2 — E4 is a *contract on the
environment* (scheduler spacing) proven of the *scheduler module*; E5 is a
contract on the needle proven of the needle datapath (O9). The dependency is
module-local, not theorem-local.

---

## 7. Honest costs (what breaks, what slows, what stays unverifiable)

- **Q2 tick deadline worsens.** The 100-cycle `ci_ready`-gap bound (Q2a1)
  becomes `100 + R_rev ≈ 164` at NB=16 in the worst case (fire stalls at
  egbuf→ring waiting a token; the tick interlock itself is untouched). The
  `cell_core.tick/fair` suites re-derive with larger constants — same
  proofs, worse numbers. This is the single worst regression and it is
  priced, not hidden.
- **The legal fabric shrinks by one cell (or one admission slot).** K3's
  configuration constraint `Σ_d K_d + 1 ≤ RCAP` binds at the top legal
  config: NCELL=15 with uniform `K_d=2` sums to 32 + needle > RCAP=32 —
  *not satisfiable* (kimi finding 5: the arithmetic is a config
  constraint, not a theorem, and one uncounted class voids the
  unrepresentability claim). Shipped configs: NCELL=14 with `K_d=2`, or
  NCELL=15 with one class at `K=1` and `K_EXTID=1`. This is the first
  proposal cost that touches the fabric's own size claim (largest legal
  fabric, SILICON-EXPERIMENTS §2) and it is stated as such.
- **egbuf deepens 2 → EDGES_N+1 = 5** (+3 FF×PW per cell ≈ +50 FF/cell —
  this, not the token bits, is now the dominant area line; total still
  ≈ +5% FF at NCELL=15). The depth bound is what makes per-op emission ≤
  capacity a structural fact rather than a promise.
- **Throughput ceiling now exists — by design.** Token circulation sustains
  ≈ `ΣK_d / (round-trip)` ≈ `2·(NCELL+1) / (4·NB)` flits/cycle ≈ 0.5 at
  NCELL=15 — ≈ 500k injections/M-cycles, against the measured post-fix P1
  rate of 497,608. **The measured workload fits with ~6% margin; the
  unbounded-injection regime that caused F3 is gone on purpose.** A workload
  2× heavier than anything measured would now throttle rather than wedge —
  the trade is the thesis.
- **Fire-storm learning rate caps.** P2's 15,600 fires/200k (78k/M) sits
  under the ceiling, but fire fanout latency stretches by up to two needle
  revolutions; refractory-period dial semantics interact (a fire held
  mid-fanout still leaks/refracts on tick) — semantics-preserving per M2,
  but a workload designer feels it.
- **Area.** +23 FF/cell (tk, ow, eps, gen) + ~45 FF needle at io ≈ +390 FF
  at NCELL=15 (~2.5% of the ~16–17k FF fabric — opencode's ballpark); the
  ringport changes are two AND terms in `li_ready` and a needle-recognition
  term — the ld_ready→li_ready timing arc stays removed (opencode: the
  token check is local-FF-only; no new cross-module arc).
- **Suite breakage (opencode's list, adopted as the port plan):** TBs that
  drive `li` with no needle in flight hang → tokens reset *open*
  (`tk=all-ones`, gating armed only after the first needle pass —
  post-reset the fabric is v1 until commissioned); golden payload compares
  break on the `a0` epoch → mask in TBs; the quiesce-repro gains a
  needle-progress witness.
- **Epoch ABA.** 4-bit `eps` wraps at 16 mutations; a view older than a
  full wrap reads fresh. Mitigated by the 8-bit generation in `(gen, eps)`
  (full ABA needs 4096 unnoticed mutations); *not eliminated* — bounded
  staleness detection with a stated bound, not an absolute one.
- **What stays unverifiable:** payload value-integrity V1 beyond BMC depth
  (unchanged); full-scale proofs beyond NCELL=2–4 (the conservation
  precedent — PDR's clause growth at NCELL≥4 is a stated risk, not a
  promise); unbounded liveness as anything but assert-within-N + E5; the
  host-drains-EXTID external contract; dials remain trust-on-bind.

---

## 8. Divergence from Rival A (against the landed PROPOSAL-A.md, SELVEDGE)

*Updated after A's doc landed (16:28). B's §1–§7 were drafted beforehand;
the shared specialists' scrollback had already revealed SELVEDGE's shape
(semilattice replicas, tick-renewed credits, bubble), and the final doc
confirms it — the deltas below are checked against the landed text.*

- **Where coherence lives.** A: in the *data* — semilattice merge makes
  replicas always-mergeable, generalized to a design law (A §4.2:
  non-commutative state is refused admission to the fabric). B: in the
  *admission* — wedges are made unrepresentable by landing guarantees
  (K2); data needs no protocol because it is single-owner + commutative
  (B §2). B's claim is smaller and cheaper: B refuses to re-house state
  that already has a home.
- **The wedge theorem's load-bearing strut.** A's Strut 1 (AX4, hole
  conservation) makes *ring saturation* unrepresentable; A's own T-B
  analysis concedes the live cycle (ST_FIRE→egbuf→inject→ring-gap) does
  not require saturation. B's K2 (landing guarantee) attacks exactly that
  cycle: no admitted flit can park at a full inbuf, so the cycle's first
  edge does not exist. Cost asymmetry: A pays ≤1/NB throughput and an
  unproven spending rule (OB-H1); B pays token machinery + the needle
  (~3% ring bandwidth) and one legal cell (§7).
- **Credits/leases.** A's `mcr` renews at the tick — zero renewal traffic,
  elegant, and it couples the transport protocol to the learning clock
  (both of A's struts consume E4; see ATTACKS-ON-A §6). B's tokens are
  event-loop (accept-driven), tick-agnostic, at the price of the needle's
  return traffic.
- **What B concedes to A.** Decay-in-readout is genuinely elegant and B has
  no equivalent (B leaves decay as-is, single-owner, untouched); A's §11
  lineage and §12 open questions make it the more scholarly document; and
  if A's OB-H1 spending rule exists and INV6 closes, A will have proven a
  clean safety invariant B deliberately chose not to carry (B's K3 is a
  config constraint, not a proved invariant — the honest asymmetry,
  stated so the referee sees that B knows it).

---

## 9. Specialist contributions (the cross-pollination ledger)

- **arena-kimi (K3):** delivered the strongest attacks this proposal
  received, all six adopted: (1) the credit-layer hold-and-wait cycle —
  killed the acquire-while-holding fire variant and forced fire-with-skip +
  egbuf depth `EDGES_N+1` (§3.3); (2) the mask-capacity token leak under
  `K_d`>1 returns per revolution — forced the sticky-deferral rule (R2) and
  the `ow` term in K1's conservation sum; (3) the immutability/taker
  contradiction — forced the comb-transit-atomic clear (N1); (4) the
  min-rank misstatement — Theorem W's proof now runs on maximal-occupied-run
  heads with the lexicographic `(occupancy, Σρ)` measure, kimi's form;
  (5) the config-constraint reading of K3 — now a checked parameter
  inequality with the NCELL=15 consequence priced in §7; (6) needle
  privilege/reset-loss — unconditional io re-arm, exactly-one-from-reset,
  watchdog with census audit. Also: the parked-hit-vs-bubble distinction
  (bubbles don't touch inbufs — the fact that forces *admission* as the
  load-bearing invariant), and, from its advice to Rival A visible in the
  shared scrollback, the bubble-rule/deflection suggestions that B subsumes
  as K3 + escape-lane-inheritance.
- **arena-claude (formal):** "invariants on handshakes, not hearts" is B's
  strategy sentence but claude enforced it — K1 needs per-flit token
  provenance (an L2-class lemma) *unless* token accounting rides the
  handshakes (adopted); N1 needs position-continuity/epoch-monotone
  structural lemmas *written before* the PDR run (adopted as O4's preamble);
  "acyclicity is safety not liveness — A holds token, B waits, C idle:
  acyclic deadlock" (adopted: Theorem L is the liveness carrier, W only
  orients it); the E_needle contract discipline (adopted as E5/O9); and the
  PDR-first-on-K1-alone sequencing (adopted as the O-runs order).
- **arena-opencode (RTL):** gate at egbuf→ring, never inside the core
  (preserves the Q2 interlock structure); needle as ACK-class
  src=EXTID=a2-marker, dst=EXTID (no cell hit-delivery, no OP_TICK
  collision); tokens reset open (suite compatibility); the in-transit
  clear is safe *only at the ri→ro handoff* (no stalled double-grants) and
  the needle must be exempted from V1/ENTRY-IDENTITY by op class (adopted
  into N1's statement); +2.5% FF; the 4-bit epoch ABA flag (adopted into
  costs); the TB-breakage list (adopted verbatim into §7).

---

## 10. What would falsify this proposal (pre-registered)

1. O1 fails to close under PDR at NCELL=2 within the conservation run's
   order of magnitude → the "second conservation law" claim is wrong.
2. The token-consume-at-inject vs flit-in-ring one-cycle window (token gone,
   flit still in egbuf — K1 must count egbuf-resident, token-consumed flits
   as in-flight, or the ledger has a hole exactly one handshake wide). If
   that window cannot be closed inductively, K1's shape is wrong.
3. N1's comb-transit clear admits a double-grant under the two-deep slice
   pipelining (needle resident in slice `s` while `s−1`'s head still
   presents the previous epoch's bits). This is N1's real content; if O4
   finds the race, R3 needs positional arbitration and the needle dat
   becomes a two-flit convoy.
4. **O8′ fails** — back-to-back fires under E4 spacing do not drain within
   the window (the cross-op drain argument leans on `2·R_rev ≤ E4`, which
   holds only for NB ≤ 16; a wider fabric or a faster tick breaks the
   inequality and with it Theorem L). This is the weakest joint, moved
   here after kimi's hold-and-wait finding forced the fire-with-skip
   redesign: the *core* is now safe by construction, and all remaining
   risk lives in this one window bound.
5. The needle's in-transit mutation defeats the flit-pipe harness idiom
   (the shadow FIFO of `flit_pipe.fly` assumes payload stability through
   the slice; if the needle class cannot be exempted cleanly by op class,
   V1's BMC cover is void for needle traffic and N2's audit becomes the
   only guard).

— Rival B, 2026-08-31. The needle exists; the wedge does not.
