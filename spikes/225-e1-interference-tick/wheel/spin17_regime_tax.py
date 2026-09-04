#!/usr/bin/env python3
"""SPIN 17, REGIME SPOKE follow-up: OSCILLATION TAX SPECTRUM.

Pre-registered hypothesis: the regime-switching tax (SPIN-16-regime, K=2
5<->30 square wave: 27.0pp @ P=16, 11.7 @ P=64, 1.7 @ P=256 vs TWmean)
decays HYPERBOLICALLY, tax(P) -> 0 as 1/P, and its collapse timescale
equals pulse settling (K x decay), not the reality period. A non-hyperbolic
decay = a second, slower memory channel (falsification direction).

EXP1  Fine period spectrum: P in {8..1024}, K in {1,2,4,8}, 5<->30 square.
      Fit tax(P) vs 1/P and vs exp(-P/tau); report which fits, tau per K.
EXP2  Duty cycle: asymmetric squares at P=16 and P=64, duty in {25,50,75}%
      (spread 30 occupies duty% of the period, 5 the rest) — does the tax
      track time-in-worse-regime or transition count?
EXP3  Amplitude: 5<->30, 10<->25, 15<->20 at P=16, K=2 — linear in spread
      amplitude or gated?

Controls everywhere: matched-mean static + TWmean (SPIN-16 scar #2).
Instrument: dyn_run — verbatim clone of exp_glm1.run_fabric interference
arm with per-tick lats_fn, k as a parameter (scar #1: no global K refs).
Integer-only inside every loop; floats only at print/fit time.
Online scheduling is single-pass simulation only (no chunked re-sim).
"""
import math
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
DRIFT = 6
PD = 3
N = 6
TICKS = 4800
KS = (1, 2, 4, 8)
PERIODS = (8, 16, 32, 48, 64, 96, 128, 192, 256, 384, 512, 1024)
T0 = time.time()


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


# ------------------------------------------------- instrument (verbatim clone)
def dyn_run(lats_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA, drift=DRIFT,
            seed=20260902):
    """run_fabric interference arm, lats per-tick, k as a PARAMETER.
    Verbatim physics (canary C1 proves byte-identity)."""
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    last = -10
    resid = []
    for t in range(ticks):
        lats = lats_fn(t)
        n = len(lats)
        reads = [reality(max(0, t - lats[i])) for i in range(n)]
        s_true = reality(t)
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
        if trig:
            last = t
        resid.append(abs(s_true - g))
    return resid


def pct(window, delta=DELTA):
    return within_pm(window, delta) / 10.0


def mean(v):
    return sum(v) / len(v)


# --------------------------------------------------------- schedulers
def square_schedule(P, lo, hi, duty100=50, ticks=TICKS, invert=False):
    """Phase layout per period P (SPIN-16 convention: lo-phase FIRST).
    duty100 = percent of the period spent in `hi`. Integer tick counts.
    invert=True swaps the phase order (phase-inversion probe: identical
    duty and transition count, different alignment with reality period
    240)."""
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


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: wiring byte-identity dyn_run vs run_fabric ==")
    nchk = 0
    for s, lats in (("zero@0", [0] * N), ("ladder@15", ladder(15)),
                    ("ladder@30", ladder(30))):
        for k in (1, 4):
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=sd)["resid"]
                b = dyn_run(lambda t, L=lats: L, k=k, seed=sd)
                nchk += 1
                if a != b:
                    ok = False
                    print(f"  MISMATCH {s} K={k} seed={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} configs byte-identical")

    print("\n== CANARY b: anchor replays (5-seed means) ==")
    for name, lats, k, want_tp, want_ev, want_debt in (
            ("zero@15   K=1", [0] * N, 1, 77.3, None, 187834),
            ("ladder@15 K=1", ladder(15), 1, 71.5, 5792, 106378)):
        rs = [dyn_run(static_fn(0) if "zero" in name else static_fn(15),
                      k=k, seed=sd) for sd in SEEDS]
        tp = mean([pct(r) for r in rs])
        rf = [run_fabric("interference", TICKS, lats, K=k, pd=PD,
                         delta=DELTA, drift=DRIFT, seed=sd) for sd in SEEDS]
        ev = mean([r["events"] for r in rf])
        dbt = mean([r["mass"] for r in rf])
        good = (abs(tp - want_tp) <= 0.2
                and (want_ev is None or abs(ev - want_ev) <= 2)
                and abs(dbt - want_debt) <= 300)
        ok &= good
        print(f"  {name}: {tp:.1f}% (want {want_tp})  ev {ev:.0f} "
              f"(want {want_ev})  debt {dbt:.0f} (want {want_debt})  "
              f"-> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY c: no-shift identity — hold-5 via scheduler path ==")
    c3 = True
    for k in KS:
        sched = square_schedule(16, 5, 5, duty100=50)  # both phases = 5
        for sd in SEEDS:
            a = dyn_run(sched_fn(sched), k=k, seed=sd)
            b = dyn_run(static_fn(5), k=k, seed=sd)
            if a != b:
                c3 = False
    print(f"  sched-path hold-5 == static-5, K in {KS}, 5 seeds: "
          f"{'PASS' if c3 else 'FAIL'}")
    return ok and c3


