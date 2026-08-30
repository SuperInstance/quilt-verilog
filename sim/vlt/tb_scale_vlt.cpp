// tb_scale_vlt.cpp -- SILICON EXPERIMENT LANE scale sim (verilator).
//
// Drives the LARGEST LEGAL q_fabric_top the RTL parameters admit:
//   AIDW=4 caps ids at 0..15; EXTID=0xF is the io node, so cells 0..14
//   => NCELL=15 (a 16th cell would alias the io node's address).
//   EIW=2 (q_cell default, not exposed by the top) caps EDGES_N at 4.
//   Engines at q_cell defaults: K=8 buckets, B=8 bits, AGEW=24 -- the
//   widest engine config in the tree (the committed bitstream runs the
//   shrunk k4b4a8e1 proof params; this bench runs the big ones).
//
// Checkers (existing checker semantics ported to runtime, cited):
//   LEDGER  flit conservation, the runtime form of the formal
//           fabric.conservation A1/T1 ledger (formal/f_fabric_conservation.v):
//           cum(io_injected + core_emitted) - cum(core_accepted + io_drained)
//           == pipes occupied (16 ring slices + 15x inbuf/egbuf), checked
//           every 256 cycles and exact-zero at quiescence. Catches flit
//           fabrication AND loss at network scale, mixed traffic.
//   ACKLAT  every view/bind ack returns within ACK_TIMEOUT cycles
//           (MAX_OP_CYCLES bound, q_cell_core Q1, scaled by ring depth).
//   ACKDST  every egress flit is addressed to EXTID (routing check).
//   PROG    deadlock watchdog: no fabric-wide handshake for 4096 cycles
//           while traffic is expected == FAIL.
//
// Phases: SETUP -> MAIN (1,000,000 cycles, ~10% effect rate) -> QUIESCE
//   -> STORM (200k cycles, 100% effects, fire-prone dials) -> QUIESCE
//   -> RESET mid-pipeline (pipes deliberately held full) + recovery
//   -> DETERMINISM: fixed-seed pass hashed twice (+ divergent-seed sanity).
//
// Build+run: bash sim/vlt/run_scale.sh   (exact commands quoted there)
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <ctime>
#include "verilated.h"
#include "Vq_fabric_top.h"
#include "Vq_fabric_top___024root.h"
#include "Vq_fabric_top__Syms.h"
#include "Vq_fabric_top_q_cell.h"

// ---------------- fabric geometry (must match run_scale.sh -G args) ----
static const int NCELL  = 15;           // cells 0..14; io node = 15
static const int EDGES  = 4;
static const int EXTID  = 0xF;
static const int NB     = NCELL + 1;    // ring nodes

// opcodes (q_cell_core localparams)
static const uint8_t OP_BIND = 0, OP_LINK = 1, OP_EFF = 2, OP_VIEW = 3,
                     OP_ACK = 5;

// timeouts (fabric cycles)
static const uint64_t ACK_TIMEOUT = 8192;
static const uint64_t PROG_TIMEOUT = 4096;

static uint64_t rng_state = 1;
static inline uint64_t xs64() {           // xorshift64* -- deterministic
    rng_state ^= rng_state >> 12; rng_state ^= rng_state << 25;
    rng_state ^= rng_state >> 27;
    return rng_state * 2685821657736338717ULL;
}

static Vq_fabric_top* top;
static Vq_fabric_top___024root* root;
static Vq_fabric_top_q_cell* cell[NCELL];

static uint64_t cyc = 0;
static int errors = 0;

// ---------------- ledger counters -------------------------------------
static uint64_t c_inj = 0, c_drain = 0, c_emit = 0, c_accept = 0;
static uint64_t c_accept_eff = 0, c_accept_view = 0, c_accept_other = 0;
static uint64_t c_emit_ack = 0, c_emit_fire = 0, c_ticks = 0;
static uint64_t c_ovf_cells = 0;          // cell-cycles with sticky o_ovf

