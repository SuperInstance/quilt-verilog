#!/usr/bin/env python3
"""SPIN 11 — SPOKE: PULSE-DIAL / MASS-COMPENSATION (dispatched by SPIN-8's
proposal; proposal-dispatched, no LCG pick consumed).

Tests Spin 8's integer law: divergence iff N > 2*pd (echo factor
|1 - N/pd| > 1). Three blades:

EXP 1 — pd sweep (uncompensated): pd in {1,2,3,6,12} x N in
    {2,3,4,5,6,7,8,12,13,24,25} (grid + 2pd/2pd+1 edge probes) at fixed
    grammar family (spread-30 ladder, N rungs), delta=12, K=1, drift=6.
    Locate the divergence edge to +/-1 N for each pd.

EXP 2 — mass compensation. Two integer emission-fabric variants (both are
    exact copies of exp_glm1.run_fabric's interference branch plus one
    division; mc=0 is byte-identical to the original):
      MC-A (brief's formula): per-twin magnitude (|e|//pd) // min(n_f, pd)
      MC-B (total-cap):       per-twin magnitude (|e|//pd) // n_f
    (both floored at 1, the fabric's `or 1` minimum-pulse contract).
    2a: compensated pd-sweep grids — where did the wall go?
    2b: rescue detail at pd=3, steps {1,2,3,5,6,10,15,30}, K=1 —
        headline rescue = comp(step5/N=7) - 0.3.
    2c: pathology audit on coarse grammars (cohort/kcoh5/kcoh1/ladder@30).

EXP 3 — joint map: best-compensated variant x delta in {12,24} x K in
    {1,2,4} x 5 grammars, comp on/off — does compensation interact with
    the K=2 echo-overlap trough?

=====================================================================
PRE-REGISTERED PREDICTIONS — written into this committed file BEFORE
any run. (Spin-8's scar honored: every prediction pins the eval window
to FIXED EV=12, i.e. within_pm(resid, 12), regardless of trigger delta.)

P1a (absolute): MC-A step5/N=7 (lats [0,5,10,15,20,25,30]) at pd=3,
    delta=12, K=1, spread 30, true12 = 22.0%, band [12, 32]. Basis:
    wall erased -> grammar-geometry-limited, comparable to spin-8's
    below-wall coarse family (step6 26.8, step10 10.5, cohort 49.3);
    fine ladder has fresher cohort than step6 but weaker anchor than
    cohort -> mid. RESCUE defined as >= 10x uncomp (>= 3.0%); predicted.

P1b (relative, instantiated from EXP 1 output before EXP 2 runs):
    MC-A step5@pd3 true12 in [E6 - 8, E6 + 8] where E6 := UNCOMPENSATED
    step5/N=7 at pd=6 (below the N=12 wall: pure geometry, no mass
    divergence). Mechanism: compensation caps total per-event shove at
    ~e//pd, i.e. removes firing mass as a variable; E6 measures the same
    grammar with the mass variable inert by dial instead of by emission.
    Band +/-8pp covers pd-response shape differences (shove e/9 vs e/6).

P2 (wall tracking): in EXP 1 the divergence edge (smallest diverged N,
    divergence := all 5 seeds maxResid > 10^6) sits at exactly
    N = 2*pd + 1 for every pd in {1,2,3,6,12}: safe at 2pd, diverged at
    2pd+1, ladder geometry notwithstanding.

P3 (compensated wall remnants):
    P3a: MC-A at pd=1 is STRUCTURALLY immune (min(n_f,1)=1): byte-identical
         trajectories to uncompensated — edge stays at N=3.
    P3b: MC-A edge moves to 2*pd^2+1 where that is inside the grid:
         pd=2 -> edge 9 (2pd^2+1); pd=3 -> edge in (12,25], probed at
         {18,19,20} (echo arithmetic says 18 safe / 19 diverged);
         pd=6,12 -> no divergence anywhere in N<=25 (edge 73, 289).
    P3c: MC-B diverges NOWHERE in the whole pd x N grid (net capped at
         ~e//pd per event, echo |1-1/pd| < 1 for pd>=2, ~0 at pd=1).

P4 (K-trough interaction): under the best-compensated variant at
    delta=12, pd=3, the K=2 echo-overlap trough PERSISTS for >= 3 of 4
    coarse grammars {kcoh5, kcoh1, ladder, cohort}@30 (comp K=2 <
    min(comp K=1, comp K=4)): the trough is overlap geometry, not firing
    mass, so compensation should not close it.

EXP 4 — mixed-pd adjudication (EXPERT nudge 2026-09-03, ACCEPTED;
    added to THIS SAME COMMIT before any run, so it is pre-registered
    too). O2b (round 3, de5ad6b) located a fan-out wall at N=6 — EVEN,
    which cannot be 2pd+1 for integer pd. Two families could produce it:
    (a) heterogeneous/effective pd (mix of twin periods -> pd_eff in
    (2,3)), or (b) a different law. Instrument: half pd_a / half pd_b
    twins (per-sensor pd, alternating by index) on ladder(30,N),
    UNCOMPENSATED, delta=12, K=1, N in {4,5,6,7,8,9,13}, same seeds,
    divergence := all 5 seeds maxResid > 10^6 (EXP 1's definition).
    Note pd=2 twins individually diverge at N=5, so mix (2,3)'s edge is
    bounded above by 5 unless the fabric as a whole behaves otherwise.

P5a (mix 2,3): edge = 5 = weakest-member law — the pd=2 half diverges
    at its own wall and drags the shared g; heterogeneity does NOT
    create an even wall; O2b's N=6 stays a separate law (booked as
    such). ALTERNATIVE outcomes: edge 6 -> effective-pd unification
    anchor for O2b; edge > 5 -> mixture protection (non-diverging
    members absorb the diverging half's shove).
P5b (mix 3,6): pure walls are 7 and 13, so NO member individually
    diverges below 7 — this arm is the clean adjudicator. Registered
    BEFORE the run: edge 7 = weakest-member law (primary prediction);
    edge 6 = even wall from pd_eff ~ 4-5 in (3,6) -> O2b unification,
    the room-pressure mapping gets a predictive anchor; edge >= 8 or
    none = mixture protection / sub-linear composition.
Canary D (mandatory): hetero runner with a UNIFORM pd list is
    byte-identical (full dict) to run_fabric_mc(mc=0) across 4 configs
    — the per-sensor path adds nothing when the population is pure.

Canaries (mandatory, abort on fail):
  A: run_fabric_mc(mc=0) full-dict byte-identity vs exp_glm1.run_fabric
     across 8 configs (grammars x pd x K x delta, incl. spread-0).
  B: spread=0 byte-identity across grammar codepaths, grouped by N,
     separately for mc=0 and mc=1 and mc=2 (spin-8's canary A extended).
  C: spin-8 replay: step6/N=6 K=1 = 26.8 (+/-0.2), step5/N=7 K=1 = 0.3
     published (brief said 0.1 -> accept [0.0, 0.5]), step1/N=31 = 0.1,
     kcoh5@30 = 53.2 (+/-0.2). All true12, pinned EV=12.
"""
import os
import sys
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "inventors-derby"))
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
TICKS = 4800
DELTA = 12
EV = 12                # PINNED eval window for every prediction (spin-8 scar)
STEPS = (1, 2, 3, 5, 6, 10, 15, 30)
PDS = (1, 2, 3, 6, 12)
NGRID = (2, 4, 5, 6, 7, 8, 12, 24)
DIV_AT = 10 ** 6       # divergence threshold on per-seed maxResid


