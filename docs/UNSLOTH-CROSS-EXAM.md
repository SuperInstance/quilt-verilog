# UNSLOTH CROSS-EXAM — measuring the pitch, keeping the ore

An external AI pitched porting Unsloth's optimization doctrines (kernel
fusion, manual autograd, unified memory, auto-packing, opcode
time-multiplexing, convergent rounding) onto this repo. House law says a
pitch gets a cross-exam, not a vibe-check: every claim is scored
ALREADY-HAVE / VIOLATES-COVENANT / WORTH-MEASURING against things that
exist at cited lines, confabulations are named as confabulations, and the
one item with real merit gets measured instead of argued. This document
is the transcript. The measurement ran 2026-08-30 on the working tree of
`master`; every number below was re-run, not recalled.

## 1. The pitch, compressed

Six doctrines plus an artifact story: fused multi-op kernels to "cut FSM
overhead", hand-derived gradients replacing "autograd overhead", a
"unified memory" layer, "auto-packing" of state, a "new 5+1 opcode
time-multiplexed decoder", and convergent rounding to "eliminate
truncation drift". Supporting lore: optimization results "across 25
repos" including `quilt-mojo`, `quilt-jetson`, `quilt-evolve`; "RLAIF
cells"; and a conservation law written "γ+η=C". An "inline cryptographic
validation loop" opcode was floated as a future extension.

## 2. Verdict table

| # | Pitch item | Verdict | Evidence |
|---|---|---|---|
| 1 | Fused multi-op kernels (bypass the per-op FSM) | **VIOLATES-COVENANT** | The bounded run-to-completion op covenant: "every op is bounded (MAX_OP_CYCLES); ci_ready reasserts after each op" (`rtl/q_cell_core.v:3-5`); tick-before-ingress non-deferrable time (`rtl/q_cell_core.v:8-11`); SER "in-service ≤ 1 (commits serialize)" machine-proved at BMC 55 (`docs/ACADEMIC-RIGOR.md:115`). One verb per op is the load-bearing wall views/starvation-freedom rest on. The perf headroom fusion chases was already taken as the PIPE_EFF retime — pipelining *inside* one op, zero covenant cost, fmax measured in SYNTHESIS-FPGA round 3. |
| 2 | Manual autograd | **N/A — rejects the premise** | Nothing in this fabric is gradient-trained; there is no autograd to elide. Learning is local Hebbian cofire (`rtl/q_hebb_edge.v` cmd 001/101), which already has zero backprop overhead. Unsloth's win exists only inside a training loop we don't have. |
| 3 | Unified memory | **ALREADY-HAVE** | "State is a file. QUF …: a flat binary container for cell state … Same file loads into sim, soft core, or fabric" (`docs/DOCTRINE.md:8`). That *is* the unified-memory doctrine, stated 2026-08-29, shipped as `docs/QUF-SPEC.md`. |
| 4 | Auto-packing | **ALREADY-HAVE** | QUF packs cell state bit-exactly: "header KV metadata — same encoding, GGUF value-type numbering" (`docs/QUF-SPEC.md:14`), section layout `cell_count × 32` bytes (`docs/QUF-SPEC.md:141`), unknown-KV skip rule (`docs/QUF-SPEC.md:189`). The Python golden writer and Verilog loader both consume it (tb_quf_loader lane, `tb/run_suite.sh`). |
| 5 | "Propose" a 5+1 opcode time-multiplexed decoder | **ALREADY-HAVE — the tell** | The fabric *is* a 5+1 opcode decoder: `OP_BIND=0 … OP_NAK=6` (`rtl/q_cell_core.v:125-127`), documented as "The 5+1 opcode model" (`README.md:34-49`), one opcode field, cooperative run-to-completion FSM. The pitch sells our status quo back to us as an upgrade — the signature of a brief written about repos it never read. |
| 6 | Convergent rounding to fix truncation drift | **WORTH-MEASURING → measured** | The only item with a real target: the act leak `act <= sclip16(act - (act >>> ka))` (`rtl/q_cell_core.v:220,541`) is floor-division decay. Measured in §3. Verdict there: the bias is real, and convergent rounding does *not* eliminate it. |
| 7 | Inline cryptographic validation loop opcode | **WORTH-MEASURING (defer to Seam 3)** | Not confabulated — it's an honest organ request. See §4: it is the same organ two tournament teams independently declared unmappable. Pricing it is Seam 3's requirements list, not a stealth commit. |

### Confabulations, named

- **`quilt-mojo`, `quilt-jetson`** — do not exist. `ls ~/projects/quilt-*`
  on this machine (2026-08-30): 35 checkouts, neither among them.
- **`quilt-evolve`** — exists, but is `@quilt/evolve` v0.1.0, a TypeScript
  package (its git log: "Initial release of @quilt/evolve v0.1.0"). It is
  not the Unsloth-lineage optimization repo the pitch describes.
