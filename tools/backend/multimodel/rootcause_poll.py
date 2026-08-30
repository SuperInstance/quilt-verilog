#!/usr/bin/env python3
"""rootcause_poll.py -- DeepSeek V4-Pro (deepseek-reasoner) as the blind
root-cause reader on the session's real mismatch evidence (multi-model
backend). For each evidence pack it names the guilty side -- Python model,
RTL, harness, or spec ambiguity -- WITHOUT seeing the fix that was
eventually written. Its verdict is then compared with the actual root
cause; agreement/disagreement goes in the MODEL-LEDGER.
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import mm  # noqa: E402

EVIDENCE = [
    {
        "id": "cosim-wsum-stale",
        "title": "differential cosim, directed program: 4 links + effects",
        "evidence": """
Differential bench: a Python model mirrors q_cell_core/q_hebb_edge
arithmetic at v1 semantics; a TB replays ops against the real q_cell RTL
and compares view(0)=act and view(1)=wsum after every op.
Program: bind; link slot0 base 0x2000 peer4; link slot1 base 0x2000
peer5; link slot2 base 0x2000 peer6; link slot3 base 0x2000 peer7;
effect(src=4, dat=0x1000); effect(src=5, dat=0x1000); wsum checkpoints.
Observed:
- after op 'link x4' (before any effect): model wsum = 0x8000, RTL wsum
  = 0x8000. AGREEMENT.
- after effect(src=4): model wsum = 0x8100 (slot0 trained once:
  0x2000+1*0x100). RTL wsum = 0x8400.
- after effect(src=5): model wsum = 0x8200. RTL wsum = 0x8400 (unchanged).
- RTL-internal state dump after effect#2: slot0 bucket0 count = 1,
  slot1 bucket0 count = 1, slots 2,3 count = 0. Bases all 0x2000.
  So the ENGINE STATE matches the model exactly (2 trains total); only
  the wsum READBACK disagrees.
- 0x8400 = 4 x 0x2100. 0x2100 is slot0's post-train readout.
Facts about the RTL plumbing: each edge engine has a registered output
o_w that keeps its last computed readout; the core iterates slots for
view(1), holding a one-hot select, and the core's visible weight is
comb_put = OR over ALL engines' o_w wires.
Question: name the guilty side (Python model / q_cell RTL / TB harness /
spec ambiguity) and the precise mechanism.""",
        "actual": "q_cell.v weight mux was an OR-tree over engine o_w "
                  "registers; unselected engines hold STALE o_w forever "
                  "after their first readout, so the OR pollutes view(1) "
                  "and effect readbacks. Fixed: one-hot select.",
    },
    {
        "id": "cosim-wacc-wrap",
        "title": "differential cosim, random program with max bases",
        "evidence": """
Same differential bench. Random program links 4 edges each with base
0xF000, trains one edge 3 times, then views wsum.
Model: readout per trained slot = 0xF000 + 0x300 = 0xF300;
wsum = 0xF300 + 0xF000 + 0xF000 + 0xF000 = 0x3B300, which exceeds the
16-bit view, so the model saturates: expected view(1) = 0xFFFF.
RTL returned view(1) = 0x0008.
Facts: the core accumulates the per-edge readouts in a register declared
`reg [PW:0] wacc` (PW=16, so 17 bits). After the sweep it reports
`wacc[PW] ? 0xFFFF : wacc[PW-1:0]`.
Question: name the guilty side and the precise mechanism.""",
        "actual": "q_cell_core.v wacc was PW+1 = 17 bits; four readouts "
                  "of up to 0xFFFF sum to 0x3FFFC which wraps past 17 "
                  "bits; only bit 16 was tested for saturation so "
                  "0x20008-class sums read as ~0x0008. Fixed: PW+EIW+1 "
                  "bits, saturation over the whole upper range.",
    },
    {
        "id": "boot-single-section",
        "title": "QUF boot loader: single-section container",
        "evidence": """
A streaming QUF loader FSM (silicon boot path) parses: header, KV pairs,
section table (name, kind, offset u64, size u64), then consumes payload
bytes in file-offset order. Internal regs: have[4] one bit per KNOWN
section (dials/edges/routing/ticks); dispatch logic at the moment the
LAST table entry completes:
  task goto_data: if (!qany) -> DONE; else if (posn == qmin) enter that
  payload; else if (posn > qmin) -> LAYOUT error; else stay in a
  padding-wait state.
qany/qmin are combinational wires over have[] and the section offsets.
The have[] bit for an entry is scheduled (nonblocking <= 1) in the SAME
clock edge where the last entry's goto_data task executes.
Observed in simulation with a QUF containing exactly ONE section
(dials, 3 rows, clean per the reference tool):
- the loader reaches DONE and the top-level boot FSM RELEASES the
  fabric (boot_ok);
- the dialfile contains NONE of the 3 rows (pure power-on defaults);
- with a 4-section file (the golden test) all sections load fine and
  the dial rows verify bit-exact.
Question: name the guilty side and the precise mechanism.""",
        "actual": "q_uf_loader.v NBA race: goto_data's wires saw the "
                  "pre-commit have[] (the just-registered entry "
                  "invisible), so a single-section file took !qany -> "
                  "DONE without entering its only payload; >=2-section "
                  "files masked it (earlier have bits committed). Fixed: "
                  "registration-aware dispatch.",
    },
]


def main():
    out = open(os.path.join(_HERE, "runs", "pro_rootcause.jsonl"), "w")
    agree = 0
    for ev in EVIDENCE:
        prompt = [
            {"role": "system", "content":
             "You are a rigorous root-cause analyst for hardware/"
             "software co-verification. You call the guilty side by name "
             "and give the precise mechanism. You do not hedge."},
            {"role": "user", "content": ev["evidence"]},
        ]
        try:
            verdict, meta = mm.pro(prompt, timeout=420)
        except mm.MMError as ex:
            print("%s: V4-Pro UNAVAILABLE (%s)" % (ev["id"], ex))
            out.write(json.dumps({"id": ev["id"], "error": str(ex)}) + "\n")
            continue
        rec = {"id": ev["id"], "verdict": verdict,
               "reasoning_head": meta.get("reasoning", "")[:1200],
               "actual_root_cause": ev["actual"],
               "model": meta.get("model")}
        out.write(json.dumps(rec) + "\n")
        v = verdict.lower()
        hit = None
        for key, tag in (("or-tree", "or"), ("or over", "or"),
                         ("stale", "stale"), ("wrap", "wrap"),
                         ("overflow", "wrap"), ("17", "wrap"),
                         ("nonblocking", "race"), ("nba", "race"),
                         ("same cycle", "race"), ("race", "race"),
                         ("one nba behind", "race")):
            if key in v:
                hit = hit or tag
        print("%-22s pro-verdict-head: %s" %
              (ev["id"], verdict.strip().splitlines()[0][:100]
               if verdict.strip() else "(empty)"))
        print("%-22s mechanism-match: %s" % (ev["id"], hit))
    out.close()


if __name__ == "__main__":
    main()
