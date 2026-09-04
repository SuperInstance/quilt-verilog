#!/usr/bin/env python3
"""SPIN-33 — REGIME: EDGE-DENSITY LADDER (SPIN-28 follow-up).

CONTEXT (SPIN-28 verdict): J-CLASS separates phase/amplitude behavior,
but strict pre-registration FALSIFIED a pure-J amplitude law (equal-J
plateau vs sawtooth differ; sawtooth amplitude flip 15.8pp collapses at
matched-mean). SPIN-21: knee ~ 2*delta/slowest-sustained-slope.
OPEN: is tax amplitude governed by (a) edge DENSITY (edges/cycle E,
per-edge damage), (b) inter-edge SLOPE, or (c) the E*J product?

DESIGN: pin jump size J=153 (sawtooth-class) across an L-shaped 2D grid
E (edges/240-cycle) x s (inter-edge rise slope, units/tick). Trace
constructor (integer-only): L=240//E per segment; trace(t) = 400 +
min(153, (t%L)*s); each segment boundary is a single-tick drop of 153.
Band [400,553] exactly like spin-21 traces. Feasibility requires
(L-1)*s >= 153. Grid points:
  E=1: s in {1,2,3,4,6}   E=2: s in {2,3,4,6}   E=3: s in {3,4,6}
  E=4: s in {3,4,6}       E=6: s in {6}
(16 grid points; J empirically asserted == 153 at every edge.)

PRE-REGISTERED DECISION RULES (committed BEFORE any run):
  Metric per grid point: dAmp_B = tax_s25 - tax_s15 (P=16, K=2,
  duty 50, square 5<->30 / 10<->25) under BOTH baselines B in {TWmean,
  matched-mean} (SPIN-17 scar — both mandatory). Seeds {1,7,42}.
  Effect sizes:
    range_all  = max - min dAmp over the whole grid
    E_effect   = mean over slope-columns with >=3 E-points of
                 (max - min dAmp within column)
    s_effect   = mean over E-rows with >=3 s-points of
                 (max - min dAmp within row)
  Rule (a) EDGE-DENSITY: E_effect >= 6.0pp AND E_effect > s_effect+3.0
  Rule (b) SLOPE:        s_effect >= 6.0pp AND s_effect > E_effect+3.0
  Rule (c) E*J product:  with J pinned, E*J is strictly monotone in E,
    so (c) predicts the SAME ordering as (a); (c) is separated from (a)
    ONLY by the slope axis: if (a)'s E-effect holds AND s_effect < 3.0pp
    (slope axis inert), report (c) preferred over (a) iff a pure E
    scalar fit (linear in E, both baselines, R^2-style residual <=2pp
    mean abs) beats any fit that needs slope. Simplified numeric rule:
      (c) iff E_effect>=6.0 AND E_effect>s_effect+3.0 AND s_effect<3.0
      (a) iff E_effect>=6.0 AND E_effect>s_effect+3.0 AND s_effect>=3.0
  Rule NONE/J-LAW (falsifies a, b, c): range_all <= 3.0pp -> amplitude
    invariant under E and slope at pinned J (supports per-edge J law,
    SPIN-28's residual finding).
  Baselines must agree on the winning rule class; disagreement ->
    MIXED-baseline verdict. If neither threshold met and range_all>3:
    INCONCLUSIVE.
  VERDICT mapping: (a)/(b)/(c) -> "VALIDATED (a)/(b)/(c)"; NONE ->
    "FALSIFIED (all three; supports per-edge-J amplitude law)".

Phase-offset spot-check (advisory, extremes E1s1 vs E6s6): swing
(max-min mean osc% over offsets 0..8, P=16 K=2 5<->30, seeds {1,7,42}).
Pre-registered: swing must NOT be explained by (a): predicted under
pure-E that swing grows monotonically with E; report numbers.

RULES: integer-only in-loop, floats at print only; single-pass inline
dyn_run (SPIN-16 scar: chunked resim resets LCG); schedule-phase pinned
(spin-23 convention for tax panels); unique output spin33-output.txt
(SPIN-30 collision scar); python3 -u direct redirect, no pipes; panel
seeds {1,7,42}, canary anchors 5-seed; every cache/print carries an
explicit trace label (SPIN-23 fn.__name__ collision scar).
Instrument: dyn_run VERBATIM reuse from spin28_regime (spin-21/23
clone, canary re-proven here).
"""
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import exp_glm1
from exp_glm1 import run_fabric, within_pm, LCG  # noqa: E402
from spin21_reality_variation import (r3_plateau, r4_sawtooth)  # noqa: E402
from spin28_regime import (dyn_run, pct, mean, ladder,  # noqa: E402
                           square_schedule23, square_schedule18,
                           sched_fn, static_fn)

