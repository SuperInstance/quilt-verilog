# SPIN 9 — SPOKE: GRAMMAR-LAW (the 2-parameter fit proposed by SPIN-5)

**Lane:** wheel_spin9_grammar_law · **Date:** 2026-09-03 ~07:35 AKDT ·
**Files:** `spin9_grammar_law.py`, `spin9-output.txt` · Fabric:
`inventors-derby/exp_glm1.run_fabric` (E1 contract items pinned). Integer-only
inside the loop; floats only in display statistics and post-hoc law fits
(PAV isotonic, additive two/three-way, rank-1 interaction, Spearman).
Dispatched by SPIN-5's GRAMMAR-LAW proposal (not the LCG pick). Full run
~55 s, ~660 fabric runs.

## Parameters (pinned)

- **Stale-mass** m_s = Σᵢ max(0, latᵢ − δ/2) / (N·(30 − δ/2)) at spread 30 —
  excess lag mass above the coherence threshold δ/2 = 6, normalized
  (denominator 144; all-30 would be 1.0, the spread-30 constraint caps at
  0.833).
- **K** ∈ {1, 2, 4, 8} replication.
- **fresh** (candidate third parameter, discovered mid-spin): coherent fresh
  cohort = # twins at lag ≤ δ/2.

## Hypothesis space (as briefed)

- **H1 (grid fit):** true% ≈ smooth f(m_s, K) — first-order law; report R²
  and failure map.
- **H2 (K-interaction):** Spin-5's claim "K flips orderings" — characterize
  the flip surface over 4 grammars × K ∈ {1,2,4,8}.
- **H3 (spread=12 bump, PRIORITY):** real resonance (period-locked,
  phase-local, survives iso-spread perturbation, tracks δ) or instrument
  scar (tick/lag quantization against δ=12)?

## Operationalization

N=6, interference arm, 4800 ticks (9600 for periodograms), stress
(δ=12, drift=6, pd=3), seeds {1, 7, 42, 1999, 20260902}. **EXP1:** 20
grammars at spread 30 (each contains a 0 and a 30; 15 distinct m_s levels
0.167–0.833; deliberate structural duplicates: 3 grammars at m_s=1/6, 4 at
7/24, 2 at 5/12) × K{1,2,4,8} × 5 seeds. **EXP2:** 7 grammars (6 grid +
zero-lock control) × K. **EXP3:** spread 9–14 × ladder/cohort; phase-folded
residency (24 bins over reality period 240); per-lag fire counts split
up/flat/down phase; event-train periodogram (periods 2–120, 9600 ticks);
five iso-spread-12 lag sets; δ ∈ {10, 14} co-move probes.

## Self-canaries (both PASS — mandatory gate)

1. **A — wiring byte-identity:** helper-built lats ≡ literal lats, full
   resid+cflags traces, 10/10. PASS.
