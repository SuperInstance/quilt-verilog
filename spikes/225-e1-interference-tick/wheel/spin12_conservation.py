#!/usr/bin/env python3
"""SPIN 12, SPOKE: CONSERVATION — invariants and ledgers across the whole
(grammar x K x stress) operating envelope of the E1 interference fabric.

Sub-hypotheses:
  (H1) ADDITIVITY / CLOSURE: total debt == sum of per-twin toll subledgers
       exactly, and mass closure (mass - sum|trigger| over emissions) == 0,
       at every honest (grammar, K, seed) point. Plus a *physical* ledger
       the returned dict never exposed: pulse-mass conservation
         sum(emitted |pm| signed) == total net injected into g
                                     + total decay loss + in-flight final,
       and the g-trajectory identity
         g_final == g_0 + sum(random drift) + total net.
  (H2) TOLL-PER-EVENT INVARIANCE: toll mass per event (debt/events) is
       grammar-invariant at fixed K — tolls track emissions, not staleness.
  (H3) SATURATION: there exists a toll CAP — at some stress point
       (drift escalation / tick escalation) on the worst grammar,
       debt-per-event stops growing because the pulse budget saturates.

Harness: run_ledger() = faithful clone of exp_glm1.run_fabric (interference
arm: fdiv decay, 64-bit LCG, FIFO oldest-first expiry, snapshot decay) with
an added ledger dict under key 'ledger' — which is why adv=None-style
byte-identity is checked by comparing the shared keys only (the clone adds
exactly one new key; canary C1 proves every run_fabric key is identical).

Integer-only inside every loop; floats ONLY in display statistics at print
time (established wheel precedent).

Config: N=6 grammars ladder@15 [0,3,6,9,12,15], ladder@30 [0,6,12,18,24,30],
zero-lock [0]*6, cohort3+3 [0,0,0,15,15,15], kcoh5@15 [0,0,0,0,0,15],
outlier@30 [0,0,0,0,0,30] (note: outlier@30 multiset == kcoh5@30, booked).
K in {1,2,4,8}, seeds {1,7,42,1999,20260902}, stress (delta=12, drift=6,
pd=3), 4800 ticks.

CANARIES (mandatory, all must PASS before any result counts):
  C1: wiring byte-identity — run_ledger() equals run_fabric() on every
      run_fabric key, >= 8 configs (4 grammars x K{1,8} x seeds {1,42}).
  C2: SPIN-11/5 anchor replay: ladder@15 K=1 71.5% ev 5792 debt 106378;
      zero@15 K=1 77.3% debt 187834.
  C3: honest closure identity on the anchor baselines (delta == 0 exact,
      every seed).
"""
import os
import sys
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


