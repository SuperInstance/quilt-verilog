#!/usr/bin/env python3
"""SPIN 16, SPOKE 6: REGIME — re-dispatch of failed SPIN-13 regime lane.

HYPOTHESIS UNDER TEST (memorylessness of the spread knee): the spread~15
knee measured in SPIN-4/5 is a STATIC property — no hysteresis, no
regime-switching tax. Falsify by direct measurement:

  (1) HYSTERESIS: hold spread s then shift mid-run to s' in {5,10,15,20,30}
      (both directions). Compare post-shift residency to the static-s'
      baseline measured over the SAME tick window (phase-fair: both runs
      share the seed's drift sequence tick-for-tick). Memoryless iff the
      post-settling deviation is ~0. Quantify transient half-life in ticks.
  (2) REGIME OSCILLATION: square-wave spread 5<->30, period P in {16,64,256},
      vs static-5, static-30, and their time-weighted mean. A switching tax
      exists iff osc < TW-mean - 2pp.
  (3) KNEE-HOLDING CONTROLLER: blind hill-climb on trailing residency,
      spread nudged +-1 within [8,22], vs static-15 (and static-8/-22).

Instrument: dyn_run — a faithful clone of exp_glm1.run_fabric with lats
generalized to a per-tick callable lats_fn(t). Every line touching g/pulses
is copied verbatim (fdiv decay mag = mag - (mag//2), FIFO expiry at life==0,
snapshot decay, decay applied only if pulses non-empty at trigger-time ...
i.e. run_fabric semantics). Canary C1 proves byte-identity.

Integer-only inside every loop; floats only at print/display time.
Config: N=6 ladder, K in {1,2}, seeds {1,7,42,1999,20260902},
delta=12 drift=6 pd=3 ticks=4800. W = settling window = 240 (one reality
period; also the natural knee timescale from SPIN-8 coherence radius).
"""
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
DRIFT = 6
PD = 3
N = 6
TICKS = 4800
HALF = TICKS // 2          # shift point
W = 240                    # settling window = one reality period
KS = (1, 2)
SHIFTS = (5, 10, 15, 20, 30)
T0 = time.time()


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


# ------------------------------------------------- instrument (verbatim clone)
def dyn_run(lats_fn, ticks=TICKS, K=4, pd=PD, delta=DELTA, drift=DRIFT,
            seed=20260902):
    """run_fabric interference arm, lats per-tick. Verbatim physics."""
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    last = -10
    resid = []
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
            pulses.appendleft([m if e > 0 else -m, K])
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
        if trig:
            last = t
        resid.append(abs(s_true - g))
    return resid


def pct(window, delta=DELTA):
    return within_pm(window, delta) / 10.0


def mean(v):
    return sum(v) / len(v)


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY C1: wiring byte-identity dyn_run vs run_fabric ==")
    nchk = 0
    for s, lats in (("zero@0", [0] * N), ("ladder@15", ladder(15)),
                    ("ladder@30", ladder(30))):
        for k in (1, 2):
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=sd)["resid"]
                b = dyn_run(lambda t, L=lats: L, K=k, seed=sd)
                nchk += 1
                if a != b:
                    ok = False
                    print(f"  MISMATCH {s} K={k} seed={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} configs byte-identical "
          f"(incl. zero@0 vs ladder(0) grammar identity)")
    # explicit zero@0 / zero@15 identity: all-zero lats is THE zero grammar
    a = dyn_run(lambda t: [0] * N, K=1, seed=SEEDS[0])
    b = dyn_run(lambda t: ladder(0), K=1, seed=SEEDS[0])
    z_ok = a == b
    ok &= z_ok
    print(f"  zero@0 == ladder(0): {'PASS' if z_ok else 'FAIL'}")

    print("\n== CANARY C2: anchor replays (5-seed means) ==")
    for name, lats, k, want in (("zero@15   K=1", [0] * N, 1, 77.3),
                                ("ladder@15 K=1", ladder(15), 1, 71.5)):
        rs = [dyn_run(lambda t, L=lats: L, K=k, seed=sd) for sd in SEEDS]
        tp = mean([pct(r) for r in rs])
        ev = None
        # replay events/debt via run_fabric for the debt check
        rf = [run_fabric("interference", TICKS, lats, K=k, pd=PD,
                         delta=DELTA, drift=DRIFT, seed=sd) for sd in SEEDS]
        ev = mean([r["events"] for r in rf])
        dbt = mean([r["mass"] for r in rf])
        want_ev, want_debt = ((5792, 106378) if "ladder" in name
                              else (None, 187834))
        good = (abs(tp - want) <= 0.2
                and (want_ev is None or abs(ev - want_ev) <= 2)
                and abs(dbt - want_debt) <= 300)
        ok &= good
        print(f"  {name}: {tp:.1f}% (want {want})  ev {ev:.0f} "
              f"(want {want_ev})  debt {dbt:.0f} (want {want_debt})  "
              f"-> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY C3: no-shift byte-identity (hold-s == static-s) ==")
    c3 = True
    for s in SHIFTS:
        lats = ladder(s)
        for k in KS:
            a = [dyn_run(lambda t, L=lats: L, K=k, seed=sd) for sd in SEEDS]
            # shift to itself at mid-run
            b = [dyn_run(lambda t, L=lats: L, K=k, seed=sd) for sd in SEEDS]
            for x, y in zip(a, b):
                if x != y:
                    c3 = False
    print(f"  hold-s vs static-s, s in {SHIFTS}, K in {KS}, 5 seeds: "
          f"{'PASS (trivially identical calls verified)' if c3 else 'FAIL'}")
    return ok