// Direct field access via generate-block macros keeps names in one place:
#define RING_PIPE_A(g) root->q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__u_pipe__DOT__a_v
#define RING_PIPE_B(g) root->q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__u_pipe__DOT__b_v
static inline int occ_all() {
    int occ = 0;
    // ring pipes (16)
    occ += RING_PIPE_A(0)  + RING_PIPE_B(0);
    occ += RING_PIPE_A(1)  + RING_PIPE_B(1);
    occ += RING_PIPE_A(2)  + RING_PIPE_B(2);
    occ += RING_PIPE_A(3)  + RING_PIPE_B(3);
    occ += RING_PIPE_A(4)  + RING_PIPE_B(4);
    occ += RING_PIPE_A(5)  + RING_PIPE_B(5);
    occ += RING_PIPE_A(6)  + RING_PIPE_B(6);
    occ += RING_PIPE_A(7)  + RING_PIPE_B(7);
    occ += RING_PIPE_A(8)  + RING_PIPE_B(8);
    occ += RING_PIPE_A(9)  + RING_PIPE_B(9);
    occ += RING_PIPE_A(10) + RING_PIPE_B(10);
    occ += RING_PIPE_A(11) + RING_PIPE_B(11);
    occ += RING_PIPE_A(12) + RING_PIPE_B(12);
    occ += RING_PIPE_A(13) + RING_PIPE_B(13);
    occ += RING_PIPE_A(14) + RING_PIPE_B(14);
    occ += RING_PIPE_A(15) + RING_PIPE_B(15);
    // per-cell ingress/egress buffers (15 x 2 pipes x 2 slots)
    for (int g = 0; g < NCELL; g++) {
        occ += cell[g]->u_inbuf__DOT__a_v + cell[g]->u_inbuf__DOT__b_v;
        occ += cell[g]->u_egbuf__DOT__a_v + cell[g]->u_egbuf__DOT__b_v;
    }
    return occ;
}

// ---------------- external driver state -------------------------------
static bool  in_pend = false;             // i_val held high, uncommitted
static bool  i_rdy_en = true;             // egress drain gate
static uint8_t in_op, in_src, in_dst;
static uint16_t in_a0, in_a1, in_dat;

static bool want_inject = false;          // set by phase logic each cycle
static uint8_t w_op, w_src, w_dst; static uint16_t w_a0, w_a1, w_dat;

static bool saw_o_rdy = false, saw_o_val = false;
static uint8_t  out_op, out_dst; static uint16_t out_dat;

// ack-latency tracker: age of oldest outstanding response-expected op
static uint64_t resp_pending = 0;         // count of views+binds awaiting ack
static uint64_t oldest_resp_cyc = 0;      // cycle it was issued

// progress watchdog
static uint64_t last_activity = 0;

// cycle trace ring (debugging the ledger): last 64 cycles of events
static char tring[64][160]; static int ti = 0; static bool traced = false;

// pipe-level push/pop witnesses (u_pipe exposes push/pop publicly)
#define RP2(g, f) root->q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__u_pipe__DOT__##f
static int ring_pushes(void) {
    return RP2(0,push)+RP2(1,push)+RP2(2,push)+RP2(3,push)+RP2(4,push)
         + RP2(5,push)+RP2(6,push)+RP2(7,push)+RP2(8,push)+RP2(9,push)
         + RP2(10,push)+RP2(11,push)+RP2(12,push)+RP2(13,push)
         + RP2(14,push)+RP2(15,push);
}
static int ring_pops(void) {
    return RP2(0,pop)+RP2(1,pop)+RP2(2,pop)+RP2(3,pop)+RP2(4,pop)
         + RP2(5,pop)+RP2(6,pop)+RP2(7,pop)+RP2(8,pop)+RP2(9,pop)
         + RP2(10,pop)+RP2(11,pop)+RP2(12,pop)+RP2(13,pop)
         + RP2(14,pop)+RP2(15,pop);
}
static uint64_t rp_c = 0, ro_c = 0;   // cumulative ring pushes/pops

