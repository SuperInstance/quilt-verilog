# HOSTILE CONSUMER REPORT — first outside attack on QUF

**Lane:** hostile-consumer · **Date:** 2026-08-30 · **Rule honored:** implementer read
`docs/QUF-SPEC.md` only. `tools/quf.py`, `rtl/`, `tb/`, and the tests were NOT read.
Independent parser written from the spec text alone, in **Rust** (chosen for explicit
integer widths against a binary format; zero unsafe code).

- Parser: `hostile-consumer/src/main.rs` (binary `qufparse`)
- Fuzzer: `hostile-consumer/fuzz.py` (mutants under `hostile-consumer/corpus/mutants/`)
- Build: `cd hostile-consumer && cargo build`

## 1. Conformance sweep — committed QUF artifacts

| artifact | verdict |
|---|---|
| examples/t3_quf_roundtrip/out/room.quf | clean |
| examples/t3_quf_roundtrip/out/room_evolved.quf | clean |
| examples/t4_cli_tools/out/room.quf | clean |
| tb/run/quf_tb_input.quf (golden vector) | clean — 576 B, layout matches §11 |
| tools/edgebench/chipmatrix_runs/cells_cpu.quf | clean |
| tools/edgebench/chipmatrix_runs/cells_gpu.quf | clean |
| tools/openmic/night/tap-openmic.quf | clean |
| quilt-tournament teams/shipwright/state.quf | **FAIL BadMagic — magic is `QC3\0`, not `QUF\0`** |

**7 parsed clean, 1 hard fail.** The failure is Finding F1 below: the first external
consumer in the wild labels a non-QUF file `.quf`. Repro:
`cd hostile-consumer && ./target/debug/qufparse ../../quilt-tournament/teams/shipwright/state.quf`

## 2. Spec-fuzz — 26 mutants, classified by the spec's stated rules

Every outcome the spec text does NOT determine is a spec bug. Numbered findings:

### CONTRADICTION (1)

**F2 — §5 vs §8.5: nonzero bytes after the last section.** §5: "zero padding
between/after" sections. §8.5: "Bytes after the last section (within the final
padding) are ignored." Nonzero trailing garbage is simultaneously "invalid layout"
(§5) and "must be ignored" (§8.5). Mutation: flip one byte in the final padding run.
Repro: `python3 fuzz.py` (mutant `truncate-575` adjacent; direct case: flip last byte
of tb/run/quf_tb_input.quf, run qufparse).

### UNDERSPECIFIED (3)

**F3 — unpadded file length.** §5 says the *reference writer* pads the file to
`align`; it never says whether a file whose length is not a multiple of `align` is
invalid or accepted. Mutation: truncate the golden vector by 1 byte (576→575, all
sections intact). Repro: `./target/debug/qufparse corpus/mutants/truncate-575.quf`.

