# SPIN-30-DEQUANT — §10 cheat-code probes: the ZENO-EFFECT probe (measurement of the live pulse state)

*Wheel spin 30, spoke 8 (DEQUANT; LCG 790425851 → 2111915288 → mod 10 = 8).
Script `spin30_dequant.py`; raw output `spin30-dequant-output.txt` (~40 s,
120 fabric runs + canaries). Integer-only inside every loop; floats only at
print/stat time. Fixed seeds 1/7/42/1999/20260902; 4800 ticks; N=6, pd=3,
delta=12, drift=6, R0 reality. Pre-registered prediction + decision rule
committed in the script header BEFORE any panel run. Not committed/pushed.*

## Hypothesis (pre-registered)

SPIN-dequant-2 attributed the interference arm's control win to WITHIN-TICK
averaging (twin pulses summing/cancelling before g moves) and booked
cross-tick wave memory (the K-tick decay wave) as decorative. The quantum-
flavored counter-hypothesis is a Zeno effect: if cross-tick coherence carries
mass, frequent observation should degrade it. **Prediction: quantized
observation at M=1 costs ≤5pp on zero-lock K=1 (77.3 anchor); >10pp would
instead support cross-tick wave memory.**

Operationalization (fixed before running): measurement = re-round every live
pulse magnitude in the deque to a q-bit power-of-two grid (round-to-nearest,
sign-safe: `mag → sign·((|mag|+½)≫sh≪sh)`), applied at the end of every M-th
tick, AFTER that tick's net delivery — observation reads state, it does not
rewrite delivered history. q∈{6,8,12} → grid step {16,4,1}; M∈{1,4,16,64,
never}; q=12 is a structural no-op control; panel = {zero, kcoh5@15} ×
K∈{1,2} × full q×M grid.

## Results (5-seed mean pct)

```
-- zero K=1 --                      -- kcoh5@15 K=1 --
 q\M    M=1   M=4  M=16  M=64 never  (identical table: all cells 74.1)
 q=6   77.3  77.3  77.3  77.3  77.3
 q=8   77.3  77.3  77.3  77.3  77.3
 q=12  77.3  77.3  77.3  77.3  77.3

-- zero K=2 --                      -- kcoh5@15 K=2 --
 q\M    M=1   M=4  M=16  M=64 never   q\M   M=1   M=4  M=16  M=64 never
 q=6    8.5  30.0  53.5  51.3  50.0   q=6  12.9  16.9  46.3  48.2  50.6
 q=8    1.3  34.6  46.8  49.5  50.0   q=8   0.8  27.1  45.3  48.6  50.6
 q=12  50.0  50.0  50.0  50.0  50.0   q=12 50.6  50.6  50.6  50.6  50.6
```

**Primary cell (zero K=1 q=8 M=1): decoherence cost = 0.0pp → VERDICT
VALIDATED** under the pre-registered ≤5pp rule. **But with a structural
caveat booked loudly:** at K=1 every pulse is appended with life=1 and decays
to life=0 within its birth tick; the expiry sweep pops it before the next
tick. At measurement time the deque is *provably dead* — quantization can
never touch anything. The K=1 Zeno probe is **vacuous by construction**,
not merely negative. The ≤5pp prediction was met trivially; the probe has
zero power at K=1. (Independently, K=1 is also where SPIN-dequant-2 says
all the value lives — so the doctrine survives, but this spin did not stress
it.)

**K=2 is where the probe has teeth, and there the measurement is EXPENSIVE
and Zeno-shaped:** zero K=2 q=8 costs 48.7pp at M=1 (50.0 → 1.3), falling
monotonically as observation rarefies (M=4: 15.4, M=16: 3.2, M=64: 0.4pp)
and as the grid refines (q=12 exactly inert at every M). Same shape on
kcoh5@15 (49.8 / 23.5 / 5.3 / 2.0). Two cells go *negative* — measurement
at M=16/64 slightly beats never (zero K=2 q=6: −3.5 and −1.4pp), noise-scale
but sign-consistent: the K=2 wave is a pathology, and coarse observation is
occasionally a mild antiseptic, never at M=1.

