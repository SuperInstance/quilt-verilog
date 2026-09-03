# OVERNIGHT-K-REPLAY — K-Axis Rescue Replay (Run 1)

*Overnight queue, night of 2026-09-02. Run 1 (retry after provider overload;
Casey: "keep everyone going as far as possible"). Lane: glm-5.3 subagent.
Subject under test: glm-3 derby invention #3 (Tail-Shock) — the claim that
the banked arena champion's crown is a K-grid artifact.*

**Hypothesis (as tasked):** the banked arena champion (granite K=5/pd4/d16,
93.2%) won because no contestant ever proposed K ≤ 2 (arena-v2.txt: every
tournament K ∈ {4,5,8}); at K=2/K=3 interference dominates beyond published
margins.

**Method.** Everything runs inside stock `e1.run` (integer-only loops; the
only division is report aggregation, exactly as `arena.py score()` does it:
pct = round(mean of per-seed pct_within, 1), debt summed, maxerr maxed).
Seeds (1, 7, 42, 1999, 20260902), 4800 ticks, K grid {1,2,3,4,5,6,8} (task
asked {1,2,3,4,6,8}; K=5 added because it is the banked champion's own row).
Four frames: the two published frames (stress-hand, gentle-tight), the banked
champion's frame, and the ledger-calm frame. Reproduce with:

```
cd inventors-derby && python3 overnight_k_replay.py        # -> overnight-k-replay-run1.txt
python3 e1.py   (spike root, stock sanity)                 # -> overnight-e1-stock-stdout.txt
```

**Determinism proof.** This run's output (`overnight-k-replay-run1.txt`) is
`diff`-clean byte-identical to the 21:58 pre-overload execution
(`overnight-k-replay-output.txt`). Two independent executions, one integer
contract, zero divergence.

---

## §0 CONTROL ARMS — FIRST, BEFORE ANY NEW CLAIM

32 byte-match gates against every published number this replay touches.
**32/32 PASS, 0 FAIL.** No new number below is read from a harness that
cannot reproduce the old numbers. Full gate table (got == want on every row;
abbreviated where per-seed tuples would pad):

```
arena-v2.txt baselines (stress d12/pd3, drift6/lat10)
  impulse      (51.4, 244973, 61)          PASS
  intf K=4     (83.1, 174978, 39)          PASS
banked champion (granite K=5 pd4 d16, stress regime)
  champion     (93.2, 132823, 38)          PASS
README per-seed stress table (K=4 pd3 d12, both arms)
  seq pct/seed  (51.9, 49.4, 53.1, 50.5, 51.9)          PASS
  seq maxE/seed (61, 61, 61, 61, 61)                    PASS
  seq ev/seed   (2524, 2655, 2469, 2602, 2513)          PASS
  int pct/seed  (83.0, 82.5, 83.4, 83.6, 83.0)          PASS
  int maxE/seed (38, 39, 38, 39, 39)                    PASS
  int ev/seed   (2064, 2022, 2044, 2009, 2070)          PASS
README gentle claim (stock e1.py defaults, seed 20260902) — the K=8 rows
  intf K=8 gentle %w = 45.5               PASS   (published 45.5)
  impulse gentle %w = 56.7                PASS   (published 56.7)
ledger-results.txt rows (calm regime drift3/lat5)
  impulse calm d12       (98.0, 55545, 53)             PASS
  hand-intf calm K=4 d12 (97.3, 81617, 35)             PASS
  granite champ calm     (97.8, 87178, 35)             PASS
glm3_run_output.txt EXP5 — full K sweep, both frames, 14 rows
  stress K=1..8: (92.9,…) (91.4,…) (86.3,…) (83.1,…) (81.1,…) (80.3,…) (78.2,…)   ALL PASS
  gentle K=1..8: (80.2,…) (92.1,…) (85.5,…) (75.4,…) (65.6,…) (56.3,…) (42.2,…)   ALL PASS
glm3 EXP5 champion-frame + ledger-calm rows
  champ-frame K=5 (93.2, 132823, 38)   K=2 (94.1, 150968, 36)   K=3 (94.2, 139257, 39)   ALL PASS
  ledger-calm intf K=2 d12 (97.8, 97682, 32)                PASS
```

The K=8 control specifically (README gentle: 45.5 vs 56.7) reproduces
exactly — so the published gentle verdict really was measured at K=8, and the
replay below may legitimately re-interrogate it at other K.

---

## §1 K SWEEP — both arms, 5 seeds, 4 frames (raw)

Sequential arm run across the FULL K grid in every frame: K-invariance
**PROVEN** (identical pct/debt/maxE/ev at every K — K is not a dial the
impulse arm owns; printed as one row per frame).

### [stress-hand] pd=3 d=12 drift=6 lat=10 (README/arena baseline frame)

```
impulse (K-invariant, PROVEN):   %w= 51.4  debt=244973  maxE=61  ev=12763
   K     %w  margin     debt maxE  canc  chat     ev
   1   92.9   +41.5   184991   33   102  5059  10815
   2   91.4   +40.0   169541   35    70  4218   9941
   3   86.3   +34.9   172707   38   128  4300  10073
   4   83.1   +31.7   174978   39   353  4446  10209
   5   81.1   +29.7   175834   39   786  4440  10218
   6   80.3   +28.9   176137   39  1288  4558  10243
   8   78.2   +26.8   180397   39  1981  4656  10478
```

### [gentle-tight] pd=3 d=6 drift=3 lat=5 (README calm frame)

```
impulse (K-invariant, PROVEN):   %w= 56.6  debt=117198  maxE=53  ev=11551
   K     %w  margin     debt maxE  canc  chat     ev
   1   80.2   +23.6   145349   31    34  9469  14506
   2   92.1   +35.5   113573   32    54  5976  11410
   3   85.5   +28.9   109411   34   215  5368  10890
   4   75.4   +18.8   112540   35  1085  5617  11171
   5   65.6    +9.0   120516   36  1691  6347  11901
   6   56.3    -0.3   131773   38  2199  7347  12893
   8   42.2   -14.4   160715   37  2600  9762  15406
```

### [arena-champ] pd=4 d=16 drift=6 lat=10 (banked champion frame)

```
impulse (K-invariant, PROVEN):   %w= 96.0  debt=139949  maxE=61  ev= 5802
   K     %w  margin     debt maxE  canc  chat     ev
   1   89.1    -6.9   195587   36   114  4850   9347
   2   94.1    -1.9   150968   36    77  3214   7190
   3   94.2    -1.8   139257   39    68  2863   6586
   4   94.0    -2.0   134688   41    81  2723   6360
   5   93.2    -2.8   132823   38   125  2649   6244   <- banked champion
   6   91.9    -4.1   134225   38   235  2686   6293
   8   89.3    -6.7   138528   39   605  2818   6482
```

### [ledger-calm] pd=3 d=12 drift=3 lat=5 (variety-ledger calm frame)

```
impulse (K-invariant, PROVEN):   %w= 98.0  debt= 55545  maxE=53  ev= 2878
   K     %w  margin     debt maxE  canc  chat     ev
   1   97.7    -0.3   134140   28    52  3012   8679
   2   97.8    -0.2    97682   32    27  1773   6103
   3   97.5    -0.5    88041   36     9  1605   5411
   4   97.3    -0.7    81617   35    28  1476   4975
   5   97.2    -0.8    76088   36    23  1318   4599
   6   97.0    -1.0    72652   36    56  1268   4352
   8   96.1    -1.9    68519   36   137  1176   4036
```

---

## §2 K-vs-MARGIN CURVES (margin = intf %w − impulse %w)

```
stress-hand   K1=+41.5  K2=+40.0  K3=+34.9  K4=+31.7  K5=+29.7  K6=+28.9  K8=+26.8
              peak K=1 (+41.5); never inverts — interference wins at every K
gentle-tight  K1=+23.6  K2=+35.5  K3=+28.9  K4=+18.8  K5=+9.0  K6= -0.3  K8=-14.4
              peak K=2 (INTERIOR, +35.5); inverts at K=6
arena-champ   K1= -6.9  K2= -1.9  K3= -1.8  K4= -2.0  K5= -2.8  K6= -4.1  K8= -6.7
              peak K=3 (interior, −1.8); inverted at every K (impulse wins all)
ledger-calm   K1= -0.3  K2= -0.2  K3= -0.5  K4= -0.7  K5= -0.8  K6= -1.0  K8= -1.9
              peak K=2 (−0.2); inverted at every K, margins tiny
```

Three shapes, one rule. **Where interference wins, short K wins more**:
under conflict (tight deadband vs drift+latency) the margin is monotone
falling in K (stress) or interior-peaked at K=2 (gentle) — every extra tick
of pulse tail is pure smear. **Where the deadband is wide relative to drift,
interference never wins** (arena-champ, ledger-calm): the impulse rarely
misfires, so there is no conflict for superposition to resolve, and tails can
only hurt. The inversion boundary is a property of (delta vs drift×latency),
NOT of mode: the README's "interference slightly worse in calm (45.5 vs
56.7)" is real at K=8 and inverts to **+35.5 at K=2** — a published regime
verdict that was actually a tail-length verdict. Mode and tail-length are
separate dials; the published table conflated them. Confirmed on fresh runs
from a harness that first reproduced the published numbers byte-for-byte.

