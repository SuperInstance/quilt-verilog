// tb_quiesce_repro.cpp -- MINIMAL REPRO for the residual fabric liveness
// death booked from the 2026-08-30 rescue lane (SILICON-EXPERIMENTS §2 #1b).
//
// Claim: even with the ringport clone fix (rtl/q_link_ringport.v, transit =
// ri_valid && !hit) and a host ack-window, a quiesced (injection-stopped)
// fabric could hold flits that NEVER drain: circular wait between full cell
// inbufs / full egbufs / full ring. Ledger stays intact (net == occ) -- no
// flit is duplicated or lost, the fabric simply stops moving. Recovery is
// reset-only (proved by P3 of tb_scale_vlt).
//
// RESOLVED (F3 escape-lane fix, 2026-08-30): inject_ok = !ri_valid || hit
// (a hit never claims ro, so injection escapes a parked delivery). On the
// fixed RTL this repro drains to occ=0 in 21 cycles, bit-identical on
// re-run; exit 1 now means F3 REGRESSION. (Note: the dials here are NOT
// fire-proof despite an early comment claiming so -- thresh 0x7FFF still
// fires on saturated effects; the pre-fix wedge was exactly a cell stuck
// in ST_FIRE. Fires are rare, not impossible.)
//
// Program (NCELL=15):
//   P0  bind/dial/link all cells (same as scale bench)
//   P1  windowed mixed traffic (<=12 views in flight, 10% effects) for
//       QV_REPRO_CYCLES cycles (default 50000, env knob)
//   P2  STOP injecting; step up to 500k cycles waiting for occ==0.
//       If occupancy freezes >0 for 4096+ cycles -> dump full fabric state,
//       print QUIESCE-DEADLOCK, exit 1. Else REPRO: PASS (drained), exit 0.
//
// Build/run: see sim/vlt/run_quiesce_repro.sh (same verilator line as the
// scale lane). Numbers measured 2026-08-30 rescue lane; see docs §2.
#include "Vq_fabric_top.h"
#include "Vq_fabric_top___024root.h"
#include "Vq_fabric_top_q_cell.h"
#include "Vq_fabric_top__Syms.h"
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <ctime>

static Vq_fabric_top* top;
static Vq_fabric_top___024root* root;
static Vq_fabric_top_q_cell* cell[15];

static uint64_t cyc = 0;
static uint64_t rng_state = 1;
static inline uint64_t xs64() {
    rng_state ^= rng_state >> 12; rng_state ^= rng_state << 25;
    rng_state ^= rng_state >> 27;
    return rng_state * 2685821657736338717ULL;
}

static const int EXTID  = 0xF;
static const uint8_t OP_BIND = 0, OP_LINK = 1, OP_EFF = 2, OP_VIEW = 3;

#define RING_PIPE_A(g) root->q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__u_pipe__DOT__a_v
#define RING_PIPE_B(g) root->q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__u_pipe__DOT__b_v
static inline int occ_all() {
    int occ = 0;
    occ += RING_PIPE_A(0)+RING_PIPE_B(0);  occ += RING_PIPE_A(1)+RING_PIPE_B(1);
    occ += RING_PIPE_A(2)+RING_PIPE_B(2);  occ += RING_PIPE_A(3)+RING_PIPE_B(3);
    occ += RING_PIPE_A(4)+RING_PIPE_B(4);  occ += RING_PIPE_A(5)+RING_PIPE_B(5);
    occ += RING_PIPE_A(6)+RING_PIPE_B(6);  occ += RING_PIPE_A(7)+RING_PIPE_B(7);
    occ += RING_PIPE_A(8)+RING_PIPE_B(8);  occ += RING_PIPE_A(9)+RING_PIPE_B(9);
    occ += RING_PIPE_A(10)+RING_PIPE_B(10);occ += RING_PIPE_A(11)+RING_PIPE_B(11);
    occ += RING_PIPE_A(12)+RING_PIPE_B(12);occ += RING_PIPE_A(13)+RING_PIPE_B(13);
    occ += RING_PIPE_A(14)+RING_PIPE_B(14);occ += RING_PIPE_A(15)+RING_PIPE_B(15);
    for (int g = 0; g < 15; g++) {
        occ += cell[g]->u_inbuf__DOT__a_v + cell[g]->u_inbuf__DOT__b_v;
        occ += cell[g]->u_egbuf__DOT__a_v + cell[g]->u_egbuf__DOT__b_v;
    }
    return occ;
}

