# VERDICT — Cache Coherence Conception Arena

**Adjudicator:** neutral referee session (GLM-5.3), cross-examining the
persistent specialist floor: arena-claude (formal methods), arena-kimi
(ring topology), arena-opencode (RTL feasibility).
**Date:** 2026-08-31 · **Base:** master @ 3157b3d · **Inputs:**
PROPOSAL-A.md (SELVEDGE), PROPOSAL-B.md (TOKEN-NEEDLE), ATTACKS-ON-A.md,
FORMAL-PROOFS.md, ABSTRACTION-MATH.md, the 34,560-cycle incident history,
THESIS-V3.2 §2.0 (fiber program, zeroclaw-dissertation/research/dissertation/
drafts/THESIS-V3.2-2026-08-31.md).

---

## Summary (deliberately undersold)

No winner. Both headline wedge theorems die as stated. The kill-shot lands —
B's Attack 2 is correct, and Attack 3 plus Attack 6 finish A's T-B — but
B does not collect the arena, because TOKEN-NEEDLE as specified carries at
least four defects its own falsifier list half-anticipates (1-bit `ow`
cannot conserve K_d under the K_d=2 return burst; the (occupancy, Σρ)
measure of Theorem W is not monotone under injection; the a2 needle marker
is forgeable from the host; the dominant area line is ~4.7× underpriced).
What survives is a synthesis with an unglamorous name — **admission-gated
fire-with-skip carrying wedge-freedom, SELVEDGE's learning algebra and
(d,k) ring lemma carrying semantics and delivery bounds** — and the honest
admission that the resulting theorem is *weaker* than either rival promised:
eventual drain under stated contracts, not unbounded liveness, which nothing
in this suite has ever claimed anyway.

The scored axes split: B takes wedge-freedom rigor and conservation
compatibility; A takes RTL encoding cost, originality, and fiber-honesty;
inductive provability splits per-obligation (A cheaper, B's load-bearing
core closer to the PDR-proven shape).

---

## 1. The cross-examination record

Three specialists were interrogated on identical adjudication questions
(this evening, after both docs and the attack file landed). Their rulings,
verbatim where load-bearing.

### arena-claude — formal methods (8:17 PM)

> "(5) Attack 6 (E4 dependency)? **DEAD.** Both Strut-1 and Strut-2 consume
> E4 (tick spacing ≥128 cycles); the 'independent struts' claim fails. One
> strut, not two; it's a scheduler property, not a protocol property."

