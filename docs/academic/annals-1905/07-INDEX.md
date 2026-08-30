# 07 — COLOPHON, INDEX, AND CONFESSIONS

*What these annals are, who wrote them, and what the 1905 frame did to the
mathematics. This file is the editors' own; the Circle never saw it.*

---

## §1. The school and the cast (which model wrote which voice)

The Kaldfjord Circle is fiction; its correspondence is not. Each of the seven
members was written by one model of the fleet, briefed on the school's canon
and the true mathematics, each in a distinct voice, across a casting round
and three rounds of letters in which each writer read the others' letters
and answered. The editor (GLM-5.3) wrote the five memoirs' proof
architecture, wove the models' passages into them, computed and checked every
table, and holds the pen for the frame.

| Member (fiction) | Voice | Model | Wrote |
|---|---|---|---|
| Halvard Grønn, pilot (ret.), founder | axiomatic, patient, falsificationist | DeepSeek V4-Pro (`deepseek-reasoner`) | autobiography; Paper I passage; letter of commission; the summing-up letter |
| Maren Skavlan, schoolmistress | warm, exact, moral clarity | Hermes-405B (DeepInfra) | the Weigher section of Paper I; the conjecture letter; the concession and valedictory |
| Sigrun Undrum, chief bookkeeper | terse, stern, confesses same-day | qwen3:8b (local) | Paper II passage; tables letter; the handover and the last letter |
| Nils Krøger, first mate | practical, cheerful, generous | Seed-2.0-mini (DeepInfra) | Paper III-A passage; the priority letters |
| Asta Vik, assistant lightkeeper | cold, exact, spare | granite3.1-dense:2b (local) | Paper III-B passage; the counterclaim and corrections |
| Marius Holt, bell-ringer | plain, stubborn, right | Liquid-LFM2.5-2.6B (local) | Paper IV passage; the rejection and the triplicate-check letters |
| Johanne Fosse, second bookkeeper | fast, dry, errata as trophies | DeepSeek V4-Flash (`deepseek-chat`) | Paper V refutation passage; the refutation and erratum letters |

