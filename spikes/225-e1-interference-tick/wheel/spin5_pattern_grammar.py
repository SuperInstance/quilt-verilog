#!/usr/bin/env python3
"""SPIN 5, SPOKE: PATTERN-GRAMMAR — the second-order dial proposed by SPIN-4.

SPIN-4 verdict: spread is the first-order dial (ladder knee ~15) but
pattern-invariance was FALSIFIED (cohort 49.3% vs ladder 26.8% at
spread=30, K=1) and spread=0 is a chatter anomaly (worse than spread=5).
This spoke holds total spread fixed and sweeps the multiset GRAMMAR.

Fabric: exp_glm1.run_fabric (E1 contract: fdiv decay, 64-bit LCG, FIFO
oldest-first expiry, snapshot decay). Integer-only inside the loop; floats
appear ONLY in display statistics (means, interpolated crossings, Pearson r).

HYPOTHESES:
  H1 (densified knee): the ladder knee localizes to +-2 and tracks the
     slope-adjusted 2*DELTA crossing (reality slope 8/5 per tick:
     (8/5)*spread = 24 -> spread ~15), not the raw 2*DELTA = 24.
  H2 (grammar dial): at fixed total spread (15 and 30) the multiset grammar
     moves true-residency by >= 10pp; the majority axis (size of the largest
     coherent cohort: zero 6+0, outlier 5+1, quart 4+2, cohort 3+3,
     tri 2+2+2, ladder graded 1+1+1+1+1+1) orders the result.
  H3 (chatter mechanism): the spread=0 anomaly is synchronized-duplicate
     chatter: all twins read the SAME residual, all fire the SAME tick
     (Spin-1's gap=1 refire mode at cohort scale), the arm applies
     ~6*(e//3) ~ 2e and overshoots onto its own echo, re-firing next tick.
     Quantified: grammar losses correlate with same-tick correlated
     corrections across the grammar sweep.

DESIGN: N=6 fixed, interference arm, 4800 ticks, stress params
(delta=12, drift=6, pd=3), seeds {1,7,42,1999,20260902}, K in {1,2}.
Grammars at nominal spread s (max-min latency):
  ladder  : [0, s/5, 2s/5, ..., s]   graded (SPIN-4 continuity)
  cohort  : [0,0,0,s,s,s]            half-half 3+3 (SPIN-4 cohort)
  tri     : [0,0,s//2,s//2,s,s]      tripartite 2+2+2 (the literal
                                     ((0,0),(15,15),(30,30)) reading)
  quart   : [0,0,0,0,s,s]            4 fresh + 2 stale
  outlier : [0,0,0,0,0,s]            single stale outlier (5+1)
  paired  : [0,s,0,s,0,s]            duplicate pairs (== cohort multiset;
                                     order-invariance canary C)
  zero    : [0]*6                    synchronized chatter mode (ignores s)

CANARIES (mandatory — every one must PASS before any result counts):
  A. spread=0: all 7 grammar codepaths byte-identical (K in {1,2}).
  B. SPIN-4 replay: ladder spread=15 K=1 within published numbers
     (per-seed permille 709/713/721/714/717, events mean 5792,
      debt mean 106378, cancels mean 4).
  C. order-invariance: paired == cohort byte-identical in BOTH arms
     (interference correction is a function of the error multiset only;
     sequential trig[0] resolves to fresh-else-stale for both orders).
  D. zero-lock ignores nominal spread: zero@15 == zero@30 byte-identical.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
N = 6
TICKS = 4800


# ---------------------------------------------------------- grammars
def ladder(s):
    return [round(i * s / (N - 1)) for i in range(N)]


def cohort(s):
    return [0, 0, 0, s, s, s]


def tri(s):
    return [0, 0, s // 2, s // 2, s, s]


def quart(s):
    return [0, 0, 0, 0, s, s]


def outlier(s):
    return [0, 0, 0, 0, 0, s]


def paired(s):
    return [0, s, 0, s, 0, s]


def zero(s):
    return [0] * N


GRAMMARS = (("ladder", ladder), ("cohort", cohort), ("tri", tri),
            ("quart", quart), ("outlier", outlier), ("paired", paired),
            ("zero", zero))


# ---------------------------------------------------------- helpers
def one(mode, lats, k, seed):
    return run_fabric(mode, TICKS, lats, K=k, pd=3, delta=DELTA,
                      drift=6, seed=seed)


def scalars(r):
    return dict(true_pm=within_pm(r["resid"], DELTA),
                all_pm=1000 * r["settles"] // r["ticks"],
                events=r["events"], debt=r["mass"],
                cancels=r["cancels"], chatter=r["chatter"])


def fingerprint(r):
    """Exact-enough identity: scalars + tuple hash of the full resid and
    cflags traces (Python tuple hash is comparison-grade)."""
    s = scalars(r)
    return (s["true_pm"], s["all_pm"], s["events"], s["debt"],
            s["cancels"], s["chatter"], hash(tuple(r["resid"])),
            hash(tuple(r["cflags"])))


def byte_identical(r1, r2):
    return (fingerprint(r1) == fingerprint(r2)
            and tuple(r1["resid"]) == tuple(r2["resid"])
            and tuple(r1["cflags"]) == tuple(r2["cflags"]))


def chatter_stats(r):
    """Per-tick correction-event statistics from the emissions ledger.
    multi2 : event-ticks where >=2 sensors fired (same-tick correlated)
    full   : event-ticks where all 6 fired (fully synchronized)
    refire1: events (t,i) whose sensor also fired at t-1 (Spin-1 gap-1)
    sync   : consecutive event-ticks whose firing sets overlap by >=2
             (synchronized duplicates refiring together)
    shares in permille of event-ticks / events respectively."""
    per = {}
    seen = set()
    for (t, i, pm, e) in r["emissions"]:
        per.setdefault(t, []).append(i)
        seen.add((t, i))
    ts = sorted(per)
    multi2 = full = sync = 0
    for t in ts:
        if len(per[t]) >= 2:
            multi2 += 1
        if len(per[t]) == N:
            full += 1
    for a, b in zip(ts, ts[1:]):
        if b - a == 1 and len(per[b]) >= 2 and len(set(per[b])
                                                  & set(per[a])) >= 2:
            sync += 1
    refire1 = sum(1 for (t, i) in seen if (t - 1, i) in seen)
    nev = max(1, len(r["emissions"]))
    nt = max(1, len(ts))
    return dict(multi2=multi2, full=full, refire1=refire1, sync=sync,
                ticks_ev=len(ts), mshare=1000 * multi2 // nt,
                rshare=1000 * refire1 // nev, sshare=1000 * sync // nt)


def mean(v):
    return sum(v) / len(v)  # display only


def pearson(xs, ys):
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = ((sum((x - mx) ** 2 for x in xs)
            * sum((y - my) ** 2 for y in ys)) ** 0.5)
    return num / den if den else 0.0  # display only


def row(cells):
    return " | ".join(f"{c:>8}" for c in cells)


# ---------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY A: spread=0 byte-identical across all 7 grammar "
          "codepaths ==")
    for k in (1, 2):
        base = one("interference", ladder(0), k, SEEDS[0])
        for gname, gfn in GRAMMARS[1:]:
            other = one("interference", gfn(0), k, SEEDS[0])
            if not byte_identical(base, other):
                ok = False
                print(f"  MISMATCH K={k} ladder(0) vs {gname}(0)")
    print("  PASS: 12/12 comparisons byte-identical (7 grammars x K{1,2})"
          if ok else "  FAIL")

    print("\n== CANARY B: SPIN-4 replay (ladder spread=15, K=1) ==")
    pub_true = (709, 713, 721, 714, 717)
    res = [one("interference", ladder(15), 1, s) for s in SEEDS]
    got = tuple(scalars(r)["true_pm"] for r in res)
    ev = mean([scalars(r)["events"] for r in res])
    dbt = mean([scalars(r)["debt"] for r in res])
    can = mean([scalars(r)["cancels"] for r in res])
    b_ok = (got == pub_true and abs(ev - 5792) <= 1
            and abs(dbt - 106378) <= 100 and abs(can - 4) <= 0.5)
    print(f"  per-seed true_pm got {got} pub {pub_true}")
    print(f"  events {ev:.1f} (pub 5792)  debt {dbt:.0f} (pub 106378)  "
          f"cancels {can:.1f} (pub 4, display-rounded)")
    print("  PASS: replay within published numbers" if b_ok
          else "  FAIL: replay DRIFTED")
    ok &= b_ok

    print("\n== CANARY C: order-invariance (paired == cohort multiset) ==")
    c_ok = True
    for mode in ("interference", "sequential"):
        for s in (15, 30):
            for k in ((1, 2) if mode == "interference" else (1,)):
                for sd in SEEDS:
                    r1 = one(mode, cohort(s), k, sd)
                    r2 = one(mode, paired(s), k, sd)
                    if not byte_identical(r1, r2):
                        c_ok = False
                        print(f"  MISMATCH {mode} s={s} K={k} seed={sd}")
    print("  PASS: paired == cohort byte-identical, both arms, "
          "s{15,30}, K{1,2}, 5 seeds (30/30)" if c_ok else "  FAIL")
    ok &= c_ok

    print("\n== CANARY D: zero-lock ignores nominal spread (zero@15 == "
          "zero@30) ==")
    d_ok = True
    for k in (1, 2):
        for sd in SEEDS:
            r1 = one("interference", zero(15), k, sd)
            r2 = one("interference", zero(30), k, sd)
            if not byte_identical(r1, r2):
                d_ok = False
                print(f"  MISMATCH K={k} seed={sd}")
    print("  PASS: zero@15 == zero@30 byte-identical (K{1,2}, 5 seeds)"
          if d_ok else "  FAIL")
    ok &= d_ok
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — results below do "
          "NOT count")
    return ok


# ---------------------------------------------------------- exp 1
def exp1_knee():
    spreads = (10, 12, 14, 15, 16, 18, 20, 22, 24)
    print("\n== EXP 1: DENSIFIED KNEE (ladder, N=6 interference, per-seed "
          "permille) ==")
    print(row(["spread", "lats", "K", "s1", "s7", "s42", "s1999",
               "s2s60902", "mean%", "evMean", "debtMean", "canc"]))
    means = {1: {}, 2: {}}
    for s in spreads:
        for k in (1, 2):
            res = [one("interference", ladder(s), k, sd) for sd in SEEDS]
            tp = [scalars(r)["true_pm"] for r in res]
            means[k][s] = mean(tp)
            print(row([s, str(ladder(s)), k] + tp +
                      [f"{means[k][s]/10:.1f}",
                       f"{mean([scalars(r)['events'] for r in res]):.0f}",
                       f"{mean([scalars(r)['debt'] for r in res]):.0f}",
                       f"{mean([scalars(r)['cancels'] for r in res]):.0f}"]))

    print("\n== EXP 1b: sequential reference (K=1, ladder) ==")
    print(row(["spread", "mean%", "evMean", "debtMean"]))
    smean = {}
    for s in spreads:
        res = [one("sequential", ladder(s), 1, sd) for sd in SEEDS]
        smean[s] = mean([scalars(r)["true_pm"] for r in res])
        print(row([s, f"{smean[s]/10:.1f}",
                   f"{mean([scalars(r)['events'] for r in res]):.0f}",
                   f"{mean([scalars(r)['debt'] for r in res]):.0f}"]))

    print("\n== EXP 1c: knee localization ==")
    for k in (1, 2):
        m = means[k]
        pts = sorted(m)
        raw = max(zip(pts, pts[1:]),
                  key=lambda ab: m[ab[0]] - m[ab[1]])
        norm = max(zip(pts, pts[1:]),
                   key=lambda ab: (m[ab[0]] - m[ab[1]]) / (ab[1] - ab[0]))
        cross = None
        for a, b in zip(pts, pts[1:]):
            if m[a] >= 500 >= m[b]:
                cross = a + (m[a] - 500) * (b - a) / (m[a] - m[b])
                break
        print(f"  K={k}: steepest raw drop {m[raw[0]]/10:.1f}->"
              f"{m[raw[1]]/10:.1f} over [{raw[0]},{raw[1]}]; "
              f"steepest per-spread-unit over [{norm[0]},{norm[1]}] "
              f"({(m[norm[0]]-m[norm[1]])/(norm[1]-norm[0])/10:.1f}pp/unit); "
              f"50%-crossing at spread ~= "
              f"{cross if cross is not None else 'none (never crosses)'}")
    cross = None
    pts = sorted(smean)
    for a, b in zip(pts, pts[1:]):
        if smean[a] >= 500 >= smean[b]:
            cross = a + (smean[a] - 500) * (b - a) / (smean[a] - smean[b])
            break
    print(f"  sequential K=1: 50%-crossing at spread ~= {cross}")
    print("  reference marks: slope-adjusted 2*DELTA crossing = 15 "
          "((8/5)*15=24); raw 2*DELTA = 24")


# ---------------------------------------------------------- exp 2
SWEEP = []  # (grammar, s, k, true_pm mean, scalars mean, chatter mean)


def exp2_grammar():
    print("\n== EXP 2: GRAMMAR SWEEP at fixed total spread (N=6 "
          "interference, per-seed permille) ==")
    print(row(["s", "grammar", "lats", "K", "s1", "s7", "s42", "s1999",
               "s2s60902", "mean%", "allW", "evMean", "debtMean", "canc",
               "mShare", "rShare", "sShare"]))
    for s in (15, 30):
        for gname, gfn in GRAMMARS:
            for k in (1, 2):
                res = [one("interference", gfn(s), k, sd) for sd in SEEDS]
                sc = [scalars(r) for r in res]
                ch = [chatter_stats(r) for r in res]
                tp = [x["true_pm"] for x in sc]
                SWEEP.append(dict(g=gname, s=s, k=k, true=mean(tp),
                                  mshare=mean([c["mshare"] for c in ch]),
                                  rshare=mean([c["rshare"] for c in ch]),
                                  sshare=mean([c["sshare"] for c in ch]),
                                  events=mean([x["events"] for x in sc])))
                print(row([s, gname, str(gfn(s)), k] + tp +
                          [f"{mean(tp)/10:.1f}",
                           f"{mean([x['all_pm'] for x in sc])/10:.1f}",
                           f"{mean([x['events'] for x in sc]):.0f}",
                           f"{mean([x['debt'] for x in sc]):.0f}",
                           f"{mean([x['cancels'] for x in sc]):.0f}",
                           f"{mean([c['mshare'] for c in ch]):.0f}",
                           f"{mean([c['rshare'] for c in ch]):.0f}",
                           f"{mean([c['sshare'] for c in ch]):.0f}"]))

    print("\n== EXP 2b: sequential control (K=1, per grammar) ==")
    print(row(["s", "grammar", "mean%", "evMean", "debtMean"]))
    for s in (15, 30):
        for gname, gfn in GRAMMARS:
            res = [one("sequential", gfn(s), 1, sd) for sd in SEEDS]
            sc = [scalars(r) for r in res]
            print(row([s, gname,
                       f"{mean([x['true_pm'] for x in sc])/10:.1f}",
                       f"{mean([x['events'] for x in sc]):.0f}",
                       f"{mean([x['debt'] for x in sc]):.0f}"]))

    print("\n== EXP 2c: grammar effect size at fixed spread (interference) ==")
    for s in (15, 30):
        for k in (1, 2):
            vals = [(d["g"], d["true"] / 10) for d in SWEEP
                    if d["s"] == s and d["k"] == k]
            lo = min(vals, key=lambda gv: gv[1])
            hi = max(vals, key=lambda gv: gv[1])
            print(f"  s={s} K={k}: min {lo[0]} {lo[1]:.1f}%  max {hi[0]} "
                  f"{hi[1]:.1f}%  spread-of-grammar {hi[1]-lo[1]:.1f}pp")


# ---------------------------------------------------------- exp 3
def excerpt(title, r, want_full, start_min=1200, width=30):
    per = {}
    for (t, i, pm, e) in r["emissions"]:
        per.setdefault(t, []).append((i, pm, e))
    ts = [t for t in sorted(per)
          if t >= start_min and (len(per[t]) == N if want_full
                                 else len(per[t]) >= 2)]
    t0 = ts[0] if ts else start_min
    print(f"\n  -- {title}: per-tick log t={t0}..{t0+width-1} "
          f"(nFired | fired-set | sumPM | maxTrig | residAfter) --")
    for t in range(t0, t0 + width):
        evs = per.get(t, [])
        sset = ",".join(str(i) for i, _, _ in evs) or "-"
        spm = sum(pm for _, pm, _ in evs)
        mtr = max((abs(e) for _, _, e in evs), default=0)
        print(f"  t={t:>4}  n={len(evs)}  [{sset:>11}]  sumPM={spm:>5}  "
              f"maxTrig={mtr:>4}  resid={r['resid'][t]:>3}")


def exp3_chatter():
    print("\n== EXP 3a: chatter stats, named modes (interference, 5-seed "
          "means) ==")
    print(row(["mode", "K", "true%", "ticksEv", "multi2", "full6",
               "refire1", "sync", "mShare", "rShare", "sShare"]))
    for gname, gfn in (("zero", zero), ("paired", paired), ("cohort", cohort),
                       ("ladder", ladder)):
        for k in (1, 2):
            res = [one("interference", gfn(15), k, sd) for sd in SEEDS]
            sc = [scalars(r) for r in res]
            ch = [chatter_stats(r) for r in res]
            print(row([f"{gname}@15", k,
                       f"{mean([x['true_pm'] for x in sc])/10:.1f}",
                       f"{mean([c['ticks_ev'] for c in ch]):.0f}",
                       f"{mean([c['multi2'] for c in ch]):.0f}",
                       f"{mean([c['full'] for c in ch]):.0f}",
                       f"{mean([c['refire1'] for c in ch]):.0f}",
                       f"{mean([c['sync'] for c in ch]):.0f}",
                       f"{mean([c['mshare'] for c in ch]):.0f}",
                       f"{mean([c['rshare'] for c in ch]):.0f}",
                       f"{mean([c['sshare'] for c in ch]):.0f}"]))

    print("\n== EXP 3b: mechanism excerpts (seed 1) ==")
    r = one("interference", zero(15), 1, SEEDS[0])
    excerpt("zero-lock K=1 (fully synchronized fires)", r, True)
    r = one("interference", paired(15), 1, SEEDS[0])
    excerpt("paired-duplicates K=1 (>=2-sensor fires)", r, False)

    print("\n== EXP 3c: echo sign analysis, zero-lock K=1 (does the arm "
          "re-fire on its own overshoot?) ==")
    for sd in SEEDS:
        r = one("interference", zero(15), 1, sd)
        per = {}
        for (t, i, pm, e) in r["emissions"]:
            per[t] = per.get(t, 0) + pm
        ts = sorted(per)
        flips = same = 0
        for a, b in zip(ts, ts[1:]):
            if b - a == 1:
                if (per[a] > 0) != (per[b] > 0):
                    flips += 1
                else:
                    same += 1
        gap1 = sum(1 for a, b in zip(ts, ts[1:]) if b - a == 1)
        print(f"  seed {sd:>9}: event-ticks {len(ts)}  consecutive-pairs "
              f"{gap1}  sign-FLIP {flips}  sign-SAME {same}")

    print("\n== EXP 3d: do grammar losses correlate with same-tick "
          "correlated corrections? (Pearson over 28 sweep configs) ==")
    ys = [d["true"] / 10 for d in SWEEP]
    for key, label in (("mshare", "multi-sensor share"),
                       ("rshare", "same-sensor gap1 refire share"),
                       ("sshare", "synchronized-refire share")):
        xs = [d[key] for d in SWEEP]
        print(f"  r(true%, {label:<32}) = {pearson(xs, ys):+.3f}")
    for s in (15, 30):
        sub = [d for d in SWEEP if d["s"] == s]
        ys2 = [d["true"] / 10 for d in sub]
        for key in ("mshare", "rshare", "sshare"):
            xs2 = [d[key] for d in sub]
            print(f"  s={s}: r(true%, {key}) = "
                  f"{pearson(xs2, ys2):+.3f}  (n={len(sub)})")

    print("\n== EXP 3e: Spin-1 gap=1 refractory check across the grammar "
          "sweep ==")
    hits = 0
    for s in (15, 30):
        for gname, gfn in GRAMMARS:
            for k in (1, 2):
                for sd in SEEDS:
                    r = one("interference", gfn(s), k, sd)
                    if chatter_stats(r)["refire1"] > 0:
                        hits += 1
    print(f"  runs with same-sensor gap-1 refires: {hits}/140 "
          f"(Spin-1 found min-gap 1 in 20/20 runs)")


if __name__ == "__main__":
    ok = canaries()
    if ok:
        exp1_knee()
        exp2_grammar()
        exp3_chatter()
    else:
        print("ABORT: canaries failed — no results collected.")
