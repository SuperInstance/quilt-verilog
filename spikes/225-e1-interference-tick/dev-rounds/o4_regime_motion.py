#!/usr/bin/env python3
# O4 — Lag-compensation regime motion (RESEARCH-AGENDA.md §4, O4; from S2/F19).
# Closed loop: lag discovery (480-tick first-difference blade) -> per-twin lag
# compensation -> REGIME-META kappa-detector -> mode dial (sequential <-> interference),
# run on a mid-stream shift sequence (calm -> conflict -> bursty, charter §3.2).
# Static arms at identical budget: sequential/interference x raw/compensated
# (fixed-lag and oracle-lag). Integer-only; reuses e1.py LCG/reality primitives.
# Run: python3 dev-rounds/o4_regime_motion.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import deque
from e1 import LCG, reality

SEEDS = (1, 7, 42, 1999, 20260902)
TICKS = 4800
SEG_A, SEG_B = 1600, 3200          # shift times, fixed, unknown to controllers
WINDOW, MAXLAG = 480, 15
GLITCH_MAG = 45

# ---- REGIME-META detector constants (REGIME-META.md) ----
DEBT_CLIMB_THRESH = 120
CANCEL_THRESH = 4
KAPPA_THRESH_PERMILLE = 280
CONFLICT_ENTRY, CALM_EXIT = 2, 5
CALM, CONFLICT = 0, 1

def seg(t):
    """Environment segment parameters: (delta, drift, lat2, glitch_rate_n)."""
    if t < SEG_A:   return 6, 3, 5, 0     # calm
    if t < SEG_B:   return 12, 6, 10, 0   # conflict
    return 6, 3, 10, 4                    # bursty: calm params + ADC glitches (1-in-4)

def seg_name(t):
    return "calm" if t < SEG_A else ("conflict" if t < SEG_B else "bursty")

# ---- kimi exp3 lag blade, verbatim (canary A) ----
def discover_lag(lat2, window=WINDOW, maxlag=MAXLAG):
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

# ---- live estimator: same blade on OBSERVED streams, sign-clipped (glitch-robust) ----
def discover_lag_obs(s1h, s2h, end, window=WINDOW, maxlag=MAXLAG):
    # sign-only first differences: sgn(d) in {-1,0,1}; glitches are common-mode
    # same-tick spikes (they hit both twins) and would seat a false L=0 peak in
    # the raw-product blade; sign-clipping keeps them at unit weight while the
    # true-lag seat accumulates ~window genuine matches.
    def d(stream, t):
        x = stream[t] - stream[t - 1]
        return (x > 0) - (x < 0)
    best_l, best_c = 0, None
    for L in range(maxlag + 1):
        c = 0
        for t in range(end - window, end):
            c += d(s1h, t) * d(s2h, t + L)
        if best_c is None or c > best_c:
            best_l, best_c = L, c
    return best_l

class Detector:
    def __init__(self):
        self.debt_w = [0]*16; self.cancel_w = [0]*16
        self.didx = self.cidx = 0
        self.hits = 0; self.calm_t = 0; self.regime = CALM
        self.total_snaps = 0; self.cancel_events = 0
    def tick(self, tick_debt, cancel_flag, snap_event):
        self.debt_w[self.didx] = tick_debt; self.didx = (self.didx + 1) & 0xF
        self.cancel_w[self.cidx] = cancel_flag; self.cidx = (self.cidx + 1) & 0xF
        self.total_snaps += snap_event; self.cancel_events += cancel_flag
        older = sum(self.debt_w[(self.didx + i) & 0xF] for i in range(8))
        recent = sum(self.debt_w[(self.didx + i + 8) & 0xF] for i in range(8))
        debt_climb = recent > older + DEBT_CLIMB_THRESH
        cancel_sum = sum(self.cancel_w)
        chatter = cancel_sum >= CANCEL_THRESH
        kappa = self.cancel_events * 1000 > KAPPA_THRESH_PERMILLE * (self.total_snaps + 1)
        cand = debt_climb or chatter or kappa
        if cand: self.hits += 1; self.calm_t = 0
        else:    self.hits = 0; self.calm_t += 1
        if self.hits >= CONFLICT_ENTRY and self.regime == CALM:
            self.regime = CONFLICT; self.hits = 0
        if self.calm_t >= CALM_EXIT and self.regime == CONFLICT:
            self.regime = CALM; self.calm_t = 0

