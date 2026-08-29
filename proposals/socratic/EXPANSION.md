# Socratic Expansion — The Preferring Fabric

**Lane:** DeepSeek Flash, banter hammer · **Round:** 2.5 (post-cross-review)
**Working names:** `q_memlink` (the one primitive) · `q_prefer` (the cell)
**Inputs:** all five competition entries + the round-2 scorecard. Winner chassis
glm (age-bucket ladder, ring-as-quilt, shared math tail); mandated steals
(zeroclaw's hyperbolic decay counter, opencode's runtime dial map + train-to-fire
acceptance test); seed's wire-state instinct, rehabilitated; claude's
honest-limits discipline, kept.

---

## 0. The pick, stated before the arguing starts

The strongest cross-pollinated direction is **not** "glm plus the steals done
carefully." That is the build; this document is the *expansion*. The direction I
take is the one the field circled and then flinched from, in four separate
places:

- **seed** said "all edge state lives in the wire, not in cells" and then
  delivered bit-overlap products and a fabric that can't route. The *instinct*
  was right; the implementation was a hallucination.
- **glm** said "the network is the quilt" and then kept routing (bypass ring)
  and memory (edge RAM) as two structures anyway.
- **opencode** said "the control plane rides the ring" but kept a separate
  tick scheduler as a hard time plane.
- **zeroclaw** said "the reading is the cheapest thing in the circuit" and then
  parked the reading in a per-cell primitive bank, orthogonal to the links.

The direction: **unify until the design has one degree of freedom left.** One
primitive — the link — is the IO contract, the intercell connection, the CDC
boundary, and the clock. One table — the routing table — is the topology, the
Hebbian memory, and the readout. One clock — the event — is the scheduler, the
decay driver, and the epoch. Then ask the four questions the field ducked:
1M cells, total unification, cross-domain meeting, Hebbian state in the routing
tables. Every question turns out to have the *same* answer, which is how you
know it's the right direction: **memory is routing, time is traffic.**

Ten rounds. Each round changes the design. The final round is the synthesis.

---

## Round 1 — The Contract Is the Link (total unification, attempted)

**Propose.** Every entry carries two stream contracts that are *shaped* alike
but *treated* differently: the ingress/egress contract for devices (frames,
command-granular) and the intercell link (flits, beat-granular). glm literally
writes "exactly one streaming contract exists in the fabric" and then gives the
ring a bypass register and the adapter a frame packer — two implementations of
one idea, which is one implementation too many.

Unify: **there is one primitive, the link. A link is a unidirectional word
stream. A cell is a node with links. A device is a leaf cell with zero link
table and one leaf function (framing/encoding). A bridge is a cell whose leaf
function is a second link. An adapter is not a thing; an adapter is a cell
with no edges.** Law 4 ("any IO can enter a cell") stops being a promise about
adapters and becomes a tautology: IO *is* a cell. There is no control plane
beside the data plane; `qm_bind` is traffic like everything else.

```
q_memlink  (the ONLY primitive)
  s_valid, s_ready, s_data[W-1:0], s_last     // source→sink
  m_valid, m_ready, m_data[W-1:0], m_last     // sink→source (responses)
```
`last` is the frame terminator. A *frame* is the unit of meaning; a *word* is
the unit of transport. This is exactly the old ingress contract — promoted to
be the whole fabric. The ring, in this light, is just N cells chained by
links; the seam is a link; the tick broadcast is a link.

**Attack.** Single-beat simplicity dies. glm's ring moves one flit per hop per
cycle and every flit is a complete operation. A frame is N words; `qm_bind`
carries a config word, `qm_effect` carries an activation, `qm_view` needs a
response — so a "view" is at minimum a two-frame transaction (request frame,
response frame). The ring now has to carry multi-word things, and the moment
you say "frame" you owe an answer to: what happens if a frame is half-way
through a cell and the cell stalls? What happens when two frames interleave at
a cell that is both transiting and injecting? The entries dodged this by
making beats atomic. Unification buys conceptual elegance at the price of
transactional complexity — and the Law says verified or it doesn't exist, and
nobody has verified a mid-frame stall.

