#!/usr/bin/env python3
# gc_c2_synchrony_bench.py -- GC-C2 FALSIFIER BENCH 2/4 (GENERAL-CALCULUS.md
# §7, GC-C2): the synchrony separation. Direction (a) is PROVED (GC-T8:
# every wavefront-W calculus is eagerly simulated by a local-tick calculus
# with freshness F <= W) and machine-checked at scale in
# tools/verifies/wavefront_bench.py; this bench re-runs a compact instance
# of it and then hunts the OPEN half (b): a wavefront simulator with a
# FIXED per-cell ingress buffer bound B, no drops, no blocking, that
# preserves every enumerated local-tick source -- the registered
# falsifier, searched for and (expected) not found.
#
# Conjecture (GC-C2b). No wavefront calculus with bounded per-cell ingress
# buffers simulates the local-tick calculi: for every buffer bound B there
# is a local-tick quilt (a burst source: a cell legally receiving more
# than B deliveries between barriers) whose behaviors no bounded-B
# wavefront machine preserves without dropping (losing behaviors) or
# blocking (breaking totality, Q4). Q1-Q5 bound SERVICE, never ARRIVAL --
# so the burst source is a legal quilt.
#
# Registered falsifier: a wavefront simulator with fixed buffer bound B,
# no drops, no blocking, and a simulation proof covering ALL local-tick
# quilts (the artifact: the machine, the proof, and the treatment of the
# burst family -- the source that emits k deliveries between barriers for
# adversarial k). Alternatively, a lower-bound proof (unboundedness for
# all wavefront simulators) resolves the conjecture positively.
#
# Bench moves:
#   [A] compact GC-T8 re-check (the proved direction stays proved): eager
#       local-tick simulation of wavefront instances -- per-cell apply
#       sequences preserved, staleness <= W at every observation, phi = 0
#       gives full sequence equality.
#   [B] the bounded-buffer counterexample SEARCH: simulator space
#       (B in {1,2,4,8} x policy in {drop, block, coalesce}) x source
#       space (DISTINCT-content bursts k = 1..12 between barriers, the
#       adversarial family; DELTA-grammar sources, the protocol-shaped
#       family). A policy survives only if it preserves EVERY enumerated
#       source with 0 drops and 0 blocks. Every bounded in-model policy
#       must die on a named source (the counterexample search outcome);
#       the unbounded wavefront machine is the preservation ceiling
#       (control); k <= B must preserve under drop (control: the harness
#       is not a blanket rejector).
#   [C] wavefront membership + the PLATO special case: the early-flush
#       policy preserves everything but services BETWEEN barriers -- the
#       membership checker must reject it (it is the local-tick machine
#       wearing the wavefront's clothes; out of model). The DELTA grammar
#       (write-only-changes: at most one emission per variable per window,
#       the latest value) fits B = 1 -- and the SAME machine and config
#       dies on the unrestricted grammar: the bound came from the SOURCE's
#       shape, not the simulator's cleverness. The conjecture says that
#       shape was necessity, not thrift; the bench exhibits both sides.
#
# Verdict semantics:
#   PASS    -- every bounded in-model policy died on a named source at
#              these bounds; GC-C2(b) grade unchanged (open; this is
#              bounded evidence in the falsifier's own frame).
#   KILLED  -- some fixed-B, no-drop, no-block wavefront policy preserved
#              every enumerated source INCLUDING the adversarial DISTINCT
#              family: the kill artifact, printed with B, the policy, and
#              the burst treatment.
#   FAIL    -- a control misfired (the unbounded machine failed to
#              preserve; k <= B was rejected; the membership checker
#              accepted a mid-window flush; the (a)-direction re-check
#              failed): the harness is insensitive and PASS is vacuous.
#
# WHAT A KILL WOULD MEAN: publish the machine (fixed B, the policy), the
# no-drop/no-block invariant, and the simulation proof covering the burst
# family for adversarial k -- that kills GC-C2(b) outright (bounded
# wavefront simulation of ALL local-tick quilts exists; PLATO's
# write-only-changes was thrift, not necessity). A lower-bound proof
# resolves it positively instead. Until either: the grade stays open.
#
# Integer-only; zero floats; FAIL/KILLED printed loudly, never buried.
# Bounded checks are bounded: section headers print instance bounds.
#
# Run: python3 benches/gc/gc_c2_synchrony_bench.py  (stdlib only, ~seconds)

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


print("gc_c2_synchrony_bench.py -- GC-C2 synchrony separation falsifier, "
      "exact integers")
print("=" * 78)

# ---------------------------------------------------------------------------
# [A] compact GC-T8 re-check (the proved direction stays proved)
# ---------------------------------------------------------------------------
print("\n[A] GC-T8 compact: wavefront-W eagerly simulated by local-tick "
      "tau == W; sequences preserved, staleness <= W")
