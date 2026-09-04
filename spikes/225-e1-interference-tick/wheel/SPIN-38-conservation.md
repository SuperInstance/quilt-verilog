# SPIN-38 — CONSERVATION (debt-ceiling law on the E1 fabric)

Lane: wheel_spin38_conservation (zai/glm-5.3). Run: 2026-09-04 08:19 UTC
(44 s wall). Script: `wheel/spin38_conservation.py` (hypothesis + decision
rule pre-registered verbatim in the header BEFORE running); raw output:
`wheel/spin38-output.txt`. Nothing committed or pushed; WHEEL-LOG untouched.

## Hypothesis (pre-registered in script header)

H1: at fixed grammar (outlier@30, worst by SPIN-15's stable debt/ev ranking)
the debt ceiling under escalation is a conservation constant f(drift, delta)
only — (a) ceiling scales ~linearly with drift, (b) monotone in delta,
(c) the cap is REACHED within the run (last-window debt rate < 50% of
first-window) in ≥ half the delta≤6 cells, (d) evap/event stays in
0.17–0.30, (e) closure Δ = 0 / mass Δ = 0 everywhere. H0: unbounded or
non-monotone (>10% zig-zag) in drift/delta, evap band breaks, or identity
fails. Full numeric decision rule verbatim in the script header.

## Arms

outlier@30 grammar (N=6, lats [0,0,0,0,0,30]), pd=3, **ticks = 38400 (8×
the 4800 base)**, drift ∈ {0, 96, 192, 384, 768} × delta ∈ {1, 6, 12} ×
K ∈ {1, 2} = 30 cells × 5 seeds {1, 7, 42, 1999, 20260902} = 150 runs,
all real. Debt trajectory recorded as 8 windows of 4800 ticks. Integer-only
in every loop; floats display-only. Fabric = verbatim inline clone of
spin15's canary-proven ledger clone (floor-div decay, expiry-evaporation
channel).

## Canaries — ALL PASS

- **(a) wiring byte-identity:** 8/8 configs vs `exp_glm1.run_fabric`,
  deliberately including escalated parameters (drift 768/delta 1, drift 0,
  drift 384) — identity holds in this spin's actual operating region.
- **(b) anchor replays EXACT:** zero@15 K=1 → 77.3% / ev 8756 / debt
  187834; ladder@15 K=1 → 71.5% / ev 5792 / debt 106378 — all exact.
- **(c) SPIN-15 replay:** ladder@30 K=1 drift=384 debt/ev = **9202.3**
  (SPIN-15: 9202.4) PASS. Note: the brief said "outlier@30" but SPIN-15's
  saturation hunt ran on ladder@30 (worst by residency); replayed ladder@30
  for the anchor and recorded outlier@30 = 9181.9 alongside (the two worst
  grammars are within 0.3% — the brief's confusion is benign).
- **(d) double-run determinism:** 4/4 configs byte-identical (full ledger
  keys).

## Results (all real runs)

1. **No debt ceiling anywhere at stress.** Every drift≥96 cell grows
   linearly-or-faster in-window; last/first-window debt-rate ratio r =
   0.91–4.44 (never < 0.5). K=2 is RUNAWAY SUPERLINEAR: debt-rate ratio
   grows within the run (r = 1.85 at drift 96 → 4.44 at drift 768) —
   SPIN-15's "+9–12 debt/ev K=2 pathology" is a divergence, not a tax.
2. **The delta dimension COLLAPSES.** At every drift ≥ 96, total debt is
   delta-INVARIANT to ~0.1% (e.g. drift=384 K=1: 2.95729 B / 2.95717 B /
   2.95756 B at delta 1/6/12). SPIN-15's "hard-capped ~460k under delta→1"
   was a duration artifact: at 8× duration debt grows 8× at every delta.
   The ceiling is NOT f(drift, delta) — it is f(drift, K) with delta gone.
3. **Drift scaling is monotone but sub/super-linear, not linear.** Debt
   ratios per drift doubling: K=1: 4.27, 4.25, 2.24 (concave — saturation
   of the *rate*, not of the total); K=2: 2.46, 2.04, 2.88 (convex again at
   the top — the runaway). H1a's [0.8, 1.25] linear window fails on every
   (delta, K).
4. **Events saturate at 99.98% occupancy** at stress (230,394 / 230,400
   possible twin-ticks) — reproduces and sharpens SPIN-15's 99.85% event
   ceiling. Events, like debt, are delta-invariant at stress.
5. **Evap band BREAKS: 0.093–0.351** (H1d falsified). Evap/event tracks
   (drift, K), not a universal constant: K=2 at drift 0 → 0.093–0.127;
   K=2 at drift ≥ 96 → 0.31–0.33; K=1 spans 0.16–0.33. SPIN-15's
   0.17–0.30 band was a property of its sampled region, not a law.
6. **Identities hold everywhere:** closure Δ=0, Σtolls, pulse-flow (with
   expiry channel), g-trajectory — 4/4 on all 150 runs + all canary runs.
7. drift=0 curiosity: debt is still 3.1–4.8 M (drift is not required for
   debt; stale reads + echo divergence suffice), and K=2 is the only cell
   with a >10% delta zig-zag (4.83 M / 3.15 M / 3.92 M) — the drift-free
   regime is where delta still matters.

## Verdict (per pre-registered rule)

**FALSIFIED.** H1a breaks (no linear drift scaling), H1b breaks (K=2
drift=0 zig-zag; and at stress the delta axis is flat, which the rule's
"consistent direction" reading cannot rescue as the hypothesized tightening
law), H1c breaks (0/20 cells saturate — debt never caps), H1d breaks (evap
0.093–0.351). Only H1e (identity conservation) holds.

## Headline number

**Debt at outlier@30, 38,400 ticks is delta-INVARIANT (±0.1%) and unbounded
in drift: 163 M → 696 M → 2.96 B → 6.62 B at K=1 — SPIN-15's "~460k
delta-cap" was a duration artifact, and the true conservation structure is
f(drift, K): events pinned at 99.98% occupancy, K=2 divergence superlinear
(last/first window rate ratio 4.4 at drift 768).**

## Scars / honest bookings

- The pre-registered rule's H1b wording ("tightens with delta") was
  ambiguous under a flat delta axis; scored as a break and reported — no
  post-hoc reinterpretation.
- Window-rate analysis is coarse (8 windows); the K=2 superlinearity
  exponent is not fitted, only bracketed by ratios.
- drift=0 / K=2 zig-zag is a single-cell effect; no mechanism chased.
- Evap sign structure still unmeasured (SPIN-15 scar carried forward).

## Next-spoke proposal

**DEBT-RATE LAW (conservation follow-up):** fit the exact debt-rate
law d(debt)/dt = Φ(drift, K) on outlier@30 — K=1 looks concave-saturating
in drift (rate doubling ratio 4.25→2.24), K=2 convex; test whether
Φ = (drift term) × (K-resonance factor) separates, and whether K=2 runaway
diverges or re-saturates at 32× duration. Cheap (one sweep, ~1 min), direct
successor to the collapsed-delta finding.