**Confound, honestly booked:** round-to-nearest grid rounding is not pure
observation — at grid step 4, magnitudes 1–2 round to ZERO (mass deletion;
step 16 zeroes mags ≤7). Part of the M=1/q=6 collapse is destroyed pulse
mass, not "decoherence". The clean statement is the *ordering*, not the
magnitude: cost monotone in observation frequency and in grid coarseness,
exactly the Zeno signature, on the arm that carries live cross-tick state.

## Verdict

**VALIDATED** (pre-registered primary rule met: 0.0pp ≤ 5.0pp) — with the
sharpened boundary: **there is no measurable Zeno channel at K=1 because
there is no measurable STATE (pulses are structurally dead between ticks);
the Zeno channel exists exactly where SPIN-dequant-2 said the wave lives
(K≥2) and only ever hurts there — rare coarse observation of the K=2
pathology-wave costs ≤5pp, frequent observation collapses it by up to
48.7pp, and the untouched wave remains the best K=2 cell.** The
within-tick-averaging doctrine is consistent with everything measured: the
load-bearing mechanism (K=1) has no cross-tick state to observe; the
decorative mechanism (K=2 wave) is the only thing observation can touch.

**Headline number: decoherence cost 0.0pp at the pre-registered primary cell
(zero K=1 q=8 M=1); 48.7pp at the maximal-observation K=2 cell (50.0 → 1.3),
monotone in M and q.**

## Canary table (gate: ALL PASS before panel read)

| # | Canary | Result |
|---|---|---|
| a | Wiring byte-identity dyn_run_q(never,sh=0) vs run_fabric resid | PASS — 12/12 configs identical |
| b | Anchors: zero K=1 77.3/187834/8756; ladder@15 K=1 71.5/106378/5792 (debt=mean mass, ev=mean events) | PASS — pct exact to 0.1, debt/ev digit-exact |
| c | Structural no-op q=12 ≡ M=never, full resid | PASS — 4/4 |
| d | Determinism dual-run on quantized cells | PASS — 2/2 byte-identical |

First run FAILED canary b (debt computed as Σresid, ev as Σevents — both
5× the publishing format) and aborted before any panel output: the gate did
its job. Fixed to spin-10 semantics (mean mass / mean events), exact match.

## Scars

1. **K=1 Zeno probes are structurally vacuous** — pulse lifetime at K=1 ends
   within the birth tick; any end-of-tick measurement is untestable by
   construction. Future measurement probes must run at K≥2 or measure
   mid-tick (between emission and net delivery).
2. **Grid rounding deletes mass** (mags ≤ half-grid → 0): "quantized
   observation" conflates observation with amputation. A mass-preserving
   variant (floor at ±1, or rescale by the delivery identity) is needed to
   isolate pure decoherence.
3. **File-name collision:** this lane's first redirect overwrote
   `wheel/spin30-output.txt` belonging to the completed SPIN-30-drift-band
   lane; recovered by deterministic regeneration from its script (canary
   receipts re-verified: C=28.1 replay PASS). Output-file names must carry
   the spoke suffix; dequant output now lives at `spin30-dequant-output.txt`.

## Next-spoke proposal

**MASS-PRESERVING ZENO at K=2**: re-run the grid with rounding floored at
±1 (no mass deletion) plus a delivered-mass ledger (SPIN-15 identity) to
split the 48.7pp into deleted-mass vs true decoherence; if floor-at-1
collapses the cost to ≤5pp, the K=2 fragility is quantization mass-loss,
not coherence — one more boundary for §10's table. (Cheap: same harness,
~1 min.)

— dequant lane (zai/glm-5.3), SPIN-30, 2026-09-03 18:2x AKDT. One lane, no
sub-lanes. Not committed.
