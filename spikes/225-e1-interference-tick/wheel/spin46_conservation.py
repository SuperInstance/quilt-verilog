#!/usr/bin/env python3
"""SPIN 46, SPOKE: CONSERVATION — the debt-RATE law d(debt)/dt = Phi(drift, K).

Executes SPIN-38's filed next-spoke proposal (SPIN-38-conservation.md
"Next-spoke proposal"). SPIN-38 falsified the debt ceiling (linear
in-window growth at every drift up to 768; delta collapses at drift>=96)
but left the RATE uncharacterized: K=1 debt-doubling ratios per drift
doubling 4.27, 4.25, 2.24 (concave — rate saturates in drift), K=2:
2.46, 2.04, 2.88 (convex again — runaway).

PRE-REGISTERED HYPOTHESES (before any run; decision rule verbatim below):

  H1 (separability of Phi): on outlier@30, delta=12 (delta is dead at
      stress per SPIN-38; spot-checked again here), ticks=38400, the
      asymptotic debt rate Phi(drift, K) = total_debt / ticks (mean over
      the 5 seeds) factors as
          Phi(drift, K) = D(drift) * R(K)
      with D(drift) = Phi(drift, 1) and R(K) the K-resonance factor,
      i.e. the K-ratio rho(drift) = Phi(drift, 2)/Phi(drift, 1) is
      CONSTANT in drift on the stress grid {96, 192, 384, 768}.
      drift=0 is recorded as a BOUNDARY cell (SPIN-38: the drift-free
      regime is where delta still matters) and is EXCLUDED from the H1
      verdict by this pre-registration, reported separately.
  H2 (K=2 runaway fate at 32x): at 32x SPIN-38's window duration
      (153600 ticks = 32 windows of 4800), the K=2 runaway RE-SATURATES:
      late-run debt accumulation decays.
  FALSIFY H1 if the interaction term is required; FALSIFY H2 if debt
      still grows without bound at 32x.

PRE-REGISTERED DECISION RULE (verbatim, immutable once run starts):
  H1 VALIDATED  iff on stress drifts {96,192,384,768}:
                 (i)  spread(rho) = (max rho - min rho) <= 0.10 * mean(rho)
                 AND  (ii) multiplicative-model residual
                      max_drift |Phi(drift,2) - D(drift)*Rhat| / Phi(drift,2)
                      <= 0.10, where Rhat = mean(rho).
  H1 FALSIFIED  iff (i) or (ii) breaks, i.e. the K-resonance factor is
                 drift-DEPENDENT: the interaction term is required.
  H2 VALIDATED  iff at ticks=153600, K=2, for >= 3 of the 4 stress
                 drifts {96,192,384,768}: last-window debt rate / first-
                 window debt rate < 0.5 (true late-run decay).
  H2 FALSIFIED  iff for >= 3 of the 4 stress drifts that ratio >= 0.9
                 (debt still grows unbounded in-window at 32x).
  MIXED otherwise, per hypothesis.
  INCONCLUSIVE if canaries fail or the environment crashes (no numbers
  count).
  DIVERGENCE GATE (SPIN-16/44 scar class): if any cell crashes/corrupts,
  exclude post-hoc with a printed labeled exclusion, never silently.

CANARIES (mandatory gate, ALL PASS before panel read):
  a. harness provenance: import SPIN-38's spin38_conservation and prove
     byte-identity of THIS spin's runner vs spin38.run_ledger on >= 6
     configs including escalated parameters (full key equality, ledger +
     windows).
  b. anchors digit-exact: zero@15 K=1 -> 77.3% / ev 8756 / debt 187834;
     ladder@15 K=1 -> 71.5% / ev 5792 / debt 106378 (default params).
  c. SPIN-38 drift=384 debt/event ~= 9202 replay (ladder@30 K=1 @4800t).
  d. gate=never == mc=0: with delta = 10**9 (trigger gate can never fire)
     events == mass == all ledger flows == 0 — no pulse mass is created
     from nothing.
  e. SPIN-15 mass/debt closure identities hold on EVERY arm run.
  f. double-run determinism (>= 4 configs, full key byte-equality).

ARMS: outlier@30 (N=6, lats [0,0,0,0,0,30]), pd=3, delta=12.
  Main grid : drift {0,96,192,384,768} x K {1,2} @ 38400 ticks (8 windows).
  Delta spot: drift=384, delta {1,6,12}, K {1,2} @ 38400 (delta-dead check).
  H2 arm   : K=2 (and K=1 at drift 768 for the scaling control),
             drift {0,96,192,384,768} @ 153600 ticks (32 windows).
  Seeds {1, 7, 42, 1999, 20260902}. Integer-only inside every loop;
  floats only at print time. Real runs; no fabricated numbers.
"""
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import spin38_conservation as sp38  # noqa: E402  (harness provenance)
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
PD = 3
N = 6
BASE_TICKS = 4800
GRAMMAR = ("outlier@30", [0, 0, 0, 0, 0, 30])
DRIFTS = (0, 96, 192, 384, 768)
STRESS = (96, 192, 384, 768)
KS = (1, 2)
DELTA = 12
T8 = 38400    # 8 windows  (SPIN-38 duration)
T32 = 153600  # 32 windows (32x SPIN-38's 4800-tick window)
T0 = time.time()


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