static bool in_pend = false, want_inject = false, w_fresh = false;
static uint8_t in_op, in_src, in_dst;
static uint16_t in_a0, in_a1, in_dat;
static uint8_t w_op, w_src, w_dst; static uint16_t w_a0, w_a1, w_dat;
static bool saw_o_rdy = false, saw_o_val = false;
static uint8_t out_op, out_dst;
static uint64_t resp_pending = 0;
static uint64_t c_inj = 0, c_drain = 0, c_emit = 0, c_accept = 0;
static uint64_t last_activity = 0;

#define RP2(g, f) root->q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__u_pipe__DOT__##f
static inline int ring_pushes(void) {
    return RP2(0,push)+RP2(1,push)+RP2(2,push)+RP2(3,push)+RP2(4,push)
         + RP2(5,push)+RP2(6,push)+RP2(7,push)+RP2(8,push)+RP2(9,push)
         + RP2(10,push)+RP2(11,push)+RP2(12,push)+RP2(13,push)
         + RP2(14,push)+RP2(15,push);
}
static inline int ring_pops(void) {
    return RP2(0,pop)+RP2(1,pop)+RP2(2,pop)+RP2(3,pop)+RP2(4,pop)
         + RP2(5,pop)+RP2(6,pop)+RP2(7,pop)+RP2(8,pop)+RP2(9,pop)
         + RP2(10,pop)+RP2(11,pop)+RP2(12,pop)+RP2(13,pop)
         + RP2(14,pop)+RP2(15,pop);
}
// entry-identity trap (clone detector): a ring push must be sourced by an
// io/cell li handshake or paired with an upstream pop (transit). Fires the
// first cycle it breaks. Silent = clone fix intact.
static bool entry_identity_ok() {
    int lhs = ring_pushes() - ring_pops();
    int rhs = ((top->i_val && top->o_rdy) ? 1 : 0);
    for (int g = 0; g < 15; g++) {
        if (cell[g]->li_valid_w && cell[g]->li_ready_w) rhs++;
        if (cell[g]->ld_valid && cell[g]->ld_ready) rhs--;
    }
    if (top->o_val && top->i_rdy) rhs--;
    return lhs == rhs;
}

static void step() {
    if (in_pend && saw_o_rdy) in_pend = false;
    if (!in_pend && want_inject && w_fresh) {
        in_op = w_op; in_src = w_src; in_dst = w_dst;
        in_a0 = w_a0; in_a1 = w_a1; in_dat = w_dat;
        in_pend = true; w_fresh = false;
    }
    top->i_val = in_pend;
    top->i_op = in_op; top->i_src = in_src; top->i_dst = in_dst;
    top->i_a0 = in_a0; top->i_a1 = in_a1; top->i_dat = in_dat;
    top->i_rdy = 1;

    top->clk = 0; top->eval();
    static bool trap_fired = false;
    if (!trap_fired && cyc > 0 && !entry_identity_ok()) {
        trap_fired = true;
        printf("ENTRY-IDENTITY BREAK @cyc=%llu (clone bug present?)\n",
               (unsigned long long)cyc);
    }
    saw_o_rdy = top->o_rdy; saw_o_val = top->o_val;
    out_op = top->o_op; out_dst = top->o_dst;

    bool act = false;
    if (top->i_val && saw_o_rdy) { c_inj++; act = true; }
    if (saw_o_val && top->i_rdy) { c_drain++; act = true;
        if (resp_pending) resp_pending--; }
    for (int g = 0; g < 15; g++) {
        Vq_fabric_top_q_cell* c = cell[g];
        if (c->eg_s_valid && c->eg_s_ready) { c_emit++; act = true; }
        if (c->ci_valid && c->ci_ready_w)   { c_accept++; act = true; }
    }
    if (act) last_activity = cyc;
    top->clk = 1; top->eval();
    cyc++;
}

