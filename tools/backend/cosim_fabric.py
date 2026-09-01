#!/usr/bin/env python3
"""cosim_fabric.py -- FABRIC-LEVEL differential cosim: Python fabric
model vs the real q_fabric_top RTL (iverilog) on ONE shared stimulus
program (backend lane; the §10/B6 artifact at small scale, NCELL=2).

This is the harness THE-BREAKDOWN §10 specified: the same flit stream
feeds the Python model and the RTL ring; every egress flit (ACK/NAK
responses, EXTID echoes, fire fanout to the host) is diffed
field-for-field, per pacing window, N seeded programs + directed
corners.

Honest scoping (what is measured vs modeled):
  * Tick TIMING is scheduler fact, not a seam under test. The TB
    samples each cell's SERVICED-tick count at every grant (the Q2
    interlock merges tick pulses that arrive mid-service, so serviced
    counts -- not pulse counts -- are the truth); the model applies
    exactly those measured per-cell tick deltas before replaying each
    op. What the diff then proves bit-exact: op semantics, ring
    routing/delivery, response/echo/fire egress, under the real ring's
    interleaving -- the serialization seam the invariant-level checks
    could not see.
  * Same-tick fire fanout to EXTID egresses in ring-position order
    (cell 0 before cell 1; a transit flit blocks a node's injection,
    so an upstream fire cannot be overtaken by a downstream one).
  * Ops are atomic per the Q2 interlock (tick_pend serviced at IDLE
    before any new ingress); the pacing contract (settle + quiescence
    per flit) keeps every response/fire inside its own window.

The cell arithmetic (Engine: train/tick/readout, sclip16 integration,
fire test) is imported from cosim_cell.py, which proved it bit-exact
against the q_cell RTL on 68+128 programs; this lane composes those
cells into the fabric and checks the ring.

Output: tb/run/cosim_fabric_prog.hex (program) and
tb/run/cosim_fabric_trace.txt (RTL trace). Exit 1 on any mismatch.
Stdlib only.
"""
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cosim_cell import Engine, POR_DIALS, sclip16, sat_u16, to_signed16

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
OUT = os.path.join(_ROOT, "tb", "run")

NCELL = 2
EDGES_N = 4
EXTID = 0xF
OP_BIND, OP_LINK, OP_EFF, OP_VIEW, OP_TICK, OP_ACK, OP_NAK = range(7)


