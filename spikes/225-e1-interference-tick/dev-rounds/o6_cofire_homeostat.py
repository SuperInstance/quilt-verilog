#!/usr/bin/env python3
# O6 — Cofire homeostat micro-probe (RESEARCH-AGENDA.md §4 O6; from S1/F17/F21/F8).
# Minimal repair of charter §1.2 cofire collapse (three independent lanes):
#   (1) BOUNDED trust in [4,12], init 8, with decay toward neutral 8 (homeostat
#       proper: kimi #1's floor/decay proposal, bounded so it cannot learn deafness).
#   (2) LAGGED reference credit assignment (opencode #2 — the only discriminative
#       ingredient): judge twin i's trigger sign at t against twin j's trigger sign
#       at t-lag (the same reality point, kimi #3 / opencode #1 first-difference
#       blade), NOT against the same-tick pulse queue (kimi #1's update read the
#       fabric's own echo; glm-1 C showed the echo self-locks at tau=3).
# Fault models: clean, noisy-T2 (+/-14 sensor noise), lying-T2 (+24 lie,
# ticks 1200..2399 — glm-1 A's attack window). Whistle = cancellation permille
# lie-window vs honest-window (F6 cross-check, expect >=2x on a defector).
# Integer-only. Fixed seeds. Reuses e1.py LCG/reality; kimi exp1 fabric reused.
# Run: python3 dev-rounds/o6_cofire_homeostat.py   (write to log via tee)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import deque
from e1 import LCG, reality

SEEDS = (1, 7, 42, 1999, 20260902)
TICKS = 4800
WINDOW, MAXLAG = 480, 15
TRUST_LO, TRUST_HI, TRUST_N = 4, 12, 8
DECAY_INTERVAL = 32          # ticks without evidence before homeostat pulls to 8
LIE_START, LIE_END = 1200, 2400
NOISE = 14
LIE = 24

REGIMES = {
    "stress": dict(delta=12, drift=6, K=4, pulse_div=3, lat2=10),
    "calm":   dict(delta=6,  drift=3, K=8, pulse_div=3, lat2=5),
}

