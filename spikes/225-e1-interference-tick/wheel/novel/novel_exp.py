#!/usr/bin/env python3
"""NOVEL LANE — spin 6-candidate experiments N1 + N2 (see NOVEL-DESIGN.md).

N1  SLOPE-LAW (channel-memory rescue): spin-dequant-2 booked the honest
    scope "K>1 earning its keep would need a channel with useful phase."
    Nobody has tested it. Slope-controlled triangle channels (integer,
    period 240) at per-tick slope sigma in {2,3,4,6,8,16} (~1.3-10x the e1
    home ramp), K in {1,2,4,8}, e1-home conflict pair lats=[0,10],
    stress params, 5 seeds. H1: exists sigma* above which pm(K) turns
    INCREASING in K (stacked pulse velocity pays when error regrows
    fast). Falsified if pm strictly decreasing in K at every sigma.

N2  ORIGIN-DIP DECORRELATION (phase-offset duplicate schedules): spin-4
    found spread=0 (synchronized duplicates) WORSE than spread=5 (U-shape
    at the origin). Mechanism untested. H2 (simultaneous-fire resonance):
    spread=1 already recovers most of the dip (>=88% residency at K=1)
    and events collapse toward spread-5 levels. Alternative (gradual
    mass/debt story): slow recovery across 0->5.

Self-canaries (mandatory, run first):
  A  byte-identity: run2 (this port, pluggable reality) with e1 reality
     == exp_glm1.run_fabric EXACTLY (full dict incl. resid/emissions)
     on both modes x K in {1,8} x lats [0]*6 and [0,10] — catches any
     port drift (name-map/geometry bug class).
  B  prior-spin replay: spin-4 published means ladder(spread=15) K=1/2/8
     true% 71.5 / 60.0 / 70.7 (+-0.15) and spread 0/5 anchor rows.

Integer-only inside every loop (Python ints, floor div, LCG contract:
fdiv decay, 64-bit intermediate, FIFO oldest-first expiry, snapshot
decay). Floats only in display means, same as spin1/spin4 drivers.
"""
import sys
sys.path.insert(0, "inventors-derby")
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402
from collections import deque

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
N = 6


# ---------------- pluggable-reality port of run_fabric ----------------
def run2(mode, ticks, lats, reality_fn, K=4, pd=3, delta=12, drift=6,
         seed=20260902):
    """exp_glm1.run_fabric with reality_fn(t) replacing the pinned ramp.
    Ops/order copied verbatim; canary A proves byte-identity at e1 reality."""
    rng = LCG(seed)
    g = reality_fn(0)
    pulses = deque()
    n = len(lats)
    events = mass = cancels = chatter = settles = 0
    last = -10
    resid = []
    cflags = []
    emissions = []

    for t in range(ticks):
        reads = [reality_fn(max(0, t - lats[i])) for i in range(n)]
        s_true = reality_fn(t)
        g += rng.below(2 * drift + 1) - drift

        while pulses and pulses[-1][1] == 0:      # FIFO, oldest-first expiry
            pulses.pop()

        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > delta]

        cflag = 0
        if mode == "sequential":
            if trig:
                i, e = trig[0]
                g += e
                events += 1
                mass += abs(e)
                emissions.append((t, i, e, e))
                if t - last == 1:
                    chatter += 1
                last = t
        else:
            for i, e in trig:
                m = abs(e) // pd or 1
                pm = m if e > 0 else -m
                pulses.appendleft([pm, K])
                events += 1
                mass += abs(e)
                emissions.append((t, i, pm, e))
            if pulses:
                net = sum(p[0] for p in pulses)
                if net == 0 and any(p[0] > 0 for p in pulses) \
                        and any(p[0] < 0 for p in pulses):
                    cancels += 1
                    cflag = 1
                decayed = deque()                   # snapshot decay
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)  # fdiv sign-safe
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
            if trig:
                if t - last == 1:
                    chatter += 1
                last = t

        resid.append(abs(s_true - g))
        cflags.append(cflag)
        if all(abs(r - g) <= delta for r in reads):
            settles += 1

    return dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
                settles=settles, resid=resid, cflags=cflags,
                emissions=emissions, audit=None, ticks=ticks)


# ---------------- channels (integer, period 240) ----------------
def tri(sigma):
    """Triangle channel, per-tick slope sigma, period 240, base 400."""
    def f(t):
        ph = t % 240
        if ph < 120:
            return 400 + ph * sigma
        return 400 + 120 * sigma - (ph - 120) * sigma
    return f


def one(mode, lats, k, seed, rf=None):
    if rf is None:
        r = run_fabric(mode, 4800, lats, K=k, pd=3,
                       delta=DELTA, drift=6, seed=seed)
    else:
        r = run2(mode, 4800, lats, rf, K=k, pd=3,
                 delta=DELTA, drift=6, seed=seed)
    return dict(true_pm=within_pm(r["resid"], DELTA),
                events=r["events"], debt=r["mass"],
                cancels=r["cancels"], maxe=max(r["resid"]))


def mean(v):
    return sum(v) / len(v)   # display only


