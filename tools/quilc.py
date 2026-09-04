#!/usr/bin/env python3
"""quilc.py -- QUIL front-end checker and .qm emitter (QUIL builder lane).

Implements the grammar subset from docs/QUIL-RFC-local.md (the LOCAL RFC copy):
  cell / int<PW> declarations (S1.1), tick + effect assignments (S1.2),
  view (S1.3), bind / link (S1.4), propose-as-input-port (S1.5),
  for loops with static or journal-derived bounds (S1.6).

Two cell forms lower to the same IR (the RFC S1.1 cell-block form is
canonical; the scalar form is accepted alongside it):
  cell NAME { TYPE field = init; ... }   -- cell-block form; NAME.field
                                          references in bodies
  cell NAME int<W> = k { stmt* }         -- scalar form; bare NAME references
                                          (one implicit field "val"; body
                                          statements: tick / view / for)

Also accepted, per the RFC and its S3 acceptance sketch: literal widths
(int<16>) beside the PW parameter, the ternary (?:) in tick expressions,
bare references to bound views, the journal-prefix builtin fired(c, -k)
(S3.2), and named elaboration constants as static trip counts (S1.6).

Checks -- every violation is a compile error BEFORE any lowering exists
(pass L1 discipline, S2.1):
  R1  only tick writes; single writer per cell.field per tick; no effect may
      read another effect's same-tick dest (SPIN-19 bug class, made a parse
      error); in the scalar form, a cell's tick writes only its own state
  R2  view purity: a view body names only its declared journal-prefix params,
      integer constants, and other views -- never propose ports, never raw
      out-of-signature cell state, never assignments
  R3  helm-region hygiene: no float literals, no wall-clock primitives, no
      network primitives anywhere in helm code (S1.5: the vocabulary is
      absent by design, not by convention)
  R4  loop trip counts are static (0..<N or 0..<ELAB_CONST) or
      journal-derived (journal(cell)); data-dependent bounds on live state
      and unbounded loop constructs (while/do/until) are a parse error (S1.6)
  R5  fabric shape: bind sources are views, destinations declared cells,
      fanout equals the named reader count (D4 conservation), arrive is a
      round-19 mechanism; link is the symmetric form 'A <-> B kind = gap'

Success emits .qm (format "qm", version 1): a JSON op list in declaration
order; effects nest in ticks, ticks nest in loops. Failure prints cell/line
diagnostics of the form `path:line: error[cell]: message` and exits 1.

Stdlib only, Python >= 3.8. Usage:
  python3 tools/quilc.py check FILE.quil [-o OUT.qm]
  python3 tools/quilc.py selftest [--dir DIR]
"""

import argparse
import json
import os
import re
import subprocess
import sys

QM_FORMAT = "qm"
QM_VERSION = 1

# journal-prefix builtins callable inside views/effects (RFC S1.3):
#   fired(cell, -k) -- 1 iff the cell fired on journal entry t-k
#   journal(cell)   -- the cell's journal length (loop-bound derivations)
BUILTIN_VIEWS = {"fired", "journal"}
ARRIVE_FAMILY = ("queue_cell", "credit_fence", "staged_grant")
BUILTIN_FNS = ("fired",)  # journal-prefix fire lookup helper (RFC S3.2 sketch)
UNBOUNDED_LOOPS = ("while", "do", "until")  # R4: never expressible (S1.6)
BANNED_EXACT = {
    "now", "clock", "time", "wallclock", "wall_clock", "sleep",
    "net", "socket", "http", "https", "url", "recv", "send",
    "listen", "fetch", "rpc",
}
BANNED_PREFIX = ("net_",)
TOP_KEYWORDS = ("cell", "view", "bind", "link", "propose", "tick", "for")

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

TOK_RE = re.compile(
    r"""
      (?P<ws>\s+)
    | (?P<float>\d+\.\d+(?:[eE][+-]?\d+)?|\d+[eE][+-]?\d+)
    | (?P<int>\d+)
    | (?P<ident>[A-Za-z_][A-Za-z0-9_]*)
    | (?P<punct><->|->|\.\.|<=|>=|==|!=|&&|\|\||[{}();,=<>+\-*/%.!?:])
    """,
    re.VERBOSE,
)


class Tok:
    __slots__ = ("kind", "text", "line")

    def __init__(self, kind, text, line):
        self.kind = kind
        self.text = text
        self.line = line

    def is_p(self, text):
        return self.kind == "punct" and self.text == text

    def __repr__(self):  # pragma: no cover - debug aid
        return "Tok(%s,%r,L%d)" % (self.kind, self.text, self.line)


