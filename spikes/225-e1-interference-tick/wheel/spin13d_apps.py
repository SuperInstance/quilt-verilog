#!/usr/bin/env python3
"""
SPIN-13d — ADDENDUM 3: the design contract, demonstrated.

  ENGINEER  owns tolerance + application fit (per-application parameter).
  MECHANIC  owns refinement (shared ops from the common toolkit).
  TOOLKIT   = wheel/anglekit.py — common property, integer-only exact core.

Application A  FINEWIRE spline builder : engineer tolerance 0.01 deg, depth 3
Application B  PILOT heading selector  : engineer tolerance 3.0  deg, depth 1
Both call the SAME toolkit on the SAME seed direction set (Eisenstein
budget-16, 36 directions) — only the engineer's knobs differ.

Canaries: 13b closure-total anchor; select == exhaustive reference on both
tables/tolerances; exact 30-degree balanced bisection; double-run byte
identity (+ external diff run by the operator).
"""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anglekit
from anglekit import angdist, angle_deg, bisect_b, bisect_n, combine

TOL_A = 0.01     # engineer's spec, application A (fine spline)
TOL_B = 3.0      # engineer's spec, application B (coarse heading)
ARC_R = 60.0
ANG0, ANG1 = 15.0, 105.0
MCTRL = 10
PHI = (math.sqrt(5.0) - 1.0) / 2.0


def ideal_edges():
    ctrl = []
    for i in range(MCTRL):
        th = math.radians(ANG0 + (ANG1 - ANG0) * i / (MCTRL - 1))
        ctrl.append((ARC_R * math.cos(th), ARC_R * math.sin(th)))
    return [(ctrl[i + 1][0] - ctrl[i][0], ctrl[i + 1][1] - ctrl[i][1])
            for i in range(MCTRL - 1)]


def edge_angle_deg(e):
    return angle_deg(primitive_of(e))


def primitive_of(e):
    from anglekit import primitive
    return primitive(int(round(e[0] * 64)), int(round(e[1] * 64 / math.sqrt(3))))


def bspline_samples(ctrl):
    samples = []
    for j in range(len(ctrl) - 2):
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
    from anglekit import primitive as prim
    out = []
    for i in range(len(samples) - 1):
        k = prim(samples[i + 1][0] - samples[i][0], samples[i + 1][1] - samples[i][1])
        if k is not None:
            out.append(k)
    return out


def mechanic_refine(table, target, tol):
    """The mechanic's hand tools: shared ops on the bracketing directions
    when the table selection misses the engineer's tolerance."""
    u, v = table.bracket(target)
    cands = [("bisect_b(u,v)", bisect_b(u, v)),
             ("bisect_n(u,v)", bisect_n(u, v)),
             ("combine(u,v,1,2)", combine(u, v, 1, 2)),
             ("combine(u,v,2,1)", combine(u, v, 2, 1)),
             ("combine(u,v,1,1)", combine(u, v, 1, 1)),
             ("combine(u,v,2,-1)", combine(u, v, 2, -1)),
             ("combine(u,v,1,-1)", combine(u, v, 1, -1))]
    best = None
    for name, k in cands:
        if k is None:
            continue
        e = angdist(angle_deg(k), target)
        if best is None or e < best[0]:
            best = (e, name, k)
    return best


def exhaustive_ref(table, t, tol):
    """Independent exhaustive reference: min bits over ALL records."""
    best = None
    for nd in table.nodes:
        if angdist(angle_deg(nd[0]), t) <= tol:
            if best is None or nd[1] < best:
                best = nd[1]
    return best