def row(cells):
    return " | ".join(f"{c:>9}" for c in cells)


def ladder(s, n=N):
    return [round(i * s / (n - 1)) for i in range(n)]


def canaries():
    print("== CANARY A: run2(reality) byte-identical to run_fabric ==")
    ok = True
    for mode in ("sequential", "interference"):
        for lats in ([0] * 6, [0, 10]):
            for k in (1, 8):
                a = run_fabric(mode, 4800, lats, K=k, pd=3,
                               delta=DELTA, drift=6, seed=SEEDS[0])
                b = run2(mode, 4800, lats, reality, K=k, pd=3,
                         delta=DELTA, drift=6, seed=SEEDS[0])
                if a != b:
                    ok = False
                    print(f"  MISMATCH {mode} {lats} K={k}")
    print("  PASS: 8/8 configs full-dict identical" if ok else "  FAIL")

    print("\n== CANARY B: spin-4 replay (ladder N=6, mean of 5 seeds) ==")
    print(row(["spread", "K", "true%", "s4true%"]))
    anchors = {(0, 1): 77.3, (0, 2): 50.0, (0, 8): 69.0,
               (5, 1): 97.6, (5, 2): 84.9, (5, 8): 90.2,
               (15, 1): 71.5, (15, 2): 60.0, (15, 8): 70.7}
    ok2 = True
    for (s, k), want in anchors.items():
        got = mean([one("interference", ladder(s), k, sd)["true_pm"]
                    for sd in SEEDS]) / 10
        m = abs(got - want) <= 0.15
        ok2 &= m
        print(row([s, k, f"{got:.1f}", want]) + ("  OK" if m else "  DRIFT"))
    print("  spin-4 replay OK" if ok2 else "  spin-4 replay DRIFTED")
    return ok and ok2


def n1_slope_law():
    print("\n== N1 SLOPE-LAW: pm vs K across channel slope sigma "
          "(lats=[0,10], stress, pd=3) ==")
    print(row(["channel", "K", "s1", "s7", "s42", "s1999", "s2026",
               "mean%", "evMean", "debtMean", "maxE"]))
    slopes = [2, 3, 4, 6, 8, 16]
    chans = [("e1ramp~1.6", None)] + [(f"tri{g}", tri(g)) for g in slopes]
    table = {}
    for cname, rf in chans:
        for k in (1, 2, 4, 8):
            res = [one("interference", [0, 10], k, sd, rf) for sd in SEEDS]
            tp = [r["true_pm"] for r in res]
            table[(cname, k)] = mean(tp) / 10
            print(row([cname, k] + tp +
                      [f"{mean(tp)/10:.1f}",
                       f"{mean([r['events'] for r in res]):.0f}",
                       f"{mean([r['debt'] for r in res]):.0f}",
                       f"{max(r['maxe'] for r in res)}"]))
    print("\n-- N1 sequential reference (impulse, no memory) --")
    print(row(["channel", "mean%", "evMean", "debtMean", "maxE"]))
    for cname, rf in chans:
        res = [one("sequential", [0, 10], 1, sd, rf) for sd in SEEDS]
        print(row([cname,
                   f"{mean([r['true_pm'] for r in res])/10:.1f}",
                   f"{mean([r['events'] for r in res]):.0f}",
                   f"{mean([r['debt'] for r in res]):.0f}",
                   f"{max(r['maxe'] for r in res)}"]))
    print("\n-- N1 verdict input: pm(K=8)-pm(K=1) per channel --")
    for cname, _ in chans:
        d = table[(cname, 8)] - table[(cname, 1)]
        print(f"  {cname:>12}: {d:+.1f} pp   "
              f"(K1 {table[(cname,1)]:.1f} -> K8 {table[(cname,8)]:.1f})")


def n2_origin_dip():
    print("\n== N2 ORIGIN-DIP: fine spreads 0..5 + phase-offset ring@1 "
          "(N=6, stress, K in {1,2,8}) ==")
    print(row(["lats", "K", "mean%", "allW", "evMean", "debtMean", "canc"]))
    cfgs = []
    for s in (0, 1, 2, 3, 5):
        cfgs.append((f"lad{s}", ladder(s)))
    cfgs.append(("ring1", [0, 1, 0, 1, 0, 1]))
    cfgs.append(("cohort1", [0, 0, 0, 1, 1, 1]))
    for name, lats in cfgs:
        for k in (1, 2, 8):
            res = [one("interference", lats, k, sd) for sd in SEEDS]
            print(row([f"{name}{lats if 'lad' not in name else ''}", k,
                       f"{mean([r['true_pm'] for r in res])/10:.1f}",
                       f"{mean([1000*r['events']//4800 for r in res])/10:.1f}",
                       f"{mean([r['events'] for r in res]):.0f}",
                       f"{mean([r['debt'] for r in res]):.0f}",
                       f"{mean([r['cancels'] for r in res]):.0f}"]))


def main():
    ok = canaries()
    if not ok:
        print("\nCANARY FAILURE — aborting (no numbers booked)")
        sys.exit(1)
    n1_slope_law()
    n2_origin_dip()


if __name__ == "__main__":
    main()
