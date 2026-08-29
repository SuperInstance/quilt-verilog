# V2 NOTES — the judge's must-ship pair, as built

**Lane:** v2-features · **Date:** 2026-08-29
**Mandate:** `docs/INNOVATION-JUDGEMENT.md` §5 fold-ins 1+2 — the echo gate
(opencode, winner) and RQH (flash, runner-up) ship **in the same merge**:
the gate's `g = 15 − msb(F)` turns every gated cofire into a graded
insertion; RQH banks the fraction that insertion drops. Each converts the
other from curiosity to payoff (§4.4).

**Status: built, integrated, verified.** 11/11 testbenches pass
`iverilog -g2005` (8 pre-existing, bit-exact, + 3 new); `verilator
--lint-only -Wall` clean on `rtl/` (fabric top and per-module tops); the
QUF loader lane (which compiles the modified dialfile) still passes
byte-exact.

---

## 1. Integration choice: in-core, not sidecar

Both features are instantiated **inside `rtl/q_cell_core.v`** (the edge
engines stay in `q_cell.v`). This was the "only if clean" path and it
proved clean:

- Every v1 file change is additive behind default-off dials
  (`FLOOR=0`, `RQEN=0`), collapsing to bit-exact v1 — verified by the
  **unchanged** v1 acceptance gate `tb_fabric_smoke.v` passing with the
  identical `maxlat=31` (same timing, same goldens, zero drift).
- All 8 pre-existing TBs pass unmodified against the integrated RTL.
- The gated path can only *shorten* the effect op (skip-train reads the
  weight directly), so the Q1 `ci_ready`-gap bound is preserved by
  construction.

### Per-file delta

| File | Delta |
|---|---|
| `rtl/q_echo_gate.v` | **new** — the fire trace (opencode's verified `q_echo_trace` design, §4.1 verbatim semantics; see hardening in §3.3) |
| `rtl/q_rqh_bank.v` | **new** — per-edge residue bank with the **corrected** deposit (§3.2) |
| `rtl/q_hebb_edge.v` | + `i_gclass` port; + engine cmd `3'b101` (graded cofire: ladder lands in bucket `clamp(gclass, K−1)`, hyperbola ≡ cmd 001). Cmd `001` and all other commands byte-identical |
| `rtl/q_cell_core.v` | + `K` param; + gate/bank instances; `ST_EFFT` gate issue (open → cmd 101 + `hb_gcl`; closed → cmd 011 skip-train, act integrates ungated); `ST_TLEAK` fire pulse + once-per-tick leak strobe; credit folded into `eff_sum` and the `wsum` view accumulate (`ST_VACW`); + dial/status ports |
| `rtl/q_dialfile.v` | + dials 11–15 (below); + `i_probe` input (live trace aliased read-only at dial 13; writes ignored) |
| `rtl/q_cell.v` | wiring only (dials → core, `hb_gcl` → engines, probe → dialfile, `o_antic` status tap) |

## 2. Dial map (v2 additions)

| addr | dial | reset | meaning |
|---|---|---|---|
| 11 | `KLE` | 2 | echo-trace leak shift (τ ≈ 4·ln2 ticks) |
| 12 | `FLOOR` | **0** | echo gate floor; **0 = gate off = bit-exact v1** (the A/B referee) |
| 13 | `FTRACE` | — | read-only probe of the live trace `F` via `view(2)` |
| 14 | `RQ` | 0x0008 | bit 15 = `RQEN` (master enable); bits 3:0 = `QDW` (quanta/credit shift) |
| 15 | `RQL` | 0x0008 | bits 3:0 = `QLEAK` (reservoir deadband leak shift) |

## 3. Deviations from the proposals (all honest, all cited)

### 3.1 Graded train is a new engine command, not a rewiring of cmd 001
opencode §4.2 sketched re-wiring cmd `001`'s ladder branch to read
`i_gclass`. As built, the graded cofire is a **new** engine command `101`;
`001` keeps its exact v1 semantics. This keeps `tb_hebb_edge.v` (which
instantiates the engine without `i_gclass` and only issues 001/010/011/100)
bit-exact with the port left unconnected — the same freeze-the-gate-not-the-
law discipline the Tap night asked for. Fabric Law 2 is untouched: `hb_cmd`
is cell-internal, not a flit opcode.

### 3.2 The RQH deposit is the corrected condition (C3/T3c), not `2^g`
`docs/academic/error-envelopes.md` Theorem 3c falsified the original
deposit (misses the convergence condition by ~9,100× at class 0, class
dependence inverted). The bank implements the corrected magnitude:

```
deposit(g) = 2^(K+QDW−g)·(1 − 1/(2 ln 2))      (exact, T3c)
           ≈ (2^(K+QDW−g) >> 2) + (2^(K+QDW−g) >> 5)   (9/32 = 0.28125, +0.9%)
```

— two shifts and one add, as the paper prescribed. With K=QDW=8: a fresh
(class-0) cofire banks 18,432 quanta → 72 readout LSBs of credit ≈ the mean
band overstatement of a fresh cofire (0.2787·256), i.e. the bank now tracks
the actual quantization debt. Consequences, stated per T3: the credit is
bounded (≤ 2^(RW−QDW)−1 = 255 LSB), envelope-**preserving** (the worst-case
band is additively widened, never tightened — the strong claim stays false),
and `o_antic`'s cadence is ~2^(g−K)/0.28 cofires per credit (~3.6 fresh),
not the proposal's 2^(QDW−g). `RQEN=0` is bit-exact passthrough (credit 0,
antic 0, reservoirs frozen), per the original RQH promise.