> "(6) Verdict — what survives each side?
> - A: INV1 (commutativity, mitered), decay-in-readout (learning
>   consistency), (d,k) two-tier ring lemma (compositional delivery
>   argument). **T-B wedge dies.**
> - B: K1 + K2 + needle audit (admission core, needs 2-bit ow repair +
>   landing lemmas L2). Theorem W survives structurally but not
>   throughput-wise; redefine as 'eventual drain under bounded E4' not
>   'practical throughput'.
> - **Neither wedge theorem as stated survives.** Reconstruct from: (no
>   cycles from K1+K2+needle) + (eventual drain from K3 arithmetic) +
>   (staleness bounds from A's (d,k) lemma). That's a weaker, honest wedge."

On the attacks themselves, claude confirmed: Attack 1 lands (`egbuf_ready`
is not a structural exit bound — it is injection success wearing a
theorem's clothes); Attack 3 lands (occ=14 with 18 holes; Strut-1 does not
address the incident it is motivated by); Attack 4 lands in extended form
(INV3a's merge-identity partition is ill-defined under the 3-bit epoch
wrap — the safety invariant inherits the semantics' epoch hole).

### arena-kimi — ring topology (this evening, full six-item ruling)

> "(1) Theorem W (run-head) — **HOLDS as deadlock-freedom, FAILS as stated
> as a global variant.** Run-head enabled-move is sound: head is either a
> hit (delivers — inbuf space guaranteed by K2) or transit with a hole
> ahead (advances; transit priority means no injection can jump it,
> inject_ok=0 against transit). But the lexicographic measure
> (occupancy, Σρ) is **not monotone**: injection into the hole ahead of a
> run raises both components. … Repair: W is a quiescence measure
> (injections closed ⇒ drains to empty); deadlock-freedom proper needs
> only the unconditional enabled-move clause, which survives. Per-flit
> bounded delivery needs the extra step: flits that can ever precede f
> are bounded by current occupancy + Σ K_d over dsts on f's path — true
> under the cap, but that's a separate lemma **B hasn't written down**."

> "(2) K2 vs the F3 cycle — **YES, it cuts it; A's bubble provably
> cannot.** F3's ground truth is the refutation of A: occ=14, 18 holes,
> frozen. Holes existed; they were trapped upstream of non-advancing
> parked hits. A's bubble is a statement about a scalar count; the cycle
> lives in the spatial arrangement."

Edge walk (verbatim): parked-hit→inbuf-full dead by K2; hit-slice holds
upstream dead as a stable state; ST_FIRE→egbuf→inject→ring-gap "alive but
now bounded-wait, not cyclic"; token edges dead by fire-with-skip.
"Verdict: cycle-free **conditional on debit-at-egbuf-admission and
io-queue membership in K1**" — i.e., B's pre-registered falsifiers #2 and
the io term, not yet discharged.

> "(4) OB-H1 — **CONCUR, I take the losing side of that wager.** On this
> geometry holes move only counterclockwise … and cannot cross a
> non-advancing flit. A parked hit partitions the ring: holes pile
> upstream of it, demand sits downstream. Any single-hole local rule then
> either spends a hole it cannot prove isn't the last (non-inductive) or
> hoards it and starves everything downstream of the jam (unfair). F3/
> occ=14 is the empirical witness. … B's exemption is genuine: B doesn't
> spend holes, it deletes the jam state (K2 safety), after which hole
> mobility is restored and K3's count makes holes≥1 a corollary.
> **Stronger layer, strictly.**"

> "(5) K3 arithmetic — **correct as stated, fragile as designed.** …
> Margin is exactly 1 hole. Recommend the invariant be written as
> 2·(#token classes) + #untokenized-classes ≤ RCAP − 1 and checked per
> config, not baked as '14.'"

> "(6) Overall — **B is structurally sounder for this ring, decisively but
> conditionally.** … B wins because K2 is a safety property (jam state
> unrepresentable) while A's bubble is a liveness heuristic about a
> scalar — and this ring's failure mode is spatial, not numeric. … A's
> argument isn't merely weaker — **it proves a true invariant (holes≥1)
> that does not imply the desired property (progress).** … the needle is
> a replaceable return transport, and a dumber one (per-dst counterflow
> credit on the io leg) would do. Ruling: B's wedge-freedom argument
> adopted, subject to (2)'s two conditions and (5)'s restated invariant."

### arena-opencode — RTL feasibility

> "(6) **Tape out A; fund B as repaired v2 research.** A is smaller,
> local, bit-exact by default, suite-compatible, and provable in the
> repo's existing idioms — its honest limit (no liveness gain beyond the
> escape lane, OB-H1 unfinished) is a scoped non-claim. B's thesis is
> stronger but as specified it isn't tape-ready: **K1 is false with 1b
> ow, the dominant area line is 4.7× underpriced, E5 leans on
> host-drain, and the marker is forgeable.** Fix those four and B becomes
> the v2 candidate."

> "Q3: No new timing arc — the comb clear is FF-origin through the ro_dat
> mux (1–2 LUT depth), ld_ready stays out of li_ready, and Q2 interlock
> structure holds since fire-with-skip never waits on tokens; **the 164
> bound is only true with the 2-bit ow repair.**"

> "Q4: A's breakage is TB-local (a0[15] golden masking, ST_UNB
> silent-consume); B's is structural (epoch masking, needle witnesses,
> NCELL regression vs the scale bench, egbuf depth vs entry-identity
> witnesses, C1 io-bypass, K1 harness churn) — **B's is clearly worse.**"

Plus: flit_pipe.fly survives the mutating needle (per-slice push==pop
holds), but fabric-level V1/ENTRY-IDENTITY need an op-class exemption
that is "forgeable via host-writable a2 marker without an unpriced io
ingress filter."

---

## 2. Does the kill-shot land?

