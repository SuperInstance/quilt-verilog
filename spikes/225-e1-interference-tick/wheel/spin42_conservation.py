#!/usr/bin/env python3
"""SPIN-42 — CONSERVATION spoke 5: STOCHASTIC-MASS-NEUTRAL OBSERVER at K=2.

SPIN-41's next-spoke proposal, executed. SPIN-41 falsified the floor-at-1
rescue (zero K=2 q=8 M=1 cost 48.7pp, identical to SPIN-30's amputating
rounder) while booking that the floored rounder is NOT mass-neutral: it
ADDS net mass (deleted 7,007 / created 50,267 per run). The open question:
is the K=2 decoherence channel BIAS (systematic net mass distortion of the
live wave) or OBSERVATION PER SE (any grid snap of the live wave)?

OPERATIONALIZATION (fixed BEFORE any panel run; extends spin41_dequant.py,
imported and byte-identity-canaried below):
  Measurement (stochastic variant) = at end of every M-th tick, every live
  pulse magnitude is re-rounded to the 2^sh grid with UNBIASED stochastic
  rounding (integer-only, no floats):
      a = |mag|;  base = a >> sh;  rem = a - (base << sh)   # a mod step
      draw u = rng2.below(step)    # dedicated LCG stream, seed-mixed
      r = (base + 1) << sh  if u < rem else base << sh
      mag -> sign(mag) * r
  P(round up) = rem/step exactly -> E[new] = a: UNBIASED in expectation,
  never maps a>0 to 0 (r >= base<<sh, and if base==0 the up-branch gives
  step; down-branch gives 0 ONLY when rem==0 forces base>=1 since a>=1...
  note: a<step has rem=a>0 so the u<rem branch can fire; the complement
  branch yields r=0 with prob (step-a)/step. Zeroing CAN occur but only
  with the exact probability that makes E[r]=a; it is the price of true
  unbiasedness and is ledgered like every other delta.)
  rng2 = LCG(seed ^ 0x5A17C0DE) — disjoint from the dynamics stream, so
  m_every=None arms consume no rng2 draws and stay byte-identical.
  SPIN-15 delivered-mass ledger kept verbatim from SPIN-41 on every arm:
      emitted_signed + quant_delta == decay_loss + expired + inflight
  (assert-enforced; violation aborts the spin). created/deleted per run
  are the drift diagnostic: drift = created - deleted (expect ~0 mean).

PRE-REGISTERED HYPOTHESIS + DECISION RULE (BEFORE any panel run):
  PRIMARY cell: zero grammar, K=2, q=8 (grid 4), M=1, stochastic observer.
  cost = pct(K=2 anchor = same-cell M=never) - pct(cell).
    cost <= 5.0pp   -> VALIDATED (H1): the decoherence channel is BIAS —
                       net mass distortion — not observation per se; the
                       unbiased observer collapses the SPIN-30/41 cost.
    cost > 10.0pp   -> FALSIFIED (H1), with drift-closed ledger (|created-
                       deleted| small vs SPIN-41's +43k bias): observation
                       itself — any grid snap of the live wave — is the
                       killer.
    else            -> MIXED.
  SECONDARY (descriptive): kcoh5@15 K=2 same cell; monotonicity in M/q;
  per-run drift stats; comparison row vs SPIN-41's floored rounder.

CANARIES (mandatory gate, ALL PASS before panel read):
  a. Harness byte-identity: sp41.dyn_run_mq(never) == dyn_run_sto(never)
     == run_fabric resid (6+ configs, full resid lists).
  b. Anchors (run_fabric 5-seed means): zero K=1 pct 77.3 / debt 187834 /
     ev 8756; ladder@15 K=1 pct 71.5 / debt 106378 / ev 5792 (0.2pp pct
     tol; debt/ev digit-exact).
  c. SPIN-41 floored primary replay via the IMPORTED original: zero K=2
     q=8 M=1 floored cost 48.7pp (0.3pp tol).
  d. gate=never == mc=0: m_every=None arms report created == deleted == 0
     and never-quantized ledgers close exactly (assert-live).
  e. Determinism: one floored AND one stochastic cell each run twice,
     byte-identical (resid, events, ledger).
  f. Unbiasedness instrument check: over the primary stochastic cell,
     total up-rounds vs down-rounds mass drift reported (descriptive
     closure of the E[]=a property; no assert on random realization,
     only the SPIN-15 integer-exact ledger assert is hard).

Integer-only inside every loop; floats only at print/stat time.
One lane, no sub-lanes. python3 -u, direct redirect, no pipes. Not committed.
"""
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)                       # import SPIN-41 harness
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import exp_glm1
from exp_glm1 import run_fabric, within_pm, LCG
import spin41_dequant as sp41                  # byte-identity canary source
from spin41_dequant import (SEEDS, DELTA, DRIFT, PD, N, TICKS, KS, QS,
                            SH_OF, MS, GRAMMARS, reality, pct, mean,
                            static_fn)