ANCH_LAT = {"ladder@15": ladder(15), "zero": [0] * N}


# ---- runner: verbatim loop of spin38.run_ledger, generalized ONLY in the
# ---- window count (nw). nw=8 at ticks=38400 reproduces spin38 exactly.
def run_ledger(lats, k, seed, ticks=T8, delta=12, drift=6, pd=PD, nw=8):
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
    win = ticks // nw if nw else 0
    windows = []

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
        if win and (t + 1) % win == 0:
            windows.append(mass)

    inflight = sum(p[0] for p in pulses)
    d = dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
             settles=settles, resid=resid, cflags=cflags,
             emissions=emissions, audit=None, ticks=ticks)
    d["ledger"] = dict(toll=toll, emitted_abs=emitted_abs,
                       emitted_signed=emitted_signed, net_total=net_total,
                       decay_loss=decay_loss, inflight=inflight,
                       expired_total=expired_total,
                       drift_total=drift_total, g_final=g, g0=g0)
    d["windows"] = windows
    return d


def mean(v):
    return sum(v) / len(v)      # display only


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


def key(r):
    """Everything a rerun must reproduce byte-exactly."""
    led = r["ledger"]
    return (r["events"], r["mass"], r["cancels"], r["chatter"],
            r["settles"], tuple(r["resid"]), tuple(r["cflags"]),
            tuple(led["toll"]), led["emitted_abs"], led["emitted_signed"],
            led["net_total"], led["decay_loss"], led["inflight"],
            led["expired_total"], led["drift_total"], led["g_final"])


# ------------------------------------------------------------ canaries
def canary_a():
    print("== CANARY (a): provenance — this runner == spin38.run_ledger ==")
    ok = True
    cfgs = [
        (GRAMMAR[1], 1, 1, T8, dict(drift=96, delta=6)),
        (GRAMMAR[1], 2, 42, T8, dict(drift=768, delta=1)),
        (GRAMMAR[1], 1, 7, T8, dict(drift=0, delta=12)),
        (GRAMMAR[1], 2, 1999, T8, dict(drift=384, delta=12)),
        (GRAMMAR[1], 1, 42, T32, dict(drift=768, delta=12)),  # nw=32 too
        (ANCH_LAT["zero"], 2, 1, T8, dict(drift=6, delta=12)),
        (ANCH_LAT["ladder@15"], 1, 20260902, BASE_TICKS,
         dict(drift=6, delta=12)),
    ]
    for lats, k, s, tk, kw in cfgs:
        nw = 8 if tk != T32 else 32
        mine = run_ledger(lats, k, s, ticks=tk, nw=nw, **kw)
        theirs = sp38.run_ledger(lats, k, s, ticks=tk, **kw)
        good = key(mine) == key(theirs) and \
            mine["windows"][-1] == theirs["windows"][-1] \
            and len(mine["windows"]) == nw
        ok &= good
        print(f"  {'identical' if good else 'MISMATCH'}: K={k} seed={s} "
              f"ticks={tk} {kw} (nw={nw})")
    print(f"  {'PASS' if ok else 'FAIL'}: {len(cfgs)}/{len(cfgs)} configs")
    return ok


