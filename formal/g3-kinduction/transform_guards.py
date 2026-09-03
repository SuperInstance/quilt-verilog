#!/usr/bin/env python3
"""G3: convert every assume of the flattened fabric into a sticky assert guard.

Input:  g3_flat.il (produced by flatten.ys: the exact sby-prep-equivalent
        netlist incl. formalff -assume's init-related assume cells).
Output: g3_flat_guarded.il where
  - every $check FLAVOR "assume" cell (A, EN) is deleted and contributes
    violation flag viol_i = EN & ~A to a shared bus g3_viol (reduce_or);
  - every $check FLAVOR "assert" cell (B, EN) is rewired to
    assert(B | g3_viol, EN).
Semantics: AG(!bad') on the guarded net == AG(!bad) on the original net
under G(all assumes).  The guard is a combinational predicate of the
CURRENT state -- exactly what PDR's baked-aig experiment proved inductive
with an EMPTY invariant -- so plain k-induction on the guarded net is the
engine-independent G3 certificate (no 854-clause machine invariant).

Usage: transform_guards.py g3_flat.il g3_flat_guarded.il
"""
import re, sys

CELL_RE = re.compile(r"(  cell \$check (\S+)\n.*?\n  end\n)", re.S)


def main(src, dst):
    text = open(src).read()
    assumes, asserts = [], []
    for m in CELL_RE.finditer(text):
        body = m.group(1)
        fl = re.search(r'parameter \\FLAVOR "(\w+)"', body)
        if not fl:
            continue
        a = re.search(r"connect \\A (.+)\n", body)
        e = re.search(r"connect \\EN (.+)\n", body)
        rec = {"full": m.group(1), "A": a.group(1).strip(), "EN": e.group(1).strip()}
        if fl.group(1) == "assume":
            assumes.append(rec)
        elif fl.group(1) == "assert":
            asserts.append(rec)
    if not asserts or not assumes:
        sys.exit(f"found asserts={len(asserts)} assumes={len(assumes)} -- dialect?")
    print(f"assumes={len(assumes)} asserts={len(asserts)}")

    L = []
    viols = []
    for i, asm in enumerate(assumes):
        A, EN = asm["A"], asm["EN"]
        L.append(f"  wire \\g3_na{i}")
        L.append(f"  cell $not $g3_not{i}")
        L.append("    parameter \\A_SIGNED 0")
        L.append("    parameter \\A_WIDTH 1")
        L.append("    parameter \\Y_WIDTH 1")
        L.append(f"    connect \\A {A}")
        L.append(f"    connect \\Y \\g3_na{i}")
        L.append("  end")
        if EN == "1'h1":
            viols.append(f"\\g3_na{i}")
        else:
            L.append(f"  wire \\g3_v{i}")
            L.append(f"  cell $and $g3_and{i}")
            L.append("    parameter \\A_SIGNED 0")
            L.append("    parameter \\A_WIDTH 1")
            L.append("    parameter \\B_SIGNED 0")
            L.append("    parameter \\B_WIDTH 1")
            L.append("    parameter \\Y_WIDTH 1")
            L.append(f"    connect \\A \\g3_na{i}")
            L.append(f"    connect \\B {EN}")
            L.append(f"    connect \\Y \\g3_v{i}")
            L.append("  end")
            viols.append(f"\\g3_v{i}")
    L.append("  wire \\g3_viol")
    L.append("  cell $reduce_or $g3_orviol")
    L.append("    parameter \\A_SIGNED 0")
    L.append(f"    parameter \\A_WIDTH {len(viols)}")
    L.append("    parameter \\Y_WIDTH 1")
    L.append("    connect \\A { " + " ".join(viols) + " }")
    L.append("    connect \\Y \\g3_viol")
    L.append("  end")
    # sticky trace-exclusion: g3_bad_t = (OR of assume violations so far, incl. current)
    # g3_sticky is init-0 FF: Q <= g3_bad; assert guard uses g3_bad directly.
    L.append("  attribute \\init 1'0")
    L.append("  wire \\g3_sticky")
    L.append("  attribute \\keep 1")
    L.append("  wire \\g3_bad")
    L.append("  cell $dff $g3_sticky_ff")
    L.append("    parameter \\CLK_POLARITY 1")
    L.append("    parameter \\WIDTH 1")
    L.append("    connect \\CLK \\clk")
    L.append("    connect \\D \\g3_bad")
    L.append("    connect \\Q \\g3_sticky")
    L.append("  end")
    L.append("  cell $or $g3_bador")
    L.append("    parameter \\A_SIGNED 0")
    L.append("    parameter \\A_WIDTH 1")
    L.append("    parameter \\B_SIGNED 0")
    L.append("    parameter \\B_WIDTH 1")
    L.append("    parameter \\Y_WIDTH 1")
    L.append("    connect \\A \\g3_sticky")
    L.append("    connect \\B \\g3_viol")
    L.append("    connect \\Y \\g3_bad")
    L.append("  end")
    inject = "\n".join(L) + "\n"

    new_text = text
    for asm in assumes:
        # cells carry an attribute line right above them; strip both
        idx = new_text.find(asm["full"])
        assert idx >= 0
        # find start of preceding attribute line if attached
        pre = new_text.rfind("\n  attribute ", 0, idx)
        line_start = new_text.rfind("\n", 0, idx) + 1
        cut_from = pre + 1 if pre >= 0 and new_text.count("\n", pre, idx) <= 1 else line_start
        new_text = new_text[:cut_from] + new_text[cut_from + (idx - cut_from) + len(asm["full"]):]

    first = asserts[0]["full"]
    idx = new_text.find(first)
    assert idx >= 0
    new_text = new_text[:idx] + inject + new_text[idx:]

    for i, asr in enumerate(asserts):
        block = (
            f"  wire \\g3_aa{i}\n"
            f"  cell $reduce_or $g3_orass{i}\n"
            f"    parameter \\A_SIGNED 0\n"
            f"    parameter \\A_WIDTH 2\n"
            f"    parameter \\Y_WIDTH 1\n"
            f"    connect \\A {{ {asr['A']} \\g3_bad }}\n"
            f"    connect \\Y \\g3_aa{i}\n"
            f"  end\n"
        )
        old_cell = asr["full"]
        new_cell = old_cell.replace(
            f"connect \\A {asr['A']}\n", f"connect \\A \\g3_aa{i}\n", 1)
        assert new_cell != old_cell, asr["A"]
        k = new_text.find(old_cell)
        assert k >= 0, f"assert {i} cell not found"
        new_cell = new_cell.replace("cell $check ", "cell $assert ", 1)
        new_cell = re.sub(r"    parameter .+\n", "", new_cell)
        new_cell = re.sub(r"    connect \\ARGS .+\n", "", new_cell)
        new_cell = re.sub(r"    connect \\TRG .+\n", "", new_cell)
        new_text = new_text[:k] + block + new_cell + new_text[k + len(old_cell):]

    open(dst, "w").write(new_text)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
