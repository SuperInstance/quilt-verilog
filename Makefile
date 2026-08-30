# quilt-verilog — root Makefile (iteration 2, 2026-08-29)
# One command per lane. PATH pinned to the stock oss-cad-suite location;
# override with OSSCAD=... if yours lives elsewhere.
OSSCAD ?= /home/eileen/tools/oss-cad-suite/bin
export PATH := $(OSSCAD):$(PATH)

# Tool guard: fail with a hint, not a raw "command not found".
# Usage inside a recipe: @$(call GUARD,iverilog)
define GUARD
command -v $(1) >/dev/null 2>&1 || { \
  echo "ERROR: '$(1)' not found on PATH."; \
  echo "quilt-verilog builds with stock oss-cad-suite. Point the Makefile at yours:"; \
  echo "    make OSSCAD=/path/to/oss-cad-suite/bin <target>"; \
  echo "(currently pinned to: $(OSSCAD)). See README, 'Quickstart' -> Toolchain."; \
  exit 127; }
endef

FORMAL_SBY := formal/cell_core.fair.sby formal/cell_core.tick.sby \
              formal/flit_pipe.fly.sby formal/fabric.conservation.sby \
              formal/echo_gate.dyadic.sby tb/formal/flit_pipe.sby

.PHONY: all test sim formal synth pnr clean

all: test sim formal synth pnr

## test — RTL testbench suite (iverilog). Expect 18/18 PASS.
test:
	@$(call GUARD,iverilog)
	bash tb/run_suite.sh

## sim — behavioral Python lane over the same QUF. Expect 34/34 OK.
sim:
	python3 -m unittest discover -s sim/tools -p 'test_*.py'

## formal — all six SymbiYosys proofs (BMC + k-induction).
formal:
	@$(call GUARD,sby)
	@$(call GUARD,yosys)
	@$(call GUARD,boolector)
	@fail=0; for sby in $(FORMAL_SBY); do \
	  echo "== sby -f $$sby"; \
	  sby -f $$sby || fail=1; \
	done; exit $$fail

## synth — yosys iCE40 elaboration of the PnR-converged top (k4b4a8e1).
## Elaboration ONLY (~20 s); the measured PnR/bitstream numbers come next:
synth:
	@$(call GUARD,yosys)
	yosys -s synth/fpga-converged.ice40

## pnr — full place & route + bitstream of the converged top. Depends on
## synth (regenerates synth/fabric2_k4b4a8e1_ice40.json). Reproduces the
## measured HX8K-CT256 numbers: ~7,528/7,680 LC (98%), fmax ~40 MHz,
## 135,100-byte fabric2_k4b4a8e1.bin. ~3 min on a laptop.
pnr: synth
	@$(call GUARD,nextpnr-ice40)
	@$(call GUARD,icepack)
	nextpnr-ice40 --hx8k --package ct256 \
	  --json synth/fabric2_k4b4a8e1_ice40.json --freq 12 \
	  --timing-allow-fail --pcf-allow-unconstrained \
	  --asc synth/fabric2_k4b4a8e1.asc --report synth/report_k4b4a8e1.json
	icepack synth/fabric2_k4b4a8e1.asc synth/fabric2_k4b4a8e1.bin

## clean — remove generated proof dirs and TB run artifacts (keeps sources).
clean:
	rm -rf formal/cell_core.fair formal/cell_core.tick formal/flit_pipe.fly \
	       formal/fabric.conservation formal/echo_gate.dyadic \
	       tb/formal/flit_pipe tb/run /tmp/quf_out*
