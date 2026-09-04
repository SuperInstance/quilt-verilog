#!/usr/bin/env python3
"""SPIN 22 (spoke 8: DEQUANT) — INTERFERENCE-vs-SEQUENTIAL at MATCHED BUDGET.

The old interference-vs-sequential gap (956 vs 745 permille-era claims; the
arena baselines "impulse ~52% vs interference ~83%" at stress) compared arms
with UNEQUAL twin-evaluation and application budgets: interference reads all
N twins and applies up to N pulses per tick; sequential-first-trigger reads
all N twins but applies at most 1 impulse per tick. SPIN-dequant-2 left this
as its top open edge: does the interference advantage survive when sequential
is given the same SENSOR-EVALUATION budget?

BUDGET DEFINITION (fixed before any run):
  budget = sensor reads (reality evaluations). A tick of the N=6 fabric
  costs 6 reads in INT and SEQ-EVERY, 1 read in SEQ-RR.

ARMS (stress fabric: N=6, delta=12, drift=6, pd=3, lats per grammar):
  INT        : interference (exp_glm1 verbatim arm), 6 reads/tick,
               <=6 applied pulses/tick.            ticks=4800 -> 28800 reads
  SEQ-EVERY  : sequential first-trigger (exp_glm1 verbatim arm), 6 reads/tick,
               <=1 impulse/tick.                   ticks=4800 -> 28800 reads
               (read-budget-matched to INT; application-budget 1/6 of INT)
  SEQ-RR     : sequential ROUND-ROBIN, 1 read/tick (twin i = t mod N),
               <=1 impulse/tick.                   ticks=28800 -> 28800 reads
               (read-budget-matched to INT AND application-budget-matched
               in expected max-applies-per-read)
  SEQ-RR4800 : same arm at ticks=4800 (4800 reads) — lower-budget anchor,
               isolates the "N x the ticks" credit.

GRAMMARS: zero [0]*6, ladder15 [0,3,6,9,12,15], cohort33 [0,0,0,30,30,30].
Metric: pct = permille of ticks with |s_true - g| <= delta, /10 at print.
Integer-only inside every loop; floats only at aggregation/print.
5 seeds (1,7,42,1999,20260902). python3 -u direct redirect, no pipes.

PRE-REGISTERED DECISION RULES (stated BEFORE any panel run):
  DR1 SURVIVES: interference's budget-matched advantage is REAL iff, on the
     zero grammar, pct(INT,K) - pct(SEQ-RR@28800) >= 3.0pp for a MAJORITY
     of K in {1,2,4,8} (>=3 of 4), AND the best-INT - SEQ-RR@28800 gap
     >= 3.0pp on >=2 of 3 grammars.
  DR2 BUDGET-ARTIFACT: the old gap is an evaluation/application-budget
     artifact iff pct(SEQ-RR@28800) >= pct(INT at its best K) - 3.0pp on
     >=2 of 3 grammars (i.e. DR1's second clause fails).
  DR3 EFFICIENCY: report settles-per-1000-reads and mass-per-read; an arm
     may lose on pct yet win on efficiency — booked separately, no override.
  Threshold 3.0pp = 2x typical 5-seed mean noise (~1.5pp observed across
  SPIN-10..21 panels); chosen before any run.

CANARIES (mandatory gate before any panel):
  a. byte-identity of the inline clones vs exp_glm1.run_fabric:
     INT-vs-interference and SEQ-EVERY-vs-sequential, 4 configs x 2 seeds.
  b. published anchors EXACT: zero K=1 = 77.3% / ev 8756 / debt 187834;
     ladder15 K=1 = 71.5% / ev 5792 / debt 106378 (5-seed sums/means).
  c. determinism: every arm type run twice, byte-identical resid.

Usage: python3 spin22_dequant.py   (single pass, prints as it goes)
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
TICKS_RR = TICKS * N          # 28800: read-budget match to INT/SEQ-EVERY
KS = (1, 2, 4, 8)
GRAMMARS = (
    ("zero",     [0] * N),
    ("ladder15", [0, 3, 6, 9, 12, 15]),
    ("cohort33", [0, 0, 0, 30, 30, 30]),
)
RT = [reality(t) for t in range(240)]
T0 = time.time()


def ridx(t):
    return RT[t % 240]


# ---------------------------------------------------------------- clones
def run_int(lats, k, seed, ticks=TICKS):
    """Interference arm, verbatim exp_glm1 physics (canary a proves it)."""
    rng = LCG(seed)
    g = ridx(0)
    pulses = deque()
    resid = []
    events = mass = 0
    reads = 0
    for t in range(ticks):
        reads += len(lats)
        s_true = ridx(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        trig = 0
        for lat in lats:
            e = ridx(t - lat if t >= lat else 0) - g
            if e > DELTA or e < -DELTA:
                trig += 1
                m = abs(e) // PD or 1
                pulses.appendleft([m if e > 0 else -m, k])
                events += 1
                mass += abs(e)
        if pulses:
            net = 0
            for p in pulses:
                net += p[0]
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
        resid.append(abs(s_true - g))
    return dict(resid=resid, events=events, mass=mass, reads=reads,
                ticks=ticks)


def run_seq_every(lats, seed, ticks=TICKS):
    """Sequential first-trigger arm, verbatim exp_glm1 semantics."""
    rng = LCG(seed)
    g = ridx(0)
    resid = []
    events = mass = 0
    reads = 0
    for t in range(ticks):
        reads += len(lats)
        s_true = ridx(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT
        e0 = 0
        fired = False
        for lat in lats:
            e = ridx(t - lat if t >= lat else 0) - g
            if (e > DELTA or e < -DELTA) and not fired:
                e0 = e
                fired = True
        if fired:
            g += e0
            events += 1
            mass += e0 if e0 > 0 else -e0
        resid.append(abs(s_true - g))
    return dict(resid=resid, events=events, mass=mass, reads=reads,
                ticks=ticks)


def run_seq_rr(lats, seed, ticks):
    """Sequential round-robin: 1 read/tick, twin i = t mod N, snap on trig."""
    n = len(lats)
    rng = LCG(seed)
    g = ridx(0)
    resid = []
    events = mass = 0
    reads = 0
    for t in range(ticks):
        lat = lats[t % n]
        reads += 1
        s_true = ridx(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT
        e = ridx(t - lat if t >= lat else 0) - g
        if e > DELTA or e < -DELTA:
            g += e
            events += 1
            mass += e if e > 0 else -e
        resid.append(abs(s_true - g))
    return dict(resid=resid, events=events, mass=mass, reads=reads,
                ticks=ticks)


ARMS = (("INT", run_int), ("SEQ-EVERY", run_seq_every), ("SEQ-RR", run_seq_rr))


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY a: inline clones byte-identical to exp_glm1.run_fabric ==")
    nchk = 0
    cfgs = (("zero", [0] * N, 1), ("zero", [0] * N, 2),
            ("ladder15", [0, 3, 6, 9, 12, 15], 4),
            ("cohort33", [0, 0, 0, 30, 30, 30], 2))
    for name, lats, k in cfgs:
        for sd in (1, 42):
            if run_int(lats, k, sd)["resid"] != run_fabric(
                    "interference", TICKS, lats, K=k, pd=PD, delta=DELTA,
                    drift=DRIFT, seed=sd)["resid"]:
                ok = False
                print(f"  MISMATCH INT {name} K={k} seed={sd}")
            if run_seq_every(lats, sd)["resid"] != run_fabric(
                    "sequential", TICKS, lats, K=k, pd=PD, delta=DELTA,
                    drift=DRIFT, seed=sd)["resid"]:
                ok = False
                print(f"  MISMATCH SEQ {name} K={k} seed={sd}")
            nchk += 2
    print(f"  {'PASS' if ok else 'FAIL'}: {nchk} raw-resid arrays identical")

    print("\n== CANARY b: published anchors EXACT (interference, 5 seeds) ==")
    want = (("zero", [0] * N, 1, 773, 8756, 187834),
            ("ladder15", [0, 3, 6, 9, 12, 15], 1, 715, 5792, 106378))
    for name, lats, k, pct0, ev0, m0 in want:
        ev = mass = st = 0
        for sd in SEEDS:
            r = run_int(lats, k, sd)
            ev += r["events"]
            mass += r["mass"]
            st += sum(1 for x in r["resid"] if x <= DELTA)
        pctm = st * 1000 // (len(SEEDS) * TICKS)
        good = (pctm == pct0 and round(ev / 5) == ev0
                and round(mass / 5) == m0)
        ok &= good
        print(f"  {name:<9} K=1: pct {pctm/10:.1f} (want {pct0/10:.1f}) "
              f"ev {round(ev/5)} (want {ev0}) debt {round(mass/5)} "
              f"(want {m0}) "
              f"-> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY c: determinism (each arm twice, byte-identical) ==")
    c3 = True
    for label, fn, kw in (("INT", run_int, dict(k=4)),  # noqa
                          ("SEQ-EVERY", run_seq_every, dict()),
                          ("SEQ-RR", run_seq_rr, dict(ticks=TICKS_RR))):
        a = fn(lats=[0] * N, seed=7, **kw)
        b = fn(lats=[0] * N, seed=7, **kw)
        if a["resid"] != b["resid"] or a["events"] != b["events"]:
            c3 = False
            print(f"  NONDETERMINISTIC {label}")
    print(f"  {'PASS' if c3 else 'FAIL'}")
    return ok and c3


# ---------------------------------------------------------------- panels
def agg(runs):
    st = sum(1 for r in runs for x in r["resid"] if x <= DELTA)
    tk = sum(r["ticks"] for r in runs)
    ev = sum(r["events"] for r in runs)
    mass = sum(r["mass"] for r in runs)
    rd = sum(r["reads"] for r in runs)
    return dict(pct=st * 1000 // tk, ev=ev, mass=mass, reads=rd,
                eff=st * 1000 // max(1, rd),          # settles/1000 reads
                mpr=mass // max(1, rd))               # mass per read


def main():
    print("SPIN-22 DEQUANT — INTERFERENCE-vs-SEQUENTIAL at MATCHED BUDGET —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"config: N={N} delta={DELTA} drift={DRIFT} pd={PD} seeds={SEEDS}")
    print("budget = sensor READS. INT/SEQ-EVERY: 6 reads/tick @4800 = 28800;")
    print("SEQ-RR: 1 read/tick @28800 = 28800 (matched); @4800 = 4800 (anchor).")
    print("DR1 SURVIVES: zero-grammar INT-vs-SEQRR gap >= 3.0pp for >=3 of 4 K")
    print("        AND best-INT - SEQRR >= 3.0pp on >=2 of 3 grammars.")
    print("DR2 BUDGET-ARTIFACT: SEQRR >= best-INT - 3.0pp on >=2 of 3 grammars.")
    print("DR3: efficiency (settles/1000 reads, mass/read) booked separately.")
    sys.stdout.flush()

    if not canaries():
        print("\nALL CANARIES: FAIL — nothing below counts")
        sys.exit(1)
    print("\nALL CANARIES: PASS")
    sys.stdout.flush()

    # ---- PANEL 1: baseline grid, 4800 ticks (per grammar, per arm)
    print("\n== PANEL 1: grammars x arms x K (5-seed means; pct in %) ==")
    print(f"{'grammar':>9} {'arm':>10} {'K':>2} {'pct':>6} {'events':>7} "
          f"{'debt':>8} {'reads':>7} {'set/kr':>7} {'mass/r':>7}")
    res = {}
    for gname, lats in GRAMMARS:
        for k in KS:
            a = agg([run_int(lats, k, sd) for sd in SEEDS])
            res[(gname, "INT", k)] = a
            print(f"{gname:>9} {'INT':>10} {k:>2} {a['pct']/10:>6.1f} "
                  f"{a['ev']//5:>7} {a['mass']//5:>8} {a['reads']//5:>7} "
                  f"{a['eff']/10:>7.1f} {a['mpr']:>7}")
        a = agg([run_seq_every(lats, sd) for sd in SEEDS])
        res[(gname, "SEQ-EVERY", 0)] = a
        print(f"{gname:>9} {'SEQ-EVERY':>10} {'-':>2} {a['pct']/10:>6.1f} "
              f"{a['ev']//5:>7} {a['mass']//5:>8} {a['reads']//5:>7} "
              f"{a['eff']/10:>7.1f} {a['mpr']:>7}")
        for tk, lab in ((TICKS_RR, "SEQ-RR28"), (TICKS, "SEQ-RR04")):
            a = agg([run_seq_rr(lats, sd, ticks=tk) for sd in SEEDS])
            res[(gname, lab, 0)] = a
            print(f"{gname:>9} {lab:>10} {'-':>2} {a['pct']/10:>6.1f} "
                  f"{a['ev']:>7} {a['mass']:>8} {a['reads']:>7} "
                  f"{a['eff']/10:>7.1f} {a['mpr']:>7}")
        sys.stdout.flush()

    # ---- PANEL 2: budget-matched gaps
    print("\n== PANEL 2: budget-matched gaps (pp, INT minus SEQ-RR@28800) ==")
    print(f"{'grammar':>9}" + "".join(f"{'K=' + str(k):>8}" for k in KS)
          + f"{'bestK':>8}{'SEQ-EV':>8}{'SEQRR04':>8}")
    dr1a = dr2 = 0
    gaps = {}
    for gname, _ in GRAMMARS:
        row = {}
        for k in KS:
            row[k] = (res[(gname, "INT", k)]["pct"]
                      - res[(gname, "SEQ-RR28", 0)]["pct"]) / 10.0
        gaps[gname] = row
        best = max(KS, key=lambda k: res[(gname, "INT", k)]["pct"])
        print(f"{gname:>9}" + "".join(f"{row[k]:>8.1f}" for k in KS)
              + f"{row[best]:>8.1f}"
              + f"{(res[(gname, 'SEQ-EVERY', 0)]['pct'] - res[(gname, 'SEQ-RR28', 0)]['pct'])/10:>8.1f}"
              + f"{(res[(gname, 'SEQ-RR04', 0)]['pct'] - res[(gname, 'SEQ-RR28', 0)]['pct'])/10:>8.1f}")
    # DR1 clause 1: zero grammar majority
    zw = sum(1 for k in KS if gaps["zero"][k] >= 3.0)
    # DR1 clause 2 / DR2: best-INT gap on >=2 of 3 grammars
    best_gaps = []
    for gname, _ in GRAMMARS:
        b = max(res[(gname, "INT", k)]["pct"] for k in KS)
        best_gaps.append((b - res[(gname, "SEQ-RR28", 0)]["pct"]) / 10.0)
    n_surv = sum(1 for x in best_gaps if x >= 3.0)
    print(f"\nDR1 clause 1 (zero, >=3 of 4 K with gap>=3.0pp): {zw}/4 "
          f"-> {'PASS' if zw >= 3 else 'FAIL'}")
    print(f"DR1 clause 2 (best-INT gap>=3.0pp on >=2/3 grammars): "
          f"{n_surv}/3 (gaps {[round(x,1) for x in best_gaps]}) "
          f"-> {'PASS' if n_surv >= 2 else 'FAIL'}")
    print(f"DR1 OVERALL: {'SURVIVES' if (zw >= 3 and n_surv >= 2) else 'FAILS'}")
    print(f"DR2 BUDGET-ARTIFACT: {'YES' if n_surv < 2 else 'no'}")

    # ---- PANEL 3: efficiency at matched reads (DR3)
    print("\n== PANEL 3: efficiency at matched 28800 reads (5-seed totals) ==")
    print(f"{'grammar':>9} {'arm':>10} {'set/kr':>8} {'mass/r':>8} "
          f"{'ev/kr':>7}")
    for gname, _ in GRAMMARS:
        best = max(KS, key=lambda k: res[(gname, "INT", k)]["pct"])
        for lab in ("INT(bK)", "SEQ-EVERY", "SEQ-RR28"):
            key = (gname, "INT", best) if lab == "INT(bK)" else \
                (gname, "SEQ-EVERY" if lab == "SEQ-EVERY" else "SEQ-RR28", 0)
            a = res[key]
            print(f"{gname:>9} {lab:>10} {a['eff']/10:>8.1f} {a['mpr']:>8} "
                  f"{a['ev'] * 1000 // max(1, a['reads']):>7}")

    print(f"\nDONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
