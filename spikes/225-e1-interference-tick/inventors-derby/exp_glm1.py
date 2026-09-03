#!/usr/bin/env python3
"""Inventors Derby — contestant glm-1 (z.ai GLM-5.3 lane).

Four novel small-scale experiments on the E1 interference-tick machinery.
Integer-only inside the loop (Python ints, floor div, LCG contract items from
e1.py: fdiv semantics, 64-bit LCG intermediate, FIFO oldest-first expiry,
decay-from-snapshot). Floats appear ONLY in display rounding at print time,
same as e1.py's pct_within.

A. BYZANTINE TWIN — adversarial lying sensor, interference vs impulse.
B. BUNDLE CAPACITY — N staggered twins, where does superposition stop winning.
C. COFIRE LATENCY LEARNER — first-ever run of the charter's cofire primitive:
   integer coincident-fire histogram self-calibrates the twin skew.
D. QUEUE ARCHAEOLOGY AUDITOR — retrodict the ledger from the pulse queue alone;
   single-substrate catch of the DIVERGENCE.md queue-geometry bug class.
"""
from collections import deque

SEEDS = (1, 7, 42, 1999, 20260902)
PERIOD = 240


class LCG:
    def __init__(self, seed):
        self.x = seed & 0x7FFFFFFF or 1

    def next(self):
        self.x = (1103515245 * self.x + 12345) & 0x7FFFFFFF
        return self.x

    def below(self, n):
        return self.next() % n


def reality(t):
    phase = t % PERIOD
    if phase < 96:
        return 400 + phase * 8 // 5
    elif phase < 144:
        return 400 + 96 * 8 // 5 - (phase - 96)
    else:
        return 400 + 96 * 8 // 5 - 48 - (phase - 144) * 8 // 5


def run_fabric(mode, ticks, lats, lies=None, K=4, pd=3, delta=12, drift=6,
               seed=20260902, expiry_bug=False, audit_tick=None):
    """Generalized E1 runner: N sensors with individual latencies and optional
    per-sensor lie offsets (callable t -> int added to the reading).
    Sequential arm keeps e1 semantics: first triggering sensor in list order
    wins (T1 priority). Interference arm: every triggering sensor emits."""
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    n = len(lats)
    lies = lies or {}
    emissions = []          # (tick, sensor, signed_pulse_or_impulse, trigger_err)
    events = mass = cancels = chatter = settles = 0
    last = -10
    resid = []              # per-tick |g - s_true| AFTER correction
    cflags = []             # per-tick destructive-cancellation flag
    audit = None

    for t in range(ticks):
        reads = [reality(max(0, t - lats[i])) + (lies[i](t) if i in lies else 0)
                 for i in range(n)]
        s_true = reality(t)
        g += rng.below(2 * drift + 1) - drift

        # FIFO expiry, oldest at the right end (e1 contract item 3)
        if expiry_bug:
            while pulses and pulses[-1][1] <= 1:   # window-edge off-by-one bug
                pulses.pop()
        else:
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
                m = abs(e) // pd or 1
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
                decayed = deque()                      # snapshot decay (item 4)
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)     # fdiv sign-safe (item 1)
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
        if audit_tick is not None and t == audit_tick:
            audit = (t, [tuple(p) for p in pulses])

    return dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
                settles=settles, resid=resid, cflags=cflags,
                emissions=emissions, audit=audit, ticks=ticks)


def within_pm(window, delta):
    return 1000 * sum(1 for x in window if x <= delta) // len(window)


