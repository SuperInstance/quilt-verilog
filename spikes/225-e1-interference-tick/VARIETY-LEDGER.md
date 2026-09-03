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

## Roster doctrine — the negative space (Casey, 2026-09-02 17:06)

> The best teams aren't always made of superstars. Sometimes stars aren't
> able to synergize — like nameless elite who know each other's names very
> well, and how each has grown into the negative space of what they are
> especially good at where their teammates need it.

Observed in this very arena: the superstar field (LFM 2.6B, qwen3:8b) failed
to produce a single parseable design, while the nameless roster — two small
LFM models and granite 2b — converged, held, and beat the human hand-tune.
Synergy beats stardom, empirically, at 2B scale. Fleet application: the
arena should prefer rosters that GROW INTO each other's gaps (a specialist
completing what a generalist leaks) over stacking the largest models; and
agent-to-agent familiarity (knowing each other's names and tendencies) is a
capability — the elephant's per-counterparty dial memory is how the fleet
practices it.

— doctrine entry, E1 arena, 2026-09-02
