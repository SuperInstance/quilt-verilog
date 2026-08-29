# LINEAGE — the pre-C engineering inheritance of the quilt

**Lane:** lineage-research (Flash, extensive web sweep) · **Date:** 2026-08-29
**Inputs:** v1 rtl/ + docs/DOCTRINE.md + docs/BACK-DECK-APP.md + docs/ABSTRACTION-MATH.md
**Method:** primary-source sweep of CERL reports (X-5 economics, X-20 architecture, X-27
output controller, X-35 spelling/concept recognition), the TUTOR command reference (Avner 1981),
the CDC PLATO User's Guide (1981), the 1954 FORTRAN Preliminary Report, Backus's 1978 Turing
lecture, the CHM Bitzer oral history (2022), plus the RPG/COBOL/VSM/HDL secondary literature.
**Companion:** ABSTRACTION-MATH.md (the formal-object side of the same bet: the fabric is a
traced monoidal wiring of causal stream functions; this doc is the *why we are allowed to go
there* — the lineage of people who built the same way before the split hardened).

> **The one buildable idea, in two lines.** Every concept the quilt needs at the bottom —
> approximate semantic judgment, asynchronous presence at scale, budget-forced frugality,
> fixed-cycle transactionality, cell-to-cell contracts — was already built, working, and
> economically forced between 1954 and 1981, *before the hardware/software split hardened*.
> The five opcodes are not a novel reduction; they are the common denominator of PLATO's
> TUTOR runtime, RPG's program cycle, COBOL's ledger batch, and FORTRAN's array machine —
> re-derived bottom-up in silicon because the software layer that inherited those ideas
> abandoned the machine model that made them cheap.

---

## 0. TL;DR

- **PLATO (CERL/UIUC, 1960–80s) is the direct ancestor of the cell graph.** Its TUTOR
  language ran *judging machinery* — a family of small, independently switchable approximate
  matchers (spelling, word order, capitalization, numeric tolerance, synonym tables) feeding a
  tri-state verdict (`ok` / anticipated `wrong` / unanticipated `no`) — on a 60-bit-word
  mainframe, behind a 1260-baud link, at a 25–30¢/terminal-hour price target that *forced* the
  gas-plasma panel (memory in the glass, no refresh, write-only-changes). It served ~1000
  terminals off one CDC 6400 with a 1/60-second broadcast frame and NOPs to idle terminals
  (X-20, X-27), and its economic model (X-5, 1973) was a queuing-theory proof that 4000 users
  could share one CPU at 500 µs expected wait. The "session illusion" — thousands of
  co-present-feeling users on physically separate CYBERs — ran on shared-memory TUTOR common
  blocks, per-user persistent state, notesfiles, and a billing substrate of Network Transfer
  Units. Everything here is a quilt concept with the serial numbers filed off.
- **RPG (1959/64) and COBOL (1959/60) are the transactional lineage.** RPG's *program cycle*
  is the fixed loop-as-structure (read → calculate → output → total, with level breaks and
  matching records) — the tick, before clocks were clocks. COBOL's four divisions, PICTURE
  clauses, and master-file/transaction-file batch update encode ledger semantics: control
  totals, hash totals, and the audit trail. Double-entry's "every debit has a credit" is the
  intercell contract in accounting form.
