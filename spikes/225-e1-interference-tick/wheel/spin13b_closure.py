#!/usr/bin/env python3
"""
SPIN-13b SNAP-SHADOW ADDENDUM — BISECTION-COMBINATION CLOSURE (Casey):
"snapped angles themselves can be bisected and combined for a plethora of
absolute precision with a finite number of bits to explain, each optimizable
for a situation depending on what they are relative to."

Seeds = budget-16 (norm^2<=16) shadow direction sets from SPIN-13
(Eisenstein-2D, and Z^d->shadow projections d=4/6/8 seed 1, same fixed
matrices). Closure ops, all integer-only with lattice renormalization
(primitive reduction), no trig in the core:

  BIS_N  naive bisection      : (u,v) -> prim(u + v)
  BIS_B  balanced bisection   : (u,v) -> prim(l*u + m*v), l,m in [1..12]
                                chosen so l^2*|u|^2 ~ m^2*|v|^2 (EXACT integer
                                norm comparison; true arc-midpoint balancing)
  COMB   integer combination  : (u,v) -> prim(a*u + b*v),
                                (a,b) in {(1,1),(1,2),(2,1),(2,2),(1,-1),(-1,1)}

Every derived direction is addressed by a finite bit-string (op tree):
  base:  ceil(log2(|S0|)) bits
  op :   2 tag bits + 2*ceil(log2(pool)) parent bits (+3 coef bits for COMB)

Measurements:
  (1) PLETHORA: distinct exact angles per closure depth vs bits spent.
  (2) PRECISION LADDER: min/median gap vs depth (2^-depth hypothesis).
  (3) BITS-TO-PRECISION: 32 golden targets x tolerance ladder; minimal
      bit-string hitting tolerance; op-type of the winner (context
      optimality: bisection vs combination per tolerance regime), compared
      against RAW budget-growth arms (no closure) at equal address bits.
Canaries: exact 30-degree bisection bisB((2,0),(1,1))==(3,1); idempotence
bisN(u,u)==u; u,(-u) ops rejected; eis seed set == independent direct
enumeration; full double-run byte identity; fixed LCG pair sampling.
"""
import bisect
import math
from math import atan2, degrees, sqrt

SQRT3 = sqrt(3.0)
B_ENTRIES = 3
PRE_BUDGET_SQ = 16
DEPTHS = 3
PAIRS_PER_DEPTH = 12000
BIS_BOUND = 12
PHI = (sqrt(5.0) - 1.0) / 2.0
TARGETS = [(360.0 * (i + 1) * PHI) % 360.0 for i in range(32)]
TOLS = (10.0, 3.0, 1.0, 0.3, 0.1, 0.03, 0.01, 0.003)

# deterministic LCG for pair sampling
_LCG_X = [12345]


def lcg(n):
    out = []
    for _ in range(n):
        _LCG_X[0] = (1664525 * _LCG_X[0] + 1013904223) % 2147483648
        out.append(_LCG_X[0])
    return out


def igcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def dir_key(X, Y):
    if X == 0 and Y == 0:
        return None
    g = igcd(abs(X), abs(Y))
    return (X // g, Y // g)


def angle_deg(key):
    X, Y = key
    return degrees(atan2(Y * SQRT3, X)) % 360.0


def angdist(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def norm2(X, Y):
    return X * X + 3 * Y * Y


# -------- enumeration & projections (verbatim from SPIN-13) --------
def enum_ball_sq(d, r2max):
    pts = []

    def rec(pref, i, n2):
        if i == d:
            if n2 > 0:
                pts.append((n2, pref))
            return
        rec(pref + (0,), i + 1, n2)
        v = 1
        while n2 + v * v <= r2max:
            nv = n2 + v * v
            rec(pref + (v,), i + 1, nv)
            rec(pref + (-v,), i + 1, nv)
            v += 1

    rec((), 0, 0)
    pts.sort()
    return pts


def enum_ball_eis(r2max):
    pts = []
    R = math.isqrt(r2max) + 2
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            n2 = a * a + a * b + b * b
            if 0 < n2 <= r2max:
                pts.append((n2, (a, b)))
    pts.sort()
    return pts


def proj_matrix(d, seed):
    if d == 2:
        return (2, 1), (0, 1)
    rnd = __import__("random").Random(9173 * seed + d)
    while True:
        mx = tuple(rnd.randint(-B_ENTRIES, B_ENTRIES) for _ in range(d))
        my = tuple(rnd.randint(-B_ENTRIES, B_ENTRIES) for _ in range(d))
        g = 0
        for x in mx + my:
            g = igcd(g, x)
        if g != 1:
            continue
        g2 = 0
        for i in range(d):
            for j in range(i + 1, d):
                g2 = igcd(g2, mx[i] * my[j] - mx[j] * my[i])
        if g2 == 1:
            return mx, my


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def seed_dirs(d, seed, r2max):
    mx, my = proj_matrix(d, seed)
    pts = enum_ball_eis(r2max) if d == 2 else enum_ball_sq(d, r2max)
    dirs = set()
    for _n2, z in pts:
        k = dir_key(dot(mx, z), dot(my, z))
        if k is not None:
            dirs.add(k)
    return dirs


# -------- closure ops (integer-only) --------
def op_bis_n(u, v):
    return dir_key(u[0] + v[0], u[1] + v[1])


def op_bis_b(u, v):
    n1 = norm2(*u)
    n2 = norm2(*v)
    best = None
    for lam in range(1, BIS_BOUND + 1):
        for mu in range(1, BIS_BOUND + 1):
            d = lam * lam * n1 - mu * mu * n2
            ad = d if d >= 0 else -d
            if ad == 0:
                best = (0, lam, mu)
                break
            if best is None or ad < best[0]:
                best = (ad, lam, mu)
        if best[0] == 0:
            break
    _ad, lam, mu = best
    return dir_key(lam * u[0] + mu * v[0], lam * u[1] + mu * v[1])


def op_comb(u, v, a, b):
    return dir_key(a * u[0] + b * v[0], a * u[1] + b * v[1])


# -------- closure engine --------
def build_closure(S0):
    """Returns nodes: dict key -> (bits, tag, depth); plus per-depth stats."""
    pool = sorted(S0)                       # deterministic order
    base_bits = max(1, (len(pool) - 1).bit_length())
    nodes = {k: (base_bits, "BASE", 0) for k in pool}
    depth_new = {0: list(pool)}
    stats = []
    cum_angles = sorted(angle_deg(k) for k in nodes)

    def gapstat(angles):
        n = len(angles)
        gaps = [angles[i + 1] - angles[i] for i in range(n - 1)]
        gaps.append(angles[0] + 360.0 - angles[-1])
        gaps.sort()
        m = n // 2
        med = gaps[m - 1] if n % 2 else 0.5 * (gaps[m - 1] + gaps[m])
        return gaps[0], med

    stats.append((0, len(nodes), 0, *gapstat(cum_angles)))
    n_invalid = 0
    for depth in range(1, DEPTHS + 1):
        prev_new = depth_new[depth - 1]
        order = sorted(nodes.keys(), key=lambda k: angle_deg(k))
        n_pool = len(order)
        pbits = max(1, (n_pool - 1).bit_length())
        # deterministic pair sampling: 6000 random, 3000 adjacent, 3000 new-x-rand
        rnd = lcg(24000)
        pairs = []
        for i in range(6000):
            pairs.append((rnd[2 * i] % n_pool, rnd[2 * i + 1] % n_pool))
        for i in range(3000):
            j = rnd[12000 + 2 * i] % n_pool
            pairs.append((j, (j + 1) % n_pool))
        off = 18000
        ord_index = {k: i for i, k in enumerate(order)}
        for i in range(3000):
            a = rnd[off + 2 * i] % len(prev_new)
            b = rnd[off + 2 * i + 1] % n_pool
            pairs.append((ord_index[prev_new[a]], b))
        cands = []   # (bits, seq, key, tag)
        seq = 0
        bis_bits = 2 + 2 * pbits
        comb_bits = bis_bits + 3
        for (i, j) in pairs:
            if i == j:
                continue
            u, v = order[i], order[j]
            for tag, key, bits in (
                ("BIS_N", op_bis_n(u, v), bis_bits),
                ("BIS_B", op_bis_b(u, v), bis_bits),
                ("COMB", op_comb(u, v, 1, 1), comb_bits),
                ("COMB", op_comb(u, v, 1, 2), comb_bits),
                ("COMB", op_comb(u, v, 2, 1), comb_bits),
                ("COMB", op_comb(u, v, 2, 2), comb_bits),
                ("COMB", op_comb(u, v, 1, -1), comb_bits),
                ("COMB", op_comb(u, v, -1, -1), comb_bits),
            ):
                if key is None:
                    n_invalid += 1
                    continue
                cands.append((bits, seq, key, tag))
                seq += 1
        cands.sort()
        new_keys = []
        for bits, _seq, key, tag in cands:
            cur = nodes.get(key)
            if cur is None or bits < cur[0]:
                nodes[key] = (bits, tag, depth)
                if cur is None:
                    new_keys.append(key)
        depth_new[depth] = new_keys
        cum_angles = sorted(angle_deg(k) for k in nodes)
        gmin, gmed = gapstat(cum_angles)
        mean_bits = sum(nodes[k][0] for k in new_keys) / max(1, len(new_keys))
        stats.append((depth, len(new_keys), len(nodes), gmin, gmed, mean_bits))
    return nodes, stats, n_invalid


def bits_to_precision(nodes):
    """Per tolerance: median over 32 targets of min address bits hitting tol,
    unreached count, and winner-op histogram."""
    arr = sorted((angle_deg(k), nodes[k][0], nodes[k][1]) for k in nodes)
    angs = [a for a, _b, _t in arr]
    rows = []
    for tol in TOLS:
        bits_list = []
        tags = {"BASE": 0, "BIS_N": 0, "BIS_B": 0, "COMB": 0}
        for t in TARGETS:
            i = bisect.bisect_left(angs, t)
            lo = i
            hi = i
            best = None
            while True:
                moved = False
                if lo - 1 >= 0 and angdist(angs[lo - 1], t) <= tol:
                    lo -= 1
                    moved = True
                if hi < len(angs) and angdist(angs[hi], t) <= tol:
                    hi += 1
                    moved = True
                if lo == 0 and hi == len(angs):
                    break
                if not moved:
                    # also probe wraparound window
                    if angdist(angs[-1], t) <= tol and hi < len(angs):
                        hi = len(angs)
                        moved = True
                    if angdist(angs[0], t) <= tol and lo > 0:
                        lo = 0
                        moved = True
                    if not moved:
                        break
            for k in range(lo, hi):
                a, b, tg = arr[k]
                if angdist(a, t) <= tol and (best is None or b < best[0]):
                    best = (b, tg)
            if best is None:
                bits_list.append(None)
            else:
                bits_list.append(best[0])
                tags[best[1]] += 1
        got = [b for b in bits_list if b is not None]
        med = sorted(got)[len(got) // 2] if got else None
        rows.append((tol, med, 32 - len(got), tags))
    return rows


def median_err(nodes):
    angs = sorted(angle_deg(k) for k in nodes)
    errs = []
    for t in TARGETS:
        i = bisect.bisect_left(angs, t)
        best = 1e9
        for j in (i % len(angs), (i - 1) % len(angs)):
            best = min(best, angdist(angs[j], t))
        errs.append(best)
    es = sorted(errs)
    return 0.5 * (es[len(es) // 2 - 1] + es[len(es) // 2])


# =====================================================================
def run_all():
    L = []
    P = L.append
    P("== SPIN-13b SNAP-SHADOW ADDENDUM: BISECTION-COMBINATION CLOSURE ==")
    P("integer-only core; ops: BIS_N prim(u+v), BIS_B prim(l*u+m*v) with")
    P("l^2|u|^2 ~ m^2|v|^2 exact-integer balance, COMB prim(a*u+b*v);")
    P("seeds = SPIN-13 budget-16 (norm^2<=16) direction sets; pairs/depth=%d" % PAIRS_PER_DEPTH)
    P("")

    # ---- canaries
    P("== CANARIES ==")
    u30, v30 = (2, 0), (1, 1)
    ok1 = op_bis_b(u30, v30) == (3, 1) and abs(angle_deg((3, 1)) - 30.0) < 1e-9
    ok1b = op_bis_n(u30, v30) == (3, 1)
    P("  bisB((2,0),(1,1)) == (3,1) @ exactly 30deg: %s (naive equal: %s)"
      % ("PASS" if ok1 else "FAIL", ok1b))
    ok2 = all(op_bis_n(w, w) == w for w in ((1, 0), (1, 1), (3, 1), (5, 2)))
    P("  bisN(u,u) == u idempotence (primitive u): %s" % ("PASS" if ok2 else "FAIL"))
    ok3 = op_bis_n((2, 0), (-2, 0)) is None
    P("  opposite-direction op rejected (zero vector): %s" % ("PASS" if ok3 else "FAIL"))
    S_eis = seed_dirs(2, 1, PRE_BUDGET_SQ)
    direct = set()
    for a in range(-7, 8):
        for b in range(-7, 8):
            n2 = a * a + a * b + b * b
            if 0 < n2 <= PRE_BUDGET_SQ:
                k = dir_key(2 * a + b, b)
                direct.add(k)
    ok4 = S_eis == direct
    P("  eis seed set == independent direct enumeration (%d dirs): %s"
      % (len(S_eis), "PASS" if ok4 else "FAIL"))
    P("")

    arms = [("eis-2D", 2, 1), ("shadow d=4 s=1", 4, 1), ("shadow d=6 s=1", 6, 1),
            ("shadow d=8 s=1", 8, 1)]
    closure_results = {}
    P("== (1)+(2) PLETHORA & PRECISION LADDER (cumulative distinct directions) ==")
    P("  arm              | depth |   new  |  total | minGap     | medGap    | meanBits(new)")
    for tag, d, s in arms:
        S0 = seed_dirs(d, s, PRE_BUDGET_SQ)
        _LCG_X[0] = 12345  # reset LCG identically per arm
        nodes, stats, ninv = build_closure(S0)
        closure_results[tag] = nodes
        for row in stats:
            if row[0] == 0:
                P("  %-16s |     0 |     -- | %6d | %10.4f | %9.4f |      --"
                  % (tag, row[1], row[3], row[4]))
            else:
                P("  %-16s | %5d | %6d | %6d | %10.6f | %9.6f | %6.1f"
                  % (tag, row[0], row[1], row[2], row[3], row[4], row[5]))
        P("  %-16s   (invalid zero-vector ops rejected: %d)" % ("", ninv))
    P("")

    P("== (3) BITS-TO-PRECISION — minimal bit-string hitting tolerance ==")
    P("  (32 golden targets; medBits = median min address bits; X = unreached;")
    P("   winner op = which op created the minimal-bit node)")
    for tag, _d, _s in arms:
        rows = bits_to_precision(closure_results[tag])
        P("  %s:" % tag)
        for tol, med, unreach, tags in rows:
            P("    tol=%7.3fdeg : medBits=%s unreached=%2d  winners BASE/BIS_N/BIS_B/COMB = %d/%d/%d/%d"
              % (tol, med if med is not None else "--", unreach,
                 tags["BASE"], tags["BIS_N"], tags["BIS_B"], tags["COMB"]))
    P("")

    P("== RAW BUDGET-GROWTH BASELINES (no closure; bits = ceil(log2(#dirs))) ==")
    P("  arm                 | budget |  dirs  | bits | medErr(32 targets)")
    for tag, d, s, r2 in [("eis-2D", 2, 1, 16), ("eis-2D", 2, 1, 64),
                          ("eis-2D", 2, 1, 256), ("shadow d=4 s=1", 4, 1, 16),
                          ("shadow d=4 s=1", 4, 1, 64), ("shadow d=4 s=1", 4, 1, 256),
                          ("shadow d=6 s=1", 6, 1, 16), ("shadow d=8 s=1", 8, 1, 16)]:
        S = seed_dirs(d, s, r2)
        P("  %-18s | %6d | %6d | %4d | %9.5f deg"
          % (tag, r2, len(S), max(1, (len(S) - 1).bit_length()), median_err(S)))
    P("")

    P("== VERDICT INPUTS ==")
    eis_nodes = closure_results["eis-2D"]
    d8_nodes = closure_results["shadow d=8 s=1"]
    P("  eis: base %d dirs -> closure total %d dirs (%.1fx plethora),"
      % (36, len(eis_nodes), len(eis_nodes) / 36.0))
    e0 = median_err(set(k for k in eis_nodes if eis_nodes[k][2] == 0))
    e3 = median_err(eis_nodes)
    P("  eis: median target err base %.4f deg -> closure %.6f deg (%.0fx)"
      % (e0, e3, e0 / e3))
    r_eis = bits_to_precision(eis_nodes)
    r_d8 = bits_to_precision(d8_nodes)
    for tol in (0.1, 0.01):
        fe = [r for r in r_eis if r[0] == tol][0]
        f8 = [r for r in r_d8 if r[0] == tol][0]
        P("  tol %.3fdeg: eis-closure medBits=%s (unreached %d) | d8-closure medBits=%s (unreached %d)"
          % (tol, fe[1], fe[2], f8[1], f8[2]))
    P("")
    return "\n".join(L)


def main():
    out1 = run_all()
    out2 = run_all()
    det = out1 == out2
    print("== CANARY: full-suite double-run byte identity: %s ==" % ("PASS" if det else "FAIL"))
    print("")
    print(out1)


if __name__ == "__main__":
    main()
