# The Substrate Ladder — Python → C → Verilator → ESP32

*Cross-repo doc: quilt-verilog spike 225-E1 × quilt-deck Stage-1 cosim.
2026-09-03, written on the IDEATOR nudge while the connection is fresh.*

## The idea

A single algorithm — the E1 interference tick (integer pulse-superposition
snapping, paper 225 §6) — verified across independent implementation
substrates. Each rung of the ladder is a different language *and* a
different set of silent assumptions, so each rung can catch a different
class of bug. Agreement is not redundancy; it is triangulation.

| Rung | Substrate | Status | Divergence it caught |
|------|-----------|--------|----------------------|
| 1 | Python (`e1.py`) | reference | — (defines the contract) |
| 2 | C99 (`e1.c`) | 10/10 exact | **pulse-queue geometry bug** — the port encoded
the decay window against the wrong index base; caught by full-vector
comparison, fixed, documented in [DIVERGENCE.md](DIVERGENCE.md) |
| 3 | Verilator (deck `tb_deck_cosim.v`) | **OPEN — booked spike** | target: deck's frame-#36 DIVERGENT verdict |
| 4 | ESP32 (KimiCode porting notes → quilt-esp32 cells) | notes staged | pattern proven by quilt-esp32 oil-pressure cell (17/17 golden vectors host-side) |

## Why this matters to deck's frame #36

Deck's Stage-1 differential verdict is DIVERGENT at frame #36 (u8 bucket
overflow, X-inert verified), and its culprit-attribution section correctly
states the limitation: **reference = Python, because there was no third
oracle.** E1 is exactly the missing third substrate, and the E1 C-port
experience is exactly the bug class frame #36 smells like: a geometry
assumption (index base, bucket width, window edge) that two substrates
can share silently because the second was written *from* the first.

### Methodology handoff (the E1 divergence audit trail, as a template)

1. **Full-vector comparison, not spot checks.** 5 seeds × 2 arms, every
   counter compared (events, debt, cancellations, chatter, maxErr).
   A single divergent row is a finding, not noise.
2. **Characterize before reading the port.** The E1 bug was localized by
   asking *which invariant* broke (queue geometry) before looking at C.
3. **Fix the port, never the reference — unless the contract was wrong.**
   The reference defines the contract; a port fix changes the port.
   Changing the contract requires a documented reason (deck's u8 bucket
   overflow may be exactly this case — that's the attribution question).
4. **Document the divergence even after the fix.** DIVERGENCE.md is the
   artifact; the fix is almost a footnote. The geometry class is the
   payload.

## The one-tick story (hundred-boats framing)

Same tick, same integer contract, verified on a laptop Python process, a
gcc binary, an FPGA-bound Verilog netlist under Verilator, and eventually
a microcontroller in the wheelhouse. Each substrate that agrees makes the
contract more real than any single implementation can. Each divergence —
first-class, like deck's frame #36 and E1's queue bug — maps an edge of
where the assumption lived.

## Next concrete moves

- **Spike (booked):** port E1's pulse-queue tick to Verilog as a deck
  cosim engine → triple agreement (Python/C/Verilator) converts deck's
  "trust Python" into a triangulated reference.
- Deck: apply the audit-trail template to frame #36; if the culprit is
  the u8 bucket width itself, the *contract* changes and both Python and
  C move with it — that is a legitimate outcome, not a failure.

## The hostile-tpw row (2026-09-03, e6f746d) — one known-blind input, four substrates

A file that claims `tpw=40` when the hardware epoch field is 5 bits —
the sharpest exhibit yet of why the ladder exists. Same bytes, four
substrates, four different truths:

| Rung | What tpw=40 does | Blindness |
|------|------------------|-----------|
| 1 Python | **REJECTED** post-e6f746d (verify: "tpw 40 exceeds 5-bit hw epoch field"); pre-fix it verified clean — the reference substrate had the blindness first | verifier range |
| 2 C99 | golden model follows quf.py semantics — rejects iff its quf port tracks rung 1 | port sync |
| 3 Verilator (loader) | **BOOTS, epoch latches tpw&31 = 8** — by design, registered HW-blind | 5-bit field: cannot see the claim |
| 4 ESP32 | *whatever the silicon actually does* — the rung the ladder exists to find out | real hardware |

The disagreement is not a bug — it is the map. Python's strictness,
the loader's tolerance, and silicon's eventual verdict are three
observations of one blindness class; see
[docs/BLINDNESS-REGISTRY.md](../../docs/BLINDNESS-REGISTRY.md) for the
full twin-table and zeroclaw §6's formal twin (blindness-groups).
