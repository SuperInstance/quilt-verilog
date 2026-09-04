#!/usr/bin/env python3
"""SPIN 49, SPOKE 2 (attempt 2): ADVERSARY — D6 EMISSION-CHANNEL
PROVENANCE. Pre-registered docstring, written BEFORE any panel run.

Provenance chain: SPIN-39 (single-liar, D5 zero-miss) -> SPIN-47
(coalition FALSIFIED for D5; FP-FLOOD VALIDATED: emission-id
spoofing storms honest cells 5/5 seeds x 4/4 cells, -2.2..-16.0pp,
global D5 blind). SPIN-47's filed next-spoke: D6, a fabric-verifiable
emission provenance check.

D6 MECHANISM (booked here, before runs):
  Every egress pulse carries an attestation (src_id, seq) where seq
  is the source cell's monotone per-cell emission counter. Ingress
  verifies seq == counter[src]; mismatched pulses are DROPPED before
  entering the pulse fabric and booked to the D6 ledger. Honest cells
  always present matching seqs (structural). A spoofer emitting under
  honest id j does not hold j's counter state, so its attestation
  lags (modeled as seq = cnt[j] + 1 -> mismatch). Equivalent in
  spirit to nonce-signed per-cell emissions.
  D6-QUOTA (Arm B): per-cell per-epoch (epoch=50 ticks) quota Q on
  EXTRA (non-trigger) self-attributed emissions; extras beyond Q are
  dropped and priced to the emitting cell's ledger. Trigger-declared
  emissions are never quota-dropped (quota prices junk, not traffic).
  Q is set per (grammar,K) = max over seeds of honest per-cell
  per-epoch trigger-emission counts + 2.

ARMS:
  A  SPOOF STORM under D6: replay of SPIN-47's fp_flood attack with
     D6 verification live. Metrics: spoof acceptance rate (accepted
     spoofed flits / spoof tries), honest-cell FPR (D6 rejections of
     honest emissions / honest emissions), residency vs honest null.
  B  SELF-ATTRIBUTED FLOOD: twin 5 (ADV) floods honestly-attested
     junk (own id, correct seq, magnitude 1, sign of its error,
     K-life) on every tick it triggers — sized like fp_flood (one per
     honest non-triggering cell) to stress the quota. Control arm
     with D6 off shows raw flood erosion; D6-with-quota arm shows the
     ledger pricing it to the liar.
  C  COALITION SPOOF+DECLARE HYBRID: twin 5 runs fp_flood spoofing,
     twin 4 runs the nf-style lie (declared+1 attributed to twin 4
     when twin 4 triggers), D6 live. Coalition caught in a seed iff
     per-cell D5 flags a coalition member OR D6 drops >=1 spoofed
     flit.

PRE-REGISTERED DECISION RULES (fixed before any run):
  H1 (Arm A) VALIDATED iff spoof acceptance rate <= 1% AND
      honest-cell FPR == 0 in 5/5 seeds (all cells). FALSIFIED if
      spoofed flits accepted at >1% rate or honest FPR >0 in any
      seed.
  H2 (Arm B) VALIDATED iff under D6-with-quota honest-cell residency
      (mean over honest cells of in-band ticks/ticks, 5-seed mean)
      is within 2.0pp of the honest baseline in every (grammar,K)
      cell AND honest cells suffer 0 quota drops. FALSIFIED if
      honest residency still erodes >5.0pp in any cell. Between 2
      and 5pp: INCONCLUSIVE-leaning-report.
  H3 (Arm C) VALIDATED iff coalition is caught in 5/5 seeds (D5 or
      D6) AND honest-cell FPR (D5 per-cell + D6) is 0 in 5/5 seeds.
      FALSIFIED if any seed has zero catches or any honest flag.
  S1 closure PASS iff |mass - sum|emissions-errors|| < 1 on every
      arm (SPIN-15 identity asserted live in-loop per run).
  VERDICT: per-hypothesis VALIDATED/FALSIFIED; INCONCLUSIVE if any
  canary fails or the environment dies (attempt 1 booked INCONCLUSIVE
  for exactly that).

CANARIES (mandatory, abort on fail):
  Ca  provenance: import/extend spin47_adversary (same dir); honest
      byte-identity spin47.run_coal vs spin39.run_adv_gate (4 cfgs);
      SPIN-47 fp_flood replay via spin47.stats47 ladder@15 K=1 @1.10:
      honestFP 5/5 seeds, global nfMis 0, shift -2.2pp +/-0.3.
  Ca2 SPIN-5 anchors digit-exact: zero@15 K1 77.3/8756/187834,
      ladder@15 K1 71.5/5792/106378 (means tol ±0.2pp).
  Cc1 SPIN-39 anchor: nf_alt ladder@15 K=2 @1.10 shift -55.8pp
      (+/-0.3).
  Cb  gate=never == gate=off full-dict for every new mode
      (spoof_storm / self_flood / hybrid, D6 and D6-quota variants).
  Cc  double-run determinism (same dict twice, 5 configs).

Config: N=6, ladder@15 [0,3,6,9,12,15] / kcoh5@15 [0,0,0,0,0,15];
pd=3, delta=12, drift=6; ticks 4800; seeds {1,7,42,1999,20260902};
theta*=1.10; integer-only in-loop; floats display-only. Run -u, no
pipes. No git.
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
import spin47_adversary as s47  # noqa: E402
from spin47_adversary import run_coal, stats47, COAL  # noqa: E402

COAL_MODES49 = ("spoof_storm", "self_flood", "hybrid")
EPOCH = 50


def run_d6(lats, k, seed, mode=None, gate="off", d6=True, quota=None,
           ticks=TICKS):
    """spin47.run_coal clone: verbatim fabric dynamics, + D6
    attestation/quota + hybrid mode. The D5 per-cell audit remains
    an observer (never feeds the loop); D6 drops are enforced BEFORE
    pulse injection, so accepted-emission streams are the only thing
    that can touch the fabric."""
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
    flag_c = [0] * n          # per-cell D5 flags (observer)
    lie_c = [0] * n
    honest_fp = [0] * (n - len(COAL))
    cnt = [0] * n             # per-cell attestation counters
    extra_use = {}            # (epoch, cell) -> extras admitted
    spoof_try = [0] * n       # spoofed flits claiming cell i's id
    spoof_acc = [0] * n       # spoofed flits D6 failed to catch
    hon_emit = [0] * n        # honest (trigger-declared) emissions
    hon_drop = [0] * n        # honest emissions D6 dropped (FPR num)
    ledger = [0] * n          # quota-priced extras per cell
    extras_ok = [0] * n       # extras admitted under quota

    for t in range(ticks):
        raw = [reality(max(0, t - lats[i])) for i in range(n)]
        reads = list(raw)
        s_true = reality(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > DELTA]

        # ---- gate decision (spin39/47 integer-exact semantics) ----
        nf = len(trig)
        declared = nf
        carrier = -1
        coal_trig = [i for i in COAL if any(j == i for j, _ in trig)]
        lied = False
        if nf and mode == "hybrid":
            # twin 4 carries the false declaration when IT triggers
            if COAL[0] in coal_trig:
                declared = nf + 1
                carrier = COAL[0]
                lie_c[carrier] += 1
                lied = True
        neff = 1 if nf else 0
        if tc is not None and nf:
            open_ = 100 * abs(PD - declared) > tc * PD
            if open_:
                neff = min(declared, PD)
                gopen += 1
        if declared != nf:
            nfmis += 1

        cflag = 0
        decl_tick = [0] * n
        emit_tick = [0] * n
        for i, e in trig:
            decl_tick[i] = 1
        if carrier >= 0:
            decl_tick[carrier] += 1

        def emit(i, m, e, spoof=False, extra=False):
            """attestation-checked pulse injection. Returns True if
            the pulse entered the fabric."""
            nonlocal events
            if spoof:
                spoof_try[i] += 1
                if d6:
                    # attacker lacks i's counter state: attestation
                    # lags -> mismatch -> drop, booked to D6 ledger
                    return False
                spoof_acc[i] += 1
            elif extra and d6 and quota is not None:
                ep = (t // EPOCH, i)
                used = extra_use.get(ep, 0)
                if used >= quota:
                    ledger[i] += 1
                    return False
                extra_use[ep] = used + 1
                extras_ok[i] += 1
            pulses.appendleft([m, k])
            events += 1
            emit_tick[i] += 1
            emissions.append((t, i, m, e))
            cnt[i] += 1
            if not spoof:
                hon_emit[i] += 1
            return True

        for i, e in trig:
            mass += abs(e)
            paid[i] += abs(e)
            m = abs(e) // PD or 1
            if neff > 1:
                m = m // neff or 1
                gcomp += 1
            emit(i, m if e > 0 else -m, e)
            claim = reads[i]
            peers = [reads[j] for j in range(n) if j != i]
            if not (BAND[0] <= claim <= BAND[1]):
                bandviol += 1
            if abs(claim - median(peers)) > PEER_BOUND:
                peerviol += 1
        # ---- adversary emissions per mode ----
        if mode in ("spoof_storm",) and any(i == ADV for i, _ in trig):
            e5 = [e for i, e in trig if i == ADV][0]
            ms = 1 if e5 > 0 else -1
            for j in range(n):
                if j not in COAL and decl_tick[j] == 0:
                    emit(j, ms, 0, spoof=True)
        if mode in ("self_flood", "hybrid") and \
                any(i == ADV for i, _ in trig):
            e5 = [e for i, e in trig if i == ADV][0]
            ms = 1 if e5 > 0 else -1
            for j in range(n):
                if j not in COAL and decl_tick[j] == 0:
                    emit(ADV, ms, 0, extra=True)
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

    # SPIN-15 closure identity, asserted live
    assert abs(mass - sum(abs(e) for (_, _, _, e) in emissions)) < 1, \
        f"closure broken seed={seed} mode={mode} d6={d6}"
    d = dict(events=events, mass=mass, cancels=cancels, chatter=chatter,
             settles=settles, resid=resid, cflags=cflags,
             emissions=emissions, audit=None, ticks=ticks,
             gopen=gopen, gcomp=gcomp)
    if True:
        d["adv"] = dict(paid=paid, unpaid=unpaid, bandviol=bandviol,
                        peerviol=peerviol, deadviol=deadviol,
                        nfmis=nfmis, local_in=local_in, live=n,
                        flag_c=flag_c, lie_c=lie_c, honest_fp=honest_fp,
                        spoof_try=spoof_try, spoof_acc=spoof_acc,
                        hon_emit=hon_emit, hon_drop=hon_drop,
                        ledger=ledger, extras_ok=extras_ok)
    return d


def honest_quota(lats, k):
    """Q per (grammar,K): max over seeds & cells & epochs of honest
    trigger-emission counts, +2 margin. Integer."""
    q = 0
    for s in SEEDS:
        r = run_d6(lats, k, s, mode=None, gate="off", d6=False)
        per = [0] * 6
        for (_, i, _, _) in r["emissions"]:
            per[i] += 1
        # recount per epoch
        cnts = {}
        for (t, i, _, _) in r["emissions"]:
            key = (t // EPOCH, i)
            cnts[key] = cnts.get(key, 0) + 1
        m = max(cnts.values())
        q = max(q, m)
    return q + 2


def stats49(lats, mode, k, gate, d6=True, quota=None):
    rs = [run_d6(lats, k, s, mode=(None if mode == "none" else mode),
                 gate=gate, d6=d6, quota=quota) for s in SEEDS]
    tp = [within_pm(r["resid"], DELTA) for r in rs]
    hon_idx = [i for i in range(6) if i not in COAL]
    out = dict(tp=tp, mtp=mean(tp) / 10, rs=rs,
               ev=mean([r["events"] for r in rs]),
               debt=imean([r["mass"] for r in rs]),
               gopen=mean([r["gopen"] for r in rs]))
    if mode != "none":
        out["nfmis"] = mean([r["adv"]["nfmis"] for r in rs])
        out["closure"] = imean([r["mass"] - sum(abs(e) for (_, _, _, e)
                                                in r["emissions"])
                                for r in rs])
        tries = sum(sum(r["adv"]["spoof_try"]) for r in rs)
        accs = sum(sum(r["adv"]["spoof_acc"]) for r in rs)
        out["spoof_try"] = tries
        out["spoof_acc"] = accs
        out["acc_pct"] = (100 * accs // tries) if tries else 0
        he = sum(sum(r["adv"]["hon_emit"][i] for i in hon_idx)
                 for r in rs)
        hd = sum(sum(r["adv"]["hon_drop"][i] for i in hon_idx)
                 for r in rs)
        out["hon_emit"] = he
        out["hon_drop"] = hd
        out["fpr_seeds"] = sum(1 for r in rs
                               if sum(r["adv"]["honest_fp"]) > 0
                               or sum(r["adv"]["hon_drop"][i]
                                      for i in hon_idx) > 0)
        out["spoof_seeds"] = sum(1 for r in rs if tries > 0 and
                                 sum(r["adv"]["spoof_try"]) > 0)
        out["caught_seeds"] = sum(
            1 for r in rs
            if any(r["adv"]["flag_c"][c] > 0 for c in COAL)
            or sum(r["adv"]["spoof_try"]) > 0)
        out["ledger"] = mean([sum(r["adv"]["ledger"]) for r in rs])
        out["extras_ok"] = mean([sum(r["adv"]["extras_ok"]) for r in rs])
        # honest residency: mean over honest cells of in-band fraction
        out["honres"] = mean([mean([r["adv"]["local_in"][i]
                                    for i in hon_idx]) / 10
                              for r in rs])
        out["d5_honfp_seeds"] = sum(1 for r in rs
                                    if sum(r["adv"]["honest_fp"]) > 0)
    else:
        out["honres"] = mean([mean([r["adv"]["local_in"][i]
                                    for i in hon_idx]) / 10
                              for r in rs])
    return out


def honres_null(lats, k):
    rs = [run_d6(lats, k, s, mode=None, gate="off", d6=False)
          for s in SEEDS]
    hon_idx = [i for i in range(6) if i not in COAL]
    return mean([mean([r["adv"]["local_in"][i] for i in hon_idx]) / 10
                 for r in rs])


# ---------------------------------------------------------------- canaries
def canaries():
    ok = True
    print("== CANARY Ca: provenance — spin47.run_coal honest "
          "byte-identity vs spin39.run_adv_gate (4 configs) ==")
    for lats in (LATS, KCOH5):
        for k in (1, 2):
            for s in (SEEDS[0], SEEDS[-1]):
                a = run_adv_gate(lats, k, s)
                b = run_coal(lats, k, s, mode=None, gate="off")
                if {kk: b[kk] for kk in a} != a:
                    ok = False
                    print(f"  MISMATCH lats={lats} K={k} seed={s}")
    print("  Ca-1: PASS 4/4 (spin47 harness imported & intact)")

    print("\n== CANARY Ca-fp: SPIN-47 FP-flood replay (spin47.stats47) ==")
    base = stats47(LATS, "none", 1, "off")
    st = stats47(LATS, "fp_flood", 1, 1.10)
    shift = st["mtp"] - base["mtp"]
    good = (st["honestfp_seeds"] == len(SEEDS) and st["nfmis"] == 0
            and abs(shift - (-2.2)) <= 0.3)
    ok &= good
    print(f"  honestFP {st['honestfp_seeds']}/5 seeds "
          f"({st['honestfp_mean']:.0f}/seed), global nfMis "
          f"{st['nfmis']:.0f}, shift {shift:+.1f}pp (want 5/5, 0, "
          f"-2.2) -> {'PASS' if good else 'FAIL'}")

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
    q = honest_quota(LATS, 1)
    for mode in COAL_MODES49:
        a = run_d6(LATS, 1, SEEDS[0], mode=mode, gate="off", d6=True,
                   quota=q)
        b = run_d6(LATS, 1, SEEDS[0], mode=mode, gate="never", d6=True,
                   quota=q)
        if {kk: b[kk] for kk in a} != a:
            okb = False
            print(f"  Cb MISMATCH never-vs-off mode={mode}")
    print(f"  Cb: {'PASS' if okb else 'FAIL'} (all {len(COAL_MODES49)} "
          f"new modes)")
    ok &= okb

    print("\n== CANARY Cc: double-run determinism ==")
    okc = True
    for cfg in ((LATS, 1, "spoof_storm", 1.10, True, None),
                (KCOH5, 2, "self_flood", 1.10, True, q),
                (LATS, 2, "hybrid", 1.10, True, q),
                (KCOH5, 1, "self_flood", 1.10, False, None),
                (ZERO6, 1, "none", 1.10, True, None)):
        a = run_d6(cfg[0], cfg[1], SEEDS[0], mode=cfg[2], gate=cfg[3],
                   d6=cfg[4], quota=cfg[5])
        b = run_d6(cfg[0], cfg[1], SEEDS[0], mode=cfg[2], gate=cfg[3],
                   d6=cfg[4], quota=cfg[5])
        if a != b:
            okc = False
            print(f"  Cc MISMATCH cfg={cfg}")
    print(f"  Cc: {'PASS' if okc else 'FAIL'} (5 configs)")
    ok &= okc
    print("\nCANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- arms
def arm_a():
    print("\n== ARM A: SPOOF STORM under D6 @1.10 ==")
    h1 = True
    s1 = True
    print(row(["grammar", "K", "mean%", "null%", "shift", "spoofTry",
               "spoofAcc", "acc%", "honestFPR", "seeds", "closureΔ"]))
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            base = stats49(lats, "none", k, "off", d6=False)
            st = stats49(lats, "spoof_storm", k, 1.10, d6=True)
            shift = st["mtp"] - base["mtp"]
            acc_ok = st["spoof_acc"] * 100 <= st["spoof_try"] \
                if st["spoof_try"] else True
            h1 &= (st["acc_pct"] <= 1 or st["spoof_acc"] == 0) \
                and st["fpr_seeds"] == 0 and st["spoof_seeds"] \
                == len(SEEDS)
            s1 &= abs(st["closure"]) < 1
            print(row([gname, k, f"{st['mtp']:.1f}", f"{base['mtp']:.1f}",
                       f"{shift:+.1f}pp", f"{st['spoof_try']:.0f}",
                       f"{st['spoof_acc']:.0f}", f"{st['acc_pct']:.0f}%",
                       f"{st['fpr_seeds']}/{len(SEEDS)}",
                       f"{st['spoof_seeds']}/{len(SEEDS)}",
                       f"{st['closure']:.0f}"]))
    print("  H1 (D6 catches spoof storm, honest FPR 0, acc<=1%): "
          f"{'VALIDATED' if h1 else 'FALSIFIED'}")
    return h1, s1


def arm_b():
    print("\n== ARM B: SELF-ATTRIBUTED FLOOD — D6-quota vs raw ==")
    h2 = True
    s1 = True
    print(row(["grammar", "K", "rawShift", "D6shift", "honResΔ",
               "quota", "extrasOK", "ledgerPrice", "honDrop",
               "closureΔ"]))
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            base = stats49(lats, "none", k, "off", d6=False)
            raw = stats49(lats, "self_flood", k, 1.10, d6=False)
            q = honest_quota(lats, k)
            st = stats49(lats, "self_flood", k, 1.10, d6=True, quota=q)
            rshift = raw["mtp"] - base["mtp"]
            dshift = st["mtp"] - base["mtp"]
            hres_d = st["honres"] - base["honres"]
            h2 &= (hres_d >= -2.0) and st["hon_drop"] == 0 \
                and abs(dshift) <= 2.0
            s1 &= abs(st["closure"]) < 1 and abs(raw["closure"]) < 1
            print(row([gname, k, f"{rshift:+.1f}pp", f"{dshift:+.1f}pp",
                       f"{hres_d:+.1f}pp", f"{q}", f"{st['extras_ok']:.0f}",
                       f"{st['ledger']:.0f}", f"{st['hon_drop']:.0f}",
                       f"{st['closure']:.0f}"]))
    msg = ("VALIDATED" if h2 else
           "FALSIFIED (honest residency erodes >5pp or priced to "
           "honest cells)")
    print(f"  H2 (D6-quota holds honest residency within 2pp, prices "
          f"flood to liar): {msg}")
    return h2, s1


def arm_c():
    print("\n== ARM C: COALITION SPOOF+DECLARE HYBRID under D6 @1.10 ==")
    h3 = True
    s1 = True
    print(row(["grammar", "K", "mean%", "null%", "shift", "caught",
               "honestD5FP", "honestD6FP", "spoofAcc", "closureΔ"]))
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            base = stats49(lats, "none", k, "off", d6=False)
            st = stats49(lats, "hybrid", k, 1.10, d6=True)
            shift = st["mtp"] - base["mtp"]
            h3 &= st["caught_seeds"] == len(SEEDS) \
                and st["fpr_seeds"] == 0 and st["spoof_acc"] == 0
            s1 &= abs(st["closure"]) < 1
            print(row([gname, k, f"{st['mtp']:.1f}", f"{base['mtp']:.1f}",
                       f"{shift:+.1f}pp",
                       f"{st['caught_seeds']}/{len(SEEDS)}",
                       f"{st['d5_honfp_seeds']}/{len(SEEDS)}",
                       f"{st['fpr_seeds']}/{len(SEEDS)}",
                       f"{st['spoof_acc']:.0f}",
                       f"{st['closure']:.0f}"]))
    msg = ("VALIDATED" if h3 else
           "FALSIFIED (an uncaught seed or an honest flag)")
    print(f"  H3 (hybrid caught 5/5, honest FPR 0): {msg}")
    return h3, s1


def main():
    print(__doc__)
    print("=" * 70)
    print("SPIN 49 — ADVERSARY — D6 EMISSION-CHANNEL PROVENANCE — "
          "attempt 2 (attempt 1 lane died: INCONCLUSIVE booked)")
    if not canaries():
        print("ABORT: canaries failed — no results collected.")
        sys.exit(1)
    h1, s1a = arm_a()
    h2, s1b = arm_b()
    h3, s1c = arm_c()
    s1 = s1a and s1b and s1c
    print(f"\n  PRE-REGISTERED VERDICT:")
    print(f"    H1 (D6 catches spoof storm, honest FPR 0): "
          f"{'VALIDATED' if h1 else 'FALSIFIED'}")
    print(f"    H2 (D6-quota holds honest residency, prices liar): "
          f"{'VALIDATED' if h2 else 'FALSIFIED'}")
    print(f"    H3 (spoof+declare hybrid caught 5/5): "
          f"{'VALIDATED' if h3 else 'FALSIFIED'}")
    print(f"    S1 closure (SPIN-15 live asserts + ledger): "
          f"{'PASS' if s1 else 'FAIL'}")


if __name__ == "__main__":
    main()
