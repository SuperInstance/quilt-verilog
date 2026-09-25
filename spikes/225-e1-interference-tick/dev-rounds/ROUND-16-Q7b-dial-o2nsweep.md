# DEV ROUND 16 — Q7b: regime dial on the O2 contention N-sweep

Date: 2026-09-03 (AKDT). Branch `g3-kinduction`. Item: Q7b (round-14 dial ported to the
O2 N-sweep fabric with the F14 mag/C=1 gate LIVE at every N ∈ {2..8}).
Harness: `dev-rounds/q7b_dial_o2nsweep.py` → `q7b-dial-o2nsweep-output.txt`.

## PART 1 — Pre-registered BEFORE any comparison numbers (committed first)

### Hypothesis (as booked, before running)

The round-14 3-register regime dial (R1 = L̂ blade-fast, R2 = σ stress bit via κ-slow
confirm, R3 = β bursty bit via transient-hit rate) was built and tuned on the 2-twin O4
protocol (segmented calm→conflict→bursty with ADC glitches). Its contention-facing
machinery is the per-stream transient suppressor plus the F14 mag/C=1 sort. Hypothesis:
on the O2 contention N-sweep fabric (fixed calm/stress regimes, NO glitch segment, N
twins at spread latencies), the dial does **not** move the O2 contention wall — the wall
(raw sort win ≥2pp first clears at N=6, round 3/O2b: +4.5pp) is set by coherent
same-tick fan-out error, not by transient hits or regime params, so suppressor+sort
should be ≈ sort-alone. The alternative (to be located if it fires): the σ-driven param
outputs (K=1, pd=2, phase-decay, td=12) shift the wall the way per-twin lag compensation
moved the N=4 bundle wall (round 7/O7: 12.2%→86.3% trueRes).

### Porting decisions (pre-registered, gate-eligible)

- Fabric: `o2_contention.py`/`o2_boundary.py` verbatim base — 4800 ticks, calm
  (K=8, Δ=6, drift=3) / stress (K=4, Δ=12, drift=6), pd=3, seeds (1, 7, 42, 1999,
  20260902). N ∈ {2..8}; latency sets: N=2 (0,12), N=3 (0,6,12), N=4 (0,4,8,12)
  [NEW interpolation, pre-registered], N=5 (0,3,6,9,12), N=6 (0,2,5,7,10,12),
  N=7 (0,2,4,6,8,10,12), N=8 (0,2,3,5,7,8,10,12).
- DIAL arm (primary, gate-eligible): O2 switchboard loop with (a) mag/C=1 sort ALWAYS
  live at every N; (b) per-twin transient suppressor v1 spec — a twin's error is
  withheld from candidacy for one tick when its reading jumps ≥40 vs the previous tick
  (always active; β does NOT gate the suppressor — that was dial-v2, booked not
  gate-eligible in round 14); (c) registers: R1 blade per-twin (raw arm: discovery
  only; comp arm: compensation), R2 σ = (max discovered lag ≥ 8) OR κ-detector confirm
  (O4 Detector verbatim, fed tick debt / cancel flag net==0 with ≥2 pulses / snap),
  R3 β = ≥2 transient hits in last 16 ticks; stress_now = σ and not β → param outputs
  K=1, pd=2, phase-decay ON, td=12 (else regime defaults). The O4 sequential↔interference
  MODE switch is NOT ported: the O2 fabric is the interference switchboard by
  construction; porting the mode switch would replace the plant, not dial it. Logged as
  a porting scar.
- Attribution arm (secondary, not gate-eligible): "sort+supp" — suppressor + mag/C=1
  only, no σ param modulation (registers computed and logged, outputs inert).
- Unmodified arms: admit-all raw/comp, mag-C=1 raw/comp — these carry the anchor replay.

### Pre-registered decision rule

- Define win(arm) = %w(arm) − %w(admit-all, same N/regime/rawness); ADD(N) =
  win(dial) − win(sort-alone). %w = mean over 5 seeds (integer core; printed at 0.1pp).
