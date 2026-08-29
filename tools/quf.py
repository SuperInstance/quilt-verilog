#!/usr/bin/env python3
"""quf.py -- QUF (QUilt Format) reference implementation.

Doctrine item 3: state is a file. QUF is the GGUF of cellular silicon: a
flat, little-endian binary container for cell state (dials, edges with
Hebbian walk counts, routing, tick schedule). See docs/QUF-SPEC.md.

Stdlib only. Python >= 3.8.

Commands:
  create IN.json OUT.quf   build a QUF from JSON (also writes OUT.hex)
  info  FILE.quf           header + section table summary
  dump  FILE.quf           full decode of known sections
  verify FILE.quf          structural verification, exit 0 if clean
  hex   FILE.quf OUT.hex   byte-per-line hex for $fscanf testbenches
  selftest                 byte-exact golden vector + round-trip checks
"""

import argparse
import hashlib
import json
import os
import struct
import sys

MAGIC = b"QUF\x00"
VERSION = 1
ENDIAN_LITTLE = 1

# GGUF-compatible value-type numbering (doctrine: tooling intuition transfers).
T_U8, T_I8, T_U16, T_I16, T_U32, T_I32, T_F32, T_BOOL, T_STR, T_ARR, \
    T_U64, T_I64, T_F64 = range(13)

TYPE_NAMES = {
    T_U8: "u8", T_I8: "i8", T_U16: "u16", T_I16: "i16", T_U32: "u32",
    T_I32: "i32", T_F32: "f32", T_BOOL: "bool", T_STR: "string",
    T_ARR: "array", T_U64: "u64", T_I64: "i64", T_F64: "f64",
}
STRUCT_FMT = {
    T_U8: "<B", T_I8: "<b", T_U16: "<H", T_I16: "<h", T_U32: "<I",
    T_I32: "<i", T_F32: "<f", T_BOOL: "<?", T_U64: "<Q", T_I64: "<q",
    T_F64: "<d",
}
FIXED_SIZE = {
    T_U8: 1, T_I8: 1, T_U16: 2, T_I16: 2, T_U32: 4, T_I32: 4, T_F32: 4,
    T_BOOL: 1, T_U64: 8, T_I64: 8, T_F64: 8,
}

# Canonical header KV order for the reference writer.
CANON_KV = [
    "quf.version", "cell_count", "edge_count", "route_count", "edge.k",
    "tick_period", "quant.dials", "quant.edges", "quant.routing", "align",
]
STRING_KV = {"quf.version", "quant.dials", "quant.edges", "quant.routing"}
# Canonical section order.
SECTION_ORDER = ["dials", "edges", "routing", "ticks"]

DEFAULT_EDGE_K = 8
DEFAULT_ALIGN = 32
NDIALS = 16          # dials per cell (q_dialfile ND)


class QufError(Exception):
    pass


def u32(x):
    return struct.pack("<I", x)


# ---------------------------------------------------------------- values --

def pack_value(vt, v):
    if vt == T_STR:
        b = v.encode("utf-8")
        return u32(len(b)) + b
    if vt == T_ARR:
        if not isinstance(v, tuple) or len(v) != 2:
            raise QufError("array value must be (elem_type, list)")
        et, evs = v
        if et not in FIXED_SIZE:
            raise QufError("array element type must be fixed-size")
        out = u32(et) + u32(len(evs))
        for e in evs:
            out += pack_value(et, e)
        return out
    try:
        return struct.pack(STRUCT_FMT[vt], v)
    except (KeyError, struct.error) as ex:
        raise QufError("bad value for type %s: %s" % (TYPE_NAMES.get(vt), ex))


def unpack_value(buf, off, vt):
    def take(n):
        nonlocal off
        if off + n > len(buf):
            raise QufError("truncated value at %d" % off)
        b = buf[off:off + n]
        off += n
        return b

    if vt == T_STR:
        (n,) = struct.unpack("<I", take(4))
        return take(n).decode("utf-8"), off
    if vt == T_ARR:
        (et,) = struct.unpack("<I", take(4))
        (n,) = struct.unpack("<I", take(4))
        if et not in FIXED_SIZE:
            raise QufError("unknown array element type %d" % et)
        vals = []
        for _ in range(n):
            v, off = unpack_value(buf, off, et)
            vals.append(v)
        return vals, off
    if vt not in STRUCT_FMT:
        raise QufError("unknown value type %d (cannot skip safely)" % vt)
    sz = FIXED_SIZE[vt]
    (v,) = struct.unpack(STRUCT_FMT[vt], take(sz))
    return v, off