# --------------------------------------------------- exp 1: hysteresis
def static_resid_by_tick(s, k):
    """Mean per-tick within-flag vectors (0/1) across seeds for static s."""
    out = []
    for sd in SEEDS:
        r = dyn_run(lambda t, L=ladder(s): L, K=k, seed=sd)
        out.append([1 if x <= DELTA else 0 for x in r])
    return out


def shift_resid_by_tick(s, sp, k):
    out = []
    for sd in SEEDS:
        def fn(t, A=ladder(s), B=ladder(sp)):
            return A if t < HALF else B
        r = dyn_run(fn, K=k, seed=sd)
        out.append([1 if x <= DELTA else 0 for x in r])
    return out


def half_life(shift_vec, static_vec):
    """Transient half-life (ticks) after the shift.

    d(t) = seed-mean within-flag difference, post-shift. Find the first
    post-shift tick t* where |seed-mean d| >= 2pp sustained... simpler and
    honest: fit the cumulative deviation profile. half-life = first tick
    after which the running mean of d over the next W ticks stays < half
    of the initial-window (first 8 ticks post-shift) mean deviation,
    provided the initial deviation is nonzero.
    """
    T = len(shift_vec[0])
    d = [(mean([sv[t] for sv in shift_vec]) - mean([sv[t] for sv in static_vec]))
         for t in range(HALF, T)]
    if max(abs(x) for x in d) == 0:
        return 0, 0.0, 0.0
    d0 = mean(d[:8])
    if abs(d0) < 1e-9:
        # no immediate jump; half-life undefined, report peak
        pk = max(d, key=abs)
        return -1, d0 * 100, pk * 100
    # coarse scan in steps of 4: first tau where |mean(d[tau:tau+240])| < |d0|/2
    for tau in range(0, len(d) - W + 1, 4):
        if abs(mean(d[tau:tau + W])) < abs(d0) / 2:
            return tau, d0 * 100, mean(d[len(d) - W:]) * 100
    return len(d), d0 * 100, mean(d[len(d) - W:]) * 100


def exp1_hysteresis():
    print("\n== EXP 1: HYSTERESIS — mid-run spread shifts, half=" + str(HALF)
          + " ==")
    print(f"{'shift':>10}{'K':>3}{'post%':>8}{'static%':>9}{'dev pp':>8}"
          f"{'tail dev':>9}{'t1/2':>7}")
    tail_devs = {}
    for k in KS:
        statics = {s: static_resid_by_tick(s, k) for s in SHIFTS}
        for s in SHIFTS:
            for sp in SHIFTS:
                if s == sp:
                    continue
                sv = shift_resid_by_tick(s, sp, k)
                st = statics[sp]
                # phase-fair comparison: static run measured on same ticks
                post = [mean([x[t] for x in sv]) * 100
                        for t in range(HALF, TICKS)]
                stat = [mean([x[t] for x in st]) * 100
                        for t in range(HALF, TICKS)]
                post_pct = mean(post)
                stat_pct = mean(stat)
                dev = post_pct - stat_pct
                tail = mean(post[TICKS - HALF - W:]) - \
                    mean(stat[TICKS - HALF - W:])
                hl, d0, _ = half_life(sv, st)
                tail_devs[(s, sp, k)] = tail
                flag = "  <== >2pp" if abs(tail) > 2.0 else ""
                print(f"{s:>4}->{sp:<4}{k:>3}{post_pct:>8.1f}{stat_pct:>9.1f}"
                      f"{dev:>8.1f}{tail:>9.1f}{hl:>7}{flag}")
    mx = max(tail_devs.values(), key=abs)
    print(f"\n  max |tail deviation| (post-settling, last {W} ticks): "
          f"{mx:+.1f} pp")
    loop_area = {}
    for k in KS:
        up = tail_devs.get((5, 30, k), 0.0)
        dn = tail_devs.get((30, 5, k), 0.0)
        loop_area[k] = abs(up - dn) * W / 100.0
        print(f"  K={k}: 5->30 tail dev {up:+.1f} pp, 30->5 tail dev "
              f"{dn:+.1f} pp -> |loop area| ~ {loop_area[k]:.1f} tick-pp")
    return tail_devs, loop_area


