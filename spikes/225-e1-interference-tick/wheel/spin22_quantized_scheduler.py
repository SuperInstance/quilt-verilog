#!/usr/bin/env python3
"""SPIN 22 — QUANTIZED SCHEDULER (SPIN-20 question #3).
Does quantizing the echo-gate theta onto a 4/8/16-level ladder across the
useful band (theta in (1, 4/3) at pd=3) help or hurt vs continuous theta*=1.1?
Fabric: spin16 run_fabric_gate reused verbatim (integer-only in-loop gate
100*|pd-nf| > t100*pd). Panel/cells/prediction/decision rule/canaries are
PRE-REGISTERED in SPIN-22-quantized-scheduler.md (committed before this run).
Seeds {1,7,42} for the panel; canary (2) uses the 5-seed anchor set so the
published 71.5 is directly checked. Single-pass inline; python3 -u; no pipes.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "inventors-derby"))
sys.path.insert(0, HERE)
from exp_glm1 import within_pm  # noqa: E402
from spin11_pulse_dial import ladder, ladder_step  # noqa: E402
from spin16_pulse_dial2 import run_fabric_gate, mean, SEEDS  # noqa: E402

TICKS = 4800
EV = 12
S3 = (1, 7, 42)
CONT = 110  # t100 for theta* = 1.1 (spin-16 corrected calibration)


def sha(r):
    h = hashlib.sha256()
    for k in ("events", "mass", "cancels", "chatter", "settles",
              "resid", "cflags", "emissions", "gopen", "gcomp"):
        h.update(repr((k, r[k])).encode())
    return h.hexdigest()[:16]


def cell(lats, t100, K=1, seeds=S3):
    rs = [run_fabric_gate("interference", TICKS, lats, K=K, pd=3, delta=12,
                          drift=6, seed=s, gate=t100 / 100) for s in seeds]
    t12 = [within_pm(r["resid"], EV) for r in rs]
    return (mean(t12) / 10, [sha(r) for r in rs])


PANEL = [
    ("kcoh5@15", [0, 0, 0, 0, 0, 15], 1),
    ("ladder30", ladder(30), 1),
    ("step5K1", ladder_step(30, 5), 1),
    ("step5K2", ladder_step(30, 5), 2),
    ("zero7", [0] * 7, 1),
]


def ladder_levels(L, lo=100, hi=133):
    return sorted({lo + round((i + 0.5) * (hi - lo) / L) for i in range(L)})


def main():
    ok = True
    print("== CANARY 1: spread=0 byte-identity, kcoh5 gate==off ==")
    r_never = [run_fabric_gate("interference", TICKS, [0] * 5 + [0], K=1,
                               seed=s, gate="never") for s in S3]
    r_theta = [run_fabric_gate("interference", TICKS, [0] * 5 + [0], K=1,
                               seed=s, gate=1.1) for s in S3]
    b1 = [sha(r) for r in r_never]
    b2 = [sha(r) for r in r_theta]
    dual = [sha(dict(r)) for r in
            [run_fabric_gate("interference", TICKS, [0] * 5 + [0], K=1,
                             seed=s, gate="never") for s in S3]]
    g1 = b1 == b2
    g2 = b1 == dual
    print(f"  kcoh5@0 gate(never)==gate(1.1) full-dict sha: "
          f"{'IDENTICAL' if g1 else 'DIFFER'}; dual-run: "
          f"{'IDENTICAL' if g2 else 'DIFFER'}")
    ok &= g1 and g2

    print("\n== CANARY 2: ladder@15 K=1 = 71.5 exact (5-seed anchor) ==")
    v, _ = cell(ladder(15), "never", seeds=SEEDS)
    g = abs(v - 71.5) <= 0.2
    ok &= g
    print(f"  got {v:.1f}  want 71.5  {'OK' if g else 'DRIFT'}")

    print("\n== CANARY 3: zero7 gate = 99.8 anchor ==")
    v, _ = cell([0] * 7, 1.1)
    g = abs(v - 99.8) <= 0.2
    ok &= g
    print(f"  got {v:.1f}  want 99.8  {'OK' if g else 'DRIFT'}")
    print(f"CANARIES: {'ALL PASS' if ok else 'FAIL - ABORT'}")
    if not ok:
        sys.exit(1)

    print("\n== PANEL: quantized ladder vs continuous theta*=1.10 (t100=110) ==")
    ref = {}
    for name, lats, K in PANEL:
        m, hs = cell(lats, CONT, K)
        ref[name] = (m, hs)
        print(f"  ref {name:<9} K={K} continuous 1.10: true12 {m:5.1f}")

    print(f"\n{'levels':>5} {'t100':>5} {'theta':>6} | " +
          " | ".join(f"{n:>9}" for n, _, _ in PANEL))
    worst = {n: 0.0 for n, _, _ in PANEL}
    bite = {}
    for L in (4, 8, 16):
        for t in ladder_levels(L):
            row = []
            for name, lats, K in PANEL:
                m, hs = cell(lats, t, K)
                d = m - ref[name][0]
                worst[name] = min(worst[name], d)
                byte = "==" if hs == ref[name][1] else "!="
                if d < -1.0:
                    bite.setdefault(name, []).append((L, t, d))
                row.append(f"{m:5.1f}{byte}{d:+5.1f}")
            print(f"{L:>5} {t:>5} {t/100:>6.2f} | " + " | ".join(
                f"{c:>9}" for c in row))

    print("\n== OUT-OF-BAND PROBES on step5K1 (where does quantization bite?) ==")
    for t in (99, 100, 134):
        m, hs = cell(ladder_step(30, 5), t)
        d = m - ref["step5K1"][0]
        byte = "==" if hs == ref["step5K1"][1] else "!="
        print(f"  t100={t} (theta {t/100:.2f}): true12 {m:5.1f} {byte} "
              f"({d:+.1f}pp vs continuous)")

    print("\n== VERDICT INPUTS ==")
    for name, _, _ in PANEL:
        s = "GO-side" if worst[name] >= -1.0 else "NO-GO-side"
        print(f"  {name:<9} worst delta vs continuous: {worst[name]:+.1f}pp "
              f"-> {s}")
        if name in bite:
            for L, t, d in bite[name]:
                print(f"    bites at L={L} t100={t} ({d:+.1f}pp)")
    print("\nByte-identity claim: every in-band cell reports '==' iff "
          "full-dict sha matches the continuous reference per seed.")


if __name__ == "__main__":
    main()
