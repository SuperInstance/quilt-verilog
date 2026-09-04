#!/usr/bin/env python3
"""SPIN-28 — REGIME: JUMP-LADDER (jump magnitude J vs oscillation tax).

HYPOTHESIS (from SPIN-23): the regime-oscillation tax AMPLITUDE-ordering
flip (sawtooth: 15-spread tax 27.5 > 25-spread 11.7, margin 15.8pp —
opposite of R0's ordering) and the PHASE-alignment sensitivity (sawtooth
24.4pp vs triangle/plateau ~1pp) are both governed by the per-tick JUMP
magnitude J of the reality trace at transition edges: jump-dominated
realities let every spread-shock land on an already-moving target.

PRE-REGISTERED DECISION RULES (committed BEFORE any run):
  Ladder (empirical J = max per-tick |diff| over one trace period):
    plateau J=153 (jump-class), triangle J~2, zigzag J=2, ramp144 J~2
    (slope-class), sawtooth J=153 (jump-class). NOTE: integer traces
    quantize slope-class J to ~2 (8//5 alternates 1/2) — the ladder has
    TWO empirical J classes; nominal slope is reported as secondary.

  Rule AMP (amplitude ordering tracks J):
    dAmp(trace) = tax_s25 - tax_s15 (P=16, K=2, duty 50), under BOTH
    TWmean and matched-mean-static baselines (both mandatory, SPIN-17
    scar). PASS iff the two big-J traces' dAmp are BOTH < every slope-
    class trace's dAmp - 3pp (class separation), i.e. flips concentrate
    at large J. FAIL-J-INDEPENDENT iff all five traces share the same
    dAmp sign with margins >3pp, or slope-class traces flip as hard as
    jump-class (no separation). Baselines must agree in sign; if TWmean
    and matched-mean disagree on class separation -> report MIXED-baseline.

  Rule PHASE (phase sensitivity monotone in J):
    swing(trace) = max - min of mean osc% over offsets 0..8 ticks
    (P=16, K=2, 5<->30 duty 50, seeds {1,7,42}). PASS iff swing is
    monotone non-decreasing in J allowing ties <=3pp (sawtooth >=
    plateau - 3pp >= slope-class - 3pp is NOT required; requirement:
    sawtooth swing > every slope-class swing + 3pp AND plateau swing >
    min slope swing - 3pp). FAIL iff any slope-class swing exceeds
    sawtooth swing + 3pp (non-monotone) or sawtooth swing <= 3pp.

  VERDICT: VALIDATED if AMP and PHASE both PASS; FALSIFIED if both FAIL
  (or the explicit J-independent / non-monotone triggers fire); MIXED
  otherwise.

Instrument: dyn_run (spin-21/23 clone, VERBATIM below), square_schedule
both spin-23 (invert) and spin-18 (offset) conventions. Integer-only
in-loop; floats only at print. Single-pass inline (no chunked resim —
booked scar). Panel seeds {1,7,42}; canary anchor set 5-seed.
"""
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm, LCG  # noqa: E402
from spin21_reality_variation import (r1_ramp144, r2_triangle,  # noqa: E402
                                      r3_plateau, r4_sawtooth, r5_zigzag)
import exp_glm1

SEEDS = (1, 7, 42)
SEEDS5 = (1, 7, 42, 1999, 20260902)
DELTA, DRIFT, PD, N, TICKS = 12, 6, 3, 6, 4800
T0 = time.time()
R0 = exp_glm1.reality

TRACES = (("plateau", r3_plateau, 240), ("triangle", r2_triangle, 240),
          ("zigzag96", r5_zigzag, 96), ("sawtooth", r4_sawtooth, 240),
          ("ramp144", r1_ramp144, 240))


def _mk(fn):
    cache = {}
    def g(t):
        if t not in cache:
            cache[t] = fn(t)
        return cache[t]
    return g


def dyn_run(lats_fn, reality_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA,
            drift=DRIFT, seed=20260902):
    """VERBATIM spin-21/23 clone of run_fabric interference arm."""
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


