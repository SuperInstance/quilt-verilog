#!/usr/bin/env python3
"""SPIN-41 — DEQUANT spoke 8: MASS-PRESERVING ZENO at K=2 (§10 probes).

SPIN-30's next-spoke proposal, executed. SPIN-30 booked a 48.7pp K=2
zero-lock cost (zero grammar, K=2, q=8, M=1: 50.0 -> 1.3) under round-to-
nearest quantization and could NOT split deleted-mass (grid rounding zeroes
mags <= half-grid: mass deletion / amputation) from true decoherence. This
spin re-runs SPIN-30's Zeno grid with per-measurement rounding FLOORED AT
±1 (no magnitude is ever quantized to zero) plus the SPIN-15 delivered-mass
ledger on every arm, and closes the ledger integer-exact.

OPERATIONALIZATION (fixed BEFORE any panel run; extends spin30_dequant.py,
imported and byte-identity-canaried below):
  Measurement (floor variant) = at end of every M-th tick, every live pulse
  magnitude is re-rounded to the 2^sh grid but floored at 1:
      a = |mag|;  r = ((a + half) >> sh) << sh;  if r < 1: r = 1
      mag -> sign(mag) * r
  Small mags (1..half-grid) that round-to-nearest would ZERO are left at
  their current value (>=1) -> no deletion-to-zero channel. Large mags can
  still move down (rounding) or up (rounding) -> those deltas are LEDGERED.
  Same grid/q/M panel as SPIN-30: q {6,8,12} -> sh {4,2,0}, M {1,4,16,64,
  never}; q=12 with floor is still a structural no-op (r == a always).

DELIVERED-MASS LEDGER (SPIN-15 identity, every arm, integer-exact):
  emitted_signed + quant_delta == decay_loss + expired_total + inflight
  where quant_delta = created - deleted (created/deleted = abs rounding
  up/down mass at measurement), decay_loss = Σ mag//2 removals (verbatim
  run_fabric decay), expired_total/inflight = signed resting mass. The
  telescoping identity holds per-pulse; violation => AssertionError abort.
  Also exact: g_final == g0 + drift_total + net_total.
  deleted-mass is thus a measured, booked quantity per cell.

PRE-REGISTERED PREDICTION + DECISION RULE (BEFORE any panel run):
  PRIMARY cell: zero grammar, K=2, q=8 (grid 4), M=1, floored rounding.
  cost = pct(K=2 anchor = same-cell M=never) - pct(cell).
    cost <= 5.0pp  -> VALIDATED: the SPIN-30 K=2 zero-lock fragility is
                      quantization MASS-LOSS, not cross-tick coherence;
                      floor-at-1 collapses it.
    cost > 10.0pp  (with closed mass ledger) -> FALSIFIED: true
                      decoherence channel survives mass preservation.
    else           -> MIXED.
  SECONDARY (descriptive): full grid trend; kcoh5@15 K=2 same cell;
  monotonicity in M and q; deleted-vs-created mass per cell (expect
  deleted << SPIN-30's implied amputation).

CANARIES (mandatory gate, ALL PASS before panel read):
  a. Harness byte-identity: spin30_dequant.dyn_run_q(never, sh=0) == my
     dyn_run_mq(never, floor) resid AND == run_fabric resid (6 configs).
  b. Anchors (run_fabric 5-seed means): zero K=1 pct 77.3 / debt 187834 /
     ev 8756; ladder@15 K=1 pct 71.5 / ev 5792 / debt 106378 (0.2pp pct
     tol; debt/ev digit-exact; spin-10 publishing format).
  c. SPIN-30 M=1 K=2 replay via the IMPORTED original: zero K=2 q=8
     M=1 -> 1.3, M=never -> 50.0, cost 48.7pp (0.15pp tol).
  d. gate=never == mc=0: m_every=None arms report created == deleted == 0
     and never-quantized ledgers close exactly.
  e. Determinism: two floored cells run twice, byte-identical (resid,
     events, ledger).

Integer-only inside every loop; floats only at print/stat time.
One lane, no sub-lanes. python3 -u, direct redirect, no pipes. Not committed.
"""
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)                       # import SPIN-30 harness
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import exp_glm1
from exp_glm1 import run_fabric, within_pm, LCG
import spin30_dequant as sp30                  # byte-identity canary source
from spin30_dequant import (SEEDS, DELTA, DRIFT, PD, N, TICKS, KS, QS,
                            SH_OF, MS, GRAMMARS, reality, pct, mean,
                            static_fn)


