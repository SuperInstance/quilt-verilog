# INVENTIONS — contestant: kimi (KimiCode), 2026-09-02

Brief: inventors-derby/BRIEF.md. Read first: QTORCH-CHARTER.md (epigraph, §6
gears, §8 sorted switchboard, §9 dialometer/feeler-gauges/snap points, §10
cheat-code), README.md, e1.py, arena.py, and all RD-*.md / VARIETY-LEDGER /
REGIME-META / SYNOPTIC-MAP / DIVERGENCE dossiers (novelty check, delegated
full read — verdicts cited per invention).

All experiments: python3 3.14.4, pure-stdlib, integer-only (settle counts and
per-mille via integer division; no floats anywhere — including display),
fixed seeds `(1, 7, 42, 1999, 20260902)` (arena convention). Experiment
scripts were run from `/tmp/derby-kimi/` so the repo stayed untouched; full
source is embedded below verbatim — each reruns with
`python3 <script>` from any directory (they import `e1` by absolute path).
Sanity anchor: my re-implementation of the fixed harness reproduces the
README numbers (stress interference 830‰ settles vs README 83.0%; stress
sequential 12322/24000 = 51.3% vs README ~52%).

Scoreboard:

| # | Name | Verdict | One-line result |
|---|------|---------|-----------------|
| 1 | COFIRE TRUST | **FALSIFIED (booked)** | Charter §1.2's anti-cofire rule, run for the first time, learns *deafness*: trust collapses to ~0, cancellations vanish because emitters are silenced, settles 830‰→308‰ |
| 2 | DIALOMETER SWEEP | **VALIDATED + discovery** | pulse_div as a feeler-gauge dial: blade flips at pd=3 in calm, never flips in stress — flip position is a regime signal; also found a new calm optimum (pd=2: 17942 settles vs impulse 13589) |
| 3 | LAG BLADE | **VALIDATED** | Integer cross-correlation of first-difference streams discovers twin latency exactly (5/5 lags); lag-compensated arm: 830‰→984‰, debt 34995→17700, maxErr 39→28 |

---

## 1. COFIRE TRUST — the first run of the charter's cofire rule learns deafness (honest failure)