- **FORTRAN (1954–57) is the vectorization lineage and the split's ground zero.** Arrays and
  DO loops made the machine's memory a *mathematical object*; the 1954 Preliminary Report
  explicitly moved machine knowledge *out of the programmer* ("built into the FORTRAN system
  and it is not necessary for the programmer to be familiar with this information" [1]) —
  that is the moment compilation abstracted the machine away. What was lost: the machine model
  itself. The kernel/BIOS people never stopped holding it by hand (CP/M BIOS, PC BIOS, device
  drivers, interrupt vectors), and the hardware people never got a language for it until
  Verilog (1984) and VHDL (1987) — 27–30 years after FORTRAN, and even then HDLs started as
  simulation, with synthesis coming later. The quilt's bet: go back below the split. The
  fabric is the machine; state is a file; "intelligence lives at the bottom."
- **Before "embedding" meant word2vec**, vector meant *array* (FORTRAN), then *machine*
  (Cray-1, CDC STAR-100), then *document* (Salton's vector space model, 1975 — cosine
  similarity for retrieval), then *word* (Mikolov 2013). The quilt's cosine/vMF cells sit at
  the 1975 end of that chain and are implementable at the 1957 end: fixed-point arrays and
  shift-add cosine, no floating point, no divide.

---

## 1. PLATO: the judging machinery and the price-point that forced the hardware

### 1.1 The answer-judging machinery (the match-cell's grandfather)

PLATO III lessons were FORTRAN programs; the TUTOR language (Tenczar, 1967; CERL 1969) was
created expressly because FORTRAN was too hard for teachers: the TUTOR Manual abstract is
explicit — "TUTOR is designed to transcend the difficulties of FORTRAN for a computer-based
educational system utilizing graphical screen displays. The language consists of about
seventy words or 'commands'… designed specifically for use by lesson authors lacking prior
knowledge of and experience with computers. Although authors are able to write parts of
useful lessons after approximately one hour of introduction to TUTOR…" [2]. Seventy commands,
one hour to first useful lesson: the same ratio as the quilt's five opcodes. The ERIC
abstract for the X-35 report [3] describes what those commands were for: "matching of words
and concepts offered by students to those proposed by lesson authors… a word recognition
algorithm that handles spelling errors without doing character-string manipulations or linear
searches. The spelling algorithm uses human rather than machine criteria."

The mechanism (Tenczar & Golden 1972, CERL X-35; summarized in [4]): each word of student
input and each word of the answer pattern was converted to a **bit vector** (60/64 bits) with
fields for letter presence, letter-pair presence, and first letter; the **Hamming distance**
between XOR'd bit vectors approximated phonetic difference. No string manipulation, no
linear search, no dictionary — a fixed-cost, hardware-friendly approximate matcher. That is
the keypunch-era pattern judgment: it is what a match-cell is, minus the pipeline.

The judging block (from the TUTOR command reference [5], which is the CDC/UIUC authoring
bible) was an **iterative control structure**: `arrow` opens a judging block, `answer` /
`wrong` / `answerc` / `wrongc` / `answera` / `wrongs` pattern-match the response, `specs`
tunes the judgers, `judge` alters the verdict, `okword` / `noword` customize the feedback.
The details that matter to the quilt:

- **The judging copy.** Before matching, the response is normalized into a "judging copy":
  `bump` strips characters, `put`/`putd`/`putv` replace substrings, `close`/`open` convert
  storage. All judging runs on the normalized copy — the response pipeline is a cell graph in
  miniature, and the ALIAS cell's "aliases are data" [6] is its descendant. Hard bound: if the
  judging copy exceeds 300 characters, judgment terminates as "no" [5]. A budget on the
  normalization stage, in 1972.
- **The specs family = dials.** `specs` tags independently disable or relax individual
  judgers: `nospell` (off with the spelling judger), `noorder` (off with the word-order
  judger), `nodiff` (off with the numeric-difference judger, "which treats a numerical
  response as a 'misspelling' if it is within 1% of the correct response"), `okcap`,
  `okextra`, `okspell` ("any reasonable spelling"), `toler` (1% numeric tolerance),
  `allwords`, `alphxnum`, `bumpshift`, `exorder`, `holdmark`, `nomark`, `nookno`, `noops`,
  `novars`, `okassign` [5]. Each judger is a small independent machine with its own on/off
  and tolerance; the system variables `spell`, `capital`, `extra`, `order` report which
  judgers were active. This is `q_dialfile` semantics: **config is a set of switches on
  independent matchers, not a program rewrite.** The quilt's THRESH / MATCH_WIN / LEGAL_SET
  dials [6] are specs tags.
- **Synonym tables.** `synonym` "sets up a list of synonyms for judging"; `vocabs`/`vocab`
  define ignorable words plus synonymous required words with endings; `concept`/`miscon`
  judge at the concept level, detecting *which* synonym was entered ("concept WORD1 WORD2,
  VAR1+ WORD1, VAR2+ WORD2 (detects which synonym is entered if the vocabulary is
  appropriately set up)") [5]. The ALIAS table (pink≡humpy, chum≡dog≡keta, king≡chinook,
  coho≡silver [6]) is a `vocabs` block. Note the two-way corroboration in BACK-DECK-APP — the
  tote volume ID *corroborates* a new overheard alias row [6] — which is exactly the
  `concept` command's synonym-detection wiring.
- **The tri-state verdict.** The `judged` system variable is ternary: **-1 = ok, 0 = wrong
  (anticipated), +1 = no (unanticipated)** [5]. `judge` commands alter it: `judgeok`,
  `judgeno`, `judgewrong`, and the quit variants. Anticipated-vs-unanticipated is not a
  cosmetic distinction — it drives what feedback the student gets and what the author learns.
  The quilt's XID-MATCH cell returns match / no-match / **AMBIGUOUS** ("never a guess" [6]):
  the same refusal to collapse three states into two. And the lesson author's "Duplicate
  Answer" rejection (X-5 documents the system refusing a repeated answer and demanding a
  *different* correct response [7]) is an audit-cell behavior: the ledger remembers what was
  already accepted.
- **Algorithmic judgment vs. answer lists.** X-5 is explicit: "whenever possible, algorithms
  are used to determine the correctness of the student's response… The use of algorithms
  instead of comparing the answer against a long list of pre-stored answers not only makes
  the system more flexible but also saves memory space" [7]. Judgment by computation, not
  lookup — the quilt's golden-model testbenches and sby monitors [8] are the same doctrine
  applied to silicon.
- **Judging is a first-class cost.** X-5's traffic statistics: 70% of requests are a
  keypush-and-echo; judging a completed answer — "the computer must analyze his answer to
  see if it is equivalent to a correct response, check for spelling and completeness of the
  answer, as well as inform him which part of an incorrect answer is unacceptable" — is 7% of
  requests, with 20 ms average processing [7]. The system was *designed around* the
  request-rate × processing-time product being roughly constant (drill: 1 request/1.5 s at
  10 ms; tutorial/inquiry: 1 request/4 s at 20 ms) [7]. The quilt's streaming fixed-point
  matchers are the same accounting: match-cells are budgeted per tick, not per corpus.

### 1.2 The price point that forced the hardware (the fabric budget's ancestor)

X-5 (Bitzer & Skaperdas, CERL, 1969–73) is the economic charter. The design goal: "the cost
of computer-based education should be comparable with the cost of teaching at the elementary
grade school level… (25–30 [¢] per terminal hour for the use of the computer and terminal)"
[7]. Conventional elementary instruction ≈ 27¢/student-contact-hour; the computer + software
was budgeted at 12¢/student-contact-hour; that left **≤ $1,900 per terminal** (including a
digitally addressable graphical display, keyset, and slide selector) as the maximum, and
"present indications are that this cost can be met" [7]. The delivered Magnavox PLATO IV
terminals cost on the order of **$12,000** [9] — the gap between price point and delivered
price is the whole tragedy of PLATO's commercialization (CDC eventually charged $50/hour for
data-center access [9]).