class FabricCell:
    """one q_cell on the ring: FSM semantics + dialfile + engines."""

    def __init__(self):
        self.dials = list(POR_DIALS)
        self.edges = [None] * EDGES_N
        self.peers = [0] * EDGES_N
        self.act = 0                 # signed
        self.refr = 0
        self.cell_id = 0
        self.bound = False
        self.ftrace = 0              # q_echo_gate trace (dial-13 probe)

    def d(self, i):
        return self.dials[i]

    def host_op(self, op, src, a0, a1, a2, dat=0):
        """one delivered host flit -> (egress-flit-or-None, fanout-list)

        fanout: [(dst, dat)] effects to peers (delivered, not egress)
        """
        fanout = []
        if not self.bound:
            if op == OP_BIND:
                self.cell_id = a0 & 0xF
                self.bound = True
                return self._ack(src, a2, 0), fanout
            return self._nak(src, a2), fanout
        if op == OP_BIND:
            addr = a0 & 0xF
            if addr != 13:                 # probe alias: ignored
                self.dials[addr] = a1 & 0xFFFF
            return self._ack(src, a2, 0), fanout
        if op == OP_LINK:
            slot = a0 & 0x3
            if self.edges[slot] is None:
                self.edges[slot] = Engine()
            self.edges[slot].base = a1 & 0xFFFF
            self.peers[slot] = src & 0xF
            return self._ack(src, a2, 0), fanout
        if op == OP_EFF:
            slot = self._find(src)
            if slot is not None:
                mode = self.d(9) & 1
                e = self.edges[slot]
                e.train(mode)
                w = e.readout(mode)
                prod = w * to_signed16(dat & 0xFFFF)
                self.act = sclip16(self.act + (prod >> 15))
            return None, fanout            # effects are silent
        if op == OP_VIEW:
            sel = a0 & 0x3
            if sel == 0:
                return self._ack(src, a2, self.act & 0xFFFF), fanout
            if sel == 1:
                mode = self.d(9) & 1
                wacc = sum(e.readout(mode) for e in self.edges
                           if e is not None)
                return self._ack(src, a2, sat_u16(wacc)), fanout
            if sel == 2:
                addr = a1 & 0xF
                # dial 13 is the read-only live echo-trace probe
                val = self.ftrace if addr == 13 else self.d(addr)
                return self._ack(src, a2, val), fanout
            return self._nak(src, a2), fanout        # sel 3: v1 NAK
        # OP_ACK / OP_NAK / OP_TICK delivered to a cell: consumed, no
        # action, no response
        return None, fanout

    def deliver_effect(self, src, dat):
        """a peer's fire fanout (or a host effect) lands in this cell"""
        self.host_op(OP_EFF, src, 0, 0, 0, dat)

    def host_effect(self, src, dat):
        return self.host_op(OP_EFF, src, 0, 0, 0, dat)

    def tick(self):
        """one serviced tick -> fires [(dst, dat)] in slot order"""
        mode = self.d(9) & 1
        hl = self.d(10)
        p0e = self.d(8) & 0x1F
        for e in self.edges:
            if e is not None:
                e.tick(mode, hl, p0e)
        thresh = to_signed16(self.d(5))
        ka = self.d(4) & 0xF
        fires = []
        if self.act >= thresh and self.refr == 0:
            afire = self.act & 0xFFFF
            fires = [(self.peers[i], afire) for i in range(EDGES_N)
                     if self.edges[i] is not None]
            self.act = 0
            self.refr = self.d(6) & 0xFFFF
            # echo trace: fire refills to max one cycle AFTER the leak
            # strobe of this same tick service (fire wins by construction)
            self.ftrace = 0xFFFF
        else:
            self.act = sclip16(self.act - (self.act >> ka))
            if self.refr:
                self.refr -= 1
            # echo trace leak with deadband snap (q_echo_gate)
            kle = self.d(11) & 0xF
            floor = self.d(12) & 0xFFFF
            fleak = self.ftrace - (self.ftrace >> kle)
            if (fleak <= floor) or (fleak <= 1) or (fleak >= self.ftrace):
                self.ftrace = 0
            else:
                self.ftrace = fleak
        return fires

    def _find(self, src):
        for i in range(EDGES_N):
            if self.edges[i] is not None and self.peers[i] == (src & 0xF):
                return i
        return None

    def _ack(self, dst, a2, dat):
        return (OP_ACK, self.cell_id, dst, 0, 0, a2 & 0xFFFF, dat & 0xFFFF)

    def _nak(self, dst, a2):
        return (OP_NAK, self.cell_id, dst, 0, 0, a2 & 0xFFFF, 0)


