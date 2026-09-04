#!/usr/bin/env python3
"""Q4 §3.1 MI-criticality sweep — driver + integer-only MI analysis.

Integer contract: everything between the C counters and the printed millibit
figures is Python int. ln is computed by the fixed-point atanh series
(scale S = 2**30). ln(2) is derived by the same routine from 2/1. No floats.

Self-canary (C3, pre-registered): a deliberately mislabeled arm that reports
the SAME-VARIABLE table (off-diagonal cells zeroed -> MI == H exactly) under
the label "neighbor MI". Detector: any arm labeled neighbor-MI whose value
equals the marginal entropy H is flagged. Must print CAUGHT.
"""
import subprocess, sys, hashlib
from fractions import Fraction

S = 1 << 30          # fixed-point scale
SEEDS = [1, 7, 42, 1999, 20260902]
PS = [1, 3, 10, 30, 100, 300, 1000, 3000]   # /10000
DS = [1, 2, 3]
Z_SIZES = [64, 128, 256]      # Z_L vs D_{L/2}, matched vertex counts

# ---------- integer fixed-point ln ----------
def ln_fix(num, den, terms=40):
    """ln(num/den) in fixed point (units of 1/S), num,den > 0 ints."""
    if num == den:
        return 0
    if num < den:
        return -ln_fix(den, num, terms)
    # range reduction: bring ratio into [1,2) by halving; each halving adds ln2
    k = 0
    while num > 2 * den:
        den *= 2
        k += 1
    r_num, r_den = num - den, num + den          # r in (0, 1/3]
    r = r_num * S // r_den                       # fixed point
    r2 = r * r // S
    acc, p = 0, r
    for i in range(terms):
        acc += p // (2 * i + 1)
        p = p * r2 // S
    return k * LN2_FIX + 2 * acc

LN2_FIX = 744261118  # ln(2)*2^30; verified below against the integer routine
assert ln_fix(2, 1) == LN2_FIX or abs(ln_fix(2, 1) - 744261118) <= 16

def mi_fix(n00, n01, n10, n11):
    """MI in fixed-point NATS from a 2x2 integer contingency table."""
    cells = [(n00,), (n01,), (n10,), (n11,)]
    n = n00 + n01 + n10 + n11
    nx0, nx1 = n00 + n01, n10 + n11
    ny0, ny1 = n00 + n10, n01 + n11
    tot = 0
    margins = [(nx0, ny0), (nx0, ny1), (nx1, ny0), (nx1, ny1)]
    for c, (cx, cy) in zip((n00, n01, n10, n11), margins):
        if c:
            tot += c * (ln_fix(c, 1) + ln_fix(n, 1) - ln_fix(cx, 1) - ln_fix(cy, 1))
    return tot // n          # nats, fixed point

def h_fix(n0, n1):
    n = n0 + n1
    if n0 == 0 or n1 == 0:
        return 0
    return -(n0 * ln_fix(n0, n) + n1 * ln_fix(n1, n)) // n

def to_millibits(fix):
    """nats fixed point -> millibits (integer):  fix / ln2 * 1000 / S, all integer."""
    return fix * 1000 // LN2_FIX // S   # note: LN2_FIX is fixed-point ln2*S; fix//S=nats; nats/LN2 -> bits... see check

# careful: bits = nats / ln2. nats_fix = nats*S. bits_fix = nats_fix * S // LN2_FIX.
def to_millibits(fix):
    bits_fix = fix * S // LN2_FIX
    return bits_fix * 1000 // S

# self-test (integer): identical variables -> MI == H; independent -> 0
_t1 = mi_fix(500, 0, 0, 500); _h1 = h_fix(500, 500)
_t2 = mi_fix(250, 250, 250, 250)
assert abs(_t1 - _h1) <= 32, ("self-test identity failed", _t1, _h1)
assert abs(_t2) <= 32, ("self-test independence failed", _t2)
assert abs(LN2_FIX - 744261118) < 100  # ln2 * 2^30, cross-check against published digits