The price point forced the hardware in a specific, documented chain:

1. **Memory in the glass.** The plasma panel (Bitzer & Slottow patent applied 1964, issued
   1968; first manufacturing partner Owens-Illinois, per the CHM oral history [10]) is a
   bistable gas-discharge cell array: each cell holds its state, so "absolutely no refreshing
   of the display panel by the computer is required" [11]. X-5: "In contrast to the
   commonly-used cathode ray tube display, on which images must be continually regenerated,
   the plasma display retains its own images and responds directly to the digital signals
   from the computer. This feature will reduce considerably the cost of communication
   distribution lines" [7]. No refresh memory, no raster regeneration, no terminal-side video
   RAM: the cost was moved into a simple glass structure projected to be cheap in volume.
2. **Write-only-changes.** Bitzer, verbatim: "we didn't want to retransmit anything… if we
   wanted to change the picture, we only wanted to transfer the changes… 'Only [send] changes
   to the terminal.' And boy, that cut the bandwidth way down… low bandwidth, but high
   performance at the terminal end" [10]. The data link was 1200 bps (later 1260 bps), the
   character writing rate 180 chars/s [7][11].
3. **Broadband economics.** Remote distribution used the CATV midband (the frequency gap
   between TV channels 5 and 6): "the cost of a 4.5 MHz TV channel is approximately $35 per
   month per mile, whereas the rate for a 3 kc telephone line is approximately $3.50 per month
   per mile. Each TV channel can handle at least 1500 terminals on a time-shared basis" [7].
   X-27: an inter-city ETV channel at ~$55/mile/month carries >1000 terminals at <5.5¢/mile/
   month per terminal, versus ~$4.50/mile/month per voice-grade line [12].

The quilt analogue is exact: the fabric budget (LUTs, flits, ticks) is the 27¢-per-student-
hour constraint. It forces memory-adjacent frugality — quantized-by-default, multiplier-free
fixed-point, "the quantization IS the algorithm" [13] — in exactly the way the terminal
budget forced the plasma panel. Every "steal" in the v1 architecture (shift-implied ladder
weights, msb-quantized decay intervals) is a price-point artifact.

### 1.3 The session illusion: 1000–4000 simultaneous users on one CPU (the async-cell precedent)

The PLATO IV architecture (Stifle, CERL X-20, 1972 [11]) and the output controller (Tucker,
CERL X-27, 1971 [12]) are the scaling mechanism, in primary source:

- **One CPU, 1008 terminals, a 1/60-second heartbeat.** The CDC 6400's output controller
  holds two 1024×20-bit memories (double-buffered); every 1/60 s it broadcasts one 20-bit
  word to *every* terminal in the system over a single TV channel [11][12]. "The computer is
  therefore required to send data only to those terminals requiring new information; the
  controller will automatically transmit NOP codes to all other terminals" [11]. The terminal
  ignores NOPs; the display holds its own state. **The tick is a broadcast frame; idle cells
  receive NOPs.** This is `q_tick_sched`'s hard-deadline service discipline [8][14] — the
  fabric guarantees the frame, and cells that have nothing to say pay nothing.
- **Queuing-theory capacity proof.** X-5 models 4000 student stations as Poisson arrivals
  with exponential service times: 1 ms per request, ρ = 0.5, expected wait E(w) = 500 µs,
  "the probability of a student's request queue becoming long… is very small," and the
  computer is idle ~50% of the time — idle time explicitly usable for background batch [7].
  Asynchrony is not a compromise; it is the design. The quilt's "no global scheduler, cells
  tick on their own schedule" [13] is this, without the central mainframe: the ring is the
  arbitration.
- **Per-user load budget.** Doug Jones (who ported TUTOR to a minicomputer, 1976): "PLATO
  was designed as a timesharing system. The machine could execute one MIPS… If they wanted to
  support 200 users, the average user load had to be under 5 TIPS (Thousand Instructions per
  Second)" [15]. A hard per-user instruction budget — the "load unit" of the era. The quilt
  version: per-cell flit/edge budget on the fabric; the tier says how much of the model is
  expressed [6].
- **Shared memory as the multi-user illusion.** Each user process had 150 persistent
  "student variables" (n1–n150 / v1–v150) that followed the user across sessions; lessons
  could attach a shared common block of up to 1500 words — unnamed common blocks shared by
  *all users of that lesson*, named common blocks tied to a disk file [4]. Games (Empire,
  Avatar) ran on those shared words; the Wikipedia PLATO article notes 1500 shared 60-bit
  variables per game made online multiplayer possible [9]. State lives in shared cells; the
  QUF file is the common block, warm-started [6].