def run_ledger(lats, k, seed, ticks=TICKS, delta=DELTA, drift=DRIFT,
               pd=PD):
    """run_fabric clone (interference arm) + conservation ledger.

    Ledger fields (all exact integers):
      toll[i]        per-twin toll subledger (sum |trigger err| charged)
      emitted_abs    sum of |signed pulse| at emission
      emitted_signed sum of signed pulses at emission
      net_total      sum of net injections into g over all ticks
      decay_loss     sum of (mag // 2) removed by fdiv decay (signed sum of
                     the removed halves, but mags here keep sign; we track
                     the removed amount with sign of its pulse)
      inflight       signed sum of pulse mags alive at run end
      drift_total    sum of random-walk drift steps
      g_final        final g value (trajectory identity check)
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
    emitted_abs = emitted_signed = net_total = decay_loss = 0
    drift_total = 0

    for t in range(ticks):
        reads = [reality(max(0, t - lats[i])) for i in range(n)]
        s_true = reality(t)
        d = rng.below(2 * drift + 1) - drift
        g += d
        drift_total += d

        while pulses and pulses[-1][1] == 0:
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
                        half = mag // 2 if mag > 0 else -((-mag) // 2)
                        decay_loss += half
                        mag = mag - half
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
                       drift_total=drift_total, g_final=g, g0=g0)
    return d


def mean(v):
    return sum(v) / len(v)          # display only


def row(cells, w=11):
    return " | ".join(f"{c:>{w}}" for c in cells)


def check_identities(r):
    """Return dict of exact boolean identity checks for one run."""
    led = r["ledger"]
    return dict(
        closure=r["mass"] == sum(abs(e) for (_, _, _, e) in r["emissions"]),
        additivity=r["mass"] == sum(led["toll"]),
        pulse_flow=led["emitted_signed"] == led["net_total"]
        + led["decay_loss"] + led["inflight"],
        trajectory=led["g_final"] == led["g0"] + led["drift_total"]
        + led["net_total"],
    )


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY C1: wiring byte-identity vs exp_glm1.run_fabric ==")
    ncfg = 0
    for name, lats in (GRAMMARS[0], GRAMMARS[2], GRAMMARS[3], GRAMMARS[4]):
        for k in (1, 8):
            for s in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=s)
                b = run_ledger(lats, k, s)
                ncfg += 1
                if a != {kk: b[kk] for kk in a}:
                    ok = False
                    print(f"  MISMATCH {name} K={k} seed={s}")
    print(f"  PASS: {ncfg}/{ncfg} configs all run_fabric keys byte-identical"
          if ok else "  FAIL")
    return ok


def canary_anchors():
    ok = True
    print("\n== CANARY C2: SPIN-11/5 anchor replay ==")
    checks = (("ladder@15 K=1", GRM["ladder@15"], 1, 71.5, 5792, 106378),
              ("zero@15   K=1", GRM["zero"], 1, 77.3, 8756, 187834))
    for name, lats, k, want_tp, want_ev, want_debt in checks:
        rs = [run_ledger(lats, k, s) for s in SEEDS]
        tp = mean([within_pm(r["resid"], DELTA) for r in rs])
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        good = (abs(tp / 10 - want_tp) <= 0.2 and round(ev) == want_ev
                and round(dbt) == want_debt)
        ok &= good
        print(f"  {name}: {tp/10:.1f}% (want {want_tp}) ev {ev:.0f} "
              f"(want {want_ev}) debt {dbt:.0f} (want {want_debt}) "
              f"-> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY C3: honest closure identity (anchors, every seed) ==")
    allok = True
    for name, lats in (("ladder@15", GRM["ladder@15"]), ("zero", GRM["zero"])):
        for s in SEEDS:
            r = run_ledger(lats, 1, s)
            ids = check_identities(r)
            good = all(ids.values())
            allok &= good
            if not good:
                print(f"  FAIL {name} seed={s}: {ids}")
    print("  PASS: closure/additivity/pulse-flow/trajectory all exact, "
          "2 grammars x 5 seeds" if allok else "  FAIL")
    print("\nALL CANARIES:", "PASS" if (ok and allok) else
          "FAIL — nothing below counts")
    return ok and allok


# ------------------------------------------------------- experiments
def exp1_closure_sweep():
    print("\n== EXP 1: closure sweep — 6 grammars x K{1,2,4,8} x 5 seeds ==")
    print("   identities checked per run: closure, additivity, pulse-flow,")
    print("   trajectory (all must be exact integers)")
    print(row(["grammar", "K", "mean%", "ev", "debt", "toll/ev",
               "pulseAbs/ev", "cancels", "chat", "maxRes", "IDs"]))
    worst = None
    results = {}
    for name, lats in GRAMMARS:
        for k in (1, 2, 4, 8):
            rs = [run_ledger(lats, k, s) for s in SEEDS]
            ids = all(all(check_identities(r).values()) for r in rs)
            tp = mean([within_pm(r["resid"], DELTA) for r in rs])
            ev = mean([r["events"] for r in rs])
            dbt = mean([r["mass"] for r in rs])
            pabs = mean([r["ledger"]["emitted_abs"] for r in rs])
            mtp = tp / 10
            results[(name, k)] = (mtp, ev, dbt)
            if ids and k == 1 and (worst is None or mtp < worst[1]):
                worst = (name, mtp)
            print(row([name, k, f"{mtp:.1f}", f"{ev:.0f}", f"{dbt:.0f}",
                       f"{dbt/ev:.1f}", f"{pabs/ev:.1f}",
                       f"{mean([r['cancels'] for r in rs]):.0f}",
                       f"{mean([r['chatter'] for r in rs]):.0f}",
                       max(max(r["resid"]) for r in rs),
                       "4/4" if ids else "FAIL"]))
    print(f"\n  worst grammar at K=1 (saturation-hunt target): "
          f"{worst[0]} ({worst[1]:.1f}%)")
    return results, worst[0]


def exp2_toll_invariance(results):
    print("\n== EXP 2: toll-per-event invariance across grammars, fixed K ==")
    verdicts = {}
    for k in (1, 2, 4, 8):
        vals = [(name, results[(name, k)][2] / results[(name, k)][1])
                for name, _ in GRAMMARS]
        nums = [v for _, v in vals]
        spread = (max(nums) - min(nums)) / (sum(nums) / len(nums)) * 100
        verdicts[k] = (min(vals, key=lambda x: x[1]),
                       max(vals, key=lambda x: x[1]), spread)
        print(f"  K={k}: " + "  ".join(f"{nm} {v:.1f}" for nm, v in vals))
        print(f"        min {min(nums):.1f} ({verdicts[k][0][0]})  "
              f"max {max(nums):.1f} ({verdicts[k][1][0]})  "
              f"rel-spread {spread:.1f}%")
    return verdicts


def exp3_saturation(grammar_name):
    lats = GRM[grammar_name]
    print(f"\n== EXP 3: saturation hunt on worst grammar ({grammar_name}) ==")
    print("   arm A: drift escalation (delta fixed 12, K=1)")
    print(row(["drift", "mean%", "ev", "debt", "debt/ev", "pulseAbs/ev",
               "netAbs/ev", "decay/ev", "IDs"]))
    for drift in (6, 12, 24, 48, 96, 192, 384):
        rs = [run_ledger(lats, 1, s, drift=drift) for s in SEEDS]
        ids = all(all(check_identities(r).values()) for r in rs)
        tp = mean([within_pm(r["resid"], DELTA) for r in rs]) / 10
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        pabs = mean([r["ledger"]["emitted_abs"] for r in rs])
        nabs = mean([abs(r["ledger"]["net_total"]) for r in rs])
        dec = mean([abs(r["ledger"]["decay_loss"]) for r in rs])
        print(row([drift, f"{tp:.1f}", f"{ev:.0f}", f"{dbt:.0f}",
                   f"{dbt/ev:.1f}", f"{pabs/ev:.1f}", f"{nabs/ev:.1f}",
                   f"{dec/ev:.1f}", "4/4" if ids else "FAIL"]))

    print("\n   arm B: tick escalation (drift 6, K=1) — debt/ev stability")
    print(row(["ticks", "mean%", "ev", "debt", "debt/ev", "IDs"]))
    for ticks in (4800, 9600, 19200, 38400):
        rs = [run_ledger(lats, 1, s, ticks=ticks) for s in SEEDS]
        ids = all(all(check_identities(r).values()) for r in rs)
        tp = mean([within_pm(r["resid"], DELTA) for r in rs]) / 10
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        print(row([ticks, f"{tp:.1f}", f"{ev:.0f}", f"{dbt:.0f}",
                   f"{dbt/ev:.1f}", "4/4" if ids else "FAIL"]))

    print("\n   arm C: K-budget saturation on fine-ladder@30 (K big = long "
          "pulse life)")
    print(row(["K", "mean%", "ev", "debt", "debt/ev", "pulseAbs/ev", "IDs"]))
    for k in (1, 2, 4, 8, 16, 32):
        rs = [run_ledger(lats, k, s) for s in SEEDS]
        ids = all(all(check_identities(r).values()) for r in rs)
        tp = mean([within_pm(r["resid"], DELTA) for r in rs]) / 10
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        pabs = mean([r["ledger"]["emitted_abs"] for r in rs])
        print(row([k, f"{tp:.1f}", f"{ev:.0f}", f"{dbt:.0f}",
                   f"{dbt/ev:.1f}", f"{pabs/ev:.1f}",
                   "4/4" if ids else "FAIL"]))


GRM = dict(GRAMMARS)


def main():
    print("SPIN-12 CONSERVATION — run", os.popen("date -u").read().strip())
    if not canaries():
        sys.exit(1)
    if not canary_anchors():
        sys.exit(1)
    results, worst = exp1_closure_sweep()
    inv = exp2_toll_invariance(results)
    exp3_saturation(worst)
    print("\nDONE.")


if __name__ == "__main__":
    main()
