#!/usr/bin/env python3
# ROUND 9 / Q2 — Minimal cofire homeostat, v2 charter predicate (predictability, not agreement).
# Charter: commit 987d6e4, ROUND-6-O6-cofire-homeostat.md §"Cofire v2 charter".
#   Trust scores lagged cross-PREDICTION: per-pair sign-product accumulator with
#   exponential decay  s <- s - (s>>D) + sign(i@t)*sign(j@t-lag) ; trust maps from |s|
#   (predictable at EITHER sign), demotion on |s| collapsing toward 0. A liar breaks
#   predictability, not agreement.
# PRE-REGISTERED CONSTANTS (fixed before the run, per charter point (a)):
#   D=6 (decay; steady-correlation plateau |s| ~ 2^6 = 64), SAT=128 (accumulator cap),
#   HI_TH=48 (predictability band), LO_TH=12 (unpredictability band), trust in [4,12] init 8,
#   neutral-decay interval 32 silent ticks (as round 6).
# ARMS (max 3 variants from the round-6 lane proposals + charter):
#   V2a  charter verbatim (sign-product accumulator from |s|).
#   V2b  charter + REFRACTORY window R=4 ticks after a twin's own trigger during which no
#        trust evidence is scored for that pair (glm-1 C's refractory proposal — damp echo).
#   V2c  charter + ASYMMETRIC descent: trust steps down only on every SLOW=2nd consecutive
#        unpredictable event, up unchanged (kimi #1 variant-B floor/decay flavor).
# GATES (charter):
#   G1' honest no-bleed: clean stress mean >=800 permille AND end-trust mean >=7.0.
#   G2' liar demotion: lying-T2 late-window trust <=5 on >=900 permille of ticks, T1 >=7.0.
#   G4  negative-correlation preservation: clean stress honest pair ends with |s| mean above
#       the band AND mean s negative AND trust >=7 (ends at/above INIT, not floor).
#   (G3 whistle reported as cross-check, not promotion-gating, per round-9 decision rule.)
# DECISION RULE: any variant passes G1' AND G2' AND G4 => promote with spec;
#   all fail => book "every local no-error-signal rule on the correction channel learns
#   silence" as the Q2 verdict with the failure numbers.
# CONSTRAINTS: integer-only, seeds (1,7,42,1999,20260902), 4800 ticks, calm+stress,
#   canaries: F17 anchor replay (verbatim kimi fabric, imported from o6 harness), lag blade,
#   mislabeled-arm self-canary, double-run byte-identity.
# Run: python3 dev-rounds/q2_cofire_minimal.py 2>&1 | tee dev-rounds/q2-cofire-minimal-output.txt
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import deque
from o6_cofire_homeostat import (kimi_run_trust, discover_lag, REGIMES, SEEDS,
                                 TICKS, WINDOW, MAXLAG, TRUST_LO, TRUST_HI, TRUST_N,
                                 DECAY_INTERVAL, LIE_START, LIE_END, NOISE, LIE, mean)
from e1 import LCG, reality

# ---- pre-registered v2 constants (see header) ----
D_ACC, SAT, HI_TH, LO_TH = 6, 128, 48, 12
REFRACTORY = 4      # variant V2b
SLOW = 2            # variant V2c
BAND = HI_TH        # G4 stability band

VARIANTS = ("v2a-charter", "v2b-refractory", "v2c-slowfloor")

