# INVENTIONS — glm-2 (Inventors Derby, 2026-09-02)

**Assigned edge:** QTORCH charter **§9** (dialometer / feeler-gauge bank / snap
points) and **§10** (cheat-code claims) — *testable miniature versions*.
All experiments: integer-only, fixed seeds, actually run with python3 on this
box (0.5 s total). No floats in any instrument loop (exact integers /
stdlib `Fraction` only; one verification print cross-checks e1.py's own
float-rounded output). Scripts live beside this file:
`glm2_dialometer.py`, `glm2_dequant_walk.py`, `glm2_snapsearch.py`.

Novelty baseline checked against RD-BEYOND-UTM / RD-PHYSICAL-SUBSTRATES /
RD-SPREADSHEET-LINEAGE / RD-SWARM-SUBSTRATE, SYNOPTIC-MAP, VARIETY-LEDGER,
REGIME-META (grep: "feeler/dialometer/runout/snap point/dequantiz/cheat"
hits nothing outside the charter itself).

---

## 1. TWIN-RUNOUT DIALOMETER — the §9 feeler-gauge bank, run for real

**Mechanism.** Two codings of one channel — the E1 twins: T1 native, T2 the
late twin (latency 10). A dial λ ∈ [0,255] advances the late twin to
re-align the coupling. The true runout wave W(λ) = Σ|T1(t) − T2(t+λ)| is
*never read continuously*: the only legal readout is a feeler-gauge bank —
boolean pulls "does blade q fit the gap?", implemented as integer
accumulation with **early exit the instant the running sum exceeds q** (a
tripping blade never pays for the rest of the wave). The runout profile,
the seatings, and the joint diagnosis are reconstructed from the boolean
log alone; the continuous wave is computed once afterwards, purely to audit
the log. Machinist order: one coarse blade across the dial, fine blades
descended **only where the coarse blade seats**.

**Actual numbers** (`python3 glm2_dialometer.py`, window N=1440, dial 256
steps, wave cost = 368,640 adds):

```
GOOD COUPLING (rotation joint), two-stage:
  stage A: 256 pulls, 25,085 adds (6% of wave)
  stage B: +8 pulls, +11,520 adds -> total 36,605 adds (9% of wave cost)
  zero-seatings (blade 0 logs): [10, 250]   spacing: [240]
  boolean bracket audit at seatings (lower < W <= seated): True

BUG ARM (twin sensor on a 2x-coarse grid — the E1 v1 basis-bug class):
  total 27,272 adds (7% of wave)
  zero-seatings: NONE — true runout floor 720 (exactly the odd-value count)
  bracket audit: True

NAIVE BANK (full ladder at every dial step): 564,838 adds = 153% of wave
```

**Findings.**
- The boolean log alone discovers the twin latency (λ=10) **and** the
  channel period (second zero-seating at λ=250, spacing 240) — the period is
  a *relation across booleans*, never a continuous reading. §9's "the shape
  lives only in the relation across the booleans" is demonstrated, not asserted.
- **Joint-type diagnosis:** a rotation dial can seat a rotation joint
  (zero-seatings exist) but cannot seat a *scale* joint — the bug arm's
  runout floor is exactly the count of odd channel values in the window
  (720/1440). "A flat spot in the sweep means the misalignment is not the
  joint you're sweeping" — §9's phase-tells-you-which-joint claim, in integers.
- **Honest cost lesson (booked):** booleans per se save *nothing* — the
  naive bank pays **153%** of wave cost. The economy lives entirely in the
  search policy (coarse-then-fine, pay only at seatings): 9%. An instrument
  must be designed as a *procedure*, not as a data type.

**Novelty claim.** Nothing in the dossiers instruments §9; E1's
byte-identity gate is the special case "runout = 0 at one setting." This is
the first swept, cost-accounted, boolean-only runout instrument in the org,
and the rotation-vs-scale seating dichotomy is a new mini-result (floor =
odd-count is exact, not empirical).

---

## 2. DEQUANTIZED INTERFERENCE WALK — §10 cheat #2, quantified at two grains

**Mechanism.** The Hadamard quantum walk on a 193-site line, 96 steps — the
canonical system whose signature (ballistic two-lobe spread) is *pure
interference*. Three arms, all integer: **EXACT** — the walk's dyadic
numerators as exact big integers (after n steps amplitudes are
(integer)·2^(−n/2), so site probabilities are L²+R² over 2^(n+1): never a
float); **FABRIC** — the *same* signed-integer superposition recurrence
under a width cap: whenever max|value| trips the cap, every value halves
(toward zero, sign-symmetric) and odd values lose a half — quantized
cancellation, each loss logged; **CLASSICAL** — LCG coin walkers, the
no-interference null.

**Actual numbers** (`python3 glm2_dequant_walk.py`):

```
arm                TVD identity(ppm)  TVD 16-grain(ppm)  var/n^2(ppm)  var/n(ppm)
EXACT (reference)          —                   —            204990     19679065
CLASSICAL (null)           —                   —             10182       977481
FABRIC cap=2^20           13                  11            204987     19678844   rescales=27 losses=1566
FABRIC cap=2^10        16709               14040            202449     19435164   rescales=37 losses=1684

16-site-bin mass (ppm), exact vs fabric-2^10:
bin:     0      1      2      3   ...   9     10    11  12
exa:     0 217667 268127 129394  ... 58345  50825   0   0
fab:     0 222146 277689 129326  ... 57013  50018   0   0
```

**Findings.**
- The interference signature survives quantization remarkably well: at cap
  2^20 the fabric reproduces the exact histogram to **13 ppm at identity
  grain** after 27 rescales and 1,566 loss events; ballistic coefficient
  0.20499·n² vs classical 0.977·n (≈20× variance separation), and the
  interference-only left-lobe bias (48.5% vs 11.5%) reproduces within ppm.
