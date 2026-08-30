// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vq_fabric_top.h for the primary calling header

#include "Vq_fabric_top__pch.h"
#include "Vq_fabric_top__Syms.h"
#include "Vq_fabric_top___024root.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__ico(Vq_fabric_top___024root* vlSelf);
#endif  // VL_DEBUG

void Vq_fabric_top___024root___eval_triggers__ico(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_triggers__ico\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered.set(0U, (IData)(vlSelfRef.__VicoFirstIteration));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vq_fabric_top___024root___dump_triggers__ico(vlSelf);
    }
#endif
}

void Vq_fabric_top___024root___ico_sequent__TOP__0(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top___024root___ico_sequent__TOP__1(Vq_fabric_top___024root* vlSelf);

void Vq_fabric_top___024root___eval_ico(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_ico\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        Vq_fabric_top___024root___ico_sequent__TOP__0(vlSelf);
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___ico_sequent__TOP__1(vlSelf);
    }
}

VL_INLINE_OPT void Vq_fabric_top___024root___ico_sequent__TOP__0(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___ico_sequent__TOP__0\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.i_por_n 
        = vlSelfRef.rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__i_val = vlSelfRef.i_val;
    vlSelfRef.q_fabric_top__DOT__i_op = vlSelfRef.i_op;
    vlSelfRef.q_fabric_top__DOT__i_src = vlSelfRef.i_src;
    vlSelfRef.q_fabric_top__DOT__i_dst = vlSelfRef.i_dst;
    vlSelfRef.q_fabric_top__DOT__i_a0 = vlSelfRef.i_a0;
    vlSelfRef.q_fabric_top__DOT__i_a1 = vlSelfRef.i_a1;
    vlSelfRef.q_fabric_top__DOT__i_a2 = vlSelfRef.i_a2;
    vlSelfRef.q_fabric_top__DOT__i_dat = vlSelfRef.i_dat;
    vlSelfRef.q_fabric_top__DOT__i_rdy = vlSelfRef.i_rdy;
    vlSelfRef.q_fabric_top__DOT__pv = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v) 
                                        << 0xfU) | 
                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v) 
                                         << 0xeU) | 
                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v) 
                                          << 0xdU) 
                                         | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v) 
                                             << 0xcU) 
                                            | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v) 
                                                << 0xbU) 
                                               | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v) 
                                                   << 0xaU) 
                                                  | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v) 
                                                      << 9U) 
                                                     | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v) 
                                                         << 8U) 
                                                        | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v) 
                                                            << 7U) 
                                                           | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v) 
                                                               << 6U) 
                                                              | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v) 
                                                                  << 5U) 
                                                                 | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v) 
                                                                     << 4U) 
                                                                    | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v) 
                                                                        << 3U) 
                                                                       | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v) 
                                                                           << 2U) 
                                                                          | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v) 
                                                                              << 1U) 
                                                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.rst_n 
        = vlSelfRef.rst_n;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.clk 
        = vlSelfRef.clk;
    vlSelfRef.q_fabric_top__DOT__clk = vlSelfRef.clk;
    vlSelfRef.q_fabric_top__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__tick = vlSelfRef.q_fabric_top__DOT__u_ts__DOT__o_tick;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_val 
        = vlSelfRef.q_fabric_top__DOT__i_val;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_op 
        = vlSelfRef.q_fabric_top__DOT__i_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_src 
        = vlSelfRef.q_fabric_top__DOT__i_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_dst 
        = vlSelfRef.q_fabric_top__DOT__i_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a0 
        = vlSelfRef.q_fabric_top__DOT__i_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a1 
        = vlSelfRef.q_fabric_top__DOT__i_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a2 
        = vlSelfRef.q_fabric_top__DOT__i_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_dat 
        = vlSelfRef.q_fabric_top__DOT__i_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_rdy 
        = vlSelfRef.q_fabric_top__DOT__i_rdy;
    vlSelfRef.q_fabric_top__DOT__u_ts__DOT__clk = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__clk 
        = vlSelfRef.q_fabric_top__DOT__clk;
    vlSelfRef.q_fabric_top__DOT__u_ts__DOT__rst_n = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__rst_n 
        = vlSelfRef.q_fabric_top__DOT__rst_n;
    vlSelfRef.o_op = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__o_op = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.o_src = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__o_src = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.o_a0 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__o_a0 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.o_a1 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__o_a1 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.o_a2 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__o_a2 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.o_dat = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__o_dat = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready;
    vlSelfRef.q_fabric_top__DOT__nr = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready) 
                                        << 0xfU) | 
                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready) 
                                         << 0xeU) | 
                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready) 
                                          << 0xdU) 
                                         | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready) 
                                             << 0xcU) 
                                            | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready) 
                                                << 0xbU) 
                                               | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready) 
                                                   << 0xaU) 
                                                  | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready) 
                                                      << 9U) 
                                                     | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready) 
                                                         << 8U) 
                                                        | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready) 
                                                            << 7U) 
                                                           | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready) 
                                                               << 6U) 
                                                              | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready) 
                                                                  << 5U) 
                                                                 | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready) 
                                                                     << 4U) 
                                                                    | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready) 
                                                                        << 3U) 
                                                                       | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready) 
                                                                           << 2U) 
                                                                          | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready) 
                                                                              << 1U) 
                                                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__pop = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_op)) 
                                         << 0x2dU) 
                                        | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op)) 
                                            << 0x2aU) 
                                           | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_op)) 
                                               << 0x27U) 
                                              | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_op)) 
                                                  << 0x24U) 
                                                 | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_op)) 
                                                     << 0x21U) 
                                                    | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_op)) 
                                                        << 0x1eU) 
                                                       | (QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_op) 
                                                                           << 0x1bU) 
                                                                          | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_op) 
                                                                              << 0x18U) 
                                                                             | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 0x15U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 0x12U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 0xfU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 9U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 6U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 3U) 
                                                                                | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_op))))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__psrc = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_src)) 
                                          << 0x3cU) 
                                         | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src)) 
                                             << 0x38U) 
                                            | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_src)) 
                                                << 0x34U) 
                                               | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_src)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_src)) 
                                                      << 0x2cU) 
                                                     | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_src)) 
                                                         << 0x28U) 
                                                        | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_src)) 
                                                            << 0x24U) 
                                                           | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_src)) 
                                                               << 0x20U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0x1cU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 4U) 
                                                                                | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_src))))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__pa0[0U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0) 
                                             << 0x10U) 
                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a0));
    vlSelfRef.q_fabric_top__DOT__pa0[1U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[2U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[3U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[4U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[5U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a0) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__pa1[0U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1) 
                                             << 0x10U) 
                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a1));
    vlSelfRef.q_fabric_top__DOT__pa1[1U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[2U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[3U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[4U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[5U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a1) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__pa2[0U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2) 
                                             << 0x10U) 
                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a2));
    vlSelfRef.q_fabric_top__DOT__pa2[1U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[2U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[3U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[4U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[5U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a2) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__pdat[0U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat) 
                                              << 0x10U) 
                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dat));
    vlSelfRef.q_fabric_top__DOT__pdat[1U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[2U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[3U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[4U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[5U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(
                                                        (((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat)))))) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[6U] = (((IData)(
                                                      (((QData)((IData)(
                                                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat)))) 
                                                        << 0x20U) 
                                                       | (QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat)))))) 
                                              >> 0x10U) 
                                             | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat)))) 
                                                           << 0x20U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat) 
                                                                              << 0x10U) 
                                                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat))))) 
                                                         >> 0x20U)) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dat) 
                                              << 0x10U) 
                                             | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat)))) 
                                                           << 0x20U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat) 
                                                                              << 0x10U) 
                                                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat))))) 
                                                         >> 0x20U)) 
                                                >> 0x10U));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSelfRef.o_dst = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__o_dst = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_valid 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v) 
           & (0xfU == (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst)));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__pdst = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dst)) 
                                          << 0x3cU) 
                                         | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst)) 
                                             << 0x38U) 
                                            | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dst)) 
                                                << 0x34U) 
                                               | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dst)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dst)) 
                                                      << 0x2cU) 
                                                     | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dst)) 
                                                         << 0x28U) 
                                                        | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dst)) 
                                                            << 0x24U) 
                                                           | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dst)) 
                                                               << 0x20U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0x1cU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 4U) 
                                                                                | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dst))))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_val;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__i_rdy;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dst;
    if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_valid) {
        vlSelfRef.o_val = 1U;
        vlSelfRef.q_fabric_top__DOT__o_val = 1U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_val = 1U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__hit = 1U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready 
            = vlSelfRef.i_rdy;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed 
            = vlSelfRef.i_rdy;
    } else {
        vlSelfRef.o_val = 0U;
        vlSelfRef.q_fabric_top__DOT__o_val = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_val = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__hit = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed = 0U;
    }
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__inject_ok 
        = (1U & ((~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v)) 
                 | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__transit 
        = ((~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed)) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__inject_ok));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__transit) 
           | ((IData)(vlSelfRef.i_val) & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__inject_ok)));
    if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__transit) {
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    } else {
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op 
            = vlSelfRef.i_op;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src 
            = vlSelfRef.i_src;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst 
            = vlSelfRef.i_dst;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0 
            = vlSelfRef.i_a0;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1 
            = vlSelfRef.i_a1;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2 
            = vlSelfRef.i_a2;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat 
            = vlSelfRef.i_dat;
    }
    vlSelfRef.o_rdy = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready;
    vlSelfRef.q_fabric_top__DOT__o_rdy = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_rdy 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op) 
            << 8U) | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src) 
                       << 4U) | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___ico_sequent__TOP__1(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___ico_sequent__TOP__1\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__ovf_cells = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                               << 0xeU) 
                                              | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                  << 0xdU) 
                                                 | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                     << 0xcU) 
                                                    | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                        << 0xbU) 
                                                       | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                           << 0xaU) 
                                                          | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                              << 9U) 
                                                             | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                 << 8U) 
                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                    << 7U) 
                                                                   | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                       << 6U) 
                                                                      | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                          << 5U) 
                                                                         | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                             << 4U) 
                                                                            | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                                << 3U) 
                                                                               | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                                << 2U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                                << 1U) 
                                                                                | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.o_ovf)))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__pr = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_ready) 
                                        << 0xfU) | 
                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready) 
                                         << 0xeU) | 
                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                          << 0xdU) 
                                         | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                             << 0xcU) 
                                            | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                << 0xbU) 
                                               | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                   << 0xaU) 
                                                  | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                      << 9U) 
                                                     | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                         << 8U) 
                                                        | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                            << 7U) 
                                                           | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                               << 6U) 
                                                              | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                  << 5U) 
                                                                 | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                     << 4U) 
                                                                    | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                        << 3U) 
                                                                       | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                           << 2U) 
                                                                          | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                              << 1U) 
                                                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_ready))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nv = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid) 
                                        << 0xfU) | 
                                       (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                         << 0xeU) | 
                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                          << 0xdU) 
                                         | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                             << 0xcU) 
                                            | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                << 0xbU) 
                                               | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                   << 0xaU) 
                                                  | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                      << 9U) 
                                                     | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                         << 8U) 
                                                        | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                            << 7U) 
                                                           | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                               << 6U) 
                                                              | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                  << 5U) 
                                                                 | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                     << 4U) 
                                                                    | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                        << 3U) 
                                                                       | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                           << 2U) 
                                                                          | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                              << 1U) 
                                                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_valid))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nop = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op)) 
                                         << 0x2dU) 
                                        | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                            << 0x2aU) 
                                           | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                               << 0x27U) 
                                              | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                                  << 0x24U) 
                                                 | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                                     << 0x21U) 
                                                    | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                                        << 0x1eU) 
                                                       | (QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                           << 0x1bU) 
                                                                          | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                              << 0x18U) 
                                                                             | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 0x15U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 0x12U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 0xfU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 9U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 6U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 3U) 
                                                                                | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_op))))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nsrc = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src)) 
                                          << 0x3cU) 
                                         | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                             << 0x38U) 
                                            | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                << 0x34U) 
                                               | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                      << 0x2cU) 
                                                     | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                         << 0x28U) 
                                                        | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                            << 0x24U) 
                                                           | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                               << 0x20U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0x1cU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 4U) 
                                                                                | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_src))))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__ndst = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst)) 
                                          << 0x3cU) 
                                         | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                             << 0x38U) 
                                            | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                << 0x34U) 
                                               | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                      << 0x2cU) 
                                                     | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                         << 0x28U) 
                                                        | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                            << 0x24U) 
                                                           | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                               << 0x20U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0x1cU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 4U) 
                                                                                | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dst))))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__na0[0U] = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                             << 0x10U) 
                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a0));
    vlSelfRef.q_fabric_top__DOT__na0[1U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[2U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[3U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[4U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[5U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__na1[0U] = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                             << 0x10U) 
                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a1));
    vlSelfRef.q_fabric_top__DOT__na1[1U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[2U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[3U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[4U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[5U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__na2[0U] = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                             << 0x10U) 
                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a2));
    vlSelfRef.q_fabric_top__DOT__na2[1U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[2U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[3U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[4U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[5U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dst)));
    vlSelfRef.q_fabric_top__DOT__ndat[0U] = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                              << 0x10U) 
                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dat));
    vlSelfRef.q_fabric_top__DOT__ndat[1U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[2U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[3U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[4U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[5U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(
                                                        (((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat)))))) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[6U] = (((IData)(
                                                      (((QData)((IData)(
                                                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                                                        << 0x20U) 
                                                       | (QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat)))))) 
                                              >> 0x10U) 
                                             | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                                                           << 0x20U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                              << 0x10U) 
                                                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat))))) 
                                                         >> 0x20U)) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat) 
                                              << 0x10U) 
                                             | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                                                           << 0x20U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                              << 0x10U) 
                                                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat))))) 
                                                         >> 0x20U)) 
                                                >> 0x10U));
    vlSelfRef.o_ovf = (0U != (IData)(vlSelfRef.q_fabric_top__DOT__ovf_cells));
    vlSelfRef.q_fabric_top__DOT__o_ovf = vlSelfRef.o_ovf;
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__act(Vq_fabric_top___024root* vlSelf);
#endif  // VL_DEBUG

