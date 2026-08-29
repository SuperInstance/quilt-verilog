#!/usr/bin/env python3
"""tapfabric.py -- run the Tap's bar AS a quilt cell graph (docs/TAP-FABRIC.md).

A Python bridge that maps MudArena session-log lines (the real wire formats
from ~/projects/mud-arena: watch-stream NDJSON, sim-tick NDJSON, telnet
command lines) into QUF cell ops, runs the graph through the SAME semantics
the RTL implements (q_cell_core / q_hebb_edge / q_dialfile arithmetic
mirrored bit-for-bit; file handling reuses tools/quf.py), and emits:

  OUT.quf             the tap-room QUF (dials = mood board, edges with live
                      ladder buckets = who hears whom, routing, ticks,
                      tap.* provenance KVs)
  OUT.transcript.txt  rendered transcript: which cell spoke, which cells
                      heard and with what verdict, how act/dials moved, the
                      elephant's warmth trace, each patron's arc (ledger)

Stdlib only. Python >= 3.8.

Usage:
  python3 sim/tools/tapfabric.py LOG.jsonl [--out BASE]
  python3 sim/tools/tapfabric.py --demo-cell    (RTL invariants, exit 0)

Mapping (TAP-FABRIC §1): patron = cell (J = taste, ledger = arc), room =
dial-aggregating cell, elephant = rhythm cell (JEPA: warmth fed by message
timestamps), qm_bind = sit down, qm_link = follow, qm_effect = speak,
qm_tick = round of conversation, qm_view = lurk.
"""

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.normpath(os.path.join(_HERE, "..", "..", "tools"))
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

import quf  # noqa: E402  (tools/quf.py -- QUF reference implementation)

# ------------------------------------------------------------------ consts --

PW = 16               # payload/weight width (q_cell_core PW)
NDIALS = quf.NDIALS   # 16 dials per cell (q_dialfile ND)
K_BUCKETS = 8         # ladder buckets (q_hebb_edge K)
B_BITS = 8            # bits per ladder bucket (q_hebb_edge B)
EDGES_N = 8           # edge slots per cell (q_cell_core EDGES_N, widened)

# Dial addresses (the q_dialfile.v map -- physical, untouched).
D_ETA_F, D_ETA_S, D_KF, D_KS, D_KA, D_THRESH, D_REFR, D_COSMIN = range(8)
D_P0E, D_MODE, D_HL, D_KLE, D_FLOOR, D_FTRACE, D_RQ, D_RQL = range(8, 16)

# q_dialfile.v reset defaults (what a cold cell binds with).
DIAL_DEFAULTS = [0x0800, 0x0080, 6, 12, 5, 0x6000, 4, 0x2CCD,
                 20, 0, 48, 0, 0, 0, 0, 0]

ROOM_ID, ELEPHANT_ID = 0, 1          # fixed cell ids
ROOM_NAME, ELEPHANT_NAME = "the-tap", "elephant"
PATRON_BASE_W = 8192                 # Q1.15 0.25 bind-time affinity
ROOM_BASE_W = 4096                   # the room listens softer than friends
ELEPHANT_BASE_W = 0                  # warmth storage only
TPW = 6                              # tick_period = 2^6 (QUF ticks section)

# Message kinds (the judgment's input-space kind coordinate).
KINDS = ["GREET", "JOKE", "STORY", "QUESTION", "GRIPE", "MOVE", "IDLE"]
KIND_GREET, KIND_JOKE, KIND_STORY, KIND_QUESTION, KIND_GRIPE, \
    KIND_MOVE, KIND_IDLE = range(7)
KIND_BASE_HEAT = {                   # signed Q1.15, deterministic
    KIND_GREET: 6144, KIND_JOKE: 12288, KIND_STORY: 16384,
    KIND_QUESTION: 8192, KIND_GRIPE: -12288, KIND_MOVE: 0, KIND_IDLE: 0,
}
WARM_WORDS = ("welcome", "thanks", "thank", "please", "sorry", "love",
              "warm", "good", "great", "toast", "laughs")
COOL_WORDS = ("damn", "shut", "lost", "whatever", "nah", "stupid")

TAP_SPOTS = ("bar_rail", "bridge_table", "corner_booth")
NPC_NAMES = ("oldman", "barkeep", ROOM_NAME)


def sclip16(v):
    """sclip16 from q_cell_core.v: saturate to Q1.15 full scale, never wrap."""
    return max(-32768, min(32767, v))


def sat_u16(v):
    """Unsigned u16 saturation (q_hebb_edge wfin/wout path)."""
    return max(0, min(0xFFFF, v))


def heat_bucket(heat):
    """Top 3 bits of the signed heat word -- the J feature coordinate."""
    return (heat & 0xFFFF) >> 13


def fnv1a(s):
    """Deterministic 32-bit FNV-1a -- taste derives from the patron's name."""
    h = 0x811C9DC5
    for ch in s.encode("utf-8"):
        h = ((h ^ ch) * 0x01000193) & 0xFFFFFFFF
    return h


