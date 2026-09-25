#!/usr/bin/env python3
# Q7 — Minimal regime-gating dial (RESEARCH-AGENDA.md open tier, charter §5.4).
# Round 14. Reuses O4's protocol, environment, arms, κ-detector and live lag
# blade VERBATIM (o4_regime_motion.py); adds the 3-register dial per the
# pre-registered spec in ROUND-14-Q7-regime-dial.md PART 1.
# Integer-only; no multiply in the dial path (adds/subs/compares//2 only).
# Run: python3 dev-rounds/q7_regime_dial.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import deque
from e1 import LCG, reality
from o4_regime_motion import (SEEDS, TICKS, SEG_A, SEG_B, WINDOW, MAXLAG,
                              CALM, CONFLICT, seg, seg_name, Detector,
                              discover_lag_obs, discover_lag,
                              run_arm, mean_pm, mean_debt, max_err)

JUMP_THRESH = 40          # single-tick aligned-reading jump => transient (glitch)
TRANS_WIN = 16            # transient-hit window length (detector idiom)
TRANS_ARM = 2             # hits needed to set the bursty bit beta
GLITCH_DEFAULT = 45

# F14 sort gate (rounds 2/3): mag key, C=1, active only at N >= 6.
F14_N_GATE = 6
N_TWINS = 2


def f14_gate(cands, n):
    """Return cands with at most the single largest-|e| trigger when n >= 6.
    Inert at n < 6. Integer compares only."""
    if n < F14_N_GATE or len(cands) <= 1:
        return cands, 0
    best = 0
    for i in range(1, len(cands)):
        if abs(cands[i]) > abs(cands[best]):
            best = i
    return [cands[best]], len(cands) - 1


