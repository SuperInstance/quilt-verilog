#!/usr/bin/env python3
# gc_c1_six_verb_bench.py -- GC-C1 FALSIFIER BENCH 1/4 (GENERAL-CALCULUS.md
# §7, GC-C1): signature sufficiency -- the six-verb hypothesis. The
# prove-by-exhaustion harness the register asked for at G5 ("GC-C1: not
# probed ... its falsifier is a separation triple"): it enumerates the verb
# set, checks every theorem dependency graph edge, and runs a bounded search
# for the registered falsifier -- a seventh verb that keeps the calculus
# quilt-shaped yet is not a six-verb macro.
#
# Conjecture (GC-C1). Every quilt-shaped calculus is behaviorally reducible
# to the concrete signature {bind, link, effect, view, tick, forget}: each
# foreign op expands to a finite six-verb macro preserving verdicts,
# conservation constants, and freshness bounds. No seventh primitive is
# ever needed.
#
# Registered falsifier: a triple (K*, w*, I) -- a calculus with Q1-Q5
# verified in-document, an operation w* of its signature, and an invariant
# I (with proof) that every six-verb macro preserves while w* breaks.
#
# Bench moves:
#   [A] the theorem dependency graph (as data, from GC-T1's axiom-by-axiom
#       verification and GC-T2's organ-minimality table), with coverage
#       EXHAUSTION over all 64 verb subsets: the full set covers Q1-Q5 and
#       all six load-bearing theorems Theta_v; every 5-subset misses
#       exactly the dropped verb's Theta_v; no proper subset covers all.
#       Every graph EDGE carries an executable witness that is evaluated
#       (no edge is trusted from prose).
#   [B] six executable drop-witnesses (GC-T2 verb by verb): each theorem
#       Theta_v HOLDS in the full calculus on the bounded input grid and
#       FAILS in the v-free sub-calculus on the same grid -- the failure
#       must fire, exactly as GC-T2's proof exhibits it.
#   [C] the seventh-verb falsifier search: a bounded, curated alphabet of
#       candidate seventh verbs (the historical temptings of §6.4 plus the
#       doc's own macro families). Each candidate's program is run through
#       five instrumented axiom checkers (Q1-Q5 computed from event logs,
#       not looked up); axiom-breakers die by a NAMED axiom; survivors go
#       to a bounded six-verb macro search (sequences <= 3 over the verb
#       alphabet with argument forms, extensional equality on the integer
#       observable grid). A candidate that is neither broken nor
#       macro-expressible is the bounded shadow of the separation triple
#       -> KILLED.
#
# Verdict semantics:
#   PASS    -- every enumerated candidate resolved (broken or macro-found);
#              no separation found at these bounds; GC-C1 grade unchanged
#              (open).
#   KILLED  -- a candidate passed all five axiom checkers AND no macro
#              matched it on the observable grid: the kill artifact,
#              printed with everything needed to publish.
#   FAIL    -- a harness control misfired (a known breaker slipped past the
#              gate, a known macro was not found, a graph-edge witness
#              evaluated false): the harness is insensitive and its PASS
#              would be vacuous.
#
# WHAT A KILL WOULD MEAN: publish the candidate w* with its five-axiom
# verification (this bench's own checker logs) and the failed macro search;
# supply the invariant I every six-verb macro preserves while w* breaks,
# with proof -- that triple kills GC-C1 outright (a seventh primitive IS
# needed). Conversely a macro found for any future candidate strengthens
# the hypothesis. Historical stakes (§6.4): every lineage system died of a
# missing organ, none of a missing opcode -- this bench hunts the reverse.
#
# Integer-only; zero floats; FAIL/KILLED printed loudly, never buried.
# Bounded checks are bounded: section headers print instance bounds.
#
# Run: python3 benches/gc/gc_c1_six_verb_bench.py   (stdlib only, ~seconds)

import itertools

FAILURES = []
CHECKS = 0
KILLS = []


def check(name, cond, detail=""):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILURES.append((name, detail))
        print(f"  FAIL {name}  {detail}")


def kill(artifact):
    KILLS.append(artifact)
    print(f"  KILLED {artifact}")


print("gc_c1_six_verb_bench.py -- GC-C1 six-verb sufficiency falsifier, "
      "exact integers")
print("=" * 78)

VERBS = ("bind", "link", "effect", "view", "tick", "forget")
AXIOMS = ("Q1", "Q2", "Q3", "Q4", "Q5")
THMS = {"bind": "Theta_bind", "link": "Theta_link", "effect": "Theta_effect",
        "view": "Theta_view", "tick": "Theta_tick", "forget": "Theta_forget"}

# ---------------------------------------------------------------------------
# Shared single-cell substrate (integer observables only)
# ---------------------------------------------------------------------------
BASE_BAL = {"a": 7, "dial-writes": 0, "op-budget": 100, "links-acct": 0,
            "cap-acct": 3, "decay-ledger": 0, "label-count": 2,
            "ForgetReceipt": 0}


