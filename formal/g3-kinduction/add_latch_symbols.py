#!/usr/bin/env python3
"""Append a latch symbol table (l<k> name[bit]) to a binary AIGER file.

The aim's var column is the 0-based latch index of the yosys-written aiger
(max aim var 802 < L=804). Names are resolved against the flattened IL's
wire list so every emitted symbol is a real handle; latches with no
resolvable name get a fallback token (clauses touching them are dropped
downstream -- sound, since fewer assumptions = stronger obligation).

Usage: add_latch_symbols.py in.aig map.aim flat.il out.aig
"""
import re, sys

def parse_aiger_body(path):
    data = open(path, "rb").read()
    # header line
    eol = data.index(b"\n")
    hdr = data[:eol].decode().split()
    assert hdr[0] == "aig"
    M, I, L, O, A = (int(x) for x in hdr[1:6])
    ext = [int(x) for x in hdr[6:]]  # B C J F if present
    pos = eol + 1
    # latch lines (ascii, one per latch)
    latches = []
    for _ in range(L):
        nl = data.index(b"\n", pos)
        latches.append(data[pos:nl].decode())
        pos = nl + 1
    nout = O + (ext[0] if len(ext) > 0 else 0) + (ext[1] if len(ext) > 1 else 0)
    outputs = []
    for _ in range(nout):
        nl = data.index(b"\n", pos)
        outputs.append(data[pos:nl].decode())
        pos = nl + 1
    # AND records: 2 varints each
    def read_varint(pos):
        shift = 0
        val = 0
        while True:
            b = data[pos]
            pos += 1
            val |= (b & 0x7F) << shift
            shift += 7
            if not (b & 0x80):
                return val, pos
    for _ in range(A):
        _, pos = read_varint(pos)
        _, pos = read_varint(pos)
    return data, hdr, latches, outputs, pos

def main():
    aig, aim, il, out = sys.argv[1:5]
    data, hdr, latches, outputs, body_end = parse_aiger_body(aig)
    L = int(hdr[3])
    # aim: var (latch idx) -> [(name, bit)]
    from collections import defaultdict
    amap = defaultdict(list)
    for line in open(aim):
        t = line.split()
        if t and t[0] in ("latch", "invlatch"):
            amap[int(t[1])].append((t[3], int(t[2])))
    # il wires
    wires = {}
    for line in open(il):
        m = re.match(r"^  wire(?: width (\d+))? \\(.+)$", line.rstrip("\n"))
        if m:
            wires[m.group(2)] = int(m.group(1) or 1)
    syms, unresolved = [], 0
    for k in range(L):
        cands = amap.get(k, [])
        pick = None
        for name, bit in cands:
            if name in wires and 0 <= bit < wires[name]:
                pick = f"{name}[{bit}]"
                break
        if pick is None:
            pick = f"unresolved_l{k}"
            unresolved += 1
        syms.append(f"l{k} {pick}")
    blob = data[:body_end]  # everything through AND records
    # existing trailing section (symbol table / comment) -- inspect
    tail = data[body_end:]
    keep_tail = b""
    if tail:
        # strip any existing symbol table/comment; keep comment content only if no 'c'
        text = tail.decode(errors="replace")
        if text.startswith("c"):
            keep_tail = b"c\nadded-latch-symbols g3\n"
        # else: existing symbol table dropped (we supply our own)
    symtable = ("\n".join(syms) + "\n").encode()
    open(out, "wb").write(blob + symtable + keep_tail)
    print(f"L={L} symbols written, unresolved={unresolved}, tail={tail[:20]!r}")

if __name__ == "__main__":
    main()
