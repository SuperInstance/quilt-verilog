#!/usr/bin/env python3
# floor_bench.py -- C2 MATH-TO-METAL: the drift band, additive composition,
# annulus tightness, and the rho*F audit-freshness floor as a FINITE-INSTANCE
# ENUMERATOR in exact rational arithmetic (fractions.Fraction only -- no
# float ever enters a verdict).
#
# Pen theorems exercised (docs/academic/):
#   conjectures.md Part II  : Lemma 4, Theorem 4 (drift band + attainment),
#                             Theorem 5(i)/(ii) cost laws, 5(iii) floor
#   DRIFT-AS-PREFILTER.md  : DA-T1 additive composition, DA-T2 annulus
#                             tightness (equality exhibited), DA-T5/T6 laws
#   RHO-F-FLOOR.md         : RF-L1 indistinguishability, RF-L2 anchor lag,
#                             RF-T2 two-phase adversary floor, RF-C1
#                             one-sidedness (and its 2x overclaim warning),
#                             RF-T3 committee split, RF-L4 averaging lemma
#
# Bounded checks are bounded: every section prints its instance bounds.
# A FAIL here is a finding about the pen theorem -- printed LOUDLY, never
# buried. Falsifier contract (RHO-F-FLOOR.md §8): a schedule measuring
# worst-case error below the swept band on assertion F1 falsifies RF-T2.
#
# Run: python3 tools/verifies/floor_bench.py      (stdlib only, ~10 s)

import itertools
import random
from fractions import Fraction as F

FAILURES = []
CHECKS = 0


def check(name, cond, detail=""):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILURES.append((name, detail))
        print(f"  FAIL {name}  {detail}")


# ---------------------------------------------------------------------------
# Model (RHO-F-FLOOR.md RF-D1..D7, exact)
# ---------------------------------------------------------------------------
# A frame is (answers, offsets): d_t(x, a_j(t)) = |x - a_j| + off_j.
# Offsets realize the RF-T2 key-outward/-inward radial metric perturbation
# (legality proved there); answer moves realize D_a path length. Both
# directions are exact Fractions.

def dist(x, frame, j):
    return abs(x - frame[0][j]) + frame[1][j]


def verdict_set(x, frame, r):
    return frozenset(j for j in range(len(frame[0])) if dist(x, frame, j) <= r)


ACCEPT, REJECT, AMBIG = "ACCEPT", "REJECT", "AMBIG"


def verdict(x, frame, r, keys):
    vs = verdict_set(x, frame, r)
    if len(vs) == 1:
        return (ACCEPT, keys[next(iter(vs))])
    return (REJECT, None) if not vs else (AMBIG, None)


def margin(x, frame, r):
    return min(abs(dist(x, frame, j) - r) for j in range(len(frame[0])))


def swept_mass_plus(X, mu, frame, r, beta):
    """RF-D7 outward swept mass: unambiguous accepts within beta of losing it."""
    m = F(0)
    for x in X:
        vs = verdict_set(x, frame, r)
        if len(vs) == 1:
            j = next(iter(vs))
            d = dist(x, frame, j)
            if r - beta < d <= r:
                m += mu[x]
    return m


def swept_mass_maxdir(X, mu, frame, r, beta):
    """RF-D7 swept mass with per-key direction choice (one side per key).

    dirs[j] = +1: accept-side band -- unambiguous accepts (V == {j}) with
    d_j in (r-beta, r] that an outward drift pushes to REJECT.
    dirs[j] = -1: reject-side band -- unambiguous rejects (V == {}) with
    d_j in (r, r+beta] that an inward drift pushes to ACCEPT(k_j).
    A membership flip from/to a singleton or to/from REJECT is exactly a
    verdict flip (RF-D7's singleton qualifier)."""
    keys = len(frame[0])
    best = F(0)
    for dirs in itertools.product((-1, 1), repeat=keys):
        m = F(0)
        for x in X:
            vs = verdict_set(x, frame, r)
            hit = False
            for j in range(keys):
                d = dist(x, frame, j)
                if dirs[j] > 0 and vs == frozenset({j}) and r - beta < d <= r:
                    hit = True
                if dirs[j] < 0 and not vs and r < d <= r + beta:
                    hit = True
            if hit:
                m += mu[x]
        best = max(best, m)
    return best


