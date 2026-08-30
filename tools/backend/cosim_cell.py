#!/usr/bin/env python3
"""cosim_cell.py -- differential bench: Python v1 cell model vs the real
q_cell RTL in iverilog (backend lane, Phase 3; the §10-shaped cosim seed
at small scale).

The Python model mirrors q_cell_core/q_hebb_edge/q_dialfile arithmetic
bit-for-bit at v1 semantics (v2 dials pinned OFF: FLOOR=0, RQEN=0 -- the
POR defaults). Random bounded programs (bind/link/effect/view/tick) are
generated with a fixed seed, the model computes a checkpoint after every
op (act, wsum, fire fanout), tb/tb_cosim_fuzz.v replays the same program
against q_cell (PIPE_EFF retime included) and compares at every
checkpoint. ANY mismatch is a loud FINDING (either side may own the bug).

Output: tb/run/cosim_fuzz.hex. Report: checkpoints compared, agreement
rate, fire events crossed. Exit 1 on any mismatch. Stdlib only.
"""
import os
import random
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, "..", ".."))
OUT = os.path.join(_ROOT, "tb", "run")

PW, K, B, EDGES_N = 16, 8, 8, 4
NDIALS = 16
# q_dialfile POR defaults (raw words) -- v2 OFF by construction
POR_DIALS = [0x0800, 0x0080, 6, 12, 5, 0x6000, 4, 0x2CCD,
             20, 0, 64, 2, 0, 0, 0x0008, 0x0008]

OP_BIND, OP_LINK, OP_EFF, OP_VIEW, OP_TICK = 0, 1, 2, 3, 4


def sclip16(v):
    return max(-32768, min(32767, v))


def sat_u16(v):
    return max(0, min(0xFFFF, v))


def to_signed16(u):
    return u - 0x10000 if u >= 0x8000 else u


def msb16(v):
    m = 0
    for j in range(PW):
        if (v >> j) & 1:
            m = j
    return m


class Engine:
    """q_hebb_edge, both engines; mode comes from the cell dial."""

    __slots__ = ("buckets", "hl_cnt", "wh", "age", "base")

    def __init__(self):
        self.buckets = [0] * K
        self.hl_cnt = 0
        self.wh = 0
        self.age = 0
        self.base = 0

    def train(self, mode):
        if not mode:
            if self.buckets[0] >= (1 << B) - 1:
                pass                      # sticky ovf (not modeled further)
            else:
                self.buckets[0] += 1
        else:
            if self.wh >= (1 << PW) - 1:
                pass
            else:
                self.wh += 1

    def tick(self, mode, hl, p0e):
        if not mode:
            if self.hl_cnt + 1 >= hl:
                self.buckets[1:] = self.buckets[:-1]
                self.buckets[0] = 0
                self.hl_cnt = 0
            else:
                self.hl_cnt += 1
        else:
            ival = max(1, (1 << p0e) >> (2 * msb16(self.wh)))
            if self.wh and (self.age + 1 >= ival):
                self.wh -= 1
                self.age = 0
            else:
                self.age = (self.age + 1) & 0xFFFFFF   # AGEW=24 wrap

    def readout(self, mode):
        if not mode:
            acc = 0
            for i, c in enumerate(self.buckets):
                acc += c << (K - i)
            eng = 0xFFFF if (acc >> PW) else acc
        else:
            eng = 0xFFFF if self.wh > 255 else (self.wh & 0xFF) << 8
        return sat_u16(self.base + eng)


