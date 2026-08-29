# ADVOCACY.md — the devil's advocate lane

**Seat:** hermes (the seat, not the model — the Hermes-405B provider failed twice
this round; the argument below is carried by DeepSeek V4-Flash under the hermes
name, so the lane lives but the voice is different. Reader beware of that too:
everything here should be checked, especially the parts that agree with you).

**Role:** attack the recommendation. The scorecard says winner glm, runner-up
opencode, 17/24 skeletons compile, steal-list to merge. This lane's job is not to
re-litigate scores — it is to find the single strongest *concrete mechanism* by
which each entry (including the winner) fails, then to steelman the fleet's own
core assumption, then to bind the synthesis with three questions it must answer
before a single line of `rtl/` is written.

A mechanism of failure is not "it's missing X" or "it's risky." It is the chain
of events: *this resource is shared, this path is unarbitrated, therefore this
state is reachable, therefore this behavior is wrong.*

---

## 1. Mechanisms of failure (one per entry, strongest only)

### 1.1 glm (winner) — the grant is assumed, and assumptions don't gate

The failure: **the fabric cannot live without the shared math tail, and the
tail's grant path has no liveness argument.** It is the one subsystem the winner
itself flags as unscheduled — round 2: "the math-tail *grant* path across cells
is named but not sketched; the arbitration FSM is the hardest unscheduled piece
of the build" — and the fabric defaults `HAS_MT=1`.

The mechanism, step by step:

1. Cosine costs two sequential divides and two square roots on the shared tail —
   ~200 cycles at N=32, DW=16 — and the tail is granted at tick boundaries.
2. The tail's job is non-preemptible, but the per-cell edge sweep it shares the
   cell with is advertised as "preemptible at slot granularity." No save/restore
   of an in-flight tail job across a tick is described. Either the tail is not
   preemptible (job latency jitter, grant queueing) or it is (unsketched context
   state, corruption risk). Both horns are unpriced.
3. Under an effect storm, the ring saturates (fire fanout serializes E flits per
   firing cell). The only priority rule in the design is *wrap priority at the
   seam* — and it arbitrates outward, protecting ring traffic from external
   injection. Internal priority — view responses vs. effect flits vs. grant
   requests — has no rule at all.
4. Therefore a `qm_view` response has **no bounded latency**: its cos path waits
   on the grant, the grant waits on tick boundaries, tick boundaries wait on the
   storm to clear. The fabric's only witness of learning (qm_view) can be starved
   by the fabric's own learning traffic. The acceptance test cannot see the
   failure because the test's views are scheduled, and the failure lives in the
   gap between scheduled and actual.

Compounding evidence already in hand: the winner's one implemented
scheduling-adjacent structure — the ladder readout adder tree — ships with a
circular comb (`qs_hebb_edge` trips verilator UNOPTFLAT on the `t` chain): a
loop that can oscillate in simulation and glitch in silicon. The winner's own
code shows that combinational behavior at scheduling boundaries is exactly where
this entry goes wrong.

### 1.2 opencode (runner-up) — the busiest cell silently stops learning

The failure: **a cell that receives continuous ingress never ticks, and nothing
in hardware bounds the deferral.** The mechanism is in the skeleton, not in the
plan. In `q_cell_core`, a tick strobe that arrives while the cell is busy sets
the `tick_go` latch — but the tick executes only when `!ci_valid`
(`if (tick_go && !ci_valid)`, RTL-SKETCH §9). Under sustained ingress the tick
is deferred indefinitely: the decay sweep never runs, `act` never leaks, the
fire test never runs.

The consequence is perverse in exactly the right direction: **the cell receiving
the most effects — the one that should be learning fastest — is the one that
never learns.** It still accepts traffic, so nothing breaks loudly; a directed TB
can't catch it, and the train-to-fire acceptance test structurally cannot catch
it, because its train phase drives effects in bursts, which leaves `!ci_valid`
gaps for the deferred tick to sneak through. The phases are advisory (limit 9),
the hardware watchdog is a "build item" with no sketch (RTL-SKETCH §12 note):
nothing interlocked.

This is the field's cleanest live counterexample to the belief that "the tick is
time." In a learning fabric, time is the only invariant; a design where time can
be starved by traffic has inverted the priority of its own semantics.

### 1.3 zeroclaw — no-drop becomes unreachable

The failure: **the no-drop doctrine converts an effect storm into a total
administrative outage.** ZeroClaw has exactly one stream contract for all IO —
bind, view, and effect share the ingress (§1.2) — and the effect FIFO "never
drops: backpressure via stall" (§1.1). A congested FIFO deasserts `ready` on
*everything*, control included.

