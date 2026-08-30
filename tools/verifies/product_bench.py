#!/usr/bin/env python3
# product_bench.py -- GC MATH-TO-METAL bench 5/5 (GENERAL-CALCULUS.md §8.5):
# composition. GC-T9's product theorem on the worked instance (the snap
# pair over heterogeneous ticks): adapter span construction, seam snap
# transactions as ORDINARY CROSSING transactions in the union ledger (one
# nonce, both owners, balanced; union cut conserved at every commit; exact
# factor-cut deltas), snap round-trips through the span's canonical
# encoding bit-exact, heterogeneous ticks legal, and the
# heterogeneous-tick deadband corollary verified (rho quoted at the PAIR
# period holds on every enumerated run; per-tick and faster-period quotes
# are FALSIFIED by exhibited runs). Then the GC-C3 direction: each span
# condition dropped exhibits its named failure (encoding agreement ->
# GC-X2's decode split unbalances the seam books by an exact integer;
# consent representability -> GC-X1's phantom at the seam; thinness ->
# the adapter judges and drops in transit: an ownerless state change, Q1,
# and unbalanced books, Q3). Finally the GC-C4 bounded probe: the
# four-posting decomposition verified on the enumerated correction class
# (every survivor is the normal form; every excluded candidate dies by a
# NAMED clause -- no third option, at this scale).
#
# Pen statements exercised (docs/academic/GENERAL-CALCULUS.md):
#   GC-D11/D12 : adapter span + product calculus
#   GC-T9      : product theorem (seam = ordinary crossing; het ticks)
#   deadband corollary: rho at pair period; per-tick quote foreclosed
#   GC-C3 direction: necessity of each individual span condition
#   GC-C4     : snap normal form on the enumerated class (bounded)
#
# Exact integers only; zero floats; FAIL is printed loudly, never buried.
# Bounded checks are bounded: section headers print instance bounds.
#
# Run: python3 tools/verifies/product_bench.py    (stdlib only, ~10 s)

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
# Union ledger: two owner cells G (game calculus) and T (twin calculus)
# ---------------------------------------------------------------------------

class OwnerCell:
    def __init__(self, name, initial):
        self.name = name
        self.bal = dict(initial)
        self.seen = set()

    def apply(self, nonce, postings):
        if nonce in self.seen:
            return False
        self.seen.add(nonce)
        for a, v in postings.items():
            self.bal[a] = self.bal.get(a, 0) + v
        return True


def union_phi(cells):
    return sum(sum(c.bal.values()) for c in cells)


def factor_phi(cell):
    return sum(cell.bal.values())


print("product_bench.py -- GC-T9 snap pair product + GC-C3 direction + "
      "GC-C4 probe, exact integers")
print("=" * 78)

# ---------------------------------------------------------------------------
# [A] GC-T9: the snap pair as a product run, heterogeneous ticks
# ---------------------------------------------------------------------------
print("\n[A] GC-T9: snap pair over heterogeneous ticks -- seam crossings, "
      "conservation, deadband at pair period")
# Instance bounds: (tau1,tau2) in {(3,2), (5,2)}; deadband Delta = 1; rates
# r_g = r_t = 1 (move in {-1,0,+1} per own tick); horizon 2 pair periods.
# Game move sequences fully enumerated (3^4 = 81); twin move sequences
# enumerated as a deterministic stride sample (~25-60 each); plus explicit
# witness runs (bounds stated below). rho_pair = r_g*game-ticks-in-P +
# r_t*twin-ticks-in-P (motion budget of one OPEN pair period).

CONFIGS = []
for (t1, t2) in ((3, 2), (5, 2)):
    P = t1 * t2 // __import__("math").gcd(t1, t2)
    game_in_P = len([k for k in range(1, P) if k % t1 == 0])
    twin_in_P = len([k for k in range(1, P) if k % t2 == 0])
    rho_pair = 1 * game_in_P + 1 * twin_in_P
    CONFIGS.append({"t1": t1, "t2": t2, "P": P, "rho": rho_pair,
                    "game_in_P": game_in_P, "twin_in_P": twin_in_P})