class CellModel:
    """q_cell at v1 semantics. Slots are engine-owned (no eviction)."""

    def __init__(self):
        self.dials = list(POR_DIALS)
        self.edges = [None] * EDGES_N       # Engine or None (invalid)
        self._peer = [0] * EDGES_N          # slot -> peer cell id
        self.act = 0                        # signed
        self.refr = 0
        self.cell_id = 0
        self.bound = False

    def d(self, i):
        return self.dials[i]

    def op(self, op, src, a0, a1):
        """apply one op; returns (view0, view1, fires) checkpoint AFTER it"""
        fires = []
        if not self.bound:
            if op == OP_BIND:
                self.cell_id = a0 & 0xF
                self.bound = True
            return self.view0(), self.view1(), fires
        if op == OP_BIND:
            addr = a0 & 0xF
            if addr != 13:                  # FTRACE probe alias: ignored
                self.dials[addr] = a1 & 0xFFFF
        elif op == OP_LINK:
            slot = a0 & 0x3
            if self.edges[slot] is None:
                self.edges[slot] = Engine()
            self.edges[slot].base = a1 & 0xFFFF
            self._peer[slot] = src & 0xF
        elif op == OP_EFF:
            slot = self._find(src)
            if slot is not None:
                e = self.edges[slot]
                mode = self.d(9) & 1
                e.train(mode)               # gate open (FLOOR=0): train
                w = e.readout(mode)         # post-train readback
                prod = w * to_signed16(a1 & 0xFFFF)
                self.act = sclip16(self.act + (prod >> 15))
        elif op == OP_VIEW:
            pass                            # views are the checkpoint
        elif op == OP_TICK:
            mode = self.d(9) & 1
            hl = self.d(10)
            p0e = self.d(8) & 0x1F          # 5-bit dial slice
            for e in self.edges:
                if e is not None:
                    e.tick(mode, hl, p0e)
            thresh = to_signed16(self.d(5))
            ka = self.d(4) & 0xF
            if self.act >= thresh and self.refr == 0:
                afire = self.act
                fires = [(self._peer[i], afire & 0xFFFF)
                         for i in range(EDGES_N) if self.edges[i] is not None]
                self.act = 0
                self.refr = self.d(6) & 0xFFFF
            else:
                self.act = sclip16(self.act - (self.act >> ka))
                if self.refr:
                    self.refr -= 1
        return self.view0(), self.view1(), fires

    _peer = None

    def _find(self, src):
        for i in range(EDGES_N):
            if self.edges[i] is not None and self._peer[i] == (src & 0xF):
                return i
        return None

    def view0(self):
        return self.act & 0xFFFF

    def view1(self):
        mode = self.d(9) & 1
        wacc = sum(e.readout(mode) for e in self.edges if e is not None)
        return sat_u16(wacc)


# ------------------------------------------------------------- programs --

def gen_program(rng, nops, mode):
    """random bounded program: list of (op, src, a0, a1)"""
    prog = [(OP_BIND, 0, 1, 0)]             # first bind: cell_id = 1
    peers = []
    for _ in range(nops):
        r = rng.random()
        if r < 0.10:
            # dial binds that matter: KA, THRESH, REFR, HL, P0E, MODE(pin)
            which = rng.choice([4, 5, 6, 8, 10, 7, 11, 12])
            val = {4: rng.randrange(0, 16), 5: rng.choice(
                [0, 1, 0x1000, 0x3800, 0x6000, 0x7FFF, 0x8000, 0xC000]),
                6: rng.randrange(0, 6), 8: rng.randrange(0, 24),
                10: rng.choice([1, 2, 3, 4, 8, 64]),
                7: rng.randrange(0, 4), 11: rng.randrange(0, 4),
                12: 0}[which]              # dial 12 pinned 0 (gate OFF)
            prog.append((OP_BIND, 0, which, val))
        elif r < 0.28:
            slot = rng.randrange(EDGES_N)
            src = rng.randrange(16)
            peers.append(src)
            prog.append((OP_LINK, src, slot,
                         rng.choice([0, 4096, 8192, 0xF000,
                                     rng.randrange(0x10000)])))
        elif r < 0.62:
            src = rng.choice(peers) if peers and rng.random() < 0.8 \
                else rng.randrange(16)
            dat = rng.choice([0, 1, 0x7FFF, 0x8000, 0xFFFF, 0x4000,
                              rng.randrange(0x10000)])
            prog.append((OP_EFF, src, 0, dat))
        elif r < 0.72:
            prog.append((OP_VIEW, 0, rng.randrange(3), rng.randrange(16)))
        else:
            prog.append((OP_TICK, 0, 0, 0))
    return prog


