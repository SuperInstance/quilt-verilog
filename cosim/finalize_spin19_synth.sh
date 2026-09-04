#!/usr/bin/env bash
# finalize_spin19_synth.sh -- wait for the two gate synth arms (yosys
# abc9 on the 48-bit divider is slow), then write cosim/synth-summary.txt,
# append the numbers line to the SPIN-19 report, commit + push.
# Bounded: 60 x 20s = 20 min max.
set -u
cd "$(dirname "$0")/.."
for i in $(seq 1 60); do
  if [ -f cosim/stat_gate_never.txt ] && [ -f cosim/stat_gate_theta.txt ]; then
    break
  fi
  sleep 20
done
if [ ! -f cosim/stat_gate_never.txt ] || [ ! -f cosim/stat_gate_theta.txt ]; then
  echo "TIMEOUT waiting for gate synth arms" > cosim/synth-summary.txt
  exit 1
fi

n_lut=$(grep -o "SB_LUT4 * [0-9]*" cosim/stat_gate_never.txt | grep -o "[0-9]*$")
n_dff=$(grep -o "SB_DFF[A-Z]* * [0-9]*" cosim/stat_gate_never.txt | grep -o "[0-9]*$" | paste -sd+ | bc)
n_car=$(grep -o "SB_CARRY * [0-9]*" cosim/stat_gate_never.txt | grep -o "[0-9]*$")
t_lut=$(grep -o "SB_LUT4 * [0-9]*" cosim/stat_gate_theta.txt | grep -o "[0-9]*$")
t_dff=$(grep -o "SB_DFF[A-Z]* * [0-9]*" cosim/stat_gate_theta.txt | grep -o "[0-9]*$" | paste -sd+ | bc)
t_car=$(grep -o "SB_CARRY * [0-9]*" cosim/stat_gate_theta.txt | grep -o "[0-9]*$")

{
  echo "SPIN-19 SYNTH SUMMARY (yosys 0.47 iCE40, spin19_synth_top wrapper)"
  echo "config: N=7 K=1 PD=3 PW=48 DELTA=12, registered-IO wrapper"
  echo "baseline fabric (make synth, q_fabric_top k4b4a8e1): 5978 LUT4 / 2434 FF / 879 SB_CARRY (committed round-3: 5951/~2340)"
  echo "gate cell GMODE=0 (never):  LUT4=$n_lut  DFF=$n_dff  CARRY=$n_car"
  echo "gate cell GMODE=2 (theta):  LUT4=$t_lut  DFF=$t_dff  CARRY=$t_car"
  echo "gate marginal cost (theta - never): LUT4 $((t_lut - n_lut))  DFF $((t_dff - n_dff))  CARRY $((t_car - n_car))"
  echo "divider-dominated: the 48-bit |e|/pd (const) + m/neff (runtime) path is the"
  echo "bulk of BOTH arms; the theta gate itself is a cross-mult comparator + mux."
} > cosim/synth-summary.txt

printf '\n## Synth numbers (auto-appended)\n\n```\n%s\n```\n' "$(cat cosim/synth-summary.txt)" \
  >> spikes/225-e1-interference-tick/wheel/SPIN-19-rtl-honesty.md

git add cosim/stat_gate_never.txt cosim/stat_gate_theta.txt \
        cosim/synth-summary.txt cosim/synth-gate-never-output.txt \
        cosim/synth-gate-theta-output.txt \
        spikes/225-e1-interference-tick/wheel/SPIN-19-rtl-honesty.md
git commit -q -m "spin19 synth: gate cell LC cost, never vs theta arms (divider-dominated; baseline fabric 5978 LUT4 reproduced)" && \
  git push origin g3-kinduction
echo done
