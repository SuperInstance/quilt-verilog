#!/usr/bin/env python3
"""LEDGER_MODE_SELECTION — Mode switching based on running ledger statistics.

Mechanism: use sliding window of ledger stats (cancellations, correction rate)
to decide impulse vs interference mode tick-by-tick.

Run: python3 exp2_adaptive_mode.py
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

def run_adaptive_mode(ticks=4800, K=4, pulse_div=3, delta=12, drift=6, lat2=10):
    """Adaptive: select mode each tick based on recent ledger stats."""
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
    mode_switches = 0
    current_mode = "interference"
    window_size = 50
    cancel_window = deque(maxlen=window_size)
    event_window = deque(maxlen=window_size)

    for t in range(ticks):
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

        new_mode = current_mode
        if t >= window_size:
            cancel_count = sum(cancel_window)
            pulses_alive = max(len([p for p in pulses if p[1] > 0]), 1)
            cancel_rate = cancel_count / pulses_alive if pulses_alive > 0 else 0
            event_rate = sum(event_window) / window_size if window_size > 0 else 0

            if cancel_rate > 0.15 and event_rate < 50:
                new_mode = "interference"
            elif cancel_rate <= 0.1 or event_rate >= 50:
                new_mode = "impulse"

            if new_mode != current_mode:
                mode_switches += 1
                current_mode = new_mode

        if current_mode == "sequential":
            if trig:
                g += trig[0]
                snap_events += 1
                ledger_mass += abs(trig[0])
                event_window.append(1)
                cancel_window.append(0)
                if t - last_snap == 1:
                    chatter += 1
                last_snap = t
                if max(abs(s1 - g), abs(s2 - g)) > max_trig:
                    constructive += 1
            else:
                event_window.append(0)
                cancel_window.append(0)
        else:
            for e in trig:
                m = abs(e) // pulse_div or 1
                pulses.appendleft([m if e > 0 else -m, K])
                snap_events += 1
                ledger_mass += abs(e)
            event_window.append(len(trig))

            if pulses:
                net = sum(p[0] for p in pulses)
                cancel_this_tick = 1 if (net == 0 and len(pulses) >= 2) else 0
                if cancel_this_tick:
                    cancellations += 1
                cancel_window.append(cancel_this_tick)

                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
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
            else:
                cancel_window.append(0)

        err = max(abs(s1 - g), abs(s2 - g))
        max_err = max(max_err, err)
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1

    return dict(snap_events=snap_events, ledger_mass=ledger_mass,
                constructive=constructive, cancellations=cancellations,
                chatter=chatter, max_err=max_err,
                pct_within=round(100 * settles / ticks, 1),
                mode_switches=mode_switches)

if __name__ == "__main__":
    print("stress: delta=12, drift=6, K=4, latency 10")
    print()
    r_seq = e1.run("sequential", delta=12, drift=6, K=4, lat2=10)
    r_int = e1.run("interference", delta=12, drift=6, K=4, lat2=10)
    r_adap = run_adaptive_mode(delta=12, drift=6, K=4, lat2=10)

    print(f"sequential:    events={r_seq['snap_events']:4d} debt={r_seq['ledger_mass']:6d} %within={r_seq['pct_within']:5.1f}")
    print(f"interference:  events={r_int['snap_events']:4d} debt={r_int['ledger_mass']:6d} %within={r_int['pct_within']:5.1f}")
    print(f"adaptive:      events={r_adap['snap_events']:4d} debt={r_adap['ledger_mass']:6d} %within={r_adap['pct_within']:5.1f} (switches={r_adap['mode_switches']})")
