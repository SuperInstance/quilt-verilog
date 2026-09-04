#!/usr/bin/env python3
"""SPIN-44 — METROLOGY spoke 1: COHERENCE-MASS NORMALIZER.

SPIN-43's scar: the registered rho = sqrt(noise_energy)/live_mass_sum was
CONFOUNDED with the treatment — the live-mass denominator is inflated at
coarse grids (more mass in flight when big rounding errors delay decay),
so rho was non-monotone in step (peaked at q=7) and the shared collapse
curve failed (max LOO 40.8pp). This spin tests whether the correct
denominator is the PULSE-MASS SCALE, not the grid.

INSTRUMENT (read-only integers, identical dynamics — no rng change):
  per-PULSE rho:
      n_pulses = events                       # delivered pulses this run
      per-pulse noise std  = sqrt(noise_energy / n_pulses)
      per-pulse live mass   = live_mass_sum   / n_pulses
      rho_pp = sqrt(noise_energy/n_pulses) / (live_mass_sum/n_pulses)
             = sqrt(noise_energy * n_pulses) / live_mass_sum
  (floated ONLY at print/stat time; all loop state stays integer.)

ARMS (pre-registered BEFORE any panel run; harness = SPIN-43's
dyn_run_sto43 imported and byte-identity-canaried below):
  A) per-pulse rho on the SPIN-43 grid: grammars {zero, ladder@15,
     kcoh5@15} x K=2 x q {5,6,7,8} x M=1, 5 seeds; never anchor per
     grammar (pd=3). K=1 rows reported only (structurally vacuous,
     SPIN-30/41/42/43 scar) — not used in verdicts.
  B) noise-per-draw fixed (q=6, step 16, M=1, K=2), sweep the
     pulse-mass scale: pd in {2,3,6} x same 3 grammars, 5 seeds;
     never anchor per (grammar, pd).

H1 (pre-registered, decision rule fixed BEFORE any run):
  CLAIM: the correct denominator is the PULSE-MASS SCALE (the variance
  channel is pulse-mass-relative), not the grid.
  RULE (evaluated in this order):
    1. FALSIFIED if cost is pd-FLAT at matched step: at q=6, K=2, every
       grammar's cost max-min across pd in {2,3,6} <= 2.0pp.
    2. Else VALIDATED iff (a) cost moves with pd at matched step (at
       least one grammar's pd-spread > 2.0pp) AND (b) per-pulse rho
       COLLAPSES across grammars within eps: pooled leave-one-grammar-
       out nearest-rho_pp prediction on the ARM-A K=2 panel (12 cells,
       3 grammars x 4 q) has max |residual| <= eps = 5.0pp AND pooled
       Spearman(cost, rho_pp) >= 0.90.
    3. Else MIXED.
  Supporting (reported, non-binding): same LOO collapse computed with
  SPIN-43's grid rho on the identical pool (the confounded normalizer,
  expected to fail), and arm-B pooled LOO with rho_pp.

H2 (pre-registered): per-pulse rho is MONOTONE in step at K=2
  (repairing SPIN-43's non-monotonicity scar). Monotone = rho_pp
  non-increasing as step decreases (q 5->8), for EVERY grammar in the
  arm-A K=2 panel, with no interior extremum. VALIDATED iff all 3
  grammars monotone; FALSIFIED if any grammar has an interior extremum.

CANARIES (mandatory gate, ALL PASS before any panel read):
  a. harness import byte-identity vs spin43_topology.py:
     sp43.dyn_run_sto43 == sp42.dyn_run_sto on measurement arms
     (resid AND ledger minus the 3 new instruments) AND never-arms ==
     run_fabric resid.
  b. Anchors (run_fabric 5-seed means): zero K=1 77.3/187834/8756;
     ladder@15 K=1 71.5/106378/5792 (0.2pp pct tol, debt/ev exact).
  c. SPIN-43 replays via imported sp43.dyn_run_sto43: ladder K=2 q=5
     M=1 cost 57.4pp (tol 0.3); zero K=2 q=8 M=1 cost 0.7pp (tol 0.3).
  d. gate=never == mc=0: created == deleted == n_draws == 0 on 6 arms,
     SPIN-15 ledger assert live.
  e. Determinism: two cells run twice byte-identical (resid, events,
     ledger incl. instruments).

SPIN-15 ledger closure assert live on EVERY arm (inside dyn_run_sto43).
Integer-only inside loops; floats only at print/stat time (rho stats
computed log-space because pd=2 arms diverge with unbounded-integer
masses; divergence flagged and gated post-hoc, LABELED as such below).
Seeds
1/7/42/1999/20260902. Real runs — environment failure => INCONCLUSIVE.
One lane, no sub-lanes. python3 -u, direct redirect, no pipes. NOT
committed to git.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import exp_glm1
from exp_glm1 import run_fabric
import spin42_conservation as sp42
import spin43_topology as sp43              # byte-identity canary source
from spin30_dequant import (SEEDS, DELTA, DRIFT, PD, N, TICKS,
                            reality, pct, mean, static_fn)

dyn = sp43.dyn_run_sto43                     # THE harness (untouched)

QS = (5, 6, 7, 8)
SH = {q: 10 - q for q in QS}                 # steps 32/16/8/4
PDS = (2, 3, 6)
K2 = 2
LAD15 = [round(i * 15 / (N - 1)) for i in range(N)]
GRAMS = (("zero", [0] * N),
         ("ladder@15", LAD15),
         ("kcoh5@15", [0, 0, 0, 0, 0, 15]))
EPS = 5.0                                    # H1 band, pre-registered
FLAT = 2.0                                   # pd-flat threshold, pre-reg


import math


def rho_pp(r):
    """per-pulse rho from a run dict; floats at stat time only.
    Log-space: pd=2 arms are supra-wall divergent (N=6 > 2*pd+1),
    masses overflow float range — log handles arbitrary ints."""
    led = r["ledger"]
    np_ = r["events"]
    if not np_ or not led["live_mass_sum"] or not led["noise_energy"]:
        return 0.0
    return math.exp(0.5 * (math.log(led["noise_energy"])
                            - math.log(np_))
                    - (math.log(led["live_mass_sum"])
                       - math.log(np_)))


def rho_grid(r):
    """SPIN-43's confounded normalizer, same run (for comparison)."""
    led = r["ledger"]
    if not led["live_mass_sum"] or not led["noise_energy"]:
        return 0.0
    return math.exp(0.5 * math.log(led["noise_energy"])
                    - math.log(led["live_mass_sum"]))


