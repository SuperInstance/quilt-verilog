#!/usr/bin/env python3
"""SPIN dequant-2 — three §10 cheat-code probes on the E1 interference tick.

Spoke 8 (DEQUANT) of the Wheel of Discovery. Casey directive 2026-09-02
22:18: "keep going on our post-quantum work."

Probes:
  1. INTERFERENCE-AS-GROVER-CURVE — is the interference mode "amplitude
     amplification of the correct reset direction"? Measure the per-tick
     pulse velocity toward truth vs the sequential snap, the velocity ramp
     as pulses stack, ticks-to-deadband scaling vs sqrt/linear/log models,
     and book exactly where the analogy breaks.
  2. THE THERMODYNAMIC ARM — sample the reset from the pulse ensemble
     (weighted by |pulse|) instead of summing it: cold=sum, warm=weighted
     sample, hot=uniform sample. Does warm beat cold and sequential
     anywhere, on settles or settles-per-debt?
  3. SNAP-POINT RE-AIM AS SEARCH — the (pulse_div, K) grid as an
     oracle-free integer search: exhaustive vs slide search vs short-probe
     sample access vs closed-form zero-query prediction.

Integer-only: no floats in any instrument loop. Percentages are per-mille
integers. Fixed seeds (1, 7, 42, 1999, 20260902). The vanilla port is
validated against e1.run counters byte-identically before any arm runs.

Usage: python3 spin_dequant2.py [validate|exp1|exp2|exp3|all]
"""
import os
import sys
from collections import deque
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import e1  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
RT = [e1.reality(t) for t in range(e1.PERIOD)]  # reality() is pure in t%240

DEFAULTS = dict(ticks=4800, K=8, pulse_div=3, delta=6, drift=3, lat2=5)
STRESS = dict(ticks=4800, K=4, pulse_div=3, delta=12, drift=6, lat2=10)
DEEP = dict(ticks=4800, K=6, pulse_div=3, delta=16, drift=8, lat2=16)


def pm(n, d):
    """per-mille, integer floor."""
    return n * 1000 // max(1, d)


