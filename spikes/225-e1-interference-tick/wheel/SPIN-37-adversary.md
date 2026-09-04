# SPIN-37 — ADVERSARY × SUB-1.0 DEFLATION-DODGE (θ-gate, the booked scar)

*Wheel spoke ADVERSARY, spin 37. Dispatched 2026-09-03, lane wheel_spin37_adversary
(zai/glm-5.3). Tests the scar booked in SPIN-35: the sub-1.0 half of the θ-gate
where deflation could bite. Harness: spin37_adversary.py = spin35 clone with
parameterized t100 + new nf_both mode. Not committed, not pushed.*

## VERDICT: **VALIDATED (H1)** per the pre-registered rule (A1=P, dodge=Y, S1=P, S2=P)

**Headline: at θ\*=0.90 the deflation-dodge is REAL and it is the mirror image of
SPIN-35's inflate attack — a single deflating twin suppresses ALL gate compensation
(gComp 444–4080 → 0 per seed, every cell) and drags collective residency DOWN by up
to −17.3pp (kcoh5@15 K=2: 67.9% honest-gated → 50.6%), exactly cancelling the
honest gate's rescue. Unlike inflate (stabilizing-only leverage), this attack
DEGRADES. D5 still flags every lied tick; ledger closure stays exactly 0.**

## Pre-registration

H1/H0, arms A1/A2/A3, decision rule, and verdict mapping committed in
spin37_adversary.py's docstring before any run (verbatim in spin37-output.txt).
Falsifier: deflation inert at all θ or shifts ≤5pp. H1 evaluated against the
honest-twin-at-same-θ\* baseline (correct null: same fabric, same gate, no lie).

## Canaries (4/4 PASS — numbers count)

- **Ca**: adv=none gate=off byte-identical to `exp_glm1.run_fabric` (8/8 full-dict);
  SPIN-5 anchors exact: zero@15 K1 77.3/8756/187834, ladder@15 K1 71.5/5792/106378.
- **Cb1**: gate="never" ≡ gate="off" full-dict for all 4 adv modes; gate=1.10 ≡ off
  for honest + nf_deflate (SPIN-35 inertness reproduces).
- **Cb2**: honest gate 1.10 ≡ off, 3 grammars × K{1,2} (structural CE continuity).
- **Cc**: double-run determinism 4/4 (includes θ*=0.90 arms).

## Arm A1 — SPIN-35 anchor-continuity: PASS (4/4 exact)

nf_inflate @ θ*=1.10 reproduces the published table to the decimal: ladder K1
−0.4pp, ladder K2 +6.4pp, kcoh5 K1 +7.9pp, kcoh5 K2 +17.3pp (tol ±0.2pp; hit ±0.0).

## Arm A2 — nf_deflate @ θ*=0.90: H1 CONFIRMED

| grammar | K | liar% | off-base% | honest90% | shift vs h90 | gOpen liar | gOpen honest | gComp liar | gComp honest* | closureΔ |
|---|---|---|---|---|---|---|---|---|---|---|
| ladder@15 | 1 | 71.5 | 71.5 | 71.1 | +0.4pp | 1067 | 75 | 0 | 444 | 0 |
| ladder@15 | 2 | 60.0 | 60.0 | 66.5 | **−6.4pp** | 793 | 86 | 0 | 564 | 0 |
| kcoh5@15 | 1 | 74.1 | 74.1 | 82.1 | **−7.9pp** | 2365 | 343 | 0 | 1968 | 0 |
| kcoh5@15 | 2 | 50.6 | 50.6 | 67.9 | **−17.3pp** | 1910 | 679 | 0 | 4080 | 0 |

*gComp-honest from a seed-1 forensic re-run (post-hoc evidence, labeled; the
5-seed gOpen means are in the output table).

- The leverage bound is **violated in 3/4 cells**, and this time in the
  *degrading* direction: deflation denies the honest fabric its pile-up rescue.
- Byte-proof of mechanism (seed 1, all 4 cells): the deflating twin's dynamics are
  **byte-identical to a gate-free fabric** — it doesn't just dodge its own
  compensation, it **unilaterally deletes the gate for the whole collective**
  (every 6-trigger pile-up it joins is declared 5, below the 0.90 open threshold).
- The liar's gOpen counter is high but degenerate: its only "opens" are
  declared=0 ticks (nf=1, its solo trigger), where neff=min(0,pd)=0 compensates
  nothing. gComp=0 is the true dodge metric — the pre-registered
  "liar gOpen < honest gOpen" detector missed it for this reason (see Scars);
  the effective-compensation check (gComp 0 < 444–4080) is the corrected evidence,
  consistent with the registered rule's intent ("dodge or slip").
