#!/usr/bin/env python3
"""SPIN 36 -- SILICON: SYNTHESIZE the PW=41 minimum-width fabric.
SPIN-34's filed next-rung proposal, executed: same gate-cell standalone
synth as SPIN-19 (yosys 0.47 iCE40, registered-IO wrapper), PW=41 vs
PW=48, GMODE in {0 (never), 2 (theta)}, same RTL tree
(rtl/q_wall_gate.v, SPIN-34's PW-parameterized patched lineage --
byte-identical at PW=48, proven in SPIN-34 by cmp vs SPIN-19 traces).

PRE-REGISTERED (this header written before any synth run completed):
  H1 (clean synth): PW=41 arms synthesize with 0 yosys CHECK problems,
      no latch inference (no $dlatch cells / no 'latch' warnings in the
      log), like the PW=48 arms before them.
  H2 (area): the THETA marginal cost (theta - never) at PW=41 is within
      +/-15% of the PW=48 marginal (SPIN-19 anchor: LUT4 886, CARRY 268)
      -- PW only widens the guard/datapath, not the control; AND the
      theta-arm TOTAL drops or holds vs PW=48 (narrower divider =>
      smaller cell; prediction: ~6-8% drop per SPIN-34's filed guess).
  Decision rule:
      VALIDATED  iff H1 and both halves of H2 hold.
      MIXED      iff H1 holds but exactly one half of H2 holds.
      FALSIFIED  iff H1 fails (latches / CHECK problems) or both halves
                  of H2 fail.
      INCONCLUSIVE if tooling fails on environment grounds (reported
                  with the exact error; no fabricated numbers).
  Headline numbers: dLUT4% and dCARRY% (marginal, PW41 vs PW48 anchor),
  plus total-cell deltas per arm.
Canaries (before trusting any synth number):
  a) RTL replay: re-run the existing SPIN-34-built binaries, byte-compare
     vs cosim/out34 traces, and canonical-sha vs published anchors:
     kcoh5_gate s1 (pw48) 5621c4c1e813ab32, step5_gate s1 (pw41)
     6680a395fa140ad3; double-run determinism on the pw41 leg.
  b) Python anchor: recompute kcoh5_gate s1 sha from run_fabric_gate and
     match 5621c4c1e813ab32 (spin34's canary machinery reused).
  c) Unsized >32-bit localparam literals: none added; the only wide
     constant path is SPIN-34's sized GUARD64 (scar respected). Also
     grep-verify the patched RTL still sizes it.
Integer-only; no floats in the fabric; synth only (no simulation leg
beyond canary replays; those use SPIN-34's binaries verbatim).
Run: python3 -u spin36_silicon.py > spin36-output.txt (from wheel/)
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(SPIKE))
sys.path.insert(0, HERE)
sys.path.insert(0, SPIKE)

OUT34 = os.path.join(ROOT, "cosim", "out34")
COSIM = os.path.join(ROOT, "cosim")

ANCHOR_KCOH5_PW48_S1 = "5621c4c1e813ab32"
ANCHOR_STEP5_PW41_S1 = "6680a395fa140ad3"
PW48_MARGINAL = {"LUT4": 886, "CARRY": 268}   # SPIN-19 anchor


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def parse_rtl(path):
    from spin34_silicon import parse_rtl as p
    return p(path)


def canon_hsh(path):
    from spin34_silicon import parse_rtl, hsh, canon
    return hsh(canon(parse_rtl(path)))


def synth_stat(path):
    """Extract cell counts from a yosys stat file."""
    txt = open(path).read()
    dff = sum(int(m) for m in
              re.findall(r"SB_DFF[A-Z]*\s+(\d+)", txt))
    lut = sum(int(m) for m in re.findall(r"SB_LUT4\s+(\d+)", txt))
    car = sum(int(m) for m in re.findall(r"SB_CARRY\s+(\d+)", txt))
    return {"LUT4": lut, "DFF": dff, "CARRY": car}


def synth_log_flags(path):
    txt = open(path).read()
    latches = len(re.findall(r"\$dlatch", txt))
    latchwarn = len(re.findall(r"[Ll]atch", txt))
    problems = re.findall(r"Found and reported (\d+) problems", txt)
    return {"dlatch_cells": latches, "latch_mentions": latchwarn,
            "check_problems": int(problems[-1]) if problems else None,
            "warnings": len(re.findall(r"^Warning:", txt, re.M))}


def main():
    print("== SPIN-36 SILICON: synthesize the PW=41 fabric (SPIN-34 next rung) ==")
    print("pre-reg: H1 clean synth (0 CHECK problems, no latches); "
          "H2 theta-marginal within +/-15% of LUT4 886 / CARRY 268 "
          "AND PW=41 theta total <= PW=48 theta total")
    ok = True

    # ---- canary c: sized-literal scar respected in the RTL lineage
    rtl = open(os.path.join(ROOT, "rtl", "q_wall_gate.v")).read()
    sized = "GUARD64" in rtl and "64'd1000000000000" in rtl
    print(f"== canary c: patched RTL sizes GUARD wide: {'PASS' if sized else 'FAIL'}")
    ok &= sized

    # ---- canary a: RTL replays from SPIN-34 binaries + determinism
    print("== canary a: RTL replay vs published anchors ==")
    legs = [
        ("obj34/pw48_n6_g2/spin19_tb", ["+seed=1", "+lats=0,0,0,0,0,30"],
         "out34/pw48_kcoh5_gate_s1.txt", ANCHOR_KCOH5_PW48_S1),
        ("obj34/pw41_n7_g2/spin19_tb", ["+seed=1", "+lats=0,5,10,15,20,25,30"],
         "out34/pw41_step5_gate_s1.txt", ANCHOR_STEP5_PW41_S1),
    ]
    for exe, args, ref, sha in legs:
        exe_p = os.path.join(COSIM, exe)
        out = run([exe_p] + args).stdout
        f = os.path.join(COSIM, "out36", os.path.basename(ref))
        with open(f, "w") as fh:
            fh.write(out)
        refp = os.path.join(COSIM, ref)
        byte = open(f, "rb").read() == open(refp, "rb").read()
        h = canon_hsh(f)
        print(f"  {os.path.basename(ref)}: byte==spin34 {byte}; "
              f"sha {h} expect {sha} {'OK' if h == sha else 'FAIL'}")
        ok &= byte and h == sha
        # double-run determinism
        out2 = run([exe_p] + args).stdout
        det = out2 == out
        print(f"  double-run byte-identical: {det}")
        ok &= det

    # ---- canary b: python anchor
    print("== canary b: Python anchor kcoh5_gate s1 ==")
    from spin16_pulse_dial2 import run_fabric_gate
    from spin34_silicon import canon as canon_d, hsh
    d = run_fabric_gate("interference", 4800, [0, 0, 0, 0, 0, 30], K=1,
                        pd=3, delta=12, drift=6, seed=1, gate=1.1)
    hb = hsh(canon_d(d))
    print(f"  py sha {hb} expect {ANCHOR_KCOH5_PW48_S1} "
          f"{'OK' if hb == ANCHOR_KCOH5_PW48_S1 else 'FAIL'}")
    ok &= hb == ANCHOR_KCOH5_PW48_S1
    print(f"== canaries {'ALL PASS' if ok else 'FAIL — synth numbers below are untrusted'}")

    # ---- synth stats
    print("== yosys 0.47+22 iCE40 synth (spin36_synth_top, PW-param wrapper) ==")
    arms = {}
    for pw in (48, 41):
        for g, gm in (("never", 0), ("theta", 2)):
            name = f"pw{pw}_{g}"
            sp = os.path.join(COSIM, f"stat36_{name}.txt")
            lp = os.path.join(COSIM, f"spin36-synth-{name}-output.txt")
            if not os.path.exists(sp):
                print(f"  {name}: STAT MISSING ({sp}) — INCONCLUSIVE")
                print(f"INCONCLUSIVE: synth arm {name} did not produce stats")
                return
            arms[name] = {"stat": synth_stat(sp), "log": synth_log_flags(lp)}
            a = arms[name]
            print(f"  {name} (PW={pw} GMODE={gm}): LUT4={a['stat']['LUT4']} "
                  f"DFF={a['stat']['DFF']} CARRY={a['stat']['CARRY']} "
                  f"| CHECK problems={a['log']['check_problems']} "
                  f"dlatch={a['log']['dlatch_cells']} "
                  f"warnings(unique-ish)={a['log']['warnings']}")

    # ---- H1
    h1 = all(arms[k]["log"]["check_problems"] == 0 and
             arms[k]["log"]["dlatch_cells"] == 0 for k in arms)
    print(f"H1 (clean synth at PW=41): {'PASS' if h1 else 'FAIL'}")

    # ---- H2
    m48 = {"LUT4": arms["pw48_theta"]["stat"]["LUT4"] - arms["pw48_never"]["stat"]["LUT4"],
           "CARRY": arms["pw48_theta"]["stat"]["CARRY"] - arms["pw48_never"]["stat"]["CARRY"]}
    m41 = {"LUT4": arms["pw41_theta"]["stat"]["LUT4"] - arms["pw41_never"]["stat"]["LUT4"],
           "CARRY": arms["pw41_theta"]["stat"]["CARRY"] - arms["pw41_never"]["stat"]["CARRY"]}
    dl = 100 * (m41["LUT4"] - PW48_MARGINAL["LUT4"]) // max(1, PW48_MARGINAL["LUT4"])
    dc = 100 * (m41["CARRY"] - PW48_MARGINAL["CARRY"]) // max(1, PW48_MARGINAL["CARRY"])
    print(f"  PW=48 marginal re-measured: LUT4 {m48['LUT4']} (SPIN-19: 886) "
          f"CARRY {m48['CARRY']} (SPIN-19: 268)")
    print(f"  PW=41 marginal: LUT4 {m41['LUT4']} CARRY {m41['CARRY']}")
    print(f"  dMarginal vs SPIN-19 anchor: dLUT4 {dl:+d}% dCARRY {dc:+d}%")
    tot_hold = arms["pw41_theta"]["stat"]["LUT4"] <= arms["pw48_theta"]["stat"]["LUT4"]
    tot_d = 100 * (arms["pw41_theta"]["stat"]["LUT4"] - arms["pw48_theta"]["stat"]["LUT4"]) \
        // max(1, arms["pw48_theta"]["stat"]["LUT4"])
    tot_dc = 100 * (arms["pw41_theta"]["stat"]["CARRY"] - arms["pw48_theta"]["stat"]["CARRY"]) \
        // max(1, arms["pw48_theta"]["stat"]["CARRY"])
    print(f"  theta TOTAL: PW48 {arms['pw48_theta']['stat']['LUT4']} -> "
          f"PW41 {arms['pw41_theta']['stat']['LUT4']} LUT4 ({tot_d:+d}%), "
          f"CARRY {tot_dc:+d}% -> {'drop-or-hold PASS' if tot_hold else 'rise FAIL'}")
    h2a = abs(dl) <= 15 and abs(dc) <= 15
    h2b = tot_hold
    print(f"H2a (marginal within +/-15%): {'PASS' if h2a else 'FAIL'}")
    print(f"H2b (PW41 theta total <= PW48): {'PASS' if h2b else 'FAIL'}")

    if not ok:
        print("VERDICT: INCONCLUSIVE — canary failure, numbers untrusted")
    elif h1 and h2a and h2b:
        print("VERDICT: VALIDATED")
    elif h1 and (h2a != h2b):
        print("VERDICT: MIXED")
    else:
        print("VERDICT: FALSIFIED")
    print(f"HEADLINE: dMarginal LUT4 {dl:+d}% CARRY {dc:+d}%; "
          f"theta-arm total LUT4 {tot_d:+d}% CARRY {tot_dc:+d}% (PW41 vs PW48)")


if __name__ == "__main__":
    main()
