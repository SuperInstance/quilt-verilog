# ROUND 14 — Q7: minimal regime-gating dial (charter §5.4)

**Item:** Q7 (RESEARCH-AGENDA.md, open tier; charter §5.4 regime-gating mandate).
Branch `g3-kinduction`. Date: 2026-09-03. Lane `dev_q7_regime_dial`.
Harness: `dev-rounds/q7_regime_dial.py` (reuses `o4_regime_motion.py` arms,
protocol, κ-detector, and live blade VERBATIM; `e1.py` LCG/reality lineage;
integer-only, no multiply anywhere in the control path — shifts/adds/compares
only). Output: `dev-rounds/q7-dial-output.txt`.

---

## PART 1 — PRE-REGISTRATION (committed before any comparison run)

### Hypothesis

A minimal integer controller mapping observable state {κ-detector output,
lag-blade estimate L̂, fan-out N} (+ one transient-hit sensor, see below) to
config {mode, K, pd} exists with **3 integer registers and no multiply**, and
clears BOTH O4 gates that the O4 κ-dial alone failed:

- (a) **%w ≥ 932‰** (beat O4 adaptive), and
- (b) **debt ≤ 32,770** (60% of best-static seq-comp-oracle 54,616 — the gate
  O4 failed at 57,136), and
- (c) **L̂ knife-edge**: no dial arm may degrade >5pp vs its L̂-aligned twin
  (O4 scar: bursty sequential L̂=9→994‰, L̂=10→336‰).

on the same calm→conflict→bursty protocol (4800 ticks × 5 seeds, shifts at
1600/3200, unknown to controllers), same 6 static arms + O4 adaptive arm as
baselines, re-run verbatim from `o4_regime_motion.py`.

### Why O4 failed and what changes (mechanism, pre-registered)

O4's booking decomposed the failure into three causes; the dial is designed
against each:

1. **90-tick κ-detector entry lag** (debt-climb window must fill ~11× while
   the regime hurts). Fix (task doctrine): the **lag blade is the fast path** —
   L̂ jumps 5→10 at the conflict shift and seats within one 480-tick refresh;
   κ is demoted to **slow confirm** (bridge before the first post-shift blade
   refresh). Bursty is detected FASTER than both by a **transient-hit sensor**
   (below), since bursty = calm deltas + ±45 single-tick ADC glitches.
2. **Debt is a floor under bursts at Δ6**: every ±45 glitch is answered
   tick-for-tick (~90 debt per glitch event: chase out + chase back), ~36k of
   the 54.6k best-static debt. Fix: a **single-tick transient suppressor** on
   the aligned streams — a genuine per-tick reading change is ≤2 (reality
   slope) ± alignment shift at blade refresh (≤ ~10); any aligned single-tick
   jump ≥ 40 can only be a glitch, so that stream's trigger is suppressed for
   one tick. This is an *admission* filter on triggers (per-stream, one tick,
   no deferral queue — F16's deferred-admission failure mode is avoided
   because nothing is ever admitted late; the tick is simply skipped and g
   keeps drifting ≤3). Known coupling, booked up front: **threshold 40 is
   informed by the pre-registered ±45 glitch magnitude** (REGIME-META E4.E
   shape, characterized in round 4); robustness probed at glitch mag 60 and 20.
3. **L̂ knife-edge** (exact alignment is glitch-coherent and kills sequential
   in bursty): the transient suppressor removes the mechanism — whether twins
   glitch on the same aligned tick (L̂ exact) or split ticks (L̂±1), each
   stream's jump is ≥40 and suppressed individually. Gate (c) tests this
   directly at forced L̂±1.

### Dial spec (3 registers, integer, no multiply)

| Register | Meaning | Source | Update |
|---|---|---|---|
| R1 = L̂ | lag-blade estimate, 0..15 | O4 live blade (`discover_lag_obs`, sign-clipped, verbatim) | every 480 ticks from t=480 |
| R2 = σ (stress bit) | regime estimate | fast: L̂ ≥ 8 → 1; slow confirm: κ-detector CONFLICT → 1 | per tick (OR of fast/slow) |
| R3 = β (bursty bit) | transient regime | ≥2 transient hits in the last 16 ticks (16-slot integer window) | per tick |

