#!/usr/bin/env python3
"""SPIN-33 -- REGIME BRACKET: what does the SPIN-32 flip locus pd*=4.25
mean on an integer-pd lattice?  Pre-registered BEFORE any run (this
header IS the pre-registration; commit first, run second).

Background (SPIN-32, ea8a693): the bilinear fit's flip locus
d(alpha)/d(delta) = 0 sits at pd* = 4.25.  The fabric's pd is integer;
endpoints measured: pd=3 CURVES INTO THE WALL (dalpha/ddelta > 0),
pd=6 LINEAR-CONTINUES (dalpha/ddelta < 0).  Claim booked: pd*=4.25 is
an interpolated REGIME-BOUNDARY LOCATION, not a parameter estimate.
This spin tests that reading directly on the lattice.

Design: arms pd in {4, 5} (integer, production-realistic) x delta in
{8,10,12,14,16}, plus rational-pd brackets {3.5=7/2, 4.25=17/4,
4.75=19/4} on the same delta axis, 3 seeds/arm (1,7,42), sweep
spreads 8..30 step 2, K=1, N=6, slope 1.6, drift=6, ticks=4800.
Instrument: spin32's dyn_run_r (rational pulse divider), pct/crossing
from spin29.  alpha per arm = crossing of the seed-mean curve.

Pre-registered gates (decided now, before any run):
  G1 (regime): sign of dalpha/ddelta (LSQ slope over the 5 deltas)
      is POSITIVE at pd=4 and NEGATIVE at pd=5.  If both share a
      sign, the boundary reading is WRONG and pd* is re-opened.
  G2 (location): the sign flip interpolates inside (4,5); loose
      bracket 4.0 <= pd*_interp <= 5.0 by linear interp of the two
      integer-pd slopes.  (No gate vs 4.25 itself: one interpolated
      number from a refused-family fit is context, not ground truth.)
  G3 (monotone bracket): rational-pd slopes are monotone decreasing
      in pd across {3.5, 4, 4.25, 4.75, 5} (allowing one tie within
      2*median arm NF).  A non-monotone bracket means the boundary
      picture is too simple and gets reported as such.
  NF per arm = half the seed range of alpha (SPIN-32 convention).

Integer-only inside every loop; floats only at print/stat time.
Output: python3 -u spin33_regime_bracket.py > spin33-output.txt
(no pipes; SPIN-30 collision scar).
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spin29_metrology_cdelta import (static_fn, ladder, S16, pct,
                                     crossing, mean)
from spin32_grid2d import dyn_run_r

DELTAS = (8, 10, 12, 14, 16)
SPREADS = tuple(range(8, 31, 2))
SEEDS = (1, 7, 42)
# (pdn, pdd, label): integer anchors first, rational brackets between
ARMS = [(4, 1, "4"), (7, 2, "3.5"), (17, 4, "4.25"), (19, 4, "4.75"),
        (5, 1, "5")]

T0 = time.time()


def curve(pdn, pdd, delta, seed):
    return [pct(dyn_run_r(static_fn(ladder(s)), S16[1], k=1, pdn=pdn,
                          pdd=pdd, delta=delta, seed=seed), delta=delta)
            for s in SPREADS]


def lsq_slope(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


def main():
    print(f"SPIN-33 regime bracket start {time.strftime('%H:%M:%S')}")
    print(f"arms pd={{3.5,4,4.25,4.75,5}} x delta={DELTAS}, "
          f"seeds={SEEDS}, spreads={SPREADS[0]}..{SPREADS[-1]}")
    alpha = {}   # (label, delta) -> (alpha, nf)
    for pdn, pdd, lab in ARMS:
        for delta in DELTAS:
            per_seed = [curve(pdn, pdd, delta, sd) for sd in SEEDS]
            mean_c = [mean([per_seed[si][i] for si in range(len(SEEDS))])
                      for i in range(len(SPREADS))]
            a = crossing(mean_c, delta)
            per_seed_a = [crossing(c, delta) for c in per_seed]
            nf = (max(per_seed_a) - min(per_seed_a)) / 2.0
            alpha[(lab, delta)] = (a, nf)
            print(f"  pd={lab:>4} d={delta:2d}  alpha={a:7.4f} "
                  f"nf={nf:.4f}  per-seed={[round(x,4) for x in per_seed_a]}"
                  f"  [{time.time()-T0:6.0f}s]")
    # per-pd slope of alpha vs delta
    print("\n-- d(alpha)/d(delta) per pd (LSQ over 5 deltas) --")
    slopes = []
    for pdn, pdd, lab in ARMS:
        ys = [alpha[(lab, d)][0] for d in DELTAS]
        nfmax = max(alpha[(lab, d)][1] for d in DELTAS)
        s = lsq_slope(list(DELTAS), ys)
        slopes.append((lab, s, nfmax))
        print(f"  pd={lab:>4}  slope={s:+.5f}  maxNF={nfmax:.4f}  "
              f"alpha(delta=8..16)={[round(y,3) for y in ys]}")
    # gates
    print("\n-- gates --")
    sl = {lab: s for lab, s, _ in slopes}
    g1 = sl["4"] > 0 and sl["5"] < 0
    print(f"G1 regime (pd=4 up, pd=5 down): {'PASS' if g1 else 'FAIL'}")
    if sl["4"] > 0 and sl["5"] < 0:
        pdstar = 4 + (5 - 4) * sl["4"] / (sl["4"] - sl["5"])
        g2 = 4.0 <= pdstar <= 5.0
        print(f"G2 location: pd*_interp = {pdstar:.3f} in (4,5): "
              f"{'PASS' if g2 else 'FAIL'}  (SPIN-32 fit said 4.25)")
    else:
        print("G2 location: N/A (G1 failed)")
    vals = [s for _, s, _ in slopes]
    ties = sum(1 for i in range(len(vals) - 1)
               if abs(vals[i] - vals[i + 1]) < 1e-9)
    g3 = all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
    print(f"G3 monotone bracket {['%s:%+.5f' % (l, s) for l, s, _ in slopes]}: "
          f"{'PASS' if g3 else 'FAIL'} ({ties} exact ties)")
    print(f"\nSPIN-33 done in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
