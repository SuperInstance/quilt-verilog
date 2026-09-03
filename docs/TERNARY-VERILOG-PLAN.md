# TERNARY-VERILOG-PLAN — SuperInstance ternary lane → quilt RTL

Surveyed 2026-09-02, shallow (README + ≤4 key source files per repo via
`gh api`, no clones). All eleven target repos exist and are public; ten are
single-file or few-file Rust crates, mostly `#![no_std]` and already close to
integer-only. This plan maps each repo's mechanism to a concrete
Verilog-2005 modular enhancement of the quilt cell.

## Design rules (apply to every row)

- **Integer-only.** No floats, no dividers in the datapath. Float mechanisms
  from the Rust sources are re-expressed as shift-leak (`x - (x>>>k)`),
  multiply-out compares (`3*cnt vs total` instead of `cnt/total vs 1/3`),
  or small LUTs. What cannot be re-expressed honestly is dropped, not faked.
- **Gate-added.** Every enhancement sits behind a dial whose OFF value makes
  the fabric bit-exact v1 (the echo-gate FLOOR=0 / RQH RQEN=0 pattern).
  New mechanisms never change the reset-default behavior.
- **Cell-local, GALS-safe.** No global timestamps; strobes come from the
  tick service the cell already performs (cf. `q_echo_gate.i_tick`).
- **Dial space is FULL.** `q_dialfile.v` allocates all 16 slots (0–15).
  New features must either pack sub-fields into one dial (the dial-14
  `{RQEN, QDW}` pattern) or reclaim a reserved slot (D_ETA_F/D_ETA_S/D_COSMIN
  are marked reserved for post-v1 engines and are the natural candidates).
  Each row below names its proposed packing.

## Summary table

| Repo | Mechanism | RTL target | New module | Gate-added | Priority |
|------|-----------|------------|------------|------------|----------|
| ternary-dice | LCG → balanced-ternary bias | fire test (sampling mode) | `q_tern_dice.v` **(prototyped, this change)** | yes (EN=0 → bias 0) | **1** |
| ternary-conserve | budget/severity monitor | formal lane, not datapath | SVA/SBY checkers | n/a (prove-time) | **2** |
| ternary-spiral | RPS cyclic dominance | cofire train gate | `q_tern_spiral.v` | yes | 3 |
| eisenstein | D6 hex lattice, deadband ring | fabric topology | `q_hex_topo.v` | yes (topo mux) | 4 |
| ternary-critical | ternary Ising MC sweep | per-cell spin mode | `q_tern_ising.v` | yes | 5 |
| ternary-trust | per-edge trust score | extends `q_hebb_edge` | `q_trust_edge.v` | yes | 6 |
| ternary-memory | Ebbinghaus STM/LTM | consolidation unit | `q_tern_mem.v` | yes | 7 |
| ternary-ensemble | weighted ternary vote | fabric readout | `q_tern_vote.v` | yes | 8 |
| ternary-norm | adaptive ternary snap | act readout | `q_tern_snap.v` | yes | 9 |
| ternary-current | dominant-direction merge + eddy | flit arbitration probe | `q_tern_current.v` | yes | 10 |
| ternary-fitness | trit-landscape climber | mostly host-side | `q_tern_climb.v` (thin) | yes | 11 |

---

## 1. ternary-dice → `rtl/q_tern_dice.v` (PROTOTYPED in this change)

**Source mechanism.** `ternary-dice` does weighted random generation over
`{-1,0,+1}`: three weights, one uniform draw, bucket compare
(`r < w_neg → -1; r < w_neg+w_zero → 0; else +1`), deterministic per seed,
with per-die seed spreading `seed + i*7919` (prime spreader). Upstream uses
xorshift32; the quilt harness already standardized on the glibc LCG
(`1103515245*x + 12345 mod 2^31`), so the port keeps the LCG.

**Quilt mapping (RD-PHYSICAL lane 3/7).** RD-PHYSICAL-SUBSTRATES.md's honest
pitch: *deterministic tick by default, stochastic tick as a mode* — noise
earns its keep only for sampling/annealing workloads. So the dice unit emits
a balanced-ternary bias **per tick** that perturbs the fire test in
`q_cell_core.ST_TLEAK` (sampling mode), and nothing else. EN=0 → bias 0 →
the comparison is the untouched v1 test.

