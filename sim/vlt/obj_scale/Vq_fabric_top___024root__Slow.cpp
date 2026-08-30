// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vq_fabric_top.h for the primary calling header

#include "Vq_fabric_top__pch.h"
#include "Vq_fabric_top__Syms.h"
#include "Vq_fabric_top___024root.h"

// Parameter definitions for Vq_fabric_top___024root
constexpr CData/*3:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__EXTID;
constexpr CData/*3:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__EXTID;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__NCELL;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__EDGES_N;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__TPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__NB;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__u_ts__DOT__TPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__0__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__1__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__2__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__3__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__4__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__5__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__6__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__7__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__8__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__9__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__10__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__11__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__12__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__13__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__14__KET____DOT__u_pipe__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__connio__DOT__u_io__DOT__u_rp__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top___024root::q_fabric_top__DOT__nodes__BRA__15__KET____DOT__u_pipe__DOT__FW;


void Vq_fabric_top___024root___ctor_var_reset(Vq_fabric_top___024root* vlSelf);

Vq_fabric_top___024root::Vq_fabric_top___024root(Vq_fabric_top__Syms* symsp, const char* v__name)
    : VerilatedModule{v__name}
    , vlSymsp{symsp}
 {
    // Reset structure values
    Vq_fabric_top___024root___ctor_var_reset(this);
}

void Vq_fabric_top___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vq_fabric_top___024root::~Vq_fabric_top___024root() {
}
