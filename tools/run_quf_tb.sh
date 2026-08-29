#!/usr/bin/env bash
# run_quf_tb.sh -- end-to-end QUF lane: python builds the golden container,
# iverilog compiles loader + dialfile + TB, vvp runs it.
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH=/home/eileen/tools/oss-cad-suite/bin:$PATH

python3 tools/quf.py selftest
python3 tools/quf.py create tb/quf_tb.json tb/run/quf_tb_input.quf
cp tb/run/quf_tb_input.quf.hex tb/run/quf_tb_input.hex

iverilog -g2005 -o tb/run/quf_tb.vvp \
    rtl/q_uf_loader.v rtl/q_dialfile.v tb/quf_tb.v
vvp tb/run/quf_tb.vvp
