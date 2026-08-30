# examples/ — runnable tutorials with committed expected outputs

Companion code for [docs/TUTORIALS.md](../docs/TUTORIALS.md) and
[docs/USER-GUIDE.md](../docs/USER-GUIDE.md). Each directory is
self-contained: a `run.sh` that compiles/derives only into its own
`out/` (gitignored), runs the real RTL or the real `tools/quf.py`, and
**diffs its stdout against a committed `.expected` file** — exit 0
means you reproduced the documented behavior byte-for-byte.

| dir | lesson | door | runtime |
|-----|--------|------|---------|
| `t1_first_fabric/`  | five opcodes on a live 2-cell fabric: bind, dial write/read, link, one effect, tick leak | parallel flit port (`q_fabric_top`, iverilog) | <1 s |
| `t2_hebbian_edges/` | the Hebbian ladder: 10 cofires = +0xA00 exactly, HL=2 sweep forgets to base; VCD for GTKWave | parallel flit port (iverilog) | <1 s |
| `t3_quf_roundtrip/` | state is a file: save, reload, canonical-form identity, mutate, restore, three refusal classes | Python (`tools/quf.py`) | <1 s |
| `t4_cli_tools/`     | the QUF CLI tour: create → verify → info → dump → hex on a real container | Python CLI (`tools/quf.py`) | <1 s |

Run them all:

```sh
bash examples/t1_first_fabric/run.sh
bash examples/t2_hebbian_edges/run.sh
bash examples/t3_quf_roundtrip/run.sh
bash examples/t4_cli_tools/run.sh
```

Toolchain: oss-cad-suite on `PATH` or via `OSSCAD=/path/to/bin` for the
Verilog examples (T1/T2); Python ≥ 3.8 stdlib for T3/T4. Expected
outputs were generated with Icarus 13.0 / CPython 3.14 on this tree;
`.expected` files contain no machine-specific paths.

Progressive order is T1 → T2 → T3; T4 is the CLI appendix. The
testbenches in `tb/` are the deeper usage reference (same house
patterns, harder assertions) — see `tb/run_suite.sh` and
[docs/VERIFICATION.md](../docs/VERIFICATION.md).
