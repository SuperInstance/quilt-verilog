#!/usr/bin/env python3
"""emith.py -- the tower pilot's L0 -> L2 emitter (SEMANTIC-TOWER section 3).

Reads one natural-language-anchored YAML cell descriptor (L0, the edit set:
io / raw / rendering / snap / tick) and emits a single C translation unit
(L2 middle layer) implementing, in order, the rendering chain:

    raw ADC read -> moving-median prefilter -> rendering equation (exact
    integer arithmetic on the cell's chosen basis) -> whole-unit
    quantization (Pythagorean snapping, 1-D case) -> deadband snap client
    (squared-form integer judge, posts only on SNAP) -> QUF state line.

The generated C is Arduino/ESP-IDF compatible, depends on nothing but
<stdint.h>/<stddef.h>, contains no floating-point types and no allocation
in the loop (state is a flat static image -- state-is-a-file). Its comments
quote the cell spec line-by-line: the middle layer IS the verification
surface; a human audits L2 against L0 without reading any Python.

Supported cell family (this pilot compiles exactly one shape):
  - one adc IO port, raw = integer millivolts supplied by platform glue
  - affine rendering equation  out = (in - K) * N / D  with integer K,N,D
  - basis exactness required: the psi range must land on the N/D lattice
  - moving_median prefilter, odd window 1..15
  - whole-unit deadband dial, squared-form judge

Usage:  emith.py CELL.yaml [-o OUT.c]     (default: emit to stdout)
Stdlib only.
"""

import argparse
import hashlib
import os
import re
import sys

MAX_WINDOW = 15


class CellError(Exception):
    """A cell-spec violation: the compiler may not proceed past these."""


# --------------------------------------------------------------------------
# tiny YAML-subset parser (block maps, block lists of maps, folded text,
# flow maps/lists, quoted/bare scalars, integers). Strict on purpose: the
# cell format IS the contract; anything it cannot express is rejected
# loudly rather than guessed.
# --------------------------------------------------------------------------

def _strip_comment(line):
    out = []
    q = None
    for i, ch in enumerate(line):
        if q:
            out.append(ch)
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def _split_flow(s):
    parts, depth, q, cur = [], 0, None, []
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            cur.append(ch)
        elif ch in "[{":
            depth += 1
            cur.append(ch)
        elif ch in "]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur))
    return [p for p in (x.strip() for x in parts) if p]


def _scalar(s, lineno):
    s = s.strip()
    if not s:
        return None
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    if s.startswith("["):
        if not s.endswith("]"):
            raise CellError("line %d: unterminated flow list" % lineno)
        return [_scalar(x, lineno) for x in _split_flow(s[1:-1])]
    if s.startswith("{"):
        if not s.endswith("}"):
            raise CellError("line %d: unterminated flow map" % lineno)
        out = {}
        for part in _split_flow(s[1:-1]):
            if ":" not in part:
                raise CellError("line %d: flow map item %r lacks ':'"
                                % (lineno, part))
            k, v = part.split(":", 1)
            out[k.strip()] = _scalar(v, lineno)
        return out
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _lex(path):
    with open(path, encoding="utf-8") as f:
        raw = f.readlines()
    entries = []
    for lineno, line in enumerate(raw, 1):
        text = _strip_comment(line)
        if not text.strip():
            continue
        indent = len(text) - len(text.lstrip(" "))
        body = text.strip()
        m = re.match(r"^-\s+(.*)$", body)
        if m:  # expand "key: x" list items into marker + body at indent+2
            entries.append((lineno, indent, "-"))
            if m.group(1).strip():
                entries.append((lineno, indent + 2, m.group(1).strip()))
        else:
            entries.append((lineno, indent, body))
    return entries


_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:(.*)$")