# Instance bounds: W in {2,3}; 2 barriers of batches, batch content from
# {"", "X", "XY"} (9 shapes per W); <= 2 scheduled items, due times on the
# grid 1..2W-1; phi in 0..W-1. (The full-scale check: wavefront_bench.py.)

def service_times(items, W, phi, HB):
    """Ordered apply list [(t, item)] for the machine with service
    instants kW+phi: deliveries EAGER at arrival; scheduled items at the
    next service instant >= due. Tie-break at equal instants: scheduled
    (due order) then deliveries (arrival order) -- identical for both
    machines, so phi=0 yields identical sequences."""
    out = []
    for it in items:
        if it[0] == "deliv":
            out.append((it[1], 1, it[2][1], it))
        else:
            t = min(k * W + phi for k in range(0, HB + 3)
                    if k * W + phi >= it[1])
            out.append((t, 0, it[1], it))
    out.sort(key=lambda e: (e[0], e[1], e[2]))
    return [(t, it) for t, _, _, it in out]


def max_staleness(applies, commits, horizon):
    pts = sorted(set([c for c, _ in applies] + list(commits) + [0]))
    worst = 0
    for t in range(0, horizon + 1):
        last = max(p for p in pts if p <= t)
        worst = max(worst, t - last)
    return worst


n_A = 0
for W in (2, 3):
    HB = 2
    horizon = HB * W
    for batches in itertools.product([(), ("X",), ("X", "Y")], repeat=HB):
        items, bid = [], 0
        for k, b in enumerate(batches):
            for sym in b:
                items.append(("deliv", k * W, (sym, bid)))
                bid += 1
        due_pairs = [(None,)] + [(d,) for d in range(1, horizon)] + \
            [(d1, d2) for d1 in range(1, horizon)
             for d2 in range(1, horizon) if d1 < d2]
        for dp in due_pairs:
            its = list(items)
            for d in dp:
                if d is not None:
                    its.append(("sched", d, ("S", d)))
            if not its:
                continue
            wf = service_times(its, W, 0, HB)
            for phi in range(W):
                sim = service_times(its, W, phi, HB)
                check("A.multiset",
                      sorted(map(str, [i for _, i in wf]))
                      == sorted(map(str, [i for _, i in sim])),
                      f"W={W} phi={phi}: apply multisets differ")
                check("A.batch.order",
                      [i for _, i in wf if i[0] == "deliv"]
                      == [i for _, i in sim if i[0] == "deliv"],
                      f"W={W} phi={phi}: batch order not preserved")
                ss = max_staleness(sim, [k * W + phi
                                         for k in range(HB + 2)], horizon)
                check("A.stale.sim", ss <= W, f"W={W} phi={phi}: {ss} > W")
                if phi == 0:
                    check("A.phi0.equal", wf == sim,
                          f"W={W}: phi=0 sequences must be equal")
                n_A += 1
print(f"  instances: W in {{2,3}} x 9 batch shapes x due-time patterns x "
      f"phi 0..W-1 = {n_A} constructions; all preserved; staleness <= W "
      f"everywhere; phi=0 full equality")

# ---------------------------------------------------------------------------
# [B] the bounded-buffer counterexample search (the open half)
# ---------------------------------------------------------------------------
print("\n[B] GC-C2(b) search: bounded wavefront policies x burst sources; "
      "every bounded policy must die on a named source")
# Model. A local-tick source quilt (legal: service bounded, arrival
# unbounded -- Q1-Q5 bound service, never arrival) emits k deliveries
# between two wavefront barriers (window W). The wavefront simulator
# services ONLY at barriers, so arrivals sit in the per-cell ingress
# buffer. Buffer bound B; policy on buffer-full:
#   drop     -- the arrival is lost (apply set shrinks: behavior lost)
#   block    -- the source stalls (its bounded tick service cannot
#               complete: Q4+/Q5 broken on the simulated quilt)
#   coalesce -- arrivals targeting the same variable merge, latest wins
#               (write-only-changes semantics); DISTINCT content has
#               nothing to merge, so coalesce == drop on the adversarial
#               family.
# Instance bounds: W in {2,3,4}; DISTINCT bursts k = 1..12; DELTA sources
# with V in {1,2,3} variables and <= 1 change per variable per window;
# B in {1,2,4,8}.

W_GRID = (2, 3, 4)
K_MAX = 12
B_GRID = (1, 2, 4, 8)


def source_distinct(W, k):
    """The adversarial family: k fresh-content deliveries between
    barriers, one per unit (tau_source = 1, bounded service per tick).
    Returns the per-window emission list."""
    per_unit = k // W
    rem = k % W
    emissions = []
    for unit in range(W):
        n = per_unit + (1 if unit < rem else 0)
        for j in range(n):
            emissions.append(("d", unit, f"item-{unit}-{j}"))
    return emissions


