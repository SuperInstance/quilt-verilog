# SPIN-39 — SPOKE 2: ADVERSARY — Mixed-Strategy Evasion vs the θ-Gate + D5 Integrity

Date: 2026-09-04 · Work dir: `225-e1-interference-tick/` · Script: `wheel/spin39_adversary.py` · Raw output: `wheel/spin39-output.txt` (python3 -u, single pass, no pipes). Not committed/pushed.

Continuation of SPIN-35 (θ-gate holds vs classic adversaries; D5 declared-vs-emitted audit, 0 FP) and SPIN-37 (deflation not inert below θ=1; A3 boundary "leak" at θ*=1.00).

## Pre-registered hypothesis (docstring, written before any run)

- **H1**: a mixed-strategy twin — alternating inflate/deflate per trigger tick (`nf_alt`), LCG-random coin (`nf_rnd`), or exactly-2pd pile-up impersonator (`nf_2pd`, declared nf = 2·PD = 6; gate provably blind there since |PD−2PD|=PD and 100·PD > tc·PD iff tc<100) — evades the θ-gate AND the D5 audit in ≥1 grammar×K cell (>5pp **unflagged** residency shift). Falsified if every >5pp shift carries D5 flags.
- **H2**: the SPIN-37 θ*=1.00 A3 leak is a boundary artifact — gone by θ*=0.95 and θ*=1.05 (nf_both ≤ inflate + 0.2pp at both shoulders).

Decision rules fixed in the docstring before running (H1 via gate-off honest null ≡ honest@1.10 by canary Cb2; H2 via the two shoulders; S1 D5 flag-per-seed + structural 0 FP; S2 ledger closure).

## Canaries — ALL PASS

- Ca: adv=none gate=off byte-identity vs `exp_glm1.run_fabric`, 8/8 full-dict.
- Ca2: anchors zero@15 K1 77.3/8756/187834; ladder@15 K1 71.5/5792/106378 — exact.
- Cc1: SPIN-35 inflate replay @1.10: ladder K2 +6.4pp, kcoh5 K1 +7.9pp — exact.
- Cb1: gate=never ≡ gate=off full-dict for all 7 modes (incl. new alt/rnd/2pd). Cb2: honest@1.10 ≡ off, 3 grammars × K{1,2}.
- Cc: double-run determinism, 5 configs incl. mixed and 2pd arms.

## Arm A+B: mixed twin @ θ*=1.10 (5-seed means, gate-off honest null)

| mode | grammar | K | mean% | null% | shift | gOpen | nfMis/seed | closureΔ |
|---|---|---|---|---|---|---|---|---|
| nf_alt | ladder@15 | 1 | 71.5 | 71.5 | +0.0pp | 22 | 5/5 | 0 |
| nf_alt | ladder@15 | 2 | 4.2 | 60.0 | **−55.8pp** | 2251 | 5/5 | 0 |
| nf_alt | kcoh5@15 | 1 | 81.4 | 74.1 | +7.3pp | 156 | 5/5 | 0 |
| nf_alt | kcoh5@15 | 2 | 0.5 | 50.6 | **−50.1pp** | 2380 | 5/5 | 0 |
| nf_rnd | ladder@15 | 1 | 71.5 | 71.5 | +0.0pp | 22 | 5/5 | 0 |
| nf_rnd | ladder@15 | 2 | 5.0 | 60.0 | **−55.1pp** | 2228 | 5/5 | 0 |
| nf_rnd | kcoh5@15 | 1 | 81.4 | 74.1 | +7.3pp | 156 | 5/5 | 0 |
| nf_rnd | kcoh5@15 | 2 | 0.8 | 50.6 | **−49.8pp** | 2373 | 5/5 | 0 |
| nf_2pd | all 4 cells | — | =null | =null | +0.0pp | **0** | 5/5 | 0 |

Deterministic vs random patterning is indistinguishable (±0.7pp) — the harm is in the *mixed* structure, not the sequence.

## Arm C: θ* sweep, nf_both vs nf_inflate, ladder@15 K=1

