#!/usr/bin/env python3
"""Tests for sim/tools/tapfabric.py -- the TAP-FABRIC bridge.

Run from the repo root:
    python3 -m unittest discover -s sim/tools -p 'test_*.py'
or directly:
    python3 sim/tools/test_tapfabric.py

Covers: RTL-exact engine/cell invariants (q_hebb_edge, q_cell_core), the
D2 judgment under its OPENNESS dial, all three real MudArena log formats,
fixture replay with emergent fire, and QUF warm-start round-trip via
tools/quf.py.
"""

import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import tapfabric as tf  # noqa: E402
import quf              # noqa: E402

FIXTURE = os.path.join(_ROOT, "sim", "fixtures", "tap-session-01.jsonl")


class TestLadderEngine(unittest.TestCase):
    """q_hebb_edge.v MODE=0 semantics, bit-for-bit."""

    def test_fresh_cofire_reads_2p8(self):
        e = tf.Edge(0, 1, 0, 0)
        e.train()
        self.assertEqual(e.readout(), 256)      # SYNTHESIS weight map scale

    def test_ladder_readout_is_exact_dyadic_sum(self):
        """W-hat = 256 * sum_i c_i * 2^-i (SYNTHESIS readout scale); the
        ladder IS the dyadic staircase, so equality holds by construction
        and each half-life exactly halves an old cofire's class."""
        e = tf.Edge(0, 1, 0, 0)
        e.train()
        e.train()
        e.tick(1, 20)                           # HL=1: every tick ages a class
        # buckets = [0, 2]: both cofires now in class 1 -> 2 * 2^7
        self.assertEqual(e.readout(), 2 * 128)
        e.train()
        # buckets = [1, 2]: 1*2^8 + 2*2^7 = 512
        self.assertEqual(e.readout(), 256 + 2 * 128)
        # factor-2 envelope: an aged cofire is exactly half a fresh one
        e2 = tf.Edge(0, 1, 0, 0)
        e2.train()
        e2.tick(1, 20)                          # HL=1 again
        self.assertEqual(e2.readout(), 256 // 2)

    def test_half_life_shift_moves_class(self):
        e = tf.Edge(0, 1, 0, 0)
        e.train()
        for _ in range(48):
            e.tick(48, 20)
        self.assertEqual(e.readout(), 128)      # class aged 1: 2^-1 * 256
        e.train()
        self.assertEqual(e.readout(), 256 + 128)

    def test_bucket_saturation_sticky(self):
        e = tf.Edge(0, 1, 0, 0)
        for _ in range(300):
            e.train()
        self.assertEqual(e.buckets[0], 255)
        self.assertTrue(e.ovf)                  # sticky overflow flag
        # acc above the PW bits saturates the readout at 0xFFFF
        e.buckets[1] = 2                        # 255*256 + 2*128 = 65536
        self.assertEqual(e.readout(), 0xFFFF)


class TestHyperbolicEngine(unittest.TestCase):
    """q_hebb_edge.v MODE=1 semantics: W0/(1+W0*t/P0) within [1,4)x."""

    def test_readout_is_wh_times_256(self):
        e = tf.Edge(0, 1, 0, 0, mode=1)
        for _ in range(5):
            e.train()
        self.assertEqual(e.readout(), 5 << 8)

    def test_decay_interval_bound(self):
        p0 = 1 << 20
        w0 = 40
        e = tf.Edge(0, 1, 0, 0, mode=1)
        e.wh = w0
        decs = []
        last = w0
        for t in range(1 << 16):
            e.tick(48, 20)
            if e.wh < last:
                decs.append(t + 1)              # tick of each decrement
                last = e.wh
            if len(decs) >= 3 or e.wh == 0:
                break
        self.assertTrue(len(decs) >= 3)
        ivals = [b - a for a, b in zip(decs, decs[1:])]
        for ivl in ivals:
            exact = p0 // (w0 * w0)
            self.assertTrue(exact <= ivl < 4 * exact,
                            "interval %d outside [1,4)x exact %d"
                            % (ivl, exact))


class TestCellCore(unittest.TestCase):
    """q_cell_core.v effect/tick arithmetic."""

    def _hearing_pair(self, base=0x4000):
        hearer = tf.Cell(2, "a")
        speaker = tf.Cell(3, "b")
        hearer.link(speaker.cid, base)
        return hearer, speaker

    def test_effect_integration_exact(self):
        hearer, speaker = self._hearing_pair(base=0x4000)
        # effect() trains as part of delivery (ST_EFFT): one cofire lands
        # in bucket 0 and the POST-update weight is read back (ST_EFFR).
        w = 0x4000 + 256
        note = tf.Note(tf.KIND_GREET, 8192, "hi")
        hearer.judgment = tf.Judgment(
            [(tf.KIND_GREET, note.bucket, "land", "greet")], 7)
        hearer.effect(speaker.cid, 8192, note)
        expect = tf.sclip16(0 + ((w * 8192) >> 15))
        self.assertEqual(hearer.act, expect)

    def test_effect_saturates_never_wraps(self):
        hearer, speaker = self._hearing_pair(base=0x7F00)
        note = tf.Note(tf.KIND_GREET, 32767, "loud")
        hearer.judgment = tf.Judgment(
            [(tf.KIND_GREET, 7, "land", "loud")], 7)
        for _ in range(5):
            hearer.effect(speaker.cid, 32767, note)
        self.assertEqual(hearer.act, 32767)      # sclip16: no wrap

    def test_unknown_src_dropped(self):
        hearer, _ = self._hearing_pair()
        note = tf.Note(tf.KIND_GREET, 8192, "x")
        r = hearer.effect(99, 8192, note)        # no edge to cell 99
        self.assertIsNone(r)                     # ST_EFFT: silent drop
        self.assertEqual(hearer.act, 0)

    def test_fire_uses_preleak_act_and_sets_refractory(self):
        hearer, _ = self._hearing_pair()
        hearer.act = 20000
        hearer.dials[tf.D_THRESH] = 0x3800       # 14368
        afire = hearer.tick()
        self.assertEqual(afire, 20000)           # pre-leak value
        self.assertEqual(hearer.act, 0)          # ST_FIRE zeroes
        self.assertEqual(hearer.refr, hearer.dials[tf.D_REFR])
        hearer.act = 20000
        afire2 = hearer.tick()
        self.assertIsNone(afire2)                # refractory blocks refire

    def test_leak_arithmetic(self):
        hearer, _ = self._hearing_pair()
        hearer.dials[tf.D_THRESH] = 0x7FFF       # no fire during this test
        hearer.act = 16384
        hearer.dials[tf.D_KA] = 5
        hearer.tick()
        self.assertEqual(hearer.act, 16384 - (16384 >> 5))

    def test_negative_act_leak_floors_like_verilog(self):
        hearer, _ = self._hearing_pair()
        hearer.act = -8192
        hearer.dials[tf.D_KA] = 5
        hearer.tick()
        # >>> on negative is arithmetic (floor): -8192 - (-8192 >> 5)
        self.assertEqual(hearer.act, -8192 - (-8192 >> 5))


class TestJudgment(unittest.TestCase):
    """FOUNDATION D2 as taste: the OPENNESS dial is the bet."""

    def _j(self, openness):
        return tf.Judgment(
            [(tf.KIND_STORY, 4, "land", "story@4"),
             (tf.KIND_QUESTION, 3, "sip", "question@3")], openness)

    def test_tolerance_dial_moves_verdict(self):
        x = (tf.KIND_STORY, 5)                   # d=1 to land, d=5 to sip
        self.assertEqual(self._j(0)(x)[0], "REJECT")
        self.assertEqual(self._j(1)(x)[0], "ACCEPT")
        self.assertEqual(self._j(4)(x)[0], "ACCEPT")   # sip still outside
        # ...and wide enough tolerance honestly reports AMBIGUOUS (D2):
        self.assertEqual(self._j(7)(x)[0], "AMBIGUOUS")

    def test_kind_penalty(self):
        x = (tf.KIND_GRIPE, 4)                   # kind mismatch: d >= 3
        self.assertEqual(self._j(2)(x)[0], "REJECT")
        self.assertEqual(self._j(3)(x)[0], "ACCEPT")

    def test_ambiguous_never_guesses(self):
        # STORY@3: d=1 to land (STORY@4), d=3 to sip (QUESTION@3)
        x = (tf.KIND_STORY, 3)
        self.assertEqual(self._j(3)(x)[0], "AMBIGUOUS")
        self.assertEqual(self._j(2)(x)[0], "ACCEPT")   # only land within r

    def test_reject_cools(self):
        fab = tf.Fabric()
        fab.sit_down("a", "bar_rail")
        fab.sit_down("b", "bar_rail")
        a, b = fab.patron("a"), fab.patron("b")
        b.judgment = tf.Judgment([(tf.KIND_JOKE, 1, "land", "jokes")], 0)
        note = tf.Note(tf.KIND_STORY, 16384, "a story")
        b.link(a.cid, 0x4000)
        before = b.act
        fab.speak(a, note, target=b.cid)
        self.assertLess(b.act, before)           # REJECT integrates negative


class TestLogParsing(unittest.TestCase):
    """The three real MudArena wire formats parse; nothing chokes."""

    def test_watch_stream_line(self):
        evs = tf.parse_line(
            '{"type": "agent_update", "agent_id": "pearl", '
            '"location": "bar_rail", "action": "talk to moss", "score": 1}',
            {})
        self.assertEqual(len(evs), 1)
        self.assertEqual(evs[0].etype, "speak")
        self.assertEqual(evs[0].agent, "pearl")
        self.assertEqual(evs[0].kind, tf.KIND_GREET)

    def test_watch_start_sets_telnet_attribution(self):
        state = {}
        tf.parse_line('{"type": "watch_start", "agent_id": "heron", '
                      '"location": "corner_booth", "action": "idle", '
                      '"score": 0}', state)
        evs = tf.parse_line("> look", state)
        self.assertEqual(evs[0].etype, "look")
        self.assertEqual(evs[0].agent, "heron")

    def test_sim_tick_line_fans_out(self):
        evs = tf.parse_line(
            '{"agents": {"pearl": {"location": "bridge_table", '
            '"action": "move to bridge_table", "score": 3}, '
            '"moss": {"location": "bridge_table", "action": "idle", '
            '"score": 3}}}', {})
        self.assertEqual(len(evs), 2)
        self.assertEqual([e.etype for e in evs], ["move", "idle"])
        self.assertEqual(evs[0].location, "bridge_table")

    def test_npc_says_line(self):
        evs = tf.parse_line(
            "oldman says: 'welcome to the tap, the rail stools are for "
            "regulars'", {})
        self.assertEqual(evs[0].etype, "speak")
        self.assertEqual(evs[0].agent, "oldman")
        self.assertEqual(evs[0].kind, tf.KIND_GREET)

    def test_npc_says_line_is_speech_not_command(self):
        # regression: 'last call ...' starts with 'l' but is speech
        evs = tf.parse_line("oldman says: 'last call for the bridge table'",
                            {})
        self.assertEqual(evs[0].etype, "speak")
        self.assertNotEqual(evs[0].heat, 0)

    def test_mud_command_grammar(self):
        for line, etype in [
                ("> look", "look"),
                ("go north", "move"),
                ("take key", "unknown"),
                ("use queen with the trick", "unknown"),
                ("examine crystal_ball", "unknown")]:
            evs = tf.parse_line(line, {"watch": "pearl"})
            self.assertEqual(evs[0].etype, etype, line)

    def test_garbage_tolerated(self):
        evs = tf.parse_line("{{{ not json", {})
        self.assertEqual(evs[0].etype, "unknown")
        evs = tf.parse_line("", {})
        self.assertEqual(evs, [])
        evs = tf.parse_line("# comment", {})
        self.assertEqual(evs, [])


class TestReplay(unittest.TestCase):
    """The fixture replays with emergent fire and every verdict kind."""

    @classmethod
    def setUpClass(cls):
        cls.fab = tf.replay(FIXTURE)

    def test_cells_and_edges(self):
        names = [self.fab.cells[c].name for c in self.fab.order]
        self.assertEqual(names[0], "the-tap")    # room is cell 0
        self.assertEqual(names[1], "elephant")   # rhythm cell is cell 1
        for who in ("pearl", "moss", "heron"):
            self.assertIn(who, names)
        self.assertGreaterEqual(
            sum(len(self.fab.cells[c].edges) for c in self.fab.order), 10)

    def test_emergent_fire_happened(self):
        self.assertGreaterEqual(self.fab.fires, 1)
        self.assertTrue(any(l.startswith("t") and " FIRE " in l
                            for l in self.fab.transcript))

    def test_every_verdict_kind_seen(self):
        verdicts = [r["verdict"] for c in self.fab.cells.values()
                    for r in c.ledger]
        for v in ("ACCEPT", "REJECT", "AMBIGUOUS"):
            self.assertIn(v, verdicts, "missing verdict %s" % v)

    def test_elephant_warmth_grew_and_saw_novelty(self):
        self.assertGreater(len(self.fab.warmth_trace), 10)
        w0, w1 = self.fab.warmth_trace[0][1], self.fab.warmth_trace[-1][1]
        self.assertGreater(w1, w0)
        el = self.fab.elephant
        self.assertGreaterEqual(
            sum(1 for r in el.ledger if r["verdict"] == "steady"), 1)
        self.assertGreaterEqual(
            sum(1 for r in el.ledger if r["verdict"] == "novelty"), 1)
        self.assertEqual(self.fab.elephant.accounts.get("turns"), 0)

    def test_transcript_renders_speakers_and_dials(self):
        text = self.fab.render("fixture")
        for marker in ("SPEAK", "FIRE", "VIEW", "BIND", "arcs",
                       "elephant", "warmth"):
            self.assertIn(marker, text)
        # dial movements are rendered: act before->after
        self.assertIn("->", text)

    def test_deterministic_replay(self):
        fab2 = tf.replay(FIXTURE)
        self.assertEqual(self.fab.export_quf("x"), fab2.export_quf("x"))


class TestQufRoundTrip(unittest.TestCase):
    """State-is-a-file: the tap-room QUF verifies and warm-loads."""

    @classmethod
    def setUpClass(cls):
        cls.fab = tf.replay(FIXTURE)
        cls.data = cls.fab.export_quf("tap-session-01.jsonl")

    def test_quf_verifies(self):
        self.assertEqual(quf.verify_bytes(self.data, "tap.quf"), [])

    def test_header_carries_provenance(self):
        parsed = quf.read(self.data)
        hdr = parsed["header"]
        self.assertEqual(hdr["tap.room"], "the-tap")
        self.assertIn("elephant", hdr["tap.cellnames"].split(","))
        self.assertEqual(hdr["cell_count"], len(self.fab.order))

    def test_warm_start_restores_state(self):
        warm = self.fab.import_quf(self.data)
        self.assertEqual(len(warm.order), len(self.fab.order))
        for cid in self.fab.order:
            a, b = self.fab.cells[cid], warm.cells[cid]
            self.assertEqual(a.dials, b.dials)
            self.assertEqual(a.act, b.act)
            self.assertEqual(a.refr, b.refr)
            self.assertEqual(a.name, b.name)
            self.assertEqual(len(a.edges), len(b.edges))
            for ea, eb in zip(a.edges, b.edges):
                self.assertEqual(ea.dst, eb.dst)
                self.assertEqual(ea.base, eb.base)
                self.assertEqual(ea.buckets, eb.buckets)  # walk counts!
                self.assertEqual(ea.mode, eb.mode)

    def test_warm_start_can_continue(self):
        warm = self.fab.import_quf(self.data)
        n_ledgers = sum(len(warm.cells[c].ledger) for c in warm.order)
        a = warm.patron("pearl")
        warm.speak(a, tf.Note(tf.KIND_JOKE, 12288, "one more"))
        warm.round()
        self.assertGreater(
            sum(len(warm.cells[c].ledger) for c in warm.order), n_ledgers)

    def test_rtl_loader_profile_skips_tap_kvs(self):
        # unknown KV keys skip (QUF-SPEC §8/§9): read() already proves the
        # container parses; assert the tap.* keys are unknown-but-skippable
        # by checking every value type is defined in quf's type table.
        parsed = quf.read(self.data)
        for key, vt, _ in parsed["kv"]:
            self.assertIn(vt, quf.TYPE_NAMES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