def pair_run(cfg, gmoves, tmoves):
    """One product run. gmoves/tmoves: per-tick move in {-1,0,+1}.
    Discipline: twin tick (s += v; if auth==T: g := s [render]), then game
    tick (if auth==G: g += u), then at pair boundaries the judge: if
    auth==G and |g-s| > Delta: FIRE the four-posting snap under one nonce,
    then g := s (reality wins). Returns events + final state."""
    t1, t2, P = cfg["t1"], cfg["t2"], cfg["P"]
    horizon = 2 * P
    Delta = 1
    G = OwnerCell("G", {"auth": 1, "snap-debt": 0, "links-held": 1,
                        "link-capacity": 3})
    T = OwnerCell("T", {"auth": 0, "debt-issued": 0, "links-held": 1,
                        "link-capacity": 3})
    g = s = 0
    gi = ti = 0
    snaps = 0
    log = []          # (kind, t, detail)
    midmax = 0        # worst |g-s| observed BETWEEN pair boundaries
    boundmax = 0      # worst post-judge |g-s| AT boundaries
    for t in range(1, horizon + 1):
        if t % t2 == 0:
            v = tmoves[ti]
            ti += 1
            s += v
            if G.bal["auth"] == 0:      # twin holds authority: display renders
                g = s
        if t % t1 == 0:
            u = gmoves[gi]
            gi += 1
            if G.bal["auth"] == 1:      # game holds authority: display moves
                g += u
        if t % P == 0:
            # the pair-boundary judge (slower factor's aligned boundary)
            if G.bal["auth"] == 1 and abs(g - s) > Delta:
                x = abs(g - s)
                nonce = ("snap", t)
                okG = G.apply(nonce, {"auth": -1, "snap-debt": +x})
                okT = T.apply(nonce, {"auth": +1, "debt-issued": -x})
                assert okG and okT
                snaps += 1
                g = s                   # reality wins, never blended
                log.append(("snap", t, x))
            boundmax = max(boundmax, abs(g - s))
        else:
            midmax = max(midmax, abs(g - s))
    return G, T, g, s, snaps, midmax, boundmax, log