def to_signed16(u):
    return u - 0x10000 if u >= 0x8000 else u


# ------------------------------------------------------------- edge engine --

def _msb16(v):
    """msb16 priority encode from q_hebb_edge.v (0 when v == 0)."""
    m = 0
    for j in range(PW):
        if (v >> j) & 1:
            m = j
    return m


class Edge:
    """One q_hebb_edge: both decay engines behind one interface.

    Ladder (MODE=0): K bucket counters of B bits; train increments bucket 0
    (saturating, sticky ovf); every half-life (HL ticks) the ladder shifts
    one class older; readout sum_i c_i * 2^-i placed at bit offset (K-i),
    saturating at the PW boundary. Hyperbola (MODE=1): integer wh + age;
    tick: age+1 >= max(1, P0 >> 2*msb(wh)) and wh>0 -> wh--, age=0.
    Both: w = sat_u16(base + engine_readout). Integer state only (never
    drifts).
    """

    __slots__ = ("src", "dst", "slot", "mode", "base", "buckets",
                 "hl_cnt", "wh", "age", "ovf")

    def __init__(self, src, dst, slot, base, mode=0):
        self.src = src
        self.dst = dst
        self.slot = slot
        self.mode = mode
        self.base = base
        self.buckets = [0] * K_BUCKETS
        self.hl_cnt = 0
        self.wh = 0
        self.age = 0
        self.ovf = False

    # -- commands (q_hebb_edge.v cmd 001/010/011/100) ----------------------

    def train(self, gclass=None):
        """Cofire potentiation. gclass=None is exact v1 cmd 001 (bucket 0);
        an integer class is the v2 graded train (cmd 101)."""
        if not self.mode:
            idx = 0 if gclass is None else min(gclass, K_BUCKETS - 1)
            if self.buckets[idx] >= (1 << B_BITS) - 1:
                self.ovf = True
            else:
                self.buckets[idx] += 1
        else:
            if self.wh >= (1 << PW) - 1:
                self.ovf = True
            else:
                self.wh += 1

    def tick(self, hl, p0e):
        """Advance decay one tick (cmd 010)."""
        if not self.mode:
            if self.hl_cnt + 1 >= max(1, hl):
                self.buckets[1:] = self.buckets[:-1]
                self.buckets[0] = 0
                self.hl_cnt = 0
            else:
                self.hl_cnt += 1
        else:
            ival = max(1, (1 << p0e) >> (2 * _msb16(self.wh)))
            if self.wh and (self.age + 1 >= ival):
                self.wh -= 1
                self.age = 0
            else:
                self.age += 1

    def readout(self):
        """Engine readout (cmd 011): ladder sum c_i<<(K-i) saturating above
        the PW bits; hyperbola wh*256 saturating; w = sat_u16(base + eng)."""
        if not self.mode:
            acc = 0
            for i, c in enumerate(self.buckets):
                acc += c << (K_BUCKETS - i)
            eng = 0xFFFF if acc >> PW else acc   # (|acc[AW-1:PW]) ? PW'ones
        else:
            eng = 0xFFFF if self.wh > 255 else (self.wh & 0xFF) << 8
        return sat_u16(self.base + eng)

    def record(self):
        """QUF edge record (QUF-SPEC §6.2)."""
        return {"src": self.src, "dst": self.dst, "mode": self.mode,
                "slot": self.slot, "base": self.base, "wh": self.wh,
                "age": self.age, "buckets": list(self.buckets)}


# ---------------------------------------------------------------- judgment --

class Judgment:
    """FOUNDATION D2 instantiated as taste: J = (A, r) over integer features.

    Input space X = (kind, bucket). Pseudometric d = 3*[kind mismatch] +
    |bucket diff|. Keys A carry classes ("land"/"sip"); tolerance r is the
    OPENNESS dial (COS_MIN, whole feature units). |V(x)| > 1 -> AMBIGUOUS:
    the verdict set, not a score, is the output -- never guesses.
    """

    def __init__(self, keys, openness):
        self.keys = keys                      # [(kind, bucket, cls, note)]
        self.openness = openness

    @staticmethod
    def distance(a, b):
        return 3 * (a[0] != b[0]) + abs(a[1] - b[1])

    def __call__(self, x):
        v = [(cls, note) for (k, b, cls, note) in self.keys
             if self.distance(x, (k, b)) <= self.openness]
        if not v:
            return "REJECT", "off-taste (d>%d)" % self.openness
        if len(v) > 1:
            return "AMBIGUOUS", "two keys within r -- no guess"
        return "ACCEPT", v[0][1]


