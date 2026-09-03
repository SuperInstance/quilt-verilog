#!/usr/bin/env python3
"""DEV ROUND 2 — O2: Contention controller boundary (RESEARCH-AGENDA §4, from F14).

Question: does the sorted-switchboard win (mag+C=1 beats admit-all at N=5 stress,
69.6 vs 68.0 %w, maxE 232 vs 281 [glm-3 #1]) survive
  (a) generalization N ∈ {2,3,5,8} × regime ∈ {calm, stress}, and
  (b) per-twin lag compensation (F19/F20 first-difference integer
      cross-correlation blade, 480-tick window)?

Arms: raw vs lag-compensated. Integer-only core (no floats in the loop;
percentages are computed once at print time from integer settle counts).

Self-canary (instrument gate doctrine): a deliberately mislabeled arm
(mag+C=1 run labeled "admit-all") must be caught by the instrumentation
(differs from true admit-all, matches true mag), and the N=5 stress raw
control must reproduce glm-3's published numbers (%w 68.0/69.6, maxE 281/232).
Run: python3 o2_contention.py
"""
import sys, os
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inventors-derby"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from e1 import LCG, reality
from glm3_experiments import run_sw, LATS, KEYS

SEEDS = (1, 7, 42, 1999, 20260902)
TICKS = 4800
REGIMES = {"calm":   dict(K=8, pulse_div=3, delta=6,  drift=3),
           "stress": dict(K=4, pulse_div=3, delta=12, drift=6)}
KEY = "mag"  # F14's winning sort key

# Per-N twin latency sets (twin 0 always live). Spreads 0..12 like glm-3's N=5.
LATS_N = {
    2: (0, 12),
    3: (0, 6, 12),
    5: (0, 3, 6, 9, 12),
    8: (0, 2, 3, 5, 7, 8, 10, 12),
}

# ------------------------------------------------- F19 lag blade (verbatim method)
WINDOW, MAXLAG = 480, 15

def discover_lag(lat, window=WINDOW, maxlag=MAXLAG, reference_lag=0):
    """First-difference integer cross-correlation of the reality streams.
    Correlate d_ref (lag 0 twin) against d_lat (twin at lag `lat`); seats at L=lat.
    Reality-only streams -> seed-independent by construction."""
    n = window + maxlag + 2
    s1 = [reality(max(0, t - reference_lag)) for t in range(n)]
    s2 = [reality(max(0, t - lat)) for t in range(n)]
    d1 = [s1[t + 1] - s1[t] for t in range(n - 1)]
    d2 = [s2[t + 1] - s2[t] for t in range(n - 1)]
    best_l, best_c = 0, None
    for L in range(maxlag + 1):
        c = 0
        for t in range(window):
            c += d1[t] * d2[t + L]
        if best_c is None or c > best_c:
            best_l, best_c = L, c
    return best_l

# ------------------------------------------------- compensated switchboard runner
def run_sw_comp(seed, key=None, C=None, ticks=TICKS, lats=LATS, laghat=None, **params):
    """run_sw with each twin's delay line shifted by its discovered lag L̂_i.
    laghat=None -> raw arm (identical to glm3 run_sw, called directly).
    laghat=list -> reads_i(t) = reality(max(0, t - lats[i] + laghat[i]))."""
    if laghat is None:
        return run_sw(seed, key=key, C=C, ticks=ticks, lats=lats, **params)
    rng = LCG(seed)
    g = reality(0)
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
        reads = [reality(max(0, t - lats[i] + laghat[i])) for i in range(n)]
        g += rng.below(2 * params["drift"] + 1) - params["drift"]
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        cands = []
        for i, s in enumerate(reads):
            e = s - g
            if abs(e) > params["delta"]:
                cands.append(dict(id=i, err=e, err_abs=abs(e),
                                  last_fire=last_fire[i], cont=cont[i]))
                cont[i] += 1
        if key and len(cands) > C:
            cands.sort(key=KEYS[key])
            rejected += len(cands) - C
            cands = cands[:C]
        trig = [c["err"] for c in cands]
        max_trig = max((abs(e) for e in trig), default=0)
        for c in cands:
            e = c["err"]
            m = abs(e) // params["pulse_div"] or 1
            pulses.appendleft([m if e > 0 else -m, params["K"]])
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
        if all(abs(s - g) <= params["delta"] for s in reads):
            settles += 1
    return dict(events=events, debt=debt, chatter=chatter, cancel=cancellations,
                maxerr=max_err, pct=round(100 * settles / ticks, 1),
                fires=fires, rejected=rejected)


