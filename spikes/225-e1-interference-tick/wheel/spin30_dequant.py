#!/usr/bin/env python3
"""SPIN-30 — DEQUANT spoke 8: ZENO-EFFECT probe (§10 cheat-code probes).

Does frequent integer "measurement" of the twin-pulse superposition degrade
the WITHIN-TICK AVERAGING credit that SPIN-dequant-2 attributed the control
win to? SPIN-dequant-2 found pm strictly decreasing in K and argued the
load-bearing superposition is within-tick (twin pulses summing/cancelling
before g moves), with cross-tick wave memory decorative. The quantum-flavored
counter-hypothesis is a Zeno effect: frequent observation (quantization of
the live pulse state) should freeze/degrade dynamics IF cross-tick coherence
carries mass; it should be nearly free if only within-tick averaging matters.

OPERATIONALIZATION (fixed BEFORE any run):
  Measurement = re-round every live pulse magnitude in the deque to a q-bit
  power-of-two grid, applied at the END of every M-th tick:
      mag -> sign(mag) * ((|mag| + half) >> sh << sh),  half = 1 << (sh-1)
  q in {6, 8, 12} -> grid step {16, 4, 1} -> sh {4, 2, 0}.
  M in {1, 4, 16, 64, "never"}. M=1 + q=6 is the maximal-observation cell;
  q=12 (sh=0) is grid-1 = a structural no-op control; M=never is the
  untouched reference. Applied AFTER the decay snapshot of the measurement
  tick, so the net correction of that tick is already delivered unquantized
  (measurement observes state, it does not rewrite history).

PANEL: grammars {zero, kcoh5@15} x K in {1,2} x q {6,8,12} x M {1,4,16,64,
never}, N=6, pd=3, delta=12, drift=6, R0 reality, 4800 ticks, 5 seeds
(1, 7, 42, 1999, 20260902). Metric: pct = per-mille ticks within delta of
truth (5-seed mean).

PRE-REGISTERED PREDICTION + DECISION RULE (BEFORE any panel run):
  Define decoherence cost(cost) = pct(M=never) - pct(cell), per grammar/K.
  PRIMARY cell: zero grammar, K=1, q=8 (grid 4), M=1.
    cost <= 5.0pp  -> WITHIN-TICK AVERAGING doctrine holds: quantized
                      observation is cheap; verdict VALIDATED (Zeno-inert).
    cost > 10.0pp  -> frequent observation of the live pulse state destroys
                      performance that the never-arm enjoys -> supports
                      CROSS-TICK WAVE MEMORY; verdict FALSIFIED (Zeno-real).
    5.0 < cost <= 10.0pp -> MIXED.
  SECONDARY (descriptive, no rule): full grid trend; kcoh5@15 same cell;
  monotonicity in M (Zeno prediction: cost decreasing in M, i.e. rarer
  observation cheaper) and in q (finer grid cheaper).
  FALLBACK (only if panel degenerate, i.e. every cell within 0.2pp of never):
  Manhattan-vs-Euclidean interference metric probe — NOT expected.

CANARIES (mandatory gate, must all PASS before panel is read):
  a. Wiring byte-identity: dyn_run_q(M=never, sh=0) == run_fabric resid,
     6 configs (2 grammars x K{1,2} x seeds{1,42}).
  b. Anchors (run_fabric, 5-seed means): zero K=1 pct 77.3 / debt 187834 /
     ev 8756; ladder@15 K=1 pct 71.5 / ev 5792 / debt 106378 (0.2pp tol on
     pct; debt/ev exact).
  c. Structural no-op: q=12 (sh=0) full-dict == M=never at every M tried
     (quantization of an all-integer grid-1 is identity), >= 4 configs.
  d. Determinism: two quantized cells run twice, byte-identical.
debt := 5-seed mean of run_fabric mass; ev := mean events (spin10
publishing format).

Integer-only inside every loop; floats only at print/stat time.
Single-pass inline; python3 -u, direct redirect, no pipes. One lane only.
"""
import os
import sys
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
KS = (1, 2)
QS = (6, 8, 12)
SH_OF = {6: 4, 8: 2, 12: 0}
MS = (1, 4, 16, 64, None)          # None = never

GRAMMARS = (
    ("zero", [0] * N),
    ("kcoh5@15", [0, 0, 0, 0, 0, 15]),
)


def reality(t):
    return exp_glm1.reality(t)


def pct(window, delta=DELTA):
    return within_pm(window, delta) / 10.0


def mean(v):
    return sum(v) / len(v)


def static_fn(lats):
    return lambda t, L=lats: L


