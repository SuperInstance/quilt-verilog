# CULTURE-DEEP-DIVE — what computing's cultures teach the semantic-tower compiler

**Lane:** culture-deep-dive (Flash, extensive) · **Date:** 2026-08-29
**Companions:** `FOUNDATION.md` (the formal twin — D1–D5; this document is its
*cultural* twin and deliberately repeats none of its math), `SYNTHESIS.md`
(v1 mechanisms), `QUF-SPEC.md` (the state-is-a-file doctrine), `ABSTRACTION-MATH.md`
(formal object map), `BACK-DECK-APP.md` (the running example).
**Method:** web sweep (PLATO/TUTOR archives, interactive-fiction history, demoscene,
digital-twin literature, robot-simulator docs) + repo survey of the SuperInstance
quilt fleet under `/home/eileen/projects/`.

> **The one buildable idea, in two lines.** Every era of computing that felt
> *alive* — PLATO's teachers, Zork's parser, the demoscene's 4k intros — got its
> life from the same move: **judgment with tolerance, feedback within the frame,
> and content made by the users, not the implementers.** The semantic-tower
> compiler's job is to make those three properties compile-time guarantees:
> tolerance dials are state (D2), every op answers within a bounded number of
> cycles (Q1/Q2), and the top of the tower is an authoring surface, not a
> deployment pipeline — `@create` at runtime, the MUD builder's godhood, as a
> compiler front-end.

---

## Part I — the cultures, era by era

Four eras, each with a culture, a set of needs/desires that shaped the tech, and
a column of design lessons for the compiler. The per-era lesson tables feed the
consolidated table in Part II.

---

### 1. PLATO (1960–2006) — the teachers wrote the judgment, the students wrote the culture

**The setting.** PLATO (Programmed Logic for Automatic Teaching Operations) ran
from 1960 at the University of Illinois (ILLIAC I → CDC 6000/Cyber), grew to
several thousand plasma-panel terminals worldwide by the late 1970s, and the last
production system ran until 2006. PLATO IV terminals were ~$12,000 each; CDC
charged ~$50/hour for access; courseware cost CDC ~$300,000 per delivery hour to
develop (CERL did it far cheaper). External evaluation found PLATO "essentially
equal to an average human teacher" on advancement — **and everyone enjoyed using
it.** That sentence is the era in miniature: the product was not instruction, it
was *presence*.

**The teachers.** Courseware authors were mostly faculty and graduate students —
biology grad student Paul Tenczar designed TUTOR (1967); 25 music faculty and 40+
grad students built music courseware; the medical school built self-testing
systems. By the end there were 12,000+ contact hours of courseware. Key cultural
facts: authors were *domain people, not programmers*; the language had to make
judging easy; when TUTOR changed, the maintainers ran conversion software over the
entire online corpus of lessons — **whole-ecosystem refactoring as routine.**

**The students.** Students answered free text and got instant, contextual
feedback; they also played games (dnd, Empire, Avatar, Spasim, Airfight — the
FPS and the MUD and the flight-sim lineages all start here), made the first
emojis (Bruce Parello, 1972), and turned the system into a community that lasted
20+ years. Gameplay got so popular that "The Enforcer" — a background process —
was written to regulate/disable games at certain sites and times. Moderation and
joy arrived on the same system, as software.

**The judge (the heart of the era).** TUTOR's *Answer Judging Machinery* (~25
commands) judged free-text answers with tolerance:

- `arrow` opens a **judging block** — a backtracking loop that re-prompts (▷)
  until a correct answer lets progress continue; feedback from a wrong attempt is
  *erased* before the next attempt.
- `answer`/`wrong` patterns mix optional words `<it, is, a>`, required choices
  `(right, rt)`, and alternatives `(triangle, triangular)` — "it is a right
  triangle", "it's a triangular figure", and "rt triangle" all pass.
- **Spelling tolerance is built in**: "triangel"/"triangl" match. Words are
  converted to 60/64-bit bit-vectors (letter presence, letter-pair presence,
  first letter); the popcount of the XOR approximates phonetic distance. The
  author tunes pedantry with the `specs` command — **tolerance is a dial, set per
  lesson, per answer.**
- The `compute` command compiles the student's typed *expression* and checks
  numeric equivalence within roundoff — "32.4" is fine for "32.2". TUTOR's
  floating-point `x = y` was defined as *approximately equal*: the tolerance was
  in the language's bones.
- `join` — textual-substitution subroutine calls — could split a judging block
  across units: judgment composes.

**The notes-files (the first social media — dig here).** David Woolley's
PLATO Notes (1973) was one of the world's first online message boards, direct
progenitor of Lotus Notes and the newsgroup. Around it: Pad (1973), Talkomatic
(1973, five live participants + unlimited spectators), Term-talk (1973, the
precursor to IM), Personal Notes (1974, email), Monitor Mode (1974, screen
sharing — instructors watching/helping students). But the *culture* is the
lesson, not the feature list:

- **Users wrote the content.** Political-science student Valarie Lamont built
  *Boneyard Creek*, a narrative about a polluted stream where users commented and
  gave feedback — a citizen-science cell graph, 1973. Stuart Umpleby built
  *DELPHI*, structured community deliberation: users shared opinions, rated their
  importance, and gave probabilities of outcomes — **a judgment-with-tolerance
  aggregation engine, 20 years before groupware.**
- **The community policed itself and was policed.** A Watergate discussion group
  was killed under threat of NSF-funding loss; women users faced harassment. The
  moderation problem is not new — PLATO shipped it.
- **The terminal was a lifeline, not a toy.** At Madadeni College in kwaZulu
  (South Africa) — no classroom electricity, one crank telephone for the whole
  college — 16 PLATO terminals in an air-conditioned room were sometimes the
  *only* way to communicate with the outside world, via term-talk.

**What the needs/desires were.** Teachers wanted to teach *many* students with
feedback that felt individual — without grading essays by hand. Students wanted
to be seen, to talk, to play. The hardware forced it: 1260 baud, 60-bit words,
150-variable private data segments, 1500 shared 60-bit variables per game. The
economics forced it: at $50/hour you had better judge the answer on the first
try, with tolerance, or the student feels robbed.

