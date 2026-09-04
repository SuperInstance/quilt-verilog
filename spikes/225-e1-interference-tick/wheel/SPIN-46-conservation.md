# SPIN-46 — CONSERVATION (debt-rate law d(debt)/dt = Φ(drift, K))

Lane: wheel_spin46_conservation (zai/glm-5.3). Run: 2026-09-04 14:34 UTC
(41 s wall). Script: `wheel/spin46_conservation.py` (H1 + H2 with decision
rules pre-registered verbatim in the header BEFORE any panel run); raw
output: `wheel/spin46-conservation-output.txt` (python3 -u redirect, no
pipes). Nothing committed or pushed; WHEEL-LOG untouched by this lane.
Executes SPIN-38's filed next-spoke proposal.

## Hypotheses (pre-registered in script header)

- **H1 (separability):** Φ(drift, K) = D(drift) × R(K) on the stress grid
  drift ∈ {96,192,384,768} (drift=0 registered as an excluded boundary
  cell). VALIDATED iff (i) spread of ρ(drift) = Φ(drift,2)/Φ(drift,1)
  ≤ 10% of mean AND (ii) max multiplicative-model residual ≤ 10%.
  FALSIFIED if the interaction term is required.
- **H2 (runaway fate):** K=2 re-saturates at 32× SPIN-38's window duration
  (153,600 ticks = 32 windows of 4800). VALIDATED iff last/first-window
  debt-rate ratio < 0.5 in ≥ 3 of 4 stress drifts; FALSIFIED if ≥ 0.9 in
  ≥ 3 of 4 (unbounded).

## Arms

outlier@30 (N=6, lats [0,0,0,0,0,30]), pd=3, delta=12 (delta-deadness
re-spot-checked), seeds {1, 7, 42, 1999, 20260902}, all real runs.
Main grid drift × K at 38,400 ticks; H2 arm at 153,600 ticks (K=2 all
drifts + K=1 drift=768 control). Integer-only in-loop; floats at print.

## Canaries — ALL PASS

- **(a) provenance:** this runner ≡ `spin38_conservation.run_ledger`
  byte-identical on 7/7 configs including a 153,600-tick nw=32 case.
- **(b) anchors digit-exact:** zero@15 K=1 → 77.3 / 8756 / 187834;
  ladder@15 K=1 → 71.5 / 5792 / 106378.
- **(c) SPIN-38 replay:** ladder@30 K=1 drift=384 debt/ev = 9202.3
  (anchor 9202.4 ± 5%).
- **(d) gate=never ≡ mc=0:** delta=10⁹ → all-zero ledgers, 4/4.
- **(e) SPIN-15 mass/debt identities:** 4/4 on every arm (main grid,
  delta spot check, all 32× arms).
- **(f) double-run determinism:** 4/4 byte-identical.

## Results (all real)

1. **H1 FALSIFIED — the interaction term is required.** The K-resonance
   factor is violently drift-DEPENDENT: ρ = Φ(drift,2)/Φ(drift,1) =
   **3.69 (96) → 2.13 (192) → 1.03 (384) → 1.32 (768)**; spread 130% of
   mean vs the 10% gate, max multiplicative residual 99%. The two
   resonance branches *cross*: at drift 96 the K=2 rate is 3.7× K=1; at
   drift 384 they are indistinguishable (1.03×); above that K=2 pulls
   ahead again (1.32×) because its runaway exponent keeps compounding
   while K=1's rate saturates in drift. Φ is genuinely 2-D in (drift, K).
2. **H2 FALSIFIED — no re-saturation at 32×.** K=2 last/first-window
   debt-rate ratios at 153,600 ticks: **1.14 / 1.80 / 6.19 / 8.05** at
   drift 96/192/384/768 — every stress cell ≥ 0.9 (unb 4/4, sat 0/4), and
   the ratios are HIGHER than at 8× (SPIN-38: 1.83 → 4.44 at drift 768;
   now 8.05): the runaway accelerates with duration, it does not decay.
   32×/8× debt ratios: 3.59 / 4.43 / 5.61 / **9.29** — superlinear in
   duration at drift ≥ 384 (linear continuation would give 4.0).
3. **K=1's concavity is also duration-unstable (control cell):** at 32×,
   drift=768 K=1 has last/first rate ratio 2.97 (vs 1.73 at 8×) and a
   32×/8× debt ratio of 6.35 > 4 — even the "saturating" branch is
   superlinear in duration at the top drift. The K=1-vs-K=2 dichotomy is
   a difference of runaway exponent, not of kind.
4. **Delta-deadness re-confirmed:** drift=384 spread 0.01% (K=1), 0.02%
   (K=2) across delta ∈ {1,6,12}. drift=0 remains the boundary regime
   (rho=1.28, linear-flat window rates r≈1.0, 32×/8× ratio 4.01 — exactly
   linear in duration there).
5. Events pinned at 99.96–99.98% occupancy at stress, delta-invariant,
   K-invariant — the rate law lives entirely in per-event debt mass.

## Verdict (per pre-registered rules)

**H1 FALSIFIED / H2 FALSIFIED.** The debt rate is NOT separable: Φ is an
irreducible 2-D function of (drift, K) with a crossing resonance, and the
K=2 runaway does not re-saturate even at 32× duration — it accelerates.
Combined with SPIN-38: there is no debt ceiling, no delta dimension, and
no separable rate law; debt is a divergent channel whose growth exponent
is set by the full (drift, K, duration) triple.

## Headline number

**ρ(drift) = Φ(·,2)/Φ(·,1) collapses 3.69 → 1.03 then rebounds to 1.32
across drift 96 → 768 (resonance crossing), and at 32× duration the K=2
drift=768 arm hits last/first window rate 8.05 with 9.29× debt in 4× the
ticks — the runaway is superlinear in duration and accelerating.**

## Scars / honest boundaries

- One index typo (`cells[d]` vs `cells[(d,1)]` in the H1 residual line)
  crashed the first execution before any verdict was computed; fixed and
  rerun fresh end-to-end — the archived output file is the second,
  complete run (first run's partial stdout overwritten by the rerun;
  no numbers from the crashed run used anywhere).
- The 8-window main grid measures Φ as debt/ticks = a duration-averaged
  rate; at drift ≥ 384 the within-run acceleration makes Φ
  duration-dependent, so Φ values are not asymptotic constants — they
  are lower bounds. A true asymptotic Φ̂ would need window-local rates
  (the 32× arms provide them for K=2 only; no K=1 32× sweep below
  drift 768 was run — budget call, not cherry-pick).
- Window-rate ratios are 4800-tick aggregates; oscillatory structure
  inside windows (visible as w8 vs w16 non-monotone dips at 32×) is
  uncharacterized.
- rho non-monotonicity (crossing at ~drift 384) has no mechanism model —
  candidate: K sets pulse lifetime (echo period), drift sets input
  bandwidth; crossing where echo period ≈ drift autocorrelation scale.
  Untested.

## Next-spoke proposal

**WINDOW-LOCAL RATE EXPONENT (regime follow-up):** the runaway is
superlinear in duration at K=2 and now also at K=1/drift=768 — extract
the local growth exponent γ(t) = d log(debt-rate)/d log(t) window-by-
window at 32× for the full drift × K grid (one sweep, ~1 min), and test
whether γ converges to a finite constant (power-law runaway with a law
γ(drift, K)) or keeps growing (genuine divergence, no exponent). Also
bracket the rho-crossing drift (is it exactly 384?). Direct successor:
this spin showed the interaction is required but did not fit its shape.
