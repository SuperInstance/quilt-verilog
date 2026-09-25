# ROUND 8 — Q1: class-grain boundary on linear-superposition substrates

**Date:** 2026-09-03 (dev round 8, subagent lane) · **Branch:** g3-kinduction
**Agenda item:** RESEARCH-AGENDA §6 Q1 · **Charter:** §10 cheat #2 ("every claimed cheat must name its grain")
**Anchor:** glm-2 #2 / F11 — dequantized Hadamard walk, identity grain HOLDS (13 ppm TVD), binning buys ~nothing (13→11).

---

## 1. Hypothesis (pre-registered BEFORE any new number was read)

The class-grain requirement for quantized interference statistics is decided by a
substrate property. Known data points: embedding-census substrate REQUIRES class
grain (E7/F5); linear-superposition Hadamard walk HOLDS at identity grain
(glm-2 #2/F11). Candidate discriminators: **(a) nonlinearity of readout,
(b) learned-vs-fixed dynamics, (c) dimensionality.** Prediction at registration:
one of the three axes will show identity-grain TVD blowing up while class-grain
TVD stays low (the E7 pattern re-emerging); the other two will hold at identity
grain like the anchor.

## 2. Method

Reference arm = the SAME recurrence, uncapped, exact big integers. Fabric arm =
same recurrence under width cap 2^20 with global halving rescale (toward zero,
sign-symmetric) — byte-identical mechanics to glm-2's FABRIC arm. One property
varied at a time from the anchor baseline:

- **A1 readout:** linear |v|² (anchor), threshold-occupancy 1[|v|≥T] with T
  relative to the arm's own max (T = max//frac), signum (signed measure
  pᵢ ∝ (Lᵢ+Rᵢ), L1-normed).
- **A2 dynamics:** "learned" coin — LCG-driven per-step integer perturbation of
  the coin matrix (identical stream fed to both arms). Seeds 1, 7, 42, 1999,
  20260902. Perturbation constrained so the coin can never be the zero matrix.
- **A3 dimension:** 2-D grid walk (129×129, one chirality shifts −x, other +y,
  same coin), 96 steps, no wrap.

Metric: TVD(reference, fabric) at identity grain and 16-site class grain, floored
ppm, exactly glm-2's `show()`. Integer-only verdict path (Fraction everywhere;
floats only in display division). **Tick count matched to the anchor exactly**
(n=96, L=193 — anchor geometry, per method rules) rather than the ≥4800
alternative. Determinism: fixed seeds, no wall-clock, no unordered iteration.

## 3. Canaries (mandatory, all PASS)

| # | Canary | Result |
|---|--------|--------|
| C2 | Anchor replay before any new number: identity 13 ppm, 16-grain 11 ppm, rescales=27, losses=1566 | **PASS** (byte-exact vs glm-2 published) |
| C3 | Self-canary: classical LCG null mislabeled "fabric cap=2^20" | **CAUGHT** (817,460 ppm vs 13 baseline, >100× threshold) |
| C1 | Double-run byte-identity (final config, two runs) | **PASS** — sha256 `f4a526a897532645d69743ea112eaecc4cf0f535beb4ecb807a412766d3f3e56` both runs |

## 4. Numbers (from q1-class-grain-output.txt)

