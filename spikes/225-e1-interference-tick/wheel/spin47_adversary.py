#!/usr/bin/env python3
"""SPIN 47, SPOKE 2: ADVERSARY — D5 UNDER COALITION.
Pre-registered docstring, written BEFORE any run. Continuation of
SPIN-35 (single-liar nf adversaries; D5 declared-vs-emitted audit,
0 FP) -> SPIN-37 (mixed twins) -> SPIN-39 (mixed-strategy evasion
FALSIFIED: every lied tick D5-flagged, honest FPR structurally 0).

OPEN QUESTION THIS SPIN ATTACKS:
  D5's zero-miss record (5/5 seeds, 0 false positives) is the
  defense's entire load-bearing wall and has NEVER been attacked
  directly by more than one liar. Two questions:
  (1) COALITION: can two coordinated liars split the lying load so
      each member's per-tick lie attribution stays small enough that
      D5 misses at least one of them in at least one seed, while the
      collective drift injection matches SPIN-39's single-liar rate?
      NOTE on "per-tick lie magnitude under D5's flag threshold":
      in the booked model D5's flag threshold is exactly 0 (any
      declared!=emitted tick flags) and lie magnitude is integer, so
      the minimum splittable magnitude is 1 — there is no sub-
      threshold slot. The coalition therefore splits the load by
      TURNS (who carries the +1 declaration each lied tick), halving
      each member's per-liar miss-rate. The pre-registered question
      is whether that is enough for evasion.
  (2) FP-FLOOD: can a liar emit pulses attributed to HONEST cells'
      ids (fabric-verifiable per-cell audit sees honest ids with
      emissions they never declared) so that D5 FALSE-FLAGS honest
      cells? And does the resulting honest-flag storm erode
      collective residency?

ARMS:
  A  COALITION @ θ*=1.10 on {ladder@15, kcoh5@15} x K in {1,2},
     coalition = twins {4,5}, per-tick audit per-cell (declared
     contribution vs emitted contribution, per cell per tick):
       coal_alt : lie schedule == SPIN-39 nf_inflate (declared =
                  nf+1 iff twin 5 in trig — collective rate matched
                  to the single liar); the false +1 is ATTRIBUTED to
                  coalition members alternating per lied tick.
       coal_tag : same rate; attribution by tick parity (t%2).
       coal_cov : coverage escalation — lie iff ANY coalition member
                  in trig (rate probe above single-liar; attribution
                  alternating). Booked as scaling evidence only.
  B  FP-FLOOD @ θ*=1.10, same 4 cells: twin 5 declares HONESTLY
     (declared = nf) but on every tick it triggers emits one extra
     spoofed pulse (magnitude 1, sign of its own error, K-life)
     under EVERY honest non-triggering cell's id. Per-cell D5 then
     sees honest cells with emitted-but-never-declared pulses.
  C  control: SPIN-39 mixed-twin replay (nf_alt ladder@15 K=2
     @1.10) as anchor-continuity (published -55.8pp).

PRE-REGISTERED DECISION RULE (fixed before running):
  H1 VALIDATED   iff some coalition strategy/cell shifts collective
                 residency >5.0pp vs the gate-off honest null AND,
                 in at least one seed of that cell, NO coalition
                 member is D5-flagged (evasion: harm with zero
                 flagged liars). FALSIFIED if in every seed of every
                 strategy/cell D5 flags >= 1 coalition member.
  H2 VALIDATED   iff fp_flood produces >=1 honest-cell false flag
                 in 5/5 seeds (per-cell D5, honest cells only).
                 FALSIFIED if honest-cell false flags stay 0 in any
                 seed. Residency erosion of the storm is reported
                 as evidence either way (not a gate).
  S1 closure PASS iff |mass - sum|emissions-errors|| < 1 on every
     arm (SPIN-15 identity asserted live in-loop-collected, checked
     per run).
  VERDICT: per-hypothesis VALIDATED/FALSIFIED; INCONCLUSIVE if any
  canary fails or the environment dies.

CANARIES (mandatory, abort on fail):
  Ca: provenance — import/extend spin39_adversary (same dir); honest
      byte-identity vs exp_glm1.run_fabric re-run through spin39's
      run_adv_gate (8 configs).
  Ca2: SPIN-5 anchors digit-exact: zero@15 K1 77.3/8756/187834,
      ladder@15 K1 71.5/5792/106378 (tol ±0.2pp on means).
  Cc1: SPIN-39 mixed-twin replay: nf_alt ladder@15 K=2 @1.10 shift
      -55.8pp vs gate-off null (tol ±0.3pp).
  Cb: gate=never == gate=off full-dict for every new mode (a
      never-open gate cannot see a lie) — coal_alt/tag/cov/fp_flood.
  Cc: double-run determinism (same dict twice, 5 configs).

Config: N=6, ladder@15 [0,3,6,9,12,15] / kcoh5@15 [0,0,0,0,0,15];
pd=3, delta=12, drift=6; ticks 4800; seeds {1,7,42,1999,20260902};
θ*=1.10; integer-only in-loop; floats display-only (spin39 imean
lesson). Run with -u, no pipes.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "inventors-derby"))
sys.path.insert(0, HERE)
from exp_glm1 import run_fabric, within_pm, reality  # noqa: E402
from spin11_adversary import (LCG, SEEDS, DELTA, PD, DRIFT, TICKS,  # noqa: E402
                              ADV, BAND, PEER_BOUND, median, mean)
from spin39_adversary import (LATS, KCOH5, ZERO6, run_adv_gate,  # noqa: E402
                              stats as stats39, row, imean, t100_of)

COAL = (4, 5)                        # coalition twins (5 = SPIN-39's ADV)
COAL_MODES = ("coal_alt", "coal_tag", "coal_cov", "fp_flood")


def run_coal(lats, k, seed, mode=None, gate="off", ticks=TICKS):
    """spin39.run_adv_gate clone, verbatim dynamics, + coalition &
    fp_flood modes + a PER-CELL declared-vs-emitted audit (observer
    only — it never feeds the fabric loop). Per tick per cell:
    declared contribution = 1 if the cell triggered (+1 if the cell
    carried the coalition's false declaration); emitted contribution
    = pulses emitted under that cell's id this tick (spoofed pulses
    count). flag_c[i] += 1 on mismatch. nfmis keeps SPIN-39's global
    declared-vs-emitted-nf counter for continuity. Returns spin39's
    dict + audit sub-dict."""
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
    carrierphase = 0
    tc = t100_of(gate)
    flag_c = [0] * n                    # per-cell D5 flags (per seed)
    lie_c = [0] * n                     # per-cell lie attributions
    honest_fp = [0] * (n - len(COAL))   # honest-cell false-flag ticks

    for t in range(ticks):
        raw = [reality(max(0, t - lats[i])) for i in range(n)]
        reads = list(raw)
        s_true = reality(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > DELTA]

        # ---- gate decision (spin16/39 integer-exact semantics) ----
        nf = len(trig)
        declared = nf
        carrier = -1
        coal_trig = [i for i in COAL if any(j == i for j, _ in trig)]
        if nf and mode in ("coal_alt", "coal_tag", "coal_cov"):
            fire = (mode == "coal_cov" and coal_trig) or \
                   (mode != "coal_cov" and ADV in coal_trig)
            if fire:
                declared = nf + 1
                if mode == "coal_alt":
                    carrier = COAL[carrierphase % 2]
                    carrierphase += 1
                elif mode == "coal_tag":
                    carrier = COAL[t % 2]
                else:
                    carrier = COAL[carrierphase % 2]
                    carrierphase += 1
                lie_c[carrier] += 1
        neff = 1 if nf else 0
        if tc is not None and nf:
            open_ = 100 * abs(PD - declared) > tc * PD
            if open_:
                neff = min(declared, PD)
                gopen += 1
        if declared != nf:
            nfmis += 1     # global D5 (spin39 continuity)

        cflag = 0
        decl_tick = [0] * n
        emit_tick = [0] * n
        for i, e in trig:
            decl_tick[i] = 1
        if carrier >= 0:
            decl_tick[carrier] += 1
        for i, e in trig:
            mass += abs(e)
            paid[i] += abs(e)
            m = abs(e) // PD or 1
            if neff > 1:
                m = m // neff or 1
                gcomp += 1
            pulses.appendleft([m if e > 0 else -m, k])
            events += 1
            emit_tick[i] += 1
            emissions.append((t, i, m if e > 0 else -m, e))
            claim = reads[i]
            peers = [reads[j] for j in range(n) if j != i]
            if not (BAND[0] <= claim <= BAND[1]):
                bandviol += 1
            if abs(claim - median(peers)) > PEER_BOUND:
                peerviol += 1
        # ---- fp_flood: spoofed pulses under honest non-triggering ids
        if mode == "fp_flood" and any(i == ADV for i, _ in trig):
            e5 = [e for i, e in trig if i == ADV][0]
            ms = 1 if e5 > 0 else -1
            for j in range(n):
                if j not in COAL and decl_tick[j] == 0:
                    pulses.appendleft([ms, k])
                    events += 1
                    emit_tick[j] += 1
                    emissions.append((t, j, ms, 0))
        # ---- per-cell D5 audit (observer only) ----
        for i in range(n):
            if decl_tick[i] != emit_tick[i]:
                flag_c[i] += 1
                if i not in COAL:
                    honest_fp[0 if i < COAL[0] else i - len(COAL)] += 1
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

    # SPIN-15 closure identity, asserted live (not just printed)
    assert abs(mass - sum(abs(e) for (_, _, _, e) in emissions)) < 1, \
        f"closure broken seed={seed} mode={mode}"
    d = dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
             settles=settles, resid=resid, cflags=cflags,
             emissions=emissions, audit=None, ticks=ticks,
             gopen=gopen, gcomp=gcomp)
    if mode is not None:
        d["adv"] = dict(paid=paid, unpaid=unpaid, bandviol=bandviol,
                        peerviol=peerviol, deadviol=deadviol,
                        nfmis=nfmis, local_in=local_in, live=n,
                        flag_c=flag_c, lie_c=lie_c, honest_fp=honest_fp)
    return d


def stats47(lats, mode, k, gate):
    rs = [run_coal(lats, k, s, mode=(None if mode == "none" else mode),
                   gate=gate) for s in SEEDS]
    tp = [within_pm(r["resid"], DELTA) for r in rs]
    out = dict(tp=tp, mtp=mean(tp) / 10,
               ev=mean([r["events"] for r in rs]),
               debt=imean([r["mass"] for r in rs]),
               gopen=mean([r["gopen"] for r in rs]),
               rs=rs)
    if mode != "none":
        out["nfmis"] = mean([r["adv"]["nfmis"] for r in rs])
        out["closure"] = imean([r["mass"] - sum(abs(e) for (_, _, _, e)
                                                in r["emissions"])
                                for r in rs])
        out["flags4"] = sum(1 for r in rs if r["adv"]["flag_c"][COAL[0]] > 0)
        out["flags5"] = sum(1 for r in rs if r["adv"]["flag_c"][COAL[1]] > 0)
        out["anyflag"] = sum(1 for r in rs
                             if any(r["adv"]["flag_c"][c] > 0
                                    for c in COAL))
        out["honestfp_seeds"] = sum(1 for r in rs
                                    if sum(r["adv"]["honest_fp"]) > 0)
        out["honestfp_mean"] = mean([sum(r["adv"]["honest_fp"])
                                     for r in rs])
        out["lie4"] = mean([r["adv"]["lie_c"][COAL[0]] for r in rs])
        out["lie5"] = mean([r["adv"]["lie_c"][COAL[1]] for r in rs])
    return out


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY Ca: provenance — spin39.run_adv_gate honest "
          "byte-identity vs exp_glm1.run_fabric (8 configs) ==")
    for lats in (LATS, ZERO6):
        for k in (1, 2):
            for s in (SEEDS[0], SEEDS[-1]):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=s)
                b = run_adv_gate(lats, k, s)
                if {kk: b[kk] for kk in a} != a:
                    ok = False
                    print(f"  MISMATCH lats={lats} K={k} seed={s}")
    print("  Ca: PASS 8/8 (spin39 harness imported & intact)")

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

    print("\n== CANARY Cc1: SPIN-39 mixed-twin replay, nf_alt "
          "ladder@15 K=2 @1.10 ==")
    base = stats39(LATS, "none", 2, "off")
    st = stats39(LATS, "nf_alt", 2, 1.10)
    shift = st["mtp"] - base["mtp"]
    good = abs(shift - (-55.8)) <= 0.3
    ok &= good
    print(f"  shift {shift:+.1f}pp (want -55.8) -> "
          f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY Cb: gate=never == gate=off full-dict, new modes ==")
    okb = True
    for mode in COAL_MODES:
        a = run_coal(LATS, 1, SEEDS[0], mode=mode, gate="off")
        b = run_coal(LATS, 1, SEEDS[0], mode=mode, gate="never")
        if {kk: b[kk] for kk in a} != a:
            okb = False
            print(f"  Cb MISMATCH never-vs-off mode={mode}")
    print(f"  Cb: {'PASS' if okb else 'FAIL'} (all {len(COAL_MODES)} "
          f"new modes)")
    ok &= okb

    print("\n== CANARY Cc: double-run determinism ==")
    okc = True
    for cfg in ((LATS, 1, "coal_alt", 1.10), (KCOH5, 2, "coal_tag", 1.10),
                (LATS, 2, "coal_cov", 1.10), (KCOH5, 1, "fp_flood", 1.10),
                (ZERO6, 1, "none", 1.10)):
        a = run_coal(cfg[0], cfg[1], SEEDS[0], mode=cfg[2], gate=cfg[3])
        b = run_coal(cfg[0], cfg[1], SEEDS[0], mode=cfg[2], gate=cfg[3])
        if a != b:
            okc = False
            print(f"  Cc MISMATCH cfg={cfg}")
    print(f"  Cc: {'PASS' if okc else 'FAIL'} (5 configs)")
    ok &= okc
    print("\nCANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- arms
def arm_a():
    print("\n== ARM A: COALITION @ θ*=1.10 (vs gate-off honest null) ==")
    print("   (honest @1.10 == gate=off by spin39 Cb2; null is exact)")
    h1_valid = False
    s1 = True
    print(row(["mode", "grammar", "K", "mean%", "null%", "shift",
               "gOpen", "lie4/lie5", "flag4/5 seeds", "anyFlag",
               "honestFP", "closureΔ"]))
    for mode in ("coal_alt", "coal_tag", "coal_cov"):
        for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
            for k in (1, 2):
                base = stats47(lats, "none", k, "off")
                st = stats47(lats, mode, k, 1.10)
                shift = st["mtp"] - base["mtp"]
                seeds_noflag = len(SEEDS) - st["anyflag"]
                if abs(shift) > 5.0 and seeds_noflag > 0:
                    h1_valid = True
                s1 &= abs(st["closure"]) < 1
                s1 &= st["honestfp_mean"] == 0
                print(row([mode, gname, k, f"{st['mtp']:.1f}",
                           f"{base['mtp']:.1f}", f"{shift:+.1f}pp",
                           f"{st['gopen']:.0f}",
                           f"{st['lie4']:.0f}/{st['lie5']:.0f}",
                           f"{st['flags4']}/{st['flags5']}",
                           f"{st['anyflag']}/{len(SEEDS)}",
                           f"{st['honestfp_mean']:.0f}",
                           f"{st['closure']:.0f}"]))
    msg = ("VALIDATED" if h1_valid else
           "FALSIFIED (D5 flags >=1 coalition member in every seed "
           "of every strategy)")
    print(f"  H1 (coalition evasion, >5pp with an unflagged seed): {msg}")
    return h1_valid, s1


def arm_b():
    print("\n== ARM B: FP-FLOOD @ θ*=1.10 — spoofed honest-id pulses ==")
    h2_valid = True
    s1 = True
    print(row(["grammar", "K", "mean%", "null%", "shift", "gOpen",
               "global nfMis", "honestFP seeds", "honestFP/seed",
               "closureΔ"]))
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            base = stats47(lats, "none", k, "off")
            st = stats47(lats, "fp_flood", k, 1.10)
            shift = st["mtp"] - base["mtp"]
            h2_valid &= st["honestfp_seeds"] == len(SEEDS)
            s1 &= abs(st["closure"]) < 1
            print(row([gname, k, f"{st['mtp']:.1f}", f"{base['mtp']:.1f}",
                       f"{shift:+.1f}pp", f"{st['gopen']:.0f}",
                       f"{st['nfmis']:.0f}",
                       f"{st['honestfp_seeds']}/{len(SEEDS)}",
                       f"{st['honestfp_mean']:.0f}",
                       f"{st['closure']:.0f}"]))
    # does the flag storm erode residency? printed, not gated
    msg = ("VALIDATED" if h2_valid else
           "FALSIFIED (honest FPR 0 in some seed)")
    print(f"  H2 (>=1 honest-cell false flag in 5/5 seeds): {msg}")
    return h2_valid, s1


def arm_c():
    print("\n== ARM C: control — SPIN-39 mixed-twin replay cells "
          "(anchor-continuity, via spin39 harness) ==")
    s1 = True
    print(row(["mode", "grammar", "K", "mean%", "null%", "shift",
               "nfMis/seed", "closureΔ"]))
    for mode in ("nf_alt", "nf_rnd", "nf_2pd"):
        for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
            for k in (1, 2):
                base = stats39(lats, "none", k, "off")
                st = stats39(lats, mode, k, 1.10)
                shift = st["mtp"] - base["mtp"]
                seeds_lied = sum(1 for r in st["rs"]
                                 if r["adv"]["nfmis"] > 0)
                s1 &= abs(st["closure"]) < 1 and seeds_lied == len(SEEDS)
                print(row([mode, gname, k, f"{st['mtp']:.1f}",
                           f"{base['mtp']:.1f}", f"{shift:+.1f}pp",
                           f"{seeds_lied}/{len(SEEDS)}",
                           f"{st['closure']:.0f}"]))
    return s1


def main():
    print(__doc__)
    print("=" * 70)
    print("SPIN 47 — ADVERSARY — D5 UNDER COALITION — harness run, "
          "-u, no pipes")
    if not canaries():
        print("ABORT: canaries failed — no results collected.")
        sys.exit(1)
    h1, s1a = arm_a()
    h2, s1b = arm_b()
    s1c = arm_c()
    s1 = s1a and s1b and s1c
    print(f"\n  PRE-REGISTERED VERDICT:")
    print(f"    H1 (coalition evasion of D5): "
          f"{'VALIDATED' if h1 else 'FALSIFIED'}")
    print(f"    H2 (FP-flood honest false flags 5/5): "
          f"{'VALIDATED' if h2 else 'FALSIFIED'}")
    print(f"    S1 closure (SPIN-15 live asserts + ledger): "
          f"{'PASS' if s1 else 'FAIL'}")


if __name__ == "__main__":
    main()
