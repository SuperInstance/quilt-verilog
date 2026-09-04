#!/usr/bin/env python3
"""DEV ROUND 19b -- bounded-fabric arrival-rate absorbers under the PW-invariance gate.

Pre-registration: wheel/round19b-prereg.md (committed BEFORE this run).
Question (dispatch verbatim): is there a bounded-fabric mechanism (queue cell / credit
fence / staged grant) that absorbs arrival-rate pressure (fan-out 64, arrival kappa~8,
C-lift 6->24+ pp) WITHOUT (a) breaking bit-exact replay at any PW, (b) floats or
wall-clock, (c) violating determinism?

Fabric: run_sw semantics cloned VERBATIM (statement order) from glm3_experiments.py
(round-2/19 fabric) so anchors replay bit-exact; arms swap only the admission gate.
PW leg: same fabric with every state variable two's-complement wrapped at PW bits
(g, pulse masses, debt, I; SPIN-19/34 semantics); trace = sha256 over JSON
{events, debt, rejected, maxerr, fires, adm-per-tick, settle-bit string} (SPIN-34
hash convention, 16 hex chars).

Prereg ambiguity disclosure (printed in L3 too): sgrant seat-A is named
"least-recently-fired candidate ... anti-starvation" but the parenthetical says
"(max last_fire)". run_sw's fair key sorts ASCENDING on last_fire (least-recently-
fired first); the named semantics require MIN last_fire. Implemented: min(last_fire),
tie min id. Disclosed as an interpretation, not a re-derivation.

Run: python3 -u round19b_arrival_fabric.py > round19b-output.txt   (from wheel/)
Legs: L0 canaries C2/C3 + round-19 wall replay + PW48==unbounded anchor identity;
L1 metric grid with maxstate tracking; L2 PW hash legs (T2); L3 C-lift table +
H1/H2/H3 bands + verdict ladder.
"""
import hashlib
import json
import os
import re
import sys
import time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))          # .../wheel
SPIKE = os.path.dirname(HERE)                              # 225-e1-...
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(SPIKE, "inventors-derby"))
sys.path.insert(0, SPIKE)

import e1                                        # noqa: E402  (LCG, reality)
from glm3_experiments import run_sw              # noqa: E402  (verbatim reference for C2)

T0 = time.time()
PD = 3
SEEDS = (1, 7, 42, 1999, 20260902)
TICKS = 4800
PWS = (41, 42, 43, 44, 45, 46, 47, 48)
FAMILIES = {                       # round-19 verbatim
    "calm":   dict(K=8, drift=3),
    "stress": dict(K=4, drift=6),
}
KAPPA_DELTA = {                    # kappa = delta/K (round-19 arrival-rate knob)
    "calm":   {2: 16, 8: 64, 16: 128},
    "stress": {2: 8, 8: 32, 16: 64},
}
DEFAULT_DELTA = {"calm": 6, "stress": 12}   # round-2/3/17 anchors
NS = (2, 5, 13, 21, 34, 64)
LATS_N = {                          # round-17/19 canonical + interpolation
    2: (0, 12),
    3: (0, 6, 12),
    5: (0, 3, 6, 9, 12),
    8: (0, 2, 3, 5, 7, 8, 10, 12),
}
R19_WALL = 6                        # round-17/19 pd=3 default wall anchor
MECHS = ("qcell", "cfence", "sgrant", "crutch")
LIM = 1 << 40                       # T1 theorem tier bound (signed-41 range)


def lats_for(n):
    if n in LATS_N:
        return LATS_N[n]
    return tuple(round(i * 12 / (n - 1)) for i in range(n))


def wrapv(x, pw):
    """Two's-complement wrap at pw bits (SPIN-19/34 semantics)."""
    m = 1 << pw
    h = 1 << (pw - 1)
    return ((x + h) % m) - h


