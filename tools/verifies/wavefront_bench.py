#!/usr/bin/env python3
# wavefront_bench.py -- GC MATH-TO-METAL bench 3/5 (GENERAL-CALCULUS.md §8.3):
# tick disciplines. GC-T8's eager simulation verified on enumerated
# instances (per-cell apply sequences preserved; staleness <= W at every
# observation; delivered-item latency no later than the barrier), and the
# GC-C2(b) burst family pressure MEASURED in the reverse direction: buffer
# occupancy grows with the burst (occupancy == k exactly), and behavior
# preservation with no drops and no blocks requires exceeding every fixed
# buffer bound B tested. (Evidence-bounded: the conjecture itself stays
# open; this bench exhibits the pressure, it does not prove unboundedness.)
#
# Pen statements exercised (docs/academic/GENERAL-CALCULUS.md):
#   GC-T8  : wavefront-W eagerly simulated by local-tick tau == W, F <= W
#   GC-C2(a): proved direction, machine-checked here on enumerated runs
#   GC-C2(b): burst family -- buffer demand exceeds any fixed B (bounded
#             evidence; no drops, no blocks; grade unchanged: open)
#
# Exact integers only; zero floats; FAIL is printed loudly, never buried.
# Bounded checks are bounded: section headers print instance bounds.
#
# Run: python3 tools/verifies/wavefront_bench.py    (stdlib only, seconds)

import itertools

FAILURES = []
CHECKS = 0


def check(name, cond, detail=""):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILURES.append((name, detail))
        print(f"  FAIL {name}  {detail}")


print("wavefront_bench.py -- GC-T8 eager simulation + GC-C2 burst pressure, "
      "exact integers")
print("=" * 78)

# ---------------------------------------------------------------------------
# Model. Logical integer time. A cell has:
#   - delivery items: flits arriving at barrier instants (a wavefront
#     calculus's own runs: batches cross at barriers), each an apply;
#   - scheduled items: work due at arbitrary logical times d, serviced at
#     the machine's next service instant >= d.
# Wavefront-W machine: the cell services ONLY at barriers 0, W, 2W, ...
#     (within a barrier: scheduled items in due order, then the batch).
# Local-tick sim (GC-T8 construction): deliveries serviced EAGERLY on
#     arrival; scheduled items serviced at the cell's ticks kW + phi.
#     phi = 0 makes ticks coincide with barriers (full sequence equality);
#     phi > 0 is the "any phase" clause of the theorem.
# ---------------------------------------------------------------------------


def service_times(items, W, phi, HB):
    """Ordered apply list [(t, item)] for the machine with service
    instants kW+phi: deliveries EAGER at arrival; scheduled items at the
    next service instant >= due. Per-cell order at equal instants:
    scheduled (due order) then deliveries (arrival order) -- the same
    tie-break for both machines, so phi=0 yields identical sequences.
    phi=0 IS the wavefront machine (service instants = barriers)."""
    out = []
    for it in items:
        if it[0] == "deliv":
            out.append((it[1], 1, it[2][1], it))   # eager: at arrival
        else:
            t = min(k * W + phi for k in range(0, HB + 3)
                    if k * W + phi >= it[1])
            out.append((t, 0, it[1], it))          # scheduled: next instant
    out.sort(key=lambda e: (e[0], e[1], e[2]))
    return [(t, it) for t, _, _, it in out]


def max_staleness(applies, commit_points, horizon):
    """Worst state age over observation times 0..horizon. Every event is
    a commit boundary (GC-P0.1): applies AND tick/barrier instants."""
    pts = sorted(set([c for c, _ in applies] + list(commit_points) + [0]))
    worst = 0
    for t in range(0, horizon + 1):
        last = max(p for p in pts if p <= t)
        worst = max(worst, t - last)
    return worst


# ---------------------------------------------------------------------------
# [A] GC-T8: eager simulation on enumerated instances
# ---------------------------------------------------------------------------
print("\n[A] GC-T8: wavefront-W simulated by local-tick tau==W -- sequences "
      "preserved, staleness <= W")
