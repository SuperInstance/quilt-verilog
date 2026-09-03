#!/usr/bin/env bash
# run_spin19.sh -- SPIN-19 cosim: build q_wall_gate per config (verilator,
# parallel builds) then run seeds {1,7,42} per grammar/mode in parallel
# processes (24-core box: parallelism via per-seed jobs). No pipes; every
# run writes its own file under cosim/out/.
set -eu
cd "$(dirname "$0")/.."
RTL=rtl/q_wall_gate.v
TB=cosim/vlt/spin19_tb.cpp
V=verilator
mkdir -p cosim/obj cosim/out

build () { # name N GMODE
  local name=$1 N=$2 gm=$3
  if [ ! -x "cosim/obj/${name}/spin19_tb" ]; then
    $V --cc --exe --build -j 8 \
      --top-module q_wall_gate \
      -GN=$N -GK=1 -GPD=3 -GDELTA=12 -GDRIFT=6 -GPW=48 -GTW=14 \
      -GGMODE=$gm -GTHETA100=110 -GTICKS=4800 \
      -Wno-fatal -CFLAGS -O2 \
      -o spin19_tb -Mdir "cosim/obj/${name}" \
      "$RTL" "$TB" > "cosim/obj/${name}.buildlog" 2>&1
  fi
}

run () { # name seed lats tag
  local name=$1 seed=$2 lats=$3 tag=$4
  "cosim/obj/${name}/spin19_tb" "+seed=${seed}" "+lats=${lats}" \
    > "cosim/out/${tag}_s${seed}.txt"
}

# builds: N6/N7 x gate modes {never=0, always=1, theta110=2}
build n6_g0 6 0
build n6_g1 6 1
build n6_g2 6 2
build n7_g0 7 0
build n7_g1 7 1
build n7_g2 7 2
echo "builds done"

# grammars (SPIN-16 panel, pd=3 K=1 delta=12):
#   kcoh5  [0,0,0,0,0,30]      (N=6, byte-frozen under gate -- R1(b))
#   ladder [0,6,12,18,24,30]   (N=6)
#   step5  [0,5,10,15,20,25,30](N=7, rescue cell -- R1(a))
#   zero7  [0,0,0,0,0,0,0]     (N=7, diverged probe)
for s in 1 7 42; do
  run n6_g2 $s 0,0,0,0,0,30       kcoh5_gate   &
  run n6_g2 $s 0,6,12,18,24,30    ladder_gate  &
  run n7_g2 $s 0,5,10,15,20,25,30 step5_gate   &
  run n7_g2 $s 0,0,0,0,0,0,0      zero7_gate   &
  run n6_g0 $s 0,0,0,0,0,30       kcoh5_off    &
  run n7_g0 $s 0,5,10,15,20,25,30 step5_off    &
  run n6_g1 $s 0,0,0,0,0,30       kcoh5_mc1    &
  run n7_g1 $s 0,5,10,15,20,25,30 step5_mc1    &
done
wait
echo "runs done"
ls cosim/out/
