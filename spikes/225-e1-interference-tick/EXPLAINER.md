# Why the Model Arena Is Mechanistically Novel

*A short explainer for sharing — the full data lives in this directory (arena-v2.txt, ledger-results.txt, VARIETY-LEDGER.md).*

We ran a self-improvement loop where small AI models (2B-scale, on a local consumer GPU) compete to design strategies for a control problem, with a deterministic simulator as the only judge — models never grade each other's work. Three things make it mechanistically novel:

## 1. The ratchet fixes the classic failure of iterative improvement

When models revise after seeing a leaderboard, they abandon their own best work under pressure — we watched champions regress from 83% to 78% because "revising" felt obligatory. The fix is per-agent memory: your best-ever score is locked in; a new proposal only replaces it if it is measurably better. **Competition without amnesia.**

## 2. The Variety Ledger attacks leaderboard monoculture

Normal rankings test one scenario and crown one winner — which quietly destroys every other approach right before the environment changes. Instead, every strategy is scored across *multiple regimes* (calm and stressed) and banked if it is optimal on *any* metric axis. Result: the "losing" strategy was the undisputed specialist for the calm regime. **Score became a query ("who wins here?"), not a verdict.**

## 3. Small synergistic teams beat star rosters

The biggest models failed to produce valid output at all; a 2-billion-parameter model found a strategy 10 points better than the human hand-tuned one, and two tiny models independently converged on the same optimum without communicating. **Population diversity plus objective selection beat scale.**

## The one-liner

It's an evolutionary algorithm where the mutations are written by AI models, the selection pressure is a physics simulator instead of a vibe, and the gene pool is deliberately saved instead of collapsed.

The loop — propose → score → ratchet → bank variety → call the right play for the current regime — is now a standing, reusable discipline. Runs free at the margin on local hardware.

*Context: this arena tests strategies from paper 225 ("The Batten Is the Wave") — integer-only analog computation via constraint superposition. See ../../papers/225-the-batten-is-the-wave.md.*
