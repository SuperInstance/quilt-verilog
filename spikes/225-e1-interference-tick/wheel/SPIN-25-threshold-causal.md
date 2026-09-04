# SPIN 25 — THRESHOLD CAUSAL + BEST-θ (filed follow-up to SPIN-24)

**Spoke:** QUANTIZED-GATE × CAUSALITY · **Date:** 2026-09-03 (pre-registration
written and committed BEFORE any run)
**Files:** `spin25_threshold_causal.py`, `spin25-output.txt`, this report.
**Base code reused:** spin16 `run_fabric_gate` (verbatim), spin24 panel /
`cell` / `sha` / canary pattern. Integer-only in-loop; floats only at
aggregation/print; `python3 -u`, no pipes; seeds {1,7,42} panel.

## QUESTIONS (filed by SPIN-24 follow-ups)

**(a) CAUSAL TEST of the pd=3 second level.** SPIN-24's +7.9pp on kcoh5@15
between t100 halves is correlational: the band halves differ ONLY in nf=6
admission by arithmetic (at pd=3: nf∈{1,5} admit iff t100≤66; nf=6 iff
t100≤99; nf=7 iff t100≤133), but the two runs are different dial settings,
not a controlled toggle. Controlled design: at pd=3, K=1, hold everything
fixed and toggle ONLY nf=6 admission. Realized as t100=99 (nf6 IN) vs
t100=100 (nf6 OUT) — arithmetic guarantee: these two settings have
IDENTICAL admission for every nf≠6 (all other thresholds lie at ≤66 or
≥133), so any behavioral delta is caused by the nf=6 bit alone.

**(b) BEST EMBEDDED θ.** Sweep t100 ∈ {67,75,80,85,90,95,99} (integer gate
thresholds on the sub-1.0 side) on the SPIN-22 anchor panel + step5 rescue.
FIRST verify by full-dict sha which t100 values are behaviorally distinct
(admission-set argument predicts ALL SEVEN are one class: identical
admission set {nf=6, nf=7} ⇒ identical shas); run the panel only on
distinct classes.

## DEFINITIONS (fixed before any run)

Anchors (K=1 unless noted, SPIN-22/24 panel): kcoh5@15 [0,0,0,0,0,15];
ladder@30 = ladder(30); step5/N=7 = ladder_step(30,5) (K=1 and K=2);
zero7 [0]·7. Task filing "zero@30" reads as the SPIN-22 zero cell zero7
(same reading SPIN-24 booked; N=7 twin ceiling makes [0]·30 unreachable).
**Healthy anchors** := kcoh5@15, ladder@30, zero7 (all pile-up-free
grammars). **Rescue set** := {step5K1, step5K2, zero7-gate-vs-never}? — NO,
fixed precisely: rescue(t) := mean over {step5K1, step5K2} of
(pct(t100=t) − pct(gate="never")). zero7 is a healthy anchor here (its
never-gate K=1 cell was already fine in SPIN-22's booking; SPIN-22's
"rescues step5/zero7" referred to the K≥2 band — keep zero7 in the toggle
(a) panel as healthy, out of the rescue metric).

## PREDICTIONS (pre-stated)

- **P-a (causal, healthy-inert):** the +7.9pp on kcoh5@15 REPRODUCES under
  the exact toggle (nf6 IN − OUT ≈ +7.9pp, within ±2pp of 3-seed noise),
  and ladder@30 and zero7 deltas are exactly 0.00pp (byte-identical runs —
  healthy grammars never produce nf≥6 concurrents, so the gate bit is
  inert). Verdict if so: second level is CAUSAL and HEALTHY-INERT.
- **P-b (all one class, simplest wins):** all seven t100 values are
  sha-identical (one distinct class); rescue ≈ SPIN-22's booked nf=7
  rescue (equal for all, since identical); healthy anchors byte-identical
  to gate="never"; zero regression. Best embedded θ = simplest
  representative: t100=67 (edge of the flat half, fewest false promises)
  — but if the class is genuinely flat the "simplest" choice is
  bookkeeping, not physics; book as such.

## DECISION RULE (pre-stated verbatim contract)

- **(a)** causal := kcoh5@15 delta under the toggle ≥ +5pp (reproduces the
  booked magnitude); healthy-inert := |delta| ≤ 1pp AND sha-identical
  runs on ladder@30 and zero7. If any healthy anchor moves >1pp: the level
  COSTS something — book which anchor and how much.
- **(b)** best embedded θ := among distinct t100 classes, the one with
  highest rescue; eligibility requires sha byte-identity vs gate="never"
  on all three healthy anchors AND no healthy-anchor pct regression >1pp.
  Ties broken by simpler (smaller-set / more-negative-side / lowest
  representative) threshold. If all seven are one class: verdict
  "θ-independent in [67,99]", representative = 67, flagged as
  bookkeeping.

## CANARIES (abort on fail; identical to SPIN-24)

1. spread=0 byte-identity: kcoh5@0 K=1, gate "never" vs 1.1 vs dual-run,
   full-dict sha identical, seeds {1,42}.
2. ladder@15 K=1 = 71.5 exact (5-seed anchor set, gate path).
3. plateau K=2 tax ≥ 36pp at the SPIN-23 anchor (square_schedule P=16,
   5↔30, duty 50, TWmean, seeds {1,7,42}); SPIN-23/24 booked 36.7.