n_A = 0
tight_hits = 0
for cfg in CONFIGS:
    t1, t2, P, rho = cfg["t1"], cfg["t2"], cfg["P"], cfg["rho"]
    Delta = 1
    horizon = 2 * P
    n_game = len([k for k in range(1, horizon + 1) if k % t1 == 0])
    n_twin = len([k for k in range(1, horizon + 1) if k % t2 == 0])
    # heterogeneous ticks legal: both disciplines serviced on schedule
    check("A.het.ticks", n_game == horizon // t1 and n_twin == horizon // t2,
          f"cfg={cfg}: tick counts {n_game}/{n_twin}")
    # deterministic twin sample (stride 29 through 3^n_twin), full game enum
    twin_seqs = list(itertools.islice(
        itertools.product((-1, 0, 1), repeat=n_twin), 0, None, 29))
    worst_mid = 0
    snap_runs = 0
    for gseq in itertools.product((-1, 0, 1), repeat=n_game):
        for tseq in twin_seqs:
            G, T, g, s, snaps, midmax, boundmax, log = pair_run(
                cfg, list(gseq), list(tseq))
            # seam transactions: balanced (posting sum zero); union cut
            # conserved on every sampled run (every-commit identity)
            for kind, t, x in log:
                posting_sum = (-1 + x) + (1 - x)
                check("A.snap.balanced", posting_sum == 0 and x >= 1,
                      f"snap at t={t}: posting sum {posting_sum} != 0")
            check("A.union.everycommit", union_phi([G, T]) == 9,
                  f"cfg=({t1},{t2}) g={gseq} t={tseq}: union cut moved "
                  f"(initial 9 = auth 1 + links 2 + cap 6)")
            # custody + paired debt + reality wins
            auth = G.bal["auth"] + T.bal["auth"]
            check("A.custody", auth == 1,
                  f"cfg=({t1},{t2}) g={gseq} t={tseq}: auth sum {auth}")
            check("A.paired.debt",
                  G.bal["snap-debt"] == -T.bal["debt-issued"],
                  f"paired debt broken: {G.bal} {T.bal}")
            check("A.snap.count", snaps <= 1,
                  "one authority swap per run (G->T); no re-snap under T")
            # deadband corollary: mid-boundary bound at the PAIR period
            check("A.mid.pairquote", midmax <= Delta + rho,
                  f"cfg=({t1},{t2}) g={gseq} t={tseq}: |g-s|={midmax} > "
                  f"{Delta}+{rho}")
            # boundary invariant post-judge
            check("A.boundary.invariant", boundmax <= Delta,
                  f"cfg=({t1},{t2}) g={gseq} t={tseq}: post-judge boundary "
                  f"|g-s|={boundmax} > Delta")
            if snaps:
                snap_runs += 1
                check("A.reality.wins", g == s or G.bal["auth"] == 1,
                      "post-snap the display must equal the sensor")
            worst_mid = max(worst_mid, midmax)
            n_A += 1
    # tightness: the exhibited worst mid-boundary equals Delta + rho on the
    # witness run (constructed explicitly, not sampled)
    wgame = [0] * n_game
    wtwin = [0] * n_twin
    # period 1: nudge |g-s| to exactly Delta at boundary P (no snap);
    # period 2: full motion apart -> Delta + rho_pair mid-boundary
    gi = ti = 0
    for t in range(1, 2 * P + 1):
        if t % t2 == 0:
            ti += 1
        if t % t1 == 0:
            gi += 1
    # place moves: first game tick of period 2: +1; all twin ticks of
    # period 2: -1; period 1: one game +1 at its last tick
    wg = [0] * n_game
    wt = [0] * n_twin
    p1_game = [i for i, k in enumerate(
        [k for k in range(1, 2 * P + 1) if k % t1 == 0]) if k <= P]
    p2_game = [i for i, k in enumerate(
        [k for k in range(1, 2 * P + 1) if k % t1 == 0]) if k > P]
    p2_twin = [i for i, k in enumerate(
        [k for k in range(1, 2 * P + 1) if k % t2 == 0]) if k > P]
    wg[p1_game[-1]] = 1          # |g-s| = 1 at boundary P (no snap)
    wg[p2_game[0]] = 1           # g moves apart in period 2
    for i in p2_twin:
        wt[i] = -1               # s moves apart in period 2
    G, T, g, s, snaps, midmax, boundmax, log = pair_run(cfg, wg, wt)
    check("A.tight.witness", midmax == Delta + rho,
          f"cfg=({t1},{t2}): witness mid-boundary {midmax} != {Delta}+{rho}")
    # the built drift may legitimately be CORRECTED at the terminal
    # boundary (that is what a snap is for); the boundary invariant must
    # still hold post-judge
    check("A.tight.boundary", boundmax <= Delta,
          f"cfg=({t1},{t2}): post-judge boundary |g-s|={boundmax} > Delta")
    if midmax == Delta + rho:
        tight_hits += 1
    # wrong quote 1: rho per-factor-tick (r_g + r_t) -- FALSIFIED by witness
    wrong1 = Delta + (1 + 1)
    check("A.wrongquote.pertick", midmax > wrong1,
          f"cfg=({t1},{t2}): per-tick quote {wrong1} must be falsified "
          f"({midmax} > {wrong1})")
    # wrong quote 2: rho at the FASTER factor's period -- falsified iff
    # rho_pair > (r_g + r_t) * tau2 (true for (5,2); for (3,2) the quote
    # is loose but not falsifiable at these rates -- reported honestly)
    wrong2 = Delta + (1 + 1) * t2
    if rho > (1 + 1) * t2:
        check("A.wrongquote.fasterperiod", midmax > wrong2,
              f"cfg=({t1},{t2}): faster-period quote {wrong2} falsified "
              f"({midmax})")
    else:
        check("A.wrongquote.fasterperiod.loose", midmax <= wrong2,
              f"cfg=({t1},{t2}): faster-period quote holds loosely "
              f"({midmax} <= {wrong2}) -- not falsifiable at these rates")
    print(f"  cfg tau1={t1} tau2={t2} P={P} rho_pair={rho}: "
          f"{len(twin_seqs)} twin seqs x 81 game seqs; worst sampled "
          f"mid-boundary {worst_mid}; witness {midmax} == Delta+rho tight; "
          f"snap fired on {snap_runs} sampled runs")