# ---------------------------------------------------------------- A
def exp_a():
    print("== A. BYZANTINE TWIN (lie +24 on sensor 3, ticks 1200-2399; "
          "delta=12 drift=6 K=4 pd=3 lats=[0,10,5]) ==")
    print(f"{'mode':<14}{'seed':>9}{'honest%':>9}{'lie%':>8}{'maxDrag':>9}"
          f"{'cancLie':>9}{'recover':>9}")

    def lie(t):
        return 24 if 1200 <= t < 2400 else 0

    for mode in ("sequential", "interference"):
        for seed in SEEDS:
            r = run_fabric(mode, 3600, [0, 10, 5], lies={2: lie}, seed=seed)
            w_h, w_l, w_r = r["resid"][:1200], r["resid"][1200:2400], r["resid"][2400:]
            rec = -1
            for i in range(len(w_r) - 10):
                if all(x <= 12 for x in w_r[i:i + 10]):
                    rec = i
                    break
            print(f"{mode:<14}{seed:>9}{within_pm(w_h,12)/10:>9.1f}"
                  f"{within_pm(w_l,12)/10:>8.1f}{max(w_l):>9}"
                  f"{sum(r['cflags'][1200:2400]):>9}{rec:>9}")


# ---------------------------------------------------------------- B
def exp_a2():
    print("\n== A2. lie-detector stat: cancellation permille, honest vs lie window (interference) ==")
    def lie(t):
        return 24 if 1200 <= t < 2400 else 0
    for seed in SEEDS:
        r = run_fabric("interference", 3600, [0, 10, 5], lies={2: lie}, seed=seed)
        h = 1000 * sum(r["cflags"][:1200]) // 1200
        l = 1000 * sum(r["cflags"][1200:2400]) // 1200
        print(f"  seed {seed:>9}: honest {h} permille  lie {l} permille  ratio x{(l + 1) // (h + 1)}")


def exp_b():
    print("\n== B. BUNDLE CAPACITY (N staggered twins, lat spacing 10; stress) ==")
    print(f"{'N':>2} {'mode':<13}{'allWithin%':>11}{'trueRes%':>10}{'events':>8}"
          f"{'cancels':>9}{'maxTrue':>8}")
    for N in range(2, 9):
        lats = list(range(0, N * 10, 10))
        for mode in ("sequential", "interference"):
            aw = tr = ev = ca = mt = 0
            for seed in SEEDS:
                r = run_fabric(mode, 4800, lats, seed=seed)
                aw += r["settles"] * 1000 // r["ticks"]
                tr += within_pm(r["resid"], 12)
                ev += r["events"]
                ca += r["cancels"]
                mt = max(mt, r["resid"] and max(r["resid"]))
            k = len(SEEDS)
            print(f"{N:>2} {mode:<13}{aw/k/10:>11.1f}{tr/k/10:>10.1f}{ev//k:>8}"
                  f"{ca//k:>9}{mt:>8}")


# ---------------------------------------------------------------- C
def cofire_scores(emissions, maxlag=25, quiet=5):
    """Integer coincident-fire correlator over snap events.
    score[tau] = (# same-sign A->B pairs at lag tau) - (# opposite-sign pairs).
    Variants: quiet (B isolated), iso (B isolated AND paired A isolated)."""
    A = [(t, 1 if s > 0 else -1) for (t, i, s, e) in emissions if i == 0]
    B = [(t, 1 if s > 0 else -1) for (t, i, s, e) in emissions if i == 1]
    apos = set(t for t, s in A if s > 0)
    aneg = set(t for t, s in A if s < 0)
    at = set(t for t, s in A)
    bt = set(t for t, s in B)

    def quiet_at(tt, times):
        return not any((tt - j) in times for j in range(1, quiet + 1))

    sc = [0] * (maxlag + 1)
    scq = [0] * (maxlag + 1)
    sci = [0] * (maxlag + 1)
    for t, s in B:
        bq = quiet_at(t, bt)
        for tau in range(maxlag + 1):
            ta = t - tau
            hit = 1 if (ta in apos) else (-1 if (ta in aneg) else 0)
            if hit:
                v = hit * s
                sc[tau] += v
                if bq:
                    scq[tau] += v
                    if quiet_at(ta, at):
                        sci[tau] += v
    return sc, scq, sci


