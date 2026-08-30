#!/usr/bin/env python3
"""quf_epoch.py -- QUF-FORGETTING-V1 PRODUCER (reference-tooling lane).

Builds self-authenticating epoch archives per docs/QUF-FORGETTING-V1.md:
custody section + epoch.<N> sections (48B header + payload + 32B HMAC seal),
on top of the v1 base container produced by tools/quf.py (quf.build/rebuild).

This is the PRODUCER side of the v1-consumer independence test. The consumer
(hostile-consumer/v1_consumer) is written from the spec alone and never sees
this file. quf.py + this script = legitimate reference producer.

Stdlib only. Python >= 3.8.

Commands:
  gen   OUTDIR N_EPOCHS      generate corpus: base + sealed file (N epochs) + keys
  forge KIND OUTDIR          generate one forged variant (see main() for KINDs)
"""

import argparse
import hmac
import hashlib
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quf  # noqa: E402  (producer lane: allowed to use the reference impl)

DOMAIN = b"QUF-EPOCH-V1\x00"
EPCH_MAGIC = b"EPCH"

# Deterministic corpus keys (test vectors, not secrets).
ARCHIVE_KEY = bytes.fromhex("11" * 32)   # the real archive key
WRONG_KEY = bytes.fromhex("aa" * 32)     # attacker key
KEY_ID = bytes.fromhex("0123456789abcdef0123456789abcdef")[:16]
CEREMONY_TICK = 7


def seal_epoch(epoch_no, status, created_tick, payload_kind, primer_addr,
               payload, key):
    msg = (DOMAIN + struct.pack("<I", epoch_no) + bytes([status]) +
           struct.pack("<Q", created_tick) + struct.pack("<I", payload_kind) +
           struct.pack("<Q", primer_addr) + struct.pack("<I", len(payload)) +
           payload)
    return hmac.new(key, msg, hashlib.sha256).digest()


def epoch_section(epoch_no, demoted, created_tick, payload, key,
                  primer_addr=0, payload_kind=0):
    status = 1 if demoted else 0
    hdr = bytearray(48)
    hdr[0:4] = EPCH_MAGIC
    struct.pack_into("<I", hdr, 4, epoch_no)
    hdr[8] = status
    struct.pack_into("<Q", hdr, 12, created_tick)
    struct.pack_into("<I", hdr, 20, payload_kind)
    struct.pack_into("<I", hdr, 24, len(payload))
    struct.pack_into("<Q", hdr, 32, primer_addr)
    tag = seal_epoch(epoch_no, status, created_tick, payload_kind,
                     primer_addr, payload, key)
    return bytes(hdr) + payload + tag


def custody_section():
    b = struct.pack("<II", 1, 1) + KEY_ID + struct.pack("<Q", CEREMONY_TICK)
    return b


def base_doc(cells=64, nedges=256, k=8):
    dials = [[(c * 16 + d) % 997 for d in range(quf.NDIALS)]
             for c in range(cells)]
    edges = [{"src": (i * 7) % cells, "dst": (i * 13 + 1) % cells,
              "mode": 0, "slot": i % 8, "base": i % 1000,
              "wh": (i * 17) % 65536, "age": i % 5000,
              "buckets": [(j * 3 + i) % 256 for j in range(k)]}
             for i in range(nedges)]
    routing = [{"dst": i % cells, "via": (i + 1) % cells}
               for i in range(0, cells, 4)]
    return {
        "header": {"cell_count": cells, "edge_count": nedges,
                   "route_count": len(routing), "edge.k": k,
                   "tick_period": 8},
        "dials": dials, "edges": edges, "routing": routing,
        "ticksched": {"tpw": 3, "phases": [i % 8 for i in range(cells)]},
    }


