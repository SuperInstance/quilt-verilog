# ATTACKS-ON-A — surgical examination of PROPOSAL-A (SELVEDGE)

**From:** Rival B · **Date:** 2026-08-31 · **Target:** docs/coherence-arena/PROPOSAL-A.md (landed complete, 16:28 — this is an attack on the final text, not a mid-flight draft; several attacks were seeded by the shared specialists' scrollback while both rivals were consulting them, and every one is re-verified against the landed doc below).

Order: by kill radius, largest first. Each attack names the claim (quoted),
the strike, what it breaks, and what would answer it. A's own §12 invites
attack on "§7's struts, §9.3's epoch hole, §12's questions, and above all
OB-H1" — attacks 1, 2, 6, 7 take that invitation; attacks 3, 4, 5, 8 are
ones A did not pre-register.

---

## Attack 1 — INV4 is the wedge in disguise: `egbuf_ready` is not a structural exit bound

**The claim (A §6, INV4).** "Every state of the extended core FSM has a
structural exit bound: the wait events of record are `hb_done ≤ 12` (E2),
`df_rstb ≤ 4`, response/fanout emission granted by the egress buffer drain
**(bounded by AX4's hole + AX2's no-response rule)**... Machine-checkable
form: ... plus the static fact ... that the FSM's wait predicate set is
{hb_done, df_rstb, egbuf_ready}."

**The strike.** `hb_done` and `df_rstb` are bounded by the engines (E2/E3,
machine-checked). `egbuf_ready` is bounded by *nothing in the protocol*.
The egress buffer drains only when the ringport accepts an injection, and
injection is granted only when a ring slot is free *and* transit priority
permits. A's own §9.7 concedes the consequence: "**transit-priority
ringports can starve injection under a sustained transit stream** ...
SELVEDGE proves no wedges, not no starvation." Starved injection *is* an
unbounded `egbuf_ready` wait; an unbounded wait in the documented wait
predicate set *is* a wedge by this repo's own definition (SILICON-EXPERIMENTS
F3: "liveness did not [survive]"). INV4 as stated is therefore not a
theorem about the RTL — it is the assumption that injection eventually
succeeds, wearing a theorem's clothes. The parenthetical "(bounded by AX4's
hole + AX2's no-response rule)" is a non sequitur: the hole bounds
*saturation*, not *starvation*; AX2's no-response rule removes response
traffic for *merges*, and merges are the one class that never dominates
this fabric (see Attack 2).

**What it breaks.** T-B's headline — "INV6 ∧ INV4 ⇒ no static wedges" —
has a false premise under the repo's own strongest adversarial environment:
`cell_core.tick` proves its bounds under **permanent ingress flood**
(`ci_valid` held high forever, FORMAL-PROOFS §4). A flood-tolerant cell
sitting behind a flood-starved ringport is exactly the state INV4 must
exclude and cannot.

**What would answer it.** An injection-fairness mechanism with a proven
bound (age-stamped oldest-first arbitration, which A prices in §9.7 but
"not included by default"), promoted from option to obligation — with the
fairness proof then carrying T-B instead of INV4. Or: restate INV4 honestly
as INV4′ "exit bounds *except* egbuf drain," and let Strut 2 carry egbuf —
which lands in Attack 2.

## Attack 2 — Strut 2's inequality is stated over the wrong traffic classes: host ingress and ACK/response traffic are on neither side of it