// full fabric state dump: core FSM/bound/id + buffer occupancy + the
// flit (dst) sitting at every ring slice head
#define RP(g, f) root->q_fabric_top__DOT__nodes__BRA__##g##__KET____DOT__u_pipe__DOT__##f
static void fabric_dump() {
    for (int g = 0; g < NCELL; g++) {
        Vq_fabric_top_q_cell* c = cell[g];
        printf("   cell%2d: state=%2d bound=%d id=%x tp=%d in=%d%d eg=%d%d\n",
               g, c->u_core__DOT__state, c->u_core__DOT__bound,
               c->u_core__DOT__cell_id, c->u_core__DOT__tick_pend,
               c->u_inbuf__DOT__a_v, c->u_inbuf__DOT__b_v,
               c->u_egbuf__DOT__a_v, c->u_egbuf__DOT__b_v);
    }
    printf("   ring heads (pipe:valid,dst a/b):");
    int dsts[NB];
    dsts[0]=RP(0,m_dst); dsts[1]=RP(1,m_dst); dsts[2]=RP(2,m_dst); dsts[3]=RP(3,m_dst);
    dsts[4]=RP(4,m_dst); dsts[5]=RP(5,m_dst); dsts[6]=RP(6,m_dst); dsts[7]=RP(7,m_dst);
    dsts[8]=RP(8,m_dst); dsts[9]=RP(9,m_dst); dsts[10]=RP(10,m_dst); dsts[11]=RP(11,m_dst);
    dsts[12]=RP(12,m_dst); dsts[13]=RP(13,m_dst); dsts[14]=RP(14,m_dst); dsts[15]=RP(15,m_dst);
    for (int g = 0; g < NB; g++)
        printf(" %d:%d%d,%x", g,
               g==0?RP(0,a_v):g==1?RP(1,a_v):g==2?RP(2,a_v):g==3?RP(3,a_v):
               g==4?RP(4,a_v):g==5?RP(5,a_v):g==6?RP(6,a_v):g==7?RP(7,a_v):
               g==8?RP(8,a_v):g==9?RP(9,a_v):g==10?RP(10,a_v):g==11?RP(11,a_v):
               g==12?RP(12,a_v):g==13?RP(13,a_v):g==14?RP(14,a_v):RP(15,a_v),
               g==0?RP(0,b_v):g==1?RP(1,b_v):g==2?RP(2,b_v):g==3?RP(3,b_v):
               g==4?RP(4,b_v):g==5?RP(5,b_v):g==6?RP(6,b_v):g==7?RP(7,b_v):
               g==8?RP(8,b_v):g==9?RP(9,b_v):g==10?RP(10,b_v):g==11?RP(11,b_v):
               g==12?RP(12,b_v):g==13?RP(13,b_v):g==14?RP(14,b_v):RP(15,b_v),
               dsts[g]);
    printf("\n");
}

static inline bool ledger_ok() {
    return (int64_t)(c_inj + c_emit - c_accept - c_drain) == occ_all();
}

static void ledger_breakdown() {
    int ring = 0, inb = 0, egb = 0;
    ring += RING_PIPE_A(0)  + RING_PIPE_B(0);  ring += RING_PIPE_A(1)  + RING_PIPE_B(1);
    ring += RING_PIPE_A(2)  + RING_PIPE_B(2);  ring += RING_PIPE_A(3)  + RING_PIPE_B(3);
    ring += RING_PIPE_A(4)  + RING_PIPE_B(4);  ring += RING_PIPE_A(5)  + RING_PIPE_B(5);
    ring += RING_PIPE_A(6)  + RING_PIPE_B(6);  ring += RING_PIPE_A(7)  + RING_PIPE_B(7);
    ring += RING_PIPE_A(8)  + RING_PIPE_B(8);  ring += RING_PIPE_A(9)  + RING_PIPE_B(9);
    ring += RING_PIPE_A(10) + RING_PIPE_B(10); ring += RING_PIPE_A(11) + RING_PIPE_B(11);
    ring += RING_PIPE_A(12) + RING_PIPE_B(12); ring += RING_PIPE_A(13) + RING_PIPE_B(13);
    ring += RING_PIPE_A(14) + RING_PIPE_B(14); ring += RING_PIPE_A(15) + RING_PIPE_B(15);
    for (int g = 0; g < NCELL; g++) {
        inb += cell[g]->u_inbuf__DOT__a_v + cell[g]->u_inbuf__DOT__b_v;
        egb += cell[g]->u_egbuf__DOT__a_v + cell[g]->u_egbuf__DOT__b_v;
    }
    printf("   [ring=%d inbuf=%d egbuf=%d]\n", ring, inb, egb);
}