**Signal sketch.**

```
q_tern_dice #(PW=16) (
  clk, rst_n,
  i_tick,              // strobe: once per tick service (same tap as echo gate)
  i_seed_wr, i_seed[PW-1:0],   // per-cell seed load (bind-time)
  i_en,                // dial: sampling mode enable
  i_band_neg[14:0],    // P(-1) = band_neg / 32768
  i_band_pos[14:0],    // P(+1) = band_pos / 32768
  o_bias signed [1:0], // {-1,0,+1}, registered, held until next tick
  o_state[30:0]        // LCG state probe (view alias)
)
```

State: one 31-bit LCG register + one 2-bit bias register. Draw uses the
*new* state's bits `[30:16]` (glibc rand slice, the LCG's high-quality
bits). Band compare: `-1` if `draw < band_neg`; else `+1` if
`draw >= 32768 - band_pos`; else `0`. Overlap (band_neg + band_pos >
32768) resolves toward `-1` — documented, deterministic.
Recommended per-cell seeding at bind: `seed = SEED_DIAL + cell_id*7919`
(the repo's prime spreader), computed by the binding parent or host.

**Fire-test integration (not in this change; q_cell_core untouched here):**
`fire ⟺ act + bias_step·o_bias >= d_thresh` with `bias_step` a shift of the
threshold (e.g. `d_thresh >>> 4`), keeping it integer and dial-scaled.

**Dial packing proposal:** reclaim one reserved dial as DICE:
`{en[15], rsvd[14], band_pos[13:7], band_neg[6:0]}` — bands in units of
256 (`band = field << 8`), 128 steps ≈ 0.4% granularity, balanced default
`0x2B2B` ≈ 1/3 each. EN=0 default.

**Cost estimate:** ~35 FF, one constant-multiply (1103515245 = fixed
coefficient → shift-add network), two 15-bit compares. Verified by
`tb/tb_q_tern_dice.v` (iverilog -g2005): bit-exact LCG vs 64-bit golden,
band bucketing, balance statistics, reseed determinism, extreme bands,
overlap priority, disabled mode.

---

## 2. ternary-conserve → SVA/SBY conservation invariants (formal lane)

**Source mechanism.** Despite the name, no ternary arithmetic: a generic
resource-budget monitor — `Budget{total, allocated, consumed}`, per-tick
`consumed += c`, priority compare chain against `{warning, critical, floor}`
emitting a ternary severity. Level-triggered events; budgets only deplete.

**Quilt mapping.** This is a *checker*, not a cell behavior — its value is
the pattern: accumulator + saturating compare chain + ternary severity, all
re-expressible as SystemVerilog assertions under the existing `formal/`
flow (`sby`, cf. `fabric.conservation`). Port as pulse-flow conservation
invariants on the fabric:

```
// sketch: pulse conservation per cell (formal/fabric.conserve.sby)
// injected effects account for all activation, modulo known sinks:
always @(posedge clk) assume (i_en);
// 1. fanout bound: a fire emits at most EDGES_N effect flits
assert (fire_pulse |-> ##[0:EDGES_N+2] !lx_valid);
// 2. no spontaneous activation: act changes only on effect, tick leak,
//    or fire reset (exhaustive cause check on act delta)
assert (act_changed |-> (in_eff || in_tick || in_fire));
// 3. severity ladder on fabric pulse budget: pulses_in_window vs
//    {warn, crit, floor} dials -> 2-bit severity probe (observability
//    only; never gates datapath)
```

**Gate-added?** Not applicable — prove-time only; zero RTL cost, zero
behavior change. Invariants (1)–(2) are exact; (3) is a witness monitor.
**Drops:** `rate()`/`project_remaining()` (f64 division), event history
FIFO, `RateAnomaly` (dead code upstream too).

---

## 3. ternary-spiral → `rtl/q_tern_spiral.v` (cyclic-dominance train gate)

**Source mechanism.** Rock-paper-scissors cyclic dominance on a toroidal
2-D lattice: trits `{-1,0,+1}` ≡ {rock, paper, scissors},
`beats(a,b) ⟺ (a+1) mod 3 == b`; a cell converts to the majority species
among neighbors that beat it (fixed tie-break rock>paper>scissors);
synchronous double-buffer update. Finding that matters for quilt: spatial
structure is *required* for coexistence — well-mixed populations fix to one
species (monoculture), matching ternary-tenforward's lock-in-by-tick-35
warning.

**Quilt mapping.** Not a lattice CA — a **train gate on cofire learning**,
in the exact niche of the echo gate. Classify each cell's phase by its
ladder bucket or act sign into a trit `phase ∈ {-1,0,+1}`; an effect from
`src` trains the edge only if `beats(phase_src, phase_dst)` (cyclic
dominance) — learning flows only along the dominance direction, which
prevents the uniform-potentiation monoculture the RPS result predicts.
The update rule itself (one 2-bit add + mod-3 compare, three 3-bit
beater counters, priority mux) is combinational.

**Signal sketch.**

```
q_tern_spiral (
  clk, rst_n,
  i_eff,                    // strobe: effect hit in ST_EFFT (same tap as eg)
  i_src_phase[1:0],         // trit of the effect's source cell
  i_own_phase[1:0],         // trit of this cell (from act sign / bucket)
  i_cden,                   // dial: cyclic-dominance enable (0 = open)
  o_train_ok                // trains iff !i_cden || beats(src, own)
)
// beats: beats(a,b) = ((a+1) mod 3 == b) — one increment, one 2-entry
// wrap mux (mod 3 on 2-bit trits), one compare. ~6 gates.
```

Consumed in `q_cell_core.ST_EFFT` as an AND with `eg_live` on the
`hb_cmd <= 3'b101` path. **Gate-added:** `i_cden=0` → `o_train_ok=1` →
bit-exact v1/v2. **Dial packing:** one bit; share a dial with another
feature's spare bits (e.g. DICE rsvd[14]).
**Drops:** the full 2-D CA, torus grid, Shannon/Simpson biodiversity
(f64 `ln`) — the coexistence *decision* metrics (`count > total/2`,
each `> total/20`) stay available as integer compares if ever needed.

---

## 4. eisenstein → `rtl/q_hex_topo.v` (Cayley-lattice topology, Seam B)

**Source mechanism.** Exact integer hexagonal-lattice arithmetic via
Eisenstein integers `z = a + bω`: coords `E12{a:i32, b:i32}`; the 6 neighbor
directions are the group units `±(1,0), ±(0,1), ±(1,1)`; D6 rotation by 60°
is `r60(a,b) = (−b, a−b)` (period exactly 6, norm-preserving); hex distance
`max(|Δa|, |Δb|, |Δa−Δb|)` (use the map-layer formula — `lib.rs`'s axial
average is a known upstream bug); disk of radius R has exactly `3R²+3R+1`
cells. `deadband_ring`: when `|map_field| >= threshold`, flood-fill the
largest over-threshold region and compute a front direction as the D6 unit
maximizing the integer alignment score `align = 2x·a − x·b − y·a + 2y·b`
against the centroid displacement, with deterministic tie-break and
stateful band memory.

**Quilt mapping (RD-BEYOND-UTM Seam B).** Seam B's thesis: declare the
lattice as a group G with generating set S, and dynamics class becomes a
*choice of G*. The hex lattice is the first non-ring instance: a topology
module that maps `cell_id → (a,b)` axial coords and enumerates the 6
unit-neighbor ids, so `qm_link`/fanout address a hex Cayley graph
(generating set = the 6 units) instead of the v1 ring. D6 rotation gives
the fabric a group action per tick for free (1 add + 1 sub + mux over 6
baked forms). `deadband_ring`'s per-cell half (`panic >= threshold`) is the
existing fire comparator; the region/front half scales down to a per-cell
"region crossing" flag + the 8-mult align score (narrowable to 32 bits at
fabric sizes) — enough to emit a 3-bit front-direction probe.

**Signal sketch.**

```
q_hex_topo #(AIDW=4, CW=12) (           // CW: coord width, signed
  i_id[AIDW-1:0],                       // cell id
  o_a signed [CW-1:0], o_b signed [CW-1:0],  // axial coords (LUT-free:
                                             // id -> (a,b) by ring formula)
  i_dir[2:0],                           // 0..5 D6 unit index
  o_nbr[AIDW-1:0],                      // neighbor id along unit i_dir
  o_valid                               // inside the radius-R disk
)
// deadband add-on: i_field signed [PW-1:0], i_band[PW-1:0],
// o_ring (|field| >= band), o_front[2:0] — D6 front direction probe
```

Hex distance `max(|Δa|,|Δb|,|Δa−Δb|)` (3 abs + 2 cmp) replaces hop-count in
link validation; `3R²+3R+1` sizes the address map exactly.
**Gate-added:** a fabric-level topo mux (ring id-offsets vs hex units);
ring mode = bit-exact v1. Lives in `q_fabric_top`/`q_flit_pipe` addressing,
never in the cell FSM.
**Drops:** `snap_from_angle` (float trig), `RoomField.warmth()` f64 weights
(portable later as per-mille integer weights summing to 1000 if wanted),
BFS pathfinding and triple search (host tooling), `int_sqrt`.
**Formal note:** norm multiplicativity `‖z1·z2‖ = ‖z1‖·‖z2‖` and D6
invariance are clean `formal/` properties, verified upstream over 10k
fuzzed multiplies.

---

## 5. ternary-critical → `rtl/q_tern_ising.v`

**Source mechanism.** Deterministic 2-D ternary Ising lattice: spins
`{-1,0,+1}` (0 = energy-neutral), `E = −Σ sᵢsⱼ` over 4-neighbor bonds,
Metropolis-style sweep with a **3-valued temperature**: `T=−1` accept
`ΔE<0`, `T=0` accept `ΔE≤0`, `T=+1` accept all; candidate spin order fixed,
fully deterministic, no PRNG. Magnetization via multiply-out compare
(`3·Σs ≥ N`); cold-temperature energy is provably monotone non-increasing
(upstream test). Golden vector: 8×8 critical seed relaxes to `E=−112`,
`m=−1` in ≤50 sweeps.

**Quilt mapping.** A per-cell **spin mode**: the cell's state word gains a
2-bit spin; the tick sweep becomes a bond-sum + ΔE-accept evaluation
against the 4 hex/mesh neighbors' spins. The 3-valued temperature is
literally a three-position dial — the ternary-native control knob.

```
q_tern_ising (
  clk, rst_n,
  i_sweep,                  // strobe: this cell's turn in the sweep order
  i_spin_n, i_spin_e, i_spin_s, i_spin_w,   // 4 x signed [1:0]
  i_temp signed [1:0],      // dial: {-1 cold, 0 critical, +1 hot}
  i_isen,                   // dial: ising mode enable (0 = v1 tick)
  o_spin signed [1:0],      // current spin
  o_de signed [3:0]         // last ΔE (probe; range -8..8)
)
```

**Gate-added:** `i_isen=0` → tick follows the v1 path. Bond sum is 4 adds;
ΔE for a candidate flip is one multiply of small trits (LUT-able);
accept rule is a 3-way mux. Magnetization/energy roll up as fabric
telemetry (one accumulator + two comparators). The cold-mode monotone
energy property becomes a `formal/` assertion, and the 8×8/50-sweep
relaxation is a ready-made golden TB vector.
**Drops:** binder cumulant (`m⁴/(3⟨m²⟩²)` — hostile division, and it only
ever yields a trit; a comparator tree can replace it if ever needed),
susceptibility history (keep an 8–32-deep shift register at most).

---

## 6. ternary-trust → `rtl/q_trust_edge.v` (extends `q_hebb_edge`)

**Source mechanism.** Per-directed-edge trust score on `[−1,+1]`, clamped;
events `{+mag, −mag, betrayal=−0.5 fixed}`; per tick: multiplicative decay
toward zero with a **floor snap** (`|s'| < floor → sign·floor`, zero stays
zero), then **forgiveness**: negative scores add `min(recovery, |s|)`,
never crossing zero. Stage classifier at `±0.2, ±0.6` → 5 stages; agents
act on the stage, not the float. No transitive trust, no PRNG.

**Quilt mapping.** Same niche as `q_hebb_edge` — a per-edge scalar updated
by events and decayed per tick — so it rides the existing engine protocol
(`hb_cmd`/`hb_sel`/`hb_done`) as an alternate per-edge register bank.

```
q_trust_edge #(PW=16) (   // trust in Q2.14: betrayal = -16'h2000 exactly
  clk, rst_n,
  i_cmd[2:0], i_sel[EDGES_N-1:0],     // reuse hebb engine cmd/select
  i_ev[1:0], i_mag[13:0],             // event kind + magnitude
  i_tk, i_tleak[3:0],                 // decay shift k: retention 1-2^-k
  i_floor[13:0], i_rec[13:0],         // floor snap, forgiveness rate
  i_tren,                             // dial: trust enable (0 = passthru)
  o_trust signed [PW-1:0], o_stage[2:0], o_done
)
```

Decay is `s − (s>>>k)` — the house leak idiom; floor snap is 2 cmp + sign
mux; forgiveness is 1 cmp + min + add; stage is 4 signed compares.
**Gate-added:** `i_tren=0` → engine behaves as v1 `q_hebb_edge`.
**Formal invariants straight from the upstream test suite:** forgiveness
never crosses zero; floor never lifts zero; saturation at ±full-scale
(100 betrayals ≡ 1 betrayal); unrelated-slot events are no-ops.
**Drops:** f64 → Q2.14 (thresholds ±0.2/±0.6 approximate to <2^-13 error,
immaterial for a 5-stage classifier); reputation *average* needs a divide —
keep sum+count and compare against `threshold·count`, or shift-approximate
at power-of-2 neighbor counts.

---

## 7. ternary-memory → `rtl/q_tern_mem.v`

**Source mechanism.** Three-tier memory: STM ring buffer of
`(action, outcome, tick)` with **Ebbinghaus retention** `R = e^(−t/S)`
(half-life default 100 ticks) applied lazily at recall; LTM per-label
Welford running stats; episodic store triggered at `outcome ≥ 0.8`
(breakthrough) or `≤ −0.5` (near-miss), mutually exclusive.

**Quilt mapping.** The key insight is already in the codebase: shift-leak
`act −= act>>>ka` *is* an Ebbinghaus exponential with half-life
`≈ ln2·2^ka` ticks. So retention needs no new math — `q_tern_mem` is a
small ring buffer whose entries age against the tick counter, plus a
consolidation path whose **breakthrough/near-miss pulse feeds the existing
RQH residue bank** (a remembered extreme event deposits residue credit) or
strobes the echo gate.

```
q_tern_mem #(DEPTH=8, PW=16) (
  clk, rst_n,
  i_push, i_op[2:0], i_outcome signed [1:0],   // decision record (trit)
  i_tickn[15:0],              // fabric tick counter (for age)
  i_hl[3:0],                  // retention half-life shift (ka-style)
  i_men,                      // dial: memory enable (0 = off)
  o_recall_w[7:0],            // retention weight 0..255 of head entry
  o_mean signed [PW-1:0],     // LTM running mean (count-streak update)
  o_episode, o_severity       // breakthrough(+1)/near-miss(-1) pulse
)
```

Mean update uses the count-streak trick (`mean += δ>>>log2(count)` at
power-of-2 counts) or a plain EMA — both shift-only; bit-exact Welford
needs a divide and is dropped. Upstream test invariants double as TB
vectors: `retention(0)=1`, `retention(H)=½`, `retention(2H)=¼` are exact
in binary only for pure shift decay, so the TB must use shift-compatible
half-lives (ka=7 → ≈89, ka=8 → ≈177; 100 sits between and is *not*
bit-exact — document honestly). Divide-by-zero on empty recall: mux to 0.
**Gate-added:** `i_men=0` → no deposits, no strobes, bit-exact v1.
**Drops:** `exp/powf/ln/sqrt` (all f64), power-law forgetting variant,
String-keyed index, `C(n)=1−1/(1+√n)` confidence (LUT on log2-bucketed n
if ever wanted).

---

## 8. ternary-ensemble → `rtl/q_tern_vote.v` (fabric readout layer)

**Source mechanism.** N weak ternary classifiers (each `score = Σ wᵢfᵢ +
bias`, dual fixed thresholds ±0.3 → trit) combined by majority/weighted/
Borda vote with a **load-bearing tie rule: lowest class index wins**;
AdaBoost-style mistake reweighting `×(1±lr)`; weak-agent accuracy
*asserted* < 0.60 ("combine many bad agents" — a fabric of weak cells).

**Quilt mapping.** A readout-layer module: N cells' ternary outputs
(from `q_tern_snap` or fire/no-fire) → 3 weight-scaled accumulators →
priority-encoded argmax with lowest-index tie-break. Optional mistake
feedback reweights voters by `w += (w>>>k)` / `w −= (w>>>k)` with
`lr = 2^-k` — the same shift-update idiom as `q_hebb_edge`, reward
correct / punish wrong.

```
q_tern_vote #(N=8) (
  clk, rst_n,
  i_valid, i_votes[N*2-1:0],        // N packed trits
  i_w[N*8-1:0],                     // per-voter weights (u8; uniform = vote)
  i_fb, i_fb_wrong[N-1:0],          // mistake feedback strobe + mask
  i_k[3:0],                         // reweight shift
  i_wen,                            // dial: weighted mode (0 = plain vote)
  o_class[1:0], o_margin[15:0]      // winning class + runner-up gap
)
```

**Gate-added:** `i_wen=0` → unweighted majority (the upstream fallback
when weights are missing — the hardware default mirrors it); the module
never touches cell dynamics, so v1 is trivially preserved.
**Drops:** all f64 scores/confidences → Q-format; `α = ½ln((1−ε)/ε)` →
drop the α update, keep only multiplicative reweighting; renormalizing
divides → shift-normalize or saturate; stacking/gradient descent → dropped
(voting + mistake feedback covers the mechanism at hardware cost).

---

## 9. ternary-norm → `rtl/q_tern_snap.v`

**Source mechanism.** Normalization for ternary nets that always funnels
into one primitive: `v > t → +1; v < −t → −1; else 0`. Threshold is a
sparsity knob (sweet spot [0.3, 0.7], default 0.5); running stats via EMA
(`mom=0.1`).

**Quilt mapping.** The statistics machinery (batch/layer/group norm, all
f64 with `sqrt` and divides) has no dynamical content — port **only the
closing operator**: a gated ternary snap on the `act` readout (view path),
with an optional adaptive threshold. EMA with `mom = 2^-k` is the house
leak idiom running in reverse. Scale-free form avoids the sqrt entirely:
snap when `(act − μ)² > (t·σ̂)²`, with μ and σ̂ (mean-abs-deviation) both
EMA-tracked — all integer multiplies.

```
q_tern_snap #(PW=16) (
  clk, rst_n,
  i_tick,                           // EMA update once per tick service
  i_act signed [PW-1:0],            // live accumulator view
  i_thr[PW-1:0],                    // fixed threshold (Q1.15), and
  i_ak[3:0],                        // adaptive EMA shift (0 = fixed thr)
  i_sen,                            // dial: snap enable (0 = pass act)
  o_trit signed [1:0],              // snapped view {-1,0,+1}
  o_mu signed [PW-1:0]              // EMA mean probe
)
```

**Gate-added:** `i_sen=0` → view returns raw `act`, bit-exact v1. The
upstream open question (snap during training vs only at readout) maps
directly onto the dial: readout-only by default.
**Drops:** ε padding (meaningless in integers), γ/β affine (or restrict γ
to a shift), all vector-norm functions, true σ (use MAD).

---

## 10. ternary-current → `rtl/q_tern_current.v`

**Source mechanism.** Directed flow bookkeeping: ternary direction
`{−1,0,+1}` + u8 strength; **dominant-direction merge** — stronger
direction wins, strengths *sum with saturation* (opposing currents do not
cancel; the dominant absorbs both masses; ties favor self); attenuation
only ever shrinks; **eddy rings** — cyclic flows that never escape
(`next = rooms[(idx+1) mod N]`), with `dissolve()` as the break.

**Quilt mapping.** Two kernels, both small: (a) a **merge primitive** for
flit arbitration where two effect streams contend — saturating strength
add + dominant-direction select replaces naive priority when pulses carry
a strength field; (b) an **eddy detector** — a shift-register ring over
recently visited cell ids flags a pulse that returns to its origin N times
(lock-in witness for the fabric, the hardware answer to the monoculture
warning). Upstream's pinned test invariants become formal properties:
saturation never wraps (`200+200=255`), merge tie favors self, attenuation
never amplifies.

```
q_tern_current (
  clk, rst_n,
  i_push, i_dir signed [1:0], i_str[7:0],   // arriving current
  i_atk[3:0],               // attenuate shift: s - (s>>>k) per hop
  i_cen,                    // dial: current accounting enable
  o_dir signed [1:0], o_str[7:0],           // merged running current
  o_eddy                    // strobe: cycle detected (never escaped)
)
```

**Gate-added:** `i_cen=0` → arbitration follows v1 priority, no eddy
strobe. Attenuation moves from f64 multiply to shift-leak — a deliberate,
documented rounding change (upstream truncates after float mult).
**Drops:** String labels, HashMap room tables (fabric addressing already
provides identity), unbounded buffers (fixed capacity, silent drop — which
matches upstream consumer semantics anyway). No PRNG anywhere upstream;
none here.

---

## 11. ternary-fitness → `rtl/q_tern_climb.v` (thin) + host tooling

**Source mechanism.** Exhaustive fitness-landscape analysis over
n-trit strategies: separable fitness `Σ reward[i][sᵢ+1]` (3-entry LUT per
position); Hamming-1 neighborhood; deterministic steepest ascent; trit
histogram / Shannon diversity; `n ≤ 15` practical (`3^15 ≈ 1.4e7`).
Finding: separable rewards ⇒ single global peak unless ties — ruggedness
needs epistasis the crate doesn't model.

**Quilt mapping.** Landscape *enumeration* is host tooling, not RTL. On
chip, keep the single-step pieces: a `2n`-bit strategy register, LUT-based
integer reward (the `q_dialfile` pattern — reward tables are dials), an
n-term adder tree for fitness, and a one-mutation-per-tick climber FSM
(matches tick-epoch discipline). Trit histogram + Hamming popcount are
cheap diversity telemetry.

```
q_tern_climb #(NTR=8) (
  clk, rst_n,
  i_tick,                           // one mutation candidate per tick
  i_strat[NTR*2-1:0],               // current strategy trits
  i_rew[NTR*3*8-1:0],               // reward LUT (8-bit signed entries)
  i_clen,                           // dial: climb enable
  o_fit signed [23:0],              // fitness of current strategy
  o_move[NTR-1:0], o_delta signed [9:0]  // proposed mutation + Δfitness
)
```

**Gate-added:** `i_clen=0` → no mutation proposals; observability only.
**Drops:** f64 rewards → 8-bit signed LUT entries; Shannon entropy
(`log₂`) off-chip — keep the integer trit counts on-chip; Pareto front and
basin analysis — host-side by construction.

---

## Recommended build order

1. **q_tern_dice** (done here) — smallest, self-contained, unblocks the
   RD-PHYSICAL sampling-mode claim with a real gate-added module.
2. **fabric.conserve.sby** — zero RTL, strengthens the formal lane, and the
   pulse-flow invariants double as regression checks for every later module.
3. **q_tern_spiral** — one AND term in `ST_EFFT`, direct anti-monoculture
   mechanism, trivially A/B-able against the echo gate.
4. **q_hex_topo** — the strategic one (Seam B: dynamics class = choice of
   lattice group), but it's a fabric-level change and should land after the
   cell-level gates prove the gate-added discipline holds under synth.
5+. The rest in table order; trust/memory/ensemble/norm are independent
cell-local rows that can be picked off in any sequence once 1–4 set the
integration patterns (dial packing, probe aliases, formal invariants).
