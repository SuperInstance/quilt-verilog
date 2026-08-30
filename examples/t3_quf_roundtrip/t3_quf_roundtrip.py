#!/usr/bin/env python3
"""t3_quf_roundtrip.py -- TUTORIAL 3: QUF round-trip, state is a file.

The doctrine's proof by construction (docs/DOCTRINE.md item 3, QUF-SPEC):
save the fabric's state to a QUF container, mutate the live state, reload
from the file, and verify identity -- the canonical-form property pins it:

  * the writer is canonical (fixed KV order, fixed section order, aligned
    payloads), so the SAME state always rebuilds to the SAME bytes --
    asserted byte-exact by quf.py selftest's golden vector (sha256 pinned
    in docs/QUF-SPEC.md SS11) and the warm-start tests under `make sim`
    (docs/VERIFICATION.md, lane 2).

The state here is Tutorial 2's ending frozen into a file: cell 0's edge
still carries the 10 ladder cofires (buckets [10,0,...]), dials are the
POR defaults with cell 1 a little more earnest (THRESH 0x3800).

Stdlib only. Run: bash examples/t3_quf_roundtrip/run.sh
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TOOLS = os.path.join(ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import quf  # noqa: E402  (tools/quf.py -- the QUF reference implementation)

OUT = os.path.join(HERE, "out")


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16] + "..."


def state_print(dec, tag):
    print("%-7s cells=%d  THRESH: cell0=0x%04X cell1=0x%04X  "
          "edge buckets=%s" %
          (tag, len(dec["dials"]),
           dec["dials"][0][5], dec["dials"][1][5],
           dec["edges"][0]["buckets"]))


def main():
    os.makedirs(OUT, exist_ok=True)
    doc = json.load(open(os.path.join(HERE, "room.json")))
    doc = quf.add_digest(doc)          # pin section content (quf.sha256)

    # ---- 1. SAVE: state -> file --------------------------------------
    data = quf.build(doc)
    path = os.path.join(OUT, "room.quf")
    with open(path, "wb") as f:
        f.write(data)
    issues = quf.verify_bytes(data, path)
    assert not issues, issues
    rel = os.path.relpath(path, ROOT)     # stable across checkouts
    print("save   %s (%d bytes)  verify clean  sha256 %s"
          % (rel, len(data), sha(data)))

    # ---- 2. RELOAD: file -> state (the warm boot) --------------------
    buf = open(path, "rb").read()
    parsed = quf.read(buf)
    dec = quf.decode_sections(parsed)
    state_print(dec, "reload")

    # ---- 3. IDENTITY: same state -> same bytes (canonical form) ------
    again = quf.rebuild(parsed)
    if again == buf:
        print("id     rebuild(parsed) == file bytes  -> canonical form holds")
    else:
        print("id     MISMATCH: rebuild differs from file")
        return 1

    # ---- 4. MUTATE the live state, save to a second file -------------
    doc2 = json.loads(json.dumps(doc))
    doc2["dials"][0][5] = 0x3800               # cell 0 eases off
    doc2["edges"][0]["buckets"][0] = 11        # one more cofire heard
    data2 = quf.build(quf.add_digest(doc2))
    path2 = os.path.join(OUT, "room_evolved.quf")
    open(path2, "wb").write(data2)
    dec2 = quf.decode_sections(quf.read(data2))
    state_print(dec2, "mutate")
    print("       sha256 %s  (differs: state changed, file changed)"
          % sha(data2))

    # ---- 5. RESTORE from the FIRST file: identity re-verified --------
    decr = quf.decode_sections(quf.read(open(path, "rb").read()))
    state_print(decr, "restore")
    if quf.rebuild(quf.read(buf)) == buf and \
            decr["dials"][0][5] == 0x6000 and \
            decr["edges"][0]["buckets"][0] == 10:
        print("id     room.quf still boots the ORIGINAL state "
              "(THRESH 0x6000, 10 cofires) -- the file is the state")
    else:
        print("id     FAIL: restore did not reproduce the saved state")
        return 1

    # ---- 6. REFUSAL: corruption is loud, never a half-load -----------
    refusals = []
    bad = bytearray(buf)
    soff = parsed["table"][0][2]            # dials section offset
    bad[soff + 10] ^= 0x01                  # flip one DIAL byte in place
    issues = quf.verify_bytes(bytes(bad), "corrupt.quf")
    refusals.append(issues[0] if issues else None)
    print("refuse dial byte flip: %s" % refusals[-1])
    bad2 = bytearray(buf)
    bad2[4] = 0x02                           # version word != 1
    issues = quf.verify_bytes(bytes(bad2), "corrupt2.quf")
    refusals.append(issues[0] if issues else None)
    print("refuse bad version  : %s" % refusals[-1])
    trunc = buf[:len(buf) // 2]
    issues = quf.verify_bytes(trunc, "trunc.quf")
    refusals.append(issues[0] if issues else None)
    print("refuse truncated    : %s" % refusals[-1])
    if any(r is None for r in refusals):
        print("T3 FAIL: a corrupt container was accepted")
        return 1

    print("T3 PASS: save -> reload -> identity -> mutate -> restore -> refuse")
    return 0


if __name__ == "__main__":
    sys.exit(main())
