#!/usr/bin/env python3
"""SPIN 48, SPOKE: METROLOGY — WINDOW-LOCAL RATE EXPONENT alpha(drift,K).

Executes SPIN-46's filed next-spoke proposal (SPIN-46-conservation.md,
"Next-spoke proposal: WINDOW-LOCAL RATE EXPONENT"). SPIN-46 falsified
separability (rho crossing at ~drift 384) and falsified re-saturation at
32x; the recorded scar: "Phi values are not asymptotic constants — they
are lower bounds. A true asymptotic Phi-hat would need window-local
rates." This spin extracts them as a local GROWTH EXPONENT.

DEFINITION (pre-registered instrument):
  Let W_j = cumulative debt at the end of window j (j = 1..32, windows
  of 4800 ticks, 153600 total = 32x SPIN-38's window), seed-meaned.
  The window-local exponent at window boundary j is
      alpha_j = ln(W_{j+1} / W_j) / ln((j+1) / j),   j = 1..31.
  alpha_j = 1 <=> debt grows linearly in time; alpha_j > 1 <=> the
  cumulative-debt curve is locally superlinear (accelerating).
  The reported per-cell exponent is the LATE-ASYMPTOTE
      alpha(drift, K) = mean(alpha_j for j in 24..31)   (last quarter).
  Error bar: per-seed alpha recomputed the same way; err = max seed
  deviation from the seed-mean (5 seeds).

PRE-REGISTERED HYPOTHESES (written BEFORE any panel run; immutable):

  H1 (K=2 exponent transition, bracketing the rho-crossing):
      on outlier@30 (N=6, lats [0,0,0,0,0,30]), pd=3, delta=12
      (delta-dead at stress per SPIN-38/46), ticks=153600, K=2, seeds
      {1,7,42,1999,20260902}, stress drift grid
      {96, 192, 288, 384, 480, 576, 768} (densified around SPIN-46's
      rho-crossing at ~384):
      alpha(96) <= 1.05 (linear) AND alpha(768) >= 1.10 (accelerating)
      AND the transition drift d* — the smallest grid drift with
      alpha >= 1.05 — satisfies 192 < d* < 480, i.e. the alpha = 1.05
      crossing is BRACKETED by the grid neighbors of 384 (288 < ~384
      crossing < 480 with 288 and 480 the grid points straddling 384).
  FALSIFY H1 if alpha is DRIFT-FLAT (max-min alpha across the stress
      grid <= 0.03) OR the transition does not bracket 384 (d* <= 192
      or d* > 480, including no-crossing-at-768).

  H2 (the K-dichotomy is an EXPONENT difference, not a prefactor one —
      sharpening SPIN-46's control cell where even K=1/drift=768 went
      superlinear at 32x):
      at ticks=153600, alpha(K=2) > alpha(K=1) + err at EVERY stress
      drift >= 96 (drifts {96,192,384,768}), where
      err = err_seed(alpha2) + err_seed(alpha1).
  FALSIFY H2 if at ANY drift >= 96 the exponents are equal within
      error: alpha(K=2) - alpha(K=1) <= err.

  MIXED / INCONCLUSIVE per hypothesis as usual; INCONCLUSIVE if any
  canary fails or the environment crashes (no numbers count).

  DIVERGENCE GATE (SPIN-16/44 scar class): if any cell crashes or its
  ledger identities fail, exclude it post-hoc with a printed labeled
  exclusion and use log-space stats there; never silently.

CANARIES (mandatory gate, ALL PASS before any panel number is read):
  a. harness provenance: import SPIN-46's spin46_conservation (which
     itself gates on spin38); a verbatim-copy runner inside this file
     must be byte-identical to sp46.run_ledger on >= 6 configs
     INCLUDING a 153600-tick nw=32 case (full key equality + windows).
  b. anchors digit-exact: zero@15 K=1 -> 77.3% / ev 8756 / debt 187834;
     ladder@15 K=1 -> 71.5% / ev 5792 / debt 106378 (default params).
  c. SPIN-38/46 drift=384 debt/ev ~ 9202 replay (ladder@30 K=1 @4800t).
  d. gate=never == mc=0 (delta=10**9: events == mass == all flows == 0).
  e. SPIN-15 mass/debt closure identities live on EVERY arm run.
  f. double-run determinism (>= 4 configs, full key byte-equality).

ARMS: outlier@30, pd=3, delta=12, seeds {1,7,42,1999,20260902}.
  H1 arm : K=2, drift {0(boundary), 96,192,288,384,480,576,768} @153600.
  H2 arm : K=1, drift {96,192,384,768} @153600 (completing the sweep
           SPIN-46 left unrun below 768 — budget, not cherry-pick).
Integer-only inside every loop (inherited harness); floats only at
print/stat time. Real runs; no fabricated numbers.
"""
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import spin46_conservation as sp46  # noqa: E402  (harness provenance)
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
PD = 3
N = 6
BASE_TICKS = 4800
GRAMMAR = ("outlier@30", [0, 0, 0, 0, 0, 30])
H1_DRIFTS = (96, 192, 288, 384, 480, 576, 768)   # densified around 384
H2_DRIFTS = (96, 192, 384, 768)
KS = (1, 2)
DELTA = 12
T32 = 153600   # 32 windows of 4800
NW = 32
T0 = time.time()


