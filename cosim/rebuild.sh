#!/bin/bash
set -e
cd "$(dirname "$0")/.."
RTL=rtl/q_wall_gate.v
TB=cosim/vlt/spin19_tb.cpp
V=verilator

for name in n6_g0 n6_g1 n6_g2 n7_g0 n7_g1 n7_g2; do
  N=$(echo $name | cut -c2)
  gm=$(echo $name | cut -c5)
  echo "Building $name (N=$N, GMODE=$gm)..."
  mkdir -p cosim/obj cosim/out
  $V --cc --exe --build -j 8 \
    --top-module q_wall_gate \
    -GN=$N -GK=1 -GPD=3 -GDELTA=12 -GDRIFT=6 -GPW=48 -GTW=14 \
    -GGMODE=$gm -GTHETA100=110 -GTICKS=4800 \
    -Wno-fatal -CFLAGS -O2 \
    -o spin19_tb -Mdir "cosim/obj/${name}" \
    "$RTL" "$TB" > "cosim/obj/${name}.buildlog" 2>&1 &
done
wait
echo "All builds complete"
ls cosim/obj/*/spin19_tb