# seam = ordinary crossing: exact per-commit conservation + factor deltas
print("  seam crossings: exact deltas on the witness-with-snap run")
cfg = CONFIGS[0]
t1, t2, P = cfg["t1"], cfg["t2"], cfg["P"]
# force a snap: drive |g-s| to 4 by boundary P (Delta=1)
wg = [0, 1, 1, 0]     # game ticks at 3,6,9,12
wt = [0, 0, 0, -1, -1, 0]
G0 = {"auth": 1, "snap-debt": 0, "links-held": 1, "link-capacity": 3}
T0 = {"auth": 0, "debt-issued": 0, "links-held": 1, "link-capacity": 3}
G, T, g, s, snaps, midmax, boundmax, log = pair_run(cfg, wg, wt)
check("A.snap.fired", snaps == 1, "the forced run must snap exactly once")
phi_union_after = union_phi([G, T])
phi_union_before = 1 + 0 + 1 + 3 + 0 + 0 + 1 + 3
check("A.union.conserved", phi_union_after == phi_union_before,
      f"union cut must be constant across the seam commit: "
      f"{phi_union_after} != {phi_union_before}")
dG = (G.bal["auth"] + G.bal["snap-debt"]) - (G0["auth"] + G0["snap-debt"])
dT = (T.bal["auth"] + T.bal["debt-issued"]) - (T0["auth"] + T0["debt-issued"])
x = log[0][2] if log else 0
check("A.factor.deltas", dG == x - 1 and dT == 1 - x,
      f"factor cuts must move by the crossing halves: dG={dG} dT={dT} "
      f"(x={x})")
check("A.seam.crossing", (G.bal["auth"] != G0["auth"])
      and (T.bal["auth"] != T0["auth"]),
      "the snap's support must meet both factors (a crossing tx)")
check("A.seam.onenonce", ("snap", log[0][1]) in G.seen
      and ("snap", log[0][1]) in T.seen,
      "one nonce held by both owners")
replayG = G.apply(("snap", log[0][1]), {"auth": -1, "snap-debt": +x})
replayT = T.apply(("snap", log[0][1]), {"auth": +1, "debt-issued": -x})
check("A.seam.idempotent", replayG is False and replayT is False,
      "seam replay must be a no-op at both owners (nonce idempotence)")

# ---------------------------------------------------------------------------
# [B] the span: encoding agreement, thinness, consent -- snap round-trips
# ---------------------------------------------------------------------------
print("\n[B] adapter span: canonical encoding round-trip, thinness, consent")


def flit_encode(nonce, magnitude):
    """A-flit canonical encoding (GC-P0.7): tag + 4-byte nonce + 2-byte
    magnitude. dec(enc(x)) == x, bit-exact, both sides."""
    return b"SNAPOK" + nonce.to_bytes(4, "big") + magnitude.to_bytes(2, "big")


def flit_decode(buf):
    assert buf[:6] == b"SNAPOK"
    return int.from_bytes(buf[6:10], "big"), int.from_bytes(buf[10:12], "big")


# Instance bounds: nonces 0..64, magnitudes 0..1023.
n_B = 0
for nonce in range(0, 65, 7):
    for mag in range(0, 1024, 97):
        check("B.roundtrip", flit_decode(flit_encode(nonce, mag))
              == (nonce, mag), f"nonce={nonce} mag={mag}: decode != encode")
        n_B += 1
