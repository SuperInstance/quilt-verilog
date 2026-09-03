#!/usr/bin/env python3
"""SPIN 11, SPOKE: ADVERSARY — liar / free-rider / jammer / mute inside the
N=6 ladder fabric. Hypothesis: the fabric's invariants (debt/toll ledger
closure, delivery identity, mass conservation) DETECT and CONTAIN a
minority (1-of-6) adversary twin.

Sub-hypotheses:
  (a) LIAR (sign-flips its claimed channel reading): caught by
      delivery-identity mismatch (band + peer-distance detectors, both
      fabric-verifiable without ground truth); damage bounded to its own
      cohort share.
  (b) FREE-RIDER (emits, never pays toll): dynamics byte-identical to
      honest (it corrects honestly) but ledger closure breaks by exactly
      its unpaid tolls -> identifiable by amount and per-twin subledger.
  (c) JAMMER (constant max-amplitude emission every tick, tolls paid,
      claims honest): degradation no worse than the booked zero-lock /
      oscillation anchor (SPIN-5: zero@15 K=1 77.3%, 100% synchronized
      fires) — the adversary gets no leverage beyond incoherence.
      Operationally: drop vs its honest baseline bounded by the zero-lock
      drop scale, deadband-violation detector flags ~all its emissions.
  (d) MUTE (stops emitting entirely): byte-equivalent to removing the
      twin (5-live fabric replays exactly), residency drop modest and
      monotone with live-twin count, no cascade (no chatter/cancel/maxErr
      blowup).

Harness: run_adv() is a faithful clone of exp_glm1.run_fabric (E1
contract: fdiv decay, 64-bit LCG, FIFO oldest-first expiry, snapshot
decay) plus an `adv` hook. adv=None must be byte-identical to run_fabric
(canary C1). Integer-only inside every loop; floats ONLY in display
statistics at print time (established wheel precedent).

Config: N=6 ladder grammar at spread 15 (lats [0,3,6,9,12,15]), K in
{1,2}, stress params (delta=12, drift=6, pd=3), ticks 4800, seeds
{1,7,42,1999,20260902}, adversary = exactly twin index 5 (the lat-15
stale end), majority honest = 5.

Canaries (mandatory, before any number counts):
  C1 adv=none byte-matches exp_glm1.run_fabric full-dict.
  C2 SPIN-5 replay: zero@15 K=1 mean 77.3% (ev 8756, debt 187834);
     ladder@15 K=1 mean 71.5% (ev 5792, debt 106378); +-0.2pp,
     events/debt rounded-exact (published rounding respected).
"""
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "inventors-derby"))
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402

SEEDS = (1, 7, 42, 1999, 20260902)
DELTA = 12
N = 6
TICKS = 4800
PD = 3
DRIFT = 6
LATS = [0, 3, 6, 9, 12, 15]        # ladder, spread 15
ADV = 5                             # adversary twin index (lat 15)

# channel band invariant (fabric-verifiable contract constant: reality's
# own range over one period — no per-tick ground truth needed)
BAND = (min(reality(t) for t in range(240)), max(reality(t) for t in range(240)))
# peer transport bound: twins span `spread` ticks at max slope 8/5, plus
# trigger deadband slack on both ends. spread 15 -> 2*24 + 2*12 = 72.
SPREAD_SLOPE = 15 * 8 // 5
PEER_BOUND = 2 * SPREAD_SLOPE + 2 * DELTA


def median(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) // 2