static void xfer_noack(uint8_t op, uint8_t src, uint8_t dst,
                       uint16_t a0, uint16_t a1, uint16_t dat,
                       uint64_t timeout = 4096) {
    uint64_t inj_b = c_inj, t0 = cyc;
    w_op = op; w_src = src; w_dst = dst; w_a0 = a0; w_a1 = a1; w_dat = dat;
    want_inject = true; w_fresh = true;
    while (c_inj == inj_b) {
        step();
        if (cyc - t0 > timeout) {
            printf("XFER-TIMEOUT @cyc=%llu op=%d dst=%x (bench timeout)\n",
                   (unsigned long long)cyc, op, dst);
            exit(2);
        }
    }
    want_inject = false;
}
static uint16_t xfer(uint8_t op, uint8_t src, uint8_t dst,
                     uint16_t a0, uint16_t a1, uint16_t dat,
                     uint64_t timeout = 4096) {
    uint64_t inj_b = c_inj, drain_b = c_drain, t0 = cyc;
    w_op = op; w_src = src; w_dst = dst; w_a0 = a0; w_a1 = a1; w_dat = dat;
    want_inject = true; w_fresh = true;
    while (c_inj == inj_b) {
        step();
        if (cyc - t0 > timeout) goto TO;
    }
    while (c_drain == drain_b) {
        step();
        if (cyc - t0 > timeout) goto TO;
    }
    want_inject = false;
    return out_op == 5 ? (uint16_t)0 : (uint16_t)1; // placeholder (unused)
TO:
    printf("XFER-TIMEOUT @cyc=%llu op=%d dst=%x (bench timeout)\n",
           (unsigned long long)cyc, op, dst);
    exit(2);
}

static int peer_of[15][4];
static void gen_traffic(int eff_pct) {
    uint64_t r = xs64();
    if ((r % 100) < (uint64_t)eff_pct) {
        int dst = (int)((xs64() >> 8) % 15);
        int slot = (int)((xs64() >> 16) % 4);
        w_op = OP_EFF; w_src = (uint8_t)peer_of[dst][slot];
        w_dst = (uint8_t)dst; w_a0 = 0; w_a1 = 0;
        w_dat = (uint16_t)(0x4000 + (xs64() & 0x3FFF));
    } else {
        int dst = (int)((xs64() >> 8) % 15);
        w_op = OP_VIEW; w_src = EXTID; w_dst = (uint8_t)dst;
        w_a0 = 0; w_a1 = 0; w_dat = 0;
        resp_pending++;
    }
    want_inject = true; w_fresh = true;
}

static void do_reset(uint64_t n) {
    top->rst_n = 0; top->i_val = 0; in_pend = false; want_inject = false;
    w_fresh = false;
    for (uint64_t i = 0; i < n; i++) { top->clk = 0; top->eval();
                                       top->clk = 1; top->eval(); cyc++; }
    top->rst_n = 1;
    c_inj = c_drain = c_emit = c_accept = 0;
    resp_pending = 0; last_activity = cyc;
}

static void setup_fabric() {
    static const int ndial = 7;
    static const uint8_t  daddr[ndial] = { 4, 5, 6, 11, 12, 14, 15 };
    const uint16_t dval[ndial]  = { 8, 0x7FFF, 0x7FFF, 2, 0x0010, 0x8008, 0x0008 };
    for (int c = 0; c < 15; c++) {
        xfer(OP_BIND, EXTID, (uint8_t)c, (uint16_t)c, 0, 0);
        for (int d = 0; d < ndial; d++)
            xfer(OP_BIND, EXTID, (uint8_t)c, daddr[d], dval[d], 0);
        for (int s = 0; s < 4; s++) {
            peer_of[c][s] = (c + s + 1) % 15;
            xfer_noack(OP_LINK, (uint8_t)peer_of[c][s], (uint8_t)c,
                       (uint16_t)s, 0x0100, 0);
        }
    }
}

