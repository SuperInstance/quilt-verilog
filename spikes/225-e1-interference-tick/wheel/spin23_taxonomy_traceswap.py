#!/usr/bin/env python3
"""SPIN-23 — TAXONOMY TRACE-SWAP (pre-registration in SPIN-23-taxonomy-traceswap.md).

Rerun SPIN-17's four tax-class anchors (T1 amplitude gate, T2 duty,
T3 phase, T4 K=2 spike; all @P=16, 5<->30, K=2 unless noted) on three
non-ramp realities from SPIN-21's trace generator (VERBATIM trace code):
r2_triangle, r4_sawtooth, r3_plateau.

Instrument: dyn_run, spin-21's clone (reality_fn + k as parameters).
Integer-only in-loop; floats only at print. Panel seeds {1,7,42};
canary anchors use the 5-seed set to reproduce published numbers.
Decision rule (pre-registered): see .md — survives iff direction holds
on >=2/3 traces (ties within 3pp = hold); trace-coupled iff flips on
>=2/3; else indeterminate.
"""
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm, LCG  # noqa: E402
from spin21_reality_variation import r2_triangle, r4_sawtooth, r3_plateau  # noqa: E402
import exp_glm1

SEEDS = (1, 7, 42)                # panel seeds (pre-registered)
SEEDS5 = (1, 7, 42, 1999, 20260902)  # canary anchor set (published)
DELTA, DRIFT, PD, N, TICKS = 12, 6, 3, 6, 4800
KS = (1, 2, 4, 8)
T0 = time.time()

TRACES = (("triangle", r2_triangle), ("sawtooth", r4_sawtooth),
          ("plateau", r3_plateau))
R0 = exp_glm1.reality


def _mk(fn):
    cache = {}
    def g(t):
        if t not in cache:
            cache[t] = fn(t)
        return cache[t]
    return g


# instrument: verbatim clone of run_fabric interference arm (spin-21)
def dyn_run(lats_fn, reality_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA,
            drift=DRIFT, seed=20260902):
    rng = LCG(seed)
    g = reality_fn(0)
    pulses = deque()
    resid = []
    for t in range(ticks):
        lats = lats_fn(t)
        n = len(lats)
        reads = [reality_fn(max(0, t - lats[i])) for i in range(n)]
        s_true = reality_fn(t)
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > delta]
        for i, e in trig:
            m = abs(e) // pd or 1
            pulses.appendleft([m if e > 0 else -m, k])
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
        resid.append(abs(s_true - g))
    return resid


def pct(w, delta=DELTA):
    return within_pm(w, delta) / 10.0


def mean(v):
    return sum(v) / len(v)


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


def square_schedule(P, lo, hi, duty100=50, ticks=TICKS, invert=False):
    """Spin-17 scheduler, VERBATIM (lo-phase first; invert swaps order)."""
    hi_ticks = P * duty100 // 100
    sched = []
    for t in range(ticks):
        in_hi = (t % P) >= P - hi_ticks
        if invert:
            in_hi = (t % P) < hi_ticks
        sched.append(hi if in_hi else lo)
    return sched


def sched_fn(sched):
    return lambda t, S=sched: ladder(S[t])


def static_fn(s):
    return lambda t, L=ladder(s): L


_pct_cache = {}


def osc(sched, fn, k, sd, tag=""):
    key = ("sched", hash(tuple(sched)), tag, k, sd)
    if key not in _pct_cache:
        _pct_cache[key] = pct(dyn_run(sched_fn(sched), fn, k=k, seed=sd))
    return _pct_cache[key]


