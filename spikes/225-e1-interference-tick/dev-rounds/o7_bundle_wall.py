#!/usr/bin/env python3
# O7 — Bundle wall × compensation (RESEARCH-AGENDA.md §4 O7; from F7 × F19/F20).
# Hypothesis: the N=4 bundle-capacity toxicity wall (glm-1 sheet B: interference
# true-residency 91% -> 10% by N>=4, impulse flat ~51%) is LAG-DRIVEN; per-twin
# lag compensation (F19 kimi blade / F20 opencode 480-tick first-difference
# integer cross-correlation, argmax) moves the wall right: N=4 trueRes >= 50%.
# Decision rule: N=4 trueRes >= 50% compensated  => capacity law restated as
# "stale-sensing capacity, not twin count"; wall unmoved => wall is geometric
# (10-tick-stale disagreement up to 16 on the 8/5 slope) — book two-law split.
#
# Harness: glm-1 exp_b N-sweep runner ported VERBATIM (canary anchor) from
# inventors-derby/exp_glm1.py; lag blade ported from kimi exp3 (INVENTIONS-kimi
# #3) / o4_regime_motion.py. Integer-only verdict path (permille); floats only
# in display division. Grid: N in 2..8 x {raw, lag-comp} x {calm, stress}
# x {sequential (impulse), interference}, 5 seeds, 4800 ticks.
# Run: python3 dev-rounds/o7_bundle_wall.py
from collections import deque

SEEDS = (1, 7, 42, 1999, 20260902)
PERIOD = 240
TICKS = 4800
BLADE_WINDOW = 480          # F19/F20: 480-tick first-difference blade

REGIMES = {
    # name: (delta, drift, K, pd, spacing)
    "stress": (12, 6, 4, 3, 10),   # glm-1 sheet B exact regime
    "calm":   (6,  3, 8, 3, 5),    # kimi/ledger calm regime
}


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
    """VERBATIM port of glm-1 exp_glm1.run_fabric (canary anchor; untouched)."""
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


# ---- F19/F20 lag blade: 480-tick first-difference integer cross-correlation.
# Correlates twin i's delayed stream against the reference (twin 0, lag 0)
# reality stream. Streams are reality-only => discovery is seed-independent
# (kimi exp3 doctrine). maxlag per-twin: lat + 5 (blade margin).
def discover_lag(lat, window=BLADE_WINDOW):
    maxlag = lat + 5
    n = window + maxlag + 2
    s1 = [reality(t) for t in range(n)]
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


def compensated_lats(lats):
    """Per-twin blade discovery then repayment: lat' = max(0, lat - L_hat)."""
    return [max(0, lat - discover_lag(lat)) for lat in lats]


def run_cell(mode, comp, regime, N, seed):
    delta, drift, K, pd, spacing = REGIMES[regime]
    lats = list(range(0, N * spacing, spacing))
    if comp:
        lats = compensated_lats(lats)
    return run_fabric(mode, TICKS, lats, seed=seed, K=K, pd=pd,
                      delta=delta, drift=drift)


