#!/usr/bin/env python3
"""SPIN-31 — METROLOGY (pd-law spoke): does C = s*·slope scale predictably
with pd?  (Spin 29's expert adjudication, now tested as metrology.)

BACKGROUND (booked):
  SPIN-29:  C(delta) ~= 2.38·delta at pd=3, drift=6 — but the adjudicator
  measured alpha(delta=12, pd=6) = 0.977 (-17%, past the 15% gate) and NO
  CROSSING at pd=2 (N=6 co-fire wall). alpha=1.19 is a CELL reading
  (pd=3, delta>=8), not a law. This spin makes pd a first-class axis.

HYPOTHESIS (pre-registered BEFORE any panel run):
  C(pd, delta) = s*·slope = beta · (2·delta) · g(pd),  g LINEAR in pd,
  i.e. alpha(pd) = C/(2·delta) = alpha0 + gamma·pd on the crossing cells.
  Adjudicator pins two points: alpha(pd=3)=1.172, alpha(pd=6)=0.977 ->
  linear interpolation predicts alpha(4)=1.107, alpha(5)=1.042;
  C(pd) at delta=12 predicted: 28.1, 26.6, 25.0, 23.4 for pd=3..6.
  DELTA-STABILITY ARM: at pd=6, alpha must hold across delta in {8,12,16}
  (predicted C = 15.6, 23.4, 31.3).

PRE-REGISTERED DECISION RULE (fixed before any run):
  VALIDATED if ALL of:
    (L) alpha(pd) at delta=12 is linear in pd: max |residual| of the
        least-squares line alpha = a + b·pd over pd in {3,4,5,6} is
        <= 0.03 (about 3x the last-digit noise of ~0.01 in alpha);
    (S) monotone: alpha strictly decreasing OR strictly increasing in pd
        (direction pre-predicted: DECREASING, b < 0);
    (D) delta-stable: at pd=6, max alpha spread across delta in
        {8,12,16} is <= 10% of mean alpha(pd=6).
  FALSIFIED if (L) fails AND the alternative saturation test passes
    instead: SATURATION = |alpha(6)-alpha(5)| <= 0.5·|alpha(4)-alpha(3)|
    (the step shrinks by half or more at the top).
  MIXED if (L) holds but (D) fails (pd-law is delta-coupled), or if
    (L) fails without saturation.
  INCONCLUSIVE if any pd in {3,4,5,6} shows NO 50% crossing at delta=12
  (regime wall extends further up than pd=2).

DESIGN: N=6 ladder, K=1, slope 1.6 from SPEC (200/125 exact, SPIN-21
scar), spread sweep 8..30 step 2 (12 points, per brief; all predicted
knees lie in 9.8..19.5 — no clipping), drift=6, ticks=4800, seeds
1/7/42/1999/20260902 (5-seed means). pd=2 SKIPPED — no crossing already
booked by the SPIN-29 adjudicator (N=6 > 2·pd+1 co-fire wall).
Arms: pd in {3,4,5,6} at delta=12 (pd=3 doubles as replay anchor) plus
pd=6 replication at delta in {8,16} (delta=12 leg shared).

CANARIES (all must pass before any panel read; abort on fail):
  a. wiring byte-identity >= 8 configs dyn_run vs run_fabric, INCLUDING
     pd=6 (pd is now the swept knob, so both pd=3 and pd=6 legs checked).
  b. anchors (spin-10 publishing semantics: debt=mean mass, ev=mean
     events): zero@15 K=1 = 77.3 / 187834 / 8756; ladder@15 K=1 = 71.5 /
     106378 / 5792.
  c. delta=12 pd=3 replay: s* ~= 17.9 (tol 1.0), C ~= 28.6 (tol 1.5).
  d. double-run byte-identity on >= 2 cells (pd=4 and pd=6 legs).

Integer-only inside every loop; floats only at print/stat time.
Instrument: dyn_run verbatim-imported from spin29_metrology_cdelta
(itself spin27's clone of spin21's canary-proven inline run_fabric arm).
python3 -u direct redirect to spin31-output.txt; unique filename
(SPIN-30 collision scar). No pipes.
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spin29_metrology_cdelta import (dyn_run, static_fn, ladder, S16, pct,
                                     crossing, mean, SEEDS, SPEC_SLOPE,
                                     SPREADS, DRIFT, TICKS, r0)
from exp_glm1 import run_fabric

PD0 = 3
DELTA0 = 12
PDS = (3, 4, 5, 6)
DELTA_REPL = (8, 12, 16)          # pd=6 replication arm
N = 6
T0 = time.time()
SPREADS_31 = tuple(range(8, 31, 2))   # 8..30 step 2, 12 points (per brief)


def arm(spread, k, delta, pd):
    return mean([pct(dyn_run(static_fn(ladder(spread)), S16[1], k=k,
                             delta=delta, pd=pd, seed=sd), delta=delta)
                 for sd in SEEDS])


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
        for pd in (PD0, 6):
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=1, pd=pd,
                               delta=DELTA0, drift=DRIFT, seed=sd)["resid"]
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
        r = run_fabric("interference", TICKS, ladder(15), K=1, pd=PD0,
                       delta=DELTA0, drift=DRIFT, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn(ladder(15)), r0, k=1, pd=PD0,
                              seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b1 = (abs(p - 71.5) <= 0.05 and abs(ev - 5792) <= 0.5
          and abs(m - 106378) <= 0.5)
    print(f"  ladder15 K=1: pct={p:.2f} (71.5)  ev={ev:.1f} (5792)  "
          f"debt={m:.1f} (106378)  -> {'PASS' if b1 else 'FAIL'}")
    tot_ev = tot_m = 0
    rs = []
    for sd in SEEDS:
        r = run_fabric("interference", TICKS, [0] * N, K=1, pd=PD0,
                       delta=DELTA0, drift=DRIFT, seed=sd)
        tot_ev += r["events"]
        tot_m += r["mass"]
        rs.append(pct(dyn_run(static_fn([0] * N), r0, k=1, pd=PD0,
                              seed=sd)))
    ev, m, p = tot_ev / 5, tot_m / 5, mean(rs)
    b2 = abs(p - 77.3) <= 0.05 and abs(ev - 8756) <= 0.5 \
        and abs(m - 187834) <= 0.5
    print(f"  zero    K=1: pct={p:.2f} (77.3)  ev={ev:.1f} (8756)  "
          f"debt={m:.1f} (187834)  -> {'PASS' if b2 else 'FAIL'}")
    ok &= b1 and b2

    print("\n== CANARY c: delta=12 pd=3 replay s*~=17.9, C~=28.6 ==")
    pcts = [arm(s, 1, 12, 3) for s in SPREADS_31]
    cx = crossing(pcts, spreads=SPREADS_31)
    c_ok = cx is not None and abs(cx - 17.9) <= 1.0 \
        and abs(cx * SPEC_SLOPE - 28.6) <= 1.5
    print("  curve: " + " ".join(f"{p:.1f}" for p in pcts))
    print(f"  s*={cx and round(cx,1)} (want ~17.9 tol 1.0)  "
          f"C={cx and round(cx*SPEC_SLOPE,1)} (want ~28.6 tol 1.5)"
          f"  -> {'PASS' if c_ok else 'FAIL'}")
    ok &= c_ok

    print("\n== CANARY d: determinism (dual runs, pd=4 and pd=6 cells) ==")
    d_ok = True
    n2 = 0
    for pd in (4, 6):
        for s in (8, 18, 30):
            a = dyn_run(static_fn(ladder(s)), S16[1], k=1, delta=12,
                        pd=pd, seed=42)
            b = dyn_run(static_fn(ladder(s)), S16[1], k=1, delta=12,
                        pd=pd, seed=42)
            n2 += 1
            if a != b:
                d_ok = False
                print(f"  NONDETERMINISTIC pd={pd} s={s}")
    print(f"  {'PASS' if d_ok else 'FAIL'}: {n2} dual runs byte-identical")
    ok &= d_ok
    return ok


# ------------------------------------------------------------ panel
def leg_pd():
    print("\n== LEG 1: pd sweep {3,4,5,6} at delta=12, slope 1.6, K=1 ==")
    print(f"{'pd':>4}" + "".join(f"{s:>6}" for s in SPREADS_31)
          + "   s*      C   alpha   predC")
    out = {}
    for pd in PDS:
        c1 = [arm(s, 1, 12, pd) for s in SPREADS_31]
        x = crossing(c1, spreads=SPREADS_31)
        out[pd] = (c1, x)
        if x is None:
            print(f"{pd:>4}" + "".join(f"{p:>6.1f}" for p in c1)
                  + "   NO CROSSING")
        else:
            C = x * SPEC_SLOPE
            pred = 2 * 12 * (1.172 + (0.977 - 1.172) * (pd - 3) / 3)
            print(f"{pd:>4}" + "".join(f"{p:>6.1f}" for p in c1)
                  + f" {x:6.1f} {C:6.1f} {C/24:6.3f} {pred:7.1f}")
        sys.stdout.flush()
    return out


def leg_delta6():
    print("\n== LEG 2: delta replication at pd=6 (alpha delta-stability) ==")
    print(f"{'delta':>6}" + "".join(f"{s:>6}" for s in SPREADS_31)
          + "   s*      C   alpha   predC")
    out = {}
    for d in DELTA_REPL:
        if d == 12:
            x = leg_pd_out[6][1] if leg_pd_out else None
            c1 = leg_pd_out[6][0] if leg_pd_out else []
        else:
            c1 = [arm(s, 1, d, 6) for s in SPREADS_31]
            x = crossing(c1, spreads=SPREADS_31)
        out[d] = (c1, x)
        if x is None:
            print(f"{d:>6}" + "".join(f"{p:>6.1f}" for p in c1)
                  + "   NO CROSSING")
        else:
            C = x * SPEC_SLOPE
            print(f"{d:>6}" + "".join(f"{p:>6.1f}" for p in c1)
                  + f" {x:6.1f} {C:6.1f} {C/(2*d):6.3f}"
                  f" {0.977*2*d:7.1f}")
        sys.stdout.flush()
    return out


leg_pd_out = None


def analyze(pd_out, dl_out):
    print("\n== ANALYSIS (decision rule pre-registered in header) ==")
    alphas = {}
    for pd in PDS:
        x = pd_out[pd][1]
        if x is None:
            print(f"  pd={pd}: NO CROSSING at delta=12 -> INCONCLUSIVE "
                  f"(regime wall above pd=2)")
            verdict = "INCONCLUSIVE"
            print(f"VERDICT: {verdict}")
            return verdict, alphas
        C = x * SPEC_SLOPE
        alphas[pd] = C / 24.0
        print(f"  pd={pd}: s*={x:5.1f}  C={C:5.1f}  alpha={alphas[pd]:.3f}")
    xs = [float(p) for p in PDS]
    ys = [alphas[p] for p in PDS]
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    res = [y - (a + b * x) for x, y in zip(xs, ys)]
    maxres = max(abs(e) for e in res)
    mono_dec = all(ys[i] > ys[i + 1] for i in range(len(ys) - 1))
    mono_inc = all(ys[i] < ys[i + 1] for i in range(len(ys) - 1))
    L = maxres <= 0.03
    S = (mono_dec and b < 0) or (mono_inc and b > 0)
    sat = abs(ys[3] - ys[2]) <= 0.5 * abs(ys[1] - ys[0])
    print(f"  fit: alpha = {a:.3f} {b:+.4f}·pd   max|resid|={maxres:.4f} "
          f"(gate 0.03) -> L {'PASS' if L else 'FAIL'}")
    print(f"  monotone: dec={mono_dec} inc={mono_inc} slope b={b:+.4f} "
          f"(pre-predicted DECREASING) -> S {'PASS' if S else 'FAIL'}")
    print(f"  saturation test: |a6-a5|={abs(ys[3]-ys[2]):.4f} vs "
          f"0.5·|a4-a3|={0.5*abs(ys[1]-ys[0]):.4f} -> "
          f"{'SATURATING' if sat else 'not saturating'}")

    print("  -- delta-stability at pd=6 (gate 10% of mean alpha) --")
    D = None
    a6 = {}
    for d in DELTA_REPL:
        x = dl_out[d][1]
        if x is None:
            print(f"  delta={d}: NO CROSSING at pd=6")
            continue
        a6[d] = x * SPEC_SLOPE / (2 * d)
    if len(a6) == 3:
        vals = list(a6.values())
        spread = (max(vals) - min(vals)) / mean(vals)
        D = spread <= 0.10
        print("  alpha(pd=6): "
              + "  ".join(f"d{d}={v:.3f}" for d, v in a6.items())
              + f"  spread={spread*100:.1f}% -> D "
              f"{'PASS' if D else 'FAIL'}")
    else:
        print(f"  only {len(a6)}/3 crossings at pd=6 -> D FAIL")

    if L and S and D:
        verdict = "VALIDATED"
    elif (not L) and sat and not D:
        verdict = "FALSIFIED (saturation, not linear)"
    elif L and S and not D:
        verdict = "MIXED (pd-law linear but delta-coupled)"
    elif (not L) and sat:
        verdict = "MIXED (saturating AND delta-unstable)"
    elif not L and not sat:
        verdict = "MIXED (nonlinear without saturation)"
    else:
        verdict = "MIXED"
    print(f"VERDICT: {verdict}")
    return verdict, alphas


def main():
    global leg_pd_out
    print("SPIN-31 METROLOGY pd-law —", time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} ladder, slope 1.6 spec (200/125), K=1, "
          f"spreads={list(SPREADS_31)}, pd sweep {PDS} @ delta=12, "
          f"pd=6 delta-repl {DELTA_REPL}, seeds={SEEDS}, ticks={TICKS}, "
          f"drift={DRIFT}. pd=2 skipped (no crossing booked, spin-29 adj.)")
    print("PREDICTION (pre-registered): alpha(pd)=a+b·pd LINEAR "
          "(1.172 -> 0.977 across pd 3..6, DECREASING); C=beta·2·delta·g(pd).")
    print("RULE: VALIDATE iff linearity(max|resid|<=0.03) AND monotone-"
          "decreasing AND pd=6 delta-spread <=10%; FALSIFY if nonlinear AND "
          "saturating (|a6-a5| <= 0.5|a4-a3|); else MIXED/INCONCLUSIVE.")

    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    sys.stdout.flush()
    if not ok:
        sys.exit(1)

    leg_pd_out = leg_pd()
    dl_out = leg_delta6()
    analyze(leg_pd_out, dl_out)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
