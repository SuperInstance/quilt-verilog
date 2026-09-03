#!/usr/bin/env python3
"""SPIN 25 — THRESHOLD CAUSAL + BEST-THETA (pre-reg in SPIN-25-threshold-causal.md).

(a) exact nf=6-only toggle at pd=3, K=1: t100=99 (IN) vs t100=100 (OUT).
    Arithmetic: at pd=3 every other nf threshold is <=66 (nf 1,2,4,5) or
    >=133 (nf 7), so 99 vs 100 differ ONLY in nf=6 admission.
(b) t100 in {67,75,80,85,90,95,99}: sha-distinctness FIRST, then panel +
    step5 rescue on distinct classes only.
Reuses spin24 machinery verbatim (spin16 run_fabric_gate, panel, canaries).
Integer-only in-loop; python3 -u, no pipes.
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
T0 = time.time()

PANEL = (
    ("kcoh5@15", [0, 0, 0, 0, 0, 15], 1),
    ("ladder30", ladder(30), 1),
    ("step5K1", ladder_step(30, 5), 1),
    ("step5K2", ladder_step(30, 5), 2),
    ("zero7", [0] * 7, 1),
)
HEALTHY = ("kcoh5@15", "ladder30", "zero7")
RESCUE = ("step5K1", "step5K2")
T_SWEEP = (67, 75, 80, 85, 90, 95, 99)


def sha(r):
    h = hashlib.sha256()
    for k in ("events", "mass", "cancels", "chatter", "settles",
              "resid", "cflags", "emissions", "gopen", "gcomp"):
        h.update(repr((k, r.get(k))).encode())
    return h.hexdigest()[:16]


def pct(r):
    return within_pm(r["resid"], EV) / 10.0


def cell(lats, k, gate, seeds=S3):
    v = 0.0
    for s in seeds:
        v += pct(run_fabric_gate("interference", TICKS, lats, K=k, pd=3,
                                 delta=12, drift=6, seed=s, gate=gate))
    return v / len(seeds)


# ---------- spin23 clones (canary 3 only) ----------------------------
def dyn_run_fn(lats_fn, reality_fn, ticks=TICKS, k=4, pd=3, delta=12,
              drift=6, seed=20260902):
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


def mean(v):
    return sum(v) / len(v)


def ladder6(s):
    return [round(i * s / 5) for i in range(6)]


def square_schedule(P, lo, hi, duty100=50, ticks=TICKS):
    hi_ticks = P * duty100 // 100
    return [hi if (t % P) >= P - hi_ticks else lo for t in range(ticks)]


_pc = {}


def plpct(lats, k, sd):
    key = (tuple(lats), k, sd)
    if key not in _pc:
        _pc[key] = within_pm(
            dyn_run_fn((lambda t, L=lats: L), r3_plateau, k=k, pd=3,
                       seed=sd), 12) / 10.0
    return _pc[key]


def oscpct(sched, k, sd):
    key = ("osc", tuple(sched[:64]), k, sd)
    if key not in _pc:
        def fn(t, S=sched):
            return ladder6(S[t])
        _pc[key] = within_pm(dyn_run_fn(fn, r3_plateau, k=k, pd=3,
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
    osc = mean([oscpct(sched, 2, sd) for sd in S3])
    twm = mean([0.5 * plpct(ladder6(5), 2, sd)
                + 0.5 * plpct(ladder6(30), 2, sd) for sd in S3])
    tax = twm - osc
    g = tax >= 36.0
    print(f"  TWmean tax = {tax:.1f}pp (booked 36.7) "
          f"{'PASS' if g else 'FAIL'}")
    ok &= g
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- part (a)
def part_a():
    print("\n== PART A: nf=6-only toggle at pd=3, K=1 (t100=99 IN vs 100 OUT) ==")
    print("arithmetic: at pd=3 other nf thresholds: nf1,nf5<=66; "
          "nf2,nf4<=33; nf7<=133 -> 99 vs 100 differ ONLY in nf=6.")
    names = ("kcoh5@15", "ladder30", "zero7")
    latsmap = {n: l for n, l, k in PANEL}
    rows = []
    for n in names:
        vin = cell(latsmap[n], 1, 0.99)
        vout = cell(latsmap[n], 1, 1.0)
        # per-seed sha identity check between the two toggle arms
        sh_same = True
        for s in S3:
            ri = sha(run_fabric_gate("interference", TICKS, latsmap[n],
                                     K=1, pd=3, seed=s, gate=0.99))
            ro = sha(run_fabric_gate("interference", TICKS, latsmap[n],
                                     K=1, pd=3, seed=s, gate=1.0))
            sh_same &= (ri == ro)
        d = vin - vout
        rows.append((n, vout, vin, d, sh_same))
        tag = "healthy" if n != "kcoh5@15" else "target "
        print(f"  {n:9s} [{tag}]  OUT(100)={vout:5.1f}  IN(99)={vin:5.1f}  "
              f"delta={d:+5.1f}pp  arm-sha-identical={'Y' if sh_same else 'N'}")
    tgt = rows[0][3]
    healthy_ok = all(abs(r[3]) <= 1.0 and r[4] for r in rows[1:])
    causal = tgt >= 5.0
    print(f"\n  kcoh5@15 delta {tgt:+.1f}pp -> reproduces booked +7.9: "
          f"{'YES' if causal else 'NO'} (rule: >= +5pp)")
    print(f"  healthy anchors (ladder30, zero7): "
          f"{'INERT (|d|<=1pp and arm-sha-identical)' if healthy_ok else 'LEVEL COSTS — SEE TABLE'}")
    print(f"  PART A VERDICT: "
          f"{'CAUSAL + HEALTHY-INERT' if (causal and healthy_ok) else 'NOT healthy-inert / not causal — booked'}")
    return causal, healthy_ok


# ---------------------------------------------------------------- part (b)
def part_b():
    print("\n== PART B: t100 sweep {67,75,80,85,90,95,99} — sha distinctness FIRST ==")
    latsmap = {n: (l, k) for n, l, k in PANEL}
    # class by full signature of shas over (panel anchor, seed)
    sig = {}
    for t in T_SWEEP:
        s_list = []
        for n, (l, k) in latsmap.items():
            for s in S3:
                s_list.append(sha(run_fabric_gate(
                    "interference", TICKS, l, K=k, pd=3, seed=s,
                    gate=t / 100)))
        sig[t] = tuple(s_list)
    classes = {}
    for t in T_SWEEP:
        classes.setdefault(sig[t], []).append(t)
    print(f"  distinct behavioral classes: {len(classes)}")
    for i, (sg, ts) in enumerate(classes.items()):
        print(f"    class {i}: t100={ts}  sha-prefix={sg[0]}")
    if len(classes) == 1:
        print("  (matches PREDICTION P-b: admission set {nf6,nf7} identical "
              "across [67,99])")

    print("\n  -- panel pct per distinct class (pd=3, seeds {1,7,42}) --")
    best = None
    for i, (sg, ts) in enumerate(classes.items()):
        t = ts[0]
        vals = {n: cell(l, k, t / 100) for n, (l, k) in latsmap.items()}
        never = {n: cell(l, k, "never") for n, (l, k) in latsmap.items()}
        rescue = mean([vals[n] - never[n] for n in RESCUE])
        # eligibility: healthy anchors byte-identical to never + no regress
        elig = True
        for n in HEALTHY:
            for s in S3:
                l, k = latsmap[n]
                elig &= (sha(run_fabric_gate("interference", TICKS, l, K=k,
                                             pd=3, seed=s, gate=t / 100))
                         == sha(run_fabric_gate("interference", TICKS, l,
                                                K=k, pd=3, seed=s,
                                                gate="never")))
            elig &= (vals[n] >= never[n] - 1.0)
        row = " ".join(f"{n}={vals[n]:5.1f}(nv {never[n]:5.1f})"
                       for n in vals)
        print(f"    class {i} (rep t100={t}): rescue={rescue:+5.1f}pp "
              f"eligible={'Y' if elig else 'N'}  {row}")
        if elig and (best is None or rescue > best[1]):
            best = (t, rescue)
    if best:
        print(f"\n  BEST EMBEDDED theta: t100={best[0]} (representative; "
              f"rescue {best[1]:+.1f}pp)")
        if len(classes) == 1:
            print("  -> theta-INDEPENDENT across [67,99]; representative is "
                  "bookkeeping (ties broken by simplest/lowest)")
    else:
        print("\n  NO eligible class — booked as failure of embedded rule")
    return classes, best


def main():
    print("SPIN-25 THRESHOLD CAUSAL + BEST-THETA —",
          time.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"panel seeds {S3}; ticks {TICKS}; pd=3; delta/drift 12/6; EV=12")
    if not canaries():
        sys.exit(1)
    a = part_a()
    b = part_b()
    print(f"\nSUMMARY: (a) causal={a[0]} healthy-inert={a[1]}  "
          f"(b) classes={len(b[0])} best={b[1]}")
    print(f"DONE. elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
