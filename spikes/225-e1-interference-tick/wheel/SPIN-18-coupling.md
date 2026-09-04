# SPIN-18 — COUPLING: REGIME RESONANCE MAP (SPIN-17 follow-up, spoke 7)

Everything below was actually run: `wheel/spin18_coupling.py`, raw output
`wheel/spin18-output.txt` (elapsed 15 s). Config: N=6 ladder, delta=12,
drift=6, pd=3, 4800 ticks, seeds {1,7,42,1999,20260902}, integer-only in
every loop, floats only at print. Instrument = `dyn_run`, the canary-proven
verbatim clone of `exp_glm1.run_fabric` (k as parameter), single-pass inline
scheduling. Phase convention pinned: offset=0 = hi-phase starts tick 0;
"anti" = offset P/2. (SPIN-17's lo-first base = our offset P/2 at duty-50,
so the replay check maps to the anti column.)

**HYPOTHESIS (pre-registered):** the regime tax is a RESONANCE coupling
between the spread schedule and reality's 240-tick cycle; tax peak follows
a K×P law (max when pulse-superposition lifetime ≈ 120); anti-alignment
cancels the K=2 P=16 catastrophe.

## Verdicts

| # | Sub-claim | Verdict |
|---|-----------|---------|
| 1 | Tax peak follows a K×P resonance law (peak when pulse lifetime ≈ 120) | **FALSIFIED** — peak P is 24–48 at K=1, 16 at K=2, and pinned at the P=8 grid floor for all K≥4; no K×P law (peak K×P = 24,32,32,64,128), and the P=8 edge means the true peak for K≥4 is below the floor |
| 2 | Anti-aligned phase cancels the K=2 P=16 catastrophe (27.0 → ?) | **FALSIFIED** — anti-alignment *modulates*, never cancels: 32.0 aligned → 27.0 anti (the catastrophe survives both phases) |
| 3 | Coupling is to reality's 240-cycle (phase DOF only for commensurate P) | **VALIDATED** — the phase effect d(osc) is large ONLY for P dividing 240 (16:+5.1, 24:+5.8, 48:−6.5, 120:+6.2, 240:−4.8) and ≈0 for all non-divisors (32:0, 64:+1.7, 96:−0.6, 128:+1.1, 192:−0.3, 256:+0.3, K=2 row; same pattern every K). Incommensurate P=100/140 show no phase structure and mid-low taxes |
| 4 | Guerrilla duty: exists a duty maximizing damage per unit bad time | **VALIDATED — sharpened**: duty **10% @ P=16** is the guerrilla optimum: osc 34.7 (−55.8 pp vs mmS), D/tick = 34.9 (vs 13.1 at SPIN-17's duty-25 anchor). At P=16, duty-10 = ONE single tick of spread-30 per 16 ticks |
| 5 | Phase-offset effect is smooth (resonance) at K=2 P=16 | **MIXED** — offsets {0,1,2,4,6,8} → osc {24.8, 26.2, 30.3, 26.2, 27.8, 29.9}: 5.5 pp of real phase leverage, but jagged and non-monotone (offset 1 ≡ offset 4), not a graded resonance ramp |

**Headline: the K=2 catastrophe is phase-ROBUST (anti-alignment moves it
only 32.0→27.0 pp) but commensurability-gated — the phase degree of freedom
exists only when P divides reality's 240-cycle — and the guerrilla optimum
is a single bad tick per 16 (duty-10, K=2): one spread-30 tick in sixteen
collapses accuracy 50 pp below static-5 (34.7 vs 84.9).**

## EXP 1 — Resonance map (K ∈ {1,2,4,8,16} × P ∈ {8..256} × {ali, anti, inc})

Key structure (tax = TWmean − osc, pp; dmm = osc − mmS):

- **K=2 remains uniquely catastrophic**: peak 32.0 (ali) / 27.0 (anti) at
  P=16; every other K peaks at 6.8–10.4. The catastrophe is not a ridge in
  K — it is a K=2 pin, phase-robust, ~3× its neighbors.
- **The phase DOF is commensurability-gated** (the cleanest law in the
  data): at every K, d(osc) between aligned and anti-aligned is 4–8 pp for
  P ∈ {16,24,48,120,240} (the divisors of 240 on the grid) and ≤1.7 pp for
  every non-divisor. Offsetting by P/2 shifts alignment with the 240-cycle
  only when P | 240 — a direct coupling signature, not generic phase noise.
- **P=240 aligned is a phase trap**: K=1 tax −4.5 (beats TWmean!) with dmm
  +13.5, while anti-aligned sits at +4.0 tax — an 8.4 pp swing from phase
  alone when the schedule period equals the reality period. Consistent with
  SPIN-17's Jensen floor (slow sampling beats the concave mean) but here
  phase decides which sign you get.
- **K=1 has a genuine interior peak** (tax 9.0 @ P=24 aligned, 7.9 @ P=48
  anti) that SPIN-17's coarser grid missed; K≥4 peaks sit at the P=8 floor
  (6.8–10.4), so their true peak may lie below P=8 — grid-floor caveat.
- **Incommensurate P=100/140**: uniformly low tax (K=2: 6.6/4.0; K≥4:
  0.8–1.6), no phase structure — an incommensurate schedule launders out
  both the resonance and the phase DOF. Cheap defense: pick P coprime-ish
  to 240.
- **K≥4 columns are near-carbon copies of each other** (K=8 vs K=16 differ
  ≤0.9 pp everywhere) — the K-axis saturates at 8.

## EXP 2 — Guerrilla duty (K=2; damage-rate = (mmS − osc)/(duty·P))

| P | duty | osc% | tax | dmm | D/tick |
|---|------|------|-----|-----|--------|
| 16 | **10** | **34.7** | **44.5** | **−55.8** | **34.9** |
| 16 | 15 | 29.6 | 46.8 | −61.9 | 25.8 |
| 16 | 25 (anchor) | 35.7 | 35.1 | −52.3 | 13.1 |
| 16 | 5 | 84.9 | −2.8 | −3.9 | 4.9 |
| 64 | 10 | 77.1 | 2.1 | −13.4 | 2.1 |
| 64 | 25 | 58.7 | 12.1 | −29.3 | 1.8 |

- **The P=16 duty axis is wildly non-monotone**: duty 5 → benign (but note
  scheduler quantization: 16·5//100 = 0 hi-ticks = pure static-5, an
  artifact to book), duty 10 → catastrophic (44.5 tax), duty 20 → mild
  (6.4), duty 25 → bad again (35.1). Damage is not a function of bad-time
  fraction; it depends on the exact tick pattern of the 1–4-tick pulses
  against the pulse-superposition and trigger dynamics.
- **Headline guerrilla**: ONE tick of spread-30 per 16 (duty-10) collapses
  osc to 34.7 vs static-5's 84.9 — a 50 pp collapse from 6.25% bad-time.
  Per unit bad-regime time this is 2.7× SPIN-17's duty-25 anchor. At P=64
  the same duty is 17× weaker (2.1) — the guerrilla effect is itself
  period-resonant.
- duty-15 has the worst absolute dmm (−61.9, new worst on record for this
  spoke) but duty-10 wins on rate.

## EXP 3 — Phase-offset fine sweep (K=2, P=16, offsets {0,1,2,4,6,8})

osc% = {24.8, 26.2, 30.3, 26.2, 27.8, 29.9}; tax = {32.0, 30.7, 26.5, 30.7,
29.1, 27.0}. Real leverage (5.5 pp) but **jagged**: offset 1 and offset 4
land identically, offset 2 is a local max, and there is no monotone ramp
toward the anti-aligned endpoint. Verdict: not a smooth standing-wave
resonance in phase; the phase response is lattice-shaped (consistent with
integer pulse superposition + tick-quantized triggers). A smooth-vs-quantized
 discriminator needs per-seed deltas or offsets 0–8 at step 1 (next spoke).

## Canaries — all PASS

- **(a)** dyn_run vs run_fabric byte-identity, 6 configs (grammars × K ×
  seeds): PASS.
- **(b)** Anchors: zero@15 K=1 = 77.3% / ev 8756 / debt 187834 EXACT;
  ladder@15 K=1 = 71.5% / ev 5792 / debt 106378 EXACT. SPIN-17 replays K=2
  tax: 27.0 @ P=16, 11.7 @ P=64, 1.7 @ P=256 — all EXACT.
- **(c)** No-shift identity: hold-5 through the scheduler path (offsets 0
  and 8), K ∈ {1,2,4,8,16} × 5 seeds, byte-identical. PASS.

## Scars

1. **Duty quantization bites at small duty×P** (new): P=16 duty-5 yields
   `16*5//100 = 0` hi-ticks — silently a static run. Always report
   hi_ticks; sweep duty with hi_ticks ∈ {1,2,3,...} instead of % when P is
   small.
2. **Phase convention must be stated against the replay source**: our
   offset-0 is SPIN-17's *invert* column. The replay check only lines up
   because the anti column (offset P/2) reproduces SPIN-17's lo-first base
   at duty-50. Pin and document, or you will compare ali against lo-first
   and "discover" a 5 pp shift that is pure convention.
3. **Grid floors masquerade as peaks** (SPIN-17 scar #3, K-axis edition):
   K≥4 "peak at P=8" is the P-floor; don't quote a peak law from a corner.
   Extend P below 8 before claiming peak-P for K≥4.
4. **Both baselines, always** (SPIN-17 scar #2, still true): K=1 P=240
   aligned is −4.5 vs TWmean but +13.5 vs mmS — opposite signs, same run.

## Next spoke proposal

**SPIN-19 — GUERRILLA PULSE GRAMMAR (coupling/regime joint):** the P=16
duty sweep is non-monotone in hi_ticks {0,1,2,3,4} (benign/catastrophic/
worst/mild/bad) — map damage vs (hi_ticks, pulse spacing, P ∈ {8,12,16,20,
24,32,48}) at K=2 with per-seed resolution, plus single-tick pulses at
every phase offset against the 240-cycle, to find the grammar of maximal
one-tick damage (is there a "killer tick" alignment?) and its mirror —
the scheduling rule that launders the resonance (incommensurate P already
hints at it: 4–6× cheaper than P | 240).

Status: **COMPLETE.** Nothing committed or pushed. WHEEL-LOG.md untouched.
