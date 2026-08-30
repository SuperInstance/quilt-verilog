#!/usr/bin/env python3
# escrow_bench.py -- GC MATH-TO-METAL bench 1/5 (GENERAL-CALCULUS.md §8.1):
# k-ary consent. GC-X1's phantom link made EXECUTABLE (naive 2-of-3 consent
# books a 2-link nobody agreed to), then GC-T4's escrowed-consent repair
# verified: no phantom under pairwise scanning at every commit, formation
# fires only at k-full escrow, refund fires at the tick deadline (bounded),
# and every cut constant is conserved at every commit.
#
# Pen statements exercised (docs/academic/GENERAL-CALCULUS.md):
#   GC-X1 : naive n-ary consent breaks Q2 -- pairwise scanner declares the
#           A-B 2-link from 2-of-3 consents; under the joint-nonce
#           definition the failure inverts (capacity debited against a
#           link that does not exist)
#   GC-T3 : conservation is arity-blind (all cuts, all k, checked literally)
#   GC-T4 : escrowed consent -- escrow inert, formation only at k-full,
#           tick-bounded refund, conservation at every commit
#
# Ledger substrate mirrors the tapfabric/q_cell discipline (GC-P0.2):
# append-only log, nonce idempotence, single-writer ownership, integer
# balances. Zero floats; every verdict is an integer comparison.
# Bounded checks are bounded: section headers print instance bounds.
# FAIL is printed loudly, never buried.
#
# Run: python3 tools/verifies/escrow_bench.py    (stdlib only, seconds)

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
# Per-cell ledger (GC-P0.2: append-only, nonce-idempotent, owner-only posts)
# ---------------------------------------------------------------------------

class Cell:
    def __init__(self, name):
        self.name = name
        self.log = []
        self.seen = set()
        self.bal = {}

    def apply(self, nonce, postings):
        """Apply the OWNED SLICE of a transaction; nonce idempotence (A4).
        A transaction crossing owners is applied at each owner (GC-P0.2)."""
        if nonce in self.seen:
            return False
        self.seen.add(nonce)
        self.log.append((nonce, dict(postings)))
        for a, v in postings.items():
            self.bal[a] = self.bal.get(a, 0) + v
        return True

    def bal_of(self, a):
        return self.bal.get(a, 0)


def cut_totals(books, names):
    """Phi(C) for EVERY cell subset C, as a dict subset-tuple -> total."""
    out = {}
    for r in range(0, len(names) + 1):
        for sub in itertools.combinations(names, r):
            out[sub] = sum(sum(books[n].bal.values()) for n in sub)
    return out


def pairwise_scan(books, names, theory):
    """The GC-X1 observer: pairwise scan of the books -- a 2-ary link (i,j)
    on `theory` exists iff both endpoints hold links-held on that theory."""
    links = []
    for i, j in itertools.combinations(names, 2):
        hi = books[i].bal_of(f"{i}:links-held@{theory}")
        hj = books[j].bal_of(f"{j}:links-held@{theory}")
        if hi >= 1 and hj >= 1:
            links.append((i, j))
    return links


def joint_scan(books, names, theory):
    """The k-ary shared-nonce definition (GC-T4 step 2): a k-link on
    `theory` exists iff some ONE nonce is held by ALL k endpoints AND its
    postings touch links-held (a formation transaction). Unilateral naive
    postings never share a nonce, so they denote nothing."""
    common = set.intersection(*[books[n].seen for n in names]) if names else set()
    # a common nonce counts only if it booked links-held at every endpoint
    for nonce in common:
        ok = True
        for n in names:
            entry = next((p for nn, p in books[n].log if nn == nonce), None)
            if entry is None or entry.get(f"{n}:links-held@{theory}", 0) <= 0:
                ok = False
                break
        if ok:
            return True
    return False


print("escrow_bench.py -- GC-X1 phantom link + GC-T4 escrowed consent, exact integers")
print("=" * 78)