# ------------------------------------------------------------------ build --

def _coerce_header_kv(k, v):
    """Type-check one header KV for the writer. No floats in fleet state."""
    if k in STRING_KV:
        if not isinstance(v, str):
            raise QufError("header %s must be a string" % k)
        return T_STR, v
    if isinstance(v, bool) or not isinstance(v, int):
        raise QufError("header %s must be an integer (u32)" % k)
    if not (0 <= v < 2 ** 32):
        raise QufError("header %s out of u32 range" % k)
    return T_U32, v


def _infer_extra(v):
    if isinstance(v, bool):
        return T_BOOL, v
    if isinstance(v, int):
        if not (0 <= v < 2 ** 32):
            raise QufError("extra header value out of u32 range "
                           "(u64 via tools not supported by writer)")
        return T_U32, v
    if isinstance(v, str):
        return T_STR, v
    if isinstance(v, list):
        for e in v:
            if isinstance(v, bool) or not isinstance(v, int):
                raise QufError("extra header arrays must be u32 arrays")
        return T_ARR, (T_U32, list(v))
    raise QufError("unsupported extra header type %s "
                   "(doctrine: no floats in fleet state)" % type(v).__name__)


def _pack_dials(dials, cell_count):
    if len(dials) != cell_count:
        raise QufError("dials must have cell_count rows (%d != %d)"
                       % (len(dials), cell_count))
    out = bytearray()
    for row in dials:
        if len(row) != NDIALS:
            raise QufError("each dials row must have %d entries" % NDIALS)
        for v in row:
            if not (0 <= v < 2 ** 16):
                raise QufError("dial value out of u16 range: %r" % v)
            out += struct.pack("<H", v)
    return bytes(out)


def _pack_edges(edges, k):
    out = bytearray()
    for e in edges:
        src, dst = int(e["src"]), int(e["dst"])
        mode, slot = int(e["mode"]), int(e["slot"])
        base, wh = int(e["base"]), int(e["wh"])
        age = int(e["age"])
        for name, v in (("src", src), ("dst", dst), ("mode", mode),
                        ("slot", slot)):
            if not (0 <= v < 2 ** 8):
                raise QufError("edge %s out of u8 range" % name)
        for name, v in (("base", base), ("wh", wh)):
            if not (0 <= v < 2 ** 16):
                raise QufError("edge %s out of u16 range" % name)
        if not (0 <= age < 2 ** 32):
            raise QufError("edge age out of u32 range")
        buckets = list(e.get("buckets", []))[:k]
        buckets += [0] * (k - len(buckets))
        for b in buckets:
            if not (0 <= b < 2 ** 8):
                raise QufError("edge bucket out of u8 range")
        out += struct.pack("<BBBBHHI", src, dst, mode, slot, base, wh, age)
        out += bytes(buckets)
    return bytes(out)


def _pack_routing(routing):
    out = bytearray()
    for r in routing:
        dst, via = int(r["dst"]), int(r["via"])
        for name, v in (("dst", dst), ("via", via)):
            if not (0 <= v < 2 ** 8):
                raise QufError("route %s out of u8 range" % name)
        out += struct.pack("<BB", dst, via)
    return bytes(out)


def _pack_ticks(ticks, cell_count):
    tpw = int(ticks["tpw"])
    if not (0 <= tpw < 2 ** 32):
        raise QufError("tpw out of u32 range")
    phases = list(ticks.get("phases", []))[:cell_count]
    phases += [0] * (cell_count - len(phases))
    out = struct.pack("<I", tpw)
    for p in phases:
        out += struct.pack("<I", p)
    return out


