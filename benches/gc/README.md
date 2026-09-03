# benches/gc — the GC-C1..C4 conjecture falsifier lane

One assertion-level bench per open conjecture of
`docs/academic/GENERAL-CALCULUS.md` §7, built to hunt each conjecture's
**registered falsifier** (the artifact a hostile party executes to kill
it). Distinct from `tools/verifies/` (the §8 CLOSED-BOUNDED benches for
the *proved* statements, run by `tools/gc-verifies/run_gc.sh`): this
lane's benches are *falsifier searches* — each enumerates a bounded
candidate space where a kill would live, verifies the harness can see
preservation/generation where it exists (controls), and reports a
verdict.

Run everything:

```sh
bash benches/gc/run_benches.sh        # or: make test (wired into tb/run_suite.sh)
```

House rules kept: exact-integer arithmetic only (zero floats), bounds
stated per section in-file, FAIL/KILLED printed loudly never buried,
stdlib only, seconds per bench.

## Verdict semantics (all four benches)

| verdict | exit | meaning |
|---|---|---|
| `PASS` | 0 | every enumerated candidate resolved; no kill found at the stated bounds; the conjecture's grade is unchanged (open) |
| `KILLED` | 2 | the kill artifact fired: a candidate beat the harness at its own game (passed Q1–Q5 and resisted the macro search; preserved every burst source; quilt-shaped a span-less product; an in-class action not generated). Printed with everything needed to publish. The lane fails loudly — a kill is a publishable event, not a routine pass |
| `FAIL` | 1 | a harness control misfired (a known breaker slipped the gate, a known macro was missed, a ceiling failed to preserve). The harness is insensitive and its PASS would be vacuous |

## The benches

| bench | conjecture | search space (bounds) | what a kill would mean |
|---|---|---|---|
| `gc_c1_six_verb_bench.py` | **GC-C1** signature sufficiency (the six-verb hypothesis) | [A] dependency graph (25 edges, each with an executable witness) + coverage exhaustion over all 64 verb subsets; [B] six GC-T2 drop-witnesses (storms ≤ 12, depth ≤ 12, drift ≤ 6); [C] 13 candidate seventh verbs (the §6.4 historical temptings + macro families) through five computed Q1–Q5 checkers, then a six-verb macro search (sequences ≤ 3 over 7 argument-forms, extensional equality on the integer observable grid) | a seventh verb that keeps Q1–Q5 intact yet admits no six-verb macro: publish it with an invariant I every macro preserves while it breaks — that separation triple kills GC-C1 (a seventh primitive IS needed). A macro found for any candidate strengthens |
| `gc_c2_synchrony_bench.py` | **GC-C2** the synchrony separation (open half (b)) | [A] compact GC-T8 re-check (W ∈ {2,3}, 9 batch shapes × due patterns × φ, 553 constructions); [B] 12 bounded wavefront policies (B ∈ {1,2,4,8} × drop/block/coalesce) × DISTINCT bursts k ≤ 12 × DELTA grammars V ≤ 3; [C] wavefront-membership gate + the PLATO write-only-changes case both sides | a fixed-B, no-drop, no-block wavefront policy preserving every enumerated source including adversarial k — publish machine + proof + burst treatment to kill GC-C2(b) (PLATO's shape was thrift, not necessity). A lower-bound proof would resolve it positively instead |
| `gc_c3_span_bench.py` | **GC-C3** span necessity for composition | [A] span witness construction (snap pair: ~80k product runs × five instrumented axioms; byte/hex bridge span); [B] impossibility witnesses computed (256-byte u8/i8 census; custody-motion exhaustion over (v,w) ∈ [1,8]² × reachable b); [C] six cross-link disciplines × two span-less pairs through five computed checkers + span-path control | a discipline passing all five axioms on a span-less pair — publish pair + discipline + five-axiom verification: calculi compose into QS with no adapter span, a genuinely new composition mechanism |
| `gc_c4_snapnorm_bench.py` | **GC-C4** the snap normal form | [A] single-fire census, extended bounds (9,720 candidates, named-clause partition); [B] two-orientation deadband machine (81 runs) + fire-sequence algebra (39 custody-valid sequences, run-length canonical form, order-independent books); [C] wiggle room: coupled corrections (2,700 candidates), 3-cell custody BFS, deferred-debt clauses | a transaction satisfying (i)–(iv) whose account action is not a composition of four-posting snaps (swap paired with debt), invariants exhibited — that kills GC-C4: the emended form is not the normal form of corrections |

## Findings the benches recorded on the way (honesty notes)

- **GC-C1**: the dependency-graph exhaustion confirms GC-T2's organ
  minimality *as a graph property* — only the full six-verb set covers
  Q1–Q5 + all six Θ_v; each 5-subset misses exactly its own Θ_v.
- **GC-C2**: every bounded in-model policy dies at k = B+1 (the
  smallest overflow burst); the DELTA (write-only-changes) grammar fits
  B = V — the buffer bound tracks the *source's* declared shape, never
  the machine: the conjecture's "necessity, not thrift" reading,
  exhibited from both sides.
- **GC-C4**: within the (i)–(iv) class, per-family authority is
  *monotone toward reality* — a fired family cannot re-fire (the display
  renders from the sensor), so machine-reachable multi-fire is
  multi-family; the sequence algebra covers alternating-direction
  sequences, whose canonical form is the run-length merge (alternations
  are irreducible: authority must physically return) and whose books are
  order-independent in direction sums. The deferred-debt pair dies by
  two named clauses (underbook; no-fire-settlement) and nets to the
  canonical snap at run level.
- The falsifier harnesses bit their own author twice during development
  (a `coalesce` overflow fall-through in GC-C2; an over-compressing
  canonicalizer in GC-C4) — both caught by the benches' own controls /
  kill machinery before commit, which is the point of building them.

## Grades

All four conjectures keep their §7 grades (**open**). Nothing here
closes GC-C1, GC-C2(b), GC-C3, or GC-C4; the benches bound the spaces
where a kill would live and demonstrate that the harnesses can see both
preservation and failure (controls green, kill paths probed).
