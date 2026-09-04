# SPIN-47 — SPOKE 2: ADVERSARY — D5 UNDER COALITION

Date: 2026-09-04 · Work dir: `225-e1-interference-tick/` · Script: `wheel/spin47_adversary.py` (extends `spin39_adversary.py`) · Raw output: `wheel/spin47-adversary-output.txt` (python3 -u, single pass, no pipes). Not committed/pushed.

## ⚠️ ENVIRONMENT INCIDENT (logged before any verdict — read first)

At ~06:39 AKDT, **mid-task**, a concurrent process rewound the `wheel/` directory to a ~2026-09-03 18:36 snapshot: every artifact from SPIN-15 through SPIN-46 (sources, outputs, reports — including `spin39_adversary.py`, this spin's mandated provenance base) disappeared, and `WHEEL-LOG.md` was reverted to a pre-SPIN-15 state that **no longer contains the SPIN-47 dispatch entry/brief**. Directory observed stable afterward (45 s watch); `__pycache__` still held the pre-deletion `spin39_adversary.cpython-314.pyc`.

**Recovery (documented, not fabricated):** `spin39_adversary.py` was read in full at 06:38, minutes before deletion; it was rewritten verbatim from that read and **verified bytecode-identical to the surviving pre-deletion `.pyc`** (`dis` dump, addresses/paths normalized — exact match), and it re-runs to its published verdict set (canaries PASS; H1/H2 FALSIFIED; S1/S2 PASS). Per the no-delete/archive doctrine this is a restore, not a rewrite. All other SPIN-15..46 artifacts remain missing as of run time — that loss is the wheel master's to reconcile; nothing in this spin depends on them beyond spin39 (verified by import graph: spin39 → spin11 → exp_glm1, all present).

## Pre-registered hypotheses (docstring, written before any run)

- **H1 (COALITION evasion):** two coordinated liars (twins {4,5}) split the lying load by turns so each member's per-liar miss-rate halves, with collective drift injection matched to SPIN-39's single-liar rate. VALIDATED iff some strategy/cell shifts residency >5pp vs the gate-off honest null with ≥1 seed where **no** coalition member is D5-flagged. Strategies: `coal_alt` (alternate carrier), `coal_tag` (tick-parity carrier), `coal_cov` (any-member trigger, scaling probe). Honest boundary documented up front: D5's flag threshold is 0 and lie magnitude is integer (minimum 1), so "per-tick magnitude under threshold" is structurally impossible — load-splitting can only be by turns, which is what was built.
- **H2 (FP-FLOOD):** a liar that declares honestly but emits spoofed ±1 pulses under honest non-triggering cells' ids produces ≥1 honest-cell false flag in 5/5 seeds under the per-cell declared-vs-emitted audit. FALSIFIED if honest FPR stays 0 in any seed. Residency erosion reported as evidence, not a gate.
- **S1:** SPIN-15 closure identity asserted live in-loop on every run; honest-cell FPR 0 on coalition arms.

## Canaries — ALL PASS

- **Ca:** spin39 harness imported & intact — honest byte-identity vs `exp_glm1.run_fabric`, 8/8.
- **Ca2:** SPIN-5 anchors digit-exact: zero@15 K1 77.3/8756/187834; ladder@15 K1 71.5/5792/106378.
- **Cc1:** SPIN-39 mixed-twin replay: nf_alt ladder@15 K=2 @1.10 shift −55.8pp — exact.
- **Cb:** gate=never ≡ gate=off full-dict for all 4 new modes.
- **Cc:** double-run determinism, 5 configs (incl. coalition + flood).

## Arm A: COALITION @ θ*=1.10 (5-seed means, gate-off honest null)

| mode | grammar | K | shift | gOpen | lie4/lie5 | flag4/5 seeds | anyFlag | honestFP |
|---|---|---|---|---|---|---|---|---|
| coal_alt | ladder@15 | 1 | −0.4pp | 75 | 775/775 | 5/5 | 5/5 | 0 |
| coal_alt | ladder@15 | 2 | **+6.4pp** | 86 | 885/885 | 5/5 | 5/5 | 0 |
| coal_alt | kcoh5@15 | 1 | **+7.9pp** | 343 | 1484/1483 | 5/5 | 5/5 | 0 |
| coal_alt | kcoh5@15 | 2 | **+17.3pp** | 679 | 1575/1574 | 5/5 | 5/5 | 0 |
| coal_tag | (same 4 cells) | | identical shifts | | ~50/50 splits | 5/5 | 5/5 | 0 |
| coal_cov | (same 4 cells) | | identical shifts | | up to 2000/2000 | 5/5 | 5/5 | 0 |

Rate-matched coalition harm is **exactly** the single-liar inflate harm (SPIN-35 replay values +6.4/+7.9/+17.3/−0.4, digit-exact) — the load split changes nothing the fabric sees, as designed. **H1: FALSIFIED.** D5 flags ≥1 coalition member in every seed of every strategy/cell; both members flagged 5/5 everywhere. There is no sub-threshold slot: integer lie magnitude ≥1 against a zero-threshold detector means every carrier tick is attributable, and turn-splitting only halves each member's flag count (lie4 ≈ lie5 ≈ half), never zeroes it.

## Arm B: FP-FLOOD @ θ*=1.10 — spoofed honest-id pulses

| grammar | K | mean% | null% | shift | gOpen | global nfMis | honestFP seeds | honestFP/seed |
|---|---|---|---|---|---|---|---|---|
| ladder@15 | 1 | 69.3 | 71.5 | −2.2pp | 0 | **0** | 5/5 | 5342 |
| ladder@15 | 2 | 44.0 | 60.0 | **−16.0pp** | 0 | **0** | 5/5 | 4759 |
| kcoh5@15 | 1 | 63.3 | 74.1 | **−10.9pp** | 0 | **0** | 5/5 | 7889 |
| kcoh5@15 | 2 | 38.4 | 50.6 | **−12.2pp** | 0 | **0** | 5/5 | 6672 |

**H2: VALIDATED — and this is the first real crack in the load-bearing wall.** The fp-flood attacker:

1. **Evades both booked audits in attribution.** Global D5 (declared-vs-trig-count) records **0 mismatches** — the liar declares honestly and the spoofed pulses live only in the emission channel. Per-cell D5 flags only the *victims*: thousands of honest-cell false flags per seed while the liar's own per-cell ledger stays clean (declared 1, honest-emitted 1).
2. **Erodes residency −2.2 to −16.0pp** with magnitude-1 spoofed pulses — degrading (first degrading adversary in this lineage that no declared-channel detector sees; SPIN-35/39 damage was either stabilizing or fully flagged).

Boundary honesty: the spoof is an emission-channel attack *outside the declared-nf threat model D5 was booked against* — D5's zero-miss record is intact **within** its model (Arm A proves it against coalitions), but the model's perimeter is now known to exclude id-spoofed emissions. The residency drop also conflates flood-noise with flag-storm effect; disentangling would need a spoof-without-storm control (next spoke).

## Arm C: control — SPIN-39 replay (via spin39 harness)

All 12 cells reproduce the published SPIN-39 table digit-exact (nf_alt −55.8/−50.1/+7.3/+0.0; nf_rnd −55.1/−49.8/+7.3/+0.0; nf_2pd +0.0 everywhere; nfMis 5/5 everywhere; closure 0). Anchor continuity holds.

## Verdicts (pre-registered rules)

- **H1 (coalition evasion of D5): FALSIFIED** — flags ≥1 member in every seed of every strategy.
- **H2 (FP-flood honest false flags 5/5 seeds): VALIDATED** — 4/4 cells, 5/5 seeds, 4.7k–7.9k flags/seed, with −16.0pp worst erosion and zero global-D5 detection.
- **S1 closure: PASS** — live SPIN-15 asserts on every run, ledger Δ=0 everywhere, honest FPR 0 on all coalition arms.

**Headline: D5 holds against coalitions exactly as well as against single liars — no evasion, no honest false positives — but it is blind-sided by emission-id spoofing, which simultaneously escapes global attribution, slander-flags honest cells thousands of times per seed, and degrades collective residency up to −16pp.**

## Scars / honesty log

- The 06:39 directory revert destroyed this spin's mandated provenance base mid-task; recovery via verbatim rewrite + bytecode-exact verification against the surviving `.pyc` is documented above. The wheel master should re-book the lost SPIN-15..46 artifacts (`.pyc`s for spin39/41/42/43/44 survive in `__pycache__` as recovery seeds) and re-append the SPIN-47 dispatch entry lost from WHEEL-LOG.md.
- Arm A's per-cell audit is an observer instrument added in spin47 (never feeds the loop); honest nulls in `run_coal` reproduce the published nulls exactly (71.5/60.0/74.1/50.6) but no explicit run_coal-vs-run_adv_gate honest byte-identity canary was run — the anchor match is the evidence; book the explicit canary next time.
- `coal_cov`'s lie rate exceeds the single-liar rate by design (any-member trigger); its shifts still landed identical to rate-matched cells because twin-4 triggers are subset-dominated — the scaling probe was therefore uninformative, noted rather than hidden.
- Run-1 syntax error (unterminated f-string) and the ModuleNotFoundError from the deleted spin39 were fixed before any data was collected; output file contains the registered run only.

## Next-spoke proposal (ADVERSARY or successor spoke)

**SPIN-48 — D6: emission-channel provenance.** The fp-flood result demands a fabric-verifiable emission-identity detector (per-cell pulse attestation / nonce-signed emissions) tested against: spoof storm, spoof-without-residency-harm (disentangle noise vs slander), and coalition spoof+declare hybrid (does pairing fp_flood with a coalition lie reopen attribution?). Also worth one control: fp_flood with spoofed pulses under the *liar's own* id (self-attributed flood) to isolate the misattribution mechanism.
