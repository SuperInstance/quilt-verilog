#!/usr/bin/env python3
"""O5 — Phase-decay coupling vs admission gate, multi-seed confirm.

F24 (claude #1): phase-decay coupling at stress, seed 20260902: 84.3% vs 83.0%.
F16 (glm-3 #4): admission gating throttles. O5 tests whether F24 survives 5 seeds,
against baseline interference and an admission gate at MATCHED duty (same phase
clock, same 4/12 refractory window; pulses deferred while refractory).

Arms (all share one code path; integer-only, deterministic LCG, fixed seed per run):
  baseline      : plain interference (e1 semantics, seed-parameterized)
  phase_decay   : refractory cells dissipate pulses faster (double integer halving)
  admission_gate: pulse admission DEFERRED during the same refractory window
                  (duty-matched: identical phase_counter/period to phase_decay)

Run: python3 o5_phase_decay.py
"""
from collections import deque
import sys

SEEDS = [1, 7, 42, 1999, 20260902]
TICKS = 4800

REGIMES = {
    "calm":  dict(delta=6,  drift=3, K=8, lat2=5),
    "stress": dict(delta=12, drift=6, K=4, lat2=10),
}

PHASE_PERIOD = 12
REFRACTORY = 4  # phase_counter < REFRACTORY => in refractory (duty 4/12)


class LCG:
    def __init__(self, seed):
        self.x = seed & 0x7FFFFFFF or 1

    def next(self):
        self.x = (1103515245 * self.x + 12345) & 0x7FFFFFFF
        return self.x

    def below(self, n):
        return self.next() % n


def reality(t, period=240):
    phase = t % period
    if phase < 96:
        return 400 + phase * 8 // 5
    elif phase < 144:
        return 400 + 96 * 8 // 5 - (phase - 96)
    else:
        return 400 + 96 * 8 // 5 - 48 - (phase - 144) * 8 // 5


