#!/usr/bin/env python3
"""Recover fold's latch correspondence by simulation.

PDR's invariant dump names latches lo<k> in the POST-fold net (fold destroys
yosys names). We simulate the pre-fold net (whose latches we can name via
the aim: var col = 0-based latch index) and the post-fold net with
identical pseudo-random PI streams from the all-zero init, then match each
post-fold latch to the unique pre-fold latch whose value sequence is
identical (or complementary). Unambiguous, eventful matches only; anything
else maps to None (clauses touching it are dropped downstream -- sound).

Usage: sim_match.py pre.aig folded.aig folded_map.json --steps 320
  folded_map.json: {"k": [j_or_null, flip_or_0]} per folded latch index k
"""
import json, random, sys

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
        t = data[pos:nl].decode().split()
        latches.append(int(t[0]))  # next-state literal
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
    ands = [None] * (M + 1)  # var -> (l0, l1)
    for v in range(I + L + 1, M + 1):
        d1, pos = rv(pos)
        d2, pos = rv(pos)
        l0 = 2 * v - d1
        ands[v] = (l0, l0 - d2)
    assert pos <= len(data)
    return I, L, latches, ands

def simulate(I, L, nextlits, ands, steps, seed):
    rng = random.Random(seed)
    andv = [0] * len(ands)
    lat = [0] * L
    traces = [[] for _ in range(L)]
    for t in range(steps):
        pis = [rng.randrange(2) for _ in range(I)]
        # record current state
        for k in range(L):
            traces[k].append(lat[k])
        # evaluate ANDs bottom-up (vars increase)
        for v in range(len(ands)):
            e = ands[v]
            if e is None:
                continue
            l0, l1 = e
            a = val(l0, I, lat, pis, andv, v)
            b = val(l1, I, lat, pis, andv, v)
            andv[v] = a & b
        nxt = []
        for k in range(L):
            nxt.append(val(nextlits[k], I, lat, pis, andv, 0))
        lat = nxt
    return traces

def val(lit, I, lat, pis, andv, _v):
    v, neg = lit >> 1, lit & 1
    if v == 0:
        x = 0
    elif v <= I:
        x = pis[v - 1]
    elif v <= I + len(lat):
        x = lat[v - I - 1]
    else:
        x = andv[v]
    return x ^ neg

def main():
    pre, folded, out = sys.argv[1], sys.argv[2], sys.argv[3]
    steps = int(sys.argv[sys.argv.index("--steps") + 1]) if "--steps" in sys.argv else 320
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 0xC0FFEE
    Ip, Lp, np, ap = parse(pre)
    If, Lf, nf, af = parse(folded)
    assert Ip == If, (Ip, If)
    tp = simulate(Ip, Lp, np, ap, steps, seed)
    tf = simulate(If, Lf, nf, af, steps, seed)
    # index pre traces by content
    byseq = {}
    for j in range(Lp):
        key = bytes(tp[j])
        byseq.setdefault(key, []).append(j)
    mapping = {}
    named = amb = const = 0
    for k in range(Lf):
        seq = bytes(tf[k])
        cands = byseq.get(seq, [])
        flip = 0
        if not cands:
            inv = bytes(1 - b for b in tf[k])
            cands = byseq.get(inv, [])
            flip = 1
        if len(set(cands)) == 1:
            j = cands[0]
            toggles = sum(1 for a, b in zip(tp[j], tp[j][1:]) if a != b)
            if toggles == 0:
                mapping[k] = [j, flip, "const"]
                const += 1
            else:
                mapping[k] = [j, flip, "ok"]
                named += 1
        else:
            mapping[k] = [None, 0, "ambiguous" if cands else "nomatch"]
            amb += 1
    json.dump(mapping, open(out, "w"))
    print(f"folded latches: {Lf}, matched-ok: {named}, const: {const}, unmatched/ambiguous: {amb}")

if __name__ == "__main__":
    main()
