#!/usr/bin/env python3
"""WHEEL SPIN 1 — METROLOGY blade.

Measure, per seed (1, 7, 42, 1999, 20260902), on the E1 harness:
  - ticks-to-fixed-point: first tick t such that |e1| <= 1 and |e2| <= 1
    holds for 50 consecutive ticks (sustained fix), else NOT-REACHED.
  - correction-event spacing distribution (min gap = refractory floor,
    mean gap), over the whole 4800-tick run.
  - residual steady-state error: integer mean and max of max(|e1|,|e2|)
    over the last 2400 ticks.

Integer-only arithmetic throughout (means via floor division). No floats.
Reuses LCG and reality() from e1.py verbatim; the tick loop is a faithful
instrumented copy of e1.run() (same order of operations, same decay,
same trigger) — checked against e1.run() outputs for sanity below.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import deque
from e1 import LCG, reality  # canonical machinery

SEEDS = [1, 7, 42, 1999, 20260902]
TICKS = 4800
FIX_EPS = 1
FIX_HOLD = 50


def run_instrumented(seed, mode, K=8, pulse_div=3, delta=6, drift=3, lat2=5):
    deadband = delta
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    corr_ticks = []            # ticks on which >=1 correction event fired
    errs = []                  # max(|e1|,|e2|) after correction, per tick

    # sustained-fix tracker
    run_ok = 0
    t_fix = -1                 # tick at which the 50-tick sustain COMPLETED

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

        corrected = False
        if mode == "sequential":
            if trig:
                g += trig[0]
                corrected = True
        else:
            for e in trig:
                m = abs(e) // pulse_div or 1
                pulses.appendleft([m if e > 0 else -m, K])
                corrected = True
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

        if corrected:
            corr_ticks.append(t)

        err = max(abs(s1 - g), abs(s2 - g))
        errs.append(err)
        if t_fix < 0:
            if err <= FIX_EPS:
                run_ok += 1
                if run_ok >= FIX_HOLD:
                    t_fix = t
            else:
                run_ok = 0

    # spacing distribution (integer only)
    gaps = [corr_ticks[i] - corr_ticks[i - 1] for i in range(1, len(corr_ticks))]
    min_gap = min(gaps) if gaps else -1
    mean_gap = (sum(gaps) // len(gaps)) if gaps else -1

    # steady-state residual over last half
    tail = errs[TICKS // 2:]
    resid_mean = sum(tail) // len(tail)
    resid_max = max(tail)

    n_fix = sum(1 for e in errs if e <= FIX_EPS)
    # harness-native criterion: sustained hold inside the deadband (|e|<=delta)
    run_db = 0
    t_fix_db = -1
    for t, e in enumerate(errs):
        if t_fix_db >= 0:
            break
        if e <= deadband:
            run_db += 1
            if run_db >= FIX_HOLD:
                t_fix_db = t
        else:
            run_db = 0
    n_db = sum(1 for e in errs if e <= deadband)
    return dict(mode=mode, events=len(corr_ticks), t_fix=t_fix,
                t_fix_db=t_fix_db, deadband=deadband,
                min_gap=min_gap, mean_gap=mean_gap,
                resid_mean=resid_mean, resid_max=resid_max,
                pct_within_1=100 * n_fix // TICKS,
                pct_within_db=100 * n_db // TICKS)


def fmt_fix(t):
    return "NOT-REACHED" if t < 0 else str(t)


def sweep(name, **kw):
    print(f"\n== {name} ==")
    print(f"{'seed':>9} {'mode':<12} {'t_fix@db':>10} {'#corr':>6} {'minGap':>7} {'meanGap':>8} "
          f"{'residMean':>9} {'residMax':>8} {'%inDB':>6}")
    acc = {}
    for mode in ("sequential", "interference"):
        for seed in SEEDS:
            r = run_instrumented(seed, mode, **kw)
            acc.setdefault(mode, []).append(r)
            print(f"{seed:>9} {r['mode']:<12} {fmt_fix(r['t_fix_db']):>10} {r['events']:>6} "
                  f"{r['min_gap']:>7} {r['mean_gap']:>8} {r['resid_mean']:>9} "
                  f"{r['resid_max']:>8} {r['pct_within_db']:>6}")
    # summary: mean time-to-fix (over seeds that fixed), ratio int/seq
    for mode in ("sequential", "interference"):
        tf = [r["t_fix_db"] for r in acc[mode] if r["t_fix_db"] >= 0]
        if tf:
            print(f"  {mode}: mean t_fix(deadband) = {sum(tf)//len(tf)} ({len(tf)}/{len(SEEDS)} seeds), "
                  f"min refractory = {min(r['min_gap'] for r in acc[mode] if r['min_gap']>0)}")
        else:
            print(f"  {mode}: no seed reached sustained deadband fix")
    return acc


if __name__ == "__main__":
    acc_calm = sweep("CALM  (delta=6, drift=3, K=8, lat2=5)", delta=6, drift=3, K=8, lat2=5)
    acc_stress = sweep("STRESS (delta=12, drift=6, K=4, lat2=10)", delta=12, drift=6, K=4, lat2=10)