def patron_taste(name):
    """Deterministic taste from the patron's name (bind-time dials)."""
    h = fnv1a(name)
    speakable = [KIND_GREET, KIND_JOKE, KIND_STORY, KIND_QUESTION, KIND_GRIPE]
    liked = speakable[h % 5]
    center = 3 + (h >> 8) % 2
    openness = 2 + (h >> 16) % 2
    keys = [(liked, center, "land", "%s@%d" % (KINDS[liked], center)),
            (KIND_QUESTION, 3, "sip", "curious-question@3")]
    return Judgment(keys, openness), liked, center


# ------------------------------------------------------------------- cell --

class Note:
    __slots__ = ("kind", "bucket", "heat", "text")

    def __init__(self, kind, heat, text):
        self.kind = kind
        self.heat = heat
        self.bucket = heat_bucket(heat)
        self.text = text


class Cell:
    """One patron / the room / the elephant: a q_cell_core + q_dialfile +
    q_hebb_edge array under the Tap overlay of TAP-FABRIC §2.

    act = buzz (patron) / VOLUME (room). THRESH = earnestness, KA =
    attention/volume decay, REFR = refractory, COS_MIN = OPENNESS (J's
    tolerance dial), HL = familiarity half-life, MODE = engine select.
    """

    def __init__(self, cid, name, kind="patron"):
        self.cid = cid
        self.name = name
        self.kind = kind                    # patron | room | elephant
        self.dials = list(DIAL_DEFAULTS)
        self.edges = []                     # hearer-owned links (qm_link)
        self.act = 0                        # signed Q1.15 register
        self.refr = 0
        self.judgment = None                # patrons only
        self.accounts = {"turns": 0, "heard": 0}
        self.ledger = []                    # the arc (D3)
        self.nonce = 0
        self.spot = None
        if kind == "patron":
            self.judgment, _, _ = patron_taste(name)
            self.dials[D_THRESH] = 0x3800   # earnestness 0.4375
            self.dials[D_COSMIN] = self.judgment.openness
        elif kind == "room":
            self.dials[D_THRESH] = 0x4800   # a room-moment takes 0.56 crowd
            self.dials[D_KA] = 4            # volume decays gently
            self.dials[D_REFR] = 3
        else:                               # elephant: cannot fire, won't
            self.dials[D_THRESH] = 0x7FFF
            self.dials[D_KF] = 2            # fast gap-EMA shift (alpha 1/4)
            self.dials[D_KS] = 4
            self.dials[D_COSMIN] = 80       # novelty window, 64ths of a tick

    # -- qm_bind (dial write) ------------------------------------------------

    def bind_dial(self, addr, value):
        self.dials[addr & 0xF] = value & 0xFFFF

    # -- qm_link ----------------------------------------------------------------

    def find_edge(self, dst):
        for e in self.edges:
            if e.dst == dst:
                return e
        return None

    def link(self, dst, base, mode=0):
        """qm_link: wire one hearer-owned edge; a full table evicts the
        coldest stool (lowest readout -- the bridge policy of §8)."""
        e = self.find_edge(dst)
        if e is not None:
            e.base = base
            return e
        if len(self.edges) >= EDGES_N:
            coldest = min(self.edges, key=lambda x: x.readout())
            self.edges.remove(coldest)
        e = Edge(self.cid, dst, len(self.edges), base, mode)
        self.edges.append(e)
        return e

    # -- qm_effect (hearer side) -------------------------------------------------

    def effect(self, src_cid, dat, note):
        """A delivered flit. RTL: integrate only if src matches a valid edge
        slot ("link before effect", ST_EFFT); train-then-integrate with the
        post-update weight readback (ST_EFFR->ST_EFFI); unknown src drops
        silently."""
        e = self.find_edge(src_cid)
        if e is None:
            return None                      # dropped (q_cell_core ST_EFFT)
        e.train()
        w = e.readout()
        verdict, vnote = "ACCEPT", "room takes everything"
        applied = dat
        if self.kind == "patron":
            verdict, vnote = self.judgment((note.kind, note.bucket))
            if verdict == "REJECT":
                applied = -(abs(dat) >> 1)   # off-taste loudness cools
            elif verdict == "AMBIGUOUS":
                applied = 0                  # no guess, no integration
        elif self.kind == "elephant":
            applied = 0                      # content-blind; rhythm only
        before = self.act
        self.act = sclip16(self.act + ((w * applied) >> 15))
        self.book([(src_cid, "heard", +1)], note, verdict, vnote)
        return {"w": w, "verdict": verdict, "vnote": vnote,
                "applied": applied, "before": before, "after": self.act}

    # -- qm_tick (one round) -------------------------------------------------------

    def tick(self):
        """One qm_tick: decay sweep over all edges, act leak, fire test.
        Exactly ST_TLEAK: the fire decision and afire use the PRE-leak act;
        on fire act := 0 and refr := REFR; otherwise act leaks
        (act -= act >>> KA) and refr drains."""
        hl = self.dials[D_HL]
        p0e = self.dials[D_P0E]
        for e in self.edges:
            e.tick(hl, p0e)
        thresh = to_signed16(self.dials[D_THRESH])
        ka = self.dials[D_KA] & 0xF
        if self.kind != "elephant" and self.act >= thresh and self.refr == 0:
            afire = self.act
            self.act = 0
            self.refr = self.dials[D_REFR]
            return afire
        self.act = sclip16(self.act - (self.act >> ka))
        if self.refr:
            self.refr -= 1
        return None

    def fanout(self):
        """Fire fanout targets (ST_FIRE): every valid edge peer."""
        return [e.dst for e in self.edges]

    # -- ledger (D3) ------------------------------------------------------------------

    def book(self, entries, note=None, verdict=None, vnote=None):
        self.nonce += 1
        rec = {"nonce": self.nonce, "entries": entries,
               "verdict": verdict, "vnote": vnote, "note": note}
        self.ledger.append(rec)
        for _, acct, d in entries:
            self.accounts[acct] = self.accounts.get(acct, 0) + d
        return rec

    # -- qm_view ------------------------------------------------------------------------

    def view(self, sel, arg=0):
        """qm_view: 0 = act, 1 = wsum(edges), 2 = dial[arg]. Fresh read."""
        if sel == 0:
            return self.act
        if sel == 1:
            return sat_u16(sum(e.readout() for e in self.edges))
        return self.dials[arg & 0xF]