def run_arm(arm, seed, invert_dial=False):
    """arm in {seq-raw, int-raw, seq-comp-fix, int-comp-fix, seq-comp-oracle,
    int-comp-oracle, adaptive}. Returns dict of integer metrics + telemetry."""
    rng = LCG(seed); grng = LCG(seed ^ 0x5A5A)
    g = reality(0)
    pulses = deque()
    det = Detector()
    s1h = [0]*TICKS; s2h = [0]*TICKS      # observed (glitch-inclusive) readings
    laghat = 0; mode = "sequential"; trig_delta = 6
    settles = debt = max_err = 0
    seg_st = {"calm": 0, "conflict": 0, "bursty": 0}
    lag_trace = []
    mode_ticks = {"calm": 0, "conflict": 0, "bursty": 0}
    seq_frac = {"calm": [0,0], "bursty": [0,0]}
    switches = 0; prev_mode = mode
    det_lag = {}                          # segment -> ticks from shift to regime flip
    flips = {}
    for t in range(TICKS):
        delta_e, drift, lat2, grn = seg(t)
        s1 = reality(t); s2 = reality(max(0, t - lat2))
        glitch = 0
        if grn and grng.below(grn) == 0:
            glitch = 45 if grng.below(2) else -45
        s1 += glitch; s2 += glitch
        s1h[t] = s1; s2h[t] = s2
        g += rng.below(2 * drift + 1) - drift

        # --- controller: compensation + mode ---
        if arm == "adaptive":
            if t >= WINDOW and t % WINDOW == 0:
                laghat = discover_lag_obs(s1h, s2h, t)
                lag_trace.append((t, seg_name(t), laghat))
            det_regime = det.regime
            if invert_dial: det_regime = CONFLICT - det_regime
            mode = "sequential" if det_regime == CALM else "interference"
            trig_delta = 6 if det_regime == CALM else 12
            if mode != prev_mode: switches += 1
            prev_mode = mode
            if t == SEG_A: flips["t_at_conflict_onset"] = t
            # detector lag: first CONFLICT regime tick at/after SEG_A, etc.
            for edge, name in ((SEG_A, "conflict"), (SEG_B, "bursty")):
                if t >= edge and name not in det_lag and det.regime == CONFLICT:
                    det_lag[name] = t - edge
            if "calm_back" not in det_lag and t >= SEG_B and det.regime == CALM:
                det_lag["calm_back"] = t - SEG_B
            lag_eff = laghat
        elif arm.endswith("-fix"):   lag_eff = 10
        elif arm.endswith("-oracle"):
            lag_eff = lat2
        else:                        lag_eff = 0
        static_mode = {"seq": "sequential", "int": "interference"}
        m = mode if arm == "adaptive" else static_mode[arm.split("-")[0]]
        td = trig_delta if arm == "adaptive" else (6 if m == "sequential" else 12)

        # --- aligned readings (post-compensation frame: delay fresh T1 by L-hat) ---
        a1 = s1h[max(0, t - lag_eff)]
        a2 = s2h[t]
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        e1v, e2v = a1 - g, a2 - g
        trig = []
        if abs(e1v) > td: trig.append(e1v)
        if abs(e2v) > td: trig.append(e2v)
        tick_debt = 0; cancel_flag = 0; snap_event = 0
        if m == "sequential":
            if trig:
                g += trig[0]; tick_debt = abs(trig[0]); debt += tick_debt
                snap_event = 1
        else:
            for e in trig:
                pm = abs(e) // 3 or 1
                pulses.appendleft([pm if e > 0 else -pm, 4]); tick_debt += abs(e)
            debt += tick_debt
            snap_event = 1 if trig else 0
            if pulses:
                net = sum(p[0] for p in pulses)
                if net == 0 and len(pulses) >= 2 and \
                   (any(p[0] > 0 for p in pulses) and any(p[0] < 0 for p in pulses)):
                    cancel_flag = 1
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1: mag = mag - (mag // 2)
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
        det.tick(tick_debt, cancel_flag, snap_event)
        if abs(a1 - g) <= delta_e and abs(a2 - g) <= delta_e:
            settles += 1
            seg_st[seg_name(t)] += 1
        err = max(abs(a1 - g), abs(a2 - g))
        if err > max_err: max_err = err
        sn = seg_name(t)   # segment name for this tick
        mode_ticks[sn] += 1 if m == "interference" else 0
        if sn in seq_frac:
            seq_frac[sn][0 if m == "sequential" else 1] += 1
    return dict(arm=arm, seed=seed, pm=settles * 1000 // TICKS, debt=debt,
                max_err=max_err, int_frac=mode_ticks, switches=switches,
                det_lag=det_lag, seq_frac=seq_frac,
                seg_pm={k: v * 1000 // 1600 for k, v in seg_st.items()},
                lag_trace=lag_trace)

def mean_pm(rows): return sum(r["pm"] for r in rows) // len(rows)
def mean_debt(rows): return sum(r["debt"] for r in rows) // len(rows)
def max_err(rows): return max(r["max_err"] for r in rows)

if __name__ == "__main__":
    print("== O4: lag-compensation regime motion (calm->conflict->bursty, %d ticks) ==" % TICKS)
    print("segments: calm [0,%d) d6/d3/lat5 | conflict [%d,%d) d12/d6/lat10 | bursty [%d,%d) d6/d3/lat10 + 1-in-4 +/-45 ADC glitches"
          % (SEG_A, SEG_A, SEG_B, SEG_B, TICKS))
    print()
    print("-- CANARY A: kimi F19 anchors (exp3_lag_blade.py verbatim replay) --")
    ok = True
    for lat2 in (3, 5, 7, 10, 15):
        got = discover_lag(lat2)
        good = got == lat2
        ok &= good
        print("  true lag %2d -> discovered %2d  %s" % (lat2, got, "OK" if good else "FAIL"))
    # compensated stress rows, exp3 run_comp verbatim (delta=12, drift=6, K=4, pd=3)
    def run_comp(ticks, K, pulse_div, delta, drift, lat2, seed, mode, laghat):
        rng = LCG(seed); g = reality(0); pulses = deque()
        settles = debt = max_err = 0
        for t in range(ticks):
            s1 = reality(t); s2 = reality(max(0, t - lat2 + laghat))
            g += rng.below(2 * drift + 1) - drift
            while pulses and pulses[-1][1] == 0: pulses.pop()
            e1v, e2v = s1 - g, s2 - g
            trig = []
            if abs(e1v) > delta: trig.append(e1v)
            if abs(e2v) > delta: trig.append(e2v)
            if mode == "sequential":
                if trig: g += trig[0]; debt += abs(trig[0])
            else:
                for e in trig:
                    m = abs(e) // pulse_div or 1
                    pulses.appendleft([m if e > 0 else -m, K]); debt += abs(e)
                if pulses:
                    net = sum(p[0] for p in pulses)
                    decayed = deque()
                    for mag, life in pulses:
                        if life > 0:
                            if abs(mag) > 1: mag = mag - (mag // 2)
                            decayed.append([mag, life - 1])
                    pulses = decayed; g += net
            if abs(s1 - g) <= delta and abs(s2 - g) <= delta: settles += 1
            err = max(abs(s1 - g), abs(s2 - g))
            if err > max_err: max_err = err
        return settles * 1000 // ticks, debt, max_err
    anchor_rows = {}
    for mode in ("sequential", "interference"):
        for laghat, tag in ((0, "raw"), (10, "compensated")):
            rows = [run_comp(TICKS, 4, 3, 12, 6, 10, s, mode, laghat) for s in SEEDS]
            pm, db, me = sum(r[0] for r in rows)//5, sum(r[1] for r in rows)//5, max(r[2] for r in rows)
            anchor_rows[(mode, tag)] = (pm, db, me)
            print("  %-28s %5d permille  debt %6d  maxErr %2d" % (mode+" "+tag, pm, db, me))
    a = anchor_rows
    okA = (a[("interference","compensated")] == (984, 17700, 28)
           and a[("sequential","compensated")][0] == 1000
           and a[("interference","raw")] == (830, 34995, 39)
           and a[("sequential","raw")][0] == 512)
    per_seed = [run_comp(TICKS,4,3,12,6,10,20260902,"interference",10)[0]]
    print("  anchor check: interference comp 984/17700/28, seq comp 1000, int raw 830/34995/39, seq raw 512 ->",
          "PASS" if okA else "FAIL")
    print()

    print("-- CANARY B: self-canary (mislabeled arm must be caught) --")
    mis = run_arm("adaptive", 20260902, invert_dial=True)
    # checker: an arm labeled 'adaptive' must run sequential-mode during the calm
    # and bursty segments (dial doctrine); the inverted dial runs interference there.
    caught = mis["seq_frac"]["calm"][1] > mis["seq_frac"]["calm"][0]
    print("  inverted-dial 'adaptive' @seed 20260902: calm-seq ticks %d vs calm-int ticks %d -> %s"
          % (mis["seq_frac"]["calm"][0], mis["seq_frac"]["calm"][1],
             "CAUGHT" if caught else "MISSED"))
    print()

    print("-- GRID: arms x seeds (real runs) --")
    ARMS = ("seq-raw", "int-raw", "seq-comp-fix", "int-comp-fix",
            "seq-comp-oracle", "int-comp-oracle", "adaptive")
    results = {arm: [run_arm(arm, s) for s in SEEDS] for arm in ARMS}
    statics = [a for a in ARMS if a != "adaptive"]
    print("  %-18s %6s %8s %7s  per-seed pm" % ("arm", "pm", "debt", "maxErr"))
    for arm in ARMS:
        rows = results[arm]
        print("  %-18s %5d‰ %8d %7d  %s" % (arm, mean_pm(rows), mean_debt(rows),
              max_err(rows), [r["pm"] for r in rows]))
        print("       seg pm (calm/conflict/bursty, mean): %s  debt-mean %d"
              % ("/".join(str(sum(r["seg_pm"][k] for r in rows)//5)
                          for k in ("calm", "conflict", "bursty")),
                 sum(r["debt"] for r in rows)//5))
    print()
    ad = results["adaptive"]
    for r in ad:
        print("  adaptive seed %-9d pm %4d‰ debt %6d switches %2d det_lag %s" %
              (r["seed"], r["pm"], r["debt"], r["switches"], r["det_lag"]))
    print("  adaptive interference-tick fraction per segment (mean):",
          {k: sum(r["int_frac"][k] for r in ad)//5 for k in ("calm","conflict","bursty")})
    print("  adaptive lag re-estimations (t, segment, laghat) seed 20260902:")
    for t_, s_, l_ in ad[-1]["lag_trace"]:
        print("    t=%4d %-9s laghat=%2d (true %s)" % (t_, s_, l_,
              {"calm": 5, "conflict": 10, "bursty": 10}[s_]))
    print()

    print("-- DECISION RULE --")
    best_static = max(statics, key=lambda a: mean_pm(results[a]))
    adpm, addebt = mean_pm(ad), mean_debt(ad)
    bs_rows = results[best_static]
    cond1 = adpm >= mean_pm(bs_rows) - 10
    cond2 = addebt * 10 <= 6 * mean_debt(bs_rows)   # debt <= 60% of best static
    print("  best static arm: %s (pm %d‰, debt %d)" % (best_static, mean_pm(bs_rows), mean_debt(bs_rows)))
    print("  adaptive pm %d‰ >= best-10? %s | adaptive debt %d <= 60%% of best static (%d)? %s"
          % (adpm, "YES" if cond1 else "NO", addebt, 6*mean_debt(bs_rows)//10, "YES" if cond2 else "NO"))
    print("  VERDICT:", "PROMOTE (E4 architecture + pre-load §3.2 QTORCH arm)"
          if (cond1 and cond2) else "BOOK BOUNDARY (detector lag vs regime dwell, numbers above)")
