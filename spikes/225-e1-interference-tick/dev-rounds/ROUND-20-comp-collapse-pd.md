# DEV ROUND 20 — comp-collapse confirmation at pd ∈ {2, 6}

Round 19's booked next spoke (4cbfd83). Harness: `r20_arrivalwall_pd.py`
(r19 lineage: `r19_arrivalwall.py`, `o2_contention.py`, `q7b_dial_o2nsweep.py`).

## PART 1 — PRE-REGISTRATION (committed before any round-20 comparison numbers)

**Item.** Round 19 swept candidate arrival rate r = delta/K at pd=3, N∈{2..13},
raw + lag-compensated arms. Verdict PARTIAL: raw-wall arrival-rate law REFUTED
(two-knob object); genuine post-hoc discovery — lag compensation collapses the
K degree of freedom: comp wall(delta/K) is a single curve across both delta/K
families over 1.7 decades. This round tests whether that comp-collapse law
survives at pd ∈ {2, 6} (round 17 anchors: raw walls pd2→N5, pd3→N6, pd6→N7).

**Sweep.** Same families as r19: calm (K=8, drift=3, deltas 2..48) and stress
(K=4, drift=6, deltas 2..48), r spanning ≥1 decade; N ∈ {2..13}; arms raw AND
lag-compensated (per-twin F19 lag blade + compensation, verbatim `run_sw_comp`);
4800 ticks; seeds (1, 7, 42, 1999, 20260902); integer-only arithmetic inside
loops. Wall gate round-3 unchanged: smallest N with mean win (mag+C=1 minus
admit-all, 5 seeds) ≥ +2.0pp.

**Comp-collapse domain (pre-declared):** r ≥ 0.5. r19's calm r=0.25 comp outlier
(wall 7) sits below the law's stated domain and is excluded from collapse reads.

**PRE-REGISTERED DECISION RULE (comp arm, primary):**
- **PROMOTE** the comp-collapse law if the comp-arm walls at pd ∈ {2, 3, 6} all
  collapse onto a single arrival-rate curve within ±1 seat — at every r ≥ 0.5
  where families overlap, family spread ≤ 1 seat within each pd, AND pd=2/pd=6
  walls within ±1 seat of the pd=3 anchor curve (pd=3 comp curve from round 19,
  exact-replayed as canary).
- **BOOK** "pd is a second knob in the comp regime too" if pd shifts the comp
  curve, with the measured seat offsets per r against pd=3.
- **PARTIAL / boundary** if collapse holds at one pd but not the other: locate
  the boundary between them.

**Canaries (mandatory, all must pass before any verdict):**
- C1 byte-identity: double-run of the harness must produce byte-identical
  deterministic per-cell dumps (`r20-data/`, ≥8 files, no timings).
- C2 anchor replay: (i) round-2 N=5 stress raw anchor 68.0/69.6; (ii) round-17
  raw default walls pd2=5, pd3=6, pd6=7 exactly; (iii) round 19 pd=3 comp walls
  reproduce EXACTLY (hardcoded from 4cbfd83).
- C3 mislabeled-arm self-canary: mag+C=1 relabeled admit-all must be CAUGHT.

**Not touched:** unrelated uncommitted files (q_wall_gate.v, wheel logs).

## PART 2 — NUMBERS (run 22:16, 525 s, harness r20_arrivalwall_pd.py, commit 1480949 pre-reg)

### Canary gates — ALL PASS
- **C1 byte-identity:** two full independent runs; 72/72 per-cell dumps in
  `r20-data/` byte-identical (`diff -r` clean).
- **C2 anchor replay:** round-2 N=5 stress raw 68.0/69.6 exact; round-17 raw
  default walls pd2=5, pd3=6, pd6=7 ALL exact; r19 pd=3 comp walls 12/12 cells
  reproduce EXACTLY.
- **C3 mislabeled arm:** mag+C=1 relabeled admit-all -> 69.6 vs anchor 68.0 ->
  CAUGHT.

### Comp-arm walls by r = delta/K (domain r ≥ 0.5; None = never crosses +2.0pp)

| r | pd=2 (calm/stress) | pd=3 anchor (calm/stress) | pd=6 (calm/stress) |
|---|---|---|---|
| 0.50 | 3 / 2 | 2 / 2 | 2 / 2 |
| 0.75 | 2 | 2 | 2 |
| 1.00 | 2 | 2 | 2 |
| 1.50 | 2 | 3 | 2 |
| 2.00 | 2 | 3 | 4 |
| 3.00 | 3 / 2 | 3 / 3 | 6 / 8 |
| 6.00 | 3 / 3 | 4 / 4 | 6 / 7 |
| 12.00 | 3 | 4 | 7 |

(Raw-arm walls for reference, from output: pd=2 raw walls 5–7, pd=3 raw 6–10,
pd=6 raw mostly None/3–6 — raw arm remains the two-knob object of round 19.)

### Decision-rule evaluation
- (a) within-pd family collapse (±1 at overlapping r): pd2 PASS, pd3 PASS,
  **pd6 FAIL** (r=3.0 family spread 2: calm 6 vs stress 8).
- (b) cross-pd collapse vs pd=3 anchor (±1): **pd2 PASS**, **pd6 FAIL** —
  offsets at pd=6: r=3 → +5 seats (vs anchor 3), r=6 → +3, r=12 → +3.

### VERDICT: **PARTIAL — collapse holds at pd=2, breaks at pd=6**

The comp-collapse law does NOT survive at pd=6: the comp wall moves +3 to +5
seats at high r and even loses cross-family collapse (pd is not fully collapsed
out even within a fixed pd=6). The boundary lies between pd=3 and pd=6 —
not located this round (needs a pd fine-sweep at fixed r, e.g. r ∈ {3,6},
pd ∈ {4, 5}; that is the booked next spoke).

Honest secondary observation (post-hoc label): even at pd=2 the comp curve sits
a uniform −1 seat below the pd=3 anchor for r ≥ 1.5 (2,2,2,2,2,3,3,3 vs
2,2,2,3,3,3,4,4) — inside the ±1 gate but consistent with a monotone pd effect
at high r: comp wall(r=12) = 3 (pd2), 4 (pd3), 7 (pd6). At low r (0.5–1.0) the
comp wall is exactly 2 seats at every pd tested — the collapse is exact and
pd-free there.

### HEADLINE
**Comp-collapse survives pd=2 (±1 seat) but breaks at pd=6: comp wall jumps
+5 seats at r=3 (anchor 3 → stress 8) and the pd=6 comp arm loses cross-family
collapse itself. pd is a second knob in the comp regime at high r; boundary
between pd=3 and pd=6.**
