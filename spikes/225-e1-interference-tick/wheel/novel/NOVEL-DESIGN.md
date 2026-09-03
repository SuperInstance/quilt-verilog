# NOVEL LANE — Beyond the wheel's spokes: five new experiments, two run

*Casey directive 2026-09-03: "keep pushing gold… novel experimentation to take our
science to the next level." Lane `wheel-novel` (zai/glm-5.3). Parallel lane owns
spin5_* / SPIN-5-* / WHEEL-LOG.md — untouched. All runs: `wheel/novel/novel_exp.py`,
raw output `wheel/novel/novel-output.txt`. Fabric: `inventors-derby/exp_glm1.run_fabric`
(E1 contract items pinned: fdiv decay, 64-bit LCG intermediate, FIFO oldest-first
expiry, snapshot decay). Integer-only inside every loop; floats only in display
means. Seeds {1, 7, 42, 1999, 20260902}, 4800 ticks, stress params (delta=12,
drift=6, pd=3) unless stated.*

## PHASE 1 — What the mine gave up (every untested prediction found)

- **SPIN-dequant-2 §3.4 honest scope:** "K>1 earning its keep would need a channel
  with useful phase" — the single most explicit untested prediction in the corpus.
  pm is strictly decreasing in K on the e1 ramp; the wave's cross-tick memory was
  convicted *on one channel shape*.
- **SPIN-4 U-shaped origin anomaly:** spread=0 (perfectly synchronized duplicates)
  is WORSE (50.0–77.3%) than spread=5 (84.9–97.6%). Mechanism (simultaneous-fire
  resonance vs gradual mass pile-up) untested; grid jumps 0→5 so the origin dip is
  unresolved below 5.
- **SPIN-4 knee-vs-2Δ:** collapse knee at spread≈15 vs the 2Δ=24 prediction —
  predicted by a hand-waved "disagreement-slope × spread ≈ 2Δ" argument never tested
  as a *scaling law in Δ* (only one Δ measured).
- **SPIN-1 refractory-floor chatter:** no refractory floor — interference fires on
  consecutive ticks in 20/20 runs (minGap=1 < K). The proposed explicit-cooldown
  blade (REFRACTORY-BLADE) is still unrun. SPIN-4's origin dip is plausibly the same
  pathology amplified by 6 synchronized duplicates.
- **SPIN-dequant-2 §2 escape hatch:** cold> warm>hot on the quasi-convex 1-D pull;
  the booked escape is "a genuinely multi-modal pull geometry, which E1 does not
  instantiate" — nobody has instantiated it.
- **SPIN-3 "duplicate twins are not free"** (2.5–4× events at ~90% residency) and
  K-ranking inverts with topology — no unifying law offered.
- **Metrology scars reused here:** name-map bug class → byte-identity canary
  (CANARY A); LCG low-bit period-2 → unused here (no sub-streams); decay
  sign-asymmetry → kept per contract.

## PHASE 2 — Five candidate experiments (novel, falsifiable)

### N1 — SLOPE-LAW: does cross-tick wave memory ever earn its keep? (RUN — top pick)
**Hypothesis (H1):** spin-dequant-2's negative (pm strictly decreasing in K) is a
channel-shape artifact; on faster channels (per-tick slope σ), stacked pulse
generations deliver higher sustained correction velocity, so ∃ σ* above which
pm(K) turns *increasing* in K.
**Falsification:** pm(K) non-increasing in K at every σ tested (up to 10× home
slope), OR K-increase appears only inside a collapsed-residency regime.
**Cost:** 6 channels × 4 K × 5 seeds + 6 sequential refs ≈ 130 runs, <60 s.
**Expected headline:** either "critical slope σ* where K=8 overtakes K=1" or "the
wave never pays, even at 10× slope."