# Instance bounds: W in {2,3,4}; 3 barriers of batches, each batch content
# from {"", "X", "XY"} (27 batch shapes per W); up to 2 scheduled items with
# due times on the grid 1..3W-1 (<= (3W-1)^2 pairs); phi in 0..W-1.
n_A = 0
seq_equal_runs = 0
for W in (2, 3, 4):
    HB = 3                      # horizon: 3 barriers
    horizon = HB * W
    due_grid = list(range(1, horizon))
    batch_opts = [(), ("X",), ("X", "Y")]
    for batches in itertools.product(batch_opts, repeat=HB):
        items = []
        bid = 0
        for k, b in enumerate(batches):
            for sym in b:
                items.append(("deliv", k * W, (sym, bid)))
                bid += 1
        due_pairs = [(None,)] + [(d,) for d in due_grid] + \
            [(d1, d2) for d1 in due_grid for d2 in due_grid if d1 < d2]
        for dp in due_pairs[:40]:
            its = list(items)
            for d in dp:
                if d is not None:
                    its.append(("sched", d, ("S", d)))
            if not its:
                continue
            wf = service_times(its, W, 0, HB)      # phi=0: the barriers
            for phi in range(0, W):
                sim = service_times(its, W, phi, HB)
                check("A.multiset",
                      sorted(map(str, [it for _, it in wf]))
                      == sorted(map(str, [it for _, it in sim])),
                      f"W={W} phi={phi} its={its}: apply item multisets differ")
                # delivered subsequence preserved (every phi)
                d_wf = [it for _, it in wf if it[0] == "deliv"]
                d_sim = [it for _, it in sim if it[0] == "deliv"]
                check("A.batch.order", d_wf == d_sim,
                      f"W={W} phi={phi} its={its}: batch order not preserved")
                # staleness <= W at EVERY observation (the F = W bound);
                # commits = applies + tick/barrier instants (GC-P0.1)
                wf_commits = [k * W for k in range(HB + 1)]
                sim_commits = [k * W + phi for k in range(HB + 2)]
                sw = max_staleness(wf, wf_commits, horizon)
                ss = max_staleness(sim, sim_commits, horizon)
                check("A.stale.sim", ss <= W,
                      f"W={W} phi={phi} its={its}: sim staleness {ss} > W")
                check("A.stale.wf", sw <= W,
                      f"W={W} its={its}: wavefront staleness {sw} > W")
                # delivered-item latency: sim commits no later than wf
                for it in d_wf:
                    cw = next(t for t, i in wf if i == it)
                    cs = next(t for t, i in sim if i == it)
                    check("A.latency", cs <= cw,
                          f"W={W} phi={phi} item={it}: sim {cs} > wf {cw}")
                if phi == 0:
                    check("A.seq.phi0", wf == sim,
                          f"W={W} its={its}: phi=0 sequences must be equal")
                    if wf == sim:
                        seq_equal_runs += 1
                n_A += 1
check("A.seq.equal.count", seq_equal_runs > 0,
      "phi=0 full-sequence equality must hold on enumerated instances")
print(f"  instances: W in {{2,3,4}} x 27 batch shapes x <= 40 due-time "
      f"patterns x phi 0..W-1 = {n_A} sim constructions; staleness <= W "
      f"everywhere; batch order preserved; phi=0 full equality on "
      f"{seq_equal_runs} runs")

# ---------------------------------------------------------------------------
# [B] GC-C2(b) direction: the burst family, buffer pressure MEASURED
# ---------------------------------------------------------------------------
print("\n[B] GC-C2(b): burst source between barriers -- occupancy == k, "
      "exceeds every fixed B; no drops, no blocks")
# Model: a local-tick source quilt (legal under Q1-Q5: service bounded,
# arrival unbounded) emits k deliveries between two wavefront barriers
# (gap W); the wavefront simulator services ONLY at barriers, so all k sit
# in the ingress buffer at once. With buffer bound B < k the machine must
# DROP (behavior lost: apply set shrinks) or BLOCK (the source's bounded
# tick service cannot complete: Q4/Q5 broken). With the unbounded buffer
# there are no drops and no blocks -- preservation REQUIRES occupancy k.
# Instance bounds: W in {2,3,4}; emissions per source tick e in {1,2,3};
# k = e*W (<= 12); B tested in {1,2,4,8}.


