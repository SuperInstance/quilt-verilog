#!/bin/bash
# run_quiesce_repro.sh -- build + run the F3 saturation-deadlock MINIMAL
# REPRO (sim/vlt/tb_quiesce_repro.cpp). Deterministic (seed 0xC0FFEE):
# 120k windowed mixed-traffic cycles wedge the fabric (ledger-intact
# circular wait, cell ST_FIRE + blocked own-delivery at its ringport);
# 100k cycles drain clean. Exit 1 = wedge reproduced (the expected,
# booked result -- SILICON-EXPERIMENTS.md §3 F3 / §3.1); exit 0 = drained
# (would mean F3 got fixed; update the docs).
set -u
cd "$(dirname "$0")/../.."
OSSCAD_DEFAULT=/home/eileen/tools/oss-cad-suite/bin
if [ -d "$OSSCAD_DEFAULT" ]; then export PATH="$OSSCAD_DEFAULT:$PATH"; fi

verilator --cc --build --exe -j 4 \
  --top-module q_fabric_top -GNCELL=15 -GEDGES_N=4 \
  --public-flat-rw -Mdir sim/vlt/obj_qrepro \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
  rtl/q_tick_sched.v rtl/q_flit_pipe.v rtl/q_link_ringport.v \
  rtl/q_dialfile.v rtl/q_hebb_edge.v rtl/q_echo_gate.v \
  rtl/q_rqh_bank.v rtl/q_cell_core.v rtl/q_cell.v rtl/q_io_port.v \
  rtl/q_fabric_top.v sim/vlt/tb_quiesce_repro.cpp || exit 1

QV_REPRO_CYCLES=${QV_REPRO_CYCLES:-120000} ./sim/vlt/obj_qrepro/Vq_fabric_top