def _parse(entries, i, indent):
    if entries[i][2] == "-":
        out = []
        while i < len(entries) and entries[i][1] == indent \
                and entries[i][2] == "-":
            i += 1
            if i < len(entries) and entries[i][1] > indent:
                val, i = _parse(entries, i, entries[i][1])
            else:
                val = None
            out.append(val)
        return out, i
    out = {}
    while i < len(entries) and entries[i][1] == indent:
        lineno, _, text = entries[i]
        m = _KEY_RE.match(text)
        if not m:
            raise CellError("line %d: expected 'key: value', got %r"
                            % (lineno, text))
        key, rest = m.group(1), m.group(2).strip()
        i += 1
        if rest in (">", "|"):
            parts = []
            while i < len(entries) and entries[i][1] > indent:
                parts.append(entries[i][2])
                i += 1
            val = " ".join(parts) if rest == ">" else "\n".join(parts)
        elif rest == "":
            if i < len(entries) and entries[i][1] > indent:
                val, i = _parse(entries, i, entries[i][1])
            else:
                val = None
        else:
            val = _scalar(rest, lineno)
        out[key] = val
    if i < len(entries) and entries[i][1] > indent:
        raise CellError("line %d: unexpected indent" % entries[i][0])
    return out, i


def load_cell(path):
    entries = _lex(path)
    if not entries:
        raise CellError("%s: empty cell file" % path)
    doc, i = _parse(entries, 0, entries[0][1])
    if i != len(entries):
        raise CellError("line %d: trailing content" % entries[i][0])
    return doc


# --------------------------------------------------------------------------
# derive + validate: the compiler's zero-tolerance gates. Semantics (the
# edit set) is checked exactly; representation choices are left free.
# --------------------------------------------------------------------------

_EQ_RE = re.compile(
    r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)"
    r"\s*-\s*(\d+)\s*\)\s*\*\s*(\d+)\s*(?:/\s*(\d+))?$")
_BASIS_RE = re.compile(r"^1/(\d+)\s*psi$")


def _need(doc, key, where=""):
    if key not in doc or doc[key] is None:
        raise CellError("%s: missing '%s'" % (where, key))
    return doc[key]