# --------------------------------------------------------------- EXP 1
_static_cache = {}


def static_pct(s, k):
    key = (s, k)
    if key not in _static_cache:
        _static_cache[key] = [pct(dyn_run(static_fn(s), k=k, seed=sd))
                              for sd in SEEDS]
    return _static_cache[key]


def exp1_spectrum():
    print("\n== EXP 1: PERIOD SPECTRUM — 5<->30 square, duty 50% ==")
    results = {}   # (P,k) -> dict(osc list, tax list, twm, st17)
    for k in KS:
        st5 = static_pct(5, k)
        st30 = static_pct(30, k)
        st17 = static_pct(17, k)
        twm = mean([(a + b) / 2.0 for a, b in zip(st5, st30)])
        print(f"\n-- K={k}: static5={mean(st5):.1f} static30={mean(st30):.1f}"
              f" TWmean={twm:.1f} static17={mean(st17):.1f} --")
        print(f"{'P':>5}{'osc%':>7}{'tax pp':>8}"
              + "".join(f"{'s' + str(s):>9}" for s in SEEDS))
        for P in PERIODS:
            sched = square_schedule(P, 5, 30, 50)
            oscs = [pct(dyn_run(sched_fn(sched), k=k, seed=sd))
                    for sd in SEEDS]
            taxes = [twm - o for o in oscs]
            results[(P, k)] = dict(osc=oscs, tax=taxes, twm=twm,
                                   st17=mean(st17))
            print(f"{P:>5}{mean(oscs):>7.1f}{mean(taxes):>8.1f}"
                  + "".join(f"{t:>9.1f}" for t in taxes))
    print("\n-- EXP 1b: PHASE-INVERSION probe (swap lo/hi phase order; same "
          "duty, same transitions) --")
    print(f"{'P':>5}{'K':>3}{'lo-first%':>11}{'tax':>7}{'hi-first%':>11}"
          f"{'tax':>7}{'dphi':>7}")
    for k in KS:
        for P in (16, 64):
            s1 = square_schedule(P, 5, 30, 50)
            s2 = square_schedule(P, 5, 30, 50, invert=True)
            o1 = mean([pct(dyn_run(sched_fn(s1), k=k, seed=sd))
                       for sd in SEEDS])
            o2 = mean([pct(dyn_run(sched_fn(s2), k=k, seed=sd))
                       for sd in SEEDS])
            twm = results[(P, k)]["twm"]
            print(f"{P:>5}{k:>3}{o1:>11.1f}{twm - o1:>7.1f}{o2:>11.1f}"
                  f"{twm - o2:>7.1f}{o2 - o1:>7.1f}")

    print("\n-- FITS: tax(P) vs 1/P (hyperbolic) and exp(-P/tau) --")
    print(f"{'K':>3}{'tax_max':>9}{'hyper r2':>10}{'hyper sl':>9}"
          f"{'exp r2':>8}{'tau':>7}{'expA':>7}  note")
    fits = {}
    for k in KS:
        xs = [float(P) for P in PERIODS]
        ys = [mean(results[(P, k)]["tax"]) for P in PERIODS]
        # hyperbolic fit: tax = a/P + b (least squares)
        n = len(xs)
        mx, my = mean(xs), mean(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        # regression on x=1/P
        us = [1.0 / x for x in xs]
        mu = mean(us)
        suu = sum((u - mu) ** 2 for u in us)
        suy = sum((u - mu) * (y - my) for u, y in zip(us, ys))
        a = suy / suu
        b = my - a * mu
        pred_h = [a * u + b for u in us]
        ss_res = sum((y - p) ** 2 for y, p in zip(ys, pred_h))
        ss_tot = sum((y - my) ** 2 for y in ys)
        r2h = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        # exp fit on log(tax) over positive taxes
        pts = [(x, y) for x, y in zip(xs, ys) if y > 0.3]
        if len(pts) >= 4:
            lx = [p[0] for p in pts]
            ly = [math.log(p[1]) for p in pts]
            mlx, mly = mean(lx), mean(ly)
            sxxe = sum((v - mlx) ** 2 for v in lx)
            sxye = sum((x - mlx) * (y - mly) for x, y in zip(lx, ly))
            lam = sxye / sxxe          # = -1/tau
            tau = -1.0 / lam if lam < 0 else float("inf")
            lnA = mly - lam * mlx
            pred_e = [math.exp(lam * v + lnA) for v in lx]
            ly_hat = [lam * v + lnA for v in lx]
            ss_re = sum((q - h) ** 2 for q, h in zip(ly, ly_hat))
            ss_te = sum((q - mly) ** 2 for q in ly)
            r2e = 1 - ss_re / ss_te if ss_te > 0 else float("nan")
        else:
            tau, r2e, lnA = float("nan"), float("nan"), float("nan")
        fits[k] = dict(a=a, b=b, r2h=r2h, tau=tau, r2e=r2e)
        note = ("hyperbolic" if r2h > r2e else "exponential") \
            if not (r2h != r2h or r2e != r2e) else "n/a"
        print(f"{k:>3}{max(ys):>9.1f}{r2h:>10.3f}{a:>9.2f}"
              f"{r2e:>8.3f}{tau:>7.1f}{math.exp(lnA) if lnA == lnA else float('nan'):>7.2f}"
              f"  {note}")
        # residual diagnostics for the hyperbola at small P
    return results, fits


# --------------------------------------------------------------- EXP 2
def exp2_duty():
    print("\n== EXP 2: DUTY CYCLE — asymmetric squares, 30 for duty% of P, "
          "5 otherwise ==")
    print("  predictions: time-weighted => tax(duty) ~ duty*(1-duty) "
          "shape w/ peak at 50%; transition-count => tax(25,75) ~ half "
          "of tax(50) at fixed P (fewer transitions per period).")
    print(f"{'P':>4}{'K':>3}{'duty':>6}{'osc%':>7}{'TWm%':>7}{'tax pp':>8}"
          f"{'mmS%':>7}{'vs mmS':>8}{'trans':>7}")
    out = {}
    for k in (1, 2):
        st5, st30 = static_pct(5, k), static_pct(30, k)
        for P in (16, 64):
            for duty in (25, 50, 75):
                sched = square_schedule(P, 5, 30, duty)
                oscs = [pct(dyn_run(sched_fn(sched), k=k, seed=sd))
                        for sd in SEEDS]
                f = duty / 100.0
                twm = mean([a * (1 - f) + b * f
                            for a, b in zip(st5, st30)])
                mm = ladder(round(5 * (1 - f) + 30 * f))
                mms = mean([pct(dyn_run(lambda t, L=mm: L, k=k, seed=sd))
                            for sd in SEEDS])
                tax = twm - mean(oscs)
                hi_ticks = P * duty // 100
                trans = 2 * (TICKS // P) - (1 if TICKS % P == 0 else 0)
                out[(P, k, duty)] = (mean(oscs), twm, tax, mms)
                print(f"{P:>4}{k:>3}{duty:>6}{mean(oscs):>7.1f}{twm:>7.1f}"
                      f"{tax:>8.1f}{mms:>7.1f}{mean(oscs) - mms:>8.1f}"
                      f"{trans:>7}")
    return out


# --------------------------------------------------------------- EXP 3
def exp3_amplitude():
    print("\n== EXP 3: AMPLITUDE — 5<->30, 10<->25, 15<->20 @ P=16, K=2 "
          "(+ K=1 column) ==")
    print(f"{'pair':>8}{'K':>3}{'spread':>7}{'osc%':>7}{'TWm%':>7}"
          f"{'mmS%':>7}{'tax':>7}{'vs mmS':>8}")
    out = {}
    for lo, hi in ((5, 30), (10, 25), (15, 20)):
        for k in (2, 1):
            slo = static_pct(lo, k)
            shi = static_pct(hi, k)
            twm = mean([(a + b) / 2.0 for a, b in zip(slo, shi)])
            mms = round((lo + hi) / 2.0)
            mm = mean(static_pct(mms, k))
            sched = square_schedule(16, lo, hi, 50)
            oscs = [pct(dyn_run(sched_fn(sched), k=k, seed=sd))
                    for sd in SEEDS]
            tax = twm - mean(oscs)
            out[(lo, hi, k)] = (mean(oscs), twm, tax, mm)
            print(f"{f'{lo}-{hi}':>8}{k:>3}{hi - lo:>7}{mean(oscs):>7.1f}"
                  f"{twm:>7.1f}{mm:>7.1f}{tax:>7.1f}{mean(oscs) - mm:>8.1f}")
    return out


def main():
    print("SPIN-17 REGIME TAX SPECTRUM —", os.popen("date -u").read().strip())
    print(f"config: N={N} ladder, K={KS}, seeds={SEEDS}, ticks={TICKS}, "
          f"delta={DELTA}, drift={DRIFT}, pd={PD}")
    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    if not ok:
        sys.exit(1)
    results, fits = exp1_spectrum()
    exp2_duty()
    exp3_amplitude()
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