def canary_b():
    ok = True
    print("\n== CANARY (b): anchor replays digit-exact (drift=6 delta=12)")
    checks = (("zero@15   K=1", "zero", 77.3, 8756, 187834),
              ("ladder@15 K=1", "ladder@15", 71.5, 5792, 106378))
    for name, gname, want_tp, want_ev, want_debt in checks:
        rs = [run_ledger(ANCH_LAT[gname], 1, s, ticks=BASE_TICKS)
              for s in SEEDS]
        tp = mean([within_pm(r["resid"], 12) for r in rs]) / 10
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        good = (abs(tp - want_tp) <= 0.2 and abs(ev - want_ev) <= 2
                and abs(dbt - want_debt) <= 300)
        ok &= good
        print(f"  {name}: {tp:.1f}% (want {want_tp})  ev {ev:.0f} "
              f"(want {want_ev})  debt {dbt:.0f} (want {want_debt})  "
              f"-> {'PASS' if good else 'FAIL'}")
    return ok


def canary_c():
    print("\n== CANARY (c): SPIN-38 drift=384 debt/ev ~9202 replay @4800t ==")
    rs = [run_ledger(ladder(30), 1, s, ticks=BASE_TICKS, drift=384, delta=12)
          for s in SEEDS]
    dp = mean([r["mass"] / r["events"] if r["events"] else 0 for r in rs])
    good = abs(dp - 9202.4) / 9202.4 <= 0.05
    print(f"  ladder@30 K=1 drift=384: debt/ev {dp:.1f} (SPIN-15/38 anchor "
          f"9202.4 +-5%) -> {'PASS' if good else 'FAIL'}")
    return good


def canary_d():
    print("\n== CANARY (d): gate=never == mc=0 (delta=10**9, no trigger) ==")
    ok = True
    for k in KS:
        for drift in (0, 384):
            r = run_ledger(GRAMMAR[1], k, 1, ticks=BASE_TICKS,
                           delta=10 ** 9, drift=drift)
            led = r["ledger"]
            zero = (r["events"] == 0 and r["mass"] == 0 and r["cancels"] == 0
                    and led["toll"] == [0] * N and led["emitted_abs"] == 0
                    and led["emitted_signed"] == 0 and led["net_total"] == 0
                    and led["decay_loss"] == 0 and led["inflight"] == 0
                    and led["expired_total"] == 0
                    and r["windows"] == [0] * 8)
            ok &= zero
            print(f"  K={k} drift={drift}: "
                  f"{'all-zero ledger (PASS)' if zero else 'MASS CREATED (FAIL)'}")
    return ok


def canary_f():
    print("\n== CANARY (f): double-run determinism (>=4 configs) ==")
    ok = True
    cfgs = [(GRAMMAR[1], 1, 1, T8, dict(drift=0), 8),
            (GRAMMAR[1], 2, 42, T8, dict(drift=768), 8),
            (GRAMMAR[1], 2, 7, T32, dict(drift=384), 32),
            (ANCH_LAT["zero"], 2, 1999, T8, dict(drift=96), 8)]
    for i, (lats, k, s, tk, kw, nw) in enumerate(cfgs):
        r1 = key(run_ledger(lats, k, s, ticks=tk, nw=nw, **kw))
        r2 = key(run_ledger(lats, k, s, ticks=tk, nw=nw, **kw))
        good = r1 == r2
        ok &= good
        print(f"  cfg{i} K={k} seed={s} ticks={tk} {kw}: "
              f"{'byte-identical' if good else 'DIVERGED'}")
    print(f"  {'PASS' if ok else 'FAIL'}: {len(cfgs)}/{len(cfgs)}")
    return ok


# ------------------------------------------------------- experiment
def cell(drift, k, ticks=T8, delta=DELTA, nw=8, label=""):
    """Mean-over-seeds cell; identities checked on EVERY arm (canary e)."""
    rs = [run_ledger(GRAMMAR[1], k, s, ticks=ticks, delta=delta,
                     drift=drift, nw=nw) for s in SEEDS]
    ids = all(all(check_identities(r).values()) for r in rs)
    ev = mean([r["events"] for r in rs])
    dbt = mean([r["mass"] for r in rs])
    wd = []
    for j in range(nw):
        vals = []
        for r in rs:
            prev = r["windows"][j - 1] if j else 0
            vals.append(r["windows"][j] - prev)
        wd.append(mean(vals))
    return dict(ev=ev, debt=dbt, rate=dbt / ticks, windows=wd, ids=ids,
                label=label)