def run_dial(seed, force_lag=None, no_filter=False, invert=False,
             glitch_mag=GLITCH_DEFAULT, f14_n=N_TWINS, label="dial",
             beta_gated_filter=False, beta_latch=False):
    """The Q7 dial arm. Registers: R1=L^, R2=sigma (stress bit), R3=beta (bursty bit).
    Outputs: mode, K, pd (pulse_div), phase-decay, td; per-stream transient
    suppressor; F14 mag/C=1 sort gate at N>=6; live lag compensation (O4 frame)."""
    rng = LCG(seed); grng = LCG(seed ^ 0x5A5A)
    g = reality(0)
    pulses = deque()
    det = Detector()
    s1h = [0]*TICKS; s2h = [0]*TICKS
    laghat = 0                     # R1
    sigma = 0                      # R2 stress bit
    trans_w = [0]*TRANS_WIN; twidx = 0   # R3 sensor window
    beta_latched = 0; quiet = 0          # latch variant (amendment, labeled)
    mode = "sequential"; prev_mode = mode
    settles = debt = max_err = 0
    seg_st = {"calm": 0, "conflict": 0, "bursty": 0}
    seg_debt = {"calm": 0, "conflict": 0, "bursty": 0}
    seq_frac = {"calm": [0, 0], "conflict": [0, 0], "bursty": [0, 0]}
    switches = 0; suppressed = 0; rejected = 0; f14_events = 0
    beta_trace = {"calm": 0, "conflict": 0, "bursty": 0}
    pd_ticks = 0
    prev_a1 = prev_a2 = 0

    for t in range(TICKS):
        delta_e, drift, lat2, grn = seg(t)
        s1 = reality(t); s2 = reality(max(0, t - lat2))
        glitch = 0
        if grn and grng.below(grn) == 0:
            glitch = glitch_mag if grng.below(2) == 0 else -glitch_mag
        s1 += glitch; s2 += glitch
        s1h[t] = s1; s2h[t] = s2
        g += rng.below(2 * drift + 1) - drift

        # --- R1: fast path — live blade (O4 verbatim) ---
        if t >= WINDOW and t % WINDOW == 0:
            laghat = discover_lag_obs(s1h, s2h, t)
            if force_lag is not None:
                laghat = force_lag
        if force_lag is not None:
            laghat = force_lag

        # --- R2: sigma = fast (blade) OR slow (kappa confirm) ---
        sigma = (1 if laghat >= 8 else 0) | (1 if det.regime == CONFLICT else 0)

        # --- R3: beta = bursty bit (transient hits in last 16 ticks >= 2) ---
        if beta_latch:
            # latch: arm at >=2 hits/16; release after 32 consecutive hit-free ticks
            if sum(trans_w) >= TRANS_ARM:
                beta_latched = 1; quiet = 0
            elif beta_latched:
                quiet += 1
                if quiet >= 32:
                    beta_latched = 0; quiet = 0
            beta = beta_latched
        else:
            beta = 1 if sum(trans_w) >= TRANS_ARM else 0

        # --- outputs ---
        stress_now = sigma and not beta
        mode = "interference" if stress_now else "sequential"
        if invert:
            mode = "sequential" if stress_now else "interference"
        K = 1 if stress_now else 8            # O1: K small under stress
        pulse_div = 2 if stress_now else 3    # O1 champion pd=2
        td = 12 if stress_now else 6
        phase_decay = stress_now              # O5: pd-doubling on for stress/conflict
        if mode != prev_mode:
            switches += 1
        prev_mode = mode
        lag_eff = laghat

        # --- aligned readings (O4 live-realizable compensation frame) ---
        a1 = s1h[max(0, t - lag_eff)]
        a2 = s2h[t]

        # --- transient suppressor (per aligned stream, single tick) ---
        # POST-HOC AMENDMENT (dial-v2, labeled): beta_gated_filter disables the
        # suppressor while beta=1 (bursty) -- chasing settles glitch ticks and
        # the bursty %w ceiling under suppression is ~54%. NOT gate-eligible.
        filt_off = no_filter or (beta_gated_filter and beta)
        e1v, e2v = a1 - g, a2 - g
        hit = 0
        if filt_off:
            pass
        else:
            if t > 0:
                if abs(a1 - prev_a1) >= JUMP_THRESH:
                    e1v = None; hit = 1
                if abs(a2 - prev_a2) >= JUMP_THRESH:
                    e2v = None; hit = 1
            suppressed += hit
        trans_w[twidx] = hit; twidx = (twidx + 1) % TRANS_WIN
        prev_a1, prev_a2 = a1, a2

        trig = []
        if e1v is not None and abs(e1v) > td:
            trig.append(e1v)
        if e2v is not None and abs(e2v) > td:
            trig.append(e2v)
        if len(trig) > 1:
            f14_events += 1
        trig, rej = f14_gate(trig, f14_n)
        rejected += rej

        # --- plant (O4 loop structure; pd halving doubled when phase_decay) ---
        tick_debt = 0
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        if mode == "sequential":
            if trig:
                g += trig[0]; tick_debt = abs(trig[0]); debt += tick_debt
        else:
            for e in trig:
                pm = abs(e) // pulse_div or 1
                pulses.appendleft([pm if e > 0 else -pm, K]); tick_debt += abs(e)
            debt += tick_debt
            if pulses:
                net = sum(p[0] for p in pulses)
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1:
                            mag = mag - (mag // 2)
                            if phase_decay and abs(mag) > 1:
                                mag = mag - (mag // 2)
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
        # feed the SAME plant telemetry the O4 detector consumed (tick debt,
        # cancel flag, snap event) so the kappa organ sees an honest plant
        cancel_flag = 0
        if mode == "interference" and pulses:
            net = sum(p[0] for p in pulses) if pulses else 0
        det.tick(tick_debt, cancel_flag, 1 if trig else 0)

        sn = seg_name(t)
        seg_debt[sn] += tick_debt
        if abs(a1 - g) <= delta_e and abs(a2 - g) <= delta_e:
            settles += 1
            seg_st[sn] += 1
        err = max(abs(a1 - g), abs(a2 - g))
        if err > max_err: max_err = err
        seq_frac[sn][0 if mode == "sequential" else 1] += 1
        beta_trace[sn] += beta

    return dict(arm=label, seed=seed, pm=settles * 1000 // TICKS, debt=debt,
                max_err=max_err, switches=switches, suppressed=suppressed,
                rejected=rejected,
                seg_pm={k: v * 1000 // 1600 for k, v in seg_st.items()},
                seg_debt=seg_debt, seq_frac=seq_frac, beta_frac=beta_trace)


def seg_pm_mean(rows, k):
    return sum(r["seg_pm"][k] for r in rows) // len(rows)


def seg_debt_mean(rows, k):
    return sum(r["seg_debt"][k] for r in rows) // len(rows)


def canary_anchors():
    """Canary 2: O4/F19 anchor replay (verbatim O4 canary machinery)."""
    print("-- CANARY 2: O4/F19 anchor replay --")
    ok = True
    for lat2 in (3, 5, 7, 10, 15):
        got = discover_lag(lat2)
        good = got == lat2
        ok &= good
        print("  blade true lag %2d -> %2d  %s" % (lat2, got, "OK" if good else "FAIL"))
    from o4_regime_motion import run_arm as _ra
    ad = [_ra("adaptive", s) for s in SEEDS]
    adpm, addebt = mean_pm(ad), mean_debt(ad)
    good = (adpm == 932 and addebt == 57136)
    ok &= good
    print("  O4 adaptive replay: pm %d permille debt %d (expect 932/57136)  %s"
          % (adpm, addebt, "OK" if good else "FAIL"))
    # F19 stress anchors via run_comp (O4 canary semantics, verbatim port)
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
    rows = [run_comp(TICKS, 4, 3, 12, 6, 10, s, "interference", 10) for s in SEEDS]
    ic = (sum(r[0] for r in rows) // 5, sum(r[1] for r in rows) // 5,
          max(r[2] for r in rows))
    good = ic == (984, 17700, 28)
    ok &= good
    print("  F19 int-comp anchor (5-seed mean): %s (expect (984, 17700, 28))  %s"
          % (ic, "OK" if good else "FAIL"))
    rowsc = [run_comp(TICKS, 4, 3, 12, 6, 10, s, "sequential", 10) for s in SEEDS]
    sc = sum(r[0] for r in rowsc) // 5
    good = sc == 1000
    ok &= good
    print("  F19 seq-comp anchor pm (5-seed mean): %d (expect 1000)  %s" % (sc, "OK" if good else "FAIL"))
    return ok


def dial_signature():
    """CANARY 4 helper: run the dial + adaptive arms twice, return comparable signature."""
    sig = []
    for s in SEEDS:
        r = run_dial(s, label="dial")
        sig.append((r["pm"], r["debt"], r["max_err"], r["switches"], r["suppressed"]))
    for s in SEEDS:
        r = run_arm("adaptive", s)
        sig.append((r["pm"], r["debt"], r["max_err"], r["switches"]))
    return sig


def main():
    out = []
    def p(s=""):
        print(s); out.append(s)

    p("== Q7 ROUND 14: minimal regime-gating dial (calm->conflict->bursty, %d ticks x 5 seeds) ==" % TICKS)
    p("segments: calm [0,%d) d6/d3/lat5 | conflict [%d,%d) d12/d6/lat10 | bursty [%d,%d) d6/d3/lat10 + 1-in-4 +/-45 glitches"
      % (SEG_A, SEG_A, SEG_B, SEG_B, TICKS))
    p("dial: R1=L^ (blade, fast) R2=sigma (stress: blade>=8 OR kappa) R3=beta (bursty: >=2 transients/16)")
    p("outputs: mode int<->seq, K=1/pd=2+phase-decay under stress-confirmed, td 12/6, transient suppressor >=40, F14 mag/C=1 gate at N>=6 (inert at N=2)")
    p("")

    # ---- CANARY 1: F14 gate unit checks ----
    p("-- CANARY 1: F14 sort gate unit checks --")
    cands = [3, -17, 5, 44, -2, 9]
    kept, rej = f14_gate(cands, 6)
    c1 = (kept == [44] and rej == 5)
    kept2, rej2 = f14_gate(cands, 2)
    c1b = (kept2 == cands and rej2 == 0)
    p("  N=6: %s kept 1/6, rejected %d  %s" % (kept, rej, "OK" if c1 else "FAIL"))
    p("  N=2: inert (kept all, rejected %d)  %s" % (rej2, "OK" if c1b else "FAIL"))
    p("")

    # ---- CANARY 2: O4/F19 anchors ----
    c2 = canary_anchors()
    p("  ANCHOR SET: %s" % ("PASS" if c2 else "FAIL"))
    p("")

    # ---- CANARY 3: self-canary (mislabeled arms must be caught) ----
    p("-- CANARY 3: self-canary --")
    mis = run_dial(20260902, invert=True, label="dial-inverted")
    caught_mode = mis["seq_frac"]["calm"][1] > mis["seq_frac"]["calm"][0]
    p("  inverted-dial 'dial' @20260902: calm-seq %d vs calm-int %d ticks -> %s"
      % (mis["seq_frac"]["calm"][0], mis["seq_frac"]["calm"][1],
         "CAUGHT" if caught_mode else "MISSED"))
    full = run_dial(42, label="dial")
    nof = run_dial(42, no_filter=True, label="dial-nofilter")
    fp = lambda r: (r["pm"], r["debt"], r["suppressed"])
    caught_filt = fp(full) != fp(nof)
    p("  filter-off arm passed off as full dial @42: fingerprints %s vs %s -> %s"
      % (fp(full), fp(nof), "CAUGHT" if caught_filt else "MISSED"))
    c3 = caught_mode and caught_filt
    p("")

    # ---- CANARY 4: double-run byte-identity (dial + adaptive arms) ----
    p("-- CANARY 4: double-run byte-identity --")
    sig1 = dial_signature()
    sig2 = dial_signature()
    c4 = sig1 == sig2
    p("  dial+adaptive x 5 seeds run twice: %s" % ("PASS" if c4 else "FAIL"))
    p("")

    # ---- GRID: baselines (verbatim O4 arms) + dial arms ----
    p("-- GRID: baseline arms x seeds (O4 run_arm verbatim) --")
    ARMS = ("seq-raw", "int-raw", "seq-comp-fix", "int-comp-fix",
            "seq-comp-oracle", "int-comp-oracle", "adaptive")
    results = {arm: [run_arm(arm, s) for s in SEEDS] for arm in ARMS}
    p("  %-18s %6s %8s %7s  per-seed pm" % ("arm", "pm", "debt", "maxErr"))
    for arm in ARMS:
        rows = results[arm]
        p("  %-18s %5d permille %8d %7d  %s" % (arm, mean_pm(rows), mean_debt(rows),
            max_err(rows), [r["pm"] for r in rows]))
    p("")

    p("-- GRID: dial arms x seeds --")
    dial_arms = [
        ("dial", {}),
        ("dial-Lm1", dict(force_lag=9)),
        ("dial-Lp1", dict(force_lag=11)),
        ("dial-nofilter", dict(no_filter=True)),
        ("dial-g60", dict(glitch_mag=60)),
        ("dial-g20", dict(glitch_mag=20)),
        # POST-HOC AMENDMENT arms (run 1 numbers were seen first; labeled, not gate-eligible)
        ("dialv2", dict(beta_gated_filter=True, beta_latch=True)),
        ("dialv2-Lm1", dict(beta_gated_filter=True, beta_latch=True, force_lag=9)),
        ("dialv2-Lp1", dict(beta_gated_filter=True, beta_latch=True, force_lag=11)),
        ("dialv2-flap", dict(beta_gated_filter=True)),  # unlatched variant (thrash probe)
    ]
    dres = {}
    for name, kw in dial_arms:
        dres[name] = [run_dial(s, label=name, **kw) for s in SEEDS]
        rows = dres[name]
        p("  %-14s %5d permille %8d %7d  per-seed pm %s  segpm c/cf/bu %d/%d/%d  segdebt %d/%d/%d  supp %d rej %d sw %d"
          % (name, mean_pm(rows), mean_debt(rows), max_err(rows),
             [r["pm"] for r in rows],
             seg_pm_mean(rows, "calm"), seg_pm_mean(rows, "conflict"), seg_pm_mean(rows, "bursty"),
             seg_debt_mean(rows, "calm"), seg_debt_mean(rows, "conflict"), seg_debt_mean(rows, "bursty"),
             sum(r["suppressed"] for r in rows) // 5,
             sum(r["rejected"] for r in rows) // 5,
             sum(r["switches"] for r in rows) // 5))
    p("")

    # ---- DECISION RULE (pre-registered) ----
    p("-- DECISION RULE (pre-registered) --")
    statics = [a for a in ARMS if a != "adaptive"]
    best_static = max(statics, key=lambda a: mean_pm(results[a]))
    bs = results[best_static]
    dial = dres["dial"]
    dpm, ddebt = mean_pm(dial), mean_debt(dial)
    adpm, addebt = mean_pm(results["adaptive"]), mean_debt(results["adaptive"])
    gate_a = dpm >= adpm
    gate_b = ddebt <= 32770
    lm1, lp1 = dres["dial-Lm1"], dres["dial-Lp1"]
    c_plain = min(mean_pm(lm1), mean_pm(lp1)) >= dpm - 50
    c_bursty = min(seg_pm_mean(lm1, "bursty"), seg_pm_mean(lp1, "bursty")) \
        >= seg_pm_mean(dial, "bursty") - 50
    gate_c = c_plain and c_bursty
    p("  gate a: dial pm %d >= adaptive %d ? %s" % (dpm, adpm, "PASS" if gate_a else "FAIL"))
    p("  gate b: dial debt %d <= 32770 ? %s" % (ddebt, "PASS" if gate_b else "FAIL"))
    p("  gate c: L^-1/L^+1 pm %d/%d vs dial %d (-50 allowed); bursty %d/%d vs %d -> %s"
      % (mean_pm(lm1), mean_pm(lp1), dpm,
         seg_pm_mean(lm1, "bursty"), seg_pm_mean(lp1, "bursty"),
         seg_pm_mean(dial, "bursty"), "PASS" if gate_c else "FAIL"))
    p("  canaries: f14-unit %s, anchors %s, self-canary %s, byte-identity %s"
      % ("PASS" if (c1 and c1b) else "FAIL", "PASS" if c2 else "FAIL",
         "CAUGHT" if c3 else "MISSED", "PASS" if c4 else "FAIL"))
    verdict = ("PROMOTED" if (gate_a and gate_b and gate_c and c1 and c1b and c2 and c3 and c4)
               else "REFUTED" if not (gate_a or gate_b or gate_c)
               else "BOUNDARY BOOKED")
    p("  VERDICT: %s" % verdict)
    p("  best static: %s pm %d debt %d | adaptive %d/%d | dial %d/%d"
      % (best_static, mean_pm(bs), mean_debt(bs), adpm, addebt, dpm, ddebt))

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "q7-dial-output.txt"), "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
