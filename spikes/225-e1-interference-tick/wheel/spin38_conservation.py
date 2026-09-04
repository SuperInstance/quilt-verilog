#!/usr/bin/env python3
"""SPIN 38, SPOKE: CONSERVATION — is the debt ceiling a conservation constant?

PRE-REGISTERED HYPOTHESIS (before any run; decision rule verbatim below):
  SPIN-15 found debt unbounded under drift=384 but hard-capped ~460k under
  delta->1 tightening (on ladder@30, 4800 ticks). Test whether that debt
  ceiling is a conservation-law constant: at FIXED grammar (outlier@30 —
  worst by SPIN-15's stable debt/ev ranking), the debt ceiling under
  escalation is a function of (drift, delta) ONLY:
  H1a: ceiling (final debt at 8x duration) scales ~linearly with drift
       at fixed (delta, K).
  H1b: ceiling tightens monotonically with delta at fixed (drift, K)
       (a stable, single-direction relationship in delta).
  H1c: the cap is REACHED (saturates within the run — last-window debt
       accumulation rate < 50% of first-window rate), not merely slowed,
       in the delta-small arms at minimum.
  H1d: expiry-evaporation per event stays in the measured 0.17-0.30 band
       across ALL arms.
  H1e: closure delta = 0 and pulse-mass delta = 0 on every run (wiring
       identities must hold under all escalated parameters).
  H0: ceiling unbounded (linear in-window growth everywhere) or
      non-monotone in drift/delta (>10% zig-zag), or evap band breaks,
      or any identity fails.

PRE-REGISTERED DECISION RULE (verbatim, immutable once run starts):
  VALIDATED   iff H1a AND H1b AND H1c AND H1d AND H1e all hold
              (H1a: for every (delta,K), debt monotone non-decreasing in
               drift over {96,192,384,768} AND each drift-doubling scales
               debt by ratio in [0.8, 1.25] for >= 2 of 3 doublings;
               H1b: for every (drift,K), debt monotone in delta with a
               consistent direction across all 3 delta steps or a plateau
               within 10%; H1c: >= half of the delta<=6 cells show
               last-window/first-window debt-rate ratio < 0.5).
  FALSIFIED   iff debt grows linearly in-window in ALL arms (no cap
              anywhere: last/first window ratio > 0.9 in every cell), OR
              any non-monotonicity > 10% in drift or delta, OR evap/event
              exits [0.17, 0.30] in any cell, OR any identity fails.
  MIXED       otherwise (report which sub-claims held/broke).
  INCONCLUSIVE if canaries fail or the environment crashes (no numbers
              count).

ARMS: drift in {0, 96, 192, 384, 768} x delta in {1, 6, 12} x K in {1, 2}
  on outlier@30 grammar (N=6), pd=3, ticks = 38400 (8x the 4800 base,
  SPIN-15's arm-C escalation, to let ceilings emerge within-run).
  Seeds {1, 7, 42, 1999, 20260902}. Integer-only inside every loop; floats
  only at print. Debt trajectory = 8 windows of 4800 ticks each.

CANARIES (all must PASS or INCONCLUSIVE):
  (a) wiring byte-identity vs exp_glm1.run_fabric on >=8 configs INCLUDING
      escalated parameters (this spin's operating region).
  (b) anchor replays: zero@15 K=1 -> 77.3% / ev 8756 / debt 187834;
      ladder@15 K=1 -> 71.5% / ev 5792 / debt 106378 (default params).
  (c) SPIN-15 drift=384 debt/event ~9202-and-climbing replay. NOTE: SPIN-15
      ran its saturation hunt on ladder@30 (worst by residency); the 9202.4
      number is ladder@30 K=1 drift=384 delta=12 @4800 ticks. Replay THAT
      config (tolerance +-5%) and also record outlier@30's value for the
      record.
  (d) double-run determinism on >=4 configs (full ledger byte-equality).
"""
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
PD = 3
N = 6
BASE_TICKS = 4800
TICKS = 38400            # 8x base — escalation duration
NW = TICKS // BASE_TICKS  # 8 windows
DRIFTS = (0, 96, 192, 384, 768)
DELTAS = (1, 6, 12)
KS = (1, 2)
GRAMMAR = ("outlier@30", [0, 0, 0, 0, 0, 30])
T0 = time.time()


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


ANCH_LAT = {"ladder@15": ladder(15), "zero": [0] * N}