# ---------------------------------------------------------------- fabric
class LCG:
    def __init__(self, seed):
        self.x = seed & 0x7FFFFFFF or 1

    def next(self):
        self.x = (1103515245 * self.x + 12345) & 0x7FFFFFFF
        return self.x

    def below(self, n):
        return self.next() % n


def reality(t):
    phase = t % 240
    if phase < 96:
        return 400 + phase * 8 // 5
    elif phase < 144:
        return 400 + 96 * 8 // 5 - (phase - 96)
    else:
        return 400 + 96 * 8 // 5 - 48 - (phase - 144) * 8 // 5


def run_fabric_mc(mode, ticks, lats, lies=None, K=4, pd=3, delta=12, drift=6,
                  seed=20260902, mc=0):
    """EXACT copy of exp_glm1.run_fabric's loop with one added emission
    rule. mc=0: byte-identical to the original. mc=1: MC-A
    (|e|//pd)//min(n_f,pd). mc=2: MC-B (|e|//pd)//n_f. Both floored at 1."""
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    n = len(lats)
    lies = lies or {}
    emissions = []
    events = mass = cancels = chatter = settles = 0
    last = -10
    resid = []
    cflags = []

    for t in range(ticks):
        reads = [reality(max(0, t - lats[i])) + (lies[i](t) if i in lies else 0)
                 for i in range(n)]
        s_true = reality(t)
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > delta]

        cflag = 0
        if mode == "sequential":
            if trig:
                i, e = trig[0]
                g += e
                events += 1
                mass += abs(e)
                emissions.append((t, i, e, e))
                if t - last == 1:
                    chatter += 1
                last = t
        else:
            nf = len(trig)
            if mc == 1:
                neff = min(nf, pd)
            elif mc == 2:
                neff = nf
            else:
                neff = 1 if nf else 0
            for i, e in trig:
                m = abs(e) // pd or 1
                if neff > 1:
                    m = m // neff or 1
                pm = m if e > 0 else -m
                pulses.appendleft([pm, K])
                events += 1
                mass += abs(e)
                emissions.append((t, i, pm, e))
            if pulses:
                net = sum(p[0] for p in pulses)
                if net == 0 and any(p[0] > 0 for p in pulses) \
                        and any(p[0] < 0 for p in pulses):
                    cancels += 1
                    cflag = 1
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
            if trig:
                if t - last == 1:
                    chatter += 1
                last = t

        resid.append(abs(s_true - g))
        cflags.append(cflag)
        if all(abs(r - g) <= delta for r in reads):
            settles += 1

    return dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
                settles=settles, resid=resid, cflags=cflags,
                emissions=emissions, audit=None, ticks=ticks)


