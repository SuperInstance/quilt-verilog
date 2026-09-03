# Tick-liveness proof — referee's notes

*Written for the EXPERT cross-exam (2026-09-03). Everything below is
quoted from logs in-tree; nothing is paraphrased from memory.*

## Claim under exam

`formal/cell_core.tick.prove.sby` (abc PDR, sby mode prove): every tick
strobe is serviced — Q2a1 strobe→ci_ready pulse ≤100 cycles, Q2a2 first
sweep cmd ≤66 cycles, Q2b pending strobe ⇒ !ci_ready — under permanent
ingress flood and arbitrary strobes. Committed as c1f5a73 ("unbounded
tick liveness via PDR, 747s").

## (1) What encoding? Liveness-to-safety, and which assumptions carry it

The deadlines are **bounded-response safety encodings**: shadow trackers
in `formal/f_cell_core_tick.v` arm a 7-bit cycle counter at each strobe
(`f_dl`, max 100 < 128) and assert the witness (ready pulse / sweep cmd)
before the counter caps. A violated deadline is a finite counterexample;
an unbounded PASS is a safety invariant. No unbounded-progress fairness
(assume-guarantee "eventually", SVA fairness, or liveness under
fairness) is used anywhere — so there is no fairness caveat, because
there is no liveness-to-safety-with-fairness step to hide one.

What the proof IS conditional on — stated plainly:

- **E1 (adversity, not progress):** `assume (ci_valid)` during reset-
  free operation — ingress never stops. This makes the environment
  harsher, not friendlier.
- **E2 (engine responsiveness contract):** `assume (f_hbc <= f_hblim)`
  — the HEbb engine answers set-base/clear commands within 12 cycles
  (set-base) / 4 (others), enforced by a counting assumption. This is
  a bounded safety contract on the engine, **not proven here**. Its
  silicon corroboration is measured (q_hebb_edge answers in 10/2 —
  docs/BACKEND-NOTES.md). The liveness theorem reads: *given* an
  engine meeting E2, every strobed tick is serviced ≤100 cycles.
  If the engine regresses past its contract, Q2a1 does not cover it —
  the engine's own responsiveness is a separate proof obligation.
- **E3 (dialfile stub):** 1-cycle read latency, matching rtl/q_dialfile.

So the honest headline is: **unbounded bounded-response liveness,
conditional on E1/E2/E3, all three of which are bounded safety
contracts — no fairness assumptions of any kind.**

## (2) Did PDR converge to an inductive invariant, or just run out of BMC?

It converged. Exact termination lines (sby run and the independent
re-run, both in-tree under `tick-liveness/`):

```
Proved output 1 in frame 3 (converged).            (sby run, logfile.txt)
Invariant F[106] : 8743 clauses with 0 flops (out of 361) (cex = 0, ave = 44.67)
Verification of invariant with 8743 clauses was successful.  Time =     0.45 sec
Property proved.  Time =   400.04 sec              (independent re-run)
Property proved.  Time =   745.75 sec              (original sby run)
```

"Verification of invariant ... was successful" is ABC *independently
re-checking* that the 8743 derived clauses are inductive (init ∧ T ⊆ I,
I ∧ T ⊆ I). That is a proof of unbounded safety, not a depth-limited
"no CEX ≤130". (The sby `[options] depth 130` is irrelevant to the abc
pdr engine's convergence; the frame count that matters is F[106].)

## (3) The artifact

`tick-liveness/inv.pla` — the dumped inductive invariant, 8743 clauses
over 90 inputs / 1 output (813 KB, PLA). Dump command (the `-d` flag is
required; without it ABC writes an empty file and says nothing):

```
yosys-abc -c "read_aiger model/design_aiger.aig; fold; strash; \
              pdr -d -v -I inv.pla"
```

(aig produced by `sby -f formal/cell_core.tick.prove.sby`; model inputs
are constraint-encoded AIGER, same convention as the G3 dump.)

**Ring-scale follow-up (booked, not done):** instantiate this per-cell
liveness proof at NCELL 2/4/8 (5d9d848 lineage) to close G2 across the
ring. The dumped clause family is the asset to diff across
instantiations — if the ring-scale invariants are per-cell copies plus
boundary clauses, G2 closes almost for free; if not, the diff IS the
new coupling analysis.