- **PROMOTE** if ADD ≥ +2pp at some N ≥ 3 uncompensated (raw) while dial debt ≤
  1.10 × sort-alone debt at that N.
- **BOOK "dial inert on contention"** if |ADD| ≤ 0.5pp at every N (both arms, raw and
  comp).
- **LOCATE** otherwise: report the new N where the ≥2pp raw sort win gate first clears
  under the dial (raw and compensated).

### Canaries (pre-registered, mandatory)

1. Byte-identity: re-run the full N=6 cell (all arms) a second time; the printed table
   block must be byte-identical (hash compared).
2. Anchor replay: unmodified arms must reproduce round-2/O2 + round-3/O2b published
   numbers exactly — stress raw N=8: admit-all 57.8 / magC1 69.7 (+11.9pp); stress
   comp N=8: 42.7 / 98.9 (+56.2pp); stress raw N=6: +4.5pp wall; plus round-2 grid rows
   for N∈{2,3,5}.
3. Self-canary: run one dial cell with the σ register INVERTED (stress_now = (not σ)
   and not β) and label it "dial"; the comparison instrumentation must catch the
   mislabel (fingerprint differs from the true dial arm).

## PART 2 — Results (generated after PART 1 was committed; pre-reg commit dd19f18)

Runtime ~20 s CPU. Harness: `q7b_dial_o2nsweep.py`; raw log: `q7b-dial-o2nsweep-output.txt`.

### Canaries

1. **Byte-identity PASS** — full N=6 stress cell re-run, sha256 `a89326dc2e2262a6…` both runs.
2. **Anchor replay PASS 21/21** — every round-2/O2 and round-3/O2b published cell reproduced
   exactly on the unmodified arms (stress raw N=8 57.8→69.7 = +11.9pp; stress comp N=8
   42.7→98.9 = +56.2pp; stress raw N=6 65.2→69.7 = **+4.5pp wall**; N=2/3/5/7 and calm N=8
   rows all exact). Lag blade exact 35/35 twins across N∈{2..8}.
3. **Self-canary CAUGHT** — σ-inverted arm labeled "dial" differed in fingerprint
   (88.6%w/4344 stress-ticks vs 69.0%w/0 stress-ticks at seed 42, N=6 stress).

### Main grid (mean over 5 seeds; %w / debt / maxE)

| regime | N | admit-all raw | sortC1 raw | DIAL raw | admit-all comp | sortC1 comp |
|---|---|---|---|---|---|---|
| stress | 2 | 69.8 / 46968 | 69.8 / 43364 | **90.0** / 41025 | 98.5 / 17700 | 98.9 / 13317 |
| stress | 3 | 69.7 / 50396 | 69.8 / 43901 | 89.0 / 41420 | 95.6 / 29006 | 98.9 / 13317 |
| stress | 4 | 68.8 / 57080 | 69.7 / 44159 | 88.7 / 41561 | 86.3 / 64346 | 98.9 / 13317 |
| stress | 5 | 68.0 / 64864 | 69.6 / 44151 | 88.6 / 41634 | 74.8 / 135255 | 98.9 / 13317 |
| stress | 6 | 65.2 / 78295 | 69.7 / 44042 | 88.6 / 41313 | 73.9 / 170656 | 98.9 / 13317 |
| stress | 7 | 62.9 / 89190 | 69.7 / 44175 | 88.7 / 41405 | 61.3 / 294809 | 98.9 / 13317 |
| stress | 8 | 57.8 / 134134 | 69.7 / 44263 | 88.6 / 41450 | 42.7 / 676269 | 98.9 / 13317 |
| calm | 2 | 5.0 / 81385 | 4.9 / 58413 | 3.1 / 28456 | 71.8 / 29866 | 84.3 / 12210 |
| calm | 8 | 1.8 / 276511 | 4.1 / 59766 | 2.4 / 29718 | 31.7 / 455216 | 84.3 / 12210 |

