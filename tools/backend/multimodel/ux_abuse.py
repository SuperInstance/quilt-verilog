#!/usr/bin/env python3
"""ux_abuse.py -- Seed-2.0-mini (DeepInfra) as the adversarial UX user
(multi-model backend). It WRITES a shell script of hostile CLI abuse for
tools/quf.py; we RUN what it wrote for real in a sandbox and grade every
invocation: traceback = finding (the tool's fault), clean error/usage =
handled, script-syntactic breakage = skipped (the model's, logged).
"""
import json
import os
import subprocess
import stat
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, _HERE)
import mm  # noqa: E402

PY = sys.executable
QUF = os.path.join(_ROOT, "tools", "quf.py")

PROMPT = [
    {"role": "system", "content":
     "You are a hostile user who wants to break a command-line tool and "
     "embarrass its author. You write a bash script of abuse: wrong "
     "flags, absurd arguments, weird paths, piped stdin, interrupted "
     "output, hostile filenames. Output ONLY a bash script. Rules: the "
     "tool is invoked as: python3 tools/quf.py <subcommand> <args...> "
     "(subcommands: create IN.json OUT.quf [--digest], info FILE, dump "
     "FILE, verify FILE, hex FILE OUT, selftest). Work inside a "
     "temporary dir; do not touch anything outside it; no network; no "
     "sudo; no infinite loops; at most 30 invocations."},
    {"role": "user", "content":
     "Write the abuse script. Make the author cry."},
]


def main():
    try:
        script, meta = mm.seed(PROMPT, timeout=240, temperature=1.0)
    except mm.MMError as ex:
        print("seed UNAVAILABLE: %s" % ex)
        open(os.path.join(_HERE, "runs", "ux_abuse.jsonl"), "w").write(
            json.dumps({"error": str(ex)}) + "\n")
        return
    # strip fences if fenced
    body = script
    if "```" in body:
        parts = body.split("```")
        for p in parts:
            if "quf.py" in p:
                body = p
                if body.lower().startswith("bash"):
                    body = body[4:]
                break
    results = []
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "abuse.sh")
        with open(path, "w") as f:
            f.write("set +e\n" + body + "\n")
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
        r = subprocess.run(["bash", path], capture_output=True, text=True,
                           timeout=120, cwd=d,
                           env={**os.environ, "QUF": QUF, "PY": PY})
        # grade per-invocation from the transcript: count tracebacks
        tb = [ln for ln in r.stderr.splitlines() + r.stdout.splitlines()
              if "Traceback" in ln]
        results = {"rc": r.returncode, "tracebacks": len(tb),
                   "stdout_head": r.stdout[:1200],
                   "stderr_head": r.stderr[:1200],
                   "script": body, "model": meta.get("model")}
    with open(os.path.join(_HERE, "runs", "ux_abuse.jsonl"), "w") as f:
        f.write(json.dumps(results) + "\n")
    print("seed script ran: rc=%s, tracebacks=%d"
          % (results["rc"], results["tracebacks"]))
    if results["tracebacks"]:
        print("FINDINGS (traceback lines):")
        for ln in tb[:5]:
            print("  " + ln[:100])
    else:
        print("no tracebacks: every abuse handled cleanly")


if __name__ == "__main__":
    main()