| arm | identity ppm | 16-grain ppm | rescales | losses |
|-----|-------------:|-------------:|---------:|-------:|
| A0 baseline (anchor) | 13 | 11 | 27 | 1566 |
| A1 readout=linear | 13 | 11 | 27 | 1566 |
| A1 readout=threshold (max//128) | 0 | 0 | 27 | 1566 |
| A1 readout=signum | 10 | 4 | 27 | 1566 |
| A2 perturbed coin, seed=1 | 4 | 1 | 33 | 297 |
| A2 seed=7 | 6 | 2 | 42 | 342 |
| A2 seed=42 | 0 | 0 | 79 | 1139 |
| A2 seed=1999 | 3 | 2 | 28 | 285 |
| A2 seed=20260902 | 0 | 0 | 79 | 1180 |
| A3 2-D grid 129×129 | 13 | 11 | 27 | 1566 |

**A1-APPENDIX — threshold-cut sweep (the load-bearing extra):**

| cut T = max//frac | cap=2^20 ident | cap=2^20 class | cap=2^24 ident | cap=2^24 class |
|---|---:|---:|---:|---:|
| //128 | 0 | 0 | 0 | 0 |
| //4096 | 0 | 0 | 0 | 0 |
| //65536 | 0 | 0 | 0 | 0 |
| //262144 | 11,904 | 11,761 | 0 | 0 |
| //1048576 | **564,766** | **123,365** | 0 | 0 |

## 5. Verdict per axis

- **A1 readout — nonlinearity: PARTIAL decider, but NOT via grain.** Linear
  readout: identity grain survives (13 ppm, anchor). Signum (signed-linear):
  survives (10 ppm). Threshold: survives at every cut **until the cut
  approaches the quantization floor** (T ~ max/cap): then identity TVD explodes
  (564,766 ppm at max//2^20, cap 2^20) — and **class grain does NOT rescue it**
  (123,365 ppm at 16-bin; 4.6× gain, still 12% of all mass). At the SAME
  relative cut with cap 2^24, the failure vanishes entirely (0 ppm). So the
  threshold failure is a **width/floor effect at the discontinuity, not a grain
  effect**: cured by width budget, immune to binning. The E7 pattern
  (identity fails, class saves) never appears on this substrate.
- **A2 dynamics — learned-vs-fixed: NOT a decider.** LCG-perturbed coin,
  5 seeds: identity TVD 0–6 ppm, ≤ the anchor's own 13. Binning buys nothing.
  Grain law transfers.
- **A3 dimension — 1-D vs 2-D: NOT a decider.** 2-D grid reproduces the
  baseline's exact 13/11 ppm, rescales=27, losses=1566. Grain law transfers
  (suspiciously exactly — the 2-D walk at this geometry keeps all amplitude in
  motion patterns that mirror the 1-D rescale schedule; booked as observed).

**Decider among the three candidates: none in the pre-registered form.** The
boundary is not (a)/(b)/(c) as stated — it is **relative scale of the readout's
discontinuity to the quantization floor**. A nonlinear readout breaks quantized
statistics only when its cut lands within ~one cap-scale of the floor, and when
it breaks, NO grain saves it — only width does. On linear-superposition
substrates the E7 class-grain law does not merely fail to transfer; the
class-grain escape hatch does not exist here at all.

**Charter §10 consequence:** cheat #2 on linear-superposition substrates may
claim **identity grain for any continuous (linear or signed-linear) readout,
and for discontinuous readouts only if the discontinuity scale is kept well
above the width floor** — the honest obligation is "name your cut vs your
floor," not "name your grain." (Cheap §10 correction, draftable from this.)

## 6. Scars (honest failures booked)

1. **v1 threshold readout was scale-unfair:** fixed absolute T=8 compared the
   uncapped reference against a globally-halved fabric — a ~1.3×10⁵ ppm
   artifact masquerading as a grain result. Caught by asking "what does T mean
   after rescale?"; fixed to per-arm relative cut. The v1 numbers are in no
   table above.
2. **v1 perturbed coin could die:** unconstrained ±1 on all four coin entries
   admits the zero matrix (dA=dB=dC=−1, dD=+1) → ZeroDivisionError mid-run on
   seed set. Constrained to keep the diagonal nonzero; the walk provably
   cannot die.
3. **A3's byte-identical 13/11/27/1566 to the 1-D baseline** was not
   anticipated; I double-checked the grid arm is actually 2-D (it is — 129×129
   state, x/y chirality shifts). The coincidence of the rescale schedule is
   real but unexplained; booked as an open eyebrow, not a claim.
4. **Tick count:** matched the anchor's 96 steps rather than ≥4800 (method rule
   "match the anchor exactly"). Stationarity caveat inherited from the anchor.
5. First harness run predates the final threshold patch; its sha differs
   (f1618bff…) — C1 byte-identity is claimed only for the final config.

## 7. Files

- `q1_class_grain.py` — harness (deterministic, integer-only verdict path)
- `q1-class-grain-output.txt` — raw output (sha256 f4a526a8…)
- this report
