# E6 slice — E1 interference tick on the ESP32-S3 .qm runtime

Port plan for landing `e1.c` (the C99 reference contract) on the ESP32-S3
.qm cell runtime. `e1.c` is the authority: this document maps its `run()`
body onto the five opcodes (`qm_bind`/`qm_link`/`qm_effect`/`qm_view`/
`qm_tick`) without changing a single arithmetic decision. Integer-only
end to end — **no floats anywhere**: not in the harness, not in the ADC
calibration path, not in the certificate math, not in the metrics.

Contract recap (pinned by the spike, see README / DIVERGENCE.md):

1. `fdiv()` floor division, verbatim. Never `>>1`, never raw `/`.
2. LCG `(1103515245LL * x + 12345) & 0x7FFFFFFF`, 64-bit intermediate.
3. Pulse queue is FIFO with **oldest-first** expiry.
4. Decay reads the pre-decay snapshot; all pulses decay within one tick,
   no in-place contamination.
5. Acceptance = byte-identical integer metrics vs `e1.py` for seeds
   {1, 7, 42, 1999, 20260902}.

## 1. Cell decomposition

Four cells. One harness instance per core; all state static (no heap).

| Cell | Owns | e1.c origin |
|---|---|---|
| `e1/sense` | channel source: `reality(t)` on the bench, ADC counts on target; latency ring for the lagging twin | lines 32–38, 59–61 |
| `e1/drift` | LCG plant-wander source (switchable; off when the plant is real) | lines 23–30, 64 |
| `e1/core` | plant account `g`, trigger scan, pulse ring, superposition + decay | lines 53–144 |
| `e1/ledger` | `result_t` — events, debt, constructive, cancellations, chatter, max_err, settles | lines 45–48, all `r.*` updates |

RAM budget (static, `.bss`): pulse ring 64 × 8 B = 512 B; sense latency
ring 16 × 4 B = 64 B; `result_t` = 28 B; cell dials + LCG state ≈ 32 B.
**Total < 1 KiB.** `run()` tick locals ≈ 60–100 B stack, no recursion.

## 2. Wiring (`qm_link`)

Links are negotiated once at setup; they carry no per-tick policy.

```
e1/sense ──s1──▶ e1/core        live twin        (view channel, F = 0)
e1/sense ──s2──▶ e1/core        lagging twin     (view channel, F = lat2)
e1/drift ──w───▶ e1/core        plant wander     (effect channel)
e1/core  ──leg─▶ e1/ledger      bookkeeping legs (effect channel)
```

- `s1`/`s2` are **views** (shadow, read-only telemetry direction) — the
  twins observe the plant; they never write it. This matches the
  view-vs-effect direction rule (`qm_view` = shadow, `qm_effect` = twin).
- `w` and `leg` are **effects** (balanced transactions): the drift effect
  debits `e1/drift` and credits `g`; every ledger leg debits `e1/core` and
  credits the account named in the flit. No metric enters the ledger
  without its leg.
- Telemetry drains are additional `qm_view` links from the host to
  `e1/ledger` and `e1/core` (see §6).

## 3. Dial binding (`qm_bind`)

