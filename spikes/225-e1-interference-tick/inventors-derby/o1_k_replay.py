#!/usr/bin/env python3
"""O1 — K=2/3 CHAMPION REPLAY (overnight queue, dev round 1, night 2026-09-02).

Hypothesis (RESEARCH-AGENDA §4 O1): with the tournament schema widened to
K in {1..8} (arena.py v3), short-K interference entries beat the banked
champion (granite K=5/pd4/d16 = 93.2% stress %w), and the ledger's calm
specialist is displaced by short-K interference at delta=6 (92.1 vs impulse
56.6; 74.8 vs 56.6 on the pd axis).

Protocol:
  Phase 0  CONTROL ARMS — byte-match every published number touched here
           (champion row, gentle-tight rows, arena baselines, ledger-calm).
  Phase 1  STATIC NON-LLM PROBES: K in {1,2,3} x pd in {2,3} at the
           champion's own frame (d16, drift6, lat10) + the glm-3 claim rows
           (K3/pd4, K2/pd4) + the champion row itself. Scored on BOTH
           regimes: stress (champion frame) + the two calm frames
           (ledger-calm d12/drift3/lat5, gentle-tight d6/drift3/lat5).
  Phase 2  LLM ROUND (arena.py v3 lane, granite3.1-dense:2b, widened prompt
           K in 1..8, 5 seeds): does any contestant propose K<=3 this time?
  Phase 3  HOLDOUT VERIFICATION: any entry beating 93.2% on the primary
           seed set is re-run on holdout seeds (11, 313, 8888) before any
           banking decision.
  Phase 4  Decision rule: any K<=3 entry beating 93.2% on holdout => new
           champion banked (champion's debt crown noted, not dominated);
           ledger calm cell re-keyed. No LLM proposes K<=3 => book "grid
           anchoring" as a standing arena bias and promote the static probe.

Integer-only: every measurement loop runs inside stock e1.run (Python ints);
division appears only in report aggregation exactly as arena.py score() does
(pct = round(mean of per-seed pct_within, 1), debt summed, maxerr maxed).
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import e1

SEEDS = (1, 7, 42, 1999, 20260902)
HOLDOUT = (11, 313, 8888)

# Frames (named exactly as OVERNIGHT-K-REPLAY.md so numbers are comparable)
STRESS = dict(drift=6, lat=10)          # arena stress regime; delta from entry
GENTLE = dict(delta=6, drift=3, lat=5)  # README calm frame (the delta=6 axis)
LCALM = dict(delta=12, drift=3, lat=5)  # variety-ledger calm frame
CHAMP_FRAME_DELTA = 16                  # banked champion's delta

OLLAMA = "http://127.0.0.1:11434/api/generate"
MODEL = "granite3.1-dense:2b"           # the banked champion's own designer

PROMPT = """You design a control strategy for an integer-only snap system.

A simulated game state g drifts each tick by -6..+6. Two sensor twins report
the true channel: one live, one delayed 10 ticks. When |sensor - g| > delta,
a correction fires. Two correction modes exist:
- "sequential": hard impulse — g is set to the sensor instantly.
- "interference": corrections become signed pulses of size |error|/pulse_div
  that decay by halving over K ticks; overlapping pulses ADD before touching g.

Tune for maximum percent of ticks where BOTH sensors are within delta of g,
tie-broken by lower total ledger mass. Constraints: 1 <= K <= 8,
1 <= pulse_div <= 8, 4 <= delta <= 24, mode is one of the two above.

Known data point: impulse alone scores ~52% within, maxErr 61. Interference
with K=4, pulse_div=3, delta=12 scores ~83% within, maxErr 39.

{round_hdr}

