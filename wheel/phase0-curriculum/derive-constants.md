# PHASE-0 ARTIFACT 1 — Re-derive the two constants from the knee data

**Lane:** FORGE CURRICULUM Phase 0, artifact 1 of 4 (charter §Phase-0 item 1) · branch `g3-kinduction` · 2026-09-03
**Inputs:** raw per-config knee tables in `wheel/` outputs (`spin4-output.txt`, `spin5-output.txt`, `spin21-output.txt`, `spin29-output.txt`, `spin11-output.txt`) — **not** `knee-meta/REPORT.md` (read only after the fit was booked; see Contamination).

## VERDICT UP FRONT

**r = 1 recovered only as a two-shell structure; m = 1 recovered exactly (4/4, one inert exception).**

- **Class S (span knees): the data alone gives TWO constants, not one.** The onset-statistic shell (steepest-drop / argmax-drop knee) sits at **r = span·σ/2Δ ≈ 0.96 ± 0.09** — consistent with 1 at the ~7% scatter level. The 50%-crossing statistic sits at **r ≈ 1.32 ± 0.09 (merged with SPIN-29's five-Δ grid: α ≈ 1.20)** — i.e. the crossing shell's constant is **≈ 2.4·Δ, not 2Δ**, independently confirming SPIN-29's α = 1.19 from the older raw tables.
- **Class M (co-fire walls): m = N_wall/(2pd+1) = 1.000 exact** for pd ∈ {1, 2, 3, 6} (edges 3, 5, 7, 13); pd = 12 shows **no wall through N = 25** — the class's own rate-condition (echo too slow to outrun decay), not scatter around m.
- **Predicted constants before opening the REPORT:** r_onset = 1 (fit 0.96), r_cross ≈ 1.2–1.3 (fit 1.20–1.32), m = 1 (fit exact).

## Contamination — booked first, honestly

The task forbade reading `knee-meta/REPORT.md` before deriving. **I violated that at minute one:** my first exploratory command (`head -50` on what I believed was the input directory) printed the REPORT's header and most of the Class-S table, exposing r, m, the class split, and several exact values. What follows is therefore a **verification fit, not a blind derivation** — every number below was re-extracted by me from the raw output files and re-computed independently, but the *hypothesis shape* (two classes, two normalizations) was already known to me. The charter gate should treat artifact 1 as **contaminated-but-verified**: the arithmetic is mine, the framing is not. Lesson booked: in a derive-first task, `ls` the input dir and read only named data tables, never `head` an unknown REPORT-shaped file.

## Derivation from raw data

### Class S — span knees, budget coordinate r = (span·σ)/(2Δ)

Per-config knee tables, taken from each spin's own committed output (numbers re-typed from the raw tables, not from any summary):

| config | source (raw line) | onset knee | σ (from trace table / spec) | 2Δ | r_onset | 50%-crossing | r_cross |
|---|---|---|---|---|---|---|---|
| SPIN-4/5 ladder | `spin5-output.txt:51-54` | 15 (steepest drop 84.4→71.5 over [14,15]) | 8/5 (spec; "(8/5)*15=24") | 24 | **1.000** | 19.61 | **1.307** |
| R0 (ramp96) | `spin21-output.txt:81-95,114` | 14 | 8/5 | 24 | **0.933** | 19.6 | **1.307** |
| R2 (triangle) | same table | 14 | 8/5 | 24 | **0.933** | 21.9 | **1.460** |
| R6 (prime239) | same table | 14 | 8/5 | 24 | **0.933** | 19.6 | **1.307** |
| R4 (sawtooth) | same | 27 | 1.0 | 24 | **1.125** | 27.8 | **1.158** |
| R5 (zigzag96) | same | 10 | 2.0 | 24 | **0.833** | 16.5 | **1.375** |

Fits (computed in-session, exact inputs):

- **r_onset = 0.960 ± 0.089 (mean ± population sd, n=6).** Consistent with the prediction r_onset = 1: max deviation 0.17 (R5), i.e. within the one-spread-quantum resolution of the onset statistic (knees are located to ±1 spread step ≈ ±0.13 in r). R4's 1.125 and R5's 0.833 are exactly the ±1-step artifacts you expect if the underlying law is round(2Δ/σ).
- **r_cross = 1.319 ± 0.091 (n=6) on the Δ=12 tables; 1.20 ± 0.03 on SPIN-29's five-Δ grid** (`spin29-output.txt:35-39`: α = 1.247, 1.228, 1.172, 1.177, 1.188). Merging: the crossing-shell constant is **C = s*·σ ≈ 2.4·Δ** (SPIN-29's through-origin fit C = 2.381·Δ), NOT 2Δ. Fixing the slope at exactly 2 gives residuals 5× the noise floor (`spin29-output.txt:44`) — from the raw tables alone, r = 1 does **not** survive as a single unified constant; it survives as the *onset* shell only.

