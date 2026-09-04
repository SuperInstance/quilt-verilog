#!/usr/bin/env bash
# run_spin34.sh -- SPIN-34 SILICON: minimum-PW sweep on q_wall_gate.
# PW in {48,46,44,42,41,40} x configs {n6_g0,n6_g1,n6_g2,n7_g0,n7_g2}
# then 8 tags x seeds {1,7,42,1999,20260902} per PW into cosim/out34/.
# No pipes; every run writes its own file. Parallel builds + parallel runs.
set -eu
cd "$(dirname "$0")/.."
RTL=rtl/q_wall_gate.v
TB=cosim/vlt/spin19_tb.cpp
V=verilator
mkdir -p cosim/obj34 cosim/out34

PWS="48 46 44 42 41 40"
SEEDS="1 7 42 1999 20260902"

build () { # pw name N GMODE
  local pw=$1 name=$2 N=$3 gm=$4
  if [ ! -x "cosim/obj34/${name}/spin19_tb" ]; then
    $V --cc --exe --build -j 4 \
      --top-module q_wall_gate \
      -GN=$N -GK=1 -GPD=3 -GDELTA=12 -GDRIFT=6 -GPW=${pw} -GTW=14 \
      -GGMODE=$gm -GTHETA100=110 -GTICKS=4800 \
      -Wno-fatal -CFLAGS -O2 \
      -o spin19_tb -Mdir "cosim/obj34/${name}" \
      "$RTL" "$TB" > "cosim/obj34/${name}.buildlog" 2>&1
  fi
}

run () { # name seed lats tag
  local name=$1 seed=$2 lats=$3 tag=$4
  "cosim/obj34/${name}/spin19_tb" "+seed=${seed}" "+lats=${lats}" \
    > "cosim/out34/pw${PW}_${tag}_s${seed}.txt"
}

# build all PW variants in parallel (30 builds, 4 jobs each -> waves)
for pw in $PWS; do
  build $pw pw${pw}_n6_g0 6 0 &
  build $pw pw${pw}_n6_g1 6 1 &
  build $pw pw${pw}_n6_g2 6 2 &
  build $pw pw${pw}_n7_g0 7 0 &
  build $pw pw${pw}_n7_g1 7 1 &
  build $pw pw${pw}_n7_g2 7 2 &
  wait
  echo "pw=${pw} builds done"
done

for pw in $PWS; do
  PW=$pw
  for s in $SEEDS; do
    run pw${pw}_n6_g2 $s 0,0,0,0,0,30       kcoh5_gate   &
    run pw${pw}_n6_g2 $s 0,6,12,18,24,30    ladder_gate  &
    run pw${pw}_n7_g2 $s 0,5,10,15,20,25,30 step5_gate   &
    run pw${pw}_n7_g2 $s 0,0,0,0,0,0,0      zero7_gate   &
    run pw${pw}_n6_g0 $s 0,0,0,0,0,30       kcoh5_off    &
    run pw${pw}_n7_g0 $s 0,5,10,15,20,25,30 step5_off    &
    run pw${pw}_n6_g1 $s 0,0,0,0,0,30       kcoh5_mc1    &
    run pw${pw}_n7_g1 $s 0,5,10,15,20,25,30 step5_mc1    &
    wait
  done
  echo "pw=${pw} runs done"
done

# determinism double-run: re-run two arms DIRECTLY (run() redirects
# internally -- outer redirect captured empty files: scar booked),
# byte-compare against the sweep's own output file.
cosim/obj34/pw48_n7_g2/spin19_tb +seed=1 +lats=0,5,10,15,20,25,30 > cosim/out34/detA.txt
cosim/obj34/pw48_n7_g2/spin19_tb +seed=1 +lats=0,5,10,15,20,25,30 > cosim/out34/detA2.txt
cosim/obj34/pw41_n6_g2/spin19_tb +seed=42 +lats=0,0,0,0,0,30 > cosim/out34/detB.txt
cosim/obj34/pw41_n6_g2/spin19_tb +seed=42 +lats=0,0,0,0,0,30 > cosim/out34/detB2.txt
cmp -s cosim/out34/detA.txt cosim/out34/detA2.txt && [ -s cosim/out34/detA.txt ] && echo "DET-A byte-identical" || echo "DET-A DIFFER"
cmp -s cosim/out34/detB.txt cosim/out34/detB2.txt && [ -s cosim/out34/detB.txt ] && echo "DET-B byte-identical" || echo "DET-B DIFFER"
cmp -s cosim/out34/detA.txt cosim/out34/pw48_step5_gate_s1.txt && echo "DET-A == sweep file" || echo "DET-A != sweep file"

# canary: PW=48 rebuilt RTL must reproduce SPIN-19 trace bytes
cmp -s cosim/out34/pw48_step5_gate_s1.txt cosim/out/step5_gate_s1.txt && echo "CANARY-RTL-48 byte-identical vs SPIN-19" || echo "CANARY-RTL-48 DIFFERS"
cmp -s cosim/out34/pw48_kcoh5_gate_s1.txt cosim/out/kcoh5_gate_s1.txt && echo "CANARY-RTL-48-kcoh5 byte-identical vs SPIN-19" || echo "CANARY-RTL-48-kcoh5 DIFFERS"
echo "spin34 runs complete"
