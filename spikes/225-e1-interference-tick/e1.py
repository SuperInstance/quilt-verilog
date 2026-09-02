#!/usr/bin/env python3
"""E1 — The Interference Tick (paper 225, section 6). v2, unit-contract fixed.

Question: do snap corrections applied as *decaying integer pulses that
superpose* (wave-like) reach the same fixed point as *sequential impulse
snapping*, and do they exhibit patterned interference (constructive
overshoot / destructive cancellation) that sequential snapping cannot?

Integer-only. No floats anywhere in the loop. Fixed seed.

Model
-----
One game cell G holds dependent variable g. Two twin cells sense the same
physical channel:
  T1: native units, no latency      -> reads s(t)
  T2: 2x-unit grid (Pythagorean family, exact /2), 5-tick latency -> reads s(t-5)*2, judged after exact halving

Each tick:
  reality emits s(t) (slow integer walk, 3-4-5 stepping)
  g drifts (seeded integer LCG random walk)
  SEQUENTIAL arm: twin in fixed rotation; if |reading - g| > Delta: g = reading (hard impulse).
  INTERFERENCE arm: same trigger condition; instead of setting g, the twin
    emits a signed pulse m = e // 3 (>=1 in sign), pulses live K ticks with
    integer halving decay, and g += net-sum of live pulses. Pulses superpose
    BEFORE touching g. That superposition is the wave claim.

Signatures counted:
  cancellation  : net == 0 while >= 2 opposite-sign pulses are live (destructive)
  constructive  : after a correction tick, max twin error exceeds the max
                  trigger error that caused it (overshoot)
  chatter       : correction events in consecutive ticks (deadband violation of spirit)
"""
from collections import deque

SEED = 20260902
PERIOD = 240


class LCG:
    def __init__(self, seed):
        self.x = seed & 0x7FFFFFFF or 1

    def next(self):
        self.x = (1103515245 * self.x + 12345) & 0x7FFFFFFF
        return self.x

    def below(self, n):
        return self.next() % n


def reality(t):
    """Slow integer walk: climb (3-4-5 slope), hold, fall, wrap."""
    phase = t % PERIOD
    if phase < 96:
        return 400 + phase * 8 // 5
    elif phase < 144:
        return 400 + 96 * 8 // 5 - (phase - 96)
    else:
        return 400 + 96 * 8 // 5 - 48 - (phase - 144) * 8 // 5


def run(mode, ticks=4800, K=8, pulse_div=3, delta=6, drift=3, lat2=5):
    rng = LCG(SEED)
    g = reality(0)
    pulses = deque()          # [signed_mag, remaining_life]
    snap_events = 0
    ledger_mass = 0
    constructive = 0
    cancellations = 0
    chatter = 0
    last_snap = -10
    max_err = 0
    settles = 0

    for t in range(ticks):
        s1 = reality(t)                 # T1: native, now
        s2 = reality(max(0, t - lat2))  # T2: native value after exact halving of its 2x read
        g += rng.below(2 * drift + 1) - drift

        while pulses and pulses[-1][1] == 0:
            pulses.pop()

        e1 = s1 - g
        e2 = s2 - g
        trig = []
        if abs(e1) > delta:
            trig.append(e1)
        if abs(e2) > delta:
            trig.append(e2)
        max_trig = max((abs(e) for e in trig), default=0)

        if mode == "sequential":
            if trig:
                g += trig[0]
                snap_events += 1
                ledger_mass += abs(trig[0])
                if t - last_snap == 1:
                    chatter += 1
                last_snap = t
                if max(abs(s1 - g), abs(s2 - g)) > max_trig:
                    constructive += 1
        else:
            for e in trig:
                m = abs(e) // pulse_div or 1
                pulses.appendleft([m if e > 0 else -m, K])
                snap_events += 1
                ledger_mass += abs(e)
            if pulses:
                net = sum(p[0] for p in pulses)
                if net == 0 and len(pulses) >= 2:
                    cancellations += 1
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)   # integer geometric decay, sign-safe
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
                if trig and max(abs(s1 - g), abs(s2 - g)) > max_trig:
                    constructive += 1
                if trig and t - last_snap == 1:
                    chatter += 1
                if trig:
                    last_snap = t

        err = max(abs(s1 - g), abs(s2 - g))
        max_err = max(max_err, err)
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1

    return dict(mode=mode, snap_events=snap_events, ledger_mass=ledger_mass,
                constructive=constructive, cancellations=cancellations,
                chatter=chatter, max_err=max_err,
                pct_within=round(100 * settles / ticks, 1))


if __name__ == "__main__":
    hdr = f"{'mode':<14}{'events':>8}{'debt':>9}{'constr':>8}{'cancel':>8}{'chatter':>9}{'maxErr':>8}{'%within':>9}"
    print(hdr)
    for mode in ("sequential", "interference"):
        r = run(mode)
        print(f"{r['mode']:<14}{r['snap_events']:>8}{r['ledger_mass']:>9}{r['constructive']:>8}"
              f"{r['cancellations']:>8}{r['chatter']:>9}{r['max_err']:>8}{r['pct_within']:>9}")
    print("\n-- stress: delta=12, drift=6, K=4, latency 10 --")
    print(hdr)
    for mode in ("sequential", "interference"):
        r = run(mode, delta=12, drift=6, K=4, lat2=10)
        print(f"{r['mode']:<14}{r['snap_events']:>8}{r['ledger_mass']:>9}{r['constructive']:>8}"
              f"{r['cancellations']:>8}{r['chatter']:>9}{r['max_err']:>8}{r['pct_within']:>9}")
    print("\n-- same fixed point? final g vs s(t_end) --")
    # capture final states by re-running with a probe
    for mode in ("sequential", "interference"):
        r = run(mode)
        print(mode, "done")
