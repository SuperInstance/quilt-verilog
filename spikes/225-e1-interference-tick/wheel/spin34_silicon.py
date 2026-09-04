#!/usr/bin/env python3
"""SPIN 34 -- SILICON: minimum-PW sweep. Does SPIN-19's bit-exactness
survive PW < 48?  Pre-registered hypothesis (before any run):
  H1: bounded arms stay full-dict bit-exact down to PW=41; the bound is
      GUARD representability (1e12 needs signed 41 bits), NOT the
      compensated envelope (maxresid ~ 95).
  H2: PW=40 fails (GUARD truncates negative -> spurious guard hit).
  Decision rule: min-PW = smallest PW in {48,46,44,42,41,40} with all
  7 bounded tags x seeds {1,7,42,1999,20260902} full-dict sha256-equal
  to Python. step5_off must stay prefix-bit-exact + div-co-signed for
  every PW where bounded arms pass.
Canaries: kcoh5_gate s1 sha 5621c4c1e813ab32..., byte-frozen gate==off,
step5_gate true12 36.9 (3-seed SPIN-16 anchor), kcoh5 true12 53.0-55.4.
Run: python3 -u spin34_silicon.py > spin34-output.txt (from wheel/)
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # .../wheel
SPIKE = os.path.dirname(HERE)                              # 225-e1-...
ROOT = os.path.dirname(os.path.dirname(SPIKE))              # quilt-verilog
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(SPIKE, "inventors-derby"))
sys.path.insert(0, SPIKE)

from exp_glm1 import within_pm  # noqa: E402
from spin11_pulse_dial import run_fabric_mc  # noqa: E402
from spin16_pulse_dial2 import run_fabric_gate  # noqa: E402

TICKS, EV = 4800, 12
SEEDS = (1, 7, 42, 1999, 20260902)
PWS = (48, 46, 44, 42, 41, 40)
BOUNDED = ("kcoh5_gate", "ladder_gate", "step5_gate", "zero7_gate",
           "kcoh5_off", "kcoh5_mc1", "step5_mc1")
GRAMMARS = {
    "kcoh5":  [0, 0, 0, 0, 0, 30],
    "ladder": [0, 6, 12, 18, 24, 30],
    "step5":  [0, 5, 10, 15, 20, 25, 30],
    "zero7":  [0, 0, 0, 0, 0, 0, 0],
}
OUT = os.path.join(ROOT, "cosim", "out34")


def ref(tag, lats, seed):
    if tag.endswith("_gate"):
        return run_fabric_gate("interference", TICKS, lats, K=1, pd=3,
                               delta=12, drift=6, seed=seed, gate=1.1)
    if tag.endswith("_mc1"):
        return run_fabric_gate("interference", TICKS, lats, K=1, pd=3,
                               delta=12, drift=6, seed=seed, gate="always")
    return run_fabric_mc("interference", TICKS, lats, K=1, pd=3,
                         delta=12, drift=6, seed=seed, mc=0)


def canon(d):
    return {
        "events": d["events"], "mass": d["mass"], "cancels": d["cancels"],
        "chatter": d.get("chatter"), "settles": d.get("settles"),
        "gopen": 0 if d.get("gopen") is None else d["gopen"],
        "gcomp": 0 if d.get("gcomp") is None else d["gcomp"],
        "resid": list(d["resid"]), "cflags": list(d["cflags"]),
        "emissions": [list(e) for e in d["emissions"]],
    }


def hsh(c):
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]


def parse_rtl(path):
    resid, cflags, emissions, fin, ovf_tick = [], [], [], None, None
    with open(path) as f:
        for ln in f:
            p = ln.split()
            if not p:
                continue
            if p[0] == "T":
                resid.append(int(p[2])); cflags.append(int(p[3]))
            elif p[0] == "E":
                emissions.append([int(x) for x in p[1:5]])
            elif p[0] == "X":
                ovf_tick = int(p[1])
            elif p[0] == "F":
                fin = [int(x) for x in p[1:8]]
    if fin is None:
        raise RuntimeError(f"{path}: no F line")
    return {"events": fin[0], "mass": fin[1], "cancels": fin[2],
            "chatter": fin[3], "settles": fin[4], "gopen": fin[5],
            "gcomp": fin[6], "resid": resid, "cflags": cflags,
            "emissions": emissions, "ovf": ovf_tick}


def first_diff(a, b):
    for k in ("events", "mass", "cancels", "chatter", "settles",
              "gopen", "gcomp"):
        if a.get(k) is not None and b.get(k) is not None and a[k] != b[k]:
            return f"counter {k}: py={a[k]} rtl={b[k]}"
    for k in ("resid", "cflags"):
        if len(a[k]) != len(b[k]):
            return f"trace {k} len py={len(a[k])} rtl={len(b[k])}"
        for i, (x, y) in enumerate(zip(a[k], b[k])):
            if x != y:
                return f"{k}@{i}: py={x} rtl={y}"
    if len(a["emissions"]) != len(b["emissions"]):
        return f"emissions py={len(a['emissions'])} rtl={len(b['emissions'])}"
    for i, (x, y) in enumerate(zip(a["emissions"], b["emissions"])):
        if x != y:
            return f"emission {i}: py={x} rtl={y}"
    return None


def prefixify(d, xt):
    """SPIN-19 semantics: pre-X prefix, counters recomputed."""
    em = [e for e in d["emissions"] if e[0] < xt]
    return {"events": len(em), "mass": sum(abs(e[3]) for e in em),
            "cancels": sum(d["cflags"][:xt]), "chatter": None,
            "settles": None, "gopen": None, "gcomp": None,
            "resid": d["resid"][:xt], "cflags": d["cflags"][:xt],
            "emissions": em}


def main():
    print("== SPIN-34 SILICON: minimum-PW sweep (q_wall_gate cosim) ==")
    print("hypothesis H1: bit-exact down to PW=41 (GUARD representability "
          "bound); H2: PW=40 fails (GUARD truncation)")
    refs = {}
    for tag in BOUNDED + ("step5_off",):
        g = tag.rsplit("_", 1)[0]
        refs[tag] = {s: ref(tag, GRAMMARS[g], s) for s in SEEDS}

    # ---- canary 1: published Python anchors (3-seed SPIN-16/19 set)
    print("== canary 1: Python anchors ==")
    ok1 = True
    exp = {1: "5621c4c1e813ab32", 7: "00a23583c03b124d",
           42: "9d4ae35e45b43f37"}
    for s, e in exp.items():
        h = hsh(canon(refs["kcoh5_gate"][s]))
        m = h == e
        ok1 &= m
        print(f"  kcoh5_gate s={s} sha={h} expect={e} {'OK' if m else 'FAIL'}")
    frozen = all(canon(refs["kcoh5_gate"][s]) == canon(refs["kcoh5_off"][s])
                 for s in SEEDS)
    ok1 &= frozen
    print(f"  kcoh5 gate==off byte-frozen (5 seeds): {frozen}")
    t12 = [within_pm(refs["step5_gate"][s]["resid"], EV) / 10
           for s in (1, 7, 42)]
    ok1 &= abs(sum(t12) / 3 - 36.9) < 0.15
    print(f"  step5_gate true12 3-seed mean={sum(t12)/3:.1f} "
          f"(anchor 36.9) vals={[round(x,1) for x in t12]}")
    kt = [within_pm(refs["kcoh5_gate"][s]["resid"], EV) / 10
          for s in (1, 7, 42)]
    ok1 &= kt == [53.0, 55.4, 51.0]
    print(f"  kcoh5 true12 3-seed={[round(x,1) for x in kt]} "
          f"expect [53.0,55.4,51.0] (SPIN-19 out; the 53.0-55.4 quote "
          f"covers s1/s7): {kt == [53.0, 55.4, 51.0]}")
    print(f"  CANARY-1 {'PASS' if ok1 else 'FAIL'}")

    # ---- sweep
    print("== PW sweep (bounded arms, full-dict bit-exact vs Python) ==")
    min_pw = None
    for pw in PWS:
        allok, n_ok, n_tot, fails = True, 0, 0, []
        for tag in BOUNDED:
            for s in SEEDS:
                n_tot += 1
                path = os.path.join(OUT, f"pw{pw}_{tag}_s{s}.txt")
                try:
                    v = parse_rtl(path)
                except Exception as e:  # noqa: BLE001
                    allok = False
                    fails.append(f"{tag}s{s} missing: {e}")
                    continue
                d = first_diff(canon(refs[tag][s]), canon(v))
                if d is None:
                    n_ok += 1
                else:
                    allok = False
                    fails.append(f"{tag}s{s}: {d}")
        print(f"  PW={pw}: {n_ok}/{n_tot} bounded arms bit-exact"
              f"{'  <-- all PASS' if allok else ''}")
        for f_ in fails[:6]:
            print(f"      FAIL {f_}")
        if allok and min_pw is None:
            pass
        if not allok:
            break  # decision rule: first failing PW stops the descent
        min_pw = pw
    print(f"  min-PW (bounded arms, 5 seeds) = {min_pw}")

    # ---- step5_off prefix check at each surviving PW
    print("== step5_off: prefix bit-exactness + divergence co-sign ==")
    if min_pw is not None:
        for pw in [p for p in PWS if p >= min_pw]:
            for s in SEEDS:
                path = os.path.join(OUT, f"pw{pw}_step5_off_s{s}.txt")
                v = parse_rtl(path)
                r = refs["step5_off"][s]
                xt = v["ovf"]
                if xt is None:
                    print(f"  pw={pw} s={s}: NO X LINE (full window?)")
                    continue
                d = first_diff(canon(prefixify(r, xt)),
                               canon(prefixify(v, xt)))
                mr = max(prefixify(r, xt)["resid"])
                print(f"  pw={pw} s={s}: X@{xt} "
                      f"{'PREFIX-MATCH' if d is None else 'PREFIX MISMATCH ' + str(d)}"
                      f" maxresid={mr:.3g}"
                      f"{' cosigned>1e6' if mr > 1e6 else ' NOT cosigned'}")

    # ---- headline stats
    print("== headline ==")
    if min_pw is not None:
        h = hsh(canon(parse_rtl(
            os.path.join(OUT, f"pw{min_pw}_step5_gate_s1.txt"))))
        t = within_pm(parse_rtl(
            os.path.join(OUT, f"pw{min_pw}_step5_gate_s1.txt"))["resid"],
            EV) / 10
        print(f"  PW={min_pw} step5_gate s1: sha={h} true12={t:.1f}")
    verdict = ("VALIDATED" if min_pw == 41 else
               "FALSIFIED" if min_pw is not None else "INCONCLUSIVE")
    print(f"  verdict vs pre-registered H1(min=41): {verdict}")


if __name__ == "__main__":
    main()
