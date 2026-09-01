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