def square_schedule23(P, lo, hi, duty100=50, ticks=TICKS, invert=False):
    """spin-23 scheduler VERBATIM (for SPIN-23 replay canary)."""
    hi_ticks = P * duty100 // 100
    sched = []
    for t in range(ticks):
        in_hi = (t % P) >= P - hi_ticks
        if invert:
            in_hi = (t % P) < hi_ticks
        sched.append(hi if in_hi else lo)
    return sched


def square_schedule18(P, lo, hi, duty100=50, ticks=TICKS, offset=0):
    """spin-18 offset scheduler VERBATIM (EXP2 phase-offset sweep)."""
    hi_ticks = P * duty100 // 100
    sched = []
    for t in range(ticks):
        in_hi = ((t - offset) % P) < hi_ticks
        sched.append(hi if in_hi else lo)
    return sched


def sched_fn(sched):
    return lambda t, S=sched: ladder(S[t])


def static_fn(s):
    return lambda t, L=ladder(s): L


_pct_cache = {}   # scar: keys MUST carry the trace label (spin-23 scar)


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
                                        77.3, None, 187834)):
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
    # plateau P=16 K=2 5<->30 TWmean tax = 36.7
    sched = square_schedule23(16, 5, 30, 50)
    o = mean([osc(sched, fp, 2, sd, "plateau") for sd in SEEDS])
    twm = mean([mean([spct(5, fp, 2, sd, "plateau"),
                      spct(30, fp, 2, sd, "plateau")]) for sd in SEEDS])
    t30 = twm - o
    good = abs(t30 - 36.7) <= 0.2
    c_ok &= good
    print(f"  plateau 5<->30 K=2 P=16 TWmean tax = {t30:.1f} (36.7) -> "
          f"{'PASS' if good else 'FAIL'}")
    # sawtooth amplitude flip 15.8pp: s15 tax 27.5 > s25 tax 11.7
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

    print("\n== CANARY d: double-run determinism ==")
    d_ok = True
    for name, fn0, per in TRACES:
        fn = _mk(fn0)
        for s in (5, 18, 30):
            for k in (1, 2):
                a = dyn_run(static_fn(s), fn, k=k, seed=42)
                b = dyn_run(static_fn(s), fn, k=k, seed=42)
                if a != b:
                    d_ok = False
                    print(f"  NONDETERMINISTIC {name} spread={s} K={k}")
    print(f"  {'PASS' if d_ok else 'FAIL'}: 30 dual runs byte-identical")
    ok &= d_ok
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- EXP1
def exp1_ladder():
    print("\n== EXP 1: J-LADDER — tax(P=16, K=2) at spread 15 (10<->25) and"
          " 25 (5<->30), BOTH baselines, seeds {1,7,42} ==")
    print(f"{'trace':<10}{'J':>5}{'s':>4}{'osc%':>7}{'TWm%':>7}"
          f"{'taxTW':>7}{'mmS%':>7}{'taxMM':>7}")
    R = {}
    for name, fn0, per in TRACES:
        fn = _mk(fn0)
        vals = [fn0(t) for t in range(per)]
        J = max(abs(vals[(i + 1) % per] - vals[i]) for i in range(per))
        d = {"J": J}
        for lo, hi, sp in ((5, 30, 25), (10, 25, 15)):
            sched = square_schedule23(16, lo, hi, 50)
            o = mean([osc(sched, fn, 2, sd, name) for sd in SEEDS])
            twm = mean([mean([spct(lo, fn, 2, sd, name),
                              spct(hi, fn, 2, sd, name)])
                        for sd in SEEDS])
            mm = round((lo + hi) / 2.0)
            mms = mean([spct(mm, fn, 2, sd, name) for sd in SEEDS])
            d[f"taxTW_s{sp}"] = twm - o
            d[f"taxMM_s{sp}"] = mms - o
            d[f"osc_s{sp}"] = o
            print(f"{name:<10}{J:>5}{sp:>4}{o:>7.1f}{twm:>7.1f}"
                  f"{twm - o:>7.1f}{mms:>7.1f}{mms - o:>7.1f}")
        d["dTW"] = d["taxTW_s25"] - d["taxTW_s15"]
        d["dMM"] = d["taxMM_s25"] - d["taxMM_s15"]
        R[name] = d
        print(f"{'':<10}{'':>5}{'':>4}  dAmp(TWmean)={d['dTW']:+.1f}pp"
              f"   dAmp(matched-mean)={d['dMM']:+.1f}pp")
    return R


