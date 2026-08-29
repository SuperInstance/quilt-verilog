# Skeleton Compile & Lint Harness — Round 1 Verification

Date: 2026-08-29. Toolchain: `/home/eileen/tools/oss-cad-suite/bin` (iverilog, verilator), on PATH.

Method: every ```verilog fenced block in `proposals/{seed,claude,glm,opencode}/RTL-SKETCH.md` was
extracted verbatim to `tb/scratch/<entry>_<module>.v` with a provenance header line. Each file
compiled with `iverilog -g2005 -o /dev/null` and linted with `verilator --lint-only -Wall
--default-language 1364-2005`. Where a skeleton instantiates sibling skeletons from the same
entry, the siblings were included in the compile (opencode q_cosine_stream + q_isqrt16 + q_divu;
seed quilt_cell + hebbian_edge_update retry).

**Artifact note:** every `%Warning-DECLFILENAME` in the logs is a harness artifact of the
`<entry>_` filename prefix vs. the module name — NOT a defect of the entry. All other
warnings/errors are real. `glm_tb_qs_dial.v` is a testbench example, excluded from the tally.

## Tally: 17 / 24 iverilog-clean

| Entry | Skeletons | Compile | Verilator -Wall clean | Key failures |
|---|---|---|---|---|
| opencode | 9 | 9/9 | 0/9 (width warnings only) | none fatal; WIDTHTRUNC/WIDTHEXP/UNUSEDSIGNAL |
| glm | 8 | 5/8 | 0/8 | qs_cell_core: use-before-declaration of `st`/`S_IDLE` (iverilog elaboration error); qs_fabric: unresolved `qs_cell`/`qs_tickgen` deps (wrapper not provided); qs_hebb_edge: UNOPTFLAT circular comb on readout tree `t` |
| seed | 3 | 1/3 | 0/3 | quilt_cell: block-local variable declarations require SystemVerilog + reversed-range slice `dial[3:0]` on unpacked array; quilt_fabric: `cell` used as instance name = reserved word, invalid instantiation |
| claude | 4 | 1/4 | 0/4 | cell_fsm: procedural assignment to `wire` outputs (10 errors); link_arbiter: unpacked-array port (illegal V2005); tick_scheduler: `int` type + bare `disable;` (SystemVerilog-isms, syntax errors) |
| zeroclaw | 0 | — | — | no RTL-SKETCH.md shipped |

## Verbatim tool output

Appended below, unedited except DECLFILENAME-filtered copies where noted in the review docs.
Full raw log preserved in `tb/scratch/compile-log.txt`.

See `docs/review-*.md` for per-entry analysis of these results.
