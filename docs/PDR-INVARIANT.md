# The PDR invariant, dumped and read — the lemma k-induction was missing

**Date:** 2026-08-31 · **Follows:** FORMAL-PROOFS.md §"PDR referee" (the
booked `pdr -i` follow-up lane) · **Trigger:** STUDENT nudge
("it EXISTS, can you dump it?") · **Answer: yes.**

## TL;DR

`fabric.conservation` is sealed unbounded by an explicit, machine-derived,
inductive invariant: **854 clauses over 169 latch variables** (ABC PDR,
`-d -I` dump, proof time 39.8 s from the SBY-model aiger directly).
It is committed here in two forms — the ABC PLA
(`fabric.conservation.invariant.pla`) and a signal-named rendering
(`fabric.conservation.invariant.readable.txt`, one clause per line, every
literal mapped through the SBY aiger map to hierarchical Verilog names
with bit indices). "The engine is smarter than us" is now "here is the
invariant, and here is what it says."

## Method (reproduce in ~40 s)

```
cd formal/fabric.conservation.pdr/model
yosys-abc -c "read_aiger design_aiger.aig; fold; strash; \
              pdr -v -l -d -I invariant.txt; quit"
```

`-d` requires the all-zero init convention — which the SBY aiger already
satisfies by construction. Latch names come from `design_aiger.aim`
(`latch <var> <bit> <name>` lines; multi-bit signals appear under one name
with per-bit indices — the naive name-only rendering shows impossible
clauses like `f_book & !f_book` because bits collapse; annotate bits or
you will "find" contradictions that aren't there).

## What the invariant says (clause-size histogram)

2-lit: 67 · 3-lit: 191 · 4-lit: 264 · 5-lit: 167 · 6-lit: 76 · 7+: 88+32.
Three readable families:

1. **The pipe-content hypothesis (dominant).** `!u_pipe.m_a0[3]` appears
   in 752 of 854 clauses. The flit pipe is (almost) never allowed to hold
   a command with `a0` bit 3 set; nearly every other fact is conditioned
   on it. This is exactly the "`op == OP_EFF`-style pipe-content clause"
   FORMAL-PROOFS.md guessed the strengthening would need — confirmed.
   The companion shapes: `m_a1[0..1] & !m_a0[3]`, `m_a2[5,14,15] &
   !m_a0[3]`, odd-parity style `m_dat[k] & !m_a0[3]`.
2. **Per-bit accounting lemmas (the conservation core).** ~300 clauses of
   the form `!f_acc[k] & f_emitA[k..] & !f_pocc[0..1]`,
   `f_acc[k] & !f_book[..] & !f_book[k]` — the account balance vs
   booked/emitted/pending occupancy relation carried bit-plane by
   bit-plane, plus `f_book`/`f_icnt`/`f_sA`/`f_emitA` couplings. This is
   the conservation property itself, embedded as strengthened bit-level
   facts — the human prose version ("value conserved across
   book/emit/pocc") written out bitwise by the machine.
3. **Cross-core handshake coordination.** `u_coreB.hb_wq[..] &
   u_coreB.act_e[..]`, `!u_coreB.eff_pe & !u_coreA.u_rq.i_sel &
   !u_engB.rstate & u_coreB.act_e` — request-bank occupancy vs core FSM
   state vs engine rstate, cross-core (206 clauses mention both cores).

## Honest status

- **Inductive and machine-checked:** these 854 clauses (conjoined) hold
  in all initial states and are preserved by the transition relation —
  that is PDR's output contract, verified by the 39.8 s proof run.
- **Not minimal, not tidy:** PDR over-approximates then prunes; expect
  redundancy (the same apparent fact at several bit-indices) and no
  pretense of a short "reason." It is the lemma set k-induction lacked,
  not a textbook.
- **Readability, not yet elegance:** the human L1/L2 whitebox writeup
  remains OPTIONAL — the machine now does what it was going to document.
  If someone distills ~854 clauses into 3 named lemmas later, this file
  is the raw material.
- **k-induction still fails** with this invariant available: PDR's
  clauses are the strengthened conjecture; feeding them back as
  assumptions to `mode prove` smtbmc is the obvious next experiment
  (unbooked, cheap, would close the loop from "exists" to "reusable").

## Files

- `fabric.conservation.invariant.pla` — ABC's own dump (positional PLA,
  `lo###` latch indices).
- `fabric.conservation.invariant.readable.txt` — 854 lines, one clause
  per line, ` & `-joined signal names with bit indices.

## Follow-up lane (2026-08-31, STUDENT nudge): feed the clauses back

**Booked ask:** assume the 854/981-clause invariant in the `mode prove`
smtbmc run — either k-induction closes (certificate is complete + reusable)
or it doesn't (real finding). **Outcome: partially landed, with two real
toolchain findings and one open question the DEVIL lane should see.**

**Landed:**

1. **Self-contained certificate reproduction.** The SBY model aiger +
   sby's own aiger script were replicated standalone
   (`formal/pdr-invariant/sbyreplica/`): `abc pdr -d -I` re-proved
   conservation unbounded (39.0 s) and — decisive — **ABC re-verified the
   dumped invariant in the same run: "Verification of invariant with 981
   clauses was successful"** (981 clauses / 171 latches on the replica
   encoding; the original dump was 854/169 — different gate
   normalization, same property). The certificate's inductiveness and
   property-implication are machine-checked by the tool whose semantics
   define them. Committed: `inv.txt` (PLA), `inv_readable2.txt`
   (signal-named, bits annotated).