def derive_spec(doc, where="cell"):
    s = {}
    s["name"] = _need(doc, "name", where)
    if not re.fullmatch(r"[a-z][a-z0-9-]*", s["name"]):
        raise CellError("name %r must be lowercase hyphen-words" % s["name"])
    s["cname"] = s["name"].replace("-", "_")
    s["desc"] = _need(doc, "description", where)

    io = _need(doc, "io", where)
    if not isinstance(io, list) or len(io) != 1:
        raise CellError("io: pilot compiles exactly one port")
    io0 = io[0]
    if not isinstance(io0, dict) or io0.get("kind") != "adc":
        raise CellError("io[0]: pilot supports kind: adc only")
    s["io_name"] = _need(io0, "name", "io[0]")
    s["io_kind"] = io0["kind"]
    s["io_unit"] = _need(io0, "unit", "io[0]")
    s["io_note"] = io0.get("note", "")

    raw = _need(doc, "raw", where)
    s["raw_quantity"] = _need(raw, "quantity", "raw")
    pre = _need(raw, "prefilter", "raw")
    if pre.get("kind") != "moving_median":
        raise CellError("raw.prefilter: pilot supports moving_median only")
    w = pre.get("window")
    if not isinstance(w, int) or not 1 <= w <= MAX_WINDOW or w % 2 == 0:
        raise CellError("raw.prefilter.window must be an odd int 1..%d"
                        % MAX_WINDOW)
    s["window"] = w

    r = _need(doc, "rendering", where)
    s["eq_text"] = _need(r, "equation", "rendering")
    m = _EQ_RE.match(s["eq_text"])
    if not m:
        raise CellError(
            "rendering.equation %r: pilot compiles the affine form "
            "'out = (in - K) * N [/ D]' with integer constants"
            % s["eq_text"])
    s["eq_out"], s["eq_in"], s["off_mv"], s["num"], den = m.groups()
    s["den"] = int(den) if den else 1
    s["off_mv"], s["num"] = int(s["off_mv"]), int(s["num"])
    if s["eq_in"] != "mV" or s["eq_out"] != "psi":
        raise CellError("rendering.equation: pilot family is psi-of-mV")
    if s["num"] <= 0 or s["den"] <= 0 or s["den"] % 2 != 0:
        raise CellError("rendering.equation: N>0 and even D>0 required "
                        "(D/2 drives round-to-nearest)")

    basis = _need(r, "basis", "rendering")
    mb = _BASIS_RE.match(str(basis))
    if not mb or int(mb.group(1)) != s["den"]:
        raise CellError("rendering.basis %r must be 1/%d psi to match the "
                        "equation" % (basis, s["den"]))
    s["basis"] = str(basis)

    rng = _need(r, "range_psi", "rendering")
    if not (isinstance(rng, list) and len(rng) == 2
            and all(isinstance(x, int) for x in rng) and 0 <= rng[0] < rng[1]):
        raise CellError("rendering.range_psi must be [min, max], 0<=min<max")
    s["psi_min"], s["psi_max"] = rng
    span_psi = rng[1] - rng[0]
    if (span_psi * s["den"]) % s["num"] != 0:
        raise CellError(
            "basis not exact: span %d psi does not land on the 1/%d-psi "
            "lattice under *%d/%d -- choose report units per SEMANTIC-TOWER "
            "5.3 instead of approximating" % (span_psi, s["den"], s["num"],
                                              s["den"]))
    s["span_mv"] = span_psi * s["den"] // s["num"]
    if s["psi_min"] != 0:
        raise CellError("pilot family clamps to a 0-based psi range")

    if r.get("quantize") != "whole_psi":
        raise CellError("rendering.quantize: pilot is whole_psi "
                        "(Pythagorean snapping, 1-D case)")
    db = _need(r, "deadband", "rendering")
    if db.get("unit") != "psi":
        raise CellError("rendering.deadband.unit must be psi")
    dwh = db.get("whole")
    if not isinstance(dwh, int) or dwh < 1:
        raise CellError("rendering.deadband.whole must be an int >= 1")
    s["deadband"] = dwh

    snap = _need(doc, "snap", where)
    s["endpoint"] = _need(snap, "twin_endpoint", "snap")
    s["dial"] = _need(snap, "dial", "snap")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", s["dial"]):
        raise CellError("snap.dial %r must be a lowercase identifier"
                        % s["dial"])

    tick = _need(doc, "tick", where)
    tp = tick.get("period_ms")
    if not isinstance(tp, int) or tp <= 0:
        raise CellError("tick.period_ms must be a positive int")
    s["tick_ms"] = tp

    for key, val in s.items():
        if isinstance(val, str):
            try:
                val.encode("ascii")
            except UnicodeEncodeError:
                raise CellError("%s: non-ASCII not allowed in cells "
                                "(generated C stays plain ASCII)" % key)
    return s


# --------------------------------------------------------------------------
# emission
# --------------------------------------------------------------------------

def _quote_row(label, value, width=64):
    """One 'label : value' comment row, wrapped and aligned."""
    pad = " " * 23
    head = " *   %-18s: " % label
    words, cur, out = str(value).split(), "", []
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        out.append(cur)
    lines = [head + out[0]] if out else [head.rstrip()]
    lines += [" *" + pad + l for l in out[1:]]
    return "\n".join(lines)