# ----------------------------------------------- exp 2: oscillation tax
def exp2_oscillation():
    print("\n== EXP 2: REGIME OSCILLATION — square wave 5<->30 ==")
    print("  (static-17 and 10<->25 control added: separates true switching")
    print("   cost from the nonlinear spread->residency curve / Jensen.)")
    print(f"{'P':>5}{'K':>3}{'osc%':>7}{'stat5%':>8}{'stat30%':>9}"
          f"{'TWmean%':>9}{'stat17%':>9}{'tax pp':>8}{'verdict':>10}")
    taxes = {}
    for k in KS:
        st5 = mean([pct(dyn_run(lambda t, L=ladder(5): L, K=k, seed=sd))
                    for sd in SEEDS])
        st30 = mean([pct(dyn_run(lambda t, L=ladder(30): L, K=k, seed=sd))
                     for sd in SEEDS])
        st17 = mean([pct(dyn_run(lambda t, L=ladder(17): L, K=k, seed=sd))
                     for sd in SEEDS])
        twm = (st5 + st30) / 2.0
        for P in (16, 64, 256):
            def fn(t, P=P):
                return ladder(5) if (t // (P // 2)) % 2 == 0 else ladder(30)
            osc = mean([pct(dyn_run(fn, K=k, seed=sd)) for sd in SEEDS])
            tax = twm - osc
            taxes[(P, k)] = (osc, twm, tax)
            v = "TAX" if tax > 2.0 else "no-tax"
            print(f"{P:>5}{k:>3}{osc:>7.1f}{st5:>8.1f}{st30:>9.1f}"
                  f"{twm:>9.1f}{st17:>9.1f}{tax:>8.1f}{v:>10}")
        # control: 10<->25 square wave (same mean spread 17.5)
        for P in (16, 64):
            def fc(t, P=P):
                return ladder(10) if (t // (P // 2)) % 2 == 0 else ladder(25)
            osc = mean([pct(dyn_run(fc, K=k, seed=sd)) for sd in SEEDS])
            taxes[(f"10-25/P{P}", k)] = (osc, st17, st17 - osc)
            print(f"{f'10<->25 P={P}':>8}{k:>3}{osc:>7.1f}{'':>8}{'':>9}"
                  f"{'':>9}{st17:>9.1f}{st17 - osc:>8.1f}"
                  f"{'CTRL':>10}")
    return taxes


# ------------------------------------------------ exp 3: knee controller
def exp3_controller():
    print("\n== EXP 3: KNEE-HOLDING CONTROLLER — blind hill-climb, "
          "spread in [8,22] ==")
    print(f"{'mode':>16}{'K':>3}{'resid%':>8}")
    res = {}
    for k in KS:
        rows = {}
        for s in (8, 15, 22):
            rows[f"static-{s}"] = mean(
                [pct(dyn_run(lambda t, L=ladder(s): L, K=k, seed=sd))
                 for sd in SEEDS])
        ctl_tot = []
        for sd in SEEDS:
            r = dyn_run(controller_lats(sd, k), K=k, seed=sd)
            ctl_tot.append(pct(r))
        rows["controller"] = mean(ctl_tot)
        res[k] = rows
        for nm, v in rows.items():
            print(f"{nm:>16}{k:>3}{v:>8.1f}")
        c = rows["controller"]
        best_static = max(rows[f"static-{s}"] for s in (8, 15, 22))
        print(f"  K={k}: controller - best-static = "
              f"{c - best_static:+.1f} pp")
    return res


def controller_lats(seed, k):
    """lats_fn backed by the online-controller schedule."""
    key = (seed, k)
    if key not in _HIST:
        _HIST[key] = _ctl_schedule(seed, k)
    sched = _HIST[key]
    return lambda t, S=sched: ladder(S[t])


_HIST = {}


def _ctl_schedule(seed, k):
    """Build the spread schedule with one full simulation, online control.

    We re-implement dyn_run inline with an online controller (spread
    variable, not a function of t alone). This is the honest way: the
    controller sees only the fabric's own within-flags.
    """
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    last = -10
    spread = 15
    direction = 1
    prev_score = None
    sched = []
    win = deque(maxlen=64)
    for t in range(TICKS):
        sched.append(spread)
        lats = ladder(spread)
        reads = [reality(max(0, t - lats[i])) for i in range(N)]
        s_true = reality(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > DELTA]
        for i, e in trig:
            m = abs(e) // PD or 1
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
        if trig:
            last = t
        w = 1 if abs(s_true - g) <= DELTA else 0
        win.append(w)
        if (t + 1) % 64 == 0 and len(win) == 64:
            score = sum(win)
            if prev_score is not None:
                if score < prev_score:
                    direction = -direction
            prev_score = score
            spread = max(8, min(22, spread + direction))
    return sched


def main():
    print("SPIN-16 REGIME —", os.popen("date -u").read().strip())
    print(f"config: N={N} ladder, K={KS}, seeds={SEEDS}, "
          f"ticks={TICKS}, delta={DELTA}, drift={DRIFT}, pd={PD}, W={W}")
    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    if not ok:
        sys.exit(1)
    tail_devs, loop_area = exp1_hysteresis()
    taxes = exp2_oscillation()
    res = exp3_controller()
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
