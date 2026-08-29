# BACK-DECK-APP — the back deck pipeline as a QUF-warmable cell graph

2026-08-29. Companion to ai-writings paper 68 (*The Back Deck Papers*) and to
`SYNTHESIS.md` / `QUF-SPEC.md`. The fabric does not know what a salmon is; this
document is what the fabric *hosts*: the dictated F/V EILEEN back-deck camera
pipeline (Casey's spec, quotes his) expressed as cells, links, and dials — the
same five opcodes, warm from one QUF file.

---

## 1. What the application layer is (and is not)

The Back Deck application is a **cell graph above the silicon**, not a second
fabric. Every object in it is a cell; every touch is an opcode; every knob is a
dial; the whole graph's state travels in one QUF (dials image + edges + routing
+ tick schedule). No object in the graph is a "service," a "job," or a "queue."
The vocabulary it adds — constraint-cells, alias-tables, match-cells,
count-cells, ledger-cells, cron-cells, A/B-cells, audit-cells — is wiring
convention on top of the v1 cell, not new silicon. Paper 68 §4 defines each.

Ground rule, from the dictation: *"The ML gets as good as the human crew
because the crew's own sorting IS the label."* The graph below is the net that
catches the crew's existing sorting behavior and turns it into labels, records,
and nightly self-improvement. Nobody on the deck does anything they were not
already doing.

## 2. The cell graph

Application cells, their fabric role, and the ingress they own (Law 4: any IO
can enter a cell; adapters are thin and dumb).

| Cell | Kind | Ingress | Egress (what it emits) |
|---|---|---|---|
| `CAM-UW`   | adapter cell | underwater camera stream | leave-frame events `{t, frame-features}` |
| `CAM-DECK-P/H/SF/SA` | adapter cells | deck cameras over tote volumes + gear column + scale | surface-break events `{t, features}`, landing events, hook-column frames, dial frames |
| `TOTE-PORT`, `TOTE-HOLD`, `TOTE-STBD-F`, `TOTE-STBD-A` | **constraint-cells** | landing events from their deck camera | ground-truth species ID as a hard rule: port→pink, hold→chum, SF→king, SA→coho |
| `ALIAS`    | **alias-table cell** | overheard deck-conversation transcript | canonical ID: pink≡humpy, chum≡dog≡keta, king≡chinook, coho≡silver — *"aliases are data"* |
| `XID-MATCH` | **match-cell** | leave-frame(t) + surface-break(t) | same-fish verdict inside the window; `AMBIGUOUS` flag when >1 candidate — never a guess |
| `HOOK-COUNT` | **count-cell** | hook-column frames | cannonball depth = hooks-visible × 1.5 fathoms (gear is 30 hooks) — labeled depth *without* the underwater camera |
| `SOUNDER`  | model cell | echogram frames + labeled depth pairs | biomass/depth inference; the cell the night improves |
| `LEDGER-SCALE` | **ledger-cell** | CAM-SCALE dial frames | `{t, weight, species-from-tote}` tuples — *"nobody keeps records; the camera keeps them"* |
| `BESTSHOT` | review-surface cell | every fish's footage chain | essential frames + one best-shot per fish |
| `AUDIT-CAPTAIN` | **audit-cell** | BESTSHOT output, wheelhouse UI | confirm / **quarantine** (quarantine propagates back down the label chain it came from) |
| `NIGHT-CRON` | **cron-cell** | tick schedule (see §5) | nightly retrain trigger; promotion verdicts from `AB-PROMOTE` |
| `AB-PROMOTE` | **A/B-cell** | NIGHT-CRON candidates + next-day feedback cells | incumbent/challenger dial writes via `qm_bind`; rollback is the default verdict |

Honest v1 note: the v1 fabric is a 4-cell ring with `q_cell` cores. The
application graph above runs the same opcodes on soft/agent-tier cells
(Cowboy Doctrine: *the tier says how much of the model is expressed; the
opcodes are the same on every boat*). The graph is QUF-portable across tiers —
that is the whole point of state-is-a-file.

## 3. The links (`qm_link` topology)

Composition is wiring, not scheduling. Links (src → dst, what flows):

```
CAM-UW ──────────────▶ XID-MATCH          leave-frame(t)
CAM-DECK-* ──────────▶ XID-MATCH          surface-break(t)
CAM-DECK-P ──────────▶ TOTE-PORT          landing events      ─┐
CAM-DECK-H ──────────▶ TOTE-HOLD          landing events       │ constraint-cells:
CAM-DECK-SF ─────────▶ TOTE-STBD-F        landing events       │ rules, not classifiers
CAM-DECK-SA ─────────▶ TOTE-STBD-A        landing events      ─┘
TOTE-* ──────────────▶ ALIAS              raw IDs in, canonical IDs out (both directions: overheard name → tote volume ID corroborates new alias rows)
TOTE-* ──────────────▶ XID-MATCH          species label, propagates BACKWARD to the underwater sighting once matched
XID-MATCH ───────────▶ CAM-UW label port  retro-labeled underwater sightings (quarantine propagates the same way)
CAM-DECK-* ──────────▶ HOOK-COUNT         hook-column frames
HOOK-COUNT ──────────▶ SOUNDER            labeled (echogram, depth) pairs — the link that frees the sounder from the underwater camera
SOUNDER/NMEA ────────▶ SOUNDER            echogram ingress (external)
CAM-SCALE ───────────▶ LEDGER-SCALE       dial frames; LEDGER joins species via the tote label bus
TOTE-*/XID-MATCH ────▶ BESTSHOT           per-fish footage chains + labels
BESTSHOT ────────────▶ AUDIT-CAPTAIN      the flip-through pile
AUDIT-CAPTAIN ───────▶ NIGHT-CRON         quarantine list (excluded from tonight's training set)
NIGHT-CRON ──────────▶ SOUNDER (challenger instance)   retrain on the day's labels
AB-PROMOTE ──────────▶ SOUNDER            dial writes = model swap (§4)
```

