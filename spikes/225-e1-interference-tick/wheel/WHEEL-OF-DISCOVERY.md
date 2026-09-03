# THE WHEEL OF DISCOVERY — standing experimentation engine
*Casey directive 2026-09-02 21:56: "I want more experimentations — create a wheel of discovery with your agents."*

The wheel is a recurring spin: each cycle picks one spoke, dispatches an agent lane to run
a real small-scale experiment on that spoke, logs the result here, and — when a spoke pays
off — bolts on new spokes. No floats, fixed seeds, booked failures, always.

## The spokes (rotate in order; the spin index lives in WHEEL-LOG.md)

1. **METROLOGY** — measure a fabric parameter the harness assumes (latency, channel
   period, refractory time, noise floor). Blades slide until they log. *Seeded by:
   lag metrology (kimi/opencode, replicated).*
2. **ADVERSARY** — put a liar, a jammér, a free-rider, or a mute inside the fabric and
   see what the invariants catch. *Seeded by: glm-1 byzantine twin, opencode zombie audit.*
3. **ALPHABET** — quantization floors: bit-width, ternary, Z₃/Z₅ gears, cap sweeps.
   *Seeded by: opencode quanta floor, kimi q_tern_dice.*
4. **TOPOLOGY** — group/lattice structure: rings, dihedral, hex, N-twin fan-out, K-axis.
   *Seeded by: glm-3 K-reversal + capacity wall, claude group-criticality falsification.*
5. **CONSERVATION** — invariants and ledgers: mass closure, toll caps, debt identities,
   annuity accounting. *Seeded by: glm-3 annuity ledger, opencode I1/I2.*
6. **REGIME** — calm/stress boundaries, hysteresis, regime-motion, controller switching.
   *Seeded by: REGIME-META, kimi lag-compensation regime flip.*
7. **COUPLING** — cross-mechanism composition: phase×decay, decay×dice, trust×lag,
   sort×admission. Wheels within wheels. *Seeded by: claude phase-decay, glm-3 controller.*
8. **DEQUANT** — the §10 cheat-code probes: what quantum-flavored claim survives integer
   sampling? Book every boundary honestly. *Seeded by: glm-2 13ppm walk.*
9. **SILICON** — one T-item from NOVEL-ENHANCEMENTS.md advanced one rung (lint→sby→synth).
   *Seeded by: T1–T15 program.*
10. **WILDCARD** — free spoke: the lane invents its own hypothesis from the week's open
    questions. Serendipity quota.

## Spin protocol (the cron lane's job each cycle)
1. Read WHEEL-LOG.md tail → next spoke index (LCG advance, mod 10 — deterministic).
2. Read RESEARCH-AGENDA.md + the spoke's seeded sheets for what's open.
3. Spawn ONE experiment lane (GLM-5.3) with a tight brief: hypothesis, harness pointer
   (e1.py/arena.py/rtl/), integer-only, fixed seeds, run-it-for-real, write to
   `spikes/225-e1-interference-tick/wheel/SPIN-<n>-<spoke>.md`.
4. On result: log one block to WHEEL-LOG.md — spin #, spoke, verdict (VALIDATED /
   FALSIFIED / MIXED / INCONCLUSIVE), headline number, and whether a new spoke is proposed.
5. A spoke that produces a confirmed finding twice gets a standing upgrade into the
   overnight queue; a spoke that falsifies twice in a row still stays — negative results
   are first-class.

*Doctrine: sweeps propose, blades dispose. The wheel never deletes a spoke — it banks the runout.*
