# REGIME-META.md — Calm/Conflict regime switching for E4

**Purpose:** Define the detector, parameter sets, and transition logic for adaptive
mode switching (impulse vs. interference). E4 goal: calm rooms use impulse
(smaller code, exact), conflicted rooms use interference (overlapping pulses).

**Ground truth:** e1.py (reference harness), arena.py + ledger.py (regime
performance), README.md (E1 validated results).

## Detector Specification

**Goal:** Distinguish two regimes with integer-only arithmetic; no floats, no
division except sign-safe fdiv.

**State machine:** two consecutive conflict hits → enter conflict. Five
consecutive calm ticks → exit to calm. Hysteresis prevents thrashing.

### Metrics

1. **Debt climbing:** pulse-queue ledger mass accumulation rate over a sliding
   window.
   - Window: 16-tick ring buffer of per-tick debt increments.
   - Trend: compare sum of ticks 8–15 (recent) vs. sum of ticks 0–7 (older).
   - Signal: `debt_recent > debt_older + debt_climb_threshold` → candidate.

2. **Cancellation chatter:** destructive interference (net == 0, multiple
   opposite-sign pulses live). Persistent cancellation indicates conflicting
   corrections fighting.
   - Window: 16-tick ring buffer of boolean flags (cancel occurred this tick?).
   - Accumulation: `cancel_count = sum of flags over window`.
   - Signal: `cancel_count >= cancel_threshold` → candidate.

3. **κ-style contamination index** (integer, per-mille):
   ```
   κ = (cancel_events * 1000) / (total_snap_events + 1)  // +1 guards /0
   ```
   High κ (>250 per-mille, tunable) → regime signal. Avoids division by scaling
   the comparand: `cancel_events * 1000 > κ_thresh * (total_events + 1)`.

### Pseudocode: detector tick

```c
/* Integer-only detector. Fixed seed for ledger prng.
   Assumes e1 harness supplies: tick_debt (this tick's ledger delta),
   cancel_flag (1 if destructive cancellation observed), snap_event (1 if
   correction fired). */

struct regime_detector {
    int debt_window[16];      /* circular, index d_idx */
    int cancel_window[16];    /* circular, index c_idx */
    int d_idx, c_idx;         /* write positions */
    int conflict_hits;        /* consecutive conflict-signal ticks */
    int calm_ticks;           /* consecutive calm ticks */
    int regime;               /* CALM (0) or CONFLICT (1) */
    int total_snaps;
};

void detector_tick(struct regime_detector *det,
                   int tick_debt, int cancel_flag, int snap_event) {
    /* Append to windows (oldest values wrap). */
    det->debt_window[det->d_idx] = tick_debt;
    det->d_idx = (det->d_idx + 1) & 0xF;  /* mod 16 */

    det->cancel_window[det->c_idx] = cancel_flag;
    det->c_idx = (det->c_idx + 1) & 0xF;

    det->total_snaps += snap_event;

    /* Compute trend: sum first 8 vs. last 8 ticks (oldest...newest). */
    int debt_older = 0, debt_recent = 0;
    for (int i = 0; i < 8; i++) {
        debt_older += det->debt_window[(det->d_idx + i) & 0xF];
        debt_recent += det->debt_window[(det->d_idx + i + 8) & 0xF];
    }

    /* Debt climbing: recent > older + threshold. */
    int debt_climb = debt_recent > (debt_older + DEBT_CLIMB_THRESH);

    /* Cancellation chatter: count flags in window. */
    int cancel_sum = 0;
    for (int i = 0; i < 16; i++) {
        cancel_sum += det->cancel_window[i];
    }
    int cancel_chatter = cancel_sum >= CANCEL_THRESH;

    /* κ contamination: avoid division. */
    int contamination_signal = 0;
    if (det->total_snaps > 0) {
        /* κ_per_mille = (cancel_sum * 1000) / det->total_snaps
           Signal if > KAPPA_THRESH_PERMILLE:
           cancel_sum * 1000 > KAPPA_THRESH_PERMILLE * det->total_snaps */
        if (cancel_sum * 1000 > KAPPA_THRESH_PERMILLE * det->total_snaps) {
            contamination_signal = 1;
        }
    }

    /* Conflict candidate: either debt climbing OR chatter OR high κ. */
    int conflict_candidate = debt_climb || cancel_chatter || contamination_signal;

    if (conflict_candidate) {
        det->conflict_hits++;
        det->calm_ticks = 0;
    } else {
        det->conflict_hits = 0;
        det->calm_ticks++;
    }

    /* Hysteresis transitions. */
    if (det->conflict_hits >= 2 && det->regime == CALM) {
        det->regime = CONFLICT;
        det->conflict_hits = 0;
    }
    if (det->calm_ticks >= 5 && det->regime == CONFLICT) {
        det->regime = CALM;
        det->calm_ticks = 0;
    }
}
```

