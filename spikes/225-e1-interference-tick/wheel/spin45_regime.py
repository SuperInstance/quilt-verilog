#!/usr/bin/env python3
"""SPIN-45 — REGIME spoke 6: EDGE-SPACING RESONANCE (SPIN-33 next-spoke).

CONTEXT (SPIN-33 verdict MIXED): at pinned J=153 the amplitude axis rides
edge DENSITY E (TWmean) or the E*J product (matched-mean), and the PHASE
swing INVERTS with density: E1s1 (inter-edge gap g=240) swings 16.3pp
across offsets while E6s6 (g=40) collapses to 1.5pp — pure per-edge
damage accumulation falsified by phase; dense edges renormalize to a
quasi-static gradient. SPIN-28's sawtooth phase sensitivity (24.4pp) is
an E=1 phenomenon. OPEN: is the phase swing (and the amplitude flip)
governed by the COMMENSURABILITY of the inter-edge gap g with the
scheduler period P?

DESIGN: fixed J=153, fixed slope s=6 (feasible at every gap:
(g-1)*6 >= 153 for all g >= 40). Gap axis g = 240/E in
{40, 48, 60, 80, 120, 240} (E = 6, 5, 4, 3, 2, 1) x scheduler period
P in {8, 12, 16, 24, 32, 48}; K=2, duty-50 square spreads 5<->30
(phase) and 10<->25 / 5<->30 (amplitude), N=6 ladder@0 base, seeds
{1,7,42} for panels. 36 resonance-map cells. J==153 and edge-count==E
asserted empirically at every g. Phase offsets 0..P//2 (spin-18
convention, SPIN-33 used 0..8 at P=16 = P//2).

PRE-REGISTERED RULE (verbatim from SPIN-33-regime.md 'Next-spoke
proposal', written BEFORE this spin; restated here BEFORE any panel
run — no H-rule below was edited after any panel execution):
  "swing(t) monotonically decreasing in min distance
   |g/P - round(g/P)| modulo both; falsified if swing is flat across
   the resonance map."
OPERATIONALIZATION (fixed in this header before the run):
  swing(g,P) = max - min of mean osc% over offsets 0..P//2
  (P=16 replay convention), seeds {1,7,42}, spread 5<->30 K=2.
  d(g,P) = |g/P - round(g/P)| (exact rational, floated at print).
  Spearman(swing, d) over the 36 cells.
    VALIDATED   iff Spearman <= -0.70 AND map swing range >= 5.0pp
    FALSIFIED   iff range <= 3.0pp (flat) OR Spearman >= +0.70
                (monotone INCREASING in d, i.e. resonance inverted)
    otherwise   MIXED
  Binned-by-d mean swing reported (advisory monotonicity check).
  Amplitude flip dAmp = tax_s25 - tax_s15 (both baselines, SPIN-17
  scar: TWmean + matched-mean mandatory) per cell is ADVISORY-only
  context for the same commensurability axis; the verdict rule above
  is swing-only, per SPIN-33's filed proposal.

STRUCTURAL PRE-CHECK (SPIN-44 scar class, before sweeping): no pd
sweep here; the standing constraint N <= 2*pd+1 holds (6 <= 2*3+1=7).
Traces are bounded in [400,553] (no supra-wall divergence expected);
a hard divergence gate (max resid < 10**6) is asserted on EVERY run —
any divergence aborts for a labeled post-hoc exclusion decision
(SPIN-16/44 scar class), never a silent number.

INSTRUMENT PROVENANCE: dynamics VERBATIM spin-28/33 dyn_run (imported
from spin33_regime, which imports spin28_regime); dyn45 below is that
same loop with READ-ONLY integer ledger counters added (no RNG or
state change). SPIN-15 LEDGER CLOSURE ASSERT LIVE ON EVERY ARM:
  g-balance:   g == g0 + drift_total + net_total   (assert)
  mass-balance: emitted == decay_loss + expired + inflight (assert)
  quantization draws n_draws == 0 always (this harness measures
  nothing: gate=never == mc=0 by construction, asserted).
Byte-identity canary proves dyn45 resid == sp33.dyn_run resid.

CANARIES (mandatory gate, ALL PASS before any panel read):
  a. dyn45 byte-identity vs sp33.dyn_run (R0 statics + sched + edge
     traces, K in {1,2}, seeds {1,42}) — resid lists identical.
  b. run_fabric 5-seed anchors: zero K=1 77.3/8756/187834;
     ladder15 K=1 71.5/5792/106378.
  c. SPIN-33 swing replays via dyn45: E1s1 swing 16.3pp, E6s6 swing
     1.5pp (tol 0.2 each), offsets 0..8 at P=16.
  d. gate=never == mc=0: n_draws == 0 and created == deleted == 0 on
     6 arms; SPIN-15 ledger assert live (every run, not just canary).
  e. double-run determinism (resid + ledger) on 2 cells.

Integer-only inside loops; floats only at print/stat time. Seeds
1/7/42 panels, 1/7/42/1999/20260902 canary anchors. Real runs —
environment failure => INCONCLUSIVE. One lane, no sub-lanes.
python3 -u direct redirect, no pipes. Unique spoke-suffixed output
spin45-regime-output.txt (SPIN-30 collision scar). NOT committed.
"""
import os
import sys
import time
from collections import deque
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
import exp_glm1
from exp_glm1 import run_fabric
import spin28_regime as sp28
import spin33_regime as sp33              # harness provenance source
from spin28_regime import (LCG, pct, mean, ladder,  # noqa: E402
                           square_schedule23, square_schedule18,
                           sched_fn, static_fn)