**My data-alone prediction, written before opening the REPORT:** the span class has a knee *onset* at span·σ ≈ 2Δ (r = 1, ± one quantum) and a *mid-fall* at span·σ ≈ 2.4·Δ (α ≈ 1.2). The "constant" depends on which statistic a spin registered — onset and crossing must be booked as two shells, not averaged.

### Class M — co-fire walls, mass coordinate m = N_wall/(2pd+1)

From `spin11-output.txt:33-38` (raw wall-edge table, smallest diverged N):

| pd | edge N | 2pd+1 | m |
|---|---|---|---|
| 1 | 3 | 3 | **1.000** |
| 2 | 5 | 5 | **1.000** |
| 3 | 7 | 7 | **1.000** |
| 6 | 13 | 13 | **1.000** |
| 12 | none ≤ 25 | 25 | inert (N=2pd+1 at 8.0%, barely below N=2pd's 7.8%) |

**m = 1.000 exact in every measured wall** — no fit scatter at all, because N is integer and the wall is quantal. The pd=12 non-wall is a rate condition (echo factor too slow), not evidence against m; the compensated grids (`spin11-output.txt:58-62`) move the edges as predicted by compensation, consistent with a gain mechanism, not a budget.

## Comparison with the published REPORT (read after booking the above)

Read `knee-meta/REPORT.md` in full after the fit above was written. Scorecard:

- **Class split and units: agree.** REPORT's r = (span·σ)/2Δ and m = N/(2pd+1) are exactly the coordinates I fit. (Contamination caveat applies — see above.)
- **Class M: agree exactly.** REPORT rows 15–19 are the same four edges, m = 1.00 each; row 20 books the pd=12 inertness as the rate condition. My fit adds nothing and contradicts nothing.
- **Class S: REPORT books r = 1 as the headline; my fit says that is only the onset shell.** REPORT's own table concedes this — row 3 (SPIN-5 50%-crossing) = 1.31, rows 9–11 (SPIN-21 R4/R5/R1) = 1.125/0.83/0.885, row 4 (SPIN-8) = 1.248 — and its Caveats section books "statistic choice matters: onset 1.00 vs mid-curve ≈ 1.25; both shells reported rather than absorbed." My independent numbers land on the same two shells (0.96 vs 1.20–1.32). What the REPORT under-weights, and SPIN-29 (later the same day) then settled: **the crossing shell is itself a clean linear law C = 2.38·Δ across a 2.5× Δ grid — the "mid-curve" value is not curvature noise, it is a second constant.**
- **Net:** r = 1 recovered **as onset-shell truth, not as the whole truth**; m = 1 recovered **cleanly**. Anything-else finding: the two-shell structure is the finding — and it was already latent in the REPORT's own caveats and then made decisive by SPIN-29.

## Receipts

- Raw extractions: `sed -n '45,60p' spin5-output.txt`; `sed -n '81,95p' spin21-output.txt`; `grep` wall-edge table `spin11-output.txt:33-38`; `spin29-output.txt:35-44` (α table + fit table).
- Fit arithmetic: in-session python (`statistics` module) — onset mean 0.960/sd 0.089; cross mean 1.319/sd 0.091; SPIN-29 α mean 1.203. Inputs as typed in the table above.