# ------------------------------------------------------------------ fabric --

class Fabric:
    """The tap room as cells + links. Every event lands in the transcript
    with its dial movements; every transaction lands in a ledger."""

    def __init__(self):
        self.cells = {}
        self.order = []                     # bind order (cell ids)
        self.tick = 0
        self.transcript = []
        self.warmth_trace = []              # (tick, warmth) per speech
        self.speeches = 0                   # log-speak + fire deliveries
        self.fires = 0
        self.nonce = 0
        self._gap = {"last": None, "ef": 64, "es": 64}
        self._room_heat_sum = 0
        room = Cell(ROOM_ID, ROOM_NAME, "room")
        el = Cell(ELEPHANT_ID, ELEPHANT_NAME, "elephant")
        self.cells[ROOM_ID], self.cells[ELEPHANT_ID] = room, el
        self.order += [ROOM_ID, ELEPHANT_ID]
        # the elephant's first edge is the room: warmth storage (§5)
        el.link(ROOM_ID, ELEPHANT_BASE_W)
        self.room = room
        self.elephant = el

    # -- qm_bind (sit down) ----------------------------------------------------

    def sit_down(self, name, spot):
        cid = len(self.order)
        c = Cell(cid, name, "patron")
        self.cells[cid] = c
        self.order.append(cid)
        self.room.link(cid, ROOM_BASE_W)           # the old man links you
        self.elephant.link(cid, ELEPHANT_BASE_W)   # so do the walls
        c.link(ROOM_ID, PATRON_BASE_W)             # you can hear the room
        c.spot = spot
        self.say("BIND  %-8s sits down at %-12s cell %d (earnestness %.4f, "
                 "openness %d)" % (name, spot, cid,
                                   c.dials[D_THRESH] / 32768.0,
                                   c.dials[D_COSMIN]))
        return c

    def patron(self, name):
        for c in self.cells.values():
            if c.kind == "patron" and c.name == name:
                return c
        return None

    # -- qm_link (co-present hearing) -------------------------------------------

    def copresent_link(self, mover):
        for c in self.cells.values():
            if c.kind == "patron" and c is not mover and \
                    c.spot is not None and c.spot == mover.spot:
                if c.find_edge(mover.cid) is None:
                    c.link(mover.cid, PATRON_BASE_W)
                    self.say("LINK  %-8s and %s now hear each other (%s)"
                             % (c.name, mover.name, mover.spot))

    # -- qm_effect (speak) ---------------------------------------------------------

    def speak(self, speaker, note, target=None, why="SPEAK"):
        """A speech. The speaker's flits land on every cell that linked the
        speaker (the hearer owns the edge; mutual hearing gates
        integration -- RTL-true). 'talk to X' restricts patron hearers to X
        (room + elephant always hear: it's a bar)."""
        self.nonce += 1
        self.speeches += 1
        speaker.book([(speaker.cid, "turns", -1)], note)
        hearers = []
        for c in self.cells.values():
            if c is speaker or c.find_edge(speaker.cid) is None:
                continue
            if target is not None and c.kind == "patron" and \
                    c.cid != target and why == "SPEAK":
                continue
            r = c.effect(speaker.cid, note.heat, note)
            if r:
                hearers.append((c, r))
        warmth = self._elephant_hears()
        parts = ["%-5s %-8s ->" % (why, speaker.name)]
        for c, r in hearers:
            if c.kind == "patron":
                parts.append("%s[%s w=%.4f act %.4f->%.4f]"
                             % (c.name, r["verdict"][0], r["w"] / 32768.0,
                                r["before"] / 32768.0, r["after"] / 32768.0))
        parts.append("heat %+.4f" % (note.heat / 32768.0))
        parts.append("room-vol %.4f" % (self.room.act / 32768.0))
        parts.append("warmth %.4f" % (warmth / 65536.0))
        self.say(" ".join(parts))
        self._room_heat_sum += note.heat
        return hearers

    def fire(self, cell, afire):
        """Emergent speech from qm_tick: fanout to the cell's own peers."""
        self.fires += 1
        heat = sclip16(afire)
        note = Note(KIND_STORY, heat, "%s can't hold it" % cell.name)
        self.say("FIRE  %-8s act %.4f >= thresh %.4f, refractory clear -- "
                 "speaks to %s" % (cell.name, afire / 32768.0,
                                   cell.dials[D_THRESH] / 32768.0,
                                   [self.cells[d].name
                                    for d in cell.fanout()]))
        self.speak(cell, note, target=None, why="FIRE")

    # -- the elephant (§5: JEPA as a dial cell) --------------------------------------

    def _elephant_hears(self):
        """Content-blind rhythm cell: all-integer gap EMAs (fast/slow, in
        64ths of a tick), residual eps = actual - predicted, ladder train
        only inside the novelty window. Warmth = qm_view(1) = wsum of its
        edges (the room edge carries the rhythm mass; cofire mass from
        hearing patrons rides the other slots)."""
        el = self.elephant
        gap = 1 if self._gap["last"] is None else \
            max(1, self.tick - self._gap["last"])
        self._gap["last"] = self.tick
        g64 = gap << 6
        kf, ks = el.dials[D_KF] & 0xF, el.dials[D_KS] & 0xF
        ef, es = self._gap["ef"], self._gap["es"]
        eps = g64 - ef
        self._gap["ef"] = ef + ((g64 - ef) >> kf)
        self._gap["es"] = es + ((g64 - es) >> ks)
        window = el.dials[D_COSMIN]
        e_room = el.find_edge(ROOM_ID)
        if abs(eps) <= window and e_room is not None:
            e_room.train()
            verdict = "steady"
        else:
            verdict = "novelty"
        el.book([], Note(KIND_IDLE, 0, "gap"), verdict,
                "pred %.2ft act %dt eps %d/64" % (self._gap["ef"] / 64.0,
                                                  gap, eps))
        warmth = el.view(1)
        self.warmth_trace.append((self.tick, warmth))
        return warmth

    # -- qm_tick (a round of conversation) ---------------------------------------------

    def round(self):
        """One qm_tick for every cell (one log line = one tick, the CPU
        fallback's 1 s cadence). Fires are collected and delivered at the
        end of the round (one legal serialization of ring delivery)."""
        self.tick += 1
        fired = []
        for cid in self.order:
            cell = self.cells[cid]
            afire = cell.tick()
            if afire is not None:
                fired.append((cell, afire))
        # room mood binding (the dial-aggregating cell, §2): fast EMA of the
        # round's signed message heat, integer shift, stored as Q1.15.
        mood = to_signed16(self.room.dials[D_ETA_F])
        mood = sclip16(mood + ((self._room_heat_sum - mood) >> 2))
        self.room.dials[D_ETA_F] = mood & 0xFFFF
        self._room_heat_sum = 0
        for cell, afire in fired:
            self.fire(cell, afire)
        return fired

    # -- qm_view (lurk) -------------------------------------------------------------------

    def lurk(self, who, cell=None):
        cell = cell or self.room
        warmth = self.elephant.view(1)
        mood = to_signed16(cell.dials[D_ETA_F]) / 32768.0
        line = ("VIEW  %-8s lurks %s: volume %.4f mood %+.4f warmth %.4f "
                "(tick %d)" % (who.name, cell.name, cell.act / 32768.0,
                               mood, warmth / 65536.0, self.tick))
        self.say(line)
        who.book([], Note(KIND_IDLE, 0, "lurk"), "VIEW", line)
        return line

    # -- transcript -------------------------------------------------------------------------

    def say(self, line):
        self.transcript.append("t%03d  %s" % (self.tick, line))

    # -- QUF out/in (state-is-a-file) ---------------------------------------------------------

    def export_quf(self, source=""):
        # tap.* extras are comma-separated string KVs (QUF-SPEC §8
        # extensibility; strings are the portable extra type -- quf.py's
        # writer currently rejects array-valued extras).
        names = ",".join(self.cells[c].name[:31] for c in self.order)
        doc = {
            "header": {
                "quf.version": "tapfabric.py 1.0",
                "edge.k": K_BUCKETS,
                "tick_period": 1 << TPW,
                "tap.room": ROOM_NAME,
                "tap.source": source,
                "tap.cellnames": names,
                "tap.act": ",".join(str(self.cells[c].act & 0xFFFF)
                                     for c in self.order),
                "tap.refr": ",".join(str(self.cells[c].refr & 0xFFFF)
                                     for c in self.order),
            },
            "dials": [list(self.cells[c].dials) for c in self.order],
            "edges": [self.cells[c].edges[i].record()
                      for c in self.order
                      for i in range(len(self.cells[c].edges))],
            "routing": [{"dst": c, "via": c} for c in self.order],
            "ticksched": {"tpw": TPW,
                          "phases": [(c * 3) & 0xFFFF for c in self.order]},
        }
        return quf.build(doc)

    def import_quf(self, buf):
        """Warm start: restore dials, edges (ladder walk counts included),
        routing, ticks and the tap.* KVs. The Python path is the full-state
        path (QUF-SPEC §9); the RTL loader profile would re-train instead."""
        parsed = quf.read(buf)
        dec = quf.decode_sections(parsed)
        hdr = parsed["header"]
        names = [n for n in hdr.get("tap.cellnames", "").split(",") if n]
        acts = [int(x) for x in hdr.get("tap.act", "").split(",") if x]
        refrs = [int(x) for x in hdr.get("tap.refr", "").split(",") if x]
        f = Fabric.__new__(Fabric)
        f.cells, f.order, f.tick, f.transcript = {}, [], 0, []
        f.warmth_trace, f.speeches, f.fires, f.nonce = [], 0, 0, 0
        f._gap = {"last": None, "ef": 64, "es": 64}
        f._room_heat_sum = 0
        for row, name in zip(dec["dials"], names):
            kind = ("room" if name == ROOM_NAME else
                    "elephant" if name == ELEPHANT_NAME else "patron")
            c = Cell(len(f.order), name, kind)
            c.dials = list(row)
            if kind == "patron":
                c.judgment, _, _ = patron_taste(name)
            f.cells[c.cid] = c
            f.order.append(c.cid)
        for rec in dec["edges"]:
            c = f.cells[rec["src"]]
            e = Edge(rec["src"], rec["dst"], rec["slot"], rec["base"],
                     rec["mode"])
            e.buckets = list(rec["buckets"])
            e.wh, e.age = rec["wh"], rec["age"]
            c.edges.append(e)
        for cid, act in zip(f.order, acts):
            f.cells[cid].act = to_signed16(act & 0xFFFF)
        for cid, refr in zip(f.order, refrs):
            f.cells[cid].refr = refr & 0xFFFF
        f.room = f.cells[ROOM_ID]
        f.elephant = f.cells[ELEPHANT_ID]
        return f

    def render(self, source):
        out = []
        out.append("=== THE TAP, AS A QUILT -- replay of %s ===" % source)
        out.append("cells: %s" % ", ".join(
            "%s=%d" % (self.cells[c].name, c) for c in self.order))
        out.append("dials: volume/decay=KA(4) earnestness=THRESH(5) "
                   "refr=REFR(6) openness=COS_MIN(7) mood=ETA_F(0) "
                   "familiarity-halflife=HL(10)")
        out.append("")
        out.extend(self.transcript)
        out.append("")
        out.append("--- elephant (JEPA rhythm cell) ---")
        w0 = self.warmth_trace[0][1] if self.warmth_trace else 0
        w1 = self.warmth_trace[-1][1] if self.warmth_trace else 0
        el = self.elephant
        steady = sum(1 for r in el.ledger if r["verdict"] == "steady")
        novel = sum(1 for r in el.ledger if r["verdict"] == "novelty")
        out.append("warmth %.4f -> %.4f over %d messages "
                   "(steady-gap trains %d, novelty breaks %d; last %s)"
                   % (w0 / 65536.0, w1 / 65536.0, len(self.warmth_trace),
                      steady, novel,
                      el.ledger[-1]["vnote"] if el.ledger else "-"))
        out.append("")
        out.append("--- arcs (ledgers, D3) ---")
        for cid in self.order:
            c = self.cells[cid]
            acc = sum(1 for r in c.ledger if r["verdict"] == "ACCEPT")
            rej = sum(1 for r in c.ledger if r["verdict"] == "REJECT")
            amb = sum(1 for r in c.ledger if r["verdict"] == "AMBIGUOUS")
            out.append("%-10s turns %d heard %d | ACCEPT %d REJECT %d "
                       "AMBIG %d | %s %+.4f"
                       % (c.name, -c.accounts.get("turns", 0),
                          c.accounts.get("heard", 0), acc, rej, amb,
                          "volume" if c.kind == "room" else
                          "warmth" if c.kind == "elephant" else "buzz",
                          (c.view(1) / 65536.0 if c.kind == "elephant"
                           else c.act / 32768.0)))
        out.append("")
        out.append("fires (emergent speech): %d   speeches (log): %d   "
                   "ticks: %d" % (self.fires, self.speeches - self.fires,
                                  self.tick))
        out.append("state-is-a-file: this room warm-loads from the .quf "
                   "beside this transcript, buckets and all.")
        return "\n".join(out) + "\n"


