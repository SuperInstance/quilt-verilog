#!/usr/bin/env python3
"""quilt_lower.py -- step-1 lowering: counter subset of .qm -> Verilog.

Reads a .qm (format "qm", version 1, emitted by tools/quilc.py) and lowers
the counter subset to synthesizable Verilog:

  cell ops  -> one reg per cell.field; the declared init is the synchronous
               reset value (journal entry 0). int<NN> gives the reg width;
               int<PW> takes the --pw parameter (default 16)
  tick ops  -> next-state logic in one always @(posedge clk) block with
               synchronous reset; every effect must be of the step-1 form
               dest <= dest + k (k a nonnegative integer; -k and a bare
               dest hold/decay variants are accepted)
  view ops  -> skipped: views are pure journal-prefix reads, and with the
               implicit journal (registers hold the latest entry) an
               identity view is just the register wire

The journal is implicit: no history is materialized; each register holds
the latest entry. bind / link / propose / loop ops are outside the step-1
subset and are rejected, as is anything but the effect form above, with
diagnostics of the form `path: error[lower]: message`.

The output module is quilt_<module> with non-identifier characters mapped
to underscores ("01-counter" -> quilt_01_counter). Ports: clk, rst, and
one output wire [W-1:0] per cell field (bare field name; qualified
cell_field on collision). Output defaults to an out/ dir beside the input
(regenerable, gitignored).

Stdlib only, Python >= 3.8. Usage:
  python3 tools/quilt_lower.py IN.qm [-o OUT.v] [--pw 16]
"""

import argparse
import json
import os
import re
import sys

DEFAULT_PW = 16
REJECTED_OPS = ("bind", "link", "propose", "loop")
IDENT_RE = re.compile(r"[^A-Za-z0-9_]")
EXPR_RE = re.compile(
    r"^(?P<cell>[A-Za-z_]\w*)\s*\.\s*(?P<field>[A-Za-z_]\w*)"
    r"(?:\s*(?P<sign>[+-])\s*(?P<k>\d+))?$")


def diag(path, msg):
    return "%s: error[lower]: %s" % (path, msg)


def ident(name):
    return IDENT_RE.sub("_", name)


def lit(value, width):
    return "%d'd%d" % (width, value & ((1 << width) - 1))