static void dump() {
    int ring = 0, inb = 0, egb = 0;
    for (int g = 0; g < 15; g++) {
        Vq_fabric_top_q_cell* c = cell[g];
        inb += c->u_inbuf__DOT__a_v + c->u_inbuf__DOT__b_v;
        egb += c->u_egbuf__DOT__a_v + c->u_egbuf__DOT__b_v;
    }
    ring = occ_all() - inb - egb;
    printf("STUCK-STATE @cyc=%llu: occ=%d [ring=%d inbuf=%d egbuf=%d] "
           "(inj=%llu emit=%llu acc=%llu drain=%llu, ledger %s)\n",
           (unsigned long long)cyc, occ_all(), ring, inb, egb,
           (unsigned long long)c_inj, (unsigned long long)c_emit,
           (unsigned long long)c_accept, (unsigned long long)c_drain,
           ((int64_t)(c_inj + c_emit - c_accept - c_drain) == occ_all())
               ? "intact" : "BROKEN");
    for (int g = 0; g < 15; g++) {
        Vq_fabric_top_q_cell* c = cell[g];
        printf("  cell %2d: state=%2d bound=%d in=%d%d eg=%d%d\n", g,
               c->u_core__DOT__state,
               c->u_core__DOT__bound ? 1 : 0,
               c->u_inbuf__DOT__a_v, c->u_inbuf__DOT__b_v,
               c->u_egbuf__DOT__a_v, c->u_egbuf__DOT__b_v);
    }
    printf("  ring heads (slice:valid a/b,dst):");
#define RP(g, f) root->q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__u_pipe__DOT__##f
    for (int q = 0; q < 16; q++)
        printf(" %d:%d%d/%x", q,
               q==0?RP(0,a_v):q==1?RP(1,a_v):q==2?RP(2,a_v):q==3?RP(3,a_v):
               q==4?RP(4,a_v):q==5?RP(5,a_v):q==6?RP(6,a_v):q==7?RP(7,a_v):
               q==8?RP(8,a_v):q==9?RP(9,a_v):q==10?RP(10,a_v):q==11?RP(11,a_v):
               q==12?RP(12,a_v):q==13?RP(13,a_v):q==14?RP(14,a_v):RP(15,a_v),
               q==0?RP(0,b_v):q==1?RP(1,b_v):q==2?RP(2,b_v):q==3?RP(3,b_v):
               q==4?RP(4,b_v):q==5?RP(5,b_v):q==6?RP(6,b_v):q==7?RP(7,b_v):
               q==8?RP(8,b_v):q==9?RP(9,b_v):q==10?RP(10,b_v):q==11?RP(11,b_v):
               q==12?RP(12,b_v):q==13?RP(13,b_v):q==14?RP(14,b_v):RP(15,b_v),
               q==0?RP(0,m_dst):q==1?RP(1,m_dst):q==2?RP(2,m_dst):q==3?RP(3,m_dst):
               q==4?RP(4,m_dst):q==5?RP(5,m_dst):q==6?RP(6,m_dst):q==7?RP(7,m_dst):
               q==8?RP(8,m_dst):q==9?RP(9,m_dst):q==10?RP(10,m_dst):q==11?RP(11,m_dst):
               q==12?RP(12,m_dst):q==13?RP(13,m_dst):q==14?RP(14,m_dst):RP(15,m_dst));
    printf("\n");
}

int main(int argc, char** argv) {
    (void)argc; (void)argv;
    uint64_t repro_cyc = 50000;
    if (const char* e = getenv("QV_REPRO_CYCLES")) repro_cyc = strtoull(e, 0, 0);
    rng_state = 0xC0FFEE;

    top = new Vq_fabric_top;
    root = top->rootp;
    Vq_fabric_top__Syms* symsp = top->rootp->vlSymsp;
    cell[0]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell;
#define CELLN(g) cell[g] = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__connc__DOT__u_cell
    CELLN(1);  CELLN(2);  CELLN(3);  CELLN(4);  CELLN(5);
    CELLN(6);  CELLN(7);  CELLN(8);  CELLN(9);  CELLN(10);
    CELLN(11); CELLN(12); CELLN(13); CELLN(14);

    do_reset(16);
    setup_fabric();
    printf("P0 setup done @%llu (ledger %s, occ=%d)\n", (unsigned long long)cyc,
           ((int64_t)(c_inj + c_emit - c_accept - c_drain) == occ_all())
               ? "OK" : "FAIL", occ_all());

    // P1: windowed mixed traffic, fire-proof dials
    for (uint64_t i = 0; i < repro_cyc; i++) {
        if (!in_pend && resp_pending < 12) gen_traffic(10);
        else if (!in_pend) want_inject = false;
        step();
    }
    want_inject = false; top->i_val = 0; in_pend = false;
    printf("P1 traffic done @%llu: occ=%d pending=%llu inj=%llu drain=%llu\n",
           (unsigned long long)cyc, occ_all(),
           (unsigned long long)resp_pending,
           (unsigned long long)c_inj, (unsigned long long)c_drain);

    // P2: quiesce -- no injection, wait for full drain
    uint64_t t0 = cyc;
    int last_occ = -1; uint64_t occ_stuck_since = 0;
    while (occ_all() && cyc - t0 < 500000) {
        step();
        int o = occ_all();
        if (o != last_occ) { last_occ = o; occ_stuck_since = cyc; }
    }
    if (occ_all()) {
        printf("QUIESCE-DEADLOCK @cyc=%llu: occ=%d stuck since cyc=%llu "
               "-- FABRIC LIVENESS BUG (ledger-intact circular wait)\n",
               (unsigned long long)cyc, occ_all(),
               (unsigned long long)occ_stuck_since);
        dump();
        printf("REPRO: DEADLOCK (exit 1)\n");
        return 1;
    }
    printf("REPRO: PASS (drained to occ=0 in %llu cycles)\n",
           (unsigned long long)(cyc - t0));
    delete top;
    return 0;
}
