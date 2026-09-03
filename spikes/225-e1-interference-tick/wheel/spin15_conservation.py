#!/usr/bin/env python3
"""SPIN 15, SPOKE: CONSERVATION — re-dispatch of failed SPIN-12 conservation
lane (brief preserved verbatim). Closure sweep on the E1 interference fabric.

Sub-claims (from the brief):
  (1) MASS CLOSURE: mass - sum(|trigger err|) == 0 exactly, every run.
  (2) DEBT ADDITIVITY: global debt == sum of per-twin toll subledgers,
      integer-exact, every run.
  (3) TOLL-PER-EVENT GRAMMAR-INVARIANCE at fixed K: does debt/events depend
      on the grammar, or only on K and occupancy?
  (4) SATURATION: escalate stress on the worst grammar hunting a debt/event
      cap. Is there a ceiling, and where?

Design notes / what went wrong last time (spin12_conservation.py, failed):
  its ledger clone decayed negative pulses as mag = mag - (-( -mag)//2),
  which does NOT match run_fabric's mag = mag - (mag//2) (Python floor div)
  for negative odd mags — a byte-identity canary killer. This clone calls
  mag//2 directly, identical semantics, no re-derivation.

Honesty note: closure and additivity are checked against ledgers built in
the same pass as the mass counter, so they are wiring invariants (they catch
instrumentation bugs, they cannot detect a harness-level misbook). The
NON-trivial conservation laws are the pulse-mass identity
  emitted_signed == decay_loss + inflight + expired_residual
(telescoping per pulse: pm -> successive (mag//2) removals -> residual;
draft 1 omitted the expiry channel — pulses whose life expires carry an
un-decayed residual that the fabric SILENTLY DESTROYS at expiry. That
channel is real booked physics: mass evaporation, measured below)
and the trajectory identity
  g_final == g0 + drift_total + net_total
which close over four independently accumulated counters.

Integer-only inside every loop; floats only at print/display time
(established wheel precedent). Grammars: 6 (ladder@15, ladder@30, zero,
cohort3+3, kcoh5@15, outlier@30). K in {1,2,4,8}. Seeds {1,7,42,1999,20260902}.
Stress: delta=12 drift=6 pd=3, 4800 ticks.

CANARIES (all must PASS or nothing counts):
  C1 wiring byte-identity vs exp_glm1.run_fabric, >=8 configs.
  C2 SPIN-11 anchor replay: ladder@15 K=1 ~71.5% ev 5792 debt 106378;
     zero@15 K=1 ~77.3% debt 187834 (small rounding tolerance).
  C3 closure identities exact on the anchor baselines, every seed.
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
KS = (1, 2, 4, 8)
T0 = time.time()


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


GRAMMARS = (
    ("ladder@15", ladder(15)),
    ("ladder@30", ladder(30)),
    ("zero", [0] * N),
    ("cohort3+3", [0, 0, 0, 15, 15, 15]),
    ("kcoh5@15", [0, 0, 0, 0, 0, 15]),
    ("outlier@30", [0, 0, 0, 0, 0, 30]),
)
GRM = dict(GRAMMARS)


def run_ledger(lats, k, seed, ticks=TICKS, delta=DELTA, drift=DRIFT, pd=PD):
    """Faithful clone of run_fabric interference arm + conservation ledger.

    Every line that touches g / pulses is copied verbatim from exp_glm1
    (floor-div decay mag = mag - (mag//2)), so C1 byte-identity can hold.
    Ledger (all exact ints):
      toll[i]   per-twin toll subledger
      emitted_signed / emitted_abs   pulse accounting at emission
      net_total   sum of net injections into g
      decay_loss  sum of (mag // 2) removed at each decay step
      inflight    signed sum of pulse mags alive at run end
      drift_total, g0, g_final
    """
    rng = LCG(seed)
    g = reality(0)
    g0 = g
    pulses = deque()
    n = len(lats)
    events = mass = cancels = chatter = settles = 0
    last = -10
    resid = []
    cflags = []
    emissions = []
    toll = [0] * n
    emitted_abs = emitted_signed = net_total = decay_loss = drift_total = 0
    expired_total = 0

    for t in range(ticks):
        reads = [reality(max(0, t - lats[i])) for i in range(n)]
        s_true = reality(t)
        d = rng.below(2 * drift + 1) - drift
        g += d
        drift_total += d

        while pulses and pulses[-1][1] == 0:
            expired_total += pulses[-1][0]
            pulses.pop()

        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > delta]

        cflag = 0
        for i, e in trig:
            m = abs(e) // pd or 1
            pm = m if e > 0 else -m
            pulses.appendleft([pm, k])
            events += 1
            mass += abs(e)
            toll[i] += abs(e)
            emissions.append((t, i, pm, e))
            emitted_abs += abs(pm)
            emitted_signed += pm
        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and any(p[0] > 0 for p in pulses) \
                    and any(p[0] < 0 for p in pulses):
                cancels += 1
                cflag = 1
            g += net
            net_total += net
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        decay_loss += mag // 2       # removed amount, floor div
                        mag = mag - (mag // 2)       # verbatim run_fabric decay
                    decayed.append([mag, life - 1])
            pulses = decayed
        if trig:
            if t - last == 1:
                chatter += 1
            last = t

        resid.append(abs(s_true - g))
        cflags.append(cflag)
        if all(abs(r - g) <= delta for r in reads):
            settles += 1

    inflight = sum(p[0] for p in pulses)
    d = dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
             settles=settles, resid=resid, cflags=cflags,
             emissions=emissions, audit=None, ticks=ticks)
    d["ledger"] = dict(toll=toll, emitted_abs=emitted_abs,
                       emitted_signed=emitted_signed, net_total=net_total,
                       decay_loss=decay_loss, inflight=inflight,
                       expired_total=expired_total,
                       drift_total=drift_total, g_final=g, g0=g0)
    return d


def mean(v):
    return sum(v) / len(v)      # display only


def row(cells, w=11):
    return " | ".join(f"{c:>{w}}" for c in cells)


def check_identities(r):
    led = r["ledger"]
    return dict(
        closure=r["mass"] == sum(abs(e) for (_, _, _, e) in r["emissions"]),
        additivity=r["mass"] == sum(led["toll"]),
        pulse_flow=led["emitted_signed"] == led["decay_loss"]
        + led["inflight"] + led["expired_total"],
        trajectory=led["g_final"] == led["g0"] + led["drift_total"]
        + led["net_total"],
    )


# ------------------------------------------------------------ canaries
def canary_c1():
    print("== CANARY C1: wiring byte-identity vs exp_glm1.run_fabric ==")
    ok = True
    ncfg = 0
    for name, lats in (GRAMMARS[0], GRAMMARS[1], GRAMMARS[2], GRAMMARS[3],
                       GRAMMARS[4], GRAMMARS[5]):
        for k in (1, 8):
            for s in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=s)
                b = run_ledger(lats, k, s)
                ncfg += 1
                same = a == {kk: b[kk] for kk in a}
                if not same:
                    ok = False
                    print(f"  MISMATCH {name} K={k} seed={s}")
    print(f"  {'PASS' if ok else 'FAIL'}: {ncfg}/{ncfg} configs, every "
          f"run_fabric key byte-identical (6 grammars x K{{1,8}} x seeds "
          f"{{1,42}})")
    return ok


def canary_c2():
    ok = True
    print("\n== CANARY C2: SPIN-11 anchor replay (adversary=none) ==")
    checks = (("ladder@15 K=1", "ladder@15", 1, 71.5, 5792, 106378),
              ("zero@15   K=1", "zero", 1, 77.3, None, 187834))
    for name, gname, k, want_tp, want_ev, want_debt in checks:
        rs = [run_ledger(GRM[gname], k, s) for s in SEEDS]
        tp = mean([within_pm(r["resid"], DELTA) for r in rs]) / 10
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        good = (abs(tp - want_tp) <= 0.2
                and (want_ev is None or abs(ev - want_ev) <= 2)
                and abs(dbt - want_debt) <= 300)
        ok &= good
        print(f"  {name}: {tp:.1f}% (want {want_tp})  ev {ev:.0f} "
              f"(want {want_ev})  debt {dbt:.0f} (want {want_debt})  "
              f"-> {'PASS' if good else 'FAIL'}")
    return ok


def canary_c3():
    print("\n== CANARY C3: closure identities exact on anchors, all seeds ==")
    ok = True
    for name, lats in (("ladder@15", GRM["ladder@15"]),
                       ("zero", GRM["zero"])):
        for s in SEEDS:
            r = run_ledger(lats, 1, s)
            ids = check_identities(r)
            if not all(ids.values()):
                ok = False
                print(f"  FAIL {name} seed={s}: {ids}")
    print(f"  {'PASS' if ok else 'FAIL'}: closure/additivity/pulse-flow/"
          f"trajectory all exact (2 grammars x 5 seeds)")
    return ok


# ------------------------------------------------------- experiments
def exp1_closure_sweep():
    print("\n== EXP 1: closure sweep — 6 grammars x K{1,2,4,8} x 5 seeds ==")
    print(row(["grammar", "K", "resid%", "ev", "debt", "debt/ev",
               "pulseAbs/ev", "cancel", "chat", "maxRes", "IDs"]))
    results = {}
    worst = None
    for name, lats in GRAMMARS:
        for k in KS:
            rs = [run_ledger(lats, k, s) for s in SEEDS]
            ids = all(all(check_identities(r).values()) for r in rs)
            tp = mean([within_pm(r["resid"], DELTA) for r in rs]) / 10
            ev = mean([r["events"] for r in rs])
            dbt = mean([r["mass"] for r in rs])
            pabs = mean([r["ledger"]["emitted_abs"] for r in rs])
            results[(name, k)] = (tp, ev, dbt)
            if ids and (worst is None or tp < worst[1]):
                worst = (name, tp)
            print(row([name, k, f"{tp:.1f}", f"{ev:.0f}", f"{dbt:.0f}",
                       f"{dbt / ev:.1f}", f"{pabs / ev:.1f}",
                       f"{mean([r['cancels'] for r in rs]):.0f}",
                       f"{mean([r['chatter'] for r in rs]):.0f}",
                       max(max(r["resid"]) for r in rs),
                       "4/4" if ids else "FAIL"]))
    print(f"\n  worst grammar by residency (any K): {worst[0]} "
          f"({worst[1]:.1f}%) -> saturation-hunt target")
    return results, worst[0]


def exp2_toll_invariance(results):
    print("\n== EXP 2: toll-per-event (debt/ev) across grammars at fixed K ==")
    out = {}
    for k in KS:
        vals = [(nm, results[(nm, k)][2] / results[(nm, k)][1])
                for nm, _ in GRAMMARS]
        nums = [v for _, v in vals]
        spread = (max(nums) - min(nums)) / (sum(nums) / len(nums)) * 100
        lo = min(vals, key=lambda x: x[1])
        hi = max(vals, key=lambda x: x[1])
        out[k] = (lo, hi, spread)
        print(f"  K={k}: " + "  ".join(f"{nm} {v:.1f}" for nm, v in vals))
        print(f"        min {lo[1]:.1f} ({lo[0]})  max {hi[1]:.1f} "
              f"({hi[0]})  rel-spread {spread:.1f}%")
    return out


def exp3_saturation(gname):
    lats = GRM[gname]
    print(f"\n== EXP 3: saturation hunt on worst grammar ({gname}, K=1) ==")
    print("   arm A: drift escalation, delta=12 fixed")
    print(row(["drift", "resid%", "ev", "debt", "debt/ev", "pulseAbs/ev",
               "|net|/ev", "|decay|/ev", "|evap|/ev", "IDs"]))
    armA = []
    for drift in (6, 12, 24, 48, 96, 192, 384):
        rs = [run_ledger(lats, 1, s, drift=drift) for s in SEEDS]
        ids = all(all(check_identities(r).values()) for r in rs)
        tp = mean([within_pm(r["resid"], DELTA) for r in rs]) / 10
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        pabs = mean([r["ledger"]["emitted_abs"] for r in rs])
        nabs = mean([abs(r["ledger"]["net_total"]) for r in rs])
        dec = mean([abs(r["ledger"]["decay_loss"]) for r in rs])
        exp_ = mean([abs(r["ledger"]["expired_total"]) for r in rs])
        armA.append((drift, dbt / ev))
        print(row([drift, f"{tp:.1f}", f"{ev:.0f}", f"{dbt:.0f}",
                   f"{dbt / ev:.1f}", f"{pabs / ev:.1f}", f"{nabs / ev:.1f}",
                   f"{dec / ev:.1f}", f"{exp_ / ev:.2f}",
                   "4/4" if ids else "FAIL"]))

    print("\n   arm B: delta tightening (drift=6 fixed) — tighter spread, "
          "more events")
    print(row(["delta", "resid%", "ev", "debt", "debt/ev", "IDs"]))
    armB = []
    for delta in (12, 8, 6, 4, 2, 1):
        rs = [run_ledger(lats, 1, s, delta=delta) for s in SEEDS]
        ids = all(all(check_identities(r).values()) for r in rs)
        tp = mean([within_pm(r["resid"], delta) for r in rs]) / 10
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        armB.append((delta, dbt / ev))
        print(row([delta, f"{tp:.1f}", f"{ev:.0f}", f"{dbt:.0f}",
                   f"{dbt / ev:.1f}", "4/4" if ids else "FAIL"]))

    print("\n   arm C: tick escalation (drift 6, delta 12) — debt/ev "
          "stationarity")
    print(row(["ticks", "resid%", "ev", "debt", "debt/ev", "IDs"]))
    for ticks in (4800, 9600, 19200, 38400):
        rs = [run_ledger(lats, 1, s, ticks=ticks) for s in SEEDS]
        ids = all(all(check_identities(r).values()) for r in rs)
        tp = mean([within_pm(r["resid"], DELTA) for r in rs]) / 10
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        print(row([ticks, f"{tp:.1f}", f"{ev:.0f}", f"{dbt:.0f}",
                   f"{dbt / ev:.1f}", "4/4" if ids else "FAIL"]))
    return armA, armB


def main():
    print("SPIN-15 CONSERVATION —", os.popen("date -u").read().strip())
    ok = canary_c1() & canary_c2() & canary_c3()
    print("\nALL CANARIES:", "PASS" if ok else
          "FAIL — nothing below counts")
    if not ok:
        sys.exit(1)
    results, worst = exp1_closure_sweep()
    exp2_toll_invariance(results)
    exp3_saturation(worst)
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
