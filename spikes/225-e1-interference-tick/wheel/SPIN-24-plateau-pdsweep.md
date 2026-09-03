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