class FabricModel:
    def __init__(self):
        self.cells = [FabricCell() for _ in range(NCELL)]

    def apply_ticks(self, counts, egress, widx):
        """counts[i] MORE serviced ticks for cell i (measured); fires
        fan out immediately: peer==EXTID egresses (ring-position order),
        peer cells integrate act."""
        counts = list(counts)
        for _ in range(max(counts)):
            batch = []
            for c, cell in enumerate(self.cells):
                if counts[c] > 0:
                    counts[c] -= 1
                    batch.append((c, cell.tick()))
            # same-tick EXTID fires egress in ring-position order;
            # fire-to-cell effects integrate (order-independent: act
            # adds commute, trains hit distinct edges by src)
            for c, fires in batch:
                for dst, dat in fires:
                    if dst == EXTID:
                        egress.append((widx, OP_EFF, self.cells[c].cell_id,
                                       EXTID, 0, 0, 0, dat))
            for c, fires in batch:
                for dst, dat in fires:
                    if dst < NCELL:
                        self.cells[dst].deliver_effect(
                            self.cells[c].cell_id, dat)
                    # dst in NCELL..14: nonexistent node -- flit circles
                    # the ring forever in v1 (no TTL); the generator
                    # never links such peers, asserted at gen time.

    def op(self, flit, egress, widx):
        op, src, dst, a0, a1, a2, dat = flit
        if dst == EXTID:
            # echo: injected by the io node, circles, egresses as-is
            egress.append((widx, op, src, dst, a0, a1, a2, dat))
            return
        if dst >= NCELL:
            return                          # generator never does this
        if op == OP_EFF:
            self.cells[dst].host_effect(src, dat)
            return                          # silent
        resp, _ = self.cells[dst].host_op(op, src, a0, a1, a2, dat)
        if resp is not None:
            rdst = resp[2]
            if rdst == EXTID:
                egress.append((widx,) + resp)
            elif rdst < NCELL:
                # response routed to a peer cell (link flit claimed a
                # cell src): delivered, consumed silently (OP_ACK/NAK
                # to a bound cell = no action; to an unbound cell = NAK
                # back toward... its lr_src -- modeled as consumed here;
                # the generator only links bound cells, and the NAK's
                # dst is a bound cell in every generated program)
                pass


# ------------------------------------------------------------- program --

def gen_program(rng, nops):
    """host flits as (op,src,dst,a0,a1,a2,dat,wait)"""
    prog = []
    prog.append((OP_BIND, EXTID, 0, 0, 0, 1, 0, 200))
    prog.append((OP_BIND, EXTID, 1, 1, 0, 2, 0, 200))
    bound_dials = [set(), set()]
    linked = [set(), set()]                 # cells with >=1 edge
    a2 = 3
    for _ in range(nops):
        a2 = (a2 + 1) & 0xFFFF
        r = rng.random()
        wait = rng.choice([64, 64, 128, 300, 800,
                           rng.randrange(64, 3000),
                           rng.randrange(15000, 40000)])
        if r < 0.12:
            c = rng.randrange(NCELL)
            which = rng.choice([4, 5, 6, 8, 9, 10, 13, 7, 11])
            val = {4: rng.randrange(0, 16), 5: rng.choice(
                [0, 1, 0x1000, 0x3800, 0x6000, 0x7FFF, 0x8000, 0xC000]),
                6: rng.randrange(0, 6), 8: rng.randrange(0, 24),
                9: rng.randrange(0, 2), 10: rng.choice([1, 2, 3, 4, 8, 64]),
                13: 0xBEEF, 7: rng.randrange(0, 4),
                11: rng.randrange(0, 4)}[which]
            prog.append((OP_BIND, EXTID, c, which, val, a2, 0, wait))
            bound_dials[c].add(which)
        elif r < 0.28:
            c = rng.randrange(NCELL)
            slot = rng.randrange(EDGES_N)
            peer = rng.choice([0, 1, EXTID])
            base = rng.choice([0, 4096, 8192, 0xF000, rng.randrange(0x10000)])
            prog.append((OP_LINK, peer, c, slot, base, a2, 0, wait))
            linked[c].add(slot)
        elif r < 0.60:
            if rng.random() < 0.15:
                prog.append((OP_EFF, EXTID, EXTID, 0, 0, a2,
                             rng.randrange(0x10000), wait))   # echo
            else:
                c = rng.randrange(NCELL)
                peer = rng.choice([0, 1])
                dat = rng.choice([0, 1, 0x7FFF, 0x8000, 0xFFFF, 0x4000,
                                  rng.randrange(0x10000)])
                prog.append((OP_EFF, peer, c, 0, 0, a2, dat, wait))
        elif r < 0.78:
            c = rng.randrange(NCELL)
            sel = rng.choice([0, 1, 2, 2, 3])
            a1 = rng.randrange(16) if sel == 2 else 0
            prog.append((OP_VIEW, EXTID, c, sel, a1, a2, 0, wait))
        else:
            # long waits let scheduler ticks (and fires) land
            prog.append((OP_VIEW, EXTID, rng.randrange(NCELL), 0, 0,
                         a2, 0, rng.randrange(15000, 50000)))
    return prog