### N2 — ORIGIN-DIP DECORRELATION: phase-offset duplicate schedules (RUN — second pick)
**Hypothesis (H2):** the spread=0 dip is a *simultaneous-fire resonance* — spread=1
(one-tick phase offset between duplicate classes) already recovers most of the
residency (≥88% at K=1) and collapses the event count toward spread-5 levels.
Falsified if recovery is gradual across 0→5 (mass/debt story instead).
**Cost:** 7 latency configs × 3 K × 5 seeds ≈ 105 runs, <60 s. Zero overlap with
the parallel spin-5 lane (their grammar sweep sits at spread=15; their densification
at 12–24 — the 0–5 origin region is untouched by both).
**Expected headline:** "one tick of phase offset buys back ≥12 points of residency."

### N3 — KNEE-Δ SCALING LAW (designed, not run — overlap risk with spin-5 densification)
**Hypothesis:** the SPIN-4 collapse knee scales as knee(Δ) = c·Δ with c ∈ [1.0, 1.6]
(the 2Δ prediction says c=2; the measured single point Δ=12, knee≈15 says c≈1.25).
Sweep Δ ∈ {6, 9, 12, 18, 24} × spread ∈ {6..30 step 3}, find knee(Δ) per Δ.
**Falsification:** c not constant across Δ (the "law" is an accident of one regime).
**Cost:** 5 × 9 × 3 K × 5 seeds ≈ 675 runs, ~5 min. **Deferred** because spin-5 is
actively densifying the Δ=12 knee; the scaling axis is ours to run next spin.

### N4 — MULTIMODAL THERMAL ESCAPE: cheat #3's last refuge (designed, not run)
**Hypothesis:** instantiate the multi-modal pull spin-dequant-2 booked as missing —
a bimodal truth channel (reality alternates between two distant trajectories with
hysteresis) that creates deadlock rings — and warm/hot sampling then beats cold
(sum > expectation). **Falsification:** cold still ≥ warm on bimodal channels.
**Cost:** port the thermal arm (warm/hot draw at LCG bit ≥11) + 2 channels × 3
temps × 5 seeds ≈ 30 runs, ~3 min of coding beyond budget tonight. **Next pick.**

### N5 — VELOCITY-CAPACITY LAW (promoted from N1's serendipity — see verdict)
**Hypothesis:** the interference arm has a finite per-tick correction velocity
v_max(σ, K, pd) (stacked, decaying pulses) while sequential snapping has none
(impulse = full correction in one tick). Residency collapse is governed by a single
inequality σ > v_max; measured v_max predicts the slope wall across (K, pd, Δ).
**Falsification:** wall position not predicted by the delivery identity within ±1
slope step. **Cost:** this is N1's data re-read + a σ-densification pass — partially
run tonight (σ ∈ {3, 6} added); full law (pd sweep) next spin.

### N6 (not picked) — CROSS-SUBSTRATE SAME-CONTRACT COMPARISON
Hebb / RPS / dice-noise / conservation substrates judged under the same 5-opcode
contract. Genuinely new but a multi-lane program, not a 35-minute lane. Logged for
the wheel's COUPLING spoke.

**Top-2 pick justification (novelty × cheapness):** N1 attacks the corpus's most
explicit untested prediction with a one-knob channel family and a sign-flip
criterion — maximal novelty per line of code; N2 resolves a published anomaly
(U-shape at origin) with zero new machinery and zero collision with the parallel
lane. N3 was scientifically adjacent but operationally overlapping with spin-5;
N4 needed a thermal-arm port we couldn't canary in time; N5 only existed after N1
ran.

## PHASE 3 — Verdicts (both canaries PASSED first: 8/8 full-dict byte-identity
of the pluggable-reality port vs `run_fabric`; 9/9 spin-4 anchor rows exact:
spread 0/5/15 × K∈{1,2,8} → 77.3/50.0/69.0, 97.6/84.9/90.2, 71.5/60.0/70.7)

### N1 — MIXED, and richer than either outcome: a MEMORY WINDOW at the wall's edge
pm(K=8) − pm(K=1) per channel (5-seed means; per-seed agreement 5/5 everywhere):

| σ (slope/tick) | 1.6 (e1) | 2 | **3** | 4 | 6 | 8 | 16 |
|---|---|---|---|---|---|---|---|
| K=1 residency | 92.9% | 93.8% | **13.9%** | 5.2% | 3.5% | 2.5% | 0.8% |
| K=8 residency | 90.3% | 89.0% | **45.6%** | 7.1% | 3.1% | 2.1% | 0.9% |
| K8−K1 | −2.6pp | −4.8pp | **+31.7pp** | +1.9pp | −0.4pp | −0.3pp | +0.1pp |
| sequential ref | 78.4% | 57.2% | 52.3% | 51.5% | 51.2% | 54.8% | 81.3% |

