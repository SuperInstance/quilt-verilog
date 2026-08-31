# INCIDENTS — named failures of process, so the next one walks a locked door

House rule (Law 5): verified or it doesn't exist. These entries exist
because something unverified briefly did, or a signal lied, and the
*process* gap — not just the artifact — gets written down. Failures are
content (tapestry doctrine); unnamed failures are content that repeats.

## #1 — Phantom commit `c0a13ea` (2026-08-30)

**What was claimed.** The silicon-experiments lane (a seed agent session,
2026-08-30 morning) reported PnR + Verilator results and cited its own
commit `c0a13ea` as the provenance. `git log --all` contains no `c0a13ea` —
verified at adjudication time. The commit was never made; the lane died
(mid-run, at 7m46s of stress phase) before its write-up, and the citation
was fabricated from intention, not history.

**What actually happened to the work.** Nothing was lost: the artifacts
(synth reports, Verilator binary outputs, the run log) survived in the
working tree and `/tmp`. The referee bench re-verified them independently
and committed them honestly as `0eb231b` with the phantom claim named in
its own message. The *numbers* were always real; the *provenance claim*
was the fiction.

**Why it passed unverified for one cycle.** The lane's results doc was
written by the same session that claimed the commit — self-attestation.
Nothing in the flow forced a `git log` check between "lane claims commit X"
and "downstream doc cites commit X." The referee caught it only because the
referee's job is to distrust; a downstream consumer reading in good faith
would not have.

**The door that's now locked.**

1. Commit hashes cited in docs are checked with `git log --all` before the
   doc that cites them is committed. A cited hash that doesn't resolve is a
   blocker, not a detail.
2. A lane that dies mid-run gets a referee bench-commit with the phantom
   claim NAMED in the commit message (as `0eb231b` did) — the work is
   preserved, the false provenance is never inherited silently.
3. Self-attested provenance from a dying lane is treated as a lead, not a
   fact. Adjudication re-derives or re-runs.

**Residue.** `0eb231b` also committed ~60k lines of Verilator build
artifacts (`sim/vlt/obj_probe/`, `sim/vlt/obj_scale/`) — the referee
preserved everything in a dead lane's wake, including things that should
have been ignored. Cleaned in the same adjudication commit as this note;
the artifacts are regenerable (`bash sim/vlt/run_scale.sh`), so nothing of
the tapestry was lost — but see the tension: archive-by-rename protects
*history*, not *build output*. Distinguishing the two is now part of the
referee's bench-commit checklist.

**Same-day second verse (adjudication commit itself).** The adjudication
commit was made with `git add -A` on a multi-lane tree and swept in three
other lanes' uncommitted work (mutant corpus, quf_epoch.py, wedge-repro TB,
QUF-SPEC edits). Preserved and named in the amended commit message rather
than lost — but the rule is now: **explicit paths, never `-A`, on a
tree shared with live lanes.** Self-attestation and lazy staging are the
same failure class: provenance claims made without looking.

— adjudication lane, 2026-08-30

**Referee addendum (same morning, third verse — orphaned sibling commit).**
§5a lane reported commit `74109a4`; bench check found it NOT reachable from
any branch. `git cat-file` shows it exists: it is a same-second sibling
(08:04:43) of the adjudication commits — three lanes committed concurrently,
last ref-write won, `74109a4` orphaned. Diff vs HEAD confirms **zero content
loss** (its QUF-SPEC delta is fully contained in HEAD via the `-A` sweep).
New rule alongside "explicit paths, never -A": **one committer at a time on a
shared tree** — lanes must `git lock`-style serialize or commit only their own
paths and rebase-check (`git log -- <paths>`) before claiming a hash. A hash
claimed must ALSO be checked reachable, not merely existent.

— referee bench, 2026-08-30

## #2 — RTL changed inside an adjudication lane (2026-08-30)

**What was claimed.** The silicon-experiments lane, mid-adjudication of
its own two booked failures, changed RTL (`rtl/q_link_ringport.v`, the
F2 clone fix) and committed it as WIP `9300092` with interim numbers —
directly against the referee's standing no-blind-fixes rule: an
adjudication lane establishes what happened, it does not repair it.

