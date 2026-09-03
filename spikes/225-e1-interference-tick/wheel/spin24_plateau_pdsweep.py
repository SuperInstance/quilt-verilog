#!/usr/bin/env python3
"""SPIN 24 — PLATEAU PD-SWEEP (pre-registration in SPIN-24-plateau-pdsweep.md).

(a) gate-crossing count vs pd in {1..8} on the SPIN-22 anchor panel
    (spin16 run_fabric_gate reused verbatim; integer gate test
    100*|pd-nf| > t100*pd).
(b) plateau-only K=2 wall vs pd: zero grammar [0]*N, N swept, wall_edge vs
    2pd+1 (spin21 plateau trace + spin23 dyn_run/tax clones).
Panel seeds {1,7,42}; canary anchors use the 5-seed set.
Integer-only in-loop; floats only at aggregation/print. python3 -u, no pipes.
"""
import hashlib
import os
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
sys.path.insert(0, HERE)
from exp_glm1 import within_pm, LCG, reality  # noqa: E402
from spin11_pulse_dial import ladder, ladder_step  # noqa: E402
from spin16_pulse_dial2 import run_fabric_gate  # noqa: E402
from spin21_reality_variation import r3_plateau  # noqa: E402

TICKS = 4800
EV = 12
S3 = (1, 7, 42)
S5 = (1, 7, 42, 1999, 20260902)
PDS_A = tuple(range(1, 9))
PDS_B = (1, 2, 3, 4, 6, 8)
T0 = time.time()

PANEL = (
    ("kcoh5@15", [0, 0, 0, 0, 0, 15], 1),
    ("ladder30", ladder(30), 1),
    ("step5K1", ladder_step(30, 5), 1),
    ("step5K2", ladder_step(30, 5), 2),
    ("zero7", [0] * 7, 1),
)


def sha(r):
    h = hashlib.sha256()
    for k in ("events", "mass", "cancels", "chatter", "settles",
              "resid", "cflags", "emissions", "gopen", "gcomp"):
        h.update(repr((k, r.get(k))).encode())
    return h.hexdigest()[:16]


def pct(r):
    return within_pm(r["resid"], EV) / 10.0


def cell(lats, k, pd, t100, seeds=S3):
    """mean pct on the gate fabric at one (pd, t100)."""
    v = 0.0
    for s in seeds:
        r = run_fabric_gate("interference", TICKS, lats, K=k, pd=pd,
                            delta=12, drift=6, seed=s, gate=t100 / 100)
        v += pct(r)
    return v / len(seeds)


# -------- spin23 dyn_run/tax clones (part b + canary 3) --------------
def dyn_run_fn(lats_fn, reality_fn, ticks=TICKS, k=4, pd=3, delta=12,
              drift=6, seed=20260902):
    """spin23 dyn_run clone with per-tick grammar (spin-21 form)."""
    rng = LCG(seed)
    g = reality_fn(0)
    pulses = deque()
    resid = []
    for t in range(ticks):
        lats = lats_fn(t)
        reads = [reality_fn(max(0, t - lats[i])) for i in range(len(lats))]
        s_true = reality_fn(t)
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > delta]
        for i, e in trig:
            m = abs(e) // pd or 1
            pulses.appendleft([m if e > 0 else -m, k])
        if pulses:
            net = sum(p[0] for p in pulses)
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
        resid.append(abs(s_true - g))
    return resid


def dyn_run(lats, reality_fn, ticks=TICKS, k=4, pd=3, delta=12, drift=6,
            seed=20260902):
    return dyn_run_fn((lambda t, L=lats: L), reality_fn, ticks, k, pd,
                      delta, drift, seed)


def mean(v):
    return sum(v) / len(v)


def ladder6(s):
    return [round(i * s / 5) for i in range(6)]


def square_schedule(P, lo, hi, duty100=50, ticks=TICKS):
    hi_ticks = P * duty100 // 100
    sched = []
    for t in range(ticks):
        in_hi = (t % P) >= P - hi_ticks
        sched.append(hi if in_hi else lo)
    return sched


def sched_fn(sched):
    return lambda t, S=sched: ladder6(S[t])


def static6(s):
    return lambda t, L=ladder6(s): L


_pc = {}
_PLATEAU_FN = r3_plateau