_BODY = r"""#include <stdint.h>
#include <stddef.h>

/* ============================================================== constants =
 * Every constant below is copied from the cell spec quoted in the file
 * header. Nothing numeric is invented here; the compiler only chose
 * representations, which is below the attention horizon (ST 1).
 */
#define TOWER_CELL_NAME       "@NAME@"
#define TOWER_TWIN_ENDPOINT   "@ENDPOINT@"
#define TOWER_DIAL_DEADBAND   "@DIAL@"
#define TOWER_MED_WINDOW      @WINDOW@   /* raw.prefilter: moving_median */
#define TOWER_EQ_OFFSET_mV    @OFFMV@    /* rendering.equation: @EQTEXT@ */
#define TOWER_EQ_NUM          @NUM@      /* numerator of the basis slope */
#define TOWER_EQ_DEN          @DEN@      /* rendering.basis: @BASIS@ */
#define TOWER_PSI_MIN         @PSIMIN@
#define TOWER_PSI_MAX         @PSIMAX@
#define TOWER_DEADBAND_WHOLE  @DEADBAND@ /* rendering.deadband.whole (D) */
#define TOWER_TICK_PERIOD_MS  @TICKMS@   /* tick.period_ms (loop config) */
#define TOWER_QUF_LINE_MAX    192

/* ================================================================== state =
 * State-is-a-file: flat static storage, nothing allocated in the loop
 * (ST 5.4: the no-allocation game rule is the QUF doctrine). The whole
 * image is renderable as one QUF-readable line by tower_quf_line(); every
 * stage of the chain is a visible field, which is the maintenance-zoom
 * invariant (ST 6): raw IO -> prefilter -> equation -> whole psi -> twin.
 */
static int32_t  med_win[TOWER_MED_WINDOW]; /* ring of raw mV samples     */
static uint8_t  med_len;                   /* samples held, < window     */
static uint8_t  med_idx;                   /* next ring slot to write    */
static int32_t  st_raw_mV;                 /* latest raw sample          */
static int32_t  st_med_mV;                 /* median of the window       */
static int32_t  st_psi80;                  /* rendered, @BASIS@          */
static int32_t  st_psi;                    /* whole psi (report lattice) */
static int32_t  st_twin;                   /* what we believe the twin   */
static uint8_t  st_twin_known;             /* 0 until first snap syncs   */
static uint32_t st_posts;                  /* snaps posted to endpoint   */
static int32_t  st_snap_debt;              /* sum of corrections (ST 5.4)*/
static uint32_t st_tick;                   /* qm_tick count              */

/* ========================================================= public surface */
#if defined(__GNUC__)
#define TOWER_WEAK __attribute__((weak))
#else
#define TOWER_WEAK
#endif

TOWER_WEAK int32_t tower_adc_read_mV(void);                 /* glue: raw */
TOWER_WEAK void    tower_twin_post(const char *, const char *); /* glue  */
void     tower_tick(void);                       /* one fixed timestep   */
void     tower_reset(void);                      /* zero the image      */
size_t   tower_quf_line(char *buf, size_t n);    /* QUF state line      */
int32_t  tower_raw_mV(void);
int32_t  tower_med_mV(void);
int32_t  tower_psi80(void);
int32_t  tower_psi_whole(void);
int32_t  tower_twin_psi(void);
uint32_t tower_posts(void);
int32_t  tower_snap_debt(void);
uint32_t tower_ticks(void);
void     tower_twin_set_belief(int32_t v);       /* host/game-side seam */

/* ============================================================== raw IO ====
 * io[0]: @IONAME@ -- kind @IOKIND@, unit @IOUNIT@ (@IONOTE@)
 * raw.quantity: @RAWQ@
 * The cell sees ONLY integer millivolts. Counts-to-mV and pin setup are
 * platform concerns, below the horizon; override the weak default in a
 * board file:
 *   Arduino-ESP32 : return analogReadMilliVolts(@IONAME@);
 *   ESP-IDF       : adc_oneshot_read + counts * VREF_mV / 4095 (integer)
 */
TOWER_WEAK int32_t tower_adc_read_mV(void)
{
    return 0; /* board glue must override */
}

/* ==================================================== twin transport ======
 * snap.twin_endpoint: @ENDPOINT@
 * Posting happens ONLY on a SNAP verdict, and the payload is the QUF
 * state line itself -- one line, both books, nonce = the tick count (ST
 * 5.4). Redelivery safety is the ledger's job (idempotence, FOUNDATION
 * D3), not this cell's: the transport never blocks, never retries.
 * Override with a strong definition (UART line, MQTT, HTTP, fabric flit).
 */
TOWER_WEAK void tower_twin_post(const char *endpoint, const char *state_line)
{
    (void)endpoint;
    (void)state_line;
}

/* ============================================================ prefilter ===
 * raw.prefilter: moving_median, window @WINDOW@
 * Median of the last @WINDOW@ integer mV samples: an exact integer
 * statistic. Fewer than half the window corrupt keeps the median
 * unchanged -- one ignition spike moves the mean but cannot move this
 * median at all. Sorts a fixed stack copy; no allocation in the loop.
 */
static int32_t median_of(int32_t *a, uint8_t n)
{
    uint8_t i;
    for (i = 1; i < n; i++) {
        int32_t k = a[i];
        int8_t j = (int8_t)(i - 1);
        while (j >= 0 && a[j] > k) {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = k;
    }
    return a[n / 2]; /* window is odd (spec): a real sample, never a mean */
}

static int32_t prefilter_push(int32_t raw_mV)
{
    int32_t win[TOWER_MED_WINDOW];
    uint8_t i;
    med_win[med_idx] = raw_mV;
    med_idx = (uint8_t)((med_idx + 1u) % TOWER_MED_WINDOW);
    if (med_len < TOWER_MED_WINDOW) {
        med_len++;
    }
    for (i = 0; i < TOWER_MED_WINDOW; i++) {
        win[i] = med_win[i];
    }
    return median_of(win, med_len);
}

/* ==================================================== rendering equation ==
 * rendering.equation: @EQTEXT@
 * rendering.basis:    @BASIS@ -- span @SPANMV@ mV * @NUM@/@DEN@ = @SPANPSI@ psi
 *                     exactly; the calibration is exact integer arithmetic
 *                     by choice of unit (ST 1's basis trick).
 * Step 1 keeps @DEN@ths of a psi -- psi80 = (mV - @OFFMV@) * @NUM@ -- and
 * never divides: the multiply is exact on the lattice.
 * rendering.range_psi: [@PSIMIN@, @PSIMAX@] -- clamped here, before any
 * rounding, so the report never leaves the transducer's stated span.
 */
static int32_t render_psi80(int32_t mV)
{
    int32_t psi80 = (mV - TOWER_EQ_OFFSET_mV) * TOWER_EQ_NUM;
    if (psi80 < TOWER_PSI_MIN * TOWER_EQ_DEN) {
        psi80 = TOWER_PSI_MIN * TOWER_EQ_DEN;
    }
    if (psi80 > TOWER_PSI_MAX * TOWER_EQ_DEN) {
        psi80 = TOWER_PSI_MAX * TOWER_EQ_DEN;
    }
    return psi80;
}

/* Step 2 -- rendering.quantize: whole_psi. Pythagorean snapping, 1-D case
 * (ST 5.3): the report unit is chosen so the quantity sits ON the
 * lattice; quantizing to whole psi is round-to-nearest on it,
 * (psi80 + D/2)/D, exact integer arithmetic. psi80 >= 0 after the clamp,
 * so C truncation equals floor. No approximation anywhere: no floating
 * point because none is needed.
 */
static int32_t quantize_whole_psi(int32_t psi80)
{
    return (psi80 + TOWER_EQ_DEN / 2) / TOWER_EQ_DEN;
}

/* ==================================================== deadband judge ======
 * rendering.deadband: @DEADBAND@ whole psi -- dial @DIAL@ (snap.dial)
 * FOUNDATION D2 with the integer metric and r = D, polarity inverted
 * (ST 5.2): WITHIN while d(psi, twin) <= D -- the deadband is a Schmitt
 * trigger against chatter -- SNAP when d > D. Judged in SQUARED form,
 * d*d > D*D: the comparison is monotone, needs no square root, and no
 * floating point. The weakest substrate sets the arithmetic (ST 5.3):
 * this exact integer comparison is what BOTH members of the snap pair
 * run, or the verdict itself could diverge across substrates.
 */
static int judge_snap(int32_t psi, int32_t twin, uint8_t twin_known)
{
    int32_t d;
    if (!twin_known) {
        return 1; /* first sighting: syncing the pair is a snap */
    }
    d = psi - twin;
    if (d < 0) {
        d = -d;
    }
    return d * d > (int32_t)TOWER_DEADBAND_WHOLE * TOWER_DEADBAND_WHOLE;
}

/* ========================================================= QUF state line =
 * The whole cell image as one line of key=value pairs -- the text form of
 * what a QUF container carries (all values integers; no floating point in
 * fleet state, QUF-SPEC 4). This is the maintenance surface (ST 6): the
 * entire rendering chain readable in one line, every stage auditable
 * against the equation quoted above. Keys are stable; consumers skip
 * unknown keys per QUF-SPEC 8. Integer formatting is hand-rolled: no
 * stdio, so the loop stays dependency-free and allocation-free.
 */
static char *quf_str(char *p, char *end, const char *s)
{
    while (p < end && *s != '\0') {
        *p++ = *s++;
    }
    return p;
}

static char *quf_u32(char *p, char *end, uint32_t v)
{
    char tmp[10];
    uint8_t i = 0;
    do {
        tmp[i++] = (char)('0' + (v % 10u));
        v /= 10u;
    } while (v != 0u);
    while (i != 0u && p < end) {
        *p++ = tmp[--i];
    }
    return p;
}

static char *quf_i32(char *p, char *end, int32_t v)
{
    char tmp[11];
    uint8_t i = 0;
    uint32_t u = (v < 0) ? (uint32_t)(-(int64_t)v) : (uint32_t)v;
    do {
        tmp[i++] = (char)('0' + (u % 10u));
        u /= 10u;
    } while (u != 0u);
    if (v < 0 && p < end) {
        *p++ = '-';
    }
    while (i != 0u && p < end) {
        *p++ = tmp[--i];
    }
    return p;
}

size_t tower_quf_line(char *buf, size_t n)
{
    char *p = buf;
    char *end = buf + n - 1u;
    p = quf_str(p, end, "QUF1 cell=" TOWER_CELL_NAME);
    p = quf_str(p, end, " tick=");       p = quf_u32(p, end, st_tick);
    p = quf_str(p, end, " raw_mV=");     p = quf_i32(p, end, st_raw_mV);
    p = quf_str(p, end, " med_mV=");     p = quf_i32(p, end, st_med_mV);
    p = quf_str(p, end, " psi80=");      p = quf_i32(p, end, st_psi80);
    p = quf_str(p, end, " psi=");        p = quf_i32(p, end, st_psi);
    p = quf_str(p, end, " twin=");       p = quf_i32(p, end, st_twin);
    p = quf_str(p, end, " " TOWER_DIAL_DEADBAND "=");
    p = quf_i32(p, end, TOWER_DEADBAND_WHOLE);
    p = quf_str(p, end, " posts=");      p = quf_u32(p, end, st_posts);
    p = quf_str(p, end, " snap_debt=");  p = quf_i32(p, end, st_snap_debt);
    if (p > end) {
        p = end;
    }
    *p = '\0';
    return (size_t)(p - buf);
}

/* ================================================================ qm_tick =
 * One fixed-timestep iteration of the whole chain (tick.period_ms =
 * @TICKMS@ lives in the platform loop; the cell itself is cadence-agnostic
 * and deterministic per tick -- same delta-t every tick, game discipline
 * as cell anatomy, ST 5.4). Sense -> prefilter -> render -> quantize ->
 * judge -> snap. Nothing else happens, and nothing allocates.
 */
void tower_tick(void)
{
    st_tick++;
    st_raw_mV = tower_adc_read_mV();
    st_med_mV = prefilter_push(st_raw_mV);
    st_psi80 = render_psi80(st_med_mV);
    st_psi = quantize_whole_psi(st_psi80);
    if (judge_snap(st_psi, st_twin, st_twin_known)) {
        /* SNAP: reality wins (ST 5.1). Set the twin's belief to the
         * sensor value, book the drift as snap debt (the ST 5.4
         * account), and post the state line: the post IS the ledger
         * entry -- one line, both books. */
        int32_t d = st_twin_known ? (st_psi - st_twin) : 0;
        if (d < 0) {
            d = -d;
        }
        st_snap_debt += d;
        st_twin = st_psi;
        st_twin_known = 1;
        st_posts++;
        {
            char line[TOWER_QUF_LINE_MAX];
            (void)tower_quf_line(line, sizeof line);
            tower_twin_post(TOWER_TWIN_ENDPOINT, line);
        }
    }
}

/* ================================================================ reset ==
 * Zero the image (warm-start shape: what a QUF loader would restore).
 * The twin belief is forgotten, so the first tick after reset syncs it.
 */
void tower_reset(void)
{
    uint8_t i;
    for (i = 0; i < TOWER_MED_WINDOW; i++) {
        med_win[i] = 0;
    }
    med_len = 0;
    med_idx = 0;
    st_raw_mV = 0;
    st_med_mV = 0;
    st_psi80 = 0;
    st_psi = 0;
    st_twin = 0;
    st_twin_known = 0;
    st_posts = 0;
    st_snap_debt = 0;
    st_tick = 0;
}

/* ============================================================= accessors =
 * qm_view surface (FOUNDATION D4): bounded-freshness reads of the static
 * image; pure, always consistent, never torn.
 */
int32_t  tower_raw_mV(void)    { return st_raw_mV; }
int32_t  tower_med_mV(void)    { return st_med_mV; }
int32_t  tower_psi80(void)     { return st_psi80; }
int32_t  tower_psi_whole(void) { return st_psi; }
int32_t  tower_twin_psi(void)  { return st_twin; }
uint32_t tower_posts(void)     { return st_posts; }
int32_t  tower_snap_debt(void) { return st_snap_debt; }
uint32_t tower_ticks(void)     { return st_tick; }

/* Host/game-side seam: pretend the twin now holds v. The real pair learns
 * this from the game's own traffic; the verification harness uses it to
 * stage deadband tests. Not reachable from tower_tick -- belief moves
 * only on SNAP.
 */
void tower_twin_set_belief(int32_t v)
{
    st_twin = v;
    st_twin_known = 1;
}
"""