def run(arm, seed, ticks=TICKS, K=8, pulse_div=3, delta=6, drift=3, lat2=5):
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    deferred = deque()   # admission_gate only: pulses waiting out refractory
    snap_events = 0
    ledger_mass = 0
    constructive = 0
    cancellations = 0
    chatter = 0
    last_snap = -10
    max_err = 0
    settles = 0
    phase_counter = 0

    for t in range(ticks):
        phase_counter = (phase_counter + 1) % PHASE_PERIOD
        in_refractory = phase_counter < REFRACTORY

        s1 = reality(t)
        s2 = reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift

        while pulses and pulses[-1][1] == 0:
            pulses.pop()

        e1_val = s1 - g
        e2_val = s2 - g
        trig = []
        if abs(e1_val) > delta:
            trig.append(e1_val)
        if abs(e2_val) > delta:
            trig.append(e2_val)
        max_trig = max((abs(e) for e in trig), default=0)

        if arm == "admission_gate":
            # F16-style: admission DEFERRED while refractory (matched duty).
            for e in trig:
                if in_refractory:
                    deferred.append(e)
                else:
                    m = abs(e) // pulse_div or 1
                    pulses.appendleft([m if e > 0 else -m, K])
                    snap_events += 1
                    ledger_mass += abs(e)
            if deferred and not in_refractory:
                # admit the waiting pulses once refractory lifts
                for e in deferred:
                    m = abs(e) // pulse_div or 1
                    pulses.appendleft([m if e > 0 else -m, K])
                    snap_events += 1
                    ledger_mass += abs(e)
                deferred.clear()
        else:
            for e in trig:
                m = abs(e) // pulse_div or 1
                pulses.appendleft([m if e > 0 else -m, K])
                snap_events += 1
                ledger_mass += abs(e)

        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
            decayed = deque()
            for mag, life in pulses:
                if life > 0:
                    if abs(mag) > 1:
                        mag = mag - (mag // 2)
                        if arm == "phase_decay" and in_refractory and abs(mag) > 1:
                            mag = mag - (mag // 2)
                    decayed.append([mag, life - 1])
            pulses = decayed
            g += net
            if trig and max(abs(s1 - g), abs(s2 - g)) > max_trig:
                constructive += 1
            if trig and t - last_snap == 1:
                chatter += 1
            if trig:
                last_snap = t

        err = max(abs(s1 - g), abs(s2 - g))
        max_err = max(max_err, err)
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1

    return dict(arm=arm, seed=seed, snap_events=snap_events,
                ledger_mass=ledger_mass, constructive=constructive,
                cancellations=cancellations, chatter=chatter,
                max_err=max_err, pct_within=round(1000 * settles / ticks) / 10.0)


def arm_fingerprint(r):
    return (r["snap_events"], r["ledger_mass"], r["cancellations"], r["pct_within"])


def main():
    out = []

    def p(s=""):
        print(s)
        out.append(s)

    p("=" * 78)
    p("O5 — phase-decay coupling vs admission gate (matched duty), 5 seeds x 2 regimes")
    p("=" * 78)

    # ---- CANARY 1: published-anchor replay (F24 @ seed 20260902, stress) ----
    p("\n[CANARY 1] F24 anchor replay: expect baseline 83.0, phase_decay 84.3, cancels 68/107")
    base_a = run("baseline", 20260902, **REGIMES["stress"])
    pd_a = run("phase_decay", 20260902, **REGIMES["stress"])
    anchor_ok = (base_a["pct_within"] == 83.0 and pd_a["pct_within"] == 84.3
                 and base_a["cancellations"] == 68 and pd_a["cancellations"] == 107)
    p(f"  baseline:  %within={base_a['pct_within']} cancel={base_a['cancellations']}")
    p(f"  phase_decay: %within={pd_a['pct_within']} cancel={pd_a['cancellations']}")
    p(f"  ANCHOR: {'PASS' if anchor_ok else 'FAIL'}")

    # ---- CANARY 2: self-canary (mislabeled arm must be caught) ----
    p("\n[CANARY 2] self-canary: deliberately mislabeled arm must be caught")
    true_pd = run("phase_decay", 42, **REGIMES["stress"])
    labeled = {"phase_decay": run("baseline", 42, **REGIMES["stress"])}  # mislabel
    reference = {"phase_decay": true_pd}
    caught = arm_fingerprint(labeled["phase_decay"]) != arm_fingerprint(reference["phase_decay"])
    p(f"  labeled phase_decay actually ran baseline -> fingerprint mismatch caught: "
      f"{'PASS (mismatch detected)' if caught else 'FAIL'}")
    if not caught:
        anchor_ok = False

    # ---- Main grid ----
    results = {}
    p("\n" + "-" * 78)
    for regime, params in REGIMES.items():
        p(f"\n== REGIME: {regime} ({params}) ==")
        hdr = (f"{'seed':>9} | {'baseline %w (cancel)':>22} | {'phase_decay %w (cancel)':>24} "
               f"| {'admission_gate %w (cancel)':>26} | {'Δpd':>6} | {'Δgate':>7}")
        p(hdr)
        p("-" * len(hdr))
        for seed in SEEDS:
            b = run("baseline", seed, **params)
            d = run("phase_decay", seed, **params)
            a = run("admission_gate", seed, **params)
            results[(regime, seed)] = (b, d, a)
            p(f"{seed:>9} | {b['pct_within']:>10} ({b['cancellations']:>4})        "
              f"| {d['pct_within']:>12} ({d['cancellations']:>4})          "
              f"| {a['pct_within']:>14} ({a['cancellations']:>4})           "
              f"| {d['pct_within']-b['pct_within']:>+5.1f} | {a['pct_within']-b['pct_within']:>+6.1f}")

    # ---- Summary + decision rule (primary: stress, phase_decay vs baseline) ----
    p("\n" + "=" * 78)
    p("DECISION RULE (pre-registered, primary metric: stress, phase_decay vs baseline)")
    p("  promote iff mean Δ ≥ +0.5pp AND no seed < −0.5pp")
    deltas = []
    for seed in SEEDS:
        b, d, a = results[("stress", seed)]
        deltas.append(d["pct_within"] - b["pct_within"])
    mean_d = sum(deltas) / len(deltas)
    worst = min(deltas)
    per_seed = ", ".join(f"{x:+.1f}" for x in deltas)
    p(f"  per-seed Δ (stress): [{per_seed}]")
    p(f"  mean Δ = {mean_d:+.2f}pp   worst seed = {worst:+.1f}pp")
    rule1 = mean_d >= 0.5
    rule2 = worst >= -0.5
    verdict = "PROMOTE" if (rule1 and rule2) else "BOOK AS SINGLE-SEED NOISE"
    p(f"  mean Δ ≥ +0.5pp: {'YES' if rule1 else 'NO'}; no seed < −0.5pp: {'YES' if rule2 else 'NO'}")
    p(f"  VERDICT: {verdict}")

    p("\nSecondary: calm regime, phase_decay vs baseline")
    dc = [results[("calm", s)][1]["pct_within"] - results[("calm", s)][0]["pct_within"] for s in SEEDS]
    p(f"  per-seed Δ (calm): [{', '.join(f'{x:+.1f}' for x in dc)}]  mean = {sum(dc)/len(dc):+.2f}pp")

    p("\nAdmission gate (matched duty) vs baseline — F16 replication, both regimes:")
    for regime in REGIMES:
        da = [results[(regime, s)][2]["pct_within"] - results[(regime, s)][0]["pct_within"] for s in SEEDS]
        ca = [results[(regime, s)][2]["cancellations"] for s in SEEDS]
        cb = [results[(regime, s)][0]["cancellations"] for s in SEEDS]
        p(f"  {regime}: mean Δ = {sum(da)/len(da):+.2f}pp  "
          f"(cancels {sum(ca)} vs baseline {sum(cb)})")

    with open("o5-phase-decay-output.txt", "w") as f:
        f.write("\n".join(out) + "\n")
    p("\n(raw output written to o5-phase-decay-output.txt)")


if __name__ == "__main__":
    main()
