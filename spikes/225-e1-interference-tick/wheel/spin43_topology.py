#!/usr/bin/env python3
"""SPIN-43 — TOPOLOGY spoke 4: VARIANCE-CHANNEL LAW across grammars.

SPIN-42's next-spoke proposal, executed. SPIN-42 validated the unbiased
stochastic observer at fine grid (zero K=2 q=8 M=1 cost 0.7pp) but left
the honest boundary: at q=6 (step 16) the SAME unbiased observer still
costs 21.0pp (zero) / 34.5pp (kcoh5@15) at M=1 — a VARIANCE channel
(rounding noise >> live mass). This spin maps cost(step) and tests
whether it is governed by the NOISE-TO-LIVE-MASS ratio, not step per se.

OPERATIONALIZATION (fixed BEFORE any panel run; extends
spin42_conservation.py, imported and byte-identity-canaried below):
  Same unbiased stochastic rounder as SPIN-42 (integer LCG draws on the
  dedicated observer stream rng2 = LCG(seed ^ 0x5A17C0DE), draw only when
  rem = a mod step != 0, P(up) = rem/step exactly). The only additions
  are READ-ONLY integer instruments inside the measurement loop (they
  consume no rng and touch no state, so dynamics stay byte-identical):
      live_mass_sum += a          # Σ |mag| over all observations
      noise_energy   += rem*(step-rem)   # Σ variance of each round
                                     # (integer, mass^2 units)
      n_obs += 1
  Instrument statistic (floated ONLY at verdict/print time):
      rho = sqrt(noise_energy) / live_mass_sum
  (characteristic per-run rounding noise relative to live mass).

GRID (pre-registered): grammars {zero, ladder@15, kcoh5@15} x K {1,2}
  x q {5,6,7,8} (steps 32/16/8/4; sh = 10-q) x M=1 only, 5 seeds
  (1/7/42/1999/20260902); M=never anchors per cell. 24 cells x 5 seeds.

H1 (pre-registered BEFORE any run): a SINGLE collapse curve
  cost ~ h(rho) shared across grammars. Decision rule:
  - Pool all K=2 cells (3 grammars x 4 q). Shared curve = pooled
    nearest-rho neighbor prediction with LEAVE-ONE-GRAMMAR-OUT honesty:
    for each cell, predicted cost = pct of the nearest-rho cell from the
    OTHER grammars (flat extrapolation at the ends).
  - epsilon = 5.0pp. VALIDATED iff every |residual| <= epsilon AND
    pooled Spearman(cost, rho) >= 0.90 (monotone shared curve);
    FALSIFIED iff any grammar's curve departs > epsilon (residual > eps)
    with drift-closed ledgers (|created-deleted| < 10% of created);
    else MIXED.
  - K=1 rows are structurally vacuous (pulses dead within birth tick,
    SPIN-30/41/42 scar) — reported, not used in the verdict.

H2 (pre-registered): coarse-grid q=6 (step 16) cost is MONOTONE in the
  step-16 noise magnitude (noise_energy) across the 3 grammars at K=2.
  VALIDATED iff cost ranks == noise_energy ranks exactly (and also
  monotone in rho); FALSIFIED if either ordering breaks.

CANARIES (mandatory gate, ALL PASS before panel read):
  a. Harness import byte-identity vs spin42_conservation.py:
     dyn_run_sto43 == sp42.dyn_run_sto on measurement arms (resid AND
     ledger dict) AND never-arms == run_fabric resid.
  b. Anchors (run_fabric 5-seed means): zero K=1 77.3 / 187834 / 8756;
     ladder@15 K=1 71.5 / 106378 / 5792 (0.2pp pct tol, debt/ev exact).
  c. SPIN-42 replays via the IMPORTED original sp42.dyn_run_sto:
     zero K=2 q=8 M=1 cost 0.7pp (tol 0.3); zero K=2 q=6 M=1 cost
     21.0pp (tol 0.3).
  d. gate=never == mc=0: created == deleted == n_draws == 0 on 6 arms,
     ledger assert live.
  e. Determinism: two cells run twice byte-identical (resid, events,
     ledger incl. instruments).

SPIN-15 ledger closure assert (emitted_signed + quant_delta ==
decay_loss + expired_total + inflight) live on EVERY arm; violation
aborts the spin. Integer-only inside every loop; floats only at
print/stat time. One lane, no sub-lanes. python3 -u, direct redirect,
no pipes. Not committed to git.
"""
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)                       # import SPIN-42 harness
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import exp_glm1
from exp_glm1 import run_fabric, LCG
import spin42_conservation as sp42             # byte-identity canary source
from spin30_dequant import (SEEDS, DELTA, DRIFT, PD, N, TICKS,
                            reality, pct, mean, static_fn)

