#!/usr/bin/env python3
"""SPIN 3, SPOKE 4: TOPOLOGY — is the F7 bundle-capacity wall a function of
(K, twin-geometry), not a fabric constant?

Fabric: exp_glm1.run_fabric (E1 contract: fdiv decay, 64-bit LCG, FIFO
oldest-first expiry, snapshot decay). Integer-only inside the loop.

Operationalization of "topology": the wall in F7 was created by *staggered*
latencies 0,10,20,...,10(N-1) — every twin mutually stale (all-to-all
disagreement). We sweep three twin geometries as latency patterns:

  all_to_all : [0,10,20,...,10(N-1)]  — every pair disagrees (F7 baseline)
  ring       : [0,10,0,10,...]        — only ring-ADJACENT twins disagree;
                                         distant twins cohere (local geometry)
  star       : [0,10,10,...,10]       — one fresh hub, one coherent stale
                                         cohort of leaves

At N=1 and N=2 all three collapse to [0] / [0,10] — a built-in self-canary:
metrics MUST be identical across topologies there, else the name map is wrong.

Second canary: K=4, all_to_all must reproduce F7's table (interference true%
91.0/34.5/12.2 at N=2/3/4, events ~2041 at N=2).

Sweep: N in 1..6 x K in {1,2,8} x topology in {all_to_all, ring, star},
interference arm, 5 fixed seeds, 4800 ticks, stress params (delta=12,
drift=6, pd=3). Sequential reference arm per (N, topology) — K-independent.
"""
import sys
sys.path.insert(0, "inventors-derby")
from exp_glm1 import run_fabric, within_pm  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12


def latencies(topo, n):
    if topo == "all_to_all":
        return [10 * i for i in range(n)]
    if topo == "ring":
        return [0 if i % 2 == 0 else 10 for i in range(n)]
    if topo == "star":
        return [0] + [10] * (n - 1)
    raise ValueError(topo)


def one(mode, topo, n, k, seed):
    r = run_fabric(mode, 4800, latencies(topo, n), K=k, pd=3,
                   delta=DELTA, drift=6, seed=seed)
    return dict(true_pm=within_pm(r["resid"], DELTA),
                all_pm=1000 * r["settles"] // r["ticks"],
                events=r["events"], debt=r["mass"],
                cancels=r["cancels"])


def mean(vals):
    return sum(vals) / len(vals)  # display only


def row(cells):
    return " | ".join(f"{c:>8}" for c in cells)


TOPOS = ("all_to_all", "ring", "star")


def main():
    # ---- canary 1: N<=2 topologies identical ----
    print("== CANARY 1: N<=2 must be identical across topologies ==")
    ok = True
    for n in (1, 2):
        for k in (1, 2, 8):
            base = one("interference", "all_to_all", n, k, SEEDS[0])
            for topo in ("ring", "star"):
                other = one("interference", topo, n, k, SEEDS[0])
                if base != other:
                    ok = False
                    print(f"  MISMATCH n={n} k={k} all_to_all vs {topo}:",
                          base, other)
    print("  PASS: N<=2 identical across all 3 topologies x K" if ok
          else "  FAIL")

    # ---- canary 2: reproduce F7 at K=4 all_to_all ----
    print("== CANARY 2: F7 replay (K=4, all_to_all, mean of 5 seeds) ==")
    print(row(["N", "true%", "events", "F7true%", "F7ev"]))
    f7 = {2: (91.0, 2041), 3: (34.5, 6415), 4: (12.2, 10408),
          5: (9.7, 15025), 6: (9.9, 19338)}
    ok2 = True
    for n in range(2, 7):
        res = [one("interference", "all_to_all", n, 4, s) for s in SEEDS]
        tp = mean([r["true_pm"] for r in res]) / 10
        ev = mean([r["events"] for r in res])
        match = abs(tp - f7[n][0]) <= 0.15 and abs(ev - f7[n][1]) <= 15
        ok2 &= match
        print(row([n, f"{tp:.1f}", f"{ev:.0f}", f7[n][0], f7[n][1]])
              + ("  OK" if match else "  DRIFT"))
    print("  F7 replay OK" if ok2 else "  F7 replay DRIFTED — investigate")

    # ---- main sweep ----
    print("\n== MAIN: interference, per-seed true-residency permille ==")
    print(row(["N", "K", "topo", "s1", "s7", "s42", "s1999", "s2s260902",
               "mean%", "allW", "evMean", "debtMean", "canc"]))
    for n in range(1, 7):
        for k in (1, 2, 8):
            for topo in TOPOS:
                res = [one("interference", topo, n, k, s) for s in SEEDS]
                tp = [r["true_pm"] for r in res]
                print(row([n, k, topo] + tp +
                          [f"{mean(tp)/10:.1f}",
                           f"{mean([r['all_pm'] for r in res])/10:.1f}",
                           f"{mean([r['events'] for r in res]):.0f}",
                           f"{mean([r['debt'] for r in res]):.0f}",
                           f"{mean([r['cancels'] for r in res]):.0f}"]))

    # ---- sequential reference (K-independent) ----
    print("\n== REFERENCE: sequential arm (T1-priority), mean of 5 seeds ==")
    print(row(["N", "topo", "true%", "allW", "events", "debt"]))
    for n in range(1, 7):
        for topo in TOPOS:
            res = [one("sequential", topo, n, 1, s) for s in SEEDS]
            print(row([n, topo,
                       f"{mean([r['true_pm'] for r in res])/10:.1f}",
                       f"{mean([r['all_pm'] for r in res])/10:.1f}",
                       f"{mean([r['events'] for r in res]):.0f}",
                       f"{mean([r['debt'] for r in res]):.0f}"]))


if __name__ == "__main__":
    main()