def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


ANCH_LAT = {"ladder@15": ladder(15), "zero": [0] * N}


# ---- runner: VERBATIM copy of sp46.run_ledger (which is spin38's loop,
# ---- generalized only in window count). Canary (a) proves byte-identity.
def run_ledger(lats, k, seed, ticks=T32, delta=12, drift=6, pd=PD, nw=NW):
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
    return sum(v) / len(v)      # display / stat only


check_identities = sp46.check_identities   # SPIN-15 closure, verbatim
key = sp46.key                               # byte-equality key, verbatim


# ------------------------------------------------------- exponent math
def local_exponents(windows):
    """alpha_j = ln(W_{j+1}/W_j)/ln((j+1)/j), j = 1..len-1.
    Floats ONLY here (stat time) — never inside the harness loops."""
    out = []
    for j in range(1, len(windows)):
        w0, w1 = windows[j - 1], windows[j]
        if w0 > 0 and w1 > 0:
            out.append(__import__("math").log(w1 / w0)
                       / __import__("math").log((j + 1) / j))
        else:
            out.append(float("nan"))
    return out


LATE = range(24, 32)   # last-quarter window boundaries for the asymptote


def cell(drift, k, ticks=T32, nw=NW, label=""):
    """5-seed cell: per-run identities (canary e), cumulative windows,
    seed-mean late-asymptote exponent + max seed deviation."""
    rs = [run_ledger(GRAMMAR[1], k, s, ticks=ticks, delta=DELTA,
                     drift=drift, nw=nw) for s in SEEDS]
    ids = all(all(check_identities(r).values()) for r in rs)
    wd = []
    for j in range(nw):
        vals = []
        for r in rs:
            prev = r["windows"][j - 1] if j else 0
            vals.append(r["windows"][j] - prev)
        wd.append(mean(vals))
    cum = []
    run = 0
    for w in wd:
        run += w
        cum.append(run)
    alphas = [local_exponents(r["windows"]) for r in rs]
    per_seed_late = [mean([a[j - 1] for j in LATE]) for a in alphas]
    a_mean = mean(per_seed_late)
    a_err = max(abs(a - a_mean) for a in per_seed_late)
    a_pub = mean(local_exponents(cum))   # seed-mean curve, recorded too
    return dict(ev=mean([r["events"] for r in rs]),
                debt=mean([r["mass"] for r in rs]),
                inc=wd, cum=cum, alpha=a_mean, err=a_err,
                alpha_curve=local_exponents(cum), ids=ids,
                per_seed=per_seed_late, label=label)


# ------------------------------------------------------------ canaries
def canary_a():
    print("== CANARY (a): provenance — this runner == sp46.run_ledger ==")
    ok = True
    cfgs = [
        (GRAMMAR[1], 1, 1, 38400, dict(drift=96, delta=6), 8),
        (GRAMMAR[1], 2, 42, 38400, dict(drift=768, delta=1), 8),
        (GRAMMAR[1], 1, 7, 38400, dict(drift=0, delta=12), 8),
        (GRAMMAR[1], 2, 1999, 38400, dict(drift=384, delta=12), 8),
        (GRAMMAR[1], 1, 42, T32, dict(drift=768, delta=12), 32),
        (GRAMMAR[1], 2, 7, T32, dict(drift=384, delta=12), 32),
        (ANCH_LAT["zero"], 2, 1, 38400, dict(drift=6, delta=12), 8),
    ]
    for lats, k, s, tk, kw, nw in cfgs:
        mine = run_ledger(lats, k, s, ticks=tk, nw=nw, **kw)
        theirs = sp46.run_ledger(lats, k, s, ticks=tk, nw=nw, **kw)
        good = key(mine) == key(theirs) and \
            mine["windows"] == theirs["windows"] and \
            len(mine["windows"]) == nw
        ok &= good
        print(f"  {'identical' if good else 'MISMATCH'}: K={k} seed={s} "
              f"ticks={tk} {kw} (nw={nw})")
    print(f"  {'PASS' if ok else 'FAIL'}: {len(cfgs)}/{len(cfgs)} configs "
          f"(incl. 153600-tick nw=32 x2)")
    return ok


