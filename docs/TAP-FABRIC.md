# TAP-FABRIC — running the Tap's bar as a quilt cell graph

**Lane:** tap-fabric · **Date:** 2026-08-29
**Companions:** `DOCTRINE.md` (the bet), `QUF-SPEC.md` (the file), `FOUNDATION.md` (D1–D5), `SEMANTIC-TOWER.md` (L0→L1→L2), `BACK-DECK-APP.md` (the other worked application).
**Upstream:** `~/projects/the-tap` (the bar: `src/tap-room`, `src/tap-dynamics`, the JEPA paper `research/papers/paper-4-jepa-room-perception.md`), `~/projects/mud-arena` (the room engine: `src/mud_arena` command grammar + `EventBus`, `src/server.py` watch/tick wire formats).

> **The claim this document makes exact.** The Tap is already a cellular system wearing a bar's clothes. Every patron is a cell (a judgment over messages, a ledger that is their arc), the room itself is a cell whose dials are the room's mood board, and a round of conversation is a tick. What MudArena logs as text, the fabric logs as `qm_effect` flits. This document is the bridge: the bar compiled to the five verbs, the same QUF that loads into a testbench, a soft core, or silicon — and a prototype (`sim/tools/tapfabric.py`) that replays *real-format* MudArena session logs through RTL-exact cell semantics and hands back a tap-room QUF plus a rendered transcript.

---

## 1. The mapping

| Bar thing | Fabric thing | Organ (FOUNDATION D1) |
|---|---|---|
| a patron | a **cell** | `S` = dials + edges + accounts; `J` = taste (§3); `L` = their arc (§4); `τ` = the round; `δ` = hear/speak/cool |
| the room (the old man who built the place) | the **room cell**, a dial-aggregating cell | its `q_dialfile` row *is* the mood board (§2); its edge table is who's present |
| the elephant (walls with ears) | the **rhythm cell** | content-blind; warmth dial fed by message timestamps (§5) |
| who hears whom | **links** (edges owned by the *hearer*) | `qm_link` — "link before effect" is the RTL's own rule (unknown src drops silently) |
| a speech | `qm_effect` flit `{op, src, dst, …, dat=heat}` | a balanced transaction (D3): debit speaker `turns`, credit hearer `heard` |
| sitting down | `qm_bind` | set `cell_id` + the patron's taste dials |
| following someone into a conversation | `qm_link` | slot + bind-time base weight = affinity |
| a round of conversation passing | `qm_tick` | decay sweep (topics age, familiarity half-lives), buzz leak, fire test |
| butting in when you can't hold it | **fire** (emergent, from `qm_tick`) | `act ≥ THRESH ∧ REFR=0` → fanout effects to everyone you listen to |
| lurking | `qm_view` | bounded-freshness read; the transcript's only sanctioned peek |

Two ways a cell speaks, and the transcript keeps them distinct:

- **LOG-SPEAK** — exogenous speech from the replayed session (an IO-port injection, Law 4: the log is an adapter cell).
- **FIRE** — emergent speech: buzz accumulated from what was heard crosses the earnestness threshold inside `qm_tick`, exactly the RTL integrate-leak-fire path. Nobody scripted it; the room produced it.

### 1.1 Why edges are owned by the hearer

`q_cell_core.v` integrates an effect only when the flit's `src` matches a valid slot in *this* cell's edge table ("link before effect", ST_EFFT). So "who hears whom" is literally the hearer's edge table: you link the people you listen to. Fire fans out to a cell's *own* peers (etab), and the peer integrates only if it has an edge back — mutual hearing is required for a speech to land, which is also the sociological truth: a speech only lands on people who were listening. The room links every present patron (the old man carries the entire graph of the space in his head — in the fabric this is not a metaphor, it is his edge RAM). The elephant links everyone too, but never fires (§5).

Slot discipline: `EDGES_N = 8` stools per cell in the prototype; a full table evicts the lowest-weight edge (the coldest acquaintance). QUF carries the eviction forward — warm start restores exactly who you were listening to.

## 2. The dial overlay (mood board)

The physical dial map is `q_dialfile.v`'s, untouched (QUF-SPEC §6.1: the map is defined by the RTL; values are pre-saturated Q1.15). The Tap *names* a subset of it. Same registers, bar semantics — the L0 convention of SEMANTIC-TOWER §1, not a new file format.