QS43 = (5, 6, 7, 8)
SH43 = {q: 10 - q for q in QS43}               # steps 32/16/8/4
KS43 = (1, 2)
LAD15 = [round(i * 15 / (N - 1)) for i in range(N)]
GRAMS43 = (("zero", [0] * N),
           ("ladder@15", LAD15),
           ("kcoh5@15", [0, 0, 0, 0, 0, 15]))
EPS = 5.0                                      # H1 band, pre-registered


def dyn_run_sto43(lats_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA,
                  drift=DRIFT, seed=20260902, sh=0, m_every=None):
    """sp42.dyn_run_sto clone + read-only integer instruments
    (live_mass_sum, noise_energy, n_obs). No rng2 draws added/removed;
    dynamics byte-identical. SPIN-15 ledger assert-enforced."""
    rng = LCG(seed)
    rng2 = LCG((seed ^ 0x5A17C0DE) & 0x7FFFFFFF or 1)
    g = reality(0)
    g0 = g
    pulses = deque()
    resid = []
    events = 0
    step = (1 << sh) if sh > 0 else 1
    emitted_signed = net_total = decay_loss = drift_total = 0
    expired_total = created = deleted = quant_signed = 0
    n_draws = live_mass_sum = noise_energy = n_obs = 0
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
                n_obs += 1                       # instruments (read-only)
                live_mass_sum += a
                noise_energy += rem * (step - rem)
                if rem:
                    u = rng2.below(step)
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
                    quant_signed += new - p[0]
                    p[0] = new
    inflight = sum(p[0] for p in pulses)
    assert emitted_signed + quant_signed == decay_loss + expired_total \
        + inflight, "MASS LEDGER OPEN"
    assert g == g0 + drift_total + net_total, "g BALANCE OPEN"
    return dict(resid=resid, events=events,
                ledger=dict(emitted_signed=emitted_signed, created=created,
                            deleted=deleted, quant_delta=quant_signed,
                            decay_loss=decay_loss,
                            expired_total=expired_total,
                            inflight=inflight, net_total=net_total,
                            drift_total=drift_total, g_final=g, g0=g0,
                            n_draws=n_draws, live_mass_sum=live_mass_sum,
                            noise_energy=noise_energy, n_obs=n_obs))


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY a: harness import byte-identity vs "
          "spin42_conservation.py ==")
    nchk = 0
    for name, lats in GRAMS43:
        for k in KS43:
            for sd in (1, 42):
                fab = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                                 delta=DELTA, drift=DRIFT, seed=sd)["resid"]
                b = sp42.dyn_run_sto(static_fn(lats), k=k, seed=sd, sh=0,
                                     m_every=None)
                c = dyn_run_sto43(static_fn(lats), k=k, seed=sd, sh=0,
                                  m_every=None)
                nchk += 1
                if not (fab == b["resid"] == c["resid"]):
                    ok = False
                    print(f"  NEVER MISMATCH {name} K={k} seed={sd}")
    nmeas = 0
    for name, lats in GRAMS43:
        for k in KS43:
            for q in (6, 8):
                for sd in (1, 42):
                    b = sp42.dyn_run_sto(static_fn(lats), k=k, seed=sd,
                                         sh=SH43[q], m_every=1)
                    c = dyn_run_sto43(static_fn(lats), k=k, seed=sd,
                                      sh=SH43[q], m_every=1)
                    nmeas += 1
                    bled = {kk: vv for kk, vv in b["ledger"].items()}
                    cled = {kk: vv for kk, vv in c["ledger"].items()
                            if kk not in ("live_mass_sum", "noise_energy",
                                          "n_obs")}
                    if (b["resid"] != c["resid"] or b["events"] !=
                            c["events"] or bled != cled):
                        ok = False
                        print(f"  MEAS MISMATCH {name} K={k} q={q} sd={sd}")
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} never-arms triple-identical"
          f" + {nmeas} measurement arms (resid+ledger) identical")

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

    print("\n== CANARY c: SPIN-42 replays (imported sp42.dyn_run_sto) ==")
    zl = GRAMS43[0][1]
    for q, wcost in ((8, 0.7), (6, 21.0)):
        fl = mean([pct(sp42.dyn_run_sto(static_fn(zl), k=2, seed=sd,
                                        sh=SH43[q], m_every=1)["resid"])
                   for sd in SEEDS])
        nv = mean([pct(sp42.dyn_run_sto(static_fn(zl), k=2, seed=sd,
                                        sh=SH43[q], m_every=None)["resid"])
                   for sd in SEEDS])
        cost = nv - fl
        good = abs(cost - wcost) <= 0.3
        ok &= good
        print(f"  zero K=2 q={q} M=1: {fl:.1f} vs never {nv:.1f} -> cost "
              f"{cost:.1f}pp (want {wcost})  -> "
              f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY d: gate=never == mc=0 ==")
    d_ok = True
    for name, lats in GRAMS43:
        for k in KS43:
            led = dyn_run_sto43(static_fn(lats), k=k, seed=7, sh=5,
                                m_every=None)["ledger"]
            if led["created"] or led["deleted"] or led["n_draws"]:
                d_ok = False
                print(f"  TOUCHED {name} K={k} under never")
    print(f"  {'PASS' if d_ok else 'FAIL'}: 6 arms created=deleted=0, 0 "
          f"draws, ledger assert-live")
    ok &= d_ok

    print("\n== CANARY e: determinism (two cells, run twice) ==")
    e_ok = True
    for name, lats in (("zero", GRAMS43[0][1]),
                       ("kcoh5@15", GRAMS43[2][1])):
        a = dyn_run_sto43(static_fn(lats), k=2, seed=7, sh=4, m_every=1)
        b = dyn_run_sto43(static_fn(lats), k=2, seed=7, sh=4, m_every=1)
        if (a["resid"] != b["resid"] or a["events"] != b["events"]
                or a["ledger"] != b["ledger"]):
            e_ok = False
            print(f"  NONDETERMINISTIC {name}")
    print(f"  {'PASS' if e_ok else 'FAIL'}: 2 dual runs byte-identical "
          f"(resid, events, ledger incl. instruments)")
    return ok and e_ok


# ------------------------------------------------------------ panel
def cell(lats, k, q):
    """5-seed means for M=1 (sto) and M=never anchor; returns
    (pct_M1, pct_never, del, cre, rho_mean, noise_mean)."""
    m1 = [dyn_run_sto43(static_fn(lats), k=k, seed=sd, sh=SH43[q],
                        m_every=1) for sd in SEEDS]
    nv = [dyn_run_sto43(static_fn(lats), k=k, seed=sd, sh=SH43[q],
                        m_every=None) for sd in SEEDS]
    rhos = [((r["ledger"]["noise_energy"]) ** 0.5
             / r["ledger"]["live_mass_sum"]) if
            r["ledger"]["live_mass_sum"] else 0.0 for r in m1]
    return (mean([pct(r["resid"]) for r in m1]),
            mean([pct(r["resid"]) for r in nv]),
            mean([r["ledger"]["deleted"] for r in m1]),
            mean([r["ledger"]["created"] for r in m1]),
            mean(rhos),
            mean([r["ledger"]["noise_energy"] for r in m1]))


def spearman(pairs):
    """rank correlation, floats at stat time only."""
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


def main():
    print(f"SPIN-43 topology variance-channel law — pid {os.getpid()}, "
          f"{sys.version.split()[0]}")
    ok = canaries()
    print("\nCANARY GATE: " + ("ALL PASS" if ok else "FAIL — ABORT"))
    sys.stdout.flush()
    if not ok:
        sys.exit(1)

    print("\n== PANEL: unbiased stochastic observer, M=1, 5-seed means ==")
    print("   cost = pct(never anchor) - pct(M=1); rho = "
          "sqrt(noise_energy)/live_mass; noise = noise_energy per run\n")
    res = {}
    for name, lats in GRAMS43:
        for k in KS43:
            print(f"-- {name}  K={k} --")
            print(f"{'q':>3}{'step':>5}{'never':>8}{'M=1':>8}{'cost':>8}"
                  f"{'rho':>9}{'noise':>12}{'del':>8}{'cre':>8}{'drift':>9}")
            for q in QS43:
                r = cell(lats, k, q)
                res[(name, k, q)] = r
                print(f"{q:>3}{1 << SH43[q]:>5}{r[1]:>8.1f}{r[0]:>8.1f}"
                      f"{r[1] - r[0]:>8.1f}{r[4]:>9.4f}{r[5]:>12.0f}"
                      f"{r[2]:>8.0f}{r[3]:>8.0f}{r[3] - r[2]:>9.0f}")
            sys.stdout.flush()

    # ---------------- H1: shared collapse curve ----------------
    print("\n== H1: single collapse curve cost ~ h(rho), shared across "
          "grammars ==")
    print("   leave-one-grammar-out nearest-rho prediction; eps = "
          f"{EPS}pp; pooled Spearman(cost,rho) >= 0.90 required")
    cells = sorted(((nm, q, res[(nm, 2, q)]) for nm, _ in GRAMS43
                     for q in QS43), key=lambda c: c[2][4])
    pool = [(r[4], r[1] - r[0], nm, q) for nm, q, r in cells]
    maxres = 0.0
    for rho, cost, nm, q in pool:
        others = [p for p in pool if p[2] != nm]
        if not others:
            continue
        pred = min(others, key=lambda p: abs(p[0] - rho))[1]
        resid = cost - pred
        maxres = max(maxres, abs(resid))
        print(f"  {nm:<10} q={q} rho={rho:.4f} cost={cost:5.1f} "
              f"LOO-pred={pred:5.1f} resid={resid:+6.1f}"
              f"{'  >EPS' if abs(resid) > EPS else ''}")
    rho_ = spearman([(p[0], p[1]) for p in pool])
    drift_ok = all(abs(r[3] - r[2]) < 0.10 * max(r[3], 1)
                   for _, _, r in cells)
    print(f"  pooled Spearman(cost, rho) = {rho_:.3f} (need >= 0.90); "
          f"max |LOO residual| = {maxres:.1f}pp (need <= {EPS}); "
          f"drift-closed (<10% of created): {drift_ok}")
    if maxres <= EPS and rho_ >= 0.90:
        h1 = "VALIDATED"
    elif maxres > EPS and drift_ok:
        h1 = "FALSIFIED"
    else:
        h1 = "MIXED"
    print(f"-> H1 VERDICT: {h1}")

    # ---------------- H2: q=6 monotone in noise magnitude -------------
    print("\n== H2: q=6 (step 16) cost monotone in noise magnitude, "
          "K=2 ==")
    q6 = [(nm, res[(nm, 2, 6)]) for nm, _ in GRAMS43]
    q6s = sorted(q6, key=lambda kv: kv[1][5])          # by noise_energy
    costs_by_noise = [kv[1][1] - kv[1][0] for kv in q6s]
    q6r = sorted(q6, key=lambda kv: kv[1][4])          # by rho
    costs_by_rho = [kv[1][1] - kv[1][0] for kv in q6r]
    for nm, r in q6:
        print(f"  {nm:<10} cost {r[1]-r[0]:5.1f}pp  noise {r[5]:.3e}  "
              f"rho {r[4]:.4f}")
    mono_noise = all(costs_by_noise[i] <= costs_by_noise[i + 1]
                     for i in range(len(costs_by_noise) - 1))
    mono_rho = all(costs_by_rho[i] <= costs_by_rho[i + 1]
                   for i in range(len(costs_by_rho) - 1))
    print(f"  monotone in noise_energy: {mono_noise}; monotone in rho: "
          f"{mono_rho}")
    h2 = "VALIDATED" if (mono_noise and mono_rho) else "FALSIFIED"
    print(f"-> H2 VERDICT: {h2}")

    print("\nhead: H1 %s (maxLOO %.1fpp, rho %.3f), H2 %s"
          % (h1, maxres, rho_, h2))


if __name__ == "__main__":
    main()
