#!/usr/bin/env python3
"""
ANGLEKIT — the shared snap-angle toolkit (SPIN-13 deliverable, addendum 3).

DIVISION OF LABOR (the contract):
  * ENGINEER (architecture/spec layer) owns TOLERANCE and application fit:
    chooses the per-application tolerance, the seed direction set, and the
    closure depth. Tolerance is ALWAYS a caller-supplied parameter — the
    toolkit never bakes one in.
  * MECHANIC (application layer) owns REFINEMENT: calls
    table.select(target, tolerance) and, when hand-tuning, applies the
    shared refinement ops (bisect_n / bisect_b / combine) — the same tools
    for every application, common property.
  * TOOLKIT (this module) is common property: integer-only exact core
    (Z[sqrt3] direction frame, primitive lattice renormalization, packed
    bitstring op-tree addresses). Floats appear only in angle display and
    nearest-search metrics; every returned construction is exact.

Public API:
  primitive(X, Y)                 -> direction key or None
  bisect_n(u, v), bisect_b(u, v)  -> shared refinement ops (exact)
  combine(u, v, a, b)             -> shared refinement op (exact)
  angle_deg(key), angdist(a, b)   -> display helpers (float)
  part_class(key), real_length(key) -> construction-cost classes (COST DOCTRINE)
  build_table(seed_set, depth=3, k_bits=16) -> AngleTable
  AngleTable.select(target_deg, tolerance_deg, prefer="cost") -> Selection | None
      COST DOCTRINE (addendum 4): the objective is NOT min |theta-target| but
      min CONSTRUCTION COST subject to |theta-target| <= tolerance.
      prefer="cost"  (default): rank by (part_class, bits, depth, err) —
          Pythagorean-standard forms (integer real length k=sqrt(X^2+3Y^2),
          k <= 64: the 3-4-5-class shelf) beat exotic high-norm hits even
          when the exotic is closer. The engineer's tolerance is exactly
          the room that makes standard parts viable.
      prefer="bits"  : legacy min-bitstring ranking (SPIN-13c/d semantics)
      prefer="nearest": min angle error, then bits
      None if nothing is within tolerance (sampling hole).
  AngleTable.key/bits/bitstring/evaluate(i)  -> exact node accessors
  AngleTable.catalog(max_k=64)   -> the shelf of standard parts
  AngleTable.bracket(target)     -> adjacent pair for hand refinement
  AngleTable.stats()              -> entries/payload/bytes per depth

Determinism: fixed LCG pair sampling; identical inputs give byte-identical
tables. Anchors: feeding the SPIN-13 seed sets reproduces SPIN-13b totals.
"""
import bisect
import math
from math import atan2, degrees, sqrt

SQRT3 = sqrt(3.0)
PAIRS_PER_DEPTH = 12000
BIS_BOUND = 12
COEFS = ((1, 1), (1, 2), (2, 1), (2, 2), (1, -1), (-1, -1))

_LCG_X = [12345]


def _lcg(n):
    out = []
    for _ in range(n):
        _LCG_X[0] = (1664525 * _LCG_X[0] + 1013904223) % 2147483648
        out.append(_LCG_X[0])
    return out


def igcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