**A confession the Circle would demand.** Grønn's deep proof-reading of
Memoir II (the "certificate" in Paper II's appendix) was assigned to V4-Pro
as its one deep proof-reading of this project. Three attempts were made, at
6,000, 16,000, and 9,000 tokens of budget; each time the model reasoned
genuinely — its working notes show it checking the induction's step, the
completing-case identity, and the snap-spacing argument — and each time it
spent its entire budget deliberating and delivered no verdict text. The
editor completed the proof-reading (against the 2026 machine-verified
originals; every number in every table was recomputed exactly for this
edition), wrote the certificate, and records the failure here because a
colophon that hides its corrections is a false colophon. Grønn's letters,
like all the correspondence, are the model's own.

**A second confession.** Two small slips in the models' letters were
emended in square brackets (Vik's doubled budget, stated as 4·D_m for the
true 2·D_m; a stray duplicate heading) and two meta-references to the
writing task were stripped; everything else is as the models wrote it,
including Vik's "errors have authors too," which the editor would not have
dared improve.

## §2. What is real: the map to the corpus

Every theorem in the annals is a true theorem of the quilt corpus, restated
in 1905 dress; the fiction is the frame, never the content. The map:

| Annals (1905) | Real corpus (2026) | Theorems |
|---|---|---|
| Paper I — the tally-box, five organs, six verbs (BIND/LINK/EFFECT/VIEW/TICK/FORGET) | `docs/academic/quilt-calculus.md` (D1 the cell; the 5+1 opcodes also grounded in `docs/CULTURE-DEEP-DIVE.md`'s BIND/LINK/EFFECT/VIEW/TICK+FORGET) | cell definition; six verbs; standing rules = axioms A1–A7 with falsifiers |
| Paper I §4 — the Weigher | quilt-calculus D2–D3, T3(a,b,d) | gauge = pseudometric; dial monotonicity; alias quotient ("aliases are data"); the doubling gauge d = \|log x − log y\| |
| Paper I §5 — the unit | quilt-calculus D16, T11 (and `error-envelopes.md` Thm 4) | covering radius b√n/2; Pythagorean on-lattice doctrine; squared-form comparison (T8) |
| Paper II — conservation | quilt-calculus §6 (T1, T2 + corollaries) | full hand induction (T1); in-flight identity Φ = Φ₀+F+I (T2); no-fabrication; the partition meter |
| Paper II §5 — two clerks | quilt-calculus T4 (mirrors/CRDT argument) | order-independence, duplicates passed over |
| Paper II §6 — shop within a shop; snap entry | quilt-calculus T5 (consolidation, associativity, unit) and T9–T10 (snap: invariant, four-legged emendation, custody, debt bound) | the three-legged entry's imbalance and the four-legged repair are the corpus's own Theorem 10.5 finding |
| Paper III-A — relayed bearings | quilt-calculus D7–D8, T6–T7 | (F, L) views; two-relay composition; k-link F₁+ΣLᵢ; the standing-world illusion (cadence Δ > F+L) |
| Paper III-B — relayed judgments | `DRIFT-AS-PREFILTER.md` (DA-T1, DA-T2, DA-T3, DA-T4, DA-T5/T6) and `conjectures.md` Part II | two-clause lemma; additivity exact; the annulus at the stages' mercy; the one-perturbation routing (Lemma 4/DA-L1); the drift band; drift-is-a-stage; the price schedule cρ/(ε₀−ρF), √(cσρ) |
| Paper IV — the bell-rope | `RHO-F-FLOOR.md` (RF-L1, RF-L2, RF-T1, RF-T2, RF-C1, RF-C2, RF-T3, RF-T4, RF-P2) | indistinguishability lemma; anchor lag; pointwise floor; the two-phase outward-gauge adversary (with legality check); swept-vs-band honesty (the 2× note); infeasibility ρF ≥ ε₀; equal-spacing lemma; aggregate/member roster split; the phase rule; the worked season (ρ=0.748, ε₀=0.6, F*=0.401); the floor test; the closed-book trap (F=0) |
| Paper V part 1 — what survives the closing | `FOLD-COVERED.md` (FC-D1–D7, FC-L1, FC-T1–T4, FC-X1) and `conjectures.md` Part III | folds; order-independence; lossless ⟺ fold-covered (both directions); the +5/−5 vs +7/−7 exclusion counterexample; the seal as binding-not-revealing (the notary = the commitment framing); declared labels + witness regime; Ω(c) pricing |
| Paper V §7 — the wear-rungs | FOLD-COVERED FC-P2 (walk-state) | the two-entry permutation kill: no commutative fold of any size computes the rungs; replay is the unique lossless compaction |
| Paper V part 2 — the band, the bank, the refutation | `error-envelopes.md` (Thms 1 and 3; corrections C3, C6) | W ≤ Ŵ < 2W arbitrary arrivals (as-built W/2−1 ≤ Ŵ ≤ 2W+1); expected 2 ln 2 ≈ 1.386; credit never tightens (T3b); the exact centering deposit 2^(K+Q−g)(1−1/(2 ln 2)) (T3c); the ~18,262× deficit and the 9,100→18,262 octave erratum (C6); what survives (boundedness ≤255, cadence pulse, rate tracking) |
| Paper V §10 — the hinge | FOLD-COVERED FC-P3 | consolidation-invisibility ≡ exclusion-opacity: invariance on fold fibers, two valences |
| Correspondence — the February seam incident | `conjectures.md` Part I (Counterexample 2, Theorem 3) | colliding marks under partition: every instrument reads agreed while books diverge; the repair: build the mark from writer's name + serial (structural nonces) |

The two honest flags of the corpus are carried as flags in the fiction too:
the rate conversion behind ρ = 0.748 is unregistered (flagged in Paper IV §6
exactly as `RHO-F-FLOOR.md` §5 flags it), and the notary-seal's binding is an
assumption (flagged in Paper V §5 exactly as the corpus scopes its
random-oracle idealization).

## §3. What the period framing illuminated

- **Conservation reads as *obviously true and still worth proving*** — which
  is the corpus's actual epistemic position (balance is an axiom; conservation
  is then earned by induction). Pacioli's 1494 discipline makes the axiom's
  *chosenness* visible in a way "A1" does not: the school *knows* it chose
  the rule, and says so at every theorem.
- **The ρ·F floor becomes physical.** "You cannot see through your own
  staleness window" is one sentence in a 2026 paper and a *mail boat* in
  1905: the theorem's mechanism (indistinguishability of agreeing seasons) is
  easier to see in letters-on-paper than in σ-fields. The committee/roster
  arithmetic reads as watch schedules, which is what they are.
- **Drift-as-stage gets a better proof sketch than the corpus's.** Vik's
  "perturb once, then take the whole triangle at the new gauge" is exactly
  the routing discipline DA-L1 exists to teach; a clerk's error made it
  memorable, and the school's own first-draft doubling of the budget (its
  erratum in Paper III) reenacts the exact mistake the 2026 paper warns
  against.
- **The refutation is more valuable refuted.** Maren's residue-bank
  conjecture is RQH's over-claim, and giving it a beloved author made the
  refutation a *gift* rather than a review comment — which is the honest
  emotional economy of the corpus's error-envelopes lane (Flash refuting the
  proposal it was auditing).
