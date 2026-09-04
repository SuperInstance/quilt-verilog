# SPIN 34 — SPOKE: SILICON (MINIMUM-PW SWEEP: HOW THIN CAN THE WIRE GET?)

**Lane:** subagent spin · **Date:** 2026-09-03 · **Files:** this report;
`spin34_silicon.py` + `spin34-output.txt` (wheel); repo side:
`cosim/run_spin34.sh`, `cosim/out34/` (210 sweep runs + det/canary files),
RTL patch in `rtl/q_wall_gate.v`. Toolchain: verilator 5.032 (Debian),
same `q_wall_gate.v` + `cosim/vlt/spin19_tb.cpp` harness as SPIN-19.
Item: SPIN-19 "Next" #2 (NOVEL-ENHANCEMENTS.md absent — queue used as
briefed). One rung: **extend the existing rtl/cosim suite** (no new sby
property attempted; the sweep IS the cosim-suite extension).

## Pre-registration (written BEFORE any run)

- **H1**: bounded arms (kcoh5/ladder/step5/zero7 gate, kcoh5_off,
  kcoh5_mc1, step5_mc1) stay full-dict bit-exact vs Python down to
  **PW=41**; the minimum is set by GUARD representability (10¹² needs
  signed 41 bits), NOT by the compensated envelope (maxresid ≈ 95).
- **H2 (falsifier)**: at PW=40, GUARD=10¹₂ truncates with the sign bit
  inside the magnitude ⇒ GUARD goes negative ⇒ spurious guard hit ⇒
  MISMATCH.
- **Decision rule**: min-PW = smallest PW in {48,46,44,42,41,40} with
  all 7 bounded tags × seeds {1,7,42,1999,20260902} full-dict
  sha256-identical to Python; descent stops at first failing PW.
  Secondary: step5_off must stay prefix-bit-exact + divergence-co-signed
  (prefix maxresid > 10⁶) at every surviving PW.

## Methods

- **RTL honesty patch (pre-condition for the sweep)**: SPIN-19's RTL had
  two PW-blind constants — `ovf` thresholds hard-coded to 54-bit
  ±2^47 (the PW=48 boundary) and `GUARD = 48'd1000000000000`. Both
  parameterized: `PW_MAX = {1'b0,{(PW-1){1'b1}}}` (= 140737488355327
  at PW=48, exactly the old constant) and GUARD via sized
  `GUARD64 = 64'd1000000000000` sliced to PW bits. Equivalence at
  PW=48 is proven by **byte-identity canary** (below), not argued.
- 30 verilator builds (6 PW × 5 N/GMODE combos), 210 seed runs
  (6 PW × 7 tags × 5 seeds) + 10 step5_off runs, all parallel, no
  `--threads`, every run its own file under `cosim/out34/`.
- Python reference: `spin16.run_fabric_gate` / `spin11.run_fabric_mc`
  (committed), full-dict canonical sha256 both sides (SPIN-19 compare
  semantics; overflow arms via prefixify + E-line |e| mass).

## Results (`spin34-output.txt`)

- **Canary 1 (Python anchors)**: kcoh5_gate shas = 5621c4c1e813ab32 /
  00a23583c03b124d / 9d4ae35e45b43f37 (s1/s7/s42) — exact; gate==off
  byte-frozen across all **5** seeds (two new: 1999, 20260902);
  step5_gate true12 = 36.4/37.3/37.0 (mean 36.9 = anchor);
  kcoh5 true12 = 53.0/55.4/51.0 (= SPIN-19's published line — note the
  "53.0–55.4" quote covers s1/s7 only; s42 is 51.0). PASS.
- **Canary 2 (RTL rebuild)**: patched RTL at PW=48 reproduces SPIN-19's
  committed traces **byte-identically** (`cmp` rc=0) for
  step5_gate_s1 and kcoh5_gate_s1 — the parameterization is provably
  inert at the anchor width.
