#!/usr/bin/env python3
"""SPIN 30 — METROLOGY: drift x band sweep at delta=12. Where does alpha~1.19
come from? (SPIN-29 next-spoke proposal.)

HYPOTHESES (pre-registered in this header AND SPIN-30-drift-band.md BEFORE
any panel run):
  H1 (drift violator): alpha = 1 + f(drift/delta). Predicts alpha(drift=0,
     A=200) -> 1, i.e. C -> 2*delta = 24.0, s* -> 15.0, and alpha varying
     > 15% across drift {0,2,6,10} at A=200. VALIDATED iff alpha(d0,A200)
     within 15% of 1.0 AND drift-range of alpha > 15%.
  H2 (fabric constant): C ~= 2.38*delta independent of drift and band.
     VALIDATED iff alpha within 15% of mean alpha across ALL 12 arms
     (including drift=0).
  Else MIXED.
  SECONDARY: fit C vs drift (A=200) to {affine, alpha = 1 + c*drift/delta};
  fit C vs A (drift=6, A in {96,200,400}) to {const, affine-in-log2(A)}.

DESIGN (pre-registered): delta=12 fixed, slope pinned exactly 1.6 by SPEC,
K=1, N=6 ladder, 4800 ticks, pd=3, seeds 1/7/42/1999/20260902 (5-seed
means), spread sweep 8..40 step 2 (17 pts, same grid as SPIN-29 — no
post-hoc widening; an arm whose 50% crossing falls outside 8..40 is
INCONCLUSIVE, reported as such). 12 arms = full grid drift {0,2,6,10} x
band-amplitude {96,200,400} at delta=12.

PRE-REGISTERED DEVIATION FROM BRIEF: brief said band-amplitude {100,200,
400}; A=100 is not integer-realizable at spec slope exactly 1.6 (t_up =
62.5 non-integer; SPIN-21 scar: slope from SPEC, never sampled). Sub-
stituted A=96 (t_up=60, spec slope 96/60 = 1.600 exact). Registered in
SPIN-30-drift-band.md BEFORE any run. BAND_LO pinned 353 all arms.

CANARIES (unchanged from SPIN-29; gate before any panel counts):
  a. 16/16 byte-identity dyn_run(R0,d12) vs exp_glm1.run_fabric.
  b. anchors d12: ladder15 K=1 pct 71.5/ev 5792/debt 106378; zero K=1
     pct 77.3/debt 187834.
  c. d12 slope-1.6 baseline replay of SPIN-29: s* ~ 17.6 (tol 1.0),
     C ~ 28.1 (tol 1.0). If C != 28.1 +- 1.0: STOP (harness discrepancy).
  d. determinism: 30 dual runs byte-identical.

Integer-only inside every loop; floats only at print/stat time.
Instrument: dyn_run — verbatim clone of spin29_metrology_cdelta.py's clone
of spin27's clone of spin21's canary-proven inline run_fabric interference
arm. python3 -u direct redirect; no pipes.
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
DELTA = 12
DRIFT = 6
PD = 3
N = 6
TICKS = 4800
DRIFTS = (0, 2, 6, 10)
AMPS = (96, 200, 400)                    # spec slope 1.6: t_up = A*5/8
SPREADS = tuple(range(8, 41, 2))          # 17 points, pre-registered
BAND_LO = 353
T0 = time.time()
SPEC_SLOPE = 1.6


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


def slope_trace(amp):
    """Symmetric integer ramp, band [BAND_LO, BAND_LO+amp], spec slope
    amp/t_up = 1.600 exact (t_up = amp*5/8, integer for amp in AMPS)."""
    t_up = amp * 5 // 8
    period = 2 * t_up

    def fn(t):
        p = t % period
        if p < t_up:
            return BAND_LO + p * amp // t_up
        return BAND_LO + amp - (p - t_up) * amp // t_up
    return fn


TRACES = {a: _mk(slope_trace(a)) for a in AMPS}


# ------------------------------------------------------------ instrument
def dyn_run(lats_fn, reality_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA,
            drift=DRIFT, seed=20260902):
    """run_fabric interference arm clone (spin29 verbatim); drift param."""
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


def pct(window, delta=DELTA):
    return within_pm(window, delta) / 10.0


def mean(v):
    return sum(v) / len(v)


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


def static_fn(lats):
    return lambda t, L=lats: L


def crossing(pcts, spreads=SPREADS, level=50.0):
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
                               delta=DELTA, drift=DRIFT, seed=sd)["resid"]
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
                       delta=DELTA, drift=DRIFT, seed=sd)
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
                       delta=DELTA, drift=DRIFT, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn([0] * N), r0, k=1, seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b2 = abs(p - 77.3) <= 0.05 and abs(m - 187834) <= 0.5
    print(f"  zero    K=1: pct={p:.2f} (77.3)  debt={m:.1f} (187834)"
          f"  -> {'PASS' if b2 else 'FAIL'}")
    ok &= b1 and b2

    print("\n== CANARY c: d12 slope-1.6 baseline replay of SPIN-29 "
          "(s*=17.6, C=28.1; STOP if C!=28.1+-1.0) ==")
    pcts = [mean([pct(dyn_run(static_fn(ladder(s)), TRACES[200], k=1,
                               seed=sd))
                  for sd in SEEDS]) for s in SPREADS]
    cx = crossing(pcts)
    C = cx * SPEC_SLOPE if cx is not None else None
    c_ok = cx is not None and abs(cx - 17.6) <= 1.0 and abs(C - 28.1) <= 1.0
    print(f"  curve: " + " ".join(f"{p:.1f}" for p in pcts))
    print(f"  s*={cx and round(cx,1)} (want 17.6 tol 1.0)  "
          f"C={C and round(C,1)} (want 28.1 tol 1.0)"
          f"  -> {'PASS' if c_ok else 'FAIL'}")
    ok &= c_ok

    print("\n== CANARY d: determinism (30 dual runs, arms sample) ==")
    d_ok = True
    n2 = 0
    for dft in DRIFTS:
        for a in AMPS:
            b1_ = dyn_run(static_fn(ladder(20)), TRACES[a], k=1,
                          drift=dft, seed=42)
            b2_ = dyn_run(static_fn(ladder(20)), TRACES[a], k=1,
                          drift=dft, seed=42)
            n2 += 1
            if b1_ != b2_:
                d_ok = False
                print(f"  NONDETERMINISTIC drift={dft} A={a}")
    print(f"  {'PASS' if d_ok else 'FAIL'}: {n2} dual runs byte-identical")
    ok &= d_ok
    return ok


# ------------------------------------------------------------ panel
def arm(spread, drift, amp):
    return mean([pct(dyn_run(static_fn(ladder(spread)), TRACES[amp], k=1,
                             drift=drift, seed=sd))
                 for sd in SEEDS])


def run_panel():
    print("\n== PANEL: 12 arms (drift x band) at d=12, slope 1.6 spec, "
          "5-seed mean %, spread 8..40 ==")
    out = {}
    for a in AMPS:
        print(f"-- band amplitude A={a} (t_up={a*5//8}, spec slope "
              f"{a}/{a*5//8}={SPEC_SLOPE:.3f}) --")
        print(f"{'drift':>6}" + "".join(f"{s:>6}" for s in SPREADS)
              + "  50%x" + "     C")
        for dft in DRIFTS:
            cs = [arm(s, dft, a) for s in SPREADS]
            x = crossing(cs)
            out[(dft, a)] = (cs, x)
            cstr = f"{x*SPEC_SLOPE:.1f}" if x is not None else "—"
            print(f"{dft:>6}" + "".join(f"{p:>6.1f}" for p in cs)
                  + f" {x is not None and round(x,1) or '—':>6}"
                  + f" {cstr:>7}")
            sys.stdout.flush()
    return out


def analyze(out):
    print("\n== ANALYSIS (decision rules pre-registered in header) ==")
    print("-- headline: C(drift,A) = s*·slope, alpha = C/(2·12) --")
    C, alpha = {}, {}
    for (dft, a), (_, x) in sorted(out.items()):
        if x is None:
            print(f"  drift={dft:>2} A={a:>3}: NO 50% crossing in 8..40 — "
                  f"INCONCLUSIVE arm")
            continue
        C[(dft, a)] = x * SPEC_SLOPE
        alpha[(dft, a)] = C[(dft, a)] / (2 * DELTA)
        print(f"  drift={dft:>2} A={a:>3}: s*={x:6.1f}  C={C[(dft,a)]:6.1f}"
              f"  alpha={alpha[(dft,a)]:.3f}")
    sys.stdout.flush()

    if (0, 200) not in C:
        print("VERDICT: INCONCLUSIVE (baseline arm drift=0,A=200 has no "
              "crossing)")
        return "INCONCLUSIVE", C, alpha

    a_d0 = alpha[(0, 200)]
    al_drift = [alpha[(d, 200)] for d in DRIFTS if (d, 200) in alpha]
    drift_rng = (max(al_drift) - min(al_drift)) / mean(al_drift) if al_drift else 0
    all_al = list(alpha.values())
    all_rng = (max(all_al) - min(all_al)) / mean(all_al)

    print(f"  alpha(d0,A200) = {a_d0:.3f} (H1 needs within 15% of 1.000)")
    print(f"  alpha range across drift @A200 = {drift_rng*100:.1f}% "
          f"(H1 needs >15%)")
    print(f"  alpha range across ALL 12 arms = {all_rng*100:.1f}% "
          f"(H2 needs <=15%)")

    # secondary: C vs drift at A=200
    if len(al_drift) == 4:
        ds = [float(d) for d in DRIFTS]
        ys = [C[(d, 200)] for d in DRIFTS]
        sxx = sum((x - mean(ds)) ** 2 for x in ds)
        b = sum((x - mean(ds)) * (y - mean(ys)) for x, y in zip(ds, ys)) / sxx
        a0 = mean(ys) - b * mean(ds)
        print(f"  fit C = {a0:.2f} + {b:.3f}·drift  (2Δ law would be "
              f"intercept 24.0, slope 0)")
        # fit alpha = 1 + c*drift/delta
        c = (mean(ys) - 24.0) / mean(ds) if True else 0
        print(f"  fit alpha = 1 + {c:.4f}·(drift/12): implies C(0)= "
              f"{24.0:.1f}? reported intercept {a0:.2f}")

    # secondary: C vs A at drift=6
    ys6 = [(a, C[(6, a)]) for a in AMPS if (6, a) in C]
    if len(ys6) == 3:
        import math
        xs = [math.log2(a) for a, _ in ys6]
        yy = [y for _, y in ys6]
        sxx = sum((x - mean(xs)) ** 2 for x in xs)
        b = sum((x - mean(xs)) * (y - mean(yy))
                for x, y in zip(xs, yy)) / sxx
        a0 = mean(yy) - b * mean(xs)
        res = [y - (a0 + b * x) for x, y in zip(xs, yy)]
        print(f"  fit C = {a0:.2f} + {b:.3f}·log2(A) @drift=6 "
              f"(maxres={max(abs(r) for r in res):.2f}, const-law resid "
              f"spread {max(yy)-min(yy):.2f}; noise ~0.5)")

    h1 = abs(a_d0 - 1.0) <= 0.15 and drift_rng > 0.15
    h2 = all_rng <= 0.15
    if h1:
        verdict = "H1 VALIDATED: drift is the violator; 2Δ returns at drift=0"
    elif h2:
        verdict = "H2 VALIDATED: alpha is a fabric constant ~ 2.38Δ law"
    else:
        verdict = "MIXED"
    print(f"VERDICT: {verdict}")
    sys.stdout.flush()
    return verdict, C, alpha


def main():
    print("SPIN-30 METROLOGY drift x band sweep @ d=12 —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} ladder, slope 1.6 spec, spreads 8..40, "
          f"drifts={DRIFTS}, amps={AMPS}, K=1, seeds={SEEDS}, "
          f"ticks={TICKS}, pd={PD}, delta={DELTA}, BAND_LO={BAND_LO}")
    print("PRE-REGISTERED: H1 alpha->1 at drift=0 (2Δ returns); H2 alpha "
          "const ~1.19 across all 12 arms; else MIXED.")

    print("\n== TRACE FINGERPRINTS (from SPEC) ==")
    for a in AMPS:
        vals = [TRACES[a](t) for t in range(2 * (a * 5 // 8))]
        print(f"  A={a:>3}: period={2*(a*5//8)} band=[{min(vals)},"
              f"{max(vals)}] spec-slope={a}/{a*5//8}={SPEC_SLOPE:.3f}")
    sys.stdout.flush()

    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    sys.stdout.flush()
    if not ok:
        print("STOP per pre-registration (canary c gate: C != 28.1 +- 1.0 "
              "or other canary failure).")
        sys.exit(1)

    out = run_panel()
    analyze(out)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