def _c_str(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def emit_c(spec, src_name, cell_sha16):
    rows = [
        ("name", spec["name"]),
        ("description", spec["desc"]),
        ("io[0]", "%s kind=%s unit=%s -- %s" % (spec["io_name"],
                                                spec["io_kind"],
                                                spec["io_unit"],
                                                spec["io_note"])),
        ("raw.quantity", spec["raw_quantity"]),
        ("raw.prefilter", "moving_median window=%d" % spec["window"]),
        ("rendering.equation", spec["eq_text"]),
        ("rendering.basis", "%s -- span %d mV * %d/%d = %d psi exactly"
         % (spec["basis"], spec["span_mv"], spec["num"], spec["den"],
            spec["psi_max"] - spec["psi_min"])),
        ("rendering.range", "psi in [%d, %d]" % (spec["psi_min"],
                                                 spec["psi_max"])),
        ("rendering.quantize", "whole_psi (Pythagorean snapping, 1-D)"),
        ("rendering.deadband", "%d whole psi (unit psi)" % spec["deadband"]),
        ("snap.twin_endpoint", spec["endpoint"]),
        ("snap.dial", spec["dial"]),
        ("tick.period_ms", str(spec["tick_ms"])),
    ]
    quoted = "\n".join(_quote_row(label, value) for label, value in rows)

    header = """\
/*
 * tower_%s.c -- L2 C middle layer for the L0 cell "%s".
 * GENERATED by tools/tower/emith.py from %s -- do not edit by hand;
 * edit the cell, regenerate, and re-run tools/tower/verify.py.
 * SEMANTIC-TOWER 3: the middle layer is the verification surface, so the
 * entire cell spec is quoted below; each code section quotes the line it
 * implements. A human audits this file against L0 without reading Python.
 *
 * Provenance (ST 4.3): source %s sha256/16 %s
 *
 * --------------------------- the cell, quoted verbatim --------------------
%s
 * --------------------------------------------------------------------------
 *
 * Target substrate note (ST 7 table, the rows this family consumes):
 * numeric discipline = integer-only (no FPU assumed, weakest-substrate
 * rule ST 5.3); allocation policy = none-in-loop, flat static state;
 * tick = caller-driven fixed timestep; IO surface = one integer-mV adapter
 * (weak); verification harness = tools/tower/verify.py (host gcc).
 *
 * Contract, one line (ST 5.5): agree-to-within-D, snap-on-exceed,
 * reality-wins, log-both-books, all-integer, fixed-tick. Concretely:
 *   - no floating-point types anywhere in this file, on purpose;
 *   - no allocation inside the tick; state is a flat static image;
 *   - the snap judge compares in squared form (ST 5.2), no square root;
 *   - posts happen only on SNAP, and carry the QUF state line (ST 5.4/6).
 */
""" % (spec["cname"], spec["name"], src_name, src_name, cell_sha16, quoted)

    subs = {
        "NAME": _c_str(spec["name"]),
        "ENDPOINT": _c_str(spec["endpoint"]),
        "DIAL": _c_str(spec["dial"]),
        "WINDOW": str(spec["window"]),
        "OFFMV": str(spec["off_mv"]),
        "NUM": str(spec["num"]),
        "DEN": str(spec["den"]),
        "BASIS": _c_str("1/%d psi" % spec["den"]),
        "PSIMIN": str(spec["psi_min"]),
        "PSIMAX": str(spec["psi_max"]),
        "DEADBAND": str(spec["deadband"]),
        "TICKMS": str(spec["tick_ms"]),
        "EQTEXT": _c_str(spec["eq_text"]),
        "SPANMV": str(spec["span_mv"]),
        "SPANPSI": str(spec["psi_max"] - spec["psi_min"]),
        "IONAME": _c_str(spec["io_name"]),
        "IOKIND": _c_str(spec["io_kind"]),
        "IOUNIT": _c_str(spec["io_unit"]),
        "IONOTE": _c_str(spec["io_note"]),
        "RAWQ": _c_str(spec["raw_quantity"]),
    }
    body = _BODY
    for k, v in subs.items():
        body = body.replace("@" + k + "@", v)
    if "@" in body:
        pos = body.index("@")
        raise CellError("unsubstituted @token@ near: %r" % body[pos:pos + 40])
    return header + body


def compile_cell(path):
    with open(path, "rb") as f:
        sha16 = hashlib.sha256(f.read()).hexdigest()[:16]
    doc = load_cell(path)
    spec = derive_spec(doc)
    return spec, emit_c(spec, os.path.basename(path), sha16)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="emith.py",
        description="emit the L2 C middle layer for one L0 tower cell")
    ap.add_argument("cell", help="cell descriptor YAML (the edit set)")
    ap.add_argument("-o", "--out", default="-",
                    help="output .c path (default stdout)")
    args = ap.parse_args(argv)
    try:
        spec, c_text = compile_cell(args.cell)
    except CellError as e:
        print("emith: REJECT %s: %s" % (args.cell, e), file=sys.stderr)
        return 1
    sys.stderr.write(
        "emith: ACCEPT %s -> %s (span %d mV over %d psi on 1/%d-psi basis, "
        "exact; median window %d, deadband %d whole psi)\n"
        % (args.cell, "tower_%s.c" % spec["cname"], spec["span_mv"],
           spec["psi_max"] - spec["psi_min"], spec["den"], spec["window"],
           spec["deadband"]))
    if args.out == "-":
        sys.stdout.write(c_text)
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(c_text)
        sys.stderr.write("emith: wrote %s (%d bytes)\n"
                         % (args.out, len(c_text.encode())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
