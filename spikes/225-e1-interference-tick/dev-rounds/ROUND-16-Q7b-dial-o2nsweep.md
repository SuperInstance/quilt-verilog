# DEV ROUND 16 — Q7b: regime dial on the O2 contention N-sweep

Date: 2026-09-03 (AKDT). Branch `g3-kinduction`. Item: Q7b (round-14 dial ported to the
O2 N-sweep fabric with the F14 mag/C=1 gate LIVE at every N ∈ {2..8}).
Harness: `dev-rounds/q7b_dial_o2nsweep.py` → `q7b-dial-o2nsweep-output.txt`.

## PART 1 — Pre-registered BEFORE any comparison numbers (committed first)

### Hypothesis (as booked, before running)

The round-14 3-register regime dial (R1 = L̂ blade-fast, R2 = σ stress bit via κ-slow
confirm, R3 = β bursty bit via transient-hit rate) was built and tuned on the 2-twin O4
protocol (segmented calm→conflict→bursty with ADC glitches). Its contention-facing
machinery is the per-stream transient suppressor plus the F14 mag/C=1 sort. Hypothesis:
on the O2 contention N-sweep fabric (fixed calm/stress regimes, NO glitch segment, N
twins at spread latencies), the dial does **not** move the O2 contention wall — the wall
(raw sort win ≥2pp first clears at N=6, round 3/O2b: +4.5pp) is set by coherent
same-tick fan-out error, not by transient hits or regime params, so suppressor+sort
should be ≈ sort-alone. The alternative (to be located if it fires): the σ-driven param
outputs (K=1, pd=2, phase-decay, td=12) shift the wall the way per-twin lag compensation
moved the N=4 bundle wall (round 7/O7: 12.2%→86.3% trueRes).

### Porting decisions (pre-registered, gate-eligible)

- Fabric: `o2_contention.py`/`o2_boundary.py` verbatim base — 4800 ticks, calm
  (K=8, Δ=6, drift=3) / stress (K=4, Δ=12, drift=6), pd=3, seeds (1, 7, 42, 1999,
  20260902). N ∈ {2..8}; latency sets: N=2 (0,12), N=3 (0,6,12), N=4 (0,4,8,12)
  [NEW interpolation, pre-registered], N=5 (0,3,6,9,12), N=6 (0,2,5,7,10,12),
  N=7 (0,2,4,6,8,10,12), N=8 (0,2,3,5,7,8,10,12).
- DIAL arm (primary, gate-eligible): O2 switchboard loop with (a) mag/C=1 sort ALWAYS
  live at every N; (b) per-twin transient suppressor v1 spec — a twin's error is
  withheld from candidacy for one tick when its reading jumps ≥40 vs the previous tick
  (always active; β does NOT gate the suppressor — that was dial-v2, booked not
  gate-eligible in round 14); (c) registers: R1 blade per-twin (raw arm: discovery
  only; comp arm: compensation), R2 σ = (max discovered lag ≥ 8) OR κ-detector confirm
  (O4 Detector verbatim, fed tick debt / cancel flag net==0 with ≥2 pulses / snap),
  R3 β = ≥2 transient hits in last 16 ticks; stress_now = σ and not β → param outputs
  K=1, pd=2, phase-decay ON, td=12 (else regime defaults). The O4 sequential↔interference
  MODE switch is NOT ported: the O2 fabric is the interference switchboard by
  construction; porting the mode switch would replace the plant, not dial it. Logged as
  a porting scar.
- Attribution arm (secondary, not gate-eligible): "sort+supp" — suppressor + mag/C=1
  only, no σ param modulation (registers computed and logged, outputs inert).
- Unmodified arms: admit-all raw/comp, mag-C=1 raw/comp — these carry the anchor replay.

### Pre-registered decision rule

- Define win(arm) = %w(arm) − %w(admit-all, same N/regime/rawness); ADD(N) =
  win(dial) − win(sort-alone). %w = mean over 5 seeds (integer core; printed at 0.1pp).
- **PROMOTE** if ADD ≥ +2pp at some N ≥ 3 uncompensated (raw) while dial debt ≤
  1.10 × sort-alone debt at that N.
- **BOOK "dial inert on contention"** if |ADD| ≤ 0.5pp at every N (both arms, raw and
  comp).
- **LOCATE** otherwise: report the new N where the ≥2pp raw sort win gate first clears
  under the dial (raw and compensated).

### Canaries (pre-registered, mandatory)

1. Byte-identity: re-run the full N=6 cell (all arms) a second time; the printed table
   block must be byte-identical (hash compared).
2. Anchor replay: unmodified arms must reproduce round-2/O2 + round-3/O2b published
   numbers exactly — stress raw N=8: admit-all 57.8 / magC1 69.7 (+11.9pp); stress
   comp N=8: 42.7 / 98.9 (+56.2pp); stress raw N=6: +4.5pp wall; plus round-2 grid rows
   for N∈{2,3,5}.
3. Self-canary: run one dial cell with the σ register INVERTED (stress_now = (not σ)
   and not β) and label it "dial"; the comparison instrumentation must catch the
   mislabel (fingerprint differs from the true dial arm).