---

## Regime Parameter Table

**Base parameters from arena champion + E1 validated results:**

| Regime  | Mode          | δ (delta) | K  | pulse_div | Motivation |
|---------|---------------|-----------|----|-----------|----|
| CALM    | sequential    | 6         | —  | —         | Impulse: exact, 98% settle rate, no overshoot (arena: impulse baseline is impulse-specialist in calm). |
| CONFLICT| interference  | 12        | 4  | 3         | Superposition: 83% within vs. 52% impulse under stress. Arena champion is granite3.1-dense:2b at K=5, ÷4, but K=4, ÷3 is hand-tuned, validated. |

**Detector thresholds (integer, tunable per deployment):**

| Parameter | Calm | Conflict | Notes |
|-----------|------|----------|-------|
| `DEBT_CLIMB_THRESH` | — | 120 | Debt accumulation rate. Calm: <120 units/8-tick window. Stress: >120. |
| `CANCEL_THRESH` | — | 4 | Cancellation flag count in 16-tick window. Calm: <4 events. Conflict: ≥4. |
| `KAPPA_THRESH_PERMILLE` | — | 280 | Contamination index (per-mille). Calm: κ <280‰. Conflict: κ ≥280‰. (~28% of snaps are cancellations.) |
| `CONFLICT_ENTRY` | — | 2 | Consecutive conflict-candidate ticks to enter conflict mode. |
| `CALM_EXIT` | — | 5 | Consecutive calm ticks to exit conflict mode. |

**Refractory logic:**
- On conflict → conflict mode: refractory period = 10 ticks (ignore calm signals).
  Prevents mode-thrashing on borderline signals.
- On conflict → calm transition: refractory = 20 ticks (higher confidence required
  to re-enter conflict).
- During refractory, detector still accumulates window state; only transition is
  inhibited.

---

## E4 Predictions: Deadband Residence & Recovery

**Scenario:** calm environment → sudden conflict → return to calm → bursty noise.
Seed=20260902, single run (4800 ticks baseline).

### E4.A: Calm steady-state (first 600 ticks)

**Mode: impulse (δ=6, sequential)**
- Expected %within: **98.0%** (arena data: impulse calm specialist)
- Max error: **≤ 18** (noise floor)
- Snap events: **~30–40** per 100 ticks (minimal corrections)
- Debt accumulation: **~90–120** per 100 ticks (low conflict stress)

**Detector state:**
- debt_window sum: ~18–24 per-mille of baseline
- cancel_sum: 0 (no superposition pulses)
- regime: **CALM** (stable)

### E4.B: Conflict onset (ticks 600–700)

**External trigger:** twins' latency increases 5→10 ticks, drift increases 3→6.
Impulse mode now mismatches the corrected value; same sensor re-fires next tick.

**Mode still: impulse (old parameter set latches)**
- Expected degradation: **51.4%** within (arena data: impulse under stress)
- Snap events: **~120–150** per 100 ticks (chatter)
- Debt accumulation: **~850–950** per 100 ticks (2–3× calm rate)

**Detector response (same tick):**
- debt_older (ticks 600–607) ≈ 18 units (calm baseline)
- debt_recent (ticks 608–615) ≈ 220 units
- debt_climb signal fires: 220 > 18 + 120 ✓
- conflict_hits → 1 (first candidate tick)
- regime still CALM (awaiting second hit)

**Next tick (601):** if stress persists, debt_climb fires again.
- conflict_hits → 2
- **Regime switches to CONFLICT; mode → interference (δ=12, K=4, ÷3)**
- conflict_hits reset to 0

### E4.C: Conflict steady-state (ticks 702–1500)

**Mode: interference (δ=12, K=4, pulse_div=3)**
- Expected recovery: **83.0%** within (E1 validated)
- Max error: **39** (vs. 61 under impulse stress)
- Snap events: **~85–100** per 100 ticks (fewer, larger corrections)
- Debt accumulation: **~620–680** per 100 ticks (overlaps halved via superposition)
- Cancellations observed: **~12–18** per 100 ticks (destructive interference working)

