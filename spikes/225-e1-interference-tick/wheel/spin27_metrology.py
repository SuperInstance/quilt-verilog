#!/usr/bin/env python3
"""SPIN 27 — METROLOGY (spoke 1): the slope-law knee.

HYPOTHESIS (pre-registered, filed by SPIN-21's next-spoke proposal and in
WHEEL-LOG SPIN-27 brief BEFORE any panel run):
  The spread-knee law is  knee ~ 2*delta / SLOWEST sustained ramp slope of
  the reality trace (R1 evidence: knee 20 at spec slope 200/188 ~ 1.06 on
  ramp144; 2*12/1.06 ~ 22.6, crossing measured 23.7).
  Prediction: for synthetic integer traces with controlled sustained slope
  s in {0.8, 1.2, 1.6, 2.0, 2.4} (integer numerator/denominator per-tick
  realization, band-matched to R0's 353-553 amplitude with wrap), the
  ladder-grammar 50%-residency-crossing spread s* satisfies
      s* * slope ~ 24 +/- 2     (2*delta = 24, delta = 12).
  FALSIFY if the product varies > 30% across slopes, or if the knee is
  slope-independent (identical s* within noise on all traces).

DESIGN
  Traces: symmetric rise/descent over band [353,553] (A=200), integer
  interpolation value(t) = 353 + t*A//T_up so slope is EXACTLY the
  rational A/T_up per SPEC (booked scar from SPIN-21: fingerprints from
  the SPEC, never sampled). T_up = round(A/s): 250, 167, 125, 100, 83.
  Period = 2*T_up (slopes 0.800, 1.198, 1.600, 2.000, 2.410).
  Grammar: N=6 ladder, spread sweep {8,10,...,30} (12 points), K=1
  primary; K=2 secondary column. Statistic: 50%-residency crossing by
  linear interpolation between adjacent spreads (SPIN-21 named this
  cleaner than argmax-drop onset).
  Seeds 1/7/42/1999/20260902, 5-seed means; 4800 ticks; delta=12.

CANARIES (mandatory gate, all must pass before any panel counts):
  a. wiring byte-identity >= 6 configs dyn_run(R0) vs exp_glm1.run_fabric
     raw resid arrays.
  b. anchors exact: ladder15 K=1 pct=71.5 / ev 5792 / debt 106378;
     zero K=1 pct=77.3 / debt 187834 (5-seed means).
  c. ramp144 trace replay of SPIN-21 knee-20 anchor (argmax-drop knee 20,
     50%-crossing ~23.7, tol 2.0).
  d. determinism: every arm run twice, byte-identical resid.

Integer-only inside every loop; floats only at print/stat time.
Instrument: dyn_run — VERBATIM clone of spin21_reality_variation.py's
canary-proven single-pass inline run_fabric interference arm with
reality_fn and k as parameters. python3 -u direct redirect; no pipes; no
shell=True.
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
SPREADS = tuple(range(8, 31, 2))          # 8,10,...,30 (12 points)
SLOPE_SET = (0.8, 1.2, 1.6, 2.0, 2.4)
BAND_LO = 353
AMP = 200                                  # 353-553, R0's true band
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
    """Symmetric integer ramp over [353,553]: rise T_up, descend T_up.
    Slope per SPEC = AMP/T_up (exact rational). Integer at every tick."""
    period = 2 * t_up

    def fn(t):
        p = t % period
        if p < t_up:
            return BAND_LO + p * AMP // t_up
        return BAND_LO + AMP - (p - t_up) * AMP // t_up
    return fn


def r1_ramp144(t):
    """SPIN-21 R1 verbatim (knee-20 anchor replay)."""
    p = t % 240
    if p < 144:
        return 400 + p * 153 // 144
    return 553 - (p - 144) * 153 // 96


# spec'd slopes: rational AMP/T_up per slope target (SCAR: spec, not sample)
TRACES = []
TUP_OF = {}
for s in SLOPE_SET:
    t_up = int(AMP / s + 0.5)
    TUP_OF[s] = t_up
    TRACES.append((f"s{s}-T{t_up}", _mk(slope_trace(t_up))))
SPEC_SLOPE = {f"s{s}-T{TUP_OF[s]}:": None for s in SLOPE_SET}
SPEC_SLOPE = {f"s{s}-T{TUP_OF[s]}": (AMP, TUP_OF[s]) for s in SLOPE_SET}
R1 = ("R1-ramp144", _mk(r1_ramp144))


# ------------------------------------------------------------ instrument
def dyn_run(lats_fn, reality_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA,
            drift=DRIFT, seed=20260902):
    """run_fabric interference arm clone; reality_fn + k PARAMETERS.
    Verbatim physics otherwise (canary a re-proves byte-identity)."""
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


def events_mass(lats, k, fn, seeds=SEEDS):
    """ev/debt (events, mass) via run_fabric only for R0 anchors."""
    tot_ev = tot_m = 0
    for sd in seeds:
        if fn is r0:
            r = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                           delta=DELTA, drift=DRIFT, seed=sd)
        else:
            raise ValueError("anchors only on R0")
        tot_ev += r["events"]
        tot_m += r["mass"]
    return tot_ev / len(seeds), tot_m / len(seeds)


def crossing(pcts, level=50.0):
    """50% crossing by linear interpolation between adjacent spreads."""
    for i in range(len(pcts) - 1):
        if pcts[i] >= level >= pcts[i + 1]:
            return SPREADS[i] + (pcts[i] - level) / (
                pcts[i] - pcts[i + 1]) * (SPREADS[i + 1] - SPREADS[i])
    return None


def argmax_drop(pcts):
    drops = [pcts[i] - pcts[i + 1] for i in range(len(pcts) - 1)]
    return SPREADS[drops.index(max(drops))] if max(drops) > 0 else None


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: wiring byte-identity dyn_run(R0) vs run_fabric ==")
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

    print("\n== CANARY b: R0 anchors (5-seed means) ==")
    # ladder15 K=1: pct 71.5 / ev 5792 / debt 106378
    ev, m = events_mass(ladder(15), 1, r0)
    rs = [pct(dyn_run(static_fn(ladder(15)), r0, k=1, seed=sd))
          for sd in SEEDS]
    p = mean(rs)
    b1 = abs(p - 71.5) <= 0.05 and abs(ev - 5792) <= 0.5 \
        and abs(m - 106378) <= 0.5
    print(f"  ladder15 K=1: pct={p:.2f} (71.5)  ev={ev:.1f} (5792)  "
          f"debt={m:.1f} (106378)  -> {'PASS' if b1 else 'FAIL'}")
    ev, m = events_mass([0] * N, 1, r0)
    rs = [pct(dyn_run(static_fn([0] * N), r0, k=1, seed=sd))
          for sd in SEEDS]
    p = mean(rs)
    b2 = abs(p - 77.3) <= 0.05 and abs(m - 187834) <= 0.5
    print(f"  zero    K=1: pct={p:.2f} (77.3)  debt={m:.1f} (187834)"
          f"  -> {'PASS' if b2 else 'FAIL'}")
    ok &= b1 and b2

    print("\n== CANARY c: ramp144 replay of SPIN-21 knee-20 anchor ==")
    pcts = [mean([pct(dyn_run(static_fn(ladder(s)), R1[1], k=1, seed=sd))
                  for sd in SEEDS]) for s in SPREADS]
    kn = argmax_drop(pcts)
    cx = crossing(pcts)
    c_ok = kn == 20 and cx is not None and abs(cx - 23.7) <= 2.0
    print(f"  curve: " + " ".join(f"{p:.1f}" for p in pcts))
    print(f"  knee(argmax-drop)={kn} (want 20)  50%x={cx and round(cx,1)}"
          f" (want 23.7 tol 2.0)  -> {'PASS' if c_ok else 'FAIL'}")
    ok &= c_ok

    print("\n== CANARY d: determinism (each arm twice, byte-identical) ==")
    d_ok = True
    for name, fn in TRACES + [R1]:
        for s in (8, 18, 30):
            for k in (1, 2):
                a = dyn_run(static_fn(ladder(s)), fn, k=k, seed=42)
                b = dyn_run(static_fn(ladder(s)), fn, k=k, seed=42)
                if a != b:
                    d_ok = False
                    print(f"  NONDETERMINISTIC {name} spread={s} K={k}")
    print(f"  {'PASS' if d_ok else 'FAIL'}: 36 dual runs byte-identical")
    ok &= d_ok
    return ok


# ------------------------------------------------------------ panel
def arm(fn, spread, k):
    return mean([pct(dyn_run(static_fn(ladder(spread)), fn, k=k, seed=sd))
                 for sd in SEEDS])


def run_panel():
    print("\n== PANEL: ladder spread sweep {8..30}, 5-seed mean % ==")
    print("          K=1 (primary)                |  K=2 (secondary)")
    print(f"{'trace':>12}" + "".join(f"{s:>6}" for s in SPREADS)
          + "  50%x" + "".join(f"{s:>6}" for s in SPREADS) + "  50%x")
    out = {}
    for name, fn in TRACES:
        c1 = [arm(fn, s, 1) for s in SPREADS]
        c2 = [arm(fn, s, 2) for s in SPREADS]
        x1 = crossing(c1)
        x2 = crossing(c2)
        out[name] = (c1, c2, x1, x2)
        print(f"{name:>12}"
              + "".join(f"{p:>6.1f}" for p in c1)
              + f" {x1 is not None and round(x1,1) or '—':>6}"
              + "".join(f"{p:>6.1f}" for p in c2)
              + f" {x2 is not None and round(x2,1) or '—':>6}")
        sys.stdout.flush()
    return out


def analyze(out):
    print("\n== ANALYSIS (decision rule pre-registered in header) ==")
    print("-- headline: s* * slope per trace (predict 24 +/- 2; "
          "FALSIFY if range > 30% of 24) --")
    prods = []
    for name, (c1, c2, x1, x2) in out.items():
        a, tu = SPEC_SLOPE[name]
        sl = a / tu                       # spec rational slope (float at print)
        if x1 is None:
            print(f"  {name}: no 50% crossing on K=1 — INCONCLUSIVE arm")
            prods.append(None)
            continue
        pr = x1 * sl
        prods.append(pr)
        print(f"  {name}: spec slope {a}/{tu}={sl:.3f}  s*={x1:.1f}  "
              f"s**slope={pr:.1f}  (pred 24; |dev|={abs(pr-24):.1f})")
    vals = [p for p in prods if p is not None]
    rng = max(vals) - min(vals)
    rel = rng / 24.0
    verdict = ("VALIDATED" if rng <= 4.8 and all(abs(p - 24) <= 4.8
                                                 for p in vals)
               else "FALSIFIED" if rel > 0.30 else "MIXED")
    # slope-independence check: FALSIFY if s* identical (range <= 1.0)
    xs = [out[n][2] for n in out if out[n][2] is not None]
    indep = (max(xs) - min(xs)) <= 1.0
    print(f"  product range {rng:.2f} ({rel*100:.0f}% of 24) -> "
          f"{verdict if not indep else 'FALSIFIED (slope-independent)'}")
    print(f"  s* range {min(xs):.1f}..{max(xs):.1f} -> "
          f"{'slope-DEPENDENT (law alive)' if not indep else 'INDEPENDENT'}")
    # K=2 column
    print("-- secondary K=2 crossing --")
    for name, (c1, c2, x1, x2) in out.items():
        a, tu = SPEC_SLOPE[name]
        if x2 is None:
            print(f"  {name}: no crossing (K=2)")
        else:
            print(f"  {name}: s*2={x2:.1f}  s*2*slope={x2*a/tu:.1f}")
    sys.stdout.flush()
    return verdict


def main():
    print("SPIN-27 METROLOGY slope-law knee —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} ladder, spreads={list(SPREADS)}, K=1(+2), "
          f"seeds={SEEDS}, ticks={TICKS}, delta={DELTA}, drift={DRIFT}, "
          f"pd={PD}")
    print("PREDICTION (pre-registered): s* * slope ~ 24 +/- 2; FALSIFY "
          "if product varies > 30% or knee slope-independent.")

    print("\n== TRACE FINGERPRINTS (from SPEC) ==")
    for name, fn in TRACES:
        a, tu = SPEC_SLOPE[name]
        vals = [fn(t) for t in range(2 * tu)]
        print(f"  {name:<12} period={2*tu:>3} band=[{min(vals)},"
              f"{max(vals)}] spec-slope={a}/{tu}={a/tu:.3f}")
    sys.stdout.flush()

    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    sys.stdout.flush()
    if not ok:
        sys.exit(1)

    out = run_panel()
    v = analyze(out)
    print(f"\nVERDICT: {v}")
    print(f"DONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