void Vq_fabric_top___024root___eval_triggers__act(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_triggers__act\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered.set(0U, ((IData)(vlSelfRef.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0))));
    vlSelfRef.__VactTriggered.set(1U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(2U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(3U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(4U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(5U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(6U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(7U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(8U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(9U, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.clk) 
                                       & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(0xaU, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.clk) 
                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(0xbU, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.clk) 
                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(0xcU, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.clk) 
                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(0xdU, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.clk) 
                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(0xeU, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.clk) 
                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__VactTriggered.set(0xfU, ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.clk) 
                                         & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__clk__0))));
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__clk__0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.clk;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vq_fabric_top___024root___dump_triggers__act(vlSelf);
    }
#endif
}

void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top___024root___nba_sequent__TOP__0(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__1(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__0(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__1(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__2(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__3(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__4(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__5(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__6(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__7(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__8(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__9(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__10(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__11(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__12(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__13(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__14(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__15(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___nba_comb__TOP__16(Vq_fabric_top___024root* vlSelf);

void Vq_fabric_top___024root___eval_nba(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_nba\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell));
    }
    if ((4ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell));
    }
    if ((8ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x10ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x20ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x40ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x80ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x100ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x200ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x400ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x800ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x1000ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x2000ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x4000ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell));
    }
    if ((0x8000ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell));
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top___024root___nba_sequent__TOP__0(vlSelf);
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell__1((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell));
    }
    if ((0xfffeULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top___024root___nba_comb__TOP__0(vlSelf);
    }
    if ((3ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__1(vlSelf);
    }
    if ((5ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__2(vlSelf);
    }
    if ((9ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__3(vlSelf);
    }
    if ((0x11ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__4(vlSelf);
    }
    if ((0x21ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__5(vlSelf);
    }
    if ((0x41ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__6(vlSelf);
    }
    if ((0x81ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__7(vlSelf);
    }
    if ((0x101ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__8(vlSelf);
    }
    if ((0x201ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__9(vlSelf);
    }
    if ((0x401ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__10(vlSelf);
    }
    if ((0x801ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__11(vlSelf);
    }
    if ((0x1001ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__12(vlSelf);
    }
    if ((0x2001ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__13(vlSelf);
    }
    if ((0x4001ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__14(vlSelf);
    }
    if ((0x8001ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top_q_cell___nba_comb__TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell__0((&vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell));
        Vq_fabric_top___024root___nba_comb__TOP__15(vlSelf);
    }
    if ((0xffffULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_fabric_top___024root___nba_comb__TOP__16(vlSelf);
    }
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_sequent__TOP__0(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_sequent__TOP__0\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*7:0*/ __Vdly__q_fabric_top__DOT__u_ts__DOT__cnt;
    __Vdly__q_fabric_top__DOT__u_ts__DOT__cnt = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v = 0;
    // Body
    __Vdly__q_fabric_top__DOT__u_ts__DOT__cnt = vlSelfRef.q_fabric_top__DOT__u_ts__DOT__cnt;
    __Vdly__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v;
    __Vdly__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v;
    if (vlSelfRef.rst_n) {
        __Vdly__q_fabric_top__DOT__u_ts__DOT__cnt = 
            (0xffU & ((IData)(1U) + (IData)(vlSelfRef.q_fabric_top__DOT__u_ts__DOT__cnt)));
        vlSelfRef.q_fabric_top__DOT__u_ts__DOT__o_tick 
            = (0U == (IData)(vlSelfRef.q_fabric_top__DOT__u_ts__DOT__cnt));
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__pop) {
            __Vdly__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_v;
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[0U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[0U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[1U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[1U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U] 
                = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[2U];
            vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_v = 0U;
        }
        if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__push) {
            if (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__pop)))) {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[2U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_v = 1U;
            } else {
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[0U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[0U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[1U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[1U];
                vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U] 
                    = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[2U];
                __Vdly__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v = 1U;
            }
        }
    } else {
        __Vdly__q_fabric_top__DOT__u_ts__DOT__cnt = 0U;
        vlSelfRef.q_fabric_top__DOT__u_ts__DOT__o_tick = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
        __Vdly__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_v = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[0U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[1U] = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_q[2U] = 0U;
    }
    vlSelfRef.q_fabric_top__DOT__u_ts__DOT__cnt = __Vdly__q_fabric_top__DOT__u_ts__DOT__cnt;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v 
        = __Vdly__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__tick = vlSelfRef.q_fabric_top__DOT__u_ts__DOT__o_tick;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready 
        = (1U & (~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__b_v)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__pv = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v) 
                                        << 0xfU) | 
                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v) 
                                         << 0xeU) | 
                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v) 
                                          << 0xdU) 
                                         | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v) 
                                             << 0xcU) 
                                            | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v) 
                                                << 0xbU) 
                                               | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v) 
                                                   << 0xaU) 
                                                  | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v) 
                                                      << 9U) 
                                                     | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v) 
                                                         << 8U) 
                                                        | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v) 
                                                            << 7U) 
                                                           | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v) 
                                                               << 6U) 
                                                              | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v) 
                                                                  << 5U) 
                                                                 | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v) 
                                                                     << 4U) 
                                                                    | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v) 
                                                                        << 3U) 
                                                                       | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v) 
                                                                           << 2U) 
                                                                          | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v) 
                                                                              << 1U) 
                                                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_op 
        = (7U & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U] 
                 >> 8U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_src 
        = (0xfU & (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U] 
                   >> 4U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[1U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[1U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2 
        = (vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[0U] 
           >> 0x10U);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat 
        = (0xffffU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[0U]);
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dst 
        = (0xfU & vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_q[2U]);
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.s_tick 
        = vlSelfRef.q_fabric_top__DOT__tick;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_valid;
    vlSelfRef.o_op = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__o_op = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.o_src = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__o_src = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.o_a0 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__o_a0 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.o_a1 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__o_a1 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.o_a2 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__o_a2 = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.o_dat = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__o_dat = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.o_dst = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__o_dst = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_valid 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v) 
           & (0xfU == (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dst;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_op;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_src;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat;
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nr = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready) 
                                        << 0xfU) | 
                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready) 
                                         << 0xeU) | 
                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready) 
                                          << 0xdU) 
                                         | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready) 
                                             << 0xcU) 
                                            | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready) 
                                                << 0xbU) 
                                               | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready) 
                                                   << 0xaU) 
                                                  | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready) 
                                                      << 9U) 
                                                     | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready) 
                                                         << 8U) 
                                                        | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready) 
                                                            << 7U) 
                                                           | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready) 
                                                               << 6U) 
                                                              | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready) 
                                                                  << 5U) 
                                                                 | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready) 
                                                                     << 4U) 
                                                                    | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready) 
                                                                        << 3U) 
                                                                       | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready) 
                                                                           << 2U) 
                                                                          | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready) 
                                                                              << 1U) 
                                                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready;
    vlSelfRef.q_fabric_top__DOT__pop = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_op)) 
                                         << 0x2dU) 
                                        | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op)) 
                                            << 0x2aU) 
                                           | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_op)) 
                                               << 0x27U) 
                                              | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_op)) 
                                                  << 0x24U) 
                                                 | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_op)) 
                                                     << 0x21U) 
                                                    | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_op)) 
                                                        << 0x1eU) 
                                                       | (QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_op) 
                                                                           << 0x1bU) 
                                                                          | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_op) 
                                                                              << 0x18U) 
                                                                             | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 0x15U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 0x12U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 0xfU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 9U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 6U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_op) 
                                                                                << 3U) 
                                                                                | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_op))))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_op;
    vlSelfRef.q_fabric_top__DOT__psrc = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_src)) 
                                          << 0x3cU) 
                                         | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src)) 
                                             << 0x38U) 
                                            | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_src)) 
                                                << 0x34U) 
                                               | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_src)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_src)) 
                                                      << 0x2cU) 
                                                     | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_src)) 
                                                         << 0x28U) 
                                                        | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_src)) 
                                                            << 0x24U) 
                                                           | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_src)) 
                                                               << 0x20U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0x1cU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_src) 
                                                                                << 4U) 
                                                                                | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_src))))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_src;
    vlSelfRef.q_fabric_top__DOT__pa0[0U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0) 
                                             << 0x10U) 
                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a0));
    vlSelfRef.q_fabric_top__DOT__pa0[1U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[2U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[3U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[4U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[5U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a0)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa0[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a0) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a0) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a0))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a0;
    vlSelfRef.q_fabric_top__DOT__pa1[0U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1) 
                                             << 0x10U) 
                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a1));
    vlSelfRef.q_fabric_top__DOT__pa1[1U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[2U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[3U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[4U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[5U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a1)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa1[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a1) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a1) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a1))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a1;
    vlSelfRef.q_fabric_top__DOT__pa2[0U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2) 
                                             << 0x10U) 
                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_a2));
    vlSelfRef.q_fabric_top__DOT__pa2[1U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[2U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[3U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[4U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[5U] = (((0xffffU 
                                              & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_a2)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pa2[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_a2) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_a2) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_a2))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_a2;
    vlSelfRef.q_fabric_top__DOT__pdat[0U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat) 
                                              << 0x10U) 
                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dat));
    vlSelfRef.q_fabric_top__DOT__pdat[1U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[2U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[3U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[4U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[5U] = (((0xffffU 
                                               & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dat)) 
                                              | ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(
                                                        (((QData)((IData)(
                                                                          (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat)))))) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[6U] = (((IData)(
                                                      (((QData)((IData)(
                                                                        (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat)))) 
                                                        << 0x20U) 
                                                       | (QData)((IData)(
                                                                         (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat)))))) 
                                              >> 0x10U) 
                                             | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat)))) 
                                                           << 0x20U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat) 
                                                                              << 0x10U) 
                                                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat))))) 
                                                         >> 0x20U)) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__pdat[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dat) 
                                              << 0x10U) 
                                             | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat)))) 
                                                           << 0x20U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dat) 
                                                                              << 0x10U) 
                                                                             | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dat))))) 
                                                         >> 0x20U)) 
                                                >> 0x10U));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dat;
    vlSelfRef.q_fabric_top__DOT__pdst = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_dst)) 
                                          << 0x3cU) 
                                         | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst)) 
                                             << 0x38U) 
                                            | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dst)) 
                                                << 0x34U) 
                                               | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_dst)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_dst)) 
                                                      << 0x2cU) 
                                                     | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_dst)) 
                                                         << 0x28U) 
                                                        | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_dst)) 
                                                            << 0x24U) 
                                                           | (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_dst)) 
                                                               << 0x20U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0x1cU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_dst) 
                                                                                << 4U) 
                                                                                | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_dst))))))))))))))))));
    vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_dst;
    if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ld_valid) {
        vlSelfRef.o_val = 1U;
        vlSelfRef.q_fabric_top__DOT__o_val = 1U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_val = 1U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__hit = 1U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready 
            = vlSelfRef.i_rdy;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed 
            = vlSelfRef.i_rdy;
    } else {
        vlSelfRef.o_val = 0U;
        vlSelfRef.q_fabric_top__DOT__o_val = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_val = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__hit = 0U;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed = 0U;
    }
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ri_ready 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__inject_ok 
        = (1U & ((~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v)) 
                 | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed)));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__transit 
        = ((~ (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__consumed)) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__inject_ok));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__transit) 
           | ((IData)(vlSelfRef.i_val) & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__inject_ok)));
    if (vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__transit) {
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_op;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_src;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dst;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a0;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a1;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_a2;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat 
            = vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__m_dat;
    } else {
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op 
            = vlSelfRef.i_op;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src 
            = vlSelfRef.i_src;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst 
            = vlSelfRef.i_dst;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0 
            = vlSelfRef.i_a0;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1 
            = vlSelfRef.i_a1;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2 
            = vlSelfRef.i_a2;
        vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat 
            = vlSelfRef.i_dat;
    }
    vlSelfRef.o_rdy = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready;
    vlSelfRef.q_fabric_top__DOT__o_rdy = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__o_rdy 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__li_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_valid 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_op 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_src 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_dst 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a0 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a1 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_a2 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__ro_dat 
        = vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op) 
            << 8U) | (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src) 
                       << 4U) | (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__0(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__0\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__ovf_cells = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                               << 0xeU) 
                                              | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                  << 0xdU) 
                                                 | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                     << 0xcU) 
                                                    | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                        << 0xbU) 
                                                       | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                           << 0xaU) 
                                                          | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                              << 9U) 
                                                             | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                 << 8U) 
                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                    << 7U) 
                                                                   | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                       << 6U) 
                                                                      | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                          << 5U) 
                                                                         | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                             << 4U) 
                                                                            | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                                << 3U) 
                                                                               | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                                << 2U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.o_ovf) 
                                                                                << 1U) 
                                                                                | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.o_ovf)))))))))))))));
    vlSelfRef.o_ovf = (0U != (IData)(vlSelfRef.q_fabric_top__DOT__ovf_cells));
    vlSelfRef.q_fabric_top__DOT__o_ovf = vlSelfRef.o_ovf;
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__1(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__1\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__2(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__2\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__3(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__3\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__4(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__4\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__5(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__5\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__6(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__6\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__7(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__7\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__8(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__8\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__9(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__9\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__10(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__10\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__11(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__11\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__12(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__12\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__13(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__13\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__14(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__14\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__15(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__15\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__m_ready 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_ready;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__pop 
        = ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_ready) 
           & (IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__a_v));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_valid 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_valid;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__push 
        = ((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_ready) 
           & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_valid));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_op 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_op;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_src 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_src;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_dst 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dst;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a0 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a1 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_a2 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_dat 
        = vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat;
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[0U] 
        = (IData)((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                    << 0x30U) | (((QData)((IData)((
                                                   ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                    << 0x10U) 
                                                   | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                  << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat)))));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[1U] 
        = (IData)(((((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                     << 0x30U) | (((QData)((IData)(
                                                   (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                     << 0x10U) 
                                                    | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                   << 0x10U) | (QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                   >> 0x20U));
    vlSelfRef.q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__s_bus[2U] 
        = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_op) 
            << 8U) | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_src) 
                       << 4U) | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dst)));
}

VL_INLINE_OPT void Vq_fabric_top___024root___nba_comb__TOP__16(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___nba_comb__TOP__16\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.q_fabric_top__DOT__pr = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ri_ready) 
                                        << 0xfU) | 
                                       (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ri_ready) 
                                         << 0xeU) | 
                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                          << 0xdU) 
                                         | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                             << 0xcU) 
                                            | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                << 0xbU) 
                                               | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                   << 0xaU) 
                                                  | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                      << 9U) 
                                                     | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                         << 8U) 
                                                        | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                            << 7U) 
                                                           | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                               << 6U) 
                                                              | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                  << 5U) 
                                                                 | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                     << 4U) 
                                                                    | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                        << 3U) 
                                                                       | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                           << 2U) 
                                                                          | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ri_ready) 
                                                                              << 1U) 
                                                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ri_ready))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nv = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_valid) 
                                        << 0xfU) | 
                                       (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                         << 0xeU) | 
                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                          << 0xdU) 
                                         | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                             << 0xcU) 
                                            | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                << 0xbU) 
                                               | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                   << 0xaU) 
                                                  | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                      << 9U) 
                                                     | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                         << 8U) 
                                                        | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                            << 7U) 
                                                           | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                               << 6U) 
                                                              | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                  << 5U) 
                                                                 | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                     << 4U) 
                                                                    | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                        << 3U) 
                                                                       | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                           << 2U) 
                                                                          | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_valid) 
                                                                              << 1U) 
                                                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_valid))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nop = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_op)) 
                                         << 0x2dU) 
                                        | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                            << 0x2aU) 
                                           | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                               << 0x27U) 
                                              | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                                  << 0x24U) 
                                                 | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                                     << 0x21U) 
                                                    | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_op)) 
                                                        << 0x1eU) 
                                                       | (QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                           << 0x1bU) 
                                                                          | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                              << 0x18U) 
                                                                             | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 0x15U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 0x12U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 0xfU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 9U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 6U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_op) 
                                                                                << 3U) 
                                                                                | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_op))))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__nsrc = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_src)) 
                                          << 0x3cU) 
                                         | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                             << 0x38U) 
                                            | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                << 0x34U) 
                                               | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                      << 0x2cU) 
                                                     | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                         << 0x28U) 
                                                        | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                            << 0x24U) 
                                                           | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_src)) 
                                                               << 0x20U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0x1cU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_src) 
                                                                                << 4U) 
                                                                                | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_src))))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__ndst = (((QData)((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dst)) 
                                          << 0x3cU) 
                                         | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                             << 0x38U) 
                                            | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                << 0x34U) 
                                               | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                      << 0x2cU) 
                                                     | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                         << 0x28U) 
                                                        | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                            << 0x24U) 
                                                           | (((QData)((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dst)) 
                                                               << 0x20U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0x1cU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0x18U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0x14U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0x10U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 0xcU) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 8U) 
                                                                                | (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dst) 
                                                                                << 4U) 
                                                                                | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dst))))))))))))))))));
    vlSelfRef.q_fabric_top__DOT__na0[0U] = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                             << 0x10U) 
                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a0));
    vlSelfRef.q_fabric_top__DOT__na0[1U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[2U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[3U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[4U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[5U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a0)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na0[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a0) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a0)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a0) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a0))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[0U] = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                             << 0x10U) 
                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a1));
    vlSelfRef.q_fabric_top__DOT__na1[1U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[2U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[3U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[4U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[5U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a1)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na1[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a1) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a1)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a1) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a1))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[0U] = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                             << 0x10U) 
                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_a2));
    vlSelfRef.q_fabric_top__DOT__na2[1U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[2U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[3U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[4U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[5U] = (((0xffffU 
                                              & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_a2)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                >> 0x10U)) 
                                            | ((IData)(
                                                       (((QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                                         << 0x20U) 
                                                        | (QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2)))))) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[6U] = (((IData)(
                                                     (((QData)((IData)(
                                                                       (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                         << 0x10U) 
                                                                        | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                                       << 0x20U) 
                                                      | (QData)((IData)(
                                                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2)))))) 
                                             >> 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2))))) 
                                                        >> 0x20U)) 
                                               << 0x10U));
    vlSelfRef.q_fabric_top__DOT__na2[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_a2) 
                                             << 0x10U) 
                                            | ((IData)(
                                                       ((((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_a2)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_a2) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_a2))))) 
                                                        >> 0x20U)) 
                                               >> 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[0U] = (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                              << 0x10U) 
                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell.ro_dat));
    vlSelfRef.q_fabric_top__DOT__ndat[1U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[2U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[3U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[4U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[5U] = (((0xffffU 
                                               & (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell.ro_dat)) 
                                              | ((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                 >> 0x10U)) 
                                             | ((IData)(
                                                        (((QData)((IData)(
                                                                          (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                            << 0x10U) 
                                                                           | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                                                          << 0x20U) 
                                                         | (QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat)))))) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[6U] = (((IData)(
                                                      (((QData)((IData)(
                                                                        (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                          << 0x10U) 
                                                                         | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                                                        << 0x20U) 
                                                       | (QData)((IData)(
                                                                         (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                           << 0x10U) 
                                                                          | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat)))))) 
                                              >> 0x10U) 
                                             | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                                                           << 0x20U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                              << 0x10U) 
                                                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat))))) 
                                                         >> 0x20U)) 
                                                << 0x10U));
    vlSelfRef.q_fabric_top__DOT__ndat[7U] = (((IData)(vlSelfRef.q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__ro_dat) 
                                              << 0x10U) 
                                             | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                             << 0x10U) 
                                                                            | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell.ro_dat)))) 
                                                           << 0x20U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell.ro_dat) 
                                                                              << 0x10U) 
                                                                             | (IData)(vlSymsp->TOP__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell.ro_dat))))) 
                                                         >> 0x20U)) 
                                                >> 0x10U));
}
