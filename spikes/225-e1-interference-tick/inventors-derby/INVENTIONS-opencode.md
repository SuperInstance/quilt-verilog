# INVENTIONS — opencode (Inventors Derby, 2026-09-02)

Contestant: opencode (zai/glm-5.3). Read BRIEF.md, QTORCH-CHARTER.md (§1.2,
§6, §8–§10), README.md, e1.py, arena.py, all four RD dossiers, plus
DIVERGENCE.md / REGIME-META.md / VARIETY-LEDGER.md for the novelty check.

Method note: every experiment below is a self-contained Python port of the
e1.py tick (contract items 1–4 preserved), **validated against `e1.run()`
on integer counters (events/debt/cancellations/maxErr) before any arm was
run**. Integer-only, fixed seeds `(1, 7, 42, 1999, 20260902)`, percentages
reported as per-mille (‰) via `settles*1000//ticks` — no floats anywhere in
any loop. Scripts (scratch, not added to the repo):

- `/tmp/opencode/fringe.py` — invention 1
- `/tmp/opencode/cofire_trust.py` — invention 2
- `/tmp/opencode/zombie_audit.py` — invention 3
- `/tmp/opencode/quant_floor.py` — invention 4

Run any with `python3 <script>` (needs `e1.py` importable from the spike dir).

---

## 1. THE DIFFERENCE INTERFEROMETER — twin latency read off the fabric's own fringes

**Mechanism.** The interference arm's twin errors are two views of one wave:
`e1[t] = s(t) − g(t)`, `e2[t] = s(t−λ) − g(t)`. Their first differences
`d_i[t] = Δs(·) − Δg(t)` kill the shared g random-walk, leaving exactly two
coincidences: the shared drift step `Δg(t)` (same tick only) and the shared
reality wave `Δs` (at lag λ). So the integer scan
`D(L) = Σ_t d1[t−L]·d2[t]` is a Michelson interferogram in ℤ: a central
fringe (shared actuation+noise, L≈0) and a **path-difference fringe whose
seating point IS the twin's latency** (§9: each lag is a feeler blade; the
echo fringe is where the blade logs). No pulses need be stored beyond a
25-tick window of two integers per twin — the ledger already carries it.

**Experiment (ran, 5 seeds × 2 regimes).** Instrumented interference arm
(validated: events/debt byte-identical to e1.py on probed seeds), collected
d1/d2, scanned L ∈ 0..24 (stress) and 0..16 (gentle):

```
STRESS (lat2=10):  argmax over L>=2 = 10 on 5/5 seeds
  seed        1: D(0)=143085  D(10)=+49063  max(D(9),D(11))= -13204  -> READ
  seed        7: D(0)=145761  D(10)=+45411  neighbors             =  -7872  -> READ
  seed       42: D(0)=142824  D(10)=+48024  neighbors             = -13951  -> READ
  seed     1999: D(0)=144239  D(10)=+49592  neighbors             = -10488  -> READ
  seed 20260902: D(0)=148106  D(10)=+49360  neighbors             = -16065  -> READ
GENTLE (lat2=5):   argmax over L>=2 = 5 on 5/5 seeds (D(5)=+37..41k, neighbors −22..−26k)
```

10/10 regime×seed reads correct, with the echo fringe +45k..50k against
**negative** first side-lobes — contrast ≈ 60k–90k against a ±5k noise floor.
Cost: lmax×window integer multiply-adds, O(25·4800) per read; state: 2 ints
per tick in a 25-deep ring per twin.

**Failed variants (booked honestly).** (a) Raw signed pulse-stream fringes
(cofire counts vs lag) FAIL: trend common-mode dominates, argmax drifts to
L=18–24. (b) Snap-point onset fringes FAIL: common-mode g-wander couples the
twins at L≈3–4 (stress peak L=4, not 10; gentle L=6–7 vs true 5). Only the
*difference* interferogram isolates the path difference. The negative
findings are themselves the doctrine: **tick-time coincidence is actuation;
channel-time coincidence is sensation; you must difference to see the sensor.**

**Novelty claim.** Not in any RD dossier. Closest existing: REGIME-META.md's
detector classifies calm/conflict from debt/cancel counters (no latency
estimate); RD-BEYOND-UTM lane-9 proposes regime histogram classification
(proposed, not run); charter §9 supplies the feeler-gauge framing but never
applies it to sensor metrology. Reading a *parameter* (latency) off
interference fringes of the fabric's own state is new here, and it works in
the gentle regime where superposition is the *losing* actuator — metrology
independent of control mode.

