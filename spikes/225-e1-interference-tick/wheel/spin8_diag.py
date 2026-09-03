#!/usr/bin/env python3
"""SPIN 8 diagnostic: name the mechanism behind the step<=5 collapse in EXP 1.

Hypothesis to test: dense ladders put MANY twins inside the trigger band
simultaneously; the per-tick net shove (sum of e//3 pulses) exceeds delta,
overshoots onto its own echo, and locks into a divergent sign-alternating
oscillation (zero-lock chatter generalized to a staggered band). The
step5(N=7) vs step6(N=6) cliff at K=1 (0.3% vs 26.8%) should then show as a
jump in same-tick firing multiplicity / net shove magnitude.
Integer-only in-loop; floats display-only.
"""
import sys
sys.path.insert(0, "inventors-derby")
from exp_glm1 import run_fabric  # noqa: E402


def diag(step, k=1, seed=1):
    lats = list(range(0, 31, step))
    r = run_fabric("interference", 4800, lats, K=k, pd=3, delta=12,
                   drift=6, seed=seed)
    em = r["emissions"]
    by_tick = {}
    for (t, i, pm, e) in em:
        by_tick.setdefault(t, []).append(pm)
    mult = [len(v) for v in by_tick.values()]
    nets = {t: sum(v) for t, v in by_tick.items()}
    # recompute applied net per tick is not in ledger; use fire-tick net sum
    ts = sorted(nets)
    flips = sum(1 for a, b in zip(ts, ts[1:]) if nets[a] * nets[b] < 0)
    resid = r["resid"]
    # NOTE: integer-only means; net magnitudes can exceed float range when
    # the band oscillation diverges (itself a mechanism finding).
    tot_net = sum(abs(nets[t]) for t in ts)
    mean_net = tot_net // max(1, len(ts))
    max_net = max((abs(nets[t]) for t in ts), default=0)
    mean_resid = sum(resid) // len(resid)
    big = 1000 * sum(1 for x in resid if x > 60) // len(resid)
    mn = min(mean_net, 10**18)
    mx = min(max_net, 10**18)
    mr = min(mean_resid, 10**18)
    print(f"step{step:>2} N={len(lats):>2} K={k}: trig/tick "
          f"{r['events']/4800:.2f}  eventTicks {len(by_tick):>4}  "
          f"meanMult {sum(mult)/max(1,len(mult)):.2f}  maxMult {max(mult) if mult else 0:>2}  "
          f"meanFireNet {mn}  maxFireNet {mx}  "
          f"netSignFlip {1000*flips//max(1,len(ts)-1):>4}permille  "
          f"residMean {mr}  resid>60 {big}permille")


print("== DIAG: mechanism of the fine-granularity collapse (seed 1, K=1) ==")
for step in (1, 2, 3, 5, 6, 10, 30):
    diag(step)
print("\n== DIAG: K dependence of the bifurcation (seed 1) ==")
for step in (3, 5, 6):
    for k in (1, 2, 8):
        diag(step, k=k)

print("\n== DIAG 2: duplicate-bloc vs gradient-band divergence discriminator ==")
print("   same-error fresh bloc of size M + one lag-30 laggard, K=1, delta=12")
print("   duplicate-mass law predicts divergence iff N=M+1 > 2*pd=6;")
print("   band-mass law predicts safe at any M (single error value in band).")
for m in (3, 5, 6, 7, 11):          # N = M+1 in {4,6,7,8,12}
    lats = [0] * m + [30]
    r = run_fabric("interference", 4800, lats, K=1, pd=3, delta=12,
                   drift=6, seed=1)
    resid = r["resid"]
    cap = 10 ** 18
    print(f"  M={m:>2} N={m+1:>2} lags[0]*{m}+[30]: true12% "
          f"{1000*sum(1 for x in resid if x <= 12)//len(resid)/10:>5.1f} "
          f"residMean {min(sum(resid)//len(resid), cap):>19} "
          f"events {r['events']}")

print("\n== DIAG 3: does the N-optimum track delta or 2*pd? (5-seed means) ==")
print("   ladder steps {1,5,6,10} at spread 30, K=1, delta in {6,12,24};")
print("   eval window pinned at 12. If optimum stays N=6 -> tracks 2*pd=6.")
SEEDS = (1, 7, 42, 1999, 20260902)
for d in (6, 12, 24):
    line = []
    for g in (1, 5, 6, 10):
        lats = list(range(0, 31, g))
        acc = 0
        for s in SEEDS:
            r = run_fabric("interference", 4800, lats, K=1, pd=3, delta=d,
                           drift=6, seed=s)
            acc += 1000 * sum(1 for x in r["resid"] if x <= 12) // 4800
        line.append(f"step{g}(N={len(lats)}): {acc/len(SEEDS)/10:.1f}%")
    print(f"  delta={d:>2}  " + "   ".join(line))
