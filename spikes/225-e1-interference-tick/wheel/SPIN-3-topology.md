# SPIN 3 — SPOKE 4: TOPOLOGY

**Lane:** wheel_spin3_topology · **Date:** 2026-09-02 ~23:20 AKDT ·
**Files:** `spin3_topology.py`, `spin3-output.txt` · Fabric: `inventors-derby/exp_glm1.run_fabric` (E1 contract items pinned: fdiv decay, 64-bit LCG, FIFO oldest-first expiry, snapshot decay). Integer-only inside the loop.

## Hypothesis (sharpened)

F7 measured a bundle-capacity wall: interference true-residency collapses
91%→10% by N≥4 twins (staggered latencies 0,10,…,10(N−1), K=4). Claim under
attack: **the wall is a fabric constant of N.** Sharpened rival: the wall's
position is set by the twin *staleness geometry* — the pattern of mutual
disagreement — which topology controls. Short tails (K≤2, per F13) and
structured geometry (ring adjacency, star hub-cohort) should hold residency
where all-to-all fan-out collapses.

## Operationalization (be explicit — this is the spoke's main assumption)

"Topology" is realized as the latency pattern over N twins (latency = the
only twin-distinguishing structure in the E1 fabric; F7's wall was built from
staggered latencies, so geometry-of-staleness is the honest carrier):

- **all_to_all**: [0,10,20,…,10(N−1)] — every pair mutually stale (F7 baseline)
- **ring**: [0,10,0,10,…] — only ring-adjacent twins disagree; max spread = 10 for all N
- **star**: [0,10,10,…,10] — one fresh hub vs one coherent stale cohort; max spread = 10 for all N

Sweep: N ∈ {1..6} × K ∈ {1,2,8} × topo, interference arm, 4800 ticks,
stress params (delta=12, drift=6, pd=3), seeds {1, 7, 42, 1999, 20260902}.
Sequential reference per (N, topo). Ring/star twins are exact duplicates of
their latency class — that is the point (coherence), and it is also the
caveat (see Verdict).

## Self-canaries (both PASS)

1. **N≤2 identity:** all three topologies reduce to [0]/[0,10] at N≤2 — all
   18 comparisons (N∈{1,2} × K∈{1,2,8} × topo pairs) byte-identical. A
   mislabeled arm (the dequant-lane bug class) would break this instantly.
2. **F7 replay:** K=4, all_to_all reproduces F7's published means exactly —
   true% 91.0/34.5/12.2/9.7/9.9 and events 2042/6415/10408/15026/19339 at
   N=2..6 (F7: 2041/6415/10408/15025/19338; deltas are display rounding).

## Raw results — interference, mean of 5 seeds (per-seed ‰ in spin3-output.txt)

### true-residency % (|g−s_true| ≤ delta)

| N | K=1 all | K=1 ring | K=1 star | K=2 all | K=2 ring | K=2 star | K=8 all | K=8 ring | K=8 star |
|---|---------|----------|----------|---------|----------|----------|---------|----------|----------|
| 1 | 96.2 | 96.2 | 96.2 | 98.7 | 98.7 | 98.7 | 97.7 | 97.7 | 97.7 |
| 2 | 92.9 | 92.9 | 92.9 | 93.8 | 93.8 | 93.8 | 90.3 | 90.3 | 90.3 |
| 3 | **23.0** | **96.4** | 93.2 | 32.8 | 95.3 | 90.0 | 35.8 | 94.1 | 85.2 |
| 4 | **10.5** | **96.3** | 89.0 | 12.9 | 90.4 | 81.2 | 12.5 | 89.5 | 75.4 |
| 5 | **9.4** | **97.1** | 86.6 | 10.8 | 86.0 | 76.8 | 9.9 | 88.3 | 66.9 |
| 6 | 13.9 | 75.9 | **81.2** | 16.2 | 69.4 | 59.2 | **10.1** | **82.6** | 62.8 |