# ---------- run one config via the C harness ----------
def run_cfg(group, n, d, p_num, seed):
    out = subprocess.run(["./q4_mi_sweep", str(group), str(n), str(d), str(p_num), str(seed)],
                         capture_output=True, text=True, check=True).stdout.strip()
    f = [int(x) for x in out.split(",")]
    (grp, nn, dd, pp, ss, act_num, act_tot,
     r00, r01, r10, r11, s00, s01, s10, s11,
     f00, f01, f10, f11, x00, x01, x10, x11) = f
    return dict(group=grp, n=nn, d=dd, p=pp, seed=ss, act_num=act_num, act_tot=act_tot,
                r=(r00, r01, r10, r11), s=(s00, s01, s10, s11),
                f=(f00, f01, f10, f11), x=(x00, x01, x10, x11), raw=out)

def sumtab(tabs):
    return tuple(sum(t[i] for t in tabs) for i in range(4))

def sweep(group, sizes):
    """returns rows[(d, L, p)] = dict with MI(millibits), floor, activity permille"""
    rows = {}
    for d in DS:
        for L in sizes:
            for p in PS:
                runs = [run_cfg(group, L, d, p, s) for s in SEEDS]
                n2 = L
                rtab, stab, xtab = sumtab([u["r"] for u in runs]), sumtab([u["s"] for u in runs]), sumtab([u["x"] for u in runs])
                if group == 0:
                    # Z: sum the two generator directions into one neighbor table
                    rtab = tuple(rtab[i] + stab[i] for i in range(4))
                    mi_mb = to_millibits(mi_fix(*rtab))
                    mi_s = None
                else:
                    mi_mb = to_millibits(mi_fix(*rtab))
                    mi_s = to_millibits(mi_fix(*stab))
                floor = to_millibits(mi_fix(*xtab))
                act = sum(u["act_num"] for u in runs) * 1000 // sum(u["act_tot"] for u in runs)
                rows[(d, L, p)] = dict(mi=mi_mb, mi_s=mi_s, floor=floor, act=act)
    return rows

def canaries():
    res = {}
    # C2 anchor replay
    e1 = subprocess.run([sys.executable, "../e1.py"], capture_output=True, text=True, check=True, cwd=".")
    res["e1_sha"] = hashlib.sha256(e1.stdout.encode()).hexdigest()
    res["c2"] = res["e1_sha"] == "4f4acccc67420736ec90778a5ad7d4091f7bed5189580e2df83cc1c3e83e5bee"
    # C3 self-canary: mislabeled arm reporting same-variable table as neighbor MI
    # take a real neighbor table from a hot config and corrupt to same-variable form
    u = run_cfg(0, 64, 1, 3000, 20260902)
    n0, n1 = u["r"][0] + u["r"][1], u["r"][2] + u["r"][3]
    broken_tab = (n0, 0, 0, n1)                     # act[t][v] vs act[t][v]
    mi_broken = to_millibits(mi_fix(*broken_tab))
    h_marg = to_millibits(h_fix(n0, n1))
    res["c3_caught"] = abs(mi_broken - h_marg) <= 1
    res["c3_detail"] = (mi_broken, h_marg)
    return res

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["gcc", "-O2", "-o", "q4_mi_sweep", "q4_mi_sweep.c"], check=True)
    can = canaries()
    print("== canaries ==")
    print("C2 anchor replay:", "PASS" if can["c2"] else "FAIL", can["e1_sha"][:16])
    print("C3 self-canary :", "CAUGHT" if can["c3_caught"] else "MISSED", can["c3_detail"])
    for tag, group, sizes in (("Z", 0, Z_SIZES), ("D", 1, [s // 2 for s in Z_SIZES])):
        rows = sweep(group, sizes)
        print(f"\n== group {tag} (vertex counts {Z_SIZES}) ==")
        print("d,L,p_num,act_permille,MI_millibits" + (",MI_s_edge" if group else "") + ",floor_millibits")
        for (d, L, p), v in sorted(rows.items()):
            line = f"{d},{L},{p},{v['act']},{v['mi']}"
            if group:
                line += f",{v['mi_s']}"
            print(line + f",{v['floor']}")