SEEDS = (1, 7, 42)
SEEDS5 = (1, 7, 42, 1999, 20260902)
DELTA, DRIFT, PD, N, TICKS = 12, 6, 3, 6, 4800
T0 = time.time()
R0 = exp_glm1.reality
JPIN = 153
PER = 240

GRID = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 6),
        (2, 2), (2, 3), (2, 4), (2, 6),
        (3, 3), (3, 4), (3, 6),
        (4, 3), (4, 4), (4, 6),
        (6, 6))


def edge_trace(E, s):
    """Integer trace, band [400,553], E drops of 153 per 240-cycle."""
    L = PER // E
    def f(t):
        i = t % L
        return 400 + min(JPIN, i * s)
    return f


def _mk(fn):
    cache = {}
    def g(t):
        if t not in cache:
            cache[t] = fn(t)
        return cache[t]
    return g


_pct_cache = {}   # scar: keys MUST carry trace label (spin-23 scar)


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


def empirical_J(fn, per=PER):
    v = [fn(t) for t in range(per)]
    return max(abs(v[(i + 1) % per] - v[i]) for i in range(per))


def empirical_E(fn, per=PER, thr=12):
    v = [fn(t) for t in range(per)]
    return sum(1 for i in range(per)
               if abs(v[(i + 1) % per] - v[i]) > thr)


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY a: wiring byte-identity dyn_run(R0) vs run_fabric ==")
    nchk = 0
    for name, lats in (("zero", [0] * N), ("ladder@30", ladder(30)),
                       ("ladder@14", ladder(14)),
                       ("cohort", [0, 0, 0, 30, 30, 30])):
        for k in (1, 2):
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=sd)["resid"]
                b = dyn_run(lambda t, L=lats: L, R0, k=k, seed=sd)
                nchk += 1
                if a != b:
                    ok = False
                    print(f"  MISMATCH {name} K={k} seed={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} configs byte-identical")

    print("\n== CANARY b: R0 anchors (5-seed means) ==")
    b_ok = True
    for name, lats, k, wp, wev, wm in (("ladder15", ladder(15), 1,
                                        71.5, 5792, 106378),
                                       ("zero", [0] * N, 1,
                                        77.3, 8756, 187834)):
        te = tm = 0
        rs = []
        for sd in SEEDS5:
            r = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                           delta=DELTA, drift=DRIFT, seed=sd)
            te += r["events"]
            tm += r["mass"]
            rs.append(pct(r["resid"]))
        p, ev, m = mean(rs), te / 5.0, tm / 5.0
        good = abs(p - wp) <= 0.05 and abs(m - wm) <= 0.5 \
            and (wev is None or abs(ev - wev) <= 0.5)
        b_ok &= good
        print(f"  {name:<9} K={k}: pct={p:.2f} ({wp})  ev={ev:.1f}"
              f" ({wev})  debt={m:.1f} ({wm})  -> "
              f"{'PASS' if good else 'FAIL'}")
    ok &= b_ok

    print("\n== CANARY c: SPIN-23 replays (seeds {1,7,42}) ==")
    c_ok = True
    fp = _mk(r3_plateau)
    fs = _mk(r4_sawtooth)
    sched = square_schedule23(16, 5, 30, 50)
    o = mean([osc(sched, fp, 2, sd, "plateau") for sd in SEEDS])
    twm = mean([mean([spct(5, fp, 2, sd, "plateau"),
                      spct(30, fp, 2, sd, "plateau")]) for sd in SEEDS])
    t30 = twm - o
    good = abs(t30 - 36.7) <= 0.2
    c_ok &= good
    print(f"  plateau 5<->30 K=2 P=16 TWmean tax = {t30:.1f} (36.7) -> "
          f"{'PASS' if good else 'FAIL'}")
    s15 = square_schedule23(16, 10, 25, 50)
    o15 = mean([osc(s15, fs, 2, sd, "sawtooth") for sd in SEEDS])
    twm15 = mean([mean([spct(10, fs, 2, sd, "sawtooth"),
                        spct(25, fs, 2, sd, "sawtooth")]) for sd in SEEDS])
    t15 = twm15 - o15
    o25 = mean([osc(sched, fs, 2, sd, "sawtooth") for sd in SEEDS])
    twm25 = mean([mean([spct(5, fs, 2, sd, "sawtooth"),
                        spct(30, fs, 2, sd, "sawtooth")]) for sd in SEEDS])
    t25 = twm25 - o25
    good = abs(t15 - 27.5) <= 0.2 and abs(t25 - 11.7) <= 0.2 \
        and abs((t15 - t25) - 15.8) <= 0.4
    c_ok &= good
    print(f"  sawtooth tax s15={t15:.1f} (27.5)  s25={t25:.1f} (11.7)  "
          f"flip={t15 - t25:+.1f}pp (15.8) -> {'PASS' if good else 'FAIL'}")
    ok &= c_ok

    print("\n== CANARY d: double-run determinism + grid J/E assertions ==")
    d_ok = True
    for E, s in ((1, 1), (2, 3), (4, 4), (6, 6)):
        f0 = edge_trace(E, s)
        f = _mk(f0)
        if empirical_J(f0) != JPIN:
            d_ok = False
            print(f"  BAD J at E={E} s={s}: {empirical_J(f0)}")
        if empirical_E(f0) != E:
            d_ok = False
            print(f"  BAD E-edge-count at E={E} s={s}: {empirical_E(f0)}")
        for sp in (5, 18, 30):
            a = dyn_run(static_fn(sp), f, k=2, seed=42)
            b = dyn_run(static_fn(sp), f, k=2, seed=42)
            if a != b:
                d_ok = False
                print(f"  NONDETERMINISTIC E{E}s{s} spread={sp}")
    print(f"  {'PASS' if d_ok else 'FAIL'}: 12 dual runs byte-identical,"
          f" J==153 and edge-count==E on 4 grid corners")
    ok &= d_ok
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- EXP1
def exp1_grid():
    print("\n== EXP 1: EDGE-DENSITY LADDER — tax(P=16, K=2) at spread 15"
          " (10<->25) and 25 (5<->30), BOTH baselines, seeds {1,7,42} ==")
    print(f"{'trace':<10}{'J':>5}{'E':>3}{'s':>3}{'osc15':>7}{'osc25':>7}"
          f"{'taxTW15':>8}{'taxTW25':>8}{'taxMM15':>8}{'taxMM25':>8}"
          f"{'dTW':>7}{'dMM':>7}")
    R = {}
    sched15 = square_schedule23(16, 10, 25, 50)
    sched25 = square_schedule23(16, 5, 30, 50)
    for E, s in GRID:
        f0 = edge_trace(E, s)
        f = _mk(f0)
        tag = f"E{E}s{s}"
        d = {"E": E, "s": s, "J": empirical_J(f0)}
        o15 = mean([osc(sched15, f, 2, sd, tag) for sd in SEEDS])
        o25 = mean([osc(sched25, f, 2, sd, tag) for sd in SEEDS])
        twm15 = mean([mean([spct(10, f, 2, sd, tag),
                            spct(25, f, 2, sd, tag)]) for sd in SEEDS])
        twm25 = mean([mean([spct(5, f, 2, sd, tag),
                            spct(30, f, 2, sd, tag)]) for sd in SEEDS])
        mm15 = (10 + 25 + 1) // 2  # 18
        mm25 = (5 + 30 + 1) // 2   # 18
        mms = mean([spct(mm15, f, 2, sd, tag) for sd in SEEDS])
        d["taxTW15"], d["taxTW25"] = twm15 - o15, twm25 - o25
        d["taxMM15"], d["taxMM25"] = mms - o15, mms - o25
        d["dTW"] = d["taxTW25"] - d["taxTW15"]
        d["dMM"] = d["taxMM25"] - d["taxMM15"]
        d["osc15"], d["osc25"] = o15, o25
        R[tag] = d
        print(f"{tag:<10}{d['J']:>5}{E:>3}{s:>3}{o15:>7.1f}{o25:>7.1f}"
              f"{d['taxTW15']:>8.1f}{d['taxTW25']:>8.1f}"
              f"{d['taxMM15']:>8.1f}{d['taxMM25']:>8.1f}"
              f"{d['dTW']:>7.1f}{d['dMM']:>7.1f}")
    return R


