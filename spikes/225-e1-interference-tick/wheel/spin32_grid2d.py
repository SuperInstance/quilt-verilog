#!/usr/bin/env python3
"""SPIN-32 — METROLOGY (2D-grid spoke): the alpha(pd, delta) surface.

Casey directive: extensive experimentation, figure it out for real.
Dispatched from SPIN-31's next-spoke proposal (full 2D grid with model
competition pre-registered BEFORE running).

BACKGROUND (booked):
  SPIN-29: C = 2.381·delta at pd=3 (alpha = C/2delta ~ 1.19), but EXPERT
  adjudication: alpha is pd-coupled (pd=6 -> 0.977 at delta=12, -17%) and
  delta-coupled at fixed pd (pd=3: alpha RISES as delta shrinks below 12;
  pd=6: alpha FALLS).  pd=2: NO CROSSING (N=6 co-fire wall).
  SPIN-30: 2delta DEAD with or without drift.  At A=200: C = 27.22 +
  0.138·drift (drift-independent to first order); at drift=6:
  C = 45.20 - 2.11·log2(A), weak negative log-band term; A=96 x drift>=6
  corner ignites (alpha -> 1.398).  A=100 NOT integer-realizable at spec
  slope 1.6 (t_up=62.5) — scar pattern booked.
  SPIN-31: alpha(pd, delta=12) = 1.365 - 0.067·pd LINEAR (max|resid| 0.019,
  gate PASS) but pd=6 delta-replication alpha-spread 14.8% vs 10% gate FAIL
  — separable C = beta·2delta·g(pd) DEAD, cross term required.  7 cells
  measured; sign of d(alpha)/d(delta) FLIPS with pd (3: rises as delta
  shrinks; 6: falls).

HYPOTHESIS + MODEL COMPETITION (pre-registered BEFORE any panel run):
  alpha(pd, delta) is a smooth low-order surface over the 20-cell grid
  pd in {3,4,5,6} x delta in {8,10,12,14,16}.  Four competing closed
  forms, fitted by least squares to the 20 arm-mean alpha values:
    M1 bilinear-no-cross : alpha = a + b·pd + c·delta                (k=3)
    M2 bilinear-with-cross: alpha = a + b·pd + c·delta + d·pd·delta  (k=4)
    M3 separable product : alpha = (a + b·pd)·(e + f·delta)          (k=4)
    M4 saturation knee   : alpha = a + b·pd + s·max(0, pd - p0),
                           p0 fitted on grid {3.0..5.75 step 0.25}   (k=4)
  M3 is M2's linear span (1, pd, delta, pd·delta) minus one degree of
  freedom (constraint A0·A3 = A1·A2), so SSE(M3) >= SSE(M2) necessarily;
  AIC/BIC arbitrate whether the constraint's parsimony pays.  M2/M3
  fitted via OLS normal equations (M3: Gauss-Newton on (a,b,e,f),
  3 fixed starts, 40 iters, deterministic).
  Selection statistic: AIC = n·ln(SSE/n) + 2(k+1); BIC likewise
  (n = 20 arms, sigma counted in k).  Reported for all four.

PRE-REGISTERED DECISION RULE (fixed before any run):
  WINNER DECLARED iff BOTH:
    (W1) Delta-AIC >= 10 between winner and runner-up (AIC ordering);
    (W2) leave-one-arm-out cross-validation: refit on 19 arms, predict
         held-out arm; |pred - obs| <= 2·NF on >= 80% of arms (>= 16/20),
         where NF_arm = half the per-seed alpha range (3 seeds per arm,
         seeds 1/7/42) — the noise floor measured by this very spin —
         with the global median NF as fallback for arms whose per-seed
         crossings are undefined.
  If no model passes both: VERDICT = "NO SINGLE SURFACE (within reach)";
  best partial reported honestly.  If winner is M2 or M3, the surface
  closes: C(pd, delta) = 2·delta·alpha(pd, delta).

SECONDARY PRE-REGISTERED GATES:
  (R) SPIN-31 REPLICATION: the 14.8% delta-spread of alpha(pd=6) across
      delta in {8,12,16} must survive seed replication: recompute range
      of alpha(pd=6) over the 5-point delta column {8,10,12,14,16} and
      compare to 2·(median NF).  REAL if range > 2·median NF, NOISE if
      not.  Direction expectation (pre-registered): monotone RISING in
      delta (0.864 -> 1.005 over 8 -> 16 measured).
  (K) ENDPOINT CURVATURE: probes at corners pd in {3,6} x delta in {8,16}
      with 3 extra pd-points each: pd=3 corners get {2.5, 2.75, 3.5},
      pd=6 corners get {5.5, 5.75, 6.5}.  (Brief said "2.5, 3.5 / 5.5,
      6.5 where integer-realizable — else nearest and book it"; pd is
      integer-realizable at ANY rational via the generalized divider
      m = pdn·|e| // pdd, see below, so all half/quarter points are
      realizable; the third quarter-step point per corner is a
      pre-registered densification for a 3-point second difference.)
      Curvature test at pd=3: |alpha(3.5) - 2·alpha(3) + alpha(2.5)| vs
      2·NF -> LINEAR-CONTINUES or CURVES.  Same at pd=6 with 5.5/6.5.
      NO-CROSSING at pd in {2.5, 2.75} (wall-adjacent) is PRE-BOOKED as
      wall-location data, not failure: pd=2 shows no crossing.
  (P) PAYOFF: with winner alpha(pd, delta), combine SPIN-30's A/drift
      first-order terms (measured at pd=3, delta=12) into the candidate
      closed form  C(pd, delta, A, drift) ~= 2·delta·alpha_win(pd, delta)
        + 0.138·(drift - 6) - 2.11·log2(A/200),
      validity domain A >= 200, drift in [0,10], pd in [2.5, 6.5],
      delta in [8, 16]; A=96 x drift>=6 corner explicitly OUTSIDE
      (SPIN-30 ignition).  Cross-pd validity of the A/drift corrections
      is UNTESTED by this design and flagged.

DESIGN:
  Grid: pd in {3,4,5,6} x delta in {8,10,12,14,16} = 20 arms.
  Per arm: spread sweep 8..30 step 2 (12 points — SPIN-31's sweep,
  house-proven no clipping: max expected knee ~23.5 at pd=3/delta=16),
  K=1, N=6 ladder, slope 1.6 from SPEC (A=200, T_up=125, exact 200/125,
  SPIN-21 scar), drift=6, ticks=4800.  THREE seeds per arm (1/7/42) per
  brief — per-seed crossings give the per-arm noise floor NF_arm (the
  deliverable); 5-seed means retained ONLY inside canaries/anchors.
  Curvature probes: 4 corners x 3 pd-points, same sweep, 3 seeds.
  Run budget: 20·12·3 (grid) + 4·3·12·3 (probes) + canaries ~= 1,300
  fabric runs — cheap.

INSTRUMENT (new, canary-gated):
  dyn_run_r — verbatim clone of spin29's dyn_run with the pulse divider
  generalized to rational pd = pdn/pdd (pd is a DIVISOR):
  m = pdd*|e| // pdn or 1.
  For pdd == 1, pdn == 3 this reduces EXACTLY to dyn_run's m = |e| // pd
  (canary
  e: byte-identity on 4 configs x 2 seeds vs dyn_run AND run_fabric).
  Integer-only in-loop preserved for every rational pd used (all probes
  use pdn,pdd in small integers: 2.5=5/2, 2.75=11/4, 3.5=7/2, 5.5=11/2,
  5.75=23/4, 6.5=13/2).

CANARIES (unchanged from SPIN-29 suite, gate before any panel read):
  a. wiring byte-identity dyn_run vs exp_glm1.run_fabric, 16 configs,
     pd=3 AND pd=6 legs (pd is a swept knob; SPIN-31 standard).
  b. anchors (spin-10 semantics): ladder15 K=1 = 71.48 / 5791.6 /
     106378.4; zero K=1 = 77.26 / 8756.4 / 187833.6 (5-seed means).
  c. STOP-gate: delta=12 pd=3 5-seed replay must reproduce SPIN-31
     digit-for-digit: s* rounds to 17.6 and C=s*·1.6 rounds to 28.1.
  d. determinism: dual runs, ONE PER GRID ARM (20) + 2 probe arms.
  e. dyn_run_r(pdn=3,pdd=1) == dyn_run(pd=3) byte-identical, 4 configs
     x 2 seeds (probe-instrument wiring).

SCARS (pre-registered BEFORE running):
  - A=100 non-integer-realizable pattern (SPIN-30): any new (slope, A)
    pair needs t_up = A/slope integer.  Here A=200 fixed -> no exposure.
  - delta grid {8,10,12,14,16}: delta is an integer tolerance — all
    realizable by construction.  No delta-side exposure exists.
  - Rational-pd divider is a NEW instrument path (not run_fabric-
    testable at non-integer pd); covered by canary e at the integer
    reduction only.  Honest boundary, booked.
  - pd in {2.5, 2.75} wall-adjacent: no-crossing outcomes pre-booked
    as wall-mapping data; the pd=3-side curvature test survives on
    3.5 alone if 2.5/2.75 both die.
  - 3 seeds per arm (brief) < 5-seed house standard: NF estimates
    carry 3-sample statistics (2 dof); canaries stay 5-seed.
  - Single slope (1.6), single N (6), single drift (6), single band
    (A=200) by design — the surface is pd x delta ONLY; A/drift/N
    corrections ride on SPIN-30/other spokes, flagged in the payoff.

python3 -u direct redirect to spin32-output.txt; unique filename
(SPIN-30 collision scar).  No pipes.  Integer-only inside every loop;
floats only at print/stat time.
"""
import math
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spin29_metrology_cdelta import (dyn_run, static_fn, ladder, S16, pct,
                                     crossing, mean, SEEDS, SPEC_SLOPE,
                                     DRIFT, TICKS, r0, N)
