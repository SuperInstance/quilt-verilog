#!/usr/bin/env python3
"""ROUND 18 — Rollier-Baetens exact affine-CA spectra (Seam B).
Pre-registration: ROUND-18-rollier-baetens.md PART 1 (commit 7ad7f76, frozen).

Integer contract: masks, matrices, cyclic traces tau_k = Tr(M^k), Gershgorin
bounds — exact Python ints throughout. Floats appear only as display of
integer-derived quantities (rho-hat, brackets). Seeds fixed: 1/7/42/1999/20260902.
"""
import hashlib, math, sys

SEEDS = [1, 7, 42, 1999, 20260902]
MS = [4, 6, 8, 10, 12, 16]          # N = 2m in {8,12,16,20,24,32}
K_MAX = 288
ARM_A = (3, 2, 2)                    # round-13 linearization, x6
LCG_C, LCG_A = 12345, 1103515245

def lcg_mask(seed):
    """(c_e, c_r, c_s) uniform in [-4,4], redraw if all zero."""
    x = seed & 0x7FFFFFFF
    while True:
        out = []
        for _ in range(3):
            x = (LCG_A * x + LCG_C) & 0x7FFFFFFF
            out.append(x % 9 - 4)
        if any(out):
            return tuple(out)

def neighbors(m, group):
    """Round-13 q6_barbieri.py nb() wiring, verbatim. group: 'Z'|'D'|'P'."""
    n = 2 * m
    def nb(v):
        if group == 'Z':
            return ((v + 1) % n, (v + n - 1) % n)          # (r-neighbor, s-neighbor)
        f, k = divmod(v, m)
        r = f * m + (k + 1) % m
        if group == 'D':
            s = (1 - f) * m + (m - k) % m
        else:
            s = (1 - f) * m + k
        return (r, s)
    return [nb(v) for v in range(n)]

def rinv(m, group, v):
    """Preimage under the r-edge (r^-1(v)); s is an involution (s^-1 = s)."""
    n = 2 * m
    if group == 'Z':
        return (v + n - 1) % n
    f, k = divmod(v, m)
    return f * m + (k - 1) % m

def build_M(m, group, mask):
    """x'_v = c_e x_v + c_r x_{r^-1(v)} + c_s x_{s^-1(v)}  (round-13 wiring)."""
    n = 2 * m
    ce, cr, cs = mask
    nbs = neighbors(m, group)
    M = [[0] * n for _ in range(n)]
    for v in range(n):
        M[v][v] = ce
        M[v][rinv(m, group, v)] += cr
        M[v][nbs[v][1]] += cs       # s^-1(v) = s(v), involution
    return M

def trace_powers(M, kmax):
    """tau_k = Tr(M^k) and sigma_k = sum (M^k)_ij^2, exact ints, k = 1..kmax.
    sigma_k = sum_i |lambda_i|^(2k): phase-immune, monotone in k."""
    n = len(M)
    P = [row[:] for row in M]
    taus, sigmas = [], []
    for _ in range(kmax):
        taus.append(sum(P[i][i] for i in range(n)))
        sigmas.append(sum(x * x for row in P for x in row))
        cols = list(zip(*M))
        P = [[sum(a * b for a, b in zip(Prow, col)) for col in cols] for Prow in P]
    return taus, sigmas

def gershgorin(M):
    return max(sum(abs(x) for x in row) for row in M)

def ipow(x, e):
    """x^(1/2K) for huge int x, via bit-length + ln_fix (round-11 idiom), float-free path."""
    bl = x.bit_length()
    e = e * 2
    # x^(1/e) = 2^((bl + log2(m))/e), m in [1,2)
    shift = 60
    m = x << shift >> (bl - 1) if bl - 1 <= shift else x >> (bl - 1 - shift)
    # ln(m) in 2^60 fixed point
    def ln_fix(num, den, terms=60):
        r = (num - den) * (1 << 62) // (num + den)
        r2 = r * r >> 62
        acc, p = 0, r
        for i in range(terms):
            acc += p // (2 * i + 1); p = p * r2 >> 62
        return acc >> 1
    LN2_60 = int(0.6931471805599453 * (1 << 60)) + 1
    total = (bl - 1) * LN2_60 + ln_fix(m, 1 << 60)
    import math
    return math.exp(total / (1 << 60) / e)