def diverged(r):
    """supra-wall divergence flag (post-hoc label, stat time)."""
    return max(r["resid"]) > 10 ** 6


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: harness import byte-identity "
          "(sp43.dyn_run_sto43 == sp42.dyn_run_sto) ==")
    nchk = nmeas = 0
    for name, lats in GRAMS:
        for sd in (1, 42):
            fab = run_fabric("interference", TICKS, lats, K=1, pd=PD,
                             delta=DELTA, drift=DRIFT, seed=sd)["resid"]
            b = sp42.dyn_run_sto(static_fn(lats), k=1, seed=sd, sh=0,
                                 m_every=None)
            c = dyn(static_fn(lats), k=1, seed=sd, sh=0, m_every=None)
            nchk += 1
            if not (fab == b["resid"] == c["resid"]):
                ok = False
                print(f"  NEVER MISMATCH {name} seed={sd}")
    for name, lats in GRAMS:
        for q in (6, 8):
            for sd in (1, 42):
                b = sp42.dyn_run_sto(static_fn(lats), k=K2, seed=sd,
                                     sh=SH[q], m_every=1)
                c = dyn(static_fn(lats), k=K2, seed=sd, sh=SH[q],
                        m_every=1)
                cled = {kk: vv for kk, vv in c["ledger"].items()
                       if kk not in ("live_mass_sum", "noise_energy",
                                     "n_obs")}
                nmeas += 1
                if (b["resid"] != c["resid"] or b["events"] != c["events"]
                        or b["ledger"] != cled):
                    ok = False
                    print(f"  MEAS MISMATCH {name} q={q} sd={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} never-arms "
          f"triple-identical + {nmeas} measurement arms "
          f"(resid+events+full ledger) identical")

    print("\n== CANARY b: anchors (run_fabric 5-seed means) ==")
    for name, lats, k, wp, wd, we in (
            ("zero", [0] * N, 1, 77.3, 187834, 8756),
            ("ladder@15", LAD15, 1, 71.5, 106378, 5792)):
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

    print("\n== CANARY c: SPIN-43 replays (imported "
          "sp43.dyn_run_sto43) ==")
    for nm_i, lats, q, wcost in ((1, LAD15, 5, 57.4),
                                 (0, [0] * N, 8, 0.7)):
        fl = mean([pct(dyn(static_fn(lats), k=K2, seed=sd, sh=SH[q],
                           m_every=1)["resid"]) for sd in SEEDS])
        nv = mean([pct(dyn(static_fn(lats), k=K2, seed=sd, sh=SH[q],
                           m_every=None)["resid"]) for sd in SEEDS])
        cost = nv - fl
        good = abs(cost - wcost) <= 0.3
        ok &= good
        print(f"  {GRAMS[nm_i][0]:<10} K=2 q={q} M=1: {fl:.1f} vs never "
              f"{nv:.1f} -> cost {cost:.1f}pp (want {wcost})  -> "
              f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY d: gate=never == mc=0 ==")
    d_ok = True
    for name, lats in GRAMS:
        for pd in PDS:
            led = dyn(static_fn(lats), k=K2, seed=7, sh=4, m_every=None,
                      pd=pd)["ledger"]
            if led["created"] or led["deleted"] or led["n_draws"]:
                d_ok = False
                print(f"  TOUCHED {name} pd={pd} under never")
    print(f"  {'PASS' if d_ok else 'FAIL'}: 9 arms created=deleted=0, 0 "
          f"draws, ledger assert-live")
    ok &= d_ok

    print("\n== CANARY e: determinism (two cells, run twice) ==")
    e_ok = True
    for name, lats in (("zero", GRAMS[0][1]),
                       ("kcoh5@15", GRAMS[2][1])):
        a = dyn(static_fn(lats), k=K2, seed=7, sh=4, m_every=1, pd=6)
        b = dyn(static_fn(lats), k=K2, seed=7, sh=4, m_every=1, pd=6)
        if (a["resid"] != b["resid"] or a["events"] != b["events"]
                or a["ledger"] != b["ledger"]):
            e_ok = False
            print(f"  NONDETERMINISTIC {name}")
    print(f"  {'PASS' if e_ok else 'FAIL'}: 2 dual runs byte-identical")
    return ok and e_ok


# ------------------------------------------------------------ cells
def cell(lats, k, q, pd):
    """5-seed means, q grid cell: (pct_M1, pct_never, rpp, rgrid)."""
    m1 = [dyn(static_fn(lats), k=k, seed=sd, sh=SH[q], m_every=1, pd=pd)
          for sd in SEEDS]
    nv = [dyn(static_fn(lats), k=k, seed=sd, sh=SH[q], m_every=None,
              pd=pd) for sd in SEEDS]
    return (mean([pct(r["resid"]) for r in m1]),
            mean([pct(r["resid"]) for r in nv]),
            mean([rho_pp(r) for r in m1]),
            mean([rho_grid(r) for r in m1]))


def spearman(pairs):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for z in range(i, j + 1):
                rk[order[z]] = avg
            i = j + 1
        return rk
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    rx, ry = ranks(xs), ranks(ys)
    mx, my = mean(rx), mean(ry)
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(len(pairs)))
    den = (sum((r - mx) ** 2 for r in rx)
           * sum((r - my) ** 2 for r in ry)) ** 0.5
    return num / den if den else 0.0


