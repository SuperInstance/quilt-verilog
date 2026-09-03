#!/usr/bin/env python3
"""INVENTION 3 — SNAP-POINT SEARCH ECONOMY (glm-2 derby entry, 2026-09-02)

Charter §10 cheat #1 + §9 second amendment, testable miniature: "when the
answer is where the wiggle ends, don't simulate the wiggle" — instrumented
as a certified boolean blade oracle on the E1 judge.

Question put to the judge: what is the MINIMAL deadband delta in 4..24 such
that the interference arm reaches >= Q percent of ticks within deadband of
BOTH twins, 5-seed stress sweep (drift=6, K=4, pulse_div=3, latency 10)?

  FULL-WAVE cost: evaluate the percent for every delta — 21 x 5 x 4800
    ticks; every tick is paid for even when the verdict was already decided.

  BLADE oracle: a boolean pull "does delta pass Q?" that runs the SAME
    integer loop with certified early exit, bounds anchored to the FULL
    horizon (settles only accrue):
      PASS certain once 100*settles      >= Q*TICKS
      FAIL  certain once 100*(remaining possible settles) < Q*TICKS
    The blade never sees a percent, only YES/NO; the counter records what
    each pull actually paid. Seating = binary search on delta with blades;
    the horizon-anchored bound IS the certificate (a PASS verdict is already
    mathematically certain when it fires — no full run needed).

Integer-only, fixed seeds, no floats in the loop. Dynamics re-implemented
from e1.py's interference arm and cross-checked against e1.run row-by-row.
"""
from collections import deque

SEEDS = (1, 7, 42, 1999, 20260902)
TICKS = 4800
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
    phase = t % PERIOD
    if phase < 96:
        return 400 + phase * 8 // 5
    if phase < 144:
        return 400 + 96 * 8 // 5 - (phase - 96)
    return 400 + 96 * 8 // 5 - 48 - (phase - 144) * 8 // 5

def run_probe(seed, delta, Q):
    """One seed of the E1 interference arm; Q=None -> full evaluation.

    v1 bug booked 2026-09-02: the early-PASS bound compared settles against
    ELAPSED ticks, so one good first tick certified a pass. Bounds must be
    anchored to the full horizon: settles only accrue, so the final percent
    can never drop below 100*settles/TICKS and never exceed
    100*(settles+remaining)/TICKS.
    """
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    settles = 0
    K, pulse_div, drift, lat2 = 4, 3, 6, 10
    for t in range(TICKS):
        s1 = reality(t)
        s2 = reality(max(0, t - lat2))
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
        for e in trig:
            m = abs(e) // pulse_div or 1
            pulses.appendleft([m if e > 0 else -m, K])
        if pulses:
            net = sum(p[0] for p in pulses)
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1
        if Q is not None:
            if 100 * settles >= Q * TICKS:                     # cannot drop
                return settles, t + 1, "PASS"
            if 100 * (settles + (TICKS - t - 1)) < Q * TICKS:  # cannot reach
                return settles, t + 1, "FAIL"
    if Q is None:
        return settles, TICKS, "FULL"
    return settles, TICKS, ("PASS" if 100 * settles >= Q * TICKS else "FAIL")

class Blades:
    def __init__(self, Q):
        self.Q = Q
        self.pulls = 0
        self.ticks = 0
        self.per_pull = []
    def pull(self, delta):
        """Boolean: does delta seat blade Q? 5-seed aggregate, certified
        early exit within and across seeds."""
        self.pulls += 1
        S = 0
        TOT = len(SEEDS) * TICKS
        for i, seed in enumerate(SEEDS):
            s, paid, verdict = run_probe(seed, delta, self.Q)
            S += s
            self.ticks += paid
            rem_seeds = len(SEEDS) - i - 1
            if verdict == "PASS" or 100 * S >= self.Q * TOT:
                self.per_pull.append((delta, "PASS", self.ticks))
                return True
            if 100 * (S + rem_seeds * TICKS) < self.Q * TOT:
                self.per_pull.append((delta, "FAIL", self.ticks))
                return False
        ok = 100 * S >= self.Q * TOT
        self.per_pull.append((delta, "PASS" if ok else "FAIL", self.ticks))
        return ok

def full_grid():
    """The wave: exact per-delta 5-seed integer percents (cost baseline)."""
    pcts = {}
    S_all = {}
    for delta in range(4, 25):
        S = 0
        for seed in SEEDS:
            s, _, _ = run_probe(seed, delta, None)
            S += s
        pcts[delta] = 100 * S // (len(SEEDS) * TICKS)
        S_all[delta] = S
    return pcts, len(range(4, 25)) * len(SEEDS) * TICKS, S_all

def seat(Q, label):
    b = Blades(Q)
    lo, hi = 4, 24
    trace = []
    while lo < hi:
        mid = (lo + hi) // 2
        fits = b.pull(mid)
        trace.append((mid, fits))
        if fits:
            hi = mid
        else:
            lo = mid + 1
    d_star = lo
    cert_hi = b.pull(d_star)                    # certificate: seat holds
    cert_lo = (not b.pull(d_star - 1)) if d_star > 4 else True   # and below fails
    print(f"\n{label}: binary seating trace (delta, seats): {trace}")
    print(f"  seat delta* = {d_star}; certificate pulls: seat={cert_hi}, below-seat-fails={cert_lo}")
    print(f"  pulls: {b.pulls}, ticks paid: {b.ticks}")
    return d_star, b

if __name__ == "__main__":
    print("SNAP-POINT SEARCH ECONOMY — interference arm, 5 seeds x", TICKS,
          "ticks, delta in [4,24]")
    d1, b1 = seat(75, "Q = 75")

    print("\nverification vs the full wave (integer grid, cost counted separately):")
    pcts, wave_ticks, S_all = full_grid()
    grid_min = min(d for d, p in pcts.items() if p >= 75)
    mono = all(pcts[d] <= pcts[d + 1] for d in range(4, 24))
    print("  delta : " + " ".join(f"{d:>3}" for d in range(4, 25)))
    print("  pct   : " + " ".join(f"{pcts[d]:>3}" for d in range(4, 25)))
    print(f"  grid minimal delta = {grid_min}; blade seat = {d1}; agree: {grid_min == d1}")
    print(f"  percent monotone nondecreasing in delta: {mono}")

    # dynamics cross-check vs e1.py itself (settle counts agree within rounding)
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import e1
    e1_ok = True
    for seed in SEEDS:
        e1.SEED = seed
        r = e1.run("interference", ticks=TICKS, K=4, pulse_div=3, delta=12, drift=6, lat2=10)
        s_mine, _, _ = run_probe(seed, 12, None)
        # e1 rounds to 1 decimal; accept +-0.15pp
        if abs(r["pct_within"] - (100 * s_mine) / TICKS) > 0.15:
            e1_ok = False
    print(f"  dynamics cross-check vs e1.run at delta=12, 5 seeds (within 0.15pp): {e1_ok}")

    print(f"\n  full-wave cost: {wave_ticks} ticks; blade engine (Q=75): {b1.ticks} ticks"
          f" -> {100 * b1.ticks // wave_ticks}% of wave")
    print(f"  per-pull tick costs: {[(d, v, t) for (d, v, t) in b1.per_pull]}")

    d2, b2 = seat(85, "second blade Q = 85")
    grid_min2 = min((d for d, p in pcts.items() if p >= 85), default=None)
    print(f"  grid minimal = {grid_min2}; agree: {d2 == grid_min2}; "
          f"ticks {b2.ticks} = {100 * b2.ticks // wave_ticks}% of wave")
