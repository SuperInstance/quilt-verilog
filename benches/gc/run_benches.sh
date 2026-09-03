#!/usr/bin/env bash
# run_benches.sh -- GC CONJECTURE FALSIFIER lane runner: the four
# GC-C1..C4 benches from GENERAL-CALCULUS.md §7 (benches/gc/).
# Distinct from tools/gc-verifies (the §8 CLOSED-BOUNDED benches for the
# proved statements): this lane hunts the REGISTERED FALSIFIERS of the
# four open conjectures. Exit codes: 0 all PASS; 1 harness FAIL or bench
# error; a KILLED verdict (exit 2 per bench) is reported loudly and
# fails the lane -- a kill is a publishable event, not a routine pass.
set -u
cd "$(dirname "$0")/../.."

BENCHES="benches/gc/gc_c1_six_verb_bench.py \
benches/gc/gc_c2_synchrony_bench.py \
benches/gc/gc_c3_span_bench.py \
benches/gc/gc_c4_snapnorm_bench.py"

rc=0
for b in $BENCHES; do
  echo "============================================================"
  echo "== RUN  $b"
  echo "============================================================"
  python3 "$b"
  code=$?
  if [ "$code" -ne 0 ]; then
    echo "== FAIL/KILLED  $b (exit $code -- see the bench banner above)"
    rc=1
  fi
done
echo "============================================================"
if [ "$rc" -eq 0 ]; then
  echo "GC FALSIFIER SUITE: ALL PASS (4 benches, 0 kills)"
else
  echo "GC FALSIFIER SUITE: FAILURE OR KILL PRESENT (see above)"
fi
exit "$rc"
