#!/usr/bin/env python3
"""SPIN-40 — METROLOGY (pd x delta interaction spoke): map the alpha(pd,delta)
knee surface SPIN-31 discovered.

BACKGROUND (booked):
  SPIN-31 at delta=12: alpha(pd) = 1.365 - 0.067·pd linear (max|resid| 0.019),
  BUT separable C = beta·(2·delta)·g(pd) is DEAD: at pd=6 alpha rises with
  delta (0.864 -> 0.977 -> 1.005 over delta 8/12/16, 14.8% spread, 10% gate
  blown), while at pd=3 alpha RISES as delta shrinks below 12 (1.172 -> 1.247
  at delta=8, spin-29 adjudicator leg 2). The delta-coupling sign FLIPS
  across pd. This spin builds the full interaction grid.

HYPOTHESES (pre-registered BEFORE any panel run):
  H1 (interaction plane): alpha(pd, delta) = a - b·pd - c·(delta-12) fits
      all crossing cells with max |residual| <= 0.03 (3x the ~0.01
      last-digit noise in alpha). FALSIFY H1 if any cell's residual exceeds
      0.03, or no plane fits (fit degenerate / too few cells).
      Secondary EXPLORATORY (pre-registered, does NOT rescue H1): bilinear
      alpha = a + b·pd + c·(delta-12) + d·pd·(delta-12) — report whether
      the cross term absorbs what the plane misses.
  H2 (sign-flip boundary): the boundary pd_flip where d(alpha)/d(delta)
      changes sign moves predictably with pd — i.e. the local delta-slope
      m(pd) = dalpha/ddelta (linear fit within each pd column) is a
      monotone, well-fit function of pd; fit m(pd) = m0 + m1·pd and state
      pd_flip = -m0/m1 (formula). FALSIFY H2 if the flip is noise:
      bootstrap by seed (per-seed alpha grids recomputed from the same
      per-seed curves) — if the SIGN of m(pd) at the extreme pd columns
      (pd=3 vs pd=6) is not stable across a majority of the 5 single-seed
      replicates, the flip is noise and H2 falls.
  No-crossing cells (if any): reported as NO CROSSING, never extrapolated.
      If any full pd column has no crossings, both hypotheses degrade to
      the surviving columns; if fewer than 2 surviving columns, INCONCLUSIVE.

DESIGN: N=6 ladder, K=1, slope 1.6 from SPEC (A=200, T_up=125, exact
200/125 — SPIN-21 scar), grid pd in {3,4,5,6} x delta in {8,10,12,16,20}
(20 cells), spread sweep 8..40 step 2 (17 points — spin-29's pre-widened
sweep; the pd=3/delta=20 knee ~29.7 would clip an 8..30 sweep), drift=6,
ticks=4800, seeds 1/7/42/1999/20260902 (5-seed means + per-seed bootstrap
curves), statistic 50%-residency crossing by linear interpolation
(SPIN-21/27), C = s*·1.6, alpha = C/(2·delta).

CANARIES (all must pass before any panel read; abort on fail):
  a. wiring byte-identity >= 8 configs dyn_run vs exp_glm1.run_fabric,
     spanning BOTH knobs (pd in {3,6} x delta in {8,20}).
  b. anchors (spin-10 semantics): zero@15 K=1 = 77.3 / ev 8756 / debt
     187834; ladder@15 K=1 = 71.5 / ev 5792 / debt 106378.
  c. SPIN-31 replays at delta=12: pd=3 s* ~= 17.9 (measured 17.6, tol
     1.0); alpha(pd=4/5/6) matches SPIN-31's BOOKED measured values
     1.096/1.012/0.977 within 0.01 (brief quoted 1.119/1.052/0.985 —
     those are NOT the booked SPIN-31 measurements; gating on the md's
     table, discrepancy flagged in the report).
  d. double-run determinism (dual runs byte-identical, >= 2 grid corners).

Integer-only inside every loop; floats only at print/stat time.
Instrument: dyn_run verbatim-imported from spin29_metrology_cdelta
(spin27's clone of spin21's canary-proven inline run_fabric arm), exactly
as SPIN-31 imported it. python3 -u direct redirect to spin40-output.txt;
unique filename (SPIN-30 collision scar). No pipes.
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spin29_metrology_cdelta import (dyn_run, static_fn, ladder, S16, pct,
                                     crossing, mean, SEEDS, SPEC_SLOPE,
                                     DRIFT, TICKS, r0)
from exp_glm1 import run_fabric

PDS = (3, 4, 5, 6)
DELTAS = (8, 10, 12, 16, 20)
N = 6
T0 = time.time()
SPREADS_40 = tuple(range(8, 41, 2))   # 8..40 step 2, 17 points (spin-29 sweep)
ALPHA31 = {3: 1.172, 4: 1.096, 5: 1.012, 6: 0.977}   # booked SPIN-31 @ d12


def cell_curves(pd, delta):
    """Per-seed pct curves for one grid cell: list of 5 lists (per seed)."""
    return [[pct(dyn_run(static_fn(ladder(s)), S16[1], k=1, delta=delta,
                         pd=pd, seed=sd), delta=delta) for s in SPREADS_40]
            for sd in SEEDS]


# ------------------------------------------------------------ canaries
def canaries():
    ok = True

    print("== CANARY a: wiring byte-identity dyn_run vs run_fabric "
          "(pd x delta corners) ==")
    nchk = 0
    a_ok = True
    for name, lats in (("zero", [0] * N), ("ladder@30", ladder(30)),
                       ("ladder@14", ladder(14)),
                       ("cohort", [0, 0, 0, 30, 30, 30])):
        for pd in (3, 6):
            for dlt in (8, 20):
                a = run_fabric("interference", TICKS, lats, K=1, pd=pd,
                               delta=dlt, drift=DRIFT, seed=42)["resid"]
                b = dyn_run(static_fn(lats), r0, k=1, pd=pd, delta=dlt,
                            seed=42)
                nchk += 1
                if a != b:
                    a_ok = False
                    print(f"  MISMATCH {name} pd={pd} delta={dlt}")
    print(f"  {'PASS' if a_ok else 'FAIL'}: {nchk} configs byte-identical")
    ok &= a_ok

    print("\n== CANARY b: R0 anchors at delta=12 pd=3 (5-seed means) ==")
    tot_ev = tot_m = 0
    rs = []
    for sd in SEEDS:
        r = run_fabric("interference", TICKS, ladder(15), K=1, pd=3,
                       delta=12, drift=DRIFT, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn(ladder(15)), r0, k=1, pd=3,
                              seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b1 = (abs(p - 71.5) <= 0.05 and abs(ev - 5792) <= 0.5
          and abs(m - 106378) <= 0.5)
    print(f"  ladder15 K=1: pct={p:.2f} (71.5)  ev={ev:.1f} (5792)  "
          f"debt={m:.1f} (106378)  -> {'PASS' if b1 else 'FAIL'}")
    tot_ev = tot_m = 0
    rs = []
    for sd in SEEDS:
        r = run_fabric("interference", TICKS, [0] * N, K=1, pd=3,
                       delta=12, drift=DRIFT, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn([0] * N), r0, k=1, pd=3,
                              seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b2 = abs(p - 77.3) <= 0.05 and abs(ev - 8756) <= 0.5 \
        and abs(m - 187834) <= 0.5
    print(f"  zero    K=1: pct={p:.2f} (77.3)  ev={ev:.1f} (8756)  "
          f"debt={m:.1f} (187834)  -> {'PASS' if b2 else 'FAIL'}")
    ok &= b1 and b2

    print("\n== CANARY c: SPIN-31 replay at delta=12 (s*~=17.9 tol 1.0; "
          "alpha within 0.01 of booked 1.096/1.012/0.977) ==")
    c_ok = True
    for pd in PDS:
        cur = cell_curves(pd, 12)
        mcurve = [mean([c[i] for c in cur]) for i in range(len(SPREADS_40))]
        x = crossing(mcurve, spreads=SPREADS_40)
        if x is None:
            print(f"  pd={pd}: NO CROSSING (canary FAIL)")
            c_ok = False
            continue
        alpha = x * SPEC_SLOPE / 24.0
        if pd == 3:
            good = abs(x - 17.9) <= 1.0
            print(f"  pd=3 : s*={x:.1f} (want ~17.9 tol 1.0)"
                  f"  -> {'PASS' if good else 'FAIL'}")
        else:
            good = abs(alpha - ALPHA31[pd]) <= 0.01
            print(f"  pd={pd}: alpha={alpha:.3f} (booked {ALPHA31[pd]:.3f}, "
                  f"brief { {4:1.119,5:1.052,6:0.985}[pd]:.3f})  "
                  f"-> {'PASS' if good else 'FAIL'}")
        c_ok &= good
    ok &= c_ok

    print("\n== CANARY d: determinism (dual runs, grid corners) ==")
    d_ok = True
    n2 = 0
    for pd in (3, 6):
        for dlt in (8, 20):
            for s in (8, 24, 40):
                a = dyn_run(static_fn(ladder(s)), S16[1], k=1, delta=dlt,
                            pd=pd, seed=42)
                b = dyn_run(static_fn(ladder(s)), S16[1], k=1, delta=dlt,
                            pd=pd, seed=42)
                n2 += 1
                if a != b:
                    d_ok = False
                    print(f"  NONDETERMINISTIC pd={pd} d={dlt} s={s}")
    print(f"  {'PASS' if d_ok else 'FAIL'}: {n2} dual runs byte-identical")
    ok &= d_ok
    return ok


# ------------------------------------------------------------ grid
def run_grid():
    """Returns grid[pd][delta] = (mean_curve, mean_crossing or None)."""
    print("\n== GRID: pd x delta, slope 1.6, K=1, s* and C and alpha ==")
    hdr = f"{'pd':>3}{'d':>4}" + "".join(f"{s:>6}" for s in SPREADS_40) \
        + "   s*      C   alpha"
    print(hdr)
    grid = {}
    curves = {}
    for pd in PDS:
        for dlt in DELTAS:
            cur = cell_curves(pd, dlt)
            curves[(pd, dlt)] = cur
            mcurve = [mean([c[i] for c in cur]) for i in range(len(cur[0]))]
            x = crossing(mcurve, spreads=SPREADS_40)
            grid[(pd, dlt)] = (mcurve, x)
            if x is None:
                print(f"{pd:>3}{dlt:>4}"
                      + "".join(f"{p:>6.1f}" for p in mcurve)
                      + "   NO CROSSING")
            else:
                C = x * SPEC_SLOPE
                print(f"{pd:>3}{dlt:>4}"
                      + "".join(f"{p:>6.1f}" for p in mcurve)
                      + f" {x:6.1f} {C:6.1f} {C/(2*dlt):6.3f}")
            sys.stdout.flush()
    return grid, curves


# ------------------------------------------------------------ fits
def lsqlin(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my - b * mx, b


def alpha_of(x, dlt):
    return x * SPEC_SLOPE / (2.0 * dlt)


def plane_fit(cells):
    """cells: list of (pd, dlt, alpha). Fit alpha = a - b·pd - c·(dlt-12)
    via least squares on design [1, -pd, -(dlt-12)]."""
    import itertools
    A = [[1.0, -float(p), -float(d - 12)] for p, d, _ in cells]
    y = [a for _, _, a in cells]
    n = 3
    # normal equations
    ata = [[sum(A[r][i] * A[r][j] for r in range(len(A)))
            for j in range(n)] for i in range(n)]
    aty = [sum(A[r][i] * y[r] for r in range(len(A))) for i in range(n)]
    # gaussian elimination
    M = [row[:] + [aty[i]] for i, row in enumerate(ata)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[col][col] != 0:
                f = M[r][col] / M[col][col]
                for k in range(col, n + 1):
                    M[r][k] -= f * M[col][k]
    beta = [M[i][n] / M[i][i] if M[i][i] else 0.0 for i in range(n)]
    res = [y[r] - (beta[0] - beta[1] * p - beta[2] * (d - 12))
           for r, (p, d, _) in enumerate(cells)]
    return beta, res


def bilinear_fit(cells):
    """alpha = a + b·pd + c·(dlt-12) + d·pd·(dlt-12), 4-param LS."""
    A = [[1.0, float(p), float(d - 12), float(p) * float(d - 12)]
         for p, d, _ in cells]
    y = [a for _, _, a in cells]
    n = 4
    ata = [[sum(A[r][i] * A[r][j] for r in range(len(A)))
            for j in range(n)] for i in range(n)]
    aty = [sum(A[r][i] * y[r] for r in range(len(A))) for i in range(n)]
    M = [row[:] + [aty[i]] for i, row in enumerate(ata)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[col][col] != 0:
                f = M[r][col] / M[col][col]
                for k in range(col, n + 1):
                    M[r][k] -= f * M[col][k]
    beta = [M[i][n] / M[i][i] if M[i][i] else 0.0 for i in range(n)]
    res = [y[r] - (beta[0] + beta[1] * p + beta[2] * (d - 12)
                   + beta[3] * p * (d - 12))
           for r, (p, d, _) in enumerate(cells)]
    return beta, res


def analyze(grid, curves):
    print("\n== ANALYSIS (decision rules pre-registered in header) ==")
    cells = []
    for pd in PDS:
        for dlt in DELTAS:
            x = grid[(pd, dlt)][1]
            if x is None:
                print(f"  cell pd={pd} d={dlt}: NO CROSSING — excluded, "
                      f"not extrapolated")
            else:
                cells.append((pd, dlt, alpha_of(x, dlt)))
    print(f"  crossing cells: {len(cells)}/20")

    print("-- H1: plane alpha = a - b·pd - c·(delta-12) --")
    if len(cells) < 6:
        print("  too few crossing cells for a plane -> H1 FALSIFIED "
              "(no plane fits)")
        h1 = "FALSIFIED"
        beta = res = None
    else:
        beta, res = plane_fit(cells)
        maxres = max(abs(e) for e in res)
        print(f"  fit: alpha = {beta[0]:.3f} - {beta[1]:.3f}·pd "
              f"- {beta[2]:.3f}·(delta-12)")
        print(f"  max|resid| = {maxres:.4f} (gate 0.03) -> H1 "
              f"{'VALIDATED' if maxres <= 0.03 else 'FALSIFIED'}")
        worst = sorted(zip((abs(e) for e in res), cells), reverse=True)[:3]
        for ar, (p, d, a) in worst:
            print(f"    worst: pd={p} d={d} alpha={a:.3f} "
                  f"resid={a - (beta[0] - beta[1]*p - beta[2]*(d-12)):+.4f}")
        h1 = "VALIDATED" if maxres <= 0.03 else "FALSIFIED"
        if h1 == "FALSIFIED":
            bb, bres = bilinear_fit(cells)
            bmax = max(abs(e) for e in bres)
            print(f"  [exploratory, cannot rescue H1] bilinear: alpha = "
                  f"{bb[0]:.3f} + {bb[1]:.3f}·pd + {bb[2]:.3f}·(d-12) + "
                  f"{bb[3]:.4f}·pd·(d-12)  max|resid|={bmax:.4f} "
                  f"({'fits 0.03 gate' if bmax <= 0.03 else 'also fails'})")

    print("-- H2: delta-slope m(pd) and the sign-flip boundary --")
    # per-pd-column linear alpha vs delta (full crossing columns)
    ms = {}
    for pd in PDS:
        pts = [(float(d), a) for (p, d, a) in cells if p == pd]
        if len(pts) < 3:
            print(f"  pd={pd}: only {len(pts)} crossings — column fit "
                  f"unreliable, skipped for m(pd)")
            continue
        a0, m = lsqlin([p[0] for p in pts], [p[1] for p in pts])
        res_c = [y - (a0 + m * x) for x, y in pts]
        ms[pd] = m
        print(f"  m(pd={pd}) = {m:+.5f}/delta "
              f"(col max|resid| {max(abs(e) for e in res_c):.4f}, "
              f"n={len(pts)})")
    if len(ms) < 2:
        print("  fewer than 2 usable columns -> H2 INCONCLUSIVE")
        h2 = "INCONCLUSIVE"
        flip_line = None
    else:
        xs = sorted(ms)
        f0, f1 = lsqlin([float(p) for p in xs], [ms[p] for p in xs])
        pd_flip = -f0 / f1 if f1 else float("inf")
        mono = all(ms[xs[i]] < ms[xs[i + 1]] for i in range(len(xs) - 1)) \
            or all(ms[xs[i]] > ms[xs[i + 1]] for i in range(len(xs) - 1))
        print(f"  m(pd) fit: m = {f0:+.5f} {f1:+.5f}·pd  "
              f"{'monotone' if mono else 'NONMONOTONE'}")
        if 0 < pd_flip < 100:
            print(f"  pd_flip = -m0/m1 = {pd_flip:.2f}   "
                  f"[H2 formula: pd_flip = {-f0:.4f}/{f1:.4f}]")
        else:
            print(f"  pd_flip = {pd_flip:.2f} (outside grid)")
        # bootstrap by seed: recompute per-seed alpha grid crossings
        print("  -- bootstrap by seed (5 single-seed replicates) --")
        votes_stable = 0
        for si, sd in enumerate(SEEDS):
            scells = []
            for pd in PDS:
                for dlt in DELTAS:
                    x = crossing(curves[(pd, dlt)][si], spreads=SPREADS_40)
                    if x is not None:
                        scells.append((pd, dlt, alpha_of(x, dlt)))
            sms = {}
            for pd in PDS:
                pts = [(float(d), a) for (p, d, a) in scells if p == pd]
                if len(pts) >= 3:
                    sms[pd] = lsqlin([p[0] for p in pts],
                                     [p[1] for p in pts])[1]
            lo = sms.get(min(sms))
            hi = sms.get(max(sms))
            if lo is not None and hi is not None and lo < 0 < hi:
                votes_stable += 1
                tag = "flip (m(lo)<0<m(hi))"
            else:
                tag = "no clean flip"
            print(f"    seed {sd}: " + "  ".join(
                f"m({p})={sms[p]:+.4f}" for p in sorted(sms))
                + f"  -> {tag}")
        print(f"  flip sign-stable in {votes_stable}/5 seed replicates "
              f"(majority gate: >= 3/5)")
        sign_ok = votes_stable >= 3
        # H2 verdict: monotone m(pd) with sign flip inside/near grid AND
        # bootstrap-stable; monotone but no interior flip = MIXED; noise =
        # FALSIFIED
        if sign_ok and mono and 2.5 <= pd_flip <= 6.5:
            h2 = "VALIDATED"
        elif sign_ok and mono:
            h2 = "MIXED"
        elif not sign_ok:
            h2 = "FALSIFIED (flip is noise by bootstrap)"
        else:
            h2 = "MIXED (nonmonotone m(pd))"
        flip_line = (f0, f1, pd_flip)

    print(f"\nVERDICT H1: {h1}")
    print(f"VERDICT H2: {h2}")
    return h1, h2, cells, beta, res


def main():
    print("SPIN-40 METROLOGY pd x delta interaction grid —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} ladder, slope 1.6 spec (200/125), K=1, "
          f"spreads={list(SPREADS_40)}, grid pd{list(PDS)} x "
          f"delta{list(DELTAS)}, seeds={SEEDS}, ticks={TICKS}, drift={DRIFT}")
    print("PREREG H1: alpha = a - b·pd - c·(d-12) plane, max|resid|<=0.03; "
          "FALSIFY if resid>0.03 anywhere or no plane fits. Bilinear "
          "cross-term fit is exploratory only.")
    print("PREREG H2: delta-slope m(pd) monotone in pd, pd_flip=-m0/m1 "
          "stated; FALSIFY if per-seed bootstrap (5 replicates) shows the "
          "m-sign flip is not majority-stable. No-crossing cells excluded, "
          "never extrapolated.")

    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    sys.stdout.flush()
    if not ok:
        sys.exit(1)

    grid, curves = run_grid()
    h1, h2, cells, beta, res = analyze(grid, curves)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