---

## 2. LAGGED-COFIRE TRUST — the cell learns which twin to believe, at the fringe lag

**Mechanism.** Per-twin integer trust dial w ∈ 0..8 (init 4). Emission gated
by dial tier (≤1 mute, 2–4 half-magnitude pulse, ≥5 full). The update is pure
coincidence counting with **no error signal**: judge T2's claim at tick t
against T1's claim at t−λ (the SAME reality point — the reference arm of
invention 1): agree → w+1, disagree → w−1, lone claims → no evidence. A
persistently noisy twin is demoted to silence by the ledger's own history.
This is charter §1.2's cofire run for the first time on E1 — with the
twist that coincidence must be evaluated at the *measured channel lag*, not
the tick.

**Experiment (ran, fault model: T2 latent-10 + independent ±14 sensor noise).**

```
arm                          events   debt  cancel maxErr pm_read pm_true pm_T1
D clean-T2 static (ref)        2041  34995     70     39     830     830    910
A noisy-T2 static              3287  59653    207     46     576     670    766
B noisy-T2 cofire-trust        1065  18524     29     79     552     661    973
C oracle T1-only                831  13316      0     70     655     655    988
(pm_*: per-mille settles vs readings / vs true channel / vs trusted twin only)
```

The dial collapses T2 to mute by t≈100 on 5/5 seeds (lagged evidence
disagree:agree ≈ 5.4:1, e.g. seed 1: 289 vs 54; seed 1999 briefly re-admits
at t=600, re-demotes immediately — the dial is self-correcting).

**Honest mixed verdict.** Isolation works and pays where the ledger doctrine
says it pays: debt **3.2× lower** than static (18524 vs 59653), events 3.1×
lower, trusted-channel residency **97.3% vs 76.6%**. But the headline
both-twins metric does NOT reward it (552 vs 576‰): a muted twin still
defines half the settle criterion while contributing nothing, and the static
arm can buy residency on the noisy reading by chasing noise at 3× the cost.
Fault isolation is a debt/trusted-channel mechanism, not a deadband
mechanism. Also booked: **v1 (symmetric same-tick cofire/anti-cofire)
provably cannot discriminate** — both dials receive identical updates, so
w1≡w2 forever (ran it: w=(8,8) on 4/5 seeds, performance below static).
Lag structure is not decoration; it is what makes credit assignment possible.

**Novelty claim.** The cofire *primitive* is charter §1.2 doctrine (API
sketch, never run); no RD dossier runs trust learning on E1. RD-SPREADSHEET
notes the negative-space asymmetric update rule and q_hebb cofire as fabric
plans; VARIETY-LEDGER names "per-counterparty dial memory" as aspiration;
RD-SWARM cites partner-label memory externally. The runnable mechanisms —
lagged-reference cofire, tier-gated emission, and the w1≡w2 impossibility
result for symmetric rules — are new here.

---

## 3. THE ZOMBIE AUDITOR — invariants that catch the e1.c bug class in ONE substrate