- Honest θ*=0.90 gate opens exactly on all-6 pile-up ticks (75/86/343/679 per
  5-seed means) and lifts residency by the same magnitudes inflate faked at 1.10
  — the two halves of the surface are exact mirrors (+17.3 vs −17.3 at kcoh5 K2).

## Arm A3 — nf_both @ boundary θ*=1.00: rule-FAIL on 1/4, substance PASS

Both-direction twin (declared pushed away from pd) at θ*=1.00 is **exactly inert**:
gOpen=0, shift +0.0pp, byte-identical to gate-off in all 4 cells (nf≤pd→+1 can
never cross the |pd−nf|>pd threshold at θ*=1.00; nf>pd→−1 moves away from it).
Pure inflate @1.00 behaves as @1.10 (−0.4/+6.4/+7.9/+17.3). The registered rule
("both ≤ inflate + 0.2pp") fails only on ladder K1, where the inflate anchor is
−0.4pp of noise and both is exactly 0.0pp — a sign artifact of a noise cell, not a
gain for the adversary. Booked honestly as a rule drafting flaw; the substantive
claim (boundary adds nothing beyond inflate) holds in every cell.

## Secondary

- **S1 (D5 detection): PASS.** nfmis fires in every seed of every lying arm
  (1547–3365 lied ticks per seed across cells); honest arms carry no declared-
  nf channel, structurally 0 false positives. The dodge is fully detectable —
  same as SPIN-35: the lie can hurt but cannot hide.
- **S2 (ledger closure): PASS.** closureΔ = 0 exactly in every arm; toll logic
  remains blind to the gate (by construction), and band/peer detectors stay 0.

## Interpretation (post-hoc, labeled)

- The θ-gate is now a **complete two-sided adversarial surface**: inflate at θ>1
  fakes a pile-up to force the rescue open (SPIN-35, +17.3pp); deflate at θ<1
  hides a real pile-up to keep the rescue shut (SPIN-37, −17.3pp). At θ*=1.00 the
  two halves meet and a both-direction liar gains nothing — but each one-directional
  lie at its favorable θ is unbounded above 5pp by the same mechanism.
- Critical asymmetry vs SPIN-35: the sub-1.0 attack **degrades** residency
  (denies compensation), while the super-1.0 attack could only accidentally
  stabilize. If deployed, the gate's nf input must be fabric-audited (D5) —
  the emitted-pulse count per tick is verifiable against the declared nf, and
  this spin shows detection does not weaken at any θ.
- The honest θ<1 gate itself is a genuine rescue mechanism (it lifted kcoh5 K2
  from 50.6 → 67.9 honestly) — worth its own non-adversarial spoke.

## Scars / honesty log

- Run 1 aborted at canaries: my Cb1 wrongly demanded inflate@1.10 ≡ gate-off —
  but that non-identity IS SPIN-35's published finding. Canary corrected to
  the provable identities (never≡off all modes; 1.10≡off honest+deflate) before
  any experimental number was produced. Fabric unaffected.
- The pre-registered dodge detector ("liar gOpen < honest gOpen") is blind to
  degenerate neff=0 opens; the liar's gOpen is *higher* while its effective
  compensation is zero. gComp comparison is the correct detector. Rule text kept,
  verdict unchanged (H1 was confirmed via the >5pp shift clause regardless).
- A3's 1/4 rule-FAIL is a drafting artifact (noise-cell sign), documented above;
  verdict mapping did not depend on A3.
- Full-run wall time 4.1 s; no leg near the detach threshold.

## Next-spoke proposal

**SPIN-38 (ADVERSARY or FABRIC): D5-enforced gate.** Wire the declared-nf audit
into the gate itself — compensation paid only when declared nf equals the
fabric-counted trigger count that tick (or per-twin signed trigger receipts) —
and re-run the SPIN-35/37 attack matrix at θ*∈{0.90,1.00,1.10}. Prediction:
all leverage collapses to 0pp, honest θ*=0.90 rescue survives. Secondary
question worth booking: does requiring per-tick nf attestation introduce a new
collusion surface (twins cross-signing each other's lies)?

## Deliverables

- spin37_adversary.py (harness, pre-registered docstring, canaries)
- spin37-output.txt (full run: canaries + A1/A2/A3 + registered verdict)
- Not committed, not pushed.