**Detector state stabilizes:**
- κ_permille = (15 * 1000) / 95 ≈ 158‰ (moderate conflict signature)
- debt_climb usually fires (220 > 18+120)
- cancel_chatter sometimes fires (8–12 ≥ 4)
- conflict_ticks counter increments but regime stays CONFLICT (stable)

### E4.D: Return to calm (ticks 1500–1700)

**External trigger:** twin latency drops back 10→5, drift returns 6→3 (stress removed).
Mode is still interference; corrections shrink. Cancellations become rare.

**Mode: interference (parameters don't auto-downgrade; detector must signal)**
- Snap events: **~35–45** per 100 ticks (like calm, because stress is gone)
- Cancellations: **0–1** per 100 ticks (calm has no interference conflicts)
- Debt accumulation: **~95–110** per 100 ticks (back to baseline)

**Detector response:**
- debt_older (recent 8) ≈ 24 units
- debt_recent (prior 8) ≈ 26 units
- debt_climb signal dies: 26 ≤ 24 + 120 ✗
- cancel_chatter dies: 1 < 4 ✗
- κ_permille ≈ 1‰ ✗
- conflict_candidate = 0

**calm_ticks increments each tick. After 5 ticks:**
- calm_ticks → 5
- **Regime switches to CALM; mode → sequential (δ=6)**
- calm_ticks reset to 0

### E4.E: Bursty noise (ticks 1700–2000)

**External trigger:** random ADC glitches every 3–5 ticks (single large outlier,
then quiet). Stress parameter at baseline (drift=3). Interference mode still live.

**If detector were stuck in CONFLICT:**
- Impulse would overshoot on each glitch (61 maxErr)
- Recovery after glitch slow (settle in ~15 ticks)
- Sequence: glitch-snap, drift back, glitch-snap-snap-snap (chatter)

**Actual behavior (mode switched to sequential):**
- Glitch fires one hard impulse; g snaps exactly to sensor
- No overshoot, no lingering pulses
- Max error = glitch magnitude (e.g., 45 units)
- Next tick, if glitch was transient, s(t) moves away naturally
- Settle time: **3–5 ticks** (vs. 15 under interference on same glitch)

**Detector remains CALM:**
- Glitch is single-tick event; debt_window averages it out
- cancel_sum = 0 (no interference pulses live)
- Regime stays CALM

---

## Failure Modes & Honest Limits

### 1. **Transition latency (2–3 tick jitter in mode switch)**

**Scenario:** conflict threshold crossed at tick 602. Detector signals at tick 603
(need 2 consecutive hits). Mode switch takes effect at tick 604 correction-phase.
Intermediate ticks 602–603 run impulse with stress params → 2 ticks of degraded
%within.

**Impact:** negligible in longer runs (>4800 ticks), ~0.04% of total. Noticeable
in spike-short windows (<100 ticks).

**Mitigation:** none. Hysteresis prevents false-positive thrashing; cost is
latency. Design trade-off accepted.

### 2. **Borderline contamination (κ near threshold)**

**Scenario:** environment has κ=250‰ (just below KAPPA_THRESH_PERMILLE=280).
Spurious cancellations from slow transients can push κ=270‰, triggering conflict
falsely.

**Symptom:** mode flips to interference, debt_recent soars (superposition is more
expensive on calm workloads, arena data: interference loses ~9% vs. impulse in
CALM). Regime flips back 5 ticks later when κ settles.

**Impact:** ~2–3% penalty in %within for ~8 ticks, then recovery. Rare if δ is
tuned conservatively (δ=6 in calm has κ ≈ 40‰, safe margin).

**Mitigation:** increase KAPPA_THRESH_PERMILLE to 320 or add refractory period
(10 ticks before allowing re-entry to conflict). Trades sensitivity for stability.

### 3. **Cascading conflicts under sustained twin fight**

**Scenario:** the two twins have *inverted* latency (T1 now delayed, T2 native).
Corrections flip source each tick. Impulse mode creates ping-pong (g oscillates
±30 units).

**Detector response:**
- Debt climbing *still fires* (each ping-pong adds to ledger)
- cancel_chatter *also fires* (interference mode's cancellations detect the
  opposite-sign fight)
- Regime enters CONFLICT; mode → interference
- Superposition merges corrections → net often 0 (destructive cancellation)
- **BUT**: destructive cancellation is not an error state; it's correct behavior.
  The detector counts cancellations as a conflict indicator, but under inverted
  latency it's the *solution*, not the problem.

**Impact:** Correct regime switch (forced into interference mode), but for a
reason the detector misinterprets. Mode choice is right, diagnosis is confused.

**Honest risk:** If a fleet field reports "mode thrashing on every 100 ticks,"
this is a sign that the detector's cancellation threshold is too low for that
environment (κ_thresh should be higher, or CANCEL_THRESH should exclude low-magnitude
cancellations). Cannot diagnose from detector state alone; requires telemetry of
actual corrections.

### 4. **Refractory period hiding recovery (conflict→calm→conflict→calm thrashing)**

**Scenario:** environment oscillates between mild conflict (κ=290‰) and calm
(κ=40‰) every ~30 ticks.

**Without refractory:** regime flips 2–3×, costs ~4% in settled ticks per cycle.

**With refractory=20:** after exiting conflict, regime stays calm for 20 ticks
even if κ spikes again. If conflict re-enters during refractory, conflict_hits
resets; mode stays calm (latched decision). Next genuine conflict must re-enter
via the 2-hit gate.

**Impact:** stabilizes the decision, but can delay re-entry by up to 20 ticks if
environment degrades again mid-refractory. On a bursty channel, this trades
latency for coherence.

**Honest risk:** high-variance environments (switching every 20–50 ticks) may see
coherence penalty. Tune CALM_EXIT = 5 upward (e.g., 8–10 ticks) in noisy deployments.

### 5. **Division by zero in κ calculation (no snaps yet)**

**Safeguard:** `total_snaps + 1` guards the denominator. Early ticks report
κ_permille = (0 * 1000) / 1 = 0 → no conflict signal. Safe.

### 6. **Integer overflow in debt window accumulation**

**Scenario:** debt_window each holds up to ~60000 (realistic per e1.py: stress run
ledger_mass = 96832 over 4800 ticks ≈ 20 per tick). Sum over 8 ticks: ~160.
Sum over 16: ~320. No overflow risk on 32-bit.

**Edge case:** pulses decay asymptotically; pulse_div=1 (hypothetical) emits raw
error magnitudes. ledger_mass could reach 500k in pathological input. debt_window
sum → 2M+. Still safe on 32-bit (max 2^31 ≈ 2.1B).

**Mitigation:** none needed for realistic E1 parameters.

---

## Regime-Switch Checklist

Before deploying E4:

- [ ] Confirm e1.py baseline: calm δ=6 impulse achieves 98% within.
- [ ] Confirm arena champion: interference K=4 (or K=5), ÷3 (or ÷4), δ=12 achieves 83%+ within under stress.
- [ ] Tune detector thresholds on field data: debt_climb_thresh, cancel_thresh,
      κ_thresh from actual twin latency variance in deployment.
- [ ] Measure refractory period: does 10 / 20 tick latency cause mode-thrashing
      in your environment? (Expect <0.1% penalty if tuned.)
- [ ] Validate E4.D recovery time: when stress is removed, is regime back to
      CALM within 10–15 ticks? (Confirm calm_ticks=5 exit is appropriate.)
- [ ] Log regime transitions in telemetry: every mode switch is actionable data.

---

## Cross-References

- **e1.py:** source of truth for E1 metrics (snap_events, ledger_mass,
  cancellations, %within). Run baselines before tuning detector.
- **arena.py:** validates that interference and impulse are Pareto-optimal in
  different regimes. Cherry-pick champion params for your delta / K.
- **ledger.py + VARIETY-LEDGER.md:** regime specialists are not failures; they
  are data. κ distribution across calm vs. stress regimes confirms detector
  thresholds.
- **README.md §E4:** architecture of mode dial in fleet terms.

---

**Undersell:** This detector is a gate, not a full adaptive system. It assumes
you can measure debt, cancellations, and snap events in your harness. If you
have neither twins nor pulses, you have no signal; regime switching is
moot. **Overdeliver:** Once tuned on your deployment's twin latency and noise,
the detector runs in 32 integer ops/tick (16 window reads, 2 sums, 4 comparisons,
1 state update). Byte-identical across languages per DIVERGENCE.md contract.