## Stages

1. This pre-registration, committed before running.
2. Script + run + raw output (spin25-output.txt).
3. Book: toggle table, distinct-θ table, verdict, scars, follow-up, one
   WHEEL-LOG line.

---

## RESULTS (booked after the run; elapsed 4 s + robustness pass; all canaries PASS)

Canaries 3/3 PASS (identity, 71.5 exact, plateau tax **36.7 byte-equal to
SPIN-23/24** — after one script scar: my first clone pointed dyn_run at
`reality` instead of spin24's `r3_plateau` plateau trace; canary caught it,
fixed, rerun clean).

### (a) nf=6-only toggle table (pd=3, K=1, seeds {1,7,42}; 5-seed robustness in parens)

| anchor | OUT (t100=100) | IN (t100=99) | delta | arms sha-identical |
|--------|---------------|--------------|-------|--------------------|
| kcoh5@15 (target) | 74.6 | 82.5 | **+7.9pp** (+7.94 @5-seed) | N (gate fires) |
| ladder30 (healthy) | 26.1 | 24.7 | **−1.4pp** (−1.34 @5-seed) | N (gate fires) |
| zero7 (healthy) | 99.8 | 99.8 | 0.0 | Y (bit never touched) |

**Verdict: CAUSAL but NOT healthy-inert.** The second level's +7.9pp on
kcoh5@15 reproduces EXACTLY under the controlled toggle (82.5/74.6 — the
same pair SPIN-24 saw across the band halves; now proven causal since the
two settings differ only in the nf=6 admission by arithmetic). But the
pre-registered healthy-inert half is **FALSIFIED**: the cost lands on
**ladder30, −1.3 to −1.4pp** (robust across 3- and 5-seed sets; ladder30's
grammar DOES reach nf=6 concurrents — arms not sha-identical). zero7 is
exactly inert (byte-identical arms: its pile-ups are nf=7, the wall bit,
untouched by this toggle). PREDICTION P-a: causal half RIGHT, healthy-inert
half WRONG.

### (b) Distinct-θ table (sha over full panel × seeds, BEFORE any panel run)

| class | t100 members | note |
|-------|--------------|------|
| 0 (only) | {67, 75, 80, 85, 90, 95, 99} | all sha-identical — admission set {nf6,nf7} constant across [67,99], exactly P-b |

Panel (class rep t100=67): kcoh5@15 74.6→82.5, ladder30 26.1→24.7,
step5K1 0.3→36.3, step5K2 0.4→30.8, zero7 0.1→99.8 (vs gate="never").
**Rescue = +33.2pp** (step5K1/K2 mean vs never).

**Best embedded θ: NONE — no eligible class.** θ is exactly one class on
[67,99] (P-b right, tie-break moot), rescue is large (+33.2pp, plus zero7
0.1→99.8), but eligibility fails on BOTH prongs: (i) byte-identity vs
"never" fails on kcoh5@15 and ladder30 — necessarily, because the gate bit
CHANGES those runs (that is what part (a) proved); the filed rule's
"byte-identity preserved on healthy anchors" silently assumed healthy
anchors never reach nf=6, which part (a) disproved for ladder-class
grammars. (ii) Even under the softer no-regression reading, ladder30
−1.4pp > 1pp kills eligibility. So the sub-1.0 level is a TRADE-OFF dial,
not a free lunch: buy +7.9 kcoh / +33 rescue / +99.7 zero7 for −1.4
ladder.

### Prediction scorecard
- P-a causal — **RIGHT** (+7.9pp exact reproduction under the toggle).
- P-a healthy-inert — **WRONG** (ladder30 −1.4pp; zero7 inert).
- P-b one class across [67,99] — **RIGHT** (all seven sha-identical).

### Scars
1. **"Healthy anchor ⇒ gate never opens" is false for spread grammars.**
  ladder30 hits nf=6; only pile-up-free-by-structure grammars (zero7, all
  twins equal) are structurally inert. Byte-identity eligibility rules must
  be per-anchor, not blanket.
2. **Canary 3 caught a wrong-trace clone** (reality vs r3_plateau): the
  tax anchor is the only cell sensitive to which trace dyn_run rides —
  keep it in every spin that clones spin23 machinery.
3. The decision rule conflated "no regression" with "no change": the two
  prongs can disagree (kcoh5 changes +7.9 with no cost). Book both
  readings separately next time.
4. SPIN-24's scar 3 (bestpair cannot isolate crossings) is now resolved at
  pd=3 by the exact-toggle design; pd=2's nf=4 crossing remains untested.

### Follow-up
- pd=2 exact-toggle (nf=4-only pair) to settle SPIN-24's rule-technical
  MULTI verdict at pd=2 — does the sub-crossing there also carry a cost?
- Cost/benefit frontier: is the ladder30 −1.4pp the SAME mechanism's shadow
  (nf=6 compensation mis-dividing ladder-grammar errors)? Per-tick gcomp
  diff between arms on ladder30 would localize it.
- If an embedded rule is wanted despite the trade: the wall bit alone
  (t100 ∈ [100,133]) rescues step5/zero7 with kcoh untouched — sweep the
  OTHER half's eligibility; the free lunch may live there, not at nf=6.

Status: **COMPLETE.** Committed+pushed g3-kinduction. WHEEL-LOG appended.
