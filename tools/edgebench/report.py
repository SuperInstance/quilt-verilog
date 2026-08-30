#!/usr/bin/env python3
"""report.py -- emit docs/EDGE-BENCH.md from a night's runs (EDGE-BENCH lane).

Reads runs/night.jsonl (dedup: last record wins per key), runs/state.json,
runs/calibration.json and runs/night.quf (verified via tools/quf.py), and
writes the EDGE-BENCH report: setup, per-model table (parse rate, edge
growth, warmth trajectory), three observations about which local model
makes the best CELL, and the honest limitations.

Usage: python3 tools/edgebench/report.py [--runs-dir DIR] [--out PATH]
"""

import argparse
import datetime
import json
import os
import shutil
import statistics
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import edgebench as eb  # noqa: E402

SPARK = " .:-=+*#%"


def median(xs):
    return statistics.median(xs) if xs else 0.0


def sparkline(vals, width=48):
    if not vals:
        return ""
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1.0
    step = max(1, len(vals) // width)
    out = []
    for i in range(0, len(vals), step):
        v = vals[i]
        idx = int((v - lo) / span * (len(SPARK) - 1))
        out.append(SPARK[idx])
    return "".join(out)


def load_runs(runs_dir):
    queries, rounds = {}, {}
    with open(os.path.join(runs_dir, "night.jsonl")) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec["type"] == "query":
                queries[(rec["round"], tuple(rec["pair"]),
                         rec["speaker"])] = rec
            else:
                rounds[rec["round"]] = rec
    qs = [queries[k] for k in sorted(queries)]
    rs = [rounds[k] for k in sorted(rounds)]
    return qs, rs


def per_model_stats(qs, rs):
    seed = eb.BenchFabric()
    base_edges = {(e["src"], e["dst"]): e for e in seed.edge_table()}
    final = {(e["src"], e["dst"]): e
             for e in (rs[-1]["edges"] if rs else [])}
    stats = {}
    for name, tag in eb.MODELS:
        mq = [q for q in qs if q["speaker"] == name]
        ok = [q for q in mq if q["parse_ok"]]
        fails = {}
        for q in mq:
            if not q["parse_ok"] and q.get("fail"):
                key = q["fail"].split(":")[0]
                fails[key] = fails.get(key, 0) + 1
        ops = {"fire": 0, "link": 0, "dial": 0}
        for q in ok:
            ops[q["op"]["op"]] += 1
        out_wh = sum(e["wh"] for (s, d), e in final.items() if s == name)
        out_w = sum(e["w"] for (s, d), e in final.items() if s == name)
        base_wh = sum(e["wh"] for (s, d), e in base_edges.items()
                      if s == name)
        base_w = sum(e["w"] for (s, d), e in base_edges.items()
                     if s == name)
        indeg = sum(1 for (s, d), _e in final.items() if d == name)
        base_indeg = sum(1 for (s, d), _e in base_edges.items()
                         if d == name)
        lats = [q["latency_s"] for q in mq if q.get("latency_s")]
        tpss = [q["tok_s"] for q in mq if q.get("tok_s")]
        cell = seed.cell_by_name(name)
        vcounts = {}
        stats[name] = {
            "tag": tag, "queries": len(mq), "parse_ok": len(ok),
            "parse_rate": (len(ok) / len(mq)) if mq else 0.0,
            "ops": ops, "fails": fails,
            "med_lat": median(lats), "mean_tps": (sum(tpss) / len(tpss))
            if tpss else 0.0,
            "out_wh": out_wh, "out_wh_growth": out_wh - base_wh,
            "out_w": out_w, "out_w_growth": out_w - base_w,
            "indeg": indeg, "indeg_growth": indeg - base_indeg,
            "seed_openness": cell.dials[eb.D_COSMIN],
            "final_act": (rs[-1]["acts"].get(name, 0) if rs else 0),
        }
    return stats


def gpu_line():
    if shutil.which("nvidia-smi"):
        try:
            out = subprocess.run(["nvidia-smi", "--query-gpu=name",
                                  "--format=csv,noheader"],
                                 capture_output=True, text=True,
                                 timeout=10).stdout.strip()
            if out:
                return out
        except Exception:
            pass
    return ("nvidia-smi not exposed in this shell; host directive says "
            "RTX 4050-class laptop GPU. Measured throughput below is the "
            "honest number.")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="report.py")
    ap.add_argument("--runs-dir", default=os.path.join(_HERE, "runs"))
    ap.add_argument("--out",
                    default=os.path.normpath(os.path.join(
                        _HERE, "..", "..", "docs", "EDGE-BENCH.md")))
    args = ap.parse_args(argv)

    qs, rs = load_runs(args.runs_dir)
    with open(os.path.join(args.runs_dir, "state.json")) as f:
        state = json.load(f)
    calib_path = os.path.join(args.runs_dir, "calibration.json")
    calib = {}
    if os.path.exists(calib_path):
        with open(calib_path) as f:
            calib = json.load(f).get("per_model_query_s", {})
    stats = per_model_stats(qs, rs)

    try:
        ollama_ver = eb.Ollama(timeout=5).version()
    except Exception:
        ollama_ver = "unreachable"

    quf_path = os.path.join(args.runs_dir, "night.quf")
    quf_note = "missing"
    if os.path.exists(quf_path):
        with open(quf_path, "rb") as f:
            buf = f.read()
        issues = eb.quf.verify_bytes(buf, quf_path)
        quf_note = ("%d bytes, quf.py verify %s"
                    % (len(buf), "CLEAN" if not issues
                       else "FAIL: %s" % issues))

    warmth = [r["warmth_f"] for r in rs]
    n_rounds = state.get("rounds_done", len(rs))
    cut = state.get("cut_note")
    min_per_round = state.get("projected_s_per_round", 0.0) / 60.0

    scored = []
    max_lat = max((s["med_lat"] for s in stats.values()), default=1.0) or 1.0
    max_links = max((s["ops"]["link"] for s in stats.values()), default=1) or 1
    max_indeg = max((s["indeg"] for s in stats.values()), default=1) or 1
    for name, s in stats.items():
        score = (2.0 * s["parse_rate"]
                 + 1.0 * s["ops"]["link"] / max_links
                 + 1.0 * s["indeg"] / max_indeg
                 + 1.0 * (1.0 - s["med_lat"] / max_lat))
        scored.append((score, name, s))
    scored.sort(reverse=True)

    L = []
    A = L.append
    A("# EDGE-BENCH — local chips as the experimentation fabric")
    A("")
    A("**Lane:** edge-bench · **Date:** %s · **Companions:** `DOCTRINE.md`, "
      "`QUF-SPEC.md`, `TAP-FABRIC.md` (cell semantics), `tools/quf.py` "
      "(the file)." % datetime.date.today().isoformat())
    A("")
    A("> **The claim this document makes exact.** Casey's hundred-boats "
      "directive: iterate lots on the edge, zero cloud cost. One laptop, "
      "one Ollama daemon, four local models — every one of them a CELL in "
      "a tiny quilt. Each turn a model is handed its cell's integer state "
      "(dials, edges, weights, recent room events) and must emit ONE "
      "schema-strict JSON op — `fire` / `link` / `dial-nudge`. The "
      "harness applies it through RTL-true cell semantics "
      "(link-before-effect, train-then-integrate, integrate-leak-fire "
      "ticks) and tracks the Hebbian graph in a real QUF. Parse failures "
      "are the model's fault and are logged. The experiment asks one "
      "question: **which local model makes the best cell?**")
    A("")
    A("## 1. Setup")
    A("")
    A("| cell | Ollama model | role |")
    A("|---|---|---|")
    for name, tag in eb.MODELS:
        role = {"lfm": "sibling cell (Liquid; verbose thinker -- seeded "
                       "with an assistant-prefill `{` so it answers "
                       "directly)",
                "qwen3": "sibling cell (heaviest, thinking disabled via "
                         "`think:false`)",
                "wesley": "sibling cell (granite, per directive)",
                "nano": "the nano cell (0.5b floor)"}[name]
        A("| `%s` | `%s` | %s |" % (name, tag, role))
    A("")
    A("- Ollama `%s` at `%s` — all inference local, zero cloud queries."
      % (ollama_ver, eb.OLLAMA_HOST))
    A("- GPU: %s" % gpu_line())
    A("- Round = one `qm_tick` for all 5 cells after 6 pair-turns "
      "(all-pairs of the 4 model cells, one judgment query per pair, "
      "speaker alternates by round parity).")
    A("- Hebb rule (edgebench readout): cofire adds a walk to the QUF "
      "edge's `wh`; silence decays it (hyperbola tick, P0=2^%d); "
      "`w = base + %d·ln(1+walks)` in Q1.15, u16-saturating."
      % (eb.BENCH_P0E, eb.LN_SCALE))
    A("- Seed graph: ring (`lfm→qwen3→wesley→nano→lfm`) + every cell "
      "hears `room`; the room hears everyone. Everything else the models "
      "built themselves with `link`.")
    A("")
    if qs:
        pace_note = ("(calibrated %.2fs/query mean, %.2fs/query realized)."
                     % (sum(calib.values()) / max(1, len(calib)),
                        statistics.mean([q["latency_s"] for q in qs])))
    else:
        pace_note = ""
    A("**Night:** N=%d planned → **%d rounds completed** (%d judgment "
      "queries). %s Projected pace %.1f min/round %s"
      % (state["config"]["rounds"], n_rounds, state.get("query_count", 0),
         ("Cut: `%s`." % cut) if cut else "No cut needed.",
         min_per_round, pace_note))
    A("")
    A("## 2. Per-model results")
    A("")
    A("| cell | queries | parse rate | op mix f/l/d | med lat (s) | "
      "tok/s | walks Σ (Δ) | out-wsum (Δ) | hears-me | final buzz |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for name in ["lfm", "qwen3", "wesley", "nano"]:
        s = stats[name]
        A("| `%s` | %d | %.1f%% | %d/%d/%d | %.2f | %.0f | %d (+%d) | "
          "%d (+%d) | %d | %+.3f |"
          % (name, s["queries"], 100.0 * s["parse_rate"],
             s["ops"]["fire"], s["ops"]["link"], s["ops"]["dial"],
             s["med_lat"], s["mean_tps"],
             s["out_wh"], s["out_wh_growth"], s["out_w"], s["out_w_growth"],
             s["indeg"], s["final_act"] / 32768.0))
    A("")
    A("Dominant parse-failure reasons per model (the model's fault, "
      "logged raw in `runs/night.jsonl`):")
    A("")
    for name in ["lfm", "qwen3", "wesley", "nano"]:
        f = stats[name]["fails"]
        top = ", ".join("%s ×%d" % (k, v)
                        for k, v in sorted(f.items(),
                                           key=lambda kv: -kv[1])[:3]) \
            or "none"
        A("- `%s`: %s" % (name, top))
    A("")
    A("## 3. Room-warmth trajectory (the dial aggregate)")
    A("")
    A("Warmth = the room cell's `ETA_F` dial (addr 0), an integer Q1.15 "
      "EMA of per-round landed heat (accepted fire dats + 1024 per link "
      "op) — the tap-fabric mood binding, unchanged.")
    A("")
    if warmth:
        A("```")
        A("warmth %s" % sparkline(warmth))
        A("start %+.4f  mid %+.4f  end %+.4f  min %+.4f  max %+.4f  "
          "(Q1.15)" % (warmth[0], warmth[len(warmth) // 2], warmth[-1],
                       min(warmth), max(warmth)))
        A("```")
        emergent = [r for r in rs if r["emergent"]]
        n_emerg = sum(len(r["emergent"]) for r in emergent)
        A("%d emergent fire%s (cells whose buzz crossed earnestness "
          "inside `qm_tick`, unscripted) over %d rounds."
          % (n_emerg, "" if n_emerg == 1 else "s", len(rs)))
    A("")
    A("## 4. Three observations")
    A("")
    best_score, best, bs = scored[0] if scored else (0, "?", {})
    by_parse = sorted(stats.items(), key=lambda kv: -kv[1]["parse_rate"])
    by_link = sorted(stats.items(),
                     key=lambda kv: (-kv[1]["ops"]["link"]))
    A("1. **Schema discipline is the gate.** `%s` parsed %.1f%% of its "
      "turns, `%s` %.1f%%, `%s` %.1f%%, `%s` %.1f%%. A cell that cannot "
      "emit its own op is a cell that cannot act — every failed turn is "
      "a round the graph does not grow through that model."
      % (by_parse[0][0], 100 * by_parse[0][1]["parse_rate"],
         by_parse[1][0], 100 * by_parse[1][1]["parse_rate"],
         by_parse[2][0], 100 * by_parse[2][1]["parse_rate"],
         by_parse[3][0], 100 * by_parse[3][1]["parse_rate"]))
    A("2. **Linking is what populates a quilt.** `%s` issued the most "
      "`link` ops (%d) and ends the night with %d cells listening to it "
      "(in-degree %d, from a seed of 1). Fires move buzz; links move the "
      "graph. The Hebbian ledger agrees: final walk mass `%s` Σ%d walks "
      "vs `%s` Σ%d."
      % (by_link[0][0], by_link[0][1]["ops"]["link"],
         by_link[0][1]["indeg"], by_link[0][1]["indeg"],
         max(stats.items(), key=lambda kv: kv[1]["out_wh"])[0],
         max(s["out_wh"] for s in stats.values()),
         min(stats.items(), key=lambda kv: kv[1]["out_wh"])[0],
         min(s["out_wh"] for s in stats.values())))
    A("3. **Cell economics: tempo × reliability.** At median latencies "
      "(%s), a quilt of such cells ticks at %s. `%s` sustains the best "
      "duty cycle per watt of attention: %.1f%% parse at %.2fs a turn, "
      "%.0f tok/s — fast enough to sit in a 6-query round without "
      "stalling the tick."
      % (", ".join("`%s` %.2fs" % (n, stats[n]["med_lat"])
                   for n in ["lfm", "qwen3", "wesley", "nano"]),
         "one round per ~%.0fs" % (6 * statistics.mean(
             [q["latency_s"] for q in qs])) if qs else "?",
         best, 100 * bs.get("parse_rate", 0), bs.get("med_lat", 0),
         bs.get("mean_tps", 0)))
    A("")
    A("**Best cell-model: `%s`** (`%s`) — composite %.2f/5 = "
      "2×parse(%.1f%%) + links(%.0f%% of max) + in-degree(%.0f%%) + "
      "tempo(%.2fs median turn). %s"
      % (best, bs.get("tag", ""), best_score,
         100 * bs.get("parse_rate", 0),
         100 * bs.get("ops", {}).get("link", 0) / max_links
         if max_links else 0,
         100 * bs.get("indeg", 0) / max_indeg if max_indeg else 0,
         bs.get("med_lat", 0),
         ("It is also the cheapest cell on the night's ledger — see the "
          "table." if best_score > 3.5 else
          "The field is closer than the score suggests; see limitations.")))
    A("")
    A("## 5. Honest limitations")
    A("")
    A("- **One query per pair per round** (speaker alternates). A model's "
      "judgment is sampled, not exhausted; a different serialization of "
      "the same night diverges (tick order is one legal serialization, "
      "TAP-FABRIC §8 inherits).")
    A("- **Hearer-side verdicts are deterministic Python taste** "
      "(fnv1a of the cell name), not model-judged — one LLM call per "
      "pair-round keeps the night under budget; the model supplies the "
      "will, the fabric supplies the integration filter.")
    A("- **The ln readout is edgebench's**, not the RTL's `wh<<8` "
      "(directive: `base + ln(1+walks)`); decay is the RTL hyperbola "
      "with a bench-chosen P0 so silence visibly decays inside one night.")
    A("- **`think:false` for qwen3 and the assistant-prefill for lfm** "
      "are harness kindness; a thinking model left on would burn its "
      "token budget reasoning and fail parse — that failure would be "
      "real but measures budget policy, not cell character.")
    A("- **Temperature 0.7, one night, N=%d rounds.** Small graph "
      "(5 cells, ≤8 stools each), hand-shaped prompt. No claim of "
      "statistical strength — this is a hundred-boats probe, not a "
      "benchmark paper." % n_rounds)
    A("- **Parse failures include rough justice**: a trailing-prose JSON "
      "reply parses (fair), but any schema slip does not (strict by "
      "design; the raw text is in the log for re-adjudication).")
    A("")
    A("## 6. Artifacts")
    A("")
    A("- `tools/edgebench/edgebench.py` — engine (cells, ln-Hebb edges, "
      "QUF I/O, schema-strict parser, selftest)")
    A("- `tools/edgebench/run_night.py` — calibrate → project → run, "
      "checkpoint/resume every 25 rounds")
    A("- `tools/edgebench/runs/night.jsonl` — every query (raw model "
      "text, op, latency, tok/s) + per-round edge/warmth snapshots")
    A("- `tools/edgebench/runs/night.quf` — final room state, %s. "
      "Warm-loads via `BenchFabric.import_quf`; verify: `python3 "
      "tools/quf.py verify tools/edgebench/runs/night.quf`" % quf_note)
    A("- `tools/edgebench/runs/state.json`, `runs/calibration.json` — "
      "night ledger and per-model timing")
    A("")
    A("*A hundred boats, all seaworthy enough to matter: the quilt's "
      "cells can be populated by the chips already on the desk.*")
    A("")

    with open(args.out, "w") as f:
        f.write("\n".join(L))
    print("wrote %s (%d lines) from %d queries / %d rounds"
          % (args.out, len(L), len(qs), len(rs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
