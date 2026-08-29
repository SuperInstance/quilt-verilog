# Review: opencode — "LOOM/1"

**Reviewer:** cross-review round 2 · **Files:** `proposals/opencode/ARCHITECTURE.md`, `RTL-SKETCH.md`

## Strengths
- **Only entry whose skeletons compile 9/9 under `iverilog -g2005`** — and it said so before we
  ran it ("not compiled… first CI action is the compile gate"). That honesty is worth points.
- **Most complete cell semantics in the field:** bind-as-dial-write with a concrete runtime
  address map (ETA_F/ETA_S/KF/KS/KA/THRESH/REFR/COS_MIN), unbound-cell NAK, refractory fire
  logic, train-then-integrate effect ordering, ack/nak per opcode. This is the only entry where
  the five verbs have full behavioral definitions down to cycle counts.
- **`tb_fabric_smoke` train-to-fire-decay scenario** (§10) is the best acceptance test proposed
  by anyone: prove the fabric *learns* (train w past THRESH, view it, tick until fire, observe
  egress, decay below THRESH). Steal-worthy.
- Ring port deliver/transit/inject contract is clean, with bubble-after-consume and explicit
  inject-vs-transit priority; `q_flit_pipe` registered slices mirror glm's but with a correct
  `ready = !vq || m_ready`.
- Honest-limits section is brutal and specific (14 numbered limits, including "no tool runs
  yet" and "resource numbers are paper").

## Weaknesses (real ones)
- **The math is the least ambitious of the serious entries.** Sum-of-two-exponentials
  "power-law" is the textbook Fusi/Drew/Abbott approximation, credited honestly, but it buys
  ~2 decades with 12% shape error and *user-set* k's — a power-law-shaped window, not a
  heavy-tail memory law. vs glm's bounded staircase or zeroclaw's true hyperbola, it is the
  weakest forgetting story.
- **No κ/vMF, no ln, no log-domain anything.** The entry knows it (limits 1, 13) — link
  admission via cosine floor is all the "field reading" it does.
- **11 verilator warnings on the capstone alone**, including signed-width expansions on `act`
  arithmetic (ST_EFFI integrate, ST_TLEAK leak) — exactly the paths where a silent sign
  extension changes learning behavior. Compile-clean ≠ lint-clean ≠ correct.
- **Caps on scale:** AIDW ≤ 8 (256 ids), EDGES_N ≤ 16 as reg-array, BRAM template swap
  "planned and unexercised." Tier-L gateways specified, not built.
- Tick phases are *advisory* — a wedged cell overrunning phase 0 is detected only by TB
  assertion; the HW watchdog is a "build item" with no sketch.
- `ST_RESP` holds `lo_valid <= 1'b1` then clears on handshake in the same-state branch —
  correct, but the lo_* payload re-assignment every cycle in ST_RESP is wasteful and the
  `tick_go` latch can delay ticks indefinitely under sustained ingress (only fires when
  `!ci_valid`) — starvation is acknowledged nowhere.

## What it missed
- **Fixed-point correctness:** truncation everywhere with bias "counted in the TB budget" —
  no convergent rounding; sign-extension warnings suggest the budget hasn't been audited yet.
- **Fabric-size portability:** tier table exists but every hard number stops at tier-M; the
  BRAM swap — the actual scaling hinge — is unexercised.
- **Testbench feasibility:** best behavioral coverage plan of the field (fuzz + watchdog +
  protocol checkers), weakest numeric-verification plan (no golden-model error-bound
  assertions like glm's exact-equality dial test or zeroclaw's κ-vs-bisection bound).
- **Purity:** compliant (no `initial`, no SV constructs, `$clog2` avoided even); lint hygiene
  mediocre.

## Scores
| Novelty | Buildability | Purity | Distribution | Total |
|---|---|---|---|---|
| 7/10 | 10/10 | 9/10 | 7/10 | **33/40** |

Tied with glm on total; loses the tiebreak on novelty (the competition's subject is the
intelligence math, and two-exponential decay + cosine is the conservative read of it).
Buildability is untouchable: 9/9 compile, full opcode semantics, best acceptance test.
