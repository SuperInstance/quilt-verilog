# KNEE-META — every published knee in unified units (span·σ)/(2Δ)

**Lane:** zero-compute meta-analysis (SPIN-20 question #4 / U1+V1) · branch `g3-kinduction` · 2026-09-03
**Method:** pure re-analysis of published numbers — no new simulation. Every value below is quoted from a
committed artifact (hash per row). Arithmetic in exact fractions (integers) wherever the inputs are integers;
decimals only where the published statistic itself is decimal.

## The unified unit

**r = (span·σ)/(2Δ)** where span = max−min twin latency (the knee's native variable for spread knees),
σ = reality's sustained per-tick slope, 2Δ = the deadband budget. Fabric defaults: Δ=12 → 2Δ=24;
R0 reality slope σ = 8/5 = 1.6 exactly (ramp96 @+8/5, band 353–553) — published at
`spin5-output.txt:54` ("slope-adjusted 2*DELTA crossing = 15 ((8/5)*15=24)") and in SPIN-21's trace table.
tri3 reality σ = 3 (SPIN-10's booking). SPIN-21's refinement — the knee-relevant slope is the
**slowest sustained** slope a stale twin can ride — is adopted throughout (σ per row).

For firing-mass walls (knee variable is headcount N, not span) the unified span-coordinate is **degenerate:
r_span = 0** (zero-lock / fully-compensated grammars); these are instead normalized as **m = N_wall/(2pd+1)**.

## Class S — staleness / slope knees (span-budget mechanism)

| # | source | knee (as published) | σ | 2Δ | unified r (exact) | commit |
|---|--------|--------------------|-----|-----|-------------------|--------|
| 1 | SPIN-4-knee (ladder N=6 K=1) | spread ≈ 15 (93.5→71.5→49.2 @10/15/20) | 8/5 | 24 | 15·(8/5)/24 = 24/24 = **1.00** | `f499eda` |
| 2 | SPIN-5-knee onset | 14–16, steepest at 15 (84.4→71.5) | 8/5 | 24 | 14/15 … 16/15 = 0.933–1.067, center **1.00** | `7452ee7` |
| 3 | SPIN-5-knee 50%-crossing | 19.61 | 8/5 | 24 | (961/49)·(8/5)/24 = 961/735 ≈ **1.31** | `7452ee7` |
| 4 | SPIN-8-rho knee | 0.78·2Δ (= 18.72 @ δ=12) | 8/5 | 24 | (39/50)·(8/5) = 156/125 = **1.248** | `0a66572` |
| 5 | SPIN-9 knee-δ law | onset 12 @δ10 / 14–15 @δ12 / >14 @δ14 (knee ≈ 1.2–1.25·δ) | 8/5 | 2δ | 24/25, 14/15…1, ≥4/5 → **0.96–1.00** | `8aa156e` |
| 6 | SPIN-10-span anchor | e1 knee: 1.6·15 = 24 = 2Δ | 8/5 | 24 | **1.00** (the proposal's own anchor) | `7c769fd` |
| 7 | SPIN-10-span tri3 cliff | even1 span 5 → 100.0 healthy; even2 span 10 → 48.1 collapsed; boundary bracketed 5 < b ≤ 10 | 3 | 24 | 5/8 … 5/4 → bracket **(0.625, 1.25]** | `7c769fd` |
| 8 | SPIN-21 knee, R0/R2/R6 | knee 14 (argmax drop) | 8/5 | 24 | 14·(8/5)/24 = 14/15 ≈ **0.93** | `90d5357` |
| 9 | SPIN-21 knee, R4 | knee 27 (pred 24) | 1 | 24 | 27/24 = 9/8 = **1.125** (pred 1.00) | `90d5357` |
| 10 | SPIN-21 knee, R5 | knee 10 (pred 12) | 2 | 24 | 20/24 = 5/6 ≈ **0.83** (pred 1.00) | `90d5357` |
| 11 | SPIN-21 knee, R1 | knee 20; 50%-crossing 23.7 (pred 2Δ/min-slope = 384/17 ≈ 22.6) | 17/16 | 24 | 85/96 ≈ **0.885**; 50%: 1343/1280 ≈ **1.049** | `90d5357` |
| 12 | O7 raw bundle wall (stress, K=4, spacing 10) | wall N=3–4: 91.0 → 34.5 → 12.2; spans 10/20/30 | 8/5 | 24 | 2/3 → 4/3 → 2: edge brackets **1** (N=2 @ 0.67 healthy, N=3 @ 1.33 collapsed) | `0a637a1` |
| 13 | O7 raw bundle wall (calm, Δ=6, spacing 5) | wall N=3–4: 73.4 → 46.5 → 13.3; spans 5/10 | 8/5 | 12 | 2/3 → 4/3: **same bracket at halved budget** (2Δ and span both halved — self-consistency check) | `0a637a1` |
| 14 | SPIN-17 amplitude gate (P=16 K=2) | tax 27.0pp @ amp 25; 22.8 @ 15; 0.6 @ 5 | 8/5 | 24 | amp·σ/2Δ = 5/3, **1.00**, 1/3 → gate's upper edge sits exactly at **r = 1** | `31904d7` |

## Class M — firing-mass / co-fire walls (r_span = 0; unified m = N_wall/(2pd+1))

| # | source | knee (as published) | r_span | unified m | commit |
|---|--------|--------------------|--------|-----------|--------|
| 15 | SPIN-8-gran wall | divergence iff N > 2pd (pd=3: N=7 → 0.1%); duplicate-bloc M=6→0.2% vs M=5→53.0% | 0 | 7/7 = **1.00** | `0a66572` |
| 16 | SPIN-11-pd-wall pd=1 | edge N=3 | 0 | 3/3 = **1.00** | `bc24cab` |
| 17 | SPIN-11-pd-wall pd=2 | edge N=5 | 0 | 5/5 = **1.00** | `bc24cab` |
| 18 | SPIN-11-pd-wall pd=3 | edge N=7 | 0 | 7/7 = **1.00** | `bc24cab` |
| 19 | SPIN-11-pd-wall pd=6 | edge N=13 | 0 | 13/13 = **1.00** | `bc24cab` |
| 20 | SPIN-11-pd-wall pd=12 | NO wall through N=25 (echo factor 1.08 too slow to outrun decay in window) | 0 | m=1.0 but **inert** — the class's own rate-condition, not scatter | `bc24cab` |
| 21 | O7 compensated co-fire wall | comp arm degrades from N≈7 (86→74→61→43), all lats → 0 | **0 exact** (co-located) | 7/7 @ pd=3 = **1.00** | `0a637a1` |
| 22 | SPIN-16 θ-gate partition theorem | gate opens ⟺ nf ≥ 2pd+1 (proved, not fitted) | 0 | **1.00 by proof** | `59aac85` (pre-reg `2dacb9d`) |

## The one knee on neither axis — SPIN-17 resonance

| # | source | knee | unified coordinate | commit |
|---|--------|------|--------------------|--------|
| 23 | SPIN-17 K=2 tax spectrum | peak at P=16 (27.0pp), τ ≈ 131 | **P_peak·s_knee = 16·15 = 240 = T_reality, integer-exact**; τ ≈ T/2 = 120. Lives on the reality-cycle axis, not on 2Δ — and is only admitted through the Class-S gate (row 14: no tax unless amplitude crosses the r=1 budget) | `31904d7` |

## Collapse verdict

**Single-constant collapse: REJECTED. TWO constants emerge, split by mechanism class.**

1. **Class S → r ≈ 1.** All 15 measured span-knee points land in r ∈ [0.83, 1.33]; the 13 onset-statistic
   knees land in [0.83, 1.13] with canonical center exactly 1.00 (SPIN-4/5/10's 15·1.6=24). The three
   mid-curve statistics (SPIN-5 50%-crossing 1.31, SPIN-8 ρ-knee 1.25, SPIN-21 R1 50% 1.05) form the second
   shell at ≈ 1.25 — **the published "0.75·2Δ" family is the mid-curve statistic of the same r = 1 boundary**
   (0.75·σ = 0.75·8/5 = 1.2), not a separate law. SPIN-9's 1.2–1.25·δ and SPIN-10's (max−min)·σ ≲ 2Δ and
   SPIN-21's 2Δ/slowest-slope are the same constant in three costumes. Consolidation: 5 beacons → 1 law,
   **span·σ_slowest ≈ 2Δ**.
2. **Class M → m = 1 exactly, r_span = 0.** Five independent walls (SPIN-11 edges 3/5/7/13, SPIN-8's
   granularity wall, O7's compensated wall) plus a proof (SPIN-16 partition theorem) collapse onto
   N_wall = 2pd+1 with zero span. They cannot collapse onto Class S's constant — every one of them sits at
   r_span = 0 while diverging.

**The named physical distinction: a staleness BUDGET vs a co-fire GAIN.**
Class S is a continuous, geometric, memoryless budget: twins riding different points of reality's slope
accumulate pairwise decorrelation ≈ |lag_i − lag_j|·slope, and residency fails when that product crosses the
deadband 2Δ — losses are graceful, slope-driven (move the trace's slope and the knee moves inversely,
SPIN-21 rows 8–11), reversible with zero hysteresis (SPIN-16-regime, `31904d7`), and rescuable by any
lag-compensation or scheduling that shortens effective span (O7 raw wall: N=4 at 12.2% → 86.3%).
Class M is a quantal multiplicative gain: co-located twins co-fire as one bloc, the net shove scales
~N·‖e‖/pd, and divergence is the echo factor |1−N/pd| exceeding 1 fast enough to outrun decay — it needs no
span at all (survives span = 0), is catastrophic not graceful (0.1–2.3% at the wall), is invisible to phase
scheduling (SPIN-16 EXP3: AS rescues none of the wall grammars), and yields only to mass compensation or the
θ-gate. **O7 is the cleanest adjudicator: one experiment, both walls — its raw wall collapses onto r=1, its
compensated wall onto m=1.**

The resonance (row 23) is a third coordinate — the reality cycle T, entering as P_peak·s_knee = T exactly —
but it is gated by Class S (amplitude must cross the budget before any tax exists), so it couples the two
axes rather than breaking the two-class picture.

## Caveats (booked honestly)

- Statistic choice matters within Class S (onset 1.00 vs mid-curve ≈ 1.25); both shells are reported rather
  than absorbed — the tri3 boundary (row 7) is bracketed (0.625, 1.25], unmeasured (the 15-min tri3 confirm
  of SPIN-20 #4 remains the one open leg).
- Metric dependence (SPIN-16-regime, `31904d7`): in absolute residency, spread→residency is monotone
  (5→97.6, 15→71.5, 30→26.8) — the knee is a drop-rate/curvature feature; rows quote each source's own
  registered knee statistic.
- O7 raw rows are K=4 (grid default), the only non-K=1 knees in Class S; their brackets, not points.
- Plateau reality (R3, σ=0) has no knee mechanism (SPIN-21) — the r=0 origin is the span law's degenerate
  point (SPIN-10's origin-dip booking), excluded by construction.
- tri3 σ=3 is quoted from SPIN-10's published booking (`7c769fd`), not independently re-derived here.

## Provenance

Commits: `f499eda` (SPIN-4), `7452ee7` (SPIN-5), `0a66572` (SPIN-8), `8aa156e` (SPIN-9), `7c769fd`
(SPIN-10), `bc24cab` (SPIN-11), `2dacb9d`/`59aac85` (SPIN-16), `31904d7` (SPIN-17 + SPIN-16-regime),
`90d5357` (SPIN-21), `0a637a1`/`009e736` (O7 numbers/verdict). Raw anchors: `spin5-output.txt:51-54`
(19.61, 84.4→71.5, (8/5)·15=24), `spin9-output.txt:238-254` (δ-co-move onsets), `o7-bundle-wall-output.txt`
(wall tables), `spin8-output.txt:133-135` (duplicate-bloc discriminator, wall N=M+1>2pd).
