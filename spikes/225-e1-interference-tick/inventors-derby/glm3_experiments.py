#!/usr/bin/env python3
"""glm-3 Inventors Derby — E1-harness minis for the spreadsheet-lineage reclaim list.

Edge: RD-SPREADSHEET-LINEAGE.md R1 (phase-gated noise), R2 (conservation
invariant), R4 (diversity-biased decay) + charter §8 (sorted switchboard).
Integer-only, fixed seeds, stdlib python3. Run: python3 glm3_experiments.py

Each experiment forks e1.run's interference arm VERBATIM and modifies one
thing. Controls must reproduce e1.run's published stress numbers exactly
(the self-checks print PASS/FAIL).
"""
import sys, os
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import e1

SEEDS = (1, 7, 42, 1999, 20260902)
TICKS = 4800
STRESS = dict(K=4, pulse_div=3, delta=12, drift=6, lat2=10)


# ---------------------------------------------------------------- helpers
class Triangle:
    """8-bit-up/down integer triangle wave — sin() at 2-bit fidelity, no multiplier."""
    __slots__ = ("val", "up", "peak", "thr")

    def __init__(self, period, frac=(2, 4), antiphase=False):
        self.peak = max(1, period // 2)
        # gate opens in upper part of the triangle: val >= peak*frac (integer compare)
        self.thr = (self.peak * frac[0]) // frac[1]
        self.val = self.peak if antiphase else 0
        self.up = not antiphase

    def step(self):
        if self.up:
            if self.val >= self.peak:
                self.up = False
                self.val -= 1
            else:
                self.val += 1
        else:
            if self.val <= 0:
                self.up = True
                self.val += 1
            else:
                self.val -= 1
        return self.val

    def open_(self):
        return self.val >= self.thr


def agg(rows):
    n = len(rows)
    out = {}
    for k in rows[0]:
        vals = [r[k] for r in rows]
        if isinstance(vals[0], list):
            out[k] = [round(sum(col) / n, 1) for col in zip(*vals)]
        else:
            out[k] = round(sum(vals) / n, 1) if isinstance(vals[0], float) else sum(vals)
    return out


def show(label, a):
    print(f"  {label:<26} ev={a['events']:>6} debt={a['debt']:>7} chat={a['chatter']:>4} "
          f"canc={a['cancel']:>4} maxE={a['maxerr']:>3} %w={a['pct']:>5}")


# ---------------------------------------------------------------- EXP 1: phase gate (R1)
def run_gate(seed, P1=None, P2=None, ticks=TICKS, K=4, pulse_div=3, delta=12, drift=6, lat2=10,
             frac=(2, 4), anti2=False):
    """Interference arm + per-twin triangle phase gate on pulse ADMISSION.
    Trigger with gate closed => DEFER (error persists, re-tested next tick)."""
    rng = e1.LCG(seed)
    g = e1.reality(0)
    pulses = deque()
    snap_events = ledger_mass = constructive = cancellations = chatter = 0
    max_err = settles = 0
    last_snap = -10
    deferred = both_open = one_open = 0
    gates = [Triangle(P, frac) if P else None for P in (P1, P2)]
    if anti2 and gates[1]:
        gates[1] = Triangle(P2, frac, antiphase=True)

    for t in range(ticks):
        s1 = e1.reality(t)
        s2 = e1.reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift
        for tri in gates:
            if tri:
                tri.step()
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = (s1 - g, s2 - g)
        trig = []
        for i, e in enumerate(errs):
            if abs(e) > delta:
                if gates[i] is None or gates[i].open_():
                    trig.append(e)
                else:
                    deferred += 1
        if gates[0] and gates[1]:
            o = (gates[0].open_(), gates[1].open_())
            if o[0] and o[1]:
                both_open += 1
            elif o[0] or o[1]:
                one_open += 1
        max_trig = max((abs(e) for e in trig), default=0)
        for e in trig:
            m = abs(e) // pulse_div or 1
            pulses.appendleft([m if e > 0 else -m, K])
            snap_events += 1
            ledger_mass += abs(e)
        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
            if trig and max(abs(s1 - g), abs(s2 - g)) > max_trig:
                constructive += 1
            if trig and t - last_snap == 1:
                chatter += 1
            if trig:
                last_snap = t
        err = max(abs(s1 - g), abs(s2 - g))
        max_err = max(max_err, err)
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1

    return dict(events=snap_events, debt=ledger_mass, chatter=chatter,
                cancel=cancellations, maxerr=max_err,
                pct=round(100 * settles / ticks, 1),
                deferred=deferred, both_open=both_open, one_open=one_open)


# ---------------------------------------------------------------- EXP 2: annuity ledger (R2)
def run_cons(seed, ticks=TICKS, K=4, pulse_div=3, delta=12, drift=6, lat2=10):
    """Interference arm instrumented with a per-tick integer conservation monitor.

    Pulse entries: [mag, life, cls(+1/-1), m0]. Booked per tick:
      emitted    unsigned initial mass at admission
      applied    |net| and net (signed) applied to g
      integral+/- per-sign sum of every live pulse's magnitude (the annuity)
      monitor    recomputes net two ways; any mismatch is a violation bit
    """
    rng = e1.LCG(seed)
    g = e1.reality(0)
    pulses = deque()
    snap_events = ledger_mass = constructive = cancellations = chatter = 0
    max_err = settles = 0
    last_snap = -10
    emitted = applied_abs = applied_net = 0
    integ_pos = integ_neg = 0
    m0_pos = m0_neg = 0
    violations = unit_stick = reached_unit = n_pulses = 0
    cancel_mass = 0

    for t in range(ticks):
        s1 = e1.reality(t)
        s2 = e1.reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        e1v = s1 - g
        e2v = s2 - g
        trig = []
        if abs(e1v) > delta:
            trig.append(e1v)
        if abs(e2v) > delta:
            trig.append(e2v)
        max_trig = max((abs(e) for e in trig), default=0)
        for e in trig:
            m = abs(e) // pulse_div or 1
            cls = 1 if e > 0 else -1
            pulses.appendleft([m if e > 0 else -m, K, cls, m])
            snap_events += 1
            ledger_mass += abs(e)
            emitted += m
            n_pulses += 1
            if cls > 0:
                m0_pos += m
            else:
                m0_neg += m
        if pulses:
            net = sum(p[0] for p in pulses)
            # conservation monitor: two independent sums must agree every tick
            chk_pos = sum(p[0] for p in pulses if p[2] > 0)
            chk_neg = sum(p[0] for p in pulses if p[2] < 0)
            if net != chk_pos + chk_neg:
                violations += 1
            applied_abs += abs(net)
            applied_net += net
            integ_pos += chk_pos
            integ_neg += chk_neg
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
                cancel_mass += sum(abs(p[0]) for p in pulses)
            decayed = deque()
            for mag, life, cls, m0 in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        nm = mag - (mag // 2)
                        if abs(nm) == 1:
                            reached_unit += 1
                        mag = nm
                    decayed.append([mag, life - 1, cls, m0])
                    if abs(mag) == 1:
                        unit_stick += 1
            pulses = decayed
            g += net
            if trig and max(abs(s1 - g), abs(s2 - g)) > max_trig:
                constructive += 1
            if trig and t - last_snap == 1:
                chatter += 1
            if trig:
                last_snap = t
        err = max(abs(s1 - g), abs(s2 - g))
        max_err = max(max_err, err)
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1

    return dict(events=snap_events, debt=ledger_mass, chatter=chatter,
                cancel=cancellations, maxerr=max_err,
                pct=round(100 * settles / ticks, 1),
                emitted=emitted, applied_abs=applied_abs, applied_net=applied_net,
                integ_pos=integ_pos, integ_neg=integ_neg, m0_pos=m0_pos, m0_neg=m0_neg,
                violations=violations, unit_stick=unit_stick,
                reached_unit=reached_unit, n_pulses=n_pulses, cancel_mass=cancel_mass)


# ---------------------------------------------------------------- EXP 3: sorted switchboard (§8)
LATS = (0, 3, 6, 9, 12)
KEYS = {
    "mag":     lambda r: (-r["err_abs"], r["id"]),   # biggest error first (stale twins dominate)
    "fair":    lambda r: (r["last_fire"], r["id"]),  # least-recently-fired first
    "static":  lambda r: (r["id"],),                 # tape order: linear book-keeping
    "contend": lambda r: (r["cont"], r["id"]),       # least-contended first (derby balance)
}


def run_sw(seed, key=None, C=len(LATS), ticks=TICKS, K=4, pulse_div=3, delta=12, drift=6, lats=LATS):
    """N-twin channel. The switchboard is a row per twin {id, err, last_fire, cont}.
    When candidates exceed the contention budget C, the board is SORTED by key
    and only the top-C are admitted. key=None, C=N => admit-all control."""
    rng = e1.LCG(seed)
    g = e1.reality(0)
    n = len(lats)
    last_fire = [-10] * n
    cont = [0] * n
    fires = [0] * n
    pulses = deque()
    events = debt = constructive = cancellations = chatter = 0
    max_err = settles = 0
    last_snap = -10
    rejected = 0

    for t in range(ticks):
        reads = [e1.reality(max(0, t - L)) for L in lats]
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        cands = []
        for i, s in enumerate(reads):
            e = s - g
            if abs(e) > delta:
                cands.append(dict(id=i, err=e, err_abs=abs(e),
                                  last_fire=last_fire[i], cont=cont[i]))
                cont[i] += 1  # showed up to the derby
        if key and len(cands) > C:
            cands.sort(key=KEYS[key])
            rejected += len(cands) - C
            cands = cands[:C]
        trig = [c["err"] for c in cands]
        max_trig = max((abs(e) for e in trig), default=0)
        for c in cands:
            e = c["err"]
            m = abs(e) // pulse_div or 1
            pulses.appendleft([m if e > 0 else -m, K])
            events += 1
            debt += abs(e)
            last_fire[c["id"]] = t
            fires[c["id"]] += 1
        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
            if trig and max(abs(s - g) for s in reads) > max_trig:
                constructive += 1
            if trig and t - last_snap == 1:
                chatter += 1
            if trig:
                last_snap = t
        err = max(abs(s - g) for s in reads)
        max_err = max(max_err, err)
        if all(abs(s - g) <= delta for s in reads):
            settles += 1

    return dict(events=events, debt=debt, chatter=chatter, cancel=cancellations,
                maxerr=max_err, pct=round(100 * settles / ticks, 1),
                fires=fires, rejected=rejected)


# ---------------------------------------------------------------- EXP 4: diversity-biased decay (R4)
def run_div(seed, kd=0, ticks=TICKS, K=4, pulse_div=3, delta=12, drift=6, lat2=10, win=8, thresh=3):
    """Per-twin sliding window (last 8 emissions) of emission signs.
    >=3 sign flips in window => 'diverse' twin: K_eff = K+kd; else K-kd (clamped 1..16).
    kd=0 reproduces stock E1 exactly."""
    rng = e1.LCG(seed)
    g = e1.reality(0)
    pulses = deque()
    snap_events = ledger_mass = constructive = cancellations = chatter = 0
    max_err = settles = 0
    last_snap = -10
    hist = [deque(maxlen=win), deque(maxlen=win)]
    diverse_emissions = 0

    for t in range(ticks):
        s1 = e1.reality(t)
        s2 = e1.reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        e1v = s1 - g
        e2v = s2 - g
        trig = []
        if abs(e1v) > delta:
            trig.append((0, e1v))
        if abs(e2v) > delta:
            trig.append((1, e2v))
        max_trig = max((abs(e) for _, e in trig), default=0)
        for i, e in trig:
            m = abs(e) // pulse_div or 1
            sign = 1 if e > 0 else -1
            hist[i].append(sign)
            h = list(hist[i])
            flips = sum(1 for a, b in zip(h, h[1:]) if a != b)
            diverse = flips >= thresh
            K_eff = max(1, min(16, K + kd if diverse else K - kd))
            if diverse:
                diverse_emissions += 1
            pulses.appendleft([m if e > 0 else -m, K_eff])
            snap_events += 1
            ledger_mass += abs(e)
        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
            if trig and max(abs(s1 - g), abs(s2 - g)) > max_trig:
                constructive += 1
            if trig and t - last_snap == 1:
                chatter += 1
            if trig:
                last_snap = t
        err = max(abs(s1 - g), abs(s2 - g))
        max_err = max(max_err, err)
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1

    return dict(events=snap_events, debt=ledger_mass, chatter=chatter,
                cancel=cancellations, maxerr=max_err,
                pct=round(100 * settles / ticks, 1), diverse_em=diverse_emissions)


# ---------------------------------------------------------------- EXP 5: K-axis sweep (born from R4's accident)
def sweep_k():
    print("\n== EXP 5: K-AXIS SWEEP on stock e1.run (the R4 accident, decomposed) ==")
    frames = {"stress d12/pd3": dict(delta=12, drift=6, lat2=10, pd=3),
              "gentle d6/pd3":  dict(delta=6, drift=3, lat2=5, pd=3)}
    for fname, f in frames.items():
        print(f"  [{fname}]  (impulse ref: see run below)")
        for K in (1, 2, 3, 4, 5, 6, 8):
            tw = td = tc = tt = 0.0
            me = 0
            for s in SEEDS:
                e1.SEED = s
                r = e1.run("interference", K=K, pulse_div=f["pd"], delta=f["delta"],
                           drift=f["drift"], lat2=f["lat2"])
                tw += r["pct_within"]; td += r["ledger_mass"]
                tc += r["cancellations"]; tt += r["chatter"]; me = max(me, r["max_err"])
            print(f"    K={K}: %w={tw/5:>5.1f} debt={int(td):>7} maxE={me:>3} canc={int(tc):>5} chat={int(tt):>5}")
        tw = td = 0.0
        me = 0
        for s in SEEDS:
            e1.SEED = s
            r = e1.run("sequential", delta=f["delta"], drift=f["drift"], lat2=f["lat2"])
            tw += r["pct_within"]; td += r["ledger_mass"]; me = max(me, r["max_err"])
        print(f"    impulse: %w={tw/5:>5.1f} debt={int(td):>7} maxE={me:>3}")
    # ledger/arena frames
    print("  [ledger calm frame drift=3/lat=5, delta=12]")
    for mode, K, pd, d, tag in (("sequential", 1, 3, 12, "impulse d12 (banked calm champ)"),
                                ("interference", 2, 3, 12, "intf K=2 d12"),
                                ("interference", 2, 3, 6, "intf K=2 d6 (tight)")):
        tw = td = 0.0; me = 0
        for s in SEEDS:
            e1.SEED = s
            r = e1.run(mode, K=K, pulse_div=pd, delta=d, drift=3, lat2=5)
            tw += r["pct_within"]; td += r["ledger_mass"]; me = max(me, r["max_err"])
        print(f"    {tag:<32} %w={tw/5:>5.1f} debt={int(td):>7} maxE={me:>3}")
    print("  [arena stress frame drift=6/lat=10, granite pd4/d16]")
    for K in (5, 2, 3):
        tw = td = 0.0; me = 0
        for s in SEEDS:
            e1.SEED = s
            r = e1.run("interference", K=K, pulse_div=4, delta=16, drift=6, lat2=10)
            tw += r["pct_within"]; td += r["ledger_mass"]; me = max(me, r["max_err"])
        tag = "granite K=5 (banked champ)" if K == 5 else f"granite-short K={K}"
        print(f"    {tag:<32} %w={tw/5:>5.1f} debt={int(td):>7} maxE={me:>3}")


# ---------------------------------------------------------------- EXP 6: single-pulse annuity integrals
def pulse_integral(m, K):
    """Lifetime signed integral of one pulse under e1's exact decay rule."""
    pulses = deque([[m, K]])
    tot = 0
    for _ in range(K):
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        if not pulses:
            break
        tot += sum(p[0] for p in pulses)
        d = deque()
        for mag, life in pulses:
            if life > 0:
                if abs(mag) > 1:
                    mag = mag - (mag // 2)
                d.append([mag, life - 1])
        pulses = d
    return tot


def sweep_integral():
    print("\n== EXP 6: SINGLE-PULSE ANNUITY INTEGRALS (floor-halving sign bias) ==")
    for K in (4, 8):
        for m in (2, 5, 9, 20):
            ip, im = pulse_integral(m, K), pulse_integral(-m, K)
            print(f"  K={K} m0={m:>3}:  +{m} applies {ip:>3} ({ip/m:.2f}x)   "
                  f"-{m} applies {im:>3} ({abs(im)/m:.2f}x)   bias {ip + im:+d}")


# ---------------------------------------------------------------- main
def main():
    print("== SELF-CHECK: forks vs stock e1.run (stress: d=12,drift=6,K=4,lat=10) ==")
    ok = True
    for seed in SEEDS:
        e1.SEED = seed
        ref = e1.run("interference", **STRESS)
        mine = run_gate(seed, None, None, **STRESS)
        mine2 = run_div(seed, kd=0, **STRESS)
        for m, tag in ((mine, "gate-ctl"), (mine2, "div-kd0")):
            if (m["events"], m["debt"], m["pct"], m["maxerr"]) != \
               (ref["snap_events"], ref["ledger_mass"], ref["pct_within"], ref["max_err"]):
                ok = False
                print(f"  FAIL seed={seed} {tag}: {m['events']}/{m['debt']}/{m['pct']}/{m['maxerr']}"
                      f" vs {ref['snap_events']}/{ref['ledger_mass']}/{ref['pct_within']}/{ref['max_err']}")
    print("  PASS all 5 seeds: gate-control and div-kd0 byte-match e1.run"
          if ok else "  *** MISMATCH — do not trust forks ***")

    print("\n== EXP 1: TRIANGLE PHASE GATE on pulse admission (R1) ==")
    for label, kw in [("no gate (stock E1)", dict(P1=None, P2=None)),
                      ("homog anti P=16/16 f1/2", dict(P1=16, P2=16, anti2=True)),
                      ("diverse P=13/29 f1/2", dict(P1=13, P2=29)),
                      ("diverse P=13/29 f1/4", dict(P1=13, P2=29, frac=(1, 4))),
                      ("diverse P=13/29 f3/4", dict(P1=13, P2=29, frac=(3, 4))),
                      ("diverse P=11/41 f1/4", dict(P1=11, P2=41, frac=(1, 4)))]:
        rows = [run_gate(s, **kw, **STRESS) for s in SEEDS]
        a = agg(rows)
        extra = (f" defer={a['deferred']} bothOpen={a['both_open']} oneOpen={a['one_open']}"
                 if kw["P1"] else "")
        show(label, a)
        print(f"    {extra.strip()}")

    print("\n== EXP 2: ANNUITY LEDGER — conservation audit of stock E1 (R2) ==")
    for tag, params in (("stress", STRESS),
                        ("gentle", dict(K=8, pulse_div=3, delta=6, drift=3, lat2=5))):
        rows = [run_cons(s, **params) for s in SEEDS]
        a = agg(rows)
        print(f"  [{tag}] viol={a['violations']} pulses={a['n_pulses']} "
              f"emitted={a['emitted']:.0f} applied|net|={a['applied_abs']:.0f} "
              f"applied_net={a['applied_net']:.0f}")
        amp_p = a["integ_pos"] / a["m0_pos"] if a["m0_pos"] else 0
        amp_n = abs(a["integ_neg"] / a["m0_neg"]) if a["m0_neg"] else 0
        print(f"        annuity amp(+) = {amp_p:.3f}x   amp(-) = {amp_n:.3f}x   "
              f"asymmetry = {amp_p - amp_n:+.3f}x")
        print(f"        reached|1|={a['reached_unit']:.0f} unit-stick-ticks={a['unit_stick']:.0f} "
              f"cancels={a['cancel']:.0f} cancel-mass={a['cancel_mass']:.0f}")

    print("\n== EXP 3: SORTED SWITCHBOARD — N=5 twins, contention budget C=3 (§8) ==")
    rows = [run_sw(s, key=None, C=len(LATS)) for s in SEEDS]
    show("admit-all control", agg(rows))
    print(f"    fires/twin: {agg(rows)['fires']}")
    for C in (3, 2, 1):
        print(f"  -- budget C={C} --")
        for key in ("mag", "fair", "static", "contend"):
            rows = [run_sw(s, key=key, C=C) for s in SEEDS]
            a = agg(rows)
            show(f"sort={key}", a)
            print(f"    fires/twin: {a['fires']}  rejected={a['rejected']}")

    print("\n== EXP 4: DIVERSITY-BIASED DECAY — window-flip K_eff (R4) ==")
    for kd in (-2, -1, 0, 1, 2):
        rows = [run_div(s, kd=kd, **STRESS) for s in SEEDS]
        a = agg(rows)
        show(f"kd={kd:+d}", a)
        print(f"    diverse-emissions={a['diverse_em']}")

    sweep_k()
    sweep_integral()


if __name__ == "__main__":
    main()