The mechanism: storm fills the FIFO → ingress stalls → `qm_bind` cannot
reconfigure, `qm_view` cannot observe, the cell is unreachable from outside →
recovery waits for the storm to drain — but the storm is driven by the fabric's
own cofire traffic, which the cell can neither throttle (no dial write path) nor
even witness. The doctrine "amnesia is worse than latency" (§6.8) has quietly
upgraded latency to *inaccessibility*: the FIFO depth parameter simultaneously
bounds learning capacity and observability, and the entry's own mitigation —
"receipt-then-drop with journal replay" — is admitted (§6.8) to be unsketched.

Secondary, compounding: the entry's semantics are defined as one-to-one with a
C behavioral golden model (quilt-esp32 firmware) whose semantics are
event-order, not cycle-order. There is zero RTL — so the first cycle-accurate
integration will have to invent answers to timing questions (what does a view
return mid-drain? what is the FIFO state at the exact tick boundary?) that the
golden model cannot validate. The entry with the deepest math is also the entry
whose failures are the least discoverable.

### 1.4 seed — the learning rule doesn't compute the thing it claims

The failure: **the multiplier-free "product" is not a product, and the Hebbian
field therefore learns activation magnitudes, not co-activation statistics.**
The mechanism: `overlap[i] = pre[i] & post[i]`, priority-encoded to the MSB,
shifted by `(14 − highest + rate)` — a magnitude estimator of
min(|pre|,|post|) truncated to their common prefix. Its value is a function of
the operands' *exponents*, not their fine structure.

The chain: any two co-active cells whose activations share a magnitude band get
the same update regardless of correlation → the update signal is confounded by a
spurious covariate (magnitude) → in a hard-saturating Q1.14 world the weights
fill up as a function of scale, not of "fire together" → the fabric stops
differentiating exactly where Hebbian learning is supposed to differentiate. The
acceptance test would *pass* — weights grow, thresholds are crossed — while the
semantics are wrong. And the routing story completes the damage: `egress_ready`
is tied to 1, so the confounded updates are also lossy, silently (contra the
entry's own "no backpressure, intentional").

This is the one failure a learning fabric cannot survive: not a wrong constant,
not a timing hazard, but a learning rule that measures the wrong thing while
appearing to learn.

### 1.5 claude — the only learning rule writes zeros, and its guard checks stale state

The failure: **even granting compilation, the intelligence is a no-op with an
unguarded accumulator.** Two mechanisms, both in the code:

1. The Hebbian skeleton stores `16'h0000` as write data (`hebbian_din` is a
   placeholder) — the learning rule literally writes zeros. The "intelligence"
   is a no-op.
2. Granting the placeholder filled in: stages 2–4 of the "4-cycle pipeline"
   execute in one `else if` branch, so `sum` is computed from last cycle's
   `product2` and the saturate check reads last cycle's `sum` — the datapath is
   a one-cycle-lagged cascade mislabeled as a pipeline. The saturation guarantee
   — the entry's only integrity mechanism — would apply one cycle late, letting
   a wrap through on the very cycle the accumulator overflows.

Combined: zero learning, and the mechanism that would have caught the overflow
is structurally blind to it. The entry's honest-limits list concedes starvation
and serialization — the real failures are not in the list, they are in the
datapath. And the sketch's closing claim ("Status: Ready for synthesis") was
false by ten minutes of iverilog; the honesty gap is not a footnote, it is a
warning about the entry's calibration on its own code.

---

## 2. What the fleet believes that might be wrong

The fleet's belief (README Law 3, confirmed by the scorecard's tiebreak):
**intelligence lives at the bottom as fixed-point RTL primitives; the
competition's subject is the intelligence math in silicon; the winner is the
entry with the best math-to-evidence ratio.**

The steelman — intelligence as software on a soft core:

1. **The fabric is tick-paced, and software-class latencies are fine.**
   Everything in every entry is "a few cycles to a few hundred"; ticks are
   thousands of cycles (opencode defaults TICK_LEN = 4096). The entire
   O(latent) state — 16 dials plus an edge table — is a few KB at most, in RAM
   a small core already owns. Throughput is not the argument and never was.
2. **Exactness is the software win.** A soft core gets float, or wider fixed
   point than anyone here dares, with no quantization policy, no rounding
   doctrine, no truncation-bias apparatus, no convergent-rounding wars. The
   entire §3 math policy of every serious entry exists because gates are
   expensive and error is structural. Software just computes — and its golden
   model *is* the implementation.
