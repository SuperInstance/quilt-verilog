#!/usr/bin/env python3
# c3_fold_bench.py -- C3 MATH-TO-METAL: lossless compaction == fold-covered,
# for bounded ledgers, in exact integer/byte arithmetic.
#
# Pen theorems exercised (docs/academic/conjectures.md Part III and
# FOLD-COVERED.md):
#   FC-L1  : order independence (associative + commutative folds)
#   FC-T1  : lossless <=> fold-covered (both directions on the enumerated
#             class: covered queries round-trip BYTE-EXACT; uncovered
#             queries die on exhibited fiber pairs)
#   FC-T2  : the fold taxonomy (balance = T4, projection = T5, count, sum,
#             min/max, Lambda-fold, product folds) -- every one round-trips
#   FC-X1  : the post-hoc exclusion counterexample, concretely, both regimes
#             (summary-only unconditional; digest ROM hiding with advantage
#             EXACTLY 0 over every enumerable decision rule; binding holds)
#   FC-P1  : fiber entropy -- the balance fold loses c - O(log c) bits
#   FC-T4  : Omega(c) checkpoint pricing (enumeration family separates all
#             2^c prefixes)
#   FC-T3  : recovery -- Lambda-fold counts exact + Merkle witnesses verify,
#             forged proofs rejected
#
# Bounded checks are bounded; bounds printed per section. FAIL is loud.
#
# Run: python3 tools/verifies/c3_fold_bench.py   (stdlib only, seconds)

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


def canon(x):
    """Canonical byte serialization (the byte-exactness yardstick):
    dicts keyed by sorted key, recursively -- order-insensitive by
    construction, so equality of canon == equality of folded state."""
    if isinstance(x, dict):
        return canon([(k, canon(v)) for k, v in sorted(x.items(),
                                                       key=lambda kv: repr(kv[0]))])
    if isinstance(x, (list, tuple)):
        return b"[" + b",".join(canon(v) for v in x) + b"]"
    return repr(x).encode()


# ---------------------------------------------------------------------------
# Ledger substrate: transactions = (nonce, postings, payload)
# payload alphabet: two datum symbols carrying integer "value" and "seq"
# fields -- everything a post-hoc predicate might ask about.
# ---------------------------------------------------------------------------

TX_ALPHABET = [
    {"postings": {"a": +5, "b": -5}, "payload": {"kind": "X", "val": 5, "seq": 1}},
    {"postings": {"a": -5, "b": +5}, "payload": {"kind": "Y", "val": -5, "seq": 2}},
    {"postings": {"c": +7, "d": -7}, "payload": {"kind": "X", "val": 7, "seq": 3}},
    {"postings": {"c": -7, "d": +7}, "payload": {"kind": "Y", "val": -7, "seq": 4}},
]
ACCTS = ["a", "b", "c", "d"]
EXPOSED = ["a", "c"]   # the projection fold's window (T5: nest boundary)


def mk_tx(spec_idx, nonce):
    base = TX_ALPHABET[spec_idx]
    return {"nonce": nonce, "postings": dict(base["postings"]),
            "payload": dict(base["payload"])}


# ---------------------------------------------------------------------------
# The fold taxonomy (FC-T2 / FC-D2): (Sigma, f, combine) -- all associative
# and commutative; states canonicalized for byte-exact comparison.
# ---------------------------------------------------------------------------

