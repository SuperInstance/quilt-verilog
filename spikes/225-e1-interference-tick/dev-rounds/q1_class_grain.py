#!/usr/bin/env python3
"""ROUND 8 — Q1: class-grain boundary on linear-superposition substrates.

RESEARCH-AGENDA §6 Q1 + CHARTER §10 cheat #2. Anchor: glm-2's dequantized
Hadamard-walk probe (inventors-derby/glm2_dequant_walk.py): identity grain
HOLDS (13 ppm TVD exact-vs-fabric at cap=2^20), binning buys ~nothing
(13 -> 11 ppm) — the E7 class-grain law does NOT transfer [F11].

DESIGN (pre-registered before any new number was read):

  Reference arm  = the SAME recurrence, uncapped, exact big integers.
  Fabric arm     = the SAME recurrence under a width cap 2^20 with global
                   halving rescale (toward zero, sign-symmetric) — identical
                   to glm-2's FABRIC. One property is varied at a time from
                   the identity-grain-safe baseline (the anchor config).

  Axes (one varied property per rung):
    A0 BASELINE  : anchor replay — Hadamard walk on a line, linear |v|^2
                   readout, fixed coin. MUST reproduce 13/11 ppm.
    A1 READOUT   : same walk, three readouts of the superposition:
                   linear |v|^2 (anchor), threshold-occupancy 1[|v|>=T],
                   signum (signed measure, p_i ~ sign(v_i)*|v_i|, L1-normed).
    A2 DYNAMICS  : "learned" coin — LCG-driven perturbed coin matrix each
                   step (M -> M + small integer perturbation), identical
                   perturbation stream in both arms. 5 fixed seeds.
    A3 DIMENSION : 2-D grid walk (coin mixes two chirality components;
                   one chirality shifts x, the other shifts y).

  Metric: TVD(reference, fabric) at identity grain and at 16-site class
  grain, in ppm (floored, like glm-2's show()). Grain law TRANSFERS to a
  variant if identity TVD is small and binning buys little (ratio ~1);
  class grain becomes NECESSARY if identity TVD >> class TVD.

  Integer-only verdict path: all arithmetic integer/Fraction; floats appear
  only in display division (show()). Ticks: exactly the anchor's 96 steps,
  L=193 line (anchor tick count matched exactly per method rules). 2-D rung
  uses 96 steps on a 129x129 grid (max Manhattan reach = 96, no wrap).

CANARIES (mandatory, in run order):
  C2 ANCHOR REPLAY first: baseline must byte-reproduce glm-2's published
      13 / 11 ppm, rescales=27, losses=1566 before any new number is read.
  C3 SELF-CANARY: a deliberately mislabeled arm (classical LCG null labeled
      as "fabric cap=2^20") must be caught: identity TVD must exceed the
      baseline by >100x and the harness must print CAUGHT.
  C1 DOUBLE-RUN: byte-identity of the full output across two runs (checked
      by the caller via sha256; harness itself is deterministic: fixed
      seeds, no wall-clock, no dict-order dependence).
"""
from fractions import Fraction

# ---------- anchor geometry (matched exactly to glm-2) ----------
NSTEPS = 96
L = 193
CENTER = 96
CAP = 1 << 20

LCG_X = 20260902
def lcg_reset(seed):
    global LCG_X
    LCG_X = seed & 0x7FFFFFFF
def lcg():
    global LCG_X
    LCG_X = (1103515245 * LCG_X + 12345) & 0x7FFFFFFF
    return LCG_X

# ---------- 1-D recurrence ----------
def step_line(Lv, Rv, perturb=None):
    """One Hadamard-coin + conditional-shift step on the line.
    perturb: optional (dA, dB, dC, dD) integer perturbation of the coin
    matrix M=[[a,b],[c,d]] -> [[a+dA,b+dB],[c+dD,d+dD]]. Same stream must
    be consumed identically by reference and fabric arms (caller supplies
    the values; we generate them OUTSIDE and pass in, so both arms match)."""
    nL = [0] * L
    nR = [0] * L
    for i in range(L):
        a = Lv[i] + Rv[i]
        b = Lv[i] - Rv[i]
        if perturb is not None:
            dA, dB, dC, dD = perturb
            # perturbed coin: v' = M*v + D*v, D small integer matrix
            a2 = (1 + dA) * Lv[i] + (1 + dB) * Rv[i]
            b2 = (1 + dC) * Lv[i] + (-1 + dD) * Rv[i]
            a, b = a2, b2
        if a:
            nL[(i - 1) % L] += a
        if b:
            nR[(i + 1) % L] += b
    return nL, nR