**F4 — who enforces the 4 GiB limit?** §9 limits files to <4 GiB ("u64 high words
must be zero") for the RTL profile with error 7, but §2/§5 (the format proper) put
no bound on offset/size u64s. Two legal consumers can disagree on the same file.
Mutation: oversized section table with nonzero u64 high words.
Repro: `./target/debug/qufparse corpus/mutants/section-count-1000.quf`.

**F5 — are the §6 size formulas enforced?** §6 gives `dials = cell_count×32`,
`edges = edge_count×(12+K)`, `ticks = 4+4×cell_count` but never states that a
present-but-wrong `cell_count` (etc.) is a verification failure. The writer
"derives" counts when omitted — when present AND inconsistent, behavior is unstated.
Mutation: set `cell_count` KV to 3 with a 2-cell dials section.
Repro: patch kv `cell_count` value word to 3; run qufparse.

### AMBIGUITY (5)

**F6 — truncated file semantics.** Nowhere does the spec say a reader must reject
a file cut mid-header, mid-KV, or mid-table. §5's "must not extend past end of
file" covers section payloads only. Mutations: truncate at 8/16/100/300 bytes.
Repro: `./target/debug/qufparse corpus/mutants/truncate-16.quf`.

**F7 — count fields that lie.** `kv_count`/`section_count` larger than the data
present walk the reader off the file; no bound or overrun rule exists for the
header/table region (RTL error 3 "layout overrun" hints but binds only §9).
Mutations: `kvcount-lie-11`, `section-count-0xFFFFFFFF`.
Repro: `./target/debug/qufparse corpus/mutants/kvcount-lie-11.quf`.

**F8 — invalid UTF-8 in names.** §4/§5 say "name_len × UTF-8 bytes" but define no
failure semantics for invalid sequences (length-counted bytes, so skip-size is
determinate — content validation is not).

**F9 — zero-length known sections.** §6 never says a known section (e.g. `dials`)
may or may not be size 0. With size 0 the former payload becomes inter-section
padding that is then nonzero (F2's twin for interior bytes — §5 does say interior
padding is zero, so this one is determinate, but only by inference; a one-line rule
would close it). Repro: `./target/debug/qufparse corpus/mutants/zero-size-dials.quf`.

**F10 — endian-word rejection is profile-scoped.** §3 says "No other value is
defined" and §7 says a big-endian host "detects and refuses" — but refusal is only
mandated as RTL error 4, not for the full profile. Mutation: endian=0, endian=2.
Repro: `./target/debug/qufparse corpus/mutants/endian-zero.quf`.

**F11 — section payload may overlap the header/KV/table region.** §5 forbids
sections overlapping *each other*, but never requires `offset` to be past the end
of the header+KV+table. A hostile file can point `dials` at offset 32 — straight
into the KV metadata — satisfying every stated rule. Mutation: rewrite the first
section-entry offset from 384 to 32. (found by the claude -p pass)
Repro: patch u64 offset of section 0 in tb/run/quf_tb_input.quf to 32; qufparse.

**F12 — string/array value lengths are unbounded.** A KV string (type 8) or array
(type 9) declaring len/count = 0xFFFFFFFF is length-validated by nothing in §4;
skip-size arithmetic can overflow or read past EOF, and the spec gives no
failure rule distinct from F6/F7. (found by the claude -p pass)
Repro: patch a KV string value's u32 length word to 0xFFFFFFFF; qufparse.

### ECOSYSTEM (1)

**F1 — `.quf` extension hijack in the wild.** Tournament team shipwright's
`state.quf` carries magic `QC3\0` version 3 — a private format mislabeled with the
QUF extension. Not a spec bug, but the first observed consumer-vs-format drift;
worth a "magic gate" line in the tournament referee. (See §1 repro.)

## 3. Verdict

- **Spec bugs: 11** — 1 contradiction (F2), 3 underspecified (F3, F4, F5),
  7 ambiguities (F6–F12) — plus 1 ecosystem finding (F1).
- 7/8 committed artifacts parse clean from the spec alone; the one failure is
  consumer-side mislabeling, not a spec defect.
- Core container rules (magic/version/endian/alignment/overlap/unknown-skip) are
  crisp and survived every mutation with a determinate answer. The gaps cluster
  in exactly one place: **hostile-input semantics — what a reader must REJECT vs
  tolerate when the file lies about itself.** A ~15-line "§5a Invalid files"
  (truncation, count/length overrun, table-overlap, trailing-bytes precedence,
  formula enforcement, u64 high words) would close all 11.

## Provenance

- **qufparse (Rust, this agent, GLM-5.3 subagent)** — spec-only parser + conformance
  sweep + fuzzer; found F1 (QC3 hijack), F3 (truncate-575 gap), F6/F7 (truncation
  and lying counts — the sharpest family), F9.
- **claude -p independent pass** — adversarial spec readout (12-item list),
  cross-checked against the fuzz table; corroborated F2/F6/F7 and independently
  contributed F8 (invalid UTF-8), F11 (section-over-table overlap — its best
  find), and F12 (unbounded string/array lengths). F5 phrasing corroborated.
- opencode run --auto: not dispatched — the claude pass returned a full
  independent finding list that the fuzzer confirmed; a third pass would not
  have changed the outcome.
- F2 (the contradiction, best single find) and F4 were surfaced by the fuzzer run
  and pinned to spec text by this agent.