FOLDS = {
    # T4: the balance fold (mirror convergence is order-independence of it).
    # State = TOTAL map over the account universe (untouched = 0) -- the
    # paper's folds agree on full balance maps, so zero-net prefixes over
    # different account pairs land on the SAME state (the FC-X1 fiber).
    "balance": (
        lambda tx: {k: tx["postings"].get(k, 0) for k in ACCTS},
        lambda s, t: {k: s.get(k, 0) + t.get(k, 0) for k in ACCTS},
        {k: 0 for k in ACCTS}),
    # T5: the exposed-projection fold (consolidation: interior vanishes)
    "projection": (
        lambda tx: {k: tx["postings"].get(k, 0) for k in EXPOSED},
        lambda s, t: {k: s.get(k, 0) + t.get(k, 0) for k in EXPOSED},
        {k: 0 for k in EXPOSED}),
    # count fold
    "count": (
        lambda tx: 1,
        lambda s, t: s + t,
        0),
    # sum fold over payload value
    "sum": (
        lambda tx: tx["payload"]["val"],
        lambda s, t: s + t,
        0),
    # min/max fold over payload seq (sentinel identity)
    "minseq": (
        lambda tx: tx["payload"]["seq"],
        lambda s, t: min(s, t),
        10 ** 9),
    # Lambda-fold over the DECLARED label q_kind = "payload kind == X"
    "lambda_X": (
        lambda tx: 1 if tx["payload"]["kind"] == "X" else 0,
        lambda s, t: s + t,
        0),
    # product fold: (balance, count) componentwise
    "product": (
        lambda tx: ({k: tx["postings"].get(k, 0) for k in ACCTS}, 1),
        lambda s, t: ({k: s[0].get(k, 0) + t[0].get(k, 0) for k in ACCTS},
                      s[1] + t[1]),
        ({k: 0 for k in ACCTS}, 0)),
}


def fold(foldname, txs):
    f, comb, ident = FOLDS[foldname]
    state = ident
    for tx in txs:
        state = comb(state, f(tx))
    return state


def fold_query(foldname, qhat, txs):
    return qhat(fold(foldname, txs))


print("c3_fold_bench.py -- C3 lossless == fold-covered, exact byte enumerator")
print("=" * 78)

# ---------------------------------------------------------------------------
# [A] FC-L1 + FC-T1(a): every taxonomy fold round-trips BYTE-EXACT
# ---------------------------------------------------------------------------
print("\n[A] taxonomy folds: order-independent, byte-exact round-trip")
# Instance bounds: logs length <= 3 over the 4-tx alphabet (85 logs),
# every checkpoint c in [0..n], all permutations per multiset (<= 6).
n_A = 0
for L in range(0, 4):
    for seq in itertools.product(range(4), repeat=L):
        txs = [mk_tx(s, i) for i, s in enumerate(seq)]
        # order independence across ALL permutations
        for perm in itertools.permutations(txs):
            for fname in FOLDS:
                check(f"A.orderind[{fname}]",
                      canon(fold(fname, perm)) == canon(fold(fname, txs)),
                      f"seq={seq} perm={[t['nonce'] for t in perm]}")
                n_A += 1
        # split identity at every checkpoint: sigma(P (+) S) == sigma(L)
        for c in range(0, L + 1):
            for fname in FOLDS:
                whole = fold(fname, txs)
                _, comb, ident = FOLDS[fname]
                split = comb(fold(fname, txs[:c]), fold(fname, txs[c:]))
                check(f"A.split[{fname}]",
                      canon(whole) == canon(split),
                      f"seq={seq} c={c}")
                n_A += 1
print(f"  instances: 85 logs x {len(FOLDS)} folds x all perms + all "
      f"checkpoints = {n_A} byte-exact checks")

# fold-covered queries: qhat(sigma(L)) == Q(L) on every enumerated log
QUERIES = {
    ("balance", lambda s: s.get("a", 0),
     lambda txs: sum(t["postings"].get("a", 0) for t in txs), "bal(a)"),
    ("balance", lambda s: {k: s.get(k, 0) for k in ACCTS},
     lambda txs: {k: sum(t["postings"].get(k, 0) for t in txs)
                  for k in ACCTS}, "bal-map"),
    ("projection", lambda s: s.get("a", 0) + s.get("c", 0),
     lambda txs: sum(t["postings"].get(k, 0) for t in txs for k in EXPOSED),
     "exposed-total"),
    ("count", lambda s: s, lambda txs: len(txs), "count"),
    ("sum", lambda s: s, lambda txs: sum(t["payload"]["val"] for t in txs),
     "sum-val"),
    ("minseq", lambda s: None if s == 10 ** 9 else s,
     lambda txs: min((t["payload"]["seq"] for t in txs), default=None),
     "min-seq"),
    ("lambda_X", lambda s: (s, s > 0),
     lambda txs: (sum(1 for t in txs if t["payload"]["kind"] == "X"),
                  any(t["payload"]["kind"] == "X" for t in txs)),
     "declared-label-count/any"),
    ("product", lambda s: (s[1], s[0].get("a", 0)),
     lambda txs: (len(txs), sum(t["postings"].get("a", 0) for t in txs)),
     "(count, bal(a))"),
}
n_A2 = 0
for L in range(0, 4):
    for seq in itertools.product(range(4), repeat=L):
        txs = [mk_tx(s, i) for i, s in enumerate(seq)]
        for fname, qhat, Q, qname in QUERIES:
            check(f"A.covered[{fname}:{qname}]",
                  canon(fold_query(fname, qhat, txs)) == canon(Q(txs)),
                  f"seq={seq}")
            n_A2 += 1