# ---------------------------------------------------------------- helpers
def ladder_step(s, g):
    return list(range(0, s + 1, g))


def ladder(s, n=6):
    return [round(i * s / (n - 1)) for i in range(n)]


def kcoh(k, s):
    return [0] * k + [s] * (6 - k)


def mean(v):
    return sum(v) / len(v)


def cap(x):
    return min(x, 10 ** 18)   # display-only cap, spin-8 convention


def mult10(emissions):
    """mean fire-multiplicity *10 and max multiplicity (integer)."""
    c = Counter(t for t, i, pm, e in emissions)
    if not c:
        return 0, 0
    return 10 * sum(c.values()) // len(c), max(c.values())


def cell(lats, pd, K=1, delta=DELTA, mc=0, seeds=SEEDS):
    rs = [run_fabric_mc("interference", TICKS, lats, K=K, pd=pd, delta=delta,
                        drift=6, seed=s, mc=mc) for s in seeds]
    t12 = [within_pm(r["resid"], EV) for r in rs]
    mr = [max(r["resid"]) for r in rs]
    mm = [mult10(r["emissions"])[0] for r in rs]
    return dict(t12=t12, m=mean(t12) / 10, mr=mr, div=all(x > DIV_AT for x in mr),
                mm=mean(mm) / 10, rs=rs)


