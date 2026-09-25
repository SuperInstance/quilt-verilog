#!/usr/bin/env python3
# Q7b (DEV ROUND 16): round-14 3-register regime dial ported onto the O2
# contention N-sweep fabric (N in {2..8}, calm/stress, raw vs lag-compensated)
# with the F14 mag/C=1 sort gate LIVE at every N.
# Pre-registered spec + decision rule: ROUND-16-Q7b-dial-o2nsweep.md PART 1
# (committed before any comparison numbers were generated).
# Integer-only loop core; percentages computed once at print time.
# Run: python3 dev-rounds/q7b_dial_o2nsweep.py
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inventors-derby"))
from collections import deque
from e1 import LCG, reality
from o2_contention import (SEEDS, TICKS, REGIMES, KEY, discover_lag,
                           run_sw, run_sw_comp)
from o4_regime_motion import Detector, WINDOW

# ---- dial constants (q7_regime_dial.py v1 spec, verbatim) ----
JUMP_THRESH = 40          # single-tick reading jump => transient hit
TRANS_WIN = 16
TRANS_ARM = 2             # hits in window needed to set beta
SIGMA_LAG_FAST = 8        # R1 fast bit: max discovered lag >= 8

LATS_N = {
    2: (0, 12),
    3: (0, 6, 12),
    4: (0, 4, 8, 12),      # NEW pre-registered interpolation
    5: (0, 3, 6, 9, 12),
    6: (0, 2, 5, 7, 10, 12),
    7: (0, 2, 4, 6, 8, 10, 12),
    8: (0, 2, 3, 5, 7, 8, 10, 12),
}

# round-2/O2 + round-3/O2b published anchors (unmodified arms, mean over 5 seeds)
ANCHORS = {  # (regime, N, arm, kind) -> pct_x10
    ("stress", 8, "raw", "all"): 578, ("stress", 8, "raw", "c1"): 697,
    ("stress", 8, "comp", "all"): 427, ("stress", 8, "comp", "c1"): 989,
    ("stress", 6, "raw", "all"): 652, ("stress", 6, "raw", "c1"): 697,  # +4.5pp wall
    ("stress", 7, "raw", "all"): 629, ("stress", 7, "raw", "c1"): 697,  # +6.8pp
    ("stress", 2, "raw", "all"): 698, ("stress", 2, "raw", "c1"): 698,
    ("stress", 3, "raw", "all"): 697, ("stress", 3, "raw", "c1"): 698,
    ("stress", 5, "raw", "all"): 680, ("stress", 5, "raw", "c1"): 696,
    ("stress", 5, "comp", "all"): 748, ("stress", 5, "comp", "c1"): 989,
    ("calm", 8, "raw", "all"): 18, ("calm", 8, "raw", "c1"): 41,
    ("calm", 8, "comp", "all"): 317, ("calm", 8, "comp", "c1"): 843,
}