| θ* | both shift | inflate shift | both−inflate | gOpen b/i |
|---|---|---|---|---|
| 0.90 | +0.0pp | −0.8pp | +0.8pp | 0/132 |
| 0.95 | +0.0pp | −0.8pp | +0.8pp | 0/132 |
| 1.00 | +0.0pp | −0.4pp | +0.4pp | 0/75 |
| 1.05 | +0.0pp | −0.4pp | +0.4pp | 0/75 |
| 1.10 | +0.0pp | −0.4pp | +0.4pp | 0/75 |

## Verdicts (pre-registered rules)

- **H1: FALSIFIED.** Every cell with >5pp shift is D5-flagged in 5/5 seeds (`nfMis/seed = 5/5` everywhere; honest arms structurally 0 FP). No unflagged manipulation exists in the model: any declared≠emitted tick is caught, and the only way to keep declared==emitted is to not lie.
- **H2: FALSIFIED — and recharacterized.** The both-vs-inflate advantage is NOT narrow: nf_both beats inflate by +0.4..+0.8pp at *every* θ* tested, because nf_both **never opens the gate anywhere** (gOpen-b = 0 across the whole sweep — its declared value always lands inside |PD−d| ≤ θ*·PD, closing openings honest pile-ups would earn at θ*≤0.95). But the effect is residency-inert on ladder K1 (+0.0pp at all θ) and fully D5-flagged (nfMis 1547/run). So SPIN-37's "A3 boundary leak" was not a boundary artifact; it was the first sighting of a *global dodge* that happens to be harmless here.
- **S1 (D5 under pressure): PASS.** S2 (closure): PASS, |Δ|<1 everywhere (runaway cells close exactly too).

## Headline

**A mixed alternating inflate/deflate twin collapses collective residency by −55.8pp (ladder@15 K=2; −50.1pp kcoh5 K=2) — 8.7× the worst SPIN-35 inflate cell — yet D5 flags every single lied tick in every seed: no evasion, no false positives.** The exactly-2pd impersonator confirms the gate's blind spot (gOpen=0) but is equally D5-visible and completely inert (+0.0pp in all 4 cells).

Mechanism of the crash (observed, not hypothesized): alternating lies let the liar *open* the gate on honest pile-up ticks (nf=6 → declared 7 → neff=3), dividing everyone's compensation by 3 exactly when full-strength pulses are needed; half-closed/half-opened compensation lets the drift random walk outrun correction and the mass ledger runs away (integer mass > 10^300; residency → ~4%). This required one harness-only fix: an integer display-mean (`imean`) because `spin11.mean`'s float division overflows on a genuinely diverged arm — fabric loop untouched, byte-identity canaries unaffected.

## Scars

- The θ-gate alone is a *safety* mechanism, not a *security* one: its division schedule can be weaponized by a declaration liar to suppress honest compensation far worse than inflation ever did (−55.8pp vs +17.3pp max). D5 is the only thing standing between the fabric and this crash — resilience now rests entirely on the audit's zero-miss record.
- Both-direction lying is a global gate-dodge (0 openings at every θ), not a θ*=1.00 boundary quirk; SPIN-37's A3 interpretation is superseded.
- Gate-blind ≠ harmless-proof: nf_2pd is the cleanest demonstration that D5, not the gate, is the actual detector of pile-up impersonation.
- Display-only float overflow on runaway arms: any future adversary spin must use integer means for mass/debt.

## Next spoke proposal (SPIN-40)

1. **Mitigation spoke**: does D5-triggered exclusion (liar's pulses quarantined once nfmis>0, or liar demoted to mute) neutralize the −55.8pp crash? Test on ladder@15 K=2, the worst cell, with detection→response latency swept {1, 10, 100} ticks.
2. **Evasion-lower-bound spoke**: prove (or break) the structural claim that D5 has no false-negative channel in this fabric — i.e., enumerate every path by which residency shifts without a declared≠emitted tick (e.g., timing manipulation: twin *withholding* honest pulses rather than lying about nf — the mute/free-rider axis SPIN-11 covered without a gate; re-test under the θ-gate).
3. K-dependence: the crash is K=2-only in these cells; sweep K∈{1..4} to find the compensation-half-life threshold where mixed lying flips from inert to runaway.
