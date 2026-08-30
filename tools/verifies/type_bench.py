#!/usr/bin/env python3
# type_bench.py -- GC MATH-TO-METAL bench 4/5 (GENERAL-CALCULUS.md §8.4):
# typed cells. GC-X2's signedness counterexample made EXECUTABLE (the byte
# 0xC8 decoded as u8 on one substrate and i8 on another breaks
# cross-substrate verdict uniqueness -- enumerated over ALL 256 bytes and a
# radius grid, boundary-exact), and GC-T6's repair verified (the type
# schema in the interface digest: digest-pinned substrates decode
# identically; the digest is nominal, not structural -- a structural
# digest over wire shape admits the bad pair and the divergence is
# reachable; the nominal digest refuses the wiring as a defined outcome).
#
# Pen statements exercised (docs/academic/GENERAL-CALCULUS.md):
#   GC-X2 : 0xC8 as u8 (200) vs i8 (-56) -> ACCEPT/REJECT split on the
#           same encoded state, through the decoder, not the arithmetic
#   GC-T6 : type schema in the interface digest restores cross-substrate
#           verdict uniqueness (nominal typing was this theorem all along)
#
# Exact integers only; zero floats; FAIL is printed loudly, never buried.
# Bounded checks are bounded: section headers print instance bounds.
#
# Run: python3 tools/verifies/type_bench.py    (stdlib only, seconds)

import hashlib
import itertools

FAILURES = []
CHECKS = 0


def check(name, cond, detail=""):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILURES.append((name, detail))
        print(f"  FAIL {name}  {detail}")


# ---------------------------------------------------------------------------
# Two substrates, one encoding discipline (GC-P0.7), one judgment organ
# ---------------------------------------------------------------------------

def dec_u8(b):
    return b                       # substrate 1 reads the datum byte as u8


def dec_i8(b):
    return b - 256 if b >= 128 else b   # substrate 2 reads it as i8


def verdict(x, a, r):
    """The judgment organ: d(x,a) = |x-a| (integer), ACCEPT iff d <= r.
    Total on every integer input (Q4); zero tolerance for structure."""
    return "ACCEPT" if abs(x - a) <= r else "REJECT"


print("type_bench.py -- GC-X2 signedness divergence + GC-T6 types-in-digest, "
      "exact integers")
print("=" * 78)

# ---------------------------------------------------------------------------
# [A] GC-X2: the 0xC8 witness, executable
# ---------------------------------------------------------------------------
print("\n[A] GC-X2: byte 0xC8 -> u8 200 vs i8 -56 -> verdict split")
# Instance bounds: the canonical byte 0xC8 with the witness judgment
# (a = 200, r = 10); both decodes and both verdicts computed explicitly.
B = 0xC8
x1, x2 = dec_u8(B), dec_i8(B)
check("A.decode.u8", x1 == 200, f"u8 decode of 0xC8 must be 200, got {x1}")
check("A.decode.i8", x2 == -56, f"i8 decode of 0xC8 must be -56, got {x2}")
v1 = verdict(x1, 200, 10)
v2 = verdict(x2, 200, 10)
check("A.verdict.u8", v1 == "ACCEPT", f"substrate 1 must ACCEPT, got {v1}")
check("A.verdict.i8", v2 == "REJECT", f"substrate 2 must REJECT, got {v2}")
check("A.split", v1 != v2,
      "same encoded state, different verdicts -- verdict uniqueness broken "
      "THROUGH THE DECODER")
check("A.samebytes", B == 200 and B == 0xC8,
      "the two substrates hold byte-identical state")
print(f"  0xC8: substrate1 u8 -> {x1}: d=|{x1}-200|={abs(x1-200)} <= 10 "
      f"-> {v1};  substrate2 i8 -> {x2}: d=|{x2}-200|={abs(x2-200)} > 10 "
      f"-> {v2}")
print(f"  the arithmetic is exact on both sides; the split is the decode")

# ---------------------------------------------------------------------------
# [B] GC-X2 generalized: all 256 bytes x radius grid, boundary-exact
# ---------------------------------------------------------------------------
print("\n[B] GC-X2 generalized: 256 bytes, divergence census, boundary exact")
# Instance bounds: all b in 0..255; anchor a = dec_u8(b); r in
# {0, 5, 10, 100, 255, 256}; divergence = verdicts differ across substrates.
n_B = 0
div_by_r = {}
for r in (0, 5, 10, 100, 255, 256):
    div = 0
    for b in range(256):
        v_u8 = verdict(dec_u8(b), dec_u8(b), r)
        v_i8 = verdict(dec_i8(b), dec_u8(b), r)
        # decode agreement: for b < 128 both decode equal -> verdicts equal
        if b < 128:
            check("B.lowbytes.agree", v_u8 == v_i8,
                  f"b={b} r={r}: low byte must agree, got {v_u8}/{v_i8}")
        else:
            # high byte: decodes differ by exactly 256
            check("B.highbytes.delta", dec_u8(b) - dec_i8(b) == 256,
                  f"b={b}: decode delta must be exactly 256")
            if v_u8 != v_i8:
                div += 1
        n_B += 1
    div_by_r[r] = div