def run_dial_sw(seed, lats, params, laghat=None, sort=True, supp=True,
                sigma_params=True, invert=False, label="dial"):
    """O2 switchboard loop + the round-14 dial.
    laghat=None -> raw arm (no compensation; blade still runs for R1/sigma).
    supp=False or sigma_params=False -> attribution arm 'sort+supp' variants.
    invert=True -> sigma inverted (self-canary mislabel probe)."""
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
    det = Detector()
    sigma_fast = 1 if max(lats) >= SIGMA_LAG_FAST else 0   # R1 fast bit (blade is exact)
    trans_w = [0] * TRANS_WIN
    twidx = 0
    prev_reads = [0] * n
    stress_ticks = beta_ticks = suppressed = 0
    for t in range(TICKS):
        if laghat is None:
            reads = [reality(max(0, t - lats[i])) for i in range(n)]
        else:
            reads = [reality(max(0, t - lats[i] + laghat[i])) for i in range(n)]
        g += rng.below(2 * params["drift"] + 1) - params["drift"]
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        # --- R3 sensor + suppressor (v1: always active when supp) ---
        hits = 0
        for i in range(n):
            if supp and t > 0 and abs(reads[i] - prev_reads[i]) >= JUMP_THRESH:
                hits += 1
        trans_w[twidx] = 1 if hits else 0
        twidx = (twidx + 1) % TRANS_WIN
        beta = 1 if sum(trans_w) >= TRANS_ARM else 0
        beta_ticks += beta
        # --- R2 sigma: fast (blade seat) OR slow (kappa confirm) ---
        sigma = sigma_fast | (1 if det.regime == 1 else 0)
        stress_now = sigma and not beta
        if invert:
            stress_now = (not sigma) and not beta
        if stress_now:
            stress_ticks += 1
            K = 1; pulse_div = 2; td = 12; phase_decay = 1
        else:
            K = params["K"]; pulse_div = params["pulse_div"]
            td = params["delta"]; phase_decay = 0
        if not sigma_params:
            K = params["K"]; pulse_div = params["pulse_div"]
            td = params["delta"]; phase_decay = 0
        # --- candidates, suppressor, sort ---
        cands = []
        for i in range(n):
            if supp and t > 0 and abs(reads[i] - prev_reads[i]) >= JUMP_THRESH:
                suppressed += 1
                prev_reads[i] = reads[i]
                continue
            prev_reads[i] = reads[i]
            e = reads[i] - g
            if abs(e) > td:
                cands.append(dict(id=i, err=e, err_abs=abs(e),
                                  last_fire=last_fire[i], cont=cont[i]))
                cont[i] += 1
        if sort and len(cands) > 1:
            best = max(cands, key=lambda c: c["err_abs"])
            rejected += len(cands) - 1
            cands = [best]
        trig = [c["err"] for c in cands]
        cancel_flag = 0
        max_trig = max((abs(e) for e in trig), default=0)
        tick_debt = 0
        for c in cands:
            e = c["err"]
            m = abs(e) // pulse_div or 1
            pulses.appendleft([m if e > 0 else -m, K])
            events += 1
            debt += abs(e)
            tick_debt += abs(e)
            last_fire[c["id"]] = t
            fires[c["id"]] += 1
        if pulses:
            net = sum(p[0] for p in pulses)
            cancel_flag = 1 if (net == 0 and len(pulses) >= 2) else 0
            cancellations += cancel_flag
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
            if trig and max(abs(s - g) for s in reads) > max_trig:
                constructive += 1
            if trig and t - last_snap == 1:
                chatter += 1
            if trig:
                last_snap = t
        det.tick(tick_debt, cancel_flag, 1 if trig else 0)
        err = max(abs(s - g) for s in reads)
        max_err = max(max_err, err)
        if all(abs(s - g) <= params["delta"] for s in reads):
            settles += 1
    return dict(arm=label, seed=seed, events=events, debt=debt, chatter=chatter,
                cancel=cancellations, maxerr=max_err,
                pct=round(100 * settles / TICKS, 1), fires=fires, rejected=rejected,
                stress_ticks=stress_ticks, beta_ticks=beta_ticks,
                suppressed=suppressed)


def cell(rows):
    n = len(rows)
    return (round(10 * sum(r["pct"] for r in rows) / n),
            round(sum(r["debt"] for r in rows) / n),
            round(sum(r["maxerr"] for r in rows) / n, 1))


def fingerprint(rows):
    return tuple((r["pct"], r["debt"], r["maxerr"], r["suppressed"],
                  r["stress_ticks"], r["beta_ticks"]) for r in rows)


def run_cell(lats, params, lag, dial_kw, label):
    return [run_dial_sw(s, lats, params, laghat=lag, label=label, **dial_kw)
            for s in SEEDS]


