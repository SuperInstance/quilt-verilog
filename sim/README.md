# sim/ — behavioral prototypes over the same QUF the RTL loads

The RTL stays the truth; `sim/` proves semantics in Python first, on the
same file format (`tools/quf.py`) and the same opcode arithmetic.

| lane | tool | docs |
|---|---|---|
| tap-fabric | `tools/tapfabric.py` + `fixtures/` | `docs/TAP-FABRIC.md` — the Tap's bar run as a quilt cell graph: MudArena session logs replayed through q_cell_core/q_hebb_edge-exact semantics, emitting a tap-room QUF + rendered transcript |

Run the tap-fabric bridge:

```
python3 sim/tools/tapfabric.py sim/fixtures/tap-session-01.jsonl --out /tmp/tap_room
python3 tools/quf.py verify /tmp/tap_room.quf
python3 -m unittest discover -s sim/tools -p 'test_*.py'
```
