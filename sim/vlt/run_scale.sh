#!/bin/bash
# run_scale.sh -- build + run the SILICON EXPERIMENT LANE scale sim
# (sim/vlt/tb_scale_vlt.cpp). iverilog is the functional lane (18/18 TBs)
# but ~1000x too slow for 1M+ cycles on a 15-cell fabric; verilator is
# the scale lane. Exact commands (quoting for the docs):
#
#   verilator --cc --build --exe -j 4 \
#     --top-module q_fabric_top -GNCELL=15 -GEDGES_N=4 \
#     --public-flat-rw -Mdir sim/vlt/obj_scale \
#     -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
#     rtl/q_tick_sched.v rtl/q_flit_pipe.v rtl/q_link_ringport.v \
#     rtl/q_dialfile.v rtl/q_hebb_edge.v rtl/q_echo_gate.v \
#     rtl/q_rqh_bank.v rtl/q_cell_core.v rtl/q_cell.v rtl/q_io_port.v \
#     rtl/q_fabric_top.v sim/vlt/tb_scale_vlt.cpp
#   ./sim/vlt/obj_scale/Vq_fabric_top
#
# K=8 B=8 AGEW=24 ride q_cell's defaults (the top does not override them);
# NCELL=15 is the largest legal ring (AIDW=4, ids 0..14; 0xF is the io
# node), EDGES_N=4 the largest legal edge count at EIW=2.
set -u
cd "$(dirname "$0")/../.."
OSSCAD_DEFAULT=/home/eileen/tools/oss-cad-suite/bin
if [ -d "$OSSCAD_DEFAULT" ]; then export PATH="$OSSCAD_DEFAULT:$PATH"; fi

verilator --cc --build --exe -j 4 \
  --top-module q_fabric_top -GNCELL=15 -GEDGES_N=4 \
  --public-flat-rw -Mdir sim/vlt/obj_scale \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
  rtl/q_tick_sched.v rtl/q_flit_pipe.v rtl/q_link_ringport.v \
  rtl/q_dialfile.v rtl/q_hebb_edge.v rtl/q_echo_gate.v \
  rtl/q_rqh_bank.v rtl/q_cell_core.v rtl/q_cell.v rtl/q_io_port.v \
  rtl/q_fabric_top.v sim/vlt/tb_scale_vlt.cpp || exit 1

./sim/vlt/obj_scale/Vq_fabric_top