# ------------------------------------------------------------- log parsing --

_SAYS_RE = re.compile(r"^([A-Za-z][\w -]*?) says: '(.*)'$")
_CMD_RE = re.compile(r"^(?:>\s*)?(.+)$")
_TARGET_RE = re.compile(
    r"^(?:talks?|tells?|asks?|thanks?)(?: to| with)? ([A-Za-z]+)\b")


# First words of the commands.py verb grammar (mud_arena/commands.py):
# the telnet line's first word decides whether it is a command at all.
_CMD_FIRST = frozenset((
    "look", "l", "inventory", "i", "inv", "help", "quit", "exit", "q",
    "examine", "x", "inspect", "take", "get", "pick", "grab", "drop",
    "use", "go", "move", "walk", "run", "head",
    "north", "south", "east", "west", "n", "s", "e", "w", "ne", "nw",
    "se", "sw", "up", "down", "in", "out",
))
_LOOK_FIRST = frozenset(("look", "l"))
_MOVE_FIRST = frozenset(("go", "move", "walk", "run", "head", "north",
                         "south", "east", "west", "n", "s", "e", "w",
                         "ne", "nw", "se", "sw", "up", "down", "in",
                         "out"))


def speech_heat(t):
    """Speech kind + signed Q1.15 heat from action text (integer-only)."""
    if ("thank" in t or "welcome" in t or t.startswith("talk") or
            t.startswith("hello") or t.startswith("hi ")):
        kind = KIND_GREET
    elif "gripe" in t or "damn" in t or "shut" in t:
        kind = KIND_GRIPE
    elif t.startswith("ask") or t.endswith("?") or " why " in t:
        kind = KIND_QUESTION
    elif "story" in t or "tale" in t or " about " in t:
        kind = KIND_STORY
    elif "joke" in t or "laughs" in t or "funny" in t:
        kind = KIND_JOKE
    else:
        kind = KIND_GREET
    heat = KIND_BASE_HEAT[kind]
    heat += 2048 * sum(1 for w in WARM_WORDS if w in t)
    heat -= 2048 * sum(1 for w in COOL_WORDS if w in t)
    return kind, sclip16(heat)


