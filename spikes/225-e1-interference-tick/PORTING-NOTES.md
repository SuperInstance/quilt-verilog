# E1 → ESP32-S3 .qm Runtime: Porting Notes

Analysis-only pass over `e1.c` (the C99, ESP32-ready half of the spike) and
`e1.py` (the semantic reference). `e1.c` is the port baseline: it is already
integer-only, statically allocated, and pins Python floor semantics via
`fdiv()`. These notes cover the four open questions for landing it on the
ESP32-S3 .qm runtime.

## 1. Memory footprint — static allocation audit

The entire state fits in a handful of bytes; there is nothing to port here
except habits to keep.

- `pulses[64]` × 8 B = **512 B** static (`.bss`). This is the only
  container. `MAX_PULSES=64` is a hard compile-time bound — worst-case loop
  work and worst-case RAM are both fixed at build time, which is exactly
  what a no-malloc discipline wants.
- `result_t` = 7 × int32 = **28 B**, returned by value; on LX7 that lands on
  the caller's stack or is sret'd into caller storage. Make `run()`'s caller
  hold it statically and pass a pointer if the .qm runtime prefers.
- `lcg_x` (4 B) and `n_pulses` (4 B): static, single-instance. Fine for one
  harness instance per core; if .qm ever runs two cells concurrently,
  move both into a context struct — do not add locks.
- `run()` locals: ~15 int32 ≈ **60–100 B stack**, no recursion, no VLAs.
  Peak stack depth across `main → run → fdiv/lcg` is well under 256 B.
- Code size: trivially fits IRAM; no flash-resident data tables at all
  (`reality()` is computed).

Verdict: fits a strict no-malloc loop discipline unchanged. Total footprint
< 1 KiB RAM. The one Python artifact that must not sneak back in: `e1.py`'s
`deque` grows unboundedly; `e1.c` already replaced it with the fixed ring +
tail-trim (`while ... life == 0`). Any .qm port must keep the C behavior —
saturated pulses are silently dropped (`if (n_pulses < MAX_PULSES)`), which
is a bounded-loss policy, not a bug. If pulse saturation matters
scientifically, count drops as an eighth metric rather than allocating.

## 2. The integer contract

**fdiv floor semantics.** This is the load-bearing trap and `e1.c` already
solves it: C `/` truncates toward zero, Python `//` floors toward −∞, and
the pulse decay (`mag - fdiv(mag, 2)`) and pulse magnitude
(`fdiv(|e|, pulse_div)`) both operate on values that can be negative or
non-multiples of the divisor. The LX7 hardware divider truncates like C, so
`fdiv()` must be kept verbatim — one extra divide, one remainder check, one
conditional decrement. Do not "optimize" it to `>>1` or to a raw divide; a
right shift floors for positive values but the sign-symmetric decay relies
on flooring toward −∞ for *negative* magnitudes too (e.g. `fdiv(-3,2) = -2`,
so `-3 - (-2) = -1`, vs truncation giving `-3 - (-1) = -2` — different
trajectory, different metrics, broken cross-substrate contract). Keep the
byte-identical-to-e1.py test as the port's acceptance gate.

**LCG 64-bit intermediate.** `1103515245 * x` with `x < 2^31` needs a 62-bit
product. This is a non-issue on the ESP32-S3: Xtensa LX7 has 32×32→64
multiply (`MULUH`/`MULL`), and GCC lowers `int64_t` multiply to two
instructions plus an add. Keep the `(1103515245LL * lcg_x + 12345LL) &
0x7FFFFFFF` form exactly as written. Only if a future substrate were strict
32-bit would an alternative be needed, in which case the options are:
(a) split the constant into 16-bit limbs (`0x41C64E6D = 0x41C6<<16 | 0x4E6D`)
and accumulate two 32-bit partial products under the 2^31 mask — same
sequence, no semantic change; or (b) switch to xorshift32 — *different*
sequence, breaks byte-identity with `e1.py`, needs re-baselining. Prefer (a).
On ESP32-S3, neither is needed.

**Overflow audit.** All live values are tiny: `reality()` output ∈ [352, 553],
`g` stays within a few hundred of it (observed `max_err` ≤ 61), pulse mags
≤ |e|/3. The only accumulators that grow over 4800 ticks are `events` (~2.6k)
and `debt` (~48k) — both far inside int32. The `int64_t` casts inside
`reality()` (`phase * 8` ≤ 1920) are dead weight; harmless to keep for
symmetry with a scaled-up ADC range (see §4 — if ADC counts 0–4095 map
directly into units, `phase * 8`-style terms still can't exceed ~33k, so
int32 remains safe; only revisit if the micro-unit scale ever exceeds ~2^20).

**Modulo costs.** `lcg_below(n)` does a signed `%` with variable `n`
(hardware divide, ~35 cycles on LX7), once per tick — negligible. `t % 240`
in `reality()` likewise. No change needed.

