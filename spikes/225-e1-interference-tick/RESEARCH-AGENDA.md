# RESEARCH-AGENDA — The Single Ordered Agenda for the QTORCH Program

*Synthesized 2026-09-02 ~21:53 AKDT, Forge Lane, from: QTORCH-CHARTER.md (§0–§10 + epigraph),
docs/NOVEL-ENHANCEMENTS.md (T1–T15), the four RD dossiers on disk, and all six derby sheets
(INVENTIONS-{claude,glm-1,glm-2,glm-3,kimi,opencode}.md). Ordered: what runs first and why.
Undersold on purpose; every claim cites its sheet; failures are first-class entries.*

**Method note (honesty first).** The synthesis directive said "seven RD-*.md dossiers"; the spike
directory holds **four** (`RD-BEYOND-UTM`, `RD-PHYSICAL-SUBSTRATES`, `RD-SWARM-SUBSTRATE`,
`RD-SPREADSHEET-LINEAGE`) — a repo-wide `find` confirms no others exist. The agenda below is built
from what is actually on disk. "Confirmed" below means: an experiment that was **actually run** with
numbers, in this spike, tonight or earlier — not proposed, not sketched. Derby scripts live in
`inventors-derby/` (glm/kimi lanes checked in; claude's `exp1-3_*.py` at spike root; opencode's in
`/tmp/opencode/` — flagged: those are scratch, not banked; re-home them before anything depends on them).
**Verification pass (retry lane, 22:2x AKDT):** after the provider overload, a second lane re-read
all six sheets, all four dossiers, the charter, NOVEL-ENHANCEMENTS, README/DIVERGENCE/e7 RESULTS,
and spot-checked every number in §2–§6 against its cited source. No discrepancies found; file
stands as synthesized at 21:53.

---

## 1. Keel