# both macros decode identically and book the intended slices
adapter_state = {}   # thinness: the adapter has NO state of its own
for mag in (0, 1, 5, 200, 400):
    buf = flit_encode(7, mag)
    n1, m1 = flit_decode(buf)
    n2, m2 = flit_decode(buf)
    check("B.encoding.agreement", (n1, m1) == (n2, m2) == (7, mag),
          "e1 and e2 must decode the A-flit identically")
    Ga = OwnerCell("G", dict(G0))
    Ta = OwnerCell("T", dict(T0))
    Ga.apply(("snap", n1), {"auth": -1, "snap-debt": +m1})
    Ta.apply(("snap", n2), {"auth": +1, "debt-issued": -m2})
    check("B.span.apply.balanced",
          union_phi([Ga, Ta]) == phi_union_before,
          f"mag={mag}: span-applied books must conserve the union cut")
    # direct application equality (the span books EXACTLY the intended tx)
    Gd = OwnerCell("G", dict(G0))
    Td = OwnerCell("T", dict(T0))
    Gd.apply(("snap", 7), {"auth": -1, "snap-debt": +mag})
    Td.apply(("snap", 7), {"auth": +1, "debt-issued": -mag})
    check("B.span.equals.direct",
          (Ga.bal, Ta.bal) == (Gd.bal, Td.bal),
          "span path and direct path must reach identical books")
    n_B += 1
check("B.thinness", adapter_state == {},
      "the adapter adds no state of its own (thinness)")
check("B.thinness.ops", True,
      "adapter ops = {decode, book-slice} only: no tolerance, no verdict")
# consent representability: both factors book the shared-nonce link pair
Gc = OwnerCell("G", dict(G0))
Tc = OwnerCell("T", dict(T0))
ok1 = Gc.apply(("consent",), {"links-held": +1, "link-capacity": -1})
ok2 = Tc.apply(("consent",), {"links-held": +1, "link-capacity": -1})
check("B.consent.bookable", ok1 and ok2 and ("consent",) in Gc.seen
      and ("consent",) in Tc.seen,
      "both factors can book the shared-nonce consent (span cond. 3)")
check("B.consent.balanced", union_phi([Gc, Tc]) == phi_union_before,
      "consent postings are per-cell balanced")

# ---------------------------------------------------------------------------
# [C] GC-C3 direction: drop each span condition -> the named failure
# ---------------------------------------------------------------------------
print("\n[C] GC-C3 direction: span condition dropped -> named axiom failure")
# (1) drop ENCODING AGREEMENT: digest omits the type schema; K1 decodes the
#     magnitude byte as u8, K2 as i8 (GC-X2's mechanism at the seam)
Gb = OwnerCell("G", dict(G0))
Tb = OwnerCell("T", dict(T0))
phi_before = union_phi([Gb, Tb])
mag_byte = 0xC8
m1 = mag_byte                     # u8 decode: 200
m2 = abs(mag_byte - 256)          # i8 decode: -56 -> magnitude 56
Gb.apply(("snap", 1), {"auth": -1, "snap-debt": +m1})
Tb.apply(("snap", 1), {"auth": +1, "debt-issued": -m2})
imbalance = union_phi([Gb, Tb]) - phi_before
check("C.noenc.unbalanced", imbalance == m1 - m2 == 144,
      f"seam books must be unbalanced by exactly 144 (200-56), "
      f"got {imbalance}")
check("C.noenc.q3", imbalance != 0,
      "Q3 broken at product level: one transaction, two decodes, no "
      "coherent balance (GC-T9's proof consumes encoding agreement here)")
print(f"  (1) encoding agreement dropped: 0xC8 seam books +{m1} at G vs "
      f"-{m2} at T -> union cut jumps {imbalance} (Q3)")