| addr | physical dial | patron reading | room reading |
|---|---|---|---|
| 0 `ETA_F` | fast eta | — | **MOOD** (fast signed EMA of message heat) |
| 1 `ETA_S` | slow eta | — | — |
| 2 `KF` | fast shift | — | elephant: gap-EMA fast shift (§5) |
| 3 `KS` | slow shift | — | elephant: gap-EMA slow shift |
| 4 `KA` | leak shift | **attention decay** (buzz leak per round) | **volume decay** (crowd energy leak per round) |
| 5 `THRESH` | fire threshold | **EARNESTNESS** (heard-energy before you must speak) | **EARNESTNESS** (crowd energy before a room-moment: a toast, last call) |
| 6 `REFR` | refractory | min rounds between your own speeches | min rounds between room-moments |
| 7 `COS_MIN` | similarity floor | **OPENNESS** — the tolerance dial of J (§3), in feature-distance units | — |
| 8 `P0E` | log2(P0) | hyperbolic memory horizon (fame decays) | — |
| 9 `MODE` | engine select | familiarity engine: 0 = ladder (regulars: counts with half-life), 1 = hyperbolic (fame: big weight, slow decay) | — |
| 10 `HL` | half-life | how many rounds before familiarity ages one class | how long the room remembers a topic |
| 11–15 | v2 features | unused (0) — round-tripped, never read | — |

Cell state outside the dial file — `act` (the patron's **buzz** / the room's **VOLUME**) and `refr` — travels in QUF header KV (`tap.act`, `tap.refr`) under the extensibility rule (QUF-SPEC §8); SEMANTIC-TOWER §4.3 is exactly what that rule is for. The v1 RTL loader profile does not restore them (QUF-SPEC §9: warm start re-binds and re-trains) — the Python path is the full-state path, and the file says which one you're holding.

## 3. Judgment J = taste (D2 instantiated)

FOUNDATION D2: `J = (A, r)`, keyed answers `A ⊆ X × K`, tolerance dial `r`, verdict set `V(x)`, never guesses on `|V|>1`.

- **Input space** `X` = messages as integer feature pairs `(kind, bucket)` — kind ∈ {GREET, JOKE, STORY, QUESTION, GRIPE, MOVE, IDLE}, bucket = top 3 bits of the message's signed Q1.15 heat (0..7). No text crosses the judgment; the bridge renders heat deterministically from the log line (§6), integers only.
- **Metric** `d((k,b),(k′,b′)) = 3·[k≠k′] + |b−b′|` — city-block with a kind penalty. A pseudometric would carry aliases (regulars' nicknames); v1 keeps it a metric.
- **Keyed answers** `A` = the patron's taste, two keys fixed at bind: a *liked* kind with a heat center, and a *curious* key (questions, mid heat) — the pair that makes AMBIGUOUS reachable, as D2 requires.
- **Tolerance** `r` = dial 7, OPENNESS, whole units, bound with the rest of the taste at sit-down. Widening it trades missed messages for mislanded ones — the dial is the bet.

Verdict → effect integration (the RTL dat path):

| verdict | note | integration |
|---|---|---|
| ACCEPT | the key's class note ("warm-story", "good-question") | `act += sat((w·heat) ≫ 15)` — the message lands |
| REJECT | what bounced and why | `act += sat((w·(−|heat|≫1)) ≫ 15)` — off-taste loudness *cools* the room for this patron |
| AMBIGUOUS | both keys within r — no guess | no integration; ledger entry only |

The weight `w` is the post-update readback of the hearer's edge to the speaker (train-then-integrate, matching the RTL's ST_EFFT→ST_EFFR→ST_EFFI ordering).

## 4. Ledger = the patron's arc

Every op is booked (D3). A speech is one nonce, balanced:

```
qm_effect(speaker → hearer, heat):
  (speaker : turns , −1)      (hearer : heard , +1)
  hearer ledger += {nonce, src, verdict, note}     # the arc, in order
```

The rendered transcript's closing "arcs" section is the ledgers printed: what each patron accepted, rejected, stayed ambiguous on, spoke, and had left in buzz when the log ran out. The patron's arc *is* the ledger — no separate story of the evening exists.

## 5. The elephant — JEPA as a dial cell

Paper 4's thesis: the room's state *is* a prediction-error signal; prediction happens in latent space, never by reconstructing content — privacy by architecture. The elephant cell takes that literally:

