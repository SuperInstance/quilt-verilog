# SPIN-49 — ADVERSARY (wheel spoke 2, attempt 2): D6 EMISSION-CHANNEL PROVENANCE

Executed per the pre-registered brief in `WHEEL-LOG.md` (## SPIN-49-ADVERSARY).
Attempt 1 lane died with zero output (INCONCLUSIVE booked); attempt 2 staged
`spin49_adversary.py` BEFORE any panel run.

- Script: `wheel/spin49_adversary.py` (pre-registered docstring header written before any run)
- Output: `wheel/spin49-adversary-output.txt` (`python3 -u` redirect, no pipes) + appended, clearly-labeled post-hoc sensitivity block
- Harness provenance: imports/extends `spin47_adversary` (`run_coal`, `stats47`, `COAL`) on `spin39`/`spin11`/`exp_glm1` — same wheel dir, verbatim fabric dynamics.
- Not committed to git.

## D6 mechanism (booked pre-run)

Egress pulses carry `(src_id, seq)` where `seq` is the source cell's monotone emission counter; ingress verifies `seq == counter[src]`, drops mismatches before fabric entry, books them to a D6 ledger. A spoofer doesn't hold the honest cell's counter state, so its attestation lags — dropped. Arm-B quota: per-cell per-epoch (50 ticks) cap Q on extra self-attributed emissions, drops priced to the emitter's ledger; trigger-declared traffic never quota-dropped. Pre-registered Q = max honest per-cell per-epoch emission envelope + 2 (= 39–52 across cells).

## Canaries — ALL PASS

- Ca-1 provenance: `run_coal` honest byte-identity vs `run_adv_gate` 4/4.
- Ca-fp SPIN-47 replay: fp_flood ladder@15 K=1 @1.10 → honestFP 5/5 seeds (5342/seed), global nfMis 0, shift −2.2pp (digit-exact vs published).
- Ca2 anchors digit-exact: zero@15 K1 77.3/8756/187834; ladder@15 K1 71.5/5792/106378.
- Cc1 SPIN-39 anchor: nf_alt ladder@15 K=2 @1.10 −55.8pp.
- Cb gate=never ≡ gate=off full-dict, all 3 new modes (D6 + quota variants).
- Cc double-run determinism 5/5 configs.
- S1: SPIN-15 closure asserted live in every run; ledger Δ=0 everywhere.

## Arm A — SPOOF STORM under D6

| grammar | K | shift | spoofTry | spoofAcc | acc% | honestFPR | seeds |
|---|---|---|---|---|---|---|---|
| ladder@15 | 1 | +0.0pp | 28651 | 0 | 0% | 0/5 | 5/5 |
| ladder@15 | 2 | +0.0pp | 28040 | 0 | 0% | 0/5 | 5/5 |
| kcoh5@15 | 1 | +0.0pp | 47304 | 0 | 0% | 0/5 | 5/5 |
| kcoh5@15 | 2 | +0.0pp | 38200 | 0 | 0% | 0/5 | 5/5 |

**H1 VALIDATED**: 0 spoofed flits accepted out of ~142k tries across cells; honest-cell FPR 0 in 5/5 seeds; residency returns exactly to the honest null (spoof drops make the fabric bit-identical to honest given the same RNG stream).

## Arm B — SELF-ATTRIBUTED FLOOD (H2 FALSIFIED)

Envelope quota (Q=39–52) admits ~63% of the flood: raw erosion −2.2/−16.0/−10.9/−12.2pp becomes −1.5/−12.8/−5.2/−9.5pp — better but **honest residency still erodes −18.2 to −89.4pp** (honest in-band fraction vs baseline). **H2 FALSIFIED** under the pre-registered rule (>5pp erosion), with 0 honest drops and the ledger correctly pricing 956–4557 drops/seed to the liar.

**Post-hoc sensitivity (exploratory, NOT the gate)** — tight quotas:

| Q | worst honResΔ across 4 cells | verdict flavor |
|---|---|---|
| 1 | −1.2pp | holds everywhere |
| 2 | −5.5pp | 3/4 cells hold |
| 4 | −8.9pp | fails |
| 8 | −19.6pp | fails |

The mechanism is sound but the envelope-calibrated Q is not: a volume quota sized to honest bursts cannot price a flood that mimics honest volume. The defense only holds when Q is tightened to ~1/epoch, far below the honest envelope — and at that point the quota is pricing *rate*, not *provenance*. D6's per-flit attestation solves misattribution (Arm A) but volume denial is a separate problem the quota only partially buys.

## Arm C — COALITION SPOOF+DECLARE HYBRID

| grammar | K | shift | caught | honestD5FP | honestD6FP |
|---|---|---|---|---|---|
| ladder@15 | 1 | −2.4pp | 5/5 | 0/5 | 0/5 |
| ladder@15 | 2 | −4.2pp | 5/5 | 0/5 | 0/5 |
| kcoh5@15 | 1 | −0.1pp | 5/5 | 0/5 | 0/5 |
| kcoh5@15 | 2 | +10.3pp | 5/5 | 0/5 | 0/5 |

**H3 VALIDATED**: every seed catches the coalition (spoof drops hit the D6 ledger; the declaring twin's per-cell D5 flags fire on lie ticks), honest cells flagged nowhere. Splitting roles does not split the detection.

## Verdicts (pre-registered rules)

- **H1 (D6 catches spoof storm, honest FPR 0): VALIDATED** — 0/142k accepted, FPR 0, 5/5 seeds, 4/4 cells.
- **H2 (envelope D6-quota holds honest residency ≤2pp): FALSIFIED** — −18.2 to −89.4pp honest-residency erosion persists; ledger prices the liar but doesn't protect the commons. (Tight-quota sensitivity shows ≤1.2pp at Q=1, post-hoc.)
- **H3 (hybrid caught 5/5, honest FPR 0): VALIDATED.**
- **S1 closure: PASS** — live asserts on every arm, ledger Δ=0.

**Headline: per-flit emission provenance closes SPIN-47's spoofing crack completely — zero accepted spoofed flits, zero honest false positives, hybrid coalitions still caught 5/5 — but a volume quota calibrated to the honest envelope cannot defend against a self-attributed flood; attribution and congestion-pricing are separable problems.**

## Scars / honesty log

- The D6 catch is structural (spoofed attestations can never match the monotone counter, as with nonce-signed emissions); the honest boundary is that this models a counter-holder adversary, not a key-compromise adversary. D6-with-key-compromise is untested.
- H2's falsification is partly a design artifact: Q was pre-registered at the honest envelope, which the flood (sized at 4×trig-rate extras) mostly fits under. The sensitivity table shows the knob's actual operating curve — reported rather than re-gated post-hoc.
- honResΔ magnitudes (−89pp) are large because honest in-band fraction is near-saturated at baseline (~99%), so small absolute erosion reads as large pp; the gated quantity honest-D6-drops stayed 0 everywhere.
- Attempt-1 lane death (zero output) is why the script was staged before any panel; canaries re-verified all provenance on this attempt.
- The `if True:` guard around the adv-dict in `run_d6` means honest runs also carry the audit (unlike spin47); harmless but noted for byte-diff archaeology.

## Next-spoke proposal

**SPIN-50 — D7: rate-adaptive emission pricing.** The honest gap H2 exposed: a per-cell ledger that adapts Q to the cell's own honest envelope is gameable by floods sized under the envelope. Attack surface for the next adversary spoke: (a) slow-drip flood under a tight quota (does Q=1 still hold when the liar paces junk at 1/epoch forever? ledger cost vs harm curve), (b) quota-free alternative — content-aware pricing (junk magnitude/mass audit, SPIN-15 ledger as discriminator), (c) key-compromise model for D6. Metrology side: book the Q-operating curve (Q vs honResΔ vs ledger) as a law candidate.