# ============================================================================
# Fabric loop: identical semantics to o6_cofire_homeostat.run_arm (reused, not
# forked) — only the trust-update block is swapped for the v2 predicate.
# ============================================================================
def run_v2(regime, seed, fault="clean", variant="v2a-charter", learn=True,
           lag=None, ticks=TICKS):
    p = REGIMES[regime]
    delta, drift, K, pulse_div, lat2 = p["delta"], p["drift"], p["K"], p["pulse_div"], p["lat2"]
    if lag is None:
        lag = discover_lag(lat2)
    rng = LCG(seed)
    fault_rng = LCG(seed * 2 + 1)
    g = reality(0)
    pulses = deque()
    trust = [TRUST_N, TRUST_N]
    last_neutral = [-1, -1]          # last tick the neutral-decay pulled toward 8
    s_acc = [0, 0]                   # sign-product accumulators (per-twin predictability)
    bad_streak = [0, 0]              # V2c: consecutive unpredictable events
    last_trig = [-REFRACTORY, -REFRACTORY]
    HIST = lag + 2
    hist = [deque([0] * HIST, maxlen=HIST), deque([0] * HIST, maxlen=HIST)]
    snap_events = ledger_mass = cancellations = 0
    settles = 0
    cancel_lie = cancel_honest = lie_ticks = honest_ticks = 0
    t2_late_sum = t2_late_n = t2_floor_n = t1_late_sum = 0
    s_band_ticks = [0, 0]            # ticks with |s| above band (G4 evidence)
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
            if learn:
                m = m * trust[twin] // TRUST_N
            sgn = m if e > 0 else -m
            pulses.appendleft([sgn, K, twin])
            snap_events += 1
            ledger_mass += abs(e)
            hist[twin].append(1 if e > 0 else -1)
            last_trig[twin] = t
        fired = {twin for twin, _ in trig}
        for twin in (0, 1):
            if twin not in fired:
                hist[twin].append(0)
        # ---- v2 predicate: lagged cross-prediction, predictability not agreement ----
        if learn:
            for twin, other in ((0, 1), (1, 0)):
                cur = hist[twin][-1]
                ref = hist[other][-1 - lag] if len(hist[other]) > lag else 0
                if variant == "v2b-refractory" and t - last_trig[other] < REFRACTORY:
                    cur = cur  # refractory: suppress evidence near the echo (no-op guard, kept explicit)
                    ref = 0   # do not score reference pulses inside the refractory window
                if cur != 0 and ref != 0:
                    s_acc[twin] -= s_acc[twin] >> D_ACC
                    s_acc[twin] += cur * ref
                    if s_acc[twin] > SAT: s_acc[twin] = SAT
                    if s_acc[twin] < -SAT: s_acc[twin] = -SAT
                    a = s_acc[twin] if s_acc[twin] >= 0 else -s_acc[twin]
                    if a >= HI_TH:
                        trust[twin] = min(TRUST_HI, trust[twin] + 1)
                        bad_streak[twin] = 0
                        last_neutral[twin] = t
                    elif a <= LO_TH:
                        bad_streak[twin] += 1
                        if variant != "v2c-slowfloor" or (bad_streak[twin] % SLOW) == 0:
                            trust[twin] = max(TRUST_LO, trust[twin] - 1)
                        last_neutral[twin] = t
                    else:
                        last_neutral[twin] = t
                if t - last_neutral[twin] >= DECAY_INTERVAL:
                    if trust[twin] < TRUST_N: trust[twin] += 1
                    elif trust[twin] > TRUST_N: trust[twin] -= 1
                    last_neutral[twin] = t
                if t >= ticks - WINDOW:
                    aa = s_acc[twin] if s_acc[twin] >= 0 else -s_acc[twin]
                    if aa >= BAND: s_band_ticks[twin] += 1
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
        "s_end": tuple(s_acc),
        "s_band_frac": tuple(b * 1000 // WINDOW for b in s_band_ticks),
        "lag": lag,
        "lie_pm": lie_pm, "hon_pm": hon_pm,
        "whistle": (lie_pm * 10) // max(1, hon_pm),
        "t2_late_mean": (t2_late_sum * 10) // max(1, t2_late_n),
        "t2_floor_frac": (t2_floor_n * 1000) // max(1, t2_late_n),
        "t1_late_mean": (t1_late_sum * 10) // max(1, t2_late_n),
        "max_err": max_err,
        "variant": variant, "fault": fault, "regime": regime, "learn": learn,
    }

def fp(r):
    return (r["pm"], r["debt"], r["events"], r["cancels"], r["trust"], r["s_end"])

def sweep():
    rows = {}
    lag_c, lag_s = discover_lag(REGIMES["calm"]["lat2"]), discover_lag(REGIMES["stress"]["lat2"])
    for var in ("static",) + VARIANTS:
        for reg in ("stress", "calm"):
            key = (reg, "clean", var)
            rows[key] = [run_v2(reg, s, "clean", var if var != "static" else "v2a-charter",
                                learn=(var != "static")) for s in SEEDS]
        for fault in ("noisy", "lie"):
            key = ("stress", fault, var)
            rows[key] = [run_v2("stress", s, fault, var if var != "static" else "v2a-charter",
                                learn=(var != "static")) for s in SEEDS]
    return rows, (lag_c, lag_s)

