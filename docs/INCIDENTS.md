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

— adjudication lane, 2026-08-30
