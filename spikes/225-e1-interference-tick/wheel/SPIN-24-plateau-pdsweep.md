# SPIN 24 — PLATEAU PD-SWEEP (filed follow-up to SPIN-22/23)

**Spoke:** QUANTIZED-GATE × REGIME · **Date:** 2026-09-03 (pre-registration written and committed BEFORE any run)
**Files:** `spin24_plateau_pdsweep.py`, `spin24-output.txt`, this report.
**Base code reused:** spin16 `run_fabric_gate` (crossing machinery), spin21 trace generator (`r3_plateau`), spin23 `dyn_run`/`tax` clones. Integer-only in-loop; floats only at aggregation/print; single-pass inline; `python3 -u`, no pipes; seeds {1,7,42} panel.

## QUESTIONS (filed by SPIN-22 Next + SPIN-23 surprise)

**(a)** SPIN-22 found the θ dial has ONE useful level at pd=3 (only crossing in
band: nf=7=2pd+1) and its Next asked: find the first pd where TWO in-band
crossings exist. Sweep pd ∈ {1..8} on the anchor panel and map where a second
crossing enters the useful band — is there a pd where the gate is genuinely
multi-level?

**(b)** SPIN-23's surprise: plateau (0-slope) K=2 tax is 36.7pp, the LARGEST
trace. On plateau only, sweep the K=2 regime vs pd and test whether the
co-fire law m = N/(2pd+1) ≈ 1 still prices the wall when slope is zero — does
the wall move with pd, and does it sit at m≈1?

## DEFINITIONS (fixed before any run)

Gate test (spin16, verbatim): opens at nf iff `100·|pd−nf| > t100·pd`, i.e.
nf is admitted iff `t100 < T_nf := 100·|pd−nf|/pd`. Max twins N=7, so
reachable nf ∈ {1..7}, nf≠pd (nf=pd never opens: 0 > t100·pd false).