def main():
    out = []
    def p(s=""):
        print(s); out.append(s)

    p("== Q7b ROUND 16: regime dial on the O2 contention N-sweep (F14 mag/C=1 gate LIVE, N=2..8) ==")
    p("dial v1: R1=blade (exact per-twin) R2=sigma (lag>=8 OR kappa) R3=beta (>=2 jumps/16)")
    p("outputs: suppressor(jump>=40, always on) + mag/C=1 sort; stress_now -> K=1/pd=2/phase-decay/td=12")
    p("attribution arm sort+supp: registers logged, sigma outputs inert")

    print("== lag blade discovery (per-N, per-twin; comp arms) ==")
    laghat = {}
    for n, lats in LATS_N.items():
        hs = [discover_lag(L) for L in lats]
        laghat[n] = hs
        exact = all(h == L for h, L in zip(hs, lats))
        print(f"  N={n} lats={lats} -> discovered {hs} exact={exact}")
        p(f"  blade N={n}: exact={exact}")

    # ---- main grid ----
    # results[(regime, N, armname)] = (pct_x10, debt, maxe, rows)
    results = {}
    for reg, params in REGIMES.items():
        for n, lats in LATS_N.items():
            # unmodified arms (anchor carriers)
            results[(reg, n, "all-raw")] = cell(
                [run_sw(s, key=None, C=n, lats=lats, **params) for s in SEEDS])
            results[(reg, n, "c1-raw")] = cell(
                [run_sw_comp(s, key=KEY, C=1, lats=lats, laghat=None, **params) for s in SEEDS])
            results[(reg, n, "all-comp")] = cell(
                [run_sw_comp(s, key=None, C=n, lats=lats, laghat=laghat[n], **params) for s in SEEDS])
            results[(reg, n, "c1-comp")] = cell(
                [run_sw_comp(s, key=KEY, C=1, lats=lats, laghat=laghat[n], **params) for s in SEEDS])
            # dial arms
            results[(reg, n, "dial-raw")] = cell(
                run_cell(lats, params, None, {}, "dial"))
            results[(reg, n, "dial-comp")] = cell(
                run_cell(lats, params, laghat[n], {}, "dial"))
            results[(reg, n, "sortsupp-raw")] = cell(
                run_cell(lats, params, None, dict(sigma_params=False), "sort+supp"))
            results[(reg, n, "sortsupp-comp")] = cell(
                run_cell(lats, params, laghat[n], dict(sigma_params=False), "sort+supp"))

    # ---- CANARY 2: anchor replay (unmodified arms vs published) ----
    p("")
    p("-- CANARY 2: anchor replay (unmodified arms vs round-2/O2 + round-3/O2b) --")
    anchor_ok = True
    kind_map = {("all",): "all", ("c1",): "c1"}
    for (reg, n, arm, kind), want in sorted(ANCHORS.items()):
        a = "all" if kind == "all" else "c1"
        got = results[(reg, n, f"{a}-{arm}")][0]
        good = got == want
        anchor_ok &= good
        p("  %-6s N=%d %-4s %-4s got %d want %d  %s"
          % (reg, n, arm, kind, got, want, "OK" if good else "FAIL"))
    p("  ANCHOR REPLAY: %s" % ("PASS" if anchor_ok else "FAIL"))

    # ---- main table ----
    p("")
    p("== MAIN GRID (%w x10 / debt / maxE; 5 seeds, 4800 ticks) ==")
    p("%-7s %2s | %-13s | %-13s | %-13s | %-13s | %-13s"
      % ("regime", "N", "admit-all raw", "sortC1 raw", "DIAL raw",
         "admit-all comp", "sortC1 comp"))
    for reg in REGIMES:
        for n in LATS_N:
            def f(k):
                r = results[(reg, n, k)]
                return "%d/%d/%.1f" % (r[0], r[1], r[2])
            p("%-7s %2d | %-13s | %-13s | %-13s | %-13s | %-13s"
              % (reg, n, f("all-raw"), f("c1-raw"), f("dial-raw"),
                 f("all-comp"), f("c1-comp")))
    p("")
    p("== ATTRIBUTION (sort+supp: suppressor+sort, sigma outputs inert; %w x10 / debt / maxE) ==")
    p("%-7s %2s | %-13s | %-13s | %-13s" % ("regime", "N", "sortC1 raw",
                                             "sort+supp raw", "sort+supp comp"))
    for reg in REGIMES:
        for n in LATS_N:
            def g(k):
                r = results[(reg, n, k)]
                return "%d/%d/%.1f" % (r[0], r[1], r[2])
            p("%-7s %2d | %-13s | %-13s | %-13s"
              % (reg, n, g("c1-raw"), g("sortsupp-raw"), g("sortsupp-comp")))

    # ---- dial telemetry ----
    p("")
    p("== dial telemetry (mean over 5 seeds): stress_ticks / beta_ticks / suppressed ==")
    for reg in REGIMES:
        for n in LATS_N:
            rows = run_cell(LATS_N[n], REGIMES[reg], None, {}, "dial")
            p("  %-6s N=%d raw: stress %d/4800 beta %d/4800 suppressed %d"
              % (reg, n, sum(r["stress_ticks"] for r in rows) // 5,
                 sum(r["beta_ticks"] for r in rows) // 5,
                 sum(r["suppressed"] for r in rows) // 5))

    # ---- decision table ----
    p("")
    p("== DECISION TABLE: ADD(N) = [dial - admit-all] - [sort-alone - admit-all] (pp) ==")
    p("   wall gate: raw sort win >= +2pp (unmodified) first clears at N=6 (round 3)")
    promote_locs = []
    inert_ok = True
    for reg in REGIMES:
        for armraw, dname, sname in (("raw", "dial-raw", "c1-raw"),
                                     ("comp", "dial-comp", "c1-comp")):
            for n in LATS_N:
                aa = results[(reg, n, "all-" + armraw)][0]
                so = results[(reg, n, sname)][0]
                dl = results[(reg, n, dname)][0]
                add = (dl - aa) - (so - aa)
                debt_d = results[(reg, n, dname)][1]
                debt_s = results[(reg, n, sname)][1]
                def pp(v):
                    return "%+d.%d" % (v // 10 if v >= 0 else -((-v + 9) // 10), abs(v) % 10)
                p("  %-6s N=%d %-4s sortwin %s pp  dialwin %s pp  ADD %s pp"
                  "  debt dial %d vs sort %d (%s)"
                  % (reg, n, armraw, pp(so - aa), pp(dl - aa), pp(add),
                     debt_d, debt_s,
                     "ok" if debt_d <= 11 * debt_s // 10 else "BREACH>10%"))
                if abs(add) > 5:
                    inert_ok = False
                if armraw == "raw" and n >= 3 and add >= 20 and debt_d <= 11 * debt_s // 10:
                    promote_locs.append((reg, n, add, debt_d, debt_s))
    # wall location under dial (raw)
    p("")
    p("== WALL LOCATION (raw arm): first N where win >= +2.0pp ==")
    for label, keyw in (("sort-alone", "c1-raw"), ("dial", "dial-raw")):
        wall = None
        for n in sorted(LATS_N):
            for reg in ("stress", "calm"):
                w = results[(reg, n, keyw)][0] - results[(reg, n, "all-raw")][0]
                if w >= 20:
                    wall = (reg, n, w)
                    break
            if wall:
                break
        p("  %-11s -> %s" % (label, "no N clears" if not wall else
                            "%s N=%d (+%d.%dpp)" % (wall[0], wall[1], wall[2] // 10, wall[2] % 10)))

    # ---- CANARY 1: byte-identity (rerun full N=6 cell, hash) ----
    p("")
    p("-- CANARY 1: byte-identity (N=6 stress full cell, run twice, hashed) --")
    def n6cell():
        parts = []
        for k in ("all-raw", "c1-raw", "dial-raw", "all-comp", "c1-comp", "dial-comp"):
            r = results[("stress", 6, k)]
            parts.append("%s=%d/%d/%.1f" % (k, r[0], r[1], r[2]))
        return "; ".join(parts)
    h1 = hashlib.sha256(n6cell().encode()).hexdigest()
    # genuinely re-run the cell
    lats = LATS_N[6]; params = REGIMES["stress"]
    rerun = []
    rerun.append(cell([run_sw(s, key=None, C=6, lats=lats, **params) for s in SEEDS]))
    rerun.append(cell([run_sw_comp(s, key=KEY, C=1, lats=lats, laghat=None, **params) for s in SEEDS]))
    rerun.append(cell(run_cell(lats, params, None, {}, "dial")))
    rerun.append(cell([run_sw_comp(s, key=None, C=6, lats=lats, laghat=laghat[6], **params) for s in SEEDS]))
    rerun.append(cell([run_sw_comp(s, key=KEY, C=1, lats=lats, laghat=laghat[6], **params) for s in SEEDS]))
    rerun.append(cell(run_cell(lats, params, laghat[6], {}, "dial")))
    parts2 = []
    for k, r in zip(("all-raw", "c1-raw", "dial-raw", "all-comp", "c1-comp", "dial-comp"), rerun):
        parts2.append("%s=%d/%d/%.1f" % (k, r[0], r[1], r[2]))
    h2 = hashlib.sha256("; ".join(parts2).encode()).hexdigest()
    byte_ok = h1 == h2
    p("  run1 %s" % h1[:16])
    p("  run2 %s" % h2[:16])
    p("  BYTE-IDENTITY: %s" % ("PASS" if byte_ok else "FAIL"))

    # ---- CANARY 3: self-canary (mislabeled sigma-inverted arm) ----
    p("")
    p("-- CANARY 3: self-canary (sigma-inverted arm labeled 'dial') --")
    true_rows = run_cell(LATS_N[6], REGIMES["stress"], None, {}, "dial")
    mis_rows = run_cell(LATS_N[6], REGIMES["stress"], None,
                        dict(invert=True), "dial")
    caught = fingerprint(true_rows) != fingerprint(mis_rows)
    p("  true dial  fp[0] %s" % (fingerprint(true_rows)[0],))
    p("  mislabeled fp[0] %s" % (fingerprint(mis_rows)[0],))
    p("  MISLABEL: %s" % ("CAUGHT" if caught else "MISSED"))

    # ---- verdict ----
    p("")
    p("-- DECISION RULE (pre-registered) --")
    if promote_locs:
        verdict = "PROMOTED"
    elif inert_ok:
        verdict = "BOOKED: dial inert on contention"
    else:
        verdict = "LOCATED"
    p("  VERDICT: %s" % verdict)
    if promote_locs:
        for reg, n, add, dd, ds in promote_locs:
            p("  promote site: %s N=%d ADD=+%d.%dpp debt %d<=%d" % (reg, n, add // 10, add % 10, dd, ds))
    p("  canaries: anchors %s, byte-identity %s, self-canary %s"
      % ("PASS" if anchor_ok else "FAIL", "PASS" if byte_ok else "FAIL",
         "CAUGHT" if caught else "MISSED"))

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "q7b-dial-o2nsweep-output.txt"), "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