def build(doc):
    """Build canonical QUF bytes from a JSON-shaped dict."""
    hdr = dict(doc.get("header", {}))
    dials = doc.get("dials")
    edges = doc.get("edges", [])
    routing = doc.get("routing", [])
    ticks = doc.get("ticksched")

    if "cell_count" not in hdr:
        if dials is None:
            raise QufError("cell_count required when no dials section")
        hdr["cell_count"] = len(dials)
    cell_count = hdr["cell_count"]
    hdr.setdefault("edge_count", len(edges))
    hdr.setdefault("route_count", len(routing))
    k = hdr.setdefault("edge.k", DEFAULT_EDGE_K)
    if not (1 <= k <= 16):
        raise QufError("edge.k must be 1..16")
    if ticks is not None and "tick_period" not in hdr:
        hdr["tick_period"] = 2 ** int(ticks["tpw"])

    align = hdr.setdefault("align", DEFAULT_ALIGN)
    if align < 8 or (align & (align - 1)) != 0:
        raise QufError("align must be a power of two >= 8")

    # -- KV pairs in canonical order, then sorted extras
    kvs = []
    for key in CANON_KV:
        if key in hdr:
            vt, v = _coerce_header_kv(key, hdr[key])
            kvs.append((key, vt, v))
    for key in sorted(set(hdr) - set(CANON_KV)):
        vt, v = _infer_extra(hdr[key])
        kvs.append((key, vt, v))

    kv_bytes = bytearray()
    for key, vt, v in kvs:
        kb = key.encode("utf-8")
        kv_bytes += u32(len(kb)) + kb + u32(vt) + pack_value(vt, v)

    # -- section payloads in canonical order
    secs = []
    if dials is not None:
        secs.append(("dials", _pack_dials(dials, cell_count)))
    if edges:
        secs.append(("edges", _pack_edges(edges, k)))
    if routing:
        secs.append(("routing", _pack_routing(routing)))
    if ticks is not None:
        secs.append(("ticks", _pack_ticks(ticks, cell_count)))

    table_len = 4 + sum(4 + len(n.encode("utf-8")) + 20 for n, _ in secs)
    base = 16 + len(kv_bytes) + table_len

    # place sections at ascending, `align`-ed offsets after the table
    entries = bytearray()
    body = bytearray()
    off = (base + align - 1) // align * align
    for name, payload in secs:
        entries += table_chunk(name, off, len(payload))
        body += b"\x00" * (off - (base + len(body)))
        body += payload
        off = (base + len(body) + align - 1) // align * align

    out = bytearray()
    out += MAGIC
    out += struct.pack("<III", VERSION, ENDIAN_LITTLE, len(kvs))
    out += kv_bytes
    out += u32(len(secs))
    out += entries
    out += body
    # pad whole file to align (keeps the byte stream an integral word count)
    if len(out) % align:
        out += b"\x00" * (align - (len(out) % align))
    return bytes(out)


def table_chunk(name, off, size):
    nb = name.encode("utf-8")
    return u32(len(nb)) + nb + u32(0) + struct.pack("<QQ", off, size)


# ------------------------------------------------------------------- read --

def read(buf, path=""):
    where = path or "buffer"

    def need(n, off):
        if off + n > len(buf):
            raise QufError("%s: truncated (need %d bytes at %d)"
                           % (where, n, off))

    need(16, 0)
    if buf[:4] != MAGIC:
        raise QufError("%s: bad magic %r" % (where, buf[:4]))
    version, endian, nkv = struct.unpack_from("<III", buf, 4)
    if version != VERSION:
        raise QufError("%s: unsupported version %d" % (where, version))
    if endian != ENDIAN_LITTLE:
        raise QufError("%s: only little-endian QUF is defined (got %d)"
                       % (where, endian))

    off = 16
    kvs = []
    for _ in range(nkv):
        need(4, off)
        (nl,) = struct.unpack_from("<I", buf, off)
        off += 4
        need(nl, off)
        key = buf[off:off + nl].decode("utf-8")
        off += nl
        need(4, off)
        (vt,) = struct.unpack_from("<I", buf, off)
        off += 4
        v, off = unpack_value(buf, off, vt)
        kvs.append((key, vt, v))

    need(4, off)
    (nsec,) = struct.unpack_from("<I", buf, off)
    off += 4
    table = []
    for _ in range(nsec):
        need(4, off)
        (nl,) = struct.unpack_from("<I", buf, off)
        off += 4
        need(nl, off)
        name = buf[off:off + nl].decode("utf-8")
        off += nl
        need(20, off)
        kind, soff, ssize = struct.unpack_from("<IQQ", buf, off)
        off += 20
        table.append((name, kind, soff, ssize))

    sections = []
    for name, kind, soff, ssize in table:
        need(ssize, soff)
        sections.append((name, kind, bytes(buf[soff:soff + ssize])))

    return {
        "version": version,
        "kv": kvs,
        "table": table,
        "sections": sections,
        "header": {k: v for k, _, v in kvs},
        "payload": {name: data for name, _, data in sections},
    }