def run_adv(lats, k, seed, adv=None, jam_amp=0, ticks=TICKS):
    """run_fabric clone + adversary hook. adv in {None,'liar','freerider',
    'jammer','mute'}. Returns run_fabric's dict plus adversary forensics
    under key 'adv' (None -> no extra key, byte-identity preserved)."""
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    n = len(lats)
    emissions = []
    events = mass = cancels = chatter = settles = 0
    last = -10
    resid = []
    cflags = []
    # adversary forensics
    paid = [0] * n                 # per-twin toll subledger
    unpaid = 0                     # tolls waived (freerider)
    bandviol = deadviol = peerviol = 0
    claims_log = []                # (t, i, claim) per tick for detectors
    local_in = [0] * n             # per-twin local residency ticks

    for t in range(ticks):
        raw = [reality(max(0, t - lats[i])) for i in range(n)]
        reads = list(raw)
        if adv == "liar" and ADV < n:
            reads[ADV] = -raw[ADV]          # sign-flipped claim
        s_true = reality(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT

        while pulses and pulses[-1][1] == 0:
            pulses.pop()

        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > DELTA]
        if adv == "mute":
            trig = [(i, e) for (i, e) in trig if i != ADV]

        cflag = 0
        if adv != "mute":
            for i, e in trig:
                if adv == "jammer" and i == ADV:
                    continue          # pure jammer: only constant emission
                if adv == "freerider" and i == ADV:
                    unpaid += abs(e)        # toll waived, emission happens
                else:
                    mass += abs(e)
                    paid[i] += abs(e)
                m = abs(e) // PD or 1
                pulses.appendleft([m if e > 0 else -m, k])
                events += 1
                emissions.append((t, i, m if e > 0 else -m, e))
                # delivery-identity detectors on this emission's claim
                claim = reads[i]
                peers = [reads[j] for j in range(n) if j != i]
                if not (BAND[0] <= claim <= BAND[1]):
                    bandviol += 1
                if abs(claim - median(peers)) > PEER_BOUND:
                    peerviol += 1
        elif adv == "mute":
            for i, e in trig:                 # honest twins emit normally
                mass += abs(e)
                paid[i] += abs(e)
                m = abs(e) // PD or 1
                pulses.appendleft([m if e > 0 else -m, k])
                events += 1
                emissions.append((t, i, m if e > 0 else -m, e))
        if adv == "jammer" and ADV < n:
            # constant max-amplitude emission EVERY tick, toll paid
            pulses.appendleft([jam_amp, k])
            events += 1
            mass += jam_amp
            paid[ADV] += jam_amp
            emissions.append((t, ADV, jam_amp, jam_amp))  # ledger basis
            if abs(errs[ADV]) <= DELTA:
                deadviol += 1              # fired inside deadband
            claim = reads[ADV]            # jammer's claim stays honest
            peers = [reads[j] for j in range(n) if j != ADV]
            if not (BAND[0] <= claim <= BAND[1]):
                bandviol += 1
            if abs(claim - median(peers)) > PEER_BOUND:
                peerviol += 1
        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and any(p[0] > 0 for p in pulses) \
                    and any(p[0] < 0 for p in pulses):
                cancels += 1
                cflag = 1
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
        if trig or (adv == "jammer"):
            if t - last == 1:
                chatter += 1
            last = t

        resid.append(abs(s_true - g))
        cflags.append(cflag)
        live = [i for i in range(n) if not (adv == "mute" and i == ADV)]
        for i in live:
            if abs(reads[i] - g) <= DELTA:
                local_in[i] += 1
        if all(abs(reads[i] - g) <= DELTA for i in live):
            settles += 1

    d = dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
             settles=settles, resid=resid, cflags=cflags,
             emissions=emissions, audit=None, ticks=ticks)
    if adv is not None:
        d["adv"] = dict(paid=paid, unpaid=unpaid, bandviol=bandviol,
                        peerviol=peerviol, deadviol=deadviol,
                        local_in=local_in, live=n - (1 if adv == "mute" else 0))
    return d


def honest_max_pulse():
    """Jam amplitude = max |emitted pulse| over the honest 5-seed baseline
    (fabric's own honest scale; K-independent by construction)."""
    return max(abs(pm) for s in SEEDS
               for (t, i, pm, e) in run_adv(LATS, 1, s)[ "emissions"])


def mean(v):
    return sum(v) / len(v)     # display only


def row(cells, w=10):
    return " | ".join(f"{c:>{w}}" for c in cells)


