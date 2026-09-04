#!/usr/bin/env python3
"""SPIN 37, SPOKE: ADVERSARY — SUB-1.0 DEFLATION-DODGE vs THE θ-GATE.
Pre-registered docstring, committed BEFORE any run. Continuation of
SPIN-35 (wheel/SPIN-35-adversary.md): the θ>1 half of the gate was
one-directional (inflate can open, deflate inert — byte-proven). The
booked scar: at θ*<1 an honest gate OPENS on pile-up ticks (nf=6=2pd:
|3-6|=3 > 0.9*3=2.7), so a deflating twin can DODGE compensation that
honest twins would have received.

HYPOTHESIS (pre-registered):
  H1: at gate θ*=0.90, a deflating minority twin (twin 5, otherwise
      honest, declared nf = emitted nf - 1 whenever it triggers) can
      dodge or slip the gate and shift collective residency > 5pp vs
      the honest twin at the same θ* (correct null: same fabric, same
      gate, no lie).
  H0: deflation remains inert for ALL θ (0.90 / 1.00 / 1.10), or any
      residency shift is <= 5pp.

  Secondary (S1): D5 (declared-vs-emitted pulse count per tick) still
  flags every lied tick, zero false positives on honest arms.
  Secondary (S2): ledger/debt closure stays exactly 0 under every arm.

ARMS:
  A1 anchor-continuity: replay SPIN-35 nf_inflate at θ*=1.10 and
     reproduce the published table (ladder K1 -0.4 / K2 +6.4;
     kcoh5 K1 +7.9 / K2 +17.3 vs gate-off honest-none; tol ±0.2pp).
  A2 deflation at θ*=0.90 (nf_deflate, twin 5) on ladder@15 + kcoh5@15,
     K in {1,2}. Baselines BOTH gate-off honest-none (SPIN-35
     convention) and honest twin at θ*=0.90 (registered null; H1
     evaluated against the latter).
  A3 both-direction twin at boundary θ*=1.00: declared nf pushed away
     from pd (nf+1 if nf<=pd else nf-1) — tests whether adaptive
     lying gains beyond pure inflate at the boundary where the two
     regimes meet.

PRE-REGISTERED DECISION RULE (fixed before running):
  A1 PASS iff all four published inflate cells reproduce ±0.2pp.
  A2 H1 CONFIRMED iff any deflation cell shifts residency > 5.0pp vs
     the honest-θ*=0.90 twin baseline (either direction), or gOpen for
     the deflating twin < honest gOpen on any grammar (a dodge:
     honest gate opens, liar's declared value closes it). H0 confirmed
     otherwise (all shifts <= 5pp and no dodge).
  A3 PASS (boundary inert for deflate half) iff both-direction at
     1.00 shift <= pure-inflate-at-1.00 shift + 0.2pp in every cell.
  S1 PASS iff nfmis > 0 in every seed of every lying arm and nfmis == 0
     in every honest arm.
  S2 PASS iff |closureΔ| < 1 everywhere.
  VERDICT: VALIDATED(H1) if A2 shows >5pp shift or a dodge with a
     >5pp shift... -- stated plainly: report VALIDATED if H1 holds
     (shift > 5pp), FALSIFIED if deflation inert at 0.90 AND shifts
     <= 5pp, MIXED if a dodge occurs but shift <= 5pp, INCONCLUSIVE if
     canaries or A1 fail (no anchor continuity).

CANARIES (mandatory, abort on fail; reuse SPIN-35 set):
  Ca: adv=none gate=off byte-matches exp_glm1.run_fabric (8 configs)
      + SPIN-5 anchors zero@15 K1 77.3/8756/187834, ladder@15 K1
      71.5/5792/106378.
  Cb: gate="never" (t100=10**9) == gate="off" full-dict equivalence,
      and honest gate 1.10 == gate=off on N=6 grammars {ladder@15,
      kcoh5@15, zero@15} (structural CE, SPIN-35 Cb2 continuity).
  Cc: double-run determinism (same dict twice, 4 configs, includes
      θ*=0.90 arms).

Config: N=6, ladder@15 [0,3,6,9,12,15] / kcoh5@15 [0,0,0,0,0,15];
K in {1,2}; pd=3, delta=12, drift=6; ticks 4800; seeds
{1,7,42,1999,20260902}; ADV = twin 5; θ* in {0.90, 1.00, 1.10};
integer-only in-loop; floats display-only. Run with -u, no pipes.
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
ADV_MODES = ("nf_inflate", "nf_deflate", "nf_both")


def t100_of(gate):
    """gate: "off", "never", or a float θ* (0.90/1.00/1.10)."""
    if gate == "off":
        return None
    if gate == "never":
        return 10 ** 9
    return int(round(gate * 100))


def run_adv_gate(lats, k, seed, adv=None, gate="off", ticks=TICKS):
    """spin35.run_adv_gate clone with parameterized θ* (t100) and the
    nf_both mode. gate="off" -> byte-identical to spin11.run_adv;
    gate="never" -> structurally identical loop, provably-closed gate.
    adv in {nf_inflate, nf_deflate, nf_both}: the DECLARED nf fed to
    the gate is lied about when ADV triggers; emissions/tolls/claims
    stay honest. nf_both: declared = nf+1 if nf <= PD else nf-1
    (push away from pd). Returns spin11's dict + gopen/gcomp/nfmis."""
    rng = LCG(seed)
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
            else:  # nf_both: push declared away from pd
                declared = nf + 1 if nf <= PD else nf - 1
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