def show(c):
    return f"{c['m']:5.1f}{'D' if c['div'] else ' '}"


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY A: run_fabric_mc(mc=0) byte-identity vs exp_glm1.run_fabric ==")
    cfgs = [
        (ladder(30), dict(pd=3, K=1)),
        (ladder(30), dict(pd=3, K=2)),
        (kcoh(5, 30), dict(pd=3, K=1)),
        ([0, 0, 0, 30, 30, 30], dict(pd=12, K=4)),
        (ladder_step(30, 5), dict(pd=1, K=1)),
        (ladder(0), dict(pd=6, K=8)),
        ([0] * 7, dict(pd=2, K=1)),
        (ladder_step(0, 3), dict(pd=12, K=2)),
    ]
    for lats, kw in cfgs:
        a = run_fabric("interference", TICKS, lats, drift=6, seed=SEEDS[0], **kw)
        b = run_fabric_mc("interference", TICKS, lats, drift=6, seed=SEEDS[0],
                          mc=0, **kw)
        if a != b:
            ok = False
            print(f"  MISMATCH lats={lats[:8]} {kw}")
    print(f"  {'PASS' if ok else 'FAIL'}: {len(cfgs)} configs full-dict identical")

    print("\n== CANARY A2: MC-A at pd=1 structural immunity (mc=1 == mc=0) ==")
    ok2 = True
    for lats in (ladder(30), ladder_step(30, 5), [0] * 7):
        a = run_fabric_mc("interference", TICKS, lats, K=1, pd=1, delta=DELTA,
                          drift=6, seed=SEEDS[0], mc=0)
        b = run_fabric_mc("interference", TICKS, lats, K=1, pd=1, delta=DELTA,
                          drift=6, seed=SEEDS[0], mc=1)
        if a != b:
            ok2 = False
            print(f"  MISMATCH lats={lats[:8]}")
    print(f"  {'PASS' if ok2 else 'FAIL'}: min(n_f,1)=1 -> MC-A inert at pd=1"
          f" (P3a prerequisite holds structurally)")
    ok &= ok2

    print("\n== CANARY B: spread=0 codepath identity by N-group, per mc mode ==")
    fams = {f"step{g}": ladder_step(0, g) for g in (1, 2, 3, 5, 6, 10, 15, 30)}
    fams.update({"ladder0": ladder(0), "kcoh5_0": kcoh(5, 0), "kcoh1_0": kcoh(1, 0),
                 "cohort0": [0] * 6})
    groups = {}
    for name, lats in fams.items():
        groups.setdefault(len(lats), []).append(name)
    for mc in (0, 1, 2):
        okb = True
        for nn, names in sorted(groups.items()):
            ref = run_fabric_mc("interference", TICKS, fams[names[0]], K=1, pd=3,
                                delta=DELTA, drift=6, seed=SEEDS[0], mc=mc)
            for nm in names[1:]:
                if run_fabric_mc("interference", TICKS, fams[nm], K=1, pd=3,
                                 delta=DELTA, drift=6, seed=SEEDS[0], mc=mc) != ref:
                    okb = False
                    print(f"  MISMATCH mc={mc} N={nn} {nm}")
        print(f"  mc={mc}: {'PASS' if okb else 'FAIL'}"
              f" ({sum(len(v) for v in groups.values())} codepaths,"
              f" {len(groups)} N-groups)")
        ok &= okb

    print("\n== CANARY C: spin-8 replay (5-seed means, true12 pinned EV=12) ==")
    targets = [
        ("step6/N=6 K=1", ladder(30), 1, 3, 26.8, 0.2),
        ("step5/N=7 K=1", ladder_step(30, 5), 1, 3, 0.3, 0.5),
        ("step1/N=31 K=1", ladder_step(30, 1), 1, 3, 0.1, 0.5),
        ("kcoh5@30 K=1", kcoh(5, 30), 1, 3, 53.2, 0.2),
    ]
    for name, lats, k, pd, pub, tol in targets:
        c = cell(lats, pd, K=k)
        m = abs(c["m"] - pub) <= tol
        ok &= m
        print(f"  {name:<16} got {c['m']:5.1f}  pub {pub:5.1f}  "
              f"{'OK' if m else 'DRIFT'}")
    print("  CANARIES:", "PASS" if ok else "FAIL")
    return ok