def classify_action(text):
    """Kind + signed Q1.15 heat from an action string -- deterministic,
    integer-only (TAP-FABRIC 6.1). Returns (kind|'LOOK'|'CMD', heat).
    The command/move decision uses the commands.py first-word grammar, so
    an NPC saying 'last call ...' is speech, not a look."""
    t = text.lower().strip()
    words = t.split()
    first = words[0] if words else ""
    if t.startswith("move to") or t in TAP_SPOTS or first in _MOVE_FIRST:
        return KIND_MOVE, 0
    if first in _LOOK_FIRST:
        return "LOOK", 0
    if first in _CMD_FIRST:
        return "CMD", 0
    if t.startswith("idle"):
        return KIND_IDLE, 0
    return speech_heat(t)


class LogEvent:
    __slots__ = ("etype", "agent", "location", "action", "kind", "heat")

    def __init__(self, etype, agent=None, location=None, action=None,
                 kind=None, heat=0):
        self.etype = etype          # bind|move|speak|look|idle|unknown
        self.agent = agent
        self.location = location
        self.action = action
        self.kind = kind
        self.heat = heat


def _action_event(agent, action, location):
    kind, heat = classify_action(action)
    if kind == KIND_MOVE:
        dest = location
        if " to " in (action or ""):
            dest = action.split(" to ")[-1].strip() or location
        return LogEvent("move", agent=agent, location=dest, action=action)
    if kind == "LOOK":
        return LogEvent("look", agent=agent, action=action)
    if kind == "CMD":
        return LogEvent("unknown", agent=agent, action=action)
    if kind == KIND_IDLE:
        return LogEvent("idle", agent=agent, location=location,
                        action=action)
    return LogEvent("speak", agent=agent, location=location, action=action,
                    kind=kind, heat=heat)