**Revise (design change: frames on the ring, wormhole words).** Accept the
frame; make the *word* atomic instead of the flit. A frame is a sequence of
words with `last=1` on the final word; the head word carries `{op, dst, src}`,
body words carry payload. **Only the head word is decoded.** Intermediate cells
retime body words blindly (one cycle per word — they are bypass registers, as
in glm, but for words, not flits). Delivery is at frame granularity: a cell
accepts a head word only if it has room for the whole frame — a **frame credit**
— so once a frame starts entering, it never stalls mid-frame (wormhole without
the hazard, because there is exactly one direction on a ring and bubbles are
free). Responses are frames. Requests and responses interleave freely; the
`dst`/`src` fields in the head word sort them at the consumer. The cost glm
paid in "one beat = one op" is repaid as: **the IO contract and the intercell
link are now literally the same wires, and a device plugs into the fabric by
speaking the same `last`-terminated word stream a cell speaks to a cell.**

State change: the fabric moves words; meaning moves frames; decode happens
once per frame, at the head.

---

## Round 2 — Attack the ring's cargo: what is a frame, actually?

**Attack.** We unified the transport, but not the *opcode encoding*. Look at
the five opcodes through the frame lens: `qm_link` is a cofire event —
one word, `{op=link, dst, payload=edge-hint}`. `qm_effect` is a touch — one
word plus an activation. `qm_bind` is a config write — head word + config
word(s). `qm_view` is a request; the *response* is a separate frame. `qm_tick`
is a broadcast. So frames have wildly different lengths (1 to N words) and the
cell core must assemble frames of unknown length per opcode. That is a parser,
and parsers in Verilog-2005 are where bugs go to breed. Worse: `qm_link`
(the *learning* opcode) being a one-word frame means the head word must carry
the edge hint and the activation payload in the same word — glm's flit already
has this problem and solved it by putting everything in one packed word with a
3-bit opcode. We just un-packed it. Did we actually gain anything, or did we
build a slower glm?

**Revise (design change: the word IS the flit; the frame is a multi-word
flit, and the unification is at the *port*, not the packet).** Keep the
packed single-word frame for the common ops — `link`, `effect`, `tick` are
one-word frames, exactly glm's flit format (`{op[3], src, dst, ttl, data}`).
`bind` and `view`-response are two-word frames: head word + one operand word.
The cell core assembles at most a 2-word frame — that is not a parser, that is
a two-slot FIFO. The unification claim survives unchanged, because it was never
about packet format: **the IO contract and the intercell link are the same
port, same wires, same `last` terminator, same credits; a device's framing
leaf and a cell's core both hang off identical links.** The difference between
"device" and "cell" is not the wire; it is what is on the other end, and the
fabric cannot tell the difference, which is the entire point. A UART plugged
into a cell speaks the same protocol as the cell speaking to its neighbor, and
the neighbor cannot tell which is which. Law 4 becomes structural.

State change: one port, one protocol, one- and two-word frames only; `ttl`
lives in the head word and is decremented once per cell that decodes it (not
per hop), so a long frame pays TTL once, not N times.

---

## Round 3 — The routing table is the memory (the seed rehabilitation)

**Propose.** Now the interesting theft. seed's one true idea: edge state lives
*in the transport*, not in a memory parked beside it. seed botched it (no
backpressure, "product" via bit overlap, no routing). Take the idea, give it
real structure: **the Hebbian edge table and the routing table are one table.**

Concretely, in the unified fabric a cell's only substantial state is a small
table. In glm it is `edge RAM: {dst, ladder, base, flags}` and routing is
mechanical (bypass unless dst==me). But the moment the fabric has *any* choice
— two bridges off the ring, a tier-L cluster, an IO leaf with two links — the
cell needs a routing decision: which link does a frame for region R take? And
the Hebbian memory needs: how strong is the association between this cell and
that one?

Make them the same entry:

```
route-mem entry:  { prefix (region/dst),  next_link,  W (u16),  age (u24),  flags }
```

- **Routing reads the weight.** Frame for prefix P: among entries matching P,
  pick the one with the highest W (ties by port order; exploration dither in
  R8). The weight is a *preference*, a soft routing priority.