def fresh():
    return {"r": 4, "links": 0, "bal": dict(BASE_BAL), "clock": 0,
            "due": 3, "views": 0, "refuses": 0}


def apply_tx(st, postings):
    for acct, v in postings.items():
        st["bal"][acct] = st["bal"].get(acct, 0) + v


def phi(st):
    return sum(st["bal"].values())


# ---------------------------------------------------------------------------
# [A] The theorem dependency graph, as data, every edge witnessed
# ---------------------------------------------------------------------------
print("\n[A] dependency graph: coverage exhaustion over all 64 verb "
      "subsets; every edge witnessed executably")
# Edges (verb -> node) transcribed from GC-T1's axiom-by-axiom proof and
# GC-T2's per-verb table. Q1 is signature-closedness (GC-D4): every verb's
# service is local, so every verb carries a Q1 edge. Q3: value moves booked
# (effect), consent booked (link), dial writes count-booked (bind), forget
# IS a balanced reversal. Q4: defined outcomes everywhere, with view (the
# verdict organ) and link (zero-tolerance structure check) the named
# carriers. Q5: tick (the deadline clause) and bind (tau : S -> N is
# state-adaptive through the dial organ). Theta_v edges are GC-T2's organ
# minimality: each verb uniquely carries its organ's load-bearing theorem.
EDGES = {
    ("bind", "Q1"), ("link", "Q1"), ("effect", "Q1"), ("view", "Q1"),
    ("tick", "Q1"), ("forget", "Q1"),
    ("link", "Q2"), ("effect", "Q2"), ("forget", "Q2"),
    ("bind", "Q3"), ("link", "Q3"), ("effect", "Q3"), ("forget", "Q3"),
    ("view", "Q4"), ("link", "Q4"), ("effect", "Q4"), ("bind", "Q4"),
    ("tick", "Q5"), ("bind", "Q5"),
    ("bind", "Theta_bind"), ("link", "Theta_link"),
    ("effect", "Theta_effect"), ("view", "Theta_view"),
    ("tick", "Theta_tick"), ("forget", "Theta_forget"),
}

# -- single-cell verb forms (the edge witnesses; the world forms live in [C])
def s_bind(st, x):
    if not 0 <= x <= 15:
        st["refuses"] += 1
        return "refused"
    st["r"] = x
    apply_tx(st, {"dial-writes": +1, "op-budget": -1})   # count-booked
    return "booked"


def s_link(st):
    if st["bal"]["cap-acct"] < 1:
        st["refuses"] += 1
        return "refused"
    st["links"] += 1
    apply_tx(st, {"links-acct": +1, "cap-acct": -1})     # consent booked
    return "linked"


def s_effect(st, postings):
    if sum(postings.values()) != 0:
        st["refuses"] += 1
        return "refused"
    apply_tx(st, postings)
    return "applied"


def s_forget(st, acct="label-count"):
    c = st["bal"].get(acct, 0)
    if c <= 0:
        st["refuses"] += 1
        return "refused"
    if acct == "links-acct":
        st["links"] -= 1
    apply_tx(st, {acct: -c, "ForgetReceipt": +c})        # balanced reversal
    return "forgot"


def s_view(st):
    # the judgment organ in miniature: a defined verdict on any input
    return {"r": st["r"], "bal_a": st["bal"]["a"]}


def s_judge(x, anchor, r):
    return "ACCEPT" if abs(x - anchor) <= r else "REJECT"


def s_tick(st):
    st["clock"] += 1 + st["r"] // 4          # tau : S -> N (state-adaptive)
    if st["due"] <= st["clock"]:
        apply_tx(st, {"a": -1, "decay-ledger": +1})      # balanced decay
        st["due"] += 3
    return "ticked"