def parse_line(line, state):
    """Parse one real-format MudArena log line.

    Returns a list of LogEvents (usually 0 or 1; sim-tick lines fan out to
    one event per agent). Formats, exactly as they exist in the repo:
      * watch NDJSON  {"type": "agent_update"|"watch_start", "agent_id",
                       "location", "action", "score"}  (server.py
                       _notify_watchers / watch_start payload)
      * sim-tick NDJSON  {"agents": {aid: {"location","action","score"}}}
                       (server.py _read_stdout / CPUFallbackSimulator)
      * telnet text  "> command" or bare command lines (commands.py grammar,
                       attributed to the current watch agent) and NPC replies
                       "<npc> says: '...'" (agent.py _do_talk shape)
    Blank lines and comments are skipped; anything unparseable is 'unknown'
    -- the parser never chokes.
    """
    s = line.strip()
    if not s or s.startswith("#"):
        return []
    if s.startswith("{"):
        try:
            obj = json.loads(s)
        except ValueError:
            return [LogEvent("unknown", action=s)]   # never choke
        if not isinstance(obj, dict):
            return [LogEvent("unknown", action=s)]
        if obj.get("type") in ("agent_update", "watch_start"):
            state["watch"] = obj.get("agent_id") or state.get("watch")
            return [_action_event(obj["agent_id"], obj.get("action", "idle"),
                                  obj.get("location"))]
        if "agents" in obj:
            return [_action_event(aid, a.get("action", "idle"),
                                  a.get("location"))
                    for aid, a in obj["agents"].items()]
        return [LogEvent("unknown", text=None) if False else
                LogEvent("unknown", action=s)]
    m = _SAYS_RE.match(s)
    if m:
        # an NPC says-line is always speech (agent.py _do_talk shape)
        kind, heat = speech_heat(m.group(2).lower())
        return [LogEvent("speak", agent=m.group(1).strip().replace(" ", "_"),
                         action=m.group(2), kind=kind, heat=heat)]
    m = _CMD_RE.match(s)
    if m:
        who = state.get("watch") or "oldman"
        return [_action_event(who, m.group(1).strip(), None)]
    return [LogEvent("unknown", action=s)]


