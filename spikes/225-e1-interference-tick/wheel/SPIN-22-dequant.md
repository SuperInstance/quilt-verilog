# SPIN-22 — DEQUANT (§10 cheat-code probe): INTERFERENCE vs SEQUENTIAL at MATCHED BUDGET

**Spoke:** 8 (DEQUANT) · **Date:** 2026-09-03 ~14:57 AKDT
**Files:** `spin22_dequant.py`, `spin22-output.txt` (elapsed 1 s, ~150 fabric runs). Harness: inline canary-proven clones of `exp_glm1.run_fabric` interference and sequential arms, plus a new **SEQ-RR** arm (sequential round-robin, 1 read/tick). Integer-only in every loop; floats only at print. 5 seeds {1,7,42,1999,20260902}; `python3 -u` direct redirect; no pipes.

## Question (SPIN-dequant-2's top open edge, candidate (a))

The old interference-vs-sequential gap was measured at **unequal twin-evaluation counts** (interference reads all N=6 twins and applies up to 6 pulses/tick; the sequential baseline reads all twins but applies ≤1 impulse/tick). Does the interference advantage survive when sequential is given the **same sensor-read budget** (28,800 reads)?

**Budget definition (pre-registered):** 1 budget unit = 1 sensor read. INT: 6 reads/tick × 4800 t = 28,800. SEQ-EVERY (verbatim exp_glm1 sequential): 28,800 reads. SEQ-RR: 1 read/tick (twin t mod N) × 28,800 t = 28,800 — read- AND application-budget matched. SEQ-RR@4800 (4,800 reads) = low-budget anchor.

**Decision rules (pre-registered in script header BEFORE any panel):**
- DR1 SURVIVES: zero-grammar INT−SEQRR gap ≥ 3.0 pp for ≥3 of 4 K, AND best-INT − SEQRR ≥ 3.0 pp on ≥2 of 3 grammars.
- DR2 BUDGET-ARTIFACT: SEQRR ≥ best-INT − 3.0 pp on ≥2 of 3 grammars.
- DR3: efficiency (settles/1000 reads, mass/read) booked separately, no override. Threshold 3.0 pp = 2× typical 5-seed mean noise (~1.5 pp across SPIN-10..21).

## Canaries — ALL PASS

- (a) Byte-identity: inline INT and SEQ-EVERY clones vs `exp_glm1.run_fabric` raw-resid arrays, 4 configs × 2 seeds × 2 arms = **16/16 identical**.
- (b) Published anchors EXACT: zero K=1 = 77.3 / ev 8756 / debt 187834; ladder15 K=1 = 71.5 / ev 5792 / debt 106378 — both PASS, zero error.
- (c) Determinism: every arm (incl. 28,800-tick SEQ-RR) run twice, byte-identical.

## Results (5-seed means, stress fabric N=6 δ=12 drift=6 pd=3)

**Budget-matched gaps (INT − SEQ-RR@28800), pp:**

| grammar | K=1 | K=2 | K=4 | K=8 | best-K | INT best | SEQ-RR28 | SEQ-EVERY |
|---|---|---|---|---|---|---|---|---|
| zero | **−22.7** | −50.0 | −26.1 | −31.0 | −22.7 | 77.3 | **100.0** | **100.0** |
| ladder15 | **+3.9** | −7.6 | +2.9 | +3.1 | +3.9 | 71.5 | 67.6 | 62.6 |
| cohort33 | −3.9 | −19.9 | −31.5 | −31.5 | −3.9 | 49.3 | 53.2 | 53.6 |

- DR1 clause 1: 0/4 → FAIL. DR1 clause 2: 1/3 (only ladder15) → FAIL. **DR1 OVERALL: FAILS.**
- **DR2 BUDGET-ARTIFACT: YES.**
- DR3 (efficiency, matched 28,800 reads): sequential dominates everywhere — settles/1000 reads: zero 100.0 (SEQ-RR) vs 12.8 (best INT); ladder15 67.6 vs 11.9; cohort33 53.2 vs 8.2. Mass/read also ≥2× lower for sequential in every grammar. Interference loses on BOTH pct and efficiency at matched budget on 2 of 3 grammars.
- SEQ-RR@4800 ≈ SEQ-RR@28800 (zero 100.0/100.0; ladder15 67.8/67.6; cohort33 53.3/53.2): the "sequential gets N× the ticks" credit saturates — 1/6 of the reads already carries ~all of sequential's power on this fabric, because a hard snap against a triggering twin resets error to that twin's view instantly.