def stats(mode, k, jam_amp):
    rs = [run_adv(LATS, k, s, adv=(None if mode == "none" else mode),
                  jam_amp=jam_amp) for s in SEEDS]
    tp = [within_pm(r["resid"], DELTA) for r in rs]
    out = dict(tp=tp, mtp=mean(tp) / 10, ev=mean([r["events"] for r in rs]),
               debt=mean([r["mass"] for r in rs]),
               canc=mean([r["cancels"] for r in rs]),
               chat=mean([r["chatter"] for r in rs]),
               maxres=max(max(r["resid"]) for r in rs))
    if mode != "none":
        a = rs[0]["adv"]
        out["bandviol"] = mean([r["adv"]["bandviol"] for r in rs])
        out["peerviol"] = mean([r["adv"]["peerviol"] for r in rs])
        out["deadviol"] = mean([r["adv"]["deadviol"] for r in rs])
        out["unpaid"] = mean([r["adv"]["unpaid"] for r in rs])
        out["closure"] = mean([r["mass"] - sum(abs(e) for (t, i, pm, e)
                                               in r["emissions"])
                               for r in rs])
        live = a["live"]
        out["localpm"] = mean([1000 * sum(x for j, x in
                                           enumerate(r["adv"]["local_in"])
                                           if j != ADV)
                               // (r["ticks"] * (N - 1)) for r in rs])
    return out, rs


def rpe(tp_pm, ev):
    return tp_pm / 10 * 1000.0 / ev if ev else 0.0   # display


# ------------------------------------------------------------ canaries
def canaries():
    ok = True
    print("== CANARY C1: adv=none byte-matches exp_glm1.run_fabric ==")
    for lats in (LATS, [0] * 6):
        for k in (1, 2):
            for s in (SEEDS[0], SEEDS[-1]):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=s)
                b = run_adv(lats, k, s)
                same = (a == b)
                if not same:
                    ok = False
                    print(f"  MISMATCH lats={lats} K={k} seed={s}")
    print("  PASS: 8/8 configs full-dict byte-identical" if ok else "  FAIL")

    print("\n== CANARY C2: SPIN-5 published-anchor replay ==")
    checks = [("zero@15", [0] * 6, 1, 77.3, 8756, 187834),
              ("ladder@15 K=1", LATS, 1, 71.5, 5792, 106378)]
    for name, lats, k, want_tp, want_ev, want_debt in checks:
        rs = [run_adv(lats, k, s) for s in SEEDS]
        tp = mean([within_pm(r["resid"], DELTA) for r in rs])
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        good = (abs(tp / 10 - want_tp) <= 0.2
                and round(ev) == want_ev and round(dbt) == want_debt)
        ok &= good
        print(f"  {name}: got {tp/10:.1f}% (want {want_tp}) "
              f"ev {ev:.0f} (want {want_ev}) debt {dbt:.0f} (want "
              f"{want_debt})  -> {'PASS' if good else 'FAIL'}")
    print("\nALL CANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ------------------------------------------------------------ experiments
def exp_adversaries(jam_amp):
    print(f"\njam amplitude (max honest |pulse| over 5-seed baseline) = {jam_amp}")
    print("\n== EXP 1: adversary sweep, ladder@15, K in {1,2}, per-seed "
          "permille ==")
    hdr = ["mode", "K", "s1", "s7", "s42", "s1999", "s2s60902", "mean%",
           "evMean", "debtMean", "canc", "chat", "maxRes", "rpe"]
    print(row(hdr))
    table = {}
    for mode in ("none", "liar", "freerider", "jammer", "mute"):
        for k in (1, 2):
            st, rs = stats(mode, k, jam_amp)
            table[(mode, k)] = st
            print(row([mode, k] + st["tp"] +
                      [f"{st['mtp']:.1f}", f"{st['ev']:.0f}",
                       f"{st['debt']:.0f}", f"{st['canc']:.0f}",
                       f"{st['chat']:.0f}", st["maxres"],
                       f"{rpe(st['tp'][0] if False else mean(st['tp']), st['ev']):.2f}"]))
    return table


def exp_detectors(jam_amp):
    print("\n== EXP 2: invariant detectors + containment forensics "
          "(5-seed means) ==")
    print(row(["mode", "K", "bandViol", "peerViol", "deadViol",
               "unpaidToll", "closureDelta", "advTollShare", "honestLocal%"]))
    for mode in ("liar", "freerider", "jammer", "mute"):
        for k in (1, 2):
            st, rs = stats(mode, k, jam_amp)
            a = rs[0]["adv"]
            tot_paid = mean([sum(r["adv"]["paid"]) for r in rs])
            adv_paid = mean([r["adv"]["paid"][ADV] for r in rs])
            share = 1000 * adv_paid // max(1, int(tot_paid + st["unpaid"]))
            print(row([mode, k, f"{st['bandviol']:.0f}", f"{st['peerviol']:.0f}",
                       f"{st['deadviol']:.0f}", f"{st['unpaid']:.0f}",
                       f"{st['closure']:.0f}", f"{share/10:.1f}%",
                       f"{st['localpm']/10:.1f}"]))
    # ledger closure identity check: honest + each mode
    print("\n  ledger-closure identity (mass - sum|e| over emissions):")
    for mode in ("none", "liar", "freerider", "jammer", "mute"):
        for k in (1, 2):
            st, rs = stats(mode, k, jam_amp)
            if mode == "none":
                cl = mean([r["mass"] - sum(abs(e) for (_, _, _, e)
                                           in r["emissions"]) for r in rs])
                print(f"    {mode:<10} K={k}: closure delta = {cl:.1f}")
            else:
                print(f"    {mode:<10} K={k}: closure delta = "
                      f"{st['closure']:.0f}  unpaid = {st['unpaid']:.0f}  "
                      f"match={abs(st['closure'] + st['unpaid']) < 1}")


def exp_mute_linearity():
    print("\n== EXP 3: mute == twin removal (byte-identity) + live-count "
          "ladder ==")
    ok = True
    for k in (1, 2):
        for s in SEEDS:
            m = run_adv(LATS, k, s, adv="mute")
            h5 = run_fabric("interference", TICKS, [0, 3, 6, 9, 12], K=k,
                            pd=PD, delta=DELTA, drift=DRIFT, seed=s)
            msub = {kk: m[kk] for kk in h5}
            if msub != h5:
                ok = False
                print(f"  MISMATCH K={k} seed={s}")
    print("  PASS: mute(6-lats) byte-identical to honest 5-twin fabric, "
          "K{1,2} x 5 seeds" if ok else "  FAIL")
    print(row(["liveN", "lats", "mean%", "evMean", "debtMean", "maxRes"]))
    for live, lats in ((6, [0, 3, 6, 9, 12, 15]), (5, [0, 3, 6, 9, 12]),
                       (4, [0, 3, 6, 9]), (3, [0, 3, 6]), (2, [0, 3])):
        rs = [run_fabric("interference", TICKS, lats, K=1, pd=PD,
                         delta=DELTA, drift=DRIFT, seed=s) for s in SEEDS]
        tp = mean([within_pm(r["resid"], DELTA) for r in rs])
        print(row([live, str(lats), f"{tp/10:.1f}",
                   f"{mean([r['events'] for r in rs]):.0f}",
                   f"{mean([r['mass'] for r in rs]):.0f}",
                   max(max(r["resid"]) for r in rs)]))
    print("  (cascade check: mute row vs honest-6 row — chatter/cancels/"
          "maxRes in EXP 1 tables)")


def exp_liar_locality(jam_amp):
    print("\n== EXP 4: liar containment — honest-cohort local residency "
          "vs global truth ==")
    print(row(["mode", "K", "globalTrue%", "honestLocal% (5 twins)",
               "drop vs none (global)", "drop vs none (local)"]))
    base = {}
    for k in (1, 2):
        # freerider dynamics are byte-identical to honest (EXP 1) and carry
        # the per-twin local-residency forensics; use it as the honest base.
        base[k] = stats("freerider", k, jam_amp)[0]
    for mode in ("liar", "jammer"):
        for k in (1, 2):
            st, _ = stats(mode, k, jam_amp)
            st0 = base[k]
            print(row([mode, k, f"{st['mtp']:.1f}", f"{st['localpm']/10:.1f}",
                       f"{st['mtp']-st0['mtp']:+.1f}pp",
                       f"{st['localpm']/10-st0['localpm']/10:+.1f}pp"]))


if __name__ == "__main__":
    ok = canaries()
    if not ok:
        print("ABORT: canaries failed — no results collected.")
        sys.exit(1)
    A = honest_max_pulse()
    exp_adversaries(A)
    exp_detectors(A)
    exp_mute_linearity()
    exp_liar_locality(A)