def dyn_run_q(lats_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA, drift=DRIFT,
              seed=20260902, sh=0, m_every=None):
    """run_fabric interference-arm clone (spin21 canary-proven dyn_run) with
    the Zeno measurement bolted on: at end of every m_every-th tick, every
    live pulse magnitude is re-rounded to the 2^sh grid (round-to-nearest,
    sign-safe). m_every=None disables measurement. sh=0 is a structural
    no-op. Returns (resid, events)."""
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    resid = []
    events = 0
    half = (1 << (sh - 1)) if sh > 0 else 0
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
            events += 1
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
        if m_every is not None and sh > 0 and (t + 1) % m_every == 0:
            for p in pulses:
                a = abs(p[0])
                p[0] = (((a + half) >> sh) << sh) * (1 if p[0] > 0 else -1)
    return resid, events


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: wiring byte-identity dyn_run_q(never,sh=0) vs "
          "run_fabric ==")
    nchk = 0
    for name, lats in GRAMMARS + (("ladder@15",
                                    [round(i * 15 / (N - 1))
                                     for i in range(N)]),):
        for k in KS:
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=sd)["resid"]
                b, _ = dyn_run_q(static_fn(lats), k=k, seed=sd, sh=0,
                                 m_every=None)
                nchk += 1
                if a != b:
                    ok = False
                    print(f"  MISMATCH {name} K={k} seed={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} configs byte-identical")

    print("\n== CANARY b: anchors (run_fabric 5-seed means) ==")
    lad15 = [round(i * 15 / (N - 1)) for i in range(N)]
    for name, lats, k, wp, wd, we in (
            ("zero", [0] * N, 1, 77.3, 187834, 8756),
            ("ladder@15", lad15, 1, 71.5, 106378, 5792)):
        ps, ds, es = [], [], []
        for sd in SEEDS:
            d = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                           delta=DELTA, drift=DRIFT, seed=sd)
            ps.append(pct(d["resid"]))
            ds.append(d["mass"])
            es.append(d["events"])
        p, dd, ev = mean(ps), round(mean(ds)), round(mean(es))
        good = abs(p - wp) <= 0.2 and dd == wd and ev == we
        ok &= good
        print(f"  {name:<10} K=1: pct {p:6.1f} (want {wp})  debt {dd}"
              f" (want {wd})  ev {ev} (want {we})  -> "
              f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY c: structural no-op q=12 (sh=0) == M=never ==")
    c3 = True
    for name, lats in GRAMMARS:
        for m in (1, 16):
            a, _ = dyn_run_q(static_fn(lats), k=2, seed=42, sh=0,
                             m_every=m)
            b, _ = dyn_run_q(static_fn(lats), k=2, seed=42, sh=0,
                             m_every=None)
            if a != b:
                c3 = False
                print(f"  MISMATCH {name} M={m}")
    print(f"  {'PASS' if c3 else 'FAIL'}: 4 configs full-resid identical")
    ok &= c3

    print("\n== CANARY d: determinism (quantized cells, run twice) ==")
    c4 = True
    for (name, lats) in GRAMMARS:
        a, ea = dyn_run_q(static_fn(lats), k=1, seed=7, sh=4, m_every=1)
        b, eb = dyn_run_q(static_fn(lats), k=1, seed=7, sh=4, m_every=1)
        if (a != b) or (ea != eb):
            c4 = False
            print(f"  NONDETERMINISTIC {name}")
    print(f"  {'PASS' if c4 else 'FAIL'}: 2 dual runs byte-identical")
    return ok and c4


# ------------------------------------------------------------ panel
_cache = {}


def cell(lats, k, sh, m, tag):
    key = (tag, k, sh, m, tuple(lats))
    if key not in _cache:
        _cache[key] = mean([pct(dyn_run_q(static_fn(lats), k=k, seed=sd,
                                          sh=sh, m_every=m)[0])
                            for sd in SEEDS])
    return _cache[key]


def run_panel():
    print("\n== PANEL: pct (5-seed mean) per grammar x K x q x M ==")
    print("   grid: q6->step16  q8->step4  q12->step1(no-op); M=None "
          "never\n")
    res = {}
    for name, lats in GRAMMARS:
        for k in KS:
            print(f"-- {name}  K={k} --")
            print(f"{'q\\M':>6}" + "".join(f"{('M=' + str(m)):>9}"
                                           for m in MS))
            res[(name, k)] = {}
            for q in QS:
                row = [cell(lats, k, SH_OF[q], m, name) for m in MS]
                res[(name, k)][q] = dict(zip(MS, row))
                print(f"{'q=' + str(q):>6}"
                      + "".join(f"{v:>9.1f}" for v in row))
            sys.stdout.flush()
    return res


def verdict(res):
    print("\n== DECOHERENCE COSTS (pp vs M=never) ==")
    print(f"{'grammar':>10}{'K':>3}{'q':>4}"
          + "".join(f"{('M=' + str(m)):>9}" for m in MS))
    costs = {}
    for key, d in res.items():
        name, k = key
        for q in QS:
            row = [d[q][None] - d[q][m] for m in MS]
            costs[(name, k, q)] = row
            print(f"{name:>10}{k:>3}{q:>4}"
                  + "".join(f"{v:>9.1f}" for v in row))

    prim = costs[("zero", 1, 8)][0]
    print(f"\nPRIMARY cell: zero K=1 q=8 M=1  cost = {prim:.1f}pp")
    print("PRE-REGISTERED rule: <=5.0 VALIDATED (Zeno-inert, within-tick "
          "averaging holds);")
    print("                   >10.0 FALSIFIED (cross-tick wave memory "
          "supported); else MIXED.")
    v = ("VALIDATED" if prim <= 5.0
         else "FALSIFIED" if prim > 10.0 else "MIXED")
    print(f"-> VERDICT: {v}")

    sec = costs[("kcoh5@15", 1, 8)][0]
    print(f"secondary kcoh5@15 K=1 q=8 M=1 cost = {sec:.1f}pp")
    return v, prim, sec


def main():
    print(f"SPIN-30 dequant Zeno probe — pid {os.getpid()}, "
          f"{sys.version.split()[0]}")
    ok = canaries()
    print("\nCANARY GATE: " + ("ALL PASS" if ok else "FAIL — ABORT"))
    if not ok:
        sys.exit(1)
    res = run_panel()
    v, prim, sec = verdict(res)
    print("\nhead: verdict %s, primary cost %.1fpp, secondary %.1fpp"
          % (v, prim, sec))


if __name__ == "__main__":
    main()