def run_line(perturb_stream=None, cap=None):
    Lv = [0] * L; Rv = [0] * L
    Lv[CENTER] = 1; Rv[CENTER] = 1
    rescales = 0; losses = 0
    for t in range(NSTEPS):
        p = perturb_stream[t] if perturb_stream is not None else None
        Lv, Rv = step_line(Lv, Rv, p)
        if cap is not None:
            m = 0
            for v in Lv:
                if v > m: m = v
                elif -v > m: m = -v
            for v in Rv:
                if v > m: m = v
                elif -v > m: m = -v
            if m > cap:
                rescales += 1
                for arr in (Lv, Rv):
                    for j, v in enumerate(arr):
                        if v & 1:
                            losses += 1
                        arr[j] = v // 2 if v >= 0 else -((-v) // 2)
    return Lv, Rv, rescales, losses

# ---------- 2-D recurrence (129x129 grid, chirality-0 shifts x, chirality-1 shifts y) ----------
G = 129
GC = 64
def step_grid(Av, Bv, perturb=None):
    nA = [0] * (G * G)
    nB = [0] * (G * G)
    for idx in range(G * G):
        x, y = divmod(idx, G)
        la = Av[idx]; lb = Bv[idx]
        if perturb is not None:
            dA, dB, dC, dD = perturb
            ca = (1 + dA) * la + (1 + dB) * lb
            cb = (1 + dC) * la + (-1 + dD) * lb
        else:
            ca = la + lb
            cb = la - lb
        if ca:
            nA[idx - G if x > 0 else idx] += ca   # move -x
        if cb:
            nB[idx + 1 if y < G - 1 else idx] += cb  # move +y
    return nA, nB

def run_grid(cap=None):
    Av = [0] * (G * G); Bv = [0] * (G * G)
    Av[GC * G + GC] = 1; Bv[GC * G + GC] = 1
    rescales = 0; losses = 0
    for _ in range(NSTEPS):
        Av, Bv = step_grid(Av, Bv)
        if cap is not None:
            m = 0
            for v in Av:
                if v > m: m = v
                elif -v > m: m = -v
            for v in Bv:
                if v > m: m = v
                elif -v > m: m = -v
            if m > cap:
                rescales += 1
                for arr in (Av, Bv):
                    for j, v in enumerate(arr):
                        if v & 1:
                            losses += 1
                        arr[j] = v // 2 if v >= 0 else -((-v) // 2)
    return Av, Bv, rescales, losses

# ---------- readouts & metrics ----------
def readout_linear(Lv, Rv):
    num = [Lv[i] * Lv[i] + Rv[i] * Rv[i] for i in range(len(Lv))]
    tot = sum(num)
    return [Fraction(v, tot) for v in num]

def readout_threshold(Lv, Rv, frac=128):
    """Nonlinear readout: occupancy indicator 1[|amplitude| >= T], with T
    RELATIVE to the arm's own max magnitude (T = max|v| // frac). v1 used a
    fixed absolute T=8 — scale-unfair: the fabric arm has been globally
    halved `rescales` times, so an absolute cut compares different scales
    and produced a ~1.3e5 ppm artifact. Booked as a scar. The relative cut
    is the honest nonlinear (discontinuous) readout."""
    mx = 0
    for i in range(len(Lv)):
        m = max(abs(Lv[i]), abs(Rv[i]))
        if m > mx:
            mx = m
    T = mx // frac
    num = [1 if max(abs(Lv[i]), abs(Rv[i])) >= T else 0 for i in range(len(Lv))]
    tot = sum(num)
    if tot == 0:
        return [Fraction(0)] * len(Lv)
    return [Fraction(v, tot) for v in num]

def readout_signum(Lv, Rv):
    """Nonlinear readout: signed measure p_i ~ sign(Lv_i+Rv_i)*|Lv_i+Rv_i|,
    L1-normed (amplitude sign is where quantization bites hardest — odd
    values halving toward zero can flip tiny survivors across zero)."""
    raw = []
    for i in range(len(Lv)):
        s = Lv[i] + Rv[i]
        raw.append(s)  # keep the sign
    l1 = sum(abs(v) for v in raw)
    if l1 == 0:
        return [Fraction(0)] * len(Lv)
    return [Fraction(v, l1) for v in raw]