#### PLATO → design lessons

| Culture fact | The need behind it | Design lesson for the semantic-tower compiler |
|---|---|---|
| `answer (right, rt) (triangle, triangular)`; "triangel" matches | Teachers wanted *similar-not-identical*, tuned per question | Judgment = (keyed answers, tolerance dial) as **state**, not code (FOUNDATION D2). The compiler's pattern grammar must ship optional/required/alternative word classes and a per-answer pedantry dial — `specs` is a compile-time directive. |
| `compute` checks numeric equivalence within roundoff | Math answers are expressions, not strings | The compiler needs an **expression-evaluating judge** — lower the student's formula, run it, compare within ε. Verdicts: ACCEPT/REJECT/**AMBIGUOUS** — never guess (D2 property 3). |
| Judging block erases feedback on retry | Students should re-attempt without clutter | **Attempts are first-class state**: per-attempt feedback, rollback of effect, bounded retry budget. The compiler should emit attempt-counting into cell state, not just a score. |
| `specs` command tunes spelling pedantry | One pedantry level never fits all | Tolerance dials belong at *every* tower level (spelling → synonym → paraphrase → numeric), each independently settable. AMBIGUOUS must surface the verdict *set*, not a score. |
| Notes-files, DELPHI, Boneyard Creek | Users wanted to publish, deliberate, aggregate | **Content is user-authored cells.** The top of the tower is an authoring surface: notes = cells with comment edges; DELPHI = cells whose judgment aggregates weighted opinions; moderation = a background cell ("The Enforcer" as a first-class process). |
| Whole-corpus conversion when TUTOR changed | Language evolution must not strand lessons | The compiler must be able to **recompile the entire corpus** — all lessons/sheets/QUFs migrate together. Versioned IR + codemod passes are compiler features, not ops. |
| $50/hour, $12k terminals, "equal to a human teacher but everyone enjoyed it" | Cost forced first-try tolerance; enjoyment was the real product | Latency and tolerance are the product. The compiler's acceptance gate should optimize *judgment quality per cycle*, and the fabric's responsiveness is a feature, not an implementation detail. |
| The Enforcer | Institutions wanted governance as software | Regulation is a cell with its own opcodes — revocable, forgettable (cf. quilt-mhs `FORGET` as safety teardown). |

---

### 2. MUDs & Zork (1976–1990s) — text worlds made alive by tolerance, telemetry, and improvisation

**The lineage.** Colossal Cave Adventure (1976, Crowther/Woods) → Zork (1977–79,
MIT Dynamic Modelling Group: Anderson, Blank, Daniels, Lebling — MDL, PDP-10) →
Infocom's Z-machine (1979–80) → MUD1 (1978, Roy Trubshaw/Richard Bartle, Essex,
named after the Fortran Zork port *DUNGEN*). Avatar (1978, PLATO, 60 players)
ran in parallel. Zork I–III sold 680,000+ copies through 1986; the Library of
Congress put Zork in its 2007 game canon; Microsoft open-sourced Zork I–III in
November 2025.

**What made text worlds feel alive.** Four things, and each is a compiler lesson:

**a) Parser tolerance — the interface was a judgment, not a menu.** Zork's parser
was the "Dungeon Master": it accepted "put the lamp and sword in the case",
synonyms, abbreviations. Its responses were *sarcastic and opinionated on
purpose* — the implementers' design note is that sarcasm both made the machine
feel human **and trained the player to write commands the parser could parse**
(feedback loop: human adapts to machine, machine adapts to human). Marc Blank
wrote "40 or 50" iterations of the parser. The `answer`/`wrong` word-class
grammar of TUTOR and the synonym tables of Infocom are the same technology:
*an alias table is a zero-distance equivalence class* (FOUNDATION D2, the
pseudometric).

**b) "Guess the verb" as community folklore.** Every early player knows the
rituals: type `xyzzy` in every room (from Adventure's magic word; in Zork it
always answered "Nothing happens" — and players kept trying, in every game, for
decades). The beloved Zork I typo **"You can't get ye flask"** was kept in every
re-release. "Frob" became the canonical unknown-word test. Infocom shipped
*InvisiClues* hint booklets and feelies. The folklore is the point: **parser
failure became shared culture** — the community's map of what the parser accepts
was passed mouth-to-mouth, and games deliberately seeded it. The parser's
rejections were as much content as its descriptions.

**c) Player improvisation as content.** Zork's implementers added a **command
transcript feature to log commands players tried unsuccessfully** — failed-input
telemetry mined to improve the parser. Players suggested puzzles; a community
mailing list distributed updates. In MUDs this went all the way: Bartle's MUD1
made the *database* the world — wizards, points, a persona communication system —
and students at Essex wrote entire worlds in MUDDL (Mist, Rock, Blud, Uni). The
builder-immortal with `@create` godhood became the genre's core power fantasy
(The Tap's Builder System is this mapped onto LLM agents — see Part III).

**d) A machine for portability, not rewrites.** To get Zork off the PDP-10, Blank
and Berez invented the **Z-machine**: games compiled from ZIL to a bytecode for a
fictional computer; each microcomputer (Apple II, C64, Atari 8-bit, CP/M, IBM PC)
only needed a thin interpreter. One game, N interpreters. This is the direct
ancestor of the QUF doctrine — *state is a file; the same bytes run anywhere* —
and of the `.qm` mint-to-metal chain (Part III). It is also the origin of the
word "Dungeon": Zork was renamed for distribution, the Fortran port leaked as
DUNGEN, and MUD1 took its name from that — **portability accidents became
lineage.**

**The constraints.** Zork lived in one megabyte of PDP-10 memory and literally
ran out of space — the last puzzles were added in February 1979 because the team
"had run out of space". MUD1 was rewritten in BCPL to "conserve memory and make
the program easier to maintain". Essex allowed outside MUD access only 2am–7am
over BT's Packet Switch Stream. Zork III's earthquake fires after ~130 moves — a
global clock. Text worlds were alive *within* brutal budgets; the budget was the
aesthetic.

