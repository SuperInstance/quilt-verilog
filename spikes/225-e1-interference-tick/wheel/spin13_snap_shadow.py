#!/usr/bin/env python3
"""
SPIN-13 SNAP-SHADOW — multidimensional integer snapping shadowed back to 2D.

Claim under test (Casey): "multidimensional snapping shadowed back to smaller
dimensions for an explosion in possible precise angles and splines."

Design:
  * Domain lattices Z^d for d in {2,3,4,6,8} (d=2 = Eisenstein lattice with
    quadratic form a^2+ab+b^2, the strongest 2D baseline).
  * Shadow plane has coordinates (X, Y*sqrt3) with X,Y integers; projection
    X = Mx.z, Y = My.z with FIXED seeded integer matrices (entries in [-3,3],
    columns required to generate the full integer frame Z^2, i.e. Smith
    invariants (1,1)). d=2 uses the Eisenstein identity (2,1),(0,1).
  * INTEGER-ONLY CORE: direction dedup/keys/ordering, B-spline tangent keys,
    curvature signs, budget accounting — all exact integer arithmetic
    (parallelism test = integer cross product in the (X, Y*sqrt3) frame).
    Floats are used ONLY for display angles, nearest-point search metrics,
    and summary statistics.

Experiments:
  EXP1a  distinct snap angles at MATCHED POINT BUDGET (same # lattice points).
  EXP1b  distinct snap angles at MATCHED RADIUS (same domain norm^2 bound).
  EXP2   angular gap distribution (min/median/max) at matched budget & radius.
  EXP3   splines: point-snapped quadratic B-splines (exact dyadic sampling),
         direction-snapped control polygons, worked example of an angle
         (113,21)*sqrt3-frame that is low-budget-unrepresentable in 2D,
         plus unbiased median target-angle error over 64 golden targets.
  EXP4   cost: kernel redundancy, point-snap error, angle gain, sweet spot.

Canaries: d_in=2 shadow == independently-coded direct Eisenstein direction set
at several budgets; Eisenstein shell counts 6/12/18/30; full-suite double-run
byte identity; fixed seeds only.
"""
import bisect
import math
import random
from math import atan2, degrees, sqrt

SQRT3 = sqrt(3.0)
B_ENTRIES = 3
SEEDS = (1, 2, 3)
DIMS = (2, 3, 4, 6, 8)
BUDGETS = (24, 128, 1024, 8192)          # matched point budgets
SHELLS = (1, 2, 3, 4, 6, 8)              # matched radius (norm^2) bounds
PRE_BUDGET_SQ = 16                        # spline / precision budget (norm^2)
FRONTIER_CAP = {3: 36, 4: 36, 6: 25, 8: 16}  # worked-example frontier caps
# (X,Y) with X-Y odd: NEVER an exact Eisenstein direction (parity), i.e.
# genuinely 2D-unrepresentable exactly; only approachable by approximation.
TARGET_KEY = (113, 20)                    # worked-example direction (X,Y)

_t0 = __import__("time").time()


def igcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def dir_key(X, Y):
    """Primitive directed key of shadow vector (X, Y*sqrt3). None if origin."""
    if X == 0 and Y == 0:
        return None
    g = igcd(abs(X), abs(Y))
    return (X // g, Y // g)


def angle_deg(key):
    X, Y = key
    return degrees(atan2(Y * SQRT3, X)) % 360.0


# ---------------------------------------------------------------- enumeration
def enum_ball_sq(d, r2max):
    """All z in Z^d with 0 < sum z_i^2 <= r2max, sorted by (norm2, lex)."""
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
    """(a,b) with 0 < a^2+ab+b^2 <= r2max (Eisenstein norm), sorted."""
    pts = []
    R = math.isqrt(r2max) + 2
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            n2 = a * a + a * b + b * b
            if 0 < n2 <= r2max:
                pts.append((n2, (a, b)))
    pts.sort()
    return pts


_cache = {}


def ball(d, r2max):
    k = (d, r2max)
    if k not in _cache:
        _cache[k] = enum_ball_eis(r2max) if d == 2 else enum_ball_sq(d, r2max)
    return _cache[k]


def budget_ball(d, N):
    """Smallest power-of-two radius ball with >= N points; sorted list."""
    r2max = 1
    while len(ball(d, r2max)) < N:
        r2max *= 2
    return ball(d, r2max)


def budget_slice(d, N):
    return budget_ball(d, N)[:N]


# ---------------------------------------------------------------- projections
def proj_matrix(d, seed):
    if d == 2:
        return (2, 1), (0, 1)  # Eisenstein identity — canary arm
    rnd = random.Random(9173 * seed + d)
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


def area_scale(mx, my):
    """A = sigma1*sigma2 = sqrt(det(M M^T)) — exact integer sum, float sqrt."""
    d = len(mx)
    s = 0
    for i in range(d):
        for j in range(i + 1, d):
            mnr = mx[i] * my[j] - mx[j] * my[i]
            s += mnr * mnr
    return sqrt(float(s))


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def shadow_scan(mx, my, pts):
    """Direction keys + distinct shadow points over a point list."""
    dirs = set()
    shpts = set()
    for _n2, z in pts:
        X = dot(mx, z)
        Y = dot(my, z)
        k = dir_key(X, Y)
        if k is not None:
            dirs.add(k)
            shpts.add((X, Y))
    return dirs, shpts


# ---------------------------------------------------------------- statistics
def gap_stats(dirs):
    angs = sorted(angle_deg(k) for k in dirs)
    n = len(angs)
    if n < 2:
        return None
    gaps = [angs[i + 1] - angs[i] for i in range(n - 1)]
    gaps.append(angs[0] + 360.0 - angs[-1])
    gaps.sort()
    m = n // 2
    med = gaps[m - 1] if n % 2 else 0.5 * (gaps[m - 1] + gaps[m])
    return gaps[0], med, gaps[-1], 360.0 / n


def median(xs):
    ys = sorted(xs)
    m = len(ys) // 2
    if len(ys) % 2:
        return ys[m]
    return 0.5 * (ys[m - 1] + ys[m])


# ------------------------------------------------------- direct 2D baselines
def direct_eis_dirs(N):
    """INDEPENDENT code path: enumerate Eisenstein, dedup by linear scan.
    Square-window growth, then prefix-completion so the first-N slice is the
    true global (n2, lex) prefix (|a| <= 2*sqrt(n2N) covers the shell)."""
    def gather(R):
        lst = []
        for a in range(-R, R + 1):
            for b in range(-R, R + 1):
                n2 = a * a + a * b + b * b
                if n2 > 0:
                    lst.append((n2, a, b))
        lst.sort()
        return lst

    R = 2
    lst = gather(R)
    while len(lst) < N:
        R *= 2
        lst = gather(R)
    n2N = lst[N - 1][0]
    Rneed = int(2 * math.sqrt(n2N)) + 1
    if Rneed > R:
        lst = gather(Rneed)
    out = []
    for _n2, a, b in lst[:N]:
        X, Y = 2 * a + b, b
        g = igcd(abs(X), abs(Y))
        pr = (X // g, Y // g)
        if pr not in out:
            out.append(pr)
    return set(out)


def err_frontier(mx, my, pts_sorted, target_deg):
    """(budget n2, best err deg) improvement frontier over ascending n2."""
    best = 1e9
    out = []
    for n2, z in pts_sorted:
        k = dir_key(dot(mx, z), dot(my, z))
        if k is None:
            continue
        err = abs(((angle_deg(k) - target_deg + 180.0) % 360.0) - 180.0)
        if err < best:
            best = err
            out.append((n2, err))
    return out


def budget_for(frontier, thresh):
    for n2, err in frontier:
        if err <= thresh:
            return n2
    return None


# ----------------------------------------------------------------- splines
def bspline_samples(ctrl):
    """Exact uniform quadratic B-spline samples at u in {0,1/2,1} per segment,
    numerators over common denominator 8. Returns [(xnum, ynum), ...]."""
    samples = []
    m = len(ctrl)
    for j in range(m - 2):
        C0, C1, C2 = ctrl[j], ctrl[j + 1], ctrl[j + 2]
        samples.append((4 * C0[0] + 4 * C1[0], 4 * C0[1] + 4 * C1[1]))
        samples.append((C0[0] + 6 * C1[0] + C2[0], C0[1] + 6 * C1[1] + C2[1]))
        samples.append((4 * C1[0] + 4 * C2[0], 4 * C1[1] + 4 * C2[1]))
    ded = [samples[0]]
    for s in samples[1:]:
        if s != ded[-1]:
            ded.append(s)
    return ded


def tangent_keys(samples):
    """Exact integer tangent direction keys between consecutive samples."""
    out = []
    for i in range(len(samples) - 1):
        dx = samples[i + 1][0] - samples[i][0]
        dy = samples[i + 1][1] - samples[i][1]
        k = dir_key(dx, dy)
        if k is not None:
            out.append(k)
    return out


def singvals(mx, my):
    """(sigma1, sigma2) of the 2xd projection — ellipse semi-axis scales."""
    tr = float(dot(mx, mx) + dot(my, my))
    det = area_scale(mx, my) ** 2
    disc = sqrt(max(0.0, tr * tr - 4.0 * det))
    return sqrt(0.5 * (tr + disc)), sqrt(0.5 * (tr - disc))


def snap_point(pts_xy, px, py):
    """Nearest (by real (x, y*sqrt3) float metric) shadow point to (px,py)."""
    best = None
    bx = by = 0
    for X, Y in pts_xy:
        dx = X - px
        dy = Y * SQRT3 - py
        d2 = dx * dx + dy * dy
        if best is None or d2 < best:
            best = d2
            bx, by = X, Y
    return (bx, by), sqrt(best)


# ============================================================== experiment
def run_all():
    L = []
    P = L.append
    P("== SPIN-13 SNAP-SHADOW: multidimensional snapping shadowed to 2D ==")
    P("integer-only core; floats for display/search metrics only")
    P("entries B=%d, seeds %s, dims %s" % (B_ENTRIES, SEEDS, DIMS))
    P("")

    M = {(d, s): proj_matrix(d, s) for d in DIMS for s in SEEDS}

    # ---------------- matrices / theory
    P("== PROJECTIONS (fixed seeded; d=2 = Eisenstein identity canary arm) ==")
    for d in DIMS:
        for s in SEEDS:
            mx, my = M[(d, s)]
            if d == 2:
                P("  d=2 seed=%d  Mx=%s My=%s  (Eisenstein identity)" % (s, mx, my))
            else:
                P("  d=%d seed=%d  Mx=%s My=%s  A=%.2f" % (d, s, mx, my, area_scale(mx, my)))
    P("")

    # ---------------- CANARY A: d=2 reproduction + shell counts
    P("== CANARY A: d_in=2 shadow == direct Eisenstein set ==")
    okA = True
    for N in (6, 24, 128, 1024):
        mx, my = M[(2, 1)]
        dirs2, _ = shadow_scan(mx, my, budget_slice(2, N))
        dref = direct_eis_dirs(N)
        same = dirs2 == dref
        okA &= same
        P("  N=%5d  shadow(d=2)=%5d  direct=%5d  sets-equal=%s" % (N, len(dirs2), len(dref), same))
    shell_counts = {}
    for n2b in (1, 3, 4, 7):
        pts = [p for p in ball(2, n2b) if p[0] <= n2b]
        shell_counts[n2b] = len(pts)
    want = {1: 6, 3: 12, 4: 18, 7: 30}
    okA &= all(shell_counts[k] == want[k] for k in want)
    P("  Eisenstein cumulative shells 6/12/18/30: got %s -> %s"
      % ("/".join(str(shell_counts[k]) for k in (1, 3, 4, 7)),
         "PASS" if all(shell_counts[k] == want[k] for k in want) else "FAIL"))
    P("  CANARY A: %s" % ("PASS" if okA else "FAIL"))
    P("")

    # ---------------- EXP1a: matched point budget
    P("== EXP1a: distinct directed snap angles at MATCHED POINT BUDGET N ==")
    base_dirs = {}
    for N in BUDGETS:
        mx, my = M[(2, 1)]
        base_dirs[N], _ = shadow_scan(mx, my, budget_slice(2, N))
    P("     N |  eis-2D |" + "".join("     d=%d     |" % d for d in DIMS[1:]) + " ratios d3/d4/d6/d8 vs eis")
    exp1a = {}
    for N in BUDGETS:
        row = []
        ratios = []
        for d in DIMS[1:]:
            vals = []
            for s in SEEDS:
                dirs, _ = shadow_scan(*M[(d, s)], budget_slice(d, N))
                vals.append(len(dirs))
            row.append((min(vals), max(vals)))
            ratios.append(0.5 * (min(vals) + max(vals)) / len(base_dirs[N]))
            exp1a[(N, d)] = vals
        P("  %5d | %7d |" % (N, len(base_dirs[N]))
          + "".join(" %5d-%-5d |" % (mn, mx_) for mn, mx_ in row)
          + "  " + "/".join("%.2f" % r for r in ratios))
    P("  (range over seeds %s; eis-2D is the d=2 Eisenstein baseline)" % (SEEDS,))
    P("")

    # ---------------- EXP1b: matched radius
    P("== EXP1b: distinct directed snap angles at MATCHED RADIUS (norm^2 <= b) ==")
    P("   b^2 |  eis-2D |" + "".join("     d=%d     |" % d for d in DIMS[1:]) + " ratios d3/d4/d6/d8 vs eis")
    exp1b = {}
    for n2b in SHELLS:
        eis_dirs, _ = shadow_scan(*M[(2, 1)], [p for p in ball(2, n2b) if p[0] <= n2b])
        row = []
        ratios = []
        for d in DIMS[1:]:
            vals = []
            for s in SEEDS:
                dirs, _ = shadow_scan(*M[(d, s)], [p for p in ball(d, n2b) if p[0] <= n2b])
                vals.append(len(dirs))
            row.append((min(vals), max(vals)))
            ratios.append(0.5 * (min(vals) + max(vals)) / max(1, len(eis_dirs)))
            exp1b[(n2b, d)] = vals
        P("  %5d | %7d |" % (n2b, len(eis_dirs))
          + "".join(" %4d-%-4d  |" % (mn, mx_) for mn, mx_ in row)
          + "  " + "/".join("%.1f" % r for r in ratios))
    P("  NOTE: matched radius = equal coefficient magnitude budget per axis;")
    P("  addressing a point in Z^d costs ~d*log(2R+1) bits vs ~2*log(2R+1).")
    P("")

    # ---------------- EXP2: gap distributions
    P("== EXP2: angular gap stats (degrees), distinct-direction sets ==")
    P("  matched-budget N=1024:")
    for tag, d, s in [("eis-2D", 2, 1)] + [("d=%d s=%d" % (d, s), d, s)
                                            for d in (3, 4, 6, 8) for s in SEEDS]:
        if d == 2:
            dirs, _ = shadow_scan(*M[(2, 1)], budget_slice(2, 1024))
        else:
            dirs, _ = shadow_scan(*M[(d, s)], budget_slice(d, 1024))
        gmin, gmed, gmax, gmean = gap_stats(dirs)
        P("    %-8s dirs=%5d  min=%8.4f  median=%7.4f  max=%7.3f  mean=%7.4f"
          % (tag, len(dirs), gmin, gmed, gmax, gmean))
    P("  matched-radius norm^2 <= %d:" % PRE_BUDGET_SQ)
    pre_stats = {}
    for tag, d, s in [("eis-2D", 2, 1)] + [("d=%d s=%d" % (d, s), d, s)
                                            for d in (3, 4, 6, 8) for s in SEEDS]:
        pts = [p for p in ball(d, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ]
        dirs, _ = shadow_scan(*M[(d, s)], pts) if d != 2 else shadow_scan(*M[(2, 1)], pts)
        gmin, gmed, gmax, gmean = gap_stats(dirs)
        pre_stats[(d, s)] = (len(dirs), gmin, gmed, gmax)
        P("    %-8s dirs=%5d  min=%8.4f  median=%7.4f  max=%7.3f  mean=%7.4f"
          % (tag, len(dirs), gmin, gmed, gmax, gmean))
    P("")

    # ---------------- shared setup for EXP3 (arc, edges, budget-16 candidates)
    ARC_R = 60.0
    ANG0, ANG1 = 15.0, 105.0
    MCTRL = 10
    ctrl_ideal = []
    for i in range(MCTRL):
        th = math.radians(ANG0 + (ANG1 - ANG0) * i / (MCTRL - 1))
        ctrl_ideal.append((ARC_R * math.cos(th), ARC_R * math.sin(th)))
    ideal_edges = []
    for i in range(MCTRL - 1):
        ideal_edges.append((ctrl_ideal[i + 1][0] - ctrl_ideal[i][0],
                            ctrl_ideal[i + 1][1] - ctrl_ideal[i][1]))
    eis_pts = [(2 * a + b, b) for _n2, (a, b) in
               [p for p in ball(2, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ]]
    eis_dirs16, _ = shadow_scan(*M[(2, 1)], [p for p in ball(2, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ])

    # ---------------- EXP3a: point-snap quantization & reach at budget 16
    P("== EXP3a: POINT-SNAP at budget norm^2<=%d — quantization vs reach ==" % PRE_BUDGET_SQ)
    PHI0 = (sqrt(5.0) - 1.0) / 2.0
    gdirs = [(math.cos(math.radians(360.0 * (i + 1) * PHI0)),
              math.sin(math.radians(360.0 * (i + 1) * PHI0))) for i in range(16)]
    s1e, s2e = singvals(*M[(2, 1)])
    P("  eis ball real radius = 2*sqrt(16) = 8.0; shadow reach = ellipse min semi-axis")
    P("  method        | sig1  sig2 | reach | medErr@r=3 | medErr@r=7 | medErr@r=12")
    rows_pt = {}

    def pt_probe(cand):
        meds = []
        for r in (3.0, 7.0, 12.0):
            errs = [snap_point(cand, r * ux, r * uy)[1] for ux, uy in gdirs]
            meds.append(median(errs))
        return meds

    m = pt_probe(list(eis_pts))
    rows_pt["eis"] = (m, 8.0)
    P("  direct-E      | %5.2f %5.2f | %5.1f |   %7.4f   |   %7.4f   |   %7.4f"
      % (s1e, s2e, 8.0, m[0], m[1], m[2]))
    for d in (3, 4, 6, 8):
        seeds = SEEDS if d < 8 else (1,)
        for s in seeds:
            mxv, myv = M[(d, s)]
            pts = [p for p in ball(d, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ]
            cand = [(dot(mxv, z), dot(myv, z)) for _n, z in pts]
            sg1, sg2 = singvals(mxv, myv)
            m = pt_probe(cand)
            rows_pt[(d, s)] = (m, sg2 * 4.0)
            P("  shadow d=%d s=%d | %5.2f %5.2f | %5.1f |   %7.4f   |   %7.4f   |   %7.4f"
              % (d, s, sg1, sg2, sg2 * 4.0, m[0], m[1], m[2]))
    P("  r=3: common-region quantization (both lattices dense there); r=7/r=12")
    P("  expose reach (eis ball ends at radius 8; shadows reach min-axis listed).")
    P("")

    # ---------------- EXP3a2: B-splines over direction-snapped integer polygons
    P("== EXP3a2: quadratic B-splines over DIRECTION-SNAPPED control polygons ==")
    P("  (vertices = cumulative snapped edges; each stored edge z has norm^2 <= %d;" % PRE_BUDGET_SQ)
    P("   exact dyadic B-spline sampling; ideal = R=60 arc 15..105 deg, 10 pts)")
    ideal_turn = (ANG1 - ANG0) / 15.0  # 17 samples -> 16 tangents -> 15 turns

    def dir_snap_polygon(dirs):
        angs = sorted((angle_deg(k), k) for k in dirs)
        avals = [a for a, _ in angs]
        verts = [(0, 0)]
        ang_errs = []
        drift = (0.0, 0.0)
        for ex, ey in ideal_edges:
            ta = degrees(atan2(ey, ex)) % 360.0
            i = bisect.bisect_left(avals, ta)
            cand = []
            for j in ((i - 1) % len(avals), i % len(avals)):
                e = abs(((avals[j] - ta + 180) % 360) - 180)
                cand.append((e, angs[j][1]))
            e, k = min(cand)
            ang_errs.append(e)
            drift = (drift[0] + k[0] - ex, drift[1] + k[1] * SQRT3 - ey)
            verts.append((verts[-1][0] + k[0], verts[-1][1] + k[1]))
        samples = bspline_samples(verts)
        tk = tangent_keys(samples)
        turns = []
        for i in range(len(tk) - 1):
            t = angle_deg(tk[i + 1]) - angle_deg(tk[i])
            turns.append(((t + 180) % 360) - 180)
        med_turn_dev = median([abs(t - ideal_turn) for t in turns]) if turns else 0.0
        turn_jmp = (median([abs(turns[i + 1] - turns[i]) for i in range(len(turns) - 1)])
                    if len(turns) > 1 else 0.0)
        return (median(ang_errs), max(ang_errs), len(set(tk)), len(tk),
                med_turn_dev, turn_jmp, sqrt(drift[0] ** 2 + drift[1] ** 2))

    r = dir_snap_polygon(eis_dirs16)
    P("  direct-E      : medEdgeAngErr=%6.3f max=%6.3f | tangDirs=%3d/%3d medTurnDev=%6.2f turnJmp=%5.2f endDrift=%7.2f"
      % (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
    for d in (3, 4, 6, 8):
        for s in SEEDS:
            pts = [p for p in ball(d, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ]
            dirs, _ = shadow_scan(*M[(d, s)], pts)
            r = dir_snap_polygon(dirs)
            P("  shadow d=%d s=%d: medEdgeAngErr=%6.3f max=%6.3f | tangDirs=%3d/%3d medTurnDev=%6.2f turnJmp=%5.2f endDrift=%7.2f"
              % (d, s, r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
    P("")

    # ---------------- EXP3b: direction-snapped control polygons
    P("== EXP3b: control polygons with EDGE DIRECTIONS snapped at budget norm^2<=%d ==" % PRE_BUDGET_SQ)
    def dir_snap_eval(tag, dirs):
        # nearest direction (float angle) per ideal edge; report angle err,
        # distinct dirs used, endpoint drift with primitive-length edges.
        angs = sorted((angle_deg(k), k) for k in dirs)
        avals = [a for a, _ in angs]
        import bisect
        errs = []
        used = set()
        drift = (0.0, 0.0)
        for ex, ey in ideal_edges:
            ta = degrees(atan2(ey, ex)) % 360.0
            i = bisect.bisect_left(avals, ta)
            cand = []
            for j in ((i - 1) % len(avals), i % len(avals)):
                e = abs(((avals[j] - ta + 180) % 360) - 180)
                cand.append((e, angs[j][1]))
            e, k = min(cand)
            errs.append(e)
            used.add(k)
            real = (k[0], k[1] * SQRT3)
            drift = (drift[0] + real[0] - ex, drift[1] + real[1] - ey)
        drift_norm = sqrt(drift[0] * drift[0] + drift[1] * drift[1])
        # rescaled (angle-isolated) rms
        return median(errs), max(errs), len(used), drift_norm

    md, mxd, ud, dr = dir_snap_eval("eis", eis_dirs16)
    P("  direct-E    : dirs=%5d  medAngErr=%7.3fdeg max=%7.3f  used=%3d  endDrift(primitive-len)=%7.3f"
      % (len(eis_dirs16), md, mxd, ud, dr))
    for d in (3, 4, 6, 8):
        for s in SEEDS:
            pts = [p for p in ball(d, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ]
            dirs, _ = shadow_scan(*M[(d, s)], pts)
            md, mxd, ud, dr = dir_snap_eval("d%d" % d, dirs)
            P("  shadow d=%d s=%d: dirs=%5d  medAngErr=%7.3fdeg max=%7.3f  used=%3d  endDrift(primitive-len)=%7.3f"
              % (d, s, len(dirs), md, mxd, ud, dr))
    P("")

    # ---------------- EXP3c: worked example — unrepresentable angle
    P("== EXP3c: WORKED EXAMPLE — target direction (%d, %d*sqrt3), %.4f deg ==" %
      (TARGET_KEY[0], TARGET_KEY[1], angle_deg(TARGET_KEY)))
    tgt = angle_deg(TARGET_KEY)

    def frontier_str(fr):
        parts = ["best-within-cap err=%.4f" % fr[-1][1]]
        for thr in (30.0, 10.0, 3.0, 1.0, 0.5, 0.25, 0.1, 0.05):
            b = budget_for(fr, thr)
            parts.append("%.2fdeg@n2=%s" % (thr, b))
        return "  ".join(parts)

    fr_eis = err_frontier(*M[(2, 1)], budget_ball(2, 16384), tgt)
    P("  direct-E : %s" % frontier_str(fr_eis))
    for d in (3, 4, 6, 8):
        s = 1
        cap = FRONTIER_CAP[d]
        fr = err_frontier(*M[(d, s)], ball(d, cap), tgt)
        P("  shadow d=%d s=1 (cap %d): %s" % (d, cap, frontier_str(fr)))
        for thr in (1.0, 0.25, 0.05):
            b = budget_for(fr, thr)
            be = budget_for(fr_eis, thr)
            if b and be:
                P("    %.2fdeg: shadow norm^2=%d vs direct norm^2=%d  -> %dx cheaper"
                  % (thr, b, be, be / b))
            else:
                P("    %.2fdeg: shadow=%s direct=%s (within caps)" % (thr, b, be))
    P("")

    # ---------------- EXP3d: unbiased median target error
    P("== EXP3d: UNBIASED precision — 64 golden-ratio targets, budget norm^2<=%d ==" % PRE_BUDGET_SQ)
    PHI = (sqrt(5.0) - 1.0) / 2.0
    targets = [(360.0 * (i + 1) * PHI) % 360.0 for i in range(64)]

    def med_err_over(dirs):
        angs = sorted(angle_deg(k) for k in dirs)
        errs = []
        for t in targets:
            i = bisect.bisect_left(angs, t)
            best = 1e9
            for j in ((i - 1) % len(angs), i % len(angs)):
                e = abs(((angs[j] - t + 180) % 360) - 180)
                best = min(best, e)
            errs.append(best)
        return median(errs), max(errs)

    me, xe = med_err_over(eis_dirs16)
    P("  direct-E    : median err = %7.4f deg   max err = %7.4f deg" % (me, xe))
    for d in (3, 4, 6, 8):
        vals = []
        for s in SEEDS:
            pts = [p for p in ball(d, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ]
            dirs, _ = shadow_scan(*M[(d, s)], pts)
            vals.append(med_err_over(dirs))
        P("  shadow d=%d : median err = %7.4f deg (seeds %s)  gain vs eis = %.1fx"
          % (d, median([v[0] for v in vals]),
             "/".join("%.3f" % v[0] for v in vals), me / median([v[0] for v in vals])))
    P("")

    # ---------------- EXP4: cost table
    P("== EXP4: COST — redundancy, point error, angle gain, reach ==")
    P("    d |   A   |  dirs@8192  | kernel-redund | medAngErr@16 | medPtErr@r3 | reach")
    eis_ang16 = med_err_over(eis_dirs16)[0]
    P("  eis |  1.0  | %8d    |        1.00x  |   %7.4f    |   %7.4f   |  %4.1f"
      % (len(base_dirs[8192]), eis_ang16, rows_pt["eis"][0][0], rows_pt["eis"][1]))
    for d in (3, 4, 6, 8):
        As = [area_scale(*M[(d, s)]) for s in SEEDS]
        dirsN = exp1a[(8192, d)]
        reds = []
        perrs = []
        aerrs = []
        reach = []
        for s in SEEDS:
            mxv, myv = M[(d, s)]
            ptsN = budget_slice(d, 8192)
            _dirs, shpts = shadow_scan(mxv, myv, ptsN)
            reds.append(len(ptsN) / len(shpts))
            if (d, s) in rows_pt:
                perrs.append(rows_pt[(d, s)][0][0])
                reach.append(rows_pt[(d, s)][1])
            pts16 = [p for p in ball(d, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ]
            d16, _ = shadow_scan(mxv, myv, pts16)
            aerrs.append(med_err_over(d16)[0])
        P("  %3d | %5.1f | %5.0f-%-5.0f  |        %.2fx  |   %7.4f    |   %7.4f   |  %4.1f"
          % (d, 0.5 * (min(As) + max(As)), min(dirsN), max(dirsN),
             0.5 * (min(reds) + max(reds)), median(aerrs), median(perrs), median(reach)))
    P("")

    # ---------------- verdict (computed from the measured numbers)
    P("== VERDICT INPUTS ==")
    r8192 = median(exp1a[(8192, 8)]) / len(base_dirs[8192])
    r128 = median(exp1a[(128, 8)]) / len(base_dirs[128])
    eis_med16 = med_err_over(eis_dirs16)[0]
    d8_med16 = median([med_err_over(shadow_scan(*M[(8, s)],
                                                 [p for p in ball(8, PRE_BUDGET_SQ) if p[0] <= PRE_BUDGET_SQ])[0])[0]
                        for s in SEEDS])
    P("  angle-count ratio d=8 @ N=8192 : %.3f  (explosion would need > 1 and growing in d)" % r8192)
    P("  angle-count ratio d=8 @ N=128  : %.3f" % r128)
    P("  unbiased median ang err @16: eis %.4f vs d=8 %.4f -> gain %.1fx"
      % (eis_med16, d8_med16, eis_med16 / d8_med16))
    counts_by_d = [median(exp1a[(8192, d)]) for d in (3, 4, 6, 8)]
    P("  dirs@8192 by d: 3:%d 4:%d 6:%d 8:%d (eis %d)"
      % (counts_by_d[0], counts_by_d[1], counts_by_d[2], counts_by_d[3], len(base_dirs[8192])))
    P("")
    return "\n".join(L)


def main():
    out1 = run_all()
    out2 = run_all()
    det = out1 == out2
    print("== CANARY B: full-suite double-run byte identity: %s ==" % ("PASS" if det else "FAIL"))
    print("")
    print(out1)


if __name__ == "__main__":
    main()