**Mechanism.** DIVERGENCE.md's bug (wrong-end expiry → immortal pulses at
±1, ~293k counterfeit net-contributions per run) was caught by a
cross-substrate byte-diff. That gate needs a second implementation. Two
O(queue) integer invariants ride along with the tick instead:
**I1 liveness** — no pulse with life ≤ 0 may ever be summed into `net`;
**I2 toll cap** — a pulse may actuate g at most K times (per-pulse
contribution counter; toll > K = counterfeiting). Plus a mass-flow ledger
that closes exactly even in lawful runs: `emitted = decay_heat +
expiry_discard + resident` — an auditable conservation identity for the wave
(§1.1's "snap writes are booked" made quantitative).

**Experiment (ran).** Buggy arm reproduces e1.c-as-shipped in Python
(append-at-end, tail-trim; it reproduces DIVERGENCE.md's exact 25.8% collapse
for seed 20260902: 258‰).

```
FALSE POSITIVES (correct expiry, 5 seeds x {stress, default}): 10/10 CLEAN
  mass ledger closes EXACTLY every run, e.g. stress seed 1:
    emitted=-615 = heat -445 + discard -171 + resident 1
  default seed 20260902: emitted=+14 = heat 136 + discard -124 + resident 2

DETECTION (buggy expiry, stress):
  seed        1: I1 tick 13, I2 tick 14, metrics-only tick 500  (38x)
  seed        7: I1 tick 11, I2 tick 12, metrics-only tick 500  (45x)
  seed       42: I1 tick 13, I2 tick 14, metrics-only tick 500  (38x)
  seed     1999: I1 tick 13, I2 tick 14, metrics-only tick 532  (40x)
  seed 20260902: I1 tick  8, I2 tick  9, metrics-only tick 500  (62x)
```

Metrics-only detection = first tick a trailing-500-window residency falls to
≤700‰; its floor is the window itself (≥500 ticks). The audit reads the
counterfeit at tick 8–13, before performance telemetry can even report, in a
single substrate, with zero false positives across both regimes. Overhead:
one comparison per queue entry per tick (queue peaks at 2K entries).

**Novelty claim.** RD-SPREADSHEET R2 *proposes* a γ+η=C conservation monitor
for the RTL fabric (not run, different substrate); RD-SWARM's PROCTOR canaries
are judge-decoys against reward hacking (different failure class). Running
physics invariants against this spike's own recorded bug class — and getting
the exact mass-closure identity `emitted = heat + discard + resident` for
free — is new here. Honest overlap: the spirit is R2's; the instantiation,
the toll-cap invariant, and the detection-latency numbers are this entry's.

---

## 4. THE WAVE'S QUANTA FLOOR — how coarse can a pulse be before interference stops winning?

**Mechanism.** E1 emits unbounded pulse magnitudes `|e|//pulse_div`. The
hardware doctrine (AIMC optimal 3–4 bits/cell; Z₃ the unique group on
{−1,0,+1}; charter §6's ternary gear) says small finite alphabets are the
destination — so clamp the emitted magnitude to a cap (the blade thickness)
and sweep. This measures the actuator's resolution floor *on the interference
tick itself*, complementing lane-5's proposed-but-unrun bit-floor sweep on
reservoirs.

**Experiment (ran, stress regime, 5-seed means; impulse baseline pm 519‰ / debt 48397).**

```
 cap   alphabet  events   debt  cancel maxErr   pm   beats impulse?
   1    -1..+1     2814  53907    190     51   575   yes (residency only)
   2    -2..+2     2478  45600    176     49   687   yes
   3    -3..+3     2209  39154     70     48   771   yes
   5    -5..+5     2034  35169     59     48   824   yes (99% of full win)
   7    -7..+7     2026  34822     77     45   834   saturated
  11   -11..+11    2044  35039     71     41   830   saturated
  inf  unbounded   2041  34995     70     39   830   reference (validated identical)
```

The advantage saturates at cap≈5–7: a **3-bit pulse alphabet recovers 99% of
the full win** — the interference tick's own 3–4-bit floor, matching the
AIMC doctrine from the inside. The ternary edge survives but changes
character: sign-only pulses (m=±1, a literal Z₃ wave) still beat impulse on
residency (575 vs 519‰) with **more** cancellations (190 vs 70 — the coarse
wave cancels constantly) but *lose on debt* (53907 > impulse's 48397): below
~2 bits the trade inverts — residency is bought with ledger mass and event
count (2814 vs 2041). Coarse waves are cheap to store and expensive to run.

**Novelty claim.** Lane-5 of RD-PHYSICAL proposes a bit-floor sweep for
ESN/Ising couplings (not run, other substrate); the 3–4-bit optimality
results it cites are external (2604.26979). Instantiating the floor question
on E1's own pulse alphabet — including the ternary point and the
residency/debt inversion below it — is new here and directly sets the u-bit
budget for the ESP32 port (PORTING-NOTES.md's <1KiB lane).

---

## Cross-invention note

1 → 2 is load-bearing, not a coincidence: the fringe lag is what makes a
*reference arm* exist, and a reference arm is what makes local credit
assignment discriminative (symmetric coincidence provably cannot isolate a
fault). 3 is the same doctrine at the container level: liveness/toll are
"cofire audits" on the queue itself. 4 prices the whole stack in bits. All
four are §9's feeler gauges in different couplings: lag blades, trust
seatings, toll counts, magnitude quanta — every reading a boolean at a
quantum, every smooth curve anchored to logs.

— opencode, 2026-09-02, per BRIEF.md. Not committed. No files outside
`inventors-derby/INVENTIONS-opencode.md` and `/tmp/opencode/` touched.