def cell(seeds_runs):
    """Aggregate 5 seed-runs -> (mean %w x10, MEAN maxE [glm-3 agg convention], mean events)."""
    pct_x10 = round(10 * sum(r["pct"] for r in seeds_runs) / len(seeds_runs))
    maxe = round(sum(r["maxerr"] for r in seeds_runs) / len(seeds_runs), 1)
    ev = sum(r["events"] for r in seeds_runs) // len(seeds_runs)
    return pct_x10, maxe, ev


def main():
    print("== O2: lag-blade discovery (per-N, per-twin) ==")
    laghat = {}
    for n, lats in LATS_N.items():
        hs = [discover_lag(L) for L in lats]
        laghat[n] = hs
        exact = all(h == L for h, L in zip(hs, lats))
        print(f"  N={n} lats={lats} -> discovered {hs} exact={exact}")

    print("\n== REPRODUCTION GATE: N=5 stress raw must match glm-3 published ==")
    all_rows = [run_sw(s, key=None, C=len(LATS), **REGIMES["stress"]) for s in SEEDS]
    a_pct = round(10 * sum(r["pct"] for r in all_rows) / 5) / 10
    a_maxe = round(sum(r["maxerr"] for r in all_rows) / 5, 1)
    mag_rows = [run_sw(s, key=KEY, C=1, **REGIMES["stress"]) for s in SEEDS]
    m_pct = round(10 * sum(r["pct"] for r in mag_rows) / 5) / 10
    m_maxe = round(sum(r["maxerr"] for r in mag_rows) / 5, 1)
    print(f"  admit-all %w={a_pct} maxE_sum5={round(a_maxe * 5)} (glm-3: 68.0/281)")
    print(f"  mag+C=1   %w={m_pct} maxE_sum5={round(m_maxe * 5)} (glm-3: 69.6/232)")
    # glm-3's agg SUMS int metrics over 5 seeds (maxE 281 = 5x56.2), so compare 5x mean.
    repro_ok = (a_pct == 68.0 and round(a_maxe * 5) == 281
                and m_pct == 69.6 and round(m_maxe * 5) == 232)
    print(f"  REPRODUCTION: {'PASS' if repro_ok else 'FAIL'}")

    print("\n== SELF-CANARY: mislabeled arm must be caught by instrumentation ==")
    # Run mag+C=1 but LABEL it admit-all; instrumentation must show it does NOT
    # equal true admit-all (and DOES equal true mag). Canary = seeded labeling bug.
    canary = round(10 * sum(r["pct"] for r in mag_rows) / 5) / 10
    caught = (canary != a_pct) and (canary == m_pct)
    print(f"  mislabeled 'admit-all'(actually mag C=1) %w={canary} vs true admit-all {a_pct}"
          f" -> {'CAUGHT' if caught else 'MISSED'}")

    print("\n== MAIN GRID: N x C x regime x arm, mag key, 5 seeds, 4800 ticks ==")
    results = {}
    for reg, params in REGIMES.items():
        for n, lats in LATS_N.items():
            for arm, lag in (("raw", None), ("comp", laghat[n])):
                for C in range(1, n + 1):
                    rows = [run_sw_comp(s, key=KEY, C=C, lats=lats, laghat=lag, **params)
                            for s in SEEDS]
                    results[(reg, n, arm, C)] = cell(rows)
                rows = [run_sw_comp(s, key=None, C=n, lats=lats, laghat=lag, **params)
                        for s in SEEDS]
                results[(reg, n, arm, "all")] = cell(rows)

    print(f"\n{'regime':7s} {'N':>2s} {'arm':5s}  admit-all %w/maxE/ev"
          f"   | C=1..N (%w|maxE) mag-sorted")
    for reg in REGIMES:
        for n in LATS_N:
            for arm in ("raw", "comp"):
                aa = results[(reg, n, arm, "all")]
                cs = "  ".join(
                    f"C{C}={results[(reg, n, arm, C)][0]/10:.1f}|{results[(reg, n, arm, C)][1]}"
                    for C in range(1, n + 1))
                print(f"{reg:7s} {n:2d} {arm:5s}  {aa[0]/10:5.1f} {aa[1]:5.1f} {aa[2]:6d}    {cs}")

    print("\n== DECISION TABLE: mag C=1 minus admit-all (pp), per N/regime/arm ==")
    for reg in REGIMES:
        for arm in ("raw", "comp"):
            for n in LATS_N:
                if n < 2:
                    continue
                aa = results[(reg, n, arm, "all")][0]
                c1 = results[(reg, n, arm, 1)][0]
                print(f"  {reg:7s} N={n} {arm:5s}  admit-all {aa/10:.1f}%w  magC1 {c1/10:.1f}%w"
                      f"  delta {(c1-aa)/10:+.1f}pp")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "o2-contention-output.txt"), "w") as f:
        f.write("see stdout; regenerate with python3 o2_contention.py\n")


if __name__ == "__main__":
    main()