- **Honest complication for the charter:** §10 says the cheat "lives exactly
  at class grain" (E7's law). Here the identity grain already holds at cap
  2^20 (13 ppm vs 11 ppm at 16-site grain — binning buys almost nothing),
  and at cap 2^10 grain helps only marginally (16,709 → 14,040). For
  *linear-superposition* substrates the quantization noise is diffuse, so
  the E7 grain law does **not** transfer as-is; it is a property of
  embedding-census substrates, not of interference statistics. The §10
  claim "quantized cancellation reproduces the wanted histogram" is
  *stronger than needed* here — worth booking before anyone over-generalizes
  E7 into §10.
- **Bonus bug, booked:** the classical arm first ran with a low-bit LCG coin
  and produced variance **0** across 20,000 walkers — the pinned contract
  LCG (odd multiplier, odd increment) has a **period-2 low bit**: parity
  alternates every call, so every walker walked the identical trajectory.
  Bit 11 used instead. Lesson: integer instruments must audit their own
  noise source; e1.py's `below()` with odd modulus mostly launders this, but
  any future coin/branch off the raw low bit inherits the degeneracy.

**Novelty claim.** RD-BEYOND-UTM treats groups/VSA theoretically; §10 cites
Tang's dequantization line as *positioning*. Nobody in the org has run an
integer-superposition fabric against an exactly-computed unitary object and
measured the distance at two grains. Honest scope note: the Hadamard walk
is classically simulable anyway — this tests the **fidelity** claim of
cheat #2 (statistics without amplitudes/unitarity), not any complexity
claim; §10's "no cheat for Shor" boundary stands untouched.

---

## 3. SNAP-POINT SEARCH ECONOMY — §10 cheat #1 as a certified blade oracle on the E1 judge

**Mechanism.** Question put to the judge: *minimal deadband Δ ∈ [4,24] such
that the interference arm holds ≥ Q% of ticks within deadband of both
twins (5-seed stress sweep, 4800 ticks each)*. The full wave costs
21×5×4800 = 504,000 ticks. The blade oracle answers only YES/NO per pull,
running the identical integer loop with **certified early exit**: settles
only accrue, so PASS is mathematically certain once 100·settles ≥ Q·TICKS
and FAIL once even all remaining ticks cannot reach Q — the bound itself is
the certificate; no full run is ever needed to trust a verdict. Seating =
binary search on Δ with blades (legitimate because the grid is verified
monotone); the log records what every pull actually paid.

**Actual numbers** (`python3 glm2_snapsearch.py`):

```
Q = 75:  binary seating trace: (14,True) (9,False) (12,True) (11,True) (10,False)
  seat delta* = 11; certificate pulls: seat=True, below-seat-fails=True
  pulls: 7, ticks paid: 43,060 -> 8% of the 504,000-tick wave
Q = 85:  seat delta* = 13, ticks 40,283 -> 7% of wave
verification grid (full wave, computed after): minimal delta = 11 (Q=75), 13 (Q=85)
  percent monotone nondecreasing in delta: True; blade seat agrees at both Q
dynamics cross-check vs e1.run at delta=12, 5 seeds: True (within 0.15pp display rounding)
```

**Findings.**
- "Never pay for the amplitudes, only for the landings" is quantified: the
  snap-point answer costs **7–8% of the wave**, with verdicts that are
  *stronger* than the wave's (certainty at pull time vs estimate at
  completion). Failing blades trip cheapest (Δ=9 pull: 8,548 ticks for 5
  seeds); passing blades pay up to their certified moment.
- **Booked instrument bug (v1):** my first early-PASS bound compared settles
  against *elapsed* ticks — one good first tick certified a pass (every pull
  "SEATS" in 1 tick, seat Δ*=4, 100% savings, beautifully wrong). The fix —
  anchor both bounds to the full horizon — is exactly the §1.5 judge
  doctrine in miniature: an oracle you can satisfy at t=1 is a self-canary.
  The derby keeps the scar: **elapsed-relative bounds are the boolean-oracle
  equivalent of harness tampering.**

**Novelty claim.** The arena/PROCTOR lane has canaries and holdouts but no
certified early-exit boolean oracle with a paid-ticks ledger; §9's "blade
slides until it logs" becomes a *search procedure* with a correctness
certificate. The v1 bug is itself a donateable failure class for the judge
chapter ("the optimistic-bound bug").

---

## Summary — the 3 best, with the numbers

| # | Invention | One-line result | Cost vs wave |
|---|-----------|-----------------|--------------|
| 1 | Twin-runout dialometer | zero-seatings [10, 250] → latency+period from booleans only; scale-joint floor = 720 (odd-count), no seating; bracket audit True | 9% (naive bank: 153%) |
| 2 | Dequantized interference walk | fabric ≡ exact to 13 ppm identity grain (cap 2^20); 1.67% at cap 2^10; ballistic 0.205·n² vs classical 0.977·n; E7 grain law does NOT transfer to linear superposition | (fidelity experiment) |
| 3 | Snap-point search economy | Δ*=11 @Q=75, Δ*=13 @Q=85, both agree with full grid; verdicts certified at pull time | 8% / 7% |

**Cross-cutting honest bookings:** (a) boolean-ness alone saves nothing —
procedures, not data types, carry the economy; (b) the E7 class-grain law
is substrate-specific, not universal — §10 should not lean on it for
interference statistics; (c) the contract LCG has a period-2 low bit —
audit every coin; (d) elapsed-relative early-exit bounds are a
self-canary failure class.

— glm-2 (zai/glm-5.3), Inventors Derby, 2026-09-02. Not committed, per rules.
