#!/usr/bin/env python3
"""SPIN 16 — SPOKE: PULSE-DIAL II: ADAPTIVE (ECHO-GATED) COMPENSATION
(proposal-dispatched by SPIN-11-pulse-dial.md's Next section; no LCG pick
consumed). Files: spin16_pulse_dial2.py (this), spin16-output.txt (raw),
SPIN-16-pulse-dial2.md (report). Fabric: spin11_pulse_dial.run_fabric_mc
reused verbatim for off / MC-A arms; the new runner run_fabric_gate is an
exact copy of its interference loop with ONE added per-tick gate at the
emission line (gate="never" is byte-identical to mc=0; gate="always" is
byte-identical to mc=1 / MC-A).

MECHANISM (Spin 11's pd=12 lesson): blanket compensation is a trade — it
rescues wall casualties (step5/N=7: 0.3 -> 8.8 at delta=12 K=1) but hurts
healthy grammars (kcoh5 53.2 -> 37.6). The wall law says divergence needs
the echo factor |1 - N/pd| materially > 1. ADAPTIVE IDEA: compensate only
the events whose CONCURRENT echo factor exceeds a threshold:
    gate opens at tick t iff nf(t) > 0 and |1 - nf/pd| > theta_g
where nf = number of triggering twins THIS tick — an in-loop observable
(the scheduler counts simultaneous triggers; no future information).
Integer arithmetic: 100*|pd-nf| > round(100*theta)*pd. When open, that
tick's emissions take the MC-A division (//min(nf,pd)); when closed they
emit the raw fabric pulse |e|//pd. Memory guard carried over from spin-11
verbatim (bail at any |e| > 10^12) for every gate mode except "never".

=====================================================================
PRE-REGISTERED PREDICTIONS — in this committed docstring BEFORE any run.
Every endpoint pinned to eval window EV=12 (true12 = within_pm(resid,12)),
the spin-8 saturation-scar convention, regardless of delta.

R1 (SPIN-11's registered Next-section prediction, tested verbatim):
    echo-gated compensation at pd=3, delta=12, K=1:
    (a) step5/N=7 [0,5,10,15,20,25,30] true12 >= 9.0
    (b) kcoh5@30 [0,0,0,0,0,30]        true12 >= 50.0
    Leg (b) is structural: N=6=2pd at pd=3 => concurrent factor <= 1.0
    < theta for every theta > 1 => the gate provably never opens (byte-
    proven by canary CE). Leg (a) is the live test: blanket MC-A gave
    8.8; the gate leaves mid-size (nf <= 2pd) corrective shoves
    uncompensated, worth >= +0.2pp over MC-A if R1(a) passes.

P16b (EXP 1 calibration, secondary): theta-coverage law — the gate opens
    at a 2pd+1 wall iff theta < 1 + 1/pd, i.e. pd < 1/(theta-1). Sweep
    prediction at the pd=6 wall cell ladder(30,13) (2pd+1=13, echo factor
    7/6 ~ 1.167), delta=12, K=1: theta in {1.05, 1.1} rescue (true12
    >= 5.0); theta in {1.25, 1.5, 2.0} do NOT (cell stays diverged,
    true12 <= 3.0). Coverage table: 1.05 -> pd<=19, 1.1 -> pd<=9,
    1.25 -> pd<=3, 1.5 -> pd<=1, 2.0 -> none.

theta* selection rule (pre-registered; used by EXP 2/3): the LARGEST
    theta in the sweep satisfying BOTH R1(a) (step5 >= 9.0 at delta=12
    K=1) AND P16b's rescue leg (wall6 >= 5.0); if none satisfies both,
    argmax of step5 rescue at delta=12 K=1, flagged REGISTERED-GATE-MISS.

P16a (THE new quantitative prediction for EXP 3, registered in this
    commit BEFORE the exp-3 run; one prediction, one falsifier): AS x
    gate composition on N=7 supra-wall grammars {step5 [0,5,10,15,20,25,30]
    (AS no-op control), kcoh1w7 [0]*6+[30], cohort37 [0,0,0,30,30,30,30],
    zero7 [0]*7} at pd=3, delta=12, K in {1,2}, arms {base, AS-exact,
    gate@theta*, AS-exact + gate@theta*}: in every cell where BOTH single
    knobs beat base by >= +5.0pp (true12),
        residual := joint - max(single_AS, single_gate) lies in [-2.0, +2.0]
    (additive, NOT superadditive). Pre-registered mechanism: substrate
    coupling — AS decorrelates firing times and thereby STARVES the
    nf >= 2pd+1 pile-ups the gate feeds on; witness: gate-open ticks under
    AS+gate <= 10% of gate-alone's in qualifying cells (and if the joint
    gate never opens, the joint run is byte-identical to AS-alone).
    FALSIFIER: any qualifying cell with residual >= +2.1 (superadditive:
    spin-14's orthogonal-channel law extends to the gate — knob-physics
    channels, phase vs amplitude, would be doing the work) or <= -2.1
    (destructive competition). Basis: spin-14 found superadditivity only
    for orthogonal FAILURE channels; the gate and AS attack the same
    failure substrate (the synchronized pile-up) even though their knob
    physics differ.

Embedded wall-law probe (unregistered observation, EXP 3 base arm): zero7
    uncompensated tests whether N > 2pd divergence survives at span 6
    (spin-8/11 measured the wall only on spread-30 ladders); zero6=77.3
    is the N=2pd anchor.

Canaries (mandatory, abort on fail):
  CA: spin-11 replay via run_fabric_mc(mc=0), EV=12: step6/N=6 26.8,
      step5/N=7 0.3, step1/N=31 0.1, kcoh5@30 53.2.
  CB: spread=0 codepath identity by N-group, separately for gate modes
      {never, always, 1.05, 1.25} (spin-11 canary B extended to the gate).
  CC: gate="never" == run_fabric_mc(mc=0) full-dict, 8 configs.
  CD: gate="always" == run_fabric_mc(mc=1) full-dict, 8 configs.
  CE: structural inertness: gate in {1.05, 1.25} == mc=0 full-dict for
      every N=6 pd=3 panel grammar (plus one K=4 and one delta=24 probe)
      — the byte-level guarantee behind R1(b).

Integer-only in-loop (gate comparison included: 100*|pd-nf| > theta100*pd);
floats only in display. Seeds {1,7,42,1999,20260902}, 4800 ticks,
delta=12 unless stated, drift=6, pd=3 unless stated. Run with -u, no pipes.
"""
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "inventors-derby"))
sys.path.insert(0, HERE)
from exp_glm1 import run_fabric, within_pm  # noqa: E402
import spin11_pulse_dial as s11  # noqa: E402
from spin11_pulse_dial import (LCG, reality, run_fabric_mc,  # noqa: E402
                               ladder, ladder_step, kcoh, mean, SEEDS)

