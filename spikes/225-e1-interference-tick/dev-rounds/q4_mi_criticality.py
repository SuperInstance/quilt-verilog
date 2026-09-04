#!/usr/bin/env python3
"""Q4 §3.1 MI-criticality sweep — driver + integer-only MI analysis. FINAL RUN.

Arms:
  v1  q4_mi_sweep.c  — pre-registered model (commit 39e893c). Gain>1 medium.
  v2  q4_mi_sweep2.c — amendment: emitter pays e per neighbor (conservative waves).
  v3  q4_mi_sweep3.c — exploratory probe: emission deadband |a|>=2.

Integer contract: everything between the C counters and the printed millibit
figures is Python int. ln = fixed-point (S=2^30) atanh series with range
reduction; ln(2) derived from 2/1 by the same routine. No floats in the
measurement path (float referee used only in dev self-test, not in results).

Canaries: C2 anchor replay (e1.py byte-identical), C3 self-canary (mislabeled
same-variable arm; must be CAUGHT). C1 byte-identity: run this whole script
twice and compare sha256 (driver-level, done in shell, pre-registered).
"""
import subprocess, sys, hashlib, os

S = 1 << 30
SEEDS = [1, 7, 42, 1999, 20260902]
PS = [1, 3, 10, 30, 100, 300, 1000, 3000]   # /10000
DS = [1, 2, 3]
Z_SIZES = [64, 128, 256]      # Z_L vs D_{L/2}, matched vertex counts

def ln_fix(num, den, terms=40):
    if num == den: return 0
    if num < den: return -ln_fix(den, num, terms)
    k = 0
    while num > 2 * den:
        den *= 2; k += 1
    r = (num - den) * S // (num + den)
    r2 = r * r // S
    acc, p = 0, r
    for i in range(terms):
        acc += p // (2 * i + 1); p = p * r2 // S
    return k * 744261118 + 2 * acc

LN2_FIX = 744261118   # ln(2)*2^30, verified vs integer routine (delta<=16 units)

def mi_fix(n00, n01, n10, n11):
    n = n00 + n01 + n10 + n11
    tot = 0
    for c, cx, cy in ((n00, n00+n01, n00+n10), (n01, n00+n01, n01+n11),
                      (n10, n10+n11, n00+n10), (n11, n10+n11, n01+n11)):
        if c:
            tot += c * (ln_fix(c, 1) + ln_fix(n, 1) - ln_fix(cx, 1) - ln_fix(cy, 1))
    return tot // n

def h_fix(n0, n1):
    n = n0 + n1
    if n0 == 0 or n1 == 0: return 0
    return -(n0 * ln_fix(n0, n) + n1 * ln_fix(n1, n)) // n

def to_millibits(fix):
    return (fix * S // LN2_FIX) * 1000 // S

# dev self-tests (integer only)
_t1, _h1 = mi_fix(500, 0, 0, 500), h_fix(500, 500)
_t2 = mi_fix(250, 250, 250, 250)
assert abs(_t1 - _h1) <= 32 and abs(_t2) <= 32 and abs(ln_fix(2, 1) - LN2_FIX) <= 16

def run_cfg(binary, group, n, d, p_num, seed):
    out = subprocess.run(["./" + binary, str(group), str(n), str(d), str(p_num), str(seed)],
                         capture_output=True, text=True, check=True).stdout.strip()
    f = [int(x) for x in out.split(",")]
    return dict(act_num=f[5], act_tot=f[6],
                r=tuple(f[7:11]), s=tuple(f[11:15]),
                f=tuple(f[15:19]), x=tuple(f[19:23]))

def sumtab(tabs):
    return tuple(sum(t[i] for t in tabs) for i in range(4))

def sweep(binary, group, sizes):
    rows = {}
    for d in DS:
        for L in sizes:
            for p in PS:
                runs = [run_cfg(binary, group, L, d, p, s) for s in SEEDS]
                rtab, stab = sumtab([u["r"] for u in runs]), sumtab([u["s"] for u in runs])
                xtab = sumtab([u["x"] for u in runs])
                ftab = sumtab([u["f"] for u in runs])
                if group == 0:
                    rtab = tuple(rtab[i] + stab[i] for i in range(4))
                    mi_s = None
                else:
                    mi_s = to_millibits(mi_fix(*stab))
                rows[(d, L, p)] = dict(
                    mi=to_millibits(mi_fix(*rtab)), mi_s=mi_s,
                    floor=to_millibits(mi_fix(*xtab)),
                    persist=to_millibits(mi_fix(*ftab)),
                    act=sum(u["act_num"] for u in runs) * 1000 // sum(u["act_tot"] for u in runs))
    return rows

def canaries():
    res = {}
    e1 = subprocess.run([sys.executable, "../e1.py"], capture_output=True, text=True, check=True, cwd=".")
    res["e1_sha"] = hashlib.sha256(e1.stdout.encode()).hexdigest()
    res["c2"] = res["e1_sha"] == "4f4acccc67420736ec90778a5ad7d4091f7bed5189580e2df83cc1c3e83e5bee"
    u = run_cfg("q4_mi_sweep", 0, 64, 1, 3000, 20260902)
    n0, n1 = u["r"][0] + u["r"][1], u["r"][2] + u["r"][3]
    mi_broken = to_millibits(mi_fix(n0, 0, 0, n1))
    h_marg = to_millibits(h_fix(n0, n1))
    res["c3_caught"] = abs(mi_broken - h_marg) <= 1
    res["c3_detail"] = (mi_broken, h_marg)
    return res

ARMS = [("v1", "q4_mi_sweep", 0, Z_SIZES, [s // 2 for s in Z_SIZES]),
        ("v2", "q4_mi_sweep2", 0, Z_SIZES, [s // 2 for s in Z_SIZES]),
        ("v3", "q4_mi_sweep3", 0, Z_SIZES, [s // 2 for s in Z_SIZES])]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    can = canaries()
    print("== canaries ==")
    print("C2 anchor replay:", "PASS" if can["c2"] else "FAIL", can["e1_sha"][:16])
    print("C3 self-canary :", "CAUGHT" if can["c3_caught"] else "MISSED", can["c3_detail"])
    for name, binary, gz, zs, ds_ in ARMS:
        for tag, group, sizes in (("Z", 0, zs), ("D", 1, ds_)):
            rows = sweep(binary, group, sizes)
            print(f"\n== arm {name} group {tag} (vertex counts {sizes if tag=='Z' else zs}) ==")
            print("d,L,p_num,act_permille,MI_millibits" + (",MI_s_edge" if tag == "D" else "") + ",persist_millibits,floor_millibits")
            for (d, L, p), v in sorted(rows.items()):
                line = f"{d},{L},{p},{v['act']},{v['mi']}"
                if tag == "D":
                    line += f",{v['mi_s']}"
                print(line + f",{v['persist']},{v['floor']}")