#### MUD/Zork → design lessons

| Culture fact | The need behind it | Design lesson for the semantic-tower compiler |
|---|---|---|
| "Guess the verb" folklore; `xyzzy` → "Nothing happens" | Players needed a shared way to probe the parser's world-model | REJECT is a *social* signal: the compiler must make rejection feedback witty, consistent, and part of the artifact's identity. Verdicts must be deterministic so folklore can form around them. |
| Command transcript of failed inputs | The implementers mined what players tried | **Failed-input telemetry is the compiler's training set.** The fabric should log REJECT/AMBIGUOUS verdicts (with input, context, dial settings) as first-class data — the input side of a quilt-evolve loop (Part III). |
| Parser sarcasm trained the user | The machine and human must co-adapt | The compiler should emit *feedback text* as part of the judged cell's contract — the rejection message is a dial too, and it trains the user toward parseable input. |
| "40 or 50" parser iterations; `answer` word-classes | Understanding is an iterative craft | Synonym tables and word-class grammars are compile-time data, not runtime code. Ship a default alias lexicon (MUD-arena's `parse_command` folding is a working example) and let every cell override it. |
| Player-built worlds; wizard godhood; `@create` | The most durable content was user-authored | **Content creation is a runtime op, not a build-time event.** The tower's top level must lower *authoring* (rooms, items, bridges, rituals) as cell creation with grants — the builder-immortal is the compiler's front-end persona. |
| Z-machine: compile once, interpret everywhere | Portability across many cheap machines | The compiler's middle end emits a portable IR (QUF); targets are thin loaders/interpreters. Verification = the same IR producing bit-identical behavior on every target. |
| Zork's 1MB; MUD1's BCPL rewrite; 2am–7am windows | Budgets were the aesthetic | Budgets are compiler inputs: byte budgets, RAM budgets, contact-hour budgets. The compiler reports per-cell cost and refuses to lower a sheet that breaks the target's budget (demoscene rule, next era). |
| Zork III's earthquake at move ~130 | Time itself can be a puzzle | A global clock is just a cell with a tick schedule. The compiler must let authors bind semantics to tick counts — deadlines as first-class (SYNTHESIS Q2). |

---

### 3. Old-school game code (1978–2000s) — discipline as feel: instant reactions, fixed timestep, frame budget, and the demoscene's constraint worship

**The discipline.** Four interlocking practices made games *feel* alive, and they
are all compiler-shaped:

**a) Instant reactions.** Arcade and console games optimized for input-to-effect
latency measured in frames. Nintendo's platformers gave the player a
within-a-frame response window, coyote time, input buffering — *forgiveness is
feel*. The 2012 "juice" canon (Juice It or Lose It) is the same claim: feedback
within the frame is the product. Space Invaders (1978) is the cautionary tale in
the other direction: the game speeds up as invaders die because the CPU (an 8080
at 2MHz) has more free cycles per frame — **variable timestep as emergent
difficulty**; the game loop *was* the difficulty curve, by accident.

**b) Fixed timestep.** Determinism demands fixed ticks. Vanilla Doom runs its
simulation at exactly 35Hz and its demo system is a deterministic replay of
inputs; fighting games publish frame data at 60Hz and rollback netcode (GGPO)
depends on bit-exact determinism; Age of Empires ran deterministic lockstep
across machines. Glenn Fiedler's canonical "Fix Your Timestep" (2004) names the
rule: variable dt → unstable, non-deterministic physics; fixed dt + accumulator +
interpolation is the cure. **Determinism is not a nice-to-have; it is what makes
replays, demos, and networked play trustworthy.** The quilt fabric already took
this bet: ticks are deadlines, local clocks, commit boundaries (FOUNDATION §0);
"clock is its own traffic" (ABSTRACTION-MATH, endochrony).

**c) Frame budget.** A 60fps game has 16.7ms per frame, and the frame budget is a
published, per-subsystem accounting: AI gets 2ms, physics 3ms, rendering the
rest; if the AI blows its budget the frame misses and the game stutters. The NES
ran a 1.79MHz 6502 with 2KB of RAM, 8 sprites per scanline, and a vblank NMI as
the heartbeat — the whole console was a fixed-timestep machine with a hardware
interrupt as its tick. Budgets were *measured*, and the measure was the
discipline.

**d) The demoscene's constraint worship.** The demoscene (born from cracktros,
~1986) turned constraints into identity: the 4k intro (4096 bytes) and 64k intro
(65536 bytes) are competition categories where the executable *size* is the
canvas. Farbrausch's *kkrieger* (2004) is a fully playable FPS in 96KB — every
texture and mesh generated procedurally at load. Future Crew's *Second Reality*
(1993) made a 486 sing. The scene's rules are cultural: creativity over ripping,
effort over asking, "elite" vs "lamer", groups of coder/musician/graphician/
swapper, compos judged by peers at parties (Assembly, Breakpoint, Revision).
Finland put the demoscene on its UNESCO intangible-heritage list in 2020 — the
first digital subculture so honored. The ethos: **the constraint is not the
enemy; it is the generative pressure that makes the work recognizable.** "Make a
device do more than was intended in its original design" — a 6502, 4KB of RAM,
and a raster interrupt were a *voice*.

**Why this matters for a compiler.** Games and demos are the purest existing
proof that *bounded latency, deterministic ticks, and hard budgets are
compile-time contracts, not runtime aspirations*. The quilt-verilog doctrine is
already demoscene-shaped (quantized-by-default, zero vendor deps, 5k-LUT iCE40
to the biggest fabric) — this era gives it its engineering spine.

#### Game-code → design lessons