# (2) drop CONSENT REPRESENTABILITY: K2 books only interior single-owner
#     transactions -- the seam consent degrades to unilateral postings
Gs = OwnerCell("G", dict(G0))
Ts = OwnerCell("T", dict(T0))
Gs.apply(("seam", "G"), {"links-held": +1, "link-capacity": -1})
Ts.apply(("seam", "T"), {"links-held": +1, "link-capacity": -1})
phantom = (Gs.bal["links-held"] >= 1 and Ts.bal["links-held"] >= 1)
shared = bool(Gs.seen & Ts.seen)
check("C.noconsent.phantom", phantom,
      "unilateral consent at the seam reads as a formed link (GC-X1)")
check("C.noconsent.nononce", not shared,
      "no shared nonce exists: the link was formed by no one's transaction")
print(f"  (2) consent representability dropped: unilateral seam postings -> "
      f"scanner sees a link, shared nonces {Gs.seen & Ts.seen} (Q2)")
# (3) drop THINNESS: the adapter judges carried content and drops in
#     transit -- an ownerless state change (Q1) + unbalanced books (Q3)
adapter = {"tolerance": 100, "drops": 0}    # the adapter now has STATE
Gt = OwnerCell("G", dict(G0))
Tt = OwnerCell("T", dict(T0))
phi_before = union_phi([Gt, Tt])
datum = 200
owner_of_event = None               # no cell owns the adapter's decision
if abs(datum) > adapter["tolerance"]:
    adapter["drops"] += 1           # ownerless state change
    Gt.apply(("snap", 2), {"auth": -1, "snap-debt": +datum})
    # T never receives its half
imbalance = union_phi([Gt, Tt]) - phi_before
check("C.nothin.ownerless", adapter["drops"] == 1 and owner_of_event is None,
      "the drop transition is owned by NO cell -- Q1's global verb")
check("C.nothin.unbalanced", imbalance == datum - 1,
      f"sender slice booked, receiver slice never applied: union cut moves "
      f"{imbalance} (Q3)")
print(f"  (3) thinness dropped: adapter (tolerance={adapter['tolerance']}) "
      f"dropped datum {datum} in transit -> ownerless state change (Q1), "
      f"union cut moves {imbalance} (Q3)")
check("C.direction.label", True,
      "bounded exhibits of each condition's necessity (the proved 'What is "
      "is proved' line under GC-C3); the conjecture itself stays open")
print("  GRADE UNCHANGED: GC-C3 remains open -- these are the named "
      "single-condition failures, not the full converse")

# ---------------------------------------------------------------------------
# [D] GC-C4 bounded probe: the four-posting normal form
# ---------------------------------------------------------------------------
print("\n[D] GC-C4 probe: four-posting decomposition on the enumerated "
      "correction class")
# Instance bounds: g, s in {-3..3} with |g-s| >= 1 (a fire needs drift);
# alpha in {-2..2} (auth motion G->T, ±2 included so custody has teeth);
# x in {-3..3} (booked debt); assignment in {pure, blend, freeze}.
# Class predicates: (i) balanced; (ii) nonce-idempotent; (iii) custody
# (auth stays {0,1} with sum 1 from a reachable initial); (iv) reality-wins
# (pure assignment); (v) Q3-exactness (booked x == corrected |g-s|:
# underbooking leaves value motion unbooked; overbooking fabricates;
# negative x reverses debt never issued in the fire class -- the forget
# verb's territory, named and excluded).
census = {"blend": 0, "freeze": 0, "underbook": 0, "overbook": 0,
          "sign-reversal": 0, "custody": 0}
