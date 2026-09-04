#!/usr/bin/env python3
# ROUND 4 — O4 regime-motion closed loop (E4's real architecture).
#
# PRE-REGISTERED HYPOTHESIS: the closed loop — lag discovery (480-tick blade,
#   kimi #3/F19) -> per-twin lag compensation -> REGIME-META kappa-detector
#   state machine -> mode dial (sequential-calm vs interference-conflict) —
#   beats every static arm under mid-stream regime shifts, because
#   compensation converts conflict->calm and the dial must follow
#   (kimi #3 canary: compensated sequential 1000 permille vs compensated
#   interference 984 permille).
#
# PRE-REGISTERED DECISION RULE (fixed BEFORE any stress run):
#   Let W(X) = mean settle-permille over 5 seeds (1,7,42,1999,20260902),
#     measured with a UNIFORM post-compensation criterion |e|<=12 for both
#     twins (matches the canary cells; arm trigger deltas stay arm-owned).
#   Let D(X) = mean ledger debt over the same runs.
#   PROMOTE to E4 architecture iff:
#     (1) W(adaptive) >= max(W over all static arms, raw or compensated) - 10
#         (10 permille = 1pp), AND
#     (2) D(adaptive) <= 0.60 * min(D over static arms)   [debt gate].
#   ELSE book the boundary: report detector reaction lag (ticks from segment
#   boundary to confirmed mode flip) vs segment dwell (1600 ticks/segment).
#
# ENVIRONMENT (charter S3.2 task shape, fixed per seed, identical across arms):
#   ticks 0..1599    CALM     : lat2=5,  drift=3, no glitches
#   ticks 1600..3199 CONFLICT : lat2=10, drift=6
#   ticks 3200..4799 BURSTY   : lat2=5,  drift=3, one-tick twin glitches
#   Glitch stream: env LCG (separate from harness rng), prob 1/4 per tick,
#   magnitude sign* (28 + env.below(30)) applied to BOTH twin readings for
#   exactly that tick.
#
# ARMS (all 4800 ticks, 5 seeds, integer-only in-loop arithmetic):
#   A  adaptive  : blade every 480 ticks on raw twin history -> laghat comp ->
#                  kappa-detector (REGIME-META thresholds 120/4/280, entry 2,
#                  exit 5, refractory 10/20) -> dial: CALM=sequential d6,
#                  CONFLICT=interference d12/K4/div3.
#   B  static interference  (d12,K4,div3), raw and compensated variants
#   C  static sequential    (d12)          , raw and compensated variants
#   D  static impulse       (sequential d6), raw and compensated variants
#   E  compensated-static controls == the compensated variants of B/C/D
#      (same lag blade, frozen dial).
#
# CANARY (gate before stress runs): kimi #3 exp3 replay cells reproduce —
#   compensated sequential 1000 permille, compensated interference 984
#   permille, lag blade 5/5 exact (exp3 source imported verbatim from
#   INVENTIONS-kimi.md).

import sys
sys.path.insert(0, "/home/eileen/projects/quilt-verilog/spikes/225-e1-interference-tick")
from collections import deque
from e1 import LCG, reality

SEEDS = (1, 7, 42, 1999, 20260902)
WINDOW, MAXLAG = 480, 15
TICKS = 4800
SEG = (0, 1600, 3200, 4800)  # calm, conflict, bursty


def seg_at(t):
    if t < SEG[1]:
        return 0
    if t < SEG[2]:
        return 1
    return 2


def env_params(t):
    s = seg_at(t)
    if s == 0:
        return 5, 3
    if s == 1:
        return 10, 6
    return 5, 3


class Env:
    """Regime-motion environment: latency/drift schedule + glitch stream.

    Independent LCG (seeded once per run) so the environment stream is
    identical across arms for a given seed."""

    def __init__(self, seed):
        self.rng = LCG(seed ^ 0x5EED)

    def glitch(self):
        if self.rng.below(4) != 0:
            return 0
        mag = 28 + self.rng.below(30)
        return mag if self.rng.below(2) else -mag


# ---------------- kimi #3 exp3 replay (verbatim core) ----------------

def discover_lag(lat2, window=WINDOW, maxlag=MAXLAG):
    # d2(t) = d1(t - lat2); C(L) = sum_t d1(t)*d2(t+L) seats at L = lat2.
    n = window + maxlag + 2
    s1 = [reality(t) for t in range(n)]
    s2 = [reality(max(0, t - lat2)) for t in range(n)]
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