TICKS = 4800
DELTA = 12
EV = 12                 # PINNED eval window for every prediction (spin-8 scar)
DIV_AT = 10 ** 6
THETAS = (1.05, 1.1, 1.25, 1.5, 2.0)
MCK = ("events", "mass", "cancels", "chatter", "settles",
       "resid", "cflags", "emissions", "audit", "ticks")


def mkeys(r):
    return {k: r[k] for k in MCK}


# ---------------------------------------------------------------- fabric
def run_fabric_gate(mode, ticks, lats, lies=None, K=4, pd=3, delta=12, drift=6,
                    seed=20260902, gate=1.05):
    """EXACT copy of spin11.run_fabric_mc's loop; the MC selector is replaced
    by the echo gate. gate="never" -> byte-identical to mc=0; gate="always"
    -> byte-identical to mc=1 (MC-A); numeric theta -> per-tick gate
    |1-nf/pd| > theta, integer-exact as 100*|pd-nf| > theta100*pd. When the
    gate opens, that tick's emissions take the MC-A division //min(nf,pd);
    otherwise the raw fabric pulse |e|//pd. Guard as in spin-11 for every
    mode except "never". Extra diagnostics: gopen (ticks gate open),
    gcomp (twins compensated)."""
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
    gopen = gcomp = 0
    t100 = None if gate in ("never", "always") else int(round(gate * 100))

    for t in range(ticks):
        reads = [reality(max(0, t - lats[i])) + (lies[i](t) if i in lies else 0)
                 for i in range(n)]
        s_true = reality(t)
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        if gate != "never" and any(abs(e) > 10 ** 12 for e in errs):
            # spin-11 memory guard, carried over verbatim for
            # compensated-capable arms; "never" stays byte-identical to mc=0.
            resid.append(abs(s_true - g))
            cflags.append(0)
            break
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
            if gate == "always":
                neff = min(nf, pd)
            elif gate == "never":
                neff = 1 if nf else 0
            else:
                open_ = nf > 0 and 100 * abs(pd - nf) > t100 * pd
                neff = min(nf, pd) if open_ else (1 if nf else 0)
                if open_:
                    gopen += 1
            for i, e in trig:
                m = abs(e) // pd or 1
                if neff > 1:
                    m = m // neff or 1
                    gcomp += 1
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
                emissions=emissions, audit=None, ticks=ticks,
                gopen=gopen, gcomp=gcomp)