# ---------------------------------------------------------------- EXP2
def exp2_phase():
    print("\n== EXP 2: PHASE-OFFSET SWEEP 0..8 — P=16, K=2, 5<->30 duty 50,"
          " grid extremes E1s1 vs E6s6, seeds {1,7,42} ==")
    S = {}
    for E, s in ((1, 1), (6, 6)):
        f = _mk(edge_trace(E, s))
        tag = f"E{E}s{s}o"
        row = []
        for off in range(9):
            sched = square_schedule18(16, 5, 30, 50, offset=off)
            o = mean([osc(sched, f, 2, sd, tag) for sd in SEEDS])
            row.append(o)
            print(f"  E{E}s{s:<2} offset={off}: osc={o:.1f}")
        swing = max(row) - min(row)
        S[f"E{E}s{s}"] = (row, swing)
        print(f"  E{E}s{s:<2} SWING = {swing:.1f}pp")
    return S


# ---------------------------------------------------------------- verdicts
def col_row_effects(R, key):
    bys = {}
    for tag, d in R.items():
        bys.setdefault(d["s"], []).append((d["E"], d[key]))
    cols = [v for v in bys.values() if len(v) >= 3]
    bye = {}
    for tag, d in R.items():
        bye.setdefault(d["E"], []).append((d["s"], d[key]))
    rows = [v for v in bye.values() if len(v) >= 3]
    e_eff = mean([max(x[1] for x in c) - min(x[1] for x in c)
                  for c in cols]) if cols else 0.0
    s_eff = mean([max(x[1] for x in r) - min(x[1] for x in r)
                  for r in rows]) if rows else 0.0
    rng = max(d[key] for d in R.values()) - min(d[key] for d in R.values())
    return e_eff, s_eff, rng, cols, rows