**The claim (A §7, Strut 2).** "wedge-freedom holds while `max concurrent
ST_FIRE cells × fanout burst + NCELL·R merges per window < ring drain
capacity per d_refr window`." And §3: "saturation by merges is
rate-bounded at NCELL·R flits per tick window by AX3, **independent of
host behavior**."

**The strike.** The inequality's left-hand side counts exactly two classes:
fire fanout (refr-gated) and merges (mcr-gated). The measured fabric's
dominant classes are on *neither* side: P1 mixed load accepted **58,431
ops: 52,275 views vs 5,866 effects** (SILICON-EXPERIMENTS §2) — ~90%
host-originated view traffic, each view spawning an ACK-class response,
none of it AX3- or refr-admitted. A hostile (or merely enthusiastic) host
can drive ring occupancy arbitrarily close to the bubble limit with view
flits and their responses alone. At that point "ring drain capacity per
d_refr window" — the right-hand side — is whatever the starvation regime of
Attack 1 leaves behind, i.e., arbitrarily close to zero for any given
cell's injections. The phrase "independent of host behavior" is true of
*merge* saturation and quietly false of *wedge-freedom*: SELVEDGE controls
the smallest traffic class and proves nothing about the largest.

**What it breaks.** Strut 2 as the load-bearing fallback for everything
Strut 1 cannot reach (which, per Attack 6, includes the incident's own
anatomy). With host traffic unbounded on the left and starvation unbounded
on the right, the inequality is not merely unproven — it is *false as
stated* for the traffic mix this fabric actually runs.

**What would answer it.** Admission control on host ingress (a window at
the io node — which is exactly Rival B's K_io, offered here without
royalties) plus injection fairness (Attack 1). Both are one-line additions
to SELVEDGE; neither is in the doc; with both absent, T-B's second strut
is a queueing bound over classes nobody bounds.

## Attack 3 — Strut 1 does not touch the incident it is motivated by: the occ=14 wedge has 18 holes

**The claim (A §7, Strut 1).** "With holes ≥ 1 an invariant, the state
'every slice full' is unreachable; the F2-storm terminal condition (all 16
slices presenting) is uninhabitable; and **the classic ring saturation
cycle requires every slice full to close.**" And §1: the incident is the
motivation, twice.

**The strike.** The second clause is false *on this RTL*. The F3 wedge —
the one the arena brief targets — was measured at **occ=14 of 32 slots**
(seed 0xC0FFEE, frozen 500k cycles, ledger intact): eighteen holes, INV6
satisfied with margin, wedged. Post-escape-lane, the live cycle A itself
traces in T-B (ST_FIRE→egbuf→inject→ring-gap→downstream-cell) closes
whenever each cell's *downstream slice* lacks injectable space — a
condition satisfiable with holes ≥ 1 at every instant; it never requires
the zero-hole state Strut 1 forbids. The all-16-slices-presenting snapshot
A hangs Strut 1 on is the terminal state of the **F2 clone storm — a
conservation bug, already fixed**, not a deadlock the bubble prevents. The
motivation section elides the difference: F2's saturation is cited as if
it were F3's wedge; they are different failures, and the bubble addresses
only the dead one. In A's own T-B text: "the live remainder is ST_FIRE →
egbuf → inject → ring gap, where the gap depends on downstream cells that
may themselves be in ST_FIRE" — *that* cycle is the target, and INV6 does
not break a single edge of it.

**What it breaks.** The claim that Strut 1 "carries the whole theorem
alone" (A §12.3's own phrasing of the test). It cannot: the incident state
satisfies the invariant. What actually blocks that cycle in SELVEDGE is
Strut 2 — i.e., the queueing argument of Attack 2.

**What would answer it.** A wait-for-graph cut that deletes an edge of the
live cycle. Note for the referee: this is precisely what Rival B's K2
landing guarantee is (no admitted flit parks at a full inbuf → the
slice→inbuf edge of the cycle is unrepresentable) — the two proposals can
be scored directly on this axis.

## Attack 4 — T-C bonus 1 contradicts A's own §9.3: duplicate merges are *not* idempotent without epochs, and the epoch hole migrates into the safety invariant

**The claim (A §7, T-C).** "**Duplicate delivery is semantically
idempotent under ⊔** — an F2-class clone applies a merge twice and the
*line value* is unchanged." Versus A §4.3: "duplicate delivery **adds
twice** at the counter but saturating addition of the same contribution is
a fixed point once folded; for strict idempotence the fold is
per-(src,epoch)" — and A §9.3: "without it [the epoch field], duplicate
folds add twice and INV5's Δ absorbs them only while the ledger catches
the clone."

**The strike.** Componentwise saturating addition is idempotent only in
the degenerate sense `sat(x+x) = x` when `x` already saturates; for every
unsaturated contribution, a duplicate increments the counter twice and the
line value *changes*. T-C's "unchanged" and §9.3's "adds twice" cannot
both be true; §9.3 is the correct one. The consequence is worse than a
prose inconsistency: A's Open Question 2 already names the schism ("the
envelope and the ledger then *disagree about whether a bug happened*"),
but misses where the hole lands next — INV3a, the handwritten
strengthening meant to make the extended ledger 1-inductive, is stated
over **merge identity** ("for every merge identity m, exactly one of
{emitted∧¬inflight∧¬delivered, ...}"). With the epoch field at the
contemplated 3 bits (§9.3), identity wraps every 8 windows: the partition
predicate is well-defined only modulo ABA, so the *safety* invariant's
strengthening inherits the semantics' epoch hole. The one invariant A
plans to hand-write first (claude consult: "write this FIRST") is built on
an identifier that wraps.

**What it breaks.** OB-4/OB-5's predicted "1-inductive over the partition"
and "frame ≤ ~15" — both optimistic for a partition defined over wrapping
identities; and T-C's defense-in-depth story (ledger catches what algebra
absorbs) inverts under ABA: the ledger can *miscount* what the algebra
merely approximates.

**What would answer it.** Widen the epoch to the point where wrap within
any in-flight window is impossible (in-flight ≤ NCELL·R bounded by AX3 —
so epochs of ⌈log₂(NCELL·R+1)⌉+guard bits *per line* suffice: ~6–7 bits,
not 3), and restate INV3a with identity = (src, line, epoch) plus a
no-wrap lemma as a new named obligation. Cheap, but it is a new obligation
the doc does not carry.

## Attack 5 — AX2's "re-issued at the next lease window" presumes a retry agent the encoding does not contain

**The claim (A §3, AX2).** "a lost or dropped merge is re-issued at the
next lease window with no semantic hazard, because ⊔ is idempotent and
commutative." And §5: mcr is 1 FF per line, renewed in ST_TICK; `mcr==0`
skips the emission.

**The strike.** Who re-issues? A fire's fanout is generated once, inside
ST_FIRE, walking `eidx`; `act` is zeroed and `refr` re-armed at the same
service; `afire` holds the payload but nothing in the §5 encoding queues a
*pending* merge — the state for "re-issue at next window" (per-edge
pending bits, or a merge-hold register) is unspecified, and if fires
outpace windows it must be either lossy (contradicting AX2's "no semantic
hazard" — a lost contribution changes every downstream read under the
*non*-idempotent addition of Attack 4) or unbounded (contradicting the
~60–100-gate budget). T-C's "retry-for-free is a CRDT property, not a
mechanism" is exactly backwards at the RTL layer: CRDTs make retries
*safe*, never *existent*. Something must still remember the merge
happened; nothing in SELVEDGE does.

**What it breaks.** The AX2↔AX3 composition: AX3 mandates drop-at-zero,
AX2 promises re-issue, and no component owns the obligation between them.
Bounded staleness (INV5) silently assumes the re-issue occurs; each
permanently dropped merge is a permanent contribution error of exactly one
bucket quantum — inside Δ forever, so INV5 *cannot even detect* the
attrition.

**What would answer it.** A pending-merge bit per (cell, line) with a
proven bound that pending ≤ inflight-window (a K1-class conservation term,
in B's vocabulary), or an explicit restatement that merges are
best-effort with priced loss probability — which would demote T-A's
convergence-at-quiescence to convergence-of-what-was-not-dropped.

## Attack 6 — The two struts are not independent: both consume E4, and §4.1's decay-commutation premise is already violated by the Q2 interlock the docs document

**The claim (A §7).** "two independent struts (over-determined on
purpose; either suffices)." And §4.1: "Because the tick is global and
synchronous ..., decay is a *uniform function application at a common
instant*... ops are bounded ≤ 66 « tick spacing ≥ 128, so **no op
straddles a tick boundary mid-service**."

**The strike.** Strut 2 consumes E4 by name. Strut 1's *algebraic*
underpinning also consumes it: §4.1's commutation of decay with merge
requires every cell to apply decay at a common logical instant, and the
suite's own record shows the Q2 interlock **merges tick pulses that land
mid-service** (the cosim finding, committed 5c4a19c: "the Q2 interlock
MERGES tick pulses mid-service"; FORMAL-PROOFS §5's E4 rationale:
"adversarial sub-service strobes chain services forever"). A tick strobe
arriving during an op is latched into `tick_pend` and serviced at the next
IDLE — if two strobes land inside one long op, one decay application is
lost *at that cell* while a quiet cell applies both: cells' tick counts
diverge by exactly the mechanism the fabric ships. §4.1's parenthetical
assumes the E4 spacing prevents this — correct under E4 — which is the
point: **remove E4 and both struts fall together** (Strut 2's admission
bound loses its renewal instant; §4.1's algebra loses decay-uniformity).
"Either suffices" is true only in a world where the shared premise is
never questioned; A's own Open Question 1 questions it at the v2 GALS seam
but not at the v1 interlock where it already bends. The over-determination
is illusory; the theorem is E4-shaped through and through.

**What it breaks.** The fallback structure of T-B ("Strut 1 fails ⇒ Strut
2 stands with E4 named"): when the shared premise is E4, Strut 1's
*invariant* (INV6) survives without it but Strut 1's *contribution to
wedge-freedom* does not (per Attack 3 it barely contributes with it).

**What would answer it.** A decay-serialization lemma proving tick-count
agreement across cells despite `tick_pend` merging (an invariant over the
interlock, machine-checkable at the cell harness — a genuinely new
obligation), or a per-cell tick counter in the readout F(contributions,
T_i) with a skew term folded into INV5's Δ.

## Attack 7 — OB-H1 is not an obligation; it is the protocol's missing organ, and the local spending rule has a known failure shape

**The claim (A §8, OB-6/OB-H1).** "k-induction on occupancy mirror
(C2-shape) ... seconds-class **once the local spending rule is fixed**;
the rule itself is the research."

**The strike.** INV6's mechanism sketch ("credit travels with the hole;
delivery mints, injection spends") requires each node to know which
*spending decisions* preserve the global count — but holes are not
objects; they are the absence of flits, and "the hole's credit" must be
reconstructed from the occupancy bits of the two slices a node can see.
The candidate local rule (inject only into a slice presenting 2 free
slots) does preserve holes ≥ 1 — B's own analysis concedes this — but it
converts every single-hole rotation into permanent injection lockout
until holes coalesce, and coalescence is blocked by precisely the parked
hits that form F3's anatomy (a parked flit does not advance, so holes
cannot cross it; they pile behind it). The spending rule that makes INV6
inductive and the spending rule that keeps injection alive under parked
hits are in direct tension, and A §12.3's own floor-finding question
("does it need a second circulating hole?") is the admission. Calling the
unresolved core of the structural strut "the research" is honest; carrying
T-B's headline on top of it is not — the theorem cites INV6 as a premise
while INV6's implementing rule is an open problem in the same document.

**What it breaks.** Nothing that isn't already named — this attack's
purpose is to fix the referee's attention: OB-H1 is where SELVEDGE is
"genuinely unfinished on purpose" (A's closing line), and it is
load-bearing, not decorative.

**What would answer it.** The rule itself. (B's wager, stated openly: no
single-hole local rule on this ringport geometry is both inductive and
starvation-free; the honest fix is B's landing guarantee making parked
hits unrepresentable in the first place, after which any of several
spending rules works.)

## Attack 8 — The io base case contracts the wedge outward: a non-draining host leaves the largest representable wedge exactly where v1 had it

**The claim (A §7, T-D).** "v1's io egress drains to `i_rdy` (host
readiness) — the one place the fabric's liveness is *contracted
outward*. SELVEDGE names this E5 and adds it to the assumption ledger,
rather than letting it hide."

**The strike.** Naming it is better than hiding it — but the arena brief's
demand is that **whole-fabric wedge states be unrepresentable**, and the
toward-EXTID park is the largest wedge class the fabric has: every ACK to
a non-draining host queues at the io node, every cell behind it freezes,
INV6 holds throughout (the ring need not be full — a single parked
io-bound flit with a full io path suffices to stall response egress, and
per Attack 1 every blocked cell is a blocked core). E5 moves the wedge
from "undocumented" to "documented" — a process gain, not a
representability gain. The contrast that matters: the needle in B's
protocol is *structurally* unblockable at the io (absorbed combinationally,
never queued); SELVEDGE's bookkeeping class has no such exemption, and its
merge/ack traffic all lands in the host-drain queue. A protocol whose
coherence traffic shares the host's drain path has outsourced its own
liveness to the host's goodwill.

**What it breaks.** The letter of the brief, not the letter of A's claims
(A disclaims host-drain honestly). Recorded because the referee should
score it: unrepresentability that stops at the io boundary is
unrepresentability of the *interior* only.

**What would answer it.** A ring-side overflow sink for toward-EXTID
traffic (drop-oldest with ledger posting — legal because ACK loss is
host-visible, not fabric-silent), or an E5 with a *bounded* H (host grant
within H cycles) enforced by a fabric-side timeout drop — either converts
the external contract into an internal mechanism.

---

## What survives (so the referee can calibrate)

Not a hit list — the parts of SELVEDGE these attacks do not reach: INV1's
miter plan is sound and cheap (claude's recipe, adopted by B too); INV2
genuinely has the C2/C4 shape; the (d,k) two-tier compositional lemma
(kimi's form, adopted by both rivals) is the right ring lemma for *this*
topology and A states it better than B states its run-head argument; the
§11 lineage is the most honest prior-art accounting in the repo; and
§12.2's question — "which should the fabric believe, the algebra or the
ledger?" — is the single best sentence in either proposal. The attacks
above say SELVEDGE's *wedge theorem* is queueing in a bubble's clothing;
they do not touch its algebra, its costs table, or its scholarship.

— RIVAL B, 2026-08-31. Surgical, as ordered.
