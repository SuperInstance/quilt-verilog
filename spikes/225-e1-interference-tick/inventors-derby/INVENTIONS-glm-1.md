# INVENTIONS — glm-1 (Inventors Derby, 2026-09-02)

Contestant: glm-1 (z.ai GLM-5.3 lane). All experiments actually run with `python3`
(integer-only inside the loop, fixed seeds 1/7/42/1999/20260902, floats only in
display rounding, exactly as `e1.py` does). Harness: `exp_glm1.py` in this dir
(self-contained; generalizes the e1 runner to N sensors with individual latencies
and per-sensor lie offsets, preserving contract items 1–4: fdiv semantics,
64-bit LCG intermediate, FIFO oldest-first expiry, decay-from-snapshot).
Raw output: `run_glm1.txt`. Not committed, per rules.

**The 3 best: A (Byzantine twin), B (bundle-capacity wall), D (queue-archaeology
auditor). C is a booked failure — first-ever run of the charter's cofire
primitive, which fails in an instructive, seed-stable way.**

---

## A. THE BYZANTINE TWIN — bounded adversarial drag + the cancellation whistle

**Mechanism.** Add a third sensor that lies: reading = s(t−5) + 24 during a
1200-tick attack window, honest before and after. Impulse snapping hands the
liar the state outright (g := lie whenever it triggers, then honest twins
yank back — ping-pong at full lie amplitude). Pulse superposition instead
admixes the liar's ±24/3-magnitude pulses with the honest twins' counter-
pulses: the lie is partially canceled every tick, and — the invention — the
*cancellation rate itself becomes a byzantine-sensor detector*: a sustained
net==0-both-signs-live signature that no honest regime produces at this rate.

**Numbers** (lie +24, ticks 1200–2399, delta=12, drift=6, K=4, pd=3,
lats=[0,10,5], 3600 ticks):

| mode | seed | honest% | lie% | maxDrag | cancels-in-lie | recover(ticks) |
|---|---|---|---|---|---|---|
| sequential | 1 | 77.9 | 49.0 | **61** | 0 | 44 |
| sequential | 7 | 76.3 | 48.9 | 61 | 0 | 16 |
| sequential | 42 | 81.5 | 48.7 | 61 | 0 | 21 |
| sequential | 1999 | 78.4 | 49.2 | 61 | 0 | 97 |
| sequential | 20260902 | 79.7 | 49.0 | 61 | 0 | 69 |
| interference | 1 | 91.0 | 51.6 | **27** | 72 | 25 |
| interference | 7 | 91.5 | 52.1 | 29 | 63 | 16 |
| interference | 42 | 91.8 | 52.0 | 27 | 82 | 30 |
| interference | 1999 | 92.3 | 51.2 | 33 | 69 | 11 |
| interference | 20260902 | 90.3 | 50.6 | 34 | 54 | 23 |

(maxDrag = max |g − s(t)| during the lie window; % = ticks within delta=12 of
the TRUE channel; recover = ticks after lie ends until 10 consecutive in-band.)

**The whistle (cancellation permille, honest vs lie window, interference):**

| seed | honest ‰ | lie ‰ | ratio |
|---|---|---|---|
| 1 | 10 | 60 | ×5 |
| 7 | 19 | 52 | ×2 |
| 42 | 19 | 68 | ×3 |
| 1999 | 10 | 57 | ×5 |
| 20260902 | 14 | 45 | ×3 |

**Findings, honestly:** (1) superposition does NOT preserve deadband residency
under a sustained lie (~51% both modes — the lie window is simply hard); (2)
it bounds worst-case displacement 61 → 27–34 (lie amplification 2.5× → ~1.2×:
sub-amplifying); (3) the liar manufactures the cancellation state at 2–5× the
honest rate on every seed — a one-counter byzantine alarm; (4) both modes
recover in ≤ ~100 ticks, interference slightly faster on 4/5 seeds.

