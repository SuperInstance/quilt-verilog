#!/usr/bin/env python3
"""Q6 Barbieri integer Lyapunov proxy — driver + exact fixed-point fit.
Pre-registration: ROUND-13-Q6-barbieri.md PART 1 (frozen before run).
Integer contract: exponents from exact integer log2 (bit-length + fixed-point
mantissa ln, round-11 ln_fix idiom), reported as reduced Fractions. No floats
in the measurement path.
"""
import subprocess, sys, os, hashlib
from fractions import Fraction

S = 1 << 30
SEEDS = [1, 7, 42, 1999, 20260902]
PS = [3, 30, 300, 3000]
N = 256
T = 1024
GNAMES = {0: "Z", 1: "D", 2: "P"}

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

def log2_fix(x):
    """log2(x)*2^30 for positive integer x, exact integer arithmetic."""
    bl = x.bit_length()
    # mantissa m in [1,2): x = m * 2^(bl-1)
    shift = 30
    m = x << shift >> (bl - 1) if bl - 1 <= shift else x >> (bl - 1 - shift)
    # m in [2^30, 2^31)
    return (bl - 1) * S + ln_fix(m, 1 << 30)

def run(group, n, d, p_num, seed, mode=0, pert=1, t=T):
    out = subprocess.run(["./q6_lyapunov", str(group), str(n), str(d), str(p_num),
                          str(seed), str(mode), str(pert), str(t)],
                         capture_output=True, text=True, check=True).stdout.strip().splitlines()
    series = {}
    for line in out[1:]:
        tt, s1, sup = (int(x) for x in line.split(","))
        series[tt] = (s1, sup)
    return series

def alpha(series, t1=8, t2=128):
    """L1 growth exponent as Fraction (log2 units per tick), or None if floor-hit."""
    s1, s2 = series[t1][0], series[t2][0]
    if s1 <= 0 or s2 <= 0:
        return None  # absorbing annihilation (quantization floor)
    a_fix = (log2_fix(s2) - log2_fix(s1)) * Fraction(1, (t2 - t1))
    return a_fix  # Fraction, value = exponent * 2^30

def cell(group, n, p_num):
    series_list = [run(group, n, 3, p_num, s) for s in SEEDS]
    alphas = [alpha(sr) for sr in series_list]
    floor_hits = sum(1 for a in alphas if a is None)
    vals = [a for a in alphas if a is not None]
    mean = sum(vals) / len(vals) / S if vals else None   # per-tick exponent (float-free Fraction)
    # doubling ratios raw at t=16->32->64
    drs = {s: (series_list[i][16][0], series_list[i][32][0], series_list[i][64][0], series_list[i][128][0])
           for i, s in enumerate(SEEDS)}
    # amplification plateau S_max
    smax = max(max(sr[t][0] for t in sr) for sr in series_list)
    return dict(alphas=alphas, floor_hits=floor_hits, mean=mean, drs=drs, smax=smax,
                series=series_list)

def fmt_frac(fr):
    return f"{fr.numerator}/{fr.denominator} (≈{(float(fr.numerator)/fr.denominator):+.5f})"

def canaries():
    res = {}
    e1 = subprocess.run([sys.executable, "../e1.py"], capture_output=True, text=True, check=True, cwd=".")
    sha = hashlib.sha256(e1.stdout.encode()).hexdigest()
    res["C_c_anchor"] = ("PASS" if sha == "4f4acccc67420736ec90778a5ad7d4091f7bed5189580e2df83cc1c3e83e5bee" else "FAIL", sha[:16])
    # C-a null: identity coin, shared noise -> S==1 forever, alpha==0 exactly
    ok = True
    for g in (0, 1, 2):
        sr = run(g, N, 3, 3000, 7, mode=1, pert=1, t=128)
        if any(v[0] != 1 for v in sr.values()):
            ok = False
    res["C_a_null"] = ("PASS" if ok else "FAIL", "S(t)==1 for all t, all groups")
    # C-b self: no perturbation -> S==0 forever
    ok = True
    for g in (0, 1, 2):
        sr = run(g, N, 3, 3000, 7, mode=0, pert=0, t=128)
        if any(v[0] != 0 for v in sr.values()):
            ok = False
    res["C_b_self"] = ("PASS" if ok else "FAIL", "S(t)==0 for all t, all groups")
    # C-d wiring canary: p=0 pure-ballistic support must equal BFS ball size on the
    # same Cayley graph (independent Python BFS), all three groups, at t=1,2,4,8
    def bfs_ball(group, n, steps):
        n2 = n // 2
        def nb(e, kind):
            if group == 0: return (e + 1) % n if kind == 0 else (e + n - 1) % n
            f, k = divmod(e, n2)
            if kind == 0: return f * n2 + (k + 1) % n2
            if group == 1: return (1 - f) * n2 + (n2 - k) % n2
            return (1 - f) * n2 + k
        ball = {n // 2}
        for _ in range(steps):
            ball = ball | {nb(e, kk) for e in ball for kk in (0, 1)}
        return len(ball)
    ok = True
    for g in (0, 1, 2):
        sr = run(g, N, 3, 0, 1, mode=0, pert=1, t=8)
        for t in (1, 2, 4, 8):
            if sr[t][1] != bfs_ball(g, N, t):
                ok = False
    res["C_d_wiring"] = ("PASS" if ok else "FAIL", "p=0 support == BFS ball size, all groups, t=1/2/4/8")
    return res

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["gcc", "-O2", "-std=c99", "-o", "q6_lyapunov", "q6_lyapunov.c"], check=True)
    print("== canaries ==")
    can = canaries()
    for k, v in can.items():
        print(f"{k}: {v[0]}  {v[1]}")
    print("\n== main grid (N=256, d=3, T=1024, fit t in [8,128]) ==")
    results = {}
    for g in (0, 1, 2):
        for p in PS:
            c = cell(g, N, p)
            results[(g, p)] = c
            per_seed = " ".join("FLOOR" if a is None else f"{float(a / S):+.4f}" for a in c["alphas"])
            mean_s = "FLOOR" if c["mean"] is None else f"{float(c['mean'].numerator/c['mean'].denominator):+.4f}"
            print(f"{GNAMES[g]} p={p:4d}/10^4  alpha_mean={mean_s:>8}  per-seed[{per_seed}]  "
                  f"floor_hits={c['floor_hits']}/5  S_max={c['smax']}")
    print("\n== confirm N=512, p=300 ==")
    for g in (0, 1, 2):
        c = cell(g, 512, 300)
        mean_s = "FLOOR" if c["mean"] is None else f"{float(c['mean'].numerator/c['mean'].denominator):+.4f}"
        print(f"{GNAMES[g]} N=512 alpha_mean={mean_s} floor_hits={c['floor_hits']}/5 S_max={c['smax']}")
    print("\n== confirm N=128, p=300 ==")
    for g in (0, 1, 2):
        c = cell(g, 128, 300)
        mean_s = "FLOOR" if c["mean"] is None else f"{float(c['mean'].numerator/c['mean'].denominator):+.4f}"
        print(f"{GNAMES[g]} N=128 alpha_mean={mean_s} floor_hits={c['floor_hits']}/5 S_max={c['smax']}")
    # raw doubling-ratio dump for one representative cell
    print("\n== raw S1 checkpoints (Z/D/P, p=300, seed 42, t=1..256) ==")
    for g in (0, 1, 2):
        sr = run(g, N, 3, 300, 42, t=256)
        pts = " ".join(f"t{t}:{sr[t][0]}({sr[t][1]})" for t in sorted(sr) if t <= 256)
        print(f"{GNAMES[g]}: {pts}")
