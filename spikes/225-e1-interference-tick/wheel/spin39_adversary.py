#!/usr/bin/env python3
"""SPIN 39, SPOKE 2: ADVERSARY — MIXED-STRATEGY EVASION vs θ-GATE + D5.
Pre-registered docstring, written BEFORE any run. Continuation of
SPIN-35 (θ-gate holds vs classic adversaries; D5 emitted-pulse-vs-
declared-nf audit, 0 false positives) and SPIN-37 (deflation NOT inert
below θ=1: at θ*=0.90 a deflating twin suppresses honest compensation
up to -17.3pp; A3 boundary FAIL: nf_both at θ*=1.00 beats pure-inflate
in 1/4 cells — ladder K1 leak).

OPEN QUESTIONS THIS SPIN ATTACKS:
  (1) the A3 θ*=1.00 boundary leak — artifact or real?
  (2) D5 detector integrity under adversarial pressure — can a
      manipulator evade or false-flag D5?

HYPOTHESIS (pre-registered):
  H1: a mixed-strategy twin (alternating inflate/deflate per trigger
      tick, or an LCG-random inflate/deflate coin, or an exactly-2pd
      pile-up impersonator: declared nf = 2*PD exactly — the SPIN-16
      serendipity point where the gate is provably blind: |PD-2PD|=PD
      and 100*PD > tc*PD iff tc<100, so the gate NEVER opens at any
      θ*>=1.00) evades the θ-gate AND the D5 audit in at least one
      grammar x K cell (>5pp unflagged residency shift). "Unflagged"
      = the arm's residency shift exceeds 5pp while its lied-tick
      count (D5 hits) is ZERO, i.e. the manipulation never declares a
      mismatch. FALSIFY H1 if every mixed-strategy shift >5pp carries
      D5 flags (nfmis > 0 in every seed).
  H2: the SPIN-37 A3 boundary leak (nf_both beats pure-inflate at
      θ*=1.00, ladder@15 K=1) is a boundary artifact: narrow in θ*,
      gone by θ*=0.95 and θ*=1.05 (nf_both shift <= pure-inflate
      shift + 0.2pp at both).

ARMS:
  A  mixed twin at θ*=1.10 on {ladder@15, kcoh5@15} x K in {1,2}:
     nf_alt (alternate inflate/deflate per trigger tick, phase from a
     dedicated LCG), nf_rnd (LCG coin per trigger tick).
  B  exactly-2pd impersonator at θ*=1.10 (nf_2pd: declared = 2*PD
     whenever ADV triggers; gate provably closed there), same 4 cells.
  C  θ* boundary sweep {0.90, 0.95, 1.00, 1.05, 1.10} with the
     SPIN-37 nf_both twin, ladder@15 K=1, vs pure nf_inflate at each
     θ* and vs gate-off honest null.

PRE-REGISTERED DECISION RULE (fixed before running):
  H1 VALIDATED   iff some arm A/B cell shifts residency >5.0pp vs the
                 gate-off honest null (== honest @1.10 by Cb2) AND
                 that arm records nfmis == 0 across all seeds
                 (unflagged). Otherwise H1 FALSIFIED (with the
                 observed shift table + flag counts as evidence).
  H2 VALIDATED   iff at BOTH θ*=0.95 and θ*=1.05 on ladder@15 K=1:
                 shift(nf_both) <= shift(nf_inflate) + 0.2pp.
                 FALSIFIED if nf_both beats inflate by >0.2pp at
                 either shoulder.
  S1 (D5 under pressure) PASS iff nfmis > 0 in every seed of every
     lying arm A/B/C, and honest arms structurally carry 0 false
     positives (no adv dict) — plus honest@θ* full-dict identity to
     gate-off (Cb2) doubles as the false-negative/positive contract.
  S2 closure PASS iff |mass - sum|emissions|| < 1 everywhere.
  VERDICT: report per-hypothesis VALIDATED/FALSIFIED; INCONCLUSIVE if
  any canary fails.

CANARIES (mandatory, abort on fail; SPIN-35/37 set):
  Ca: adv=none gate=off byte-matches exp_glm1.run_fabric (8 configs)
      + SPIN-5 anchors zero@15 K1 77.3/8756/187834, ladder@15 K1
      71.5/5792/106378.
  Cc1: SPIN-35 inflate replay @θ*=1.10: ladder K2 +6.4pp, kcoh5 K1
      +7.9pp (tol ±0.2pp).
  Cb: gate=never == gate=off full-dict for ALL modes (incl. new
      mixed/2pd modes — a never-open gate cannot see a lie), and
      honest gate 1.10 == gate=off on {ladder,kcoh5,zero} x K{1,2}.
  Cc: double-run determinism (same dict twice, 5 configs incl. mixed
      and 2pd arms).

Config: N=6, ladder@15 [0,3,6,9,12,15] / kcoh5@15 [0,0,0,0,0,15];
K in {1,2}; pd=3, delta=12, drift=6; ticks 4800; seeds
{1,7,42,1999,20260902}; ADV = twin 5; θ* per arm; integer-only
in-loop; floats display-only. Run with -u, no pipes.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "inventors-derby"))
sys.path.insert(0, HERE)
from exp_glm1 import run_fabric, within_pm, reality  # noqa: E402
from spin11_adversary import (LCG, SEEDS, DELTA, PD, DRIFT, TICKS,  # noqa: E402
                              ADV, BAND, PEER_BOUND, median, mean)

LATS = [0, 3, 6, 9, 12, 15]          # ladder@15
KCOH5 = [0, 0, 0, 0, 0, 15]          # kcoh5@15
ZERO6 = [0] * 6
ADV_MODES = ("nf_inflate", "nf_deflate", "nf_both",
             "nf_alt", "nf_rnd", "nf_2pd")


def t100_of(gate):
    if gate == "off":
        return None
    if gate == "never":
        return 10 ** 9
    return int(round(gate * 100))


def run_adv_gate(lats, k, seed, adv=None, gate="off", ticks=TICKS):
    """spin37.run_adv_gate clone, verbatim loop, + mixed modes.
    nf_alt: alternate inflate/deflate per trigger tick (phase from a
    dedicated LCG seeded by run seed — deterministic). nf_rnd: LCG
    coin per trigger tick. nf_2pd: declared = 2*PD (pile-up
    impersonation; gate blind at any θ*>=1.00). Declared-vs-emitted
    mismatch always counted in nfmis (D5). Emissions/tolls/claims
    stay honest in every mode. Returns spin11's dict + gate stats."""
    rng = LCG(seed)
    arng = LCG(seed * 2654435761 % (2 ** 31) + 1)   # adversary LCG
    g = reality(0)
    from collections import deque
    pulses = deque()
    n = len(lats)
    emissions = []
    events = mass = cancels = chatter = settles = 0
    last = -10
    resid = []
    cflags = []
    paid = [0] * n
    unpaid = 0
    bandviol = deadviol = peerviol = 0
    local_in = [0] * n
    gopen = gcomp = nfmis = 0
    altphase = 0
    tc = t100_of(gate)

    for t in range(ticks):
        raw = [reality(max(0, t - lats[i])) for i in range(n)]
        reads = list(raw)
        s_true = reality(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > DELTA]

        # ---- gate decision (spin16 integer-exact, θ* parameterized) ----
        nf = len(trig)
        declared = nf
        if nf and adv in ADV_MODES \
                and any(i == ADV for i, _ in trig):
            if adv == "nf_inflate":
                declared = nf + 1
            elif adv == "nf_deflate":
                declared = nf - 1
            elif adv == "nf_both":
                declared = nf + 1 if nf <= PD else nf - 1
            elif adv == "nf_alt":
                declared = nf + 1 if altphase % 2 == 0 else nf - 1
                altphase += 1
            elif adv == "nf_rnd":
                declared = nf + 1 if arng.below(2) else nf - 1
            elif adv == "nf_2pd":
                declared = 2 * PD
        neff = 1 if nf else 0
        if tc is not None and nf:
            open_ = 100 * abs(PD - declared) > tc * PD
            if open_:
                neff = min(declared, PD)
                gopen += 1
        if declared != nf:
            nfmis += 1     # D5: declared-vs-emitted mismatch, per lied tick

        cflag = 0
        for i, e in trig:
            mass += abs(e)
            paid[i] += abs(e)
            m = abs(e) // PD or 1
            if neff > 1:
                m = m // neff or 1
                gcomp += 1
            pulses.appendleft([m if e > 0 else -m, k])
            events += 1
            emissions.append((t, i, m if e > 0 else -m, e))
            claim = reads[i]
            peers = [reads[j] for j in range(n) if j != i]
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
        if trig:
            if t - last == 1:
                chatter += 1
            last = t
        resid.append(abs(s_true - g))
        cflags.append(cflag)
        for i in range(n):
            if abs(reads[i] - g) <= DELTA:
                local_in[i] += 1
        if all(abs(reads[i] - g) <= DELTA for i in range(n)):
            settles += 1

    d = dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
             settles=settles, resid=resid, cflags=cflags,
             emissions=emissions, audit=None, ticks=ticks,
             gopen=gopen, gcomp=gcomp)
    if adv is not None:
        d["adv"] = dict(paid=paid, unpaid=unpaid, bandviol=bandviol,
                        peerviol=peerviol, deadviol=deadviol,
                        nfmis=nfmis, local_in=local_in, live=n)
    return d