SEEDS = (1, 7, 42)
SEEDS5 = (1, 7, 42, 1999, 20260902)
DELTA, DRIFT, PD, N, TICKS = 12, 6, 3, 6, 4800
T0 = time.time()
R0 = exp_glm1.reality
JPIN, SLOPE, PER = 153, 6, 240

GAPS = (40, 48, 60, 80, 120, 240)          # g = 240/E
PERs = (8, 12, 16, 24, 32, 48)
SPR, HPR = 5, 30                           # phase-arm spread 5<->30
DIV_GATE = 10 ** 6


def dyn45(lats_fn, reality_fn, ticks=TICKS, k=4, pd=PD, delta=DELTA,
          drift=DRIFT, seed=20260902):
    """spin-28 dyn_run VERBATIM + read-only SPIN-15 integer ledger.

    Dynamics identical (byte-identity canaried vs sp33.dyn_run).
    """
    rng = LCG(seed)
    g = reality_fn(0)
    pulses = deque()
    resid = []
    g0 = g
    drift_total = net_total = 0
    emitted = decay_loss = expired = 0
    for t in range(ticks):
        lats = lats_fn(t)
        reads = [reality_fn(max(0, t - lats[i])) for i in range(N)]
        s_true = reality_fn(t)
        d = rng.below(2 * drift + 1) - drift
        g += d
        drift_total += d
        while pulses and pulses[-1][1] == 0:
            expired += pulses[-1][0]
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > delta]
        for i, e in trig:
            m = abs(e) // pd or 1
            pulses.appendleft([m if e > 0 else -m, k])
            emitted += m if e > 0 else -m
        if pulses:
            net = sum(p[0] for p in pulses)
            g += net
            net_total += net
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    nm = mag - (mag // 2) if abs(mag) > 1 else mag
                    decay_loss += mag - nm
                    decayed.append([nm, life - 1])
            pulses = decayed
        resid.append(abs(s_true - g))
    inflight = sum(p[0] for p in pulses)
    # --- SPIN-15 ledger closure (integer-exact, LIVE on every run) ---
    assert g == g0 + drift_total + net_total, "g BALANCE OPEN"
    assert emitted == decay_loss + expired + inflight, "MASS LEDGER OPEN"
    assert max(resid) < DIV_GATE, "DIVERGENCE GATE tripped (SPIN-16/44)"
    return {"resid": resid,
            "ledger": dict(drift_total=drift_total, net_total=net_total,
                           emitted=emitted, decay_loss=decay_loss,
                           expired=expired, inflight=inflight,
                           n_draws=0, created=0, deleted=0)}


_pct_cache = {}   # keys MUST carry trace label (spin-23 scar)


def osc(sched, fn, k, sd, tag=""):
    key = ("sched", hash(tuple(sched)), tag, k, sd)
    if key not in _pct_cache:
        _pct_cache[key] = pct(dyn45(sched_fn(sched), fn, k=k,
                                    seed=sd)["resid"])
    return _pct_cache[key]


def spct(s, fn, k, sd, tag=""):
    key = ("static", s, tag, k, sd)
    if key not in _pct_cache:
        _pct_cache[key] = pct(dyn45(static_fn(s), fn, k=k,
                                    seed=sd)["resid"])
    return _pct_cache[key]


def gap_trace(g):
    """Integer trace, band [400,553], edges of J=153 every g ticks."""
    def f(t):
        return 400 + min(JPIN, (t % g) * SLOPE)
    return f


def _mk(fn):
    return sp33._mk(fn)


def swing_cell(g, P):
    """max-min mean osc% over offsets 0..P//2, seeds {1,7,42}."""
    f = _mk(gap_trace(g))
    tag = f"g{g}P{P}o"
    row = []
    for off in range(P // 2 + 1):
        sched = square_schedule18(P, SPR, HPR, 50, offset=off)
        row.append(mean([osc(sched, f, 2, sd, tag) for sd in SEEDS]))
    return row, max(row) - min(row)


def amp_cell(g, P):
    """SPIN-33 amplitude metric at this cell's own P (advisory)."""
    f = _mk(gap_trace(g))
    tag = f"g{g}P{P}a"
    s15 = square_schedule23(P, 10, 25, 50)
    s25 = square_schedule23(P, SPR, HPR, 50)
    o15 = mean([osc(s15, f, 2, sd, tag) for sd in SEEDS])
    o25 = mean([osc(s25, f, 2, sd, tag) for sd in SEEDS])
    tw15 = mean([mean([spct(10, f, 2, sd, tag), spct(25, f, 2, sd, tag)])
                 for sd in SEEDS])
    tw25 = mean([mean([spct(SPR, f, 2, sd, tag), spct(HPR, f, 2, sd, tag)])
                 for sd in SEEDS])
    mm = mean([spct(18, f, 2, sd, tag) for sd in SEEDS])
    return (tw15 - o15, tw25 - o25, mm - o15, mm - o25)


def dist(g, P):
    """|g/P - round(g/P)| as exact rational (floated at print)."""
    r = Fraction(g, P)
    return abs(r - round(r))


def spearman(pairs):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for z in range(i, j + 1):
                rk[order[z]] = avg
            i = j + 1
        return rk
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    rx, ry = ranks(xs), ranks(ys)
    mx, my = mean(rx), mean(ry)
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(len(pairs)))
    den = (sum((r - mx) ** 2 for r in rx)
           * sum((r - my) ** 2 for r in ry)) ** 0.5
    return num / den if den else 0.0


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY a: dyn45 byte-identity vs sp33.dyn_run "
          "(spin-28 loop verbatim + read-only ledger) ==")
    a_ok = True
    nchk = 0
    traces = (("R0", R0),
              ("gap40", gap_trace(40)), ("gap240", gap_trace(240)),
              ("E1s1", sp33.edge_trace(1, 1)))
    for name, fn in traces:
        f = _mk(fn)
        for sp, ln in ((0, "lad0"), (15, "lad15")):
            for k in (1, 2):
                for sd in (1, 42):
                    a = dyn45(static_fn(sp), f, k=k, seed=sd)["resid"]
                    b = sp33.dyn_run(static_fn(sp), f, k=k, seed=sd)
                    nchk += 1
                    if a != b:
                        a_ok = False
                        print(f"  MISMATCH {name}/{ln} K={k} sd={sd}")
    sched = square_schedule23(16, 10, 25, 50)
    for sd in (1, 42):
        f = _mk(gap_trace(60))
        a = dyn45(sched_fn(sched), f, k=2, seed=sd)["resid"]
        b = sp33.dyn_run(sched_fn(sched), f, k=2, seed=sd)
        nchk += 1
        if a != b:
            a_ok = False
            print(f"  MISMATCH sched60 sd={sd}")
    ok &= a_ok
    print(f"  {'PASS' if a_ok else 'FAIL'}: {nchk} configs byte-identical"
          f" (ledger assert live in dyn45, absent in sp33.dyn_run)")

    print("\n== CANARY b: run_fabric anchors (5-seed means) ==")
    b_ok = True
    for name, lats, wp, wev, wm in (("ladder15", ladder(15), 71.5,
                                     5792, 106378),
                                    ("zero", [0] * N, 77.3, 8756, 187834)):
        te = tm = 0
        rs = []
        for sd in SEEDS5:
            r = run_fabric("interference", TICKS, lats, K=1, pd=PD,
                           delta=DELTA, drift=DRIFT, seed=sd)
            te += r["events"]
            tm += r["mass"]
            rs.append(pct(r["resid"]))
        p, ev, m = mean(rs), te / 5.0, tm / 5.0
        good = abs(p - wp) <= 0.05 and abs(m - wm) <= 0.5 \
            and abs(ev - wev) <= 0.5
        b_ok &= good
        print(f"  {name:<9} K=1: pct={p:.2f} ({wp})  ev={ev:.1f}"
              f" ({wev})  debt={m:.1f} ({wm})  -> "
              f"{'PASS' if good else 'FAIL'}")
    ok &= b_ok

    print("\n== CANARY c: SPIN-33 swing replays (P=16, offsets 0..8) ==")
    c_ok = True
    for E, s, want in ((1, 1, 16.3), (6, 6, 1.5)):
        f = _mk(sp33.edge_trace(E, s))
        tag = f"replayE{E}s{s}"
        row = []
        for off in range(9):
            sched = square_schedule18(16, SPR, HPR, 50, offset=off)
            row.append(mean([osc(sched, f, 2, sd, tag) for sd in SEEDS]))
        sw = max(row) - min(row)
        good = abs(sw - want) <= 0.2
        c_ok &= good
        print(f"  E{E}s{s} swing = {sw:.1f}pp (want {want}) -> "
              f"{'PASS' if good else 'FAIL'}")
    ok &= c_ok

    print("\n== CANARY d: gate=never == mc=0 + trace-shape assertions ==")
    d_ok = True
    for g in GAPS:
        f0 = gap_trace(g)
        if sp33.empirical_J(f0, g) != JPIN:      # empirical J over period
            d_ok = False
            print(f"  BAD J at g={g}")
        if sp33.empirical_E(f0, PER, 12) != PER // g:
            d_ok = False
            print(f"  BAD edge count at g={g}")
        led = dyn45(static_fn(0), _mk(f0), k=2, seed=7)["ledger"]
        if led["n_draws"] or led["created"] or led["deleted"]:
            d_ok = False
            print(f"  TOUCHED ledger at g={g} under never")
    ok &= d_ok
    print(f"  {'PASS' if d_ok else 'FAIL'}: J==153 + edge-count==240/g at"
          f" all 6 gaps; n_draws=created=deleted=0; SPIN-15 asserts live")

    print("\n== CANARY e: double-run determinism ==")
    e_ok = True
    f = _mk(gap_trace(80))
    for sched in (square_schedule18(24, SPR, HPR, 50, offset=5),
                  square_schedule23(16, 10, 25, 50)):
        a = dyn45(sched_fn(sched), f, k=2, seed=42)
        b = dyn45(sched_fn(sched), f, k=2, seed=42)
        if a["resid"] != b["resid"] or a["ledger"] != b["ledger"]:
            e_ok = False
            print("  NONDETERMINISTIC")
    ok &= e_ok
    print(f"  {'PASS' if e_ok else 'FAIL'}: 2 dual runs byte-identical"
          f" (resid + ledger)")
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- panels
def panel_swing():
    print("\n== PANEL 1: RESONANCE MAP — swing(g,P), offsets 0..P//2,"
          " spread 5<->30, K=2, seeds {1,7,42} ==")
    print(f"{'g':>4}{'E':>3} | " + "".join(f"P={P:<12}" for P in PERs))
    R = {}
    for g in GAPS:
        cells = []
        for P in PERs:
            row, sw = swing_cell(g, P)
            R[(g, P)] = (row, sw, dist(g, P))
            cells.append(sw)
        print(f"{g:>4}{PER // g:>3} | "
              + "".join(f"{c:>6.1f}        " for c in cells))
    print("swing (pp) per cell; d=|g/P-round(g/P)| map:")
    print(f"{'g':>4} | " + "".join(f"P={P:<12}" for P in PERs))
    for g in GAPS:
        print(f"{g:>4} | " + "".join(
            f"{float(R[(g, P)][2]):>6.3f}        " for P in PERs))
    return R