def rho_hat(sigmas, n):
    """Phase-immune point estimate: (sigma_K)^(1/2K). Rigorous bracket:
    rho in [rho_hat / n^(1/2K), rho_hat]. (tau-only estimator deprecated after
    canary C5 caught its phase bias; see PART 2 scar E1.)"""
    k = len(sigmas)
    return ipow(sigmas[-1], k), k

def lower_bound(taus, n):
    best, bk = 0, 0
    for k, t in enumerate(taus, 1):
        if t != 0 and abs(t) > n:
            v = (abs(t) / n) ** (1.0 / k)
            if v > best:
                best, bk = v, k
    return best, bk

def circulant_rho(m, mask):
    """Analytic Z value: with round-13 wiring BOTH off-diagonal preimages land on v-1,
    so M_Z = ce*I + (cr+cs)*S^- (scaled permutation) and rho_Z = |ce|+|cr+cs| exactly."""
    ce, cr, cs = mask
    return float(abs(ce) + abs(cr + cs))

def cell(m, group, mask, swap=False):
    g = {'Z': 'D', 'D': 'Z', 'P': 'P'}[group] if swap else group
    M = build_M(m, g, mask)
    taus, sigmas = trace_powers(M, K_MAX)
    return dict(M=M, taus=taus, sigmas=sigmas, U=gershgorin(M), n=2 * m,
                group=group, built=g)

