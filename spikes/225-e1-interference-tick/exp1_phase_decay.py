#!/usr/bin/env python3
"""PHASE_DECAY_COUPLING — Pulse decay modulated by cell refractory state.

Mechanism: cells in refractory state dissipate pulses faster.
Run: python3 exp1_phase_decay.py
"""
from collections import deque
import sys
sys.path.insert(0, ".")
import e1

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
    phase = t % PERIOD
    if phase < 96:
        return 400 + phase * 8 // 5
    elif phase < 144:
        return 400 + 96 * 8 // 5 - (phase - 96)
    else:
        return 400 + 96 * 8 // 5 - 48 - (phase - 144) * 8 // 5

def run_phase_coupling(ticks=4800, K=8, pulse_div=3, delta=6, drift=3, lat2=5):
    """Phase-decay: refractory cells dissipate pulses faster.

    In refractory phase: decay exponent is doubled (halving twice per tick instead of once).
    """
    rng = LCG(SEED)
    g = reality(0)
    pulses = deque()
    snap_events = 0
    ledger_mass = 0
    constructive = 0
    cancellations = 0
    chatter = 0
    last_snap = -10
    max_err = 0
    settles = 0
    phase_counter = 0
    phase_period = 12

    for t in range(ticks):
        phase_counter = (phase_counter + 1) % phase_period
        in_refractory = phase_counter < 4

        s1 = reality(t)
        s2 = reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift

        while pulses and pulses[-1][1] == 0:
            pulses.pop()

        e1_val = s1 - g
        e2_val = s2 - g
        trig = []
        if abs(e1_val) > delta:
            trig.append(e1_val)
        if abs(e2_val) > delta:
            trig.append(e2_val)
        max_trig = max((abs(e) for e in trig), default=0)

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
                        mag = mag - (mag // 2)
                        if in_refractory and abs(mag) > 1:
                            mag = mag - (mag // 2)
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

    return dict(snap_events=snap_events, ledger_mass=ledger_mass,
                constructive=constructive, cancellations=cancellations,
                chatter=chatter, max_err=max_err,
                pct_within=round(100 * settles / ticks, 1))

if __name__ == "__main__":
    print("stress: delta=12, drift=6, K=4, latency 10")
    r_baseline = e1.run("interference", delta=12, drift=6, K=4, lat2=10)
    r_phase = run_phase_coupling(delta=12, drift=6, K=4, lat2=10)

    print(f"baseline interference:")
    print(f"  events={r_baseline['snap_events']} debt={r_baseline['ledger_mass']} "
          f"cancel={r_baseline['cancellations']} %within={r_baseline['pct_within']}")
    print(f"phase_decay_coupling:")
    print(f"  events={r_phase['snap_events']} debt={r_phase['ledger_mass']} "
          f"cancel={r_phase['cancellations']} %within={r_phase['pct_within']}")
