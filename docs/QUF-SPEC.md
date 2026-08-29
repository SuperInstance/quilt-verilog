# QUF — QUilt Format, v1

**QUF is the GGUF of cellular silicon.** llama.cpp won because weights are
just a file; QUF is the same bet for the fabric: a flat, binary,
little-endian container that holds the complete state of a quilt — dials,
edges (with Hebbian walk counts), routing, and the tick schedule. One file
loads into simulation (testbench), a soft core, or a real FPGA, identically
(DOCTRINE item 3). Where GGUF carries *tensors*, QUF carries *cell state*.

| GGUF notion            | QUF counterpart                                  |
|------------------------|--------------------------------------------------|
| magic `GGUF`           | magic `'Q','U','F',0x00` (bytes `51 55 46 00`)   |
| little-endian scalars  | same                                             |
| header KV metadata     | same encoding, GGUF value-type numbering         |
| aligned tensor sections| aligned state sections: dials/edges/routing/ticks|
| `general.*` keys       | `quf.version`, `quant.*` keys                    |
| unknown KV → skip      | same rule                                        |

Reference implementation: `tools/quf.py` (stdlib only).
Synthesizable consumer: `rtl/q_uf_loader.v` (§9, loader profile).

## 1. Conformance

- **Full spec** — `tools/quf.py`: parses and emits everything below,
  verifies structure, restores all state including edge walk counts.
- **RTL loader profile** — `rtl/q_uf_loader.v`: streaming parse of the
  subset a v1 cell needs (§9). Unknown metadata is *skipped*, never
  fatal — the extensibility rule is load-bearing.

## 2. File map

```
+-----------------------------+  offset 0
| magic          4 bytes      |  'Q','U','F',0x00
| version        u32          |  = 1
| endian         u32          |  = 1 (little); big-endian QUF is undefined
| kv_count       u32          |  number of header KV pairs
+-----------------------------+
| kv_count × KV pair          |  §4
+-----------------------------+
| section_count  u32          |
| section_count × entry       |  §5 (name, kind, offset u64, size u64)
+-----------------------------+  end of table
| zero padding to `align`     |
| section payloads            |  §6, at the offsets named in the table
| zero padding between/after  |  file padded to `align` at EOF
+-----------------------------+
```

All multi-byte integers are **little-endian**. Offsets are absolute from
byte 0 of the file.

## 3. Fixed header (16 bytes)

| field     | size | value                                            |
|-----------|------|--------------------------------------------------|
| magic     | 4    | `51 55 46 00`                                    |
| version   | u32  | 1 (this document)                                |
| endian    | u32  | 1 = little-endian. No other value is defined.    |
| kv_count  | u32  | number of KV pairs that follow                   |

## 4. Header KV metadata

Each pair:

```
u32 name_len, name_len × UTF-8 bytes, u32 value_type, value bytes
```

Value types use **GGUF's numbering** so tooling intuition transfers:

| id | type   | size                  |
|----|--------|-----------------------|
| 0  | u8     | 1                     |
| 1  | i8     | 1                     |
| 2  | u16    | 2                     |
| 3  | i16    | 2                     |
| 4  | u32    | 4                     |
| 5  | i32    | 4                     |
| 6  | f32    | 4                     |
| 7  | bool   | 1                     |
| 8  | string | u32 len + len bytes   |
| 9  | array  | u32 elem_type, u32 count, count × elements |
| 10 | u64    | 8                     |
| 11 | i64    | 8                     |
| 12 | f64    | 8                     |

Array element types must be fixed-size (no nested strings/arrays).

**Standard keys** (writers emit them in this order; `*` = required when
the related section is present):