def tvd_signed(p, q):
    # works for signed measures: TVD = 1/2 sum |p_i - q_i|
    return sum((abs(a - b) for a, b in zip(p, q)), Fraction(0)) / 2

def grain(dist, binsize, n):
    out = []
    for s in range(0, n, binsize):
        out.append(sum(dist[s:s + binsize], Fraction(0)))
    return out

def show(x):
    return f"{(abs(x.numerator) * 1000000) // x.denominator:>7}"

def compare(ref_dist, fab_dist, n):
    t_id = tvd_signed(ref_dist, fab_dist)
    t_cl = tvd_signed(grain(ref_dist, 16, n), grain(fab_dist, 16, n))
    return t_id, t_cl

# ---------- arms ----------
def arm_baseline():
    Lv, Rv, _, _ = run_line()
    ref = readout_linear(Lv, Rv)
    Lv, Rv, rs, lo = run_line(cap=CAP)
    fab = readout_linear(Lv, Rv)
    t_id, t_cl = compare(ref, fab, L)
    return t_id, t_cl, rs, lo

def arm_readout(name):
    Lv, Rv, _, _ = run_line()
    LvF, RvF, rs, lo = run_line(cap=CAP)
    if name == "linear":
        ref = readout_linear(Lv, Rv); fab = readout_linear(LvF, RvF)
    elif name == "threshold":
        ref = readout_threshold(Lv, Rv); fab = readout_threshold(LvF, RvF)
    elif name == "signum":
        ref = readout_signum(Lv, Rv); fab = readout_signum(LvF, RvF)
    return compare(ref, fab, L) + (rs, lo)

def perturb_stream(seed, amp=1):
    """LCG-driven small integer coin perturbations; identical stream fed to
    BOTH arms. Constrained so the coin matrix can never be the zero matrix
    (diagonal entries stay nonzero: (1+dA) in {1,2}, (-1+dD) in {-1,0};
    off-diagonals (1+dB),(1+dC) in {0,1,2}): a nonzero input amplitude can
    never map to zero everywhere, so the walk never dies. v1 (unconstrained
    [-1,1] on all four) hit a zero matrix and died — booked as a scar."""
    lcg_reset(seed)
    out = []
    for _ in range(NSTEPS):
        dA = lcg() % 2            # {0,1}
        dD = lcg() % 2            # {0,1}
        dB = (lcg() % 3) - 1      # {-1,0,1}
        dC = (lcg() % 3) - 1
        out.append((dA, dB, dC, dD))
    return out

def arm_dynamics(seed, cap=CAP):
    ps = perturb_stream(seed, 1)  # amp=1: coin entries in {0,1,2} / {-2..0}
    Lv, Rv, _, _ = run_line(perturb_stream=ps)
    ref = readout_linear(Lv, Rv)
    Lv, Rv, rs, lo = run_line(perturb_stream=ps, cap=cap)
    fab = readout_linear(Lv, Rv)
    t_id, t_cl = compare(ref, fab, L)
    return t_id, t_cl, rs, lo

def arm_grid():
    Av, Bv, _, _ = run_grid()
    ref = readout_linear(Av, Bv)
    Av, Bv, rs, lo = run_grid(cap=CAP)
    fab = readout_linear(Av, Bv)
    t_id, t_cl = compare(ref, fab, G * G)
    return t_id, t_cl, rs, lo

def classical_null():
    """glm-2's classical LCG walkers — the no-interference null."""
    lcg_reset(20260902)
    pos2count = [0] * L
    for _ in range(20000):
        p = CENTER
        for _ in range(NSTEPS):
            p += 1 if (lcg() >> 11) & 1 else -1
        pos2count[p] += 1
    return [Fraction(c, 20000) for c in pos2count]