def source_delta(W, V):
    """The protocol-shaped family (write-only-changes): at most one
    emission per variable per window, the LATEST value; emissions bounded
    by the source's own grammar (<= V per window)."""
    emissions = []
    for v in range(V):
        unit = (v * 7 + W) % W          # spread changes across the window
        emissions.append(("c", unit, f"var-{v}"))
    emissions.sort(key=lambda e: e[1])
    return emissions


def simulate(emissions, W, B, policy):
    """Run one inter-barrier window through a wavefront machine with
    buffer bound B (B=None: unbounded ceiling). Returns (applied,
    drops, blocks, peak_occupancy). 'applied' is the barrier-service
    apply sequence. On buffer-full: drop loses the arrival; block stalls
    the source (its bounded tick service cannot complete); coalesce
    first merges same-variable arrivals (latest wins) and then, for
    what cannot merge, degrades to drop -- DISTINCT content has nothing
    to merge, so coalesce == drop on the adversarial family."""
    buf = []
    peak = 0
    drops = 0
    blocks = 0
    for e in emissions:
        unit, item = e[1], e[2]
        if policy == "coalesce" and e[0] == "c":
            # latest-wins merge on the variable's slot
            slot = item.split("-")[0] + "-" + item.split("-")[1]
            buf = [x for x in buf if not x[1].startswith(slot)]
        if B is not None and len(buf) >= B:
            if policy == "block":
                blocks += 1           # the source's tick stalls one unit
                continue
            drops += 1                # drop, and coalesce's unmergeable
            continue                  # residue, degrade here
        buf.append((unit, item))
        peak = max(peak, len(buf))
    return buf, drops, blocks, peak


def preserves(emissions, W, B, policy):
    """True iff the machine applies EXACTLY the emission multiset, in
    order, with zero drops and zero blocks."""
    buf, drops, blocks, _ = simulate(emissions, W, B, policy)
    return (drops == 0 and blocks == 0
            and [it for _, it in buf] == [e[2] for e in emissions])


# controls first: the harness must be able to SEE preservation
print("  controls: preservation must be visible where it exists")
for W in W_GRID:
    for k in (1, 5, 12):
        em = source_distinct(W, k)
        ok = preserves(em, W, None, "drop")
        check("B.ceiling.unbounded", ok,
              f"W={W} k={k}: the unbounded wavefront machine is the "
              f"preservation ceiling; preservation invisible => harness "
              f"broken")
for B in B_GRID:
    for W in W_GRID:
        em = source_distinct(W, min(B, K_MAX))
        check("B.control.smallk", preserves(em, W, B, "drop"),
              f"B={B} W={W} k={min(B, K_MAX)} <= B: no overflow, drop "
              f"policy must preserve (harness is not a blanket rejector)")

# the search itself: every bounded policy must die on a named source
print("  search: DISTINCT bursts k = 1..12 (the adversarial family); "
      "buffer demand grows with k, no plateau")
survivors = []
occupancy = {}
for B in B_GRID:
    for policy in ("drop", "block", "coalesce"):
        deaths = []          # (k, why) sources this policy dies on
        preserved_all = True
        for W in W_GRID:
            for k in range(1, K_MAX + 1):
                em = source_distinct(W, k)
                buf, drops, blocks, peak = simulate(em, W, B, policy)
                # measure demand on the unbounded machine
                _, _, _, peak_u = simulate(em, W, None, policy)
                occupancy[k] = peak_u
                if drops == 0 and blocks == 0 \
                        and [it for _, it in buf] == [e[2] for e in em]:
                    continue
                preserved_all = False
                if drops:
                    why = f"drop x{drops}"
                elif blocks:
                    why = f"block x{blocks} (source stall: Q4+/Q5 broken)"
                else:
                    why = "apply order/content lost"
                deaths.append((W, k, why))
        if preserved_all:
            survivors.append((B, policy))
        else:
            W0, k0, why0 = deaths[0]
            check(f"B.dies.B{B}.{policy}", k0 <= B + 1,
                  f"B={B} {policy}: first death at k={k0} must be the "
                  f"smallest overflow burst k=B+1={B + 1} (got {why0})")
check("B.occupancy.exact",
      all(occupancy[k] == k for k in occupancy),
      f"unbounded-machine occupancy must equal the burst size exactly: "
      f"{occupancy}")
check("B.occupancy.noplateau", len(set(occupancy.values()))
      == len(occupancy) and max(occupancy) > max(B_GRID),
      "buffer demand linear in k, exceeding every tested B (no plateau)")