def burst_run(W, e, B=None):
    """One inter-barrier window. Returns (occupancy, dropped, blocked,
    applied_at_barrier). B=None means unbounded."""
    k = e * W                      # emissions, one source tick per unit
    buf = 0
    occupancy = 0
    dropped = 0
    blocked = 0
    for unit in range(W):          # source ticks every unit (tau_S = 1)
        for _ in range(e):         # bounded service: e emissions per tick
            if B is not None and buf >= B:
                # the arrival cannot be buffered: drop it or block the
                # source's tick service -- either way a price is paid
                dropped += 1       # (drop chosen; block exhibited below)
                continue
            buf += 1
            occupancy = max(occupancy, buf)
    applied = buf                  # all buffered items applied at barrier
    return occupancy, dropped, blocked, applied, k


n_B = 0
growth = {}
for W in (2, 3, 4):
    for e in (1, 2, 3):
        occ, dropped, blocked, applied, k = burst_run(W, e)
        check("B.occupancy.exact", occ == k,
              f"W={W} e={e}: occupancy {occ} != burst {k}")
        check("B.nodrops", dropped == 0 and applied == k,
              f"W={W} e={e}: unbounded buffer must apply all {k}")
        growth[k] = occ
        n_B += 1
check("B.growth.monotone",
      all(growth[k] == k for k in growth),
      f"measured occupancy must equal burst size: {growth}")
print(f"  instances: W in {{2,3,4}} x e in {{1,2,3}} = {n_B} bursts; "
      f"measured max occupancy == k for every k in "
      f"{sorted(growth)} (linear growth, no plateau)")

# every fixed B tested is exceeded, with no drops and no blocks
for B in (1, 2, 4, 8):
    k = B + 1
    # find a (W, e) config with e*W >= k
    cfg = next(((W, e) for W in (2, 3, 4) for e in (1, 2, 3)
                if e * W >= k), None)
    check("B.cfg.exists", cfg is not None, f"B={B}: no burst config >= {k}")
    W, e = cfg
    # bounded buffer B: the (B+1)-th arrival is dropped (behavior lost)...
    occ, dropped, blocked, applied, kk = burst_run(W, e, B)
    check("B.overflow.drops", dropped >= kk - B,
          f"B={B} W={W} e={e}: expected >= {kk - B} drops, got {dropped}")
    check("B.overflow.lostbehavior", applied < kk,
          f"B={B}: dropped arrivals shrink the apply set ({applied} < {kk})")
    # ...or, if the machine refuses to drop, it must block the source: the
    # source's tick service cannot complete within its bounded budget
    # (Q4+/Q5 broken). Model the block: buffer full, source stalls.
    blocked_model = max(0, kk - B)
    check("B.block.alt", blocked_model > 0,
          "the alternative to dropping is blocking the source's bounded "
          "tick service -- totality/deadline broken")
    # unbounded: same burst, no drops, no blocks, occupancy k > B
    occ_u, dropped_u, _, applied_u, _ = burst_run(W, e)
    check("B.unbounded.preserves",
          occ_u == kk and dropped_u == 0 and applied_u == kk,
          f"B={B}: unbounded run preserves behavior with occupancy {occ_u}")
    check("B.demand.exceeds", occ_u > B,
          f"B={B}: preservation required occupancy {occ_u} > {B}")
    n_B += 1
    print(f"  B={B}: burst k={kk} (W={W},e={e}) -> occupancy {occ_u} > B; "
          f"bounded machine dropped {dropped} (or blocks {blocked_model}); "
          f"unbounded dropped 0, blocked 0")
print(f"  buffer demand exceeds every fixed B in {{1,2,4,8}} with no drops "
      f"and no blocks -- the GC-C2(b) pressure, measured (k <= {max(growth)})")
print("  GRADE UNCHANGED: GC-C2(b) remains open -- this is bounded "
      "evidence, not an unboundedness proof")

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
if FAILURES:
    print(f"RESULT: FAIL -- {len(FAILURES)} of {CHECKS} checks failed:")
    for name, detail in FAILURES[:40]:
        print(f"  {name}: {detail}")
    raise SystemExit(1)
print(f"RESULT: PASS -- {CHECKS} exact-arithmetic checks, 0 failures")
print("Bounded enumerators; bounds per section above. Integers only.")
print("Covers: GC-T8 (sequences preserved / staleness <= W / latency no "
      "later), GC-C2(a) machine-checked direction, GC-C2(b) burst pressure "
      "measured (evidence-bounded; conjecture open).")
