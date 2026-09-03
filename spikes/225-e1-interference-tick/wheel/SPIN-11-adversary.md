# SPIN-11 — ADVERSARY (liar / free-rider / jammer / mute in the N=6 fabric)

*Wheel spoke 2 (ADVERSARY). Dispatched 2026-09-03 ~07:43 AKDT, lane wheel_spin11_adversary
(zai/glm-5.3, run mode). Harness: exp_glm1.run_fabric contract, cloned as `run_adv`
(adv=None byte-identical to the parent — canary-proven).*

## Hypothesis (falsifiable, as briefed)

The fabric's invariants (debt/toll ledger closure, delivery identity, mass conservation)
DETECT and CONTAIN a minority (1-of-6) adversary twin:
- **(a) LIAR** (sign-flips its claimed channel reading) — caught by delivery-identity
  mismatch; damage bounded to its own cohort share.
- **(b) FREE-RIDER** (emits, never pays toll) — debt closure breaks identifiably;
  ledger delta = unpaid tolls.
- **(c) JAMMER** (constant max-amplitude emission every tick) — degradation no worse
  than the booked zero-lock/oscillation case (SPIN-5 zero@15 K=1: 77.3%); no leverage
  beyond incoherence.
- **(d) MUTE** (stops emitting) — equivalent to removing the twin; residency drop ≈
  linear in live-twin count; no cascade.

## Method

- Fabric: `run_adv()` = faithful clone of `exp_glm1.run_fabric` (fdiv decay, 64-bit LCG,
  FIFO oldest-first expiry, snapshot decay) + one `adv` hook on twin index 5.
  Integer-only inside every loop; floats only in display statistics (wheel precedent).
- Config: N=6 ladder grammar spread 15 (`lats [0,3,6,9,12,15]`), K∈{1,2}, stress
  (delta=12, drift=6, pd=3), 4800 ticks, seeds {1,7,42,1999,20260902}, adversary =
  exactly twin 5 (lat-15 stale end), majority honest = 5.