2. **B — SPIN-5 replay:** zero@30 K=1 per-seed (791,755,775,780,762) and
   ladder@30 K=1 (264,253,266,281,274) EXACT; events 8756/14952 and debt
   187834/366275 exact. PASS. (Cross-check: zero K=8 = 69.0 matches the
   novel lane's published anchor.)

## Results

### EXP 1 — the (m_s, K) grid: first-order law YES, complete law NO

Fits on 80 grammar×K cells (5-seed means; per-seed spread 1–4‰):

| fit | R² |
|---|---|
| F1 additive μ + a(m_s) + b(K) | **0.779** |
| F1b additive μ + a(fresh) + b(K) | **0.809** |
| F1c additive μ + a(fresh) + c(m_s) + b(K) | **0.877** |
| F2 per-K isotonic in m_s (PAV) | 0.923 / 0.971 / 0.984 / 0.988 (K=1/2/4/8) |
| F2 pooled within-K isotonic | **0.973** |
| F3 = F1 + rank-1 interaction | 0.780 (+0.001 — nothing) |

- **First-order law VALIDATED:** within fixed K, m_s is a strong monotone
  predictor — Spearman(m_s, true%) = −0.91/−0.82/−0.95/−0.96 at
  K=1/2/4/8; more stale mass is worse, at every K, 20/20 grammars
  consistent per seed.
- **Completeness FALSIFIED:** grammars sharing an m_s level differ by up
  to **33.8pp** (m_s=7/24: g2 20.2% vs stag 50.3%; m_s=5/12: ladder 26.8%
  vs d24 49.9%) — 10–30× the seed swing (~1–4pp). The additive law's
  worst residuals are exactly these: g2 −24.7pp, d24 +19.1pp.
- **The missing axis is the coherent fresh cohort** (mass at lag ≤ δ/2):
  fresh alone orders K=1 better than m_s alone (0.809 vs 0.79 cell-fit;
  fresh×K cell means at K=1: 14.8 / 24.6 / 51.9 / 50.5 / 54.3 for
  fresh=1..5). What kills a grammar is not how much stale mass it carries
  but **whether its fresh mass is coherent or grated across the danger
  zone**: bimodal 0-vs-stale splits (out5_1, m24, stag, d24, c3_3) all sit
  45–58% at K=1 regardless of m_s 0.17–0.50, while graded mid-lag
  grammars (g2, ladder, g3 — lags scattered through 4–24, mutually
  incoherent) collapse to 10–30%.
- fresh and m_s are anticorrelated by design here, so F1c's split between
  them is partly degenerate; the honest statement is a 2.5-parameter law:
  **true% ≈ g(fresh-cohort, K) with m_s as the within-level tilt**, R²
  0.877, residual failures = the graded family (still overpredicted) and
  coherent-stale splits (still underpredicted — a coherent stale block
  {24,24,30} beats a graded tail at equal m_s; intra-stale coherence is
  the next refinement, booked).

### EXP 2 — K-flip surface: VALIDATED, SHARPENED, and it HEALS

| grammar | fresh | K=1 | K=2 | K=4 | K=8 | Δ(K8−K1) |
|---|---|---|---|---|---|---|
| out5_1 [0,0,0,0,0,30] | 5 | 53.2 | 47.4 | 66.6 | 67.3 | **+14.1** |
| m24 | 4 | 50.0 | 54.1 | 50.1 | 52.6 | +2.6 |
| q4_2 | 4 | 45.4 | 53.4 | 45.4 | 47.9 | +2.5 |
| d24 | 3 | 49.9 | 34.6 | 29.9 | 30.7 | −19.2 |
| ladder | 2 | 26.8 | 28.9 | 12.8 | 14.0 | −12.8 |
| c3_3 | 3 | 49.3 | 33.3 | 21.7 | 21.7 | **−27.6** |
| zero0 control | 6 | 77.3 | 50.0 | 73.9 | 69.0 | −8.3 |

- **Flips are real but transient:** pairwise rank inversions 6/15 at
  K1→2 (Spearman +0.46), 4/15 at 2→4, **0/15 at 4→8 (+1.00 — the ordering
  freezes)**. "K flips orderings" is a low-K phenomenon.
- **The flip surface is the fresh-cohort crossing:** fresh-majority
  grammars RISE with K (fresh=5: +12.7pp mean, K1→K8), stale-coherent
  grammars FALL (fresh=3: −13.1pp). The fresh×K cells cross between
  fresh=3 and 4: at K=1 the order is 5>4>3>2>1, at K=8 it is 5>4>3 with
  3 far below where it started (51.9→38.8).
- **K=2 is the global worst K** (additive b(K) = +0.0/−0.9/−5.1/−3.6pp):
  the echo-overlap penalty (SPIN-5's mechanism) peaks at K=2 — the
  previous tick's half-decayed pulse stacks same-sign onto the fresh
  overshoot; at K≥4 the tail spreads and per-tick overlap shrinks.
- **Spin-5's zero-lock reading was a K=2 snapshot artifact:** zero falls
  77.3→50.0 at K=2 but RECOVERS to 73.9 (K=4) / 69.0 (K=8). The
  synchronized-choir penalty is not monotone in K either.

### EXP 3 — the spread=12 bump: INSTRUMENT SCAR, not resonance (PRIORITY)

Densified ladder K=1 (mean of 5 seeds; every per-seed gap ≥ 25‰):

| spread | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|
| ladder % | 97.2 | **93.5** | 96.9 | 95.0 | 95.7 | 84.4 |
| cohort % | 89.0 | 75.9 | 75.0 | 64.3 | 62.8 | 55.4 |

- **The "bump at 12" inverts:** with both neighbors measured, 12 is
  ordinary plateau; **10 is the anomaly** — a local dip 3.8pp below its
  higher neighbor, below BOTH neighbors, all 5 seeds.
- **No resonance signature anywhere:**
  1. *Periodogram* (9600 ticks, periods 2–120): identical top periods at
     spread 11/12/13 — 80/40/120, i.e. reality's own 3-phase harmonics
     (240/3, /6, /2). No spread-specific period appears or moves.
  2. *Phase-fold:* the residency deficit sits at the up-ramp start (bin
     0–10: 71–130‰ vs 400‰ elsewhere) at ALL of 11/12/13 — no localized
     bump anywhere.
  3. *Cohort control:* strictly monotone 89.0→55.4, no feature at 12.
  4. *Iso-spread perturbation* (5 different lag sets, spread 12):
     91.6–96.3% — the rounded default set (95.0) is nothing special.
- **The scar's mechanism is quantization against the firing threshold.**
  A mid-lag twin fires on ramps iff (8/5)·lag > δ ⟺ lag ≥ 8 at δ=12.
  round(i·s/5) straddles that boundary non-monotonically: ladder(9) puts
  every mid lag below it ({5,7} → 11.2 ≤ 12, never fire) — an accidental
  5-fresh-cohort grammar → 97.2%; from s=10 the crossing pattern changes
  every spread ({8,10} vs {9,11} vs {10,12} vs {8,10,13} …), producing
  ±2–4pp lattice wobble uncorrelated with spread itself.
- **Δ co-move seals it:** the dip sits at spread **10** at δ=10
  (97.1→92.3), δ=12 (97.2→93.5), AND δ=14 (97.1→94.5) — it tracks the
  ladder(10) lattice (the only uniform spacing-2, all-even lag set), NOT
  δ. A resonance against δ=12 would have moved with δ; this doesn't.
- **Serendipitous booking (for the novel lane's N3):** the δ co-move doubles
  as a 3-point knee-scaling measurement: collapse onset ≈ 12 at δ=10,
  ≈ 15 at δ=12, > 14 at δ=14 → knee ≈ 1.2–1.25·δ — the slope-adjusted 2Δ
  law (SPIN-5's knee finding) holds across δ, not just at δ=12.

## Verdict: MIXED

- **H1 (2-parameter law): MIXED.** First-order law VALIDATED — within-K
  monotone in m_s, pooled isotonic R² = 0.973, Spearman −0.82…−0.96.
  Complete description FALSIFIED — same-m_s grammars differ by up to
  33.8pp; additive (m_s, K) R² = 0.779; rank-1 interaction adds nothing.
  The grammar dial's true second axis is the coherent fresh cohort;
  (fresh, m_s, K) reaches R² = 0.877 with identifiable residual structure
  (graded-mid-lag family toxic beyond all three parameters).
- **H2 (K-flip): VALIDATED and SHARPENED.** Flips concentrate at K=2 and
  heal completely by K=4→8 (0/15 inversions); the flip surface is the
  fresh≥4-rising / fresh≤3-falling crossing; K=2 is the global worst K;
  zero-lock's "fall" recovers at K≥4.
- **H3 (bump): RESOLVED — INSTRUMENT SCAR.** The reproducible feature was
  real (all seeds) but misread: it is a dip at spread 10 (present at all
  three δ), a lattice artifact of round(i·s/5) against the discrete
  (8/5)·lag > δ firing threshold. No period, no phase locality, no
  iso-spread specificity, no δ-tracking. Not new physics — and the
  knee-δ scaling it surfaced on the way out IS new support for the
  slope-adjusted knee law.

## Headline numbers

1. **Law:** pooled within-K isotonic R² = 0.973 (Spearman −0.82…−0.96) —
   but 33.8pp same-m_s structural spread kills the 2-parameter claim;
   (fresh, m_s, K) additive R² = 0.877.
2. **K-flip:** inversions 6/15 → 4/15 → **0/15** (K1→2→4→8); flip =
   fresh-cohort crossing: out5_1 +14.1pp vs c3_3 −27.6pp (K1→K8); K=2 is
   the worst K on average (−5.1pp vs K=1 at K=4… b(K) +0/−0.9/−5.1/−3.6).
3. **Bump:** re-read as dip-at-10: 97.2/**93.5**/96.9 at spreads 9/10/11,
   recurring at δ ∈ {10,12,14}; periodogram shows only reality's own
   80/40/120 harmonics at every spread; knee scales ≈ 1.2–1.25·δ
   (onset 12/15/>14 at δ=10/12/14).

## Scars / honest boundaries

- **Instrument scar (booked, closes SPIN-5's open item):** the spread=12
  "fine structure" was a 2-point comparison (10 vs 12) whose reading
  inverts when both neighbors are measured. Rule: claim a local feature
  only with BOTH neighbors on the grid.
- **My own scar:** first-run F3 printed R² = 0.707 < F1's 0.779 —
  impossible for a nested model; I had mixed level-mean residual SS with
  cell-level SS. Fixed to cell-level prediction (0.780). Rule: nested
  model comparisons must be scored from predictions at the same
  granularity as the base model.
- fresh vs m_s are anticorrelated by construction in this grid (bimodal
  splits have both low m_s and high fresh); F1c's coefficient split
  between them is not fully identifiable from this design alone. The
  falsification of 2-parameter completeness (within-m_s spread) is
  design-independent; the (fresh, m_s) attribution wants an orthogonal
  grid (fixed fresh, vary m_s) — booked as the follow-up's first rung.
- 5 seeds × permille means only; no inferential claims. Per-seed
  consistency was 5/5 for every ordering statement quoted.
- Sequential arm untouched this spin (SPIN-5 established
  multiplicity-blindness); all law statements are interference-arm.

## New spoke proposed: YES — ORTHOGONAL-GRAMMAR (fresh × stale-mass decoupled)

The 3-parameter law wants an orthogonal design: fix fresh ∈ {2,3,4} and
sweep stale-mass at fixed spread (e.g. fresh=4 with the stale dyad at
{10,30}/{20,30}/{24,30}/{30,30} — wait, that last one changes fresh) —
concretely: fresh=3 + stale trio graded vs coherent at matched m_s, plus
the intra-stale coherence axis ({24,24,30} vs {20,25,30} vs {18,24,30})
that the residual map points at. Also rung 2 of the knee-Δ scaling
(δ ∈ {6,9,18,24}) to pin or break c ≈ 1.25 before the novel lane's N3
claims it. Either the 3-param law pins at R² > 0.95 or the grammar dial
is irreducibly spectral.

## Log-ritual bookkeeping

This spin was dispatched by SPIN-5's GRAMMAR-LAW proposal (not the LCG
pick). LCG advance for next cycle: 2035015474 → **368800899** → mod 10 =
**9** (SILICON). The wheel ledger resumes LCG selection at the next cycle.

VERDICT: MIXED — (m_s, K) is a validated first-order monotone law (pooled isotonic R²=0.973) but falsified as complete (33.8pp same-m_s spread); the true second axis is the coherent fresh cohort (3-param R²=0.877); K-flips are real, K=2-localized, and heal by K=4→8 (0/15 inversions); the spread=12 bump is an instrument scar — a lattice dip at spread 10 recurring at all three δ, no resonance signature — while the knee-δ scaling it surfaced (knee ≈ 1.2–1.25·δ) independently confirms the slope-adjusted knee law.