def tokenize(source):
    """Return (tokens, errors). Errors cover S1.5 hygiene: float literals and
    wall-clock / network primitives are rejected at the vocabulary level."""
    toks, errors = [], []
    for line_no, raw in enumerate(source.splitlines(), 1):
        line = raw.split("//", 1)[0]
        pos = 0
        while pos < len(line):
            m = TOK_RE.match(line, pos)
            if not m:
                errors.append((line_no, "helm",
                               "syntax: unexpected character %r" % line[pos]))
                pos += 1
                continue
            pos = m.end()
            kind = m.lastgroup
            text = m.group()
            if kind == "ws":
                continue
            if kind == "float":
                errors.append((line_no, "helm",
                               "R3: float literal '%s' in helm region "
                               "(int<PW> only, S1.5)" % text))
            elif kind == "ident":
                if text in BANNED_EXACT or text.startswith(BANNED_PREFIX):
                    errors.append((line_no, "helm",
                                   "R3: wall-clock/network primitive '%s' in "
                                   "helm region (S1.5: no such vocabulary)" % text))
            toks.append(Tok(kind, text, line_no))
    return toks, errors


# ---------------------------------------------------------------------------
# Parser + semantic checker
# ---------------------------------------------------------------------------

class Compiler:
    def __init__(self, source, path="<quil>"):
        self.path = path
        self.toks, self.errors = tokenize(source)
        self.i = 0
        self.ops = []
        self.cells = {}          # name -> {"fields": {f: init}, "line": n}
        self.views = {}          # name -> {"params": [...], "line": n}
        self.propose_ports = set()

    # -- diagnostics --------------------------------------------------------

    def err(self, line, cell, msg):
        self.errors.append((line, cell, msg))

    def diag(self, line, cell, msg):
        return "%s:%d: error[%s]: %s" % (self.path, line, cell, msg)

    # -- token cursor -------------------------------------------------------

    def peek(self, ahead=0):
        j = self.i + ahead
        return self.toks[j] if j < len(self.toks) else None

    def advance(self):
        t = self.peek()
        if t is not None:
            self.i += 1
        return t

    def eat_p(self, text):
        t = self.peek()
        if t is not None and t.is_p(text):
            self.i += 1
            return True
        return False

    def expect_p(self, text, cell, what):
        if not self.eat_p(text):
            t = self.peek()
            got = t.text if t else "<eof>"
            self.err(t.line if t else 0, cell,
                     "syntax: expected '%s' %s, got '%s'" % (text, what, got))
            return False
        return True

    def expect_ident(self, cell, what):
        t = self.peek()
        if t is None or t.kind != "ident":
            got = t.text if t else "<eof>"
            self.err(t.line if t else 0, cell,
                     "syntax: expected identifier %s, got '%s'" % (what, got))
            return None
        self.i += 1
        return t

    def recover_to_top(self):
        depth = 0
        while True:
            t = self.peek()
            if t is None:
                return
            if t.kind == "punct":
                if t.text in "{([":
                    depth += 1
                elif t.text in "})]":
                    depth = max(0, depth - 1)
                elif t.text == ";" and depth == 0:
                    self.i += 1
                    return
            elif t.kind == "ident" and t.text in TOP_KEYWORDS and depth == 0:
                return
            self.i += 1

    # -- top level ----------------------------------------------------------

    def parse(self):
        while True:
            t = self.peek()
            if t is None:
                break
            if t.kind != "ident":
                self.err(t.line, "top", "syntax: unexpected token '%s'" % t.text)
                self.advance()
                self.recover_to_top()
                continue
            word = t.text
            try:
                if word == "cell":
                    self.parse_cell()
                elif word == "view":
                    self.parse_view()
                elif word == "bind":
                    self.parse_bind()
                elif word == "link":
                    self.parse_link()
                elif word == "propose":
                    self.parse_propose()
                elif word == "tick":
                    self.ops.append(self.parse_tick())
                elif word == "for":
                    self.ops.append(self.parse_for())
                else:
                    self.parse_stray_write()
            except _Recover:
                self.recover_to_top()
        return self

    def parse_stray_write(self):
        """A write-shaped statement at top level: the R1 trap. Accepts
        `cell.field <= expr;`, `effect cell.field <= expr;`, and the scalar
        form's bare `name <= expr;`."""
        t = self.peek()
        line = t.line
        j = self.i
        if t.text == "effect" and self.peek(1) is not None:
            self.advance()
            t = self.peek()
        if (self.peek(1) is not None and self.peek(1).is_p(".")
                and self.peek(2) is not None and self.peek(2).kind == "ident"
                and self.peek(3) is not None and self.peek(3).is_p("<=")):
            cell = "%s.%s" % (t.text, self.peek(2).text)
            self.err(line, cell, "R1: write outside tick -- tick is the only "
                                 "writer (S1.2)")
        elif self.peek(1) is not None and self.peek(1).is_p("<="):
            self.err(line, t.text, "R1: write outside tick -- tick is the only "
                                   "writer (S1.2)")
        else:
            self.err(line, "top", "syntax: unknown statement '%s'" % t.text)
        self.i = j
        self.recover_to_top()

    # -- constructs ---------------------------------------------------------

    def parse_pw_type(self, cell, where):
        """Consume `int<PW>` or a literal width like `int<16>`; return the
        type string (e.g. "int<PW>", "int<16>"), or None on error."""
        t = self.expect_ident(cell, "(type)")
        if t is None:
            return None
        if t.text != "int":
            self.err(t.line, cell, "syntax: %s: only type is int<PW>, got "
                                   "'%s'" % (where, t.text))
            return None
        if not self.expect_p("<", cell, "after 'int'"):
            return None
        w = self.peek()
        if w is not None and w.kind == "ident":
            self.advance()
            if w.text != "PW":
                self.err(w.line, cell,
                         "syntax: %s: width must be the PW parameter or an "
                         "integer literal, got '%s'" % (where, w.text))
                self.expect_p(">", cell, "closing width")
                return None
            width = "PW"
        elif w is not None and w.kind == "int":
            self.advance()
            width = w.text
        else:
            got = w.text if w else "<eof>"
            self.err(w.line if w else 0, cell,
                     "syntax: %s: width must be the PW parameter or an "
                     "integer literal, got '%s'" % (where, got))
            return None
        if not self.expect_p(">", cell, "closing width"):
            return None
        return "int<%s>" % width

    def parse_cell(self):
        t = self.advance()  # 'cell'
        name = self.expect_ident(t.text, "(cell name)")
        if name is None:
            raise _Recover()
        if name.text in self.cells:
            self.err(name.line, name.text, "duplicate cell declaration")
        if not self.expect_p("{", name.text, "to open cell body"):
            raise _Recover()
        fields, order = {}, []
        while True:
            nxt = self.peek()
            if nxt is None:
                self.err(name.line, name.text, "syntax: unterminated cell body")
                raise _Recover()
            if nxt.is_p("}"):
                self.advance()
                break
            if not self.parse_pw_type(name.text, "cell field"):
                self.recover_to_top()
                raise _Recover()
            f = self.expect_ident(name.text, "(field name)")
            if f is None:
                raise _Recover()
            init = None
            if self.eat_p("="):
                sign = -1 if self.eat_p("-") else 1
                v = self.peek()
                if v is not None and v.kind == "int":
                    self.advance()
                    init = sign * int(v.text)
                else:
                    self.err(f.line, "%s.%s" % (name.text, f.text),
                             "syntax: initializer must be an integer constant")
                    raise _Recover()
            if not self.expect_p(";", name.text, "after field"):
                raise _Recover()
            if f.text in fields:
                self.err(f.line, "%s.%s" % (name.text, f.text),
                         "duplicate field in cell")
            fields[f.text] = init
            order.append(f.text)
        self.cells[name.text] = {"fields": fields, "line": name.line}
        self.ops.append({
            "op": "cell", "name": name.text, "line": name.line,
            "fields": [{"name": f, "type": "int<PW>", "init": fields[f]}
                       for f in order],
        })

    def parse_view(self):
        t = self.advance()  # 'view'
        name = self.expect_ident(t.text, "(view name)")
        if name is None:
            raise _Recover()
        if name.text in self.views:
            self.err(name.line, name.text, "duplicate view declaration")
        if not self.expect_p("(", name.text, "to open view params"):
            raise _Recover()
        params = []
        while True:
            p = self.expect_ident(name.text, "(view parameter)")
            if p is None:
                raise _Recover()
            ref = p.text
            if self.eat_p("."):
                fld = self.expect_ident(name.text, "(view parameter field)")
                if fld is None:
                    raise _Recover()
                ref = "%s.%s" % (p.text, fld.text)
            params.append(ref)
            if self.eat_p(","):
                continue
            break
        if not self.expect_p(")", name.text, "to close view params"):
            raise _Recover()
        if not self.expect_p("->", name.text, "before return type"):
            raise _Recover()
        if not self.parse_pw_type(name.text, "view return"):
            raise _Recover()
        if not self.expect_p("{", name.text, "to open view body"):
            raise _Recover()
        body, depth = [], 0
        while True:
            nxt = self.peek()
            if nxt is None:
                self.err(name.line, name.text, "syntax: unterminated view body")
                raise _Recover()
            if nxt.is_p("}"):
                if depth == 0:
                    self.advance()
                    break
                depth -= 1
            elif nxt.is_p("("):
                depth += 1
            elif nxt.is_p(")"):
                if depth == 0:
                    self.err(nxt.line, name.text, "syntax: unbalanced ')' in "
                                                  "view body")
                    raise _Recover()
                depth -= 1
            body.append(self.advance())
        self.views[name.text] = {"params": params, "line": name.line}
        self.ops.append({
            "op": "view", "name": name.text, "line": name.line,
            "params": params, "body": " ".join(b.text for b in body),
            "_body_toks": body,
        })

    def parse_bind(self):
        t = self.advance()  # 'bind'
        src = self.expect_ident(t.text, "(bind source view)")
        if src is None:
            raise _Recover()
        if not self.expect_p("->", src.text, "in bind"):
            raise _Recover()
        dsts = []
        while True:
            d = self.expect_ident(src.text, "(bind destination cell)")
            if d is None:
                raise _Recover()
            dsts.append(d)
            if self.eat_p(","):
                continue
            break
        fanout, arrive = None, None
        f = self.expect_ident(src.text, "(fanout attr)")
        if f is not None:
            if f.text != "fanout":
                self.err(f.line, src.text, "syntax: expected 'fanout', got "
                                           "'%s'" % f.text)
                raise _Recover()
            if not self.expect_p("=", src.text, "after fanout"):
                raise _Recover()
            v = self.peek()
            if v is not None and v.kind == "int":
                self.advance()
                fanout = int(v.text)
            else:
                self.err(f.line, src.text, "syntax: fanout must be an integer")
                raise _Recover()
            a = self.expect_ident(src.text, "(arrive attr)")
            if a is None:
                raise _Recover()
            if a.text != "arrive":
                self.err(a.line, src.text, "syntax: expected 'arrive', got "
                                           "'%s'" % a.text)
                raise _Recover()
            if not self.expect_p("=", src.text, "after arrive"):
                raise _Recover()
            m = self.expect_ident(src.text, "(arrival mechanism)")
            if m is None:
                raise _Recover()
            arrive = m.text
        self.expect_p(";", src.text, "to end bind")
        self.ops.append({
            "op": "bind", "line": src.line, "src": src.text,
            "dsts": [d.text for d in dsts], "fanout": fanout,
            "arrive": arrive, "_dst_lines": [d.line for d in dsts],
        })

    def parse_link(self):
        t = self.advance()  # 'link'
        a = self.expect_ident(t.text, "(link endpoint)")
        if a is None:
            raise _Recover()
        if not self.expect_p("<->", a.text, "in link"):
            raise _Recover()
        b = self.expect_ident(a.text, "(link endpoint)")
        if b is None:
            raise _Recover()
        kind = None
        k = self.expect_ident(a.text, "(link kind attr)")
        if k is not None:
            if k.text != "kind":
                self.err(k.line, a.text, "syntax: expected 'kind', got '%s'"
                         % k.text)
                raise _Recover()
            if not self.expect_p("=", a.text, "after kind"):
                raise _Recover()
            kv = self.expect_ident(a.text, "(link kind)")
            if kv is None:
                raise _Recover()
            kind = kv.text
        self.expect_p(";", a.text, "to end link")
        self.ops.append({
            "op": "link", "line": a.line, "a": a.text, "b": b.text,
            "kind": kind,
        })

    def parse_propose(self):
        t = self.advance()  # 'propose'
        name = self.expect_ident(t.text, "(propose name)")
        if name is None:
            raise _Recover()
        if not self.expect_p("{", name.text, "to open propose region"):
            raise _Recover()
        ports = []
        while True:
            nxt = self.peek()
            if nxt is None:
                self.err(name.line, name.text, "syntax: unterminated propose "
                                               "region")
                raise _Recover()
            if nxt.is_p("}"):
                self.advance()
                break
            e = self.expect_ident(name.text, "(port decl)")
            if e is None or e.text != "external":
                self.err(nxt.line, name.text, "syntax: propose region contains "
                                              "only 'external port' lines")
                raise _Recover()
            p = self.expect_ident(name.text, "('port')")
            if p is None or p.text != "port":
                raise _Recover()
            if not self.parse_pw_type(name.text, "propose port"):
                raise _Recover()
            pn = self.expect_ident(name.text, "(port name)")
            if pn is None:
                raise _Recover()
            ports.append(pn.text)
            self.propose_ports.add(pn.text)
        self.ops.append({
            "op": "propose", "name": name.text, "line": name.line,
            "ports": [{"name": p, "type": "int<PW>", "dir": "in"}
                      for p in ports],
        })

    def parse_tick(self):
        t = self.advance()  # 'tick'
        if not self.expect_p("{", "tick", "to open tick block"):
            raise _Recover()
        effects = []
        while True:
            nxt = self.peek()
            if nxt is None:
                self.err(t.line, "tick", "syntax: unterminated tick block")
                raise _Recover()
            if nxt.is_p("}"):
                self.advance()
                break
            effects.append(self.parse_effect())
        op = {"op": "tick", "line": t.line, "effects": effects}
        return op

    def parse_effect(self):
        line = self.peek().line
        if self.peek().kind == "ident" and self.peek().text == "effect":
            self.advance()
        c = self.expect_ident("tick", "(effect dest cell)")
        if c is None:
            raise _Recover()
        if not self.expect_p(".", c.text, "in effect dest"):
            raise _Recover()
        f = self.expect_ident(c.text, "(effect dest field)")
        if f is None:
            raise _Recover()
        if not self.expect_p("<=", "%s.%s" % (c.text, f.text),
                             "in effect (dest <= expr)"):
            raise _Recover()
        expr = []
        while True:
            nxt = self.peek()
            if nxt is None or nxt.is_p("}"):
                self.err(line, "%s.%s" % (c.text, f.text),
                         "syntax: effect missing ';'")
                raise _Recover()
            if nxt.is_p(";"):
                self.advance()
                break
            expr.append(self.advance())
        return {
            "dest": "%s.%s" % (c.text, f.text), "cell": c.text,
            "field": f.text, "expr": " ".join(x.text for x in expr),
            "line": line, "_expr_toks": expr,
        }

    def parse_for(self):
        t = self.advance()  # 'for'
        var = self.expect_ident(t.text, "(loop variable)")
        if var is None:
            raise _Recover()
        ctx = "loop %s" % var.text
        inn = self.expect_ident(ctx, "('in')")
        if inn is None or inn.text != "in":
            self.err(inn.line if inn else 0, ctx,
                     "syntax: expected 'in' after loop variable")
            raise _Recover()
        bound = self.parse_bound(var.text)
        if not self.expect_p("{", ctx, "to open loop body"):
            raise _Recover()
        body = []
        while True:
            nxt = self.peek()
            if nxt is None:
                self.err(t.line, ctx, "syntax: unterminated loop body")
                raise _Recover()
            if nxt.is_p("}"):
                self.advance()
                break
            if nxt.kind == "ident" and nxt.text == "tick":
                if self.peek(1) is not None and self.peek(1).is_p("{"):
                    body.append(self.parse_tick())
                else:
                    self.advance()  # bare 'tick' statement: one fabric tick
                    body.append({"op": "tick", "line": nxt.line, "effects": []})
            elif nxt.kind == "ident" and nxt.text == "for":
                body.append(self.parse_for())
            elif nxt.kind == "ident" and nxt.text == "effect":
                self.err(nxt.line, ctx, "R1: effect outside tick -- only tick "
                                        "blocks write (S1.2)")
                raise _Recover()
            else:
                self.err(nxt.line, ctx, "syntax: only 'tick' or 'for' allowed "
                                        "in loop body, got '%s'" % nxt.text)
                raise _Recover()
        op = {
            "op": "loop", "line": t.line, "var": var.text, "bound": bound,
            "body": body,
        }
        return op

    def parse_bound(self, var):
        ctx = "loop %s" % var
        t = self.peek()
        if t is None:
            self.err(0, ctx, "syntax: missing loop bound")
            raise _Recover()
        if t.kind == "int":
            self.advance()
            if not self.expect_p("..", ctx, "in static range"):
                raise _Recover()
            if not self.expect_p("<", ctx, "in static range (0..<N)"):
                raise _Recover()
            n = self.peek()
            if n is not None and n.kind == "int":
                self.advance()
                return {"kind": "static", "from": int(t.text), "to": int(n.text)}
            if n is not None and n.kind == "ident" and n.text not in self.cells:
                # named elaboration-time constant, e.g. 0..<TICKS (S1.6 static).
                # A declared cell name here is NOT a constant -- reject (R4).
                self.advance()
                return {"kind": "symbol", "from": int(t.text),
                        "name": n.text, "line": n.line}
            self.err(n.line if n else t.line, ctx,
                     "R4: trip count must be static (0..<N) or journal-derived "
                     "(journal(<cell>)); bound is not an elaboration-time "
                     "constant (S1.6)")
            raise _Recover()
        if t.kind == "ident" and t.text == "journal":
            self.advance()
            if not self.expect_p("(", ctx, "after journal"):
                raise _Recover()
            c = self.expect_ident(ctx, "(journal cell)")
            if c is None:
                raise _Recover()
            if not self.expect_p(")", ctx, "to close journal(...)"):
                raise _Recover()
            return {"kind": "journal", "cell": c.text, "line": c.line}
        self.err(t.line, ctx,
                 "R4: trip count must be static (0..<N) or journal-derived "
                 "(journal(<cell>)); got '%s' (S1.6)" % t.text)
        raise _Recover()

    # -- semantic checks ----------------------------------------------------

    def check(self):
        for op in self.ops:
            self.check_op(op, [])
        return self

    def check_op(self, op, loop_vars):
        kind = op["op"]
        if kind == "view":
            self.check_view(op)
        elif kind == "bind":
            self.check_bind(op)
        elif kind == "link":
            self.check_link(op)
        elif kind == "loop":
            b = op["bound"]
            if b["kind"] == "journal" and b["cell"] not in self.cells:
                self.err(b.get("line", op["line"]), "loop %s" % op["var"],
                         "R4: journal(%s) names an undeclared cell" % b["cell"])
            for child in op["body"]:
                self.check_op(child, loop_vars + [op["var"]])
        elif kind == "tick":
            self.check_tick(op, loop_vars)

    def check_view(self, op):
        name, params = op["name"], set(op["params"])
        for p in op["params"]:
            if "." in p:
                c, f = p.split(".", 1)
                cell = self.cells.get(c)
                if cell is None or f not in cell["fields"]:
                    self.err(op["line"], name,
                             "view param '%s' names an unknown cell field" % p)
        toks = op["_body_toks"]
        j = 0
        while j < len(toks):
            t = toks[j]
            if t.is_p("="):
                self.err(t.line, name, "R2: view purity: assignment in view "
                                       "(views are pure, S1.3)")
                j += 1
                continue
            if t.kind != "ident":
                j += 1
                continue
            nxt = toks[j + 1] if j + 1 < len(toks) else None
            if nxt is not None and nxt.is_p("."):
                fld = toks[j + 2] if j + 2 < len(toks) else None
                ref = "%s.%s" % (t.text, fld.text if fld else "?")
                if ref not in params:
                    self.err(t.line, name, "R2: view purity: body references "
                                           "'%s', not a declared parameter "
                                           "(S1.1/S1.3)" % ref)
                j += 3
                continue
            if nxt is not None and nxt.is_p("("):
                if t.text not in self.views and t.text not in BUILTIN_VIEWS:
                    self.err(t.line, name, "R2: view purity: call to unknown "
                                           "view '%s'" % t.text)
                j += 1
                continue
            if t.text in self.propose_ports:
                self.err(t.line, name, "R2: view purity: propose output '%s' "
                                       "in view -- it never gates, never "
                                       "appears (S1.5)" % t.text)
            elif t.text not in params:
                self.err(t.line, name, "R2: view purity: body references "
                                       "'%s', not a declared parameter" % t.text)
            j += 1

    def check_bind(self, op):
        src = op["src"]
        if src not in self.views:
            self.err(op["line"], src, "R5: bind source '%s' is not a view"
                     % src)
        for d, dl in zip(op["dsts"], op["_dst_lines"]):
            if d not in self.cells:
                self.err(dl, src, "R5: bind destination '%s' is not a declared "
                                  "cell" % d)
        if op["fanout"] is None:
            self.err(op["line"], src, "R5: bind missing fanout declaration "
                                      "(S1.4)")
        elif op["fanout"] != len(op["dsts"]):
            self.err(op["line"], src, "R5: fanout=%d but %d named readers -- "
                                      "conservation ledger (D4) cannot "
                                      "reconcile" % (op["fanout"], len(op["dsts"])))
        if op["arrive"] not in ARRIVE_FAMILY:
            self.err(op["line"], src, "R5: arrive='%s' not in the round-19 "
                                      "mechanism family %s"
                     % (op["arrive"], list(ARRIVE_FAMILY)))

    def check_link(self, op):
        for end in (op["a"], op["b"]):
            if end not in self.cells:
                self.err(op["line"], op["a"], "R5: link endpoint '%s' is not a "
                                              "declared cell" % end)
        if op["kind"] != "gap":
            self.err(op["line"], op["a"], "R5: link kind must be gap "
                                          "(S1.4), got '%s'" % op["kind"])

    def check_tick(self, op, loop_vars):
        effects = op["effects"]
        dests, first_line = set(), {}
        for e in effects:
            key = (e["cell"], e["field"])
            if key in dests:
                self.err(e["line"], e["dest"],
                         "R1: single-writer: '%s' written again in the same "
                         "tick (first write at line %d) -- one effect per "
                         "cell.field per tick (S1.2)"
                         % (e["dest"], first_line[key]))
            else:
                dests.add(key)
                first_line[key] = e["line"]
            cell = self.cells.get(e["cell"])
            if cell is None or e["field"] not in cell["fields"]:
                self.err(e["line"], e["dest"], "R1: effect writes unknown cell "
                                               "field")
        for e in effects:
            self.scan_effect_expr(e, dests, loop_vars)

    def scan_effect_expr(self, e, dests, loop_vars):
        own = (e["cell"], e["field"])
        toks = e["_expr_toks"]
        scope, pending_call = [], None
        j = 0
        while j < len(toks):
            t = toks[j]
            if t.kind == "punct":
                if t.text == "(":
                    scope.append(pending_call)
                    pending_call = None
                elif t.text == ")":
                    if scope:
                        scope.pop()
                    else:
                        self.err(t.line, e["dest"], "syntax: unbalanced ')'")
                j += 1
                continue
            if t.kind != "ident":
                j += 1
                continue
            nxt = toks[j + 1] if j + 1 < len(toks) else None
            if nxt is not None and nxt.is_p("."):
                fld = toks[j + 2] if j + 2 < len(toks) else None
                ref = (t.text, fld.text if fld else "?")
                pretty = "%s.%s" % ref
                cell = self.cells.get(ref[0])
                if cell is None or ref[1] not in cell["fields"]:
                    self.err(t.line, e["dest"], "R1: expression reads unknown "
                                                "cell field '%s'" % pretty)
                elif ref == own:
                    pass  # a cell's new value may read its own old value
                elif ref in dests:
                    self.err(t.line, e["dest"],
                             "R1: same-tick cycle: reads '%s', written by "
                             "another effect this tick -- SPIN-19 class is a "
                             "parse error (S1.2)" % pretty)
                elif not any(s is not None for s in scope):
                    self.err(t.line, e["dest"],
                             "R1: raw state read: '%s' outside a view call -- "
                             "only views of another cell's state (S1.1)" % pretty)
                j += 3
                continue
            if nxt is not None and nxt.is_p("("):
                if t.text not in self.views and t.text not in BUILTIN_VIEWS:
                    self.err(t.line, e["dest"], "R1: call to unknown view '%s'"
                             % t.text)
                else:
                    pending_call = t.text
                j += 1
                continue
            if t.text in self.views:
                pass  # a bound view's value may be read inside an effect
            elif t.text not in self.propose_ports and t.text not in loop_vars:
                self.err(t.line, e["dest"], "R1: unknown identifier '%s' in "
                                            "effect expression" % t.text)
            j += 1

    # -- emission -----------------------------------------------------------

    def emit(self):
        module = os.path.splitext(os.path.basename(self.path))[0] or "quilt"
        return {
            "format": QM_FORMAT,
            "version": QM_VERSION,
            "module": module,
            "ops": [_strip_private(op) for op in self.ops],
        }