# ============================================================================
# CANARY A — kimi exp1 variant A, verbatim from INVENTIONS-kimi.md sheet #1.
# F17 anchor: stress fixed mean 830 permille, trust-A mean 308, cancel mean 5.
# ============================================================================
def kimi_run_trust(ticks=4800, K=4, pulse_div=3, delta=12, drift=6, lat2=10,
                   seed=1, use_trust=True):
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()          # [signed_mag, remaining_life, twin_id]
    trust = [8, 8]
    snap_events = ledger_mass = cancellations = 0
    settles = 0
    for t in range(ticks):
        s1 = reality(t)
        s2 = reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        trig = []
        e1v, e2v = s1 - g, s2 - g
        if abs(e1v) > delta: trig.append((0, e1v))
        if abs(e2v) > delta: trig.append((1, e2v))
        for twin, e in trig:
            m = abs(e) // pulse_div or 1
            if use_trust:
                m = m * trust[twin] // 8
            if m == 0:
                continue
            sgn = m if e > 0 else -m
            if use_trust:
                for pmag, plife, ptwin in pulses:
                    if ptwin == twin: continue
                    if (pmag > 0) == (sgn > 0):
                        trust[ptwin] = min(16, trust[ptwin] + 1)   # A: j predicted me
                    else:
                        trust[ptwin] = max(0, trust[ptwin] - 1)    # A: j contradicted
        # (sheet's inner loop ends with pulse append; kept identical below)
            pulses.appendleft([sgn, K, twin])
            snap_events += 1
            ledger_mass += abs(e)
        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
            decayed = deque()
            for mag, life, twin in pulses:
                if life > 0:
                    if abs(mag) > 1: mag = mag - (mag // 2)
                    decayed.append([mag, life - 1, twin])
            pulses = decayed
            g += net
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1
    return settles * 1000 // ticks, ledger_mass, cancellations, tuple(trust)

# ============================================================================
# Lag blade — kimi exp3 / opencode #1 first-difference cross-correlation
# (verbatim from dev-rounds/o4_regime_motion.py canary).
# ============================================================================
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

# ============================================================================
# O6 arm — kimi exp1 fabric + bounded homeostat + lagged-reference credit.
# ============================================================================
def run_arm(regime, seed, fault="clean", homeostat=True, lag=None, ticks=TICKS):
    """fault: clean | noisy (T2 +/-14) | lie (T2 +24 in [1200,2400)).
    homeostat=False -> static trust 8 (kimi 'fixed' arm; whistle baseline).
    Returns fingerprint dict."""
    p = REGIMES[regime]
    delta, drift, K, pulse_div, lat2 = p["delta"], p["drift"], p["K"], p["pulse_div"], p["lat2"]
    if lag is None:
        lag = discover_lag(lat2)          # the fabric calibrates itself (S2 doctrine)
    rng = LCG(seed)
    fault_rng = LCG(seed * 2 + 1)         # dedicated stream: fault injection never
    g = reality(0)                        # perturbs the base drift stream
    pulses = deque()
    trust = [TRUST_N, TRUST_N]
    last_evidence = [-DECAY_INTERVAL, -DECAY_INTERVAL]
    # trigger-sign history per twin, for lagged reference (0 = no trigger)
    HIST = lag + 2
    hist = [deque([0] * HIST, maxlen=HIST), deque([0] * HIST, maxlen=HIST)]
    snap_events = ledger_mass = cancellations = 0
    settles = 0
    # whistle bookkeeping
    cancel_lie = cancel_honest = lie_ticks = honest_ticks = 0
    # demotion bookkeeping
    t2_late_sum = t2_late_n = t2_floor_n = t1_late_sum = 0
    max_err = 0
    for t in range(ticks):
        s1 = reality(t)
        s2 = reality(max(0, t - lat2))
        if fault == "noisy":
            s2 += fault_rng.below(2 * NOISE + 1) - NOISE
        elif fault == "lie" and LIE_START <= t < LIE_END:
            s2 += LIE
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        trig = []
        e1v, e2v = s1 - g, s2 - g
        if abs(e1v) > delta: trig.append((0, e1v))
        if abs(e2v) > delta: trig.append((1, e2v))
        for twin, e in trig:
            m = abs(e) // pulse_div or 1
            if homeostat:
                m = m * trust[twin] // TRUST_N
            sgn = m if e > 0 else -m
            pulses.appendleft([sgn, K, twin])
            snap_events += 1
            ledger_mass += abs(e)
            hist[twin].append(1 if e > 0 else -1)
        fired = {twin for twin, _ in trig}
        for twin in (0, 1):
            if twin not in fired:
                hist[twin].append(0)
        # -- lagged-reference credit assignment (opencode #2 ingredient) --
        if homeostat:
            for twin, other in ((0, 1), (1, 0)):
                cur = hist[twin][-1]
                ref = hist[other][-1 - lag] if len(hist[other]) > lag else 0
                if cur != 0 and ref != 0:
                    if cur == ref:
                        trust[twin] = min(TRUST_HI, trust[twin] + 1)   # cofire at the lag
                    else:
                        trust[twin] = max(TRUST_LO, trust[twin] - 1)   # anti-cofire
                    last_evidence[twin] = t
                # bounded homeostat: decay toward neutral 8 when silent
            for twin in (0, 1):
                if t - last_evidence[twin] >= DECAY_INTERVAL:
                    if trust[twin] < TRUST_N: trust[twin] += 1
                    elif trust[twin] > TRUST_N: trust[twin] -= 1
                    last_evidence[twin] = t
        if pulses:
            net = sum(q[0] for q in pulses)
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
                if fault == "lie":
                    if LIE_START <= t < LIE_END: cancel_lie += 1
                    else: cancel_honest += 1
            decayed = deque()
            for mag, life, twin in pulses:
                if life > 0:
                    if abs(mag) > 1: mag = mag - (mag // 2)
                    decayed.append([mag, life - 1, twin])
            pulses = decayed
            g += net
        if fault == "lie":
            if LIE_START <= t < LIE_END: lie_ticks += 1
            else: honest_ticks += 1
        if fault == "lie" and LIE_START + 100 <= t < LIE_END:
            t2_late_sum += trust[1]; t2_late_n += 1
            t1_late_sum += trust[0]
            if trust[1] <= 5: t2_floor_n += 1
        err = max(abs(s1 - g), abs(s2 - g))
        if err > max_err: max_err = err
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1
    lie_pm = cancel_lie * 1000 // max(1, lie_ticks)
    hon_pm = cancel_honest * 1000 // max(1, honest_ticks)
    return {
        "pm": settles * 1000 // ticks,
        "debt": ledger_mass,
        "events": snap_events,
        "cancels": cancellations,
        "trust": tuple(trust),
        "lag": lag,
        "lie_pm": lie_pm, "hon_pm": hon_pm,
        "whistle": (lie_pm * 10) // max(1, hon_pm),   # tenths of x
        "t2_late_mean": (t2_late_sum * 10) // max(1, t2_late_n),  # tenths
        "t2_floor_frac": (t2_floor_n * 1000) // max(1, t2_late_n),  # permille
        "t1_late_mean": (t1_late_sum * 10) // max(1, t2_late_n),
        "max_err": max_err,
    }

def mean(xs):
    return sum(xs) // len(xs)

# ============================================================================
def main():
    out = []
    def P(s=""):
        out.append(s)
        print(s)

    P("=" * 78)
    P("O6 COFIRE HOMEOSTAT MICRO-PROBE — branch g3-kinduction — 2026-09-03")
    P("trust in [%d,%d] init %d, decay->%d every %d silent ticks; lagged (first-diff," %
      (TRUST_LO, TRUST_HI, TRUST_N, TRUST_N, DECAY_INTERVAL))
    P("480-tick blade) reference credit. Faults: clean / noisy-T2 +/-%d / lying-T2 +%d [%d,%d)." %
      (NOISE, LIE, LIE_START, LIE_END))
    P("ticks=%d, seeds=%s, integer-only." % (TICKS, str(SEEDS)))
    P("=" * 78)

    # ---------------- CANARY A: F17 anchor replay (kimi verbatim) ------------
    P("")
    P("-- CANARY A: kimi exp1 variant A verbatim (F17 anchor: 830 -> 308 permille) --")
    fixed_pm, trustA_pm, trustA_cancel, trustA_final = [], [], [], []
    for s in SEEDS:
        f = kimi_run_trust(seed=s, use_trust=False)
        tr = kimi_run_trust(seed=s, use_trust=True)
        fixed_pm.append(f[0]); trustA_pm.append(tr[0]); trustA_cancel.append(tr[2])
        trustA_final.append(tr[3])
        P("  seed %9d  fixed %4d permille  trust-A %4d permille  cancel %d  trust=%s" %
          (s, f[0], tr[0], tr[2], str(tr[3])))
    P("  means: fixed %d  trust-A %d  cancel %d  (sheet: 830 / 308 / 5)" %
      (mean(fixed_pm), mean(trustA_pm), mean(trustA_cancel)))
    ok_a = (mean(fixed_pm) == 830 and mean(trustA_pm) == 308
            and mean(trustA_cancel) == 5)
    P("  CANARY A: %s" % ("PASS" if ok_a else "FAIL"))

    # ---------------- CANARY A2: lag blade exact ----------------
    P("")
    P("-- CANARY A2: first-difference lag blade (F19/F20: exact lags) --")
    reads = [discover_lag(REGIMES[r]["lat2"]) for r in ("calm", "stress")]
    P("  calm lag %d (true 5)  stress lag %d (true 10)  -> %s" %
      (reads[0], reads[1], "PASS" if reads == [5, 10] else "FAIL"))

    # ---------------- arm sweep ----------------
    rows = {}
    P("")
    P("-- ARM 1: clean homeostat vs static (honest twins; both regimes) --")
    for reg in ("stress", "calm"):
        for arm in ("static", "homeostat"):
            key = (reg, "clean", arm)
            rows[key] = [run_arm(reg, s, "clean", arm == "homeostat") for s in SEEDS]
            pms = [r["pm"] for r in rows[key]]
            P("  %-6s clean %-10s pm/seed %s  mean %4d permille  debt %6d  cancel %d  trust(end) mean %.1f" %
              (reg, arm, str(pms), mean(pms), mean([r["debt"] for r in rows[key]]),
               mean([r["cancels"] for r in rows[key]]),
               mean([r["trust"][0] for r in rows[key]]) / 1))
    P("")
    P("-- ARM 2: noisy-T2 (+/-%d) stress: static vs homeostat --" % NOISE)
    for arm in ("static", "homeostat"):
        key = ("stress", "noisy", arm)
        rows[key] = [run_arm("stress", s, "noisy", arm == "homeostat") for s in SEEDS]
        for s, r in zip(SEEDS, rows[key]):
            P("  seed %9d  %-10s pm %4d  debt %6d  events %4d  trust=(%d,%d)" %
              (s, arm, r["pm"], r["debt"], r["events"], r["trust"][0], r["trust"][1]))
    P("")
    P("-- ARM 3: lying-T2 (+%d in [%d,%d)) stress: static vs homeostat --" %
      (LIE, LIE_START, LIE_END))
    for arm in ("static", "homeostat"):
        key = ("stress", "lie", arm)
        rows[key] = [run_arm("stress", s, "lie", arm == "homeostat") for s in SEEDS]
        for s, r in zip(SEEDS, rows[key]):
            P("  seed %9d  %-10s pm %4d  debt %6d  cancels %4d  whistle %d.%dx  "
              "t2_late %d.%d  floor-frac %4d permille  t1_late %d.%d  maxE %d" %
              (s, arm, r["pm"], r["debt"], r["cancels"], r["whistle"] // 10, r["whistle"] % 10,
               r["t2_late_mean"] // 10, r["t2_late_mean"] % 10, r["t2_floor_frac"],
               r["t1_late_mean"] // 10, r["t1_late_mean"] % 10, r["max_err"]))
    # noisy-window demotion summary (late-window trust for noisy arm, recomputed cheaply
    # from full-run trust trajectory is not stored; use trust dynamics summary instead)
    P("")

    # ---------------- CANARY B: self-canary (mislabeled arm must be caught) --
    P("-- CANARY B: self-canary (lie-static run mislabeled as lie-homeostat) --")
    truth = rows[("stress", "lie", "static")][0]
    fake_label = "homeostat"
    claimed = run_arm("stress", SEEDS[0], "lie", homeostat=False)  # relabeled static
    fp_true = rows[("stress", "lie", "homeostat")][0]
    caught = (claimed["events"] != fp_true["events"] or claimed["debt"] != fp_true["debt"]
              or claimed["cancels"] != fp_true["cancels"] or claimed["pm"] != fp_true["pm"])
    P("  fingerprint static-as-%s: pm %d debt %d events %d cancels %d" %
      (fake_label, claimed["pm"], claimed["debt"], claimed["events"], claimed["cancels"]))
    P("  fingerprint true homeostat : pm %d debt %d events %d cancels %d" %
      (fp_true["pm"], fp_true["debt"], fp_true["events"], fp_true["cancels"]))
    P("  CANARY B: %s" % ("CAUGHT" if caught else "MISSED"))

    # ---------------- decision-rule evaluation ----------------
    P("")
    P("=" * 78)
    P("DECISION RULE EVALUATION (pre-registered)")
    P("=" * 78)
    clean_hs = rows[("stress", "clean", "homeostat")]
    honest_pm = mean([r["pm"] for r in clean_hs])
    P("GATE 1 honest steady-state: clean homeostat stress mean %d permille (gate >=800) -> %s" %
      (honest_pm, "PASS" if honest_pm >= 800 else "FAIL"))
    lie_hs = rows[("stress", "lie", "homeostat")]
    dem = mean([r["t2_late_mean"] for r in lie_hs])
    floor = mean([r["t2_floor_frac"] for r in lie_hs])
    t1ok = mean([r["t1_late_mean"] for r in lie_hs])
    P("GATE 2 defector demotion: lie-window T2 trust mean %d.%d (gate <=5.0), "
      "floor-frac %d permille (gate >=900), T1 trust %d.%d (gate >=7.0) -> %s" %
      (dem // 10, dem % 10, floor, t1ok // 10, t1ok % 10,
       "PASS" if (dem <= 50 and floor >= 900 and t1ok >= 70) else "FAIL"))
    wh = mean([r["whistle"] for r in lie_hs])
    whs = mean([r["whistle"] for r in rows[("stress", "lie", "static")]])
    P("GATE 3 whistle: homeostat lie/honest cancel ratio mean %d.%dx (gate >=2.0x); "
      "static baseline %d.%dx -> %s" %
      (wh // 10, wh % 10, whs // 10, whs % 10, "PASS" if wh >= 20 else "FAIL"))
    no_hs = rows[("stress", "noisy", "homeostat")]
    no_pm = mean([r["pm"] for r in no_hs])
    no_st = mean([r["pm"] for r in rows[("stress", "noisy", "static")]])
    P("SECONDARY noisy-T2: homeostat %d vs static %d permille; debt %d vs %d; "
      "end-trust pairs %s" %
      (no_pm, no_st, mean([r["debt"] for r in no_hs]),
       mean([r["debt"] for r in rows[("stress", "noisy", "static")]]),
       str([r["trust"] for r in no_hs])))
    calm_hs = rows[("calm", "clean", "homeostat")]
    P("SECONDARY calm (K=8 artifact regime, F13): homeostat %d vs static %d permille" %
      (mean([r["pm"] for r in calm_hs]),
       mean([r["pm"] for r in rows[("calm", "clean", "static")]])))
    verdict = ok_a and reads == [5, 10] and caught and honest_pm >= 800 and \
        dem <= 50 and floor >= 900 and t1ok >= 70 and wh >= 20
    P("")
    P("VERDICT: cofire v1.1 %s into the §3.2 demo arm" %
      ("SURVIVES" if verdict else "DEMOTE -> v2 (charter failure mode (c)); demo runs selection-only"))

    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "o6-cofire-output.txt"), "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("\n[log written to o6-cofire-output.txt]")

if __name__ == "__main__":
    main()