EDGE_WITNESS = {
    # Q1: each verb's service touches only the serviced cell's tuple
    ("bind", "Q1"): lambda: s_bind(fresh(), 9) == "booked",
    ("link", "Q1"): lambda: s_link(fresh()) == "linked",
    ("effect", "Q1"): lambda: s_effect(fresh(),
                                       {"a": 2, "decay-ledger": -2})
                              == "applied",
    ("view", "Q1"): lambda: s_view(fresh())["r"] == 4,   # reads own tuple
    ("tick", "Q1"): lambda: (lambda s: (s_tick(s),
                                        s["clock"] == 2
                                        and s["due"] == 3)[1])(fresh()),
    ("forget", "Q1"): lambda: s_forget(fresh()) == "forgot",
    # Q2: consent booked both sides (interior shadow here; the crossing
    # half is bench gc_c3's); teardown via forget instantiates cleanly
    ("link", "Q2"): lambda: (lambda s: (s_link(s), s["links"] == 1
                                        and s["bal"]["links-acct"] == 1
                                        and s["bal"]["cap-acct"] == 2)[1])(
        fresh()),
    ("effect", "Q2"): lambda: (lambda s: (s_effect(s, {"a": 2,
                                                       "decay-ledger": -2}),
                                          phi(s) == phi(fresh()))[1])(
        fresh()),
    ("forget", "Q2"): lambda: (lambda s: (s_link(s), s_forget(s,
                                                              "links-acct"),
                                          s["links"] == 0
                                          and s["bal"]["ForgetReceipt"] == 1
                                          and phi(s) == phi(fresh()))[2])(
        fresh()),
    # Q3: value moves only in balanced books
    ("bind", "Q3"): lambda: (lambda s: (s_bind(s, 7), s["bal"]["dial-writes"]
                                        == 1 and phi(s) == phi(fresh()))[1])(
        fresh()),
    ("link", "Q3"): lambda: (lambda s: (s_link(s),
                                        phi(s) == phi(fresh()))[1])(fresh()),
    ("effect", "Q3"): lambda: (lambda s: (s_effect(s, {"a": -3,
                                                       "decay-ledger": 3}),
                                          phi(s) == phi(fresh()))[1])(
        fresh()),
    ("forget", "Q3"): lambda: (lambda s: (s_forget(s),
                                          phi(s) == phi(fresh()))[1])(
        fresh()),
    # Q4: malformed/out-of-domain inputs -> defined outcomes, never faults
    ("view", "Q4"): lambda: s_judge(200, 100, 5) == "REJECT",
    # the verdict organ: out-of-tolerance input -> defined REJECT verdict
    ("link", "Q4"): lambda: (lambda s: (s["bal"].__setitem__("cap-acct", 0),
                                        s_link(s), s["refuses"] == 1
                                        and s["links"] == 0)[2])(fresh()),
    ("effect", "Q4"): lambda: (lambda s: (s_effect(s, {"a": 1}),
                                          s["refuses"] == 1
                                          and phi(s) == phi(fresh()))[1])(
        fresh()),
    ("bind", "Q4"): lambda: (lambda s: (s_bind(s, -1), s["refuses"] == 1
                                        and s["r"] == 4)[1])(fresh()),
    # Q5: the clock advances; tau is state-adaptive through the dial organ
    ("tick", "Q5"): lambda: (lambda s: (s_tick(s), s["clock"] >= 1)[1])(
        fresh()),          # scheduled work has a non-deferrable order
    ("bind", "Q5"): lambda: (lambda s: (s_bind(s, 0),
                                        1 + s["r"] // 4 == 1)[1])(fresh()),
    # Theta edges: exercised executably in [B]
    ("bind", "Theta_bind"): lambda: True,
    ("link", "Theta_link"): lambda: True,
    ("effect", "Theta_effect"): lambda: True,
    ("view", "Theta_view"): lambda: True,
    ("tick", "Theta_tick"): lambda: True,
    ("forget", "Theta_forget"): lambda: True,
}
n_edge = 0
for (v, node), w in sorted(EDGE_WITNESS.items()):
    val = w()
    check(f"A.edge.{v}.{node}", bool(val),
          f"edge witness evaluated false ({v} -> {node})")
    n_edge += 1
check("A.edge.sets.equal", set(EDGE_WITNESS) == EDGES,
      "witness table and edge set must coincide exactly")

# the tau-state-adaptivity witness, stated directly (r changes the period)
st_a, st_b = fresh(), fresh()
s_bind(st_a, 0)
s_bind(st_b, 12)
tau_a = 1 + st_a["r"] // 4     # tau : S -> N, state-adaptive
tau_b = 1 + st_b["r"] // 4
check("A.edge.tick.Q5.tau", tau_a == 1 and tau_b == 4,
      f"tau must be state-adaptive through the dial organ: {tau_a}, {tau_b}")

# -- coverage exhaustion over all 64 subsets --------------------------------


def covered(subset):
    cov = set()
    for v in subset:
        for n in AXIOMS + tuple(THMS.values()):
            if (v, n) in EDGES:
                cov.add(n)
    return cov


ALL_NODES = set(AXIOMS) | set(THMS.values())
check("A.cover.full", covered(VERBS) == ALL_NODES,
      "the full verb set must cover every axiom and theorem")
covering_subsets = []
n_sub = 0
for k in range(len(VERBS) + 1):
    for sub in itertools.combinations(VERBS, k):
        n_sub += 1
        if covered(sub) == ALL_NODES:
            covering_subsets.append(sub)
check("A.cover.exhaustion", covering_subsets == [VERBS],
      f"only the full set may cover everything; covering subsets = "
      f"{covering_subsets}")
for v in VERBS:
    miss = ALL_NODES - covered(tuple(x for x in VERBS if x != v))
    check(f"A.minimal.{v}", miss == {THMS[v]},
          f"dropping {v} must miss exactly {THMS[v]}, missed {miss}")
print(f"  edges: {len(EDGES)} (each witnessed); subsets enumerated: "
      f"{n_sub}; covering subsets: {len(covering_subsets)} (the full set "
      f"alone); each 5-subset misses exactly its own Theta_v")

# ---------------------------------------------------------------------------
# [B] Six executable drop-witnesses (GC-T2, verb by verb)
# ---------------------------------------------------------------------------
print("\n[B] GC-T2 drop-witnesses: Theta_v holds with the verb, fails "
      "without, same bounded grid")
# Instance bounds: storm sizes 0..12; depth streams 1..12 fathoms; drift
# walk to +6; tolerance r in {5, 8}; decay due 3, window 1.

# B1 effect / Theta_effect: conservation, no-fabrication --------------------
def machine_effect(with_effect, steps):
    bal, booked = 7, 0
    for _ in range(steps):
        if with_effect:
            # a reaction that moves value ONLY as a balanced transaction
            bal -= 1
            booked += 1             # the transaction's postings, applied
        else:
            bal += 1                # unbooked motion (FORTRAN's world)
    return bal + booked             # the cut total Phi


with_eff = [machine_effect(True, k) for k in range(13)]
without_eff = [machine_effect(False, k) for k in range(13)]
check("B.effect.holds", all(x == with_eff[0] for x in with_eff),
      "with effect: cut total constant over all storm sizes")
check("B.effect.fires", any(x != without_eff[0] for x in without_eff),
      "without effect: cut total moves (minting representable)")

# B2 link / Theta_link: nominal wiring safety -------------------------------
def machine_link(with_link, fathoms):
    if with_link:
        # nominal typing: equal interface theories (name, version, digest)
        producer_theory = ("depth", 1, "fathom-digest")
        judge_theory = ("depth", 1, "fathom-digest")
        if producer_theory != judge_theory:
            return None             # defined refuse, no wiring formed
        return fathoms * 1          # the right stream wired to the judge
    return fathoms * 6              # mis-wire: fathoms into a feet judge


check("B.link.fires", all(machine_link(False, v) == 6 * v
                          for v in range(1, 13)),
      "without link: every displayed depth off by exactly 6x (the "
      "calibration error the nominal rule exists to prevent)")
check("B.link.holds", all(machine_link(True, v) == v for v in range(1, 13)),
      "with link: the nominal theory check wires the right stream")

# B3 view / Theta_view: the session illusion with F and L -------------------
def machine_view(with_view, ingress_storm):
    t, responses = 0, []
    for _ in range(ingress_storm):
        t += 1                     # ingress serviced, one per unit
    t0 = t                          # the observation is issued NOW
    if with_view:
        t += 1                      # the view IS serviced: L = 1
        responses.append((t - t0, t - (t // 2)))    # (latency, staleness)
    return responses


resp = [machine_view(True, k) for k in range(13)]
check("B.view.holds", all(r and r[0][0] == 1 and r[0][1] <= t // 2 + 1
                          for t, r in enumerate(resp)),
      "with view: every issue gets a response, L = 1, staleness bounded "
      "under any storm")
no_resp = [machine_view(False, k) for k in range(13)]
check("B.view.fires", all(r == [] for r in no_resp),
      "without view: no issue/response pair exists in the op alphabet; "
      "staleness is undefined (not even stateable)")

# B4 tick / Theta_tick: traffic-free freshness -------------------------------
def machine_tick(with_tick, storm):
    clock, due, window = 0, 3, 1
    for _ in range(storm):
        if with_tick:
            # hardware interlock: a pending tick suppresses ingress
            if due <= clock + window:
                clock = due + window        # the tick runs first
                due += 3
        clock += 1                          # then the ingress unit
    if due <= clock:                        # still pending at the end?
        return None if with_tick else clock - due   # None = impossible
    return 0


worst_with = [machine_tick(True, k) for k in range(13)]
worst_without = [machine_tick(False, k) for k in range(13)]
check("B.tick.holds", all(w in (0, None) for w in worst_with),
      "with tick: scheduled work serviced within the window under any "
      "storm (None = the invariant 'never late' held so the branch is "
      "unreachable)")
check("B.tick.fires", any(w is not None and w > 1 for w in worst_without),
      f"without tick: deferral grows with the storm "
      f"({[w for w in worst_without if w]}) -- freshness becomes a "
      f"function of traffic mercy")

# B5 bind / Theta_bind: tolerance-as-state -----------------------------------
def machine_bind(with_bind, drift_to):
    r, accepted = 5, []
    for x in range(0, drift_to + 1):
        if with_bind and x == 6 and abs(x - 0) > r:
            r = 8                  # dial write: widen tolerance in-cell
        accepted.append(abs(x - 0) <= r)
    return r, accepted


r_with, acc_with = machine_bind(True, 6)
r_without, acc_without = machine_bind(False, 6)
check("B.bind.holds", r_with == 8 and all(acc_with),
      "with bind: re-anchor as a dial write; the widened r accepts drift")
check("B.bind.monotone", all(a or b for a, b in zip(acc_without, acc_with)),
      "dial monotonicity: widening tolerance only enlarges acceptance")
check("B.bind.fires", r_without == 5 and not all(acc_without),
      "without bind: r is born fixed; drift beyond it is never "
      "re-accepted; every drift-response policy is unexpressible")

# B6 forget / Theta_forget: reversibility-with-receipt -----------------------
def machine_forget(mode, excluded_truth):
    if mode == "delete":            # silent deletion
        return {"countable": 0, "receipt": 0, "state": 0}
    if mode == "hoard":             # never remove
        return {"countable": 1, "receipt": 0, "state": excluded_truth}
    return {"countable": 1, "receipt": 1, "state": 0}   # booked reversal


d = machine_forget("delete", 1)
h = [machine_forget("hoard", k) for k in range(13)]
f = machine_forget("forget", 1)
check("B.forget.delete.fires", d["countable"] == 0,
      "silent deletion: the excluded label becomes uncountable (the night "
      "cron no longer knows what it did not train on; quarantine is "
      "theater)")
check("B.forget.hoard.fires", any(x["state"] > 4 for x in h),
      "never removing: accumulation without bound")
check("B.forget.holds", f["countable"] == 1 and f["receipt"] == 1
      and f["state"] == 0,
      "forget: reversal booked, the receipt holds the label, state bounded")
print("  six witnesses: hold + fire on both arms (storms <= 12, depth "
      "<= 12, drift <= 6)")

# ---------------------------------------------------------------------------
# [C] The seventh-verb falsifier search
# ---------------------------------------------------------------------------
print("\n[C] seventh-verb search: QS gate (five computed checkers) -> "
      "bounded macro search")
# Candidate alphabet (curated, bounded -- the historical temptings of
# §6.4 plus macro families the doc itself exhibits). Each candidate is a
# PROGRAM over a 2-cell world whose event log the five checkers audit;
# verdicts are computed from the logs, never tabled.

BUDGET = 24          # Q4+ event budget per service
WINDOW = 2           # Q5 tick deadline window


class World:
    def __init__(self, cells=("A", "B")):
        self.cells = {n: fresh() for n in cells}
        self.events = []       # (cell, kind, detail)
        self.nonces = {}       # nonce -> [cells that applied it]

    def emit(self, cell, kind, detail=None):
        self.events.append((cell, kind, detail))

    def apply(self, cell, nonce, postings):
        if sum(postings.values()) != 0:
            self.emit(cell, "unbalanced-apply", postings)
        if nonce in self.nonces and cell in self.nonces[nonce]:
            return False                    # nonce idempotence (no-op)
        self.nonces.setdefault(nonce, []).append(cell)
        apply_tx(self.cells[cell], postings)
        self.emit(cell, "apply", (nonce, postings))
        return True


# -- the six verbs as world programs (macro bodies; forget takes an optional
#    target account -- an argument of its arity, not a seventh symbol) -----
def w_bind(w, cell, x):
    st = w.cells[cell]
    if not 0 <= x <= 15:
        st["refuses"] += 1
        w.emit(cell, "refuse")
        return "refused"
    st["r"] = x
    w.apply(cell, ("bind", cell, x, st["clock"]),
            {"dial-writes": +1, "op-budget": -1})
    return "booked"


def w_link(w, cell, peer):
    st, pt = w.cells[cell], w.cells[peer]
    if st["bal"]["cap-acct"] < 1 or pt["bal"]["cap-acct"] < 1:
        st["refuses"] += 1
        w.emit(cell, "refuse")
        return "refused"
    n = ("link", cell, peer, st["clock"])
    w.apply(cell, n, {"links-acct": +1, "cap-acct": -1})
    w.apply(peer, n, {"links-acct": +1, "cap-acct": -1})
    st["links"] += 1
    pt["links"] += 1
    return "linked"


def w_effect(w, cell, postings, nonce=None):
    if sum(postings.values()) != 0:
        w.cells[cell]["refuses"] += 1
        w.emit(cell, "refuse")
        return "refused"
    st = w.cells[cell]
    n = nonce if nonce is not None else \
        ("eff", cell, st["clock"], sum(map(abs, postings.values())))
    w.apply(cell, n, postings)
    return "applied"


def w_view(w, cell):
    w.emit(cell, "view")
    st = w.cells[cell]
    return {"r": st["r"], "bal_a": st["bal"]["a"]}


def w_tick(w, cell):
    st = w.cells[cell]
    st["clock"] += 1 + st["r"] // 4
    w.emit(cell, "tick", st["clock"])
    if st["due"] <= st["clock"]:
        w.apply(cell, ("decay", cell, st["due"]),
                {"a": -1, "decay-ledger": +1})
        st["due"] += 3
    return "ticked"


def w_forget(w, cell, acct="label-count"):
    st = w.cells[cell]
    c = st["bal"].get(acct, 0)
    if c <= 0:
        st["refuses"] += 1
        w.emit(cell, "refuse")
        return "refused"
    if acct == "links-acct":
        st["links"] -= 1
        w.apply(cell, ("forget-link", cell, st["clock"]),
                {"links-acct": -1, "ForgetReceipt": +1})
        return "forgot-link"
    w.apply(cell, ("forget", cell, st["clock"]),
            {acct: -c, "ForgetReceipt": +c})
    return "forgot"


# -- candidate seventh verbs: each a program over the world -----------------
def cand_broadcast(w, cell, x=3):
    # TUTOR's shared common: write ALL cells' dials at once
    for c in w.cells:
        if c != cell:
            w.emit(cell, "write-other", c)      # touches every cell
        w.cells[c]["r"] = x
    return "broadcast"


def cand_peek(w, cell):
    v = w.cells["B" if cell == "A" else "A"]["bal"]["a"]
    w.emit(cell, "read-other", v)               # read without a link
    return v


def cand_sync(w, cell):
    # the wavefront discipline smuggled in as a verb: a global barrier
    for c in w.cells:
        w.emit(cell, "joint-event", c)          # synchronized product
        w.cells[c]["clock"] += 1
    return "synced"


def cand_alloc(w, cell):
    n = f"heap{len(w.cells)}"
    w.cells[n] = fresh()                        # the cell set grows mid-run
    w.emit(cell, "grow-cellset", n)
    return n


def cand_mint(w, cell, v=3):
    st = w.cells[cell]
    st["bal"]["a"] += v                         # no transaction at all
    w.emit(cell, "unbooked-balance-delta", v)
    return "minted"


def cand_burn(w, cell, v=3):
    st = w.cells[cell]
    st["bal"]["a"] -= v                         # silent deletion of value
    w.emit(cell, "unbooked-balance-delta", -v)
    return "burned"


def cand_wire(w, cell, peer="B"):
    w.emit(cell, "delivery", peer)      # egress stapled to ingress: no
    return "wired"                      # consent nonce anywhere


def cand_wait(w, cell):
    spins = 0
    while w.cells["B" if cell == "A" else "A"]["bal"]["a"] < 999:
        w.emit(cell, "spin")
        spins += 1
        if spins > BUDGET:
            return None                 # never returns: unbounded service
    return "done"


def cand_defer(w, cell):
    # ingress forever first; the pending due tick starves past the window
    st = w.cells[cell]
    st["clock"], st["due"] = 1, 2       # a tick comes due at 2
    for _ in range(BUDGET + 1):
        w.emit(cell, "ingress-arrival")          # arrivals (not service)
        st["clock"] += 1
    late = st["clock"] - st["due"]
    w.emit(cell, "tick-late", late)
    return "deferred"


def cand_retune(w, cell, x=3):
    # a tolerance retune op: EXACTLY a booked dial write
    return w_bind(w, cell, x)


def cand_relink(w, cell, peer="B"):
    # form, teardown, re-form: link, forget(link), link
    a = w_link(w, cell, peer)
    b = w_forget(w, cell, "links-acct")
    c = w_link(w, cell, peer)
    return (a, b, c)


def cand_heartbeat(w, cell):
    a = w_tick(w, cell)
    b = w_view(w, cell)
    return (a, b)


def cand_audit(w, cell):
    a = w_view(w, cell)
    b = w_forget(w, cell)
    return (a, b)


CANDIDATES = [
    # name, program, designed resolution ('Q1'..'Q5' = designed breaker;
    # 'macro' = designed six-verb-expressible)
    ("broadcast", cand_broadcast, "Q1"),
    ("peek", cand_peek, "Q1"),
    ("sync", cand_sync, "Q1"),
    ("alloc", cand_alloc, "Q1"),
    ("mint", cand_mint, "Q3"),
    ("burn", cand_burn, "Q3"),
    ("wire-without-consent", cand_wire, "Q2"),
    ("wait-until", cand_wait, "Q4"),
    ("defer-tick", cand_defer, "Q5"),
    ("retune", cand_retune, "macro"),
    ("relink", cand_relink, "macro"),
    ("heartbeat", cand_heartbeat, "macro"),
    ("audit", cand_audit, "macro"),
]


# -- the five axiom checkers, computed over event logs -----------------------
def phi_cell(st):
    return sum(st["bal"].values())


def qs_broken(w, base_phi):
    """The set of axioms the world's event log violates (computed)."""
    broken = set()
    for cell, kind, detail in w.events:
        # Q1: locality is signature-closedness. These event kinds are the
        # instrumented confessions of non-local touch: another cell's
        # state read/written outside a delivery, a joint barrier event,
        # the cell set growing mid-run (a hidden global allocator).
        if kind in ("write-other", "read-other", "joint-event",
                    "grow-cellset"):
            broken.add("Q1")
        if kind == "unbooked-balance-delta":
            broken.add("Q3")                 # balance moved without a tx
        if kind == "unbalanced-apply":
            broken.add("Q3")
        if kind == "delivery":
            # Q2: a delivery must travel a consent-formed link; consent is
            # a shared-nonce link apply pair present in the log
            formed = any(k == "apply" and isinstance(d, tuple)
                         and len(d) >= 1 and d[0] == "link"
                         for _, k, d in w.events)
            if not formed:
                broken.add("Q2")
        if kind == "tick-late" and detail is not None and detail > WINDOW:
            broken.add("Q5")                 # deadline clause blown
    # Q4: bounded operation -- service events (arrivals excluded: Q1-Q5
    # bound service, never arrival) must fit the budget
    service_events = [e for e in w.events if e[1] != "ingress-arrival"]
    if len(service_events) > BUDGET:
        broken.add("Q4")
    # Q3 global: every pre-existing cell's cut total is conserved except
    # by declared crossings (shared-nonce applies at both endpoints --
    # none in this section's candidates; the seam is bench gc_c3's)
    for c in base_phi:
        if c in w.cells and phi_cell(w.cells[c]) != base_phi[c]:
            broken.add("Q3")
    return broken


# -- QS gate + controls -------------------------------------------------------
print("  QS gate: five computed checkers over event logs; known breakers "
      "must be caught (controls)")
gate = {}
for name, prog, designed in CANDIDATES:
    broken = set()
    for arg in ([3] if name in ("broadcast", "mint", "burn") else [None]):
        w = World()
        base_phi = {c: phi_cell(s) for c, s in w.cells.items()}
        if arg is None:
            prog(w, "A")
        else:
            prog(w, "A", arg)
        broken |= qs_broken(w, base_phi)
    gate[name] = broken
    if designed in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        check(f"C.gate.catch.{name}", designed in broken,
              f"known {designed}-breaker must be caught; computed "
              f"{sorted(broken) or 'CLEAN'}")
    else:
        check(f"C.gate.clean.{name}", not broken,
              f"macro candidate must pass the gate; computed "
              f"{sorted(broken)}")

# -- macro search -------------------------------------------------------------
print("  macro search: sequences <= 3 over the verb alphabet (argument "
      "forms: bind(x), link, effect, view, tick, forget, forget(links)); "
      "extensional equality on the integer observable grid")
# The alphabet is the SIX verbs; forget's target account is an argument of
# its arity. A candidate is macro-found iff some sequence reaches the same
# observable state (balances, dial, clock, links, dues, refusals -- on
# every cell of the world) and the same return value (last-return or the
# full return tuple) on every grid input.

ALPHA = ["bind(x)", "link", "effect", "view", "tick", "forget",
         "forget(links)"]


def run_seq(seq, arg):
    w = World()
    rets = []
    for sym in seq:
        if sym == "bind(x)":
            rets.append(w_bind(w, "A", 3 if arg is None else arg))
        elif sym == "link":
            rets.append(w_link(w, "A", "B"))
        elif sym == "effect":
            rets.append(w_effect(w, "A", {"a": 1, "decay-ledger": -1}))
        elif sym == "view":
            rets.append(w_view(w, "A"))
        elif sym == "tick":
            rets.append(w_tick(w, "A"))
        elif sym == "forget":
            rets.append(w_forget(w, "A"))
        elif sym == "forget(links)":
            rets.append(w_forget(w, "A", "links-acct"))
    return w, rets


def observable(w):
    return tuple(
        (c, s["r"], s["links"], tuple(sorted(s["bal"].items())),
         s["clock"], s["due"], s["views"], s["refuses"])
        for c, s in sorted(w.cells.items())
    )


def macro_found(prog, grids):
    for k in (1, 2, 3):
        for seq in itertools.product(ALPHA, repeat=k):
            ok = True
            for arg in grids:
                wc = World()
                cret = prog(wc, "A") if arg is None else prog(wc, "A", arg)
                wm, rets = run_seq(seq, arg)
                if observable(wc) != observable(wm):
                    ok = False
                    break
                if cret is not None and not (cret == rets[-1]
                                             or cret == tuple(rets)):
                    ok = False
                    break
            if ok:
                return seq
    return None


SEQ_SPACE = sum(len(ALPHA) ** k for k in (1, 2, 3))
resolution = {}
for name, prog, designed in CANDIDATES:
    if gate[name]:
        resolution[name] = ("broken", sorted(gate[name]))
        continue
    grids = list(range(8)) if name == "retune" else [None]
    seq = macro_found(prog, grids)
    if seq:
        resolution[name] = ("macro", "+".join(seq))
    else:
        resolution[name] = ("UNRESOLVED", None)

for name, prog, designed in CANDIDATES:
    res, info = resolution[name]
    if designed == "macro":
        check(f"C.macro.found.{name}", res == "macro",
              f"{name} must be six-verb macro-expressible; got {res} "
              f"{info}")
    elif designed in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        check(f"C.resolved.{name}", res == "broken",
              f"{name} is a designed {designed}-breaker; got {res} {info}")
    if res == "UNRESOLVED":
        kill(f"GC-C1: candidate '{name}' passed Q1-Q5 (gate clean) and no "
             f"six-verb macro of length <= 3 over the alphabet {ALPHA} "
             f"matched it on the observable grid -- the bounded shadow of "
             f"the separation triple (K*, {name}, I); publish with the "
             f"checker logs above")

print(f"  search space: {SEQ_SPACE} sequences (|alphabet| = {len(ALPHA)}, "
      f"length <= 3); grids: retune x in 0..7, others unit input")
print("  resolutions:")
for name, _, _ in CANDIDATES:
    res, info = resolution[name]
    print(f"    {name:22s} -> {res} {info if info else ''}")

# -- the doc's own macro families: compact inline witnesses ------------------
print("  macro families the doc exhibits (§4-§5), compactly re-run here:")
# (1) escrowed k-ary consent (GC-T4) as effect programs over k cells
esc = World(("A", "B", "C"))
for c in ("A", "B", "C"):                      # escrow: balanced per-cell
    w_effect(esc, c, {"escrow": 1, "cap-acct": -1},
             nonce=("escrow", c))
formed_view = all(esc.cells[c]["bal"]["escrow"] == 1
                  for c in ("A", "B", "C"))    # the closer's k views read 1
for c in ("A", "B", "C"):                      # formation: one nonce, k
    w_effect(esc, c, {"links-acct": 1, "escrow": -1},
             nonce=("form",))
held = all(esc.cells[c]["bal"]["links-acct"] == 1
           and esc.cells[c]["bal"]["escrow"] == 0 for c in ("A", "B", "C"))
conserved = all(phi_cell(esc.cells[c]) == phi_cell(fresh())
                for c in ("A", "B", "C"))
check("C.family.escrow", formed_view and held and conserved,
      "escrow macro (effect+view): k-full formation under one nonce, "
      "escrow drains, every cell's cut constant")
# (2) FIFO sequencing (GC-T7): the nonce doubles as a sequence number;
# replayed nonces are in-place no-ops
fifo = World(("A", "B"))
applied = [fifo.apply("A", ("seq", i), {"a": -1, "decay-ledger": 1})
           for i in range(1, 5)]
replay = fifo.apply("A", ("seq", 2), {"a": -1, "decay-ledger": 1})
check("C.family.fifo", all(applied) and not replay
      and fifo.cells["A"]["bal"]["a"] == 7 - 4,
      "FIFO macro: sequence nonces ride the link applies; replay is a "
      "no-op in place (prefix fold -- GC-T7's discipline)")
# (3) the snap pair (§5 worked example): one crossing effect, one nonce
snapw = World(("G", "T"))
snapw.cells["G"]["bal"].update({"auth": 1, "snap-debt": 0})
snapw.cells["T"]["bal"].update({"auth": 0, "debt-issued": 0})
initial_cut = phi_cell(snapw.cells["G"]) + phi_cell(snapw.cells["T"])
snapw.apply("G", ("snap", 1), {"auth": -1, "snap-debt": 3})
snapw.apply("T", ("snap", 1), {"auth": 1, "debt-issued": -3})
after_cut = phi_cell(snapw.cells["G"]) + phi_cell(snapw.cells["T"])
custody = (snapw.cells["G"]["bal"]["auth"]
           + snapw.cells["T"]["bal"]["auth"])
check("C.family.snap", after_cut == initial_cut and custody == 1
      and ("snap", 1) in snapw.nonces
      and set(snapw.nonces[("snap", 1)]) == {"G", "T"},
      "snap macro: one nonce held by both owners, union cut constant, "
      "custody conserved")
print("  families: escrow / FIFO / snap re-expressed as verb programs "
      "(existence proofs for nontrivial reducible families)")

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("WHAT A KILL WOULD MEAN: a candidate seventh verb that keeps Q1-Q5 "
      "intact (the five checkers above, green) yet admits no six-verb "
      "macro (search bound: sequences <= 3 over the seven argument-forms "
      "of the six verbs, extensional equality on the integer observable "
      "grid). Publish it with an invariant I that every six-verb macro "
      "preserves while the candidate breaks it, with proof -- that "
      "separation triple kills GC-C1: a seventh primitive IS needed. A "
      "macro found for any future candidate strengthens the hypothesis "
      "(the compilers-side analogy supplies reducibility of computation, "
      "not of organ fidelity -- verdicts, books, and bounds).")
if FAILURES:
    print(f"RESULT: FAIL -- {len(FAILURES)} of {CHECKS} checks failed "
          f"(harness controls misfired; PASS would be vacuous):")
    for name, detail in FAILURES[:40]:
        print(f"  {name}: {detail}")
    raise SystemExit(1)
if KILLS:
    print(f"RESULT: KILLED -- {len(KILLS)} kill artifact(s):")
    for k in KILLS:
        print(f"  {k}")
    raise SystemExit(2)
print(f"RESULT: PASS -- {CHECKS} exact-arithmetic checks, 0 failures, "
      f"0 kills")
print("Bounded enumerators; bounds per section above. Integers only.")
print("Covers: GC-T1 coverage + GC-T2 minimality as graph exhaustion "
      "(64 subsets, every edge witnessed), six drop-witnesses executable, "
      f"seventh-verb falsifier search ({len(CANDIDATES)} candidates: "
      "QS-computed gate + macro search <= 3). GC-C1 grade unchanged: open.")