def render(rows, lags):
    out = []
    def P(s=""):
        out.append(s); print(s)
    P("=" * 78)
    P("ROUND 9 / Q2 — MINIMAL COFIRE HOMEOSTAT, v2 CHARTER PREDICATE (predictability,")
    P("not agreement; commit 987d6e4). Integer sign-product accumulator D=%d SAT=%d," % (D_ACC, SAT))
    P("bands HI=%d LO=%d, trust [%d,%d] init %d, neutral-decay %d ticks." %
      (HI_TH, LO_TH, TRUST_LO, TRUST_HI, TRUST_N, DECAY_INTERVAL))
    P("Variants: %s | %s (R=%d) | %s (SLOW=%d). Seeds %s, %d ticks, integer-only." %
      (VARIANTS[0], VARIANTS[1], REFRACTORY, VARIANTS[2], SLOW, str(SEEDS), TICKS))
    P("Faults: clean / noisy-T2 +/-%d / lying-T2 +%d ticks [%d,%d)." %
      (NOISE, LIE, LIE_START, LIE_END))
    P("=" * 78)
    # -- CANARY A: F17 anchor replay (kimi fabric imported verbatim from o6 harness) --
    P("")
    P("-- CANARY A: F17 anchor replay (kimi exp1 variant A, sheet: 830/308/5) --")
    fpm, tpm, tcn, tfin = [], [], [], []
    for s in SEEDS:
        f = kimi_run_trust(seed=s, use_trust=False)
        tr = kimi_run_trust(seed=s, use_trust=True)
        fpm.append(f[0]); tpm.append(tr[0]); tcn.append(tr[2]); tfin.append(tr[3])
        P("  seed %9d  fixed %4d  trust-A %4d  cancel %d  trust=%s" %
          (s, f[0], tr[0], tr[2], str(tr[3])))
    okA = (mean(fpm) == 830 and mean(tpm) == 308 and mean(tcn) == 5)
    P("  means %d / %d / %d  CANARY A: %s" % (mean(fpm), mean(tpm), mean(tcn),
                                              "PASS" if okA else "FAIL"))
    P("")
    P("-- CANARY A2: lag blade (F19/F20) — calm %d (true 5), stress %d (true 10) -> %s" %
      (lags[0], lags[1], "PASS" if lags == (5, 10) else "FAIL"))
    # -- clean arms --
    P("")
    P("-- CLEAN, both regimes: static vs v2 variants --")
    for reg in ("stress", "calm"):
        for var in ("static",) + VARIANTS:
            rs = rows[(reg, "clean", var)]
            P("  %-6s %-15s pm/seed %-24s mean %4d permille  debt %6d  cancel %3d  "
              "trust(end) mean %d.%d  s_end mean %d  band-frac %d/%d permille" %
              (reg, var, str([r["pm"] for r in rs]), mean([r["pm"] for r in rs]),
               mean([r["debt"] for r in rs]), mean([r["cancels"] for r in rs]),
               mean([r["trust"][0] + r["trust"][1] for r in rs]) // 2,
               (mean([r["trust"][0] + r["trust"][1] for r in rs]) * 5) % 10,
               mean([r["s_end"][0] + r["s_end"][1] for r in rs]) // 2,
               mean([r["s_band_frac"][0] for r in rs]),
               mean([r["s_band_frac"][1] for r in rs])))
    # -- noisy / lie arms --
    for fault, label in (("noisy", "NOISY-T2 (+/-%d) STRESS" % NOISE),
                         ("lie", "LYING-T2 (+%d, [%d,%d)) STRESS" % (LIE, LIE_START, LIE_END))):
        P("")
        P("-- %s --" % label)
        for var in ("static",) + VARIANTS:
            rs = rows[("stress", fault, var)]
            for s, r in zip(SEEDS, rs):
                if var == "static":
                    P("  seed %9d  %-15s pm %4d  debt %6d  cancels %4d  whistle %d.%dx  maxE %d" %
                      (s, var, r["pm"], r["debt"], r["cancels"], r["whistle"] // 10,
                       r["whistle"] % 10, r["max_err"]))
                elif fault == "lie":
                    P("  seed %9d  %-15s pm %4d  debt %6d  cancels %4d  whistle %d.%dx  "
                      "t2_late %d.%d  floor %4d permille  t1_late %d.%d  maxE %d" %
                      (s, var, r["pm"], r["debt"], r["cancels"], r["whistle"] // 10,
                       r["whistle"] % 10, r["t2_late_mean"] // 10, r["t2_late_mean"] % 10,
                       r["t2_floor_frac"], r["t1_late_mean"] // 10, r["t1_late_mean"] % 10,
                       r["max_err"]))
                else:  # noisy: no lie window; report end-trust instead of lie-window metrics
                    P("  seed %9d  %-15s pm %4d  debt %6d  cancels %4d  trust(end)=(%d,%d)  "
                      "s_end=(%d,%d)  maxE %d" %
                      (s, var, r["pm"], r["debt"], r["cancels"], r["trust"][0],
                       r["trust"][1], r["s_end"][0], r["s_end"][1], r["max_err"]))
    # -- CANARY B: mislabeled-arm self-canary --
    P("")
    P("-- CANARY B: self-canary (lie static run mislabeled as v2a) --")
    truth_v2a = rows[("stress", "lie", "v2a-charter")][0]
    fake = run_v2("stress", SEEDS[0], "lie", "v2a-charter", learn=False)  # relabeled static
    caught = fp(fake) != fp(truth_v2a)
    P("  fingerprint static-as-v2a: pm %d debt %d events %d cancels %d trust=%s s=%s" %
      (fake["pm"], fake["debt"], fake["events"], fake["cancels"], str(fake["trust"]),
       str(fake["s_end"])))
    P("  fingerprint true v2a    : pm %d debt %d events %d cancels %d trust=%s s=%s" %
      (truth_v2a["pm"], truth_v2a["debt"], truth_v2a["events"], truth_v2a["cancels"],
       str(truth_v2a["trust"]), str(truth_v2a["s_end"])))
    P("  CANARY B: %s" % ("CAUGHT" if caught else "MISSED"))
    # -- gates --
    P("")
    P("=" * 78)
    P("DECISION-RULE EVALUATION (charter gates G1'/G2'/G4; G3 whistle cross-check)")
    P("=" * 78)
    any_pass = False
    for var in VARIANTS:
        cl = rows[("stress", "clean", var)]
        hpm = mean([r["pm"] for r in cl])
        htr = mean([r["trust"][0] + r["trust"][1] for r in cl]) // 2
        li = rows[("stress", "lie", var)]
        flr = mean([r["t2_floor_frac"] for r in li])
        t1m = mean([r["t1_late_mean"] for r in li])
        wh = mean([r["whistle"] for r in li])
        send = mean([r["s_end"][0] + r["s_end"][1] for r in li[:0]] or
                    [r["s_end"][0] + r["s_end"][1] for r in cl]) // 2
        bandf = mean([r["s_band_frac"][0] + r["s_band_frac"][1] for r in cl]) // 2
        g1 = hpm >= 800 and htr >= 7
        g2 = flr >= 900 and t1m >= 70
        g4 = bandf >= 500 and send < 0 and htr >= 7
        any_pass = any_pass or (g1 and g2 and g4)
        P("%s:" % var)
        P("  G1' honest no-bleed : pm %4d permille (>=800), end-trust %d (>=7)      -> %s" %
          (hpm, htr, "PASS" if g1 else "FAIL"))
        P("  G2' liar to floor   : floor-frac %4d permille (>=900), T1 %d.%d (>=7.0) -> %s" %
          (flr, t1m // 10, t1m % 10, "PASS" if g2 else "FAIL"))
        P("  G4  neg-corr kept   : s_end mean %d (<0), band-frac %d permille (>=500), "
          "trust %d (>=7) -> %s" % (send, bandf, htr, "PASS" if g4 else "FAIL"))
        P("  G3  whistle (x-check): %d.%dx" % (wh // 10, wh % 10))
    P("")
    P("VERDICT: %s" %
      ("PROMOTE cofire v2 (predictability predicate) with spec" if any_pass else
       "ALL VARIANTS FAIL — book Q2: every local no-error-signal rule on the correction "
       "channel learns silence (family demotes to monitor-only per the charter falsifier)"))
    P("")
    okA2 = lags == (5, 10)
    P("CANARIES: A %s / A2 %s / B %s" %
      ("PASS" if okA else "FAIL", "PASS" if okA2 else "FAIL", "CAUGHT" if caught else "MISSED"))
    return "\n".join(out) + "\n", any_pass, (okA, okA2, caught)

def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def main():
    rows, lags = sweep()
    text, anyp, canaries = render(rows, lags)
    rows2, lags2 = sweep()          # double-run byte-identity canary
    text2, _, _ = render(rows2, lags2)
    print("")
    print("CANARY C (double-run byte-identity): %s  (sha %s / %s)" %
          ("PASS" if text == text2 else "FAIL", digest(text), digest(text2)))
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "q2-cofire-minimal-output.txt")
    with open(path, "w") as fh:
        fh.write(text)
        fh.write("CANARY C (double-run byte-identity): %s  (sha %s / %s)\n" %
                 ("PASS" if text == text2 else "FAIL", digest(text), digest(text2)))
    print("[log written to %s]" % path)

if __name__ == "__main__":
    main()
