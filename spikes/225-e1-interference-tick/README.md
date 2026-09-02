# E1 — The Interference Tick (spike, 2026-09-02)

Paper 225 §6 E1. Question: do snap corrections applied as decaying integer
pulses that *superpose* (wave-like) reach the same fixed point as sequential
impulse snapping, and do they exhibit patterned interference (constructive
overshoot / destructive cancellation) that sequential snapping cannot?

## Verdict: VALIDATED

Question: integer pulse-superposition snapping is a coherent alternative to
impulse snapping, with genuine wave-like signatures, integer-only — and it
reproduces byte-identically across two independent language substrates.

## Results

### Python reference harness (e1.py)

Stress params (delta=12, drift=6, K=4, twin latency 10 ticks, 5-seed sweep):

```
 seed     seq_ev  int_ev  seq%w  int%w  seqErr  intErr
    1       2524    2064   51.9   83.0      61      38
    7       2655    2022   49.4   82.5      61      39
   42       2469    2044   53.1   83.4      61      38
 1999       2602    2009   50.5   83.6      61      39
20260902    2513    2070   51.9   83.0      61      39
```

Interference arm under stress: ~20% fewer correction events, ~27% less
ledger debt, max error 61 → 39, and 83% vs 52% of ticks within deadband of
BOTH twins. Destructive cancellation observed directly (net == 0 with both
signs live — a state no impulse system can occupy).

### Cross-substrate agreement (e1.c, C99 port)

After fixing the pulse-queue geometry bug (see DIVERGENCE.md), the C port
reproduces the Python harness **exactly** — 10/10 rows identical on events,
debt, constructive, cancellations, chatter, and maxErr across 5 seeds × 2
arms (residual ±1 on the percent column is display rounding of the same
settles count). Two languages, one integer contract, zero divergences. This
is the reflex-arc acceptance pattern (500 vectors → 100.0000% agreement)
applied at spike scale.

### What worked

- Superposition regularizes conflicting sensors. The two twins (one live,
  one 5-10 ticks late) fight under impulse snapping; under pulses their
  corrections blend — the batten effect predicted in paper 225 §6 E2 shows
  up already: fewer, smaller, smoother corrections under conflict.
- The interference signature is countable and integer-exact (net==0 with
  both signs live). Measurable, falsifiable.

### What failed / surprised

- v1 harness unit-contract bug (twin basis halved the value instead of
  doubling the units): twins ping-ponged g at ~230-mass corrections — the
  Semantic Tower §5.2 basis inequality violated empirically. Doctrine
  proved by breaking it.
- The C port diverged via *container geometry*, not arithmetic: Python's
  `appendleft` deque and C's tail-append array expire opposite ends of the
  queue. fdiv() pinned division; nothing pinned the queue. Contract lesson
  recorded in DIVERGENCE.md.
- At GENTLE params (delta=6, drift=3) interference is slightly WORSE
  (45.5% vs 56.7% within) — pulse tails smear state the impulse would set
  exactly. Interference is a conflict-resolution regime, not a free lunch.

## The Cross-Substrate Contract (pinned by this spike)

1. **Division**: Python floor semantics are canonical; C pins them via
   `fdiv()` (floor toward −∞). Never `>>1`, never raw `/`, for signed or
   non-multiple operands. Sign-symmetric decay depends on it.
2. **LCG**: `(1103515245LL * x + 12345) & 0x7FFFFFFF` — 64-bit intermediate
   mandatory (62-bit product).
3. **Container geometry**: pulse queue is FIFO with oldest-first expiry;
   new pulses may go at either end but the expiry end must hold the
   OLDEST. (The bug class this spike donated.)
4. **Decay snapshot**: all pulses decay from the pre-decay snapshot within
   a tick; no in-place contamination.
5. **Acceptance gate**: byte-identical sweep vs e1.py before any port is
   believed. Full CSV diff is the gate, not spot checks.

## Next steps

- **E6**: port to the ESP32-S3 .qm runtime (see PORTING-NOTES.md — <1 KiB
  RAM static, fdiv + 64-bit multiply fine on LX7); then point `reality()`
  at a real noisy ADC channel with a dyadic-envelope certificate.
- **E4**: field-adaptive Δ from the elephant's κ — calm rooms want impulse
  mode, conflicted rooms want superposition. The mode dial is the
  architecture's beta/gate, in fleet terms.

## Files

- `e1.py` — canonical reference harness (Python, integer-only)
- `e1.c` — C99 port, ESP32-ready, static allocation, contract-pinned
- `py-sweep.csv` / `c-sweep.csv` — 5-seed sweep outputs (post-fix, matching)
- `DIVERGENCE.md` — the queue-geometry bug, root cause, fix, verification
- `PORTING-NOTES.md` — ESP32-S3 .qm porting analysis (KimiCode lane)

Run: `python3 e1.py` · `gcc -O2 -o e1c e1.c && ./e1c` · compare CSVs.