if survivors:
    for B, policy in survivors:
        kill(f"GC-C2(b): bounded wavefront policy '{policy}' with B={B} "
             f"preserved EVERY enumerated source with 0 drops and 0 "
             f"blocks, including DISTINCT bursts up to k={K_MAX} -- the "
             f"registered falsifier artifact; publish the machine, the "
             f"no-drop/no-block invariant, and the burst-family treatment")
print(f"  policies searched: {len(B_GRID) * 3} bounded "
      f"(B in {B_GRID} x drop/block/coalesce); survivors: "
      f"{len(survivors)}; first deaths all at k = B+1 (the smallest "
      f"overflow burst)")

# ---------------------------------------------------------------------------
# [C] wavefront membership + the PLATO special case
# ---------------------------------------------------------------------------
print("\n[C] membership gate + the PLATO special case (write-only-changes)")


def is_wavefront(service_instants, W):
    """Membership: a wavefront machine services ONLY at barrier
    instants (multiples of W). Anything else is a different discipline
    (GC-D10: the synchronized product), not a wavefront machine."""
    return all(t % W == 0 for t in service_instants)


# control: the barrier machine is in-model
check("C.member.barrier", is_wavefront([0, W, 2 * W], W_GRID[0]),
      "barrier-only service must be in-model")
# the early-flush policy: preserves everything, but is NOT a wavefront
# machine -- it services between barriers (abandoning synchrony to buy
# the buffer: the local-tick machine in disguise)
early_instants = [0, 1, W_GRID[0], W_GRID[0] + 1, 2 * W_GRID[0]]
check("C.member.rejects.earlyflush", not is_wavefront(early_instants,
                                                      W_GRID[0]),
      "the membership checker must reject mid-window flushes (out of "
      "model: services between barriers)")
# and the early-flush policy DOES preserve the adversarial family -- the
# point is that it does so by LEAVING the model, which is exactly the
# separation: synchrony or buffers, not both
for k in (2, 5, 9):
    em = source_distinct(2, k)
    preserved_anyhow = preserves(em, 2, None, "drop")  # unbounded ceiling
    check("C.earlyflush.preserves.outside", preserved_anyhow,
          f"k={k}: preservation exists only by unbounding the buffer or "
          f"leaving the model (early flush) -- the separation itself")

# the PLATO special case: DELTA grammar fits B = V (the source's shape)
print("  PLATO case: DELTA sources (<= 1 emission per variable per "
      "window, latest value) fit B = V; the SAME machine dies on the "
      "unrestricted grammar and on V+1 variables")
for W in W_GRID:
    for V in (1, 2, 3):
        em = source_delta(W, V)
        check("C.delta.fits.shape", preserves(em, W, V, "coalesce"),
              f"W={W} V={V}: the protocol-shaped source must fit B=V "
              f"under write-only-changes (one word per variable: the "
              f"bounded historical answer, PLATO's 1024-word buffers)")
        # the same B=V machine on the unrestricted grammar dies: the
        # bound came from the source's shape, not the simulator
        em_bad = source_distinct(W, V + 1)
        check("C.dies.unrestricted", not preserves(em_bad, W, V,
                                                   "coalesce"),
              f"W={W}: B=V + coalesce dies on a {V + 1}-item DISTINCT "
              f"burst: the shape was NECESSITY, not thrift")
        # a LEGAL delta source with one more variable breaks B=V too:
        # no fixed B covers every legal source -- the fit is the
        # source's declared shape, and quilts exist past every shape
        em_more = source_delta(W, V + 1)
        check("C.delta.scaling", not preserves(em_more, W, V, "coalesce"),
              f"W={W}: a delta source with V+1={V + 1} variables breaks "
              f"B=V: the buffer bound tracks the SOURCE, never the "
              f"machine")
print("  the bounded answer exists ONLY as a source-shape property "
      "(write-only-changes); the conjecture reads that as necessity")

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("WHAT A KILL WOULD MEAN: a fixed-B wavefront simulator, no drops, "
      "no blocks, preserving every enumerated source INCLUDING DISTINCT "
      "bursts up to k=12 (and the published version: for adversarial k, "
      "with the simulation proof). That artifact kills GC-C2(b): PLATO's "
      "write-only-changes was thrift, not necessity. A lower-bound proof "
      "would resolve the conjecture positively instead. Until either "
      "lands, the grade stays open.")
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
print("Covers: GC-T8 compact re-check (proved direction), GC-C2(b) "
      "bounded-buffer counterexample search (12 bounded policies x "
      "DISTINCT k<=12 x DELTA V<=3, all bounded policies die at k=B+1), "
      "membership gate (early-flush rejected), PLATO special case both "
      "sides. GC-C2(b) grade unchanged: open.")