def _apply(fab, ev):
    """One log event -> cell ops (TAP-FABRIC §6.1), then one round."""
    if ev.etype == "speak":
        speaker = fab.patron(ev.agent)
        if speaker is None:
            if ev.agent in NPC_NAMES:
                speaker = fab.room          # the old man / the room speaks
            else:
                speaker = fab.sit_down(ev.agent, "bar_rail")
        target = None
        m = _TARGET_RE.match((ev.action or "").lower())
        if m:
            tgt = fab.patron(m.group(1))
            if tgt is not None and tgt is not speaker:
                target = tgt.cid
                # you hear who talks to you (link before effect)
                if tgt.find_edge(speaker.cid) is None:
                    tgt.link(speaker.cid, PATRON_BASE_W)
        fab.speak(speaker, Note(ev.kind, ev.heat, ev.action), target=target)
    elif ev.etype == "move":
        who = fab.patron(ev.agent)
        if who is None:
            who = fab.sit_down(ev.agent, ev.location or "bar_rail")
        else:
            who.spot = ev.location or who.spot
            fab.copresent_link(who)
    elif ev.etype == "look":
        who = fab.patron(ev.agent) or fab.sit_down(ev.agent, "bar_rail")
        fab.lurk(who)
    elif ev.etype == "idle":
        if ev.location and fab.patron(ev.agent) is None:
            fab.sit_down(ev.agent, ev.location)
    # 'unknown' (take/use/deal/...): tolerated, booked as nothing
    fab.round()


def replay(path):
    """Replay a session log through the fabric: parse -> ops -> one tick."""
    fab = Fabric()
    state = {"watch": None}
    with open(path) as f:
        for raw in f:
            for ev in parse_line(raw, state):
                _apply(fab, ev)
    return fab


# ------------------------------------------------------------------ checks --

def demo_cell():
    """RTL invariants the bridge must hold (all asserted in tests too)."""
    e = Edge(0, 1, 0, 0)
    e.train()
    assert e.readout() == 256, "fresh cofire reads 2^K (SYNTHESIS scale)"
    for _ in range(48):
        e.tick(48, 20)
    e.train()
    assert e.readout() == 256 + 128, "post-half-life cofire lands class 1"
    h = Edge(0, 1, 0, 0, mode=1)
    for _ in range(3):
        h.train()
    assert h.readout() == 3 << 8, "hyperbola reads wh*256"
    print("tapfabric demo-cell PASS (ladder/hyperbola scales)")


# --------------------------------------------------------------------- CLI --

def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="tapfabric.py",
        description="run the Tap's bar as a quilt cell graph "
                    "(docs/TAP-FABRIC.md)")
    ap.add_argument("log", nargs="?", help="MudArena session log (.jsonl)")
    ap.add_argument("--out", default="tap_room",
                    help="output base (writes BASE.quf, BASE.transcript.txt)")
    ap.add_argument("--demo-cell", action="store_true",
                    help="run the RTL invariant demo and exit")
    args = ap.parse_args(argv)

    if args.demo_cell:
        demo_cell()
        return 0
    if not args.log:
        ap.error("log path required (or --demo-cell)")

    fab = replay(args.log)
    data = fab.export_quf(source=os.path.basename(args.log))
    issues = quf.verify_bytes(data, args.out + ".quf")
    assert not issues, issues
    with open(args.out + ".quf", "wb") as f:
        f.write(data)
    with open(args.out + ".transcript.txt", "w") as f:
        f.write(fab.render(os.path.basename(args.log)))
    print("wrote %s.quf (%d bytes, quf.verify clean) + %s.transcript.txt"
          % (args.out, len(data), args.out))
    print("cells %d, edges %d, speeches %d (fires %d), ticks %d, "
          "warmth %.4f"
          % (len(fab.order),
             sum(len(fab.cells[c].edges) for c in fab.order),
             fab.speeches, fab.fires, fab.tick,
             fab.elephant.view(1) / 65536.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