| key             | type   | meaning                                        |
|-----------------|--------|------------------------------------------------|
| `quf.version`   | string | producer identification                        |
| `cell_count`*   | u32    | number of cells the file describes             |
| `edge_count`    | u32    | number of edge records (= rows in `edges`)     |
| `route_count`   | u32    | number of routing records                      |
| `edge.k`        | u32    | ladder buckets per edge record, 1..16, default 8 |
| `tick_period`   | u32    | ticks per scheduler period (2^tpw), semantic  |
| `quant.dials`   | string | Q-format of dial words, e.g. `Q1.15`           |
| `quant.edges`   | string | Q-format of edge base weights                  |
| `quant.routing` | string | numeric format of routing fields               |
| `align`         | u32    | section alignment, power of two ≥ 8, default 32|

The reference writer derives `cell_count`/`edge_count`/`route_count` from
the payloads when omitted, and computes `tick_period` from the ticks
section. f32/f64 exist in the type space for numbering compatibility; the
reference writer **refuses to emit them** (doctrine: quantized-by-default,
no floats in fleet state).

## 5. Section table

`u32 section_count`, then per section:

```
u32 name_len, name_len × UTF-8 name, u32 kind, u64 offset, u64 size
```

Rules:

- `kind = 0` is the standard raw-bytes kind; other kinds are skipped by
  readers that do not understand them.
- `offset` is absolute from file start and **must be a multiple of
  `align`**.
- Table entries must be **strictly ascending by offset**, and sections
  must **not overlap** and must **not extend past end of file**. Padding
  between the table and the first section, between sections, and after
  the last section is zero bytes.
- Duplicate section names are a verification failure.
- Unknown section names: skip via the table (extensibility rule).
- The reference writer pads the whole file to `align`, so the byte stream
  is always an integral number of 16-bit words (what the RTL loader eats).

## 6. Sections (v1)

### 6.1 `dials` — per-cell dial register file image

Flat image of the `q_dialfile`: `cell_count` rows × 16 `u16` words
(row = one cell, word = one dial, index = dial address 0..15), row-major,
little-endian. Size = `cell_count × 32` bytes. Interpretation is
saturating fixed-point, format declared by `quant.dials` (default
`Q1.15`). Values are stored **pre-saturated**; loaders never clip on the
way in. The dial map itself is defined by `q_dialfile.v` (ETA_F, ETA_S,
KF, KS, KA, THRESH, REFR, COS_MIN, P0E, MODE, HL at addresses 0..10;
11..15 reserved, still round-tripped).

### 6.2 `edges` — Hebbian edge table

`edge_count` records, each `12 + edge.k` bytes, little-endian:

| off | size | field    | notes                                    |
|-----|------|----------|------------------------------------------|
| 0   | 1    | src      | owning cell id                           |
| 1   | 1    | dst      | peer cell id                             |
| 2   | 1    | mode     | 0 = ladder, 1 = hyperbolic               |
| 3   | 1    | slot     | edge slot index within src cell          |
| 4   | 2    | base     | u16 bind-time base weight, `quant.edges` |
| 6   | 2    | wh       | u16 hyperbolic integer weight            |
| 8   | 4    | age      | u32 hyperbolic age counter (ticks)       |
| 12  | K    | buckets  | u8 × K ladder walk counts; bucket 0 = newest class |

`K = edge.k`. Size = `edge_count × (12 + K)`. Both decay engines' state
travels in every record; the active one is selected by `mode`.

### 6.3 `routing` — topology portability

`route_count` records of 2 bytes: `u8 dst, u8 via` (destination cell,
next hop toward it). For the v1 single ring `via == dst`; the section
exists so multi-ring / mesh fabrics stay file-compatible. Size =
`route_count × 2`.

### 6.4 `ticks` — tick schedule

`u32 tpw` followed by `cell_count` × `u32 phase` (per-cell phase offset
in clock cycles; v1 single-clock fabric ignores phases, they are carried
for v2 metronome cells). Size = `4 + 4 × cell_count`. `tick_period` in
the header is the semantic period `2^tpw`.

## 7. Alignment and endianness

