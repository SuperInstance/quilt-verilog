#!/usr/bin/env python3
"""G3: inject the PDR invariant as $assume cells (latch-index mapping).

Input: bare_inv.pla from `yosys-abc "read_aiger guarded_bare.aig; pdr -d
-I bare_inv.pla"`.  Its .ilb entries lo<k> are GLOBAL latch indices of
the source aig (verified: 147 support latches scattered over 0..499;
NOT positional).  Clause convention pinned empirically (sim_check):
row = cube of EXCLUDED states, so clause = negation = OR of literals
with '0' = positive and '1' = NEGATED.  (The committed 854-clause lane
pinned the opposite convention from a write_invariant dump -- at least
one of the two dumps has the other polarity; ours is verified against
273k simulated clause-checks from init with zero violations.)

Latch k -> wire name via guarded_baked.aig's symbol table (l<k> name),
falling back to guarded_aig.aim aliases.  Clauses touching a latch with
no resolvable name are DROPPED (fewer assumptions = stronger
obligation, sound) and reported.

Usage: inject_assumes.py bare_inv.pla guarded_baked.aig guarded_aig.aim \
                          guarded_aig.il guarded_assumed.il
"""
import re, sys
from collections import Counter


def parse_aig_symbols(path):
    data = open(path, "rb").read()
    eol = data.index(b"\n")
    hdr = data[:eol].decode().split()
    M, I, L, O, A = (int(x) for x in hdr[1:6])
    pos = eol + 1
    for _ in range(L):
        pos = data.index(b"\n", pos) + 1
    for _ in range(O):
        pos = data.index(b"\n", pos) + 1

    def rv(pos):
        s = v = 0
        while True:
            b = data[pos]; pos += 1
            v |= (b & 0x7F) << s; s += 7
            if not (b & 0x80):
                return v, pos
    for _ in range(A):
        _, pos = rv(pos); _, pos = rv(pos)
    sym = {}
    for line in data[pos:].split(b"\n"):
        t = line.decode().split()
        if t and t[0].startswith("l") and t[0][1:].isdigit() and len(t) > 1:
            sym.setdefault(int(t[0][1:]), t[1])
    return sym


def main(pla, aig, aim, il, out):
    sym = parse_aig_symbols(aig)
    varalias = {}
    for line in open(aim):
        t = line.split()
        if len(t) >= 4 and t[0] in ("latch", "init", "invlatch"):
            varalias.setdefault(int(t[1]), t[3])

    support, clauses = [], []
    for line in open(pla):
        line = line.rstrip("\n")
        if line.startswith(".ilb"):
            support = [int(x[2:]) for x in line.split()[1:]]
            continue
        # a PLA data row is two tokens with output in {0,1}; rows padded with
        # '.' can start with '.' and must NOT be read as dot-directives
        parts = line.split()
        if parts and parts[0].startswith(".") and not (
                len(parts) == 2 and parts[1] in ("0", "1")):
            continue
        if not line.strip() or line.startswith("#"):
            continue
        if not parts:
            continue
        cubes, o = parts[0], parts[-1]
        if o not in ("0", "1"):
            continue
        lit = [(support[j], -1 if c == "1" else +1)
               for j, c in enumerate(cubes) if c in "01"]
        if lit:
            clauses.append(lit)

    wires = {}
    for line in open(il):
        m = re.match(r"^  wire(?: width (\d+))?(?: signed| unsigned)? ([\\$].+)$",
                     line.rstrip("\n"))
        if m:
            wires[m.group(2)[1:]] = int(m.group(1) or 1)

    def name_of(k):
        for n in (sym.get(k), varalias.get(k)):
            if n:
                base = n
                m = re.fullmatch(r"(.+)\[(\d+)\]", n)
                bit = 0
                if m and m.group(1) in wires:
                    base, bit = m.group(1), int(m.group(2))
                elif n in wires:
                    base, bit = n, 0
                else:
                    continue
                if 0 <= bit < wires[base]:
                    return (base, bit)
        return None

    latchname = {k: name_of(k) for k in set(support)}
    unres = [k for k, v in latchname.items() if v is None]
    print(f"support={len(support)} unresolved-latches={len(unres)} {unres[:10]}")

    kept, dropped = [], []
    resolved = []
    for i, lit in enumerate(clauses):
        rr, ok = [], True
        for k, pol in lit:
            n = latchname[k]
            if n is None:
                ok = False
                break
            rr.append((n, pol))
        (resolved.append(rr), kept.append(i)) if ok else dropped.append(i)

    negbank, negidx = [], {}
    for lit in resolved:
        for (b, i2), pol in lit:
            if pol < 0 and (b, i2) not in negidx:
                negidx[(b, i2)] = len(negbank)
                negbank.append((b, i2))

    L = []
    if negbank:
        L.append(f"  wire width {len(negbank)} \\g3c_negbank")
        L.append("  cell $not $g3c_not_bank")
        L.append("    parameter \\A_SIGNED 0")
        L.append(f"    parameter \\A_WIDTH {len(negbank)}")
        L.append(f"    parameter \\Y_WIDTH {len(negbank)}")
        L.append("    connect \\A { " + " ".join(
            (f"\\{b}" if not b.startswith("$") else b) + f" [{i2}]" for b, i2 in negbank) + " }")
        L.append("    connect \\Y \\g3c_negbank")
        L.append("  end")
    for i, lit in zip(kept, resolved):
        L.append(f"  wire \\g3c_{i}")
        L.append(f"  cell $reduce_or $g3c_or_{i}")
        L.append("    parameter \\A_SIGNED 0")
        L.append(f"    parameter \\A_WIDTH {len(lit)}")
        L.append("    parameter \\Y_WIDTH 1")
        specs = []
        for (b, i2), pol in lit:
            ref = (f"\\{b}" if not b.startswith("$") else b) + f" [{i2}]"
            specs.append(ref if pol > 0 else f"\\g3c_negbank [{negidx[(b, i2)]}]")
        L.append("    connect \\A { " + " ".join(specs) + " }")
        L.append(f"    connect \\Y \\g3c_{i}")
        L.append("  end")
        L.append(f"  cell $assume $g3c_asm_{i}")
        L.append(f"    connect \\A \\g3c_{i}")
        L.append("    connect \\EN 1'1")
        L.append("  end")

    text = open(il).read()
    idx = text.rindex("end\n")
    text = text[:idx] + "\n".join(L) + "\n" + text[idx:]
    open(out, "w").write(text)
    print(f"clauses={len(clauses)} kept={len(kept)} dropped={len(dropped)} "
          f"negbank={len(negbank)}")


if __name__ == "__main__":
    main(*sys.argv[1:6])