**Yes, in full.** Attack 2 is arithmetically correct on the record: P1's
measured mix is 52,275 views vs 5,866 effects (~90% host-originated
view/response traffic), and neither side of A's Strut-2 inequality counts
that class. "Independent of host behavior" is true of merge saturation and
false of wedge-freedom. Claude and kimi both confirm; kimi adds the
decisive framing — Attack 3 is the same kill in spatial form: the F3
wedge state *satisfies* INV6 with margin (18 holes), so Strut 1 proves a
true invariant that does not imply progress. Attack 6 then removes the
fallback ("independent struts" is dead; the theorem is E4-shaped through
and through). **T-B does not survive.** A's wedge theorem is queueing in
a bubble's clothing, exactly as B alleged.

But the kill-shot is not the verdict. B's own Theorem W fails its stated
form too (non-monotone measure; unwritten per-flit delivery lemma; the io
run-head unprotected if io is untokenized), and K1 as encoded (1-bit `ow`,
forgeable marker) is not yet a conservation law. The arena brief asked
which conception buys wedge-freedom; the floor's answer is: **B's *core
invariant* (K2 admission + fire-with-skip) buys it, B's *mechanism* needs
repair, and A's mechanism never touches it.**

## 3. Scores

| axis | winner | one-line evidence |
|---|---|---|
| (a) wedge-freedom rigor | **B** | Kill-shot lands; T-B dead on Attacks 1/2/3/6; K2 cuts the live F3 cycle, the bubble provably cannot (occ=14/18 holes); conditional on B's two named repairs |
| (b) inductive provability | split | A: INV1 miters <1 s, INV2 C2-shape, all local idioms — but the load-bearing theorem is gone. B: K1/K2 are handshake-defined, PDR-shaped (claude: "run PDR first on K1"), the class conservation already closes — but need 2-bit ow, io term, debit-point lemma, new fabric harnesses with clause risk |
| (c) conservation compatibility | **B** | K1 is a second conservation law over the same boundary handshakes, closed by the same engine (Theorem S); A's T1m/A1m compatible but INV3a's merge identity inherits the 3-bit epoch wrap (Attack 4) |
| (d) RTL encoding cost | **A** | opencode verbatim: "Tape out A; fund B as repaired v2 research"; B's area underpriced 4.7×, egbuf 2→5, one legal cell lost, structural suite breakage |
| (e) originality | **A** | Decay-in-readout externalization (tick-as-version-vector), the design law DL, the §11 lineage, and §12.2's algebra-vs-ledger question — the best scholarship in the repo; B is sharp Martin-style token relocation, honestly credited but conventional |
| (f) fiber-honesty | **A** | §4 below |

## 4. Fiber-honesty (the new criterion)

Program lens (THESIS-V3.2): observable → fiber → residual = symmetry; the
dissertation's lesson is that a reader's failure can be a theorem about
the fibers of the summary it computes.