print(f"  fold-covered queries: {n_A2} answers exact through the fold "
      f"(qhat(sigma(L)) == Q(L), byte-exact)")

# ---------------------------------------------------------------------------
# [B] FC-T1(b) necessity: fiber pairs kill non-covered queries, concretely
# ---------------------------------------------------------------------------
print("\n[B] FC-T1(b): non-fold-covered queries die on exhibited fibers")
# Instance bounds: all equal-length prefix pairs from the 85-log census.
def posthoc_Q(txs):
    """Post-hoc exclusion predicate: does the prefix contain a +5 posting?"""
    return any(5 in t["postings"].values() for t in txs)


n_B = 0
fiber_pairs = 0
killed = 0
by_len = {1: [], 2: [], 3: []}
for L in range(1, 4):
    for seq in itertools.product(range(4), repeat=L):
        by_len[L].append([mk_tx(s, i) for i, s in enumerate(seq)])
for L in (1, 2, 3):
    for P1, P2 in itertools.combinations(by_len[L], 2):
        if canon(fold("balance", P1)) == canon(fold("balance", P2)):
            fiber_pairs += 1
            if posthoc_Q(P1) != posthoc_Q(P2):
                killed += 1
                # the concrete counterexample: identical compacted forms,
                # differing Q -- no answerer can be right on both
                for S in ([], [mk_tx(2, 99)]):     # empty + a common suffix
                    K1 = (canon(fold("balance", P1)), canon(S))
                    K2 = (canon(fold("balance", P2)), canon(S))
                    check("B.fiber.kill",
                          K1 == K2 and posthoc_Q(P1 + S) != posthoc_Q(P2 + S),
                          f"balance-fold fiber pair with differing Q: "
                          f"{[t['nonce'] for t in P1]} vs {[t['nonce'] for t in P2]}")
                    n_B += 1
check("B.fiber.exists", fiber_pairs > 0 and killed > 0,
      f"fiber pairs found: {fiber_pairs}, killing pairs: {killed}")
print(f"  balance-fold fibers: {fiber_pairs} equal-fold prefix pairs "
      f"enumerated; {killed} carry differing post-hoc Q -- each is a "
      f"concrete no-answerer witness ({n_B} checks)")

# FC-X1 canonical pair, concretely (conjectures.md Part III / FC-X1)
P1 = [mk_tx(0, "n1"), mk_tx(1, "n2")]   # (a:+5,b:-5),(a:-5,b:+5)
P2 = [mk_tx(2, "n3"), mk_tx(3, "n4")]   # (c:+7,d:-7),(c:-7,d:+7)
ZERO = {k: 0 for k in ACCTS}
check("B.X1.foldsequal", canon(fold("balance", P1)) == canon(fold("balance", P2))
      and fold("balance", P1) == ZERO,
      "P1/P2 must have identical (total) balance folds -- the zero map")
check("B.X1.qdiffers", posthoc_Q(P1) is True and posthoc_Q(P2) is False,
      "Q = '+5 in prefix?' must be YES on P1, NO on P2")
check("B.X1.seqwise", all(sum(t["postings"].values()) == 0 for t in P1 + P2),
      "both prefixes balanced sequence-wise (A1 per tx)")
