#!/usr/bin/env python3

"""SPIN 14, SPOKE 7: COUPLING — cross-mechanism composition law.

HYPOTHESIS (falsifiable): composition is universally subadditive — for
every (grammar, spread, K) cell,
    gain(AS+N1) <= max(gain(AS), gain(N1)) + 2pp.
Secondary: mechanism value is grammar-class dependent — AS helps
fresh-cohort grammars (kcoh5), memory (N1 tri3 window) helps stale-heavy
grammars (ladder/cohort), so the right knob is predictable from class.

Mechanisms (per SPIN-10 idiom):
  baseline = grammar lats on e1 reality
  AS       = AS-exact lats (full within-cohort 1-tick decorrelation,
             spread preserved; even(1) for zero-lock) on e1 reality
  N1       = grammar lats on tri3 memory-window channel (sigma=3)
  AS+N1    = AS-exact lats on tri3

Gains measured vs the SAME-CELL baseline (e1 reality, grammar lats).
Additivity residual = observed_joint_gain - max(single_gain).

Grid: N=6, grammars {ladder, cohort 3+3, kcoh5, zero-lock} x spreads
{15,30} x K in {1,2} x arms {base, AS, N1, AS+N1}.
Swap-in: learned spread-scheduler (cohort 15->8 parking, kimi lane) at
K=2, arms {base, AS, N1, AS+N1} — three-way interaction probe.

Canaries (mandatory):
  A  anchor replay: ladder@15 K=1 ~71.5, zero@15 K=1 77.3 with
     ev~8756 debt~187834 (publishing-format rounding tolerance).
  B  determinism: one config run twice, byte-identical.

Integer-only inside every fabric loop; floats only in display stats.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "inventors-derby"))
sys.path.insert(0, str(ROOT / "wheel" / "novel"))
from exp_glm1 import run_fabric, within_pm, LCG, reality  # noqa: E402
from novel_exp import run2, tri, mean, SEEDS  # noqa: E402

DELTA = 12
N = 6
TICKS = 4800
CH_N1 = tri(3)


def row(cells):
    return " | ".join(f"{c:>10}" for c in cells)


def even(d, n=N):
    return [i * d for i in range(n)]


def stats(lats, k, ch=None):
    """5-seed mean stats. ch=None -> e1 reality (run_fabric); else channel."""
    if ch is None:
        rs = [run_fabric("interference", TICKS, lats, K=k, pd=3,
                         delta=DELTA, drift=6, seed=s) for s in SEEDS]
    else:
        rs = [run2("interference", TICKS, lats, ch, K=k, pd=3,
                   delta=DELTA, drift=6, seed=s) for s in SEEDS]
    return dict(tp=mean([within_pm(r["resid"], DELTA) for r in rs]) / 10,
                ev=mean([r["events"] for r in rs]),
                debt=mean([r["mass"] for r in rs]),
                chat=mean([r["chatter"] for r in rs]))


# grammar -> (base_lats(s), as_lats(s))
def grammar_lats(name, s):
    if name == "zero":
        return [0] * N, even(1)
    if name == "ladder":
        return even(round(s / (N - 1))), [0, 1, 2, 3, 4, s]
    if name == "cohort":
        return [0, 0, 0, s, s, s], [0, 1, 2, s - 2, s - 1, s]
    if name == "kcoh5":
        return [0, 0, 0, 0, 0, s], [0, 1, 2, 3, 4, s]
    raise ValueError(name)


# ------------------------- canaries -------------------------
def canaries():
    print("== CANARY A: published-anchor replay ==")
    print(row(["config", "K", "got%", "want%", "ev", "evWant",
               "debt", "dWant", "ok"]))
    ok = True
    anchors = [
        ("ladder15", even(3), 1, 71.5, 5792, 106378),
        ("ladder15", even(3), 2, 60.0, None, None),
        ("zero", [0] * 6, 1, 77.3, 8756, 187834),
        ("zero", [0] * 6, 2, 50.0, 15133, 511660),
        ("cohort15", [0, 0, 0, 15, 15, 15], 1, 57.1, None, None),
        ("kcoh5@15", [0, 0, 0, 0, 0, 15], 1, 74.1, None, None),
        ("kcoh5@15AS", [0, 1, 2, 3, 4, 15], 1, 79.4, None, None),
    ]
    for name, lats, k, want, wev, wdebt in anchors:
        s = stats(lats, k)
        good = abs(s["tp"] - want) <= 0.15
        if wev is not None:
            good &= round(s["ev"]) == wev
        if wdebt is not None:
            good &= round(s["debt"]) == wdebt
        ok &= good
        print(row([name, k, f"{s['tp']:.1f}", want, f"{round(s['ev'])}",
                   wev if wev is not None else "-",
                   f"{round(s['debt'])}", wdebt if wdebt is not None else "-",
                   "OK" if good else "DRIFT"]))

    print("\n== CANARY B: determinism (one config twice, byte-identical) ==")
    a = run_fabric("interference", TICKS, [0, 1, 2, 3, 4, 15], K=2, pd=3,
                   delta=DELTA, drift=6, seed=SEEDS[2])
    b = run_fabric("interference", TICKS, [0, 1, 2, 3, 4, 15], K=2, pd=3,
                   delta=DELTA, drift=6, seed=SEEDS[2])
    det = a == b
    tri_a = run2("interference", TICKS, [0, 0, 0, 8, 8, 8], CH_N1, K=2, pd=3,
                 delta=DELTA, drift=6, seed=SEEDS[3])
    tri_b = run2("interference", TICKS, [0, 0, 0, 8, 8, 8], CH_N1, K=2, pd=3,
                 delta=DELTA, drift=6, seed=SEEDS[3])
    det &= tri_a == tri_b
    print(f"  e1-reality dict equal: {a == b};  tri3 dict equal: {tri_a == tri_b}"
          f"  -> {'PASS' if det else 'FAIL'}")
    return ok and det


# ------------------------- main grid -------------------------
def grid():
    print("\n== EXP1: 4-way arm grid  grammar x spread x K ==")
    print(row(["cell", "arm", "true%", "events", "chat", "gain pp"]))
    results = {}
    for gname in ("ladder", "cohort", "kcoh5", "zero"):
        for s in (15, 30):
            base_lats, as_lats = grammar_lats(gname, s)
            for k in (1, 2):
                cell = f"{gname}@{s}"
                arms = {
                    "base": stats(base_lats, k),
                    "AS": stats(as_lats, k),
                    "N1": stats(base_lats, k, CH_N1),
                    "AS+N1": stats(as_lats, k, CH_N1),
                }
                results[(cell, k)] = arms
                b = arms["base"]["tp"]
                for aname, s_ in arms.items():
                    gain = 0.0 if aname == "base" else s_["tp"] - b
                    print(row([cell, aname, f"{s_['tp']:.1f}",
                               f"{s_['ev']:.0f}", f"{s_['chat']:.0f}",
                               f"{gain:+.1f}" if aname != "base" else "  --"]))

    print("\n== EXP2: additivity residuals  joint_gain - max(single_gain) ==")
    print("   hypothesis: residual <= +2pp in every cell")
    print(row(["cell", "K", "g(AS)", "g(N1)", "g(joint)", "residual",
               "subadd?"]))
    n_ok = n_tot = 0
    for (cell, k), arms in sorted(results.items()):
        b = arms["base"]["tp"]
        gas = arms["AS"]["tp"] - b
        gn1 = arms["N1"]["tp"] - b
        gj = arms["AS+N1"]["tp"] - b
        resid = gj - max(gas, gn1)
        sub = resid <= 2.0
        n_tot += 1
        n_ok += sub
        print(row([cell, k, f"{gas:+.1f}", f"{gn1:+.1f}", f"{gj:+.1f}",
                   f"{resid:+.1f}", "YES" if sub else "NO"]))
    print(f"   subadditive cells: {n_ok}/{n_tot}")

    print("\n== EXP3: grammar-class x mechanism (which knob wins where) ==")
    print(row(["cell", "K", "g(AS)", "g(N1)", "winner"]))
    for (cell, k), arms in sorted(results.items()):
        b = arms["base"]["tp"]
        gas = arms["AS"]["tp"] - b
        gn1 = arms["N1"]["tp"] - b
        win = "AS" if gas > gn1 + 2 else ("N1" if gn1 > gas + 2 else "tie")
        print(row([cell, k, f"{gas:+.1f}", f"{gn1:+.1f}", win]))
    return results


# ------------------------- swap-in cells -------------------------
def swapin(grid_results):
    print("\n== EXP4: learned spread-scheduler swap-in (cohort 15->8 parking, K=2) ==")
    print("   reference: cohort@15 K=2 base + AS + N1 from EXP1")
    ref = grid_results[("cohort@15", 2)]
    base8 = [0, 0, 0, 8, 8, 8]
    as8 = [0, 1, 2, 6, 7, 8]
    arms = {"base": stats(base8, 2), "AS": stats(as8, 2),
            "N1": stats(base8, 2, CH_N1), "AS+N1": stats(as8, 2, CH_N1)}
    print(row(["arm", "true%", "events", "chat",
               "vs coh15-base", "vs coh15-same-arm"]))
    rb = ref["base"]["tp"]
    for aname, s_ in arms.items():
        v1 = s_["tp"] - rb
        v2 = s_["tp"] - ref[aname]["tp"]
        print(row([aname, f"{s_['tp']:.1f}", f"{s_['ev']:.0f}",
                   f"{s_['chat']:.0f}", f"{v1:+.1f}", f"{v2:+.1f}"]))
    b = arms["base"]["tp"]
    gas = arms["AS"]["tp"] - b
    gn1 = arms["N1"]["tp"] - b
    gj = arms["AS+N1"]["tp"] - b
    resid = gj - max(gas, gn1)
    print(f"\n   swap-in residuals: g(AS) {gas:+.1f}  g(N1) {gn1:+.1f}  "
          f"g(joint) {gj:+.1f}  residual {resid:+.1f}  "
          f"(subadditive: {'YES' if resid <= 2.0 else 'NO'})")
    # three-way: scheduler-gain composing with best mechanism
    best15 = max(ref[a]["tp"] for a in ("AS", "N1"))
    print(f"   three-way probe: best coh15 mechanism {best15:.1f} vs "
          f"best coh8 mechanism {max(arms[a]['tp'] for a in ('AS','N1')):.1f} "
          f"vs coh8 joint {gj + b:.1f}")
    return arms


def main():
    ok = canaries()
    if not ok:
        print("\nCANARY FAILURE — aborting (no numbers booked)")
        sys.exit(1)
    res = grid()
    swapin(res)
    x = LCG(368800899).next()
    print(f"\nLCG ritual: 368800899 -> {x} -> mod 10 = {x % 10}")


if __name__ == "__main__":
    main()
