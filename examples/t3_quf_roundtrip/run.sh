#!/usr/bin/env bash
# run.sh -- T3 QUF round-trip: build/save/reload/mutate/restore/refuse with
# tools/quf.py, diff stdout against the committed .expected.
# Usage: bash examples/t3_quf_roundtrip/run.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
OUT="$HERE/out"
mkdir -p "$OUT"

python3 "$HERE/t3_quf_roundtrip.py" 2>&1 | tee "$OUT/t3.actual.txt"

if diff -u "$HERE/t3_quf_roundtrip.expected" "$OUT/t3.actual.txt"; then
    echo "T3 expected-output match: OK (containers in $OUT/)"
else
    echo "T3 expected-output MISMATCH (see diff above)" >&2
    exit 1
fi