# ---------------------------------------------------------------- EXP 1
def exp1():
    print("\n== EXP 1: pd x N sweep, UNCOMPENSATED (ladder spread-30, delta=12,"
          " K=1) ==")
    print("   cell = true12% ; D = diverged (all 5 seeds maxResid > 10^6)")
    ns = sorted(set(NGRID) | {2 * p + 1 for p in PDS})
    tab = {}
    print("  pd | " + " | ".join(f"N={n:<4}" for n in ns) + "| meanMult@2pd+1")
    for pd in PDS:
        row = []
        mmnote = ""
        for n in ns:
            if n > 25:
                continue
            c = cell(ladder(30, n), pd)
            tab[(pd, n)] = c
            row.append(show(c))
            if n == 2 * pd + 1:
                mmnote = f"{c['mm'] / 10:.1f}/{n}"
        print(f"  {pd:>2} | " + " | ".join(f"{x:<6}" for x in row) + f" | {mmnote}")
    print("\n  wall edge location (smallest diverged N; expected 2pd+1):")
    allpass = True
    for pd in PDS:
        edge = next((n for n in ns if n <= 25 and tab[(pd, n)]["div"]), None)
        exp = 2 * pd + 1
        good = edge == exp
        allpass &= good
        e2pd = tab[(pd, 2 * pd)]["m"]
        e2pd1 = tab[(pd, 2 * pd + 1)]["m"]
        print(f"   pd={pd:>2}: edge={edge}  expected={exp}  "
              f"{'MATCH' if good else 'MISMATCH'}"
              f"   [N=2pd: {e2pd:.1f}%  N=2pd+1: {e2pd1:.1f}%]"
              f"  maxResid@2pd+1 ~ 10^{len(str(cap(tab[(pd, 2*pd+1)]['mr'][0]))) - 1}")
    print(f"  P2 (wall tracks N=2pd+1 exactly): "
          f"{'PASS' if allpass else 'FAIL'}")
    # lats transparency for edge cells
    for pd in (1, 2, 3):
        for n in (2 * pd, 2 * pd + 1):
            print(f"   lats pd={pd} N={n}: {ladder(30, n)}")
    e6 = tab[(6, 7)]["m"]
    print(f"\n  >>> P1b INSTANTIATION (before EXP 2): E6 = uncomp step5/N=7 @pd=6"
          f" true12 = {e6:.1f}%  ->  band [{e6 - 8:.1f}, {e6 + 8:.1f}] <<<")
    return tab, e6