def rebuild(parsed):
    """Re-emit canonical bytes from a parsed container (order preserved)."""
    kv_bytes = bytearray()
    for key, vt, v in parsed["kv"]:
        kb = key.encode("utf-8")
        kv_bytes += u32(len(kb)) + kb + u32(vt) + pack_value(vt, v)
    hdr = {k: v for k, _, v in parsed["kv"]}
    align = int(hdr.get("align", DEFAULT_ALIGN))
    secs = [(name, data) for name, _, data in parsed["sections"]]

    table_len = 4 + sum(4 + len(n.encode()) + 20 for n, _ in secs)
    base = 16 + len(kv_bytes) + table_len
    out = bytearray()
    out += MAGIC
    out += struct.pack("<III", VERSION, ENDIAN_LITTLE, len(parsed["kv"]))
    out += kv_bytes
    out += u32(len(secs))
    entries = bytearray()
    body = bytearray()
    off = (base + align - 1) // align * align
    for name, payload in secs:
        entries += table_chunk(name, off, len(payload))
        body += b"\x00" * (off - (base + len(body)))
        body += payload
        off = (base + len(body) + align - 1) // align * align
    out += entries
    out += body
    if len(out) % align:
        out += b"\x00" * (align - (len(out) % align))
    return bytes(out)


# ----------------------------------------------------------------- verify --

def verify_bytes(buf, path=""):
    issues = []
    try:
        parsed = read(buf, path)
    except QufError as e:
        return [str(e)]

    hdr = parsed["header"]
    align = int(hdr.get("align", DEFAULT_ALIGN))
    if align < 8 or (align & (align - 1)) != 0:
        issues.append("align %d is not a power of two >= 8" % align)
        align = max(8, align)

    table_end = 16 + sum(
        4 + len(k.encode()) + 4 + pack_value(vt, v).__len__()
        for k, vt, v in parsed["kv"]) + 4 + sum(
        4 + len(n.encode()) + 20 for n, _, _, _ in parsed["table"])

    prev_end = table_end
    for name, kind, soff, ssize in parsed["table"]:
        if kind != 0:
            issues.append("section %r has non-standard kind %d" % (name, kind))
        if soff % align != 0:
            issues.append("section %r offset %d not %d-aligned"
                          % (name, soff, align))
        if soff < prev_end:
            issues.append("section %r at %d overlaps/precedes previous "
                          "data ending at %d" % (name, soff, prev_end))
        if soff + ssize > len(buf):
            issues.append("section %r extends past EOF (%d > %d)"
                          % (name, soff + ssize, len(buf)))
        prev_end = max(prev_end, soff + ssize)

    payload = parsed["payload"]
    cc = hdr.get("cell_count")
    ec = hdr.get("edge_count")
    rc = hdr.get("route_count")
    k = hdr.get("edge.k", DEFAULT_EDGE_K)
    if "dials" in payload and cc is not None:
        if len(payload["dials"]) != cc * NDIALS * 2:
            issues.append("dials size %d != cell_count*%d*2"
                          % (len(payload["dials"]), cc))
    if "edges" in payload and ec is not None:
        if len(payload["edges"]) != ec * (12 + k):
            issues.append("edges size %d != edge_count*(12+edge.k)=%d"
                          % (len(payload["edges"]), ec * (12 + k)))
    if "routing" in payload and rc is not None:
        if len(payload["routing"]) != rc * 2:
            issues.append("routing size %d != route_count*2"
                          % (len(payload["routing"]), rc))
    if "ticks" in payload and cc is not None:
        if len(payload["ticks"]) != 4 + 4 * cc:
            issues.append("ticks size %d != 4+4*cell_count"
                          % len(payload["ticks"]))
    if ("dials" in payload or "ticks" in payload) and cc is None:
        issues.append("cell_count KV required when dials/ticks present")
    return issues