- Adversary semantics:
  - **liar**: claimed reading = −(honest reading) (sign flip; claims land at −400..−750).
  - **freerider**: identical trigger/emission behavior, toll waived (mass not charged).
  - **jammer**: one constant signed pulse every tick of amplitude A = max honest |pulse|
    over the 5-seed honest baseline (**A = 28**, fabric's own scale, K-independent);
    tolls paid in full; claims stay honest. No deadband respect.
  - **mute**: twin 5 neither emits nor counts (fully removed).
- Detectors (fabric-verifiable, no per-tick ground truth):
  - D1 band: claim outside the channel's own period range [400, 750] (contract constant).
  - D2 peer-distance: |claim − median(other 5 claims)| > 72 (= 2·spread·8/5 + 2·delta).
  - D3 deadband: emission while |claim − g| ≤ delta (honest-trigger impossibility).
  - D4 ledger closure: mass − Σ|trigger| over emissions (exactly 0 honest).
- Metrics: true residency permille (|g−s_true| ≤ 12), residency-per-event (rpe),
  events, debt, cancels, chatter, maxRes, per-twin toll subledger, honest-cohort local
  residency (5 honest twins' own reads vs g).

## Canaries (2/2 PASS — all numbers below count)

- **C1**: adv=none full-dict byte-identical to `exp_glm1.run_fabric`, 8/8 configs
  (ladder+zero × K{1,2} × seeds 1/20260902). PASS.
- **C2**: SPIN-5 anchor replay — zero@15 K=1: **77.3%**, ev 8756, debt 187834 (exact);
  ladder@15 K=1: **71.5%**, ev 5792, debt 106378 (exact). PASS (±0.0pp).

## EXP 1 — adversary sweep (ladder@15, per-seed permille)

| mode | K | s1 | s7 | s42 | s1999 | s20260902 | mean% | evMean | debtMean | canc | chat | maxRes | rpe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none | 1 | 709 | 713 | 721 | 714 | 717 | **71.5** | 5792 | 106378 | 4 | 3282 | 59 | 12.3 |
| none | 2 | 603 | 623 | 599 | 591 | 586 | 60.0 | 9481 | 259758 | 112 | 3526 | 98 | 6.3 |
| liar | 1 | 155 | 127 | 145 | 174 | 60 | **13.2** | 25413 | 7505059 | 7 | 4799 | 368 | 0.5 |
| liar | 2 | 155 | 84 | 141 | 133 | 119 | 12.6 | 25080 | 7564970 | 11 | 4799 | 570 | 0.5 |
| freerider | 1 | 709 | 713 | 721 | 714 | 717 | **71.5** | 5792 | 79129 | 4 | 3282 | 59 | 12.3 |
| freerider | 2 | 603 | 623 | 599 | 591 | 586 | 60.0 | 9481 | 206415 | 112 | 3526 | 98 | 6.3 |
| jammer | 1 | 258 | 262 | 259 | 262 | 258 | **26.0** | 21992 | 559780 | 84 | 4799 | 40 | 1.2 |
| jammer | 2 | 281 | 272 | 279 | 279 | 285 | 27.9 | 22074 | 572221 | 108 | 4799 | 58 | 1.3 |
| mute | 1 | 956 | 956 | 956 | 955 | 956 | **95.6** | 3339 | 58106 | 8 | 1371 | 45 | 28.6 |
| mute | 2 | 897 | 889 | 888 | 891 | 887 | 89.0 | 3685 | 68328 | 42 | 1475 | 54 | 24.2 |

## EXP 2 — detectors + forensics (5-seed means)

| mode | K | bandViol | peerViol | deadViol | unpaidToll | closureΔ | advTollShare | honestLocal% |
|---|---|---|---|---|---|---|---|---|
| liar | 1 | 4800 | 4800 | 0 | 0 | 0 | 49.8% | 14.8 |
| liar | 2 | 4800 | 4800 | 0 | 0 | 0 | 49.4% | 16.4 |
| freerider | 1 | 0 | 0 | 0 | 27249 | −27249 | 0.0% | 90.7 |
| freerider | 2 | 0 | 0 | 0 | 53343 | −53343 | 0.0% | 74.2 |
| jammer | 1 | 0 | 0 | 1863 | 0 | 0 | 24.0% | 27.3 |
| jammer | 2 | 0 | 0 | 1846 | 0 | 0 | 23.4% | 27.6 |
| mute | 1 | 0 | 0 | 0 | 0 | 0 | 0.0% | 96.6 |
| mute | 2 | 0 | 0 | 0 | 0 | 0 | 0.0% | 92.0 |

Ledger-closure identity holds exactly (0) for none/liar/jammer/mute; for freerider
closureΔ = −unpaid exactly, both K (K=1: −27249 = 27249; K=2: −53343 = 53343).
Zero false positives: honest twins and honest modes never trip D1/D2/D3.

## EXP 3 — mute equivalence + live-count ladder

- **Byte-identity PASS**: mute(6-lats) full-dict byte-identical to honest 5-twin
  fabric `[0,3,6,9,12]`, K{1,2} × 5 seeds (10/10).
- Live-count ladder (K=1, truncated ladder): 6→71.5%, 5→95.6%, 4→96.5%, 3→97.6%,
  2→98.7%. Events 5792→3339→2301→1882→1664; debt 106378→58106→39532→31072→26467;
  maxRes 59→45→38→32→34.
- No cascade: removing twin 5 lowers chatter (3282→1371 K=1), maxRes (59→45),
  cancels roughly flat (4→8).

## EXP 4 — liar/jammer containment (global truth vs honest-cohort local)

| mode | K | globalTrue% | honestLocal% | Δglobal vs none | Δlocal vs none |
|---|---|---|---|---|---|
| liar | 1 | 13.2 | 14.8 | −58.3pp | −76.0pp |
| liar | 2 | 12.6 | 16.4 | −47.4pp | −57.7pp |
| jammer | 1 | 26.0 | 27.3 | −45.5pp | −63.4pp |
| jammer | 2 | 27.9 | 27.6 | −32.1pp | −46.5pp |

(honest baseline local: 90.7% K=1 / 74.2% K=2, from the freerider run whose dynamics
are byte-identical to honest — verified by identical per-seed permille rows.)

## Verdicts

- **(a) LIAR: MIXED — detection VALIDATED, containment FALSIFIED.**
  Both delivery-identity detectors fire on 100% of the liar's emissions (4800/4800,
  band AND peer-distance) with zero false positives anywhere else. But damage is
  global, not cohort-bounded: honest-cohort local residency collapses 90.7→14.8%
  (−76.0pp vs a 1/6 ≈ 16.7% cohort share), global truth-residency −58.3pp, debt ×70
  (106378→7505059 — the liar pays ~half of all tolls, advTollShare 49.8%), maxRes
  59→368. Detection is total; containment is nil. The liar drags g to the
  sign-mirrored channel (≈ −s) and the honest majority spends its whole pulse budget
  fighting it every tick.
- **(b) FREE-RIDER: VALIDATED (clean).** Dynamics byte-identical to honest
  (per-seed permille exactly 709/713/721/714/717 — the freerider corrects honestly,
  so zero dynamic damage and zero detector flags), but ledger closure breaks by
  EXACTLY its unpaid tolls (−27249 / −53343, integer-exact both K) and the per-twin
  subledger attributes it (advTollShare 0.0% while emitting). The theft is purely
  financial and the ledger catches it to the unit.
- **(c) JAMMER: FALSIFIED (as bounded; direction honest).** Residency 26.0% (K=1) —
  51.3pp BELOW the zero-lock anchor (77.3%) and 45.5pp below its own honest baseline.
  The jammer gets real leverage beyond incoherence: a constant bias standoff (g parked
  above s where honest opposition balances the constant pulse). Nuance worth banking:
  maxRes stays SMALL (40 vs honest 59) — jammer damage is displacement, not divergence;
  and the deadband detector flags 1863/4800 = 38.8% of its ticks (fires inside the
  deadband — honest-impossible), so it is detectable, just not by delivery identity
  (its claims are honest; D1/D2 never fire).
- **(d) MUTE: MIXED — equivalence + no-cascade VALIDATED, drop-direction FALSIFIED.**
  Mute is byte-identical to removing the twin (10/10 full-dict), no cascade (chatter,
  maxRes, cancels all improve or hold). But residency does not drop — it JUMPS
  71.5→95.6% (+24.1pp): the removed twin was the stalest (lat 15), and SPIN-5's
  stale-mass law dominates any live-count linearity. Residency along the truncated
  ladder is monotone-increasing as stale twins leave (71.5/95.6/96.5/97.6/98.7), and
  rpe says the 5-live fabric is the most efficient of the family (28.6 vs 12.3).
  "Linear in live-twin count" is the wrong law on this grammar; staleness mass is
  the right one.

## Headline

**Detection is total, containment is nil: a 1-of-6 liar is flagged on 100% of its
emissions (4800/4800) yet still costs the honest cohort −76.0pp local residency and
×70 debt; only the ledger-borne adversaries (free-rider, mute) are exactly contained —
closureΔ = −unpaid to the unit, and mute replays the 5-twin fabric byte-identically.**

## Scars

1. **Mute implementation bug (caught by its own canary)**: first version silenced the
   ENTIRE fabric when adv=mute (mute row showed 8.4% / 0 events; the mute==removal
   byte-identity check FAILED 10/10). Fix: skip only the adversary's emissions.
   Lesson re-learned: the byte-identity canary is the experiment's immune system —
   it caught a semantics bug no scalar table would have.
2. **Peer-distance detector (D2) constant is config-coupled**: PEER_BOUND = 2·spread·(8/5)
   + 2·delta = 72 is valid only at spread 15 / delta 12; re-derive per config before
   reuse. Band detector (D1) is contract-constant and portable.
3. **Jammer amplitude grounded in the honest baseline** (A=28 = max honest |pulse|):
   results are amplitude-relative; a louder jammer scales the bias standoff, not the
   mechanism (untested beyond A=28 — booked as unmeasured).
4. **Liar seed-variance is wide** (60–174 permille at K=1) — single-seed readings of
   adversary damage are unreliable; the 5-seed mean is the bookable number.

## Proposed new spoke (one)

**TRUST-GATE / ADMISSION** — the detectors exist and are perfect; the fabric just
doesn't use them. Next spoke: gate emissions on delivery identity + deadband legality
(reject/ignore non-compliant pulses, or charge doubled tolls) and measure whether
gating restores honest-baseline residency under liar/jammer (and whether an adaptive
liar that stays inside the peer bound defeats the gate — the honest-looking adversary).
This is the charter's trust axis meeting the SPIN-5 grammar law where it broke.

*Files: wheel/spin11_adversary.py (driver), wheel/spin11-output.txt (raw). Not committed.*