def gen_directed():
    """corner programs"""
    progs = []
    # saturation: hammer one edge past bucket saturation + max act
    p = [(OP_BIND, 0, 1, 0), (OP_LINK, 3, 0, 0x7FFF)]
    p += [(OP_EFF, 3, 0, 0x7FFF)] * 40 + [(OP_TICK, 0, 0, 0)] * 3
    p += [(OP_EFF, 3, 0, 0x8000)] * 40 + [(OP_TICK, 0, 0, 0)] * 3
    p += [(OP_VIEW, 0, 1, 0)]
    progs.append(p)
    # fire storm: low threshold, high refr, repeated fire/refractory cycles
    p = [(OP_BIND, 0, 1, 0), (OP_BIND, 0, 5, 0x0100), (OP_BIND, 0, 6, 3),
         (OP_BIND, 0, 4, 15)]
    for i in range(4):
        p.append((OP_LINK, 4 + i, i, 0x2000))
    p += [(OP_EFF, 4, 0, 0x7FFF), (OP_EFF, 5, 1, 0x7FFF)]
    p += [(OP_TICK, 0, 0, 0)] * 12
    p += [(OP_EFF, 6, 2, 0x6000)] * 6 + [(OP_TICK, 0, 0, 0)] * 8
    progs.append(p)
    # re-link persistence: buckets survive a base change (cmd 100 only)
    p = [(OP_BIND, 0, 1, 0), (OP_LINK, 2, 1, 0x1000)]
    p += [(OP_EFF, 2, 0, 0x4000)] * 5
    p += [(OP_LINK, 2, 1, 0x3000)]          # same slot, new base
    p += [(OP_EFF, 2, 0, 0x4000), (OP_VIEW, 0, 1, 0)]
    progs.append(p)
    # negative act leak floor: act<0, ka=0 (no leak) and ka=15
    p = [(OP_BIND, 0, 1, 0), (OP_LINK, 9, 0, 0x7FFF),
         (OP_BIND, 0, 4, 0)]
    p += [(OP_EFF, 9, 0, 0x8000)] * 8 + [(OP_TICK, 0, 0, 0)] * 2
    p += [(OP_BIND, 0, 4, 15), (OP_TICK, 0, 0, 0)] * 4
    p += [(OP_VIEW, 0, 0, 0), (OP_VIEW, 0, 1, 0)]
    progs.append(p)
    # unknown-src drops: effects to unlinked srcs never move act
    p = [(OP_BIND, 0, 1, 0), (OP_LINK, 5, 2, 0x4000)]
    p += [(OP_EFF, 5, 0, 0x7FFF)]
    p += [(OP_EFF, 6, 0, 0x7FFF), (OP_EFF, 5, 0, 0x7FFF)]
    p += [(OP_VIEW, 0, 0, 0), (OP_VIEW, 0, 1, 0)]
    progs.append(p)
    # dial 13 write ignored (probe alias)
    p = [(OP_BIND, 0, 1, 0), (OP_BIND, 0, 13, 0xBEEF),
         (OP_VIEW, 0, 2, 13), (OP_VIEW, 0, 1, 0)]
    progs.append(p)
    # REGRESSION (differential-found 2026-08-29): the q_cell weight mux
    # was an OR-tree over all engines -- after ANY readback, stale o_w
    # registers polluted every later view(1) (4x0x2100=0x8400 vs 0x8200)
    p = [(OP_BIND, 0, 1, 0)]
    for i in range(4):
        p.append((OP_LINK, 4 + i, i, 0x2000))
    p += [(OP_EFF, 4, 0, 0x1000), (OP_EFF, 5, 1, 0x1000),
          (OP_EFF, 6, 2, 0x1000), (OP_VIEW, 0, 1, 0)]
    progs.append(p)
    # REGRESSION (differential-found 2026-08-29): wacc was 17-bit -- four
    # near-max readouts wrapped it (0x20008-class sums read small). Max
    # bases + trains must saturate view(1) at exactly 0xFFFF.
    p = [(OP_BIND, 0, 1, 0)]
    for i in range(4):
        p.append((OP_LINK, 8 + i, i, 0xF000))
    p += [(OP_EFF, 8, 0, 0x7FFF)] * 3 + [(OP_VIEW, 0, 1, 0)]
    progs.append(p)
    return progs


