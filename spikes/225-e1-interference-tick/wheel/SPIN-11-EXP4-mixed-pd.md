# SPIN-11 SPOKE RESULTS — PULSE-DIAL: EXP 4 (mixed-pd adjudication)

Worker lane (eco-quiltverilog), 2026-09-03. Pre-registration: the EXP 4
docstring block + P5a/P5b committed BEFORE any run (c32a669 sweep /
5cabf21 booking). Run log: `spin11-exp4-output.txt` (committed alongside).
Canary D (uniform-pd hetero runner == run_fabric_mc(mc=0), full-dict
byte-identity, 4 configs): **PASS** — the per-sensor path adds nothing
on pure populations.

## Results (ladder(30,N), delta=12, K=1, drift=6, 5 seeds, div = all
   seeds maxResid > 1e6; pd alternating per sensor index)

| mix    | N=4  | N=5   | N=6   | N=7   | N=8   | N=9   | N=13  | edge |
|--------|------|-------|-------|-------|-------|-------|-------|------|
| (2, 3) | 16.2 | 0.4D  | 0.2D  | 0.2D  | 0.1D  | 0.1D  | 0.1D  | 5    |
| (3, 6) | 14.4 | 10.3  | 14.0  | 14.4  | 21.9  | 0.3D  | 0.1D  | 9    |

## Verdicts vs pre-registration

- **P5a mix(2,3) edge=5: REGISTERED PRIMARY CONFIRMED.** The pd=2 half
  diverges at its own wall and drags the shared g — weakest-member law.
- **P5b mix(3,6) edge=9: registered alternative "mixture protection /
  sub-linear composition" CONFIRMED** (registered primary was 7;
  "edge 6 = O2b unification" REJECTED). The non-diverging pd=6 half
  absorbs the diverging pd=3 half's shove: the mixed fabric survives 2N
  past the pure-pd=3 wall (7 → 9). Heterogeneity buys robustness, not
  an even wall.
- **O2b's EVEN wall (N=6, round 3 de5ad6b) does NOT unify with the
  2pd+1 echo law under any registered reading:** no mix produced an
  edge at 6; neither pd_eff interpolation nor mixture protection lands
  there. The room-pressure mapping keeps O2b as a separate law — the
  "predictive anchor" the nudge hoped for is a NEGATIVE result: the
  echo wall and the fan-out wall are different physics. Booked as such;
  O2b's own context (its population's structure) remains the only place
  its N=6 can be reproduced.

## Nudge booking (EXPERT, inter-session 2026-09-03)

1. "P3b pd=3 probes {18,19,20} not in EXP 1's grid" — **REJECTED with
   reason:** P3b is an EXP 2a prediction and the pre-registered EXP 2a
   grid explicitly extends the N set with {9, 18, 19, 20} (present in
   the committed pre-registration file; see the `ns = sorted(set(NGRID)
   | {2*p+1 ...} | {9, 18, 19, 20})` line). No quiet-adjacent-scoring
   seam exists.
2. "Mixed-pd arm to adjudicate O2b" — **ACCEPTED** and executed as
   EXP 4 above, pre-registered before the run. Outcome: unification
   hypothesis rejected; weakest-member and mixture-protection laws
   confirmed at (2,3) and (3,6) respectively.