- **Determinism**: double-runs byte-identical (pw48 step5_gate s1,
  pw41 kcoh5_gate s42); DET-A == sweep file.
- **Sweep**: PW ∈ {48,46,44,42,41}: **35/35 bounded arms bit-exact**
  (7 tags × 5 seeds). **PW=40: 5/35** — the only survivors are the five
  kcoh5_off seeds (GMODE=0 disables the memory guard, so the corrupted
  negative GUARD cannot trip it; envelope fits trivially); every gate/mc1
  arm halts at tick 0 with events=0 — the guard fires spuriously because
  `1e12 mod 2^40` interpreted signed is ≈ −9.95×10¹⁰.
- **step5_off**: prefix bit-exact + divergence co-signed (maxresid
  4.7×10¹¹–7.8×10¹³ ≫ 10⁶) at every PW ≥ 41, all 5 seeds; X tick moves
  monotonically earlier as PW shrinks (s1: 107→102→97→93→90), tracking
  the 2^(PW−1) envelope exactly.
- **PW-invariance bonus**: PW=41 step5_gate s1 sha = `6680a395fa140ad3`
  — the SAME hash as SPIN-19's PW=48 run. The bounded fabric's entire
  observable behavior is identical from 41 to 48 bits.

## Verdict: **VALIDATED** — headline: **min-PW = 41 (35/35 bounded arms bit-exact at PW≥41, 5 seeds; PW=40 fails exactly as pre-registered)**

The minimum wire is set by GUARD representability, not the compensated
envelope (which would fit in ~11 bits). Both H1 and H2 landed as
predicted; the sweep also extended bit-exactness to two new seeds
(1999, 20260902) beyond SPIN-19's panel, and proved the bounded fabric
is PW-invariant in [41,48] down to the trace hash.

## Scars / honest boundaries

- **Unsized-literal trap (found by the first canary run, not by reading)**:
  `localparam ... GUARD = 1000000000000;` (unsized) truncates to 32 bits
  in verilator and lands NEGATIVE — guard trips at tick 0, silent-total
  failure. Fixed with the sized 64-bit literal. Verilog scar class:
  constants wider than 32 bits MUST be sized.
- **Shell-script redirect bug**: `run ... > detA.txt` captured an EMPTY
  file because `run()` redirects internally — the first "DET byte-identical"
  was empty==empty, a false pass. Caught by the `CANARY-RTL-48 DIFFERS`
  that followed; fixed with direct binary invocation + `-s` emptiness
  guard. Canaries catch harness bugs as well as RTL bugs — again.
- PW=40's survivors (kcoh5_off ×5) are bit-exact only because the guard
  is structurally disabled at GMODE=0; they are NOT evidence that PW=40
  is safe — one bit less wire and the contract breaks.
- step5_off full-window off value remains Python's 0.3 (diverged);
  RTL prefix statistics only (SPIN-16/19 guard-prefix scar class).
- Stray file: an earlier copy of spin34_silicon.py landed under
  `~/.openclaw/projects/quilt-verilog/.../wheel/` (write-tool path
  quirk); the canonical copy is in the repo tree, left the stray in
  place rather than deleting (archive rule).
- No sby rung this spin (lint/build via verilator only); yosys synth
  untouched — PW=41 gate cell cost vs the 886-LUT4 marginal is an open
  next-rung question.

## Next-spoke proposal (SILICON, one rung up)

**Synthesize the PW=41 fabric**: re-run the SPIN-19 gate-cell standalone
synth (`stat_gate_never` / `stat_gate_theta`, iCE40) at PW=41 vs PW=48 —
pre-registered hypothesis: LUT4/CARRY counts drop ≈ 6–8% (divider width
dominates; 48→41 is a 15% width cut but CARRY chains scale ~linearly in
width). Decision rule: report ΔLUT4/ΔCARRY per arm; VALIDATED if the
theta arm's marginal cost (was LUT4 886 / CARRY 268) shrinks or holds
while cosim at PW=41 stays 35/35 (already banked this spin).