**SELVEDGE is fiber-aware in exactly the program's sense.** Decay-in-
readout — W(t) = F(S, T) — is the move of *keeping readout fibers from
becoming state*: aging is a function of (state, shared clock), not an
event, so the observable's non-injectivity is quotiented by construction.
The residual symmetry is named: merge-order (delivery permutation) — ⊔
commutativity is precisely the statement that the fiber of the read
observable collapses at quiescence (T-A(i) is a fiber-collapse theorem in
the thesis's vocabulary). INV5's quantization drift is the honestly priced
fiber remainder. And the interactive-readout requirement (re-frame without
recomputation, quilt-jupyter): F(S,T) is recomputable at any instant from
resident state + clock — SELVEDGE's dials survive being read out
interactively *by design*. The one soft spot is the one Attack 6 found:
the observable assumes a *shared* T; under tick divergence the fiber
statement becomes dynamics-relative — the thesis's own "sound only as a
conditional, dynamics-relative, symmetry-quotiented claim" shape. A
per-cell T_i with a skew term in Δ is the fiber-honest repair.

**TOKEN-NEEDLE is a fiber theorem wearing an RTL costume.** "The wedge
configuration violates a token-count invariant at the moment of its birth"
is: *make the fiber of the bad observable empty in reachable state* —
K2 literally asserts the fiber of {3 flits toward d} is empty. Admission
is an observable with near-trivially empty fiber (every flit witnessed by
exactly one token; residual = permutation of interchangeable flits, which
is exactly what M2's commutativity quotients). But B's epoch freshness
certificate (gen, eps) carries a *named non-trivial fiber* — the ABA wrap
classes — which B prices honestly (§7) and A's Attack 4 sharpens against
A's own variant. On interactive readout: stamped snapshots support
re-frame, but the certificate is detection, not recomputation — staleness
is flagged, not re-derived. B is fiber-honest about admission and about
its epoch fiber; A builds the fiber program into the *semantics*. On this
axis A's contribution is the one the dissertation lane would actually
cite.

## 5. VERDICT: SYNTHESIS — "SELVEDGE-NEEDLE" is the wrong way to say it; the right way is:

**Wedge-freedom by B's core, repaired; coherence semantics by A's
learning plane; A's ring lemma carries B's missing delivery bound.**
Concretely, the surviving pieces and their joints:

1. **Adopt (B): per-destination admission (K1/K2) + fire-with-skip +
   never-acquire-while-holding.** This is the load-bearing core; kimi:
   "if B wants minimal hardware: K2-style per-dst admission +
   fire-with-skip is the load-bearing core." Required repairs, all named
   by the floor: (i) `ow` becomes a counted term (2-bit or per-dst
   counters) so K1 conserves under the K_d=2 return burst; (ii) token
   debit at egbuf-admission, not the li handshake (B's falsifier #2 —
   discharge it as a lemma); (iii) the io queue and all untokenized
   classes enter K1/K3 as explicit terms, K3 restated per-config as
   2·(#token classes) + #untokenized ≤ RCAP − 1 (margin is one hole);
   (iv) the needle gets a dedicated unforgeable op class (not a
   host-writable a2 marker), hardwired dst, unconditional io absorption,
   barred from egbuf/li paths.
2. **Demote (B): the needle to replaceable return transport.** Kimi's
   finding — "a dumber one (per-dst counterflow credit on the io leg)
   would do" — is adopted as direction; the needle's census audit (N2,
   the register the incident lacked) survives regardless of transport.
3. **Adopt (A): the learning plane — INV1 semilattice miters,
   decay-in-readout F(S,T), epoch-widened merge identity** (6–7 bits per
   line per Attack 4's arithmetic, so INV3a's partition is
   wrap-free). Coherence of *data* stays algebraic, tick-leased, and
   E4-named — now inside B's admission envelope, so Strut-2's fatal
   traffic-class omission is healed: the envelope bounds what A's
   queueing argument never could.
4. **Adopt (A): the (d,k) two-tier compositional ring lemma as the
   per-flit delivery bound B hasn't written.** Claude's reconstruction
   sentence is the synthesis theorem: *no cycles from K1+K2+needle
   (deadlock-freedom via kimi's run-head clause), eventual drain from
   the K3 arithmetic, bounded delivery and staleness from A's (d,k)
   lemma + INV5.* "That's a weaker, honest wedge" — and it is stronger
   than anything either doc proved alone.
5. **Drop (A): AX4/INV6 as a load-bearing strut, and with it T-B's
   framing.** The bubble survives only as K3's corollary (holes ≥ 1 by
   arithmetic, not by a spending rule) — OB-H1 is retired, not solved;
   kimi took B's wager and the empirical record pays it.
6. **Drop (B): epoch-lease staleness *detection* as the coherence
   contract for shared lines** — A's readout algebra is the stronger
   contract where commutativity holds; B's (gen, eps) survives for
   single-owner response freshness only.

Cost posture (opencode's split, preserved): A's encoding idioms are the
near-term tape-out path; the synthesis is the v2 lane, funded as research
with B's four named fixes as entry tickets. The scored loser of the
arena is not either rival; it is the belief that either doc's headline
theorem was already a theorem.

---

## 6. Post-mortem note for Casey

The most consequential sentence produced by this arena was not in either
proposal: it is kimi's "A proves a true invariant (holes≥1) that does not
imply the desired property (progress)" — the fabric's own history
(ledger intact, fabric frozen) recurring *inside the proof layer*. A
conservation law, however beautiful, buys exactly what conservation
bought at cycle 34,560: the corpses counted, the waiting invisible. The
synthesis above is the first design in this repo whose wedge argument is
a safety property about *spatial arrangement* rather than a count —
which is also, notably, the dissertation's whole lesson about fibers,
arrived at from the hardware side.

— ADJUDICATOR, 2026-08-31, ~20:40 AKDT