def spct(s, fn, k, sd, tag=""):
    key = ("static", s, tag, k, sd)
    if key not in _pct_cache:
        _pct_cache[key] = pct(dyn_run(static_fn(s), fn, k=k, seed=sd))
    return _pct_cache[key]


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY 1: spread=0 byte-identity (scheduler path vs static-5,"
          " per trace, K{1,2,4,8} x seeds{1,7,42}) ==")
    c1 = True
    for name, fn0 in TRACES + (("R0", R0),):
        fn = _mk(fn0)
        sched = square_schedule(16, 5, 5, 50)
        for k in KS:
            for sd in SEEDS:
                a = dyn_run(sched_fn(sched), fn, k=k, seed=sd)
                b = dyn_run(static_fn(5), fn, k=k, seed=sd)
                if a != b:
                    c1 = False
                    print(f"  MISMATCH {name} K={k} seed={sd}")
    print(f"  {'PASS' if c1 else 'FAIL'}: 36 configs byte-identical")

    print("\n== CANARY 2: R0 anchors exact (5-seed means) ==")
    c2 = True
    for name, lats, k, want in (("ladder@15 K=1", ladder(15), 1, 71.5),
                                ("zero@15   K=1", [0] * N, 1, 77.3)):
        m = mean([pct(dyn_run(static_fn(0 if "zero" in name else 15),
                              R0, k=k, seed=sd)) for sd in SEEDS5])
        good = abs(m - want) <= 0.2
        c2 &= good
        print(f"  {name}: {m:.1f} (want {want}) -> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY 3: SPIN-21 K=2 floor >= 7.5pp reproduces on every"
          " rerun trace (zero grammar, 5-seed) ==")
    c3 = True
    for name, fn0 in TRACES:
        fn = _mk(fn0)
        row = {}
        for k in KS:
            row[k] = mean([pct(dyn_run(static_fn(0), fn, k=k, seed=sd))
                           for sd in SEEDS5])
        trough = min(row[1], row[4]) - row[2]
        good = trough >= 7.5
        c3 &= good
        print(f"  {name:<9} K-sweep {row[1]:.1f}/{row[2]:.1f}/{row[4]:.1f}/"
              f"{row[8]:.1f}  trough={trough:.1f}pp -> "
              f"{'PASS' if good else 'FAIL'}")
    ok = c1 and c2 and c3
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- panel
def tax(sched, fn, k, lo, hi, duty100=50, tag=""):
    """TWmean tax (Spin-17 convention): twm - osc, per panel seeds."""
    f = duty100 / 100.0
    oscs = [osc(sched, fn, k, sd, tag) for sd in SEEDS]
    twm = mean([spct(lo, fn, k, sd, tag) * (1 - f) + spct(hi, fn, k, sd, tag) * f
                for sd in SEEDS])
    return twm - mean(oscs), mean(oscs), twm


def step(a, b):
    """compare anchor-ordering step a>b: +1 hold, -1 flip, 0 tie(<=3pp)"""
    if a - b > 3.0:
        return 1
    if b - a > 3.0:
        return -1
    return 0