H1 as pre-registered (monotone: ∃σ* above which memory always pays) is **FALSIFIED** —
but its intended core is **VALIDATED inside a one-step window**: at σ=3, cross-tick
memory is worth **+31.7pp** (13.9% → 45.6%, K-rank fully inverted: 1<2<4<8), the
first measured channel where the wave's coherence genuinely earns its keep —
spin-dequant-2's conviction was a channel-shape artifact *in the window*, and a
true law everywhere else. Structure: three channel regimes.
1. **Slow (σ≤2):** conflict regime, interference >> sequential (93.8 vs 57.2 at
   σ=2), K short best — the known world (F1/F13).
2. **Window (σ≈3, at the wall's edge):** K=1 has already collapsed (13.9%) but
   stacked pulse generations still keep pace — memory pays enormously. Impulse
   still edges the best interference arm (52.3 vs 45.6).
3. **Fast (σ≥4): the SLOPE WALL.** All K collapsed (≤7.1%) while impulse holds
   51–81% — at σ=16 the arms are separated ~100× (81.3% vs 0.9%). Mechanism
   (measured shape): a twin firing at error e delivers only e//3 per pulse; when
   the channel outruns the stacked decay tail, g falls permanently behind and the
   deadband is never re-entered — proportional control has finite velocity
   capacity; impulse snapping has none. **This is the regime complement of F1**
   (superposition owns slow conflict 83.0 vs 51.9; impulse owns fast channels
   absolutely) and hands E4's mode dial a physical trigger variable: measure σ
   (a boolean-blade slope probe), not κ alone.

### N2 — VALIDATED (sharp recovery): the origin dip is a simultaneous-fire resonance
N=6 ladder, K=1, mean true-residency: spread 0 → 77.3%, **1 → 89.3%**, 2 → 92.1%,
3 → 96.4%, 5 → 97.6%. Events collapse 8756 → 5232 on the *first* tick of offset
and to 2598 by spread 5; debt 187.8k → 87.4k → 43.9k. **One tick of phase offset
buys back 12.0 points of residency and −40% events** — the H2 signature (sharp,
not gradual). Corroboration: ring@1 [0,1,0,1,0,1] and cohort@1 [0,0,0,1,1,1] are
*identical to ladder@1 to the last digit* (5/5 seeds × 3 K) — at spread 1 the
pattern grammar doesn't exist yet; only the offset does. K=2 remains the worst arm
at every spread ≤ 3 (61.8% at spread 1) — the dip is deepest for mid-K, consistent
with SPIN-1's no-refractory chatter: synchronized duplicates + longer tails =
maximal refire overlap. Spin-3's "duplicate twins are not free" now has its price
mechanism: the cost is *synchrony*, not duplication.

## Bookings
- **The wave's cross-tick memory is real and conditional**: negative at σ≤2 and
  σ≥4, worth **+31.7pp at σ=3** (the velocity window between conflict and wall).
  spin-dequant-2's scope note upgrades from "would need a channel with useful
  phase" to "pays exactly at the wall's edge, where demand ≈ single-generation
  capacity" — a *window law*, not a monotone law (predicted next: window center
  should slide with pd and Δ; that is N5's follow-up).
- **Slope wall pinned**: σ* between 3 and 4 at Δ=12, drift=6, pd=3, lats=[0,10];
  beyond it impulse snapping is the only viable arm (81.3% vs 0.9% at σ=16).
- Origin dip resolved: resonance at exact synchrony, cured by one tick of offset,
  pattern-blind at spread 1.
- Scars: none — both canaries first-run PASS; the identical ring@1/cohort@1/lad1
  rows are *expected* (spread-1 collapse), doubling as a free name-map canary.

— novel lane (zai/glm-5.3), 2026-09-03 07:2x AKDT. Committed to g3-kinduction.