from exp_glm1 import run_fabric, LCG

PDS = (3, 4, 5, 6)
DELTAS = (8, 10, 12, 14, 16)
SPREADS32 = tuple(range(8, 31, 2))       # 12 points, SPIN-31's sweep
SEEDS3 = (1, 7, 42)                      # 3 seeds per arm, per brief
DRIFT32 = DRIFT                          # 6
T0 = time.time()

# probe corners: (pd_anchor, [(pdn, pdd), ...]) at delta in {8, 16}
PROBES = [
    (3, [(5, 2), (11, 4), (7, 2)]),      # 2.5, 2.75, 3.5
    (6, [(11, 2), (23, 4), (13, 2)]),    # 5.5, 5.75, 6.5
]
PROBE_DELTAS = (8, 16)


# ------------------------------------------------------------ instrument
def dyn_run_r(lats_fn, reality_fn, ticks=TICKS, k=1, pdn=3, pdd=1,
              delta=12, drift=DRIFT32, seed=42):
    """spin29 dyn_run clone; pulse divider generalized to pd = pdn/pdd
    (a DIVISOR):  m = pdd*|e| // pdn or 1.  For pdn=3, pdd=1 this is
    exactly m = |e| // 3 == dyn_run(pd=3) — canary e proves it."""
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
            m = pdd * abs(e) // pdn or 1
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