def main():
    print("SPIN-23 TAXONOMY TRACE-SWAP —", time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N}, seeds(panel)={SEEDS}, ticks={TICKS}, "
          f"delta={DELTA}, drift={DRIFT}, pd={PD}, P=16 anchors")
    if not canaries():
        sys.exit(1)

    print("\n== PANEL: tax-class anchors per trace (5-seed-style TWmean tax,"
          " panel seeds {1,7,42}) ==")
    R = {}  # trace -> dict of measurements
    for name, fn0 in TRACES:
        fn = _mk(fn0)
        d = {}
        # T1 amplitude: pairs at P=16 K=2, tax vs TWmean
        for lo, hi in ((5, 30), (10, 25), (15, 20)):
            t, o, w = tax(square_schedule(16, lo, hi, 50), fn, 2, lo, hi, tag=name)
            d[f"T1_tax_s{hi - lo}"] = t
            d[f"T1_osc_s{hi - lo}"] = o
        # T2 duty: 5<->30, K=2, P=16, duty in {25,50,75}
        for duty in (25, 50, 75):
            t, o, w = tax(square_schedule(16, 5, 30, duty), fn, 2, 5, 30,
                          duty, tag=name)
            d[f"T2_tax_d{duty}"] = t
        # T3 phase: lo-first vs hi-first, K=2, P=16, duty 50
        s1 = square_schedule(16, 5, 30, 50)
        s2 = square_schedule(16, 5, 30, 50, invert=True)
        t1, o1, _ = tax(s1, fn, 2, 5, 30, tag=name)
        t2, o2, _ = tax(s2, fn, 2, 5, 30, tag=name)
        d["T3_tax_lofirst"] = t1
        d["T3_tax_hifirst"] = t2
        d["T3_dphi_osc"] = o2 - o1
        # T4 K-grid: 5<->30 P=16 duty50, K in {1,2,4,8}
        for k in KS:
            t, o, _ = tax(square_schedule(16, 5, 30, 50), fn, k, 5, 30, tag=name)
            d[f"T4_tax_K{k}"] = t
        R[name] = d
        print(f"\n-- {name} --")
        for k in sorted(d):
            print(f"  {k:<16} {d[k]:7.1f}")

    # ------------------------------------------------ verdicts
    print("\n== VERDICTS (decision rule pre-registered in .md) ==")
    print(f"{'class':<38}" + "".join(f"{t:>10}" for t, _ in TRACES)
          + "   verdict")

    def verdict(holds, flips):
        if holds >= 2:
            return "SURVIVES"
        if flips >= 2:
            return "TRACE-COUPLED"
        return "INDETERMINATE"

    rows = []
    for name, d in R.items():
        # T1: two steps 25>15>5; direction holds if steps are +1 or 0
        s1 = step(d["T1_tax_s25"], d["T1_tax_s15"])
        s2 = step(d["T1_tax_s15"], d["T1_tax_s5"])
        gate = d["T1_tax_s5"] < 3.0
        d["T1_hold"] = (s1 >= 0 and s2 >= 0 and gate)
        d["T1_flip"] = (s1 == -1 or s2 == -1)
        d["T1_steps"] = f"{s1:+d},{s2:+d},gate={'Y' if gate else 'N'}"
        # T2: two steps 25>50>75
        s1 = step(d["T2_tax_d25"], d["T2_tax_d50"])
        s2 = step(d["T2_tax_d50"], d["T2_tax_d75"])
        d["T2_hold"] = (s1 >= 0 and s2 >= 0)
        d["T2_flip"] = (s1 == -1 or s2 == -1)
        d["T2_steps"] = f"{s1:+d},{s2:+d}"
        # T3: hi-first tax >= lo-first (tie<=3pp holds)
        dd = d["T3_tax_hifirst"] - d["T3_tax_lofirst"]
        d["T3_hold"] = dd >= -3.0
        d["T3_flip"] = dd < -3.0
        d["T3_steps"] = f"dphi_tax={dd:+.1f}"
        # T4: K2 exceeds every other K by >=3pp
        others = max(d[f"T4_tax_K{k}"] for k in KS if k != 2)
        dd = d["T4_tax_K2"] - others
        d["T4_hold"] = dd >= 3.0
        d["T4_flip"] = dd <= -3.0
        d["T4_steps"] = f"K2-max_other={dd:+.1f}"

    for cls, desc in (("T1", "amplitude gate (25>15>5, gate<3pp)"),
                      ("T2", "duty/guerrilla (25>50>75)"),
                      ("T3", "phase (hi-first >= lo-first)"),
                      ("T4", "K=2 spike (K2 > others by 3pp)")):
        cells = []
        for name, d in R.items():
            if d[cls + "_hold"]:
                cells.append("hold")
            elif d[cls + "_flip"]:
                cells.append("FLIP")
            else:
                cells.append("~")
        h = sum(1 for c in cells if c == "hold")
        f = sum(1 for c in cells if c == "FLIP")
        rows.append((cls, cells, verdict(h, f)))
        print(f"{cls + ': ' + desc:<38}"
              + "".join(f"{c:>10}" for c in cells) + f"   {verdict(h, f)}")

    print("\n-- detail: steps per trace --")
    for name, d in R.items():
        print(f"  {name:<10} T1[{d['T1_steps']}] T2[{d['T2_steps']}] "
              f"T3[{d['T3_steps']}] T4[{d['T4_steps']}]")
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