- Little-endian everywhere; the header `endian` word exists so a
  big-endian host can detect and refuse, not to define a second encoding.
- `align` (default 32) applies to **section offsets** and to the whole
  file length. The fixed header and KV region are never moved.

## 8. Extensibility and versioning

1. **Unknown KV keys: skip.** A reader must not fail on metadata it does
   not know (skipping is safe because every value's size is derivable
   from its type).
2. **Unknown value types: reject.** An undefined type id makes the value
   un-skippable; readers must fail loudly, not guess.
3. **Unknown section names: skip** via the section table.
4. **Unknown section kinds: skip** the payload.
5. Bytes after the last section (within the final padding) are ignored.
6. New sections and new KV keys may be added without bumping `version`.
   Changing the meaning or encoding of an existing section/KV, or the
   fixed header, bumps `version` — readers reject other versions.

## 9. RTL loader profile (`rtl/q_uf_loader.v`)

The synthesizable consumer. What it does:

- Eats the QUF as a **word stream** on the `q_io_port` external-ingress
  handshake shape (`i_val/o_rdy/i_dat[15:0]`); bytes arrive little-endian,
  low byte of each word first.
- Parses the fixed header, **skips** every KV pair it does not need, and
  captures `edge.k` (must be u32; known key with wrong type = error).
- Walks the section table, then streams the payloads:
  - `dials`: writes the row of cell `i_mycell` into the `q_dialfile`
    write port, word for word, byte-exact.
  - `edges`: writes records with `src == i_mycell` into the edge RAM as
    32-bit words `{base[15:0], dst[7:0], mode[7:0]}` addressed by `slot`.
  - `routing`: writes `{dst, via}` nibbles into the route RAM.
  - `ticks`: captures `tpw` (bits [4:0] → the `q_tick_sched` parameter).
- Asserts `o_done` after the last byte of the last known section.

v1 profile limits, on purpose: edge walk state (`wh`, `age`, `buckets`)
is *consumed but not restored* — the v1 `q_hebb_edge` engines have no
load port; a warm-started fabric re-binds topology + dials and trains the
ladders back (full state restore is the Python path). Files must be
< 4 GiB (u64 high words must be zero), names ≤ 255 bytes, `edge.k` in
1..16.

Error codes (`o_err`, sticky, stops the load):

| code | meaning                                        |
|------|------------------------------------------------|
| 1    | bad magic                                      |
| 2    | bad version                                    |
| 3    | layout overrun (pos passed a section offset)   |
| 4    | bad endian word (≠ 1)                          |
| 5    | known KV (`edge.k`) not u32                    |
| 6    | unknown value type / bad array element type    |
| 7    | nonzero u64 high word (offset or size)         |
| 8    | KV/section name longer than 255 bytes          |
| 9    | `edge.k` out of 1..16                          |

## 10. JSON schema and CLI (`tools/quf.py`)

Input to `create` is the golden shape:

```json
{
  "header":  { "quf.version": "...", "cell_count": 2, "edge_count": 3,
               "route_count": 3, "edge.k": 8, "tick_period": 64,
               "quant.dials": "Q1.15", "quant.edges": "Q1.15",
               "quant.routing": "u8", "align": 32 },
  "dials":   [ [16 × u16], ... per cell ],
  "edges":   [ {"src":0,"dst":1,"mode":0,"slot":0,"base":4660,
                "wh":0,"age":0,"buckets":[0,0,0,0,0,0,0,0]}, ... ],
  "routing": [ {"dst":1,"via":1}, ... ],
  "ticksched": { "tpw": 6, "phases": [0, 3] }
}
```

Commands: `create IN.json OUT.quf` (also writes `OUT.hex`, a
byte-per-line hex image for `$fscanf` testbenches), `info`, `dump`,
`verify`, `hex`, `selftest`.

## 11. Golden test vector

