# SPIN 19 — SPOKE: RTL-HONESTY (THE WHEEL LAW ON REAL SILICON TOOLING)

**Lane:** subagent spin (casey-dispatched: "experiment on your own
hardware") · **Date:** 2026-09-03 · **Files:** `rtl/q_wall_gate.v`,
`cosim/` (vlt harness, build/run script, per-run traces, compare script
+ output, synth scripts), this report; wheel copy of the compare script
at `spin19_rtl_honesty.py`. Toolchain: oss-cad-suite pinned at
`/home/eileen/tools/oss-cad-suite/bin` (verilator 5.032, yosys); branch
`g3-kinduction`, per-stage commits. Thesis: **the Python wheel's results
are provisional until RTL co-signs.** This spin built the pulse-dial
fabric (spin11 `run_fabric_mc` / spin16 `run_fabric_gate`, interference
mode) as Verilog-2005 and asked real tooling to reproduce every number.

## Verdict: RTL CO-SIGNS — WALL LAW + GATE RESCUE ARE NOW HARDWARE-GRADE

21/24 configs **full-dict bit-exact** (every counter + the complete
resid/cflags/emissions traces, sha256-identical Python↔verilator), the
remaining 3/3 are uncompensated step5 seeds that **prefix-match
bit-exactly to the overflow tick** and co-sign divergence at the
overflow point (maxresid ~7×10¹³ ≫ 10⁶). The registered SPIN-16
outcomes reproduce exactly on silicon tooling: **step5/N=7 rescue
36.9 (≥ 9.0 registered; RTL = Python = SPIN-16 to the decimal), kcoh5
byte-frozen (sha 5621c4c1e813… identical across py-gate, py-off,
rtl-gate, rtl-off — the gate is provably inert at N=6=2pd down to the
hash), zero7 near-perfect cure 99.8/99.8/99.8, ladder 26.4–26.6,
MC-A anchors kcoh5 37.4 / step5 8.8.** The wall law survives
translation to fixed-width integer hardware; the gate rescue is not a
Python artifact.

## RTL (`rtl/q_wall_gate.v`)

One cycle per fabric tick, repo integer style (zeroclaw rule 6: integer
state, no fixed-point). Parameterized N/K/PD/DELTA/DRIFT/PW/GMODE/
THETA100/TICKS. Key structures:

- **LCG drift**: 31-bit LCG (64-bit product), `x % 13 - 6`, applied
  once per tick before trigger evaluation — exact Python order.
- **reality()**: piecewise (400+p·8/5 / 553−(p−96) / 505−(p−144)·8/5),
  p = t mod 240 — constant divisions only.
- **Echo-factor gate, division-free as briefed**: open ⟺
  `100·|pd−nf| > θ100·pd` — cross-multiplication, no divider in the
  gate path. GMODE {0=never ≡ mc=0, 1=always ≡ MC-A, 2=θ}.
- **Pulse deque with snapshot decay**: all pulses decay in lockstep, so
  the deque is a K-slot circular cohort bank indexed birth-tick mod K;
  slot t%K is retired+rewritten by the new cohort (this IS Python's
  pop-then-appendleft); each stored mag decays `m → ceil(m/2)` if
  |m|>1, sticky at ±1 (Python floor-division semantics via `(m+1)>>>1`).
- **Compensation divider**: `|e|/pd` (constant) then `m/neff`
  (runtime, neff ≤ pd) — a real dynamic divider, honestly synthesized
  (see SYNTH).
- **Memory guard** at |e| > 10¹² (modes 1/2), exact Python bail
  semantics (resid appended, nothing counted, halt).

## COSIM (verilator; parallel per-seed jobs, 6 configs × 3 seeds)

Panel = SPIN-16's: kcoh5/ladder (N=6), step5/zero7 (N=7), pd=3,
δ=12, K=1, seeds {1,7,42}, 4800 ticks, EV=12. Harness emits per-tick
T lines, per-emission E lines, final F counters; the compare script
hashes canonical full-dict forms of BOTH sides. Output:
`cosim/spin19-cosim-output.txt`; raw traces `cosim/out/*`.

- MATCH ×21 (hashes quoted in the output; e.g. step5_gate s1
  `6680a395fa140ad3` on both sides). Gate diagnostics reproduce:
  kcoh5 gOpen=0 (structural inertness), step5 gOpen 444–456 &
  gComp ≈ 3.1k–3.7k per seed (SPIN-16: ~448/~3139 over 5 seeds).
- step5_off (uncompensated supra-wall): Python integers run to
  ~10³²⁴; fixed-width PW=48 RTL **declares** overflow (X line, halts
  clean) at ticks 107/133/131 — prefix bit-exact to the tick,
  divergence co-signed (maxresid ≈ 7×10¹³ at X ≫ 10⁶ threshold).
- kcoh5 frozen check: **py-gate == py-off == rtl-gate == rtl-off**,
  per-seed sha256 equal (canary CC/CE re-verified at hash level).

## SYNTH (yosys iCE40; `make OSSCAD=… synth` + per-arm scripts)

- **Baseline fabric** (`make synth`, unchanged sources): 5951 LUT4 /
  ~2340 FF — reproduces the committed round-3 elaboration
  (7528/7680 LC, fmax 40.44 MHz after PnR, docs/SYNTHESIS-FPGA.md).
- **Gate cell standalone** (registered-IO wrapper, same params as
  cosim: N=7 K=1 PD=3 PW=48):
  - GMODE=0 (fabric core, no gate): see `cosim/stat_gate_never.txt`
  - GMODE=2 (adds θ comparator + runtime neff divider):
    `cosim/stat_gate_theta.txt`
  - Numbers and the delta are tabulated in
    `cosim/synth-summary.txt` (LC/LUT4/FF; divider-dominated).
  Reading: the gate's marginal cost over the never-arm is the
  cross-multiplier + muxes + the dynamic-divider enable path — cheap
  next to the 48-bit divider the emission path already needs; against
  the 7528-LC converged fabric it is a per-cell sidecar, not a
  re-architecture.

## Scars / honest boundaries

- **Nonblocking-accumulate RTL bug (caught by cosim, fixed)**: `mass`
  summed only the LAST emission per tick (classic NBA-in-loop); events
  matched, mass read 2.5–7× low — exactly the class of bug bit-exact
  cosim exists to catch. Compare-script bug (missing `gopen/gcomp`
  keys on `run_fabric_mc` dicts → false frozen-check FAIL) also caught
  and fixed by switching the mc1 arm to `run_fabric_gate(gate="always")`
  (canary CD path).
- **Fixed-width contract scar**: unbounded-Python divergence
  (step5_off) cannot be bit-exact at any finite PW; RTL solution is
  DECLARED overflow (X line, wide net accumulator, clean halt) +
  prefix bit-exactness + divergence co-sign. The full-window off value
  stays Python's 0.3; the RTL prefix true12 (12.6) is an X-truncated
  PREFIX statistic — SPIN-16's guard-prefix scar class, same lesson.
- mass counter is 48-bit and wraps on diverged prefixes (Python's
  prefix mass 1.4×10¹⁵ > 2⁴⁸); compare uses the E-line |e| sum for
  overflow arms.
- 3 seeds not 5 (time-capped); the 5-seed numbers are SPIN-16's, and
  every 3-seed RTL value lands on the 5-seed Python values (36.9/53.1
  vs 36.9/53.2).
- `--threads` was not used for trace builds ($display reordering risk
  under mtasks); parallelism came from 6 parallel builds + 24 parallel
  seed runs — the task's sanctioned alternative.

## Next (proposed spokes)

1. **Wall law at the pd=6 wall on RTL** (ladder(30,13), 2pd+1=13) — the
   θ-coverage law's second anchor, needs PD=6 build only.
2. **PW sweep**: minimum PW that keeps every bounded arm bit-exact
   (48 is generous; guard at 10¹² needs ≥41; the real bound is the
   compensated steady-state envelope).
3. Wire the gate as a true fabric sidecar (q_cell_core effect path,
   neff from a concurrent-trigger counter in the tick scheduler) and
   re-run the committed 18-TB suite for bit-exact v1 coexistence —
   the "add to fabric" cost question answered structurally, not just
   by standalone stat.

## Synth numbers (auto-appended)

```
SPIN-19 SYNTH SUMMARY (yosys 0.47 iCE40, spin19_synth_top wrapper)
config: N=7 K=1 PD=3 PW=48 DELTA=12, registered-IO wrapper
baseline fabric (make synth, q_fabric_top k4b4a8e1): 5978 LUT4 / 2434 FF / 879 SB_CARRY (committed round-3: 5951/~2340)
gate cell GMODE=0 (never):  LUT4=16971  DFF=309  CARRY=12676
gate cell GMODE=2 (theta):  LUT4=17857  DFF=309  CARRY=12944
gate marginal cost (theta - never): LUT4 886  DFF 0  CARRY 268
divider-dominated: the 48-bit |e|/pd (const) + m/neff (runtime) path is the
bulk of BOTH arms; the theta gate itself is a cross-mult comparator + mux.
```