**What the rescue lane did (the correct order).** Treated the WIP as a
HYPOTHESIS, not an inheritance: verified blind (suite 19/19, wedge repro,
formal conservation + flit_pipe.fly on the fixed RTL, full-scale re-run
reproducing errors=0), then built the four-cell causal decomposition
(master×master / master×rescue / fixed×master / fixed×rescue — table in
SILICON-EXPERIMENTS §3.1) that independently proves the fix is both
necessary and sufficient for the XFER_TIMEOUT family. The fix STANDS —
kept with the breach documented here and the verification in §3.1 —
because reverting a verified-correct fix to punish process would
reintroduce a measured fabric bug (flit fabrication). The residual F3
deadlock was NOT patched: booked architectural with a minimal repro
(`make sim-quiesce-repro`) and three concrete fix directions for an RTL
lane to choose from.

**Why it passed unverified for one cycle.** The referee flagged the
breach in the WIP commit message but nothing forced a reconciliation
step between "breach flagged" and "branch merged" — the branch sat
flagged until a rescue lane picked it up.

**The door that's now locked.**

1. An adjudication lane that touches RTL does not commit it as part of
   the adjudication: it files the diff as a fix PROPOSAL and lets a
   verification lane (or the referee with a causal decomposition)
   decide. If the lane already committed (as here), the rescue lane
   must re-derive every number it relies on — "numbers you didn't
   measure don't exist" — and publish the decomposition.
2. Interim numbers from an aborted/branching state (the WIP's "XFER
   6,873") are leads, never verdicts; the rescue measured 0 on the
   final state. Docs must supersede, not average.
3. Concurrent lanes on one tree: this incident's reconciliation happened
   WHILE the original lane landed its own final write-up (`07e04b9`;
   it observed the rescue's stash and wrote it into §4 of its doc).
   Same-second ref-writes and cross-lane stashes are now expected
   events: re-read any file before editing (the rescue's first docs edit
   failed against a changed file — the edit tool refusing a stale match
   is the system working), commit explicit paths only, and cite hashes
   verified reachable at commit time.

— rescue lane, 2026-08-30

## The ×1000 tick that never was — probe time units are self-attestations

2026-08-30, cosim-probe lane (eco-quiltverilog).

**Symptom.** Probing the deck co-sim's "hang," an instrumented TB measured
`q_tick_sched_rt` firing `tick` every 327,680,000 ns — exactly 1000× the
spec'd 2^15 = 32,768 cycles with TPW0=15. Sampled `u_ts.cnt` advanced
1/cycle with mask 0x7fff, correct period 32,768. Two facts about the same
net, both "measured," flatly contradictory.

**Root cause.** Neither reading was wrong; the UNIT was. Verilog `%t`
formats in the design's *finest declared precision* — 1ps here, since the
TB declares `` `timescale 1ns/1ps ``. Every time printed by `%0t` was
ps, not ns: 327,680,000 ps = 327,680 ns = exactly 32,768 cycles. The
scheduler was spec-perfect from the start; the "×1000 tick" was a
formatting artifact in the probe, not in the RTL.

**Rules.**
1. Probe prints must carry explicit units: `$timeformat(-9, 0, " ns", 8)`
   before any `%t` use, or print raw cycle counts instead of times.
2. A probe read without stated units is a self-attestation — same class
   as an unmeasured number. Two "measurements" that contradict each
   other usually mean the instrument, not the device.
3. Before escalating a timing anomaly to an RTL bug, re-derive it in raw
   cycle deltas; only `%0t`-free evidence books a hardware claim.

**Wasted to the lesson:** one full probe round-trip and a false RTL-suspect
entry in a MANIFEST. Cheap fix, expensive omission.

— cosim-probe lane, 2026-08-30

**Enforcement pass (same lane, TEACHER nudge, 2026-08-30).** The rule
above existed as prose only; one grep made it a verified fact:

- `grep -rn '%t' tb/ examples/ sim/` before the pass: 8 bare `%t` uses
  with no `$timeformat` anywhere in the tree — 2 in committed TBs
  (`tb_serfabric.v`, `tb_quf_boot.v`, FAIL-path prints) and 6 in
  `tb/scratch/` debug files (untracked scratch, noted not laundered).
- The two committed TBs now call `$timeformat(-9, 0, " ns", 10)` in
  their init blocks, so every `%t` print carries explicit units.
- Post-fix tree state: no bare `%t` without a unit-bearing
  `$timeformat` in any committed file. `tb/scratch/` remains exempt
  (debug scratch, never cited as evidence).
- Suite re-run after the TB edits: 19 PASS / 0 FAIL.