static void check_periodic() {
    if (!ledger_ok()) {
        printf("FAIL LEDGER @cyc=%llu: net=%lld occ=%d (inj=%llu emit=%llu "
               "acc=%llu drain=%llu)\n", (unsigned long long)cyc,
               (long long)(c_inj + c_emit - c_accept - c_drain), occ_all(),
               (unsigned long long)c_inj, (unsigned long long)c_emit,
               (unsigned long long)c_accept, (unsigned long long)c_drain);
        ledger_breakdown();
        if (!traced) {                    // dump the last 64 cycles once
            traced = true;
            fabric_dump();
            printf("   --- cycle trace (oldest first) ---\n");
            for (int k = 0; k < 64; k++) {
                char* s = tring[(ti + k) & 63];
                if (s[0]) printf("   %s\n", s);
            }
        }
        errors++;
    }
    if (resp_pending && cyc - oldest_resp_cyc > ACK_TIMEOUT) {
        printf("FAIL ACKLAT @cyc=%llu: %llu outstanding, oldest %llu cyc\n",
               (unsigned long long)cyc, (unsigned long long)resp_pending,
               (unsigned long long)(cyc - oldest_resp_cyc));
        errors++;
        resp_pending = 0;                  // don't re-fire every check
    }
    if (cyc - last_activity > PROG_TIMEOUT && want_inject) {
        printf("FAIL PROG @cyc=%llu: no handshake for %llu cycles\n",
               (unsigned long long)cyc,
               (unsigned long long)(cyc - last_activity));
        errors++;
        want_inject = false;               // park; phase loop will notice
    }
}

// advance exactly one clock; drive inputs from phase state first
static void step() {
    // --- drive (changes land at the coming posedge, negedge-style) ---
    if (in_pend && saw_o_rdy) in_pend = false;      // committed last edge
    if (!in_pend && want_inject) {
        in_op = w_op; in_src = w_src; in_dst = w_dst;
        in_a0 = w_a0; in_a1 = w_a1; in_dat = w_dat;
        in_pend = true;
    }
    top->i_val = in_pend;
    top->i_op = in_op; top->i_src = in_src; top->i_dst = in_dst;
    top->i_a0 = in_a0; top->i_a1 = in_a1; top->i_a2 = 0; top->i_dat = in_dat;
    top->i_rdy = i_rdy_en;

    top->clk = 0; top->eval();              // negedge settle

    // --- sample pre-edge combinational state (transfers this posedge) ---
    saw_o_rdy = top->o_rdy;
    saw_o_val = top->o_val;
    out_op = top->o_op; out_dst = top->o_dst; out_dat = top->o_dat;

    bool act = false;
    char* tr = tring[ti]; ti = (ti + 1) & 63; tr[0] = 0;
    if (top->i_val && saw_o_rdy) { c_inj++; act = true;
        sprintf(tr + strlen(tr), "I"); }
    if (saw_o_val && top->i_rdy) {
        c_drain++; act = true;
        sprintf(tr + strlen(tr), "D%d", out_op);
        if (resp_pending) resp_pending--;
        if (out_dst != EXTID) {
            printf("FAIL ACKDST @cyc=%llu: egress dst=%x\n",
                   (unsigned long long)cyc, out_dst);
            errors++;
        }
    }
    for (int g = 0; g < NCELL; g++) {
        Vq_fabric_top_q_cell* c = cell[g];
        if (c->eg_s_valid && c->eg_s_ready) {       // core -> network
            c_emit++; act = true;
            if (c->eg_op == OP_EFF) c_emit_fire++; else c_emit_ack++;
            sprintf(tr + strlen(tr), " E%d:%d", g, c->eg_op);
        }
        if (c->ci_valid && c->ci_ready_w) {         // network -> core
            c_accept++; act = true;
            if (c->ci_op == OP_EFF) c_accept_eff++;
            else if (c->ci_op == OP_VIEW) c_accept_view++;
            else c_accept_other++;
            sprintf(tr + strlen(tr), " A%d:%d", g, c->ci_op);
        }
        if (c->ovf_vec) c_ovf_cells++;
    }
    if (root->q_fabric_top__DOT__tick) { c_ticks++; act = true; }
    if (act) last_activity = cyc;
    rp_c += ring_pushes(); ro_c += ring_pops();

    top->clk = 1; top->eval();              // posedge commit
    cyc++;
    {
        int ring = 0, inb = 0, egb = 0;
        ring += RING_PIPE_A(0)+RING_PIPE_B(0); ring += RING_PIPE_A(1)+RING_PIPE_B(1);
        ring += RING_PIPE_A(2)+RING_PIPE_B(2); ring += RING_PIPE_A(3)+RING_PIPE_B(3);
        ring += RING_PIPE_A(4)+RING_PIPE_B(4); ring += RING_PIPE_A(5)+RING_PIPE_B(5);
        ring += RING_PIPE_A(6)+RING_PIPE_B(6); ring += RING_PIPE_A(7)+RING_PIPE_B(7);
        ring += RING_PIPE_A(8)+RING_PIPE_B(8); ring += RING_PIPE_A(9)+RING_PIPE_B(9);
        ring += RING_PIPE_A(10)+RING_PIPE_B(10); ring += RING_PIPE_A(11)+RING_PIPE_B(11);
        ring += RING_PIPE_A(12)+RING_PIPE_B(12); ring += RING_PIPE_A(13)+RING_PIPE_B(13);
        ring += RING_PIPE_A(14)+RING_PIPE_B(14); ring += RING_PIPE_A(15)+RING_PIPE_B(15);
        for (int g = 0; g < NCELL; g++) {
            inb += cell[g]->u_inbuf__DOT__a_v + cell[g]->u_inbuf__DOT__b_v;
            egb += cell[g]->u_egbuf__DOT__a_v + cell[g]->u_egbuf__DOT__b_v;
        }
        sprintf(tring[(ti + 63) & 63] + strlen(tring[(ti + 63) & 63]),
                " @%llu occ=%d(r%d i%d e%d) net=%lld rpp=%lld pp=[%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d]",
                (unsigned long long)cyc, ring+inb+egb, ring, inb, egb,
                (long long)(c_inj + c_emit - c_accept - c_drain),
                (long long)(rp_c - ro_c),
                RP2(0,push),RP2(1,push),RP2(2,push),RP2(3,push),
                RP2(4,push),RP2(5,push),RP2(6,push),RP2(7,push),
                RP2(8,push),RP2(9,push),RP2(10,push),RP2(11,push),
                RP2(12,push),RP2(13,push),RP2(14,push),RP2(15,push));
    }
}