- **Content-blind by construction.** Its J ignores kind and heat entirely. It receives every speech effect (it links everyone) and integrates nothing into buzz (its taste keys are never matched; effectively `dat→0` for act, ledger-only). What it keeps is *when*.
- **Predictor P.** An all-integer EMA over inter-message gaps measured in ticks (one log line = one tick; the MudArena CPU sim ticks at exactly 1 s/line, so tick count is the log's honest clock — the wire format carries no wall time). Fast/slow EMAs in 64ths of a tick, shifts on dials 2/3 (`KF`/`KS`): `e_f += ((gap≪6) − e_f) ≫ KF`.
- **Residual.** `ε = (gap≪6) − e_f`, booked in the ledger per message: predicted vs actual, the JEPA error vector reduced to the one dimension that matters at a bar — rhythm. `‖ε‖` small: the room is predictable, the evening has a pulse. `‖ε‖` large: something happened, direction unknown (paper 4's semantic-blindness caveat, kept honest: the elephant knows *that*, not *what*).
- **Warmth = ladder mass.** One edge (elephant → room), base 0. A message whose `|ε|` is inside the novelty window (dial 7) trains bucket 0 — steady rhythm keeps refilling the newest class faster than half-life ages it, and `qm_view(1)` (wsum) reads out as **warmth**: the accumulated, decaying evidence that the room has a rhythm. A burst, a fight, a silence: error spikes, no train, warmth bleeds through the ladder shifts. The elephant never fires (no reachable threshold, and fanout over an audience of one room that already heard everything would be noise); it is a listener with a dial.
- **Privacy.** The elephant's QUF state contains buckets, gaps in 64ths, and error magnitudes — nothing reconstructable into a sentence. Paper 4's no-decoder property, inherited by the file format.

## 6. Log formats (real MudArena shapes)

The bridge parses the three wire formats that actually exist in `~/projects/mud-arena`:

1. **Watch stream (NDJSON)** — `src/server.py` `_notify_watchers` / `watch_start`: `{"type": "agent_update"|"watch_start", "agent_id", "location", "action", "score"}` — one per line, exactly as the telnet/WS watch feed pushes them.
2. **Sim tick stream (NDJSON)** — `src/server.py` `_read_stdout` consumes the simulator's newline-delimited JSON: `{"agents": {aid: {"location", "action", "score"}}, …}`; the CPU fallback emits `"action": "move to <room>"` strings.
3. **Command lines (telnet)** — the `mud_arena/commands.py` grammar as typed at the telnet `> ` prompt: `go north`, `look`, `talk to guard`, `take key`, `use key with door`; NPC replies in the `_do_talk` shape `"<npc> says: '…'"`. Unprefixed command lines are attributed to the most recent `watch_start` agent, which is exactly how an interleaved telnet watch session reads.

**Fixture status, honestly:** `mud-arena` contains no `.log`/`.jsonl` session captures (checked — `find` over the repo finds none). `sim/fixtures/tap-session-01.jsonl` is therefore **synthesized**, but format-exact against the source above: watch payloads field-for-field, tick lines in the CPU-fallback shape, command lines in the parser's grammar, locations named from the Tap's own rooms (bar_rail, bridge_table, corner_booth), and the NPC line in the `_do_talk` mold. When a real capture exists it drops in unchanged — the parser never sees the difference, because there is none at the byte level it reads.

### 6.1 Log → ops

| log event | fabric ops |
|---|---|
| agent first seen (`watch_start` / first update) | `qm_bind` patron (cell_id, taste dials); room links patron; elephant links patron; patron links room |
| `move to X` / location change | co-present linking at the new spot (`qm_link` both ways, if stools) |
| `talk to X` / `X says: …` | `qm_effect` speak (LOG-SPEAK): effects to the room, the elephant, the target/mutual hearers; each hearer's edge to the speaker cofires (trains) |
| `look` | `qm_view` on the room (lurk) |
| score change | ledger account credit |
| each line, after its ops | one `qm_tick` round for every cell (the 1 s cadence) |

Heat is rendered deterministically from the action text: kind from keywords/verbs, signed Q1.15 magnitude from kind base ± per-word lexicon credits (warm words, cool words, question marks). No floats, no model calls — the same all-integer discipline the RTL demands (SEMANTIC-TOWER §5.3), and the transcript quotes the exact integer it used.

## 7. The prototype — `sim/tools/tapfabric.py`

Stdlib-only Python (≥3.8), reusing `tools/quf.py` structures (`build`, `read`, `verify_bytes`, `decode_sections`) for the file and mirroring the RTL bit-for-bit where the RTL defines behavior:

- **`q_hebb_edge` fidelity** — ladder: bucket-0 train saturating at 255 with sticky overflow; half-life shift (`hl_cnt+1 ≥ HL`); readout `Σ cᵢ·2^(K−i)` saturating at the PW boundary; `w = sat_u16(base + readout)`. Hyperbola: `wh++` on train; tick: `age+1 ≥ max(1, P0 ≫ 2·msb(wh))` → `wh−−` (the `[1,4)×` interval bound).
- **`q_cell_core` fidelity** — effect: `act = sclip16(act + ((u16 w × i16 dat) ≫ 15))`, train-before-integrate, unknown-src drop; tick: pre-leak fire test (`act ≥ THRESH ∧ refr=0`), fire uses the **pre-leak** act as `afire` then zeroes it, non-fire leaks `act −= act ≫ KA` and decrements `refr`; fire fans out to the cell's own valid peers.
- **Warmth, mood, volume** — per §5 and §2, all-integer.

Run it:

```
python3 sim/tools/tapfabric.py sim/fixtures/tap-session-01.jsonl --out /tmp/tap_room
# writes /tmp/tap_room.quf (verify with: python3 tools/quf.py verify /tmp/tap_room.quf)
#        /tmp/tap_room.transcript.txt
```

Output: the tap-room **QUF** (dials = the mood board, edges with live ladder buckets = who hears whom and how warmly, routing, tick schedule, plus `tap.*` provenance KVs), and a **rendered transcript** — every op annotated with which cell spoke, which cells heard, each verdict, act movements before→after, room VOLUME/MOOD, and the elephant's warmth trace. Fires are marked `FIRE` and are distinguishable from `SPEAK` (log-sourced). Tests: `python3 -m unittest discover -s sim/tools -p 'test_*.py'` (or `python3 sim/tools/test_tapfabric.py`): RTL invariants (fresh-cofire 256, ladder dyadic readout + half-life shifts, hyperbola interval bound, saturating integration, pre-leak fire test), D2 verdict behavior under the OPENNESS dial, all three log formats parse, the fixture replays with emergent fire, QUF verifies and round-trips warm state byte-exactly.

### 7.1 What the example actually does (`tap-session-01.jsonl`)

5 cells (the-tap=0, elephant=1, pearl, moss, heron), 16 edges, 45 ticks, 27 speeches. The graph produces, unscripted:

- **Every verdict kind.** moss: 8 ACCEPT / 7 REJECT / 1 AMBIGUOUS — the ambiguous one is a warm story landing within OPENNESS of both his keys, and the transcript shows his act *unchanged* (`0.0893->0.0893`): D2's "never guesses" as a visible number.
- **A fire cascade.** t043: moss's buzz (0.5737) crosses earnestness (0.4375) — he butts in. That speech pushes room VOLUME to 0.5745, over the room's own threshold (0.5625); t044: **the room fires** — last call for everybody, volume discharges to 0, refractory 3 rounds. Two ticks, nobody scripted either.
- **A warmth arc.** Elephant warmth 0.0078 → 0.1914 over 27 messages (22 steady-gap trains, 5 novelty breaks, final prediction error −24/64 tick).

## 8. Honest debts

- **Tick ordering is a simulation serial order** (cells tick in id order; fire fanouts land at the end of the round). The RTL ring interleaves delivery; the prototype picks one legal serialization, not the only one.
- **`act`/`refr` ride KV, not a section.** A v2 QUF section would be cleaner; extensibility KV was the zero-new-format move, and the RTL loader profile simply skips them.
- **The eviction policy** (coldest stool out) is a bridge policy, not RTL — the hardware would need an eviction FSM or bigger tables.
- **v2 features unused.** Echo gate, RQH bank: off. The graded-train path is exactly the hook a future "reply-window learning" would use (you only *learn* from a reply that lands inside your own echo trace) — specified in INNOVATION-JUDGEMENT, deliberately not simulated here.
- **The transcript's heat lexicon is tiny** and hand-tuned. That's the L0 edit set of the bridge; better taste belongs in dial values and key sets, not in more bridge code.

*The bar was already a cell graph; the fabric just gave it a file format. Last call is a tick.*