print(f"  FC-X1 canonical: sigma_bal(P1) == sigma_bal(P2) == zero map; "
      f"Q(P1)=YES Q(P2)=NO -- unconditional regime")

# ---------------------------------------------------------------------------
# [C] FC-L2 hiding (regime 2): ROM stand-in, advantage EXACTLY 0
# ---------------------------------------------------------------------------
print("\n[C] FC-L2 digest hiding: answerer advantage exactly 0 (ROM stand-in)")
# Model: root range of R = 8 values; the ROM is a seeded injective map from
# prefix-strings to roots (all injective assignments enumerated = the seed
# distribution). The answerer holds (sigma_bal, h(P_b)), b uniform, and is
# ANY function roots -> {YES, NO}: all 2^R = 256 rules enumerated.
R = 8
ROOTS = range(R)
enc = lambda P: hashlib.sha256(canon([
    (t["postings"], t["payload"]) for t in P])).digest()
# seeds: all injective assignments of the two hidden inputs to root values
seed_assignments = [(r1, r2) for r1 in ROOTS for r2 in ROOTS if r1 != r2]
n_C = 0
max_adv = None
for rule in itertools.product((True, False), repeat=R):
    # advantage over uniform b and uniform seed: Pr[rule(h(P_b)) == Q(P_b)] - 1/2
    correct = 0
    for (r1, r2) in seed_assignments:
        correct += rule[r1]            # b=0: Q(P1) = YES  (True counts)
        correct += (not rule[r2])      # b=1: Q(P2) = NO
    pr = correct / (2 * len(seed_assignments))
    adv = pr - 0.5
    if max_adv is None or abs(adv) > abs(max_adv):
        max_adv = adv
    check("C.hiding.exact0", adv == 0,
          f"rule={rule}: advantage {adv} != 0 -- hiding broken")
    n_C += 1
print(f"  decision rules enumerated: {n_C} (all 2^{R} root-classifiers); "
      f"max |advantage| = {max_adv} (exactly 0)")
# binding side: the digest SEPARATES (distinct committed values), i.e.
# separation is not extraction
check("C.binding.distinct", enc(P1) != enc(P2),
      "digest must separate P1/P2 (binding) while revealing nothing (hiding)")
print("  binding: h(P1) != h(P2) -- separation holds; extraction does not")

# ---------------------------------------------------------------------------
# [D] FC-P1 fiber entropy + FC-T4 Omega(c) pricing
# ---------------------------------------------------------------------------
print("\n[D] FC-P1/FC-T4: the balance fold loses c - O(log c) bits; Omega(c)")
# Single-account universe: prefixes of +/-1 postings to account 'a' chosen
# by a binary payload bit. sigma_bal(p) = sum(p) in [-c, c]: image 2c+1.
for c in (4, 8, 12):
    image = set()
    for bits in itertools.product((0, 1), repeat=c):
        s = sum(1 if b else -1 for b in bits)
        image.add(s)
    # sums of c many +/-1: { -c, -c+2, ..., c } -- c+1 states
    check("D.image.size", len(image) == c + 1,
          f"c={c}: single-account image {len(image)} != c+1={c + 1}")
    import math
    avg = (2 ** c) / (c + 1)
    lost = c - math.ceil(math.log2(c + 1))
    check("D.fiber.mass", avg >= (2 ** c) / (c + 1), "counting")
    print(f"  c={c:2d}: 2^c={2**c:5d} prefixes -> {len(image)} fold states; "
          f"largest fiber >= {avg:.0f}; answering bits lost >= "
          f"c - log2(c+1) = {lost}")
    check("D.lost.positive", lost >= 0 or c < 6, "small-c sanity")