def build_forgetting(n_epochs, live_epoch=None, key=ARCHIVE_KEY,
                     flip_name_no=None, two_live=False, bad_magic=False,
                     trunc=False):
    """Build a QUF-FORGETTING-V1 container. live_epoch: index of the single
    non-demoted epoch (None = all demoted). flip_name_no: epoch whose header
    epoch_no is corrupted (E4 forge). two_live: two non-demoted epochs (E6).
    bad_magic: corrupt first epoch magic (E1). trunc: cut the file short (E2).
    """
    base = quf.build(base_doc())
    parsed = quf.read(base)
    align = parsed["header"]["align"]
    # payload_kind 0 fragment: the four v1 section payloads, each padded to
    # align, concatenated (QUF-FORGETTING-V1 §2.3).
    frag = bytearray()
    for name in quf.SECTION_ORDER:
        data = parsed["payload"][name]
        frag += data
        if len(frag) % align:
            frag += b"\x00" * (align - len(frag) % align)
    secs = [(n, k, d) for n, k, d in parsed["sections"]]
    secs.append(("custody", 0, custody_section()))
    for n in range(n_epochs):
        demoted = True
        if live_epoch is not None and n == live_epoch:
            demoted = False
        if two_live and n in (0, 1):
            demoted = False
        no = n
        if flip_name_no is not None and n == flip_name_no:
            no = (n + 1) % 65536  # header says N+1 while section name says N
        sec = bytearray(epoch_section(no, demoted, created_tick=1000 + n,
                                      payload=bytes(frag), key=key,
                                      primer_addr=(n << 32) | 0xC0DE))
        if bad_magic and n == 0:
            sec[0:4] = b"XXXX"
        secs.append(("epoch.%d" % n, 0, bytes(sec)))
    parsed["sections"] = secs
    out = bytearray(quf.rebuild(parsed))
    if trunc:
        out = out[:-64]
    return bytes(out)


def write(path, data):
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


def flip_demoted_bit(data, epoch_name="epoch.0"):
    """In-place hostile edit: flip status bit0 of the named epoch WITHOUT
    resealing. If the epoch was sealed live, this forges a demotion; if it
    was sealed demoted, this forges resurrection. Either way the seal no
    longer covers status -> must E3 under verify-then-skip (§4)."""
    parsed = quf.read(data)
    for name, _, off, size in parsed["table"]:
        if name == epoch_name:
            buf = bytearray(data)
            buf[off + 8] ^= 0x01
            return bytes(buf)
    raise SystemExit("epoch %s not found" % epoch_name)


def cmd_gen(args):
    os.makedirs(args.outdir, exist_ok=True)
    write(os.path.join(args.outdir, "archive.key"), ARCHIVE_KEY)
    write(os.path.join(args.outdir, "wrong.key"), WRONG_KEY)
    # plain v1 base (zero epochs) — sanity that epochs are an extension
    write(os.path.join(args.outdir, "base_v1.quf"), quf.build(base_doc()))
    for n in (4, 16, 64):
        d = os.path.join(args.outdir, "n%d" % n)
        os.makedirs(d, exist_ok=True)
        # all-demoted mount (the forgetting-native case) + one-live variant
        write(os.path.join(d, "all_demoted.quf"), build_forgetting(n))
        write(os.path.join(d, "one_live.quf"),
              build_forgetting(n, live_epoch=0))


def cmd_forge(args):
    os.makedirs(args.outdir, exist_ok=True)
    o = lambda f: os.path.join(args.outdir, f)  # noqa: E731
    if args.kind == "wrongkey":
        write(o("wrongkey.quf"), build_forgetting(4, key=WRONG_KEY))
    elif args.kind == "flipbit":
        # epoch 0 sealed LIVE; attacker flips its bit to demoted, no reseal.
        write(o("flipbit.quf"),
              flip_demoted_bit(build_forgetting(4, live_epoch=0)))
    elif args.kind == "flipbit-demoted":
        # epoch sealed demoted; attacker flips to resurrect it live (then the
        # file has one "live" epoch whose seal is broken -> E3).
        write(o("flipbit_demoted.quf"),
              flip_demoted_bit(build_forgetting(4)))
    elif args.kind == "e1":
        write(o("badmagic.quf"), build_forgetting(4, bad_magic=True))
    elif args.kind == "e2":
        write(o("truncated.quf"), build_forgetting(4, trunc=True))
    elif args.kind == "e4":
        write(o("namemismatch.quf"), build_forgetting(4, flip_name_no=0))
    elif args.kind == "e6":
        write(o("twolive.quf"), build_forgetting(4, two_live=True))
    else:
        raise SystemExit("unknown forge kind %r" % args.kind)


def main(argv=None):
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("outdir")
    g.add_argument("n_epochs", type=int)
    g.set_defaults(func=cmd_gen)
    f = sub.add_parser("forge")
    f.add_argument("kind")
    f.add_argument("outdir")
    f.set_defaults(func=cmd_forge)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