# ------------------------------------------------------------- manifest --

def run_model(progs):
    """returns per-program checkpoints: [(v0, v1, [(dst,dat)...]) ...]"""
    all_ckpts = []
    for prog in progs:
        m = CellModel()
        ck = []
        for (op, src, a0, a1) in prog:
            v0, v1, fires = m.op(op, src, a0, a1)
            ck.append((v0, v1, fires))
        all_ckpts.append(ck)
    return all_ckpts


def write_manifest(progs, ckpts):
    os.makedirs(OUT, exist_ok=True)
    lines = []
    nops_total = sum(len(p) for p in progs)
    lines.append("%04X" % len(progs))
    for prog, ck in zip(progs, ckpts):
        lines.append("%04X" % len(prog))
        for (op, src, a0, a1), (v0, v1, fires) in zip(prog, ck):
            lines.append("%1X%1X%04X" % (op, src, a0))
            lines.append("%04X" % a1)
            lines.append("%04X%04X" % (v0, v1))
            lines.append("%02X" % len(fires))
            for dst, dat in fires:
                lines.append("%1X%04X" % (dst, dat))
    path = os.path.join(OUT, "cosim_fuzz.hex")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path, nops_total


def run_tb():
    vvp = os.path.join(OUT, "tb_cosim_fuzz.vvp")
    env = dict(os.environ)
    env["PATH"] = "/home/eileen/tools/oss-cad-suite/bin:" + env["PATH"]
    r = subprocess.run(
        "iverilog -g2005 -s tb_cosim_fuzz -o %s "
        "rtl/q_tick_sched.v rtl/q_flit_pipe.v rtl/q_link_ringport.v "
        "rtl/q_dialfile.v rtl/q_hebb_edge.v rtl/q_echo_gate.v "
        "rtl/q_rqh_bank.v rtl/q_cell_core.v rtl/q_cell.v tb/tb_cosim_fuzz.v"
        " && vvp %s" % (vvp, vvp),
        shell=True, cwd=_ROOT, capture_output=True, text=True, env=env)
    return r


def main():
    rng = random.Random(0xC0511)
    progs = gen_directed()
    for i in range(60):
        mode = i % 4 == 3                   # every 4th: hyperbola MODE=1
        p = gen_program(rng, rng.randrange(40, 140), mode)
        if mode:
            p.insert(1, (OP_BIND, 0, 9, 1))         # MODE dial = 1
            p.insert(2, (OP_BIND, 0, 8, rng.randrange(0, 20)))
        progs.append(p)
    ckpts = run_model(progs)
    path, nops = write_manifest(progs, ckpts)
    nfire = sum(len(f) for ck in ckpts for _, _, f in ck)
    nck = sum(len(ck) * 2 for ck in ckpts)
    print("cosim_cell: %d programs, %d ops, %d view checkpoints, "
          "%d fire events -> %s" % (len(progs), nops, nck, nfire, path))
    r = run_tb()
    out = r.stdout + r.stderr
    print(out.strip()[-2000:])
    if r.returncode != 0 or "COSIM FAIL" in out:
        return 1
    if "COSIM PASS" not in out:
        print("cosim_cell: no verdict line")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