---

## §3 glm-3's CLAIM — granite-short K=3 (94.2%) vs banked champion K=5 (93.2%)

Exact banked-champion frame (pd=4 d=16 drift=6 lat=10), full seed set,
per-seed spread (`overnight-k-replay-perseed.txt`):

```
     seed   K=2 %w   K=3 %w   K=5 %w   K3−K5   winner
        1     94.2     94.5     93.3    +1.2    K=3
        7     94.3     94.4     92.8    +1.6    K=3
       42     94.0     94.0     93.6    +0.4    K=3
     1999     94.1     94.0     93.3    +0.7    K=3
 20260902     94.1     94.1     93.1    +1.0    K=3

K=3: mean 94.2%  spread 94.0..94.5  debt 139257 (per-seed 27126..28188)  maxE 39
K=5: mean 93.2%  spread 92.8..93.6  debt 132823 (per-seed 26121..27089)  maxE 38
K=2: mean 94.1%  spread 94.0..94.3  debt 150968 (per-seed 29723..30613)  maxE 36
per-seed winners: K=3 beats the champion 5/5 (K=2 also 5/5)
```

**CONFIRMED.** K=3 beats the banked champion on the primary metric on all
five seeds (mean +1.0, range +0.4..+1.6) — glm-3's 94.2 vs 93.2 is real and
seed-robust, not an average hiding a split. **Not Pareto domination**: the
champion keeps the debt crown (132,823 vs 139,257) and the maxE crown (38 vs
39); K=2 keeps the tightest maxE of all (36). glm-3 already booked this
honestly; the replay adds that the per-seed win is unanimous.

