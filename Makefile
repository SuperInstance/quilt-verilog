# quilt-verilog — root Makefile (iteration 2, 2026-08-29)
# One command per lane. PATH pinned to the stock oss-cad-suite location;
# override with OSSCAD=... if yours lives elsewhere.
OSSCAD ?= /home/eileen/tools/oss-cad-suite/bin
export PATH := $(OSSCAD):$(PATH)

FORMAL_SBY := formal/cell_core.fair.sby formal/cell_core.tick.sby \
              formal/flit_pipe.fly.sby formal/fabric.conservation.sby \
              formal/echo_gate.dyadic.sby tb/formal/flit_pipe.sby

.PHONY: all test sim formal synth clean

all: test sim formal synth

## test — RTL testbench suite (iverilog). Expect 18/18 PASS.
test:
	bash tb/run_suite.sh

## sim — behavioral Python lane over the same QUF. Expect 34/34 OK.
sim:
	python3 -m unittest discover -s sim/tools -p 'test_*.py'

## formal — all six SymbiYosys proofs (BMC + k-induction).
formal:
	@fail=0; for sby in $(FORMAL_SBY); do \
	  echo "== sby -f $$sby"; \
	  sby -f $$sby || fail=1; \
	done; exit $$fail

## synth — yosys elaboration of the PnR-converged iCE40 top (k4b4a8e1).
## (PnR + icepack commands for a full bitstream: see docs/VERIFICATION.md.)
synth:
	yosys -s synth/fpga-converged.ice40

## clean — remove generated proof dirs and TB run artifacts (keeps sources).
clean:
	rm -rf formal/cell_core.fair formal/cell_core.tick formal/flit_pipe.fly \
	       formal/fabric.conservation formal/echo_gate.dyadic \
	       tb/formal/flit_pipe tb/run /tmp/quf_out*