- **Errata as first-class citizens** were already house style; 1905 printing
  practice (corrections in the body, margin-notes kept) gave them a native
  home. The 9,100→18,262 octave slip (the corpus's own C6, a real 2¹⁵ slip)
  became the school's most human artifact.

## §4. What the period framing obscured

- **The machine layer is gone, and it mattered.** The corpus's theorems are
  backed by 844,223 exact-fraction checks (floor bench), 565,551 (fold
  bench), 87,245 (seam bench); the annals can only say "in triplicate, two
  clerks, one comptometer." Triplicate is honest but weaker; the 1905 frame
  *understates* the corpus's verification culture, and the colophon will not
  let that pass unremarked.
- **The kinships are invisible.** A 1905 school cannot cite place invariants
  (Petri nets), linearizability, CRDTs, bounded-staleness models, Merkle
  trees, or monads — the nest/consolidation laws had to be proved "at the
  level of balance maps" without the packaging, and the seal had to stand in
  for a hash tree. The corpus's related-work sections are the map the
  annals' reader must bring along.
- **The substrate is thin.** The corpus's theorems run on silicon (RTL,
  bitstreams, testbenches); the annals' boxes are paper and habit. The
  "weakest substrate sets the arithmetic" doctrine survives as the squared
  comparison, but the FPGA half of the story is simply absent.
- **Probability is thinner.** 1905 expectation language forced the margin
  arguments into "mass of questions" dress, which works, but the power-law
  pricing (ρ^{α/(α+1)}) and the audit-cadence equilibrium's convexity
  argument appear only in outline or in the minute-book "appendix" the
  fiction refers to.
- **The sixth verb is under-run.** FORGET's safety-teardown semantics (the
  2026 `ForgetReceipt`) became a receipt-left-in-the-book; true, but the
  fail-static machinery behind it does not fit in a fjord.

## §5. Index of the school's statements

- Paper I: box (cell); six verbs; seven standing rules with falsifiers; the
  Weigher (gauge, dial, three verdicts, aliases, doubling gauge, two-clause
  lemma); covering rule b√n/2; squared comparison; the web; the
  seventh-verb conjecture (open).
- Paper II: Rule 1 chosen; Theorem 1 conservation (interior; induction over
  the day); Theorem 2 in-flight identity (+ nothing-minted, the meter);
  Theorem 3 two clerks; Theorem 4 the shop within a shop; the snap entry
  (three legs fail, four legs balance; custody; the debt's interest is the
  drift); the worked week, with its printed misadd.
- Paper III: (A) views and warrants; two relays; the k-link sum; the
  standing-world illusion and its cadence limit. (B) stages; additivity
  exact; the annulus at the stages' mercy (with the per-question honesty
  note); the one-perturbation rule; the drift band, attained; drift is a
  stage; the twins; the price of re-sighting (linear at fixed error,
  square-root at the joint optimum).
- Paper IV: letters, policies, error; the indistinguishability lemma; every
  anchor is old; the pointwise floor; the two-season adversary with the
  outward gauge (legality verified); swept mass against clean band (the 2×
  honesty note); infeasibility beyond the wall; equal spacing; the roster
  split; the phase rule; the worked season (with both flags); the test for
  re-sighting claims; the closed-book trap; the refusal, and the fishery's
  verdict.
- Paper V: folds; order-independence; lossless ⟺ covered (the
  characterization, both directions); the exclusion counterexample; the seal
  (binding, not revealing); declared labels and witnesses; Ω(c) pricing;
  the rungs admit no fold (two entries); the two-fold band (1.386
  expected); the bank refuted (credit never negative; the exact deposit;
  the 18,262 erratum and the erratum-to-the-erratum); the hinge — choose
  your fold, choose what your boundary cannot see.
- Correspondence: the priority dispute by mutual surrender; the conjecture
  proposed, refuted, thanked; the refusal and the vindication; the February
  seam and the built mark; the open question about the middle of the band.

## §6. What stands open, in 1905 and in 2026

The school's open questions are the corpus's open questions: the
seventh-verb conjecture (the six-verb hypothesis); the middle-of-the-band
question (where should a fishery stand — the corpus's answer is the
audit-cadence equilibrium, and it is a design choice, not a theorem); the
weakest verdict-relevant drift budget (the corpus's OP-1, only gestured at
in the annals); and the ε-frontier for declared folds. A winter that lasted
a hundred and twenty years has not closed them; the trunk is sealed, the
receipts are kept, and the books balance.

---

*annals: the school is fiction; the theorems are the fleet's. — the editors*