# ------------------------------------------------------------------- dump --

def decode_sections(parsed):
    hdr = parsed["header"]
    out = {}
    p = parsed["payload"]
    cc = hdr.get("cell_count", 0)
    k = hdr.get("edge.k", DEFAULT_EDGE_K)
    if "dials" in p:
        rows = []
        for c in range(cc):
            rows.append(list(struct.unpack_from("<%dH" % NDIALS, p["dials"],
                                                c * NDIALS * 2)))
        out["dials"] = rows
    if "edges" in p:
        edges = []
        for i in range(len(p["edges"]) // (12 + k)):
            src, dst, mode, slot, base, wh, age = struct.unpack_from(
                "<BBBBHHI", p["edges"], i * (12 + k))
            buckets = list(p["edges"][i * (12 + k) + 12:
                                     i * (12 + k) + 12 + k])
            edges.append(dict(src=src, dst=dst, mode=mode, slot=slot,
                              base=base, wh=wh, age=age, buckets=buckets))
        out["edges"] = edges
    if "routing" in p:
        out["routing"] = [dict(dst=d, via=v) for d, v in
                          struct.iter_unpack("<BB", p["routing"])]
    if "ticks" in p:
        tpw = struct.unpack_from("<I", p["ticks"], 0)[0]
        phases = list(struct.unpack_from("<%dI" % cc, p["ticks"], 4)) \
            if cc else []
        out["ticksched"] = dict(tpw=tpw, phases=phases)
    return out


def to_hexfile(data):
    lines = ["%04X" % len(data)] + ["%02X" % b for b in data]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------- selftest --

GOLDEN = {
    "header": {
        "quf.version": "quf.py 1.0",
        "cell_count": 2,
        "edge_count": 3,
        "route_count": 3,
        "edge.k": 8,
        "tick_period": 64,
        "quant.dials": "Q1.15",
        "quant.edges": "Q1.15",
        "quant.routing": "u8",
        "align": 32,
    },
    "dials": [
        [0x0800, 0x0080, 6, 12, 5, 0x5000, 4, 0x2CCD, 20, 0, 48,
         0, 0, 0, 0, 0],
        [0x0800, 0x0080, 6, 12, 5, 0x6000, 4, 0x2CCD, 20, 1, 64,
         0, 0, 0, 0, 0],
    ],
    "edges": [
        {"src": 0, "dst": 1, "mode": 0, "slot": 0, "base": 0x1234,
         "wh": 0, "age": 0, "buckets": [0] * 8},
        {"src": 0, "dst": 2, "mode": 1, "slot": 1, "base": 0x0040,
         "wh": 7, "age": 1000, "buckets": [0] * 8},
        {"src": 1, "dst": 0, "mode": 0, "slot": 0, "base": 0x0200,
         "wh": 3, "age": 5, "buckets": [0] * 8},
    ],
    "routing": [
        {"dst": 1, "via": 1},
        {"dst": 2, "via": 2},
        {"dst": 15, "via": 15},
    ],
    "ticksched": {"tpw": 6, "phases": [0, 3]},
}

# Byte-exact golden vector (see docs/QUF-SPEC.md §11). 576 bytes,
# sha256 5b2a236ba5e38bca9ad96783c4252a12f36517f98a9164a249f0db115f221392
GOLDEN_HEX = """
5155460001000000010000000a0000000b0000007175662e76657273696f6e08
0000000a0000007175662e707920312e300a00000063656c6c5f636f756e7404
000000020000000a000000656467655f636f756e7404000000030000000b0000
00726f7574655f636f756e74040000000300000006000000656467652e6b0400
0000080000000b0000007469636b5f706572696f6404000000400000000b0000
007175616e742e6469616c73080000000500000051312e31350b000000717561
6e742e6564676573080000000500000051312e31350d0000007175616e742e72
6f7574696e670800000002000000753805000000616c69676e04000000200000
0004000000050000006469616c73000000008001000000000000400000000000
000005000000656467657300000000c0010000000000003c0000000000000007
000000726f7574696e6700000000000200000000000006000000000000000500
00007469636b730000000020020000000000000c000000000000000000000000
0008800006000c00050000500400cd2c14000000300000000000000000000000
0008800006000c00050000600400cd2c14000100400000000000000000000000
00010000341200000000000000000000000000000002010140000700e8030000
0000000000000000010000000002030005000000000000000000000000000000
010102020f0f0000000000000000000000000000000000000000000000000000
0600000000000000030000000000000000000000000000000000000000000000
"""


def selftest():
    ok = True
    b = build(GOLDEN)
    if GOLDEN_HEX:
        want = bytes.fromhex("".join(GOLDEN_HEX.split()))
        if b != want:
            ok = False
            print("FAIL: golden vector mismatch")
            print("  built : %s" % b.hex())
            print("  golden: %s" % want.hex())
    parsed = read(b)
    b2 = rebuild(parsed)
    if b2 != b:
        ok = False
        print("FAIL: round-trip not byte-exact")
    issues = verify_bytes(b)
    if issues:
        ok = False
        print("FAIL: golden vector does not verify: %s" % issues)

    # tb/quf_tb.json, when present, must build to the same golden bytes.
    tbjson = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "tb", "quf_tb.json")
    if os.path.exists(tbjson):
        with open(tbjson) as f:
            doc = json.load(f)
        if build(doc) != b:
            ok = False
            print("FAIL: tb/quf_tb.json does not build to the golden bytes")

    if not ok:
        sys.exit(1)
    print("quf.py selftest PASS: %d bytes, sha256 %s, round-trip byte-exact"
          % (len(b), hashlib.sha256(b).hexdigest()))
    print("golden hex: %s" % b.hex())


