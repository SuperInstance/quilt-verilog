#!/usr/bin/env python3
"""SPIN 29 — METROLOGY (C=f(delta) spoke): is the knee constant 2*delta?

HYPOTHESIS (pre-registered in this header BEFORE any panel run; filed by
SPIN-27's next-spoke proposal):
  SPIN-27 measured C = s*·slope ~= 28.6 +- 0.7 at delta=12 (slope 1.6,
  K=1), decisively NOT 2*delta=24. This spin tests whether C is set by
  delta at all:
      C(delta) = s*(delta)·slope ~= alpha · 2·delta     with alpha const
  Predicted point estimates (alpha = 28.6/24 ~= 1.192):
      delta= 8 -> C ~= 19.1, s* ~= 11.9
      delta=10 -> C ~= 23.8, s* ~= 14.9
      delta=12 -> C ~= 28.6, s* ~= 17.9   (SPIN-27 continuity anchor)
      delta=16 -> C ~= 38.2, s* ~= 23.9
      delta=20 -> C ~= 47.7, s* ~= 29.8
  FALSIFY if C(delta) is not linear in delta (curvature beyond noise), or
  if alpha = C/(2*delta) varies > 15% across the delta grid.
  SECONDARY: fit C(delta) to {linear-through-origin C=b*delta, affine
  C=a+b*delta, 2delta+const C=2*delta+c}; report winner + constants.

DESIGN
  delta in {8, 10, 12, 16, 20}; slope pinned at 1.6 (integer rational
  realization A=200, T_up=125 — spec slope exactly 200/125 = 1.600, the
  SPIN-21 scar: slope from SPEC, never sampled). N=6 ladder grammar.
  Spread sweep 8..40 step 2 (17 points). NOTE (pre-registered deviation
  from the task brief's 8..30): at delta=20 the prediction puts s*~29.8;
  an 8..30 sweep would clip the knee exactly as s0.8 clipped SPIN-27, so
  the sweep is widened to 40 BEFORE any run, symmetric across all deltas.
  K=1 primary everywhere; K=2 only at delta=12 (continuity column).
  Statistic: 50%-residency crossing by linear interpolation (SPIN-21/27).
  Seeds 1/7/42/1999/20260902, 5-seed means, 4800 ticks, drift=6, pd=3.

CANARIES (mandatory gate, all must pass before any panel counts):
  a. wiring byte-identity >= 8 configs dyn_run(R0) vs exp_glm1.run_fabric
     (delta=12 leg).
  b. anchors at delta=12: ladder15 K=1 pct=71.5 / ev 5792 / debt 106378;
     zero K=1 pct=77.3 / debt 187834 (5-seed means).
  c. delta=12 slope-1.6 arm reproduces SPIN-27: s* ~= 17.9
     (measured 17.6; tol 1.0; product ~28.6 tol 1.5).
  d. determinism: dual runs byte-identical across all deltas.

Integer-only inside every loop; floats only at print/stat time.
Instrument: dyn_run — verbatim clone of spin27_metrology.py's clone of
spin21's canary-proven inline single-pass run_fabric interference arm
(reality_fn/k/delta as parameters). python3 -u direct redirect; no pipes.
"""
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import exp_glm1
from exp_glm1 import run_fabric, within_pm, LCG

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA0 = 12                              # canary/anchor delta
DRIFT = 6
PD = 3
N = 6
TICKS = 4800
DELTAS = (8, 10, 12, 16, 20)
SPREADS = tuple(range(8, 41, 2))          # 8,10,...,40 (17 points)
BAND_LO = 353
AMP = 200                                 # band [353,553], R0's true band
T_UP = 125                                # slope 1.6: spec 200/125 exact
T0 = time.time()


# ------------------------------------------------------------ traces
def r0(t):
    return exp_glm1.reality(t)


def _mk(fn):
    cache = {}
    def g(t):
        if t not in cache:
            cache[t] = fn(t)
        return cache[t]
    return g


def slope_trace(t_up):
    """Symmetric integer ramp over [353,553] (spin27 verbatim).
    Slope per SPEC = AMP/t_up (exact rational); integer every tick."""
    period = 2 * t_up

    def fn(t):
        p = t % period
        if p < t_up:
            return BAND_LO + p * AMP // t_up
        return BAND_LO + AMP - (p - t_up) * AMP // t_up
    return fn


S16 = ("s1.6-T125", _mk(slope_trace(T_UP)))   # spec slope 200/125 = 1.600
SPEC_SLOPE = 200 / 125


# ------------------------------------------------------------ instrument
def dyn_run(lats_fn, reality_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA0,
            drift=DRIFT, seed=20260902):
    """run_fabric interference arm clone (spin27 verbatim); delta param."""
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


def pct(window, delta=DELTA0):
    return within_pm(window, delta) / 10.0


def mean(v):
    return sum(v) / len(v)


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


def static_fn(lats):
    return lambda t, L=lats: L


