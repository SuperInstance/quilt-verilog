#!/bin/bash
# run_suite.sh -- full TB suite on iverilog (-g2005). One line per TB.
# Usage: bash tb/run_suite.sh
set -u
export PATH=/home/eileen/tools/oss-cad-suite/bin:$PATH
cd "$(dirname "$0")/.."
mkdir -p tb/run
RTL="rtl/q_tick_sched.v rtl/q_flit_pipe.v rtl/q_link_ringport.v rtl/q_dialfile.v \
     rtl/q_hebb_edge.v rtl/q_echo_gate.v rtl/q_rqh_bank.v rtl/q_cell_core.v \
     rtl/q_cell.v rtl/q_io_port.v rtl/q_fabric_top.v"
fail=0

t() { # tbfile top extra_rtl
  local f=$1 top=$2 extra=${3:-}
  if [ ! -f "$f" ]; then echo "MISSING $f"; fail=1; return; fi
  if iverilog -g2005 -s "$top" -o "tb/run/$top.vvp" $RTL $extra "$f" 2>/tmp/err_$$; then
    if out=$(timeout 300 vvp "tb/run/$top.vvp" 2>&1); then
      if echo "$out" | grep -qE "PASS"; then
        echo "PASS  $top: $(echo "$out" | grep -E 'PASS' | head -1)"
      else
        echo "FAIL  $top (no PASS banner)"; echo "$out" | tail -5; fail=1
      fi
    else
      echo "FAIL  $top (run timeout/crash)"; fail=1
    fi
  else
    echo "FAIL  $top (compile)"; head -5 /tmp/err_$$; fail=1
  fi
}

t tb/tb_tick_sched.v       tb_tick_sched
t tb/tb_flit_pipe.v        tb_flit_pipe
t tb/tb_link_ringport.v    tb_link_ringport
t tb/tb_dialfile.v         tb_dialfile
t tb/tb_hebb_edge.v        tb_hebb_edge
t tb/tb_hyperbola_tail.v   tb_hyperbola_tail
t tb/tb_q_echo_gate.v      tb_q_echo_gate
t tb/tb_q_rqh_bank.v       tb_q_rqh_bank
t tb/tb_rqh_saturation.v  tb_rqh_saturation "rtl/q_hebb_rqh.v"
t tb/tb_cell_core.v        tb_cell_core
t tb/tb_io_port.v          tb_io_port
t tb/tb_fabric_smoke.v     tb_fabric_smoke
t tb/tb_fabric_smoke_v2.v  tb_fabric_smoke_v2
t tb/tb_judge_consistency.v tb_judge_consistency "rtl/q_uf_loader.v"
t tb/tb_hebb_pipe.v        tb_hebb_pipe
# QUF boot TB reads the golden container hex (fuzz-found 2026-09-03: on a
# fresh clone this didn't exist yet -- the loader lane below used to be the
# only producer, and it runs AFTER tb_quf_boot). Build it first.
[ -f tb/run/quf_tb_input.hex ] || {
  python3 tools/quf.py create tb/quf_tb.json tb/run/quf_tb_input.quf
  cp tb/run/quf_tb_input.quf.hex tb/run/quf_tb_input.hex
}
t tb/tb_quf_boot.v         tb_quf_boot "rtl/q_uf_loader.v rtl/quf_boot.v"
t tb/tb_q_tern_dice.v      tb_q_tern_dice "rtl/q_tern_dice.v"
# QUF loader lane (python golden build -> iverilog)
if bash tools/run_quf_tb.sh > /tmp/quf_out 2>&1 && grep -q PASS /tmp/quf_out; then
  echo "PASS  tb_quf_loader: $(grep PASS /tmp/quf_out | head -1)"
else
  echo "FAIL  tb_quf_loader"; tail -5 /tmp/quf_out; fail=1
fi
# pin-fix lane: serialized fabric front-end differential TB (needs the
# same golden container hex the QUF lane just built; regen if missing)
[ -f tb/run/quf_tb_input.hex ] || bash tools/run_quf_tb.sh > /tmp/quf_out2 2>&1 || true
t tb/tb_serfabric.v       tb_serfabric "rtl/q_uf_loader.v rtl/quf_boot.v rtl/q_tick_sched_rt.v rtl/q_boot_gate.v rtl/q_serfabric_top.v"
t tb/tb_wedge_repro.v     tb_wedge_repro    # silicon-lane regression guard: the commissioning wedge (SILICON-EXPERIMENTS F1) must stay dead

# backend battery: format fuzz, boot-boundary fuzz, differential cosim
# (cell + fabric), bug regression (~2.5 min; see tools/backend/run_all.sh)
if bash tools/backend/run_all.sh > /tmp/backend_out 2>&1; then
  echo "PASS  backend_battery: $(grep -E 'PASS:' /tmp/backend_out | tr '\n' ' ')"
else
  echo "FAIL  backend_battery"; grep -E 'FAIL|Error' /tmp/backend_out | head -8; fail=1
fi

exit $fail