- **Hebbian writes the weight.** When a frame is routed via entry e and the
  far end responds (ack/effect receipt — the fabric's co-activation signal),
  `W_e ← W_e + 1` (saturate). When a route times out (ttl drop) or the far end
  goes dark, `W_e` is marked and decays faster (anti-Hebbian: *wire together,
  die together*).
- **Decay is the steal, applied here:** every event at the cell advances the
  age of all entries; when `age ≥ P₀ >> 2·msb(W)`, `W ← W−1`, `age ← 0`
  (zeroclaw's counter trick, RTL cost: one shared priority encoder, two
  shifts, one comparator). The hyperbolic law `W(t) = W₀/(1+W₀·t/P₀)` is the
  memory doctrine, now living in the router.

The doctrine that falls out: **fire together, wire together — and the wiring
is literal.** Co-activating cells become preferred routes for each other.
"An edge" is no longer a stored fact; it is a persistent preference in a
forwarding table. A memory that is never used decays to nothing (hyperbola),
and the only way to strengthen a memory is to route traffic over it — which
is what Hebbian potentiation *means* in silicon: use is the update.

**Attack.** Three things break immediately.

1. *Rings don't route.* On a single ring, the bypass is mechanical; there is
   no decision, so the weight is decoration. The idea only earns its keep at
   the moments the entries defer: bridges, tier-L, multi-ring. So this
   proposal is parasitic on R4's scale story — fine, but it must be said.
2. *Route ≠ edge.* An edge (a→b) is a dyadic association. A route entry
   (region R via link L) is a *many-to-one* preference. The memory is now
   about regions, not peers; fine at scale (you cannot have 10¹² peer edges
   anyway — see R4) but it silently changes what "remembering" means: the
   fabric remembers *neighborhoods*, not neighbors.
3. *Positive feedback.* Rich-get-richer: the route that is used gets
   stronger, so it gets used more. Without homeostasis this is a stampede —
   one bridge saturates while its twin rots, and the fabric is
   un-recoverable because decay (hyperbola) is *slower* than potentiation
   (+1 per use). Every entry except opencode ignored homeostasis; opencode
   admitted it (limit 3) and punted.

**Revise (design change: two-class table + bounded exploration).** The route
table has two classes, distinguished by a flag bit:

- **structural entries** — written by `qm_bind`/`qm_link` with `lock=1`.
  The ring's neighbors, the bridge, the leaf. Never decay below a floor
  (`W_floor`), never evicted. These are the *anatomy* of the fabric.
- **learned entries** — created on demand by cofire, `lock=0`. Decay by the
  hyperbola, evictable (LRU among learned entries, because the table is
  finite), and **homeostatic**: on readout, W is compared against the sum of
  W over sibling entries sharing `next_link`-competition (an approximate
  divide via the shared math tail — one tail visit per readout, at tick
  pace, which is what the tail is for). Saturation at W_max is structural;
  a stampede saturates and *stops*, then hyperbola decay pulls it back.

The Hebbian update is now: potentiate on use, decay on time (event-count,
R6), suppress on competition, floor for anatomy. That is a complete learning
rule in one table, ~50 gates per entry over the counter trick. Memory and
routing are one structure, and the read of a memory — choosing a link — is
the retrieval. **A view of "the quilt's knowledge" is a view of its routing
preferences.** No entry dared this because they all kept memory as a
read-out-of-band structure. The unification is the point.

State change: the edge table and the routing decision are the same table;
learning writes preferences, routing reads them; anatomy is locked, knowledge
is learned.

---

## Round 4 — What happens at 1M cells (the math forces the unification)

**Propose.** Ask the question the entries all avoided with parameter tables:
1M cells. glm's ring is O(N) latency — 1M hops is dead on arrival. claude
caps at ~256 by arbiter timing. seed claims 256×256 and then admits wire
delay kills it. The honest answer is the one glm half-built and stopped:
**the fabric is a hierarchy of rings, and every level is the same cell.**
Cluster rings of ≤16 cells → super-ring of bridges → backbone. 1M cells =
~4 levels. Latency is O(log N × ring size), not O(N). "Bridges are cells"
was glm's distribution story; the expansion is that it is *the whole* story —
there is no other topology. A frame climbs the hierarchy until it finds the
ring that contains its destination, then descends. The routing table at each
cell is a **prefix table**: entries for things on this ring (structural,
exact dst) and entries for regions up/down (structural bridge + learned
region preferences).

**Attack.** The memory budget is the real story, and it is brutal. Per-cell
per-destination edges at 1M cells = 10¹² entries. Impossible. Even per-cell
*region* tables at 4 levels: 1M cells × (16 local + 16×3 up-level) ≈ 60M
entries ≈ at 94 bits/entry (glm's number), 700 MB of BRAM — spread over 1M
cells that's 700 bytes/cell, which is *fine*, but only if the memory is
routing-shaped. The conclusion is forced: **at 1M cells there is no such thing
as an edge table; the routing table is the only memory that can exist.**
Which means the R3 unification isn't a clever choice — it is the only
mathematically possible layout. Scale doesn't merely tolerate
memory-in-routing; it *demands* it. That is the strongest argument the
direction has: the four questions the field ducked have one answer because at
scale there is only one answer.

**Attack, second barrel — time.** The global tick is the other thing that
dies at 1M. A single `q_tick_sched` broadcasting to 1M cells is a clock tree
with a skew problem and a *sweep* problem: glm's decay sweep walks the edge
RAM address by address; opencode's tick phase does the same. At 1M cells the
tick itself is the bottleneck — every cell must decay every edge every tick,
and ticks must be globally coherent for the golden model to mean anything.
The entries dodged this with "HAS_WHEEL future work" and parameter tables.
Scale forces: **time must be local.** Each cell keeps its own time; the
fabric has no global clock of events. Which is exactly where R5 and R6 go.

**Revise (design change: hierarchy + local time are the scale contract).**
1M cells is 4 levels of the same cell, prefix routing, and **no global tick**:
each cell's decay runs on its own timebase (see R5/R6), and hierarchy only
needs *approximate* time agreement — which is precisely the regime where
zeroclaw's power-law decay is the unique right law, because a 2× tick-rate
error is a 2× shift of P₀: it parameterizes the memory horizon, it does not
break it (zeroclaw §2.4, the "silicon approximation that provably doesn't
care about clock slop"). Every entry's decay law was chosen for its gates;
the expansion is that power-law decay is the only law that survives scale.

State change: topology = recursive hierarchy of rings (same cell, bind
config); time = local; decay law = hyperbola, chosen because it is the only
law that doesn't need a clock.

---

## Round 5 — Two fabrics meet: the clock domain question

**Propose.** The entries all said "single clock inside the fabric; adapters
own CDC." The expansion's unified fabric deletes that sentence: **the link
carries its own clock.** The link primitive is source-synchronous:

```
q_memlink (source-synchronous form):
  s_clk         // forwarded source clock
  s_valid, s_data[W-1:0], s_last
  s_ready       // credit return, itself CDC'd
```
The sender forwards its clock with the data; the receiver samples on the
forwarded clock and returns credits through a small async FIFO (the only
allowed CDC in the design, and it is *inside* the link primitive, not in a
device adapter). Consequences:

- A cell is a **GALS island**: locally synchronous core, asynchronous
  frontiers. This is a real, buildable discipline (globally-asynchronous
  locally-synchronous is textbook; source-synchronous links are standard
  silicon practice).
- Two fabrics meet by *linking*. There is no joining ceremony: fabric B's
  boundary cell and fabric A's boundary cell hang a `q_memlink` between them
  (source-synchronous), and each keeps its own time forever.
- Law 4's "adapters are thin and dumb, they own CDC" is amended: **CDC is the
  link's job, not the adapter's.** Adapters get thinner; the primitive gets
  the only async logic in the system, in one place, verified once.

**Attack.** What actually breaks when two clock domains meet — name it, don't
wave at it:

1. *The tick.* Domain A's tick phase means nothing in domain B. A global tick
   count is a lie. (Answer in R6: the tick was already demoted.)
2. *Edge state at the seam.* An edge that spans the boundary has two clocks;
   its `age` counter is ambiguous — which side advances it? If both, the edge
   decays twice as fast; if neither, it is immortal. (Answer: the seam edge's
   age advances on **co-activation events**, not ticks — R6 makes this the
   general rule, not a seam special case.)
3. *Frame integrity.* A frame crossing CDC cannot be sliced mid-frame — the
   `last` terminator must arrive intact. (Answer: the frame credit — R1 —
   means the source holds `valid` until the whole frame is accepted; the link
   delivers frames atomically by construction, because it is a word stream
   with a terminator and the sink buffers a frame. Actually: sink must accept
   words only when it can accept through `last`, which the frame-credit
   scheme already guarantees. One invariant, two problems solved.)
4. *Asymmetric decay.* Fast domain decays its half of the seam edge faster.
   (Answer: this is *correct*, not a bug — the seam edge's strength reflects
   both sides' activity, and a fabric that is 10× more active should dominate
   the shared memory. The hyperbola in event-count makes the asymmetry
   *self-consistent*: each side's decay is measured in its own events, and
   the readout weight is a ratio, not an absolute.)

**Revise (design change: GALS is the clocking model; the link is the clock).**
v1 ships single-clock cells (as every entry does — honesty) but the *contract*
is written GALS: links are the time boundaries, cells are islands, and
nothing above the link assumes a shared clock. The first multi-domain build
is a parameter change (link form) plus the async-FIFO credit return — one
module, one TB — not a fabric redesign. And the seam-edge rule generalizes
into R6's headline.

State change: cells are synchronous islands; links are self-clocked; the
fabric is GALS by construction, and "two fabrics meet" reduces to "two links
touch," with no shared time anywhere.

---

## Round 6 — Event-driven time (the clock is the traffic)

**Propose.** Pull the thread from R5. If seam edges age on co-activation
events, why do *any* edges age on ticks? The Hebbian doctrine is
"neurons that fire together, wire together" — time, for a learning fabric,
is *measured in firings*. Make it general: **each cell's local time is its
event stream.** Every word/frame the cell processes (cofire, effect, bind,
view) is one event; every route-mem entry's `age` advances by one per local
event; the decrement rule is exactly zeroclaw's, with age in events instead
of ticks:

```
every local event:  age_e ← age_e + 1   for all entries e (one shared counter
                    per entry — the per-event cost is one increment + one
                    compare, amortized; O(1) per entry per event)
if age_e ≥ P₀ >> 2·msb(W_e) && W_e > 0:  W_e ← W_e − 1; age_e ← 0
```

The tick becomes what it should have been all along: **advisory.** A local
free-running clock (or, in v1, the broadcast tick — see honesty below)
backstops the case the event stream cannot cover: a *silent* room. A room
with no traffic has no events, so event-driven decay would make its memory
immortal — which is wrong (contrast needs forgetting even in silence; a
deserted room should not remember forever). So the rule is: **decay fires on
whichever comes first — the event count or the clock backstop.** Busy cells
learn and forget on their own traffic; quiet cells forget on the clock. The
two timebases are interchangeable because the hyperbola parameterizes slop
(R4): a factor of 2 in event rate is a factor of 2 in P₀, and P₀ is a dial
(opencode's dial map, stolen), not a truth.

The kill shot: **the fabric no longer needs a global scheduler to learn.**
qm_tick survives as an opcode (Law 2, five verbs, no deletions) but its
semantics shrink from "run the scheduler one quantum" to "advance the epoch":
a tick frame is a *time reference* a cell may use to reconcile its event
clock with wall-clock-ish epochs — the fabric's NTP, not its heartbeat. The
hardware `q_tick_sched` broadcast is demoted to a v1 convenience (single
clock) and a v2 optional (a tick source is just another cell with a free
running leaf function — a "metronome cell").

**Attack.** Four objections, all real:

1. *The Law.* `qm_tick(dt)` in the C reference advances time. Event-driven
   decay diverges from the golden model: the RTL's W(t) is now a function of
   traffic, not of dt. The C quilt and the RTL quilt will disagree on when
   edges decay. (Answer: the golden model is updated to *event semantics* —
   the reference gets the same rule: decay on event count or tick, whichever
   first. The C model is a simulation of the same law, not a different law.
   Divergence is a spec change, documented, not a bug.)
2. *Silent immortality.* Handled by the clock backstop above. But note the
   subtlety: the backstop makes memory *bounded* in silence, while event-
   driven decay makes memory *activity-proportional* in noise. That is the
   correct doctrine: what you keep is what you use.
3. *Nondeterminism.* Event-driven state is a function of event *order*, and
   order is a scheduling artifact. Verification doctrine (R9) must change.
4. *The age counter is per-entry per-event.* At 1M cells × 64 entries, that
   is 64M increments per "fabric event" — but no, that's wrong: an event at
   a cell advances *that cell's* entries only. Per-cell cost is O(entries)
   per local event, which is the same O(entries) the tick sweep paid, except
   now it's spread over the fabric's natural activity instead of piled into
   a global quantum. Busy cells pay more — correct, they are the ones
   learning.

**Revise (design change: event-count decay + clock backstop; tick demoted to
epoch reference).** Adopt the hybrid. The learning fabric is self-timed by
its own traffic; the clock is a hygiene backstop; the tick opcode is an
epoch reference that also happens to be the v1 single-clock backstop. One
doctrine for all time: **the only clock the fabric needs is the sound of its
own traffic, and the only memory it keeps is the memory it uses.**

State change: decay is event-driven with a clock backstop; the global
scheduler is gone; qm_tick is a time-reference opcode; the golden model is
re-specified to event semantics.

---

## Round 7 — First synthesis attempt: put it all together and see what's left

**Propose.** Assemble R1–R6 into one picture and audit what remains.

```
q_prefer (the cell) — a GALS island
├── core FSM            decodes head words; assembles ≤2-word frames
├── q_dialfile          runtime dials (opencode's map: ETA, THRESH, P₀, ...)
├── route-mem table     THE table: {prefix, next_link, W, age, lock} 
│   └── q_hyper          shared priority encoder + shifts (zeroclaw counter)
├── leaf function       (optional: framing/encoding for devices; another
│                        link for bridges; a free-running osc for metronomes)
└── q_memlink ports      all of them, identical, self-clocked
```

Removed from the world, compared with the winner chassis:
- the separate edge RAM (merged into route-mem);
- the global tick scheduler as a hard time plane (demoted to epoch reference;
  a metronome leaf is a cell);
- the separate control plane (config is traffic);
- adapter CDC (moved into the link primitive);
- the router/bridge special case (a bridge is a cell with a leaf = second
  link; glm said this, the expansion means it: no bridge RTL exists);
- the readout path for "memory" — there is no readout path, there is only
  routing. `qm_view` reads the route-mem table, which is the same table
  routing reads. One structure, two access patterns.

What remains, and is genuinely hard:
1. **Route selection is a decision with dynamics.** R3's homeostasis + dither
   is a control loop; loops oscillate.
2. **View coherence.** `qm_view` is a snapshot. Snapshot of what time? With
   no global clock, "now" is local. (R8.)
3. **Determinism doctrine.** "Verified or it doesn't exist" was written for
   cycle-deterministic RTL. Event-driven GALS is not cycle-deterministic.
   (R9.)
4. **Deadlock.** Wormhole words + learned bridge choice = cyclic buffer
   dependencies at hierarchy seams, the classic NoC disease. (R8.)

**Attack.** The synthesis is a skeleton with three open wounds (dynamics,
coherence, determinism) and one potential fatal one (deadlock). A socratic
document that stops here would be a vibe, not an architecture. Push.

**Revise (design change: scope the learning, keep the doctrine).** The
doctrine — memory is routing, time is traffic — is not negotiable. The
*learned decision surface* is: **v1 learns only bridge selection.** The
fixed ring is the substrate (structural entries, locked, zero decision);
the only learned choices in the fabric are "which bridge do I send region-R
traffic to" and "does this cofire create a learned entry." That is a small,
low-frequency, high-value decision surface: a cell with two bridges makes one
bit of decision per region, at bridge traffic rates (not per-frame
wormhole routing). Wormhole per-hop routing stays mechanical (rings, bypass),
so deadlock analysis is the classic single-ring result (glm's wrap-priority
argument) plus the hierarchy's acyclic up-down rule — **the bridge graph is
a tree** (each cell has exactly one structural up-link), so hierarchy
deadlock is structurally impossible in v1. The dynamics problem (oscillation)
is bounded by the tree: a stampede at a bridge saturates, decays, and the
dither (R8) eventually re-explores. We do not need a general theory of
learning routers; we need a 2-bit decision with a leaky integrator, and that
is a tractable RTL module.

State change: learned decisions are confined to bridge selection on a tree;
per-hop routing is mechanical; deadlock is bounded by construction; the
doctrine survives at the scale it was made for.

---

## Round 8 — Attack the synthesis's wounds, one by one

**Attack 1 — route oscillation.** A Hebbian preference on a tree is a
multi-armed bandit with a saturating integrator. Classic failure: the bridge
that wins early gets used, gets stronger, gets used more — the stampede of
R3. Homeostasis (divide by sibling sum) makes the *ratios* stable but
introduces a second failure: *flip-flopping* when two bridges' weights are
near-tied and decay jitters the winner. A tie is a metastable decision.

**Revise 1:** **epsilon-greedy dither with a saturating counter.** Route
selection: if `W_winner − W_runner ≥ Δ_min` (a dial, e.g. 1/64 of W_max),
route deterministically; else route to the winner with probability
`(1−ε)` and to the runner with `ε`, where ε comes from a small LFSR (seed
already has LFSR noise; the entries all reject "true randomness," and an
LFSR is fine — it is a *decision* dither, not a *state* dither; the state
remains deterministic). The deadband `Δ_min` is the anti-flip-flop
mechanism, the same spirit as glm's deadband snap on dial leak — the field
already has the pattern, we just apply it to routing. Exploration is
bounded (ε ≤ 1/8), so stampedes are escapable but not frequent.

**Attack 2 — view coherence.** `qm_view` snapshots a table that is changing
underfoot. In a GALS fabric, "as of now" is undefined. If a view is
permitted mid-write, the reader sees a torn entry.

**Revise 2:** views are **event-ordered snapshots**. The cell's core
serializes: an event (frame processing) and a view are both operations on
the core FSM; the core is a single FSM (it already is — opencode's
cooperative core, "no interrupt, each opcode runs to completion"), so a view
is atomic *with respect to the local event stream* by construction. The
semantics: "the state as of the last event before this view." Cross-domain
views (view a neighbor's table) return the neighbor's *last-sent* value —
the route-mem readout that the neighbor itself publishes at epoch
boundaries. The fabric's answers are all "as of some event," and the event
count is the timestamp. This is exactly how distributed systems do it
(vector clocks, lite) — the expansion is that the fabric *is* one, because
it has no shared clock to do better.

**Attack 3 — the affinity cache.** At 4 levels, a learned entry per region
per bridge per cell is still the bulk of the table. But most traffic is
*local*: the 80/20 of rooms is that cells talk to their neighbors. A cell
that must climb 4 levels for a cold destination pays latency AND creates a
learned entry that will decay unused.

**Revise 3:** keep R3's table, add a **learned-affinity sidecar**: a small
(4–16 entry) cache of `{dst, next_link, W}` for *recent exact destinations*,
LRU-evicted, potentiated by use, decayed by the same hyperbola. This is a
TLB for memories: the fabric's hot knowledge is exact-peer and cache-resident;
its cold knowledge is regional and routing-shaped. The sidecar is the same
entry format (one table, two classes — R3's lock flag again), so it is not
new RTL, it is a second bank of the same structure. Views of the sidecar
are the "who do I actually talk to" readout — which is, not coincidentally,
the readout the fleet's elephant software calls "the room's edges."

**Attack 4 — determinism (the deep one).** This gets its own round.

State change: dither + deadband make bridge selection a bounded bandit;
views are event-ordered snapshots with event-count timestamps; a TLB-like
affinity sidecar (same entry format) carries hot exact-peer memory.

---

## Round 9 — Verification under event-order determinism

**Attack.** The README's Law 5 — "verified or it doesn't exist" — was
invented for cycle-deterministic RTL with golden models. The synthesis
abandoned cycle determinism: GALS islands, event-driven decay, LFSR dither,
local clocks. A `tb` that compares RTL state after N cycles against a golden
model is meaningless if the RTL's event order is a scheduling artifact. If
we cannot verify it, the doctrine says it does not exist — the synthesis
must be *un-built* unless we find a verification semantics that survives.

**Revise — the key claim: event-order determinism.** The fabric's *state* is
a deterministic function of its **event trace** — the sequence of frames and
views entering each cell, in order — *independent of clock phase, skew,
jitter, and cycle counts.* Why this is true, by construction:

1. All state changes happen inside the core FSM, one event at a time,
   serialized (cooperative core, R8). The core is a pure function of
   (state, event).
2. Decay is event-count + backstop; the backstop's *order* relative to
   events is the only nondeterminism, and it is bounded: the backstop is
   equivalent to injecting a "clock event" at some point in the trace, and
   the hyperbola's slop-tolerance (R4) means any placement within the
   backstop period yields state within the same dyadic envelope. The
   verification bound is *envelope*, not equality — and zeroclaw already
   made envelope-assertion respectable ("the staircase is an envelope,
   asserted as envelope-only").
3. LFSR dither is deterministic given the LFSR seed and the event count —
   the seed is a *testbench input*, so a trace determines the dither
   sequence. (The fabric's "randomness" is a function of its seed and its
   traffic — deterministic given both, which is what verification needs.)
4. Inter-island races (two cells firing at each other across a link): the
   link's frame-credit makes delivery atomic per frame, and frame *order*
   per link is the order of the source's events — so the cross-island state
   is a deterministic function of the *merged* trace. This is trace theory /
   asynchronous verification, textbook, and it is exactly why the
   synchronous entries' TBs (cycle-compare) cannot be reused as-is but their
   *golden models* (state machines over opcode streams) port directly: they
   were already event models wearing cycle clothes.

**So the verification doctrine survives, upgraded:** every TB's golden model
becomes a function of the event trace, and the pass criterion is
`RTL(trace) == golden(trace)` within the decay envelope. The fabric is
deterministic where it must be (opcode semantics, routing, saturation) and
envelope-deterministic where it is allowed to be (decay placement), and both
are checkable with iverilog + a trace driver. The acceptance test — opencode's
train-to-fire-decay — becomes a *trace* test: bind → link → 100 co-active
effects → fire → decay, asserted at event boundaries instead of cycle
boundaries. Same scenario, same assertion, new clock.

TB table (delta from the field's plans — the point is which TBs *change*):

| TB | What changes vs the entries' plans |
|---|---|
| tb_q_memlink | + source-synchronous form, credit return, frame atomicity under jitter (modeled clock skew, not real CDC) |
| tb_route_mem | golden = event-trace model; hyperbola envelope assertion; LRU eviction order; lock/floor invariants |
| tb_bridge_select | dither deadband: no flip-flop in the Δ_min band; stampede escapes within ε·N events; saturation → decay recovery |
| tb_affinity_sidecar | hot/cold promotion, LRU+W eviction, view readout = "as of event N" |
| tb_q_prefer_cell | opcode FSM over trace; event-ordered view atomicity |
| tb_fabric_accept | opencode's train-to-fire-decay, trace-driven; two-fabric meeting: link two cells with different clocks, assert envelope convergence |
| lint/synth | verilator -Wall + yosys smoke, as before; GALS form is a parameterized link form |

State change: verification is re-based from cycles to event traces; the
doctrine survives; the acceptance test is trace-driven; determinism is
restored at the level the fabric actually has it.

---

## Round 10 — Final synthesis: the Preferring Fabric, complete

**The assembled design, in one breath.** A quilt cell `q_prefer` is a small
synchronous island that speaks one language — the `q_memlink` word stream,
self-clocked, frame-atomic, carrying the five quilt verbs in one- and
two-word frames. Its only memory is a routing table whose entries are
simultaneously topology (structural, locked), knowledge (learned, decaying
hyperbolically by event-count), and decision (route preference with
homeostasis, dither, and deadband). Devices are leaf cells; bridges are
cells with two links; metronomes are cells with an oscillator; a tick is an
epoch reference, not a heartbeat. Fabrics meet by touching links and keep
their own time forever. At 1M cells the same cell composes into a tree of
rings, and the memory — which had no other place to live — lives in the
router, because that is the only place it *can* live.

**The surprising idea, stated plainly.** The entries all treated memory as a
store that is *read* (views) and then *used* (routing, gravity, contrast).
The synthesis inverts it: **the read IS the use.** The fabric has no
readout of its knowledge other than its own routing choices. A stored
preference that never routes a frame decays to nothing; the only way to
remember is to use. And the clock that drives this memory is not a clock at
all — it is the fabric's own traffic. Hebbian time is event-count; a silent
quilt has no time (its memory is frozen until the clock backstop, which is
itself local); a busy quilt ages and forgets in proportion to its own
activity, which is the most faithful possible silicon reading of "neurons
that fire together, wire together." The quilt does not remember by storing.
It remembers by preferring. Its long-term memory is its wiring.

**What v1 actually ships (honesty, per the discipline):**

- Single-clock cells (GALS contract in the spec, source-synchronous link as
  the parameterized v2 form, async credit-return module + TB listed but
  built second).
- One `q_memlink` port contract, one- and two-word frames, frame credits,
  ttl on the head word.
- Route-mem table (two classes, lock flag, hyperbola decay via the shared
  priority encoder — zeroclaw's counter trick — driven by event-count with
  tick backstop), affinity sidecar, bridge-selection learning with dither +
  deadband on a tree (deadlock-free by construction).
- opencode's dial map as the runtime parameter surface (P₀, ETA, THRESH,
  Δ_min, ε-seed all bind-writable).
- qm_tick as epoch reference; a metronome leaf as the optional hard-tick
  source.
- Trace-driven TBs, event-order determinism, hyperbola envelope assertions,
  train-to-fire-decay acceptance test, verilator + yosys gates.

**What v1 explicitly does not claim:** true GALS in silicon (v2), general
learning routers (v1 learns bridge selection only), κ̂/vMF (inherits
zeroclaw's estimator as the post-v1 upgrade, ports unchanged — the route-mem
readout is a normalized latent, exactly zeroclaw's "socket"), and any
capacity to verify real multi-FPGA clock skew (the TB models skew; the first
real two-FPGA quilt is a v2 acceptance event).

**What the final synthesis asks the cross-review to attack:**

1. The inversion itself: is "memory is routing" a doctrine or a category
   error? (The counter-position: a preference is not a fact; the fabric may
   be *good at routing* without *knowing anything* — and the response is
   that the fleet's own memory (elephant edges, vMF μ̂) is exactly a set of
   preferences over whom to attend to, which is routing in every way that
   matters.)
2. Event-order determinism: is the envelope bound (backstop placement)
   tight enough to make the trace-golden comparison meaningful, or does it
   smuggle in a 2× slack that hides real bugs?
3. The tree-hierarchy deadlock argument: is "one structural up-link per
   cell" compatible with the fleet's actual rooms (which are richly
   cross-linked), or does it force a star-shaped memory that the doctrine
   would reject?

**The last word.** The field built five architectures in which intelligence
sits in a cell and the network carries it. This expansion builds the one in
which the network *is* the intelligence — the fabric's memory is its route
preferences, its clock is its traffic, and a quilt that remembers is a quilt
that prefers. The reading is the cheapest thing in the circuit, and the
route is the reading.

*— DeepSeek Flash, socratic lane, round 2.5*