def grid(pass_no=1):
    rows = []
    for regime in ("stress", "calm"):
        print(f"\n== regime {regime} "
              f"(delta={REGIMES[regime][0]} drift={REGIMES[regime][1]} "
              f"K={REGIMES[regime][2]} pd={REGIMES[regime][3]} "
              f"spacing={REGIMES[regime][4]}) ==")
        print(f"{'N':>2} {'mode':<12}{'arm':<5}{'allW%':>8}{'trueRes%':>10}"
              f"{'events':>8}{'cancels':>9}{'maxTrue':>9}")
        for N in range(2, 9):
            for comp in (False, True):
                for mode in ("interference", "sequential"):
                    aw = tr = ev = ca = mt = 0
                    for seed in SEEDS:
                        r = run_cell(mode, comp, regime, N, seed)
                        aw += r["settles"] * 1000 // r["ticks"]
                        tr += within_pm(r["resid"], REGIMES[regime][0])
                        ev += r["events"]
                        ca += r["cancels"]
                        mt = max(mt, max(r["resid"]))
                    k = len(SEEDS)
                    row = (pass_no, regime, N, mode, "comp" if comp else "raw",
                           aw // k, tr // k, ev // k, ca // k, mt)
                    rows.append(row)
                    print(f"{N:>2} {mode:<12}{row[4]:<5}{aw/k/10:>8.1f}"
                          f"{tr/k/10:>10.1f}{ev//k:>8}{ca//k:>9}{mt:>9}")
    return rows


# ---- canary 2: anchor replay vs glm-1 sheet B published values (stress) ----
# Published (INVENTIONS-glm-1.md sheet B, 5-seed means):
#   N=2 interf true 91.0, N=3 34.5, N=4 12.2; seq true N=2 78.4, N>=3 ~51
#   (53.1/51.4/50.9/50.9/50.9/50.9). Tolerance +-2pp.
ANCHOR = {
    ("interference", "raw", 2): 91.0,
    ("interference", "raw", 3): 34.5,
    ("interference", "raw", 4): 12.2,
    ("sequential", "raw", 2): 78.4,
    ("sequential", "raw", 3): 53.1,
    ("sequential", "raw", 4): 51.4,
    ("sequential", "raw", 5): 50.9,
    ("sequential", "raw", 8): 50.9,
}
TOL = 20   # permille (=2pp)


def anchor_check(rows, inject_mislabel=False):
    stress = {(m, a, n): tr for (_, rg, n, m, a, aw, tr, ev, ca, mt) in rows
              if rg == "stress"}
    if inject_mislabel:
        # SELF-CANARY: pass the N=2 raw interference arm off as N=4 raw.
        stress[("interference", "raw", 4)] = stress[("interference", "raw", 2)]
    ok = True
    for (m, a, n), pub in sorted(ANCHOR.items(), key=lambda x: (x[0][2], x[0])):
        got = stress[(m, a, n)]
        hit = abs(got - int(pub * 10)) <= TOL
        ok = ok and hit
        print(f"  {'PASS' if hit else 'FAIL'} {m:<12}{a:<4}N={n}: "
              f"got {got/10:.1f}% vs published {pub}% (tol ±2pp)")
    return ok


def main():
    print("== O7. BUNDLE WALL x LAG COMPENSATION "
          "(N 2..8 x {raw, comp} x {stress, calm}; 5 seeds; 4800 ticks) ==")

    # lag-blade verification first (F19 5/5 pattern; extended to long lags)
    print("\n== lag blade verification (stress spacing 10, calm spacing 5) ==")
    exact = 0
    for lat in (3, 5, 7, 10, 15, 20, 30, 40, 50, 60, 70):
        L = discover_lag(lat)
        hit = (L == lat)
        exact += hit
        print(f"  true lag {lat:>2} -> discovered {L:>2}  {'OK' if hit else 'MISS'}")
    print(f"  blade exact: {exact}/11")

    rows1 = grid(pass_no=1)
    rows2 = grid(pass_no=2)

    # canary 1: byte-identity double-run over ALL cells
    sig1 = [(r[1:]) for r in rows1]
    sig2 = [(r[1:]) for r in rows2]
    identical = sig1 == sig2
    print(f"\ncanary 1 (double-run byte-identity, {len(sig1)} cells "
          f"x 5 seeds): {'PASS' if identical else 'FAIL'}")

    # canary 2: anchor replay
    print("\ncanary 2 (anchor replay vs glm-1 sheet B, stress raw):")
    a_ok = anchor_check(rows1)

    # canary 3: self-canary — mislabeled arm must be CAUGHT
    print("\ncanary 3 (self-canary: N=2 raw interf passed off as N=4 — "
          "checker must FAIL it):")
    caught = not anchor_check(rows1, inject_mislabel=True)
    print(f"  self-canary {'CAUGHT (PASS)' if caught else 'MISSED (FAIL)'}")

    # verdict vs decision rule
    print("\n== verdict inputs ==")
    n4 = {(m, a): tr for (_, rg, n, m, a, aw, tr, ev, ca, mt) in rows1
          if rg == "stress" and n == 4}
    print(f"  N=4 stress interference raw  trueRes {n4[('interference','raw')]/10:.1f}%")
    print(f"  N=4 stress interference comp trueRes {n4[('interference','comp')]/10:.1f}%"
          f"   (decision gate: >= 50%)")
    n4c = n4[("interference", "comp")]
    verdict = "WALL MOVED (stale-sensing capacity)" if n4c >= 500 \
        else "WALL UNMOVED (geometric; two-law split)"
    print(f"\nVERDICT: {verdict}")
    print(f"canaries: double-run {'PASS' if identical else 'FAIL'}, "
          f"anchor {'PASS' if a_ok else 'FAIL'}, "
          f"self-canary {'CAUGHT' if caught else 'MISSED'}")


if __name__ == "__main__":
    main()
