# hostile-consumer

First outside attack on the QUF format: an independent parser + spec-fuzzer,
written from `docs/QUF-SPEC.md` ONLY (no access to `tools/quf.py`, `rtl/`, tests).

- `src/main.rs` — Rust parser (`qufparse`), spec-only
- `fuzz.py` — mutant generator; writes `corpus/mutants/`
- Findings: `docs/HOSTILE-CONSUMER-REPORT.md`

```sh
cargo build
./target/debug/qufparse <file.quf> [--dump]
python3 fuzz.py [seed.quf]
```
