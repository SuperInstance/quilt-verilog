# COSIM-LANE BRIEF — Scale-Up (§10 gap)

You are the COSIM SCALE-UP lane for quilt-verilog. Repo: /home/eileen/projects/quilt-verilog. Start from branch `cosim-scaleup` if it exists (it may hold partial work — review `git log cosim-scaleup` first and build on it), else cut from master. Branch: `cosim-scaleup`. DeepSeek/DeepInfra REVOKED — do not call.

NOTE: a prior lane attempt committed `5d9d848` ("cosim scale-up: NCELL parameterized 2->4/8, ring-scale directed seams, decidable-only classification, private run dirs") — locate it (`git log --all --oneline | grep 5d9d848`) and CONTINUE its work rather than redoing it.

MISSION: close the §10 scale gap. Baseline: fabric-level Python-vs-RTL cosim (tb/tb_cosim_fabric.v + cosim_fabric.py) bit-exact at NCELL=2 (30/30 programs, 0 findings on fresh seed).

1. Scale to NCELL=4 minimum, try 8 — watch ring timing, dial-13 view semantics (live q_echo_gate trace, deadband-snap), ACK-to-cell-src consumption (documented in commit 3157b3d's message).
2. Directed cases at the seams: mid-ring fire-to-host, chained fire >2 cells, probe decay under congestion + 3x random volume, multiple fresh seeds.
3. Every disagreement is a finding — classify model-side vs RTL-side honestly (first run's findings were ALL model-side; never "fix" RTL to match the model).
4. SHARPENING RULE (from the R4 differential conception): classify programs decidable vs budget-adjacent BEFORE running; report counts with the split explicit; unclassifiable disagreement classes are named findings, not failures.
5. Full battery (bash tb/run_suite.sh + tools/backend/run_all.sh) must stay ALL PASS. Incremental commits on your branch, no merge/push.
6. Update §10 gap status in THE-BREAKDOWN/BACKEND-NOTES only if measured counts justify it.

REPORT: NCELL reached, program counts with decidable/budget-adjacent split, seeds, findings + classification, sim time, remaining gap honestly stated.
