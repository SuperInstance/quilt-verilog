# DIVERGENCE.md — e1.c interference-arm divergence from e1.py

**Scope:** diagnosis only. `e1.c` was not modified. Fix verified on a scratch
copy (`/tmp/opencode/e1_fixed.c`), reproducing `e1.py` byte-identically.

## Symptom (reproduced)

Stress params (delta=12, drift=6, K=4, lat2=10), seed 20260902:

| arm        | events | debt  | maxErr | %within |
|------------|--------|-------|--------|---------|
| py int     | 2070   | 35508 | 39     | 83.0    |
| c int      | 4376   | 96832 | 56     | 25.8    |

C interference events swing 2741..4494 across seeds; Python is stable
(~2009..2070). Sequential arm matches exactly (2513 / 48397 on every metric),
which localizes the bug to the interference branch — specifically to the
pulse container.

## Root cause: pulse expiry trims the wrong end of the array

`e1.c:66-67`:

```c
/* expire dead pulses (tail) */
while (n_pulses > 0 && pulses[n_pulses - 1].life == 0) n_pulses--;
```

Python (`e1.py:80-81`, `e1.py:105`) inserts with **`appendleft`**: the deque is
newest-first, so the **oldest** pulse sits at the tail, and
`while pulses and pulses[-1][1] == 0: pulses.pop()` correctly removes dead
(oldest) pulses from the tail.

The C port appends new pulses at `pulses[n_pulses]` (`e1.c:95-99`,
`e1.c:106-110`), i.e. **oldest-first, newest at the end** — the insertion end
was flipped (`appendleft` → append) without flipping the expiry end
(tail → front). Dead pulses (life==0) are always at the **front** in C; the
trim tests the **newest** pulse at `n_pulses-1`, which has the highest life,
so it almost never fires.

Instrumented probe (scratch copy, seed 20260902 stress): first divergence
appears within the first ~10 ticks — after expiry the array reads
`lives: 0 2 3`: a dead pulse at the front behind live ones, already counting
toward `net`.

### Failure cascade

1. A dead pulse (life==0) is never trimmed; it is summed into `net`
   (`e1.c:116`) although Python removed it before summing.
2. The decay loop decrements it to −1, −2, … (`e1.c:128`). `life == 0` can
   never be true again → the pulse is **immortal**.
3. Its magnitude decays to ±1 and freezes there (guard `mag > 1 || mag < -1`
   skips ±1, `e1.c:126`), so it contributes ±1 to `net` **every tick,
   forever**.
4. Zombies accumulate until `n_pulses` saturates at 64. Probe totals per
   4800-tick run: ~293k–295k dead-pulse contributions to `net` (≈61 per tick
   at saturation), `max_n_pulses = 64` on every seed.
5. At saturation, new legitimate pulses are silently dropped
   (`if (n_pulses < MAX_PULSES)`) while still counted as events — probe:
   1770–3401 dropped per run.
6. The frozen zombie sum is a persistent, seed-dependent bias applied to `g`
   each tick → chronic re-triggering → inflated events/debt/chatter,
   collapsed %within, and wild seed-to-seed variance. That is exactly the
   observed signature.

Sequential arm is unaffected because it never touches `pulses[]` — hence the
exact match.

## Suspects checked and cleared

- **Insertion order (`appendleft` vs append) — not a bug by itself.**
  Order within the container affects nothing observable: `net` is a
  commutative sum, decay is per-pulse independent, and cancellation detection
  uses order-insensitive sign flags. Proof: the verified fix keeps C's
  append-at-end (opposite of Python's deque order) and matches byte-identically.
  Order matters only insofar as it decides **which end expiry must trim** —
  and that end was not flipped. This is the bug.
- **Decay in-place mutation — correct.** Python sums `net` from the pre-decay
  snapshot, then builds a fresh `decayed` deque. C completes the full `net`
  sum (`e1.c:116`) *before* the in-place decay loop (`e1.c:124-129`), and each
  magnitude update reads only its own value. No contamination of the sum or
  of sibling pulses.
- **Expiry position in the tick** (after drift, before error computation) —
  matches Python.
- `fdiv`, LCG, `reality()`, `max_trig`, pulse magnitude `|e|//3 or 1`,
  cancellation predicate (C's opposite-sign check is implied by Python's
  `net==0` with nonzero mags) — all equivalent; sequential-arm equality
  corroborates the shared plumbing.

## Minimal fix

One change at `e1.c:66-67`: trim dead pulses from the **front** (the array is
oldest-first), compacting the remainder:

```c
/* expire dead pulses (front: this array is oldest-first, unlike
 * Python's appendleft deque where the oldest sits at the tail) */
{
    int32_t d = 0;
    while (d < n_pulses && pulses[d].life <= 0) d++;
    if (d > 0) {
        for (i = d; i < n_pulses; i++) pulses[i - d] = pulses[i];
        n_pulses -= d;
    }
}
```

`life <= 0` rather than `== 0`: identical behavior once trimming is correct
(lives never reach 0 mid-array while newer pulses live, and never go
negative), and self-healing if a negative life ever reappears.

## Verification

Patched copy (e1.c in the workspace untouched) vs `e1.run()`, seeds
{1, 7, 42, 1999, 20260902} × {sequential, interference} × {default params,
stress params}: **all metrics byte-identical** (events, debt, constructive,
cancellations, chatter, maxErr, settles). Seed 20260902 stress interference:
2070 / 35508 / 79 / 68 / 927 / 39 / 83.0% — exact match to Python.

With correct expiry, `n_pulses` peaks at 2·K (8 stress, 16 default) — nowhere
near `MAX_PULSES=64`, so saturation-drop can no longer occur in these sweeps.

## Secondary (cosmetic) observation

`pctW` printing differs in rounding policy: C truncates
(`(settles * 1000) / TICKS`) while the Python sweep rounds
(`round(100 * settles / ticks, 1)`), so identical states can print 518 vs 519
per-mille (visible in the otherwise-matching seq rows of `c-sweep.csv` vs
`py-sweep.csv`). Simulation state is identical (verified on raw `settles`);
align the printers only if the acceptance gate requires literally identical
CSV text.

## Note for PORTING-NOTES.md

`PORTING-NOTES.md` §1 currently blesses the faulty construct ("e1.c already
replaced it with the fixed ring + tail-trim") and calls saturation-drop "a
bounded-loss policy, not a bug". Both statements should be corrected when the
fix lands: the tail-trim is the divergence, and with correct expiry the
64-slot cap is never reached in these parameter regimes.