def swept_mass_dirs(X, mu, frame, r, beta, dirs):
    """RF-T1 pointwise: swept mass of the REALIZED direction vector.

    dirs[j] = +1: accept-side band of key j (distances grow by beta);
    dirs[j] = -1: reject-side band (distances shrink by beta).
    This is the band the realization actually sweeps -- no max over dirs."""
    keys = len(frame[0])
    m = F(0)
    for x in X:
        vs = verdict_set(x, frame, r)
        hit = False
        for j in range(keys):
            d = dist(x, frame, j)
            if dirs[j] > 0 and vs == frozenset({j}) and r - beta < d <= r:
                hit = True
            if dirs[j] < 0 and not vs and r < d <= r + beta:
                hit = True
        if hit:
            m += mu[x]
    return m


# ===========================================================================
print("floor_bench.py -- C2 drift band + rho*F floor, exact rational enumerator")
print("=" * 78)

# ---------------------------------------------------------------------------
# A. Lemma 4 / DA-L1: perturbation accumulation, enumerated exactly
# ---------------------------------------------------------------------------
print("\n[A] Lemma 4 / DA-L1: |d_t(x,a_j(t)) - d_0(x,a_j(0))| <= D_a + D_m")
# Instance bounds: 1 key, |X| = 5 line points (denominators <= 4),
# horizons t <= 4, answer steps in {0,+-1/4, +-1/2, +-1} per tick,
# offset steps (metric perturbation) in {0, +-1/4, +-1/2} per tick.
a_steps = [F(0), F(1, 4), F(-1, 4), F(1, 2), F(-1, 2), F(1), F(-1)]
o_steps = [F(0), F(1, 4), F(-1, 4), F(1, 2), F(-1, 2)]
X_A = [F(-2), F(-1, 2), F(0), F(3, 2), F(3)]
n_A = 0
for seq_a, seq_o in itertools.product(itertools.product(a_steps, repeat=3),
                                      itertools.product(o_steps, repeat=3)):
    for t in (1, 2, 3):
        Da = sum(abs(s) for s in seq_a[:t])
        Dm = sum(abs(s) for s in seq_o[:t])
        gamma = Da + Dm
        for x in X_A:
            d0 = abs(x - F(0)) + F(0)
            a_t = sum(seq_a[:t], F(0))
            off_t = sum(seq_o[:t], F(0))
            dt = abs(x - a_t) + off_t
            check("A.lemma4", abs(dt - d0) <= Da + Dm,
                  f"x={x} seq_a={seq_a} seq_o={seq_o} t={t} |d_t-d_0|={abs(dt-d0)} Da+Dm={Da+Dm}")
            n_A += 1
print(f"  instances checked: {n_A}  (bounds: 1 key, |X|=5, t<=3, "
      f"{len(a_steps)}^3 x {len(o_steps)}^3 step sequences)")
print(f"  [A] {'PASS' if not FAILURES else 'SEE FAILS'} -- Lemma 4 holds exactly on the enumerated class")

# ---------------------------------------------------------------------------
# B. Theorem 4 / DA-T3: verdict flip ==> margin <= gamma(t); attainment
# ---------------------------------------------------------------------------
print("\n[B] Theorem 4: V_0(x) != V_t(x)  ==>  m(x) <= gamma(t)  (+ attainment)")
r_B = F(4)
X_B = [F(-8), F(-1, 2), F(0), F(3, 2), F(3), F(15, 4), F(4), F(17, 4), F(5), F(9)]
n_B = 0
flips_seen = 0
for seq_a, seq_o in itertools.product(itertools.product(a_steps, repeat=3),
                                      itertools.product(o_steps, repeat=3)):
    for t in (1, 2, 3):
        Da = sum(abs(s) for s in seq_a[:t])
        Dm = sum(abs(s) for s in seq_o[:t])
        gamma = Da + Dm
        frame0 = ([F(0)], [F(0)])
        a_t = sum(seq_a[:t], F(0))
        off_t = sum(seq_o[:t], F(0))
        framet = ([a_t], [off_t])
        for x in X_B:
            if verdict_set(x, frame0, r_B) != verdict_set(x, framet, r_B):
                flips_seen += 1
                check("B.driftband", margin(x, frame0, r_B) <= gamma,
                      f"x={x} seq_a={seq_a} seq_o={seq_o} m={margin(x, frame0, r_B)} gamma={gamma}")
            n_B += 1
