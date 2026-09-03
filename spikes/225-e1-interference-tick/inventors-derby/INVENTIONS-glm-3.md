# INVENTIONS — glm-3 (zai/glm-5.3 lane)

*Inventors Derby, 2026-09-02. Assigned edge: RD-SPREADSHEET-LINEAGE.md reclaim
list (R1 phase-gated noise, R2 conservation, R4 diversity-biased decay) +
charter §8 sorted switchboard, as runnable minis on the E1 harness.*

Method: every experiment forks `e1.run`'s interference arm verbatim and changes
one thing. **Self-check: both fork controls byte-match stock `e1.run` on all 5
seeds (1, 7, 42, 1999, 20260902) before any new number was read.** Integer-only
(flo appear only in this report's arithmetic, never in the loops). Reproduce
everything with:

```
cd inventors-derby && python3 glm3_experiments.py     # full output: glm3_run_output.txt
```

Metrics: ev = correction events, debt = ledger mass, chat = chatter,
canc = destructive cancellations, maxE = max error, %w = ticks within deadband
of ALL sensors. 5-seed means/totals unless noted.

**Best three: #1 Contention-Sorted Switchboard, #2 Annuity Ledger, #3
Tail-Shock.** (#4 Triangle-Ticket is the honest negative.)

---

## 1. THE CONTENTION-SORTED SWITCHBOARD — §8's patch bay as a controller

**Mechanism.** E1 is promoted from 2 twins to N=5 sensing cells (latencies
0/3/6/9/12 ticks). The switchboard is literally a row per twin — `{id, err,
last_fire, contention}` — rebuilt every tick. When candidates for correction
exceed a contention budget C, the board is **sorted by a key** and only the
top-C rows are admitted as pulses; rejected rows still book contention (they
showed up to the derby). Sort keys: `mag` (largest error first), `fair`
(least-recently-fired), `static` (cell id — the tape's one legal ordering,
"linear book-keeping"), `contend` (least-contended first). This makes §8's
claim testable twice over: as a *mechanism* (does the ordering choice change
dynamics?) and as an *analysis* (does sorting expose structure no debugger
shows?).

**Experiment.** `run_sw` in `glm3_experiments.py`: 4800 ticks, K=4, pd=3,
delta=12, drift=6, 5 seeds; admit-all control vs four keys at C=3/2/1.

**Numbers** (5-seed means; fires/twin order = latency 0,3,6,9,12):

```
admit-all (C=5)   ev=18368 debt=324322 chat=7414 canc=945 maxE=281 %w=68.0
                  fires/twin: [1586, 516, 195, 301, 1075]   <- U-shape: live + stalest fire most
C=1  sort=mag     ev=12744 debt=220754 maxE=232 %w=69.6  fires [1591, 30, 35, 35, 858]
C=1  sort=fair    ev=12962 debt=205010 maxE=270 %w=68.0  fires [1267, 323, 97, 132, 774]
C=1  sort=static  ev=12799 debt=210818 maxE=327 %w=69.8  fires [1627, 15, 34, 135, 749]
C=1  sort=contend ev=13083 debt=201496 maxE=271 %w=67.7  fires [1126, 409, 173, 185, 723]
C=3  (all keys)   %w=67.7–68.0, maxE 284–348; rejection rare (~1k/18k) — keys barely bind
```

Three findings. (a) **Mechanism:** at binding contention (C=1) the sort key
spreads %w by 2.1 pts, maxE by 41% (232 vs 327), debt by 9%. `mag`+C=1 *beats
admit-all* on every column (%w 69.6 vs 68.0, maxE 232 vs 281, events −30%):
admit only the loudest discrepancy and the stale-twin chorus stops
overcorrecting. The tape ordering is the worst maxE (327 at C=1, 348 at C=3) —
linear book-keeping pays for its single sort key in excursion. (b) **Analysis:**
each key is a camera angle on the same data: `mag` reveals a bimodal derby
(extremes win: [1591,…,858]); `static` starves twin-1 to 15 fires (tape
tyranny); `contend` flattens the top of the distribution and posts the lowest
debt (201k); the admit-all fires/twin vector exposes the U-shaped contention
curve (freshest and stalest cells contend most, middle latencies least) —
§8's "sort by degree and you see hubs" as an integer vector. (c) **Honesty:**
at C=3 the key choice barely matters — the switchboard is a *dial that only
exists under scarcity*; plenty makes all orderings equivalent.

**Novelty claim.** §8 is charter prose with no runnable instantiation
anywhere in the spike; E1 has 2 twins and no switchboard; no RD dossier runs a
sortable patch-bay experiment (RD-SWARM's MAP-Elites archives sort *solutions*,
not wiring). This is the first experiment where the *ordering of the wiring
data* is itself the control law, and it produced a mechanism finding
(one-loudest admission beats consensus) and a structure finding (the U-curve).
Most novel of my four.

---

## 2. THE ANNUITY LEDGER — R2's "transfer or duplication?" answered with integers

**Mechanism.** RD-SPREADSHEET-LINEAGE R2 asks whether fire is transfer or
duplication and proposes an RTL conservation monitor. The E1 answer falls out
of instrumenting stock `e1.run`: a pulse is **re-applied to g every tick it is
alive** (g += net each tick), so a pulse is neither a transfer (applied once)
nor a duplication (fanout copy) but a **decaying annuity**: it pays its current
magnitude into g each tick while halving. Conservation holds exactly only if
you count the whole annuity — so the monitor books, per tick, per pulse:
emitted mass, signed/unsigned applied, and per-sign lifetime integrals,
recomputed by two independent sums (the `CellResult.conservation_ok` pattern at
every evaluation, in Python).

**Experiment.** `run_cons`: stock interference arm, zero behavior change,
5 seeds, stress (K=4) and gentle (K=8) regimes, 4800 ticks each.

**Numbers** (5-seed totals):

```
[stress] violations=0   pulses=10209   emitted=54702   applied|net|=71953   applied_net=-319
         annuity amp(+) = 2.055x   amp(-) = 1.860x   sign asymmetry = +0.195x
         reached|1| = 10204/10209 pulses   unit-stick-ticks=26697   cancel-mass=3394
[gentle] violations=0   pulses=15406   emitted=48009   applied|net|=63847   applied_net=-349
         annuity amp(+) = 3.479x   amp(-) = 3.430x   asymmetry = +0.049x
         unit-stick-ticks=115938  (~7.5 of 8 life-ticks spent pinned at ±1)
single-pulse integrals (EXP 6, exact):
  K=4: +5 applies 11 (2.20x)  vs  -5 applies 9 (1.80x)   bias +2
  K=4: +9 applies 19 (2.11x)  vs  -9 applies 16 (1.78x)  bias +3
  K=8: +2 applies 9 (4.50x)   vs  -2 applies 9 (4.50x)   bias 0   (even m0: symmetric)
```

Four booked findings. (a) **Fire is an annuity**: unsigned applied throughput
is 1.32× emitted mass at stress, 1.33× at gentle — the fabric *creates*
application events from one admission; yet signed displacement is −319 vs
71,953 unsigned (0.44%): dissipation and destructive cancellation consume
99.6% of gross throughput. (b) **Contract item 1 has a semantic cost nobody
audited**: pinned floor-halving (`mag - mag//2`, floor toward −∞, chosen for
byte-identity) decays |negative| pulses faster than positive (+5→3, −5→−2), so
equal-magnitude corrections push g harder when positive — up to **+0.4× at mid
magnitudes** (11 vs 9), vanishing at even magnitudes and long K. Byte-identity
bought asymmetry; this is the first audit that prices it. (c) **Unit-pulse
immortality**: |mag|==1 never decays (`abs(mag) > 1` guard), so 10204/10209
pulses pin at ±1 until expiry — at gentle, pulses spend ~94% of life at ±1,
making the annuity amplifier magnitude-dependent (4.50× at m0=2 vs 2.15× at
m0=20, K=8). (d) The per-tick dual-sum monitor ran 48,000 ticks × 2 regimes
with **0 violations** — R2's conservation bit is implementable and exact in
integers, and E1 needs a heat channel in any silicon port because the annuity
re-application otherwise breaks naive Σact bookkeeping.

**Novelty claim.** R2 proposed the SVA/heat-register experiment and left
transfer-vs-duplication open for q_cell_core; nobody has audited E1's own
pulse arithmetic. Findings (b) and (c) — the sign bias of the *pinned*
contract and unit-stick domination — appear nowhere in the dossiers, README,
or DIVERGENCE.md, and are exactly the kind of thing byte-identity testing
cannot see (both substrates share the bias).

---

## 3. TAIL-SHOCK — the K-axis reversal (an R4 mechanism failed; its accident won)

**Mechanism.** R4 (diversity-biased decay): per-twin sliding window over the
last 8 emission signs; ≥3 flips ⇒ "diverse" twin gets K+kd pulse life, else
K−kd (clamped 1..16). Booked honestly: **the diversity gate is a no-op here**
— it fired 9 times in 10,209 emissions. What actually happened: kd=+2 ⇒
K_eff≈2 for ~all pulses ⇒ 91.4% vs stock 83.1%. The mechanism failed; the
accident said *the K axis is under-explored*, so I decomposed it with a plain
K sweep on stock `e1.run` (EXP 5).

**Experiment.** `sweep_k` + the kd sweep, 5 seeds, both regimes, plus the
ledger/arena frames.

**Numbers:**

```
kd sweep (stress d12/pd3):  kd=-2: 80.4%   kd=0: 83.1% (=stock, byte-matched)   kd=+2: 91.4%
                             diverse-emissions: 7 / 5 / 9 out of 10209  -> mechanism no-op
K sweep, GENTLE (d6/pd3, drift3/lat5):   K=8: 42.2%   K=4: 75.4%   K=3: 85.5%   K=2: 92.1%   K=1: 80.2%
                                         impulse ref: 56.6% (maxE 53)
K sweep, STRESS (d12/pd3):  K=8: 78.2%  K=4: 83.1%  K=2: 91.4% (maxE 35, canc 70)  K=1: 92.9%
                            impulse ref: 51.4%
ledger calm frame (d12):    impulse 98.0% debt 55545 maxE 53  vs  intf K=2: 97.8% debt 97682 maxE 32
arena stress frame (pd4/d16): granite K=5 (banked champ) 93.2% debt 132823 maxE 38
                             granite-short K=2 94.1% maxE 36;  K=3 94.2% maxE 39
```

Two reversals. (a) The README's regime verdict — "at gentle params
interference is *worse* than impulse (45.5% vs 56.7%)" — is an artifact of the
K=8 default: at K=2 the same gentle frame scores **92.1% vs impulse's 56.6%**
(+35.5 pts, maxE 32 vs 53). The E4 "mode dial" conclusion (calm rooms want
impulse) inverts at short tails: calm rooms want *short pulses*; mode and
tail-length are separate dials and the published table conflated them. (b) The
arena's banked champion is beatable on its own primary metric in its own
frame: granite-short K=3 ⇒ **94.2% vs 93.2%** — though NOT Pareto-dominated
(debt 139,257 vs 132,823; the champion keeps its debt crown). No tournament
contestant proposed K≤2 in any round (arena-v2.txt: every K ∈ {4,5,8}) — the
models anchored on the hand-tuned K=4 example; the ledger banked calm
specialism from an impulse entry running a wider deadband (d12), and its crown
stands (98.0%) only because nobody entered short-K interference at d6, where
it leads by 35 points.

**Novelty claim.** R4's flip-counter mechanism is the dossier's; my windowed
variant is a faithful mini of it, and it **failed** (booked: anti-collapse
rationale has no purchase at 2 cells — there is nothing to collapse). The
K-sweep is mundane tuning; the novelty is what it falsifies: the gentle-regime
verdict in the spike's own README, the completeness of the arena's search, and
the implication that the Variety Ledger's calm-specialist entry is an artifact
of the entry grid, not of the mode. Failed-mechanism + artifact-finding,
verified, per derby rule 4.

---

## 4. TRIANGLE-TICKET ADMISSION — R1 run honestly: a throttle, not free resonance

**Mechanism.** spreadsheet-cells' `RNG()·sin(phase)` reclaimed as pure
integers: each twin gets an up/down **triangle phase counter** (period P, no
multiplier — sin at 2-bit fidelity); a correction is *admitted* only in the
upper fraction of the triangle (gate threshold = peak·f), otherwise **deferred**
(error persists, re-tested next tick — defer, not drop). Configs: homogeneous
antiphase 16/16, diverse 13/29 and 11/41, duty f ∈ {1/4, 1/2, 3/4}.

**Experiment.** `run_gate`, stress params, 5 seeds.

**Numbers:**

```
no gate (stock)              ev=10209 debt=174978 chat=4446 canc=353 maxE=193 %w=83.1
homog antiphase 16/16 f1/2   ev= 5549 debt= 97024 chat=2200 canc=  14 maxE=355 %w=55.2
diverse 13/29 f1/2           ev= 6411 debt=117357 chat=2697 canc= 204 maxE=325 %w=60.2
diverse 13/29 f1/4 (wide)    ev= 9051 debt=155721 chat=3618 canc= 249 maxE=335 %w=80.5
diverse 13/29 f3/4 (narrow)  ev= 4878 debt= 95589 chat=2170 canc=  71 maxE=380 %w=50.8
diverse 11/41 f1/4           ev= 8658 debt=152878 chat=3530 canc= 195 maxE=264 %w=78.9
gate-window stats (f1/2, 13/29): bothOpen=7710  oneOpen=11435 of 24000 ticks
```

**Verdict: R1's hypothesis is rejected at mini scale.** The dossier predicted
phase gating buys the stochastic-resonance benefit (fewer events *while
holding* %w); instead %w falls monotonically with deferral (83.1 → 80.5 → 60.2
→ 55.2) — at 2 cells the gate is a pure throttle: every deferred correction is
a tick outside deadband. Two salvageable observations: a wide gate (f1/4) cuts
events 11% and chatter 19% for 2.6 pts of %w (a tunable conservation dial, not
a free lunch); and **antiphase homogeneous gating nearly eliminates twin
conflict** — cancellations 353 → 14 (−96%) with oneOpen=21000/24000 — the
twins take turns and stop fighting, at heavy residency cost. Phase gating as
conflict-*suppression* (a scheduled mode-dial) survives; as noise-for-free it
does not.

**Novelty claim.** The mechanism and the experiment sketch are RD-SPREADSHEET
R1's (it proposed exactly this for `e1.c`); the contribution is running it at
all, the deferral semantics, the duty sweep, and the honest negative plus the
antiphase cancellation kill (353→14), which the dossier did not predict. Least
novel of the four; included because verified negatives are derby currency.

---

## Ledger of what failed

- R4 diversity gate: no-op at 2 cells (9/10209 firings). Booked above.
- R1 free-resonance hypothesis: rejected at 2 cells. Booked above.
- §8 "orderings are mechanisms": holds only under binding contention (C=1);
  at C=3 all four orderings are within noise. Booked as a boundary, not a win.
- My own harness bug (caught by the self-check design): first draft ran both
  homogeneous triangles in lockstep from phase 0 — bothOpen=13500/oneOpen=0
  was synchronization, not biology. Fixed with an antiphase init before any
  claim was written down.

*Files: `glm3_experiments.py` (all six experiments, self-checking),
`glm3_run_output.txt` (canonical output). Not committed. No files outside my
own lane were touched.*