def classify(e_eff, s_eff, rng):
    if rng <= 3.0:
        return "NONE"
    if e_eff >= 6.0 and e_eff > s_eff + 3.0:
        return "c" if s_eff < 3.0 else "a"
    if s_eff >= 6.0 and s_eff > e_eff + 3.0:
        return "b"
    return "INCONCLUSIVE"


def verdicts(R, S):
    print("\n== PRE-REGISTERED VERDICT RULES ==")
    res = {}
    for key, lbl in (("dTW", "TWmean"), ("dMM", "matched-mean")):
        e_eff, s_eff, rng, cols, rows = col_row_effects(R, key)
        cls = classify(e_eff, s_eff, rng)
        res[key] = cls
        print(f"  [{lbl}] E_effect={e_eff:.1f}pp  s_effect={s_eff:.1f}pp"
              f"  grid_range={rng:.1f}pp  -> rule '{cls}'")
    if res["dTW"] == res["dMM"] and res["dTW"] != "INCONCLUSIVE":
        v = res["dTW"]
        if v == "NONE":
            verdict = "FALSIFIED (all three: a, b, c — amplitude invariant" \
                      " under E and slope at pinned J; supports per-edge-J law)"
        else:
            verdict = f"VALIDATED ({v})"
    elif res["dTW"] != res["dMM"]:
        verdict = "MIXED-baseline"
    else:
        verdict = "INCONCLUSIVE"
    print(f"  baselines: TW={res['dTW']}  MM={res['dMM']}")
    print(f"  VERDICT: {verdict}")
    print(f"  ADVISORY phase: swings E1s1={S['E1s1'][1]:.1f}pp vs "
          f"E6s6={S['E6s6'][1]:.1f}pp (pure-E predicts E6s6 > E1s1)")
    return verdict


def main():
    print("SPIN-33 REGIME EDGE-DENSITY LADDER —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} ladder, J pinned {JPIN}, grid {len(GRID)} pts,"
          f" seeds={SEEDS}, ticks={TICKS}, P=16, K=2")
    if not canaries():
        sys.exit(1)
    R = exp1_grid()
    S = exp2_phase()
    verdicts(R, S)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
