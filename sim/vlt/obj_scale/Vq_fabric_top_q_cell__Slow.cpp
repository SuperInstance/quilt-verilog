// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vq_fabric_top.h for the primary calling header

#include "Vq_fabric_top__pch.h"
#include "Vq_fabric_top__Syms.h"
#include "Vq_fabric_top_q_cell.h"

// Parameter definitions for Vq_fabric_top_q_cell
constexpr CData/*2:0*/ Vq_fabric_top_q_cell::u_core__DOT__OP_BIND;
constexpr CData/*2:0*/ Vq_fabric_top_q_cell::u_core__DOT__OP_LINK;
constexpr CData/*2:0*/ Vq_fabric_top_q_cell::u_core__DOT__OP_EFF;
constexpr CData/*2:0*/ Vq_fabric_top_q_cell::u_core__DOT__OP_VIEW;
constexpr CData/*2:0*/ Vq_fabric_top_q_cell::u_core__DOT__OP_TICK;
constexpr CData/*2:0*/ Vq_fabric_top_q_cell::u_core__DOT__OP_ACK;
constexpr CData/*2:0*/ Vq_fabric_top_q_cell::u_core__DOT__OP_NAK;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_RST;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_UNB;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_IDLE;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_BIND;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_LINK;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_LNKW;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_EFF;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_EFFT;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_EFFR;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_VIEW;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_VACC;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_VACW;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_VRD;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_RESP;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_TICK;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_TSW;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_TSWW;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_TLEAK;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_FIRE;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_EFFI;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_EFFP;
constexpr CData/*4:0*/ Vq_fabric_top_q_cell::u_core__DOT__ST_EFFM;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_core__DOT__u_eg__DOT__TOPJ;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_core__DOT__u_rq__DOT__K4;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_ETA_F;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_ETA_S;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_KF;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_KS;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_KA;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_THRESH;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_REFR;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_COSMIN;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_P0E;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_MODE;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_HL;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_KLE;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_FLOOR;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_FTRACE;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_RQ;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::u_df__DOT__D_RQL;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::edges__BRA__0__KET____DOT__u_hebb__DOT__K4;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::edges__BRA__1__KET____DOT__u_hebb__DOT__K4;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::edges__BRA__2__KET____DOT__u_hebb__DOT__K4;
constexpr CData/*3:0*/ Vq_fabric_top_q_cell::edges__BRA__3__KET____DOT__u_hebb__DOT__K4;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::OPW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::AIDW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::EDGES_N;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::EIW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::K;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::B;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::AGEW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__EDGES_N;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__EIW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__K;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__PIPE_EFF;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__u_eg__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__u_rq__DOT__RW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__u_rq__DOT__K;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__u_rq__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__u_rq__DOT__EDGES_N;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_core__DOT__u_rq__DOT__EIW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_df__DOT__DW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_df__DOT__ND;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_df__DOT__AW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_inbuf__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_inbuf__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_inbuf__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_inbuf__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_egbuf__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_egbuf__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_egbuf__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_egbuf__DOT__FW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_rp__DOT__OPW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_rp__DOT__AIDW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::u_rp__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__0__KET____DOT__u_hebb__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__0__KET____DOT__u_hebb__DOT__K;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__0__KET____DOT__u_hebb__DOT__B;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__0__KET____DOT__u_hebb__DOT__AGEW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__0__KET____DOT__u_hebb__DOT__AW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__0__KET____DOT__u_hebb__DOT__IIW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__1__KET____DOT__u_hebb__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__1__KET____DOT__u_hebb__DOT__K;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__1__KET____DOT__u_hebb__DOT__B;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__1__KET____DOT__u_hebb__DOT__AGEW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__1__KET____DOT__u_hebb__DOT__AW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__1__KET____DOT__u_hebb__DOT__IIW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__2__KET____DOT__u_hebb__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__2__KET____DOT__u_hebb__DOT__K;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__2__KET____DOT__u_hebb__DOT__B;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__2__KET____DOT__u_hebb__DOT__AGEW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__2__KET____DOT__u_hebb__DOT__AW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__2__KET____DOT__u_hebb__DOT__IIW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__3__KET____DOT__u_hebb__DOT__PW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__3__KET____DOT__u_hebb__DOT__K;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__3__KET____DOT__u_hebb__DOT__B;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__3__KET____DOT__u_hebb__DOT__AGEW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__3__KET____DOT__u_hebb__DOT__AW;
constexpr IData/*31:0*/ Vq_fabric_top_q_cell::edges__BRA__3__KET____DOT__u_hebb__DOT__IIW;


void Vq_fabric_top_q_cell___ctor_var_reset(Vq_fabric_top_q_cell* vlSelf);

Vq_fabric_top_q_cell::Vq_fabric_top_q_cell(Vq_fabric_top__Syms* symsp, const char* v__name)
    : VerilatedModule{v__name}
    , vlSymsp{symsp}
 {
    // Reset structure values
    Vq_fabric_top_q_cell___ctor_var_reset(this);
}

void Vq_fabric_top_q_cell::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vq_fabric_top_q_cell::~Vq_fabric_top_q_cell() {
}
