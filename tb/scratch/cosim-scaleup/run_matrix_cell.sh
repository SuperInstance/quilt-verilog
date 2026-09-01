#!/bin/bash
# COSIM SCALE-UP lane, phase 2: scale matrix. One cell per invocation,
# caller commits after each. Usage: run_matrix_cell.sh <name> <seed> <nrand> <ncell>
set -u
NAME=$1; SEED=$2; NRAND=$3; NCELL=$4
cd /home/eileen/projects/quilt-verilog
LOG=tb/run/cosim_scaleup_lane/${NAME}.log
echo "=== cell ${NAME}: NCELL=${NCELL} seed=${SEED} nrand=${NRAND} start $(date -u +%FT%TZ)" | tee -a "$LOG"
python3 -u tools/backend/cosim_fabric.py "$SEED" "$NRAND" "$NCELL" 2>&1 | tee -a "$LOG"
rc=${PIPESTATUS[0]}
echo "=== cell ${NAME} exit=${rc} end $(date -u +%FT%TZ)" | tee -a "$LOG"
exit $rc