THE-HUNDRED-HOOKS says every layer exposes its tick metadata to the layer below — a hundred hooks,
each a blade that slides until it logs [CHARTER §6]. Tonight six lanes each dropped a feeler gauge
into the same fabric and the seatings agree: the fabric is **Schrödinger's troller in integers** —
trolling = tick, pull = read, plinko = the ledger, fleet = the topology [CHARTER §6] — and the
program is the study of *where the wiggle ends* [epigraph, Casey 21:03]. The wiggle ended in eight
places tonight, with numbers: superposition beats impulse under conflict by 31 points (83.0 vs 51.9,
[README]); short-tail K=2 superposition beats it in *calm* too (92.1 vs 56.6, [glm-3 #3]) — the
published "impulse is the calm specialist" verdict was a K=8 grid artifact, independently exposed on
a second axis by [kimi #2]; the fabric measures its own twin latency exactly from its own fringes,
twice, by two lanes that never compared notes ([kimi #3], [opencode #1]); and the charter's own
§1.2 cofire primitive, run for the first time by three lanes, collapsed trust to zero in all of them
([glm-1 C], [kimi #1], [opencode #2]). Where the blade did not seat is as load-bearing as where it
did: the agenda below orders the seatings to confirm, the seams two lanes found independently
(replication outranks cleverness), the silicon rungs each idea must climb, and the questions the
charter raised that nobody has yet paid ticks for. Sweeps propose; blades dispose.

---

## 2. Confirmed findings (run with numbers only)

| # | Finding | Numbers | Sheet |
|---|---------|---------|-------|
| F1 | Integer pulse-superposition beats impulse snapping under twin conflict (stress, 5 seeds) | 83.0% vs 51.9% within-deadband; −20% events; −27% debt; maxErr 61→39; 538 ticks of net==0 both-signs-live cancellation | [README], [e1.py] |
| F2 | Cross-substrate byte-identity after contract pinning (Python ↔ C99) | 10/10 rows identical, 5 seeds × 2 arms; caught the queue-geometry bug class first | [README], [DIVERGENCE.md] |
| F3 | Interference is NOT a free lunch in calm (at the then-published params) | gentle: 45.5% vs 56.7% — **superseded in part by F13: artifact of K=8** | [README]; see [glm-3 #3] |
| F4 | Simulator-judged tournament: 2B model beats human hand-tune; ratchet holds; variety real | granite3.1-2b K=5/÷4/Δ=16: 93.2% vs human 83.1%; ratchet held 3/3 under revision pressure; 5/6 strategies Pareto-optimal somewhere; impulse calm-specialist 98.0% calm / 51.4% stress | [README], [arena-v2.txt], [ledger-results.txt] |
| F5 | Learned cells are per-substrate; class grain transfers (E7) | Jaccard 0.934–0.955 under 4× coarsening; ±1 dither flips zero routes; cross-model exact-cell Jaccard 0.013–0.047 vs null 0.000–0.009; domain-class LCS 2–3× null, 3/3 model pairs | [e7-embed-route/RESULTS.md] |
| F6 | Byzantine twin: superposition bounds adversarial drag; cancellation rate is a lie detector | maxDrag 61→27–34; lie-window cancel rate ×2–5 honest baseline on 5/5 seeds; recovery ≤100 ticks | [glm-1 A] |
| F7 | Bundle-capacity wall: superposition toxic past N=3 twins | interference true-residency 91%→10% by N≥4 (impulse flat ~51%); ~6.1 extra events/twin; cancellations peak N=4 then fall (saturation, not resolution) | [glm-1 B] |
| F8 | Charter §1.2 cofire, first run: self-locks on the fabric's echo, not the world | lag estimate 0/5 seeds; anti-cofire trough pinned at τ=3 (decay echo) 5/5; 22% of fires are same-tick opposite-sign antagonist pairs | [glm-1 C] |
| F9 | Queue archaeology: pulse queue is exact in time, dyadic-lossy in amplitude; self-audits container geometry | 64/64 tick attributions exact, 0 ghosts/losses; injected window-edge bug caught via 15 losses + zeroed age-3 census | [glm-1 D] |
| F10 | Dialometer (§9): boolean blades + coarse-then-fine recover latency and period at 9% of wave cost | zero-seatings [10, 250] (lag + period); scale-joint floor = 720 = exact odd-count; naive full bank pays 153% — procedures, not data types, carry the economy | [glm-2 #1] |
| F11 | Dequantized interference walk: integer superposition reproduces unitary statistics; E7 grain law does NOT transfer to linear superposition | 13 ppm TVD at identity grain (cap 2²⁰, 27 rescales); ballistic 0.205·n² vs classical 0.977·n; binning buys ~nothing (13→11 ppm) | [glm-2 #2] |
| F12 | Snap-point search (§10 cheat #1): certified early-exit boolean oracle answers at 7–8% of wave cost | Δ*=11 @Q=75, Δ*=13 @Q=85, both verified against full grid; verdict certain at pull time; elapsed-relative bounds are a self-canary (v1 bug, booked) | [glm-2 #3] |
| F13 | **K-axis reversal**: short tails dominate everywhere; calm-verdict was a K=8 artifact | gentle K=2: 92.1% vs impulse 56.6 (maxE 32 vs 53); stress K=2: 91.4 vs 83.1 (K=1: 92.9); arena frame: granite-short K=3 94.2% vs banked 93.2% (champion keeps debt crown 132,823 vs 139,257); no tournament contestant ever proposed K≤2 (all K∈{4,5,8}) | [glm-3 #3] |
| F14 | Contention-sorted switchboard (§8): ordering is a control law under scarcity | mag+C=1 beats admit-all on every column: %w 69.6 vs 68.0, maxE 232 vs 281, events −30%; keys spread maxE 41%; at C=3 all keys within noise — dial exists only under scarcity; U-shaped contention curve (freshest + stalest fire most) | [glm-3 #1] |
| F15 | Annuity ledger: fire is a decaying annuity; conservation exact in integers; contract's floor-halving has an unpriced sign bias | 0 violations / 48,000 ticks dual-sum; applied 1.32× emitted; signed displacement 0.44% of throughput; +0.195× sign asymmetry (stress), vanishing at even mags; 10,204/10,209 pulses pin at ±1 (unit-immortality) | [glm-3 #2] |
| F16 | Phase-gated *admission* is a throttle, not free resonance | %w falls monotonically with deferral 83.1→55.2; antiphase turn-taking kills cancellations 353→14 (−96%) at heavy residency cost | [glm-3 #4] |
| F17 | Cofire trust (charter §1.2 verbatim): learns *deafness*, both blame variants, both regimes | settles 830‰→308‰ (A) / 118‰ (B); trust→(0,·) all seeds; cancellations vanish by silencing (70→5), not resolution | [kimi #1] |
| F18 | Dialometer on pulse_div: snap-point displacement is a regime signal; calm optimum was one quantum off | calm blade flips at pd=3; stress: no snap in [1,8] (runout ≥5 quanta); calm pd=2: 17,942 settles (74.8%) vs impulse 13,589 (56.6%), lowest debt on the dial | [kimi #2] |
| F19 | Lag blade: fabric discovers its own twin latency exactly, then compensation converts conflict→calm | 5/5 exact lags from a 480-tick window; interference 830‰→984‰, debt 34,995→17,700, maxErr 39→28; **compensated sequential wins 1000‰ vs 984‰** — regime motion flips the optimal arm | [kimi #3] |
| F20 | Difference interferometer: latency reads off the fabric's own error fringes | 10/10 regime×seed correct; echo fringe +45–50k vs negative side-lobes (contrast 60–90k vs ±5k floor); raw pulse-stream and snap-onset fringes FAIL (common-mode) — difference to see the sensor | [opencode #1] |
| F21 | Lagged cofire trust: lag structure is what makes credit assignment discriminative; symmetric same-tick provably cannot | noisy-T2: debt 3.2× lower (18,524 vs 59,653), trusted-channel 97.3% vs 76.6%; headline both-twins metric NOT improved (552 vs 576‰); v1 symmetric: w1≡w2 forever (ran, confirmed) | [opencode #2] |
| F22 | Zombie auditor: physics invariants catch the DIVERGENCE bug class in one substrate | I1/I2 detect at tick 8–13 vs ≥500 for metrics (38–62× earlier); 10/10 clean false positives; mass ledger closes exactly (emitted = heat + discard + resident) | [opencode #3] |
| F23 | Quanta floor: 3-bit pulse alphabet recovers 99% of the interference win; ternary edge inverts the trade | cap=5: 824‰ vs full 830‰ (impulse 519‰); saturates cap≈5–7; Z₃ sign-only: 575‰ residency (beats impulse) but debt 53,907 > impulse 48,397 — coarse waves cheap to store, expensive to run | [opencode #4] |
| F24 | Phase-decay *coupling* (decay modulation, not admission): small consistent win | 84.3% vs 83.0% (+1.3pp), cancels 107 vs 68 — **single seed, needs O5 confirm** | [claude #1] |
| F25 | Ledger-driven mode selection: too noisy at 50-tick windows | 52 triggers, 0 effective switches, 83.0% identical to static — falsified at this timescale | [claude #2] |
| F26 | Naïve Barbieri dichotomy (noise-driven activity): FALSIFIED | dihedral slope 0.196 vs abelian/virtually-cyclic 0.991 (0.20×, *lower* not higher); operationalization must target CA-rule sensitivity, not feedback-loop activity | [claude #3] |
| F27 | RTL gear: q_snaplog.v (T1) + q_whistle.v (T3) landed, lint-clean both tools | elaborated at DEPTH=1/32, MAG=0; **UNVERIFIED-BEYOND-LINT** — no sim, no sby, no synthesis run | [NOVEL-ENHANCEMENTS] |

---

## 3. Convergent seams (independent replication ⇒ priority)

Independent replication by lanes that never compared notes is the strongest evidence class the
program owns tonight. These outrank single-lane wins.

**S1. Cofire as-specified collapses — ×3.** [glm-1 C] (self-locking 3-tick echo; reads the fabric,
not the world), [kimi #1] (trust→0, learns *silence*, both blame variants, both regimes), and
[opencode #2] (symmetric same-tick rule *provably* cannot discriminate — w1≡w2 identity). Three
lanes, one verdict: **charter §1.2 needs a homeostat and a lagged reference before §3.2's demo bets
on it** — the charter's own pre-registered failure mode (c) is now empirically armed. This is the
single most consequential seam: the stake demo's QTORCH arm currently contains a primitive with a
known collapse mode.

**S2. The fabric measures its own latency from its own streams — ×2.** [kimi #3] and [opencode #1]
independently arrived at first-difference integer cross-correlation: 5/5 and 10/10 exact reads,
480-tick windows, no floats, no second substrate. Both also found the *compensation* consequence:
debt halves, maxErr drops, and — kimi's twist — the optimal arm flips back to impulse once the lag
is repaid (1000‰ vs 984‰). Metrology independent of control mode ([opencode #1]: works in gentle
where superposition is the losing actuator). Promote to a named primitive: the fabric calibrates
its own switchboard before judging anything.

**S3. The published calm-regime verdict was a grid artifact — ×2, two axes.** [glm-3 #3] (K axis:
gentle K=2 92.1% vs impulse 56.6%) and [kimi #2] (pd axis: calm pd=2 74.8% vs impulse 56.6%, lowest
debt on the dial). Neither lane knew of the other. Consequence: the Variety Ledger's calm-
specialist entry is an entry-grid artifact, and the arena's search was incomplete (no contestant
proposed K≤2, ever — model anchoring on the hand-tuned example).

**S4. The fabric audits its own container geometry — ×2.** [glm-1 D] (retrodictive queue audit:
exact-time/dyadic-amplitude split; bug caught two ways) and [opencode #3] (liveness + toll-cap
invariants; tick-8 detection vs tick-500 metrics; exact mass closure). Both kill the DIVERGENCE.md
bug class *without a second substrate*. Complementary, not duplicate: one is forensic (post-hoc),
one is runtime (invariant).

**S5. Superposition tolerates adversaries; cancellation statistics carry the fault signal — ×2.**
[glm-1 A] (lie model: bounded drag, ×2–5 whistle) and [opencode #2] (noise model: 3.2× debt
isolation, 97.3% trusted-channel residency). Different fault models, same conclusion — and the
whistle (F6) is now cheap enough for silicon (T3, landed lint-clean [NOVEL-ENHANCEMENTS]).

*Also convergent, lower weight:* phase touches the fabric two ways with opposite signs — decay-
*modulation* wins small (F24, [claude #1]), admission-*gating* throttles (F16, [glm-3 #4]); the
boundary between them is itself a finding (see O5).

---

## 4. Overnight queue (ordered)

Each entry: hypothesis · harness · cost · decision rule. All CPU-minutes unless noted; all reuse
existing harnesses (e1.py / e1.c / arena.py / ledger.py / derby scripts) with contract items 1–4
pinned. Run in this order — the ordering is the thesis of this document.

**O1 — K=2/3 champion replay (the §3-rafters correction; from S3/F13).**
*Hypothesis:* allowing K ∈ {1,2,3} in the tournament schema yields entries beating the banked
champion on stress %w (glm-3's static probe says 94.2 vs 93.2 [glm-3 #3]); the ledger's calm
specialist gets displaced by short-K interference at Δ=6 (92.1 vs impulse's 56.6 [glm-3 #3];
74.8 vs 56.6 on the pd axis [kimi #2]).
*Harness:* arena.py v3 — widen strategy JSON schema to K∈{1..8}; also enter the static grid
points (K∈{1,2,3} × pd∈{2,3}) as non-LLM probes; 5 seeds, both regimes, frozen holdouts, PROCTOR
canary per RD-SWARM checklist; verify every promotion on holdout seeds before banking.
*Cost:* ~1–2 h model calls (local Ollama), minutes of judging.
*Decision rule:* any K≤3 entry beating 93.2% on holdout ⇒ new champion banked, champion's debt
crown noted (not dominated); ledger calm cell re-keyed. If no LLM proposes K≤3 again, book "grid
anchoring" as a standing arena bias and promote the static probe manually — the ledger banks
results, not lineages.

**O2 — Contention controller boundary (T2's gate; from F14).**
*Hypothesis:* mag+C=1 admission beats admit-all at N≥3 under conflict (69.6 vs 68.0, maxE 232 vs
281 at N=5 [glm-3 #1]), but the win is lag-shaped — with per-twin lag compensation (O1's blade,
F19/F20) contention collapses and the dial goes slack (C=3 already showed keys don't bind when
rejection is rare [glm-3 #1]).
*Harness:* glm3_experiments.py `run_sw` generalized: N ∈ {2,3,5,8} × C ∈ {1..N} × {calm, stress}
× {raw, lag-compensated}; 5 seeds; 4800 ticks.
*Cost:* ~30 min CPU.
*Decision rule:* win ≥2pp %w at N≥3 uncompensated ⇒ promote sort to RTL (q_tick_sched bitonic +
fairness/net==0 SVA per T2 [NOVEL-ENHANCEMENTS]); win vanishes compensated ⇒ book "contention is
a lag symptom," demote T2 behind the lag compensator in the build order.

**O3 — Quanta floor on RTL alphabets (the u-bit budget; from F23).**
*Hypothesis:* the 3-bit cap (99% of win at cap=5 [opencode #4]) holds at K=2 too (interaction of
the two reversals — short tails × coarse alphabet — is untested); the Z₃ debt inversion (53,907 vs
48,397 [opencode #4]) persists everywhere.
*Harness:* opencode `quant_floor.py` ported into e1.c (C99, static alloc), cap ∈ {1,2,3,5,7,11,∞}
× K ∈ {1,2,3,4}, both regimes, 5 seeds; then the same caps on the q_cell_core.v Verilator rung if
the cosim spike is alive.
*Cost:* ~20 min CPU + optional Verilator run.
*Decision rule:* cap=±5 retains ≥99% at K=2 ⇒ adopt 3-bit alphabet as the ESP32/.qm port default
(feeds PORTING-NOTES <1KiB lane); knee elsewhere ⇒ adopt the measured knee; Z₃ stays a sampling
gear (dice), not a correction gear, unless debt inverts back.

**O4 — Lag-compensation regime motion (E4's real architecture; from S2/F19).**
*Hypothesis:* closed loop — lag discovery (480-tick blade) → compensation → REGIME-META κ-detector
→ mode dial — beats every static arm, because compensation converts conflict→calm and the dial must
follow (kimi: compensated sequential 1000‰ vs compensated interference 984‰ [kimi #3]; ledger
doctrine applies to the *new* regime).
*Harness:* kimi exp3 + REGIME-META detector state machine + mode switch; stress runs with mid-
stream shifts (calm→conflict→bursty per charter §3.2 task shape), 5 seeds.
*Cost:* ~45 min CPU.
*Decision rule:* adaptive ≥ max(static arms) − 1pp post-compensation %w AND debt ≤ 60% of best
static ⇒ promote to E4 architecture and pre-load the §3.2 demo's QTORCH arm; else book the
boundary (detector lag vs regime dwell) with numbers.

**O5 — Phase-decay coupling, multi-seed confirm (single-seed result; from F24 vs F16).**
*Hypothesis:* claude's +1.3pp (84.3 vs 83.0, seed 20260902 only [claude #1]) survives 5 seeds;
the decay-modulation/admission-gating contrast (F24 vs F16) is real — dissipating *faster in
refractory* preserves net==0 states; *deferring admission* destroys residency.
*Harness:* exp1_phase_decay.py, 5 seeds × {calm, stress}; alongside glm-3 #4's gate at matched
duty for the paired comparison.
*Cost:* ~10 min CPU.
*Decision rule:* mean Δ ≥ +0.5pp and no seed < −0.5pp ⇒ promote to e1.py candidate default and
price the RTL (~30 LUTs per R1); otherwise book as single-seed noise — the F16 throttle verdict
stands alone.

**O6 — Cofire homeostat micro-probe (S1's repair; from F17/F21/F8).**
*Hypothesis:* minimal repair — bounded trust ∈ [4,12] with decay toward neutral 8, plus opencode's
lagged reference (the discriminative ingredient [opencode #2]) — preserves ≥800‰ steady-state on
honest twins while still demoting a true defector, with glm-1's whistle (×2–5 [glm-1 A]) as the
cross-check.
*Harness:* kimi exp1 variant A + floor/decay homeostat + lagged evaluation; fault models: clean,
noisy-T2 (±14), lying-T2 (+24, 1200-tick window).
*Cost:* ~20 min CPU.
*Decision rule:* holds ≥800‰ honest AND demotes the defector with whistle firing ⇒ cofire v1.1
survives into the §3.2 demo arm; fails either ⇒ demote cofire to v2 per charter failure mode (c),
and the demo runs selection-only learning. Either outcome unblocks the demo design.

**O7 — Bundle wall × compensation (capacity law re-measured; from F7 × F19).**
*Hypothesis:* the N=4 toxicity wall [glm-1 B] is lag-driven; compensating each twin's discovered
lag moves the wall right (true-residency at N=4 recovers toward the ~51% impulse floor or better).
*Harness:* glm-1 exp_glm1.py N-sweep with per-twin lag blades applied; N ∈ {2..8}, 5 seeds.
*Cost:* ~30 min CPU.
*Decision rule:* N=4 trueRes ≥ 50% ⇒ capacity law restated as "stale-sensing capacity, not twin
count"; wall unmoved ⇒ the wall is geometric (10-tick-stale disagreement up to 16 on the 8/5
slope), book the two-law split.

*Ordering rationale:* O1 first because it corrects the record the whole program cites (the calm
verdict and the champion) and costs the most wall-clock (model calls overlap O2–O5); O2/O3 gate
silicon decisions; O4 is the demo's spine; O5/O6 clear single-seed and collapse-mode hazards;
O7 closes the envelope. If only one thing runs tonight, run O1.

---

## 5. Silicon track — T1–T15 (status · next rung)

Source: [NOVEL-ENHANCEMENTS] (both rounds, incl. artifact-status footer). Verification ladder:
lint → sim (differential TB vs C99) → sby → synthesis → board. Nothing above lint has run.

| T# | Idea | Status tonight | Next rung |
|----|------|----------------|-----------|
| T1 | QUF-SNAP append-only snap log | `rtl/q_snaplog.v` landed, lint clean ×2 tools, elaborated DEPTH=1/32; UNVERIFIED-BEYOND-LINT | Differential TB: (QUF@t, log) → C99 replay byte-identical; snaplog sby (monotone tick, drops = fires − DEPTH). Derby support: F9/F22 say the log's information suffices — prove it in metal |
| T2 | Contention-sorted admission (glm-3 §8 → RTL) | Simulation evidence F14; no RTL | **Gated by O2.** If O2 holds: bitonic sort + budget comparator in q_tick_sched; SVA: no-silent-starvation + net==0 across scheduler |
| T3 | Byzantine whistle tripwire | `rtl/q_whistle.v` landed, lint clean; bounding invariant = aspiration | sby attempt on the bounding lemma (under one lying input, cancel rate ≤ base×K); sim calibrated to F6's measured ×2–5 ratios |
| T4 | K as runtime dial | Simulation evidence F13; no RTL | **Gated by O1.** After re-banking: LUT-masked fan-out dial in q_hebb_edge, not elaboration-time |
| T5 | Dialometer as BIST | None | Algorithm exists — F10's coarse-then-fine (9% cost; naive bank 153% is the anti-pattern). `q_bist_sweep.v` with pass = runout ≤ 1 quantum; phase locates the joint |
| T6 | Snap-only observability theorem | None (theorem unstated) | Statement now has evidence shoulders: F12 (certified boolean oracle), F10 (booleans recover structure), F11 (identity-grain fidelity). Write the sby obligation: observable ≡ snap-log; close it |
| T7 | Headroom as capacity (TDM) | None; F16 warns phase-*gating* throttles | Honor by construction: antiphase as clock-enable per phase, never clock switching (T11 refines) |
| T8 | QUF diff as instruction | None | Host-side first: quf.py diff over existing checkpoints; zero RTL; feeds T14/T15 |
| T9 | SPRAM flight recorder (UP5K, 16,384 marks) | None | T1's backing; TB = C99 replay at depth 16K; check yosys infers SPRAM not LCs |
| T10 | Whistle battery on hard DSP | Budget math only (per-edge 32>28 DSP does not fit — that bound IS the design) | Synth-lane: yosys `stat` must show multiplies in DSP; per-cell default on ECP5 |
| T11 | One clock, three phases (HX8K 3.70× headroom → 3× cells) | None | Differential TB: 6 virtual cells vs C99 vs real-6-cell netlist; per-phase-window conservation sby; 36 MHz close |
| T12 | Ring goes electrical (ECP5 sysIO pair, two-boat fabric) | None | Framing TB (byte-exact round trip, backpressure both ways); two-node link model extends conservation sby |
| T13 | PicoRV32 as fabric citizen (proof-carrying seam) | None | Three-view replay: RVFI trace + fire log + QUF snapshot, each replayable by C99 to the same state — the fabric audits its auditor |
| T14 | Feynman-desk ledger (GPU+CPU+RTL, FPGA referee) | None; host-side piece runnable tonight | quf.py diff over the desk's existing per-lane checkpoints; Lamport monotonicity joins T1's sby |
| T15 | Lockstep shadow fabric (HX8K) | None | One sby, two instantiations, same flit stream; fault-injection TB trips the strobe within one tick |

*Rung order stands as written* — T3 → T1 → T2 → T6 → T5 → T4 → T7 → T8, then T13 → T9 → T15 →
T11 → T10 → T12 → T14 [NOVEL-ENHANCEMENTS] — with two gates added by tonight: **T2 waits on O2,
T4 waits on O1.** The first sby run anywhere in this program is itself a milestone: currently
everything above lint is aspiration, and the artifact-status footer says so.

---

## 6. Open questions (charter raised · nobody ran)

**Q1 — §10's class-grain boundary on linear-superposition substrates.** The charter's cheat #2
leans on E7's law ("the cheat lives exactly at class grain" [CHARTER §10]). glm-2 ran the one
probe that exists: for the Hadamard walk, quantized interference holds at *identity* grain (13 ppm,
binning buys nothing) — the E7 grain law **does not transfer to linear-superposition substrates**
[glm-2 #2]. Open: map the boundary. Which substrate property decides whether quantized statistics
need class grain (embedding-census: yes, F5) or hold at identity grain (linear superposition: no,
F11)? Candidates: nonlinearity of the readout, learned-vs-fixed dynamics, dimensionality. Until
mapped, §10's cheat #2 must name its grain per-substrate, not inherit E7's. (The §10 correction is
cheap to draft tonight; the boundary map is a mini research program — one substrate per rung.)

**Q2 — Cofire homeostat design.** Three collapses (S1) all point at the same missing piece; every
lane proposed a different repair (refractory window [glm-1 C]; floor/decay or outcome-free
vindication [kimi #1]; lagged reference [opencode #2] — the only one shown discriminative). O6
probes one composite. Open beyond O6: is there a *minimal* homeostat with a provable no-collapse
bound, or does every local no-error-signal rule on a correction channel learn silence? This is
§1.2's load-bearing unknown and the §3.2 demo cannot be designed honestly until it resolves
(either direction is a result; the charter pre-registered both).

**Q3 — T6 observability theorem.** "Nothing observable is lost by reading only where blades fit"
[NOVEL-ENHANCEMENTS T6] is asserted, never formalized, never sby'd. Tonight's derby sharpened it
from three sides — F12 (certified early-exit oracle: boolean verdicts *stronger* than full-wave
estimates), F10 (structure recoverable from booleans at 9% cost), F9 (exact-time/dyadic-amplitude
split as the concrete information content of a log) — but sharpening is not proving. Open: state
the equivalence (observable behavior ≡ snap-log behavior) as a checkable obligation on q_snaplog +
q_cell_core and close it in sby. Nobody has run a single sby in this program yet; this is the
highest-value first.

*Second tier (also raised, also unrun):*
- **Q4 — §3.1 MI-criticality sweep**: the charter's own hello-world and "the cheapest experiment
  in the dossier" [RD-BEYOND-UTM Seam C]. Never run. Claude's group-criticality mini (F26) is a
  *different* operationalization and its failure does not touch this one.
- **Q5 — §3.2 stake demo**: the equal-budget GD control arm does not exist. Nothing in the derby
  or arena touched it. It remains the only cure for the selection-bias objection [CHARTER §5.1].
- **Q6 — Barbieri operationalized properly**: F26 falsified the naïve version; the real one
  (perturbation-support growth / exact integer Lyapunov proxy on ℤ_n vs D_n vs ℤ_n×ℤ₂ Cayley
  lattices [RD-BEYOND-UTM Seam B experiment]) is unrun — and it gates the Lattice primitive's
  group-typing story.
- **Q7 — The charter's §5.4 regime-gating mandate** now has three converged inputs (S2 lag, S3
  K-axis, F14 contention) but no unified dial design: what is the minimal integer controller that
  takes {κ-detector, lag blade, fan-out N} and emits {mode, K, pd}? O4 is its first cut, not its
  answer.

---

## Standing rules (carried forward)

1. Every claim cites its sheet; every experiment pins contract items 1–4 and byte-matches stock
   `e1.run` before reading new numbers (glm-3's self-check pattern — adopt org-wide).
2. Failed experiments are banked with the same care as wins (F8, F16, F17, F25, F26 are agenda
   items, not footnotes).
3. Sweeps propose, blades dispose — no smooth curve without its snap-point log [CHARTER §9].
4. Not committed. This file lives in the working tree with its sources.

— Synthesized by the research-agenda subagent (zai/glm-5.3), 2026-09-02, Riker's deck timezone.
Sources: QTORCH-CHARTER.md; docs/NOVEL-ENHANCEMENTS.md; RD-{BEYOND-UTM, PHYSICAL-SUBSTRATES,
SWARM-SUBSTRATE, SPREADSHEET-LINEAGE}.md; inventors-derby/INVENTIONS-{claude,glm-1,glm-2,glm-3,
kimi,opencode}.md; README.md; e7-embed-route/RESULTS.md; arena-v2.txt; ledger-results.txt.