Attribution arm (σ outputs inert, suppressor+sort only): sort+supp raw ≈ sortC1 raw within
±0.1pp everywhere (stress 69.7–69.8 all N; calm ±1pp); sort+supp **comp** = 83.8/98.5 =
−0.5pp vs sort-alone. **The suppressor is inert on this fabric** (38–152 suppressed ticks
per 4800; β set 76–456/4800 ticks — there are no transients to suppress, by construction).

### Decision table highlights (ADD = dial win − sort-alone win, pp)

- stress raw: ADD = **+19.0 to +20.2pp at every N∈{2..8}** (dial debt 41313–41634 vs sort
  43364–44263 — debt guard OK at all raw promote sites).
- calm raw: ADD = −2.0 to −3.1pp at every N (dial wins less / loses more).
- comp arms: ADD ≈ +0.1pp (stress) — dial ≈ sort-alone — but **debt guard BREACHED**
  (dial comp debt 15143–15963 vs sort 12210–13317, +20–24% > 10%).
- σ duty cycle: **4344–4724 of 4800 ticks "stress-confirmed"** in every cell, calm included.
  The κ-detector (O4-tuned) latches permanently in the O2 switchboard: net==0
  cancellations are native to the pulse plant, not a stress signature.

### Verdict

**PROMOTED — by the letter of the pre-registered rule; with two booked caveats that matter
more than the promotion.**

1. The rule fires: ADD ≥ +2pp at N≥3 uncompensated (in fact at every N) with debt within
   the guard at each promote site. Formally the wall moves from N=6 to N=2 — but that is
   **not a wall shift, it is a floor lift**: the +19pp is N-invariant, which is the
   signature of a static re-parameterization, not of contention arbitration.
2. **Attribution kills the mechanism story.** The suppressor + mag/C=1 sort combination —
   the contention-facing machinery this round was asking about — moves nothing (sort+supp
   within ±0.5pp of sort-alone, both arms, every N). The entire +19pp comes from the
   σ-driven param outputs (K=1, pd=2, td=12, phase-decay), i.e. running a gentler, more
   forgiving plant law, and it comes at −2 to −3pp in calm raw and a >10% debt breach on
   the comp arms. The O2 contention wall at N=6 is NOT moved the way per-twin lag
   compensation moved the O7 bundle wall.
3. **σ is regime-blind on this fabric** (90%+ duty even in calm): the round-14 dial's
   registers do not transfer to the O2 switchboard — the κ-detector's cancel flag means
   something different here. Booking: the dial is O4-protocol-bound; porting it requires
   re-deriving σ on switchboard-native telemetry.

**Booking:** do NOT promote the suppressor+sort combination (inert here). The dial's
param outputs deserve a separate, honestly-labeled round (they lift stress raw %w by
~19pp at lower debt — but that is a plant-law comparison, not a contention result, and
the calm regression + comp debt breach must gate it). T2 RTL note from round 3 stands
unchanged: the wall is at N=6.

### Honest scars

- The mode switch (sequential↔interference) was NOT ported — the O2 fabric is the
  interference switchboard by construction; porting the mode would replace the plant.
  This was pre-registered in PART 1 and is why the σ outputs reduce to param modulation.
- First draft of this script had two bugs caught before any number was booked
  (UnboundLocalError on cancel_flag; ModuleNotFoundError on e1 path) — fixed, rerun;
  no partial numbers leaked into the deliverable.
- N=4 latency set (0,4,8,12) is a NEW pre-registered interpolation (round 2/3 never ran
  N=4); its unmodified-arm cells have no published anchor — flagged, first cell of the
  N=4 column is anchor-less by design.
- The debt-guard text of the rule was written per promote-site; the comp-arm breaches
  (+20–24%) are reported here even though the rule did not require it.
- σ-invert self-canary produced stress_ticks=0 with %w 69.0 — i.e. the inverted dial
  collapses to sort-alone behavior, independently confirming attribution point 2.
