#!/usr/bin/env python3
"""run_night.py -- the hundred-boats night run (EDGE-BENCH lane).

N rounds; each round loops the 6 unordered pairs of the 4 local model
cells (one judgment query per pair, speaker alternates by round parity =
N*6 queries total). Every 25 rounds: checkpoint -- QUF snapshot +
state.json; the JSONL log is appended line-by-line and flushed per query.
Resume: re-run with the same --runs-dir, it picks up at rounds_done+1.

Runtime discipline: a calibration pass times each model (also warm-loads
it); if the projected night exceeds --max-minutes, N is CUT to fit and
the cut is announced and recorded. A runtime guard re-checks every round.

Usage:
  python3 tools/edgebench/run_night.py [--rounds 200] [--max-minutes 90]
                                       [--checkpoint-every 25] [--runs-dir DIR]
                                       [--reset] [--dry-run]
"""

import argparse
import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import edgebench as eb  # noqa: E402

PAIRS = [(eb.MODELS[i][0], eb.MODELS[j][0])
         for i in range(len(eb.MODELS))
         for j in range(i + 1, len(eb.MODELS))]

# Speaker clustering: consecutive queries share a model so Ollama's cache
# stays warm. Odd rounds: pair[0] speaks; even rounds: pair[1] speaks.
ODD_ORDER = list(PAIRS)
EVEN_ORDER = [("lfm", "qwen3"), ("lfm", "nano"), ("qwen3", "nano"),
              ("wesley", "nano"), ("qwen3", "wesley"), ("lfm", "wesley")]


def round_pairs(r):
    if r % 2 == 1:
        return [(a, b, a) for a, b in ODD_ORDER]
    return [(a, b, b) for a, b in EVEN_ORDER]


def calibrate(ollama, runs_dir, per_model=2):
    """Time each model with realistic turn prompts; writes
    calibration.json. Returns {short: avg_query_seconds}."""
    fab = eb.BenchFabric()
    times = {}
    for name, tag in eb.MODELS:
        cell = fab.cell_by_name(name)
        prompt = eb.turn_prompt(fab, cell)
        ts = []
        for _ in range(per_model):
            r = ollama.chat(tag, eb.SYSTEM_PROMPT, prompt)
            if not r["ok"]:
                print("CALIBRATION FAIL %s: %s" % (tag, r.get("error")))
                ts.append(30.0)
                continue
            eb.parse_op(r["content"], name)   # warm the exact code path
            ts.append(r["latency_s"])
        times[name] = sum(ts) / len(ts)
        print("calib %-7s %-28s %.2fs/query (load %.1fs)"
              % (name, tag, times[name], r.get("load_s", 0.0)), flush=True)
    with open(os.path.join(runs_dir, "calibration.json"), "w") as f:
        json.dump({"per_model_query_s": times,
                   "ts": time.time()}, f, indent=1)
    return times


def project(times):
    odd = sum(times[sp] for _a, _b, sp in round_pairs(1))
    even = sum(times[sp] for _a, _b, sp in round_pairs(2))
    return (odd + even) / 2.0


def load_state(runs_dir):
    p = os.path.join(runs_dir, "state.json")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)


def save_state(runs_dir, state):
    state["updated_ts"] = time.time()
    with open(os.path.join(runs_dir, "state.json"), "w") as f:
        json.dump(state, f, indent=1)


