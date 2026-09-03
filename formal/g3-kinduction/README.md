# G3 k-induction lane — CLOSED 2026-09-02

**Result: `fabric.conservation.g3-certificate.sby` PASS — "successful
proof by k-induction" (smtbmc/boolector, 10 s wall).** The PDR trophy is
now a re-checkable, engine-independent inductive certificate: 910
machine-mined clauses, all 910 resolved by name against the netlist they
were mined from, zero dropped.

## The certificate pipeline (regenerate with `make g3` semantics below)

```
flatten.ys            -> g3_flat.il          (exact sby-prep-equivalent flatten)
transform_guards.py   -> g3_flat_guarded.il  (sticky assume guard, see below)
guarded_aig.ys        -> guarded_aig.il/.aim (sby's model "aig" recipe, no fold)
  strip symbols       -> guarded_bare.aig
bake_constraints.py   -> guarded_baked.aig   (AIGER C-outputs baked into bad outs)
yosys-abc "pdr -d -I" -> bare_inv.pla        (910 clauses; lo<k> = global latch idx)
inject_assumes.py     -> guarded_assumed.il  ($assume cell per clause, 910/910 kept)
sby -f fabric.conservation.g3-certificate.sby  ->  PASS (k-induction, 10 s)
```

## What this lane discovered (all measured, all reproducible)

1. **Classic `abc pdr` ignores AIGER constraint outputs.** Only `fold`
   applies them. Explains the frame-0 "failures": plain pdr on the
   unconstrained miter sees states the assumes exclude.
2. **Fold is what made the committed 854-clause PLA unmappable.** Fold
   retimes and renumbers latches (804 -> 673); trace matching cannot
   recover the correspondence (668/673 ambiguous — symmetric datapath
   latches share traces). Solution here: never fold. Bake the assume
   semantics into the bad outputs instead
   (`bake_constraints.py`: b' = b & !c1 & !c2 & !c3, constraint outputs
   are violation flags) and run pdr on the unretimed net.
3. **pdr's `pdr -d` PLA polarity is the OPPOSITE of the committed
   lane's "implicate probe" pin.** Rows are cubes of EXCLUDED states:
   '1' = NEGATED literal, '0' = positive. Pinned empirically: with this
   convention the 910 clauses pass 273,000 simulated clause-checks from
   init with zero violations; the other polarity violates immediately
   (and makes sby's base case PREUNSAT, which is how the wrong first
   attempt failed loudly).
4. **`pdr -d`'s `.ilb` lo<k> names are GLOBAL latch indices, not
   positional.** `.i 147` counts the support latches; the 147 lo-numbers
   scatter over 0..499. Positional zipping (what the symbol-name dump
   tempts you into) is wrong; `inject_assumes.py` maps via the aig's
   latch symbol table + aim aliases.
5. **The sticky guard is needed for smtbmc assume semantics.** A per-step
   assert guard (b |= !c) is unsound: a trace can violate an assume at
   step 5 with asserts failing at step 3 (base case FAILS — measured).
   `transform_guards.py` latches the violation (g3_sticky: init-0 FF,
   Q <= sticky|viol) so any trace that ever violates an assume is vacuous
   from the violation onward — exactly smtbmc's trace-exclusion, and the
   base case passes again.
6. **The empty-invariant red herring.** PDR on the state-weakened
   (baked, non-sticky) property proves with ZERO clauses in 0.03 s —
   but that proof does not transfer to k-induction (induction from
   arbitrary states genuinely needs the clauses; the sticky-guarded
   harness without them is UNKNOWN). The 910 clauses are real work.
7. **yosys 0.47 IL dialect notes** (cost hours, record to save them):
   `$check` cells come from `formalff -assume`; `async2sync` +
   `formalff -setundef -clk2ff -ff2anyinit -hierarchy` converts them to
   legacy `$assert`/`$assume` (which are the ONLY cells write_aiger
   accepts); hand-written `$assert` cells must carry exactly `\A` +
   `\EN` connects and no parameters; `$concat` is not usable post-check.