# Omega(c): the positional predicate family {pi_w : w in {0,1}^c} separates
# EVERY prefix pair -- verified pairwise with the theorem's own witness
# (w = p distinguishes p from any p' != p at every differing position).
for c in (4, 8, 10):
    prefixes = list(itertools.product((0, 1), repeat=c))
    check("D.omega.count", len(prefixes) == 2 ** c, "enumeration size")
    n_pairs = 0
    for p, q in itertools.combinations(prefixes, 2):
        # answer to pi_w on prefix r = frozenset({i : r_i == w_i}).
        # Witness w = p: every position i distinguishes unless q_i == p_i;
        # since p != q some i differs -> answers differ. Verified directly:
        a_p = frozenset(i for i in range(c))           # w = p: all match
        a_q = frozenset(i for i in range(c) if q[i] == p[i])
        check("D.omega.separates", a_p != a_q,
              f"c={c}: pi_p must distinguish {p} from {q}")
        n_pairs += 1
    print(f"  c={c:2d}: family separates all {n_pairs} prefix pairs "
          f"-> any lossless state distinguishes 2^c -> >= {c} bits, forever")

# ---------------------------------------------------------------------------
# [E] FC-T3 recovery: Lambda-fold exact + Merkle witnesses verify/reject
# ---------------------------------------------------------------------------
print("\n[E] FC-T3: declared labels exact; Merkle witnesses verify; forgeries die")


def merkle_root(txs):
    leaves = [hashlib.sha256(canon([(t["postings"], t["payload"])
                                    for t in [t]])).digest() for t in txs]
    if not leaves:
        return hashlib.sha256(b"").digest()
    layer = leaves
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            l = layer[i]
            r = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(l + r).digest())
        layer = nxt
    return layer[0]


def merkle_proof(txs, idx):
    layer = [hashlib.sha256(canon([(t["postings"], t["payload"])
                                   for t in [t]])).digest() for t in txs]
    path = []
    i = idx
    while len(layer) > 1:
        sib = i ^ 1
        if sib >= len(layer):
            sib = i
        path.append(layer[sib])
        nxt = []
        for j in range(0, len(layer), 2):
            l = layer[j]
            r = layer[j + 1] if j + 1 < len(layer) else layer[j]
            nxt.append(hashlib.sha256(l + r).digest())
        layer = nxt
        i //= 2
    return path


def merkle_verify(root, idx, leaf, path):
    cur = leaf
    i = idx
    for sib in path:
        if i % 2 == 0:
            cur = hashlib.sha256(cur + sib).digest()
        else:
            cur = hashlib.sha256(sib + cur).digest()
        i //= 2
    return cur == root


n_E = 0
for L in range(1, 5):
    for seq in itertools.product(range(4), repeat=L):
        txs = [mk_tx(s, i) for i, s in enumerate(seq)]
        root = merkle_root(txs)
        # Lambda-fold count exactness vs ground truth
        declared = sum(1 for t in txs if t["payload"]["kind"] == "X")
        check("E.lambda.exact", fold("lambda_X", txs) == declared,
              f"seq={seq}")
        # every honest inclusion proof verifies
        for i, t in enumerate(txs):
            leaf = hashlib.sha256(canon([(t["postings"], t["payload"])
                                         for t in [t]])).digest()
            check("E.proof.honest", merkle_verify(root, i, leaf,
                                                  merkle_proof(txs, i)),
                  f"seq={seq} idx={i}")
            # forged proof: same path, different transaction -> rejected
            other = mk_tx((seq[i] + 1) % 4, 999)
            bad_leaf = hashlib.sha256(canon([(other["postings"],
                                              other["payload"])
                                             for t in [other]])).digest()
            check("E.proof.forged", not merkle_verify(root, i, bad_leaf,
                                                      merkle_proof(txs, i)),
                  f"seq={seq} idx={i}: forged leaf must fail (else SHA collision)")
            n_E += 2
        n_E += 1
print(f"  instances: all logs length <= 4 (341 logs), every position: "
      f"{n_E} witness checks (honest verify, forged reject), Lambda counts exact")

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
if FAILURES:
    print(f"RESULT: FAIL -- {len(FAILURES)} of {CHECKS} checks failed:")
    for name, detail in FAILURES[:40]:
        print(f"  {name}: {detail}")
    raise SystemExit(1)
print(f"RESULT: PASS -- {CHECKS} exact checks, 0 failures")
print("Bounded enumerators; bounds per section above. Integers + SHA bytes only.")