# ---------------------------------------------------------------- EXP 2
def exp2(e6):
    print("\n== EXP 2a: compensated pd x N grids — where did the wall go? ==")
    ns = sorted(set(NGRID) | {2 * p + 1 for p in PDS} | {9, 18, 19, 20})
    ns = [n for n in ns if n <= 25]
    tabs = {}
    for mc, tag in ((1, "MC-A (//min(n_f,pd))"), (2, "MC-B (//n_f)")):
        tab = {}
        print(f"\n  --- {tag} ---")
        print("  pd | " + " | ".join(f"N={n:<4}" for n in ns))
        for pd in PDS:
            row = []
            for n in ns:
                c = cell(ladder(30, n), pd, mc=mc)
                tab[(pd, n)] = c
                row.append(show(c))
            print(f"  {pd:>2} | " + " | ".join(f"{x:<6}" for x in row))
        tabs[mc] = tab
        print("  edges (smallest diverged N):")
        for pd in PDS:
            edge = next((n for n in ns if tab[(pd, n)]["div"]), None)
            pred = {1: 3, 2: 9, 3: 19}.get(pd, None)
            print(f"   pd={pd:>2}: edge={edge}   P3 pred="
                  f"{pred if pred else 'none<=25'}"
                  f"   {'MATCH' if edge == pred else ('MISMATCH' if pred else '')}")
        if mc == 1:
            nb = sum(1 for pd in PDS for n in ns if tab[(pd, n)]["div"])
            print(f"  P3a/P3b MC-A: diverged cells = {nb}; pd=1 immunity proven"
                  f" byte-level by CANARY A2 (structural)")
        else:
            nb = sum(1 for pd in PDS for n in ns if tab[(pd, n)]["div"])
            print(f"  P3c MC-B: diverged cells in whole grid = {nb} "
                  f"(predicted 0) -> {'PASS' if nb == 0 else 'FAIL'}")

    print("\n== EXP 2b: rescue detail at pd=3, delta=12, K=1 (true12%) ==")
    print(f"  {'step':>4} {'N':>3} | {'uncomp':>7} {'MC-A':>7} {'MC-B':>7} |"
          f" {'rescueA':>8} {'rescueB':>8}")
    base = {}
    for g in STEPS:
        lats = ladder_step(30, g)
        u = cell(lats, 3)["m"]
        a = cell(lats, 3, mc=1)["m"]
        b = cell(lats, 3, mc=2)["m"]
        base[g] = (u, a, b)
        print(f"  {g:>4} {len(lats):>3} | {u:>7.1f} {a:>7.1f} {b:>7.1f} |"
              f" {a - u:>+8.1f} {b - u:>+8.1f}")
    u5, a5, b5 = base[5]
    print(f"\n  HEADLINE rescue step5/N=7: {u5:.1f}% -> MC-A {a5:.1f}% "
          f"(x{a5 / max(u5, 0.1):.0f}), MC-B {b5:.1f}% (x{b5 / max(u5, 0.1):.0f})")
    print(f"  P1a absolute [12,32]: MC-A {'PASS' if 12 <= a5 <= 32 else 'FAIL'}"
          f"  MC-B {b5:.1f}")
    print(f"  P1b relative [E6-8, E6+8] = [{e6 - 8:.1f}, {e6 + 8:.1f}]:"
          f" MC-A {'PASS' if e6 - 8 <= a5 <= e6 + 8 else 'FAIL'}"
          f"  MC-B {'PASS' if e6 - 8 <= b5 <= e6 + 8 else 'FAIL'}")

    print("\n== EXP 2c: pathology audit, coarse grammars @30 pd=3 K=1 ==")
    print(f"  {'grammar':>8} | {'uncomp':>7} {'best':>7} | {'events':>13} "
          f"{'cancels':>14} {'maxResid':>19}")
    best = 2 if base[5][2] > base[5][1] else 1
    print(f"  best-comp variant for EXP 3: {'MC-B' if best == 2 else 'MC-A'}")
    for name, lats in (("kcoh5", kcoh(5, 30)), ("kcoh1", kcoh(1, 30)),
                       ("ladder", ladder(30)), ("cohort", [0, 0, 0, 30, 30, 30])):
        u = cell(lats, 3)
        c = cell(lats, 3, mc=best)
        print(f"  {name:>8} | {u['m']:>7.1f} {c['m']:>7.1f} |"
              f" {mean([r['events'] for r in u['rs']]):>6.0f}/"
              f"{mean([r['events'] for r in c['rs']]):<6.0f}"
              f" {mean([r['cancels'] for r in u['rs']]):>7.0f}/"
              f"{mean([r['cancels'] for r in c['rs']]):<7.0f}"
              f" {cap(max(u['mr'])):>9}/{cap(max(c['mr'])):<9}")
    return best, base