def run_comp(ticks=4800, K=4, pulse_div=3, delta=12, drift=6, lat2=10,
             seed=1, mode="interference", laghat=0):
    # E1 loop with T2's delay line shifted by laghat (laghat=0 -> e1.run).
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    settles = debt = max_err = 0
    for t in range(ticks):
        s1 = reality(t)
        s2 = reality(max(0, t - lat2 + laghat))
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        trig = []
        e1v, e2v = s1 - g, s2 - g
        if abs(e1v) > delta:
            trig.append(e1v)
        if abs(e2v) > delta:
            trig.append(e2v)
        if mode == "sequential":
            if trig:
                g += trig[0]
                debt += abs(trig[0])
        else:
            for e in trig:
                m = abs(e) // pulse_div or 1
                pulses.appendleft([m if e > 0 else -m, K])
                debt += abs(e)
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
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1
        err = max(abs(s1 - g), abs(s2 - g))
        if err > max_err:
            max_err = err
    return settles * 1000 // ticks, debt, max_err


# ---------------- round-4 regime-motion harness ----------------

DEBT_CLIMB_THRESH = 120
CANCEL_THRESH = 4
KAPPA_THRESH = 280
CONFLICT_ENTRY = 2
CALM_EXIT = 5
REFRACTORY_IN, REFRACTORY_OUT = 10, 20


class Detector:
    def __init__(self):
        self.dw = [0] * 16
        self.cw = [0] * 16
        self.di = self.ci = 0
        self.hits = 0
        self.calm = 0
        self.regime = 0            # 0 calm, 1 conflict
        self.total_snaps = 0
        self.refrac = 0
        self.last_regime = 0
        self.switch_t = None       # tick of last confirmed flip

    def tick(self, t, tick_debt, cancel_flag, snap_event):
        self.dw[self.di] = tick_debt
        self.di = (self.di + 1) & 0xF
        self.cw[self.ci] = 1 if cancel_flag else 0
        self.ci = (self.ci + 1) & 0xF
        self.total_snaps += snap_event
        older = sum(self.dw[(self.di + i) & 0xF] for i in range(8))
        recent = sum(self.dw[(self.di + i + 8) & 0xF] for i in range(8))
        climb = recent > older + DEBT_CLIMB_THRESH
        csum = sum(self.cw)
        chatter = csum >= CANCEL_THRESH
        kappa = (csum * 1000) > (KAPPA_THRESH * (self.total_snaps + 1)) \
            if self.total_snaps > 0 else False
        cand = climb or chatter or kappa
        if cand:
            self.hits += 1
            self.calm = 0
        else:
            self.hits = 0
            self.calm += 1
        if self.refrac > 0:
            self.refrac -= 1
        else:
            if self.hits >= CONFLICT_ENTRY and self.regime == 0:
                self.regime = 1
                self.hits = 0
                self.refrac = REFRACTORY_IN
                self.switch_t = t
            elif self.calm >= CALM_EXIT and self.regime == 1:
                self.regime = 0
                self.calm = 0
                self.refrac = REFRACTORY_OUT
                self.switch_t = t
        return self.regime


def discover_lag_stream(d1_hist, d2_hist):
    """Blade on live streams: d2(t) = d1(t - lat2). Seat L maximizing
    sum d1[t]*d2[t+L]. Same correlation as kimi #3, integer-only."""
    n = min(len(d1_hist), len(d2_hist))
    best_l, best_c = 0, None
    for L in range(MAXLAG + 1):
        c = 0
        for t in range(n - MAXLAG - 1):
            c += d1_hist[t] * d2_hist[t + L]
        if best_c is None or c > best_c:
            best_l, best_c = L, c
    return best_l