def checkpoint(fab, runs_dir, state, jsonl):
    buf = fab.export_quf()
    issues = eb.quf.verify_bytes(buf, "night.quf")
    if issues:
        print("QUF VERIFY FAIL (keeping previous checkpoint): %s" % issues)
        return False
    with open(os.path.join(runs_dir, "night.quf"), "wb") as f:
        f.write(buf)
    state["recent_events"] = list(fab.events)
    state["query_count"] = state.get("query_count", 0)
    save_state(runs_dir, state)
    jsonl.flush()
    os.fsync(jsonl.fileno())
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(prog="run_night.py")
    ap.add_argument("--rounds", type=int, default=200)
    ap.add_argument("--max-minutes", type=float, default=90.0)
    ap.add_argument("--checkpoint-every", type=int, default=25)
    ap.add_argument("--runs-dir",
                    default=os.path.join(_HERE, "runs"))
    ap.add_argument("--reset", action="store_true",
                    help="ignore existing state and start over")
    ap.add_argument("--dry-run", action="store_true",
                    help="calibrate + project only")
    args = ap.parse_args(argv)

    os.makedirs(args.runs_dir, exist_ok=True)
    ollama = eb.Ollama()

    state = None if args.reset else load_state(args.runs_dir)
    if state is None:
        state = {"config": {"rounds": args.rounds,
                            "max_minutes": args.max_minutes,
                            "checkpoint_every": args.checkpoint_every,
                            "models": [t for _n, t in eb.MODELS]},
                 "rounds_done": 0, "n": args.rounds,
                 "query_count": 0, "cut_note": None,
                 "started_ts": time.time()}

    if state["rounds_done"] == 0 or "calibration" not in state:
        print("calibrating (times each model, warms the cache)...",
              flush=True)
        times = calibrate(ollama, args.runs_dir)
        state["calibration"] = times
        per_round = project(times)
        fit = int((args.max_minutes * 60.0 * 0.90) / per_round) \
            if per_round > 0 else args.rounds
        if fit < args.rounds:
            state["cut_note"] = ("projected %.0f min for N=%d "
                                 "(%.1fs/round) -- cut to N=%d"
                                 % (per_round * args.rounds / 60.0,
                                    args.rounds, per_round, fit))
            print("PROJECTED OVER BUDGET: %s" % state["cut_note"], flush=True)
            args.rounds = fit
        state["n"] = args.rounds
        state["projected_s_per_round"] = per_round
        save_state(args.runs_dir, state)
        print("projection: %.1fs/round, N=%d -> ~%.0f min"
              % (per_round, state["n"],
                 per_round * state["n"] / 60.0), flush=True)
    else:
        print("resuming: rounds_done=%d n=%d queries=%d"
              % (state["rounds_done"], state["n"],
                 state.get("query_count", 0)), flush=True)
        args.rounds = state["n"]

    if args.dry_run:
        return 0

    # -- fabric: fresh or warm-loaded from the last checkpoint QUF --------
    quf_path = os.path.join(args.runs_dir, "night.quf")
    if state["rounds_done"] > 0 and os.path.exists(quf_path):
        with open(quf_path, "rb") as f:
            fab = eb.BenchFabric.import_quf(f.read())
        fab.events = state.get("recent_events", [])
        print("warm start from %s (round %d, %d edges)"
              % (quf_path, fab.round, len(fab.edge_table())), flush=True)
    else:
        fab = eb.BenchFabric()

    jsonl = open(os.path.join(args.runs_dir, "night.jsonl"),
                 "w" if state["rounds_done"] == 0 else "a")
    t_start = time.time()
    parse_ok = parse_tot = 0
    round_times = []

    for r in range(state["rounds_done"] + 1, state["n"] + 1):
        t_round = time.time()
        round_ops = []
        for a, b, speaker_name in round_pairs(r):
            speaker = fab.cell_by_name(speaker_name)
            prompt = eb.turn_prompt(fab, speaker)
            res = ollama.chat(eb.MODEL_TAG[speaker_name],
                              eb.SYSTEM_PROMPT, prompt)
            rec = {"type": "query", "round": r, "pair": [a, b],
                   "speaker": speaker_name,
                   "model": eb.MODEL_TAG[speaker_name], "ts": time.time()}
            if not res["ok"]:
                rec.update({"parse_ok": False, "op": None,
                            "fail": "infra:" + str(res.get("error"))[:80],
                            "content": "", "latency_s":
                                round(res["latency_s"], 3),
                            "eval_count": 0, "tok_s": 0.0})
            else:
                op, why = eb.parse_op(res["content"], speaker_name)
                rec.update({"parse_ok": op is not None, "op": op,
                            "fail": why,
                            "content": res["content"][:200],
                            "latency_s": round(res["latency_s"], 3),
                            "eval_count": res["eval_count"],
                            "tok_s": (round(res["eval_count"]
                                            / res["eval_dur_s"], 1)
                                      if res["eval_dur_s"] > 0 else 0.0)})
                if op is not None:
                    ev = fab.apply_op(speaker, op)
                    fab.event(ev)
                    round_ops.append("%s:%s" % (speaker_name, op["op"]))
            parse_tot += 1
            parse_ok += 1 if rec["parse_ok"] else 0
            jsonl.write(json.dumps(rec) + "\n")
            jsonl.flush()
            state["query_count"] += 1
        emergent = fab.round_tick()
        warm = fab.warmth()
        jsonl.write(json.dumps({
            "type": "round", "round": r, "warmth": warm,
            "warmth_f": round(warm / 32768.0, 4),
            "edges": fab.edge_table(),
            "acts": {fab.cells[c].name: fab.cells[c].act
                     for c in fab.order},
            "emergent": emergent, "ops": round_ops}) + "\n")
        jsonl.flush()
        state["rounds_done"] = r
        dt = time.time() - t_round
        round_times.append(dt)
        avg = sum(round_times[-20:]) / len(round_times[-20:])
        print("round %3d/%d  %.1fs  ops[%s]  parse %d/%d  warmth %+.3f  "
              "eta %.0fm"
              % (r, state["n"], dt, " ".join(round_ops) or "-",
                 parse_ok, parse_tot, warm / 32768.0,
                 avg * (state["n"] - r) / 60.0), flush=True)

        if r % args.checkpoint_every == 0 or r == state["n"]:
            checkpoint(fab, args.runs_dir, state, jsonl)
            elapsed = time.time() - t_start
            projected = elapsed + avg * (state["n"] - r)
            if projected > args.max_minutes * 60.0 and r < state["n"]:
                state["cut_note"] = ("runtime guard: projected %.0f min > "
                                     "%.0f, stopping at round %d"
                                     % (projected / 60.0,
                                        args.max_minutes, r))
                state["n"] = r
                print("RUNTIME GUARD: %s" % state["cut_note"], flush=True)
                checkpoint(fab, args.runs_dir, state, jsonl)
                break

    checkpoint(fab, args.runs_dir, state, jsonl)
    jsonl.close()
    tot_min = (time.time() - t_start) / 60.0
    print("=" * 60, flush=True)
    print("night complete: %d rounds, %d queries, parse rate %.1f%%, "
          "%.1f min wall" % (state["rounds_done"], state["query_count"],
                             100.0 * parse_ok / max(1, parse_tot),
                             tot_min), flush=True)
    if state.get("cut_note"):
        print("cut: %s" % state["cut_note"], flush=True)
    print("final warmth %+.4f | %d edges | QUF at %s"
          % (fab.warmth() / 32768.0, len(fab.edge_table()), quf_path),
          flush=True)
    print("next: python3 tools/edgebench/report.py", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