### 3.3 Deadband snap hardened past both sketches (found by the new TBs)
The sketched snap (`leak ≤ 1`) leaks by exactly zero once the state drops
below 2^shift: values in `[2, 2^shift − 1]` **park forever**. For the bank
that is a stale base that could later cross a credit boundary with no fresh
cofire (flash's own limit 6, un-closed at the tail); for the gate with a
small FLOOR and large KLE the parked trace sits **above** the floor — an
immortal open gate. Both modules snap additionally on **no-progress**
(`leak ≥ state`); the flowing regime is unchanged (verified: every
flowing-tick golden in both TBs is untouched by the fix), and
`tb_q_echo_gate` carries the pathological combo (KLE=4, FLOOR=2) as an
explicit drain-to-zero regression.

### 3.4 Echo-gate default FLOOR is 0, not 0x0080
opencode proposed 0x0080 as the default floor. As built the reset default
is **0** (gate off): the v1 acceptance gate `tb_fabric_smoke` must pass
unchanged per the A/B contract, and under the gate its training phase would
train nothing (cell 1 has not fired when the 100-effect stream arrives).
Opt-in is one dial write — exactly the referee's switch.

### 3.5 Class bracket direction (doc note, no RTL change)
opencode §3 states the class bracket as `2^-g ∈ (k/2, k]`; the implemented
`g = 15 − msb(F)` delivers `2^-g ∈ (k, 2k]` (k = F/Fmax). The RTL is the
intended one — a bucket-g cofire is an event born ~g half-lives old under
the ladder's aligned-phase convention, which is the object Theorem 1's
`W ≤ Ŵ < 2W` already bounds. The prose bracket was the mis-phased twin;
noted so nobody "fixes" the encoder to match the sentence.

## 4. Test matrix

| TB | Status | Covers |
|---|---|---|
| `tb_q_echo_gate` (new) | PASS | reset/dead; fire refill; leak recurrence bit-exact KLE∈{1,2,3} ×40 ticks; real envelope `k(d)·F0 ≤ f ≤ k(d)·F0+d+1`; dyadic bracket on every live tick; snap hysteresis + window length (snap at tick 22 vs analytic 21.7); sticky-band drain regression (KLE=4/FLOOR=2); fire-beats-leak; disabled mode; dead trace |
| `tb_q_rqh_bank` (new) | PASS | disabled A/B (outputs 0, reservoir frozen through a storm); corrected deposit bit-exact g=0..7 (18432…144 quanta); class clamp g≥K; credit/antic cadence with saturation (6 class-0 trains → credits 72,144,216,255,255,255 → exactly 4 antics); class-3 cadence; deadband leak bit-exact + full drain + stay-zero; train-beats-tick; cross-edge isolation; QDW=6 scale-invariance (credit per cofire is QDW-independent — the T3c 2^QDW factor cancels) |
| `tb_fabric_smoke_v2` (new) | PASS | **P1** flooding sender ×60 at a never-fired cell: `wsum == base` exactly (v1 would read base+60·256), FTRACE=0; **P2** fire observed (act→0, FTRACE=0xFFFF), graded cofires land in buckets 0/1/4 with exact wsum steps +256/+128/+16 as the trace decays; **P3** RQH credit visible in w readout (class-4 cofire moves wsum +16 engine +4 credit, bit-exact), RQEN A/B off/on mid-stream (credit suppressed/reappears — same stored ladder), class-5 cofire with leak accounting; **P4** FLOOR=0 + RQEN=0 collapse to ungated +256/cofire, engine ladder only |
| 8 × v1 TBs | PASS | unchanged files, unchanged goldens; `tb_fabric_smoke` maxlat identical (31) — timing-exact, not just value-exact |
| `verilator --lint-only -Wall` | clean | `rtl/` whole (fabric top) + `q_cell`, `q_echo_gate`, `q_rqh_bank`, `q_hebb_edge` tops |
| QUF loader lane | PASS | dialfile change is read-compatible (byte-exact readback) |

## 5. Honest limits (in addition to each proposal's own list)

1. **MODE=1 is binary-gated and RQH-unclaimed.** The hyperbola engine gets
   the rectangular gate window only (no fractional buckets); train-side
   deposits cannot correct its dominant *temporal* error (T2), so RQH
   ships scoped to MODE=0 per the judgement §4.2 — deposits still occur in
   MODE=1 (bounded, harmless, experimental).
2. **A one-sided credit centers, never closes** (T3c). The corrected
   deposit makes the credit's long-run rate equal the band-overstatement
   rate — the strongest property available without a signed correction,
   which would require observing the mis-phase.
3. **Saturation headroom.** RW=16 with QDW=8: a single class-0 deposit is
   28% of the reservoir (≈3.6 fresh cofires to saturation under flood);
   credit caps at 255 LSBs (T3a bound). Operators wanting finer retention
   can dial QDW down (credit per cofire is QDW-invariant; only the
   fractional-LSB tail and the cap change).
4. **`o_antic` is a status tap** exposed on the core (`o_antic`) and
   probed hierarchically; it is not yet wired to any dial/vMF consumer —
   the anticipation-to-dial coupling remains a v3 acceptance arm.
5. **The v2 smoke's graded-class constants are phase-locked** to the
   deterministic tick scheduler (TPW=10; every wait window contains exactly
   N tick services). They are golden values in the v1-smoke tradition; a
   pacing edit will move a class and fail the assert loudly rather than
   silently.

## 6. Not shipped (per the judgement's fold-in list)

TCH (second gate), DWS (alternate class-source dial), CTHL (storage fix
required) — untouched, awaiting their own lanes.
