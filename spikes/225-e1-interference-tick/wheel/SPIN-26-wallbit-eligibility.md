# SPIN 26 — WALL-BIT-ONLY ELIGIBILITY SWEEP (filed follow-up to SPIN-25)

**Spoke:** QUANTIZED-GATE × ELIGIBILITY · **Date:** 2026-09-03 (pre-registration
committed BEFORE any run)
**Files:** `spin26_wallbit_eligibility.py`, `spin26-output.txt`, this report.
**Base code reused verbatim:** spin16 `run_fabric_gate`, spin24/25 panel /
`cell` / `sha` / canary pattern. Integer-only in-loop; floats only at
aggregation/print; `python3 -u`, no pipes; seeds {1,7,42}.

## QUESTION (filed by SPIN-25)

SPIN-25 killed θ∈[67,99] for **embedded** eligibility: the nf=6 level costs
ladder30 −1.4pp under the exact toggle (kcoh5 +7.9 causal, but ladder30
−1.4 ⇒ not healthy-inert). Remaining question: the **wall-bit-only half**
t100 ∈ [100,133] — admission set {nf=7} exactly, nf=6 REJECTED — may admit
NOTHING on healthy grammars (never an nf=7 pile-up) ⇒ byte-identity vs
gate="never" on healthy anchors, while keeping whatever nf=7 rescue exists
on pile-up grammars (step5). If so: free lunch lives at the wall bit.

## ARITHMETIC (fixed before any run)

Gate: open iff `100·|pd−nf| > t100·pd`. At pd=3: nf=6 admits iff t100≤99;
nf=7 iff t100≤133; nf∈{1,5} iff t100≤66; nf∈{2,4} iff t100≤33. Hence for
every t100 ∈ {100,105,110,120,133} the admission set is **{nf=7} only** —
all five sweep values should be ONE sha-class (same prediction structure as
SPIN-25 P-b, now on the supra-wall half).

## PANEL / DEFINITIONS (fixed; SPIN-22/24/25 anchors)

Anchors, K=1 unless noted, pd=3, delta/drift 12/6, ticks 4800, EV=12:
kcoh5@15 [0,0,0,0,0,15]; ladder@30; zero7 [0]·7; step5K1 = ladder_step(30,5);
step5K2 same with K=2. **Healthy** := {kcoh5@15, ladder@30, zero7}.
**Rescue** := mean over {step5K1, step5K2} of (pct(t100=t) − pct(never)).
Byte-identity = per-seed full-dict sha equality vs gate="never".

## PREDICTIONS (pre-stated)

- **P-1 (one class):** all five t100 values in {100,105,110,120,133} are
  sha-identical (admission sets all {nf=7}); panel run only on one
  representative.
- **P-2 (healthy byte-identity):** on all three healthy anchors, every
  seed's sha at wall-bit t100 equals the gate="never" sha exactly (healthy
  grammars never reach nf=7).
- **P-3 (rescue):** wall-bit rescue ≥ Spin-22's booked +33pp on the step5
  rescue set (nf=7 admissions do the whole rescue; nf=6 contributed nothing
  to rescue anyway — it only cost ladder30).

## DECISION RULE (pre-stated verbatim contract)

**eligible-embedded(wall bit)** := byte-identity vs never on ALL healthy
anchors (3 anchors × 3 seeds shas) AND rescue ≥ +33pp (Spin-22 booked).
- If BOTH hold for the class: verdict **"free lunch lives at the wall bit"**
  → one-liner in BEACONS.md.
- If any healthy sha differs: book which anchor and which pile-up depth
  caused it; verdict "wall bit not free".
- Per-t100 verdict reported exactly (expected: identical across the class).

## CANARIES (must pass before anything counts)

1. spread=0 byte-identity across gate modes (spin-25 C1 pattern).
2. ladder@15 K=1 = 71.5 exact, 5-seed (spin-25 C2).
3. Spin-25 toggle table reproduces on this rerun: kcoh5@15 nf6 IN−OUT
   ≈ +7.9pp (≥+5 rule) and ladder30 ≈ −1.4pp (t100=99 vs 100 exact toggle).