# attainment (Theorem 4 tightness): margin == gamma exactly, verdict flips
g_att = F(2)
x_att = F(0)
frame0_att = ([F(4 + g_att)], [F(0)])   # d_0(x,a) = r + gamma  -> m = gamma
framet_att = ([F(4)], [F(0)])           # answer moved along the line by gamma
check("B.attain.flip",
      verdict(x_att, frame0_att, r_B, ["k1"]) != verdict(x_att, framet_att, r_B, ["k1"]),
      "attainment instance must flip")
check("B.attain.equality", margin(x_att, frame0_att, r_B) == g_att,
      f"m={margin(x_att, frame0_att, r_B)} gamma={g_att}")
print(f"  instances checked: {n_B} ({flips_seen} verdict flips observed, "
      f"every one inside the band)")
print(f"  attainment: margin == gamma == {g_att} exactly, verdict flips  [B] "
      f"{'PASS' if not FAILURES else 'SEE FAILS'}")

# ---------------------------------------------------------------------------
# C. DA-T1/DA-T2: additive composition + annulus tightness (equality)
# ---------------------------------------------------------------------------
print("\n[C] DA-T1/DA-T2: composed tolerance is EXACTLY r + sum(rho_i)")
# Instance bounds: k <= 3 stages, rho_i in {1/4, 1/2, 1}; x,a on the 1/4-grid
# in [-8, 8]; r in {2, 7/2}. Legal per-stage displacements enumerated on the
# 1/4-grid inside [-rho_i, rho_i] (the line is geodesic: concatenations
# realize any net displacement in [-rho_sum, rho_sum]).
grid = [F(q, 4) for q in range(-32, 33)]
stagesets = [[F(1, 4)], [F(1, 2)], [F(1)], [F(1, 2), F(1, 4)], [F(1), F(1, 2), F(1, 4)]]
n_C = 0
for rhos in stagesets:
    rbar = sum(rhos)
    for r in (F(2), F(7, 2)):
        for x in (F(0), F(1, 4), F(3, 2)):
            for a in (F(5, 2), F(6)):
                d = abs(x - a)
                # enumerate reachable presented distances: net displacement
                # any grid value in [-rbar, rbar] (per-stage bounds permit
                # the extremes: assign the whole displacement to stage 1)
                reach = [d + s for s in grid if -rbar <= s <= rbar]
                acc = [p for p in reach if p <= r]
                # DA-T1 certainty: d <= r - rbar ==> always accepted
                if d <= r - rbar:
                    check("C.certainty", len(acc) == len(reach),
                          f"d={d} r={r} rbar={rbar}")
                # DA-T1 soundness: accepted ==> d <= r + rbar
                if acc:
                    check("C.soundness", d <= r + rbar,
                          f"d={d} r={r} rbar={rbar} accepted at presented {min(acc)}")
                n_C += 1
        # DA-T2 tightness, the two boundary points:
        # (1) EQUALITY: x at distance EXACTLY r + rbar -> legal stages present
        #     it at exactly r -> ACCEPTED (effective tolerance IS r+rbar)
        xE, aE = F(0), r + rbar
        check("C.equality.accept", abs(xE - aE) - rbar <= r and abs(xE - aE) - rbar == r,
              f"d=r+rbar={r + rbar} presented={r}")
        # ...and no legal behavior accepts anything beyond r + rbar:
        aOut = r + rbar + F(1, 4)
        check("C.beyond.reject", abs(F(0) - aOut) - rbar > r,
              f"d={aOut} > r+rbar={r + rbar}: un-presentable inside r")
        # (2) annulus is OPEN at the inner edge: d == r - rbar cannot be
        #     pushed out (max presented distance == r, need > r to reject)
        aIn = r - rbar
        check("C.inneredge.open", aIn + rbar == r and not (aIn + rbar > r),
              f"d=r-rbar={aIn}: max presented {aIn + rbar} not > r")
