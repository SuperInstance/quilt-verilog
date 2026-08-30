// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vq_fabric_top.h for the primary calling header

#include "Vq_fabric_top__pch.h"
#include "Vq_fabric_top___024root.h"

VL_ATTR_COLD void Vq_fabric_top___024root___eval_static(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_static\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vq_fabric_top___024root___eval_final(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_final\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__stl(Vq_fabric_top___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vq_fabric_top___024root___eval_phase__stl(Vq_fabric_top___024root* vlSelf);

VL_ATTR_COLD void Vq_fabric_top___024root___eval_settle(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_settle\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY((0x64U < __VstlIterCount))) {
#ifdef VL_DEBUG
            Vq_fabric_top___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("rtl/q_fabric_top.v", 4, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vq_fabric_top___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__stl(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___dump_triggers__stl\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VstlTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vq_fabric_top___024root___eval_triggers__stl(Vq_fabric_top___024root* vlSelf);
VL_ATTR_COLD void Vq_fabric_top___024root___eval_stl(Vq_fabric_top___024root* vlSelf);

VL_ATTR_COLD bool Vq_fabric_top___024root___eval_phase__stl(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_phase__stl\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vq_fabric_top___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        Vq_fabric_top___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__ico(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___dump_triggers__ico\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VicoTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__act(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___dump_triggers__act\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((2ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(posedge q_fabric_top.nodes[0].conn0.u_cell.clk)\n");
    }
    if ((4ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 2 is active: @(posedge q_fabric_top.nodes[1].connc.u_cell.clk)\n");
    }
    if ((8ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 3 is active: @(posedge q_fabric_top.nodes[2].connc.u_cell.clk)\n");
    }
    if ((0x10ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 4 is active: @(posedge q_fabric_top.nodes[3].connc.u_cell.clk)\n");
    }
    if ((0x20ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 5 is active: @(posedge q_fabric_top.nodes[4].connc.u_cell.clk)\n");
    }
    if ((0x40ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 6 is active: @(posedge q_fabric_top.nodes[5].connc.u_cell.clk)\n");
    }
    if ((0x80ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 7 is active: @(posedge q_fabric_top.nodes[6].connc.u_cell.clk)\n");
    }
    if ((0x100ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 8 is active: @(posedge q_fabric_top.nodes[7].connc.u_cell.clk)\n");
    }
    if ((0x200ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 9 is active: @(posedge q_fabric_top.nodes[8].connc.u_cell.clk)\n");
    }
    if ((0x400ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 10 is active: @(posedge q_fabric_top.nodes[9].connc.u_cell.clk)\n");
    }
    if ((0x800ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 11 is active: @(posedge q_fabric_top.nodes[10].connc.u_cell.clk)\n");
    }
    if ((0x1000ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 12 is active: @(posedge q_fabric_top.nodes[11].connc.u_cell.clk)\n");
    }
    if ((0x2000ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 13 is active: @(posedge q_fabric_top.nodes[12].connc.u_cell.clk)\n");
    }
    if ((0x4000ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 14 is active: @(posedge q_fabric_top.nodes[13].connc.u_cell.clk)\n");
    }
    if ((0x8000ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 15 is active: @(posedge q_fabric_top.nodes[14].connc.u_cell.clk)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__nba(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___dump_triggers__nba\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(posedge q_fabric_top.nodes[0].conn0.u_cell.clk)\n");
    }
    if ((4ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 2 is active: @(posedge q_fabric_top.nodes[1].connc.u_cell.clk)\n");
    }
    if ((8ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 3 is active: @(posedge q_fabric_top.nodes[2].connc.u_cell.clk)\n");
    }
    if ((0x10ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 4 is active: @(posedge q_fabric_top.nodes[3].connc.u_cell.clk)\n");
    }
    if ((0x20ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 5 is active: @(posedge q_fabric_top.nodes[4].connc.u_cell.clk)\n");
    }
    if ((0x40ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 6 is active: @(posedge q_fabric_top.nodes[5].connc.u_cell.clk)\n");
    }
    if ((0x80ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 7 is active: @(posedge q_fabric_top.nodes[6].connc.u_cell.clk)\n");
    }
    if ((0x100ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 8 is active: @(posedge q_fabric_top.nodes[7].connc.u_cell.clk)\n");
    }
    if ((0x200ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 9 is active: @(posedge q_fabric_top.nodes[8].connc.u_cell.clk)\n");
    }
    if ((0x400ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 10 is active: @(posedge q_fabric_top.nodes[9].connc.u_cell.clk)\n");
    }
    if ((0x800ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 11 is active: @(posedge q_fabric_top.nodes[10].connc.u_cell.clk)\n");
    }
    if ((0x1000ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 12 is active: @(posedge q_fabric_top.nodes[11].connc.u_cell.clk)\n");
    }
    if ((0x2000ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 13 is active: @(posedge q_fabric_top.nodes[12].connc.u_cell.clk)\n");
    }
    if ((0x4000ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 14 is active: @(posedge q_fabric_top.nodes[13].connc.u_cell.clk)\n");
    }
    if ((0x8000ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 15 is active: @(posedge q_fabric_top.nodes[14].connc.u_cell.clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vq_fabric_top___024root___ctor_var_reset(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___ctor_var_reset\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->rst_n = VL_RAND_RESET_I(1);
    vlSelf->i_val = VL_RAND_RESET_I(1);
    vlSelf->o_rdy = VL_RAND_RESET_I(1);
    vlSelf->i_op = VL_RAND_RESET_I(3);
    vlSelf->i_src = VL_RAND_RESET_I(4);
    vlSelf->i_dst = VL_RAND_RESET_I(4);
    vlSelf->i_a0 = VL_RAND_RESET_I(16);
    vlSelf->i_a1 = VL_RAND_RESET_I(16);
    vlSelf->i_a2 = VL_RAND_RESET_I(16);
    vlSelf->i_dat = VL_RAND_RESET_I(16);
    vlSelf->o_val = VL_RAND_RESET_I(1);
    vlSelf->i_rdy = VL_RAND_RESET_I(1);
    vlSelf->o_op = VL_RAND_RESET_I(3);
    vlSelf->o_src = VL_RAND_RESET_I(4);
    vlSelf->o_dst = VL_RAND_RESET_I(4);
    vlSelf->o_a0 = VL_RAND_RESET_I(16);
    vlSelf->o_a1 = VL_RAND_RESET_I(16);
    vlSelf->o_a2 = VL_RAND_RESET_I(16);
    vlSelf->o_dat = VL_RAND_RESET_I(16);
    vlSelf->o_ovf = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__i_val = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__o_rdy = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__i_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__i_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__i_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__i_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__i_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__i_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__i_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__o_val = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__i_rdy = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__o_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__o_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__o_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__o_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__o_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__o_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__o_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__o_ovf = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nv = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nr = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nop = VL_RAND_RESET_Q(48);
    vlSelf->q_fabric_top__DOT__nsrc = VL_RAND_RESET_Q(64);
    vlSelf->q_fabric_top__DOT__ndst = VL_RAND_RESET_Q(64);
    VL_RAND_RESET_W(256, vlSelf->q_fabric_top__DOT__na0);
    VL_RAND_RESET_W(256, vlSelf->q_fabric_top__DOT__na1);
    VL_RAND_RESET_W(256, vlSelf->q_fabric_top__DOT__na2);
    VL_RAND_RESET_W(256, vlSelf->q_fabric_top__DOT__ndat);
    vlSelf->q_fabric_top__DOT__pv = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__pr = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__pop = VL_RAND_RESET_Q(48);
    vlSelf->q_fabric_top__DOT__psrc = VL_RAND_RESET_Q(64);
    vlSelf->q_fabric_top__DOT__pdst = VL_RAND_RESET_Q(64);
    VL_RAND_RESET_W(256, vlSelf->q_fabric_top__DOT__pa0);
    VL_RAND_RESET_W(256, vlSelf->q_fabric_top__DOT__pa1);
    VL_RAND_RESET_W(256, vlSelf->q_fabric_top__DOT__pa2);
    VL_RAND_RESET_W(256, vlSelf->q_fabric_top__DOT__pdat);
    vlSelf->q_fabric_top__DOT__tick = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__ovf_cells = VL_RAND_RESET_I(15);
    vlSelf->q_fabric_top__DOT__u_ts__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__u_ts__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__u_ts__DOT__o_tick = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__u_ts__DOT__cnt = VL_RAND_RESET_I(8);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_val = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_rdy = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_val = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_rdy = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__i_myid = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__hit = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__transit = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__inject_ok = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__clk = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__rst_n = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_valid = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_ready = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_op = VL_RAND_RESET_I(3);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_src = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dst = VL_RAND_RESET_I(4);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a0 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a1 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a2 = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dat = VL_RAND_RESET_I(16);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_v = VL_RAND_RESET_I(1);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q);
    VL_RAND_RESET_W(75, vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__push = VL_RAND_RESET_I(1);
    vlSelf->q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__pop = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__clk__0 = VL_RAND_RESET_I(1);
}
