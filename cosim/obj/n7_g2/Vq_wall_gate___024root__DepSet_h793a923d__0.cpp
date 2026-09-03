// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vq_wall_gate.h for the primary calling header

#include "Vq_wall_gate__pch.h"
#include "Vq_wall_gate___024root.h"

void Vq_wall_gate___024root___eval_act(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

void Vq_wall_gate___024root___nba_sequent__TOP__0(Vq_wall_gate___024root* vlSelf);

void Vq_wall_gate___024root___eval_nba(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((3ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vq_wall_gate___024root___nba_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void Vq_wall_gate___024root___nba_sequent__TOP__0(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___nba_sequent__TOP__0\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ q_wall_gate__DOT__any_pos;
    q_wall_gate__DOT__any_pos = 0;
    CData/*0:0*/ q_wall_gate__DOT__any_neg;
    q_wall_gate__DOT__any_neg = 0;
    SData/*13:0*/ q_wall_gate__DOT__eff;
    q_wall_gate__DOT__eff = 0;
    SData/*13:0*/ q_wall_gate__DOT__ph;
    q_wall_gate__DOT__ph = 0;
    QData/*47:0*/ q_wall_gate__DOT__drift_val;
    q_wall_gate__DOT__drift_val = 0;
    QData/*63:0*/ q_wall_gate__DOT__lprod;
    q_wall_gate__DOT__lprod = 0;
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_h547154ec__0;
    q_wall_gate__DOT____Vlvbound_h547154ec__0 = 0;
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_hbb21dfa5__0;
    q_wall_gate__DOT____Vlvbound_hbb21dfa5__0 = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_reality__0__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_reality__0__Vfuncout = 0;
    SData/*13:0*/ __Vfunc_q_wall_gate__DOT__f_reality__0__ph;
    __Vfunc_q_wall_gate__DOT__f_reality__0__ph = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout = 0;
    SData/*13:0*/ __Vfunc_q_wall_gate__DOT__f_reality__1__ph;
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__5__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_abs__5__Vfuncout = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__5__v;
    __Vfunc_q_wall_gate__DOT__f_abs__5__v = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__6__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_abs__6__Vfuncout = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__6__v;
    __Vfunc_q_wall_gate__DOT__f_abs__6__v = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__7__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_abs__7__Vfuncout = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__7__v;
    __Vfunc_q_wall_gate__DOT__f_abs__7__v = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__8__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_abs__8__Vfuncout = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__8__v;
    __Vfunc_q_wall_gate__DOT__f_abs__8__v = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__9__v;
    __Vfunc_q_wall_gate__DOT__f_abs__9__v = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__10__v;
    __Vfunc_q_wall_gate__DOT__f_abs__10__v = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__11__v;
    __Vfunc_q_wall_gate__DOT__f_abs__11__v = 0;
    SData/*14:0*/ __Vdly__q_wall_gate__DOT__t;
    __Vdly__q_wall_gate__DOT__t = 0;
    SData/*14:0*/ __Vdly__q_wall_gate__DOT__last;
    __Vdly__q_wall_gate__DOT__last = 0;
    QData/*47:0*/ __Vdly__o_events;
    __Vdly__o_events = 0;
    QData/*47:0*/ __Vdly__o_mass;
    __Vdly__o_mass = 0;
    QData/*47:0*/ __Vdly__o_cancels;
    __Vdly__o_cancels = 0;
    QData/*47:0*/ __Vdly__o_chatter;
    __Vdly__o_chatter = 0;
    QData/*47:0*/ __Vdly__o_settles;
    __Vdly__o_settles = 0;
    QData/*47:0*/ __Vdly__o_gopen_tot;
    __Vdly__o_gopen_tot = 0;
    QData/*47:0*/ __Vdly__o_gcomp;
    __Vdly__o_gcomp = 0;
    CData/*0:0*/ __Vdly__o_bail;
    __Vdly__o_bail = 0;
    CData/*1:0*/ __Vdly__q_wall_gate__DOT__st;
    __Vdly__q_wall_gate__DOT__st = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__cnt__v0;
    __VdlySet__q_wall_gate__DOT__cnt__v0 = 0;
    CData/*5:0*/ __VdlyVal__q_wall_gate__DOT__i_lats_reg__v0;
    __VdlyVal__q_wall_gate__DOT__i_lats_reg__v0 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v1;
    __VdlySet__q_wall_gate__DOT__mags__v1 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v2;
    __VdlySet__q_wall_gate__DOT__mags__v2 = 0;
    CData/*5:0*/ __VdlyVal__q_wall_gate__DOT__i_lats_reg__v1;
    __VdlyVal__q_wall_gate__DOT__i_lats_reg__v1 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v4;
    __VdlySet__q_wall_gate__DOT__mags__v4 = 0;
    CData/*5:0*/ __VdlyVal__q_wall_gate__DOT__i_lats_reg__v2;
    __VdlyVal__q_wall_gate__DOT__i_lats_reg__v2 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v6;
    __VdlySet__q_wall_gate__DOT__mags__v6 = 0;
    CData/*5:0*/ __VdlyVal__q_wall_gate__DOT__i_lats_reg__v3;
    __VdlyVal__q_wall_gate__DOT__i_lats_reg__v3 = 0;
    CData/*5:0*/ __VdlyVal__q_wall_gate__DOT__i_lats_reg__v4;
    __VdlyVal__q_wall_gate__DOT__i_lats_reg__v4 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__i_lats_reg__v4;
    __VdlySet__q_wall_gate__DOT__i_lats_reg__v4 = 0;
    CData/*5:0*/ __VdlyVal__q_wall_gate__DOT__i_lats_reg__v5;
    __VdlyVal__q_wall_gate__DOT__i_lats_reg__v5 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__i_lats_reg__v5;
    __VdlySet__q_wall_gate__DOT__i_lats_reg__v5 = 0;
    CData/*5:0*/ __VdlyVal__q_wall_gate__DOT__i_lats_reg__v6;
    __VdlyVal__q_wall_gate__DOT__i_lats_reg__v6 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__i_lats_reg__v6;
    __VdlySet__q_wall_gate__DOT__i_lats_reg__v6 = 0;
    CData/*3:0*/ __VdlyVal__q_wall_gate__DOT__cnt__v1;
    __VdlyVal__q_wall_gate__DOT__cnt__v1 = 0;
    CData/*0:0*/ __VdlyDim0__q_wall_gate__DOT__cnt__v1;
    __VdlyDim0__q_wall_gate__DOT__cnt__v1 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__cnt__v1;
    __VdlySet__q_wall_gate__DOT__cnt__v1 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v7;
    __VdlyVal__q_wall_gate__DOT__mags__v7 = 0;
    CData/*0:0*/ __VdlyDim1__q_wall_gate__DOT__mags__v7;
    __VdlyDim1__q_wall_gate__DOT__mags__v7 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v7;
    __VdlySet__q_wall_gate__DOT__mags__v7 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v8;
    __VdlyVal__q_wall_gate__DOT__mags__v8 = 0;
    CData/*0:0*/ __VdlyDim1__q_wall_gate__DOT__mags__v8;
    __VdlyDim1__q_wall_gate__DOT__mags__v8 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v8;
    __VdlySet__q_wall_gate__DOT__mags__v8 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v9;
    __VdlyVal__q_wall_gate__DOT__mags__v9 = 0;
    CData/*0:0*/ __VdlyDim1__q_wall_gate__DOT__mags__v9;
    __VdlyDim1__q_wall_gate__DOT__mags__v9 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v9;
    __VdlySet__q_wall_gate__DOT__mags__v9 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v10;
    __VdlyVal__q_wall_gate__DOT__mags__v10 = 0;
    CData/*0:0*/ __VdlyDim1__q_wall_gate__DOT__mags__v10;
    __VdlyDim1__q_wall_gate__DOT__mags__v10 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v10;
    __VdlySet__q_wall_gate__DOT__mags__v10 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v11;
    __VdlyVal__q_wall_gate__DOT__mags__v11 = 0;
    CData/*0:0*/ __VdlyDim1__q_wall_gate__DOT__mags__v11;
    __VdlyDim1__q_wall_gate__DOT__mags__v11 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v11;
    __VdlySet__q_wall_gate__DOT__mags__v11 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v12;
    __VdlyVal__q_wall_gate__DOT__mags__v12 = 0;
    CData/*0:0*/ __VdlyDim1__q_wall_gate__DOT__mags__v12;
    __VdlyDim1__q_wall_gate__DOT__mags__v12 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v12;
    __VdlySet__q_wall_gate__DOT__mags__v12 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v13;
    __VdlyVal__q_wall_gate__DOT__mags__v13 = 0;
    CData/*0:0*/ __VdlyDim1__q_wall_gate__DOT__mags__v13;
    __VdlyDim1__q_wall_gate__DOT__mags__v13 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v13;
    __VdlySet__q_wall_gate__DOT__mags__v13 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v14;
    __VdlyVal__q_wall_gate__DOT__mags__v14 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v14;
    __VdlySet__q_wall_gate__DOT__mags__v14 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v15;
    __VdlyVal__q_wall_gate__DOT__mags__v15 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v15;
    __VdlySet__q_wall_gate__DOT__mags__v15 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v16;
    __VdlyVal__q_wall_gate__DOT__mags__v16 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v16;
    __VdlySet__q_wall_gate__DOT__mags__v16 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v17;
    __VdlyVal__q_wall_gate__DOT__mags__v17 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v17;
    __VdlySet__q_wall_gate__DOT__mags__v17 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v18;
    __VdlyVal__q_wall_gate__DOT__mags__v18 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v18;
    __VdlySet__q_wall_gate__DOT__mags__v18 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v19;
    __VdlyVal__q_wall_gate__DOT__mags__v19 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v19;
    __VdlySet__q_wall_gate__DOT__mags__v19 = 0;
    QData/*47:0*/ __VdlyVal__q_wall_gate__DOT__mags__v20;
    __VdlyVal__q_wall_gate__DOT__mags__v20 = 0;
    CData/*0:0*/ __VdlySet__q_wall_gate__DOT__mags__v20;
    __VdlySet__q_wall_gate__DOT__mags__v20 = 0;
    // Body
    __Vdly__q_wall_gate__DOT__last = vlSelfRef.q_wall_gate__DOT__last;
    __Vdly__o_events = vlSelfRef.o_events;
    __Vdly__o_mass = vlSelfRef.o_mass;
    __Vdly__o_cancels = vlSelfRef.o_cancels;
    __Vdly__o_chatter = vlSelfRef.o_chatter;
    __Vdly__o_settles = vlSelfRef.o_settles;
    __Vdly__o_gopen_tot = vlSelfRef.o_gopen_tot;
    __Vdly__o_gcomp = vlSelfRef.o_gcomp;
    __Vdly__o_bail = vlSelfRef.o_bail;
    __Vdly__q_wall_gate__DOT__st = vlSelfRef.q_wall_gate__DOT__st;
    __Vdly__q_wall_gate__DOT__t = vlSelfRef.q_wall_gate__DOT__t;
    __VdlySet__q_wall_gate__DOT__i_lats_reg__v4 = 0U;
    __VdlySet__q_wall_gate__DOT__i_lats_reg__v5 = 0U;
    __VdlySet__q_wall_gate__DOT__i_lats_reg__v6 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v1 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v2 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v4 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v6 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v7 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v8 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v9 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v10 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v11 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v12 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v13 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v14 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v15 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v16 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v17 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v18 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v19 = 0U;
    __VdlySet__q_wall_gate__DOT__mags__v20 = 0U;
    __VdlySet__q_wall_gate__DOT__cnt__v0 = 0U;
    __VdlySet__q_wall_gate__DOT__cnt__v1 = 0U;
    if (vlSelfRef.rst_n) {
        vlSelfRef.o_tval = 0U;
        vlSelfRef.o_gopen = 0U;
        vlSelfRef.o_em_mask = 0U;
        if ((0U == (IData)(vlSelfRef.q_wall_gate__DOT__st))) {
            if (vlSelfRef.i_go) {
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0 
                    = (0x3fU & (IData)(vlSelfRef.i_lats));
                vlSelfRef.q_wall_gate__DOT__lcg_x = 
                    ((0U == (0x7fffffffU & vlSelfRef.i_seed))
                      ? 1U : (0x7fffffffU & vlSelfRef.i_seed));
                vlSelfRef.q_wall_gate__DOT__g = 0x190ULL;
                __Vdly__q_wall_gate__DOT__t = 0U;
                __Vdly__q_wall_gate__DOT__last = 0x7ff6U;
                __VdlySet__q_wall_gate__DOT__cnt__v0 = 1U;
                __VdlyVal__q_wall_gate__DOT__i_lats_reg__v0 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0;
                __Vdly__o_events = 0ULL;
                __Vdly__o_mass = 0ULL;
                __Vdly__o_cancels = 0ULL;
                __Vdly__o_chatter = 0ULL;
                __Vdly__o_settles = 0ULL;
                __Vdly__o_gopen_tot = 0ULL;
                __Vdly__o_gcomp = 0ULL;
                __Vdly__o_bail = 0U;
                __Vdly__q_wall_gate__DOT__st = 1U;
                vlSelfRef.o_running = 1U;
                __VdlySet__q_wall_gate__DOT__mags__v1 = 1U;
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0 
                    = (0x3fU & (IData)((vlSelfRef.i_lats 
                                        >> 6U)));
                __VdlySet__q_wall_gate__DOT__mags__v2 = 1U;
                __VdlyVal__q_wall_gate__DOT__i_lats_reg__v1 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0;
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0 
                    = (0x3fU & (IData)((vlSelfRef.i_lats 
                                        >> 0xcU)));
                __VdlySet__q_wall_gate__DOT__mags__v4 = 1U;
                __VdlyVal__q_wall_gate__DOT__i_lats_reg__v2 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0;
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0 
                    = (0x3fU & (IData)((vlSelfRef.i_lats 
                                        >> 0x12U)));
                __VdlySet__q_wall_gate__DOT__mags__v6 = 1U;
                __VdlyVal__q_wall_gate__DOT__i_lats_reg__v3 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0;
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0 
                    = (0x3fU & (IData)((vlSelfRef.i_lats 
                                        >> 0x18U)));
                __VdlyVal__q_wall_gate__DOT__i_lats_reg__v4 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0;
                __VdlySet__q_wall_gate__DOT__i_lats_reg__v4 = 1U;
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0 
                    = (0x3fU & (IData)((vlSelfRef.i_lats 
                                        >> 0x1eU)));
                __VdlyVal__q_wall_gate__DOT__i_lats_reg__v5 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0;
                __VdlySet__q_wall_gate__DOT__i_lats_reg__v5 = 1U;
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0 
                    = (0x3fU & (IData)((vlSelfRef.i_lats 
                                        >> 0x24U)));
                __VdlyVal__q_wall_gate__DOT__i_lats_reg__v6 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_h66797142__0;
                __VdlySet__q_wall_gate__DOT__i_lats_reg__v6 = 1U;
            }
        } else if ((1U == (IData)(vlSelfRef.q_wall_gate__DOT__st))) {
            vlSelfRef.q_wall_gate__DOT__lcg_x = vlSelfRef.q_wall_gate__DOT__lcg_next;
            vlSelfRef.o_t = (0x3fffU & (IData)(vlSelfRef.q_wall_gate__DOT__t));
            vlSelfRef.o_tval = 1U;
            vlSelfRef.o_nf = vlSelfRef.q_wall_gate__DOT__nf;
            if (vlSelfRef.q_wall_gate__DOT__guard_hit) {
                VL_WRITEF_NX("T %0d %0d 0 0 0\n",0,
                             15,vlSelfRef.q_wall_gate__DOT__t,
                             48,([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__5__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__s_true 
                                          - vlSelfRef.q_wall_gate__DOT__g_now));
                                __Vfunc_q_wall_gate__DOT__f_abs__5__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__5__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__5__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__5__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__5__Vfuncout));
            } else {
                VL_WRITEF_NX("T %0d %0d %0# %0# %0#\n",0,
                             15,vlSelfRef.q_wall_gate__DOT__t,
                             48,([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__6__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__s_true 
                                          - (vlSelfRef.q_wall_gate__DOT__g_now 
                                             + vlSelfRef.q_wall_gate__DOT__net)));
                                __Vfunc_q_wall_gate__DOT__f_abs__6__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__6__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__6__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__6__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__6__Vfuncout),
                             1,(IData)(vlSelfRef.q_wall_gate__DOT__cancel),
                             4,vlSelfRef.q_wall_gate__DOT__nf,
                             1,(IData)(vlSelfRef.q_wall_gate__DOT__open_));
                if (VL_UNLIKELY((1U & (IData)(vlSelfRef.q_wall_gate__DOT__trig)))) {
                    VL_WRITEF_NX("E %0d 0 %0d %0d\n",0,
                                 15,vlSelfRef.q_wall_gate__DOT__t,
                                 48,vlSelfRef.q_wall_gate__DOT__pm_new
                                 [0U],48,vlSelfRef.q_wall_gate__DOT__errs
                                 [0U]);
                }
                if (VL_UNLIKELY((2U & (IData)(vlSelfRef.q_wall_gate__DOT__trig)))) {
                    VL_WRITEF_NX("E %0d 1 %0d %0d\n",0,
                                 15,vlSelfRef.q_wall_gate__DOT__t,
                                 48,vlSelfRef.q_wall_gate__DOT__pm_new
                                 [1U],48,vlSelfRef.q_wall_gate__DOT__errs
                                 [1U]);
                }
                if (VL_UNLIKELY((4U & (IData)(vlSelfRef.q_wall_gate__DOT__trig)))) {
                    VL_WRITEF_NX("E %0d 2 %0d %0d\n",0,
                                 15,vlSelfRef.q_wall_gate__DOT__t,
                                 48,vlSelfRef.q_wall_gate__DOT__pm_new
                                 [2U],48,vlSelfRef.q_wall_gate__DOT__errs
                                 [2U]);
                }
                if (VL_UNLIKELY((8U & (IData)(vlSelfRef.q_wall_gate__DOT__trig)))) {
                    VL_WRITEF_NX("E %0d 3 %0d %0d\n",0,
                                 15,vlSelfRef.q_wall_gate__DOT__t,
                                 48,vlSelfRef.q_wall_gate__DOT__pm_new
                                 [3U],48,vlSelfRef.q_wall_gate__DOT__errs
                                 [3U]);
                }
                if (VL_UNLIKELY((0x10U & (IData)(vlSelfRef.q_wall_gate__DOT__trig)))) {
                    VL_WRITEF_NX("E %0d 4 %0d %0d\n",0,
                                 15,vlSelfRef.q_wall_gate__DOT__t,
                                 48,vlSelfRef.q_wall_gate__DOT__pm_new
                                 [4U],48,vlSelfRef.q_wall_gate__DOT__errs
                                 [4U]);
                }
                if (VL_UNLIKELY((0x20U & (IData)(vlSelfRef.q_wall_gate__DOT__trig)))) {
                    VL_WRITEF_NX("E %0d 5 %0d %0d\n",0,
                                 15,vlSelfRef.q_wall_gate__DOT__t,
                                 48,vlSelfRef.q_wall_gate__DOT__pm_new
                                 [5U],48,vlSelfRef.q_wall_gate__DOT__errs
                                 [5U]);
                }
                if (VL_UNLIKELY((0x40U & (IData)(vlSelfRef.q_wall_gate__DOT__trig)))) {
                    VL_WRITEF_NX("E %0d 6 %0d %0d\n",0,
                                 15,vlSelfRef.q_wall_gate__DOT__t,
                                 48,vlSelfRef.q_wall_gate__DOT__pm_new
                                 [6U],48,vlSelfRef.q_wall_gate__DOT__errs
                                 [6U]);
                }
            }
            if (vlSelfRef.q_wall_gate__DOT__guard_hit) {
                __Vfunc_q_wall_gate__DOT__f_abs__7__v 
                    = (0xffffffffffffULL & (vlSelfRef.q_wall_gate__DOT__s_true 
                                            - vlSelfRef.q_wall_gate__DOT__g_now));
                __Vfunc_q_wall_gate__DOT__f_abs__7__Vfuncout 
                    = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__7__v)
                                             ? (- __Vfunc_q_wall_gate__DOT__f_abs__7__v)
                                             : __Vfunc_q_wall_gate__DOT__f_abs__7__v));
                vlSelfRef.o_resid = __Vfunc_q_wall_gate__DOT__f_abs__7__Vfuncout;
                vlSelfRef.o_cflag = 0U;
                vlSelfRef.q_wall_gate__DOT__g = vlSelfRef.q_wall_gate__DOT__g_now;
                __Vdly__o_bail = 1U;
                __Vdly__q_wall_gate__DOT__st = 2U;
                vlSelfRef.o_running = 0U;
            } else {
                __Vfunc_q_wall_gate__DOT__f_abs__8__v 
                    = (0xffffffffffffULL & (vlSelfRef.q_wall_gate__DOT__s_true 
                                            - (vlSelfRef.q_wall_gate__DOT__g_now 
                                               + vlSelfRef.q_wall_gate__DOT__net)));
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h9637dd8d__0 
                    = vlSelfRef.q_wall_gate__DOT__nf;
                if (vlSelfRef.q_wall_gate__DOT__cancel) {
                    __Vdly__o_cancels = (0xffffffffffffULL 
                                         & (1ULL + vlSelfRef.o_cancels));
                }
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [0U];
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                    = vlSelfRef.q_wall_gate__DOT__errs
                    [0U];
                __Vfunc_q_wall_gate__DOT__f_abs__8__Vfuncout 
                    = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__8__v)
                                             ? (- __Vfunc_q_wall_gate__DOT__f_abs__8__v)
                                             : __Vfunc_q_wall_gate__DOT__f_abs__8__v));
                vlSelfRef.o_em_pm[0U] = (IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0);
                vlSelfRef.o_em_pm[1U] = ((0xffff0000U 
                                          & vlSelfRef.o_em_pm[1U]) 
                                         | (IData)(
                                                   (vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                                                    >> 0x20U)));
                vlSelfRef.o_em_e[0U] = (IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0);
                vlSelfRef.o_em_e[1U] = ((0xffff0000U 
                                         & vlSelfRef.o_em_e[1U]) 
                                        | (IData)((vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                                                   >> 0x20U)));
                vlSelfRef.o_em_mask = vlSelfRef.q_wall_gate__DOT__trig;
                vlSelfRef.o_gopen = vlSelfRef.q_wall_gate__DOT__open_;
                vlSelfRef.o_cflag = vlSelfRef.q_wall_gate__DOT__cancel;
                vlSelfRef.o_resid = __Vfunc_q_wall_gate__DOT__f_abs__8__Vfuncout;
                vlSelfRef.q_wall_gate__DOT__g = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__g_now 
                                                    + vlSelfRef.q_wall_gate__DOT__net));
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [1U];
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                    = vlSelfRef.q_wall_gate__DOT__errs
                    [1U];
                vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [0U];
                vlSelfRef.o_em_pm[1U] = ((0xffffU & 
                                          vlSelfRef.o_em_pm[1U]) 
                                         | ((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0) 
                                            << 0x10U));
                vlSelfRef.o_em_pm[2U] = (((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0) 
                                          >> 0x10U) 
                                         | ((IData)(
                                                    (vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                                                     >> 0x20U)) 
                                            << 0x10U));
                vlSelfRef.o_em_e[1U] = ((0xffffU & 
                                         vlSelfRef.o_em_e[1U]) 
                                        | ((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0) 
                                           << 0x10U));
                vlSelfRef.o_em_e[2U] = (((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0) 
                                         >> 0x10U) 
                                        | ((IData)(
                                                   (vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                                                    >> 0x20U)) 
                                           << 0x10U));
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [2U];
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                    = vlSelfRef.q_wall_gate__DOT__errs
                    [2U];
                if ((0U >= (1U & VL_MODDIVS_III(32, 
                                                VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U))))) {
                    __VdlyVal__q_wall_gate__DOT__cnt__v1 
                        = vlSelfRef.q_wall_gate__DOT____Vlvbound_h9637dd8d__0;
                    __VdlyDim0__q_wall_gate__DOT__cnt__v1 
                        = (1U & VL_MODDIVS_III(32, 
                                               VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)));
                    __VdlySet__q_wall_gate__DOT__cnt__v1 = 1U;
                    __VdlyVal__q_wall_gate__DOT__mags__v7 
                        = vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0;
                    __VdlyDim1__q_wall_gate__DOT__mags__v7 
                        = (1U & VL_MODDIVS_III(32, 
                                               VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)));
                    __VdlySet__q_wall_gate__DOT__mags__v7 = 1U;
                }
                vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [1U];
                vlSelfRef.o_em_pm[3U] = (IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0);
                vlSelfRef.o_em_pm[4U] = ((0xffff0000U 
                                          & vlSelfRef.o_em_pm[4U]) 
                                         | (IData)(
                                                   (vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                                                    >> 0x20U)));
                vlSelfRef.o_em_e[3U] = (IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0);
                vlSelfRef.o_em_e[4U] = ((0xffff0000U 
                                         & vlSelfRef.o_em_e[4U]) 
                                        | (IData)((vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                                                   >> 0x20U)));
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [3U];
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                    = vlSelfRef.q_wall_gate__DOT__errs
                    [3U];
                if (VL_LIKELY((0U >= (1U & VL_MODDIVS_III(32, 
                                                          VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))))) {
                    __VdlyVal__q_wall_gate__DOT__mags__v8 
                        = vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0;
                    __VdlyDim1__q_wall_gate__DOT__mags__v8 
                        = (1U & VL_MODDIVS_III(32, 
                                               VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)));
                    __VdlySet__q_wall_gate__DOT__mags__v8 = 1U;
                }
                vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [2U];
                vlSelfRef.o_em_pm[4U] = ((0xffffU & 
                                          vlSelfRef.o_em_pm[4U]) 
                                         | ((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0) 
                                            << 0x10U));
                vlSelfRef.o_em_pm[5U] = (((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0) 
                                          >> 0x10U) 
                                         | ((IData)(
                                                    (vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                                                     >> 0x20U)) 
                                            << 0x10U));
                vlSelfRef.o_em_e[4U] = ((0xffffU & 
                                         vlSelfRef.o_em_e[4U]) 
                                        | ((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0) 
                                           << 0x10U));
                vlSelfRef.o_em_e[5U] = (((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0) 
                                         >> 0x10U) 
                                        | ((IData)(
                                                   (vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                                                    >> 0x20U)) 
                                           << 0x10U));
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [4U];
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                    = vlSelfRef.q_wall_gate__DOT__errs
                    [4U];
                if (VL_LIKELY((0U >= (1U & VL_MODDIVS_III(32, 
                                                          VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))))) {
                    __VdlyVal__q_wall_gate__DOT__mags__v9 
                        = vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0;
                    __VdlyDim1__q_wall_gate__DOT__mags__v9 
                        = (1U & VL_MODDIVS_III(32, 
                                               VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)));
                    __VdlySet__q_wall_gate__DOT__mags__v9 = 1U;
                }
                vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [3U];
                vlSelfRef.o_em_pm[6U] = (IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0);
                vlSelfRef.o_em_pm[7U] = ((0xffff0000U 
                                          & vlSelfRef.o_em_pm[7U]) 
                                         | (IData)(
                                                   (vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                                                    >> 0x20U)));
                vlSelfRef.o_em_e[6U] = (IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0);
                vlSelfRef.o_em_e[7U] = ((0xffff0000U 
                                         & vlSelfRef.o_em_e[7U]) 
                                        | (IData)((vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                                                   >> 0x20U)));
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [5U];
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                    = vlSelfRef.q_wall_gate__DOT__errs
                    [5U];
                if (VL_LIKELY((0U >= (1U & VL_MODDIVS_III(32, 
                                                          VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))))) {
                    __VdlyVal__q_wall_gate__DOT__mags__v10 
                        = vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0;
                    __VdlyDim1__q_wall_gate__DOT__mags__v10 
                        = (1U & VL_MODDIVS_III(32, 
                                               VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)));
                    __VdlySet__q_wall_gate__DOT__mags__v10 = 1U;
                }
                vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [4U];
                vlSelfRef.o_em_pm[7U] = ((0xffffU & 
                                          vlSelfRef.o_em_pm[7U]) 
                                         | ((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0) 
                                            << 0x10U));
                vlSelfRef.o_em_pm[8U] = (((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0) 
                                          >> 0x10U) 
                                         | ((IData)(
                                                    (vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                                                     >> 0x20U)) 
                                            << 0x10U));
                vlSelfRef.o_em_e[7U] = ((0xffffU & 
                                         vlSelfRef.o_em_e[7U]) 
                                        | ((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0) 
                                           << 0x10U));
                vlSelfRef.o_em_e[8U] = (((IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0) 
                                         >> 0x10U) 
                                        | ((IData)(
                                                   (vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                                                    >> 0x20U)) 
                                           << 0x10U));
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [6U];
                vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                    = vlSelfRef.q_wall_gate__DOT__errs
                    [6U];
                if (VL_LIKELY((0U >= (1U & VL_MODDIVS_III(32, 
                                                          VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))))) {
                    __VdlyVal__q_wall_gate__DOT__mags__v11 
                        = vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0;
                    __VdlyDim1__q_wall_gate__DOT__mags__v11 
                        = (1U & VL_MODDIVS_III(32, 
                                               VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)));
                    __VdlySet__q_wall_gate__DOT__mags__v11 = 1U;
                }
                vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0 
                    = vlSelfRef.q_wall_gate__DOT__pm_new
                    [5U];
                vlSelfRef.o_em_pm[9U] = (IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0);
                vlSelfRef.o_em_pm[0xaU] = (0xffffU 
                                           & (IData)(
                                                     (vlSelfRef.q_wall_gate__DOT____Vlvbound_h3b3f478e__0 
                                                      >> 0x20U)));
                vlSelfRef.o_em_e[9U] = (IData)(vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0);
                vlSelfRef.o_em_e[0xaU] = (0xffffU & (IData)(
                                                            (vlSelfRef.q_wall_gate__DOT____Vlvbound_h257e8aec__0 
                                                             >> 0x20U)));
                if ((0U >= (1U & VL_MODDIVS_III(32, 
                                                VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U))))) {
                    __VdlyVal__q_wall_gate__DOT__mags__v12 
                        = vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0;
                    __VdlyDim1__q_wall_gate__DOT__mags__v12 
                        = (1U & VL_MODDIVS_III(32, 
                                               VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)));
                    __VdlySet__q_wall_gate__DOT__mags__v12 = 1U;
                    vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0 
                        = vlSelfRef.q_wall_gate__DOT__pm_new
                        [6U];
                    __VdlyVal__q_wall_gate__DOT__mags__v13 
                        = vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0;
                    __VdlyDim1__q_wall_gate__DOT__mags__v13 
                        = (1U & VL_MODDIVS_III(32, 
                                               VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)));
                    __VdlySet__q_wall_gate__DOT__mags__v13 = 1U;
                } else {
                    vlSelfRef.q_wall_gate__DOT____Vlvbound_hb12a105e__0 
                        = vlSelfRef.q_wall_gate__DOT__pm_new
                        [6U];
                }
                if ((0U != (IData)(vlSelfRef.q_wall_gate__DOT__nf))) {
                    __Vdly__o_events = (0xffffffffffffULL 
                                        & (vlSelfRef.o_events 
                                           + (QData)((IData)(vlSelfRef.q_wall_gate__DOT__nf))));
                    if ((1U < (IData)(vlSelfRef.q_wall_gate__DOT__neff))) {
                        __Vdly__o_gcomp = (0xffffffffffffULL 
                                           & (vlSelfRef.o_gcomp 
                                              + (QData)((IData)(vlSelfRef.q_wall_gate__DOT__nf))));
                    }
                    if (vlSelfRef.q_wall_gate__DOT__open_) {
                        __Vdly__o_gopen_tot = (0xffffffffffffULL 
                                               & (1ULL 
                                                  + vlSelfRef.o_gopen_tot));
                    }
                    if ((VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)) 
                         == ((IData)(1U) + VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__last))))) {
                        __Vdly__o_chatter = (0xffffffffffffULL 
                                             & (1ULL 
                                                + vlSelfRef.o_chatter));
                    }
                    if ((1U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
                        __Vdly__o_mass = (0xffffffffffffULL 
                                          & (vlSelfRef.o_mass 
                                             + ([&]() {
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__v 
                                            = vlSelfRef.q_wall_gate__DOT__errs
                                            [0U];
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout 
                                            = (0xffffffffffffULL 
                                               & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   ? 
                                                  (- __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   : __Vfunc_q_wall_gate__DOT__f_abs__9__v));
                                    }(), __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout)));
                    }
                    __Vdly__q_wall_gate__DOT__last 
                        = vlSelfRef.q_wall_gate__DOT__t;
                    if ((2U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
                        __Vdly__o_mass = (0xffffffffffffULL 
                                          & (vlSelfRef.o_mass 
                                             + ([&]() {
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__v 
                                            = vlSelfRef.q_wall_gate__DOT__errs
                                            [1U];
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout 
                                            = (0xffffffffffffULL 
                                               & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   ? 
                                                  (- __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   : __Vfunc_q_wall_gate__DOT__f_abs__9__v));
                                    }(), __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout)));
                    }
                    if ((4U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
                        __Vdly__o_mass = (0xffffffffffffULL 
                                          & (vlSelfRef.o_mass 
                                             + ([&]() {
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__v 
                                            = vlSelfRef.q_wall_gate__DOT__errs
                                            [2U];
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout 
                                            = (0xffffffffffffULL 
                                               & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   ? 
                                                  (- __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   : __Vfunc_q_wall_gate__DOT__f_abs__9__v));
                                    }(), __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout)));
                    }
                    if ((8U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
                        __Vdly__o_mass = (0xffffffffffffULL 
                                          & (vlSelfRef.o_mass 
                                             + ([&]() {
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__v 
                                            = vlSelfRef.q_wall_gate__DOT__errs
                                            [3U];
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout 
                                            = (0xffffffffffffULL 
                                               & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   ? 
                                                  (- __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   : __Vfunc_q_wall_gate__DOT__f_abs__9__v));
                                    }(), __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout)));
                    }
                    if ((0x10U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
                        __Vdly__o_mass = (0xffffffffffffULL 
                                          & (vlSelfRef.o_mass 
                                             + ([&]() {
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__v 
                                            = vlSelfRef.q_wall_gate__DOT__errs
                                            [4U];
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout 
                                            = (0xffffffffffffULL 
                                               & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   ? 
                                                  (- __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   : __Vfunc_q_wall_gate__DOT__f_abs__9__v));
                                    }(), __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout)));
                    }
                    if ((0x20U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
                        __Vdly__o_mass = (0xffffffffffffULL 
                                          & (vlSelfRef.o_mass 
                                             + ([&]() {
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__v 
                                            = vlSelfRef.q_wall_gate__DOT__errs
                                            [5U];
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout 
                                            = (0xffffffffffffULL 
                                               & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   ? 
                                                  (- __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   : __Vfunc_q_wall_gate__DOT__f_abs__9__v));
                                    }(), __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout)));
                    }
                    if ((0x40U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
                        __Vdly__o_mass = (0xffffffffffffULL 
                                          & (vlSelfRef.o_mass 
                                             + ([&]() {
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__v 
                                            = vlSelfRef.q_wall_gate__DOT__errs
                                            [6U];
                                        __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout 
                                            = (0xffffffffffffULL 
                                               & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   ? 
                                                  (- __Vfunc_q_wall_gate__DOT__f_abs__9__v)
                                                   : __Vfunc_q_wall_gate__DOT__f_abs__9__v));
                                    }(), __Vfunc_q_wall_gate__DOT__f_abs__9__Vfuncout)));
                    }
                }
                vlSelfRef.q_wall_gate__DOT__dv = ((0U 
                                                   == 
                                                   VL_MODDIVS_III(32, 
                                                                  VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))
                                                   ? 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [0U]
                                                   : 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [0U]);
                vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1 
                    = (0xffffffffffffULL & (VL_LTS_IQQ(48, 1ULL, 
                                                       ([&]() {
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__v 
                                        = vlSelfRef.q_wall_gate__DOT__dv;
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout 
                                        = (0xffffffffffffULL 
                                           & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               ? (- __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               : __Vfunc_q_wall_gate__DOT__f_abs__10__v));
                                }(), __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout))
                                             ? VL_SHIFTRS_QQI(48,48,32, 
                                                              (0xffffffffffffULL 
                                                               & (1ULL 
                                                                  + vlSelfRef.q_wall_gate__DOT__dv)), 1U)
                                             : vlSelfRef.q_wall_gate__DOT__dv));
                __VdlyVal__q_wall_gate__DOT__mags__v14 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1;
                __VdlySet__q_wall_gate__DOT__mags__v14 = 1U;
                vlSelfRef.q_wall_gate__DOT__dv = ((0U 
                                                   == 
                                                   VL_MODDIVS_III(32, 
                                                                  VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))
                                                   ? 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [1U]
                                                   : 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [1U]);
                vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1 
                    = (0xffffffffffffULL & (VL_LTS_IQQ(48, 1ULL, 
                                                       ([&]() {
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__v 
                                        = vlSelfRef.q_wall_gate__DOT__dv;
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout 
                                        = (0xffffffffffffULL 
                                           & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               ? (- __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               : __Vfunc_q_wall_gate__DOT__f_abs__10__v));
                                }(), __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout))
                                             ? VL_SHIFTRS_QQI(48,48,32, 
                                                              (0xffffffffffffULL 
                                                               & (1ULL 
                                                                  + vlSelfRef.q_wall_gate__DOT__dv)), 1U)
                                             : vlSelfRef.q_wall_gate__DOT__dv));
                __VdlyVal__q_wall_gate__DOT__mags__v15 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1;
                __VdlySet__q_wall_gate__DOT__mags__v15 = 1U;
                vlSelfRef.q_wall_gate__DOT__dv = ((0U 
                                                   == 
                                                   VL_MODDIVS_III(32, 
                                                                  VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))
                                                   ? 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [2U]
                                                   : 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [2U]);
                vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1 
                    = (0xffffffffffffULL & (VL_LTS_IQQ(48, 1ULL, 
                                                       ([&]() {
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__v 
                                        = vlSelfRef.q_wall_gate__DOT__dv;
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout 
                                        = (0xffffffffffffULL 
                                           & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               ? (- __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               : __Vfunc_q_wall_gate__DOT__f_abs__10__v));
                                }(), __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout))
                                             ? VL_SHIFTRS_QQI(48,48,32, 
                                                              (0xffffffffffffULL 
                                                               & (1ULL 
                                                                  + vlSelfRef.q_wall_gate__DOT__dv)), 1U)
                                             : vlSelfRef.q_wall_gate__DOT__dv));
                __VdlyVal__q_wall_gate__DOT__mags__v16 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1;
                __VdlySet__q_wall_gate__DOT__mags__v16 = 1U;
                vlSelfRef.q_wall_gate__DOT__dv = ((0U 
                                                   == 
                                                   VL_MODDIVS_III(32, 
                                                                  VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))
                                                   ? 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [3U]
                                                   : 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [3U]);
                vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1 
                    = (0xffffffffffffULL & (VL_LTS_IQQ(48, 1ULL, 
                                                       ([&]() {
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__v 
                                        = vlSelfRef.q_wall_gate__DOT__dv;
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout 
                                        = (0xffffffffffffULL 
                                           & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               ? (- __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               : __Vfunc_q_wall_gate__DOT__f_abs__10__v));
                                }(), __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout))
                                             ? VL_SHIFTRS_QQI(48,48,32, 
                                                              (0xffffffffffffULL 
                                                               & (1ULL 
                                                                  + vlSelfRef.q_wall_gate__DOT__dv)), 1U)
                                             : vlSelfRef.q_wall_gate__DOT__dv));
                __VdlyVal__q_wall_gate__DOT__mags__v17 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1;
                __VdlySet__q_wall_gate__DOT__mags__v17 = 1U;
                vlSelfRef.q_wall_gate__DOT__dv = ((0U 
                                                   == 
                                                   VL_MODDIVS_III(32, 
                                                                  VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))
                                                   ? 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [4U]
                                                   : 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [4U]);
                vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1 
                    = (0xffffffffffffULL & (VL_LTS_IQQ(48, 1ULL, 
                                                       ([&]() {
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__v 
                                        = vlSelfRef.q_wall_gate__DOT__dv;
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout 
                                        = (0xffffffffffffULL 
                                           & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               ? (- __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               : __Vfunc_q_wall_gate__DOT__f_abs__10__v));
                                }(), __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout))
                                             ? VL_SHIFTRS_QQI(48,48,32, 
                                                              (0xffffffffffffULL 
                                                               & (1ULL 
                                                                  + vlSelfRef.q_wall_gate__DOT__dv)), 1U)
                                             : vlSelfRef.q_wall_gate__DOT__dv));
                __VdlyVal__q_wall_gate__DOT__mags__v18 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1;
                __VdlySet__q_wall_gate__DOT__mags__v18 = 1U;
                vlSelfRef.q_wall_gate__DOT__dv = ((0U 
                                                   == 
                                                   VL_MODDIVS_III(32, 
                                                                  VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))
                                                   ? 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [5U]
                                                   : 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [5U]);
                vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1 
                    = (0xffffffffffffULL & (VL_LTS_IQQ(48, 1ULL, 
                                                       ([&]() {
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__v 
                                        = vlSelfRef.q_wall_gate__DOT__dv;
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout 
                                        = (0xffffffffffffULL 
                                           & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               ? (- __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               : __Vfunc_q_wall_gate__DOT__f_abs__10__v));
                                }(), __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout))
                                             ? VL_SHIFTRS_QQI(48,48,32, 
                                                              (0xffffffffffffULL 
                                                               & (1ULL 
                                                                  + vlSelfRef.q_wall_gate__DOT__dv)), 1U)
                                             : vlSelfRef.q_wall_gate__DOT__dv));
                vlSelfRef.q_wall_gate__DOT__dv = ((0U 
                                                   == 
                                                   VL_MODDIVS_III(32, 
                                                                  VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))
                                                   ? 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [6U]
                                                   : 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [6U]);
                __VdlyVal__q_wall_gate__DOT__mags__v19 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1;
                __VdlySet__q_wall_gate__DOT__mags__v19 = 1U;
                vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1 
                    = (0xffffffffffffULL & (VL_LTS_IQQ(48, 1ULL, 
                                                       ([&]() {
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__v 
                                        = vlSelfRef.q_wall_gate__DOT__dv;
                                    __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout 
                                        = (0xffffffffffffULL 
                                           & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               ? (- __Vfunc_q_wall_gate__DOT__f_abs__10__v)
                                               : __Vfunc_q_wall_gate__DOT__f_abs__10__v));
                                }(), __Vfunc_q_wall_gate__DOT__f_abs__10__Vfuncout))
                                             ? VL_SHIFTRS_QQI(48,48,32, 
                                                              (0xffffffffffffULL 
                                                               & (1ULL 
                                                                  + vlSelfRef.q_wall_gate__DOT__dv)), 1U)
                                             : vlSelfRef.q_wall_gate__DOT__dv));
                __VdlyVal__q_wall_gate__DOT__mags__v20 
                    = vlSelfRef.q_wall_gate__DOT____Vlvbound_heee9059e__1;
                __VdlySet__q_wall_gate__DOT__mags__v20 = 1U;
                vlSelfRef.q_wall_gate__DOT__sall = 1U;
                if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__11__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__reads
                                          [0U] - (vlSelfRef.q_wall_gate__DOT__g_now 
                                                  + vlSelfRef.q_wall_gate__DOT__net)));
                                __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__11__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout))) {
                    vlSelfRef.q_wall_gate__DOT__sall = 0U;
                }
                if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__11__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__reads
                                          [1U] - (vlSelfRef.q_wall_gate__DOT__g_now 
                                                  + vlSelfRef.q_wall_gate__DOT__net)));
                                __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__11__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout))) {
                    vlSelfRef.q_wall_gate__DOT__sall = 0U;
                }
                if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__11__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__reads
                                          [2U] - (vlSelfRef.q_wall_gate__DOT__g_now 
                                                  + vlSelfRef.q_wall_gate__DOT__net)));
                                __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__11__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout))) {
                    vlSelfRef.q_wall_gate__DOT__sall = 0U;
                }
                if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__11__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__reads
                                          [3U] - (vlSelfRef.q_wall_gate__DOT__g_now 
                                                  + vlSelfRef.q_wall_gate__DOT__net)));
                                __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__11__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout))) {
                    vlSelfRef.q_wall_gate__DOT__sall = 0U;
                }
                if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__11__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__reads
                                          [4U] - (vlSelfRef.q_wall_gate__DOT__g_now 
                                                  + vlSelfRef.q_wall_gate__DOT__net)));
                                __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__11__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout))) {
                    vlSelfRef.q_wall_gate__DOT__sall = 0U;
                }
                if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__11__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__reads
                                          [5U] - (vlSelfRef.q_wall_gate__DOT__g_now 
                                                  + vlSelfRef.q_wall_gate__DOT__net)));
                                __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__11__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout))) {
                    vlSelfRef.q_wall_gate__DOT__sall = 0U;
                }
                if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                                __Vfunc_q_wall_gate__DOT__f_abs__11__v 
                                    = (0xffffffffffffULL 
                                       & (vlSelfRef.q_wall_gate__DOT__reads
                                          [6U] - (vlSelfRef.q_wall_gate__DOT__g_now 
                                                  + vlSelfRef.q_wall_gate__DOT__net)));
                                __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout 
                                    = (0xffffffffffffULL 
                                       & (VL_GTS_IQQ(48, 0ULL, __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           ? (- __Vfunc_q_wall_gate__DOT__f_abs__11__v)
                                           : __Vfunc_q_wall_gate__DOT__f_abs__11__v));
                            }(), __Vfunc_q_wall_gate__DOT__f_abs__11__Vfuncout))) {
                    vlSelfRef.q_wall_gate__DOT__sall = 0U;
                }
                if (vlSelfRef.q_wall_gate__DOT__sall) {
                    __Vdly__o_settles = (0xffffffffffffULL 
                                         & (1ULL + vlSelfRef.o_settles));
                }
                if ((0x12bfU == VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)))) {
                    __Vdly__q_wall_gate__DOT__st = 2U;
                    vlSelfRef.o_running = 0U;
                } else {
                    __Vdly__q_wall_gate__DOT__t = (0x7fffU 
                                                   & ((IData)(1U) 
                                                      + 
                                                      VL_EXTENDS_II(15,15, (IData)(vlSelfRef.q_wall_gate__DOT__t))));
                }
            }
        } else if (VL_UNLIKELY((2U == (IData)(vlSelfRef.q_wall_gate__DOT__st)))) {
            VL_WRITEF_NX("F %0# %0# %0# %0# %0# %0# %0# %0#\n",0,
                         48,vlSelfRef.o_events,48,vlSelfRef.o_mass,
                         48,vlSelfRef.o_cancels,48,
                         vlSelfRef.o_chatter,48,vlSelfRef.o_settles,
                         48,vlSelfRef.o_gopen_tot,48,
                         vlSelfRef.o_gcomp,1,(IData)(vlSelfRef.o_bail));
            vlSelfRef.o_running = 0U;
        } else {
            __Vdly__q_wall_gate__DOT__st = 0U;
        }
    } else {
        __Vdly__q_wall_gate__DOT__st = 0U;
        vlSelfRef.o_running = 0U;
        __Vdly__o_bail = 0U;
        vlSelfRef.o_tval = 0U;
        vlSelfRef.o_gopen = 0U;
        vlSelfRef.o_em_mask = 0U;
        __Vdly__o_events = 0ULL;
        __Vdly__o_mass = 0ULL;
        __Vdly__o_cancels = 0ULL;
        __Vdly__o_chatter = 0ULL;
        __Vdly__o_settles = 0ULL;
        __Vdly__o_gopen_tot = 0ULL;
        __Vdly__o_gcomp = 0ULL;
    }
    vlSelfRef.q_wall_gate__DOT__last = __Vdly__q_wall_gate__DOT__last;
    vlSelfRef.o_events = __Vdly__o_events;
    vlSelfRef.o_mass = __Vdly__o_mass;
    vlSelfRef.o_cancels = __Vdly__o_cancels;
    vlSelfRef.o_chatter = __Vdly__o_chatter;
    vlSelfRef.o_settles = __Vdly__o_settles;
    vlSelfRef.o_gopen_tot = __Vdly__o_gopen_tot;
    vlSelfRef.o_gcomp = __Vdly__o_gcomp;
    vlSelfRef.o_bail = __Vdly__o_bail;
    vlSelfRef.q_wall_gate__DOT__st = __Vdly__q_wall_gate__DOT__st;
    vlSelfRef.q_wall_gate__DOT__t = __Vdly__q_wall_gate__DOT__t;
    if (__VdlySet__q_wall_gate__DOT__i_lats_reg__v4) {
        vlSelfRef.q_wall_gate__DOT__i_lats_reg[4U] 
            = __VdlyVal__q_wall_gate__DOT__i_lats_reg__v4;
    }
    if (__VdlySet__q_wall_gate__DOT__i_lats_reg__v5) {
        vlSelfRef.q_wall_gate__DOT__i_lats_reg[5U] 
            = __VdlyVal__q_wall_gate__DOT__i_lats_reg__v5;
    }
    if (__VdlySet__q_wall_gate__DOT__i_lats_reg__v6) {
        vlSelfRef.q_wall_gate__DOT__i_lats_reg[6U] 
            = __VdlyVal__q_wall_gate__DOT__i_lats_reg__v6;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v1) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][1U] = 0ULL;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v2) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][2U] = 0ULL;
        vlSelfRef.q_wall_gate__DOT__i_lats_reg[1U] 
            = __VdlyVal__q_wall_gate__DOT__i_lats_reg__v1;
        vlSelfRef.q_wall_gate__DOT__mags[0U][3U] = 0ULL;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v4) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][4U] = 0ULL;
        vlSelfRef.q_wall_gate__DOT__i_lats_reg[2U] 
            = __VdlyVal__q_wall_gate__DOT__i_lats_reg__v2;
        vlSelfRef.q_wall_gate__DOT__mags[0U][5U] = 0ULL;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v6) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][6U] = 0ULL;
        vlSelfRef.q_wall_gate__DOT__i_lats_reg[3U] 
            = __VdlyVal__q_wall_gate__DOT__i_lats_reg__v3;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v7) {
        vlSelfRef.q_wall_gate__DOT__mags[__VdlyDim1__q_wall_gate__DOT__mags__v7][0U] 
            = __VdlyVal__q_wall_gate__DOT__mags__v7;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v8) {
        vlSelfRef.q_wall_gate__DOT__mags[__VdlyDim1__q_wall_gate__DOT__mags__v8][1U] 
            = __VdlyVal__q_wall_gate__DOT__mags__v8;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v9) {
        vlSelfRef.q_wall_gate__DOT__mags[__VdlyDim1__q_wall_gate__DOT__mags__v9][2U] 
            = __VdlyVal__q_wall_gate__DOT__mags__v9;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v10) {
        vlSelfRef.q_wall_gate__DOT__mags[__VdlyDim1__q_wall_gate__DOT__mags__v10][3U] 
            = __VdlyVal__q_wall_gate__DOT__mags__v10;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v11) {
        vlSelfRef.q_wall_gate__DOT__mags[__VdlyDim1__q_wall_gate__DOT__mags__v11][4U] 
            = __VdlyVal__q_wall_gate__DOT__mags__v11;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v12) {
        vlSelfRef.q_wall_gate__DOT__mags[__VdlyDim1__q_wall_gate__DOT__mags__v12][5U] 
            = __VdlyVal__q_wall_gate__DOT__mags__v12;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v13) {
        vlSelfRef.q_wall_gate__DOT__mags[__VdlyDim1__q_wall_gate__DOT__mags__v13][6U] 
            = __VdlyVal__q_wall_gate__DOT__mags__v13;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v14) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][0U] = __VdlyVal__q_wall_gate__DOT__mags__v14;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v15) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][1U] = __VdlyVal__q_wall_gate__DOT__mags__v15;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v16) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][2U] = __VdlyVal__q_wall_gate__DOT__mags__v16;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v17) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][3U] = __VdlyVal__q_wall_gate__DOT__mags__v17;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v18) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][4U] = __VdlyVal__q_wall_gate__DOT__mags__v18;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v19) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][5U] = __VdlyVal__q_wall_gate__DOT__mags__v19;
    }
    if (__VdlySet__q_wall_gate__DOT__mags__v20) {
        vlSelfRef.q_wall_gate__DOT__mags[0U][6U] = __VdlyVal__q_wall_gate__DOT__mags__v20;
    }
    if (__VdlySet__q_wall_gate__DOT__cnt__v0) {
        vlSelfRef.q_wall_gate__DOT__cnt[0U] = 0U;
        vlSelfRef.q_wall_gate__DOT__mags[0U][0U] = 0ULL;
        vlSelfRef.q_wall_gate__DOT__i_lats_reg[0U] 
            = __VdlyVal__q_wall_gate__DOT__i_lats_reg__v0;
    }
    if (__VdlySet__q_wall_gate__DOT__cnt__v1) {
        vlSelfRef.q_wall_gate__DOT__cnt[__VdlyDim0__q_wall_gate__DOT__cnt__v1] 
            = __VdlyVal__q_wall_gate__DOT__cnt__v1;
    }
    q_wall_gate__DOT__lprod = (0x3039ULL + (0x41c64e6dULL 
                                            * (QData)((IData)(vlSelfRef.q_wall_gate__DOT__lcg_x))));
    vlSelfRef.q_wall_gate__DOT__lcg_next = (0x7fffffffU 
                                            & (IData)(q_wall_gate__DOT__lprod));
    q_wall_gate__DOT__drift_val = (0xffffffffffffULL 
                                   & ((QData)((IData)(
                                                      VL_MODDIV_III(32, vlSelfRef.q_wall_gate__DOT__lcg_next, (IData)(0xdU)))) 
                                      - 6ULL));
    vlSelfRef.q_wall_gate__DOT__g_now = (0xffffffffffffULL 
                                         & (vlSelfRef.q_wall_gate__DOT__g 
                                            + q_wall_gate__DOT__drift_val));
    q_wall_gate__DOT__ph = (0x3fffU & VL_MODDIVS_III(32, 
                                                     VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(0xf0U)));
    __Vfunc_q_wall_gate__DOT__f_reality__0__ph = q_wall_gate__DOT__ph;
    vlSelfRef.q_wall_gate__DOT__guard_hit = 0U;
    __Vfunc_q_wall_gate__DOT__f_reality__0__Vfuncout 
        = (0xffffffffffffULL & ((0x60U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__0__ph))
                                 ? (0x190ULL + VL_DIV_QQQ(48, 
                                                          (0xffffffffffffULL 
                                                           & VL_SHIFTL_QQI(48,48,32, (QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__0__ph)), 3U)), 5ULL))
                                 : ((0x90U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__0__ph))
                                     ? (0x229ULL - 
                                        ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__0__ph)) 
                                         - 0x60ULL))
                                     : (0x1f9ULL - 
                                        VL_DIV_QQQ(48, 
                                                   (0xffffffffffffULL 
                                                    & VL_SHIFTL_QQI(48,48,32, 
                                                                    ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__0__ph)) 
                                                                     - 0x90ULL), 3U)), 5ULL)))));
    vlSelfRef.q_wall_gate__DOT__trig = 0U;
    vlSelfRef.q_wall_gate__DOT__s_true = __Vfunc_q_wall_gate__DOT__f_reality__0__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__nf = 0U;
    vlSelfRef.q_wall_gate__DOT__net = 0ULL;
    q_wall_gate__DOT__any_pos = 0U;
    q_wall_gate__DOT__any_neg = 0U;
    q_wall_gate__DOT__eff = (VL_GTES_III(15, (IData)(vlSelfRef.q_wall_gate__DOT__t), 
                                         (0x7fffU & 
                                          VL_EXTENDS_II(15,7, 
                                                        vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                        [0U])))
                              ? (0x3fffU & (VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)) 
                                            - VL_EXTENDS_II(32,7, 
                                                            vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                            [0U])))
                              : 0U);
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = (0x3fffU 
                                                  & VL_MODDIV_III(32, (IData)(q_wall_gate__DOT__eff), (IData)(0xf0U)));
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout 
        = (0xffffffffffffULL & ((0x60U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                 ? (0x190ULL + VL_DIV_QQQ(48, 
                                                          (0xffffffffffffULL 
                                                           & VL_SHIFTL_QQI(48,48,32, (QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)), 3U)), 5ULL))
                                 : ((0x90U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                     ? (0x229ULL - 
                                        ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                         - 0x60ULL))
                                     : (0x1f9ULL - 
                                        VL_DIV_QQQ(48, 
                                                   (0xffffffffffffULL 
                                                    & VL_SHIFTL_QQI(48,48,32, 
                                                                    ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                                                     - 0x90ULL), 3U)), 5ULL)))));
    q_wall_gate__DOT____Vlvbound_h547154ec__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[0U] = q_wall_gate__DOT____Vlvbound_h547154ec__0;
    q_wall_gate__DOT____Vlvbound_hbb21dfa5__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [0U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[0U] = q_wall_gate__DOT____Vlvbound_hbb21dfa5__0;
    if (VL_LTS_IQQ(48, 0xe8d4a51000ULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [0U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__guard_hit = 1U;
    }
    if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [0U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__trig = (1U | (IData)(vlSelfRef.q_wall_gate__DOT__trig));
    }
    q_wall_gate__DOT__eff = (VL_GTES_III(15, (IData)(vlSelfRef.q_wall_gate__DOT__t), 
                                         (0x7fffU & 
                                          VL_EXTENDS_II(15,7, 
                                                        vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                        [1U])))
                              ? (0x3fffU & (VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)) 
                                            - VL_EXTENDS_II(32,7, 
                                                            vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                            [1U])))
                              : 0U);
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = (0x3fffU 
                                                  & VL_MODDIV_III(32, (IData)(q_wall_gate__DOT__eff), (IData)(0xf0U)));
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout 
        = (0xffffffffffffULL & ((0x60U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                 ? (0x190ULL + VL_DIV_QQQ(48, 
                                                          (0xffffffffffffULL 
                                                           & VL_SHIFTL_QQI(48,48,32, (QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)), 3U)), 5ULL))
                                 : ((0x90U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                     ? (0x229ULL - 
                                        ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                         - 0x60ULL))
                                     : (0x1f9ULL - 
                                        VL_DIV_QQQ(48, 
                                                   (0xffffffffffffULL 
                                                    & VL_SHIFTL_QQI(48,48,32, 
                                                                    ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                                                     - 0x90ULL), 3U)), 5ULL)))));
    q_wall_gate__DOT____Vlvbound_h547154ec__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[1U] = q_wall_gate__DOT____Vlvbound_h547154ec__0;
    q_wall_gate__DOT____Vlvbound_hbb21dfa5__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [1U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[1U] = q_wall_gate__DOT____Vlvbound_hbb21dfa5__0;
    if (VL_LTS_IQQ(48, 0xe8d4a51000ULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [1U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__guard_hit = 1U;
    }
    if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [1U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__trig = (2U | (IData)(vlSelfRef.q_wall_gate__DOT__trig));
    }
    q_wall_gate__DOT__eff = (VL_GTES_III(15, (IData)(vlSelfRef.q_wall_gate__DOT__t), 
                                         (0x7fffU & 
                                          VL_EXTENDS_II(15,7, 
                                                        vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                        [2U])))
                              ? (0x3fffU & (VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)) 
                                            - VL_EXTENDS_II(32,7, 
                                                            vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                            [2U])))
                              : 0U);
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = (0x3fffU 
                                                  & VL_MODDIV_III(32, (IData)(q_wall_gate__DOT__eff), (IData)(0xf0U)));
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout 
        = (0xffffffffffffULL & ((0x60U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                 ? (0x190ULL + VL_DIV_QQQ(48, 
                                                          (0xffffffffffffULL 
                                                           & VL_SHIFTL_QQI(48,48,32, (QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)), 3U)), 5ULL))
                                 : ((0x90U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                     ? (0x229ULL - 
                                        ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                         - 0x60ULL))
                                     : (0x1f9ULL - 
                                        VL_DIV_QQQ(48, 
                                                   (0xffffffffffffULL 
                                                    & VL_SHIFTL_QQI(48,48,32, 
                                                                    ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                                                     - 0x90ULL), 3U)), 5ULL)))));
    q_wall_gate__DOT____Vlvbound_h547154ec__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[2U] = q_wall_gate__DOT____Vlvbound_h547154ec__0;
    q_wall_gate__DOT____Vlvbound_hbb21dfa5__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [2U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[2U] = q_wall_gate__DOT____Vlvbound_hbb21dfa5__0;
    if (VL_LTS_IQQ(48, 0xe8d4a51000ULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [2U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__guard_hit = 1U;
    }
    if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [2U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__trig = (4U | (IData)(vlSelfRef.q_wall_gate__DOT__trig));
    }
    q_wall_gate__DOT__eff = (VL_GTES_III(15, (IData)(vlSelfRef.q_wall_gate__DOT__t), 
                                         (0x7fffU & 
                                          VL_EXTENDS_II(15,7, 
                                                        vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                        [3U])))
                              ? (0x3fffU & (VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)) 
                                            - VL_EXTENDS_II(32,7, 
                                                            vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                            [3U])))
                              : 0U);
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = (0x3fffU 
                                                  & VL_MODDIV_III(32, (IData)(q_wall_gate__DOT__eff), (IData)(0xf0U)));
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout 
        = (0xffffffffffffULL & ((0x60U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                 ? (0x190ULL + VL_DIV_QQQ(48, 
                                                          (0xffffffffffffULL 
                                                           & VL_SHIFTL_QQI(48,48,32, (QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)), 3U)), 5ULL))
                                 : ((0x90U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                     ? (0x229ULL - 
                                        ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                         - 0x60ULL))
                                     : (0x1f9ULL - 
                                        VL_DIV_QQQ(48, 
                                                   (0xffffffffffffULL 
                                                    & VL_SHIFTL_QQI(48,48,32, 
                                                                    ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                                                     - 0x90ULL), 3U)), 5ULL)))));
    q_wall_gate__DOT____Vlvbound_h547154ec__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[3U] = q_wall_gate__DOT____Vlvbound_h547154ec__0;
    q_wall_gate__DOT____Vlvbound_hbb21dfa5__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [3U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[3U] = q_wall_gate__DOT____Vlvbound_hbb21dfa5__0;
    if (VL_LTS_IQQ(48, 0xe8d4a51000ULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [3U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__guard_hit = 1U;
    }
    if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [3U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__trig = (8U | (IData)(vlSelfRef.q_wall_gate__DOT__trig));
    }
    q_wall_gate__DOT__eff = (VL_GTES_III(15, (IData)(vlSelfRef.q_wall_gate__DOT__t), 
                                         (0x7fffU & 
                                          VL_EXTENDS_II(15,7, 
                                                        vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                        [4U])))
                              ? (0x3fffU & (VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)) 
                                            - VL_EXTENDS_II(32,7, 
                                                            vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                            [4U])))
                              : 0U);
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = (0x3fffU 
                                                  & VL_MODDIV_III(32, (IData)(q_wall_gate__DOT__eff), (IData)(0xf0U)));
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout 
        = (0xffffffffffffULL & ((0x60U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                 ? (0x190ULL + VL_DIV_QQQ(48, 
                                                          (0xffffffffffffULL 
                                                           & VL_SHIFTL_QQI(48,48,32, (QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)), 3U)), 5ULL))
                                 : ((0x90U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                     ? (0x229ULL - 
                                        ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                         - 0x60ULL))
                                     : (0x1f9ULL - 
                                        VL_DIV_QQQ(48, 
                                                   (0xffffffffffffULL 
                                                    & VL_SHIFTL_QQI(48,48,32, 
                                                                    ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                                                     - 0x90ULL), 3U)), 5ULL)))));
    q_wall_gate__DOT____Vlvbound_h547154ec__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[4U] = q_wall_gate__DOT____Vlvbound_h547154ec__0;
    q_wall_gate__DOT____Vlvbound_hbb21dfa5__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [4U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[4U] = q_wall_gate__DOT____Vlvbound_hbb21dfa5__0;
    if (VL_LTS_IQQ(48, 0xe8d4a51000ULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [4U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__guard_hit = 1U;
    }
    if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [4U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__trig = (0x10U | (IData)(vlSelfRef.q_wall_gate__DOT__trig));
    }
    q_wall_gate__DOT__eff = (VL_GTES_III(15, (IData)(vlSelfRef.q_wall_gate__DOT__t), 
                                         (0x7fffU & 
                                          VL_EXTENDS_II(15,7, 
                                                        vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                        [5U])))
                              ? (0x3fffU & (VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)) 
                                            - VL_EXTENDS_II(32,7, 
                                                            vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                            [5U])))
                              : 0U);
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = (0x3fffU 
                                                  & VL_MODDIV_III(32, (IData)(q_wall_gate__DOT__eff), (IData)(0xf0U)));
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout 
        = (0xffffffffffffULL & ((0x60U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                 ? (0x190ULL + VL_DIV_QQQ(48, 
                                                          (0xffffffffffffULL 
                                                           & VL_SHIFTL_QQI(48,48,32, (QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)), 3U)), 5ULL))
                                 : ((0x90U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                     ? (0x229ULL - 
                                        ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                         - 0x60ULL))
                                     : (0x1f9ULL - 
                                        VL_DIV_QQQ(48, 
                                                   (0xffffffffffffULL 
                                                    & VL_SHIFTL_QQI(48,48,32, 
                                                                    ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                                                     - 0x90ULL), 3U)), 5ULL)))));
    q_wall_gate__DOT____Vlvbound_h547154ec__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[5U] = q_wall_gate__DOT____Vlvbound_h547154ec__0;
    q_wall_gate__DOT____Vlvbound_hbb21dfa5__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [5U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[5U] = q_wall_gate__DOT____Vlvbound_hbb21dfa5__0;
    if (VL_LTS_IQQ(48, 0xe8d4a51000ULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [5U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__guard_hit = 1U;
    }
    if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [5U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__trig = (0x20U | (IData)(vlSelfRef.q_wall_gate__DOT__trig));
    }
    q_wall_gate__DOT__eff = (VL_GTES_III(15, (IData)(vlSelfRef.q_wall_gate__DOT__t), 
                                         (0x7fffU & 
                                          VL_EXTENDS_II(15,7, 
                                                        vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                        [6U])))
                              ? (0x3fffU & (VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)) 
                                            - VL_EXTENDS_II(32,7, 
                                                            vlSelfRef.q_wall_gate__DOT__i_lats_reg
                                                            [6U])))
                              : 0U);
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = (0x3fffU 
                                                  & VL_MODDIV_III(32, (IData)(q_wall_gate__DOT__eff), (IData)(0xf0U)));
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout 
        = (0xffffffffffffULL & ((0x60U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                 ? (0x190ULL + VL_DIV_QQQ(48, 
                                                          (0xffffffffffffULL 
                                                           & VL_SHIFTL_QQI(48,48,32, (QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)), 3U)), 5ULL))
                                 : ((0x90U > (IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph))
                                     ? (0x229ULL - 
                                        ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                         - 0x60ULL))
                                     : (0x1f9ULL - 
                                        VL_DIV_QQQ(48, 
                                                   (0xffffffffffffULL 
                                                    & VL_SHIFTL_QQI(48,48,32, 
                                                                    ((QData)((IData)(__Vfunc_q_wall_gate__DOT__f_reality__1__ph)) 
                                                                     - 0x90ULL), 3U)), 5ULL)))));
    q_wall_gate__DOT____Vlvbound_h547154ec__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[6U] = q_wall_gate__DOT____Vlvbound_h547154ec__0;
    q_wall_gate__DOT____Vlvbound_hbb21dfa5__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [6U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[6U] = q_wall_gate__DOT____Vlvbound_hbb21dfa5__0;
    if (VL_LTS_IQQ(48, 0xe8d4a51000ULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [6U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__guard_hit = 1U;
    }
    if (VL_LTS_IQQ(48, 0xcULL, ([&]() {
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v 
                        = vlSelfRef.q_wall_gate__DOT__errs
                        [6U];
                    vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout 
                        = (0xffffffffffffULL & (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 ? 
                                                (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v)
                                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__v));
                }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout))) {
        vlSelfRef.q_wall_gate__DOT__trig = (0x40U | (IData)(vlSelfRef.q_wall_gate__DOT__trig));
    }
    if ((1U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__nf = (0xfU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.q_wall_gate__DOT__nf)));
    }
    if ((2U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__nf = (0xfU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.q_wall_gate__DOT__nf)));
    }
    if ((4U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__nf = (0xfU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.q_wall_gate__DOT__nf)));
    }
    if ((8U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__nf = (0xfU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.q_wall_gate__DOT__nf)));
    }
    if ((0x10U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__nf = (0xfU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.q_wall_gate__DOT__nf)));
    }
    if ((0x20U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__nf = (0xfU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.q_wall_gate__DOT__nf)));
    }
    if ((0x40U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__nf = (0xfU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.q_wall_gate__DOT__nf)));
    }
    vlSelfRef.q_wall_gate__DOT__open_ = ((0U != (IData)(vlSelfRef.q_wall_gate__DOT__nf)) 
                                         & (0x14aU 
                                            < ((3U 
                                                > (IData)(vlSelfRef.q_wall_gate__DOT__nf))
                                                ? ((IData)(0x64U) 
                                                   * 
                                                   ((IData)(3U) 
                                                    - (IData)(vlSelfRef.q_wall_gate__DOT__nf)))
                                                : ((IData)(0x64U) 
                                                   * 
                                                   ((IData)(vlSelfRef.q_wall_gate__DOT__nf) 
                                                    - (IData)(3U))))));
    vlSelfRef.q_wall_gate__DOT__neff = (0xfU & ((IData)(vlSelfRef.q_wall_gate__DOT__open_)
                                                 ? 
                                                ((3U 
                                                  < (IData)(vlSelfRef.q_wall_gate__DOT__nf))
                                                  ? 3U
                                                  : (IData)(vlSelfRef.q_wall_gate__DOT__nf))
                                                 : 
                                                ((0U 
                                                  != (IData)(vlSelfRef.q_wall_gate__DOT__nf))
                                                  ? 1U
                                                  : 0U)));
    vlSelfRef.q_wall_gate__DOT__pm_new[0U] = 0ULL;
    if ((1U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                            & VL_DIVS_QQQ(48, 
                                                          ([&]() {
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v 
                            = vlSelfRef.q_wall_gate__DOT__errs
                            [0U];
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout 
                            = (0xffffffffffffULL & 
                               (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 ? (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v));
                    }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout), 3ULL));
        if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
            vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
        }
        if ((1U < (IData)(vlSelfRef.q_wall_gate__DOT__neff))) {
            vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                                & VL_DIV_QQQ(48, vlSelfRef.q_wall_gate__DOT__mtmp, (QData)((IData)(vlSelfRef.q_wall_gate__DOT__neff))));
            if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
                vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
            }
        }
        vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [0U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[0U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1;
    }
    vlSelfRef.q_wall_gate__DOT__pm_new[1U] = 0ULL;
    if ((2U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                            & VL_DIVS_QQQ(48, 
                                                          ([&]() {
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v 
                            = vlSelfRef.q_wall_gate__DOT__errs
                            [1U];
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout 
                            = (0xffffffffffffULL & 
                               (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 ? (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v));
                    }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout), 3ULL));
        if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
            vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
        }
        if ((1U < (IData)(vlSelfRef.q_wall_gate__DOT__neff))) {
            vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                                & VL_DIV_QQQ(48, vlSelfRef.q_wall_gate__DOT__mtmp, (QData)((IData)(vlSelfRef.q_wall_gate__DOT__neff))));
            if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
                vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
            }
        }
        vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [1U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[1U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1;
    }
    vlSelfRef.q_wall_gate__DOT__pm_new[2U] = 0ULL;
    if ((4U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                            & VL_DIVS_QQQ(48, 
                                                          ([&]() {
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v 
                            = vlSelfRef.q_wall_gate__DOT__errs
                            [2U];
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout 
                            = (0xffffffffffffULL & 
                               (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 ? (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v));
                    }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout), 3ULL));
        if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
            vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
        }
        if ((1U < (IData)(vlSelfRef.q_wall_gate__DOT__neff))) {
            vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                                & VL_DIV_QQQ(48, vlSelfRef.q_wall_gate__DOT__mtmp, (QData)((IData)(vlSelfRef.q_wall_gate__DOT__neff))));
            if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
                vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
            }
        }
        vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [2U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[2U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1;
    }
    vlSelfRef.q_wall_gate__DOT__pm_new[3U] = 0ULL;
    if ((8U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                            & VL_DIVS_QQQ(48, 
                                                          ([&]() {
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v 
                            = vlSelfRef.q_wall_gate__DOT__errs
                            [3U];
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout 
                            = (0xffffffffffffULL & 
                               (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 ? (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v));
                    }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout), 3ULL));
        if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
            vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
        }
        if ((1U < (IData)(vlSelfRef.q_wall_gate__DOT__neff))) {
            vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                                & VL_DIV_QQQ(48, vlSelfRef.q_wall_gate__DOT__mtmp, (QData)((IData)(vlSelfRef.q_wall_gate__DOT__neff))));
            if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
                vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
            }
        }
        vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [3U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[3U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1;
    }
    vlSelfRef.q_wall_gate__DOT__pm_new[4U] = 0ULL;
    if ((0x10U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                            & VL_DIVS_QQQ(48, 
                                                          ([&]() {
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v 
                            = vlSelfRef.q_wall_gate__DOT__errs
                            [4U];
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout 
                            = (0xffffffffffffULL & 
                               (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 ? (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v));
                    }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout), 3ULL));
        if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
            vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
        }
        if ((1U < (IData)(vlSelfRef.q_wall_gate__DOT__neff))) {
            vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                                & VL_DIV_QQQ(48, vlSelfRef.q_wall_gate__DOT__mtmp, (QData)((IData)(vlSelfRef.q_wall_gate__DOT__neff))));
            if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
                vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
            }
        }
        vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [4U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[4U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1;
    }
    vlSelfRef.q_wall_gate__DOT__pm_new[5U] = 0ULL;
    if ((0x20U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                            & VL_DIVS_QQQ(48, 
                                                          ([&]() {
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v 
                            = vlSelfRef.q_wall_gate__DOT__errs
                            [5U];
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout 
                            = (0xffffffffffffULL & 
                               (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 ? (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v));
                    }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout), 3ULL));
        if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
            vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
        }
        if ((1U < (IData)(vlSelfRef.q_wall_gate__DOT__neff))) {
            vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                                & VL_DIV_QQQ(48, vlSelfRef.q_wall_gate__DOT__mtmp, (QData)((IData)(vlSelfRef.q_wall_gate__DOT__neff))));
            if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
                vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
            }
        }
        vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [5U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[5U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1;
    }
    vlSelfRef.q_wall_gate__DOT__pm_new[6U] = 0ULL;
    if ((0x40U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
        vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                            & VL_DIVS_QQQ(48, 
                                                          ([&]() {
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v 
                            = vlSelfRef.q_wall_gate__DOT__errs
                            [6U];
                        vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout 
                            = (0xffffffffffffULL & 
                               (VL_GTS_IQQ(48, 0ULL, vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 ? (- vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v)
                                 : vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__v));
                    }(), vlSelfRef.__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout), 3ULL));
        if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
            vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
        }
        if ((1U < (IData)(vlSelfRef.q_wall_gate__DOT__neff))) {
            vlSelfRef.q_wall_gate__DOT__mtmp = (0xffffffffffffULL 
                                                & VL_DIV_QQQ(48, vlSelfRef.q_wall_gate__DOT__mtmp, (QData)((IData)(vlSelfRef.q_wall_gate__DOT__neff))));
            if ((0ULL == vlSelfRef.q_wall_gate__DOT__mtmp)) {
                vlSelfRef.q_wall_gate__DOT__mtmp = 1ULL;
            }
        }
        vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [6U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[6U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_h5108c7b6__1;
    }
    if ((0U == VL_MODDIVS_III(32, VL_EXTENDS_II(32,15, (IData)(vlSelfRef.q_wall_gate__DOT__t)), (IData)(1U)))) {
        if ((1U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [0U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [0U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [0U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((2U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [1U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [1U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [1U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((4U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [2U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [2U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [2U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((8U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [3U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [3U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [3U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((0x10U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [4U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [4U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [4U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((0x20U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [5U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [5U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [5U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((0x40U & (IData)(vlSelfRef.q_wall_gate__DOT__trig))) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__pm_new
                                                  [6U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [6U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__pm_new
                           [6U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
    } else {
        if ((0U < vlSelfRef.q_wall_gate__DOT__cnt[0U])) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [0U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][0U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][0U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((1U < vlSelfRef.q_wall_gate__DOT__cnt[0U])) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [1U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][1U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][1U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((2U < vlSelfRef.q_wall_gate__DOT__cnt[0U])) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [2U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][2U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][2U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((3U < vlSelfRef.q_wall_gate__DOT__cnt[0U])) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [3U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][3U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][3U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((4U < vlSelfRef.q_wall_gate__DOT__cnt[0U])) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [4U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][4U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][4U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((5U < vlSelfRef.q_wall_gate__DOT__cnt[0U])) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [5U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][5U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][5U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
        if ((6U < vlSelfRef.q_wall_gate__DOT__cnt[0U])) {
            vlSelfRef.q_wall_gate__DOT__net = (0xffffffffffffULL 
                                               & (vlSelfRef.q_wall_gate__DOT__net 
                                                  + 
                                                  vlSelfRef.q_wall_gate__DOT__mags
                                                  [0U]
                                                  [6U]));
            if (VL_LTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][6U])) {
                q_wall_gate__DOT__any_pos = 1U;
            }
            if (VL_GTS_IQQ(48, 0ULL, vlSelfRef.q_wall_gate__DOT__mags
                           [0U][6U])) {
                q_wall_gate__DOT__any_neg = 1U;
            }
        }
    }
    vlSelfRef.q_wall_gate__DOT__cancel = (((0ULL == vlSelfRef.q_wall_gate__DOT__net) 
                                           & (IData)(q_wall_gate__DOT__any_pos)) 
                                          & (IData)(q_wall_gate__DOT__any_neg));
}

void Vq_wall_gate___024root___eval_triggers__act(Vq_wall_gate___024root* vlSelf);

bool Vq_wall_gate___024root___eval_phase__act(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_phase__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlTriggerVec<2> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vq_wall_gate___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelfRef.__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelfRef.__VactTriggered, vlSelfRef.__VnbaTriggered);
        vlSelfRef.__VnbaTriggered.thisOr(vlSelfRef.__VactTriggered);
        Vq_wall_gate___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vq_wall_gate___024root___eval_phase__nba(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_phase__nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelfRef.__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vq_wall_gate___024root___eval_nba(vlSelf);
        vlSelfRef.__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_wall_gate___024root___dump_triggers__nba(Vq_wall_gate___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_wall_gate___024root___dump_triggers__act(Vq_wall_gate___024root* vlSelf);
#endif  // VL_DEBUG

void Vq_wall_gate___024root___eval(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            Vq_wall_gate___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("rtl/q_wall_gate.v", 38, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelfRef.__VactIterCount = 0U;
        vlSelfRef.__VactContinue = 1U;
        while (vlSelfRef.__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelfRef.__VactIterCount))) {
#ifdef VL_DEBUG
                Vq_wall_gate___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("rtl/q_wall_gate.v", 38, "", "Active region did not converge.");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactContinue = 0U;
            if (Vq_wall_gate___024root___eval_phase__act(vlSelf)) {
                vlSelfRef.__VactContinue = 1U;
            }
        }
        if (Vq_wall_gate___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vq_wall_gate___024root___eval_debug_assertions(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_debug_assertions\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY((vlSelfRef.clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((vlSelfRef.rst_n & 0xfeU))) {
        Verilated::overWidthError("rst_n");}
    if (VL_UNLIKELY((vlSelfRef.i_go & 0xfeU))) {
        Verilated::overWidthError("i_go");}
    if (VL_UNLIKELY((vlSelfRef.i_lats & 0ULL))) {
        Verilated::overWidthError("i_lats");}
}
#endif  // VL_DEBUG