- **The multi-CYBER illusion and its billing substrate.** By the late 1970s PLATO ran on
  nearly a dozen networked mainframes serving several thousand terminals worldwide [9]. The
  CDC User's Guide (1981) documents the Data Services Network sign-on (dial → modem/acoustic
  coupler → "type in the identifier of the PLATO system you will be using" → Welcome
  Display) [16], intersystem notesfiles ("Connect Notes Files Across Systems" between e.g.
  "minnd" and "minna", the Minneapolis CYBERs), intersystem file security — and the meter:
  "A unit of inter-PLATO system data transfer is a network transfer unit (NTU). The NTU is
  the tracking and billing unit for use of the networking features… One note is one NTU. One
  note sent to five connected notes files is five NTUs… Intersystem transactions are billed
  as one NTU for every 128 computer words… When a TUTOR file is sent from one system to
  another, one NTU will be charged for each block sent" [16]. Per-site memory allotments
  (`siteinfo`: "the base EM allotment… the EM currently allotted… the EM currently in use…
  the number of active terminals at the site") [5] meter extended-memory per site. The
  session illusion had an accounting layer; so does the quilt (flit counts, QUF as the
  fleet's ledger, audit-cells).
- **The community layer.** Notesfiles (Woolley, 1973; invented because the shared text-file
  "notes" had no authentication [17]), term-talk, Talkomatic, personal notes, Monitor Mode
  screen sharing [9][17]: the asynchronous presence that made thousands of users feel
  co-present. The quilt's back-deck graph [6] is this layer restated as cells: ALIAS,
  BESTSHOT, AUDIT-CAPTAIN, NIGHT-CRON are notesfiles with hardware deadlines.

### 1.4 Authoring under teacher constraints (the five-opcode lesson)

TUTOR's design constraint was the author: a teacher, not a programmer. Seventy commands, one
hour to first useful lesson [2]; the language grew (if/else, loops, indentation-based blocks
that "presaged Python" [4]) by *converting the entire corpus of existing lessons on the
system* whenever the language changed [4] — the system rewrote its own codebase, because the
corpus lived on the machine. X-5 reports author costs ranging over a factor of 10 across
author languages, and that "preparing a good CAI course is roughly equivalent in effort to
writing a good textbook" [7]. The failures are equally instructive: CDC's commercial PLATO
was judged "essentially equal to an average human teacher" at five times the cost [9]; the
critique of page-turner courseware is anticipated by X-5's own guideline #2 — "the computer
should be used as much as possible to simulate turning pages" [7]. The quilt's response is
the same one TUTOR made: authoring = a tiny fixed vocabulary + wiring; complexity lives in
composition, not in the language. Five opcodes, one interpreter, "composition = wiring, not
scheduling" [13].

---

## 2. The transactional lineage: RPG's cycle and COBOL's ledger

### 2.1 RPG: the loop-cycle as fixed structure

RPG (Report Program Generator, IBM, 1959 for the 1401; FARGO was its tab-machine predecessor)
was built so that tab-equipment technicians could move to computers: "Tab machine technicians
were accustomed to plugging wires into control panels… Tab machine programs were executed by
impulses emitted in a machine cycle; hence, FARGO and RPG emulated the notion of the machine
cycle with the program cycle" [18]. The **program cycle** is the language: the programmer
writes code for *one record* and the cycle applies it to every record — read → detail
calculations → detail output → total calculations → total output — with **level breaks** and
**matching records** (header-to-detail file matching) handled by the cycle itself [18]. The
programmer never writes the loop; the loop is the machine's heartbeat. Indicators (01–99
user-defined logical variables plus record/field/report indicators) gate which lines act on
which record [18].

This is the tick in its purest form: a fixed cycle, a fixed set of boolean flags, level
breaks as boundary detection, matching records as windowed association. The quilt's
`q_tick_sched` + `tick_pend` deadline [14] and the night-cron ("the tick is a
hardware-interlocked deadline… the day's effect storms cannot eat the night's improvement
epoch" [6]) are RPG's cycle with the accounting made explicit. The back-deck XID-MATCH window
(MATCH_WIN dial, lost-label vs. crossed-label bet [6]) is an RPG matching-record operation
under a dial.

### 2.2 COBOL: ledger semantics and batch transactionality

COBOL (CODASYL, 1959–60; from FLOW-MATIC, AIMACO, COMTRAN) was the DoD's answer to
non-portable data processing: a 1959 survey found average programming cost of $800,000 per
installation and $600,000 per conversion [19]. Its lasting contributions — long names,
English command words, **separation of data descriptions from instructions** (FLOW-MATIC), the
**PICTURE clause** (COMTRAN) [19] — are all ledger-shaped. The four divisions
(IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE) mirror the structure of business documents;
PICTURE clauses (PIC 9(5)V99) describe data the way an accounting form describes columns;
OCCURS/REDEFINES model tables and overlays.

The semantics that matter here are the batch ones: **master file + transaction file →
updated master file**, with control totals and hash totals checked at the end of each run —
the audit trail as a first-class output. COBOL's world is a world of sequential ledgers
updated in fixed passes, where every run re-derives its own consistency and the totals must
balance or the run is rejected. The double-entry heritage is visible in the shape even where
the language doesn't say the words: every transaction has two legs; the ledger is
self-consistent or it is wrong; the trial balance is the invariant. The quilt's ledger-cells,
audit-cells, and A/B gate [6] are COBOL's batch semantics with the roles reassigned:
`LEDGER-SCALE` writes `{t, weight, species-from-tote}` tuples because "nobody keeps records;
the camera keeps them" [6]; `AUDIT-CAPTAIN` confirm/quarantine with quarantine propagating
*back down the label chain* [6] is the control-total check; `AB-PROMOTE` with **rollback as
the default verdict** ("if the verdict does not clear PROMOTE_MARGIN, nothing is written"
[6]) is the batch commit that refuses to post an unbalanced run. Double-entry → intercell
contract: every `qm_effect` must have its bookkeeping leg; no label enters the ledger without
its corroborating entry.

### 2.3 Why the transactional lineage belongs at the bottom

RPG and COBOL were built for the same machine the quilt targets: sequential, record-at-a-time
hardware with no random access to speak of (cards and tape). Their structures — fixed cycle,
fixed field layout, batch commit, totals — are what transactionality *is* when the memory is
a stream and the clock is a drum. The quilt re-derives them in RTL for the same reason:
cells are byte-addressable state machines; the QUF is a sequential file; the tick is the
cycle; and the audit trail is not a feature but the default semantics of `qm_effect`
propagating through constraint-cells.

---

## 3. FORTRAN: vectorization before "embedding" meant anything

### 3.1 Arrays, DO loops, and the 1954 abstraction moment

The 1954 Preliminary Report [1] is the birth certificate of the split:

- "The IBM Mathematical Formula Translating System or briefly, FORTRAN, will comprise a large
  set of programs to enable the IBM 704 to accept a concise formulation of a problem in terms
  of a mathematical notation and to produce automatically a high speed 704 program."
- Cost case: "out of every dollar spent to solve an average problem on a high speed computer,
  less than 25 cents is spent for analysis and programming, more than 25 cents is spent for
  personnel coding and debugging cost, about 25 cents for machine debugging cost, and about
  25 cents for machine running cost" — so "FORTRAN should virtually eliminate coding and
  debugging, [and] it should be possible to solve problems for less than half the cost."
- The abstraction, verbatim: "the amount of knowledge necessary to utilize the 704 effectively
  by means of FORTRAN is far less than the knowledge required to make effective use of the 704
  by direct coding. Information concerning how to use subprograms, what machine instructions
  are available, how to optimize a sequence of calculations, and concerning a large number of
  other coding techniques, is built into the FORTRAN system and it is not necessary for the
  programmer to be familiar with this information."

That last paragraph is the moment compilation abstracted away the machine. FORTRAN's
vectorization roots are in the same document: DIMENSION (arrays), DO loops, subscripted
variables as first-class math — "vector" as a *mathematical* object (the 1957 compiler even
ran a Monte Carlo simulation of the generated code, weighted by FREQUENCY statements, to place
basic blocks [20]: compilation as simulation, the ancestor of the quilt's golden-model TBs
[8]). What "embedding" meant in 1954–1975, before ML: (a) in mathematics, an injective
structure-preserving map — the placement of one space inside another; (b) in psychometrics,
multidimensional scaling's placement of stimuli into a metric space preserving dissimilarity
(Torgerson 1958; Shepard 1962; Kruskal 1964) — the direct ancestor of word embeddings; (c) in
FORTRAN, the *storage* embedding of arrays into memory, which the compiler computed for you
(subscript → address), and EQUIVALENCE, the programmer's hand-forged overlay [20].

The hardware vectorization line: CDC STAR-100 (1973) and TI ASC (1972) made "vector" a
machine operation; the Cray-1 (1976) sized its vector registers for FORTRAN DO-loop semantics;
"vectorizing compilers" (Kuck's Parafrase et al., 1970s–80s) detected DO-loop independence —
all of it about turning *scalar loops into array operations* on contiguous memory. The
semantic vectorization line: Salton, Wong & Yang, "A Vector Space Model for Automatic
Indexing" (CACM 18(11):613–620, 1975), built on the SMART retrieval system: documents and
queries as term vectors, ranked by **cosine similarity** [21]. That 1975 paper is where
"embedding" became *meaning*: words/documents placed in a space where angle = relatedness.
From there the chain to the quilt is direct: distributed representations (Hinton 1986) →
neural language models (Bengio 2003) → word2vec (Mikolov 2013) → von Mises–Fisher spherical
models (Banerjee et al. 2005; Reisinger et al. 2010; Fisher's "Dispersion on a sphere," 1953,
is the vMF parent) — and the quilt's cosine/vMF estimation cells [8][13] implement the 1975
idea with 1957 arithmetic: fixed-point arrays, shift-add dot products, no divides.

The honest caveat: FORTRAN's abstraction *worked* because the machine model was still
in the compiler writers' heads. What the quilt keeps is the pre-split stance: the machine
model lives in the fabric, and "intelligence lives at the bottom" [13].

---

## 4. Where hardware split from programming — and what was lost

**The split:** 1957, FORTRAN on the IBM 704 — the first compiler good enough that assembly
programmers accepted a high-level language [20]. The 1954 report says what was intended:
machine knowledge moves into the compiler; the programmer supplies the math. The intent
succeeded so completely that within a decade the machine was invisible, and by 1978 Backus
himself was arguing the abstraction had produced languages "as complex as" the machines they
hid: "Conventional programming languages are growing ever more enormous, but not stronger…
their primitive word-at-a-time style of programming inherited from their common ancestor — the
von Neumann computer"; "The assignment statement is the von Neumann bottleneck of programming
languages"; "every feature of a von Neumann language must be spelled out in stupefying detail
in its framework" [22]. Backus's whole 1978 lecture is the confession of the split's cost:
word-at-a-time thinking, semantics coupled to state, changeable parts that cannot change.

**What was lost:** the programmer's machine model — memory maps, register allocation, timing,
word size, I/O ports, interrupt discipline. The FORTRAN-era programmers *knew* the machine
(the 704's three index registers and CAS instruction shaped the language: arithmetic IF maps
to the three-way CAS [20]); the post-split programmer doesn't, and the performance contract
moved to the compiler. The people who never lost it are the kernel/BIOS-era engineers: CP/M's
BIOS (Kildall, 1974–75) — the original hardware-abstraction layer, the machine-specific wedge
that made an OS portable across dozens of different boxes; the IBM PC BIOS (1981); device
drivers, interrupt vectors, timing loops, memory maps — all the hand-held machine knowledge
that FORTRAN moved into the compiler. And the hardware people themselves: they kept working
on the concrete side with schematics and logic, and did not get a *language* for their work
until Verilog (Goel/Moorby/Huang, Gateway Design Automation, 1983–84) and VHDL (IEEE 1076,
1987) — 27–30 years after FORTRAN — and even then "originally, Verilog was only intended to
describe and allow simulation; the automated synthesis of subsets of the language to
physically realizable structures was developed after the language had achieved widespread
usage" [23]. Verilog's infobox lineage lists FORTRAN among its influences [23]: the hardware
side finally got a language, and it inherited the split's grammar — a language that *models*
concurrency but whose modules are still structural (wires, registers, instances).

**The counter-examples (the split never hardened everywhere):** the Burroughs B5000 (1961)
put the software stack in the hardware (stack machine, descriptor-based memory, ALGOL as the
machine's native language); the CDC 6600 (1964) had 10 peripheral processors designed for the
I/O reality of timesharing; the Cray-1's vector registers were designed *for* FORTRAN loops.
In those machines the compiler and the architecture were one negotiation. The quilt's
doctrine — "the tier says how much of the model is expressed; the opcodes are the same on
every boat" [6] — is the B5000/Cray stance restated for a cellular fabric: the cell core is
the one interpreter [14]; the fabric is the machine; there is no OS above it to abstract the
machine away from the intelligence. The bottom layer is where the pre-C engineering always
lived: judgment, cycle, ledger, and array — as hardware.

---

## 5. The mapping: PLATO / RPG / COBOL / FORTRAN → quilt cells

| Pre-C concept (source) | What it was | Quilt cell concept (doc) |
|---|---|---|
| `judged` tri-state verdict — ok / anticipated-wrong / unanticipated-no (Avner 1981 §J [5]) | Judgment refused to collapse to two states; feedback differed by class | XID-MATCH verdict: match / no-match / `AMBIGUOUS` — "never a guess" (BACK-DECK-APP §2 [6]) |
| `specs` family — independent switchable judgers: nospell, noorder, nodiff (1% numeric), okcap, okextra, toler… (Avner §J [5]) | Config was per-judger switches, not program rewrite | Dials as traffic (Law 2): THRESH, MATCH_WIN, QUARANTINE, LEGAL_SET… (BACK-DECK-APP §4 [6]) |
| `synonym` / `vocabs` / `concept` — synonym tables, ignorable words, which-synonym detection (Avner §J [5]) | Aliases were data, maintained by the community, used by the matcher | ALIAS-table cell: pink≡humpy…, tote-volume corroboration of new alias rows (BACK-DECK-APP §2 [6]) |
| Judging copy pipeline — bump/put/close/open normalize the response before matching; 300-char hard bound (Avner §J [5]) | Normalization was a pipeline with a budget; matching ran on the canonical form | Thin dumb adapters + ingress normalization; any IO can enter a cell (Law 4); per-stage budgets |
| Bit-vector word matching — letter/pair/first-letter fields, Hamming distance, no strings, no search (Tenczar & Golden X-35 [3][4]) | Approximate semantic matching at fixed cost, hardware-friendly | Fixed-point cosine / vMF estimation cells; shift-add datapaths, no divides (DOCTRINE [13], ABSTRACTION-MATH [8]) |
| Algorithmic judgment over answer lists (X-5 [7]) | Judge by computation, not lookup — saves memory, is more flexible | Golden-model TBs + sby monitors; prove-by-simulation discipline (ABSTRACTION-MATH §1 [8]) |
| Session illusion — 4000 users on one CPU, Poisson arrivals, 500 µs wait, 50% idle for batch (X-5 [7]); 5 TIPS/user load budget (Jones [15]) | Asynchrony was the design; capacity was a per-user instruction budget | Async cells, no global scheduler; per-cell flit/edge budget; the tier says how much of the model is expressed (DOCTRINE [13], BACK-DECK-APP §1 [6]) |
| 1/60 s broadcast frame, NOP to idle terminals, write-only-changes (X-20, X-27 [11][12]; Bitzer OH [10]) | The heartbeat was a hardware deadline; silent cells cost nothing; only deltas traveled | `q_tick_sched` hard interlock: `tick_pend` serviced before any ingress; effect storms cannot starve the tick (SYNTHESIS Q2 [14]) |
| Plasma panel price point — 27¢/hr classroom cost, ≤$1,900 terminal budget, memory in the glass (X-5 [7]; Bitzer OH [10]) | The $-budget forced the hardware: bistable cells, no refresh memory, cheap glass | Fabric budget: quantized-by-default, multiplier-free, saturate-never-wrap — the quantization IS the algorithm (DOCTRINE [13]) |
| Shared common blocks — 1500 shared words per lesson, 150 persistent student vars (TUTOR [4]) | Multi-user presence via shared memory; identity via persistent per-user state | Cell state + QUF: state is a file; warm start restores dials, edges, schedule (DOCTRINE [13], QUF-SPEC) |
| NTU billing + site EM allotments (CDC User's Guide [16]; Avner §M [5]) | The illusion had a meter: per-message, per-128-words, per-block; site memory caps | Flit accounting; QUF as the fleet's ledger; per-site/per-cell memory allotments |
| Notesfiles / term-talk — async community with authentication (Woolley [17]) | Presence without simultaneity; records were first-class | BESTSHOT / AUDIT-CAPTAIN / NIGHT-CRON review surfaces (BACK-DECK-APP §2 [6]) |
| RPG program cycle — fixed read→calc→output→totals loop; level breaks; matching records (IBM RPG [18]) | The loop was the structure; the programmer wrote per-record code | Tick schedule in QUF; the tick is a hardware-interlocked deadline; XID-MATCH window (MATCH_WIN) as matching-record (BACK-DECK-APP §5 [6]) |
| RPG indicators 01–99 (IBM RPG [18]) | Boolean flags gate which logic acts on which record | Dial flags / THRESH / MODE selectors on cells |
| COBOL divisions + PICTURE — data described as forms; batch master+transaction update with control totals (COBOL [19]) | Ledger semantics: sequential passes, totals must balance, audit trail | Ledger-cells (`LEDGER-SCALE`), audit-cells (confirm/quarantine), night-cron batch retrain, A/B promotion as batch commit (BACK-DECK-APP §2, §5 [6]) |
| Double-entry bookkeeping — every debit has a credit; the books balance or they are wrong | Self-consistent transactional state as an invariant | Intercell contract: every effect has its ledger leg; quarantine propagates both directions down the label chain; rollback is the default verdict (BACK-DECK-APP §4 [6]) |
| FORTRAN arrays + DO — vector as math object; subscript→address done by compiler (1954 report [1]) | Memory as a mathematical object; the machine hidden behind the array | Cell arrays / ring; streaming fixed-point datapaths; the fabric keeps the machine model |
| Salton vector space model — cosine similarity for retrieval (Salton 1975 [21]) | Meaning as angle between vectors | Cosine / vMF similarity cells; spherical geometry in fixed point (DOCTRINE [13]) |
| The 1954 abstraction moment — machine knowledge "built into the FORTRAN system" (Preliminary Report [1]); Backus's 1978 recantation [22] | The compiler took the machine away from the programmer; word-at-a-time thinking remained | Intelligence at the bottom: the fabric is the machine; no OS; state is a file; the ring avoids the global-store bottleneck (DOCTRINE [13]) |
| Verilog born 1984, simulation-first, synthesis later (Verilog [23]) | Hardware got a language 27 years after FORTRAN — but it stayed structural | RTL is still schematic-adjacent; the quilt is the bottom layer, below the split (README Law 1–5) |

---

## 6. What this does (and doesn't) buy the quilt

- **It licenses the bottom layer.** Every primitive in v1 has a working 1960s–70s ancestor
  that ran on a 1 MIPS machine behind a 1260-baud link: approximate matching, tri-state
  verdicts, alias tables, fixed cycles, ledger batches, array arithmetic. None of this needs
  the software stack; all of it predates the split.
- **It names the budget.** The price-point story (X-5) and the per-user load story (Jones's
  5 TIPS; X-5's request-rate×time product) are the original fabric budgets. The quilt's
  quantization and multiplier-free doctrines are not aesthetic; they are the plasma-panel
  argument (memory in the glass) applied to LUTs.
- **It warns.** PLATO's failure was economic (the terminal never hit its price point; CDC
  priced at $50/hr [9]) and authorial (page-turners; author cost variance ×10 [7]). The
  quilt's warnings: the fabric budget must be *real* (a 12¢/hr claim without a $1,900
  terminal is a slide), and authoring ergonomics are a first-class engineering constraint
  (five opcodes, one interpreter, QUF as the only file format [13]).

---

## References

1. Backus, J.W., Herrick, H., Ziller, I. *Preliminary Report: Specifications for the IBM
   Mathematical FORmula TRANslating System, FORTRAN.* IBM Programming Research Group,
   Nov 10 1954. (CHM scan, text layer, archive.computerhistory.org 102679231.)
2. Avner, R.A., Tenczar, P. *The TUTOR Manual.* CERL Report X-4, 1970 (ERIC ED050583,
   abstract: "TUTOR is designed to transcend the difficulties of FORTRAN…").
3. Tenczar, P.J., Golden, W.M. *Spelling, Word, and Concept Recognition.* CERL Report X-35,
   1972 (ERIC ED124944, abstract).
4. "TUTOR (programming language)." Wikipedia (accessed 2026-08-29), incl. the bit-vector/
   Hamming-distance summary of Tenczar & Golden 1972, judging-block semantics, common blocks,
   corpus-wide language conversion.
5. Avner, E. *Summary of TUTOR Commands and System Variables.* CERL/PLATO Publications,
   10th ed., Aug 1981 (ERIC ED208879): answer/wrong/answerc/judge/specs/synonym/vocabs/
   concept/match/store commands, `judged` tri-state, site commands, judging-copy pipeline.
6. quilt-verilog *docs/BACK-DECK-APP.md* (2026-08-29): cell graph, alias-table, dials
   (MATCH_WIN, QUARANTINE, LEGAL_SET, PROMOTE_MARGIN), night-cron-as-tick, warm start.
7. Bitzer, D., Skaperdas, D. *The Design of an Economically Viable Large-Scale Computer-Based
   Education System.* CERL Report X-5, 1969–1973: 25–30¢/terminal-hour target, 27¢ classroom
   cost, 12¢ computer cost, ≤$1,900 terminal budget, plasma rationale, CATV economics,
   queuing model (4000 users, 500 µs E(w)), 70M-request statistics, algorithmic judging,
   "simulate turning pages" guideline.
8. quilt-verilog *docs/ABSTRACTION-MATH.md* (2026-08-29): formal-object map, sby monitors,
   golden models.
9. "PLATO (computer system)." Wikipedia (accessed 2026-08-29): ~$12,000 terminals, 950
   terminals by 1976, several thousand terminals on ~a dozen networked mainframes, CDC $50/hr
   pricing, shared-variable multiplayer, Micro-PLATO, Cyber1.
10. *Oral History of Donald L. Bitzer.* Computer History Museum, Jul 2022 (CHM Ref
    2022.0124): Owens-Illinois partnership, write-only-changes doctrine, low-bandwidth/high-
    performance rationale, plasma panel memory.
11. Stifle, J. *The PLATO IV Architecture.* CERL Report X-20, Apr 1971/rev. May 1972:
    NIU, 1008-terminal ETV channel, 1/60 s output frame, NOP-to-idle, no-refresh terminal,
    2048 chars, 126 alterable characters, site controller, 32 lines × 32 terminals.
12. Tucker, P.T. *A Large Scale Computer Terminal Output Controller.* CERL Report X-27 / MS
    thesis, Jun 1971: double-buffered 1024×20 output controller, 525-line TV raster format,
    ETV-vs-voice-grade tariff economics (<5.5¢/mile/month per terminal).
13. quilt-verilog *docs/DOCTRINE.md* (2026-08-29): llama.cpp shape, quantized-by-default,
    state-is-a-file, cellularized, five opcodes, inference everywhere.
14. quilt-verilog *docs/SYNTHESIS.md* (2026-08-29): Q2 hard-interlocked tick deadline,
    `tick_pend` front-of-queue service.
15. Jones, D.W. "PLATO Index" (homepage.divms.uiowa.edu/~jones/plato/, accessed 2026-08-29):
    1 MIPS machine, 200 users ⇒ <5 TIPS/user budget; notesfiles; TUTOR port to MODCOMP IV
    (MS thesis, 1976, UIUCDCS-R-77-868).
16. *PLATO User's Guide.* Control Data Corporation, Apr 1981 (97405900C, bitsavers):
    DSN sign-on, intersystem notesfiles, NTU billing rules, account/site management.
17. Dear, B. *The Friendly Orange Glow* (Pantheon, 2017); "PLATO Notes released 40 years ago
    today" (platohistory.org blog, 2013): Woolley's Notes, authentication, three forums.
18. "IBM RPG." Wikipedia (accessed 2026-08-29): program cycle, indicators 01–99, level
    breaks, matching records, tab-machine control-panel heritage (FARGO).
19. "COBOL." Wikipedia (accessed 2026-08-29): CODASYL 1959–60, FLOW-MATIC/COMTRAN lineage,
    four divisions, PICTURE clause, $800k programming / $600k conversion survey, batch
    processing.
20. "Fortran." Wikipedia (accessed 2026-08-29): 1954 spec, Apr 1957 compiler, 32 statement
    types incl. DIMENSION/EQUIVALENCE/arithmetic IF/FREQUENCY, Monte Carlo basic-block
    placement, 1401 63-phase in-core compiler.
21. Salton, G., Wong, A., Yang, C.S. "A Vector Space Model for Automatic Indexing." CACM
    18(11):613–620, Nov 1975. (Also: "Vector space model," Wikipedia, accessed 2026-08-29.)
22. Backus, J. "Can Programming Be Liberated from the von Neumann Style? A Functional Style
    and Its Algebra of Programs." CACM 21(8):613–641, Aug 1978 (Turing Award lecture).
23. "Verilog." Wikipedia (accessed 2026-08-29): 1983–84, Gateway Design Automation,
    simulation-first then synthesis, IEEE 1364-1995, C/FORTRAN influence.