def gen_directed():
    progs = []
    # D1: fire to host: cell0 links EXTID as peer, low thresh, hammer
    p = [(OP_BIND, EXTID, 0, 0, 0, 1, 0, 200),
         (OP_BIND, EXTID, 0, 5, 0x0100, 2, 0, 100),
         (OP_BIND, EXTID, 0, 6, 3, 3, 0, 100),
         (OP_LINK, EXTID, 0, 0, 0x2000, 4, 0, 200),
         (OP_LINK, EXTID, 0, 1, 0x2000, 5, 0, 200),
         (OP_EFF, EXTID, 0, 0, 0, 6, 0x7FFF, 400),
         (OP_VIEW, EXTID, 0, 0, 0, 7, 0, 30000),
         (OP_VIEW, EXTID, 0, 1, 0, 8, 0, 30000),
         (OP_VIEW, EXTID, 0, 0, 0, 9, 0, 40000)]
    progs.append(p)
    # D2: chained fire: cell0 peer=cell1; cell1 thresh low, fires to host
    p = [(OP_BIND, EXTID, 0, 0, 0, 1, 0, 200),
         (OP_BIND, EXTID, 1, 1, 0, 2, 0, 200),
         (OP_BIND, EXTID, 0, 5, 0x4000, 3, 0, 100),
         (OP_BIND, EXTID, 1, 5, 0x0800, 4, 0, 100),
         (OP_LINK, 1, 0, 0, 0x4000, 5, 0, 200),
         (OP_LINK, EXTID, 1, 0, 0x4000, 6, 0, 200),
         (OP_EFF, 1, 0, 0, 0, 7, 0x7FFF, 400),
         (OP_VIEW, EXTID, 0, 0, 0, 8, 0, 30000),
         (OP_VIEW, EXTID, 1, 0, 0, 9, 0, 40000)]
    progs.append(p)
    # D3: nak paths: ops to unbound... both cells bind first, so probe
    # dial13 ignore + view sel3 NAK + unknown-src effect drop + echo
    p = [(OP_BIND, EXTID, 0, 0, 0, 1, 0, 200),
         (OP_BIND, EXTID, 1, 1, 0, 2, 0, 200),
         (OP_BIND, EXTID, 0, 13, 0xBEEF, 3, 0, 200),
         (OP_VIEW, EXTID, 0, 2, 13, 4, 0, 300),
         (OP_VIEW, EXTID, 0, 3, 0, 5, 0, 300),
         (OP_EFF, 1, 0, 0, 0, 6, 0x7FFF, 300),      # no edge: drop
         (OP_VIEW, EXTID, 0, 0, 0, 7, 0, 300),
         (OP_EFF, EXTID, EXTID, 0, 0, 8, 0xABCD, 300),
         (OP_EFF, 1, 0, 0, 0, 9, 0x7FFF, 20000)]    # drop + tick window
    progs.append(p)
    # D4: re-link same slot keeps bucket state; base changes readback
    p = [(OP_BIND, EXTID, 0, 0, 0, 1, 0, 200),
         (OP_LINK, 1, 0, 2, 0x1000, 2, 0, 200),
         (OP_EFF, 1, 0, 0, 0, 3, 0x4000, 300),
         (OP_EFF, 1, 0, 0, 0, 4, 0x4000, 300),
         (OP_LINK, 1, 0, 2, 0x3000, 5, 0, 300),
         (OP_EFF, 1, 0, 0, 0, 6, 0x4000, 300),
         (OP_VIEW, EXTID, 0, 1, 0, 7, 0, 300),
         (OP_VIEW, EXTID, 0, 0, 0, 8, 0, 40000)]
    progs.append(p)
    # D5: saturation: max bases, hammer past bucket + wacc saturation
    p = [(OP_BIND, EXTID, 0, 0, 0, 1, 0, 200)]
    for i in range(4):
        p.append((OP_LINK, EXTID if i == 3 else 1, 0, i, 0xF000,
                  2 + i, 0, 200))
    p += [(OP_EFF, 1, 0, 0, 0, 6, 0x7FFF, 300)] * 6
    p += [(OP_VIEW, EXTID, 0, 1, 0, 20, 0, 300),
          (OP_VIEW, EXTID, 0, 0, 0, 21, 0, 40000)]
    progs.append(p)
    # D6: dial-13 probe: ftrace refills on fire, leaks with deadband snap
    p = [(OP_BIND, EXTID, 0, 0, 0, 1, 0, 200),
         (OP_BIND, EXTID, 0, 5, 0x0100, 2, 0, 100),
         (OP_LINK, EXTID, 0, 0, 0x2000, 3, 0, 200),
         (OP_EFF, EXTID, 0, 0, 0, 4, 0x7FFF, 400),
         (OP_VIEW, EXTID, 0, 2, 13, 5, 0, 30000),   # fired -> 0xFFFF
         (OP_VIEW, EXTID, 0, 2, 13, 6, 0, 30000),   # leaked once
         (OP_VIEW, EXTID, 0, 2, 13, 7, 0, 40000),
         (OP_VIEW, EXTID, 0, 2, 13, 8, 0, 40000)]
    progs.append(p)
    return progs