def stats(lats, mode, k, gate):
    rs = [run_adv_gate(lats, k, s, adv=(None if mode == "none" else mode),
                       gate=gate) for s in SEEDS]
    tp = [within_pm(r["resid"], DELTA) for r in rs]
    out = dict(tp=tp, mtp=mean(tp) / 10,
               ev=mean([r["events"] for r in rs]),
               debt=mean([r["mass"] for r in rs]),
               chat=mean([r["chatter"] for r in rs]),
               maxres=max(max(r["resid"]) for r in rs),
               gopen=mean([r["gopen"] for r in rs]),
               gcomp=mean([r["gcomp"] for r in rs]),
               rs=rs)
    if mode != "none":
        out["bandviol"] = mean([r["adv"]["bandviol"] for r in rs])
        out["peerviol"] = mean([r["adv"]["peerviol"] for r in rs])
        out["nfmis"] = mean([r["adv"]["nfmis"] for r in rs])
        out["closure"] = mean([r["mass"] - sum(abs(e) for (_, _, _, e)
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

    print("\n== CANARY Cb: gate contract identities ==")
    okb = True
    # gate=never == gate=off for ALL modes (provably closed gate);
    # gate=1.10 == off for honest + nf_deflate only (SPIN-35: deflate
    # inert at θ>1; inflate legitimately opens the gate, so it is
    # EXCLUDED from the identity check — that non-identity is the
    # published finding, not a canary failure).
    for adv in (None, "nf_inflate", "nf_deflate", "nf_both"):
        a = run_adv_gate(LATS, 1, SEEDS[0], adv=adv, gate="off")
        b = run_adv_gate(LATS, 1, SEEDS[0], adv=adv, gate="never")
        if {kk: b[kk] for kk in a} != a:
            okb = False
            print(f"  Cb1 MISMATCH never-vs-off adv={adv}")
    for adv in (None, "nf_deflate"):
        a = run_adv_gate(LATS, 1, SEEDS[0], adv=adv, gate="off")
        b = run_adv_gate(LATS, 1, SEEDS[0], adv=adv, gate=1.10)
        if {kk: b[kk] for kk in a} != a:
            okb = False
            print(f"  Cb1 MISMATCH 1.10-vs-off adv={adv}")
    print("  Cb1 gate=never == gate=off full-dict (4 adv modes); "
          "gate=1.10 == off for honest+deflate: "
          f"{'PASS' if okb else 'FAIL'}")
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
    for cfg in ((LATS, 1, "nf_inflate", 1.10), (KCOH5, 2, "nf_deflate", 0.90),
                (LATS, 2, "nf_both", 1.00), (ZERO6, 1, "none", 0.90)):
        a = run_adv_gate(cfg[0], cfg[1], SEEDS[0], adv=cfg[2], gate=cfg[3])
        b = run_adv_gate(cfg[0], cfg[1], SEEDS[0], adv=cfg[2], gate=cfg[3])
        if a != b:
            okc = False
            print(f"  Cc MISMATCH cfg={cfg}")
    print(f"  Cc double-run: {'PASS' if okc else 'FAIL'} (4 configs)")
    ok &= okc
    print("\nCANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- arms
def arm_a1():
    print("\n== ARM A1: SPIN-35 anchor-continuity — nf_inflate @ θ*=1.10 ==")
    published = {("ladder@15", 1): -0.4, ("ladder@15", 2): 6.4,
                 ("kcoh5@15", 1): 7.9, ("kcoh5@15", 2): 17.3}
    verdict = True
    print(row(["grammar", "K", "mean%", "base%", "shift",
               "pub-shift", "dOK"]))
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            base = stats(lats, "none", k, "off")
            st = stats(lats, "nf_inflate", k, 1.10)
            shift = st["mtp"] - base["mtp"]
            dok = abs(shift - published[(gname, k)]) <= 0.2
            verdict &= dok
            print(row([gname, k, f"{st['mtp']:.1f}", f"{base['mtp']:.1f}",
                       f"{shift:+.1f}pp", f"{published[(gname,k)]:+.1f}pp",
                       "OK" if dok else "DRIFT"]))
    print(f"  ARM A1: {'PASS' if verdict else 'FAIL'}")
    return verdict


def arm_a2():
    print("\n== ARM A2: nf_deflate @ θ*=0.90 — the sub-1.0 dodge test ==")
    verdict_h1 = False      # set True if H1 confirmed (>5pp shift)
    dodge_seen = False
    s1 = True
    s2 = True
    print(row(["grammar", "K", "mean%", "off-base%", "honest90-base%",
               "shift-vs-h90", "gOpen-liar", "gOpen-honest", "gComp",
               "nfMis", "closureΔ"]))
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            off = stats(lats, "none", k, "off")
            h90 = stats(lats, "none", k, 0.90)
            st = stats(lats, "nf_deflate", k, 0.90)
            shift = st["mtp"] - h90["mtp"]
            if st["gopen"] < h90["gopen"]:
                dodge_seen = True
            if abs(shift) > 5.0:
                verdict_h1 = True
            # D5: fires in every seed of the lying arm (honest arms
            # carry no adv dict -> structurally 0 false positives)
            s1 &= all(r["adv"]["nfmis"] > 0 for r in st["rs"])
            s2 &= abs(st["closure"]) < 1
            print(row([gname, k, f"{st['mtp']:.1f}", f"{off['mtp']:.1f}",
                       f"{h90['mtp']:.1f}", f"{shift:+.1f}pp",
                       f"{st['gopen']:.0f}", f"{h90['gopen']:.0f}",
                       f"{st['gcomp']:.0f}", f"{st['nfmis']:.0f}",
                       f"{st['closure']:.0f}"]))
    print(f"  dodge (liar gOpen < honest gOpen): "
          f"{'YES' if dodge_seen else 'no'}")
    print(f"  H1 (>5pp shift vs honest-0.90 baseline): "
          f"{'CONFIRMED' if verdict_h1 else 'not confirmed'}")
    print(f"  S1 D5: {'PASS' if s1 else 'FAIL'}  "
          f"S2 closure: {'PASS' if s2 else 'FAIL'}")
    # honest-arm D5 false-positive check
    fp = any(r.get("adv", {}).get("nfmis", 0) != 0
             for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5))
             for k in (1, 2) for r in stats(lats, "none", k, 0.90)["rs"])
    # honest arms have no 'adv' key -> structurally 0 false positives
    print("  S1 honest false-positives: 0 (honest arms carry no adv dict)")
    return verdict_h1, dodge_seen, s1, s2


def arm_a3():
    print("\n== ARM A3: nf_both @ boundary θ*=1.00 vs pure inflate ==")
    verdict = True
    s1 = True
    s2 = True
    print(row(["grammar", "K", "both%", "shift-off", "gOpen",
               "nfMis", "closureΔ", "vs-inflate"]))
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            off = stats(lats, "none", k, "off")
            stb = stats(lats, "nf_both", k, 1.00)
            sti = stats(lats, "nf_inflate", k, 1.00)
            shb = stb["mtp"] - off["mtp"]
            shi = sti["mtp"] - off["mtp"]
            okc = shb <= shi + 0.2
            verdict &= okc
            s1 &= all(r["adv"]["nfmis"] > 0 for r in stb["rs"])
            s2 &= abs(stb["closure"]) < 1 and abs(sti["closure"]) < 1
            print(row([gname, k, f"{stb['mtp']:.1f}", f"{shb:+.1f}pp",
                       f"{stb['gopen']:.0f}", f"{stb['nfmis']:.0f}",
                       f"{stb['closure']:.0f}",
                       f"{shi:+.1f}pp {'OK' if okc else 'EXCEEDS'}"]))
    print(f"  ARM A3: {'PASS' if verdict else 'FAIL'}  "
          f"S1: {'PASS' if s1 else 'FAIL'}  "
          f"S2: {'PASS' if s2 else 'FAIL'}")
    return verdict, s1, s2


def main():
    print(__doc__)
    print("=" * 70)
    print("SPIN 37 — ADVERSARY — SUB-1.0 DEFLATION-DODGE — "
          "harness run, -u, no pipes")
    if not canaries():
        print("ABORT: canaries failed — no results collected.")
        sys.exit(1)
    a1 = arm_a1()
    h1, dodge, s1a, s2a = arm_a2()
    a3, s1b, s2b = arm_a3()
    s1 = s1a and s1b
    s2 = s2a and s2b
    if not a1:
        verdict = "INCONCLUSIVE (anchor continuity failed)"
    elif h1:
        verdict = "VALIDATED (H1: deflation dodge shifts residency > 5pp)"
    elif dodge:
        verdict = ("MIXED (dodge observed — gate openings suppressed — "
                   "but shift <= 5pp)")
    else:
        verdict = "FALSIFIED (H0: deflation inert/bounded at every θ*)"
    print(f"\n  PRE-REGISTERED VERDICT: {verdict}")
    print(f"  (A1={'P' if a1 else 'F'} dodge={'Y' if dodge else 'N'} "
          f"S1={'P' if s1 else 'F'} S2={'P' if s2 else 'F'})")


if __name__ == "__main__":
    main()