# ---------------- exact core ----------------
def primitive(X, Y):
    """Direction key: primitive reduction of lattice vector (X, Y*sqrt3)."""
    if X == 0 and Y == 0:
        return None
    g = igcd(abs(X), abs(Y))
    return (X // g, Y // g)


def _norm2(X, Y):
    return X * X + 3 * Y * Y


def bisect_n(u, v):
    """Naive arc bisection with lattice renorm: prim(u + v)."""
    return primitive(u[0] + v[0], u[1] + v[1])


def bisect_b(u, v):
    """Balanced arc bisection: prim(l*u + m*v) with l^2|u|^2 ~ m^2|v|^2
    chosen by exact integer norm comparison (no trig)."""
    n1, n2 = _norm2(*u), _norm2(*v)
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
    return primitive(lam * u[0] + mu * v[0], lam * u[1] + mu * v[1])


def combine(u, v, a=1, b=1):
    """Integer combination with lattice renorm: prim(a*u + b*v)."""
    return primitive(a * u[0] + b * v[0], a * u[1] + b * v[1])


def angle_deg(key):
    X, Y = key
    return degrees(atan2(Y * SQRT3, X)) % 360.0


def angdist(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


# ---------------- cost doctrine (addendum 4) ----------------
_STD_K_MAX = 64


def part_class(key):
    """Construction-cost class of a direction (integer-only).
    norm2 = X^2 + 3Y^2 is the exact squared real length in the (X, Y*sqrt3)
    frame; a perfect square means INTEGER real length k — the Pythagorean
    analog in this frame (Euclid-style: X=m^2-3n^2, Y=2mn, k=m^2+3n^2).
    class 0: standard part — integer length, k <= 64 (cheap/common/durable)
    class 1: integer length, any k
    class 2: small mundane norm (norm2 <= 100)
    class 3: exotic (everything else)"""
    X, Y = key
    n2 = X * X + 3 * Y * Y
    k = math.isqrt(n2)
    if k * k == n2:
        return 0 if k <= _STD_K_MAX else 1
    return 2 if n2 <= 100 else 3


def real_length(key):
    """Exact integer real length k if X^2+3Y^2 is a perfect square, else None."""
    X, Y = key
    n2 = X * X + 3 * Y * Y
    k = math.isqrt(n2)
    return k if k * k == n2 else None


# ---------------- table construction ----------------
class AngleTable(object):
    """Closure table over a seed direction set with packed bitstring
    addresses. select() honors caller tolerance — never baked in."""

    def __init__(self, seed_set, depth=3, k_bits=16):
        _LCG_X[0] = 12345  # every table build is self-contained/deterministic
        self.k_bits = k_bits
        self.nbuck = 1 << k_bits
        self.buck_w = 360.0 / self.nbuck
        pool = sorted(set(seed_set))
        base_bits = max(1, (len(pool) - 1).bit_length())
        # node record: [key, bits, val, tag, pi, pj, coefcode, depth, pw]
        self.nodes = [[k, base_bits, i, -1, i, -1, -1, 0, 0]
                      for i, k in enumerate(pool)]
        self.best = {k: i for i, k in enumerate(pool)}
        depth_new = {0: list(range(len(pool)))}
        for dep in range(1, depth + 1):
            self._close_depth(dep, depth_new)
        # angle-sorted view for exact selects
        self._aorder = sorted(range(len(self.nodes)),
                              key=lambda i: angle_deg(self.nodes[i][0]))
        self._aang = [angle_deg(self.nodes[i][0]) for i in self._aorder]
        self._dense = {}   # tolerance -> dense list (lazy fast path)

    def _close_depth(self, dep, depth_new):
        nodes, best = self.nodes, self.best
        prev_new = depth_new[dep - 1]
        cur_ids = sorted(best.values(), key=lambda i: angle_deg(nodes[i][0]))
        n_pool = len(cur_ids)
        pbits = max(1, (n_pool - 1).bit_length())
        pos_of = {nid: p for p, nid in enumerate(cur_ids)}
        rnd = _lcg(24000)
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
        wbits = max(1, (len(nodes) - 1).bit_length())  # parent-id width
        bis_bits = 2 + 2 * wbits
        comb_bits = bis_bits + 3
        cands = []
        seq = 0
        for (i, j) in pairs:
            if i == j:
                continue
            u, v = nodes[cur_ids[i]][0], nodes[cur_ids[j]][0]
            for tag, key, bits, cc in (
                (0, bisect_n(u, v), bis_bits, -1),
                (1, bisect_b(u, v), bis_bits, -1),
                (2, combine(u, v, *COEFS[0]), comb_bits, 0),
                (2, combine(u, v, *COEFS[1]), comb_bits, 1),
                (2, combine(u, v, *COEFS[2]), comb_bits, 2),
                (2, combine(u, v, *COEFS[3]), comb_bits, 3),
                (2, combine(u, v, *COEFS[4]), comb_bits, 4),
                (2, combine(u, v, *COEFS[5]), comb_bits, 5),
            ):
                if key is None:
                    continue
                pi, pj = cur_ids[i], cur_ids[j]
                if tag == 2:
                    val = 2 | (pi << 2) | (pj << (2 + wbits)) | (cc << (2 + 2 * wbits))
                else:
                    val = tag | (pi << 2) | (pj << (2 + wbits))
                cands.append((bits, seq, key, tag, pi, pj, cc, val, wbits))
                seq += 1
        cands.sort()
        new_ids = []
        for bits, _s, key, tag, pi, pj, cc, val, wb in cands:
            bi = best.get(key)
            if bi is None or bits < nodes[bi][1]:
                nodes.append([key, bits, val, tag, pi, pj, cc, dep, wb])
                nid = len(nodes) - 1
                if bi is None:
                    new_ids.append(nid)
                best[key] = nid
        depth_new[dep] = new_ids

    # ---------------- mechanic-facing API ----------------
    def n_entries(self):
        return len(self.best)

    def key(self, i):
        return self.nodes[i][0]

    def bits(self, i):
        return self.nodes[i][1]

    def bitstring(self, i):
        nd = self.nodes[i]
        return (nd[2], nd[1])  # (packed value, width in bits)

    def evaluate(self, i, _memo=None):
        """Exact op-tree evaluation of node i's bitstring -> direction key."""
        memo = _memo if _memo is not None else {}
        if i in memo:
            return memo[i]
        nd = self.nodes[i]
        if nd[3] == -1:
            memo[i] = nd[0]
            return nd[0]
        u = self.evaluate(nd[4], memo)
        v = self.evaluate(nd[5], memo)
        if nd[3] == 0:
            k = bisect_n(u, v)
        elif nd[3] == 1:
            k = bisect_b(u, v)
        else:
            k = combine(u, v, *COEFS[nd[6]])
        memo[i] = k
        return k

    def select(self, target_deg, tolerance_deg, prefer="cost"):
        """Rank-and-return within tolerance. The engineer supplies tolerance;
        the ranking policy implements the cost doctrine (module docstring):
        prefer='cost' (default) | 'bits' (legacy) | 'nearest'."""
        if prefer == "bits" and tolerance_deg >= 4.0 * self.buck_w:
            slots = self._dense.get(tolerance_deg)
            if slots is None:
                slots = self._build_dense(tolerance_deg)
            b = int(target_deg / self.buck_w) % self.nbuck
            nid = slots[b]
            if nid == -1:
                return None
            if angdist(angle_deg(self.nodes[nid][0]), target_deg) > tolerance_deg:
                nid = self._exact_scan(target_deg, tolerance_deg, prefer)
                if nid is None:
                    return None
        else:
            nid = self._exact_scan(target_deg, tolerance_deg, prefer)
            if nid is None:
                return None
        nd = self.nodes[nid]
        ang = angle_deg(nd[0])
        return {"node": nid, "key": nd[0], "bits": nd[1],
                "bitstring": (nd[2], nd[1]), "angle_deg": ang,
                "err_deg": angdist(ang, target_deg),
                "cost_class": part_class(nd[0]),
                "real_length": real_length(nd[0])}

    def bracket(self, target_deg):
        """The two angularly-adjacent table directions around a target —
        the mechanic's starting pair for shared-op refinement."""
        angs = self._aang
        i = bisect.bisect_left(angs, target_deg)
        return (self.key(self._aorder[(i - 1) % len(angs)]),
                self.key(self._aorder[i % len(angs)]))

    def catalog(self, max_k=_STD_K_MAX):
        """The shelf of standard parts: distinct directions with integer real
        length k <= max_k, cheapest address first."""
        out = {}
        for nd in self.nodes:
            k = real_length(nd[0])
            if k is not None and k <= max_k:
                cur = out.get(nd[0])
                if cur is None or nd[1] < cur[0]:
                    out[nd[0]] = (nd[1], nd[7], k)
        return sorted((v[2], key, v[0], v[1]) for key, v in out.items())

    def _exact_scan(self, t, tol, prefer="bits"):
        angs = self._aang
        n = len(angs)
        i = bisect.bisect_left(angs, t)
        lo = hi = i
        while lo > 0 and angdist(angs[lo - 1], t) <= tol:
            lo -= 1
        while hi < n and angdist(angs[hi], t) <= tol:
            hi += 1
        if lo == 0 and angdist(angs[-1], t) <= tol:
            hi = n
        if hi == n and angdist(angs[0], t) <= tol:
            lo = 0
        best = None
        best_rank = None
        for j in range(lo, hi):
            if angdist(angs[j], t) > tol:
                continue
            nid = self._aorder[j]
            nd = self.nodes[nid]
            if prefer == "cost":
                rank = (part_class(nd[0]), nd[1], nd[7], angdist(angs[j], t))
            elif prefer == "nearest":
                rank = (angdist(angs[j], t), nd[1])
            else:  # "bits" (legacy SPIN-13c/d semantics)
                rank = (nd[1], nd[7], angdist(angs[j], t))
            if best_rank is None or rank < best_rank:
                best_rank = rank
                best = nid
        return best

    def _build_dense(self, tol):
        order = sorted(range(len(self.nodes)), key=lambda i: (self.nodes[i][1], i))
        angs = [angle_deg(self.nodes[i][0]) for i in order]
        slots = [-1] * self.nbuck
        remaining = self.nbuck
        span = int(tol / self.buck_w) + 1
        for pos, i in enumerate(order):
            if remaining == 0:
                break
            th = angs[pos]
            b0 = int(th / self.buck_w)
            for b in range(b0 - span, b0 + span + 1):
                bb = b % self.nbuck
                if slots[bb] == -1:
                    c = (bb + 0.5) * self.buck_w
                    if angdist(th, c) <= tol:
                        slots[bb] = i
                        remaining -= 1
        self._dense[tol] = slots
        return slots

    def stats(self):
        """Per-depth table stats: entries (distinct directions) and payload
        bytes of addressable op-tree records."""
        nbest = {}
        for nid in self.best.values():
            d = self.nodes[nid][7]
            nbest[d] = nbest.get(d, 0) + 1
        pay = {}
        for nd in self.nodes:
            pay[nd[7]] = pay.get(nd[7], 0) + (nd[1] + 7) // 8
        depthmax = max(nd[7] for nd in self.nodes)
        out = []
        cum = 0
        for d in range(depthmax + 1):
            cum += nbest.get(d, 0)
            out.append((d, cum, pay.get(d, 0)))
        return out


def build_table(seed_set, depth=3, k_bits=16):
    """ENGINEER entry point: seed_set = direction keys (e.g. from any
    integer lattice shadow), depth = closure depth budget."""
    return AngleTable(seed_set, depth=depth, k_bits=k_bits)


# ---------------- seed-set helpers (shared lattice machinery) ----------------
def igcd2(a, b):
    return igcd(a, b)


def proj_matrix(d, seed, b_entries=3):
    """Fixed seeded integer projection Z^d -> Z^2 (SPIN-13 convention;
    d=2 returns the Eisenstein identity)."""
    if d == 2:
        return (2, 1), (0, 1)
    rnd = __import__("random").Random(9173 * seed + d)
    while True:
        mx = tuple(rnd.randint(-b_entries, b_entries) for _ in range(d))
        my = tuple(rnd.randint(-b_entries, b_entries) for _ in range(d))
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


def seed_dirs(d, seed, r2max=16):
    """Shadow direction set: integer ball of Z^d (d=2: Eisenstein) under the
    fixed projection, primitive-reduced. The shared lattice machinery."""
    mx, my = proj_matrix(d, seed)
    pts = enum_ball_eis(r2max) if d == 2 else enum_ball_sq(d, r2max)
    dirs = set()
    for _n2, z in pts:
        k = primitive(sum(a * b for a, b in zip(mx, z)),
                      sum(a * b for a, b in zip(my, z)))
        if k is not None:
            dirs.add(k)
    return dirs
