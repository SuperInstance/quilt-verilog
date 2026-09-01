# COSIM SCALE-UP lane — live status (relaunch #5)

Branch: `cosim-scaleup` (private worktree `/home/eileen/projects/quilt-cosim-wt`).
Harness lineage: 5d9d848 (NCELL param) -> fb60056 (phase-1 proof) -> 8c8f846 (cell A)
-> 866782f (G4 digest patch).

## Evidence so far (all committed)

| cell | NCELL | seed | progs | result | commit |
|------|-------|------|-------|--------|--------|
| phase-1 re-proof | 4 | 0xFAB41C | 8d+12r | 20/20 bit-exact, 837 egress, 14dec+6bud | fb60056 |
| A pinned continuity | 8 | 0xFAB41C | 8d+12r | 20/20 bit-exact, 790 egress, 14dec+6bud | 8c8f846 |
| digest non-perturbation | 4 | 0xFAB41C | 8d+12r | 20/20 bit-exact, 837 egress (patched harness) | 866782f |
| B fresh 3x | 8 | 0x5EEDC0DE | 8d+36r | RUNNING | — |
| D fresh 3x | 4 | 0x0D15EA5E | 8d+36r | RUNNING | — |
| C fresh 3x | 8 | 0xBA5EBA11 | 8d+36r | queued after B/D | — |

## G4 digest (WORLD-CLASS-GAP.md port) — DONE, commit 866782f
Two-level commutative chain (leaf FNV-1a over 7 flit fields; window = sum
mod 2^32; root = FNV chain over window digests). TB emits additive D/R
lines; Python mirrors exactly; diff() self-checks TB D-vs-E, compares
model roots, bisects first divergent window. Vacuity-tested on a
doctored E-line. Per-program roots now in every log line (OK lines).

## Ops notes for relaunch #6 (if this lane dies)
- SHARED-WORKTREE HAZARD: at 22:06 the G3 lane checked out `g3-kinduction`
  in the shared repo while phase-1 sims ran. Worktree contents were
  identical (their branch sat at 5d9d848) so no harm — but my first commit
  landed on THEIR branch by accident. Fixed via temp-index plumbing +
  `git update-ref` (no shared-state touch). REMEDY (in place): this lane
  now works ONLY in private worktree `../quilt-cosim-wt`. Any lane touching
  this repo should do the same. The accidental duplicate commit 54aebe6
  remains on g3-kinduction (additive, left in place — never rewrite).
- `git add` under `tb/scratch/` needs `-f` (.gitignore covers the dir;
  tracked files there are precedent).
- Canonical logs: `tb/scratch/cosim-scaleup/` (tracked); raw run dirs
  `tb/run/cosim-<pid>/` are ignored scratch.
- Run wall-times: NCELL=4 20-prog battery ~1 min idle (7 min under another
  lane's checkout churn). Expect NCELL=8 44-prog cells ~5-15 min each.

## Still to do
- Cells B/C/D completion + per-cell commits
- Full batteries: tb/run_suite.sh + tools/backend/run_all.sh (private
  worktree) must be ALL PASS on final harness
- THE-BREAKDOWN / BACKEND-NOTES §10 update if counts justify (they will if
  B/C/D are clean: NCELL=8 with 3x fresh-seed volume)