# ---- fabric clone: every g/pulse line copied verbatim from spin15's
# ---- canary-proven clone (which itself copied exp_glm1.run_fabric).
# ---- ONLY additions: window debt snapshots (outside the fabric lines).
def run_ledger(lats, k, seed, ticks=TICKS, delta=12, drift=6, pd=PD):
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
    win = TICKS and ticks // NW or ticks
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
    print("== CANARY (a): wiring byte-identity vs exp_glm1.run_fabric ==")
    print("   8 configs INCLUDING escalated parameters (this spin's region)")
    ok = True
    cfgs = [
        (GRAMMAR, 1, 1, dict(drift=96, delta=6)),
        (GRAMMAR, 2, 42, dict(drift=96, delta=6)),
        (GRAMMAR, 1, 1, dict(drift=768, delta=1)),
        (GRAMMAR, 2, 42, dict(drift=768, delta=1)),
        (GRAMMAR, 1, 7, dict(drift=0, delta=12)),
        (("ladder@15", ANCH_LAT["ladder@15"]), 1, 1, dict(drift=6, delta=12)),
        (("zero", ANCH_LAT["zero"]), 2, 42, dict(drift=384, delta=12)),
        (GRAMMAR, 1, 1999, dict(drift=192, delta=12)),
    ]
    for (nm, lats), k, s, kw in cfgs:
        a = run_fabric("interference", BASE_TICKS, lats, K=k, pd=PD,
                       seed=s, **kw)
        b = run_ledger(lats, k, s, ticks=BASE_TICKS, **kw)
        same = a == {kk: b[kk] for kk in a}
        if not same:
            ok = False
            print(f"  MISMATCH {nm} K={k} seed={s} {kw}")
        else:
            print(f"  identical: {nm} K={k} seed={s} {kw}")
    print(f"  {'PASS' if ok else 'FAIL'}: {len(cfgs)}/{len(cfgs)} configs")
    return ok