**But the replay finds the bigger artifact the derby missed.** In the
champion's OWN frame, the sequential arm — which no contestant ever entered
at d16, and which the ledger only ever ran at d12 — scores **96.0% with zero
seed variance (96.0 on all 5 seeds)**, beating K=3 head-to-head 5/5. The
arena crown is therefore a *joint* grid artifact: nobody proposed K ≤ 2
(anchoring on the prompt's K=4 example — glm-3's finding), AND nobody
proposed impulse at wide deadband. The true stress-frame ranking under a
swept grid is:

```
impulse d16    96.0%  debt 139949  maxE 61   (unseen entry — wins pct)
intf K=3       94.2%  debt 139257  maxE 39
intf K=2       94.1%  debt 150968  maxE 36   (maxE crown)
intf K=4       94.0%  debt 134688  maxE 41
intf K=5       93.2%  debt 132823  maxE 38   (banked champion — debt crown)
```

And even here the Variety Ledger doctrine holds rather than dissolves: on
(pct↑, debt↓, maxE↓) NOTHING dominates anything — impulse-d16 owns pct,
K=5 owns debt, K=2 owns maxE, K=3 is the balanced interior. The champion's
frame has a **four-way Pareto front**. The crown was never a single winner;
it was an unexplored grid wearing one.

---

## §4 PROPOSALS

