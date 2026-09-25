# PHASE-0 ARTIFACT 2 — Replay SPIN-29's canary suite, reproduce booked numbers

**Lane:** FORGE CURRICULUM Phase 0, artifact 2 of 4 (charter §Phase-0 item 2) · branch `g3-kinduction` · 2026-09-03
**Target:** `wheel/SPIN-29-metrology-cdelta.md` (booked 2026-09-03 17:32 AKDT, script `spin29_metrology_cdelta.py`, committed output `spin29-output.txt`).
**Replay environment:** same tree, same interpreter (`python3 -u` direct redirect, no pipes — harness rule honored), no code changes (`git status` clean on the wheel scripts).

## VERDICT UP FRONT

**ALL FOUR CANARIES PASS; every booked number reproduces digit-for-digit; replay vs committed output is byte-identical except the timestamp on line 1.** Charter item 2 ("reproduce its booked numbers byte-exactly") is met at the strongest reading available: the script's own line-1 timestamp makes literal byte-identity across time impossible; everything after line 1 — canaries, full 5×17 panel, K=2 column, analysis, verdicts — matches with zero diff lines.

## Receipts

### R1 — Full replay run 1 (command + elapsed)

```
$ cd spikes/225-e1-interference-tick/wheel
$ python3 -u spin29_metrology_cdelta.py > /tmp/spin29-replay-1.txt 2>&1
real 0m5.819s   (booked: "elapsed 6 s" — matches)
```

Canary block, verbatim from the replay output (`spin29-replay-output.txt:7-21`):

```
== CANARY a: wiring byte-identity dyn_run(R0,d12) vs run_fabric ==
  PASS: 16 configs byte-identical
== CANARY b: R0 anchors at delta=12 (5-seed means) ==
  ladder15 K=1: pct=71.48 (71.5)  ev=5791.6 (5792)  debt=106378.4 (106378)  -> PASS
  zero    K=1: pct=77.26 (77.3)  debt=187833.6 (187834)  -> PASS
== CANARY c: delta=12 slope-1.6 replay of SPIN-27 s*==17.9 ==
  s*=17.6 (want ~17.9 tol 1.0)  C=28.1 (want ~28.6 tol 1.5)  -> PASS
== CANARY d: determinism (dual runs, all deltas) ==
  PASS: 30 dual runs byte-identical
ALL CANARIES: PASS
```

Per-canary verdict vs SPIN-29's booking:

| canary | booked (SPIN-29 .md) | replay | verdict |
|---|---|---|---|
| (a) byte-identity vs `exp_glm1.run_fabric`, Δ=12 leg | 16/16 configs | **16/16** | **PASS** |
| (b) anchors ladder15/zero (pct/ev/debt) | 71.5 / 5792 / 106378; 77.3 / 187834 | 71.48 / 5791.6 / 106378.4; 77.26 / 187833.6 | **PASS** (exact) |
| (c) Δ=12 SPIN-27 replay | s*=17.6, C=28.1 | **s*=17.6, C=28.1** | **PASS** (digit-for-digit) |
| (d) determinism, 30 dual runs | byte-identical | **byte-identical** | **PASS** |

### R2 — Booked-number reproduction (headline panel)

Every headline value from `SPIN-29-metrology-cdelta.md`'s table reproduces exactly (replay `spin29-replay-output.txt:34-44` vs committed `spin29-output.txt:34-44`):

| Δ | booked s* / C / α | replay s* / C / α | match |
|---|---|---|---|
| 8 | 12.5 / 20.0 / 1.247 | 12.5 / 20.0 / 1.247 | ✅ |
| 10 | 15.4 / 24.6 / 1.228 | 15.4 / 24.6 / 1.228 | ✅ |
| 12 | 17.6 / 28.1 / 1.172 | 17.6 / 28.1 / 1.172 | ✅ |
| 16 | 23.5 / 37.7 / 1.177 | 23.5 / 37.7 / 1.177 | ✅ |
| 20 | 29.7 / 47.5 / 1.188 | 29.7 / 47.5 / 1.188 | ✅ |
| α range | 6.3% | 6.3% | ✅ |
| K=2 @Δ12 | s*=17.8, C=28.6 | s*=17.8, C=28.6 | ✅ |

Full 5×17 residency panel and every per-spread cell also match (zero diff lines beyond line 1 — see R3).

### R3 — Byte-identity vs committed output

```
$ diff /tmp/spin29-replay-1.txt spin29-output.txt
1c1
< SPIN-29 METROLOGY C=f(delta) — 2026-09-03 18:00:59
> SPIN-29 METROLOGY C=f(delta) — 2026-09-03 17:32:33
```

**Exactly one differing line: the timestamp header.** 100% of data lines byte-identical.

### R4 — Independent dual-run determinism (beyond the script's internal canary d)

```
$ python3 -u spin29_metrology_cdelta.py > /tmp/spin29-replay-2.txt
$ diff /tmp/spin29-replay-1.txt /tmp/spin29-replay-2.txt
1c1  (timestamps 18:00:59 vs 18:01:09 — line 1 only)
```

Two fresh end-to-end runs agree on every line except the timestamp. (Canary d's "30 dual runs" is internal; this checks whole-process reproducibility including the panel.)

## Honest boundaries

- **Byte-identity is modulo line-1 timestamp** — the script stamps its own run time. I judge this satisfies "byte-exactly" (the stamp is not a booked number), but the reader lane should see it stated, not discovered.
- Replay ran on the same machine/tree, minutes-to-hours after the booking, same Python — this is a determinism + arithmetic replay, not a portability test. No claim about other interpreters.
- Artifact 1's contamination does not touch this artifact: SPIN-29 replay used no REPORT.md content; the target was the SPIN-29 spin file and its committed output.
- Replay output preserved at `wheel/phase0-curriculum/spin29-replay-output.txt` for the grading lane.