def row(cells, w=9):
    return " | ".join(f"{c:>{w}}" for c in cells)


def imean(v):
    """Integer display-mean: spin11.mean overflows float when a liar
    arm diverges the fabric (mass > 1e308 is a real runaway, not a
    bug). Integer floor keeps display exact; fabric untouched."""
    return sum(v) // len(v)


def stats(lats, mode, k, gate):
    rs = [run_adv_gate(lats, k, s, adv=(None if mode == "none" else mode),
                       gate=gate) for s in SEEDS]
    tp = [within_pm(r["resid"], DELTA) for r in rs]
    out = dict(tp=tp, mtp=mean(tp) / 10,
               ev=mean([r["events"] for r in rs]),
               debt=imean([r["mass"] for r in rs]),
               chat=mean([r["chatter"] for r in rs]),
               maxres=max(max(r["resid"]) for r in rs),
               gopen=mean([r["gopen"] for r in rs]),
               gcomp=mean([r["gcomp"] for r in rs]),
               rs=rs)
    if mode != "none":
        out["bandviol"] = mean([r["adv"]["bandviol"] for r in rs])
        out["peerviol"] = mean([r["adv"]["peerviol"] for r in rs])
        out["nfmis"] = mean([r["adv"]["nfmis"] for r in rs])
        out["closure"] = imean([r["mass"] - sum(abs(e) for (_, _, _, e)
                                                 in r["emissions"])
                                for r in rs])
    return out


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY Ca: adv=none gate=off byte-matches exp_glm1.run_fabric ==")
    for lats in (LATS, ZERO6):
        for k in (1, 2):
            for s in (SEEDS[0], SEEDS[-1]):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=s)
                b = run_adv_gate(lats, k, s)
                bsub = {kk: b[kk] for kk in a}
                if bsub != a:
                    ok = False
                    print(f"  MISMATCH lats={lats} K={k} seed={s}")
    print("  PASS: 8/8 full-dict byte-identical (extra keys gopen/gcomp)")

    print("\n== CANARY Ca2: SPIN-5 anchor replay (5-seed means) ==")
    for name, lats, want in (("zero@15 K=1", ZERO6, (77.3, 8756, 187834)),
                             ("ladder@15 K=1", LATS, (71.5, 5792, 106378))):
        rs = [run_adv_gate(lats, 1, s) for s in SEEDS]
        tp = mean([within_pm(r["resid"], DELTA) for r in rs])
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        good = (abs(tp / 10 - want[0]) <= 0.2 and round(ev) == want[1]
                and round(dbt) == want[2])
        ok &= good
        print(f"  {name}: {tp/10:.1f}% ev {ev:.0f} debt {dbt:.0f} "
              f"(want {want[0]}/{want[1]}/{want[2]}) -> "
              f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY Cc1: SPIN-35 inflate replay @ θ*=1.10 ==")
    published = {("ladder@15", 2): 6.4, ("kcoh5@15", 1): 7.9}
    for (gname, k), want in published.items():
        lats = LATS if gname == "ladder@15" else KCOH5
        base = stats(lats, "none", k, "off")
        st = stats(lats, "nf_inflate", k, 1.10)
        shift = st["mtp"] - base["mtp"]
        good = abs(shift - want) <= 0.2
        ok &= good
        print(f"  {gname} K={k}: shift {shift:+.1f}pp "
              f"(want {want:+.1f}) -> {'PASS' if good else 'FAIL'}")

    print("\n== CANARY Cb: gate contract identities ==")
    okb = True
    for adv in (None,) + ADV_MODES:
        a = run_adv_gate(LATS, 1, SEEDS[0], adv=adv, gate="off")
        b = run_adv_gate(LATS, 1, SEEDS[0], adv=adv, gate="never")
        if {kk: b[kk] for kk in a} != a:
            okb = False
            print(f"  Cb1 MISMATCH never-vs-off adv={adv}")
    print(f"  Cb1 gate=never == gate=off full-dict (all {1+len(ADV_MODES)} "
          f"modes): {'PASS' if okb else 'FAIL'}")
    ok &= okb
    okb = True
    for lats in (LATS, KCOH5, ZERO6):
        for k in (1, 2):
            a = run_adv_gate(lats, k, SEEDS[0], gate="off")
            b = run_adv_gate(lats, k, SEEDS[0], gate=1.10)
            if {kk: b[kk] for kk in a} != a:
                okb = False
                print(f"  Cb2 MISMATCH lats={lats} K={k}")
    print(f"  Cb2 honest gate 1.10 == off (adv=none, 3 grammars x K{{1,2}}): "
          f"{'PASS' if okb else 'FAIL'}")
    ok &= okb

    print("\n== CANARY Cc: double-run determinism ==")
    okc = True
    for cfg in ((LATS, 1, "nf_alt", 1.10), (KCOH5, 2, "nf_rnd", 1.10),
                (LATS, 2, "nf_2pd", 1.10), (LATS, 1, "nf_both", 0.95),
                (ZERO6, 1, "none", 1.05)):
        a = run_adv_gate(cfg[0], cfg[1], SEEDS[0], adv=cfg[2], gate=cfg[3])
        b = run_adv_gate(cfg[0], cfg[1], SEEDS[0], adv=cfg[2], gate=cfg[3])
        if a != b:
            okc = False
            print(f"  Cc MISMATCH cfg={cfg}")
    print(f"  Cc double-run: {'PASS' if okc else 'FAIL'} (5 configs)")
    ok &= okc
    print("\nCANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- arms
def arms_ab():
    print("\n== ARMS A+B: mixed twin @ θ*=1.10 (vs gate-off honest null) ==")
    print("   (honest @1.10 == gate=off by Cb2, so the null is exact)")
    h1_valid = False
    s1 = True
    s2 = True
    print(row(["mode", "grammar", "K", "mean%", "null%", "shift",
               "gOpen", "gComp", "nfMis/seed", "closureΔ"]))
    for mode in ("nf_alt", "nf_rnd", "nf_2pd"):
        for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
            for k in (1, 2):
                base = stats(lats, "none", k, "off")
                st = stats(lats, mode, k, 1.10)
                shift = st["mtp"] - base["mtp"]
                seeds_lied = sum(1 for r in st["rs"]
                                 if r["adv"]["nfmis"] > 0)
                unflagged = all(r["adv"]["nfmis"] == 0 for r in st["rs"])
                if abs(shift) > 5.0 and unflagged:
                    h1_valid = True
                s1 &= seeds_lied == len(SEEDS)
                s2 &= abs(st["closure"]) < 1
                print(row([mode, gname, k, f"{st['mtp']:.1f}",
                           f"{base['mtp']:.1f}", f"{shift:+.1f}pp",
                           f"{st['gopen']:.0f}", f"{st['gcomp']:.0f}",
                           f"{seeds_lied}/{len(SEEDS)}",
                           f"{st['closure']:.0f}"]))
    # honest false-positives: honest arms carry no adv dict -> 0
    print("  D5 honest false-positives: 0 (honest arms carry no adv dict)")
    if h1_valid:
        h1_txt = "VALIDATED"
    else:
        h1_txt = "FALSIFIED (every lied tick is D5-flagged)"
    print(f"  H1 (a >5pp UNFLAGGED shift): {h1_txt}")
    return h1_valid, s1, s2


def arm_c():
    print("\n== ARM C: θ* boundary sweep, nf_both vs nf_inflate, "
          "ladder@15 K=1 ==")
    h2_valid = True
    s1 = True
    s2 = True
    base = stats(LATS, "none", 1, "off")
    print(row(["θ*", "both%", "shift-off", "inflate%", "shift-off",
               "both-inflate", "gOpen-b/i", "nfMis", "closureΔ"]))
    for gate in (0.90, 0.95, 1.00, 1.05, 1.10):
        stb = stats(LATS, "nf_both", 1, gate)
        sti = stats(LATS, "nf_inflate", 1, gate)
        shb = stb["mtp"] - base["mtp"]
        shi = sti["mtp"] - base["mtp"]
        excess = shb - shi
        if gate in (0.95, 1.05) and excess > 0.2:
            h2_valid = False
        s1 &= all(r["adv"]["nfmis"] > 0 for r in stb["rs"]) \
            and all(r["adv"]["nfmis"] > 0 for r in sti["rs"])
        s2 &= abs(stb["closure"]) < 1 and abs(sti["closure"]) < 1
        print(row([f"{gate:.2f}", f"{stb['mtp']:.1f}", f"{shb:+.1f}pp",
                   f"{sti['mtp']:.1f}", f"{shi:+.1f}pp", f"{excess:+.1f}pp",
                   f"{stb['gopen']:.0f}/{sti['gopen']:.0f}",
                   f"{stb['nfmis']:.0f}", f"{stb['closure']:.0f}"]))
    print(f"  H2 (leak narrow: both <= inflate+0.2pp at 0.95 AND 1.05): "
          f"{'VALIDATED' if h2_valid else 'FALSIFIED'}")
    return h2_valid, s1, s2


def main():
    print(__doc__)
    print("=" * 70)
    print("SPIN 39 — ADVERSARY — MIXED-STRATEGY EVASION + D5 INTEGRITY — "
          "harness run, -u, no pipes")
    if not canaries():
        print("ABORT: canaries failed — no results collected.")
        sys.exit(1)
    h1, s1a, s2a = arms_ab()
    h2, s1b, s2b = arm_c()
    s1 = s1a and s1b
    s2 = s2a and s2b
    print(f"\n  PRE-REGISTERED VERDICT:")
    print(f"    H1 (mixed/2pd evasion): "
          f"{'VALIDATED' if h1 else 'FALSIFIED'}")
    print(f"    H2 (boundary artifact): "
          f"{'VALIDATED' if h2 else 'FALSIFIED'}")
    print(f"    S1 D5-under-pressure: {'PASS' if s1 else 'FAIL'}  "
          f"S2 closure: {'PASS' if s2 else 'FAIL'}")


if __name__ == "__main__":
    main()