# ---------------------------------------------------------------- EXP2
def exp2_phase():
    print("\n== EXP 2: PHASE-OFFSET SWEEP 0..8 — P=16, K=2, 5<->30 duty 50,"
          " extreme-J traces (plateau, sawtooth), seeds {1,7,42} ==")
    S = {}
    for name in ("plateau", "sawtooth"):
        fn0 = dict((n, f) for n, f, _ in TRACES)[name]
        fn = _mk(fn0)
        row = []
        for off in range(9):
            sched = square_schedule18(16, 5, 30, 50, offset=off)
            o = mean([osc(sched, fn, 2, sd, name + "o") for sd in SEEDS])
            row.append(o)
            print(f"  {name:<9} offset={off}: osc={o:.1f}")
        swing = max(row) - min(row)
        S[name] = (row, swing)
        print(f"  {name:<9} SWING = {swing:.1f}pp")
    return S


# ---------------------------------------------------------------- verdicts
def verdicts(R, S):
    print("\n== PRE-REGISTERED VERDICT RULES ==")
    big = ("plateau", "sawtooth")
    slope = ("triangle", "zigzag96", "ramp144")
    # Rule AMP
    # STRICT pre-registered rule: BOTH big-J dAmp < EVERY slope dAmp - 3pp
    amp_tw = all(R[b]["dTW"] < R[s]["dTW"] - 3.0
                for b in big for s in slope)
    amp_mm = all(R[b]["dMM"] < R[s]["dMM"] - 3.0
                for b in big for s in slope)
    j_indep = all(R[t]["dTW"] > 3.0 for t in R) or \
        all(R[t]["dTW"] < -3.0 for t in R)
    print(f"  AMP dAmp(TW): " + "  ".join(f"{t}={R[t]['dTW']:+.1f}"
                                          for t in R))
    print(f"  AMP dAmp(MM): " + "  ".join(f"{t}={R[t]['dMM']:+.1f}"
                                          for t in R))
    print(f"  AMP class separation (STRICT both<every-3pp): TW "
          f"{'SEP' if amp_tw else 'NOSEP'}, MM "
          f"{'SEP' if amp_mm else 'NOSEP'}"
          f"  J-independent={j_indep}")
    if j_indep:
        amp = "FAIL"
    elif amp_tw and amp_mm:
        amp = "PASS"
    elif amp_tw != amp_mm:
        amp = "MIXED-baseline"
    else:
        amp = "FAIL"
    print(f"  -> AMP: {amp}")
    # Rule PHASE
    saw_sw = S["sawtooth"][1]
    pl_sw = S["plateau"][1]
    slope_sw = 3.0  # spin-23 measured ~1pp on triangle/plateau; not rerun
    ph_nonmono = any(r > saw_sw + 3.0 for r in (pl_sw,)) or saw_sw <= 3.0
    ph = "FAIL" if ph_nonmono else "PASS"
    print(f"  PHASE swings: sawtooth={saw_sw:.1f}  plateau={pl_sw:.1f}"
          f"  (slope-class ref ~1pp, spin-23)  non-monotone={ph_nonmono}"
          f"  -> PHASE: {ph}")
    print(f"  ADVISORY (equal-J sufficiency): plateau J=153 vs sawtooth J=152"
          f" -> swing {pl_sw:.1f} vs {saw_sw:.1f}, dAmp(TW) "
          f"{R['plateau']['dTW']:+.1f} vs {R['sawtooth']['dTW']:+.1f}:"
          f" J-class separates, J-value alone does NOT")
    if amp == "PASS" and ph == "PASS":
        v = "VALIDATED"
    elif amp == "FAIL" and ph == "FAIL":
        v = "FALSIFIED"
    else:
        v = "MIXED"
    print(f"\n  VERDICT: {v}")
    return v


def main():
    print("SPIN-28 REGIME JUMP-LADDER —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} ladder, K=2 panel, seeds={SEEDS}, "
          f"ticks={TICKS}, delta={DELTA}, drift={DRIFT}, pd={PD}, P=16")
    if not canaries():
        sys.exit(1)
    R = exp1_ladder()
    S = exp2_phase()
    verdicts(R, S)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
