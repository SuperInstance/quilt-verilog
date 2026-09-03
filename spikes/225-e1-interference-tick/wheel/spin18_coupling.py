#!/usr/bin/env python3
"""SPIN 18, spoke 7 = COUPLING: REGIME RESONANCE MAP (SPIN-17 follow-up).

Pre-registered hypothesis: the regime-switching tax is a RESONANCE coupling
between the spread-oscillation schedule and reality's 240-tick cycle.
Tests (per SPIN-17's next-spoke proposal):
EXP1  RESONANCE MAP: tax (BOTH gaps: vs TWmean and vs matched-mean static)
      over K in {1,2,4,8,16} x P in {8..256} x phase in {aligned (hi-phase
      starts tick 0), anti-aligned (offset P/2), incommensurate (P=100/140)}.
      Prediction: tax peak follows a K x P law (max when pulse-superposition
      lifetime ~ 240/2); does anti-alignment cancel the K=2 P=16
      catastrophe (27.0pp -> ?)?
EXP2  GUERRILLA DUTY: K=2, P in {16,64}, duty in {5,10,15,20,25,40,60,75,90}.
      Find duty maximizing damage per unit bad-regime time:
      (mmS - osc) / (duty_fraction * P).
EXP3  PHASE-OFFSET FINE SWEEP: K=2, P=16, offset in {0,1,2,4,6,8} ticks —
      smooth (resonance) or lattice-quantized?

Config: N=6 ladder, delta=12, drift=6, pd=3, 4800 ticks, seeds
{1,7,42,1999,20260902}. Integer-only in every loop; floats at print/fit.
Instrument: dyn_run — canary-proven verbatim clone of exp_glm1.run_fabric
interference arm, k as a PARAMETER, single-pass inline scheduling.
SPIN-17 scars honored: phase-order pinned (offset parameter, explicit),
both baselines always, K swept before declaring K-laws.
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
KS = (1, 2, 4, 8, 16)
PERIODS = (8, 16, 24, 32, 48, 64, 96, 120, 128, 192, 240, 256)
INCOMMENSURATE_P = (100, 140)
T0 = time.time()


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


# ------------------------------------------------- instrument (verbatim clone)
def dyn_run(lats_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA, drift=DRIFT,
            seed=20260902):
    """run_fabric interference arm, lats per-tick, k as a PARAMETER.
    Verbatim physics (canary a proves byte-identity)."""
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
        resid.append(abs(s_true - g))
    return resid


def pct(window, delta=DELTA):
    return within_pm(window, delta) / 10.0


def mean(v):
    return sum(v) / len(v)


# --------------------------------------------------------- schedulers
def square_schedule(P, lo, hi, duty100=50, ticks=TICKS, offset=0):
    """Duty-percent square, integer tick counts, phase pinned by `offset`
    (SPIN-17 scar #1): hi-phase nominally starts at tick `offset`; we
    implement in_hi = ((t - offset) mod P) < hi_ticks so offset=0 means
    hi-phase starts at tick 0 ('aligned'), offset=P//2 is 'anti-aligned'."""
    hi_ticks = P * duty100 // 100
    sched = []
    for t in range(ticks):
        in_hi = ((t - offset) % P) < hi_ticks
        sched.append(hi if in_hi else lo)
    return sched


def sched_fn(sched):
    return lambda t, S=sched: ladder(S[t])


def static_fn(s):
    return lambda t, L=ladder(s): L


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: wiring byte-identity dyn_run vs run_fabric ==")
    nchk = 0
    for lats, k, sd in (("zero@0", 1, 1), ("ladder@15", 1, 42),
                        ("ladder@30", 2, 7), ("zero@0", 4, 42),
                        ("ladder@15", 4, 1999), ("ladder@30", 8, 20260902)):
        s = 0 if "zero" in lats else int(lats.split("@")[1])
        a = run_fabric("interference", TICKS, ladder(s), K=k, pd=PD,
                       delta=DELTA, drift=DRIFT, seed=sd)["resid"]
        b = dyn_run(static_fn(s), k=k, seed=sd)
        nchk += 1
        if a != b:
            ok = False
            print(f"  MISMATCH {lats} K={k} seed={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} configs byte-identical")

    print("\n== CANARY b: anchor replays (5-seed means) ==")
    for name, s, k, want_tp, want_ev, want_debt in (
            ("zero@15   K=1", 0, 1, 77.3, 8756, 187834),
            ("ladder@15 K=1", 15, 1, 71.5, 5792, 106378)):
        lats = ladder(s)
        rs = [pct(dyn_run(static_fn(s), k=k, seed=sd)) for sd in SEEDS]
        tp = mean(rs)
        rf = [run_fabric("interference", TICKS, lats, K=k, pd=PD,
                         delta=DELTA, drift=DRIFT, seed=sd) for sd in SEEDS]
        ev = mean([r["events"] for r in rf])
        dbt = mean([r["mass"] for r in rf])
        good = (abs(tp - want_tp) <= 0.2 and abs(ev - want_ev) <= 2
                and abs(dbt - want_debt) <= 300)
        ok &= good
        print(f"  {name}: {tp:.1f}% (want {want_tp})  ev {ev:.0f} "
              f"(want {want_ev})  debt {dbt:.0f} (want {want_debt})  "
              f"-> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY c: no-shift identity — hold-5 via scheduler path ==")
    c3 = True
    for k in KS:
        for off in (0, 8):
            sched = square_schedule(16, 5, 5, duty100=50, offset=off)
            for sd in SEEDS:
                if dyn_run(sched_fn(sched), k=k, seed=sd) != \
                        dyn_run(static_fn(5), k=k, seed=sd):
                    c3 = False
    print(f"  sched-path hold-5 (offset 0 and 8) == static-5, K in {KS}, "
          f"5 seeds: {'PASS' if c3 else 'FAIL'}")
    return ok and c3


# --------------------------------------------------------------- EXP 1
_static_cache = {}


def static_pct(s, k):
    key = (s, k)
    if key not in _static_cache:
        _static_cache[key] = [pct(dyn_run(static_fn(s), k=k, seed=sd))
                              for sd in SEEDS]
    return _static_cache[key]


def run_cell(k, P, duty, offset, st5, st30, duty_frac):
    """One (k,P,duty,offset) cell: returns osc mean, twm, mms mean."""
    sched = square_schedule(P, 5, 30, duty, offset=offset)
    oscs = [pct(dyn_run(sched_fn(sched), k=k, seed=sd)) for sd in SEEDS]
    f = duty_frac
    twm = mean([a * (1 - f) + b * f for a, b in zip(st5, st30)])
    mm = ladder(round(5 * (1 - f) + 30 * f))
    mms = mean(static_pct(round(5 * (1 - f) + 30 * f), k))
    return mean(oscs), twm, mms


def exp1_resonance():
    print("\n== EXP 1: RESONANCE MAP — 5<->30 square duty-50, "
          "K x P x phase ==")
    print("  gaps reported BOTH ways: tax = TWmean - osc; dmm = osc - mmS "
          "(negative = damage vs matched-mean static)")
    print("  phases: ALIGNED = hi-phase starts tick 0; ANTI = offset P/2; "
          "INCOMM = P in {100,140} (aligned) — both shown separately")
    grid = {}   # (P, k, phase) -> (osc, twm, mms)
    for k in KS:
        st5, st30 = static_pct(5, k), static_pct(30, k)
        print(f"\n-- K={k}: static5={mean(st5):.1f} static30={mean(st30):.1f}"
              f" --")
        print(f"{'P':>5}{'ali%':>7}{'tax':>7}{'dmm':>7}"
              f"{'anti%':>7}{'tax':>7}{'dmm':>7}{'d(osc)':>7}")
        for P in PERIODS:
            o_a, twm, mms = run_cell(k, P, 50, 0, st5, st30, 0.5)
            o_n, twm2, mms2 = run_cell(k, P, 50, P // 2, st5, st30, 0.5)
            assert twm == twm2 and mms == mms2
            grid[(P, k, "ali")] = (o_a, twm, mms)
            grid[(P, k, "anti")] = (o_n, twm, mms)
            print(f"{P:>5}{o_a:>7.1f}{twm - o_a:>7.1f}{o_a - mms:>7.1f}"
                  f"{o_n:>7.1f}{twm - o_n:>7.1f}{o_n - mms:>7.1f}"
                  f"{o_n - o_a:>7.1f}")
        for P in INCOMMENSURATE_P:
            o_i, twm, mms = run_cell(k, P, 50, 0, st5, st30, 0.5)
            grid[(P, k, "inc")] = (o_i, twm, mms)
            print(f"{P:>5}{o_i:>7.1f}{twm - o_i:>7.1f}{o_i - mms:>7.1f}"
                  f"{'(incommensurate)':>22}")

    # SPIN-17 replay check (K=2, aligned column is offset convention? note:
    # SPIN-17 lo-first = hi occupies LAST half; ours offset=0 = hi FIRST
    # half = SPIN-17's 'hi-first/invert'. So replay vs both, and report.)
    print("\n-- SPIN-17 replay check (K=2 tax vs TWmean): "
          "want 27.0 @16, 11.7 @64, 1.7 @256 (lo-first conv) --")
    for P, want in ((16, 27.0), (64, 11.7), (256, 1.7)):
        # lo-first = hi last half = our offset = P//2
        o, twm, _ = grid[(P, 2, "anti")]
        print(f"  P={P}: tax={twm - o:.1f} (want {want}) "
              f"{'PASS' if abs((twm - o) - want) <= 0.6 else 'CHECK'}")

    print("\n-- PEAK LAW: argmax_P tax per K per phase; K*P at peak; "
          "is peak P ~ 240/(2*K)? --")
    for phase in ("ali", "anti"):
        print(f" phase={phase}")
        for k in KS:
            pts = [(P, grid[(P, k, phase)][1] - grid[(P, k, phase)][0])
                   for P in PERIODS]
            pmax, tmax = max(pts, key=lambda x: x[1])
            print(f"  K={k:>2}: peak tax {tmax:6.1f} @ P={pmax:>3}"
                  f"  K*P={k * pmax:>5}  240/(2K)={240 // (2 * k):>3}")
    print(" phase=inc (P in {100,140})")
    for k in KS:
        pts = [(P, grid[(P, k, 'inc')][1] - grid[(P, k, 'inc')][0])
               for P in INCOMMENSURATE_P]
        for P, tx in pts:
            print(f"  K={k:>2}: P={P:>3} tax {tx:6.1f}")
    return grid


# --------------------------------------------------------------- EXP 2
def exp2_guerrilla():
    print("\n== EXP 2: GUERRILLA DUTY — K=2, 30 for duty% of P, 5 rest ==")
    print("  damage-per-unit-bad-time = (mmS - osc) / (duty_frac * P)")
    print(f"{'P':>4}{'duty':>6}{'osc%':>7}{'TWm%':>7}{'tax':>7}{'mmS%':>7}"
          f"{'dmm':>7}{'D/tick':>8}")
    best = {}
    k = 2
    st5, st30 = static_pct(5, k), static_pct(30, k)
    for P in (16, 64):
        for duty in (5, 10, 15, 20, 25, 40, 60, 75, 90):
            f = duty / 100.0
            o, twm, mms = run_cell(k, P, duty, 0, st5, st30, f)
            dmg = (mms - o) / (f * P)
            best[(P, duty)] = (o, twm, mms, dmg)
            print(f"{P:>4}{duty:>6}{o:>7.1f}{twm:>7.1f}{twm - o:>7.1f}"
                  f"{mms:>7.1f}{o - mms:>7.1f}{dmg:>8.3f}")
    for P in (16, 64):
        bd = max(d for (p, d), (_, _, _, d) in best.items() if p == P)
        print(f"  best damage-rate @ P={P}: duty="
              f"{[d for (p, d), v in best.items() if p == P and v[3] == bd][0]}"
              f"%  D/tick={bd:.3f}")
    # SPIN-17 anchor: duty-25 @ P=16 K=2 = 34.6 osc, -53.5pp vs mmS
    # (SPIN-17 used lo-first convention; ours offset=0 is hi-first)
    return best


# --------------------------------------------------------------- EXP 3
def exp3_fine_phase():
    print("\n== EXP 3: PHASE-OFFSET FINE SWEEP — K=2, P=16, duty-50 ==")
    print(f"{'offset':>7}{'osc%':>7}{'tax':>7}{'dmm':>7}")
    k = 2
    st5, st30 = static_pct(5, k), static_pct(30, k)
    outs = {}
    for off in (0, 1, 2, 4, 6, 8):
        sched = square_schedule(16, 5, 30, 50, offset=off)
        oscs = [pct(dyn_run(sched_fn(sched), k=k, seed=sd)) for sd in SEEDS]
        twm = mean([(a + b) / 2.0 for a, b in zip(st5, st30)])
        mms = mean(static_pct(18, k))
        outs[off] = (mean(oscs), twm, mms)
        print(f"{off:>7}{mean(oscs):>7.1f}{twm - mean(oscs):>7.1f}"
              f"{mean(oscs) - mms:>7.1f}")
    spread = max(v[0] for v in outs.values()) - min(v[0] for v in outs.values())
    print(f"  osc spread across offsets {0}..8: {spread:.1f} pp "
          f"(smooth-resonance if graded steps; lattice if plateaus)")
    return outs


def main():
    print("SPIN-18 COUPLING — REGIME RESONANCE MAP — "
          + os.popen("date -u").read().strip())
    print(f"config: N={N} ladder, K={KS}, seeds={SEEDS}, ticks={TICKS}, "
          f"delta={DELTA}, drift={DRIFT}, pd={PD}; reality period 240")
    ok = canaries()
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    if not ok:
        sys.exit(1)
    exp1_resonance()
    exp2_guerrilla()
    exp3_fine_phase()
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