All configuration travels as bind traffic, booked as transactions. Binds
are only legal between runs (or in the runtime's RUN-state window), never
mid-tick.

| Dial | Type | Default (stress arena) | Bind effect |
|---|---|---|---|
| `mode` | {0=sequential, 1=interference} | 1 | selects the arm at lines 83 / 95 |
| `seed` | int32 | swept | reseeds LCG (`lcg_seed`: `& 0x7FFFFFFF`, 0→1) |
| `K` | 1..16 | 4 | pulse initial life |
| `pulse_div` | 1..8 | 3 | `fdiv(|e|, pulse_div)` divisor |
| `delta` | int32 | 12 (bench) / from certificate (target, §7) | deadband |
| `drift` | 0..16 | 6 (bench) / 0 (target) | LCG wander half-range; 0 compiles the drift effect out behaviorally |
| `lat2` | 0..16 | 10 | lagging-twin delay; sizes the sense ring read offset |
| `src` | {0=reality(), 1=ADC} | 0 | sense-cell source select |

Binding `seed` is the run-reset transaction: it also zeroes `g`'s pending
state (`g = reality(0)` or first ADC sample), flushes the pulse ring
(count = 0), and zeroes `result_t` via a leg to `e1/ledger`.

## 4. The tick (`qm_tick`)

One `qm_tick` on the harness = one iteration of the `for (t…)` loop
(e1.c lines 58–151). Order is pinned; the .qm tick scheduler runs the
scheduled work in exactly this sequence. Flit fields use the fabric
contract `{op, src, dst, a0, a1, a2, dat}`.

| Step | e1.c lines | Opcode | Payload |
|---|---|---|---|
| 1. Sample twins | 59–61 | `qm_view` `core→sense` ×2 | returns `s1 = u(t)`, `s2 = u(t−lat2)` (s2t clamped at 0). Bounded freshness: s2's staleness *is* lat2, by construction |
| 2. Wander | 64 | `qm_effect` `drift→core` | `dat = lcg_below(2*drift+1) − drift`; credit `g += dat`. On target with `drift=0` this effect is elided (the real plant wanders on its own) |
| 3. Expire pulses | 69–72 | internal to tick | advance ring head past `life == 0` entries (§5) — O(live), no flit |
| 4. Trigger scan | 74–81 | internal | `e1=|s1−g|`, `e2=|s2−g|`, `trig1/trig2`, `max_trig` |
| 5a. Sequential arm | 83–94 | `qm_effect` `core→core` (snap) + leg | snap applies `g += e` atomically in-tick; then leg below |
| 5b. Interference arm | 95–143 | pulse push (internal) + `qm_effect` net application | pulses pushed to ring (§5); `net = Σ mag`; decay all (§6); `g += net` as the tick's single plant effect |
| 6. Bookkeeping | 87–93, 105–117, 127, 136–142, 146–150 | `qm_effect` `core→ledger`, one per tick | `a0 = err` (post-tick max twin error), `a1 = flags` bitfield {within1, within2, event, constructive, cancellation, chatter}, `a2 = |e|` debt mass (0 if no event), `dat = t` (nonce/ordering) |
| 7. Publish | — | (state becomes viewable) | end-of-tick commit; views issued after this point see tick `t` state |

`e1/ledger` is a pure fold over step-6 legs:
`events += flags.event`, `debt += a2`,
`cancellations += flags.cancellation`, `chatter += flags.chatter`,
`constructive += flags.constructive`, `max_err = max(max_err, a0)`,
`settles += flags.within1 & flags.within2`. Every metric is event-sourced;
the audit trail is the default semantics, not a feature.

Bench vs production: on the bench, batch 4800 `qm_tick`s back-to-back
(worst case < 100 ms at 240 MHz; ≤ ~21 µs/tick worst, ~5 µs typical — see
PORTING-NOTES §3). In production the tick body is the per-cycle callback
of the control loop; even a 1 kHz loop leaves > 95% headroom next to ADC
oneshot reads and telemetry. Never batch inside the control loop.

## 5. Pulses deque → ring buffer

`e1.py`'s unbounded `deque` becomes a fixed power-of-two ring, FIFO with
oldest-first expiry — the geometry the spike pinned as contract #3.
`e1.c` already gets the *semantics* right with an O(n) shift; the .qm
port keeps the semantics and makes the container O(1). 64 = 2⁶, so wrap
is a mask, not a divide.

```c
#define MAX_PULSES 64                 /* 2^6: wrap by mask */
#define RING_MASK  (MAX_PULSES - 1)

typedef struct { int32_t mag, life; } pulse_t;

static pulse_t ring[MAX_PULSES];      /* 512 B static */
static int32_t head;                  /* OLDEST live pulse */
static int32_t count;                 /* live pulses, 0..64 */
static int32_t drops;                 /* optional 8th metric */

static void ring_push(int32_t mag, int32_t life) {
    if (count < MAX_PULSES) {         /* bounded-loss policy, not a bug */
        ring[(head + count) & RING_MASK].mag  = mag;
        ring[(head + count) & RING_MASK].life = life;
        count++;
    } else {
        drops++;                      /* saturation is counted, never allocated */
    }
}

static void ring_expire(void) {       /* oldest-first, from the head */
    while (count > 0 && ring[head].life == 0) {
        head = (head + 1) & RING_MASK;
        count--;
    }
}
```

Iteration order for net-sum / sign-scan / decay is `ring[(head + i) &
RING_MASK]` for `i` in `0..count-1`. Equivalence to `e1.c` holds because
both are FIFO with expiry at the oldest end; the shift array and the ring
visit live pulses in the same order, so `net`, `opp`, and per-pulse decay
see identical values. `drops` is the eighth metric PORTING-NOTES §1
sanctions — report it, don't allocate around it.

## 6. Decay = integer halving, floor semantics

Load-bearing: decay is `mag − floor(mag/2)` for **signed** `mag`. C `/`
truncates toward zero and breaks the negative half of the trajectory
(`fdiv(−3,2) = −2` → `−3 −(−2) = −1`; truncation gives `−2` — different
trajectory, different metrics, broken cross-substrate contract). `fdiv()`
is kept **verbatim** from e1.c:

```c
static int32_t fdiv(int32_t a, int32_t b) {   /* floor toward −inf */
    int32_t q = a / b;
    if ((a % b != 0) && ((a < 0) != (b < 0))) q--;
    return q;
}
```

Decay pass (from the pre-decay snapshot; one pass, all pulses, then the
single `g += net`):

```c
for (i = 0; i < count; i++) {
    int32_t mag = ring[(head + i) & RING_MASK].mag;
    if (mag > 1 || mag < -1) mag = mag - fdiv(mag, 2);
    ring[(head + i) & RING_MASK].mag = mag;
    ring[(head + i) & RING_MASK].life--;
}
```

Forbidden substitutions: `mag >> 1`, `mag / 2`, `mag - (mag >> 1)`. The
LX7 hardware divider truncates exactly like C, so `fdiv` costs one extra
divide + remainder check + conditional decrement per pulse — worst case
64 × ~40 cycles, inside the 21 µs tick budget. The same `fdiv` covers the
pulse magnitude `fdiv(|e|, pulse_div)` (divisor is a dial, positive, but
the contract pins one code path for all division).

LCG likewise verbatim (62-bit product; LX7 lowers `int64_t` multiply to
`MULUH`/`MULL` + add):

```c
lcg_x = (int32_t)((1103515245LL * lcg_x + 12345LL) & 0x7FFFFFFFLL);
```

## 7. Real ADC channel + dyadic-envelope certificate

On target, `e1/sense` swaps `reality(t)` for a sampled channel (ADC1,
12-bit raw counts, oneshot or DMA-continuous). The twin structure
survives: `s1 = u(t)`; `s2 = u(t − lat2)` served from the sense cell's
static `int32_t lat_ring[LAT2_MAX]` (64 B at lat2 ≤ 16), same mask-wrap
idiom as §5.

**Quantization — integer only, dyadic only.**

- eFuse calibration applied as integer gain/offset: `c = (raw * gain >>
  CAL_SHIFT) + off`. Never route through float mV.
- Map counts to micro-units by shift, never by arbitrary divisor:
  `u = c >> k`. The dyadic shift keeps the mapping exact and monotone and
  keeps every value inside the overflow-audited regime (PORTING-NOTES §2:
  total scale < 2²⁰, int32 throughout).
- If gain is needed instead of attenuation, multiply by a small integer
  before the shift; re-audit the < 2²⁰ bound.

**Dyadic-envelope certificate checklist** — `delta` is a certified bound,
not a guess:

- [ ] **Dwell.** Hold the channel at a steady physical state. Sample
      N ≥ 4800 ticks (one full run length) at the production tick rate.
      Record raw counts.
- [ ] **Convert.** Apply the production path exactly: calibration →
      `>> k`. All integer. Record `k`, `gain`, `off`, `CAL_SHIFT`.
- [ ] **Center.** Compute the integer median `m` of `u(t)` (select, not
      mean — no float). Record it.
- [ ] **Excursion.** `n_max = max_t |u(t) − m|`. Repeat the dwell across
      the temperature/supply corners that matter; keep the worst `n_max`.
- [ ] **Bound.** `N = 2^ceil(log2(n_max + 1))`, computed integer-only
      (bit-scan / `__builtin_clz`). The certificate is the statement
      "noise ≤ N, N dyadic", recorded next to the dwell log:
      `{n_max, N, k, gain, off, corners, date}`.
- [ ] **Compose.** The k-bit shift maps the envelope exactly:
      envelope in micro-units is `N >> k`. Set the dial
      `delta ≥ N >> k` via `qm_bind`. Then sensor noise alone can never
      fire a trigger, and the interference signatures (constructive /
      cancellation / chatter) measure real plant motion.
- [ ] **Verify.** Run a noise-only dwell through the full harness:
      `events == 0` for the whole run. Any event falsifies the
      certificate — re-dwell, don't widen `delta` by hand.
- [ ] **(Optional) Tighten.** Enable ADC multisampling/averaging before
      quantization, re-run the checklist, record the new smaller `N`.
      The certificate gives the before/after comparison for free.
- [ ] **A/B.** Bind `drift = 0` (real plant wanders itself) but keep the
      LCG cell linked — it costs one multiply and stays available for
      dither experiments and regression against the spike baseline.

## 8. Acceptance gate (port is done when)

1. **Byte-identity.** The S3 build, bench source (`src=0`), runs the
   stress sweep — seeds {1, 7, 42, 1999, 20260902} × {sequential,
   interference} at K=4, pulse_div=3, delta=12, drift=6, lat2=10 — and
   reproduces `e1.py`/`c-sweep.csv` **exactly** on the six integer
   metrics (events, debt, constructive, cancellations, chatter, maxErr),
   10/10 rows. Full CSV diff is the gate, not spot checks. The pct column
   is derived integer per-mille (`settles * 1000 / 4800`); reconcile via
   the settles count, never via float percent.
2. **ADC variant.** Runs a fixed-tick loop with `delta` set from a
   recorded dyadic-envelope certificate (§7 checklist complete, dwell log
   + certificate in-repo), and the noise-only falsification run shows
   `events == 0`.
3. **No heap.** Build confirms zero dynamic allocation: no heap symbols
   referenced by the harness objects; all state static per §1 (< 1 KiB).
4. **Tick budget.** Worst-case tick ≤ ~21 µs @ 240 MHz measured on target
   (bounded by `MAX_PULSES`, data-dependent but capped — real-time safe).

## 9. DEVIL cross-exam receipts (2026-09-03)

Three challenges, three answered with receipts — the port doc is
destined for the boat, so the edges live here in writing.

**(1) Held-out seeds — not training-data agreement.** The §8 sweep uses
the five dev seeds `{1, 7, 42, 1999, 20260902}` — the same seeds the
arena policies were iterated on, so "10/10" alone would be agreeing
with its training data. Cross-exam result: the held-out set
`{13, 313, 777, 271828, 90210}` run through the same ring translation
at stress params reproduces `e1.py` **exactly on all six integer
metrics, 10/10 rows** (pct column reconciles as percent-vs-per-mille:
50.6% == 506‰). The claim "ring-verified" survives the 727ab7d
seed-split test.

**(2) Horizon — no additive drift at 10×.** Integer conversion is a
silent-semantics class, so the horizon of the verification sweep is now
stated and tested: both engines are already integer-only end to end
(e1.py has no float path; `pct_within` percent is reporting-only), and
at **48,000 ticks (10× the sweep horizon)** all 10 rows — 5 dev seeds ×
2 arms — reproduce exactly (events, debt, constructive, cancellations,
chatter, maxErr). A full per-tick `g`-trace diff (seed 1, interference,
48k points) is byte-identical. There is no slow integer/float diverge
to accumulate: drift is additive-checkable and checks clean at 10×.
Honest caveat: 48k ≠ unbounded; the .qm target adds ADC quantization
(§7 certificate), which is a NEW integer input stream, not a rounding
accumulation — covered by the dyadic-envelope checklist, not by this
sweep.

**(3) Ring overflow — policy is drop-new, divergence documented.** The
64-entry pulse ring is FIFO with a **drop-new** overflow policy: the
push sites are guarded `if (n_pulses < MAX_PULSES)` — a trigger that
arrives with the ring full is counted (events/debt still booked) but
its pulse never enters the superposition. e1.py's `deque` grows
unboundedly, so under sustained interference beyond 64 live pulses the
C/.qm plant gets *less* correction than the Python twin. That regime is
unreachable in the verification harness: pulse life is K=4..5 ticks and
at most 2 pulses enter per tick, so live-pulse peak is ~2K = 8..10,
6× below overflow. On the boat, sustained ring-full means trigger rate
≥ 16/snaps-per-life-tick — by then the delta deadband (§7 certificate)
is mis-sized, which is a separate, louder alarm. Signed int32 `g`
cannot overflow in-regime (random walk ±~800 at 48k ticks vs 2³¹).
