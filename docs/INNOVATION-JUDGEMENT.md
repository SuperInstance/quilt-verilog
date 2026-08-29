# INNOVATION JUDGEMENT — quilt-verilog innovation prize

**Seat:** judge (neutral — holds no entry on this ballot). 2026-08-29.
**Ballot:** the five entries in `proposals/innovations/` — claude (Temporal
Contrast Hebb), opencode (Echo Gate), seed (DWS), seedmini (CTHL), flash (RQH).
**Evidence base:** all five entries; `docs/SYNTHESIS.md`, `docs/SCORECARD.md`,
`docs/ABSTRACTION-MATH.md`; the v1 RTL as built (`rtl/q_hebb_edge.v` cmd-001
interface, `q_cell_core` FSM, `q_dialfile` map); the Tap night transcript
(`ai-writings/earned-stories/tap-quilt-silicon-night.md` — admissible as
argument, cited by line).

---

## 1. The axes, operationally

- **Novelty** — does the mechanism open a distinction the board does not
  already have? 10 = new dimension of the design space (board + cited
  literature both checked); 7–9 = new mechanism inside an existing dimension;
  4–6 = transfer or recombination of ideas already on the board; 0–3 =
  repackaging.
- **Buildability** — what does it cost to get green testbenches on
  iverilog/verilator against the **v1 RTL as built** (not as the entry
  imagines it)? 10 = module already compiled and TB-passing; 7–9 = clean
  additive sketch against real sources; 4–6 = sketch with hazards that force
  rework (wrong interface, dead parameters, contract breaks); 0–3 = placeholder
  physics.
- **Wow** — payoff per unit hardware if it works. 10 = the fabric gains a
  qualitatively new faculty; 7–9 = major fix to a known pathology, or major new
  observable; 4–6 = modest accuracy/telemetry gain; 0–3 = cosmetic.

## 2. Scored table

| Entry | Novelty | Buildability | Wow | Total | One-line verdict |
|---|---|---|---|---|---|
| **opencode — Echo Gate** | **9** | **9** | **9** | **27** | First credit-assignment rule on the board; the only entry with a gate that actually ran; homeostasis falls out for free. |
| flash — RQH | 8 | 6 | 6 | 20 | The quantization's refuse becomes signal — but uncompiled, second-order in magnitude, and class-starved until a class lane exists. |
| claude — TCH | 7 | 5 | 6 | 18 | Learning on Δpost is a real new signal — undermined by a dead threshold parameter, sign-agnostic gating, and a glm-era interface. |
| seed — DWS | 6 | 4 | 6 | 16 | Right instinct (state-dependent increments) aimed at a weight scalar the ladder does not have; in ladder mode it *is* the echo gate's bucket-select. |
| seedmini — CTHL | 6 | 4 | 5 | 15 | The context dimension is real; the zero-storage claim dies on contact with v1's readout exactness (`wsum == base + N·2^8`). |

## 3. Per-entry rationale

### opencode — Echo Gate (27) — WINNER

