#!/usr/bin/env python3
"""Shift-closure augmentation, take 2 (fixed): generate every valid shifted
variant of the data-bus singleton templates, dedup against the mined set,
assert each generated row has >=2 bound literals, and insert rows BEFORE
the .e terminator.

Usage: shift_closure.py bare_inv.pla guarded_baked.aig guarded_aig.aim \
        guarded_aig.il bare_inv_aug2.pla [out_report]
"""
import re, sys
from collections import defaultdict
sys.path.insert(0, '.')
from group_clauses import parse_aig_symbols


def main(pla, aig, aim, il, out, report=None):
    sym = parse_aig_symbols(aig)
    varalias = {}
    for line in open(aim):
        t = line.split()
        if len(t) >= 4 and t[0] in ("latch", "init", "invlatch"):
            varalias.setdefault(int(t[1]), t[3])
    wires = {}
    for line in open(il):
        m = re.match(r"^  wire(?: width (\d+))?(?: signed| unsigned)? ([\\$].+)$",
                     line.rstrip("\n"))
        if m:
            wires[m.group(2)[1:]] = int(m.group(1) or 1)

    def resolve(k):
        for n in (sym.get(k), varalias.get(k)):
            if not n:
                continue
            base, bit = n, 0
            m = re.fullmatch(r"(.+)\[(\d+)\]", n)
            if m and m.group(1) in wires:
                base, bit = m.group(1), int(m.group(2))
            elif n not in wires:
                continue
            if 0 <= bit < wires[base]:
                return (base, bit)
        return None

    lines = open(pla).read().splitlines()
    ilb, clauses = [], []
    for line in lines:
        if line.startswith(".ilb"):
            ilb = [int(x[2:]) for x in line.split()[1:]]
        elif line.startswith(".") or line.startswith("#") or not line.strip():
            continue
        else:
            cubes, o = line.split()
            if o == "1":
                clauses.append([(ilb[j], -1 if c == "1" else +1)
                                for j, c in enumerate(cubes) if c in "01"])
    pos_of = {k: j for j, k in enumerate(ilb)}
    # rev built ONLY from support latches (names proven collision-free)
    rev = {resolve(k): k for k in ilb}

    def row_of(inst):
        row = ["."] * len(ilb)
        for b, bit, p in inst:
            k = rev.get((b, bit))
            if k is None or k not in pos_of:
                return None
            row[pos_of[k]] = "1" if p < 0 else "0"
        return "".join(row)

    existing = set()
    for cl in clauses:
        row = ["."] * len(ilb)
        for k, p in cl:
            row[pos_of[k]] = "1" if p < 0 else "0"
        existing.add("".join(row))

    fams = defaultdict(list)
    for cl in clauses:
        lits, bits = [], []
        for k, p in cl:
            b, bit = resolve(k)
            lits.append((b, bit if wires[b] > 1 else 0, p))
            if wires[b] > 1:
                bits.append(bit)
        pos = [b for b in bits if b > 0]
        anchor = min(pos) if pos else (min(bits) if bits else 0)
        ents = [(b, ("s" if wires[b] == 1 else i - anchor), p) for b, i, p in lits]
        key = tuple(sorted(ents, key=lambda t: (t[0], str(t[1]), t[2])))
        fams[key].append(anchor)

    new = []
    skipped_covered = skipped_unsupported = 0
    for key, anchors in fams.items():
        if len(anchors) != 1:
            continue
        data = [(b, i, p) for b, i, p in key if i != "s"]
        if not data or not all(wires[b] > 1 for b, _, _ in data):
            continue
        maxmin = min(wires[b] for b, _, _ in data)
        maxrel = max(i for _, i, _ in data)
        minrel = min(i for _, i, _ in data)
        for a in range(-minrel, maxmin - maxrel):
            if a in anchors:
                skipped_covered += 1
                continue
            inst = [(b, (i + a) if i != "s" else 0, p) for b, i, p in key]
            if any(not (0 <= bit < wires[b]) for b, bit, p in inst):
                continue
            r = row_of(inst)
            if r is None:
                skipped_unsupported += 1
                continue
            nbound = sum(1 for c in r if c in "01")
            assert nbound >= 2, ("empty/near-empty row", key, a, r)
            if r not in existing:
                existing.add(r)
                new.append(r)
    print(f"shift-candidate singleton templates processed; "
          f"new rows: {len(new)} (covered anchors skipped: {skipped_covered}, "
          f"out-of-support shifts skipped: {skipped_unsupported})")

    # insert before .e, keep everything else verbatim
    outl, inserted = [], False
    for line in lines:
        if line.startswith(".p"):
            outl.append(f".p {len(clauses) + len(new)}")
        elif line.startswith(".e") and not inserted:
            outl.extend(r + " 1" for r in new)
            outl.append(line)
            inserted = True
        else:
            outl.append(line)
    assert inserted, "no .e terminator found"
    open(out, "w").write("\n".join(outl) + "\n")
    if report:
        open(report, "w").write("\n".join(
            ["# shift-closure augmentation manifest"] +
            [f"{r} 1" for r in new]) + "\n")
    print(f"wrote {out}: {len(clauses) + len(new)} clauses")


if __name__ == "__main__":
    main(*sys.argv[1:6], *(sys.argv[6:7] or [None]))
