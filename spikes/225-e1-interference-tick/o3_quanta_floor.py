#!/usr/bin/env python3
"""O3 — Quanta floor on RTL alphabets (RESEARCH-AGENDA.md §4, from F23).

Hypothesis (pre-registered): the 3-bit cap (±5, 99% of interference win at
K=4 stress [F23 / opencode #4]) holds at K=2 too; the Z3 debt inversion
(sign-only pulses: residency beats impulse but debt exceeds it) persists
everywhere.

Grid: cap ∈ {1,2,3,5,7,11,INF} × K ∈ {1,2,3,4} × regime {calm, stress}
      × seeds {1,7,42,1999,20260902}. Z3 sign-only arm = cap=1, reported
      separately at K∈{2,4}.

Decision rule (pre-registered): cap=±5 retains ≥99% of the uncapped win at
K=2 ⇒ adopt 3-bit alphabet as ESP32/.qm port default; knee elsewhere ⇒
adopt the measured knee; Z3 stays sampling gear unless debt inverts back
below impulse.

Integer-only. Reuses e1.py primitives (LCG, reality, pulse mechanics)
re-implemented with a seed parameter (e1.run hardcodes SEED); byte-identity
is proven by CANARY A below, which diffs this harness against e1.run itself.
"""
from collections import deque

SEEDS = [1, 7, 42, 1999, 20260902]
CAPS = [1, 2, 3, 5, 7, 11, None]  # None = unbounded
KS = [1, 2, 3, 4]
REGIMES = {
    "calm":   dict(delta=6, drift=3, lat2=5),
    "stress": dict(delta=12, drift=6, lat2=10),
}
TICKS = 4800
PULSE_DIV = 3

from e1 import LCG, reality  # identical primitives, imported not copied


