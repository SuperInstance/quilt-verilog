#!/usr/bin/env python3
"""Model arena — Liquid models compete to design the best integer snap strategy.

Arena: the E1 interference-tick stress environment (drift=6, twin latency=10).
Each competitor proposes a strategy as JSON: {K, pulse_div, delta, mode}.
The e1 harness (5 seeds) is the only judge. Two rounds: propose, then revise
after seeing the leaderboard. Self-improvement = round-over-round delta.

Integer-only scoring. Local models only. Ollama at 127.0.0.1:11434.
"""
import json, re, subprocess, sys
sys.path.insert(0, ".")
import e1

OLLAMA = "http://127.0.0.1:11434/api/generate"
OLLAMA_CHAT = "http://127.0.0.1:11434/api/chat"
STRESS = dict(delta=None, drift=6, lat2=10)   # delta comes from the model
SEEDS = (1, 7, 42, 1999, 20260902)

CONTESTANTS = [
    "Liquid-LFM2.5-2.6B:latest",
    "LiquidAI/lfm2.5-1.2b-instruct:latest",
    "LiquidAI/lfm2.5-350m:latest",
    "qwen3:8b",
    "granite3.1-dense:2b",
]

PROMPT = """You design a control strategy for an integer-only snap system.

A simulated game state g drifts each tick by -6..+6. Two sensor twins report
the true channel: one live, one delayed 10 ticks. When |sensor - g| > delta,
a correction fires. Two correction modes exist:
- "sequential": hard impulse — g is set to the sensor instantly.
- "interference": corrections become signed pulses of size |error|/pulse_div
  that decay by halving over K ticks; overlapping pulses ADD before touching g.

Tune for maximum percent of ticks where BOTH sensors are within delta of g,
tie-broken by lower total ledger mass. Constraints: 1 <= K <= 16,
1 <= pulse_div <= 8, 4 <= delta <= 24, mode is one of the two above.

Known data point: impulse alone scores ~52% within, maxErr 61. Interference
with K=4, pulse_div=3, delta=12 scores ~83% within, maxErr 39.

{round_hdr}

Reply with ONLY a JSON object, no other text:
{{"K": <int>, "pulse_div": <int>, "delta": <int>, "mode": "<mode>", "reason": "<one sentence>"}}"""


def _balanced_objects(text):
    """String-aware brace scan: (complete {...} spans, start of an unterminated one)."""
    spans, depth, start, in_str, esc = [], 0, None, False, False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                spans.append(text[start:i + 1])
                start = None
    return spans, (start if depth else None)


def _salvage_truncated(text):
    """LFM-2.6B overrun case: reply died mid-object — regex the fields out of the tail."""
    _, open_at = _balanced_objects(text)
    if open_at is None:
        return None
    frag = text[open_at:]
    fields = {}
    for key in ("K", "pulse_div", "delta"):
        m = re.search(r'"%s"\s*:\s*(-?\d+)' % key, frag)
        if m:
            fields[key] = int(m.group(1))
    if not all(k in fields for k in ("K", "pulse_div", "delta")):
        return None
    m = re.search(r'"mode"\s*:\s*"(sequential|interference)', frag)
    fields["mode"] = m.group(1) if m else "interference"
    fields["reason"] = "salvaged from truncated response"
    return fields