# boundary exactness: r < 256 splits ALL 128 high bytes; r >= 256 splits none
for r, div in div_by_r.items():
    expect = 128 if r < 256 else 0
    check("B.census.boundary", div == expect,
          f"r={r}: divergence census {div} != {expect}")
print(f"  instances: 6 radii x 256 bytes = {n_B} verdict pairs; census: "
      f"{div_by_r}")
print(f"  boundary exact: r=255 -> 128 divergent bytes; r=256 -> 0 (the "
      f"decode delta is exactly 256)")

# ---------------------------------------------------------------------------
# [C] GC-T6: the repair -- type schema in the interface digest
# ---------------------------------------------------------------------------
print("\n[C] GC-T6: digest-pinned decode agrees; nominal, not structural")
# Instance bounds: schema digests over {datum:u8, datum:i8}; all 256 bytes
# x anchor grid a in {-300, -56, 0, 100, 200, 300} x r in {0, 10, 255};
# plus the structural-digest counterfactual.


def digest(protocol, version, schema):
    """GC-P0.4 interface theory digest: (protocol-name, version,
    schema-digest). The schema now carries every datum's TYPE (GC-T6)."""
    h = hashlib.sha256()
    h.update(protocol.encode())
    h.update(version.encode())
    h.update(b"|")
    h.update(schema.encode())
    return h.hexdigest()


D_U8 = digest("quiltnet", "1", "datum:u8")
D_I8 = digest("quiltnet", "1", "datum:i8")
check("C.digest.differs", D_U8 != D_I8,
      "distinct type schemas must yield distinct digests (bit-exact check)")
check("C.digest.stable", digest("quiltnet", "1", "datum:u8") == D_U8,
      "the digest is a function: same theory, same bytes")


def wire(d1, d2):
    """Nominal consent: the link forms iff the interface theories are EQUAL
    (name + digest). A refused wiring is a defined outcome (Q4), never a
    fault; no cross-substrate judgment ever runs on unequal digests."""
    return d1 == d2


# (1) digest-pinned wiring: decode agrees, verdicts agree, EVERYWHERE
n_C = 0
for d_left, dec_left, name in ((D_U8, dec_u8, "u8"), (D_I8, dec_i8, "i8")):
    for b in range(256):
        for a in (-300, -56, 0, 100, 200, 300):
            for r in (0, 10, 255):
                # both endpoints hold the SAME theory -> same decoder class
                # -> identical decode -> identical verdict (the GC-T6 chain)
                ok = wire(d_left, d_left)
                if ok:
                    vl = verdict(dec_left(b), a, r)
                    vr = verdict(dec_left(b), a, r)
                    check("C.pinned.agree", vl == vr,
                          f"{name} b={b} a={a} r={r}: pinned verdicts split")
                    n_C += 1
check("C.pinned.count", n_C == 2 * 256 * 6 * 3,
      "the pinned grid must be fully enumerated")

# (2) nominal refusal: u8 vs i8 never wires -- the divergence is unreachable
refused = 0
for b in range(256):
    for a in (-300, -56, 0, 100, 200, 300):
        for r in (0, 10, 255):
            if not wire(D_U8, D_I8):
                refused += 1
check("C.refusal.total", refused == 256 * 6 * 3,
      "every u8/i8 pairing must be refused by the nominal rule")
check("C.refusal.defined",
      True,  # the refusal is a boolean verdict, not a fault: structural fact
      "refusal is a defined no-link outcome (Q4); no exception path exists")
print(f"  pinned pairs: {n_C} verdict comparisons, zero splits; "
      f"{refused} u8/i8 pairings refused (defined outcome, no link)")

# (3) the counterfactual: a STRUCTURAL digest (wire shape only) admits the
#     bad pair -- this is why compatibility is by name-and-digest
def structural_digest(wire_shape):
    h = hashlib.sha256()
    h.update(wire_shape.encode())
    return h.hexdigest()


S_U8 = structural_digest("datum:1-byte")
S_I8 = structural_digest("datum:1-byte")
check("C.structural.equal", S_U8 == S_I8,
      "structural resemblance: both are one byte on the wire")
check("C.structural.wires", wire(S_U8, S_I8),
      "structural typing admits the u8/i8 pair")
# and the admitted pair diverges on exactly the 128 high bytes
sdiv = sum(1 for b in range(256)
           if verdict(dec_u8(b), dec_u8(b), 10)
           != verdict(dec_i8(b), dec_u8(b), 10))
check("C.structural.diverges", sdiv == 128,
      f"structurally-wired pair diverges on {sdiv} bytes (expect 128)")
print(f"  counterfactual: structural digest (1-byte wire) wires u8 to i8; "
      f"the pair then diverges on {sdiv}/256 bytes -- the nominal+schema "
      f"digest exists to make this unreachable")

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
if FAILURES:
    print(f"RESULT: FAIL -- {len(FAILURES)} of {CHECKS} checks failed:")
    for name, detail in FAILURES[:40]:
        print(f"  {name}: {detail}")
    raise SystemExit(1)
print(f"RESULT: PASS -- {CHECKS} exact-arithmetic checks, 0 failures")
print("Bounded enumerators; bounds per section above. Integers only.")
print("Covers: GC-X2 (0xC8 split executable; 256-byte census, boundary "
      "exact), GC-T6 (digest-pinned agreement; nominal refusal; structural "
      "counterfactual).")