def canary_b():
    ok = True
    print("\n== CANARY (b): SPIN-11 anchor replays (default drift=6 delta=12)")
    checks = (("zero@15   K=1", "zero", 1, 77.3, 8756, 187834),
              ("ladder@15 K=1", "ladder@15", 1, 71.5, 5792, 106378))
    for name, gname, k, want_tp, want_ev, want_debt in checks:
        rs = [run_ledger(ANCH_LAT[gname], k, s, ticks=BASE_TICKS)
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
    print("\n== CANARY (c): SPIN-15 drift=384 debt/ev ~9202 replay @4800t ==")
    ok = True
    for nm, lats in (("ladder@30", ladder(30)), GRAMMAR):
        rs = [run_ledger(lats, 1, s, ticks=BASE_TICKS, drift=384, delta=12)
              for s in SEEDS]
        dp = mean([r["mass"] / r["events"] if r["events"] else 0
                   for r in rs])
        print(f"  {nm} K=1 drift=384: debt/ev {dp:.1f}"
              + ("  (SPIN-15 anchor; want 9202.4 +-5% -> "
                 f"{'PASS' if abs(dp - 9202.4) / 9202.4 <= 0.05 else 'FAIL'})"
                 if nm == "ladder@30" else "  (outlier@30, recorded)"))
        if nm == "ladder@30":
            ok &= abs(dp - 9202.4) / 9202.4 <= 0.05
    return ok


def canary_d():
    print("\n== CANARY (d): double-run determinism (>=4 configs) ==")
    ok = True
    cfgs = [(GRAMMAR[1], 1, 1, dict(drift=0, delta=1)),
            (GRAMMAR[1], 2, 42, dict(drift=768, delta=6)),
            (GRAMMAR[1], 1, 7, dict(drift=384, delta=12)),
            (ANCH_LAT["zero"], 2, 1999, dict(drift=96, delta=6))]
    for i, (lats, k, s, kw) in enumerate(cfgs):
        r1 = key(run_ledger(lats, k, s, **kw))
        r2 = key(run_ledger(lats, k, s, **kw))
        good = r1 == r2
        ok &= good
        print(f"  cfg{i} K={k} seed={s} {kw}: "
              f"{'byte-identical' if good else 'DIVERGED'}")
    print(f"  {'PASS' if ok else 'FAIL'}: {len(cfgs)}/{len(cfgs)}")
    return ok


# ------------------------------------------------------- experiment
def cell(drift, delta, k):
    """Mean-over-seeds cell at 8x duration with trajectory windows."""
    rs = [run_ledger(GRAMMAR[1], k, s, drift=drift, delta=delta)
          for s in SEEDS]
    ids = all(all(check_identities(r).values()) for r in rs)
    ev = mean([r["events"] for r in rs])
    dbt = mean([r["mass"] for r in rs])
    # window DELTAS (debt accumulated per window), mean over seeds
    wd = []
    for j in range(NW):
        vals = []
        for r in rs:
            prev = r["windows"][j - 1] if j else 0
            vals.append(r["windows"][j] - prev)
        wd.append(mean(vals))
    evap = mean([abs(r["ledger"]["expired_total"])
                 / (r["events"] or 1) for r in rs])
    tp = mean([within_pm(r["resid"], delta) for r in rs]) / 10
    return dict(ev=ev, debt=dbt, dpev=dbt / (ev or 1), windows=wd,
                evap=evap, ids=ids, tp=tp)


def main():
    print("SPIN-38 CONSERVATION —", os.popen("date -u").read().strip())
    print("hypothesis + decision rule pre-registered in script header "
          "(unchanged at run time)")
    ok = canary_a() & canary_b() & canary_c() & canary_d()
    print("\nALL CANARIES:", "PASS" if ok else
          "FAIL -> INCONCLUSIVE, nothing below counts")
    if not ok:
        sys.exit(1)

    print(f"\n== ARMS: outlier@30, {TICKS} ticks (8x), pd=3, seeds {SEEDS}")
    cells = {}
    print("drift | delta | K | resid% | events | debt | debt/ev | "
          "evap/ev | w1->w8 debt-rate | IDs")
    for drift in DRIFTS:
        for delta in DELTAS:
            for k in KS:
                c = cell(drift, delta, k)
                cells[(drift, delta, k)] = c
                wd = c["windows"]
                print(f"{drift:5d} | {delta:5d} | {k} | {c['tp']:5.1f} | "
                      f"{c['ev']:9.0f} | {c['debt']:11.0f} | "
                      f"{c['dpev']:9.1f} | {c['evap']:7.3f} | "
                      f"{wd[0]:8.0f}->{wd[-1]:8.0f} "
                      f"(r {wd[-1] / wd[0] if wd[0] else float('nan'):.2f}) | "
                      f"{'4/4' if c['ids'] else 'FAIL'}")

    # ---- apply pre-registered decision rule
    print("\n== PRE-REGISTERED DECISION RULE APPLICATION ==")
    h1a_ok = True
    h1a_notes = []
    for delta in DELTAS:
        for k in KS:
            seq = [cells[(d, delta, k)]["debt"]
                   for d in (96, 192, 384, 768)]
            mono = all(b >= a for a, b in zip(seq, seq[1:]))
            ratios = [b / a if a else float("inf")
                      for a, b in zip(seq, seq[1:])]
            inline = sum(0.8 <= r <= 1.25 for r in ratios)
            good = mono and inline >= 2
            h1a_ok &= good
            h1a_notes.append((delta, k, mono, ratios, good))
    print(f"  H1a (linear drift scaling, ratio [0.8,1.25] x>=2/3 doublings): "
          f"{'HOLDS' if h1a_ok else 'BREAKS'}")
    for delta, k, mono, ratios, good in h1a_notes:
        print(f"    delta={delta} K={k}: mono={mono} "
              f"ratios={[f'{r:.2f}' for r in ratios]} -> "
              f"{'ok' if good else 'VIOLATION'}")

    h1b_ok = True
    for drift in DRIFTS:
        for k in KS:
            seq = [cells[(drift, d_, k)]["debt"] for d_ in DELTAS]
            up = all(b >= a * 0.9 for a, b in zip(seq, seq[1:]))
            dn = all(b <= a * 1.1 for a, b in zip(seq, seq[1:]))
            good = up or dn
            h1b_ok &= good
            print(f"  H1b drift={drift} K={k}: debt by delta "
                  f"{[f'{v:.0f}' for v in seq]} -> "
                  f"{'ok' if good else 'NON-MONOTONE (>10% zig-zag)'}")
    print(f"  H1b (monotone-in-delta with consistent direction): "
          f"{'HOLDS' if h1b_ok else 'BREAKS'}")

    small_cells = [cells[(d, d_, k)] for d in DRIFTS for d_ in (1, 6)
                   for k in KS]
    sat = sum(1 for c in small_cells
              if c["windows"][0] and c["windows"][-1] / c["windows"][0] < 0.5)
    h1c_ok = sat >= len(small_cells) // 2
    print(f"  H1c (cap reached: last/first window rate < 0.5 in >= half of "
          f"delta<=6 cells): {sat}/{len(small_cells)} -> "
          f"{'HOLDS' if h1c_ok else 'BREAKS'}")

    h1d_ok = all(0.17 <= c["evap"] <= 0.30 for c in cells.values())
    evap_lo = min(c["evap"] for c in cells.values())
    evap_hi = max(c["evap"] for c in cells.values())
    print(f"  H1d (evap/event in [0.17,0.30]): observed "
          f"[{evap_lo:.3f}, {evap_hi:.3f}] -> "
          f"{'HOLDS' if h1d_ok else 'BREAKS'}")

    h1e_ok = all(c["ids"] for c in cells.values())
    print(f"  H1e (closure/mass identities every run): "
          f"{'HOLDS' if h1e_ok else 'BREAKS'}")

    all_linear = all(c["windows"][0]
                     and c["windows"][-1] / c["windows"][0] > 0.9
                     for c in cells.values())
    nonmono = not (h1a_ok or True)  # zig-zag detected per-cell above
    zig = any(not g for _, _, _, _, g in h1a_notes) or not h1b_ok

    if h1a_ok and h1b_ok and h1c_ok and h1d_ok and h1e_ok:
        verdict = "VALIDATED"
    elif all_linear or zig or not h1d_ok or not h1e_ok:
        verdict = "FALSIFIED"
    else:
        verdict = "MIXED"
    print(f"\n  VERDICT (pre-registered rule): {verdict}")
    if all_linear:
        print("   (basis: linear in-window growth everywhere — no cap)")
    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
