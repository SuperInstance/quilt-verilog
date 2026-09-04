# SPIN-36-SILICON — synth the PW=41 fabric (SPIN-34 next rung)

**Verdict: MIXED, per the pre-registered gates as frozen.** H1 (clean synth) PASS, H2b (θ-arm total drops or holds at PW=41) PASS, H2a (θ marginal within ±15% of SPIN-19's 886 LUT4 / 268 CARRY) FAIL — the marginal did not merely hold, it **collapsed**: LUT4 111 (−88%), CARRY 155 (−43%).

## Salvage note (lane history, booked honestly)

Dispatch 2026-09-03 21:45 AKDT; the subagent lane died mid-flight and the batch was declared INCONCLUSIVE at 22:02 with a scar booked (multi-minute yosys legs need a detached runner). The staged yosys legs had actually survived as detached processes and completed at 22:11 (PW=41 arms). This tick completed the missing PW=48 legs with the lane's own staged scripts (`spin36_pw48_{theta,never}.ice40`, run sequentially under `setsid`, ~21 + ~16 min) and executed the lane's frozen analysis driver `spin36_silicon.py` unmodified (one file-naming shim: the driver expects `spin36-synth-pw4X_{arm}-output.txt`; surviving logs were hyphenated — byte-identical copies made).

## Numbers (yosys 0.47+22 iCE40 synth, `spin36_synth_top` PW wrapper)

| arm | LUT4 | DFF | CARRY | CHECK problems | dlatch |
|---|---|---|---|---|---|
| PW=48 never | 16914 | 309 | 12566 | 0 | 0 |
| PW=48 theta | 17259 | 309 | 12876 | 0 | 0 |
| PW=41 never | 13263 | 288 | 9630 | 0 | 0 |
| PW=41 theta | 13374 | 288 | 9785 | 0 | 0 |

Canaries: ALL PASS — RTL replays byte-identical to SPIN-34 published traces (kcoh5_gate s1 sha `5621c4c1e813ab32`, step5_gate s1 sha `6680a395fa140ad3`), double-run deterministic, Python model anchor sha matches, GUARD64 sized-literal scar present.

## Gate reading (honest, per pre-reg)

- **H2a FAIL is a stale-anchor artifact, and the driver says so obliquely**: it re-measures the PW=48 marginal at **345 LUT4 / 310 CARRY** — far from SPIN-19's 886/268 — because the RTL lineage changed under SPIN-34 (GUARD widened to 64-bit, q_wall_gate PW-parameterized). Against the *re-measured* PW=48 marginal, PW=41's 111/155 is still a −68% / −50% drop: the θ-gate's cost shrinks **superlinearly** with pulse width, not the ~linear 15% the dispatch brief guessed.
- **H2b PASS cleanly**: θ-arm total 17259 → 13374 LUT4 (−23%), CARRY −25%. The 15% width cut buys a 23–25% fabric cut.
- **H1 PASS**: zero CHECK problems, zero inferred latches in all four arms (18 warnings each — same benign set).

## Booked conclusion

The cosim side already showed PW=41 is functionally tight (SPIN-34: min-PW 41, 35/35 bit-exact). SPIN-36 adds the silicon side: **at PW=41 the θ-gate is nearly free** (111 LUT4 / 155 CARRY on a 13.4k-LUT fabric, ~0.8%). For the embedded target, the SPIN-34/22 recommendation stands upgraded: hard-code the 1-bit `nf > 2*pd` gate where possible; where the full θ-arm is kept, PW=41 is the right fabric point — cheaper *and* gate-cheaper.

Not done here (booked): nextpnr timing legs (the lane's staged files, named `*.ice40`, were yosys script dumps, not PnR output — PnR never ran; they are committed as `spin36_pw4*.ys`. Do not mistake them for bitstreams). Timing closure is the natural SPIN-37-adjacent rung if silicon numbers are ever needed beyond cell counts.

Raw: `../cosim/stat36_pw4*.txt`, `spin36-output.txt` (driver), yosys logs kept on disk uncommitted (55–65 MB each).