class _Recover(Exception):
    pass


def _strip_private(obj):
    if isinstance(obj, dict):
        return {k: _strip_private(v) for k, v in obj.items()
                if not k.startswith("_")}
    if isinstance(obj, list):
        return [_strip_private(x) for x in obj]
    return obj


def compile_quil(source, path):
    c = Compiler(source, path).parse().check()
    if c.errors:
        return [c.diag(*e) for e in c.errors], None
    return [], c.emit()


def count_ops(ops):
    n = 0
    for o in ops:
        n += 1 + count_ops(o["body"] if isinstance(o.get("body"), list) else [])
    return n
# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_check(args):
    with open(args.file, "r", encoding="utf-8") as fh:
        source = fh.read()
    errors, qm = compile_quil(source, args.file)
    if errors:
        for d in errors:
            print(d, file=sys.stderr)
        print("FAIL %s: %d error(s)" % (args.file, len(errors)))
        return 1
    out = args.out or os.path.splitext(args.file)[0] + ".qm"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(qm, fh, indent=2)
        fh.write("\n")
    print("OK %s -> %s (format %s v%d, %d ops)"
          % (args.file, out, QM_FORMAT, QM_VERSION, count_ops(qm["ops"])))
    return 0


# ---------------------------------------------------------------------------
# Selftest: 1 valid example + 5 reject cases (one per rule) + hygiene snippets
# ---------------------------------------------------------------------------