2. **The invariant is human-readable and family-structured** (pipe
   hypothesis, per-bit conservation core, cross-core handshake
   coordination — see above). 10 of 981 clauses reference aiger free-state
   bits (anyinit encodings); dropping them only weakens the lemma.

**Findings (either-way ask, outcome 2-flavored):**

3. **yosys silently re-declares hierarchical references.** A Verilog
   lemma file referencing `u_coreA.act_e` from the harness gets a FRESH
   WIRE named `\u_sub.inner_reg` with only a warning — the connection is
   silently dropped. Any future "assume the lemma" flow must inject
   post-`flatten` (or expose ports); naive hierarchical assumptions are
   sound-traps.

4. **`write_verilog` roundtrip of the flattened formal design is not
   faithful** (memory bits get multiple drivers on re-read; `$anyseq`
   cells need a whitebox stub). The smtbmc-with-assumed-lemmas harness
   was not landed through this path.

5. **OPEN QUESTION (init-encoding correspondence — DEVIL lane).** An
   independent SMT cross-check (yosys `write_smt2 -wires` from the same
   `design_prep.il` + hand-written property) found clauses like
   `u_coreB.act_e[4] & u_coreB.hb_wq[4]` violated at the SMT initial
   state: after `async2sync` + `formalff`, registers without reset
   attributes (act/state families) appear FREE at t0 in the smt2
   encoding, while the aiger (`write_aiger -zinit`) forces every latch to
   0 at t0. So "the PDR invariant holds in the initial state" is true in
   the aiger encoding and *not even well-posed* in the smt2 encoding
   without deciding which init semantics is the intended one. The
   conservation property itself is independently safe (smtbmc basecase
   PASS on the same harness, and every RTL bench), but **whether the
   abc-pdr unbounded PASS is init-faithful to the Verilog-level model
   depends on sby's sanctioned zinit semantics and is not yet
   adjudicated.** Until then, the honest citation remains: *unbounded in
   the aiger encoding ABC proves; bounded-55 + prose at the Verilog
   level; equivalence of the two encodings' initial states = open lane.*

**Reproduce (replica + dump + verification, ~45 s):**
```
cd formal/pdr-invariant/sbyreplica
yosys -q -p "read_rtlil design_prep.il; delete */t:\$print; \
  hierarchy -simcheck; formalff -assume; flatten; setundef -undriven -anyseq; \
  setattr -unset keep; delete -output; opt -full; techmap; opt -fast; \
  memory_map -formal; formalff -clk2ff -ff2anyinit; simplemap; dffunmap; \
  abc -g AND -fast; opt_clean; write_aiger -zinit -map sby.aim sby.aig"
yosys-abc -c "read_aiger sby.aig; fold; strash; pdr -d -I inv.txt; quit"
```