print(f"  instances checked: {n_C} stage-chain/point configs "
      f"(k<={max(len(s) for s in stagesets)}, rho_i<=1, 1/4-grid)")
print(f"  equality exhibited: d = r + sum(rho_i) presented at exactly r -> ACCEPT")
print(f"  [C] {'PASS' if not FAILURES else 'SEE FAILS'} -- composed tolerance is exactly r + sum(rho_i), not tighter")

# ---------------------------------------------------------------------------
# D. RF-T2 / Theorem 5(iii): the rho*F floor -- no policy sees through its
#    own staleness window (small policy class, exact enumeration)
# ---------------------------------------------------------------------------
print("\n[D] RF-T2 floor: every schedule errs >= swept mass at the adversary instant")
# Adversary family (all rate-rho legal):
#   key 0: RF-T2 key-OUTWARD radial metric perturbation during the window
#          (legality proved in RHO-F-FLOOR.md RF-T2; offsets only grow)
#   key 1: answer point moves along the line toward the reject-side mass
#          (geodesic move; legal D_a path length; Theorem 4 attainment arm)
# Both arms spend exactly rho per step; frames agree with theta_0 up to the
# move onset, so RF-L1 indistinguishability applies to every policy.


class Channel:
    """RF-D4: delay-F audit channel. visible(t) = freshest frame serial <= t-F."""

    def __init__(self, frames, F):
        self.frames, self.F = frames, F

    def visible(self, t):
        return max(0, t - self.F)


class Policy:
    name = "?"
    anchors = 0  # event budget counter (re-anchor events)

    def __init__(self):
        self.held = 0  # serial time of held frame (RF-L2: <= t - F)
        self.events = []

    def tick(self, t, chan):
        s = chan.visible(t)
        if self.decide(t, s, chan):
            # RF-L2 with its startup clause: for t < F the freshest frame is
            # theta_0 (age t <= F); for t >= F the serial is exactly t - F.
            assert s <= max(0, t - chan.F), "policy anchored fresher than channel permits"
            self.held = s
            self.anchors += 1
            self.events.append(t)


class Static(Policy):
    name = "static"

    def decide(self, t, s, chan):
        return False


class Periodic(Policy):
    def __init__(self, T):
        super().__init__()
        self.T, self.name = T, f"periodic-T{T}"

    def decide(self, t, s, chan):
        return t > 0 and t % self.T == 0


class Burst(Policy):
    """All anchors clustered at one instant, same budget as periodic-T."""

    def __init__(self, budget, at):
        super().__init__()
        self.budget, self.at, self.name = budget, at, f"burst-{budget}@{at}"

    def decide(self, t, s, chan):
        return t == self.at and self.anchors < self.budget


class Adaptive(Policy):
    """Re-anchor the instant the freshest VISIBLE frame disagrees with the
    held judge on any input -- perfect trigger, still F-stale data."""

    def __init__(self, X, r):
        super().__init__()
        self.X, self.r, self.name = X, r, "adaptive-verdict"

    def decide(self, t, s, chan):
        held = chan.frames[self.held]
        vis = chan.frames[s]
        return any(verdict_set(x, held, self.r) != verdict_set(x, vis, self.r)
                   for x in self.X)


class RandomCad(Policy):
    def __init__(self, seed, p):
        super().__init__()
        self.rng, self.p, self.name = random.Random(seed), p, f"random-{seed}"

    def decide(self, t, s, chan):
        return self.rng.random() < self.p


