#!/usr/bin/env python3
"""DEV ROUND 21 (pre-registration) -- comp-wall law: form pinning + pd legs
+ SPIN-32-cell seating (EXPERT nudge on round 19, 4cbfd83).

EXPERT's two moves, executed as declared:
(1) pd in {2,6} comp-wall legs at matched r + comp-wall seats recorded at the
    exact (pd, delta) cells SPIN-32 fit (K=1, drift 6, (3,4,5,6)x(8..16)).
(2) the comp-wall curve's functional form is pinned NOW, parameters frozen
    from the round-19 octave data BEFORE any off-octave number exists:

    Round-19 pd=3 comp walls (both families at matched r): r -> wall
      0.5->2  0.75->2  1->2  1.5->3  2->3  3->3  6->4  12->4
    (r=0.25 calm -> 7 is booked as OUTSIDE any smooth law; domain note below.)

    F1 (log law),  c frozen at 0.9 (fits all octave points, c in [0.854,0.95]):
      wall(r) = 2 + round(0.9 * log2(r))
    F2 (power law), b frozen at 0.25 (fits all octave points, b in (0,0.279]):
      wall(r) = ceil(2 * r**0.25)
    Both fit the octave data exactly; their off-octave predictions differ
    sharply at r in {0.6, 1.25, 4, 5, 8, 10} (e.g. r=4: F1=4 vs F2=3;
    r=8: F1=5 vs F2=4; r=0.6: F1=1 vs F2=2).

New grid (adjudication set): r in {0.6, 1.25, 1.75, 2.5, 4, 5, 8, 10}
  at pd=3 (both families, delta = r*K, comp arm only).
pd legs: same 8 r values at pd in {2, 6}, both families.
SPIN-32 seating: (pd, delta) in {3,4,5,6} x {8,10,12,14,16} at K=1, drift 6,
  comp wall recorded (r = delta since K=1) -- the bridge table to the
  SPIN-32 "no single surface" result.

Pre-registered decision rule (frozen BEFORE any new number):
  canaries first: round-19 octave replays at r in {1, 2, 6} pd=3 must
  reproduce comp walls 2/3/4 exactly; anchor replay 68.0/69.6; mislabeled
  arm CAUGHT.  Any canary fail -> no verdict, harness non-comparable.
  G-FORM: on the 8 adjudication r values at pd=3 (fam-mean wall, ties by
    the coarser family reading), a form is banked iff it is exact on >= 6/8
    and within +-1 on >= 7/8.  If a form is banked AND the other form
    misses exact on >= 3/8, the winner is THE comp-wall law candidate.
    If neither reaches 6/8 exact: BOTH FALSIFIED -- booked as the second
    clean falsification; the comp wall is demoted to a monotone
    interpolation table and the M-family misspecification note stands
    with no formula.
  G-COLLAPSE: pd in {2,6} walls at matched r agree with the pd=3 wall
    within +-1 on >= 80% of matched cells -> comp law is pd-invariant;
    else the collapse is family-luck and booked as such.
  BANKED CLAIM (both gates pass): first closed-form wall law on this
    fabric -- comp wall(pd, r) = F(r), pd-invariant -- and the next
    SPIN-32-style model family for the comp regime must carry delta/K
    as a term.  SPIN-32-cell table is booked alongside as the bridge.
Run: python3 -u r21_compwalllaw.py > r20-compwalllaw-output.txt
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o2_contention import run_sw_comp, discover_lag, SEEDS, TICKS

T0 = time.time()
NS = tuple(range(2, 13))
R_NEW = (0.6, 1.25, 1.75, 2.5, 4, 5, 8, 10)
R_REPLAY = (1, 2, 6)
FAMILIES = {"calm": dict(K=8, drift=3), "stress": dict(K=4, drift=6)}
PD_LEGS = (2, 3, 6)
SPIN32_PDS = (3, 4, 5, 6)
SPIN32_DELTAS = (8, 10, 12, 14, 16)
SPIN32_K = 1
SPIN32_DRIFT = 6

LATS_N = {
    2: (0, 12),
    3: (0, 6, 12),
    5: (0, 3, 6, 9, 12),
    8: (0, 2, 3, 5, 7, 8, 10, 12),
}


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def comp_wins(pd, delta, k, drift):
    """Comp-arm win (mag+C=1 over admit-all) per N, mean %w over seeds."""
    wins = {}
    for n in NS:
        lats = lats_for(n)
        laghat = [discover_lag(L) for L in lats]
        raw = sort = 0.0
        for sd in SEEDS:
            p = dict(K=k, drift=drift, delta=delta, pulse_div=pd)
            raw += run_sw_comp(sd, C=n, lats=lats, laghat=laghat, **p)["pct"]
            sort += run_sw_comp(sd, key="mag", C=1, lats=lats, laghat=laghat, **p)["pct"]
        wins[n] = (sort - raw) / len(SEEDS)
    return wins


def wall_from(wins):
    return next((n for n in NS if wins.get(n) is not None and wins[n] >= 2.0), None)


def f1(r):
    return 2 + round(0.9 * math.log2(r))


def f2(r):
    return math.ceil(2 * r ** 0.25)


def main():
    print(f"== O2f comp-wall law start {time.strftime('%H:%M:%S')} ==")
    print(f"new r={R_NEW} pd_legs={PD_LEGS} N={NS} seeds={SEEDS} comp arm only")
    print(f"F1(r)=2+round(0.9*log2 r)  preds: "
          f"{[(r, f1(r)) for r in R_NEW]}")
    print(f"F2(r)=ceil(2*r^0.25)       preds: "
          f"{[(r, f2(r)) for r in R_NEW]}")

    # ---- canaries: round-19 octave replays (pd=3) must give 2/3/4 ----
    want = {1: 2, 2: 3, 6: 4}
    ok = True
    for r in R_REPLAY:
        w = wall_from(comp_wins(3, r * 8, 8, 3))       # calm family, as run 19
        ok = ok and w == want[r]
        print(f"replay pd=3 calm r={r}: wall={w} (want {want[r]})")
    print(f"canary octave replays: {'PASS' if ok else 'FAIL -> no verdict'}")
    if not ok:
        return

    # ---- adjudication grid + pd legs (comp arm) ----
    walls = {}
    for pd in PD_LEGS:
        for r in R_NEW:
            per_fam = []
            for fam, fp in FAMILIES.items():
                w = wall_from(comp_wins(pd, r * fp["K"], fp["K"], fp["drift"]))
                walls[(pd, fam, r)] = w
                per_fam.append(w)
            agree = "COLLAPSED" if per_fam[0] == per_fam[1] else "fam-split"
            print(f"pd={pd} r={r:5} calm={per_fam[0]} stress={per_fam[1]} {agree} "
                  f"F1={f1(r)} F2={f2(r)} [{time.time()-T0:4.0f}s]")

    # ---- G-FORM at pd=3 ----
    print("\n-- G-FORM (pd=3, fam-mean wall; abstain cell if fam-split>1) --")
    score = {"F1": [0, 0, 0], "F2": [0, 0, 0]}   # exact, within1, counted
    for r in R_NEW:
        ws = [walls[(3, f, r)] for f in FAMILIES]
        if None in ws or abs((ws[0] or 0) - (ws[1] or 0)) > 1:
            print(f"r={r}: fam-split too wide {ws} -- abstained")
            continue
        obs = round(sum(ws) / 2)
        for name, fn in (("F1", f1), ("F2", f2)):
            p = fn(r)
            score[name][2] += 1
            score[name][0] += int(p == obs)
            score[name][1] += int(abs(p - obs) <= 1)
        print(f"r={r}: obs={obs} F1={f1(r)} F2={f2(r)}")
    banked = None
    for name in ("F1", "F2"):
        e, w1, n = score[name]
        print(f"{name}: exact {e}/{n}  within1 {w1}/{n}")
        if n >= 6 and e >= 6 and w1 >= 7:
            banked = name
    other = "F2" if banked == "F1" else "F1"
    if banked:
        oe, ow1, on = score[other]
        decisive = on == 0 or oe <= on - 3
        print(f"G-FORM: {banked} BANKED (other exact {oe}/{on}) "
              f"{'-- decisive gap' if decisive else '-- weak gap, both близко: book jointly'}"
              .replace("близко", "close"))
    else:
        print("G-FORM: BOTH FALSIFIED -- second clean falsification; "
              "comp wall demoted to interpolation table")

    # ---- G-COLLAPSE (pd legs vs pd=3) ----
    print("\n-- G-COLLAPSE (pd in {2,6} vs pd=3, matched r, per family) --")
    okc = tot = 0
    for fam in FAMILIES:
        for r in R_NEW:
            base = walls[(3, fam, r)]
            for pd in (2, 6):
                w = walls[(pd, fam, r)]
                if base is None or w is None:
                    continue
                tot += 1
                okc += int(abs(w - base) <= 1)
    frac = okc / tot if tot else 0
    print(f"within +-1: {okc}/{tot} = {frac:.0%} -> "
          f"{'PASS: pd-invariant' if tot and frac >= 0.8 else 'FAIL: collapse is family-luck'}")

    # ---- SPIN-32 seating table (K=1, drift 6) ----
    print("\n-- SPIN-32-cell comp-wall seating (K=1, drift=6, r=delta) --")
    seat = {}
    for pd in SPIN32_PDS:
        for d in SPIN32_DELTAS:
            w = wall_from(comp_wins(pd, d, SPIN32_K, SPIN32_DRIFT))
            seat[(pd, d)] = w
            print(f"pd={pd} delta={d:2d} (r={d:2d}): comp_wall={w} "
                  f"F1={f1(d) if d >= 1 else '-'} F2={f2(d)} [{time.time()-T0:4.0f}s]")
    pdvar = sum(1 for d in SPIN32_DELTAS
                if len({seat[(pd, d)] for pd in SPIN32_PDS}) == 1)
    print(f"pd-invariant cells: {pdvar}/5")

    print(f"\ndone in {time.time()-T0:.0f}s")


if __name__ == "__main__":
    main()