def run_all():
    L = []
    P = L.append
    P("== SPIN-13d: ENGINEER/Mechanic/Toolkit contract demo ==")
    P("toolkit: anglekit.py | tolerance ALWAYS caller-supplied")
    P("")

    # ---------------- canaries ----------------
    P("== CANARIES ==")
    seeds = anglekit.seed_dirs(2, 1, 16)
    tabA = anglekit.build_table(seeds, depth=3)
    totals = [s[1] for s in tabA.stats()]
    okA = totals == [36, 341, 6012, 32254]
    P("  closure totals == SPIN-13b anchor [36, 341, 6012, 32254]: %s (got %s)"
      % ("PASS" if okA else "FAIL", totals))
    ok30 = bisect_b((2, 0), (1, 1)) == (3, 1) and abs(angle_deg((3, 1)) - 30.0) < 1e-9
    P("  bisect_b((2,0),(1,1)) == (3,1) @ exactly 30 deg: %s" % ("PASS" if ok30 else "FAIL"))
    tabB = anglekit.build_table(seeds, depth=1)
    okS = True
    nchk = 0
    for tab, tol in ((tabA, TOL_A), (tabA, TOL_B), (tabB, TOL_B), (tabB, TOL_A)):
        for i in range(16):
            t = (360.0 * (i + 1) * PHI) % 360.0
            sel = tab.select(t, tol, prefer="bits")
            ref = exhaustive_ref(tab, t, tol)
            nchk += 1
            if (sel is None) != (ref is None):
                okS = False
            elif sel is not None and sel["bits"] != ref:
                okS = False
    P("  select == exhaustive reference (%d checks, 2 tables x 2 tolerances): %s"
      % (nchk, "PASS" if okS else "FAIL"))
    P("")

    # ---------------- shared spec table ----------------
    P("== SHARED TOOLKIT, TWO ENGINEER SPECS ==")
    for tag, tab, tol in (("A FINEWIRE spline", tabA, TOL_A), ("B PILOT heading", tabB, TOL_B)):
        st = tab.stats()
        P("  %s: tolerance %.3f deg (engineer), depth %d, %d entries, payload %d B"
          % (tag, tol, len(st) - 1, st[-1][1], sum(r[2] for r in st)))
    P("")

    # ---------------- application A: FINEWIRE spline builder ----------------
    P("== APP A: FINEWIRE spline builder (engineer tol %.3f deg) ==" % TOL_A)
    edges = ideal_edges()
    verts = [(0, 0)]
    total_bits = 0
    miss = 0
    errs = []
    for e in edges:
        t = math.degrees(math.atan2(e[1], e[0])) % 360.0
        sel = tabA.select(t, TOL_A, prefer="bits")  # legacy policy pinned (13d semantics)
        if sel is None:
            miss += 1
            ref = mechanic_refine(tabA, t, TOL_A)
            P("    edge @ %8.3f deg: table MISS -> mechanic %s -> err %.5f deg %s"
              % (t, ref[1], ref[0], "(within tol)" if ref[0] <= TOL_A else "(STILL OUT)"))
            k = ref[2]
            errs.append(ref[0])
            total_bits += 24  # hand-refined op counted at one op-tree record
        else:
            k = sel["key"]
            errs.append(sel["err_deg"])
            total_bits += sel["bits"]
        verts.append((verts[-1][0] + k[0], verts[-1][1] + k[1]))
    es = sorted(errs)
    med = 0.5 * (es[len(es) // 2 - 1] + es[len(es) // 2])
    tk = tangent_keys(bspline_samples(verts))
    P("  edges=%d  table-miss=%d  medianErr=%.5f deg  maxErr=%.5f deg  totalBits=%d"
      % (len(edges), miss, med, max(errs), total_bits))
    P("  exact B-spline tangents: %d distinct directions" % len(set(tk)))
    P("  all within engineer tolerance: %s" % ("YES" if max(errs) <= TOL_A else "NO"))
    P("")

    # ---------------- application B: PILOT heading selector ----------------
    P("== APP B: PILOT heading selector (engineer tol %.2f deg) ==" % TOL_B)
    legs = [(360.0 * (i + 1) * PHI) % 360.0 for i in range(12)]
    total_bits = 0
    errs = []
    for t in legs:
        sel = tabB.select(t, TOL_B, prefer="bits")  # legacy policy pinned (13d semantics)
        if sel is None:
            P("    heading %8.3f deg: MISS" % t)
            continue
        total_bits += sel["bits"]
        errs.append(sel["err_deg"])
    es = sorted(errs)
    med = es[len(es) // 2]
    P("  headings=%d  medianErr=%.4f deg  maxErr=%.4f deg  totalBits=%d (mean %.1f/leg)"
      % (len(errs), med, max(errs), total_bits, total_bits / max(1, len(errs))))
    P("  all within engineer tolerance: %s" % ("YES" if max(errs) <= TOL_B else "NO"))
    P("")

    # ---------------- the contract, in numbers ----------------
    P("== CONTRACT SUMMARY ==")
    P("  same toolkit, same seed set (36 Eisenstein directions):")
    P("  - engineer A demanded 0.01 deg -> mechanic works at depth 3,")
    P("    ~30-bit constructions, hand-refinement fills table holes;")
    P("  - engineer B demanded 3.0 deg -> depth-1 table suffices,")
    P("    ~6-15-bit constructions, O(1) dense lookups;")
    P("  - refinement ops are identical shared tools in both apps;")
    P("  - tolerance never lives inside the toolkit.")
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