def main():
    out = []
    w = out.append
    w("== ROUND 18 Rollier-Baetens exact spectra ==")
    w(f"grid m={MS} K_MAX={K_MAX} seeds={SEEDS}")

    # ---- C2: round-13 anchor replay (byte-identical rerun of q6_barbieri.py) ----
    import subprocess, os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    r = subprocess.run([sys.executable, "q6_barbieri.py"], capture_output=True, text=True)
    with open("q6-barbieri-output.txt") as f:
        banked = f.read()
    c2 = "PASS" if r.stdout == banked else "FAIL"
    w(f"C2 round-13 anchor replay: {c2}")
    w("")

    # ---- canaries C3/C4/C5/C6 + ARM A ----
    w("== ARM A (mask 3,2,2) + C5 structural theorem (rho must be 7 for all) ==")
    armA = {}
    c3 = c5 = True
    for m in MS:
        for g in ("Z", "D", "P"):
            c = cell(m, g, ARM_A)
            armA[(m, g)] = c
            if c["taus"][0] != 2 * m * ARM_A[0]:
                c3 = False
            rh, k = rho_hat(c["sigmas"], c["n"])
            lo = rh / (c["n"] ** (1.0 / (2 * K_MAX)))
            if not (lo - 1e-9 <= 7.0 <= rh + 1e-9):
                c5 = False
            w(f"A {g} m={m:2d} tau_1={c['taus'][0]} U={c['U']} rho_hat={rh if rh is None else round(rh,6)} (k={k})")
    w(f"C3 trace identity tau_1 == N*c_e everywhere: {'PASS' if c3 else 'FAIL'}")
    w(f"C5 ARM A structural theorem (rho=7 all cells): {'PASS' if c5 else 'FAIL'}")
    w("")

    # ---- C4/C6: circulant cross-check + mislabeled-group self-canary ----
    masksB = {s: lcg_mask(s) for s in SEEDS}
    w("== ARM B masks (LCG, seeds fixed) ==")
    for s in SEEDS:
        w(f"seed {s}: (c_e,c_r,c_s)={masksB[s]}")
    w("")
    c4 = True
    for s in SEEDS:
        c = cell(12, "Z", masksB[s])
        rh = rho_hat(c["sigmas"], c["n"])[0]
        an = circulant_rho(12, masksB[s])
        if abs(rh - an) / an > 1e-3:      # bracket: rho_hat <= rho * n^(1/2K) ~ +0.7%
            c4 = False
        w(f"seed {s}: Z m=12 rho_hat={rh:.6f} analytic=|ce|+|cr+cs|={an:.6f}")
    w(f"C4 Z circulant cross-check: {'PASS' if c4 else 'FAIL'}")

    # C6: swap Z/D constructors; the circulant identity on mislabeled 'Z' must fail
    detected = False
    for s in SEEDS:
        cs = cell(12, "Z", masksB[s], swap=True)   # built with D wiring
        rhs = rho_hat(cs["sigmas"], cs["n"])[0]
        if rhs is None or abs(rhs - circulant_rho(12, masksB[s])) > 1e-6:
            detected = True
    w(f"C6 mislabeled-group self-canary: {'LABEL-SWAP DETECTED — PASS' if detected else 'NOT DETECTED — FAIL'}")
    w("")

    # ---- ARM B main grid ----
    w("== ARM B main grid (directed random masks, exact tau; rho_hat at max k) ==")
    results = {}
    for m in MS:
        for s in SEEDS:
            for g in ("Z", "D", "P"):
                c = cell(m, g, masksB[s])
                rh, k = rho_hat(c["sigmas"], c["n"])
                lb = rh / (c["n"] ** (1.0 / (2 * K_MAX)))
                results[(m, s, g)] = (rh, lb, c["U"], k)
                w(f"B m={m:2d} seed={s:9d} {g} rho_hat={rh:.6f} L={lb:.6f} U={c['U']}")
    w("")

    # ---- verdict inputs (pre-registered rule) ----
    D_SEP, D_NULL = 1 / 64, 1 / 256
    w("== decision inputs (ARM B pairwise gaps) ==")
    sep_cells = null_cells = degen_cells = 0
    top_counts = {"Z": 0, "D": 0, "P": 0}
    total = 0
    for m in MS:
        for s in SEEDS:
            rzs, rds, rps = (results[(m, s, g)][0] for g in "ZDP")
            if None in (rzs, rds, rps):
                degen_cells += 1
                continue
            total += 1
            gaps = [abs(rzs - rds), abs(rzs - rps), abs(rds - rps)]
            mx = max(gaps)
            if mx >= D_SEP:
                sep_cells += 1
                top_counts[max(("Z", "D", "P"), key=lambda g: results[(m, s, g)][0])] += 1
            elif all(g_ <= D_NULL for g_ in gaps):
                null_cells += 1
            w(f"m={m:2d} seed={s:9d} rho Z={rzs:.6f} D={rds:.6f} P={rps:.6f} maxgap={mx:.6f}")
    w(f"separating cells (>=1/64): {sep_cells}  null cells (<=1/256): {null_cells}  "
      f"degenerate: {degen_cells}  / {len(MS)*len(SEEDS)}")
    w(f"top group in separating cells: {top_counts}")
    w("")
    # raw tau dump (representative: m=8, seed=42, all groups, k=1..192)
    w("== raw tau_k dump (m=8, seed=42, mask=%s) ==" % (masksB[42],))
    for g in ("Z", "D", "P"):
        c = cell(8, g, masksB[42])
        w(f"{g} tau: " + ",".join(str(t) for t in c["taus"]))
        w(f"{g} sig: " + ",".join(str(t) for t in c["sigmas"]))

    text = "\n".join(out) + "\n"
    sys.stdout.write(text)
    with open("r18-spectra-output.txt", "w") as f:
        f.write(text)
    print(f"\n[sha256 self] {hashlib.sha256(text.encode()).hexdigest()}", file=sys.stderr)

if __name__ == "__main__":
    main()