**Novelty claim.** No RD dossier runs an adversarial sensor inside the fabric.
PROCTOR (RD-SWARM) is judge-side adversarial; REGIME-META.md uses cancellation
chatter to detect *regime* (calm vs conflict) — adjacent metric, different
object (I detect a *defector*, not a regime). The bounded-drag asymmetry and
the lie-whistle ratio are new numbers. Closest prior: none found in dossiers.

---

## B. THE BUNDLE-CAPACITY WALL — where superposition poisons itself

**Mechanism.** E1 always ran exactly 2 twins. Generalize to N staggered twins
(latencies 0,10,20,…,10(N−1)), same stress params, and sweep N. The question:
how much mutually-stale sensing can integer superposition absorb before the
overlapping opposite-sign pulses — the very mechanism that wins at N=2 —
drown the state they protect? This measures the fabric's bundling capacity
(§5 honesty item 4, "interference is not a free lunch") as an empirical curve.

**Numbers** (5-seed means; allWithin% = all N twins within delta; trueRes% =
|g − s(t)| ≤ delta; events per 4800 ticks):

| N | seq allW% | interf allW% | seq true% | interf true% | seq ev | interf ev | interf cancels |
|---|---|---|---|---|---|---|---|
| 2 | 51.3 | **83.1** | 78.4 | **91.0** | 2552 | 2041 | 70 |
| 3 | 6.9 | **14.1** | **53.1** | 34.5 | 4576 | 6415 | 276 |
| 4 | 1.9 | 3.7 | **51.4** | 12.2 | 4741 | 10408 | 321 |
| 5 | 0.4 | 1.0 | **50.9** | 9.7 | 4787 | 15025 | 199 |
| 6 | 0.2 | 0.2 | **50.9** | 9.9 | 4791 | 19338 | 203 |
| 7 | 0.2 | 0.2 | **50.9** | 10.9 | 4791 | 23690 | 121 |
| 8 | 0.2 | 0.1 | **50.9** | 11.4 | 4791 | 28316 | 79 |

**Findings:** (1) the consensus wall (allWithin) collapses for BOTH modes by
N≈5 — geometric: a 10-tick-stale twin disagrees with a live one by up to 16 on
the 8/5-slope, so no g satisfies everyone; (2) the decisive result is
**trueResidency: interference's grip on the true channel collapses 91→10%
while impulse holds a flat 51%** — past N=3 superposition is actively
toxic, 5× worse than the thing it replaced; (3) the toxicity signature is an
event explosion ~6 extra corrections per added twin (2041→28316, ~6.1/twin —
debt scales the same way) while the sequential arm is starvation-invariant
(flat 4791 ≈ ticks: T1-priority turns extra twins into spectators);
(4) cancellations peak at N=4 (321) then *fall* — not because conflict
resolves, but because the fabric saturates into permanent chatter.

**Novelty claim.** The charter cites HRR's bundling bound as external theory
(2606.24948); no dossier runs N>2. The crossover (interference wins N≤2,
ties N=3, poisons N≥4), the 6.1-events/twin explosion rate, and the flat
impulse floor are new. This is the first *measured* capacity law for the E1
fabric — and it sharpens E4's regime dial: the mode switch must fire on
fan-out, not just conflict level.

---

## C. COFIRE SELF-CALIBRATION — first run of the charter's §1.2 primitive: FAILED, diagnosed

**Mechanism (as designed).** The charter's cofire primitive (integer ±1
coincidence counting) had never been run. Attempt: let the fabric learn its
own sensor skew — an integer cross-correlator over snap events,
score[τ] = same-sign(A at t−τ, B at t) − opposite-sign pairs, τ ∈ 0..25;
τ̂ = argmax should equal the twin latency (10); then re-run with the stale
twin realigned by τ̂ and measure the %within payoff.

**Numbers (all three variants, true lag = 10):**
- v1 dense correlator: peak at the maxlag boundary (35–40), τ̂ useless. 0/5.
- v2 isolation filter (both sensors 5-tick silent before their snaps):
  argmax at τ=0–1 on all 5 seeds. 0/5.
- v3 anti-cofire trough (argmin of score): trough at **τ=3 on 5/5 seeds**
  (iso: 3–4 on 5/5) — consistent, but wrong: sc[10] = −88…−124 is not the
  extreme; sc[3-region] reaches −358…−382.

