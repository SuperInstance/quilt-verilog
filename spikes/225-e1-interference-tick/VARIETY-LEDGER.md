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

## Re-banking — O1 K-replay (2026-09-02, dev round 1; see inventors-derby/O1-K-REPLAY.md)

The K-axis replay (S3/F13) forced the ledger's first champion change and a calm re-key.
All changes verified on holdout seeds (11, 313, 8888); 10/10 byte-match control gates
passed before any new number was read.

- **Stress champion: static probe `K=1, pd=2, d=16` interference — 96.1%** (old champion
  granite K5/pd4/d16: 93.2%). Not a crown swap but a **triple-axis Pareto domination**
  (pct 96.1>93.2, debt 121,762<132,823, maxE 33<38); zero seed variance across all 8
  seeds run. It also dominates the impulse-d16 unseen entry (96.0/139,949/61).
- **Stress debt crown: K=2/pd=2/d16 (debt 111,224)** — debt and pct no longer travel
  together; the stress Pareto front is K1/pd2 (pct+maxE), K2/pd2 (debt), K3/pd4
  (interior). Old champion kept in the structural bank — first LLM-crowned champion,
  lineage preserved.
- **Calm (Δ=6) re-key: K=1/pd=2 interference, 98.0% vs impulse 56.6** — the calm
  specialist seat flips from sequential to short-K interference; holdout 98.0 vs 57.3.
  Calm (d12) stays impulse (98.0 tie, debt 33,514 ≪ 57,264). The calm boundary is a
  deadband-to-conflict property, not a mode property.
- **Standing bias booked: grid anchoring.** No LLM contestant has ever proposed K≤3
  interference (arena v2: all K∈{4,5,8}; v3 widened rounds: K=4, then a mode jump).
  Static non-LLM probes are now a permanent arena fixture; the ledger banks results,
  not lineages. Schema fix landed: arena.py v3, K∈{1..8}.
- Playbook update: read the deadband-to-conflict ratio, then call the tail —
  conflicted room → shortest tails (K≤2); calm or wide room → no tails (or K=1/pd=2,
  which won both frames of its own — the new play is "quantized impulse", pending
  its mode-classification question).