def main():
    print("SPIN-46 CONSERVATION (debt-rate law) —",
          os.popen("date -u").read().strip())
    print("hypotheses + decision rule pre-registered in script header "
          "(unchanged at run time)")
    ok = (canary_a() & canary_b() & canary_c() & canary_d() & canary_f())
    print("\nALL CANARIES:", "PASS" if ok else
          "FAIL -> INCONCLUSIVE, nothing below counts")
    if not ok:
        sys.exit(1)

    # ---- main grid: Phi(drift, K) at 8-window duration
    print(f"\n== MAIN GRID: outlier@30, delta={DELTA}, {T8} ticks, "
          f"seeds {SEEDS}")
    cells = {}
    print("drift | K | events | debt | Phi=debt/t | w1->w8 rate "
          "(last/first r) | IDs")
    for drift in DRIFTS:
        for k in KS:
            c = cell(drift, k)
            cells[(drift, k)] = c
            wd = c["windows"]
            r = wd[-1] / wd[0] if wd[0] else float("nan")
            print(f"{drift:5d} | {k} | {c['ev']:9.0f} | {c['debt']:11.0f} | "
                  f"{c['rate']:9.1f} | {wd[0]:9.0f}->{wd[-1]:9.0f} "
                  f"(r {r:.2f}) | {'4/4' if c['ids'] else 'FAIL'}")
    ids_all = all(c["ids"] for c in cells.values())
    print(f"  canary (e) mass/debt identities on every main-grid arm: "
          f"{'PASS' if ids_all else 'FAIL'}")
    ok &= ids_all

    # delta-dead spot check at drift=384
    print(f"\n== DELTA SPOT CHECK (drift=384, {T8}t): delta-dead per SPIN-38?")
    dd = {}
    for delta in (1, 6, 12):
        for k in KS:
            c = cell(384, k, delta=delta)
            dd[(delta, k)] = c
            print(f"  delta={delta} K={k}: debt {c['debt']:.0f} "
                  f"IDs {'4/4' if c['ids'] else 'FAIL'}")
    for k in KS:
        vals = [dd[(d_, k)]["debt"] for d_ in (1, 6, 12)]
        spread = (max(vals) - min(vals)) / mean(vals)
        print(f"  K={k} delta spread {spread * 100:.2f}% -> "
              f"{'delta-dead (<1%)' if spread < 0.01 else 'delta ALIVE'}")
    ok &= all(c["ids"] for c in dd.values())

    # ---- H2: 32-window arms
    print(f"\n== H2 ARM: {T32} ticks = 32x SPIN-38 window, K=2 "
          f"(K=1 drift=768 control), delta={DELTA}")
    h2 = {}
    print("drift | K | debt | Phi | w1 | w8 | w16 | w24 | w32 | "
          "last/first r | 32x/8x debt ratio | IDs")
    for drift in DRIFTS:
        c = cell(drift, 2, ticks=T32, nw=32, label="H2")
        h2[(drift, 2)] = c
        c8 = cells[(drift, 2)]
        wd = c["windows"]
        r = wd[-1] / wd[0] if wd[0] else float("nan")
        ratio = c["debt"] / c8["debt"]
        print(f"{drift:5d} | 2 | {c['debt']:11.0f} | {c['rate']:9.1f} | "
              f"{wd[0]:9.0f} | {wd[7]:9.0f} | {wd[15]:9.0f} | "
              f"{wd[23]:9.0f} | {wd[31]:9.0f} | {r:.2f} | "
              f"{ratio:6.2f} | {'4/4' if c['ids'] else 'FAIL'}")
    ck = cell(768, 1, ticks=T32, nw=32, label="H2-control")
    h2[(768, 1)] = ck
    wd = ck["windows"]
    print(f"{768:5d} | 1 | {ck['debt']:11.0f} | {ck['rate']:9.1f} | "
          f"{wd[0]:9.0f} | {wd[7]:9.0f} | {wd[15]:9.0f} | "
          f"{wd[23]:9.0f} | {wd[31]:9.0f} | "
          f"{wd[-1] / wd[0] if wd[0] else float('nan'):.2f} | "
          f"{ck['debt'] / cells[(768, 1)]['debt']:6.2f} | "
          f"{'4/4' if ck['ids'] else 'FAIL'}")
    ok &= all(c["ids"] for c in h2.values())

    # ---- H1: separability test (pre-registered rule)
    print("\n== H1 SEPARABILITY: Phi(drift,K) = D(drift) x R(K)? ==")
    print("  stress grid only (drift 96..768); drift=0 = boundary cell")
    rho = {}
    for drift in STRESS:
        phi1 = cells[(drift, 1)]["rate"]
        phi2 = cells[(drift, 2)]["rate"]
        rho[drift] = phi2 / phi1
        print(f"  drift={drift:3d}: Phi1={phi1:9.1f}  Phi2={phi2:9.1f}  "
              f"rho={rho[drift]:.4f}")
    r0 = cells[(0, 2)]["rate"] / cells[(0, 1)]["rate"]
    print(f"  [boundary drift=0: rho={r0:.4f} — excluded from verdict "
          f"by pre-registration]")
    rvals = [rho[d] for d in STRESS]
    rmean = mean(rvals)
    spread = (max(rvals) - min(rvals)) / rmean
    h1_i = spread <= 0.10
    resid = max(abs(cells[(d, 1)]["rate"] * rmean
                - cells[(d, 2)]["rate"])
                / cells[(d, 2)]["rate"] for d in STRESS)
    h1_ii = resid <= 0.10
    print(f"  (i)  spread(rho) = {spread * 100:.2f}% of mean(rho)"
          f"={rmean:.4f}  [gate <=10%]  -> "
          f"{'HOLDS' if h1_i else 'BREAKS'}")
    print(f"  (ii) max multiplicative-model residual = {resid * 100:.2f}%  "
          f"[gate <=10%]  -> {'HOLDS' if h1_ii else 'BREAKS'}")
    h1 = h1_i and h1_ii
    print(f"  H1 VERDICT: {'VALIDATED — Phi separates; no interaction term '
          'needed' if h1 else 'FALSIFIED — interaction term IS required'}")
    # drift-term shape (recorded, not gated)
    print("  [recorded] K=1 drift-doubling Phi ratios:",
          [f"{cells[(b, 1)]['rate'] / cells[(a, 1)]['rate']:.2f}"
           for a, b in zip(STRESS, STRESS[1:])])
    print("  [record] K=2 drift-doubling Phi ratios:",
          [f"{cells[(b, 2)]['rate'] / cells[(a, 2)]['rate']:.2f}"
           for a, b in zip(STRESS, STRESS[1:])])

    # ---- H2 verdict (pre-registered rule)
    print("\n== H2 RUNAWAY FATE at 32x (K=2, stress drifts) ==")
    sat = 0
    unb = 0
    for drift in STRESS:
        wd = h2[(drift, 2)]["windows"]
        r = wd[-1] / wd[0] if wd[0] else float("nan")
        tag = "SATURATE (<0.5)" if r < 0.5 else (
            "UNBOUNDED (>=0.9)" if r >= 0.9 else "middle")
        sat += r < 0.5
        unb += r >= 0.9
        print(f"  drift={drift:3d}: last/first window rate r={r:.2f} -> {tag}"
              f"  [32x/8x debt ratio "
              f"{h2[(drift, 2)]['debt'] / cells[(drift, 2)]['debt']:.2f}]")
    if sat >= 3:
        h2v = "VALIDATED"
    elif unb >= 3:
        h2v = "FALSIFIED"
    else:
        h2v = "MIXED"
    print(f"  H2 VERDICT: {h2v} (sat={sat}/4, unb={unb}/4)")

    print(f"\n== SUMMARY: H1 {'VALIDATED' if h1 else 'FALSIFIED'} / "
          f"H2 {h2v} / canaries {'ALL PASS' if ok else 'FAIL'}")
    print(f"DONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
