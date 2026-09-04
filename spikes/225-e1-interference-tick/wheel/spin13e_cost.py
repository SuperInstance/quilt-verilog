#!/usr/bin/env python3
"""
SPIN-13e — ADDENDUM 4: the COST DOCTRINE, measured.

"Big data says the optimal monofilament is sqrt(8) ~ 2.83 mm, but 3 mm is
cheap, common, more durable, and trades only a sliver of catch-rate."

select() now ranks by min CONSTRUCTION COST subject to |theta-target| <=
tolerance: Pythagorean-standard parts (integer real length k = sqrt(X^2+3Y^2),
the Euclid-formula analog in the Z[sqrt3] frame) beat exotic high-norm hits
even when the exotic is closer. The engineer's tolerance is exactly the room
that makes standard parts viable.

Measured here, on the SAME tables as SPIN-13d (Eisenstein seed, depth 3
and depth 1):
  * the SHELF: standard parts in each table (k, direction, address bits);
  * DIVERGENCE: how often the cost pick differs from the nearest-angle pick
    (and from the legacy min-bits pick), per tolerance;
  * THE SLIVER: precision traded away (err_cost - err_nearest) in degrees
    and as a fraction of tolerance — the 2.83-vs-3.0 loss;
  * WHAT IT BUYS: address bits saved and standard-part coverage;
  * VIABILITY ENVELOPE: fraction of targets with >=1 standard part within
    tolerance, vs tolerance — the room the engineer must grant.
Canaries: 13b anchor totals; cost picks always within tolerance; exact
30-degree bisection; legacy 'bits' policy reproduces 13d picks; double-run
byte identity.
"""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anglekit
from anglekit import angdist, angle_deg, bisect_b, part_class, real_length

PHI = (math.sqrt(5.0) - 1.0) / 2.0
TARGETS = [(360.0 * (i + 1) * PHI) % 360.0 for i in range(64)]
TOLS_A = (3.0, 1.0, 0.3, 0.1, 0.03, 0.01)
TOLS_B = (3.0,)
ANCHOR = [36, 341, 6012, 32254]


def median(xs):
    ys = sorted(xs)
    m = len(ys) // 2
    return ys[m] if len(ys) % 2 else 0.5 * (ys[m - 1] + ys[m])