# ---------------------------------------------------------------------------
# [A] GC-X1: the phantom link, executable (canonical 3-ary instance)
# ---------------------------------------------------------------------------
print("\n[A] GC-X1: naive 2-of-3 consent -> pairwise scanner declares the A-B 2-link")
# Instance bounds: k = 3 parties {A,B,C}, one theory P, all 2^3 consent
# subsets; scanner run after every consent event.
THEORY = "P"
PARTIES3 = ["A", "B", "C"]


def naive_run(consenters):
    books = {n: Cell(n) for n in PARTIES3}
    for n in PARTIES3:  # initial capacity endowment (interior, balanced)
        books[n].apply(("endow", n), {f"{n}:link-capacity@{THEORY}": +4,
                                      f"{n}:capacity-source": -4})
    phi0 = cut_totals(books, PARTIES3)
    phantoms_first = None
    for n in PARTIES3:
        if n not in consenters:
            continue
        # naive generalization: the binary handshake posted UNILATERALLY
        books[n].apply((THEORY, "naive", n),
                       {f"{n}:links-held@{THEORY}": +1,
                        f"{n}:link-capacity@{THEORY}": -1})
        links = pairwise_scan(books, PARTIES3, THEORY)
        if links and phantoms_first is None:
            phantoms_first = (n, tuple(links))
    return books, phi0, phantoms_first


# canonical: A and B consent; C never does (dial stays 0 -- Q4 holds)
books, phi0, first = naive_run({"A", "B"})
check("A.phantom.fires", first is not None,
      "pairwise scanner must declare a link from 2-of-3 naive consents")
check("A.phantom.isAB", first is not None and set(first[1][0]) == {"A", "B"},
      f"the phantom must be the A-B 2-link, got {first}")
check("A.C.silent", books["C"].bal_of(f"C:links-held@{THEORY}") == 0
      and books["C"].bal_of(f"C:link-capacity@{THEORY}") == 4,
      "C never consented; its dial state is a defined total outcome (Q4)")
check("A.books.balanced",
      all(sum(p.values()) == 0 for c in books.values() for _, p in c.log),
      "every naive posting is balanced -- the failure is Q2, not A1")
check("A.cuts.conserved", cut_totals(books, PARTIES3) == phi0,
      "all cut constants conserved (conservation survives; Q2 does not)")
# the inverted failure: under the JOINT definition no link exists, yet
# capacity is debited at A and B against a link that does not exist
check("A.joint.nolink", not joint_scan(books, PARTIES3, THEORY),
      "joint-nonce definition: no 3-link exists (C never consented)")
check("A.capacity.stranded",
      books["A"].bal_of(f"A:link-capacity@{THEORY}") == 3
      and books["B"].bal_of(f"B:link-capacity@{THEORY}") == 3
      and books["A"].bal_of(f"A:links-held@{THEORY}") == 1,
      "capacity debited while (jointly) no link exists -- the inverted failure")
print(f"  canonical: A,B consent, C silent -> scanner declares {first[1]}; "
      f"joint scan: no link; capacity stranded at A,B")

# generalized: every consent subset of {A,B,C} (k=3) and {A,B,C,D} (k=4)
n_A = 0
for k, names in ((3, PARTIES3), (4, ["A", "B", "C", "D"])):
    for r in range(0, k + 1):
        for S in itertools.combinations(names, r):
            globals()["PARTIES3_TMP"] = None
            books = {n: Cell(n) for n in names}
            for n in names:
                books[n].apply(("endow", n),
                               {f"{n}:link-capacity@{THEORY}": +4,
                                f"{n}:capacity-source": -4})
            phi0 = cut_totals(books, names)
            for n in S:
                books[n].apply((THEORY, "naive", n),
                               {f"{n}:links-held@{THEORY}": +1,
                                f"{n}:link-capacity@{THEORY}": -1})
            links = pairwise_scan(books, names, THEORY)
            # phantom fires iff >= 2 consented (a 2-link from partial k-ary consent)
            check("A.gen.phantom", (len(links) >= 1) == (len(S) >= 2),
                  f"k={k} S={S}: scanner={links} but |S|={len(S)}")
            check("A.gen.cuts", cut_totals(books, names) == phi0,
                  f"k={k} S={S}: cut constants moved")
            check("A.gen.joint", not joint_scan(books, names, THEORY),
                  f"k={k} S={S}: no full k-link can exist under |S|<k")
            n_A += 1