def plpct(lats, k, sd, pd):
    key = (tuple(lats), k, sd, pd)
    if key not in _pc:
        _pc[key] = within_pm(dyn_run(lats, _PLATEAU_FN, k=k, pd=pd,
                                     seed=sd), 12) / 10.0
    return _pc[key]


def oscpct(sched, k, sd, pd, tag=""):
    """scheduled (time-varying) grammar — spin23 osc() clone."""
    key = ("osc", tag, tuple(sched[:64]), len(sched), k, sd, pd)
    if key not in _pc:
        def fn(t, S=sched):
            return ladder6(S[t])
        _pc[key] = within_pm(dyn_run_fn(fn, _PLATEAU_FN, k=k, pd=pd,
                                       seed=sd), 12) / 10.0
    return _pc[key]


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY 1: spread=0 byte-identity, kcoh5@0 gate modes ==")
    hs = {}
    for mode in ("never", 1.1, "never2"):
        gate = "never" if mode == "never2" else mode
        hs[mode] = [sha(run_fabric_gate("interference", TICKS, [0] * 6,
                                        K=1, seed=s, gate=gate))
                    for s in (1, 42)]
    g = hs["never"] == hs[1.1] == hs["never2"]
    print(f"  never==theta1.1==dual-run shas: {'PASS' if g else 'FAIL'}")
    ok &= g

    print("\n== CANARY 2: ladder@15 K=1 = 71.5 exact (5-seed, R0) ==")
    v = mean([pct(run_fabric_gate("interference", TICKS, ladder(15), K=1,
                                  seed=s, gate="never")) for s in S5])
    g = abs(v - 71.5) <= 0.2
    print(f"  got {v:.1f}  want 71.5  {'PASS' if g else 'FAIL'}")
    ok &= g

    print("\n== CANARY 3: plateau K=2 tax >= 36pp at SPIN-23 anchor ==")
    sched = square_schedule(16, 5, 30, 50)
    osc = mean([oscpct(sched, 2, sd, 3, "c3") for sd in S3])
    twm = mean([0.5 * plpct(ladder6(5), 2, sd, 3)
                + 0.5 * plpct(ladder6(30), 2, sd, 3) for sd in S3])
    tax = twm - osc
    g = tax >= 36.0
    print(f"  TWmean tax = {tax:.1f}pp (SPIN-23 booked 36.7) "
          f"{'PASS' if g else 'FAIL'}")
    ok &= g
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- part (a)
def part_a():
    print("\n== PART A: crossing map vs pd (N=7 twins; t100 dial) ==")
    print("T_nf = 100*|pd-nf|/pd; nf admitted at t100 <= (100|pd-nf|-1)//pd;")
    print("band = (100*(1-1/pd), 100*(1+1/pd)].")
    multilevel = []
    for pd in PDS_A:
        b_lo = 100 * (pd - 1) / pd
        b_hi = 100 * (pd + 1) / pd
        lo_i = int(b_lo) + 1
        hi_i = int(b_hi) if b_hi != int(b_hi) else int(b_hi)
        rows = []
        cands = set(range(max(1, lo_i), hi_i + 1))
        for nf in range(1, 8):
            if nf == pd:
                continue
            tnum = 100 * abs(pd - nf)
            c = (tnum - 1) // pd          # max admitting t100
            T = tnum / pd
            inb = b_lo < T <= b_hi
            rows.append((nf, T, c, inb))
            cands.update((c, c + 1))
        cands = sorted(x for x in cands if 1 <= x <= 400)
        res = {}
        for t in cands:
            res[t] = {name: cell(lats, k, pd, t) for name, lats, k in PANEL}
        n_inband = sum(1 for nf, T, c, inb in rows if inb)
        print(f"\n-- pd={pd}  band t100 ({b_lo:.1f}, {b_hi:.1f}] "
              f"int [{lo_i}..{hi_i}]  in-band crossings: {n_inband}")
        for nf, T, c, inb in rows:
            mark = "*" if inb else " "
            print(f"  nf={nf}: T={T:6.1f} maxadmit={c:3d} "
                  f"inband={'Y' if inb else 'n'}{mark}")
        # distinguishability among in-band integer t100 settings
        inb_ts = [t for t in cands if lo_i <= t <= hi_i]
        best = 0.0
        bestpair = None
        for i in range(len(inb_ts)):
            for j in range(i + 1, len(inb_ts)):
                for name, _, _ in PANEL:
                    d = abs(res[inb_ts[i]][name] - res[inb_ts[j]][name])
                    if d > best:
                        best = d
                        bestpair = (inb_ts[i], inb_ts[j], name,
                                    res[inb_ts[i]][name], res[inb_ts[j]][name])
        verdict = "MULTI-LEVEL" if (n_inband >= 2 and best > 1.0) else \
                  "one-level"
        print(f"  in-band t100 range spread {len(inb_ts)} settings; "
              f"best in-band pct delta {best:.2f}pp "
              f"{('at ' + str(bestpair[:3]) + f' {bestpair[3]:.1f} vs {bestpair[4]:.1f}') if bestpair else ''}"
              f" -> {verdict}")
        if verdict == "MULTI-LEVEL":
            multilevel.append(pd)
        # reference row (theta=1.1) and nf-side probes for the table
        for t in sorted(set([c for _, _, c, _ in rows] + [c + 1 for _, _, c, _ in rows])):
            if t in res:
                vals = " ".join(f"{res[t][n]:5.1f}" for n, _, _ in PANEL)
                tag = "inband" if lo_i <= t <= hi_i else "probe "
                print(f"  t100={t:3d} {tag}: {vals}")
    print("\nPART A VERDICT:",
          f"MULTI-LEVEL at pd={multilevel}" if multilevel
          else "one-level at every pd (no pd has >=2 distinguishable "
               "in-band crossings)")
    return not multilevel


