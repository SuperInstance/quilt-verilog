// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vq_fabric_top.h for the primary calling header

#include "Vq_fabric_top__pch.h"
#include "Vq_fabric_top___024root.h"

void Vq_fabric_top___024root___eval_triggers__ico(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___eval_ico(Vq_fabric_top___024root* vlSelf);

bool Vq_fabric_top___024root___eval_phase__ico(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_phase__ico\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    Vq_fabric_top___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelfRef.__VicoTriggered.any();
    if (__VicoExecute) {
        Vq_fabric_top___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void Vq_fabric_top___024root___eval_act(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_act\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
}

void Vq_fabric_top___024root___eval_triggers__act(Vq_fabric_top___024root* vlSelf);

bool Vq_fabric_top___024root___eval_phase__act(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_phase__act\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlTriggerVec<16> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vq_fabric_top___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelfRef.__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelfRef.__VactTriggered, vlSelfRef.__VnbaTriggered);
        vlSelfRef.__VnbaTriggered.thisOr(vlSelfRef.__VactTriggered);
        Vq_fabric_top___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

void Vq_fabric_top___024root___eval_nba(Vq_fabric_top___024root* vlSelf);

bool Vq_fabric_top___024root___eval_phase__nba(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_phase__nba\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelfRef.__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vq_fabric_top___024root___eval_nba(vlSelf);
        vlSelfRef.__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__ico(Vq_fabric_top___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__nba(Vq_fabric_top___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vq_fabric_top___024root___dump_triggers__act(Vq_fabric_top___024root* vlSelf);
#endif  // VL_DEBUG

void Vq_fabric_top___024root___eval(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VicoIterCount;
    CData/*0:0*/ __VicoContinue;
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    __VicoContinue = 1U;
    while (__VicoContinue) {
        if (VL_UNLIKELY((0x64U < __VicoIterCount))) {
#ifdef VL_DEBUG
            Vq_fabric_top___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("rtl/q_fabric_top.v", 4, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (Vq_fabric_top___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelfRef.__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY((0x64U < __VnbaIterCount))) {
#ifdef VL_DEBUG
            Vq_fabric_top___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("rtl/q_fabric_top.v", 4, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelfRef.__VactIterCount = 0U;
        vlSelfRef.__VactContinue = 1U;
        while (vlSelfRef.__VactContinue) {
            if (VL_UNLIKELY((0x64U < vlSelfRef.__VactIterCount))) {
#ifdef VL_DEBUG
                Vq_fabric_top___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("rtl/q_fabric_top.v", 4, "", "Active region did not converge.");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactContinue = 0U;
            if (Vq_fabric_top___024root___eval_phase__act(vlSelf)) {
                vlSelfRef.__VactContinue = 1U;
            }
        }
        if (Vq_fabric_top___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vq_fabric_top___024root___eval_debug_assertions(Vq_fabric_top___024root* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vq_fabric_top___024root___eval_debug_assertions\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY((vlSelfRef.clk & 0xfeU))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY((vlSelfRef.rst_n & 0xfeU))) {
        Verilated::overWidthError("rst_n");}
    if (VL_UNLIKELY((vlSelfRef.i_val & 0xfeU))) {
        Verilated::overWidthError("i_val");}
    if (VL_UNLIKELY((vlSelfRef.i_op & 0xf8U))) {
        Verilated::overWidthError("i_op");}
    if (VL_UNLIKELY((vlSelfRef.i_src & 0xf0U))) {
        Verilated::overWidthError("i_src");}
    if (VL_UNLIKELY((vlSelfRef.i_dst & 0xf0U))) {
        Verilated::overWidthError("i_dst");}
    if (VL_UNLIKELY((vlSelfRef.i_rdy & 0xfeU))) {
        Verilated::overWidthError("i_rdy");}
}
#endif  // VL_DEBUG