def exp_c():
    print("\n== C. COFIRE LATENCY LEARNER (interference stress, lat2=10, 4800 ticks) ==")
    print("   v1 dense-fire correlator FAILED (peak at maxlag boundary, tauQ=0);")
    print("   v2: isolation filter (both sensors 5-tick silent before their snaps)")
    print(f"{'seed':>9}{'top5lags(iso)':>26}{'tau':>5}{'learnLat':>10}{'before%':>9}{'after%':>9}")
    for seed in SEEDS:
        r = run_fabric("interference", 4800, [0, 10], seed=seed)
        sc, scq, sci = cofire_scores(r["emissions"])
        top = sorted(range(len(sci)), key=lambda i: -sci[i])[:5]
        tau = max(range(len(sci)), key=lambda i: sci[i])
        lat2 = max(0, 10 - tau)
        r2 = run_fabric("interference", 4800, [0, lat2], seed=seed)
        b = r["settles"] * 1000 // r["ticks"]
        a = r2["settles"] * 1000 // r2["ticks"]
        print(f"{seed:>9}{str(top):>26}{tau:>5}{lat2:>10}{b/10:>9.1f}{a/10:>9.1f}")


# ---------------------------------------------------------------- D
def audit_queue(audit, emissions, K):
    """Retrodict emissions from queue snapshot; cross-check vs ledger."""
    t_star, qs = audit
    led = {}
    for (t, i, pm, e) in emissions:
        led.setdefault(t, []).append(1 if pm > 0 else -1)
    ghosts = losses = 0
    ages = []
    for mag, life in qs:
        a = K - 1 - life
        ages.append(a)
        te = t_star - a
        sg = 1 if mag > 0 else -1
        if te not in led or sg not in led[te]:
            ghosts += 1
    implied = {t_star - (K - 1 - life) for mag, life in qs}
    for te in range(t_star - K + 1, t_star + 1):
        if te in led and te not in implied:
            losses += len(led[te])
    uniq = sum(1 for a in ages if a == 0)
    width = sum((1 << a) - 1 for a in ages)
    return dict(n=len(qs), ghosts=ghosts, losses=losses, ages=sorted(ages),
                uniq=uniq, mean_width10=10 * width // max(1, len(qs)))


def exp_d():
    print("\n== D. QUEUE ARCHAEOLOGY AUDITOR (interf stress seed 20260902, K=4) ==")
    print("   48 audit ticks (every 100 from 300): aggregate retrodiction stats")
    for bug in (False, True):
        tot = dict(n=0, ghosts=0, losses=0, uniq=0, width=0, ages=[0]*4)
        for ta in range(300, 4800, 100):
            r = run_fabric("interference", 4800, [0, 10], seed=20260902,
                           audit_tick=ta, expiry_bug=bug)
            a = audit_queue(r["audit"], r["emissions"], 4)
            tot["n"] += a["n"]; tot["ghosts"] += a["ghosts"]
            tot["losses"] += a["losses"]; tot["uniq"] += a["uniq"]
            tot["width"] += a["mean_width10"] * a["n"] // 10
            for age in a["ages"]:
                if age < 4:
                    tot["ages"][age] += 1
        tag = "BUG expiry window-edge" if bug else "correct harness     "
        n = max(1, tot["n"])
        print(f"{tag}  pulses={tot['n']:>3} ghosts={tot['ghosts']} "
              f"losses={tot['losses']} ageHist0-3={tot['ages']} "
              f"exactAmp={tot['uniq']} meanAmbWidth={tot['width']/n:.2f}")
    r = run_fabric("interference", 4800, [0, 10], seed=20260902, audit_tick=4790)
    a = audit_queue(r["audit"], r["emissions"], 4)
    print("   sample audit t=4790, live pulse magnitudes by age:",
          {age: [m for m, l in r['audit'][1] if 4 - 1 - l == age] for age in range(4)})


if __name__ == "__main__":
    exp_a()
    exp_a2()
    exp_b()
    exp_c()
    exp_d()
