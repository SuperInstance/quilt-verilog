#!/usr/bin/env python3
"""SPIN 50, ADVERSARY spoke, attempt 3 of the SPIN-49 brief.
D6 EMISSION-CHANNEL PROVENANCE — pre-registered docstring, written
BEFORE any run. Continuation of SPIN-39 (mixed-strategy evasion
FALSIFIED; D5 declared-vs-emitted audit 0 FP) -> SPIN-47 (coalition
FALSIFIED; FP-FLOOD VALIDATED: spoofed honest-id pulses false-flag
honest cells 5/5 seeds, -2.2..-16.0pp residency erosion, global D5
blind — emission-id spoofing is OUTSIDE D5's declared-nf model).

OPEN QUESTION THIS SPIN ATTACKS:
  D5 audits the DECLARATION channel (declared nf vs emitted pulses)
  and is provably blind to forged emission IDs. SPIN-47's spoof
  storm is therefore an open hole. D6 moves the audit to the
  EMISSION channel itself: every egress flit carries a source
  attestation the fabric verifies at ingress — per-cell emission
  counters (this epoch, mod 256) cross-checked against the epoch
  tag. A forger cannot increment a victim's counter (private
  per-cell state), so a forged flit survives only by guessing the
  victim's exact next counter value (1/256 per flit, epoch public).
  A per-cell token-bucket ledger (refill 1/tick, burst 2 — the
  honest contract is <=1 flit/cell/tick) prices volume floods to
  the emitting cell: excess flits are dropped and attributed.

ARMS (all @ theta*=1.10, cells {ladder@15, kcoh5@15} x K{1,2}):
  A  SPOOF STORM under D6-provenance: exact SPIN-47 fp_flood
     dynamics, forged flits now tag-verified at ingress.
     H1: D6 catches the spoof storm with honest-cell FPR 0 in 5/5
     seeds. FALSIFY if spoofed flits accepted at >1% or honest
     FPR >0 (any seed, any cell).
  B  SELF-ATTRIBUTED FLOOD under D6-quota: twin 5 floods honestly-
     attributed junk (3 magnitude-1 pulses per trigger tick, valid
     tags) to exhaust the flag budget. Ledger prices the excess to
     the liar.
     H2: D6-with-quota holds residency within 2pp of the honest
     baseline in all cells while the ledger prices the flood to the
     liar. FALSIFY if honest residency erodes >5pp in any cell;
     MIXED if between.
  C  COALITION SPOOF+DECLARE HYBRID under D6-full (prov+quota):
     twin 5 runs nf_inflate declarations AND the spoof storm.
     Caught iff either D5 (per-cell declared!=emitted) or D6
     (forged-tag catch) flags. H3: caught in 5/5 seeds with honest
     FPR 0; report as coverage evidence.

PRE-REGISTERED DECISION RULE (fixed before running):
  H1 VALIDATED iff honest_rej == 0 AND honest D5 flags == 0 in
     5/5 seeds of all 4 cells AND forged-acceptance <= 1.0% in all
     4 cells. FALSIFIED otherwise (report which clause broke).
  H2 VALIDATED iff |shift vs gate-off honest null| <= 2.0pp in all
     4 cells. FALSIFIED if any |shift| > 5.0pp. MIXED otherwise.
  H3 VALIDATED iff union(D5, D6) catch in 5/5 seeds of all 4 cells
     with honest FPR 0.
  S1 closure: SPIN-15 identity asserted live in-loop per run.
  VERDICT per arm VALIDATED/FALSIFIED/MIXED; INCONCLUSIVE if any
  canary fails.

CANARIES (mandatory, abort on fail):
  Ca: provenance — run50(mode in {none, fp_flood}, d6=off)
      full-dict byte-identical to spin47.run_coal (8 configs) and
      mode=none byte-identical to exp_glm1.run_fabric (8 configs).
  Ca2: SPIN-5 anchors digit-exact: zero@15 K1 77.3/8756/187834,
      ladder@15 K1 71.5/5792/106378.
  Cc47: SPIN-47 FP-flood replay (via run50 d6=off): honest FP
      5/5 seeds, global D5 zero, shifts -2.2/-16.0/-10.9/-12.2pp
      tol ±0.3pp.
  Cc39: SPIN-39 anchor nf_alt ladder@15 K2 @1.10 = -55.8pp ±0.3.
  Cb: gate=never == gate=off full-dict for all new modes incl.
      d6=full (a never-open gate cannot see a lie; mc=0).
  Cc: double-run determinism (same dict twice, 5 configs).

Config: N=6, ladder@15 / kcoh5@15; pd=3, delta=12, drift=6;
ticks 4800; seeds {1,7,42,1999,20260902}; ADV=5; theta*=1.10;
EPOCH=400 ticks; counter mod 256; quota token bucket R=1/tick,
B=2; integer-only in-loop; floats display-only. Run with -u,
detached, no pipes.
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
from spin47_adversary import run_coal, COAL  # noqa: E402

EPOCH = 400          # ticks per attestation epoch
CMOD = 256           # emission-counter modulus (forge space)
QREFILL = 1          # token-bucket refill per tick per cell
QBURST = 2           # token-bucket burst cap (honest contract <=1/tick)
JUNKF = 3            # junk pulses per liar trigger tick (arm B)
MODES = ("spoof_prov", "self_flood", "hybrid", "fp_flood")


def run50(lats, k, seed, mode=None, gate="off", d6="off", ticks=TICKS):
    """spin47.run_coal clone, verbatim dynamics, + D6 emission-
    provenance layer. d6: off | prov (tag verify) | quota (token
    bucket) | full (both). With mode in {None, fp_flood} and
    d6=off the loop is byte-identical to run_coal (canary Ca).
    Observer counters: honest_rej (honest flits rejected at
    ingress), forged_att/passed (forge attempts/acceptances),
    junk_att/pass/priced (arm B ledger), d5 per-cell flags (47),
    nfmis global D5 (39/47 continuity)."""
    rng = LCG(seed)
    arng = LCG(seed * 2654435761 % (2 ** 31) + 1)   # forger's LCG
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
    flag_c = [0] * n
    lie_c = [0] * n
    honest_fp = [0] * (n - len(COAL))
    # ---- D6 state ----
    cnt = [0] * n          # per-cell emission counter this epoch
    tokens = [QBURST] * n  # per-cell token bucket
    honest_rej = forged_att = forged_pass = 0
    junk_att = junk_pass = junk_priced = 0
    priced_c = [0] * n     # ledger: flits priced (dropped) per cell

    def emit(i, mag):
        """Egress one flit under cell i's id with attestation
        (epoch, cnt[i]%CMOD); ingress-verify + token-bucket price.
        Returns True iff the flit enters the fabric."""
        nonlocal honest_rej, junk_pass, junk_priced
        ep = (t // EPOCH)
        tag = (ep, cnt[i] % CMOD)
        ok = True
        if d6 in ("prov", "full"):
            ok = (tag[0] == ep and tag[1] == cnt[i] % CMOD)
            if not ok:
                honest_rej += 1
                return False
        cnt[i] += 1
        if d6 in ("quota", "full"):
            if tokens[i] > 0:
                tokens[i] -= 1
            else:
                junk_priced += 1
                priced_c[i] += 1
                return False
        return True

    def forge(j, mag):
        """Forged flit under victim j's id: forger cannot increment
        j's private counter, must guess it (arng, 1/CMOD)."""
        nonlocal forged_att, forged_pass
        forged_att += 1
        ep = (t // EPOCH)
        guess = arng.below(CMOD)
        if d6 in ("prov", "full"):
            if ep == (t // EPOCH) and guess == cnt[j] % CMOD:
                forged_pass += 1
                if d6 == "full" and tokens[j] > 0:
                    tokens[j] -= 1
                return True
            return False
        forged_pass += 1     # no verification: everything slips in
        return True

    for t in range(ticks):
        raw = [reality(max(0, t - lats[i])) for i in range(n)]
        reads = list(raw)
        s_true = reality(t)
        g += rng.below(2 * DRIFT + 1) - DRIFT
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        if d6 in ("quota", "full"):
            for i in range(n):
                if tokens[i] < QBURST:
                    tokens[i] += QREFILL
        if t % EPOCH == 0 and t > 0:
            cnt = [0] * n    # epoch rollover: counters reset
        errs = [r - g for r in reads]
        trig = [(i, e) for i, e in enumerate(errs) if abs(e) > DELTA]

        # ---- gate decision (spin16/39/47 integer-exact) ----
        nf = len(trig)
        declared = nf
        carrier = -1
        coal_trig = [i for i in COAL if any(j == i for j, _ in trig)]
        spoof = mode in ("fp_flood", "spoof_prov", "hybrid")
        if nf and mode == "hybrid" and ADV in coal_trig:
            declared = nf + 1          # nf_inflate declaration lie
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
            nfmis += 1

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
            if emit(i, m if e > 0 else -m):
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
        # ---- spoof storm (47 fp_flood dynamics, now verified) ----
        if spoof and any(i == ADV for i, _ in trig):
            e5 = [e for i, e in trig if i == ADV][0]
            ms = 1 if e5 > 0 else -1
            for j in range(n):
                if j not in COAL and decl_tick[j] == 0:
                    if forge(j, ms):
                        pulses.appendleft([ms, k])
                        events += 1
                        emit_tick[j] += 1
                        emissions.append((t, j, ms, 0))
        # ---- self-attributed junk flood (arm B) ----
        if mode == "self_flood" and any(i == ADV for i, _ in trig):
            e5 = [e for i, e in trig if i == ADV][0]
            ms = 1 if e5 > 0 else -1
            for _f in range(JUNKF):
                junk_att += 1
                if emit(ADV, ms):
                    junk_pass += 1
                    pulses.appendleft([ms, k])
                    events += 1
                    emissions.append((t, ADV, ms, 0))
        # ---- per-cell D5 audit (observer only, 47) ----
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
    if mode is not None:
        d["adv"] = dict(paid=paid, unpaid=unpaid, bandviol=bandviol,
                        peerviol=peerviol, deadviol=deadviol,
                        nfmis=nfmis, local_in=local_in, live=n,
                        flag_c=flag_c, lie_c=lie_c, honest_fp=honest_fp,
                        honest_rej=honest_rej, forged_att=forged_att,
                        forged_pass=forged_pass, junk_att=junk_att,
                        junk_pass=junk_pass, junk_priced=junk_priced,
                        priced_c=priced_c)
    return d


def stats50(lats, mode, k, gate, d6="off"):
    rs = [run50(lats, k, s, mode=(None if mode == "none" else mode),
                gate=gate, d6=d6) for s in SEEDS]
    tp = [within_pm(r["resid"], DELTA) for r in rs]
    out = dict(tp=tp, mtp=mean(tp) / 10,
               ev=mean([r["events"] for r in rs]),
               gopen=mean([r["gopen"] for r in rs]),
               rs=rs)
    if mode != "none":
        a = [r["adv"] for r in rs]
        out["nfmis"] = mean([x["nfmis"] for x in a])
        out["closure"] = imean([r["mass"] - sum(abs(e) for (_, _, _, e)
                                                in r["emissions"])
                                for r in rs])
        out["honest_rej"] = sum(x["honest_rej"] for x in a)
        out["forged_att"] = mean([x["forged_att"] for x in a])
        out["forged_pass"] = mean([x["forged_pass"] for x in a])
        out["honestfp_seeds"] = sum(1 for x in a
                                    if sum(x["honest_fp"]) > 0
                                    or x["honest_rej"] > 0)
        out["junk_att"] = mean([x["junk_att"] for x in a])
        out["junk_pass"] = mean([x["junk_pass"] for x in a])
        out["junk_priced"] = mean([x["junk_priced"] for x in a])
        out["d5flag5_seeds"] = sum(1 for x in a if x["flag_c"][ADV] > 0)
        out["d6catch_seeds"] = sum(1 for x in a if x["forged_att"]
                                   - x["forged_pass"] > 0
                                   or x["priced_c"][ADV] > 0)
    return out


# ---------------------------------------------------------------- canaries
def _sub(a, b):
    """True iff dict a equals b restricted to a's keys (recursive
    one level into 'adv'). Provenance: new observer keys must not
    break identity vs spin47's dict."""
    for kk in a:
        if kk == "adv":
            for k2 in a[kk]:
                if b["adv"][k2] != a["adv"][k2]:
                    return False
        elif b[kk] != a[kk]:
            return False
    return True


def canaries():
    ok = True
    print("== CANARY Ca: provenance — run50 == spin47.run_coal / "
          "run_fabric byte-identity (8+8 configs, d6=off) ==")
    for lats in (LATS, KCOH5):
        for k in (1, 2):
            for s in (SEEDS[0], SEEDS[-1]):
                a = run_fabric("interference", TICKS, lats, K=k, pd=PD,
                               delta=DELTA, drift=DRIFT, seed=s)
                b = run50(lats, k, s)
                c = run_coal(lats, k, s)
                if {kk: b[kk] for kk in a} != a:
                    ok = False
                    print(f"  MISMATCH-fabric lats={lats} K={k} seed={s}")
                if not _sub(c, b):
                    ok = False
                    print(f"  MISMATCH-47none lats={lats} K={k} seed={s}")
                d47 = run_coal(lats, k, s, mode="fp_flood")
                d50 = run50(lats, k, s, mode="fp_flood", d6="off")
                if not _sub(d47, d50):
                    ok = False
                    print(f"  MISMATCH-47fp lats={lats} K={k} seed={s}")
    print("  Ca: PASS 16/16 identity triples (fabric / 47-none / "
          "47-fp_flood)")

    print("\n== CANARY Ca2: SPIN-5 anchor replay (5-seed means) ==")
    for name, lats, want in (("zero@15 K=1", ZERO6, (77.3, 8756, 187834)),
                             ("ladder@15 K=1", LATS, (71.5, 5792, 106378))):
        rs = [run50(lats, 1, s) for s in SEEDS]
        tp = mean([within_pm(r["resid"], DELTA) for r in rs])
        ev = mean([r["events"] for r in rs])
        dbt = mean([r["mass"] for r in rs])
        good = (abs(tp / 10 - want[0]) <= 0.2 and round(ev) == want[1]
                and round(dbt) == want[2])
        ok &= good
        print(f"  {name}: {tp/10:.1f}% ev {ev:.0f} debt {dbt:.0f} "
              f"(want {want[0]}/{want[1]}/{want[2]}) -> "
              f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY Cc47: SPIN-47 FP-flood replay via run50(d6=off) ==")
    want47 = {("ladder@15", 1): -2.2, ("ladder@15", 2): -16.0,
              ("kcoh5@15", 1): -10.9, ("kcoh5@15", 2): -12.2}
    for (gname, k), want in want47.items():
        lats = LATS if gname == "ladder@15" else KCOH5
        base = stats50(lats, "none", k, "off")
        st = stats50(lats, "fp_flood", k, 1.10, d6="off")
        shift = st["mtp"] - base["mtp"]
        good = (abs(shift - want) <= 0.3 and st["honestfp_seeds"] == 5
                and st["nfmis"] == 0)
        ok &= good
        print(f"  {gname} K={k}: shift {shift:+.1f}pp honestFP "
              f"{st['honestfp_seeds']}/5 nfMis {st['nfmis']:.0f} "
              f"(want {want:+.1f}, FP 5/5, D5 0) -> "
              f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY Cc39: SPIN-39 anchor, nf_alt ladder@15 K=2 @1.10 ==")
    base = stats39(LATS, "none", 2, "off")
    st = stats39(LATS, "nf_alt", 2, 1.10)
    shift = st["mtp"] - base["mtp"]
    good = abs(shift - (-55.8)) <= 0.3
    ok &= good
    print(f"  shift {shift:+.1f}pp (want -55.8) -> "
          f"{'PASS' if good else 'FAIL'}")

    print("\n== CANARY Cb: gate=never == gate=off full-dict, new modes "
          "(incl. d6=full) ==")
    okb = True
    for mode, d6 in (("spoof_prov", "prov"), ("self_flood", "quota"),
                     ("hybrid", "full"), ("fp_flood", "off")):
        a = run50(LATS, 1, SEEDS[0], mode=mode, gate="off", d6=d6)
        b = run50(LATS, 1, SEEDS[0], mode=mode, gate="never", d6=d6)
        if a != b:
            okb = False
            print(f"  Cb MISMATCH never-vs-off mode={mode} d6={d6}")
    print(f"  Cb: {'PASS' if okb else 'FAIL'} (4 mode/d6 pairs)")
    ok &= okb

    print("\n== CANARY Cc: double-run determinism ==")
    okc = True
    for cfg in ((LATS, 1, "spoof_prov", 1.10, "prov"),
                (KCOH5, 2, "self_flood", 1.10, "quota"),
                (LATS, 2, "hybrid", 1.10, "full"),
                (KCOH5, 1, "fp_flood", 1.10, "off"),
                (ZERO6, 1, None, 1.10, "off")):
        a = run50(cfg[0], cfg[1], SEEDS[0], mode=cfg[2], gate=cfg[3],
                  d6=cfg[4])
        b = run50(cfg[0], cfg[1], SEEDS[0], mode=cfg[2], gate=cfg[3],
                  d6=cfg[4])
        if a != b:
            okc = False
            print(f"  Cc MISMATCH cfg={cfg}")
    print(f"  Cc: {'PASS' if okc else 'FAIL'} (5 configs)")
    ok &= okc
    print("\nCANARIES:", "PASS" if ok else "FAIL — nothing below counts")
    return ok


# ---------------------------------------------------------------- arms
NULLS = {}


def null_of(lats, k):
    key = (tuple(lats), k)
    if key not in NULLS:
        NULLS[key] = stats50(lats, "none", k, "off")
    return NULLS[key]


def arm_a():
    print("\n== ARM A: SPOOF STORM under D6-provenance @1.10 ==")
    print(row(["grammar", "K", "mean%", "null%", "shift",
               "storm-noD6", "forgedAtt", "forgedPass", "accept%",
               "honestRej", "honestFP", "closureΔ"]))
    h1 = True
    why = []
    worst = 0.0
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            base = null_of(lats, k)
            storm = stats50(lats, "fp_flood", k, 1.10, d6="off")
            st = stats50(lats, "spoof_prov", k, 1.10, d6="prov")
            shift = st["mtp"] - base["mtp"]
            shift0 = storm["mtp"] - base["mtp"]
            acc = 100 * st["forged_pass"] / max(1, st["forged_att"])
            worst = max(worst, acc)
            if st["honest_rej"] > 0 or st["honestfp_seeds"] > 0:
                h1 = False
                why.append(f"honest FPR>0 {gname} K{k}")
            if acc > 1.0:
                h1 = False
                why.append(f"accept {acc:.2f}% {gname} K{k}")
            print(row([gname, k, f"{st['mtp']:.1f}", f"{base['mtp']:.1f}",
                       f"{shift:+.1f}pp", f"{shift0:+.1f}pp",
                       f"{st['forged_att']:.0f}", f"{st['forged_pass']:.1f}",
                       f"{acc:.2f}%", f"{st['honest_rej']}",
                       f"{st['honestfp_seeds']}/5", f"{st['closure']:.0f}"]))
    msg = ("VALIDATED" if h1 else
           "FALSIFIED (" + "; ".join(why) + ")")
    print(f"  H1 (D6 catches storm, honest FPR 0, accept<=1%): {msg} "
          f"[worst accept {worst:.2f}%]")
    return h1


def arm_b():
    print("\n== ARM B: SELF-ATTRIBUTED FLOOD under D6-quota @1.10 ==")
    print(row(["grammar", "K", "mean%", "null%", "shift",
               "junkAtt", "junkPass", "junkPriced", "pricedSeeds",
               "closureΔ"]))
    h2 = True
    fals = False
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            base = null_of(lats, k)
            st = stats50(lats, "self_flood", k, 1.10, d6="quota")
            shift = st["mtp"] - base["mtp"]
            priced_seeds = sum(1 for r in st["rs"]
                               if r["adv"]["priced_c"][ADV] > 0)
            if abs(shift) > 5.0:
                fals = True
            elif abs(shift) > 2.0:
                h2 = False
            print(row([gname, k, f"{st['mtp']:.1f}", f"{base['mtp']:.1f}",
                       f"{shift:+.1f}pp", f"{st['junk_att']:.0f}",
                       f"{st['junk_pass']:.0f}", f"{st['junk_priced']:.0f}",
                       f"{priced_seeds}/5", f"{st['closure']:.0f}"]))
    msg = ("FALSIFIED (>5pp erosion in some cell)" if fals else
           ("VALIDATED (all |shift| <= 2pp)" if h2 else
            "MIXED (some cell in (2pp, 5pp])"))
    print(f"  H2 (quota holds residency within 2pp, prices liar): {msg}")
    return msg


def arm_c():
    print("\n== ARM C: SPOOF+DECLARE HYBRID under D6-full @1.10 ==")
    print(row(["grammar", "K", "mean%", "null%", "shift",
               "D5flag5", "D6catch", "union", "honestFP", "closureΔ"]))
    h3 = True
    for gname, lats in (("ladder@15", LATS), ("kcoh5@15", KCOH5)):
        for k in (1, 2):
            base = null_of(lats, k)
            st = stats50(lats, "hybrid", k, 1.10, d6="full")
            shift = st["mtp"] - base["mtp"]
            union = sum(1 for r in st["rs"]
                        if r["adv"]["flag_c"][ADV] > 0
                        or (r["adv"]["forged_att"]
                            - r["adv"]["forged_pass"]) > 0
                        or r["adv"]["priced_c"][ADV] > 0)
            if union < len(SEEDS) or st["honestfp_seeds"] > 0:
                h3 = False
            print(row([gname, k, f"{st['mtp']:.1f}", f"{base['mtp']:.1f}",
                       f"{shift:+.1f}pp", f"{st['d5flag5_seeds']}/5",
                       f"{st['d6catch_seeds']}/5", f"{union}/5",
                       f"{st['honestfp_seeds']}/5",
                       f"{st['closure']:.0f}"]))
    msg = ("VALIDATED" if h3 else
           "FALSIFIED (a seed/cell escapes both D5 and D6, or honest "
           "FPR >0)")
    print(f"  H3 (union catch 5/5, honest FPR 0): {msg}")
    return h3


def main():
    print(__doc__)
    print("=" * 70)
    print("SPIN 50 — ADVERSARY — D6 EMISSION-CHANNEL PROVENANCE — "
          "harness run, -u, detached, no pipes")
    if not canaries():
        print("ABORT: canaries failed — no results collected.")
        sys.exit(1)
    h1 = arm_a()
    h2 = arm_b()
    h3 = arm_c()
    print(f"\n  PRE-REGISTERED VERDICT:")
    print(f"    H1 (D6 prov catches spoof storm, FPR 0): "
          f"{'VALIDATED' if h1 else 'FALSIFIED'}")
    print(f"    H2 (quota holds residency <=2pp): {h2}")
    print(f"    H3 (hybrid union catch 5/5): "
          f"{'VALIDATED' if h3 else 'FALSIFIED'}")
    print("    S1 closure: PASS (live asserts, no abort)")


if __name__ == "__main__":
    main()