# ------------------------------------------------------------- driver --

def write_program(prog):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "cosim_fabric_prog.hex")
    with open(path, "w") as f:
        f.write("%d\n" % len(prog))
        for (op, src, dst, a0, a1, a2, dat, wait) in prog:
            f.write("%X %X %X %X %X %X %X %d\n"
                    % (op, src, dst, a0, a1, a2, dat, wait))
    return path


def run_tb():
    vvp = os.path.join(OUT, "tb_cosim_fabric.vvp")
    env = dict(os.environ)
    env["PATH"] = "/home/eileen/tools/oss-cad-suite/bin:" + env["PATH"]
    r = subprocess.run(
        "iverilog -g2005 -s tb_cosim_fabric -o %s "
        "rtl/q_tick_sched.v rtl/q_flit_pipe.v rtl/q_link_ringport.v "
        "rtl/q_dialfile.v rtl/q_hebb_edge.v rtl/q_echo_gate.v "
        "rtl/q_rqh_bank.v rtl/q_cell_core.v rtl/q_cell.v rtl/q_io_port.v "
        "rtl/q_fabric_top.v tb/tb_cosim_fabric.v"
        " && vvp %s" % (vvp, vvp),
        shell=True, cwd=_ROOT, capture_output=True, text=True, env=env)
    return r