| Culture fact | The need behind it | Design lesson for the semantic-tower compiler |
|---|---|---|
| Space Invaders speeds up as aliens die | Variable timestep produced emergent behavior | The compiler must **forbid variable-timestep semantics at the cell level**: every op is bounded (`MAX_OP_CYCLES`), ticks are deadlines. Emergent difficulty is a dial (tick-schedule state), not an accident. |
| Doom 35Hz demos; GGPO rollback; AoE lockstep | Trust requires bit-exact determinism | Determinism is a compile-time guarantee: fixed-point everywhere, no float escape hatch (DOCTRINE 2), one interpreter per cell, commit boundaries per event. The compiler emits determinism tests (same QUF, same ticks → same state). |
| Frame budget accounting (AI 2ms, physics 3ms, ...) | Missed frames are felt as stutter | The compiler emits **per-cell budget reports** (cycles per op, LUTs, RAM) and refuses sheets that exceed the target fabric's frame budget. Budgets are part of the sheet contract, like a type. |
| 1-frame response; coyote time; input buffering | Forgiveness is feel | Latency bounds are verified properties: a `qm_view` answers within (queued flits × `MAX_OP_CYCLES` + ring latency) even under an effect storm (SYNTHESIS I2). The TBs assert it; the compiler should too. |
| 4k/64k intros; kkrieger's 96KB FPS | Constraint is identity and generative | **The quantization IS the algorithm** (DOCTRINE 2). The compiler should offer "intro categories": target fabric + byte/RAM/LUT budget as a first-class compile configuration, and celebrate what fits. |
| Compos; peer judging; elite/lamer | The scene is a judging culture | The compiler's competition loop (quilt-verilog's proposals/) is the demoscene compo: neutral-seat judges, published criteria, cross-review. Keep the judging honest — "mechanisms not paragraphs" (SYNTHESIS). |

---

### 4. Digital twins (1969–today) — fidelity is bought with complexity

**The literature, briefly.** The *concept* predates the name: NASA's Apollo
simulators (1969–70) were the first (unlabeled) digital twins — the Apollo 13
oxygen-tank failure was evaluated on simulators. Gelernter's *Mirror Worlds*
(1991) named the dream; Digital City Kyoto (1998) wired live sensor feeds into a
3D city. NASA's 2010 definition made it practical: a digital twin continuously
uses real data from its physical counterpart to stay synchronized — a model
without that data link is (per the strict definition) just a simulation, and
critics warn that the label is becoming a buzzword. The standard anatomy: a
physical object, a digital representation, and the *digital thread* between
them. The classification that matters: **Digital Shadow** (data flows one way,
physical → digital) vs **Digital Twin** (bidirectional — the twin can command
the asset) — and the lifecycle split **DTP** (prototype, pre-build) / **DTI**
(per-instance, in service) / **DTA** (aggregate across a fleet, for prognostics
and design feedback). The DoD's definition is the maximalist one: "an integrated
multiphysics, multiscale, probabilistic simulation of an as-built system,
enabled by a Digital Thread." Virtual commissioning — simulating a production
line to find bottlenecks before any physical equipment is installed — is the
industrial flagship use.

**Where game-engine/robot-twin co-simulation actually lives today** — and what it
costs:

| Simulator | Physics/model | Where the complexity hides | Cost in complexity |
|---|---|---|---|
| **NVIDIA Isaac Sim** | PhysX or Newton on USD scenes; RTX ray-traced sensors | USD pipeline, Omniverse ecosystem, Isaac Lab (RL), Replicator (synthetic data), ROS 2 SIL | **Highest.** RTX GPU required, multi-GB install, USD authoring skill, extension/Omnigraph wiring. Payoff: GPU-parallel physics, thousands of parallel training envs, photoreal SDG. |
| **Gazebo** (Classic + Sim/Ignition) | ODE default (also Bullet/DART/Simbody), SDF/URDF worlds | Plugin architecture (model/world/sensor/system plugins), version coupling with ROS distros, CPU-bound | **High, in friction.** "Gazebo hell" is the ROS-version/plugin-build tax. Payoff: the de-facto standard for ROS robot stacks; huge model library. |
| **Webots** (Cyberbotics, Apache-2.0 since 2018) | ODE fork; VRML-based `.wbt` worlds | Controller = external process per robot (C/C++/Python/ROS/Java/MATLAB); supervisor API | **Moderate.** One process per robot, CPU-bound; fine for dozens of robots and evolutionary-robotics runs; `robotbenchmark.net` runs it in the cloud. Payoff: determinism, education, self-reconfiguring/swarm robotics research. |
| **MuJoCo** (Google DeepMind) | Custom fast contact model; MJCF | Tuning contact params; no rendering out of the box | **Low-moderate.** The RL workhorse (dm_control); extremely fast, deterministic-ish, made for learning loops. |
| **PyBullet** | Bullet | Python-native; simpler but less faithful | **Low.** Fastest to script; the "good enough" tier. |

The pattern across all five: **every step up in fidelity is a step up in
toolchain complexity — GPU requirements, scene formats, plugin ecosystems,
version coupling — and the fidelity is only worth it if the question you're
asking needs it.** A twin that answers "will the door close before the arm
arrives" does not need RTX ray tracing; it needs a good clock and honest
collision math. The strict-definition literature adds the second rule: a twin
without a live data link to its physical counterpart is a simulation, and
labeling it a twin breeds cynicism. The third rule, from virtual commissioning:
the twin's highest-value moment is *before* the physical thing exists.

**What quilt already is.** The fleet's own repos are full of twin-shaped code
(Part III): `mud-arena/src/tolerance.py` tracks prediction-vs-measurement error;
`vessel_to_quilt.py` bridges F/V EILEEN's twin state; `quilt-mhs` makes a device
an addressable resource with a safety envelope; the REFLEX-ARC chain replays a
gate bit-identically on metal. The lesson the era adds: **a twin is a contract
with a calibration loop** — shadow → twin → aggregate, with the digital thread
as a first-class data path, and the cheapest simulator that answers the question
as the default.

#### Digital-twin → design lessons

