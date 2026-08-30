# Specification Gaps and Implementation Decisions

Numbered log of places where QUF-SPEC.md and QUF-FORGETTING-V1.md were insufficient to implement without making choices. Each entry documents: **WHERE** (section), **WHAT** is underspecified, **WHAT YOU GUESSED** (the chosen resolution), and **SEVERITY**.

---

## 1. KV pair size computation (§4, QUF-SPEC.md base spec)

**WHERE**: QUF-SPEC.md §4 (Header KV metadata)

**WHAT**: For array type (id=9), the spec says `u32 elem_type, u32 count, count × elements`, but does not explicitly state whether `elem_type` must be a fixed-size type or if nested types (arrays/strings) are allowed.

**WHAT YOU GUESSED**: Nested arrays/strings in array elements are forbidden; only fixed-size types (u8–u64, bool) are valid. This matches the RTL loader profile's constraint (§9). Parser rejects any elem_type outside 0–7, 10–12 as E4.

**SEVERITY**: Low — the spec says "fixed-size" in the text (§4 value-type table), but the pseudocode does not show element type validation. Matches RTL profile intent.

---

## 2. Epoch section naming format (§2.2, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §2.2 and §4

**WHAT**: Spec says "decimal N, no zero padding" for epoch section names (`epoch.0`, `epoch.12`), and "ASCII digits only (§4)". What exactly is "ASCII digits only"? Does it mean:
- All characters in the name part (after `epoch.`) must be digits (0–9)?
- Or just the numeric portion can use hex, octal, etc.?

**WHAT YOU GUESSED**: After `epoch.`, all characters must be ASCII decimal digits (0–9), matched via `isascii_digit()`. Leading zeros are forbidden (e.g., `epoch.00` is invalid). Parser extracts the name suffix and validates this before parsing epoch_no.

**SEVERITY**: Low — spec text is clear ("ASCII digits only"), but the pseudocode (§4) only checks `isascii_digit()` without specifying rejection of leading zeros. Implementation is strict.

---

## 3. Custody section presence and E5 trigger (§6, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §6 (Custody requirements)

**WHAT**: §6 requirement 3 says "a consumer that finds epoch sections but no `custody` section... reports **E5**". However, the pseudocode in §4 does not mention E5 at all. When exactly should E5 be raised?
- If there are any `epoch.N` sections and no `custody` section?
- If custody section exists but keys cannot be resolved?
- Only during skip_mount, not verify?

**WHAT YOU GUESSED**: E5 is reserved for custody violations but not currently implemented in verify_epoch or skip_mount. The pseudocode in §4 does not show where E5 would be raised, and the spec says custody section is optional ("0 or 1" per §2.2). This is marked as a gap but not implemented, treating it as advisory-only for now. If strict custody validation were needed, E5 would be raised when epoch sections exist but custody section is absent or cannot be validated.

**SEVERITY**: High — this is an honest gap where the spec's requirement (§6, item 3) contradicts the pseudocode (§4, which does not show E5 handling). Implementer chose to follow the pseudocode and treat it as future work.

---

## 4. Epoch section table ordering (§2.5, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §2.5

**WHAT**: Spec says custody section "MUST come before the first `epoch.<N>` section in table order". Does this mean:
- The custody section must appear earlier in the section table entries (lower offset)?
- Or only that custody must be parsed before any epoch is restored?

**WHAT YOU GUESSED**: Implementation does not validate table ordering; it walks the section table and processes epochs as found. If strict ordering is needed, a validation pass would check that the custody section entry (by offset) comes before all epoch section entries. For now, this is assumed to be a writer requirement, not a reader validation requirement.

**SEVERITY**: Medium — the spec uses "MUST" language, but the pseudocode does not show validation. This could be a security requirement (enforce ordering as part of the spec contract) or a producer guideline (producers emit it correctly). Conservative choice: follow pseudocode, not requirement text.

---

