# SPIN 16 — SPOKE: PULSE-DIAL II: ADAPTIVE (ECHO-GATED) COMPENSATION

**Lane:** subagent spin (proposal-dispatched by SPIN-11's Next section; no LCG
pick consumed) · **Date:** 2026-09-03 · **Files:** `spin16_pulse_dial2.py`,
`spin16-output.txt`, this report · Pre-registration committed BEFORE any run
(2dacb9d); post-hoc corrective addendum clearly labeled inside script and raw
output. Fabric: `spin11_pulse_dial.run_fabric_mc` reused verbatim for off/MC-A
arms; new runner `run_fabric_gate` = exact copy of its interference loop with
one per-tick gate at the emission line. mc=0 byte-identity preserved (canaries
CC/CE). Integer-only in-loop (gate test included: `100·|pd−nf| > θ100·pd`).
Seeds {1,7,42,1999,20260902}, 4800 ticks, EV=12 pinned everywhere.

## Verdict: ADAPTIVE GATE VALIDATED FAR BEYOND REGISTRATION — THE WALL LAW IS NOW A SCHEDULER

Spin 11's registered prediction (R1) **PASS with 4× margin**: gated
compensation rescues step5/N=7 **0.3 → 36.9** (registered ≥ 9.0; blanket MC-A
managed only 8.8) while kcoh5 stays **53.2 ≥ 50** byte-identically (the gate
provably never opens for N=6=2pd at pd=3 — canary CE full-dict). **The
compensation trade of SPIN 11 is dissolved**: healthy grammars are untouched
(K-trough, comp×K signs, every number identical to off), wall casualties are
rescued 4× better than blanket compensation. The gate is Spin 8/11's wall law
(|1−N/pd| > 1) implemented as an in-loop scheduler on the concurrent trigger
count nf. One instrument artifact (guard-prefix inflation) gamed the
registered θ\* selection — caught, booked, corrected post-hoc (below).

## EXP 1 — θ calibration (θ ∈ {1.05, 1.1, 1.25, 1.5, 2})

| cell | off | MC-A | θ=1.05 | 1.1 | 1.25 | 1.5 | 2.0 |
|---|---|---|---|---|---|---|---|
| step5/N=7 pd=3 | 0.3D | 8.8 | **36.9** | 36.9 | 36.9 | 15.3D* | 15.3D* |
| kcoh5@30 pd=3 | 53.2 | 37.6 | 53.2 | 53.2 | 53.2 | 53.2 | 53.2 |
| ladder30x13 pd=6 | 2.3D | 8.1 | **23.9** | 23.9 | 18.1D* | 18.1D* | 18.1D* |

\* = guard-prefix artifact, see Scars. Integer gate arithmetic quantizes the
sweep: at pd=3, {1.05, 1.1, 1.25} all open exactly at nf≥7 and behave
byte-identically; {1.5, 2.0} never open. At pd=6 the sweep separates exactly
as the coverage law predicts: **gate opens at a 2pd+1 wall iff θ < 1+1/pd**
(1.05→pd≤19, 1.1→pd≤9, 1.25→pd≤3, 1.5→pd≤1, 2.0→none) — behaviorally
confirmed at both walls. Gate diagnostics: step5 gOpen ≈ 448 ticks (~9%),
compTw ≈ 3139 of 20883 emissions (~15%) — the gate compensates 15% of events
and leaves the other 85% at full corrective strength; that 85% is worth
+28pp over MC-A (36.9 vs 8.8). P16b booked **FAIL as registered** (the
no-rescue band "true12 ≤ 3.0" was broken by the prefix artifact 18.1), with
correct divergence-flag legs; the law underneath is confirmed.

## EXP 2 — full panel × delta {12,24} × K {1,2,4} (pd=3)

- **All five N=6 grammars: gate ≡ off, byte-identical, structural** (nf ≤
  6=2pd ⇒ concurrent factor ≤ 1.0 < θ). kcoh5 53.2, kcoh1 13.2, ladder 26.8,
  cohort 49.3, zero 77.3 — all K-rows, both deltas, unchanged. Spin-11's
  damage table (kcoh5 53.2→37.6, cohort 49.3→11.4, ladder 26.8→9.5 under
  MC-A) simply does not happen under the gate. K=2 trough preserved for
  every N=6 grammar (structural); comp×K interaction signs preserved.