| Culture fact | The need behind it | Design lesson for the semantic-tower compiler |
|---|---|---|
| Shadow vs twin (data flow direction) | One-way monitoring ≠ bidirectional control | The compiler's twin opcodes must distinguish `view` (shadow: read-only telemetry) from `effect` (twin: commanded write) — which the 5-opcode vocabulary already does (`qm_view` vs `qm_effect`). Make the direction part of the cell contract. |
| DTP / DTI / DTA lifecycle | Prototype, per-instance, fleet-aggregate are different artifacts | The compiler should emit a **prototype sheet** (DTP), instantiate per-device twins (DTI) bound to device IDs, and define aggregate views (DTA) as fleet-level cells. `quilt-mhs`'s `DeviceManifest`/`DeviceId` are the DTI spine. |
| Virtual commissioning | Validate the process before the hardware exists | Compile-then-simulate must be a first-class flow: same QUF drives the testbench, the soft core, and the fabric (DOCTRINE 5). The compiler's sim is not a preview; it is the same artifact. |
| "A twin without a data link is a simulation" | The label must mean live synchronization | The compiler must track **freshness** — a bounded-staleness dial on every view (FOUNDATION D4, session illusion). Stale views are a verdict class, not an implementation detail. |
| Isaac Sim's RTX/USD tax; Gazebo's version coupling | Fidelity is expensive | The compiler's default target is the cheapest honest simulator (Webots-class determinism, or the fabric testbench itself), with Isaac Sim-class fidelity only as an explicit, budgeted upgrade. **Fidelity is a dial, not a default.** |
| Calibration (tolerance tracking, sim-to-real) | Predictions must be falsifiable | Every twin ships a `ToleranceTracker`-style cell: predicted vs measured, error %, drift detection, adjustment suggestions (`mud-arena/src/tolerance.py` is the seed). The compiler emits calibration cells with each twin. |

---

## Part II — the consolidated culture → design table

| # | Era | Sharpest culture fact | Design lesson (one line) | Compiler consequence |
|---|---|---|---|---|
| 1 | PLATO | Teachers wanted similar-not-identical; `specs` tuned pedantry | Judgment is (answers, tolerance dial) as state, not code | Pattern grammar + per-answer dials; AMBIGUOUS never guesses |
| 2 | PLATO | `compute` accepted any numerically-equivalent expression | Expressions are judged by execution, not string match | Expression-judge cells; compile-then-compare within ε |
| 3 | PLATO | Notes-files, DELPHI, Boneyard Creek | Users are authors; deliberation is aggregation | Authoring = cell creation; moderation = a cell; weighted opinion = judgment |
| 4 | PLATO | Whole-corpus conversion on language change | The ecosystem migrates atomically | Versioned IR + codemod passes in the compiler |
| 5 | MUD/Zork | `xyzzy` → "Nothing happens" — folklore from rejection | REJECT is social; determinism lets folklore form | Deterministic verdicts; identity in the rejection text |
| 6 | MUD/Zork | Command transcripts of failed inputs | Failed input is the training set | Log REJECT/AMBIGUOUS streams; feed a self-improvement loop |
| 7 | MUD/Zork | Wizard godhood; `@create`; student-built worlds | Content is created at runtime by users | Top of the tower is an authoring surface; grants per creation |
| 8 | MUD/Zork | Z-machine: one game, N interpreters | Portability is a machine, not a rewrite | QUF IR; thin targets; bit-identical behavior everywhere |
| 9 | Games | Space Invaders' emergent speedup | Variable timestep is an accident, not a dial | Fixed ticks as deadlines; bounded ops |
| 10 | Games | Doom 35Hz demos; lockstep RTS; GGPO | Determinism is what makes replay/trust possible | Fixed-point everywhere; determinism tests emitted by the compiler |
| 11 | Games | 16.7ms frame budget, per-subsystem | Budgets are measured and enforced | Per-cell budget reports; refuse over-budget sheets |
| 12 | Games | 1-frame response; coyote time; input buffering | Forgiveness is feel; latency is the product | View-latency bounds verified by TBs (SYNTHESIS I2) |
| 13 | Demoscene | 4k/64k intros; kkrieger's 96KB FPS | Constraint is identity and generative | Quantization IS the algorithm; target budgets as first-class configs |
| 14 | Twins | Shadow vs twin; digital thread | Direction of data flow is the contract | `view` vs `effect` opcodes; freshness dials |
| 15 | Twins | DTP/DTI/DTA lifecycle | Prototype, instance, fleet are different artifacts | Compiler emits prototype sheets, per-device twins, fleet aggregates |
| 16 | Twins | Virtual commissioning | Simulate before the hardware exists | Same QUF drives sim and fabric; sim is the same artifact |
| 17 | Twins | Isaac Sim's RTX tax vs Webots' determinism | Fidelity is a dial, not a default | Cheapest honest simulator is the default target |

The three sharpest (for the report, Part IV): **#1 (tolerance judgment as state),
#6 (failed-input telemetry as training data), #8 (portability machine + #10
determinism)** — these are the ones with no equivalent already in the quilt
canon and the largest leverage on the compiler's shape.

---

## Part III — the SuperInstance reuse map: which repo feeds which compiler level

**The tower, named.** The compiler's levels follow the 8-level fractal already
defined in code: `quilt-cell-bridges/abstraction_levels_to_quilt.py` —
cell (0) → sheet (1) → agent (2) → harness (3) → fleet (4) → ecosystem (5) →
infrastructure (6) → system (7). Each level is itself a cell with its own
primitives, conservation law, and watch oscillation. The compiler's job:
**lower L7–L5 semantic content (bridges, rituals, charters) through L1 sheets to
L0 cells, then to QUF and fabric** — with judgment and verification at every
level.

### Repo-by-repo survey

#### `quilt-cell-bridges` — the tower itself + the front-end
**What it does.** 50 bridge scripts port the 300-repo SuperInstance ecosystem
into `.qzt` cell graphs; one file, three openers (TOP spatial / FRONT signals /
SIDE time).

**Cell/bridge/twin concepts already in code.**
- `abstraction_levels_to_quilt.py` — `LEVELS` (0–7, each with the 8 primitives),
  `CONSERVATION` (per-level γ/η/budget triples), `WATCH` (per-level oscillation),
  `EXAMPLES`, `make_level_cell()`. **This is the semantic tower, in code.**
- The bridge pattern (read → map → emit) + `cell(path, kind, value, depends_on)`
  helper (`vessel_to_quilt.py`) — the minimal cell constructor the compiler's
  front-end should reuse verbatim.