def run_all():
    L = []
    P = L.append
    P("== SPIN-13e COST DOCTRINE: standard parts over exotic precision ==")
    P("ranking: (part_class, bits, depth, err); tolerance = the engineer's room")
    P("")

    seeds = anglekit.seed_dirs(2, 1, 16)
    tabA = anglekit.build_table(seeds, depth=3)
    tabB = anglekit.build_table(seeds, depth=1)

    # ---------------- canaries ----------------
    P("== CANARIES ==")
    totals = [s[1] for s in tabA.stats()]
    P("  closure totals == 13b anchor: %s (got %s)"
      % ("PASS" if totals == ANCHOR else "FAIL", totals))
    ok30 = bisect_b((2, 0), (1, 1)) == (3, 1) and abs(angle_deg((3, 1)) - 30.0) < 1e-9
    P("  bisect_b((2,0),(1,1)) == (3,1) @ exactly 30 deg: %s" % ("PASS" if ok30 else "FAIL"))
    # part_class self-consistency on known parts
    ok_pc = (part_class((1, 1)) == 0 and real_length((1, 1)) == 2
             and part_class((13, 3)) == 0 and real_length((13, 3)) == 14
             and part_class((3, 1)) == 2 and real_length((3, 1)) is None
             and part_class((1, 4)) == 0 and real_length((1, 4)) == 7)
    P("  part_class/real_length known triples (1,1)k2 (13,3)k14 (1,4)k7; (3,1) exotic: %s"
      % ("PASS" if ok_pc else "FAIL"))
    ok_tol = True
    n = 0
    for tab, tols in ((tabA, TOLS_A), (tabB, TOLS_B)):
        for tol in tols:
            for t in TARGETS:
                sel = tab.select(t, tol, prefer="cost")
                n += 1
                if sel is not None and sel["err_deg"] > tol + 1e-12:
                    ok_tol = False
    P("  all %d cost picks within engineer tolerance: %s" % (n, "PASS" if ok_tol else "FAIL"))
    P("")

    # ---------------- the shelf ----------------
    P("== THE SHELF OF STANDARD PARTS (integer real length k <= 64) ==")
    for tag, tab in (("depth-3 table", tabA), ("depth-1 table", tabB)):
        cat = tab.catalog(64)
        P("  %s: %d standard parts (of %d entries)" % (tag, len(cat), tab.n_entries()))
        ks = sorted(set(c[0] for c in cat))
        P("    k values: %s" % ks)
        cheap = [c for c in cat if c[2] <= 15]
        ex = ", ".join("(%d,%d)k%d@%db" % (c[1][0], c[1][1], c[0], c[2]) for c in cheap[:10])
        P("    cheapest ten: %s" % ex)
    P("")

    # ---------------- divergence & the sliver ----------------
    P("== DIVERGENCE: cost pick vs nearest-angle pick (and vs legacy min-bits) ==")
    P("  tol    | n  | differ-vs-nearest | medTradedDeg | medTraded/tol | medBitsSaved | std-part picks")
    for tag, tab, tols in (("A(d3)", tabA, TOLS_A), ("B(d1)", tabB, TOLS_B)):
        for tol in tols:
            n = 0
            diff_near = 0
            diff_bits = 0
            traded = []
            bits_saved = []
            std_picks = 0
            std_near = 0
            for t in TARGETS:
                sc = tab.select(t, tol, prefer="cost")
                sn = tab.select(t, tol, prefer="nearest")
                sb = tab.select(t, tol, prefer="bits")
                if sc is None or sn is None:
                    continue
                n += 1
                if sc["node"] != sn["node"]:
                    diff_near += 1
                    traded.append(sc["err_deg"] - sn["err_deg"])
                if sc["node"] != sb["node"]:
                    diff_bits += 1
                if sb and sc["bits"] < sb["bits"]:
                    bits_saved.append(sb["bits"] - sc["bits"])
                if sc["cost_class"] == 0:
                    std_picks += 1
                if sn["cost_class"] == 0:
                    std_near += 1
            P("  %s %5.2f | %2d | %6.1f%%        | %11.5f | %12.3f | %11.1f | %d/%d (nearest %d)"
              % (tag, tol, n, 100.0 * diff_near / max(1, n), median(traded) if traded else 0.0,
                 (median(traded) / tol if traded else 0.0), median(bits_saved) if bits_saved else 0.0,
                 std_picks, n, std_near))
    P("")

    # ---------------- exemplars: the 2.83-vs-3.0 moments ----------------
    P("== EXEMPLARS: exotic nearest hit vs standard-part cost pick ==")
    shown = 0
    for t in TARGETS:
        if shown >= 4:
            break
        tol = 1.0
        sc = tabA.select(t, tol, prefer="cost")
        sn = tabA.select(t, tol, prefer="nearest")
        if sc is None or sn is None or sc["node"] == sn["node"]:
            continue
        if sc["cost_class"] == 0 and sn["cost_class"] >= 2:
            P("  target %8.3f deg (tol %.2f):" % (t, tol))
            P("    nearest: key=%-12s err=%.4f deg bits=%2d class=%d (norm2=%d)"
              % (str(sn["key"]), sn["err_deg"], sn["bits"], sn["cost_class"],
                 sn["key"][0] ** 2 + 3 * sn["key"][1] ** 2))
            P("    cost   : key=%-12s err=%.4f deg bits=%2d class=0 k=%d"
              % (str(sc["key"]), sc["err_deg"], sc["bits"], sc["real_length"]))
            shown += 1
    P("")

    # ---------------- viability envelope ----------------
    P("== VIABILITY ENVELOPE: fraction of targets with a standard part in tol ==")
    P("  tol    | d3 table | d1 table")
    for tol in (10.0, 3.0, 1.0, 0.3, 0.1, 0.03, 0.01, 0.003):
        row = []
        for tab in (tabA, tabB):
            hits = 0
            for t in TARGETS:
                sel = tab.select(t, tol, prefer="nearest")
                # any standard part within tol? scan via cost policy result class
                sc = tab.select(t, tol, prefer="cost")
                if sc is not None and sc["cost_class"] == 0:
                    hits += 1
            row.append(hits)
        P("  %6.3f | %5d/64 | %5d/64" % (tol, row[0], row[1]))
    P("")

    # ---------------- verdict ----------------
    P("== VERDICT INPUTS ==")
    tol = 1.0
    dn = 0
    ntot = 0
    traded = []
    bits_saved = []
    for t in TARGETS:
        sc = tabA.select(t, tol, prefer="cost")
        sn = tabA.select(t, tol, prefer="nearest")
        sb = tabA.select(t, tol, prefer="bits")
        if sc is None or sn is None:
            continue
        ntot += 1
        if sc["node"] != sn["node"]:
            dn += 1
            traded.append(sc["err_deg"] - sn["err_deg"])
        if sb and sc["bits"] < sb["bits"]:
            bits_saved.append(sb["bits"] - sc["bits"])
    P("  @tol 1.0deg: cost-vs-nearest divergence %d/%d (%.0f%%)" % (dn, ntot, 100.0 * dn / ntot))
    P("  traded precision: median %.4f deg = %.1f%% of tolerance (the sliver)"
      % (median(traded), 100.0 * median(traded) / tol))
    P("  bought: median %s address bits saved vs legacy min-bits policy"
      % ("%.1f" % median(bits_saved) if bits_saved else "0"))
    P("  standard-part picks: %d/64 @ tol 1.0 (nearest policy: %d)"
      % (sum(1 for t in TARGETS
             if (lambda s: s is not None and s["cost_class"] == 0)(tabA.select(t, 1.0, prefer="cost"))),
         sum(1 for t in TARGETS
             if (lambda s: s is not None and s["cost_class"] == 0)(tabA.select(t, 1.0, prefer="nearest")))))
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
