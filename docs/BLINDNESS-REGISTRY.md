# BLINDNESS-REGISTRY.md — what this fabric cannot see

*Fleet-wide format (IDEATOR nudge, 2026-09-03), instantiated here for
quilt-verilog. Shared schema — one row per twin-class the system's own
observables cannot separate:*

```
what-cannot-be-seen | why (field width / mapping / uninstrumented path) | priced-by-whom
```

This is the hardware instance of the same phenomenon zeroclaw §6
formalizes as **blindness-groups** (observables that cannot separate two
distinct protocol states — the Δ₀ pigeonhole: the room's visible
dynamics cannot see certain twins). Here the room is silicon, and the
twins are "file that says X" vs "file that says Y" where the loader FSM
lands both on the same state. The Python verifier's issue list is the
sibling registry under a different name: rows where verify is *stricter*
than silicon are exactly rows where a blindness exists.

## Registry (quilt-verilog)

| what-cannot-be-seen | why | priced-by-whom |
|---|---|---|
| tpw ≥ 32 from tpw&31 | `o_tick_tpw` is 5 bits; epoch latches `tpw&31`. tpw=40 boots as 8. Python verify now hard-rejects (e6f746d); RTL tolerance by design | boot_fuzz HW_BLIND; writer 0..31 check |
| age ≥ 2²⁴ from age&2²⁴−1 | Hyperbola age wraps at 24 bits (AGEW) in RTL; QUF record carries u32. Diverges only after 16.7M unticked ticks on a wh=0 edge | BACKEND-NOTES "What remains weak"; no fuzz row yet — **booked: hostile age=2²⁴ case in boot_fuzz** |
| digest-corrupt payload from honest payload | q_uf_loader has no sha engine; a corrupted-but-structural file boots with wrong dials. Python paths all sha-protected | boot_fuzz classifies digest-mismatch HW-blind on purpose; loader CRC32 = open weakness |
| kind≠0 sections from unknown sections | verify polices `kind≠0`; loader ignores (forward-compat by design) | HW_BLIND "non-standard kind" |
| duplicate section names | verify rejects; loader last-wins/ignores | HW_BLIND "duplicate section name" |
| tick_period-lie files | verify cross-checks `tick_period == 2**tpw`; loader never reads tick_period | HW_BLIND "tick_period" |
| cell_count over-provision | files with `cell_count > MYCELL` boot on RTL with only cell MYCELL's dials landed | boot_fuzz BOOT oracle extracts row MYCELL |

## Mined candidates (battery corpus sweep, this tick)

Swept every output-width mismatch between `q_uf_loader.v` port widths and
the quf.py verifier's checked ranges. Fields whose *writer* path is
already range-checked (dials u16, routing u8, edge src/dst/mode/slot)
have no blindness row: Python rejects before silicon can disagree. The
two live rows above (tpw fixed this tick, age open) are the complete
current set for the loader; the digest row is a structural blindness
(no instrument at all), which is why it prices highest.

## Cross-repo pointers

- **zeroclaw §6**: blindness-group clauses — the Δ₀ pigeonhole result;
  this registry is that formalism's hardware twin.
- **quilt-deck**: divergence-oracle coverage gaps (frame-#36 DIVERGENT
  verdict, cosim lane) — deck rows to be appended under the same schema.
- **SUBSTRATE-LADDER.md** (spikes/225-e1-interference-tick/): the
  four-substrate disagreement table is this registry made dynamic —
  each rung's blindness is what makes triangulation work.

## Doctrine

"Here is the complete map of what this fabric cannot see" is a stronger
doc than any feature list. Rule going forward: **a new HW_BLIND row or a
new verify-vs-RTL asymmetry MUST add its row here the same tick.**
