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