- **"25 repos"** — matches nothing measured here (35 local quilt-*
  checkouts; the pitch's own citations resolve to 0 of 3).
- **"RLAIF cells"** — no RL, no reward model, no human-feedback loop
  anywhere in this corpus. Cells are Hebbian ring cells
  (`docs/THE-TICK.md`, `rtl/q_cell.v`).
- **"γ+η=C" conservation law** — no such law exists here. Our conservation
  law is the **cut-conservation theorem** (`docs/ACADEMIC-RIGOR.md:175`),
  stated as "The ledger: conservation by induction"
  (`docs/academic/quilt-calculus.md:281`) and machine-checked as T1/A1 at
  BMC depth 55 (`docs/ACADEMIC-RIGOR.md:181`) with the prove-mode gap
  honestly booked (L1 induction-pending, `docs/ACADEMIC-RIGOR.md:193`).
  If a pitch renames our theorem, it hasn't read it.

**Counts: ALREADY-HAVE 3 · VIOLATES-COVENANT 1 · WORTH-MEASURING 2
(one measured below) · N/A 1 · confabulations flagged 5.**

## 3. The measured piece — truncation drift in the tick leak

**Setup** (`tb/tb_decay_drift.v`, `make drift`). One real `q_cell`, one
linked edge at base `0x7F00` so the seeding cofire's ladder readout
(`+0x0100`) puts the integrating weight at exactly `0x8000` — a single
OP_EFF then writes `act := dat` bit-exactly. Dials: `ka=4` (dial 4),
`thresh=0x7FFF` so the cell never fires and mass stays in `act`. Then
N=100,000 ticks per run, `act` read back via view(0) every 10,000.
TB-side truncation and round-half-to-even models run alongside; the
truncation model matched the RTL `act` **bit-exactly at every checkpoint
(20/20)**, so the numbers below are the DUT's, not a model's. The
convergent-rounding variant exists only as the parallel module
`decay_rne` inside the testbench — `rtl/` is untouched. Wall time for
both 100k-tick runs: ~4 s (iverilog, this machine).

**Results** (drift = |act| vs the exact geometric decay, which crosses
below ½ LSB at tick ~165 for |seed|=20000, ka=4):

| seed | canonical RTL (floor) | convergent (round-half-even) |
|---|---|---|
| +20000 | **stalls at +15 LSB** — last state change tick 120, frozen through tick 100,000 at every checkpoint | **stalls at +8 LSB** — last change tick 119 |
| −20000 | **annihilates to 0** — tick 120; burns to zero slightly *faster* than exact en route | **stalls at −8 LSB** — last change tick 119 |

Why, at the register level: for `ka=4`, floor makes every positive
`act ≤ 15` a fixed point (`act >>> 4 == 0` ⇒ zero leak) while negative
mass over-leaks (`-1 >>> 4 == -1`, so −1 dies in one tick). Round-half-
even halves the sticky band to `≤ 2^(ka-1)` and makes it sign-symmetric
(ties round the quotient to even, so ±8 are both fixed points).

**Verdict on the pitch's claim.** Half right, twice over. (a) The bias is
real — the pitch is right that right-shift truncation drifts. (b) Its
fix does not deliver what it promises: convergent rounding **does not
eliminate** the drift; it reduces the stall band 15→8 LSB (positive) and
symmetrizes it (0→8 LSB magnitude, negative). Any fixed-point leak with
integer state has fixed points; rounding policy only chooses where.
Register-level conservation is never violated (each tick is a subtract:
`act_0 = act_N + Σleak` exactly) — what drifts is fidelity to the exact
decay curve, and across a mixed-sign population the floor variant biases
total mass *upward* (positive residue is immortal, negative residue is
annihilated). The repo already contains the correct doctrine where decay
must not drift: the edge engines keep **integer state** — "the state is
never fixed-point, so it never drifts" (`rtl/q_hebb_edge.v:20-22`). If
zero-drift act decay ever matters, the fix is integer state or a priced
subnormal path — a dial decision, not a rounding-mode swap. Until
something consumes those 8–15 LSB, the canonical leak stands: simpler,
measured, honest.

Reproduce: `make drift` (compiles and runs `tb/tb_decay_drift.v`; PASS =
models bit-exact vs RTL; the drift numbers are data, not pass/fail).

## 4. The G4 connection — convergence, not coincidence

The pitch's "inline cryptographic validation loop" opcode and the
tournament's G4 portability probe (referee/SEAM2-GRADING-NOTES.md §3) are
the same request arriving from independent directions. G4 scored teams on
the honesty of their unmappable lists; two of three independently
converged on the same roots: deadband — "HMAC-SHA256 — UNMAPPABLE … the
RTL corpus has no hash unit of any kind … A keyed hash would be a new
organ" (teams/deadband/docs/PORTABILITY.md:56-63); deadledger — "No verb
computes a keyed hash" (:23-24), "keyed verification before restore has
no substrate" (:31), with the unmappable table booking it explicitly
(:104-106). An external pitch, written with no knowledge of those
documents, independently proposes a keyed-validation opcode. That is
three sources, one organ request: a cryptographic validation organ (and
its custody substrate) is the fabric's most externally-demanded missing
feature. Per the G4 framing this becomes Seam 3's requirements list —
priced, verb-mapped, covenant-checked — not a rushed graft. The
cross-exam keeps the ore and names the vein.

## 5. Ledger

- Verdicts: 3 ALREADY-HAVE, 1 VIOLATES-COVENANT, 2 WORTH-MEASURING
  (convergent rounding measured; crypto organ deferred to Seam 3),
  1 N/A, 5 confabulations flagged.
- Measured: 2 × 100,000-tick runs, 4 s wall; trunc stalls +15/0 LSB,
  RNE stalls ±8 LSB; models bit-exact vs RTL 20/20 checkpoints.
- Not claimed: any change to canonical RTL. Nothing in `rtl/` moved.
