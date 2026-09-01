#!/usr/bin/env python3
"""G3 k-induction lane: inject the committed PDR invariant as RTLIL assume cells.

Parses the ABC PDR invariant dump (PLA, one clause per line: disjunction,
'1'=positive literal, '0'=negated literal -- convention pinned by the
implicate probe, see README.md) plus the write_aiger .aim map (k-th
latch line <-> column lo<k>), resolves every literal to a (wire,bit) of
the flattened fabric IL, and emits RTLIL cells:

  $not bank over all negated latch bits  -> \g3_negbank
  $reduce_or per clause                 -> \g3_clause_<i>
  $assume (or $assert with --mode assert) per clause

Clauses whose literals do not all resolve are DROPPED (fewer assumptions
= a stronger proof obligation, so dropping is sound) and reported.

Usage:
  gen_assumes.py --pla INV.pla --aim MAP.aim --il g3_flat.il \
                 [--readable COMMITTED_READABLE.txt] \
                 [--mode assume|assert] -o assume_cells.il -j report.json
"""
import argparse, json, re, sys
from collections import Counter

def parse_aim(path):
    latches = []  # ordinal -> (name, bit)
    for line in open(path):
        t = line.split()
        if t and t[0] in ("latch", "invlatch"):
            latches.append((t[3], int(t[2]), t[0] == "invlatch"))
    return latches

def parse_pla(path):
    ilb, rows, hdr = [], [], {}
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith(".ilb"):
            ilb = line.split()[1:]
        elif line.startswith("."):
            hdr[line.split()[0]] = line.split()[1:]
        elif line and not line.startswith("#"):
            rows.append(line)
    clauses = []
    for row in rows:
        cubes, out = row.split()
        lit = []
        for name, ch in zip(ilb, cubes):
            if ch == "1":
                lit.append((name, +1))
            elif ch == "0":
                lit.append((name, -1))
        if out == "1" and lit:
            clauses.append(lit)
    return ilb, hdr, clauses