# ---------------------------------------------------------------- helpers
def gcell(lats, pd=3, K=1, delta=DELTA, gate=1.05, seeds=SEEDS):
    rs = [run_fabric_gate("interference", TICKS, lats, K=K, pd=pd, delta=delta,
                          drift=6, seed=s, gate=gate) for s in seeds]
    t12 = [within_pm(r["resid"], EV) for r in rs]
    mr = [max(r["resid"]) for r in rs]
    return dict(m=mean(t12) / 10, mr=mr, div=all(x > DIV_AT for x in mr),
                gopen=mean([r["gopen"] for r in rs]),
                gcomp=mean([r["gcomp"] for r in rs]),
                ev=mean([r["events"] for r in rs]), rs=rs)


def mcell(lats, pd=3, K=1, delta=DELTA, mc=0):
    return s11.cell(lats, pd, K=K, delta=delta, mc=mc)


def show(c):
    return f"{c['m']:5.1f}{'D' if c['div'] else ' '}"


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY CA: spin-11 replay via run_fabric_mc(mc=0) (EV=12) ==")
    for name, lats, pd, pub, tol in (
            ("step6/N=6 K=1", ladder(30), 3, 26.8, 0.2),
            ("step5/N=7 K=1", ladder_step(30, 5), 3, 0.3, 0.5),
            ("step1/N=31 K=1", ladder_step(30, 1), 3, 0.1, 0.5),
            ("kcoh5@30 K=1", kcoh(5, 30), 3, 53.2, 0.2)):
        c = mcell(lats, pd)
        good = abs(c["m"] - pub) <= tol
        ok &= good
        print(f"  {name:<16} got {c['m']:5.1f}  pub {pub:5.1f}  "
              f"{'OK' if good else 'DRIFT'}")

    print("\n== CANARY CB: spread=0 codepath identity by N-group, per gate mode ==")
    fams = {f"step{g}": ladder_step(0, g) for g in (1, 2, 3, 5, 6, 10, 15, 30)}
    fams.update({"ladder0": ladder(0), "kcoh5_0": kcoh(5, 0),
                 "kcoh1_0": kcoh(1, 0), "cohort0": [0] * 6})
    groups = {}
    for name, lats in fams.items():
        groups.setdefault(len(lats), []).append(name)
    for gm in ("never", "always", 1.05, 1.25):
        okb = True
        for nn, names in sorted(groups.items()):
            ref = run_fabric_gate("interference", TICKS, fams[names[0]], K=1,
                                  pd=3, delta=DELTA, drift=6, seed=SEEDS[0],
                                  gate=gm)
            for nm in names[1:]:
                if mkeys(run_fabric_gate("interference", TICKS, fams[nm], K=1,
                                         pd=3, delta=DELTA, drift=6,
                                         seed=SEEDS[0], gate=gm)) != mkeys(ref):
                    okb = False
                    print(f"  MISMATCH gate={gm} N={nn} {nm}")
        print(f"  gate={gm}: {'PASS' if okb else 'FAIL'} "
              f"({len(fams)} codepaths, {len(groups)} N-groups)")
        ok &= okb

    cfgs = (
        (ladder(30), dict(pd=3, K=1)),
        (kcoh(5, 30), dict(pd=3, K=4)),
        ([0, 0, 0, 30, 30, 30], dict(pd=3, K=1, delta=24)),
        (ladder(30, 13), dict(pd=6, K=1)),
        (ladder_step(30, 5), dict(pd=3, K=1)),
        (ladder(0), dict(pd=6, K=8)),
        ([0] * 7, dict(pd=2, K=1)),
        (ladder_step(0, 3), dict(pd=12, K=2)),
    )
    print("\n== CANARY CC: gate='never' == run_fabric_mc(mc=0), full-dict ==")
    okc = True
    for lats, kw in cfgs:
        a = run_fabric_mc("interference", TICKS, lats, drift=6, seed=SEEDS[0],
                          mc=0, **kw)
        b = run_fabric_gate("interference", TICKS, lats, drift=6,
                            seed=SEEDS[0], gate="never", **kw)
        if mkeys(b) != mkeys(a):
            okc = False
            print(f"  MISMATCH lats={lats[:8]} {kw}")
    print(f"  {'PASS' if okc else 'FAIL'}: {len(cfgs)} configs full-dict identical")
    ok &= okc

    print("\n== CANARY CD: gate='always' == run_fabric_mc(mc=1), full-dict ==")
    okd = True
    for lats, kw in cfgs:
        a = run_fabric_mc("interference", TICKS, lats, drift=6, seed=SEEDS[0],
                          mc=1, **kw)
        b = run_fabric_gate("interference", TICKS, lats, drift=6,
                            seed=SEEDS[0], gate="always", **kw)
        if mkeys(b) != mkeys(a):
            okd = False
            print(f"  MISMATCH lats={lats[:8]} {kw}")
    print(f"  {'PASS' if okd else 'FAIL'}: {len(cfgs)} configs full-dict identical")
    ok &= okd

    print("\n== CANARY CE: structural N=6/pd=3 inertness: gate {1.05,1.25} =="
          " mc=0, full-dict ==")
    oke = True
    panel6 = (kcoh(5, 30), kcoh(1, 30), ladder(30),
              [0, 0, 0, 30, 30, 30], [0] * 6)
    for gm in (1.05, 1.25):
        for lats in panel6:
            a = run_fabric_mc("interference", TICKS, lats, K=1, pd=3,
                              delta=DELTA, drift=6, seed=SEEDS[0], mc=0)
            b = run_fabric_gate("interference", TICKS, lats, K=1, pd=3,
                                delta=DELTA, drift=6, seed=SEEDS[0], gate=gm)
            if mkeys(b) != mkeys(a):
                oke = False
                print(f"  MISMATCH gate={gm} lats={lats}")
    for lats, kw, gm in ((kcoh(5, 30), dict(K=4), 1.05),
                         ([0, 0, 0, 30, 30, 30], dict(delta=24), 1.25)):
        ka = dict(pd=3, delta=DELTA, drift=6, seed=SEEDS[0], mc=0)
        ka.update(kw)
        a = run_fabric_mc("interference", TICKS, lats, **ka)
        kb = dict(pd=3, delta=DELTA, drift=6, seed=SEEDS[0], gate=gm)
        kb.update(kw)
        b = run_fabric_gate("interference", TICKS, lats, **kb)
        if mkeys(b) != mkeys(a):
            oke = False
            print(f"  MISMATCH probe gate={gm} {kw}")
    print(f"  {'PASS' if oke else 'FAIL'}: 5 grammars x 2 thetas + K4/d24 "
          f"probes, full-dict (R1(b) structural guarantee)")
    ok &= oke
    print("\nCANARIES:", "PASS" if ok else "FAIL")
    return ok