The canonical byte-exact vector (embedded in `tools/quf.py`, asserted by
`selftest`, loaded by `tb/quf_tb.v` via `tb/quf_tb.json`): 2 cells,
3 edges, 3 routes, ticks tpw=6. 576 bytes, sha256
`5b2a236ba5e38bca9ad96783c4252a12f36517f98a9164a249f0db115f221392`.

Layout walk: fixed header 16 B → 10 KV pairs 241 B → section table
(4 + 29+29+31+29 =) 122 B → 379 → pad 5 B to 384 → `dials` @384 (64 B) →
`edges` @448 (60 B) → `routing` @512 (6 B) → `ticks` @544 (12 B) → pad to 576.

```
51554600 01000000 01000000 0a000000                        ; magic, v1, LE, 10 KVs
0b000000 7175662e76657273696f6e 08000000 0a000000 7175662e707920312e30
0a000000 63656c6c5f636f756e74     04000000 02000000
0a000000 656467655f636f756e74     04000000 03000000
0b000000 726f7574655f636f756e74   04000000 03000000
06000000 656467652e6b             04000000 08000000
0b000000 7469636b5f706572696f64   04000000 40000000
0b000000 7175616e742e6469616c73   08000000 05000000 51312e3135
0b000000 7175616e742e6564676573   08000000 05000000 51312e3135
0d000000 7175616e742e726f7574696e67 08000000 02000000 7538
05000000 616c69676e               04000000 20000000
04000000                                                       ; 4 sections
05000000 6469616c73 00000000 80010000 00000000 40000000 00000000   ; @384, 64 B
05000000 6564676573 00000000 c0010000 00000000 3c000000 00000000   ; @448, 60 B
07000000 726f7574696e67 00000000 00020000 00000000 06000000 00000000 ; @512, 6 B
05000000 7469636b73 00000000 20020000 00000000 0c000000 00000000   ; @544, 12 B
... 256 B zero padding to offset 384 ...
; dials row 0 (cell 0): 0800 0080 0006 000c 0005 5000 0004 2ccd
;                        0014 0000 0030 0000 0000 0000 0000 0000
; dials row 1 (cell 1): 0800 0080 0006 000c 0005 6000 0004 2ccd
;                        0014 0001 0040 0000 0000 0000 0000 0000
; edges: 00 01 00 00 3412 0000 00000000 0000000000000000   ; src0→dst1 base 0x1234
;        00 02 01 01 4000 0700 e8030000 00...00              ; src0→dst2 mode1 wh7 age1000
;        01 00 00 00 0002 0300 05000000 00...00              ; src1→dst0 (other cell)
; routing: 01 01 02 02 0f 0f
; ticks: 06000000 00000000 03000000
; trailing zero padding to 576
```

Full hex (whitespace-insensitive):

```
5155460001000000010000000a0000000b0000007175662e76657273696f6e080000000a0000007175662e707920312e300a00000063656c6c5f636f756e7404000000020000000a000000656467655f636f756e7404000000030000000b000000726f7574655f636f756e74040000000300000006000000656467652e6b04000000080000000b0000007469636b5f706572696f6404000000400000000b0000007175616e742e6469616c73080000000500000051312e31350b0000007175616e742e6564676573080000000500000051312e31350d0000007175616e742e726f7574696e670800000002000000753805000000616c69676e040000002000000004000000050000006469616c73000000008001000000000000400000000000000005000000656467657300000000c0010000000000003c0000000000000007000000726f7574696e670000000000020000000000000600000000000000050000007469636b730000000020020000000000000c0000000000000000000000000008800006000c00050000500400cd2c140000003000000000000000000000000008800006000c00050000600400cd2c1400010040000000000000000000000000010000341200000000000000000000000000000002010140000700e80300000000000000000000010000000002030005000000000000000000000000000000010102020f0f00000000000000000000000000000000000000000000000000000600000000000000030000000000000000000000000000000000000000000000
```