The label bus (TOTE-* outputs) is the graph's spine: it feeds XID-MATCH
(retro-labeling), LEDGER-SCALE (weight joins), BESTSHOT (review), and — one day
later, through the A/B gate — the SOUNDER's next challenger. One gesture, four
consumers.

## 4. The dials the A/B night-cron turns

All config travels as traffic (Law 2): every dial write below is a `qm_bind`
flit, so a promotion is traffic, not a reboot. Two dial tiers:

**Fabric dials** (v1 `q_dialfile` map, addresses 0–10) — what the challenger's
instance carries differently than the incumbent, and what `AB-PROMOTE` writes
on promotion:

| Dial | Addr | A/B meaning |
|---|---|---|
| `ETA_F` / `ETA_S` | 0 / 1 | fast/slow learning rates: tonight's retrain pace vs. incumbent's |
| `MODE` | 9 | decay law select (ladder vs. hyperbola) — challenger may train under a different forgetting law |
| `HL` | 10 | half-life: how much of last week's data tonight's model keeps |
| `P0E` | 8 | hyperbolic engine's P₀ — the same knob, other law |
| `THRESH` | 5 | fire threshold: the incumbent/challenger difference that decides a visible verdict on tomorrow's feedback |

**Application dials** (reserved slots 11–15, round-tripped by QUF, currently
free per `QUF-SPEC.md` §6.1 — this is what they are *for*):

| Proposed key | Addr | Meaning |
|---|---|---|
| `MATCH_WIN` | 11 | XID-MATCH window width — the lost-label vs crossed-label bet (paper 68 §6.2) |
| `HOOK_PITCH` | 12 | fathoms per hook (1.5) — count-cell calibration; re-zeroed when gear is re-rigged |
| `PROMOTE_MARGIN` | 13 | how much the challenger must beat the incumbent by on next-day feedback cells before promotion; rollback default |
| `QUARANTINE` | 14 | audit verdict weight: how strongly captain disagreement excludes a label chain from tonight's set |
| `LEGAL_SET` | 15 | this opening's legal species mask (e.g. pinks+chums only) — drives when AUDIT-CAPTAIN demands the flip-through |

Promotion semantics: the challenger is a warm QUF (its own dials image + edge
set). `NIGHT-CRON` binds it beside the incumbent overnight; both observe the
next day's label bus; `AB-PROMOTE` writes the winner's dials into the live
`SOUNDER` cell. Rollback is the null action — if the verdict does not clear
`PROMOTE_MARGIN`, nothing is written. *"No Wesley-iteration babysitting; the
system improves itself on schedule."*

## 5. Night-cron as the tick

*"The computer has the boat to itself at night."* The cron-cell is the ticks
section of the QUF made semantic: `tpw` sets the period, the phase word sets
when in the cycle the retrain epoch lands. The tick is a hardware-interlocked
deadline (SYNTHESIS Q2: `tick_pend` is serviced before any new ingress — it
cannot be starved by daytime traffic, however saturated). That property is
what makes the phrase *on schedule* literal rather than aspirational: the
day's effect storms cannot eat the night's improvement epoch. Autotrain does
not need an agent to remember it; the fabric guarantees the deadline.

## 6. QUF-warm start, honestly

Warm start = `rtl/q_uf_loader.v` eats the graph's QUF: dials restored word for
word (every dial above, fabric + application slots), edges/topology restored
(§3's links re-bound), tick schedule restored (§5). v1 honesty, per QUF-SPEC
§9: the RTL loader consumes but does not restore walk state (ladder buckets,
`wh`/`age`) — a warm-started graph re-binds and **trains the ladders back**.
For this application that is not a limitation but the doctrine: the ladder's
retraining data is the day's own label stream, replayed. The system warm-starts
topology + dials + schedule, then earns its weights back from the catch — the
same A/B discipline the night cron enforces, applied to bring-up itself.

## 7. What is real today vs. what is convention

Real and verified: the cell core, dialfile, edge engines, ring, tick deadline,
QUF reader/writer, loader (SYNTHESIS acceptance gate). Convention (this doc,
hosted, not silicon): the application cell kinds, the label-bus wiring, dial
slots 11–15 semantics, audit/BESTSHOT surfaces. Nothing here requires a fabric
change; everything here is expressible today as `qm_bind`/`qm_link` traffic
plus agent-tier cells on soft instances. When the v1 acceptance gate says
*load QUF → tick → a dial moves and an edge strengthens* — the back deck is
that demo, with fish: load the graph → one day of crew sorting → the
SOUNDER's edges strengthen → night ticks improve it → the A/B gate decides.
