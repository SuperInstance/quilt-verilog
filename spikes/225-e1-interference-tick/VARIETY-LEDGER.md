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

— doctrine entry, E1 arena, 2026-09-02