## 5. Alignment in section table (§5, QUF-SPEC.md + §2.3, QUF-FORGETTING-V1.md)

**WHERE**: QUF-SPEC.md §5 and §7

**WHAT**: Base spec requires section offsets to be multiples of `align` (default 32). For epoch sections, is this alignment requirement:
- The offset in the section table entry must be aligned?
- The offset to the first byte of the epoch payload (after the 48-byte header) must be aligned?
- Or no alignment required for epoch sections specifically?

**WHAT YOU GUESSED**: Epoch section offsets follow the same alignment rules as any other section: the offset in the table entry must be a multiple of `align`. Parser does not validate this (it's a writer constraint), but the implementation assumes offsets point to the start of the epoch magic ("EPCH") without padding between header and payload.

**SEVERITY**: Low — the spec is clear that section offsets must be aligned, but does not explicitly repeat this for epoch sections. Implementation assumes standard alignment applies.

---

## 6. Fail-closed behavior with `--unverified-load` (§4, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §4 (Fail-closed rule)

**WHAT**: The pseudocode says "it may load it unverified only if the operator explicitly passes an 'unverified-load' flag, and every restored epoch must then be tagged unverified in consumer output." But the pseudocode does not show HOW to tag unverified epochs. Is it:
- A JSON field `"unverified":true` on each epoch's output?
- A different result code?
- A separate log message?

**WHAT YOU GUESSED**: When `--unverified-load` is set and an epoch fails verification (E3), the verify command tags that epoch with `"unverified":true` in the output JSON and continues. skip_mount would similarly tag sections sourced from unverified epochs. Implementation outputs JSON with this field for CLI transparency.

**SEVERITY**: Low — the spec intent is clear (mark unverified epochs); the output format was chosen for CLI clarity.

---

## 7. Skip-mount return value and order (§4, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §4 pseudocode `skip_demoted()`

**WHAT**: The pseudocode shows `skip_demoted()` returning `live`, a list of sections. But the spec does not say:
- What order should live sections be returned in? (table order? by type?)
- Should demoted epochs be included in the output (marked as demoted)?
- Should custody section be included?

**WHAT YOU GUESSED**: Implementation returns sections in table order. Demoted epochs are skipped (not returned). Custody section is returned if present. Non-epoch sections (dials, edges, routing, ticks) are returned as-is. The output is a JSON array of section names, allowing the operator to see what would be ingested.

**SEVERITY**: Low — spec does not define the output format, only that sections should be returned. JSON format was chosen for tooling clarity.

---

## 8. Epoch offset and truncation (§2.3, §4, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §2.3 and §4

**WHAT**: The pseudocode checks `len(section_bytes) != 48 + payload_len + 32` to detect truncation (E2). But what if:
- The payload_len field is itself corrupted (claims a huge size)?
- The seal is malformed (too short)?
- Should we bounds-check payload_len before reading?

**WHAT YOU GUESSED**: Parser first checks if section_bytes has at least 80 bytes (48 header + 0 payload + 32 seal minimum). Then it reads payload_len from the header. If the computed size (48 + payload_len + 32) does not match len(section_bytes), E2 is raised. No bounds-check on payload_len itself; if it's huge and section_bytes is short, the exact-size check will catch it as E2.

**SEVERITY**: Low — the pseudocode's approach is sound; implementation follows it.

---

## 9. Reserved bytes validation (§2.3, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §2.3 (epoch header layout)

**WHAT**: The epoch header has three reserved byte ranges (rsvd0, rsvd1, rsvd2, all "zero"). Should verification fail if these bytes are non-zero?
- §2.3 says "must be 0" (producer requirement).
- §3.1 says consumers "MUST NOT interpret reserved bits; writers MUST emit 0".
- But does a reader reject if they're non-zero, or silently ignore?

**WHAT YOU GUESSED**: Implementation does not validate reserved bytes. They are read but not checked. This follows the principle that reserved fields are for future expansion, and a reader should not break on new data. If strict validation is required, a future version could add a check.

**SEVERITY**: Low — spec text suggests writers must emit 0, but does not mandate reader validation. Conservative choice: ignore them.

---

## 10. Endianness and epoch sections (§7, QUF-SPEC.md + §2.3, QUF-FORGETTING-V1.md)

**WHERE**: QUF-SPEC.md §7 and QUF-FORGETTING-V1.md §2.3

**WHAT**: Base spec says "little-endian everywhere". Epoch section header fields (epoch_no, created_tick, etc.) are u32/u64, so they are little-endian. But:
- Is the magic "EPCH" (b"EPCH" = 0x45504348) meant to be byte-for-byte as shown, or byte-swapped?
- Should "EPCH" be verified as a fixed 4-byte sequence or parsed as a u32?

**WHAT YOU GUESSED**: "EPCH" is verified as a byte-for-byte match (b"EPCH" = [0x45, 0x50, 0x43, 0x48]). It is not parsed as a u32 for endianness reasons; the spec quotes it as a string. This is the conservative choice.

**SEVERITY**: Low — spec clearly shows "EPCH" as a string; implementation treats it as literal bytes.

---

## 11. HMAC message construction — field order (§3.3, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §3.3 (Seal — keyed epoch digest)

**WHAT**: The domain separation string is given as pseudocode, but the exact byte order for multi-byte fields is not explicit. Is it:
- `u32le_bytes(epoch_no) || ...` (little-endian u32)?
- Or big-endian?

**WHAT YOU GUESSED**: All multi-byte fields in the HMAC message are little-endian, matching the QUF file format. This is consistent with base spec §7. Implementation encodes epoch_no, created_tick, payload_kind, primer_addr, and payload_len as little-endian u32/u64 in the HMAC message.

**SEVERITY**: Low — spec example pseudocode shows `u32le_bytes()`, making it explicit. Implementation follows this.

---

## 12. Constant-time comparison library (§4, pseudocode reference)

**WHERE**: QUF-FORGETTING-V1.md §4 pseudocode

**WHAT**: The pseudocode shows `hmac.compare_digest(...)`, suggesting a constant-time comparison function. But in Rust std (no external crates), this function does not exist. Should the comparison be:
- Simple `==` (vulnerable to timing attacks)?
- Manual constant-time loop?
- None (assume this is not a threat)?

**WHAT YOU GUESSED**: Implementation includes a hand-written constant-time comparison function (`constant_time_compare`) that XORs all bytes and checks if the result is zero. This matches the intent of `compare_digest` and is appropriate for cryptographic verification.

**SEVERITY**: Medium — this is a real security concern (timing-attack on seal verification). Implementation addresses it, but the spec did not make it explicit. A reference to RFC 2104 section 4 (Keyed-Hashing) would have helped.

---

## 13. File offset limits (§9, QUF-SPEC.md RTL loader profile)

**WHERE**: QUF-SPEC.md §9 (RTL loader profile)

**WHAT**: The spec says files must be < 4 GiB and "u64 high words must be zero" (error code 7). But:
- Does this apply to all QUF files, or only those targeting the RTL profile?
- Should a consumer reject files with >32-bit offsets?

**WHAT YOU GUESSED**: Implementation does not validate the < 4 GiB constraint (no check for high words of u64 offsets/sizes). This is treated as a loader-profile-specific requirement, not a core consumer requirement. A strict validator could add this check.

**SEVERITY**: Low — the spec explicitly marks this as an RTL profile constraint. Standalone consumer ignores it.

---

## 14. Section size = 0 (edge case)

**WHERE**: QUF-SPEC.md §5, §6

**WHAT**: The spec does not explicitly forbid a section with size = 0. Should this be:
- Allowed (empty section)?
- Rejected as E2 (bad structure)?
- Allowed for custody section (which is optional)?

**WHAT YOU GUESSED**: Implementation allows sections with size = 0. This would be unusual but not invalid per spec. For epoch sections, a size < 80 (48 header + 0 payload + 32 seal) would fail verification with E2 during epoch processing.

**SEVERITY**: Low — edge case that spec does not address. Implementation is permissive.

---

## 15. Multiple custody sections (§2.2, QUF-FORGETTING-V1.md)

**WHERE**: QUF-FORGETTING-V1.md §2.2

**WHAT**: Spec says custody section is "0 or 1" per file. If a file has two custody sections (unlikely but not forbidden by parser), which one should be trusted?

**WHAT YOU GUESSED**: Implementation does not track or validate uniqueness of the custody section. If multiple custody sections exist, the consumer treats them as independent sections (both returned by info/skip-mount). A stricter validator could reject duplicate section names.

**SEVERITY**: Low — spec intent is clear (at most one); implementation does not validate this, treating it as a writer constraint.

---

## Summary of severity distribution

- **High**: 1 (custody E5 contradiction)
- **Medium**: 2 (custody ordering, constant-time comparison)
- **Low**: 12 (naming, reserved bytes, offset limits, etc.)

**Action**: All gaps are either resolvable via the spec's extensibility rules, treated as writer constraints (not reader validation), or addressed by following the pseudocode faithfully. E5 is the only unresolved normative gap where §6 and §4 disagree; it is deferred to future work.

---

## Foreman cross-check additions (measured against the built consumer, not from code review)

These were confirmed by hostile corpus probes after the implementer pass; they are
gaps the implementer's faithful-to-§4 code inherited from the pseudocode itself.

### 16. §4 name check never rejects (measured, HIGH)

**WHERE**: §4 `skip_demoted` pseudocode, `E4_BAD_NAME` line.
**WHAT**: The pseudocode checks `not name[6:].isascii_digit()` → `E4_BAD_NAME`, but the
check is an expression, not a return/raise; control falls through to the
`kind == 0` branch and a malformed name matches neither branch, so the section is
neither rejected nor mounted. Measured: renaming `epoch.1` → `epoch.05` in an
otherwise-valid file yields `ok` with the epoch silently DROPPED (mounted_sections
excludes it, no E4). An attacker can hide an epoch from a §4-faithful consumer.
**FIX**: pseudocode needs `raise E4` semantics, and spec must state whether
malformed-name epoch sections reject the file (recommended) or skip loudly.
**SEVERITY**: High (silent data hiding; the E-code exists in §4.2 but is unreachable
in §4's own pseudocode as written).

### 17. `restore(sec)` is referenced but undefined (HIGH for full mount)

**WHERE**: §4 `skip_demoted`, `live.append(restore(sec))` → "§2.3 replay".
**WHAT**: Restoration "through the same write paths the loader drives" is a
reference to house machinery (base spec §9 loader). §4 alone cannot implement
restore; only verify + skip are truly §4-derivable. The independence claim in the
one-sentence contract holds for (a) verify and (b) skip, but NOT for restore.
**SEVERITY**: High for any consumer that must actually load live state; the v1
consumer here reports what WOULD be ingested and does not restore.

### 18. "skip demoted epochs in O(1) mount" is not defined anywhere (MED)

**WHERE**: one-sentence contract (§ preamble) vs §4.
**WHAT**: §4's `skip_demoted` reads the full section (`read_at(off, size)`) for
every epoch, demoted or not (verify-then-skip needs the seal, which needs the
payload bytes — the seal covers the payload). So per-epoch skip cost is
O(payload), and total mount cost is O(N·payload). If O(1) means "per-epoch header
inspection without touching payload", the seal design (payload covered, tag at
end) makes that impossible — you cannot verify a demoted epoch without reading
its payload. The spec should either drop the O(1) phrasing or define a
header-only skip tier for trusted-local contexts.
**SEVERITY**: Medium (performance claim vs mechanism mismatch; security vs speed
tension left implicit).