def panel_amp():
    print("\n== PANEL 2 (advisory): amplitude flip dAmp = tax25 - tax15"
          " per cell, both baselines, seeds {1,7,42} ==")
    print(f"{'g':>4}{'P':>4}{'dAmpTW':>8}{'dAmpMM':>8}")
    A = {}
    for g in GAPS:
        for P in PERs:
            tw15, tw25, mm15, mm25 = amp_cell(g, P)
            A[(g, P)] = (tw25 - tw15, mm25 - mm15)
            print(f"{g:>4}{P:>4}{tw25 - tw15:>8.1f}{mm25 - mm15:>8.1f}")
        sys.stdout.flush()
    return A


def verdict(R):
    print("\n== PRE-REGISTERED VERDICT (rule fixed in header BEFORE run) ==")
    pairs = [(float(R[k][2]), R[k][1]) for k in R]
    sp = spearman(pairs)
    rng = max(p[1] for p in pairs) - min(p[1] for p in pairs)
    print(f"  Spearman(swing, d) over 36 cells = {sp:+.3f}"
          f"  (VALIDATED needs <= -0.70)")
    print(f"  swing range across map = {rng:.1f}pp"
          f"  (flat-falsify gate <= 3.0pp; range gate >= 5.0pp)")
    bins = {}
    for d, s in pairs:
        bins.setdefault(round(d, 4), []).append(s)
    print("  binned mean swing by d:")
    for d in sorted(bins):
        print(f"    d={d:<6} n={len(bins[d]):>2}  mean swing "
              f"{mean(bins[d]):6.1f}pp  [{min(bins[d]):.1f},"
              f"{max(bins[d]):.1f}]")
    if rng <= 3.0:
        v = "FALSIFIED (swing flat across the resonance map)"
    elif sp >= 0.70:
        v = "FALSIFIED (swing monotone INCREASING in d — inverted)"
    elif sp <= -0.70 and rng >= 5.0:
        v = "VALIDATED (swing monotonically decreasing in " \
            "|g/P - round(g/P)|)"
    else:
        v = "MIXED"
    print(f"-> VERDICT: {v}")
    return v, sp, rng


def main():
    print("SPIN-45 REGIME EDGE-SPACING RESONANCE —",
          time.strftime("%Y-%m-%d %H:%M:%S"), "pid", os.getpid())
    print(f"config: J={JPIN} pinned, slope s={SLOPE} pinned, N={N},"
          f" seeds={SEEDS}, ticks={TICKS}, K=2, gaps={GAPS},"
          f" periods={PERs}")
    if not canaries():
        sys.exit(1)
    R = panel_swing()
    A = panel_amp()
    v, sp, rng = verdict(R)
    print(f"\nDONE. verdict {v}; Spearman {sp:+.3f}; range {rng:.1f}pp;"
          f" elapsed {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
