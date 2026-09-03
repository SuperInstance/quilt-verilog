#!/usr/bin/env python3
"""
SPIN-13c SNAP-SHADOW ADDENDUM 2 — LUT REGIME (Casey, experiment 6):
"if lookup tables are being created anyway for a set of options for lightning
speed, it changes the optimization calculation for reaching an angle precise
enough to be within tolerance but absolute in its construction."

What is measured:
  * FULL closure table (depth <= 3) with REAL packed bitstring addresses
    (op tree: tag + parent node-ids + coefficient code); construction stays
    exact integer; only the lookup key is quantized (fixed-point angle,
    k=16 bits -> 65536 buckets of 0.00549 deg).
  * (a) cheapest-absolute representation by TABLE LOOKUP vs ONLINE SEARCH
        on 64 targets x tolerance ladder (expect identical -> offline
        exhaustive = online optimal; quantify any quantization drift).
  * (b) memory cost curve: entries / payload bytes per depth, and
        tolerance-partitioned tables (dense per-tolerance 32-bit node-id
        arrays + shared node payload; Pareto-compressed variant).
  * (c) sweet spot: "lightning-speed absolute angle selection at X KB"
        per arm/depth, incl. raw-budget-growth LUT comparison.

Anchors: closure direction totals must equal SPIN-13b exactly (same LCG pair
sampling, same op order); address self-evaluation canary (op trees re-evaluated
exactly reproduce stored directions); double-run byte identity.
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
TOLS = (10.0, 3.0, 1.0, 0.3, 0.1, 0.03, 0.01, 0.003)
TARGETS = [(360.0 * (i + 1) * PHI) % 360.0 for i in range(64)]
K_BITS = 16
NBUCK = 1 << K_BITS
BUCK_W = 360.0 / NBUCK
# SPIN-13b anchors (cumulative distinct directions per depth 0..3)
ANCHORS = {
    "eis-2D": [36, 341, 6012, 32254],
    "shadow d=4 s=1": [350, 4468, 30029, 71995],
    "shadow d=6 s=1": [984, 8386, 38121, 82079],
    "shadow d=8 s=1": [866, 7830, 37424, 80625],
}
OP_TAGS = ("BIS_N", "BIS_B", "COMB")
COEFS = ((1, 1), (1, 2), (2, 1), (2, 2), (1, -1), (-1, -1))

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


# -------- enumeration & projections (verbatim SPIN-13/13b) --------
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


# -------- closure with packed bitstring addresses --------
def build_closure_addr(S0):
    pool = sorted(S0)
    base_bits = max(1, (len(pool) - 1).bit_length())
    # node record: [key, bits, val, tag, pi, pj, coefcode, depth]
    nodes = [[k, base_bits, i, -1, i, -1, -1, 0] for i, k in enumerate(pool)]
    best = {k: i for i, k in enumerate(pool)}
    depth_new = {0: list(range(len(pool)))}
    totals = [len(pool)]
    for depth in range(1, DEPTHS + 1):
        prev_new = depth_new[depth - 1]
        # pool = CURRENT best record per direction (matches 13b deduped pool)
        cur_ids = sorted(best.values(), key=lambda i: angle_deg(nodes[i][0]))
        n_pool = len(cur_ids)
        pbits = max(1, (n_pool - 1).bit_length())
        pos_of = {nid: p for p, nid in enumerate(cur_ids)}
        rnd = lcg(24000)
        pairs = []
        for i in range(6000):
            pairs.append((rnd[2 * i] % n_pool, rnd[2 * i + 1] % n_pool))
        for i in range(3000):
            j = rnd[12000 + 2 * i] % n_pool
            pairs.append((j, (j + 1) % n_pool))
        off = 18000
        for i in range(3000):
            a = rnd[off + 2 * i] % len(prev_new)
            b = rnd[off + 2 * i + 1] % n_pool
            pairs.append((pos_of[prev_new[a]], b))
        bis_bits = 2 + 2 * pbits
        comb_bits = bis_bits + 3
        cands = []
        seq = 0
        for (i, j) in pairs:
            if i == j:
                continue
            u, v = nodes[cur_ids[i]][0], nodes[cur_ids[j]][0]
            for tag, key, bits, cc in (
                (0, op_bis_n(u, v), bis_bits, -1),
                (1, op_bis_b(u, v), bis_bits, -1),
                (2, op_comb(u, v, *COEFS[0]), comb_bits, 0),
                (2, op_comb(u, v, *COEFS[1]), comb_bits, 1),
                (2, op_comb(u, v, *COEFS[2]), comb_bits, 2),
                (2, op_comb(u, v, *COEFS[3]), comb_bits, 3),
                (2, op_comb(u, v, *COEFS[4]), comb_bits, 4),
                (2, op_comb(u, v, *COEFS[5]), comb_bits, 5),
            ):
                if key is None:
                    continue
                pi, pj = cur_ids[i], cur_ids[j]
                if tag == 2:
                    val = (2) | (pi << 2) | (pj << (2 + pbits)) | (cc << (2 + 2 * pbits))
                else:
                    val = tag | (pi << 2) | (pj << (2 + pbits))
                cands.append((bits, seq, key, tag, pi, pj, cc, val))
                seq += 1
        cands.sort()
        new_ids = []
        for bits, _s, key, tag, pi, pj, cc, val in cands:
            bi = best.get(key)
            if bi is None or bits < nodes[bi][1]:
                nodes.append([key, bits, val, tag, pi, pj, cc, depth])
                nid = len(nodes) - 1
                if bi is None:
                    new_ids.append(nid)
                best[key] = nid
        depth_new[depth] = new_ids
        totals.append(len(best))
    return nodes, best, totals


def eval_node(nodes, i, memo):
    if i in memo:
        return memo[i]
    nd = nodes[i]
    if nd[3] == -1:
        memo[i] = nd[0]
        return nd[0]
    u = eval_node(nodes, nd[4], memo)
    v = eval_node(nodes, nd[5], memo)
    if nd[3] == 0:
        k = op_bis_n(u, v)
    elif nd[3] == 1:
        k = op_bis_b(u, v)
    else:
        k = op_comb(u, v, *COEFS[nd[6]])
    memo[i] = k
    return k


def build_lut(nodes):
    """Per-tolerance dense LUTs: bucket -> node id (min address bits among
    nodes within tol of bucket center), nodes processed bits-ascending."""
    order = sorted(range(len(nodes)), key=lambda i: (nodes[i][1], i))
    angs = [angle_deg(nodes[i][0]) for i in order]
    luts = {}
    for tol in TOLS:
        slots = [-1] * NBUCK
        remaining = NBUCK
        span = int(tol / BUCK_W) + 1
        for pos, i in enumerate(order):
            if remaining == 0:
                break
            th = angs[pos]
            b0 = int(th / BUCK_W)
            for b in range(b0 - span, b0 + span + 1):
                bb = b % NBUCK
                if slots[bb] == -1:
                    c = (bb + 0.5) * BUCK_W
                    if angdist(th, c) <= tol:
                        slots[bb] = i
                        remaining -= 1
        luts[tol] = slots
    return luts, order, angs


def online_min_bits(nodes, order, angs, t, tol):
    """Optimal reference: minimal address bits among all nodes within tol of t.
    Two-pointer window expansion on the angle-sorted node list."""
    if not angs:
        return None
    n = len(angs)
    i = bisect.bisect_left(angs, t)
    lo = hi = i
    if lo > 0 and angdist(angs[lo - 1], t) > tol and angdist(angs[-1], t) > tol \
            and angdist(angs[0], t) > tol:
        return None  # nearest neighbors already out of tolerance
    best = None
    while lo > 0 and angdist(angs[lo - 1], t) <= tol:
        lo -= 1
    while hi < n and angdist(angs[hi], t) <= tol:
        hi += 1
    if lo == 0 and angdist(angs[-1], t) <= tol:
        hi = n
    if hi == n and angdist(angs[0], t) <= tol:
        lo = 0
    for j in range(lo, hi):
        if angdist(angs[j], t) > tol:
            continue
        b = nodes[order[j]][1]
        if best is None or b < best:
            best = b
    return best


# =====================================================================
def run_all():
    global nodes_global
    L = []
    P = L.append
    P("== SPIN-13c LUT REGIME: closure tables, offline-exhaustive vs online ==")
    P("lookup key: fixed-point angle k=%d bits (%d buckets, %.5f deg/bucket);"
      % (K_BITS, NBUCK, BUCK_W))
    P("construction stays exact bitstring op-trees; only the key quantizes.")
    P("")

    arms = [("eis-2D", 2, 1), ("shadow d=4 s=1", 4, 1),
            ("shadow d=6 s=1", 6, 1), ("shadow d=8 s=1", 8, 1)]

    P("== CANARIES ==")
    P("  (anchors: closure totals must equal SPIN-13b; addr self-evaluation)")
    anchor_ok = True
    eval_ok = True
    results = {}
    for tag, d, s in arms:
        S0 = seed_dirs(d, s, PRE_BUDGET_SQ)
        _LCG_X[0] = 12345
        nodes, best, totals = build_closure_addr(S0)
        results[tag] = (nodes, best, totals)
        exp = ANCHORS[tag]
        match = totals == exp
        anchor_ok &= match
        P("  %-16s totals %s vs 13b %s : %s" % (tag, totals, exp,
                                                 "PASS" if match else "FAIL"))
    # address self-evaluation canary (512 deterministic samples over eis nodes)
    nds = results["eis-2D"][0]
    memo = {}
    samp = lcg(512)
    for v in samp:
        i = v % len(nds)
        if eval_node(nds, i, memo) != nds[i][0]:
            eval_ok = False
            break
    P("  addr op-tree re-evaluation (512 samples, exact): %s"
      % ("PASS" if eval_ok else "FAIL"))
    P("")

    P("== (b) MEMORY COST CURVE — per depth (entries = distinct directions;")
    P("    payload counts ALL addressable op-tree records incl. superseded parents) ==")
    P("  arm              | depth |  entries | payloadBytes | meanBits | maxBits")
    for tag, _d, _s in arms:
        nodes = results[tag][0]
        best = results[tag][1]
        bydepth = [[], [], [], []]
        for nd in nodes:
            bydepth[nd[7]].append(nd)
        nbest = [0, 0, 0, 0]
        for nid in best.values():
            nbest[nodes[nid][7]] += 1
        cum_entries = 0
        for dep in range(4):
            cum_entries += nbest[dep]
            pb = sum((nd[1] + 7) // 8 for nd in bydepth[dep])
            mb = sum(nd[1] for nd in bydepth[dep]) / max(1, len(bydepth[dep]))
            xb = max(nd[1] for nd in bydepth[dep]) if bydepth[dep] else 0
            P("  %-16s | %5d | %8d | %12d | %8.1f | %7d"
              % (tag, dep, cum_entries, pb, mb, xb))
    P("")

    P("== LUT tables (dense per-tolerance, 32-bit node ids) ==")
    P("  dense table = %d buckets x 4B = %d KB per tolerance; node payload shared." %
      (NBUCK, NBUCK * 4 // 1024))
    P("")
    for tag, _d, _s in arms:
        nodes = results[tag][0]
        nodes_g = nodes
        luts, order, angs = build_lut(nodes)
        # angle-sorted reference for the online optimal search
        aorder = sorted(range(len(nodes)), key=lambda i: angle_deg(nodes[i][0]))
        aang = [angle_deg(nodes[i][0]) for i in aorder]
        P("  %s: coverage per tolerance (holes = buckets with no node within tol):" % tag)
        for tol in TOLS:
            slots = luts[tol]
            cov = sum(1 for x in slots if x != -1)
            P("    tol=%7.3fdeg : coverage %6.2f%%  (%d/%d buckets)"
              % (tol, 100.0 * cov / NBUCK, cov, NBUCK))
        # Pareto-compressed single table: per bucket, all distinct (tol,node) fills
        slot_sets = [set() for _ in range(NBUCK)]
        for tol in TOLS:
            slots = luts[tol]
            for b in range(NBUCK):
                if slots[b] != -1:
                    slot_sets[b].add(slots[b])
        tot_slots = sum(len(x) for x in slot_sets)
        pareto_kb = (NBUCK + tot_slots * 5) / 1024.0
        P("    Pareto single-table (all tolerances): %d slots, ~%.0f KB"
          % (tot_slots, pareto_kb))
        # (a) online vs lookup on 64 targets
        P("    (a) lookup vs online optimal (64 targets):")
        for tol in TOLS:
            slots = luts[tol]
            same = 0
            miss = 0
            lut_bad = 0
            dbits = []
            for t in TARGETS:
                b = int(t / BUCK_W) % NBUCK
                nid = slots[b]
                if nid == -1:
                    miss += 1
                    continue
                lut_bits = nodes[nid][1]
                if angdist(angle_deg(nodes[nid][0]), t) > tol:
                    lut_bad += 1  # quantization: entry within tol of bucket
                    continue      # center but not of this edge-of-bucket target
                onl = online_min_bits(nodes_g, aorder, aang, t, tol)
                if onl is None:
                    continue
                if lut_bits == onl:
                    same += 1
                else:
                    dbits.append(lut_bits - onl)
            nd = 64 - miss - lut_bad
            mean_d = (sum(dbits) / len(dbits)) if dbits else 0.0
            max_d = max(dbits) if dbits else 0
            P("      tol=%7.3f: identical %2d/%2d  lookup-miss %2d  out-of-tol(via bucket edge) %2d  meanDeltaBits %+.2f  maxDelta %+d"
              % (tol, same, nd, miss, lut_bad, mean_d, max_d))
        P("")

    P("== (c) SWEET SPOT — lightning-speed absolute angle selection at X KB ==")
    P("  arm              | depth | payload | + 1 dense tau-table | serves (median err deg)")
    for tag, _d, _s in arms:
        nodes = results[tag][0]
        bydepth = [[], [], [], []]
        for nd in nodes:
            bydepth[nd[7]].append(nd)
        cum_bytes = 0
        for dep in range(1, 4):
            cum_bytes += sum((nd[1] + 7) // 8 for nd in bydepth[dep])
            dep_keys = set()
            for dd in range(dep + 1):
                for nd in bydepth[dd]:
                    dep_keys.add(nd[0])
            aa = sorted(angle_deg(k) for k in dep_keys)
            errs = []
            for t in TARGETS:
                i = bisect.bisect_left(aa, t)
                best = 1e9
                for j in (i % len(aa), (i - 1) % len(aa)):
                    best = min(best, angdist(aa[j], t))
                errs.append(best)
            errs.sort()
            med = 0.5 * (errs[31] + errs[32])
            P("  %-16s | %5d | %6d B | %8d B total | %.5f"
              % (tag, dep, cum_bytes, cum_bytes + NBUCK * 4, med))
    P("")
    P("  raw-budget LUT comparison (no closure; ids only):")
    for tag, d, s, r2 in [("eis-2D", 2, 1, 256), ("shadow d=4 s=1", 4, 1, 256)]:
        S = seed_dirs(d, s, r2)
        aa = sorted(angle_deg(k) for k in S)
        errs = []
        for t in TARGETS:
            i = bisect.bisect_left(aa, t)
            best = 1e9
            for j in (i % len(aa), (i - 1) % len(aa)):
                best = min(best, angdist(aa[j], t))
            errs.append(best)
        errs.sort()
        med = 0.5 * (errs[31] + errs[32])
        P("    %-16s budget %3d: %5d dirs, ids %2d bits -> %5d B payload; median err %.5f deg"
          % (tag, r2, len(S), max(1, (len(S) - 1).bit_length()),
             len(S) * ((max(1, (len(S) - 1).bit_length()) + 7) // 8), med))
    P("")
    P("  online search cost per query: scan N nodes (e.g. %d nodes for eis depth-3);"
      % len(results["eis-2D"][0]))
    P("  LUT cost per query: 1 array read. Build once; break-even after a handful")
    P("  of queries in Python terms, and the table IS the deliverable in hardware.")
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