print(f"  generalized: {n_A} consent subsets over k=3 and k=4 -- phantom "
      f"fires exactly when |S| >= 2; cuts conserved in every one")

# ---------------------------------------------------------------------------
# [B] GC-T4: escrowed consent -- no phantom, k-full formation, tick refund
# ---------------------------------------------------------------------------
print("\n[B] GC-T4: escrow -> no phantom ever; formation only at k-full; "
      "refund at the tick deadline")


def escrow_run(k, consenters, tau_consent=3):
    """Simulate GC-T4 with ticks. Returns (books, events).
    Events: ('consent',c,t) ('formation',t) ('refund',t) ('tick',t).
    Closer = party 0; closer ticks at t=1..; consents land at t=1."""
    names = [f"c{i}" for i in range(k)]
    theory = "P"
    books = {n: Cell(n) for n in names}
    for n in names:
        books[n].apply(("endow", n), {f"{n}:link-capacity@{theory}": +4,
                                      f"{n}:capacity-source": -4})
    phi0 = cut_totals(books, names)
    events = []
    snapshots = [cut_totals(books, names)]
    formed = False

    def closer_tick(t):
        nonlocal formed
        full = all(books[n].bal_of(f"{n}:escrow@{theory}") == 1 for n in names)
        if full and not formed:
            # formation transaction: ONE nonce, crossing all k owners
            for n in names:
                books[n].apply((theory, "formation"),
                               {f"{n}:links-held@{theory}": +1,
                                f"{n}:escrow@{theory}": -1})
            formed = True
            events.append(("formation", t))
            snapshots.append(cut_totals(books, names))
            return True
        return False

    for t in range(1, tau_consent + 1):
        if t == 1:
            for i in sorted(consenters):
                n = f"c{i}"
                books[n].apply((theory, "escrow", n),
                               {f"{n}:escrow@{theory}": +1,
                                f"{n}:link-capacity@{theory}": -1})
            events.append(("consent", tuple(sorted(consenters)), t))
            snapshots.append(cut_totals(books, names))
        if closer_tick(t):
            continue
        events.append(("tick", t))
        snapshots.append(cut_totals(books, names))
        if t == tau_consent and not formed:
            for i in sorted(consenters):  # refund: balanced, tick-driven
                n = f"c{i}"
                books[n].apply((theory, "refund", n),
                               {f"{n}:escrow@{theory}": -1,
                                f"{n}:link-capacity@{theory}": +1})
            events.append(("refund", t))
            snapshots.append(cut_totals(books, names))
    return books, events, phi0, snapshots, names, theory