# ---------------------------------------------------------------- EXP 1
def exp1():
    print("\n== EXP 1: theta calibration — registered endpoints + pd=6 wall ==")
    cells = (
        ("step5 N=7 pd=3 (rescue endpoint)", ladder_step(30, 5), 3, 0.3, 8.8),
        ("kcoh5@30 pd=3 (health endpoint)", kcoh(5, 30), 3, 53.2, 37.6),
        ("ladder30x13 pd=6 (wall probe)", ladder(30, 13), 6, 2.3, 8.1),
    )
    res = {}
    for name, lats, pd, pub_off, pub_mc in cells:
        off = mcell(lats, pd)
        alw = mcell(lats, pd, mc=1)
        print(f"\n  --- {name}: lats={lats} ---")
        print(f"  off    {show(off)}   (spin-11 pub {pub_off})   "
              f"MC-A {show(alw)}   (spin-11 pub {pub_mc})")
        res[(name, "off")] = off["m"]
        for th in THETAS:
            c = gcell(lats, pd=pd, K=1, gate=th)
            res[(name, th)] = c["m"]
            res[(name, th, "cell")] = c
            print(f"  th={th:<4} {show(c)}   gOpen/cell {c['gopen']:8.1f}   "
                  f"compTw {c['gcomp']:9.1f}   ev {c['ev']:8.0f}")

    print("\n  theta-coverage law (gate opens at 2pd+1 wall iff theta < 1+1/pd):")
    for th in THETAS:
        t100 = int(round(th * 100))
        p, q = 0, 1
        while 100 * (q + 1) > t100 * q:
            p = q
            q += 1
        print(f"   theta={th:<4}: opens at 2pd+1 wall for pd <= {p}")

    s5n = "step5 N=7 pd=3 (rescue endpoint)"
    w6n = "ladder30x13 pd=6 (wall probe)"
    cands = [th for th in THETAS
             if res[(s5n, th)] >= 9.0 and res[(w6n, th)] >= 5.0]
    if cands:
        theta_star = max(cands)
        miss = False
    else:
        theta_star = max(THETAS, key=lambda th: res[(s5n, th)])
        miss = True
    k5 = res[("kcoh5@30 pd=3 (health endpoint)", theta_star)]
    print(f"\n  theta* = {theta_star}"
          f"{'  [REGISTERED-GATE-MISS: no theta satisfied both legs]' if miss else ''}")
    print(f"  R1(a) step5 gate@th* d12 K1 = {res[(s5n, theta_star)]:.1f} "
          f"(>= 9.0: {'PASS' if res[(s5n, theta_star)] >= 9.0 else 'FAIL'})")
    print(f"  R1(b) kcoh5 gate@th* d12 K1 = {k5:.1f} "
          f"(>= 50.0: {'PASS' if k5 >= 50.0 else 'FAIL'})  [structural: gate"
          f" provably inert at N=6=2pd, canary CE]")
    pb = all(res[(w6n, th)] >= 5.0 for th in (1.05, 1.1)) and \
        all(res[(w6n, th)] <= 3.0 and res[(w6n, th, "cell")]["div"]
            for th in (1.25, 1.5, 2.0))
    for th in THETAS:
        c = res[(w6n, th, "cell")]
        leg = "rescue" if th in (1.05, 1.1) else "no-rescue"
        print(f"  P16b th={th:<4} wall6 = {c['m']:.1f}{'D' if c['div'] else ''}"
              f"  [{leg}]")
    print(f"  P16b (theta-coverage at pd=6 wall): "
          f"{'PASS' if pb else 'FAIL'}")
    return theta_star, miss, res