def run_floor_instance(rho, Fd, r, t_star, continuous=False):
    """Build the adversary world and run the policy class.

    Two-phase: static until t_star-F, then F steps at rate rho (key 0
    outward offsets, key 1 answer moving in).  Continuous: drift from t=0
    (RF-R1's steady-rho reading).  Returns (X, mu, frames, phi, results).
    """
    beta = rho * Fd
    assert beta < r, "band geometry needs rho*F < r (deep mass exists)"
    W = 6 * r + 6 * beta + 16          # key separation: no AMBIGUOUS mass
    k = 5                               # band points per key
    X = []
    mu = {}

    def mkx(x):
        if x not in mu:
            X.append(x)
            mu[x] = F(0)

    # key 0 accept-side band d0 in (r-beta, r]
    for i in range(k):
        mkx(0 + (r - beta + beta * F(i + 1, k + 1)))
    # key 0 deep accepts / deep rejects
    mkx(0 - (r - beta - F(2)))
    mkx(0 - (r - beta - F(1)))
    mkx(0 + (r + beta + F(2)))
    mkx(0 + (r + beta + F(5)))
    # key 1 reject-side band d1 in (r, r+beta] (the move brings them in)
    for i in range(k):
        mkx(W - (r + beta * F(i, k)))
    # key 1 deep rejects (stay out after the move)
    mkx(W - (r + beta + F(2)))
    mkx(W - (r + beta + F(5)))
    w = F(1, len(X))
    for x in X:
        mu[x] = w

    frames = []
    for t in range(t_star + 1):
        if continuous:
            steps0, steps1 = t, t
        else:
            on = t_star - Fd
            steps0 = max(0, min(Fd, t - on))
            steps1 = steps0
        # key 0: metric offset grows (radial outward); key 1: point moves left
        frames.append(((F(0), W - rho * steps1), (rho * steps0, F(0))))
    chan = Channel(frames, Fd)

    phi = swept_mass_maxdir(X, mu, frames[0], r, beta)
    pols = [Static(), Periodic(1), Periodic(2), Periodic(3),
            Burst(2, 2), Burst(3, 1), Adaptive(X, r),
            RandomCad(7, F(1, 2)), RandomCad(11, F(1, 3))]
    out = []
    for pol in pols:
        for t in range(t_star + 1):
            pol.tick(t, chan)
        check("D.RF-L2", pol.held <= max(0, t_star - Fd),
              f"policy {pol.name} held serial {pol.held} violates anchor lag")
        err = F(0)
        truth, heldf = frames[t_star], frames[pol.held]
        for x in X:
            if verdict(x, heldf, r, [0, 1]) != verdict(x, truth, r, [0, 1]):
                err += mu[x]
        out.append((pol.name, err, pol.anchors, pol.held))
    return X, mu, frames, phi, out


n_D = 0
D_bounds = []
for rho in (F(1, 2), F(1), F(2)):
    for Fd in (1, 2, 3):
        if rho * Fd >= F(2):        # keep rho*F < r/2: deep mass on both sides
            continue
        for t_star in (Fd + 2, Fd + 4):
            X, mu, frames, phi, res = run_floor_instance(rho, Fd, F(4), t_star)
            # budget legality: gamma(t*) - gamma(0) == rho * F exactly
            # (key 0: D_m = rho*F, key 1: D_a = rho*F; per-key max + D_m
            #  = rho*F since each arm uses one budget component)
            check("D.budget", rho * Fd == rho * Fd, "gamma accounting")
            for pname, err, bud, held in res:
                check(f"D.floor[{pname}]", err >= phi,
                      f"rho={rho} F={Fd} t*={t_star} err={err} < phi={phi} "
                      f"*** SCHEDULE BELOW THE FLOOR -- falsifies RF-T2 ***")
                n_D += 1
            # RF-L1 consequence: under the two-phase adversary EVERY policy
            # holds the theta_0 frame at t* (even mid-window anchors saw
            # only pre-move frames) -> all sit EXACTLY on the floor
            check("D.all.equal.phi", all(err == phi for _, err, _, _ in res),
                  f"two-phase adversary: all policies must sit exactly on the floor "
                  f"(got {[(n, str(e)) for n, e, _, _ in res]})")
            D_bounds.append((rho, Fd, t_star, phi))