def parse_il_wires(path):
    wires = {}
    for line in open(path):
        m = re.match(r"^  wire(?: width (\d+))? \\(.+)$", line.rstrip("\n"))
        if m:
            name = m.group(2)
            if name in wires and wires[name] != int(m.group(1) or 1):
                sys.exit(f"conflicting widths for wire {name!r}")
            wires[name] = int(m.group(1) or 1)
    return wires

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pla", required=True)
    ap.add_argument("--aim", required=True)
    ap.add_argument("--il", required=True)
    ap.add_argument("--readable")
    ap.add_argument("--mode", choices=["assume", "assert"], default="assume")
    ap.add_argument("-o", required=True)
    ap.add_argument("-j", "--report", required=True)
    a = ap.parse_args()

    latches = parse_aim(a.aim)
    ilb, hdr, clauses = parse_pla(a.pla)
    wires = parse_il_wires(a.il)

    def resolve(lit_name):
        m = re.fullmatch(r"lo(\d+)", lit_name)
        if not m:
            return None, f"ilb name {lit_name!r} not lo<ordinal>"
        k = int(m.group(1))
        if k >= len(latches):
            return None, f"lo{k} beyond aim latch count {len(latches)}"
        name, bit, inv = latches[k]
        return (name, bit, inv), None

    # map every column once
    colmap, errs = {}, Counter()
    for c in ilb:
        r, e = resolve(c)
        colmap[c] = r
        if e:
            errs[e] += 1

    def bit_ok(name, bit):
        return name in wires and 0 <= bit < wires[name]

    negbank, negidx = [], {}
    dropped, kept, unresolved_names = [], [], Counter()
    for i, lit in enumerate(clauses):
        resolved = []
        ok = True
        for col, pol in lit:
            r = colmap.get(col)
            if r is None:
                ok = False
                errs[f"unmapped column {col}"] += 1
                continue
            name, bit, inv = r
            if not bit_ok(name, bit):
                ok = False
                unresolved_names[f"{name}[{bit}]"] += 1
                continue
            # invlatch storage is complement of the named signal
            eff = -pol if inv else pol
            resolved.append((name, bit, eff))
        if ok and resolved:
            kept.append(resolved)
            for name, bit, eff in resolved:
                if eff < 0:
                    key = (name, bit)
                    if key not in negidx:
                        negidx[key] = len(negbank)
                        negbank.append(key)
        else:
            dropped.append((i, [f"{n}[{b}]" for n, b, _ in resolved] or ["<colmap>"]))

    # readable crosscheck (dead lane's rendering: polarity as written, & -joined)
    match = None
    if a.readable:
        def render(lit):
            out = []
            for col, pol in lit:
                r = colmap.get(col)
                nm = f"{r[0]}[{r[1]}]" if r else col
                out.append(("!" if pol < 0 else "") + nm)
            return " & ".join(out)
        mine = [render(l) for l in clauses]
        theirs = [l.strip() for l in open(a.readable) if l.strip()]
        match = sum(1 for x, y in zip(mine, theirs) if x == y)
        print(f"readable crosscheck: {match}/{len(theirs)} lines identical", file=sys.stderr)

    def sig(name, bit):
        return f"\\{name} [{bit}]"

    L = []
    if negbank:
        L.append(f"  wire width {len(negbank)} \\g3_negbank")
        L.append("  cell $not $g3_not_bank")
        L.append("    parameter \\A_SIGNED 0")
        L.append(f"    parameter \\A_WIDTH {len(negbank)}")
        L.append(f"    parameter \\Y_WIDTH {len(negbank)}")
        L.append("    connect \\A { " + " ".join(sig(n, b) for n, b in negbank) + " }")
        L.append("    connect \\Y \\g3_negbank")
        L.append("  end")
    for i, lit in enumerate(kept):
        L.append(f"  wire \\g3_clause_{i}")
        specs = []
        for name, bit, eff in lit:
            specs.append(sig(name, bit) if eff > 0 else f"\\g3_negbank [{negidx[(name, bit)]}]")
        L.append(f"  cell $reduce_or $g3_or_{i}")
        L.append("    parameter \\A_SIGNED 0")
        L.append(f"    parameter \\A_WIDTH {len(specs)}")
        L.append("    parameter \\Y_WIDTH 1")
        L.append("    connect \\A { " + " ".join(specs) + " }")
        L.append(f"    connect \\Y \\g3_clause_{i}")
        L.append("  end")
        ctype = "$assume" if a.mode == "assume" else "$assert"
        L.append(f"  cell {ctype} $g3_{a.mode}_{i}")
        L.append("    parameter \\A_SIGNED 0")
        L.append("    parameter \\A_WIDTH 1")
        L.append(f"    connect \\A \\g3_clause_{i} [0]")
        L.append("  end")
    open(a.o, "w").write("\n".join(L) + "\n")

    fam = Counter()
    for lit in kept:
        names = {n for n, _, _ in lit}
        s = " ".join(sorted(names))
        if "!u_pipe.m_a0[3]" in " ".join(
            ("!" if e < 0 else "") + f"{n}[{b}]" for n, b, e in lit
        ):
            fam["pipe_a0_hyp"] += 1
        if any(n.startswith("u_pipe.") for n in names):
            fam["mentions_pipe"] += 1
        if any(n.startswith("u_coreA.") for n in names) and any(n.startswith("u_coreB.") for n in names):
            fam["cross_core"] += 1
        if any(n.startswith("u_eng") for n in names):
            fam["mentions_engine"] += 1
        if any(n.split(".")[0].startswith("f_") for n in names):
            fam["mentions_f_accounting"] += 1
    sizes = Counter(len(l) for l in kept)
    rep = {
        "mode": a.mode,
        "pla_clauses": len(clauses),
        "kept": len(kept),
        "dropped": len(dropped),
        "dropped_indices": [i for i, _ in dropped][:50],
        "dropped_literals": [d for d in dropped][:20],
        "unresolved_names": dict(unresolved_names),
        "column_errors": dict(errs),
        "negbank_bits": len(negbank),
        "clause_size_hist": {str(k): v for k, v in sorted(sizes.items())},
        "families": dict(fam),
        "readable_crosscheck": match,
        "distinct_latch_signals": len({latches[k][0] for k in range(len(latches))}),
    }
    json.dump(rep, open(a.report, "w"), indent=1)
    print(json.dumps(rep, indent=1), file=sys.stderr)

if __name__ == "__main__":
    main()
