#!/usr/bin/env bash
# run.sh -- T4 CLI tools tour: the tools/quf.py command set against a real
# container (create -> info -> verify -> dump -> hex), the no-simulator
# door from docs/USER-GUIDE.md sections 2.3/3. Stdout (not the side
# files) is diffed against the committed .expected.
# Usage: bash examples/t4_cli_tools/run.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
OUT="$HERE/out"
mkdir -p "$OUT"
cd "$ROOT"     # relative paths in every printed line -> stable output

SRC=examples/t3_quf_roundtrip/room.json
DST=examples/t4_cli_tools/out/room

{
echo "\$ python3 tools/quf.py create $SRC $DST.quf"
python3 tools/quf.py create "$SRC" "$DST.quf"
echo "\$ python3 tools/quf.py verify $DST.quf"
python3 tools/quf.py verify "$DST.quf"
echo "\$ python3 tools/quf.py info $DST.quf"
python3 tools/quf.py info "$DST.quf"
echo "\$ python3 tools/quf.py dump $DST.quf"
python3 tools/quf.py dump "$DST.quf"
echo "\$ python3 tools/quf.py hex $DST.quf $DST.hex"
python3 tools/quf.py hex "$DST.quf" "$DST.hex"
echo "hex image header: $(head -1 "$DST.hex") (bytes); dials payload starts at hex line $((0x180+1))"
} | tee "$OUT/t4.actual.txt"

if diff -u "$HERE/t4_cli_tools.expected" "$OUT/t4.actual.txt"; then
    echo "T4 expected-output match: OK (container + hex image in $OUT/)"
else
    echo "T4 expected-output MISMATCH (see diff above)" >&2
    exit 1
fi
