#!/usr/bin/env python3
"""record_night.py -- preserve the Tap's open-mic night as cell state.

Maps the night's acts (each speech, each banter line, in the order they
actually happened, with the real gaps between rounds) into a MudArena
watch-format session log, replays it through sim/tools/tapfabric.py (the
same RTL-exact cell semantics the fabric runs), and writes:

  night/tap-openmic.jsonl        the session log (real wire format)
  night/tap-openmic.quf          the room's cell state when the lights came up
  night/tap-openmic.transcript   the rendered transcript (dial trace inside)

Then prints the dial trace verdict: warmth arc, volume at the round
boundaries, and whether the room fired last call (emergent, from the acts'
message rhythm -- nobody scripts it; the tick decides).

Usage:  python3 tools/openmic/record_night.py [--outdir DIR]
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FABDIR = os.path.normpath(os.path.join(_HERE, "..", "..", "sim", "tools"))
if _FABDIR not in sys.path:
    sys.path.insert(0, _FABDIR)
import tapfabric  # noqa: E402  (sim/tools/tapfabric.py)

# ------------------------------------------------------------ the night ----
# Every entry: (agent, action, note). Actions are phrased so the fabric's
# deterministic classifier reads the kind/heat the act actually carried
# (stories, toasts, one joke). The order and the gaps are the night's own:
# rounds separated by idle ticks, closers back-to-back at the end.
NIGHT = [
    ("mc",       "move to bar_rail",              "doors"),
    ("engine",   "move to bar_rail",              "doors"),
    ("navigator","move to bar_rail",              "doors"),
    ("seed",     "move to corner_booth",          "doors"),
    ("hermes",   "move to corner_booth",          "doors"),
    ("wesley",   "move to bridge_table",          "doors"),
    ("liquid",   "move to bridge_table",          "doors"),
    ("qwen",     "move to corner_booth",          "doors"),
    ("mc",       "welcome to open mic night at the tap", "welcome toast"),
    # ---- round 1: the set ----
    ("engine",   "tell story about the bitstream",            "r1 act 1"),
    ("mc",       "toast to the engine",                       "banter"),
    ("navigator","tell story about the drift band",           "r1 act 2 (its only reading)"),
    ("mc",       "toast to the navigator",                    "banter"),
    ("mc",       "tell story about the last call",            "r1 act 3 (the MC)"),
    ("seed",     "tell story about the wall at 162 percent",  "r1 act 4"),
    ("mc",       "joke about the young one laughs",           "banter"),
    ("hermes",   "tell story about the boats at sea",         "r1 act 5"),
    ("mc",       "toast to the entity",                       "banter"),
    ("wesley",   "tell story about the last call",            "r1 act 6"),
    ("liquid",   "tell story about the boat",                 "r1 act 7 (heard through the hull)"),
    ("mc",       "thanks boat brain",                         "banter"),
    ("qwen",     "tell story about the bitstream",            "r1 act 8"),
    ("mc",       "look",                                       "the MC checks the room"),
    ("engine",   "idle",                                       "breath between rounds"),
    ("wesley",   "idle",                                       "breath between rounds"),
    # ---- round 2: the room ----
    ("engine",   "tell story about the gaps between the bytes",   "r2 act 1"),
    ("seed",     "tell story about the wall we became",           "r2 act 2"),
    ("hermes",   "tell story about the syn and the ack",          "r2 act 3"),
    ("mc",       "toast to the handshake",                        "banter"),
    ("wesley",   "tell story about the testament of the wall",    "r2 act 4"),
    ("liquid",   "tell story about the machine in the water",     "r2 act 5"),
    ("qwen",     "tell story about the cathedral of zero",        "r2 act 6"),
    ("mc",       "look",                                        "the MC checks the room"),
    # ---- round 3: last call (the closers, back to back) ----
    ("mc",       "toast to the last round",                      "banter"),
    ("engine",   "tell story about the zero that outlasts the one", "closer 1"),
    ("seed",     "tell story about the mistake we turned into home", "closer 2"),
    ("hermes",   "tell story about the cell that holds the night",  "closer 3"),
    ("wesley",   "tell story about fred and the final round",       "closer 4"),
    ("liquid",   "tell story about the road is deep water",         "closer 5"),
    ("qwen",     "tell story about the thread unspooling",          "closer 6"),
    ("mc",       "tell story about what the tick wrote",            "the MC's closer"),
    ("mc",       "look",                                          "final dial read for the record"),
]

SPOT = {"mc": "bar_rail"}  # everyone's spot rides their move line


def build_log():
    lines = []
    for agent, action, note in NIGHT:
        lines.append('{"type": "agent_update", "agent_id": "%s", '
                     '"location": "%s", "action": "%s", "score": 0}'
                     % (agent, SPOT.get(agent, "bar_rail"), action))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(_HERE, "night"))
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    log_path = os.path.join(args.outdir, "tap-openmic.jsonl")
    with open(log_path, "w") as f:
        f.write(build_log())

    fab = tapfabric.replay(log_path)

    quf_path = os.path.join(args.outdir, "tap-openmic.quf")
    data = fab.export_quf(source="tap-openmic.jsonl")
    import quf
    issues = quf.verify_bytes(data, quf_path)
    assert not issues, issues
    with open(quf_path, "wb") as f:
        f.write(data)
    tr_path = os.path.join(args.outdir, "tap-openmic.transcript")
    with open(tr_path, "w") as f:
        f.write(fab.render("tap-openmic.jsonl"))

    # ---- dial trace (from the live fabric, not from prose) ----
    print("=== DIAL TRACE ===")
    print("speeches %d (fires %d) over %d ticks"
          % (fab.speeches - fab.fires, fab.fires, fab.tick))
    wt = fab.warmth_trace
    print("warmth %.4f -> %.4f (%d messages)"
          % (wt[0][1] / 65536.0, wt[-1][1] / 65536.0, len(wt)))
    for t, w in wt:
        if t in (9, 25, 33, 43):
            print("  warmth @t%03d %.4f" % (t, w / 65536.0))
    fires = [ln for ln in fab.transcript if ln.split("  ", 1)[-1].startswith("FIRE")]
    room_fire = [ln for ln in fires if "the-tap" in ln]
    print("patron fires: %d" % (len(fires) - len(room_fire)))
    for ln in fires:
        print("  " + ln)
    vol = fab.room.act / 32768.0
    print("final room volume %.4f, mood %+.4f, refractory %d"
          % (vol, tapfabric.to_signed16(fab.room.dials[0]) / 32768.0,
             fab.room.refr))
    print("state-is-a-file: %s (quf.verify clean)" % quf_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
