#!/usr/bin/env python3
"""oracle_poll.py -- local ollama models as INDEPENDENT ORACLES (multi-
model backend). qwen3:8b and deepseek-r1:8b each re-derive expected
QUF-tool behavior for sampled cases FROM THE SPEC ALONE (no Python code
shown). Ground truth comes from the committed benches. A 3-way
disagreement (Python vs RTL vs oracle) where the oracle's reading is
defensible is flagged as a SPEC-AMBIGUITY finding -- the highest-value
class per the amplification.
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import mm  # noqa: E402

SPEC = """QUF spec excerpt (docs/QUF-SPEC.md, the operative rules):
- Magic "QUF\\0", version 1, little-endian only.
- Header: counted KV pairs (name, type, value). Types: u8..f64, bool,
  string (u32 len + bytes), array (elem type + count + elems).
- Known KVs: cell_count, edge_count, route_count, edge.k (1..16),
  tick_period, align (power of two, >= 8). Names <= 255 bytes.
- Section table: (name, kind, offset u64, size u64). Known sections:
  dials (cell_count x 16 x u16), edges (count x (12 + edge.k) B),
  routing (count x 2 B), ticks (u32 tpw + cell_count x u32 phases).
- Constraint rules (spec section 7): files < 4 GiB; nonzero u64 high
  words are invalid; sections must not overlap; declared content must
  be inside the file.
- verify = structural verification; the tool exits nonzero when it
  finds issues.
- Writer canonicalization: sections at aligned ascending offsets; the
  whole file padded to align."""

CASES = [
    {"id": "trunc-mid-content",
     "q": "A QUF file's section table declares a ticks section ending at "
          "byte 392. The file is cut to 390 bytes and handed to verify. "
          "PASS or FAIL, and why?",
     "truth": "FAIL", "why": "declared content extends past EOF"},
    {"id": "payload-bitflip-nodigest",
     "q": "One bit inside the dials payload bytes is flipped. The file "
          "has NO digest KV. verify is run. PASS or FAIL, and what does "
          "that mean for a warm boot?",
     "truth": "PASS",
     "why": "structure intact; without a content digest the corruption "
            "is invisible -- the integrity gap that motivated quf.sha256"},
    {"id": "align-31",
     "q": "A file has align=31 (not a power of two) in its header, but "
          "every section offset happens to be 8-aligned. verify verdict?",
     "truth": "FAIL", "why": "align must be a power of two >= 8"},
    {"id": "empty-file",
     "q": "A zero-byte file is handed to verify. Verdict and behavior?",
     "truth": "FAIL", "why": "cannot even read the 16-byte header"},
    {"id": "tpw-32",
     "q": "A JSON doc asks the writer for ticksched tpw=32. The writer "
          "computes tick_period = 2^tpw for the header. What must the "
          "writer do?",
     "truth": "REJECT",
     "why": "2^32 does not fit the u32 tick_period KV"},
    {"id": "dup-dials-sections",
     "q": "A file's table lists TWO dials sections (different offsets, "
          "both well-formed). verify verdict?",
     "truth": "FAIL",
     "why": "duplicate section names are ambiguous (readers disagree "
            "which one counts)"},
    {"id": "trailing-garbage",
     "q": "128 bytes of garbage are APPENDED after the last declared "
          "section (all content intact). verify verdict?",
     "truth": "PASS",
     "why": "readers are table-driven; bytes past declared content are "
            "don't-care (documented behavior)"},
    {"id": "kv-name-300b",
     "q": "A header KV has a 300-byte name. verify verdict?",
     "truth": "FAIL", "why": "names <= 255 bytes (spec section 7)"},
    {"id": "edge-k-16-vs-buckets-20",
     "q": "edge.k=16 and an edge record carries 20 bucket bytes in the "
          "JSON (more than k). What does the canonical writer do?",
     "truth": "TRUNCATE",
     "why": "buckets are cut to k (canonical form; extra bytes dropped)"},
    {"id": "align-larger-than-file",
     "q": "align=4096 but the whole file is 512 B with one section at "
          "offset 32. verify verdict?",
     "truth": "PASS",
     "why": "offsets need only be aligned, not the file size (padding "
            "rule pads the file, but a hand-made file that is internally "
            "consistent still verifies)"},
]


def ask_oracle(model, case):
    prompt = [
        {"role": "system", "content":
         "You derive tool behavior from a binary-container SPEC alone. "
         "Answer with exactly one line: VERDICT: <PASS|FAIL|REJECT|"
         "TRUNCATE|UNDEFINED> then one short sentence why."},
        {"role": "user", "content": "%s\n\nCase: %s" % (SPEC, case["q"])},
    ]
    think = "deepseek" in model
    content, meta = mm.ollama(model, prompt, timeout=600, think=think)
    line = next((l for l in content.strip().splitlines()
                 if l.upper().startswith("VERDICT")), "")
    verd = line.split(":", 1)[1].strip().upper() if ":" in line else ""
    for tok in ("PASS", "FAIL", "REJECT", "TRUNCATE", "UNDEFINED"):
        if tok in verd:
            return tok, content.strip()[:300], meta
    return "UNPARSEABLE", content.strip()[:300], meta


def main(models=("qwen3:8b", "deepseek-r1:8b")):
    out = open(os.path.join(_HERE, "runs", "oracle_poll.jsonl"), "w")
    tally = {}
    for model in models:
        ok = bad = unp = 0
        for case in CASES:
            try:
                verdict, raw, meta = ask_oracle(model, case)
            except mm.MMError as ex:
                print("%s UNAVAILABLE: %s" % (model, ex))
                out.write(json.dumps({"model": model, "error": str(ex)})
                          + "\n")
                break
            match = verdict.startswith(case["truth"])
            tally[(model, case["id"])] = verdict
            rec = {"model": model, "id": case["id"],
                   "oracle": verdict, "truth": case["truth"],
                   "match": match, "raw_head": raw,
                   "thinking_head": meta.get("thinking", "")[:400]}
            out.write(json.dumps(rec) + "\n")
            ok += bool(match and verdict != "UNPARSEABLE")
            unp += verdict == "UNPARSEABLE"
            bad += (not match and verdict != "UNPARSEABLE")
            print("  %-14s %-24s oracle=%-12s truth=%-8s %s"
                  % (model, case["id"], verdict, case["truth"],
                     "OK" if match else "DISAGREE"))
        print("%s: %d agree, %d disagree, %d unparseable"
              % (model, ok, bad, unp))
    out.close()


if __name__ == "__main__":
    main()
