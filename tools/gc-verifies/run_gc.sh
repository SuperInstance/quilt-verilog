#!/usr/bin/env bash
# run_gc.sh -- GC-METAL lane runner: the five GENERAL-CALCULUS.md §8 benches
# plus the three pre-existing verifies benches (regression guard).
# Any FAIL exits nonzero loudly.
set -u
cd "$(dirname "$0")/../.."

BENCHES="tools/verifies/escrow_bench.py tools/verifies/nc_bench.py \
tools/verifies/wavefront_bench.py tools/verifies/type_bench.py \
tools/verifies/product_bench.py \
tools/verifies/c1_seam_bench.py tools/verifies/floor_bench.py \
tools/verifies/c3_fold_bench.py"

rc=0
for b in $BENCHES; do
  echo "============================================================"
  echo "== RUN  $b"
  echo "============================================================"
  if ! python3 "$b"; then
    echo "== FAIL  $b"
    rc=1
  fi
done
echo "============================================================"
if [ "$rc" -eq 0 ]; then
  echo "GC SUITE: ALL PASS (8 benches)"
else
  echo "GC SUITE: FAILURES PRESENT (see above)"
fi
exit "$rc"