## 3. Timing — does run() at 4800 ticks fit a fixed-tick budget?

Per-tick work: two `reality()` evaluations (one divide each, ~50 cycles),
one LCG step (~40 cycles), trigger arithmetic (~30 cycles), and the pulse
loops — three passes over live pulses (net-sum, sign-scan, decay), each
O(n_pulses) with a hard ceiling of 64. Typical `n_pulses` is small (pulses
live K=4 ticks), but worst case is 3×64 iterations of a few ALU ops ≈
2–4k cycles. Total worst case ≈ **5k cycles ≈ 21 µs @ 240 MHz**; typical
well under 5 µs. All 4800 ticks back-to-back: < 100 ms worst case.

Consequences for the .qm loop:

- If one harness tick maps to one control-loop period, even a 1 kHz loop
  (1 ms budget) leaves > 95% headroom alongside ADC reads (oneshot ~ a few
  µs, or DMA-continuous ≈ free), the T2 latency buffer update, and telemetry.
  Sensor IO dominates the budget, not the harness.
- The cost is *data-dependent but bounded* — `MAX_PULSES` caps every loop —
  so the tick is real-time safe: no unbounded work, no allocation, no
  blocking calls. It can run in the same task as sensor sampling without
  jitter analysis beyond "≤ 25 µs".
- Do not run `run()` as a 4800-tick batch inside the control loop; batch it
  only on the bench. In production the tick body (lines 58–146 of `e1.c`,
  minus `printf`) becomes the per-cycle callback; `main()`'s sweep loop is a
  host-side tool and stays off-target.
- `printf` in `main()` is the only non-real-time element; replace with
  counters into `result_t` drained by existing .qm telemetry.

## 4. Replacing reality() with a real ADC channel

`reality()` is a deterministic 240-tick piecewise walk in [352, 553]. On
target it becomes a sampled channel; the replacement must preserve the
integer contract and come with a certified noise envelope.

**Quantization.** Use the S3's ADC in raw counts (12-bit, 0–4095) with
eFuse-based calibration applied as integer gain/offset — never route
through float mV. Map counts into harness micro-units with a dyadic shift
(right-shift by k), not an arbitrary divisor: `u = counts >> k`. Choosing
the shift as a power of two keeps the mapping exact and monotone, and keeps
all downstream `fdiv`/trigger arithmetic in the regime already overflow-audited
above. If the signal needs gain instead of attenuation, multiply by a small
integer and keep total scale < 2^20 (see §2).

**Twin structure survives the port.** T1 is the current sample `u(t)`; T2 is
`u(t − lat2)` served from a static `int32_t ring[LAT2_MAX]` — one more
fixed array (~64 B for lat2 ≤ 16), no allocation. The synthetic LCG drift
(`g += lcg_below(...) − drift`) models plant wander; with a real channel the
plant *is* real, so the drift injection should be compiled out or kept
switchable for A/B against the spike baseline. Keep the LCG either way for
dither experiments — it costs one multiply.

**Noise model with dyadic envelope certificate.** The S3 ADC without
averaging shows tens of LSB of noise. The harness's `delta` is the deadband;
for the port it must be chosen as a certified bound, not a guess:

1. Calibration dwell: hold the channel at a steady physical state, sample N
   ticks, record `n_max = max |u(t) − median(u)|` per dwell, across
   temperature/supply corners that matter.
2. Certificate: pick the dyadic bound `N = 2^ceil(log2(n_max + 1))`. The
   certificate is the statement "noise ≤ N, N dyadic", recorded next to the
   dwell log. Dyadic (not arbitrary) so the envelope composes with the
   shift-based quantization above: a k-bit right shift maps the certified
   envelope to `N >> k` exactly, and the deadband check
   `|s − g| ≤ delta` stays integer-exact.
3. Set `delta ≥ N >> k` so sensor noise alone can never trigger a
   correction; the interference signatures (constructive/cancellation/
   chatter) then measure real plant motion against the twins' conflict,
   which is what the experiment is for.
4. Optional hardware assist: multisampling/averaging before quantization
   shrinks `n_max`, hence shrinks the certifiable `N`, hence permits a
   tighter `delta` — the certificate gives a clean before/after comparison.

The spike's own evidence (README) says interference wins under
conflict/stress and loses in calm rooms; the certified envelope is what
tells the runtime which regime it's in, feeding the E4 decision (impulse vs
superposition) that the README names as the follow-on.

## Acceptance gate

Port is done when: (a) `fdiv`-pinned e1.c compiled for S3 reproduces the
`e1.py`/sweep metrics byte-identically for seeds {1, 7, 42, 1999, 20260902}
at both parameter sets; (b) the ADC-driven variant runs a fixed-tick loop
with `delta` set from a recorded dyadic envelope certificate; (c) zero
dynamic allocation confirmed by build (no heap symbols referenced by the
harness objects).