- **Corrected step5 rows (EXP 2b, θ_c=1.1):** δ12 K{1,2,4} = **36.9 / 30.8 /
  17.7** vs MC-A 8.8/10.1/12.5 — gate wins every cell; δ24 native-window
  67.9 / 65.2 / 69.2 vs MC-A 64.7/64.1/65.4. The gated rescue is
  K-monotone-decreasing (K4−K1 = −19.2): memory overlap erodes it; best at
  K=1 (spin-10's "the joint optimum uses no memory" echo).
- **Serendipity: zero + MC-A = 99.6/99.5 (δ12), 100.0 native (δ24 K=1)** —
  blanket compensation nearly perfect on zero-lock (off 77.3/50.0), i.e.
  zero-lock's failure IS uncompensated synchronized mass. The gate cannot
  see it: at exactly-2pd pile-ups the factor is exactly 1.0 < θ. Sub-1.0 θ
  is the missing dial (booked in Next).

## EXP 3 — AS × gate composition (the Spin-14 interaction question)

Registered grid (N=7 supra-wall grammars, θ\*=2.0 — contaminated selection,
see Scars): its **base and AS arms are clean and decisive**: every N=7
grammar diverges uncompensated (0.2–0.4D) **including zero-lock at span 6**
(the wall survives low spread — Spin 8's N>2pd law is not a spread artifact),
and **AS-exact rescues none of them** (gains +0.0…+2.6pp, every arm still
diverged). Phase scheduling cannot cross a mass wall.

Corrected grid (EXP 3b, θ_c=1.1, self-contained rerun):

| grammar | K | base | AS | gate | AS+gate | gOpen gate→joint |
|---|---|---|---|---|---|---|
| step5 | 1 | 0.3D | 0.3D | **36.9** | 36.9 | 448→448 |
| kcoh1w7 | 1 | 0.2D | 0.3D | **50.7** | 34.4 | 2776→1209 |
| cohort37 | 1 | 0.3D | 0.4D | **34.6** | 41.6 | 1820→1032 |
| zero7 | 1 | 0.4D | 3.0D | **99.8** | 97.7 | 942→72 |
| zero7 | 2 | 0.4D | 1.3D | **99.4** | 94.0 | 581→155 |

(zero7 99.8 = near-perfect cure of a diverged zero-lock; kcoh1w7 50.7,
cohort37 34.6 similar rescues.)

**P16a (registered): no qualifying cells — UNTESTABLE, not falsified.** Its
antecedent ("both singles beat base by ≥5pp") is unsatisfiable on any N=7
grid because AS's gain above the wall is ~0. Corrected grid: same outcome
(AS gains ≤ +2.6). **Answer to the dispatched question: neither super- nor
subadditive — DOMAIN-DISJOINT.** Partition theorem (structural, for every
θ>1): gate-open ⟺ nf ≥ 2pd+1 ⟺ supra-wall pile-up; AS measurably works only
sub-wall. The knobs partition the failure space; Spin 14's
orthogonal-channel composition law does not extend to the gate because the
gate's channel is the one channel AS cannot enter. The observed AS-under-gate
effects are grammar-dependent second-order residue (cohort37 +7.0/+3.6 —
after gating cures divergence, the grammar behaves sub-wall and AS's normal
decorrelation benefit reappears; kcoh1w7 −16.3; zero7 −2.1/−5.4) — a
**sequencing law, not a composition law: gate first (cure the wall), then
phase-schedule (tune the sub-wall structure).**

## Canaries — ALL PASS (run before experiments; abort-on-fail)

CA spin-11 replays 26.8/0.3/0.1/53.2 exact · CB spread=0 codepath identity ×
4 gate modes (12 codepaths, 2 N-groups each) · CC gate="never" ≡ mc=0
full-dict, 8 configs · CD gate="always" ≡ mc=1 full-dict, 8 configs ·
CE structural N=6/pd=3 inertness: gate {1.05, 1.25} ≡ mc=0 full-dict (5
grammars + K4/δ24 probes) — the byte-level guarantee behind R1(b).

## Scars / honest boundaries

- **Guard-prefix artifact (the spin's own scar):** numeric-θ arms that never
  open still carry spin-11's |e|>10^12 memory guard → they bail and their
  true12 is a PREFIX statistic (step5 15.3, wall6 18.1 vs full-window 0.3,
  2.3), inflated yet still flagged D. This gamed the registered θ\* rule
  (thresholds met on prefix stats → θ\*=2.0, a closed gate). Caught because
  EXP 2/3 rows showed gOpen=0 with numbers ≠ off; corrected post-hoc at
  θ_c=1.1 (largest clean non-diverged selection), everything labeled. Rule
  learned for registrations: **selection rules must condition on the
  divergence flag, not only on the number.**
- θ-quantization: the sweep is integer-coarse ((nf−pd)/pd has granularity
  1/pd); at pd=3 it collapses to two behaviors. Coverage across pd requires
  θ < 1+1/pd_max; a fixed θ=1.05 covers every pd ≤ 19.
- Gate blind at exactly-2pd chatter (factor exactly 1.0): zero6 stays 77.3
  under the gate while MC-A reaches 99.6 — adaptive compensation cures
  divergence, not wall-edge chatter (needs θ < 1, untested).
- AS-under-gate residuals are grammar-dependent (−16.3 … +7.0) and measured
  only at 8 cells; the sequencing law is a proposal, not a mapped surface.
- EXP 2 gate rows for N=6 grammars are structural copies (≡ off), not reruns
  — justified by canary CE byte-identity; noted where printed.

## Next (proposed spokes)

1. **Sub-1.0 θ (wall-edge gate):** θ ∈ (1/pd, 1) opens at nf=2pd pile-ups —
  predicted to cure zero6's 77.3 → ~99 while (at θ > 1−1/pd, e.g. 0.9)
  still never touching sub-wall healthy grammars; the gate then covers the
  whole pile-up spectrum with a two-threshold schedule.
2. **Sequencing law:** gate-then-AS vs AS-then-gate vs joint on the cured
  sub-wall regime (cohort37's +7.0 hints order matters); prediction ready:
  gate-first ≥ joint ≥ AS-first for every supra-wall grammar.

## Log-ritual bookkeeping

Proposal-dispatched (SPIN-11's Next) — no LCG pick consumed; ledger head
486256185; next selection reference 486256185 → 1062517886 → mod 10 = 6.

VERDICT: VALIDATED (R1 PASS at 4× margin — step5 0.3→36.9 with kcoh5 byte-frozen at 53.2; the gate = wall law as scheduler, θ-coverage law confirmed) / P16b FAIL-by-artifact (prefix inflation, D-flags honest) / P16a UNTESTABLE (antecedent unsatisfiable — AS cannot cross the wall) / composition answer: DOMAIN-DISJOINT (partition theorem), sequencing law proposed.