# ----------------------------------------------------------------------------
# Core port of e1.run with instrumentation hooks. apply="sum" reproduces
# e1.py exactly (validated). apply="warm"/"hot" sample the applied reset
# from the pre-decay pulse snapshot instead of summing it.
# ----------------------------------------------------------------------------
def run_fab(mode, seed, ticks=4800, K=8, pulse_div=3, delta=6, drift=3, lat2=5,
            apply="sum", twins=2, prog=None, streaks=None, etrig=None):
    rng = e1.LCG(seed)
    samp = e1.LCG(seed + 1)  # separate stream: drift sequence identical to cold
    g = e1.reality(0)
    pulses = deque()
    snap_events = 0
    ledger_mass = 0
    constructive = 0
    cancellations = 0
    chatter = 0
    last_snap = -10
    max_err = 0
    settles = 0
    stalls = 0          # cold only: trig fired but net==0 (coherence deadlock)
    applied_mass = 0
    live_len_sum = 0
    live_ticks = 0
    solo_frac = 0       # application ticks with exactly 1 live pulse
    run_len = 0

    for t in range(ticks):
        s1 = RT[t % 240]
        s2 = RT[(t - lat2 if t >= lat2 else 0) % 240]
        g += rng.below(2 * drift + 1) - drift

        while pulses and pulses[-1][1] == 0:
            pulses.pop()

        e1v = s1 - g
        e2v = s2 - g
        trig = []
        if abs(e1v) > delta:
            trig.append(e1v)
        if twins == 2 and abs(e2v) > delta:
            trig.append(e2v)
        max_trig = 0
        for e in trig:
            if abs(e) > max_trig:
                max_trig = abs(e)

        if not trig:
            run_len = 0

        if mode == "sequential":
            if trig:
                a = trig[0]
                src = 0 if trig[0] is e1v else 1
                s = 1 if e1v > 0 else (-1 if e1v < 0 else 0)
                if s != 0:
                    if prog is not None:
                        prog.append((a * s, abs(a), src))
                    if streaks is not None and run_len < len(streaks):
                        streaks[run_len][0] += a * s * 1000 // abs(e1v)
                        streaks[run_len][1] += 1
                g += a
                snap_events += 1
                ledger_mass += abs(a)
                applied_mass += abs(a)
                run_len += 1
                if t - last_snap == 1:
                    chatter += 1
                last_snap = t
                if max(abs(s1 - g), abs(s2 - g)) > max_trig:
                    constructive += 1
        else:
            for e in trig:
                m = abs(e) // pulse_div or 1
                pulses.appendleft([m if e > 0 else -m, K])
                snap_events += 1
                ledger_mass += abs(e)
                if etrig is not None:
                    etrig.append(abs(e))
            if pulses:
                net = 0
                for p in pulses:
                    net += p[0]
                if net == 0 and len(pulses) >= 2:
                    cancellations += 1
                if apply == "sum":
                    applied = net
                    if trig and net == 0:
                        stalls += 1
                elif apply == "warm":
                    tot = 0
                    for p in pulses:
                        tot += abs(p[0])
                    r = (samp.next() >> 11) % tot  # bit 11: dodge period-2 low bit
                    acc = 0
                    applied = pulses[-1][0]
                    for p in pulses:
                        acc += abs(p[0])
                        if r < acc:
                            applied = p[0]
                            break
                else:  # hot
                    r = (samp.next() >> 11) % len(pulses)
                    applied = pulses[r][0]
                live_len_sum += len(pulses)
                live_ticks += 1
                if len(pulses) == 1:
                    solo_frac += 1
                g += applied
                applied_mass += abs(applied)
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)
                        decayed.append([mag, life - 1])
                pulses = decayed
                if trig:
                    s = 1 if e1v > 0 else (-1 if e1v < 0 else 0)
                    if s != 0:
                        if prog is not None:
                            prog.append((applied * s, abs(applied), 2))
                        if streaks is not None and run_len < len(streaks):
                            streaks[run_len][0] += applied * s * 1000 // abs(e1v)
                            streaks[run_len][1] += 1
                    run_len += 1
                    if max(abs(s1 - g), abs(s2 - g)) > max_trig:
                        constructive += 1
                    if t - last_snap == 1:
                        chatter += 1
                    last_snap = t

        err = max(abs(s1 - g), abs(s2 - g)) if twins == 2 else abs(s1 - g)
        if err > max_err:
            max_err = err
        if abs(s1 - g) <= delta and (twins == 1 or abs(s2 - g) <= delta):
            settles += 1

    return dict(mode=mode, apply=apply, snap_events=snap_events,
                ledger_mass=ledger_mass, constructive=constructive,
                cancellations=cancellations, chatter=chatter, max_err=max_err,
                settles=settles, pm=pm(settles, ticks), stalls=stalls,
                applied_mass=applied_mass,
                mean_live=live_len_sum * 1000 // max(1, live_ticks),
                solo_pm=pm(solo_frac, live_ticks))


# ----------------------------------------------------------------------------
# Validation: run_fab(mode, apply="sum") must reproduce e1.run counters.
# ----------------------------------------------------------------------------
def validate():
    ok = True
    for name, cfg in (("default", DEFAULTS), ("stress", STRESS)):
        for mode in ("sequential", "interference"):
            for s in SEEDS:
                e1.SEED = s
                ref = e1.run(mode, **{k: v for k, v in cfg.items() if k != "ticks"})
                mine = run_fab(mode, s, **cfg)
                for k in ("snap_events", "ledger_mass", "constructive",
                          "cancellations", "chatter", "max_err"):
                    if ref[k] != mine[k]:
                        print(f"MISMATCH {name} {mode} seed {s} {k}: "
                              f"{ref[k]} vs {mine[k]}")
                        ok = False
                # settles via the only float e1.run exposes (display rounding)
                if round(100 * mine["settles"] / cfg["ticks"], 1) != ref["pct_within"]:
                    print(f"MISMATCH {name} {mode} seed {s} settles: "
                          f"{ref['pct_within']} vs {mine['settles']}")
                    ok = False
    print("VALIDATE:", "PASS — all counters byte-identical to e1.run"
          if ok else "FAIL")
    return ok