# ---------------------------------------------------------------- EXP 2
def exp2(theta_star):
    print(f"\n== EXP 2: panel {{kcoh5,kcoh1,ladder,cohort,step5/N=7,zero}} x"
          f" comp {{off, gate@{theta_star}, MC-A}} x delta {{12,24}} x K"
          f" {{1,2,4}}  (pd=3; true12 EV=12; native window in parens at"
          f" delta=24) ==")
    grams = (("kcoh5", kcoh(5, 30)), ("kcoh1", kcoh(1, 30)),
             ("ladder", ladder(30)), ("cohort", [0, 0, 0, 30, 30, 30]),
             ("step5", ladder_step(30, 5)), ("zero", [0] * 6))
    gmap = dict(grams)
    tab = {}
    for d in (12, 24):
        print(f"\n  --- delta={d} ---")
        print(f"  {'grammar':>8} {'comp':>8} | {'K=1':>13} {'K=2':>13} {'K=4':>13}")
        for name, lats in grams:
            for comp in ("off", "gate", "MC-A"):
                struct = comp == "gate" and len(lats) == 6
                vals = []
                gcells = []
                for k in (1, 2, 4):
                    if comp == "off":
                        c = mcell(lats, 3, K=k, delta=d)
                        nat = mean([within_pm(r["resid"], d)
                                    for r in c["rs"]]) / 10
                        vals.append((c["m"], nat, c["div"]))
                    elif comp == "MC-A":
                        c = mcell(lats, 3, K=k, delta=d, mc=1)
                        nat = mean([within_pm(r["resid"], d)
                                    for r in c["rs"]]) / 10
                        vals.append((c["m"], nat, c["div"]))
                    elif struct:
                        vals.append(tab[(name, d, "off", k)])
                    else:
                        c = gcell(lats, 3, K=k, delta=d, gate=theta_star)
                        nat = mean([within_pm(r["resid"], d)
                                    for r in c["rs"]]) / 10
                        vals.append((c["m"], nat, c["div"]))
                        gcells.append(c)
                    tab[(name, d, comp, k)] = vals[-1]
                lbl = comp + ("=off" if struct else "")
                cells = []
                for m, nat, dv in vals:
                    s = f"{m:5.1f}" + (f"({nat:5.1f})" if d == 24 else "")
                    if dv:
                        s += "D"
                    cells.append(f"{s:>13}")
                print(f"  {name:>8} {lbl:>8} | " + " | ".join(cells))
                if gcells:
                    print(f"  {'':>8} {'gOpen':>8} | "
                          + " | ".join(f"{c['gopen']:>13.1f}"
                                        for c in gcells))

    s5 = tab[("step5", 12, "gate", 1)][0]
    k5 = tab[("kcoh5", 12, "gate", 1)][0]
    print(f"\n  R1 registered endpoints (delta=12, K=1, gate@th*): "
          f"step5 {s5:.1f} ({'PASS' if s5 >= 9.0 else 'FAIL'} vs >=9.0) ; "
          f"kcoh5 {k5:.1f} ({'PASS' if k5 >= 50.0 else 'FAIL'} vs >=50.0)")

    print("\n  K=2 trough check (K2 < min(K1,K4)) at delta=12:")
    for name, _ in grams:
        line = f"   {name:>8}:"
        for comp in ("off", "gate", "MC-A"):
            v = [tab[(name, 12, comp, k)][0] for k in (1, 2, 4)]
            line += (f"  {comp} {'T' if v[1] < min(v[0], v[2]) else '-'}"
                     f"[{v[0]:.1f},{v[1]:.1f},{v[2]:.1f}]")
        note = "  (gate==off structural)" if len(gmap[name]) == 6 else ""
        print(line + note)

    print("\n  comp x K interaction (K4-K1, delta=12):")
    for name, _ in grams:
        so = tab[(name, 12, "off", 4)][0] - tab[(name, 12, "off", 1)][0]
        sg = tab[(name, 12, "gate", 4)][0] - tab[(name, 12, "gate", 1)][0]
        sm = tab[(name, 12, "MC-A", 4)][0] - tab[(name, 12, "MC-A", 1)][0]
        note = "  gate==off (structural)" if len(gmap[name]) == 6 else ""
        print(f"   {name:>8}: off {so:+6.1f}  gate {sg:+6.1f}  MC-A {sm:+6.1f}"
              f"{note}")
    return tab