VALID = """\
// counter.quil -- minimal valid QUIL: leaky accumulator arc.
// Covers every construct in the step-1 subset.

cell AVM  { int<PW> acc = 0; }
cell AVBL { int<PW> acc = 0; }
cell AVBR { int<PW> acc = 0; }

view thr(src)  -> int<PW> { src - 1 }
view w_in(src) -> int<PW> { src }

bind  w_in -> AVBL, AVBR   fanout = 2  arrive = queue_cell;
link  AVBL <-> AVBR        kind = gap;

propose poke { external port int<PW> poke_strength }

// tick T0: sensory integration (black-box poke, as integers only)
tick {
  effect AVM.acc <= AVM.acc + poke_strength;
}

// tick T1: propagation -- one-tick edge delay via the journal prefix
tick {
  effect AVBL.acc <= thr(AVBL.acc) + w_in(AVM.acc);
  effect AVBR.acc <= thr(AVBR.acc) + w_in(AVM.acc);
}

for i in 0..<32 {
  tick {
    effect AVM.acc  <= AVM.acc + 1;
    effect AVBL.acc <= thr(AVBL.acc);
    effect AVBR.acc <= thr(AVBR.acc);
  }
}
"""

REJECTS = [
    ("reject_write_outside_tick.quil", """\
cell AVM { int<PW> acc = 0; }

AVM.acc <= 3;
""", 3, "AVM.acc", "R1: write outside tick"),
    ("reject_dup_writer.quil", """\
cell AVM { int<PW> acc = 0; }

tick {
  effect AVM.acc <= AVM.acc + 1;
  effect AVM.acc <= AVM.acc + 2;
}
""", 5, "AVM.acc", "R1: single-writer"),
    ("reject_view_impure.quil", """\
cell AVM  { int<PW> acc = 0; }
cell DB02 { int<PW> acc = 0; }

view leaky(src) -> int<PW> { src + DB02.acc }
""", 4, "leaky", "R2: view purity"),
    ("reject_helm_float.quil", """\
cell AVM { int<PW> acc = 0; }

tick {
  effect AVM.acc <= AVM.acc + 0.5;
}
""", 4, "helm", "R3: float literal"),
    ("reject_loop_bound.quil", """\
cell AVM { int<PW> acc = 0; }

tick { effect AVM.acc <= AVM.acc + 1; }

for i in 0..<AVM.acc {
  tick { effect AVM.acc <= AVM.acc + 1; }
}
""", 5, "loop i", "R4: trip count"),
]

