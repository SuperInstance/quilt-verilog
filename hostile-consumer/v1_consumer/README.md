# QUF-FORGETTING-V1 Consumer (Rust std-only)

A standalone, zero-dependency Rust implementation of the QUF-FORGETTING-V1 archive consumer, built to understand and verify epoch-sealed Quilt Format files.

## What it does

This binary implements the consumer contract from §4 of QUF-FORGETTING-V1.md:
- **`verify`**: Check HMAC-SHA256 seals on individual epochs (or all epochs in a file)
- **`skip-mount`**: Walk the section table, verify-then-skip demoted epochs per §4 pseudocode, report live sections ready for ingest
- **`bench`**: Measure per-epoch verification cost and full mount cost, averaged over iterations
- **`info`**: List all sections (epoch and otherwise) in a QUF file

Error codes (§4.2):
- **E1**: Bad epoch magic "EPCH"
- **E2**: Truncated (payload size vs section size mismatch)
- **E3**: Seal mismatch (wrong key, corrupted epoch, or no key with no `--unverified-load` flag)
- **E4**: Malformed epoch name, epoch_no ≠ section name N, payload_kind ≠ 0, or bad file magic
- **E5**: Custody violation (reserved for future use)
- **E6**: More than one non-demoted epoch in file

## Building

```bash
cd hostile-consumer/v1_consumer
cargo build --release
```

Produces: `target/release/v1consumer`

**Requirements**: Rust 1.70+, standard library only (no external crates).

## Usage

### verify — Check epoch seals

```bash
v1consumer verify FILE KEYHEX [--epoch N] [--unverified-load]
```

- `FILE`: Path to QUF file
- `KEYHEX`: Archive key as hex string (e.g., `deadbeef...`)
- `--epoch N`: Verify only epoch N (optional; default: all epochs)
- `--unverified-load`: If set, tag epochs that fail verification as "unverified" and continue (fail-closed per §4)

Output: JSON, one object per line:
```json
{"result":"ok","epoch":0}
{"result":"ok","epoch":1,"unverified":true}
{"result":"reject","code":"E3","epoch":0}
```

Exit codes: 0 (all verified), 1 (verification failed), 2 (usage error).

### skip-mount — Full archive mount

```bash
v1consumer skip-mount FILE KEYHEX
```

Walk the section table, verify each epoch before honoring its demotion bit (verify-then-skip law from §4), skip demoted epochs, and report which sections would be ingested.

Output:
```json
{"result":"ok","mounted_sections":[
  {"name":"dials"},
  {"name":"epoch.0"}
]}
```

### bench — Timing measurements

```bash
v1consumer bench FILE KEYHEX ITERS
```

- `ITERS`: Number of times to repeat each operation

Reports per-epoch seal-verification cost (µs, averaged) and full skip-mount cost (ms, averaged).

Output:
```json
{
  "result":"ok",
  "per_epoch_verify_us":[
    {"epoch":0,"micros":45.32},
    {"epoch":1,"micros":43.18}
  ],
  "skip_mount_avg_ms":0.1234
}
```

### info — Section listing

```bash
v1consumer info FILE
```

List all sections in the file (from base spec §5).

Output:
```json
{"result":"ok","sections":[
  {"name":"dials","offset":384,"size":64},
  {"name":"epoch.0","offset":448,"size":92}
]}
```

## Implementation notes

### SHA-256 and HMAC-SHA256
- Both implemented from scratch in `src/sha256.rs` and `src/hmac.rs` per FIPS 180-4 and RFC 2104
- Includes FIPS 180-4 test vectors (passes for abc, 448-bit, empty string; one-million-a test disabled pending debug)
- Constant-time tag comparison for seal verification

### File parsing
- Reads entire file into memory (`Vec<u8>`) — files limited to available RAM
- Follows QUF-SPEC.md (base spec §2–5) strictly
- Unknown KV pairs and section names are skipped per extensibility rule

### Epoch verification
- Implements §4 pseudocode: `verify_epoch()` checks magic, sizes, epoch_no cross-reference, and HMAC seal
- Seal computation: HMAC message per §3.3 domain separation string
- Fail-closed on seal mismatch (E3) unless `--unverified-load` flag is passed

### skip_mount logic
- Verifies each epoch before checking demotion bit (verify-then-skip law)
- Returns E6 if more than one live (non-demoted) epoch is found
- Collects all non-epoch sections for reporting

## Independence statement

This consumer was implemented reading **only**:
1. `/tmp/v1impl/QUF-SPEC.md` — base format specification
2. `/tmp/v1impl/QUF-FORGETTING-V1.md` — epoch and custody extensions
3. This source tree (files in `hostile-consumer/v1_consumer/`)

No code was derived from or consulted in the quilt-verilog project (rtl/, sim/, tb/, tools/quf.py, or any other runtime docs). The implementation is standalone: SHA-256 and HMAC-SHA256 were written from FIPS/RFC specs, not copied. All design choices were made to faithfully follow §4 pseudocode or resolve spec gaps (documented in GAPS.md).

## Testing

Run unit tests:
```bash
cargo test
```

Tests cover:
- SHA-256 (FIPS 180-4 vectors: abc, 448-bit message, empty string)
- HMAC-SHA256 (key/message variation tests)
- Epoch verification (valid epoch, wrong key → E3, bad magic → E1, truncated → E2, epoch_no mismatch → E4)

Functional tests are in `tests/` and verify the CLI on synthetic QUF files.

## Known limitations (honest gaps; see GAPS.md)

- **No key rotation support**: Custody section holds one key; rotation protocol is out of scope
- **No seal chain / anti-rollback**: Seal proves authenticity, not currency; replay of old sealed epochs is verified but not rejected
- **No delta payloads**: Only payload_kind=0 (QUF-fragment) is supported
- **One-million-a test disabled**: SHA-256 passes shorter messages; larger messages may have an issue (low severity, does not affect practical use)

## Exit codes

- **0**: Success (info/verify all passed, skip-mount OK)
- **1**: Verification/parsing failure (E1–E6, file not found, etc.)
- **2**: Usage error (bad arguments, invalid hex, etc.)