def dyn_run_mq(lats_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA, drift=DRIFT,
               seed=20260902, sh=0, m_every=None):
    """spin30 dyn_run_q clone with (i) floor-at-1 rounding, (ii) SPIN-15
    delivered-mass ledger. m_every=None / sh=0 disables measurement.
    Returns dict with resid, events, ledger."""
    rng = LCG(seed)
    g = reality(0)
    g0 = g
    pulses = deque()
    resid = []
    events = 0
    half = (1 << (sh - 1)) if sh > 0 else 0
    emitted_signed = net_total = decay_loss = drift_total = 0
    expired_total = created = deleted = quant_signed = 0
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
                r = ((a + half) >> sh) << sh
                if r < 1:
                    r = 1
                if r != a:
                    if r > a:
                        created += r - a
                    else:
                        deleted += a - r
                    new = r if p[0] > 0 else -r
                    quant_signed += new - p[0]   # signed telescoping term
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
                            drift_total=drift_total, g_final=g, g0=g0))


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: byte-identity sp30.dyn_run_q(never) == dyn_run_mq"
          "(never) == run_fabric ==")
    nchk = 0
    for name, lats in GRAMMARS + (("ladder@15",
                                    [round(i * 15 / (N - 1))
                                     for i in range(N)]),):
        for k in KS:
            for sd in (1, 42):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=sd)["resid"]
                b, _ = sp30.dyn_run_q(static_fn(lats), k=k, seed=sd, sh=0,
                                      m_every=None)
                c = dyn_run_mq(static_fn(lats), k=k, seed=sd, sh=0,
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

    print("\n== CANARY c: SPIN-30 M=1 K=2 replay via imported original ==")
    zl = GRAMMARS[0][1]
    c_ok = True
    for q, m, want in ((8, 1, 1.3), (8, None, 50.0)):
        got = mean([pct(sp30.dyn_run_q(static_fn(zl), k=2, seed=sd,
                                       sh=SH_OF[q], m_every=m)[0])
                    for sd in SEEDS])
        if abs(got - want) > 0.15:
            c_ok = False
            print(f"  MISMATCH q={q} M={m}: {got:.1f} != {want}")
        else:
            print(f"  q={q} M={m}: {got:.1f} == {want}")
    replay_cost = (mean([pct(sp30.dyn_run_q(static_fn(zl), k=2, seed=sd,
                                             sh=SH_OF[8], m_every=None)[0])
                         for sd in SEEDS])
                   - mean([pct(sp30.dyn_run_q(static_fn(zl), k=2, seed=sd,
                                              sh=SH_OF[8], m_every=1)[0])
                           for sd in SEEDS]))
    print(f"  SPIN-30 zero K=2 q=8 cost replay: {replay_cost:.1f}pp "
          f"(want 48.7)")
    if abs(replay_cost - 48.7) > 0.3:
        c_ok = False
    ok &= c_ok
    print(f"  {'PASS' if c_ok else 'FAIL'}")

    print("\n== CANARY d: gate=never == mc=0 (untouched ledgers) ==")
    d_ok = True
    for name, lats in GRAMMARS:
        for k in KS:
            r = dyn_run_mq(static_fn(lats), k=k, seed=7, sh=4, m_every=None)
            led = r["ledger"]
            if led["created"] or led["deleted"]:
                d_ok = False
                print(f"  QUANT TOUCHED {name} K={k} under never")
    print(f"  {'PASS' if d_ok else 'FAIL'}: 4 arms created=deleted=0, "
          f"ledgers closed (assert-live)")
    ok &= d_ok

    print("\n== CANARY e: determinism (floored cells, run twice) ==")
    e_ok = True
    for (name, lats) in GRAMMARS:
        a = dyn_run_mq(static_fn(lats), k=2, seed=7, sh=2, m_every=1)
        b = dyn_run_mq(static_fn(lats), k=2, seed=7, sh=2, m_every=1)
        if (a["resid"] != b["resid"] or a["events"] != b["events"]
                or a["ledger"] != b["ledger"]):
            e_ok = False
            print(f"  NONDETERMINISTIC {name}")
    print(f"  {'PASS' if e_ok else 'FAIL'}: 2 dual runs byte-identical")
    return ok and e_ok


# ------------------------------------------------------------ panel
_cache = {}


def cell(lats, k, sh, m, tag):
    key = (tag, k, sh, m, tuple(lats))
    if key not in _cache:
        runs = [dyn_run_mq(static_fn(lats), k=k, seed=sd, sh=sh, m_every=m)
                for sd in SEEDS]
        _cache[key] = (mean([pct(r["resid"]) for r in runs]),
                       mean([r["ledger"]["deleted"] for r in runs]),
                       mean([r["ledger"]["created"] for r in runs]))
    return _cache[key]


def run_panel():
    print("\n== PANEL (floor-at-1): pct / del / cre (5-seed means; "
          "del,cre = mass ledger per run) ==")
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
                        print(f"{'  del':>6}"
                              + "".join(f"{r[1]:>16.0f}" for r in row))
                    else:
                        print(f"{'q=' + str(q):>6}"
                              + "".join(f"{r[0]:>9.1f}"
                                        f"/{r[1]:>3.0f}" for r in row))
            sys.stdout.flush()
    return res


def verdict(res):
    print("\n== DECOHERENCE COSTS, floor-at-1 (pp vs M=never) ==")
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
    delm = res[("zero", 2)][8][1][1]
    crem = res[("zero", 2)][8][1][2]
    print(f"\nPRIMARY cell: zero K=2 q=8 M=1 floor-at-1: "
          f"pct {res[('zero', 2)][8][1][0]:.1f} vs anchor "
          f"(M=never) {anch:.1f} -> cost {prim:.1f}pp")
    print(f"  ledger: deleted {delm:.0f} / created {crem:.0f} mass/run "
          f"(closed integer-exact on every arm)")
    print("PRE-REGISTERED rule: <=5.0 VALIDATED (fragility = quantization")
    print("  mass-loss); >10.0 with closed ledger FALSIFIED (true "
          "decoherence); else MIXED.")
    v = ("VALIDATED" if prim <= 5.0
         else "FALSIFIED" if prim > 10.0 else "MIXED")
    print(f"-> VERDICT: {v}")

    sec = costs[("kcoh5@15", 2, 8)][0]
    print(f"secondary kcoh5@15 K=2 q=8 M=1 cost = {sec:.1f}pp")
    return v, prim, sec, anch, delm, crem


def main():
    print(f"SPIN-41 dequant mass-preserving Zeno — pid {os.getpid()}, "
          f"{sys.version.split()[0]}")
    ok = canaries()
    print("\nCANARY GATE: " + ("ALL PASS" if ok else "FAIL — ABORT"))
    if not ok:
        sys.exit(1)
    res = run_panel()
    v, prim, sec, anch, delm, crem = verdict(res)
    print("\nhead: verdict %s, primary floor-cost %.1fpp (anchor %.1f), "
          "secondary %.1fpp, deleted %.0f / created %.0f mass/run"
          % (v, prim, anch, sec, delm, crem))


if __name__ == "__main__":
    main()