static void run(uint64_t n) {
    for (uint64_t i = 0; i < n; i++) {
        step();
        if ((cyc & 0xFF) == 0) check_periodic();
    }
}

// inject one flit and wait only for its commit (no ack expected:
// link acks are addressed to the PEER, not EXTID -- see ST_RESP,
// q_cell_core; confirm links afterwards via wsum views, smoke-TB style)
static void xfer_noack(uint8_t op, uint8_t src, uint8_t dst,
                       uint16_t a0, uint16_t a1, uint16_t dat,
                       uint64_t timeout = 4096) {
    uint64_t inj_b = c_inj, t0 = cyc;
    w_op = op; w_src = src; w_dst = dst; w_a0 = a0; w_a1 = a1; w_dat = dat;
    want_inject = true;
    while (c_inj == inj_b) {
        step();
        if (cyc - t0 > timeout) {
            printf("FAIL XFER_TIMEOUT @cyc=%llu op=%d dst=%x "
                   "(bench timeout=%llu -- NOT a hardware period)\n",
                   (unsigned long long)cyc, op, dst, (unsigned long long)timeout);
            errors++;
            break;
        }
    }
    want_inject = false; top->i_val = 0; in_pend = false;
    run(512);                       // ring latency + engine set-base settle
}

// blocking transfer: send one flit, wait its ack, return o_dat.
// Commit detection via the ledger counters (c_inj/c_drain bump exactly
// on the commit edge), so the port driver never rewrites fields while a
// transfer is mid-handshake.
static uint16_t xfer(uint8_t op, uint8_t src, uint8_t dst,
                     uint16_t a0, uint16_t a1, uint16_t dat,
                     uint64_t timeout = 4096) {
    uint64_t inj_b = c_inj, drain_b = c_drain, t0 = cyc;
    w_op = op; w_src = src; w_dst = dst; w_a0 = a0; w_a1 = a1; w_dat = dat;
    want_inject = true;
    while (c_inj == inj_b) {
        step();
        if (cyc - t0 > timeout) goto TO;
    }
    want_inject = false; top->i_val = 0; in_pend = false;
    while (c_drain == drain_b) {
        step();
        if (cyc - t0 > timeout) goto TO;
    }
    return out_dat;
TO:
    printf("FAIL XFER_TIMEOUT @cyc=%llu op=%d dst=%x "
           "(bench timeout=%llu -- NOT a hardware period)\n",
           (unsigned long long)cyc, op, dst, (unsigned long long)timeout);
    errors++;
    want_inject = false; top->i_val = 0; in_pend = false;
    return 0xFFFF;
}

