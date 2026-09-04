# SPIN-44 — METROLOGY (spoke 1): COHERENCE-MASS NORMALIZER

**Lane:** wheel_spin44_metrology (zai/glm-5.3, run mode) · 2026-09-04
**Brief:** SPIN-43's next-spoke proposal, per WHEEL-LOG ## SPIN-44-METROLOGY.
**Artifacts:** spin44_metrology.py + spin44-metrology-output.txt (python3 -u, direct redirect, no pipes). Not committed to git.

## Pre-registration

H1/H2 and band ε = 5.0pp committed in the script header before any panel
run (see `spin44_metrology.py` docstring): per-pulse ρ =
√(noise_energy/n_pulses) / (live_mass_sum/n_pulses); Arm A = SPIN-43 grid
(3 grammars × K=2 × q{5,6,7,8} × M=1, 5 seeds, never anchors); Arm B =
q=6 fixed, pd ∈ {2,3,6} sweep of the pulse-mass scale. H1 FALSIFY rule =
pd-flat (≤2.0pp) at matched step; H1 VALIDATE = cost moves with pd AND
arm-A LOO collapse of per-pulse ρ within 5pp AND Spearman ≥ 0.90. H2 =
per-pulse ρ monotone in step at K=2.

## Canaries — 5/5 PASS (gate live before any panel read)

- **a** Harness import byte-identity: sp43.dyn_run_sto43 ≡ sp42.dyn_run_sto
  on 12 measurement arms (resid+events+ledger minus the 3 read-only
  instruments) + 6 never-arms ≡ run_fabric. The SPIN-44 script adds NO
  dynamics code — it calls the imported SPIN-43 harness untouched.
- **b** Anchors digit-exact: zero K=1 77.3/187834/8756; ladder@15 K=1
  71.5/106378/5792.
- **c** SPIN-43 replays via the imported harness: ladder K=2 q=5 M=1 cost
  57.4pp; zero K=2 q=8 cost 0.7pp — both exact.
- **d** gate=never ≡ mc=0: 9 arms (3 grammars × 3 pd) created=deleted=0,
  0 draws, SPIN-15 ledger assert live on every arm.
- **e** Double-run determinism byte-identical (resid, events, ledger
  incl. instruments).

One dev-run fix before the registered run: canary-a initially compared
full ledger dicts (sp43's 3 instrument keys ≠ sp42's) — comparison
corrected to SPIN-43's own convention; a genuine wiring check, not a
dynamics change.

## Results

### Arm A (SPIN-43 grid, per-pulse ρ)

Per-pulse ρ at K=2: zero 0.153/0.511/0.490/0.282 (q5–q8), ladder
0.095/0.281/0.325/0.316, kcoh5 0.076/0.379/0.387/0.279. K=1 rows (ρ_pp
0.5–3.1, cost 0.0 everywhere) again structurally vacuous — and
diagnostically decisive: per-pulse noise EXCEEDS per-pulse mass (ρ_pp>1)
at zero measured cost, because K=1 pulses die within the birth tick.

### Arm B (pulse-mass scale sweep, q=6, K=2)

| grammar | pd=2 | pd=3 | pd=6 |
|---|---|---|---|
| zero | cost 0.0 **DIVERGED** | 21.0 | 2.6 |
| ladder@15 | cost 0.1 **DIVERGED** | 45.1 | 4.5 |
| kcoh5@15 | cost 0.0 **DIVERGED** | 34.5 | −1.2 |

pd=2 is supra-wall divergent at N=6 (N > 2·pd+1 = 5; maxresid ~1e250,
pct saturated at 0.2) — predicted by the SPIN-8/16 wall law, discovered
here as a float-overflow crash and handled with a LABELED post-hoc
divergence gate (SPIN-16 guard-prefix scar class; flagged in-script, in
output, and excluded from the honest reading). On stable pd {3,6} only,
cost still moves hugely: spreads 18.4 / 40.6 / 35.6pp.

## Verdicts (pre-registered rules)

