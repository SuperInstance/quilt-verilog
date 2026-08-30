# QUF-FORGETTING-V1 — Self-Authenticating, Forgetting-Native Container (DRAFT)

Status: **format-spec draft. No RTL changes.** Builds on `docs/QUF-SPEC.md`
(hereafter "the base spec") without modifying its v1 byte layout. Every
structural claim about v1 cites the base spec by section and, for the golden
vector, by byte offset. Tournament requirement cited from
`../quilt-tournament/referee/R4-SCORES.md` (R4) by line.

The one-sentence contract: **any consumer, anywhere, with only this document,
can (a) verify that an epoch archive is intact and authentic and (b) skip a
demoted epoch — without knowing house law.** Forgetting stops being a runtime
behavior and becomes a format property, because formats outlive engines.

## 0. Why in the format (provenance of the decision)

- The adversarial council ruled QUF the five-year artifact ("GGUF outlived
  every llama.cpp debate"); the named weakness was that demotion/custody lived
  in house law, not in the file.
- R4 cross-team verdict item 1 (R4:75–78): **zero of six tournament entrants
  ship a distinct archive key** — the mint-key holder can forge anyone's
  archives. This draft makes the distinct archive key a spec-level MUST (§6).
- Tournament G4 probes (R4:22): all keyed entrants converged on keyed hash +
  custody substrate as the missing organ. This draft is the format-side
  answer; the fabric-side answer is the KHASH opcode proposal (§5).

## 1. Terms

- **Live state** — the four v1 sections (`dials`, `edges`, `routing`,
  `ticks`, base spec §6.1–6.4). Unchanged by this draft.
- **Epoch** — a numbered, immutable snapshot of live state taken at demotion
  time (or on demand).
- **Demotion** — the act of moving state from live to an epoch archive.
  Forgetting is demotion, not destruction (R4:63 phrasing; procession/
  deadband priced it best).
- **Seal** — HMAC-SHA256 over an epoch's canonical bytes under the **archive
  key** (distinct from every mint/hot-path key; §6).

## 2. Layout — where the new bytes live

### 2.1 What does NOT change

- Fixed header (16 B), KV region, section table mechanics, the four v1
  sections, and the golden 576-byte vector's bytes are untouched. The golden
  vector (base spec §11: dials @384, edges @448, routing @512, ticks @544,
  sha256 `5b2a236b…`) remains byte-identical and remains a valid
  QUF-FORGETTING-V1 file (a file with zero epochs).
- Base-spec §8 rule 3 (unknown section **names**: skip) is the v0/v1
  compatibility mechanism: a reader that predates this draft sees every
  epoch section below as an unknown name and skips it via the table, exactly
  as designed. No version bump is needed for parseability (§7 discusses the
  version question honestly).

### 2.2 New sections

Two new section names, both `kind = 0` (base spec §5: kind 0 is the standard
raw-bytes kind; using a new kind would also be skippable but buys nothing):

| name            | contents                        | per file |
|-----------------|---------------------------------|----------|
| `epoch.<N>`     | one epoch archive (§2.3)        | 0..65535 |
| `custody`       | custody manifest (§6, §2.5)     | 0 or 1   |

Names use decimal N, no zero padding (`epoch.0`, `epoch.12`), ASCII
digits only (§4). Name length: base §5 sets no limit; the ≤255-byte bound
is the RTL loader-profile limit (base spec §9) — writers targeting the
RTL profile MUST stay within it.

### 2.3 `epoch.<N>` payload layout

Fixed 48-byte epoch header, then payload bytes, then the 32-byte seal.
Little-endian throughout (base spec §2/§7).

| off | size | field        | notes                                          |
|-----|------|--------------|------------------------------------------------|
| 0   | u32  | epoch_magic  | `45 50 43 48` ("EPCH") — fail-fast sanity      |
| 4   | u32  | epoch_no     | == N in the section name (loaders cross-check) |
| 8   | u8   | status       | bit0: demoted. bits1–7: reserved, must be 0    |
| 9   | 3 B  | rsvd0        | zero                                           |
| 12  | u64  | created_tick | fabric tick counter at seal time               |
| 20  | u32  | payload_kind | 0 = QUF-fragment (see below)                   |
| 24  | u32  | payload_len  | bytes of payload that follow the header        |
| 28  | 4 B  | rsvd1        | zero                                           |
| 32  | 8 B  | primer_addr  | 64-bit primer address (§4.2)                  |
| 40  | 8 B  | rsvd2        | zero                                           |
| 48  | `payload_len` | payload | the archived bytes                          |
| 48+`payload_len` | 32 B | seal     | HMAC-SHA256 tag (§3)                           |

Section `size` must equal `48 + payload_len + 32`. `payload_kind = 0`
payload = the four v1 section payloads concatenated in table order
(dials, edges, routing, ticks), each padded to `align`. Restoration is
replay through the same *write paths* the loader drives (dialfile /
edge-RAM / route-RAM / tick writes, base spec §9), not a replay of the
whole-file word-stream parse — a fragment has no header/KV/table; the
consumer synthesizes the writes. Future payload kinds (e.g. deltas)
extend the space; this draft defines only 0.

### 2.4 The top-level `seal` section is deliberately absent

A whole-file seal was rejected in review (§8): the base spec says bytes
after the last section are ignored and padding is zero (§5), so a whole-file
digest would either cover mutable-by-convention padding (fragile) or require
canonicalization rules that v0 writers never promised (ignore rule:
base spec §8 rule 5 — citation corrected in review). Per-epoch seals cover
exactly the bytes an epoch claims — the explicit field list of §3.3 (epoch_no,
status, primer_addr, payload_len, payload; reserved bytes excluded) —
no canonicalization needed, v0 writers unaffected.

### 2.5 `custody` payload (summary; normative requirements in §6)

| off | size | field         | notes                                    |
|-----|------|---------------|------------------------------------------|
| 0   | u32  | algo_id       | 1 = HMAC-SHA256 (only value defined)     |
| 4   | u32  | key_count     | 1 in this draft                          |
| 8   | 16 B | key_id[0]     | truncated key identifier (see §6)        |
| 24  | u64  | ceremony_tick | when the archive key was last custoded   |

## 3. Wire fields — exact definitions

### 3.1 Demotion marker

- One byte: `epoch.<N>` header offset 8, `status`. Bit 0 set = **demoted**.
- Consumers MUST NOT interpret reserved bits; writers MUST emit 0.
- Demotion is observable by byte inspection at a fixed offset — a consumer
  needs no house law to find it.

### 3.2 Primer address

- 8 bytes little-endian at epoch-header offset 32: the fabric-wide address
  (epoch № × 2^32 | cell id, or a producer-defined opaque id when the high
  bit is set) of the primer record that names the custodian of this epoch.
  RTL consumers may ignore it; audit tooling uses it to locate the custody
  ceremony record. High bit set = "local/opaque", low 63 bits are a
  producer-defined address. This is the G4 custody-substrate hook in-file.

### 3.3 Seal — keyed epoch digest

- Primitive: **HMAC-SHA256** (RFC 2104). Chosen over raw SHA-256 because the
  R4 verdict's attack is *forgery by a key holder*, not corruption; over
  KMAC/BLAKE3 because HMAC-SHA256 is the one keyed hash every embedded
  consumer already has (ESP32 mbedTLS, iCE40 soft cores via the KHASH organ).
- Key: the **archive key** — MUST be distinct from every mint/hot-path key
  (§6, MUST-level).
- Domain separation: the HMAC message is
  `b"QUF-EPOCH-V1\x00" || epoch_no(4B) || status(1B) || created_tick(8B) ||
  payload_kind(4B) || primer_addr(8B) || payload_len(4B) || payload`.
  All non-reserved header fields are sealed (review catch: an unsealed
  `payload_kind` invites cross-type confusion once kind > 0 exists;
  `created_tick` anchors replay detection, §9). Reserved bytes excluded. (e.g. live-state seals) unforgeable across contexts even
  under key reuse — the exact weakness R4 scored in shipwright's single-byte
  0x5A/0xA5 separation (R4:64–66: "weakest domain scheme among the keyed
  entrants") and stream's none-at-all (R4:67–69).
- The 32-byte tag is stored at the end of the epoch section (§2.3).
  Verification recomputes over the stored bytes with the tag field treated
  as absent (it is, structurally — it is not covered).

## 4. Consumer contract — house-law-independent pseudocode

A consumer that has read ONLY this section (not our runtime docs) must be
able to do both operations. Python-ish pseudocode:

```python
def verify_epoch(section_name_N, section_bytes, archive_key):
    # section_bytes = one `epoch.<N>` payload, exactly as it lies in the file
    if len(section_bytes) < 80:                             E2_TRUNCATED
    if section_bytes[0:4] != b"EPCH":                      E1_BAD_MAGIC
    epoch_no     = u32le(section_bytes, 4)
    status       = section_bytes[8]
    created_tick = u64le(section_bytes, 12)
    payload_kind = u32le(section_bytes, 20)
    payload_len  = u32le(section_bytes, 24)
    primer_addr  = u64le(section_bytes, 32)
    payload      = section_bytes[48 : 48+payload_len]
    tag          = section_bytes[48+payload_len : 48+payload_len+32]
    if epoch_no != section_name_N:                          E4_NAME_MISMATCH
    if payload_kind != 0:                                   E4_BAD_KIND
    if len(payload) != payload_len or \
       len(section_bytes) != 48 + payload_len + 32:         E2_TRUNCATED
    msg = (b"QUF-EPOCH-V1\x00" + u32le_bytes(epoch_no) +
           bytes([status]) + u64le_bytes(created_tick) +
           u32le_bytes(payload_kind) + u64le_bytes(primer_addr) +
           u32le_bytes(payload_len) + payload)
    ok = hmac.compare_digest(hmac_sha256(archive_key, msg), tag)
    return ok if ok else E3_SEAL_MISMATCH

def skip_demoted(section_table, read_at, archive_key):
    # returns the pieces a loading consumer should ingest
    live, nondemoted = [], 0
    for name, kind, off, size in section_table:
        if name.startswith("epoch.") and not name[6:].isascii_digit():
                                                           E4_BAD_NAME
        if name.startswith("epoch.") and kind == 0:
            N = int(name[6:])
            sec = read_at(off, size)
            # ALWAYS verify before honoring status — verify-then-skip, so a
            # flipped demotion bit cannot force silent forgetting (review
            # finding 16: skip-without-verify was an unauthenticated-demotion
            # hole; demotion without custody must never be load-bearing)
            if not verify_epoch(N, sec, archive_key):       E3  # fail closed
            if sec[8] & 0x01:
                continue                      # demoted: verified, now skip
            nondemoted += 1
            if nondemoted > 1:                E6_MULTIPLE_LIVE  # §9 rule
            live.append(restore(sec))                          # §2.3 replay
        else:
            live.append((name, read_at(off, size)))            # v1 sections
    return live
```


Fail-closed rule: **a consumer that cannot obtain the archive key MUST NOT
silently accept a sealed epoch as verified.** It may load it unverified only
if the operator explicitly passes an "unverified-load" flag, and every
restored epoch must then be tagged unverified in consumer output.

### 4.2 Reason codes (normative)

| code | meaning                                  | consumer action   |
|------|------------------------------------------|-------------------|
| E1   | bad epoch magic                          | reject file       |
| E2   | truncated (payload_len vs section size)  | reject file       |
| E3   | seal mismatch / no key and no override   | fail closed       |
| E4   | malformed epoch name / epoch_no≠N / kind≠0 | reject file       |
| E6   | more than one non-demoted epoch            | reject file       |
| E5   | custody violation (§6)                   | fail closed       |

## 5. Fabric OP proposal — the keyed-hash organ (no RTL change yet)

The base fabric's opcode space is 3 bits with BIND=0…NAK=6 defined
(`rtl/q_cell_core.v:125–127`); **encoding 7 is free**. The 5+1 decoder
(five verbs + ACK/NAK; the MHS profile adds FORGET as a controller verb,
`docs/CULTURE-DEEP-DIVE.md:441–443`) leaves slot 7 unclaimed.

Proposal (for a future RTL change, NOT in this draft):

- **`OP_KHASH = 3'd7`** — streaming keyed hash organ.
- Flit operands: `a0` = domain code (0 = mint path, 1 = archive seal,
  2 = archive verify), `a1` = key-slot id (0 = mint key, 1 = archive key;
  slot 1 exists so the R4 "mate-key holder mints archives" attack is a
  wiring non-option), `a2` = byte count; `dat` carries 16-bit words in
  sequence (the existing word-stream shape, base spec §9). Result digest
  returns in the response flit `dat` field over multiple VIEW-style reads,
  or writes to a dial-addressable 16-word digest window.
- Sizing note for reviewers: an iCE40-up soft SHA-256 core is ~1–2 kLE;
  this is why the format (not just the tooling) must be HMAC-SHA256 —
  the cheapest keyed organ everyone can build.

## 6. Custody — the distinct-archive-key MUST (R4 verdict as spec law)

From R4:75–78 (cross-team verdict, item 1): "Uniform G2+ exposure: zero
entrants ship a distinct archive key… The mate-key holder can mint anyone's
archives. Seam-3's ratchet writes itself: distinct archive keys with a
custody ceremony become a hard gate."

Normative requirements (RFC-2119 sense):

1. **MUST**: the archive key used for epoch seals SHALL be generated,
   stored, and ceremony-logged independently of every mint/hot-path key.
   Deriving the archive key from the mint key (even via HMAC domain tag)
   is a **violation**, because it reintroduces the R4 exposure by algebra.
2. **MUST**: writers emit the `custody` section (§2.5) naming the archive
   key id and ceremony tick before the first `epoch.<N>` section in table
   order.
3. **MUST (fail-closed)**: a consumer that finds epoch sections but no
   `custody` section, or a `custody` section naming a key it cannot
   resolve, reports **E5** and refuses to restore sealed epochs (operator
   override per §4, still tagged unverified).
4. **MUST NOT**: two archives from different producers share an archive
   key unless the custody ceremony explicitly federates them (out of
   scope for this draft; the `key_id` field exists so federation is
   auditable later).

## 7. Compatibility and migration

- **v0/v1 readers**: unaffected. Epoch and custody sections are unknown
  *names*; base-spec §8 rule 3 mandates skip-via-table. The four live
  sections, header, and golden vector bytes are untouched (§2.1). Verified
  against the base spec's own extension precedent: new sections do not
  bump `version` (§8 rule 6).
- **Version path**: `version` stays 1. (Policy note, per review: base
  §8 rule 6 reserves bumps for *changed existing* encodings; a future
  epoch-header/seal change would be our own extension changing — the
  bump is therefore this draft's stated policy, not base-spec law.)
  The optional KV key
  `quf.forgetting = u32 1` (this draft) lets aware readers detect support
  without a version bump; unaware readers skip the KV (§8 rule 1). If a
  future revision ever changes the epoch-header layout or seal primitive,
  THAT bumps to version 2 and old readers reject loudly (§8 rule 6) —
  the base spec's versioning rule already covers us; this draft does not
  need to invent a nibble.
- **Migration**: no file in existence needs rewriting — a v1 file with
  zero epochs is already conformant. First demotion under this draft
  writes the first `custody` + `epoch.<N>` sections; loaders predating
  this draft keep working on live state, they merely cannot see archives.

## 8. Provenance — who argued what, and what each got wrong

Failures are first-class. Passes quoted with their actual contributions:

- **Foreman (this agent, GLM-5.3)**: overall structure — per-epoch
  sections with fixed 48-byte headers, seal at fixed end offset, the
  §2.4 rejection of a whole-file seal, `quf.forgetting` KV instead of a
  version bump, opcode slot 7 proposal. **Got wrong (caught by Claude)**:
  the first draft put the seal in a per-epoch KV pair inside the section
  payload — KV framing inside a section is not skippable by v0 section
  rules and forced the header to be parsed before any skip decision.
  Fixed-header-at-fixed-offset + fixed trailer is the corrected shape.
- **Claude (Sonnet, `claude -p` design pass)**: independently arrived at
  per-epoch seal sections as the right granularity ("each epoch owns its
  seal; scales without header bloat") and supplied the canonicalization rule
  now in §2.4: *hash sections on their actual byte boundary, padding is NOT
  hashed* — the exact reasoning behind excluding padding from seal coverage.
  Claude also pre-empted the §7 conclusion with the sharpest form of it:
  "the real argument for version=2 only exists if the digest becomes
  mandatory; ship as v1 extension, bump later if enforcement ever needs it."
  **Got wrong (caught by foreman)**: Claude proposed KV framing *inside*
  section payloads (a `__demoted` bool + digest KV on a `__epoch_seal_<N>`
  section of reserved kind). The base spec defines KV only in the header
  (§4); payload KV would be a parallel mini-format a consumer must
  variable-length-parse *before* it can make the skip decision, and `kind ≠
  0` buys nothing over the sanctioned unknown-name skip (§5, §8 rule 3).
  The fixed 48-byte header (§2.3) is the corrected shape. Claude's
  "length-extension" framing was also imprecise — HMAC-SHA256 is immune to
  length extension by construction; the real property its prefix-struct
  buys is *epoch-bound binding* (no append/truncate/splice), which §3.3
  achieves with the length-prefixed domain message.
- **OpenCode (GLM, `opencode run --auto` review pass)**: 18 numbered
  findings; accepted into the body — (a) two misattributed citations
  (name-length rule is a §9 loader limit not §5; ignore-trailing-bytes
  is §8 rule 5 not §5), (b) the §2.4-vs-§3.3 prose contradiction (§2.4
  fixed), (c) unsealed `created_tick`/`payload_kind` (now in the HMAC
  message, §3.3), (d) the missing epoch_no/N cross-check (now E4),
  (e) pseudocode robustness (ASCII digits, exact-size E2, kind check),
  (f) the **verify-then-skip hole** — its best catch: demoted epochs were
  skipped without verification, making the demotion bit itself an
  unauthenticated forget-forcing primitive (§4 now verifies before
  honoring status), (g) honest naming of the unmitigated gaps now in §9
  (no chain/anti-rollback, key rotation, custody-section authentication,
  single-live-epoch E6). **Got wrong (caught by foreman)**: finding 3
  overread §2.3 as claiming whole-file loader replay — the original text
  said "same loader paths", which meant the write paths, though the
  wording did invite the misreading and is now explicit; and finding 12's
  caveat ("section-level skip only presumed for `q_uf_loader.v`\") was
  already answered by base spec §9's own bullet "walks the section
  table, then streams the payloads" — table walking implies offset-based
  skipping, but the clarification is kept in §7.
- **DeepInfra MCP**: not reachable in this session (no MCP tooling wired
  into the subagent environment); noted honestly rather than fabricated.
  The wider-model view was instead covered by the two independent passes
  above (Sonnet + GLM small-model).

### 8.1 Claude addendum (quoted)

> "Per-epoch section: each epoch owns its seal. Clients verify just that
> section independently. Scales cleanly… v0 skips unknown names safely."
>
> "Hash sections on their actual byte boundary; padding is NOT hashed.
> This lets you re-pad without invalidating the seal."
>
> "Ship as v1 extension. If you later need to mandate digests, bump to
> v2 then — but don't do it preemptively."

Not adopted: payload-KV framing and reserved-kind sections (see §8, Claude
  miss, corrected shape §2.3); whole-table hash coverage (rejected with
  §2.4 — the consumer-independence test wants per-epoch verifiability,
  and re-hashing the table on every epoch verify couples an epoch's
  validity to unrelated sections' offsets).

### 8.2 OpenCode addendum (quoted, abridged)

> "§3.3 HMAC message omits two defined header fields: created_tick and
> payload_kind are defined but unsealed — tamperable without detection."
> "skip_demoted reads status and continues on bit0 without verifying —
> the demoted path never checks the seal, so an attacker flipping the
> bit forces silent forgetting of a live epoch. Verify-then-skip needed."
> "The seal proves authenticity, not currency — no monotonic chain…
> replaying a stale validly-sealed non-demoted epoch is a verified
> rollback."

All three folded in: (1) → §3.3 message, (2) → §4 verify-then-skip,
(3) → §9 known-limitation, honestly unmitigated.

## 9. What this draft deliberately does NOT claim

- No RTL exists for OP_KHASH; slot 7 is a proposal (§5).
- No delta/compressed epoch payloads (payload_kind reserves the space).
- No federation protocol for shared archive keys (§6 item 4).
- **No seal chain / anti-rollback**: the seal proves authenticity, not
  currency (no prev-digest link, no file nonce in the domain string) —
  a stale validly-sealed non-demoted epoch is a *verified* rollback, and
  cross-file epoch splicing verifies. `created_tick` is sealed so audit
  tooling can detect staleness, but the format does not enforce it.
- **No key rotation**: `custody` holds one key id; rotation semantics
  (overlap windows, re-sealing) are left to the ceremony layer, and the
  `custody` section itself is unauthenticated (authenticated custody is
  a v2 candidate).
- **At most one non-demoted epoch per file** is enforced (E6); restored
  live state carries no seal (§2.4) — post-restore tampering of live
  sections is out of seal scope by design.
- Re-derivation of forgotten content remains unattempted and unclaimed —
  re-derivation-zero held across all six R4 teams (R4:79–80) and this
  draft does not challenge it.
