#!/usr/bin/env python3
"""G3: bake AIGER constraint outputs into the bad outputs (assume-guarantee).

Classic `abc pdr` ignores AIGER C-outputs (only `fold` applies them), and
`fold` renumbers latches post-fold, which is what made the committed
854-clause PLA's lo<k> columns unresolvable (246/854 ambiguous via the
folded net, 668/673 ambiguous under trace matching -- symmetric datapath
latches share traces).

Reduction used here instead: each bad output b_i becomes
    b_i' = b_i AND !c1 AND !c2 AND !c3
where c_j are the constraint outputs (violation flags: must stay 0).
Proving AG(!b_i') on the UNCONSTRAINED net establishes: every trace that
satisfies G(!c1&!c2&!c3) (the assumes, in sby semantics) also satisfies
G(!b_i) -- sound, since constrained traces are a subset of unconstrained
ones and each constrained state with a live constraint set has b' = b.

The output AIG has no constraint outputs, so `pdr -d` runs without fold
and its invariant lo<k> ordinals index the SAME latch order as the aim
(var column = 0-based latch index of the yosys-written aiger).

Usage: bake_constraints.py in.aig out.aig
"""
import sys

def parse(path):
    data = open(path, "rb").read()
    eol = data.index(b"\n")
    hdr = data[:eol].decode().split()
    M, I, L, O, A = (int(x) for x in hdr[1:6])
    ext = [int(x) for x in hdr[6:]]
    B = ext[0] if len(ext) > 0 else 0
    C = ext[1] if len(ext) > 1 else 0
    pos = eol + 1
    latches = []
    for _ in range(L):
        nl = data.index(b"\n", pos)
        latches.append(data[pos:nl])
        pos = nl + 1
    outputs = []
    for _ in range(O + B + C):
        nl = data.index(b"\n", pos)
        outputs.append(int(data[pos:nl].decode()))
        pos = nl + 1

    def rv(pos):
        shift = val = 0
        while True:
            b = data[pos]; pos += 1
            val |= (b & 0x7F) << shift; shift += 7
            if not (b & 0x80):
                return val, pos
    and_recs = bytearray()
    for _ in range(A):
        start = pos
        _, pos = rv(pos)
        _, pos = rv(pos)
        and_recs += data[start:pos]
    return data, hdr, M, I, L, O, A, B, C, latches, outputs, pos, bytes(and_recs)


def enc_delta(delta):
    out = bytearray()
    while delta & ~0x7F:
        out.append((delta & 0x7F) | 0x80)
        delta >>= 7
    out.append(delta)
    return bytes(out)


def and_lit(a, b, nextvar, recs):
    # AIGER binary: lhs_max > lhs_min; d1 = 2*var - lhs_max, d2 = lhs_max - lhs_min
    if a < b:
        a, b = b, a
    recs += enc_delta(2 * nextvar - a) + enc_delta(a - b)
    return 2 * nextvar, recs


def main():
    inp, outp = sys.argv[1:3]
    (data, hdr, M, I, L, O, A, B, C, latches, outputs,
     body_end, and_recs) = parse(inp)
    if O != 0 or B == 0 or C == 0:
        sys.exit(f"unexpected header O={O} B={B} C={C}; want O=0,B=9,C=3 style")
    bad = outputs[:B]
    cons = outputs[B:B + C]
    recs = bytearray(and_recs)
    v = M + 1
    new_out = []
    for b in bad:
        t = b
        for c in cons:
            # and-tree: t = t & !c
            t, recs = and_lit(t, c ^ 1, v, recs)
            v += 1
        new_out.append(t)
    # symbol table: carry over any latch symbols from input
    tail = data[body_end - len(and_recs):]
    sym = b""
    text = data[body_end - len(and_recs) + len(and_recs):]  # after original ANDs
    rest = data[body_end:]
    for line in rest.split(b"\n"):
        if line.startswith(b"l") and b" " in line:
            sym += line + b"\n"
    out = bytearray()
    out += f"aig {v-1} {I} {L} {B} {A + (len(new_out) and (v-1-M))}".encode() + b"\n"
    out += b"\n".join(latches) + b"\n"
    out += ("\n".join(str(x) for x in new_out) + "\n").encode()
    out += recs
    out += sym
    open(outp, "wb").write(out)
    print(f"wrote {outp}: M={v-1} O={B} (bad outputs weakened by {C} constraints), "
          f"A={A + (v-1-M)}, kept {sym.count(10)} latch symbols")


if __name__ == "__main__":
    main()