# ---------------------------------------------------------------- EXP 3
def exp3(theta_star):
    print(f"\n== EXP 3: AS x gate@{theta_star} composition — N=7 supra-wall"
          f" grammars, pd=3, delta=12, K in {{1,2}} (P16a pre-registered) ==")
    grams = (
        ("step5", ladder_step(30, 5), None),          # AS no-op control
        ("kcoh1w7", [0] * 6 + [30], [0, 1, 2, 3, 4, 5, 30]),
        ("cohort37", [0, 0, 0, 30, 30, 30, 30], [0, 1, 2, 27, 28, 29, 30]),
        ("zero7", [0] * 7, [0, 1, 2, 3, 4, 5, 6]),
    )
    tab = {}
    for name, blats, alats in grams:
        if alats is None:
            alats = blats
        for k in (1, 2):
            b = gcell(blats, K=k, gate="never")
            a = gcell(alats, K=k, gate="never")
            g = gcell(blats, K=k, gate=theta_star)
            j = gcell(alats, K=k, gate=theta_star)
            tab[(name, k)] = (b, a, g, j)
            starved = all(r["gopen"] == 0 for r in j["rs"])
            byteq = ""
            if starved:
                byteq = (" ≡AS byte-level" if all(
                    mkeys(j["rs"][i]) == mkeys(a["rs"][i])
                    for i in range(len(SEEDS))) else " STARVED-but-not-AS?!")
            print(f"  {name:>8} K={k}: base {show(b)}  AS {show(a)}"
                  f"  gate {show(g)}  AS+gate {show(j)}"
                  f"  gOpen {g['gopen']:8.1f}->{j['gopen']:8.1f}{byteq}")

    print("\n  P16a residual analysis (qualify: BOTH singles >= base + 5.0):")
    nq = 0
    bad = []
    for key in sorted(tab):
        b, a, g, j = tab[key]
        ga, gg = a["m"] - b["m"], g["m"] - b["m"]
        if ga >= 5.0 and gg >= 5.0:
            nq += 1
            r = j["m"] - max(a["m"], g["m"])
            wit = (j["gopen"] <= 0.1 * g["gopen"]) if g["gopen"] > 0 else True
            tag = ("band" if -2.0 <= r <= 2.0
                   else ("SUPER" if r > 2.0 else "SUB"))
            if tag != "band" or not wit:
                bad.append((key, tag, wit))
            print(f"   {key[0]:>8} K={key[1]}: gains AS {ga:+6.1f} gate {gg:+6.1f}"
                  f" -> residual {r:+6.1f} [{tag}]  starvation-witness "
                  f"{'OK' if wit else 'FAIL'} ({j['gopen']:.0f} vs {g['gopen']:.0f})")
        else:
            print(f"   {key[0]:>8} K={key[1]}: gains AS {ga:+6.1f} gate {gg:+6.1f}"
                  f" — not qualifying")
    if nq == 0:
        print("   NO qualifying cells — P16a untestable on this grid (booked)")
    else:
        print(f"  P16a (residual in [-2,+2] on all qualifying cells, "
              f"starvation witness): {'PASS' if not bad else 'FAIL'} "
              f"({nq - len(bad)}/{nq} in band)"
              + (f"; violations: {bad}" if bad else ""))

    for k in (1, 2):
        b = tab[("zero7", k)][0]
        print(f"  wall-law probe: zero7 base K={k} = {b['m']:.1f}"
              f"{'D' if b['div'] else ''} — N>2pd at span 6 "
              f"{'diverges (wall survives low spread)' if b['div'] else 'does NOT diverge (wall is spread-dependent)'}")
    return tab


def main():
    print(__doc__)
    print("=" * 70)
    print("SPIN 16 — PULSE-DIAL II: ADAPTIVE (ECHO-GATED) COMPENSATION"
          " — harness run, -u, no pipes")
    if "--canaries" in sys.argv:
        canaries()
        return
    if not canaries():
        print("CANARY FAIL — aborting")
        sys.exit(1)
    theta_star, miss, _ = exp1()
    exp2(theta_star)
    exp3(theta_star)
    x = 486256185   # current ledger head (proposal-dispatched: no pick consumed)
    x2 = (1103515245 * x + 12345) & 0x7FFFFFFF
    print(f"\nLCG ritual: proposal-dispatched spin (SPIN-11's Next proposal) —"
          f" no pick consumed; ledger head 486256185; next selection reference:"
          f" 486256185 -> {x2} -> mod 10 = {x2 % 10}")


if __name__ == "__main__":
    main()