def diff(prog, trace_path):
    """replay the MEASURED per-cell event streams (op acceptances and
    tick services, cycle-stamped by the TB) through the model and diff
    the egress stream against the RTL trace, per window (multiset per
    window: intra-window order between a response and same-window fires
    depends on ring micro-timing; every egress VALUE is diffed exactly)"""
    egress_rtl = []
    events = []            # (cyc, kind, cell, ...)
    with open(trace_path) as f:
        for line in f:
            t = line.split()
            if not t:
                continue
            if t[0] == "E":
                vals = tuple(int(x) for x in t[1:])
                egress_rtl.append(vals[:8])   # drop the cycle stamp
            elif t[0] == "P":
                # P c win cyc op src a0 a1 a2 dat
                events.append((int(t[3]), 0, "P", int(t[1]), int(t[4]),
                               int(t[5]), int(t[6]), int(t[7]),
                               int(t[8]), int(t[9]), int(t[2])))
            elif t[0] == "T":
                # T c win cyc
                events.append((int(t[3]), 1, "T", int(t[1]), -1, -1,
                               -1, -1, -1, -1, int(t[2])))
    events.sort(key=lambda e: (e[0], e[1]))   # P before T on same cycle

    m = FabricModel()
    egress_model = []
    # host echo flits (dst==EXTID) never enter a cell; they circle and
    # egress as-is in their grant window (win i+1 for program flit i)
    for i, flit8 in enumerate(prog):
        op, src, dst, a0, a1, a2, dat = flit8[:7]
        if dst == EXTID:
            egress_model.append((i + 1, op, src, dst, a0, a1, a2, dat))
    pending_fx = []          # fire fanout effects the ring must deliver
    for ev in events:
        cyc, _, kind, c = ev[0], ev[1], ev[2], ev[3]
        win = ev[10]
        if kind == "T":
            fires = m.cells[c].tick()
            cid = m.cells[c].cell_id
            for dst, dat in fires:
                if dst == EXTID:
                    egress_model.append((win, OP_EFF, cid, EXTID,
                                         0, 0, 0, dat))
                else:
                    pending_fx.append((dst, cid, dat))
        else:
            op, src, a0, a1, a2, dat = ev[4], ev[5], ev[6], ev[7], \
                ev[8], ev[9]
            if op == OP_EFF:
                # fire fanout delivery or host effect: match against
                # pending fanout (proves delivery happened; a lost
                # fanout flit stays pending -> FINDING at the end)
                for k, (dst, cid, fdat) in enumerate(pending_fx):
                    if dst == c and cid == src and fdat == dat:
                        pending_fx.pop(k)
                        break
                m.cells[c].host_effect(src, dat)
            else:
                resp, _ = m.cells[c].host_op(op, src, a0, a1, a2, dat)
                if resp is not None and resp[2] == EXTID:
                    egress_model.append((win,) + resp)

    mismatches = []
    if pending_fx:
        mismatches.append("%d fire-fanout effects never delivered: %s"
                          % (len(pending_fx), pending_fx[:4]))
    # per-window multiset diff
    def bywin(stream):
        d = {}
        for fl in stream:
            d.setdefault(fl[0], []).append(fl[1:])
        return d
    mw, rw = bywin(egress_model), bywin(egress_rtl)
    if len(egress_model) != len(egress_rtl):
        mismatches.append("egress count: model %d vs rtl %d"
                          % (len(egress_model), len(egress_rtl)))
    for w in sorted(set(mw) | set(rw)):
        a, b = sorted(mw.get(w, [])), sorted(rw.get(w, []))
        if a != b:
            mismatches.append("window %d: model %s vs rtl %s" % (w, a, b))
            if len(mismatches) > 10:
                break
    return mismatches, len(egress_rtl)


def run_program(prog, label):
    write_program(prog)
    r = run_tb()
    out = r.stdout + r.stderr
    if r.returncode != 0 or "DONE" not in out:
        print("cosim_fabric[%s]: TB ERROR\n%s" % (label, out[-2000:]))
        return False, 0
    trace = os.path.join(OUT, "cosim_fabric_trace.txt")
    mism, neg = diff(prog, trace)
    if mism:
        print("cosim_fabric[%s]: FINDING (%s)" % (label, mism[0]))
        for x in mism[:10]:
            print("  " + x)
        return False, neg
    return True, neg


def main():
    seed = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0xFAB41C
    n_random = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    rng = random.Random(seed)
    progs = [(p, "directed-%d" % i) for i, p in enumerate(gen_directed())]
    for i in range(n_random):
        progs.append((gen_program(rng, rng.randrange(50, 130)),
                      "rand-%d" % i))
    ok = 0
    tot_eg = 0
    fails = []
    for prog, label in progs:
        good, neg = run_program(prog, label)
        tot_eg += neg
        if good:
            ok += 1
        else:
            fails.append(label)
    print("cosim_fabric: %d/%d programs bit-exact, %d egress flits "
          "compared" % (ok, len(progs), tot_eg))
    if fails:
        print("cosim_fabric: FAILING: %s" % ", ".join(fails))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
