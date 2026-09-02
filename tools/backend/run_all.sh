#!/bin/bash
# run_all.sh -- the backend battery (backend lane). One command, every
# bench: format fuzz, boot-boundary fuzz (RTL), differential cosim
# (Python model vs q_cell RTL), FABRIC-level differential cosim (Python
# model vs q_fabric_top -- THE-BREAKDOWN §10), and the bug regression bench.
# Suite companion: bash tb/run_suite.sh (RTL TBs, untouched by this lane).
set -u
cd "$(dirname "$0")/../.."
fail=0

echo "=== [1/5] QUF format fuzz + properties ==========================="
python3 tools/backend/fuzz_quf.py || fail=1

echo "=== [2/5] quf_boot boundary fuzz (iverilog) ======================"
python3 tools/backend/boot_fuzz.py || fail=1

echo "=== [3/5] differential cosim: Python model vs q_cell (iverilog) =="
python3 tools/backend/cosim_cell.py || fail=1

echo "=== [4/5] fabric-level cosim: Python vs q_fabric_top NCELL=4 (iverilog) ="
python3 tools/backend/cosim_fabric.py 0xFAB41C 12 4 || fail=1

echo "=== [5/5] bug regression bench ==================================="
python3 tools/backend/regress_backend.py || fail=1

echo
if [ $fail -eq 0 ]; then
  echo "BACKEND BATTERY: ALL PASS"
else
  echo "BACKEND BATTERY: FAILURES PRESENT"
fi
exit $fail