def parse_response(text):
    """Contract: (params, None) on success, (None, snippet) on failure.

    Models narrate, nest braces, and truncate at the token cap. Take the last
    balanced object; if none parses, salvage fields from a truncated tail."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    p = None
    for cand in reversed(_balanced_objects(text)[0]):
        for fixed in (cand, re.sub(r",\s*([}\]])", r"\1", cand)):
            try:
                p = json.loads(fixed)
                break
            except json.JSONDecodeError:
                pass
        if p is not None:
            break
    if not isinstance(p, dict):
        p = _salvage_truncated(text)
    if not isinstance(p, dict):
        return None, text.strip()[:120]
    p["K"] = max(1, min(16, int(p["K"])))
    p["pulse_div"] = max(1, min(8, int(p["pulse_div"])))
    p["delta"] = max(4, min(24, int(p["delta"])))
    if p["mode"] not in ("sequential", "interference"):
        p["mode"] = "interference"
    return p, None


def ask(model, prompt):
    try:
        opts = {"temperature": 0.7, "num_predict": 400}
        ml = model.lower()
        if "qwen3" in ml:
            # qwen3:8b answers empty via raw generate — its chat template
            # never renders. /api/chat applies it; think:false stops the
            # reasoning block from eating the whole token budget.
            url, payload = OLLAMA_CHAT, {
                "model": model, "stream": False, "think": False, "options": opts,
                "messages": [{"role": "user", "content": prompt}]}
        else:
            url, payload = OLLAMA, {
                "model": model, "prompt": prompt, "stream": False, "options": opts}
            if "2.6b" in ml:
                # LFM-2.6B narrates past num_predict and truncates the JSON
                # envelope; JSON-constrained decoding keeps output inside it.
                payload["format"] = "json"
        out = subprocess.run(
            ["curl", "-s", url, "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=180)
        data = json.loads(out.stdout)
        text = data["message"]["content"] if "message" in data else data.get("response", "")
        return parse_response(text)
    except Exception as ex:
        return None, str(ex)[:120]


def score(p):
    e1.SEED = 20260902  # sweep seeds derive from this inside run? no — run uses global; set per call
    tot_w, tot_d, tot_e = 0.0, 0, 0
    for seed in SEEDS:
        e1.SEED = seed
        r = e1.run(p["mode"], delta=p["delta"], K=p["K"],
                   pulse_div=p["pulse_div"], drift=STRESS["drift"], lat2=STRESS["lat2"])
        tot_w += r["pct_within"]; tot_d += r["ledger_mass"]; tot_e = max(tot_e, r["max_err"])
    n = len(SEEDS)
    return dict(pct=round(tot_w / n, 1), debt=tot_d, maxerr=tot_e)


def run_round(models, round_no, leaderboard=None, best=None):
    """Ratchet: best[model] is that agent's best-ever (pct, strategy).
    A revision only replaces the ratcheted strategy if it scores strictly better
    on the primary metric (pct) — competitive pressure without amnesia."""
    hdr = f"ROUND {round_no}: revise your strategy."
    if leaderboard:
        hdr += "\n\nLeaderboard so far (score = % ticks within deadband):\n" + leaderboard
        hdr += "\nImprove on your previous design. Change what lost."
    rows = []
    for m in models:
        p, err = ask(m, PROMPT.format(round_hdr=hdr))
        if p is None:
            rows.append((m, (best or {}).get(m, (None, None))[1], (best or {}).get(m, (None, None))[0], f"unparseable: {err}"))
            continue
        s = score(p)
        prev = (best or {}).get(m)
        if prev and prev[0] and prev[0]["pct"] > s["pct"]:
            # ratchet holds: keep the better-ever strategy, log the regression
            rows.append((m, prev[1], prev[0], f"ratcheted (proposed {p['K']}/{p['pulse_div']}/{p['delta']} {p['mode']} scored {s['pct']}%)"))
        else:
            best = best or {}
            best[m] = (s, p)
            rows.append((m, p, s, None))
    return rows, best


def show(rows):
    lines = []
    scored = [(r[2]["pct"], -r[2]["debt"], r) for r in rows if r[2]]
    scored.sort(reverse=True)
    for pct, nd, (m, p, s, err) in scored:
        note = f"  [{err}]" if err else ""
        lines.append(f"  {pct:5.1f}%  debt={s['debt']:>7}  maxerr={s['maxerr']:>3}  "
                     f"{m.split('/')[-1]:<28} K={p['K']} pd={p['pulse_div']} d={p['delta']} {p['mode']}{note}")
    for m, p, s, err in rows:
        if not p and err:
            lines.append(f"  -----  {m.split('/')[-1]:<28} [{err}]")
    return "\n".join(lines), scored


if __name__ == "__main__":
    print("== baselines ==")
    b1 = score(dict(mode="sequential", delta=12, K=4, pulse_div=3))
    b2 = score(dict(mode="interference", delta=12, K=4, pulse_div=3))
    print(f"  impulse       {b1['pct']:5.1f}%  debt={b1['debt']}  maxerr={b1['maxerr']}")
    print(f"  interference  {b2['pct']:5.1f}%  debt={b2['debt']}  maxerr={b2['maxerr']}")

    print("\n== ROUND 1: initial designs ==")
    r1, best = run_round(CONTESTANTS, 1)
    lb1, scored1 = show(r1)
    print(lb1)

    print("\n== ROUND 2: revise after seeing leaderboard (ratchet active) ==")
    lb_text = "\n".join(l for l in lb1.splitlines())
    r2, best = run_round(CONTESTANTS, 2, lb_text, best=best)
    lb2, scored2 = show(r2)
    print(lb2)

    print("\n== ROUND 3: second revision (ratchet active) ==")
    r3, best = run_round(CONTESTANTS, 3, lb2, best=best)
    lb3, scored3 = show(r3)
    print(lb3)

    champ = scored3[0] if scored3 else None
    print("\n== champion ==")
    if champ:
        pct, nd, (m, p, s, err) = champ
        print(f"{m} — {pct}% within, debt {s['debt']}, maxerr {s['maxerr']}")
        print(f"strategy: {json.dumps(p)}")
        print(f"reason: {p.get('reason','')}")
    print("\nvs hand-tuned interference:", b2["pct"], "% — beats hand" if champ and champ[0] > b2["pct"] else "hand tuning still leads" if champ else "")
