#!/bin/bash
# run_all.sh -- the backend battery (backend lane). One command, every
# bench: format fuzz, boot-boundary fuzz (RTL), differential cosim
# (Python model vs q_cell RTL), and the bug regression bench.
# Suite companion: bash tb/run_suite.sh (RTL TBs, untouched by this lane).
set -u
cd "$(dirname "$0")/../.."
fail=0

echo "=== [1/4] QUF format fuzz + properties ==========================="
python3 tools/backend/fuzz_quf.py || fail=1

echo "=== [2/4] quf_boot boundary fuzz (iverilog) ======================"
python3 tools/backend/boot_fuzz.py || fail=1

echo "=== [3/4] differential cosim: Python model vs q_cell (iverilog) =="
python3 tools/backend/cosim_cell.py || fail=1

echo "=== [4/4] bug regression bench ===================================="
python3 tools/backend/regress_backend.py || fail=1

echo
if [ $fail -eq 0 ]; then
  echo "BACKEND BATTERY: ALL PASS"
else
  echo "BACKEND BATTERY: FAILURES PRESENT"
fi
exit $fail
