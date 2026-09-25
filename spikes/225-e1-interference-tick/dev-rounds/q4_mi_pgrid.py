#!/usr/bin/env python3
"""Q4 round-11 DEVIL-teeth check (nudge 2026-09-03): is p*=3/10000 real?

Tooth 1 — p-grid resolution: rerun arm v2 (winner) on the refined grid
  p ∈ {1,2,3,5,7,10}/10000 (integer contract forbids 1.5; 2 and 5 bracket
  the old argmax from both sides). If the peak stays at 3 across sizes,
  the argmax location is grid-robust; if it moves to 2 (or smears to a
  2/3 tie), the capacity table's actuator recommendation must carry the
  grid pitch as its error bar.

Tooth 2 — seed split: 5 seeds → fit half {1,7,42} / held-out half
  {1999,20260902}. R1 (interior argmax ≥2/3 sizes) and R3 (monotone
  MI_max trend in L) evaluated per half independently. v2 graduates to
  finding only if both halves pass.

Integer-only measurement path, identical to q4_mi_criticality.py
(imported; canaries live there). This script is exploratory→confirmatory
per DEVIL: v2's R1–R3 pass on the ORIGINAL sweep was amendment-grade;
survival here on new grid points + held-out seeds is the graduation test.
"""
from q4_mi_criticality import (run_cfg, sumtab, to_millibits, mi_fix,
                               SEEDS)

PS_FINE = [1, 2, 3, 5, 7, 10]      # /10000 — adds 2,5,7 inside the old gap
DS = [1, 2, 3]
Z_SIZES = [64, 128, 256]
FIT_SEEDS = [1, 7, 42]
HELD_SEEDS = [1999, 20260902]
assert sorted(FIT_SEEDS + HELD_SEEDS) == sorted(SEEDS)

def rows_for(group, sizes, seeds):
    out = {}
    for d in DS:
        for L in sizes:
            for p in PS_FINE:
                runs = [run_cfg("q4_mi_sweep2", group, L, d, p, s) for s in seeds]
                if group == 0:
                    tabs = [u["r"] for u in runs] + [u["s"] for u in runs]
                    out[(d, L, p)] = to_millibits(mi_fix(*sumtab(tabs)))
                else:
                    out[(d, L, p)] = to_millibits(mi_fix(*sumtab([u["r"] for u in runs])))
    return out

def r1_r3(rows, sizes):
    """R1: interior argmax (p not at 1 or 10 grid edge) for >=2/3 sizes.
    R3: MI_max monotone in L. Returns (r1, r3, argmaxes)."""
    amax = {}
    for d in DS:
        for L in sizes:
            amax[(d, L)] = max(PS_FINE, key=lambda p: rows[(d, L, p)])
    r1 = {}
    for d in DS:
        interior = sum(1 for L in sizes if 1 < amax[(d, L)] < 10)
        r1[d] = interior >= 2
    mis_max = {d: [rows[(d, L, max(PS_FINE, key=lambda p: rows[(d, L, p)]))] for L in sizes]
               for d in DS}
    r3 = {}
    for d in DS:
        m = mis_max[d]
        r3[d] = m == sorted(m) or m == sorted(m, reverse=True)
    return r1, r3, amax, mis_max

if __name__ == "__main__":
    for tag, group, sizes in (("Z", 0, Z_SIZES), ("D", 1, [s // 2 for s in Z_SIZES])):
        for half, seeds in (("FIT", FIT_SEEDS), ("HELD", HELD_SEEDS)):
            rows = rows_for(group, sizes, seeds)
            r1, r3, amax, mmax = r1_r3(rows, sizes)
            print(f"== v2 group {tag} {half} (seeds {seeds}) ==")
            for (d, L), p in sorted(amax.items()):
                print(f"  d={d} L={L}: p*={p}/10000  MI_max={mmax[d][sizes.index(L)]}mb")
            print(f"  R1: {r1}  -> {'PASS' if any(r1.values()) and sum(r1.values())>=2 else 'FAIL'}"
                  f"   R3: {r3} -> {'PASS' if sum(r3.values())>=2 else 'FAIL'}")
        # combined-half argmax comparison on the fine grid
        full = rows_for(group, sizes, SEEDS)
        r1f, r3f, amaxf, _ = r1_r3(full, sizes)
        print(f"  fine-grid full-seed argmax: {[amaxf[(d,L)] for d in DS for L in sizes]}")
    print("\nVerdict key: p*==3 in both halves at all sizes -> grid-robust;"
          " held-out R1&R3 pass -> v2 graduates to finding.")