# ---------------------------------------------------------------- EXP 3
def exp3(best):
    tag = "MC-B" if best == 2 else "MC-A"
    print(f"\n== EXP 3: joint map, {tag} vs uncomp x delta {{12,24}} x K {{1,2,4}}"
          f" (true12 pinned EV=12; native in parens for delta=24) ==")
    grammars = [("kcoh5", kcoh(5, 30)), ("kcoh1", kcoh(1, 30)),
                ("ladder", ladder(30)), ("cohort", [0, 0, 0, 30, 30, 30]),
                ("step5", ladder_step(30, 5))]
    tab = {}
    for d in (12, 24):
        print(f"\n  --- delta={d} ---")
        print(f"  {'grammar':>8} {'comp':>5} | {'K=1':>12} {'K=2':>12} {'K=4':>12}")
        for name, lats in grammars:
            for mc in (0, best):
                vals = []
                for k in (1, 2, 4):
                    c = cell(lats, 3, K=k, delta=d, mc=mc)
                    nat = mean([within_pm(r["resid"], d) for r in c["rs"]]) / 10
                    tab[(name, d, mc, k)] = (c["m"], nat)
                    vals.append((c["m"], nat))
                lbl = tag if mc else "off"
                print(f"  {name:>8} {lbl:>5} | "
                      + " ".join(f"{v[0]:>5.1f}({v[1]:>5.1f})" for v in vals))
    print("\n  K=2 trough check (K2 < min(K1,K4)) at delta=12:")
    hits = 0
    for name, _ in grammars[:4]:
        off = [tab[(name, 12, 0, k)][0] for k in (1, 2, 4)]
        on = [tab[(name, 12, best, k)][0] for k in (1, 2, 4)]
        t_off = off[1] < min(off[0], off[2])
        t_on = on[1] < min(on[0], on[2])
        hits += t_on
        print(f"   {name:>8}: off {t_off}  comp {t_on}   "
              f"off[{off[0]:.1f},{off[1]:.1f},{off[2]:.1f}] "
              f"comp[{on[0]:.1f},{on[1]:.1f},{on[2]:.1f}]")
    print(f"  P4 (trough persists under comp for >=3/4): "
          f"{'PASS' if hits >= 3 else 'FAIL'} ({hits}/4)")
    print("\n  comp x K interaction (K4-K1 sign, delta=12):")
    for name, _ in grammars:
        s_off = tab[(name, 12, 0, 4)][0] - tab[(name, 12, 0, 1)][0]
        s_on = tab[(name, 12, best, 4)][0] - tab[(name, 12, best, 1)][0]
        print(f"   {name:>8}: off {s_off:+6.1f}  comp {s_on:+6.1f}  "
              f"{'FLIP' if s_off * s_on < 0 else 'same sign'}")
    return tab


# ---------------------------------------------------------------- EXP 4
def run_fabric_hetero(mode, ticks, lats, pds, lies=None, K=4, delta=12,
                      drift=6, seed=20260902):
    """Interference arm of exp_glm1.run_fabric with PER-SENSOR pd.
    Byte-identical to run_fabric_mc(mc=0) when pds is uniform (Canary D)."""
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    n = len(lats)
    lies = lies or {}
    emissions = []
    events = mass = cancels = chatter = settles = 0
    last = -10
    resid = []
    cflags = []
    for t in range(ticks):
        reads = [reality(max(0, t - lats[i])) + (lies[i](t) if i in lies else 0)
                 for i in range(n)]
        s_true = reality(t)
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > delta]
        cflag = 0
        if mode == "sequential":
            if trig:
                i, e = trig[0]
                g += e
                events += 1
                mass += abs(e)
                emissions.append((t, i, e, e))
                if t - last == 1:
                    chatter += 1
                last = t
        else:
            for i, e in trig:
                m = abs(e) // pds[i] or 1
                pm = m if e > 0 else -m
                pulses.appendleft([pm, K])
                events += 1
                mass += abs(e)
                emissions.append((t, i, pm, e))
            if pulses:
                net = sum(p[0] for p in pulses)
                if net == 0 and any(p[0] > 0 for p in pulses) \
                        and any(p[0] < 0 for p in pulses):
                    cancels += 1
                    cflag = 1
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
            if trig:
                if t - last == 1:
                    chatter += 1
                last = t
        resid.append(abs(s_true - g))
        cflags.append(cflag)
        if all(abs(r - g) <= delta for r in reads):
            settles += 1
    return dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
                settles=settles, resid=resid, cflags=cflags,
                emissions=emissions, audit=None, ticks=ticks)


