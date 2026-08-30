#!/usr/bin/env python3
"""formal/audit_snapshot.py — deterministic formal-verdict snapshot harness.

For each formal/*.sby, WITHOUT re-running solvers:
  1. sha256 (short) of the .sby file and of workdir/model/design.il if present
  2. last run's verdict (from workdir logfile DONE line / status file),
     engine name, depth reached, assertion hits (file:line) and
     counterexample trace refs
  3. writes formal/AUDIT-SNAPSHOT.json and prints a human-readable table

  --check  recompute and diff against the committed snapshot;
           exit 0 identical, nonzero on drift.

stdlib only. Absent workdir -> "not-run-on-this-bench" (never fabricated).
"""

import argparse
import hashlib
import json
import os
import re
import sys

TERMINAL = ("PASS", "FAIL", "UNKNOWN", "ERROR")
SNAPSHOT_NAME = "AUDIT-SNAPSHOT.json"


def short_sha(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()[:12]
    except OSError:
        return None


def engines_from_sby(sby_path):
    """Extract engine names from the [engines] section."""
    engines = []
    in_engines = False
    try:
        with open(sby_path) as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    in_engines = stripped == "[engines]"
                    continue
                if in_engines and stripped and not stripped.startswith("#"):
                    engines.append(stripped)
    except OSError:
        pass
    return engines


def parse_logfile(logpath):
    """Extract last-run verdict, depth, assertion hits, counterexample refs."""
    info = {
        "verdict": None,
        "tasks": [],
        "depth": None,
        "assertion_hits": [],
        "counterexamples": [],
        "log_tail": None,
    }
    try:
        with open(logpath, errors="replace") as f:
            lines = f.read().splitlines()
    except OSError:
        return info
    info["log_tail"] = lines[-1] if lines else None

    max_step = -1
    reached_bound = None
    per_task = {}
    for line in lines:
        m = re.search(r"DONE \((PASS|FAIL|UNKNOWN|ERROR|ERROR_)", line)
        if m:
            info["verdict"] = m.group(1)
        # summary: engine per-task verdicts e.g. "engine_0.basecase: Status returned by engine for basecase: FAIL"
        m = re.search(r"Status returned by engine for (\S+): (\w+)", line)
        if m:
            per_task[m.group(1)] = m.group(2).upper()
        m = re.search(r"Reached bound (\d+)", line)
        if m:
            reached_bound = max(reached_bound or 0, int(m.group(1)))
        m = re.search(r"in step (\d+)", line)
        if m:
            max_step = max(max_step, int(m.group(1)))
        # Assert failed in <module>: <file>:<line.range> (name)
        m = re.search(r"Assert failed in \S+: (\S+:\d+(?:\.\d+-\d+\.\d+)?)", line)
        if m:
            hit = m.group(1)
            if hit not in info["assertion_hits"]:
                info["assertion_hits"].append(hit)
        # summary line: "failed assertion mod.name at file:line.col in step N"
        m = re.search(r"failed assertion \S+ at (\S+:\d+(?:\.\d+)?) in step (\d+)", line)
        if m and m.group(1) not in info["assertion_hits"]:
            info["assertion_hits"].append(m.group(1))
    info["tasks"] = [{"task": k, "verdict": v} for k, v in sorted(per_task.items())]
    if reached_bound is not None:
        info["depth"] = reached_bound
    elif max_step >= 0:
        info["depth"] = max_step
    return info


def parse_status_file(status_path):
    """status file: one line per task: VERDICT retcode/... (sby internal)."""
    verdicts = []
    try:
        with open(status_path) as f:
            for line in f:
                parts = line.split()
                if parts and parts[0].upper() in TERMINAL:
                    verdicts.append(parts[0].upper())
    except OSError:
        pass
    return verdicts


def find_counterexamples(workdir):
    """Trace files in engine dirs (vcd/yw) = counterexample/witness artifacts."""
    refs = []
    for root, _dirs, files in os.walk(workdir):
        if os.sep + "src" + os.sep in root or os.sep + "model" + os.sep in root:
            continue
        for fn in sorted(files):
            if fn.endswith((".vcd", ".yw", ".vcd.symlnk")):
                refs.append(os.path.relpath(os.path.join(root, fn), workdir))
    return refs


def audit_sby(sby_path, formal_dir):
    rel = os.path.relpath(sby_path, formal_dir)
    workdir = sby_path[:-len(".sby")]
    entry = {"relpath": rel}
    entry["file_sha"] = short_sha(sby_path)
    entry["engines"] = engines_from_sby(sby_path)
    if not os.path.isdir(workdir):
        entry["workdir"] = "not-run-on-this-bench"
        entry["model_sha"] = None
        entry["verdict"] = "NOT-RUN"
        entry["depth"] = None
        entry["assertion_hits"] = []
        entry["counterexamples"] = []
        entry["workdir_mtime"] = None
        return entry

    entry["workdir"] = os.path.relpath(workdir, os.path.dirname(formal_dir))
    entry["model_sha"] = short_sha(os.path.join(workdir, "model", "design.il"))
    log = parse_logfile(os.path.join(workdir, "logfile.txt"))
    status_verdicts = parse_status_file(os.path.join(workdir, "status"))
    verdict = log["verdict"]  # DONE line is authoritative for a completed run
    if verdict is None:
        if status_verdicts:
            verdict = "/".join(status_verdicts)  # sby wrote terminal status lines
        else:
            # workdir exists but run produced no DONE line and no status file:
            # per-task statuses may exist mid-run; never report them as overall PASS.
            verdict = "INCOMPLETE"
    entry["verdict"] = verdict
    entry["depth"] = log["depth"]
    entry["assertion_hits"] = log["assertion_hits"]
    entry["counterexamples"] = find_counterexamples(workdir)
    try:
        entry["workdir_mtime"] = int(os.path.getmtime(workdir))
    except OSError:
        entry["workdir_mtime"] = None
    if log["tasks"]:
        entry["tasks"] = log["tasks"]
    return entry


def build_snapshot(formal_dir):
    return {
        "schema": 1,
        "entries": [
            audit_sby(os.path.join(formal_dir, fn), formal_dir)
            for fn in sorted(os.listdir(formal_dir))
            if fn.endswith(".sby")
        ],
    }


def render_table(snapshot):
    rows = []
    for e in snapshot["entries"]:
        rows.append([
            e["relpath"],
            e.get("verdict", "?"),
            str(e.get("depth") if e.get("depth") is not None else "-"),
            ",".join(e.get("engines", [])) or "-",
            e.get("file_sha") or "-",
            e.get("model_sha") or "-",
            ";".join(e.get("assertion_hits", [])) or "-",
            ";".join(e.get("counterexamples", [])) or "-",
        ])
    hdr = ["SBY", "VERDICT", "DEPTH", "ENGINE(S)", "SBY_SHA", "MODEL_SHA", "ASSERT-HITS", "COUNTEREX"]
    widths = [max(len(str(r[i])) for r in rows + [hdr]) for i in range(len(hdr))]
    lines = []
    hdr = ["SBY", "VERDICT", "DEPTH", "ENGINE(S)", "SBY_SHA", "MODEL_SHA", "ASSERT-HITS", "COUNTEREX"]
    lines.append("  ".join(h.ljust(w) for h, w in zip(hdr, widths)))
    lines.append("  ".join("-" * w for w in widths))
    for r in rows:
        lines.append("  ".join(str(c).ljust(w) for c, w in zip(r, widths)))
    return "\n".join(lines)


def drift_diff(committed, recomputed):
    """Compare entries ignoring nothing; report drift per sby."""
    def key(snap):
        return {e["relpath"]: e for e in snap.get("entries", [])}
    c, r = key(committed), key(recomputed)
    diffs = []
    for rel in sorted(set(c) | set(r)):
        if rel not in c:
            diffs.append(f"+ {rel}: new sby, not in committed snapshot")
        elif rel not in r:
            diffs.append(f"- {rel}: sby removed")
        else:
            fields = ("file_sha", "model_sha", "verdict", "depth", "engines",
                      "assertion_hits", "counterexamples")
            for fld in fields:
                if c[rel].get(fld) != r[rel].get(fld):
                    diffs.append(f"~ {rel}: {fld}: committed={c[rel].get(fld)!r} bench={r[rel].get(fld)!r}")
    return diffs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--formal-dir", default=here)
    ap.add_argument("--output", default=os.path.join(here, SNAPSHOT_NAME))
    ap.add_argument("--check", action="store_true",
                    help="recompute and diff vs committed snapshot; exit nonzero on drift")
    args = ap.parse_args()

    snapshot = build_snapshot(args.formal_dir)
    print(render_table(snapshot))

    if args.check:
        try:
            with open(args.output) as f:
                committed = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"CHECK FAIL: cannot read committed snapshot {args.output}: {exc}")
            return 2
        diffs = drift_diff(committed, snapshot)
        if diffs:
            print(f"CHECK FAIL: {len(diffs)} drift item(s) between bench and committed {SNAPSHOT_NAME}:")
            for d in diffs:
                print("  " + d)
            return 1
        print(f"CHECK PASS: bench matches committed {SNAPSHOT_NAME}")
        return 0

    with open(args.output, "w") as f:
        json.dump(snapshot, f, indent=2, sort_keys=False)
        f.write("\n")
    print(f"\nwrote {args.output} ({len(snapshot['entries'])} sby entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