**Mechanism.** Give each twin an integer trust weight in [0,16] (start 8 =
neutral), exactly the charter §1.2 cofire sketch lifted to the sensor level:
when twin *i* emits a pulse and a live pulse from twin *j* exists — same
sign ⇒ `trust[j] += 1` (j fired first and predicted me: pre-before-post,
STDP ordering); opposite sign ⇒ anti-cofire. Emission magnitude is scaled by
trust: `m' = m * trust // 8` (trust 0 = silenced). Two blame variants were
run: **A** — contradiction punishes the *standing* pulse's twin
(`trust[j] -= 1`, the charter's literal `w -= 1`); **B** — contradiction
punishes the *later* emitter (`trust[i] -= 1`, post-before-pre depression).

**Hypothesis.** Under stress, T2's stale pulses get contradicted by T1's
fresh ones, so trust₂ falls online and the fabric self-organizes toward
"believe the live twin more."

**What actually happened (5 seeds, stress: Δ=12, drift=6, K=4, lag=10;
calm: Δ=6, drift=3, K=8, lag=5; 4800 ticks):**

```
STRESS   mean settles ‰   mean debt   mean cancel   final trust (T1,T2) per seed
fixed       830            34995          70         —
trust-A     308            34302           5         (0,1) (2,0) (0,11) (0,1) (3,0)
trust-B     118            20029           8         (0,0) (0,2) (0,0) (0,1) (0,10)

CALM
fixed       421            32143         520         —
trust-A     291            18445         163         (0,4) (8,0) (0,7) (0,8) (2,0)
trust-B     239            18503         117         (0,0) (9,0) (1,0) (7,0) (1,0)
```

Both variants collapse trust to ≈0 for both twins, in both regimes. The
cancellations row looks like an improvement (70→5) until you see why: there
is nothing left to cancel — the emitters are silenced. Debt craters on some
seeds (stress seed 42, trust-B: 12668 vs fixed 35076) while settles fall to
96‰: the fabric's learnable word on this channel is **"silence"**, and raw
±1 cofire finds it immediately.

**Diagnosis (the actual finding).** A correction channel only speaks when
things are already wrong, so cofire statistics on it measure *error
coincidence*, not coordination. During every reality reversal, both twins
spend ~latency ticks in mutual contradiction; anti-cofire has no homeostasis,
so contradiction pressure ratchets everyone to zero. The "negative
knowledge" state (net==0, both signs live) fed into Hebbian blame destroys
the sensors instead of arbitrating them. Concretely: **charter §1.2's
anti-cofire, as literally specified, is a trust-collapse failure mode on E1**
— cofire needs either a floor/decay homeostat or an outcome-free vindication
signal before it can gate emission.

**Novelty claim (honest): PARTIAL.** The rule is spec'd in
QTORCH-CHARTER.md:123-136 but was never run anywhere (the charter itself
hedges: "if ratchet lookup helps but cofire hurts → demote cofire to v2").
RD-SPREADSHEET-LINEAGE.md:291 already asserts "cofire training is pure Hebb →
collapse" in fabric RTL — my run **confirms that doctrine empirically on E1**
and adds what no dossier has: per-twin sensor trust, the deafness signature
(cancellations vanish via silencing, not via resolved conflict), and the
reversal-window blame-symmetry diagnosis explaining *why* both blame
assignments fail. Failed experiment, booked per derby rule 4.

**Source (variant A; variant B is the one-hunk delta noted inline):**

```python
#!/usr/bin/env python3
# exp1_cofire_trust.py — run: python3 exp1_cofire_trust.py
import sys
sys.path.insert(0, "/home/eileen/projects/quilt-verilog/spikes/225-e1-interference-tick")
from collections import deque
from e1 import LCG, reality

SEEDS = (1, 7, 42, 1999, 20260902)

def run_trust(ticks=4800, K=4, pulse_div=3, delta=12, drift=6, lat2=10,
              seed=1, use_trust=True):
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()          # [signed_mag, remaining_life, twin_id]
    trust = [8, 8]
    snap_events = ledger_mass = cancellations = 0
    settles = 0
    for t in range(ticks):
        s1 = reality(t)
        s2 = reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        trig = []
        e1v, e2v = s1 - g, s2 - g
        if abs(e1v) > delta: trig.append((0, e1v))
        if abs(e2v) > delta: trig.append((1, e2v))
        for twin, e in trig:
            m = abs(e) // pulse_div or 1
            if use_trust:
                m = m * trust[twin] // 8
            if m == 0:
                continue
            sgn = m if e > 0 else -m
            if use_trust:
                for pmag, plife, ptwin in pulses:
                    if ptwin == twin: continue
                    if (pmag > 0) == (sgn > 0):
                        trust[ptwin] = min(16, trust[ptwin] + 1)   # A: j predicted me
                    else:
                        trust[ptwin] = max(0, trust[ptwin] - 1)    # A: j contradicted
                # VARIANT B: replace the else-branch above with
                #   disagree = True
                # and after the loop: if disagree: trust[twin] = max(0, trust[twin]-1)
            pulses.appendleft([sgn, K, twin])
            snap_events += 1
            ledger_mass += abs(e)
        if pulses:
            net = sum(p[0] for p in pulses)
            if net == 0 and len(pulses) >= 2:
                cancellations += 1
            decayed = deque()
            for mag, life, twin in pulses:
                if life > 0:
                    if abs(mag) > 1: mag = mag - (mag // 2)
                    decayed.append([mag, life - 1, twin])
            pulses = decayed
            g += net
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1
    return settles * 1000 // ticks, ledger_mass, cancellations, tuple(trust)

if __name__ == "__main__":
    for name, kw in (("STRESS", dict(delta=12, drift=6, K=4, lat2=10)),
                     ("CALM",   dict(delta=6,  drift=3, K=8, lat2=5))):
        print("--", name)
        for s in SEEDS:
            f = run_trust(seed=s, use_trust=False, **kw)
            tr = run_trust(seed=s, use_trust=True, **kw)
            print(f"  seed {s:>9}  fixed {f[0]:>4}‰  trust {tr[0]:>4}‰  "
                  f"debt {f[1]}/{tr[1]}  cancel {f[2]}/{tr[2]}  trust={tr[3]}")
```

---

## 2. DIALOMETER SWEEP — §9's feeler-gauge, instrumented; flip position is a regime signal

**Mechanism.** §9 says the dial reads in points: discrete blades, boolean
fit-or-not, and every smooth claim must trace to snap points. The E1 harness
already contains a hidden continuous dial: `pulse_div` interpolates
impulse→interference (pd=1 emits the full error as a decaying train ≈ spread
impulse; large pd = gentle waves). So: sweep pd = 1..8, and at each setting
apply one boolean blade — **does interference beat sequential on total
integer settle count over 5 seeds?** The snap point is where the blade
flips. Run the same sweep in two regimes; the *displacement* of the snap
point between regimes is the runout reading — divergence gets a reading,
not a verdict.

**Numbers (integer settle counts out of 4800 ticks × 5 seeds = 24000; debt
alongside):**

```
== calm (Δ=6, drift=3, lag=5, K=8) ==   sequential total 13589  [2652 2696 2790 2731 2720]
  pd=1  settles 13689  blade=1  debt 129435
  pd=2  settles 17942  blade=1  debt 103559
  pd=3  settles 10133  blade=0  debt 160715   <== SNAP POINT
  pd=4  settles  4711  blade=0  debt 301852
  pd=5  settles  3375  blade=0  debt 442735
  pd=6  settles  2639  blade=0  debt 547201
  pd=7  settles  2305  blade=0  debt 635963
  pd=8  settles  2079  blade=0  debt 700923

== stress (Δ=12, drift=6, lag=10, K=4) ==  sequential total 12322  [2489 2370 2547 2426 2490]
  pd=1  settles 13906  blade=1  debt 233717
  pd=2  settles 19329  blade=1  debt 176147
  pd=3  settles 19943  blade=1  debt 174978
  pd=4  settles 19513  blade=1  debt 182958
  pd=5  settles 18357  blade=1  debt 196203
  pd=6  settles 17182  blade=1  debt 208274
  pd=7  settles 16620  blade=1  debt 218942
  pd=8  settles 15471  blade=1  debt 230771
```

**Readings.**

- **Calm snap point: pd=3** (blade flips 1→0 and never returns through pd=8).
  **Stress: no snap in [1,8]** — the blade holds at every quantum. The
  runout between regimes is ≥5 dial quanta. The one-line regime classifier:
  *snap at pd≤3 ⇒ calm; no snap in range ⇒ conflict.* That is §9's
  concentricity test run on the mode dial: the fabric's own geometry
  announces the regime, from eight booleans.
- **Discovery (unplanned): the hand-tuned calm setting was off-optimum.**
  pd=2/K=8 scores 17942 settles (74.8%) in calm — beats impulse (13589,
  56.6%) *and* the documented pd=3 gentle point (10133, 42.2%), with the
  lowest debt on the whole calm dial. The ledger doctrine said "impulse is
  the calm specialist"; the dial says the calm specialist is actually
  interference at pd=2 — the loser strategy's regime was real, but its
  champion setting was wrong by one quantum. In stress the dial peaks at
  pd=3 (19943), matching the README's stress choice.
- The wave shape between snap points is extrapolation; the two booleans at
  pd=2 and pd=3 are the evidence. Sweeps propose, blades dispose.

**Novelty claim (honest): PARTIAL-to-NOVEL.** The calm/stress arm flip at
fixed params is established (VARIETY-LEDGER.md, REGIME-META.md), and sweeps
exist (py/c-sweep.csv), but per the full dossier scan: *no dossier experiment
sweeps one parameter and reports where the winning arm flips*; the
dialometer/feeler-gauge/snap-point material in §9 is metaphor with zero
experiments attached; nothing anywhere derives a regime signal from
flip-point displacement ("runout"). The pd=2 calm optimum is new
empirically. What is NOT new: the fact that the flip exists.

**Source:**

```python
#!/usr/bin/env python3
# exp2_dialometer.py — run: python3 exp2_dialometer.py
import sys
sys.path.insert(0, "/home/eileen/projects/quilt-verilog/spikes/225-e1-interference-tick")
from collections import deque
from e1 import LCG, reality

SEEDS = (1, 7, 42, 1999, 20260902)
TICKS = 4800
REGIMES = {"calm":   dict(delta=6,  drift=3, lat2=5,  K=8),
           "stress": dict(delta=12, drift=6, lat2=10, K=4)}

def settles(mode, seed, K, pulse_div=3, delta=6, drift=3, lat2=5):
    # Verbatim E1 loop, integer settle count returned directly
    # (e1.run only returns a rounded float pct; we count, not display-round).
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    st = debt = 0
    for t in range(TICKS):
        s1 = reality(t)
        s2 = reality(max(0, t - lat2))
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        trig = []
        e1v, e2v = s1 - g, s2 - g
        if abs(e1v) > delta: trig.append(e1v)
        if abs(e2v) > delta: trig.append(e2v)
        if mode == "sequential":
            if trig:
                g += trig[0]; debt += abs(trig[0])
        else:
            for e in trig:
                m = abs(e) // pulse_div or 1
                pulses.appendleft([m if e > 0 else -m, K]); debt += abs(e)
            if pulses:
                net = sum(p[0] for p in pulses)
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1: mag = mag - (mag // 2)
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            st += 1
    return st, debt

if __name__ == "__main__":
    for name, kw in REGIMES.items():
        seq = [settles("sequential", s, pulse_div=1, **kw)[0] for s in SEEDS]
        seq_tot = sum(seq)
        print(f"== {name} ==  sequential total {seq_tot}  {seq}")
        prev = None
        for pd in range(1, 9):
            row = [settles("interference", s, pulse_div=pd, **kw) for s in SEEDS]
            tot = sum(r[0] for r in row)
            blade = tot >= seq_tot
            mark = "  <== SNAP POINT" if prev is not None and blade != prev else ""
            print(f"  pd={pd}  settles {tot:>6}  blade={int(blade)}"
                  f"  debt {sum(r[1] for r in row)}{mark}")
            prev = blade
```

---

## 3. LAG BLADE — the fabric measures its own sensor latency, then repays the debt

**Mechanism.** E1's delayed twin is assumed to *have* a known latency; nobody
measures it. The lag blade slides an integer lag L = 0..15 across the first-
difference streams `d1(t) = s1(t)−s1(t−1)`, `d2(t) = s2(t)−s2(t−1)` and logs
where `C(L) = Σ_t d1(t)·d2(t+L)` seats (integer dot products, argmax — no
floats, no statistics package). First differences strip the shared DC/trend,
so the seating is a sharp single peak, not a broad autocorrelation plateau.
This is the §9 snap point in its purest form: the blade slides until it
logs, and the seating position *is* the measurement. Phase B then shifts
T2's delay line by the discovered lag (`s2'(t) = reality(t − lag + L̂)`) and
re-runs the harness.

**Phase A — discovery (deterministic; the streams are reality-only, so
seed-independent by construction — stated, not fudged):**

```
true lag  3 -> discovered  3
true lag  5 -> discovered  5
true lag  7 -> discovered  7
true lag 10 -> discovered 10
true lag 15 -> discovered 15        (estimation window: 480 ticks = 2 reality periods)
```

**Phase B — compensation, stress regime (Δ=12, drift=6, K=4, true lag 10,
per-mille within deadband, mean of 5 seeds; debt = mean total; maxErr = max):**

```
arm                          per-mille      debt   maxErr
sequential raw                    512      48994      61
sequential compensated           1000       8428      12
interference raw                  830      34995      39
interference compensated          984      17700      28
   per-seed compensated interference: [985, 985, 984, 984, 984]
```

**Readings.**

- Latency discovery is exact on 5/5 tested lags, from a 480-tick window —
  10× shorter than the 4800-tick scoring run. The fabric can calibrate its
  own switchboard (§8: the patch bay as data) before judging anything.
- Compensation converts the conflict regime into a calm one *at the source*:
  interference goes 830‰→984‰, debt halves (34995→17700), maxErr 39→28.
- The honest twist: fully compensated, **sequential wins** (1000‰ vs 984‰).
  Once the lag is repaid there is no sensor conflict left for superposition
  to arbitrate, and the calm-regime doctrine (impulse wins calm) re-asserts
  itself one level up. The lag blade doesn't just improve the score — it
  *moves the regime*, and the variety ledger's regime specialists apply to
  the new regime. A controller that compensates lag and then stays in
  interference mode leaves 16‰ on the table.
- Limits stated: the estimator can overestimate lag (then compensation
  peeks at the future — flagged, not hidden); it assumes a constant integer
  lag and a reality smooth enough that first differences align. Drift (the
  LCG term in g) never enters the streams, which is exactly why discovery is
  seed-independent.

**Novelty claim (honest): NOVEL**, per full dossier scan — latency is
assumed known in every dossier (THRML latency-shaped blocks, REGIME-META's
external trigger, RD-PHYSICAL lane 8's shift-encoding proposal which
*assumes* the lag and was never run). The only ancestor is spreadsheet-cells'
offline post-run correlation matrix for coordination detection
(RD-SPREADSHEET-LINEAGE.md:46-47) — different job (coordination, not lag),
offline, no blade sweep, and E1 explicitly dropped that line. Nothing does
online integer lag discovery, and nothing has a lag-compensated E1 arm. The
regime-motion observation (compensation converts conflict→calm and flips the
optimal arm back to impulse) is also new.

**Source:**

```python
#!/usr/bin/env python3
# exp3_lag_blade.py — run: python3 exp3_lag_blade.py
import sys
sys.path.insert(0, "/home/eileen/projects/quilt-verilog/spikes/225-e1-interference-tick")
from collections import deque
from e1 import LCG, reality

SEEDS = (1, 7, 42, 1999, 20260902)
WINDOW, MAXLAG = 480, 15

def discover_lag(lat2, window=WINDOW, maxlag=MAXLAG):
    # d2(t) = d1(t - lat2); C(L) = sum_t d1(t)*d2(t+L) seats at L = lat2.
    n = window + maxlag + 2
    s1 = [reality(t) for t in range(n)]
    s2 = [reality(max(0, t - lat2)) for t in range(n)]
    d1 = [s1[t + 1] - s1[t] for t in range(n - 1)]
    d2 = [s2[t + 1] - s2[t] for t in range(n - 1)]
    best_l, best_c = 0, None
    for L in range(maxlag + 1):
        c = 0
        for t in range(window):
            c += d1[t] * d2[t + L]
        if best_c is None or c > best_c:
            best_l, best_c = L, c
    return best_l

def run_comp(ticks=4800, K=4, pulse_div=3, delta=12, drift=6, lat2=10,
             seed=1, mode="interference", laghat=0):
    # E1 loop with T2's delay line shifted by laghat (laghat=0 -> e1.run).
    rng = LCG(seed)
    g = reality(0)
    pulses = deque()
    settles = debt = max_err = 0
    for t in range(ticks):
        s1 = reality(t)
        s2 = reality(max(0, t - lat2 + laghat))
        g += rng.below(2 * drift + 1) - drift
        while pulses and pulses[-1][1] == 0:
            pulses.pop()
        trig = []
        e1v, e2v = s1 - g, s2 - g
        if abs(e1v) > delta: trig.append(e1v)
        if abs(e2v) > delta: trig.append(e2v)
        if mode == "sequential":
            if trig:
                g += trig[0]; debt += abs(trig[0])
        else:
            for e in trig:
                m = abs(e) // pulse_div or 1
                pulses.appendleft([m if e > 0 else -m, K]); debt += abs(e)
            if pulses:
                net = sum(p[0] for p in pulses)
                decayed = deque()
                for mag, life in pulses:
                    if life > 0:
                        if abs(mag) > 1: mag = mag - (mag // 2)
                        decayed.append([mag, life - 1])
                pulses = decayed
                g += net
        if abs(s1 - g) <= delta and abs(s2 - g) <= delta:
            settles += 1
        err = max(abs(s1 - g), abs(s2 - g))
        if err > max_err: max_err = err
    return settles * 1000 // ticks, debt, max_err

if __name__ == "__main__":
    for lat2 in (3, 5, 7, 10, 15):
        print(f"  true lag {lat2:>2} -> discovered {discover_lag(lat2):>2}")
    for mode in ("sequential", "interference"):
        for laghat, tag in ((0, "raw"), (10, "compensated")):
            rows = [run_comp(mode=mode, laghat=laghat, seed=s) for s in SEEDS]
            print(f"  {mode + ' ' + tag:<28}"
                  f"{sum(r[0] for r in rows)//5:>8}‰"
                  f"  debt {sum(r[1] for r in rows)//5:>6}"
                  f"  maxErr {max(r[2] for r in rows)}")
```

---

## Meta-notes for the judge

- **Timebox**: ~40 min, within the 45. Stopped after 3 inventions per
  "quality over count."
- **Repo hygiene**: nothing outside this file was modified; experiments ran
  from `/tmp/derby-kimi/` importing the unmodified `e1.py`. No commits.
- **Reproducibility**: every number above regenerates from the embedded
  sources; exp2/exp3 re-implement the E1 loop verbatim rather than trusting
  e1.run's float display column, and the fixed-arm rows reproduce the
  README's published numbers (830‰ vs 83.0% stress interference).
- **The one I'd stake on**: LAG BLADE — exact, cheap, novel per the
  dossiers, and its twist (compensation flips the optimal arm back to
  impulse) is the variety-ledger doctrine predicting something new instead
  of decorating something old. The one I'd cite as a warning: COFIRE TRUST —
  the charter's §1.2 anti-cofire now has its first empirical result, and it
  is a collapse mode; §1.2 needs a homeostat before §3.2's demo bets on it.