3. **Doctrine uncertainty is the deepest point.** This one competition fielded
   *three* different decay laws: glm's 2^-i staircase, zeroclaw's W²/P₀
   hyperbola, opencode's two-exponential window. The functional form of
   forgetting is not settled — yet primitives-in-RTL freeze it in gates; a new
   law is a new chip. The fleet's own principle ("bindings are data") argues
   the learning rule should be runtime data — which is exactly what software
   is and what RTL primitives are not. **The fleet's heterogeneity is evidence
   against the fleet's assumption.**
4. **Verification becomes nearly free.** Golden models run in the host
   environment; Law 5 is satisfied by construction; no toolchain tax; no
   UNOPTFLAT, no width sweeps, no `-g2005` archaeology.
5. **The anti-soft-core strawman is not the steelman.** ZeroClaw's §0 attacks
   a *DMA-frame* design — buffer the raw stream, run a program on it. The
   steelman accepts the field-reading doctrine in full (O(latent) state, the
   stream never stored, dials/edges/μ̂/κ̂ as the reading) and asks only: must
   the reading be gates, or may it be instructions?

The counter — why primitives-in-RTL still wins:

1. **The policy is load-bearing, and software conventions rot.** Saturate-never-
   wrap, sticky flags, integer-state-never-drifts, deterministic tick order:
   in software these are style rules; in RTL they are structure. The project
   exists because software state drifts, wraps, and confabulates — the fleet's
   own honest notes document the ρ bias and truncation drift in the codebase
   this is replacing. A soft core re-imports exactly the failure classes the
   bottom layer exists to escape, at the layer that is supposed to be the
   bottom.
2. **The ring is not the disputed part.** Every design needs the ring, the cell
   core, and the opcode decode. The soft core displaces only the primitive
   bank — which is precisely where the doctrine says the guarantees must live.
3. **Scale.** The distribution story (generate-loops, thousands of cells,
   "intelligence degrades gracefully" via `HAS_*` generate-ifs) is only sane
   because per-cell intelligence is a few hundred gates of shift-add. A soft
   core per cell multiplies area and kills the degrade-gracefully story; a
   *shared* soft core re-creates the grant/arbitration problem — glm's weakest
   point, §1.1 — plus interrupts and context switching, i.e. timing
   nondeterminism, which tick-order-semantics forbid by definition.
4. **The fleet already has the software implementation.** Elephant, the C
   quilt — they exist. If software-on-a-core were the answer, the answer would
   be a linker script, not a competition. The competition exists to get the
   reading out of the regime where it can drift.

The steelman's honest residue — the part the synthesis must absorb, not
dismiss: it forces the primitives camp to justify two things on the merits.
(a) Freezing functional form in gates while the doctrine is unsettled enough
that three entries disagree on the decay law. (b) Paying the fixed-point error
apparatus instead of taking float — the apparatus must *earn* its complexity in
verified behavior, not in policy prose. The steal-list already half-answers
(a): glm reserves `LADDER_MODE`, and the scorecard itself merges zeroclaw's
hyperbola and opencode's two-exponential as alternate engines. The synthesis
should go further: make law-select a bind-time dial wherever silicon allows,
and let the train-to-fire acceptance gate be the referee between freeze and
steelman — if the gate only passes with a tuned law, that is evidence the law
is data, not doctrine.

---

## 3. The three questions any synthesis must answer before rtl/ is written

**Q1 — Liveness under load.** What invariant — checkable by testbench or formal
tool — bounds the latency of a `qm_view` response and guarantees every cell's
decay sweep completes when effect traffic saturates the ring and the shared
math tail? (glm's grant FSM is the largest unsketched liveness surface in the
field; opencode's `tick_go && !ci_valid` is the live counterexample of what
happens without such an invariant.)

**Q2 — Non-deferrable time.** Is the tick a hard, hardware-interlocked
deadline — not an advisory phase — such that the busiest cell in the fabric
decays, leaks, and fire-tests on every tick even under continuous ingress, and
can no storm make a cell administratively unreachable (control plane
structurally independent of the data plane)? (opencode's hottest cell silently
stops learning; zeroclaw's no-drop FIFO blocks bind/view behind effects.)

**Q3 — The rule that is verified is the rule that learns.** Is the acceptance
gate end-to-end on the real datapath — train-to-fire-to-decay on the
synthesized fabric, golden-model error bounds asserted at every integrating
boundary — so that a placeholder write (claude's `16'h0000`), a
magnitude-confounded product (seed's AND tree), or a stale saturator (claude's
one-cycle-lagged sum) cannot pass compile-clean review as learning?

---

If the synthesis answers all three affirmatively — with mechanisms, not
paragraphs — build it. If it answers them by waving, the steelman wins, and the
winner should be a soft core.