**H1: MIXED.** Cost is emphatically NOT pd-flat at matched step (the
FALSIFY arm fails: spreads 21–45pp) — the pulse-mass scale moves the
variance channel. But the denominator claim DIES: per-pulse ρ does NOT
collapse across grammars (arm-A LOO max |resid| = 44.4pp vs ε=5pp;
Spearman(cost, ρ_pp) = −0.462 vs ≥0.90 required). The per-pulse
normalizer is no better than SPIN-43's confounded grid-ρ (LOO 40.8pp,
S=−0.608) — and the sign of the failure is informative: at pd=6 cost is
near zero while ρ_pp ≈ 2.4–2.6 (per-pulse noise std exceeds per-pulse
live mass 2.4×!) yet the fabric is fine — because its never-anchor is
itself near-dead (99.4 residency). Mass-relative noise does not price
the variance channel.

**H2: FALSIFIED.** Per-pulse ρ is non-monotone in step at K=2 for ALL
THREE grammars (interior maximum at q6–q7: e.g. zero
0.153/0.511/0.490/0.282). The per-pulse normalizer does NOT repair
SPIN-43's non-monotonicity scar; it reproduces it at O(1) scale instead
of O(10⁻³).

## Headline

**The variance channel is pulse-mass-RELATIVE in its inputs (cost moves
21–45pp with pd at fixed grid) but is not priced by ANY mass-normalized
noise ratio measured so far** — neither grid-ρ (SPIN-43) nor per-pulse ρ
(here). Both the "grid is the denominator" and "pulse-mass scale is the
denominator" stories are dead as normalizers. The surviving clues:
(i) K=1 cells have ρ_pp > 1 at zero cost (noise only bites when pulses
live across ticks); (ii) at pd=6, ρ_pp ≈ 2.5 with cost ≈ 0 (the fabric's
dead zones absorb unbounded per-pulse noise); (iii) the cost curve is
interior-peaked in step, exactly where pulse lifetime (K slots) overlaps
the measurement grid.

## Scars / honest boundaries

1. **pd=2 arm is divergent, not measured.** N=6 > 2pd+1 triggers the
   co-fire wall; the registered pd grid {2,3,6} straddles it
   unintentionally. Its 0.0 "costs" are saturated-pct artifacts, excluded
   by a post-hoc labeled gate — registration lesson: pd sweeps at fixed N
   must pre-check the wall condition N ≤ 2pd+1.
2. **Cost-vs-pd is confounded with the never-anchor.** The baseline
   itself moves with pd (zero: 50.0→99.4); "cost" compares fabrics with
   different native health. A matched-health design is needed before
   "cost moves with pd" can be read as a pure variance-channel
   statement — the MIXED verdict rests partly on this.
3. **ρ_pp overflow** at divergent arms forces log-space stat computation
   (integer-safe, floats at print time only, as registered).
4. **Normalizer zoo now 2-for-2 failed** — a third mass-style normalizer
   (per-draw, per-window-variant) would be grinding, not science; the
   next attempt must change the DIMENSION, not the denominator.

## Next-spoke proposal: NOISE-TO-THRESHOLD (σ_n/Δ) normalizer

The two dead normalizers were both noise-to-MASS. The decision law that
governs the fabric is |e| > Δ — the natural scale for rounding noise is
the TRIGGER THRESHOLD, not the mass. Proposed spoke: instrument
σ_n = √(noise_energy/n_obs) per run and test collapse of cost against
σ_n/Δ across (i) the arm-A q-grid and (ii) a Δ sweep {6,9,12,18} at
q=6, K=2, pd=3 (below the wall at N=6), grammars unchanged. Prediction:
the interior peak in step is where σ_n crosses ~Δ/K (a rounding error of
one quantum flips a trigger decision a pulse lifetime wide). Falsify if
σ_n/Δ collapse fails the same 5pp LOO band. Cheap (≈ the SPIN-44 panel
size), reuses this harness verbatim, and pre-checks the wall condition
this time.