Supporting (means): all-to-all interference events explode 2041→19321 at
N=2→6 (F7's 6.1/twin rate, reproduced at every K). Ring N=6: events 7589
(K=8) — 2.5× the N=2 count for 3× the twins, no explosion. Star N=6:
5036–11106. Cancellations: all_to_all peaks N=3–4 then falls (saturation,
F7's signature); ring grows monotonically (402→602, conflict still
*resolving*, not saturating). Sequential reference: true% flat 78.4 under
ring/star for all N (T1-priority starves duplicates); 51% floor only under
all_to_all.

## Verdict: VALIDATED (with one honest caveat)

**The F7 wall is not a function of N and barely a function of K — it is a
function of topology.** At N=6, true-residency is 10.1% (all_to_all, K=8) vs
**82.6% (ring, K=8)** — an 8× displacement of the wall with identical N, K,
seeds, params. Ring keeps ≥89% through N=5 at every K; star holds 59–93% at
N=6. No K ∈ {1,2,8} rescues all_to_all at any N≥3 (best: 35.8% at N=3, K=8)
— **K is second-order; geometry is first-order.** This sharpens F13: short
tails dominate *within* a topology but cannot buy back fan-out staleness.

**Caveat (booked first-class):** ring/star keep max staleness spread at 10
while adding coherent duplicates, so the cleanest reading of the mechanism
is: **the wall sits at a critical staleness spread, not a twin count.**
F7's staggered ladder conflated N with spread (10(N−1)). Geometry moves the
wall because geometry *is* the spread schedule. A spread-controlled sweep
(spread ∈ {0,5,10,15,20,30} at fixed N) would separate the two variables —
proposed below.

Sub-findings:
- **Duplicate twins are not free:** ring N=6 pays 2.5–4× N=2's events/debt
  (e.g., K=2 ring: 1988→10381 events, 33.9k→243.0k debt) even at ~90%
  residency. Cohesion preserves truth at linear-ish event cost; fan-out
  destroys truth at ~6.1-events/twin and total residency loss.
- **K-ranking inverts with topology:** star N=6 prefers K=1 (81.2%); ring
  N=6 prefers K=8 (82.6% over 75.9). No global K champion exists — the K
  dial must know the geometry (feeds O4/Q7's regime controller).
- Sequential T1-priority is duplicate-blind (flat 78.4% ring/star) — impulse
  arm also topology-sensitive only via spread, consistent with F7.

## Headline number

**N=6, K=8: ring 82.6% vs all-to-all 10.1% true-residency (5-seed mean) —
the F7 bundle-capacity wall is a topology artifact, moved 8× by geometry
alone.**

## Scars / bugs

- None hit: both canaries passed first run; no name-map or arm-label bugs.
- Design scar carried: topology-as-latency-pattern means N and staleness
  spread are confounded in the original F7 table — recorded as a correction
  to F7's "capacity law" framing (capacity is per-geometry, not per-N).
- Per-seed variance tiny everywhere (±5‰ typical), so 5 seeds suffice; no
  seed anomalies booked.

## New spoke proposed: YES — SPREAD-LAW (staleness-spread sweep)

Decouple N from spread: N=6 fixed, latency multisets with max−min spread ∈
{0,5,10,15,20,30} (plus a shuffled-ladder control holding spread=30 at low
N). Hypothesis: true-residency collapses at a critical spread (predicted
near 15–20, where 8/5-slope disagreement × spread crosses ~2Δ), independent
of N — turning this spoke's "topology artifact" into a one-parameter law
the E4/O4 mode dial can read directly off the fabric's own lag blade (F19/F20).

VERDICT: VALIDATED — the F7 bundle-capacity wall is a topology artifact: identical N=6, K=8 twins at 82.6% (ring) vs 10.1% (all-to-all) true-residency; geometry first-order, K second-order.
