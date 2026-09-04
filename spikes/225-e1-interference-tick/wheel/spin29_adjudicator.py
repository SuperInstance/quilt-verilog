#!/usr/bin/env python3
"""SPIN-29 DEVIL/EXPERT adjudicator (nudge 2026-09-03): is alpha=1.19 a
cell reading or a law? Spin 29 held pd=3, drift=6, N=6, K=1 fixed across
the whole delta grid. Two legs, everything else verbatim:

(1) pd column: pd in {2, 3(replay), 6} at delta=12. Spin 11's echo law
    makes the interference structure pd-driven (|1-N/pd|, walls at
    2pd+1). alpha moves -> the planned drift+band 2D sweep must source
    itself in pd x delta; alpha holds -> alpha is a drift/band animal.
(2) downward-delta leg: delta in {4, 6, 8} at pd=3, drift=6 — bites
    where delta <= drift, exactly where the affine intercept (1.35,
    "not separable") and the alpha wobble share sign and would separate.

Pre-registered deviation (before any run, spin-29 precedent): the
spread sweep widens DOWN to 4 for delta<=8 because the linear law
predicts s*(4) = alpha*8/1.6 ~= 5.9 — inside the old 8..40 sweep start
would clip the knee (s0.8/SPIN-27 scar). Upward bound kept at 40.
"""
import time
from spin29_metrology_cdelta import (dyn_run, static_fn, ladder, S16,
                                     pct, crossing, mean, SEEDS, SPEC_SLOPE,
                                     SPREADS, DRIFT, TICKS)

T0 = time.time()
SPREADS_DN = tuple(sorted(set(list(range(4, 42, 2)))))       # 4..40 step 2

def arm(spread, k, delta, pd):
    return mean([pct(dyn_run(static_fn(ladder(spread)), S16[1], k=k,
                             delta=delta, pd=pd, seed=sd), delta=delta)
                 for sd in SEEDS])

def leg(tag, deltas_or_pds, sweep, label):
    print(f"\n== LEG {tag} ==")
    print(f"{label:>10}" + "".join(f"{s:>6}" for s in sweep) + "   s*      C   alpha")
    for d in deltas_or_pds:
        c1 = [arm(s, 1, *inv(d)) for s in sweep]
        x = crossing(c1, spreads=sweep)
        if x is None:
            print(f"{str(d):>10}" + "".join(f"{p:>6.1f}" for p in c1)
                  + "   NO CROSSING")
            continue
        C = x * SPEC_SLOPE
        alpha = C / (2 * inv(d)[0])
        print(f"{str(d):>10}" + "".join(f"{p:>6.1f}" for p in c1)
              + f" {x:6.1f} {C:6.1f} {alpha:6.3f}")
        sys.stdout.flush()

def inv(d):
    # leg1 passes pd with delta fixed 12; leg2 passes delta with pd fixed 3
    return (D_LEG, d) if LEG == 1 else (d, PD_LEG)

import sys
LEG = int(sys.argv[1]) if len(sys.argv) > 1 else 0
D_LEG, PD_LEG = 12, 3

if __name__ == "__main__":
    print("SPIN-29 EXPERT adjudicator —", time.strftime("%Y-%m-%d %H:%M:%S"))
    if LEG == 1:
        leg("1: pd column @ delta=12", (2, 3, 6), SPREADS, "pd")
        print("\nREAD: alpha(pd=3) replay must be ~1.172 (spin29 anchor). "
              "alpha moves >15% across pd -> alpha is pd-coupled; sweep "
              "must be pd x delta. alpha holds -> drift/band animal.")
    elif LEG == 2:
        leg("2: downward delta @ pd=3, drift=6", (4, 6, 8), SPREADS_DN,
            "delta")
        print("\nREAD: alpha(delta<=drift) separates -> intercept/alpha "
              "wobble share mechanism; alpha holds -> parsimony claim "
              "sharpened, drift/band sweep proceeds as planned.")
    else:
        print("usage: adjudicator.py 1|2")
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")