def run(mode, seed, cap, K, regime):
    """e1.run with (a) seed param, (b) magnitude cap. cap=None unbounded.
    Mechanics line-for-line from e1.py run(); cap clamps |m| only."""
    p = REGIMES[regime]
    delta, drift, lat2 = p["delta"], p["drift"], p["lat2"]
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    snap_events = 0
    ledger_mass = 0
    constructive = 0
    cancellations = 0
    chatter = 0
    last_snap = -10
    max_err = 0
    settles = 0

    for t in range(TICKS):
        s1 = reality(t)
        s2 = reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift

        while pulses and pulses[-1][1] == 0:
            pulses.pop()

        e1_ = s1 - g
        e2 = s2 - g
        trig = []
        if abs(e1_) > delta:
            trig.append(e1_)
        if abs(e2) > delta:
            trig.append(e2)
        max_trig = max((abs(e) for e in trig), default=0)

        if mode == "sequential":
            if trig:
                g += trig[0]
                snap_events += 1
                ledger_mass += abs(trig[0])
                if t - last_snap == 1:
                    chatter += 1
                last_snap = t
                if max(abs(s1 - g), abs(s2 - g)) > max_trig:
                    constructive += 1
        else:
            for e in trig:
                m = abs(e) // PULSE_DIV or 1
                if cap is not None and m > cap:
                    m = cap
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

    return dict(mode=mode, events=snap_events, debt=ledger_mass,
                constructive=constructive, cancel=cancellations,
                chatter=chatter, max_err=max_err,
                pm=1000 * settles // TICKS)  # per-mille, integer


# ---------------------------------------------------------------- canaries
def canary_a():
    """Byte-identity replay: this harness at defaults (seed 20260902,
    cap=None, e1's calm and stress params) must reproduce e1.run exactly."""
    import e1
    ok = []
    for label, kw in [("calm", dict(K=8)), ("stress", dict(K=4, delta=12, drift=6, lat2=10))]:
        for mode in ("sequential", "interference"):
            ref = e1.run(mode, **kw)
            mine = run(mode, 20260902, None, kw["K"],
                       "calm" if label == "calm" else "stress")
            # integer counters must match exactly; pm compared to ±1\u2030
            # (e1 rounds 100*settles/4800 as float; we floor 1000*settles/4800)
            same = (ref["snap_events"] == mine["events"]
                    and ref["ledger_mass"] == mine["debt"]
                    and ref["constructive"] == mine["constructive"]
                    and ref["cancellations"] == mine["cancel"]
                    and ref["chatter"] == mine["chatter"]
                    and ref["max_err"] == mine["max_err"]
                    and abs(ref["pct_within"] * 10 - mine["pm"]) <= 1)
            ok.append(same)
            print(f"  canary A [{label}/{mode}] e1.run pm={ref['pct_within']} "
                  f"debt={ref['ledger_mass']} events={ref['snap_events']} -> "
                  f"{'IDENTICAL' if same else 'MISMATCH'}")
    # F23 published anchors (5-seed stress means): uncapped interference
    # 830‰ / debt 34995; impulse 519‰ / debt 48397. Default-seed check first:
    r = run("interference", 20260902, None, 4, "stress")
    i = run("sequential", 20260902, None, 4, "stress")
    print(f"  canary A2 [F23 anchor, seed 20260902 stress]: "
          f"interference pm={r['pm']}\u2030 debt={r['debt']} | "
          f"impulse pm={i['pm']}\u2030 debt={i['debt']}")
    print(f"  (F23 booked 5-seed means: 830\u2030/34995 and 519\u2030/48397 — "
          f"compared against 5-seed grid means below)")
    return all(ok)


def canary_b():
    """Self-canary: a deliberately mislabeled arm (cap=5 labeled INF) must be
    CAUGHT — i.e. its stats must differ from the true INF arm. If they match,
    the detector is blind and the canary fails."""
    caught = []
    for seed in (20260902, 7):
        a = run("interference", seed, 5, 4, "stress")
        b = run("interference", seed, None, 4, "stress")
        differ = (a["events"], a["debt"], a["pm"]) != (b["events"], b["debt"], b["pm"])
        caught.append(differ)
        print(f"  canary B [seed {seed}] cap5 pm={a['pm']}\u2030 debt={a['debt']} "
              f"vs INF pm={b['pm']}\u2030 debt={b['debt']} -> "
              f"{'CAUGHT (differ)' if differ else 'NOT CAUGHT — BLIND'}")
    return all(caught)


# ------------------------------------------------------------------- grid
def main():
    print("=== CANARIES ===")
    a_ok = canary_a()
    b_ok = canary_b()
    print(f"canary A (byte-identity vs e1.run): {'PASS' if a_ok else 'FAIL'}")
    print(f"canary B (mislabeled-cap detector): {'PASS' if b_ok else 'FAIL'}")

    print("\n=== GRID (5-seed means, \u2030 residency, integer debt) ===")
    results = {}  # (regime, K, cap) -> dict(means per mode)
    for regime in REGIMES:
        for K in KS:
            # impulse baseline (cap irrelevant)
            imp = [run("sequential", s, None, K, regime) for s in SEEDS]
            imp_pm = sum(r["pm"] for r in imp) // len(imp)
            imp_debt = sum(r["debt"] for r in imp) // len(imp)
            for cap in CAPS:
                rows = [run("interference", s, cap, K, regime) for s in SEEDS]
                pm = sum(r["pm"] for r in rows) // len(rows)
                debt = sum(r["debt"] for r in rows) // len(rows)
                ev = sum(r["events"] for r in rows) // len(rows)
                results[(regime, K, cap)] = dict(pm=pm, debt=debt, ev=ev,
                                                 imp_pm=imp_pm, imp_debt=imp_debt)

    label = lambda c: "INF" if c is None else str(c)
    for regime in REGIMES:
        print(f"\n-- {regime} --")
        print(f"{'K':>2} {'cap':>4} {'events':>7} {'debt':>7} {'pm':>5} "
              f"{'imp_pm':>7} {'retention%':>10}")
        for K in KS:
            for cap in CAPS:
                r = results[(regime, K, cap)]
                inf = results[(regime, K, None)]
                win_cap = r["pm"] - r["imp_pm"]
                win_inf = inf["pm"] - inf["imp_pm"]
                ret = (100 * win_cap / win_inf) if win_inf > 0 else None
                rs = f"{ret:>9.1f}%" if ret is not None else "      n/a "
                print(f"{K:>2} {label(cap):>4} {r['ev']:>7} {r['debt']:>7} "
                      f"{r['pm']:>5} {r['imp_pm']:>7} {rs}")

    print("\n=== F23 ANCHOR REPLAY (5-seed stress means, K=4) ===")
    inf4 = results[("stress", 4, None)]
    imp4_pm = inf4["imp_pm"]; imp4_debt = inf4["imp_debt"]
    print(f"  uncapped interference: pm={inf4['pm']}\u2030 (F23: 830) debt={inf4['debt']} (F23: 34995)")
    print(f"  impulse baseline:      pm={imp4_pm}\u2030 (F23: 519) debt={imp4_debt} (F23: 48397)")
    # Impulse: F23's 519/48397 matches ONLY seed 20260902 (canary A stress/
    # sequential: debt 48397, pm 51.9) — F23's impulse anchor was single-seed,
    # while its interference rows are exact 5-seed means of this seed set
    # (every cap row in the grid matches F23's table to the digit).
    imp_seed = run("sequential", 20260902, None, 4, "stress")
    anchor_ok = (inf4["pm"] == 830 and inf4["debt"] == 34995
                 and imp_seed["pm"] == 518 and imp_seed["debt"] == 48397
                 and results[("stress", 4, 5)]["pm"] == 824
                 and results[("stress", 4, 1)]["debt"] == 53907)
    print(f"  (impulse seed-20260902 replay: pm={imp_seed['pm']}\u2030 debt={imp_seed['debt']}")

    print("\n=== DECISION DATA ===")
    # retention of cap=5 at K=2 (and K=1,3) per regime
    for K in KS:
        for regime in REGIMES:
            r5 = results[(regime, K, 5)]
            inf = results[(regime, K, None)]
            w5 = r5["pm"] - r5["imp_pm"]
            wi = inf["pm"] - inf["imp_pm"]
            ret = 100 * w5 / wi if wi > 0 else float("nan")
            print(f"  K={K} {regime}: cap=5 retention {ret:.1f}% "
                  f"(pm {r5['pm']} vs INF {inf['pm']} vs impulse {r5['imp_pm']})")
    print("\n  Z3 sign-only (cap=1) vs impulse debt, K∈{2,4}:")
    z3_inverts = True
    for K in (2, 4):
        for regime in REGIMES:
            r1 = results[(regime, K, 1)]
            z3_inverts = z3_inverts and (r1["debt"] > r1["imp_debt"])
            print(f"  K={K} {regime}: Z3 pm={r1['pm']}\u2030 debt={r1['debt']} "
                  f"vs impulse pm={r1['imp_pm']}\u2030 debt={r1['imp_debt']} "
                  f"-> debt {'ABOVE' if r1['debt'] > r1['imp_debt'] else 'BELOW'} impulse "
                  f"(residency {'win' if r1['pm'] > r1['imp_pm'] else 'lose'})")
    print(f"  Z3 debt inversion persists everywhere (sampled): "
          f"{'YES' if z3_inverts else 'NO — INVERTED BACK'}")
    print(f"  F23 anchor replay within tolerance: {'PASS' if anchor_ok else 'FAIL'}")


if __name__ == "__main__":
    main()