def hcell(lats, pds, K=1, delta=DELTA, seeds=SEEDS):
    rs = [run_fabric_hetero("interference", TICKS, lats, pds, K=K,
                            delta=delta, drift=6, seed=s) for s in seeds]
    mr = [max(r["resid"]) for r in rs]
    t12 = [within_pm(r["resid"], EV) for r in rs]
    return dict(t12=t12, m=mean(t12) / 10, mr=mr,
                div=all(x > DIV_AT for x in mr))


def canary_d():
    print("\n== CANARY D: hetero runner uniform-pd == mc=0 byte-identity ==")
    ok = True
    for lats, pd in ((ladder(30), 3), (ladder(30, 9), 2),
                     (ladder_step(30, 5), 6), (kcoh(5, 30), 12)):
        pds = [pd] * len(lats)
        a = run_fabric_mc("interference", TICKS, lats, K=1, pd=pd, delta=DELTA,
                          drift=6, seed=SEEDS[0], mc=0)
        b = run_fabric_hetero("interference", TICKS, lats, pds, K=1,
                              delta=DELTA, drift=6, seed=SEEDS[0])
        if a != b:
            ok = False
            print(f"  MISMATCH lats={lats[:8]} pd={pd}")
    print(f"  {'PASS' if ok else 'FAIL'}: 4 configs full-dict identical")
    return ok


def exp4():
    print("\n== EXP 4: mixed-pd adjudication — is O2b's EVEN wall N=6 an"
          " effective-pd effect? ==")
    print("   (pre-registered as P5a/P5b in this file's docstring BEFORE"
          " this run)")
    ns = (4, 5, 6, 7, 8, 9, 13)
    print("  mix   | " + " | ".join(f"N={n:<4}" for n in ns) + "| edge")
    edges = {}
    for mix in ((2, 3), (3, 6)):
        row = []
        for n in ns:
            lats = ladder(30, n)
            pds = [mix[i % 2] for i in range(n)]   # alternate by sensor idx
            c = hcell(lats, pds)
            row.append(show(c))
        edge = next((n for n in ns if hcell(ladder(30, n),
                                            [mix[i % 2]
                                             for i in range(n)]).get("div")),
                    None)
        edges[mix] = edge
        print(f"  {str(mix):>5} | " + " | ".join(f"{x:<6}" for x in row)
              + f"| {edge}")
    e23, e36 = edges[(2, 3)], edges[(3, 6)]
    print(f"\n  P5a mix(2,3): edge={e23} — "
          + ("weakest-member law (REGISTERED primary): O2b's N=6 stays a"
             " separate law" if e23 == 5 else
             "DEVIATION from registered primary — see P5a alternatives"))
    print(f"  P5b mix(3,6): edge={e36} — "
          + ("weakest-member law (REGISTERED primary): no even-wall"
             " unification" if e36 == 7 else
             ("EVEN WALL at 6 -> effective-pd unification with O2b;"
              " room-pressure mapping gets its predictive anchor"
              if e36 == 6 else
              "mixture protection / sub-linear composition (registered"
              " alternative)")))
    return edges


def main():
    print("SPIN 11 — PULSE-DIAL / MASS-COMPENSATION  (pre-registrations in"
          " spin11_pulse_dial.py docstring, committed before any run;\n"
          " ALL predictions pinned to eval window EV=12)")
    if not canaries():
        print("CANARY FAIL — aborting")
        sys.exit(1)
    _, e6 = exp1()
    best, _ = exp2(e6)
    exp3(best)
    if not canary_d():
        print("CANARY D FAIL — EXP 4 aborted")
    else:
        exp4()
    x = 486256185   # current ledger head (after SPIN-12-conservation pick)
    x2 = (1103515245 * x + 12345) & 0x7FFFFFFF
    print(f"\nLCG ritual: proposal-dispatched spin (SPIN-8's proposal) — no pick"
          f" consumed; ledger head 486256185; next selection reference:"
          f" 486256185 -> {x2} -> mod 10 = {x2 % 10}")


if __name__ == "__main__":
    main()
