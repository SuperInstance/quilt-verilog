#!/usr/bin/env bash
# run.sh -- T2 hebbian edges: compile, run (VCD to out/), diff stdout
# against the committed .expected. Usage: bash examples/t2_hebbian_edges/run.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
export PATH="${OSSCAD:-/home/eileen/tools/oss-cad-suite/bin}:$PATH"
if ! command -v iverilog >/dev/null 2>&1 || ! command -v vvp >/dev/null 2>&1; then
    echo "ERROR: 'iverilog'/'vvp' not found after PATH assembly." >&2
    echo "       Install oss-cad-suite or point OSSCAD at its bin/, e.g.:" >&2
    echo "       OSSCAD=/path/to/oss-cad-suite/bin bash examples/t2_hebbian_edges/run.sh" >&2
    exit 2
fi
OUT="$HERE/out"
mkdir -p "$OUT"

RTL="$ROOT/rtl/q_tick_sched.v $ROOT/rtl/q_flit_pipe.v $ROOT/rtl/q_link_ringport.v \
     $ROOT/rtl/q_dialfile.v $ROOT/rtl/q_hebb_edge.v $ROOT/rtl/q_echo_gate.v \
     $ROOT/rtl/q_rqh_bank.v $ROOT/rtl/q_cell_core.v $ROOT/rtl/q_cell.v \
     $ROOT/rtl/q_io_port.v $ROOT/rtl/q_fabric_top.v"

( cd "$HERE" && iverilog -g2005 -s t2_hebbian_edges -o "$OUT/t2.vvp" $RTL t2_hebbian_edges.v )
(cd "$OUT" && vvp t2.vvp) | tee "$OUT/t2.actual.txt"

if diff -u "$HERE/t2_hebbian_edges.expected" "$OUT/t2.actual.txt"; then
    echo "T2 expected-output match: OK (waveform: $OUT/t2_hebbian_edges.vcd)"
else
    echo "T2 expected-output MISMATCH (see diff above)" >&2
    exit 1
fi
