#!/usr/bin/env bash
# run.sh -- T1 first fabric: compile the real rtl/ fabric, run, diff stdout
# against the committed .expected. Usage: bash examples/t1_first_fabric/run.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
export PATH="${OSSCAD:-/home/eileen/tools/oss-cad-suite/bin}:$PATH"
OUT="$HERE/out"
mkdir -p "$OUT"

RTL="$ROOT/rtl/q_tick_sched.v $ROOT/rtl/q_flit_pipe.v $ROOT/rtl/q_link_ringport.v \
     $ROOT/rtl/q_dialfile.v $ROOT/rtl/q_hebb_edge.v $ROOT/rtl/q_echo_gate.v \
     $ROOT/rtl/q_rqh_bank.v $ROOT/rtl/q_cell_core.v $ROOT/rtl/q_cell.v \
     $ROOT/rtl/q_io_port.v $ROOT/rtl/q_fabric_top.v"

( cd "$HERE" && iverilog -g2005 -s t1_first_fabric -o "$OUT/t1.vvp" $RTL t1_first_fabric.v )
(cd "$OUT" && vvp t1.vvp) | tee "$OUT/t1.actual.txt"

if diff -u "$HERE/t1_first_fabric.expected" "$OUT/t1.actual.txt"; then
    echo "T1 expected-output match: OK"
else
    echo "T1 expected-output MISMATCH (see diff above)" >&2
    exit 1
fi