Sensor front-ends reused from O4 organs (not counted as dial registers, since
O4 already paid for them): the κ-detector's own windows, the blade's
cross-correlation, the 480-tick observation history, and a 16-slot transient-hit
window (same idiom as the detector's cancel window).

**Outputs {mode, K, pd, td} (all integer compares/selects):**

- `mode` = interference iff (σ=1 AND β=0), else sequential. (Bursty forces
  sequential at Δ6; conflict holds interference per O4/E4 doctrine; the
  compensator+filter make sequential dominant everywhere else — O4's booking.)
- `K` = 1 when interference (O1 champion axis: K small under stress), inert
  under sequential.
- `pd` (pulse_div) = 2 when interference (O1 champion), inert under sequential.
  Phase-decay doubling (O5, promoted +2.0pp stress) ON when σ=1 AND β=0.
- `td` (trigger threshold) = 12 iff (σ=1 AND β=0), else 6. (Tracks the
  environment's Δ; bursty's Δ is calm-like and β is what distinguishes it —
  L̂ cannot, both conflict and bursty sit at lag 10.)
- Compensation: fresh twin delayed by L̂ (O4 live-realizable frame, verbatim).
- Transient suppressor: per aligned stream, |jump vs previous aligned reading|
  ≥ 40 → suppress that stream's trigger this tick, log a hit.
- **F14 sort gate**: when fan-out N ≥ 6 and >1 trigger is live, admit only the
  single largest-|e| trigger (mag key, C=1 — rounds 2/3: wall at N=6, +11.9pp
  raw/+56.2pp comp at N=8). At this round's N=2 it is **inert by design**;
  verified by (i) rejected-count == 0 on all dial runs and (ii) a unit check
  that the gate selects argmax|e| on a synthetic N=6 candidate set.
- No multiply anywhere in the dial path (correlation blade is O4-reused;
  inside the dial: adds, subtracts, compares, //2 halving only).

### Arms

Baselines (verbatim `run_arm`): seq-raw, int-raw, seq-comp-fix, int-comp-fix,
seq-comp-oracle, int-comp-oracle, adaptive — 7 × 5 seeds.
Dial arms: `dial` (live), plus booked probes (not gate arms): `dial-Lm1` /
`dial-Lp1` (forced L̂±1, whole run — gate (c) arms), `dial-nofilter`
(suppressor off — shows the knife-edge returns and that the filter is
load-bearing), `dial-g60` / `dial-g20` (glitch magnitude 60/20 — threshold
coupling probe). All 5 seeds each.

### Decision rule (pre-registered)

PROMOTE iff ALL of:
1. mean %w (dial) ≥ 932‰;
2. mean debt (dial) ≤ 32,770;
3. knife-edge: min(pm(dial-Lm1), pm(dial-Lp1)) ≥ pm(dial) − 50‰ AND
   bursty-seg pm at L̂±1 ≥ aligned bursty-seg pm − 50‰;
4. canaries pass: (i) double-run byte-identity; (ii) O4/F19 anchor replay —
   adaptive mean 932‰/57,136, int-comp 984‰/17,700/28, seq-comp 1000‰, blade
   exact on 3/5/7/10/15; (iii) mislabeled-arm self-canary CAUGHT (inverted
   dial must be caught by the mode-doctrine checker; filter-off arm passed
   off as full dial must be caught by fingerprint).

If the debt gate fails again: book WHICH register saturated / WHICH input
misled (per-segment debt telemetry is recorded for exactly this). If an anchor
fails to replay: STOP, commit failure analysis, no verdict.

— end PART 1 (pre-registration; comparison runs begin only after this is committed)

---

## PART 2 — RUNS, VERDICT (comparison runs began only after PART 1 commit a02a84b)

### Canaries (all PASS/CAUGHT)

| Canary | Check | Result |
|---|---|---|
| 1 (F14 gate units) | N=6 synthetic 6-candidate set → keeps argmax|e|=44, rejects 5; N=2 inert (keeps all, rejects 0); rejected==0 on every dial run | PASS |
| 2 (O4/F19 anchors) | blade 3/5/7/10/15 exact; adaptive replay **932‰ / 57,136** exact; F19 int-comp 5-seed mean 984/17,700/28 exact; seq-comp 1000‰ exact | PASS |
| 3 (self-canary) | inverted-dial "dial": calm-seq 49 vs calm-int 1551 → CAUGHT; filter-off arm faked as dial: fingerprints (801,13393,1135) vs (932,104046,0) → CAUGHT | CAUGHT |
| 4 (byte-identity) | dial + adaptive × 5 seeds run twice, full metric signatures identical | PASS |

Scar (honest bookkeeping): the first run's F19 anchor canary FAILED — my port
compared a single seed (20260902: 984/17,352/27) against the published 5-seed
mean (984/17,700/28). Canary bug, not a harness drift: fixed to 5-seed means,
then exact. No verdict-relevant number was touched by the fix.

### Baselines (O4 `run_arm` verbatim replay — identical to round 4)

seq-raw 266‰/87,152 · int-raw 371‰/105,027 · seq-comp-fix 636‰/59,686 ·
int-comp-fix 422‰/81,193 · **seq-comp-oracle 778‰/54,616 (best static)** ·
int-comp-oracle 545‰/80,320 · **adaptive 932‰/57,136**. All exact vs round 4.

### Dial arms (5 seeds, mean; seg pm calm/conflict/bursty; seg debt c/cf/bu)

| Arm | pm | debt | seg pm | seg debt | notes |
|---|---|---|---|---|---|
| **dial** (pre-registered) | **800‰** | **13,211** | 867/992/541 | 3,980/6,641/2,590 | 2 switches/run; 1,136 suppressions |
| dial-Lm1 (forced 9) | 578‰ | 13,343 | 183/991/562 | — | calm misaligned (true 5) |
| dial-Lp1 (forced 11) | 478‰ | 14,200 | 149/991/296 | — | bursty craters too |
| dial-nofilter | 932‰ | 103,562 | 870/996/929 | 3,946/6,682/92,933 | = O4 adaptive class; knife-edge returns |
| dial-g60 | 800‰ | 13,286 | 867/992/541 | — | threshold 40 robust at mag 60 |
| dial-g20 | 909‰ | 47,633 | 867/992/867 | —/—/37,012 | ±20 slips the filter (coupling booked) |
| dialv2 (β-gated chase, latched) * | 922‰ | 56,089 | 867/992/907 | 3,980/6,641/45,468 | 68 sw: (3/4)^32 latch leaks |
| dialv2-flap (unlatched) * | 906‰ | 51,157 | 867/992/858 | — | β flaps → 196 mode switches |
| dialv2-Lm1 / -Lp1 * | 742‰ / 488‰ | — | —/991/966 and —/991/315 | — | knife-edge alive under chase |

\* post-hoc amendment arms, run AFTER the pre-registered numbers were seen;
labeled, not gate-eligible (Q4-round precedent: "falsifier fires on the letter,
amendment conducts").

### Decision rule, applied (pre-registered)

- Gate a: dial 800‰ ≥ 932‰? **FAIL** (−132‰).
- Gate b: dial debt 13,211 ≤ 32,770? **PASS** — **the first arm in the program
  under the debt gate**: 24.2% of best-static debt (54,616), 23.1% of adaptive's
  (57,136).
- Gate c: L̂±1 578/478 vs 800−50 allowed? **FAIL** (dominated by forced-wrong
  calm lag; bursty-specific: 562/296 vs 541 — even the suppressor degrades
  245‰ at L̂+1).

**VERDICT: BOUNDARY BOOKED.** Not promoted; not refuted (gate b is a real
first). Output: `dev-rounds/q7-dial-output.txt`.

### The boundary, with numbers

1. **The transient suppressor is a debt cure AND a %w killer.** Suppressing
   single-tick ≥40 aligned jumps cuts total debt 57,136 → 13,211 (−77%) and
   bursty debt 18,586 → 2,590 per seed — but unanswered ±45 ticks are
   unsettled *by construction* (the reading itself is 45 off; only chasing —
   g += e within the tick — can settle a glitch tick). Suppressed bursty caps
   at 541‰ vs chased 929‰. Gate a and the suppressor are enemies.

2. **Gates a+b are *almost* jointly satisfiable — by β-gated chasing.** Chase
   debt concentrates in bursty (92,933/5 = 18,586/seed) while suppressed
   calm+conflict cost only 10,621 → ideal gated-chase total ≈ 29,207 ≤ 32,770
   with pm ≈ (867+992+929)/3 ≈ 929‰ — **3‰ short of gate a**. The measured
   latch variant lands 922‰/56,089 (a (3/4)^32-per-tick latch leak flaps the
   mode 68×/run; each leak window chases at Δ12/interference). No register
   saturated; the binding input is the bursty environment itself.

3. **Gate c is structurally incompatible with gate a.** Every ≥929‰ arm
   chases glitches; chasing is alignment-sensitive by mechanism (O4 scar,
   replicated here: dialv2 bursty 907‰ at live L̂, 315‰ at L̂+1; dial-nofilter
   929 vs O4's 336 at exact alignment). The only ±1-stable strategy family
   (suppression) caps at 800‰. The three gates jointly demand *chase* (settle
   glitch ticks), *don't pay* (debt), and *be alignment-blind* (knife-edge) —
   **any {mode,K,pd} dial at N=2 can pick two.** The 932‰/debt-32,770/±1-stable
   corner does not exist on this protocol; O4's adaptive sat on it only by
   alignment luck (the L̂=9 underseat).

4. **Threshold coupling (booked, pre-registered):** the ≥40 suppressor is
   informed by the known ±45 magnitude — robust at 60 (identical pm), slips at
   20 (909‰, debt 47,633, only 24 suppressions fire). A field dial needs the
   threshold tied to a measured noise scale, not a protocol constant.

### What the dial got right (reusable bookings)

- Blade-as-fast-path + κ-as-slow-confirm works as tasked: 2 switches/run vs
  O4's 6; conflict seg 992‰ with no 90-tick detector hole visible at permille
  resolution (κ bridges [1600,1920) before the blade's first post-shift seat).
- Bursty detection by transient-hit rate (R3) is faster than both the κ-detector
  (round 4: ~7 ticks re-entry) and cheaper than lag inference (L̂ cannot
  distinguish conflict from bursty — both sit at lag 10; the transient rate can).
- Calm 867‰ ≈ O4 oracle-class (1000‰ post-blade; the first 480 ticks are
  uncompensated by spec — the residual deficit is the blade's seat time, not
  the dial).
- F14 mag/C=1 gate verified inert at N=2 (rejected=0 everywhere) and correct
  at N=6 (unit canary); its contention payoff remains untestable on the 2-twin
  protocol — needs the O2 fabric at N≥6, queued as follow-up.

### Follow-ups queued

- Q7b: dial on the O2 N-sweep fabric (N∈{2..8}) where the F14 gate is live —
  does the suppressor/sort combination move the O2 wall the way compensation
  moved the N=4 wall?
- Q7c: gated-chase with a leak-proof latch (release on 128+ quiet ticks or
  never within a segment) — projected ≈929‰ @ ≈29.2k debt; still fails gates
  a and c; worth one run to pin the frontier endpoint, not to promote.

## Headline number

**Pre-registered 3-register dial: %w 800‰ @ debt 13,211 vs gates 932‰/32,770 —
first arm under the debt gate (24% of best-static; adaptive was 104%), but the
gates are jointly infeasible at N=2: chasing settles bursts (929‰) but is
alignment-sensitive (L̂+1 → 315‰), suppressing is alignment-stable but leaves
bursts unanswered (541‰) — any {mode,K,pd} dial picks two of three.**