# Instance bounds: k in {2,3,4}; every nonempty consent subset (2^k - 1);
# tau_consent = 3; cut snapshot after EVERY event, all 2^k subsets each.
n_B = 0
formations = refunds = 0
for k in (2, 3, 4):
    names_k = list(range(k))
    for r in range(1, k + 1):
        for S in itertools.combinations(names_k, r):
            books, events, phi0, snaps, names, theory = escrow_run(k, set(S))
            formed = any(e[0] == "formation" for e in events)
            refunded = any(e[0] == "refund" for e in events)
            # (1) no phantom EVER: pairwise scanner empty at every snapshot
            #     taken before formation; links-held only moves at formation
            pre_form = True
            lh_moves = []
            for n in names:
                base = 0
                for nonce, p in books[n].log:
                    if f"{n}:links-held@{theory}" in p and nonce != ("endow", n):
                        lh_moves.append((n, nonce))
            check("B.escrow.inert", not lh_moves or
                  all(n[1] == (theory, "formation") for n in lh_moves),
                  f"k={k} S={S}: links-held touched outside formation: {lh_moves}")
            # (2) formation fires ONLY at k-full
            check("B.formation.kfull", formed == (len(S) == k),
                  f"k={k} S={S}: formed={formed} but |S|={len(S)}")
            # (3) refund: fires iff not formed; at the deadline tick exactly
            refund_t = next((e[1] for e in events if e[0] == "refund"), None)
            check("B.refund.fires", refunded == (not formed),
                  f"k={k} S={S}: refunded={refunded} formed={formed}")
            check("B.refund.tickbounded", refund_t == 3 if refunded
                  else refund_t is None,
                  f"k={k} S={S}: refund at {refund_t}, deadline tau=3")
            # (4) escrow drained, capacity restored after refund
            if refunded:
                for i in names_k:
                    n = f"c{i}"
                    check("B.refund.drains",
                          books[n].bal_of(f"{n}:escrow@{theory}") == 0,
                          f"k={k} S={S} {n}: escrow not drained")
                    exp = 4  # endowment; refund restores it exactly
                    check("B.refund.restores",
                          books[n].bal_of(f"{n}:link-capacity@{theory}") == exp,
                          f"k={k} S={S} {n}: capacity not restored")
                refunds += 1
            # (5) after formation: all k hold links-held, joint scan sees it
            if formed:
                for n in names:
                    check("B.formed.holds",
                          books[n].bal_of(f"{n}:links-held@{theory}") == 1,
                          f"k={k} S={S} {n}")
                check("B.formed.joint", joint_scan(books, names, theory),
                      "the formed k-link must satisfy the shared-nonce def")
                formations += 1
            # (6) conservation: EVERY cut constant at EVERY commit
            for snap in snaps:
                check("B.cuts.everycommit", snap == phi0,
                      f"k={k} S={S}: cut constants moved mid-run")
            # (7) partial states denote no link under BOTH scanners
            if not formed:
                check("B.partial.nolink",
                      not pairwise_scan(books, names, theory)
                      and not joint_scan(books, names, theory),
                      f"k={k} S={S}: partial escrow must denote no link")
            n_B += 1
print(f"  instances: k in {{2,3,4}} x nonempty consent subsets = {n_B} runs; "
      f"{formations} formations (all k-full), {refunds} refunds (all at "
      f"tick tau=3); cuts checked after every event")
check("B.counts", formations >= 3 and refunds >= 3,
      "both regimes must be exercised")

# escrow is inert: partial escrow states touch ONLY escrow and capacity
books, events, phi0, snaps, names, theory = escrow_run(3, {0})
touched = set()
for n in names:
    for nonce, p in books[n].log:
        if nonce[0] == theory:
            touched.update(p.keys())
bad = [a for a in touched if "escrow@" not in a and "link-capacity@" not in a]
check("B.escrow.only", not bad,
      f"partial escrow touched non-escrow accounts: {bad}")
check("B.escrow.nolinks", all("links-held" not in a for a in touched),
      "no links-held posting may exist in a partial escrow state")

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
if FAILURES:
    print(f"RESULT: FAIL -- {len(FAILURES)} of {CHECKS} checks failed:")
    for name, detail in FAILURES[:40]:
        print(f"  {name}: {detail}")
    raise SystemExit(1)
print(f"RESULT: PASS -- {CHECKS} exact-arithmetic checks, 0 failures")
print("Bounded enumerators; bounds per section above. Integers only.")
print("Covers: GC-X1 (executable), GC-T3 (all cuts, k<=4), "
      "GC-T4 (no phantom / k-full formation / tick-bounded refund / "
      "conservation at every commit).")