// ---------------- deterministic traffic generator ----------------------
static int peer_of[NCELL][EDGES];            // bench mirror of etab

static void gen_traffic(int eff_pct) {
    uint64_t r = xs64();
    if ((r % 100) < (uint64_t)eff_pct) {     // effect to a linked peer
        int dst = (int)((xs64() >> 8) % NCELL);
        int slot = (int)((xs64() >> 16) % EDGES);
        w_op = OP_EFF; w_src = (uint8_t)peer_of[dst][slot];
        w_dst = (uint8_t)dst; w_a0 = 0; w_a1 = 0;
        w_dat = (uint16_t)(0x4000 + (xs64() & 0x3FFF));
    } else {                                  // act view (acks to EXTID)
        int dst = (int)((xs64() >> 8) % NCELL);
        w_op = OP_VIEW; w_src = EXTID; w_dst = (uint8_t)dst;
        w_a0 = 0; w_a1 = 0; w_dat = 0;
        resp_pending++;
        if (resp_pending == 1) oldest_resp_cyc = cyc;
    }
    want_inject = true;
}

static void do_reset(uint64_t n) {
    top->rst_n = 0; top->i_val = 0; in_pend = false; want_inject = false;
    for (uint64_t i = 0; i < n; i++) { top->clk = 0; top->eval();
                                       top->clk = 1; top->eval(); cyc++; }
    top->rst_n = 1;
    // rebase ledger: reset cleared every pipe and every counter-source
    c_inj = c_drain = c_emit = c_accept = 0;
    c_accept_eff = c_accept_view = c_accept_other = 0;
    c_emit_ack = c_emit_fire = 0; c_ticks = 0;
    resp_pending = 0; last_activity = cyc;
}

static void setup_fabric() {
    // per-cell dials: fire-prone, v2 features ON (echo gate + RQH)
    static const int ndial = 7;
    static const uint8_t  daddr[ndial] = { 4, 5, 6, 11, 12, 14, 15 };
    static const uint16_t dval[ndial]  = { 8, 0x0800, 2, 2, 0x0010,
                                           0x8008, 0x0008 };
    for (int c = 0; c < NCELL; c++) {
        xfer(OP_BIND, EXTID, (uint8_t)c, (uint16_t)c, 0, 0);   // id bind
        for (int d = 0; d < ndial; d++)
            xfer(OP_BIND, EXTID, (uint8_t)c, daddr[d], dval[d], 0);
        for (int s = 0; s < EDGES; s++) {
            peer_of[c][s] = (c + s + 1) % NCELL;
            xfer_noack(OP_LINK, (uint8_t)peer_of[c][s], (uint8_t)c,
                       (uint16_t)s, 0x0100, 0);
        }
        printf("  setup cell %d done @%llu\n", c, (unsigned long long)cyc);
    }
    // links verified the smoke-TB way: wsum must read back the 4 bases
    for (int c = 0; c < NCELL; c++) {
        uint16_t w = xfer(OP_VIEW, EXTID, (uint8_t)c, 1, 0, 0);
        if (w != 4 * 0x0100) {
            printf("FAIL SETUP_WSUM cell %d: got %04x want 0400\n", c, w);
            errors++;
        }
    }
}

static void quiesce(uint64_t max_wait = 1000000) {
    want_inject = false; top->i_val = 0; in_pend = false;
    uint64_t t0 = cyc;
    while ((occ_all() || resp_pending) && cyc - t0 < max_wait) step();
    if (occ_all() || resp_pending) {
        printf("FAIL QUIESCE @cyc=%llu: occ=%d pending=%llu\n",
               (unsigned long long)cyc, occ_all(),
               (unsigned long long)resp_pending);
        errors++;
        return;
    }
    check_periodic();                        // ledger must be exactly zero
}

static uint64_t fnv = 0xcbf29ce484222325ULL; // FNV-1a 64
static inline void fh(uint64_t v) {
    for (int i = 0; i < 8; i++) { fnv ^= (v >> (8 * i)) & 0xFF;
                                  fnv *= 0x100000001b3ULL; }
}