def crossing(pcts, spreads=SPREADS, level=50.0):
    """50% crossing by linear interpolation between adjacent spreads."""
    for i in range(len(pcts) - 1):
        if pcts[i] >= level >= pcts[i + 1]:
            return spreads[i] + (pcts[i] - level) / (
                pcts[i] - pcts[i + 1]) * (spreads[i + 1] - spreads[i])
    return None


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: wiring byte-identity dyn_run(R0,d12) vs run_fabric ==")
    nchk = 0
    a_ok = True
    for name, lats in (("zero", [0] * N), ("ladder@30", ladder(30)),
                       ("ladder@14", ladder(14)),
                       ("cohort", [0, 0, 0, 30, 30, 30])):
        for k in (1, 2):
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA0, drift=DRIFT, seed=sd)["resid"]
                b = dyn_run(static_fn(lats), r0, k=k, seed=sd)
                nchk += 1
                if a != b:
                    a_ok = False
                    print(f"  MISMATCH {name} K={k} seed={sd}")
    print(f"  {'PASS' if a_ok else 'FAIL'}: {nchk} configs byte-identical")
    ok &= a_ok

    print("\n== CANARY b: R0 anchors at delta=12 (5-seed means) ==")
    tot_ev = tot_m = 0
    rs = []
    for sd in SEEDS:
        r = run_fabric("interference", TICKS, ladder(15), K=1, pd=PD,
                       delta=DELTA0, drift=DRIFT, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn(ladder(15)), r0, k=1, seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b1 = abs(p - 71.5) <= 0.05 and abs(ev - 5792) <= 0.5 \
        and abs(m - 106378) <= 0.5
    print(f"  ladder15 K=1: pct={p:.2f} (71.5)  ev={ev:.1f} (5792)  "
          f"debt={m:.1f} (106378)  -> {'PASS' if b1 else 'FAIL'}")
    tot_ev = tot_m = 0
    rs = []
    for sd in SEEDS:
        r = run_fabric("interference", TICKS, [0] * N, K=1, pd=PD,
                       delta=DELTA0, drift=DRIFT, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn([0] * N), r0, k=1, seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b2 = abs(p - 77.3) <= 0.05 and abs(m - 187834) <= 0.5
    print(f"  zero    K=1: pct={p:.2f} (77.3)  debt={m:.1f} (187834)"
          f"  -> {'PASS' if b2 else 'FAIL'}")
    ok &= b1 and b2

    print("\n== CANARY c: delta=12 slope-1.6 replay of SPIN-27 s*==17.9 ==")
    pcts = [mean([pct(dyn_run(static_fn(ladder(s)), S16[1], k=1, seed=sd,
                               delta=12), delta=12)
                  for sd in SEEDS]) for s in SPREADS]
    cx = crossing(pcts)
    c_ok = cx is not None and abs(cx - 17.9) <= 1.0 \
        and abs(cx * SPEC_SLOPE - 28.6) <= 1.5
    print(f"  curve: " + " ".join(f"{p:.1f}" for p in pcts))
    print(f"  s*={cx and round(cx,1)} (want ~17.9 tol 1.0)  "
          f"C={cx and round(cx*SPEC_SLOPE,1)} (want ~28.6 tol 1.5)"
          f"  -> {'PASS' if c_ok else 'FAIL'}")
    ok &= c_ok

    print("\n== CANARY d: determinism (dual runs, all deltas) ==")
    d_ok = True
    n2 = 0
    for dlt in DELTAS:
        for s in (8, 20, 40):
            for k in (1, 2):
                a = dyn_run(static_fn(ladder(s)), S16[1], k=k, delta=dlt,
                            seed=42)
                b = dyn_run(static_fn(ladder(s)), S16[1], k=k, delta=dlt,
                            seed=42)
                n2 += 1
                if a != b:
                    d_ok = False
                    print(f"  NONDETERMINISTIC delta={dlt} s={s} K={k}")
    print(f"  {'PASS' if d_ok else 'FAIL'}: {n2} dual runs byte-identical")
    ok &= d_ok
    return ok


# ------------------------------------------------------------ panel
def arm(spread, k, delta):
    return mean([pct(dyn_run(static_fn(ladder(spread)), S16[1], k=k,
                             delta=delta, seed=sd), delta=delta)
                 for sd in SEEDS])


def run_panel():
    print("\n== PANEL: slope 1.6 ladder sweep 8..40, 5-seed mean % ==")
    print(f"{'delta':>6}" + "".join(f"{s:>6}" for s in SPREADS)
          + "  50%x" + "   C=s*·slope")
    out = {}
    for dlt in DELTAS:
        c1 = [arm(s, 1, dlt) for s in SPREADS]
        x1 = crossing(c1)
        out[dlt] = (c1, x1)
        cstr = f"{x1 * SPEC_SLOPE:.1f}" if x1 is not None else "—"
        print(f"{dlt:>6}" + "".join(f"{p:>6.1f}" for p in c1)
              + f" {x1 is not None and round(x1,1) or '—':>6}"
              + f" {cstr:>10}")
        sys.stdout.flush()
    print("-- continuity column: K=2 at delta=12 --")
    c2 = [arm(s, 2, 12) for s in SPREADS]
    x2 = crossing(c2)
    print("     K2" + "".join(f"{p:>6.1f}" for p in c2)
          + f" {x2 is not None and round(x2,1) or '—':>6}"
          + f" {x2 is not None and f'{x2*SPEC_SLOPE:.1f}':>10}")
    out["K2@12"] = (c2, x2)
    sys.stdout.flush()
    return out


def analyze(out):
    print("\n== ANALYSIS (decision rule pre-registered in header) ==")
    print("-- headline: C(delta) = s*·slope, alpha = C/(2*delta) --")
    Cs, alphas = {}, {}
    for dlt in DELTAS:
        x1 = out[dlt][1]
        if x1 is None:
            print(f"  delta={dlt}: NO 50% crossing inside sweep — "
                  f"INCONCLUSIVE arm")
            continue
        C = x1 * SPEC_SLOPE
        Cs[dlt] = C
        alphas[dlt] = C / (2 * dlt)
        print(f"  delta={dlt:>2}: s*={x1:6.1f}  C={C:6.1f}  "
              f"alpha={alphas[dlt]:.3f}  (pred C={1.192*2*dlt:5.1f})")
    ds = sorted(Cs)
    av = [alphas[d] for d in ds]
    a_rng = (max(av) - min(av)) / mean(av)
    # linearity check: second difference of C vs delta (uneven grid ->
    # fit linear and check max residual against noise ~0.5)
    xs = [float(d) for d in ds]
    ys = [Cs[d] for d in ds]
    nb = len(xs)
    sxx = sum((x - mean(xs)) ** 2 for x in xs)
    b_aff = sum((x - mean(xs)) * (y - mean(ys))
                for x, y in zip(xs, ys)) / sxx
    a_aff = mean(ys) - b_aff * mean(xs)
    res_aff = [y - (a_aff + b_aff * x) for x, y in zip(xs, ys)]
    b_org = sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)
    res_org = [y - b_org * x for x, y in zip(xs, ys)]
    c_c2d = mean([y - 2 * d for d, y in zip(ds, ys)])
    res_c2d = [y - 2 * d - c_c2d for d, y in zip(ds, ys)]

    def sse(r):
        return sum(e * e for e in r)

    print(f"  alpha range = {a_rng*100:.1f}% of mean alpha "
          f"(falsifier at >15%)")
    print("-- secondary fits (SSE, max|resid|; noise floor ~0.5 in C) --")
    print(f"  through-origin C={b_org:.3f}·d      : "
          f"SSE={sse(res_org):7.2f}  maxres={max(abs(e) for e in res_org):.2f}"
          f"  (implied alpha={b_org/2:.3f})")
    print(f"  affine      C={a_aff:.2f}+{b_aff:.3f}·d : "
          f"SSE={sse(res_aff):7.2f}  maxres={max(abs(e) for e in res_aff):.2f}")
    print(f"  2d+const    C=2·d+{c_c2d:.2f}     : "
          f"SSE={sse(res_c2d):7.2f}  maxres={max(abs(e) for e in res_c2d):.2f}"
          f"  (implied alpha at d=12: {(24+c_c2d)/24:.3f})")

    lin_ok = max(abs(e) for e in res_aff) <= 1.5   # ~3x noise floor
    alpha_ok = a_rng <= 0.15
    if lin_ok and alpha_ok:
        verdict = "VALIDATED"
    elif not lin_ok:
        verdict = "FALSIFIED (nonlinear in delta)"
    else:
        verdict = "MIXED (linear but alpha drift > 15%)"
    print(f"  linearity: max|affine resid| = "
          f"{max(abs(e) for e in res_aff):.2f} "
          f"({'linear' if lin_ok else 'NONLINEAR'}, gate 1.5)")
    print(f"VERDICT: {verdict}")
    sys.stdout.flush()
    return verdict, Cs, alphas


def main():
    print("SPIN-29 METROLOGY C=f(delta) —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} ladder, slope 1.6 spec 200/{T_UP}, "
          f"spreads={list(SPREADS)}, deltas={DELTAS}, K=1(+2@d12), "
          f"seeds={SEEDS}, ticks={TICKS}, drift={DRIFT}, pd={PD}")
    print("PREDICTION (pre-registered): C(d)=alpha·2d, alpha~1.192; "
          "FALSIFY if C nonlinear in d or alpha varies >15%.")

    print("\n== TRACE FINGERPRINT (from SPEC) ==")
    vals = [S16[1](t) for t in range(2 * T_UP)]
    print(f"  {S16[0]}: period={2*T_UP} band=[{min(vals)},{max(vals)}] "
          f"spec-slope=200/{T_UP}={SPEC_SLOPE:.3f}")
    sys.stdout.flush()

    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    sys.stdout.flush()
    if not ok:
        sys.exit(1)

    out = run_panel()
    analyze(out)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