def lower(qm, path, pw):
    """Return (errors, verilog_text)."""
    if not isinstance(qm, dict) or qm.get("format") != "qm" \
            or qm.get("version") != 1:
        return [diag(path, "not a .qm file (expected format %r version 1)"
                     % "qm")], None

    errors = []
    cells = {}      # name -> {field: (width, init)}
    cell_order = []
    effects = {}    # (cell, field) -> signed k
    effect_order = []

    for op in qm.get("ops", []):
        kind = op.get("op")
        if kind == "cell":
            name = op.get("name", "?")
            if name in cells:
                errors.append(diag(path, "duplicate cell '%s'" % name))
                continue
            fields = {}
            for f in op.get("fields", []):
                ftype = f.get("type", "int<PW>")
                m = re.match(r"^int<(PW|\d+)>$", ftype)
                if not m:
                    errors.append(diag(path, "cell %s: unsupported field "
                                             "type %r" % (name, ftype)))
                    continue
                width = pw if m.group(1) == "PW" else int(m.group(1))
                if width < 1:
                    errors.append(diag(path, "cell %s: field %s: width must "
                                             "be >= 1" % (name, f["name"])))
                    continue
                init = f.get("init", 0)
                if not isinstance(init, int):
                    errors.append(diag(path, "cell %s: field %s: init must "
                                             "be an integer" % (name,
                                                                f["name"])))
                    continue
                fields[f["name"]] = (width, init)
            cells[name] = fields
            cell_order.append(name)
        elif kind == "view":
            continue
        elif kind == "tick":
            for e in op.get("effects", []):
                line = e.get("line", op.get("line", 0))
                m = EXPR_RE.match(e.get("expr", ""))
                if not m:
                    errors.append(diag(path, "line %s: effect '%s <= %s' is "
                                             "not the step-1 form "
                                             "dest <= dest + k"
                                             % (line, e.get("dest", "?"),
                                                e.get("expr", "?"))))
                    continue
                dest = (m.group("cell"), m.group("field"))
                if dest != (e.get("cell"), e.get("field")):
                    errors.append(diag(path, "line %s: effect reads '%s.%s', "
                                             "not its own dest '%s'"
                                             % (line, dest[0], dest[1],
                                                e.get("dest", "?"))))
                    continue
                if dest[0] not in cells or dest[1] not in cells[dest[0]]:
                    errors.append(diag(path, "line %s: effect writes unknown "
                                             "cell field '%s.%s'"
                                             % (line, dest[0], dest[1])))
                    continue
                if dest in effects:
                    errors.append(diag(path, "line %s: '%s.%s' written by "
                                             "more than one effect -- single "
                                             "writer (S1.2)"
                                             % (line, dest[0], dest[1])))
                    continue
                k = int(m.group("k")) if m.group("k") else 0
                if m.group("sign") == "-":
                    k = -k
                effects[dest] = k
                effect_order.append(dest)
        elif kind in REJECTED_OPS:
            errors.append(diag(path, "line %s: op '%s' is outside the step-1 "
                                     "counter subset" % (op.get("line", 0),
                                                         kind)))
        else:
            errors.append(diag(path, "unknown op %r" % kind))

    if not cells:
        errors.append(diag(path, "no cell declarations to lower"))
    if not effects and not errors:
        errors.append(diag(path, "no tick effects to lower"))
    if errors:
        return errors, None

    # Output port per cell field: bare field name, qualified on collision
    # or on a clash with the clk/rst control ports.
    port_of, used = {}, {"clk", "rst"}
    for cname in cell_order:
        for fname in cells[cname]:
            port = fname if fname not in used else "%s_%s" % (cname, fname)
            if port in used:
                errors.append(diag(path, "cannot name an output port for "
                                         "%s.%s" % (cname, fname)))
                continue
            port_of[(cname, fname)] = port
            used.add(port)
    if errors:
        return errors, None

    module = "quilt_" + ident(qm.get("module")
                              or os.path.splitext(os.path.basename(path))[0])

    lines = []
    lines.append("// %s -- generated by tools/quilt_lower.py from %s."
                 % (module, os.path.basename(path)))
    lines.append("// DO NOT EDIT: regenerate with"
                 " `python3 tools/quilt_lower.py %s`." % path)
    lines.append("// Step-1 counter subset: one register per cell field; the")
    lines.append("// journal is implicit (registers hold the latest entry);")
    lines.append("// synchronous reset to the declared init (journal entry 0).")
    lines.append("`default_nettype none")
    lines.append("")
    lines.append("module %s (" % module)
    lines.append("    input  wire        clk,")
    lines.append("    input  wire        rst,")
    outs = [(port_of[d], cells[d[0]][d[1]][0])
            for d in sorted(port_of, key=lambda d: port_of[d])]
    for i, (port, width) in enumerate(outs):
        rng = ("[%d:0]" % (width - 1)) if width > 1 else ""
        comma = "," if i < len(outs) - 1 else ""
        lines.append("    output wire %s%s%s"
                     % ((rng + " ").ljust(7), port, comma))
    lines.append(");")
    lines.append("")
    for cname in cell_order:
        for fname, (width, _init) in cells[cname].items():
            lines.append("    reg [%d:0] %s_%s;" % (width - 1, cname, fname))
    lines.append("")
    for (cname, fname), port in sorted(port_of.items(),
                                       key=lambda kv: kv[1]):
        lines.append("    assign %s = %s_%s;" % (port, cname, fname))
    lines.append("")
    lines.append("    always @(posedge clk) begin")
    lines.append("        if (rst) begin")
    for cname in cell_order:
        for fname, (width, init) in cells[cname].items():
            lines.append("            %s_%s <= %s;"
                         % (cname, fname, lit(init, width)))
    lines.append("        end else begin")
    for cname in cell_order:
        for fname, (width, _init) in cells[cname].items():
            reg = "%s_%s" % (cname, fname)
            k = effects.get((cname, fname), 0)
            if k > 0:
                lines.append("            %s <= %s + %s;"
                             % (reg, reg, lit(k, width)))
            elif k < 0:
                lines.append("            %s <= %s - %s;"
                             % (reg, reg, lit(-k, width)))
            else:
                lines.append("            %s <= %s;" % (reg, reg))
    lines.append("        end")
    lines.append("    end")
    lines.append("")
    lines.append("endmodule")
    lines.append("")
    lines.append("`default_nettype none")
    return [], "\n".join(lines)


def cmd_lower(args):
    try:
        with open(args.file, "r", encoding="utf-8") as fh:
            qm = json.load(fh)
    except (OSError, ValueError) as exc:
        print(diag(args.file, "cannot read .qm: %s" % exc), file=sys.stderr)
        print("FAIL %s" % args.file)
        return 1
    errors, text = lower(qm, args.file, args.pw)
    if errors:
        for d in errors:
            print(d, file=sys.stderr)
        print("FAIL %s: %d error(s)" % (args.file, len(errors)))
        return 1
    if args.out:
        out = args.out
    else:
        base = os.path.dirname(args.file) or "."
        stem = os.path.splitext(os.path.basename(args.file))[0]
        out = os.path.join(base, "out", stem + ".v")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    n_cells = sum(len(f) for f in
                  [c["fields"] for c in qm["ops"] if c.get("op") == "cell"])
    n_effects = sum(len(o.get("effects", [])) for o in qm["ops"]
                    if o.get("op") == "tick")
    module = re.search(r"^module (\w+)", text, re.M).group(1)
    print("OK %s -> %s (module %s, %d cell field(s), %d effect(s), PW=%d)"
          % (args.file, out, module, n_cells, n_effects, args.pw))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="quilt_lower",
        description="Lower the counter subset of a .qm (quilc output) to "
                    "synthesizable Verilog (step 1).")
    ap.add_argument("file", help="input .qm (format qm, version 1)")
    ap.add_argument("-o", "--out", default=None,
                    help="output .v (default: out/<stem>.v beside the input)")
    ap.add_argument("--pw", type=int, default=DEFAULT_PW,
                    help="width of int<PW> fields (default %d)" % DEFAULT_PW)
    args = ap.parse_args(argv)
    return cmd_lower(args)


if __name__ == "__main__":
    sys.exit(main())
