// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vq_wall_gate.h for the primary calling header

#include "Vq_wall_gate__pch.h"
#include "Vq_wall_gate___024root.h"

VL_ATTR_COLD void Vq_wall_gate___024root___eval_static(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_static\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vq_wall_gate___024root___eval_initial(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_initial\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
}

VL_ATTR_COLD void Vq_wall_gate___024root___eval_final(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_final\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_wall_gate___024root___dump_triggers__stl(Vq_wall_gate___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vq_wall_gate___024root___eval_phase__stl(Vq_wall_gate___024root* vlSelf);

VL_ATTR_COLD void Vq_wall_gate___024root___eval_settle(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_settle\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
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
            Vq_wall_gate___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("rtl/q_wall_gate.v", 38, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vq_wall_gate___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_wall_gate___024root___dump_triggers__stl(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___dump_triggers__stl\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VstlTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vq_wall_gate___024root___stl_sequent__TOP__0(Vq_wall_gate___024root* vlSelf);

VL_ATTR_COLD void Vq_wall_gate___024root___eval_stl(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_stl\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        Vq_wall_gate___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void Vq_wall_gate___024root___stl_sequent__TOP__0(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___stl_sequent__TOP__0\n"); );
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
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_h7e09794f__0;
    q_wall_gate__DOT____Vlvbound_h7e09794f__0 = 0;
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_hd63c7c30__0;
    q_wall_gate__DOT____Vlvbound_hd63c7c30__0 = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_reality__0__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_reality__0__Vfuncout = 0;
    SData/*13:0*/ __Vfunc_q_wall_gate__DOT__f_reality__0__ph;
    __Vfunc_q_wall_gate__DOT__f_reality__0__ph = 0;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout = 0;
    SData/*13:0*/ __Vfunc_q_wall_gate__DOT__f_reality__1__ph;
    __Vfunc_q_wall_gate__DOT__f_reality__1__ph = 0;
    // Body
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
    vlSelfRef.q_wall_gate__DOT__open_ = 0U;
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
    q_wall_gate__DOT____Vlvbound_h7e09794f__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[0U] = q_wall_gate__DOT____Vlvbound_h7e09794f__0;
    q_wall_gate__DOT____Vlvbound_hd63c7c30__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [0U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[0U] = q_wall_gate__DOT____Vlvbound_hd63c7c30__0;
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
    q_wall_gate__DOT____Vlvbound_h7e09794f__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[1U] = q_wall_gate__DOT____Vlvbound_h7e09794f__0;
    q_wall_gate__DOT____Vlvbound_hd63c7c30__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [1U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[1U] = q_wall_gate__DOT____Vlvbound_hd63c7c30__0;
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
    q_wall_gate__DOT____Vlvbound_h7e09794f__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[2U] = q_wall_gate__DOT____Vlvbound_h7e09794f__0;
    q_wall_gate__DOT____Vlvbound_hd63c7c30__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [2U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[2U] = q_wall_gate__DOT____Vlvbound_hd63c7c30__0;
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
    q_wall_gate__DOT____Vlvbound_h7e09794f__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[3U] = q_wall_gate__DOT____Vlvbound_h7e09794f__0;
    q_wall_gate__DOT____Vlvbound_hd63c7c30__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [3U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[3U] = q_wall_gate__DOT____Vlvbound_hd63c7c30__0;
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
    q_wall_gate__DOT____Vlvbound_h7e09794f__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[4U] = q_wall_gate__DOT____Vlvbound_h7e09794f__0;
    q_wall_gate__DOT____Vlvbound_hd63c7c30__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [4U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[4U] = q_wall_gate__DOT____Vlvbound_hd63c7c30__0;
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
    q_wall_gate__DOT____Vlvbound_h7e09794f__0 = __Vfunc_q_wall_gate__DOT__f_reality__1__Vfuncout;
    vlSelfRef.q_wall_gate__DOT__reads[5U] = q_wall_gate__DOT____Vlvbound_h7e09794f__0;
    q_wall_gate__DOT____Vlvbound_hd63c7c30__0 = (0xffffffffffffULL 
                                                 & (vlSelfRef.q_wall_gate__DOT__reads
                                                    [5U] 
                                                    - vlSelfRef.q_wall_gate__DOT__g_now));
    vlSelfRef.q_wall_gate__DOT__errs[5U] = q_wall_gate__DOT____Vlvbound_hd63c7c30__0;
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
    vlSelfRef.q_wall_gate__DOT__neff = ((3U < (IData)(vlSelfRef.q_wall_gate__DOT__nf))
                                         ? 3U : (0xfU 
                                                 & (IData)(vlSelfRef.q_wall_gate__DOT__nf)));
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
        vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [0U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[0U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1;
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
        vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [1U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[1U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1;
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
        vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [2U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[2U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1;
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
        vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [3U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[3U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1;
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
        vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [4U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[4U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1;
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
        vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1 
            = (0xffffffffffffULL & (VL_LTS_IQQ(48, 0ULL, 
                                               vlSelfRef.q_wall_gate__DOT__errs
                                               [5U])
                                     ? vlSelfRef.q_wall_gate__DOT__mtmp
                                     : (- vlSelfRef.q_wall_gate__DOT__mtmp)));
        vlSelfRef.q_wall_gate__DOT__pm_new[5U] = vlSelfRef.q_wall_gate__DOT____Vlvbound_hc3744b18__1;
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
    }
    vlSelfRef.q_wall_gate__DOT__cancel = (((0ULL == vlSelfRef.q_wall_gate__DOT__net) 
                                           & (IData)(q_wall_gate__DOT__any_pos)) 
                                          & (IData)(q_wall_gate__DOT__any_neg));
}

VL_ATTR_COLD void Vq_wall_gate___024root___eval_triggers__stl(Vq_wall_gate___024root* vlSelf);

VL_ATTR_COLD bool Vq_wall_gate___024root___eval_phase__stl(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___eval_phase__stl\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vq_wall_gate___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        Vq_wall_gate___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_wall_gate___024root___dump_triggers__act(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___dump_triggers__act\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((2ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(negedge rst_n)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_wall_gate___024root___dump_triggers__nba(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___dump_triggers__nba\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(negedge rst_n)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vq_wall_gate___024root___ctor_var_reset(Vq_wall_gate___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_wall_gate__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_wall_gate___024root___ctor_var_reset\n"); );
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->clk = VL_RAND_RESET_I(1);
    vlSelf->rst_n = VL_RAND_RESET_I(1);
    vlSelf->i_go = VL_RAND_RESET_I(1);
    vlSelf->i_seed = VL_RAND_RESET_I(32);
    vlSelf->i_lats = VL_RAND_RESET_Q(36);
    vlSelf->o_running = VL_RAND_RESET_I(1);
    vlSelf->o_bail = VL_RAND_RESET_I(1);
    vlSelf->o_t = VL_RAND_RESET_I(14);
    vlSelf->o_resid = VL_RAND_RESET_Q(48);
    vlSelf->o_tval = VL_RAND_RESET_I(1);
    vlSelf->o_cflag = VL_RAND_RESET_I(1);
    vlSelf->o_nf = VL_RAND_RESET_I(4);
    vlSelf->o_gopen = VL_RAND_RESET_I(1);
    vlSelf->o_em_mask = VL_RAND_RESET_I(6);
    VL_RAND_RESET_W(288, vlSelf->o_em_pm);
    VL_RAND_RESET_W(288, vlSelf->o_em_e);
    vlSelf->o_events = VL_RAND_RESET_Q(48);
    vlSelf->o_mass = VL_RAND_RESET_Q(48);
    vlSelf->o_cancels = VL_RAND_RESET_Q(48);
    vlSelf->o_chatter = VL_RAND_RESET_Q(48);
    vlSelf->o_settles = VL_RAND_RESET_Q(48);
    vlSelf->o_gopen_tot = VL_RAND_RESET_Q(48);
    vlSelf->o_gcomp = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT__lcg_x = VL_RAND_RESET_I(32);
    vlSelf->q_wall_gate__DOT__g = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT__t = VL_RAND_RESET_I(15);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 6; ++__Vi1) {
            vlSelf->q_wall_gate__DOT__mags[__Vi0][__Vi1] = VL_RAND_RESET_Q(48);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->q_wall_gate__DOT__cnt[__Vi0] = VL_RAND_RESET_I(4);
    }
    vlSelf->q_wall_gate__DOT__last = VL_RAND_RESET_I(15);
    vlSelf->q_wall_gate__DOT__st = VL_RAND_RESET_I(2);
    for (int __Vi0 = 0; __Vi0 < 6; ++__Vi0) {
        vlSelf->q_wall_gate__DOT__i_lats_reg[__Vi0] = VL_RAND_RESET_I(6);
    }
    for (int __Vi0 = 0; __Vi0 < 6; ++__Vi0) {
        vlSelf->q_wall_gate__DOT__reads[__Vi0] = VL_RAND_RESET_Q(48);
    }
    for (int __Vi0 = 0; __Vi0 < 6; ++__Vi0) {
        vlSelf->q_wall_gate__DOT__errs[__Vi0] = VL_RAND_RESET_Q(48);
    }
    vlSelf->q_wall_gate__DOT__trig = VL_RAND_RESET_I(6);
    vlSelf->q_wall_gate__DOT__nf = VL_RAND_RESET_I(4);
    for (int __Vi0 = 0; __Vi0 < 6; ++__Vi0) {
        vlSelf->q_wall_gate__DOT__pm_new[__Vi0] = VL_RAND_RESET_Q(48);
    }
    vlSelf->q_wall_gate__DOT__neff = VL_RAND_RESET_I(4);
    vlSelf->q_wall_gate__DOT__open_ = VL_RAND_RESET_I(1);
    vlSelf->q_wall_gate__DOT__net = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT__g_now = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT__s_true = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT__cancel = VL_RAND_RESET_I(1);
    vlSelf->q_wall_gate__DOT__guard_hit = VL_RAND_RESET_I(1);
    vlSelf->q_wall_gate__DOT__mtmp = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT__sall = VL_RAND_RESET_I(1);
    vlSelf->q_wall_gate__DOT__lcg_next = VL_RAND_RESET_I(32);
    vlSelf->q_wall_gate__DOT__dv = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT____Vlvbound_hc3744b18__1 = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT____Vlvbound_h527fd750__0 = VL_RAND_RESET_I(6);
    vlSelf->q_wall_gate__DOT____Vlvbound_hb3a0a8ac__0 = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT____Vlvbound_h546c86fe__0 = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT____Vlvbound_h9637dd8d__0 = VL_RAND_RESET_I(4);
    vlSelf->q_wall_gate__DOT____Vlvbound_he80f3aea__0 = VL_RAND_RESET_Q(48);
    vlSelf->q_wall_gate__DOT____Vlvbound_h686cd9a7__1 = VL_RAND_RESET_Q(48);
    vlSelf->__Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout = VL_RAND_RESET_Q(48);
    vlSelf->__Vfunc_q_wall_gate__DOT__f_abs__2__v = VL_RAND_RESET_Q(48);
    vlSelf->__Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout = VL_RAND_RESET_Q(48);
    vlSelf->__Vfunc_q_wall_gate__DOT__f_abs__3__v = VL_RAND_RESET_Q(48);
    vlSelf->__Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout = VL_RAND_RESET_Q(48);
    vlSelf->__Vfunc_q_wall_gate__DOT__f_abs__4__v = VL_RAND_RESET_Q(48);
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__rst_n__0 = VL_RAND_RESET_I(1);
}