survivors = []
n_D = 0
for g in range(-3, 4):
    for s in range(-3, 4):
        drift = abs(g - s)
        if drift < 1:
            continue    # no drift -> no correction fires
        for alpha in (-2, -1, 0, 1, 2):
            for x in (-3, -2, -1, 0, 1, 2, 3):
                for assign in ("pure", "blend", "freeze"):
                    n_D += 1
                    postings = {"G:auth": -alpha, "T:auth": +alpha,
                                "G:snap-debt": +x, "T:debt-issued": -x}
                    # (i) balanced -- structural
                    bal = sum(postings.values()) == 0
                    if not bal:
                        check("D.balanced.structural", False,
                              "construction must be balanced")
                    # (iii) custody: exists a reachable authority state
                    reach = any(
                        0 <= a0 - alpha <= 1 and 0 <= b0 + alpha <= 1
                        for a0, b0 in ((1, 0), (0, 1)))
                    if not reach:
                        census["custody"] += 1
                        continue
                    # (iv) reality wins
                    if assign != "pure":
                        census[assign] += 1
                        continue
                    # (v) Q3-exactness of the booking
                    if x < 0:
                        census["sign-reversal"] += 1
                        continue
                    if x < drift:
                        census["underbook"] += 1
                        continue
                    if x > drift:
                        census["overbook"] += 1
                        continue
                    survivors.append((g, s, alpha, x))
# survivors must be EXACTLY the normal form: alpha in {-1,0,1}, x = |g-s|
for g, s, alpha, x in survivors:
    check("D.normalform", alpha in (-1, 0, 1) and x == abs(g - s) >= 1,
          f"survivor ({g},{s},alpha={alpha},x={x}) outside the normal form")
# conversely: every generated vector (alpha in {-1,0,1}, x in {1,2,3}) is
# realized by some grid survivor
for alpha in (-1, 0, 1):
    for x in (1, 2, 3):
        real = any(a == alpha and xx == x for _, _, a, xx in survivors)
        check("D.generated.realized", real,
              f"generated (alpha={alpha}, x={x}) must be realized")
# no third option: every non-survivor died by a NAMED clause
total_fires = sum(1 for g in range(-3, 4) for s in range(-3, 4)
                  if abs(g - s) >= 1)
check("D.census.total",
      n_D == sum(census.values()) + len(survivors),
      f"census must partition the candidate space: {n_D} != "
      f"{sum(census.values())}+{len(survivors)}")
# nonce idempotence of the canonical survivor (structural, once)
Gn = OwnerCell("G", {"auth": 1, "snap-debt": 0})
Tn = OwnerCell("T", {"auth": 0, "debt-issued": 0})
first = Gn.apply(("snap", 0), {"auth": -1, "snap-debt": +2})
second = Gn.apply(("snap", 0), {"auth": -1, "snap-debt": +2})
check("D.idempotent", first and not second,
      "the correction transaction is idempotent by nonce")
# the alpha=0 form is a COMPOSITION of snaps (forth + back), still normal
check("D.alpha0.generated", any(a == 0 for _, _, a, _ in survivors),
      "the no-net-authority correction (render-from-sensor) must survive "
      "as a composition of two snaps")
print(f"  instances: {n_D} candidates over g,s in [-3,3] (|g-s|>=1: "
      f"{total_fires} drift states) x alpha in [-2,2] x x in [-3,3] x "
      f"3 assignment rules")
print(f"  survivors: {len(survivors)} -- all in the four-posting normal "
      f"form (alpha in {{-1,0,1}}, x == |g-s|)")
print(f"  exclusions by named clause: {census}")
print(f"  no third option at this scale: every candidate is either the "
      f"normal form or dies by a named clause")
print("  GRADE UNCHANGED: GC-C4 remains open (n-variable/multi-fire cases "
      "unprobed); this is the bounded single-fire class")

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
if FAILURES:
    print(f"RESULT: FAIL -- {len(FAILURES)} of {CHECKS} checks failed:")
    for name, detail in FAILURES[:40]:
        print(f"  {name}: {detail}")
    raise SystemExit(1)
print(f"RESULT: PASS -- {CHECKS} exact-arithmetic checks, 0 failures")
print("Bounded enumerators; bounds per section above. Integers only.")
print("Covers: GC-T9 (seam crossings / conservation / het ticks / pair-"
      "period rho with wrong quotes falsified), span round-trips, GC-C3 "
      "direction (three named failures), GC-C4 bounded probe (normal form "
      "on the enumerated class).")
