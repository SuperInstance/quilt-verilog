# V1 CONSUMER — §4 independence test (measured, 2026-08-30)

Question under test (docs/QUF-FORGETTING-V1.md, a83c5be): *is `verify_epoch()` /
`skip_demoted()` implementable from §4 alone by a consumer that has never read
house law?* Tested the hard way: an independent Rust consumer
(`hostile-consumer/v1_consumer/`) written by a `claude -p` pass that read ONLY
`QUF-FORGETTING-V1.md` + `QUF-SPEC.md` (copies staged in a brief dir), forbidden
`rtl/`, `sim/`, `tb/`, `tools/quf.py`. Artifacts produced by the reference
producer lane (`tools/quf_epoch.py`, which builds on `quf.py` — a producer is
not a consumer). See README.md / IMPLEMENTATION.md in this crate for the
implementer's own independence statement.

**Verdict: PROVEN for verify + skip — with 18 numbered spec gaps (15 implementer,
3 foreman cross-check). §4 alone is sufficient to seal-verify, reject forgeries,
honor verify-then-skip, and skip-mount. It is NOT sufficient for restore (gap 17)
nor for the §6 custody/E5 law (gap 3), and its own E4_BAD_NAME check is
unreachable as written (gap 16, measured silent epoch-hiding).**

## Pass/reject matrix (measured)

Consumer: `./target/release/v1consumer`, corpus in `corpus/`. Commands:
`v1consumer verify FILE KEYHEX` / `v1consumer skip-mount FILE KEYHEX`.
K = archive key (0x11×32), WK = attacker key (0xaa×32).

| # | Case | Command | Expected | Measured |
|---|------|---------|----------|----------|
| 1 | honest file, N=4/16/64, right key | verify all | all PASS | ✅ PASS, exit 0 |
| 2 | honest file, wrong key supplied | verify | E3 | ✅ E3 epoch 0, exit 1 |
| 3 | attacker-resealed epoch 0 (honest rest) | verify | E3 | ✅ E3 epoch 0, exit 1 |
| 4 | **demotion bit flipped, live→demoted, no reseal** | skip-mount | E3 (verify-then-skip law) | ✅ E3, exit 1 |
| 5 | demotion bit flipped, demoted→live | skip-mount | E3 | ✅ E3, exit 1 |
| 6 | bad epoch magic | verify | E1 | ✅ E1, exit 1 |
| 7 | truncated file | verify | E2 | ✅ E2, exit 1 |
| 8 | epoch_no ≠ name N | verify | E4 | ✅ E4 epoch 0, exit 1 |
| 9 | two live epochs | skip-mount | E6 | ✅ E6, exit 1 |
| 10 | one honest live epoch | skip-mount | mount epoch.0 | ✅ mounts epoch.0, exit 0 |
| 11 | v1 base, zero epochs | skip-mount | 4 live sections | ✅ exit 0 |
| 12 | malformed epoch name `epoch.05` | skip-mount | E4 per §4.2 | ⚠️ silently DROPPED — gap 16 |
| 13 | flipbit under `--unverified-load` | skip-mount | restore tagged unverified | ✅ exit 0, no false verified claim |

Case 4 is the headline: a consumer that skipped-without-verifying would have
silently forgotten epoch 0; the §4 verify-then-skip law caught it as E3.

## Latency curve — first archive-key numbers (deadledger had none)

`v1consumer bench FILE KEYHEX 200`, release build, WSL2 x64, 7,488 B
payload/epoch (64-cell quilt fragment). Machine: eileen.

| N epochs | per-epoch seal-verify | full skip-mount |
|----------|----------------------|-----------------|
| 4  | ~23–64 µs (median ≈26 µs) | 0.17 ms |
| 16 | ~23–30 µs (median ≈26 µs) | 0.52 ms |
| 64 | ~23–85 µs (median ≈30 µs) | 2.03 ms |

Per-epoch verify cost is flat in N (≈25–30 µs/epoch ≈ 3.3 µs/KB — HMAC-SHA256
at ~0.3 GB/s, software); mount scales linearly with total bytes because the
seal covers the payload — see gap 18: "O(1) skip" in the one-sentence contract
cannot mean payload-free skipping, or the seal would not protect what is skipped.

## Spec-gap count: 18 (see GAPS.md)

- 1 High from implementer: **gap 3** — §6 item 3 makes custody/E5 a MUST, but §4
  pseudocode never raises E5; an implementer following §4 alone builds a
  consumer that cannot fail closed on custody violations.
- 2 Medium: gap 4 (custody table-order MUST not validated by §4), gap 12
  (constant-time compare not stated as normative).
- **Worst measured gap (foreman): gap 16** — §4's own `E4_BAD_NAME` check is an
  expression, not a rejection; control falls through and a malformed epoch name
  is silently dropped. Measured on the built consumer: renaming `epoch.1` →
  `epoch.05` yields `ok` with the epoch hidden from the mount list — a
  §4-faithful consumer can be made to not-see an epoch.
- Gap 17: `restore(sec)` is referenced, never defined — §4 proves verify+skip
  independence, not restore independence (restore needs base-spec §9 write
  paths = house law).
- Gap 18: "skip demoted epochs in O(1) mount" is undefined and, as sealed,
  impossible per-epoch without reading the payload.

## Provenance

- Implementer: `claude -p` (Sonnet, Pro plan), persistent tmux session, brief at
  /tmp/v1impl/BRIEF.md; read only QUF-FORGETTING-V1.md + QUF-SPEC.md. Stopped
  once to ask 3 questions (error precedence, SHA modularization, mmap vs read);
  decisions pre-baked and rerun.
- Foreman fixes post-pass (recorded, they do not touch the §4-derivation):
  1. The 1M-'a' SHA-256 "failure" was a wrong *test vector constant* in the
     implementer's test (real digest is cdc76e5c…112cd0; the code was correct).
  2. `skip-mount` gained `--unverified-load` (§4 requires the tag at mount).
  3. Gaps 16–18 added from foreman hostile probes (badname corpus case).
- Producer: `tools/quf_epoch.py` (new, this commit) — custody + epoch sections
  per §2.3/§2.5/§3.3, HMAC via Python stdlib, built on `quf.build/rebuild`.
  `quf.py verify` still passes on the extended files (unknown-name skip works).
- Gatekeeper: DeepInfra wide model UNREACHABLE (user-set inference limit hit);
  DeepSeek direct also balance-blocked. Fallback gatekeeper: opencode/GLM-4.6
  (different model family from the implementer), bullshit-test only. Verdict
  recorded below.
- GATEKEEPER VERDICT: <!-- filled after the gatekeeper pass -->
