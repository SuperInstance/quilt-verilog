# SPIN-35 — ADVERSARY × ECHO-GATE (θ-gate vs adversaries)

*Wheel spoke 2 (ADVERSARY), spin 35. Dispatched 2026-09-03, lane wheel_spin35_adversary
(zai/glm-5.3). Harness: spin35_adversary.py = spin11.run_adv clone + spin16 gate semantics
on the trig emissions (integer-exact 100·|pd−nf| > t100·pd). Not committed, not pushed.*

## VERDICT: **MIXED** (R=P, G=P, N=F per the pre-registered rule)

**Headline: the θ-gate IS a new adversarial surface — a single nf-inflating twin
moves collective residency by up to +17.3pp (kcoh5@15 K=2: 50.6% → 67.9%) — but the
leverage is strictly *stabilizing* (accidental rescue, never degradation), and the lie
is fully detectable: D5 flags every lied tick, ledger closure stays exactly 0, and
delivery-identity detectors never weaken.**

## Pre-registration

Hypothesis + decision rule committed in spin35_adversary.py's docstring before any run
(three arms: R = SPIN-11 replay gate-off; G = honest gate θ*=1.10 under the four
SPIN-11 adversaries; N = nf-inflate/deflate adversary). Falsifier clauses: gated
detection weaker than ungated, or any residency shift > 5pp vs baseline.

## Canaries (4/4 PASS — numbers count)

- **Ca**: adv=none gate=off byte-identical to `exp_glm1.run_fabric` (8/8 full-dict);
  SPIN-5 anchors exact: zero@15 K1 77.3 / ev 8756 / debt 187834; ladder@15 K1
  71.5 / 5792 / 106378.
- **Cb1**: gate=off ≡ spin11.run_adv full-dict for all 5 adversary modes.
- **Cb2**: honest gate 1.10 ≡ gate=off on all 3 N=6 grammars (structural CE inertness).
- **Cc**: double-run determinism 4/4.

## Arm R — SPIN-11 replay (gate off): PASS

All anchors reproduce exactly (±0.0pp): none 71.5/60.0, liar 13.2/12.6 (honestLocal
14.8/16.4), freerider dynamics byte-identical to none with closureΔ = −unpaid exactly
(27249 K1 / 53343 K2), jammer 26.0/27.9 (jam_amp = 28), mute 95.6/89.0.

## Arm G — honest gate θ*=1.10 under adversaries: PASS (20/20 byte-identical)

Structural fact confirmed: on N=6=2pd grammars at pd=3 an honest θ>1 gate **never
opens** — max |pd−nf| = 3 < 3.3 — so all four adversaries' gated runs are
byte-identical to gate-off on both ladder@15 and kcoh5@15 (K∈{1,2}). Detection
unchanged, residency shift 0pp. The kcoh5@15 detector table is new-booked: liar
4800/4800 band/peer, freerider closureΔ = −unpaid (74113/114293), jammer deadViol
1725/1769.

## Arm N — nf adversary: FAIL (per rule), the real finding

Twin 5 otherwise honest (emits, pays toll, honest claims) but lies to the gate's
nf input (inflate ×2 → nf 6 counted as 7 = 2pd+1, opening the otherwise-unopenable
gate; deflate ÷2 → its trigger uncounted):

| grammar | mode | K | mean% | base% | shift | gOpen | nfMis | closureΔ |
|---|---|---|---|---|---|---|---|---|
| ladder@15 | inflate | 1 | 71.1 | 71.5 | −0.4pp | 75 | 1550 | 0 |
| ladder@15 | inflate | 2 | 66.5 | 60.0 | **+6.4pp** | 86 | 1770 | 0 |
| kcoh5@15 | inflate | 1 | 82.1 | 74.1 | **+7.9pp** | 343 | 2967 | 0 |
| kcoh5@15 | inflate | 2 | 67.9 | 50.6 | **+17.3pp** | 679 | 3149 | 0 |
| both | deflate | 1,2 | =base | — | +0.0pp | 0 | 1547–3365 | 0 |

- (i) leverage bound ≤5pp: **VIOLATED** in 3/4 inflate cells (rule fail → MIXED).
- (ii) D5 declared-vs-emitted mismatch: fires every lied tick in every seed; zero
  false positives on honest arms. Detection is NOT evaded and NOT weakened.
- (iii) closure exactly 0 everywhere (toll is charged on the trigger error, not the
  gated pulse — the ledger is blind to the gate by construction); band/peer 0.

## Interpretation (post-hoc, labeled)

- The θ>1 half of the gate is **one-directional as an attack surface**: inflating nf
  can only *open* the gate (divide pulses, the MC-A rescue). Every cell moved
  *toward* rescue (or noise, −0.4pp). Deflating nf can only close a gate that is
  already closed at θ>1 — structurally inert, byte-proven here. The sub-1.0 half
  (t100<100, SPIN-24/25) where deflation could *dodge* compensation is untested —
  booked scar, needs its own spin.
- "Cannot gain residency" as written is false: a minority twin CAN move collective
  residency >5pp, i.e. can impersonate a 7-twin pile-up. But it cannot degrade, and
  it cannot hide: the emitted-pulse count per tick is fabric-verifiable against the
  declared nf (D5), so the lie is cheaply detectable. The honest-adversary baseline
  (Arm G) is untouched.

## Scars / honesty log

- Run 1 aborted on a print-format TypeError; fixed, no data affected.
- Run 1 booked ARM R "FAIL" and D5 "FAIL" from **comparison bugs in the verdict
  logic, not the fabric**: (a) freerider K=2 dynamics compared against a cached
  K=1 honest baseline; (b) D5 lied-tick counts compared across gate-on/gate-off
  dynamics, which legitimately diverge after the first gate-open. Both fixed
  (rule text unchanged); run 2 is the registered verdict. Raw run-1 evidence is
  in the conversation record; spin35-output.txt is run 2 only.
- My first clone missed the spin11 rule that a jammer twin emits *only* the constant
  pulse (no honest-trigger emission) — caught by canary Cb1 byte-mismatch before
  any number counted. Canaries did their job.
- kcoh5@15's honest baseline is weaker than expected (74.1/50.6) — the 5-zero cohort
  pile-up; that's exactly where the inflate adversary gains most.

## Deliverables

- spin35_adversary.py (harness, pre-registered docstring)
- spin35-output.txt (full run: canaries + arms R/G/N + registered verdict)
- Not committed, not pushed.