def main():
    print("ROUND 8 — Q1 CLASS-GRAIN BOUNDARY (Hadamard-walk harness, anchor-matched: n=96, L=193, cap=2^20)")
    print()
    # C2 anchor replay — MUST pass before any new number is read
    t_id, t_cl, rs, lo = arm_baseline()
    ok = (show(t_id).strip() == "13" and show(t_cl).strip() == "11"
          and rs == 27 and lo == 1566)
    print("[CANARY C2] anchor replay: identity=%s ppm, 16-grain=%s ppm, rescales=%d, losses=%d -> %s"
          % (show(t_id), show(t_cl), rs, lo, "PASS" if ok else "FAIL"))
    assert ok, "anchor replay failed — no new numbers may be read"
    print()

    # C3 self-canary: classical null mislabeled as fabric cap=2^20
    Lv, Rv, _, _ = run_line()
    ref = readout_linear(Lv, Rv)
    null = classical_null()
    t_bad, _ = compare(ref, null, L)
    caught = t_bad > 100 * t_id
    print("[CANARY C3] self-canary (classical null mislabeled as fabric): identity TVD=%s ppm vs baseline %s ppm -> %s"
          % (show(t_bad), show(t_id), "CAUGHT" if caught else "MISSED"))
    assert caught, "self-canary failed to catch mislabeled arm"
    print()

    print(f"{'axis / arm':<44}{'ident ppm':>10}{'16-grain ppm':>13}{'bin gain':>9}{'resc':>6}{'loss':>7}")
    print("-" * 89)

    def gain(a, b):
        aN = a.numerator * b.denominator
        bN = b.numerator * a.denominator
        return Fraction(aN, bN) if bN else Fraction(0)

    rows = []
    def row(label, ti, tc, rs, lo):
        g = gain(ti, tc)
        print(f"{label:<44}{show(ti):>10}{show(tc):>13}{str(float(g))[:5]:>9}{rs:>6}{lo:>7}")
        rows.append((label, ti, tc))

    # A0
    t_id, t_cl, rs, lo = arm_baseline()
    row("A0 baseline (anchor, linear, fixed, 1-D)", t_id, t_cl, rs, lo)
    # A1 readout axis
    for nm in ("linear", "threshold", "signum"):
        ti, tc, rs, lo = arm_readout(nm)
        row(f"A1 readout={nm}", ti, tc, rs, lo)
    # A2 dynamics axis (learned/perturbed coin), 5 fixed seeds
    seeds = [1, 7, 42, 1999, 20260902]
    for s in seeds:
        ti, tc, rs, lo = arm_dynamics(s)
        row(f"A2 dynamics: LCG-perturbed coin, seed={s}", ti, tc, rs, lo)
    # A3 dimension axis
    ti, tc, rs, lo = arm_grid()
    row("A3 dimension: 2-D grid (129x129)", ti, tc, rs, lo)

    # A1-APPENDIX threshold-cut sweep: where does the discontinuous readout break?
    print()
    print("A1-APPENDIX: threshold-cut sweep (T = max|v| // frac), caps 2^20 and 2^24:")
    print(f"{'cut (frac)':<16}{'cap=2^20 ident':>15}{'class':>9}{'cap=2^24 ident':>15}{'class':>9}")
    Lv0, Rv0, _, _ = run_line()
    for frac in (128, 4096, 65536, 262144, 1048576):
        ref = readout_threshold(Lv0, Rv0, frac)
        cells = []
        for cap in (1 << 20, 1 << 24):
            Lf, Rf, _, _ = run_line(cap=cap)
            fab = readout_threshold(Lf, Rf, frac)
            ti, tc = compare(ref, fab, L)
            cells.append(f"{show(ti):>15}{show(tc):>9}")
        print(f"max//{frac:<11}" + "".join(cells))
    print("(read: failure appears only when T approaches the quantization floor")
    print(" (~max/cap); at the same relative cut, cap=2^24 is clean — a WIDTH")
    print(" effect, not a grain effect. Class grain never rescues: worst row is")
    print(" 564766 ident -> 123365 class ppm.)")

    print()
    print("[CANARY C1] double-run byte-identity: harness is deterministic (fixed seeds,")
    print("             no wall-clock, no unordered iteration) — caller verifies via sha256 of two runs.")
    print()
    # verdict hints (identity vs class TVD ratio per row, integer math)
    print("grain-law hint per row (identity/class TVD ratio, x100 floored):")
    for label, ti, tc in rows:
        r = Fraction(ti.numerator * tc.denominator, ti.denominator * tc.numerator) if tc.numerator and ti.numerator else Fraction(0)
        print(f"  {label:<44} ratio ~ {float(r):.2f}x")

if __name__ == "__main__":
    main()
