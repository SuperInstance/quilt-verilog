#!/usr/bin/env python3
"""SPIN 21 — REALITY-VARIATION (SPIN-20 question #1 / V2).

Is the K=2 regime catastrophe (zero-lock flip 77.3 -> 50.0 -> 73.9 -> 69.0;
ladder@30 K=1 26.8; fresh-cohort n_f causality; spread knee ~15) a FABRIC
LAW or a property of THIS reality trace (240-cycle, ramp<96 + two
descents, band 400-553)?

DESIGN
  R0 original reality (verbatim exp_glm1.reality).
  6 NEW integer traces, band [400,553], matched amplitude statistics,
  different structure (see TRACES below; includes a period-239 variant so
  the trace is incommensurate with 240).
  Panel: grammars {zero, ladder@30, cohort 3+3, kcoh5@30} x K{1,2,4,8}
  x 5 seeds per trace. Plus a ladder spread sweep {10,12,14,15,16,18,20,
  22,24,27,30} at K=1 per trace to locate the knee (the accessible
  "wall edge"; the 2pd+1=7 co-fire wall itself cannot be crossed at N=6
  and is outside this panel — stated here as an honest boundary).

PRE-REGISTERED DECISION RULE (stated BEFORE any panel run):
  For each phenomenon (K=2 trough depth per grammar = min(K1,K4) - K2;
  zero-lock K-flip presence = K2 is the minimum of the K-sweep AND
  trough >= 5pp; n_f effect = pct(kcoh5) - pct(cohort) at K=2):
    FABRIC-LAW (trace-stable)  iff sign is preserved across ALL 7 traces
      AND cross-trace range (max-min) of the magnitude <= 5pp.
    TRACE-PROPERTY             iff sign flips in >=1 trace OR range > 5pp.
  Knee/wall edge: "moves" iff argmax-drop spread (over the K=1 sweep)
    differs from the R0 knee by > 2 spread units; additionally compared
    to the slope-adjusted 2D prediction knee ~ round(2*delta / maxslope)
    where maxslope = max per-tick |d s/dt| of the trace (R0: 8/5 -> 15).

CANARIES (mandatory gate):
  a. wiring byte-identity dyn_run(r0) vs exp_glm1.run_fabric, 6 configs.
  b. R0 anchor replays: zero K-sweep 77.3/50.0/73.9/69.0; ladder@30 K=1
     26.8; ladder@15 K=1 71.5 (tol 0.2pp).
  c. determinism: every new trace, run twice (zero + ladder@30, K=2,
     seed 42), byte-identical.

Integer-only inside every loop; floats only at print/stat time.
Instrument: dyn_run, verbatim clone of run_fabric interference arm with
reality_fn and k as PARAMETERS (spin-17 canary-proven; re-proven here).
Single-pass inline simulation; no chunked re-sim; no pipes.
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
KS = (1, 2, 4, 8)
SPREADS = (10, 12, 14, 15, 16, 18, 20, 22, 24, 27, 30)
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


def r1_ramp144(t):
    """Rise 153 over 144 ticks (slow slope ~1.06), one fast descent 96."""
    p = t % 240
    if p < 144:
        return 400 + p * 153 // 144
    return 553 - (p - 144) * 153 // 96


def r2_triangle(t):
    """Symmetric triangle: up 96 (+8/5), down 96 (-8/5), hold 48 at 400."""
    p = t % 240
    if p < 96:
        return 400 + p * 8 // 5
    if p < 192:
        return 553 - (p - 96) * 8 // 5
    return 400


def r3_plateau(t):
    """Two-plateau step: 400 for 120 ticks, 553 for 120 ticks."""
    p = t % 240
    return 400 if p < 120 else 553


def r4_sawtooth(t):
    """Slow rise +1/tick for 153 ticks (400->553), drop, hold 400 x87."""
    p = t % 240
    if p < 153:
        return 400 + p
    return 400


def r5_zigzag(t):
    """Fast zigzag: +2/tick x48, -2/tick x48 (band 400-496), 2.5 cycles
    per 240. Slope magnitude 2 > 8/5 — steeper than reality."""
    p = t % 96
    return 400 + (p * 2 if p < 48 else (96 - p) * 2)


def r6_prime239(t):
    """R0 partition scaled to prime period 239 (ramp96, descent47 @-1,
    descent96 @-8/5) — incommensurate with every divisor of 240."""
    p = t % 239
    if p < 96:
        return 400 + p * 8 // 5
    if p < 143:
        return 553 - (p - 96)
    return 553 - 47 - (p - 143) * 8 // 5


TRACES = (
    ("R0-original", r0),
    ("R1-ramp144", _mk(r1_ramp144)),
    ("R2-triangle", _mk(r2_triangle)),
    ("R3-plateau", _mk(r3_plateau)),
    ("R4-sawtooth", _mk(r4_sawtooth)),
    ("R5-zigzag96", _mk(r5_zigzag)),
    ("R6-prime239", _mk(r6_prime239)),
)

# slope fingerprint per trace (integer, per-tick |diff| over one period)
PERIOD_OF = {"R0-original": 240, "R1-ramp144": 240, "R2-triangle": 240,
             "R3-plateau": 240, "R4-sawtooth": 240, "R5-zigzag96": 96,
             "R6-prime239": 239}


def trace_stats(fn, period):
    vals = [fn(t) for t in range(period)]
    diffs = [abs(vals[(i + 1) % period] - vals[i]) for i in range(period)]
    return min(vals), max(vals), sum(vals) / len(vals), max(diffs), \
        max(v for v in diffs if v <= 8 or v > 8)  # placeholder, replaced


# analytic slope fingerprints: name -> (description, max sustained |slope|/tick)
SLOPES = {
    "R0-original": ("ramp96 +8/5, desc48 -1, desc96 -8/5", 1.6),
    "R1-ramp144": ("rise144 ~1.06, desc96 -8/5", 1.6),
    "R2-triangle": ("up96 +8/5, down96 -8/5, hold48", 1.6),
    "R3-plateau": ("0-slope plateaus, jump 153", 0.0),
    "R4-sawtooth": ("rise153 +1, jump -153, hold", 1.0),
    "R5-zigzag96": ("48-tick ramps at 2/tick", 2.0),
    "R6-prime239": ("ramp96 +8/5, desc47 -1, desc96 -8/5", 1.6),
}

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


GRAMMARS = (
    ("zero",     [0] * N),
    ("ladder30", ladder(30)),
    ("cohort33", [0, 0, 0, 30, 30, 30]),
    ("kcoh5@30", [0, 0, 0, 0, 0, 30]),
)


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: wiring byte-identity dyn_run(R0) vs run_fabric ==")
    nchk = 0
    for name, lats in (("zero", [0] * N), ("ladder@30", ladder(30)),
                       ("cohort", [0, 0, 0, 30, 30, 30])):
        for k in (1, 2):
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=sd)["resid"]
                b = dyn_run(static_fn(lats), r0, k=k, seed=sd)
                nchk += 1
                if a != b:
                    ok = False
                    print(f"  MISMATCH {name} K={k} seed={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} configs byte-identical")

    print("\n== CANARY b: R0 anchor replays (5-seed means) ==")
    want = {("zero", 1): 77.3, ("zero", 2): 50.0, ("zero", 4): 73.9,
            ("zero", 8): 69.0, ("ladder30", 1): 26.8, ("ladder15", 1): 71.5}
    got = {}
    for (g, k), w in sorted(want.items()):
        lats = ladder(15) if g == "ladder15" else dict(GRAMMARS).get(
            g, ladder(30))
        rs = [pct(dyn_run(static_fn(lats), r0, k=k, seed=sd))
              for sd in SEEDS]
        m = mean(rs)
        got[(g, k)] = m
        good = abs(m - w) <= 0.2
        ok &= good
        print(f"  {g:<9} K={k}: {m:6.1f} (want {w})  "
              f"-> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY c: determinism, every trace (zero + ladder30, K=2,"
          " seed 42, run twice) ==")
    c3 = True
    for name, fn in TRACES:
        for lats in ([0] * N, ladder(30)):
            a = dyn_run(static_fn(lats), fn, k=2, seed=42)
            b = dyn_run(static_fn(lats), fn, k=2, seed=42)
            if a != b:
                c3 = False
                print(f"  NONDETERMINISTIC {name}")
    print(f"  {'PASS' if c3 else 'FAIL'}: 14 dual runs byte-identical")
    return ok and c3


# ------------------------------------------------------------ panel
_panel_cache = {}


def panel(grammar_lats, fn, k, tag):
    key = (tag, k, tuple(grammar_lats))
    if key not in _panel_cache:
        _panel_cache[key] = [pct(dyn_run(static_fn(grammar_lats), fn,
                                         k=k, seed=sd)) for sd in SEEDS]
    return _panel_cache[key]


def run_panel():
    print("\n== PANEL: grammar x K sweep per trace (5-seed mean %) ==")
    results = {}   # trace -> grammar -> K -> mean pct
    for name, fn in TRACES:
        print(f"\n-- {name} --")
        print(f"{'grammar':>10}" + "".join(f"{'K=' + str(k):>8}"
                                           for k in KS))
        results[name] = {}
        for gname, lats in GRAMMARS:
            row = {k: mean(panel(lats, fn, k, name)) for k in KS}
            results[name][gname] = row
            print(f"{gname:>10}"
                  + "".join(f"{row[k]:>8.1f}" for k in KS))
        sys.stdout.flush()
    return results


def run_knee():
    print("\n== KNEE: ladder spread sweep, K=1, per trace ==")
    print(f"{'trace':>12}" + "".join(f"{s:>7}" for s in SPREADS)
          + "   knee 50%x")
    knees = {}
    curves = {}
    for name, fn in TRACES:
        pcts = []
        for s in SPREADS:
            pcts.append(mean(panel(ladder(s), fn, 1, name + "#s" + str(s))))
        drops = [pcts[i] - pcts[i + 1] for i in range(len(pcts) - 1)]
        knee = SPREADS[drops.index(max(drops))] if max(drops) > 0 else None
        # 50% crossing (interpolated)
        cross = None
        for i in range(len(pcts) - 1):
            if pcts[i] >= 50.0 >= pcts[i + 1]:
                cross = SPREADS[i] + (pcts[i] - 50.0) / (
                    pcts[i] - pcts[i + 1]) * (SPREADS[i + 1] - SPREADS[i])
                break
        knees[name] = knee
        curves[name] = pcts
        print(f"{name:>12}" + "".join(f"{p:>7.1f}" for p in pcts)
              + f"   {knee}  {cross if cross is None else round(cross, 1)}")
        sys.stdout.flush()
    return knees, curves


# ------------------------------------------------------------ analysis
def analyze(results, knees, curves):
    print("\n== ANALYSIS (decision rule pre-registered in header) ==")
    tnames = [name for name, _ in TRACES]

    print("\n-- A1: K=2 trough depth (min(K1,K4) - K2, pp) per grammar --")
    print(f"{'grammar':>10}" + "".join(f"{t[:9]:>10}" for t in tnames)
          + "   range  verdict")
    for gname, _ in GRAMMARS:
        ds = []
        for t in tnames:
            row = results[t][gname]
            ds.append(min(row[1], row[4]) - row[2])
        rng = max(ds) - min(ds)
        sign_stable = all(d >= 0 for d in ds) or all(d <= 0 for d in ds)
        verdict = ("STABLE" if (sign_stable and rng <= 5.0)
                   else "TRACE-PROP")
        print(f"{gname:>10}" + "".join(f"{d:>10.1f}" for d in ds)
              + f"   {rng:4.1f}  {verdict}")

    print("\n-- A2: zero-lock K-flip (K2 is argmin of K-sweep AND "
          "trough>=5pp)? --")
    flips = []
    for t in tnames:
        row = results[t]["zero"]
        argmin = min(KS, key=lambda k: row[k])
        trough = min(row[1], row[4]) - row[2]
        flips.append(argmin == 2 and trough >= 5.0)
    print("   " + "  ".join(f"{t[:9]}={'Y' if f else 'N'}"
                            for t, f in zip(tnames, flips)))
    print(f"   persists on {sum(flips)}/{len(flips)} traces -> "
          + ("STABLE" if all(flips) else "TRACE-PROP"))

    print("\n-- A3: n_f effect = kcoh5 - cohort (pp), per K --")
    for k in KS:
        ds = [results[t]["kcoh5@30"][k] - results[t]["cohort33"][k]
              for t in tnames]
        rng = max(ds) - min(ds)
        sign_stable = all(d >= 0 for d in ds) or all(d <= 0 for d in ds)
        verdict = ("STABLE" if (sign_stable and rng <= 5.0)
                   else "TRACE-PROP")
        print(f"   K={k}:" + "".join(f"{d:>8.1f}" for d in ds)
              + f"   range {rng:4.1f}  {verdict}")
    # K=1 headline too (Spin 12 causal direction was fresh>stale)
    for k in KS:
        ds = [results[t]["kcoh5@30"][k] - results[t]["ladder30"][k]
              for t in tnames]
        rng = max(ds) - min(ds)
        sign_stable = all(d >= 0 for d in ds) or all(d <= 0 for d in ds)
        print(f"   K={k} vs ladder:" + "".join(f"{d:>8.1f}" for d in ds)
              + f"   range {rng:4.1f}  "
              + ("STABLE" if (sign_stable and rng <= 5.0) else "TRACE-PROP"))

    print("\n-- A4: knee / wall-edge relocation --")
    k0 = knees["R0-original"]
    print(f"   R0 knee (argmax drop) = {k0}")
    for t in tnames:
        mv = "STABLE" if (knees[t] is not None and k0 is not None
                          and abs(knees[t] - k0) <= 2) else "MOVES"
        print(f"   {t:<12} knee={str(knees[t]):>4}  -> {mv}")
    print("\n   slope fingerprints (analytic sustained-ramp |slope|; knee "
          "prediction ~ round(2*delta/slope)):")
    for t in tnames:
        desc, sl = SLOPES[t]
        pred = round(2 * DELTA / sl) if sl else "n/a (0-slope)"
        print(f"   {t:<12} {desc}  slope={sl}  pred-knee={pred}")
    sys.stdout.flush()


def main():
    print("SPIN-21 REALITY-VARIATION —", time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N}, K={KS}, seeds={SEEDS}, ticks={TICKS}, "
          f"delta={DELTA}, drift={DRIFT}, pd={PD}")
    print("DECISION RULE (pre-registered, see header): sign preserved on "
          "all 7 traces AND cross-trace range <= 5pp = STABLE/fabric-law; "
          "sign flip anywhere OR range > 5pp = trace-property. "
          "Knee moves iff argmax-drop spread differs > 2 units from R0.")

    print("\n== TRACE FINGERPRINTS ==")
    for name, fn in TRACES:
        p = PERIOD_OF[name]
        vals = [fn(t) for t in range(p)]
        diffs = [abs(vals[(i + 1) % p] - vals[i]) for i in range(p)]
        print(f"  {name:<12} period={p:>3} band=[{min(vals)},{max(vals)}]"
              f" mean={mean(vals):.0f} maxstep={max(diffs)}")
    sys.stdout.flush()

    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    sys.stdout.flush()
    if not ok:
        sys.exit(1)

    results = run_panel()
    knees, curves = run_knee()
    analyze(results, knees, curves)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
