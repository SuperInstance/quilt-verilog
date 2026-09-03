#!/usr/bin/env python3
"""INVENTION 2 — DEQUANTIZED INTERFERENCE WALK (glm-2 derby entry, 2026-09-02)

Charter §10 cheat #2, testable miniature: "Where the target is interference
STATISTICS, quantized cancellation reproduces the wanted histogram without
unitarity." Plus the E7 grain prediction: class grain transfers, identity
grain doesn't.

Object: the Hadamard quantum walk on a line — the canonical system whose
signature (ballistic two-lobe spread) is PURE interference; a classical
walker of equal step budget is diffusive and cannot produce it.

Three arms, all integer-only:
  EXACT     : the walk's dyadic numerators as exact big integers.
              Amplitude vector after n steps = (integer vector) * 2^(-n/2),
              because H = M / sqrt(2) with M integer. Probability at a site
              is (L^2 + R^2) / 2^(n+1) — never a float.
  FABRIC    : the SAME signed-integer superposition recurrence, but state
              lives under a width cap: whenever max|value| exceeds the cap,
              every value halves (toward zero, sign-symmetric). Odd values
              lose a half-integer — quantized cancellation, logged as loss
              events. Two caps (2^20, 2^10) give a dose-response curve.
  CLASSICAL : LCG coin walkers, no superposition (the no-interference null).

Measure: total-variation distance exact-vs-fabric at identity grain and at
class grain (16-site bins), and the ballistic coefficient var/n^2 for all
three arms. No floats anywhere; rationals via stdlib Fraction (exact).
"""
from fractions import Fraction

LCG_X = 20260902
def lcg():
    global LCG_X
    LCG_X = (1103515245 * LCG_X + 12345) & 0x7FFFFFFF
    return LCG_X

NSTEPS = 96
CENTER = 96
L = 193                    # sites 0..192, center 96, reach +-96: no wrap

def exact_walk():
    Lv = [0] * L
    Rv = [0] * L
    Lv[CENTER] = 1
    Rv[CENTER] = 1         # balanced start; global scale 2^(n/2) implicit
    for _ in range(NSTEPS):
        nL = [0] * L
        nR = [0] * L
        for i in range(L):
            a = Lv[i] + Rv[i]      # Hadamard coin, integer matrix M
            b = Lv[i] - Rv[i]
            if a:
                nL[(i - 1) % L] += a    # shift: left-moving chirality
            if b:
                nR[(i + 1) % L] += b
        Lv, Rv = nL, nR
    norm = sum(v * v for v in Lv) + sum(v * v for v in Rv)
    return [Fraction(Lv[i] * Lv[i] + Rv[i] * Rv[i], norm) for i in range(L)]

def fabric_walk(cap):
    Lv = [0] * L
    Rv = [0] * L
    Lv[CENTER] = 1
    Rv[CENTER] = 1
    rescales = 0
    losses = 0
    for _ in range(NSTEPS):
        nL = [0] * L
        nR = [0] * L
        for i in range(L):
            a = Lv[i] + Rv[i]
            b = Lv[i] - Rv[i]
            if a:
                nL[(i - 1) % L] += a
            if b:
                nR[(i + 1) % L] += b
        Lv, Rv = nL, nR
        m = 0
        for v in Lv:
            if v > m: m = v
            elif -v > m: m = -v
        for v in Rv:
            if v > m: m = v
            elif -v > m: m = -v
        if m > cap:                    # width trip: global halving rescale
            rescales += 1
            for arr in (Lv, Rv):
                for j, v in enumerate(arr):
                    if v & 1:
                        losses += 1
                    arr[j] = v // 2 if v >= 0 else -((-v) // 2)  # toward zero
    norm = sum(v * v for v in Lv) + sum(v * v for v in Rv)
    return ([Fraction(Lv[i] * Lv[i] + Rv[i] * Rv[i], norm) for i in range(L)],
            rescales, losses)

def classical_walk(nwalkers=20000):
    pos2count = [0] * L
    for _ in range(nwalkers):
        p = CENTER
        for _ in range(NSTEPS):
            # NOT the low bit: LCG parity is period-2 (odd mult + odd inc),
            # a low-bit coin sends every walker down one trajectory (var=0).
            p += 1 if (lcg() >> 11) & 1 else -1
        pos2count[p] += 1
    return [Fraction(c, nwalkers) for c in pos2count]

def tvd(p, q):
    return sum((abs(a - b) for a, b in zip(p, q)), Fraction(0)) / 2

def grain(dist, binsize):
    out = []
    for s in range(0, L, binsize):
        out.append(sum(dist[s:s + binsize], Fraction(0)))
    return out

def var(dist):
    mu = sum((i * d for i, d in enumerate(dist)), Fraction(0))
    return sum((d * (i - mu) * (i - mu) for i, d in enumerate(dist)), Fraction(0))

def show(x):
    return f"{(x.numerator * 1000000) // x.denominator:>7}"   # parts per million, floored

if __name__ == "__main__":
    exact = exact_walk()
    norm_check = sum(exact, Fraction(0))
    cl = classical_walk()
    print("DEQUANTIZED INTERFERENCE WALK — Hadamard walk, n =", NSTEPS, "steps, line of", L, "sites")
    print("exact arm normalizes to 1:", norm_check == 1)
    print()
    print(f"{'arm':<22}{'TVD identity (ppm)':>20}{'TVD 16-grain (ppm)':>20}{'var/n^2 (ppm)':>14}{'var/n (ppm)':>12}")
    ve = var(exact)
    print(f"{'EXACT (reference)':<22}{'—':>20}{'—':>20}{show(ve / (NSTEPS * NSTEPS)):>14}{show(ve / NSTEPS):>12}")
    vc = var(cl)
    print(f"{'CLASSICAL (null)':<22}{'—':>20}{'—':>20}{show(vc / (NSTEPS * NSTEPS)):>14}{show(vc / NSTEPS):>12}")
    for cap in (1 << 20, 1 << 10):
        fab, rescales, losses = fabric_walk(cap)
        t_id = tvd(exact, fab)
        t_cl = tvd(grain(exact, 16), grain(fab, 16))
        vf = var(fab)
        name = 'FABRIC cap=2^%d' % (cap.bit_length() - 1)
        print(f"{name:<22}{show(t_id):>20}{show(t_cl):>20}{show(vf / (NSTEPS * NSTEPS)):>14}{show(vf / NSTEPS):>12}"
              f"   rescales={rescales} loss-events={losses}")
    print()
    print("ballistic check (integer): exact var =", ve.numerator, "/", ve.denominator,
          "-> var/n^2 ~", show(ve / (NSTEPS * NSTEPS)), "ppm (ballistic)")
    print("                     classical var =", vc.numerator, "/", vc.denominator,
          "-> var/n ~", show(vc / NSTEPS), "ppm (diffusive, ~1.0 = 1e6 ppm)")
    # lobe structure at class grain: which bins hold mass
    print()
    print("16-site-bin mass (ppm), exact vs fabric-2^10:")
    fab10, _, _ = fabric_walk(1 << 10)
    hdr = "bin:"
    print(" ".join(f"{i:>6}" for i in range(0, 13)))
    print("exa:" + " ".join(show(x) for x in grain(exact, 16)))
    print("fab:" + " ".join(show(x) for x in grain(fab10, 16)))