def curve(delta, pd, seed):
    return [pct(dyn_run(static_fn(ladder(s)), S16[1], k=1, delta=delta,
                        pd=pd, seed=seed), delta=delta)
            for s in SPREADS32]


def curve_r(delta, pdn, pdd, seed):
    return [pct(dyn_run_r(static_fn(ladder(s)), S16[1], k=1, pdn=pdn,
                          pdd=pdd, delta=delta, seed=seed), delta=delta)
            for s in SPREADS32]


# ------------------------------------------------------------ linear alg
def solve(A, b):
    """Gaussian elimination w/ partial pivoting; deterministic."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-12:
            return None
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n + 1):
                M[r][k] -= f * M[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (M[r][n] - sum(M[r][k] * x[k] for k in range(r + 1, n)))
        x[r] /= M[r][r]
    return x


def ols(X, y):
    """least squares beta for y ~ X·beta; X rows are basis vectors."""
    k = len(X[0])
    A = [[sum(X[i][a] * X[i][b] for i in range(len(X))) for b in range(k)]
         for a in range(k)]
    bvec = [sum(X[i][a] * y[i] for i in range(len(X))) for a in range(k)]
    return solve(A, bvec)


def sse(X, y, beta):
    return sum((y[i] - sum(X[i][j] * beta[j] for j in range(len(beta))))
               ** 2 for i in range(len(X)))


# ------------------------------------------------------------ models
def basis_m1(pts):
    return [[1.0, p, d] for p, d in pts]


def basis_m2(pts):
    return [[1.0, p, d, p * d] for p, d in pts]


def fit_m3(pts, y):
    """Gauss-Newton on alpha = (a + b·pd)(e + f·delta); deterministic
    fixed starts, 40 iterations, best SSE wins."""
    best = None

    def gn(a, b, e, f):
        for _ in range(40):
            r = [y[i] - (a + b * pts[i][0]) * (e + f * pts[i][1])
                 for i in range(len(y))]
            J = []
            for p, d in pts:
                J.append([e + f * d, p * (e + f * d), a + b * p,
                          d * (a + b * p)])
            JTJ = [[sum(J[i][u] * J[i][v] for i in range(len(y)))
                    for v in range(4)] for u in range(4)]
            JTr = [sum(J[i][u] * r[i] for i in range(len(y)))
                   for u in range(4)]
            dlt = solve(JTJ, JTr)
            if dlt is None:
                break
            a2, b2, e2, f2 = (a + dlt[0], b + dlt[1], e + dlt[2],
                              f + dlt[3])
            r2 = [y[i] - (a2 + b2 * pts[i][0]) * (e2 + f2 * pts[i][1])
                  for i in range(len(y))]
            if sum(x * x for x in r2) > sum(x * x for x in r) - 1e-14:
                break
            a, b, e, f = a2, b2, e2, f2
        cur = sum(((a + b * pts[i][0]) * (e + f * pts[i][1]) - y[i]) ** 2
                  for i in range(len(y)))
        return cur, (a, b, e, f)

    for start in ((1.0, -0.05, 1.0, 0.005), (1.4, -0.07, 0.9, 0.004),
                  (0.8, -0.03, 1.2, 0.01)):
        s, par = gn(*start)
        if best is None or s < best[0] - 1e-15:
            best = (s, par)

    def predict(pd, d, par=best[1]):
        a, b, e, f = par
        return (a + b * pd) * (e + f * d)

    return predict, best[1], best[0]


def fit_m4(pts, y):
    """alpha = a + b·pd + s·max(0, pd - p0); p0 on pre-registered grid."""
    best = None
    for p0i in range(12):
        p0 = 3.0 + 0.25 * p0i
        X = [[1.0, p, max(0.0, p - p0)] for p, d in pts]
        beta = ols(X, y)
        if beta is None:      # degenerate knee (e.g. p0=3.0 -> collinear)
            continue
        s = sse(X, y, beta)
        if best is None or s < best[0] - 1e-15:
            best = (s, p0, beta)

    def predict(pd, d, p0=best[1], beta=best[2]):
        return beta[0] + beta[1] * pd + beta[2] * max(0.0, pd - p0)

    return predict, (best[1], best[2]), best[0]


def aic(n, sse_v, k):
    return n * (1.0 if sse_v <= 0 else math.log(sse_v / n)) + 2 * (k + 1)


def bic(n, sse_v, k):
    return n * (1.0 if sse_v <= 0 else math.log(sse_v / n)) \
        + (k + 1) * math.log(n)


# ------------------------------------------------------------ canaries
def canaries():
    ok = True

    print("== CANARY a: wiring byte-identity dyn_run vs run_fabric "
          "(pd=3 AND pd=6 legs) ==")
    nchk = 0
    a_ok = True
    for name, lats in (("zero", [0] * N), ("ladder@30", ladder(30)),
                       ("ladder@14", ladder(14)),
                       ("cohort", [0, 0, 0, 30, 30, 30])):
        for pd in (3, 6):
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=1, pd=pd,
                               delta=12, drift=DRIFT32, seed=sd)["resid"]
                b = dyn_run(static_fn(lats), r0, k=1, pd=pd, seed=sd)
                nchk += 1
                if a != b:
                    a_ok = False
                    print(f"  MISMATCH {name} pd={pd} seed={sd}")
    print(f"  {'PASS' if a_ok else 'FAIL'}: {nchk} configs byte-identical")
    ok &= a_ok

    print("\n== CANARY b: R0 anchors at delta=12 pd=3 (5-seed means) ==")
    tot_ev = tot_m = 0
    rs = []
    for sd in SEEDS:
        r = run_fabric("interference", TICKS, ladder(15), K=1, pd=3,
                       delta=12, drift=DRIFT32, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn(ladder(15)), r0, k=1, pd=3,
                              seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b1 = (abs(p - 71.48) <= 0.05 and abs(ev - 5791.6) <= 0.5
          and abs(m - 106378.4) <= 0.5)
    print(f"  ladder15 K=1: pct={p:.2f} (71.48)  ev={ev:.1f} (5791.6)  "
          f"debt={m:.1f} (106378.4)  -> {'PASS' if b1 else 'FAIL'}")
    tot_ev = tot_m = 0
    rs = []
    for sd in SEEDS:
        r = run_fabric("interference", TICKS, [0] * N, K=1, pd=3,
                       delta=12, drift=DRIFT32, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn([0] * N), r0, k=1, pd=3, seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b2 = (abs(p - 77.26) <= 0.05 and abs(ev - 8756.4) <= 0.5
          and abs(m - 187833.6) <= 0.5)
    print(f"  zero    K=1: pct={p:.2f} (77.26)  ev={ev:.1f} (8756.4)  "
          f"debt={m:.1f} (187833.6)  -> {'PASS' if b2 else 'FAIL'}")
    ok &= b1 and b2

    print("\n== CANARY c: STOP-gate delta=12 pd=3 replay (5-seed): "
          "s*->17.6, C->28.1 digit-for-digit ==")
    pcts = [mean([pct(dyn_run(static_fn(ladder(s)), S16[1], k=1, delta=12,
                               pd=3, seed=sd), delta=12)
                  for sd in SEEDS]) for s in SPREADS32]
    cx = crossing(pcts, spreads=SPREADS32)
    C = cx * SPEC_SLOPE
    c_ok = round(cx, 1) == 17.6 and round(C, 1) == 28.1
    print("  curve: " + " ".join(f"{p:.1f}" for p in pcts))
    print(f"  s*={cx:.3f} (round {round(cx,1)}, want 17.6)  "
          f"C={C:.3f} (round {round(C,1)}, want 28.1)"
          f"  -> {'PASS' if c_ok else 'FAIL'}")
    ok &= c_ok

    print("\n== CANARY d: determinism (one dual-run per grid arm + 2 "
          "probe arms) ==")
    d_ok = True
    n2 = 0
    for pd in PDS:
        for dlt in DELTAS:
            a = dyn_run(static_fn(ladder(16)), S16[1], k=1, delta=dlt,
                        pd=pd, seed=42)
            b = dyn_run(static_fn(ladder(16)), S16[1], k=1, delta=dlt,
                        pd=pd, seed=42)
            n2 += 1
            if a != b:
                d_ok = False
                print(f"  NONDETERMINISTIC pd={pd} delta={dlt}")
    for pdn, pdd in ((5, 2), (13, 2)):
        a = dyn_run_r(static_fn(ladder(16)), S16[1], k=1, pdn=pdn,
                      pdd=pdd, delta=12, seed=42)
        b = dyn_run_r(static_fn(ladder(16)), S16[1], k=1, pdn=pdn,
                      pdd=pdd, delta=12, seed=42)
        n2 += 1
        if a != b:
            d_ok = False
            print(f"  NONDETERMINISTIC pdn={pdn}/{pdd}")
    print(f"  {'PASS' if d_ok else 'FAIL'}: {n2} dual runs byte-identical")
    ok &= d_ok

    print("\n== CANARY e: dyn_run_r(pdn=3,pdd=1) == dyn_run(pd=3) "
          "byte-identity ==")
    e_ok = True
    ne = 0
    for name, lats in (("zero", [0] * N), ("ladder@30", ladder(30)),
                       ("ladder@14", ladder(14)),
                       ("cohort", [0, 0, 0, 30, 30, 30])):
        for sd in (1, 42):
            a = dyn_run(static_fn(lats), S16[1], k=1, pd=3, delta=12,
                        seed=sd)
            b = dyn_run_r(static_fn(lats), S16[1], k=1, pdn=3, pdd=1,
                          delta=12, seed=sd)
            ne += 1
            if a != b:
                e_ok = False
                print(f"  MISMATCH {name} seed={sd}")
    print(f"  {'PASS' if e_ok else 'FAIL'}: {ne} configs byte-identical")
    ok &= e_ok
    return ok


# ------------------------------------------------------------ panels
def grid_panel():
    print("\n== PANEL 1: 20-arm grid, 3 seeds/arm, K=1, slope 1.6 spec ==")
    print("arm = pd x delta; per-seed alpha from per-seed crossings; "
          "NF_arm = half per-seed alpha range")
    print(f"{'pd':>3}{'delta':>7}   s*      C   alpha  "
          f"|  per-seed alphas (s1,s7,s42)        NF")
    out = {}
    for pd in PDS:
        for dlt in DELTAS:
            curves = {sd: curve(dlt, pd, sd) for sd in SEEDS3}
            mean_c = [mean([curves[sd][i] for sd in SEEDS3])
                      for i in range(len(SPREADS32))]
            x = crossing(mean_c, spreads=SPREADS32)
            seed_al = []
            for sd in SEEDS3:
                xs = crossing(curves[sd], spreads=SPREADS32)
                seed_al.append(None if xs is None
                               else xs * SPEC_SLOPE / (2 * dlt))
            if x is None:
                print(f"{pd:>3}{dlt:>7}   NO CROSSING")
                out[(pd, dlt)] = None
                continue
            C = x * SPEC_SLOPE
            al = C / (2 * dlt)
            defin = [v for v in seed_al if v is not None]
            if len(defin) == 3:
                nf = (max(defin) - min(defin)) / 2
                nf_s = f"{nf:.3f}"
            else:
                nf = None
                nf_s = "n/a"
            out[(pd, dlt)] = (x, C, al, seed_al, nf)
            sstr = " ".join("  ----" if v is None else f"{v:.3f}"
                            for v in seed_al)
            print(f"{pd:>3}{dlt:>7} {x:6.1f} {C:6.1f} {al:6.3f}  "
                  f"| {sstr}   {nf_s}")
            sys.stdout.flush()
    return out


def probe_panel():
    print("\n== PANEL 2: endpoint curvature probes (rational pd), "
          "3 seeds/arm ==")
    print(f"{'pd':>6}{'delta':>7}   s*      C   alpha  per-seed alphas")
    out = {}
    for anchor, plist in PROBES:
        for dlt in PROBE_DELTAS:
            for pdn, pdd in plist:
                label = f"{pdn}/{pdd}"
                curves = {sd: curve_r(dlt, pdn, pdd, sd) for sd in SEEDS3}
                mean_c = [mean([curves[sd][i] for sd in SEEDS3])
                          for i in range(len(SPREADS32))]
                x = crossing(mean_c, spreads=SPREADS32)
                seed_al = []
                for sd in SEEDS3:
                    xs = crossing(curves[sd], spreads=SPREADS32)
                    seed_al.append(None if xs is None
                                   else xs * SPEC_SLOPE / (2 * dlt))
                if x is None:
                    print(f"{label:>6}{dlt:>7}   NO CROSSING "
                          "(wall-adjacent, pre-booked)")
                    out[(label, dlt)] = None
                    continue
                C = x * SPEC_SLOPE
                al = C / (2 * dlt)
                out[(label, dlt)] = (x, C, al, seed_al)
                sstr = " ".join("  ----" if v is None else f"{v:.3f}"
                                for v in seed_al)
                print(f"{label:>6}{dlt:>7} {x:6.1f} {C:6.1f} {al:6.3f}"
                      f"  {sstr}")
                sys.stdout.flush()
    return out


# ------------------------------------------------------------ analysis
def model_competition(grid):
    pts, ys, nfs, keys = [], [], [], []
    for pd in PDS:
        for dlt in DELTAS:
            v = grid[(pd, dlt)]
            if v is None:
                continue
            pts.append((float(pd), float(dlt)))
            ys.append(v[2])
            nfs.append(v[4])
            keys.append((pd, dlt))
    n = len(pts)
    nfs_def = sorted(v for v in nfs if v is not None)
    med_nf = nfs_def[len(nfs_def) // 2] if nfs_def else 0.02
    med_nf = max(med_nf, 0.005)
    print(f"\n== ANALYSIS 1: model competition on {n} arm-mean alphas ==")
    print(f"noise floor: median NF_arm = {med_nf:.4f} (half per-seed "
          f"range); per-arm NF used where defined")

    # M1 / M2 via OLS
    b1 = ols(basis_m1(pts), ys)
    s1 = sse(basis_m1(pts), ys, b1)
    b2 = ols(basis_m2(pts), ys)
    s2 = sse(basis_m2(pts), ys, b2)
    pred3, par3, s3 = fit_m3(pts, ys)
    pred4, par4, s4 = fit_m4(pts, ys)

    def pred_m1(pd, d, b=b1):
        return b[0] + b[1] * pd + b[2] * d

    def pred_m2(pd, d, b=b2):
        return b[0] + b[1] * pd + b[2] * d + b[3] * pd * d

    models = [
        ("M1 bilinear-no-cross", pred_m1, s1, 3),
        ("M2 bilinear-with-cross", pred_m2, s2, 4),
        ("M3 separable-product", pred3, s3, 4),
        ("M4 saturation-knee", pred4, s4, 4),
    ]
    print(f"{'model':<24}{'SSE':>9}{'maxres':>8}{'AIC':>9}{'BIC':>9}")
    scored = []
    for name, pf, s, k in models:
        a_v = aic(n, s, k)
        b_v = bic(n, s, k)
        mr = max(abs(pf(pd, d) - ys[i]) for i, (pd, d) in enumerate(pts))
        scored.append((a_v, name, pf, s, k, b_v, mr))
        print(f"{name:<24}{s:9.4f}{mr:8.4f}{a_v:9.2f}{b_v:9.2f}")
    scored.sort()
    winner, runner = scored[0], scored[1]
    daic = runner[0] - winner[0]
    print(f"\nAIC order: {scored[0][1]} < {scored[1][1]} < ... "
          f"Delta-AIC(winner vs runner-up) = {daic:.2f} "
          f"(gate >= 10) -> W1 {'PASS' if daic >= 10 else 'FAIL'}")

    # LOO
    print("\nleave-one-arm-out CV (gate: |err| <= 2·NF on >= 80% arms):")
    loo_pass = {}
    for _a, name, _pf, _s, _k, _b, _mr in scored:
        npass = 0
        errs = []
        for j in range(n):
            tr_pts = pts[:j] + pts[j + 1:]
            tr_ys = ys[:j] + ys[j + 1:]
            if name.startswith("M1"):
                bb = ols(basis_m1(tr_pts), tr_ys)
                pr = bb[0] + bb[1] * pts[j][0] + bb[2] * pts[j][1]
            elif name.startswith("M2"):
                bb = ols(basis_m2(tr_pts), tr_ys)
                pr = (bb[0] + bb[1] * pts[j][0] + bb[2] * pts[j][1]
                      + bb[3] * pts[j][0] * pts[j][1])
            elif name.startswith("M3"):
                pf3, _, _ = fit_m3(tr_pts, tr_ys)
                pr = pf3(pts[j][0], pts[j][1])
            else:
                pf4, _, _ = fit_m4(tr_pts, tr_ys)
                pr = pf4(pts[j][0], pts[j][1])
            nf = nfs[j] if nfs[j] is not None else med_nf
            e = abs(pr - ys[j])
            errs.append(e)
            if e <= 2 * nf:
                npass += 1
        loo_pass[name] = (npass, npass / n, max(errs))
        print(f"  {name:<24} pass {npass}/{n} ({npass/n*100:.0f}%)  "
              f"max|err|={max(errs):.4f}")
    wname = winner[1]
    w2 = loo_pass[wname][1] >= 0.80
    print(f"W2 (winner LOO >= 80%): {'PASS' if w2 else 'FAIL'} "
          f"({loo_pass[wname][0]}/{n})")

    verdict = ("WINNER: " + wname if (daic >= 10 and w2)
               else "NO SINGLE SURFACE (gates not both met)")
    print(f"MODEL VERDICT: {verdict}")

    # residual structure of the top-2 models by pd-row / delta-col
    print("\nwinner-fit residuals by arm (pd, delta): pred - obs")
    pf = winner[2]
    for i, (pd, d) in enumerate(pts):
        print(f"  pd={pd} delta={d:>2}: {pf(pd, d) - ys[i]:+.4f}"
              f"  (obs {ys[i]:.3f})")

    # winning params
    if wname.startswith("M2"):
        print(f"\nM2 coefficients: alpha = {b2[0]:.4f} {b2[1]:+.5f}·pd "
              f"{b2[2]:+.5f}·delta {b2[3]:+.6f}·pd·delta")
    elif wname.startswith("M1"):
        print(f"\nM1 coefficients: alpha = {b1[0]:.4f} {b1[1]:+.5f}·pd "
              f"{b1[2]:+.5f}·delta")
    elif wname.startswith("M3"):
        a, b, e, f = par3
        print(f"\nM3 coefficients: alpha = ({a:.4f} {b:+.5f}·pd)·"
              f"({e:.4f} {f:+.6f}·delta)")
    else:
        print(f"\nM4: p0={par4[0]:.2f}  a={par4[1][0]:.4f} "
              f"b={par4[1][1]:+.5f} s={par4[1][2]:+.5f}")
    return verdict, winner, med_nf, pts, ys, nfs, keys


def replication_gate(grid, med_nf):
    print("\n== ANALYSIS 2: SPIN-31 replication — alpha(pd=6) over 5-point"
          " delta column ==")
    vals = {}
    for dlt in DELTAS:
        v = grid[(6, dlt)]
        if v:
            vals[dlt] = v[2]
    s = "  ".join(f"d{d}={a:.3f}" for d, a in vals.items())
    if len(vals) >= 2:
        rng = max(vals.values()) - min(vals.values())
        mn = mean(list(vals.values()))
        gate = 2 * med_nf
        print(f"  {s}")
        print(f"  range={rng:.3f} ({rng/mn*100:.1f}% of mean {mn:.3f}); "
              f"gate range > 2·medianNF = {gate:.3f} -> "
              f"{'REAL (survives seed replication)' if rng > gate else 'NOISE'}")
        mono = all(vals[DELTAS[i]] < vals[DELTAS[i + 1]]
                   for i in range(len(DELTAS) - 1)
                   if DELTAS[i] in vals and DELTAS[i + 1] in vals)
        print(f"  monotone rising in delta (pre-registered expectation): "
              f"{'YES' if mono else 'NO'}")
        return rng > gate, rng, mn
    print("  insufficient crossings")
    return None, None, None


def curvature_gate(grid, probes, med_nf):
    print("\n== ANALYSIS 3: endpoint curvature (gate 2·medianNF on "
          "second difference) ==")
    res = {}
    for anchor, plist in PROBES:
        for dlt in PROBE_DELTAS:
            key_mid = (anchor, dlt)
            if grid.get(key_mid) is None:
                continue
            a_mid = grid[key_mid][2]
            lo_lbl = "5/2" if anchor == 3 else "11/2"
            hi_lbl = "7/2" if anchor == 3 else "13/2"
            q_lbl = "11/4" if anchor == 3 else "23/4"
            lo = probes.get((lo_lbl, dlt))
            hi = probes.get((hi_lbl, dlt))
            q = probes.get((q_lbl, dlt))
            lo_a = lo[2] if lo else None
            hi_a = hi[2] if hi else None
            q_a = q[2] if q else None
            lo_pd = float(lo_lbl.split("/")[0]) / float(lo_lbl.split("/")[1])
            hi_pd = float(hi_lbl.split("/")[0]) / float(hi_lbl.split("/")[1])
            print(f"  pd={anchor}, delta={dlt}: "
                  f"alpha({lo_pd:.2f})={lo_a}  alpha({anchor})={a_mid:.3f}  "
                  f"alpha({hi_pd:.2f})={hi_a}  quarter={q_a}")
            if lo_a is not None and hi_a is not None:
                sd2 = hi_a - 2 * a_mid + lo_a
                gate = 2 * med_nf
                tag = ("CURVES (2nd diff beyond noise)" if abs(sd2) > gate
                       else "LINEAR-CONTINUES (2nd diff within noise)")
                print(f"    second difference = {sd2:+.4f} vs gate "
                      f"{gate:.3f} -> {tag}")
                res[(anchor, dlt)] = (sd2, tag)
            else:
                print("    (lo or hi no crossing — wall side dropped, "
                      "pre-booked)")
                res[(anchor, dlt)] = None
    return res


def payoff(verdict, winner, grid):
    print("\n== ANALYSIS 4: PAYOFF — candidate closed form "
          "C(pd, delta, A, drift) ==")
    wname = winner[1]
    pf = winner[2]
    print(f"  winning surface: {wname}")
    print("  C(pd, delta) = 2·delta·alpha_win(pd, delta) at A=200, "
          "drift=6, N=6, slope 1.6:")
    for pd in PDS:
        row = []
        for dlt in DELTAS:
            row.append(f"{2*dlt*pf(float(pd), float(dlt)):5.1f}")
        print(f"    pd={pd}: " + " ".join(row))
    print("  joint candidate law (partial, pre-registered form):")
    print("    C(pd, delta, A, drift) ~= 2·delta·alpha_win(pd, delta)")
    print("        + 0.138·(drift - 6) - 2.11·log2(A/200)")
    print("  validity domain: A>=200, drift in [0,10], pd in [2.5,6.5] "
          "(wall-adjacent cells excluded), delta in [8,16], N=6, K=1,")
    print("  slope 1.6; A=96 x drift>=6 ignition corner OUTSIDE "
          "(SPIN-30); A/drift corrections measured at pd=3, delta=12 "
          "ONLY — cross-pd validity untested, flagged.")
    if (verdict.startswith("WINNER")
            and (wname.startswith("M2") or wname.startswith("M3"))):
        print("  closure status: SINGLE CLOSED FORM (pd, delta) pinned "
              "by this spin; A/drift/N terms partial.")
    else:
        print("  closure status: no single pd x delta surface passed "
              "gates; law remains open — partial only.")


def main():
    print("SPIN-32 METROLOGY 2D grid —", time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} ladder, K=1, slope 1.6 spec (200/125), "
          f"spreads={list(SPREADS32)}, grid pd{PDS} x delta{DELTAS}, "
          f"3 seeds/arm {SEEDS3}, probes rational-pd {PROBES} at "
          f"delta{PROBE_DELTAS}, ticks={TICKS}, drift={DRIFT32}")
    print("PRE-REGISTERED: M1-M4 competition, AIC Delta>=10 + LOO<=2NF "
          "80%; SPIN-31 14.8% replication gate; curvature 2nd-diff gate; "
          "payoff joint law C ~ 2d·alpha + drift/A corrections.")

    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    sys.stdout.flush()
    if not ok:
        sys.exit(1)

    grid = grid_panel()
    probes = probe_panel()
    verdict, winner, med_nf, pts, ys, nfs, keys = model_competition(grid)
    replication_gate(grid, med_nf)
    curvature_gate(grid, probes, med_nf)
    payoff(verdict, winner, grid)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