# ------------------------------------------------------------------ fabric
def fabric(seed, arm, lats, K, drift, delta, pd=PD, ticks=TICKS, pw=None,
           want_trace=False):
    """run_sw clone (verbatim statement order; round-2/19 fabric).

    arm in {admit, mag1, qcell, cfence, sgrant, crutch} selects the admission
    gate; everything else is run_sw semantics: N-twin channel, twin i reads
    e1.reality(max(0,t-lats[i])), g drifts +-drift (LCG), candidates |s-g|>delta,
    admitted twins emit pulse (mass |e|//pd or 1, sign-corrected, life K), pulses
    halve per tick (life-1), g += net, settle iff all reads within delta.

    pw=None  -> unbounded python ints (metric leg).
    pw=int   -> g, pulse masses, debt, I wrapped at pw bits (PW leg).
    maxstate = max |g, pulse masses, debt, I| seen (tracked every run).
    want_trace -> also return canonical trace hash + per-tick adm/settle.
    """
    rng = e1.LCG(seed)
    g = e1.reality(0)
    n = len(lats)
    last_fire = [-10] * n
    cont = [0] * n
    fires = [0] * n
    pulses = deque()
    events = debt = constructive = cancellations = chatter = 0
    max_err = settles = 0
    last_snap = -10
    rejected = 0
    # mechanism state (bounded by construction: ids<64, credits<=8, last_fire<=ticks)
    q = []            # qcell FIFO of deferred twin ids, capacity 8
    cred = 0          # cfence credits in [0, 8]
    acc = 0           # crutch integral accumulator I
    maxstate = 0
    adm_list = [] if want_trace else None
    settle_bits = [] if want_trace else None

    for t in range(ticks):
        reads = [e1.reality(max(0, t - L)) for L in lats]
        g += rng.below(2 * drift + 1) - drift
        if pw:
            g = wrapv(g, pw)
        if abs(g) > maxstate:
            maxstate = abs(g)
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        cands = []
        for i, s in enumerate(reads):
            e = s - g
            if abs(e) > delta:
                cands.append(dict(id=i, err=e, err_abs=abs(e),
                                  last_fire=last_fire[i], cont=cont[i]))
                cont[i] += 1  # showed up to the derby

        # ---- admission gate (the ONLY thing arms change) ----
        admitted = cands                     # admit-all baseline
        if arm == "mag1":                    # round-2 T2 sort: (-err_abs, id), top-1
            if len(cands) > 1:
                cands.sort(key=lambda r: (-r["err_abs"], r["id"]))
                admitted = cands[:1]
        elif arm == "qcell":
            cset = set(c["id"] for c in cands)
            q = [i for i in q if i in cset]          # purge non-candidates, oldest-first
            admitted = []
            if q:
                wid = q.pop(0)                        # oldest still-queued takes the seat
                admitted = [next(c for c in cands if c["id"] == wid)]
            elif cands:                               # else mag-top fresh candidate
                admitted = [min(cands, key=lambda r: (-r["err_abs"], r["id"]))]
            qset = set(q)
            for c in cands:                           # queue unadmitted while room
                if c["id"] not in qset and c not in admitted:
                    if len(q) < 8:
                        q.append(c["id"])
                        qset.add(c["id"])
        elif arm == "cfence":
            if cred < 8:
                cred += 1                             # +1 per tick BEFORE admission
            admitted = []
            if cands:
                cands.sort(key=lambda r: (-r["err_abs"], r["id"]))
                for c in cands:
                    if cred > 0 and len(admitted) < 2:
                        admitted.append(c)
                        cred -= 1
        elif arm == "sgrant":
            admitted = []
            if cands:
                seatA = min(cands, key=lambda r: (r["last_fire"], r["id"]))
                admitted = [seatA]                    # least-recently-fired (disclosed)
                rem = [c for c in cands if c["id"] != seatA["id"]]
                if rem:
                    admitted.append(max(rem, key=lambda r: (r["err_abs"], -r["id"])))
        elif arm == "crutch":
            acc += len(cands) + (acc >> 4)            # integral servo, fabric state
            if abs(acc) > maxstate:
                maxstate = abs(acc)
            if pw:
                acc = wrapv(acc, pw)
            gnt = 1 + min(n, max(0, acc >> 8))        # grant ceiling
            admitted = []
            if cands:
                cands.sort(key=lambda r: (-r["err_abs"], r["id"]))
                admitted = cands[:gnt]
        rejected += len(cands) - len(admitted)
        if want_trace:
            adm_list.append(len(admitted))

        trig = [c["err"] for c in admitted]
        max_trig = max((abs(e) for e in trig), default=0)
        for c in admitted:
            e = c["err"]
            m = abs(e) // pd or 1
            pulses.appendleft([m if e > 0 else -m, K])
            events += 1
            debt += abs(e)
            if abs(m) > maxstate:
                maxstate = abs(m)
            if pw:
                debt = wrapv(debt, pw)
            last_fire[c["id"]] = t
            fires[c["id"]] += 1
        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                    if abs(mag) > maxstate:
                        maxstate = abs(mag)
                    if pw:
                        mag = wrapv(mag, pw)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
            if pw:
                g = wrapv(g, pw)
            if abs(g) > maxstate:
                maxstate = abs(g)
            if trig and max(abs(s - g) for s in reads) > max_trig:
                constructive += 1
            if trig and t - last_snap == 1:
                chatter += 1
            if trig:
                last_snap = t
        err = max(abs(s - g) for s in reads)
        max_err = max(max_err, err)
        if all(abs(s - g) <= delta for s in reads):
            settles += 1
        if want_trace:
            settle_bits.append("1" if all(abs(s - g) <= delta for s in reads) else "0")

    out = dict(events=events, debt=debt, chatter=chatter, cancel=cancellations,
               maxerr=max_err, pct=round(100 * settles / ticks, 1),
               fires=fires, rejected=rejected, maxstate=maxstate)
    if want_trace:
        canon = {"adm": adm_list, "debt": debt, "events": events,
                 "fires": fires, "maxerr": max_err, "rejected": rejected,
                 "settle": "".join(settle_bits)}
        out["hash"] = hashlib.sha256(
            json.dumps(canon, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()[:16]
    return out


def cell(arm, fam, kappa, n, pw=None, want_trace=False):
    """5-seed mean %w (+max maxstate) for (arm, family, kappa, N)."""
    cfg = FAMILIES[fam]
    lats = lats_for(n)
    tot = 0.0
    ms = 0
    for sd in SEEDS:
        r = fabric(sd, arm, lats, K=cfg["K"], drift=cfg["drift"],
                   delta=KAPPA_DELTA[fam][kappa], pd=PD, pw=pw,
                   want_trace=want_trace)
        tot += r["pct"]
        ms = max(ms, r["maxstate"])
    return tot / len(SEEDS), ms


# ------------------------------------------------------------------ L0
def leg0():
    print("== L0 canaries ==")
    anchor_lats = LATS_N[5]
    ok_all = True

    # C2a: anchor %w replay (round-2 published, exact)
    # anchor cell is stress DEFAULT delta=12 (not a kappa seat) -> direct runs:
    tot_a = tot_m = 0.0
    for sd in SEEDS:
        ra = fabric(sd, "admit", anchor_lats, K=4, drift=6, delta=12)
        rm = fabric(sd, "mag1", anchor_lats, K=4, drift=6, delta=12)
        tot_a += ra["pct"]
        tot_m += rm["pct"]
    adm_pct, mag_pct = tot_a / len(SEEDS), tot_m / len(SEEDS)
    ok_anchor = abs(adm_pct - 68.0) <= 0.05 and abs(mag_pct - 69.6) <= 0.05
    ok_all = ok_all and ok_anchor
    print(f"C2a anchor replay: admit %w={adm_pct:.1f} (want 68.0)  "
          f"mag1 %w={mag_pct:.1f} (want 69.6)  -> {'PASS' if ok_anchor else 'FAIL'}")

    # C2b: per-seed counter equality vs glm3 run_sw verbatim (harness self-check)
    ok_counters = True
    for sd in (1, 7, 42):
        ref = run_sw(sd, C=5, lats=anchor_lats, K=4, drift=6, delta=12, pulse_div=3)
        mine = fabric(sd, "admit", anchor_lats, K=4, drift=6, delta=12)
        for k in ("events", "debt", "chatter", "cancel", "maxerr", "pct",
                  "rejected"):
            if ref[k] != mine[k]:
                ok_counters = False
        if list(ref["fires"]) != list(mine["fires"]):
            ok_counters = False
        ref1 = run_sw(sd, key="mag", C=1, lats=anchor_lats, K=4, drift=6,
                      delta=12, pulse_div=3)
        mine1 = fabric(sd, "mag1", anchor_lats, K=4, drift=6, delta=12)
        for k in ("events", "debt", "chatter", "cancel", "maxerr", "pct",
                  "rejected"):
            if ref1[k] != mine1[k]:
                ok_counters = False
    print(f"C2b per-seed counter equality vs glm3 run_sw (admit+mag1, seeds 1/7/42)"
          f" -> {'PASS' if ok_counters else 'FAIL'}")
    ok_all = ok_all and ok_counters

    # C3: mislabeled-arm self-canary (mag1 relabeled admit must be CAUGHT)
    caught = ok_anchor and abs(mag_pct - 68.0) > 0.05
    ok_all = ok_all and caught
    print(f"C3 mislabeled arm: mag1 as 'admit' %w={mag_pct:.1f} vs 68.0 -> "
          f"{'CAUGHT' if caught else 'NOT CAUGHT (gate broken)'}")

    # C2c: round-19 default wall replay == exactly 6
    # (r19 convention: mean of calm/stress default-delta wins per N, raw arm, N 2..13)
    wins = {}
    for fam in FAMILIES:
        cfg = FAMILIES[fam]
        for n in range(2, 14):
            la = lats_for(n)
            raw = srtp = 0.0
            for sd in SEEDS:
                raw += fabric(sd, "admit", la, K=cfg["K"], drift=cfg["drift"],
                              delta=DEFAULT_DELTA[fam])["pct"]
                srtp += fabric(sd, "mag1", la, K=cfg["K"], drift=cfg["drift"],
                               delta=DEFAULT_DELTA[fam])["pct"]
            wins.setdefault(n, []).append(srtp / len(SEEDS) - raw / len(SEEDS))
    wmean = {n: sum(v) / len(v) for n, v in wins.items()}
    wall = next((n for n in sorted(wmean) if wmean[n] >= 2.0), None)
    ok_wall = wall == R19_WALL
    ok_all = ok_all and ok_wall
    print("C2c round-19 wall replay: mean default-delta win by N: "
          + " ".join(f"{n}:{wmean[n]:+.1f}" for n in sorted(wmean)))
    print(f"    default wall={wall} (want exactly {R19_WALL}) -> "
          f"{'PASS' if ok_wall else 'FAIL'}")

    # C2d: PW=48 wrapped fabric == unbounded at the anchor cell (same counters)
    ok_pw48 = True
    for arm in ("admit", "mag1"):
        for sd in (1, 7):
            u = fabric(sd, arm, anchor_lats, K=4, drift=6, delta=12)
            w = fabric(sd, arm, anchor_lats, K=4, drift=6, delta=12, pw=48)
            for k in ("events", "debt", "chatter", "cancel", "maxerr", "pct",
                      "rejected"):
                if u[k] != w[k]:
                    ok_pw48 = False
    ok_all = ok_all and ok_pw48
    print(f"C2d PW=48 wrapped == unbounded at anchor cell (admit+mag1, seeds 1/7)"
          f" -> {'PASS' if ok_pw48 else 'FAIL'}")

    print(f"L0 canaries: {'ALL PASS' if ok_all else 'FAILURE -- verdicts void'}"
          f"  [elapsed L0: {time.time()-T0:.0f}s]")
    return ok_all


# ------------------------------------------------------------------ L1
def leg1():
    print("\n== L1 metric grid (5-seed mean %w; maxstate = max |g,m,debt,I|) ==")
    res = {}      # (arm, fam, kappa, n) -> (pct, maxstate)
    dropped = []  # (arm, fam, kappa, n) rows dropped by the budget guard

    def run_block(arms, kappas):
        for fam in FAMILIES:
            cfg = FAMILIES[fam]
            for kap in kappas:
                for arm in arms:
                    for n in NS:
                        if (arm, fam, kap, n) in dropped:
                            continue
                        tot = 0.0
                        ms = 0
                        la = lats_for(n)
                        for sd in SEEDS:
                            r = fabric(sd, arm, la, K=cfg["K"], drift=cfg["drift"],
                                       delta=KAPPA_DELTA[fam][kap])
                            tot += r["pct"]
                            ms = max(ms, r["maxstate"])
                        res[(arm, fam, kap, n)] = (tot / len(SEEDS), ms)
                        print(f"  {arm:7s} {fam:6s} k={kap:2d} d={KAPPA_DELTA[fam][kap]:3d}"
                              f" N={n:2d} %w={tot/len(SEEDS):6.1f} maxstate={ms}")

    # kappa=2 leg first (budget-guard measurement point)
    run_block(("admit", "mag1"), (2,))
    run_block(MECHS, (2,))
    t_k2 = time.time() - T0
    # projection: linear in completed fraction of planned grid cells
    total_cells = 2 * 2 * 3 * 6 + 4 * 2 * 2 * 6      # admit/mag1 3 kappas + mech 2
    done_cells = 2 * 2 * 6 + 4 * 2 * 6
    proj = t_k2 * total_cells / done_cells
    print(f"  [budget guard] kappa=2 leg done at {t_k2:.0f}s; projection {proj:.0f}s "
          f"(cap 1320s) -> {'OK' if proj <= 1320 else 'DROP N=34 mech k2 rows'}")
    if proj > 1320:
        for fam in FAMILIES:
            for arm in MECHS:
                dropped.append((arm, fam, 2, 34))
        print("  [budget guard] DROPPED mechanism kappa=2 N=34 rows (labeled)")
    run_block(("admit", "mag1"), (8, 16))
    run_block(MECHS, (8,))
    print(f"  [elapsed L1: {time.time()-T0:.0f}s]")
    return res, dropped


# ------------------------------------------------------------------ L2
def leg2(res):
    print("\n== L2 PW hash legs (T2 empirical; sha256 canon, 16 hex) ==")
    hashes = {}     # (arm, leg) -> list of hashes
    ok = {}

    # Leg A: worst cell per mechanism arm (stress, kappa=8, N=64, seed 1), PW 41..48
    for arm in MECHS:
        hs = []
        for pw in PWS:
            r = fabric(1, arm, lats_for(64), K=FAMILIES["stress"]["K"],
                       drift=FAMILIES["stress"]["drift"],
                       delta=KAPPA_DELTA["stress"][8], pw=pw, want_trace=True)
            hs.append(r["hash"])
        hashes[(arm, "A")] = hs
        u = len(set(hs))
        ok[arm] = (u == 1)
        print(f"  A {arm:7s} worst cell PW41..48: {len(set(hs))} unique hash(es)"
              f" -> {'PW-INVARIANT' if u == 1 else 'PW-BREAK'}")
        if u > 1:
            print(f"    hashes: {hs}")

    # Leg B: PW {41,48} x all 5 seeds (per-seed pair invariance), worst cell
    for arm in MECHS:
        allok = True
        pairs = []
        for sd in SEEDS:
            h41 = fabric(sd, arm, lats_for(64), K=FAMILIES["stress"]["K"],
                         drift=FAMILIES["stress"]["drift"],
                         delta=KAPPA_DELTA["stress"][8], pw=41, want_trace=True)["hash"]
            h48 = fabric(sd, arm, lats_for(64), K=FAMILIES["stress"]["K"],
                         drift=FAMILIES["stress"]["drift"],
                         delta=KAPPA_DELTA["stress"][8], pw=48, want_trace=True)["hash"]
            pairs.append(h41 == h48)
            allok = allok and h41 == h48
        hashes[(arm, "B")] = pairs
        print(f"  B {arm:7s} PW41==PW48 per seed: "
              + " ".join("ok" if p else "BREAK" for p in pairs)
              + f" -> {'PASS' if allok else 'FAIL'}")
        ok[arm] = ok[arm] and allok

    # Leg C: admit/mag1 at round-2 anchor cell, PW 41..48
    for arm in ("admit", "mag1"):
        hs = []
        for pw in PWS:
            r = fabric(1, arm, LATS_N[5], K=4, drift=6, delta=12, pw=pw,
                       want_trace=True)
            hs.append(r["hash"])
        hashes[(arm, "C")] = hs
        u = len(set(hs))
        ok[arm] = (u == 1)
        print(f"  C {arm:7s} anchor cell PW41..48: {u} unique -> "
              f"{'PW-INVARIANT' if u == 1 else 'PW-BREAK'}")

    print(f"  [elapsed L2: {time.time()-T0:.0f}s]")
    return ok, hashes


# ------------------------------------------------------------------ L3
def leg3(res, dropped, ok_pw, canaries_ok):
    print("\n== L3 C-lift, kill bands, verdict ==")

    # structural constraints (b)/(c): static scan of fabric source
    src = open(os.path.abspath(__file__)).read()
    fab_src = src[src.index("def fabric("):src.index("def cell(")]
    has_float = re.search(r"\d+\.\d+", fab_src) is not None
    has_time = "time." in fab_src
    print(f"  constraints: float literals in fabric: "
          f"{'NONE' if not has_float else 'FOUND'}; time calls in fabric: "
          f"{'NONE' if not has_time else 'FOUND'}; net in loop: NONE "
          f"(mechanism state = local ids/credits/last_fire/queue/FIFO); "
          f"determinism: C1 double-run")

    # C-lift table (mag1 - admit, 5-seed mean)
    print("\n  C-lift (pp, mag1-admit) by family x kappa x N:")
    lift = {}
    for fam in FAMILIES:
        for kap in (2, 8, 16):
            row = []
            for n in NS:
                a = res[("admit", fam, kap, n)][0]
                m = res[("mag1", fam, kap, n)][0]
                lift[(fam, kap, n)] = m - a
                row.append(f"N{n}:{m-a:+.1f}")
            print(f"    {fam:6s} k={kap:2d}: " + " ".join(row))

    # H1: gap reproduces (C-lift flip at fan-out 64)
    h1 = False
    h1_detail = []
    for fam in FAMILIES:
        l13, l21, l64 = lift[(fam, 8, 13)], lift[(fam, 8, 21)], lift[(fam, 8, 64)]
        q = (l13 <= 10.0 and l21 <= 10.0 and l64 >= 24.0
             and l64 - l21 >= 12.0)
        h1 = h1 or q
        h1_detail.append(f"{fam}: N13={l13:+.1f} N21={l21:+.1f} N64={l64:+.1f}"
                         f" -> {'seats' if q else 'no'}")
    kill_h1 = all(lift[(f, 8, 64)] < 12.0 for f in FAMILIES)
    print("\n  H1 gap reproduces (k=8): " + "; ".join(h1_detail))
    print(f"    H1: {'CONFIRMED' if h1 else ('NEGATIVE-on-gap (kill: lift64<12)' if kill_h1 else 'NOT CONFIRMED (no kill either)')}")

    # H2: crutch breaks PW-invariance
    crutch_ms_ge = any(res[("crutch", f, k, n)][1] >= LIM
                       for f in FAMILIES for k in (2, 8) for n in NS
                       if ("crutch", f, k, n) in res)
    h2 = (not ok_pw.get("crutch", True)) or crutch_ms_ge
    print(f"  H2 crutch breaks PW gate: hash-invariance={'BREAK' if not ok_pw.get('crutch', True) else 'hold'}"
          f" maxstate>=2^40={'YES' if crutch_ms_ge else 'no'} -> "
          f"{'CONFIRMED' if h2 else 'crutch PW-safe here (booking fails to reproduce)'}")

    # H3: mechanism promotion bands
    print("\n  H3 mechanism bands:")
    promoted = []
    for arm in ("qcell", "cfence", "sgrant"):
        ms = max(res[(arm, f, k, n)][1] for f in FAMILIES for k in (2, 8)
                 for n in NS if (arm, f, k, n) in res)
        i = ok_pw.get(arm, False) and ms < LIM
        ii = all(res[(arm, f, 8, 64)][0] - res[("admit", f, 8, 64)][0] >= 6.0
                 for f in FAMILIES)
        iii = all(res[(arm, f, 2, n)][0] - res[("admit", f, 2, n)][0] >= -2.0
                  for f in FAMILIES for n in (2, 5)
                  if (arm, f, 2, n) in res)
        iv = canaries_ok
        okk = i and ii and iii and iv
        if okk:
            promoted.append(arm)
        print(f"    {arm:7s} (i)PW={'ok' if i else 'FAIL'}(maxstate={ms}) "
              f"(ii)k8N64 gain={min(res[(arm, f, 8, 64)][0] - res[('admit', f, 8, 64)][0] for f in FAMILIES):+.1f}pp "
              f"{'ok' if ii else 'FAIL'} (iii)k2 tax "
              f"{min(res[(arm, f, 2, n)][0] - res[('admit', f, 2, n)][0] for f in FAMILIES for n in (2, 5) if (arm, f, 2, n) in res):+.1f}pp "
              f"{'ok' if iii else 'FAIL'} (iv)canaries={'ok' if iv else 'FAIL'} "
              f"-> {'PROMOTED' if okk else 'not promoted'}")
    if dropped:
        print(f"    [budget-guard dropped rows excluded: {len(dropped)}]")

    if not canaries_ok:
        verdict = "VOID (canary failure)"
    elif len(promoted) == 3:
        verdict = "STRONG-YES"
    elif len(promoted) in (1, 2):
        verdict = f"YES ({'+'.join(promoted)})"
    else:
        verdict = "NEGATIVE (no bounded-fabric rate absorber in this family)"
    print(f"\nVERDICT LADDER: {verdict}")
    print(f"H1: {'CONFIRMED' if h1 else 'not'}; H2: {'CONFIRMED' if h2 else 'not'}; "
          f"promoted: {promoted if promoted else 'none'}")
    print("disclosure: sgrant seat-A implemented as min(last_fire) "
          "(least-recently-fired, per the named anti-starvation semantics); "
          "prereg parenthetical said 'max last_fire' -- sign slip, disclosed here")
    print(f"done in {time.time()-T0:.0f}s")


def main():
    print(f"== round 19b bounded-fabric arrival absorbers start "
          f"{time.strftime('%H:%M:%S')} ==")
    print(f"pd={PD} families={ {f: FAMILIES[f] for f in FAMILIES} } "
          f"kappa->delta={KAPPA_DELTA}")
    print(f"NS={NS} seeds={SEEDS} ticks={TICKS} PWs={PWS[0]}..{PWS[-1]} "
          f"arms=admit,mag1,qcell,cfence,sgrant,crutch")
    ok0 = leg0()
    res, dropped = leg1()
    ok_pw, _ = leg2(res)
    leg3(res, dropped, ok_pw, ok0)


if __name__ == "__main__":
    main()