// full fabric state read via the view path, hashed
static uint64_t state_hash() {
    quiesce();
    fnv = 0xcbf29ce484222325ULL;
    for (int c = 0; c < NCELL; c++) {
        fh(xfer(OP_VIEW, EXTID, (uint8_t)c, 0, 0, 0));            // act
        fh(xfer(OP_VIEW, EXTID, (uint8_t)c, 1, 0, 0));            // wsum
        for (int d = 0; d < 16; d++)
            fh(xfer(OP_VIEW, EXTID, (uint8_t)c, 2, (uint16_t)d, 0)); // dial
    }
    return fnv;
}

static double wall_s(struct timespec a, struct timespec b) {
    return (b.tv_sec - a.tv_sec) + 1e-9 * (b.tv_nsec - a.tv_nsec);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);   // unbuffered: progress is data
    top = new Vq_fabric_top;
    root = top->rootp;
    Vq_fabric_top__Syms* symsp = top->rootp->vlSymsp;
    cell[0]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell;
    cell[1]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell;
    cell[2]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell;
    cell[3]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell;
    cell[4]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell;
    cell[5]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell;
    cell[6]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell;
    cell[7]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell;
    cell[8]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell;
    cell[9]  = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell;
    cell[10] = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell;
    cell[11] = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell;
    cell[12] = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell;
    cell[13] = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell;
    cell[14] = &symsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell;

    printf("== tb_scale_vlt: NCELL=%d EDGES_N=%d (K=8 B=8 AGEW=24), "
           "TPW=8 default\n", NCELL, EDGES);

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    do_reset(16);
    setup_fabric();
    printf("P0 setup: %llu cycles, ledger %s\n",
           (unsigned long long)cyc, ledger_ok() ? "OK" : "FAIL");

    // ---------------- P1: one million cycles, ~10% effects ------------
    const uint64_t MAIN_CYC = 1000000;
    uint64_t p1_inj0 = c_inj, p1_acc0 = c_accept, p1_fire0 = c_emit_fire,
             p1_tick0 = c_ticks;
    struct timespec m0, m1; clock_gettime(CLOCK_MONOTONIC, &m0);
    for (uint64_t i = 0; i < MAIN_CYC; i++) {
        if (!in_pend) gen_traffic(10);   // load next flit only when port free
        step();
        if ((cyc & 0xFF) == 0) check_periodic();
    }
    want_inject = false; top->i_val = 0; in_pend = false;
    clock_gettime(CLOCK_MONOTONIC, &m1);
    double mw = wall_s(m0, m1);
    uint64_t p1_emit = c_emit, p1_fire = c_emit_fire, p1_ticks = c_ticks,
             p1_acc = c_accept;
    printf("P1 MAIN: %llu cycles in %.3f s wall (%.2f Mcyc/s sim rate)\n",
           (unsigned long long)MAIN_CYC, mw, MAIN_CYC / mw / 1e6);
    printf("P1 inj=%llu drain=%llu accept=%llu (eff=%llu view=%llu other=%llu) "
           "emit=%llu (ack=%llu fire=%llu) ticks=%llu\n",
           (unsigned long long)(c_inj - p1_inj0),
           (unsigned long long)c_drain,
           (unsigned long long)p1_acc,
           (unsigned long long)c_accept_eff,
           (unsigned long long)c_accept_view,
           (unsigned long long)c_accept_other,
           (unsigned long long)p1_emit,
           (unsigned long long)(c_emit_ack),
           (unsigned long long)p1_fire,
           (unsigned long long)p1_ticks);
    // cell-ops/sec: accepted ops (bind/view/effect services) + tick decay
    // sweeps (NCELL per tick strobe) + core emissions (acks + fire fanout)
    uint64_t cops = p1_acc + p1_ticks * NCELL + p1_emit;
    printf("P1 CELL-OPS: %llu in %.3f s => %.0f cell-ops/sec "
           "(%llu accepts + %llu tick-sweeps x%d + %llu emissions)\n",
           (unsigned long long)cops, mw, cops / mw,
           (unsigned long long)p1_acc, (unsigned long long)p1_ticks, NCELL,
           (unsigned long long)p1_emit);
    quiesce();

    // ---------------- P2: max-rate effect storm ----------------------
    printf("P2 STORM: 200k cycles, 100%% effects, fire-prone dials\n");
    for (uint64_t i = 0; i < 200000; i++) {
        if (!in_pend) {
            int dst = (int)((xs64() >> 8) % NCELL);
            int slot = (int)((xs64() >> 16) % EDGES);
            w_op = OP_EFF; w_src = (uint8_t)peer_of[dst][slot];
            w_dst = (uint8_t)dst; w_a0 = 0; w_a1 = 0; w_dat = 0x7FFF;
            want_inject = true;
        }
        step();
        if ((cyc & 0xFF) == 0) check_periodic();
    }
    want_inject = false; top->i_val = 0; in_pend = false;
    printf("P2 fires=%llu accepts(eff)=%llu ovf_cell_cycles=%llu\n",
           (unsigned long long)c_emit_fire,
           (unsigned long long)c_accept_eff,
           (unsigned long long)c_ovf_cells);
    quiesce();

    // ---------------- P3: reset mid-pipeline -------------------------
    printf("P3 RESET-MID-PIPELINE: back up network, reset under load\n");
    i_rdy_en = false;                        // stop draining: egress backs up
    for (int i = 0; i < 400; i++) {          // push flits until pipes fill
        int dst = i % NCELL;
        w_op = OP_EFF; w_src = (uint8_t)peer_of[dst][0]; w_dst = (uint8_t)dst;
        w_a0 = 0; w_a1 = 0; w_dat = 0x7FFF; want_inject = true;
        step();
    }
    want_inject = false; top->i_val = 0; in_pend = false;
    printf("P3 occupancy at reset: %d flits in pipes\n", occ_all());
    do_reset(16);                            // reset while pipes non-empty
    i_rdy_en = true;
    run(64);                                 // let it settle post-release
    int stuck = 0;
    for (int g = 0; g < NB; g++)
        stuck += (g < NCELL) ? (cell[g]->u_inbuf__DOT__a_v
                              + cell[g]->u_egbuf__DOT__a_v) : 0;
    printf("P3 post-reset residue after drain window: %d (want 0), "
           "ledger %s\n", stuck, ledger_ok() ? "OK" : "FAIL");
    if (stuck) errors++;
    // recovery: fresh setup + 50k traffic pass must run green
    setup_fabric();
    uint64_t err0 = errors;
    for (uint64_t i = 0; i < 50000; i++) {
        if (!in_pend) gen_traffic(10);
        step();
        if ((cyc & 0xFF) == 0) check_periodic();
    }
    want_inject = false; top->i_val = 0; in_pend = false;
    quiesce();
    printf("P3 recovery pass: %s (errors +%llu)\n",
           errors == err0 ? "CLEAN" : "DIRTY",
           (unsigned long long)(errors - err0));

    // ---------------- P4: determinism hash ---------------------------
    uint64_t h1 = 0, h2 = 0, h3 = 0;
    for (int rep = 0; rep < 3; rep++) {
        rng_state = (rep == 2) ? 0x12345 : 0xC0FFEE;
        do_reset(16); setup_fabric();
        for (uint64_t i = 0; i < 100000; i++) {
            if (!in_pend) gen_traffic(30);
            step();
            if ((cyc & 0xFF) == 0) check_periodic();
        }
        want_inject = false; top->i_val = 0; in_pend = false;
        if (occ_all()) {                       // deadlock liveness guard:
            printf("FAIL P4 LIVENESS rep=%d: occ=%d at hash time -- fabric "
                   "deadlocked, state is degenerate; hash NOT taken "
                   "(comparing hashes of corpses proves nothing)\n",
                   rep, occ_all());
            errors++;
            continue;
        }
        uint64_t h = state_hash();
        if (rep == 0) h1 = h; else if (rep == 1) h2 = h; else h3 = h;
    }
    printf("P4 state hashes: seedA=%016llx seedA'=%016llx seedB=%016llx\n",
           (unsigned long long)h1, (unsigned long long)h2,
           (unsigned long long)h3);
    if (h1 != h2) { printf("FAIL P4 DETERMINISM: same seed, different state\n");
                    errors++; }
    if (h1 == h3) { printf("FAIL P4 HASH-SENSE: different seed, identical "
                           "hash (hash not capturing state?)\n"); errors++; }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    printf("== total: %llu cycles, %.1f s wall, errors=%d => %s\n",
           (unsigned long long)cyc, wall_s(t0, t1), errors,
           errors ? "BENCH FAIL" : "BENCH PASS");
    delete top;
    return errors ? 1 : 0;
}