def loo(pool, key):
    """LOO leave-one-grammar-out nearest-key prediction; max |resid|."""
    maxres = 0.0
    rows = []
    for item in pool:
        rho, cost, nm, tag = item
        others = [p for p in pool if p[2] != nm]
        pred = min(others, key=lambda p: abs(p[0] - rho))[1]
        resid = cost - pred
        maxres = max(maxres, abs(resid))
        rows.append((nm, tag, rho, cost, pred, resid))
    return maxres, rows


def main():
    print(f"SPIN-44 coherence-mass normalizer — pid {os.getpid()}, "
          f"{sys.version.split()[0]}")
    ok = canaries()
    print("\nCANARY GATE: " + ("ALL PASS" if ok else "FAIL — ABORT"))
    sys.stdout.flush()
    if not ok:
        sys.exit(1)

    # ---------------- ARM A: SPIN-43 grid, per-pulse rho --------------
    print("\n== ARM A: SPIN-43 grid, per-pulse rho (K=2 verdict rows; "
          "K=1 vacuous, reported) ==")
    resA = {}
    for name, lats in GRAMS:
        for k in (1, K2):
            print(f"-- {name}  K={k} --")
            print(f"{'q':>3}{'step':>5}{'never':>8}{'M=1':>8}{'cost':>8}"
                  f"{'rho_pp':>9}{'rho_grid':>9}")
            for q in QS:
                r = cell(lats, k, q, PD)
                resA[(name, k, q)] = r
                print(f"{q:>3}{1 << SH[q]:>5}{r[1]:>8.1f}{r[0]:>8.1f}"
                      f"{r[1] - r[0]:>8.1f}{r[2]:>9.4f}{r[3]:>9.4f}")
            sys.stdout.flush()

    # ---------------- ARM B: pd sweep at q=6 --------------------------
    print("\n== ARM B: noise-per-draw fixed (q=6 step 16, K=2, M=1), "
          "pulse-mass scale pd in {2,3,6} ==")
    resB = {}
    print(f"{'grammar':<10}{'pd':>3}{'never':>8}{'M=1':>8}{'cost':>8}"
          f"{'rho_pp':>9}{'rho_grid':>12}  flags")
    for name, lats in GRAMS:
        for pd in PDS:
            r = cell(lats, K2, 6, pd)
            resB[(name, pd)] = r
            m1r = [dyn(static_fn(lats), k=K2, seed=sd, sh=SH[6],
                       m_every=1, pd=pd) for sd in SEEDS]
            dv = any(diverged(x) for x in m1r)
            flag = "DIVERGED(supra-wall N>2pd+1)" if dv else ""
            print(f"{name:<10}{pd:>3}{r[1]:>8.1f}{r[0]:>8.1f}"
                  f"{r[1] - r[0]:>8.1f}{r[2]:>9.4f}{r[3]:>12.4f}  {flag}")
    sys.stdout.flush()

    # ---------------- H1 ------------------------------------------------
    print("\n== H1: pulse-mass-scale denominator ==")
    print(f"   rule: FALSIFIED if every grammar pd-flat at q=6 "
          f"(max-min <= {FLAT}pp); VALIDATED iff some grammar pd-spread "
          f"> {FLAT}pp AND arm-A LOO max|resid| <= {EPS}pp AND "
          f"Spearman(cost,rho_pp) >= 0.90; else MIXED")
    spreads = {}
    for name, _ in GRAMS:
        costs = [resB[(name, pd)][1] - resB[(name, pd)][0] for pd in PDS]
        spreads[name] = max(costs) - min(costs)
        print(f"  {name:<10} costs pd2/3/6: "
              + "/".join(f"{c:5.1f}" for c in costs)
              + f"  spread {spreads[name]:5.1f}pp")
    all_flat = all(s <= FLAT for s in spreads.values())
    any_move = any(s > FLAT for s in spreads.values())
    spreads_stable = {nm: max(resB[(nm, 3)][1] - resB[(nm, 3)][0],
                              resB[(nm, 6)][1] - resB[(nm, 6)][0])
                      - min(resB[(nm, 3)][1] - resB[(nm, 3)][0],
                            resB[(nm, 6)][1] - resB[(nm, 6)][0])
                      for nm, _ in GRAMS}
    any_move_stable = any(v > FLAT for v in spreads_stable.values())
    print("  post-hoc divergence gate (LABELED, SPIN-16 guard-prefix "
          "scar class): pd=2 is supra-wall divergent at N=6 "
          "(N > 2pd+1=5) — its cost is a saturated-pct artifact. "
          "pd-flat recheck on stable pd {3,6} only: spreads "
          + str({k: round(v, 1) for k, v in spreads_stable.items()}))
    poolA = [(resA[(nm, K2, q)][2], resA[(nm, K2, q)][1]
              - resA[(nm, K2, q)][0], nm, f"q{q}")
             for nm, _ in GRAMS for q in QS]
    maxres, rows = loo(poolA, 2)
    print(f"  arm-A LOO (rho_pp, 12 cells): max |resid| = {maxres:.1f}pp")
    for nm, tag, rho, cost, pred, resid in rows:
        print(f"    {nm:<10} {tag:<3} rho_pp={rho:.4f} cost={cost:5.1f} "
              f"LOO-pred={pred:5.1f} resid={resid:+6.1f}"
              f"{'  >EPS' if abs(resid) > EPS else ''}")
    sp_pp = spearman([(p[0], p[1]) for p in poolA])
    poolG = [(resA[(nm, K2, q)][3], resA[(nm, K2, q)][1]
              - resA[(nm, K2, q)][0], nm, f"q{q}")
             for nm, _ in GRAMS for q in QS]
    maxres_g, _ = loo(poolG, 3)
    sp_g = spearman([(p[0], p[1]) for p in poolG])
    print(f"  supporting: grid-rho LOO max|resid| = {maxres_g:.1f}pp, "
          f"Spearman = {sp_g:.3f} (SPIN-43's confounded normalizer)")
    print(f"  Spearman(cost, rho_pp) = {sp_pp:.3f} (need >= 0.90)")
    if all_flat:
        h1 = "FALSIFIED (cost pd-flat at matched step)"
    elif any_move and maxres <= EPS and sp_pp >= 0.90:
        h1 = "VALIDATED"
    else:
        h1 = "MIXED"
    print(f"-> H1 VERDICT: {h1}")

    # ---------------- H2 ------------------------------------------------
    print("\n== H2: per-pulse rho monotone in step at K=2 (arm A) ==")
    h2_ok = True
    for name, _ in GRAMS:
        rs = [resA[(name, K2, q)][2] for q in QS]     # step 32,16,8,4
        mono_dec = all(rs[i] >= rs[i + 1] for i in range(3))
        interior = ((rs[0] < rs[1] and rs[1] > rs[2])
                    or (rs[1] < rs[2] and rs[2] > rs[3]))
        print(f"  {name:<10} rho_pp by step 32/16/8/4: "
              + "/".join(f"{v:.4f}" for v in rs)
              + f"  monotone-nonincreasing={mono_dec} "
              f"interior-extremum={interior}")
        if interior or not mono_dec:
            h2_ok = False
    h2 = "VALIDATED" if h2_ok else "FALSIFIED"
    print(f"-> H2 VERDICT: {h2}")

    print("\nhead: H1 %s (pd-spreads %s, LOO %.1fpp, S %.3f), H2 %s"
          % (h1, {k: round(v, 1) for k, v in spreads.items()},
             maxres, sp_pp, h2))


if __name__ == "__main__":
    main()
