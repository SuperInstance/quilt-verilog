// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vq_wall_gate.h for the primary calling header

#ifndef VERILATED_VQ_WALL_GATE___024ROOT_H_
#define VERILATED_VQ_WALL_GATE___024ROOT_H_  // guard

#include "verilated.h"


class Vq_wall_gate__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vq_wall_gate___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(rst_n,0,0);
    VL_IN8(i_go,0,0);
    VL_OUT8(o_running,0,0);
    VL_OUT8(o_bail,0,0);
    VL_OUT8(o_tval,0,0);
    VL_OUT8(o_cflag,0,0);
    VL_OUT8(o_nf,3,0);
    VL_OUT8(o_gopen,0,0);
    VL_OUT8(o_em_mask,6,0);
    CData/*1:0*/ q_wall_gate__DOT__st;
    CData/*6:0*/ q_wall_gate__DOT__trig;
    CData/*3:0*/ q_wall_gate__DOT__nf;
    CData/*3:0*/ q_wall_gate__DOT__neff;
    CData/*0:0*/ q_wall_gate__DOT__open_;
    CData/*0:0*/ q_wall_gate__DOT__cancel;
    CData/*0:0*/ q_wall_gate__DOT__sall;
    CData/*5:0*/ q_wall_gate__DOT____Vlvbound_h66797142__0;
    CData/*3:0*/ q_wall_gate__DOT____Vlvbound_h9637dd8d__0;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__rst_n__0;
    CData/*0:0*/ __VactContinue;
    VL_OUT16(o_t,13,0);
    SData/*14:0*/ q_wall_gate__DOT__t;
    SData/*14:0*/ q_wall_gate__DOT__last;
    VL_IN(i_seed,31,0);
    VL_OUTW(o_em_pm,335,0,11);
    VL_OUTW(o_em_e,335,0,11);
    IData/*31:0*/ q_wall_gate__DOT__lcg_x;
    IData/*31:0*/ q_wall_gate__DOT__lcg_next;
    IData/*31:0*/ __VactIterCount;
    VL_IN64(i_lats,41,0);
    VL_OUT64(o_resid,47,0);
    VL_OUT64(o_events,47,0);
    VL_OUT64(o_mass,47,0);
    VL_OUT64(o_cancels,47,0);
    VL_OUT64(o_chatter,47,0);
    VL_OUT64(o_settles,47,0);
    VL_OUT64(o_gopen_tot,47,0);
    VL_OUT64(o_gcomp,47,0);
    QData/*47:0*/ q_wall_gate__DOT__g;
    QData/*47:0*/ q_wall_gate__DOT__net;
    QData/*47:0*/ q_wall_gate__DOT__g_now;
    QData/*47:0*/ q_wall_gate__DOT__s_true;
    QData/*47:0*/ q_wall_gate__DOT__mtmp;
    QData/*47:0*/ q_wall_gate__DOT__dv;
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_h5108c7b6__1;
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_h3b3f478e__0;
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_h257e8aec__0;
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_hb12a105e__0;
    QData/*47:0*/ q_wall_gate__DOT____Vlvbound_heee9059e__1;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__2__Vfuncout;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__2__v;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__3__Vfuncout;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__3__v;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__4__Vfuncout;
    QData/*47:0*/ __Vfunc_q_wall_gate__DOT__f_abs__4__v;
    VlUnpacked<VlUnpacked<QData/*47:0*/, 7>, 1> q_wall_gate__DOT__mags;
    VlUnpacked<CData/*3:0*/, 1> q_wall_gate__DOT__cnt;
    VlUnpacked<CData/*5:0*/, 7> q_wall_gate__DOT__i_lats_reg;
    VlUnpacked<QData/*47:0*/, 7> q_wall_gate__DOT__reads;
    VlUnpacked<QData/*47:0*/, 7> q_wall_gate__DOT__errs;
    VlUnpacked<QData/*47:0*/, 7> q_wall_gate__DOT__pm_new;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<2> __VactTriggered;
    VlTriggerVec<2> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vq_wall_gate__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vq_wall_gate___024root(Vq_wall_gate__Syms* symsp, const char* v__name);
    ~Vq_wall_gate___024root();
    VL_UNCOPYABLE(Vq_wall_gate___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