def run_arm(seed, arm, compensated=True, adaptive=False, blade=False):
    """arm: dict(mode=..., delta=..., K=..., div=...) with mode possibly None
    for adaptive. Returns per-segment permille + totals."""
    env = Env(seed)
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    det = Detector()
    mode = "sequential" if adaptive else arm["mode"]
    delta = 6 if adaptive else arm["delta"]
    K, div = (arm or {}).get("K", 4), (arm or {}).get("div", 3)
    laghat = 0
    d1_hist, d2_hist = [], []
    seg_settles = [0, 0, 0]
    seg_ticks = [1600, 1600, 1600]
    settles = debt = max_err = 0
    switch_events = []          # (tick, from, to)
    for t in range(TICKS):
        lat2, drift = env_params(t)
        gl = env.glitch() if seg_at(t) == 2 else 0
        s1 = reality(t) + gl
        raws2 = reality(max(0, t - lat2)) + gl
        s2 = raws2 if not compensated else reality(max(0, t - lat2 + laghat)) + gl
        if adaptive:
            # harness observes raw twin stream for the blade
            pass
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        trig = []
        e1v, e2v = s1 - g, s2 - g
        if abs(e1v) > delta:
            trig.append(e1v)
        if abs(e2v) > delta:
            trig.append(e2v)
        tick_debt = 0
        cancel_flag = 0
        snap_event = 0
        if mode == "sequential":
            if trig:
                g += trig[0]
                tick_debt = abs(trig[0])
                snap_event = 1
        else:
            for e in trig:
                m = abs(e) // div or 1
                pulses.appendleft([m if e > 0 else -m, K])
                tick_debt += abs(e)
                snap_event = 1
            if pulses:
                net = sum(p[0] for p in pulses)
                if net == 0 and len(pulses) >= 2:
                    cancel_flag = 1
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
        debt += tick_debt
        # uniform settle criterion: |e| <= 12 on both (compensated) views
        if abs(s1 - g) <= 12 and abs(s2 - g) <= 12:
            settles += 1
            seg_settles[seg_at(t)] += 1
        err = max(abs(s1 - g), abs(raws2 - g))
        if err > max_err:
            max_err = err
        if adaptive:
            prev = det.regime
            det.tick(t, tick_debt, cancel_flag, snap_event)
            if det.regime != prev:
                switch_events.append((t, prev, det.regime))
                mode = "sequential" if det.regime == 0 else "interference"
                delta = 6 if det.regime == 0 else 12
            # blade maintenance on glitch-free analytic channel: harness can
            # observe raw twin stream; strip glitch via magnitude gate is not
            # honest, so record raw diffs and accept glitch noise in the blade
        if blade:
            if t > 0:
                d1_hist.append(s1)
                d2_hist.append(raws2)
            if (t + 1) % WINDOW == 0 and len(d1_hist) > WINDOW + MAXLAG + 2:
                w1 = [d1_hist[i + 1] - d1_hist[i]
                      for i in range(len(d1_hist) - 1)][-WINDOW:]
                w2 = [d2_hist[i + 1] - d2_hist[i]
                      for i in range(len(d2_hist) - 1)][-WINDOW:]
                laghat = discover_lag_stream(w1, w2)
    seg_pm = [seg_settles[i] * 1000 // seg_ticks[i] for i in range(3)]
    return dict(total_pm=settles * 1000 // TICKS, seg=seg_pm, debt=debt,
                max_err=max_err, switches=switch_events)


def canary():
    ok = True
    for lat2 in (3, 5, 7, 10, 15):
        d = discover_lag(lat2)
        if d != lat2:
            ok = False
    cells = {}
    for mode in ("sequential", "interference"):
        for laghat, tag in ((0, "raw"), (10, "compensated")):
            rows = [run_comp(mode=mode, laghat=laghat, seed=s) for s in SEEDS]
            cells[mode + " " + tag] = sum(r[0] for r in rows) // 5
    print("canary:", cells)
    ok = ok and cells["sequential compensated"] == 1000 \
        and cells["interference compensated"] == 984
    return ok


if __name__ == "__main__":
    if not canary():
        print("CANARY FAILED — aborting stress runs")
        sys.exit(1)
    print("CANARY PASS (blade 5/5, seq-comp 1000, int-comp 984)")
    arms = [
        ("A adaptive (comp+detector+dial)", dict(mode=None, delta=None), True, True, True),
        ("B interference raw", dict(mode="interference", delta=12), False, False, False),
        ("B interference comp", dict(mode="interference", delta=12), True, False, True),
        ("C sequential d12 raw", dict(mode="sequential", delta=12), False, False, False),
        ("C sequential d12 comp", dict(mode="sequential", delta=12), True, False, True),
        ("D impulse d6 raw", dict(mode="sequential", delta=6), False, False, False),
        ("D impulse d6 comp", dict(mode="sequential", delta=6), True, False, True),
    ]
    results = {}
    for name, arm, comp, adapt, bl in arms:
        rows = [run_arm(s, arm, compensated=comp, adaptive=adapt, blade=bl)
                for s in SEEDS]
        results[name] = rows
        seg_pm = [sum(r["seg"][i] for r in rows) // 5 for i in range(3)]
        print(f"{name:<34} total {sum(r['total_pm'] for r in rows)//5:>5}permille"
              f"  calm/conf/bursty {seg_pm}"
              f"  debt {sum(r['debt'] for r in rows)//5:>7}"
              f"  maxErr {max(r['max_err'] for r in rows):>4}")
    # detector reaction lag
    print("\nadaptive switch events (tick, from->to) per seed:")
    for i, r in enumerate(results["A adaptive (comp+detector+dial)"]):
        print(f"  seed {SEEDS[i]:>9}: {r['switches'][:12]}")
    # decision rule
    W = {n: sum(r["total_pm"] for r in rs) // 5 for n, rs in results.items()}
    D = {n: sum(r["debt"] for r in rs) // 5 for n, rs in results.items()}
    stat = [n for n in W if n != "A adaptive (comp+detector+dial)"]
    maxW = max(W[n] for n in stat)
    minD = min(D[n] for n in stat)
    a = "A adaptive (comp+detector+dial)"
    g1 = W[a] >= maxW - 10
    g2 = D[a] <= (minD * 60) // 100
    print(f"\nDECISION: W(adaptive)={W[a]} vs maxW-10={maxW-10} -> gate1 {'PASS' if g1 else 'FAIL'}"
          f"; D(adaptive)={D[a]} vs 0.60*minD={(minD*60)//100} -> gate2 {'PASS' if g2 else 'FAIL'}")
    print("VERDICT:", "PROMOTE" if (g1 and g2) else "BOOK-BOUNDARY")