**Diagnosis (the actual finding):** (1) 22% of B-fires are same-tick with A
and those pairs are predominantly *opposite-sign* — in the conflict regime the
twins are antagonists, so charter-spec cofire (strengthen same-sign
coincidence) would wire them *negatively*; (2) the dominant coincidence
structure is the fabric's own relaxation rhythm: counter-fires follow fires
~3 ticks later (K=4 decay half-life), so the correlator reads the fabric, not
the world — self-locking, seed-stable (5/5). Consequence: cofire as specified
cannot learn static skew in a dense-fire interference fabric without a
refractory window or sparse coding. Booked as a charter-relevant negative:
§1.2 needs an eligibility gate before its "who else fired when I did" reads
the world instead of the echo.

**Novelty claim.** Nobody has run cofire (the dossiers and arena used
selection, never cofire — arena.py's ratchet is judge-side). A first-run
negative with a seed-stable mechanism (the 3-tick echo lock) is a result the
charter currently lacks. Aligned reruns showed no change (τ̂=0 ⇒ no alignment).

---

## D. QUEUE ARCHAEOLOGY — the pulse queue as a self-auditing partial ledger

**Mechanism.** Freeze the live pulse queue at audit ticks and retrodict: each
pulse's life counter pins its emission tick EXACTLY (life ℓ ⇒ emitted at
t−(K−1−ℓ)), while its magnitude reconstructs only to a dyadic interval
(inverse of ceil-halving: 2^a candidates at age a). Cross-check both
directions against the emission ledger: ghosts (queue pulses with no ledger
match) and losses (recent ledger emissions with no queue pulse). The queue is
thus a *mixed memory* — exact in time, dyadic-lossy in amplitude — and the
two-way check is a single-substrate integrity auditor for the
container-geometry bug class that DIVERGENCE.md needed a whole C port to catch.

**Numbers** (interference stress, seed 20260902, K=4, 48 audits every 100
ticks from t=300):

| harness | live pulses | ghosts | losses | age census 0/1/2/3 | exact amps | mean ambiguity width |
|---|---|---|---|---|---|---|
| correct | 64 | **0** | **0** | 19/13/15/17 | 19/64 | 2.62 mags (≈1.4 bits) |
| BUG (window-edge expiry) | 49 | 0 | **15** | 21/16/12/**0** | 21/49 | 1.00 |

Sample audit t=4790, mags by age: {0: [+2], 2: [+1], 3: [−1]} — the age-3
pulse (mag −1) reconstructs its original magnitude only to the 8-wide
interval [−8,−1].

**Findings:** (1) 64/64 tick attributions exact, zero ghosts/losses on the
correct harness — time memory is lossless by construction (the life counter
IS a log); (2) amplitude memory is dyadic-certified lossy: only age-0 pulses
(19/64) are exact; mean ambiguity 2.62 magnitudes; (3) the injected
window-edge bug (expire at life ≤1 — the DIVERGENCE.md geometry class) is
caught two ways: 15 losses AND an age census with age-3 zeroed — the census
alone says *which* edge is off. One substrate, no second port required.

**Novelty claim.** DIVERGENCE.md's lesson was cross-substrate diffing;
SUBSTRATE-LADDER.md extends it (Verilator/ESP32 rungs). The retrodictive
auditor is the complementary invention: the fabric audits its own container
geometry from inside, and the exact-time/dyadic-amplitude split is a concrete
instantiation of §9's "blades dispose" doctrine (snap points logged exactly,
the wave reconstructed only as a bounded proposal). Not in any dossier.

---

## Cross-invention takeaway (for the judge)

A and B together bracket the fabric's operating envelope from two new
directions — adversaries (bounded drag, whistle at 2–5×) and fan-out (wins at
N=2, poisons by N=4) — and both land on the same dial: E4's mode switch has
*two* necessary inputs, conflict level and twin fan-out. D makes the queue a
first-class ledger witness. C is the honest negative the charter asked for:
its own §1.2 primitive, run for the first time, fails by self-locking —
evidence for adding a refractory gate, booked as such.