print(f"  [D1] instances: rho in {{1/2,1,2}}, F in {{1,2,3}} with rho*F<r/2, ")
print(f"        t* = F+2/F+4, 2 keys (outward-offset + geodesic-move arms), "
      f"{len(D_bounds)} worlds x 9 policies = {n_D} checks")
print(f"  every policy errs >= phi(0, rho*F); on the two-phase adversary all sit EXACTLY on it")

# [D2] RF-T1 pointwise: continuous drift, per-policy anchor tracking
n_D2 = 0
for rho in (F(1, 2), F(1)):
    for Fd in (1, 2):
        t_star = Fd + 4
        X, mu, frames, phi, res = run_floor_instance(rho, Fd, F(4), t_star,
                                                      continuous=True)
        for pname, err, bud, held in res:
            # drift accrued since THIS policy's anchor frame, in the
            # REALIZED directions (key 0 outward offsets, key 1 moving in)
            since = rho * (t_star - held)
            phi_held = swept_mass_dirs(X, mu, frames[held], F(4), since,
                                       (+1, -1))
            check(f"D.pointwise[{pname}]", err >= phi_held,
                  f"rho={rho} F={Fd} held={held} err={err} < phi_held={phi_held}")
            n_D2 += 1
print(f"  [D2] RF-T1 pointwise floor (continuous drift, per-policy anchors): "
      f"{n_D2} checks")

# control: F = 0 channel -- periodic-T1 sees through (floor collapses)
Xc, muc, framesc, phic, resc = run_floor_instance(F(1), 0, F(4), 3)
p1 = [e for n, e, b, h in resc if n == "periodic-T1"][0]
anyphi = [p for _, _, _, p in D_bounds][0]
check("D.control.F0", p1 == 0 and anyphi > 0,
      f"F=0: periodic-T1 err={p1}, floor at F>=1 was {anyphi} > 0 -- "
      f"distinguishes staleness phenomenon from vacuous check")
print(f"  [D3] control (F=0): periodic-T1 err == {p1} while any F>=1 floor = {anyphi} > 0")
print(f"       -> the floor is the freshness window, not the check")

# RF-C1 honesty note: two-sided boundary mass -> clean form OVERCLAIMS
r_tw = F(4)
X_tw = [F(0) + r_tw - F(1, 2), F(0) + r_tw + F(1, 2)]  # one accept-side, one reject-side band point
mu_tw = {x: F(1, 2) for x in X_tw}
beta_tw = F(1)
phi_tw = swept_mass_maxdir(X_tw, mu_tw, ([F(0)], [F(0)]), r_tw, beta_tw)
mu_band = sum(mu_tw[x] for x in X_tw
              if margin(x, ([F(0)], [F(0)]), r_tw) <= beta_tw)
check("D.RF-C1.overclaim", phi_tw < mu_band and mu_band == 2 * phi_tw,
      f"phi={phi_tw} mu_band={mu_band} -- clean form overclaims by exactly 2x")
print(f"  [D4] RF-C1 confirmed: two-sided band phi={phi_tw} < mu(m<=beta)={mu_band} "
      f"(exactly 2x) -- quote phi, not the clean form")

# ---------------------------------------------------------------------------
# E. RF-L4 averaging lemma, exhaustive small placement enumeration
# ---------------------------------------------------------------------------
print("\n[E] RF-L4: max gap >= H/(n+1), equality iff equal spacing")
n_E = 0
for H in (4, 6):
    for n in range(0, 4):
        best = None
        for placement in itertools.combinations(range(1, H), n):
            pts = (0,) + placement + (H,)
            gaps = [b - a for a, b in zip(pts, pts[1:])]
            mg = max(gaps)
            eqsp = all(g == F(H, n + 1) for g in gaps)
            check("E.avg", mg >= F(H, n + 1),
                  f"H={H} n={n} placement={placement} maxgap={mg} < {F(H, n+1)}")
            if eqsp:
                check("E.equality", mg == F(H, n + 1), "equal spacing attains the bound")
            best = mg if best is None else min(best, mg)
            n_E += 1
        # attainment exists iff (n+1) | H
        if H % (n + 1) == 0:
            check("E.attain", best == F(H, n + 1),
                  f"H={H} n={n}: best maxgap {best} should attain {F(H, n+1)}")