### New default K per regime (decision rule)

| regime (frame) | default | number | rationale |
|---|---|---|---|
| conflict, tight deadband (d≤12, drift6/lat10) | **K=2** | 91.4% vs 92.9 (K=1) | K=1 tops pct but is barely a wave — single-tick pulses, near-zero superposition, 5059 chatter; K=2 keeps +40.0 margin with 18k less debt and live cancellations (70). K=1 is the pct-specialist bench entry. |
| gentle, tight deadband (d6, drift3/lat5) | **K=2** | 92.1% (+35.5 over impulse) | interior peak; K=8's published −14.4 inverts here |
| wide deadband vs drift (d16, drift6/lat10) | **impulse** (K=3 if interference mandated) | 96.0% vs 94.2 best-intf | no interference K wins; superposition has no conflict to resolve |
| ledger-calm (d12, drift3/lat5) | **impulse** (K=2 if mandated) | 98.0% vs 97.8 | impulse keeps the bank; K=2 is the closest chase with maxE 32 |

Rule of thumb: **read the deadband-to-conflict ratio, then pick tail length.**
Conflicted room → shortest tails (K=2); calm or wide room → no tails at all.
The stock `e1.py` default K=8 is the *worst or near-worst K in every frame*
and should stop being anyone's default — it is the harness's own tail-heavy
anchor, and it manufactured the README's gentle-regime verdict.

### Arena-grid change: sweep K as a judged axis

`arena.py` change (concrete): a contestant's entry becomes
`(mode, pulse_div, delta)`; the harness itself sweeps K ∈ {1,2,3,4,6,8} ×
5 seeds (sequential entries cost 1 run per seed — K-invariance now PROVEN,
not assumed; interference entries 6× that, ~seconds of CPU at 4800 ticks).
The leaderboard reports each entry's best-K row **plus its K-curve**, and the
ledger banks the whole curve, not a point. Effects, all verified by this
replay:

1. Granite's identical proposal (pd4/d16) is re-banked at K=3 (94.2%) —
   +1.0 over its banked K=5, found for free, no smarter model required.
2. The mode×delta hole becomes visible: impulse-d16 (96.0%) would have
   topped the stress table in round 1, and the "interference owns stress"
   narrative would have been corrected a day earlier.
3. Anchor bias dies: no contestant proposed K≤2 in ANY round (arena-v2.txt:
   all K ∈ {4,5,8}); a swept axis cannot be anchored.
4. Ledger upgrade: bank K-curves per strategy so the play-call ("read the
   regime, call the specialist") can also dial tail length, not just mode.

### Ledger actions (no crowns revoked — doctrine, not demotion)

- Champion K=5 keeps its debt + maxE Pareto seats; add K=3 (pct-interior)
  and K=2 (maxE) to the stress Pareto bank; add **impulse-d16** as the
  stress pct specialist — the sequential arm's second banked specialist
  (calm d12: 98.0; stress d16: 96.0), retiring "impulse loses stress" as
  another grid artifact.
- Book the negative: at wide deadband the K-axis rescue FAILS — no short-K
  interference entry beats impulse there. The K-artifact thesis is true in
  exactly the frames where interference wins at all.

---

## Files

- `overnight_k_replay.py` — the replay harness (phases 0–4, gates first)
- `overnight-k-replay-run1.txt` — this run's canonical output (33 lines of
  PASS incl. summary; 32/32 gates)
- `overnight-k-replay-output.txt` — 21:58 pre-overload execution; byte-identical
- `overnight-k-replay-perseed.txt` — champion-frame per-seed spreads (§3)
- `overnight-e1-stock-stdout.txt` — stock `e1.py` sanity output

**Verdict on the hypothesis:** CONFIRMED in the champion frame (K=3 > K=5,
5/5 seeds, +1.0) and beyond published margins in both published frames
(K=1/2 adds ~10 and ~47 points to the stress/gentle margins respectively);
the champion's crown is an artifact of the (mode, delta, K) entry grid —
but the deeper hole is the mode axis (impulse-d16 96.0%), not K alone.

*Not committed. No files outside the inventors-derby lane were modified.*
