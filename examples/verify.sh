#!/usr/bin/env bash
# verify.sh -- run every tutorial (T1..T4) in order, pass/fail per tutorial,
# summary line at the end. Exits nonzero if any tutorial fails.
# Usage: bash examples/verify.sh   (or `make verify-all`)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"

names=("T1 first fabric" "T2 hebbian edges" "T3 QUF roundtrip" "T4 cli tools")
scripts=(
  "$HERE/t1_first_fabric/run.sh"
  "$HERE/t2_hebbian_edges/run.sh"
  "$HERE/t3_quf_roundtrip/run.sh"
  "$HERE/t4_cli_tools/run.sh"
)

fail=0
for i in "${!names[@]}"; do
  echo "==> ${names[$i]} ..."
  if bash "${scripts[$i]}" > /tmp/quilt_verify.$$ 2>&1; then
    echo "    PASS"
  else
    echo "    FAIL"
    sed 's/^/    | /' /tmp/quilt_verify.$$ | tail -20
    fail=1
  fi
  rm -f /tmp/quilt_verify.$$
done

echo ""
if [ "$fail" -eq 0 ]; then
  echo "verify-all summary: 4/4 tutorials PASS"
else
  echo "verify-all summary: FAILED (see above)"
fi
exit "$fail"
