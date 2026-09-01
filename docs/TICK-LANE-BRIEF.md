# TICK-LANE BRIEF — The Tick Deserves Better

You are the TICK lane for quilt-verilog. Repo: /home/eileen/projects/quilt-verilog (master at 3157b3d). Branch: `tick-depth`. DeepSeek/DeepInfra REVOKED — do not call. z.ai primary; `claude -p` for adversarial review; tmux `arena-kimi`/`arena-opencode`/`arena-claude` available for RTL feasibility questions (recreate: `tmux new-session -d -s arena-claude -c /home/eileen/projects/quilt-verilog 'claude'`).

## Captain's directive (2026-08-31 20:25)
"The tick is special: it cannot be starved. A pending tick suppresses ingress acceptance (`ci_ready`) until serviced — non-deferrable time, proven under permanent ingress flood (docs/FORMAL-PROOFS.md §4). One tick traced end-to-end through the RTL: docs/THE-TICK.md." — THIS part of quilt-verilog needs further work.

## Read first
docs/FORMAL-PROOFS.md (§4 especially), docs/THE-TICK.md, rtl/ (the tick + ci_ready logic), tb/ (existing suites), docs/BACKEND-NOTES.md.

## Work items (in priority order)
1. **Quantitative tick latency**: §4 proves the tick cannot be STARVED, but starvation-freedom is qualitative. Derive and PROVE (or measure via cosim) the WORST-CASE tick service latency under permanent ingress flood: what is the bound on cycles from tick-pending to tick-serviced as a function of flit size, ring position, and ingress rate? State it as a theorem with the suppression mechanism's arithmetic made explicit. If a clean closed-form doesn't fall out, give the measured worst case at NCELL=2/4/8 with the flood program generator that already exists.
2. **Liveness formalization**: express tick-service as an sby liveness property (fairness on ci_ready suppression + eventual service) and close it in the existing toolchain. If liveness needs a fairness constraint, name the constraint and argue it's physical (hardware guarantees, not wishful thinking).
3. **THE-TICK.md depth**: the end-to-end trace should be the paper every visitor reads. Upgrade it: cycle-exact numbers from the cosim event streams (the infrastructure exists — tb_cosim_fabric.v records cycle-stamped events), every stage of the tick's journey (ingress suppression → arbitration → service → egress), annotated with WHICH formal property covers each stage. A reader should finish it understanding why non-deferrable time is the fabric's heartbeat and what breaks without it (cross-ref the 34,560 incident if the tick connection is real — check INCIDENTS.md).
4. **Adversarial pass**: `claude -p` hunting for a tick-starvation scenario the proof misses (e.g., interactions between the suppression rule and the coherence proposals' admission/needle mechanisms in docs/coherence-arena/ — would TOKEN-NEEDLE's token-holding or SELVEDGE's readout decay break the tick's guarantee? A protocol that starves the tick is disqualified — note this as a constraint on the arena verdict).
5. **Honesty**: every claim matches a measured number or a named proof obligation. Tapestry style: undersell in summary, evidence in body.

## Deliverables
- Extended docs/THE-TICK.md + §4 additions in docs/FORMAL-PROOFS.md (or a new docs/TICK-LATENCY.md if cleaner)
- Any new sby properties + sim programs committed
- Commit to branch `tick-depth`. Do NOT merge to master. Do NOT push.

## Report back
The latency bound (proven or measured, with numbers), sby liveness status, what the adversarial pass found (especially arena-protocol interactions), and the weakest remaining claim.