Reply with ONLY a JSON object, no other text:
{{"K": <int>, "pulse_div": <int>, "delta": <int>, "mode": "<mode>", "reason": "<one sentence>"}}"""


def run5(mode, K, pd, delta, drift, lat, seeds=SEEDS):
    rows = []
    for seed in seeds:
        e1.SEED = seed
        rows.append(e1.run(mode, delta=delta, K=K, pulse_div=pd, drift=drift, lat2=lat))
    return dict(
        pct=round(sum(r["pct_within"] for r in rows) / len(seeds), 1),
        debt=sum(r["ledger_mass"] for r in rows),
        maxerr=max(r["max_err"] for r in rows),
        pct_per_seed=tuple(r["pct_within"] for r in rows),
    )


FAILS = []


def gate(label, got, want):
    ok = got == want
    if not ok:
        FAILS.append(label)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got}  want {want}")


# ---------------------------------------------------------------- phase 0
def controls():
    print("== PHASE 0: CONTROL ARMS (byte-match gates; FAIL halts new claims) ==")
    a = run5("interference", 5, 4, CHAMP_FRAME_DELTA, 6, 10)
    gate("banked champion K5/pd4/d16 stress (pct,debt,maxerr)",
         (a["pct"], a["debt"], a["maxerr"]), (93.2, 132823, 38))
    a = run5("interference", 3, 4, CHAMP_FRAME_DELTA, 6, 10)
    gate("glm-3 claim K3/pd4/d16 stress", (a["pct"], a["debt"], a["maxerr"]), (94.2, 139257, 39))
    a = run5("interference", 2, 4, CHAMP_FRAME_DELTA, 6, 10)
    gate("K2/pd4/d16 stress", (a["pct"], a["debt"], a["maxerr"]), (94.1, 150968, 36))
    a = run5("sequential", 8, 3, CHAMP_FRAME_DELTA, 6, 10)
    gate("impulse d16 stress (unseen-entry control)", (a["pct"], a["debt"], a["maxerr"]), (96.0, 139949, 61))
    a = run5("interference", 2, 3, GENTLE["delta"], GENTLE["drift"], GENTLE["lat"])
    gate("gentle K=2 pd3 (calm re-key evidence)", (a["pct"], a["debt"], a["maxerr"]), (92.1, 113573, 32))
    a = run5("sequential", 8, 3, GENTLE["delta"], GENTLE["drift"], GENTLE["lat"])
    gate("impulse gentle", (a["pct"], a["debt"], a["maxerr"]), (56.6, 117198, 53))
    a = run5("interference", 2, 3, LCALM["delta"], LCALM["drift"], LCALM["lat"])
    gate("ledger-calm intf K2/pd3/d12", (a["pct"], a["debt"], a["maxerr"]), (97.8, 97682, 32))
    a = run5("sequential", 8, 3, LCALM["delta"], LCALM["drift"], LCALM["lat"])
    gate("ledger-calm impulse d12", (a["pct"], a["debt"], a["maxerr"]), (98.0, 55545, 53))
    a = run5("interference", 4, 3, 12, 6, 10)
    gate("arena-v2 interference baseline K=4", (a["pct"], a["debt"], a["maxerr"]), (83.1, 174978, 39))
    a = run5("sequential", 8, 3, 12, 6, 10)
    gate("arena-v2 impulse baseline", (a["pct"], a["debt"], a["maxerr"]), (51.4, 244973, 61))
    return not FAILS


# ---------------------------------------------------------------- phase 1
def probes():
    print("\n== PHASE 1: STATIC NON-LLM PROBES (K in {1,2,3} x pd in {2,3}, champion frame d16) ==")
    entries = []
    for K in (1, 2, 3):
        for pd in (2, 3):
            entries.append((f"probe K={K} pd={pd} d16 intf", "interference", K, pd, CHAMP_FRAME_DELTA))
    entries += [
        ("glm-3 claim K=3 pd=4 d16 intf", "interference", 3, 4, CHAMP_FRAME_DELTA),
        ("K=2 pd=4 d16 intf", "interference", 2, 4, CHAMP_FRAME_DELTA),
        ("BANKED CHAMPION K=5 pd=4 d16 intf", "interference", 5, 4, CHAMP_FRAME_DELTA),
    ]
    print(f"{'entry':<36}{'stress%':>9}{'debt':>8}{'maxE':>6}   {'gentle%':>8}{'lcalm%':>8}")
    results = {}
    for name, mode, K, pd, delta in entries:
        s = run5(mode, K, pd, delta, STRESS["drift"], STRESS["lat"])
        g = run5(mode, K, pd, GENTLE["delta"], GENTLE["drift"], GENTLE["lat"])
        c = run5(mode, K, pd, LCALM["delta"], LCALM["drift"], LCALM["lat"])
        results[name] = dict(params=(mode, K, pd, delta), stress=s, gentle=g, lcalm=c)
        print(f"{name:<36}{s['pct']:>9}{s['debt']:>8}{s['maxerr']:>6}   {g['pct']:>8}{c['pct']:>8}")
    # calm-axis evidence rows (delta=6 frame, short-K vs impulse) for the re-key
    print("\n-- calm-axis rows (gentle-tight d6/drift3/lat5) --")
    print(f"{'entry':<36}{'gentle%':>9}{'debt':>8}{'maxE':>6}")
    for K in (1, 2, 3):
        for pd in (2, 3):
            g = run5("interference", K, pd, GENTLE["delta"], GENTLE["drift"], GENTLE["lat"])
            print(f"{'gentle intf K='+str(K)+' pd='+str(pd):<36}{g['pct']:>9}{g['debt']:>8}{g['maxerr']:>6}")
    gi = run5("sequential", 8, 3, GENTLE["delta"], GENTLE["drift"], GENTLE["lat"])
    print(f"{'gentle impulse (calm specialist)':<36}{gi['pct']:>9}{gi['debt']:>8}{gi['maxerr']:>6}")
    return results


# ---------------------------------------------------------------- phase 2
def parse_response(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    spans = re.findall(r"\{[^{}]*\}", text)
    for cand in reversed(spans):
        for fixed in (cand, re.sub(r",\s*([}\]])", r"\1", cand)):
            try:
                p = json.loads(fixed)
                if all(k in p for k in ("K", "pulse_div", "delta", "mode")):
                    p["K"] = max(1, min(8, int(p["K"])))
                    p["pulse_div"] = max(1, min(8, int(p["pulse_div"])))
                    p["delta"] = max(4, min(24, int(p["delta"])))
                    if p["mode"] not in ("sequential", "interference"):
                        p["mode"] = "interference"
                    return p
            except (json.JSONDecodeError, ValueError, TypeError):
                pass
    return None


def ask_model(round_hdr):
    payload = {"model": MODEL, "prompt": PROMPT.format(round_hdr=round_hdr),
               "stream": False, "options": {"temperature": 0.7, "num_predict": 400},
               "format": "json"}
    try:
        out = subprocess.run(["curl", "-s", OLLAMA, "-d", json.dumps(payload)],
                             capture_output=True, text=True, timeout=180)
        data = json.loads(out.stdout)
        return parse_response(data.get("response", ""))
    except Exception as ex:
        print(f"  [llm lane error] {str(ex)[:120]}")
        return None


def llm_rounds(probe_stress):
    print("\n== PHASE 2: LLM ROUNDS (arena.py v3 schema, K in 1..8, granite3.1-dense:2b) ==")
    proposals = []
    lb = "probe K=3 pd=4 d16 intf: 94.2% (static probe)\nprobe K=1 pd=2 d16 intf: see round 1"
    for rnd in (1, 2):
        hdr = (f"ROUND {rnd}: propose your strategy." if rnd == 1 else
               f"ROUND {rnd}: revise your strategy.\n\nLeaderboard so far:\n{lb}\n"
               "Improve on your previous design. Change what lost.")
        p = ask_model(hdr)
        if p is None:
            print(f"  round {rnd}: unparseable/failed — static-probe-only lane")
            continue
        s = run5(p["mode"], p["K"], p["pulse_div"], p["delta"], STRESS["drift"], STRESS["lat"])
        proposals.append((rnd, p, s))
        print(f"  round {rnd}: K={p['K']} pd={p['pulse_div']} d={p['delta']} {p['mode']} "
              f"-> stress {s['pct']}% debt {s['debt']} maxE {s['maxerr']}   "
              f"{'** K<=3 PROPOSED **' if p['mode'] == 'interference' and p['K'] <= 3 else ''}")
        lb += f"\nyou round {rnd}: {s['pct']}% (K={p['K']} pd={p['pulse_div']} d={p['delta']} {p['mode']})"
    return proposals


# ---------------------------------------------------------------- phase 3
def holdout(mode, K, pd, delta):
    print(f"\n== PHASE 3: HOLDOUT VERIFICATION ({mode} K={K} pd={pd} d={delta}, seeds {HOLDOUT}) ==")
    h = run5(mode, K, pd, delta, STRESS["drift"], STRESS["lat"], seeds=HOLDOUT)
    print(f"  holdout stress: pct={h['pct']} debt={h['debt']} maxE={h['maxerr']} per-seed={h['pct_per_seed']}")
    champ_h = run5("interference", 5, 4, CHAMP_FRAME_DELTA, STRESS["drift"], STRESS["lat"], seeds=HOLDOUT)
    print(f"  champion holdout: pct={champ_h['pct']} debt={champ_h['debt']} maxE={champ_h['maxerr']} per-seed={champ_h['pct_per_seed']}")
    return h, champ_h


if __name__ == "__main__":
    if not controls():
        print("\nPHASE 0 FAILED — no new claims read from this harness.")
        sys.exit(1)
    res = probes()
    props = llm_rounds(res)
    # promotion candidates: any K<=3 entry (probe or LLM) beating 93.2 on primary seeds
    cands = []
    for name, r in res.items():
        mode, K, pd, delta = r["params"]
        if mode == "interference" and K <= 3 and r["stress"]["pct"] > 93.2:
            cands.append((name, mode, K, pd, delta, r["stress"]["pct"]))
    for rnd, p, s in props:
        if p["mode"] == "interference" and p["K"] <= 3 and s["pct"] > 93.2:
            cands.append((f"llm r{rnd}", p["mode"], p["K"], p["pulse_div"], p["delta"], s["pct"]))
    print("\n== PROMOTION CANDIDATES (K<=3, stress > 93.2% on primary seeds) ==")
    for c in cands:
        print(f"  {c}")
    if not cands:
        print("  none")
        sys.exit(0)
    best = max(cands, key=lambda c: c[5])
    h, ch = holdout(best[1], best[2], best[3], best[4])
    print(f"\nDECISION: {'PROMOTE ' + best[0] if h['pct'] > 93.2 else 'HOLDOUT FAILED, no promotion'} "
          f"(holdout {h['pct']}% vs champion holdout {ch['pct']}%)")