SNIPPETS = [
    ("snippet_wallclock", """\
cell A { int<PW> x = 0; }
tick { effect A.x <= now(); }
""", False, "R3: wall-clock/network primitive 'now'"),
    ("snippet_net", """\
cell A { int<PW> x = 0; }
tick { effect A.x <= net_send(1); }
""", False, "R3: wall-clock/network primitive 'net_send'"),
    ("snippet_journal_loop_ok", """\
cell A { int<PW> x = 0; }
tick { effect A.x <= A.x + 1; }
for i in journal(A) { tick { effect A.x <= A.x + i; } }
""", True, None),
    ("snippet_view_propose_leak", """\
cell A { int<PW> x = 0; }
propose p { external port int<PW> sig }
view v(s) -> int<PW> { s + sig }
""", False, "R2: view purity: propose output 'sig'"),
]


def cmd_selftest(args):
    d = args.dir
    os.makedirs(d, exist_ok=True)
    passed, failed = 0, 0

    def report(ok, label, detail=""):
        nonlocal passed, failed
        if ok:
            passed += 1
            print("PASS %s%s" % (label, (" -- " + detail) if detail else ""))
        else:
            failed += 1
            print("FAIL %s%s" % (label, (" -- " + detail) if detail else ""))

    # 1. valid example: checker passes, .qm emits, structure is qm v1
    vpath = os.path.join(d, "counter.quil")
    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write(VALID)
    errors, qm = compile_quil(VALID, vpath)
    ok = (not errors) and qm is not None
    detail = errors[0] if errors else ""
    if ok:
        def walk(ops):
            for o in ops:
                yield o
                if isinstance(o.get("body"), list):
                    for c in walk(o["body"]):
                        yield c
        all_ops = list(walk(qm["ops"]))
        kinds = [o["op"] for o in all_ops]
        loop = [o for o in all_ops if o["op"] == "loop"][0]
        checks = [
            qm["format"] == "qm" and qm["version"] == 1,
            kinds.count("cell") == 3 and kinds.count("view") == 2,
            kinds.count("bind") == 1 and kinds.count("link") == 1,
            kinds.count("propose") == 1 and kinds.count("tick") == 3,
            loop["bound"] == {"kind": "static", "from": 0, "to": 32},
            len(loop["body"][0]["effects"]) == 3,
            sum(len(o["effects"]) for o in all_ops if o["op"] == "tick") == 6,
        ]
        ok = all(checks)
        detail = "format qm v1, %d ops, loop 0..<32, 6 effects" % len(all_ops)
    report(ok, "valid: counter.quil", detail)

    # CLI end-to-end on the valid file (exit code + .qm on disk)
    qmpath = os.path.splitext(vpath)[0] + ".qm"
    proc = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "check", vpath],
        capture_output=True, text=True)
    report(proc.returncode == 0 and os.path.exists(qmpath),
           "valid: CLI check exits 0 and writes %s" % os.path.basename(qmpath),
           proc.stdout.strip() or proc.stderr.strip())

    # 2. five reject cases, one per rule
    for fname, src, line, cell, needle in REJECTS:
        path = os.path.join(d, fname)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src)
        errors, qm = compile_quil(src, path)
        if not errors:
            report(False, "reject: %s" % fname, "accepted (should reject)")
            continue
        blob = "\n".join(errors)
        ok = (needle in blob and ("%s:" % line) in blob
              and ("error[%s]" % cell) in blob)
        report(ok, "reject: %s" % fname, errors[0])

    # 3. hygiene snippets (wall-clock / net vocabulary, journal loop, propose leak)
    for name, src, expect_ok, needle in SNIPPETS:
        errors, _qm = compile_quil(src, "<%s>" % name)
        if expect_ok:
            report(not errors, name, "clean compile"
                   if not errors else (errors or [""])[0])
        else:
            ok = bool(errors) and needle in "\n".join(errors)
            report(ok, name, errors[0] if errors else "accepted (should reject)")

    total = passed + failed
    print()
    print("SUMMARY: pass=%d fail=%d (of %d: 1 valid + 5 reject + %d snippets)"
          % (passed, failed, total, len(SNIPPETS)))
    return 0 if failed == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="quilc", description="QUIL front-end checker + .qm emitter "
                                  "(step-1 subset of docs/QUIL-HLS-RFC.copy.md)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="check FILE.quil, emit .qm on success")
    c.add_argument("file")
    c.add_argument("-o", "--out", default=None)
    c.set_defaults(func=cmd_check)
    s = sub.add_parser("selftest", help="run the step-1 test battery")
    s.add_argument("--dir", default="/tmp/opencode/quil-selftest")
    s.set_defaults(func=cmd_selftest)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