# ----------------------------------------------------------------------------
# EXP 1a — displacement response: ticks-to-deadband scaling.
# Single twin (T1 only), g displaced by +E0 at t0, drift as specified.
# Arms: seq (snap), int (interference), scan (unit deadband-step null).
# ----------------------------------------------------------------------------
def run_disp(arm, E0, delta=12, drift=3, K=8, pulse_div=3, t0=240, seed=1,
             TMAX=600):
    rng = e1.LCG(seed)
    g = RT[t0 % 240] + E0
    pulses = deque()
    events = 0
    debt = 0
    flips = 0
    applied = 0
    profile = []   # (j, e_pre, net) for interference
    prev_sign = -1
    settle = -1
    for j in range(TMAX):
        t = t0 + j
        s1 = RT[t % 240]
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        e = s1 - g
        if abs(e) <= delta:
            settle = j
            break
        if arm == "scan":
            a = delta if e > 0 else -delta
            g += a
            events += 1
            debt += delta
            applied += delta
        elif arm == "seq":
            g += e
            events += 1
            debt += abs(e)
            applied += abs(e)
        else:
            m = abs(e) // pulse_div or 1
            pulses.appendleft([m if e > 0 else -m, K])
            events += 1
            debt += abs(e)
            net = 0
            for p in pulses:
                net += p[0]
            profile.append((j, e, net))
            g += net
            applied += abs(net)
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
        sg = 1 if e > 0 else -1
        if j > 0 and sg != prev_sign:
            flips += 1  # overshot THROUGH the deadband to the other side
        prev_sign = sg
    return dict(arm=arm, E0=E0, settle=settle, events=events, debt=debt,
                flips=flips, applied=applied, profile=profile)


def exp1a():
    delta = 12
    print("=" * 78)
    print("EXP 1a — DISPLACEMENT RESPONSE (single twin, delta=%d)" % delta)
    print("=" * 78)
    E0s = (24, 48, 96, 192, 384, 768, 1536, 3072)
    for drift in (3, 6):
        print(f"\n-- drift={drift}, K=8, pulse_div=3, 5 seeds --")
        print(f"{'E0':>6}{'N=E0/d':>8}{'T_seq':>7}{'T_scan':>8}{'T_int(sds)':>16}"
              f"{'T_grover':>9}{'flips':>7}{'deliv':>7}{'evts':>6}")
        for E0 in E0s:
            N = E0 // delta
            tg = (78539 * isqrt(max(1, N))) // 100000 + 1
            ts = []
            fl = 0
            ap = 0
            ev = 0
            for s in SEEDS:
                r = run_disp("int", E0, delta=delta, drift=drift, seed=s)
                ts.append(r["settle"])
                fl += r["flips"]
                ap += r["applied"]
                ev += r["events"]
            rsc = [run_disp("scan", E0, delta=delta, drift=drift, seed=s)["settle"]
                   for s in SEEDS]
            tscan = sum(rsc) // len(rsc)
            print(f"{E0:>6}{N:>8}{1:>7}{tscan:>8}"
                  f"{str(ts):>16}{tg:>9}{fl:>7}"
                  f"{ap * 1000 // (5 * E0):>7}{ev // 5:>6}")
    # velocity ramp: net as fraction of CURRENT error, by tick since displacement
    print("\n-- interference velocity ramp (drift=3): net/current-|e| per-mille,")
    print("   mean over 5 seeds x E0 in {192,384,768,1536,3072}, by tick j --")
    acc = {}
    for E0 in (192, 384, 768, 1536, 3072):
        for s in SEEDS:
            r = run_disp("int", E0, delta=delta, drift=3, seed=s)
            for (j, e, net) in r["profile"]:
                if abs(e) > delta:
                    acc.setdefault(j, [0, 0])
                    acc[j][0] += abs(net) * 1000 // abs(e)
                    acc[j][1] += 1
    js = sorted(acc)[:10]
    print(f"{'j':>4}{'f_j (permille)':>16}{'n':>7}{'net/E0 (permille)':>19}")
    for E0 in (384,):
        accE = {}
        for s in SEEDS:
            r = run_disp("int", E0, delta=delta, drift=3, seed=s)
            for (j, e, net) in r["profile"]:
                if abs(e) > delta:
                    accE.setdefault(j, [0, 0])
                    accE[j][0] += abs(net) * 1000 // E0
                    accE[j][1] += 1
    for j in js:
        if j in accE and accE[j][1] >= 3:
            print(f"{j:>4}{acc[j][0] // acc[j][1]:>16}{acc[j][1]:>7}"
                  f"{accE[j][0] // accE[j][1]:>19}")


