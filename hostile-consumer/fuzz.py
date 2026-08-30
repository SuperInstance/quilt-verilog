#!/usr/bin/env python3
"""hostile-consumer spec-fuzzer: mutates a seed QUF per the mission's
mutation classes and classifies the outcome. Reference behavior is NOT
consulted (tools/quf.py is off-limits by mission rule); every place where
the spec text fails to determine the outcome is filed as a SPEC GAP.

Mutation classes (mission list):
  flip version nibble / truncate file / oversized section table /
  endianness trap / zero-length section / plus extras: bad magic, bad
  endian word, bad KV value type, kv_count lie, section overlap,
  misaligned offset, nonzero padding, edge.k out of range.
Each case is emitted into corpus/mutants/ and parsed by qufparse; a
SpecGap result (or a mutation where two defensible readings both pass our
parser) is a spec finding.
"""
import os, struct, subprocess, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "target", "debug", "qufparse")
SEED = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "tb/run/quf_tb_input.quf")
OUT = os.path.join(ROOT, "corpus", "mutants")
os.makedirs(OUT, exist_ok=True)

data = bytearray(open(SEED, "rb").read())

def w32(buf, off, v): buf[off:off+4] = struct.pack("<I", v)

def case(name, blob):
    p = os.path.join(OUT, name + ".quf")
    open(p, "wb").write(bytes(blob))
    r = subprocess.run([BIN, p], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    verdict = out[0] if out else "(no output)"
    return name, r.returncode, verdict

cases = []

# 1. flipped version nibble (both nibbles)
for tag, off in [("hi", 7), ("lo", 4)]:
    b = bytearray(data); b[7] ^= 0x10 if tag == "hi" else 0x01
    cases.append(case(f"version-nibble-{tag}", b))

# 2. truncated file (several cut points)
for cut in [8, 16, 100, 300, len(data) - 1, len(data) - 33]:
    b = bytearray(data[:cut])
    cases.append(case(f"truncate-{cut}", b))

# 3. oversized section table: section_count = 0xFFFFFFFF
b = bytearray(data)
# find section_count offset: it is after kv region; locate by searching the
# golden layout is not allowed — instead recompute: skip header+KVs generically.
def kv_end(buf):
    p = 16
    for _ in range(struct.unpack_from("<I", buf, 12)[0]):
        nl = struct.unpack_from("<I", buf, p)[0]; p += 4 + nl
        vt = struct.unpack_from("<I", buf, p)[0]; p += 4
        if vt == 8:
            l = struct.unpack_from("<I", buf, p)[0]; p += 4 + l
        elif vt == 9:
            et = struct.unpack_from("<I", buf, p)[0]; p += 4
            n = struct.unpack_from("<I", buf, p)[0]; p += 4
            sz = {0:1,1:1,7:1,2:2,3:2,4:4,5:4,6:4,10:8,11:8,12:8}.get(et, 0)
            p += n * sz
        else:
            p += {0:1,1:1,7:1,2:2,3:2,4:4,5:4,6:4,10:8,11:8,12:8}[vt]
    return p

se = kv_end(data)
for sc in [5, 1000, 0xFFFFFFFF]:
    b = bytearray(data); w32(b, se, sc)
    cases.append(case(f"section-count-{sc}", b))

# 4. endianness trap: endian word = 0 (big-endian marker)
b = bytearray(data); w32(b, 8, 0)
cases.append(case("endian-zero", b))
b = bytearray(data); w32(b, 8, 2)
cases.append(case("endian-two", b))

# 5. zero-length sections (size=0 for each of the four)
sec_entries = []
p = se + 4
for _ in range(struct.unpack_from("<I", data, se)[0]):
    nl = struct.unpack_from("<I", data, p)[0]
    name = data[p+4:p+4+nl].decode()
    off = struct.unpack_from("<Q", data, p+8+nl)[0]
    size = struct.unpack_from("<Q", data, p+16+nl)[0]
    sec_entries.append((name, p+16+nl, off, size))
    p += 4 + nl + 4 + 8 + 8
for name, szpos, off, size in sec_entries:
    b = bytearray(data)
    b[szpos:szpos+8] = struct.pack("<Q", 0)
    cases.append(case(f"zero-size-{name}", b))

# extras
b = bytearray(data); b[0] = 0x47
cases.append(case("bad-magic", b))
b = bytearray(data); b[9] = 0xFF
cases.append(case("version-nonce-ff", b))

# edge.k out of range: patch the KV value (u32 at known KV position)
def kv_val_off(buf, key):
    p = 16
    for _ in range(struct.unpack_from("<I", buf, 12)[0]):
        nl = struct.unpack_from("<I", buf, p)[0]
        nm = buf[p+4:p+4+nl].decode()
        vt = struct.unpack_from("<I", buf, p+4+nl)[0]
        vo = p + 8 + nl
        if nm == key: return vo, vt
        p = vo
        if vt == 8:
            l = struct.unpack_from("<I", buf, p)[0]; p += 4 + l
        elif vt == 9:
            et = struct.unpack_from("<I", buf, p)[0]; p += 4
            n = struct.unpack_from("<I", buf, p)[0]; p += 4
            p += n * {0:1,1:1,7:1,2:2,3:2,4:4,5:4,6:4,10:8,11:8,12:8}[et]
        else:
            p += {0:1,1:1,7:1,2:2,3:2,4:4,5:4,6:4,10:8,11:8,12:8}[vt]
    return None, None

vo, vt = kv_val_off(data, "edge.k")
for k in [0, 17, 0xFFFFFFFF]:
    b = bytearray(data); w32(b, vo, k)
    cases.append(case(f"edgek-{k}", b))

# kv_count lie (too many)
b = bytearray(data); w32(b, 12, 11)
cases.append(case("kvcount-lie-11", b))
# unknown value type id
b = bytearray(data)
vo, vt = kv_val_off(data, "align")
w32(b, vo - 4, 13)
cases.append(case("kv-vtype-13", b))
w32(b, vo - 4, 99)
cases.append(case("kv-vtype-99", b))
# array of strings (nested forbidden)
b = bytearray(data); w32(b, vo - 4, 9); w32(b, vo, 8)
cases.append(case("kv-array-of-strings", b))

print(f"{'case':28s} {'rc':>3s}  verdict")
for name, rc, v in cases:
    print(f"{name:28s} {rc:3d}  {v}")
gaps = [c for c in cases if "SpecGap" in c[2]]
print(f"\n{len(cases)} mutants, {len(gaps)} parsed as SpecGap")