## VERDICTS (per sub-claim)

1. **"Interference beats sequential at matched read budget" — FALSIFIED.** DR1 fails both clauses. On zero grammar budget-matched sequential is *perfect* (100.0% vs INT's 77.3 best): a live twin + hard impulse is unbeatable, and interference's pulse-decay lag only costs. On cohort33 sequential wins by 3.9 pp. 
2. **"The old gap was an evaluation/application-budget artifact" — VALIDATED (DR2 YES).** Where interference was previously credited against sequential, the honest budget-matched comparison erases or reverses the advantage on 2 of 3 grammars.
3. **The one surviving pocket — MIXED, honestly booked:** ladder15 K=1 keeps a genuine **+3.9 pp** interference edge over budget-matched sequential (71.5 vs 67.6; also +8.9 pp over SEQ-EVERY). Mid-stagger grammars are where any twin alone is sometimes stale and the superposed staggered views genuinely add information a single hard snap can't. Under the pre-registered majority rule this does not rescue DR1 — the quantum-flavored claim shrinks to "a ~4 pp pocket in mid-stagger schedules," not a general interference advantage.
4. **Efficiency (DR3) — sequential dominates:** 4–8× more settles per read and ~2–6× less mass per read in every grammar. Interference's only wins are in absolute pct at ladder15, never in efficiency.

**Headline number: budget-matched sequential 100.0% vs interference 77.3% (zero grammar, best K) — the interference-vs-sequential advantage is DEAD at matched budget, surviving only as +3.9 pp at ladder15 K=1.**

## Mechanism note (post-hoc, labeled as such)

Sequential's hard snap sets g exactly to a triggering twin's read — error collapses to that twin's staleness in one apply. Interference pays e//3 now + geometric tail, so it is structurally slower per event; its historical pct wins came from grammars (or arms) where the sequential baseline couldn't exploit a fresh or adequate single twin each tick. Nothing here needs "amplitudes add": where interference still wins (ladder15), the credit is plausibly *information aggregation across staggered latencies* — exactly candidate (b)'s control (an N-sample mean at matched evaluations) should be run next to see if even the +3.9 pp pocket survives a mundane averaging explanation.

## Scars / boundaries

- **Dev bug (caught by canary b before any panel counted):** first version summed raw |resid| magnitudes as "settles" and compared anchor ev/debt as 5-seed totals — anchors are **per-seed means** (round). Canary gate refused to run panels until fixed. Lesson: anchor semantics (sum vs mean) must be pinned by probing `run_fabric` directly first.
- Budget = sensor reads only. Application cost (INT applies up to 6 pulses/tick vs sequential's 1 impulse) is NOT charged to INT — i.e., the falsification is conservative: charging apply-budget too would only widen sequential's win.
- SEQ-RR at 28,800 ticks takes 6× the drift/environment steps; the per-tick metric normalizes this, but it means sequential's advantage is not an artifact of seeing an easier environment per tick.
- Zero-grammar sequential = 100.0% is structurally guaranteed (live twin, first-priority, exact snap), so that cell is a floor, not a discovery; it still legitimately kills any interference-superiority claim there.
- 5 seeds; per-config seed spread on this fabric has historically been ≤ ~3 pp, and the threshold was pre-registered at 3.0 pp to be above it.

## Next spoke proposal

Run candidate (b) on the surviving pocket: ladder15 K=1, interference (+3.9 pp) vs an N-sample **integer-mean control** (snap-to-mean or mean-pulse at matched 28,800 reads). If the mean control matches INT within 3 pp, the last interference credit is variance reduction, not superposition — closing SPIN-dequant-2's open edge (b) and, with it, every §10 quantum-flavored claim on this fabric.

Status: **COMPLETE.** Not committed/pushed (per dispatch). WHEEL-LOG untouched.