# ----------------------------------------------------------------------------
# EXP 1b — closed-loop conflict harness: streak velocity ramp + progress
# toward CURRENT truth per event (the "amplification of the correct reset
# direction" test), stress and default regimes.
# ----------------------------------------------------------------------------
def exp1b():
    print("\n" + "=" * 78)
    print("EXP 1b — CONFLICT-HARNESS DIRECTION AMPLIFICATION")
    print("=" * 78)
    for name, cfg in (("default", DEFAULTS), ("stress", STRESS)):
        print(f"\n-- {name} regime --")
        for mode in ("sequential", "interference"):
            P = [0, 0]            # [sum a*s (directed), sum |a|]
            neg = 0
            nev = 0
            by_src = {0: [0, 0, 0], 1: [0, 0, 0]}  # src -> [directed, mass, neg]
            streaks = [[0, 0] for _ in range(8)]
            for s in SEEDS:
                prog = []
                run_fab(mode, s, **cfg, prog=prog, streaks=streaks)
                for (ds, mass, src) in prog:
                    P[0] += ds
                    P[1] += mass
                    nev += 1
                    if ds < 0:
                        neg += 1
                    if src in by_src and mode == "sequential":
                        by_src[src][0] += ds
                        by_src[src][1] += mass
                        if ds < 0:
                            by_src[src][2] += 1
            label = mode[:4]
            print(f"{label:>5}: directed-mass ratio {pm(P[0], P[1]):>5} permille "
                  f"(neg-events {pm(neg, nev):>4}, n={nev})")
            if mode == "sequential":
                for src, lab in ((0, "  T1-snap"), (1, "  T2-snap")):
                    d, m, ng = by_src[src]
                    if m:
                        print(f"{lab}: directed {pm(d, m):>5} permille, "
                              f"neg {pm(ng, max(1, m // 30)):>4} (approx-event)")
            else:
                row = []
                for j, (sv, n) in enumerate(streaks):
                    row.append(f"j{j}:{sv // n if n else '-'}({n})")
                print("  int streak velocity v_j (permille of current err):",
                      " ".join(row))
                sq = []
                for s in SEEDS:
                    st = [[0, 0] for _ in range(8)]
                    run_fab("sequential", s, **cfg, streaks=st)
                    for j, (sv, n) in enumerate(st):
                        if n:
                            sq.append(f"j{j}:{sv // n}({n})")
                print("  seq streak velocity v_j:", " ".join(sq[:6]))


