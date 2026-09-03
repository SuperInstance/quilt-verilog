#!/usr/bin/env python3
"""226 E1 — ICL CURRICULUM: can a tiny local LLM predict the next
correction's success bit better when shown REAL ordered trace context?

Model: LiquidAI/lfm2.5-1.2b-instruct @ 127.0.0.1:11434 (CPU/GPU local).
Task: given k exemplar correction events from a held-out run's emission
stream, predict SUCCESS (0/1) of the NEXT event. Exact-match accuracy.

Conditions:
  A real  : k immediately-preceding events from the SAME run (ordered)
  B shuf  : k events sampled at random from OTHER runs (destroyed provenance)
  C none  : no context
3 seeds of trace sampling; ~40 eval events each; temperature 0.

Hypothesis: A > B > C.  Canary: C should sit near the label base rate.
"""
import json
import os
import random
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
FAB = os.path.join(HERE, "..", "225-e1-interference-tick", "inventors-derby")
sys.path.insert(0, FAB)
from exp_glm1 import run_fabric  # noqa: E402

MODEL = "LiquidAI/lfm2.5-1.2b-instruct"
URL = "http://127.0.0.1:11434/api/generate"
SEEDS = (11, 22, 33)
N_EVAL = 40
K_SHOT = 8
N_THREADS = 4
DELTA = 12

def fmt(t, i, lag, err, pulse, ok):
    return (f"tick={t} sensor={i} lag={lag} err={err:+d} pulse={pulse:+d} "
            f"-> {'OK' if ok else 'BAD'}")

def make_streams():
    """Held-out runs (unseen configs vs E2 corpus: distinct seeds, mixed grammar)."""
    streams = []
    cfgs = [
        ("eval-ladder18", [0, 4, 7, 11, 14, 18]),
        ("eval-cohort3", [0, 0, 0, 15, 15, 15]),
        ("eval-laggard", [0, 0, 0, 0, 0, 21]),
    ]
    for name, lats in cfgs:
        for sd in (777, 888):
            r = run_fabric("interference", 1200, lats, K=2, pd=3,
                           delta=DELTA, drift=6, seed=sd)
            lag = {i: l for i, l in enumerate(lats)}
            evs = []
            for (t, i, pm, te) in r["emissions"]:
                evs.append(dict(t=t, i=i, lag=lag[i], err=te, pulse=pm,
                                ok=1 if r["resid"][t] <= DELTA else 0))
            streams.append((name, sd, evs))
    return streams

def ask_llm(prompt):
    body = json.dumps({
        "model": MODEL, "prompt": prompt, "stream": False,
        "options": {"temperature": 0, "num_predict": 8, "seed": 226},
    }).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                txt = json.loads(resp.read()).get("response", "")
            m = re.search(r"\b([01])\b", txt)
            return (int(m.group(1)) if m else None), txt.strip()
        except Exception as e:
            if attempt == 2:
                return None, f"ERR {e}"
            time.sleep(2)

def build_prompt(name, ctx, target):
    lines = "\n".join(fmt(c["t"], c["i"], c["lag"], c["err"], c["pulse"], c["ok"])
                      for c in ctx)
    q = fmt(target["t"], target["i"], target["lag"], target["err"],
            target["pulse"], target["ok"]).rsplit("->", 1)[0]
    return (f"Quilt fabric correction log ({name}). Each line: one correction "
            f"event. OK means the correction settled the cell; BAD means it "
            f"missed.\n{lines}\n{q}-> Reply with exactly one word: "
            f"OK or BAD. Do not explain.")

def parse_ok(txt):
    t = (txt or "").strip().upper()
    if t.startswith("OK"):
        return 1
    if t.startswith("BAD"):
        return 0
    m = re.search(r"\b(OK|BAD)\b", t)
    return 1 if (m and m.group(1) == "OK") else (0 if m else None)

def main():
    streams = make_streams()
    pool = [ev for _, _, evs in streams for ev in evs]
    base = sum(e["ok"] for e in pool) / len(pool)
    print(f"eval pool: {len(pool)} events, base OK rate {base:.3f}")

    results = {}
    for cond in ("A_real", "B_shuf", "B2_shuforder", "C_none"):
        accs, ns, fails, ok_ans = [], [], 0, []
        for sd in SEEDS:
            rng = random.Random(sd)
            # sample eval targets uniformly from the pool
            targets = rng.sample(pool, N_EVAL)
            jobs = []
            for tg in targets:
                if cond == "C_none":
                    ctx = []
                elif cond == "B_shuf":
                    ctx = [rng.choice(pool) for _ in range(K_SHOT)]
                else:  # A_real: k preceding events from same stream
                    src = next(evs for nm, s2, evs in streams
                               if tg in evs)
                    pos = src.index(tg)
                    ctx = src[max(0, pos - K_SHOT):pos]
                    if len(ctx) < K_SHOT:  # too early in stream -> pad
                        continue
                jobs.append((tg, ctx))
            def run_job(tg_ctx):
                tg, ctx = tg_ctx
                q = fmt(tg["t"], tg["i"], tg["lag"], tg["err"], tg["pulse"], tg["ok"]).rsplit("->", 1)[0]
                if cond == "C_none":
                    prompt = (f"Quilt fabric correction event. Predict if this "
                              f"correction settles the cell.\n{q}-> "
                              f"Reply with exactly one word: OK or BAD. "
                              f"Do not explain.")
                elif cond == "B2_shuforder":
                    src = next(evs for nm, s2, evs in streams if tg in evs)
                    pos = src.index(tg)
                    ctx = src[max(0, pos - K_SHOT):pos]
                    rng.shuffle(ctx)
                    prompt = build_prompt("eval", ctx, tg)
                else:
                    prompt = build_prompt("eval", ctx, tg)
                ans, raw = ask_llm(prompt)
                p = parse_ok(raw)
                return (p, tg["ok"], 1 if p == 1 else 0)
            with ThreadPoolExecutor(N_THREADS) as ex:
                outs = list(ex.map(run_job, jobs))
            outs = [o for o in outs if o[0] is not None]
            fails += len(jobs) - len(outs)
            if outs:
                accs.append(sum(p == y for p, y, _ in outs) / len(outs))
                ns.append(len(outs))
                ok_ans.append(sum(o for _, _, o in outs))
        mean = sum(a * n for a, n in zip(accs, ns)) / max(1, sum(ns))
        results[cond] = {"mean_acc": round(mean, 4),
                         "per_seed": [round(a, 4) for a in accs],
                         "n": sum(ns), "parse_fails": fails,
                         "ok_answer_frac": round(sum(ok_ans) / max(1, sum(ns)), 3)}
        print(f"{cond}: acc={mean:.3f} per-seed={[round(a,3) for a in accs]} "
              f"n={sum(ns)} parse_fails={fails}")
    results["base_rate"] = round(base, 4)
    with open(os.path.join(HERE, "outputs", "e1_icl_results.json"), "w") as f:
        json.dump(results, f, indent=1)
    print(json.dumps(results, indent=1))

if __name__ == "__main__":
    main()