def dyn_run_sto(lats_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA, drift=DRIFT,
                seed=20260902, sh=0, m_every=None):
    """sp41.dyn_run_mq clone with the floor-at-1 rounding replaced by
    UNBIASED STOCHASTIC rounding (integer LCG draws, dedicated stream).
    m_every=None / sh=0 disables measurement (and consumes no rng2 draws
    -> byte-identical to run_fabric). SPIN-15 ledger kept, assert-enforced.
    Returns dict with resid, events, ledger."""
    rng = LCG(seed)
    rng2 = LCG((seed ^ 0x5A17C0DE) & 0x7FFFFFFF or 1)   # observer stream
    g = reality(0)
    g0 = g
    pulses = deque()
    resid = []
    events = 0
    step = (1 << sh) if sh > 0 else 1
    emitted_signed = net_total = decay_loss = drift_total = 0
    expired_total = created = deleted = quant_signed = 0
    n_draws = 0
    for t in range(ticks):
        lats = lats_fn(t)
        n = len(lats)
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
        for i, e in trig:
            m = abs(e) // pd or 1
            pm = m if e > 0 else -m
            pulses.appendleft([pm, k])
            events += 1
            emitted_signed += pm
        if pulses:
            net = sum(p[0] for p in pulses)
            g += net
            net_total += net
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        decay_loss += mag // 2
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
        resid.append(abs(s_true - g))
        if m_every is not None and sh > 0 and (t + 1) % m_every == 0:
            for p in pulses:
                a = abs(p[0])
                base = a >> sh
                rem = a - (base << sh)
                if rem:
                    u = rng2.below(step)          # draw only when undecided
                    n_draws += 1
                    r = ((base + 1) << sh) if u < rem else (base << sh)
                else:
                    r = base << sh
                if r != a:
                    if r > a:
                        created += r - a
                    else:
                        deleted += a - r
                    new = r if p[0] > 0 else -r
                    quant_signed += new - p[0]    # signed telescoping term
                    p[0] = new
    inflight = sum(p[0] for p in pulses)
    # --- ledger closure (integer-exact; violation aborts the spin) ---
    qd = quant_signed
    assert emitted_signed + qd == decay_loss + expired_total + inflight, \
        "MASS LEDGER OPEN"
    assert g == g0 + drift_total + net_total, "g BALANCE OPEN"
    return dict(resid=resid, events=events,
                ledger=dict(emitted_signed=emitted_signed, created=created,
                            deleted=deleted, quant_delta=qd,
                            decay_loss=decay_loss, expired_total=expired_total,
                            inflight=inflight, net_total=net_total,
                            drift_total=drift_total, g_final=g, g0=g0,
                            n_draws=n_draws))


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: byte-identity run_fabric == sp41.dyn_run_mq(never)"
          " == dyn_run_sto(never) ==")
    nchk = 0
    for name, lats in GRAMMARS + (("ladder@15",
                                    [round(i * 15 / (N - 1))
                                     for i in range(N)]),):
        for k in KS:
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=sd)["resid"]
                b = sp41.dyn_run_mq(static_fn(lats), k=k, seed=sd, sh=0,
                                    m_every=None)["resid"]
                c = dyn_run_sto(static_fn(lats), k=k, seed=sd, sh=0,
                                m_every=None)["resid"]
                nchk += 1
                if not (a == b == c):
                    ok = False
                    print(f"  MISMATCH {name} K={k} seed={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} configs triple-identical")

    print("\n== CANARY b: anchors (run_fabric 5-seed means) ==")
    lad15 = [round(i * 15 / (N - 1)) for i in range(N)]
    for name, lats, k, wp, wd, we in (
            ("zero", [0] * N, 1, 77.3, 187834, 8756),
            ("ladder@15", lad15, 1, 71.5, 106378, 5792)):
        ps, ds, es = [], [], []
        for sd in SEEDS:
            d = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                           delta=DELTA, drift=DRIFT, seed=sd)
            ps.append(pct(d["resid"]))
            ds.append(d["mass"])
            es.append(d["events"])
        p, dd, ev = mean(ps), round(mean(ds)), round(mean(es))
        good = abs(p - wp) <= 0.2 and dd == wd and ev == we
        ok &= good
        print(f"  {name:<10} K=1: pct {p:6.1f} (want {wp})  debt {dd}"
              f" (want {wd})  ev {ev} (want {we})  -> "
              f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY c: SPIN-41 floored primary replay (imported) ==")
    zl = GRAMMARS[0][1]
    fl = mean([pct(sp41.dyn_run_mq(static_fn(zl), k=2, seed=sd, sh=SH_OF[8],
                                   m_every=1)["resid"]) for sd in SEEDS])
    nv = mean([pct(sp41.dyn_run_mq(static_fn(zl), k=2, seed=sd, sh=SH_OF[8],
                                   m_every=None)["resid"]) for sd in SEEDS])
    cost = nv - fl
    good = abs(cost - 48.7) <= 0.3
    ok &= good
    print(f"  floored zero K=2 q=8: pct {fl:.1f} vs never {nv:.1f} -> "
          f"cost {cost:.1f}pp (want 48.7)  -> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY d: gate=never == mc=0 (untouched ledgers) ==")
    d_ok = True
    for name, lats in GRAMMARS:
        for k in KS:
            r = dyn_run_sto(static_fn(lats), k=k, seed=7, sh=4, m_every=None)
            led = r["ledger"]
            if led["created"] or led["deleted"] or led["n_draws"]:
                d_ok = False
                print(f"  STO TOUCHED {name} K={k} under never")
    print(f"  {'PASS' if d_ok else 'FAIL'}: 4 arms created=deleted=0, "
          f"0 draws, ledgers closed (assert-live)")
    ok &= d_ok

    print("\n== CANARY e: determinism (floored + stochastic, run twice) ==")
    e_ok = True
    a1 = sp41.dyn_run_mq(static_fn(GRAMMARS[0][1]), k=2, seed=7, sh=2,
                         m_every=1)
    a2 = sp41.dyn_run_mq(static_fn(GRAMMARS[0][1]), k=2, seed=7, sh=2,
                         m_every=1)
    if (a1["resid"] != a2["resid"] or a1["events"] != a2["events"]
            or a1["ledger"] != a2["ledger"]):
        e_ok = False
        print("  NONDETERMINISTIC floored zero")
    for (name, lats) in GRAMMARS:
        a = dyn_run_sto(static_fn(lats), k=2, seed=7, sh=2, m_every=1)
        b = dyn_run_sto(static_fn(lats), k=2, seed=7, sh=2, m_every=1)
        if (a["resid"] != b["resid"] or a["events"] != b["events"]
                or a["ledger"] != b["ledger"]):
            e_ok = False
            print(f"  NONDETERMINISTIC sto {name}")
    print(f"  {'PASS' if e_ok else 'FAIL'}: floored 1 + stochastic 2 "
          f"dual runs byte-identical")
    return ok and e_ok


# ------------------------------------------------------------ panel
_cache = {}


def cell(lats, k, sh, m, tag):
    key = (tag, k, sh, m, tuple(lats))
    if key not in _cache:
        runs = [dyn_run_sto(static_fn(lats), k=k, seed=sd, sh=sh, m_every=m)
                for sd in SEEDS]
        _cache[key] = (mean([pct(r["resid"]) for r in runs]),
                       mean([r["ledger"]["deleted"] for r in runs]),
                       mean([r["ledger"]["created"] for r in runs]))
    return _cache[key]


def run_panel():
    print("\n== PANEL (stochastic unbiased): pct / del / cre (5-seed "
          "means; del,cre = mass ledger per run) ==")
    print("   q6->step16  q8->step4  q12->step1(no-op); M=None never\n")
    res = {}
    for name, lats in GRAMMARS:
        for k in KS:
            print(f"-- {name}  K={k} --")
            print(f"{'q\\M':>6}" + "".join(f"{('M=' + str(m)):>16}"
                                           for m in MS))
            res[(name, k)] = {}
            for q in QS:
                row = [cell(lats, k, SH_OF[q], m, name) for m in MS]
                res[(name, k)][q] = dict(zip(MS, row))
                for mode in (0, 1):
                    if mode:
                        print(f"{'  cre':>6}"
                              + "".join(f"{r[2]:>16.0f}" for r in row))
                        print(f"{'  del':>6}"
                              + "".join(f"{r[1]:>16.0f}" for r in row))
                    else:
                        print(f"{'q=' + str(q):>6}"
                              + "".join(f"{r[0]:>9.1f}"
                                        f"/{r[1]:>3.0f}" for r in row))
            sys.stdout.flush()
    return res


def verdict(res):
    print("\n== DECOHERENCE COSTS, stochastic unbiased (pp vs M=never) ==")
    print(f"{'grammar':>10}{'K':>3}{'q':>4}"
          + "".join(f"{('M=' + str(m)):>9}" for m in MS))
    costs = {}
    for key, d in res.items():
        name, k = key
        for q in QS:
            row = [d[q][None][0] - d[q][m][0] for m in MS]
            costs[(name, k, q)] = row
            print(f"{name:>10}{k:>3}{q:>4}"
                  + "".join(f"{v:>9.1f}" for v in row))

    prim = costs[("zero", 2, 8)][0]
    anch = res[("zero", 2)][8][None][0]
    pcell = res[("zero", 2)][8][1][0]
    delm = res[("zero", 2)][8][1][1]
    crem = res[("zero", 2)][8][1][2]
    print(f"\nPRIMARY cell: zero K=2 q=8 M=1 stochastic: pct {pcell:.1f} "
          f"vs anchor (M=never) {anch:.1f} -> cost {prim:.1f}pp")
    print(f"  ledger: deleted {delm:.0f} / created {crem:.0f} mass/run "
          f"-> drift {crem - delm:+.0f} (SPIN-41 floored bias was "
          f"+43,260); integer-exact closure assert-live on every arm")
    print("PRE-REGISTERED rule: <=5.0 VALIDATED (channel = BIAS, net mass")
    print("  distortion); >10.0 with drift-closed ledger FALSIFIED "
          "(observation per se); else MIXED.")
    v = ("VALIDATED" if prim <= 5.0
         else "FALSIFIED" if prim > 10.0 else "MIXED")
    print(f"-> VERDICT: {v}")

    sec = costs[("kcoh5@15", 2, 8)][0]
    secd = res[("kcoh5@15", 2)][8][1][2] - res[("kcoh5@15", 2)][8][1][1]
    print(f"secondary kcoh5@15 K=2 q=8 M=1 cost = {sec:.1f}pp "
          f"(drift {secd:+.0f})")
    return v, prim, sec, anch, delm, crem


def main():
    print(f"SPIN-42 conservation stochastic-mass-neutral observer — pid "
          f"{os.getpid()}, {sys.version.split()[0]}")
    ok = canaries()
    print("\nCANARY GATE: " + ("ALL PASS" if ok else "FAIL — ABORT"))
    if not ok:
        sys.exit(1)
    res = run_panel()
    v, prim, sec, anch, delm, crem = verdict(res)
    print("\nhead: verdict %s, primary sto-cost %.1fpp (anchor %.1f), "
          "secondary %.1fpp, deleted %.0f / created %.0f mass/run"
          % (v, prim, anch, sec, delm, crem))


if __name__ == "__main__":
    main()