# ---------------------------------------------------------------- part (b)
def part_b():
    print("\n== PART B: plateau wall vs pd (zero grammar [0]*N, K=2) ==")
    print("wall_edge = smallest N with mean pct < ref-10pp; ratio vs 2pd+1;")
    print("flag if ratio outside [0.8, 1.25].")
    ratios = {}
    for pd in PDS_B:
        nmax = min(2 * pd + 4, 20)
        vals = {}
        for n in range(1, nmax + 1):
            vals[n] = mean([plpct([0] * n, 2, sd, pd) for sd in S3])
        ref = max(vals.values())
        edge = None
        for n in range(1, nmax + 1):
            if vals[n] < ref - 10.0:
                edge = n
                break
        row = " ".join(f"N{n}:{vals[n]:5.1f}" for n in range(1, nmax + 1))
        print(f"\n-- pd={pd} (2pd+1={2*pd+1}) ref={ref:.1f}  {row}")
        if edge is None:
            print(f"  no collapse within sweep (N<= {nmax}); "
                  f"wall beyond sweep")
        else:
            r = edge / (2 * pd + 1)
            ratios[pd] = r
            flag = "" if 0.8 <= r <= 1.25 else "  <-- FLAG (outside 0.8-1.25)"
            print(f"  wall_edge={edge}  ratio={r:.3f}{flag}")
    mv = sorted(ratios)
    nondec = all(ratios[mv[i]] <= ratios[mv[i + 1]] + 1e-9
                 for i in range(len(mv) - 1))
    inc = sum(1 for i in range(len(mv) - 1)
              if ratios[mv[i + 1]] > ratios[mv[i]] + 1e-9)
    allin = all(0.8 <= r <= 1.25 for r in ratios.values())
    print(f"\nwall ratios: "
          + " ".join(f"pd{p}={ratios[p]:.3f}" for p in mv))
    print(f"moves with pd: {'YES' if (nondec and inc >= 2) else 'NO'} "
          f"(non-decreasing={nondec}, strict increases={inc})")
    print(f"sits at m~1 (all ratios in [0.8,1.25]): "
          f"{'YES' if allin else 'NO'}")
    return nondec and inc >= 2 and allin


def main():
    print("SPIN-24 PLATEAU PD-SWEEP —", time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"panel seeds {S3}; ticks {TICKS}; delta/drift 12/6; EV=12")
    if not canaries():
        sys.exit(1)
    a = part_a()
    b = part_b()
    print(f"\nSUMMARY: (a) one-level-everywhere={a}  (b) wall-at-m1={b}")
    print(f"DONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