# ----------------------------------------------------------------------------
# EXP 2 — thermodynamic arm.
# ----------------------------------------------------------------------------
def exp2():
    print("\n" + "=" * 78)
    print("EXP 2 — THERMODYNAMIC ARM (cold=sum, warm=|pulse|-weighted sample,")
    print("        hot=uniform pulse sample; sampling stream = LCG(seed+1), bit 11)")
    print("=" * 78)
    for name, cfg in (("default", DEFAULTS), ("stress", STRESS), ("deep-conflict", DEEP)):
        print(f"\n-- {name}: {cfg['delta']=} {cfg['drift']=} K={cfg['K']} "
              f"lat2={cfg['lat2']} --")
        print(f"{'arm':>11}{'events':>8}{'debt':>8}{'pm':>6}{'maxE':>6}"
              f"{'canc':>6}{'chat':>6}{'stall':>6}{'eff(pm/Md)':>12}"
              f"{'live':>7}{'solo':>6}")
        agg = {}
        for arm in ("sequential", "cold", "warm", "hot"):
            tot = dict(ev=0, debt=0, st=0, canc=0, chat=0, mx=0, stall=0,
                       live=0, solo=0)
            for s in SEEDS:
                if arm == "sequential":
                    r = run_fab("sequential", s, **cfg)
                else:
                    r = run_fab("interference", s, **cfg,
                                apply={"cold": "sum", "warm": "warm",
                                       "hot": "hot"}[arm])
                tot["ev"] += r["snap_events"]
                tot["debt"] += r["ledger_mass"]
                tot["st"] += r["settles"]
                tot["canc"] += r["cancellations"]
                tot["chat"] += r["chatter"]
                tot["mx"] = max(tot["mx"], r["max_err"])
                tot["stall"] += r["stalls"]
                tot["live"] += r["mean_live"]
                tot["solo"] += r["solo_pm"]
            n = len(SEEDS)
            eff = tot["st"] * 1_000_000 // max(1, tot["debt"])
            agg[arm] = (tot, eff)
            print(f"{arm:>11}{tot['ev'] // n:>8}{tot['debt'] // n:>8}"
                  f"{pm(tot['st'], n * cfg['ticks']):>6}{tot['mx']:>6}"
                  f"{tot['canc'] // n:>6}{tot['chat'] // n:>6}"
                  f"{tot['stall'] // n:>6}{eff:>12}{tot['live'] // n:>7}"
                  f"{tot['solo'] // n:>6}")
        # verdict line
        c, w, h, q = agg["cold"], agg["warm"], agg["hot"], agg["sequential"]
        wpw = w[0]["st"] > c[0]["st"]
        wew = w[1] > c[1]
        print(f"  warm>cold settles? {'YES' if wpw else 'no'}   "
              f"warm>cold eff? {'YES' if wew else 'no'}   "
              f"warm>seq settles? {'YES' if w[0]['st'] > q[0]['st'] else 'no'}")