## What is committed vs regenerable

Committed: all scripts, the `.sby`, `bare_inv.pla` (the named
certificate artifact, like the lane's committed 854-clause PLA), this
README. Regenerable (`.gitignore`): flattened ILs, aigs, aims, sby run
dirs, `guarded_inv.pla` (symbol-dump, kept out because its `.ilb`
alias list invites the positional-zip bug).

## G1 runway: first honest result is NEGATIVE (2026-09-02)

`group_clauses.py` + `family_report.md`: grouping the 910 clauses by
ring-symmetry template (identical up to one bit-offset anchor) yields
**792 families, 741 singletons, mean 1.15 members/family** under both
anchorings. The symmetric families that do exist are PARTIALLY covered
(e.g. `f_acc[0] | f_acc[i] | ~f_emitA[i]` for i=1..6 only, of 15
positions). Conclusion: PDR's invariant is position-specific and
minimal, not a closed ring template -- the "prove the family template
once per ring position" compression plan does NOT apply to the
machine-mined clause set. A human-readable conservation proof, if
pursued, must be constructed modularly (per-flit argument) from the
design, using the certificate only as a safety net -- not extracted by
compressing PDR output.

### G1 REOPENED same day: template-completion is VALID (hypothesis B confirmed)

Expert nudge split the partial-coverage observation into (A) genuinely
position-specific vs (B) PDR terminated early. Discriminator run:
`fabric.conservation.g3-completion.sby` -- extend the 11 partially
covered families to their missing anchors (+15 candidate clauses, all
injected after the parser fix below; buses are width 8,
families covered anchors 1..6/2..7 of 8) and re-run k-induction on the
augmented invariant: **PASS, basecase + induction.** The completions
are valid inductive strengthening, so the asymmetry was a PDR
termination artifact, NOT a design asymmetry. G1's live shape is now
*template completion / parametric proof*: mine the family templates,
complete them by construction, discharge once per family.

### Shift closure CONFIRMED (2026-09-02, teacher nudge) + parser bug found

The teacher nudge framed the 90 cross-position singleton clauses as a
cyclic-code question: "do they close under shift" = is the clause set a
shift-invariant subspace (circulant kernel / generator polynomial over
F2[x]/(x^n-1)). Empirical discriminator: `shift_closure.py` generates
every valid shifted variant of all data-bus singleton templates
(+702 rows; 45 shifts skipped as out-of-support, 466 already-present
anchors) and the full 1612-clause augmented invariant PASSES
k-induction (`fabric.conservation.g3-shiftclosure.sby`). The data
clause set is shift-closed as inductive strengthening: conservation is
ring-invariant; the 661 control/handshake singleton clauses are the
genuine non-parametric residue. Cyclic-code lineage for the eventual
parametric proof: the family templates behave as code words of a
shortened cyclic code; completion/shift-closure = closure under the
ring action.

**Parser bug found and fixed (inject_assumes.py):** PLA data rows whose
first column is unbound start with the default char '.', and the parser
skipped ALL leading-dot lines as dot-directives -- silently dropping
681/702 shift rows and 5/15 completion rows in the first runs. Fixed:
a data row is now recognized as two tokens with output in {0,1}. All
three sby runs re-verified after the fix (910 / 925 / 1612 clauses,
all PASS). The prior claim "+15 candidates, 10 non-redundant" was
wrong -- it was 5 rows silently dropped by this bug.

## Honest caveats

- The clause set is still machine-mined, not human-prose; the next step
  (G1 runway) is grouping the 910 into families and proving the family
  template once per ring position — the certificate's clause table is
  the input to that.
- The sticky guard slightly WEAKENS the induction obligation vs the
  raw asserts (vacuity after first assume violation); this is exactly
  sby assume semantics and the unguarded asserts are proven under it,
  but the certificate is about the guarded netlist, stated as such in
  the .sby header.
- `pdr -d` was run once with `-I bare_inv.pla`; ABC re-verified the
  dumped invariant at dump time ("Verification of invariant ..."), and
  sby re-checks every clause again in its own base case.
