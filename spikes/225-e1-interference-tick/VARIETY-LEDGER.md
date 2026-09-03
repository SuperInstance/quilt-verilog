# The Variety Ledger — arena doctrine (Casey, 2026-09-02 16:56)

> "The system should value saving variety of logic too. In an open-platform,
> score doesn't always mean the same thing from a step-back and look at the
> wider data-view."

## The principle

A leaderboard is a narrow window. It scores strategies under ONE regime
(stress params, one corpus) and one metric (% within deadband). Step back
and the wider data-view shows:

- **Regime relativity.** E1 proved this already: interference wins under
  conflict, impulse wins in calm. The same strategy changes rank when the
  environment changes. A single-regime champion is a local truth wearing a
  crown.
- **Metric relativity.** Lowest debt, tightest maxErr, best calm behavior,
  graceful degradation — different metrics crown different strategies, and
  all of them are real virtues on an open platform where tomorrow's regime
  is unknown.
- **Logic variety as an asset.** A structurally different approach (sequential
  vs pulse-superposition, later: batten-relaxation) is worth banking even when
  it never tops the table — it is the only seed that grows into the next
  regime's winner. Optimize hard and the population collapses to one genotype;
  then the regime shifts and nobody survives.

## The mechanism (arena v3)

After each round, strategies are banked — not ranked away — by:

1. **Pareto banking**: any strategy Pareto-optimal on (pct_within ↑, debt ↓,
   maxErr ↓) enters the ledger, whatever its leaderboard rank.
2. **Regime banking**: strategies are additionally scored on the calm regime
   (delta=6, drift=3) — a strategy that flips rank across regimes is recorded
   as a *regime-specialist* with both scores attached.
3. **Structural banking**: the best strategy of each distinct mode/logic stays
   in the ledger even if dominated everywhere — it is a saved logic, not a
   losing entry.
4. **The ratchet is personal, not global**: each agent's ratchet keeps its own
   best; the ledger keeps the fleet's variety. Competition refines lineages;
   the ledger prevents lineage collapse.

Champion selection is then *contextual*: the caller names the regime and the
metric, and the ledger answers with the right saved logic. "Score" becomes a
query, not a verdict.

## The Playbook Doctrine (Casey, 2026-09-02 17:01 — football plays)

> Plays are practiced depending on the other elements of the game at any
> given moment: ahead or behind (running to drain the clock and avoid
> interceptions vs long throws at higher risk). If the defense lines up
> wrong for the huddle pick, a fake hand-off gets swapped in at the line.
> Or different plays because of mismatched abilities on a specific team —
> like an opposite's known preferences.

Mapped onto the ledger:

- **Plays** = banked strategies. You practice (bank) many; you run one.
- **Game state** = regime (calm/stress ≈ ahead/behind). Play selection is
  mechanical from the ledger: read the state, call the specialist.
- **Reading the defense at the line** = online regime detection between
  ticks. The snap-debt rate IS the defensive alignment tell — debt climbing
  fast means the current play is being beaten; that is the audible trigger
  for a mid-loop swap (fake hand-off). No replay of history, no re-deriving
  strategy: the ledger holds the alternative and the swap is a lookup.
- **The opposite's known preferences** = per-counterparty knowledge. This is
  the elephant's dial memory: strategy selection keyed not just to regime
  but to WHO is on the other side of the snap pair — a known-noisy sensor,
  a known-drifting sim. Same playbook, personal tendencies scouted.
- **Practice squad** = structurally-banked logics that never start but keep
  the roster deep. You cannot audible to a play you cut.

The coordinator loop is therefore: **bank plays (variety) → read the field
(regime + opponent) → call the play (ledger lookup) → audible on debt (swap
trigger) → practice squad intact (no monoculture).** E4's field-adaptive Δ
is the first concrete play-call: the elephant's κ reading IS the down-and-
distance signal.

— doctrine entry, E1 arena, 2026-09-02

## Held-out seed confirmation (DEVIL nudge, 2026-09-03)

Objection upheld and answered: the arena's 5 seeds (1/7/42/1999/20260902)
are the SAME seeds the hand-tune was developed against — train-on-test
was the default hypothesis. Confirmation run on a DISJOINT pre-registered
held-out set (13/313/777/271828/90210, not derived from the dev base),
stress protocol identical (delta-sweep params per policy, drift=6, lat2=10):

```
policy             devStress%  heldStress%  heldCalm*%  worstHeld%  heldDebt  heldErr
impulse baseline        51.4         51.3        24.4        24.4    244237      61
hand interference       83.1         83.3        94.5        83.3    174786      39
granite champion        93.2         93.1        95.6        93.1    134036      38
```
*heldCalm here keeps lat2=10 (twin latency present, drift off) — a
different calm definition than the main ledger table; the decisive column
is heldStress vs devStress under the identical protocol.

Verdict: the 10-point gap REPRODUCES on unseen seeds (93.1 vs 83.3, a
0.1pt move from the dev-seed numbers = noise). Contamination does not
explain it. "granite3.1 2b > hand-tune under stress" is booked as REAL,
and granite also wins the held-out calm column — no regime flip. The
ratchet doctrine upgrade: **ratchets advance on dev seeds only after the
champion survives the held-out set; the held-out seeds are never shown
in prompts or leaderboards.**