# -------------------------------------------------------------------- CLI --

def cmd_create(args):
    with open(args.json) as f:
        doc = json.load(f)
    data = build(doc)
    with open(args.out, "wb") as f:
        f.write(data)
    with open(args.out + ".hex", "w") as f:
        f.write(to_hexfile(data))
    print("wrote %s (%d bytes) + %s.hex" % (args.out, len(data), args.out))


def cmd_info(args):
    with open(args.file, "rb") as f:
        parsed = read(f.read(), args.file)
    print("QUF v%d, %d KV pairs, %d sections"
          % (parsed["version"], len(parsed["kv"]), len(parsed["table"])))
    for k, vt, v in parsed["kv"]:
        print("  %-14s %-6s %s" % (k, TYPE_NAMES[vt], v))
    for name, kind, off, size in parsed["table"]:
        print("  section %-8s kind=%d off=%-6d size=%d" % (name, kind, off, size))


def cmd_dump(args):
    with open(args.file, "rb") as f:
        parsed = read(f.read(), args.file)
    cmd_info(args)
    print(json.dumps(decode_sections(parsed), indent=1))


def cmd_verify(args):
    with open(args.file, "rb") as f:
        buf = f.read()
    issues = verify_bytes(buf, args.file)
    if issues:
        for i in issues:
            print("QUF VERIFY FAIL: %s" % i)
        sys.exit(1)
    print("QUF VERIFY PASS: %s (%d bytes)" % (args.file, len(buf)))


def cmd_hex(args):
    with open(args.file, "rb") as f:
        data = f.read()
    with open(args.out, "w") as f:
        f.write(to_hexfile(data))
    print("wrote %s (%d bytes)" % (args.out, len(data)))


def cmd_selftest(_args):
    selftest()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="quf.py",
                                 description="QUF reference tool")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("create", help="build QUF from JSON")
    p.add_argument("json")
    p.add_argument("out")
    p.set_defaults(fn=cmd_create)

    p = sub.add_parser("info", help="header + section table")
    p.add_argument("file")
    p.set_defaults(fn=cmd_info)

    p = sub.add_parser("dump", help="full decode")
    p.add_argument("file")
    p.set_defaults(fn=cmd_dump)

    p = sub.add_parser("verify", help="structural verification")
    p.add_argument("file")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("hex", help="byte-per-line hex for testbenches")
    p.add_argument("file")
    p.add_argument("out")
    p.set_defaults(fn=cmd_hex)

    p = sub.add_parser("selftest", help="golden vector + round-trip")
    p.set_defaults(fn=cmd_selftest)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