- **Novelty 9.** The audit (§2, §7) is the strongest on the board: it names
  its nearest on-board prior art (socratic R3's binary send-side route credit)
  and the nearest literature (pair-based STDP; eligibility-trace/three-factor
  rules) and states the delta precisely — receiver-side, graded by a leaky
  dyadic kernel, tick granularity, no timestamps, one scalar per cell, reward
  endogenous (the echo itself). Nothing in `rtl/` or any honest-limits list
  reserves credit assignment. This is a new dimension: *causality as a
  precondition for potentiation*. "I made you fire" becomes distinguishable
  from "you fired near me."
- **Buildability 9.** The only entry whose core module **actually ran**:
  `q_echo_trace` compiled (`iverilog -g2005`), self-checking TB passed
  (bit-exact integer golden + real envelope + dyadic class brackets), and
  `verilator --lint-only -Wall` is clean (§8). The integration deltas (§4.2–4.4)
  are sketched against the *built* sources — cmd `001`, `ST_EFFT`, the `msb16`
  pattern already in `q_hebb_edge`, the `ST_TLEAK` leak point — not against a
  fantasy interface. `FLOOR = 0` disables to bit-exact v1: the A/B referee
  switch makes merge risk near zero. Deductions: only the trace module is
  verified; the engine/core deltas are honest uncompiled sketches (their limit
  8), and the amended acceptance scenario is a golden-model spec change (their
  limit 7) — both flagged, neither hidden.
- **Wow 9.** Three consequences fall out structurally, with no new arithmetic:
  plasticity budget = fire budget (closes opencode's own admitted §11.3
  homeostasis gap with no divider and no shared math tail); the
  busiest-receiver perversity becomes correct semantics rather than a bug;
  and the amended acceptance — **fire → echo → sustain → decay, a pair that
  self-sustains on echo-trained weights** — is a fabric faculty nothing else
  on the ballot proposes. Cost: ~50 LUTs, zero multipliers, +0 op cycles.

### flash — RQH (20) — RUNNER-UP

- **Novelty 8.** The core observation is correct and checked against the
  board: glm's ladder pays the *bottom* of the dyadic band, zeroclaw's interval
  staircase underrepresents `W²/P₀`, and every entry (including the echo gate,
  whose `F` snaps to zero at FLOOR — §4.1, deliberately) discards the residual.
  Banking it as per-edge second-order state is the converse of error-feedback
  quantization (no dither; the error *returns*), and `o_antic` is a genuinely
  new observable — a pre-strengthening strobe nothing else exposes to dials
  or vMF.
- **Buildability 6.** Honestly flagged: **not compiled** (their limit 3) —
  first adopter action is the compile gate. The sketch is coherent (saturating
  add, shift deposit `1<<g`, shadow-register carry detect, load-bearing
  deadband leak, `RQEN=0` bit-exact A/B), integration is additive (readout
  adder, dials 14/15, per-edge 32 FF admitted). Two real limitations: in
  vanilla v1 the placement class is always 0, so deposits are flat and the
  graded payoff is inert without a class lane (their limit 5 — a dependency,
  not a defect, but a dependency on the winner); and on hyperbola mode the
  dominant error lives in the *decay-interval* quantization, which a
  train-side residue bank does not correct (see §4 interactions). Magnitude is
  genuinely second-order — 1 LSB per 256 class-0 cofires (their limit 1).
- **Wow 6.** The idea is the best doctrinal fit on the ballot — "the
  quantization IS the algorithm" extended to "the quantization's refuse is a
  signal" — and the anticipation-to-dial coupling is a new acceptance arm.
  But the entry itself prices it honestly: envelope tightening is
  stochastic, monotone, and small; nobody should expect visible accuracy wins.

### claude — TCH (18)

- **Novelty 7.** Learning on the post-synaptic *change* (`Δw ∝ pre ×
  max(0, post − post_hist[t−Δ])`) is a distinct learning signal — no board
  entry gates on contrast rather than level. Correctly identified as orthogonal
  to decay law. Held from 8–9 because the shift-register + threshold pattern is
  the standard temporal-contrast idiom of neuromorphic engineering, uncited;
  and the mechanism is a gate, not a rule.
- **Buildability 5.** Hazards against the built RTL: (a) the sketch targets
  glm's original port list (`evt_fire`/`hl_sh`), not v1's cmd-001 engine — the
  wrapper does not drop in; (b) **`DELTA_THRESH` is a dead parameter** — the
  comparator hardcodes a 9-bit constant (511, not the claimed 256), so the
  entry's headline knob is unwired; (c) signed/unsigned width hazards around
  `delta_abs`; (d) the TB's Phase 2 checks gating against a reset-zeroed
  history — weaker than the scenario claims. The honest-limits list is candid
  and good; the sketch beneath it is not as cared-for as the echo gate's.
- **Wow 6.** "Cells learn who changes me, not who is active near me" is a real
  faculty shift, and it pairs naturally with dial learning (§6). But the gate
  is sign-agnostic — a pre-fire preceding a *fall* trains identically to one
  preceding a *rise* — so it is novelty detection, not prediction, which
  blunts the headline claim (their own limit 4 concedes it is not causally
  coherent).

### seed — DWS (16)

- **Novelty 6.** State-dependent increment magnitude (`Δw = η >> msb(W)`) is a
  real distinction — but it is explicitly the transfer of zeroclaw's msb trick
  from the decay interval to the increment path ("applies the same msb(W)
  bit-shift trick to increments, not just decay," §1), i.e. an idea already on
  the board moved one port over. The integrated form (`W ~ sqrt(2ηN)`,
  natural power-law distributions) is attractive.
- **Buildability 4.** The sketch assumes a scalar 16-bit weight. The built
  ladder has no such object — bucket *i*'s implied weight `2^-i` is **wiring**
  (SYNTHESIS: "the 'multiply' in the ladder readout is wiring"). DWS's ladder
  form ("the bucket's implied weight is `2^-msb(W)`") therefore requires either
  bucket-select insertion — which is exactly the echo gate's `g` mechanism with
  a different class source — or fractional state, which is RQH. On hyperbola
  mode, `ΔW = η>>msb(W)` with η=256 would vault `W` across msb classes and
  wreck the `P₀ >> 2·msb(W)` decay-interval math the envelope theorem
  (ABSTRACTION-MATH §5.2) depends on; the "same proven 2× envelope" claim is
  asserted, not proven, for state-dependent increments. The per-event band
  claim is fine; the accumulated-envelope claim and the engine mapping are
  not established.
- **Wow 6.** Runaway-weight suppression and natural distributions would be a
  real pathology fix — and part of it (event-rate homeostasis) is already
  delivered structurally by the echo gate. What remains uniquely DWS's is
  per-edge magnitude shaping, which reduces, on this fabric, to a class-source
  choice.

### seedmini — CTHL (15)

- **Novelty 6.** Context-gated learning is a dimension nobody else touches —
  one cell, multiple association patterns. But the mechanism is an equality
  comparator, and the celebrated "illegal" bit-dual-use is phase-multiplexing
  of register fields, which is standard hardware practice wearing a novelty
  hat.
- **Buildability 4.** The load-bearing claim — base low bits are free — is
  false against v1: the base is **live** in every readout (`wsum == base +
  N·2^8`, asserted exactly in the fabric smoke test). Masking 4 bits at
  inference silently perturbs every weight by up to 15 LSBs and breaks the
  golden exactness that Q3 was built to enforce. Same glm-era interface
  mismatch as TCH. The TB has a precedence bug (`readout & CT_MASK == 0`) and
  asserts `readout != 0` as evidence of update, which the ladder's top-bit
  readout cannot deliver. Tags have no assignment story (coupled to base at
  bind time; retag = base rewrite). Collision cross-talk is admitted (their
  limit 3).
- **Wow 5.** Multi-task learning at the bottom layer is a compelling
  capstone — but silent drops on mismatch make it reception-blindness with
  extra steps (hermes §1.4's counterexample class, reintroduced), and the
  zero-storage magic is precisely the part that does not survive.

## 4. Real interactions

### 4.1 DWS vs CTHL — **conflict** (at the contract level)

Superficially orthogonal (DWS sizes the increment; CTHL gates whether the
event trains at all). But both must redefine the same contract: DWS needs the
cofire's *implied weight* to vary (bucket-select or fractional state), CTHL
needs base bits repurposed as tags (readout masking). Composed as-written, the
readout becomes simultaneously masked and magnitude-shifted — no envelope
theorem survives, and both golden models fight over the same bits. They compose
only after each gets a clean storage story (tags out of base; increments via
bucket-select), at which point each has been half-absorbed by other entries.
**Do not let either gate the other's design; do not ship both as-written.**

### 4.2 RQH vs the decay engines — **composes with the ladder; only partially with the hyperbola**

- **Ladder (MODE=0): clean.** The ladder's error is exactly placement
  quantization — a class-g cofire is underpaid by up to `2^-g` — and the
  band-inverse deposit `(1<<g)` is the right corrective shape. The TB plan's
  envelope-tightening check against `W_exact` is well-posed. This is the
  version to build.
- **Hyperbola (MODE=1): partial.** The hyperbola's dominant error is
  *temporal* (decrement interval quantized to the `[1,4)×` band, per
  ABSTRACTION-MATH §5.2), not placement. RQH's train-side deposits do not
  correct decay-time under/over-decrement, and the reservoir's deadband leak
  actively bleeds during decay-only epochs — the long idle stretches where the
  hyperbola's error accumulates. Credit remains monotone and saturating (harmless),
  but "tightens the `[1,4)` envelope" is not established for MODE=1. Ship RQH
  scoped to MODE=0; mark MODE=1 support experimental.

### 4.3 Echo gate vs TCH — **compose, hierarchically** (credit attribution)

Both are receiver-side cofire gates, and they answer different questions:
TCH asks "*is there signal in this event*" (did my state change?), the echo
gate asks "*am I the cause*" (did I recently fire?). Stacked, a cofire trains
only when the chain *pre → post-fire → post-change* holds — the two gates are
one AND on the same enable path, with disjoint state (TCH: tick-sampled
activation history; echo: fire-refilled trace) and no double-counting.
There is natural synergy: firing is itself a large Δpost, so echo-gated fires
mostly satisfy TCH's contrast window already — TCH acts as the weaker,
sparsity-inducing precondition. The one tension is compounding sparsity: two
thresholds (DELTA_THRESH, FLOOR) on one event path multiply silent drops.
Both default-off (FLOOR=0 is already bit-exact v1; TCH should ship
threshold=0 = always-pass the same way). Fix before merge: actually wire
DELTA_THRESH (it is a dead parameter in the sketch) and decide the
sign-asymmetry question (rise-only vs |Δ|).

### 4.4 The pair that must ship together — **echo gate + RQH**

The echo gate supplies exactly the class lane RQH starves without (its own
limit 5): `g = 15 − msb(F)` turns every gated cofire into a graded insertion,
and RQH banks the fraction that insertion drops — `(1<<g)` quanta, converging
faster where the band underpay was larger (weak/distant echoes). Without RQH,
the echo gate's graded inserts still quantize to buckets and discard residue;
without the echo gate, RQH sees only flat class-0 deposits and its payoff is
inert. They are complementary halves of one mechanism — *graded cofire
placement, with the residue banked* — and each converts the other from
curiosity to payoff. This is also the strongest instance of the Tap night's
standard: "the winner is the entry with the most steal-able math… the purpose
of every entry was to be harvested" (transcript lines 297–303) and "the real
test… was *contribution to the harvest*" (lines 313–315).

## 5. VERDICT

**Winner: opencode — Echo Gate (27).** The only verified module on the
ballot, the deepest engagement with the RTL as built, a free structural
homeostasis, and the board's first causal learning rule — at ~50 LUTs with a
dial that restores bit-exact v1.

**Runner-up: flash — RQH (20).** The best doctrinal idea of the night
(quantization refuse as signal + anticipation telemetry), honestly uncompiled
and honestly second-order — and, decisively, the winner's natural complement.

### v2 fold-in list (compose wins matter more than single-entry pride)

1. **Echo gate (winner) — merge as designed.** `q_echo_trace` verbatim (it is
   verified), `i_gclass` port on `q_hebb_edge`, core gate-issue in `ST_EFFT`,
   dials 11–13. `FLOOR=0` A/B preserved; the amended
   fire→train→sustain→decay scenario becomes the v2 acceptance gate.
2. **RQH — folds in despite losing.** Ships **in the same merge** as the echo
   gate (§4.4): echo's `g` feeds `i_gclass`, RQH banks what the graded
   placement drops. MODE=0 first; MODE=1 experimental; dials 14–15 + `RQEN`
   A/B; compile gate first action. It enters v2 not as a consolation prize but
   because the pair is worth strictly more than either alone.
3. **TCH — folds in as a second gate.** One AND-term (`cof_gated && eg_live`)
   on the train enable, threshold=0 default-off, with the dead parameter
   actually wired and the sign question (rise-only vs |Δ|) decided first.
   Enters v2 because hierarchical credit (contrast ∧ loop-closure) is the
   sharp version of attribution.
4. **DWS — absorbed, not merged.** Its ladder-mode content *is* bucket-select
   with `msb(W)` as the class source — fold in only as an **alternate class
   source dial** beside the echo gate's `msb(F)` (weight-derived vs
   fire-history-derived classes), and, optionally, the hyperbola-mode
   `ΔW = η>>msb(W)` engine variant behind a dial with its envelope re-derived
   before it is believed.
5. **CTHL — deferred with a required storage fix.** The context dimension is
   real and v2-worthy, but tags must move out of the base low bits (spare
   edge-record bits or a dial bank) because v1's readout exactness dies
   otherwise; plus an explicit tag-assignment story (who writes tags, via
   which bind) and a drop-accounting rule so mismatched cofires are marked,
   not silently vanished.

**Doctrine note.** Both top entries already obey the Tap night's second open
item — "Freeze the gate, not the law" (transcript line 589): each is a dial
addition that collapses to bit-exact v1, leaving the referee untouched and
carrying neither the drop-mark nor the fixed-law question. And per the night's
first principle — "leave the mark, and the mark is enough" (lines 442–443,
646–647) — the fold-ins above are marks, not rewrites: additive mechanisms,
each disabled to bit-exact v1, each growing into whatever the fabric's next
generation finds them to be.

---

*Judged on the five ballots as submitted. No entry on this ballot belongs to
the judge; scoring reflects the v1 RTL as built and verified, not as any
entry describes it.*