- `.qzt` format: `version/kind/name/description/cells/edges/external_refs/stats/
  tags`; cell anatomy: `id/path, kind, form, description, primitives, z_in/z_out,
  jepa (predict/observe), double_entry (γ/η), vibe (pos/vel/acc), gc, murmur,
  graph, openers, substrate, tags`.
- Region conventions (`vessel.*`, `env.*`, `bathy.*`, `nav.*`, `timeline.*`,
  `soul.*`, `level_N`) — a stable addressing dialect any two bridges share.
- `mud_family_to_quilt.py` — the MUD family as cells ("The MUD family IS the
  spatial substrate of Quilt"), per-slug primitive assignment; `synth_*`
  generators for systems without live APIs.

**Feeds compiler levels:** L7–L0 *vocabulary* (levels, kinds, primitives,
conservation), the front-end (bridges = semantic capture), the sheet grammar
(`.qzt`), and the 3-views contract (a sheet must render space, signals, and time
— the compiler's completeness check for a lowered sheet).

#### `quilt-esp32` — the working compiler prototype + a backend
**What it does.** A `no_std` Rust Quilt runtime for ESP32-class chips; verified
on hardware (limb-blink, 2026-08-26); the REFLEX-ARC chain (2026-08-26) exports a
critic's gate to metal with **100.0000% agreement**.

**Cell/bridge/twin concepts already in code.**
- `src/lib.rs` — `enum CellKind { Value, Formula, Program, Sensor, Api, Listener,
  Router, Io }` (the 8-kind taxonomy), `enum CellValue { None, Bool, Int, Float }`
  (tagged union sized for an MCU), `struct Cell { id, kind, value, deps: [u8;8],
  dep_count }`, `struct QuiltEngine { cells: [Option<Cell>; 64], count }` with
  `define/set/get/add_dep` — the compiler's cell type lattice **and** its fabric
  budget (64 cells, 8 deps, single static memory block).
- `firmware/blink.qm`, `critic-gate.qm`, `eileen.qm` — `.qm` rule tables:
  data-only artifacts with sha256 mint receipts. **`.qm` is the compiler's
  proven IR-once-removed.**
- The mint-to-metal chain (`docs/REFLEX-ARC-2026-08-26.md`):
  `gate-bands.json → critic-gate.qm (export, sha baked in) → qm_gate2c.py →
  gate_qm.h (C tables) → critic_gate.c → firmware + host replay`. 480/480
  channel readings and 80/80 verdicts bit-identical; judge latency 20ns p50.
- `docs/MILESTONE-2026-08-26.md` — `blink.qm → qm2c.py → qm_prog.h
  (compile-time table)`: the LLM-authored sheet compiled to a table, flashed,
  blinking at 1Hz.

**Feeds compiler levels:** L0 cell taxonomy; the IR toolchain (`.qm` + codegen);
the verification harness (bit-exact replay across two targets); the budget
story (RAM 6.5%, flash 20.4% — per-cell cost accounting).

#### `quilt-mhs` — the device contract + constraint vocabulary
**What it does.** Bridges quilt cells ↔ Anthropic's Model Hardware Standard
(announced 2026-08-27, spec not yet public — every guess isolated behind ports):
a controller adapter, a quilt-as-device substrate profile, inter-quilt
federation, and a conformance suite.

**Cell/bridge/twin concepts already in code.**
- `crates/quilt-mhs/src/mhs/types.rs` — `enum MhsValue { Null, Bool, Int, Float,
  Str }`; `struct Channel { name, unit, writable, range: Option<(f64,f64)>,
  destructive }`; `struct SafetyEnvelope { channel_limits, max_write_rate_hz,
  destructive_requires_grant, abort_supported }`; `DeviceManifest`, `Command`,
  `enum MhsError`. **SafetyEnvelope is the tolerance-dial vocabulary for physical
  channels: limits are state the device enforces, "not agent politeness."**
- `crates/quilt-mhs/src/controller/mod.rs` — `QuiltMhsAdapter<C: MhsClient>` with
  `bind/bind_to_device/link/link_closure/effect/effect_batch/view/tick/grant/
  interlocks/forget/channel_relevance` — the **5+1 opcodes** (BIND/LINK/EFFECT/
  VIEW/TICK + FORGET), the same vocabulary as `rtl/q_cell_core.v`'s
  `OP_BIND..OP_TICK`; `DeviceBinding`, `Cell`, `OpEvent`, `ForgetReceipt`.
- `tests/conformance.rs` (a *lying transport must fail*), `tests/federation.rs`,
  `tests/laws.rs` — the conformance-suite pattern.

**Feeds compiler levels:** L2–L1 constraint/judgment vocabulary (safety
envelopes as dial state), the device-binding contract (cells ↔ physical
channels — DTI instantiation), the FORGET-as-safety-teardown semantics, and the
"conformance or it doesn't exist" verification pattern.

#### `quilt-pincher` — the agent-level sheet + LLM-as-compiler
**What it does.** A reflex engine rebuilt so every layer is a Quilt cell; same
sheet runs cloud / workstation / ESP32 (`<50ms`, no LLM on the board).

**Cell/bridge/twin concepts already in code.**
- `src/cells/sheet.ts` — the whole engine as a sheet: `pinch` (formula),
  `match` (program), `execute` (program), `veto` (listener), `compile` (ai),
  `store` (vector_store) — six cells, five kinds. **The `ai` cell is the
  "LLM as compiler" pattern**: unknown pinches get compiled into the reflex
  database at runtime.
- `src/core/types.ts` — `Reflex { id, embedding, intent, action,
  safety: SafetyHints, confidence, hits, createdAt, lastHitAt, provenance }`;
  `SafetyHints { sandbox, network, filesystem, timeoutMs }`; `PinchResult`
  (hit/confirm/compiled/vetoed/error); `Embedder`/`ReflexStore` interfaces.
  `provenance: { compiledBy, parentReflex }` is lineage as data.

**Feeds compiler levels:** L2 (agent sheets), the safety-hint vocabulary
(another dial family), and the fallback path: when the compiler can't lower
something, an `ai` cell compiles it — the semantic-tower compiler's
"unknown pinch" handler already exists as a pattern.

#### `quilt-vision` — the perception-cell grammar
**What it does.** Images as cells, vision as formulas; declarative vision
sheets ("drop an image, get caption + tags + objects").

**Cell/bridge/twin concepts already in code.**
- `src/index.js` — `class VisionCell { id, input, model, kind, params, value }`
  (a value cell whose value is the model's output on an input image cell) and
  `VISION_KINDS` — caption/text/faces/objects/tags/embed/segment/depth, each with
  `description / output / models[]` — **a declarative model-routing table.**

**Feeds compiler levels:** L1 sheet grammar for perception/sensor cells; the
`model` field as the compiler's backend-routing annotation (which target model
serves which kind, per fabric).

#### `quilt-evolve` — the self-improvement loop
**What it does.** 4-component evolution loop (generator / system / judge /
mutator) at any scope: one cell, a sub-graph, or the whole sheet.

**Cell/bridge/twin concepts already in code.**
- `src/loop.ts` — `evolve(config)`: generate inputs → run system → judge →
  mutate → stats (avg/best/stddev/plateau detection).
- `src/judge.ts` — `LLMJudge`, `HeuristicJudge`, `ExactMatchJudge`; `src/
  generator.ts` — `LLMGenerator`, `SeededGenerator`, `PerturbationGenerator`;
  `src/scope.ts` — `FullSheetScope`, `CellScope`, `SubGraphScope`,
  `ProgramCodeScope`, `HierarchicalScope`; `src/system.ts` — `FunctionSystem`,
  `QuiltSystem`.

**Feeds compiler levels:** the compiler's self-improvement loop (judge family =
tolerance dials: ExactMatch = r=0, Heuristic = dialed, LLM = learned); scopes =
compile units at any tower level; plateau detection = when to stop mutating.

#### `mud-arena` — the judge vocabulary, twin calibration, and evolution in the world
**What it does.** A MUD-mechanics agent gym: RoomGraph worlds, adventure-game
command parsing, genetic evolution of agent scripts, GPU-accelerated simulation,
tolerance tracking, WebSocket/Telnet/HTTP observation.

**Cell/bridge/twin concepts already in code.**
- `src/mud_arena/commands.py` — `enum Verb`, `@dataclass Command { verb, target,
  indirect, raw }`, `parse_command()` with **synonym folding**: `go/move/walk/
  run/head`, `examine/x/inspect`, `take/get/pick/grab`, `look/l`, `i/inv/
  inventory` — a working alias table = zero-distance equivalence classes
  (FOUNDATION D2's pseudometric, implemented).
- `src/tolerance.py` — `Measurement { predicted, actual, error_pct, ... }` and
  `ToleranceTracker` (stats, drift detection, adjustment suggestions, JSON
  persistence) — **the digital-twin calibration cell**, already written.
- `src/evolve.py` — `Script(rules)`, evaluation, tournament selection,
  crossover + mutation, adaptive scenario generation (harder as fitness
  improves), pickle export.
- `src/mud_arena/agent.py` — perceive → decide → act loop; `rooms.py` —
  `Room`/`RoomGraph`.

**Feeds compiler levels:** the parser/judge vocabulary (aliases), L0 tick
semantics (perceive/decide/act = one cell tick), twin calibration (tolerance
tracker), and evolutionary search (compiler hyperparameter/architecture search).

#### `the-tap` — the builder-immortal philosophy (design DNA, not quilt-coded)
**What it does.** The agent tavern: rooms, drinks, games, campaigns; a radio
podcast (Open Mic); rituals and social contracts. Not a quilt-coded repo, but
the clearest statement of what the tower's top level should *feel* like.

**Cell/bridge/twin concepts already in code (as design docs).**
- `THE-BUILDER-SYSTEM.md` — the MUD-builder toolkit mapped onto LLM-agent
  mechanics (potion design → context-window parameter modification; `@create`
  at runtime → Builder's Interface). Design principles: **everything is data,
  not code; everything has history; everything is transient by default; the
  builder serves the story.**
- `RITUALS-AND-CONTRACTS.md` — "You don't script culture — you create the
  conditions for it to grow." Soft enforcement via DM nudges; tradition
  tracking.
- `OPEN-MIC-SYSTEM.md` — whole-moment performances that exist once; the campaign
  log as raw material.

**Feeds compiler levels:** L7–L5 design philosophy — runtime content creation,
history as first-class data, transience as default, and the "builder serves the
story" rule (deploy cells when the story needs them, not to show off
mechanics).

#### `quilt-verilog` — the bottom of the tower (the target the compiler lowers to)
**What it is.** Pure Verilog-2005, zero vendor deps; 9 RTL modules + testbenches;
QUF container; formal checks via yosys-sby.

**Cell/bridge/twin concepts already in code.**
- `rtl/q_cell_core.v` — `OP_BIND/OP_LINK/OP_EFF/OP_VIEW/OP_TICK/OP_ACK/OP_NAK`,
  bounded run-to-completion FSM (`MAX_OP_CYCLES`), Q2 tick deadline.
- `docs/QUF-SPEC.md` + `tools/quf.py` + `rtl/q_uf_loader.v` — the GGUF-of-cell-
  state container: magic `QUF\0`, GGUF value-type numbering, dials/edges/
  routing/tick sections, unknown-KV-skip extensibility. **The compiler's IR.**
- `tb/` + `tb/formal/` — synchronous observers and sby `mode prove` (flit-pipe
  FIFO contract proves in ~0s by k-induction).

**Feeds compiler levels:** L0 target; the IR format; the verification floor.

### The reuse map, by compiler stage

| Compiler stage | Tower levels | Reuse source (repo · file · symbol) |
|---|---|---|
| **Front-end: semantic capture** | L7–L5 | `quilt-cell-bridges` · `abstraction_levels_to_quilt.py` · `LEVELS/CONSERVATION/WATCH`; the 50 `*_to_quilt.py` bridges; `the-tap` · `THE-BUILDER-SYSTEM.md` (authoring philosophy) |
| **Tower vocabulary (levels/kinds/primitives)** | all | `quilt-cell-bridges` · `abstraction_levels_to_quilt.py` (8 levels, 8 primitives); `quilt-esp32` · `src/lib.rs` · `CellKind` (8 kinds); `.qzt` cell anatomy (`jepa`, `double_entry`, `vibe`, `gc`, `substrate`) |
| **Judge/constraint vocabulary** | L2–L1 | `quilt-mhs` · `mhs/types.rs` · `SafetyEnvelope`/`Channel`; `mud-arena` · `commands.py` · `parse_command` (aliases) + `tolerance.py` · `ToleranceTracker`; `quilt-pincher` · `core/types.ts` · `SafetyHints` + `veto` cell; `quilt-evolve` · `judge.ts` · judge family |
| **Graph lowering (sheet → cells)** | L1–L0 | `quilt-pincher` · `cells/sheet.ts` · `PincherSheet`; `quilt-vision` · `src/index.js` · `VisionCell`/`VISION_KINDS`; `quilt-cell-bridges` · `vessel_to_quilt.py` · `cell()` helper |
| **IR (state is a file)** | all | `quilt-verilog` · `docs/QUF-SPEC.md` + `tools/quf.py` + `rtl/q_uf_loader.v` (QUF); `quilt-esp32` · `firmware/*.qm` (proven data artifact, sha256-minted); `quilt-cell-bridges` · `*.qzt` (semantic-layer IR) |
| **Backends (targets)** | L0 | `quilt-verilog` · `rtl/` (`q_cell_core.v` opcodes, `q_hebb_edge`, `q_dialfile`, `q_tick_sched`); `quilt-esp32` · `qm2c.py`/`qm_gate2c.py` → C tables + `src/lib.rs` no_std engine; `quilt-mhs` · substrate profile (quilt-as-MHS-device) |
| **Verification** | all | `quilt-esp32` · `docs/REFLEX-ARC-2026-08-26.md` (bit-exact cross-target replay, mint receipts); `quilt-mhs` · `tests/conformance.rs` (lying transport must fail); `quilt-verilog` · `tb/` + `tb/formal/` (sby); `mud-arena` · `tolerance.py` (drift/calibration) |
| **Self-improvement** | L2–L0 | `quilt-evolve` · `loop.ts` · `evolve()` + `scope.ts` scopes; `mud-arena` · `evolve.py` (GA, adaptive scenarios); `quilt-pincher` · `compile` (ai) cell (LLM-as-compiler fallback) |

**What's already proven end-to-end.** The REFLEX-ARC chain is the semantic-tower
compiler in miniature, already run: *semantic gate (JSON, mint artifact) → .qm
data IR → C tables → two targets (firmware + host), bit-identical, sha256
receipts, radio dark.* The compiler project is not "build the toolchain" — it is
"generalize the REFLEX-ARC chain up the tower, and hang the bridges from the
front-end."

---

## Part IV — the report: three sharpest lessons, three artifacts

**The three sharpest culture → design lessons.**

1. **PLATO: judgment with tolerance is state, not code.** Teachers wanted
   similar-not-identical answers with per-question pedantry (`specs`), numeric
   equivalence within roundoff (`compute`), and spelling tolerance by bit-vector
   phonetic distance. The compiler must make every judgment a
   (keyed-answers, tolerance-dial) pair — and AMBIGUOUS must surface the verdict
   set, never guess (FOUNDATION D2 already formalizes this; the culture proves
   it was the product, not the parser).

2. **Zork: failed input is the training set.** The implementers logged
   unsuccessful commands and improved the parser against them; "guess the verb"
   became shared folklore because rejections were deterministic and characterful.
   The compiler must record every REJECT/AMBIGUOUS verdict (input, context,
   dials) as first-class data and feed it back into the judge vocabulary — a
   built-in quilt-evolve loop from day one.

3. **Z-machine + Doom ticks: portability is a machine, trust is determinism.**
   Compile once to bytecode, interpret everywhere (Z-machine → QUF); fixed ticks
   make replays, demos, and lockstep trustworthy (Doom 35Hz, GGPO, AoE). The
   compiler's middle end emits portable IR and thin targets; its lower end
   enforces fixed-point determinism so sim == silicon — the same bet
   quilt-verilog already took, now with a compiler in front of it.

**The three reusable SuperInstance artifacts.**

1. **The 8-level tower, in code** — `quilt-cell-bridges/abstraction_levels_to_quilt.py`:
   `LEVELS` (0–7 with primitives), `CONSERVATION` triples, `WATCH` oscillations,
   `make_level_cell()` — the compiler's level vocabulary and cell anatomy,
   already emitted as `.qzt` graphs. This *is* the semantic tower; the compiler
   names its passes after it.

2. **The mint-to-metal chain** — `quilt-esp32` REFLEX-ARC: `gate-bands.json →
   critic-gate.qm (sha256 mint) → qm_gate2c.py → C tables → firmware + host`,
   100.0000% bit-exact replay, 20ns judge latency. The compiler's IR + backend +
   verification harness, proven on real hardware with honest failure-mode
   notes.

3. **QUF, the state-is-a-file IR** — `quilt-verilog` `docs/QUF-SPEC.md` +
   `tools/quf.py` + `rtl/q_uf_loader.v`: the GGUF of cell state (dials, edges
   with Hebbian walk counts, routing, tick schedule), loadable identically into
   testbench, soft core, or fabric. The one file that makes the whole tower
   portable — the Z-machine lesson, made the fleet's weights.

**Honest debt.** This lane did not verify the contemporary state of Isaac Sim's
requirements or Gazebo's ROS coupling beyond documentation-level sources (2026
docs pages, Wikipedia); simulator cost claims should be re-checked against a
live install before the compiler's fidelity dials are fixed. The `.qm` chain's
"data-only, VM stays out of the numeric path" decision is documented as
artifact-#1-only (kimi's no-generalization rule); the compiler inherits that
seam as its own open question.