# ----------------------------------------------------------------------------
# EXP 3 — snap-point grid as search.
# ----------------------------------------------------------------------------
def delivered(m, sign, K):
    """Total motion one pulse of magnitude m (signed) delivers over K ticks
    under the pinned floor decay (mag - mag//2, floor at +-1)."""
    v = m * sign
    tot = 0
    for _ in range(K):
        tot += v
        if abs(v) > 1:
            v = v - (v // 2)
    return tot


def slide(grid, i0, j0, probe_cost, full_cost):
    """Steepest-ascent coordinate slide; counts cached cell evaluations."""
    H, W = len(grid), len(grid[0])
    cache = set()
    i, j = i0, j0

    def ev(ni, nj):
        cache.add((ni, nj))
        return grid[ni][nj]

    while True:
        bv = ev(i, j)
        best = (i, j)
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W:
                v = ev(ni, nj)
                if v > bv:
                    bv = v
                    best = (ni, nj)
        if best == (i, j):
            return (i, j, bv, len(cache))
        i, j = best


def exp3():
    print("\n" + "=" * 78)
    print("EXP 3 — SNAP-POINT RE-AIM AS SEARCH over (pulse_div, K)")
    print("=" * 78)
    DIVS = list(range(1, 9))
    KS = list(range(1, 13))
    etrig_stress = []
    etrig_default = []
    for s in SEEDS:
        run_fab("interference", s, **STRESS, etrig=etrig_stress)
        run_fab("interference", s, **DEFAULTS, etrig=etrig_default)
    for name, cfg, etr in (("stress", STRESS, etrig_stress),
                           ("default", DEFAULTS, etrig_default)):
        Etyp = sum(etr) // len(etr)
        grid = []
        gridS = []
        for d in DIVS:
            row = []
            rowS = []
            for Kk in KS:
                st = 0
                stS = 0
                for s in SEEDS:
                    r = run_fab("interference", s, ticks=4800, K=Kk,
                                pulse_div=d, delta=cfg["delta"],
                                drift=cfg["drift"], lat2=cfg["lat2"])
                    st += r["settles"]
                    stS += run_fab("interference", s, ticks=600, K=Kk,
                                   pulse_div=d, delta=cfg["delta"],
                                   drift=cfg["drift"], lat2=cfg["lat2"])["settles"]
                row.append(pm(st, 5 * 4800))
                rowS.append(pm(stS, 5 * 600))
            grid.append(row)
            gridS.append(rowS)
        H, W = len(grid), len(grid[0])
        # global best
        bi, bj, bv = 0, 0, grid[0][0]
        for i in range(H):
            for j in range(W):
                if grid[i][j] > bv:
                    bv, bi, bj = grid[i][j], i, j
        print(f"\n-- {name}: E_typ(mean|trig e|)={Etyp}  "
              f"grid best: div={DIVS[bi]} K={KS[bj]} pm={bv} --")
        # local optima (strict, 4-neighbor)
        lopt = 0
        for i in range(H):
            for j in range(W):
                v = grid[i][j]
                nb = True
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] >= v:
                        nb = False
                        break
                if nb and (i, j) != (bi, bj):
                    lopt += 1
        # adjacent-pair concordance of the short probe vs the full run
        conc_pairs = 0
        all_pairs = 0
        for i in range(H):
            for j in range(W):
                for jj in range(j + 1, W):
                    all_pairs += 1
                    if (grid[i][j] > grid[i][jj]) == (gridS[i][j] > gridS[i][jj]) \
                       or grid[i][j] == grid[i][jj] and gridS[i][j] == gridS[i][jj]:
                        conc_pairs += 1
        # short-probe argmax
        si, sj, sv = 0, 0, gridS[0][0]
        for i in range(H):
            for j in range(W):
                if gridS[i][j] > sv:
                    sv, si, sj = gridS[i][j], i, j
        print(f"local optima (strict, excl. global): {lopt}; "
              f"probe(600t) vs full(4800t) pair concordance: "
              f"{pm(conc_pairs, all_pairs)} permille over {all_pairs} pairs")
        print(f"probe argmax: div={DIVS[si]} K={KS[sj]} pm600={sv} "
              f"(full pm there: {grid[si][sj]})")
        # slide searches on full grid
        exhaustive = H * W
        starts = [(0, 0), (H - 1, 0), (0, W - 1), (H - 1, W - 1),
                  (H // 2, W // 2), (2, 7)]  # last = e1 default div3 K8
        print("slide (steepest ascent, full-grid evaluations):")
        for (i0, j0) in starts:
            i, j, v, evs = slide(grid, i0, j0, 0, 0)
            print(f"  start(div={DIVS[i0]},K={KS[j0]}): seat div={DIVS[i]} "
                  f"K={KS[j]} pm={v} evals={evs}/{exhaustive} "
                  f"({'GLOBAL' if (i, j) == (bi, bj) else 'local'})")
        # slide on probes, then confirm
        print("slide using 600-tick probes + one full confirm:")
        for (i0, j0) in starts:
            i, j, v, evs = slide(gridS, i0, j0, 0, 0)
            cost = evs * 5 * 600 + 5 * 4800
            full = exhaustive * 5 * 4800
            print(f"  start(div={DIVS[i0]},K={KS[j0]}): seat div={DIVS[i]} "
                  f"K={KS[j]} probe-pm={v} full-pm={grid[i][j]} "
                  f"cost={cost} ({pm(cost, full)} permille of exhaustive)")
        # closed-form zero-query prediction
        print(f"delivered(m) table (sign +, K=8): m=1..12 ->",
              [delivered(m, 1, 8) for m in range(1, 13)])
        print(f"  sign asymmetry check (m=9, K=8): +{delivered(9, 1, 8)} "
              f"vs {delivered(9, -1, 8)}")
        # no-overshoot predictor: smallest div with delivered(E//div,K) <= E+delta
        delta = cfg["delta"]
        pred = None
        for d in DIVS:
            m = max(1, Etyp // d)
            if delivered(m, 1, cfg["K"]) <= Etyp + delta:
                pred = d
                break
        print(f"  zero-query no-overshoot prediction (E_typ={Etyp}, "
              f"K={cfg['K']}, delta={delta}): div*={pred} vs grid div*={DIVS[bi]}")


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("validate", "all"):
        if not validate():
            sys.exit(1)
    if what in ("exp1", "all"):
        exp1a()
        exp1b()
    if what in ("exp2", "all"):
        exp2()
    if what in ("exp3", "all"):
        exp3()


if __name__ == "__main__":
    main()