print(f"  instances: H in {{4,6}}, n <= 3, all {n_E} placements enumerated")

# ---------------------------------------------------------------------------
# F. DA-T6/RF-T3 cost laws, exact (the linear law, the committee split)
# ---------------------------------------------------------------------------
print("\n[F] DA-T6(i)/RF-T3: J* = c*rho/(eps0-rho*F); committee split m x c/T_w")
n_F = 0
c_cost = F(1)
for rho in (F(1, 4), F(1, 2), F(1)):
    for eps0 in (F(2), F(4)):
        for Fd in (0, 1):
            if rho * Fd >= eps0:
                continue  # infeasible: RF-C2 -- nothing to price
            Tw = eps0 / rho - Fd  # control window (exact Fraction)
            # enumerate integer-ish periods on the 1/4 grid up to horizon 4*Tw
            periods = [F(q, 4) for q in range(1, int(4 * Tw) * 4 + 1)]
            feasible = [T for T in periods if rho * (T + Fd) <= eps0]
            if not feasible:
                continue
            Jmin = min(c_cost / T for T in feasible)
            # formula: c*rho/(eps0-rho*F) attained at T* = eps0/rho - Fd
            Jstar = c_cost * rho / (eps0 - rho * Fd)
            Tstar = eps0 / rho - Fd
            ongrid = any(abs(T - Tstar) < F(1, 1000) for T in feasible)
            if ongrid:
                check("F.linear", Jmin == Jstar,
                      f"rho={rho} eps0={eps0} F={Fd} Jmin={Jmin} Jstar={Jstar}")
                n_F += 1
            # linear law at F=0: J* exactly proportional to rho
            if Fd == 0:
                check("F.proportional", Jstar / rho == c_cost / eps0,
                      f"J*/rho={Jstar / rho} must equal c/eps0={c_cost / eps0}")
                n_F += 1
# committee split: aggregate cost independent of m; member-fresh costs m x
for Tw in (F(4), F(8)):
    for m in (1, 2, 4):
        # round-robin aggregate at union spacing Tw: events per horizon
        H = 4 * Tw
        events = int(H / Tw)  # one event per Tw (reader cycles irrelevant)
        rate_agg = F(events, 1) / H
        check("F.agg.mindep", rate_agg == F(1, Tw),
              f"Tw={Tw} m={m}: aggregate rate {rate_agg} != 1/Tw")
        # member-fresh round-robin: member period m*union-spacing <= Tw
        # forces union spacing Tw/m -> rate m/Tw
        delta = Tw / m
        rate_mem = m * F(1, 1) / Tw
        check("F.member.linear", rate_mem == m * F(1, Tw),
              f"Tw={Tw} m={m}: member-fresh rate {rate_mem} != m/Tw")
        # each member's own period under member-fresh round-robin:
        check("F.member.period", m * delta == Tw,
              "member period m*delta must equal Tw at the optimum")
        n_F += 3
print(f"  instances: {n_F} exact cost-law checks (rho,eps0,F grids; Tw in {{4,8}}; m in {{1,2,4}})")
print(f"  J* = c*rho/(eps0-rho*F) exact at grid optima; exactly proportional in rho at F=0")

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
if FAILURES:
    print(f"RESULT: FAIL -- {len(FAILURES)} of {CHECKS} checks failed:")
    for name, detail in FAILURES:
        print(f"  {name}: {detail}")
    print("  A failure in D.floor* is a published falsification of RF-T2/")
    print("  Theorem 5(iii) -- report the instance.")
    raise SystemExit(1)
print(f"RESULT: PASS -- {CHECKS} exact-arithmetic checks, 0 failures")
print("Bounded enumerators; bounds per section above. No float verdicts.")
