#!/usr/bin/env python3
"""OVERNIGHT QUEUE RUN 1 — K-AXIS RESCUE REPLAY (night of 2026-09-02).

Hypothesis (glm-3 derby finding #3, Tail-Shock): the banked arena champion's
crown is a K-grid artifact; at K=2/K=3 interference dominates far beyond the
published margins.

Protocol:
  Phase 0  CONTROL ARMS — byte-match every published number this replay
           touches (README.md, arena-v2.txt, ledger-results.txt,
           glm3_run_output.txt EXP5). Any FAIL halts the report: no new
           claim may be read from a harness that cannot reproduce the old
           numbers.
  Phase 1  K sweep {1,2,3,4,5,6,8} x BOTH arms x 5 seeds x 4 frames, exact
           arena.py scoring convention (pct = round(mean of per-seed
           pct_within, 1), debt summed, maxerr maxed). Sequential arm
           verified K-invariant (K is not a dial it owns).
  Phase 2  K-vs-margin curves (margin = intf %w - seq %w): peak + inversion.
  Phase 3  glm-3's specific claim: granite-tuned K=3 (94.2%) vs banked
           champion K=5 (93.2%) — full seed set, per-seed spread + winners.
  Phase 4  decision-rule update + arena-grid proposal (printed findings).

Integer-only: every loop runs inside stock e1.run (Python ints). Division
appears only in report aggregation exactly as arena.py does it.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import e1

SEEDS = (1, 7, 42, 1999, 20260902)
KGRID = (1, 2, 3, 4, 5, 6, 8)

FRAMES = {
    "stress-hand":  dict(pd=3, delta=12, drift=6, lat=10,
                         note="README/arena baseline frame (hand tune K=4)"),
    "gentle-tight": dict(pd=3, delta=6, drift=3, lat=5,
                         note="README calm frame ('interference worse in calm')"),
    "arena-champ":  dict(pd=4, delta=16, drift=6, lat=10,
                         note="banked champion frame (granite K=5 pd4 d16)"),
    "ledger-calm":  dict(pd=3, delta=12, drift=3, lat=5,
                         note="variety-ledger calm frame (impulse d12 banked)"),
}


def run5(mode, K, pd, delta, drift, lat):
    """Exact arena.py score() convention; per-seed rows kept for spread."""
    rows = []
    for seed in SEEDS:
        e1.SEED = seed
        rows.append(e1.run(mode, delta=delta, K=K, pulse_div=pd, drift=drift, lat2=lat))
    agg = dict(
        pct=round(sum(r["pct_within"] for r in rows) / len(SEEDS), 1),
        debt=sum(r["ledger_mass"] for r in rows),
        maxerr=max(r["max_err"] for r in rows),
        canc=sum(r["cancellations"] for r in rows),
        chat=sum(r["chatter"] for r in rows),
        ev=sum(r["snap_events"] for r in rows),
    )
    return agg, rows


FAILS = []


def gate(label, got, want):
    ok = got == want
    if not ok:
        FAILS.append(label)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got}  want {want}")


# ---------------------------------------------------------------- phase 0
def controls():
    print("== PHASE 0: CONTROL ARMS (byte-match gates; FAIL halts new claims) ==")
    print("-- C1/C2: arena-v2.txt baselines (stress d12/pd3, drift6/lat10) --")
    a, _ = run5("sequential", 4, 3, 12, 6, 10)
    gate("arena impulse baseline (pct,debt,maxerr)", (a["pct"], a["debt"], a["maxerr"]), (51.4, 244973, 61))
    a, _ = run5("interference", 4, 3, 12, 6, 10)
    gate("arena interference baseline K=4", (a["pct"], a["debt"], a["maxerr"]), (83.1, 174978, 39))

    print("-- C3: banked champion (granite K=5 pd4 d16, stress regime) --")
    a, rows = run5("interference", 5, 4, 16, 6, 10)
    gate("banked champion aggregate", (a["pct"], a["debt"], a["maxerr"]), (93.2, 132823, 38))

    print("-- C4: README per-seed stress table (K=4 pd3 d12) --")
    _, srows = run5("sequential", 4, 3, 12, 6, 10)
    _, irows = run5("interference", 4, 3, 12, 6, 10)
    gate("README seq pct/seed", tuple(r["pct_within"] for r in srows), (51.9, 49.4, 53.1, 50.5, 51.9))
    gate("README seq maxErr/seed", tuple(r["max_err"] for r in srows), (61, 61, 61, 61, 61))
    gate("README seq ev/seed", tuple(r["snap_events"] for r in srows), (2524, 2655, 2469, 2602, 2513))
    gate("README int pct/seed", tuple(r["pct_within"] for r in irows), (83.0, 82.5, 83.4, 83.6, 83.0))
    gate("README int maxErr/seed", tuple(r["max_err"] for r in irows), (38, 39, 38, 39, 39))
    gate("README int ev/seed", tuple(r["snap_events"] for r in irows), (2064, 2022, 2044, 2009, 2070))

    print("-- C5: README gentle claim, stock e1.py defaults, seed 20260902 --")
    e1.SEED = 20260902
    r = e1.run("interference", K=8, pulse_div=3, delta=6, drift=3, lat2=5)
    gate("README gentle K=8 intf %w (45.5 claim)", r["pct_within"], 45.5)
    r = e1.run("sequential", delta=6, drift=3, lat2=5)
    gate("README gentle impulse %w (56.7 claim)", r["pct_within"], 56.7)

    print("-- C6: ledger-results.txt rows (calm regime drift3/lat5) --")
    a, _ = run5("sequential", 4, 3, 12, 3, 5)
    gate("ledger impulse calm d12", (a["pct"], a["debt"], a["maxerr"]), (98.0, 55545, 53))
    a, _ = run5("interference", 4, 3, 12, 3, 5)
    gate("ledger hand-intf calm d12 (K=4)", (a["pct"], a["debt"], a["maxerr"]), (97.3, 81617, 35))
    a, _ = run5("interference", 5, 4, 16, 3, 5)
    gate("ledger granite champion calm", (a["pct"], a["debt"], a["maxerr"]), (97.8, 87178, 35))

    print("-- C7: glm3_run_output.txt EXP5 K-sweep rows (both frames) --")
    want_stress = {1: (92.9, 184991, 33, 102, 5059), 2: (91.4, 169541, 35, 70, 4218),
                   3: (86.3, 172707, 38, 128, 4300), 4: (83.1, 174978, 39, 353, 4446),
                   5: (81.1, 175834, 39, 786, 4440), 6: (80.3, 176137, 39, 1288, 4558),
                   8: (78.2, 180397, 39, 1981, 4656)}
    for K in KGRID:
        a, _ = run5("interference", K, 3, 12, 6, 10)
        gate(f"glm3 EXP5 stress K={K}", (a["pct"], a["debt"], a["maxerr"], a["canc"], a["chat"]), want_stress[K])
    want_gentle = {1: (80.2, 145349, 31, 34, 9469), 2: (92.1, 113573, 32, 54, 5976),
                   3: (85.5, 109411, 34, 215, 5368), 4: (75.4, 112540, 35, 1085, 5617),
                   5: (65.6, 120516, 36, 1691, 6347), 6: (56.3, 131773, 38, 2199, 7347),
                   8: (42.2, 160715, 37, 2600, 9762)}
    for K in KGRID:
        a, _ = run5("interference", K, 3, 6, 3, 5)
        gate(f"glm3 EXP5 gentle K={K}", (a["pct"], a["debt"], a["maxerr"], a["canc"], a["chat"]), want_gentle[K])

    print("-- C8: glm3 EXP5 champion-frame + ledger-calm rows --")
    for K, want in ((5, (93.2, 132823, 38)), (2, (94.1, 150968, 36)), (3, (94.2, 139257, 39))):
        a, _ = run5("interference", K, 4, 16, 6, 10)
        gate(f"glm3 champion-frame K={K}", (a["pct"], a["debt"], a["maxerr"]), want)
    a, _ = run5("interference", 2, 3, 12, 3, 5)
    gate("glm3 ledger-calm intf K=2 d12", (a["pct"], a["debt"], a["maxerr"]), (97.8, 97682, 32))

    print()
    if FAILS:
        print(f"  *** {len(FAILS)} CONTROL(S) FAILED — new-claim sections suppressed ***")
        print(f"  failed: {FAILS}")
    else:
        print("  ALL CONTROLS PASS — stock e1.run reproduces every published number touched.")
    return not FAILS


# ---------------------------------------------------------------- phase 1+2
def sweep():
    print("\n== PHASE 1: K SWEEP — both arms, 5 seeds, 4 frames, arena.py scoring ==")
    results = {}
    for fname, f in FRAMES.items():
        print(f"\n  [{fname}]  pd={f['pd']} delta={f['delta']} drift={f['drift']} lat={f['lat']}   ({f['note']})")
        # sequential arm: run the full K grid to PROVE K-invariance
        seq_aggs = {}
        for K in KGRID:
            seq_aggs[K], _ = run5("sequential", K, f["pd"], f["delta"], f["drift"], f["lat"])
        invariant = len({(a["pct"], a["debt"], a["maxerr"], a["ev"]) for a in seq_aggs.values()}) == 1
        s = seq_aggs[KGRID[0]]
        print(f"    impulse (K-invariant: {'PROVEN' if invariant else 'VIOLATED'}): "
              f"%w={s['pct']:>5} debt={s['debt']:>7} maxE={s['maxerr']:>3} ev={s['ev']:>6}")
        print(f"    {'K':>4} {'%w':>6} {'margin':>7} {'debt':>8} {'maxE':>4} {'canc':>5} {'chat':>5} {'ev':>6}")
        rows = {}
        for K in KGRID:
            a, per_seed = run5("interference", K, f["pd"], f["delta"], f["drift"], f["lat"])
            rows[K] = (a, per_seed)
            print(f"    {K:>4} {a['pct']:>6} {round(a['pct'] - s['pct'], 1):>+7} "
                  f"{a['debt']:>8} {a['maxerr']:>4} {a['canc']:>5} {a['chat']:>5} {a['ev']:>6}")
        results[fname] = dict(seq=s, intf=rows, seq_invariant=invariant)

    print("\n== PHASE 2: K-vs-MARGIN CURVES (margin = intf %w - impulse %w) ==")
    curves = {}
    for fname, res in results.items():
        s = res["seq"]["pct"]
        pts = {K: round(a["pct"] - s, 1) for K, (a, _) in res["intf"].items()}
        peak_k = max(pts, key=lambda k: pts[k])
        inv = [k for k in sorted(pts) if pts[k] <= 0]
        curves[fname] = dict(pts=pts, peak=peak_k, invert=inv[0] if inv else None)
        inv_s = f"inverts at K={inv[0]}" if inv else "never inverts (all K > impulse)"
        print(f"  {fname:<13} margin: " + "  ".join(f"K{k}={pts[k]:+.1f}" for k in KGRID))
        print(f"  {'':<13} peak K={peak_k} ({pts[peak_k]:+.1f}); {inv_s}")
    return results, curves


# ---------------------------------------------------------------- phase 3
def claim_test():
    print("\n== PHASE 3: glm-3 CLAIM — granite-tuned K=3 (94.2%) vs banked champion K=5 (93.2%) ==")
    print("  frame: pd=4 delta=16 drift=6 lat=10 (exact banked-champion frame), per seed:")
    detail = {}
    for K in (2, 3, 5):
        a, rows = run5("interference", K, 4, 16, 6, 10)
        detail[K] = (a, rows)
    print(f"  {'seed':>9} {'K=2 %w':>8} {'K=3 %w':>8} {'K=5 %w':>8}   {'K3-K5':>6}   winner")
    for i, seed in enumerate(SEEDS):
        p2 = detail[2][1][i]["pct_within"]
        p3 = detail[3][1][i]["pct_within"]
        p5 = detail[5][1][i]["pct_within"]
        d = round(p3 - p5, 1)
        win = "K=3" if p3 > p5 else ("K=5" if p5 > p3 else "tie")
        print(f"  {seed:>9} {p2:>8} {p3:>8} {p5:>8}   {d:>+6}   {win}")
    for K in (2, 3, 5):
        a, rows = detail[K]
        pcts = [r["pct_within"] for r in rows]
        debts = [r["ledger_mass"] for r in rows]
        print(f"  K={K}: mean {a['pct']}%  spread {min(pcts)}..{max(pcts)}  "
              f"debt {a['debt']} (per-seed {min(debts)}..{max(debts)})  maxE {a['maxerr']}")
    n3 = sum(1 for i in range(5) if detail[3][1][i]["pct_within"] > detail[5][1][i]["pct_within"])
    n5 = sum(1 for i in range(5) if detail[5][1][i]["pct_within"] > detail[3][1][i]["pct_within"])
    print(f"  per-seed winners: K=3 wins {n3}/5, K=5 wins {n5}/5")
    return detail


def main():
    ok = controls()
    if not ok:
        sys.exit(1)
    results, curves = sweep()
    detail = claim_test()
    print("\n== PHASE 4: DECISION RULE (see OVERNIGHT-K-REPLAY.md for the proposal) ==")
    for fname, c in curves.items():
        best_k = max(c["pts"], key=lambda k: results[fname]["intf"][k][0]["pct"])
        print(f"  {fname:<13} best-K = {best_k} "
              f"({results[fname]['intf'][best_k][0]['pct']}% vs impulse {results[fname]['seq']['pct']}%)")


if __name__ == "__main__":
    main()