**Useful band at pd** (SPIN-16's two flanking crossings around θ=1):
t100 ∈ (100·(1−1/pd), 100·(1+1/pd)] — bounded below by the 2pd−1 chatter
crossing and above by the 2pd+1 wall crossing. **In-band crossings** = the
distinct thresholds T_nf (over reachable nf) strictly inside this band.
(Task language note: the task calls the second crossing "nf=2pd−1"; under the
spin16 gate arithmetic that threshold equals the band FLOOR exactly, and the
in-band set at pd≤3 is {nf=2pd (T=100), nf=2pd+1 (T=band ceiling)}. We test
all reachable crossings empirically, in-band and out, so the verdict does not
hang on this bookkeeping choice.)

**Anchor panel (a), K=1 unless noted** (SPIN-22 panel): kcoh5@15
[0,0,0,0,0,15]; ladder@30 = ladder(30); step5/N=7 = ladder_step(30,5);
step5 K=2; zero7 [0]·7. ("zero@30" in the task filing read as the SPIN-22
zero cell = zero7.)

## PREDICTIONS (pre-stated)

- **P-a: NO pd is genuinely multi-level.** In-band crossing count vs pd
  (N=7): pd=1 → {nf2,nf3}, pd=2 → {nf4,nf5}, pd=3 → {nf6,nf7} (2 crossings
  each, by arithmetic), pd≥4 → 0 (max T_nf = 100·(pd−7)/pd < band floor for
  pd≥4 since the 2pd+1 wall exceeds N=7). So nominally 2 in-band crossings at
  pd ≤ 3 — BUT the second (nf=2pd, θ=1.0/strict) only separates at t100 ≤ 99
  (θ<1 sub-1.0, SPIN-16's "missing dial"), and I predict the sub-1.0 side is
  behaviorally DEAD on the anchor panel at every pd: pct differences ≤1pp
  everywhere (pile-ups of exactly 2pd are rare and their compensation is
  absorbed by the K-decay). Verdict: NOT multi-level at any pd; the gate is
  one bit per pd, wall bit only, for all pd ∈ 1..8.
- **P-b: the wall MOVES with pd on plateau and sits at m≈1.** The co-fire law
  is a pile-up-rate law (spin-11: the wall is a rate, not a line), so slope
  should not matter: predicted wall_edge(pd) = 2pd+1 exactly (first collapsed
  N), ratio = 1.00, all inside 0.8–1.25.

## DECISION RULE (pre-stated verbatim contract)

- **(a) multi-level gate** := exists pd ∈ {1..8} with ≥2 in-band crossings
  AND a (K, θ/t100) pair of in-band settings selecting different crossing
  subsets whose panel pct differ by >1pp on at least one anchor. Otherwise:
  **one-level at every pd** (prediction P-a holds).
- **(b) plateau wall** := for pd ∈ {1,2,3,4,6,8}, zero grammar [0]·N,
  K=2, plateau trace, N swept 1..min(2pd+4, 20); ref(pd) = max mean pct over
  the sweep; collapsed(N) := mean pct < ref − 10pp; wall_edge(pd) = smallest
  collapsed N (if none, wall_edge = "beyond sweep", excluded from ratio).
  Report ratio wall_edge/(2pd+1); **flag any pd with ratio outside
  [0.8, 1.25]**. Wall "moves with pd" iff wall_edge is non-decreasing in pd
  and strictly increases at least twice; "sits at m≈1" iff all ratios inside
  the flag band.

## CANARIES (abort on fail)

1. **spread=0 byte-identity:** run_fabric_gate kcoh5@0 (lats [0]*6) K=1,
   gate "never" vs 1.1 vs dual-run, full-dict sha identical, seeds {1,42}.
2. **ladder@15 K=1 = 71.5 exact** (5-seed anchor set, gate path, R0).
3. **plateau K=2 tax ≥ 36pp at the SPIN-23 anchor config:** square_schedule
   (P=16, 5↔30, duty 50), K=2, TWmean tax, panel seeds {1,7,42}, plateau —
   SPIN-23 booked 36.7.

## Stages

1. This pre-registration, committed before running.
2. Script + run + raw output (spin24-output.txt).
3. Book: crossing-count table per pd, plateau wall ratios, verdicts, scars,
   follow-up, one WHEEL-LOG line.

---

## RESULTS (booked after the run; elapsed 107 s; all canaries PASS)

Canaries 3/3 PASS: spread=0 byte-identity (never == θ1.1 == dual-run sha);
ladder@15 K=1 = 71.5 EXACT; plateau K=2 tax = **36.7pp, byte-equal to
SPIN-23's booking** — the surprise reproduces.

### (a) Crossing-count table per pd (N≤7 twins; band (1−1/pd, 1+1/pd])

| pd | in-band crossings | verdict (pre-registered rule) | note |
|----|--------------------|-------------------------------|------|
| 1 | 2 (nf=2@θ1.0, nf=3@θ2.0) | one-level — 0.00pp spread across the WHOLE 200-setting dial | every nf pile-up (≥2 of 7) already fires together; gate bit changes nothing |
| 2 | 2 (nf=4@θ1.0, nf=5@θ1.5) | **MULTI-LEVEL** (53.6pp @ kcoh5@15, t100 51 vs 150) | delta dominated by the WALL bit (nf=5); the nf=4 sub-crossing is NOT shown live by the bestpair search (scar 3) |
| 3 | 2 (nf=6@θ1.0, nf=7@θ1.33) | **MULTI-LEVEL — genuinely two-level** (7.9pp @ kcoh5@15: 82.5 @ t100∈[67..99] vs 74.6 @ [100..133]) | BOTH crossings live: nf=7 rescues step5/zero7 (SPIN-22's bit); nf=6 adds +7.9pp on kcoh5@15. The two t100 halves are each internally FLAT (67..99 and 100..133 constant) — the gate is exactly 2 bits at pd=3 |
| 4 | 0 (wall nf=9 > N=7) | one-level (band empty, 0.00pp) | gate cannot reach its wall; band inert |
| 5–8 | 0 | one-level (0.00pp) | same; only sub-θ1.0 chatter crossings remain, all below band |

**Answer to (a): YES — the gate is genuinely two-level, but ONLY at pd=3
(and nominally pd=2), and the second level is the SUB-1.0 dial SPIN-16
called the "missing dial": the nf=2pd (θ=1.0-floor) crossing.** SPIN-22's
"one level" held only for the θ>1 half-band it swept. For pd≥4 with N=7
twins the band is EMPTY — the wall leaves the reachable nf set and the gate
dial goes totally flat (0.00pp across every in-band setting).

PREDICTION P-a ("sub-1.0 side is behaviorally dead at every pd") is
**FALSIFIED** at pd=3: admitting nf=6 pile-ups improves kcoh5@15 by +7.9pp
(74.6 → 82.5). Verified arithmetic: both band halves are internally
constant, so this is a real second level, not noise (3-seed means; the two
halves differ by construction only in whether nf=6 admits).

### (b) Plateau wall vs pd (zero grammar, K=2, seeds {1,7,42})

Pre-registered fit (ref−10pp, smallest N) FLAGS every pd — but inspection
shows the flag is the FIT's fault, not the wall's (scar 2): the pre-wall
decay is gradual (pd=3: N4 82.0 → N5 67.2 → N6 28.8), so "ref−10pp" fires
on the shoulder, and at pd=6/8 it even fires on the N=1 startup transient
(85.3 vs ref 98.3). The DIVERGENCE edge (pct → <5, resid blows up) is:

| pd | last healthy N | first collapsed N (pct) | 2pd+1 | ratio |
|----|----------------|--------------------------|-------|-------|
| 1 | 2 (12.8) | 3 (0.6) | 3 | 1.000 |
| 2 | 4 (33.3) | 5 (0.6) | 5 | 1.000 |
| 3 | 6 (28.8) | 7 (0.7) | 7 | 1.000 |
| 4 | 8 (28.9) | 9 (0.7) | 9 | 1.000 |
| 6 | 12 (34.3) | 13 (1.6) | 13 | 1.000 |
| 8 | 16 (32.9) | 17 (1.0) | 17 | 1.000 |

**Answer to (b): the co-fire law m = N/(2pd+1) ≈ 1 prices the plateau wall
EXACTLY — first collapsed N = 2pd+1 at all six pd, ratios 1.000 (0 flags
under the honest edge fit), wall strictly increasing 3→5→7→9→13→17.**
Zero slope does not move the wall. The pre-registered fit rule is booked as
falsified (it flagged all six pd); the divergence-edge reading is POST-HOC
and flagged as such — but it is not a fit, it is an exact integer equality
six-for-six, hard to explain away.

PREDICTION P-b ("ratio 1.00, all inside band") is **RIGHT in substance**
under the edge reading and **WRONG under the pre-registered fit** — booked
honestly as a rule-design failure, not a physics failure. Also notable: the
approach to the wall is a decaying SHOULDER (m→1 from below prices in
gradually: 97.9→82.0→67.2→28.8→0.7 at pd=3), so the SPIN-23 plateau tax
(36.7pp) and the wall law are the same object: the K=2 regime bleeds
continuously as N/(2pd+1) → 1 and cliffs exactly at 1.

### Prediction scorecard
- P-a one-level everywhere — **WRONG** (two-level at pd=3, +7.9pp live
  second crossing; nominal multi at pd=2 via the wall bit).
- P-b wall at m≈1 — **RIGHT in substance** (edge = 2pd+1 six-for-six),
  **WRONG under the pre-registered fit rule** (all six flagged).

### Scars
1. **SPIN-22's scar was half-right for the wrong reason:** it said the
   θ dial is a phantom at pd=3 — true only of the θ>1 half. The full band
   (1−1/pd, 1+1/pd] has TWO flat halves at pd=3 separated at t100=100.
   Any future θ study must sweep across θ=1, not just (1, 1+1/pd).
2. **ref−10pp "wall fit" is unusable when the pre-wall shoulder decays
   gradually** (and catastrophic when the max sits mid-sweep, as at pd=6/8
   where N=1's startup transient read as "collapsed"). Divergence edge
   (pct<5 after blow-up) is the honest statistic; booked post-hoc, flagged.
3. **bestpair search does not isolate WHICH crossing drives a MULTI-LEVEL
   verdict.** At pd=2 the 53.6pp delta is the wall bit (nf=5); whether the
   nf=4 crossing is independently live on any anchor is unresolved by this
   design (needs a pairwise-adjacent-threshold test). Book pd=2's verdict
   as rule-technical, pd=3's as genuine.
4. N=7-twin ceiling: for pd≥4 the gate's wall leaves the reachable nf set
   and the whole question goes inert — crossing maps are only meaningful
   for pd ≤ (N−1)/2.

### Follow-up
- Adjacent-threshold pairwise test (t100 = c vs c+1 for every crossing) to
  isolate per-crossing causal effect — settles pd=2's nf=4 crossing and
  gives a clean "causal level count" per pd.
- The +7.9pp nf=6 level at pd=3 is a NEW dial setting for healthy N=6
  grammars (kcoh5 family): sweep t100 ∈ [67..99] × K on healthy anchors;
  candidate best-practice θ for embedded = ~0.8·pd-side rather than 1.1.
- Plateau shoulder: fit pct vs m=N/(2pd+1) across all pd; if the collapse
  curve is a single function of m, the SPIN-23 tax and the wall unify as
  one law of m.

Status: **COMPLETE.** Committed+pushed g3-kinduction. WHEEL-LOG appended.