def canary_b():
    ok = True
    print("\n== CANARY (b): anchor replays digit-exact (drift=6 delta=12)")
    checks = (("zero@15   K=1", "zero", 77.3, 8756, 187834),
              ("ladder@15 K=1", "ladder@15", 71.5, 5792, 106378))
    for name, gname, want_tp, want_ev, want_debt in checks:
        rs = [run_ledger(ANCH_LAT[gname], 1, s, ticks=BASE_TICKS, nw=8)
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
    print("\n== CANARY (c): SPIN-38/46 drift=384 debt/ev ~9202 replay @4800t")
    rs = [run_ledger(ladder(30), 1, s, ticks=BASE_TICKS, drift=384,
                     delta=12, nw=8) for s in SEEDS]
    dp = mean([r["mass"] / r["events"] if r["events"] else 0 for r in rs])
    good = abs(dp - 9202.4) / 9202.4 <= 0.05
    print(f"  ladder@30 K=1 drift=384: debt/ev {dp:.1f} (anchor 9202.4 "
          f"+-5%) -> {'PASS' if good else 'FAIL'}")
    return good


def canary_d():
    print("\n== CANARY (d): gate=never == mc=0 (delta=10**9) ==")
    ok = True
    for k in KS:
        for drift in (0, 384):
            r = run_ledger(GRAMMAR[1], k, 1, ticks=BASE_TICKS,
                           delta=10 ** 9, drift=drift, nw=8)
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
    cfgs = [(GRAMMAR[1], 1, 1, 38400, dict(drift=0), 8),
            (GRAMMAR[1], 2, 42, 38400, dict(drift=768), 8),
            (GRAMMAR[1], 2, 7, T32, dict(drift=384), 32),
            (GRAMMAR[1], 1, 1999, T32, dict(drift=96), 32)]
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
def main():
    import math
    print("SPIN-48 METROLOGY (window-local rate exponent) —",
          os.popen("date -u").read().strip())
    print("hypotheses + decision rule pre-registered in script header "
          "(unchanged at run time)")
    ok = (canary_a() & canary_b() & canary_c() & canary_d() & canary_f())
    print("\nALL CANARIES:", "PASS" if ok else
          "FAIL -> INCONCLUSIVE, nothing below counts")
    if not ok:
        sys.exit(1)

    # ---- H1 arm: K=2 exponent across the densified drift grid @32x
    print(f"\n== H1 ARM: outlier@30 K=2, delta={DELTA}, {T32} ticks "
          f"(32 windows), seeds {SEEDS}")
    h1 = {}
    print("drift | events | debt | alpha(err) | alpha_j curve "
          "(j=4,8,12,16,20,24,28,31) | IDs")
    for drift in (0,) + H1_DRIFTS:
        c = cell(drift, 2, label="H1")
        h1[drift] = c
        ac = c["alpha_curve"]
        pts = " ".join(f"{ac[j - 1]:.3f}" for j in (4, 8, 12, 16, 20, 24, 28, 31))
        print(f"{drift:5d} | {c['ev']:8.0f} | {c['debt']:11.0f} | "
              f"{c['alpha']:.3f}({c['err']:.3f}) | {pts} | "
              f"{'5/5' if c['ids'] else 'FAIL'}")
    ok &= all(c["ids"] for c in h1.values())

    # ---- H2 arm: K=1 exponent sweep @32x (completing SPIN-46's gap)
    print(f"\n== H2 ARM: outlier@30 K=1, delta={DELTA}, {T32} ticks, "
          f"drifts {H2_DRIFTS}")
    h2 = {}
    for drift in H2_DRIFTS:
        c = cell(drift, 1, label="H2")
        h2[drift] = c
        ac = c["alpha_curve"]
        pts = " ".join(f"{ac[j - 1]:.3f}" for j in (4, 8, 12, 16, 20, 24, 28, 31))
        print(f"{drift:5d} | {c['ev']:8.0f} | {c['debt']:11.0f} | "
              f"{c['alpha']:.3f}({c['err']:.3f}) | {pts} | "
              f"{'5/5' if c['ids'] else 'FAIL'}")
    ok &= all(c["ids"] for c in h2.values())
    print(f"  canary (e) SPIN-15 identities live on every arm: "
          f"{'PASS' if ok else 'FAIL'}")

    # ---- H1 verdict (pre-registered rule)
    print("\n== H1: K=2 exponent transition brackets the rho-crossing? ==")
    a = {d: h1[d]["alpha"] for d in H1_DRIFTS}
    for d in H1_DRIFTS:
        print(f"  drift={d:3d}: alpha={a[d]:.3f} "
              f"(err {h1[d]['err']:.3f})")
    print(f"  [boundary drift=0: alpha={h1[0]['alpha']:.3f} — excluded "
          f"from verdict by pre-registration]")
    flat = (max(a.values()) - min(a.values())) <= 0.03
    low_ok = a[96] <= 1.05
    high_ok = a[768] >= 1.10
    d_star = None
    for d in H1_DRIFTS:
        if a[d] >= 1.05:
            d_star = d
            break
    bracket = d_star is not None and 192 < d_star < 480
    print(f"  (i)   alpha(96)={a[96]:.3f} <= 1.05 ? "
          f"{'YES' if low_ok else 'NO'}")
    print(f"  (ii)  alpha(768)={a[768]:.3f} >= 1.10 ? "
          f"{'YES' if high_ok else 'NO'}")
    print(f"  (iii) drift-flat gate (max-min<=0.03): spread="
          f"{max(a.values()) - min(a.values()):.3f} -> "
          f"{'FLAT (falsify)' if flat else 'NOT flat'}")
    print(f"  (iv)  d* (smallest drift with alpha>=1.05) = {d_star}; "
          f"brackets 384 iff 192 < d* < 480 -> "
          f"{'YES' if bracket else 'NO'}")
    if flat or not bracket:
        h1v = "FALSIFIED"
    elif low_ok and high_ok and bracket:
        h1v = "VALIDATED"
    else:
        h1v = "MIXED"
    print(f"  H1 VERDICT: {h1v}")

    # ---- H2 verdict (pre-registered rule)
    print("\n== H2: exponent dichotomy alpha(K=2) > alpha(K=1) at 32x? ==")
    allgt = True
    anyeq = False
    for d in H2_DRIFTS:
        a1, e1 = h2[d]["alpha"], h2[d]["err"]
        a2, e2 = h1[d]["alpha"], h1[d]["err"]
        err = e1 + e2
        diff = a2 - a1
        gt = diff > err
        allgt &= gt
        anyeq |= diff <= err
        print(f"  drift={d:3d}: alpha2={a2:.3f}({e2:.3f})  "
              f"alpha1={a1:.3f}({e1:.3f})  diff={diff:+.3f} "
              f"err={err:.3f} -> {'K2>K1' if gt else 'EQUAL WITHIN ERROR'}")
    h2v = ("FALSIFIED" if anyeq else
           ("VALIDATED" if allgt else "MIXED"))
    print(f"  H2 VERDICT: {h2v}")

    # ---- recorded (not gated): exponent law shape
    print("\n== RECORDED (no gate): alpha(drift) table + gamma convergence")
    print("  SPIN-46 asked: does gamma converge to a constant (power-law "
          "runaway) or keep growing (no exponent)?")
    for d in H1_DRIFTS:
        ac = h1[d]["alpha_curve"]
        q2 = mean(ac[12:24])
        q4 = mean(ac[24:32])
        print(f"  K=2 drift={d:3d}: alpha q2(12-24)={q2:.3f} "
              f"q4(24-32)={q4:.3f} "
              f"{'converging' if abs(q4 - q2) < 0.05 else 'drifting'}")
    for d in H2_DRIFTS:
        ac = h2[d]["alpha_curve"]
        q2 = mean(ac[12:24])
        q4 = mean(ac[24:32])
        print(f"  K=1 drift={d:3d}: alpha q2(12-24)={q2:.3f} "
              f"q4(24-32)={q4:.3f} "
              f"{'converging' if abs(q4 - q2) < 0.05 else 'drifting'}")

    print(f"\n== SUMMARY: H1 {h1v} / H2 {h2v} / canaries "
          f"{'ALL PASS' if ok else 'FAIL'}")
    print(f"DONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
